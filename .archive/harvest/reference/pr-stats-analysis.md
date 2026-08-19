# PR Statistics Deep-Dive Reference

Purpose: Statistical deep-dive of PR flow — cycle time histogram with phase decomposition, P50/P75/P90 latency reporting, contributor distribution via Lorenz curve, bot/human ratio, and large-PR risk flagging. Surfaces flow bottlenecks and concentration risk that aggregate means hide.

## Scope Boundary

- **harvest `prstats`**: distributional and risk-focused PR analytics. Histograms, percentiles, Lorenz, large-PR flags.
- **harvest `weekly` / `monthly` (elsewhere)**: aggregate counts and category breakdowns without distribution analysis.
- **harvest `dora` (elsewhere)**: DORA 5-metric percentile-band classification (DORA 2025). Lead Time at the DORA level; prstats decomposes into Pickup/Review/Merge phases.
- **harvest `okr` (elsewhere)**: outcome linkage; prstats is purely flow-statistics.
- **Pulse (elsewhere)**: live dashboards. Pulse owns ongoing tracking; prstats produces the depth report.
- **Beacon (elsewhere)**: reliability SLOs. Cycle time is delivery flow, not reliability.
- **Launch (elsewhere)**: release planning. Launch reads prstats output to size release windows.
- **Guardian (elsewhere)**: PR strategy and review policy. Guardian acts on prstats findings (large-PR thresholds, review-wait alerts).

## Workflow

```
SCOPE     →  repo, window (28-90d), branch filter, bot allowlist

COLLECT   →  gh pr list --state merged --json with timestamps + author + LOC
          →  fetch reviews timeline for first-response and approval times
          →  per_page=100 + --paginate

DECOMPOSE →  Coding (first-commit → ready-for-review)
          →  Pickup (ready → first review action)
          →  Review (first review → approval)
          →  Merge  (approval → merged)

DISTRIBUTE→  P50 / P75 / P90 per phase + total cycle
          →  histogram bins by hour up to 5d, then daily

CONCENTRATE→ Lorenz curve over PR authors; Gini coefficient
          →  bot vs human ratio (allowlist-driven)

RISK FLAG →  large PRs (>500 LOC) with review-time and defect-correlation note
          →  rubber-stamp candidates (low review time, uncorrelated with size)

REPORT    →  histograms + percentiles + Lorenz + large-PR ledger + actions
```

## Cycle Time Decomposition Benchmarks

| Phase | Elite | Good | Flag |
|-------|-------|------|------|
| Coding (first-commit → ready) | < 24h | < 3d | > 7d |
| Pickup (ready → first review) | < 6h | < 13h | > 1 business day |
| Review (first review → approval) | < 8h | < 24h | > 2 business days |
| Merge (approval → merged) | < 2h | < 8h | > 1 business day |
| Total cycle | < 26h | < 48h | > 5 business days |

(LinearB 2025 Engineering Benchmarks Report — 6.1M+ PRs across 3,000 teams; `linearb.io/blog/2025-engineering-benchmarks-insights`. Cycle starts at "ready for review" — draft PRs distort if measured from creation.)

**PR Maturity (new in LinearB 2025)**: measures how well-prepared a PR is when submitted for review (description quality, linked issues, CI green, test coverage delta). Higher PR maturity correlates with faster merges and higher team velocity. When available, surface PR maturity alongside PR size — small + mature PRs are the highest-velocity profile per the 2025 benchmarks.

## P50 / P75 / P90 Reporting

Always report three percentiles. Mean alone hides tail latency.

| Percentile | What it tells | Use for |
|------------|---------------|---------|
| P50 (median) | Typical PR experience | Headline metric |
| P75 | Upper-quartile pain | Capacity sizing |
| P90 | Tail risk | SLO-style review-wait targets |

Report P90 explicitly; if P90 is 4× P50, the team has a long-tail problem (large PRs, weekend lulls, single-reviewer bottleneck) that the median hides.

## Contributor Distribution (Lorenz / Gini)

| Gini | State | Interpretation |
|------|-------|----------------|
| 0.0 - 0.3 | Even | Healthy team distribution |
| 0.3 - 0.5 | Skewed | Normal for small teams or specialized roles |
| 0.5 - 0.7 | Concentrated | Bus-factor risk; 1-2 authors carry most flow |
| > 0.7 | Highly concentrated | Single point of failure; succession risk |

