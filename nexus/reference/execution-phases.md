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

## Short 3-Phase Path (SIMPLE + AUTORUN)

For tasks classified SIMPLE and eligible for AUTORUN, collapse the 7 phases into this short path. It **folds the safety gates in — it does not skip them**: AGGREGATE still runs inside DO, and VERIFY still runs inside CHECK.

| Short | Maps To | Actions |
|------------|---------|---------|
| PLAN | PLAN + PREPARE + CHAIN_SELECT | Classify task, assess complexity, select chain |
| DO | EXECUTE + AGGREGATE | Execute chain steps, merge parallel results |
| CHECK | VERIFY + DELIVER | Run tests, deliver final output |

Each phase completes before the next begins. Track only: current phase (PLAN/DO/CHECK) and current step (X/Y).

---

## Phase 0: PROACTIVE_ANALYSIS (Optional)

Automatically activates when `/Nexus` is invoked by itself. Skip this phase when a normal task instruction is present. Full scan steps (0-A Project State Scan, 0-B evidence-grounded Health Assessment, 0-C Recommendation Generation with priority table) → `reference/proactive-mode.md`.

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

---

## AUTORUN_FULL (7 Phases)

### Phase 1: PLAN
Classify and analyze the task:

**Task Classification:** resolve the task type against `routing-matrix.md` — it owns the type list, the signals that select each type, and each type's default chain.

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
Spawn agents via the Agent tool with guardrail checkpoints. Three layers — **L1** sequential spawn (foreground) for 1-4 step chains, **L2** parallel spawn (background) for 2-3 independent branches, **L3** Rally delegation for 4+ workers or complex ownership. Every spawned agent reads its own SKILL.md and executes autonomously; the hub takes `_STEP_COMPLETE` from the result, runs the Guardrail Check at configured checkpoints, and either passes accumulated context to the next spawn or triggers recovery. After an L2 barrier, proceed to AGGREGATE.

Per-layer spawn procedures and API signatures → `reference/execution-layers.md`. Worked spawn examples (Scout→Builder chain, email/phone parallel branches, Rally team) → `orchestration-patterns.md` Patterns A/B/G.

**agy hub variant (L1/L2/L3)**

The layers above are Claude Code (`Agent(...)`) shapes. On an **agy** hub the phase logic is unchanged, but three primitives do not exist — author against the substitutions in `_common/AGY_ORCHESTRATION.md` A1-A4 / `reference/execution-layers.md` § Antigravity CLI (no per-spawn model field, no foreground/background distinction, no Rally equivalent). Consequence for this phase:

| Missing primitive | Consequence for Phase 4 |
|--------------------|--------------------------|
| No per-spawn model field (tier is session-scoped, A3) | Pick the tier at *chain* level; a mixed-effort chain splits into per-step headless `agy -p` runs, each pinning its own tier. Recipe steps stay **High**, no downgrade (A1-R) |
| No foreground/background distinction (A2) | Deliverable is read from the **prompt-mandated artifact file**, never stdout (`_common/CLI_COMPATIBILITY.md §9.2`). Step 3 of the L1 loop becomes "read `_STEP_COMPLETE` from the artifact after the verification chain passes" |
| No Rally equivalent (A4) | L3 **flattens**: drive the fan-out from the hub in waves of 2-3, or use an installed team pack (`oh-my-antigravity` `/oma:taskboard`). Log the flattening honestly — never report a Rally spawn on agy |

Two further Phase 4 rules on agy: append the **Deep Reasoning Directive** (A9-D) to every recipe spawn prompt, and inject file context with `@<path>` — a bare path is read by an internal subagent that dies at the 60s cap (A5). For 4+ step chains, resume with `-c`/`--conversation <id>` instead of re-spawning (A4).

Layer selection criteria (1-4 steps → L1, 2-3 independent branches → L2, 4+ workers → L3) and per-engine API mapping: `reference/execution-layers.md` § Claude Code.

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
