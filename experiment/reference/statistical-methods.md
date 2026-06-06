# Statistical Methods for Experiments

## Test Selection Guide

| Metric Type | Test | When to Use |
|-------------|------|-------------|
| Binary (conversion) | Z-test for proportions | Standard A/B test |
| Continuous (revenue) | Welch's t-test | Revenue per user |
| Count (clicks) | Chi-square | Multiple categories |
| Time-to-event | Log-rank test | Time to conversion |

## Interpreting Results

| p-value | Conclusion |
|---------|------------|
| < 0.01 | Strong evidence |
| 0.01-0.05 | Moderate evidence |
| 0.05-0.10 | Weak evidence |
| > 0.10 | No significant evidence |

> **Modern guidance**: Do not rely on p-value alone. Always report effect size (absolute and relative lift), confidence interval, and practical significance. For multiple metrics, apply FDR control (Benjamini-Hochberg) rather than treating each p-value independently. Sequential testing (mSPRT / confidence sequences) replaces fixed-horizon p-values when continuous monitoring is required — these yield always-valid p-values that remain valid under peeking. (Source: Johari et al. 2022, "Always Valid Inference", *Operations Research* — https://pubsonline.informs.org/doi/10.1287/opre.2021.2135)

## Common Pitfalls
1. **Peeking**: Checking results before reaching sample size inflates false positives
2. **Multiple comparisons**: Testing many metrics without correction
3. **Selection bias**: Non-random assignment to variants
4. **Novelty effect**: Short tests may capture excitement, not sustained behavior

---

## Z-Test for Proportions (Binary Metrics)

```typescript
interface ExperimentResult {
  control: { conversions: number; total: number };
  treatment: { conversions: number; total: number };
}

interface AnalysisResult {
  controlRate: number;
  treatmentRate: number;
  relativeLift: number;
  absoluteLift: number;
  zScore: number;
  pValue: number;
  isSignificant: boolean;
  confidenceInterval: [number, number];
}

function analyzeExperiment(
  result: ExperimentResult,
  significance: number = 0.05
): AnalysisResult {
  const { control, treatment } = result;

  // Conversion rates
  const p1 = control.conversions / control.total;
  const p2 = treatment.conversions / treatment.total;

  // Pooled proportion
  const pPooled = (control.conversions + treatment.conversions) /
                  (control.total + treatment.total);

  // Standard error
  const se = Math.sqrt(
    pPooled * (1 - pPooled) * (1/control.total + 1/treatment.total)
  );

  // Z-score
  const zScore = (p2 - p1) / se;

  // P-value (two-tailed)
  const pValue = 2 * (1 - normalCDF(Math.abs(zScore)));

  // 95% Confidence interval for the difference
  const zAlpha = 1.96;
  const seDiff = Math.sqrt(
    p1 * (1 - p1) / control.total +
    p2 * (1 - p2) / treatment.total
  );
  const ci: [number, number] = [
    (p2 - p1) - zAlpha * seDiff,
    (p2 - p1) + zAlpha * seDiff
  ];

  return {
    controlRate: p1,
    treatmentRate: p2,
    relativeLift: (p2 - p1) / p1,
    absoluteLift: p2 - p1,
    zScore,
    pValue,
    isSignificant: pValue < significance,
    confidenceInterval: ci
  };
}

// Normal CDF approximation
function normalCDF(x: number): number {
  const a1 =  0.254829592;
  const a2 = -0.284496736;
  const a3 =  1.421413741;
  const a4 = -1.453152027;
  const a5 =  1.061405429;
  const p  =  0.3275911;

  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x) / Math.sqrt(2);

  const t = 1.0 / (1.0 + p * x);
  const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

  return 0.5 * (1.0 + sign * y);
}
```

---

## CUPED — Controlled experiment Using Pre-Experiment Data

CUPED reduces variance in experiment metrics by removing the component explained by pre-experiment covariates, allowing you to detect smaller effects with the same sample size. Introduced by Deng, Xu, Kohavi, Walker (Microsoft, WSDM 2013).

**Core formula:**

```
Y_adj = Y - θ * X
θ = Cov(Y, X) / Var(X)

Var(Y_adj) = Var(Y) × (1 – Cor(Y, X)²)
```

Where `X` is the pre-experiment covariate (e.g., last 30 days metric), `Y` is the experiment outcome metric, and `θ` is the regression coefficient.

**Variance reduction:** If `Cor(Y, X) = 0.5`, variance is reduced by 25%. If `Cor(Y, X) = 0.8`, variance is reduced by 64%.

**When to apply CUPED:**
- Pre-experiment data for the same metric is available (at least 2 weeks)
- The covariate correlates with the outcome metric (|Cor| > 0.2)
- You need to reduce experiment duration without sacrificing power

### CUPED variants and ML-based extensions (2026 state of the art)

The CUPED family has diverged into several production-grade variants. Pick by data availability and platform support.

| Variant | Mechanism | Key paper / origin | Use when |
|---------|-----------|--------------------|----------|
| Classical CUPED | Single pre-experiment covariate (typically prior-period outcome) | Deng et al. (Microsoft, WSDM 2013) | Strong pre-period signal, simple metric |
| **CUPAC** | ML model (e.g., GBM) predicts Y from pre-experiment features; prediction used as covariate | DoorDash — Jeff Li, Yixin Tang, Jared Bauman (2020 DoorDash Engineering blog) | Multiple pre-period features, non-linear relations |
| **MLRATE** | Cross-fit ML regression-adjusted treatment effect; consistent + asymptotically normal even with weak ML | Guo, Coey, Konutgan, Li, Schoener, Goldman (NeurIPS 2021) — at Meta/Facebook, ~70% variance reduction vs diff-in-means across 48 metrics, ~19% over univariate CUPED | Heterogeneous metrics, big-ML environment |
| **CUPED++** | Adds *assignment-time* covariates (device, region, traffic source) as additional regression terms; works even with no pre-experiment data (e.g., onboarding flows) | Eppo (now "Eppo by Datadog" after May 2025 acquisition); per Eppo: up to ~65% faster experiments | New-user experiments, when pre-period data is missing |
| **Full regression adjustment (Negi-Wooldridge)** | Treats CUPED as a special case of regression adjustment with heterogeneous treatment effects; tighter CIs than classical CUPED | Negi & Wooldridge (2021, *Econometric Reviews*); Spotify Confidence uses this as the default estimator | Heterogeneous treatment effects across covariates |
| **Pre + in-experiment combined** | Combines pre-experiment covariates with early-period (in-experiment) covariates while avoiding post-treatment bias | Guo et al., "Variance reduction combining pre-experiment and in-experiment data" (arXiv:2410.09027, 2024 / PMLR 2026) | When in-experiment early outcomes add precision over pre-period only |

Anti-pattern: using a treatment-influenced covariate (anything measured after exposure) as a CUPED control variate introduces bias — covariates must be either strictly pre-experiment, or carefully orthogonalized as in the Guo et al. (2024) framework.

**TypeScript implementation:**

```typescript
interface CupedData {
  userId: string;
  preExperimentValue: number; // X: covariate
  experimentValue: number;    // Y: outcome during experiment
  variant: 'control' | 'treatment';
}

function computeTheta(data: CupedData[]): number {
  const n = data.length;
  const meanY = data.reduce((s, d) => s + d.experimentValue, 0) / n;
  const meanX = data.reduce((s, d) => s + d.preExperimentValue, 0) / n;

  const cov = data.reduce((s, d) =>
    s + (d.experimentValue - meanY) * (d.preExperimentValue - meanX), 0) / n;
  const varX = data.reduce((s, d) =>
    s + Math.pow(d.preExperimentValue - meanX, 2), 0) / n;

  return cov / varX;
}

function applyCuped(data: CupedData[]): Array<CupedData & { adjustedValue: number }> {
  const theta = computeTheta(data);
  const globalMeanX = data.reduce((s, d) => s + d.preExperimentValue, 0) / data.length;

  return data.map(d => ({
    ...d,
    // Subtract the covariate contribution relative to the global mean
    adjustedValue: d.experimentValue - theta * (d.preExperimentValue - globalMeanX)
  }));
}

function analyzeCuped(data: CupedData[], significance = 0.05): AnalysisResult {
  const adjusted = applyCuped(data);
  const control = adjusted.filter(d => d.variant === 'control').map(d => d.adjustedValue);
  const treatment = adjusted.filter(d => d.variant === 'treatment').map(d => d.adjustedValue);

  // Use standard t-test on adjusted values
  return analyzeWithWelchTTest(control, treatment, significance);
}

function analyzeWithWelchTTest(
  control: number[],
  treatment: number[],
  significance: number
): AnalysisResult {
  const n1 = control.length, n2 = treatment.length;
  const mean1 = control.reduce((a, b) => a + b, 0) / n1;
  const mean2 = treatment.reduce((a, b) => a + b, 0) / n2;
  const var1 = control.reduce((s, v) => s + Math.pow(v - mean1, 2), 0) / (n1 - 1);
  const var2 = treatment.reduce((s, v) => s + Math.pow(v - mean2, 2), 0) / (n2 - 1);
  const se = Math.sqrt(var1 / n1 + var2 / n2);
  const tStat = (mean2 - mean1) / se;
  const pValue = 2 * (1 - normalCDF(Math.abs(tStat)));
  const zAlpha = 1.96;
  const ci: [number, number] = [
    (mean2 - mean1) - zAlpha * se,
    (mean2 - mean1) + zAlpha * se
  ];
  return {
    controlRate: mean1,
    treatmentRate: mean2,
    relativeLift: (mean2 - mean1) / Math.abs(mean1),
    absoluteLift: mean2 - mean1,
    zScore: tStat,
    pValue,
    isSignificant: pValue < significance,
    confidenceInterval: ci
  };
}
```

---

## Bayesian A/B Testing

Bayesian methods produce probability statements ("there is a 95% probability that treatment is better") rather than binary significance decisions. This avoids the peeking problem and is more interpretable.

### Beta-Binomial Model (for conversion metrics)

For binary outcomes (converted / not converted), the Beta distribution is the conjugate prior to the Binomial likelihood.

**Prior:** `Beta(α₀, β₀)` — typically `Beta(1, 1)` (uniform/non-informative)

**Posterior update:** After observing `k` conversions out of `n` trials:
```
Posterior = Beta(α₀ + k, β₀ + n - k)
```

**Posterior predictive probability that treatment > control:**
Computed via Monte Carlo sampling from both posteriors.

```typescript
interface BayesianResult {
  controlPosterior: { alpha: number; beta: number };
  treatmentPosterior: { alpha: number; beta: number };
  probTreatmentBetter: number;
  expectedLift: number;
  credibleInterval: [number, number]; // 95% HDI on lift
}

function bayesianAbTest(
  control: { conversions: number; total: number },
  treatment: { conversions: number; total: number },
  priorAlpha = 1,
  priorBeta = 1,
  nSamples = 100_000
): BayesianResult {
  const controlPost = {
    alpha: priorAlpha + control.conversions,
    beta: priorBeta + (control.total - control.conversions)
  };
  const treatmentPost = {
    alpha: priorAlpha + treatment.conversions,
    beta: priorBeta + (treatment.total - treatment.conversions)
  };

  // Monte Carlo: sample from both posteriors
  const controlSamples = sampleBeta(controlPost.alpha, controlPost.beta, nSamples);
  const treatmentSamples = sampleBeta(treatmentPost.alpha, treatmentPost.beta, nSamples);

  const wins = treatmentSamples.filter((t, i) => t > controlSamples[i]).length;
  const lifts = treatmentSamples.map((t, i) => (t - controlSamples[i]) / controlSamples[i]);

  lifts.sort((a, b) => a - b);
  const credibleInterval: [number, number] = [
    lifts[Math.floor(nSamples * 0.025)],
    lifts[Math.floor(nSamples * 0.975)]
  ];

  return {
    controlPosterior: controlPost,
    treatmentPosterior: treatmentPost,
    probTreatmentBetter: wins / nSamples,
    expectedLift: lifts.reduce((a, b) => a + b, 0) / nSamples,
    credibleInterval
  };
}

// Beta distribution sampler using Johnk's method
function sampleBeta(alpha: number, beta: number, n: number): number[] {
  return Array.from({ length: n }, () => {
    // Approximation via normal when alpha and beta are large
    if (alpha > 1 && beta > 1) {
      const mean = alpha / (alpha + beta);
      const variance = (alpha * beta) / (Math.pow(alpha + beta, 2) * (alpha + beta + 1));
      return Math.max(0, Math.min(1, mean + Math.sqrt(variance) * gaussianRandom()));
    }
    // Exact: use gamma variates ratio
    const x = gammaSample(alpha);
    const y = gammaSample(beta);
    return x / (x + y);
  });
}

function gaussianRandom(): number {
  // Box-Muller transform
  const u1 = Math.random(), u2 = Math.random();
  return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
}

function gammaSample(shape: number): number {
  // Marsaglia-Tsang method approximation
  if (shape < 1) return gammaSample(1 + shape) * Math.pow(Math.random(), 1 / shape);
  const d = shape - 1 / 3;
  const c = 1 / Math.sqrt(9 * d);
  while (true) {
    let x: number, v: number;
    do { x = gaussianRandom(); v = 1 + c * x; } while (v <= 0);
    v = v * v * v;
    const u = Math.random();
    if (u < 1 - 0.0331 * (x * x) * (x * x)) return d * v;
    if (Math.log(u) < 0.5 * x * x + d * (1 - v + Math.log(v))) return d * v;
  }
}
```

### Frequentist vs Bayesian Comparison

| Aspect | Frequentist (Z-test) | Bayesian (Beta-Binomial) |
|--------|---------------------|--------------------------|
| **Output** | p-value, reject/fail to reject H₀ | P(treatment > control), credible interval |
| **Interpretation** | "If H₀ is true, data this extreme occurs X% of the time" | "There is X% probability treatment is better" |
| **Peeking** | Inflates false positive rate | Can monitor continuously with proper stopping rules |
| **Prior knowledge** | Not incorporated | Can incorporate via informative priors |
| **Sample size** | Required upfront | More flexible; stop when confidence is sufficient |
| **Common use** | Standard industry A/B tests | Continuous experimentation, revenue optimization |

---

## Thompson Sampling

Thompson Sampling is a Bayesian bandit algorithm that allocates more traffic to better-performing variants dynamically — balancing exploration (learning) and exploitation (earning).

**When to use Thompson Sampling over A/B testing:**
- Reward is immediate (not delayed conversion)
- You want to minimize regret during the experiment
- Variants are clearly ordered by performance (not complex interactions)
- See `reference/adaptive-experimentation.md` for full MAB vs A/B selection guide

```typescript
interface ThompsonArm {
  name: string;
  alpha: number; // successes + prior_alpha
  beta: number;  // failures + prior_beta
}

class ThompsonSampler {
  private arms: ThompsonArm[];

  constructor(armNames: string[], priorAlpha = 1, priorBeta = 1) {
    this.arms = armNames.map(name => ({
      name,
      alpha: priorAlpha,
      beta: priorBeta
    }));
  }

  // Select arm by sampling from each arm's Beta posterior
  selectArm(): string {
    const samples = this.arms.map(arm => ({
      name: arm.name,
      sample: sampleBeta(arm.alpha, arm.beta, 1)[0]
    }));
    return samples.reduce((best, s) => s.sample > best.sample ? s : best).name;
  }

  // Update arm with observed reward (1 = success, 0 = failure)
  update(armName: string, reward: 0 | 1): void {
    const arm = this.arms.find(a => a.name === armName);
    if (!arm) return;
    arm.alpha += reward;
    arm.beta += 1 - reward;
  }

  getStats(): Array<{ name: string; estimatedRate: number; uncertainty: number }> {
    return this.arms.map(arm => ({
      name: arm.name,
      estimatedRate: arm.alpha / (arm.alpha + arm.beta),
      uncertainty: Math.sqrt(
        (arm.alpha * arm.beta) /
        (Math.pow(arm.alpha + arm.beta, 2) * (arm.alpha + arm.beta + 1))
      )
    }));
  }
}
```

---

## Example Analysis

```typescript
const result = analyzeExperiment({
  control: { conversions: 500, total: 10000 },      // 5.0%
  treatment: { conversions: 550, total: 10000 }     // 5.5%
});

console.log(`
Control Rate: ${(result.controlRate * 100).toFixed(2)}%
Treatment Rate: ${(result.treatmentRate * 100).toFixed(2)}%
Relative Lift: ${(result.relativeLift * 100).toFixed(1)}%
P-Value: ${result.pValue.toFixed(4)}
Significant: ${result.isSignificant ? 'Yes' : 'No'}
95% CI: [${(result.confidenceInterval[0] * 100).toFixed(2)}%, ${(result.confidenceInterval[1] * 100).toFixed(2)}%]
`);
```
