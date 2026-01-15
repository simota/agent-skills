# Guardrail Protocol

This document defines the guardrail system for safe autonomous execution in AUTORUN_FULL mode.

---

## Overview

Guardrails provide automated safety checks that allow autonomous execution while preventing catastrophic failures.
They replace mandatory human confirmations with intelligent checkpoints.

---

## Guardrail Levels

| Level | Name | Interaction | Use Case |
|-------|------|-------------|----------|
| L1 | MONITORING | None (log only) | Minor warnings, lint issues |
| L2 | CHECKPOINT | Auto-verify | Test failures <20%, security warnings |
| L3 | PAUSE | Auto-recover or wait | Test failures >50%, breaking changes |
| L4 | ABORT | Immediate stop | Critical security, data integrity risk |

---

## Guardrail Triggers

### L1 - MONITORING

Triggers that are logged but don't pause execution:

| Trigger | Description | Action |
|---------|-------------|--------|
| lint_warning | Non-critical lint issues | Log, continue |
| minor_deprecation | Non-breaking deprecation | Log, continue |
| style_inconsistency | Code style variance | Log, auto-fix if possible |
| coverage_decrease_minor | Coverage drop <5% | Log, continue |

### L2 - CHECKPOINT

Triggers that require automated verification:

| Trigger | Description | Action |
|---------|-------------|--------|
| test_failure_minor | <20% tests failing | Auto-fix attempt, retest |
| security_warning | Non-critical security issue | Add Sentinel scan |
| type_error | TypeScript errors | Return to Mason |
| performance_regression | <10% slowdown | Log, optional Bolt |
| dependency_vulnerability | Low/Medium CVE | Log, suggest update |

### L3 - PAUSE

Triggers that pause execution for recovery or escalation:

| Trigger | Description | Action |
|---------|-------------|--------|
| test_failure_major | >50% tests failing | Rollback, re-decompose |
| breaking_change | API/interface change | Pause, verify consumers |
| security_critical | High severity issue | Pause, require Sentinel |
| merge_conflict | Parallel branch conflict | Pause, resolve or escalate |
| build_failure | Build doesn't compile | Rollback, fix attempt |

### L4 - ABORT

Triggers that immediately stop execution:

| Trigger | Description | Action |
|---------|-------------|--------|
| critical_security | Critical CVE, exposed secrets | Abort, rollback |
| data_integrity_risk | Potential data loss/corruption | Abort, rollback |
| infinite_loop_detected | Recovery attempts exceeded | Abort |
| user_abort | User requested stop | Abort |
| system_error | Fatal system failure | Abort |

---

## Guardrail Configuration

### Default Configuration by Task Type

```yaml
GUARDRAIL_CONFIG:
  FEATURE:
    default_level: L2
    pre_checks: []
    post_checks: [tests_pass, build_success]
    escalate_on: [test_failure>50%, security_critical]

  SECURITY:
    default_level: L2
    pre_checks: [sentinel_scan]
    post_checks: [no_new_vulnerabilities, tests_pass]
    escalate_on: [any_security_issue]

  REFACTOR:
    default_level: L2
    pre_checks: []
    post_checks: [tests_unchanged, no_behavior_change]
    escalate_on: [test_failure_any, coverage_decrease]

  API_BREAKING:
    default_level: L3
    pre_checks: [atlas_impact_analysis]
    post_checks: [consumers_updated, migration_ready]
    escalate_on: [consumer_not_updated]

  INCIDENT:
    default_level: L3
    pre_checks: []
    post_checks: [service_restored, no_regression]
    escalate_on: [service_not_restored]

  INFRA:
    default_level: L3
    pre_checks: [dry_run_if_available]
    post_checks: [health_checks_pass]
    escalate_on: [health_check_fail]
```

---

## Guardrail Event Format

When a guardrail is triggered:

```yaml
_GUARDRAIL_EVENT:
  id: [unique event ID]
  timestamp: [ISO timestamp]
  level: [L1|L2|L3|L4]
  trigger: [trigger name]
  step: [X/Y]
  branch: [branch_id or "main"]
  agent: [current agent]
  details:
    description: [what happened]
    evidence: [logs, test output, etc.]
  action:
    type: [CONTINUE|VERIFY|PAUSE|RECOVER|ROLLBACK|ABORT]
    details: [action specifics]
  result:
    status: [SUCCESS|FAILED|ESCALATED]
    next_step: [what happens next]
```

---

## Auto-Recovery Actions

### L2 Recovery Actions

