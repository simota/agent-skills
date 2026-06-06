# Deep OSINT Signals Reference

Purpose: Use this file when Compete needs to go beyond surface-level web research and extract strategic intent signals from structured public data sources.

## Contents

- Signal source hierarchy
- Job posting signal analysis
- Patent and IP analysis
- SEC filing narrative analysis
- GitHub and open-source intelligence
- App store review mining
- Technology trajectory analysis
- Signal triangulation methodology

## Signal Source Hierarchy

Deep OSINT adds structured signal layers on top of the standard Source Tiers.

| Layer | Source | Signal type | Reliability | Lag |
|---|---|---|---|---|
| L1 | SEC 10-K/10-Q, earnings transcripts | Strategic intent, financial health | `0.95` | `1-3 months` |
| L2 | Patent filings (USPTO, EPO, WIPO) | R&D direction, technology bets | `0.90` | `6-18 months` |
| L3 | Job postings (LinkedIn, Indeed, company sites) | Hiring velocity, capability building | `0.80` | `1-3 months` |
| L4 | GitHub repos, npm/PyPI, developer activity | Technology adoption, ecosystem health | `0.75` | `real-time` |
| L5 | App store reviews, G2/Capterra trends | User sentiment trajectory | `0.70` | `real-time` |
| L6 | Conference talks, blog posts, community signals | Thought leadership, narrative shifts | `0.60` | `varies` |

Rule: triangulate across 3+ layers before drawing strategic conclusions. Single-layer signals are hypotheses, not findings.

## Job Posting Signal Analysis

### Why Job Postings Matter

A hiring spree is not just growth — it is a signal of where strategic pressure is mounting. Job postings reveal:
- **Technology bets**: "Senior Rust Engineer" → performance-critical rewrite
- **Market expansion**: "Japan Country Manager" → APAC entry
- **Capability gaps**: "First ML Engineer" → AI pivot
- **Organizational stress**: sudden spike in senior roles → leadership churn

### Collection Protocol

```markdown
## Job Signal Analysis: [Competitor Name]

### Volume Tracking
| Period | Total postings | Engineering | Sales | Product | Other |
|--------|---------------|-------------|-------|---------|-------|
| Current month | | | | | |
| Previous month | | | | | |
| 3-month trend | ↑/↓/→ | ↑/↓/→ | ↑/↓/→ | ↑/↓/→ | ↑/↓/→ |

### Strategic Signal Extraction
| Signal | Evidence | Confidence | Implication |
|--------|----------|------------|-------------|
| Technology shift | [specific job titles, required skills] | H/M/L | [what this means for their product direction] |
| Market expansion | [location-specific roles, language requirements] | H/M/L | [target markets] |
| Capability build | [new role types not previously posted] | H/M/L | [new capability being built] |
| Organizational stress | [leadership roles, sudden volume changes] | H/M/L | [internal challenges] |

### Key Skill Clusters
- [Cluster 1]: [skills] → implies [strategic direction]
- [Cluster 2]: [skills] → implies [strategic direction]
```

### Interpretation Rules

| Pattern | Signal strength | Typical meaning |
|---|---|---|
| `5+` similar roles in `< 30 days` | High | Active capability build |
| New role type never posted before | High | Strategic pivot or new initiative |
| Senior/leadership roles spike | Medium-High | Organizational restructuring or churn |
| Location cluster change | Medium | Market expansion or consolidation |
| Skill requirement shift (e.g., Python → Rust) | Medium | Technology migration |
| Hiring freeze (volume drop `>50%`) | Medium | Cash constraint or strategic pause |

## Patent and IP Analysis

### Why Patents Matter

Patents reveal R&D direction `6-18 months` before product launches. They show where a competitor is investing intellectual capital, not marketing dollars.

### Collection Protocol

