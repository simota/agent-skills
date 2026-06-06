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
