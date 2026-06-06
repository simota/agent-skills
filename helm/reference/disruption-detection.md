# Disruption Detection Reference — Helm

Purpose: Use this file when Helm must evaluate disruption risk, position a business on the industry lifecycle, or assess technology adoption trajectories.

## Contents

- Christensen disruption theory
- Industry lifecycle stages
- S-curve and technology adoption
- Disruption risk scoring
- Detection signals
- Strategic response patterns
- Templates

## Christensen Disruption Theory

### Core Model

Disruptive innovation enters from below: initially inferior on mainstream metrics but superior on a different value dimension (price, simplicity, accessibility). It improves over time until it satisfies mainstream needs — at which point incumbents lose.

### Two Types of Disruption

| Type | Entry point | Mechanism | Example |
|---|---|---|---|
| **Low-end disruption** | Overserved customers at bottom of market | Simpler, cheaper product that is "good enough" | Budget airlines, mini steel mills |
| **New-market disruption** | Non-consumers who couldn't afford/access existing solutions | Creates entirely new market | Personal computers, mobile banking |

### Disruption Vulnerability Assessment

```markdown
## Disruption Vulnerability: [Business/Product]

### Overshoot Analysis
- Are we improving faster than customers need? [Yes/No]
- Evidence of feature fatigue in customer feedback? [Yes/No]
- % of features used by average customer: [estimate]
- Price sensitivity increasing in bottom segment? [Yes/No]

### Low-End Threat Scan
| Potential disruptor | What they offer | Where they're inferior | Where they're superior | Trajectory |
|---|---|---|---|---|
| [Company A] | [product] | [our advantage] | [their advantage] | ↑ improving / → stable / ↓ fading |

### New-Market Threat Scan
| Potential disruptor | Non-consumer segment served | Value proposition | Could it migrate to our market? |
|---|---|---|---|
| [Company A] | [segment] | [proposition] | [Yes — timeline / No — why] |

### Vulnerability Score
| Factor | Score (1-5) | Weight |
|---|---|---|
| Overshoot risk | | 25% |
| Low-end threat presence | | 25% |
| New-market threat presence | | 20% |
| Business model rigidity | | 15% |
| Organizational inertia | | 15% |
| **Disruption vulnerability** | | **[X/5]** |

Interpretation:
- ≥ 4.0: HIGH — active disruption defense required
- 3.0-3.9: MODERATE — monitor and prepare contingencies
- 2.0-2.9: LOW — maintain awareness
- < 2.0: MINIMAL — focus on execution
```

## Industry Lifecycle Stages

### Stage Definitions

| Stage | Growth rate | Competition | Profit | Strategy focus |
|---|---|---|---|---|
| **Embryonic** | Uncertain, high variance | Few players, undefined market | Negative (investment) | Product-market fit, education |
| **Growth** | `> 15%` CAGR | Increasing entrants, land-grab | Improving but reinvested | Market capture, scaling |
| **Shakeout** | Decelerating (`5-15%`) | Consolidation begins, weaker players exit | Pressured | Efficiency, positioning |
| **Maturity** | `< 5%`, stable | Oligopoly, stable shares | Stable, optimized | Defend share, operational excellence |
| **Decline** | Negative | Exits accelerating | Declining unless niche | Harvest, exit, or reinvent |

### Stage Identification Protocol

```markdown
## Industry Lifecycle Position: [Industry/Category]

### Evidence Assessment
| Indicator | Current state | Points to stage |
|---|---|---|
| Market growth rate | [X]% | [stage] |
| Number of active competitors | [trend] | [stage] |
| Customer acquisition cost trend | [rising/stable/falling] | [stage] |
| Product differentiation | [high/moderate/commoditizing] | [stage] |
| M&A activity | [low/moderate/high] | [stage] |
| Regulatory attention | [low/moderate/high] | [stage] |
| Venture funding pace | [accelerating/stable/declining] | [stage] |

### Lifecycle Position: [STAGE]
### Confidence: [H/M/L]

### Strategic Implications
- At this stage, winning strategies typically involve: [...]
- Losing strategies at this stage include: [...]
- Expected transition to next stage: [timeline estimate]
```

