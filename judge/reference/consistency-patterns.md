# Consistency Pattern Detection (Judge)

Judge's role in the consistency pipeline: **detect and report**. Zen performs the actual unification.

> **Shared taxonomy:** see `_common/CONSISTENCY_FRAMEWORK.md` for the 9 categories, full BAD/GOOD examples, severity rubric, detection confidence rules, false-positive filters, and the `CONSISTENCY-NNN` finding schema. This file only covers Judge-specific detection heuristics and handoff.

## Contents
- [Detection Heuristics per Category](#detection-heuristics-per-category)
- [Confidence Gate](#confidence-gate)
- [Summary in Review Report](#summary-in-review-report)
- [Handoff to Zen](#handoff-to-zen)

---

## Detection Heuristics per Category

Each heuristic is a quick signal to flag during review. Once flagged, apply the [Confidence Gate](#confidence-gate) before emitting a finding.

### 1. Error Handling Style — HIGH
- Mixed `try/catch` and `.catch()` chains in the same service layer.
- `throw new Error(...)` and `throw new AppError(...)` (or other custom class) co-existing.
- Some functions throw, sibling functions return `null` or error codes for the same failure mode.
- Inconsistent error message format (template literal vs concatenation).

### 2. Error Type Hierarchy — HIGH
- Multiple custom error classes with no common base.
- Property names diverge across error classes (`code` / `statusCode` / `status` / `errorCode`).
- Plain-object throws (`throw { error: 'not_found' }`) mixed with class throws.
- Same HTTP status mapped from different error types inconsistently.

### 3. Null Safety — HIGH
- Mix of optional chaining (`?.`) and manual `&&` null checks for the same access pattern.
- Sibling functions where one checks for null and the other does not.
- Inconsistent default-value operator (`??` vs `||` vs ternary) for the same nullable concept.

### 4. Async Pattern — MEDIUM
- `async/await` and `.then()/.catch()` chains co-existing in the same module.
- Inconsistent error capture in async code (`try/catch` vs `.catch`).
- Sequential `await`s where `Promise.all` would parallelize independent calls.
- Callback-style mixed with Promise-style for the same I/O class.

### 5. Naming Convention — LOW
- Mixed casing for the same identifier kind (camelCase vs snake_case).
- Inconsistent type prefixes/suffixes (`IUser` vs `UserInterface` vs `User`).
- Mixed terminology for the same domain concept (`user` / `account` / `member`).
- Boolean naming inconsistency (`isActive` vs `active` vs `enabled`).

### 6. Import/Export Style — LOW
- Default exports mixed with named exports for the same construct kind.
- Relative paths mixed with path aliases in adjacent files.
- Barrel re-exports used inconsistently across modules.
- CommonJS `require` mixed with ESM `import`.

### 7. API Call · 8. State Management · 9. Logging
Judge typically does not author these heuristics during code review (they are architecture-shaped). When observed, flag at the category level and refer to `_common/CONSISTENCY_FRAMEWORK.md` for canonical examples; route to Zen with `Scope Tier: Project-wide` so Zen produces a plan rather than direct edits.

---

## Confidence Gate

Before emitting a `CONSISTENCY-NNN` finding, all three must hold (defined in `_common/CONSISTENCY_FRAMEWORK.md`):

1. Deviation appears in **≥3 files** (not a one-off).
2. Dominant pattern has **≥70% usage**.
3. The deviation is **not** on the false-positive exclusion list.

If conditions 1–2 do not hold, downgrade severity by one or omit the finding entirely. If condition 3 applies, document the exception inline and skip.

---

## Summary in Review Report

Add this section to the standard Judge Review Report:

```markdown
### Consistency Findings

| ID | Category | Severity | Files | Dominant Pattern |
|----|----------|----------|-------|------------------|
| CONSISTENCY-001 | Error Handling | HIGH | 3/12 deviate | AppError class |
| CONSISTENCY-002 | Async Pattern | MEDIUM | 5/20 deviate | async/await |

**Recommendation**: Route to Zen for consistency audit on Error Handling (HIGH priority).
```

Per-finding emission uses the schema in `_common/CONSISTENCY_FRAMEWORK.md` (Finding & Report Schemas).

---

## Handoff to Zen

When consistency violations are detected, include in `JUDGE_TO_ZEN_HANDOFF`:

```markdown
## JUDGE_TO_ZEN_HANDOFF (Consistency)

**Review ID**: [PR# or audit scope]
**Type**: Consistency Violation

**Consistency Findings**:

### [CONSISTENCY-001] Error Handling: Mixed error types
| Aspect | Detail |
|--------|--------|
| Category | Error Handling |
| Severity | HIGH |
| Dominant Pattern | `throw new AppError(code, message)` (9/12 files) |
| Deviations | 3 files using `throw new Error(message)` |
| Files | `src/legacy/handler.ts:42`, `src/api/v1/client.ts:89`, `src/utils/parser.ts:15` |

**Request**: Apply consistency audit — unify error handling to AppError pattern.
**Scope Tier**: Module (3 files, mechanical replacement)
```

Scope Tier selection guidance lives in `zen/reference/consistency-audit.md` (Zen owns the scope decision after handoff).
