# Progress Tracking

Purpose: Use this file when Sherpa needs dashboards, stalled detection, dependency analysis, retrospectives, or pace adjustment rules.

## Contents

- Epic dashboard
- Stalled progress detection
- Task tool integration
- Dependency graph
- Velocity tracking
- Retrospectives
- Adaptive pacing

## Epic Dashboard

```markdown
## Epic Dashboard: [Name]

**Started**: YYYY-MM-DD HH:MM
**Elapsed**: X hours Y minutes
**Status**: On Track | Behind | Blocked

### Progress
[========....................] 40% (4/10 steps)

### Velocity
- Completed: 4 steps in 45 min
- Average: 11 min/step
- Projected completion: 1h 15m remaining

### Steps
| # | Step | Size | Est | Actual | Status |
|---|------|------|-----|--------|--------|
| 1 | Define types | S | 10m | 8m | Done |
| 2 | API mock | M | 20m | 25m | Done |
| 3 | UI skeleton | M | 20m | 12m | Done |
| 4 | Form logic | S | 15m | - | In Progress |

### Commits
- `abc123` feat(payment): add payment types

### Blockers
- None currently

### Drift Log
- 14:23 - "Also fix footer" -> Added to backlog
```

## Stalled Progress Detection

| Condition | Threshold | Response |
| --- | --- | --- |
| No progress | `> 30 min` on one step | prompt for help or further decomposition |
| Repeated attempts | same step `3x` | suggest `Scout` investigation |
| Blocked | external dependency | switch to a valid parallel task |
| Overwhelmed | user reports being stuck | shrink the step |

### Stalled Response

```markdown
## Progress Check

**Current Step**: [Step Name]
**Time on Step**: 35 minutes

**What might help?**
1. Break down further
2. Scout investigation
3. Pair with a specialist
4. Take a short break
5. Skip to a valid parallel task
```

## Task Tool Integration

Sherpa persists progress with Claude Code task tools.

### Lifecycle

```text
TaskCreate (pending) -> TaskUpdate (in_progress) -> TaskUpdate (completed)
```

### Metadata Example

```typescript
TaskCreate({
  subject: "Define PaymentProps interface",
  description: "Create TypeScript interface for payment form props",
  activeForm: "Defining PaymentProps interface",
  metadata: {
    epicId: "payment-flow",
    stepNumber: 1,
    riskLevel: "green",
    estimatedMinutes: 10,
    agent: "Builder",
    parallelWith: [],
    blockedBy: []
  }
})
```

## Resume Template

```markdown
## Resuming Expedition

**Epic**: Payment Flow
**Last Session**: 2 hours ago
**Progress**: 4/10 steps completed

### Where We Left Off
- Step 5 was in progress
- Steps 6-10 pending

**Resume Options**:
1. Continue Step 5 (Recommended)
2. Review completed work
3. Re-plan the remaining work
```

## Dependency Analysis

| Type | Symbol | Meaning |
| --- | --- | --- |
| Sequential | `->` | A must finish before B |
| Parallel | `||` | A and B can run together |
| Blocking | `X` | external blocker |
| Optional | `?` | can be skipped if time is tight |

```markdown
### Step Dependencies

| Step | Depends On | Blocks | Parallel With |
|------|------------|--------|---------------|
| 1 | - | 2, 3 | - |
| 2 | 1 | 4 | 3 |
| 3 | 1 | 4 | 2 |
| 4 | 2, 3 | 5 | - |

**Critical Path**: 1 -> 2 -> 4 -> 5
**Parallelizable**: 2 and 3
```

## Velocity Tracking

```markdown
### Velocity Analysis

**Session Stats**:
- Steps completed: 6
- Total time: 85 minutes
- Average: 14.2 min/step

**Calibration Factor**: 0.95x

| Step | Estimated | Actual | Delta |
|------|-----------|--------|-------|
| 1 | 10 min | 8 min | -20% |
| 2 | 15 min | 18 min | +20% |
| 3 | 10 min | 9 min | -10% |
```

## Retrospectives

### Full Retrospective

```markdown
## Session Retrospective

**Date**: YYYY-MM-DD
**Duration**: Xh Ym
**Epic**: [Name]

### Progress Summary
- Started at: Step N
- Ended at: Step M
- Completed: X steps
- Commits: Y

### Metrics
| Metric | Value | Notes |
|--------|-------|-------|
| Steps/hour | X | Above/below average |
| Avg step time | Y min | On/off estimate |
| Drift incidents | Z | Managed/unmanaged |
| Blockers | N | Resolved/pending |
```

### Quick Retro

```markdown
## Quick Retro

**Completed**: Steps X-Y
**Blocked by**: Nothing / [blocker]
**Tomorrow**: Start Step Z
**Note**: [Key observation]
```

## Adaptive Pacing

| Mode | When | Step size | Check-in frequency |
| --- | --- | --- | --- |
| Sprint | fresh, deadline pressure | normal (`10-15 min`) | after each step |
| Cruise | normal working mode | normal | every `2-3` steps |
| Recovery | after blocker or break | smaller (`5-10 min`) | after each step |
| Wind-down | end of session | smallest, clean stops | frequent |

```yaml
Increase step size when:
  - velocity > 1.2x estimate for 3+ steps
  - user requests a faster pace
  - work is simple and repetitive

Decrease step size when:
  - velocity < 0.8x estimate for 2+ steps
  - errors or drift are increasing
  - territory is unfamiliar
  - fatigue signals appear

Switch to Wind-down when:
  - session > 3 hours
  - user says "one more thing then done"
  - a natural stop point is near
```
