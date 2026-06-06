# Guardrail Metrics Reference

Purpose: Design a disciplined metric portfolio for an individual experiment — primary, secondary, counter, and guardrail — with trigger rules and Type II error handling. This is the measurement contract for a single test, not the product-wide KPI tree.

## Scope Boundary

- **Experiment `guardrail`**: metrics for EXPERIMENT analysis — what moves the decision, what blocks the ship, what signals collateral damage. Typically a subset of Pulse's metrics plus experiment-specific counter metrics.
- **Pulse (elsewhere)**: product KPI tree, North Star, funnel definitions, dashboard wiring. Persistent across experiments.

If the question is "what is our retention metric?" → `Pulse`. If it is "which metrics must not regress while we ship this change, and what is the stop rule?" → `guardrail`.

## 4-Layer Metric Taxonomy

Kohavi / Tang / Xu (*Trustworthy Online Controlled Experiments*, 2020) codify four roles. Every experiment must declare at least one of layers 1 and 4; layers 2 and 3 are conditional.

| Layer | Role | Example | Decision weight |
|-------|------|---------|-----------------|
| 1. Primary (OEC) | Decides ship / no-ship | Revenue per user, 7-day retention | Highest — powered for MDE |
| 2. Secondary | Explains why primary moved | Sessions/user, CTR on treated surface | Supporting — not powered |
| 3. Counter | Detects gaming of primary | If primary = clicks, counter = bounce rate; if primary = revenue, counter = refund rate | Blocks ship if primary win comes at counter's expense |
| 4. Guardrail | Protects the business | Page load p95, crash-free rate, complaint rate, unsubscribe rate | Regression blocks ship even if primary wins |

Guardrails are **non-inferiority tests** — the question is "is the treatment no worse than control by more than a pre-declared margin?" — not the two-sided superiority test used for the primary.

## Trigger Rules

Pre-register the stop/ship matrix before launch. Do not negotiate it at analysis time.

| Primary | Guardrail | Counter | Action |
|---------|-----------|---------|--------|
| Significant win | All clean | Clean | SHIP |
| Significant win | Any breach | — | HALT — investigate root cause |
| Significant win | Clean | Breach | NO-SHIP — win is gamed |
| Null | Clean | Clean | NO-SHIP by default (Kohavi: ~30% of experiments at mature orgs win; ~12% of design changes produce positive outcomes) |
| Significant loss | — | — | HALT immediately |
| SRM detected | — | — | HALT — result is not trustworthy |

## Type II Error on Guardrails

Guardrails are typically **underpowered** for the real effect size, because the experiment is sized for the primary MDE, not the guardrail MDE.

- Declare a **non-inferiority margin** per guardrail (e.g., "p95 latency must not regress by more than 50 ms", "refund rate must not rise by more than 10 % relative").
- Use a one-sided non-inferiority test at α = 0.05 against that margin — do not use "p > 0.05, therefore no harm." A null result on an underpowered guardrail is not evidence of safety.
- If the confidence interval crosses the non-inferiority margin, treat the guardrail as **inconclusive** and either extend the experiment, run a follow-up powered for the guardrail, or ship-with-monitoring (requires explicit sign-off).
- Record guardrail power at design time. If guardrail power < 50 % for the declared margin, flag the design as high-risk.

## Revenue Guardrails

Common at Microsoft ExP, Airbnb, Booking.

- **Revenue per user** (not per session — per-session denominator bias, same as primary metric discipline).
- **Refund / chargeback rate** — lagging (30–90 day) — run a **post-experiment holdout** if refund window exceeds experiment duration.
- **Subscription cancellation rate** — for SaaS, this is the true counter to activation wins.
- **Heavy-tail handling**: revenue is right-skewed; use CUPED + Winsorization (99th percentile cap) — except when whale users (<2 %) drive the majority of revenue, in which case Winsorization underplays the real treatment effect.

## UX Guardrails

Common at Microsoft ExP, Google, Netflix.

- **Page load p95 / p99** — not mean (mean hides tail degradation that kills bounce rate).
- **Crash-free sessions** (mobile) — breach threshold typically 0.1 % absolute regression.
- **Time to interactive** — especially for treatment that adds JS weight.
- **Error rate** — 4xx / 5xx, client-side errors, failed requests.
- **Complaint / support ticket rate** — lagging, worth a post-experiment window.
- **Accessibility regression** — contrast / keyboard-nav / screen-reader, often missed.

