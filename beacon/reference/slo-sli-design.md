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

## AI / LLM Service SLOs

`http_status < 500` is the wrong good-event definition for a system that can answer fast, cheaply, and wrongly.
A confidently fabricated answer returns `200`. Define the good event as a conjunction over the whole outcome:

```yaml
good_event:
  - request_accepted            # not rejected by admission control or quota
  - response_before_deadline    # end-to-end, client clock
  - schema_valid                # structured output parses and validates
  - task_quality_pass           # meets the quality floor for its slice
  - policy_compliant            # no unsupported claim, no prohibited behavior
  - no_unauthorized_data        # no cross-tenant or out-of-ACL content
```

### SLI layers

Do not force these into one composite availability number. Publish an outcome SLO upward and keep the
component SLIs for diagnosis.

| Layer | SLI | Notes |
|-------|-----|-------|
| **Service availability** | accepted / offered, dependency health, within rate limit | rejection is a failure, not an exclusion |
| **Latency** | end-to-end p95/p99, TTFT, inter-token stall | a stalled stream fails UX at an acceptable mean |
| **Quality** | task success, per-critical-slice success, abstention rate | slice floors are independent of the overall score |
| **Reliability** | timeout rate, retry amplification (`attempts/request`), duplicate side-effect actions | duplicate actions are silent in status codes |
| **Safety / Security** | policy violations, unauthorized tool actions, data exposure | its own budget; never nets out against latency wins |
| **Cost** | cost per successful task, budget overrun | a cheaper request that gets retried is not cheaper |

### Provisional vs confirmed quality SLI

Latency and schema resolve instantly; quality does not. Automated evaluators and proxy signals give a
**provisional** value in real time, and human-sampled labels **confirm** it days later. Publish both and mark
which is which. Never close an error budget on proxy values alone — and when the confirmed value contradicts
the provisional one, the evaluator itself is a suspect, not only the system.

### Separate budgets, one release policy

Keep latency, quality, and safety error budgets as distinct metrics — a latency win must not be allowed to
mathematically absorb a quality regression — but connect them to a **single** release policy. Model, prompt,
dataset, index, and runtime are typically changed by different teams; record every one of them in the same
release ledger so budget consumption can be attributed to the change that caused it. A critical safety or
security event halts releases regardless of remaining budget.

### Capacity SLO

Capacity shortfall surfaces as `429` or queue timeout. If latency is computed over accepted requests only,
shedding load *improves* the number. Bind `admission_rejection_rate` and `successful_task_rate` into the same
SLO so the two cannot be traded against each other unnoticed.

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

Canonical tier table (matches SKILL.md Core Contract — `alerting-strategy.md` points here for full detail):

| Alert | Burn Rate | Long Window | Short Window | Budget Consumed |
|-------|-----------|-------------|--------------|-----------------|
| **Fast burn (page)** | 14.4x | 1h | 5min | ~2% in 1h |
| **Medium burn (page)** | 6x | 6h | 30min | ~5% in 6h |
| **Slow burn (ticket)** | 3x | 3d | 6h | ~10% in 3d |
| **Baseline (trend)** | 1x | 30d | — | 100% at SLO window end |

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
  - VP/Cue escalation path
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
| **SA-09** | **`HTTP 200` as AI success** | A fast, cheap, fabricated answer counts as a good event | Conjunctive good event (schema + quality + policy + authorization) |
| **SA-10** | **Denominator laundering** | Rejects, timeouts, cancellations, and abstentions dropped from the denominator; shedding load improves the SLI | Keep them in the denominator; pair latency SLO with rejection rate. Classify each as good or bad on its own merits (SA-11) — never drop it |
| **SA-11** | **Scoring a justified abstention as a failure** | "No answer" counted as unavailability, so the cheapest way to raise the SLI is to answer anyway | Split abstention by justification: no supporting evidence, unresolvable conflict, or insufficient authorization → **good event**; declining when the evidence was retrievable → bad event. See below |

### Abstention is an outcome class, not a failure class

`SA-10` and `SA-11` pull in opposite directions unless the two questions are kept apart. **Membership in the
denominator and classification as a bad event are separate decisions.** Laundering is removing the event;
mis-scoring is keeping it and grading it wrong. Both are defects, and fixing one by committing the other is
the common mistake.

An abstention is a **good event** when the supply chain correctly reported its own limit:

- no evidence supports the claim,
- two sources of equal authority conflict within the same scope,
- the requester is not authorized for the evidence that would answer it,
- the action requires a confirmation that has not been given.

It is a **bad event** when the evidence was retrievable and the system declined anyway — that is a retrieval
or ranking defect wearing an abstention's clothes, and it is invisible if every abstention is counted the
same way. Track `unjustified_abstention_rate` separately from the overall abstention rate; only the former
belongs in the error budget.

Scoring all abstentions as failures makes fabricating an answer the cheapest way to raise the SLI. The
evaluation set must therefore carry unanswerable, conflicting-source, and insufficient-permission cases with
abstention as the expected output — otherwise the metric rewards exactly the behavior the quality SLO exists
to prevent.

### Missing data is not a passing window

Excluding periods when the SLI could not be measured makes an SLO improve on paper as instrumentation
degrades. Declare a **missing-data policy** before the first measurement window closes: state whether an
unmeasured interval counts as good, bad, or excluded, and cap how much of a window may be excluded before
the window itself is void. For safety and authorization SLIs the default is **bad, not excluded** — losing
the ability to observe a control is not evidence the control held.

### Freshness targets are segmented by risk, not uniform

One freshness target across a whole corpus either overpays for static content or under-protects the volatile
kind. Segment by risk class (security advisory · policy · runbook · reference · FAQ) and set a target per
class. Report p50/p95/max and the breach count per class; a mean across classes hides the one that matters.

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
