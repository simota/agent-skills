# Retry State Machine Reference

Purpose: Design retry state machines with exponential backoff, jitter, max-attempt cap, DLQ as terminal state, and idempotency contract. Separates retriable vs non-retriable failure modes and emits a contract that tempo (schedule) and Beacon (alerts) can consume.

## Scope Boundary

- **weave `retry`**: Retry state machine design (states, transitions, backoff, jitter, DLQ) — this document.
- **weave `timeout` (elsewhere)**: TTL / deadline design. Retry and timeout are often paired; design timeout first, then retry inside the timeout envelope.
- **weave `compensation` (elsewhere)**: Saga compensation. Retry handles transient failure; compensation handles logical undo.
- **tempo (elsewhere)**: Schedule / cron / backoff curve details. Retry state machine consumes tempo's backoff rules.
- **Beacon (elsewhere)**: SLO / retry-exhaustion alerts.
- **siege concurrency (elsewhere)**: Race/deadlock analysis on retry implementations.

## Workflow

```
CLASSIFY   →  split failures: retriable (transient) vs non-retriable (logical)
           →  5xx/network/timeout → retriable
           →  4xx/validation/auth → non-retriable (usually)

STATES     →  idle → attempting → waiting → attempting ... → success / DLQ
           →  terminal: success | permanent_failure | dlq

BACKOFF    →  base delay × 2^(attempt-1), capped at max_delay
           →  add jitter: full / equal / decorrelated

CAP        →  max_attempts = f(business SLA, error budget, DLQ capacity)
           →  typical: 3 for user-facing, 5-7 for background, 10+ for async

IDEMPOTENCY → every attempt uses the same idempotency key
           →  server must dedupe; retry state machine never generates a new key mid-retry

DLQ        →  terminal state for exhausted retries
           →  DLQ emits alert + preserves original message for human review

ALERT      →  hand off retry-exhaustion signal to Beacon
           →  hand off DLQ depth alert to Beacon
```

## State Diagram

```
              ┌──────────┐
              │   idle   │
              └────┬─────┘
                   │ start
                   ▼
              ┌──────────┐       success       ┌──────────┐
              │attempting├─────────────────────►│ success  │ (terminal)
              └────┬─────┘                     └──────────┘
                   │ failure
       non-retri   │    retriable + attempts<max
       ┌───────────┤
       │           ▼
       │      ┌──────────┐
       │      │ waiting  │
       │      │ (backoff)│
       │      └────┬─────┘
       │           │ timer fires
       │           ▼
       │      ┌──────────┐
       │      │attempting│ (attempt++)
       │      └────┬─────┘
       │           │ attempts == max
       │           ▼
       │      ┌──────────┐
       │      │   dlq    │ (terminal, alert)
       │      └──────────┘
       ▼
  ┌──────────────┐
  │permanent_fail│ (terminal, no retry)
  └──────────────┘
```

## Backoff + Jitter

| Strategy | Formula | Use When |
|---------|---------|----------|
| Fixed | `delay = base` | Simple, never recommended for production retries |
| Linear | `delay = base × attempt` | Rare; prefer exponential |
| Exponential | `delay = min(base × 2^(attempt-1), max_delay)` | Default |
| Exponential + Full Jitter | `delay = random(0, min(base × 2^(attempt-1), max_delay))` | AWS recommended default |
| Exponential + Equal Jitter | `delay = half + random(0, half)` where half = exp/2 | Less variance than full |
| Decorrelated Jitter | `delay = min(cap, random(base, prev_delay × 3))` | Best for thundering-herd prevention |

**Rule**: always add jitter. No jitter → synchronized retries → thundering herd after a downstream recovery.

### Typical Parameters

| Use Case | base | max_delay | max_attempts |
|----------|------|-----------|--------------|
| User-facing HTTP | 100ms | 2s | 3 |
| Background job | 1s | 60s | 5 |
| Async queue processor | 5s | 5min | 7 |
| Batch / nightly | 10s | 30min | 10 |
| Webhook delivery | 30s | 24h | 15 (spread over days) |

## Retriable vs Non-retriable Classification

| Error | Class | Rationale |
|-------|-------|-----------|
| HTTP 429 (rate limit) | Retriable | Transient, honor Retry-After header |
| HTTP 500, 502, 503, 504 | Retriable | Server-side transient |
| HTTP 408 (timeout) | Retriable | Usually transient |
| HTTP 401, 403 | Non-retriable | Credentials / permissions |
| HTTP 400, 422 | Non-retriable | Validation — same input will fail again |
| HTTP 404 | Usually non-retriable | Exception: eventual consistency window |
| Network timeout | Retriable | Transient |
| Connection refused | Retriable | Service restarting |
| DNS failure | Retriable | Transient DNS issue |
| SSL handshake failure | Investigate | May be config issue |
| Deserialize failure | Non-retriable | Schema mismatch |
| Idempotency conflict | Non-retriable | Original request likely succeeded |

