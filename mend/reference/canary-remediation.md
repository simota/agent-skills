# Canary Release Control Reference

Purpose: Operate an in-flight progressive rollout — hold, promote, or rollback a canary — based on real-time health signals. Mend `canary` is the operational gate controller for a release already in motion. It does not design the rollout plan and does not ship code.

## Scope Boundary

- **Mend `canary`**: gate decisions during an active rollout — promote 1% → 5% → 25% → 100%, hold at current stage, auto-rollback on trigger, partial-rollback (drain canary, keep prior stages), feature-flag coordination for cohort scope.
- **Triage**: decides *whether* the canary is actually unhealthy vs noisy metric vs unrelated incident. Triage gates the rollback decision; Mend executes.
- **Builder**: owns the code fix that the rollback surfaces. A rolled-back canary returns to Builder with the failing signal as evidence.
- **Launch**: owns the rollout *plan* (stages, windows, cohorts, flag strategy) ahead of the release. Mend executes against that plan during the incident / release window.
- **Beacon**: defines the promotion-gate SLIs and thresholds. Beacon's dashboards are what Mend reads.

Rule of thumb: Mend never promotes a canary that does not have pre-defined promotion-gate thresholds. If the gates aren't defined, return to Launch / Beacon.

## Rollout Stages & Defaults

| Stage | Traffic | Minimum soak | Typical gate |
|-------|---------|--------------|--------------|
| Shadow / dark | 0% served, mirrored | 10-30 min | Error rate delta vs baseline, p95 delta |
| 1% | 1% | 15-30 min | Error rate < baseline + 0.1%, p95 < baseline * 1.1 |
| 5% | 5% | 30-60 min | Error rate, p95, business KPI (conversion, sign-in) |
| 25% | 25% | 1-4 h | Full SLI panel, cohort coverage, feature-flag exposure valid |
| 100% | 100% | — | Soak 24-72h before next release overlaps |

Soak times lengthen for user-visible / revenue paths; shorten for internal / backend-only.

## Promotion-Gate SLIs

- **Error rate**: canary vs baseline, statistically significant delta only. Raw 0.01% delta at 1% traffic is noise.
- **Latency p95 / p99**: canary tail vs baseline; beware warmup skew in first 5 min.
- **Saturation**: CPU / memory / GC / pool utilization on canary pods; higher than baseline = capacity regression.
- **Business KPI** (where applicable): conversion rate, sign-in success, cart completion. Flaking on a business KPI is a rollback trigger even if technical SLIs are green.
- **Dependency health**: downstream dep error rate attributable to canary — often the cascade origin.
- **Error budget burn**: fast-burn (>= 2% / 1h, 14.4x) on the canary cohort → auto-rollback.

## Workflow

```
PRE-CHECK      →  read current canary state: stage, traffic %, soak elapsed, cohort
               →  load Beacon promotion gates for this service
               →  read Triage assessment if incident-driven (hold/rollback request)
               →  confirm feature-flag targeting matches current stage
               →  classify tier:  T1 status read
                                  T2 hold (no user change)
                                  T3 promote or rollback (user-visible state change)

ACTION         →  status (T1):   render current stage + gate status + soak remaining
               →  hold (T2):     freeze current stage, extend soak window, notify owners
               →  promote (T3):  advance traffic % (1→5→25→100); update flag targeting;
                                  require all gates green + soak satisfied + approval
               →  rollback (T3): drain canary stage, shift traffic back to prior
                                  stage; flip flag off for canary cohort
               →  partial rb (T3): keep 5% / 25% stages, drop only the failed 100% push
               →  each step is idempotent — re-running converges on target state

STAGED VERIFY  →  Health Check:  canary pods Ready; no CrashLoop; flag eval returns
                                  expected cohort distribution
               →  Smoke Test:   synthetic probe hits canary path; prior stage unaffected;
                                feature-flag cohort sanity (opt-in users see new code)
               →  SLO Check:    canary-cohort SLI vs baseline; global SLI unchanged;
                                fast-burn alert absent for 10 min
               →  Recovery Confirmed: gates green for full soak; no lag in dependencies

ROLLBACK       →  auto-trigger if:  fast-burn (>= 14.4x) on canary cohort,
                                     crash-loop on canary pods,
                                     p95 latency 2x baseline sustained 5 min,
                                     business KPI drop > threshold,
                                     security alert on canary path
               →  action:   flip flag off for canary cohort → drain canary replicas
                              → restore prior-stage traffic → verify
               →  verify:   Health → Smoke on prior stage; log rollback to timeline
               →  report:   hand failing signal + canary artifact to Builder
```

## Cohort Selection

