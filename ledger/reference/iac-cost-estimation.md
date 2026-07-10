# IaC Cost Estimation

**Purpose:** Methods for estimating cloud costs from IaC code and a tool integration guide.
**Read when:** Assessing the cost impact of Terraform/CloudFormation/Pulumi changes.

---

## Infracost Integration

### Basic Workflow

```bash
# Estimate cost from a Terraform plan
infracost breakdown --path .

# Compare cost across a PR diff
infracost diff --path . --compare-to infracost-base.json

# CI/CD pipeline integration (GitHub Actions)
infracost comment --path . --format github-comment --behavior update
```

### CI/CD Cost Gate

```yaml
# GitHub Actions example
- name: Infracost
  run: |
    infracost diff --path . --compare-to /tmp/infracost-base.json --format json --out-file /tmp/infracost.json
    DIFF=$(jq -r '.diffTotalMonthlyCost' /tmp/infracost.json)
    if (( $(echo "$DIFF > 100" | bc -l) )); then
      echo "::warning::Monthly cost increase exceeds $100 threshold"
    fi
```

### Threshold Configuration

| Environment | Monthly Increase Threshold | Action |
|-------------|---------------------------|--------|
| dev | > $50 | Warning comment |
| staging | > $100 | Warning + approval required |
| production | > $500 | Block + mandatory review |

---

## Pricing API Reference

### AWS Pricing

| Method | Use Case | Accuracy |
|--------|----------|----------|
| AWS Pricing API | Programmatic lookup | High |
| AWS Cost Calculator | Interactive planning | High |
| Infracost | Terraform-native | High (90%+ resources) |
| Cost Explorer forecast | Historical projection | Medium |

### GCP Pricing

| Method | Use Case | Accuracy |
|--------|----------|----------|
| GCP Pricing Calculator | Interactive planning | High |
| Cloud Billing API | Programmatic lookup | High |
| Infracost | Terraform-native | High |
| Billing Export to BigQuery | Historical analysis | High |

### Azure Pricing

| Method | Use Case | Accuracy |
|--------|----------|----------|
| Azure Pricing Calculator | Interactive planning | High |
| Azure Cost Management API | Programmatic lookup | High |
| Infracost | Terraform-native | High |
| Cost Analysis + Advisor | Historical + recommendations | Medium-High |

---

## High-Cost Resource Flags

The following resources have a large cost impact, so always flag them at creation time:

| Resource | Typical Monthly Cost | Warning |
|----------|---------------------|---------|
| NAT Gateway (AWS) | $32+ per gateway + data processing | 1 per AZ × number of AZs |
| Transit Gateway | $36+ per attachment | Scales with number of VPCs |
| HA Database (non-prod) | 2× single instance | Often unnecessary in dev environments |
| GPU Instance | $500-$30,000+ | Consider scheduling based on usage hours |
| Interface VPC Endpoint | $7+ per endpoint per AZ | Many services × number of AZs |
| Cross-region data transfer | $0.02/GB | Easy to end up costing more than expected |
| AlloyDB / Spanner (GCP) | $500+/month | Overkill for small-scale use |
| Premium SSD (Azure) | 2-3× Standard SSD | Check IOPS requirements |

---

## Cost Estimation Report Template

```markdown
## Cost Estimation Report

### Summary
- **Estimated monthly cost (before):** $X,XXX
- **Estimated monthly cost (after):** $Y,YYY
- **Monthly delta:** +/- $ZZZ (+/- N%)
- **Confidence level:** High / Medium / Low

### Assumptions
1. [Usage assumption 1]
2. [Data transfer assumption]
3. [Pricing tier assumption]

### Resource Breakdown
| Resource | Type | Monthly Cost | Notes |
|----------|------|-------------|-------|
| ... | ... | ... | ... |

### High-Cost Warnings
- [Warning 1]
- [Warning 2]

### Data Transfer Costs
- Intra-region: $X
- Cross-region: $Y
- Internet egress: $Z

### Recommendations
1. [Cost optimization recommendation]
2. [Alternative architecture suggestion]
```

---

## Data Transfer Cost Matrix

| Transfer Type | AWS | GCP | Azure |
|--------------|-----|-----|-------|
| Same AZ | Free | Free | Free |
| Cross-AZ | $0.01/GB | $0.01/GB | Free (most) |
| Cross-region | $0.02/GB | $0.01-0.08/GB | $0.02-0.05/GB |
| Internet egress | $0.09/GB (first 10TB) | $0.12/GB (first 1TB) | $0.087/GB (first 5GB free) |
| VPC Peering cross-region | $0.01/GB | $0.01/GB | $0.035/GB |

**Note:** Pricing changes frequently. Check each cloud provider's pricing page for current prices.
