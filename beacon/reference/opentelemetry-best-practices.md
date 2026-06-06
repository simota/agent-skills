# OpenTelemetry Best Practices & Distributed Tracing

> Instrumentation strategy, semantic conventions, collector pipeline, sampling, tracing, telemetry correlation, GenAI observability, cost optimization

---

## 1. Instrumentation Strategy

| # | Practice | Description | Importance |
|---|---------|-------------|------------|
| **OT-01** | **Auto-first, Manual-second** | Start with auto-instrumentation for immediate visibility, then add manual spans for business-critical paths | Required |
| **OT-02** | **SDK initialization first** | Initialize OTel SDK before any application module imports | Required |
| **OT-03** | **Always close spans** | Use async/await + finally blocks to ensure spans are closed | Required |
| **OT-04** | **Add business attributes** | Enrich auto-generated spans with business context (customer_tier, order_value) | Recommended |
| **OT-05** | **Record errors and events** | Log state transitions and errors as span events | Recommended |

```
Initialization order (critical):
  // 1. Initialize OTel SDK first
  const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
  const provider = new NodeTracerProvider();
  provider.register();

  // 2. Then import application modules
  const express = require('express');
```

### Manual Span Creation

```python
@tracer.start_as_current_span("process_payment")
def process_payment(order_id: str, amount: float):
    span = trace.get_current_span()
    span.set_attribute("order.id", order_id)
    span.set_attribute("payment.amount", amount)
    span.set_attribute("payment.currency", "USD")

    try:
        result = charge_card(amount)
        span.set_attribute("payment.status", "success")
        span.set_status(StatusCode.OK)
        return result
    except PaymentError as e:
        span.set_status(StatusCode.ERROR, str(e))
        span.record_exception(e)
        raise
```

---

## 2. Semantic Conventions

### Standard Attributes (must follow)

```
HTTP:       http.method, http.status_code, http.route
DB:         db.system, db.statement, db.name
Messaging:  messaging.system, messaging.destination
RPC:        rpc.system, rpc.service, rpc.method
```

### Application-Specific Attributes

```
- Prefix: app.* for custom attributes
- Naming: snake_case consistently
- Examples: app.customer_tier, app.order_value, app.feature_flag
```

### Attribute Anti-Patterns

```
x  High-cardinality attributes (user_id) on all spans -> use traces not metrics
x  Duplicate attributes on parent/child spans
x  Mixing metric/log data into span attributes
x  Abbreviations (svc -> service)
```

---

## 3. Span Naming Conventions

| Layer | Format | Examples |
|-------|--------|---------|
| **HTTP server** | `HTTP {METHOD} {route}` | `HTTP GET /api/users/:id` |
| **HTTP client** | `HTTP {METHOD}` | `HTTP POST` |
| **Database** | `{db.system} {operation} {table}` | `postgresql SELECT orders` |
| **Message publish** | `{queue} publish` | `orders.created publish` |
| **Message consume** | `{queue} process` | `orders.created process` |
| **Business logic** | `{verb}_{noun}` | `validate_payment`, `calculate_tax` |
| **External service** | `{service}.{operation}` | `stripe.create_charge` |

---

## 4. Context Propagation

| Format | Header | Ecosystem |
|--------|--------|-----------|
| **W3C Trace Context** (recommended) | `traceparent`, `tracestate` | Standard |
| **B3** | `X-B3-TraceId`, `X-B3-SpanId` | Zipkin |
| **Jaeger** | `uber-trace-id` | Jaeger |

### Propagation Checklist

```markdown
- [ ] All HTTP clients inject trace context headers
- [ ] All HTTP servers extract trace context headers
- [ ] Message queues propagate trace context in headers/metadata
- [ ] Async workers link to parent span via context
- [ ] Batch jobs create new root spans with links to triggers
- [ ] Third-party API calls create client spans
```

### Baggage

- Use Baggage for cross-service context (customer_id, tenant_id)
- Caution: Baggage propagates to all downstream services
- Never include sensitive information in Baggage

---

## 5. Collector Deployment Patterns

| Pattern | Configuration | Pros | Cons | Scale |
|---------|--------------|------|------|-------|
| **Agent** | Sidecar per app | Network minimal, app isolation | Config management distributed | Small |
| **Gateway** | Central server | Centralized config, routing | SPOF risk | Medium |
| **Hierarchical** | Agent + Gateway | Optimal reliability/management balance | Complexity | Large (recommended) |

### Collector Configuration

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  memory_limiter:        # OOM prevention (MUST be first)
    check_interval: 1s
    limit_mib: 1000
  batch:                 # Network efficiency
    send_batch_size: 10000
    timeout: 10s

