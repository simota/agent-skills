# Nexus Guardrail System Reference

**Purpose:** Guardrail **states** (L1 MONITORING → L4 ABORT), per-task-type checkpoint config, Auto-Recovery Chains (A/B/C), and execution-state tracking.
**Read when:** You need to configure or interpret the execution-state guardrail for a task, or look up a Recovery Chain spec.

**Boundary vs `error-handling.md`:** This file owns the **execution-state axis** (L1-L4 guardrail levels + recovery chain definitions + state hierarchy). `error-handling.md` owns the **error-classification axis** (L1 retry → L5 abort by error severity) and invokes Recovery Chains defined here. Both files reference L1-L4, but along different axes — guardrails by state, error-handling by error type.

## Contents
- Guardrail Levels
- Guardrail Configuration by Task Type
- Action Tier Ladder
- Auto-Recovery Actions
- L3 Auto-Recovery Chains
- Recovery Confidence Calculation
- Recovery Decision Flow
- Guardrail Event Format
- Context Hierarchy
- State Record Format
- Parallel Branch Context
- Verification Debt Guardrail

Guardrails, context management, and state tracking for AUTORUN_FULL.

---

## Guardrail Levels

**This table is the single definition of the guardrail levels.** `_common/AUTORUN.md` § Guardrail Protocol cites
it and adds the per-level trigger→action catalog; it does not restate the levels.

**Classify by goal impact, not by a cross-domain number.** A **minor** failure — the step's goal is still
reachable by a local fix — attempts the fix and continues. A **major** failure — the goal is no longer
reachable by a local fix — stops and reconsiders (rollback / re-decompose / escalate). The percentages below
are **rough guidelines**, not fixed thresholds; each task type and domain may draw the minor/major line
differently. A failure between the guidelines is classified by that question, never left undefined.

| Level | Name | Trigger | Action |
|-------|------|---------|--------|
| L1 | MONITORING | lint_warning, minor_deprecation, minor coverage drop (~<5%) | Log only, continue execution |
| L2 | CHECKPOINT | **minor** test_failure (goal reachable; ~<20%), security_warning, type_error | Auto-verify, attempt auto-fix, conditional continue |
| L3 | PAUSE | **major** test_failure (goal not locally fixable; ~>50%), breaking_change, build_failure, merge_conflict | Pause, attempt auto-recovery |
| L4 | ABORT | critical_security, data_integrity_risk, user abort | Immediate stop, rollback |

---

## Guardrail Configuration by Task Type

| Task Type | Default Level | Pre-check | Post-check |
|-----------|---------------|-----------|------------|
| FEATURE | L2 | - | Tests pass |
| SECURITY | L2 | Sentinel scan | No new vulnerabilities |
| REFACTOR | L2 | - | Tests unchanged |
| API (breaking) | L3 | Atlas impact | All consumers updated |
| INCIDENT | L3 | - | Service restored |
| INFRA | L3 | - | Health checks pass |

---

## Edge Types — who decides the next step

Before grading how much a step may change, decide **what kind of thing chooses it**. Three kinds, and
collapsing them is how a safety rule ends up depending on a model's mood:

| Edge | Decided by | Correct use |
|------|-----------|-------------|
| `deterministic` | code / config | schema validation, budget exhaustion, error class, retry limits, required gates — anything whose answer must not vary run to run |
| `model-decided` | the model's judgment | semantic classification, hypothesis selection, which specialist fits, what to try next |
| `policy-decided` | a rule or a human | permission grants, approvals, forbidden transitions, escalation |

**Rules.**

1. **Safety, budget, schema, and error class are never model-decided.** A model may *propose* the next step;
   whether that step is reachable is decided elsewhere. Model output generates candidates; policy and
   deterministic edges control arrival.
2. **A model-decided edge returns a closed set, a confidence, and a fallback** — a label from a declared enum
   (never free text), the confidence that produced it, and where the step goes when confidence is below the
   floor or the label is unrecognized. An unknown label routes to the fallback, never to "best guess".
