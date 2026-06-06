# Alert Configuration Reference

Purpose: Materialize an alert strategy into concrete, maintainable tooling config — Alertmanager routing trees, PagerDuty / Opsgenie receivers, on-call rotation wiring, and alert-as-code via Terraform or Pulumi. Gear `alert` does not decide WHAT to alert on; it implements the plumbing AFTER thresholds are defined.

## Scope Boundary

- **Gear `alert`**: alerting TOOL config. Alertmanager YAML syntax, receiver integrations, routing trees, severity labels, dedup / grouping / silence rules, on-call schedule plumbing, Terraform / Pulumi provider resources.
- **Beacon (SLO / alert strategy)**: WHAT to alert on. Golden Signals selection, SLI definition, burn-rate multi-window thresholds, P1-P4 taxonomy policy, runbook authorship, alert fatigue root-cause analysis.

If input is "should we page on 5xx at 1%?" → `Beacon` first. If input is "route P1 prod-api alerts to PagerDuty with 2-min grouping" → Gear `alert`. Typical handoff: Beacon → Gear once SLO + burn-rate thresholds are agreed.

## Tooling Matrix

| Layer | Tool | Pick when |
|-------|------|-----------|
| Rule engine | Prometheus alerting rules + Alertmanager | Prometheus-native stack |
| Rule engine | Grafana Alerting (unified) | Grafana Cloud / mixed datasources |
| Rule engine | Datadog Monitors | Already on Datadog |
| Paging | PagerDuty | Established on-call, complex schedules |
| Paging | Opsgenie (Atlassian) | Jira-integrated teams |
| Paging | incident.io / Rootly | Modern incident-response-first workflow |
| ChatOps | Slack / Teams webhook receiver | Low-severity / FYI notifications |
| As-code | Terraform `PagerDuty` / `Opsgenie` provider | GitOps + review workflow |
| As-code | Pulumi equivalents | Typed-language teams |

Default stack: Prometheus + Alertmanager + PagerDuty, managed via Terraform.

## Workflow

```
TUNE     → confirm SLO / thresholds / severity taxonomy came from Beacon
         → inventory existing receivers, silences, and rotation gaps
         → list noisiest alerts from last 30d (fatigue baseline)

TIGHTEN  → pick ONE: new route, receiver swap, dedup tuning, rotation fix
         → draft routing tree: group_by, group_wait, group_interval, repeat_interval
         → define inhibit_rules (suppress child alerts when parent fires)

GREASE   → apply config via Terraform / Pulumi (never click-ops in prod)
         → reload Alertmanager (`amtool check-config`, SIGHUP or hot-reload)
         → register Slack / PagerDuty service keys via secrets (never inline)

VERIFY   → `amtool alert add` synthetic fire → confirm receiver got paged
         → silence + inhibit paths tested separately
         → on-call primary / secondary receive on their device

PRESENT  → diff of routing tree, fatigue-delta estimate, rollback plan
```

## Routing Tree Pattern

```yaml
# alertmanager.yml
route:
  receiver: default-slack
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers:
        - severity="P1"
        - env="prod"
      receiver: pagerduty-prod-primary
      group_wait: 10s
      continue: false
    - matchers:
        - severity=~"P2|P3"
      receiver: slack-oncall
inhibit_rules:
  - source_matchers: [severity="P1"]
    target_matchers: [severity=~"P2|P3"]
    equal: ['cluster', 'service']
```

## Severity Taxonomy (Enforce, Don't Invent)

| Severity | Response | Channel | Example |
|----------|----------|---------|---------|
| P1 | Page on-call, ack ≤ 5 min | PagerDuty high-urgency | Availability SLO burn-rate 14.4× (1h) |
| P2 | Page during business hours | PagerDuty low-urgency | Latency SLO burn-rate 6× (6h) |
| P3 | Slack ticket, next business day | Slack + Jira | Dependency deprecated, disk 70% |
| P4 | FYI, dashboard-only | Slack info channel | Informational trend |

Taxonomy source = Beacon. Gear only enforces the label → receiver mapping.

## Alert Fatigue Mitigation

- **Dedup**: `group_by` on `['alertname', 'service', 'instance']` — never omit `alertname`.
- **Grouping**: tune `group_wait` (first wait) vs `group_interval` (subsequent) — defaults 30s / 5m are sane; shorten only for P1.
- **Silence**: use `amtool silence add` with expiry for planned maintenance; never permanent.
- **Inhibit**: parent-child suppression (cluster-down inhibits pod-down).
- **Repeat interval**: 4h default for non-P1; shorten only when ignoring would cause SLO breach.
- **Audit monthly**: top 10 noisiest alerts → send back to Beacon for threshold review.

## On-Call Rotation Plumbing

- Primary + secondary + escalation (usually eng-manager or IC lead).
- Business-hours vs 24/7 split via time-based schedule layers.
- Holiday overrides declared in Terraform; no ad-hoc swaps without PR.
- Honeymoon rule: new hire shadows for ≥ 2 rotations before going primary.
- Paging fatigue quota: > 2 P1 pages per shift triggers post-incident review.

## Alert-as-Code Pattern

```hcl
# Terraform — PagerDuty service + Alertmanager receiver wired together
resource "pagerduty_service" "prod_api" {
  name              = "prod-api"
  escalation_policy = pagerduty_escalation_policy.primary.id
  alert_creation    = "create_alerts_and_incidents"
}

resource "pagerduty_service_integration" "prometheus" {
  name    = "Prometheus"
  service = pagerduty_service.prod_api.id
  vendor  = data.pagerduty_vendor.prometheus.id
}
```

Integration key lives in Vault / Secrets Manager, injected into Alertmanager via secret mount.

## Anti-Patterns

- Alerting on causes (CPU 90%) instead of symptoms (SLO burn-rate) — push back to Beacon.
- Manual UI edits in PagerDuty / Opsgenie — drift from Terraform state within a week.
- `group_by: []` (group everything) or `group_by: ['...']` (group nothing) — both hide real signals.
- Inline integration keys or Slack webhook URLs in Git — use sealed-secrets / Vault.
- Skipping synthetic-fire verification — first real incident is the wrong time to learn the receiver is broken.
- Single point of failure: one on-call primary with no secondary.

## Handoff

- **From Beacon**: SLO, SLI, burn-rate thresholds, severity policy, runbook URLs.
- **To Beacon**: fatigue telemetry (noisy alerts, ack-time distribution) for threshold retuning.
- **To Mend**: runbook-backed alerts with auto-remediation candidates.
- **To Triage**: PagerDuty service IDs and escalation map for incident response.
