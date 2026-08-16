# Parallel Execution Protocol

This document defines the protocol for parallel task execution in AUTORUN_FULL mode.

---

## Overview

Parallel execution enables independent tasks to run simultaneously, reducing total execution time.
Only available in `NEXUS_AUTORUN_FULL` mode.

### Execution Layer Selection

| Condition | Layer | Method |
|-----------|-------|--------|
| 2-3 independent branches, clear file ownership | **L2: Parallel Spawn** | `Agent(run_in_background: true)` per branch |
| 4+ workers, complex ownership, multi-step branches | **L3: Rally Delegation** | `Agent(Rally)` manages team |

**L2 Parallel Spawn**: Nexus spawns each branch as a background Agent. Each agent reads its own SKILL.md and works independently. Nexus waits for completion notifications, then aggregates.

**L3 Rally Delegation**: Nexus spawns Rally as a single Agent. Rally handles all team management using Agent Teams API.

See `_common/AUTORUN.md` for full execution layer details.

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

### Net Parallel Benefit (decide before fanning out)

The criteria above are necessary, not sufficient: work can be perfectly independent and still lose money in parallel. Estimate the balance before spawning:

```
Net Parallel Benefit
  = Saved cycle time
  + Coverage gain (perspectives a single pass would not have produced)
  − Duplicated work
  − Coordination overhead (context handed to each branch, results merged back)
  − Merge and review cost
  − Conflict rework
```

**Worker count is bounded by the tightest of four limits, not by the number of tasks:**

```
workers = min(ready independent tasks, execution capacity, review capacity, budget)
```

Review capacity is the one most often forgotten and the one that actually binds — parallelism that outruns the ability to check its output converts throughput into an unreviewed backlog.

**Rules:**
- **Parallelism is set by the critical path and the dependency graph, not by agent count.** Adding a branch that waits on another branch adds coordination cost and no wall-clock.
- **Compare against the single-agent baseline.** A parallel run that is not measured against doing it sequentially has not been shown to be worth it. This is the pre-flight counterpart to the post-hoc amplification figures in Nexus Core Rule #1 (`4.4×` centrally orchestrated vs `17.2×` uncoordinated) — those describe what goes wrong *after* fan-out; this decides whether to fan out at all.
- **Never spawn a sibling to check another sibling's output.** Verification is a sequential step, not a parallel branch.

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
    base_revision: [git SHA all branches fork from]   # REQUIRED — see § Base Revision
    shared_constraints: []     # typed, hub-owned — see § Cross-Branch Constraints

  branches:
    - branch_id: A
      description: [What this branch does]
      chain: [Agent1, Agent2]
      files_owned: [file1.ts, file2.ts]
      base_revision: [git SHA this branch actually started from]
      estimated_steps: [N]
      guardrail_level: [L1|L2|L3]

    - branch_id: B
      description: [What this branch does]
      chain: [Agent3]
      files_owned: [file3.ts]
      base_revision: [git SHA this branch actually started from]
      estimated_steps: [N]
      guardrail_level: [L1|L2|L3]

  merge_point:
    agent: [Agent name for merge verification]
    strategy: [CONCAT|RESOLVE|MANUAL]
    first_check: base_revision_match      # before any patch application

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

### Base Revision (the divergence file ownership cannot see)

Exclusive file ownership guarantees branches never overwrite each other. It guarantees nothing about whether
they were reading **the same repository**. A branch that forked before a merge landed builds against
assumptions that no longer hold — and because it touches only files it owns, `git merge` reports no conflict.
The failure surfaces at runtime, after both branches reported `SUCCESS`.

**Rules.**

1. **Record `base_revision` at the fork point and per branch.** A branch that re-based, resumed after an
   interruption, or started late records what it *actually* forked from — not what the fork point declared.
2. **Base revision match is the merge's first check**, before patch application. Branches on different bases
   are reconciled — re-based or re-verified against the merge target — never merged on the strength of a clean
   textual diff.
3. **A clean `git merge` is not evidence of semantic compatibility.** One branch changing a signature, a
   constraint, or a shared contract while another codes against the old one produces zero text conflicts. Type
   checks, contract tests, and the `sequence` / `invariant` constraints below are what catch it.
