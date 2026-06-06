# Phishing Campaign Design Reference

Purpose: Design an authorized phishing campaign that measures real organizational susceptibility, exercises the detection and reporting loop, and produces awareness-training input — without exposing participants, infrastructure, or brand trust. Every campaign is scoped, time-boxed, and tied to a learning outcome, not a gotcha score.

## Scope Boundary

- **Breach `phishing`**: authorized campaign design — pretexts, landing-page clones, credential-harvest vs session-token flows, MFA-fatigue, QR-phishing (quishing), OAuth consent-phishing, SPF/DKIM/DMARC evasion techniques, reporting and feedback loops.
- **Sentinel (elsewhere)**: static security analysis of code paths that handle inbound email or user submissions. No campaign design.
- **Probe (elsewhere)**: DAST / penetration testing of the landing-page infrastructure itself. Not the social pretext.
- **Vigil (elsewhere)**: authoring the Sigma / YARA / email-header detection rules that flag the campaign artifacts. Campaign feeds Vigil — Vigil does not run the campaign.
- **Comply (elsewhere)**: regulatory mapping (GDPR breach-notification readiness, PCI phishing controls, SOC 2 awareness-training evidence).
- **Triage (elsewhere)**: post-incident response playbook when a real (not simulated) phish lands.

If the question is "does our workforce click, report, or escalate?" → `phishing`. If it is "do our email-security controls catch this payload?" → hand the campaign artifacts to Vigil and Probe.

## Campaign Patterns

| Pattern | Pretext shape | Primary goal | Key risk if misused |
|---------|---------------|--------------|--------------------|
| Credential harvest | Password-reset / shared-doc / HR portal | Measure click + credential-submit rate | Real creds leaked to test infra — use one-way hash + instant revoke |
| Session-token theft | OAuth consent / device-code grant | Validate session-binding, MFA trust | Token persistence beyond test window |
| MFA fatigue / push-bombing | Repeated push prompts + voice pretext | Measure push-accept rate under pressure | Locking real accounts — rate-limit and pre-notify IT |
| Quishing (QR) | Printed QR / email-embedded QR | Measure mobile out-of-band susceptibility | QR on shared media — scope to controlled distribution |
| OAuth consent-phishing | Third-party app consent screen | Measure consent-scope review behavior | Real OAuth app registered — revoke within 24h |
| Clone landing | High-fidelity SSO / vendor login replica | Measure visual-cue + URL inspection | Brand misuse — keep on `*-training.<corp>` subdomain |

Pick one pattern per campaign wave. Stacking patterns muddies the learning signal.

## Workflow

```
SCOPE        → define population, exclusion list (exec/IT/HR opt-ins),
               time window, rules of engagement, legal/HR sign-off
             → declare learning outcome (click / submit / report / escalate rate)
             → pick one pattern (credential / token / MFA / quishing / OAuth / clone)

PRETEXT      → craft narrative grounded in real internal context
             → source list from OSINT-safe patterns, never exfiltrated data
             → draft subject / sender / body / CTA with a failure-mode review

INFRA        → stand up sending domain with SPF+DKIM+DMARC aligned
             → landing on isolated subdomain, TLS, WAF, one-way cred hashing
             → instrument: open, click, submit, report, reauth flag

LAUNCH       → staged rollout (canary 5% → 25% → 100%) with kill-switch
             → monitor helpdesk volume, brand-abuse alerts, user distress signals

DEBRIEF      → same-day teachable-moment landing for clicked users
             → aggregate metrics: click %, submit %, report %, MTTR (time-to-report)
             → hand off rule artifacts to Vigil, training gaps to HR awareness
```

## SPF / DKIM / DMARC Evasion Techniques (Test Targets)

Campaigns probe these misconfigurations — the goal is to confirm the defender catches them, not to weaponize them.

| Technique | What it tests | Expected defender signal |
|-----------|---------------|--------------------------|
| Cousin domain (`c0rp.com` vs `corp.com`) | Typosquatting detection at MX | Inbound policy block + user header inspection |
| Display-name spoof | Visible "CEO Name" with foreign return-path | Banner injection, display-name rewrite |
| Lookalike-punycode (`córp.com`) | IDN homograph rendering | Strip or flag punycode at gateway |
| DMARC `p=none` relaxed alignment | Policy-gap exploitation | Alert on DMARC fail with aligned SPF |
| Header injection via reply-to | Hidden redirect of replies | Reply-to header validation |
| Shared-infra bypass (marketing-SaaS) | Authorized sender co-tenancy abuse | Subdomain-scoped DMARC `sp=reject` |

Document each probe with expected detection gap → Vigil converts to detection rules.

## Reporting and Feedback Loop

A campaign without a report button is a test of clicks, not of culture.

- One-click "Report phish" must exist in the mail client (Outlook/Gmail add-in, keyboard shortcut, or dedicated alias).
- Report-rate is a **leading** indicator — track alongside click-rate.
- Mean-time-to-first-report (MTTR-FR) measures how fast the org notices — aim < 10 minutes for a standard-difficulty pretext.
- Suppress duplicate-report fatigue: auto-ack reporters, collapse by campaign-id in the SOC view.
- Close the loop: publish anonymized campaign stats to the org within 5 business days — silence kills the program.

## Awareness-Training Integration

- Clicked users see a **teachable moment** page (not a shaming page) — highlight the 2 cues they could have caught.
- Bucketed follow-up: first-click = self-serve micro-lesson; repeat-click = assigned module; 3+ clicks = manager-notified coaching.
- Avoid leaderboards or public click-shaming — they suppress reporting.
- Role-based curricula: finance (BEC and invoice-redirect pretexts), engineering (OAuth consent, package-registry), exec (voice + deepfake pretexts), HR (candidate-resume malware).

## Anti-Patterns

- Pretexts using real leaked data ("your password is X") — turns a test into a harassment incident.
- No exclusion list — a CEO click becomes a leak, not a learning signal.
- Real credentials captured in plaintext — hash one-way at submit, never store.
- No kill-switch — unable to halt the campaign during a real incident overlap.
- Reusing the same pretext quarter after quarter — the population trains to that one pattern and susceptibility looks falsely resolved.
- Publishing click-rate without report-rate — optimizes the program toward harder pretexts instead of faster detection.
- Skipping the debrief landing page — leaves users feeling tricked, not taught.
- Running on the production SSO domain — users who "caught it" by URL lose their only reliable cue.
- Ignoring quishing and OAuth consent as exotic — mobile-QR campaigns show 3-4x click-rates vs desktop email in recent sector reports.
- Treating the SOC as a separate audience — SOC must run the campaign **as** a drill; silent-campaigns miss the detection-engineering feedback.

## Handoff / Next Steps

- To **Vigil**: campaign artifacts (sending-domain patterns, landing-page fingerprints, header anomalies, timing indicators) for Sigma / detection-rule authoring.
- To **Comply**: evidence package for SOC 2 CC2.2 / PCI 12.6.3 awareness-training controls and GDPR breach-simulation logs.
- To **Triage**: the exact campaign timeline, kill-switch status, and indicator list so real-phish reports during the window can be disambiguated from the test.
- To **Sentinel**: if the campaign revealed an email-handling or link-preview code path that auto-renders untrusted content — hand off for static review.
- To **Scribe**: final campaign report (scope, outcome, metrics, trend vs prior waves) with anonymized participant data.
- Journal novel pretexts and defender gaps in `.agents/breach.md` for future-wave calibration.
