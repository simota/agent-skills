# Retain Re-engagement Triggers

Purpose: Trigger design, cadence limits, and reusable message structure for re-engagement.
Contents: trigger table, channel selection, delay rules, message examples.

## Trigger Configuration

| Trigger | Condition | Channel | Delay | Max frequency |
|---------|-----------|---------|-------|---------------|
| `dormant_3_days` | `3 <= daysSinceLastVisit < 7` | Push | `0h` | `4/month` |
| `dormant_7_days` | `7 <= daysSinceLastVisit < 14` | Email | `12h` | `2/month` |
| `incomplete_onboarding` | Onboarding incomplete and `>= 1 day` since signup | Email | `24h` | `3/month` |
| `feature_discovery` | `> 5` sessions and key feature unused | In-app | `0h` | `1/month` |
| `streak_at_risk` | Active streak and `< 6h` until expiry | Push | `0h` | `30/month` |

## Channel Rules

- Push: use for short-lived urgency, including early dormancy and streak protection.
- Email: use for recovery, incomplete setup, and higher-context value reminders.
- In-app: use for contextual feature discovery after a user has demonstrated core adoption.

## Message Patterns

```typescript
const templates = {
  miss_you_3_days: {
    title: 'We miss you',
    body: 'It has been 3 days since your last visit. Want to see what is new?',
    cta: 'Check it now'
  },
  win_back_7_days: {
    subject: '[Name], here is what changed',
    body: 'You have been away for a while. We shipped [feature] so you can now [benefit].',
    cta: 'See what is new'
  },
  complete_setup: {
    subject: 'You are almost done',
    body: 'Finish the remaining setup steps to unlock [benefit]. It should take about 5 minutes.',
    cta: 'Continue setup'
  },
  protect_streak: {
    title: 'Keep your streak alive',
    body: 'You are on a [N]-day streak. Use the product today to keep it going.',
    cta: 'Open the product'
  }
};
```
