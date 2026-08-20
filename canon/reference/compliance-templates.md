# Compliance Report Templates

## Executive Summary Template

```markdown
# Compliance Assessment Executive Summary

## Overview

| Attribute | Value |
|-----------|-------|
| Assessment Date | YYYY-MM-DD |
| Assessor | Canon (AI Agent) |
| Target | [Project/System Name] |
| Scope | [Description of what was assessed] |
| Standards | [List of standards assessed against] |

## Compliance Status

| Standard | Target Level | Achieved | Status |
...
```

---

## Detailed Compliance Report Template

```markdown
# Detailed Compliance Assessment Report

## 1. Introduction

### 1.1 Purpose
This report documents the compliance assessment of [Target] against [Standards].

### 1.2 Scope
**In Scope:**
- [Component/Module 1]
- [Component/Module 2]

**Out of Scope:**
- [Excluded items with justification]

...
```
Critical: █████ X
High:     ████████ X
Medium:   ██████████████ X
Low:      ████████████████████ X
```

---

## 3. Detailed Findings

### Finding: CANON-001

| Attribute | Value |
|-----------|-------|
| ID | CANON-001 |
| Standard | [Standard Name] |
| Requirement | [Requirement title] |
| Citation | [Section/Clause number] |
| Severity | Critical / High / Medium / Low |
| Status | ❌ Non-compliant / ⚠️ Partial / ✅ Compliant |
...
```
File: src/path/to/file.ts:42
Code: [Relevant code snippet]
```

**Impact:**
[Description of potential impact if not addressed]

**Recommendation:**
[Specific steps to achieve compliance]

**Compliant Example:**
```typescript
// Example of compliant implementation
```

**Effort Estimate:** [Low / Medium / High]

**Remediation Agent:** [Builder / Sentinel / Palette / etc.]

---

### Finding: CANON-002
[Repeat structure for each finding]

---

## 4. Exemptions and Exceptions

### 4.1 Documented Exemptions
...
```

---

## Finding Template (Single Finding)

```markdown
## Finding: [ID]

### Basic Information

| Field | Value |
|-------|-------|
| **ID** | CANON-XXX |
| **Title** | [Short descriptive title] |
| **Standard** | [Standard name and version] |
| **Requirement** | [Requirement ID/name] |
| **Citation** | [Exact section, clause, or criterion] |
| **Severity** | Critical / High / Medium / Low / Info |
| **Status** | ❌ Non-compliant / ⚠️ Partial / ✅ Compliant |
| **Category** | Security / Accessibility / API / Quality |

...
```typescript
// Non-compliant code example
```

**Standard Requirement (Quote):**
> [Exact quote from the standard]

### Impact Assessment

**Technical Impact:**
[What could go wrong technically]

**Business Impact:**
[Business/user consequences]

**Likelihood:** High / Medium / Low

**Risk Level:** Critical / High / Medium / Low
...
```typescript
// Example of compliant code
```

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

**Estimated Effort:** Low (< 2h) / Medium (2-8h) / High (> 8h)

**Remediation Agent:** Builder / Sentinel / Palette / Gateway

### Verification

**How to Verify:**
1. [Verification step 1]
2. [Verification step 2]

...
```bash
# Command to verify compliance
```

### References

- [Link to standard documentation]
- [Link to implementation guide]
- [Link to related findings]
```

---

## Compliance Tracking Template

```markdown
# Compliance Tracking: [Standard Name]

## Status Dashboard

| Category | Total | ✅ | ⚠️ | ❌ | ➖ | Progress |
|----------|-------|-----|-----|-----|-----|----------|
| Authentication | 10 | 6 | 2 | 1 | 1 | 70% |
| Access Control | 8 | 5 | 2 | 1 | 0 | 75% |
| Input Validation | 12 | 8 | 3 | 1 | 0 | 83% |
| **Overall** | 30 | 19 | 7 | 3 | 1 | **76%** |

## Detailed Status

### Category: [Category Name]

...
```

---

## Quick Audit Checklist Template

```markdown
# Quick Compliance Checklist: [Standard]

## Assessment Information
- **Date:** YYYY-MM-DD
- **Target:** [Project/Component]
- **Assessor:** Canon
- **Standard:** [Standard and version]
- **Level:** [Target compliance level]

## Checklist

### [Category 1]

| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
...
```

