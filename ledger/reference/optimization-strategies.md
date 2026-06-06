# Optimization Strategies

**Purpose:** Right-sizing、RI/SP、Spot戦略、waste elimination の詳細手法。
**Read when:** コスト最適化の具体的な推奨が必要な時。

---

## Right-Sizing Framework

### Data Collection Requirements

| Metric | Minimum Period | Source |
|--------|---------------|--------|
| CPU utilization | 14 days | CloudWatch / Cloud Monitoring / Azure Monitor |
| Memory utilization | 14 days | CloudWatch Agent / custom metrics |
| Network throughput | 7 days | VPC Flow Logs / Cloud NAT logs |
| Disk IOPS | 7 days | EBS metrics / Persistent Disk metrics |
| GPU utilization | 7 days | NVIDIA DCGM / CloudWatch |

### Instance Family Selection Guide

| Workload Type | Recommended Family | Key Factor |
|--------------|-------------------|------------|
| General web/API | t3/t3a (AWS), e2 (GCP), B-series (Azure) | Burstable, cost-effective |
| Compute-intensive | c6i/c7g (AWS), c3 (GCP), F-series (Azure) | CPU-optimized |
| Memory-intensive | r6i/r7g (AWS), n2-highmem (GCP), E-series (Azure) | Memory-optimized |
| Storage-intensive | i3/i4i (AWS), n2-standard+local SSD (GCP), L-series (Azure) | NVMe local storage |
| ML training | p4d/p5 (AWS), a2/a3 (GCP), NC-series (Azure) | GPU |
| ML inference | inf2 (AWS), g2 (GCP), NC-series (Azure) | Cost-per-inference |

### Right-Sizing Decision Tree

```
CPU < 10% for 14d?
├── Yes → Is workload bursty?
│   ├── Yes → Switch to burstable (t3/e2/B-series)
│   └── No → Downsize 2 tiers
├── CPU 10-40%?
│   └── Downsize 1 tier, monitor 7d
├── CPU 40-70%?
│   └── Appropriate — no change
└── CPU > 70%?
    ├── Sustained → Scale up 1 tier
    └── Spiking → Add autoscaling
```

---

## Reserved Instance / Savings Plan Strategy

### AWS Commitment Options

| Option | Flexibility | Discount | Best For |
|--------|------------|----------|----------|
| Compute Savings Plan | Any instance family/region/OS | 40-66% | Baseline compute |
| EC2 Instance Savings Plan | Specific family in region | 50-72% | Predictable workloads |
| Standard RI | Specific instance type/AZ | 55-75% | Unchanging workloads |
| Convertible RI | Exchangeable | 40-55% | Long-term flexible |

### GCP Commitment Options

| Option | Flexibility | Discount | Best For |
|--------|------------|----------|----------|
| Committed Use Discount (CUD) | Specific machine family/region | 37-57% | Predictable VMs |
| Flex CUD | Cancelable after 1 year | 20-35% | Uncertain workloads |
| Sustained Use Discount | Automatic | 10-30% | Always-on VMs |

### Azure Commitment Options

| Option | Flexibility | Discount | Best For |
|--------|------------|----------|----------|
| Azure Savings Plan | Any compute | 35-65% | Flexible baseline |
| Reserved VM Instance | Specific VM size/region | 40-72% | Predictable VMs |
| Spot VMs | Evictable | Up to 90% | Fault-tolerant workloads |

### Coverage Analysis Template

```markdown
## Commitment Coverage Analysis

### Current State
- Total monthly compute spend: $X,XXX
- On-Demand: $X,XXX (N%)
- Existing commitments: $X,XXX (N%)
- Coverage gap: $X,XXX (N%)

### Recommendation
| Commitment Type | Term | Amount | Expected Savings |
|-----------------|------|--------|-----------------|
| Compute SP | 1yr No Upfront | $X,XXX/hr | $X,XXX/mo (N%) |
| EC2 RI | 1yr Partial | N × instance | $X,XXX/mo (N%) |

### Risk Assessment
- Break-even: N months
- Flexibility impact: [description]
- Rollback plan: [description]
```

---

## Spot / Preemptible Strategy

### Suitability Assessment

| Workload Characteristic | Spot Suitability | Strategy |
|------------------------|-----------------|----------|
| Stateless, horizontally scalable | High | Spot Fleet with diversification |
| Batch processing | High | Spot with checkpointing |
| CI/CD runners | High | Spot with on-demand fallback |
| Dev/test environments | High | Spot with scheduled hours |
| Stateful database | Low | Not recommended |
| Latency-sensitive API | Medium | Mixed fleet (on-demand base + Spot) |

### Interruption Handling

```yaml
SPOT_RESILIENCE:
  diversification:
    - Use 4+ instance types per pool
    - Spread across 3+ AZs
    - Mix generations (e.g., m5 + m6i + m7i)

  handling:
    - 2-minute warning handler (AWS)
    - Graceful shutdown hooks
    - Checkpoint/resume for long tasks
    - Automatic fallback to on-demand

  capacity_strategy:
    - lowest-price: Cost-optimized (risk of mass interruption)
    - capacity-optimized: Stability-optimized (recommended)
    - price-capacity-optimized: Balanced (AWS default)
```

---

## Waste Elimination Checklist

| Waste Type | Detection Method | Action |
|-----------|-----------------|--------|
| Idle instances (CPU < 5% for 7d+) | CloudWatch/Monitoring | Terminate or schedule |
| Unattached EBS/PD volumes | API scan | Snapshot + delete |
| Unused Elastic IPs / static IPs | API scan | Release |
| Orphaned snapshots (> 90d, no AMI) | Age-based scan | Delete |
| Over-provisioned RDS/Cloud SQL | Performance Insights | Downsize |
| Unused load balancers (0 targets) | API scan | Delete |
| Dev/staging running 24/7 | Tag + schedule scan | Implement schedules |
| Uncompressed S3/GCS lifecycle missing | Bucket policy scan | Add lifecycle rules |
| NAT Gateway with < 1GB/day | VPC flow logs | Consider VPC endpoints |
| Unused reserved capacity | Utilization report | Sell on marketplace / modify |
