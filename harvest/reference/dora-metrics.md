# DORA 5-Key Metrics Deep-Dive Reference

Purpose: Structured deep-dive on the five DORA key metrics per the 2025 Accelerate State of DevOps Report (published 2025-10) — three **throughput** (Deployment Frequency, Lead Time for Changes, Failed Deployment Recovery Time) and two **instability** (Change Failure Rate, Rework Rate) — plus the **Reliability** quasi-metric, SPACE complement, and 7-archetype team mapping. Produces archetype-mapped delivery diagnostics with measurement-window and data-source caveats explicit. Per-metric percentile thresholds (Top 15% / Top 15-30% / etc.) replace the deprecated Elite/High/Medium/Low buckets; team-level classification uses the 7 archetypes (DORA 2025, cd.foundation 2025-10-16).

## Scope Boundary

- **harvest `dora`**: focused 5-key metric report with per-metric thresholds, 7-archetype team mapping, trend, and SPACE complement. Anchored to gh PR/release data plus deploy/incident sources.
- **harvest `weekly` / `monthly` (elsewhere)**: PR aggregation reports. Surface DORA throughput as one section but do not deep-dive tiers.
- **harvest `release` (elsewhere)**: changelog and release-note generation, not delivery-performance diagnostics.
- **harvest `retro` (elsewhere)**: narrative voice over a sprint window, not metric tier classification.
- **Pulse (elsewhere)**: dashboard implementation and KPI tracking. Harvest produces the metric report; Pulse owns the live dashboard.
- **Beacon (elsewhere)**: SLO/SLI and reliability engineering. Beacon owns MTTR-as-SLO; Harvest reports MTTR-as-DORA-input.
- **Launch (elsewhere)**: release planning and execution. Harvest reports deployment frequency; Launch owns the deploy cadence strategy.
- **Guardian (elsewhere)**: PR strategy and gatekeeping. Harvest reports change failure rate; Guardian owns the merge-gate policy.

## Workflow

```
SCOPE     →  confirm repo, window (28-90d typical), branch/env mapping
          →  identify deploy source (release tag / GHA workflow / external)

COLLECT   →  gh pr list --state merged + gh release list + workflow runs
          →  pull incident timestamps (rollback PRs, hotfix labels, external)
          →  per_page=100 + --paginate; cache deploy/incident lookups

COMPUTE   →  DF   = deploys / window
          →  LT   = merge_ts → deploy_ts (P50, P75, P90)
          →  FDRT = failed_deploy_ts → recovered_ts (P50, P75)  [throughput, formerly MTTR-flavored]
          →  CFR  = failed_deploys / total_deploys              [instability]
          →  RR   = unplanned_deploys / total_deploys           [instability, DORA 2024/2025]

CLASSIFY  →  map each metric to its 2025 percentile band (Top 15% / Top 15-30% / Mid / Bottom)
          →  flag inconsistent banding (e.g., Top-15% DF + Bottom CFR = brittle pipeline)

COMPLEMENT→  pair with SPACE: satisfaction, performance, activity, comm, efficiency
          →  add 7-archetype team profile (DORA 2025) where signals available
          →  pull Reliability quasi-metric (incident & availability signal) when SLO data exists

REPORT    →  percentile band table + trend + SPACE notes + AI-period caveat + next actions
```

## DORA 2025 Metric Categorization

DORA 2025 reorganized the metric groupings (cd.foundation 2025-10-16):
- **Throughput** (3 metrics): Deployment Frequency, Lead Time for Changes, **Failed Deployment Recovery Time** (moved from stability — teams with short lead time can deploy fixes quickly).
- **Instability** (2 metrics; renamed from "stability" to reflect that high values indicate problems): Change Failure Rate, **Rework Rate** (new in 2024/2025 report).
- **Reliability** (quasi-metric): user-facing service availability and incident behavior; sourced separately from the delivery pipeline and routed to Beacon for SLO ownership.

