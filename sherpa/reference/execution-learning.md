# Execution Learning System (CALIBRATE)

Purpose: Use this file after execution to compare estimates with reality, update multipliers, and emit reusable planning patterns.

## Contents

- CALIBRATE overview
- RECORD data
- COMPARE thresholds
- ADJUST rules
- PERSIST journal format
- Velocity prediction

## Overview

`RECORD -> COMPARE -> ADJUST -> PERSIST`

Calibration keeps Sherpa from repeating static estimates after new evidence appears.

## RECORD

Capture after each completed step:

```yaml
Step: [name]
Estimated: [minutes]
Actual: [minutes]
Size: [XS/S/M/L]
Complexity_Factors: [list]
Risk_Level: [Low/Medium/High]
Agent: [who executed]
Domain: [frontend/backend/infra/test/docs]
Outcome: [clean/rework/blocked]
Notes: [observations]
```

## COMPARE

### Accuracy Ratio

```text
Accuracy Ratio = Estimated / Actual

> 1.2   overestimated
0.8-1.2 good estimate
< 0.8   underestimated
```

### Target Range

- target long-run average: `0.85-1.15`
- compare patterns across sessions, not just one step

### Trend Example

| Session | Avg Ratio | Interpretation |
| --- | --- | --- |
| 1 | 0.72 | many unknowns |
| 2 | 0.85 | improving |
| 3 | 0.95 | stable |
| 4 | 0.92 | healthy |

## ADJUST

### Base Multipliers

```yaml
new_technology: 1.5x
unclear_requirements: 1.5x
external_dependency: 2.0x
high_risk: 1.5x
multiple_files: 1.3x
```

### Adjustment Rules

1. require `3+` data points before changing a multiplier
2. cap each session adjustment at `+/-0.3x`
3. decay toward default by `10%` per month
4. explicit user override beats learned calibration

## PERSIST

Record calibration learnings in `.agents/sherpa.md`.

```markdown
## YYYY-MM-DD - Calibration: [Project/Epic Name]

**Sessions analyzed**: N
**Overall accuracy**: X.XX
**Key adjustments**:
- [factor]: [old] -> [new] (reason)

**Pattern discovered**: [description]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Sherpa
date: YYYY-MM-DD
summary: [calibration insight]
affects: [Sherpa, relevant agents]
priority: MEDIUM
reusable: true
-->
```

## Pattern Library

| Pattern | Typical duration | Common risk | Example note |
| --- | --- | --- | --- |
| New API endpoint | `60-90 min` | external dependency | add `1.3x` for first endpoint |
| UI component | `45-75 min` | design drift | stabilizes after the second iteration |
| Bug fix | `30-60 min` | unclear root cause | `Scout` first often saves time |
| Refactor | `60-120 min` | scope creep | strict scope prevents blow-up |
| Test suite | `40-80 min` | flaky dependency | mock early |

## Velocity Prediction

```text
Predicted Remaining = sum(remaining calibrated estimates)
Confidence Band = Predicted × [0.8, 1.3]
```

### Re-Planning Thresholds

| Current velocity | Action |
| --- | --- |
| `> 1.2x` estimate | combine very small remaining steps if safe |
| `0.8-1.2x` | stay on plan |
| `0.5-0.8x` | split smaller and add buffer |
| `< 0.5x` | stop and re-plan |

## Quick Calibration

For sessions `< 1 hour` or `< 5` completed steps:

```markdown
## Quick Calibration

**Steps**: 3 completed
**Avg accuracy**: 0.90
**Action**: no multiplier change yet
```
