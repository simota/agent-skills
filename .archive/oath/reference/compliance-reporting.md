# Compliance Reporting Reference

## Report Types

| Report Type | Purpose | Audience | Frequency |
|-------------|---------|----------|-----------|
| **Gap Analysis** | Identify compliance gaps before audit | Engineering + Management | Pre-audit (3-6 months before) |
| **Readiness Assessment** | Confirm audit readiness | Management + Auditor | 1 month before audit |
| **Compliance Matrix** | Track control status across frameworks | Engineering | Continuous |
| **Remediation Roadmap** | Prioritized action plan for gaps | Engineering | After gap analysis |
| **Evidence Package** | Compiled evidence for auditor | Auditor | During audit |

---

## Compliance Matrix Template

```markdown
## Compliance Matrix: [Project Name]

**Date:** YYYY-MM-DD
**Frameworks:** [SOC2 | PCI-DSS v4.0 | HIPAA | ISO 27001:2022]
**Scope:** [Description of assessment scope]

### Summary

| Framework | Total Controls | Implemented | Partial | Missing | N/A | Compliance % |
|-----------|---------------|-------------|---------|---------|-----|-------------|
| SOC2 | XX | XX | XX | XX | XX | XX% |
| PCI-DSS v4.0 | XX | XX | XX | XX | XX | XX% |
| HIPAA | XX | XX | XX | XX | XX | XX% |
| ISO 27001:2022 | XX | XX | XX | XX | XX | XX% |

### Critical Gaps (Severity: Critical/High)

| # | Framework | Requirement | Status | Gap Description | Remediation | Owner | Target Date |
|---|-----------|-------------|--------|-----------------|-------------|-------|-------------|
| 1 | PCI-DSS Req 3.4 | Encrypt stored PAN | Missing | PAN stored in plaintext in orders table | Implement column-level encryption | Backend team | YYYY-MM-DD |
| 2 | HIPAA §164.312(b) | Audit controls | Partial | Audit logging exists but no ePHI access tracking | Add ePHI access audit events | Platform team | YYYY-MM-DD |

### Detailed Control Assessment

[Include per-control assessment using template from control-mapping.md]
```

---

## Gap Analysis Report Template

```markdown
## Gap Analysis Report

### Executive Summary
- **Overall compliance posture:** [Strong | Adequate | Needs Improvement | Critical Gaps]
- **Critical gaps:** [count]
- **High-priority gaps:** [count]
- **Estimated remediation effort:** [person-weeks]
- **Recommended audit timeline:** [date range]

### Scope
- **Frameworks assessed:** [list]
- **Systems in scope:** [list]
- **Data types:** [cardholder data, ePHI, PII, confidential]
- **Third parties:** [list of subprocessors]

### Findings by Severity

#### Critical (Immediate action required)
1. **[Finding title]**
   - Framework: [requirement reference]
   - Current state: [description]
   - Required state: [description]
   - Risk: [impact if unaddressed]
   - Remediation: [specific action]
   - Effort: [estimate]
   - Agent: [Builder | Sentinel | Gear | Beacon]

#### High (Action within 1 week)
[Same structure]

#### Medium (Action within 1 month)
[Same structure]

#### Low (Backlog)
[Same structure]

### Remediation Roadmap

| Phase | Timeline | Actions | Dependencies |
|-------|----------|---------|-------------|
| Phase 1: Critical | Week 1-2 | [Critical gap fixes] | [none] |
| Phase 2: High | Week 3-4 | [High-priority fixes] | Phase 1 |
| Phase 3: Medium | Month 2-3 | [Medium-priority fixes] | Phase 2 |
| Phase 4: Polish | Month 4 | [Low-priority + documentation] | Phase 3 |

### Risk Register

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
| [Risk description] | H/M/L | H/M/L | [Mitigation action] | [Owner] |
```

---

## Evidence Collection Guide

### Evidence Types by Framework

| Evidence Category | SOC2 | PCI-DSS | HIPAA | ISO 27001 |
|------------------|------|---------|-------|-----------|
| Access control configs | IAM policies, RBAC rules | CDE access lists, MFA config | ePHI access policies | Access control policies |
| Encryption configs | KMS policies, TLS config | PAN encryption, key management | ePHI encryption | Cryptographic controls |
| Audit log samples | Log entries, alerting rules | CHD access logs, admin logs | ePHI access/modification logs | Security event logs |
| Change management | PR history, CI/CD config | Change control procedures | System update records | Change management records |
| Incident response | IR plan, incident records | IR plan, test results | Breach notification records | Incident management records |
| Training records | Security training completion | PCI awareness training | HIPAA workforce training | InfoSec awareness records |
| Risk assessment | Risk register, treatment plan | Annual risk assessment | Risk analysis documentation | Risk assessment, SoA |
| Vendor management | Vendor assessments | Service provider monitoring | BAA inventory | Supplier assessments |

### Automated Evidence Collection

```yaml
# Evidence collection schedule
daily:
  - audit_log_sample: "Export 24h of audit events"
  - access_review_snapshot: "Current user permissions dump"

weekly:
  - vulnerability_scan_report: "SAST/DAST results"
  - dependency_audit: "CVE scan results"

monthly:
  - access_review: "User access review completion"
  - compliance_dashboard_snapshot: "Current compliance posture"

quarterly:
  - penetration_test_report: "External/internal pentest results"
  - risk_assessment_update: "Risk register review"

annually:
  - full_compliance_audit: "Comprehensive control assessment"
  - policy_review: "All security policies reviewed and updated"
  - dr_test_report: "Disaster recovery test results"
```

---

## Remediation Priority Matrix

| Impact | Critical Gap | High Gap | Medium Gap | Low Gap |
|--------|------------|----------|------------|---------|
| Data breach risk | P0 - Immediate | P1 - 48h | P2 - 1 week | P3 - 2 weeks |
| Audit failure risk | P1 - 48h | P2 - 1 week | P3 - 2 weeks | P4 - Backlog |
| Operational risk | P2 - 1 week | P3 - 2 weeks | P4 - Backlog | P5 - Nice to have |
| Documentation only | P3 - 2 weeks | P4 - Backlog | P5 - Nice to have | P5 - Nice to have |
