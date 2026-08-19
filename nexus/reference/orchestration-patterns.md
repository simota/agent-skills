# Nexus Orchestration Patterns Reference

**Purpose:** Concrete **execution-style patterns** (Sequential / Parallel / Conditional / Recovery / Escalation / Verification / Rally / Evaluator) used inside the EXECUTE phase.
**Read when:** You're inside the EXECUTE phase and need to shape spawn / handoff / merge for the current step group.

**Boundary vs `execution-phases.md`:** That file owns the **7-phase workflow sequence** (PLAN → … → DELIVER); this file owns the **pattern catalog** used inside any phase that spawns agents. The phase contract picks the pattern; this file describes the pattern.

## Contents
- Spawn Boilerplate (shared `Agent(...)` fields)
- Pattern A: Sequential Chain
- Pattern B: Parallel Branches (conflict resolution → `conflict-resolution.md`)
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

## Spawn Boilerplate (applies to every worked block below)

Every `Agent(...)` block in this file omits the fields that never vary. Assume on each spawn:

```
subagent_type: general-purpose
mode: bypassPermissions
model: sonnet                    # tier per hub-authoring.md § Model Selection
prompt prefix: "You are the <Agent> agent. First, read ~/.claude/skills/<agent>/SKILL.md
                and follow its instructions."
```

Per-pattern blocks below show **only the distinguishing fields** (name, background flag, and the
prompt delta that makes that spawn different). Canonical full template → `nexus/SKILL.md` §
**Agent Spawn Template**; per-CLI spawn syntax → `reference/execution-layers.md`.

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
result1 = Agent(name: "scout-investigation", description: "Root cause analysis",
                prompt: <Scout prefix> + "Task: ...")

result2 = Agent(name: "builder-fix", description: "Implement fix",
                prompt: <Builder prefix> + "Context from previous step: {result1}")
```

---

## Pattern B: Parallel Branches (L2: Parallel Spawn)

> **Opus 5 note — the branch count is a ceiling, not a target.** Opus 5 delegates readily, so the failure mode this pattern must guard is *over*-fan-out, not under-fan-out (`OPUS_5_AUTHORING.md` P4). Two rules follow: (1) a branch must be a genuinely independent, sizeable track — work finishable in a handful of tool calls stays inline; prefer one branch over several when one suffices. (2) **Never open a branch whose job is to check another branch's output on that branch's behalf.** Independent verification is a *sequential* step after the barrier (a different specialist, Q9), not a parallel sibling — a verify-branch racing its producer has no output to verify yet. Multi-agent coordination is otherwise a strength on Opus 5: writer-verifier hand-offs work well and branches rarely clobber each other, so the file-ownership isolation below remains the load-bearing guard rather than a workaround for model confusion.

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
# Both spawns issued in a single response; each adds run_in_background: true and the
# distinguishing "File ownership: <its own files> / Constraints: only those files may be modified".
Agent(name: "builder-email", run_in_background: true,
      prompt: <Builder prefix> + "File ownership: src/validators/email.ts, tests/validators/email.test.ts ...")
Agent(name: "builder-phone", run_in_background: true,
      prompt: <Builder prefix> + "File ownership: src/validators/phone.ts, tests/validators/phone.test.ts ...")

# Wait for both (notifications arrive automatically) → AGGREGATE → VERIFY → DELIVER
```

**agy note — there is no background primitive.** On an agy hub this pattern is realized as either multiple async TUI `/agent` invocations (aggregated by polling `/tasks`, no explicit `wait`) or N externally-launched headless `agy -p` one-shots joined by artifact polling (`_common/AGY_ORCHESTRATION.md` A4). Three consequences: (1) the branch **barrier is manual** — the hub polls until every branch's artifact exists and carries the `<<<END_OF_OUTPUT>>>` sentinel, so a missing artifact is a capture question before it is a task failure (`error-handling.md` § Level 0); (2) branches share one session-scoped tier (A3) — do not design a branch set that needs different effort levels; (3) subagent contexts are **isolated** and do not inherit hub history, so each branch prompt carries its own state delta and branches exchange nothing but filesystem artifacts. File-ownership isolation is unchanged and remains the load-bearing guard.

