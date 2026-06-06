# Nexus Orchestration Patterns Reference

**Purpose:** Concrete **execution-style patterns** (Sequential / Parallel / Conditional / Recovery / Escalation / Verification / Rally / Evaluator) used inside the EXECUTE phase.
**Read when:** You're inside the EXECUTE phase and need to shape spawn / handoff / merge for the current step group.

**Boundary vs `execution-phases.md`:** That file owns the **7-phase workflow sequence** (PLAN → … → DELIVER); this file owns the **pattern catalog** used inside any phase that spawns agents. The phase contract picks the pattern; this file describes the pattern.

## Contents
- Pattern A: Sequential Chain
- Pattern B: Parallel Branches (with Auto-Conflict Resolution)
- Pattern C: Conditional Routing
- Pattern D: Recovery Loop
- Pattern E: Escalation Path
- Pattern F: Verification Gate
- Pattern G: Rally Delegation
- Pattern H: Evaluator Loop
- Dynamic Workflows Pattern Vocabulary (official ↔ Nexus)
- Hub Communication Protocol

Detailed patterns for agent chain execution.

---

## Pattern A: Sequential Chain (L1: Direct Spawn)

```
Nexus → Agent(Scout, foreground) → _STEP_COMPLETE
                                       ↓
Nexus → Agent(Builder, foreground) → _STEP_COMPLETE
              [with Scout context]         ↓
Nexus → Agent(Radar, foreground) → _STEP_COMPLETE
              [with Builder context]       ↓
Nexus → VERIFY → DELIVER
```

**Use when**: Steps have strict dependencies (output of one is input of next)

**Implementation**: Each agent is spawned via `Agent(foreground)`. Nexus extracts `_STEP_COMPLETE` output from the returned result and passes it as handoff context to the next agent's prompt.

```
# Step 1
result1 = Agent(
  name: "scout-investigation"
  description: "Root cause analysis"
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Scout エージェントです。まず ~/.claude/skills/scout/SKILL.md を読み..."
)

# Step 2 - uses Step 1's output
result2 = Agent(
  name: "builder-fix"
  description: "Implement fix"
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Builder エージェントです。まず ~/.claude/skills/builder/SKILL.md を読み...
    前ステップからのコンテキスト: {result1}"
)
```

---

## Pattern B: Parallel Branches (L2: Parallel Spawn)

```
Nexus → Agent(Builder-A, background) ──┐
      → Agent(Builder-B, background) ──┤
                                        ↓ (wait for all)
                            ┌───────────────────────┐
                            │ CONFLICT DETECTION    │
                            │ - Identify overlaps   │
                            │ - Classify conflicts  │
                            └───────────┬───────────┘
                                        │
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
                   No Conflicts                    Has Conflicts
                        │                               │
                        │                   ┌───────────┴───────────┐
                        │                   ▼                       ▼
                        │              Auto-Resolvable         Needs User
                        │              (ADJACENT,              (SEMANTIC
                        │               FORMATTING,             unclear,
                        │               SEMANTIC clear)         STRUCTURAL)
                        │                   │                       │
                        │                   ▼                       ▼
                        │              Auto-Resolve            ESCALATE
                        │                   │                       │
                        └───────────┬───────┘                       │
                                    ▼                               │
                            AGGREGATE                               │
                                    │                               │
                                    ▼                               │
                              VERIFY (tests)                        │
                                    │                               │
                        ┌───────────┴───────────┐                   │
                        ▼                       ▼                   │
                      PASS                    FAIL                  │
                        │                       │                   │
                        ▼                       ▼                   │
                    DELIVER              RECOVERY ←─────────────────┘
```

**Use when**: 2-3 independent tasks can execute simultaneously (e.g., separate features)

**Implementation**: Each branch is spawned as a background Agent. Nexus waits for completion notifications, then aggregates results.

