# Dashboard Design Reference

RED/USE methods and Grafana dashboard-as-code reference.

---

## Dashboard Frameworks

### RED Method (Request-driven services)

| Signal | Metric | Query Example |
|--------|--------|--------------|
| **Rate** | Requests per second | `sum(rate(http_requests_total[5m]))` |
| **Errors** | Error rate (%) | `sum(rate(http_errors_total[5m])) / sum(rate(http_requests_total[5m]))` |
| **Duration** | Latency percentiles | `histogram_quantile(0.99, rate(http_duration_seconds_bucket[5m]))` |

### USE Method (Resource-oriented)

| Signal | Resource | Metric |
|--------|----------|--------|
| **Utilization** | CPU | `rate(process_cpu_seconds_total[5m])` |
| **Utilization** | Memory | `process_resident_memory_bytes / machine_memory_bytes` |
| **Saturation** | CPU | `rate(node_cpu_seconds_total{mode="iowait"}[5m])` |
| **Saturation** | Memory | `node_memory_SwapFree_bytes < 0.1 * node_memory_SwapTotal_bytes` |
| **Errors** | Disk | `rate(node_disk_io_errors_total[5m])` |

### Four Golden Signals (Google SRE)

| Signal | What | Why |
|--------|------|-----|
| **Latency** | Request duration | User experience |
| **Traffic** | Request volume | Capacity planning |
| **Errors** | Failure rate | Correctness |
| **Saturation** | Resource fullness | Headroom |

### Profiles — The Fourth OpenTelemetry Signal (2026)

OpenTelemetry **Profiles** reached Alpha in March 2026, joining logs, metrics, and traces as a first-class signal. Dashboards in 2026 should reserve a panel for **continuous CPU / allocation profiles** anchored to the same time window as the RED panels above — the profile answers "*where* did the latency or saturation come from in code", which traces and metrics together cannot.

Recommended wiring:

| Layer | Tool | What it produces |
|-------|------|--------------------|
| eBPF agent | **OpenTelemetry eBPF Profiler** (OBI) | system-wide stack samples, zero code change required |
| Ingest / storage | **Grafana Pyroscope 2.0** (rearchitected May 2026) | OTLP-compatible profile store with reduced storage cost and faster query at scale |
| Correlation | OTel Collector with profile-trace exemplars | join a span to the profile sample taken at the same instant |

A "Service Detail" dashboard should hand the on-call engineer a **flame graph that auto-scopes to the failing span** when they click an outlier on the latency panel. Without that integration, profiling exists but does not change incident response time.

---

## Dashboard Hierarchy

```
Level 1: Executive Overview (SLO status, budget remaining)
    └── Level 2: Service Overview (RED per service)
        └── Level 3: Service Detail (endpoints, dependencies)
            └── Level 4: Debug (traces, logs, resource detail)
```

### Dashboard Types

| Type | Audience | Refresh | Content |
|------|----------|---------|---------|
| **SLO Overview** | Leadership | 5min | SLO status, budget burn |
| **Service Health** | On-call | 30s | RED metrics, dependencies |
| **Deployment** | Engineers | 10s | Canary metrics, rollback triggers |
| **Capacity** | Platform team | 1h | Resource usage, projections |
| **Business** | Product | 5min | Conversion, revenue, engagement |

---

## Grafana Dashboard-as-Code

### Jsonnet Pattern

```jsonnet
local grafana = import 'grafonnet/grafana.libsonnet';
local dashboard = grafana.dashboard;
local row = grafana.row;
local prometheus = grafana.prometheus;
local graphPanel = grafana.graphPanel;

local serviceDashboard(service) =
  dashboard.new(
    title='%s Service Overview' % service,
    tags=['generated', 'service'],
    refresh='30s',
    time_from='now-1h',
  )
  .addRow(
    row.new(title='RED Metrics')
    .addPanel(
      graphPanel.new(
        title='Request Rate',
        datasource='Prometheus',
      ).addTarget(
        prometheus.target(
          'sum(rate(http_requests_total{service="%s"}[5m]))' % service,
          legendFormat='{{method}} {{status_code}}',
        )
      )
    )
  );

{
  'payment-service.json': serviceDashboard('payment-service'),
  'user-service.json': serviceDashboard('user-service'),
}
```

### Terraform Provisioning

```hcl
resource "grafana_dashboard" "service_overview" {
  for_each = toset(var.services)

  config_json = templatefile("${path.module}/templates/service-dashboard.json.tpl", {
    service_name = each.key
    slo_target   = var.slo_targets[each.key]
  })

  folder = grafana_folder.services.id
}
```

---

## Panel Design Guidelines

| Guideline | Reason |
|-----------|--------|
| **Red = bad, green = good** | Universal understanding |
| **Left axis = primary metric** | Natural reading order |
| **Annotations for deploys** | Correlate changes with metrics |
| **SLO threshold lines** | Visual reference for targets |
| **Time range: 1h default** | Recent context without noise |
| **Max 4 panels per row** | Readability on standard screens |

### Common Panel Patterns

| Pattern | Visualization | Use |
|---------|--------------|-----|
| **Current value** | Stat / Gauge | SLO %, error rate |
| **Trend over time** | Time series | Request rate, latency |
| **Distribution** | Heatmap | Latency distribution |
| **Comparison** | Bar chart | Per-endpoint breakdown |
| **Status** | Status map | Service dependency health |
| **Threshold** | Time series + threshold | SLO target line |

---

## Dashboard Sprawl Prevention

```
Anti-patterns:
  x  L2-level detail in on-call dashboards (too much noise)
  x  Each team creating custom-format dashboards (no single source of truth)
  x  20+ panels per dashboard (cognitive overload)
  x  Graphs without context (unclear what "normal" looks like)

Countermeasures:
  - Enforce L0/L1/L2 hierarchy for all new dashboards
  - Use shared templates (Jsonnet/Terraform) for consistency
  - Require level designation (L0/L1/L2) at creation time
  - Max 8-12 panels per dashboard
  - Include "what is normal" annotations on every graph
  - Quarterly dashboard audit: remove unused, consolidate duplicates
```
