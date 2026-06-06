# Compensation Transactions Reference

Purpose: Per-forward-step compensation design for Saga patterns — idempotency contracts, LIFO ordering, compensation-of-compensation handling, and failure-of-compensation escalation. Deep companion to the `saga` recipe.

## Scope Boundary

- **weave `compensation`**: Per-step compensation table, ordering, idempotency, failure-of-compensation (this document).
- **weave `saga` (elsewhere)**: Top-level Saga orchestration vs choreography choice. `saga` decides structure; `compensation` designs depth.
- **weave `retry` (elsewhere)**: Transient-failure retry. Retry handles "try again"; compensation handles "undo".
- **schema `rollback` (elsewhere)**: DB-level reverse DDL. Schema rollback is orthogonal to Saga compensation.
- **ripple `rollback-plan` (elsewhere)**: Release-level rollback. Saga compensation handles in-flight workflow; release rollback handles deployed-change reversibility.
- **Triage (elsewhere)**: On-call escalation when compensation itself fails.

## Core Principles

1. **Every forward step has a paired compensation**. If a step cannot be compensated (e.g., sending email), use a semantic compensation (e.g., send correction email).
2. **Compensations run in LIFO order** (reverse of forward execution).
3. **Compensations must be idempotent** — each compensation may run multiple times due to crash-recovery.
4. **Compensation keys are distinct from forward keys** — e.g., `forward:ord-123:step-3` vs `compensate:ord-123:step-3`.
5. **Failure-of-compensation is not retry-forever** — escalate to human runbook after N attempts.

## Compensation Table Template

```markdown
| Step | Forward Operation | Forward Key | Compensation Operation | Compensation Key | Idempotent? | Notes |
|------|-------------------|-------------|------------------------|------------------|-------------|-------|
| 1 | ReserveInventory(orderId, itemId, qty) | forward:{orderId}:1 | ReleaseInventory(orderId, itemId, qty) | compensate:{orderId}:1 | yes | No-op if already released |
| 2 | ChargePayment(orderId, amount) | forward:{orderId}:2 | RefundPayment(orderId, chargeId) | compensate:{orderId}:2 | yes | Uses Stripe refund API |
| 3 | AllocateShipping(orderId, address) | forward:{orderId}:3 | CancelShipping(orderId, allocationId) | compensate:{orderId}:3 | yes | Cancel before carrier pickup |
| 4 | SendOrderConfirmationEmail(orderId) | forward:{orderId}:4 | SendCancellationEmail(orderId) | compensate:{orderId}:4 | semantic | Cannot un-send; send correction |
```

## Execution Order

```
Forward:        Step 1 → Step 2 → Step 3 → Step 4
                                          │
                                          │ failure at Step 5
                                          ▼
Compensate:     Step 4c ← Step 3c ← Step 2c ← Step 1c   (LIFO)
```

Rationale: undoing in reverse order preserves invariants. E.g., refund must happen before inventory release if inventory was already charged into the sale.

## Idempotency Contract per Compensation

```typescript
type CompensationRecord = {
  sagaId: string;
  stepIndex: number;
  compensationKey: string;         // distinct from forward key
  status: 'pending' | 'executing' | 'success' | 'failed' | 'escalated';
  attempts: number;
  lastError: string | null;
  startedAt: Date;
  completedAt: Date | null;
};
```

Per compensation:
1. Check compensationKey — if status is `success`, skip (already compensated).
2. Set status `executing` before calling external service.
3. Call compensation with deduped key server-side.
4. On success, record `completedAt`.
5. On failure, increment attempts; if attempts < max → retry; else → `escalated` + alert.

## Compensation-of-Compensation

Occasionally, the compensation itself has side effects that need their own inverse. Example: compensation `RefundPayment` might trigger a bank-level hold that needs `ReleaseBankHold` if the compensation is later invalidated.

Guidance:
- Keep compensations atomic when possible (single external call).
- If compensation-of-compensation is unavoidable, model as a sub-Saga.
- Document explicitly in the compensation table.

## Failure-of-Compensation Escalation

When a compensation fails after max retries, the system enters an **inconsistent state** that requires human intervention.

```
compensating → compensation_retry_exhausted → human_runbook_triggered
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │ operator: 1) │
                                       │ verify state │
                                       │ 2) manual    │
                                       │ correction   │
                                       │ 3) mark done │
                                       └──────────────┘
```

Operator runbook must include:
- Diagnostic query: current state of entity.
- Manual compensation steps (with vendor console / SQL).
- Verification query.
- Mark-done command that transitions the Saga to `compensated_manual`.

