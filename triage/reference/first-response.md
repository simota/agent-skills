# First 15 Minutes Reference

Purpose: The T-0 to T+15 minute window of an incident — Incident Command assignment, war-room opening, SEV classification, scribe role, initial timeline capture, and the first holding comm. Everything beyond minute 15 belongs to `response-workflow.md` (Phases 2-5).

Lineage: FEMA Incident Command System (ICS) → Google SRE Incident Command → Atlassian Incident Handbook → PagerDuty Incident Response training. Triage inherits the roles (IC, Ops Lead, Comms Lead, Scribe) and collapses them for small-team reality.

## Scope Boundary

- **Triage `first-response`**: T-0 to T+15 min only. Command structure, severity call, initial comm.
- **Triage `respond` / `response-workflow.md`**: Full lifecycle DETECT → LEARN. `first-response` is the T-0 deep dive underneath `respond`.
- **Mend**: Executes pre-catalogued runbook remediation. `first-response` hands off to Mend only after IC is assigned and the pattern matches a known runbook.
- **Builder**: Writes the code fix. `first-response` never touches code.
- **Triage `escalation`**: Designs the paging policy; `first-response` executes it.
- **Triage `comms`**: Authors stakeholder templates; `first-response` sends only the first holding comm using those templates.

## The 15-Minute Clock

```
T+0    Alert fires / incident reported
T+1    Acknowledge (MTTA target < 5 min for critical)
T+2    Assign Incident Commander (IC)
T+3    Open war-room (Slack / Zoom / doc)
T+5    SEV classification complete
T+7    Scribe assigned, timeline entry #1 written
T+10   Holding comm sent ("aware, investigating")
T+15   Handoff to Phase 2 (ASSESS & CONTAIN)
```

Miss the T+5 SEV call → escalate first, investigate second. Late severity calls compound blast radius exponentially.

## Role Assignment (FEMA ICS / Google SRE)

| Role | Owns | Rule |
|------|------|------|
| Incident Commander (IC) | Coordination, decisions, external comms authorization | MUST NOT diagnose or write code — only coordinates |
| Ops Lead | Technical investigation and mitigation | Reports up to IC; does not speak to customers |
| Comms Lead | Stakeholder updates (internal + external) | Uses templates from `incident-communications.md` |
| Scribe | Timeline capture in UTC with decision rationale | SEPARATE person from IC — IC cannot both lead and type |

Small-team collapse: for teams < 4 engineers, one person may hold IC + Comms, but Scribe MUST be a second person. IC without Scribe = lost timeline = postmortem with no causal analysis.

## IC Assignment Script

```
"I am taking Incident Command for this incident as of HH:MM UTC.
Ops Lead: [name]. Comms Lead: [name or 'IC doubles'].
Scribe: [name, must be different from IC].
War-room: [#incident-YYYY-MM-DD-short-name] + [Zoom link].
Next checkpoint: T+5 with SEV classification."
```

Post this verbatim in the war-room. It creates the audit trail for the postmortem.

## War-Room Opening Checklist

- [ ] Create dedicated Slack channel: `#inc-YYYY-MM-DD-short-name` (not a thread; threads are un-searchable under load)
- [ ] Start Zoom / Meet bridge and pin the link at the top of the channel
- [ ] Pin the incident doc (Google Doc / Notion) for parallel written notes
- [ ] Invite: on-call primary, on-call secondary, EM (for SEV1/SEV2), Comms Lead
- [ ] Do NOT invite the wider team until SEV is classified — premature crowding destroys signal
- [ ] Silence adjacent channels / pause non-incident pages for the IC

## SEV Classification Checklist (T+2 to T+5)

Ask in order. First YES sets the floor.

| # | Question | If YES |
|---|----------|--------|
| 1 | Is there active data loss or data corruption risk? | SEV1 |
| 2 | Is production completely down or the API unreachable? | SEV1 |
| 3 | Is a security breach suspected? | SEV1 + Sentinel |
| 4 | Is a revenue-generating path broken (payments, checkout, auth)? | SEV2 |
| 5 | Is a major feature broken for > 10% of users? | SEV2 |
| 6 | Is there a workaround? | SEV3 |
| 7 | Is it cosmetic or minimal impact? | SEV4 |

Rule: when in doubt between two levels, pick the higher one. Downgrading costs nothing; late escalation costs trust.

## Initial Timeline Capture

Scribe starts a UTC-only log from minute one. Format:

```markdown
## Timeline (UTC)

| Time | Who | Event | Decision / Rationale |
|------|-----|-------|----------------------|
| 14:03 | Datadog | Alert: p99 latency 5.2s on /checkout | — |
| 14:05 | @alice | Acknowledged in PagerDuty | — |
| 14:07 | @alice | Took IC, opened #inc-2026-04-24-checkout | — |
| 14:09 | @bob (Scribe) | Scribe assigned | — |
| 14:11 | IC | Classified SEV2 | Revenue path affected, workaround unclear |
| 14:13 | Comms | Holding status page update posted | Next update by 14:30 UTC |
```

