# Nexus Error Handling Reference

**Purpose:** **Error classification** (L1 retry → L5 abort) and escalation flow when a step fails.
**Read when:** A step failed and you need retry, rollback, recovery-chain invocation, escalation, or abort rules.

**Boundary vs `guardrails.md`:** This file owns the **error-severity axis** (L1 AUTO_RETRY / L2 AUTO_ADJUST / L3 ROLLBACK / L4 ESCALATE / L5 ABORT). `guardrails.md` owns the **execution-state axis** (L1 MONITORING / L2 CHECKPOINT / L3 PAUSE / L4 ABORT) and defines the Recovery Chains (A/B/C) that L3 here invokes. Both files use L1-L4 numbering along different axes — do not conflate them.

**Boundary vs the Handoff Admission Gate:** this file owns **a step that failed**. `_common/HANDOFF.md` § Handoff Admission Gate owns **a step that succeeded and delivered something the receiver cannot work from**. The two never share a path: a refusal is not an `L1` retry, it consumes the edge's single bounce rather than an attempt budget, and it returns work to the *sender* rather than re-running it in place.

## Contents
- Error Levels (incl. Tool Error Classes — the orthogonal *what kind* axis)
- Context Failure Classes (what was wrong *before* the call) + the Context Diff
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

### Delegation Cycles and Waits (the failures that look like "still running")

Hop limits stop a task bouncing between the same two agents. They do not stop a task travelling a longer
loop, and they do not stop a run where nothing is looping at all — everyone is simply waiting.

**Circulating task.** Carry `task_id`, `hop_count`, and the set of agents already visited *in the delegation
message itself*. A task arriving at an agent that has already handled this `task_id` is denied at receipt —
the check is on task identity, not on pair frequency, because `A → B → C → A` never trips a per-pair budget.

**Mutual wait.** A waits on B's artifact while B waits on A's approval; both are healthy, neither progresses,
and no error is ever raised. Track the wait edges — who is blocked on whom — and treat a cycle among them as a
failure, not as latency. Each wait carries a deadline; when the cycle is detected or a deadline expires, one
side is chosen to proceed or abort by a fixed rule, never by whoever times out first.

**Shared retry budget.** One specialist timing out can trigger a supervisor retry, a sibling's fallback, and
a fresh tool storm — each locally reasonable, together an amplification. Retry budget is held by the *run*,
not by each participant, and the circuit breaker trips on the run's total, not per agent.

**Ownership.** Every in-flight task has exactly one owner for its final answer and its cancellation. An
unowned task is the state in which each party assumes another is watching it — and it is indistinguishable
from progress until the deadline.

### Observation Point ≠ Origin (locate before you fix)

The stage that *reported* a failure is rarely the stage that *produced* it. A gate failing at VERIFY often
means the intent was never bounded at CLASSIFY; a wrong-file edit reported at AGGREGATE usually means scope
was never declared. Fixing where the symptom surfaced adds a check that catches the same failure one step
later, forever.

Split every diagnosis into two named answers before proposing a fix:

```
observed_at:  <phase / step where it became visible>
originated_at: <phase / artifact that produced the condition>
```

Common misattributions, and where the fix actually belongs:

| Symptom | Reported at | Usually originates in |
|---------|-------------|----------------------|
| agent repeats a superseded command or API | EXECUTE | stale instruction or memory — retained context, not the step |
| edits land outside the intended area | AGGREGATE / review | scope never declared in the spawn prompt |
| the same correction is needed run after run | VERIFY | acceptance criteria absent or unmeasurable at CLASSIFY |
| diff far larger than the task | review | non-goals unstated; write scope unbounded |
| a step "passes" but the result is wrong | VERIFY | the check is not independent of the producer (`_common/EVIDENCE_LADDER.md` §2) |
| only the delegated/background run fails | EXECUTE | environment or context parity between surfaces, not the agent |

**Rules.**

1. **A fix at the observation point is provisional.** It may stop the bleeding; it does not close the failure.
   Record which one you applied.
2. **Prevention names a layer, not a paragraph.** "Be more careful" and "add this to the prompt" are the null
   fixes — the durable ones change the instruction file, the tool contract, the permission grant, or the gate.
3. **Two identical signatures ⇒ locate, do not retune.** Repetition means the origin was never found; another
   parameter tweak is Q20 thrash.

### Tool Error Classes (orthogonal to L0-L5 severity)

Severity answers *how hard to escalate*. It does not answer *what kind of wrong this is* — and a tool failure's
class, not its severity, decides whether retrying is even meaningful. Classify first, then pick the level.

| Class | Signature | Correct response |
|-------|-----------|------------------|
| `invocation` | Schema mismatch, missing required argument, malformed call | Fix the call. Retrying it unchanged is a Failure Signature repeat, not an attempt |
| `transport` | Network error, timeout **with no side effect possible** | L1 retry with backoff — the only class where a bare retry is legitimate |
| `execution` | The command ran and genuinely failed (test red, build broken) | Not a tool problem. Diagnose the work, not the call |
| `partial_success` | Some units succeeded, others did not | Re-scope to the failed subset. Re-running the whole thing repeats side effects |
| `state_conflict` | Revision / resource-version mismatch, stale precondition | Re-read current state, **update the plan**, then act. Never force |
| `policy_denial` | Permission, safety, or guardrail rejection | Stop and escalate. **Never rephrase the prompt or reshape the call to get past it** — that is bypassing a control, not recovering from an error |
| `unknown_outcome` | Timeout or crash where a side effect **may** have landed | Query the external state before anything else. Do not retry, and do not summarize as "failed" |