Escalation alerts → Triage; runbook handoff → Mend (for eventual automation).

## Semantic Compensation

Some operations cannot be undone:

| Forward | Semantic Compensation |
|---------|----------------------|
| SendEmail | SendCorrectionEmail with apology copy |
| PublishToSNS | Emit correction event, consumers tolerate |
| PhysicalShipping (already handed to carrier) | ArrangeReturn + refund |
| PrintCheck (already mailed) | RequestStopPayment + new check |

For semantic compensations:
- Accept the side effect exists (email was read).
- Focus on customer experience of the correction (hand off to Prose for copy).
- Log the semantic compensation for audit.

## Saga Log

Every Saga must persist execution to survive crashes:

```sql
CREATE TABLE saga_log (
  saga_id TEXT PRIMARY KEY,
  definition_id TEXT NOT NULL,
  current_step INT NOT NULL,
  status TEXT NOT NULL,    -- running | compensating | completed | compensated | escalated
  steps JSONB NOT NULL,    -- [{step_index, status, key, started_at, completed_at, error}]
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX ON saga_log(status) WHERE status IN ('running', 'compensating', 'escalated');
```

On crash/restart:
1. Resume Sagas where status = 'running' or 'compensating'.
2. For each, check last recorded step status.
3. If 'executing' → depends on idempotency: resume or check-and-skip.
4. If 'success' → move to next step.
5. If 'failed' → transition to 'compensating' and begin LIFO compensation.

## Output Template

```markdown
## Compensation Design: [Saga Name]

### Context
- **Saga type**: [orchestration / choreography — see weave `saga`]
- **Participants**: [list of services]
- **Business invariants**: [what must hold after success AND after full compensation]

### Step Table
| Step | Forward | Compensation | Idempotent? | Semantic? | Max Attempts |
|------|---------|--------------|-------------|-----------|--------------|
| ... | ... | ... | ... | ... | ... |

### Ordering
- Forward: [1, 2, 3, ...]
- Compensation: [..., 3c, 2c, 1c]   (LIFO)
- Exceptions: [any non-LIFO cases with rationale]

### Idempotency Keys
- **Forward key template**: `forward:{sagaId}:{stepIndex}`
- **Compensation key template**: `compensate:{sagaId}:{stepIndex}`
- **Server-side dedup TTL**: [hours]

### Saga Log Persistence
- **Storage**: [DB / event store]
- **Recovery protocol**: [on restart: resume running + compensating]

### Failure-of-Compensation Escalation
- **Max retries per compensation**: [N]
- **Escalation path**: Triage → manual runbook
- **Runbook location**: [link / ref]
- **Mark-done command**: [how operator closes the Saga manually]

### Semantic Compensations
| Step | Cannot-Undo Reason | Semantic Replacement | Customer Copy Owner |
|------|-------------------|---------------------|---------------------|
| ... | ... | ... | Prose |

### Handoffs
- weave `saga` (top-level orchestration)
- weave `retry` (per-step retry inside a step)
- Triage (escalation runbook)
- Mend (runbook automation candidate)
- Prose (correction email copy)
- Builder (implementation)
- siege concurrency (race/deadlock review of Saga log)
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| No compensation defined for email step | Use semantic compensation + note limitations |
| Same idempotency key for forward and compensation | Use distinct prefixes |
| Compensation not idempotent | Redesign to be safe under repeated execution |
| Retry compensation forever | Cap attempts, escalate to human |
| No Saga log persistence | Crash loses state; always persist |
| Ignoring LIFO order | State inconsistencies leak |
| Compensation fires before forward completes | Only compensate steps with confirmed success |
| No failure-of-compensation escalation path | State drifts silently |

## Deliverable Contract

When `compensation` completes, emit:

- **Compensation table** (forward / compensation / idempotent / semantic / max attempts).
- **Execution ordering** (LIFO default, document exceptions).
- **Idempotency key templates** (forward and compensation distinct).
- **Saga log schema** and **recovery protocol**.
- **Failure-of-compensation escalation path** (retries, runbook, mark-done).
- **Semantic compensation section** for un-undoable operations.
- **Handoffs**: saga, retry, Triage, Mend, Prose, Builder, siege.

## References

- Garcia-Molina, Salem (1987) — "Sagas" (original paper)
- Chris Richardson — "Microservices Patterns" (Saga + compensation)
- Azure Architecture Center — Compensating Transaction pattern
- AWS Step Functions — compensating Lambda patterns
- Temporal.io — long-running workflow compensation
- Stripe — Idempotency key design
