# Triage Runbooks & Communication Reference

Runbook templates and stakeholder communication templates.

Purpose: Read this when Triage must draft stakeholder communications, assess severity, or run a database, API, or third-party service incident playbook.

Contents:
- `Communication Templates`: initial alert, status update, and resolution notice
- `Escalation Matrix`: notification rules by severity and risk
- `Runbook: Database Issue`: diagnostics, mitigations, and failover procedure
- `Runbook: API Outage`: diagnostics, mitigations, and rollback procedure
- `Runbook: Third-Party Integration`: vendor outage and degraded-mode handling
- `Severity Assessment Checklist`: structured severity calculation inputs

## Communication Templates

### Initial Notification (SEV1/SEV2)

```markdown
## Incident Alert - [SEV1/SEV2]

**Service:** [affected service/feature]
**Status:** Investigating / Identified / Mitigating

**Impact:**
[Brief description of user-facing impact]

**Current Actions:**
- [What's being done]

**Next Update:** [time]

**Incident Lead:** [name/handle]
```

### Status Update

```markdown
## Incident Update - [Incident ID]

**Status:** [Investigating / Identified / Mitigating / Resolved]

**Update:**
[What's changed since last update]

**Current Impact:**
[Current state of user impact]

**Next Steps:**
- [Planned action 1]
- [Planned action 2]

**ETA to Resolution:** [if known]
**Next Update:** [time]
```

### Resolution Notice

```markdown
## Incident Resolved - [Incident ID]

**Duration:** [start time] to [end time]

**What Happened:**
[Brief, non-technical summary]

**Resolution:**
[What was done to fix it]

**Impact Summary:**
- Users affected: [count/percentage]
- Duration of impact: [X hours Y minutes]

**Prevention:**
[Brief note on what will prevent recurrence]

Postmortem will be shared within [timeframe].
```

---

## Escalation Matrix

| Condition | Action | Who to Notify |
|-----------|--------|---------------|
| SEV1 detected | Immediate escalation | On-call lead, Engineering manager |
| SEV2 > 30 min | Escalate to leadership | Engineering manager |
| Security suspected | Involve Sentinel | Security team |
| Data loss confirmed | Escalate immediately | CTO, Legal (if PII) |
| External service issue | Contact vendor | Vendor support, Internal lead |
| Unable to mitigate | Request help | Additional engineers |

---

## Runbook: Database Issue

```markdown
## Database Issue Response

### Quick Diagnostics
- [ ] Check connection pool status
- [ ] Check replication lag
- [ ] Check disk space
- [ ] Check active queries
- [ ] Check lock waits

### Common Mitigations
1. **Connection exhaustion:** Kill idle connections, increase pool
2. **Slow queries:** Identify and kill long-running queries
3. **Replication lag:** Reduce write load, check network
4. **Disk full:** Expand disk, archive old data
5. **Deadlocks:** Identify and break deadlock cycle

### Failover Procedure
1. Confirm primary is truly unhealthy
2. Notify team of failover
3. Promote replica to primary
4. Update connection strings
5. Verify application connectivity
6. Monitor for data consistency
```

---

## Runbook: API Outage

```markdown
## API Outage Response

### Quick Diagnostics
- [ ] Check error rates by endpoint
- [ ] Check latency by endpoint
- [ ] Check upstream dependencies
- [ ] Check recent deployments
- [ ] Check infrastructure health

### Common Mitigations
1. **High error rate:** Check logs, rollback if recent deploy
2. **High latency:** Scale up, check database, check cache
3. **Upstream failure:** Enable fallback, cache responses
4. **Rate limiting:** Adjust limits, block abusers
5. **Memory/CPU exhaustion:** Restart pods, scale up

### Rollback Procedure
1. Identify last known good version
2. Initiate rollback deployment
3. Verify rollback completion
4. Test critical paths
5. Monitor error rates
```

---

## Runbook: Third-Party Integration

```markdown
## Third-Party Service Issue Response

### Quick Assessment
- [ ] Check vendor status page
- [ ] Check our integration logs
- [ ] Check API response times
- [ ] Check error messages

### Common Mitigations
1. **Vendor outage:** Enable fallback/degraded mode
2. **Rate limited:** Implement backoff, queue requests
3. **API change:** Check for breaking changes, update integration
4. **Auth issue:** Refresh tokens, check credentials

### Fallback Strategies
- Cache previous responses
- Queue for retry
- Disable feature gracefully
- Switch to backup provider
```

---

## Severity Assessment Checklist

```markdown
## Severity Assessment

**Impact Scope:**
- [ ] All users affected
- [ ] Specific user segment affected
- [ ] Single user affected
- [ ] Internal only

**Business Impact:**
- [ ] Revenue loss (direct)
- [ ] Revenue loss (indirect)
- [ ] Reputation damage
- [ ] Compliance violation
- [ ] No business impact

**Data Impact:**
- [ ] Data loss confirmed
- [ ] Data corruption possible
- [ ] Data exposure risk
- [ ] No data impact

**Service State:**
- [ ] Complete outage
- [ ] Degraded performance
- [ ] Partial functionality
- [ ] Fully operational

**Calculated Severity:** SEV[1-4]
```
