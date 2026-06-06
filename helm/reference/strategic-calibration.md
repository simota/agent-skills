Purpose: Use `FORESIGHT` after strategy work to track forecast quality, recalibrate heuristics, and share reusable patterns without overreacting to thin data.

## Contents
- Workflow
- Accuracy and bracket thresholds
- Calibration rules
- Default assumption library
- Propagation format

# Strategic Calibration System (FORESIGHT)

`FORESIGHT = TRACK -> VALIDATE -> CALIBRATE -> PROPAGATE`

Use this after a simulation, quarterly review, or any point where outcomes can be compared with predictions.

## Workflow

| Phase | Goal | Keep |
|---|---|---|
| `TRACK` | Record what Helm predicted | simulation type, horizon, frameworks, assumptions, confidence, data completeness |
| `VALIDATE` | Compare predictions with actuals | accuracy rate, bracket rate, downstream utilization |
| `CALIBRATE` | Tune heuristics conservatively | framework effectiveness, scenario ranges, assumption defaults |
| `PROPAGATE` | Share reusable learnings | journal note, `EVOLUTION_SIGNAL`, future default updates |

## TRACK

Record each engagement in a compact structure:

```yaml
Simulation: [simulation-id]
Type: [SWOT | PESTLE | Porter | BCG | BSC | Ansoff | Full Strategy | KPI Forecast | M&A Evaluation | Crisis Response]
Horizon: [SHORT(0-1yr) | MID(1-3yr) | LONG(3-10yr)]
Frameworks_Applied: [list]
Scenarios_Generated: [count]
Key_Predictions:
  - prediction: [description]
    metric: [measurable KPI]
    baseline_value: [current]
    predicted_value: [target]
    confidence: [High/Medium/Low]
    timeframe: [validation date]
Assumptions_Used:
  - assumption: [description]
    source: [data/industry_default/estimate]
    sensitivity: [High/Medium/Low]
Data_Completeness: [Tier 1 only | Tier 1+2 | Tier 1+2+3 | Full]
Downstream_Handoff: [Magi/Scribe/Sherpa/Canvas/None]
```

Track at minimum:

| Signal | Why it matters |
|---|---|
| Prediction accuracy | Calibrates scenario confidence |
| Framework effectiveness | Tunes framework selection by context |
| Assumption accuracy | Improves default values when data is missing |
| Scenario bracketing quality | Checks whether optimistic/pessimistic ranges are realistic |
| Data completeness impact | Shows whether more data materially improves quality |
| Downstream utilization | Tests whether Helm output is decision-ready |

## VALIDATE

### Accuracy Thresholds

```text
Accuracy = predictions within ±15% of actual / total validated predictions

> 0.75      strong
0.50-0.75   moderate
< 0.50      weak
```

### Scenario Bracket Thresholds

```text
Bracket Rate = actuals inside optimistic-pessimistic range / total scenarios

> 0.85      well-calibrated
0.70-0.85   acceptable
< 0.70      too narrow or biased
```

### Validation Triggers

| Trigger | Validate |
|---|---|
| Quarterly KPI results | Short-term forecasts |
| Annual results | Mid-term forecasts |
| New industry report | Long-term trend assumptions |
| Strategy drift detected | Assumption validity |
| M&A / exit result known | Valuation logic |

### Validation Snapshot

```markdown
### Strategic Validation

| Metric | Value | Trend |
|--------|-------|-------|
| Simulations completed | 8 | — |
| Predictions made | 15 | — |
| Predictions validated | 10 | — |
| Accuracy rate (±15%) | 70% (7/10) | ↑ |
| Scenario bracket rate | 80% (8/10) | — |
| Framework combinations used | 5 | — |
| Downstream utilization | 88% (7/8) | — |
```

## CALIBRATE

### Calibration Rules

1. Require `3+ simulations` before changing framework effectiveness weights.
2. Cap any single adjustment at `±0.15`.
3. Apply `10%` decay per quarter back toward defaults.
4. User-stated framework preferences always override calibrated defaults.
5. If there are fewer than `3` validated predictions, record the result but do not change weights.

