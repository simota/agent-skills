# Third-Party Vendor Risk Assessment Reference

Purpose: Build a defensible third-party risk management (TPRM) program that keeps pace with SOC 2 CC9.2, PCI-DSS Req 12.8, HIPAA §164.308(b), ISO 27001 A.5.19-A.5.22, and GDPR Art. 28 expectations. Cover vendor inventory, tier classification, DPA / BAA signing, SIG / CAIQ questionnaire handling, SOC 2 report review, ongoing monitoring cadence, and subprocessor chain visibility. Every in-scope vendor has a tier, a contract, and a re-review date — no exceptions.

## Scope Boundary

- **Comply `vendor`**: vendor risk program design — inventory, tier policy, contract requirements, questionnaire process, SOC 2 report review, monitoring cadence, findings tracking.
- **Warden (elsewhere)**: V.A.I.R.E. functional quality gates on internal product, not vendor qualification.
- **Crypt (elsewhere)**: cryptographic architecture — asked when reviewing a vendor's encryption claims or key management design; Comply consumes the verdict.
- **Vigil (elsewhere)**: threat-hunt a vendor after a compromise; Comply runs the program that catches it earlier.
- **Sentinel (elsewhere)**: scan vendor SDKs you embed for vulnerabilities.
- **Cloak (elsewhere)**: privacy-specific vendor review (processor / sub-processor mapping under GDPR Art. 28) — pairs with `vendor` when personal data is in scope.

If the question is "should we sign with this vendor, what tier, and how often do we re-review?" stay in `vendor`. If it is "pen-test the vendor's API" or "review their encryption code", hand off.

## Vendor Inventory

Every vendor that touches production systems, customer data, or regulated environments appears in a single registry. Shadow SaaS (expensed-as-reimbursement tools) is the biggest audit hole — sweep procurement and SSO logs quarterly.

| Field | Content |
|-------|---------|
| Vendor name | Legal entity, not brand |
| Service description | What they do for us, in one sentence |
| Owner | Internal business owner + technical owner |
| Data shared | Categories (customer PII, employee PII, CHD, ePHI, source code, telemetry) |
| Processing location | Region(s) — feeds transfer-mechanism analysis |
| Tier | Critical / High / Medium / Low (see matrix) |
| Contracts | MSA, DPA, BAA, SCC, order form — with signed dates |
| Last assessment | Date + outcome + evidence path |
| Next review | Calendar date based on tier cadence |
| Subprocessors | Their processor chain, last synced |

## Tier Classification Matrix

| Tier | Criteria (any one triggers) | Controls required |
|------|----------------------------|-------------------|
| Critical | Processes regulated data (CHD/ePHI/special-category), part of the authentication path, outage would cause customer-visible incident in < 1h, **or hosts a foundation model that powers a user-facing feature** (treat as a subservice organization, see AI vendor section) | SOC 2 Type II + pentest summary + SIG-Core, annual on-site or deep-dive, continuous monitoring, contractual right to audit |
| High | Handles customer PII at rest, privileged infrastructure access (CI/CD, production IAM) | SOC 2 Type II or ISO 27001, SIG-Lite, annual review, subprocessor sync |
| Medium | Internal corporate data, limited PII, non-production access | Attestation letter or CAIQ, biennial review |
| Low | No data exchange, marketing tools, internal productivity | Lightweight review at onboarding, event-driven re-review |

Down-tiering a vendor requires written justification from the business owner and security lead. Up-tiering is automatic when the vendor's scope changes.

### AI Vendor Risk (2026 must-have)

By 2026 the SOC 2 / TPRM community treats AI/LLM providers as a distinct vendor class. Two consequences for the inventory and tier matrix:

1. **An LLM provider that powers production behaviour is a subservice organisation, not a "tool"**. Their SOC 2 (or equivalent) becomes part of your own SOC 2 story; their controls flow into your CSOCs. Tier them at **Critical** by default.
2. **AI-specific questionnaire items are now standard** alongside SIG / CAIQ — auditors expect to see answers on:
   - Model versioning policy (when did the version change; how is it pinned)
   - Prompt + completion logging retention and access controls
   - Training-data lineage and licence claims (Art. 53 EU AI Act for GPAI)
   - Hallucination handling and human-in-the-loop policy
   - Sub-processor chain for LLM hosting (cloud region, GPU tenancy, fine-tuning data residence)
   - **AI literacy training records** mirroring Art. 4 of the EU AI Act
   - Data-usage clause: is your input data excluded from provider training?

Customer procurement teams in 2026 increasingly refuse to open commercial conversations without an in-date SOC 2 Type II that covers the AI/LLM scope explicitly — the AI questionnaire is the new gating step before commercial alignment.

## Contract Requirements

