# Cost Anomaly Detection

**Purpose:** コスト異常検知パターン、検知ルール設計、対応プレイブック。
**Read when:** 予期しないコストスパイクや異常パターンの検知が必要な時。

---

## Anomaly Detection Methods

### Statistical Methods

| Method | Best For | Sensitivity | Complexity |
|--------|----------|-------------|------------|
| Moving average (7-day) | Steady workloads | Medium | Low |
| Standard deviation (2σ/3σ) | Normal distribution costs | Adjustable | Low |
| Exponential smoothing | Trending costs | Medium | Medium |
| Seasonal decomposition | Cyclical patterns | High | Medium |
| ML-based (AWS Cost Anomaly Detection) | Complex patterns | High | Low (managed) |

### Detection Rules

```yaml
ANOMALY_RULES:
  daily_spike:
    description: "Daily cost exceeds 7-day moving average by threshold"
    condition: "daily_cost > (7d_avg * 1.3)"
    severity: WARNING
    action: investigate

  daily_critical:
    description: "Daily cost exceeds 7-day moving average by 2x"
    condition: "daily_cost > (7d_avg * 2.0)"
    severity: CRITICAL
    action: immediate_investigation

  monthly_drift:
    description: "Monthly forecast exceeds budget by threshold"
    condition: "monthly_forecast > (budget * 1.1)"
    severity: WARNING
    action: review

  new_service:
    description: "Cost from previously unseen service"
    condition: "service NOT IN last_30d_services"
    severity: INFO
    action: categorize_and_tag

  zombie_resource:
    description: "Resource with zero utilization"
    condition: "utilization == 0 AND age > 7d"
    severity: WARNING
    action: confirm_and_schedule_termination
```

---

## Anomaly Categories

| Category | Pattern | Root Cause Examples |
|----------|---------|-------------------|
| **Spike** | Sudden cost increase | Runaway autoscaling, data processing job, attack |
| **Drift** | Gradual upward trend | Organic growth, scope creep, configuration drift |
| **New Service** | Unexpected service cost | Unplanned resource, forgotten experiment |
| **Zombie** | Cost for idle resource | Orphaned infrastructure, abandoned project |
| **Data Transfer** | High egress cost | Cross-region replication, misconfigured CDN |
| **Commitment Gap** | RI/SP utilization drop | Workload change, decommissioned service |

---

## Response Playbook

### Spike Response (> 30% daily increase)

```
1. DETECT: Alert fires
2. TRIAGE (15 min):
   - Identify affected service/account/region
   - Check for known deployments or changes
   - Determine if legitimate or anomalous
3. INVESTIGATE (30 min):
   - Cost Explorer breakdown by service/resource
   - Correlate with deployment logs
   - Check autoscaling events
   - Review data transfer patterns
4. RESPOND:
   - If runaway scaling: Apply scaling limits
   - If data issue: Fix data pipeline
   - If attack: Engage security (Sentinel/Breach)
   - If legitimate: Update budget/forecast
5. DOCUMENT:
   - Root cause
   - Impact ($ amount)
   - Prevention measures
```

### Drift Response (> 10% monthly increase)

```
1. DETECT: Monthly review identifies trend
2. CATEGORIZE:
   - Organic growth (expected): Update forecasts
   - Scope creep (unplanned): Review with team
   - Waste (unnecessary): Optimize
3. ACTION:
   - Organic: Adjust budget, review commitments
   - Scope creep: Prioritize and rationalize
   - Waste: Right-size or eliminate
4. TRACK:
   - Set specific reduction targets
   - Review at next monthly cadence
```

---

## Cloud-Native Anomaly Detection Services

### AWS

```yaml
AWS_COST_ANOMALY_DETECTION:
  setup:
    - Create cost monitor (service/account/tag-based)
    - Set alert threshold (% or $)
    - Configure SNS notifications
  monitors:
    - type: SERVICE
      services: [EC2, RDS, S3, Lambda]
    - type: COST_CATEGORY
      categories: [team-platform, team-backend]
    - type: LINKED_ACCOUNT
      accounts: [dev, staging, prod]
```

### GCP

```yaml
GCP_BUDGET_ALERTS:
  setup:
    - Create budget per project/billing account
    - Set threshold percentages
    - Configure Pub/Sub notifications
  advanced:
    - Export billing to BigQuery
    - Custom anomaly queries with SQL
    - Looker Studio dashboards
```

### Azure

```yaml
AZURE_COST_MANAGEMENT:
  setup:
    - Create cost alerts (budget/anomaly/credit)
    - Set action groups for notifications
    - Configure Logic Apps for automation
  features:
    - Built-in anomaly detection
    - Smart alerts with ML
    - Cost recommendations via Advisor
```

---

## Alert Fatigue Prevention

| Strategy | Implementation |
|----------|---------------|
| Tiered severity | INFO → WARNING → CRITICAL → EMERGENCY |
| Suppression window | No repeat alerts within 4 hours |
| Aggregate alerts | Group related anomalies per account/service |
| Context enrichment | Include recent changes, deployment info |
| Auto-resolution | Clear alert when cost normalizes |
| Weekly digest | Summarize minor anomalies weekly |
