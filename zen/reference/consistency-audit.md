# Consistency Audit (Zen)

Zen's role in the consistency pipeline: **execute the unification**. Judge detects, Zen refactors mechanically without behavior change.

> **Shared taxonomy:** see `_common/CONSISTENCY_FRAMEWORK.md` for the 9 categories, severity rubric, detection confidence rules, false-positive filters, and report schemas. This file only covers Zen-specific execution.

## Contents
- [Audit Loop](#audit-loop)
- [Refactor Playbooks per Category](#refactor-playbooks-per-category)
- [Scope Tiers](#scope-tiers)
- [Tooling](#tooling)

---

## Audit Loop

```
1. SCAN     → Collect pattern instances across target files
2. CLASSIFY → Group by category (see _common/CONSISTENCY_FRAMEWORK.md)
3. IDENTIFY → Determine dominant pattern (≥70% usage = canonical)
4. DEVIATE  → List files/locations that deviate
5. PLAN     → Migration plan respecting Scope Tier
6. APPLY    → Mechanical replacement, tests BEFORE/AFTER each batch
```

Step 3 thresholds and step 5 exclusions are defined in `_common/CONSISTENCY_FRAMEWORK.md`.

---

## Refactor Playbooks per Category

For each category Zen handles, the playbook is: identify canonical → import canonical from a single module → replace deviations mechanically → verify tests.

### Error Handling Style
1. Ensure `AppError` (or chosen base) class exists and is importable.
2. Replace string throws → `new AppError(code, message)`.
3. Replace `new Error(msg)` → `new AppError(code, msg)`.
4. Update catch blocks to read `AppError` properties.
5. Run tests after each file change.

**Before → After:**
```typescript
// Before
throw 'User not found';
throw new Error('User not found');
// After
throw new AppError('NOT_FOUND', 'User not found');
```

### Error Type Hierarchy
1. Pick or define the single base class (commonly `AppError`).
2. Normalize property names (`code`, `message`, `statusCode`).
3. Subclass leaf errors from the base; remove parallel hierarchies.
4. Update middleware/loggers if property names changed.

### API Call
1. Identify or create the shared client with standard config (auth interceptor, retry, timeout).
2. Replace raw `fetch` → `apiClient` methods.
3. Replace direct `axios` usage → `apiClient`.
4. Consolidate auth header injection into the interceptor.
5. Verify timeout and retry behavior is consistent (manual smoke + tests).

### State Management
Decide per layer (see canonical mapping in `_common/CONSISTENCY_FRAMEWORK.md` §6) before refactoring. Mechanical replacement is rare here — usually requires Atlas guidance first.

### Logging
1. Pick one logger module; export a singleton.
2. Replace `console.*` and other loggers with the singleton.
3. Normalize structured field keys (`requestId`, `userId`, etc.).
4. Re-grade log levels against the project rubric.

### Naming Convention
1. Pick canonical casing/prefix rules and terminology.
2. Use IDE rename refactor (not text replace) for safety.
3. Update barrel files and re-exports together.

### Import/Export Style
**Before → After:**
```typescript
// Before
export default class UserService {}
import UserService from './UserService';
// After
export class UserService {}
import { UserService } from './UserService';
```

Barrel files: explicit named re-exports rather than `export *`.

### Null Safety / Async Pattern / Error Type
Detection-heavy categories typically handled inside Judge's review loop; Zen executes the same mechanical replacement pattern (canonical example in `_common/CONSISTENCY_FRAMEWORK.md`).

---

## Scope Tiers

| Tier | Files | Max Lines Changed | Zen Approach |
|------|-------|-------------------|--------------|
| **Focused** | 1-3 | ≤50 | Direct refactoring (standard Zen scope) |
| **Module** | 4-10 | ≤100 | Mechanical pattern replacement only |
| **Project-wide** | 10+ | Plan only | Generate migration plan, execute in multiple PRs |

### Tier Rules

**Focused (1-3 files):** Standard Zen 50-line limit, full Before/After report, tests BEFORE and AFTER.

**Module (4-10 files):** Extended to 100 lines max. **Restricted to mechanical pattern replacement** — same transform applied identically. No logic or behavioral changes. Single pattern category across the batch. Tests BEFORE and AFTER each batch.

**Project-wide (10+ files):** Migration plan only — no code changes. Plan lists files, priority order, estimated effort per file. Execution split into multiple Focused/Module-tier PRs, each independently testable.

---

## Tooling

### AST-level Pattern Search

```bash
# ast-grep
ast-grep -p 'try { $$$ } catch($ERR) { $$$ }' src/
ast-grep -p 'fetch($URL, $$$)' src/
ast-grep -p 'console.log($$$)' src/

# ESLint
npx eslint --rule 'no-throw-literal: error' src/

# ruff (Python)
ruff check --select E,W src/

# staticcheck (Go)
staticcheck -checks all ./...
```

### Pattern Counting

```bash
ast-grep -p 'try { $$$ } catch($E) { $$$ }' src/ --json | jq length
ast-grep -p 'throw new Error($$$)' src/ --json | jq length
ast-grep -p 'throw "$$$"' src/ --json | jq length
```

---

## Routing

| Task | Agent |
|------|-------|
| Detect pattern inconsistencies | **Judge** (`judge/reference/consistency-patterns.md`) |
| Unify patterns (refactor) | **Zen** (this file) |
| Architectural pattern decisions | **Atlas** (when no dominant pattern exists) |
| Test pattern consistency | **Radar** |
| Document canonical patterns | **Quill** (ADR / coding standards) |
