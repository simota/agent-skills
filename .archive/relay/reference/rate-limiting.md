# Rate Limiting & Backpressure Reference

Purpose: Design rate-limiting and backpressure for messaging integrations — token bucket vs leaky bucket, sliding-window counters, client-side vs server-side enforcement, backpressure propagation, `429 Too Many Requests` with `Retry-After`, cost-based quotas, and per-tenant isolation. The goal is to keep a messaging surface stable under load without silently dropping or starving tenants.

## Scope Boundary

- **Relay `rate`**: transport-level rate limits on webhook intake, bot command dispatch, WebSocket message pace, queue consumer pull rate, and outbound platform-API calls (Slack / Discord / LINE). Backpressure propagation across the messaging layer.
- **Gateway (elsewhere)**: REST/GraphQL rate-limit design at the HTTP ingress (edge) and per-operation quotas for public APIs. When the concern is "public API throttling and 429 surface" → Gateway.
- **Stream (elsewhere)**: batch/streaming pipeline throttling via consumer-side batch size and windowing. When the throttling is part of ETL back-off (Flink credit, Kafka pause/resume for warehouse catch-up) → Stream.
- **Tempo (elsewhere)**: retry *policy* and backoff curves for business jobs. Relay returns `Retry-After`; Tempo decides the global retry schedule shape.
- **Beacon (elsewhere)**: SLO alerts on throttle rate, per-tenant quota utilization dashboards, anomaly detection. Relay emits metrics; Beacon sets thresholds.

If the question is "how do I throttle a messaging surface or a platform-API caller" → `rate`. If it is "how do I throttle a public REST/GraphQL API endpoint" → Gateway.

## Algorithm Selection

| Algorithm | Shape | Strengths | Weaknesses | Pick when |
|-----------|-------|-----------|------------|-----------|
| **Token bucket** | Fixed refill rate, burst = bucket size | Allows bursts up to capacity, smooth average | Bursty tail may still overwhelm downstream | Typical API throttle, webhook intake, bot command |
| **Leaky bucket** | Fixed output rate regardless of input | Smoothest output, protects slow downstream | No bursts — strict pacing | Platform-API callers with strict per-second caps (Slack, Discord) |
| **Fixed window counter** | Count per wall-clock window | Cheapest to implement | Edge spike on window boundary (2× theoretical limit) | Rough approximation only |
| **Sliding window log** | Store timestamps, count in rolling window | Exact, no edge spike | Memory scales with request rate | Low-TPS endpoints needing precision |
| **Sliding window counter** | Weighted blend of current + previous fixed windows | Near-exact without per-request log | Slight approximation error (~0.003%) | Default for API-tier throttling |

Default: **token bucket** for inbound intake (absorbs bursts), **leaky bucket** for outbound to rate-limited platforms (respects their ceiling), **sliding window counter** for per-tenant billing-tied quotas.

## Token-Bucket Reference

```
capacity  = 100         # max burst
rate      = 10 tok/s    # steady-state
on request:
  refill tokens = min(capacity, tokens + rate × Δt)
  if tokens >= cost:
    tokens -= cost
    allow
  else:
    deny with Retry-After = ceil((cost - tokens) / rate)
```

Storage options: in-memory (single node), Redis (shared — use atomic Lua or `CL.THROTTLE` from redis-cell), distributed (DynamoDB conditional writes for cross-region). In-memory works until you run two replicas.

## Client-Side vs Server-Side

| Enforcement | Where | When |
|-------------|-------|------|
| **Server-side** | Middleware on inbound; pre-send guard on outbound | Authoritative — always required for protection |
| **Client-side** | SDK-level pacing before the request leaves | Reduces 429 volume, improves p99, respects upstream limit without round trip |

Ship both. Server-side prevents abuse; client-side (including in your outbound adapter to Slack/Discord/LINE) avoids wasteful 429 round trips and keeps the user-visible latency stable. Outbound adapters should honor the platform's returned `X-RateLimit-Remaining` / `Retry-After` headers and self-throttle — do not fire-and-hope.

## Backpressure Propagation

A rate limit with no backpressure becomes a dropped-message generator. Propagate pressure upstream so senders slow down instead of the queue growing unbounded.

| Layer | Backpressure primitive |
|-------|------------------------|
| HTTP inbound | `429 Too Many Requests` + `Retry-After` |
| WebSocket | Pause reads / stop acking → TCP window closes → sender blocks; modern: WebSocketStream API |
| SSE | HTTP/TCP flow control — slow `write()` back-pressures the origin |
| Queue consumer | Reduce prefetch / max-in-flight; Kafka: `pause()` / `resume()` on partition |
| Outbound platform API | Block in outbound adapter when token bucket empty; surface to caller as typed error |

