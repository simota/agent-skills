# Platform Engineering Observability

> IDP observability architecture, Backstage SLO integration, Service Catalog, Golden Path design, Developer Experience metrics, Platform Maturity Model

---

## 1. IDP Observability Architecture (Paved Road Pattern)

An Internal Developer Platform (IDP) should provide "paved roads" — standardized, opinionated observability paths that developers follow by default.

### Three-Layer Architecture

```
Layer 3: PLATFORM PORTAL (Backstage / custom IDP UI)
  ├── Service health scores (SLO scorecards)
  ├── Ownership mapping (who owns what)
  ├── Tech radar (deprecation signals)
  └── Self-service SLO creation wizard

Layer 2: OBSERVABILITY PLATFORM
  ├── OTel Collector fleet (standardized pipelines)
  ├── Prometheus + Thanos / Grafana Mimir (metrics)
  ├── Grafana Tempo / Jaeger (traces)
  ├── Loki / OpenSearch (logs)
  └── Alertmanager → PagerDuty / Opsgenie

Layer 1: GOLDEN PATH INSTRUMENTATION
  ├── OTel SDK auto-instrumentation (via init containers or sidecars)
  ├── Standard Helm chart with pre-wired telemetry
  └── Service template with instrumentation included
```

### Paved Road Principles

| Principle | Description |
|-----------|-------------|
| **Opt-out, not opt-in** | Instrumentation is included by default in service templates |
| **Convention over configuration** | Standard attribute names, metric names, dashboard layouts |
| **Self-service with guardrails** | Developers can extend but not bypass core requirements |
| **Visibility into platform itself** | Platform team measures its own reliability (IDP SLOs) |

---

## 2. Backstage + SLO Integration

### ServiceEntity SLO Scorecard

Extend the Backstage `catalog-info.yaml` to embed SLO metadata:

```yaml
# catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  annotations:
    # SLO scorecard annotation
    beacon.io/slo-scorecard: |
      slos:
        - name: availability
          target: 0.999
          current: 0.9994
          status: healthy
          error_budget_remaining: 0.62
        - name: latency-p95
          target: 0.95
          threshold_ms: 200
          current: 0.972
          status: healthy
          error_budget_remaining: 0.44
    # Link to Grafana SLO dashboard
    grafana/dashboard-url: "https://grafana.internal/d/slo-payment-service"
spec:
  type: service
  lifecycle: production
  owner: team-payments
```

### Backstage SLO Plugin Integration

```typescript
// SLO data provider for Backstage plugin
export const sloDataProvider: SLODataProvider = {
  async getSLOStatus(entityRef: string): Promise<SLOStatus[]> {
    const response = await fetch(
      `${config.backendUrl}/api/slos/${entityRef}`
    );
    return response.json();
  },
};
```

---

## 3. Service Catalog → SLO Auto-generation

### Metadata → SLO Definition Mapping

When a new service is registered in the Service Catalog, SLOs can be auto-generated based on metadata:

```yaml
# SLO generation rules (stored in platform config)
slo_templates:
  - condition:
      type: service
      lifecycle: production
      tier: critical
    generate:
      - name: availability
        sli_type: availability
        target: 0.999
        window: 30d
      - name: latency-p95
        sli_type: latency
        target: 0.95
        threshold_ms: 200
        window: 30d

  - condition:
      type: service
      lifecycle: production
      tier: standard
    generate:
      - name: availability
        sli_type: availability
        target: 0.995
        window: 30d
```

### GitOps SLO Generation Workflow

```
Service registered in Catalog
         ↓
Catalog webhook triggers SLO generator
         ↓
Generator reads service tier from metadata
         ↓
Renders SLO YAML from template
         ↓
Opens PR to infrastructure/slos/ repo
         ↓
PR review → merge → ArgoCD applies SLO CRDs
         ↓
Grafana SLO dashboard auto-provisioned
```

---

## 4. Golden Path Design

A Golden Path provides a complete, pre-configured observability setup for new services.

### Golden Path Components

| Component | What it provides |
|-----------|-----------------|
| **Service template** (Cookiecutter/Backstage scaffolder) | Pre-wired OTel SDK, health check endpoints, structured logging |
| **Helm chart template** | OTel sidecar/init container, resource annotations for Prometheus scraping |
| **Standard dashboard template** | Pre-built Grafana dashboard with RED method panels, parameterized by service name |
| **SLO template** | Default SLO definitions based on service tier |
| **Runbook template** | Pre-filled runbook with standard investigation steps |
| **Alert template** | Standard alert rules wired to runbook |

### Golden Path OTel Init Container (Kubernetes)

```yaml
# Helm chart snippet — auto-inject OTel agent
initContainers:
  - name: otel-agent-init
    image: ghcr.io/platform/otel-agent-init:latest
    env:
      - name: OTEL_SERVICE_NAME
        valueFrom:
          fieldRef:
            fieldPath: metadata.labels['app.kubernetes.io/name']
      - name: OTEL_EXPORTER_OTLP_ENDPOINT
        value: "http://otel-collector.observability.svc:4317"
    volumeMounts:
      - name: otel-agent
        mountPath: /otel-agent
```

### Standard SLO Configuration Template

