# Logging Design Reference

Purpose: Design a structured logging contract — schema, correlation strategy, levels, sampling, and PII scrub — that turns logs into a queryable, cost-bounded, trace-correlated signal. Beacon owns the design; `Gear` owns the library and pipeline wiring.

## Scope Boundary

- **Beacon `log`**: log schema design, correlation ID strategy, level policy, source-side sampling policy, PII scrub rules, OpenTelemetry Logs signal adoption decision.
- **Gear `log`**: logging library setup (zap / zerolog / structlog / winston), log pipeline config (Fluent Bit, Vector, Loki, Datadog, CloudWatch), agent deployment, storage tier.

If the request is "what fields must every log record carry?" → `log`. If it is "how do I configure Fluent Bit to ship JSON logs to Loki?" → hand off to `Gear`.

## Principles

- Logs are structured events, not strings. Emit JSON (or OTLP Logs) — never free-form text in production.
- Every log record MUST carry correlation IDs: `trace_id`, `span_id`, `request_id`. Without them, logs are isolated and cannot be joined with traces or upstream requests.
- Levels are a policy, not a preference. DEBUG is not shipped to prod storage; INFO is the default volume driver; WARN/ERROR drive alerting.
- Sample at the source. Shipping 100% of DEBUG/INFO and deciding later is the most expensive mistake in observability.
- Never log PII. Scrub at the SDK layer, before serialization, not at the collector — collector-side scrubbing leaks during buffer replay.

## Log Schema Contract

Required fields on every record (OTel Logs semconv aligned):

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `timestamp` | ISO 8601 / epoch ns | SDK | UTC only; never local time |
| `severity_text` | string | SDK | DEBUG / INFO / WARN / ERROR / FATAL |
| `severity_number` | int | SDK | OTel SeverityNumber (1-24) |
| `body` | string | user | Human-readable message, no interpolated PII |
| `trace_id` | hex 32 | context | From active OTel span; `0` if none |
| `span_id` | hex 16 | context | From active OTel span |
| `request_id` | string | middleware | End-to-end correlation across async boundaries |
| `service.name` | string | resource | OTel resource attribute, stable across restarts |
| `service.version` | string | resource | For per-release debugging |
| `deployment.environment` | string | resource | prod / staging / dev |

Attributes (event-specific) go under `attributes.*` — typed, low-cardinality-friendly keys.

## Correlation ID Strategy

- `trace_id` / `span_id`: populated automatically via OTel context propagation. Do not generate your own.
- `request_id`: generated at the edge (ingress, API gateway) and propagated via `X-Request-Id` header. Must survive async boundaries (queue handoffs, background jobs) — stored on the job record itself.
- Async-job pattern: when enqueuing work, serialize `{trace_id, span_id, request_id}` into the job payload; on dequeue, restore context before the work's first log line.
- Never rely on thread-local storage alone — it breaks under `async/await`, goroutines, and worker-thread models.

## Level Policy

| Level | When to emit | Volume target | Alerting? |
|-------|--------------|---------------|-----------|
| DEBUG | Developer-only diagnostic | Disabled in prod by default; feature-flag to enable | No |
| INFO | State changes, request start/end, significant business events | 60-80% of volume | No |
| WARN | Recoverable anomaly, retry, degraded path taken | <5% of volume | Rate-based only |
| ERROR | Failed operation, unhandled exception, SLO-impacting event | <1% of volume; every one investigable | Yes, correlated with SLO burn |
| FATAL | Process about to exit | Near zero | Yes, immediate page |

If WARN exceeds 5% of records, the WARN definition has drifted — review and re-tier.

## Sampling at Source

Tail-based sampling (Beacon default for traces) does NOT apply to logs — log sampling is source-side.

- DEBUG: 0% in prod; 100% in dev.
- INFO for routine request logs: head-sample 10-20% with deterministic hashing on `trace_id` so sampled logs match sampled traces.
- INFO for business-critical events (payment, auth, order state): 100%, never sampled.
- WARN / ERROR / FATAL: 100%, never sampled.
- Apply sampling before serialization — skipped records must not pay serialization cost.

## PII Scrub Patterns

- Deny-list sensitive keys at the logger middleware: `password`, `token`, `secret`, `authorization`, `cookie`, `ssn`, `credit_card`.
- Redact structured fields, never regex over serialized output — regex is fragile and CPU-expensive.
- For user identifiers, log a hashed / pseudonymized ID, not the raw email.
- Bodies and query strings from HTTP middleware: default to drop; opt-in per route only after explicit review.
- Scrubbing lives in the SDK config, not in a downstream collector — pipeline failure or replay must never expose raw PII.

## OpenTelemetry Logs Signal

- Prefer OTLP Logs over legacy stdout-scrape for greenfield services — logs share resource attributes with traces and metrics, enabling native cross-signal queries.
- For brownfield, keep the existing pipeline and add OTel as an additional exporter; deprecate the legacy path once parity is verified.
- Use OTel Logs Bridge API (stable) to preserve existing library calls while emitting OTLP records.
- Collector receives logs alongside traces/metrics in the same OTLP pipeline; apply processors (batch, memory limiter, attributes) consistently with other signals.

## Anti-Patterns

- Free-form string logs in prod (`logger.info(f"user {id} did {action}")`) — unqueryable, PII-prone.
- Generating your own `trace_id` when an OTel SDK is present — breaks trace correlation.
- Shipping 100% of DEBUG to centralized storage "just in case" — dominant cost driver and rarely queried.
- Scrubbing PII at the collector — replay and buffer-disk scenarios leak the raw record.
- Using log levels as severity theater (everything is WARN to "be safe") — destroys alert signal.
- Embedding high-cardinality values (user ID, request ID) as METRIC labels because logs are expensive — correct answer is to fix the log pipeline, not poison metrics.

## Handoff to Gear

When the log design is accepted, hand off to `Gear` with:

- Field contract (required + optional attributes with types).
- Correlation ID propagation rules (headers, async-job payload shape).
- Level policy and source-side sampling rates per level.
- PII deny-list and scrub rules.
- OTel Logs exporter decision (native OTLP vs bridge vs stdout-scrape).
- Volume estimate (records/sec and GB/day) for pipeline sizing.
- Retention requirement per level (ERROR: 90d, INFO: 7-14d, DEBUG: n/a).

## Cross-Links

- `golden` — which signals need log coverage (errors always; latency via trace, not log).
- `tracing` — correlation-ID propagation and resource attribute consistency.
- `slo` — ERROR-level records feeding SLI error counts.
- `alerts` — ERROR rate burn-rate alerts and runbook links.
- Gear `log` — implementation of this design.
