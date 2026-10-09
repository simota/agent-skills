# Observability-Driven Debugging

**Purpose:** Runtime-debugging guidance for traces, logs, metrics, profiling, and production-safe probing.
**Read when:** Production signals, distributed systems, or runtime-only failures require observability evidence.

## Contents

- Four signals
- Distributed tracing
- Structured logging
- Profiling and leak detection
- Production-safe debugging

## The Four Signals

| Signal | Role | Example Tools |
|--------|------|---------------|
| Metrics | time-series resource and health data | Prometheus, Grafana |
| Traces | distributed request path | Jaeger, Tempo, Zipkin |
| Logs | event details | Loki, Elasticsearch |
| Profiles | CPU and memory hotspots | Pyroscope, pprof |

Correlation path:

`metrics -> traces -> logs -> profiles`

## Distributed Tracing

| Term | Meaning |
|------|---------|
| Trace | full request path across services |
| Span | one operation within that path |
| `trace_id` | request-wide identifier |
| `span_id` | per-operation identifier |
| `parent_span_id` | link to the parent operation |
| baggage | cross-service metadata |

Rules:

- Include `trace_id` and `span_id` in every signal.
- Propagate `traceparent`; downstream services must not start unrelated traces.
- Prioritize operations appearing in `50%+` of failing traces.

## Structured Logging

### Required Fields

```json
{
  "timestamp": "2026-03-04T10:15:30.123Z",
  "level": "ERROR",
  "service": "payment-service",
  "trace_id": "abc123def456",
  "span_id": "789ghi",
  "message": "Payment processing failed",
  "error_code": "PAYMENT_TIMEOUT",
  "duration_ms": 5032
}
```

### Rules

- Use JSON logs.
- Never log secrets, tokens, passwords, private keys, or personal data.
- Keep `ERROR` events at `100%`.
- Sample routine events at around `10%` when log volume requires it.

## Profiling And Leak Detection

| Tool | Typical Overhead | Best For |
|------|------------------|----------|
| Pyroscope | `2-5%` | multi-language continuous profiling |
| `pprof` | `~1%` | Go |
| async-profiler | `~2%` | Java |
| eBPF agent | `~1%` | code-change-free sampling |

Common JS leak patterns:

- uncleared timers or intervals
- detached DOM node references
- retained closures
- unremoved event listeners

## Production-Safe Debugging

- Shadow traffic: safe only if writes and external calls cannot affect production state.
- Canary analysis: expose `1-5%` of traffic and watch error rate, latency, CPU, memory, and change-specific metrics.
- Feature-flagged debug logging: temporarily enable extra detail without redeploying.

## Scout Usage

| Phase | How To Use Observability |
|-------|--------------------------|
| `RECEIVE` | quantify symptoms with alerts and metrics |
| `REPRODUCE` | identify failing paths with traces |
| `TRACE` | correlate traces, logs, and metrics |
| `LOCATE` | use profiling or span detail to isolate the hotspot |
| `ASSESS` | quantify blast radius |
| `REPORT` | attach evidence links to traces, logs, or dashboards |
