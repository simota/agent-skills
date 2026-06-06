# Audit Readiness and Evidence Collection Reference

Purpose: Turn an audit from a quarterly scramble into a continuous, evidence-driven workflow. Cover evidence mapping by control, chain-of-custody, sampling strategy, auditor interview preparation, findings remediation tracking, continuous-audit automation, and the gap-to-remediation playbook. The goal is that on day one of fieldwork the auditor can pull evidence themselves from a shared evidence room without asking the team to "go find it".

## Scope Boundary

- **Oath `audit`**: audit readiness orchestration — evidence architecture, sampling plan, auditor logistics, findings tracking, continuous audit design.
- **Warden (elsewhere)**: V.A.I.R.E. functional quality gates (user-experience quality), not regulatory audit.
- **Crypt (elsewhere)**: cryptographic evidence artifacts such as KMS key rotation logs, HSM attestations, and TLS cipher inventory — Oath consumes, Crypt designs.
- **Vigil (elsewhere)**: detection rule coverage evidence (Sigma/YARA) — Oath cites the coverage in the audit, Vigil authors the rules.
- **Beacon (elsewhere)**: continuous control telemetry pipelines (log shipping, dashboarding).

If the question is "what does the auditor ask for, in what order, and how do we prove it?" stay in `audit`. If the question is "write the detection rule / set up the KMS / build the SLO dashboard", hand off.

## Evidence Tier Model

| Tier | Example | Auditor weight |
|------|---------|----------------|
| 1 — System-generated | Immutable audit logs, IAM policy JSON, CloudTrail events, KMS rotation events | Highest — cannot be retrofitted |
| 2 — Configuration-as-code | Terraform state, GitHub Actions YAML, OPA policies in the repo | High — diffable, signed commits |
| 3 — Ticketing artifacts | Jira / Linear / ServiceNow ticket with approvals and timestamps | Medium — requires change-management policy backing |
| 4 — Screenshots | Console screenshots with URL + timestamp + user | Low — use only when Tier 1-3 unavailable |
| 5 — Attestations | Signed statements, workforce training acknowledgments | Supporting — rarely the primary evidence |

Always prefer the highest available tier. A screenshot of "access review completed" loses every time to a ticket with approver identity and timestamp, which loses to a log line stamped by the IAM provider.

### SOC 2 (2026) and the AI Subservice Carve-Out

By 2026 SOC 2 has shifted in two ways the audit-readiness program needs to reflect:

1. **AI / LLM providers powering production behaviour count as subservice organisations.** Their controls flow into your CSOCs; an auditor will ask whether their SOC 2 (or equivalent) covers the AI scope you actually rely on. Treat their report review as a first-class audit input — same MANIFEST + hash discipline as your own evidence.
2. **Vendor-management evidence is no longer "review the spreadsheet annually".** Auditors now expect **continuous TPRM** under SOC 2 CC9.2 — ongoing monitoring signals (security-score feeds, breach-notice cadence, subprocessor-chain syncs) in addition to the annual SOC 2 PDF review. Point-in-time assessments are graded down.

AI-specific evidence the auditor will request:
- Model version log + change tickets (when the underlying LLM version changed for your service)
- Prompt / completion logging retention policy + access controls
- AI literacy training records (mirrors EU AI Act Art. 4 + becomes load-bearing SOC 2 evidence)
- "Is customer data excluded from provider training?" — contractual evidence, not just a vendor blog post
- Hallucination handling procedure + human-in-the-loop policy for high-risk paths

These items should already exist in your AI-vendor questionnaire (`vendor-risk-assessment.md`); the audit-readiness job is to **link** each to the corresponding control + period in the evidence room.

## Evidence Room Structure

```
audit-evidence/
├── frameworks/
│   ├── soc2-2026/
│   │   ├── CC6.1-logical-access/
│   │   │   ├── design/       # Policies, architecture diagrams
│   │   │   ├── operation/    # Sampled evidence for the audit period
│   │   │   ├── tests/        # Auditor-run tests and results
│   │   │   └── MANIFEST.md   # Control owner, evidence list, hash, timestamps
│   │   └── CC7.2-monitoring/
│   ├── pci-v4/
│   └── iso-27001-2022/
├── shared/                   # Cross-framework evidence (IAM, encryption)
└── chain-of-custody.jsonl    # Append-only log of evidence additions
```

Every file has a SHA-256 in the MANIFEST and an append-only entry in `chain-of-custody.jsonl`. If the auditor later asks "prove this file was not modified after extraction", the hash + signed log line is the answer.

## Workflow

