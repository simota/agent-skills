# Escalation Matrix Reference

Purpose: Design-time artifact defining the tiered escalation policy that routes pages from detection to the right human, at the right time, with the right authority. This is the document a new on-call engineer reads during onboarding, and the doc the IC references during an incident when deciding whether to wake the VP.

Lineage: PagerDuty Incident Response training + Google SRE on-call philosophy + Atlassian Incident Handbook escalation tiers.

## Scope Boundary

- **Triage `escalation`**: Designs the human escalation policy — who gets paged, when, under what threshold, with what SLA, and what they are authorized to do.
- **Gear `alert`**: Configures the alerting infrastructure (Alertmanager routing rules, webhook targets, Prometheus thresholds). Gear sends the page; `escalation` decides who receives it and what happens next.
- **Beacon**: Designs SLOs and detection signals; `escalation` consumes Beacon's severity classifications to shape paging thresholds.
- **Mend**: Executes automated remediation; `escalation` may bypass human paging for known runbook patterns that Mend can handle autonomously within safety tiers.

Cross-link: Gear's Alertmanager route → PagerDuty service → `escalation`-defined escalation policy → tier 0 on-call.

## Escalation Tiers

Canonical 4-tier structure. Adjust for org size.

| Tier | Role | Pager Target | Ack SLA | Authority |
|------|------|--------------|---------|-----------|
| 0 | Primary on-call engineer | PagerDuty primary schedule | 5 min (SEV1), 15 min (SEV2) | Diagnose, mitigate, execute runbooks, invoke Mend |
| 1 | Secondary on-call engineer | PagerDuty secondary schedule | 10 min (SEV1), 30 min (SEV2) | Pair with tier 0, take IC if tier 0 is blocked |
| 2 | Engineering Manager (EM) / Tech Lead | Phone + SMS + PagerDuty | 15 min (SEV1), 60 min (SEV2) | Resource allocation, cross-team coordination, customer comms authorization |
| 3 | VP Engineering / CTO / Director | Phone call only | 30 min (SEV1 only) | Public disclosure, legal engagement, major rollback of business-critical systems |

Additional domain-specific tiers as sibling branches:
- Security path: tier 0 → Security on-call → CISO (bypasses EM for breach-suspected SEV1)
- Data loss path: tier 0 → DBRE on-call → Data Platform EM → CTO + Legal
- Compliance path: tier 0 → Compliance Officer (for regulated systems: SOC2 / HIPAA / PCI)

## Auto-Escalation Timers

Unacknowledged pages auto-escalate. Timer design:

| Severity | Tier 0 → Tier 1 | Tier 1 → Tier 2 | Tier 2 → Tier 3 |
|----------|-----------------|-----------------|-----------------|
| SEV1 | 5 min unack | 10 min unack | 20 min unack |
| SEV2 | 15 min unack | 45 min unack | Manual only |
| SEV3 | 30 min unack | Manual only | Never |
| SEV4 | Business-hours only, no auto-escalate | — | — |

Rules:
- Auto-escalation does NOT cancel the prior tier — it fans out, so both tier 0 and tier 1 are paged simultaneously after the timer.
- After-hours (22:00 - 08:00 local tier-0 time) SEV3 does NOT page; queues to next business day.
- SEV1 NEVER respects after-hours; all tiers are fair game.

## Paging Policy by SEV

| SEV | Page Method | After-Hours? | Escalation Window |
|-----|-------------|--------------|-------------------|
| SEV1 | Push + SMS + phone call (all simultaneous) | Yes | 5 min per tier |
| SEV2 | Push + SMS | Yes if business-critical system, else queued until 07:00 | 15 min per tier |
| SEV3 | Push only | No (09:00 - 18:00 tier-0 local) | 30 min tier 0 → tier 1, then manual |
| SEV4 | Email / Slack only | No | No auto-escalation |

## On-Call Rotation

- **Primary rotation**: 1 week, handoff Monday 10:00 local.
- **Secondary rotation**: 1 week, offset by 3 days to avoid both on-call engineers rotating off simultaneously.
- **Follow-the-sun**: for 24/7 systems, 3 regions × 8-hour shifts; each region's tier 0 auto-hands off at shift end via PagerDuty override.
- **Holiday coverage**: explicit owner for each public holiday, published in the schedule at least 90 days ahead.
- **Vacation override**: engineer takes vacation → named override engineer, NOT "whoever is around" — undocumented coverage = missed page.

