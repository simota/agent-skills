# Reliability Review Reference

Production readiness checklists, FMEA, and game day planning reference.

---

## Production Readiness Review

### Pre-Launch Checklist

```markdown
## Service: [name]  |  Review Date: [date]

### Observability
- [ ] SLOs defined and dashboards created
- [ ] Alerts configured with runbooks
- [ ] Distributed tracing instrumented
- [ ] Structured logging with correlation IDs
- [ ] Error tracking integrated (Sentry, etc.)

### Reliability
- [ ] Health check endpoints (/healthz, /ready)
- [ ] Graceful shutdown handling
- [ ] Circuit breakers for external dependencies
- [ ] Retry with exponential backoff + jitter
- [ ] Timeout configured for all external calls
- [ ] Rate limiting on public endpoints

### Scalability
- [ ] Horizontal scaling tested
- [ ] Auto-scaling configured and validated
- [ ] Load test results within SLO at 2× expected peak
- [ ] Database connection pooling configured
- [ ] Stateless design (no local state dependencies)

### Deployment
- [ ] Rollback procedure documented and tested
- [ ] Canary/blue-green deployment configured
- [ ] Feature flags for risky changes
- [ ] Database migrations are backwards-compatible
- [ ] Zero-downtime deployment verified

### Security
- [ ] Authentication/authorization implemented
- [ ] Secrets managed via vault/secret manager
- [ ] TLS for all external communication
- [ ] Input validation on all public endpoints
- [ ] Dependency vulnerability scan clean

### Disaster Recovery
- [ ] Backup strategy documented and tested
- [ ] Recovery time objective (RTO) defined
- [ ] Recovery point objective (RPO) defined
- [ ] Failover procedure documented
- [ ] Data retention policy configured
```

---

## FMEA (Failure Mode and Effects Analysis)

### FMEA Template

| Component | Failure Mode | Effect | Severity (1-10) | Probability (1-10) | Detection (1-10) | RPN | Mitigation |
|-----------|-------------|--------|----------|------------|-----------|-----|------------|
| Database | Connection pool exhausted | API 500 errors | 9 | 4 | 3 | 108 | Pool monitoring + auto-scaling |
| Cache | Full eviction | Latency spike, DB overload | 7 | 3 | 5 | 105 | Capacity alert + eviction policy |
| Auth service | Unavailable | All requests fail | 10 | 2 | 2 | 40 | Cache tokens + circuit breaker |
| Message queue | Consumer lag | Delayed processing | 6 | 5 | 4 | 120 | Lag alert + auto-scaling consumers |

### RPN (Risk Priority Number)

```
RPN = Severity × Probability × Detection

RPN Thresholds:
  > 200: Critical — Immediate action required
  100-200: High — Plan mitigation this sprint
  50-100: Medium — Backlog item
  < 50: Low — Accept risk, monitor
```

### Severity Scale

| Score | Impact |
|-------|--------|
| 1-2 | Minimal — No user impact |
| 3-4 | Minor — Degraded experience for few users |
| 5-6 | Moderate — Feature unavailable |
| 7-8 | Major — Core functionality impacted |
| 9-10 | Critical — Complete service outage, data loss |

---

## Game Day Planning

### Game Day Template

```markdown
## Game Day: [Scenario Name]
**Date**: [date]  |  **Duration**: 2-4 hours

### Objective
Test the system's response to [failure scenario] and validate
our detection, response, and recovery procedures.

### Hypothesis
When [failure is injected], we expect:
1. Alert fires within [X] minutes
2. On-call identifies the issue within [X] minutes
3. Automated remediation triggers within [X] minutes
4. Service recovers within [X] minutes
5. SLO remains within budget

### Scenario
1. **Pre-conditions**: [system state before injection]
2. **Injection**: [what failure to inject]
3. **Expected behavior**: [what should happen]
4. **Abort criteria**: [when to stop if things go wrong]

### Safety Controls
- [ ] Staging environment or isolated production segment
- [ ] Kill switch available to stop injection
- [ ] All participants know abort procedure
- [ ] Customer impact limited to < X%
- [ ] Rollback plan ready

### Participants
| Role | Person | Responsibility |
|------|--------|---------------|
| Game Master | [name] | Inject failures, control scenario |
| Observer | [name] | Document timeline and decisions |
| On-call | [name] | Respond as if real incident |
| Comms | [name] | Handle stakeholder communication |

### Post-Game Review
- [ ] Timeline documented
- [ ] Hypothesis validated or invalidated
- [ ] Gaps identified and action items created
- [ ] Runbooks updated based on findings
- [ ] Follow-up game day scheduled if needed
```

### Common Game Day Scenarios

| Scenario | Injection Method | Tests |
|----------|-----------------|-------|
| **Dependency failure** | Block network to dependency | Circuit breaker, fallbacks |
| **Zone failure** | Drain one AZ | Multi-AZ failover |
| **Database failover** | Trigger primary failure | Replica promotion, connection recovery |
| **Traffic spike** | Load generator at 3× peak | Auto-scaling, rate limiting |
| **Disk full** | Fill disk to 95% | Alerting, auto-cleanup |
| **Certificate expiry** | Use near-expiry cert | Monitoring, auto-renewal |
| **DNS failure** | Modify DNS resolution | DNS caching, fallback |