exporters:
  otlp:
    endpoint: observability-backend:4317

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]  # memory_limiter always first
      exporters: [otlp]
```

### Processor Ordering (Critical)

1. **memory_limiter** (prevent crashes)
2. **enrichment** (k8sattributes, resource)
3. **filter/transform** (PII redaction, filtering)
4. **batch** (efficient delivery, always last)

### PII/PHI Filtering

```yaml
processors:
  filter:
    spans:
      include:
        match_type: regexp
        attributes:
          - key: db.statement
            value: "(?i)(?:password|passwd)\\s*=\\s*[^\\s,;]+"
      actions:
        - key: db.statement
          action: update
          value: "REDACTED"
```

### Operational Requirements

- Minimum 4GB node memory for graceful shutdown
- Version-lock Operator, Collector, and Target Allocator together
- Use `nodeAffinity` to prevent deployment on small nodes
- Monitor: `otelcol_receiver_refused_metric_points_total` (non-zero = data loss)

---

## 6. Sampling Strategies

| Strategy | Decision Point | Pros | Cons | Use |
|----------|---------------|------|------|-----|
| **Head Sampling** | Trace start | Simple, low overhead | Misses error traces | Dev environments |
| **Tail Sampling** | Trace completion | Intelligent decisions | Requires buffering | Production (recommended) |
| **Probabilistic** | Random % | Predictable cost | Error miss risk | High traffic |
| **Rate Limiting** | Time-based cap | Spike control | Important trace loss risk | Burst protection |

### Recommended: Composite Sampling Strategy

```yaml
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors
        type: status_code
        status_code: { status_codes: [ERROR] }     # 100% error retention
      - name: slow-requests
        type: latency
        latency: { threshold_ms: 2000 }
      - name: critical-endpoints
        type: string_attribute
        string_attribute:
          key: http.route
          values: ["/api/payments", "/api/auth"]
      - name: baseline
        type: probabilistic
        probabilistic: { sampling_percentage: 5 }   # 5% normal traffic
    decision_cache_size: 50000
```

### Metrics Accuracy Preservation

- Generate metrics BEFORE sampling (spanmetrics processor)
- Use `spanmetrics` processor for automatic RED metric generation
- Use `servicegraph` processor for automatic dependency map generation

```yaml
processors:
  spanmetrics:
    metrics_exporter: prometheus
    dimensions:
      - name: service.name
      - name: http.method
      - name: http.status_code
```

---

## 7. Telemetry Correlation (Three Pillars)

```
Log-Trace correlation:
  - Inject trace_id / span_id into logs automatically
  - Use structured logging (JSON)
  - ERROR/WARN logs must also be recorded as span events

Trace -> Metrics conversion:
  - spanmetrics processor for RED metrics
  - servicegraph processor for dependency maps

Performance tuning:
  BatchSpanProcessor:
    maxQueueSize: 2048
    maxExportBatchSize: 512
    scheduledDelayMillis: 5000
    exportTimeoutMillis: 30000
  - Enable gzip compression (bandwidth reduction)
  - Circuit breaker (telemetry must not affect availability)
```

---

## 8. Trace Analysis Patterns

| Pattern | What to Look For | Action |
|---------|-----------------|--------|
| **Long spans** | Single span > SLO threshold | Optimize or decompose |
| **Wide traces** | Fan-out > 50 spans | Check N+1 queries |
| **Deep traces** | Depth > 10 levels | Simplify call chain |
| **Orphan spans** | Missing parent spans | Fix context propagation |
| **Gap spans** | Time gaps between child spans | Check queuing/scheduling |

---

## 9. Cardinality Management

```
Cardinality explosion example:
  http_requests_total{method, path, status, user_id, client_ip}
  -> method(5) x path(100) x status(10) x user_id(100K) x client_ip(50K)
  -> 2.5 trillion unique time series -> system collapse

Detection:
  1. Index size spikes (RAM/disk monitoring)
  2. remote_write ingestion delays
  3. Aggregation query (sum, avg) latency degradation
  4. Observability platform cost spikes

Control strategy:
  Tier 1: Per-service cardinality limits
    - Business-critical metrics: higher thresholds
    - Infrastructure metrics: strict limits

  Tier 2: Tiered retention policies
    - High resolution (raw data): 24-48 hours
    - Medium resolution (1min aggregation): 30 days
    - Low resolution (1hr aggregation): 13+ months

  Tier 3: Adaptive downsampling
    - Keep high-fidelity data at edge (local)
    - Selective downsampling at central aggregation
    - Prefer automation over manual recording rules
