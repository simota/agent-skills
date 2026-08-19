# Tenant Quota and Throttling Reference

Purpose: Per-tenant rate limits, fair-share scheduling, and noisy-neighbor mitigation. Defines quota algorithms (token bucket, leaky bucket, weighted round-robin), soft-vs-hard quota semantics, burst budget tuning, and overage-billing handoff. The goal is predictable performance per tenant under contention, with observability that exposes per-tenant degradation before SLO burns.

## Scope Boundary

- **shard `quota`**: per-tenant rate limits, fair-share scheduling, soft/hard quota policy, burst budgets, overage-billing handoff.
- **shard `isolation` / `rls` / `routing` / `scale` (elsewhere)**: structural tenant isolation, RLS, routing, and shard-level capacity. Quota is the *runtime* fairness layer on top of `scale`.
- **shard `provisioning` (elsewhere)**: setting plan-tier limits at tenant creation. Quota enforces those limits at runtime.
- **shard `migration` (elsewhere)**: relocating tenants. Migration may be triggered when quota signals chronic noisy-neighbor pressure.
- **beacon (elsewhere)**: SLO definition and burn-rate alerting. Quota produces per-tenant metrics; Beacon owns the SLO contract.
- **tempo (elsewhere)**: scheduled batch / business-calendar logic. Quota throttles real-time traffic; Tempo schedules deferred work.
- **gateway (elsewhere)**: HTTP layer rate-limit headers (`X-RateLimit-*`, `Retry-After`). Quota defines the policy; Gateway emits the headers.
- **ledger (elsewhere)**: overage billing and unit economics. Quota emits overage events; Ledger reconciles to invoices.

## Workflow

```
DEFINE    →  enumerate axes: requests/sec, concurrent jobs, storage, egress
          →  per plan tier: limit, burst, soft|hard, observability tags

ALGORITHM →  pick token bucket | leaky bucket | sliding window per axis
          →  pick scheduler: weighted-fair-queue | strict-priority | WRR

ENFORCE   →  middleware checks bucket; if empty → soft (alert) | hard (429)
          →  emit metric: tenant_id, axis, action, remaining

OBSERVE   →  per-tenant percentiles, top-N consumers, near-limit dashboards
          →  detect noisy neighbor pattern before SLO burn

ESCALATE  →  chronic offender → migration to dedicated shard | plan upgrade
          →  overage events → Ledger for billing handoff
```

## Algorithm Selection

| Algorithm | Shape | Best for | Avoid for |
|-----------|-------|----------|-----------|
| **Token bucket** | Burst-tolerant up to capacity, then steady | API rate limits, user-facing endpoints | Strict smoothing requirements |
| **Leaky bucket** | Constant outflow regardless of input burst | Outbound webhook fan-out, downstream protection | UX-facing endpoints (no burst headroom) |
| **Fixed window** | Counter resets every N seconds | Daily/monthly quotas, low-precision needs | Per-second precision (boundary spikes) |
| **Sliding window log** | Exact, per-event timestamps | Compliance-grade limits, low-volume APIs | High-traffic (memory cost) |
| **Sliding window counter** | Approximation of log, weighted | Mid-volume APIs needing better than fixed-window | Sub-millisecond precision |
| **Concurrency (semaphore)** | Cap on in-flight, not rate | Long-running jobs, DB connections, LLM calls | Bursty short requests |

Token bucket is the default for HTTP rate limits because it absorbs natural traffic burstiness while bounding average rate. Leaky bucket is preferred for protecting a fragile downstream — burst on the input must not become burst on the output.

## Fair-Share Scheduling

| Scheduler | Behavior | Use when |
|-----------|----------|----------|
| **FIFO** | Order of arrival | Single-tier SaaS, no plan differentiation |
| **Weighted Round-Robin (WRR)** | Quotas proportional to weight | Plan tiers (Free=1, Pro=5, Enterprise=20) |
| **Weighted Fair Queue (WFQ)** | Per-tenant queues, dequeue weighted | Heterogeneous job sizes; prevents starvation |
| **Strict priority** | Higher tier always preempts | SLA-bound enterprise + best-effort free |
| **Deficit Round-Robin (DRR)** | Variable-size aware, fair across job sizes | Background jobs with mixed durations |

WFQ is the safest default for multi-tenant background workers — it prevents a single tenant from monopolizing the worker pool even if their jobs are huge. Strict priority is dangerous without a starvation guard for low-priority tenants.

## Soft vs Hard Quota

| Quota type | Action when exceeded | Emit | Use for |
|------------|---------------------|------|---------|
| **Soft** | Allow, log, alert ops | `quota.soft.exceeded` | Trends, capacity planning, UX-warning thresholds |
| **Hard** | Reject (429 / job-rejected) | `quota.hard.exceeded` | Billing limits, abuse prevention, downstream protection |
| **Overage-billed** | Allow, meter, charge | `quota.overage.consumed` | Plans with metered overage clause |
| **Throttled** | Slow down (delay, queue) | `quota.throttled` | Background jobs, non-interactive paths |

