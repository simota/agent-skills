# IaC Cost Estimation

**Purpose:** IaCコードからクラウドコストを推定する手法とツール統合ガイド。
**Read when:** Terraform/CloudFormation/Pulumiのコスト影響を評価する必要がある時。

---

## Infracost Integration

### Basic Workflow

```bash
# Terraform plan からコスト推定
infracost breakdown --path .

# PR差分のコスト比較
infracost diff --path . --compare-to infracost-base.json

# CI/CDパイプライン統合（GitHub Actions）
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

以下のリソースはコストインパクトが大きいため、作成時に必ずフラグを立てる：

| Resource | Typical Monthly Cost | Warning |
|----------|---------------------|---------|
| NAT Gateway (AWS) | $32+ per gateway + data processing | 1 per AZ × AZ数 |
| Transit Gateway | $36+ per attachment | VPC数に比例 |
| HA Database (non-prod) | 2× single instance | 開発環境に不要な場合が多い |
| GPU Instance | $500-$30,000+ | 利用時間ベースでスケジュール検討 |
| Interface VPC Endpoint | $7+ per endpoint per AZ | 多数のサービス × AZ数 |
| Cross-region data transfer | $0.02/GB | 予想外に高額になりやすい |
| AlloyDB / Spanner (GCP) | $500+/month | 小規模には過剰 |
| Premium SSD (Azure) | 2-3× Standard SSD | IOPS要件を確認 |

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

**注意:** 料金は頻繁に変更される。最新価格は各クラウドプロバイダーの料金ページで確認すること。
