# Privacy Regulations Reference

## 2026 Enforcement Snapshot

The 2026 privacy landscape compresses three trends into a single operating reality:

- **EU AI Act** — high-risk obligations (Annex III) bind on **2 Aug 2026**; the GDPR penalty regime applies *concurrently*. New penalty ceiling adds `€35M / 7%` of global turnover for prohibited practices, `€15M / 3%` for high-risk non-compliance. See `oath/reference/gdpr-eu-ai-act.md` for the full timeline.
- **US state laws fragmenting** — `19+` US states have comprehensive privacy laws in effect by Jan 2026 (Indiana, Kentucky, Rhode Island added in Jan 2026; Texas Responsible AI Governance Act and Colorado AI Act follow). Treat "is this a CCPA-only project?" as obsolete framing; any consumer-facing US product needs a state-by-state applicability matrix.
- **GDPR fines hit €7.1B cumulative** — the regulators are *enforcing*, not warning. Treat 72-hour breach notification and DPIA-before-launch as hard deadlines, not aspirational ones.

## GDPR (EU General Data Protection Regulation)

### Lawful Basis Decision Tree

```
Is there a contract with the data subject?
├─ Yes → Art. 6(1)(b) Contract
└─ No
   Is it required by law?
   ├─ Yes → Art. 6(1)(c) Legal obligation
   └─ No
      Is explicit consent obtained?
      ├─ Yes → Art. 6(1)(a) Consent
      └─ No
         Is there a legitimate interest that doesn't override data subject rights?
         ├─ Yes → Art. 6(1)(f) Legitimate interest (document LIA)
         └─ No → Processing not permitted
```

### Key Rights & Timelines

| Right | Article | Deadline | Implementation notes |
|-------|---------|----------|---------------------|
| Access | Art. 15 | 30 days | Return all personal data in machine-readable format |
| Rectification | Art. 16 | 30 days | Update inaccurate data; propagate to processors |
| Erasure | Art. 17 | 30 days | Delete + inform all processors; exceptions for legal holds |
| Portability | Art. 20 | 30 days | JSON/CSV export; only for consent/contract basis |
| Restriction | Art. 18 | 30 days | Flag and stop processing; retain data |
| Objection | Art. 21 | Immediate | Must stop unless compelling grounds; always for direct marketing |

### Special Category Data (Art. 9)

Processing prohibited unless:
- Explicit consent (Art. 9(2)(a))
- Employment/social security law (Art. 9(2)(b))
- Vital interests (Art. 9(2)(c))
- Health care (Art. 9(2)(h))
- Public health (Art. 9(2)(i))
- Archiving/research (Art. 9(2)(j))

### Breach Notification (Art. 33-34)

| Action | Deadline | Condition |
|--------|----------|-----------|
| Notify supervisory authority | 72 hours | Unless unlikely to result in risk |
| Notify data subjects | Without undue delay | If high risk to rights/freedoms |
| Document breach internally | Immediately | All breaches, regardless of severity |

### Cross-Border Transfers (Art. 44-49)

| Mechanism | Use when |
|-----------|----------|
| Adequacy decision | Destination country has EU adequacy (Japan, UK, Canada, etc.) |
| Standard Contractual Clauses (SCCs) | No adequacy; contractual safeguards with processor |
| Binding Corporate Rules (BCRs) | Intra-group transfers within multinational |
| Explicit consent | Last resort; must inform of risks |

### DPIA Required When (Art. 35)

- Automated decision-making with legal effects (profiling)
- Large-scale processing of special category data
- Systematic monitoring of public areas
- New technologies with likely high risk
- Large-scale processing of children's data

## CCPA / CPRA (California)

### Consumer Rights

| Right | Section | Deadline | Notes |
|-------|---------|----------|-------|
| Know (access) | §1798.100 | 45 days (+ 45 extension) | 12-month lookback |
| Delete | §1798.105 | 45 days (+ 45 extension) | Exceptions: legal, security, billing |
| Opt-out of sale/sharing | §1798.120 | Immediate | "Do Not Sell/Share My Personal Information" link required |
| Correct | §1798.106 | 45 days | CPRA addition |
| Limit sensitive PI use | §1798.121 | Immediate | CPRA addition |

### Applicability Thresholds

CCPA applies if the business:
- Annual gross revenue > $25M, OR
- Buys/sells/shares PI of 100,000+ consumers/households, OR
- Derives 50%+ revenue from selling/sharing PI

### Key Implementation Requirements

1. **Privacy policy** disclosing categories of PI collected and purposes.
2. **"Do Not Sell or Share"** link on website (if applicable).
3. **Verification** of consumer identity before fulfilling requests.
4. **Non-discrimination** for exercising rights.
5. **Service provider contracts** with use restrictions.

## APPI (Japan — Act on the Protection of Personal Information)

### Key Concepts