```markdown
## Patent Signal Analysis: [Competitor Name]

### Filing Summary
| Period | Total filings | Granted | Pending | Key technology areas |
|--------|--------------|---------|---------|---------------------|
| Last 12 months | | | | |
| Previous 12 months | | | | |
| Trend | ↑/↓/→ | | | |

### Technology Cluster Analysis
| Cluster | Patent count | Key patents | Implication |
|---------|-------------|-------------|-------------|
| [Technology area 1] | | [patent IDs/titles] | [product/strategy implication] |
| [Technology area 2] | | [patent IDs/titles] | [product/strategy implication] |

### Strategic Signals
- Filing velocity change: [acceleration/deceleration in specific areas]
- New technology domains: [areas not previously filed in]
- Defensive vs offensive: [broad defensive filings vs specific product patents]
- Cross-reference with job postings: [alignment/divergence]
```

### Patent Signal Interpretation

| Pattern | Meaning |
|---|---|
| Filing surge in new domain | Market entry preparation |
| Broad defensive filings | Protecting existing moat |
| Continuation patents on specific invention | Iterating toward product launch |
| Patent acquisition (not filing) | Buy vs build decision |
| Filing in specific jurisdictions | Geographic expansion plans |

## SEC Filing Narrative Analysis

### Why Narrative Analysis Matters

Financial numbers tell what happened. Management narrative in 10-K/10-Q filings tells what leadership believes and fears. Specific sections to mine:

| Section | What to extract |
|---|---|
| Risk Factors | New risks added = strategic concerns; removed risks = resolved issues |
| MD&A (Management Discussion & Analysis) | Strategic priorities, market view, investment thesis |
| Business Description changes | Repositioning, new segments, discontinued operations |
| Earnings call transcripts | Tone shifts, analyst Q&A reveals pressure points |

### Collection Protocol

```markdown
## SEC Narrative Analysis: [Competitor Name]

### Risk Factor Changes (YoY comparison)
| Risk | Status | Significance |
|------|--------|--------------|
| [New risk added] | NEW | [what this reveals] |
| [Risk removed] | REMOVED | [what this means] |
| [Risk language changed] | MODIFIED | [direction of change] |

### MD&A Key Themes
| Theme | Quote/Evidence | Strategic Implication |
|-------|---------------|----------------------|
| [Theme 1] | "[relevant quote]" | [implication] |
| [Theme 2] | "[relevant quote]" | [implication] |

### Earnings Call Tone Analysis
| Topic | Tone (confident/cautious/defensive) | Notable quote |
|-------|--------------------------------------|---------------|
| [Topic 1] | | "[quote]" |
| [Topic 2] | | "[quote]" |

### Forward-Looking Signals
- Capital allocation shifts: [where money is moving]
- Segment revenue mix changes: [growing/shrinking areas]
- Guidance language: [raised/maintained/lowered/withdrawn]
```

### Narrative Red Flags

| Signal | Meaning |
|---|---|
| New risk factor about competition | Market pressure increasing |
| "Strategic alternatives" language | Possible M&A or exit |
| Segment restructuring | Product focus shifting |
| Guidance withdrawal | High uncertainty, potential trouble |
| Increased R&D as % of revenue | Investing for future, sacrificing current margin |
| Decreased S&M as % of revenue | Efficiency mode or demand softening |

## GitHub and Open-Source Intelligence

### Why Developer Activity Matters

Open-source activity reveals technology choices, developer ecosystem health, and community engagement before marketing announces anything.

### Collection Protocol

```markdown
## GitHub/OSS Intelligence: [Competitor Name]

### Repository Activity
| Metric | Current | 3-month ago | Trend |
|--------|---------|-------------|-------|
| Public repos | | | ↑/↓/→ |
| Stars (top 5 repos) | | | ↑/↓/→ |
| Contributors (active/month) | | | ↑/↓/→ |
| Commit frequency | | | ↑/↓/→ |
| Open issues | | | ↑/↓/→ |
| Issue response time (median) | | | ↑/↓/→ |

### Technology Signals
| Signal | Evidence | Implication |
|--------|----------|-------------|
| New repo in unfamiliar domain | [repo name, description] | [strategic direction] |
| Dependency changes | [added/removed packages] | [technology migration] |
| API/SDK updates | [changelog highlights] | [platform strategy] |
| Archived/abandoned repos | [repo names] | [deprecated initiatives] |

### Developer Ecosystem Health
- npm/PyPI download trends: [trajectory]
- Third-party integration count: [growing/stable/declining]
- Community contributions vs internal: [ratio and trend]
```

