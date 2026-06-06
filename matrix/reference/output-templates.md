# Output Templates

Purpose: Use this file when the result must be handed to another agent or converted into a reusable execution artifact.

## Contents

- Standard matrix plan
- Risk matrix
- Deploy matrix
- UX matrix
- Experiment matrix
- Coverage report

## Standard Matrix Plan

Use for all domains unless a domain-specific format is clearly better.

```markdown
## Matrix Plan: [domain] — [name]

### Combination Space Summary
- Axes: browser(3) × os(2) × auth(2)
- Original combinations: 12
- Method: Pairwise
- Optimized combinations: 4
- Reduction rate: 67%
- Coverage guarantee: 2-way 100%

### Execution Set
| # | browser | os | auth | Priority | Covered tuples |
|---|---|---|---|---|---|
| 1 | Chrome | Windows | logged_in | HIGH | ... |

### Constraints And Warnings
- Excluded: Safari × Windows
- Ask-first items:
- Uncovered tuples due to budget:

### Suggested Handoff
- Next agent:
- Why:
- Payload summary:
```

## Risk Matrix

Use when ranking threat combinations.

```markdown
## Risk Matrix: [name]

### Combination Space
- Axes:
- Original combinations:
- Optimized combinations:

### Ranked Risk Set
| # | Threat | Surface | Auth level | Risk score | Priority |
|---|---|---|---|---|---|
| 1 | SQLi | API | anonymous | 9.8 | P0 |
```

## Deploy Matrix

Use when rollout order matters.

```markdown
## Deploy Matrix: [name]

### Rollout Order
| Order | Environment | Region | Version | Traffic | Validation |
|---|---|---|---|---|---|
| 1 | staging | ap-northeast-1 | v1.5.1 | 100% | smoke checks |

### Rollback Triggers
- Error-rate threshold:
- Latency threshold:
- Stop conditions:
```

## UX Matrix

Use when handing off to Echo, Cast, or Researcher.

```markdown
## UX Matrix: [name]

### Coverage Set
| # | Persona | Device | Scenario | Validation focus |
|---|---|---|---|---|
| 1 | beginner | mobile | first_visit | drop-off points |
```

## Experiment Matrix

Use when handing off to Experiment or Pulse.

```markdown
## Experiment Matrix: [name]

### Variant Set
| # | Variable A | Variable B | Segment | Duration | KPI |
|---|---|---|---|---|---|
| 1 | blue CTA | short copy | new_users | 2 weeks | CTR, CVR |
```

## Coverage Report

Use after execution results are available.

```markdown
## Coverage Report: [name]

### Result Summary
| Metric | Planned | Actual |
|---|---:|---:|
| Total | 9 | 9 |
| Passed | - | 7 |
| Failed | - | 2 |
| Skipped | - | 0 |

### Coverage Impact
- Missing tuples caused by failures:
- Recovery target:
- Suggested supplemental cases:

### Model Feedback
- Need finer values:
- Need more axes:
- Need higher strength:
```

## Handoff Minimum

Always include:

- domain
- axes and value counts
- original count
- optimized count
- reduction rate
- method
- coverage guarantee
- constraints
- warnings
- next agent
