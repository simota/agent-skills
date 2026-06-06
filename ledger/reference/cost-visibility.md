# Cost Visibility

**Purpose:** タグ戦略、コスト配分、ダッシュボード仕様、showback/chargebackの設計ガイド。
**Read when:** コストの可視化・配分・レポート設計が必要な時。

---

## Tag Taxonomy Design

### Hierarchical Tag Structure

```yaml
TAG_HIERARCHY:
  business:
    cost-center: "CC-XXXX"       # Finance mapping
    business-unit: "engineering"  # Organization unit
    project: "project-alpha"     # Project tracking

  technical:
    team: "platform"             # Team ownership
    service: "api-gateway"       # Service name
    environment: "production"    # Deployment environment
    component: "backend"         # Service component

  operational:
    managed-by: "terraform"      # IaC tool
    owner: "alice@example.com"   # Primary contact
    created-date: "2026-01-15"   # Resource creation date

  cost_optimization:
    schedule: "business-hours"   # Auto start/stop
    commitment: "ri-eligible"    # RI/SP candidate
    criticality: "high"          # Business criticality
```

### Tag Naming Conventions

| Rule | Example | Rationale |
|------|---------|-----------|
| Lowercase, hyphen-separated | `cost-center` | Consistency |
| No spaces or special characters | `business-unit` | API compatibility |
| Prefix for namespacing | `finops:team` | Avoid conflicts |
| Consistent value format | `prod`, not `production` / `PROD` | Query reliability |

---

## Showback vs Chargeback

| Model | Description | When to Use |
|-------|-------------|-------------|
| **Showback** | Report costs to teams, no financial charge | Early FinOps maturity, building awareness |
| **Chargeback** | Charge costs to team budgets | Mature FinOps, financial accountability |
| **Hybrid** | Showback for shared, chargeback for dedicated | Most organizations |

### Shared Cost Allocation

| Resource Type | Allocation Method | Example |
|--------------|-------------------|---------|
| Shared VPC / networking | Equal split or proportional | $1000 / 5 teams = $200 each |
| Shared database | Usage-based (connections/queries) | Team A: 60%, Team B: 40% |
| Platform services | Headcount-based or equal | Per-engineer allocation |
| Support / FinOps overhead | Proportional to total spend | 3% overhead on team cost |

---

## Cost Dashboard Specification

### Executive Dashboard

| Widget | Metric | Visualization | Refresh |
|--------|--------|--------------|---------|
| Total monthly spend | Current vs budget vs last month | Gauge + trend | Daily |
| Spend by team | Top 10 teams | Horizontal bar | Daily |
| Month-over-month trend | 12-month trend | Line chart | Daily |
| Commitment coverage | RI/SP utilization % | Gauge | Weekly |
| Top cost anomalies | Last 7 days | Alert list | Real-time |

### Team Dashboard

| Widget | Metric | Visualization | Refresh |
|--------|--------|--------------|---------|
| Team monthly spend | Current vs budget | Gauge | Daily |
| Spend by service | Breakdown by AWS/GCP service | Stacked bar | Daily |
| Spend by environment | dev/staging/prod split | Pie chart | Daily |
| Cost per unit | $/request, $/user, $/transaction | Line chart | Daily |
| Right-sizing opportunities | Underutilized resources | Table | Weekly |
| Waste alerts | Idle/orphaned resources | Alert list | Daily |

### Engineering Dashboard

| Widget | Metric | Visualization | Refresh |
|--------|--------|--------------|---------|
| Cost per deployment | Average infrastructure cost per deploy | Line chart | Per-deploy |
| Spot savings | On-demand vs Spot savings | Bar chart | Daily |
| Data transfer costs | Ingress/egress by service | Sankey diagram | Daily |
| Resource utilization | CPU/Memory/Disk efficiency | Heatmap | Hourly |

---

## Unit Economics

### Key Cost Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Cost per request | Total infra cost / total requests | Decreasing trend |
| Cost per user | Total infra cost / MAU | Decreasing trend |
| Cost per transaction | Total infra cost / transactions | Stable or decreasing |
| Infrastructure cost ratio | Infra cost / revenue | < 15-25% for SaaS |
| Marginal cost | Cost increase per new user | Near-zero (scalable) |

### Unit Cost Tracking Setup

```sql
-- Example BigQuery query for unit economics (GCP)
SELECT
  DATE_TRUNC(usage_start_time, MONTH) AS month,
  SUM(cost) AS total_cost,
  -- Join with application metrics
  app_metrics.total_requests,
  app_metrics.mau,
  SUM(cost) / app_metrics.total_requests AS cost_per_request,
  SUM(cost) / app_metrics.mau AS cost_per_user
FROM `billing_export.gcp_billing_export_v1_*`
JOIN `analytics.monthly_metrics` AS app_metrics
  ON DATE_TRUNC(usage_start_time, MONTH) = app_metrics.month
GROUP BY month, app_metrics.total_requests, app_metrics.mau
ORDER BY month DESC
```

---

## Cost Report Template

```markdown
## Monthly FinOps Report — {YYYY-MM}

### Executive Summary
- Total spend: $XX,XXX (budget: $XX,XXX, delta: +/- N%)
- MoM change: +/- N%
- Top cost driver: [service/team]
- Key action items: [1-3 items]

### Spend Breakdown
| Team | Spend | Budget | Delta | Trend |
|------|-------|--------|-------|-------|
| ... | ... | ... | ... | ↑/↓/→ |

### Optimization Wins
| Action | Monthly Savings | Implemented By |
|--------|----------------|----------------|
| ... | ... | ... |

### Open Opportunities
| Opportunity | Estimated Savings | Effort | Priority |
|-------------|-------------------|--------|----------|
| ... | ... | ... | ... |

### Commitment Status
- RI/SP coverage: N%
- Utilization: N%
- Expiring next quarter: [list]

### Next Month Actions
1. [Action 1]
2. [Action 2]
3. [Action 3]
```