## Per-Metric Percentile Thresholds (DORA 2025)

DORA 2025 replaced the Elite/High/Medium/Low bucket labels with percentile distributions. The bands below preserve numeric ranges (still useful for individual-metric framing) and label them with the 2025 percentile equivalents.

| Metric | Top 15% (was "Elite") | Top 15-30% (was "High") | Mid (was "Medium") | Bottom (was "Low") |
|--------|-----------------------|--------------------------|---------------------|---------------------|
| Deployment Frequency (throughput) | On-demand (multiple/day) | On-demand to ~1/week | 1/week - 1/month | < 1/month |
| Lead Time for Changes (throughput) | < 1 day | < 1 week | 1 week - 1 month | > 1 month |
| Failed Deployment Recovery Time (throughput) | < 1 hour | < 1 day | 1 day - 1 week | > 1 week |
| Change Failure Rate (instability) | 0-5% | 5-10% | 10-15% | > 15% |
| Rework Rate (instability, new in DORA 2024/2025) | < 2% | 2-8% | 8-16% | > 16% |

Notes:
- The Top-15% Lead Time band was tightened from "<1 hour" (2023) to "<1 day" in DORA 2025 reporting (multitudes 2025).
- Team profiling MUST use the 7 archetypes (Foundational Challenges / Legacy Bottleneck / Constrained by Process / High Impact Low Cadence / Stable and Methodical / Pragmatic Performers / Harmonious High-Achievers — confirmed in the 2025 report chapter "Understanding your software delivery performance: A look at seven team profiles").
- **Rework Rate** measures unplanned deployments fixing user-visible issues ÷ total deployments. Example: 3 unplanned ÷ 10 total = 30% (cd.foundation 2025-10-16).
- **Failed Deployment Recovery Time** supersedes the older MTTR framing for delivery-pipeline failure recovery; user-facing incident MTTR is reported separately and routed to Beacon as an SLO/Reliability concern.
- **Reliability quasi-metric**: DORA 2025 lists Reliability as a sixth dimension (5 formal + 1 quasi). Treat as input to archetype mapping; do not classify Reliability into the same percentile bands as the 5 formal metrics.

## Measurement Window Selection

| Window | Use when | Caveat |
|--------|----------|--------|
| 7 days | Pulse-check during incident response or sprint demo | High variance; not for percentile-band classification |
| 28 days | Default reporting cadence | Smooths weekly noise, matches DORA survey baseline |
| 90 days | Quarterly review and band classification | Stable signal; required for Top-15% / Bottom determination |
| 180 days+ | Trend and AI-adoption comparison | Note tooling/team changes that confound trend |

## SPACE Complement

| Dimension | DORA gap it fills | Harvest signal |
|-----------|-------------------|----------------|
| Satisfaction | DORA ignores burnout; Elite DF can mask exhaustion | Survey link; PR-after-hours ratio as proxy |
| Performance | DORA measures delivery, not outcome quality | Defect rate, revert rate, customer-reported issues |
| Activity | DORA aggregates; SPACE preserves individual contribution context | PR count + review count, never as ranking |
| Communication | DORA misses collaboration cost | Review comment volume, cross-team PR ratio |
| Efficiency | DORA misses flow interruption | Cycle time 4-phase breakdown (Pickup/Review/Merge) |

Use SPACE to prevent the "Velocity Trap" — Elite DORA scores with collapsing team health.

## gh + GitHub Insights Integration

| Metric | gh source | Insights complement |
|--------|-----------|---------------------|
| Deployment Frequency | `gh release list --limit 100` or `gh run list --workflow=deploy.yml` | Repository Insights → Deployments view |
| Lead Time | `gh pr list --state merged --json mergedAt` + deploy timestamp | Pulse aggregator with per-PR ledger |
| Failed Deployment Recovery Time | `gh run list --workflow=deploy.yml --status failure` → time-to-next-success | Workflow-run timestamps; supplement with redeploy labels |
| Change Failure Rate | Rollback PR labels (`revert`, `hotfix`) / failed deploy runs | Incidents log if external |
| Rework Rate | Unplanned deploys (`revert`, `hotfix`, `rollback`, `regression` labels or commit trailers) / total deploys | Deployment ledger with cause tags |
| Reliability (quasi) | Out of gh scope — pull from SLO/incident tracker | Beacon-owned; Harvest only annotates |

