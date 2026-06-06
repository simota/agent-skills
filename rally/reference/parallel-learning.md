# Parallel Learning (HARMONIZE)

> Purpose: Read this after team execution when evaluating performance, adapting defaults, or rolling back a bad adaptation.

## Table of Contents

1. HARMONIZE Workflow
2. Learning Triggers
3. Team Effectiveness Score
4. Team Design Matrix
5. Adaptation Rules
6. Safety Guardrails and Rollback
7. Integration and Templates

## HARMONIZE Workflow

```text
COLLECT -> EVALUATE -> EXTRACT -> ADAPT -> SAFEGUARD -> RECORD
```

| Phase | Purpose | Required output |
|-------|---------|-----------------|
| `COLLECT` | capture execution facts | `EXECUTION_DATA` |
| `EVALUATE` | compute performance | TES and grade |
| `EXTRACT` | identify patterns | composition, size, model, or ownership insight |
| `ADAPT` | propose default changes | bounded proposal with rationale and rollback |
| `SAFEGUARD` | verify safety | invariant checks, evidence check, snapshot |
| `RECORD` | persist learning | journal entry, Lore share, Judge data |

### `EXECUTION_DATA`

Capture after every team session:

```yaml
EXECUTION_DATA:
  session_id: <unique id>
  task_type: <feature | bugfix | refactor | migration | test>
  team_pattern: <Frontend+Backend | Feature_Parallel | Pipeline | Specialist_Team | Code+Test+Docs>
  team_size: <int>
  subagent_types:
    - name: <teammate name>
      type: <general-purpose | Explore | Plan>
      model: <sonnet | opus | haiku>
      role: <description>
  task_count: <int>
  completed_tasks: <int>
  retried_tasks: <int>
  ownership_conflicts: <int>
  total_file_ops: <int>
  timing:
    total_seconds: <int>
    estimated_sequential_seconds: <int>
  integration_checks:
    build_pass: <bool>
    tests_pass: <bool>
    lint_pass: <bool>
  user_interventions:
    - type: <team_size_override | composition_override | task_reassign | manual_fix | abort>
      detail: <description>
  final_status: <SUCCESS | PARTIAL | BLOCKED | FAILED>
```

## Learning Triggers

| ID | Condition | Scope | Actions |
|----|-----------|-------|---------|
| `RY-01` | every team execution completes | Lightweight | `COLLECT + EVALUATE` |
| `RY-02` | same team pattern fails or conflicts `3+` times | Full | all 6 phases |
| `RY-03` | user overrides team size or composition | Full | all 6 phases |
| `RY-04` | Judge sends quality feedback | Medium | `COLLECT + EVALUATE + EXTRACT + RECORD` |
| `RY-05` | Lore sends a parallel pattern update | Medium | `COLLECT + EVALUATE + EXTRACT + RECORD` |
| `RY-06` | `30+` days since the last full HARMONIZE cycle | Full | all 6 phases |

### Trigger Priority

1. `RY-03`
2. `RY-02`
3. `RY-04`
4. `RY-05`
5. `RY-06`
6. `RY-01`

## Team Effectiveness Score

```text
TES = Parallel_Efficiency x 0.30
    + Task_Economy x 0.20
    + Conflict_Prevention x 0.20
    + Integration_Quality x 0.20
    + User_Autonomy x 0.10
```

### Components

| Component | Weight | Definition |
|-----------|--------|------------|
| `Parallel_Efficiency` | `0.30` | `estimated_sequential_time / actual_parallel_time`, capped at `1.0` |
| `Task_Economy` | `0.20` | `completed_tasks / total_tasks x (1 - retry_rate)` |
| `Conflict_Prevention` | `0.20` | `1 - (conflicts / total_file_ops)` |
| `Integration_Quality` | `0.20` | `(build + tests + lint) / total_checks` |
| `User_Autonomy` | `0.10` | `1 - (user_overrides / total_decisions)` |

### Grading Scale

| Grade | TES range | Interpretation |
|-------|-----------|----------------|
| `A` | `>= 0.90` | excellent |
| `B` | `>= 0.80` | good, protect with approval |
| `C` | `>= 0.70` | acceptable adaptation target |
| `D` | `>= 0.60` | below standard |
| `F` | `< 0.60` | full review required |

### Data Requirements

- TES requires `>= 3` data points for the same task-type and team-pattern combination.
- Grades are provisional until `>= 5` data points.
- Trend analysis requires `>= 10` data points.
- Below the threshold, report `INSUFFICIENT_DATA`.

## Team Design Matrix

Use cumulative TES by task type:

```text
                 | feature | bugfix | refactor | migration | test |
Frontend+Backend |    —    |   —    |    —     |     —     |  —   |
Feature Parallel |    —    |   —    |    —     |     —     |  —   |
Pipeline         |    —    |   —    |    —     |     —     |  —   |
Specialist Team  |    —    |   —    |    —     |     —     |  —   |
Code+Test+Docs   |    —    |   —    |    —     |     —     |  —   |
```

