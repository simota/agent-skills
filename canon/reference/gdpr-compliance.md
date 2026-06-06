# GDPR Compliance Reference

Purpose: Standards-citation-driven assessment against the EU General Data Protection Regulation (Regulation (EU) 2016/679, effective May 25, 2018). Cites specific Articles, evaluates lawful basis, surfaces DPIA triggers (Art. 35), data-subject rights coverage, breach-notification readiness (Art. 33 — 72 hours), DPO appointment threshold (Art. 37), and routes remediation to specialist agents.

## Scope Boundary

- **canon `gdpr`**: standards-citation-driven assessment. Pin "GDPR (Regulation (EU) 2016/679)", cite Article and paragraph (e.g., `Art. 6(1)(b)`, `Art. 32(1)(a)`), evidence at `file:line`, lawful-basis mapping per processing activity.
- **cloak (elsewhere)**: privacy-by-design implementation (`Art. 25`). PII detection, data-flow maps, consent-management code, DPIA facilitation, anonymization/pseudonymization design. Canon assesses; Cloak builds.
- **comply (elsewhere)**: audit trail, Records of Processing Activities (RoPA — `Art. 30`), Policy-as-Code, DPA (Data Processing Agreement) registry, supervisory-authority correspondence.
- **clause (elsewhere)**: legal text review of Privacy Policy, Cookie Notice, DPA — clause-gap detection. Canon does not make legal determinations; defer to Clause + lawyer.
- **sentinel (elsewhere)**: static scanning for PII leakage, hardcoded data-subject identifiers, insecure storage of personal data.

## Workflow

```
SURVEY    →  inventory processing activities, data categories, data subjects, recipients,
             cross-border transfers (Art. 44-49: SCC, BCR, adequacy decision)
          →  pin GDPR + check member-state derogations (e.g., German BDSG, Italian Codice Privacy)

PLAN      →  per processing activity: identify lawful basis (Art. 6 — six bases), special
             category basis (Art. 9 if applicable), purpose, retention, recipients

ASSESS    →  Articles 5/6/7/13/17/25/30/32/33/35 as core; expand to 12-22 (rights), 44-49
             (transfers) as scope demands. Evidence at file:line + DPIA/RoPA refs

VERIFY    →  gap report by Article; flag DPIA-required activities (Art. 35), 72h breach
             readiness (Art. 33), DPO threshold (Art. 37(1)(b)/(c))

PRESENT   →  delegate: Cloak (PbD, DPIA, consent code), Comply (RoPA, DPA),
             Clause (Privacy Policy text), Sentinel (PII scan), Builder (remediation)
```

## Six Lawful Bases (Art. 6(1))

| Letter | Basis | Typical Use | Caveat |
|--------|-------|-------------|--------|
| (a) | Consent | Marketing emails, optional cookies | Must meet `Art. 7` — freely given, specific, informed, unambiguous, withdrawable |
| (b) | Contract | Account creation, order fulfillment | Only data necessary for contract performance |
| (c) | Legal obligation | Tax records, AML/KYC | Cite the specific law |
| (d) | Vital interests | Medical emergency | Rare for typical SaaS |
| (e) | Public interest / official authority | Public bodies | Rare for private sector |
| (f) | Legitimate interests | Fraud prevention, internal analytics | Requires LIA (Legitimate Interests Assessment); does NOT apply to special categories without separate Art. 9 basis |

For **special categories** (Art. 9 — health, biometric, political, religious, trade union, sex life, racial/ethnic, genetic), requires both Art. 6 basis AND Art. 9 basis (e.g., explicit consent, vital interests, employment law).

## Core Articles Assessed

| Article | Title | Assessment Focus |
|---------|-------|-----------------|
| `Art. 5` | Principles | Lawfulness, fairness, transparency, purpose limitation, data minimization, accuracy, storage limitation, integrity/confidentiality, accountability |
| `Art. 6` | Lawful basis | Per-activity basis declared and documented |
| `Art. 7` | Consent conditions | Withdrawable as easily as given; pre-ticked boxes invalid |
| `Art. 13/14` | Information to data subject | Privacy Notice completeness (collected from / collected about) |
| `Art. 15-22` | Data-subject rights | Access, rectification, erasure (`Art. 17`), restriction, portability, objection, automated-decision opt-out |
| `Art. 17` | Right to erasure ("right to be forgotten") | Deletion workflow incl. backups, third-party recipients notification |
| `Art. 25` | Data Protection by Design and by Default | Default = minimum data, minimum exposure, minimum retention |
| `Art. 28` | Processor obligations | DPA in place, sub-processor flow-down, audit rights |
| `Art. 30` | Records of Processing Activities (RoPA) | Maintained for controllers (and processors) — exempt only if `<250` employees AND processing not risky/regular/special |
| `Art. 32` | Security of processing | Encryption, pseudonymization, CIA, resilience, regular testing |
| `Art. 33` | Breach notification to supervisory authority | Within 72 hours of awareness, unless unlikely to risk rights |
| `Art. 34` | Breach communication to data subjects | Where high risk to rights and freedoms |
| `Art. 35` | DPIA | Required when likely high risk; specific triggers below |
| `Art. 37` | DPO designation | Required for public authority, large-scale special categories, large-scale systematic monitoring |
| `Art. 44-49` | International transfers | SCC (2021 modules), BCR, adequacy decision (e.g., EU-US DPF), derogations |

