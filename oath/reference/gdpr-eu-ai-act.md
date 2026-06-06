# GDPR and EU AI Act Compliance Reference

Purpose: Assess compliance with the EU General Data Protection Regulation (GDPR) and the EU AI Act. Drive article-level control mapping (Art. 5/6/7/13/14/15-22/25/32/33/34), DPIA triggers, Records of Processing Activities (ROPA), lawful-basis selection, cross-border transfer controls, DSAR fulfillment workflow, and AI Act risk classification (prohibited / high-risk / limited / minimal). Every control references the exact regulation article — never generic "privacy best practice".

## Scope Boundary

- **Oath `gdpr`**: GDPR + EU AI Act regulatory mapping, article-level evidence, DPIA / ROPA / SCC design, DSAR workflow, lawful-basis documentation, AI Act conformity assessment.
- **Cloak (elsewhere)**: hands-on privacy engineering — PII detection scanners, data-flow graphing, consent-SDK implementation, pseudonymization code, DPIA facilitation workshops.
- **Crypt (elsewhere)**: cryptographic key management and KMS integration under Art. 32 (encryption at rest / in transit / envelope encryption / HSM attestation).
- **Warden (elsewhere)**: V.A.I.R.E. pre-release functional quality gate (not a regulatory audit).
- **Vigil (elsewhere)**: detection rule authoring for exfiltration / breach alerts (Art. 33/34 detection coverage, not notification workflow).

If the question is "what article applies and what evidence does the DPA expect?" stay in `gdpr`. If it is "implement the consent banner / encrypt this column / run the DPIA workshop", hand off to Cloak or Crypt.

## Article-to-Control Map

| Article | Control domain | Assessment focus |
|---------|----------------|------------------|
| Art. 5 | Principles (lawfulness, purpose limitation, minimization, accuracy, storage limitation, integrity, accountability) | Trace every personal-data field to at least one principle; flag over-collection |
| Art. 6 | Lawful basis | One of six bases must be selected and documented per processing activity |
| Art. 7 | Conditions for consent | Granular, withdrawable, separate from ToS; no pre-ticked boxes |
| Art. 13 / 14 | Information to data subject | Privacy notice completeness at collection (13) and indirect collection (14) |
| Art. 15-22 | Data subject rights | Access, rectification, erasure, restriction, portability, objection, automated decision-making (Art. 22) |
| Art. 25 | Data protection by design and by default | Pseudonymization, minimization, default privacy settings |
| Art. 28 | Processor obligations | DPA (Data Processing Agreement) signed before processing starts |
| Art. 30 | ROPA | Records maintained by controller and processor |
| Art. 32 | Security of processing | Encryption, pseudonymization, confidentiality/integrity/availability/resilience, regular testing |
| Art. 33 | Breach notification to DPA | 72-hour clock from awareness, documented regardless of risk |
| Art. 34 | Breach notification to data subject | Required when high risk to rights; plain-language communication |
| Art. 35 | DPIA | Mandatory for high-risk processing (see trigger list below) |
| Art. 44-49 | International transfers | SCC 2021 modules, BCR, adequacy decision, Art. 49 derogations |

### EU AI Act Risk Tiers

| Tier | Examples | Oath check |
|------|----------|--------------|
| Prohibited (Art. 5) | Social scoring, real-time public biometric ID, emotion recognition in workplace | Flag as non-shippable — block release |
| High-risk (Annex III) | Employment screening, credit scoring, critical infrastructure, biometric ID | Conformity assessment, FRIA, registration in EU database, post-market monitoring |
| Limited-risk | Chatbots, deepfakes, emotion recognition (non-prohibited contexts) | Transparency obligation (Art. 50) — user must know they interact with AI |
| Minimal-risk | Spam filters, recommenders outside Annex III | Voluntary codes of conduct |

General-purpose AI (GPAI) models have separate transparency + copyright obligations from August 2025; systemic-risk GPAI adds evaluation, incident reporting, and cybersecurity duties.

### EU AI Act Enforcement Timeline (2026-05 anchor)

| Phase | Date | What is binding |
|-------|------|------------------|
| Prohibited practices (Art. 5) | **In force since Feb 2025** | Social scoring, real-time public biometric ID, workplace emotion recognition — no grace period |
| GPAI transparency + copyright (Art. 53-55) | **In force since 2 Aug 2025** | Technical documentation to EU AI Office, downstream-provider support packs, copyright respect, training-data summaries |
| **Annex III high-risk AI systems** | **2 Aug 2026** | Conformity assessment, FRIA, EU database registration, post-market monitoring, human oversight, robustness + accuracy + cybersecurity controls |
| AI systems embedded in regulated products | 2 Aug 2027 | Full application across product-safety regulated sectors |

The European Commission's *Digital Omnibus* package (proposed late 2025) may push Annex III high-risk obligations to **December 2027**, but the extension is not guaranteed. **Plan against `2026-08-02` as the binding deadline** and treat any extension as a windfall — vendor-procurement gates and customer due diligence already assume the August 2026 date.

### Penalty Ladder (Art. 99)

| Infringement | Cap (whichever is higher) |
|--------------|----------------------------|
| Prohibited AI practice | `€35M` or `7%` of worldwide annual turnover |
| Non-compliance with high-risk obligations | `€15M` or `3%` of worldwide annual turnover |
| Incorrect / misleading information to authorities | `€7.5M` or `1.5%` of worldwide annual turnover |

GDPR penalties (Art. 83) apply **concurrently** when personal data is involved — the AI Act does not replace GDPR. An employment-screening AI processing EU residents can trigger both regimes for the same incident.

