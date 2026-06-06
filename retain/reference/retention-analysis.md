# Retain Retention Analysis Framework

Purpose: Cohort analysis, churn scoring, drop-off diagnosis, and retention reporting.
Contents: cohort template, risk signal scoring, churn tiers, recommended actions, report template.

## Cohort Retention Analysis Template

```markdown
## Retention Analysis: [Product/Feature]

### Cohort Retention Table
| Cohort | Week 0 | Week 1 | Week 2 | Week 4 | Week 8 | Week 12 |
|--------|--------|--------|--------|--------|--------|---------|
| Jan W1 | 100% | 42% | 35% | 28% | 22% | 18% |
| Jan W2 | 100% | 45% | 38% | 30% | 24% | 20% |
| Feb W1 | 100% | 48% | 40% | 32% | - | - |

### Key Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Day 1 Retention | [X%] | [Y%] | [Status] |
| Week 1 Retention | [X%] | [Y%] | [Status] |
| Month 1 Retention | [X%] | [Y%] | [Status] |
| Month 3 Retention | [X%] | [Y%] | [Status] |

### Drop-off Analysis
| Period | Drop-off % | Primary Reason | Intervention |
|--------|-----------|----------------|--------------|
| Day 0-1 | [X%] | [Reason] | [Action] |
| Day 1-7 | [X%] | [Reason] | [Action] |
| Week 1-4 | [X%] | [Reason] | [Action] |

### Retention Curve Shape
- Flattening point: Week [X]
- Target stable retention: [X%]
```

## Churn Risk Scoring

| Signal | Threshold | Score impact | Interpretation |
|--------|-----------|--------------|----------------|
| Inactivity | `> 14 days` | `+30` | Severe dormancy |
| Inactivity | `> 7 days` | `+15` | Early dormancy |
| Usage decline | `sessionsLast7Days < 50%` of recent baseline | `+25` | Fast engagement drop |
| Feature adoption | `featureUsageScore < 30` | `+20` | Core value not adopted |
| Support issues | `supportTicketsOpen > 2` | `+15` | Unresolved friction |
| NPS | `<= 6` | `+20` | Detractor risk |
| Billing | `billingIssues = true` | `+25` | Payment friction |

## Churn Levels And Default Actions

| Score | Level | Default action |
|-------|-------|----------------|
| `>= 70` | Critical | Immediate 1:1 follow-up |
| `50-69` | High | Personalized re-engagement |
| `30-49` | Medium | Automated re-engagement campaign |
| `< 30` | Low | Continue normal engagement |

## Implementation Notes

- Combine behavior, satisfaction, and billing signals; do not rely on a single flag.
- Use the scoring table as a prioritization tool, not as a replacement for segment context.
- Escalate faster when inactivity and unresolved support issues appear together.

## Report Template

```markdown
## Retention Analysis: [Product/Feature]

### Cohort Retention Table
| Cohort | Week 0 | Week 1 | Week 2 | Week 4 | Week 8 | Week 12 |
|--------|--------|--------|--------|--------|--------|---------|
| [Cohort] | 100% | [X%] | [X%] | [X%] | [X%] | [X%] |

### Key Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Day 1 Retention | [X%] | [Y%] | [Status] |
| Week 1 Retention | [X%] | [Y%] | [Status] |
| Month 1 Retention | [X%] | [Y%] | [Status] |
| Month 3 Retention | [X%] | [Y%] | [Status] |

### Drop-off Analysis
| Period | Drop-off % | Primary Reason | Intervention |
|--------|-----------|----------------|--------------|
| [Period] | [X%] | [Reason] | [Action] |

### Churn Risk Priorities
| Segment | Score | Level | Top Signals | Action |
|---------|-------|-------|-------------|--------|
| [Segment] | [X] | [Level] | [Signals] | [Action] |
```
