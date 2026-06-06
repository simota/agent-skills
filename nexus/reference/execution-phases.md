# Nexus Execution Phases Reference

**Purpose:** The **Nexus 7-phase workflow** (`PLAN → PREPARE → CHAIN_SELECT → EXECUTE → AGGREGATE → VERIFY → DELIVER`) and its AUTORUN/AUTORUN_FULL/proactive variants.
**Read when:** You need the exact phase sequence and what happens at each phase boundary.

**Boundary vs `orchestration-patterns.md`:** This file owns the **phase sequence** (what runs when, in which order, with which gates). `orchestration-patterns.md` owns the **execution-style patterns** (Sequential / Parallel / Conditional / Recovery / Escalation / Verification / Rally / Evaluator) — how spawn/handoff is shaped inside the EXECUTE phase. When a phase contract says "spawn agents", follow that file for the pattern.

## Contents
- Phase 0: PROACTIVE_ANALYSIS (Optional)
- AUTORUN_FULL (7 Phases) — Phase 2 includes Sprint Contract, Phase 6 includes Evaluator Loop
- AUTORUN (5 Phases - Simple Tasks Only)

Detailed phase descriptions for AUTORUN modes.

---

## Simplified 3-Phase Path (cross-model)

When 7-phase state tracking is difficult, use this simplified path:

| Simplified | Maps To | Actions |
|------------|---------|---------|
| PLAN | PLAN + PREPARE + CHAIN_SELECT | Classify task, assess complexity, select chain |
| DO | EXECUTE + AGGREGATE | Execute chain steps, merge parallel results |
| CHECK | VERIFY + DELIVER | Run tests, deliver final output |

Each phase completes before the next begins. Track only: current phase (PLAN/DO/CHECK) and current step (X/Y).

---

## Phase 0: PROACTIVE_ANALYSIS (Optional)

Automatically activates when `/Nexus` is invoked by itself. Skip this phase when a normal task instruction is present.

### 0-A: Project State Scan
Collect the current state of the project:

```bash
# Git status
git status --porcelain

# Recent commits
git log --oneline -10

# Activity Log (if exists)
.agents/PROJECT.md → Activity Log section
```

### 0-B: Health Assessment
Assess project health across four indicators:

| Indicator | Checks | Rating |
|-----------|--------|--------|
| `test_health` | Test execution, coverage | 🟢/🟡/🔴 |
| `security_health` | `npm audit`, dependencies | 🟢/🟡/🔴 |
| `code_health` | Linting, type checks | 🟢/🟡/🔴 |
| `doc_health` | README freshness, JSDoc | 🟢/🟡/🔴 |

### 0-C: Recommendation Generation
Generate recommended actions with priorities:

| Priority | Conditions |
|----------|------------|
| 🔴 High | Security issues, test failures, build errors |
| 🟡 Medium | Lint warnings, coverage regression, missing documentation |
| 🟢 Low | Refactoring opportunities, optimization suggestions |

### Flow After Phase 0

```
Phase 0 Complete
    ↓
User Selection (ON_PROACTIVE_START)
    ↓
├─ Recommended action selected → Phase 1: PLAN (AUTORUN_FULL)
├─ Continue previous work → Phase 1: PLAN (AUTORUN_FULL)
└─ New task specified → Standard routing → Phase 1
```

See `reference/proactive-mode.md` for detailed specifications.

---

## AUTORUN_FULL (7 Phases)

### Phase 1: PLAN
Classify and analyze the task:

**Task Classification:**
- **BUG**: Error fix, defect response, "not working", "broken"
- **INCIDENT**: Production outage, service degradation, "down", "emergency", "SEV1/2/3/4"
- **API**: API design, endpoint creation, OpenAPI spec
- **FEATURE**: New feature, "I want to...", "add..."
- **REFACTOR**: Code cleanup (behavior unchanged)
- **OPTIMIZE**: Performance improvement
- **SECURITY**: Security response, vulnerability
- **DOCS**: Documentation
- **INFRA**: Infrastructure provisioning

