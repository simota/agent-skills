# SOC Incident-Response Playbook Reference

Purpose: Turn a detection alert into a repeatable, auditable SOC response. The `playbook` Recipe covers runbook templating for the highest-volume incident classes (phishing, credential compromise, ransomware, BEC), severity-triage flow, SOAR integration patterns (Tines / Cortex XSOAR / Splunk SOAR), and MITRE D3FEND defensive-action mapping. It does *not* cover incident execution itself (that is Triage's job) or attack-scenario design (that is Breach's).

## Scope Boundary

- **Vigil `playbook`**: Authoring the runbook — triage flow, evidence checklist, containment steps, SOAR automation hooks, D3FEND mapping. Design-time artifact.
- **Vigil `sigma` / `snort` / `yara`** (adjacent): Detection rules that *trigger* playbooks. Every high-severity rule must cite a corresponding playbook.
- **Triage** (adjacent): *Executes* the playbook during a live incident — impact scoping, recovery orchestration, postmortem. Vigil ships the playbook; Triage runs it.
- **Breach** (adjacent): Red-team attack scenarios that stress-test the playbook end-to-end in Purple Team exercises. Breach attacks, Vigil detects, playbook responds.
- **Mend** (adjacent): Automated remediation for well-understood failure patterns. Mend runs the *automated* subset of playbook steps under safety-tier controls.

If the question is "what does the SOC do when this fires?" → `playbook`. If "what are we doing *right now* in this live incident?" → Triage. If "can we automate this response step safely?" → Mend.

## Severity Triage Flow

```
ALERT → Triage Gate
  ├── SEV-1 (active exploitation / data exfil / ransomware)
  │     → Page IR lead, declare incident, full playbook
  ├── SEV-2 (confirmed compromise, bounded blast radius)
  │     → Ticket + IR lead notify, scoped playbook
  ├── SEV-3 (suspicious, unconfirmed)
  │     → L1 analyst investigates, enrichment-only steps
  └── SEV-4 (informational / policy)
        → Auto-close with enrichment notes
```

Severity is a function of **blast radius × confidence × reversibility**, not alert rule severity alone. Low-confidence SEV-1 indicators (e.g., `T1486 Data Encrypted for Impact` on one endpoint) still page — reversibility is near-zero.

## AI SOC Co-pilot Integration (2026)

By 2026 the SOC tooling stack (Wiz Green Agent, Microsoft Security Copilot, CrowdStrike Charlotte AI, Google SecOps Duet AI, autonomous-investigation agents inside Splunk / Sentinel / Datadog / Sumo) drafts a first-pass investigation per alert: enrichment, IoC pivot, similar-incident lookup, candidate root cause with confidence. Playbook authors must wire the co-pilot in *under the same rules that govern Mend remediation*:

- **The co-pilot proposes; the human IR lead disposes.** Containment, eradication, and recovery steps that change state remain gated by the safety tiers in `mend/reference/safety-model.md`. SEV-1 / SEV-2 actions are not auto-executed even when the agent is high-confidence.
- **Enrichment is the high-ROI co-pilot step.** Reserve agent autonomy for the *enrichment* phase — pull IP reputation, sandbox detonate, query VT, correlate to known incidents — and keep response steps under human approval.
- **Confidence is preserved verbatim.** When the agent reports `medium confidence` on an attribution or candidate IoC, the playbook output must carry the label unchanged into the IR doc — never round up to "confirmed".
- **Investigation transcript is part of the audit trail.** Attach the agent transcript ID to the incident record alongside SIEM hits; downstream postmortem drafts (see `triage/reference/postmortem-templates.md` and `beacon/reference/incident-learning-postmortem.md`) consume it.

## Playbook Templates

| Incident Class | ATT&CK Entry | D3FEND Defensive Actions | Key Containment |
|----------------|--------------|--------------------------|-----------------|
| Phishing (credential harvest) | T1566.002, T1566.001 | D3-UA (User Account Locking), D3-URL (URL Analysis) | Revoke sessions, reset password, block sender |
| Credential Compromise | T1078, T1110, T1621 | D3-MFA (Multi-factor Authentication), D3-AL (Account Locking) | Rotate creds, revoke tokens, force MFA re-enroll, audit recent access |
| Ransomware | T1486, T1490, T1489 | D3-PSA (Process Self-modification Analysis), D3-SFA (System File Analysis), D3-HD (Host Disconnect) | Isolate host, snapshot memory, block C2, restore from immutable backup |
| BEC (Business Email Compromise) | T1534, T1114.003, T1098.002 | D3-IAA (Inbound Authentication Analysis), D3-MH (Mailbox Hardening) | Disable forwarding rules, audit OAuth app grants, reset credentials, notify finance |

### Runbook skeleton (Phishing credential harvest)

