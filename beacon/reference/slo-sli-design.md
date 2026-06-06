# SLO/SLI Design, Error Budgets & Governance

> SLI types, SLO templates, error budget calculation, burn rate alerts, anti-patterns, policies, maturity model

---

## SLI (Service Level Indicator) Types

| SLI Type | Formula | Use Case |
|----------|---------|----------|
| **Availability** | Successful requests / Total requests | API uptime |
| **Latency** | Requests < threshold / Total requests | Response time |
| **Throughput** | Processed events / Expected events | Data pipeline |
| **Correctness** | Correct responses / Total responses | Data accuracy |
| **Freshness** | Data updated within window / Total data | Cache/replication |

### SLI Specification Template

```yaml
sli:
  name: "api-availability"
  description: "Proportion of successful HTTP requests"
  type: availability
  good_events: "http_status < 500"
  total_events: "all HTTP requests"
  measurement:
    source: prometheus
    query: |
      sum(rate(http_requests_total{status!~"5.."}[5m]))
      /
      sum(rate(http_requests_total[5m]))
  exclusions:
    - "health check endpoints"
    - "internal monitoring traffic"
```

---

## SLO Templates

### Tiered SLO Framework

| Tier | Availability | Latency (p99) | Error Budget/month |
|------|-------------|---------------|-------------------|
| **Critical** (auth, payments) | 99.95% | 200ms | 21.6 min |
| **Core** (main features) | 99.9% | 500ms | 43.2 min |
| **Standard** (dashboards) | 99.5% | 1000ms | 3.6 hrs |
| **Best-effort** (batch jobs) | 99.0% | 5000ms | 7.2 hrs |

### SLO Document Template

```yaml
slo:
  service: "payment-api"
  tier: critical
  owner: "payments-team"
  objectives:
    - sli: availability
      target: 99.95
      window: 30d
      rolling: true
    - sli: latency
      target: 99.0
      threshold: 200ms
      percentile: p99
      window: 30d
  consequences:
    budget_exhausted:
      - "Freeze non-critical deployments"
      - "Redirect engineering to reliability"
    budget_below_25:
      - "Alert on-call lead"
      - "Increase deployment scrutiny"
```

---

## Error Budget Calculation

```
Error Budget = 1 - SLO Target

Example (99.9% SLO over 30 days):
  Budget = 1 - 0.999 = 0.001 = 0.1%
  Time budget = 30 days x 24h x 60m x 0.001 = 43.2 minutes
  Request budget = 1,000,000 requests x 0.001 = 1,000 failed requests allowed

Burn Rate:
  burn_rate = actual_error_rate / allowed_error_rate
  burn_rate 1.0 = budget exhausted in exactly the SLO window
  burn_rate 14.4 = budget exhausted in ~2 days (Critical)

Remaining budget:
  consumed = actual_bad_events / total_events
  remaining = error_budget - consumed
  remaining_pct = remaining / error_budget x 100
```

---

## Burn Rate Alerts (Multi-Window)

| Alert | Burn Rate | Long Window | Short Window | Budget Consumed |
|-------|-----------|-------------|--------------|-----------------|
| **Page (critical)** | 14.4x | 1h | 5min | 2% in 1h |
| **Page (urgent)** | 6x | 6h | 30min | 5% in 6h |
| **Ticket (warning)** | 3x | 1d | 2h | 10% in 1d |
| **Ticket (low)** | 1x | 3d | 6h | 10% in 3d |

```yaml
# Prometheus alerting rules
groups:
  - name: slo-burn-rate
    rules:
      - alert: HighBurnRate_Critical
        expr: |
          (
            sum(rate(http_errors_total[1h])) / sum(rate(http_requests_total[1h]))
          ) > (14.4 * 0.001)
          AND
          (
            sum(rate(http_errors_total[5m])) / sum(rate(http_requests_total[5m]))
          ) > (14.4 * 0.001)
        labels:
          severity: critical
        annotations:
          summary: "High burn rate: 2% budget consumed in 1 hour"

      - alert: HighBurnRate_Warning
        expr: |
          (
            sum(rate(http_errors_total[6h])) / sum(rate(http_requests_total[6h]))
          ) > (6 * 0.001)
          AND
          (
            sum(rate(http_errors_total[30m])) / sum(rate(http_requests_total[30m]))
          ) > (6 * 0.001)
        labels:
          severity: warning
```

