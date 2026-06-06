# Incident Communications Reference

Purpose: Stakeholder-specific communication templates and cadence for active incidents. Audience-aware, severity-aware, time-sensitive language. The goal is trust preservation under adverse conditions — predictable cadence with public status pages cuts inbound support volume by up to 60%.

Lineage: Atlassian Incident Handbook + Google SRE customer comms guidance + regulatory disclosure norms (GDPR 72-hour, SOC2 control). Inherits Prose's voice/tone foundation but overrides for incident-specific directness.

## Scope Boundary

- **Triage `comms`**: Incident-specific templates with severity-aware tone, legal-review hooks, time-stamped cadence. Used during live incidents and for post-incident customer notices.
- **Prose**: Product-wide microcopy, voice and tone system, onboarding copy, generic error messages. Prose defines the baseline voice; `comms` overrides it for incident directness.
- **Triage `first-response`**: Sends only the first holding comm (T+10). `comms` authors the template library and drives the full cadence afterward.
- **Launch**: Release-related comms (planned maintenance, new-feature announcements). `comms` is reactive incident; Launch is proactive release.
- **Cloak / Clause**: Data-breach legal disclosure text. `comms` provides the operational comm skeleton; Cloak / Clause / legal counsel fill in regulated language.

## Stakeholder Matrix

| Audience | Channel | Tone | Detail Level | Update Cadence |
|----------|---------|------|--------------|----------------|
| Internal engineering | Slack #inc-* channel | Technical, blunt | Full — logs, hypotheses, error rates | Continuous |
| Leadership | Slack #leadership-incidents + direct page for SEV1 | Business impact, concise | Revenue, user count, ETA | 15 min (SEV1), 30 min (SEV2) |
| Sales | Slack #sales-heads-up | Customer-talking-points | What to say to customers, NOT root cause | 30 min (SEV1), hourly (SEV2) |
| Support | Slack #support-incidents + macro/canned response | Actionable for front line | Symptoms, workarounds, escalation path | Continuous during SEV1/SEV2 |
| External status page | statuspage.io / public | Public, honest, no jargon | What's affected, next update time | 15 min (SEV1), 30 min (SEV2) |
| Direct customer notice | Email / in-app banner | Respectful, specific | User-visible impact + workaround | At classification + resolution |
| Social (X / LinkedIn) | Corporate accounts | Short, professional | Link to status page | At classification + resolution |

## SEV-Based Cadence

| SEV | Update Interval | First Comm By | Resolution Comm |
|-----|-----------------|---------------|------------------|
| SEV1 | Every 15 min | T+10 min | Required, all channels |
| SEV2 | Every 30 min | T+15 min | Required, status page + email |
| SEV3 | Every 2 hours | T+30 min | Status page only |
| SEV4 | On resolution only | On resolution | Optional |

**Rule**: every update explicitly names the next-update time in UTC. Silence erodes trust faster than bad news.

## Template Library

### Internal Engineering (Slack #inc-*)

```
[SEV1 | T+12 min | 14:15 UTC]
**Status**: INVESTIGATING
**Symptom**: p99 latency on /checkout 5.2s (baseline 280ms); error rate 8%
**Scope**: US-EAST region; ~12% of active checkouts
**Hypothesis**: DB connection pool exhaustion (see @alice's graphs)
**Actions in flight**:
- @bob: scaling read replicas (ETA 14:20 UTC)
- @carol: pulling deploy log from past 2h (80% incidents → recent change)
**Blockers**: none
**Next update**: 14:30 UTC
```

### Leadership

```
[SEV1 Update | 14:15 UTC]
**Impact**: ~12% of US checkouts failing. Revenue at risk: ~$8K/min at current traffic.
**What's happening**: Investigating database-layer bottleneck. Likely deploy-related.
**ETA**: Mitigation attempt at 14:20 UTC. Next assessment at 14:30 UTC.
**IC**: @alice. **Comms**: @dan handling status page + sales heads-up.
**Decision needed from you**: None right now. Will escalate if we need rollback approval.
```

### Sales Heads-Up

```
[SEV1 — Checkout degradation | 14:15 UTC]
**What customers may see**: Checkout failures, slow load on /checkout in US-EAST.
**What to say**: "We're aware of an issue affecting checkout and are actively working on it. You can follow updates at status.example.com."
**What NOT to say**: Do not speculate on cause, do not promise a fix time, do not mention internal systems (DB / pool / etc).
**Escalation**: For key accounts or press inquiries, route to @vp-sales + @dan (Comms Lead).
**Next update**: 14:45 UTC or on resolution.
```

