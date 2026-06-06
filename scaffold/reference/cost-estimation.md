# Terraform Cost Estimation Reference

Purpose: Use this file when you need a cost estimate, warning thresholds, tagging rules, or budget patterns for Terraform-managed infrastructure.

Contents:
1. Estimation workflow
2. Infracost quick start
3. High-cost signals
4. Environment multipliers and formulas
5. Report template
6. Budgets, tagging, commitments, optimization

## Estimation Workflow

1. Read Terraform files and identify billable resource blocks.
2. Extract cost-driving attributes: size, count, AZ count, HA flags, transfer, storage, `min_instances`.
3. Apply environment multipliers:
   - `dev`: single-AZ, smaller, no HA when safe
   - `staging`: production-like but scaled down
   - `prod`: full HA, backups, monitoring
4. Produce:
   - per-resource breakdown
   - category subtotal
   - warning list

## Infracost Quick Start

```bash
brew install infracost
infracost auth login
infracost breakdown --path /path/to/terraform
infracost diff --path /path/to/terraform --compare-to infracost-base.json
```

Monorepo example:

```yaml
version: 0.1
projects:
  - path: environments/dev
    name: dev
  - path: environments/staging
    name: staging
  - path: environments/prod
    name: prod
```

Note: the free tier referenced in the existing skill is `1,000` runs/month.

## High-Cost Signals

Flag these explicitly:

| Resource | Warning |
|----------|---------|
| NAT Gateway (AWS/GCP) | Always flag, roughly `$45-50` per gateway/month before meaningful transfer |
| Interface VPC Endpoints | Flag if `>3` endpoints |
| RDS / Cloud SQL HA | Flag in `dev` or `staging` |
| Transit Gateway | Flag per attachment |
| ElastiCache / Memorystore | Flag above small tiers |
| EKS / GKE Standard | Flag node count `>3` |
| Spanner / AlloyDB | Always flag; baseline is `>$500/month` and often much higher |
| Always-on Cloud Run | Flag `min_instances > 0` outside prod |

## Environment Multipliers And Formulas

Key heuristics:
- AWS Graviton / GCP Tau can reduce compute cost by about `20%`
- Cloud SQL `REGIONAL` is about `1.8x` `ZONAL`
- Savings Plans / RI / CUD can reduce steady-state cost by roughly `28-72%` depending on commitment type
- Spot / Preemptible can reduce cost by about `60-90%` for interruptible workloads

Useful formulas:

```text
Fargate monthly
= desired_count × (vCPU_price × vCPU + memory_price × memory_GB) × 730

Lambda monthly
= request_cost + GB-seconds × compute_rate

Aurora Serverless v2 monthly
= avg_ACU × ACU_rate × 730 + storage_GB × storage_rate

Cloud Run monthly
= active_seconds × per-second price + request charges
```

## Cost Report Template

```markdown
## Cost Estimate: [Project/Module Name]

**Provider**: AWS / GCP / Azure
**Region**: [region]
**Estimated by**: Manual analysis / Infracost
**Date**: YYYY-MM-DD

### Resource Breakdown

| # | Resource | Terraform Reference | Spec | Count | Monthly (USD) |
|---|----------|-------------------|------|-------|---------------|
| 1 | [type]   | `resource.name`   | [spec] | N | $XX |

### Warnings

- [High-cost or high-risk item]

### Optimization Opportunities

- [Potential saving and rationale]
```

## Budgets, Tagging, Commitments, Optimization

### Budget alerts

Use staged alerts at:
- `50%`
- `80%`
- `100%`
- `120%`

### Required cost tags

Use these tags everywhere cost allocation matters:
- `Project`
- `Environment`
- `Team`
- `CostCenter`
- `ManagedBy`

### Commitment strategy

- Start around `60-70%` committed coverage for stable workloads.
- Keep the remaining `30-40%` flexible with on-demand or spot capacity.
- Prefer flexible commitments before rigid family locks.

### Optimization checklist

- Remove NAT gateways from low-risk non-prod environments when alternatives exist.
- Replace Multi-AZ databases in non-prod with single-AZ where safe.
- Release unattached EIPs, stale disks, empty load balancers, and old snapshots.
- Move old storage to cheaper classes.
- Scale Cloud Run to zero in non-prod when appropriate.
- Right-size after at least `2+ weeks` of usage data.