```
READINESS   →  inventory controls in scope, map control → owner → evidence tier
            →  identify gaps (control without evidence, evidence without owner)
            →  generate Prepared-By-Client (PBC) list before auditor arrives

COLLECT     →  automate Tier-1 and Tier-2 extraction on schedule (daily/weekly)
            →  package evidence with manifest, hash, and retention metadata
            →  append to chain-of-custody log; sign with release keys

SAMPLE      →  auditor defines population and sample size — you prepare extraction
            →  population must be complete; missing rows = audit failure
            →  preserve the entire population, not just the sample (re-sampling)

FIELDWORK   →  auditor interviews + walkthroughs; control owner presents evidence
            →  answer one question at a time; provide evidence, not narrative
            →  capture every Information Request (IR) in a tracker

REMEDIATE   →  classify findings: design gap / operating gap / observation
            →  map each finding to remediation owner, root cause, timeline
            →  retest once remediated; archive evidence of closure
```

## Sampling Strategy

Auditors sample from populations to verify operating effectiveness over the audit period. The population must be complete and reproducible.

| Population frequency | AICPA typical sample size | Example |
|----------------------|---------------------------|---------|
| Daily (>= 250/year) | 25 | Daily vulnerability scans |
| Weekly (52/year) | 5 | Weekly access reviews |
| Monthly (12/year) | 2 | Monthly patch cycles |
| Quarterly (4/year) | 2 | Quarterly user access review |
| Annual (1/year) | 1 | Annual policy re-approval, DR test |
| On-event | All or judgmental | Every termination in the period |

If you cannot produce the full population, the auditor expands sample size or issues an exception. Populations built with `gap-less` cursors (auto-incrementing IDs + retention check) prove completeness.

## Auditor Interview Prep

Control owners must be able to answer three questions in under two minutes each:

1. **What is the control and why does it exist?** (Risk → objective → control language.)
2. **How does the control operate day-to-day?** (Who triggers, who approves, where logged.)
3. **How do we know it is working?** (Evidence source, frequency, monitoring alert.)

Dry-run these interviews one week before fieldwork. The most common failure mode is a control owner who cannot name the regulation section their control covers.

## Findings Remediation Tracking

| Field | Content |
|-------|---------|
| Finding ID | e.g., `SOC2-2026-F001` |
| Framework / control | `SOC2 CC6.2` |
| Severity | Critical / High / Medium / Low |
| Type | Design gap / Operating gap / Observation |
| Root cause | One-line causal statement, not symptom |
| Owner | Named individual + accountable executive |
| Target date | Calendar date — not "ASAP" |
| Evidence of closure | Path in evidence room + hash |
| Retest status | Open / Retested-Pass / Retested-Fail |

Track each finding to closure even if the audit report is already signed. Repeat findings across audits are a red-flag pattern auditors escalate.

## Continuous Audit Automation

Move from point-in-time to continuous with three layers:

1. **Automated evidence collection** — scheduled jobs pull IAM policy, CloudTrail rollups, Kubernetes admission webhook decisions, and OPA policy hits into the evidence room daily.
2. **Control health dashboards** — each control publishes a health metric (pass rate, drift count, mean time to remediate). Thresholds trigger on-call.
3. **48-hour drift flag** — per SOC 2 CC4.1-CC4.2, a deficiency must be detectable within 48 hours. Alert path = on-call → control owner → evidence of remediation appended.

## Gap-to-Remediation Playbook

```
GAP IDENTIFIED
  └─> classify (design / operating)
        └─> assign owner + accountable exec
              └─> root cause analysis (5 whys, documented)
                    └─> remediation: code / policy / process
                          └─> evidence of remediation
                                └─> retest
                                      └─> close finding, update trend report
```

A gap is not closed when the fix ships — it is closed when the retest evidence is filed.

## Anti-Patterns

- Building the evidence room for the first time one month before fieldwork — quality and completeness collapse under time pressure.
- Letting control owners write narrative answers instead of pointing to evidence artifacts.
- Sampling from an incomplete population ("we only kept 6 months of logs") — auditor expands scope or issues an exception.
- Screenshot-only evidence for automatable controls — auditors downgrade confidence.
- Treating findings as closed at remediation rather than retest — rubs against Type II operating-effectiveness requirements.
- Using the same evidence for SOC 2 and PCI-DSS without scope analysis — PCI CDE scope is narrower; irrelevant SOC 2 evidence adds noise and can expand PCI scope unintentionally.
- Missing chain-of-custody log entries when copying evidence between tools — auditor questions authenticity.
- Single-person knowledge for a control ("only X knows how this works") — if X is unavailable during fieldwork, the control fails to demonstrate.

## Handoff

**To Builder** — automation to extract Tier-1 evidence (CloudTrail digest jobs, IAM snapshot jobs, KMS rotation event exporters, access-review ticket generators).

**To Beacon** — control health dashboards, drift alerts, SLA burn for remediation timelines, on-call routing for 48-hour flags.

**To Scribe** — PBC list, control narratives, control matrix, findings remediation report, post-audit lessons-learned.

**To Gear** — CI/CD policy gates that block deploys when control-health signal is red; evidence-collection cron jobs.

**To Vigil** — detection rule coverage matrix for CC7.2 / PCI Req 10, threat hunting evidence for audit period.
