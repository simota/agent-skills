# Learning Feedback Loop Reference

Purpose: Calibrate Guardian from Judge, Zen, Harvest, and squash outcomes without overfitting to too little evidence.

## Contents

- Feedback sources
- `JUDGE_TO_GUARDIAN_FEEDBACK`
- Calibration rules
- `.agents/guardian.md` storage
- Improvement metrics
- Squash learning
- AUTORUN and Harvest integration

## Feedback Sources

Primary sources:
- `JUDGE_TO_GUARDIAN_FEEDBACK`
- `ZEN_TO_GUARDIAN_HANDOFF`
- `HARVEST_TO_GUARDIAN_HANDOFF`
- squash outcome feedback

Use feedback to update:
- prediction confidence
- quality score calibration
- pattern exceptions
- team preferences

## `JUDGE_TO_GUARDIAN_FEEDBACK`

```markdown
## JUDGE_TO_GUARDIAN_FEEDBACK

**PR**: #123 - feat(auth): add OAuth2 support
**Review Status**: CHANGES_REQUESTED

### Guardian's Predictions vs Actual Findings
| Predicted Issue | Predicted Severity | Actual Finding | Match |
|-----------------|-------------------|----------------|-------|
| Null pointer oauth.ts:45 | HIGH | Confirmed | TRUE_POSITIVE |
| Race condition token.ts:33 | MEDIUM | Not found | FALSE_POSITIVE |
| - | - | XSS in callback.ts:72 | FALSE_NEGATIVE |

### Prediction Accuracy for This PR
- Judge precision: ...
- Judge recall: ...
```

## Calibration Rules

### Prediction confidence

- initial confidence: `70%`
- true positive: `+5%`
- false positive: `-10%`
- false negative: `+10%` sensitivity on similar patterns
- bounds: minimum `30%`, maximum `95%`

### Threshold calibration

Trigger threshold recalibration when:
- `3` consecutive same-direction adjustments occur

### Quality score calibration

Target prediction bands:
- `A+` predicted: `95+`
- `A` predicted: `85-94`
- keep average deviation `< 15%`

### No-adjust guardrail

Do not recalibrate major heuristics from too little evidence:
- fewer than `3` relevant examples
- contradictory feedback without a clear dominant pattern

## `.agents/guardian.md` Storage

Store project-specific learning in this shape:

```markdown
# Guardian Calibration Data

## Last Updated
2026-03-06

## Pattern Exceptions
- naming:
  - ...

## Team Preferences
- squash:
  - ...

## Historical Accuracy
- prediction_accuracy: ...
- false_positive_rate: ...
```

## Improvement Metrics

Targets:
- prediction accuracy `> 75%`
- false positive rate `< 20%`
- average score deviation `< 15%`

## Squash Learning

Use squash calibration only when:
- `5+` data points show repeated factor misalignment

Examples:
- pairwise score too permissive on multi-author chains
- file-overlap weighting overfits noisy commits

## AUTORUN Integration

AUTORUN may:
- apply existing learned thresholds
- update confidence scores from explicit downstream feedback

AUTORUN must not:
- override stable heuristics from tiny samples
- silently change team-wide thresholds without surfacing it

## Harvest Integration

Use Harvest data to learn:
- merged PR outcomes
- review turnaround
- split strategy success
- squash strategy effectiveness across PRs