### Framework Effectiveness

Use effectiveness scores by context, then tune cautiously:

```yaml
swot_effectiveness:
  overall_assessment: 0.85
  startup_strategy: 0.80
  m_and_a: 0.75
pestle_effectiveness:
  market_entry: 0.90
  long_term_planning: 0.85
  crisis_response: 0.70
porter_effectiveness:
  industry_analysis: 0.90
  competitive_positioning: 0.85
  pricing_strategy: 0.75
bcg_effectiveness:
  portfolio_management: 0.90
  investment_allocation: 0.85
  product_strategy: 0.80
```

Example:

```yaml
bsc_effectiveness:
  startup_strategy: 0.65 -> 0.80
```

### Scenario Parameter Defaults

| Parameter | Default | Calibrated example | Use |
|---|---|---|---|
| Optimistic uplift | `+20~40%` | `+25~35%` | tighten if upside is consistently overestimated |
| Pessimistic downside | `-20~40%` | `-25~45%` | widen if downside is repeatedly underestimated |
| Short-term confidence | `±10%` | `±8%` | tighten when predictions are reliably close |
| Long-term confidence | `±30%` | `±35%` | widen when uncertainty is structurally high |

### Default Assumption Library (2026 refresh)

| Assumption | Default | Observed range | Reliability |
|---|---|---|---|
| Classical SaaS churn rate | `1-2%/mo` | `0.8-3.5%/mo` | Medium |
| AI-native SaaS churn rate (< $250/mo ACV) | `3-7%/mo` | `2-10%+/mo` | Low (high cohort variance, m3ter / SaaS Mag 2026) |
| SaaS gross margin (classical) | `70-80%` | `65-85%` | High |
| SaaS gross margin (AI-native) | `60-70%` | `50-75%` | Medium (SFAI Labs 2026 disclosure tracker; Bessemer Shooting Stars `~60%`) |
| Japan IT market growth | `3-5%/yr` | `2-7%/yr` | Medium |
| CAC Payback | `12-18mo` | `8-24mo` | Medium |
| LTV/CAC target | `3:1+` | `2.5:1-5:1` | High |
| Public SaaS Rule of 40 median (2026) | `28%` | `15-40%` | High (Aventis Advisors 2026, n=58) |
| Burn Multiple (early-stage) | `3.4x` | `1.5-5x` | High |
| Burn Multiple (AI-native at scale) | `0.8-1.2x` | `0.5-1.8x` | Medium (High Alpha 2026) |

## PROPAGATE

### Journal Format

Write reusable findings to `.agents/helm.md`:

```markdown
## YYYY-MM-DD - FORESIGHT: [Simulation Type]

**Simulations assessed**: N
**Overall accuracy**: X%
**Key insight**: [description]
**Calibration adjustment**: [framework/parameter: old -> new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Helm
date: YYYY-MM-DD
summary: [strategic insight]
affects: [Helm, Magi]
priority: MEDIUM
reusable: true
-->
```

### Pattern Library

| Context | Best framework chain | Notes |
|---|---|---|
| Annual strategy | `PESTLE -> SWOT -> Porter -> Ansoff` | Best with Tier `1+2` data |
| M&A evaluation | `Porter -> SWOT -> BCG -> Financial` | Best with Tier `1+2+3C` data |
| New market entry | `PESTLE -> Porter -> Ansoff -> Blue Ocean` | Market research quality is decisive |
| Crisis response | `SWOT -> ST-3` | Speed matters more than depth |
| KPI forecasting | `ST-1 / ST-2` | Tier `2A` data is critical |
| Long-term vision | `Blue Ocean -> PESTLE -> BSC` | Use wider scenario ranges |

### Quick FORESIGHT

Use this when evidence is too thin to recalibrate:

```markdown
## Quick FORESIGHT

**Simulations**: 1 completed
**Predictions**: 2 (too few to calibrate)
**Note**: PESTLE -> SWOT produced clear strategic direction
**Action**: No weight change (insufficient data)
```
