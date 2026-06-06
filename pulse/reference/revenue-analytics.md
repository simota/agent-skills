# Revenue Analytics

## Core SaaS Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **MRR** | Sum of active subscriptions | > 5% MoM growth |
| **ARR** | MRR x 12 | Benchmark comparison |
| **ARPU** | MRR / Active paying users | Increasing trend |
| **LTV** | ARPU x Avg lifespan | LTV:CAC > 3:1 |
| **CAC** | Total spend / New customers | Decreasing trend |
| **Net Revenue Retention** | (MRR - Contraction - Churn + Expansion) / MRR | > 100% |

## NRR Benchmarks (2025 — multi-source synthesis)

Median private-SaaS NRR has degraded since 2022; achieving ≥100% is materially harder than in the ZIRP era. The most-cited 2025 cuts (synthesized across KeyBanc, OpenView, ChartMogul, Battery, Bessemer, High Alpha):

| Segment | NRR | Notes |
|---------|-----|-------|
| Top performers (overall median) | 104-106% | 2025 |
| Private SaaS (overall median) | 101-102% | Down from prior years |
| SMB-focused | 90-105% | Often <100% in 2025 |
| Mid-market | 100-115% | Stable |
| Enterprise | 115-125% | Expansion-driven |
| Pure-play enterprise software | 120-150% | Best-in-class >130% |
| "Concerning" zone | <100% | Net shrinking from existing customers |

Growth correlation (2025): companies with NRR ≥100% grew **~2x faster YoY** than peers below 100%. Use NRR as your most reliable forward indicator for revenue compounding.

Sources: [RockingWeb — 2025 SaaS metrics benchmark synthesis (2,000 cos)](https://www.rockingweb.com.au/saas-metrics-benchmark-report-2025/), [High Alpha — 2025 SaaS Benchmarks](https://www.highalpha.com/saas-benchmarks), [ChartMogul — SaaS Retention New Normal](https://chartmogul.com/reports/saas-retention-the-new-normal/), [Benchmarkit — 2025 SaaS Performance Metrics](https://www.benchmarkit.ai/2025benchmarks).

## MRR Movement Tracking

```typescript
interface MRRMovement {
  period: string;
  startMRR: number;
  newMRR: number;
  expansionMRR: number;
  contractionMRR: number;
  churnedMRR: number;
  reactivationMRR: number;
  endMRR: number;
}
```

## LTV Calculation Methods

### Simple: `ARPU / Churn Rate`
### Cohort-Based: Fit exponential decay curve to actual revenue data

## Churn Analysis SQL

```sql
SELECT cancellation_reason, COUNT(*) as count, SUM(mrr) as lost_mrr,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as pct
FROM cancellations
WHERE cancelled_at >= DATE_TRUNC(CURRENT_DATE, MONTH)
GROUP BY cancellation_reason ORDER BY lost_mrr DESC;
```

## At-Risk Account Scoring

Risk factors and weights:
- Usage decline (> 30% drop): +30 points
- Inactivity (> 14 days): +25 points
- Open support tickets (> 3): +20 points
- Low feature adoption (< 3 features): +15 points
- Low NPS (< 7): +10 points

Threshold: Score > 60 = At Risk
