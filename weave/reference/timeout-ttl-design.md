# Timeout / TTL / Deadline State Design Reference

Purpose: Design TTL, deadline, expiry, and grace-period state transitions. Propagate deadlines across distributed calls, distinguish soft vs hard timeouts, and define escape routes from stuck states. Pairs with `retry` (retry runs inside a timeout envelope) and `compensation` (timeout triggers compensation when state is unclear).

## Scope Boundary

- **weave `timeout`**: TTL / deadline / expiry state design (this document).
- **weave `retry` (elsewhere)**: Retry inside a timeout. Timeout sets the envelope; retry consumes it.
- **weave `compensation` (elsewhere)**: Compensation triggered when timeout expires with unclear state.
- **tempo (elsewhere)**: Scheduler for expiry detection (cron, periodic sweep).
- **Beacon (elsewhere)**: Stuck-state alerts.
- **Scout (elsewhere)**: Investigation of stuck records post-alert.

## Workflow

```
DERIVE     →  per-state timeout from business SLA
           →  downstream chain timeout < upstream timeout (budget propagation)

PROPAGATE  →  deadline passed via context/header (Deadline-Propagation)
           →  every hop subtracts its own budget

SOFT/HARD  →  soft timeout (warn): customer-visible degradation starts
           →  hard timeout (abort): state transitions to timeout_expired

GRACE      →  grace period: extra window before escalation
           →  e.g., payment pending → 24h soft + 48h hard → expired

ESCAPE     →  stuck-state detection: state age > expected + N × std_dev
           →  auto-transition: stuck → recovery / manual_review

CLEAN UP   →  TTL-based cleanup: expired records archived / purged
           →  scheduled sweep via tempo
```

## Timeout Categories

| Category | Scope | Example |
|----------|-------|---------|
| Request timeout | Single RPC / HTTP call | HTTP client default 30s |
| End-to-end timeout | Full user-visible flow | Checkout must complete in 60s |
| Session / TTL | Cached or pending state | Shopping cart 24h |
| Deadline (absolute) | Time-based expiry | Coupon expires 2025-12-31 23:59 UTC |
| Grace period | Soft window before hard expiry | Subscription grace 7 days after charge fail |
| Stuck-state escape | Anomaly detection | Order "processing" > 10min → flag |

## Soft vs Hard Timeout

```
                     SLA budget
              ┌──────────────────────────┐
              │                          │
   starts     ▼                          ▼
   ────●──────────●─────────────●────────●─────→ time
           (soft timeout)  (hard timeout)
              │             │
              ▼             ▼
    user-visible warn    abort + alert + state=expired
```

| Phase | Action |
|-------|--------|
| Before soft | Normal path |
| Between soft and hard | Emit warning metric, show spinner / degrade UX, possibly retry |
| At hard | Transition to terminal failure state, emit alert, clean up resources |

## Deadline Propagation Pattern

```
Upstream client: deadline = now + 10s
  → HTTP header: Grpc-Timeout / X-Deadline / context.WithDeadline

Middle service receives: deadline_remaining = received_deadline - processing_so_far
  → Must finish OR propagate reduced deadline to downstream:
     downstream_deadline = remaining - safety_margin (e.g., 100ms for serialization)

Downstream service: same contract
  → Reject immediately if deadline already expired (do not start work)
```

Anti-pattern: each service starts its own 10s timeout. End-to-end chain can exceed caller's expectation. Always propagate and subtract.

## Stuck-State Detection

Every long-running state needs a "how long is too long" threshold:

```
stuck_threshold = expected_mean + 3 × stddev
                  OR
                = p99 + 50% safety margin
                  OR
                = business-SLA × 2
```

Per state, record:
- `entered_at`: timestamp when state was entered.
- `expected_exit_by`: computed at entry.
- `stuck_after`: timestamp after which "stuck" alert fires.

Scheduled sweep (via tempo):
```
SELECT * FROM entity
WHERE current_state IN ('processing', 'awaiting_external', 'pending')
  AND entered_at < NOW() - INTERVAL 'stuck_threshold'
```

Transition stuck records to `needs_review` or `auto_recovery`.

## TTL / Cleanup Patterns

| Pattern | Use Case | Mechanism |
|---------|----------|-----------|
| DB column expiry | Coupons, tokens | `WHERE expires_at > NOW()` + nightly purge |
| Cache TTL | Session, cart | Redis `EXPIRE` |
| Event-driven | Magic links | On create, schedule expiry event |
| Cron sweep | Batch cleanup | tempo-scheduled job |
| Partitioning | Log retention | Drop partition > N days |

**Always archive before delete** if the data has any auditing / legal-hold requirement (consult Cloak / Comply).

## Grace Period Design

For subscription / billing / critical flows:

