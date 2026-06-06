# Canary Scope Design Reference

Purpose: Design canary cohort selection, metric gates, ramp schedule, observation windows, and auto-promote / auto-abort thresholds for a proposed change. Produces a canary plan that couples blast-radius estimates with SLO-driven decision gates.

## Scope Boundary

- **ripple `canary-scope`**: Canary cohort, metric gates, ramp schedule, auto-promote/abort thresholds (this document).
- **ripple `blast-radius` (elsewhere)**: Production blast quantification. Feeds SEV tier → determines conservativeness of canary.
- **ripple `rollback-plan` (elsewhere)**: Reversibility contract. Canary auto-abort triggers the rollback plan.
- **Experiment (elsewhere)**: A/B test design and guardrail metrics. Canary is risk-limited rollout; Experiment is hypothesis validation. Avoid overlap by clarifying intent (risk-limit vs learning).
- **Launch (elsewhere)**: Release execution. This recipe supplies the canary *plan*; Launch executes the *rollout*.
- **Beacon (elsewhere)**: SLO burn-rate alerts. Canary gates consume Beacon's SLO definitions.

## Workflow

```
SCOPE      →  read blast-radius output (SEV tier, customers, data class)
           →  pick canary philosophy: risk-limit | progressive | dark-launch

COHORT     →  design cohort: % traffic | tenant allowlist | region | device
           →  exclude high-risk cohorts (top tenants, regulated regions) from early stages

GATES      →  pick metric gates: SLO (latency, error rate) + business KPI
           →  define auto-promote criteria (thresholds green for observation window)
           →  define auto-abort criteria (thresholds red within window)

SCHEDULE   →  stage ramp: 1% → 5% → 25% → 50% → 100%
           →  observation window per stage: max(1h, cohort-to-statistical-power)
           →  business-hours vs 24h window based on risk

VERIFY     →  pre-ramp checklist: flags armed, alerts armed, rollback rehearsed
           →  mid-ramp review: on-call awareness, no lingering high-severity alerts

PROMOTE    →  auto-promote on green gates + manual approval per SEV tier
           →  auto-abort + rollback on red gates

POST       →  post-100% observation window (48-72h) before treating as stable
           →  hand off to standard SRE monitoring
```

## Canary Philosophy Selection

| Philosophy | Use When | Cohort Shape |
|-----------|----------|--------------|
| Risk-limit canary | Change is customer-visible, SEV2+ potential | Small % → gradual ramp → 100% |
| Progressive rollout | Platform migration, infra change | Region-by-region or cluster-by-cluster |
| Dark launch | New feature, want live traffic without user exposure | Traffic duplicated to new code, responses discarded |
| Shadow / mirror | Validate new backend against old | Real traffic → both systems → diff detection |
| Blue-green | Stateless, atomic cut-over possible | Two environments, 0% → 100% swap |

Anti-pattern: applying progressive-ramp philosophy to a SEV4 internal-only change (unnecessary overhead); applying blue-green to a stateful migration (impossible).

## Cohort Selection

```
Preferred cohort order (early stages):
1. Internal users (dogfood)
2. Beta / opt-in customers
3. Free-tier / non-enterprise
4. Specific non-critical region
5. Specific plan tier (excluding enterprise)

Delay these until confidence is high:
- Top-10 enterprise tenants (contract SLA risk)
- Regulated regions (compliance risk)
- High-volume tenants (>5% traffic share)
- Paying customers in SLA window
```

### Cohort Selection Rules

1. **Exclude top tenants until ≥50% ramp**. One enterprise customer outage is often worse than 20% of free tier.
2. **Exclude regulated regions until full validation**. GDPR/HIPAA notification obligations make partial rollback costly.
3. **Include diverse platforms early** (mobile + web + API). Platform-specific bugs surface faster.
4. **Time-based exclusion**: avoid peak business hours for initial stages (but observe business hours at least once before 100%).

## Metric Gates

### SLO Gates (hard stops)

| Metric | Abort Threshold | Promotion Threshold |
|--------|----------------|---------------------|
| Error rate (5xx) | > 1% OR > baseline × 3 | ≤ baseline ± 10% |
| Latency P95 | > target × 1.5 | within target |
| Latency P99 | > target × 2 | within target × 1.2 |
| SLO burn | > 2x monthly budget in 1h | normal burn |

### Business KPI Gates (soft stops — pause + investigate)

| Metric | Pause Threshold | Notes |
|--------|----------------|-------|
| Conversion rate | drop ≥ 20% vs control | Check stat sig before promoting |
| Session count | drop ≥ 15% | May indicate feature-breaking bug |
| Revenue per session | drop ≥ 10% | Hand off to Experiment for depth analysis |
| Support tickets | spike ≥ 3x | Manual abort candidate |

### Guardrail Metrics (always-on)

| Metric | Always Must Hold |
|--------|-----------------|
| P95 latency on checkout | ≤ business-critical SLO |
| Auth success rate | ≥ 99.95% |
| Data integrity checks | 0 divergence events |
| Security events | 0 new anomalies |

## Ramp Schedule Templates

### Conservative (SEV1-2 risk, high blast)

```
1%   →   24h observation
5%   →   24h
10%  →   24h
25%  →   24h
50%  →   24h (include peak hours)
100% →   72h soak before "stable"
Total: ~7-9 days
```

### Standard (SEV3 risk, moderate blast)

```
1%   →  2h
5%   →  2h
25%  →  4h (include at least one business peak)
50%  →  4h
100% →  24h soak
Total: ~36h
```