## DPIA Trigger Checklist

A DPIA is required when any of the following is true. Document the reason the DPIA was or was not performed — "we did not think it applied" is an audit failure.

- Systematic and extensive automated decision-making with legal or similarly significant effects (Art. 22).
- Large-scale processing of special-category data (Art. 9) or criminal convictions (Art. 10).
- Systematic monitoring of publicly accessible areas on a large scale.
- Innovative use of technology (AI scoring, biometric ID, IoT personal data).
- Any processing on the supervisory authority's published DPIA list.
- AI Act high-risk system — FRIA (Fundamental Rights Impact Assessment) is additionally required.

## ROPA Template (Art. 30)

| Field | Content |
|-------|---------|
| Processing activity name | Short descriptor (e.g., "Customer support ticket handling") |
| Controller / joint controllers / DPO | Legal entity + contact |
| Purposes | Precise purpose, not "business operations" |
| Categories of data subjects | Customers, employees, visitors, minors |
| Categories of personal data | Identifiers, contact, financial, special-category |
| Recipients | Internal teams + external processors (subprocessor chain visible) |
| International transfers | Country + transfer mechanism (SCC module, BCR, adequacy) |
| Retention period | Specific duration tied to purpose, not "as long as necessary" |
| Security measures | Art. 32 controls mapped (encryption, access control, pseudonymization) |
| Lawful basis | Art. 6 basis + Art. 9 condition if special-category |

## Cross-Border Transfer Decision Order

1. Adequacy decision in place (e.g., UK, Japan, EU-US DPF for certified US entities)? → transfer lawful, document the decision reference.
2. If no adequacy → SCC 2021 modules (controller-to-processor / processor-to-processor etc.) + Transfer Impact Assessment (TIA).
3. BCR for intra-group transfers (requires DPA approval, typically 12-24 months).
4. Art. 49 derogations — explicit consent / contract necessity — only for occasional, non-repetitive transfers. Never treat as a steady-state basis.

## DSAR Handling Workflow

```
RECEIVE   →  verify requester identity proportionate to request risk
          →  log timestamp — 30-day clock starts (extendable +60 days if complex)
          →  classify: access / rectification / erasure / restriction / portability / objection / Art. 22

LOCATE    →  search all systems holding personal data (ROPA is the map)
          →  include processors and subprocessors (contractual obligation)
          →  flag third-party personal data requiring redaction

FULFILL   →  prepare machine-readable export (JSON / CSV) for portability requests
          →  apply Art. 23 restrictions (legal privilege, ongoing investigations)
          →  document decisions + rationale for partial / refused responses

RESPOND   →  send within 30 days; communicate free of charge unless manifestly unfounded / excessive
          →  if refused: inform of right to complain to DPA and seek judicial remedy
```

## Consent vs Legitimate Interest

| Dimension | Consent (Art. 6(1)(a)) | Legitimate interest (Art. 6(1)(f)) |
|-----------|------------------------|-------------------------------------|
| When to pick | Marketing to prospects, special-category data, AI training on personal data | B2B outreach to existing contacts, fraud prevention, internal analytics |
| Proof burden | Granular, timestamped, withdrawable record per purpose | Documented Legitimate Interest Assessment (LIA) — purpose / necessity / balancing |
| Withdrawal | Equally easy as giving; stop processing on withdrawal | Honor objection (Art. 21) unless compelling legitimate grounds |
| Children | Parental consent up to 13-16 (Member State) | Rarely appropriate — balance test usually fails |
| Never use for | Contractual necessity, legal obligation | Cookies (ePrivacy requires consent), direct marketing to new users |

## Anti-Patterns

- Treating GDPR as "privacy policy updates" — missing ROPA, missing DPIA, missing lawful-basis register.
- Collecting consent once at signup then claiming it covers every future purpose — violates Art. 7(2) granularity.
- Using Art. 49 derogations as an ongoing transfer basis instead of a one-off exception.
- "Legitimate interest" applied to AI training on user data without LIA documentation or opt-out path — the UK ICO and EDPB have both pushed back on this pattern.
- DPIA written after launch — Art. 35(1) requires it **prior to** processing.
- Treating EU AI Act obligations as 2027 work — prohibited-use bans were enforceable from Feb 2025, GPAI transparency obligations from Aug 2025, Annex III high-risk obligations from **2 Aug 2026**. The Digital Omnibus extension to Dec 2027 is a *possibility*, never an *assumption* — vendor procurement gates already price in the August 2026 date.
- Confusing DPA (controller-processor contract, Art. 28) with DPIA (impact assessment, Art. 35) — they are different instruments.
- Running DSAR search only against the primary database and missing logs, backups, analytics warehouses, and subprocessor systems.

## Handoff

**To Cloak** — implementation of privacy-by-design patterns: consent SDK integration, PII scanner wiring, pseudonymization of identified fields, DPIA facilitation.

**To Crypt** — Art. 32 cryptographic controls: key hierarchy, KMS choice (AWS KMS / GCP KMS / Azure Key Vault / HSM), envelope encryption for special-category data, TLS 1.2+ with forward secrecy.

**To Builder** — DSAR fulfillment endpoints, consent-withdrawal hooks, data-export job, retention-based deletion jobs.

**To Scribe** — ROPA document, DPIA report, privacy notice revision, DPA template for new processors.

**To Beacon** — breach-detection alert thresholds feeding the Art. 33 72-hour clock; DSAR SLA dashboard.
