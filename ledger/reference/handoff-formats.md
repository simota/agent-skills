# Handoff Formats

**Purpose:** Ledger と連携エージェント間のハンドオフYAMLテンプレート。
**Read when:** エージェント間でコスト関連情報を受け渡す時。

---

## Inbound Handoffs

### SCAFFOLD_TO_LEDGER

```yaml
SCAFFOLD_TO_LEDGER:
  request_type: "cost_estimation | tag_audit | right_sizing_review"
  iac_tool: "terraform | cloudformation | pulumi | opentofu"
  iac_path: "[path to IaC files or plan output]"
  environment: "dev | staging | production"
  context:
    current_monthly_spend: "[amount or N/A]"
    resource_count: "[number]"
    change_summary: "[brief description of IaC changes]"
  constraints:
    budget_limit: "[monthly amount or N/A]"
    timeline: "[urgency level]"
```

### BEACON_TO_LEDGER

```yaml
BEACON_TO_LEDGER:
  request_type: "cost_optimization | capacity_review | anomaly_correlation"
  slo_context:
    target_availability: "[e.g., 99.9%]"
    latency_p99: "[e.g., 200ms]"
    throughput: "[e.g., 1000 rps]"
  capacity_data:
    current_utilization: "[percentage]"
    growth_forecast: "[percentage per month]"
  constraints:
    no_downgrade_services: ["[service list]"]
    peak_hours: "[time range]"
```

### ATLAS_TO_LEDGER

```yaml
ATLAS_TO_LEDGER:
  request_type: "architecture_cost_review | migration_cost_estimate"
  architecture:
    topology: "[description or diagram reference]"
    services: ["[service list with resource types]"]
    data_flows: ["[flow descriptions with estimated volumes]"]
  context:
    migration_from: "[current state]"
    migration_to: "[target state]"
```

### PULSE_TO_LEDGER

```yaml
PULSE_TO_LEDGER:
  request_type: "unit_economics | cost_per_metric"
  business_metrics:
    mau: "[monthly active users]"
    transactions_per_month: "[count]"
    revenue_per_month: "[amount]"
  target_metrics:
    - name: "cost_per_user"
      current: "[amount]"
      target: "[amount]"
```

---

## Outbound Handoffs

### LEDGER_TO_SCAFFOLD

```yaml
LEDGER_TO_SCAFFOLD:
  deliverable_type: "right_sizing_recommendations | ri_sp_aligned_config | tag_enforcement"
  recommendations:
    - resource: "[resource identifier]"
      current: "[current type/size]"
      recommended: "[recommended type/size]"
      estimated_savings: "[monthly amount]"
      confidence: "high | medium | low"
      iac_change: "[brief description of required IaC change]"
  commitment_alignment:
    sp_type: "[Compute SP | EC2 Instance SP | N/A]"
    term: "[1yr | 3yr]"
    notes: "[alignment notes]"
```

### LEDGER_TO_BEACON

```yaml
LEDGER_TO_BEACON:
  deliverable_type: "cost_anomaly_rules | cost_alert_integration"
  anomaly_rules:
    - name: "[rule name]"
      condition: "[detection condition]"
      severity: "INFO | WARNING | CRITICAL | EMERGENCY"
      action: "[response action]"
  integration_points:
    alertmanager: "[config snippet or reference]"
    dashboard: "[widget specification]"
```

### LEDGER_TO_GEAR

```yaml
LEDGER_TO_GEAR:
  deliverable_type: "ci_cd_cost_gate | infracost_integration"
  cost_gate:
    tool: "infracost"
    thresholds:
      dev: { auto_approve: "$50", review: "$200", block: "$500" }
      staging: { auto_approve: "$100", review: "$500", block: "$1000" }
      production: { auto_approve: "$200", review: "$1000", block: "$2000" }
    workflow_file: "[path to workflow YAML]"
  integration_notes: "[setup instructions]"
```

### LEDGER_TO_CANVAS

```yaml
LEDGER_TO_CANVAS:
  deliverable_type: "cost_dashboard | trend_visualization | cost_report"
  dashboard_spec:
    type: "executive | team | engineering"
    widgets:
      - name: "[widget name]"
        metric: "[metric description]"
        visualization: "[chart type]"
        data_source: "[source]"
  data_context:
    time_range: "[e.g., last 12 months]"
    granularity: "daily | weekly | monthly"
    breakdown_dimensions: ["team", "service", "environment"]
```