## S-Curve and Technology Adoption

### S-Curve Model

```text
Performance
    │         ╭────── Maturity (diminishing returns)
    │        ╱
    │      ╱    ← Rapid improvement phase
    │    ╱
    │  ╱
    │╱──────── Introduction (slow initial progress)
    └────────────────── Time
```

### Technology Adoption Lifecycle (Rogers)

| Segment | % of market | Characteristics | Crossing the chasm |
|---|---|---|---|
| Innovators | `2.5%` | Risk-tolerant, tech enthusiasts | — |
| Early Adopters | `13.5%` | Visionaries, strategic buyers | — |
| **CHASM** | — | Gap between visionaries and pragmatists | Critical transition |
| Early Majority | `34%` | Pragmatists, need proven solutions | — |
| Late Majority | `34%` | Conservatives, need simplicity | — |
| Laggards | `16%` | Skeptics, adopt only when necessary | — |

### Adoption Stage Assessment

```markdown
## Technology Adoption Assessment: [Technology/Product Category]

### Current Adoption Stage
- Estimated adopter segment: [Innovators / Early Adopters / Early Majority / Late Majority / Laggards]
- Evidence: [adoption metrics, market penetration data]
- Chasm status: [pre-chasm / crossing / post-chasm]

### S-Curve Position
- Current phase: [Introduction / Rapid improvement / Maturity / Decline]
- Performance trajectory: [accelerating / linear / decelerating / flat]
- Emerging S-curve (replacement technology): [identified / not yet / unknown]

### Strategic Implications
| If at this stage... | Then prioritize... |
|---|---|
| Pre-chasm | Product-market fit, reference customers, use cases |
| Crossing chasm | Whole product, pragmatist messaging, vertical focus |
| Post-chasm growth | Scaling, partnerships, ecosystem |
| Maturity | Efficiency, bundling, next S-curve exploration |
| New S-curve emerging | Evaluate jump timing, dual-track investment |
```

## Disruption Risk Scoring

### Composite Disruption Risk Score

```markdown
## Disruption Risk Assessment: [Business/Industry]

| Risk dimension | Score (1-5) | Evidence | Weight |
|---|---|---|---|
| Technology S-curve maturity | | [where on curve] | 20% |
| Low-end disruptor activity | | [specific threats] | 20% |
| New-market disruption signals | | [non-consumer innovation] | 15% |
| Customer satisfaction with "good enough" | | [overserving evidence] | 15% |
| Industry lifecycle stage | | [stage and trajectory] | 15% |
| Adjacent market convergence | | [ecosystem threats] | 15% |
| **Composite disruption risk** | | | **[X/5]** |

### Risk Level
- ≥ 4.0: CRITICAL — disruption likely within 2-3 years
- 3.0-3.9: HIGH — disruption possible within 3-5 years
- 2.0-2.9: MODERATE — disruption unlikely in near term
- < 2.0: LOW — stable position, monitor periodically
```

## Detection Signals

### Early Warning Indicators

| Signal | What to watch | Check frequency | Source |
|---|---|---|---|
| New entrant targeting non-consumers | Startups serving underserved segments | Monthly | WebSearch, Compete intel |
| Technology cost curve collapse | `10×` cost reduction in enabling tech | Quarterly | Industry reports, patents |
| Regulatory shift enabling new models | Deregulation, new standards, open mandates | Quarterly | PESTLE analysis |
| Customer "good enough" behavior | Customers choosing inferior but cheaper options | Monthly | Voice data, review trends |
| Venture capital concentration | VC flooding into adjacent category | Quarterly | Funding databases |
| Talent migration | Senior engineers moving to startups in adjacent space | Monthly | Job posting signals (Compete OSINT) |
| Business model innovation | Subscription replacing perpetual, freemium replacing paid, etc. | Quarterly | Market analysis |

## Strategic Response Patterns

