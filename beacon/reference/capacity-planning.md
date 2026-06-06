# Capacity Planning Reference

Load modeling, auto-scaling strategies, and resource forecasting reference.

---

## Load Modeling

### Traffic Pattern Types

| Pattern | Description | Example |
|---------|-------------|---------|
| **Diurnal** | Daily peak/trough cycle | B2B SaaS (9am-5pm) |
| **Weekly** | Weekday vs weekend variation | E-commerce |
| **Seasonal** | Annual peaks | Black Friday, tax season |
| **Event-driven** | Sudden spikes | Product launch, marketing push |
| **Growth** | Steady increase over time | User base growth |

### Load Model Template

```yaml
load_model:
  service: "api-gateway"
  baseline:
    avg_rps: 500
    peak_rps: 1200
    peak_times: ["09:00-11:00 UTC", "14:00-16:00 UTC"]
  growth:
    monthly_rate: 8%
    projection_months: 12
  spikes:
    - event: "product_launch"
      multiplier: 3x
      duration: "4h"
    - event: "marketing_campaign"
      multiplier: 2x
      duration: "24h"
  resource_per_rps:
    cpu_cores: 0.002
    memory_mb: 4
    connections: 0.5
```

### Capacity Estimation Formula

```
Required capacity = Peak RPS × Resource per RPS × Safety margin

Example:
  Peak RPS: 1200
  CPU per RPS: 0.002 cores
  Safety margin: 1.5 (50% headroom)

  CPU needed = 1200 × 0.002 × 1.5 = 3.6 cores

With growth (12 months at 8%/month):
  Future peak = 1200 × (1.08)^12 = 3023 RPS
  CPU needed = 3023 × 0.002 × 1.5 = 9.07 cores
```

---

## Auto-Scaling Strategies

| Strategy | Metric | Pros | Cons |
|----------|--------|------|------|
| **Target tracking** | CPU/memory target | Simple, built-in | Reactive |
| **Step scaling** | Metric thresholds | Fine-grained control | Complex config |
| **Scheduled** | Time-based | Proactive for known patterns | Rigid |
| **Predictive** | ML-based forecast | Proactive for variable patterns | Requires history |
| **Custom metric** | Business metric (RPS, queue depth) | Precise | Implementation effort |

### HPA Configuration Pattern

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-service
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  minReplicas: 3
  maxReplicas: 50
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: 100
```

---

## Resource Forecasting

### Right-Sizing Methodology

```
1. Collect 2-4 weeks of resource usage data
2. Identify peak usage (p95 or p99)
3. Calculate utilization ratio: actual / allocated
4. Right-size: new_allocation = p99_usage × safety_margin

Under-utilized (< 30% avg):
  → Reduce allocation, consider burstable instances

Over-utilized (> 80% avg):
  → Increase allocation, monitor for throttling

Right-sized (40-70% avg with peaks < 90%):
  → Current allocation is appropriate
```

### Forecasting Table

| Timeframe | Method | Accuracy | Use |
|-----------|--------|----------|-----|
| **1-7 days** | Linear extrapolation | High | Incident capacity |
| **1-3 months** | Trend + seasonality | Medium | Sprint planning |
| **6-12 months** | Growth modeling | Low-Medium | Budget planning |
| **1-3 years** | Business forecasting | Low | Strategic planning |

---

## Capacity Review Checklist

```markdown
## Monthly Capacity Review

### Resource Utilization
- [ ] CPU: avg < 70%, p99 < 90%
- [ ] Memory: avg < 75%, p99 < 90%
- [ ] Disk: usage < 70%, growth rate sustainable
- [ ] Network: bandwidth < 60% of limit

### Scaling
- [ ] Auto-scaling events reviewed (frequency, duration)
- [ ] Min/max replica counts still appropriate
- [ ] Scale-up latency within acceptable range
- [ ] No scaling oscillation (flapping)

### Cost
- [ ] Resource costs within budget
- [ ] Reserved/committed use discounts applied where stable
- [ ] Spot/preemptible instances used for fault-tolerant workloads
- [ ] Unused resources identified and reclaimed

### Growth
- [ ] Traffic growth tracking against forecast
- [ ] Capacity headroom > 30% for next 3 months
- [ ] Known upcoming events factored in
```
