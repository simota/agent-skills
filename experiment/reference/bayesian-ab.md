# Bayesian A/B Testing Reference

Purpose: Design Bayesian A/B tests — specify priors, update with data to form posteriors, report credible intervals and probability-to-beat, and make decisions via ROPE (Region of Practical Equivalence) or expected loss. Bayesian A/B complements frequentist testing; it is the preferred framing when decision-makers think in probabilities rather than p-values.

## Scope Boundary

- **experiment `bayesian`**: Bayesian A/B design & analysis (this document).
- **experiment `ab` (elsewhere)**: Frequentist fixed-sample design.
- **experiment `sequential` (elsewhere)**: Anytime-valid frequentist.
- **experiment `analyze` (elsewhere)**: General result analysis.
- **Magi (elsewhere)**: Decision arbitration under uncertainty.
- **oracle (elsewhere)**: ML-adjacent Bayesian inference outside experiments.

## Why Bayesian A/B

| Question | Frequentist answer | Bayesian answer |
|----------|---------------------|-----------------|
| "Does treatment work?" | p-value / reject H0 | P(treatment > control \| data) |
| "By how much?" | CI (frequency interpretation) | Credible interval (probability interpretation) |
| "Should we ship?" | p < α + effect > MDE | P(uplift > threshold) + expected loss |
| "What if I peek?" | Invalidates inference | Posterior updates freely; decision rule separate |

**Communication advantage**: executives understand "80% probability treatment beats control by ≥ 2%" better than "p = 0.03".

**Caveats**: priors matter; Bayesian does not eliminate bias (bad prior = bad posterior); peeking still requires decision-rule discipline (ROPE or expected loss, not "ship when P(better) > 0.95").

## Core Model — Bernoulli / Conversion Metric

### Data
Binary outcomes (clicked / purchased / signed up). For each variant, observed `s` successes in `n` trials.

### Prior
Beta(α₀, β₀). Conjugate to Bernoulli.

| Prior strength | Beta params | Interpretation |
|----------------|-------------|----------------|
| Uninformative | Beta(1, 1) | Uniform [0,1] |
| Weakly informative | Beta(2, 2) | Centered at 0.5 |
| Informed by historical rate | Beta(α, β) s.t. α/(α+β) = historical rate, α+β = "effective past sample size" | Anchors to prior belief; data updates away |

### Posterior
Beta(α₀ + s, β₀ + n - s).

### Probability to beat
P(θ_T > θ_C) = ∫∫ [θ_T > θ_C] · posterior_T(θ_T) · posterior_C(θ_C) dθ_T dθ_C.

Closed form is awkward; in practice use Monte Carlo — draw 10k samples from each posterior, count fraction where T > C.

### Example

| Variant | s | n | Posterior |
|---------|---|---|-----------|
| Control | 250 | 5000 | Beta(251, 4751) |
| Treatment | 270 | 5000 | Beta(271, 4731) |

- Posterior mean control: 251/5002 ≈ 5.02%
- Posterior mean treatment: 271/5002 ≈ 5.42%
- P(T > C) via sampling ≈ 0.87
- P(uplift > 5% relative) ≈ 0.36

## Core Model — Continuous Metric (Revenue, AOV, etc.)

### Data
Continuous observations per user; may be heavy-tailed.

### Prior
Normal-Inverse-Gamma (conjugate to Normal likelihood with unknown mean and variance).

Alternatively: log-transform revenue → approximately normal; use Normal prior.

### Posterior
Normal-Inverse-Gamma updated. Samples from posterior predictive distribution.

### For heavy-tailed metrics
Bootstrapped differences or Bayesian bootstrap; or fit negative-binomial / log-normal / Tweedie.

## Decision Rules

Bayesian lets you pick a decision rule that matches business cost.

### Rule 1 — Probability to beat

Ship if P(θ_T > θ_C) > 0.95 (or 0.80, depending on risk appetite).

Simple, but can ship tiny "wins".

### Rule 2 — ROPE (Region of Practical Equivalence)

Define a ROPE around 0 (e.g., ±1% relative lift). Decision:
- If 95% credible interval on uplift is entirely above ROPE → ship.
- If entirely below → kill.
- If overlaps ROPE → inconclusive.

Forces you to state what's practically meaningful.

### Rule 3 — Expected loss

Compute expected loss for each action:
- L(ship) = E[max(θ_C - θ_T, 0)] — cost if treatment is actually worse.
- L(keep) = E[max(θ_T - θ_C, 0)] — cost of not shipping an improvement.

Ship when L(ship) < threshold (cost-aligned, e.g., $0.01/user). Statsig's engine uses this.

### Rule 4 — Value of Information

Cost-benefit of running longer vs deciding now. Classical Bayesian decision theory.

## Peeking Under Bayesian

Bayesian posteriors update freely with data, so peeking doesn't invalidate inference. But it invalidates **fixed decision thresholds** ("ship when P > 0.95") — you might cross 0.95 by chance if you check continuously.

Solutions:
- Use expected-loss stopping (ROPE) rather than probability-to-beat.
- Combine with sequential / always-valid frequentist bounds (confidence sequences).
- Accept the philosophy: peek, but decide via expected loss, not threshold-crossing.

## Prior Specification

Core challenge — priors matter, especially with small samples.

| Situation | Recommended prior |
|-----------|-------------------|
| No historical data | Weakly informative (Beta(1,1) or Beta(2,2)) |
| Strong historical baseline | Informed prior anchored to historical rate with effective sample size ≤ 10% of experiment n |
| Prior belief | Document explicit prior; sensitivity-analyze |
| Multi-tenant / multi-segment | Hierarchical model with partial pooling |

**Sensitivity analysis is mandatory**: re-run with weakly informative + informed priors; verify conclusion doesn't change.

