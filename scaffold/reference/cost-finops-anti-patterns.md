# Cost Management / FinOps Anti-Patterns

Purpose: Use this file when reviewing over-provisioning, commitments, tagging, budgets, or FinOps operating model risks.

Contents:
1. Cost anti-patterns
2. FinOps operating pitfalls
3. Commitment pitfalls
4. Resource optimization pitfalls
5. Budget pitfalls

## Cost Anti-Patterns

| ID | Anti-pattern | Signal | Safer pattern |
|----|--------------|--------|---------------|
| `CO-01` | Over-Provisioning | CPU `<20%` and memory `<30%` on steady workloads | right-size after usage review |
| `CO-02` | Zombie Resources | unattached disks, unused EIPs, empty LBs | scheduled cleanup |
| `CO-03` | No Tagging Strategy | ownership and cost allocation are unclear | required cost tags |
| `CO-04` | Commitment Misalignment | long commitments ignore roadmap changes | align commitments to platform roadmap |
| `CO-05` | NAT Gateway Cost Explosion | NAT is a top line item | endpoints, private access, topology review |
| `CO-06` | Data Transfer Blindness | cross-AZ/region transfer surprises the bill | map transfer paths explicitly |
| `CO-07` | Environment Always-On | non-prod runs `24/7` without need | scheduled shutdown / scale-to-zero |

## FinOps Operating Pitfalls

- finance / engineering / operations work in silos
- cost management is reactive instead of continuous
- optimization is manual and infrequent
- only part of the estate has cost visibility
- cost cutting ignores business impact

## Commitment Pitfalls

| ID | Anti-pattern | Safer pattern |
|----|--------------|---------------|
| `CM-01` | All-or-Nothing Commitment | commit around `60-70%`, keep the rest flexible |
| `CM-02` | Long-Term Lock Without Roadmap | start with shorter or more flexible commitments |
| `CM-03` | Instance-Family Lock-In | prefer broader Compute Savings Plans when flexibility matters |
| `CM-04` | No Coverage Tracking | monitor utilization and coverage weekly |

## Resource Optimization Pitfalls

- CPU-only right-sizing
- Spot without fallback
- ignoring storage tiering
- unlimited log retention
- uncompressed transfer where compression is feasible

## Budget Pitfalls

| ID | Anti-pattern | Safer pattern |
|----|--------------|---------------|
| `BU-01` | No Budget Alerts | staged alerts at `50/80/100/120%` |
| `BU-02` | Single Global Budget | budget by team, environment, and service |
| `BU-03` | No Cost Estimation Before Deploy | run cost estimation in PR / plan flow |
| `BU-04` | Historical-Only Forecasting | include launch/campaign roadmap in forecasts |