| Trigger | Recovery Action | Max Attempts |
|---------|-----------------|--------------|
| test_failure_minor | Run Mason fix, retest | 3 |
| type_error | Mason type strengthening | 2 |
| lint_error | Auto-fix command | 1 |
| coverage_decrease | Add targeted tests | 2 |

### L3 Recovery Actions

| Trigger | Recovery Action | Max Attempts |
|---------|-----------------|--------------|
| test_failure_major | Rollback + Sherpa decompose | 2 |
| breaking_change | Atlas analysis + migration | 1 |
| merge_conflict | Sequential re-execution | 1 |
| build_failure | Rollback + targeted fix | 2 |

---

## Guardrail Checkpoints

Pre-defined checkpoints in execution flow:

### Mandatory Checkpoints

| Checkpoint | Phase | Level | Check |
|------------|-------|-------|-------|
| POST_IMPLEMENT | After Mason | L2 | Tests pass, types valid |
| PRE_MERGE | Before aggregate | L2 | No conflicts |
| POST_MERGE | After aggregate | L2 | Combined tests pass |
| PRE_DELIVER | Before final | L2 | All acceptance criteria |

### Optional Checkpoints

| Checkpoint | When | Level | Check |
|------------|------|-------|-------|
| POST_SECURITY | After Sentinel | L2 | No new vulnerabilities |
| POST_PERF | After Bolt | L2 | No regression |
| MID_CHAIN | Every 3 steps | L1 | Progress check |

---

## Rollback Protocol

### Rollback Points

Created automatically at:
1. Before EXECUTE phase (full snapshot)
2. Before each branch in parallel mode
3. Before risky operations (per guardrail config)

### Rollback Execution

```yaml
_ROLLBACK:
  trigger: [what triggered rollback]
  rollback_point: [snapshot ID or git ref]
  scope: [STEP|BRANCH|FULL]
  action:
    - Restore state to rollback point
    - Clear partial changes
    - Update context
  next:
    - [RETRY|DECOMPOSE|ESCALATE|ABORT]
```

---

## Agent Guardrail Reporting

Agents report guardrail events in NEXUS_HANDOFF:

```text
## NEXUS_HANDOFF
- Step: 3/7
- Agent: Mason
- Summary: Implemented feature X
- Guardrail Events:
  - Level: L2
  - Trigger: test_failure_minor (2/15 tests failing)
  - Action: auto_fix
  - Result: SUCCESS (all tests now pass)
- Next action: CONTINUE
```

---

## Guardrail Escalation Path

```
L1 (Log) ──────────────────────────────────────┐
    │                                          │
    ▼ (issue persists)                         │
L2 (Checkpoint) ───────────────────────────────┤
    │                                          │
    ├─ auto_recovery_success → CONTINUE        │
    │                                          │
    ▼ (recovery failed)                        │
L3 (Pause) ────────────────────────────────────┤
    │                                          │
    ├─ auto_recovery_success → CONTINUE        │
    ├─ user_confirms → CONTINUE/ADJUST         │
    │                                          │
    ▼ (critical issue or no resolution)        │
L4 (Abort) ────────────────────────────────────┘
    │
    └─ ROLLBACK + STOP
```

---

## Integration with Other Protocols

### With PARALLEL.md
- Each branch has independent L1/L2 guardrails
- L3 pauses only affected branch
- L4 triggers global abort

### With Nexus STATE_MANAGEMENT
- Guardrail events recorded in _NEXUS_STATE
- Recovery attempts tracked
- Escalation history preserved

### With CONTEXT_MANAGEMENT
- Guardrail checkpoints create context snapshots
- Rollback uses context restoration
- Events added to context delta

---

## Guardrail Tuning

### Threshold Adjustment

Thresholds can be adjusted per project:

```yaml
# In .agents/PROJECT.md or project config
GUARDRAIL_THRESHOLDS:
  test_failure_minor_max: 20%  # Default: 20%
  test_failure_major_min: 50%  # Default: 50%
  coverage_decrease_warn: 5%   # Default: 5%
  performance_regression_warn: 10%  # Default: 10%
  max_recovery_attempts: 3     # Default: 3
```

### Disabling Guardrails (Not Recommended)

For specific scenarios, guardrails can be relaxed:

```yaml
## NEXUS_AUTORUN_FULL
guardrail_override:
  skip_pre_checks: true  # Skip pre-execution checks
  allow_test_failure: true  # Continue despite test failures
  reason: "Experimental feature, tests expected to fail initially"
```

**Warning**: Overrides should be used sparingly and with clear justification.
