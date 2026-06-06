# Vague Report Handling Reference

**Purpose:** Intake patterns and pre-question guardrails for incomplete or noisy bug reports.
**Read when:** The report is incomplete, emotional, indirect, image-only, or missing explicit reproduction steps.

## Contents

- Report pattern dictionary
- Context collection
- Three-hypothesis generation
- Pre-question checklist
- Completion criteria

## Report Pattern Dictionary

### Primary Patterns

| ID | Pattern Name | Example Keywords | Inferred Situation | Investigation Start Point |
|----|--------------|------------------|--------------------|---------------------------|
| `P01` | Total Denial | "Doesn't work", "Broken", "Can't use", "Not showing" | Complete core feature failure | entry point, recent changes |
| `P02` | Comparison | "It worked before", "Until yesterday", "Just now", "Suddenly" | Regression | `git log`, deploy history |
| `P03` | Vague Feeling | "Something's off", "Feels weird", "Uncomfortable" | Subtle deviation from expectation | UI, data display, timing |
| `P04` | Urgency | "Fix ASAP", "Urgent", "Critical", "Blocked" | Business blocker | impact scope, workarounds |
| `P05` | Tech Term Mixed | "API returns null", "500 error", "Response slow" | Specific technical issue | mentioned technical area |
| `P06` | Image Only | `[Screenshot only]`, `[Video only]` | Visual problem | visible elements, error displays |

### Extended Patterns

| ID | Pattern Name | Example Keywords | Inferred Situation | Investigation Start Point |
|----|--------------|------------------|--------------------|---------------------------|
| `P07` | Conditional | "Only when...", "If I...", "Specific..." | condition-specific issue | conditional path |
| `P08` | Environment | "In production", "On mobile", "In Chrome" | environment-specific issue | config or runtime diff |
| `P09` | User Specific | "User X said...", "Customer reported..." | user- or role-specific issue | permissions, roles, user data |
| `P10` | Frequency | "Sometimes", "Occasionally", "Not every time" | intermittent issue | race, cache, timing |
| `P11` | Action Specific | "When I click...", "After entering...", "When saving..." | action-specific issue | event handler, validation |
| `P12` | Data Specific | "With this data...", "For specific value..." | data-dependent issue | validation, edge cases |
| `P13` | Time Specific | "Only in morning", "End of month", "Periodically" | time-dependent issue | cron, timezone, date logic |
| `P14` | Error Message | "It says...", "Error appeared..." | explicit error source | thrown message or logging source |
| `P15` | Performance | "Slow", "Heavy", "Freezes" | performance issue | N+1, leak, loop |
| `P16` | Security | "Shouldn't be visible", "Permission...", "Without login..." | auth or access issue | auth, ACL, session |
| `P17` | Layout Broken | "Misaligned", "Overflowing", "Overlapping" | layout issue | styles, responsive rules |
| `P18` | Copy/Text | "Wrong text", "Translation wrong" | copy or localization issue | i18n source |
| `P19` | Notification | "Email not arriving", "No notification..." | async processing issue | queue, mailer, webhook |
| `P20` | Integration | "Connection with X...", "External service..." | external integration issue | API, webhook, OAuth |

## Context Collection

Collect before asking:

| Source | Command / Method | Why |
|--------|------------------|-----|
| Recent commits | `git log --oneline -20` | find regressions |
| Changed files | `git diff HEAD~5 --name-only` | narrow impact |
| Deploy history | CI/CD logs, tags | detect release-related issues |
| Related issues | issue search | find precedent |
| Error logs | server logs, browser console | capture exact failure |
| Report timing | compare with deploy time | separate new vs latent issues |

## Three-Hypothesis Rule

Generate exactly `3` starting hypotheses:

1. most frequent similar cause in this codebase
2. recent-change or regression hypothesis
3. pattern-based hypothesis from the report class

### Fast Templates

| Report Type | Hypothesis Set |
|-------------|----------------|
| `"Doesn't work"` | recent deploy, dependency outage, config issue |
| `"It worked before"` | regression commit, dependency update, schema change |
| `"Something's off"` | subtle UI difference, formatting/order issue, timing issue |
| `"Happens sometimes"` | race condition, cache inconsistency, specific-data dependency |
| `"Slow"` | N+1 query, large data volume, external timeout |

## Pre-Question Checklist

Only ask questions if all are true:

- [ ] recent changes checked
- [ ] changed files checked
- [ ] relevant feature code inspected
- [ ] logs or console checked where available
- [ ] past project or issue context checked
- [ ] `3` hypotheses generated
- [ ] first hypothesis tested
- [ ] proceeding with assumptions would now be dangerous

### Allowed Exceptions

Ask only for:

- production-data access
- exact environment when behavior differs materially by environment
- affected user ID for user-specific issues
- permission to continue if the issue is security-sensitive

## Completion Criteria

| Confidence | Condition | Reporting Style |
|------------|-----------|-----------------|
| `HIGH` | reproduction + file:line cause | definitive |
| `MEDIUM` | reproduction + strong estimated cause | estimated + verification |
| `LOW` | no repro + hypotheses only | hypothesis + missing info |

## Mindset

- Trust the report until evidence disproves it.
- Infer actively, then verify.
- Ask the minimum possible only after evidence gathering.
