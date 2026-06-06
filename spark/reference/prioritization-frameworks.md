# Spark Prioritization Frameworks Reference

Purpose: provide the canonical scoring rules Spark uses to compare ideas and write measurable hypotheses.

## Contents
- Impact-Effort matrix
- RICE scoring
- Hypothesis templates

## Impact-Effort Matrix

Quadrants:
- `Quick Win`: high impact, low effort, do first
- `Big Bet`: high impact, high effort, consider carefully
- `Fill-In`: low impact, low effort, do if time allows
- `Time Sink`: low impact, high effort, usually avoid

Impact scale:

| Score | Meaning | Example |
| --- | --- | --- |
| `5` | core workflow improvement | reduces a daily task by `50%` |
| `4` | significant time savings | automates a repetitive 10-minute task |
| `3` | nice enhancement | better feedback or visibility |
| `2` | minor improvement | easier navigation |
| `1` | negligible value | cosmetic change only |

Effort scale:

| Score | Meaning | Typical scope |
| --- | --- | --- |
| `5` | major architectural change | multiple weeks, many files |
| `4` | cross-cutting change | several days |
| `3` | isolated component work | `1-2 days` |
| `2` | minor code change | hours |
| `1` | trivial config or copy | minutes |

## RICE

Formula:

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

Definitions:
- `Reach`: users or customers affected per quarter
- `Impact`: `0.25`, `0.5`, `1`, `2`, `3`
- `Confidence`: `100%`, `80%`, `50%`
- `Effort`: person-months, including design, build, test, and release

Priority thresholds:
- `> 100`: high priority
- `50-100`: medium priority
- `< 50`: low priority

### `## RICE Evaluation: [Feature Name]`

Required fields:
- `Reach`
- `Impact`
- `Confidence`
- `Effort`
- `Calculation`
- `RICE Score`

## Hypothesis Templates

### `## Hypothesis: [Feature Name]`

Required fields:
- `We believe that`
- `For`
- `Will achieve`
- `We will know we are successful when`
- `We will validate this by`
- `Timeline`

### `## Hypothesis Card`

Required fields:
- `ID`
- `Feature`
- `Status`
- `Target Persona`
- `Target Metric`
- `Current Baseline`
- `Target Goal`
- `Validation Method`
- `Sample Size`
- `Timeline`
- `Key Assumptions`
- `Risks`
- `Minimum Success Criteria`

### `## Hypothesis Tracker`

Track:
- `ID`
- `Feature`
- `Status`
- `Metric`
- `Result`
