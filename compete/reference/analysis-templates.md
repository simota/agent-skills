# Compete Analysis Templates Reference

Purpose: Use this file when Compete must create a competitor profile, comparison matrix, SWOT, positioning map, benchmark, or differentiation plan.

## Contents

- Competitor profile
- Feature comparison
- SWOT
- Positioning
- Benchmarking
- Differentiation strategy

## Competitor Profile

Use this as the default one-company snapshot.

```markdown
## Competitor Profile: [Company Name]

### Overview
- Founded: [Year]
- Headquarters: [Location]
- Company Size: [Employees]
- Funding / Public Status: [Details]
- Target Market: [Description]

### Product Summary
[2-3 sentence summary]

### Strengths
1. [Strength] - [Evidence]
2. [Strength] - [Evidence]
3. [Strength] - [Evidence]

### Weaknesses
1. [Weakness] - [Evidence]
2. [Weakness] - [Evidence]
3. [Weakness] - [Evidence]

### Pricing
| Tier | Price | Key Features |
|---|---:|---|
| Free | ¥0 | [...] |
| Pro | ¥X / month | [...] |
| Enterprise | Custom | [...] |

### Target Customer
- Primary: [...]
- Secondary: [...]
- Not targeting: [...]

### Recent Moves
- [YYYY-MM] [...]
- [YYYY-MM] [...]

### Sources
- [Source] — tag with Tier (1/2/3) per `intelligence-gathering.md#source-tiers`
- [Source]
```

> **Source attribution:** every claim in the templates above should carry a source tag and Tier reliability score. See `intelligence-gathering.md#source-tiers` for the canonical Tier 1/2/3 definitions and conflict-resolution rules.

## Feature Comparison

### Basic Matrix

Use this for parity and obvious gaps.

```markdown
## Feature Comparison: [Category]

| Feature | Our Product | Competitor A | Competitor B | Competitor C |
|---|---|---|---|---|
| Feature 1 | Yes | Yes | Yes | No |
| Feature 2 | Planned | Yes | No | Yes |
| Feature 3 | Yes | Partial | Yes | Yes |

Legend:
- Yes = fully available
- Partial = limited
- Planned = roadmap
- No = absent
```

### Weighted Matrix

Use this when tradeoffs matter more than feature counts.

```markdown
## Weighted Feature Comparison

| Feature | Weight | Our Score | Comp A | Comp B | Comp C |
|---|---:|---:|---:|---:|---:|
| [Feature 1] | 5 | 4 | 5 | 3 | 4 |
| [Feature 2] | 4 | 5 | 3 | 4 | 2 |
| [Feature 3] | 3 | 3 | 4 | 5 | 3 |
| Weighted Total | - | **85** | **72** | **68** | **65** |

Scoring:
- 5 = best in class
- 4 = above average
- 3 = acceptable
- 2 = weak
- 1 = missing or poor
```

## SWOT

```markdown
## SWOT Analysis: [Our Product]

### Strengths
| Strength | Evidence | How to Leverage |
|---|---|---|
| [...] | [...] | [...] |

### Weaknesses
| Weakness | Impact | Mitigation Plan |
|---|---|---|
| [...] | High/Med/Low | [...] |

### Opportunities
| Opportunity | Potential | Required Action |
|---|---|---|
| [...] | High/Med/Low | [...] |

### Threats
| Threat | Likelihood | Response Strategy |
|---|---|---|
| [...] | High/Med/Low | [...] |
```

Rule:
- map internal positives/negatives to Strengths and Weaknesses
- map external positives/negatives to Opportunities and Threats
- every row must imply an action, not just a label

## Positioning

### 2x2 Matrix

Use a 2x2 only when the two axes drive actual buying behavior.

```markdown
## Positioning Map

Axes:
- X: [Low -> High]
- Y: [Simple -> Advanced]

Players:
- Our Product: [position]
- Competitor A: [position]
- Competitor B: [position]
- Competitor C: [position]
```

### Positioning Statement

```markdown
For [target customer]
Who [has this need]
[Product] is a [category]
That [key benefit]
Unlike [primary competitor]
Our product [key differentiator]
```

## Benchmarking

### Performance Benchmark

```markdown
## Performance Benchmark

| Metric | Our Product | Industry Avg | Best in Class | Gap |
|---|---:|---:|---:|---:|
| Load Time | 2.5s | 3.0s | 1.5s | -1.0s |
| Uptime | 99.5% | 99.0% | 99.99% | -0.49% |
| Response Time | 200ms | 300ms | 100ms | -100ms |
| Error Rate | 0.5% | 1.0% | 0.1% | -0.4% |
```

### Experience Benchmark

```markdown
## UX Benchmark

| Criterion | Our Product | Competitor A | Competitor B | Notes |
|---|---|---|---|---|
| Steps to Complete | 5 | 3 | 7 | [...] |
| Time to Complete | 2 min | 1 min | 4 min | [...] |
| Error Recovery | Good | Poor | Excellent | [...] |
| Mobile Experience | Excellent | Good | Poor | [...] |
```

## Differentiation Strategy Selector

| Strategy | Use when | Typical evidence |
|---|---|---|
| Feature | you can sustain unique capability | roadmap, patents, exclusive data |
| Price | cost structure allows durable advantage | TCO, margin model, packaging |
| Experience | UX simplicity is the deciding factor | time-to-value, completion rate, reviews |
| Niche | an underserved segment is obvious | segment-specific complaints or needs |
| Integration | partners amplify switching cost or reach | ecosystem depth, workflow lock-in |
| Speed | execution or runtime performance matters | launch cadence, latency, deployment time |
| Trust | compliance, reliability, or brand matters | certifications, references, incident record |

Default rule:
- choose the smallest set of differentiators that make the product the obvious choice for a defined buyer.
