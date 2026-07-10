# Judge: Code Smell Detection During Review

> Structural code smell detection heuristics and severity weighting rules used during Judge reviews

For the shared smell taxonomy (definitions, recognition patterns, canonical examples), see
`_common/CODE_SMELL_CATALOG.md`. This file only covers Judge-specific detection-during-review
heuristics, severity weighting, and routing.

---

## 1. Position in the Detection Layers

```
Judge's detection layers:
  Layer 1: Bug patterns        → bug-patterns.md
  Layer 2: Consistency issues  → consistency-patterns.md
  Layer 3: Code smells         → this file + _common/CODE_SMELL_CATALOG.md
  Layer 4: Test quality        → test-quality-patterns.md

Code smell = a structural problem that isn't an immediate bug, but degrades
maintainability and extensibility
```

---

## 2. Detection Heuristics During Review

Procedure for detecting smells that were "newly introduced" during a diff review.
Smells in pre-existing code are out of scope.

```
Step 1: Extract files with structural changes
  - +50 lines or more added → suspect BLOAT-family smell
  - New class/module → suspect BLOAT-002/CHG-001
  - Same fix repeated across multiple files → CHG-002 (Shotgun Surgery)

Step 2: Mechanically compute structural metrics (per the catalog's Recognition section)
  - Function LOC, parameter count, nesting depth, CC
  - Class LOC, method count, dependency count

Step 3: Flag only threshold violations (matrix below)

Step 4: Determine the target routing agent
  - Refactoring-related → Zen
  - Architecture-related → Atlas
  - Removal-related → Sweep
  - Type-design-related → Quill
```

---

## 3. Detection Threshold Matrix (Judge-Specific)

Thresholds for "whether to report" during review. Stricter than the Catalog's
Recognition thresholds (to keep review noise down).

| Catalog ID | Smell | Detection Metric | Report Threshold | Severity | Route |
|------------|-------|---------|------------|----------|-------|
| BLOAT-001 | Long Function | Function line count | > 50 | LOW | → Zen |
| BLOAT-001 | Long Function | Parameter count | > 5 | LOW | → Zen |
| BLOAT-002 | God Class | Method count | > 20 | MEDIUM | → Zen |
| BLOAT-002 | God Class | Class line count | > 500 | MEDIUM | → Zen |
| BLOAT-005 | Primitive Obsession | Same-type parameter count | ≥ 3 | LOW | → Zen / Quill |
| CHG-002 | Shotgun Surgery | Same fix scattered | 5+ files | MEDIUM | → Atlas |
| CPL-001 | Feature Envy | Chain depth | a.b.c.d | LOW | → Zen |
| CPL-002 | Inappropriate Intimacy | Private access violation/circular reference | any | MEDIUM | → Atlas |
| CTRL-001 | Spaghetti | Cyclomatic complexity | > 15 | MEDIUM | → Zen |
| CTRL-001 | Spaghetti | Nesting depth | > 4 | MEDIUM | → Zen |
| DISP-001 | Dead Code | Unused export | any | INFO | → Sweep |
| DISP-004 | Duplicated Logic | Similar blocks | 3+ lines × 2+ locations | LOW | → Zen |
| DISP-006 | Magic Number | Literal value | context-dependent | INFO | → Zen |

---

## 4. Severity Weighting Rules

Rules for raising or lowering the Catalog's baseline severity based on review context.

```
+1 level (LOW → MEDIUM, MEDIUM → HIGH):
  - Exposed on a public API / external contract
  - Hot path (called 100,000+ times/day)
  - Adjacent to a security boundary

-1 level (MEDIUM → LOW, LOW → INFO):
  - Under test / fixture / scripts/
  - Temporary migration code (with an explicit deadline)
  - Prototyping / spike branch
```

---

## 5. Report Output

### Report Format

```markdown
## Code Smell Findings

| ID | Type (Catalog) | File:Line | Description | Severity | Route |
|----|----------------|-----------|-------------|----------|-------|
| F-001 | God Class (BLOAT-002) | src/services/UserManager.ts | 35 methods, 890 LOC | MEDIUM | → Zen |
| F-002 | Long Function (BLOAT-001) | src/utils/transform.ts:45 | 120 LOC, 8 params | LOW | → Zen |
| F-003 | Dead Code (DISP-001) | src/legacy/old-helper.ts | Unused export (3 functions) | INFO | → Sweep |
```

### Reporting Policy

```
1. Prioritize bug patterns (smells are supplementary information)
2. Include only MEDIUM+ smells in the main report
3. Put INFO / LOW under an "Additional Observations" section
4. Report only newly introduced smells (pre-existing code is out of scope)
5. Always specify the target routing agent
6. Include the Catalog ID alongside to avoid confusion between synonyms
```

---

## 6. Framework-Specific Smells (Additional Checks During Review)

In addition to Catalog Section 8, Judge applies the following additional checks when scanning diffs.

```
React:
  - Prop drilling 3+ levels deep → recommend Context/State management
  - Missing/incomplete useEffect dependency array → route to bug-patterns.md
  - Component bloat (300+ lines) → recommend splitting (Route: Zen)

Express / API:
  - Fat Controller (business logic in the route handler) → separate into a Service layer (Route: Atlas)
  - Inconsistent error handling → route to consistency-patterns.md
  - Excessive middleware chain complexity → recommend simplification (Route: Zen)

TypeScript:
  - Overuse of the `any` type → define proper types (Route: Quill)
  - Overuse of type assertions (`as`) → reconsider type design (Route: Quill)
  - Inconsistent enum vs. union type usage → route to consistency-patterns.md
```

---

**Source:** [CodeRabbit: 5 Code Review Anti-Patterns](https://www.coderabbit.ai/blog/5-code-review-anti-patterns-you-can-eliminate-with-ai) · [DZone: Code Review Patterns and Anti-Patterns](https://dzone.com/refcardz/code-review-patterns-and-anti-patterns) · [HackerNoon: Code Review Anti-Patterns](https://hackernoon.com/code-review-anti-patterns-how-to-stop-nitpicking-syntax-and-start-improving-architecture)
