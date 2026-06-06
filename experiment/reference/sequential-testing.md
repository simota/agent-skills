# Sequential Testing Reference

Purpose: Enable anytime-valid monitoring of A/B tests — peek as often as needed without inflating Type-I error. Covers mSPRT (mixture Sequential Probability Ratio Test), confidence sequences, and classical group-sequential α-spending.

## Scope Boundary

- **experiment `sequential`**: Anytime-valid / group-sequential testing (this document).
- **experiment `ab` (elsewhere)**: Fixed-sample design.
- **experiment `bayesian` (elsewhere)**: Bayesian anytime-valid inference.
- **experiment `analyze` (elsewhere)**: Post-hoc analysis.
- **experiment `srm` (elsewhere)**: Always precede sequential inference with SRM check.

## Why Classical Peeking Inflates Type-I Error

Fixed-sample frequentist tests assume one evaluation at pre-specified sample size. Each early look inflates α. After 5 looks, actual Type-I error can reach 14% (not 5%).

### Three valid families

| Family | Mechanic | Use when |
|--------|----------|----------|
| **Group sequential (α-spending)** | Pre-specified look schedule with shrinking α per look | Fixed number of planned interim analyses |
| **mSPRT (anytime-valid)** | Sequential probability ratio with mixing prior | Unplanned, continuous monitoring |
| **Confidence sequences** | CI valid simultaneously at all times | Real-time dashboards |

## Group Sequential (α-Spending)

### Pocock

Uniform α per look. Aggressive early stopping; more conservative overall.

### O'Brien-Fleming

Very small α early, grows toward the end. Preserves power at final look; most common in biostatistics and enterprise A/B platforms.

### Lan-DeMets (α-spending function)

Flexible — doesn't require pre-specified look count. Define a spending function f(t) and monitor against boundary.

### Look schedule example (O'Brien-Fleming, 5 looks, α = 0.05)

| Look | Information fraction | Boundary (z-score) | Nominal α |
|------|---------------------|--------------------|-----------|
| 1 | 0.2 | 4.56 | 5.1e-06 |
| 2 | 0.4 | 3.23 | 1.3e-03 |
| 3 | 0.6 | 2.63 | 8.5e-03 |
| 4 | 0.8 | 2.28 | 0.023 |
| 5 | 1.0 | 2.04 | 0.041 |

## mSPRT (Anytime-Valid)

Howard, Ramdas et al. — "Time-uniform, nonparametric, nonasymptotic confidence sequences" (2021). Used by Optimizely, Amazon A/B.

### Core idea

Mix the SPRT over a prior on the effect size. The resulting test statistic is a martingale; Ville's inequality gives:

> P(ever rejecting H0 | H0 true) ≤ α

**You can peek continuously forever, and Type-I error stays bounded.**

### Practical form (proportion metric)

```
Λ_n = ∫ exp(θ · S_n - (n · θ²)/2) dπ(θ)

Reject H0 when Λ_n ≥ 1/α
```

Where `S_n` is the accumulated score statistic and π is the mixing prior. Most platforms use a gaussian mixing prior with variance τ² set to plausible effect range.

### When to prefer mSPRT over group-sequential

- Don't want to pre-commit to look schedule.
- Want dashboard-friendly continuous monitoring.
- Comfortable losing some power vs group-sequential for the convenience.

## Confidence Sequences

An interval (L_n, U_n) such that:

> P(∀n: θ ∈ (L_n, U_n)) ≥ 1 - α

Corresponds 1:1 with anytime-valid tests. Practical implementations:

- Howard-Ramdas confidence sequences (2021).
- Empirical Bernstein bounds (Waudby-Smith & Ramdas 2023).

### Dashboard pattern

Plot point estimate + confidence sequence that tightens over time. If the sequence excludes 0, the test is significant — at any time.

## Practical Matrix

| Need | Choice |
|------|--------|
| One planned interim + final | O'Brien-Fleming 2-look |
| 3-5 planned interims | O'Brien-Fleming (stat-heavy) or Pocock (aggressive) |
| Unplanned continuous peeking | mSPRT or confidence sequence |
| Experimentation platform default | mSPRT (Optimizely / Uber / Netflix / Amplitude lineage), GAVI (Eppo by Datadog — Howard et al. 2021), CAA / corrected-alpha (Statsig, now OpenAI), one-sided sequential safe-rollouts (GrowthBook 3.6) |
| Classical academic rigor | Lan-DeMets α-spending |

### Platform → method mapping (2026-05)

| Platform | Sequential method |
|----------|-------------------|
| Optimizely | mSPRT (Johari, Pekelis, Walsh 2015 / KDD 2017) |
| Eppo by Datadog | GAVI — generalization of always-valid inference per Howard, Ramdas, McAuliffe, Sekhon (AOS 2021) |
| Statsig (OpenAI) | Corrected-alpha approach (CAA) + always-valid p-values |
| LaunchDarkly | Sequential testing GA in 2025 across both Frequentist and Bayesian engines |
| GrowthBook 3.6+ | One-sided sequential testing on guardrail metrics within "Safe Rollouts" (released 2025-05-01) |
| Spotify Confidence | mSPRT (per Spotify Engineering, "Choosing a Sequential Testing Framework," 2023) |
| Uber / Netflix / Amplitude | mSPRT lineage

## Power Considerations

Sequential testing trades power for flexibility.

- Fixed-sample: baseline 80% power at n.
- 5-look O'Brien-Fleming: ~78% power at same n (2% loss).
- mSPRT continuous: ~70% power at same n (10% loss).

If power matters more than peeking flexibility, use fixed-sample.

