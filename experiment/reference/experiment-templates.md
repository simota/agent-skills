# Experiment Templates

## Hypothesis Document Template

```markdown
## Experiment: [Experiment Name]

### Hypothesis
**If** [we make this change]
**Then** [this metric will improve]
**Because** [this is the underlying mechanism]

### Background
- **Problem Statement:** [What problem are we solving?]
- **Current State:** [Current metric value and user behavior]
- **Evidence:** [What data/research supports this hypothesis?]

### Variants
| Variant | Description | Traffic Allocation |
|---------|-------------|--------------------|
| Control | Current experience | 50% |
| Treatment | [Describe change] | 50% |

### Metrics
**Primary Metric (Decision Metric):**
- Metric: [Name]
- Definition: [Exact calculation]
- Current Baseline: [X%]
- MDE (Minimum Detectable Effect): [Y%]
- Expected Lift: [Z%]

**Secondary Metrics (Reference Metrics):**
1. [Metric name] - [Definition]
2. [Metric name] - [Definition]

**Guardrail Metrics (Guardrail Metrics):**
1. [Metric name] - [Threshold that should not be crossed]
2. [Metric name] - [Threshold]

### Sample Size & Duration
- Required Sample Size: [N per variant]
- Current Daily Traffic: [N users]
- Expected Duration: [X days/weeks]
- Statistical Power: 80%
- Significance Level: 5%

### Success Criteria
- [ ] Primary metric shows statistically significant improvement
- [ ] No guardrail metrics violated
- [ ] Lift >= MDE

### Rollout Plan
- **If wins:** Roll out to 100% on [date]
- **If loses:** Revert and [next action]
- **If inconclusive:** [Extend / iterate / abandon]
```

---

## Experiment Report Template

```markdown
## Experiment Report: [Experiment Name]

### Summary
| Metric | Control | Treatment | Lift | P-Value | Significant |
|--------|---------|-----------|------|---------|-------------|
| Primary: [Name] | X% | Y% | +Z% | 0.0XX | Yes/No |
| Secondary: [Name] | X | Y | +Z% | 0.0XX | Yes/No |
| Guardrail: [Name] | X | Y | -Z% | 0.0XX | No violation |

### Recommendation
**[SHIP / ITERATE / ABANDON]**

[1-2 sentences explaining the recommendation]

### Key Findings
1. [Finding 1 with data support]
2. [Finding 2 with data support]
3. [Finding 3 with data support]

### Detailed Results

#### Primary Metric: [Name]
- Control: [X%] (n=[N])
- Treatment: [Y%] (n=[N])
- Relative Lift: [+Z%]
- 95% CI: [[L%, U%]]
- P-Value: [0.0XX]
- Statistical Power Achieved: [X%]

#### Segment Analysis
| Segment | Control | Treatment | Lift | Significant |
|---------|---------|-----------|------|-------------|
| Mobile | X% | Y% | +Z% | Yes/No |
| Desktop | X% | Y% | +Z% | Yes/No |
| New Users | X% | Y% | +Z% | Yes/No |
| Returning Users | X% | Y% | +Z% | Yes/No |

### Timeline
- Started: [Date]
- Ended: [Date]
- Duration: [X days]
- Total Participants: [N]

### Learnings & Next Steps
1. [Learning 1] → [Next step]
2. [Learning 2] → [Next step]

### Appendix
- [Link to hypothesis document]
- [Link to raw data]
- [Link to dashboard]
```

---

## Experimentation Maturity Model

Use this model to assess your team's current experimentation capability and plan the next step.

| Level | Name | Characteristics |
|-------|------|----------------|
| **Level 1** | Ad Hoc | Experiments run without documentation; no pre-registration; results interpreted post-hoc |
| **Level 2** | Defined | Standard hypothesis template used; sample size calculated upfront; primary metric pre-registered |
| **Level 3** | Managed | Automated assignment and tracking; SRM checks; sequential testing available; centralized platform |
| **Level 4** | Optimized | CUPED variance reduction; automated guardrail monitoring; experimentation culture across teams |
| **Level 5** | Continuous | Always-on adaptive experiments (bandits); warehouse-native analysis; organization-wide learning loops |