3. **Never delete a deterministic edge to unblock a model-decided one.** If a route the model wants is
   forbidden, that is the rule working. Route around it or escalate — do not soften the gate.
4. **A missing exit is a schema error, not a prompting problem.** A cycle with no exit edge, or a state
   reachable from nothing, is fixed in the chain definition — never by adding "remember to stop" to a prompt.

## Action Tier Ladder

Guardrail levels grade *how closely a step is watched*. Tiers grade *how much a step is allowed to change*. They are orthogonal: an L2 step can run at any tier, and lowering the tier is often cheaper than raising the level.

| Tier | Effect | Reversal cost | Typical form |
|------|--------|---------------|--------------|
| T0 `answer` | none — information only | zero | analysis, explanation, a located file |
| T1 `propose` | none — candidates only | zero | a plan, options with trade-offs, a chain design |
| T2 `prepare` | local, uncommitted | trivial | a diff, a draft, a branch, a dry-run report, a candidate list |
| T3 `execute-reversibly` | committed but recoverable | bounded | a local commit, a migration with a tested rollback, a feature flag off |
| T4 `execute-consequentially` | external or hard to undo | high or none | push, publish, delete, deploy, send, spend, credential or permission change |

**Rules.**

1. **Uncertainty lowers the tier; it does not have to stop the run.** When confidence is below the floor or a dimension is untyped (`intent-clarification.md` § Uncertainty Typing), execute the same task **one or more tiers down** and deliver that. "I could not safely commit, so here is the diff and the two questions it raises" is a completed T2 run, not a blocked T4 one. The binary ask/proceed gate is the exception path; tier degradation is the default one.
2. **Never auto-promote.** A step may descend tiers freely, ascend only when the uncertainty that capped it is *resolved* — evidence found or the user answered. Re-reading the same request more confidently is not resolution, and neither is a T2 result "looking fine".
3. **T4 is gated by grant, not by confidence.** Reaching T4 requires the step's `Authority` field to allow that effect (Q23) *and* any **Ask First** trigger to be satisfied. High confidence never substitutes for either.
4. **Report the tier you executed at.** A run that delivered at T2 when the request implied T4 states so — that is a `partial` acceptance class with a named blocker, never a silent substitution.

---

## Auto-Recovery Actions

| Trigger | Level | Auto-Recovery |
|---------|-------|---------------|
| test_failure<20% | L2 | Re-run failed tests, fix if obvious |
| test_failure 20-50% | L2 | Inject Builder for targeted fixes |
| test_failure 50-80% | L3 | **Auto-Recovery Chain A** (see below) |
| test_failure>80% | L3 | **Auto-Recovery Chain B** (see below) |
| security_warning | L2 | Add Sentinel scan, block if critical |
| breaking_change | L3 | Pause, verify with Atlas, require migration plan |
| type_error | L2 | Return to Builder for type strengthening |

---

## L3 Auto-Recovery Chains

### Chain A: Test Failure 50-80%

```yaml
L3_RECOVERY_CHAIN_A:
  trigger: test_failure_50_to_80_percent
  confidence_threshold: 0.75  # Auto-execute if >= 0.75

  steps:
    1_analyze:
      agent: Scout
      action: Analyze failing tests, identify root cause patterns
      output: failure_analysis

    2_targeted_fix:
      agent: Builder
      action: Fix identified issues based on failure_analysis
      constraints:
        - Focus on failing tests only
        - Preserve passing test behavior
      output: fixes_applied

    3_verify:
      agent: Radar
      action: Run affected tests
      output: test_results

  success_criteria:
    - test_pass_rate >= 90%
    - no_new_failures

  max_attempts: 2

  on_failure:
    action: escalate_to_chain_b
    reason: "Chain A recovery failed after 2 attempts"
```

### Chain B: Test Failure >80% (Severe)

