# Triage Response Workflow Reference

Detailed incident response phases and templates.

Purpose: Read this when Triage needs phase-by-phase operating detail, containment or mitigation options, verification checklists, or post-resolution capture rules.

Contents:
- `Phase 1: DETECT & CLASSIFY`: first-5-minute acknowledgement and initial report
- `Phase 2: ASSESS & CONTAIN`: containment options and impact framing
- `Phase 3: INVESTIGATE & MITIGATE`: handoff sequence, parallel execution, and mitigation comparison
- `Phase 4: RESOLVE & VERIFY`: recovery checklist and extended verification
- `Phase 5: LEARN & IMPROVE`: deadlines, external report decisions, and knowledge capture

## Phase 1: DETECT & CLASSIFY (First 5 minutes)

**Immediate Actions:**
1. Acknowledge the incident
2. Gather initial information
3. Classify severity
4. Notify stakeholders (if SEV1/SEV2)

### Initial Incident Report Template

```markdown
## Initial Incident Report

**Reported By:** [name/system]
**Reported At:** [YYYY-MM-DD HH:MM UTC]
**Initial Description:** [what was reported]

**Symptoms:**
- [ ] Error messages: [exact text]
- [ ] Affected URL/endpoint: [path]
- [ ] Error rate: [X% of requests]
- [ ] Latency: [current vs baseline]
- [ ] User reports: [count/nature]

**Environment:**
- [ ] Production / Staging / Dev
- [ ] Region: [if applicable]
- [ ] Version: [deployed version]
```

---

## Phase 2: ASSESS & CONTAIN (Minutes 5-15)

**Impact Assessment:**
- Determine scope of affected users/features
- Identify potential data impact
- Check for cascading failures
- Document timeline of events

### Containment Options

| Action | When to Use | Risk |
|--------|-------------|------|
| Feature flag disable | Feature-specific issue | Functionality loss |
| Rollback deploy | Recent deploy caused issue | May lose good changes |
| Scale up resources | Load-related issue | Cost increase |
| Block traffic | DDoS/abuse | Legitimate users blocked |
| Failover to backup | Primary system failure | Data sync lag |
| Disable integration | Third-party issue | Feature degradation |

---

## Phase 3: INVESTIGATE & MITIGATE (Minutes 15-60)

**Coordinate Investigation:**
- Hand off to Scout for root cause analysis
- Request Lens for evidence collection
- Request Beacon for monitoring data (if available)

### Handoff Sequence (Standard Flow)

```
1. Triage → Scout   : request RCA with symptoms, timeline, and initial hypotheses
2. Scout → Triage   : return RCA with root cause, fix location, and recommended approach
3. Triage → Builder : request remediation with Scout findings and urgency
4. Builder → Radar  : request verification with fix details and regression scope
5. Radar → Triage   : return verification results and coverage impact
6. Triage → Close   : close the incident after verification completes
```

**Parallel Execution (When applicable):**
- Lens can capture evidence while Scout is running RCA.
- If the cause is already clear, Builder may start remediation before Scout fully completes when Triage approves.

### AI SRE Co-pilot in Phase 3 (2026)

When an AI SRE co-pilot is running (Bits AI SRE, Rootly AI SRE, incident.io AI SRE), step 1 changes shape: the agent has *already* started parallel investigation from the moment of detection. Triage's job is not to wait for Scout but to **validate and route** the agent's findings.

| Step | Triage action | What changes when AI SRE is on |
|------|---------------|----------------------------------|
| 1 | Read agent's top-3 candidate causes with confidence | Skip Scout if confidence ≥ `high` on a candidate that matches a known runbook; otherwise still escalate to Scout for human RCA |
| 2 | Verify the agent's correlated metrics / logs / traces / deploys are real | Reject any candidate that cannot be backed by a specific query — hallucinated correlations get filtered here, not in the postmortem |
| 3 | Route to Mend if the agent proposes a runbook match | The runbook still passes through Mend's safety-tier classification — the AI agent's confidence does not bypass T3 / T4 approval gates |
| 4 | Route to Builder if the agent proposes a code fix | The agent's draft PR is reviewed by a human; the PR-as-safety-gate rule remains in force (see `mend/reference/safety-model.md`) |

Hard rules:

- **Triage owns the routing decision**, not the AI agent. The agent recommends; Triage accepts, modifies, or escalates to Scout for human RCA.
- **No autonomous remediation in SEV1 / SEV2.** Even when the agent's confidence is high, a named human owner approves every state-changing action.
- **Investigation transcript is captured as evidence.** Same audit-trail rule as in `first-response.md` — the transcript becomes input to the AI-assisted postmortem draft.

Reported gains in 2026 published case studies: MTTR reductions of `~40-70%` are typical when the AI co-pilot is wired into a mature Triage process; the same tools deliver near-zero improvement (and sometimes regressions) when the Triage process itself is loose, because the agent amplifies whatever discipline it is given.

### Mitigation Options Template

```markdown
## Mitigation Options

| Option | Impact | Reversibility | Time to Implement |
|--------|--------|---------------|-------------------|
| [Option 1] | [impact] | [easy/medium/hard] | [X min] |
| [Option 2] | [impact] | [easy/medium/hard] | [X min] |
| [Option 3] | [impact] | [easy/medium/hard] | [X min] |

**Recommended:** [Option] because [reason]
```

---

## Phase 4: RESOLVE & VERIFY (Variable)

### Resolution Checklist

- [ ] Root cause identified (via Scout)
- [ ] Fix implemented (via Builder)
- [ ] Fix deployed to production
- [ ] Monitoring shows recovery
- [ ] User-facing symptoms resolved
- [ ] No regression in other areas

### Resolution Verification Template

```markdown
## Resolution Verification

**Service Health:**
- [ ] Error rate returned to baseline: [X%]
- [ ] Latency returned to baseline: [X ms]
- [ ] Success rate recovered: [X%]

**User Verification:**
- [ ] Test account can complete affected flow
- [ ] No new error reports
- [ ] Affected users notified (if applicable)

**Monitoring:**
- [ ] Alerts cleared
- [ ] Dashboards show normal
- [ ] No secondary issues detected

**Extended Verification (SEV1/SEV2):**
- [ ] Primary user flow tested end-to-end
- [ ] Data integrity verified (no loss/corruption)
- [ ] Related systems verified (no cascading impact)
- [ ] 30-minute observation period completed without recurrence
- [ ] Rollback plan confirmed still viable
```

---

## Phase 5: LEARN & IMPROVE (Post-resolution)

### Postmortem Timeline

| Severity | Deadline |
|----------|----------|
| SEV1 | Within 24 hours |
| SEV2 | Within 48 hours |
| SEV3/4 | Within 1 week (if warranted) |

### External Incident Report Decision

| Report Type | Audience | Timing |
|-------------|----------|--------|
| Detailed Report | Customers, Partners, Executives | After SEV1/SEV2 resolution (Recommended) |
| Summary Report | When quick sharing is needed | On request |
| None | Internal impact only | SEV3/SEV4 |

### Knowledge Capture (Required for SEV1/SEV2)

After postmortem completion, add learnings to `.agents/PROJECT.md`:

```markdown
| YYYY-MM-DD | Triage | Postmortem: [incident title] | Root cause: [brief] | Prevention: [action item] |
```

Also update `.agents/triage.md` if:
- New incident pattern discovered
- Effective mitigation strategy found
- Runbook gap identified
