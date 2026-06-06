# Compete Playbooks Reference

Purpose: Use this file when Compete must recommend a response, arm sales, analyze deal outcomes, or run an alert workflow.

## Contents

- Competitive response
- Battle card
- Win/loss
- Alert system

## Competitive Response

```markdown
## Competitive Response: [Competitor Action]

### What Happened
- Competitor: [Name]
- Action: [What they did]
- Date: [When]
- Impact: [How it affects us]

### Assessment
| Factor | Rating | Notes |
|---|---|---|
| Urgency | High/Med/Low | [...] |
| Customer Impact | High/Med/Low | [...] |
| Differentiation Impact | High/Med/Low | [...] |

### Response Options
| Option | Pros | Cons | Effort | Recommendation |
|---|---|---|---|---|
| Option 1 | [...] | [...] | H/M/L | Yes/No |
| Option 2 | [...] | [...] | H/M/L | Yes/No |
| Do Nothing | [...] | [...] | Low | Yes/No |

### Recommended Response
[Clear action]

### Timeline
- [Date]: [Action]
- [Date]: [Action]
```

Decision rule:
- prefer a value-positioning response over a parity response unless evidence shows a meaningful win-rate gap.

## Battle Card

Use this when sales, CS, or leadership needs fast competitive talking points.

```markdown
## Battle Card: [Competitor Name]

### 30-Second Summary
[Why choose us]

### Their Strengths
- [Strength] - [How to acknowledge/respond]

### Their Weaknesses
- [Weakness] - [Our advantage]

### Common Objections and Responses
| Objection | Response |
|---|---|
| "They are cheaper" | "[TCO / ROI / hidden costs]" |
| "They have feature X" | "[Alternative / roadmap / why it matters less]" |
| "They are the standard" | "[Why the standard is not the best fit]" |
| "Switching is hard" | "[Migration support / time-to-value]" |

### Killer Questions
1. [...]
2. [...]
3. [...]

### Success Story
- Customer: [...]
- Challenge: [...]
- Why we won: [...]
- Result: [...]

### Quick Stats
| Metric | Us | Competitor |
|---|---|---|
| Deployment time | [...] | [...] |
| Support response | [...] | [...] |
| Uptime | [...] | [...] |
| Satisfaction | [...] | [...] |
```

## Win/Loss

```markdown
## Win/Loss Analysis: [Deal Name]

### Deal Summary
| Field | Value |
|---|---|
| Result | Win / Loss |
| Competitor(s) | [...] |
| Deal Size | ¥[...] |
| Sales Cycle | [...] |
| Decision Date | [...] |

### Decision Factors
| Factor | Weight | Our Score | Competitor Score | Winner |
|---|---:|---:|---:|---|
| Price | 1-5 | [...] | [...] | Us/Them |
| Features | 1-5 | [...] | [...] | Us/Them |
| UX | 1-5 | [...] | [...] | Us/Them |
| Support | 1-5 | [...] | [...] | Us/Them |
| Integration | 1-5 | [...] | [...] | Us/Them |
| Brand/Trust | 1-5 | [...] | [...] | Us/Them |

### Decision-Maker Insights
- Primary decision maker: [...]
- Influencers: [...]
- Buying criteria: [...]
- Objections: [...]

### Key Learnings
- What worked: [...]
- What failed: [...]
- Competitor tactics: [...]
- Actionable insight: [...]

### Follow-up Actions
- [ ] [...]
- [ ] [...]
```

## Alert System

### Alert Bands

| Band | Cadence | Trigger examples |
|---|---|---|
| High | immediate | funding, overlapping feature release, `10%+` price cut, executive move, acquisition, major customer win, major security incident |
| Medium | weekly review | integrations, campaigns, case studies, major changelog, whitepaper, regional expansion |
| Low | monthly review | hiring shifts, redesigns, social mentions, events |

### Sources

| Source | Frequency | Tier | Notes |
|---|---|---|---|
| Competitor websites | weekly | 1 | messaging, product, pricing |
| Crunchbase / LinkedIn | weekly | 2 | funding, hiring, executives |
| Review sites | weekly | 2 | sentiment and complaints |
| Google Alerts | daily | 2-3 | automated signal |
| Social media | daily | 3 | campaign and messaging shifts |
| Industry news | daily | 2 | partnership, acquisition, regulatory news |

> Tier column maps to `intelligence-gathering.md#source-tiers`. Use tier when scoring alert reliability and resolving conflicting signals.

### Alert Response

```markdown
## Alert Response: [Alert Name]

### Alert Details
- Date Detected: [...]
- Competitor: [...]
- Type: [...]
- Source: [...]

### Impact Assessment
| Dimension | Score (1-5) | Notes |
|---|---:|---|
| Customer Impact | [...] | [...] |
| Revenue Impact | [...] | [...] |
| Competitive Position | [...] | [...] |
| Urgency | [...] | [...] |
| Total | [Sum/20] | |

### Decision
- Immediate action
- Scheduled response
- Monitor only
- No action

### Action Plan
| Action | Owner | Deadline | Status |
|---|---|---|---|
| [...] | [...] | [...] | [...] |
```

Rule:
- any High alert must produce either a response decision or an explicit monitor-only rationale.
