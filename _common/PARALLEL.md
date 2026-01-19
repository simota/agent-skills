# Parallel Execution Protocol

This document defines the protocol for parallel task execution in AUTORUN_FULL mode.

---

## Overview

Parallel execution enables independent tasks to run simultaneously, reducing total execution time.
Only available in `NEXUS_AUTORUN_FULL` mode.

---

## Parallelization Criteria

### Tasks CAN be parallelized when:
- No data dependencies between tasks
- No shared file modifications
- No sequential ordering requirements
- Each task has clear, isolated scope

### Tasks CANNOT be parallelized when:
- Task B requires output from Task A
- Both tasks modify the same file
- Tasks share mutable state
- One task must validate another's output

---

## Parallel Execution Architecture

### Fan-out/Fan-in Pattern

```
                    ┌─────────────┐
                    │   PREPARE   │
                    │  (snapshot) │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Branch A │ │ Branch B │ │ Branch C │
        │  (Agent) │ │  (Agent) │ │  (Agent) │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
              │            │            │
              └────────────┼────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  AGGREGATE  │
                    │   (merge)   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   VERIFY    │
                    └─────────────┘
```

---

## Branch Definition

### _PARALLEL_BRANCHES Structure

```yaml
_PARALLEL_BRANCHES:
  fork_point:
    snapshot_id: [context snapshot ID]
    step: [X/Y]

  branches:
    - branch_id: A
      description: [What this branch does]
      chain: [Agent1, Agent2]
      files_owned: [file1.ts, file2.ts]
      estimated_steps: [N]
      guardrail_level: [L1|L2|L3]

    - branch_id: B
      description: [What this branch does]
      chain: [Agent3]
      files_owned: [file3.ts]
      estimated_steps: [N]
      guardrail_level: [L1|L2|L3]

  merge_point:
    agent: [Agent name for merge verification]
    strategy: [CONCAT|RESOLVE|MANUAL]

  conflict_resolution:
    on_file_conflict: [FAIL|RESOLVE|ESCALATE]
    on_test_failure: [RETRY|ROLLBACK|ESCALATE]
```

---

## File Ownership

Each branch has exclusive ownership of specific files to prevent conflicts.

### Ownership Rules

1. **Exclusive Access**: Only one branch can modify a file
2. **Declared Upfront**: File ownership declared before execution
3. **Conflict = Escalation**: Undeclared file modification triggers L3 guardrail

### Ownership Declaration

```yaml
file_ownership:
  branch_A:
    - src/features/validation/*.ts
    - tests/validation/*.test.ts
  branch_B:
    - src/features/formatting/*.ts
    - tests/formatting/*.test.ts
  shared_read:
    - src/types/*.ts
    - src/utils/*.ts
```

---

## Branch States

| State | Description |
|-------|-------------|
| PENDING | Branch defined, not started |
| RUNNING | Branch executing |
| WAITING | Waiting for dependency (if any) |
| DONE | Branch completed successfully |
| FAILED | Branch failed, may retry |
| MERGED | Results merged into main context |

---

## Parallel State Management

### _PARALLEL_STATE Structure

```yaml
_PARALLEL_STATE:
  mode: PARALLEL
  total_branches: [N]
  active_branches: [N]
  completed_branches: [N]
  failed_branches: [N]

  branches:
    - id: A
      status: [PENDING|RUNNING|WAITING|DONE|FAILED|MERGED]
      current_step: [X/Y]
      current_agent: [Agent name]
      files_modified: [list]
      guardrail_events: [list]
      error: [error details if FAILED]

    - id: B
      status: [...]
      ...

  merge_status:
    ready: [true|false]
    conflicts: [list of conflicts]
    resolution: [PENDING|RESOLVED|ESCALATED]
```

---

## Merge Strategies

### CONCAT (Default)
- Combine all changes from all branches
- No overlapping files expected
- Fail if conflicts detected