```yaml
playbook_id: PB-PHISH-001
incident_class: Phishing Credential Harvest
trigger_rules: [DET-SIGMA-042, DET-SNORT-2000123]
attack_techniques: [T1566.002, T1556.006]
d3fend_actions: [D3-UA, D3-URL, D3-SRA]
severity_default: SEV-2

steps:
  - id: 1-scope
    phase: triage
    action: "Identify recipients from mail gateway logs"
    owner: L1
    sla_min: 15
    automation: "SOAR.query('mailgw', {subject: ${alert.subject}})"

  - id: 2-contain-account
    phase: contain
    action: "Revoke active sessions + force password reset"
    owner: L2
    sla_min: 30
    automation: "AzureAD.revokeSignInSessions(${user.upn})"

  - id: 3-block-infra
    phase: contain
    action: "Block sender domain at mail gateway + malicious URL at proxy"
    owner: L2
    sla_min: 30
    automation: "Tines.run('block_url', {url: ${ioc.url}})"

  - id: 4-hunt-lateral
    phase: eradicate
    action: "Sigma hunt for MFA bypass and OAuth grant within 24h window"
    owner: Hunt
    sla_min: 240

  - id: 5-notify
    phase: recover
    action: "User notification + security-awareness follow-up tag"
    owner: L1
    sla_min: 60

  - id: 6-postmortem
    phase: lessons_learned
    action: "Detection gap review → coverage Recipe handoff"
    owner: DetEng
    sla_min: 2880
```

## SOAR Integration Patterns

| Platform | Strength | Watch-out |
|----------|----------|-----------|
| Tines | Low-code story-builder, fast iteration | Harder audit trail on story changes; pin versions in git |
| Cortex XSOAR (Palo Alto) | Mature playbook library, War Room timeline | Heavy licensing; playbook complexity creeps into Python tasks |
| Splunk SOAR (Phantom) | Tight Splunk ES integration, custom apps | Version-upgrade friction; some actions deprecated silently |
| Chronicle SOAR (Google) | Native Chronicle enrichment, Gemini assist | Smaller connector marketplace vs Cortex |
| Shuffle (OSS) | Self-hosted, zero licensing | You own the uptime; careful with credential storage |

**Automation safety rules** — adopt these on every platform:

1. **Human gate on destructive actions** (host isolation, account disable, firewall block) for SEV-2 and below; auto-allowed only with SEV-1 + high-confidence IoC.
2. **Dry-run mode** for every new automation for 2 weeks before enabling execution.
3. **Idempotency** — rerunning a playbook must not double-execute (revoke twice, block twice). Use SOAR run-IDs as dedup keys.
4. **Rollback step** — every containment action must have a matching revert step in the same playbook.
5. **Audit log to immutable sink** — not just SOAR's own DB. WORM storage or append-only SIEM index.

## D3FEND Defensive Action Mapping

Every playbook step should cite at least one D3FEND technique so defensive coverage can be measured symmetrically to ATT&CK offensive coverage:

- **Harden**: D3-AH (Application Hardening), D3-CH (Credential Hardening), D3-PH (Platform Hardening)
- **Detect**: D3-NTA (Network Traffic Analysis), D3-PA (Process Analysis), D3-UBA (User Behavior Analysis)
- **Isolate**: D3-NI (Network Isolation), D3-EI (Execution Isolation)
- **Deceive**: D3-DE (Decoy Environment), D3-DO (Decoy Object)
- **Evict**: D3-CE (Credential Eviction), D3-PE (Process Eviction)

Use D3FEND to argue *why* each containment step reduces attacker dwell — not just "we block the IP", but "D3-NI network isolation severs C2 channel T1071.001".

## Anti-Patterns

- Writing a playbook without a named `attack_techniques` list (playbook cannot be mapped to coverage).
- Same playbook for phishing and ransomware because "both are email" (collapsing incident classes hides response specificity).
- Automating containment for SEV-3 / unconfirmed alerts (one bad enrichment quarantines a VP's laptop).
- Skipping the rollback step (cannot safely undo SOAR-driven actions during a false positive).
- Treating postmortem as optional — no detection-gap feedback → same incident recurs.
- Hardcoding IoCs in the playbook body (should be `ioc` Recipe / threat-intel platform lookup).
- Letting playbook versions drift between Tines / XSOAR / wiki — one source of truth in git, everything else renders from it.

## Handoff / Next Steps

- **To Triage**: packaged playbook YAML + SOAR run-book URL + evidence-collection checklist. Triage executes during the live incident.
- **To Mend**: identify which steps are candidates for automated remediation under Mend's safety-tier rules (T1/T2 only; T3+ stays human-gated).
- **To `coverage`**: register each playbook against its ATT&CK + D3FEND IDs so both offensive-gap and defensive-gap dashboards update.
- **To `ioc`**: every IoC observed during playbook execution (URLs, hashes, C2 domains) feeds the threat-intel lifecycle.
- **To Scribe**: postmortem template pre-filled with playbook phase timestamps and SLA deltas.
- **To Breach**: Purple-Team exercise request — replay the attack end-to-end and measure MTTD / MTTC / MTTR against the playbook.
