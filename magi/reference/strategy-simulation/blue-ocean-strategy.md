# Blue Ocean Strategy Reference

Purpose: Apply Kim & Mauborgne's Blue Ocean Strategy to find uncontested market space. Produces a Value Curve (Strategy Canvas), applies the Four Actions / ERRC grid, maps buyer utility, and identifies the three tiers of non-customers.

## Scope Boundary

- **helm `blue-ocean`**: Kim & Mauborgne Blue Ocean framework (this document).
- **helm `porter` (elsewhere)**: Red ocean competitive analysis. Blue Ocean *reframes* the market; Porter *analyzes* the market as given.
- **helm `jtbd` (elsewhere)**: Jobs-to-be-done reframing. JTBD asks "what job"; Blue Ocean asks "what factors of competition can we redefine".
- **Compete (elsewhere)**: Competitor feature matrices — input to the as-is Value Curve.
- **Spark (elsewhere)**: Concrete feature proposals from the to-be value curve.

## Core Concepts

### Red Ocean vs Blue Ocean

| Red Ocean | Blue Ocean |
|-----------|------------|
| Compete in existing market | Create uncontested space |
| Beat the competition | Make competition irrelevant |
| Exploit existing demand | Create and capture new demand |
| Make value-cost trade-off | Break the value-cost trade-off (differentiation AND low cost) |
| Align activities with strategic choice of differentiation OR low cost | Align activities to pursue both |

## Strategy Canvas (Value Curve)

Visualize how an industry competes across key factors.

```
High  ┤                        ╱╲
      │                       ╱  ╲
      │                      ╱    ╲
      │                ______     ╲___
Level │          _____╱          /    ╲___
of    │    _____╱              _╱         ╲
offer │ __╱                    │
      │                        │
Low   ┼────┬─────┬─────┬─────┬─┬──────┬──
           F1    F2    F3    F4  F5    F6

  Factors of competition →
```

Plot each competitor and your offering. Identify where everyone overlaps (commoditized) and where the shape differs (differentiation).

## Four Actions / ERRC Grid

To create a new value curve, ask four questions:

```
┌───────────────────────────────┬───────────────────────────────┐
│ ELIMINATE                     │ RAISE                         │
│ Which factors that the industry│ Which factors should be raised │
│ takes for granted should be   │ well above the industry       │
│ eliminated?                   │ standard?                     │
├───────────────────────────────┼───────────────────────────────┤
│ REDUCE                        │ CREATE                        │
│ Which factors should be       │ Which factors should be       │
│ reduced well below the        │ created that the industry     │
│ industry standard?            │ has never offered?            │
└───────────────────────────────┴───────────────────────────────┘
```

The goal: a differentiated value curve that achieves **both** differentiation AND low cost (eliminate + reduce save cost; raise + create deliver differentiation).

### Classic examples

| Company | Eliminate | Reduce | Raise | Create |
|---------|-----------|--------|-------|--------|
| Cirque du Soleil | Animals, star performers, multi-show arenas | Humor, thrill | Unique venue, artistic music | Theme, refined environment, multiple productions |
| Southwest Airlines | Meals, seat class, hub-and-spoke | Lounge, seating choice | Friendly service, speed | Frequent point-to-point |
| [yellow tail] wine | Enological terminology, aging quality, vineyard prestige | Wine complexity, wine range, above-the-line marketing | Price vs premium wines | Easy drinking, easy to select, fun and adventure |

## Three Tiers of Non-Customers

Expand market by targeting not current customers but non-customers.

| Tier | Who | Approach |
|------|-----|----------|
| 1st: "Soon-to-be" | Use your industry minimally, looking to jump ship | Resolve their dissatisfaction |
| 2nd: "Refusing" | Consciously reject your industry's offering | Offer alternative that reframes |
| 3rd: "Unexplored" | Never considered themselves as potential customers | Deliver value they didn't know they wanted |

Target the tier with the largest untapped demand. Often tier 3 is the biggest — Cirque du Soleil went after adults who thought circuses were for children.

## Buyer Utility Map

For each stage of the buyer experience, ask whether you add utility across six levers:

```
Buyer Productivity  ┼────────────────────────────────
Simplicity          ┼────────────────────────────────
Convenience         ┼────────────────────────────────
Risk Reduction      ┼────────────────────────────────
Fun / Image         ┼────────────────────────────────
Environmental       ┼────────────────────────────────
Friendliness        ┼────────────────────────────────

                    Purchase → Delivery → Use → Supplements → Maintenance → Disposal
```

The "blocked utility" in existing industry = where Blue Ocean opportunity lives.

## Workflow

```
MAP-AS-IS   →  build current industry strategy canvas (use Compete data)
            →  plot key competitors on key factors

IDENTIFY    →  identify commoditized zones (where curves overlap)
            →  identify the industry's taken-for-granted factors

ERRC        →  apply 4 actions: eliminate / reduce / raise / create

NON-CUSTOMER→  identify 3 tiers of non-customers
            →  pick the tier with biggest untapped demand

UTILITY     →  run buyer utility map across 6 × 6 cells
            →  find blocked utility

DRAW-TO-BE  →  draft the new value curve
            →  verify: divergence + focus + compelling tagline

VALIDATE    →  market/economics viability (sufficient size, viable cost)
            →  hand off to Magi for Go/No-Go
```