Lorenz curve plots cumulative-PRs vs cumulative-authors. Use as concentration diagnostic — never as ranking. Pair with bus-factor analysis when Gini > 0.5.

## Bot vs Human Ratio

| Ratio (bot / total) | Reading |
|---------------------|---------|
| < 10% | Low automation; review burden falls on humans |
| 10-30% | Healthy automation (Renovate, Dependabot, codegen) |
| 30-60% | Heavy automation; verify humans still see meaningful review load |
| > 60% | Bot flood; human PRs may be drowning in noise — split reports |

Maintain an explicit bot allowlist (Dependabot, Renovate, github-actions, etc.). Default heuristics (`[bot]` suffix, `type: Bot`) are a fallback only — false-negative rate is non-trivial.

## Large-PR Risk Thresholds

| Size | Classification | Risk |
|------|---------------|------|
| ≤ 200 LOC | Small | Healthy |
| 201-400 LOC | Medium | Monitor |
| 401-500 LOC | Approaching large | Suggest split |
| 501-1000 LOC | Large | 70% lower defect-detection vs small |
| > 1000 LOC | Oversized | Recommend Sherpa split + Guardian gate |

Flag any PR > 500 LOC in the report with: review-time, reviewer count, comment count, and author. When > 30% of PRs exceed 400 LOC, recommend stacked PRs — Graphite's published customer data shows up to ~36% more PRs shipped per engineer and ~17% reduction in median PR size after adopting stacked workflows (`graphite.com/customer/semgrep`, `graphite.com/blog/stacked-prs`). InfoQ reports GitHub itself shipped native stacked-PR support in 2026-04 (`infoq.com/news/2026/04/github-stacked-prs/`).

## Dashboard Recipe

| Panel | Source |
|-------|--------|
| Cycle time histogram (4 phase stack) | Decompose section |
| P50/P75/P90 trend (28d rolling) | Distribution section |
| Lorenz curve + Gini | Concentration section |
| Bot/human ratio (stacked area) | Bot section |
| Large-PR ledger (>500 LOC) | Risk section |
| Rubber-stamp candidates table | Risk section |

Hand off to Pulse for live rendering; Harvest produces the spec and seed data.

## Anti-Patterns

- Reporting mean cycle time only — hides long-tail PRs that drive perceived pain. Always report P50/P75/P90.
- Measuring cycle from PR creation instead of ready-for-review — draft PRs inflate the metric. Use the ready-for-review timestamp.
- Counting bot PRs as developer flow — Dependabot at 50/week makes the team look productive while masking human PR drought. Always split bot/human.
- Lorenz / Gini as performance ranking — concentration is a system property (bus-factor, role specialization), not an individual scorecard. Never use to rank.
- Single LOC threshold for "large" — 500 LOC in a config refactor and 500 LOC in core business logic carry different risk. Flag with file-type context.
- Rubber-stamp blind spot — if median review lead time is < 30min and uncorrelated with PR size, reviewers are likely not reading. Surface the correlation explicitly.
- AI-period comparison without caveat — DORA 2025 reports AI now positively correlates with throughput but negatively with delivery stability (more change failures, increased rework, longer cycle times to resolve issues). Comparing pre-AI P90 to post-AI P90 without that caveat is misleading. Also note GitHub Copilot Code Review reached GA in 2025-04 (`docs.github.com/en/copilot/concepts/agents/code-review`) — review timestamps from automated Copilot reviewers should be split from human review timestamps; rubber-stamp detection rules apply differently when the "reviewer" is an LLM.
- Histogram with arithmetic bins on long-tail data — use log-spaced bins or hour-then-day stratification; arithmetic bins compress the interesting tail.
- Treating P90 as an SLO target without team agreement — Harvest reports the number; the team and Beacon set targets. Reporting an unagreed target is policy creep.

## Handoff

- **To Pulse**: histogram and percentile time-series payload for live dashboards.
- **To Beacon**: when the team wants review-wait SLOs (e.g., P90 pickup < 1 business day). Beacon owns SLO design.
- **To Guardian**: large-PR ledger and rubber-stamp candidates for review-policy adjustment.
- **To Sherpa**: oversized PR list (> 1000 LOC) with recommended split candidates.
- **To Launch**: cycle-time tail data for release-window sizing.
- **To Triage**: when data is too sparse for percentiles (< 30 PRs in window) or gh access is blocked.