```yaml
L3_RECOVERY_CHAIN_B:
  trigger: test_failure_over_80_percent OR chain_a_failed
  confidence_threshold: 0.70  # Lower threshold, more conservative

  steps:
    1_rollback:
      action: git_rollback_to_last_checkpoint
      preserve: uncommitted_analysis_notes
      output: clean_state

    2_decompose:
      agent: Sherpa
      action: Break task into smaller, testable increments
      constraints:
        - Each increment must be independently testable
        - Identify the problematic increment
      output: task_breakdown

    3_incremental_fix:
      agent: Builder
      action: Implement smallest increment first
      verify_each: true
      output: incremental_changes

    4_verify:
      agent: Radar
      action: Run full test suite
      output: test_results

  success_criteria:
    - test_pass_rate >= 95%
    - original_goal_achieved

  max_attempts: 1

  on_failure:
    action: escalate_to_user
    message: "Auto-recovery exhausted. Manual intervention required."
    provide:
      - failure_analysis
      - attempted_fixes
      - rollback_command
```

### Chain C: Breaking Change Recovery

```yaml
L3_RECOVERY_CHAIN_C:
  trigger: breaking_change_detected
  confidence_threshold: 0.80

  steps:
    1_impact:
      agent: Atlas
      action: Analyze impact scope, identify affected consumers
      output: impact_analysis

    2_decision:
      condition: impact_analysis.affected_consumers > 0
      if_true:
        action: generate_migration_plan
        agent: Builder
      if_false:
        action: proceed_with_change

    3_migrate_or_fix:
      agent: Builder
      action: |
        IF migration_plan: implement migration
        ELSE: adjust change to be non-breaking
      output: resolution

    4_verify:
      agent: Radar
      action: Run integration tests
      output: verification

  on_failure:
    action: escalate_to_user
    reason: "Breaking change requires user decision"
```

---

## Recovery Confidence Calculation

```yaml
recovery_confidence:
  base_score: 0.60

  boosters:
    - similar_recovery_succeeded_before: +0.15
    - rollback_point_available: +0.10
    - clear_failure_pattern: +0.10
    - small_change_scope: +0.05

  penalties:
    - previous_recovery_failed: -0.20
    - unclear_failure_cause: -0.15
    - large_change_scope: -0.10
    - no_rollback_available: -0.10
```

### Recovery Confidence Bands

Always compute the score with the weighted formula above; the bands below only say what to do with it and how to name it when reporting. A chain's own `confidence_threshold` (A 0.75 / B 0.70 / C 0.80) is the authoritative auto-execute gate for that chain and overrides the generic band.

| Score | Band | Action |
|-------|------|--------|
| ≥ 0.75 | HIGH | Auto-execute the recovery chain |
| 0.60 – 0.74 | MEDIUM | Execute with caution in AUTORUN_FULL; otherwise ask the user |
| < 0.60 | LOW | Ask the user before recovering |

---

## Recovery Decision Flow

```
L3 Guardrail Triggered
         │
         ▼
┌─────────────────────┐
│ Calculate Recovery  │
│    Confidence       │
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    ▼             ▼
 >= 0.75       < 0.75
    │             │
    ▼             ▼
 Auto-Execute   Ask User
 Recovery      (if not AUTORUN_FULL)
 Chain            │
    │             ▼
    │         User Decision
    │             │
    └──────┬──────┘
           ▼
    Execute Recovery
           │
    ┌──────┴──────┐
    ▼             ▼
 Success       Failed
    │             │
    ▼             ▼
 Continue      Try Next
               Chain OR
               Escalate
```

---

## Guardrail Event Format

```
_GUARDRAIL_EVENT:
  Level: [L1|L2|L3|L4]
  Trigger: [What triggered this]
  Step: [X/Y]
  Agent: [Current agent]
  Action: [CONTINUE|VERIFY|PAUSE|ROLLBACK|ABORT]
  Details: [Specifics]
  Recovery: [Recovery action if applicable]
```

