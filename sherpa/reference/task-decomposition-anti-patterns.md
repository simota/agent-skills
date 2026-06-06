# Task Decomposition Anti-Patterns

Purpose: Use this file to validate decomposition quality during `MAP`, especially when steps are too large, too early, or structurally misleading.

## Contents

- `TD-01` to `TD-07`
- Decomposition signals
- Vertical vs horizontal slicing
- WBS checklist

## Anti-Patterns

| ID | Anti-pattern | Symptom | Fix |
| --- | --- | --- | --- |
| `TD-01` | God Task | many steps still exceed `15 min`; no clear test or commit point | keep decomposing to atomic steps |
| `TD-02` | Premature Decomposition | detailed plan before the requirements are clear | investigate first, then decompose gradually |
| `TD-03` | Skill-Based Splitting | “coding / testing / docs” slices create silos | prefer functional or component slices |
| `TD-04` | Template Addiction | every story gets the same boilerplate breakdown | let tasks emerge from the actual work |
| `TD-05` | Missing 100% Rule | hidden work appears later | explicitly check setup, tests, docs, and config |
| `TD-06` | Dependency Blindness | parallel work later proves serial | create a dependency graph during decomposition |
| `TD-07` | Over-Decomposition | `20+` tasks or status work dominates real work | regroup and reduce management overhead |

## Decomposition Signals

### Split Further When

- a step exceeds `15 min`
- the test method is unclear
- no clean commit point exists
- multiple files or modules are touched
- the step contains implicit sequencing such as “do X, then Y”

### Stop Splitting When

- work is under `5 min`
- the sub-step cannot be verified on its own
- tracking cost exceeds execution cost
- the current list already exceeds about `20` items

### Sweet Spot

- Epic -> `3-5` Stories
- Story -> `3-8` Tasks
- Task -> `2-4` Atomic Steps
- Atomic Step -> do not decompose further

## Vertical vs Horizontal Slicing

```text
Horizontal slice (bad):
- HTML for all screens
- CSS for all screens
- JS for all screens
- API for all endpoints

Vertical slice (good):
- Login form (HTML + CSS + JS + API + test)
- Validation (front + back + test)
- Error handling (UI + API + test)
```

Prefer vertical slices because each slice produces something testable and reviewable.

## Decomposition Checklist

Note: "WBS" (Work Breakdown Structure) terminology originates from waterfall project management. Sherpa uses output-focused decomposition aligned with agile vertical-slice practices (SAFe 6.0, INVEST). The checklist below retains useful structural rigor while dropping phase-gate assumptions.

```text
Before decomposition:
- goal and success criteria are clear
- out-of-scope is explicit
- assumptions are listed
- high-risk areas are known

During decomposition:
- 100% rule checked (no hidden work)
- tasks are mutually exclusive
- step size is 5-15 min
- each step is testable (single observable exit criterion)
- each step has a commit point
- dependencies are explicit
- owning agent is clear
- each item is a deliverable output, not an activity

After decomposition:
- critical path identified
- parallel work identified
- blocker candidates flagged
- risk buffer considered
- management overhead remains acceptable
```