---

## Error Budget Policy

```
Green (budget remaining > 50%):
  - Normal feature development
  - Risky deployments allowed
  - Encourage experimentation

Yellow (budget remaining 25-50%):
  - Team analysis meeting
  - Low-risk deploys only
  - Pause high-risk changes
  - Prioritize reliability tasks

Red (budget remaining < 25%):
  - Freeze feature development
  - All resources on reliability
  - Release freeze (except emergency patches)
  - Maintain until budget recovers

Policy governance:
  - Designate freeze authority explicitly
  - VP/Director escalation path
  - If policy feels punitive -> SLO is too tight
  - If degradation occurs before freeze -> SLO is too loose
```

---

## SLO Anti-Patterns

| # | Anti-Pattern | Problem | Mitigation |
|---|-------------|---------|------------|
| **SA-01** | **100% target** | No deploys, patches, or scaling possible | Set realistic targets (<=99.9%) |
| **SA-02** | **Historical performance as SLO** | Heroic effort becomes baseline | Derive from user experience requirements |
| **SA-03** | **Availability-only focus** | Misses latency, freshness issues | Multi-dimensional SLIs (availability + latency + correctness) |
| **SA-04** | **Month-end budget check** | Too late to react to rapid consumption | Burn rate alerts for real-time monitoring |
| **SA-05** | **Ignoring external dependencies** | Uncontrollable SLO violations | Dependency chain analysis, factor in dependency SLAs |
| **SA-06** | **Ignoring traffic patterns** | Budget burns fast during peaks | Consider time-based / seasonal SLOs |
| **SA-07** | **No organizational alignment** | Priority mismatch with PM/leadership | SLO = business metric, shared across organization |
| **SA-08** | **SLO without policy** | Violations trigger no action ("toothless SLO") | Explicit error budget policy with enforcement |

### Metrics Sprawl Prevention

Unchecked metric creation increases noise, buries signal, and inflates costs. Countermeasures:
- **Metric owner system**: every metric has a designated owner
- **Quarterly audit**: review unused metrics, remove those with no SLO linkage
- **Purpose-driven collection**: SLO -> SLI -> required metrics (backtrack)

---

## SLO Maturity Model

| Level | State | Characteristics |
|-------|-------|----------------|
| 1 | SLIs defined, no SLO | Metrics exist but no targets |
| 2 | SLOs set, manual monitoring | Targets set, checked manually |
| 3 | Burn rate alerts, budget policy | Real-time monitoring, automated response |
| 4 | SLO-driven development | Budget consumption drives priority decisions |
| 5 | Auto-adaptive SLOs | Targets adapt to traffic patterns and seasonality |

---

## SLO Review Cadence

| Activity | Frequency | Participants |
|----------|-----------|-------------|
| **Error budget check** | Daily (automated) | On-call |
| **SLO dashboard review** | Weekly | Team lead |
| **SLO target review** | Quarterly | Engineering + Product |
| **SLO creation/retirement** | As needed | Architecture review |

### Quarterly Review Checklist

```markdown
- [ ] Are SLOs still aligned with user expectations?
- [ ] Were error budgets exhausted? Why?
- [ ] Are SLIs still measuring the right things?
- [ ] Should targets be tightened or relaxed?
- [ ] Are any SLOs consistently over-met (wasting budget)?
- [ ] New services that need SLOs?
- [ ] Retired services whose SLOs should be removed?
- [ ] Unused metrics identified and removed?
```

