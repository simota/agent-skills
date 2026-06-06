# Runbook Execution Protocol

Purpose: Read this file when parsing, validating, dry-running, or executing a Triage-authored runbook under Mend guardrails.

## Contents

- Runbook parsing
- Pre-execution validation
- Step execution and state machine
- Guardrails, retries, and branching
- Dry-run and completion reports

How Mend parses, validates, and executes runbooks provided by Triage. Every runbook execution follows strict guardrails.

---

## Runbook Parsing

### Expected Runbook Format

Triage provides runbooks in the following structure:

```markdown
## Runbook: [Title]
Incident: [incident_id]
Severity: [SEV1-4]
Author: Triage

### Prerequisites
- [ ] Condition 1
- [ ] Condition 2

### Steps
1. [Action] → Expected: [outcome]
2. [Action] → Expected: [outcome]
3. [Action] → Expected: [outcome]

### Rollback
1. [Reverse action for step 3]
2. [Reverse action for step 2]
3. [Reverse action for step 1]

### Verification
- [ ] Check 1
- [ ] Check 2
```

### Parsing Rules

1. Extract all steps as ordered list — preserve sequence
2. Extract prerequisites as pre-execution checklist
3. Extract rollback steps — map to corresponding forward steps (reverse order)
4. Extract verification criteria as post-execution checklist
5. If any section is missing: flag as incomplete, request Triage clarification

---

## Pre-Execution Validation

Before executing any step, validate:

| Check | Action if Failed |
|-------|-----------------|
| All prerequisites met | Pause — request prerequisite resolution |
| Each step has expected outcome | Warn — proceed with enhanced monitoring |
| Rollback steps exist for each forward step | Warn — create rollback plan before proceeding |
| Safety tier classified for each step | Block — classify before execution |
| No T4 actions in runbook | Block — escalate T4 steps to human |
| Runbook author is Triage (or authorized) | Block — reject unauthorized runbooks |

---

## Step Execution Protocol

### Sequential Execution

```
For each step in runbook:
  1. PRE-CHECK
     - Verify prerequisites for this step
     - Confirm safety tier classification
     - Record pre-step system state (snapshot)

  2. EXECUTE
     - Run step action
     - Monitor for unexpected side effects
     - Enforce timeout (default: 5 min per step)

  3. VERIFY
     - Compare actual outcome to expected outcome
     - If match: record success, proceed to next step
     - If mismatch: evaluate severity
       - Minor deviation: log warning, proceed
       - Major deviation: pause execution
       - Critical deviation: trigger rollback

  4. CHECKPOINT
     - Record post-step state
     - Confirm rollback capability
     - Log step completion to incident timeline
```

### Step State Machine

```
PENDING → EXECUTING → VERIFYING → COMPLETED
                ↓           ↓
            TIMED_OUT   FAILED
                ↓           ↓
            RETRY(1)    ROLLBACK
                ↓
            RETRY(2)
                ↓
            ESCALATE
```

---

## Guardrails

### Timeout Management

| Context | Default Timeout | Override |
|---------|----------------|---------|
| Individual step | 5 minutes | Configurable per step (max 15 min) |
| Total runbook | 30 minutes | Configurable (max 60 min) |
| Verification wait | 2 minutes | Configurable per check (max 5 min) |
| Rollback step | 5 minutes | Same as forward step |

When timeout is reached:
1. Record current state
2. Attempt graceful cancellation
3. If step is partially applied: evaluate rollback need
4. Log timeout with context for postmortem

### Idempotency Requirements

Every runbook step must be idempotent — safe to re-run without side effects. Non-idempotent retries are a top failure mode in runbook automation (e.g., scaling out twice, applying config change twice).

| Requirement | Detail |
|-------------|--------|
| **Pre-retry state check** | Before retrying, verify the step hasn't already been applied (check post-condition) |
| **Idempotency assertion** | Each step must declare how idempotency is achieved (e.g., "set to X" not "increment by X") |
| **Convergent actions** | Prefer declarative state (desired state) over imperative mutations (change commands) |
| **Guard clauses** | Steps should check current state before acting: skip if already in target state |

