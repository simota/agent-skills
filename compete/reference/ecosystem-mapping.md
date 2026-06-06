# Ecosystem Mapping Reference

Purpose: Use this file when Compete must analyze platform ecosystems, network effects, partnership landscapes, integration moats, or adjacent market threats.

## Contents

- Ecosystem analysis framework
- Network effect classification
- Platform ecosystem mapping
- Partnership and integration analysis
- Cross-market subsidization detection
- Ecosystem health metrics
- Templates

## Ecosystem Analysis Framework

### Why Ecosystem Analysis Matters

Traditional competitive analysis compares Company A vs Company B. But in platform economies, the unit of competition is the ecosystem, not the company. A firm's competitive advantage includes its partners, integrations, developer community, and data network effects.

### Three Lenses

| Lens | Question | Output |
|---|---|---|
| **Structure** | Who are the players and how are they connected? | Ecosystem map with node relationships |
| **Dynamics** | How do value and influence flow? | Value flow diagram with directionality |
| **Trajectory** | Where is the ecosystem heading? | Evolution forecast with tipping points |

## Network Effect Classification

| Type | Definition | Strength indicator | Example |
|---|---|---|---|
| **Direct** (same-side) | More users → more value for each user | User growth rate, engagement per user | Social networks, messaging |
| **Indirect** (cross-side) | More users on side A → more value for side B | Marketplace liquidity, match rate | Marketplaces, app stores |
| **Data** | More usage → better product via data/ML | Model accuracy, personalization quality | Search, recommendation engines |
| **Content** | More users → more content → more users | UGC volume, content diversity | YouTube, Stack Overflow |
| **Integration** | More integrations → more sticky → more integrations | Integration count, API call volume | Salesforce, Slack |
| **Protocol/Standard** | Adoption creates lock-in through compatibility | Adoption rate, switching cost | USB, TCP/IP, file formats |

### Network Effect Strength Assessment

```markdown
## Network Effect Assessment: [Company/Platform]

| Effect type | Present? | Strength (1-5) | Defensibility | Evidence |
|---|---|---|---|---|
| Direct | Y/N | | H/M/L | [evidence] |
| Indirect | Y/N | | H/M/L | [evidence] |
| Data | Y/N | | H/M/L | [evidence] |
| Content | Y/N | | H/M/L | [evidence] |
| Integration | Y/N | | H/M/L | [evidence] |
| Protocol | Y/N | | H/M/L | [evidence] |

Composite network effect score: [X/30]
Dominant effect: [type]
Vulnerability: [what could weaken the strongest effect]
```

## Platform Ecosystem Mapping

### Mapping Protocol

```markdown
## Ecosystem Map: [Platform Name]

### Core Platform
- Value proposition: [what the platform enables]
- Primary users: [who uses it directly]
- Revenue model: [how it monetizes]

### Ecosystem Layers
| Layer | Players | Role | Dependency on platform |
|---|---|---|---|
| Core product | [platform itself] | Value creation | — |
| First-party extensions | [built by platform owner] | Value expansion | High |
| Third-party integrations | [partner companies] | Ecosystem enrichment | Medium-High |
| Developer community | [independent developers] | Long-tail value | Medium |
| Complementary products | [adjacent companies] | Workflow completion | Low-Medium |
| End users | [customers] | Value consumption | Varies |

### Integration Landscape
| Integration | Type | Direction | Strategic value |
|---|---|---|---|
| [Integration A] | Native / API / Marketplace | Inbound/Outbound/Bidirectional | Critical/Important/Nice-to-have |
| [Integration B] | ... | ... | ... |

### Ecosystem Competitive Dynamics
- Platform owner power: [high/medium/low — does the platform extract or share value?]
- Multi-homing cost: [high/medium/low — how easy to use competing platforms simultaneously?]
- Disintermediation risk: [high/medium/low — can participants bypass the platform?]
```

### Platform Power Assessment

