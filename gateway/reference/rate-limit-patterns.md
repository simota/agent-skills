# Rate Limit Patterns Reference

Purpose: Design rate-limiting for an API. Choose algorithm (token bucket / leaky bucket / sliding window / fixed window), scope (per-key / per-tenant / per-route / per-IP), distributed enforcement, and signaling per the IETF `RateLimit` header draft + RFC 6585 (HTTP 429).

> **2026-05 baseline**: The IETF `RateLimit-Policy` + `RateLimit` header fields are **still an Internet-Draft** — latest `draft-ietf-httpapi-ratelimit-headers-10` (2025-09-24, Standards Track, [datatracker](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/)). **No RFC number yet** — earlier docs in this skill that cited "RFC 9331" were wrong (RFC 9331 is actually the L4S ECN spec). The draft remains stable enough to ship against — major APIs (GitHub, Stripe, Cloudflare) already emit these or a superset — but track the working group for the final RFC. The header field values follow **RFC 9651** (Structured Field Values for HTTP, 2024-09, obsoletes RFC 8941). For non-strict 429 bodies, use **RFC 9457 Problem Details (2023-07)**.

## Scope Boundary

- **gateway `rate-limit`**: API rate-limit contract design (this document).
- **Builder (elsewhere)**: Middleware implementation (Redis INCR, sliding-log, etc.).
- **Beacon (elsewhere)**: Observability of rate-limit events.
- **Probe (elsewhere)**: Abuse pattern verification.
- **scaffold (elsewhere)**: Infrastructure rate-limit (CDN / WAF / API Gateway).
- **gateway `auth` (elsewhere)**: Auth-tier-aware limits use auth identity.

## Why Rate Limit

