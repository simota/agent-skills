# Market Sizing Delta

Purpose: Evidence and uncertainty contract for Compete market sizing. TAM/SAM/SOM definitions and arithmetic are model-known.

## Required Evidence

- Date every source and distinguish public filings, analyst estimates, surveys, and inferred values.
- State units explicitly: revenue, ARR, spend, customers, seats, transactions, or GMV.
- Separate current market facts from forecasts and Compete inference.
- Record every geography, segment, product-fit, adoption, price, win-rate, and capacity assumption.
- Treat private-company revenue and market share as estimates with confidence bands, never facts.

## Cross-Verification Gate

Use at least two independent methods when the output drives strategy:

```text
top_down  = sourced market × serviceable filters
bottom_up = reachable customers × adoption × annual value
```

If the central estimates differ by more than `3x`, do not average them. Isolate the conflicting assumptions and report a range until resolved. Never derive SOM as an arbitrary percentage of TAM; ground it in distribution capacity, pipeline, win rate, or comparable penetration.

## Required Output

| Field | Content |
|---|---|
| Scope | category, geography, segment, metric, base year |
| TAM / SAM / SOM | low / base / high, not false precision |
| Methods | top-down and bottom-up calculations |
| Assumptions | value, source or rationale, sensitivity |
| Divergence | conflicting inputs and resolution status |
| Confidence | high / medium / low per estimate |
| Adjacencies | customer, workflow, technology, data, or bundle connection |

For adjacent markets, name the shared buyer or workflow, expansion enabler, barrier, and plausible time horizon. Hand strategic simulation to Magi with sources and unresolved assumptions intact.

## Reject

- Global-market figures presented as serviceable revenue.
- GMV confused with vendor revenue.
- CAGR projected beyond the source horizon without a scenario range.
- Substitutes omitted from the category boundary.
- Unsourced employee-count or funding-stage heuristics presented as observed revenue.
