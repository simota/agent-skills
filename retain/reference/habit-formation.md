# Retain Habit Formation Design

Purpose: Hook Model design, streak rules, and habit-loop safeguards.
Contents: Hook Model template, reward taxonomy, investment choices, streak logic.

## Hook Model Template

```markdown
## Hook Model: [Feature/Behavior]

### 1. Trigger
**External triggers**
- Push notification at [time]
- Email digest on [day]
- Calendar reminder

**Internal triggers**
- Emotion: [situation] -> Product
- Routine: [existing routine] -> Product

### 2. Action
**Target behavior:** [smallest useful action]
**Motivation:** [why the user wants it]
**Ability:** [how easy it is]

### 3. Variable Reward
| Type | Example |
|------|---------|
| Tribe | Social response from others |
| Hunt | Discovery of something new |
| Self | Visible progress or skill gain |

### 4. Investment
Users invest one or more of:
- time
- data
- social graph
- learning effort
```

## Streak System Rules

| Situation | Rule |
|-----------|------|
| Same-day activity | No streak change |
| `daysDiff === 1` | Increment streak |
| `daysDiff === 2` and protection available | Consume 1 protection and continue |
| `daysDiff > 2` or no protection | Reset to `1` |
| Milestone reached | Award at `7`, `30`, `100`, `365` days |

## Streak UI Cues

- Show current streak.
- Show remaining streak protections when available.
- Show longest streak as a recovery anchor after a streak break.
