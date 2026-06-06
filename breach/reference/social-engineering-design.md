# Social Engineering Scenario Design Reference

Purpose: Model human-vector attack scenarios (vishing, smishing, tailgating, pretexting, insider threat, BEC, deepfake) with learning outcomes aligned to the organization's awareness program. Behavioral-focused, not code-centric: the deliverable is scenarios, indicators, detection handoffs, and coordinated training — not executed attacks on real staff without governance.

## Scope Boundary

- **Breach `social`**: scenario design for the human layer — vishing (voice), smishing (SMS), tailgating / physical access, OSINT pretexting (LinkedIn, corporate directory, sales-enablement tools), insider-threat risk, business email compromise (BEC), deepfake voice and video, and awareness-program integration.
- **Breach `phishing` (sibling recipe)**: specifically email / landing-page / consent-phishing campaigns. `social` covers the broader human-layer surface.
- **Vigil (elsewhere)**: authoring detection rules for anomalous wire-transfer requests, voice-auth bypass attempts, badge-tailgating indicators, and impossible-travel sign-ins.
- **Cloak (elsewhere)**: PII handling, consent, and data-minimization controls that reduce OSINT surface. Cloak designs the controls; Breach tests whether they close the pretext.
- **Comply (elsewhere)**: SOC 2 CC1.4 / HIPAA 164.308(a)(5) / PCI 12.6 awareness-training and insider-threat programs.
- **Triage (elsewhere)**: post-incident response when a real social engineering attempt lands.
- **Clause (elsewhere)**: contractual and policy clauses that govern insider access and exit procedures.

If the question is "can a human be manipulated into granting access?" → `social`. If it is "can our technical controls catch it when they do?" → hand off to Vigil.

## Scenario Types

| Scenario | Channel | Target behavior | Primary learning outcome |
|----------|---------|-----------------|--------------------------|
| Vishing (voice) | Phone / VoIP | Credential disclosure, password reset, MFA approval | Voice-callback verification, out-of-band confirmation |
| Smishing (SMS) | SMS / iMessage / WhatsApp | Credential entry, OTP forwarding, app-sideload | Mobile URL-inspection, carrier-report habit |
| Tailgating / physical | On-site | Badge-less entry, reception bypass, device-drop | Challenge-culture, clean-desk, visitor log |
| OSINT pretexting | Multiple | Information disclosure under plausible persona | What is safely public vs reconnaissance fuel |
| Insider-threat risk | Internal | Abuse of legitimate access, data staging, collusion | Four-eyes for sensitive moves, egress monitoring |
| BEC (business email compromise) | Email / chat | Wire transfer, invoice redirect, payroll change | Out-of-band verification, dual-control on money movement |
| Deepfake voice / video | Voice call / video meeting | High-trust authorization under false identity | Pre-agreed safe-word, callback on known line |
| Pretexted help-desk | Phone / chat | Password reset, MFA reset, SIM swap | Caller-identity proofing, risk-tier on reset |

Pick one or two scenarios per exercise. Multi-scenario exercises are for mature programs running annually.

## Workflow

```
SCOPE          → legal / HR / works-council sign-off; labor-law review for
                 jurisdictions with consent requirements (EU, JP)
               → consent tier: opt-in volunteers, announced window, blind
               → exclusion list (new hires <90d, protected leave, execs
                 pre-briefed, IT/SOC/hotline staff kept uninformed or co-opted)
               → success metric: not "got in" but "detected / reported / stopped"

OSINT          → open-source intel gathering from public LinkedIn, job boards,
                 corporate blog, conference talks, leaked breach dumps (check-
                 only, never reuse)
               → build plausible pretext with 3+ corroborating public facts
               → record OSINT exposure as a finding — often the fix is at
                 Cloak, not the human

PRETEXT        → craft persona, script, fallback branches for refusal
               → rehearse with a neutral reviewer — if it feels coercive,
                 re-scope (the goal is learning, not entrapment)
               → deepfake scenarios: use synthetic media of actors or
                 licensed voice talent, never unauthorized likenesses

EXECUTE        → time-boxed window; safety-officer on standby to abort
               → record outcome signal (not audio of the target) —
                 binary: complied / refused / reported / escalated
               → first-line staff distress: stop immediately, debrief

DEBRIEF        → same-day private debrief with participants — framed as
                 program outcome, never as personal failure
               → aggregate anonymized results to steering committee
               → handoff detection gaps → Vigil; policy gaps → Comply;
                 OSINT gaps → Cloak; awareness-curriculum gaps → HR
```

