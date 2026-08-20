# Retry, Backoff, Dead-Letter Queue, Idempotency, Rate Limiting

Complete reference for the unhappy-path half of scheduling. Read when designing retry policies, DLQs, idempotency keys, or rate limits.

> **2026 framing: do you need to write retries by hand?** When the platform offers durable retries (Temporal Schedules, Cadence, Inngest, Azure Durable Functions, AWS Step Functions, Hatchet, Trigger.dev), prefer **declarative retry policy** + **idempotent activity / step function** over hand-rolling backoff loops in application code. Hand-rolled retries silently lose progress on worker restart; durable schedulers persist the retry state and resume from the last successful checkpoint. Keep this file's formulas as the *contract* you hand to the platform configuration, not as code you write yourself for long-running work.

---

## Backoff Formulas

### Fixed interval — almost never correct

```
delay = base
```

Causes thundering herd: N clients retry at the same instant. Use only for single-client, low-traffic cases.

### Exponential backoff — standard baseline

```
delay = base × 2^attempt
```

With `base = 100ms`: 100ms, 200ms, 400ms, 800ms, 1.6s, 3.2s, ... Growth unbounded; always cap.

```
delay = min(cap, base × 2^attempt)
```

Still deterministic — multiple clients that failed at the same tick will retry in lockstep. Not recommended alone.

### Full jitter — recommended default

```
delay = random_uniform(0, min(cap, base × 2^attempt))
```

Spreads retries across the entire window; best load-smoothing among common formulas. Source: AWS Architecture Blog "Exponential Backoff And Jitter" (2015).

### Equal jitter — half-deterministic, half-random

```
temp = min(cap, base × 2^attempt)
delay = temp/2 + random_uniform(0, temp/2)
```

Guarantees a minimum wait; mild load-spreading. Useful when you need a lower bound on retry latency.

### Decorrelated jitter — AWS Builders' Library recommendation

```
delay = min(cap, random_uniform(base, prev_delay × 3))
```

`prev_delay` is the previous computed delay (starts at `base`). Best behavior under retry storms; the random expansion prevents retries from bunching up.

### Choosing between them

| Scenario | Recommendation |
|---------|----------------|
| Single client, idempotent API | Exponential + full jitter |
| Many concurrent clients | Decorrelated jitter |
| Tight latency budget | Equal jitter (bounded minimum) |
| Anything external beyond your control | Full or decorrelated jitter + hard cap |

---

## Retry Budget

Never retry forever. Cap by **both** dimensions:

- **Max attempts**: 3-7 for external calls; 1-3 for user-initiated flows; 10-25 for background jobs.
- **Max total duration**: `max_total_duration = sum of delays + expected RTT × attempts`. Budget 30s-2m for sync user flows; 10m-1h for background; beyond that, send to DLQ.

Prefer expressing the budget in **duration** over attempts — it is independent of backoff formula changes.

### Retryable vs non-retryable errors

| Class | Status codes / examples | Retry? |
|-------|-------------------------|--------|
| Network | `ECONNRESET`, `ETIMEDOUT`, `ENOTFOUND` | Yes |
| 5xx server | 500, 502, 503, 504 | Yes (with jitter) |
| 429 Too Many Requests | Respect `Retry-After` header | Yes (honor header) |
| 408 Request Timeout | | Yes |
| 4xx client error (other) | 400, 401, 403, 404, 409, 422 | **No** — retry will fail identically |
| DB constraint violation | unique key, FK violation | No — logic bug |
| Validation | | No |
| Auth token expired | | Refresh token, then retry once |

Distinguish **transient** (retryable) from **permanent** (non-retryable) in code via typed errors or explicit classification, not string matching.

---

## Circuit Breaker

Protects downstream by failing fast when a service is unhealthy.

### States

```
    ┌────────┐   threshold hit   ┌────────┐
    │ CLOSED │──────────────────▶│  OPEN  │
    └────────┘                    └────────┘
         ▲                             │
         │ N successes                 │ timeout
         │                             ▼
         │ failure                ┌──────────┐
         └────────────────────────│ HALF-OPEN│
                                  └──────────┘
```