```
# Spawn both branches simultaneously in a single response
Agent(
  name: "builder-email"
  description: "Email validation"
  run_in_background: true
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Builder エージェントです。まず ~/.claude/skills/builder/SKILL.md を読み...
    ファイル所有権: src/validators/email.ts, tests/validators/email.test.ts
    制約: 上記ファイルのみ変更可能..."
)

Agent(
  name: "builder-phone"
  description: "Phone validation"
  run_in_background: true
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Builder エージェントです。まず ~/.claude/skills/builder/SKILL.md を読み...
    ファイル所有権: src/validators/phone.ts, tests/validators/phone.test.ts
    制約: 上記ファイルのみ変更可能..."
)

# Wait for both to complete (notifications arrive automatically)
# Then proceed to AGGREGATE → VERIFY → DELIVER
```

### Auto-Conflict Resolution Rules

| Conflict Type | Auto-Resolve? | Method |
|---------------|---------------|--------|
| ADJACENT | ✅ Always | Accept both, merge in order |
| FORMATTING | ✅ Always | Regenerate with formatter |
| SEMANTIC (owner clear) | ✅ If ownership >= 0.70 | Ownership priority |
| SEMANTIC (owner unclear) | ❌ | Escalate to user |
| STRUCTURAL | ❌ Never | Always escalate |

### Ownership Priority

When two branches modify the same code semantically:

```yaml
ownership_score:
  primary_agent_role: 0.40  # Domain specialist bonus
  change_volume: 0.30       # More changes = more ownership
  task_alignment: 0.30      # Is file central to task?

  auto_resolve_if: ownership_score >= 0.70
```

See `reference/conflict-resolution.md` for detailed resolution strategies.

---

## Pattern C: Conditional Routing

```
Nexus → NEXUS_ROUTING → Agent1 → NEXUS_HANDOFF
                           ↓
Nexus → Analyze findings
           │
           ├─ [Security issue] → Sentinel → NEXUS_HANDOFF
           ├─ [Performance issue] → Bolt → NEXUS_HANDOFF
           └─ [No issues] → Continue to next step
```

**Use when**: Next agent depends on findings (e.g., Judge → Builder OR Sentinel)

---

## Pattern D: Recovery Loop

```
Nexus → NEXUS_ROUTING → Agent → NEXUS_HANDOFF
                           │
                           ├─ [SUCCESS] → Continue
                           │
                           └─ [FAILED] → Error Handler
                                    ↓
                              ┌─────────────────┐
                              │ Recovery Action │
                              │ - Retry (L1)    │
                              │ - Inject fix (L2)│
                              │ - Rollback (L3) │
                              └────────┬────────┘
                                       ↓
                              Re-execute or Escalate
```

**Use when**: Errors occur during execution (auto-recovery enabled)

---

## Pattern E: Escalation Path

```
Nexus → NEXUS_ROUTING → Agent → NEXUS_HANDOFF (Pending Confirmation)
                                        ↓
Nexus → Present to User (AskUserQuestion)
                                        ↓
User → Select option
                                        ↓
Nexus → NEXUS_ROUTING (with User Confirmation) → Agent continues
```

**Use when**: Agent encounters decision requiring user input (L4 guardrail or GUIDED mode)

---

## Pattern F: Verification Gate

```
Nexus → Chain execution complete
                   ↓
          ┌───────────────────┐
          │ VERIFICATION GATE │
          │ - Tests pass?     │
          │ - Build OK?       │
          │ - Security OK?    │
          └─────────┬─────────┘
                    │
          ┌────────┴────────┐
          ↓ PASS            ↓ FAIL
      DELIVER          RECOVERY
                           │
                    ┌──────┴──────┐
                    │ Rollback OR │
                    │ Re-execute  │
                    └─────────────┘
```

**Use when**: Critical verification before final delivery (always used in AUTORUN_FULL)

---

## Pattern G: Rally Delegation (L3)