## OSINT Pretexting Source Map

| Source | Intel extracted | Mitigation owner |
|--------|-----------------|------------------|
| LinkedIn profiles | Org structure, tech stack, recent transitions | Corporate social-media policy |
| Job postings | Internal tool names, versions, vendor relationships | Careers-page sanitization |
| Conference talks / podcasts | Architecture, key vendors, named projects | Talk-review process |
| Leaked credential dumps | Password-reuse, email format, personal device use | Crypt / Cloak + SSO enforcement |
| Sales-enablement decks (public links) | Customer lists, pricing, internal champions | Link-sharing policy, watermarking |
| Corporate directory (shadow-copied) | Reporting chains, titles, desk phones | Access-review, anti-scraping rate limits |
| Vendor PR / customer testimonials | Who uses what, when contracts renewed | PR review, named-customer policy |

Every OSINT hit is a supply-side finding as much as a demand-side training opportunity.

## Deepfake Voice / Video Scenarios

- Capability is commoditized: consumer tools produce convincing voice clones from 30 seconds of public speech; video from a handful of public photos.
- Highest-risk surface: executive impersonation on short-notice wire transfers, on-call engineer impersonation for break-glass access, and family-emergency pretexts against execs' personal numbers.
- Control to validate: **pre-agreed safe-word** (quarterly rotation) and **callback on a known-good number** — technical voice-liveness is not reliably available in 2026.
- Visual-call controls: require the caller to perform an unscripted action (turn head, show hand in frame) — consumer deepfake pipelines degrade under unpredicted motion.
- Deepfake exercises must never train the target to distrust *all* calls from execs — the goal is verification habit, not paranoia.

## Insider-Threat Risk Modeling

- Model three archetypes: negligent (70% of incidents), malicious (20%), compromised credential posing as insider (10%).
- Pre-exit window is the highest-risk period — model staging behavior (bulk download, personal-drive sync, printer spikes).
- Collusion scenarios: finance + vendor-management, dev + cloud-admin, sales + competitor — each circumvents single-role controls.
- Scenario tests four-eyes enforcement, egress monitoring coverage, and HR-IT sync on terminations.

## Anti-Patterns

- Running social engineering exercises without HR / legal / works-council sign-off — becomes a harassment or labor-law incident.
- Targeting specific individuals as a "test of their judgment" — program-level metrics only, never individual shaming.
- Using real, non-public PII in pretexts — turns simulation into unlawful processing (GDPR Art. 6 / Japan APPI).
- Unlicensed deepfake of a real person's voice or likeness — legal and ethical failure regardless of purpose.
- Treating report-rate as a vanity metric — a 5% report-rate and 30-min MTTR beats a 0% click-rate with zero reports.
- Ignoring tailgating and physical vectors because they feel old-school — still the #1 initial-access path for physical-data-center attacks.
- Skipping the debrief — leaves targets confused, angry, or distrustful of the program indefinitely.
- Using these scenarios to assess individual employee loyalty — that is surveillance, not security testing.
- Treating "the human is the weakest link" as the conclusion — it's the starting hypothesis; the finding is usually a missing technical or process control.

## Handoff / Next Steps

- To **Vigil**: detection-rule inputs — wire-transfer request anomalies, off-hour password-reset requests, impossible-travel sign-ins, badge-tailgating indicators, MFA-reset-followed-by-login patterns.
- To **Cloak**: OSINT-exposure findings — what public data fueled the pretext, what minimization or consent-scope changes close it.
- To **Comply**: evidence package for SOC 2 CC1.4 (control environment / ethics), CC2.2 (communication), HIPAA 164.308(a)(5) (awareness training), PCI 12.6 (security awareness), and insider-threat program obligations.
- To **Triage**: playbook updates for real BEC, SIM-swap, vishing, and deepfake incident-response with the scenario's indicators.
- To **Scribe**: final exercise report with anonymized metrics, trend vs prior waves, and policy-change recommendations.
- To HR / awareness program: role-based curriculum updates (finance, exec, IT help-desk, engineering, front-desk).
- Journal novel pretexts, deepfake tooling observations, and OSINT-source changes in `.agents/breach.md`.
