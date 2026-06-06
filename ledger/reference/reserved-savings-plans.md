# Reserved Instances & Savings Plans Reference

Purpose: Subcommand-scoped methodology for evaluating cloud commitment products — AWS RI (Standard / Convertible), AWS Savings Plans (Compute / EC2 Instance / SageMaker), GCP Committed Use Discounts, and Azure Reserved VM Instances. Produces a coverage-target plan, break-even analysis, and rolling commitment ladder calibrated to steady-state usage. Optimizes for blended discount net of unused-commitment risk, not headline percentage.

## Scope Boundary

- **ledger `ri-sp`**: commitment strategy across RI / SP / CUD / Azure RI. Coverage tiering, break-even modeling, expiration ladder, conversion / exchange playbook.
- **ledger `estimate` (default, elsewhere)**: forward-looking cost projection from IaC. Feeds steady-state baseline into `ri-sp` but does not own commitment decisions.
- **ledger `rightsizing` (elsewhere)**: instance-shape correctness from utilization. Run `rightsizing` BEFORE `ri-sp` — committing to oversized instances locks in waste for 1-3 years.
- **ledger `anomaly` (elsewhere)**: detects unused-commitment drops and coverage cliffs as anomalies; `ri-sp` owns the design of corrective re-purchase or exchange.
- **scaffold (elsewhere)**: applies SP-aligned IaC changes (instance family pinning for EC2 SP). `ri-sp` recommends; Scaffold provisions.
- **beacon (elsewhere)**: SLO-aware capacity context. Steady-state baseline must respect SLO headroom — `ri-sp` consumes Beacon's capacity floor, not raw averages.
- **comply (elsewhere)**: financial-control audit (procurement approval, segregation of duties for >$10K commitments). `ri-sp` produces the artifact; Comply audits the trail.

## Workflow

```
INTAKE     →  identify scope (account/org), cloud(s), workload class (general/GPU/DB)
           →  collect 30-90d usage at hourly granularity; flag <30d as INSUFFICIENT

BASELINE   →  compute steady-state floor (p10 hourly usage over trailing 90d)
           →  separate by family/region/OS/tenancy — commitments are scoped, averages lie

MODEL      →  for each commitment product: discount %, term, payment, flexibility, exchange rules
           →  compute break-even hours, blended effective rate, unused-commitment exposure

LADDER     →  stagger expirations across quarters to avoid cliff renewal
           →  start with 1yr No-Upfront SP for baseline; layer RI for predictable shapes

DECIDE     →  recommend coverage tier per workload (see thresholds table)
           →  document assumptions, confidence, rollback path (exchange / sell on Marketplace)

HANDOFF    →  Scaffold: IaC pinning for EC2 SP; Beacon: utilization SLO for commitments;
           →  Atlas: org-level commitment portfolio view
```

## Vendor Comparison

| Product | Discount range | Term | Flexibility | Exchange | Best for |
|---------|---------------|------|-------------|----------|----------|
| AWS Standard RI | 40-72% | 1y / 3y | Family/size/AZ via modify | Sell on RI Marketplace | Stable, single-region workloads |
| AWS Convertible RI | 30-66% | 1y / 3y | Exchange across families | Yes (no resale) | Evolving instance choices |
| AWS Compute SP | 30-66% | 1y / 3y | Any region, family, OS, tenancy, Fargate, Lambda | No resale | Mixed compute portfolios |
| AWS EC2 Instance SP | 35-72% | 1y / 3y | Family-scoped, region-pinned | No | Stable family but size-flexible |
| AWS SageMaker SP | up to 64% | 1y / 3y | SageMaker only (training/inference/notebooks) | No | ML platforms on SageMaker |
| GCP CUD (Resource) | up to 57% | 1y / 3y | Project / region scoped | Limited | Steady GCE / GKE / Cloud SQL |
| GCP CUD (Spend-based) | up to 28% | 1y / 3y | Service-wide | No | Variable shape, stable spend |
| Azure Reserved VM | up to 72% | 1y / 3y | Scope: shared / single / RG | Exchange / refund (caps) | Predictable Azure VMs |
| Azure Savings Plan | up to 65% | 1y / 3y | Compute-wide hourly commit | No | Mixed Azure compute |

