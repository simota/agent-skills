# Intelligence Calibration System

Purpose: Use this file when running `SHARPEN`, validating predictions, tuning source reliability, or emitting reusable competitive patterns.

## Contents

- SHARPEN loop
- Tracking schema
- Accuracy bands
- Source calibration
- Confidence by analysis type
- Propagation format

## SHARPEN Loop

`TRACK -> VALIDATE -> CALIBRATE -> PROPAGATE`

Without SHARPEN, analyses decay into one-off opinions. With SHARPEN, Compete learns which sources, claims, and outputs actually matter.

## TRACK

Record every material analysis.

```yaml
Analysis: [analysis-id]
Type: [SWOT | Feature Matrix | Positioning | Battle Card | Alert Response | Market Trends]
Competitors_Analyzed: [list]
Sources_Used: [list with reliability tier]
Key_Predictions:
  - prediction: [description]
    confidence: [High/Medium/Low]
    timeframe: [validation window]
Actionability: [immediately_actionable | needs_further_research | monitoring_only]
Downstream_Handoff: [Spark | Growth | Helm | None]
```

Track at minimum:

| Data Point | Why |
|---|---|
| prediction accuracy | calibrates confidence |
| source reliability | tunes evidence weighting |
| actionability rate | tells whether outputs change decisions |
| downstream utilization | shows whether handoffs are usable |
| alert hit rate | tunes urgency thresholds |

## VALIDATE

### Accuracy Bands

| Accuracy | Interpretation | Default action |
|---|---|---|
| `> 0.80` | strong analyst performance | maintain method |
| `0.60-0.80` | acceptable with room to improve | inspect weak spots |
| `< 0.60` | weak prediction quality | review sources and framing |

### Validation Triggers

| Trigger | Check |
|---|---|
| feature launch | feature prediction accuracy |
| pricing change | price intelligence accuracy |
| trend materialization | market trend accuracy |
| win/loss update | battle card effectiveness |
| quarterly review | overall intelligence quality |

### Summary Template

```markdown
### Validation Report

| Metric | Value | Trend |
|---|---|---|
| Analyses produced | 12 | — |
| Predictions made | 8 | — |
| Predictions validated | 5 | — |
| Accuracy rate | 80% (4/5) | ↑ |
| Actionability rate | 67% (8/12) | — |
| Downstream utilization | 75% (6/8) | — |

Strongest area: [...]
Weakest area: [...]
```

## CALIBRATE

### Default Reliability Weights

```yaml
official_sources: 0.90
review_platforms: 0.75
financial_data: 0.85
job_postings: 0.65
community_signals: 0.60
```

### Calibration Rules

1. require `3+` data points before changing a source weight
2. maximum adjustment per cycle is `+/-0.15`
3. learned adjustments decay `10%` per quarter toward defaults
4. explicit user source preferences override calibration

### Confidence by Analysis Type

| Analysis Type | Typical Accuracy | Default Confidence |
|---|---:|---|
| Feature Matrix | `85%` | High |
| Tech Stack | `90%` | High |
| SWOT | `70%` | Medium |
| Market Trends | `60%` | Medium |
| Pricing | `55%` | Low |

## PROPAGATE

### Journal Entry

```markdown
## YYYY-MM-DD - SHARPEN: [Analysis Type]

Analyses validated: N
Overall accuracy: X%
Key insight: [...]
Calibration adjustment: [source/type: old -> new]
Apply when: [...]
reusable: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Compete
date: YYYY-MM-DD
summary: [intelligence insight]
affects: [Compete, Helm, Growth]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

| Pattern | Indicators | Typical Timeframe | Reliability |
|---|---|---|---|
| Pricing undercut | price reduction `10%+` | `1-3 months` | High |
| Feature convergence | `3+` competitors ship the same feature | `6-12 months` | Medium |
| Market consolidation | `2+` acquisitions in segment | `12-24 months` | Medium |
| Niche expansion | leader enters adjacent market | `3-6 months` | High |
| Talent drain | key hires move to competitor | `6-12 months` | Low |

### Quick SHARPEN

Use this when there are too few predictions to recalibrate.

```markdown
## Quick SHARPEN

Analyses: 2
Predictions: 1
Note: insufficient data to recalibrate
Action: keep current weights
```