Pair every hard quota with a soft warning at ~80% of limit so the customer can act before being blocked. Hard-only quotas produce surprise outages and support tickets.

## Burst Budget Tuning

Token bucket has two parameters: rate (tokens/sec) and capacity (max bucket).

| Capacity / rate ratio | Behavior | Fits |
|-----------------------|----------|------|
| capacity = rate × 1s | No burst (smooth) | Outbound to fragile downstream |
| capacity = rate × 10s | Mild burst | Default for user-facing APIs |
| capacity = rate × 60s | Strong burst | Bulk import endpoints, batch APIs |
| capacity = rate × 600s | Hoard-and-drain | Daily-quota-style usage; risks long stalls after burst |

Tune capacity by observing real traffic distribution. If P99 burst over 10s is 3× P50, capacity should be at least 3× rate.

## Per-Tenant Isolation Tactics

| Tactic | Mechanism | Trade-off |
|--------|-----------|-----------|
| **Connection pool partition** | Per-tenant min/max DB connections | Underutilization if traffic uneven |
| **Worker pool reservation** | Reserved slots for enterprise tier | Free-tier waits longer |
| **Cgroup CPU/memory caps** | OS-level per-process limits | Container restart on OOM |
| **Query timeout per tenant** | Lower timeout for free tier | Free-tier sees more timeouts on heavy queries |
| **Concurrent request cap** | Semaphore per tenant | Latency spikes when at cap |
| **Storage IOPS cap** | DB-level (e.g., RDS performance insights) | Engine-specific |
| **Egress bandwidth cap** | Reverse proxy / CDN | Hard to enforce per-tenant in shared CDN |

## Observability Hooks

Every quota decision emits a metric with at minimum: `tenant_id, axis, decision, remaining, plan_tier`. Required dashboards:

| Dashboard | Purpose |
|-----------|---------|
| Top-N tenants by axis | Identify noisy neighbors |
| Per-tenant percentiles (p50/p95/p99) | Detect tenant-specific degradation hidden by global metrics |
| Near-limit tenants (>80% of quota) | Pre-emptive customer success outreach |
| Overage events | Feed Ledger for billing |
| Throttle/reject rate per tenant | Customer support context on "why is it slow?" |

Aggregate-only dashboards hide the case where one enterprise tenant has 3s p99 while global p99 is 200ms. Per-tenant segmentation is mandatory in multi-tenant SaaS observability.

## Overage Billing Handoff

When a tenant exceeds a metered (overage-billable) quota, emit an event with: `tenant_id, axis, units_over, period, timestamp, idempotency_key`. The handoff to Ledger:

| Field | Why |
|-------|-----|
| idempotency_key | Prevents double-billing on event-bus retry |
| period | Aligns with billing cycle bucket |
| units_over | The chargeable quantity |
| axis | Maps to a SKU / line item |
| reference_event_ids | Audit trail back to underlying requests |

Overage events should be billable-grade durable (write-ahead-log or transactional outbox), not best-effort metrics.

## Anti-Patterns

- **Global rate limit only** — protects the platform but lets one tenant consume the entire budget. Per-tenant limits are mandatory.
- **Hard quota with no soft warning** — customer hits 429 with no prior signal. Always pair with ~80% soft alert.
- **Aggregate-only metrics** — global p99 looks healthy while one enterprise tenant suffers. Always segment by tenant_id.
- **Strict priority without starvation guard** — best-effort tier never schedules under sustained enterprise load.
- **Token bucket capacity = rate** — eliminates burst tolerance; legitimate spiky traffic gets throttled.
- **Fixed-window quotas at API boundary** — boundary spikes (2× burst at the window flip) bypass intent of the limit.
- **Quota without idempotency on overage events** — retries from event bus produce duplicate billing.
- **Throttling background jobs the same way as user requests** — interactive paths need fast reject; background paths benefit from delay/queue.
- **Limits hardcoded outside plan-tier config** — quota changes require code deploy; should be driven by plan-tier metadata loaded at request time.

## Handoff

- **To Beacon**: per-tenant SLI (latency, error rate, throttle rate); SLO burn-rate alerts segmented by tenant.
- **To Gateway**: HTTP rate-limit response policy (`429`, `Retry-After`, `X-RateLimit-Remaining` headers).
- **To Tempo**: scheduled overage rollup, daily/monthly counter reset, billing-cycle alignment.
- **To Ledger**: overage events for billing; plan-tier unit-cost reconciliation.
- **To shard `migration`**: chronic noisy-neighbor signal → trigger isolation-level upgrade (pool → schema → dedicated DB).
- **To shard `provisioning`**: plan-tier quota config consumed at tenant creation; quota enforced at runtime from same config.
- **To Builder**: middleware/interceptor implementation, bucket store (Redis/in-mem), scheduler code, observability emitters.
