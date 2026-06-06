# Retain Customer Health Score

Purpose: Multi-signal health scoring, trend detection, and account triage.
Contents: weighted dimensions, thresholds, trend rules, implementation notes, portfolio report template.

## Health Score Framework

| Dimension | Weight | Example signals | Calculation cue |
|-----------|--------|-----------------|-----------------|
| Usage frequency | `25%` | DAU/MAU, session count, recency | `(actual / expected) * 25` |
| Feature depth | `20%` | feature coverage, core feature usage, advanced usage | `(featuresUsed / totalFeatures) * 20` |
| Engagement | `20%` | session duration, actions, created content | `engagementPercentile * 20` |
| Satisfaction | `15%` | NPS, CSAT, CES, support satisfaction | `(satisfactionAvg / 5) * 15` |
| Growth | `10%` | seats added, plan upgrade, usage growth | `growthIndicator * 10` |
| Relationship | `10%` | resolved support, community activity, referrals | `relationshipScore * 10` |

## Health Score Thresholds

| Score | Status | Meaning | Default action |
|-------|--------|---------|----------------|
| `80-100` | Healthy | Active and satisfied | Upsell, referral, advocacy |
| `60-79` | Stable | Consistent usage | Monitor and reinforce value |
| `40-59` | At Risk | Churn signals are visible | Start automated intervention |
| `0-39` | Critical | Immediate retention risk | Human intervention |

## Health Trend Rules

| Trend | Definition | Response |
|-------|------------|----------|
| Improving | `+10 pts/month or more` | Record as a success pattern |
| Stable | `within +/-5 pts/month` | Maintain and reinforce value |
| Declining | `-10 pts/month or more` | Early intervention and diagnosis |
| Rapid decline | `-20 pts/month or more` | Immediate escalation |

## Implementation Notes

- Normalize each dimension before applying the weight.
- Compare score movement against the previous period; the trend often matters more than the absolute score.
- Use alert lists to explain *why* an account is at risk, not just *that* it is at risk.

## Report Template

```markdown
## Customer Health Report: [Period]

### Portfolio Overview
| Status | Count | % | MRR | Trend |
|--------|-------|---|-----|-------|
| Healthy | [N] | [X%] | [Amount] | [Trend] |
| Stable | [N] | [X%] | [Amount] | [Trend] |
| At Risk | [N] | [X%] | [Amount] | [Trend] |
| Critical | [N] | [X%] | [Amount] | [Trend] |

### At-Risk Accounts
| Customer | Score | Trend | Top Alert | Owner |
|----------|-------|-------|-----------|-------|
| [Name] | [X] | [Trend] | [Alert] | [Owner] |

### Dimension Analysis
| Dimension | Avg Score | Lowest Segment | Action |
|-----------|-----------|----------------|--------|
| Usage frequency | [X] | [Segment] | [Action] |
| Feature depth | [X] | [Segment] | [Action] |
| Engagement | [X] | [Segment] | [Action] |
| Satisfaction | [X] | [Segment] | [Action] |
| Growth | [X] | [Segment] | [Action] |
| Relationship | [X] | [Segment] | [Action] |
```
