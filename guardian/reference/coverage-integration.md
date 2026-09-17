# Coverage Integration

Read when changed files have CI coverage or a coverage gap affects risk. Discover the actual report path and parse its format: LCOV, Cobertura, or Istanbul. A file-level summary alone cannot prove changed-line coverage; report that evidence gap rather than substituting whole-file coverage.

## Decision Thresholds

These are Guardian routing/scoring thresholds, not universal test-quality guarantees.

| Signal | Classification |
|--------|----------------|
| Changed-line coverage `< 0.50` | Critical changed-line signal |
| Auth/security coverage `< 80%`; new payment logic `< 90%`; changed code `0%` | Critical gap |
| Core business logic `< 70%`; hotspot `< 60%`; regression risk `> 5%` | High-priority gap |

Route to Radar on any of:
- High-risk file with `coverage_gap > 0.40`.
- Hotspot with coverage `< 0.50`, or critical file with no tests.
- Coverage regression `> 5%` with high risk, or `regression_risk > 0.70`.

## Score

The Test Score component weights line coverage `30%`, branch coverage `25%`, changed-line coverage `25%`, test quality `10%`, and coverage delta `10%`. Its overall PR-quality weight is `15%`.

## Handoff and Output

`GUARDIAN_TO_RADAR_HANDOFF (Coverage)` includes **PR / Branch**, **Reason**, **Critical files** with measured coverage/evidence, and **Requested action**: focused tests, closure of changed-line gaps, and residual-risk report.

Use `Coverage Gap Analysis` with `Critical Gaps (Must Fix)` and `High Priority Gaps`; use `Coverage Integration Report` with `PR Coverage Summary` and `Test Score Breakdown`. Include only measured results; absent coverage stays unknown.

AUTORUN may parse, correlate, and report. Pause when a critical gap combines with another blocking condition or inconsistent data invalidates scoring. Missing data follows `reference/autorun-mode.md` partial-result handling.