| Disruption stage | Response option | Risk | Example |
|---|---|---|---|
| Early signals | Create internal disruptive unit | Medium | IBM PC division |
| Emerging threat | Acquire potential disruptor | Medium-High | Facebook acquiring Instagram |
| Active disruption | Dual-track: defend + disrupt self | High | Netflix DVD → streaming |
| Late-stage | Strategic pivot or managed decline | Very High | Kodak (failed), Fujifilm (succeeded) |

### Response Selection Rules

- If disruption vulnerability ≥ 4.0 and internal innovation capability is high → self-disrupt
- If disruption vulnerability ≥ 4.0 and internal innovation capability is low → acquire or partner
- If disruption risk is MODERATE → monitor + prepare contingency, do not overreact
- Never ignore disruption signals because current performance is strong — this is the innovator's dilemma

## Integration with Helm Workflow

Disruption detection integrates into the `SURVEY` phase:
- Run during external environment scan alongside PESTLE/Porter
- Feed disruption risk score into scenario simulation (especially pessimistic scenarios)
- Include in `LONG` horizon analysis as a standard check
- Cross-reference with Compete ecosystem mapping for convergence threats
- Escalate to Magi (`HELM_TO_MAGI`) if disruption risk ≥ 4.0 for Go/No-Go evaluation

## AI as Disruption: The 2025-2026 Christensen Institute Position

After Clayton Christensen's death on **2020-01-23**, the **Christensen Institute** (christenseninstitute.org) has continued to publish on how disruption theory applies to GenAI. The institute's standing position as of 2025-2026:

- **AI is not inherently disruptive or sustaining** — what matters is the *business model in which it is deployed*. The dominant tech firms (Amazon, Apple, Google, Meta, Microsoft) are largely using AI as a **sustaining innovation**, layering it onto existing offerings to keep current customers happy ([christenseninstitute.org "AI and Disruptive Innovation"](https://www.christenseninstitute.org/blog/ai-and-disruptive-innovation/)).
- **DeepSeek (Jan 2025)** is the most-cited current candidate for a textbook **low-end / new-market disruptor**: open-weight, dramatically lower training cost, initially "good enough" performance, attacking non-consumers of frontier-model APIs ([CAI-Jun, Medium Feb 2025](https://medium.com/@aestech/deepseeks-challenge-to-recreate-christensen-s-innovator-s-dilemma-a879810e11e2)).
- **AI in education** is now the institute's clearest disruption case — entrant schools use adaptive AI as the primary instruction channel while incumbents bolt AI onto teacher-directed models (sustaining only).

### "Disruptor Detective" — AI-Assisted Disruption Scoring

Imerman & Fabozzi (2025) — *Quantifying disruption in the age of AI: An AI-based approach to evaluating startup innovation and investment potential* (ScienceDirect S1544612325007500) — propose a GPT-powered tool that scores companies on seven refined Christensen criteria. Treat its output as **input**, not verdict; calibrate against the standard 5-dimension vulnerability scorecard above and require the human assessor to attach evidence per dimension.

### Updated Disruption Classification Cheat Sheet (2026)

| Candidate | Most likely classification | Why |
|---|---|---|
| GenAI APIs from incumbents (OpenAI / Anthropic / Google) priced for enterprise | Sustaining for incumbents (Microsoft, Google) | Layered onto existing offerings, sold to existing customers, defends seat ARR |
| Open-weight frontier models (DeepSeek, Qwen, Llama derivatives) | Low-end disruption | Started "good enough" for many use cases at order-of-magnitude lower TCO; improving fast |
| AI agents replacing seat-based SaaS | New-market disruption against headcount budgets | Tap budget that used to fund hires, not software |
| "Like X but with AI" thin wrappers | Usually neither — feature, not disruptor | Vulnerable to incumbent platform absorbing the feature (see `strategic-anti-patterns.md` AP-19) |
| GenAI in regulated incumbents (banking, insurance, healthcare core) | Sustaining-first, then disruption later | Compliance + brand inertia delay low-end entry by 2-4 years |
