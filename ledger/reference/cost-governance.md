# Cost Governance

**Purpose:** 予算アラート、CI/CDコストゲート、タグ強制、継続的コスト管理の運用設計。
**Read when:** コストガバナンスの仕組み構築が必要な時。

---

## Budget Alert Design

### Alert Escalation Matrix

| Threshold | Alert Type | Recipient | Action |
|-----------|-----------|-----------|--------|
| 50% of monthly budget | Info | Team Slack channel | Awareness |
| 75% of monthly budget | Warning | Team lead + FinOps | Review spending |
| 90% of monthly budget | Critical | Engineering manager | Spending freeze review |
| 100% of monthly budget | Emergency | VP Engineering | Mandatory action plan |
| 120% of monthly budget | Executive | CTO / CFO | Incident-level response |

### Budget Configuration Template

```yaml
# AWS Budget example
budget:
  name: "team-{team_name}-monthly"
  amount: 10000  # USD
  time_unit: MONTHLY

  notifications:
    - threshold: 50
      type: ACTUAL
      subscribers: ["team-slack-webhook"]
    - threshold: 75
      type: ACTUAL
      subscribers: ["team-lead@example.com"]
    - threshold: 90
      type: ACTUAL
      subscribers: ["eng-manager@example.com"]
    - threshold: 100
      type: FORECASTED
      subscribers: ["finops-team@example.com"]

  cost_filters:
    tags:
      team: ["{team_name}"]
```

---

## CI/CD Cost Gate Integration

### Infracost PR Gate

```yaml
# .github/workflows/cost-gate.yml
name: Cost Gate
on: [pull_request]

jobs:
  cost-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}

      - name: Generate cost diff
        run: |
          infracost diff \
            --path . \
            --compare-to infracost-base.json \
            --format json \
            --out-file /tmp/infracost.json

      - name: Check threshold
        run: |
          DIFF=$(jq -r '.diffTotalMonthlyCost' /tmp/infracost.json)
          THRESHOLD="${COST_THRESHOLD:-100}"
          if (( $(echo "$DIFF > $THRESHOLD" | bc -l) )); then
            echo "COST_EXCEEDED=true" >> $GITHUB_ENV
          fi

      - name: Comment on PR
        uses: infracost/actions/comment@v3
        with:
          path: /tmp/infracost.json
          behavior: update
```

### Cost Gate Thresholds

| Environment | Auto-approve | Requires Review | Blocks Merge |
|-------------|-------------|-----------------|--------------|
| dev | < $50/mo increase | $50-200/mo | > $200/mo |
| staging | < $100/mo increase | $100-500/mo | > $500/mo |
| production | < $200/mo increase | $200-1000/mo | > $1000/mo |

---

## Tag Enforcement

### Required Tags

| Tag Key | Purpose | Example Values | Enforcement |
|---------|---------|----------------|-------------|
| `team` | Cost allocation | `platform`, `backend`, `data` | Mandatory |
| `environment` | Env separation | `dev`, `staging`, `prod` | Mandatory |
| `service` | Service mapping | `api`, `web`, `worker` | Mandatory |
| `cost-center` | Finance mapping | `CC-1234` | Mandatory (prod) |
| `owner` | Accountability | `alice@example.com` | Recommended |
| `project` | Project tracking | `project-alpha` | Recommended |
| `managed-by` | IaC tracking | `terraform`, `manual` | Recommended |

### Tag Policy Enforcement

```hcl
# AWS SCP for tag enforcement
resource "aws_organizations_policy" "require_tags" {
  name    = "require-cost-tags"
  type    = "TAG_POLICY"
  content = jsonencode({
    tags = {
      team        = { tag_key = { "@@assign" = "team" }, enforced_for = { "@@assign" = ["ec2:*", "rds:*", "s3:*"] } }
      environment = { tag_key = { "@@assign" = "environment" }, enforced_for = { "@@assign" = ["ec2:*", "rds:*", "s3:*"] } }
      service     = { tag_key = { "@@assign" = "service" }, enforced_for = { "@@assign" = ["ec2:*", "rds:*", "s3:*"] } }
    }
  })
}
```

---

## Continuous Cost Review Cadence

| Cadence | Activity | Participants | Output |
|---------|----------|-------------|--------|
| Daily | Anomaly detection alert review | On-call engineer | Acknowledge / investigate |
| Weekly | Cost trend review | Team leads | Action items |
| Monthly | FinOps review | Engineering + Finance | Optimization report |
| Quarterly | Commitment review | FinOps + Finance | RI/SP purchase/adjustment |
| Annual | Architecture cost review | Tech leads + FinOps | Architecture optimization plan |

---

## FinOps Maturity Model

| Phase | Crawl | Walk | Run |
|-------|-------|------|-----|
| Visibility | Basic tagging, monthly reports | Per-team showback, automated reports | Real-time dashboards, unit economics |
| Optimization | Manual right-sizing, basic RI | Automated recommendations, SP coverage | ML-driven auto-optimization |
| Governance | Manual budget alerts | CI/CD cost gates, tag enforcement | Policy-as-code, automated remediation |
| Culture | Centralized FinOps team | Embedded FinOps practices | Engineering-owned cost optimization |

---

## Automated Remediation Patterns

| Trigger | Automated Action | Safety Gate |
|---------|-----------------|-------------|
| Dev instance idle > 24h weekday | Stop instance | Tag `auto-stop: true` required |
| Dev environment weekend | Stop all non-exempt | Tag `weekend-exempt: true` to skip |
| Untagged resource > 48h | Notify owner, add `untagged` flag | 7-day grace before termination |
| EBS volume unattached > 7d | Snapshot + schedule deletion | Notify owner first |
| Cost spike > 50% daily | Alert + auto-investigation | No auto-remediation |