## Portfolio Patterns by Company

- **Netflix**: OEC = streaming hours; guardrails = playback errors, app crashes, startup latency. Counter = engagement with non-recommended content (detects recommendation gaming).
- **Microsoft ExP (Kohavi / Tang / Xu)**: OEC = sessions per user + session quality; guardrails = page load, 4xx/5xx, crash-free. Counter = clicks-per-session vs conversion-per-session (detects click-bait regressions). Per Fabijan et al. (Microsoft, KDD 2019), **~6% of all Microsoft online controlled experiments exhibit SRM** — bake SRM into the guardrail portfolio as a non-negotiable infrastructure-level guardrail, not a per-experiment opt-in check.
- **Airbnb**: OEC = bookings; guardrails = search-to-contact rate, host response rate, cancellation rate. Counter = refund rate (lagging, post-experiment).
- **Booking.com (Kohavi era)**: ~10 guardrails per experiment by default; every team owns one — guardrails are org-wide infrastructure, not per-experiment decisions.
- **Spotify Confidence**: OEC estimator uses Negi & Wooldridge (2021) full regression adjustment as the production default (Confidence docs, "Variance Reduction (CUPED)"); guardrails include latency, crash rate, and content-loading success. Spotify Engineering's *"Risk-Aware Product Decisions in A/B Tests with Multiple Metrics"* (Mar 2024) formalizes how expected-loss across the metric portfolio drives ship/no-ship — i.e., guardrails feed into a single decision under Bayesian utility, not independent significance tests.
- **GrowthBook 3.6 (2025-05-01)**: codifies guardrails via **Safe Rollouts** — one-sided sequential testing on guardrail metrics continuously monitors for harmful changes during ramp without inflating false-positive rate. Effectively turns the guardrail layer into a sequential kill-switch.

## Anti-Patterns

- Picking primary + secondary only, skipping counter — the classic "CTR up, revenue down" trap (Etsy infinite scroll; Kohavi Rule of Thumb #5).
- Treating a guardrail null result as "no harm" when the test is underpowered.
- Choosing guardrails after seeing results — HARKing on the defensive side.
- Letting the team negotiate the non-inferiority margin after the experiment — pre-register or it doesn't count.
- Using the same α for primary and guardrail without accounting for the multiple-comparison inflation across 5–10 guardrails — apply Benjamini-Hochberg or widen the per-guardrail CI.
- Guardrails on metrics the experiment cannot move in its duration (e.g., 90-day retention on a 14-day test) — flag as **informational only**, do not use as ship blockers.
- Reusing the product-wide KPI list as the guardrail list without filtering — product KPIs are defined by Pulse for the business; guardrails are defined per experiment to protect against specific gaming modes and collateral damage of the specific treatment.

## Counter-Metric Patterns by Treatment Type

Counter metrics are treatment-specific. The counter must be the mechanism by which the primary could be gamed.

| Treatment | Primary | Counter | Why |
|-----------|---------|---------|-----|
| Ranking / recommendation change | CTR, engagement | Downstream conversion, dwell time, refund rate | High CTR + low conversion = clickbait |
| Paywall / pricing change | Revenue | Cancellation rate, refund rate, LTV proxy | Short-term revenue at long-term retention cost |
| Notification / re-engagement | DAU, session count | Unsubscribe rate, complaint rate, uninstall rate | Spam disguised as engagement |
| Onboarding change | Activation rate | 7-day / 30-day retention | Funnel-pushing users who churn |
| Search / discovery change | Search CTR | Search abandonment, zero-result follow-up | Gaming CTR on the first result |
| Infinite-scroll / feed change | Page views, session length | Conversion, search engagement, satisfaction | Etsy's 2014 infinite scroll case |

## Output Checklist

- Primary (OEC): metric, MDE, denominator, power.
- Secondary: 1–3 explanatory metrics, no power requirement.
- Counter: at least one, mapped to the specific way primary could be gamed.
- Guardrails: 3–10 metrics, each with non-inferiority margin, power-for-margin estimate, and ship-blocking flag.
- Stop/ship matrix: pre-registered.
- Multiple-comparison correction across guardrails: declared.