```
Nexus → Agent(Rally, foreground) → Rally manages team
                                       ↓
                              ┌────────────────────┐
                              │ Rally Team Session  │
                              │ - TeamCreate        │
                              │ - Spawn teammates   │
                              │ - Monitor tasks     │
                              │ - Synthesize        │
                              │ - Cleanup           │
                              └────────┬───────────┘
                                       ↓
                              _STEP_COMPLETE (aggregated)
                                       ↓
                              Nexus → VERIFY → DELIVER
```

**Use when**: 4+ workers needed, complex file ownership, or multi-step parallel branches

**Implementation**: Nexus spawns Rally as a single Agent. Rally handles all team management internally using Agent Teams API.

```
Agent(
  name: "rally-feature-impl"
  description: "Parallel feature implementation"
  subagent_type: general-purpose
  mode: bypassPermissions
  model: sonnet
  prompt: |
    あなたは Rally エージェントです。
    まず ~/.claude/skills/rally/SKILL.md を読み、その指示に従ってください。

    タスク: 以下の機能を並列実装してください。
    ワーカー:
      1. Builder: ユーザー認証API (src/auth/)
      2. Builder: プロフィールAPI (src/profile/)
      3. Artisan: ログインUI (src/components/auth/)
      4. Artisan: プロフィールUI (src/components/profile/)
      5. Radar: 統合テスト (tests/)

    制約:
    - 各ワーカーは指定ディレクトリのみ変更可能
    - ビルド・テスト・型チェック通過を確認

    完了時、_STEP_COMPLETE フォーマットで結果を出力してください。
)
```

**Escalation from L2 to L3**: If L2 parallel spawn encounters ownership conflicts or requires more than 3 branches, escalate to L3 Rally delegation.

---

## Pattern H: Evaluator Loop

```
Nexus → Agent(Generator, foreground) → _STEP_COMPLETE
                                          ↓
Nexus → spawn Evaluators in parallel:
         Agent(Evaluator-1, bg) + Agent(Evaluator-2, bg)
                                          ↓ (wait for all)
Nexus → Aggregate EVALUATION_FEEDBACK
         ├─ All ACCEPT     → DELIVER
         ├─ Any REVISE     → compile REVISION_BRIEF
         │                    → Agent(Generator, with feedback) → loop
         └─ Any BLOCK      → ESCALATE to user
```

**Use when**: Task qualifies for Evaluator Loop (FEATURE MEDIUM+, SECURITY, complex tasks). The Generator produces deliverables; independent Evaluator agents assess them against the Sprint Contract rubric.

**Key constraint**: Evaluators are read-only — they assess but do not modify code. Only the Generator makes changes.

**Implementation**: Generator runs in foreground. Evaluators spawn as background agents with the Sprint Contract and Generator's output. Nexus aggregates feedback and either accepts, compiles a revision brief for the Generator, or escalates.

```
# Step 1: Generator produces deliverable
result = Agent(
  name: "builder-feature-impl"
  description: "Implement feature"
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Builder エージェントです。まず ~/.claude/skills/builder/SKILL.md を読み...
    Sprint Contract: {contract}
    タスク: {task_description}"
)

# Step 2: Spawn Evaluators in parallel
Agent(
  name: "judge-eval-feature"
  description: "Code quality evaluation"
  run_in_background: true
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Judge エージェントです。まず ~/.claude/skills/judge/SKILL.md を読み...
    モード: EVALUATOR (評価のみ、コード変更不可)
    Sprint Contract: {contract}
    評価対象: {result}"
)

Agent(
  name: "radar-eval-feature"
  description: "Test coverage evaluation"
  run_in_background: true
  mode: bypassPermissions
  model: sonnet
  prompt: "あなたは Radar エージェントです。まず ~/.claude/skills/radar/SKILL.md を読み...
    モード: EVALUATOR (評価のみ、コード変更不可)
    Sprint Contract: {contract}
    評価対象: {result}"
)

# Step 3: Aggregate feedback → ACCEPT / REVISE / BLOCK
```

**Loop limits**: Max iterations default 3. Terminate on: all ACCEPT, diminishing returns (score delta < 0.2), or max iterations reached.

