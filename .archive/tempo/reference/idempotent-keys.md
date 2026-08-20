# Idempotency-Key Design for At-Least-Once Systems

Purpose: Design an idempotency-key contract that turns "at-least-once" delivery into "effectively-once" outcomes. The key is the single source of truth for "have we seen this request before?" — every retry-safe endpoint, job, and webhook consumer needs one. Read this when a workflow can run more than once (retry, replay, client double-click, network duplicate) and the outcome must not duplicate (charge, email, order, stock move). This is the definitive Tempo pattern pair for deadline and retry specs.

## Scope Boundary

- **Tempo `idempotent`**: key generation rules, dedup window semantics, storage model, exactly-once vs effectively-once semantics, compensating-action vs retry choice, distributed idempotency patterns.
- **Stream (elsewhere)**: exactly-once-within-pipeline via Kafka transactions, Flink checkpoints, two-phase commit sinks. Tempo defines what a logical duplicate is; Stream implements pipeline-level guarantees.
- **Gateway (elsewhere)**: header-level `Idempotency-Key` enforcement, response caching for replayed keys, key TTL at the edge. Gateway wires the header; Tempo defines the key and window.
- **Beacon (elsewhere)**: duplicate-hit rate dashboards, dedup-store size alerts, idempotency-key collision alarms.

If the question is "what is the key and how long does it live?" → `idempotent`. If it is "how do I configure Kafka transactions?" → Stream. If it is "how do I validate the `Idempotency-Key` header on POST /charges?" → Gateway. If it is "alert me when duplicate rate spikes" → Beacon.

## Exactly-Once vs Effectively-Once

| Semantic | Definition | Cost | Platforms |
|----------|-----------|------|-----------|
| At-most-once | Best effort; may lose | Lowest | Fire-and-forget metrics |
| At-least-once | Retries until ack; may duplicate | Low | Most queues default |
| Effectively-once | At-least-once + idempotency key dedup | Medium | Stripe, Square, most payment APIs |
| Exactly-once (within system) | Distributed transaction or dedicated protocol | High | Temporal workflows, Kafka EOS within a cluster |

"Exactly-once" across trust boundaries (client → server → external API) is impossible without cooperation from both sides. Effectively-once is the practical target: the client sends a key, the server dedupes on it.

## Key Generation

### Client-side vs server-side

| Source | When correct | Risk |
|--------|-------------|------|
| Client-generated UUIDv4 | Stripe / Square pattern; client owns retry intent | Client must NOT regenerate on retry |
| Server-generated from content | Webhook handlers; content is the key (`sha256(payload)`) | Two distinct requests with same content collide |
| Hybrid (client_id + content) | When content alone is ambiguous (two identical charges in 1s = two real charges) | Requires stable client identity |

Default for user-facing APIs: **client-generated UUIDv4**, passed in an `Idempotency-Key` header. Document this in the API spec.

### Deterministic keys for workflows

```ts
// Good: deterministic, scoped, collision-resistant
const key = `charge:v1:${userId}:${invoiceId}:${amount}`;

// Bad: includes a timestamp → not stable across retries
const key = `charge:${userId}:${Date.now()}`;

// Bad: unscoped → collides with other operation types
const key = `${userId}:${invoiceId}`;
```

Include a version prefix (`v1`) so schema changes can coexist with in-flight keys.

## Dedup Window: Storage TTL vs Request TTL

Two different TTLs must be distinguished:

| TTL | Meaning | Typical value |
|-----|---------|---------------|
| Request TTL | How long the client considers a key "the same request" — i.e. how long it will retry | `max_retry_duration + clock_skew` |
| Storage TTL | How long the server remembers the key + cached response | `request TTL × 2` minimum |

Storage TTL MUST exceed request TTL. Otherwise the client retries with a key the server has forgotten — and the request executes twice.

Stripe uses 24h request idempotency. A safe server default: 48h storage with a dedup entry per key.

## Storage Patterns

### Redis SETNX / SET NX EX