If decision speed matters (early wins shipped sooner, early losses stopped early), sequential gives faster expected stop time.

## Integration with CUPED

CUPED variance reduction is orthogonal and compatible. Apply CUPED to shrink the variance, then use sequential testing on the adjusted statistic. Eppo / Statsig / Datadog Experiments do this by default.

## Workflow

```
DECIDE   →  which family fits (planned vs continuous, power-sensitivity)

CALIBRATE→  α, power, MDE, estimated variance
          →  if group-sequential: pick boundary (O'Brien-Fleming default)
          →  if mSPRT: pick mixing prior variance τ²

INSTRUMENT→  daily statistic computation
           →  guardrail: SRM check before every inference
           →  log: look number, statistic, boundary, decision

MONITOR  →  dashboard with anytime-valid CI
          →  alert on boundary crossing
          →  alert on SRM

DECIDE   →  stop early on boundary crossing OR reach final look
          →  if stopped early: report effect + CI + look at which stopped
          →  if reached final without crossing: report as negative or neutral

HANDOFF  →  Launch: if ship decision
          →  Magi: if ambiguous
          →  Experiment Lead: post-mortem regardless
```

## Output Template

```markdown
## Sequential Testing Design: [Experiment]

### Choice
- **Family**: [Group sequential (OBF / Pocock / Lan-DeMets) / mSPRT / Confidence Sequence]
- **Rationale**: [...]

### Parameters
- **α**: [e.g., 0.05]
- **Power target**: [e.g., 0.80]
- **MDE**: [e.g., 2% lift]
- **Variance estimate**: [from Pulse or pilot]
- **For group-sequential**: look schedule + boundary table
- **For mSPRT**: mixing prior variance τ²

### Look Schedule (if applicable)
| Look | Info fraction | Boundary | Nominal α |
|------|---------------|----------|-----------|
| 1 | ... | ... | ... |

### Stopping Rules
- **Early stop for efficacy**: [boundary condition]
- **Early stop for futility**: [optional, e.g., conditional power < 20%]
- **Final analysis**: [at N users or T days]

### SRM + Guardrails
- [ ] SRM check at every look
- [ ] Guardrail portfolio from `guardrail` recipe

### Power Impact
- **Fixed-sample baseline power**: [e.g., 80%]
- **Sequential power**: [e.g., 78%]
- **Expected stop time** (if effect exists): [earlier than fixed-sample]

### Platform
- **Engine**: [Optimizely / Statsig / Eppo / Datadog Experiments / GrowthBook / custom]
- **Configuration**: [...]

### Handoffs
- Pulse: metric variance estimate
- Launch: ship decision
- Magi: ambiguity arbitration
- Builder: platform wiring if custom
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Peeking without sequential correction | Use mSPRT or α-spending; p-values from fixed-sample test are invalid after peek |
| Stopping when "looks significant" then claiming 95% CI | Use sequential CI, not fixed-sample |
| Picking boundary after seeing data | Pre-specify; pre-register boundary |
| Ignoring power loss with sequential | Acknowledge; use if flexibility > power |
| SRM not checked per look | SRM must pass before every sequential inference |
| Using Pocock when effect likely small | OBF preserves power better |
| mSPRT with unrealistic mixing prior | Set τ² to plausible effect range |
| Confusing sequential with Bayesian | They can coexist but are distinct families |
| Running sequential indefinitely | Still have a hard stop — cost, business window, novelty effect |

## Deliverable Contract

When `sequential` completes, emit:

- **Family choice** with rationale.
- **Parameters** (α, power, MDE, variance, boundary or prior).
- **Look schedule** if group-sequential.
- **Stopping rules** (efficacy + optional futility).
- **Power impact analysis** vs fixed-sample.
- **SRM + guardrail integration plan**.
- **Platform configuration**.
- **Handoffs**: Pulse, Launch, Magi, Builder.

## References

- Howard, Ramdas, McAuliffe, Sekhon — *Time-uniform, nonparametric, nonasymptotic confidence sequences* (AOS 2021)
- Waudby-Smith & Ramdas — *Estimating means of bounded random variables by betting* (JRSS B 2024)
- Ramdas, Grünwald, Vovk, Shafer — *Game-Theoretic Statistics and Safe Anytime-Valid Inference* (Statistical Science 2023) — SAVI / e-process foundations
- Lan & DeMets — *Discrete sequential boundaries for clinical trials* (Biometrika 1983)
- Pocock — *Group sequential methods in the design and analysis of clinical trials* (1977)
- O'Brien & Fleming — *A multiple testing procedure for clinical trials* (1979)
- Johari, Koomen, Pekelis, Walsh — *Peeking at A/B Tests: Why it matters, and what to do about it* (KDD 2017, Optimizely) / *Always Valid Inference: Bringing Sequential Analysis to A/B Testing* (arXiv:1512.04922)
- Spotify Engineering — *Choosing a Sequential Testing Framework — Comparisons and Discussions* (2023)
- GrowthBook — *Safe Rollouts: one-sided sequential guardrail monitoring* (v3.6 release notes, 2025-05-01)
- LaunchDarkly — *Introducing sequential testing for LaunchDarkly Experimentation* (2024/2025 blog) + Bayesian methodology docs
- Eppo by Datadog — GAVI sequential inference docs (post 2025-05 Datadog acquisition)
- Statsig docs — corrected-alpha (CAA) always-valid p-values (now under OpenAI Applications post 2025-09)
- Microsoft ExP — *Democratizing online controlled experiments at Booking.com, Microsoft, Spotify* — sequential inference in practice
- Ramesh Johari lectures — sequential inference for industry (YouTube)