**Source:** [Google SRE: Implementing SLOs](https://sre.google/workbook/implementing-slos/) · [Google SRE: Error Budget Policy](https://sre.google/workbook/error-budget-policy/) · [Netdata: Error Budget Policies](https://www.netdata.cloud/academy/designing-error-budget-policies/) · [Nobl9: Complete Guide to Error Budgets](https://www.nobl9.com/resources/a-complete-guide-to-error-budgets-setting-up-slos-slis-and-slas-to-maintain-reliability)

---

## SLO-as-Code

### OpenSLO Specification

[OpenSLO](https://openslo.com/) is an open specification for defining SLOs as declarative YAML, enabling GitOps-driven SLO management.

```yaml
# openslo/payment-service.yaml
apiVersion: openslo/v1
kind: SLO
metadata:
  name: payment-availability
  displayName: "Payment Service Availability"
spec:
  service: payment-service
  description: "Proportion of successful payment requests"
  indicator:
    metadata:
      name: payment-success-rate
    spec:
      ratioMetric:
        counter: true
        good:
          metricSource:
            type: Prometheus
            spec:
              query: |
                sum(rate(http_requests_total{
                  job="payment-service",
                  status!~"5.."
                }[{{window}}]))
        total:
          metricSource:
            type: Prometheus
            spec:
              query: |
                sum(rate(http_requests_total{
                  job="payment-service"
                }[{{window}}]))
  objectives:
    - displayName: "Monthly availability"
      target: 0.999
      timeWindow:
        - duration: 1M
          isRolling: false
  alertPolicies:
    - payment-burn-rate-critical
    - payment-burn-rate-warning
```

### Sloth — SLO-as-Code Generator

[Sloth](https://sloth.dev/) generates Multi-Window Multi-Burn (MWMB) Prometheus alert rules from SLO definitions.

#### CRD Mode (Kubernetes)

```yaml
# sloth-slo.yaml — applied via kubectl / ArgoCD
apiVersion: sloth.slok.dev/v1
kind: PrometheusServiceLevel
metadata:
  name: payment-service-slos
  namespace: monitoring
spec:
  service: payment-service
  slos:
    - name: availability
      objective: 99.9
      description: "Payment service availability SLO"
      sli:
        events:
          error_query: |
            sum(rate(http_requests_total{
              job="payment-service", status=~"5.."
            }[{{window}}]))
          total_query: |
            sum(rate(http_requests_total{
              job="payment-service"
            }[{{window}}]))
      alerting:
        name: PaymentServiceAvailability
        page_alert:
          labels:
            severity: critical
            team: payments
        ticket_alert:
          labels:
            severity: warning
            team: payments
```

Sloth auto-generates two MWMB alert rules per SLO:

| Alert | Window pair | Burn rate | When to fire |
|-------|-------------|-----------|--------------|
| Page (critical) | 1h + 5m | 14× | 2% budget consumed in 1h |
| Ticket (warning) | 6h + 30m | 6× | 5% budget consumed in 6h |
| Ticket (low) | 3d + 6h | 3× | 10% budget consumed in 3d |

#### CLI Mode (CI validation)

```bash
# Validate and generate rules during CI
sloth validate --input slos/
sloth generate --input slos/ --output prometheus-rules/

# Run in Docker for portability
docker run -v $(pwd):/data ghcr.io/slok/sloth:latest \
  generate --input /data/slos/ --output /data/rules/
```

### GitOps Workflow for SLOs

```
1. Engineer creates/updates SLO YAML in slos/ directory
2. PR opened → CI pipeline runs:
   a. sloth validate (schema validation)
   b. sloth generate (preview generated rules)
   c. promtool check rules (Prometheus rule syntax)
3. PR review → merge to main
4. ArgoCD detects change → applies PrometheusServiceLevel CRD
5. Sloth controller generates Prometheus recording/alert rules
6. Alertmanager picks up new rules
7. Grafana SLO dashboard auto-refreshes (if using dynamic variables)
```

### Kubernetes SLO Operator Configuration

```yaml
# Sloth controller deployment (helm values)
sloth:
  controller:
    workers: 5
    resyncPeriod: 30s
  # Inject common labels into all generated rules
  commonLabels:
    team: "{{ .Metadata.Labels.team }}"
    environment: production
  # Disable default Sloth dashboards (use custom ones)
  disableDefaultDashboards: false
  grafana:
    dashboardsEnabled: true
    datasource: Prometheus
```