### Fast (SEV4, low-risk, internal)

```
10%  →  1h
50%  →  1h
100% →  4h soak
Total: ~6h
```

### Emergency fix (escalation from incident)

```
25%  →  15min
100% →  1h soak
Total: ~1h15m (because not deploying is worse)
```

## Observation Window Sizing

Each stage needs enough observation time to hit statistical power on the canary metrics:

```
window_min = max(
  1 hour,
  sample_size_for_stat_sig / traffic_at_stage_qps,
  one_business_peak_per_stage_after_10%
)
```

Rule of thumb: if traffic < 10 QPS at a stage, you need ≥4h to detect anything below a 50% degradation. Scale up traffic before scaling observation expectations.

## Auto-Promote and Auto-Abort Automation

```yaml
canary_plan:
  name: "[change name]"
  stages:
    - percentage: 1
      cohort:
        include: [internal, beta_opt_in]
        exclude: [top_tenants, regulated_regions]
      observation_window: 2h
      auto_promote:
        require_all:
          - error_rate_5xx < 1% for entire window
          - latency_p95 < target_p95 * 1.5
          - slo_burn within monthly budget
          - no new security alerts
      auto_abort:
        trigger_any:
          - error_rate_5xx > 1%
          - latency_p99 > target_p99 * 2
          - slo_burn > 2x monthly budget
          - 3+ distinct customer reports
      manual_approval: false
    - percentage: 5
      # ... similar, tighter thresholds
      manual_approval: false
    - percentage: 25
      manual_approval: true
      approval_owner: "[team lead]"
    - percentage: 100
      manual_approval: true
      post_observation: 72h
      stable_criteria:
        - 0 rollbacks
        - 0 SEV1/2 incidents
        - SLO burn normal

  rollback:
    trigger: "see ripple rollback-plan"
    tor_target: 5min
    responsible: "[on-call team]"
```

## Canary Scope Report Template

```markdown
## Canary Scope Plan

### Context
- **Change**: [name]
- **Blast radius**: [see blast-radius report]
- **SEV tier**: [SEV1-4]
- **Rollback plan**: [see rollback-plan output]

### Philosophy
- **Type**: [risk-limit / progressive / dark-launch / shadow / blue-green]
- **Rationale**: [why this philosophy]

### Cohort Design
- **Include early**: [list]
- **Exclude until stage X**: [list]
- **Full 100% gate conditions**: [list]

### Ramp Schedule
| Stage | % | Cohort | Window | Manual Approval |
|-------|---|--------|--------|-----------------|
| 1 | 1% | [cohort] | 2h | no |
| 2 | 5% | ... | ... | ... |

### Metric Gates
- **SLO gates** (hard stops): [list]
- **Business KPI gates** (soft stops): [list]
- **Guardrail metrics**: [list]

### Auto-Promote / Auto-Abort
- **Automation platform**: [LaunchDarkly / Argo Rollouts / Flagger / manual]
- **Auto-promote conditions**: [list]
- **Auto-abort conditions**: [list]
- **Abort → rollback ToR target**: [see rollback-plan]

### Pre-Launch Checklist
- [ ] Feature flag armed
- [ ] Beacon alerts configured at each threshold
- [ ] Rollback rehearsed in staging
- [ ] On-call brief written (SEV1/2 only)
- [ ] Status page pre-draft (SEV1/2 only)
- [ ] Customer comms template ready (enterprise cohort)

### Post-100% Stability Criteria
- [ ] [72h / as specified] soak with 0 rollbacks
- [ ] 0 SEV1/2 incidents
- [ ] SLO burn normalized
- [ ] Business KPIs within ± [X%] of control
- [ ] Moved to standard SRE monitoring

### Handoffs
- [ ] Launch (execution)
- [ ] Beacon (SLO alerts + dashboards)
- [ ] Experiment (if hypothesis-validating overlap)
- [ ] Triage (on-call brief for SEV1/2)
```

## Common Pitfalls

| Pitfall | Why it breaks | Fix |
|---------|--------------|-----|
| Canary without business KPI gate | SLO can be green while conversion drops silently | Add at least one revenue / engagement KPI |
| Skipping peak-hour observation | Issues only appear under load | Ensure at least one stage spans a business peak |
| Including top tenants in stage 1 | Enterprise outage worse than stats gains | Exclude top tenants until ≥50% |
| Too fast ramp for SEV2 change | Insufficient signal to detect degradation | Use conservative template |
| No auto-abort wired | Relies on on-call vigilance | Automate thresholds via Argo Rollouts / Flagger |
| Canary without corresponding rollback plan | Abort path undefined | Pair every canary with rollback-plan output |

## Deliverable Contract

When `canary-scope` completes, emit:

- **Canary philosophy** with rationale.
- **Cohort design** (include/exclude rules for each stage).
- **Ramp schedule** (% × cohort × window × approval per stage).
- **Metric gates** (SLO + business KPI + guardrail) with thresholds.
- **Auto-promote and auto-abort conditions** (automation-platform-specific).
- **Pre-launch checklist**.
- **Post-100% stability criteria**.
- **Handoffs**: Launch, Beacon, Experiment (if overlap), Triage.

## References

- Martin Fowler — "BlueGreenDeployment", "ParallelChange", "CanaryRelease"
- Argo Rollouts documentation (metric analysis, progressive delivery)
- Flagger (CNCF) progressive delivery patterns
- Google SRE Workbook — "Canarying Releases"
- LaunchDarkly, Statsig — Feature flag canary patterns
- Gergely Orosz — Progressive rollout case studies
