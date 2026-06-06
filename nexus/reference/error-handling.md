# Nexus Error Handling Reference

**Purpose:** **Error classification** (L1 retry → L5 abort) and escalation flow when a step fails.
**Read when:** A step failed and you need retry, rollback, recovery-chain invocation, escalation, or abort rules.

**Boundary vs `guardrails.md`:** This file owns the **error-severity axis** (L1 AUTO_RETRY / L2 AUTO_ADJUST / L3 ROLLBACK / L4 ESCALATE / L5 ABORT). `guardrails.md` owns the **execution-state axis** (L1 MONITORING / L2 CHECKPOINT / L3 PAUSE / L4 ABORT) and defines the Recovery Chains (A/B/C) that L3 here invokes. Both files use L1-L4 numbering along different axes — do not conflate them.

## Contents
- Error Levels
- Recovery Flow
- Error Event Format
- Recovery Chain Integration

Error levels, recovery flow, and escalation procedures.

---

## Error Levels

### Level 1 - AUTO_RETRY (Transient Errors)
- Syntax error → Re-execute with the same agent (max 3 retries)
- Test failure (1st time) → Fix with Builder and retest
- Lint error → Auto-fix
- Network timeout → Retry with backoff

### Level 2 - AUTO_ADJUST (Recoverable Issues)
- test_failure<50% → Inject recovery agent (Builder for fixes)
- Type errors → Return to Builder for type strengthening
- Minor security warning → Add Sentinel scan step
- Performance degradation detected → Insert Bolt

### Level 3 - ROLLBACK (Significant Failures)
- test_failure 50-80% → **Auto-Recovery Chain A** (Scout → Builder → Radar)
- test_failure >80% → **Auto-Recovery Chain B** (Rollback → Sherpa → Builder → Radar)
- Breaking change detected → **Auto-Recovery Chain C** (Atlas → Builder → Radar)
- Merge conflict in parallel execution → Auto-resolve if adjacent, else Rollback branch

See `guardrails.md` for detailed recovery chain specifications.

### Level 4 - ESCALATE (Human Required)
- Blocking unknowns → Ask user (max 5 questions)
- Missing prerequisites → Pause task, confirm requirements
- External dependency issues → Check environment with Gear
- Recovery failed after 3 attempts → Request human guidance
- Ambiguous acceptance criteria → Clarify with user

### Level 5 - ABORT (Critical Issues)
- No resolution after 3 escalations
- User explicitly requests abort
- Fatal system error
- Critical security vulnerability detected (L4 guardrail)
- Data integrity risk detected

---

## Recovery Flow

```
Error Detected
    │
    ▼
┌─────────────┐
│ Classify    │ → Determine error level
└─────────────┘
    │
    ▼ (L1-L3)
┌─────────────┐
│ Auto-Handle │ → Execute recovery action
└─────────────┘
    │
    ├─ Success → Continue execution
    │
    ▼ (Failed)
┌─────────────┐
│ Escalate    │ → Bump to next level
└─────────────┘
    │
    ├─ L4: Human intervention
    │
    ▼ (No resolution)
┌─────────────┐
│ Abort       │ → L5: Stop and rollback
└─────────────┘
```

---

## Error Event Format

```
_ERROR_EVENT:
  Level: [L1|L2|L3|L4|L5]
  Type: [Error type]
  Step: [X/Y]
  Agent: [Current agent]
  Details: [Error details]
  Action: [Recovery action taken]
  Result: [SUCCESS|FAILED|ESCALATED|ABORTED]
```

---

## Recovery Chain Integration

### Automatic Chain Selection

```yaml
recovery_chain_selection:
  test_failure:
    0-20%: L1_retry
    20-50%: L2_builder_inject
    50-80%: L3_RECOVERY_CHAIN_A
    80-100%: L3_RECOVERY_CHAIN_B

  breaking_change:
    detected: L3_RECOVERY_CHAIN_C

  merge_conflict:
    adjacent_only: auto_merge
    semantic: ownership_priority
    complex: user_escalation
```

### Chain Execution Flow

```
Error Detected
      │
      ▼
┌──────────────┐
│ Classify     │ → Match to recovery chain
│ Error Type   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Check        │ → recovery_confidence >= threshold?
│ Confidence   │
└──────┬───────┘
       │
  ┌────┴────┐
  ▼         ▼
AUTO      ASK
  │         │
  ▼         ▼
Execute   User decides
Chain     which chain
  │         │
  └────┬────┘
       ▼
┌──────────────┐
│ Run Chain    │ → Step by step with checkpoints
└──────┬───────┘
       │
  ┌────┴────┐
  ▼         ▼
SUCCESS   FAILED
  │         │
  ▼         ▼
Continue  Next chain
          OR escalate
```

### Recovery Event Format

```yaml
_RECOVERY_EVENT:
  chain: [CHAIN_A|CHAIN_B|CHAIN_C]
  trigger: [What triggered recovery]
  confidence: 0.XX
  auto_executed: [true|false]

  steps:
    - step: 1
      agent: [Agent]
      action: [What was done]
      result: [SUCCESS|FAILED]

  outcome: [RECOVERED|ESCALATED|ABORTED]
  duration: [steps completed]
  artifacts:
    - [List of recovery artifacts]
```

### Recovery Metrics

Track recovery performance:

```yaml
recovery_metrics:
  chain_a:
    attempts: N
    success_rate: X%
    avg_confidence: 0.XX

  chain_b:
    attempts: N
    success_rate: X%
    avg_confidence: 0.XX

  chain_c:
    attempts: N
    success_rate: X%
    avg_confidence: 0.XX

  escalation_rate: X%  # Target: < 15%
```