## Hierarchical Models

For multi-segment experiments (per-country, per-plan), fit a hierarchical model where segment-specific effects share a common hyper-prior. Benefits:

- Partial pooling — segments with small n borrow strength from others.
- Shrinkage reduces false "winning" segments.
- Natural for heterogeneous treatment effects.

Use PyMC, Stan, or Turing.jl. Statsig and Eppo support hierarchical analysis.

## Workflow

```
FRAME       →  define metric (conversion / revenue / etc.)
            →  choose likelihood (Bernoulli / Normal / log-Normal / NB)

PRIOR       →  weakly informative by default
            →  if historical data exists, anchor with effective sample size ≤ 10% of expected n
            →  document explicitly

POWER       →  Bayesian "power" = P(correct decision) under true effect size
            →  Monte Carlo simulation under assumed truth

RUN         →  collect data
            →  SRM check per look (always)

POSTERIOR   →  update: posterior = prior × likelihood
            →  sample posteriors via MCMC or conjugate closed-form

REPORT      →  posterior mean + 95% credible interval
            →  P(T > C)
            →  P(uplift > X%)
            →  expected loss under ship / keep

DECIDE      →  apply decision rule (ROPE / expected loss)
            →  sensitivity-analyze prior

HANDOFF     →  Launch: if ship
            →  Magi: if ROPE inconclusive
            →  Pulse: update metric priors for future tests
```

## Output Template

```markdown
## Bayesian A/B Analysis: [Experiment]

### Model
- **Metric**: [conversion / revenue / ...]
- **Likelihood**: [Bernoulli / Normal / log-Normal / NB]
- **Prior**: [Beta(a, b) / Normal / hierarchical]
- **Rationale**: [historical rate / weakly informative / anchored]

### Data
| Variant | n | successes / mean | variance |
|---------|---|------------------|----------|
| Control | [...] | [...] | [...] |
| Treatment | [...] | [...] | [...] |

### SRM
- [ ] SRM passed (p ≥ 0.001)

### Posterior
| Variant | Posterior mean | 95% credible interval |
|---------|----------------|----------------------|
| Control | [...] | [...] |
| Treatment | [...] | [...] |
| Uplift (T − C) | [...] | [...] |

### Probabilities
- P(T > C) = [...]
- P(uplift > X%) = [...]
- P(in ROPE) = [...]

### Expected Loss
- L(ship) = [...]
- L(keep) = [...]
- Loss threshold: [...]

### Decision Rule Applied
- [ROPE / expected-loss / probability threshold]
- **Verdict**: SHIP / KEEP / MORE DATA

### Sensitivity Analysis
- Re-run with weakly informative prior: [same verdict / differs]
- Re-run with informed prior: [same / differs]

### Handoffs
- Launch: if SHIP
- Magi: if ambiguous
- Pulse: update historical priors
- Experiment Lead: post-mortem
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| No prior documentation | Document explicit prior; sensitivity-analyze |
| Too-strong prior dominates small-n test | Cap effective prior sample size ≤ 10% of data |
| Using "P > 0.95" with continuous peeking | Use ROPE or expected-loss stopping |
| Ignoring SRM because "Bayesian doesn't need it" | SRM still invalidates comparability; always check |
| Not sensitivity-analyzing prior | Prior that changes the verdict is a problem |
| Confusing credible interval with CI | They mean different things; use Bayesian language |
| Ignoring ROPE | "P > 0.95 for any tiny uplift" ships trivial changes |
| Bayesian with bad likelihood choice | Revenue is not Normal; use log-Normal or NB |
| Shipping without expected-loss analysis | Cost-aware decision-making is the point of Bayesian |

## Deliverable Contract

When `bayesian` completes, emit:

- **Model** (metric, likelihood, prior with rationale).
- **Posterior** (means + credible intervals per variant and uplift).
- **Probability statements** (P(T > C), P(uplift > X%), P(in ROPE)).
- **Expected loss** computation.
- **Decision rule + verdict** (ROPE or expected-loss based).
- **Sensitivity analysis** across priors.
- **SRM check** (always).
- **Handoffs**: Launch, Magi, Pulse.

## References

- Gelman, Carlin, Stern, Dunson, Vehtari, Rubin — *Bayesian Data Analysis* (3rd ed, 2013)
- Kruschke — *Doing Bayesian Data Analysis* (2nd ed, 2014) — introduces ROPE
- Kruschke & Liddell — "Bayesian New Statistics" (2018) — ROPE + credible intervals
- VWO — "Bayesian Testing for Online Experimentation" whitepaper
- Statsig (now part of OpenAI Applications post 2025-09 acquisition) — expected-loss decision engine documentation
- Eppo by Datadog (post 2025-05 acquisition) — Bayesian framework docs
- LaunchDarkly — *Experimentation statistical methodology for Bayesian experiments* (2025 docs) and *"Experimentation your way: Introducing Frequentist and Bayesian experiments in LaunchDarkly"* blog
- PostHog — new experimentation engine docs (Bayesian default, Frequentist optional)
- Chris Stucchio — "Bayesian vs Frequentist A/B Testing" (Wayfair engineering blog)
- PyMC / Stan / Turing.jl / CmdStanR — Bayesian inference libraries
- Evan Miller — "Simple Sequential A/B Testing" (frequentist sequential counterpart)
- Kohavi / Tang / Xu — *Trustworthy Online Controlled Experiments* (2020) — pragmatic Bayesian chapter
- Spotify Engineering — *Risk-Aware Product Decisions in A/B Tests with Multiple Metrics* (Mar 2024) — expected-loss decision rules across a metric portfolio; *Beyond Win Rates: How Spotify Quantifies Learning in Product Experiments* (InfoQ 2025)
