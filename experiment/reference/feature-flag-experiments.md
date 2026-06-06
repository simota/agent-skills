# Feature-Flag-Driven Experiments Reference

Purpose: Wire an experiment's assignment, exposure, and ramp through a feature-flag platform (LaunchDarkly, Flagsmith, Unleash, Statsig), and plan the flag's full lifecycle from 1 % ramp to decommission. This is an experiment-assignment reference — the flag is the measurement substrate.

## Scope Boundary

- **Experiment `ff`**: flag mechanics FOR MEASUREMENT — assignment consistency, exposure logging, ramp schedule, kill switch, decommission after the experiment concludes. Intent = learn.
- **Launch (elsewhere)**: flag mechanics FOR RELEASE — release planning, CHANGELOG, versioning, rollback plans. Intent = ship.

Overlap: both use the same flag platforms and often the same flag. Divide on intent. Cross-link: `Experiment → Launch` handoff (`EXPERIMENT_TO_LAUNCH`) hands over a flag that has finished its measurement role and now enters release tracking. See `reference/feature-flag-patterns.md` for platform comparison details; this file focuses on the experiment-specific design.

## Platform Selection

| Platform | Pick when | Skip when |
|----------|-----------|-----------|
| LaunchDarkly | Enterprise, mature targeting rules, SOC2 required; dual Frequentist/Bayesian engine, CUPED, sequential testing, MAB support GA | Cost-sensitive, need warehouse-native |
| Flagsmith | Self-hosting required, open-source core, cost-sensitive | Need built-in experimentation stats |
| Unleash | Self-hosted + open-source + GitOps-friendly; v7 GA 2025 with refreshed gradual-rollout / instant-rollback / experimentation tooling and deprecated-endpoint cleanup | Need tight experimentation analytics integration |
| Statsig | Now part of OpenAI (acquired 2025-09-02, $1.1B all-stock; CEO Vijaye Raji became OpenAI CTO of Applications). Continues to operate independently under Fidji Simo's Applications org. Dual-mode (cloud + warehouse-native), built-in experimentation stats, CUPED, corrected-alpha (CAA) always-valid p-values | Wary of OpenAI-affiliated dependency for sensitive PII data flows |
| GrowthBook | Warehouse-native first, open-source, SQL-defined metrics; v3.6 (2025-05-01) adds **Safe Rollouts** with one-sided sequential testing on guardrails + per-metric time-series view | Need hosted all-in-one with low setup effort |
| Eppo by Datadog | Warehouse-native, CUPED++ (uses assignment-time covariates so it works on new-user / onboarding tests with no pre-period data), GAVI sequential (Howard et al. 2021), observability guardrails. Acquired by Datadog 2025-05-05 (~$220M); rebranded "Eppo by Datadog" | Early-stage product, low scale |
| Datadog Experiments | Eppo-powered analytics fused with Datadog RUM/APM/logs for first-class observability guardrails | Standalone experimentation without need for Datadog stack |
| PostHog Experiments | OSS + cloud product analytics with new experimentation engine — running-time calculator, percentile-based Winsorization at metric level, choice of Bayesian (default) or Frequentist engine, 50-exposure minimum gate per variant | Need enterprise SOC2 + targeting rules at LaunchDarkly's depth |

Default for new experimentation program: **GrowthBook** (OSS, warehouse-native) or **Eppo by Datadog** (managed, warehouse-native, CUPED++) — experimentation-native, not flag-first-experiment-second. Use **Statsig** when you already operate inside the OpenAI applications stack; use **LaunchDarkly** when feature-flag governance and enterprise targeting dominate the requirement set.

## Flag ≠ Experiment

A common anti-pattern: using one flag for both the release toggle and the experiment assignment. Separate them:

- **Release flag**: controls whether the code path is reachable. Owned by Launch. Decommissioned on release stabilization (typically 2–4 weeks post-GA).
- **Experiment flag**: controls the variant assignment for a measurement window. Owned by Experiment. Decommissioned at analysis sign-off.

A single flag hides two lifecycles. Teams that conflate them end up with 6-month-old "experiment" flags that are really feature toggles, and 6-month-old "release" flags that are really forgotten A/B tests — both leak assignment and bias future experiments.

## Ramp Schedule

Standard staged ramp: **1 % → 5 % → 25 % → 50 % → 100 %**.