## Coverage Targets by Workload Class

| Workload class | Recommended coverage | Product preference | Term | Rationale |
|----------------|---------------------|--------------------|------|-----------|
| Stateless web (steady) | 70-85% | Compute SP | 1y NU | High predictability, SP flexibility absorbs family drift |
| Stateful DB (RDS/Cloud SQL) | 80-95% | RI / CUD (resource) | 1y NU then 3y | Migration risk locks shape; high discount justifies term |
| Batch / async | 30-50% | Compute SP + Spot | 1y NU | Spot covers burst; SP covers floor |
| Dev / staging | 0-20% | None or short SP | 1y NU | Schedulable; commitments waste off-hours |
| GPU training | 20-40% (baseline only) | RI for floor + Spot | 1y NU | Models churn; Spot dominates burst |
| GPU inference (real-time) | 60-80% | RI / Compute SP | 1y NU | Latency-bound, predictable |
| Serverless (Lambda/Fargate) | 50-70% | Compute SP | 1y NU | SP covers Lambda + Fargate uniformly |

## Break-Even & Risk Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Steady-state utilization (commitment hours used) | >= 80% | Healthy |
| Steady-state utilization | 60-80% | Watch — consider downsize at renewal |
| Steady-state utilization | < 60% | Unhealthy — initiate exchange / Marketplace sale |
| Break-even point (1y NU) | ~7 months | Below 7mo usage = on-demand cheaper |
| Break-even point (3y NU) | ~20 months | Reserve only if confidence on workload >= 24mo |
| Single-purchase commitment | > $10K/mo | Require executive approval (Core Contract) |
| 3-year term | any | Require executive approval (Core Contract) |
| Coverage concentration | < 40% of fleet | Increase floor coverage |
| Coverage concentration | > 90% of fleet | Reduce — peak burst goes on-demand cheaper |

## Anti-Patterns

- Committing without 30+ days of usage data — RI/SP decisions are 1-3 year contracts; under 30 days hides weekly seasonality and one-off events. Fail closed: no commitment, run on-demand.
- Buying 3-year terms without executive approval — irreversible obligation that survives team turnover and architecture migrations. Default to 1-year ladders unless explicitly authorized.
- Optimizing for headline discount % over blended effective rate — a 72% discount at 50% utilization is worse than a 40% discount at 95% utilization. Always compute effective rate = discount × utilization.
- Concentrating expirations in a single month — creates a renewal cliff where one bad week of usage data drives the entire portfolio. Stagger across quarters.
- Treating Convertible RIs as flexible enough to skip planning — they exchange but never resell; a wrong family bet locks capital for the term. Plan first, convert as a recovery path, not a strategy.
- Applying general-compute coverage targets to GPU workloads — model churn and instance-type velocity (H100 -> H200 -> B200) make 3-year GPU commitments high-risk. Cap GPU at 1-year and 20-40% baseline.
- Ignoring AZ / region scope — Standard RIs scoped to a single AZ provide capacity reservation but lose flexibility; if workload moves AZ, the discount evaporates. Default to regional scope unless capacity reservation is the goal.
- Buying Compute SP and EC2 Instance SP for the same fleet without ordering — SP application order applies the highest discount first; layered purchases can leave Compute SP underutilized. Model the application waterfall.
- Forgetting Marketplace / exchange as rollback — over-commitment is recoverable: AWS Standard RI Marketplace, Convertible exchange, Azure refund (capped). Document rollback path in every recommendation.

## Handoff

- **To Scaffold**: instance-family pinning for EC2 Instance SP coverage; tag policy for commitment-scoped resources; IaC change list with cost delta.
- **To Beacon**: commitment-utilization SLO (target >= 80%, alert at < 70% for 7 days) + cost-anomaly rule for sudden coverage drop.
- **To Atlas**: org-level commitment portfolio map — which accounts hold which commitments, expiration calendar, blended effective rate by BU.
- **To Ledger `anomaly`**: feed expiration calendar so coverage-cliff events surface as predictable anomalies, not surprises.
- **To Comply**: procurement-approval evidence for >$10K/mo or 3-year commitments; segregation-of-duties audit trail.
