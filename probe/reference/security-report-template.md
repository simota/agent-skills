# Security Report Template

Purpose: Use this file when preparing the final Probe report. It defines the minimum structure, severity summary, and per-finding schema.

## Contents

- Report skeleton
- Findings summary table
- Finding entry template
- Status labels

## Minimum Report Structure

Use this structure unless the caller provides a stricter schema.

```md
## Executive Summary
- Target
- Test period
- Environment
- Scope
- Out-of-scope items
- Methodology

## Findings Summary
| Severity | Count | Status |
| --- | --- | --- |
| Critical | 0 | Open / Mitigated / Accepted |
| High | 0 | Open / Mitigated / Accepted |
| Medium | 0 | Open / Mitigated / Accepted |
| Low | 0 | Open / Mitigated / Accepted |

## Confirmed Findings
### [FINDING-001] Vulnerability Title
- Severity:
- CVSS:
- Status:
- Affected target:
- Description:
- Impact:
- Steps to reproduce:
- Evidence:
- Remediation:
- References:

## Unconfirmed Or Needs Review
- Finding ID:
- Reason it is not yet confirmed:
- What would be needed to confirm it safely:

## False Positive Notes
- Rule or test:
- Why it was false positive:
- Suggested tuning:

## Next Actions
- Recommended owner:
- Recommended next agent:
- Required validation after fix:
```

## Findings Summary Rules

- Count only confirmed findings in the main severity summary.
- Put unconfirmed issues in a separate section.
- If no issue is confirmed, say so explicitly.
- If the scan scope was partial, state the limitation in the executive summary.

## Finding Entry Template

Use the following fields for each confirmed finding:

| Field | Requirement |
| --- | --- |
| `Severity` | `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW` |
| `CVSS` | Numeric score and vector when available |
| `Status` | `Confirmed`, `Mitigated`, `Accepted Risk`, or `Needs Fix` |
| `Description` | What was tested and what failed |
| `Impact` | Business or technical impact in plain language |
| `Steps to reproduce` | Short, reproducible, safe sequence |
| `Evidence` | Request/response pair, screenshot, log line, or marker |
| `Remediation` | Specific fix guidance, not generic advice |
| `References` | OWASP, vendor docs, or protocol references when useful |

## Status Labels

| Label | Use when |
| --- | --- |
| `Confirmed` | Safe proof exists and the issue is reproducible |
| `Needs Review` | Evidence is incomplete or risk of destructive confirmation is too high |
| `False Positive` | The signal was reproduced and disproven |
| `Mitigated` | The issue was fixed and re-validation confirms it |

## Report Quality Gate

Do not finalize the report if any of these are missing:

- Scope and environment
- Evidence for every confirmed finding
- CVSS or a reason why CVSS is not applicable
- Clear remediation guidance
- Explicit labeling of false positives and unconfirmed items