---

## Experiment Review Process Template

```markdown
## Pre-Launch Review Checklist

### Hypothesis Quality
- [ ] Falsifiable hypothesis stated (If/Then/Because)
- [ ] Primary metric pre-registered and owned by one team
- [ ] Guardrail metrics defined with explicit thresholds
- [ ] Minimum detectable effect (MDE) is practically significant

### Statistical Design
- [ ] Power analysis completed (80%+ power, 5% significance)
- [ ] Sample size achievable within experiment duration
- [ ] Randomization unit appropriate (user-level, session-level, etc.)
- [ ] No overlapping experiments on same population

### Technical Setup
- [ ] Feature flag configured and tested in staging
- [ ] Exposure tracking implemented and verified
- [ ] SRM check query prepared
- [ ] Rollback plan documented

### Ethical / Risk Review
- [ ] No negative UX impact on critical flows (if yes, approval required)
- [ ] Experiment duration ≤ 4 weeks (if longer, approval required)
- [ ] Data privacy and consent requirements met

---

## Post-Launch Review Checklist

### Data Quality
- [ ] SRM check passed (χ² p-value > 0.05)
- [ ] No mid-flight parameter changes
- [ ] Sample size target reached before analysis

### Results Interpretation
- [ ] Analysis used pre-registered primary metric
- [ ] Confidence intervals reported alongside p-values
- [ ] Segment analysis does not drive primary decision
- [ ] Guardrail metrics reviewed

### Decision and Learning
- [ ] Ship / Iterate / Abandon decision documented
- [ ] Key learnings recorded for future experiments
- [ ] Feature flag cleanup scheduled
```

---

## Experiments with Learning (EwL) Metrics

Beyond primary/secondary metrics, EwL metrics capture *what we learned* — not just *what we measured*.

| EwL Metric | Definition | Why It Matters |
|------------|------------|----------------|
| **Hypothesis Quality Score** | % of experiments with falsifiable, pre-registered hypothesis | Prevents p-hacking and HARK-ing |
| **SRM Detection Rate** | % of experiments that ran an SRM check | Ensures data integrity |
| **Null Result Rate** | % of experiments with null result | Healthy rate (40-60%) signals good calibration |
| **Experiment Velocity** | Experiments shipped per month per team | Tracks learning throughput |
| **Time to Decision** | Days from launch to ship/iterate/abandon decision | Identifies bottlenecks in analysis |
| **Learning Reuse Rate** | % of experiments that reference prior learnings | Measures institutional memory |


---

## Per-Recipe Behavior Notes (SKILL.md excerpt)

