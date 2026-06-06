# Triage Postmortem Templates Reference

Templates for postmortem documentation and incident reports.

Purpose: Read this when Triage must produce an internal postmortem, an external PIR, or an executive summary after incident resolution.

Contents:
- `Internal Postmortem Template`: technical retrospective with timeline, root cause, and action items
- `Professional Incident Report (PIR) Template`: customer or executive facing incident report
- `Executive Summary Only Template`: short external or leadership-ready summary
- `Postmortem vs PIR Comparison`: audience and tone differences

## AI-Assisted Drafts (2026)

By 2026 most incident platforms (incident.io AI SRE, Rootly AI SRE, Datadog Bits AI SRE, Howie / Resolve KG) generate a **first-draft postmortem** from the investigation transcript automatically. Treat the draft as a starting point, never as a final deliverable:

- A named **human editor of record** signs the postmortem before publication; the agent's signature does not transfer.
- Every numeric impact figure (users affected, dollars at risk, requests dropped) must trace to a query in the appendix — unsourced figures fail review.
- Blamelessness remains a human judgement: the agent flags tone, a reviewer enforces it.
- Investigation transcript IDs are required in the appendix so the chain telemetry → diagnosis → postmortem → action items is traceable end-to-end.

See `beacon/reference/incident-learning-postmortem.md` for the full AI-assisted postmortem operating rules.

## Internal Postmortem Template

```markdown
## Incident Postmortem: [Title]

### Incident Summary
| Field | Value |
|-------|-------|
| Incident ID | INC-YYYY-NNNN |
| Severity | SEV[1-4] |
| Duration | [start] to [end] (X hours Y minutes) |
| Impact | [summary of impact] |
| Teams Involved | [list] |
| Status | Resolved / Monitoring |

### Timeline (UTC)

| Time | Event |
|------|-------|
| HH:MM | [First symptom detected] |
| HH:MM | [Incident acknowledged] |
| HH:MM | [Investigation started] |
| HH:MM | [Root cause identified] |
| HH:MM | [Mitigation applied] |
| HH:MM | [Service restored] |
| HH:MM | [Incident closed] |

### Impact Analysis

**Users Affected:** [count/percentage]
**Features Affected:** [list]
**Data Impact:** [none/corrupted/lost - details]
**Business Impact:** [revenue/reputation/compliance]

### Root Cause

**What happened:**
[Detailed technical explanation of the root cause]

**Why it happened:**
[5 Whys analysis or contributing factors]

1. Why? [First level]
2. Why? [Second level]
3. Why? [Third level]
4. Why? [Fourth level]
5. Why? [Root cause]

### Detection

**How was it detected?** [Monitoring alert / User report / Automated check]
**Detection delay:** [Time from first symptom to detection]
**Detection gap:** [What should have caught this earlier?]

### Response

**What went well:**
- [Good response action 1]
- [Good response action 2]

**What could be improved:**
- [Improvement 1]
- [Improvement 2]

### Action Items

| Priority | Action | Owner | Due Date | Status |
|----------|--------|-------|----------|--------|
| P0 | [Immediate fix to prevent recurrence] | [name] | [date] | [status] |
| P1 | [Short-term improvement] | [name] | [date] | [status] |
| P2 | [Long-term prevention] | [name] | [date] | [status] |

### Lessons Learned

1. [Key lesson 1]
2. [Key lesson 2]
3. [Key lesson 3]

### Appendix

- [Link to incident channel/thread]
- [Link to monitoring dashboards]
- [Link to related PRs/commits]
```

---

## Professional Incident Report (PIR) Template

Full report for external audiences (customers, partners, executives).