---

## Handoff Templates

### Canon → Builder (Implementation)

```markdown
## Canon → Builder Handoff

### Compliance Finding Summary

| Field | Value |
|-------|-------|
| Finding ID | CANON-XXX |
| Standard | [Standard name] |
| Citation | [Section number] |
| Severity | [Critical/High/Medium/Low] |
| Deadline | YYYY-MM-DD |

### Current State

**Location:** `path/to/file.ts:42`
...
```typescript
// Non-compliant implementation
```

**Issue:** [What's wrong]

### Required Change

**Standard Requirement:**
> [Quote from standard]

**Implementation Guidance:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Compliant Example:**
```typescript
// Example implementation that meets the standard
```

### Acceptance Criteria

- [ ] [Criterion 1 - specific and testable]
- [ ] [Criterion 2 - specific and testable]
- [ ] Standard requirement [citation] is satisfied

### Verification Steps

After implementation:
1. Run: `[command]`
2. Verify: [what to check]
3. Expected result: [what success looks like]
```

### Canon → Scribe (Documentation)

```markdown
## Canon → Scribe Handoff

### Documentation Request

| Field | Value |
|-------|-------|
| Purpose | Compliance documentation |
| Standards | [List of standards] |
| Audience | [Internal / External / Auditor] |

### Required Documents

1. **Compliance Summary**
   - Overall compliance status
   - Key findings summary
...
```

---

## NEXUS Compliance Report Format

```markdown
## NEXUS_HANDOFF

- Step: [X/Y]
- Agent: Canon
- Summary: Compliance assessment completed for [target] against [standards]
- Key findings / decisions:
  - Overall compliance: XX%
  - Critical findings: X
  - High findings: X
  - Standards assessed: [list]
- Artifacts (files/commands/links):
  - Compliance report: [path or content]
  - Finding details: [summary]
- Risks / trade-offs:
  - [Non-compliance risks identified]
...
```


---

## Capability Detail (SKILL.md excerpt)

- Domains: Security (OWASP Top 10:2025, OWASP API Security Top 10:2023, ASVS 5.0, NIST CSF 2.0, CIS Controls v8.1, CWE Top 25:2025, NIST SSDF v1.1), Accessibility (WCAG 2.2 / ISO/IEC 40500:2025, WAI-ARIA), API (OpenAPI 3.1.2/3.2, RFC 9110, GraphQL), Quality (ISO/IEC 25010:2023 — 9 characteristics incl. Safety, ISO/IEC 25019:2023 Quality-in-Use, Clean Code, SOLID), Infrastructure (12-Factor, CNCF), AI Agent Security (OWASP Top 10 for Agentic Applications 2026, OWASP LLM Top 10:2025, OWASP MCP Top 10 2025, NIST AI RMF), AI Governance (ISO/IEC 42001:2023 AIMS)

- fix_prompt_generation: Pair every confirmed standards violation routed for remediation with a paste-ready LLM Fix Prompt embedding the cited standard+version+section, gap classification (missing/partial/non-conforming/over-conforming), evidence at file:line, the standard's prescribed remediation, acceptance criteria, ruled-out alternatives, and "what NOT to do". Suppress when a receiving implementation specialist owns the prompt, and withhold in gap-analysis-only mode.

---

**Agent Teams / Subagent pattern (Pattern D: Specialist Team, 2-4 workers):**
When a full compliance audit spans 3+ independent domains or frameworks, use 2-4 domain workers during ASSESS. Each owns one evidence set; Canon merges statuses and cross-framework controls in VERIFY.
- `security-assessor` (general-purpose, sonnet): OWASP/NIST/CIS assessment → security compliance report
- `a11y-assessor` (general-purpose, sonnet): WCAG/WAI-ARIA assessment → accessibility compliance report
- `api-assessor` (general-purpose, haiku): OpenAPI/RFC compliance → API compliance report
- `regulatory-assessor` (general-purpose, sonnet): SOC 2/PCI/HIPAA/ISO control evidence → regulatory matrix
- Shared read: codebase files, `reference/*.md`; exclusive write: per-domain report sections
- Do NOT spawn for single-domain assessments (overhead exceeds benefit).