- Spike protection (sudden traffic).
- Fair sharing (one tenant doesn't starve others).
- Cost control (per-tenant budget).
- Abuse defense (brute force, scraping).
- DDoS mitigation (in-app layer; infra is primary).

## Four Algorithms

| Algorithm | How it works | Strength | Weakness |
|-----------|--------------|----------|----------|
| **Token bucket** | Bucket has capacity C, refilled at rate R; each request takes 1 token | Smooth + bursty; intuitive | State per key |
| **Leaky bucket** | Queue with max size; processes at rate R | Smooth output, hard cap | Buffering; not request-counting |
| **Fixed window counter** | Count requests in N-second window; reset at boundary | Simple O(1) | 2x burst at boundary |
| **Sliding window log** | List of timestamps in the last N seconds | Exact | O(N) memory; expensive |
| **Sliding window counter** | Hybrid: previous window weighted by elapsed | O(1) + smoother | Approximation |

### Selection matrix

| Requirement | Choose |
|-------------|--------|
| User-facing API with bursts | Token bucket |
| Sustained protection (gateway) | Leaky bucket |
| Simplest implementation | Fixed window |
| High-precision throttle (financial) | Sliding window log |
| Default for distributed APIs | Sliding window counter or token bucket |

## Scoping

| Scope | When |
|-------|------|
| Per API key | Default; tracks the credentialed app |
| Per tenant | Multi-tenant SaaS; share quota across tenant's apps |
| Per route | Costly endpoints (search, AI inference) |
| Per IP | Anonymous; abuse defense |
| Per user (`sub` claim) | Per-user fairness inside a tenant |
| Composite | Combine: e.g., (tenant + route) tier |

Multi-layer is normal: per-IP cap + per-key cap + per-route cap.

## Distributed Enforcement

Single-node counters break under horizontal scaling. Patterns:

| Pattern | Notes |
|---------|-------|
| Redis INCR + EXPIRE | Most common; atomic; fast |
| Redis Lua script | Atomic multi-step (e.g., token bucket update) |
| Envoy ratelimit service | Sidecar / mesh-native |
| Cloud-native (AWS API Gateway, GCP Cloud Endpoints) | Managed; less flexible |
| Local cache + lossy sync | "Approximate" rate limit; fast but imprecise |
| Cell-based (Stripe pattern) | Each shard has own counter; aggregate periodically |

For high QPS: Redis Cluster + Lua, or local approximate + periodic flush.

## IETF `RateLimit` Headers (draft-ietf-httpapi-ratelimit-headers-10, 2025-09)

The IETF working-group draft (Standards Track, not yet an RFC; expires 2026-03).

```
RateLimit: "default";r=42;t=15
RateLimit-Policy: "default";q=100;w=60
```

Where:
- `RateLimit-Policy` advertises one or more named quota policies — `q` is the quota, `w` is the window in seconds (RFC 9651 structured-field syntax).
- `RateLimit` reports the **remaining** quota `r` and time-to-reset `t` (seconds, NOT a UTC timestamp) for the named policy.
- Each policy is a named inner list — multiple policies can coexist (e.g., one for the default plan, one for a search-only sub-bucket).

Older `X-RateLimit-Limit` / `X-RateLimit-Remaining` / `X-RateLimit-Reset` triplets remain widely deployed; emit them in parallel with the IETF form for backward compatibility until the draft becomes an RFC. The values follow **RFC 9651** Structured Field Values (2024-09, obsoletes RFC 8941). Do not cite "RFC 9331" for rate limiting — that number is L4S ECN.

## 429 Response

```
HTTP/1.1 429 Too Many Requests
Content-Type: application/problem+json
Retry-After: 30
RateLimit: "default";r=0;t=30

{
  "type": "https://api.example.com/errors/rate-limit-exceeded",
  "title": "Rate limit exceeded",
  "status": 429,
  "detail": "Quota of 100 requests/minute exceeded for API key",
  "instance": "/orders",
  "retry_after_seconds": 30
}
```

`Retry-After` SHOULD be present (RFC 6585). Use Problem Details (**RFC 9457**, 2023-07) for the body.

## Tier / Plan Design

For commercial APIs:

| Plan | Limit | Burst | Reset |
|------|-------|-------|-------|
| Free | 60 req/min | 10 | per minute |
| Pro | 1000 req/min | 100 | per minute |
| Enterprise | 10000 req/min | 1000 | per minute |
| Internal | unlimited | n/a | n/a |

Signal current plan via `RateLimit-Policy` header for client-side awareness.

### Endpoint-specific overrides

Costly endpoints (search, AI, large exports) get separate buckets:

```
RateLimit-Policy: 100;w=60;name="default", 10;w=60;name="search"
```

## Backpressure & Queueing

- 429 with `Retry-After` is the contract. Clients implement exponential backoff.
- Some APIs queue rather than reject (rare; mostly batch APIs).
- Server-side concurrency limit (semaphore) is a different thing — covers in-flight; rate limit covers total per window.

## Abuse Patterns

Things to design against:
- **Burst at window boundary** (fixed-window 2x): use sliding window.
- **Distributed scrape across many keys**: per-IP supplement.
- **Free-tier farming** (1k accounts each at 60/min): per-IP + signup CAPTCHA + email verification.
- **Token leak**: rotation + anomaly detection (Vigil).
- **Slow-loris like resource holding**: separate timeout limits.

## Workflow

```
INVENTORY    →  identify endpoints with cost characteristics (cheap / mid / expensive)
             →  identify caller types (1st-party / 3rd-party / partner / internal)

ALGORITHM    →  default token bucket or sliding window counter
             →  per-endpoint override for expensive routes

SCOPING      →  primary: per-API-key
             →  supplemental: per-IP for anonymous; per-tenant for SaaS
             →  composite for plan tiers

LIMITS       →  per plan tier
             →  per endpoint override
             →  burst capacity

ENFORCEMENT  →  Redis Cluster + Lua for atomic
             →  or Envoy ratelimit / cloud-native
             →  fallback strategy if Redis is down (fail-open vs fail-closed)

SIGNALING    →  RFC 9331 RateLimit headers on EVERY response (not just 429)
             →  429 response with Retry-After + Problem Details
             →  RateLimit-Policy header

OBSERVE      →  metric: per-key throttle rate (Beacon)
             →  alert on tenant approaching quota
             →  audit: 429 rate per endpoint

DOCS         →  client guidance: backoff, idempotency, header reading
             →  per-plan limits

HANDOFF      →  Builder: middleware impl
             →  Beacon: observability
             →  Scaffold: CDN/WAF/API GW layer
             →  Probe: abuse-pattern testing
             →  Vigil: anomaly detection
```

## Output Template

```markdown
## Rate Limit Design: [API]

### Scope Inventory
| Endpoint pattern | Cost | Default limit | Notes |
|------------------|------|---------------|-------|
| /v1/users | cheap | 1000/min | per key |
| /v1/search | expensive | 60/min | per key |
| /v1/ai/* | very expensive | 10/min | per tenant |

### Algorithm
- **Default**: [token bucket / sliding window counter]
- **Per-route override**: [list]

### Scoping
- Primary: per-API-key
- Supplemental: [per-IP / per-tenant / per-user]

### Plan Tiers
| Plan | Limit | Burst | Window |
|------|-------|-------|--------|
| Free | ... | ... | ... |
| Pro | ... | ... | ... |
| Enterprise | ... | ... | ... |

### Enforcement
- **Backend**: [Redis Cluster + Lua / Envoy / cloud-native]
- **Failure mode**: [fail-open / fail-closed; rationale]
- **Latency target**: [≤1ms p99 added]

### Headers
- `RateLimit: limit=N, remaining=N, reset=S`
- `RateLimit-Policy: ...`
- `Retry-After: S` (on 429)

### 429 Body (Problem Details, RFC 9457)
[example body]

### Observability
- per-key throttle rate
- per-endpoint 429 rate
- approaching-quota alert at [80%]

### Client Documentation
- Backoff: exponential with jitter
- Read RateLimit-Remaining for proactive throttle
- Idempotency keys for safe retry

### Handoffs
- Builder: middleware impl
- Beacon: observability + alerts
- Scaffold: CDN/WAF/API GW layer
- Probe: abuse-pattern testing
- Vigil: anomaly detection
- Voice: customer-facing rate-limit docs
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Fixed window only (2x boundary burst) | Sliding window or token bucket |
| Per-IP only with NAT'd users | Add per-key for authenticated; per-IP supplemental |
| No `RateLimit-*` headers | Always present; clients can self-throttle |
| 429 without Retry-After | Mandatory per RFC 6585 |
| Shared in-memory counter under horizontal scaling | Use Redis (or distributed equivalent) |
| Fail-closed when Redis is down | Fail-open with degraded mode (or risk full outage) |
| Single global limit ignoring endpoint cost | Per-endpoint overrides for expensive routes |
| Surprising customers with limits | Document; signal via headers |
| Limit without observability | Can't tune; can't alert |
| Limit on auth-failed requests counted toward user | Pre-auth limit (per-IP) for failed; post-auth for success |
| Disabled rate limit "for the launch" | First brownout teaches the lesson; design from day 1 |

## Deliverable Contract

When `rate-limit` completes, emit:

- **Endpoint inventory** with cost classification.
- **Algorithm choice** + per-route overrides.
- **Scoping plan** (key / tenant / IP / composite).
- **Plan tier table** with limits + bursts.
- **Enforcement backend** + failure mode.
- **Header spec** (RFC 9331) + 429 body.
- **Observability hooks**.
- **Client documentation** essentials.
- **Handoffs**: Builder, Beacon, Scaffold, Probe, Vigil, Voice.

## References

- **draft-ietf-httpapi-ratelimit-headers-10** — RateLimit header fields for HTTP (2025-09-24, Standards Track, not yet RFC) — [datatracker](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/)
- RFC 9651 — Structured Field Values for HTTP (2024-09, obsoletes RFC 8941)
- RFC 6585 — Additional HTTP Status Codes (429)
- RFC 9457 — Problem Details for HTTP APIs (2023-07, obsoletes RFC 7807)
- IETF HTTPAPI Working Group — current drafts
- Stripe API rate-limit documentation
- GitHub REST API rate-limit documentation
- Cloudflare — distributed rate-limit patterns
- Envoy Proxy — global rate-limit service
- Redis — INCR + EXPIRE patterns; Lua scripting
- AWS API Gateway — usage plans
- "Rate Limiting Strategies and Techniques" — Stripe Engineering
- Marc Brooker — "Sliding Window Rate Limiter" (Amazon Builder's Library)
