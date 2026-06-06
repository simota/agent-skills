# Adaptive Experimentation

## MAB vs A/B Test Selection Framework

Use this table to decide between classical A/B testing and Multi-Armed Bandit (MAB) approaches.

| Criterion | Traditional A/B Test | Multi-Armed Bandit (MAB) |
|-----------|---------------------|--------------------------|
| **Primary goal** | Causal inference, learning | Regret minimization, earning |
| **Reward signal** | Delayed OK (days to weeks) | Immediate required (same session) |
| **Number of variants** | 2-4 | 2-10+ |
| **Traffic allocation** | Fixed (e.g., 50/50) | Dynamic (shifts to winner over time) |
| **Statistical validity** | Strong (frequentist guarantee) | Weaker (no fixed hypothesis) |
| **Experiment duration** | Fixed (pre-calculated) | Flexible (can run indefinitely) |
| **Novelty effect** | Handled with proper duration | Risk of premature convergence |
| **Use cases** | UI redesign, pricing, onboarding | Recommendation, ad selection, content ranking |
| **Interpretability** | High (clear winner/loser) | Lower (probabilistic allocation) |

**Rule of thumb:** Use A/B test when learning matters most; use MAB when earning matters most.

---

## Thompson Sampling Implementation

Thompson Sampling is the recommended MAB algorithm due to its simplicity and strong empirical performance.

**Core concept:** Maintain a Beta distribution for each arm's estimated reward probability. At each step, sample from each arm's distribution and select the arm with the highest sample.

```typescript
// Full implementation is in statistical-methods.md → Thompson Sampling section

// Usage example:
const sampler = new ThompsonSampler(['control', 'checkout_v2', 'checkout_v3']);

// For each user request:
const arm = sampler.selectArm();  // Dynamically selects based on posteriors

// After observing outcome:
sampler.update(arm, reward);  // reward: 1 for conversion, 0 for no conversion

// Monitor progress:
const stats = sampler.getStats();
// [{ name: 'control', estimatedRate: 0.05, uncertainty: 0.002 },
//  { name: 'checkout_v2', estimatedRate: 0.065, uncertainty: 0.001 },
//  ...]
```

**When to stop Thompson Sampling:**

```typescript
interface ConvergenceCheck {
  winner: string | null;    // null if not converged
  confidence: number;       // P(this arm is truly best)
  allocationShare: number;  // Current traffic share going to leading arm
}

function checkConvergence(
  stats: Array<{ name: string; estimatedRate: number; uncertainty: number }>,
  confidenceThreshold = 0.95
): ConvergenceCheck {
  // Monte Carlo: sample 10,000 times, check if one arm consistently wins
  const nSamples = 10_000;
  const winCounts: Record<string, number> = {};

  for (let i = 0; i < nSamples; i++) {
    let bestArm = stats[0].name;
    let bestSample = -Infinity;
    for (const arm of stats) {
      // Sample from arm's posterior (approximate with normal)
      const sample = arm.estimatedRate + arm.uncertainty * gaussianRandom();
      if (sample > bestSample) { bestSample = sample; bestArm = arm.name; }
    }
    winCounts[bestArm] = (winCounts[bestArm] ?? 0) + 1;
  }

  const topArm = Object.entries(winCounts)
    .sort((a, b) => b[1] - a[1])[0];
  const confidence = topArm[1] / nSamples;

  return {
    winner: confidence >= confidenceThreshold ? topArm[0] : null,
    confidence,
    allocationShare: 0 // calculated separately from current allocation
  };
}

function gaussianRandom(): number {
  const u1 = Math.random(), u2 = Math.random();
  return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
}
```

---

## Automatic Stopping Rules

### mSPRT (mixture Sequential Probability Ratio Test)

mSPRT provides valid inference at any stopping time — you can peek continuously without inflating Type I error.

**Key property:** The p-value from mSPRT is valid at any sample size, not just the pre-planned target.

