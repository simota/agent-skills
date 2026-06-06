# Estimation & Planning Anti-Patterns

Purpose: Use this file when estimates, capacity plans, or sprint-level planning quality look distorted.

## Contents

- `EP-01` to `EP-07`
- `PP-01` to `PP-07`
- calibration and capacity rules
- execution pitfalls
- retrospective completion trap

## Estimation Anti-Patterns

| ID | Anti-pattern | Core issue | Preferred fix |
| --- | --- | --- | --- |
| `EP-01` | Solo Estimation | one person decides the estimate | estimate with the whole team |
| `EP-02` | Anchoring Bias | the first number dominates | reveal estimates simultaneously |
| `EP-03` | Time-Point Confusion | points are treated as hours | keep points relative, not time-based |
| `EP-04` | Velocity Obsession | velocity becomes a performance score | use velocity only for forecasting |
| `EP-05` | Safety Padding | personal buffer hides real uncertainty | use a separate team buffer of `15-20%` |
| `EP-06` | Estimation as Commitment | estimate becomes a promise | treat estimate as shared understanding |
| `EP-07` | Refinement Skip | vague backlog item is estimated anyway | refine before estimating |

## Planning Anti-Patterns

| ID | Anti-pattern | Core issue | Preferred fix |
| --- | --- | --- | --- |
| `PP-01` | Overcommitment Pressure | too much work is pushed into the plan | commit at about `80-85%` capacity |
| `PP-02` | Missing Sprint Goal | work is a random list, not a coherent goal | define one measurable goal |
| `PP-03` | Capacity Blindness | holidays, meetings, and interruptions are ignored | calculate available time honestly |
| `PP-04` | Last-Minute Items | unrefined work appears during planning | admit only prepared items |
| `PP-05` | Multi-Sprint Waterfall | detailed plans go too far ahead | use rolling-wave planning |
| `PP-06` | Plan Over Goal | the plan matters more than the outcome | adapt the plan to protect the goal |
| `PP-07` | Tech Debt Avoidance | only features are planned | reserve up to `20%` for debt reduction when needed |

## Best-Practice Rules

```text
Estimation:
- estimate only refined items
- include the full team
- reveal estimates simultaneously
- record why estimates changed

Calibration:
- compare estimate vs actual every sprint or session
- target accuracy ratio: 0.85-1.15
- adjust multipliers only after 3+ sprints or 3+ data points

Capacity:
- available time = workdays × hours/day - meetings - leave - interruption buffer
- commit at about 80-85% capacity
- include at least one retrospective improvement action when possible
```

## Execution Pitfalls

| Pitfall | Why it hurts | Countermeasure |
| --- | --- | --- |
| Cherry-Picking | easy tasks win, goal-critical work slips | prioritize by goal and critical path |
| Gold-Plating | scope expands during execution | enforce Definition of Done |
| Side-Gigs | invisible work bypasses the board | make all work visible |
| Hardening Sprint | quality is postponed | build quality into normal work |
| Variable Sprint Length | timebox is stretched | adjust scope, not the sprint |
| Everything's a Bug | normal work abuses the emergency lane | define bug severity clearly |

## Retrospective Completion Trap

- common completion rate is roughly `33%`
- root causes:
  - the action never enters the backlog
  - no owner exists
  - no follow-up happens

Use this rule:

```text
At each retrospective:
1. review the previous action first
2. convert each new action into a backlog item
3. assign owner, due point, and done criteria
4. record the impact after completion
```