### Permission Request Envelope (when the event asks a human to approve an effect)

`Level` + `Trigger` + `Action` describe *what the harness noticed*. They do not describe what the approver is
being asked to accept. An approval prompt that names only the operation ("run `deploy.sh`?", "allow network?")
makes the human the rubber stamp on a decision they were not given the inputs for. Any `PAUSE` that requests
approval for a **T3/T4 effect** (§ Action Tier Ladder) carries these four fields in addition to the event:

```
  Destination: [where the effect lands — host, repo, branch, recipient, tenant, environment]
  Data_classes: [what leaves or is written — public | internal | confidential | secret]
  Blast_radius: [file | repository | machine | account | external system | production]
  Reversibility: [undo | version/backup | compensating action | manual recovery | none]
  Alternative:  [the narrower action considered and why it is insufficient — or "none"]
```

**Rules.**

1. **Missing fields cap the tier, not the flow.** An envelope that cannot state destination and reversibility
   executes one tier down (deliver the diff, the plan, the dry-run) — it does not proceed on an incomplete
   approval, and it does not simply stop.
2. **Approval is scoped to this request.** A granted approval covers the stated destination and payload, once.
   Widening it to the session, the command family, or "similar calls" is escalation without a decision — the
   next call raises its own envelope. Watch for the failure directly: a wrapper approved once, then reused for
   redirect, subshell, or edited-script variants of the same command.
