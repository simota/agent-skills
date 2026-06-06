# Anti-Drift Framework

Purpose: Use this file when the current step is losing focus, expanding scope, or attracting distractions.

## Contents

- Drift indicators
- Detection keywords
- Refocus prompt
- Yak-shaving prevention rules
- Parking Lot template

## Drift Indicators

| Signal | Pattern | Example |
| --- | --- | --- |
| Scope creep | “While I'm here, I should also...” | “Let me also refactor this class.” |
| Perfectionism | “It would be better if...” | “Let me add more edge cases first.” |
| Rabbit hole | “First I need to understand...” | “Let me read every doc first.” |
| Shiny object | “I noticed that...” | “There is a bug in the footer.” |
| Premature optimization | “This could be faster if...” | “Let me add caching first.” |

## Detection Keywords

Watch for:

```text
while I'm here
might as well
before I forget
quick detour
by the way
I noticed that
let me also
should probably
one more thing
real quick
```

## Refocus Prompt

```markdown
## Refocus Alert

**Current Step**: [Step Name]
**Detected**: [Drift type]
**Trigger**: "[user or self prompt]"

**Options**:
1. **Note and continue** (Recommended)
2. **Quick fix** (< 2 min)
3. **Pause and switch**

**Reminder**: The current step is [X]% complete.
```

## Yak-Shaving Prevention Rules

```text
1. New task appears -> add to backlog, do not start it
2. "Quick fix" > 2 min -> not quick, add it to Parking Lot
3. Current step < 80% complete -> finish it first
4. Unrelated to the current Epic -> definitely defer it
5. Truly blocked -> switch to a valid parallel task, not a random new one
```

## Parking Lot

```markdown
### Parking Lot

| Item | Source | Priority | Epic |
|------|--------|----------|------|
| "Footer bug" | Drift at 14:23 | P2 | New |
| "Add dark mode" | Drift at 15:01 | P3 | User Settings |
| "Refactor utils" | Drift at 15:30 | P2 | Tech Debt |
```
