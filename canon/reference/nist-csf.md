# NIST Cybersecurity Framework (CSF) 2.0 Reference

Purpose: Standards-citation-driven assessment against NIST CSF 2.0 (released February 26, 2024). Maps each control to the six Functions (Govern, Identify, Protect, Detect, Respond, Recover), assigns Implementation Tier (1-4), and produces Current vs. Target Profile gaps with Subcategory-level evidence and remediation hand-offs.

## Scope Boundary

- **canon `nist`**: standards-citation-driven assessment. Pin version "NIST CSF 2.0", cite Function.Category.Subcategory (e.g., `GV.OC-01`, `PR.AA-05`), evidence at `file:line`, and Tier rating per Category.
- **oath (elsewhere)**: audit-trail and Policy-as-Code. Once Canon surfaces gaps, Oath owns control evidence collection (OSCAL packages), continuous-control monitoring, and auditor-facing reports.
- **cloak (elsewhere)**: privacy-by-design implementation. CSF 2.0 references NIST Privacy Framework — Cloak owns privacy-engineering controls (PII flow maps, DPIA, consent) when overlap occurs (`ID.RA`, `PR.DS`).
- **sentinel (elsewhere)**: static security scanning. SAST/secret detection feeds evidence into `DE.CM-01`, `PR.DS-01`, but Sentinel does not assess Profile/Tier alignment.
- **probe (elsewhere)**: dynamic security testing for `DE.AE` / `DE.CM` validation.

## Workflow

```
SURVEY    →  scope CSF: organizational context (GV.OC), critical assets, risk tolerance
          →  pin version "NIST CSF 2.0" + Informative References (SP 800-53r5, ISO 27001:2022)

PLAN      →  select Categories applicable to scope (not all 106 Subcategories apply)
          →  define Target Profile (desired Tier per Category) before assessing Current

ASSESS    →  per Subcategory: rate Tier 1 (Partial) → 4 (Adaptive), evidence at file:line
          →  Govern Function first — without GV, other Functions lack policy backing

VERIFY    →  Current Profile vs. Target Profile gap report
          →  prioritize gaps by risk × business impact, not Tier delta alone

PRESENT   →  delegate: Oath (audit/OSCAL), Cloak (privacy controls), Sentinel (SAST gaps),
             Probe (DAST validation), Builder (technical remediation)
```

## Six Functions × Implementation Tiers

| Function | Code | Focus | Example Categories |
|----------|------|-------|-------------------|
| Govern | GV | Cybersecurity strategy, expectations, policy (NEW in 2.0) | GV.OC, GV.RM, GV.RR, GV.PO, GV.OV, GV.SC |
| Identify | ID | Asset, risk, supply chain understanding | ID.AM, ID.RA, ID.IM |
| Protect | PR | Safeguards to limit/contain impact | PR.AA, PR.AT, PR.DS, PR.PS, PR.IR |
| Detect | DE | Find anomalies and adverse events | DE.CM, DE.AE |
| Respond | RS | Action on detected incidents | RS.MA, RS.AN, RS.CO, RS.MI |
| Recover | RC | Restore assets and operations | RC.RP, RC.CO |

| Tier | Name | Definition |
|------|------|------------|
| 1 | Partial | Ad hoc, reactive, limited awareness |
| 2 | Risk Informed | Risk-aware practices but not org-wide |
| 3 | Repeatable | Formal policy, organization-wide consistency |
| 4 | Adaptive | Continuous improvement, predictive, lessons-learned loop |

## Subcategory Evidence Examples

| Subcategory | Requirement | Typical Evidence |
|-------------|-------------|------------------|
| `GV.OC-01` | Org mission understood, informs cyber risk | Risk-tolerance statement, board minutes |
| `GV.SC-07` | Risks of suppliers monitored | Vendor risk register, SBOM at `package.json` |
| `ID.AM-01` | Inventories of hardware managed | CMDB export, IaC tag policy at `terraform/tags.tf` |
| `PR.AA-05` | Access permissions managed (least privilege) | RBAC matrix at `auth/policy.yaml:42` |
| `PR.DS-01` | Data-at-rest protected | KMS config at `infra/kms.tf`, encryption flag |
| `DE.CM-01` | Networks/systems monitored for adverse events | SIEM rules, log retention policy |
| `RS.MA-01` | Incident response plan executed during/after incident | Runbook at `docs/ir-playbook.md` |
| `RC.RP-01` | Recovery plan executed | RTO/RPO targets, last DR drill report |

## Profile and Tier Mapping Pattern

CSF 2.0 introduces **Community Profiles** (sector-specific, e.g., Manufacturing, Cloud Services) and **Organizational Profiles** (Current vs. Target). Recommend:

1. Adopt a Community Profile as Target baseline (if available for the sector).
2. Score Current Tier per Category (not per Subcategory — too granular).
3. Gap = Target Tier − Current Tier; flag deltas of `≥2` as priority remediation.
4. Quick Start Guides (released March 2024) provide enterprise-, small-business-, and supply-chain-specific starting points.

## Anti-Patterns

- Assessing without Govern function — CSF 2.0 added GV precisely because Identify-through-Recover lacks policy backing without it. Skipping GV invalidates Tier ratings.
- Treating Tier 4 as universal goal — Tier alignment must match risk tolerance. Forcing Tier 4 on low-risk Categories wastes budget.
- Citing "NIST CSF" without version — 1.1 (2018) had 5 Functions and 23 Categories; 2.0 has 6 Functions and 22 Categories. Findings against the wrong version are invalid.
- Confusing Tier with maturity model — Tiers describe risk-management rigor, not capability maturity. Do not equate Tier 4 with CMMI Level 5.
- Copy-paste Subcategory list — CSF is voluntary and tailorable. Listing all 106 Subcategories without scoping wastes assessor effort and dilutes findings.
- Paper compliance — passing an audit on policy text alone, with no operational evidence (logs, configs, drill reports). Always require `file:line` or system-level evidence.
- Audit-only thinking — point-in-time CSF assessment without continuous-monitoring tooling (OSCAL, SIEM, OPA). FedRAMP 20x and Gartner trajectory mandate continuous compliance.
- Skipping Informative References — SP 800-53r5, ISO 27001:2022, CIS Controls v8 mappings turn abstract Subcategories into testable controls. Without them, assessments become subjective.

## Handoff

- **To Oath**: gaps requiring audit trail, OSCAL package generation, or Policy-as-Code (OPA/Rego). Oath owns SOC 2 / ISO 27001 mapping and continuous-control monitoring built on CSF assessment.
- **To Cloak**: gaps in `ID.RA` (privacy risk), `PR.DS` (data minimization), `GV.SC` (third-party data sharing) — privacy-by-design implementation.
- **To Sentinel**: `PR.DS-01` (encryption), `PR.PS-06` (secure development), `DE.CM-01` (log/secret detection) — SAST evidence collection.
- **To Probe**: `DE.AE`, `RS.AN-03` validation through DAST and pentesting.
- **To Builder**: technical remediation of Subcategory-level findings with explicit acceptance criteria (Target Tier, evidence type).
