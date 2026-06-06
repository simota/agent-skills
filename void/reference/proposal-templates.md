# Proposal Templates Reference — Void

Purpose: Use this file to format Void outputs consistently and preserve routing-ready decision data.

Contents:
- Severity x confidence matrix
- Recommendation classification rules
- Canonical templates for full, single-target, scope-cut, quick, and batch outputs

## Severity x Confidence Matrix

```text
              Confidence
              High(80-100%)  Med(60-79%)   Low(<60%)
Severity
Critical(8-10)  ACT NOW        VERIFY FIRST   DO NOT PROPOSE
High(6-7)       PRIORITIZE     SCHEDULE       DEFER
Medium(4-5)     BATCH          BATCH          SKIP
Low(0-3)        OPPORTUNISTIC  SKIP           SKIP
```

Rule: if confidence is below `60%`, do not propose `REMOVE`.

## Recommendation Classification

| Recommendation | Criteria | Next agent |
|----------------|----------|------------|
| `REMOVE` | `CoK >= 7`, `Risk <= 5`, `Confidence >= 80%` | `Sweep` then `Magi` when approval is needed |
| `SIMPLIFY` | `CoK 4-8`, `Risk 3-7` | `Zen` |
| `DEFER` | `Risk >= 7` or insufficient evidence | schedule review |
| `KEEP-WITH-WARNING` | `CoK >= 5` but a valid reason still exists | record warning and re-audit |

## Template 1: Full Audit Report

```markdown
# Void: Subtraction Audit Report

**Audit Scope:** [Project / Module / Process]
**Date:** YYYY-MM-DD
**Targets Evaluated:** X

## Executive Summary

| Metric | Value |
|--------|-------|
| Targets evaluated | X |
| REMOVE recommendations | X |
| SIMPLIFY recommendations | X |
| DEFER | X |
| KEEP-WITH-WARNING | X |
| Estimated maintenance reduction | X% |
| Estimated cognitive-load reduction | X% |

## Findings

### [Target Name]

| Item | Value |
|------|-------|
| Domain | Code / Feature / Process / Document / Design / Dependency / Configuration / Specification |
| Category | Feature / Abstraction / Scope / Dependency / Configuration / Process / Document / Design_Spec |
| CoK Score | X.X / 10 |
| Removal Risk | X.X / 10 |
| Confidence | X% |
| Recommendation | REMOVE / SIMPLIFY / DEFER / KEEP-WITH-WARNING |

**5 Questions Summary**
1. **Who uses it?** [answer]
2. **What breaks if removed?** [answer]
3. **When was it last meaningfully changed?** [date + staleness]
4. **Why was it built?** [answer]
5. **What does keeping it cost?** [answer]

**Blast Radius:** [artifacts affected / verification affected / users affected]
**Subtraction Pattern:** [pattern]
**Routing:** [next agent]

## Batch Subtraction Plan

| Priority | Target | Domain | Recommendation | CoK | Risk | Pattern | Agent |
|----------|--------|--------|---------------|-----|------|---------|-------|
| 1 | [Name] | Feature | REMOVE | X.X | X.X | Sunset | Sweep |
| 2 | [Name] | Code | SIMPLIFY | X.X | X.X | Collapse | Zen |

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [risk] | HIGH/MED/LOW | HIGH/MED/LOW | [mitigation] |
```

## Template 2: Single Target Evaluation

```markdown
# Void: Target Evaluation — [Target Name]

**Domain:** [Code / Feature / Process / Document / Design / Dependency / Configuration / Specification]

## 5 Existence Questions

### Q1: Who uses it?
[answer]
**Confidence:** HIGH / MEDIUM / LOW

### Q2: What breaks if removed?
[answer]
**Blast Radius:** NONE / LOCAL / CROSS_MODULE / PUBLIC_API / DATA

### Q3: When was it last meaningfully changed?
[date]
**Staleness:** FRESH / AGING / STALE / FOSSILIZED

### Q4: Why was it built?
[answer]
**Still Valid:** YES / PARTIALLY / NO

### Q5: What does keeping it cost?
[answer]

## Cost-of-Keeping Score

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Upkeep | X/10 | [evidence] |
| Verification | X/10 | [evidence] |
| Cognitive Load | X/10 | [evidence] |
| Entanglement | X/10 | [evidence] |
| Replaceability | X/10 | [evidence] |
| **Weighted Total** | **X.X/10** | |

## Removal Risk: X.X/10

## Recommendation: REMOVE / SIMPLIFY / DEFER / KEEP-WITH-WARNING
**Confidence:** X%
**Pattern:** [pattern]
**Routing:** [next agent]
```

## Template 3: Scope Cut Proposal

```markdown
# Void: Scope Cut Proposal — [Target Name]

## Current Scope
[current scope]

## Usage Analysis

| Variation | Usage% | Maintenance Cost | Recommendation |
|-----------|--------|-----------------|---------------|
| [Variation A] | X% | LOW | KEEP |
| [Variation B] | X% | HIGH | CUT |

## Proposed Scope
[reduced scope]

## Impact
- **Coverage retained:** X%
- **Maintenance reduction:** X%
- **Artifacts affected:** X
- **Verification affected:** X
```

## Template 4: Quick YAGNI Check

```markdown
# Void: Quick YAGNI Check — [Target Name]

**Domain:** [Code / Feature / Process / Document / Design / Dependency / Configuration / Specification]

| Question | Answer | Signal |
|----------|--------|--------|
| Who uses it? | [one sentence] | GREEN / YELLOW / RED |
| What breaks? | [one sentence] | GREEN / YELLOW / RED |
| Last changed? | [date] | GREEN / YELLOW / RED |
| Why built? | [one sentence] | GREEN / YELLOW / RED |
| Keeping cost? | [one sentence] | GREEN / YELLOW / RED |

**Quick Verdict:** KEEP / INVESTIGATE FURTHER / LIKELY REMOVE
**CoK Estimate:** LOW / MODERATE / HIGH
```

## Template 5: Batch Subtraction Plan

```markdown
# Void: Batch Subtraction Plan

**Scope:** [scope]
**Targets:** X items

## Priority Queue

| # | Target | Domain | Category | CoK | Risk | Conf% | Rec | Pattern | Agent |
|---|--------|--------|----------|-----|------|-------|-----|---------|-------|
| 1 | [Name] | Feature | Feature | X.X | X.X | X% | REMOVE | Sunset | Sweep |
| 2 | [Name] | Code | Abstraction | X.X | X.X | X% | SIMPLIFY | Collapse | Zen |
| 3 | [Name] | Process | Process | X.X | X.X | X% | REMOVE | Pruning | Magi |

## Execution Order
1. [first item and reason]
2. [next item]

## Aggregate Impact
- Total artifacts affected: X
- Total verification affected: X
- Estimated maintenance reduction: X%
- Estimated cognitive-load reduction: X%

## Route to Magi
[summary when batch approval is needed]
```
