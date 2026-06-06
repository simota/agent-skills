# Predictive Quality Gate Reference

Purpose: Predict likely Judge and Zen findings before review so Guardian can warn early without over-blocking.

## Contents

- Judge prediction
- Zen prediction
- historical learning
- predictive report
- review-flow integration
- accuracy tracking

## Judge Prediction

Typical Judge issue families:
- null handling
- race conditions
- logic bugs
- missing guards
- unsafe assumptions

Confidence bands:
- high: `>= 80%`
- medium: `60-79%`
- low: `< 60%`

Warning rule:
- high confidence -> always warn
- medium confidence -> warn only if `risk_score > 50`

## Zen Prediction

Typical Zen issue families:
- generic names
- mixed naming conventions
- large functions
- magic numbers
- noisy formatting mixed with logic

Auto-fix rule:
- only for code-quality issues
- only when confidence `> 90%`

## Historical Learning

Adjust predictions with:
- accepted or rejected Judge findings
- accepted or rejected Zen suggestions
- project-specific false positive patterns

False positive handling:
- decrease pattern confidence by `5%`

## Predictive Report

```markdown
## Predictive Quality Gate Analysis

### Predicted Judge Findings
- possible null handling issue (85%)

### Predicted Zen Suggestions
- split formatting noise from logic change (92%)
```

## Integration With Review Flow

Use predictive findings before review to:
- enrich Guardian's report
- decide whether Judge or Zen should be called early
- avoid unnecessary review churn

Pause when:
- predicted security issue is high confidence
- predicted logic bug is high confidence and high impact
- multiple predicted fixes conflict

## Accuracy Tracking

Targets:
- Judge prediction accuracy `> 75%`
- Zen prediction accuracy `> 80%`
- false positive rate `< 20%`

Canonical accuracy report:

```markdown
## Prediction Accuracy Report (Last 30 Days)

### Judge Predictions
- accuracy: ...

### Zen Predictions
- accuracy: ...
```
