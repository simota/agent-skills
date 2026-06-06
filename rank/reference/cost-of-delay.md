# Cost of Delay (CD3) Reference

Purpose: Quantitative economic prioritization that puts a currency value on time. Cost of Delay (CoD) is the rate at which value is lost per unit time — typically dollars-per-week — and CD3 (Cost of Delay Divided by Duration) sequences work to maximize value-throughput. Pioneered by Don Reinertsen (*Principles of Product Development Flow*, 2009) and adapted by SAFe as a Fibonacci-relative proxy. This recipe runs the deeper, four-component CoD analysis distinct from WSJF's rough-cut approximation.

## Scope Boundary

- **rank `cod`**: full CoD economic decomposition (four components) and CD3-based sequencing. Targets revenue-quantifiable or deadline-bound work where dollars-per-week is defensible.
- **rank `wsjf` (elsewhere)**: SAFe Fibonacci-scored CoD-proxy / Job Size — quick, relative, and team-friendly. Use WSJF when financial data is absent or unreliable.
- **rank `rice` (elsewhere)**: product-feature scoring with reach × impact × confidence ÷ effort — non-economic, no time dimension.
- **Magi (elsewhere)**: multi-perspective deliberation when CoD numbers exist but stakeholders contest *which* value lens dominates.
- **Helm (elsewhere)**: strategic CoD inputs (market windows, competitive timing) feed into this recipe; Rank does the per-item math.
- **Sherpa (elsewhere)**: decomposes the top-CD3 item into atomic steps after sequencing is decided here.

## Workflow

```
COLLECT     →  list candidate items with revenue, deadline, risk, and dependency context
            →  flag items missing financial signal — they may belong in WSJF instead

DECOMPOSE   →  for each item, score the four CoD components:
              user-business value, time criticality, risk reduction, opportunity enablement
            →  sum to weekly CoD ($/week) using monetized or Fibonacci-relative scale

DURATION    →  estimate Job Duration (calendar weeks until value is realized — not effort hours)
            →  capture parallelism, dependencies, and queue time

CD3         →  compute CD3 = CoD / Duration for each item
            →  rank descending; highest CD3 sequences first

CALIBRATE   →  apply CoD-curve patterns (urgent, fixed-deadline, expedite, intangible)
            →  pairwise-compare top-N items; sensitivity-test ±30% on weakest component

PRESENT     →  CD3-ordered queue with per-item CoD breakdown, $/week, duration, confidence
            →  hand off to Sherpa (decompose top item) or Helm (strategic confirmation)
```

## Four CoD Components (Reinertsen / SAFe)

| Component | Question | Quantification approach |
|-----------|----------|-------------------------|
| User-Business Value | What revenue / cost-saving / customer value is at stake? | Direct $/week from forecast, churn modeling, or willingness-to-pay |
| Time Criticality | Does the value decay if delayed? Is there a hard deadline? | CoD curve type (urgent / fixed-date / standard) determines decay rate |
| Risk Reduction & Opportunity Enablement (RR&OE) | Does this de-risk future work or unlock new options? | Real-options pricing, or Fibonacci proxy (1/2/3/5/8/13) |

Sum the three monetized streams (or Fibonacci totals) to get weekly CoD. RR&OE is often under-counted — explicitly probe for it.

## CoD Curve Patterns (Reinertsen)

| Pattern | Shape | Sequencing implication |
|---------|-------|------------------------|
| Standard (linear) | Constant $/week loss | CD3 ranks normally |
| Urgent (front-loaded) | Steep early loss, then flat | Expedite class — preempts standard items |
| Fixed-Deadline | No loss until deadline, then cliff | Schedule backwards from deadline; not a CD3 sort |
| Intangible | Low and flat — until it isn't | Re-evaluate quarterly; default to lowest CD3 |

Identify the curve before computing CoD — applying linear math to a fixed-deadline item over-prioritizes it early and under-prioritizes it near the cliff.

## Quantification Approaches (in order of rigor)

1. **Direct monetization** — revenue model, churn delta, support-cost reduction. Highest defensibility; requires data partnership.
2. **Anchored estimation** — pick one well-understood item as the $10k/week anchor, score others relative to it.
3. **Fibonacci CoD** — score each component 1-13, sum (range 3-39). Same math as WSJF; use when monetization is impossible. Distinguish from WSJF only by deeper component decomposition and explicit curve typing.
4. **Order-of-magnitude buckets** — `<$1k/wk`, `$1k-10k/wk`, `$10k-100k/wk`, `>$100k/wk`. Coarse but auditable.

## CD3 vs WSJF — When to Use Which

| Aspect | CD3 (this recipe) | WSJF |
|--------|-------------------|------|
| CoD basis | Monetized $/week, four components | Fibonacci sum of three components |
| Job size | Calendar Duration (weeks) | Relative Job Size (Fibonacci) |
| Best for | Revenue-clear, deadline-bound, exec-visible work | Team backlog grooming under uncertainty |
| Defensibility | High — auditable financials | Medium — relative team agreement |
| Effort to produce | Hours per item | Minutes per item |

Rule of thumb: WSJF for the backlog floor; CD3 for the top quartile and any item over $50k/week of expected CoD.

## Anti-Patterns

- Reporting CoD without a curve type — applying linear math to fixed-deadline work mis-sequences the cliff.
- Skipping RR&OE because it's hard to monetize — under-counted opportunity enablement systematically demotes platform and infra work.
- Confusing Duration with Effort — CD3 wants calendar weeks to value-realization, not engineer-weeks. Queue time and dependencies belong in Duration.
- Mixing monetized CoD and Fibonacci CoD in the same ranking — the units don't compose; pick one scale per ranking.
- Treating CD3 output as immutable — CoD curves shift as deadlines approach; re-rank monthly for active queues.
- Letting HiPPO override CD3 without challenge — if a leader expedites a low-CD3 item, log it as an "executive override" and track the cumulative CoD cost.
- Claiming CD3 when actually running WSJF — the recipes overlap but differ; mis-naming erodes trust with finance and exec stakeholders.
- Single-point CoD estimates with no sensitivity range — show ±30% bands on each component or rankings look spuriously precise.
- Ignoring opportunity cost of *not* doing other work — CD3 sequencing assumes the queue is fixed; revisit when scope changes.

## Handoff

- **To Sherpa**: highest-CD3 item with CoD breakdown, duration estimate, and dependency notes — Sherpa decomposes into atomic steps.
- **To Magi**: items where stakeholders contest the value-component weights or curve type — multi-perspective deliberation resolves the dominant lens.
- **To Spark**: opportunity-enablement-heavy items that need feature ideation before they can be sequenced.
- **To Helm**: aggregated CD3 queue feeds strategic roadmap; flag items where CoD exceeds organizational capacity for expedite-class work.
- **To Scribe**: CoD methodology, curve assumptions, and per-item rationale documented for finance and audit traceability.

## Discovery Upstream: Opportunity Solution Tree Integration

When CoD items originate from continuous discovery (Teresa Torres's Opportunity Solution Tree methodology), the opportunity node in the OST typically maps to User-Business Value and RR&OE components. In 2025–2026, AI-powered OST tooling (e.g., Vistaly AI integration) can synthesize interview data into opportunity nodes automatically — use the resulting opportunity cluster as the input set for CoD decomposition rather than HiPPO-driven feature lists. [Source: Product Talk — From Customer Interviews to an Opportunity Solution Tree https://www.producttalk.org/ai-opportunity-solution-trees/]