**Two classes are load-bearing:**

- **`policy_denial` is terminal for the agent.** Working around a denial is the failure mode the denial exists
  to prevent (`_common/BOUNDARIES.md`). Report it; do not route around it.
- **`unknown_outcome` must not collapse into "failed".** Compressing it loses the fact that the effect may
  already exist — the next session then repeats a non-idempotent action. Carry it forward verbatim as
  `unknown_outcome` with the resource to check, and confirm actual state before retrying. `L0 CAPTURE_FAILURE`
  (above) is the agy-specific instance of exactly this class: `exit 0` + empty stdout describes both a success
  and a failure, so the artifact decides, not the exit code.

### Context Failure Classes (orthogonal to both severity and Tool Error Classes)

Tool Error Classes above classify **how a call went wrong**. This axis classifies **what was already wrong in
the information the agent was given** — a failure that has usually completed before any tool is invoked, and
that a correct-looking tool call will faithfully execute. A step that "succeeded" while acting on a superseded
ADR belongs here, not above.

| Class | Mechanism | Detection | Permanent fix |
|-------|-----------|-----------|---------------|
| `omission` | A required fact was never composed in | The agent's rationale never cites the constraint it violated | Add the source to the step's required set |
| `overload` | Required fact present but drowned | Correct fact is quotable from context yet unused | Cut volume, not sources — see the Preserve Set |
| `conflict` | Two composed sources disagree, unflagged | Two retrieved items assert incompatible values | Surface the conflict; resolve by authority, not by order |
| `staleness` | Composed fact was true, no longer is | Source revision ≠ the revision the claim was made against | Freshness typing + `invalidate_on` (`_common/HANDOFF.md`) |
| `misrouting` | Right context, wrong consumer | A step acts outside the scope it was briefed on | Fix the routing/scoping, not the agent |
| `wrong_authority` | A non-authoritative source drove a decision | Decision traced to chat/issue/draft over spec/ADR/policy | Per-question authority (`_common/CONTEXT_SUFFICIENCY.md`) |
| `retrieval_failure` | The item never entered the candidate set | Item exists and is authorized but was never a candidate | Ingestion / index / query — **not the reranker** |
| `ranking_failure` | It was a candidate and lost | Item in candidates, below the cut | Reranking / budget — **not ingestion**. Kept separate from the row above because the fix location differs |
| `summary_drift` | Compaction changed the claim's meaning | Hedged statement returns as a flat assertion | Category-count compression check (`context-strategy.md`) |
| `memory_pollution` | A stale/unverified belief persisted forward | A carried claim has no live source or contradicts current state | Memory write/forget governance (`oracle/reference/agent-design.md`) |
| `instruction_collision` | Two layers give incompatible directives | Two applicable rules cannot both hold | Declared precedence; unresolvable ⇒ stop, do not guess |
| `context_poisoning` | Untrusted content was read as instruction | Retrieved text steers behavior | `_common/WEB_FETCH_SAFETY.md` instruction-eligibility gate |
| `secret_leakage` | A credential entered the window | Secret value appears in prompt/args/logs | Tool-gateway pattern — resolve credentials inside the tool |
| `scope_leakage` | Data crossed a tenant/classification line | Composed set includes out-of-scope records | Gate before rank, not after |
| `hidden_dependency` | A load-bearing fact lived only outside the sources | Behavior depends on a flag/env/runtime state never composed | Add the runtime source to the inventory |
| `tool_context_mismatch` | Tool schema/permissions ≠ what the agent assumed | Call is well-formed but semantically wrong for this environment | Refresh tool context per phase |

**Trigger is not root cause.** A document update that invalidated an index is the *trigger*; the *root cause*
is that nothing rebuilt the index. Recording the trigger as the cause produces a fix that prevents nothing.

#### The Context Diff — localize the stage before changing anything

Run the subtraction top-down. Each line names one stage and one owner; the first non-empty line is where the
failure lives.

```
required   − retrieved  = retrieval omission      → ingestion / index / query
retrieved  − eligible   = policy/authority filter → permissions, scope, classification
eligible   − composed   = budget/composition drop → budget order, degradation step
composed   − consumed   = attention/utilization   → volume, position, format
consumed   − current    = staleness / wrong authority → freshness typing, authority
```

**Do not change the model, the prompt, or the reranker first.** Any of those alters the sets being subtracted
and the diff stops meaning anything. Localize, then fix the one stage. This is the context-side counterpart of
the Failure Signature rule above: an unlocalized change is not an attempt.

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
- Tool-call error → classify against **§ Tool Error Classes** *before* retrying. Only `transport` is bare-retryable; `invocation` (schema mismatch, malformed call, missing argument) must have the call **changed** before re-running, and `execution` is diagnosed, not retried
- Network timeout → Retry with backoff (max 3)
- Test failure (1st time) → Fix with Builder and retest
- Lint error → Auto-fix

> Re-issuing an `invocation` failure unchanged is a Failure Signature repeat, not an attempt, and does not consume a legitimate retry — it consumes the budget without changing anything.

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

  escalation_rate: X%  # Acceptable band: 8-30%; both bounds are alerts
```

**Escalation is two-sided.** A one-sided `< N%` target rewards suppressing escalation, which buys the number by answering confidently where the chain should have stopped. Too *low* on a risk-bearing workload is the more dangerous reading: it means the system is deciding things it was not equipped to decide. Set the band from the workload's own risk profile rather than reusing these defaults, and alert on both edges.