**Complexity Assessment:**
- **SIMPLE**: 1-2 steps to complete
- **MEDIUM**: 3-5 steps
- **COMPLEX**: 6+ steps (decompose with Sherpa)

**Analysis:**
- Identify independent tasks (parallelizable)
- Identify dependent tasks (sequential required)
- Map file ownership per branch
- Determine guardrail requirements

### Phase 2: PREPARE
Set up execution environment:

1. **Context Snapshot Creation** - Capture initial goal and acceptance criteria
2. **Rollback Point Definition** - Create git stash or branch for recovery
3. **Guardrail Configuration** - Set appropriate levels per step
4. **Parallel Branch Preparation** - Split independent tasks, assign file ownership
5. **Sprint Contract Creation** (when Evaluator Loop applicable) - Define acceptance criteria, select rubric template, assign Generator and Evaluators. See `reference/evaluator-loop-protocol.md` (§ Sprint Contract) for format and applicability rules. Skip for SIMPLE complexity or tasks where Evaluator Loop is disabled.

### Phase 3: CHAIN_SELECT
Auto-select agent chain based on classification.

For parallel execution:
```
_PARALLEL_CHAINS:
  - branch_id: A
    chain: [Agent1, Agent2]
    files: [file1.ts, file2.ts]
  - branch_id: B
    chain: [Agent3, Agent4]
    files: [file3.ts, file4.ts]
  merge_point: Radar
```

### Phase 4: EXECUTE
Spawn agents via Agent tool with guardrail checkpoints:

**L1: Sequential Spawn (foreground)**

For chains with 1-4 sequential steps:

1. Spawn agent via `Agent(name, description, subagent_type: general-purpose, mode: bypassPermissions, model, prompt)` in foreground
2. Agent reads its own SKILL.md and executes autonomously
3. Receive `_STEP_COMPLETE` from the spawned agent's response
4. Guardrail Check at configured checkpoints
5. Extract handoff context from result
6. Spawn next agent with accumulated context OR trigger recovery

```
# Step 1: Spawn Scout
Agent(
  name: "scout-[task-slug]"
  description: "[Short description]"
  subagent_type: general-purpose
  mode: bypassPermissions
  model: sonnet
  prompt: |
    あなたは Scout エージェントです。
    まず ~/.claude/skills/scout/SKILL.md を読み、その指示に従ってください。
    タスク: [task]
    制約: [constraints]
    完了時、_STEP_COMPLETE フォーマットで結果を出力してください。
)

# Step 2: Use Scout's output to spawn Builder
Agent(
  name: "builder-[task-slug]"
  ...
  prompt: |
    ...
    前ステップからのコンテキスト: [Scout's _STEP_COMPLETE output]
    ...
)
```

**L2: Parallel Spawn (background)**

For 2-3 independent branches:

1. Spawn independent agents via `Agent(run_in_background: true)` simultaneously
2. Each agent reads its own SKILL.md and works independently
3. Wait for all background agents to complete (notifications arrive automatically)
4. Collect results from all agents
5. Proceed to AGGREGATE

```
# Spawn Branch A and Branch B simultaneously
Agent(
  name: "builder-email-validation"
  description: "Implement email validation"
  run_in_background: true
  mode: bypassPermissions
  model: sonnet
  prompt: |
    あなたは Builder エージェントです。
    まず ~/.claude/skills/builder/SKILL.md を読み、その指示に従ってください。
    タスク: メールバリデーション機能を実装
    ファイル所有権: src/validators/email.ts, tests/validators/email.test.ts
    制約: 上記ファイルのみ変更可能
    完了時、_STEP_COMPLETE フォーマットで結果を出力してください。
)

Agent(
  name: "builder-phone-validation"
  description: "Implement phone validation"
  run_in_background: true
  mode: bypassPermissions
  model: sonnet
  prompt: |
    あなたは Builder エージェントです。
    まず ~/.claude/skills/builder/SKILL.md を読み、その指示に従ってください。
    タスク: 電話番号バリデーション機能を実装
    ファイル所有権: src/validators/phone.ts, tests/validators/phone.test.ts
    制約: 上記ファイルのみ変更可能
    完了時、_STEP_COMPLETE フォーマットで結果を出力してください。
)
```