3. **A reviewing agent never fills the approver's seat.** A second agent may assemble the envelope and
   critique it; the grant itself belongs to a human or a policy engine outside the producing agent's trust
   domain. Evaluation independence (`_common/LOOP_PRECONDITIONS.md` #3) is about grading output — it does not
   transfer authority.
4. **`Alternative: none` is a claim that gets checked.** Most T4 requests have a T2 form (produce the artifact,
   let a human ship it). Recording that it was considered is what keeps T4 rare.
5. **A denial is a result, not an absence.** Return it structured — `decision: deny` plus a reason code
   (`out_of_grant` · `unapproved_destination` · `data_class_too_high` · `irreversible_without_approval` ·
   `budget_exhausted` · `stale_policy`) — so the run can route on it. A denial with no reason code is
   indistinguishable from a crash, and the step will simply be retried.
6. **Reaching the same effect through a different tool is escalation, not a workaround.** After a denial,
   trying a second tool, a broader command, or a differently-shaped call that lands the same effect
   ("tool shopping") is the denial being bypassed. Treat it as a `policy_denial` repeat
   (`error-handling.md` § Tool Error Classes — terminal, never rephrased past).
7. **Grants are evaluated at use, not at discovery.** What a tool *offers* is discovered once; whether this
   call may use it is decided per call. A revoked or expired grant that still sits in a cached capability list
   is `stale_policy` — check at request time, keep the cache TTL short, and treat a revocation as an event
   that invalidates, not as something the next lookup will notice eventually.

---

## Context Hierarchy

```
L1_GLOBAL (Chain-wide)
├── goal: "User's original request"
├── acceptance_criteria: ["Criterion 1", "Criterion 2"]
├── chain_overview: "Agent1 → Agent2 → Agent3"
└── shared_knowledge: {key findings from all agents}

L2_PHASE (Per phase)
├── phase_inputs: {data entering this phase}
├── phase_outputs: {data produced by this phase}
└── dependencies: {what this phase needs/provides}

L3_STEP (Per agent step)
├── artifacts: [files, commands, links]
├── decisions: [key choices made]
└── risks: [identified risks]

L4_AGENT (Agent-specific)
├── agent_state: {internal state}
└── pending_confirmations: {questions for user}
```

---

## State Record Format

```
_NEXUS_STATE:
  Task: [Task name]
  Type: [BUG|INCIDENT|API|FEATURE|REFACTOR|OPTIMIZE|SECURITY|DOCS|INFRA]
  Mode: [AUTORUN_FULL|AUTORUN|GUIDED|INTERACTIVE]
  Phase: [PLAN|PREPARE|CHAIN_SELECT|EXECUTE|AGGREGATE|VERIFY|DELIVER]
  Chain: Agent1(DONE) → Agent2(DOING) → Agent3(PENDING)
  Step: [X/Y]
  Status: [ON_TRACK|BLOCKED|RECOVERING|PAUSED]
  Guardrail: [L1|L2|L3|L4] - [Last event summary]
  Acceptance: [Condition1: OK | Condition2: PENDING | ...]
```

---

## Parallel Branch Context

```
_PARALLEL_CONTEXT:
  main_context: [snapshot_id of fork point]
  branches:
    - branch_id: A
      context_delta: {...}
    - branch_id: B
      context_delta: {...}
  merge_strategy: [CONCAT|OVERRIDE|MANUAL]
```


## Safety Contract (SKILL.md excerpt)

- **Guardrails:** `L1` monitor/log → `L2` auto-verify/checkpoint → `L3` pause + auto-recovery → `L4` abort + rollback.
- **Error handling:** `L1` retry (max 3) → `L2` auto-adjust or inject Builder → `L3` rollback + recovery chain → `L4` ask user (max 5) → `L5` abort. **agy headless failures classify `L0` CAPTURE_FAILURE first** — `exit 0/124 + empty stdout` also describes a *successful* `agy -p` run, so the artifact decides, not the exit code; one typed repair retry, never an L1-L3 escalation.
- **Circuit breaker:** an agent failing 3 consecutive tasks is marked DEGRADED and routed around until a probe succeeds. "Agent Tennis" (two agents disagreeing 3+ turns without progress) trips the breaker and escalates.
- **Checkpoint-resume:** Chains with 4+ steps persist step outputs at each boundary so interrupted runs resume from the last checkpoint.
- **Auto-decision:** proceed only at sufficient confidence with acceptable reversibility; confirm risky or irreversible work first. Confirmation depth follows the per-task-type Autonomy Ledger and never relaxes an Ask First gate.
- **Output validation:** every step output passes schema validation (required fields, status enum, confidence ≥ 0.6) before flowing onward; semantic failures (right schema, wrong meaning) need domain checks. Three success layers, checked separately: **transport** (the step returned), **syntactic** (the envelope validates), **semantic** (the content serves the goal, cites what it claims, stays inside its authority). A chain that monitors only the first two reports `SUCCESS` on confidently wrong work, because that is exactly what it looks like from the outside.
- **Always confirm:** the triggers enumerated in **Boundaries → Ask First**.

## Verification Debt Guardrail

Generation is instant; verification is not. A chain that spawns faster than it can verify accumulates unverified state until it stops being knowable which steps are safe — the orchestration-layer form of the same failure `_common/EVIDENCE_LADDER.md` §5 describes.

**Bound agent WIP, not just agent count.** Agent count caps concurrency; WIP caps *unverified output in flight*. Two agents producing changes nobody has validated is worse than four whose output is being consumed.

| Signal | Read as |
|--------|---------|
| generated-vs-verified gap widening across steps | stop spawning; drain before adding |
| step results accepted on schema validity alone, no semantic check | E0 evidence flowing as E3 — see EVIDENCE_LADDER §2 |
| open `not_verified` / `RES-n` items with no risk class or deadline | debt has become permanent, not temporary |
| a verifier agent whose only input is the producer's own summary | Circular Verification at the chain layer |
| rework rate rising while throughput looks flat | the chain is re-doing, not progressing |

**Response, in order:** pause dispatch → drain highest-risk and oldest first → delete branches/artifacts no longer wanted rather than carrying them → repair the test signal itself before adding verification steps (a suite nobody trusts adds no evidence however often it runs).

**Reporting:** a chain that produced more than it verified reports `PARTIAL` with the unverified surface named, never `SUCCESS`. A temporary gap is normal; a gap with no owner and no deadline is the defect.