| Concept | Definition | Equivalent |
|---------|-----------|------------|
| Personal Information (個人情報) | Information that can identify a living individual | GDPR: Personal Data |
| Requiring Special Care (要配慮個人情報) | Race, creed, social status, medical history, criminal record | GDPR: Special Category |
| Anonymously Processed Information (匿名加工情報) | Irreversibly de-identified data | GDPR: Anonymized Data |
| Pseudonymously Processed Information (仮名加工情報) | Re-identifiable with additional info | GDPR: Pseudonymized Data |

### Key Requirements

| Requirement | Article | Notes |
|-------------|---------|-------|
| Specify purpose of use | Art. 17 | Must be as specific as possible |
| Consent for purpose change | Art. 18 | Unless reasonably related |
| Consent for sensitive data | Art. 20(2) | Always required for requiring-special-care data |
| Proper acquisition | Art. 20 | No deception or improper means |
| Accuracy & up-to-date | Art. 22 | Maintain accuracy to extent necessary |
| Security measures | Art. 23 | Organizational + technical safeguards |
| Third-party provision | Art. 27 | Consent required (with opt-out exceptions) |
| Cross-border transfer | Art. 28 | Equivalent protection or consent |
| Disclosure on request | Art. 33 | Without delay |
| Breach notification | Art. 26 | To PPC and data subject (promptly) |

### 2022 Amendment Key Changes

- **Pseudonymously Processed Information** category added.
- **Cross-border transfer** requirements strengthened (must inform of destination country's regime).
- **Breach notification** to PPC became mandatory.
- **Individual rights** expanded (deletion, usage cessation).

### 2026 APPI Amendment (in progress)

The Japanese Cabinet approved a fresh APPI amendment bill on **2026-04-07** and submitted it to the Diet. Expected to take full effect by **2028** if passed during 2026. Key practical impacts:

- **Cross-border transfer monitoring** — when relying on the "receiving country's protection system" basis, the controller must now monitor the receiving party's protection regime at least **once per year** (the previous rule was open-ended).
- **Cross-border consent disclosure** — when relying on data-subject consent for an overseas transfer, the controller MUST disclose (i) the destination country name, (ii) that country's data protection regime, and (iii) the receiving party's specific protective measures *before* obtaining consent.
- **Tighter alignment with GDPR / China PIPL / Korea PIPA** — the amendment is explicitly framed as continuing the trajectory toward global-standard parity.

Plan APPI projects against this trajectory even before the effective date; the cross-border monitoring requirement is the most operationally disruptive change for SaaS providers serving Japan from outside Japan.

## Regulation Comparison Matrix

| Feature | GDPR | CCPA/CPRA | APPI | EU AI Act (2026-08+) |
|---------|------|-----------|------|----------------------|
| Opt-in vs Opt-out | Opt-in (consent first) | Opt-out (collect, allow opt-out) | Opt-in (consent for sensitive) | N/A — risk-tier based |
| Territorial scope | EU residents (worldwide) | CA residents (revenue threshold) | Japan residents + Japan-based operators | EU users (worldwide) |
| Max penalty | €20M or 4% global revenue | $7,500 per intentional violation | ¥100M or criminal penalties | **€35M / 7%** (prohibited), **€15M / 3%** (high-risk) |
| DPO required | Certain organizations | No | No (recommended) | Conformity assessor for high-risk |
| Children's age | <16 (member states may lower to 13) | <16 (COPPA <13) | No specific age threshold | N/A |
| Breach notification | 72h to DPA | No fixed timeline (AG action) | Promptly to PPC | High-risk system serious-incident reporting |

When a project triggers more than one regime, **penalties apply concurrently** — GDPR + EU AI Act on the same EU-user data flow can produce two ceilings, not one. Plan to the strictest applicable rule per regime.

## DPIA Template Structure

```markdown
# Data Protection Impact Assessment

## 1. Processing Description
- **Purpose:** [Why this processing exists]
- **Data categories:** [What PII is processed]
- **Data subjects:** [Whose data]
- **Recipients:** [Who receives data]
- **Retention:** [How long]
- **Cross-border:** [Transfer destinations]

## 2. Necessity & Proportionality
- Is the processing necessary for the stated purpose?
- Could the purpose be achieved with less data?
- Is the lawful basis appropriate?

## 3. Risk Assessment
| Risk | Likelihood | Impact | Score | Mitigation |
|------|-----------|--------|-------|-----------|
| Unauthorized access | [1-5] | [1-5] | [L×I] | [Action] |
| Data breach | [1-5] | [1-5] | [L×I] | [Action] |
| Function creep | [1-5] | [1-5] | [L×I] | [Action] |
| Re-identification | [1-5] | [1-5] | [L×I] | [Action] |

## 4. Measures & Safeguards
- [ ] Encryption at rest and in transit
- [ ] Access controls (role-based)
- [ ] Pseudonymization where possible
- [ ] Audit logging
- [ ] Retention automation
- [ ] DSAR process documented
- [ ] Breach response plan

## 5. Conclusion
- [ ] Residual risk acceptable
- [ ] DPO consulted (if applicable)
- [ ] Review date scheduled
```