```markdown
# Incident Report

## Metadata
| Field | Value |
|-------|-------|
| Report ID | PIR-YYYY-NNNN |
| Incident ID | INC-YYYY-NNNN |
| Created Date | YYYY-MM-DD |
| Severity | SEV[1-4] |
| Status | Resolved / Monitoring |

---

## 1. Executive Summary

### Overview
[1-2 sentences describing the incident]

### Customer Impact
- **Affected Services**: [Service name]
- **Impact Duration**: YYYY-MM-DD HH:MM - HH:MM (Timezone)
- **Impact Scope**: [User count/Region/Features]

### Resolution
- **Recovery Completed**: YYYY-MM-DD HH:MM (Timezone)
- **Current Status**: Normal operation / Continued monitoring
- **Prevention Measures**: [1-2 key measures]

---

## 2. Incident Details

### Sequence of Events
[Chronological explanation]

### Impact Details

#### Service Impact
| Service/Feature | Impact Description | Severity |
|-----------------|-------------------|----------|
| [Service 1] | [Description] | High/Medium/Low |

#### Data Impact
- Data Loss: None / Yes ([Details])
- Data Integrity: No impact / [Details]

---

## 3. Timeline

| Time (Timezone) | Event |
|-----------------|-------|
| MM/DD HH:MM | Anomaly detected |
| MM/DD HH:MM | Investigation started |
| MM/DD HH:MM | Root cause identified |
| MM/DD HH:MM | Remediation applied |
| MM/DD HH:MM | Recovery confirmed |

### Response Metrics
- **Mean Time to Detect (MTTD)**: [X minutes]
- **Mean Time to Recover (MTTR)**: [X minutes]

---

## 4. Root Cause and Remediation

### Root Cause
[Clear explanation avoiding overly technical jargon]

### Actions Taken
| Action | Description | Status |
|--------|-------------|--------|
| Emergency Response | [Description] | Complete |
| Permanent Fix | [Description] | Complete / In Progress |

---

## 5. Prevention Measures

### Technical Measures
| Measure | Expected Effect | Timeline |
|---------|-----------------|----------|
| [Measure 1] | [Expected effect] | Complete / YYYY-MM-DD |

### Process Improvements
| Improvement | Description | Timeline |
|-------------|-------------|----------|
| [Improvement 1] | [Description] | Complete / YYYY-MM-DD |

---

## 6. Contact Information

For questions or concerns, please contact us:

- **Contact**: [Department/Contact info]
- **Hours**: [Business hours]

---

## Appendix (Technical Details)

<details>
<summary>Technical Details (Click to expand)</summary>

### Root Cause Technical Details
[Detailed explanation for technical teams]

### Change History
| Date | Change | Author |
|------|--------|--------|
| [Date] | [Description] | [Name] |

### Related Documents
- Postmortem: [Link]
- Incident Ticket: [Link]

</details>
```

---

## Executive Summary Only Template

For quick summary reports.

```markdown
# Incident Report (Summary)

## Metadata
| Field | Value |
|-------|-------|
| Report ID | PIR-YYYY-NNNN |
| Incident ID | INC-YYYY-NNNN |
| Created Date | YYYY-MM-DD |

## Executive Summary

### Overview
[1-2 sentences describing the incident]

### Customer Impact
- **Affected Services**: [Service name]
- **Impact Duration**: YYYY-MM-DD HH:MM - HH:MM (Timezone)
- **Impact Scope**: [User count/Region/Features]

### Resolution
- **Recovery Completed**: YYYY-MM-DD HH:MM (Timezone)
- **Current Status**: Normal operation / Continued monitoring
- **Prevention Measures**: [1-2 key measures]

### Contact
- **Contact**: [Department/Contact info]

---
For detailed report, please contact us.
```

---

## Postmortem vs PIR Comparison

| Aspect | Postmortem | Incident Report (PIR) |
|--------|------------|----------------------|
| Purpose | Internal learning & improvement | **External reporting & trust recovery** |
| Audience | Technical team | **Customers, Partners, Executives** |
| Detail Level | Technical details | **Business perspective + appropriate technical explanation** |
| Tone | Candid retrospective | **Professional, trust-focused** |
| Visibility | Internal only | **Externally shareable** |
