# Report Templates

**Purpose:** Standard formats for compliance dashboards, per-skill reports, and ecosystem coverage figures.
**Read when:** Executing the REPORT phase of the audit workflow.

---

## Per-Skill Compliance Card

```markdown
## Compliance Report: {AGENT_NAME}

**Date:** YYYY-MM-DD
**Auditor:** Gauge
**Coverage:** PASS {n} · PARTIAL {n} · FAIL {n} (P0 {n} · P1 {n} · P2 {n} · P3 {n}) · NOT_RUN {n} — of 21
**Blocking:** {yes/no} (any open P0)

### Item Status

| # | Item | Status | Priority | Evidence |
|---|------|--------|----------|----------|
| F1 | YAML Frontmatter | PASS/PARTIAL/FAIL | P3 | [brief evidence] |
| F2 | Description Discoverability | PASS/PARTIAL/FAIL | P0 | [brief evidence] |
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
| S10 | Body Size Constraint | PASS/PARTIAL/FAIL | P1 | [brief evidence] |
| S11 | Freshness / Staleness Check | PASS/PARTIAL/FAIL | P2 | [brief evidence] |
| A1 | AUTORUN Support | PASS/PARTIAL/FAIL | P0 | [brief evidence] |
| A2 | Nexus Hub Mode | PASS/PARTIAL/FAIL | P0 | [brief evidence] |
| CQ1 | Obviousness Density | PASS/PARTIAL/FAIL | P1 (FAIL) / P2 (PARTIAL)* | [brief evidence] |
| CQ2 | Description Trigger-Word | PASS/PARTIAL/FAIL | P1 (FAIL) / P2 (PARTIAL)* | [brief evidence] |

\* CQ1/CQ2 priority is status-dependent, not fixed — see `reference/content-quality-audit.md`.

### Summary

- **PASS:** {count}/21
- **PARTIAL:** {count}/21
- **FAIL:** {count}/21
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
**Blocked skills (open P0):** {count}

### Coverage figures — report per severity, never as one grade

There is **no single ecosystem health score.** 21 heterogeneous checks do not share a unit, and
averaging them lets a P0 routing defect be offset by cosmetic passes elsewhere. Report the
distribution instead:

```
Items checked:  total_skills × 21 = {n}
PASS     {n} ({pct}%)
PARTIAL  {n} ({pct}%)   ← counted on its own axis, never folded into PASS or into 0
FAIL     {n} ({pct}%)   broken out by severity: P0 {n} · P1 {n} · P2 {n} · P3 {n}
NOT_RUN  {n}            ← a check that did not execute; excluded from the percentages,
                          reported as its own count
```

Three rules make the numbers honest:

- **`PARTIAL` is a third state, not a zero.** A formula whose numerator is `total_pass` alone
  silently scores every partial as a total failure, which understates progress and rewards
  reclassifying borderline items downward.
- **`NOT_RUN` is never counted as `0` or dropped.** A check that did not execute is unknown, not
  failed and not passed. Folding it either way turns missing coverage into a quality claim.
- **P0 is a gate, not a weight.** Any skill with an open P0 is reported as blocked regardless of
  its other 20 results. `F2` (description) and `S11` (dangling references) are routing-critical:
  they break agent navigation, so they never average away.

This mirrors `_common/EVIDENCE_LADDER.md` ("read per risk class, never as a single average"),
`.claude/skills/darwin/reference/assessment-models.md` ("Report both; never average them"), and
`launch/reference/engineering-metrics-guardrails.md` ("treat SPACE as a checklist, not a single
composite score"). A composite grade here would have Gauge violate the standard it audits against.

### Compliance Matrix

| Skill | F1 | F2 | L1 | H1 | H2 | H3 | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | S11 | A1 | A2 | CQ1 | CQ2 | P/△/F | Blocked |
|-------|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|-----|-----|----|----|-----|-----|--------|---------|
| scribe[unified] | ✓/△/✗ | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | 18/2/1 | yes/no |
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
**Current:** PASS {n} · PARTIAL {n} · FAIL {n} · NOT_RUN {n} — of 21 · blocked: {yes/no}
**Target:** no open P0, no FAIL
**Violations:** {count} ({p0_count} P0, {p1_count} P1, {p2_count} P2, {p3_count} P3)

### Fixes (priority order)

#### Fix 1: [{priority}] {item_name}

**Status:** FAIL → PASS
**Action:** Add {section/block description}
**Exemplar:** Architect `{section name}` section

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
**Blocked (open P0):** {count} of {total}

### Quick Results

| Skill | P/△/F | Blocked | P0 | P1 | P2 | P3 | Top violation |
|-------|--------|---------|----|----|----|----|---------------|
| {name} | 18/2/1 | yes/no | {count} | {count} | {count} | {count} | {item} |
...

### Action Items

1. **Immediate (P0):** {count} skills need {description}
2. **High (P1):** {count} skills need {description}
3. **Medium (P2):** {count} skills need {description}
4. **Low (P3):** {count} skills need {description}
```