- **Closed**: normal; count failures.
- **Open**: reject calls immediately (fail fast); do not call downstream.
- **Half-open**: after `open_duration`, allow 1-3 probe requests. Success → Closed; failure → Open again.

### Trip thresholds

- **Consecutive-failure count**: simple; e.g., 5 consecutive failures → open. Risky for low-traffic services (false positives).
- **Failure-rate over rolling window**: e.g., >50% failure rate over 20 requests in the last minute → open. Better for mixed-traffic services. Requires a sliding window counter.

### Timeouts

- `open_duration`: time before half-open probe. Typical: 10-60s. Too short → probe while still unhealthy; too long → extended downtime.
- `half_open_max_calls`: probe concurrency. 1-3.

### Libraries

- Java: Resilience4j, Hystrix (deprecated).
- Node: opossum, cockatiel.
- Go: sony/gobreaker, failsafe-go.
- Python: pybreaker, tenacity (has breaker via `circuit_breaker`).
- .NET: Polly.

### Anti-pattern

- Circuit breakers **per instance** in a horizontally-scaled service have different views of "healthy" — a centralized breaker state (Redis, service mesh) provides consistency but adds a dependency. Trade-off: accept per-instance drift for simplicity in most cases.

---

## Dead-Letter Queue (DLQ)

### Purpose

Messages that exhausted the retry budget land in the DLQ so they can be:
1. Inspected by a human.
2. Root-cause analyzed (often a bug or a schema drift).
3. Replayed selectively after fix.

### Design

- **Naming**: `<original_queue>_dlq` or `<original>.dead-letter`.
- **Max-retries policy**: typically 3-5 redeliveries before DLQ (per SQS), or 25 retries with Sidekiq's exponential curve.
- **Retention**: retain DLQ messages long enough for human triage — 14 days (SQS max) is a common default; longer via cold-storage archive.
- **Monitoring**: DLQ depth > 0 is a page-worthy signal; depth increasing is a P1.
- **Replay**: documented procedure to move messages back to the main queue AFTER fixing the root cause. Never replay without a diagnosis — you will re-DLQ immediately.
- **Poison-message detection**: same message-ID DLQed repeatedly across replays → wrap in a "quarantine" queue with manual review flag.

### Platform specifics

| Platform | DLQ mechanism |
|----------|---------------|
| **AWS SQS** | Redrive policy: `maxReceiveCount` + `deadLetterTargetArn` |
| **AWS Lambda (async)** | `DeadLetterConfig` → SQS or SNS; or Destinations for both success/failure |
| **AWS SNS** | Subscription-level DLQ via SQS |
| **Azure Service Bus** | Built-in `$DeadLetterQueue` sub-queue |
| **GCP Pub/Sub** | `deadLetterPolicy` with target topic + max delivery attempts |
| **Kafka** | No native DLQ; convention = `<topic>.DLT` (Spring Kafka) or separate topic |
| **RabbitMQ** | `x-dead-letter-exchange` on queue; optional `x-dead-letter-routing-key` |
| **Sidekiq** | "Morgue" (dead set) after retry exhaustion; web UI for review |
| **BullMQ** | `failed` list; app-level move to DLQ queue |
| **Celery** | No built-in DLQ; common pattern = `task_routes` to error queue |
| **Temporal** | Failed workflows stay discoverable via query; no explicit DLQ needed |

### Replay mechanism

```python
# Pseudo-code: drain DLQ after fix
for message in dlq.receive_batch(max=10):
    if is_safely_replayable(message):  # validation, version check
        main_queue.send(message.body)
        dlq.delete(message.receipt_handle)
    else:
        quarantine.send(message.body)
        dlq.delete(message.receipt_handle)
```

Always dry-run the drain first; log every replayed message with a replay tag.

---

## Idempotency Keys

### Why

At-least-once delivery (the default for most queues and HTTP retries) means a message or request may be processed **more than once**. Idempotency keys let the handler recognize a duplicate and return the cached result without re-executing side effects.

### Design rules

1. **Deterministic**: Same logical operation → same key. Not a random UUID per attempt — that defeats the purpose.
2. **Stable across retries**: Generated once at the producer, carried through all retries.
3. **Bounded lifetime**: Stored with a TTL; after TTL expires, the operation is a new request.
4. **Cover the operation, not the payload**: Key should represent "process invoice X for user Y", not the entire JSON payload.