```

---

## 10. Cost Optimization

```
Key cost levers (most to least effective):
  1. Pipeline-level filtering BEFORE storage (Collector processors)
  2. Intelligent sampling (tail-based, composite)
  3. Tiered retention (raw -> aggregated -> archived)
  4. Per-node Target Allocator (prevents 20-40x metric duplication)
  5. Cardinality limits per service

Results benchmark (CNCF case study):
  - 72% cost reduction vs previous vendor
  - 100% APM trace coverage (was 5% sampling)
  - Enabled by: OTel Collector + open-source backends (Loki, Tempo, Mimir)

Observability budget framework:
  - Set per-team telemetry budget (GB/day or cost/month)
  - Monitor telemetry volume per service
  - Alert on budget overruns
  - Quarterly review: optimize top-5 cost contributors

Tool sprawl prevention:
  - Standardize on OTel as the single collection layer
  - Consolidate to single backend per signal type
  - Avoid Prometheus + Datadog + New Relic + custom tools in parallel
```

---

## 11. GenAI / Agent Observability

```
OTel GenAI Semantic Conventions (v1.37+):
  Standard attributes:
    gen_ai.request.model         # Model identifier
    gen_ai.usage.input_tokens    # Token usage
    gen_ai.usage.output_tokens
    gen_ai.provider.name         # Provider (openai, anthropic, etc.)
    gen_ai.request.temperature   # Model parameters
    gen_ai.request.max_tokens

  Agent-specific:
    gen_ai.agent.name            # Agent identifier
    gen_ai.agent.description
    gen_ai.tool.name             # Tool calls
    gen_ai.tool.description

Instrumentation approaches:
  Option 1: Baked-in (framework embeds OTel)
    + Simplified adoption, feature-release control
    - Framework bloat, version lag

  Option 2: External OTel libraries (recommended)
    + Decoupled, community-maintained
    - Fragmentation risk if incompatible packages

Key metrics for LLM observability:
  - Token usage per request/session
  - Latency per model call (time to first token, total)
  - Error rates by model/provider
  - Cost per request (tokens x price)
  - Tool call success/failure rates
```

---

## 12. Beacon Integration

```
Usage by mode:
  1. DESIGN: OTel instrumentation strategy, collector pipeline design
  2. SPECIFY: Collector pipeline specs, sampling configuration
  3. MEASURE: Sampling strategy optimization, cardinality monitoring
  4. Periodic review: Semantic Conventions compliance, cost optimization

Quality gates:
  - OTel SDK initialization is first in app startup (OT-02)
  - memory_limiter processor is first in pipeline
  - Error traces retained at 100%
  - Logs inject trace_id (correlation enabled)
  - PII/PHI filtering in Collector
  - Semantic Conventions compliance in attribute naming
  - New metric addition requires cardinality estimate
  - Telemetry budget per team/service defined
```

**Source:** [OTel Semantic Conventions v1.40](https://opentelemetry.io/docs/specs/semconv/) · [Better Stack: OTel Best Practices](https://betterstack.com/community/guides/observability/opentelemetry-best-practices/) · [CNCF: Cost-Effective OTel](https://www.cncf.io/blog/2025/12/16/how-to-build-a-cost-effective-observability-platform-with-opentelemetry/) · [Dash0: OTel Collector Guide](https://dash0.com/blog/opentelemetry-collector-guide) · [OTel: AI Agent Observability](https://opentelemetry.io/blog/2025/ai-agent-observability/) · [OTel GenAI SemConv](https://opentelemetry.io/docs/specs/semconv/gen-ai/) · [OTel Weaver](https://opentelemetry.io/blog/2025/otel-weaver/)

---

## 13. 2025 Ecosystem Updates

### OTel eBPF Profiler (Public Alpha)

The OpenTelemetry eBPF Profiler enables zero-instrumentation continuous profiling at the kernel level.

```
Status: Public Alpha (2025)
SIG participants: Grafana, Splunk, Odigos, Elastic

Key capabilities:
  - Language-agnostic: works with Go, Python, Java, Node.js, Rust, .NET without code changes
  - Low overhead: < 1% CPU impact via eBPF
  - Stack trace → OTel profiles → OTLP export
  - Correlate profiles with traces (via trace_id on profile frames)

Profile data format:
  - Follows OTel Profiles specification (experimental)
  - pprof-compatible export for Grafana Pyroscope

When to use:
  - CPU hotspot investigation without instrumentation
  - Memory allocation profiling in production
  - Correlate slow traces with profile data
```

### OTel Logs Stability Status

```
Logs Bridge API: STABLE (as of OTel v1.x)
  - Use for integrating existing logging frameworks (log4j, winston, etc.)
  - Bridges log records into OTel pipeline with trace correlation

