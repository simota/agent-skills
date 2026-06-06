# Consistency Framework (Shared Taxonomy)

Shared taxonomy of cross-file pattern consistency categories, examples, and severity scoring. Used by:

- **Judge** — detection stage (find violations during review). See `judge/reference/consistency-patterns.md` for detection heuristics.
- **Zen** — unification stage (refactor toward canonical pattern). See `zen/reference/consistency-audit.md` for refactor recipes.

Other agents may import this taxonomy when classifying multi-file inconsistencies.

---

## Contents
- [Categories](#categories)
- [Severity Rubric](#severity-rubric)
- [Detection Confidence Rules](#detection-confidence-rules)
- [False Positive Filtering](#false-positive-filtering)
- [Finding & Report Schemas](#finding--report-schemas)

---

## Categories

Nine categories cover the consistency surface. The first three (Error Handling, Naming, Import/Export) are common to both Judge and Zen; the remaining six are surfaced by one skill but reusable by either.

### 1. Error Handling Style — HIGH

**Concept:** How errors are raised, propagated, and recovered.

**Variants observed:** custom error class · generic `Error` · string throw · null/undefined return · Result type · `.catch()` chain.

**BAD (mixed):**
```typescript
// Service A
throw new AppError('NOT_FOUND', `User ${id} not found`);
// Service B
throw new Error('User not found');
// Service C
return null;
```

**GOOD (consistent):**
```typescript
throw new AppError('NOT_FOUND', `User ${id} not found`);
```

**Why HIGH:** Catch blocks become unreliable; debugging becomes ambiguous.

---

### 2. Error Type Hierarchy — HIGH

**Concept:** Structure of custom error classes and the properties they expose.

**Variants observed:** mixed property names (`code`/`statusCode`/`status`/`errorCode`) · multiple unrelated base classes · plain-object throws.

**BAD (mixed):**
```typescript
class NotFoundError extends Error { statusCode = 404; }
class ResourceNotFound extends AppError { code = 'NOT_FOUND'; status = 404; }
throw { error: 'not_found', httpStatus: 404 };
```

**GOOD (consistent):** single base hierarchy with stable property names.
```typescript
class AppError extends Error {
  constructor(public code: string, message: string, public statusCode: number) { super(message); }
}
class NotFoundError extends AppError { /* extends consistently */ }
```

**Why HIGH:** Centralized error middleware (loggers, HTTP mappers) cannot handle heterogeneous shapes.

---

### 3. Null Safety — HIGH

**Concept:** How nullable values are guarded and defaulted.

**Variants observed:** optional chaining (`?.`) · manual `&&` chain · no check · default via `??` vs `||` vs ternary.

**BAD (mixed):**
```typescript
const a = user?.profile?.name ?? 'Unknown';
const b = user && user.profile ? user.profile.name : 'Unknown';
const c = user.profile.name; // potential crash
```

**GOOD (consistent):**
```typescript
const name = user?.profile?.name ?? 'Unknown';
```

**Why HIGH:** Inconsistent guarding produces runtime crashes on the unchecked path.

---

### 4. Async Pattern — MEDIUM

**Concept:** How asynchronous flows are expressed.

**Variants observed:** `async/await` · `.then()/.catch()` chains · callbacks · sequential awaits where `Promise.all` would parallelize · mixed error capture.

**BAD (mixed):**
```typescript
async function fetchUser(id) {
  try { return await db.findUser(id); } catch (err) { throw new AppError('FETCH_FAILED', err.message); }
}
function fetchOrder(id) {
  return db.findOrder(id).then(o => o).catch(err => { throw new AppError('FETCH_FAILED', err.message); });
}
```

**GOOD (consistent):** all `async/await` with `try/catch`.

**Why MEDIUM:** Increases cognitive load and error-prone interleaving, but does not directly cause crashes.

---

### 5. API Call — HIGH

**Concept:** HTTP/RPC client usage, auth injection, retry, timeout.

**Variants observed:** raw `fetch` · direct `axios` · shared wrapper · ad-hoc header construction.

**BAD (mixed):**
```typescript
const a = await fetch(url, { headers: { Authorization: token } });
const b = await axios.get(url);
const c = await apiClient.get(url);
```

**GOOD (consistent):** shared client with built-in auth interceptor, retry, and timeout.

**Why HIGH:** Diverging retry/auth/timeout semantics produce subtle production-only bugs.

---

### 6. State Management — MEDIUM

**Concept:** Where state lives and how it updates within a framework layer.

**Variants observed (React):** `useState`+`useEffect` · `useReducer` · external store (Zustand/Redux) · server-state library (TanStack/SWR).

**GOOD (consistent per layer):**
- Local component state → `useState`
- Complex component state → `useReducer`
- Shared/global state → external store
- Server state → query library

**Why MEDIUM:** Mixed approaches reduce comprehensibility but rarely cause bugs directly.

---

### 7. Logging — MEDIUM

**Concept:** Logger choice, level discipline, structured fields.

**Variants observed:** `console.log` · `winston` · `pino` · structured JSON vs plain string · inconsistent level usage (`info` vs `debug` for the same event class).

**GOOD (consistent):** one logger, one schema for structured fields, codified level rubric.

**Why MEDIUM:** Observability and alerting depend on stable log shape; inconsistency silently degrades dashboards.

---

### 8. Naming Convention — LOW

**Concept:** Casing, prefixes, terminology, boolean phrasing.

**Variants observed:** `IUser` vs `UserInterface` vs `User` · `is_active` vs `isActive` · `user`/`account`/`member` for the same concept · `isActive` vs `enabled` for booleans.

**BAD (mixed):**
```typescript
interface IUserService { ... }
const is_active = user.isActive;
interface OrderServiceInterface { ... }
type AccountData = { ... }; // same concept as "User"
```

**GOOD (consistent):** one casing, no Hungarian prefixes, one canonical term per concept.

**Why LOW:** Affects readability, not behavior.

---

### 9. Import/Export Style — LOW

**Concept:** Module export shape, import path style, barrel usage.

**Variants observed:** default vs named exports for similar constructs · relative paths vs aliases · barrel re-exports vs direct imports · CommonJS mixed with ESM.

**BAD (mixed):**
```typescript
export default class UserService { ... }
export class OrderService { ... }
module.exports = { PaymentService };
```

**GOOD (consistent):** named exports across the board with a single import-path convention.

**Why LOW:** Mainly affects tree-shaking and tooling; rarely causes runtime issues.

---

## Severity Rubric

| Severity | Criteria | Recommended Action |
|----------|----------|--------------------|
| **HIGH** | Causes runtime inconsistency, hides bugs, or breaks shared middleware | Fix in current cycle |
| **MEDIUM** | Increases cognitive load or degrades observability | Fix when touching adjacent code |
| **LOW** | Cosmetic; does not affect behavior | Document for future cleanup |

Default severities by category:

| Category | Default |
|----------|---------|
| Error Handling Style | HIGH |
| Error Type Hierarchy | HIGH |
| Null Safety | HIGH |
| API Call | HIGH |
| Async Pattern | MEDIUM |
| State Management | MEDIUM |
| Logging | MEDIUM |
| Naming Convention | LOW |
| Import/Export Style | LOW |

---

## Detection Confidence Rules

Report a category as a consistency violation only when:

1. **Multi-occurrence:** the deviating pattern appears in ≥3 locations (not a one-off).
2. **Dominant pattern threshold:**
   - **≥70%** of occurrences match one pattern → that pattern is canonical; flag the rest.
   - **50–69%** → weak consensus; flag for team decision, recommend strongest candidate.
   - **<50%** → no consensus; escalate to Atlas for architectural guidance, do not auto-unify.
3. **Not on the exclusion list** (see below).

---

## False Positive Filtering

Skip or down-rank these situations:

| Exception | Reason | Action |
|-----------|--------|--------|
| Framework-required pattern | e.g., React hooks rules, GraphQL resolver shape | Skip |
| Legacy migration in progress | File marked `// TODO(migrate): ...` | Document, do not flag |
| Adapter/wrapper layers | Boundary code adapting an external API | Skip |
| Test-specific patterns | Mocks, fixtures, assertion styles | Skip |
| Generated code | Prisma client, protobuf, OpenAPI gen | Exclude from scan |
| Performance-critical path | Justified deviation (e.g., callbacks in hot path) | Flag as LOW |

---

## Finding & Report Schemas

### Single Finding (detection output)

```markdown
#### [CONSISTENCY-NNN] [Category]: [Title]

- **Category**: [one of the 9]
- **Severity**: HIGH / MEDIUM / LOW
- **Dominant Pattern**: [description, X/Y files, Z%]
- **Deviation**: [description]
- **Files Affected**:
  - `path/to/file1.ts:42` — [specific deviation]
- **Canonical Example**:
  ```ts
  // Expected pattern
  ```
- **Remediation Agent**: Zen (consistency audit)
```

### Audit Report (unification output)

```markdown
## Consistency Audit Report

### Scope
- **Category**: [one of the 9]
- **Files Scanned**: N
- **Scope Tier**: Focused / Module / Project-wide

### Canonical Pattern
| Aspect | Detail |
|--------|--------|
| Pattern | ... |
| Usage  | X/Y files, Z% |
| Justification | ... |

### Deviation Summary
| Severity | Count | Action |
|----------|-------|--------|
| HIGH | X | Fix now |
| MEDIUM | Y | Fix if touching |
| LOW | Z | Document |

### Migration Plan
| Phase | Files | Pattern Change | Estimated Lines |
|-------|-------|---------------|-----------------|
| 1 | ... | ... | ... |

### Risks
- False positive risk: framework-required differences
- Migration risk: behavioral side effects
```

---

## Cross-Agent Routing

| Stage | Agent | Responsibility |
|-------|-------|---------------|
| Detect inconsistencies during review | **Judge** | Emit `CONSISTENCY-NNN` findings |
| Unify patterns (refactor) | **Zen** | Mechanical replacement, no behavior change |
| Decide canonical pattern when no dominant exists | **Atlas** | Architectural guidance |
| Test pattern consistency | **Radar** | Test-specific patterns (fixtures, mocks) |
| Document the chosen canon | **Quill** | ADR or coding-standard write-up |