### Key formulas

| Pattern | Example | When |
|---------|---------|------|
| Natural key | `user:123:invoice:456` | Domain entities have unique IDs |
| Hash of logical input | `SHA256("payment:" + user_id + ":" + invoice_id + ":" + amount)` | Multiple natural fields combine |
| Producer-generated UUID | `{uuid-v4}` persisted by producer | Client-originated (e.g., Stripe `Idempotency-Key` header) |
| Request-ID + operation | `req-abc123:charge` | Per-request idempotency in HTTP APIs |

### Storage patterns

```redis
# Redis — atomic check-and-set
SET idempotency:abc123 "processed" EX 86400 NX
# Returns nil if key exists = duplicate; returns OK on first write
```

```sql
-- PostgreSQL — unique constraint on operation table
CREATE TABLE idempotent_ops (
  key TEXT PRIMARY KEY,
  result JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO idempotent_ops (key, result)
VALUES ('abc123', '{...}')
ON CONFLICT (key) DO NOTHING
RETURNING result;
-- Empty return = duplicate; SELECT existing to return cached result
```

### Dedup window

Explicitly document: "Same key within the last 24h is deduplicated; after 24h, reprocessed."

Formula:
```
dedup_window >= max_retry_total_duration + clock_skew_margin + safety_buffer
```

Example: max retry duration 1h, clock skew 5m, buffer 23h → window = 24h.

### Stripe-style idempotency contract

```http
POST /v1/charges
Idempotency-Key: {client-generated-unique-key}
```

Server stores `(key, request_hash, response)` for 24h. Requests with:
- Same key + same body → returns cached response.
- Same key + **different** body → returns an error (indicates client bug).
- New key → processes fresh.

Adopt this contract for any public API that mutates state.

---

## At-least-once vs Exactly-once

### At-least-once (most common, cheap)

- Message **may be delivered more than once**.
- Handler MUST be idempotent.
- Supported by: SQS, Kafka (default), RabbitMQ, Pub/Sub, nearly everything.

### Exactly-once (rare, expensive)

- True exactly-once is **theoretically impossible** across distributed systems (two-generals problem).
- Achievable **within a system boundary** via transactional semantics:
  - **Kafka transactions** (since 0.11): exactly-once within a Kafka cluster.
  - **Temporal workflows**: exactly-once workflow execution (activities still at-least-once with dedup via workflow ID).
  - **Database-level**: single DB transaction with outbox pattern.
- Does NOT cross system boundaries — "exactly-once end-to-end" is always at-least-once + idempotency.

### At-most-once (rare)

- Message may be **lost but never duplicated**.
- Only acceptable for non-critical metrics or fire-and-forget logging.
- Usually configured by disabling retry entirely.

---

## Platform Retry Implementations

### AWS SQS + Lambda

```yaml
# SQS queue with redrive
QueueName: my-queue
RedrivePolicy:
  maxReceiveCount: 5
  deadLetterTargetArn: arn:aws:sqs:...:my-queue-dlq
VisibilityTimeout: 60   # longer than max task duration
```

- Lambda async: 2 retries default (0/1/2 configurable), then DLQ.
- Lambda sync: no auto-retry; client retries.

### BullMQ (Node.js)

```javascript
await queue.add('process-order', data, {
  attempts: 5,
  backoff: {
    type: 'exponential',
    delay: 1000,   // 1s, 2s, 4s, 8s, 16s
  },
  removeOnComplete: 100,   // retain last 100 successes
  removeOnFail: 1000,      // retain last 1000 failures
});
```

### Sidekiq (Ruby)

```ruby
class MyWorker
  include Sidekiq::Worker
  sidekiq_options retry: 25, dead: true   # 25 retries, then morgue

  sidekiq_retry_in do |count, exception|
    10 * (count ** 4) + rand(30) * (count + 1)   # default curve
  end

  def perform(id)
    # idempotent work
  end
end
```

### Celery (Python)

```python
@app.task(
    bind=True,
    autoretry_for=(requests.RequestException,),
    retry_backoff=True,
    retry_backoff_max=600,
    retry_jitter=True,
    max_retries=5,
    acks_late=True,        # ack only after successful completion
)
def fetch_data(self, url):
    return requests.get(url).json()
```