```typescript
interface MSPRTState {
  logLikelihoodRatio: number;
  n: number;
  controlSuccesses: number;
  treatmentSuccesses: number;
}

function updateMSPRT(
  state: MSPRTState,
  controlEvent: 0 | 1,
  treatmentEvent: 0 | 1,
  nullEffect = 0,        // H₀: no effect
  mixingVariance = 0.01  // prior variance on effect size
): MSPRTState & { shouldStop: boolean; pValue: number } {
  const newState: MSPRTState = {
    logLikelihoodRatio: state.logLikelihoodRatio,
    n: state.n + 1,
    controlSuccesses: state.controlSuccesses + controlEvent,
    treatmentSuccesses: state.treatmentSuccesses + treatmentEvent
  };

  // Compute log-likelihood ratio update (simplified for proportions)
  const p0 = (newState.controlSuccesses + 1) / (newState.n + 2);
  const p1 = (newState.treatmentSuccesses + 1) / (newState.n + 2);
  const observedEffect = p1 - p0 - nullEffect;

  // mSPRT statistic: cumulative product of likelihood ratios
  const llrUpdate = observedEffect * observedEffect / (2 * mixingVariance);
  newState.logLikelihoodRatio += llrUpdate;

  // Convert to p-value: p = 1/e^(logLikelihoodRatio)
  const pValue = Math.exp(-newState.logLikelihoodRatio);

  return {
    ...newState,
    shouldStop: pValue < 0.05,
    pValue
  };
}
```

### Always Valid P-values (Confidence Sequences)

A simpler alternative: use confidence sequences that maintain validity at all sample sizes.

```typescript
function alwaysValidPValue(
  control: { conversions: number; total: number },
  treatment: { conversions: number; total: number },
  rho = 0.5  // mixing parameter (0 < rho < 1, smaller = more conservative)
): { pValue: number; isSignificant: boolean } {
  const n = control.total + treatment.total;
  const p1 = control.conversions / control.total;
  const p2 = treatment.conversions / treatment.total;
  const diff = p2 - p1;

  // Boundary that valid p-values must stay below
  const boundary = Math.sqrt((2 * Math.log(1 / rho) + Math.log(n + 1)) / n);
  const zStat = Math.abs(diff) / boundary;

  // Convert to p-value (approximate)
  const pValue = 2 * (1 - normalCDF(zStat));

  return {
    pValue: Math.min(1, pValue),
    isSignificant: Math.abs(diff) > boundary
  };
}

function normalCDF(x: number): number {
  return 0.5 * (1 + erf(x / Math.sqrt(2)));
}

function erf(x: number): number {
  const t = 1 / (1 + 0.3275911 * Math.abs(x));
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
    - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  return x >= 0 ? y : -y;
}
```

---

## Contextual Bandit Overview

Contextual bandits extend MAB by conditioning the arm selection on user context features. This allows personalization: different variants may win for different user segments.

**When to use contextual bandits:**
- Heterogeneous treatment effects are expected (e.g., a feature helps mobile users but hurts desktop)
- User features are available at decision time (device, location, past behavior)
- You have enough traffic to learn per-segment policies (rule of thumb: 10x more traffic than standard A/B)

**Architecture pattern:**

```
User Request
    │
    ▼
Feature Extraction     ← user_id, device, geo, past_behavior
    │
    ▼
Contextual Policy      ← LinUCB, EpsilonGreedy, Neural Bandit
    │
    ▼
Arm Selection          ← variant_A | variant_B | variant_C
    │
    ▼
Reward Observation     ← click, purchase, engagement
    │
    ▼
Policy Update          ← online learning
```

**Simplified LinUCB-inspired approach (TypeScript):**

```typescript
interface ContextualArm {
  name: string;
  // A: covariance matrix (d×d), b: reward vector (d×1)
  A: number[][];
  b: number[];
}

class SimpleContextualBandit {
  private arms: ContextualArm[];
  private alpha: number; // exploration parameter

  constructor(armNames: string[], featureDim: number, alpha = 1.0) {
    this.alpha = alpha;
    this.arms = armNames.map(name => ({
      name,
      A: identityMatrix(featureDim),
      b: new Array(featureDim).fill(0)
    }));
  }

  selectArm(features: number[]): string {
    let bestArm = this.arms[0].name;
    let bestScore = -Infinity;

    for (const arm of this.arms) {
      // UCB score = θᵀx + α * sqrt(xᵀA⁻¹x)
      const theta = solveLinearSystem(arm.A, arm.b);
      const meanReward = dotProduct(theta, features);
      const uncertainty = this.alpha * Math.sqrt(
        dotProduct(features, solveLinearSystem(arm.A, features))
      );
      const score = meanReward + uncertainty;

      if (score > bestScore) { bestScore = score; bestArm = arm.name; }
    }

    return bestArm;
  }

  update(armName: string, features: number[], reward: number): void {
    const arm = this.arms.find(a => a.name === armName);
    if (!arm) return;
    // A += xxᵀ, b += r*x
    for (let i = 0; i < features.length; i++) {
      for (let j = 0; j < features.length; j++) {
        arm.A[i][j] += features[i] * features[j];
      }
      arm.b[i] += reward * features[i];
    }
  }
}

// Placeholder helpers (use a proper linear algebra library in production)
function identityMatrix(n: number): number[][] {
  return Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => i === j ? 1 : 0)
  );
}

function dotProduct(a: number[], b: number[]): number {
  return a.reduce((sum, v, i) => sum + v * b[i], 0);
}

function solveLinearSystem(A: number[][], b: number[]): number[] {
  // NOTE: Use a real linear algebra library (e.g., mathjs) in production
  // This is a placeholder for the concept
  return b.map((_, i) => b[i] / A[i][i]);
}
```

