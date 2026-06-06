# Strategic Frameworks Reference — Helm

Purpose: Select the right strategic framework, apply it consistently, and produce decision-ready outputs without mixing incompatible lenses.

## Contents

- Framework selection rules
- Framework-specific execution notes
- Combination patterns

## Framework Selection Rules

| Goal | Primary framework | Add-on frameworks | Use when |
|------|-------------------|------------------|----------|
| overall business diagnosis | `SWOT` | `PESTLE`, `Porter` | you need internal and external summary in one pass |
| external environment scan | `PESTLE` | `SWOT` | the question is market, regulation, macro, or technology shift |
| industry attractiveness | `Porter 5 Forces` | `PESTLE` | pricing power, entry barriers, substitutes, or supplier leverage drive the decision |
| portfolio allocation | `BCG Matrix` | financial model | you need invest/hold/exit prioritization across products |
| execution management | `BSC` | monitoring | you need KPI cascade and strategy tracking |
| growth direction | `Ansoff Matrix` | `SWOT`, `Porter` | you need penetration, market expansion, product expansion, or diversification |
| advantage source | `Value Chain` | `SWOT` | you need process-level cost or differentiation insight |
| category creation | `Blue Ocean` | `PESTLE`, `BSC` | the goal is value innovation rather than head-on competition |

## Decision Tree

```text
Overall assessment -> SWOT
External scan -> PESTLE
Industry structure -> Porter 5 Forces
Portfolio allocation -> BCG Matrix
Execution management -> Balanced Scorecard
Growth direction -> Ansoff Matrix
Competitive advantage source -> Value Chain
Category creation -> Blue Ocean Strategy
```

## Framework Notes

### SWOT

Use `Strengths / Weaknesses / Opportunities / Threats` and always finish with `SO / WO / ST / WT` action paths.

Output requirements:
- evidence for each factor
- one prioritized strategy
- explicit tradeoff if strengths and threats conflict

### PESTLE

Cover `Political / Economic / Social / Technological / Legal / Environmental`.

Output requirements:
- top trend per dimension
- business impact
- time horizon
- positive/negative direction
- note cross-effects such as technology creating legal change

**2026 priority signals (always evaluate):**
- Political: US tariff escalation (tariffs increased >6x in 12 months), AI export controls, US-China tech bifurcation (BCG: https://www.bcg.com/publications/2025/geopolitical-forces-shaping-business-in-2026); geoeconomic confrontation is WEF #1 near-term global risk (WEF GRR 2026: https://www.weforum.org/publications/global-risks-report-2026/)
- Environmental: IFRS S2 climate-risk disclosure effective 1 Jan 2024, adopted in 21+ jurisdictions — LONG-horizon strategies for listed/institutional clients must address transition-plan requirements (https://www.ifrs.org/issued-standards/ifrs-sustainability-standards-vector/ifrs-s2-climate-related-disclosures/)
- Technological: AI capabilities as geopolitical asset; agentic AI shifting from task automation to multi-step workflow management (BCG AI Radar 2026)

### Porter 5 Forces

Score each force `High = 3`, `Medium = 2`, `Low = 1`. Lower total = more attractive structure.

Required forces:
- rivalry
- threat of entry
- threat of substitutes
- buyer power
- supplier power

Output requirements:
- score table
- top structural risk
- top structural advantage

> **Limitation (2025-2026):** Porter 5 Forces is a static, industry-level snapshot. It does not assess internal capabilities, execution quality, or platform-ecosystem dynamics (e.g., network effects, AI model moats). Supplement with Wardley Mapping for technology-evolution positioning and Scenario Planning for dynamic market shifts. Source: https://www.platformexecutive.com/knowledge/business-models/competitive-intelligence/choosing-the-right-framework-when-to-use-swot-pestle-porters-five-forces-and-5c-analysis/

### BCG Matrix

| Quadrant | Meaning | Default action |
|----------|---------|----------------|
| `Star` | high growth, high share | invest and defend |
| `Cash Cow` | low growth, high share | harvest and fund other bets |
| `Question Mark` | high growth, low share | selective investment or exit |
| `Dog` | low growth, low share | improve, divest, or shut down |

### Balanced Scorecard

Keep the 4 perspectives explicit:
- Financial
- Customer
- Internal process
- Learning and growth

Strategy map order:
`Learning and growth -> Process -> Customer -> Financial`

### Ansoff Matrix

| Product / Market | Existing market | New market |
|------------------|-----------------|------------|
| Existing product | Market penetration | Market development |
| New product | Product development | Diversification |

Use `low / medium / high` risk framing. Always explain why diversification is justified if chosen.

### Value Chain

Trace advantage across:
- inbound logistics
- operations or development
- outbound logistics
- marketing and sales
- service
- support activities

Use it when the strategy depends on operational advantage, not just market choice.

### Blue Ocean

Use the `ERRC` lens:
- Eliminate
- Reduce
- Raise
- Create

Require a strategy canvas if the output claims category differentiation.

## Combination Patterns

| Objective | Recommended sequence | Reason |
|-----------|----------------------|--------|
| comprehensive strategy | `PESTLE -> SWOT -> Porter -> Ansoff` | external context, internal fit, industry structure, then growth path |
| M&A evaluation | `Porter -> SWOT -> BCG -> Financial model` | structure, fit, portfolio effect, then valuation |
| new market entry | `PESTLE -> Porter -> Ansoff -> Blue Ocean` | environment, structural friction, entry mode, then differentiation |
| business improvement | `BSC -> Value Chain -> SWOT` | performance baseline, process levers, strategic synthesis |
| long-term vision | `Blue Ocean -> PESTLE -> BSC` | future position first, constraints second, execution third |