### RESOLVE
- Attempt automatic conflict resolution
- Use last-modified-wins for non-critical files
- Escalate for critical files (types, configs)

### MANUAL
- Pause execution
- Present conflicts to user
- Wait for resolution instructions

---

## Conflict Detection

### Before Merge

```yaml
_CONFLICT_CHECK:
  files:
    - path: src/types/index.ts
      modified_by: [A, B]
      conflict_type: BOTH_MODIFIED
      resolution: ESCALATE

    - path: src/utils/helper.ts
      modified_by: [A]
      conflict_type: NONE
      resolution: ACCEPT
```

### Resolution Actions

| Conflict Type | Resolution |
|---------------|------------|
| NONE | Accept change |
| ONLY_A | Accept A's version |
| ONLY_B | Accept B's version |
| BOTH_MODIFIED | Escalate (L3 guardrail) |
| DELETED_MODIFIED | Escalate |

---

## Guardrails in Parallel Execution

### Per-Branch Guardrails
Each branch has independent guardrail monitoring:
- L1/L2 events are logged but don't affect other branches
- L3 event pauses only that branch
- L4 event triggers global abort

### Global Guardrails
Some events affect all branches:
- Critical security issue → Abort all
- Shared dependency failure → Pause all
- Build failure at merge → Rollback all

---

## Rollback in Parallel Mode

### Per-Branch Rollback
```yaml
_BRANCH_ROLLBACK:
  branch_id: A
  reason: [test_failure|conflict|error]
  rollback_to: [fork_point snapshot]
  action: [RETRY|SKIP|ESCALATE]
```

### Global Rollback
```yaml
_GLOBAL_ROLLBACK:
  reason: [merge_failure|critical_error]
  rollback_to: [pre-parallel snapshot]
  branches_affected: [all]
  action: [SEQUENTIAL_RETRY|ABORT]
```

---

## Example: Parallel Feature Implementation

### Scenario
Add email validation AND phone validation (independent features)

### Branch Setup
```yaml
_PARALLEL_BRANCHES:
  fork_point:
    snapshot_id: ctx_001
    step: 2/7

  branches:
    - branch_id: email
      description: Email validation feature
      chain: [Builder, Radar]
      files_owned:
        - src/validators/email.ts
        - tests/validators/email.test.ts
      guardrail_level: L2

    - branch_id: phone
      description: Phone validation feature
      chain: [Builder, Radar]
      files_owned:
        - src/validators/phone.ts
        - tests/validators/phone.test.ts
      guardrail_level: L2

  merge_point:
    agent: Radar
    strategy: CONCAT
```

### Execution Flow
```
1. PREPARE: Create snapshot ctx_001
2. FORK: Start email branch AND phone branch
3. EXECUTE:
   - email: Builder → Radar (parallel)
   - phone: Builder → Radar (parallel)
4. WAIT: All branches complete
5. AGGREGATE: Merge results (CONCAT)
6. VERIFY: Run full test suite (Radar)
7. DELIVER: Report combined changes
```

---

## Agent HANDOFF in Parallel Mode

When agent is part of parallel branch:

```text
## NEXUS_HANDOFF
- Step: [X/Y]
- Branch: email           # Required in parallel mode
- Agent: Builder
- Summary: Implemented email validation
- Files Modified:
  - src/validators/email.ts (created)
  - tests/validators/email.test.ts (created)
- Guardrail Events:
  - Level: none
- Context Delta:
  - Added: email_validator_complete
- Next action: CONTINUE
```

---

## Parallel Execution Limits

| Metric | Limit | Reason |
|--------|-------|--------|
| Max branches | 4 | Complexity management |
| Max steps per branch | 5 | Context preservation |
| Max total parallel steps | 15 | Resource constraints |

---

## When NOT to Use Parallel

- Task has many interdependencies
- Files overlap significantly
- Sequential validation required
- Total steps < 4 (overhead not worth it)
- High-risk changes (prefer sequential with checkpoints)
