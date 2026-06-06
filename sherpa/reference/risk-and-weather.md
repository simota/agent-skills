# Risk Assessment & Weather System

Purpose: Use this file when Sherpa needs structured risk assessment, weather thresholds, or fatigue-aware pacing.

## Contents

- Risk categories
- Risk levels
- Risk assessment template
- Weather system
- Fatigue detection

## Risk Categories

| Category | Description |
| --- | --- |
| Technical | new technology, complex logic, unfamiliar patterns |
| Blocker | external dependencies, approvals, third-party APIs |
| Scope | unclear requirements, likely scope creep |
| Time | underestimation, hidden complexity, unknown unknowns |

## Risk Levels

| Level | Guidance |
| --- | --- |
| Low | proceed normally |
| Medium | monitor closely, keep fallback ready |
| High | investigate first, consider alternatives or specialist support |

## Risk Assessment Template

```markdown
### Risk Assessment: [Epic Name]

| Step | Risk Level | Category | Risk | Mitigation |
|------|------------|----------|------|------------|
| 1 | Low | - | Standard task | - |
| 2 | Medium | Technical | New API pattern | Review docs first |
| 3 | High | Blocker | External API unstable | Mock fallback ready |

**Overall Risk**: Medium
**High Risk Steps**: Step 3
**Recommended**: Scout investigation before Step 3
```

## Mitigation Strategies

| Risk type | Preferred actions |
| --- | --- |
| Technical | spike first, time-box exploration, involve the right specialist |
| Blocker | identify early, prepare mock/stub fallback, communicate dependency risk |
| Scope | define MVP explicitly, investigate unclear requirements, get written confirmation |
| Time | split smaller, add buffer, identify cut points before running late |

## Weather System

| Indicator | Clear | Cloudy | Stormy | Dangerous |
| --- | --- | --- | --- | --- |
| Velocity | on or ahead of estimate | `10-20%` slower | `20-50%` slower | `>50%` slower |
| Risk accumulation | `0-1` high-risk steps | `2` high-risk steps | `3+` high-risk steps | cascading risks |
| Blockers | none | `1` manageable | multiple | critical path blocked |
| Scope changes | none | minor additions | significant growth | uncontrolled growth |
| User energy | focused | normal | fatigued signals | frustrated or stuck |

### Weather Report

```markdown
## Weather Report

**Current Conditions**: Clear / Cloudy / Stormy / Dangerous
**Trend**: Improving / Stable / Degrading

| Indicator | Status | Notes |
|-----------|--------|-------|
| Velocity | On track, 12 min/step (est: 15) | Ahead of schedule |
| Risk level | 2 high-risk pending | Step 4 & 7 |
| Blockers | None | - |
| Scope | Stable | No changes |
| Energy | 3h into session | Consider break soon |
```

### Weather-Based Decisions

| Condition | Guidance |
| --- | --- |
| Clear | proceed at full speed; slightly larger steps are acceptable |
| Cloudy | stay on normal-sized steps and address warnings early |
| Stormy | slow down, use smaller steps, commit frequently |
| Dangerous | stop new feature work; assess retreat or escalation |

## Fatigue Detection

| Signal | Pattern | Response |
| --- | --- | --- |
| Increasing errors | same mistake `2+` times | suggest a break |
| Slowing velocity | steps take `2x` longer | reduce step size |
| Drift frequency | `3+` drift alerts in `30 min` | run a focus check |
| Frustration language | “This is annoying” | simplify and stabilize |
| Long silence | no progress for `15+ min` | check in gently |

### Rest Stop Suggestion

```markdown
## Rest Stop Suggestion

You've been climbing for 2.5 hours and completed 6 steps.

Options:
1. Quick break (5 min)
2. Commit checkpoint
3. Switch to an easier parallel task
4. Push through if the deadline truly requires it

Your current step is 80% done.
```