**Important caveats for contextual bandits:**
- Reward delay creates off-policy evaluation challenges
- Feature selection significantly impacts policy quality
- Evaluation requires offline counterfactual estimation (IPW, DM, DR estimators)
- Consider using proven libraries (Vowpal Wabbit, ML.NET, or cloud ML platforms) over custom implementation

---

## LLM / AI Feature Experimentation (2026-05)

Generative-AI features (LLM prompts, retrieval pipelines, model selection, agentic tools) introduce experimentation patterns that diverge from classical A/B:

- **High output variance**: identical inputs produce different outputs across calls; per-call cost can dominate experiment economics.
- **No fixed ground truth**: quality is often judged pairwise (which response is better?) rather than against a labeled answer.
- **Cold-start sparsity**: many prompt experiments run on weeks of data with thousands of samples, not millions.

### Pairwise preference evaluation (LMSYS-style)

The LMSYS Chatbot Arena methodology (Chiang et al., arXiv:2403.04132, "Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference") fits a **Bradley-Terry (1952) model** to pairwise human preference votes and reports an Elo-like score with bootstrap confidence intervals. This is the de facto industry standard for LLM-vs-LLM evaluation in 2026 and a direct analog of `interleaving-tests.md` for the LLM domain — both reduce between-user variance by asking "which is better?" within a single user, instead of comparing rates between groups. For implementation, see also Vovk & Wang (2021) e-values, used in newer Arena methodology iterations to obtain valid stopping decisions while ranking models.

### Prompt A/B testing tools (2026)

| Tool | Strengths | Use when |
|------|-----------|----------|
| **Promptfoo** (OSS CLI/library) | Declarative YAML configs, CI/CD-friendly, model-agnostic, security/red-team scanning | Inner-loop dev, CI gating, pre-deploy sanity checks |
| **Braintrust** | Comparison UI, AI assistant ("Loop") for prompt iteration, collaboration features | Pre-release batch eval with human sign-off |
| **LangSmith** | Tracing, prompt management, evaluation tightly integrated with LangChain stack | LangChain-based agents/RAG |
| **OpenAI Evals** | First-party from OpenAI; standard for OpenAI model-vs-model evaluation | Validating against OpenAI model upgrades |
| **Helicone**, **Maxim**, **Arize Phoenix** | Production observability + evaluation | Live LLM apps needing tracing + eval together |

Pattern (per Braintrust 2025 guidance and Promptfoo 2026 docs): run **Promptfoo in CI on every commit** (free, fast), then a **batch evaluation pass with Braintrust or LangSmith with human sign-off** before shipping a prompt change to production.

### LLM-as-judge

When pairwise human voting is infeasible, an LLM-as-judge (e.g., GPT-4-class model rating two candidate responses) is the production fallback. Validate the judge against a small human-labeled subset and report inter-rater agreement; treat the judge as a noisy oracle, not ground truth. The Arena Hard methodology and follow-up "Arena Hard Auto" line of work (LMSYS / SkyworkAI 2025 reviews) use this with calibration on Chatbot Arena votes.

### Variance reduction on LLM metrics

LLM outputs amplify the heavy-tail problem on cost, latency, and judge scores. Apply Winsorization at the 99th percentile on token-count and latency, and consider CUPED with the previous-week per-user prompt-success rate as covariate when running prompt A/B on repeat users.
