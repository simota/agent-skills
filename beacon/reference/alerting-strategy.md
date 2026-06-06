# Alerting Strategy Reference

Alert hierarchy design, runbooks, and escalation policy reference.

---

## Alert Hierarchy

### Severity Levels

| Severity | Response Time | Who | Action |
|----------|-------------|-----|--------|
| **P1 Critical** | 5 min | On-call engineer | Page immediately, war room |
| **P2 High** | 30 min | On-call engineer | Page during business hours, notify off-hours |
| **P3 Medium** | 4 hours | Team | Ticket, investigate during business hours |
| **P4 Low** | 1 week | Team | Ticket, batch with other work |

### Alert Categories

| Category | Signal | Example |
|----------|--------|---------|
| **SLO burn rate** | Error budget consumption | 14.4× burn rate in 1h |
| **Symptom** | User-visible impact | 5xx error rate > 1% |
| **Cause** | Infrastructure signal | CPU > 90% for 10min |
| **Capacity** | Resource exhaustion trending | Disk 80% and growing |
| **Security** | Threat indicators | Auth failure spike |

### Symptom vs Cause Alerts

```
PREFER symptoms (user impact):
  ✅ "API error rate > 1% for 5 minutes"
  ✅ "Checkout latency p99 > 2s for 10 minutes"

AVOID causes alone (noisy, miss novel failures):
  ❌ "CPU > 90%" (might be fine during expected batch)
  ❌ "Pod restarted" (might recover automatically)

BEST: Symptom alert pages, cause alert adds context:
  🎯 Page: "Payment success rate < 99%"
  📎 Context: "Database connection pool exhausted"
```

---

## Alert Design Principles

| Principle | Description |
|-----------|-------------|
| **Actionable** | Every alert has a clear response action |
| **Relevant** | Alerts route to the team that can fix the issue |
| **Timely** | Detection windows match urgency |
| **Unique** | No redundant alerts for the same issue |
| **Quiet** | Alert only when human action is needed |

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Alert fatigue** | Too many alerts, ignoring starts | Reduce to actionable only |
| **Missing runbook** | Engineer doesn't know what to do | Attach runbook to every alert |
| **Flapping** | Alert fires and resolves rapidly | Add hysteresis / for-duration |
| **Cascade** | One failure triggers 20 alerts | Use alert grouping/inhibition |
| **Stale alerts** | Alert for decommissioned service | Quarterly alert review |

### Alert Quality KPIs

```
Signal-to-Noise Ratio:
  actionable_alerts / total_alerts
  Target: > 30% (industry benchmark)

SLO-based alerting impact:
  - Reduces alert volume by ~85% vs threshold-based
  - Only 3% of typical threshold alerts need immediate action

Alert hygiene checklist (quarterly):
  [ ] Identify alerts with zero actions in past 30 days -> delete/adjust
  [ ] Migrate threshold alerts to SLO burn rate alerts
  [ ] Eliminate duplicate alerts for same symptom
  [ ] Separate after-hours alerts that can wait for business hours
  [ ] Measure "wolf-boy rate" (false positive rate, target: < 5%)
  [ ] Dynamic baselines for metrics with known patterns (e.g. daily CPU cycles)
```

### Multi-Window Multi-Burn-Rate Alerting (2026 default)

Google SRE's *Alerting on SLOs* recipe is the 2026 baseline for SLO-driven paging. Each rule pairs a **long window** that catches sustained burn with a **short window** that confirms the issue is current rather than historical residue. Three tiers cover the budget spectrum:

| Tier | Long window | Short window | Long burn rate | Short burn rate | Budget consumed | Action |
|------|-------------|---------------|------------------|------------------|------------------|--------|
| Page | `1 h` | `5 m` | `> 14.4` | `> 14.4` | `~2%` of monthly budget in `1 h` | P1 page |
| Ticket | `6 h` | `30 m` | `> 6` | `> 6` | `~5%` of monthly budget in `6 h` | P2 ticket, work within business hours |
| Trend | `3 d` | `6 h` | `> 1` | `> 1` | `~10%` of monthly budget in `3 d` | Weekly review, prioritise reliability work |

Implementation rules:

- The short window guards against alerts that linger long after the incident has cleared — both windows must be over the threshold to fire.
- Tune *thresholds*, not the windows. Window lengths are derived from the desired detection time vs the SLO horizon (monthly / quarterly) and should change only when the SLO horizon does.
- Pair every paging rule with a *3-day trend* rule that does not page — it is the early-warning signal that the team is eating its budget and operational work needs to be reprioritised.
- Symptom-based SLIs (request error rate, request latency p99, business-outcome success rate) drive the burn rate. Cause metrics (CPU, GC pause, pool saturation) are diagnostic context that *attaches* to the page, never the page itself.

---

## Runbook Template

```markdown
# Runbook: [Alert Name]

## Alert Description
[What this alert means in plain language]

## Impact
- **User impact**: [How users are affected]
- **Business impact**: [Revenue/reputation risk]

## Diagnosis Steps
1. Check [dashboard link] for error patterns
2. Run `kubectl get pods -n <namespace>` to check pod health
3. Check recent deployments: `kubectl rollout history`
4. Review logs: `kubectl logs -l app=<service> --tail=100`

## Remediation
### Quick Fix (< 5 min)
- Restart pods: `kubectl rollout restart deployment/<name>`
- Scale up: `kubectl scale deployment/<name> --replicas=<N>`

### Root Cause Fix
- [Steps to investigate and resolve the underlying issue]

## Escalation
- **If unresolved after 15 min**: Escalate to [team/person]
- **If data loss suspected**: Page database team immediately

## Related
- Dashboard: [link]
- SLO: [link]
- Architecture doc: [link]
```

---

## Escalation Policy

### Escalation Chain

```
Level 1 (0-15 min):   Primary on-call engineer
Level 2 (15-30 min):  Secondary on-call engineer
Level 3 (30-60 min):  Team lead / Engineering manager
Level 4 (60+ min):    VP Engineering / CTO (for P1 only)
```

### On-Call Rotation Best Practices

| Practice | Recommendation |
|----------|---------------|
| **Rotation length** | 1 week (handoff on weekday morning) |
| **Team size** | Minimum 4 for sustainable rotation |
| **Handoff** | Document active incidents, recent changes |
| **Compensation** | On-call stipend + incident response pay |
| **Post-incident** | Blameless postmortem within 48h |

---

## Notification Routing

| Channel | Use For | Example Tools |
|---------|---------|--------------|
| **PagerDuty/OpsGenie** | P1/P2 pages | Phone call, SMS, push |
| **Slack #incidents** | P1/P2 war room | Real-time coordination |
| **Slack #alerts** | P3/P4 notifications | Awareness, triage |
| **Email** | Weekly summary | Trend reports |
| **Ticket system** | P3/P4 tracking | Jira, Linear |

### Alert Routing Rules

```yaml
routes:
  - match:
      severity: critical
      service: payments
    receiver: payments-oncall-page
    continue: false

  - match:
      severity: warning
    receiver: team-slack-alerts
    group_by: [alertname, service]
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4h
```