### Codex CLI Implementation

```
# Step 1: Generator
gen_id = spawn_agent(
  prompt: "あなたは Builder エージェントです。まず ~/.claude/skills/builder/SKILL.md を読み...
    Sprint Contract: {contract}
    タスク: {task_description}"
)
gen_result = wait_agent(gen_id)

# Step 2: Evaluators in parallel
judge_id = spawn_agent(
  prompt: "あなたは Judge エージェントです。まず ~/.claude/skills/judge/SKILL.md を読み...
    モード: EVALUATOR (評価のみ、コード変更不可)
    Sprint Contract: {contract}
    評価対象: {gen_result}"
)
radar_id = spawn_agent(
  prompt: "あなたは Radar エージェントです。まず ~/.claude/skills/radar/SKILL.md を読み...
    モード: EVALUATOR (評価のみ、コード変更不可)
    Sprint Contract: {contract}
    評価対象: {gen_result}"
)

# Step 3: Collect feedback
judge_feedback = wait_agent(judge_id)
radar_feedback = wait_agent(radar_id)

# Step 4: Aggregate → ACCEPT / REVISE / BLOCK
# If REVISE: spawn_agent(Generator with REVISION_BRIEF)
# Cleanup
close_agent(gen_id)
close_agent(judge_id)
close_agent(radar_id)
```

See `reference/evaluator-loop-protocol.md` for the full end-to-end specification (loop pattern + Sprint Contract format + Rubric scoring criteria).

---

## Dynamic Workflows Pattern Vocabulary (official ↔ Nexus)

Claude Code's Dynamic Workflows feature names six canonical orchestration shapes. When a request describes one of these, use the official name (per the shared-vocabulary rule in `managed-agents-mapping.md §3`) and reuse the matching Nexus pattern below — they are the same shapes under different labels. On Claude Code, a large fan-out of any of these may delegate execution to a native dynamic workflow (`managed-agents-mapping.md §5`); off Claude Code, implement with the Nexus pattern directly.

| Dynamic Workflows pattern | What it does | Nexus equivalent |
|---------------------------|--------------|------------------|
| **Classify-and-act** | A router agent determines task type and directs to specialized handlers | Pattern C: Conditional Routing |
| **Fan-out-and-synthesize** | Split into parallel subtasks with independent agents, then merge at a synchronization barrier | Pattern B: Parallel Branches (barrier = AGGREGATE) |
| **Adversarial verification** | A separate agent verifies each output against a rubric | Pattern F: Verification Gate / Pattern H: Evaluator Loop |
| **Generate-and-filter** | Generate many candidates, then filter by quality criteria | Pattern H variant (generate → rubric filter) |
| **Tournament** | N agents compete on an identical task with pairwise judging | Pattern B fan-out + pairwise judge (see `essential`/`killer` convergence) |
| **Loop-until-done** | Spawn iteratively until a stop condition (no new findings, error resolved) | Pattern D: Recovery Loop / loop-until-dry |

These six combat the single-context failure modes (agentic laziness, self-preferential bias, goal drift) documented in `managed-agents-mapping.md §5`. [Source: claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code]

---

## Hub Communication Protocol

```
User Request
     ↓
  NEXUS (Classify & Design Chain)
     ↓
  ┌──────────────────────────────────────────────────────────────┐
  │                    NEXUS_ROUTING                             │
  │  (Context, Goal, Step, Constraints, Expected Output)         │
  └──────────────────────────────────────────────────────────────┘
     ↓
  Agent A executes
     ↓
  ┌──────────────────────────────────────────────────────────────┐
  │                    NEXUS_HANDOFF                             │
  │  (Summary, Artifacts, Risks, Suggested Next, _STEP_COMPLETE) │
  └──────────────────────────────────────────────────────────────┘
     ↓
  NEXUS (Aggregate, Route, or Verify)
     ↓
  Next Agent or DELIVER
```
