# Toil Automation Reference

Toil identification framework, automation scoring, and self-healing design reference.

---

## Toil Identification

### Toil Characteristics

| Characteristic | Description | Example |
|----------------|-------------|---------|
| **Manual** | Requires human execution | Restarting a pod |
| **Repetitive** | Same task done frequently | Weekly certificate rotation |
| **Automatable** | Can be scripted | Log cleanup |
| **Reactive** | Triggered by alerts/events | Scaling after traffic spike |
| **No enduring value** | Doesn't improve the service | Password resets |
| **Scales with service** | Grows with usage/size | Manual user provisioning |

### Toil Audit Template

```markdown
| Task | Frequency | Duration | Automatable? | Impact | Priority |
|------|-----------|----------|-------------|--------|----------|
| Pod restart on OOM | 3/week | 10min | Yes | High | P1 |
| SSL cert renewal | Monthly | 30min | Yes | Medium | P2 |
| Log rotation | Weekly | 15min | Yes | Low | P3 |
| DB backup verify | Daily | 5min | Yes | High | P1 |
| User access review | Monthly | 2h | Partial | Medium | P2 |
```

---

## Automation Scoring

### Automation ROI Formula

```
Time saved per year = frequency × duration × 52 weeks
Automation cost = development_hours × hourly_rate
ROI period = automation_cost / (time_saved × hourly_rate)
Maintenance cost = 10-20% of automation_cost per year

Example:
  Task: Manual pod restart (3×/week, 10 min each)
  Time saved = 3 × 10 × 52 = 1560 min/year = 26 hours
  Automation cost = 8 hours development
  ROI period = 8 / 26 = 0.31 years = ~4 months
  → AUTOMATE
```

### Priority Matrix

| | Low Frequency | High Frequency |
|---|---|---|
| **Easy to automate** | P3 (backlog) | P1 (do now) |
| **Hard to automate** | P4 (defer) | P2 (plan) |

---

## Self-Healing Patterns

### Pattern Catalog

| Pattern | Trigger | Action | Safeguard |
|---------|---------|--------|-----------|
| **Auto-restart** | Health check failure | Restart container | Max restart count |
| **Auto-scale** | Load threshold | Add instances | Max instance limit |
| **Auto-rollback** | Error rate spike after deploy | Revert to previous version | Rollback window |
| **Auto-failover** | Primary unreachable | Promote secondary | Split-brain protection |
| **Auto-drain** | Node unhealthy | Migrate workloads | Minimum healthy nodes |
| **Auto-remediate** | Disk full | Clean old logs/artifacts | Retention minimum |

### Self-Healing Implementation

```yaml
# Kubernetes self-healing example
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: app
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10
            failureThreshold: 3    # Restart after 3 failures
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 5
            failureThreshold: 2    # Remove from LB after 2 failures
          startupProbe:
            httpGet:
              path: /healthz
              port: 8080
            failureThreshold: 30
            periodSeconds: 10      # Allow 5 min for startup
```

### Auto-Rollback Design

```python
class AutoRollback:
    def __init__(self, error_threshold: float = 0.05, window_minutes: int = 10):
        self.error_threshold = error_threshold
        self.window = window_minutes

    def should_rollback(self, metrics: DeploymentMetrics) -> bool:
        if metrics.minutes_since_deploy > self.window:
            return False  # Past observation window

        current_error_rate = metrics.error_count / metrics.request_count
        baseline_error_rate = metrics.baseline_error_rate

        return current_error_rate > baseline_error_rate + self.error_threshold
```

---

## Toil Budget

### SRE Toil Budget Guidelines

| Category | Target Allocation |
|----------|------------------|
| **Toil (operational work)** | ≤ 50% of team time |
| **Engineering (project work)** | ≥ 50% of team time |
| **On-call (included in toil)** | ≤ 25% of team time |

### Toil Tracking

```markdown
## Weekly Toil Report

### Summary
- Total toil hours: X / Y budget (X%)
- Top toil tasks:
  1. [Task] — [hours] — [automation status]
  2. [Task] — [hours] — [automation status]

### Automation Pipeline
| Task | Status | ETA | Expected Savings |
|------|--------|-----|-----------------|
| [Task] | In Progress | 2 weeks | 4 hrs/week |
| [Task] | Planned | Next sprint | 2 hrs/week |

### Trend
- This week: X hours (Y% of budget)
- Last week: X hours
- 4-week avg: X hours
- Trend: ↑/↓/→
```