Event API: EXPERIMENTAL
  - Use for structured event emission (e.g., user actions, state transitions)
  - Not yet stable; API may change

Recommendation:
  - Use Logs Bridge API in production for log → OTLP export
  - Use span events for in-span structured data (stable)
  - Avoid Event API in production until stable
```

### Collector Declarative Configuration Schema (RC3)

The OTel Collector is adopting a declarative configuration schema that replaces the current pipeline YAML.

```yaml
# New declarative config format (RC3, 2025)
# Replaces: receivers/processors/exporters/service.pipelines
receivers:
  otlp/grpc:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  # QueueBatcher replaces batch processor — combines queuing + batching
  queuebatcher/traces:
    max_size: 1000
    timeout: 5s

  memory_limiter:
    limit_mib: 512
    spike_limit_mib: 128

exporters:
  otlphttp/backend:
    endpoint: https://otel.backend.internal

# New: pipelines defined inline with connectors
pipelines:
  traces:
    receivers: [otlp/grpc]
    processors: [memory_limiter, queuebatcher/traces]
    exporters: [otlphttp/backend]
```

Key change: **QueueBatcher** replaces the `batch` processor and adds built-in retry queuing, reducing common pipeline configuration complexity.

### Adaptive Telemetry

Adaptive telemetry dynamically adjusts sampling rates based on observed error rates and latency SLOs.

```
Grafana Cloud Adaptive Metrics: 30-50% cost reduction observed in production

Strategy:
  1. High-value signals: always-on (errors, SLO violations, critical paths)
  2. Normal traffic: tail-based sampling (10-20%)
  3. Healthy, low-latency traffic: head-based sampling (1-5%)
  4. Metrics: adaptive scrape intervals (longer for stable metrics)

Grafana Adaptive Metrics rules example:
  # Drop high-cardinality metrics with low query frequency
  - match: {__name__=~"go_.*"}
    keep_labels: [job, instance]
    drop_if_unqueried_for: 7d
```

---

## 14. 4-Layer Cost Reduction Framework

### Layer 1: Generation (Reduce what you produce)

```
Techniques:
  - Remove unused instrumentation (audit with OTel Weaver)
  - Drop debug spans in production (environment-based filtering)
  - Use exemplars instead of 100% trace sampling
  - Instrument at service boundaries, not every function

Cardinality control:
  - Never use user IDs or request IDs as metric labels
  - Maximum 10 label combinations per metric
  - Alert when cardinality exceeds threshold

Cardinality detection query (Prometheus):
  # Find metrics with > 1000 unique label combinations
  count by (__name__) (
    count by (__name__, job, instance) ({__name__=~".+"})
  ) > 1000
```

### Layer 2: Transport (Reduce what you move)

```
Techniques:
  - Enable OTLP gzip compression (50-70% size reduction)
  - Batch spans (QueueBatcher: timeout=5s, max_size=1000)
  - Filter at Collector, not at backend (cheaper CPU)
  - Use tail-based sampling to drop healthy traces before export

Collector filter example:
  processors:
    filter/drop_healthy:
      error_mode: ignore
      traces:
        span:
          # Drop spans where no error AND duration < 100ms
          - 'status.code == STATUS_CODE_OK and duration < 100ms and not IsRootSpan()'
```

### Layer 3: Storage (Reduce what you keep)

```
Retention tiers (recommended):
  | Signal  | Hot (query-ready) | Warm (compressed) | Cold (archive) |
  |---------|-------------------|-------------------|----------------|
  | Metrics | 15 days           | 90 days           | 1 year         |
  | Traces  | 3 days            | 14 days           | 90 days        |
  | Logs    | 7 days            | 30 days           | 1 year         |

Aggregation:
  - Pre-aggregate high-cardinality metrics with recording rules
  - Store raw traces only for errors and SLO violations after hot tier
  - Use log sampling for INFO-level logs after hot tier
```

### Layer 4: Query (Reduce what you read)

```
Techniques:
  - Create recording rules for frequent, expensive queries
  - Use metric resolution (5m avg) for long-range dashboards
  - Avoid full-table log scans (use structured log fields)
  - Cache dashboard queries (Grafana: 30s-5m depending on panel)

Scrape interval optimization:
  | Metric type              | Recommended interval |
  |--------------------------|----------------------|
  | SLO error budget         | 15s                  |
  | Service RED metrics      | 15s                  |
  | Infrastructure (CPU/mem) | 30s                  |
  | Capacity planning        | 60s                  |
  | Business metrics         | 60s                  |
  | Build/deploy metrics     | 300s                 |
```
