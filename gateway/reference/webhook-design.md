# Webhook Provider Design Reference

Purpose: Design the contract for an API that EMITS webhooks to subscribers. The contract covers signature, idempotency, retry, ordering, payload shape, and deprecation signaling — everything a subscriber must trust to build against the emitter.

> **2026-05 baseline**: For new webhook contracts, align with **[Standard Webhooks](https://www.standardwebhooks.com/)** ([spec](https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md), Svix-led). Adopted by **OpenAI, Anthropic, Google Gemini, Twilio, Supabase, Vanta, Drata, Kong, PagerDuty, Etsy, TaskRabbit** and many others. Standard Webhooks pins HMAC-SHA256 over `{webhook-id}.{webhook-timestamp}.{raw-body}`, a 5-minute timestamp tolerance, and `webhook-id` for receiver-side idempotency — one verification library works across all adopters. For event-payload structure (especially in multi-system pipelines), use **CloudEvents 1.0.2** ([spec](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/http-webhook.md), CNCF) — supported natively by Amazon EventBridge, Google Eventarc, Knative. OpenAPI 3.2 (2025-09) finally has first-class `webhooks` modeling (carried forward from 3.1).

## Scope Boundary

- **Gateway `webhook`**: the PROVIDER side. Designs the emit contract — what the provider promises subscribers.
- **Builder `integrate`**: the CONSUMER side. Receives a webhook from a third party, verifies signature, idempotently processes, and acks. Gateway hands off the provider contract; Builder implements the consumer.
- **Builder `api`**: the IMPLEMENTATION of the provider. Writes the emit queue, signer, retry worker, DLQ. Receives the webhook contract from Gateway via `GATEWAY_TO_BUILDER`.
- **Relay**: messaging integration and bot/adapter patterns. If the webhook target is a chat platform (Slack/Discord), Relay owns the adapter; `webhook` still owns the generic emit contract upstream of the adapter.

If the question is "what do I promise subscribers about delivery?" → `webhook`. If it is "how do I receive a Stripe/GitHub webhook safely?" → Builder `integrate`. If it is "how do I build the queue and signer?" → Builder `api`.

## Signature Verification — HMAC-SHA256 with Signed Timestamp

Every outbound webhook carries a signature so subscribers can verify origin and integrity.

Two header conventions are common in 2026:

**Standard Webhooks (recommended for new providers)** — note the `webhook-*` prefix instead of `X-` (RFC 6648 deprecated `X-` headers in 2012, finally being applied here):
- `webhook-id: msg_2KWPBgLlAfxdpx2AI54pPJ85f4W` — stable event ID for idempotency.
- `webhook-timestamp: 1674087231` — Unix seconds.
- `webhook-signature: v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=` — base64 HMAC-SHA256 of `{webhook-id}.{webhook-timestamp}.{raw-body}` using a versioned key.

**Legacy Stripe-style (still widely deployed)**:
- `X-Signature: t=<unix-seconds>,v1=<hex-hmac>` — timestamp + versioned HMAC.
- `X-Event-Id: evt_01HXYZ...` — stable event ID for idempotency.
- `X-Event-Type: order.completed` — typed event selector.
- `X-Delivery-Attempt: 3` — current retry count.

Provider signs: `hmac_sha256(secret, f"{id}.{t}.{raw_body}")` (Standard Webhooks) or `hmac_sha256(secret, f"{t}.{raw_body}")` (Stripe-style). Include the timestamp in the signing string to block replay.

Subscriber-side verification rules (document these in the contract):
1. Reject if `|now - t|` > 5 minutes → blocks replay of stolen payloads.
2. Compare signatures with a timing-safe function (`crypto.timingSafeEqual` / `hmac.compare_digest`) — regular `==` leaks timing.
3. Sign the raw request body bytes, not the parsed JSON — body reserialization changes the hash.

Rotate signing secrets by supporting `v1=` and `v2=` simultaneously during the rotation window. Deprecate `v1=` with the Sunset header (see below).

## Idempotency Key

Subscribers must be able to retry safely. Provide one stable `X-Event-Id` per logical event — the same ID across every retry of the same delivery.

Subscriber contract:
- Store the event ID on first successful processing.
- On replay of the same ID, return 2xx without re-processing.
- TTL the idempotency store at least as long as your max retry window (see below).

Never derive the ID from the payload hash — two distinct business events can produce identical payloads.

## Retry and Dead-Letter Queue

Document the retry policy explicitly so subscribers can size their idempotency window.

Recommended policy:
- Retry on 5xx, 408, 429, and network timeout. Do NOT retry 4xx (except 408/429) — the subscriber rejected the payload.
- Exponential backoff with full jitter: `delay = min(cap, base * 2^attempt) * random(0.5, 1.0)`.
- Typical schedule: 1m, 5m, 30m, 2h, 12h, 24h (6 attempts over ~40h).
- After the final attempt, move to a **dead-letter queue** and emit an observability signal (alert + dashboard).
- Expose a `GET /v1/webhook-deliveries/{id}` endpoint so subscribers can inspect and manually replay from the DLQ.

Document max retry window in the contract — subscribers use it to size their `X-Event-Id` dedup TTL.

## Event Ordering Guarantees

Be honest about what you promise. Three realistic levels:

| Level | Contract | When |
|-------|----------|------|
| Best-effort unordered | Events may arrive out of order or duplicated | Default for fan-out; simplest infra |
| Per-resource ordered | Events for the same `resourceId` arrive in emitted order | Requires partitioned queue keyed by resource |
| Globally ordered | Every subscriber sees the same total order | Expensive; rarely needed; requires single-writer log |

Include a monotonic `sequence` field per resource so subscribers can detect out-of-order delivery and reconcile.

## Payload vs Thin-Notification

| Style | Payload | Trade-off |
|-------|---------|-----------|
| Fat payload | Full resource in the event body | Convenient for subscribers; leaks PII if the delivery URL is misconfigured or logs the body; body size stresses retry storage |
| Thin notification | `{eventType, resourceId, resourceUrl}` — subscriber fetches current state via authenticated callback | Safer for PII; always current state (no stale payload vs DB); requires subscriber round-trip and valid credentials |

Default: **thin notification** for anything touching PII, payment, or auth. **Fat payload** for low-sensitivity, high-volume events where round-trip cost matters.

Hybrid: send thin notification plus a stable snapshot URL — subscriber decides.

## Sunset and Deprecation Signaling

Webhook event types evolve. Signal retirement the same way HTTP APIs do:

- **`Deprecation: Sun, 01 Jun 2026 00:00:00 GMT`** — RFC 9745, marks the event type as deprecated from the given date.
- **`Sunset: Sun, 01 Dec 2026 00:00:00 GMT`** — RFC 8594, date after which the event will no longer be emitted.
- **`Link: <https://api.example.com/docs/events/v2>; rel="successor-version"`** — pointer to replacement.

Combine with emitting both old and new event types in parallel during the transition — subscribers migrate at their own pace within the window.

Minimum deprecation window: 6 months (matches Gateway's default for REST/GraphQL breaking changes).

## Subscriber Management

The provider contract also covers:
- Subscription registration endpoint — CRUD for `(url, eventTypes[], secret)`.
- Secret rotation flow — new secret visible exactly once on creation; provider supports N+1 simultaneous secrets during rotation.
- Automatic disable after K consecutive DLQ events — prevents indefinite retry against a dead subscriber; emit an alert + email.
- Test delivery endpoint — subscriber can trigger a known event on demand to validate signature/endpoint wiring.

## Anti-Patterns

- Signing the parsed JSON instead of the raw body.
- Using `==` to compare signatures (timing attack).
- Omitting the timestamp from the signing string (replay attack).
- No idempotency key — every retry is a new event as far as subscribers can tell.
- Infinite retry with no DLQ — fills the queue forever, hides failures.
- Promising ordering you cannot deliver.
- Fat payload with PII to an HTTP (not HTTPS) URL.
- Silently removing event types — always Deprecation + Sunset first.
- Sharing one secret across all subscribers — compromise of one leaks all.

## Handoff

- **→ Builder `api`**: contract doc, signing algorithm + header names, retry schedule, DLQ policy, subscription CRUD schema, observability signals. Builder implements the emit queue, signer, retry worker.
- **→ Builder `integrate`**: NOT a handoff from `webhook` — they are opposite sides of the same contract. Cross-link so a consumer building against this provider can see the verification rules, idempotency TTL, and retry window without re-deriving them.
- **→ Relay**: if the primary consumer is a chat platform, Relay builds the adapter that translates the webhook event into a platform-native message. Gateway `webhook` still owns the upstream emit contract.
- **→ Sentinel**: security review of the signing/rotation flow before the contract goes public.
