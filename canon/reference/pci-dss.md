# PCI-DSS v4.0 / v4.0.1 Reference

Purpose: Standards-citation-driven assessment against PCI-DSS v4.0 (effective March 31, 2025 — v3.2.1 fully retired) and v4.0.1 (clarifications). Determines Cardholder Data Environment (CDE) scope, selects correct SAQ type or ROC path, evaluates the 12 Requirements, and routes remediation to specialist agents.

## Scope Boundary

- **canon `pci`**: standards-citation-driven assessment. Pin version "PCI-DSS v4.0.1", cite Requirement.Sub-requirement (e.g., `Req 3.5.1`, `Req 8.3.6`), evidence at `file:line`, scope-minimization analysis (tokenization, network segmentation).
- **comply (elsewhere)**: audit-trail, ROC/SAQ submission preparation, Policy-as-Code mapping (OPA), continuous-control monitoring. Canon scopes; Comply executes audit workflow and QSA coordination.
- **cloak (elsewhere)**: privacy-by-design for cardholder PAN/CVV handling — masking, tokenization choice (FPE vs. vault), secure deletion. Overlaps with `Req 3` (Protect Stored Account Data).
- **sentinel (elsewhere)**: static scanning for hardcoded PAN, weak crypto (`Req 3.5`, `Req 6.2.4`), secret leakage.
- **probe (elsewhere)**: DAST and ASV scanning for `Req 11.3` (external/internal vulnerability scans, pentests).
- **crypt (elsewhere)**: cryptographic algorithm selection and key-management design for `Req 3.6`, `Req 3.7`.

## Workflow

```
SURVEY    →  determine cardholder data flow: where PAN enters, transits, rests, leaves
          →  pin "PCI-DSS v4.0.1" + merchant level (1-4) + acceptance channels

PLAN      →  scope CDE: in-scope vs. connected-to vs. out-of-scope systems
          →  select assessment path: SAQ (A/A-EP/B/B-IP/C/C-VT/D-Merchant/D-SP/P2PE) or ROC

ASSESS    →  evaluate 12 Requirements; flag Customized Approach where Defined Approach impractical
          →  every "Compliant" needs evidence; every "Not Applicable" needs documented rationale

VERIFY    →  AOC-ready summary, scope-reduction recommendations, Customized Approach worksheets
          →  flag future-dated requirements (effective dates within 12 months)

PRESENT   →  delegate: Cloak (tokenization/masking), Sentinel (PAN scan, weak crypto),
             Probe (Req 11 scans), Comply (ROC/SAQ submission), Crypt (key management)
```

## 12 Requirements (PCI-DSS v4.0.1)

| # | Requirement | Key Sub-requirements |
|---|-------------|----------------------|
| 1 | Install/maintain network security controls | 1.2, 1.3 (segmentation), 1.4 (untrusted networks) |
| 2 | Apply secure configurations to all system components | 2.2 (config standards), 2.3 (wireless) |
| 3 | Protect stored account data | 3.3 (no SAD post-auth), 3.5 (PAN unreadable), 3.7 (key management) |
| 4 | Protect cardholder data with strong cryptography during transmission | 4.2 (TLS/strong crypto over open networks) |
| 5 | Protect all systems and networks from malicious software | 5.2 (anti-malware), 5.3 (active scanning) |
| 6 | Develop and maintain secure systems and software | 6.2 (secure SDLC), 6.3 (vuln mgmt), 6.4 (public-facing apps WAF/code review) |
| 7 | Restrict access to system components and cardholder data by business need to know | 7.2 (least privilege), 7.3 (access-control system) |
| 8 | Identify users and authenticate access to system components | 8.3 (MFA — expanded in 4.0), 8.4, 8.6 (system/app accounts) |
| 9 | Restrict physical access to cardholder data | 9.3 (personnel), 9.4 (visitors), 9.5 (media) |
| 10 | Log and monitor all access to system components and cardholder data | 10.4 (review), 10.7 (audit log retention 12 months, 3 months online) |
| 11 | Test security of systems and networks regularly | 11.3 (vuln scans — internal + ASV external), 11.4 (pentest), 11.6 (change-detection) |
| 12 | Support information security with organizational policies and programs | 12.3 (risk analysis), 12.8 (TPSP mgmt), 12.10 (incident response) |

