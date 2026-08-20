# Triage Recipe Registry

The full Recipe table for `triage`. `triage/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Incident Response | `respond` | ✓ | Incident first response (impact isolation + initial response + SEV classification) | `reference/response-workflow.md` |
| Impact Scoping | `impact` | | Impact scope identification (user, feature, and business dimension evaluation) | `reference/runbooks-communication.md` |
| Recovery Plan | `recover` | | Recovery procedure formulation (rollback and failover procedures) | `reference/response-workflow.md` |
| Postmortem | `postmortem` | | Postmortem document creation (5 Whys + action items) | `reference/postmortem-templates.md` |
| First 15 Minutes | `first-response` | | T-0 incident command: IC assignment, war-room opening, SEV classification, scribe, initial timeline, holding comms | `reference/first-response.md` |
| Escalation Matrix | `escalation` | | Design tiered on-call escalation, paging policy, auto-escalation thresholds, handoff script, PagerDuty/Opsgenie/VictorOps integration | `reference/escalation-matrix.md` |
| Stakeholder Comms | `comms` | | Incident-specific communication templates across internal, external status page, customer notices, social, with SEV-based cadence | `reference/incident-communications.md` |