`acks_late=True` is crucial for safety — without it, crash mid-task = message lost.

### Temporal

```go
retryPolicy := &temporal.RetryPolicy{
    InitialInterval:    time.Second,
    BackoffCoefficient: 2.0,
    MaximumInterval:    time.Minute,
    MaximumAttempts:    5,
    NonRetryableErrorTypes: []string{"InvalidArgumentError"},
}

activityOptions := workflow.ActivityOptions{
    StartToCloseTimeout: 30 * time.Second,
    RetryPolicy:         retryPolicy,
}
```

Workflow ID = natural idempotency key; duplicate workflow starts are rejected.

---

## Rate Limiting

### Token bucket

- Bucket holds up to `B` tokens; refills at rate `R` tokens/sec.
- Each request consumes 1 token; empty bucket → reject or queue.
- Allows bursts up to `B`; sustained rate `R`.

```
if tokens >= 1:
    tokens -= 1
    allow()
else:
    reject()   # or queue with deadline
```

Libraries: `golang.org/x/time/rate`, `async-ratelimiter` (Node), `ratelimit` (Python aiolimiter).

### Leaky bucket

- Requests enter a FIFO queue of size `Q`; drained at constant rate `R`.
- Smooths output to exactly `R`; rejects when queue full.
- No bursting — predictable downstream load.

### Sliding window

- Count requests in the last `W` seconds.
- More accurate than fixed-window (which has double-count at boundaries).
- Storage: Redis sorted set with timestamps + `ZREMRANGEBYSCORE`.

### GCRA (Generic Cell Rate Algorithm)

- Equivalent to leaky bucket but O(1) state (single timestamp, no queue).
- Used by Redis Cell module, Stripe's internal rate limiter.
- Formula: for each request, compute "theoretical arrival time"; allow if `now >= TAT - burst_tolerance`.

### Choosing

| Scenario | Algorithm |
|---------|-----------|
| API with bursts allowed | Token bucket |
| Strict output smoothing | Leaky bucket |
| Accurate time-windowed counting | Sliding window |
| Distributed, storage-efficient | GCRA |

### Rate-limit anti-patterns

- Per-instance rate limits that don't coordinate → actual rate = N × configured.
- Ignoring `Retry-After` on 429 responses → retry storm.
- Rate-limiting by IP only → NAT'd users sharing IP get collectively throttled.
- Fixed-window counters at exact boundaries (e.g., minute boundary) → 2× spike at each boundary.

---

## Retry Anti-patterns

1. **Unbounded retries**: no max attempts, no max duration → messages stuck forever.
2. **Retry storm**: many clients retrying the same failed dependency simultaneously → amplifies the outage. Fix with jitter + circuit breaker.
3. **Thundering herd after recovery**: all clients resume at t=recovery+1; stagger with jitter.
4. **Retry on 4xx**: client errors won't succeed by retrying (except 408, 429); wastes budget.
5. **Retry inside retry**: nested retry policies multiply (outer 3 × inner 3 = 9); flatten to one layer.
6. **Retrying non-idempotent operations without an idempotency key**: creates duplicates (duplicate charges, duplicate emails). Always pair retry with idempotency.
7. **No DLQ**: failed messages silently disappear; no audit trail.
8. **Aggressive retry on partial failures**: a 200 response with an error body is not a transient failure; classify by error, not by protocol status.

---

## Checklist: retry / backoff / idempotency design

- [ ] Max attempts AND max total duration capped.
- [ ] Backoff with jitter (full, equal, or decorrelated).
- [ ] Retryable error classes explicitly enumerated (not a catch-all).
- [ ] Non-retryable errors fail fast (no wasted budget).
- [ ] Idempotency key formula documented; stable across retries.
- [ ] Dedup window explicitly sized; stored with TTL.
- [ ] DLQ destination configured; retention + replay procedure documented.
- [ ] DLQ depth alert wired up (hand to Beacon).
- [ ] Circuit breaker in front of any external dependency (where appropriate).
- [ ] Retry behavior tested under simulated failure (chaos test with Siege, scenarios with Voyager).
- [ ] No 4xx retries (except 408, 429).
- [ ] `Retry-After` header honored.