## Three Qualities of a Good To-Be Curve

| Quality | Check |
|---------|-------|
| Focus | Emphasizes a few factors, not every factor |
| Divergence | Different shape from competitor curves |
| Compelling tagline | Can you say it in one sentence to a customer? |

Without all three, the strategy is muddy and execution will drift.

## Output Template

```markdown
## Blue Ocean Analysis: [Industry / Offering]

### As-Is Strategy Canvas
- **Key factors of competition**: [list]
- **Competitors plotted**: [list, using Compete output]
- **Commoditized zones**: [factors where everyone is high]
- **Industry-taken-for-granted**: [factors nobody questions]

### ERRC Grid
| Eliminate | Reduce |
|-----------|--------|
| [...] | [...] |
| **Raise** | **Create** |
| [...] | [...] |

### Non-Customer Focus
- **Tier targeted**: [1st / 2nd / 3rd]
- **Rationale**: [untapped demand estimate]
- **Entry path**: [how to reach them]

### Buyer Utility Map (check-cells where blocked utility exists)
| | Purchase | Delivery | Use | Supplements | Maintenance | Disposal |
|--|----------|----------|-----|-------------|-------------|----------|
| Productivity | | | ✓ | | | |
| Simplicity | ✓ | | | | | |
| ... | | | | | | |

### To-Be Value Curve
- **New competitive factors**: [list]
- **Shape description**: [one paragraph]
- **Focus check**: ✓ / ✗
- **Divergence check**: ✓ / ✗
- **Compelling tagline**: "[one sentence]"

### Viability
- **Market size estimate**: [tier × conversion]
- **Price corridor**: [affordable for target non-customer]
- **Cost target**: [achievable via eliminate + reduce savings]
- **Adoption hurdles**: [list + mitigation]

### Handoffs
- Spark: concrete feature proposals for Create + Raise
- Compete: competitor re-analysis under new frame
- Pulse: KPI re-definition for new metrics of success
- Magi: Go/No-Go on strategic pivot
- Scribe: strategy document
- Saga: customer-story with the new tagline
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| "Blue ocean" as buzzword without Value Curve | Always build the Strategy Canvas with real data |
| Only Create, no Eliminate | Cost side matters; without eliminate/reduce, no economic viability |
| Targeting all 3 tiers of non-customers | Pick one with largest untapped demand |
| No tagline | If you can't say it in one sentence, strategy is muddy |
| Mimicking a known Blue Ocean | Once executed and copied, blue becomes red — find your own |
| Ignoring adoption hurdles | Price, learning cost, legal, channel conflicts — plan for each |

## Deliverable Contract

When `blue-ocean` completes, emit:

- **As-is Strategy Canvas** with industry factors and competitor plots.
- **ERRC grid** filled with specific actions.
- **Non-customer tier** chosen with rationale.
- **Buyer Utility Map** with blocked-utility cells highlighted.
- **To-be Value Curve** passing focus + divergence + tagline tests.
- **Viability check** (market size, price corridor, cost target, adoption hurdles).
- **Handoffs**: Spark, Compete, Pulse, Magi, Scribe, Saga.

## References

- W. Chan Kim & Renée Mauborgne — *Blue Ocean Strategy* (2005)
- *Blue Ocean Shift* (Kim & Mauborgne, 2017 follow-up — process-oriented sequel)
- INSEAD Blue Ocean Strategy Institute — case studies and tools
- HBR — "Blue Ocean Strategy" (2004) — original article
- Strategy Canvas templates — Kim/Mauborgne website

## Canonical Example Status (2026)

- **Cirque du Soleil** — still the canonical textbook case ([blueoceanstrategy.com teaching materials](https://www.blueoceanstrategy.com/teaching-materials/cirque-du-soleil/)). 2020-06 Chapter 15 filing followed by 2020-11 sale to Catalyst Capital Group-led creditor consortium; by 2023 revenue returned to the pre-COVID `~$1B` mark ([Fortune 2024-04-24](https://fortune.com/2024/04/24/cirque-du-soleil-bankruptcy-growth-covid/)). The recovery is itself a Blue Ocean re-application: scaled-down touring model targeting the original adult-non-circus-goer non-customer tier. Use as cautionary tail: a successful Blue Ocean strategy does **not** immunize against operating-leverage shocks (COVID closure).
- **Southwest Airlines** and **[yellow tail] wine** — still valid as introductory ERRC cases but increasingly "red" in 2026; cite them as *historical illustrations*, not *current* Blue Oceans.
- **AI-era Blue Ocean candidates** to use when you need a 2025-2026 example: Notion AI's "second brain" reframing of the productivity factors, Perplexity's reframing of "search" into "answers with citations", Cursor's reframing of "IDE" into "agent-collaborator." Validate ERRC for each before quoting.
