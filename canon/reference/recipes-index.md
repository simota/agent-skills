# Canon Recipe Registry

The full Recipe table for `canon`. `canon/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| OWASP Review | `owasp` | ✓ | OWASP Top 10 / ASVS security standards assessment | `reference/security-standards.md` |
| WCAG Accessibility | `wcag` | | WCAG 2.2 / WAI-ARIA accessibility assessment | `reference/accessibility-standards.md` |
| OpenAPI Compliance | `openapi` | | OpenAPI 3.1 / RFC 9110 API standards compliance check | `reference/api-standards.md` |
| ISO 25010 Quality | `iso` | | ISO/IEC 25010:2023 quality characteristics assessment (SOLID/Clean Code) | `reference/quality-standards.md` |
| Gap Analysis | `gap` | | Multi-standard gap analysis, audit report generation | `reference/compliance-templates.md` |
| NIST CSF | `nist` | | NIST CSF 2.0 (Govern/Identify/Protect/Detect/Respond/Recover) Tier and Profile assessment | `reference/nist-csf.md` |
| PCI-DSS | `pci` | | PCI-DSS v4.0.1 12-Requirement compliance, CDE scoping, SAQ/ROC selection | `reference/pci-dss.md` |
| GDPR | `gdpr` | | GDPR (Reg. (EU) 2016/679) Articles 5/6/7/13/17/25/30/32/33/35 data-protection assessment | `reference/gdpr-compliance.md` |
| Regulatory Assessment | `regulatory` | | Select and scope the applicable regulatory framework before dispatching to its specific assessment | `reference/regulatory-frameworks.md` |
| SOC 2 Assessment | `soc2` | | Type I/II readiness, TSC mapping, CUECs/CSOCs, operating-effectiveness evidence | `reference/regulatory-frameworks.md` |
| HIPAA Assessment | `hipaa` | | Administrative, physical, technical safeguards; ePHI/BAA and NPRM readiness | `reference/regulatory-frameworks.md` |
| ISO 27001 Assessment | `iso27001` | | ISO 27001:2022 Annex A mapping, SoA, and risk-treatment alignment | `reference/regulatory-frameworks.md` |
| Policy as Code | `policy` | | OPA/Rego, Kyverno, Conftest, and CI/CD compliance gates | `reference/regulatory-policy-as-code.md` |
| Audit Readiness | `audit` | | Evidence room, chain of custody, sampling, interviews, findings retest, continuous audit | `reference/regulatory-audit-readiness.md` |
| Vendor Risk | `vendor` | | Vendor tiering, contracts, questionnaires, SOC 2 review, monitoring, subprocessors | `reference/regulatory-vendor-risk-assessment.md` |
| Terms of Service | `tos` | | ToS clause coverage, risk, and proposed wording | `reference/legal-document-checklists.md` |
| Privacy Policy | `privacy` | | APPI/GDPR/CCPA privacy-policy coverage and data-practice consistency | `reference/legal-document-checklists.md` |
| Tokushoho | `tokushoho` | | Japan Specified Commercial Transactions Act notation check | `reference/legal-document-checklists.md` |
| Legal Gap Analysis | `legal-gap` | | Pre-launch or multi-document consistency and missing-clause review | `reference/legal-review-patterns.md` |
| DPA Review | `dpa` | | GDPR Art. 28 clauses, roles, subprocessors, SCC modules, TIA, audit rights, and breach SLA | `reference/dpa-review.md` |
| EULA Review | `eula` | | License grant, restrictions, IP, OSS, warranties, indemnity, and jurisdiction-specific enforceability risks | `reference/eula-review.md` |
| Cookie Consent | `cookie` | | Banner UX, policy inventory, IAB TCF, categorization, scanner-policy diff, and opt-in/opt-out divergence | `reference/cookie-consent.md` |
| App Store Disclosures | `appstore` | | DSA trader, DMA anti-steering, third-party AI consent, Play AI labels, and EAA statement coverage | `reference/legal-document-checklists.md` |
| Advertising Claims | `claims` | | Advisory substantiation and disclosure coverage for superlatives, endorsements, health, price, and self-preferencing claims | `reference/legal-document-checklists.md` |

---

Behavior notes per Recipe:

| Recipe | Non-negotiable behavior |
|--------|-------------------------|
| `owasp` / `wcag` / `openapi` / `iso` / `nist` | Pin the current version and use the domain reference; WCAG requires manual review; NIST starts with Govern. |
| `gap` | Consolidate independent domains only when 3+ are in scope. |
| `pci` | Scope CDE, select SAQ/ROC, assess v4.0.1, and preserve AOC/QSA evidence needs. |
| `gdpr` | Cite Article+paragraph; include EU AI Act tier/timeline; route implementation by domain. |
| `regulatory` | Identify the governing jurisdiction and framework, then dispatch to `soc2`, `pci`, `hipaa`, `iso27001`, `gdpr`, `policy`, `audit`, or `vendor`; do not default regulatory work to `owasp`. |
| `soc2` | Separate Type I design from Type II operation; map TSC, CUECs/CSOCs, exceptions, and period evidence. |
| `hipaa` | Assess safeguards, ePHI, and BAA scope; label NPRM items as planning baseline. |
| `iso27001` | Use 2022 only; map 93 Annex A controls to SoA and risk treatment. |
| `policy` / `audit` / `vendor` | Specify executable controls, highest-tier evidence, retest/monitoring, and tier-driven vendor gates; delegate implementation. |
| `tos` / `privacy` / `tokushoho` / `legal-gap` | Run the complete relevant checklist, verify citations, assign per-finding risk, and propose wording; use a consistency matrix for multiple documents. |
| `dpa` / `eula` / `cookie` / `appstore` | Identify the recipe-specific scope first, then load only its reference and the shared checklist. |
| `claims` | Report `rule coverage verified`, never `claim approved`; insufficient substantiation routes to the accountable human and qualified counsel before blocking release. |