**L3: Rally Delegation**

For 4+ workers or complex ownership management:

1. Spawn Rally as an Agent with full task context
2. Rally reads its own SKILL.md and manages team creation, task distribution, and monitoring
3. Rally returns aggregated results via `_STEP_COMPLETE`

```
Agent(
  name: "rally-parallel-impl"
  description: "Parallel implementation coordination"
  subagent_type: general-purpose
  mode: bypassPermissions
  model: sonnet
  prompt: |
    あなたは Rally エージェントです。
    まず ~/.claude/skills/rally/SKILL.md を読み、その指示に従ってください。

    タスク: 以下の実装を並列で実行してください。
    ワーカー:
      1. Builder: メールバリデーション (src/validators/email.ts)
      2. Builder: 電話番号バリデーション (src/validators/phone.ts)
      3. Artisan: フォームUIコンポーネント (src/components/Form.tsx)
      4. Radar: 全体テスト (tests/)

    完了時、_STEP_COMPLETE フォーマットで結果を出力してください。
)
```

### Layer Selection Criteria

| Condition | Layer | Rationale |
|-----------|-------|-----------|
| Sequential chain, 1-4 steps | L1: Direct Spawn | Simple, low overhead |
| 2-3 independent branches, clear file ownership | L2: Parallel Spawn | True parallelism via background agents |
| 4+ workers, complex ownership, or multi-step branches | L3: Rally Delegation | Full team management needed |

### Phase 5: AGGREGATE
Merge parallel results:

1. Collect Branch Results - Gather outputs, check for conflicts
2. Conflict Resolution - Resolve or escalate file conflicts
3. Context Consolidation - Update L1_GLOBAL, prepare unified state

### Phase 6: VERIFY (with optional Evaluator Loop)

**When Evaluator Loop is DISABLED** (default for SIMPLE tasks, BUG, small REFACTOR):

1. Run tests (Radar equivalent)
2. Confirm build passes
3. Security scan if applicable (Sentinel)
4. Final Guardrail Check (L2_CHECKPOINT minimum)

**When Evaluator Loop is ENABLED** (FEATURE MEDIUM+, SECURITY, complex BUG/REFACTOR):

1. Spawn Evaluator team in parallel (background agents) per Sprint Contract
2. Each Evaluator scores deliverable against rubric dimensions
3. Aggregate `EVALUATION_FEEDBACK` from all Evaluators
4. Decision:
   - All ACCEPT → proceed to Phase 7: DELIVER
   - Any REVISE (iteration < max) → return to Phase 4: EXECUTE with `REVISION_BRIEF`
   - Any REVISE (iteration >= max) → accept best result, proceed to DELIVER with quality notes
   - Any BLOCK → ESCALATE to user

See `reference/evaluator-loop-protocol.md` for the full end-to-end pattern (orchestration loop + Rubric scoring + Sprint Contract format).

### Phase 7: DELIVER
Finalize and present results:

1. Integrate final output
2. Generate change summary
3. Present verification steps
4. Cleanup rollback points (on success)

---

## AUTORUN (5 Phases - Simple Tasks Only)

| Phase | Description |
|-------|-------------|
| **CLASSIFY** | Same as AUTORUN_FULL Phase 1 |
| **CHAIN_SELECT** | Auto-select agent chain |
| **EXECUTE_LOOP** | Execute each agent role, record _STEP_COMPLETE |
| **VERIFY** | Run tests, confirm build |
| **DELIVER** | Integrate output, generate summary |

COMPLEX tasks are downgraded to GUIDED mode.
