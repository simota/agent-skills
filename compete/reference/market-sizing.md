# Market Sizing Reference

Purpose: Use this file when Compete must estimate market size (TAM/SAM/SOM/PAM), validate market assumptions, or size adjacent markets for competitive context.

## Contents

- Core definitions
- Estimation methodologies
- Cross-verification protocol
- Adjacent market sizing
- Market sizing templates
- Common pitfalls

## Core Definitions

| Metric | Definition | Question it answers |
|---|---|---|
| **TAM** (Total Addressable Market) | Total market demand if 100% capture with no constraints | How big is the universe? |
| **SAM** (Serviceable Available Market) | Portion addressable with current product, geography, and model | How much can we reach? |
| **SOM** (Serviceable Obtainable Market) | Realistic share given competition and execution capacity | How much can we actually win? |
| **PAM** (Potential Addressable Market) | Future TAM including adjacent markets and product evolution | Where could we expand? |

Relationship: `TAM ⊃ SAM ⊃ SOM` and `PAM ⊃ TAM (future)`

## Estimation Methodologies

### Top-Down Approach

Start from broad industry data and narrow.

```text
TAM = Industry total revenue (from analyst reports)
SAM = TAM × geographic filter × segment filter × product fit filter
SOM = SAM × realistic market share (based on competitive position)
```

**Best for**: Quick sizing, investor-facing estimates, macro validation.
**Risk**: Overly optimistic if filters are too loose.

### Bottom-Up Approach

Count potential customers and multiply by value.

```text
TAM = Total potential customers × Average annual contract value (ACV)
SAM = Reachable customers × ACV (with current go-to-market)
SOM = Pipeline-qualified customers × Win rate × ACV
```

**Best for**: Grounding estimates in business reality, operational planning.
**Risk**: Undercounts if customer universe is incomplete.

### Value-Theory Approach

Estimate based on the value delivered, not current spending.

```text
TAM = Customer pain cost × Number of customers experiencing pain
     (even if they don't currently buy a solution)
```

**Best for**: New categories, category creation, disruptive products.
**Risk**: Hardest to validate, requires strong assumption documentation.

### Cross-Verification Protocol

**Always apply both top-down and bottom-up.** If estimates diverge by `> 3×`, revisit assumptions.

```markdown
## Market Size Cross-Verification

| Method | TAM | SAM | SOM | Key assumptions |
|--------|-----|-----|-----|-----------------|
| Top-down | $X | $Y | $Z | [list assumptions] |
| Bottom-up | $X | $Y | $Z | [list assumptions] |
| Divergence | X% | Y% | Z% | |

Divergence analysis:
- If < 2×: reasonable alignment, use average with range
- If 2-3×: investigate assumption differences, document which is more reliable
- If > 3×: RED FLAG — one methodology has a flawed assumption, resolve before proceeding
```

## Adjacent Market Sizing (PAM)

### Why Adjacent Markets Matter for CI

Competitors don't just compete in your current market. They may:
- Expand from an adjacent market into yours (platform invasion)
- Pull your customers into their adjacent market (bundling)
- Redefine the category boundary to include adjacencies

### Adjacency Mapping

```markdown
## Adjacent Market Analysis

### Current Market
- Market: [name]
- TAM: $[X]
- Our position: [leader/challenger/niche/entrant]

### Adjacent Markets
| Adjacent market | TAM | Connection type | Threat level | Key player |
|---|---|---|---|---|
| [Market A] | $X | Customer overlap | H/M/L | [Company] |
| [Market B] | $X | Technology overlap | H/M/L | [Company] |
| [Market C] | $X | Workflow adjacency | H/M/L | [Company] |

### Expansion Vectors
| Vector | From → To | Enabler | Barrier | Timeline |
|---|---|---|---|---|
| [Vector 1] | [Market A] → [Our market] | [what enables it] | [what prevents it] | [estimate] |
| [Vector 2] | [Our market] → [Market B] | [what enables it] | [what prevents it] | [estimate] |
```

### Connection Types

| Type | Definition | Example |
|---|---|---|
| Customer overlap | Same buyer persona | CRM → Marketing automation |
| Technology overlap | Shared tech stack | Cloud storage → CDN |
| Workflow adjacency | Sequential in customer workflow | Design tool → Prototyping → Dev handoff |
| Data adjacency | Shared or complementary data | Analytics → Personalization |
| Bundle economics | Lower marginal cost to add | Office suite additions |

## Market Sizing Templates

### Template: SaaS Market Sizing

```markdown
## Market Size Estimate: [Category Name]

### TAM (Top-Down)
- Global [category] market: $[X]B ([source, year])
- Annual growth rate: [X]% CAGR
- 5-year projection: $[X]B

### SAM (Filtered)
- Geographic filter: [regions] → [X]% of TAM
- Segment filter: [SMB/Mid/Enterprise] → [X]% of geographic
- Product fit filter: [specific use case] → [X]% of segment
- **SAM = $[X]B**

### SOM (Realistic)
- Current competitive win rate: [X]%
- Addressable pipeline: [X] companies
- Average ACV: $[X]
- **SOM = $[X]M** ([X]% of SAM)

### Bottom-Up Verification
- Target companies in segment: [X]
- Estimated adoption rate: [X]%
- Average ACV: $[X]
- **Bottom-up SOM = $[X]M**

### Cross-check
- Top-down SOM: $[X]M
- Bottom-up SOM: $[X]M
- Divergence: [X]%
- Assessment: [aligned / investigate / red flag]

### Sources
- [1] [source with URL and date]
- [2] [source with URL and date]
```

### Template: Competitive Market Share Estimation

```markdown
## Market Share Estimation: [Category]

### Total market: $[X] ([source])

### Share Estimation
| Player | Estimated revenue | Share | Method | Confidence |
|--------|------------------|-------|--------|------------|
| [Company A] | $[X] | [X]% | [public filing / estimate] | H/M/L |
| [Company B] | $[X] | [X]% | [public filing / estimate] | H/M/L |
| [Company C] | $[X] | [X]% | [public filing / estimate] | H/M/L |
| Others | $[X] | [X]% | remainder | L |

### Estimation Methods
- Public companies: SEC filings, segment revenue
- Private companies: employee count × revenue-per-employee benchmark, funding stage heuristics
- Growth-stage: last known ARR × estimated growth rate

### Concentration Analysis
- HHI (Herfindahl-Hirschman Index): [score]
- Top 3 concentration: [X]%
- Market structure: [monopoly / oligopoly / fragmented / emerging]
```

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| TAM fantasy | Inflating TAM with loosely related markets | Apply strict segment and product-fit filters |
| Static sizing | Treating market size as fixed | Include CAGR and project forward |
| Ignoring substitutes | Sizing only direct competitors | Include JTBD-based substitutes in TAM |
| Revenue vs transaction | Confusing GMV with revenue | Be explicit about which metric is used |
| Geography blindness | Using global TAM for local strategy | Always filter by serviceable geography |
| Snapshot bias | Sizing at one point in time | Track market size trajectory over 3+ years |
| Assumption burial | Hiding assumptions in methodology | State every assumption explicitly |
| Top-down only | Skipping bottom-up verification | Always cross-verify |

## Integration with Compete Workflow

Market sizing fits into the `MAP` phase of the main workflow:
- Run WebSearch for market reports, analyst estimates, and public filings
- Apply both estimation methodologies
- Cross-verify and document divergence
- Feed sizing data into competitive positioning analysis
- Hand off to Helm (`COMPETE_TO_HELM`) when strategic simulation needs market context
