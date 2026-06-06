# Golden Signals / RED / USE Reference

Purpose: Before setting SLO targets, select WHAT to measure. `golden` is the signal-selection method that precedes `slo`. Apply Google SRE Golden Signals as the universal frame, then narrow to RED (request-driven) or USE (resource-driven) per component.

## Scope Boundary

- **Beacon `golden`**: SIGNAL SELECTION — which SLIs to measure, at which boundary, with which method (RED / USE). Output: SLI candidate list.
- **Beacon `slo`**: TARGET SETTING — given SLIs, set SLO percentage, time window, and error budget.
- **Beacon `dashboard`**: VISUALIZATION — render the signals picked here as RED/USE panels.

Typical flow: `golden` → `slo` → `alerts` → `dashboard`. Skipping `golden` leads to SLOs that measure convenient metrics rather than user-facing reliability.

## The Four Golden Signals (Google SRE)

Defined in the Google SRE book, Ch. 6. Every user-facing service should have all four.

| Signal | Meaning | Typical SLI |
|--------|---------|-------------|
| Latency | Time to serve a request | p95 / p99 request duration, separated by success vs error |
| Traffic | Demand on the system | requests/sec, messages/sec, concurrent sessions |
| Errors | Rate of failed requests | explicit 5xx + implicit (wrong content, policy violation) |
| Saturation | How "full" the service is | queue depth, CPU utilization vs headroom, memory pressure |

Rules:

- Measure latency for successful and failed requests SEPARATELY. A fast-failing error bucket masks user-visible slowness.
- Errors include implicit failures (200 with wrong body, policy-violating responses) — not only HTTP 5xx.
- Saturation leads the others — a saturated service predicts future latency/error incidents.

## RED Method (Tom Wilkie, Weaveworks)

For REQUEST-DRIVEN services (HTTP APIs, gRPC, RPC endpoints).

| Letter | Metric | Notes |
|--------|--------|-------|
| R | Rate | requests/sec per service, per endpoint |
| E | Errors | failed-request rate; error RATIO = errors / rate |
| D | Duration | distribution of request latency, emit as histogram (not avg) |

RED is a lens on Golden Signals: R = Traffic, E = Errors, D = Latency. Saturation is tracked separately via USE on the service's resources.

## USE Method (Brendan Gregg)

For RESOURCE-DRIVEN components (CPU, memory, disk, network, thread pools, DB connections).

| Letter | Metric | Notes |
|--------|--------|-------|
| U | Utilization | % of time the resource is busy |
| S | Saturation | queue / wait time when utilization saturates — the work that couldn't run |
| E | Errors | count of error events from the resource (ECC, disk errors, TCP retransmits) |

Apply USE per resource. CPU-bound and I/O-bound components surface different saturation signals; don't conflate them.

## Picking RED vs USE

| Component type | Method | Example |
|----------------|--------|---------|
| HTTP / gRPC / RPC service | RED | Checkout API, user-profile service |
| Message consumer | RED with "request" = message | Kafka consumer, SQS worker |
| Database (as a dependency) | RED (from caller) + USE (on the DB box) | Postgres, MySQL |
| Cache / queue / broker | USE primarily | Redis, RabbitMQ, Kafka broker |
| Compute host, container, pod | USE | K8s node, EC2, Lambda concurrency |
| Batch / scheduled job | RED per run + duration SLO | Nightly ETL |

For services that do both (API with background workers), define RED on the request path and USE on the shared resource pool.

## SLI Extraction Templates

Per endpoint (RED):

```
SLI: availability = count(status < 500) / count(total)
  window: 30d rolling
  boundary: edge ingress (user-facing)

SLI: latency = count(duration < 300ms) / count(total)
  window: 30d rolling
  percentile model: threshold-based (not p99 directly) — easier error budget math
  boundary: edge ingress
```

Per resource (USE):

```
SLI: CPU_saturation = count(runq_latency_ms > 10) / count(samples)
SLI: queue_saturation = count(queue_depth > threshold) / count(samples)
SLI: disk_errors = rate(disk_error_events)
```

## Anti-Patterns

- Setting SLOs before running `golden` — ends up measuring whatever the old dashboard exposed.
- Measuring AVERAGE latency — averages hide tail behavior; always histogram.
- Measuring errors only as HTTP 5xx — 200-with-wrong-body and 4xx-policy-failures are user-visible failures too.
- Measuring latency across success AND failure combined — fast errors drag the distribution down and hide real slowness.
- Applying RED to a cache or broker — use USE; the "request" abstraction doesn't fit.
- Applying USE to an HTTP service without also applying RED — you see the resource is fine but miss that users are timing out.
- Extracting SLIs from component internals (DB query time) rather than system boundaries (user-facing endpoint).

## Output Shape

A `golden` deliverable is a table of SLI candidates, one row per (service × signal), ready to feed into `slo`:

| Service | Boundary | Signal | Method | SLI expression | Notes |
|---------|----------|--------|--------|----------------|-------|
| checkout-api | edge ingress | Availability | RED | `success / total` | excludes 4xx client errors |
| checkout-api | edge ingress | Latency | RED | `count(d<300ms)/total` | 300ms threshold from UX research |
| checkout-api | edge ingress | Traffic | RED | `rate(total)` | capacity-plan input |
| postgres-primary | resource | Saturation | USE | `connection_pool_saturation` | feeds auto-scaling |
| redis-cache | resource | Saturation | USE | `memory_pressure + evictions` | feeds cache-sizing |

## References

- Google SRE book, Ch. 6, "Monitoring Distributed Systems" — Golden Signals.
- Tom Wilkie, "The RED Method" (Weaveworks, 2017) — request-driven services.
- Brendan Gregg, "The USE Method" (brendangregg.com) — resource-driven components.

## Cross-Links

- `slo` — consumes this SLI candidate list to set targets and error budgets.
- `alerts` — burn-rate alerts are defined on the SLIs picked here.
- `dashboard` — RED and USE panels visualize these signals.
- `capacity` — Traffic and Saturation signals feed the load model.
