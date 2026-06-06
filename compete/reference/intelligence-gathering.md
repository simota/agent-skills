# Compete Intelligence Gathering Reference

Purpose: Use this file when mapping competitors, collecting evidence, or comparing pricing, reviews, stack, and SEO signals.

## Contents

- Source tiers
- Collection checklist
- Pricing intelligence
- Review intelligence
- Tech-stack intelligence
- SEO intelligence

## Source Tiers

| Tier | Source type | Default reliability |
|---|---|---:|
| Tier 1 | official website, docs, changelog, public filings | `0.90` |
| Tier 2 | review platforms, analyst reports, app stores | `0.75-0.85` |
| Tier 3 | job posts, community forums, social signals | `0.60-0.65` |

Rule:
- start with Tier 1
- use Tier 3 for signal generation, not as sole proof
- when sources conflict, report the disagreement explicitly

## Public Collection Checklist

```markdown
## Intel Gathering: [Competitor Name]

### Website & Product
- [ ] Marketing website
- [ ] Product pages
- [ ] Pricing page
- [ ] Blog
- [ ] Changelog
- [ ] Documentation

### External Sources
- [ ] Review sites
- [ ] Social media
- [ ] Job postings
- [ ] Press releases
- [ ] Industry reports
- [ ] App stores

### Community
- [ ] Forums
- [ ] Reddit
- [ ] Slack/Discord communities
- [ ] Hacker News
- [ ] Stack Overflow

### Financial
- [ ] SEC filings
- [ ] Earnings calls
- [ ] Investor presentations
```

## Pricing Intelligence

```markdown
## Price Intelligence: [Category]

### Price Positioning
| Tier | Our Price | Comp A | Comp B | Comp C | Notes |
|---|---:|---:|---:|---:|---|
| Free/Starter | ¥[...] | ¥[...] | ¥[...] | ¥[...] | [...] |
| Pro/Growth | ¥[...] | ¥[...] | ¥[...] | ¥[...] | [...] |
| Enterprise | ¥[...] | ¥[...] | ¥[...] | ¥[...] | [...] |

### TCO Comparison (3-Year)
| Component | Us | Comp A | Comp B |
|---|---:|---:|---:|
| License | ¥[...] | ¥[...] | ¥[...] |
| Implementation | ¥[...] | ¥[...] | ¥[...] |
| Training | ¥[...] | ¥[...] | ¥[...] |
| Maintenance | ¥[...] | ¥[...] | ¥[...] |
| Total TCO | ¥[...] | ¥[...] | ¥[...] |
```

Use pricing analysis to answer:
- where are we cheaper, more expensive, or structurally different?
- is the competitor winning on price or on perceived value?
- what is the real switching cost?

## Review Intelligence

```markdown
## Review Intelligence: [Competitor Name]

### Aggregate Scores
| Platform | Rating | Reviews | Trend |
|---|---:|---:|---|
| G2 | [...] | [...] | ↑/↓/→ |
| Capterra | [...] | [...] | ↑/↓/→ |
| TrustRadius | [...] | [...] | ↑/↓/→ |

### Common Complaints
| Issue | Frequency | Our Advantage |
|---|---:|---|
| [...] | [...] | [...] |

### Common Praise
| Strength | Frequency | Our Comparison |
|---|---:|---|
| [...] | [...] | Equal/Behind/Ahead |
```

Rule:
- complaints are high-signal opportunities only if they repeat across sources
- one loud review is not a market truth

## Tech-Stack Intelligence

```markdown
## Tech Stack Analysis: [Competitor Name]

### Infrastructure
| Component | Technology | Notes |
|---|---|---|
| Cloud Provider | [...] | [...] |
| CDN | [...] | [...] |
| Database | [...] | [...] |

### Frontend
| Aspect | Technology | Quality |
|---|---|---|
| Framework | [...] | [...] |
| Mobile | [...] | [...] |
| Lighthouse Performance | [...] | [...] |
| Lighthouse Accessibility | [...] | [...] |

### Backend
| Aspect | Technology | Notes |
|---|---|---|
| Language | [...] | [...] |
| Architecture | [...] | [...] |
| API | [...] | [...] |
| Real-time | [...] | [...] |
```

Sources:
- BuiltWith
- Wappalyzer
- job postings
- docs and API references

## SEO Intelligence

```markdown
## SEO Competitive Analysis: [Competitor Name]

### Domain Metrics
| Metric | Competitor | Us | Gap | Priority |
|---|---:|---:|---:|---|
| Domain Authority | [...] | [...] | [...] | H/M/L |
| Referring Domains | [...] | [...] | [...] | H/M/L |
| Organic Traffic | [...] | [...] | [...] | H/M/L |

### Keyword Gaps
| Keyword | Monthly Volume | Their Rank | Our Rank | Opportunity |
|---|---:|---:|---:|---|
| [...] | [...] | [...] | [...] | High/Med/Low |
```

Use SEO intelligence when the output must feed Growth or pricing/positioning strategy.
