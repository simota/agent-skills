# Simulation Patterns Reference — Helm

Purpose: Apply horizon-specific simulation models without mixing cadence, assumptions, or output grain.

## Contents

- Core simulation rules
- Short-term patterns
- Mid-term patterns
- Long-term patterns
- Quality checklist

## Core Rules

- Always disclose assumptions.
- Always generate `Baseline / Optimistic / Pessimistic`.
- Always include sensitivity analysis on major drivers.
- Keep cadences separate:
  - `SHORT = monthly or quarterly`
  - `MID = annual`
  - `LONG = 3/5/10-year directional blocks`

## SHORT-TERM SIMULATION (`0-1 Year`)

### Pattern `ST-1`: Monthly KPI Forecast

Use for MRR, ARR, customer-count, and churn-driven growth tracking.

Formula:

```text
MRR_next = MRR_current × (1 + growth_rate) - churned_MRR + new_MRR + expansion_MRR
growth_rate = (new_customers × ARPU + expansion_revenue) / MRR_current - churn_rate
```

Required inputs:
- current MRR
- new customers per month
- ARPU
- churn rate
- expansion rate
- CAC

Default scenario shift:
- `Optimistic = +30%`
- `Pessimistic = -25%`

### Pattern `ST-2`: Cash Flow and Runway

Use for runway, burn, and fundraising timing.

Formula:

```text
Monthly Burn = Fixed Costs + Variable Costs - Revenue
Runway = Cash Position / Monthly Burn
Break-even = Fixed Costs / Gross Margin
```

Required inputs:
- cash balance
- fixed costs
- variable costs
- revenue
- gross margin

### Pattern `ST-3`: Crisis Response

Use when a discrete shock changes assumptions fast.

| Shock | Immediate response (`0-30 days`) | Medium response (`30-90 days`) |
|------|----------------------------------|--------------------------------|
| top customer churns (`>20%` of revenue) | replace pipeline, cut spend | diversify concentration risk |
| major competitor enters | sharpen differentiation, lock in customers | invest in product separation |
| recession signal | protect retention, compress CAC | rework cost base |
| key employee leaves | retention action, temporary coverage | hiring and knowledge transfer |
| security incident | incident response and customer communication | trust recovery and prevention |

### Pattern `ST-4`: Budget vs Actual

Use for monthly operating review and forecast correction.

Track:
- budget
- actual
- variance
- variance %
- cause
- recommended correction

## MID-TERM SIMULATION (`1-3 Years`)

### Pattern `MT-1`: Market Expansion

Use Ansoff-based strategy comparison:
- market penetration
- market development
- product development
- diversification

Minimum outputs:
- initial investment
- 3-year revenue uplift
- ROI
- risk
- recommendation

### Pattern `MT-2`: Portfolio Plan

Use BCG-based resource allocation.

Track:
- current quadrant
- 1-year expected quadrant
- 3-year expected quadrant
- investment policy

### Pattern `MT-3`: Organization and Hiring Roadmap

Track:
- hiring by function
- personnel cost
- personnel cost ratio
- purpose of each hiring wave

### Pattern `MT-4`: P&L Forecast

Required parameters:
- revenue growth by scenario
- gross margin movement
- fixed-cost growth
- variable-cost ratio

Minimum outputs:
- revenue
- gross profit and margin
- SG&A
- R&D
- operating income and margin
- EBITDA

## LONG-TERM SIMULATION (`3-10 Years`)

### Pattern `LT-1`: Industry Transformation

Use for 5-10 year structure shifts.

Required outputs:
- three named scenarios
- explicit probabilities
- industry impact
- company opportunities and threats
- strategy valid across all scenarios

### Pattern `LT-2`: M&A Scenario

Track:
- target
- valuation
- strategic rationale
- integration difficulty
- ROI / payback
- major risk

### Pattern `LT-3`: Exit Strategy

Required inputs:
- current valuation method
- current value
- target exit timeline

Compare:
- IPO
- Strategic M&A
- PE
- continue independently

### Pattern `LT-4`: Long-Range Financial Model

This is directional, not precision forecasting.

Required inputs:
- TAM and growth
- attainable share
- business model durability
- external shocks

Required outputs:
- current vs `3 / 5 / 10` year metrics
- optimistic downside and disruption case
- disclaimer that long-term numbers confirm direction, not exact results

## Quality Checklist

- assumptions explicitly listed
- 3 scenarios generated
- sensitivity analysis at `±20%`
- time grain matches horizon
- benchmark comparison included when relevant
- roadmap is decomposable by Sherpa
- risk matrix included
- long-term output carries directional-not-precise disclaimer