For Lead Time, prefer "merge → deploy" over "first-commit → deploy" to avoid conflating coding time with delivery pipeline time.

## Anti-Patterns

- Using DORA in isolation without SPACE — leads to the "Velocity Trap" where teams optimize delivery speed at the cost of burnout, and Top-15% band scores hide collapsing team health.
- Classifying the team into 4-tier clusters (low/medium/high/elite) — DORA 2025 replaced these with **percentile distributions plus 7 archetypes** that incorporate human factors. Per-metric numeric ranges remain valid; team-level cluster classification does not.
- Mixing measurement windows — comparing this week's DF to last quarter's recovery time is meaningless. Always compute all five metrics on the same window.
- Treating Failed Deployment Recovery Time as a stability metric — DORA 2025 reclassified it into **throughput** (cd.foundation 2025-10-16). Misplacing it confuses categorical analysis.
- Counting deploys without a defined "deploy" event — if the team has no release tags or deploy workflow, manufactured DF numbers mislead. Either define the event or mark the metric as unavailable.
- Lead Time from first commit instead of merge — inflates the metric with coding time DORA does not target. Merge-to-deploy is the canonical definition.
- Comparing pre-AI and post-AI periods without flagging tooling adoption — DORA 2025 confirms AI now positively correlates with throughput (a reversal from DORA 2024's negative finding) but continues to correlate negatively with delivery stability — more change failures, increased rework, longer cycle times to resolve issues. Direct period comparison without this caveat is misleading.
- Reporting CFR with no incident definition — "failed deployment" must be operationalized (rollback PR, hotfix within 24h, post-deploy incident, etc.) or the metric is unauditable.
- Confusing Rework Rate with Change Failure Rate — both are instability metrics but distinct: CFR = % of deploys that failed; Rework Rate = % of deploys that were *unplanned* fixes. A team can have low CFR (deploys succeed) but high Rework Rate (most deploys are reactive).
- Treating Failed Deployment Recovery Time as an SLO — it is a DORA delivery metric. SLO and user-facing Reliability ownership belong to Beacon. Harvest reports the number; Beacon designs the target.
- Band-shopping by changing the window — switching to a 7-day window to claim Top-15% DF when the 90-day average is mid-band is metric gaming. Always document the window.

## Handoff

- **To Pulse**: percentile-band classification + 90-day trend payload for live KPI dashboard. Pulse owns ongoing tracking; Harvest owns the report.
- **To Beacon**: Failed Deployment Recovery Time data, incident timestamps, and Reliability quasi-metric inputs when the team has an SLO program. Beacon translates delivery-recovery numbers into user-facing SLOs with error budget context.
- **To Guardian**: Change Failure Rate and Rework Rate breakdown by PR size and review depth when CFR > 10% or Rework Rate > 8%. Guardian owns merge-gate policy adjustments.
- **To Launch**: Deployment Frequency trend and lead-time bottleneck phase when releases are clustered or delayed. Launch owns the cadence strategy.
- **To Triage**: when the data pipeline blocks band classification (no deploy events, no incident log, gh rate-limited).

## Source Notes

- DORA 2025 / Accelerate State of DevOps Report 2025 — Google Cloud blog (2025-10), `cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report`.
- "The DORA 4 key metrics become 5" — CD Foundation (2025-10-16), `cd.foundation/blog/2025/10/16/dora-5-metrics/`.
- DORA Metrics Best Practices (2025), oobeya, multitudes — confirm Top-15% Lead Time = "< 1 day" in 2025 reporting.
