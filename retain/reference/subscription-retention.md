# Retain Subscription Retention Strategies

Purpose: Cancellation flow design, save-offer ordering, and subscription retention reporting.
Contents: cancellation funnel, pause rules, offer matrix, selection logic, metrics template.

## Subscription Retention Flow

### Cancellation Funnel

| Step | Option | Expected conversion |
|------|--------|---------------------|
| 1 | Collect churn reason | `100%` required |
| 2 | Offer pause | `20-25%` accept |
| 3 | Offer downgrade | `15-20%` accept |
| 4 | Offer discount | `10-15%` accept |
| 5 | Complete cancellation and log reason | Remaining users |

### Pause Options

| Duration | Eligibility | Data retention | Reactivation rate |
|----------|-------------|----------------|-------------------|
| `1 month` | All users | Preserve all data | `70%+` |
| `2 months` | `6+ months` tenure | Preserve all data | `60%+` |
| `3 months` | `1+ year` tenure | Preserve all data | `50%+` |

### Save Offer Matrix

| Churn reason | Offer type | Discount | Duration |
|--------------|-----------|----------|----------|
| Price too high | Discount | `30%` | `3 months` |
| Budget cut | Downgrade | `-` | `-` |
| Cannot realize value | Training | Free | `-` |
| Temporary pause in need | Pause | `-` | `up to 3 months` |
| Competitor pressure | Special offer | `40%` | `6 months` |

## Offer Selection Rules

- First save attempt: start with pause.
- Price-driven churn:
  - always consider downgrade
  - add discount when tenure is `> 90 days`
  - use `30%` for high-value accounts, otherwise prefer smaller discounts
- Usage or feature frustration: offer training before discounts.
- Competitor-driven churn: only use the `40% / 6 months` offer for users with `> 180 days` tenure.

## Metrics Template

```markdown
## Subscription Retention Report: [Period]

### Cancellation Funnel Performance
| Step | Entries | Exits | Conversion |
|------|---------|-------|------------|
| Cancellation started | [N] | - | - |
| Pause accepted | [N] | [N saved] | [X%] |
| Downgrade accepted | [N] | [N saved] | [X%] |
| Discount accepted | [N] | [N saved] | [X%] |
| Cancellation completed | [N] | - | - |

### Save Offer Effectiveness
| Offer Type | Offered | Accepted | Rate | Revenue Saved |
|------------|---------|----------|------|---------------|
| Pause | [N] | [N] | [X%] | [Amount] |
| Downgrade | [N] | [N] | [X%] | [Amount] |
| Discount | [N] | [N] | [X%] | [Amount] |

### Pause Reactivation Tracking
| Pause Duration | Started | Reactivated | Rate |
|----------------|---------|-------------|------|
| 1 month | [N] | [N] | [X%] |
| 2 months | [N] | [N] | [X%] |
| 3 months | [N] | [N] | [X%] |
```
