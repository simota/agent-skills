# Nexus Guardrail System Reference

**Purpose:** Guardrail **states** (L1 MONITORING → L4 ABORT), per-task-type checkpoint config, Auto-Recovery Chains (A/B/C), and execution-state tracking.
**Read when:** You need to configure or interpret the execution-state guardrail for a task, or look up a Recovery Chain spec.

**Boundary vs `error-handling.md`:** This file owns the **execution-state axis** (L1-L4 guardrail levels + recovery chain definitions + state hierarchy). `error-handling.md` owns the **error-classification axis** (L1 retry → L5 abort by error severity) and invokes Recovery Chains defined here. Both files reference L1-L4, but along different axes — guardrails by state, error-handling by error type.

## Contents
- Guardrail Levels
- Guardrail Configuration by Task Type
- Auto-Recovery Actions
- L3 Auto-Recovery Chains
- Recovery Confidence Calculation
- Recovery Decision Flow
- Guardrail Event Format
- Context Hierarchy
- State Record Format
- Parallel Branch Context

Guardrails, context management, and state tracking for AUTORUN_FULL.

---

## Guardrail Levels

| Level | Name | Trigger | Action |
|-------|------|---------|--------|
| L1 | MONITORING | minor_warning, lint_warning | Log only, continue execution |
| L2 | CHECKPOINT | test_failure<20%, security_warning | Auto-verify, conditional continue |
| L3 | PAUSE | test_failure>50%, breaking_change | Pause, attempt auto-recovery |
| L4 | ABORT | critical_security, data_integrity_risk | Immediate stop, rollback |

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
- **Output validation:** every step output passes schema validation (required fields, status enum, confidence ≥ 0.6) before flowing onward; semantic failures (right schema, wrong meaning) need domain checks.
- **Always confirm:** the triggers enumerated in **Boundaries → Ask First**.