- `ab`: Full A/B experiment design — PICOT hypothesis, power analysis, randomization unit, SRM monitoring plan.
- `cuped`: Apply CUPED/CUPAC variance reduction with a 7-day pre-exposure window. Combine with Winsorization for heavy-tailed metrics unless whales drive majority of revenue.
- `switchback`: Measurement design under interference (marketplaces, logistics, pricing). Declare rotation window against treatment response horizon, block randomization (day-of-week × hour-of-day), washout/burn-in, and carryover-aware variance (block bootstrap or Bojinov HAC). Follow DoorDash 30-min / Uber 1-h / Lyft hourly / Airbnb daily precedent. Route to `cluster` randomization when response horizon > 24 h. Do not confuse with Mend `canary` — that is rollout risk-control, not measurement under interference.
- `analyze`: Post-experiment statistical analysis — SRM check first, then effect sizes, CIs, and recommendations.
- `guardrail`: Per-experiment metric portfolio — declare the 4-layer taxonomy (primary/secondary/counter/guardrail), pre-register non-inferiority margins, estimate power-for-margin per guardrail, apply Benjamini-Hochberg across 5–10 guardrails, and produce the stop/ship trigger matrix before launch. Distinct from Pulse: Pulse defines product-wide KPIs; `guardrail` defines the measurement contract for this specific test and its gaming modes. Cite Kohavi/Tang/Xu (*Trustworthy Online Controlled Experiments*) and the Netflix/Microsoft ExP/Airbnb/Booking portfolio patterns.
- `ff`: Flag-driven assignment and ramp lifecycle. Separate the release flag (Launch owns) from the experiment flag (Experiment owns). Use the 1/5/25/50/100 % ramp with sequential-test α budget (mSPRT / confidence sequences) across stages; measure primary at ≥ 25 %, use 1 % / 5 % stages for crash/SRM/latency only. Pre-register kill-switch triggers and rehearse activation in staging. On conclusion, hand off to `Launch` via `EXPERIMENT_TO_LAUNCH` with flag key, final state, and decommission deadline. Platform landscape (2026-05): Statsig acq. by OpenAI (2025-09); Eppo acq. by Datadog (2025-05), rebranded Datadog Experiments GA (2026-04); GrowthBook 4.2 adds product analytics GA + Safe Rollouts (one-sided sequential testing on guardrails); Spotify Confidence SaaS GA (2025). (Sources: datadoghq.com/blog/datadog-acquires-eppo, blog.growthbook.io/release-4-2-product-analytics, confidence.spotify.com)
- `srm`: Load `reference/srm-detection.md`. Dedicated SRM diagnosis — chi-squared test, p < 0.001 threshold, segment-level decomposition (device / region / tenure / traffic source), bucket-mismatch and assignment-bug root causes. SRM invalidates the test; trust > ship.
- `sequential`: Load `reference/sequential-testing.md`. Anytime-valid sequential testing — mSPRT, confidence sequences, group sequential (Pocock / O'Brien-Fleming / Lan-DeMets α-spending). Controls Type I error under peeking; mSPRT preferred for continuous monitoring.
- `bayesian`: Load `reference/bayesian-ab.md`. Bayesian A/B — prior specification (Beta for proportions, Normal for means), posterior updating, credible intervals, probability-to-beat, ROPE (Region of Practical Equivalence), expected loss decision rule. Contrast with frequentist; Bayesian better for decision communication and continuous monitoring without p-hacking guilt.



---

## Output Routing Table (SKILL.md excerpt)

| Signal | Approach | Primary output | Read next |
|--------|----------|----------------|-----------|
| `hypothesis`, `what to test` | Hypothesis document creation | Hypothesis doc | `reference/experiment-templates.md` |
| `A/B test`, `experiment design` | Full experiment design | Experiment plan | `reference/sample-size-calculator.md` |
| `sample size`, `power analysis` | Sample size calculation | Power analysis report | `reference/sample-size-calculator.md` |
| `feature flag`, `rollout`, `toggle` | Feature flag implementation | Flag setup guide | `reference/feature-flag-patterns.md` |
| `results`, `significance`, `analyze` | Statistical analysis | Experiment report | `reference/statistical-methods.md` |
| `sequential`, `early stopping` | Sequential testing design | Alpha spending plan | `reference/statistical-methods.md` |
| `multivariate`, `factorial` | Multivariate test design | Factorial design doc | `reference/statistical-methods.md` |
| `bandit`, `MAB`, `adaptive` | Adaptive experimentation design | MAB/Thompson Sampling plan | `reference/adaptive-experimentation.md` |
| `interleaving`, `ranking test` | Interleaving test design | Interleaving test plan | `reference/interleaving-tests.md` |
| `CUPED`, `variance reduction`, `sensitivity`, `winsorization`, `outlier capping` | CUPED/CUPAC/Winsorization variance reduction design | Variance reduction plan | `reference/statistical-methods.md` |
| `SRM`, `sample ratio`, `broken split` | SRM diagnosis and root cause analysis | SRM diagnosis report | `reference/srm-detection.md` |
| `switchback`, `marketplace test`, `network effect` | Switchback experiment design | Switchback test plan | `reference/switchback-design.md` |
| `cluster`, `interference`, `marketplace randomization` | Cluster randomization design | Cluster experiment plan | `reference/common-pitfalls.md` |
| `canary`, `observability`, `experiment diagnostics` | Observability-native experiment diagnostics | Canary test plan with guardrail integration | `reference/feature-flag-patterns.md` |
