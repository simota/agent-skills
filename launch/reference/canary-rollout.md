# Canary Rollout Reference

Purpose: Design progressive traffic-shifting deployments with guardrails. Defines per-stage traffic share, observation windows, automatic halt triggers, and promote/rollback decision rules.

## When to Use Canary

- New version carries non-trivial risk (user-facing change, cross-service protocol change, DB interaction change)
- SLO-protected service with measurable error/latency budget
- Traffic splitter available (Envoy, Istio, K8s service weights, ALB, CloudFront, LaunchDarkly percentage targeting)

**Skip canary and use blue-green** when:
- Traffic-splitting infra unavailable
- Change is all-or-nothing (schema migration)
- Rollback window tighter than smallest canary stage

## Standard Traffic Progression

### Default: 1% → 10% → 50% → 100%

| Stage | Traffic | Observation window | Why |
|-------|---------|-------------------|-----|
| 1 | 1% | 10 min | detect obvious errors without blast radius |
| 2 | 10% | 30 min | surface moderate issues, gather first SLO signal |
| 3 | 50% | 1 h | confirm infra scaling + cross-system effects |
| 4 | 100% | 2 h soak | full monitor period before calling success |

### Aggressive (trusted change / small service)

0% → 25% → 100%, 15 min per stage. Use only when historical confidence + rapid rollback both confirmed.

### Conservative (high-risk / regulated)

0.1% → 1% → 5% → 25% → 50% → 100%, 30 min+ per stage. Use for payments, billing, GDPR-adjacent flows.

## Guardrail Metrics

Every canary **must** monitor, per stage:

| Metric | Threshold (halt trigger) |
|--------|-------------------------|
| Error rate (5xx) | > 2× baseline for 5 min |
| p95 latency | > 150% baseline for 5 min |
| p99 latency | > 200% baseline for 5 min |
| SLO burn rate | > 2× normal burn for 10 min |
| Business metric (e.g., conversion) | < 95% baseline for 15 min |
| Resource (CPU / mem / connections) | > 85% capacity |
| Downstream dependency errors | any increase > 20% |

Define per-service baselines from the last 7-day rolling p50.

### Automatic Halt vs Human Approval

| Trigger | Action |
|---------|--------|
| Any guardrail breach ≥ 5xx > 5× baseline | **Auto-rollback** |
| Guardrail breach 2–5× baseline | **Auto-halt** (freeze traffic share, alert oncall) |
| Guardrail breach 1.5–2× | **Alert only**, human decides |
| All guardrails green | **Auto-promote** after observation window |

## Halt and Rollback Procedure

### Halt (freeze at current stage)

```bash
# Example: K8s service weighting
kubectl patch svc myservice -p '{"spec":{"selector":{"version":"stable"}}}'  # fall back to stable
# Or: Istio VirtualService weight: canary 0, stable 100
```

Halt is a **decision point**, not a final state. Within 15 min, oncall must choose:
- Rollback (revert to stable)
- Roll forward (fix + re-canary)
- Hold (extend observation with reduced risk)

### Rollback (full traffic back to stable)

```bash
# Route 100% → stable
# Stop canary deployment
# Run post-rollback verification (smoke tests)
# Notify stakeholders
```

Rollback SLO: ≤ 3 minutes from decision to traffic fully routed.

## Decision Matrix

For each stage transition:

| Metric state | Action |
|--------------|--------|
| All green for full window | Promote to next stage |
| Yellow (marginal drift, no threshold breach) | Extend observation 50%, then re-evaluate |
| Red on any guardrail | Halt + oncall decides |
| Red on multiple guardrails | Auto-rollback |

## Traffic Splitter Configuration Snippets

### Kubernetes + Istio

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
spec:
  http:
  - route:
    - destination:
        host: myapp
        subset: stable
      weight: 90
    - destination:
        host: myapp
        subset: canary
      weight: 10
```

### AWS ALB Weighted Target Groups

```
TargetGroup stable: weight 900
TargetGroup canary: weight 100
(ratio = 90:10)
```

### Argo Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
      - setWeight: 1
      - pause: { duration: 10m }
      - setWeight: 10
      - pause: { duration: 30m }
      - setWeight: 50
      - pause: { duration: 60m }
      - setWeight: 100
      analysis:
        templates:
        - templateName: error-rate-check
        args:
        - name: service-name
          value: myapp
```

### LaunchDarkly Percentage Rollout

```
Flag: new-checkout
Rule: percentage rollout
  canary: 1% → 10% → 50% → 100%
  (increment via scheduled releases)
```

## Per-Change-Type Recommendations

| Change type | Strategy |
|-------------|----------|
| API response field addition | Standard (1→10→50→100) |
| Algorithm / logic change | Conservative, compare outputs side-by-side |
| Performance optimization | Standard + performance-specific guardrails |
| Framework / runtime upgrade | Conservative, extended soak |
| Database client library upgrade | Conservative + connection-pool monitoring |
| New external API integration | Standard + downstream error guardrail |
| Infrastructure / deployment change | Blue-green preferred over canary |
| Schema migration | NOT a canary candidate — use dual-write pattern |

## Playbook Template

```markdown
# Canary Rollout: v2.15.0

**Service**: checkout-api
**Change**: new discount engine (PR #1234)
**Risk**: medium (logic change, conversion metric sensitive)

## Stages
| Stage | Traffic | Window | Auto-Promote Conditions |
|-------|---------|--------|-------------------------|
| 1 | 1% | 10 min | error rate < 0.2%, p95 < 220ms |
| 2 | 10% | 30 min | conversion ≥ 98% of 7d baseline |
| 3 | 50% | 60 min | all SLOs green |
| 4 | 100% | 2 h soak | no regressions reported |

## Guardrails
- Error rate (5xx): baseline 0.1%, halt at > 0.2%, rollback at > 0.5%
- p95: baseline 150ms, halt at > 225ms, rollback at > 300ms
- Conversion: baseline 4.8%, halt at < 4.6%, rollback at < 4.4%
- CPU: halt at > 85%

## Dashboards
- [Canary analysis dashboard](link)
- [Conversion funnel](link)

## Rollback
- Command: `argo rollouts abort checkout-rollout -n prod`
- SLO: ≤ 3 min
- Communication: #incidents + status page + PM notification

## Post-Success
- Close canary deployment
- Merge release commit to main-stable tag
- Update CHANGELOG + release notes (handoff Launch `notes`)
- Remove feature flag (if applicable, handoff Launch `flag`)
```

## Anti-Patterns

- Canary without guardrails (just traffic split, no automated halt)
- Observation window shorter than issue detection time (too fast to catch)
- All-or-nothing traffic jumps (0 → 100) disguised as canary
- Ignoring business metrics, only watching infra metrics
- Promoting on "no alerts" (absence of signal ≠ presence of success)
- Running canary during peak traffic (no baseline to compare to)
- No rollback rehearsal (first time using the rollback command is during an incident)
- Parallel canaries on unrelated changes (can't attribute cause when things break)
- Mutating shared state (DB rows) from canary version (corrupts data visible to stable)

## Handoffs

- **Beacon → Launch**: provides SLO baselines + dashboards
- **Gear → Launch**: implements traffic-splitting config
- **Guardian → Launch**: PR size + risk classification informs canary aggressiveness
- **Launch → Triage**: halt / rollback events escalate to incident commander
- **Launch → Harvest**: rollout summary for weekly report
