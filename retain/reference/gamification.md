# Retain Gamification Elements

Purpose: Gamification mechanics that reinforce value-based retention instead of vanity engagement.
Contents: badge examples, level system, loyalty program template, reward guardrails.

## Guardrails

- Use gamification only when the core behavior already creates real user value.
- Prefer progress, mastery, and recognition over pure reward extraction.
- Do not use points or streaks to hide weak product value.

## Badge Examples

| Badge ID | Example name | Criteria | Rarity |
|----------|--------------|----------|--------|
| `first_project` | Launch Pad | First project created | Common |
| `streak_7` | Weekly Warrior | `7-day` streak | Common |
| `streak_30` | Monthly Master | `30-day` streak | Rare |
| `power_user` | Power User | `featureUsageScore >= 90` | Rare |
| `community_helper` | Community Helper | Helped `10+` users | Epic |
| `og_member` | OG Member | Joined before a key date | Legendary |

## Progress Levels

| Level | Name | XP range | Example benefit |
|-------|------|----------|-----------------|
| 1 | Beginner | `0-99` | Core features |
| 2 | Rookie | `100-299` | Custom themes |
| 3 | Regular | `300-599` | Priority support |
| 4 | Expert | `600-999` | Beta access |
| 5 | Master | `1000+` | Community badge |

## Loyalty Program Template

```markdown
## Loyalty Program: [Program Name]

### Point Earning
| Action | Points | Frequency Limit |
|--------|--------|-----------------|
| Daily login | 10 | 1/day |
| Project created | 50 | Unlimited |
| Task completed | 5 | Unlimited |
| Referral | 500 | 10/month |
| Review submitted | 100 | 1 |
| 7-day streak | 70 | 1/week |

### Point Redemption
| Reward | Points | Description |
|--------|--------|-------------|
| 1 month free | 1000 | Premium month |
| Exclusive theme | 500 | Special UI theme |
| Streak protection | 200 | One protection charge |
| Premium trial | 300 | 7-day premium trial |

### Tier System
| Tier | Points/Year | Benefits |
|------|-------------|----------|
| Bronze | 0-999 | Core benefits |
| Silver | 1000-4999 | +10% bonus points |
| Gold | 5000-9999 | +20% bonus, priority support |
| Platinum | 10000+ | +30% bonus, exclusive features |
```