## Handoff Script (End of Shift / Follow-the-Sun)

Every shift handoff requires a written handoff in the on-call channel:

```
## On-Call Handoff — [YYYY-MM-DD HH:MM UTC]

**Outgoing:** @alice (primary), @bob (secondary)
**Incoming:** @carol (primary), @dan (secondary)

**Active incidents:** [list with INC-IDs and current SEV, or "none"]
**Recent mitigations still monitoring:** [e.g., "checkout rate-limit raised 2h ago — monitor p99"]
**Open deploys / known-risky changes:** [list with times]
**Planned maintenance windows next 24h:** [list]
**Paged-but-benign alerts in shift:** [pattern, for Beacon feedback]

**Escalation confirmations:**
- [ ] Carol acknowledges primary pager handoff in PagerDuty
- [ ] Dan acknowledges secondary pager handoff in PagerDuty
- [ ] Both have runbook access verified
```

Handoff without acknowledgement = no handoff. Pager stays on the outgoing engineer.

## After-Hours Engagement Rules

- **SEV1 any-time**: primary on-call engages within 5 min, no exceptions.
- **SEV2 after-hours**: primary engages if business-critical system (checkout, auth, API, payment); otherwise logged for 07:00 handoff.
- **SEV3 after-hours**: queued, no page.
- **Humane caps**: max 2 wake-ups per night per engineer. On third page, auto-escalate to tier 1. If tier 1 also hits 2 wake-ups, escalate to EM to reassign.
- **Post-shift rest**: any engineer paged between 22:00-06:00 gets a 4-hour delayed start the following day. This is policy, not a favor — fatigued responders cause secondary outages.

## PagerDuty / Opsgenie / VictorOps Integration

### PagerDuty

- Service per domain (checkout, auth, data-platform) — not per team. Prevents wrong-team paging.
- Escalation policy per SEV: name explicitly, e.g., `sev1-critical-4tier`, `sev2-business-hours-3tier`.
- Override rules: vacation, on-boarding grace period (first 2 weeks new hires → secondary only), named handoff.
- Response plays: pre-built templates that mobilize IC + Ops Lead + Comms + Scribe in one click for SEV1.
- Stakeholder groups: subscribe leadership / sales / support to incident lifecycle events (not raw pages).

### Opsgenie

- Teams map to domains; routing rules per integration.
- Schedules with time-based rotations; overrides via calendar.
- Escalation policies mirror PagerDuty tier structure.
- Heartbeat monitoring for critical cron / batch jobs — if heartbeat fails, page tier 0 directly.

### VictorOps / Splunk On-Call

- Routing keys per service + severity combination.
- Escalation paths via graphical policy editor; mirror the 4-tier structure.
- Post-incident review hooks to push resolved incidents into the postmortem pipeline.

### Common Configuration Checklist

- [ ] One integration per alerting source (Prometheus, Datadog, Sentry) — no daisy-chained webhooks
- [ ] Dedupe key set on every alert — otherwise one alert storm creates 100 pages
- [ ] Acknowledgement timeout configured per SEV (5 / 15 / 30 min)
- [ ] Stakeholder subscribers configured for tier-2+ alerts
- [ ] Override notification to outgoing engineer when schedule change occurs < 24h ahead

## Anti-Patterns

- ❌ "The whole team gets paged" — dilutes ownership, guarantees nobody investigates first.
- ❌ No auto-escalation — one sleeping engineer = entire outage.
- ❌ Escalation based on tenure ("ask the senior engineer") — tribal knowledge does not survive vacation or turnover.
- ❌ Paging EM before tier 1 for SEV2 — EM is for resource allocation, not diagnosis.
- ❌ After-hours SEV3 paging — trains engineers to ignore the pager, creating alert fatigue (73% of outages trace to ignored/misrouted alerts).
- ❌ No handoff document — incoming engineer walks into an unknown state.
- ❌ Escalation policy documented only in PagerDuty — nobody reads PagerDuty UI during an incident; this document must exist in searchable markdown.

## Review Cadence

- Quarterly: rotation health check (burnout indicators, wake-up counts, unacknowledged page rate).
- Per postmortem: if escalation path contributed to delay, file an action item to update this matrix.
- Annually: full tier / SLA / authority review with EM + on-call engineers together.
