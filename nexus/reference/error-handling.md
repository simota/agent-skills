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

### Level 0 - CAPTURE_FAILURE (agy headless only — classify before L1)

**Applies when the hub is agy and the step ran as headless `agy -p`.** On that path an *empty result is not evidence of a failed step*: `agy -p` never flushes to a non-TTY stdout, so `exit 0 + empty stdout` is exactly what a **successful** run looks like, and `exit 124 + empty stdout` is the pty-less silent hang (`_common/CLI_COMPATIBILITY.md §9.2`, issues #76/#115/pty). Sending such a step into L1 retry re-runs work that may already be done and burns quota; sending it to L3 rollback discards a completed step.

Classify a missing/empty artifact **before** assigning an error level:

| Observation | Verdict | Action |
|-------------|---------|--------|
| Artifact non-empty **and** ends with `<<<END_OF_OUTPUT>>>` | Step succeeded | Continue — read `_STEP_COMPLETE` from the artifact, not stdout |
| Artifact missing/empty, **transcript shows model content** (`PLANNER_RESPONSE` / `status=DONE`) | **Capture failure, not task failure** | **Typed retry, max 1**, with the repair directive: "the previous run did not write the file — rewrite your full output to `/tmp/agy-<slug>.md`". Never loop blindly |
| Artifact and transcript both empty, `--log-file` shows quota / OAuth / executor error | Runtime failure | Escalate per the log verdict — quota/auth → **L4** (human), executor error → **L1** retry once |
| Artifact and transcript both empty, no log file at all | pty was not allocated | Not an agent error — re-spawn under `python3 pty.spawn` (`script -q /dev/null` does **not** work). Does not count against the L1 retry budget |
| Artifact present and sentinel present, but content fails the step's acceptance check | Genuine task failure | Fall through to L1-L5 below as normal |

**Rule:** an agy step is never escalated past L0 on the strength of empty stdout alone, and the exit code is never the deciding signal — the artifact is. Capture failure is also **not** a REVISE signal in an evaluator loop (`orchestration-patterns.md` § Pattern H → agy Implementation).

### Failure Signature (identity of a repeated failure)

Retry budgets are meaningless without a definition of "the same failure". Before counting a retry, compute the signature:

```
Failure Signature = stage + error_code + normalized_location + relevant_state_hash
```

- `stage` — which phase produced it (EXECUTE step n, VERIFY, AGGREGATE)
- `error_code` — the machine-readable code, not the prose message
- `normalized_location` — file/symbol with line numbers and run-specific paths stripped
- `relevant_state_hash` — digest of the inputs the step actually consumed

**Rule:** a retry is only legitimate when the **action or the evidence changed**. Two runs producing the same signature are not two attempts — they are one attempt counted twice, and the second one is Q20 thrash (`autonomy-quality-protocol.md` §0: *two identical failures ⇒ stop and diagnose*). Count identical signatures toward the circuit breaker, not toward the retry budget.

### Reset vs Retry vs Rollback (do not substitute one for another)

| Operation | Purpose | Preserves | Discards |
|-----------|---------|-----------|----------|
| **Compaction** | Free context, keep going | Verified facts, decisions, current state, next action | Superseded detail, duplicated text |
| **Reset** | Remove a contaminated context | Durable checkpoint + artifacts only | The entire working context |
| **Checkpoint** | Make the run resumable | Task state, artifacts, verification result, environment fingerprint | Nothing |
| **Rollback** | Return to a known-safe state | The checkpoint being restored to | Work since that checkpoint |

Summarizing is **not** checkpointing: a compaction that loses the resume contract has produced an unresumable run that still looks healthy.

**Reset triggers** — reset the context rather than retrying when any of these holds:

1. The same Failure Signature has occurred `≥ 2` times
2. The plan and the actual workspace state disagree
3. The context contains directly conflicting instructions
4. The agent referenced a file, tool, or symbol that does not exist
5. Remaining token budget is below what one full step needs
6. Untrusted content is suspected of steering the run
7. Checkpoint integrity check failed

Triggers 6 and 7 escalate rather than reset silently — see L4/L5.

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
  Level: [L0|L1|L2|L3|L4|L5]   # L0 = agy capture failure (see Level 0)
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
