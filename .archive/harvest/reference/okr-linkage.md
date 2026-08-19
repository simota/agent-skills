# OKR Linkage Report Reference

Purpose: Connect PR activity to Objectives and Key Results so quarterly reviews trace from outcome (O) through measurable progress (KR) down to delivered work (PR). Produces a PR-to-Objective mapping, KR progress narrative, and Objective health score grounded in the actual git/PR record rather than self-reported status.

## Scope Boundary

- **harvest `okr`**: PR-to-Objective mapping and KR narrative for a quarter or OKR window. Outcome-vs-output framing.
- **harvest `weekly` / `monthly` (elsewhere)**: time-window aggregation without Objective linkage.
- **harvest `release` (elsewhere)**: changelog by release, not by Objective.
- **harvest `retro` (elsewhere)**: sprint narrative; OKR is quarterly and outcome-focused.
- **Pulse (elsewhere)**: KPI dashboard. Pulse owns ongoing KR tracking; Harvest produces the linkage report.
- **Beacon (elsewhere)**: SLO/error budget. Beacon may surface KRs framed as reliability targets, but Objective health is not Beacon's domain.
- **Launch (elsewhere)**: release planning. Launch may map releases to KRs but does not score Objective health.
- **Guardian (elsewhere)**: PR strategy. Guardian sees PRs as merge candidates; Harvest sees them as KR contributions.

## Workflow

```
SCOPE     →  identify the OKR set (quarter, team, company); load O/KR catalog
          →  agree tagging convention (label / commit-trailer / linked issue)

COLLECT   →  gh pr list --state merged + label/issue filters for the window
          →  fetch commit messages for trailers (e.g., OKR: O1.KR2)
          →  resolve linked issues for indirect mapping

MAP       →  bucket each merged PR under at most one primary KR
          →  flag PRs with no OKR tag for review (orphan rate is a signal)

NARRATE   →  for each KR: progress sentence built from PR titles + labels
          →  separate "shipped" from "in-flight"; cite PR numbers as evidence

SCORE     →  Objective health 0-100 (KR coverage, momentum, risk flags)
          →  flag vanity-metric risk and output-vs-outcome confusion

REPORT    →  Objective table + KR narratives + orphan PR list + next quarter
```

## PR-to-Objective Tagging Conventions

| Method | Example | Pros | Cons |
|--------|---------|------|------|
| Label | `okr:Q2-O1-KR2` | Visible in gh UI; easy filter | Manual; drift between teams |
| Commit trailer | `OKR: O1.KR2` in body | Survives squash-merge; auditable | Requires team discipline |
| Linked issue | PR closes `#123` tagged `okr:Q2-O1-KR2` | Indirect via issue board | Two-hop mapping; orphan risk |
| PR title prefix | `[O1.KR2] feat: ...` | Visible in lists | Title bloat; collision with conventional commits |

Pick one and document it. Mixing conventions inflates orphan rate and degrades the report.

## KR Progress Narrative Template

```
KR: <verb + measurable result + deadline>
Baseline: <starting value, date>
Current: <latest value, source>
Progress: <%, momentum direction>

Evidence (this window):
- <PR #N>: <title> — <contribution to KR>
- <PR #N>: <title> — <contribution to KR>

Confidence: High | Medium | Low
Risks: <blockers, dependencies, flat-lining>
```

Narrative draws from PR titles and labels — never invent contributions. If no PRs map, state "No PR activity attributed this window" rather than fabricating progress.

## Objective Health Scoring (0-100)

| Component | Weight | Signal |
|-----------|--------|--------|
| KR coverage | 30 | % of KRs with attributed PR activity in the window |
| Momentum | 25 | KR progress delta vs prior window |
| Evidence quality | 20 | Tagged-PR / total-PR ratio (orphan inverse) |
| Risk flags | 15 | Blocker labels, stalled KRs, dependency churn |
| Confidence diversity | 10 | KR confidence spread (all-High is a smell) |

| Score | State | Action |
|-------|-------|--------|
| 80-100 | Healthy | Continue; consider stretch |
| 60-79 | At risk | Re-prioritize; surface blockers |
| 40-59 | Off track | Reset or descope; escalate |
| 0-39 | Failing | Postmortem; consider abandoning |

Health is a triage signal, not a performance review input. Never use to rank teams.

## Quarterly Review Aggregation

| Section | Source |
|---------|--------|
| Objective health table | Score per O with color-coded state |
| KR narrative roll-up | One paragraph per KR with PR evidence |
| Orphan PR analysis | % of merged PRs with no OKR tag, with examples |
| Cross-Objective conflicts | PRs that touched multiple Objectives' code |
| Next quarter signals | KRs trending to miss; capacity recommendations |

Aggregate at the team level. Do not roll Objective health up to individual contributors — this turns OKRs into a performance scorecard, the canonical anti-pattern.

## Anti-Patterns

- Vanity metrics in KRs (PR count, LOC delivered, commits authored) — these are output, not outcome. KRs measure "did the world change for users" not "did we type more". Reject KR proposals framed as developer activity counts. Christina Wodtke's *Radical Focus* (2nd ed.) emphasizes that Key Results should be "challenging targets that you only have a 50/50 chance of accomplishing" — output counts have no such risk profile and inflate to 100% trivially.
- Output-vs-outcome confusion — "ship feature X" is output. "X-driven retention up 5pp" is outcome. Harvest reports must keep the distinction visible; if the team only has output KRs, flag it explicitly.
- Rolling Objective health up to individuals — destroys OKR psychological safety. Stack-ranking by KR contribution turns OKRs into management theater (McKinsey developer productivity controversy, 2023).
- Tagging every PR retroactively to inflate KR coverage — gaming. The tag must be set at PR-creation/merge time, not back-applied during the quarterly review.
- All-Green KR confidence — diversity-of-confidence (some Yellow / Red) is a health signal. All-Green typically indicates fear of reporting risk, not actual health.
- Counting in-flight PRs as KR progress — only merged PRs count as evidence. Open PRs are intent, not progress.
- Mapping one PR to many KRs — primary attribution must be unique. Many-to-many mapping inflates apparent progress and breaks aggregation.
- Treating OKR misses as failures — OKRs are stretch goals; 60-70% achievement is healthy. Reports framing < 100% as failure encourage sandbagging next quarter.
- Skipping orphan analysis — if 60% of merged PRs are not tagged to any Objective, the OKR system is decorative. Surface this explicitly so leadership sees the gap.

## Handoff

- **To Pulse**: live KR progress dashboard. Pulse owns the running tracker; Harvest produces the quarterly snapshot and orphan analysis.
- **To Beacon**: KRs framed as reliability targets (SLO uptime, MTTR ceiling). Beacon owns SLO design; Harvest reports OKR-side health.
- **To Launch**: KRs gated by releases. Launch coordinates release-to-KR alignment; Harvest reports the linkage.
- **To Guardian**: when orphan-PR rate exceeds 50% — Guardian owns PR-template policy and can require OKR labels at merge.
- **To Triage**: when Objective health < 40 and KRs are blocked by cross-team dependencies the team cannot resolve.