Conflict classification, the auto-resolve/escalate matrix, and the ownership-score formula that
decides a SEMANTIC conflict are owned by `reference/conflict-resolution.md` — the CONFLICT DETECTION
box above is the entry point into it.

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
  prompt: <Rally prefix> + |
    Task: implement in parallel the following features.
    Workers:
      1. Builder: user authentication API (src/auth/)
      2. Builder: profile API (src/profile/)
      3. Artisan: login UI (src/components/auth/)
      4. Artisan: profile UI (src/components/profile/)
      5. Radar: integration tests (tests/)

    Constraints:
    - Each worker may only modify its designated directory
    - Verify build, tests, and type-check pass

    On completion, emit results in the _STEP_COMPLETE format.
)
```

**Escalation from L2 to L3**: If L2 parallel spawn encounters ownership conflicts or requires more than 3 branches, escalate to L3 Rally delegation.

---

## Pattern H: Evaluator Loop

**Spec is `reference/evaluator-loop-protocol.md`** — it owns the loop ladder diagram, the Sprint
Contract format, the Rubric, and the aggregation rules. Read it before authoring this pattern; the
notes here are only the per-engine execution delta.

**Use when**: Task qualifies for Evaluator Loop (FEATURE MEDIUM+, SECURITY, complex tasks). The Generator produces deliverables; independent Evaluator agents assess them against the Sprint Contract rubric.

**Key constraint**: Evaluators are read-only — they assess but do not modify code. Only the Generator makes changes.

**Shared prompt delta** (all engines): the Generator carries `Sprint Contract: {contract}` + the task;
each Evaluator carries `Mode: EVALUATOR (evaluation only, no code changes)` + the same contract +
`Under evaluation: {generator output}`. **Loop limits**: max 3 iterations; stop on all-ACCEPT,
score delta < 0.2, or max reached.

| Engine | Generator | Evaluator fan-out | Join / cleanup |
|--------|-----------|-------------------|----------------|
| **Claude Code** | `Agent(...)` foreground | N × `Agent(..., run_in_background: true)` in one response | completion notifications; no cleanup call |
| **Codex CLI** | `spawn_agent` → `wait_agent` | N × `spawn_agent` issued before any wait | `wait_agent` each, then `close_agent` each |
| **agy** | headless one-shot (no background primitive) | wave of independent one-shots | artifact polling — no `wait` primitive exists |

Per-CLI API detail (tool names, prereqs, flags) → `reference/execution-layers.md`.

**agy-specific loop rules:** every step pins the mandated Gemini 3.7 Flash (High) tier with the Deep
Reasoning Directive appended (`_common/AGY_ORCHESTRATION.md` A1-R/A9-D), captures via the
prompt-mandated artifact + sentinel (`_common/CLI_COMPATIBILITY.md §9.2`), and injects the upstream
artifact with `@<path>` — never a bare path (A5). Maker ≠ checker still holds (separate processes,
isolated contexts), which is why the pattern ports; but the generator runs a *fast* model, so weight
the evaluator rubric accordingly. A capture failure (empty artifact / missing sentinel) is **not** a
REVISE signal — resolve it as a Level 0 capture failure first (typed retry, max 1). Iterate by
re-spawning one-shots or resuming with `-c`/`--conversation <id>`.

---

## Dynamic Workflows Pattern Vocabulary (official ↔ Nexus)

Claude Code's Dynamic Workflows feature names six canonical orchestration shapes. When a request describes one of these, reuse the matching Nexus pattern below. On Claude Code, a large fan-out may delegate execution to a native dynamic workflow; off Claude Code, implement with the Nexus pattern directly. Availability and runtime limits are volatile and belong in `_common/CLI_COMPATIBILITY.md`, not in this pattern contract.

| Dynamic Workflows pattern | Nexus equivalent |
|---------------------------|------------------|
| **Classify-and-act** | Pattern C: Conditional Routing |
| **Fan-out-and-synthesize** | Pattern B: Parallel Branches (barrier = AGGREGATE) |
| **Adversarial verification** | Pattern F: Verification Gate / Pattern H: Evaluator Loop |
| **Generate-and-filter** | Pattern H variant (generate → rubric filter) |
| **Tournament** | Pattern B fan-out + pairwise judge (see `essential`/`killer` convergence) |
| **Loop-until-done** | Pattern D: Recovery Loop / loop-until-dry |

Current product availability must be verified at execution time against Anthropic's official announcement: [Introducing Dynamic Workflows](https://claude.com/blog/introducing-dynamic-workflows-in-claude-code). Nexus owns only the stable pattern mapping above.

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