## DPIA Triggers (Art. 35(3) + WP29 Guidelines)

| Trigger | Example |
|---------|---------|
| Systematic, extensive evaluation incl. profiling with legal/significant effects | Credit-scoring, insurance underwriting |
| Large-scale processing of special categories or criminal data | Hospital EHR, HR system with health data |
| Systematic monitoring of public area | CCTV, public Wi-Fi tracking |
| Innovative technology | Biometrics, IoT, AI/LLM with personal data |
| Data combined or matched from multiple sources | Marketing data brokers |
| Data of vulnerable subjects | Children, employees (asymmetric power) |
| Cross-border processing preventing rights exercise | Sub-processor in non-adequate country |

WP29 rule: 2+ triggers → DPIA required. National DPAs publish their own DPIA-required lists.

## Breach Notification (Art. 33) — 72-Hour Clock

- Clock starts from "awareness" by controller, not from breach occurrence.
- Notification skipped only if "unlikely to result in a risk to the rights and freedoms of natural persons" — high bar.
- Phased notification allowed: initial within 72h, details in subsequent updates.
- To data subjects (Art. 34): only when "high risk" — encryption renders data unintelligible may exempt.
- Penalties: up to €20M or 4% of global turnover (whichever higher) for Art. 5/6/7/9 violations; €10M or 2% for Art. 33 procedural breaches.

## DPO Appointment (Art. 37)

Mandatory when:
- Public authority/body (except courts in judicial capacity).
- Core activities = regular and systematic monitoring of data subjects on large scale.
- Core activities = large-scale processing of special categories or criminal data.

DPO must report to highest management level, cannot be dismissed for performing tasks, and may be staff or contracted external.

## Anti-Patterns

- Treating GDPR as cookie-banner compliance — GDPR governs all personal-data processing; cookies are one slice (and ePrivacy Directive overlaps).
- Citing "GDPR Article 6" without paragraph — `Art. 6(1)(a)` consent vs. `Art. 6(1)(f)` legitimate interests have entirely different obligations. Always cite paragraph + letter.
- Consent for everything — over-relying on `Art. 6(1)(a)` when contract or legitimate interests fit better. Withdrawn consent then breaks core service.
- Paper compliance — RoPA spreadsheet maintained but never updated; Privacy Policy says "we delete on request" but no erasure pipeline exists.
- Audit-only thinking — annual privacy review without continuous DPIA updates when processing changes (new vendor, new feature, new data category).
- Copy-paste Privacy Policy from another company — wrong lawful bases, wrong retention, wrong DPO contact. Each Privacy Policy must reflect actual processing.
- Ignoring sub-processor flow-down — `Art. 28(4)` requires equivalent obligations on sub-processors; ignoring this leaves controller liable.
- Treating pseudonymization as anonymization — pseudonymized data is still personal data (Recital 26). Only true anonymization (irreversible, no re-identification) exits GDPR scope.
- Cross-border transfer on legacy SCCs — 2010 SCCs replaced by 2021 modular SCCs; old contracts after Dec 27, 2022 are invalid.
- Scope-creep / scope-shrinkage on "controller vs. processor" — misclassification shifts liability and changes obligations (RoPA, breach reporting, DPA).
- Reactive breach response — discovering on day 70 then panicking. Build a 72h-ready playbook with pre-drafted templates and decision trees.

## Handoff

- **To Cloak**: privacy-by-design implementation (`Art. 25`), DPIA facilitation (`Art. 35`), consent management code (`Art. 7`), pseudonymization/anonymization design (`Art. 4(5)`), data-subject rights API (`Art. 15-22`), data-flow maps.
- **To Comply**: RoPA maintenance (`Art. 30`), DPA registry (`Art. 28`), audit trail, Policy-as-Code (OPA rules for retention/access), supervisory-authority correspondence.
- **To Clause**: Privacy Policy / Cookie Notice / DPA legal text review and clause-gap analysis. Always pair with qualified counsel for legal determinations.
- **To Sentinel**: PII leakage scanning, hardcoded personal-data identifiers, insecure storage detection, secret/credential exposure (`Art. 32(1)(a)`).
- **To Crypt**: encryption-at-rest/in-transit design, key management for `Art. 32(1)(a)` and breach-notification exemption qualification.
- **To Builder**: technical remediation with Article-citation acceptance criteria (e.g., "Implement `Art. 17` erasure pipeline including backups within 30 days").