Capture decisions with "because" — a timeline without rationale teaches nothing at postmortem.

## First Holding Comm (T+10)

Silence after detection creates the perception that nobody is responding. Send a holding comm within 10 minutes, even with zero root cause.

Minimum template (full templates in `incident-communications.md`):

```
[INVESTIGATING] We are aware of an issue affecting [symptom from user perspective, not internal jargon].
Impact: [brief, honest — if unknown, say "investigating scope"].
Next update: [HH:MM UTC, no more than 15 min out for SEV1, 30 min for SEV2].
```

Rules:
- Never use passive voice that hides accountability ("an issue has occurred" → "we are investigating an issue").
- Never promise a fix time in the first comm — promise only the next update time.
- For SEV1 with customer data exposure suspected, the IC MUST loop in legal before the first external comm.

## Handoff to Phase 2 at T+15

The `first-response` recipe closes with a handoff, not a resolution:

```
IC @ T+15:
- SEV classified: [SEV1|SEV2|SEV3|SEV4]
- Impact snapshot: [users / feature / data]
- Initial hypothesis: [or "none yet"]
- Next phase: ASSESS & CONTAIN (see response-workflow.md Phase 2)
- Next update to stakeholders: [HH:MM UTC]
- Handoffs requested: [Scout for RCA? Mend for runbook? Sentinel for security?]
```

If at T+15 the IC cannot answer SEV or initial impact, the severity is SEV1 until proven otherwise.

## Anti-Patterns

- ❌ Starting diagnosis before IC is assigned — three engineers all typing in the channel, none owning coordination.
- ❌ IC also being the one typing the fix — you cannot command and execute simultaneously (Google SRE explicit rule).
- ❌ Skipping Scribe because "we'll reconstruct from Slack later" — Slack loses order under load, and nobody writes the rationale column retroactively.
- ❌ Delaying the holding comm until you "know more" — stakeholders interpret silence as panic or denial.
- ❌ Jumping to a fix before SEV classification — SEV drives cadence, staffing, and escalation.
- ❌ Inviting the entire engineering org to the war-room at T+2 — crowd noise destroys IC's ability to run the first 15 min.
- ❌ Using threads instead of a channel — threads lose the linear timeline and make scribing impossible.
- ❌ Letting an AI SRE agent (Bits AI SRE, Rootly AI SRE, incident.io AI SRE) take Incident Command. The agent investigates and proposes; the IC remains a named human throughout the 15-minute window.

## AI SRE Co-pilot Integration (2026)

By 2026 the leading platforms — Datadog **Bits AI SRE**, **Rootly AI SRE**, **incident.io AI SRE** — run an autonomous investigation loop from the moment the alert fires. Independent customer reports cite MTTR reductions of `~40-70%` and Datadog reports services restored `~90%` faster on its own dataset. The agent does not replace the IC; it accelerates the loop.

Operating rules during the 15-minute window:

| T | Human action | AI SRE co-pilot action |
|---|--------------|------------------------|
| `T+0` | Page fires | Agent ingests the alert, correlates metrics / logs / traces / recent deploys / dependency health in parallel |
| `T+2` | IC assigned by name | Agent posts initial impact estimate + top-3 candidate root causes with confidence into the war-room |
| `T+5` | SEV classified by the IC (not the agent) | Agent surfaces matching past incidents and runbook candidates |
| `T+10` | Comms Lead sends holding comm | Agent drafts the holding comm; Comms Lead edits and signs before posting |
| `T+15` | IC handoff to Phase 2 | Agent's investigation transcript is attached to the incident doc as evidence |

Hard rules:

- **No agent-initiated state changes during the first 15 minutes** beyond read-only investigation. Runbook execution still flows through Mend with its tier classification (`mend/reference/safety-model.md`).
- **The IC names the SEV.** The agent can recommend, but the SEV classification carries blame-line authority and stays with the IC.
- **Confidence is preserved verbatim.** If the agent reports `medium confidence` on a candidate root cause, the IC must preserve that label when communicating downstream — never round up to "the agent found the cause".
- **Investigation transcript is part of the audit trail.** Save the agent's reasoning alongside the timeline; it is the input to AI-assisted postmortem drafts (see `beacon/reference/incident-learning-postmortem.md`).

## What `first-response` Does NOT Do

- Does NOT execute remediation → Mend (known runbooks) or Builder (novel fix).
- Does NOT author full stakeholder templates → `comms` / `incident-communications.md`.
- Does NOT design the paging policy → `escalation` / `escalation-matrix.md`.
- Does NOT run RCA → Scout.
- Does NOT write the postmortem → `postmortem` / `postmortem-templates.md`.

The deliverable of `first-response` is: a classified incident, a named command structure, an open war-room with a running timeline, and one holding comm sent — all within 15 minutes.