### Support Canned Response

```
[For inbound tickets mentioning checkout / slow / errors | SEV1 active]

"Thanks for reaching out. We're aware of an issue currently affecting checkout for some users and are actively working to resolve it. You can follow live updates at https://status.example.com/incidents/[ID]. We'll reach out directly once service is fully restored. We apologize for the disruption."

**Flag ticket with tag**: `inc-[YYYY-MM-DD]-checkout`
**Escalate to tier 2 support if**: customer reports data loss, double-charge, or security concern.
```

### External Status Page (Public)

**Initial (T+15 max):**
```
[INVESTIGATING — 14:15 UTC]
We are investigating reports of errors and slow response times affecting checkout.
Users in the US may experience failures when completing orders.
Our engineers are actively working on a resolution.
Next update: 14:30 UTC.
```

**Mitigating:**
```
[IDENTIFIED — 14:32 UTC]
We have identified the cause of the checkout issues and are deploying a mitigation.
Some users may continue to see errors for the next 10-15 minutes while the fix rolls out.
Next update: 14:45 UTC.
```

**Resolved:**
```
[RESOLVED — 15:04 UTC]
The checkout issue has been resolved as of 15:01 UTC. All systems are operating normally.
Total duration: 61 minutes. Impact: approximately 12% of US checkout attempts between 14:03 and 15:01 UTC.
A full incident report will be published within 48 hours.
Thank you for your patience.
```

### Direct Customer Notice (Email / In-App)

**For impacted users only, post-resolution:**
```
Subject: Resolved: Checkout issue on [Date]

Hi [Name],

On [Date], between [start time] and [end time] UTC, a subset of users — including your account — experienced failures when attempting to complete checkout. This has been fully resolved.

If any order appears missing or duplicated, please reply to this email and we will make it right. No payment information was affected.

We're sorry for the inconvenience. Our full incident report will be published at [link] within 48 hours.

— [Team]
```

### Social (X / LinkedIn)

```
We're aware of an issue affecting checkout for some users. Our team is investigating.
Live updates: status.example.com
```

```
The checkout issue has been resolved. Thanks for your patience — full report coming within 48 hours.
```

## Legal-Review Hooks

Any external comm that mentions **any of the following** MUST pass legal review before publication:

- Data loss or data corruption
- Unauthorized access / security breach / PII exposure
- Regulated data (health, payment card, financial, minors)
- Service-level commitments or refund promises
- Named third-party vendors as cause
- Regulated geographies (EU — GDPR 72-hour clock starts; California — CCPA; others)

Workflow: Comms Lead drafts → legal reviews → IC approves publication. For SEV1 with breach suspicion, engage legal within the first 30 minutes, not at resolution.

## Tone Overrides (vs Prose Baseline)

Prose establishes product voice (warm, helpful, on-brand). Incident comms OVERRIDE for:

- **Directness**: "We are investigating X" — not "Our team is looking into some reported concerns."
- **No marketing polish**: strip adjectives; facts only.
- **Accountability language**: "we", not "the system" or passive voice.
- **Honesty about uncertainty**: "We do not yet know the cause" is more trustworthy than a vague guess.
- **Explicit next-update time in UTC**: always, without exception.
- **No apology inflation**: one sincere apology at resolution is worth more than five hedging apologies mid-incident.

## Anti-Patterns

- ❌ "An issue has been detected" — passive voice, hides ownership.
- ❌ Promising a fix time in the first comm — you don't know yet; promise next-update time instead.
- ❌ Copy-pasting the internal Slack update to the status page — technical jargon erodes public trust.
- ❌ Going silent for 45 minutes because "we'll update when we have news" — stakeholders fill silence with worst-case assumptions.
- ❌ Naming a specific vendor as the cause before the postmortem — opens legal liability.
- ❌ Using the word "resolved" before 30-min observation window completes — premature resolution + recurrence destroys trust.
- ❌ Corporate social post referring people to file a support ticket — route to the status page instead to prevent support flood.
- ❌ Marketing-tone apology ("We truly value your trust and are committed to...") — during an incident, plain is better.

## Post-Incident Customer Report

For SEV1/SEV2, publish a public-facing post-incident report within 48-72 hours. Structure:

1. **What happened** (1 paragraph, plain language)
2. **Who was affected** (scope, duration, concrete numbers)
3. **What we did** (timeline of major actions)
4. **Why it happened** (root cause summary, non-technical)
5. **What we are doing to prevent recurrence** (concrete action items with owners and dates)

Link the public report from the status page incident entry. Internal technical postmortem stays internal → see `postmortem-templates.md`.