`—` means `INSUFFICIENT_DATA`.

### Update Rules

1. Record the team-pattern and task-type outcome after each `RY-01`.
2. When a cell reaches `>= 3` data points, calculate the TES average and grade.
3. Prefer higher-graded patterns at design time.
4. If every pattern is `INSUFFICIENT_DATA`, fall back to `reference/team-design-patterns.md`.

## Adaptation Rules

### Allowed Scope by Grade

| Current grade | Allowed adaptations | Approval |
|---------------|---------------------|----------|
| `A` | no auto-change | human required |
| `B` | no auto-change | human required |
| `C` | team-size defaults, `subagent_type` preference tuning | auto with snapshot |
| `D` | size defaults, model heuristics, pattern recommendations | auto with snapshot |
| `F` | full review including pattern, size, model, and ownership reassessment | auto with snapshot |

### Adaptation Types

| Type | Example | Max per session |
|------|---------|-----------------|
| Team size default change | default to `3` for bugfix work | `2` |
| `subagent_type` preference | prefer `Explore` for refactor investigation | `1` |
| Model heuristic | use `opus` for complex migration design | `1` |
| Pattern recommendation | recommend `Pipeline` for migration tasks | `1` |
| Ownership refinement | split shared test directories | `1` |

Total maximum: `3` parameter default changes per session.

### Application Process

1. Propose the change with rationale, expected TES impact, and rollback plan.
2. Run `SAFEGUARD`.
3. Save a snapshot.
4. Apply the change.
5. Monitor the next `3` executions.

## Safety Guardrails and Rollback

| Mechanism | Rule |
|-----------|------|
| Change volume limit | maximum `3` parameter default changes per session |
| Auto-adaptation ceiling | `TES >= B` requires human approval |
| Rollback snapshot | save state before every adaptation |
| Diminishing returns | `3` consecutive TES improvements `< 0.02` -> pause HARMONIZE |
| Lore sync | extracted patterns must be sent to Lore |
| Minimum evidence | no adaptation with `< 3` execution data points |
| File ownership invariant | never modify the `exclusive_write` or `shared_read` protocol |

### Rollback Protocol

1. Detect regression: TES drops `>= 0.10` after adaptation, measured across the next `3` executions.
2. Load the pre-adaptation snapshot.
3. Restore previous defaults and heuristic state.
4. Record the rollback in `.agents/rally.md` with root cause analysis.
5. Share the rollback event to Lore as a negative pattern.

## Integration and Templates

### Integration Points

| Partner | Direction | Data exchanged |
|---------|-----------|----------------|
| Lore | Rally -> Lore | team composition patterns, TES trends, rollback events |
| Lore | Lore -> Rally | validated parallel patterns |
| Judge | Rally -> Judge | TES scores and completion quality |
| Judge | Judge -> Rally | `QUALITY_FEEDBACK` |

### Lore Sync Protocol

```yaml
RALLY_TO_LORE_PATTERN:
  type: PARALLEL_EXECUTION_PATTERN
  pattern_name: <descriptive name>
  source_data:
    task_type: <task type>
    team_pattern: <team pattern>
    team_size: <int>
    sample_size: <int>
    tes_impact: <float>
  pattern_detail: <description>
  confidence: <HIGH | MEDIUM | LOW>
  actionable: <bool>
```

```yaml
LORE_TO_RALLY_PATTERN:
  type: PARALLEL_PATTERN_UPDATE
  pattern_name: <descriptive name>
  source_agents: <list of contributing agents>
  recommendation: <action to consider>
  priority: <HIGH | MEDIUM | LOW>
```

### Session Feedback Record

```markdown
## Team Session Feedback — <session_id>

**Date:** YYYY-MM-DD
**Task Type:** <feature | bugfix | refactor | migration | test>
**Team Pattern:** <Frontend+Backend | Feature_Parallel | Pipeline | Specialist_Team | Code+Test+Docs>
**Team Size:** <int> | **Subagent Types:** <type list> | **Models:** <model list>
**Final Status:** <SUCCESS | PARTIAL | BLOCKED | FAILED>
**TES:** <score> (Grade: <A-F>) | **Previous TES:** <score> (Grade: <A-F>)
```

### Team Profile Update

```markdown
## Team Profile Update — <date>

**Team Pattern:** <pattern name>
**Task Type:** <task type>
**Previous Grade:** <grade or INSUFFICIENT_DATA>
**New Grade:** <grade>
**Data Points:** <count>
```

### Adaptation Log

```markdown
## Adaptation Log — <date>

**Trigger:** <RY-xx>
**Current TES:** <score> (Grade: <grade>)
**Target TES:** <expected score>

### Safeguard Check
- File ownership invariant: PASS / FAIL
- Evidence threshold (>= 3): PASS / FAIL
- Grade ceiling check: PASS / FAIL
- Snapshot saved: <snapshot identifier>

### Outcome
- TES after 3 executions: <score>
- Rollback needed: YES / NO
```
