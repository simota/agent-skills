# Business Model Canvas & Lean Canvas

Purpose: lay out a whole business model on one page to stress-test its coherence before
committing strategy or capital. Two related one-pagers live here:
- **Business Model Canvas (BMC)** — Osterwalder/Strategyzer, 9 blocks, for established or
  multi-stakeholder businesses.
- **Lean Canvas** — Ash Maurya's startup adaptation of the BMC, 9 blocks, optimized for
  early-stage problem/risk discovery.

Use these for business-model design, pivot evaluation, or as the zoom-out companion when
`spark`'s Value Proposition Canvas has settled customer-fit but the *whole-business* fit
is unproven.

> **Not the same as the Strategy Canvas.** The Blue Ocean "Strategy Canvas / Value Curve"
> in `blue-ocean-strategy.md` plots competition factors to find uncontested space — a
> *competitive positioning* tool. The BMC/Lean Canvas describe *how one business creates,
> delivers, and captures value*. Keep them distinct.

## Contents
- Business Model Canvas (9 blocks)
- Lean Canvas (9 blocks)
- BMC vs Lean Canvas — which to use
- Stress-testing & handoffs

## Business Model Canvas — 9 Blocks

| # | Block | Question |
|---|-------|----------|
| 1 | `Customer Segments` | Who are we creating value for? Who are the most important customers? |
| 2 | `Value Propositions` | What value do we deliver? Which problem/job do we solve? (zoom-in → VPC) |
| 3 | `Channels` | How do segments want to be reached and served? |
| 4 | `Customer Relationships` | What relationship does each segment expect (self-serve, dedicated, community)? |
| 5 | `Revenue Streams` | For what value are customers willing to pay? Pricing mechanism? |
| 6 | `Key Resources` | What assets does the value proposition require (physical, IP, human, financial)? |
| 7 | `Key Activities` | What must we do well to deliver (production, platform, problem-solving)? |
| 8 | `Key Partnerships` | Who are our key suppliers/partners? What do we source vs build? |
| 9 | `Cost Structure` | What are the dominant costs? Cost-driven vs value-driven? |

Fill order: right side first (1→5, the value/market side), then left side (6→9, the
infrastructure/cost side). The two sides must balance — Revenue Streams (5) must
plausibly exceed Cost Structure (9) given the chosen resources/activities/partners.

## Lean Canvas — 9 Blocks

Replaces four BMC infrastructure blocks with startup-risk blocks. Built for *finding what
will kill the business first*.

| # | Block | Question | (BMC block it replaces) |
|---|-------|----------|--------------------------|
| 1 | `Problem` | Top 1-3 problems + existing alternatives | (Key Partnerships) |
| 2 | `Customer Segments` | Target customers + early adopters | (=) |
| 3 | `Unique Value Proposition` | Single clear compelling message + high-level concept | (=) |
| 4 | `Solution` | Top 1-3 features that address the problems | (Key Activities) |
| 5 | `Channels` | Path to customers | (=) |
| 6 | `Revenue Streams` | Revenue model, pricing | (=) |
| 7 | `Cost Structure` | Customer acquisition, distribution, hosting, people | (=) |
| 8 | `Key Metrics` | The few numbers that tell you how the business is doing | (Key Resources) |
| 9 | `Unfair Advantage` | What can't be easily copied or bought | (Customer Relationships) |

Fill order: `Problem` + `Customer Segments` first (they anchor everything), then UVP,
then the rest. `Unfair Advantage` is usually filled last and is often empty early — an
honest blank is more useful than a fabricated moat (route moat analysis to `compete`).

## BMC vs Lean Canvas — Which to Use

| Use BMC when… | Use Lean Canvas when… |
|---------------|------------------------|
| business/model exists; refining or pivoting | brand-new idea, high uncertainty |
| multiple stakeholders / partners / resources matter | speed and risk-spotting matter most |
| infrastructure & partnerships are strategic | problem and unfair advantage are the open questions |
| communicating a model to investors/teams | a founder iterating weekly |

For an early-stage startup blueprint, Lean Canvas pairs with `nexus package domain=startup`
(venture preset). For a corporate strategy review, BMC pairs with `helm scenario`/`swot`.

## Stress-Testing & Handoffs
- **Coherence test:** trace one customer segment through value prop → channel →
  relationship → revenue, and confirm the left-side blocks (resources/activities/partners/
  cost) actually support it. Broken traces are the model's real risk.
- **Scenario stress:** run the model through `simulation-patterns.md` (Baseline/Optimistic/
  Pessimistic) — especially Revenue Streams vs Cost Structure sensitivity.
- **Handoffs:** value-proposition zoom-in → `spark` `value-proposition-canvas.md`;
  moat/unfair-advantage validation → `compete` (`moat-7-powers.md`); KPI/Key Metrics
  instrumentation → `pulse`; financial modeling of Revenue/Cost → `helm forecast`
  (`financial-modeling-pitfalls.md`).