## App Store Review Mining

### Why Review Trends Matter

Aggregate review scores are lagging indicators. Review text trends are leading indicators of product trajectory.

### Collection Protocol

```markdown
## Review Trend Analysis: [Competitor Name]

### Score Trajectory (not just current score)
| Platform | 6mo ago | 3mo ago | Current | Trend | Velocity |
|----------|---------|---------|---------|-------|----------|
| G2 | | | | ↑/↓/→ | fast/slow |
| Capterra | | | | ↑/↓/→ | fast/slow |
| App Store | | | | ↑/↓/→ | fast/slow |
| Product Hunt | | | | ↑/↓/→ | fast/slow |

### Theme Extraction (from recent reviews)
| Theme | Frequency | Sentiment | Trend vs 3mo ago |
|-------|-----------|-----------|-------------------|
| [Theme 1] | | +/- | ↑/↓/→ |
| [Theme 2] | | +/- | ↑/↓/→ |

### Strategic Signals
- Emerging complaints: [new pain points appearing]
- Resolved complaints: [previously common issues disappearing]
- Feature requests clustering: [unmet demand signals]
- Churn signals: [migration mentions, "switching to X"]
```

## Technology Trajectory Analysis

### Trajectory vs Snapshot

A snapshot tells where a competitor is now. A trajectory tells where they are heading and how fast.

### Multi-Signal Trajectory Framework

```markdown
## Technology Trajectory: [Competitor Name]

### Evidence Matrix
| Signal source | Direction | Velocity | Confidence |
|---|---|---|---|
| Job postings (skill shifts) | [direction] | fast/medium/slow | H/M/L |
| Patent filings (tech clusters) | [direction] | fast/medium/slow | H/M/L |
| GitHub activity (tech stack) | [direction] | fast/medium/slow | H/M/L |
| Product releases (feature cadence) | [direction] | fast/medium/slow | H/M/L |
| Conference talks (narrative) | [direction] | fast/medium/slow | H/M/L |

### Trajectory Assessment
- Primary direction: [where they are heading]
- Secondary bets: [parallel explorations]
- Abandoned directions: [what they stopped investing in]
- Estimated timeline: [when product impact expected]
- Our exposure: [how this trajectory affects our position]
```

## Signal Triangulation Methodology

### The Triangulation Rule

No strategic conclusion from a single signal source. Require cross-validation:

| Conclusion confidence | Minimum requirement |
|---|---|
| High | `3+` independent layers confirm, no contradictions |
| Medium | `2` layers confirm, no contradictions |
| Low | `1` layer suggests, plausible but unverified |
| Speculative | Pattern-matched from indirect signals only |

### Cross-Reference Matrix

```markdown
## Signal Triangulation: [Strategic Hypothesis]

Hypothesis: [Competitor X is preparing to enter market Y]

| Layer | Supporting evidence | Contradicting evidence | Weight |
|---|---|---|---|
| Job postings | | | |
| Patents | | | |
| SEC filings | | | |
| GitHub/OSS | | | |
| Product changes | | | |
| Reviews/community | | | |

Triangulation score: [High/Medium/Low/Speculative]
Recommended action: [proceed with analysis / gather more data / discard hypothesis]
```

### Anti-Pattern: Confirmation Bias in Deep OSINT

When collecting deep signals, the risk of seeing patterns that aren't there increases. Guard against:
- Cherry-picking job postings that support your hypothesis while ignoring others
- Over-interpreting a single patent filing as a strategic shift
- Reading too much into earnings call tone without textual evidence
- Assuming technology adoption in GitHub means product commitment

Antidote: always document contradicting evidence alongside supporting evidence in the triangulation matrix.