If a step cannot be made idempotent, it must be classified as **T3 minimum** (approval required) regardless of other risk factors.

### Conditional Branching

Runbooks may include conditional logic for multi-path remediation:

```
Step N: Check condition
  ├── If [condition A] → Execute Step N+1a
  ├── If [condition B] → Execute Step N+1b
  └── If [neither] → Escalate
```

**Rules:**
- Each branch must have its own rollback path
- Branch conditions must be evaluable from observable system state (not assumptions)
- Maximum nesting depth: 2 levels (to maintain comprehensibility)
- Default branch must always exist (typically: escalate)

### Retry Policy

| Condition | Action |
|-----------|--------|
| Transient failure (network timeout, temporary unavailability) | Retry up to 2 times with exponential backoff (10s, 30s) — **only if step is idempotent** |
| Deterministic failure (permission denied, invalid config) | No retry — escalate immediately |
| Partial success (some targets applied, others failed) | Retry failed targets only — **verify unapplied state first** |
| After 2 failed retries | Stop retrying — escalate to Triage |

### Blast Radius Re-evaluation

After each step, re-evaluate blast radius:

```
If actual_blast_radius > classified_blast_radius:
  PAUSE execution
  Reclassify safety tier
  If new tier requires higher approval: request approval
  If new tier is T4: halt and escalate
```

### Abort Conditions

Immediately abort runbook execution when:

| Condition | Action |
|-----------|--------|
| Unexpected service goes down | Abort + rollback completed steps |
| Error rate spikes in unrelated service | Abort + investigate correlation |
| Data integrity alert fires | Abort + escalate to T4 handling |
| Rollback capability lost | Abort + escalate immediately |
| Step produces output outside expected range | Pause + evaluate before continuing |

---

## Dry-Run Mode

For T3 actions and uncertain situations, Mend supports dry-run execution:

### Dry-Run Protocol

1. Execute all validation and pre-checks as normal
2. Simulate each step and report expected outcome
3. Show complete execution plan with risk assessment
4. Present to approver with:
   - Actions to be taken
   - Expected outcomes per step
   - Risk score per step
   - Rollback plan
   - Total estimated duration
5. Await explicit approval before actual execution

### Dry-Run Output Format

```markdown
## Dry-Run Report: [Runbook Title]

### Execution Plan
| Step | Action | Safety Tier | Risk Score | Expected Outcome |
|------|--------|-------------|------------|------------------|
| 1 | ... | T2 | 4 | ... |
| 2 | ... | T3 | 18 | ... |

### Risk Assessment
- Total Risk Score: [sum]
- Highest Tier: [T3]
- Estimated Duration: [X min]

### Rollback Plan
| If Step N Fails | Rollback Action | Time to Rollback |
|-----------------|-----------------|------------------|
| Step 2 | ... | < 5 min |
| Step 1 | ... | < 1 min |

### Approval Required
- [ ] Approve execution
- [ ] Approve with modifications: ___
- [ ] Reject — reason: ___
```

---

## Runbook Completion Report

After runbook execution (success or failure), generate:

```markdown
## Runbook Execution Report

**Incident:** [incident_id]
**Runbook:** [title]
**Status:** SUCCESS / PARTIAL / FAILED / ABORTED
**Duration:** [start_time] → [end_time] ([total duration])

### Steps Executed
| Step | Action | Status | Duration | Notes |
|------|--------|--------|----------|-------|
| 1 | ... | SUCCESS | 30s | |
| 2 | ... | SUCCESS | 2m | Retry 1 required |
| 3 | ... | FAILED | 5m (timeout) | Escalated |

### Rollback Actions (if any)
| Step | Rollback Action | Status |
|------|-----------------|--------|
| 2 | ... | SUCCESS |
| 1 | ... | SUCCESS |

### Verification Results
- [ ] Health check: PASS/FAIL
- [ ] Smoke test: PASS/FAIL
- [ ] SLO check: PASS/FAIL/PENDING

### Next Steps
- [Recommended follow-up actions]
```