## Idempotency Contract

Every retry must use the same idempotency key:

```typescript
type RetryState = {
  idempotencyKey: string;      // generated ONCE at `idle → attempting`
  attempt: number;             // 1..max_attempts
  lastError: string | null;
  nextAttemptAt: Date | null;
  terminal: 'success' | 'permanent_failure' | 'dlq' | null;
};
```

Server-side contract:
- Dedupe by idempotency key within a TTL window (often 24h).
- Return the original response for duplicate key (same status, same body).
- If business rule conflicts (e.g., email already sent), return 409 with the original request-id.

## DLQ Design

The DLQ terminal state must:

1. **Preserve full payload** (not just error).
2. **Record failure cause** (last error + attempt history).
3. **Emit alert** (Beacon signal — DLQ depth > threshold).
4. **Allow manual replay** with idempotency preserved.
5. **Have TTL** (typically 7-30 days before archival / purge).

### DLQ Alert Thresholds (Beacon)

| Signal | Threshold | Severity |
|--------|-----------|----------|
| DLQ depth > 10 messages | Page | HIGH |
| DLQ depth growing > 1/min for 10 min | Page | CRITICAL |
| Single message failing repeatedly across replay | Investigation | MEDIUM |

## Output Template

```markdown
## Retry State Machine: [Name]

### Context
- **Use case**: [HTTP client / queue consumer / webhook / batch]
- **SLA**: [end-to-end deadline]
- **Blast radius on failure**: [customer impact if DLQ]

### Failure Classification
- **Retriable**: [list of error codes / exceptions]
- **Non-retriable**: [list]
- **Ambiguous**: [list + default handling + rationale]

### State Machine
| State | Entry Actions | Exit Transitions |
|-------|--------------|------------------|
| idle | none | start → attempting |
| attempting | increment attempt counter | success → success; non-retriable → permanent_failure; retriable + attempts<max → waiting; retriable + attempts==max → dlq |
| waiting | compute next_delay with jitter | timer → attempting |
| success | emit success event | terminal |
| permanent_failure | emit permanent-failure event | terminal |
| dlq | enqueue to DLQ + alert | terminal |

### Backoff Parameters
- **Strategy**: [Exponential + Full Jitter / ...]
- **base**: [X ms]
- **max_delay**: [X s]
- **max_attempts**: [N]
- **total_time_budget**: [approx. Σ delays, worst case]

### Idempotency
- **Key generation**: [UUID v4 / ULID / hash of payload]
- **Server-side dedup TTL**: [hours]
- **Conflict handling**: [409 response pattern]

### DLQ
- **Storage**: [SQS FIFO / Kafka DLQ topic / DB table]
- **Retention**: [days]
- **Replay mechanism**: [manual / scheduled]

### Alert Integration (Beacon)
- **Retry-exhaustion rate > X%** over 5 min → HIGH
- **DLQ depth > N** → HIGH
- **DLQ growing > M/min** → CRITICAL

### Handoffs
- tempo (backoff curve details)
- Beacon (alerts)
- Builder (implementation)
- Triage (DLQ review runbook)
```

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| No jitter | Always add jitter (full or decorrelated) |
| Retrying 4xx | Classify as non-retriable unless specifically transient |
| New idempotency key per attempt | Generate once, reuse across retries |
| Unbounded retries | Always cap max_attempts |
| Ignoring Retry-After header | Honor server-requested delay |
| DLQ without alert | Alert on DLQ depth + growth rate |
| Synchronous retry on user request | Use async queue for user-facing calls |
| Retry storming on circuit-breaker close | Combine with circuit breaker state |

## Deliverable Contract

When `retry` completes, emit:

- **Failure classification table** (retriable / non-retriable / ambiguous).
- **State machine** (states, transitions, terminal conditions).
- **Backoff + jitter parameters** (strategy, base, max_delay, max_attempts, total budget).
- **Idempotency contract** (key generation, server dedup TTL, conflict handling).
- **DLQ design** (storage, retention, replay).
- **Alert thresholds** for Beacon.
- **Handoffs**: tempo, Beacon, Builder, Triage.

## References

- Amazon Architecture Blog — "Exponential Backoff and Jitter"
- AWS SDK default retry policy documentation
- Google SRE Book — Handling Overload
- Stripe — Idempotency key design
- RFC 6585 — 429 Too Many Requests
- Polly (.NET), resilience4j (Java), tenacity (Python) — reference implementations