```
Normal → at_risk (first failure) → grace (soft warnings) → suspended (hard cutoff) → cancelled (terminal)
```

| State | Duration | Customer Visible? | Actions |
|-------|----------|-------------------|---------|
| at_risk | minutes-hours | No | Retry payment, internal alert |
| grace | 1-7 days | Email / banner | Warnings, allow access |
| suspended | 7-30 days | Limited access | Cannot use premium features |
| cancelled | terminal | Yes | Archive, notify |

Hand off to Prose for grace-period copy, Retain for win-back strategy.

## Deadline vs Duration

- **Deadline** = absolute point in time (e.g., `2025-12-31T23:59:59Z`).
- **Duration** = relative span (e.g., `24 hours`).

For distributed systems, **always propagate as absolute deadline** (wall-clock time). Each hop converts its local duration to deadline: `deadline = now() + budget`. Prevents clock drift and double-counting.

Caveat: clock skew between services must be bounded (NTP sync). Otherwise, add safety margin per hop.

## Output Template

```markdown
## Timeout / TTL Design: [Name]

### Context
- **End-to-end SLA**: [duration]
- **Business criticality**: [grace period needs / hard cutoff]
- **Downstream chain depth**: [N hops]

### Timeout Budget Allocation
| Hop | Timeout | Rationale |
|-----|---------|-----------|
| user-facing HTTP | 10s | browser expectation |
| BFF → API | 8s | 2s reserved for BFF processing |
| API → DB | 3s | query p99 < 500ms + safety |
| API → external | 4s | vendor SLA + jitter |

### State Timeouts
| State | Expected duration | Stuck threshold | Escape transition |
|-------|-------------------|-----------------|-------------------|
| payment_pending | ≤ 2s | > 30s | → payment_timeout |
| awaiting_webhook | ≤ 60s | > 5min | → webhook_missing |
| processing | ≤ 5s | > 60s | → needs_review |

### Soft/Hard Timeout Pairs
| Flow | Soft | Hard | Soft Action | Hard Action |
|------|------|------|-------------|-------------|
| checkout | 45s | 60s | show spinner | abort, refund pending |
| video upload | 2 min | 5 min | show progress | cancel, partial cleanup |

### Grace Period (if applicable)
| State | Duration | Customer copy | Internal action |
|-------|----------|---------------|-----------------|
| at_risk | 4h retry window | none | internal alert |
| grace | 7 days | email banner | feature limited |
| suspended | 30 days | login block | data archived |

### Deadline Propagation
- **Header / context key**: [Grpc-Timeout / X-Deadline-At]
- **Safety margin per hop**: [100ms recommended]
- **Pre-deadline rejection**: each hop checks remaining deadline, rejects if < minimum-work-time

### Stuck-State Sweep
- **Schedule**: [cron — e.g., every 5 min]
- **Query**: [SQL template]
- **Alert threshold (Beacon)**: stuck count > N
- **Escape transition**: [which state on stuck]

### TTL / Cleanup
- **Mechanism**: [cron / event-driven / TTL index]
- **Archive policy**: [before delete: yes/no, where]
- **Compliance check**: [PII retention rules — defer to Cloak/Comply]

### Handoffs
- tempo (sweep schedule, expiry events)
- Beacon (stuck-state alerts)
- Scout (investigation of stuck records)
- Cloak / Comply (retention rules)
- Prose (grace-period copy)
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Each service has its own timeout | Propagate absolute deadline |
| Stuck states never escape | Add sweep + escape transition |
| Soft and hard timeouts collapsed | Separate — soft warns, hard aborts |
| No grace period for billing | Customers churn on first transient failure |
| Using duration (not deadline) across services | Clock drift + double-counting |
| Archive via immediate DELETE | Add archive step first when retention rules apply |
| Downstream retry inside upstream timeout ignores deadline | Retry must respect remaining_deadline |

## Deliverable Contract

When `timeout` completes, emit:

- **Timeout budget allocation** across the call chain (absolute deadlines).
- **Per-state timeout table** (expected, stuck threshold, escape).
- **Soft/hard pair table** with actions.
- **Grace period design** (if applicable).
- **Deadline propagation contract** (header/context key, safety margin).
- **Stuck-state sweep plan** (schedule, query, alert, escape).
- **TTL/cleanup policy** (mechanism, archive, retention).
- **Handoffs**: tempo, Beacon, Scout, Cloak/Comply, Prose.

## References

- Google SRE Workbook — "Load Balancing in the Datacenter" (deadline propagation)
- Rust async deadlines / Go context.WithDeadline
- gRPC timeout propagation (grpc-timeout header)
- Dave Farley — Continuous Delivery, stateful workflow patterns
- Stripe — subscription dunning / grace period patterns