Drop messages only at the outermost boundary and only after emitting a metric. Silent drops in the middle of the pipeline become untraceable incidents.

## 429 Response Contract

Always include these headers on a rate-limit rejection:

```
HTTP/1.1 429 Too Many Requests
Retry-After: 12
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1714046400
```

- `Retry-After` — seconds or HTTP-date. Seconds is simpler and widely supported.
- `X-RateLimit-*` — non-standard but near-universal convention (GitHub, Stripe, Twitter). Expose the remaining budget so well-behaved clients can self-pace.
- Body: JSON with machine-readable `code` (`"rate_limited"`) and the same retry hint — some clients cannot read headers (legacy SDKs).

Never return `200` with an empty body on throttle — it is indistinguishable from success and breaks clients.

## Cost-Based Quotas

Not every request costs the same. Charge weighted tokens:

| Operation | Cost |
|-----------|------|
| `chat.postMessage` (single) | 1 |
| `conversations.history` (page 100) | 10 |
| `files.upload` (10 MB) | 25 |
| LLM completion (500 tok out) | tokens × price |

Apply weights to the token bucket so a few heavy calls do not starve many light ones. Document the weight table publicly so clients can estimate their budget. For billing-tied quotas (LLM pass-through, media processing), use an **immediate-decrement + reconcile** pattern — charge an estimate before the call, settle against the actual cost after.

## Per-Tenant Isolation

In a multi-tenant messaging surface, one noisy tenant must not starve the others.

| Strategy | How |
|----------|-----|
| **Per-tenant bucket** | Keyed by `tenantId` in Redis — independent refill and capacity |
| **Per-tenant + global cap** | Two-level check: tenant bucket passes, then global bucket — global protects downstream |
| **Fair queueing** | Round-robin or weighted-fair dispatch across tenant queues instead of FIFO |
| **Quota tiers** | `free` / `pro` / `enterprise` → different capacity and refill rates |
| **Noisy-neighbor eviction** | Sustained overage → temporary demotion or hard cap with paging to on-call |

Cache the tenant tier lookup — hitting the tier DB on every request is the first thing that collapses under load.

## Anti-Patterns

- Fixed-window counters advertised as "60 req/min" — a burst at the window boundary delivers ~2× the stated rate and breaks downstream SLAs.
- Returning `429` without `Retry-After` — clients thrash with tight retry loops and amplify the problem.
- Global single-tenant bucket in a multi-tenant product — one heavy tenant throttles everyone else's messages.
- In-memory token bucket across multiple replicas — effective limit is `N × configured` where N is replica count; use Redis or a shared store.
- Counting-only (no cost weighting) on a pass-through LLM or media endpoint — a handful of large requests exhaust quota meant for thousands of small ones.
- Throttling inbound without propagating backpressure to the producer — queue grows until OOM instead of senders slowing down.
- Silently dropping messages when the bucket is empty — untraceable lost messages; always emit a throttle event metric and a typed response.
- Ignoring platform-returned `X-RateLimit-Remaining` in the outbound adapter and waiting to get 429'd — wastes a request and slows end-to-end latency.
- Hard-coding retry with tight `setTimeout(100)` on 429 — always honor `Retry-After`, add jitter, cap attempts.
- Rate-limiting on `req.ip` behind a load balancer without honoring `X-Forwarded-For` — every request looks like it comes from the LB and all users share one bucket.

## Handoff / Next Steps

**To Builder** (RELAY_TO_BUILDER):
- Algorithm choice per surface, bucket sizing, cost table, per-tenant key scheme, storage backend (Redis / DynamoDB / in-memory), 429 response contract.

**To Gateway** (when public HTTP surface):
- Handoff if the limit is on a public REST/GraphQL endpoint — Gateway owns the API-level policy and OpenAPI `x-rate-limit` documentation.

**To Tempo** (when retry policy needs scheduling):
- Retry-After hint is transport-level; hand off the full retry schedule (exponential + jitter + max duration) to Tempo.

**To Sentinel** (RELAY_TO_SENTINEL):
- Brute-force / enumeration surfaces that require tighter per-IP or per-identity limits independent of quota.

**To Beacon** (RELAY_TO_BEACON):
- Metrics: throttle rate per tenant, 429 emit rate, bucket fill-level histogram, per-tier quota utilization, outbound platform-API remaining-budget, backpressure events (WS pause, queue prefetch reduction). SLO: throttle-induced failures < 0.1% of total inbound and no single tenant exceeds 5% of global budget sustained for > 5 min without alerting.