| Dimension | Low power | High power |
|---|---|---|
| Switching cost | Data portable, standards-based | Proprietary format, deep integration |
| Multi-homing | Easy to use multiple platforms | Exclusive or high friction |
| Value capture | Platform shares most value | Platform extracts disproportionate rent |
| Governance | Open, predictable rules | Opaque, frequently changing |
| API stability | Stable, versioned, backward-compatible | Frequent breaking changes |

## Partnership and Integration Analysis

### Partnership Landscape Mapping

```markdown
## Partnership Landscape: [Company Name]

### Partnership Types
| Partner | Type | Depth | Strategic value | Exclusivity |
|---|---|---|---|---|
| [Partner A] | Technology | Deep/Surface | H/M/L | Yes/No |
| [Partner B] | Distribution | Deep/Surface | H/M/L | Yes/No |
| [Partner C] | Data | Deep/Surface | H/M/L | Yes/No |

### Partnership Signals
- New partnerships announced: [list with dates]
- Partnerships dissolved: [list with dates]
- Partnership depth changes: [upgrades/downgrades]

### Integration Moat Assessment
- Total integrations: [count]
- Growth rate: [monthly/quarterly new integrations]
- Integration depth: [shallow API / deep embedded / native]
- Developer ecosystem: [SDK quality, documentation, community size]
- Marketplace health: [if applicable — listing count, review quality, revenue share]
```

## Cross-Market Subsidization Detection

### Why This Matters

Platform companies often price below cost in one market to capture value in an adjacent market. Recognizing this pattern is critical for competitive response.

### Detection Signals

| Signal | What to look for | Example |
|---|---|---|
| Below-cost pricing | Product priced lower than standalone economics justify | Google Workspace pricing vs standalone office tools |
| Aggressive free tier | Generous free tier beyond normal PLG economics | Amazon's loss-leading devices |
| Bundling acceleration | Rapid addition of features from adjacent markets | Microsoft adding Teams to Office 365 |
| Acquisition in adjacent space | Buying companies in markets they don't yet monetize | Platform acquiring complementary tools |
| Revenue mix shift | Growing revenue from adjacent market while core pricing drops | Core product becomes distribution for adjacent revenue |

### Assessment Template

```markdown
## Cross-Market Subsidization Analysis: [Company]

### Markets Operated In
| Market | Product | Pricing posture | Revenue (est) | Role |
|---|---|---|---|---|
| [Market A] | [Product] | Premium/Competitive/Below-cost | $X | Cash cow / Subsidizer |
| [Market B] | [Product] | Premium/Competitive/Below-cost | $X | Growth / Subsidized |

### Subsidy Flow
- Direction: [Market A] → subsidizes → [Market B]
- Mechanism: [bundling / free tier / cross-sell / data leverage]
- Estimated subsidy magnitude: [X]% of Market B costs covered by Market A profits
- Sustainability: [indefinite / time-limited / VC-funded]

### Competitive Implication
- Can we compete on price in the subsidized market? [Yes/No — why]
- What is our counter-strategy? [differentiate / niche / partner / match]
```

## Ecosystem Health Metrics

Use these to evaluate the vitality and trajectory of a platform ecosystem:

| Metric | Healthy | Warning | Critical |
|---|---|---|---|
| Developer growth (YoY) | `> 20%` | `0-20%` | `< 0%` (shrinking) |
| Integration count growth | `> 15%` | `0-15%` | `< 0%` |
| Third-party app quality | Improving ratings | Stable | Declining ratings |
| API breaking changes/year | `0-1` | `2-3` | `4+` |
| Partner satisfaction | High (survey/signals) | Mixed | Low / departures |
| Multi-homing rate | Low (sticky) | Rising | High (commodity) |
| Platform revenue per partner | Growing | Flat | Declining |

## Integration with Compete Workflow

Ecosystem analysis fits into the `ANALYZE` phase:
- Use during Landscape analysis when competitors operate as platforms
- Use during Strategy analysis to assess moat durability via network effects
- Use during Benchmark analysis to compare ecosystem breadth and health
- Feed ecosystem findings into Helm (`COMPETE_TO_HELM`) for strategic simulation of platform dynamics