| Stage | Duration | Checks | Stop condition |
|-------|----------|--------|----------------|
| 1 % | 24–48 h | Exposure logging, crash rate, SRM check | Crash / SRM / p95 latency breach |
| 5 % | 2–3 days | Guardrails, telemetry, error rates | Guardrail breach |
| 25 % | Until MDE reached or stop-rule fires | Primary metric, guardrails, variance | Stat-sig loss on primary, guardrail breach |
| 50 % | Main measurement phase | Full OEC + guardrails | Decision gate — go/no-go |
| 100 % | Release phase (Launch owns) | Post-launch monitoring | — |

**Ramp ≠ peeking**. Ramping traffic is not early stopping — but every stage boundary where you *could* halt is effectively an interim analysis. Use **sequential testing (mSPRT / confidence sequences)** during ramp, not classical fixed-horizon α. Budget α across ramp stages.

**Ramp vs statistical power**: at 1 % and 5 %, the sample is too small to measure the primary. Use those stages for operational guardrails only (crashes, latency, SRM). Start measuring the primary at 25 % or later.

## Kill Switch

Every experiment flag must have a **kill switch** with an SLA-bounded activation path:

- **Activation latency**: flag-platform update → SDK propagation ≤ 60 s for LaunchDarkly/Statsig streaming; ≤ 5 min for polling SDKs. Confirm this at design time.
- **Kill-switch triggers** (pre-registered):
  - SRM detected (χ² p < 0.001).
  - Primary metric regression > pre-declared loss threshold.
  - Guardrail breach with CI outside non-inferiority margin.
  - Error rate > 2× baseline.
  - Crash rate > 0.1 % absolute regression (mobile).
- **Manual override**: on-call can force-disable via flag platform without deploy.
- **Rehearsal**: kill-switch activation must be tested in staging before launch — untested kill switches have a ~30 % fail rate at real incidents (anecdotal from post-incident reviews; LaunchDarkly best-practice guidance).

## Assignment Consistency

- **Sticky bucketing**: hash `user_id` + `experiment_key` → variant. Never hash on session or request ID — produces re-randomization within a user, inflates variance, and breaks per-user metrics.
- **Anonymous users**: hash on a first-party cookie persisted ≥ experiment duration. Safari/Firefox block 3rd-party cookies — never use 3P-cookie-based assignment.
- **Server-side assignment** preferred over client-side — client-side assignment leaks variant (users can flip by editing cookies) and is blocked by ad blockers / ITP.
- **Salt per experiment**: same user should get independent variants across concurrent non-interacting experiments. Salt = experiment_key.
- **Exposure logging**: log assignment at the point of *exposure* (when the treated surface is rendered), not at the point of assignment — prevents overcounting users who never saw the treatment.

## Decommission Plan

Flags that outlive their experiment become technical debt and bias future experiments through residual traffic targeting. Pre-register decommission:

| Outcome | Action | Deadline |
|---------|--------|----------|
| Ship | Flag → 100 %, then archive. Code path becomes default. Remove flag check within 2 sprints. | 4 weeks post-decision |
| Discard | Flag → 0 %, archive, remove code path. | 2 weeks post-decision |
| Iterate | Roll into next experiment with new flag key. Old flag decommissioned. | 2 weeks post-decision |
| Inconclusive | Extend with pre-registered plan, or decommission and mark as learning. | 2 weeks post-decision |

Handoff to `Launch` via `EXPERIMENT_TO_LAUNCH` carries: flag key, final state, code-removal ticket, rollback expiration date.

## Anti-Patterns

- Reusing the same flag across multiple experiments — residual assignment from experiment 1 biases experiment 2.
- Skipping the 1 % / 5 % stages "because we have logging" — these stages exist for unknown-unknowns (crash bugs, SRM from targeting rules) not for statistical power.
- Client-side-only assignment with a 3P cookie — 50 % of web traffic silently drops out.
- No kill-switch rehearsal — first real activation during an incident fails due to stale SDK cache.
- Long-lived "experiment" flags (> 90 days) that became feature toggles — migrate to a release flag owned by Launch, or remove.
- Measuring the primary at 1 % traffic — underpowered; you will either stop early on noise (if peeking) or extend for months.
- Conflating ramp stage and statistical-decision stage — ramp is operational; statistical decision requires full power.

## Output Checklist

- Platform (LaunchDarkly / Flagsmith / Unleash / Statsig / GrowthBook / Eppo).
- Flag key, salt, and ownership (Experiment vs Launch).
- Assignment unit (user_id / cookie) and hashing strategy.
- Exposure logging point.
- Ramp schedule with per-stage checks and SLAs.
- Kill-switch triggers (pre-registered) and rehearsal evidence.
- Sequential-test α budget across ramp stages.
- Decommission plan with deadlines and Launch handoff.