## SAQ Type Selection

| SAQ | Merchant Profile | Common Requirements |
|-----|------------------|---------------------|
| A | Card-not-present, fully outsourced (e.g., redirect/iframe to PCI-DSS PSP) | Subset (~20 reqs) |
| A-EP | E-commerce, partial outsourcing (merchant page touches PAN via JS) | Larger subset (~150 reqs) |
| B | Imprint machines or standalone dial-out terminals only | Small subset |
| B-IP | Standalone IP-connected terminals | Subset |
| C | Payment app systems connected to internet, no e-commerce | Subset |
| C-VT | Web-based virtual terminal, no electronic storage | Subset |
| D-Merchant | All others (default) | All 12 Requirements |
| D-SP | Service Providers | All 12 Requirements |
| P2PE | Validated P2PE solution only | Smallest subset |

ROC (Report on Compliance) by QSA is required for: Level 1 merchants (>6M Visa/MC transactions/yr), all Service Providers Level 1, or where acquirer mandates.

## Scope Minimization Patterns

| Technique | Effect | Caveat |
|-----------|--------|--------|
| Tokenization (vault or FPE) | Removes PAN from systems → out of scope | Vault provider must be validated; tokens that can be detokenized stay in scope |
| Network segmentation | Isolates CDE from rest of network | Must be tested annually (Req 11.4.5 for SP, 11.4.6 for merchants) |
| P2PE validated solution | Encrypts at swipe/dip → merchant sees only ciphertext | Only PCI-listed P2PE solutions qualify |
| Hosted payment pages (redirect/iframe) | Browser communicates with PSP, not merchant | Merchant page must not be in PAN path (else SAQ A-EP) |
| Outsourcing to PCI-DSS PSP | Shifts most controls to PSP | Merchant retains Req 12.8 oversight |

## v4.0 Key Changes from v3.2.1

- 51 new requirements (13 effective March 2024, 38 effective March 31, 2025).
- Customized Approach option per Requirement (with risk analysis and Customized Approach Objective).
- Expanded MFA: `Req 8.4.2` requires MFA for all access into CDE (not just remote/admin).
- Targeted risk analysis required for several requirements (`Req 12.3.1`).
- Phishing-resistant authentication, password length 12+ chars (was 7), automated log review tools.

## Anti-Patterns

- Scope creep — assessing entire enterprise instead of CDE + connected-to systems. Inflates effort 5-10×.
- Scope shrinkage — declaring systems "out of scope" without segmentation testing. Default assumption: connected = in scope.
- Citing "PCI-DSS" without version — v3.2.1 retired March 31, 2024; assessing against it in 2025+ produces invalid AOC.
- Choosing SAQ A when JavaScript executes on merchant page — that is SAQ A-EP. Misclassification is a leading cause of e-skimming breaches (Magecart).
- Paper compliance — policy documents without operational evidence. Auditors reject "we have a policy" without log samples, config dumps, drill reports.
- Treating tokenization as automatic scope removal — if the vault is operated by the merchant or tokens are reversible without strong controls, scope persists.
- Audit-only thinking — annual ROC without continuous monitoring. Most breaches occur between audits; v4.0 emphasizes "business-as-usual" controls.
- Copy-paste compensating controls — each compensating control needs its own risk analysis and must meet original requirement intent. Reusing prior-year worksheets without re-justification fails QSA review.
- Assessing against Defined Approach when Customized Approach fits — wastes effort on impossible-to-meet prescriptive requirements when documented-objective approach is acceptable.

## Handoff

- **To Cloak**: PAN masking/tokenization design, secure deletion (`Req 3.2`, `Req 3.5`), data-flow diagrams.
- **To Sentinel**: hardcoded PAN scanning, weak crypto detection (`Req 3.5`, `Req 6.2.4`), secret leakage.
- **To Probe**: ASV external scans (`Req 11.3.2`), internal vuln scans (`Req 11.3.1`), pentest (`Req 11.4`).
- **To Crypt**: key-management design (`Req 3.6`, `Req 3.7`), TLS configuration (`Req 4.2`), HSM selection.
- **To Comply**: ROC/SAQ submission, Policy-as-Code, AOC artifact storage, QSA coordination, TPSP register (`Req 12.8`).
- **To Builder**: technical remediation with Requirement-citation acceptance criteria.