4. **Carry `base_revision` into every branch handoff.** Without it, a divergence is undetectable after the
   fact, and `_common/HANDOFF.md` § *Completed vs Verified* has no `head` to bind evidence to.

### Cross-Branch Constraints (what file ownership does not protect)

File ownership prevents branches from **writing over each other**. It does nothing about constraints whose satisfaction is a property of the *whole* fan-out — and those are the ones a locally-successful branch breaks. Every branch can meet its own acceptance criteria and the run can still blow a total budget, invert a required order, or violate an invariant no single branch could see.

Type each inherited constraint, because the type decides **who can check it**:

| Type | Example | Checked by | Fails as |
|------|---------|-----------|----------|
| `per-action` | no single file rewritten wholesale | the branch, per step | local — branch catches it |
| `per-object` | every touched endpoint keeps its contract | the branch, per object | local — branch catches it |
| `aggregate` | total new dependencies ≤ 2 · total diff ≤ N lines · one migration per run | **hub only** | each branch "compliant", sum over budget |
| `temporal` | nothing merged during the release freeze | **hub only** | branch has no clock context |
| `sequence` | schema migration lands before the code that reads it | **hub only** | both branches SUCCESS, integration broken |
| `invariant` | no secret in a committed file, ever, in any branch | hub + every branch | holds in each branch, violated in the merge |

**Rules.**

1. **Declare typed constraints at the fork point**, not per branch — a constraint that exists only inside branch definitions cannot be aggregate-checked.
2. **`aggregate` / `temporal` / `sequence` are hub-owned.** Never delegate them into a branch prompt as if the branch could verify them; a branch reporting "constraint satisfied" for an aggregate is reporting on evidence it does not have.
3. **`sequence` constraints bound the fan-out itself.** Work whose correctness depends on ordering is not parallelizable across branches — either serialize it or make the dependent branch block on the producer's completion, and say which.
4. **Verify at the merge point, not only at branch exit.** The merge agent re-checks every `aggregate` / `sequence` / `invariant` entry before CONCAT; a clean per-branch record is not evidence for any of them.

```yaml
shared_constraints:            # declared at fork_point, inherited by all branches
  - id: C1
    type: aggregate
    rule: "total new runtime dependencies across all branches <= 2"
    owner: hub
  - id: C2
    type: sequence
    rule: "branch_A migration merges before branch_B reader"
    owner: hub
  - id: C3
    type: invariant
    rule: "no credential literal in any committed file"
    owner: hub + every branch
```

### Dynamic Claim (upfront declaration impossible)

Upfront ownership requires knowing the work list before execution. When the work list is discovered *during* the run — a long-lived swarm on a shared repo, an open-ended bug queue — switch to **claim-on-start** instead of declare-upfront:

1. Before touching any file, the agent writes a claim file to `current_tasks/<task-id>.md` naming the task and the files it will own, then commits it.
2. Push rejection / merge conflict on the claim file **is** the duplicate-work signal — no lock server needed. A rejected agent pulls, drops the claim, and picks another task.
3. Work, commit, push, then delete the claim.

Verified at 16 concurrent agents on one shared git repo (`anthropic.com/engineering/building-c-compiler`, 2026-02-05: 2,000 sessions / 2 weeks / ~$20,000). Git's own merge detection was the entire synchronization mechanism.

### Blocking-Task Split (parallelism collapse)

Parallelism fails when every branch converges on the same blocker — one monolithic task that all agents must clear before any can proceed. Symptom: N branches, all `IN_PROGRESS`, all on the same failure.

**Fix:** find an *oracle* that decomposes the monolith into independently attributable units. In the C-compiler run, "compile the Linux kernel" blocked all 16 agents; using GCC as an online oracle to diff outputs per file turned one blocker into per-file bugs that 16 agents could fix in parallel.

Generalized: when a shared blocker appears, look for a **known-good reference implementation** to differential-test against (`_common/DIFFERENTIAL_PARITY.md`). Absent an oracle, serialize the blocker on one branch and re-fan-out after — do not leave branches spinning.

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
