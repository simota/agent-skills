# Retain Onboarding Optimization

Purpose: Activation milestone design, time-to-value reduction, and onboarding retention analysis.
Contents: milestone thresholds, TTV targets, progressive disclosure, nudges, report template.

## Activation Framework

### Activation Milestones

| Milestone | Target time | Success criteria | D30 impact |
|-----------|-------------|------------------|------------|
| `M0: Account created` | `T+0` | Email verified | Baseline |
| `M1: Profile complete` | `T+5 min` | Required fields completed | `+8%` |
| `M2: First action` | `T+24h` | One core action completed | `+15%` |
| `M3: Value moment` | `T+3 days` | Artifact created or goal achieved | `+25%` |
| `M4: Habit forming` | `T+7 days` | Active on `3+` days | `+35%` |
| `M5: Established` | `T+14 days` | Uses product `2+` times per week | `+45%` |

### Time-to-Value Targets

| Segment | Current TTV | Target TTV | Strategy |
|---------|-------------|------------|----------|
| New user | [X min] | [Y min] | Templates and starter defaults |
| Invited user | [X min] | [Y min] | Preset configuration |
| Trial user | [X min] | [Y min] | Guided tour |
| New paid user | [X min] | [Y min] | 1:1 onboarding |

### Progressive Disclosure Schedule

| Week | Available features | Introduction method |
|------|--------------------|---------------------|
| Week 1 | Core features only | Tutorial |
| Week 2 | + intermediate features | Tooltips |
| Week 3 | + advanced features | Feature introduction |
| Week 4+ | Full feature set | Help center and contextual help |

## Onboarding Nudges

| Trigger | Channel | Delay |
|---------|---------|-------|
| Profile incomplete | In-app | `1h` |
| No first action | Email | `24h` |
| No value moment | Email | `72h` |
| Habit-risk | Push | `120h` |

## Report Template

```markdown
## Onboarding Performance Report: [Period]

### Funnel Overview
| Milestone | Reached | Conversion | Avg Time | Target Time |
|-----------|---------|------------|----------|-------------|
| Account created | [N] | 100% | - | - |
| Profile complete | [N] | [X%] | [X] min | 5 min |
| First action | [N] | [X%] | [X] h | 24 h |
| Value moment | [N] | [X%] | [X] d | 3 d |
| Habit forming | [N] | [X%] | [X] d | 7 d |
| Established | [N] | [X%] | [X] d | 14 d |

### Onboarding -> Retention Correlation
| Completed Milestones | D7 Retention | D30 Retention |
|---------------------|--------------|---------------|
| 0-1 | [X%] | [X%] |
| 2-3 | [X%] | [X%] |
| 4-5 | [X%] | [X%] |
| 6 (All) | [X%] | [X%] |

### Improvement Opportunities
1. Biggest drop-off: M[X] -> M[Y] ([Z%])
2. Slowest transition: M[X] -> M[Y] ([Z] hours)
```
