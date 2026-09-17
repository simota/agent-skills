# Technical Debt Scoring

Load for a debt inventory, repayment plan or ROI comparison. The SKILL core contract owns TDR thresholds, the ≥15% capacity rule above 5% TDR, Cost-of-Delay ordering, and `comprehension_debt`; do not substitute a vendor's survey or a fixed example sprint budget for those rules.

## Severity Matrix

| Impact | Low effort | Medium effort | High effort |
|--------|------------|---------------|-------------|
| High | P0: Fix now | P1: Next sprint | P2: Plan |
| Medium | P1: Next sprint | P2: Plan | P3: Backlog |
| Low | P2: Plan | P3: Backlog | P4: Accept |

## Item Scoring

`Priority = Impact × (6 - Cost)`, each scored 1–5. Support Impact with touchpoints, frequency of developer friction and related defects; support Cost with remediation effort, regression risk and prerequisite changes. Record production-incident risk (1–5) and the estimate's unit separately. Do not silently equate this ranking with TDR or the severity matrix.

Categories: Design, Code, Architecture, Test, Documentation, Infrastructure, Dependency. Use the affected quality/owner to choose; a security issue is not automatically medium merely because it is dependency debt.

## Inventory / Repayment Contract

Inventory: total/high-priority counts and estimated effort; each TD-ID's category, location, Impact, Cost, Priority, proposed fix, dependencies and owner. Include `comprehension_debt` HIGH/MEDIUM/LOW with actual AI-authorship/review-depth evidence; its remediation is documentation/ADR backfill/review, not automatically refactoring.

Repayment plan: protected capacity and accountable owner; measurable goals; staged work linked to TD-IDs and dependencies; milestones; before/after success metrics. Avoid a standalone rewrite or an unfunded “20% rule.” Validate outcomes with defects, tests, cycle time and business impact rather than optimizing a single tool score.

## ROI

- Monthly avoidable cost: defect-fix time + extra development time + onboarding overhead, each × the applicable rate.
- One-time fix cost: development + testing + review/deployment effort, each × rate.
- Break-even months: fix cost / monthly savings.
- 12-month ROI: `(monthly savings * 12 - fix cost) / fix cost * 100`.

Declare assumptions/ranges, currency and time window. If savings are non-positive, there is no positive break-even; if fix cost is zero, percentage ROI is undefined. Conclude Fix / Defer / Accept with the rationale. Industry-wide spending figures are not evidence of this repository's costs.
