# Report Templates

**Purpose:** Standard formats for compliance dashboards, per-skill reports, and ecosystem health scores.
**Read when:** Executing the REPORT phase of the audit workflow.

---

## Per-Skill Compliance Card

```markdown
## Compliance Report: {AGENT_NAME}

**Date:** YYYY-MM-DD
**Auditor:** Gauge
**Health Score:** {score}% ({grade})

### Item Status

| # | Item | Status | Priority | Evidence |
|---|------|--------|----------|----------|
| F1 | YAML Frontmatter | PASS/PARTIAL/FAIL | P3 | [brief evidence] |
| L1 | Language Compliance | PASS/PARTIAL/FAIL | P1 | [brief evidence] |
| H1 | CAPABILITIES_SUMMARY | PASS/PARTIAL/FAIL | P3 | [brief evidence] |
| H2 | COLLABORATION_PATTERNS | PASS/PARTIAL/FAIL | P3 | [brief evidence] |
| H3 | PROJECT_AFFINITY | PASS/PARTIAL/FAIL | P3 | [brief evidence] |
| S1 | Trigger Guidance | PASS/PARTIAL/FAIL | P2 | [brief evidence] |
| S2 | Core Contract | PASS/PARTIAL/FAIL | P1 | [brief evidence] |
| S3 | Boundaries | PASS/PARTIAL/FAIL | P1 | [brief evidence] |
| S4 | Workflow | PASS/PARTIAL/FAIL | P1 | [brief evidence] |
| S5 | Output Routing | PASS/PARTIAL/FAIL | P2 | [brief evidence] |
| S6 | Output Requirements | PASS/PARTIAL/FAIL | P2 | [brief evidence] |
| S7 | Collaboration | PASS/PARTIAL/FAIL | P0 | [brief evidence] |
| S8 | Reference Map | PASS/PARTIAL/FAIL | P3 | [brief evidence] |
| S9 | Operational | PASS/PARTIAL/FAIL | P3 | [brief evidence] |
| A1 | AUTORUN Support | PASS/PARTIAL/FAIL | P0 | [brief evidence] |
| A2 | Nexus Hub Mode | PASS/PARTIAL/FAIL | P0 | [brief evidence] |

### Summary

- **PASS:** {count}/16
- **PARTIAL:** {count}/16
- **FAIL:** {count}/16
- **P0 violations:** {list}
- **P1 violations:** {list}

### Fix Plan (priority order)

1. **[P0] {item}:** {fix description} → See fix snippet below
2. **[P1] {item}:** {fix description} → See fix snippet below
...
```

---

## Ecosystem Compliance Dashboard

```markdown
## Ecosystem Compliance Dashboard

**Date:** YYYY-MM-DD
**Skills audited:** {count}
**Ecosystem Health Score:** {score}%

### Health Score Formula

`Health Score = (total_pass / (total_skills × 16)) × 100`

### Grade Scale

| Grade | Score | Description |
|-------|-------|-------------|
| A+ | 95-100% | Exemplary compliance |
| A  | 90-94% | Strong compliance |
| B  | 80-89% | Good compliance with minor gaps |
| C  | 70-79% | Moderate compliance, action needed |
| D  | 60-69% | Significant gaps |
| F  | <60% | Critical non-compliance |

### Compliance Matrix

| Skill | F1 | L1 | H1 | H2 | H3 | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | A1 | A2 | Score |
|-------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|-------|
| accord | ✓/△/✗ | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | X/16 |
...

**Legend:** ✓ = PASS, △ = PARTIAL, ✗ = FAIL

### Top Violations (by frequency)

| Item | FAIL count | PARTIAL count | Total non-compliant | % of skills |
|------|-----------|---------------|---------------------|-------------|
| {item} | {count} | {count} | {total} | {pct}% |
...

### Priority Breakdown

| Priority | Total violations | % of all violations |
|----------|-----------------|---------------------|
| P0 | {count} | {pct}% |
| P1 | {count} | {pct}% |
| P2 | {count} | {pct}% |
| P3 | {count} | {pct}% |
```

---

## Per-Skill Fix Plan

```markdown
## Fix Plan: {AGENT_NAME}

**Date:** YYYY-MM-DD
**Current score:** {score}/16 ({pct}%)
**Target score:** 16/16 (100%)
**Violations:** {count} ({p0_count} P0, {p1_count} P1, {p2_count} P2, {p3_count} P3)

### Fixes (priority order)

#### Fix 1: [{priority}] {item_name}

**Status:** FAIL → PASS
**Action:** Add {section/block description}
**Exemplar:** Quest `{section name}` section

\```markdown
{fix snippet here}
\```

#### Fix 2: [{priority}] {item_name}

...
```

---

## Evolution Report

```markdown
## Evolution Report

**Date:** YYYY-MM-DD
**Trigger:** {trigger_id} — {trigger_description}
**Scope:** {Lightweight | Medium | Full}

### Research Findings

| # | Source | Tier | Finding | Relevance |
|---|--------|------|---------|-----------|
| 1 | {URL or reference} | T{1-4} | {summary} | {high/medium/low} |
...

### Proposed Changes

| # | Target file | Change type | Safety level | Description |
|---|-------------|-------------|--------------|-------------|
| 1 | {file} | {Add/Update/Remove} | {A/B/C/D} | {description} |
...

### Budget Check

- Session remaining: {X} changes
- Monthly remaining: {Y} changes

### Verification

- Pre-change state: {description}
- Post-change state: {description}
- Regression check: PASS/FAIL

### Applied Changes

{list of actually applied changes with before/after}
```

---

## Batch Audit Summary

Use this format when auditing multiple skills in a single session.

```markdown
## Batch Audit Summary

**Date:** YYYY-MM-DD
**Skills audited:** {count}
**Average score:** {score}/16 ({pct}%)

### Quick Results

| Skill | Score | Grade | P0 | P1 | P2 | P3 | Top violation |
|-------|-------|-------|----|----|----|----|---------------|
| {name} | X/16 | {grade} | {count} | {count} | {count} | {count} | {item} |
...

### Action Items

1. **Immediate (P0):** {count} skills need {description}
2. **High (P1):** {count} skills need {description}
3. **Medium (P2):** {count} skills need {description}
4. **Low (P3):** {count} skills need {description}
```
