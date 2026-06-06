# Cloud Pricing Models

**Purpose:** AWS/GCP/Azureのプライシングモデル比較とリファレンス。
**Read when:** マルチクラウドのコスト比較やプライシングモデル理解が必要な時。

---

## Pricing Model Comparison

### Compute

| Model | AWS | GCP | Azure |
|-------|-----|-----|-------|
| On-Demand | Per-second (60s min) | Per-second (1m min) | Per-minute |
| Spot/Preemptible | Up to 90% off, 2-min warning | Up to 91% off, 30s warning (Spot), 24h max (Preemptible) | Up to 90% off, 30s warning |
| Reserved (1yr) | 40-60% off | 37-57% CUD | 40-60% off |
| Reserved (3yr) | 55-75% off | 50-70% CUD | 55-72% off |
| Savings Plan | 40-66% compute flexibility | N/A (Flex CUD similar) | 35-65% compute flexibility |
| Sustained Use | N/A | Auto 10-30% off (after 25% of month) | N/A |
| Free Tier | 750h t2.micro/12mo | e2-micro always free | 750h B1s/12mo |

### Storage

| Type | AWS (S3) | GCP (GCS) | Azure (Blob) |
|------|----------|-----------|--------------|
| Standard | $0.023/GB | $0.020/GB | $0.018/GB |
| Infrequent Access | $0.0125/GB | $0.010/GB | $0.010/GB |
| Archive | $0.004/GB (Glacier) | $0.004/GB (Archive) | $0.002/GB (Archive) |
| Operations (per 1K) | $0.005 PUT, $0.0004 GET | $0.005 PUT, $0.0004 GET | $0.005 PUT, $0.0004 GET |

**注意:** 料金は頻繁に変更される。上記は参考値であり、最新価格は各プロバイダーで確認すること。

### Database

| Service | AWS | GCP | Azure |
|---------|-----|-----|-------|
| Managed RDBMS | RDS ($0.017-$0.96/h) | Cloud SQL ($0.015-$0.80/h) | Azure SQL ($0.015-$0.85/h) |
| Serverless RDBMS | Aurora Serverless v2 | AlloyDB (min $0.10/h) | Azure SQL Serverless |
| NoSQL | DynamoDB ($1.25/WCU, $0.25/RCU) | Firestore/Bigtable | Cosmos DB ($0.008/100 RU/s/h) |
| Cache | ElastiCache ($0.017-$0.90/h) | Memorystore ($0.016-$0.86/h) | Azure Cache ($0.022-$0.90/h) |

---

## Cost-Effective Architecture Patterns

### Pattern 1: Right-Sized Compute

```
ANTI-PATTERN:
  3 × m5.2xlarge (8 vCPU, 32 GB) → $830/mo
  Average CPU: 15%

OPTIMIZED:
  3 × t3.large (2 vCPU, 8 GB) + autoscaling → $180/mo
  Savings: $650/mo (78%)
```

### Pattern 2: Tiered Storage

```
ANTI-PATTERN:
  All data in S3 Standard → $2,300/mo (100 TB)

OPTIMIZED:
  Hot (10 TB): S3 Standard → $230/mo
  Warm (30 TB): S3 IA → $375/mo
  Cold (60 TB): S3 Glacier IR → $240/mo
  Total: $845/mo
  Savings: $1,455/mo (63%)
```

### Pattern 3: Serverless for Variable Workloads

```
ANTI-PATTERN:
  Always-on API server (m5.large) → $73/mo
  Average utilization: 5%

OPTIMIZED:
  Lambda + API Gateway → ~$15/mo (at low traffic)
  Savings: $58/mo (80%)

  NOTE: Serverless cost exceeds EC2 at ~10M requests/month
  Crossover analysis required for each workload
```

### Pattern 4: Data Transfer Optimization

```
ANTI-PATTERN:
  App in us-east-1, DB in eu-west-1
  Cross-region transfer: 500 GB/mo → $10/mo
  + Latency penalty

OPTIMIZED:
  Co-locate in same region
  Transfer cost: $0
  + Latency improvement
```

---

## Provider-Specific Cost Tools

### AWS

| Tool | Purpose | Cost |
|------|---------|------|
| Cost Explorer | Visualization, forecasting | Free |
| Budgets | Alert and governance | Free (first 2), $0.01/day after |
| Cost Anomaly Detection | ML-based anomaly alerts | Free |
| Compute Optimizer | Right-sizing recommendations | Free |
| Trusted Advisor | Best practice checks | Business/Enterprise support |

### GCP

| Tool | Purpose | Cost |
|------|---------|------|
| Cloud Billing | Cost tracking, budgets | Free |
| Billing Export to BigQuery | Custom analysis | BigQuery query costs |
| Recommender | Right-sizing, commitment | Free |
| Active Assist | ML-based optimization | Free |
| Looker Studio | Dashboarding | Free |

### Azure

| Tool | Purpose | Cost |
|------|---------|------|
| Cost Management | Visualization, budgets | Free |
| Advisor | Right-sizing, reservations | Free |
| Cost Alerts | Budget/anomaly/credit alerts | Free |
| Power BI | Advanced dashboarding | License required |

---

## Multi-Cloud Cost Comparison Checklist

新しいワークロードのクラウド選定時に使用：

```markdown
## Cost Comparison: [Workload Name]

| Factor | AWS | GCP | Azure | Weight |
|--------|-----|-----|-------|--------|
| Compute (monthly) | $X | $X | $X | 40% |
| Storage (monthly) | $X | $X | $X | 15% |
| Data transfer (monthly) | $X | $X | $X | 15% |
| Managed services (monthly) | $X | $X | $X | 20% |
| Support plan (monthly) | $X | $X | $X | 10% |
| **Weighted total** | **$X** | **$X** | **$X** | |

### Non-Cost Factors
- Existing expertise: [provider]
- Regulatory requirements: [constraints]
- Service availability: [specific services needed]
- Commitment discounts available: [details]
```