- **Random %**: default for backend / API changes; statistically clean.
- **Employee / internal first**: for UX-heavy changes; bias-accepted in exchange for fast feedback.
- **Opt-in beta cohort**: for large UX changes; users expect canary. Smaller signal magnitude.
- **Geographic / single-AZ**: for infra-coupled changes; blast-radius contained.
- **Tenant-scoped** (B2B / SaaS): one friendly tenant first, then tier-up. Coordinate with account team before promotion.

Never canary with a cohort that cannot be reverted (anonymous users with no flag key). Without a reversible cohort, rollback is not atomic.

## Feature-Flag Coordination

- Canary = infrastructure-level traffic shift (what code runs). Feature flag = user-level exposure (who sees the feature). They are *different layers*; both must be coordinated.
- Flag-off + canary-deployed is safe — new code runs but is dark.
- Flag-on + no-canary is unsafe — the feature is exposed via existing code paths that may not support it.
- When rolling back, flip the flag first (instant), then drain the canary (slower). The flag is the fast safety switch.

## Partial Rollback Tactics

- **Drain canary stage only**: keep 25% stage, roll back the 25 → 100% push. Used when 100% introduced a new cohort-specific failure.
- **Cohort carve-out**: keep most cohorts on new version, flip the failing cohort's flag off. Used when failure is tenant / region specific.
- **Feature-only rollback**: keep the code, flip the feature flag off. Used when code is safe but feature logic is buggy. Cheapest rollback.
- **Full rollback**: revert all stages → 0%. Used when the failure is not cohort-bound.

## Anti-Patterns

- Promoting without satisfying soak time because "the gates are green right now". Short-soak regressions appear at minute 12, not minute 3.
- Using a single-metric gate (only error rate). Multi-SLI gating is table stakes.
- Rolling back by redeploying the old build rather than shifting traffic. Traffic-shift rollback is seconds; redeploy is minutes.
- Running two canaries on the same service simultaneously. Signals alias; you cannot attribute the failure.
- Treating feature-flag flip as a substitute for canary traffic control, or vice-versa. They complement, not replace.
- Auto-promoting on a T3 action. Promotion is always approval-gated; automation presents the decision, a human confirms.

## Tooling Landscape (2026-05)

| Tool | Pairs with | What Mend reads / writes |
|------|------------|---------------------------|
| **Argo Rollouts** | ArgoCD GitOps | Reads `AnalysisRun` results to know whether a gate failed; writes promotion or abort via the Rollout CRD; relies on `AnalysisTemplate` for the per-stage metric checks |
| **Flagger** | FluxCD GitOps + service mesh (Istio / Linkerd / App Mesh / NGINX) | Reads canary state + metric provider results; writes hold / promote / rollback via the `Canary` CR; relies on `MetricTemplate` for promotion gates |
| **Cloud-native progressive deploy** (GKE Cloud Deploy, AWS App Runner deployment policies, Azure Container Apps revisions) | Cloud-native CI/CD | Reads the platform's analysis output; writes promote / rollback through the platform API |

Real-world calibration: Intuit's published Argo Rollouts setup uses an `AnalysisTemplate` that compares the canary against ~`47` metrics and requires three consecutive successful analysis windows before automatic promotion. Treat that as the upper bound for "robust gate"; the lower bound is the multi-SLI gate already specified above. Tooling cannot fix a single-metric gate.

### Self-Healing Pipeline Alignment

The 2026 self-healing-pipeline pattern (Datadog Bits AI SRE, Azure SRE Agent, Wiz Green Agent, GitHub Copilot SRE flows) externalises this loop:

1. Incident or canary metric breaches a gate.
2. An investigation agent autonomously gathers traces, logs, code-change context, and dependency health.
3. The agent proposes a remediation — most often a **traffic-shift rollback** plus a candidate PR for the code fix.
4. A human approves the rollback (or auto-approves under the T2 envelope above) and reviews the PR before merging.

Mend `canary` is the executor of step 3 inside this loop: it does not invent the rollback strategy, but it must accept investigation handoffs that include cohort, gate that failed, and proposed action. Reject handoffs that omit any of the three.

## Handoff

- **Triage ← Mend `canary`**: if the rollback signal is ambiguous (metric noise vs real regression), Triage adjudicates before Mend rolls back.
- **Builder ← Mend `canary`**: every rollback hands Builder the failing cohort's evidence (traces, logs, metric deltas) for the code fix.
- **Launch ← Mend `canary`**: Launch owns the next retry of the rollout — updated plan, adjusted gates, revised cohort. Mend executes.
- **Beacon ← Mend `canary`**: post-incident, Beacon reviews whether the promotion gates caught the regression in time or whether thresholds need tightening.