```yaml
# templates/slo.yaml — included in Golden Path
apiVersion: sloth.slok.dev/v1
kind: PrometheusServiceLevel
metadata:
  name: {{ .Values.serviceName }}-slos
  namespace: {{ .Release.Namespace }}
spec:
  service: {{ .Values.serviceName }}
  slos:
    - name: availability
      objective: {{ .Values.slo.availability | default 99.5 }}
      description: "{{ .Values.serviceName }} availability SLO"
      sli:
        events:
          error_query: |
            sum(rate(http_requests_total{
              job="{{ .Values.serviceName }}",
              status=~"5.."
            }[{{"{{"}}window{{"}}"}}]))
          total_query: |
            sum(rate(http_requests_total{
              job="{{ .Values.serviceName }}"
            }[{{"{{"}}window{{"}}"}}]))
      alerting:
        name: {{ .Values.serviceName | title }}AvailabilitySLO
        page_alert:
          labels:
            severity: critical
        ticket_alert:
          labels:
            severity: warning
```

---

## 5. Developer Experience Metrics

Track the health of the platform itself through DX (Developer Experience) metrics.

### Core DX Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| **Time-to-first-deploy** | Minutes from `git init` to first successful production deploy (following Golden Path) | < 30 min |
| **Onboarding time** | Days for a new engineer to make their first production contribution | < 5 days |
| **Golden Path adoption rate** | % of services using the standard Helm chart template | > 80% |
| **Self-service success rate** | % of service creation requests completed without platform team intervention | > 90% |
| **P95 CI pipeline duration** | 95th percentile of CI/CD pipeline run time | < 10 min |
| **Deployment frequency** | Deploys per team per week | Trending up |
| **Platform NPS** | Developer satisfaction score (quarterly survey) | > 30 |
| **MTTR for IDP incidents** | Mean time to restore IDP services | < 1 hour |

### DORA Metrics Integration

The platform should surface DORA metrics per team/service:

```promql
# Deployment frequency (deploys/day per team)
increase(deployments_total[1d])

# Change failure rate
sum(rate(deployments_total{status="failed"}[7d]))
/ sum(rate(deployments_total[7d]))

# Mean time to restore (MTTR)
avg_over_time(incident_duration_seconds[30d])
```

---

## 6. Platform Maturity Model (L1–L4)

Assess and plan platform observability evolution across four maturity levels.

| Level | Name | Observability Capabilities | Key Signals |
|-------|------|---------------------------|-------------|
| **L1** | Reactive | Manual metrics/logs, no SLOs, ad-hoc dashboards | Alerts go off, team scrambles |
| **L2** | Structured | Basic SLOs defined, standard dashboards, alerting in place | Error budgets tracked manually |
| **L3** | Proactive | Automated SLO generation, Golden Path adopted, DX metrics tracked | Error budget drives prioritization |
| **L4** | Adaptive | AI-assisted anomaly detection, predictive capacity, auto-remediation, feedback loops | Platform evolves based on data |

### Maturity Assessment Checklist

#### L1 → L2 (Structured)

- [ ] SLOs defined for all production services (availability + latency minimum)
- [ ] Error budgets calculated and visible
- [ ] Standard dashboard template adopted by > 50% of teams
- [ ] Alert runbooks exist for all P1 alerts
- [ ] On-call rotation established with defined escalation path

#### L2 → L3 (Proactive)

- [ ] Golden Path adopted by > 80% of new services
- [ ] SLO auto-generation from Service Catalog live
- [ ] Error budget policy drives sprint prioritization
- [ ] DX metrics tracked (TTD, onboarding time, adoption rate)
- [ ] Platform team has its own SLOs

#### L3 → L4 (Adaptive)

- [ ] Anomaly detection on key SLIs (ML-based or statistical)
- [ ] Predictive capacity models running in production
- [ ] Auto-remediation runbooks executing for known failure patterns (→ Mend)
- [ ] DX feedback loop: survey → roadmap → measure improvement
- [ ] Observability cost optimization automated (adaptive sampling)

---

## 7. IDP SLOs (Platform Eating Its Own Cooking)

The platform team must define and maintain SLOs for the IDP itself.

| SLO | Target | SLI Query |
|-----|--------|-----------|
| Backstage availability | 99.5% | `avg_over_time(up{job="backstage"}[5m])` |
| Service registration latency | P95 < 5s | `histogram_quantile(0.95, catalog_request_duration_seconds_bucket)` |
| CI pipeline success rate | > 95% | `sum(rate(pipeline_runs_total{status="success"}[1h])) / sum(rate(pipeline_runs_total[1h]))` |
| OTel Collector drop rate | < 0.1% | `otelcol_processor_dropped_spans_total / otelcol_receiver_accepted_spans_total` |
| Secret distribution latency | P95 < 10s | `histogram_quantile(0.95, vault_secret_read_duration_seconds_bucket)` |

---

**Source:** [Backstage Annotations](https://backstage.io/docs/features/software-catalog/well-known-annotations) · [DORA Research](https://dora.dev/) · [Team Topologies — Platform Teams](https://teamtopologies.com/key-concepts) · [Humanitec: IDP Maturity Model](https://humanitec.com/blog/internal-developer-platform-maturity-model)