```
SET idem:charge:v1:u42:inv99 "<response-hash>" NX EX 172800
```

`NX` = only set if not exists; `EX 172800` = 48h TTL. Atomic check-and-set. First write wins; all subsequent retries read the cached response.

### DB unique constraint

```sql
CREATE TABLE idempotency (
  key TEXT PRIMARY KEY,
  operation TEXT NOT NULL,
  request_hash BYTEA NOT NULL,
  response JSONB,
  status TEXT NOT NULL,  -- 'in_flight' | 'completed' | 'failed'
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX ON idempotency(expires_at);
```

The `(key, operation)` pair defines uniqueness. Background job sweeps `expires_at < NOW()`.

### In-flight guard

A key seen a second time WHILE the first is still processing is the hardest case. Options:

- Block second caller on the same key and return the first result when done (strong consistency, risk of deadlock)
- Return `409 Conflict` + `Retry-After` to force client to wait (simpler, client-friendly)
- Return `202 Accepted` with a status-poll URL (async-native APIs)

Stripe returns `409 Conflict` on concurrent same-key in-flight requests. Good default.

## Compensating Action vs Retry

Not every failed operation is retry-safe. Decision table:

| Failure type | Action |
|--------------|--------|
| Network error before server saw request | Retry with same key |
| Server saw + processed + crashed before response | Retry with same key (dedup returns cached result) |
| Server processed but wrote partial state | Requires compensating action, NOT retry |
| External side-effect committed, response lost | Retry with same key (dedup returns cached result) OR query external system to confirm |

When the operation straddles systems (charge card → write DB row → send email), the idempotency key guards the whole envelope, but each step MUST be individually idempotent (Saga pattern). Hand state-machine design to Weave for this case.

## Distributed Idempotency

When multiple services touch the same operation, agree on ONE key scope and propagate it:

```
Client ──(Idempotency-Key: K)──▶ API ──(key=K)──▶ Charge Service ──(key=K)──▶ Ledger
                                                       │
                                                       └─(key=K)──▶ Notification
```

Rules:
- The key is opaque to every downstream hop; they only dedupe on it.
- Include the key in async messages (SQS/Kafka message attribute) so consumers dedupe independently.
- Do NOT re-derive the key downstream; passing it through preserves the client's retry contract.

## Anti-Patterns

- Using a timestamp as part of the key — defeats dedup on retry.
- Missing version prefix — schema change silently collides with in-flight keys.
- Storage TTL ≤ request TTL — late retries execute twice.
- Key without operation scope (`user_id` alone) — two different operations on the same user collide.
- Caching only the success response; re-executing on failed-response replay — non-determinism.
- Deduping AFTER side-effect execution — defeats the purpose; dedupe must happen BEFORE the side-effect.
- Trusting `POST` retries without requiring an `Idempotency-Key` header — client double-clicks charge twice.
- Swallowing `409 Conflict` as success — duplicate submission silently lost.
- Re-using keys across environments (dev/stage/prod) — test runs contaminate prod dedup store.
- Storing unbounded dedup rows without sweep — table grows forever.

## Handoff

**To Builder:** deliver the key formula (with version prefix and scope), the dedup window (request TTL + storage TTL), the storage mechanism (Redis SETNX / DB unique / DynamoDB conditional put), the in-flight behavior (block / 409 / 202), and the cached-response contract.

**To Gateway:** deliver the HTTP contract — header name (`Idempotency-Key`), required on which methods (usually `POST`, `PATCH`), response behavior on replay (same 2xx body), response on in-flight duplicate (`409 Conflict` + `Retry-After`).

**To Weave:** deliver the Saga-step idempotency requirement when the operation spans multiple services — each step needs its own idempotent contract composable under the envelope key.

**To Beacon:** deliver duplicate-hit-rate SLO, dedup-store size alert, in-flight-collision counter, and key-TTL-expiry observability.

**To Voyager:** deliver scenarios — same key + same payload (return cached), same key + different payload (reject 422), concurrent same-key (one wins, one gets 409), key older than TTL (new execution), cross-region replay.