| Contract | When required | Key clauses |
|----------|--------------|-------------|
| MSA | All vendors | Liability cap, indemnity, termination, data return/deletion |
| DPA (GDPR Art. 28) | Any processor of personal data | Purpose limitation, subprocessor notice, audit right, SCC incorporation |
| BAA (HIPAA §164.314) | Any business associate handling ePHI | Permitted uses, safeguards, subcontractor BAA flow-down, breach notice within agreed window (24h under proposed 2026 Security Rule) |
| SCC 2021 | Non-adequate country transfers | Correct module (C2P / P2P / etc.), Annex I-III completed, TIA attached |
| Security addendum | Critical / High tier | Encryption requirements, incident notification window, pentest frequency, right-to-audit |

Never onboard a vendor touching regulated data before the relevant contract is countersigned. "We'll get the BAA next week" is how HIPAA breaches compound.

## Questionnaire Handling

| Questionnaire | Use when | Pages | Notes |
|---------------|----------|-------|-------|
| SIG-Core (Shared Assessments) | Critical / High tier, annual | 800+ | Deep; pair with evidence attachments |
| SIG-Lite | High / Medium tier | ~250 | Good default; extensible |
| CAIQ (CSA) | SaaS cloud providers | ~260 | Map to CCM controls; useful for cloud stack |
| Custom | Never first choice | — | Reserve for gaps the standards miss |

Store completed questionnaires in the evidence room with a response date, reviewer identity, and delta-vs-prior-year analysis. A questionnaire answered "yes" every year with no deltas is a signal the vendor is not tracking their own program.

## SOC 2 Report Review Checklist

Do not merely file the PDF — review actively:

1. **Scope** — does the report cover the system you consume? Trust Service Criteria included?
2. **Period** — Type II period overlaps your audit period; gap-period letter if needed.
3. **CUEC / CSOC** — Complementary User Entity Controls and Complementary Subservice Organization Controls: **you are responsible for these**. Enumerate them and map to your own controls.
4. **Exceptions** — every finding by the vendor's auditor; assess residual risk.
5. **Subservice organizations** — inclusive vs carve-out method; if carve-out, review the subservice's SOC 2 as well.
6. **Management response** — serious exceptions must have remediation committed.
7. **Bridge letter** — covers the gap between report end and your reliance date.

Output a short internal memo per report: scope match, period, CUECs owned, exceptions of concern, subservice posture, next review trigger.

## Ongoing Monitoring Cadence

```
CRITICAL  →  quarterly control-health check (uptime + security posture)
          →  annual SOC 2 / pentest summary refresh
          →  real-time subprocessor notifications (DPA clause)
          →  immediate review on breach notice / CVE affecting vendor / M&A event

HIGH      →  semi-annual check-in
          →  annual SOC 2 / ISO cert refresh
          →  30-day window on new subprocessors

MEDIUM    →  annual attestation
          →  event-driven on change

LOW       →  biennial review
          →  event-driven only
```

Event triggers that force re-review regardless of tier: data breach at the vendor, ownership change (acquisition, bankruptcy), material change in the service, new regulatory requirement, repeated SLA misses.

## Subprocessor Chain Visibility

GDPR Art. 28(4) and similar obligations require the prime processor to be liable for its subprocessors. Maintain a tree, not a list:

```
Your company
  └─ Vendor A (prime processor)
       ├─ Subprocessor A1 (hosting — AWS us-east-1)
       ├─ Subprocessor A2 (email — SendGrid)
       └─ Subprocessor A3 (analytics — Segment)
            └─ Sub-subprocessor A3.1 (warehousing — Snowflake)
```

Require vendors to publish and version their subprocessor list, and to notify you with an objection window (typically 30 days) before adding a new one. Capture sub-subprocessors for critical-tier vendors where the chain reaches regulated data.

## Anti-Patterns

- Relying on vendor marketing claims ("enterprise-grade security") without a SOC 2 or ISO 27001 report.
- Signing a DPA without completing Annex III (list of subprocessors) — the agreement is incomplete.
- Treating SOC 2 as binary pass/fail — ignoring exceptions, CUECs, and subservice carve-outs is the silent audit failure.
- Using the same tier cadence for every vendor — critical vendors need quarterly eyes on them.
- Shadow SaaS not in the registry — the vendor you do not know about is the one that leaks customer data.
- Letting contract renewals roll forward without re-review — multi-year auto-renewal freezes vendor posture.
- Accepting a Type I report where Type II is needed — Type I only covers control design, not operation.
- Ignoring the bridge letter and relying on a SOC 2 whose period ended eight months ago.
- Confusing "DPA signed" with "subprocessor chain mapped" — the second is ongoing work.

## Handoff

**To Cloak** — subprocessor map under GDPR Art. 28, international transfer analysis for vendors in non-adequate countries, DPIA inputs for high-risk processing.

**To Crypt** — validate vendor cryptographic claims (encryption at rest, key custody, HSM attestation, BYOK / CMEK options).

**To Sentinel** — scan vendor SDKs / libraries embedded in your product for CVEs.

**To Builder** — vendor inventory registry implementation, webhook intake for subprocessor notifications, SSO-log to registry sweeper.

**To Beacon** — vendor health signal dashboards, SLA monitoring, alert paths on vendor status-page incidents.

**To Scribe** — vendor risk policy, tier classification standard, SOC 2 review memo template, subprocessor notice template.
