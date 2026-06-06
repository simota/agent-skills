# Work Hours Estimation

Purpose: Use this reference when Harvest must estimate effort for individual reports or client-facing summaries.

## Contents

- Implemented baseline formula
- Optional refinement layers
- Size bands
- Adjustment factors
- Range reporting rules

## Implemented Baseline Formula

This is the baseline currently implemented in `scripts/generate-report.js`.

```text
baseline_hours =
  ((additions + deletions) / 100)
  + (changedFiles * 0.25)

minimum = 0.5h
rounding = nearest 0.5h
```

Use this baseline unless the report explicitly requires a richer estimate.

## Optional Refinement Layers

These refinements exist in Harvest guidance and may be applied manually when the audience needs more nuance:

| Layer | Rule |
|------|------|
| File weights | `test=0.7`, `config=0.5`, `docs=0.3`, `source=1.0` |
| New-file bonus | `new_files * 0.5h` |
| Review-time overlay | `business_hours(createdAt, mergedAt) * 0.2` |
| Complexity multiplier | Add `20-100%` depending on architecture, security, APIs, or multi-service impact |

If you apply refinement layers, say so explicitly in the report.

## Size Bands

| Band | Total changed lines | Typical range |
|------|---------------------|---------------|
| `XS` | `< 50` | `0.5-1h` |
| `S` | `50-200` | `1-3h` |
| `M` | `200-500` | `3-8h` |
| `L` | `500-1000` | `8-16h` |
| `XL` | `> 1000` | `16h+` |

## Adjustment Factors

Use these only as additive caution, not as hard truth:

| Factor | Suggested adjustment |
|--------|----------------------|
| New architecture or novel pattern | `+50-100%` |
| Security-sensitive work | `+30-50%` |
| Data integrity risk | `+30-50%` |
| External API integration | `+20-40%` |
| Performance-sensitive work | `+20-40%` |
| Multi-service change | `+20-30%` |
| Significant test work | `+10-20%` |

## Range Reporting Rules

Prefer ranges for management or client reporting:

```text
min      = expected * 0.7
expected = refined_or_baseline
max      = expected * 1.5
```

Rules:
- Label hours as estimates.
- Do not present LOC-derived values as productivity rankings.
- Warn when night/weekend work exceeds `10%` of activity because fatigue can distort effort signals.

## AI-Assisted Coding Caveat (2026)

LOC-based effort estimation breaks down when AI coding assistants are in heavy use:
- DORA 2025 finds AI now positively correlates with throughput; LinearB 2025 separately reports that PR size distribution has shifted larger in AI-heavy teams.
- This means equal LOC counts pre/post AI adoption represent different human effort. Always tag the report with the team's AI tooling posture (Copilot in IDE, Claude Code, Cursor, etc.) so consumers can interpret the LOC-derived hours.
- Prefer time-based signals (review-cycle time, PR pickup time) over LOC-derived hours when AI usage is significant.
