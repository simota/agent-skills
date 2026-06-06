# Defensive Excess — Unnecessary Fallback Detection and Fixes

Purpose: Use this file when fallback-heavy code may be hiding bugs or cluttering internal code paths.

## Contents
- [6 Patterns](#6-patterns)
- [Detection Tooling](#detection-tooling)
- [Judgment Guide — Keep vs Remove](#judgment-guide--keep-vs-remove)

Detect and remove over-defensive coding patterns that reduce readability, hide bugs, and add noise.

**Key principle**: Defensive code is valuable at system boundaries (user input, external APIs, file I/O). It becomes harmful when applied to internal, type-checked, or control-flow-guaranteed paths.

---

## 6 Patterns

### Pattern 1: Silent Catch (Exception Swallowing)

Empty `catch` blocks or catch-and-log-only without re-throwing or recovery.

**Detection**: Empty `catch {}` · `catch` with only `console.log`/`logger.warn` · `catch` returning default without context

**Why harmful**: Errors vanish silently. Bugs become impossible to trace downstream.

**Fix**: Re-throw, propagate, or handle with explicit recovery logic.

```typescript
// BEFORE: silent catch hides failures
try { return await api.get(`/users/${id}`); }
catch (e) { console.log("error"); return null; }

// AFTER: let errors propagate (caller decides policy)
return await api.get(`/users/${id}`);

// AFTER (alt): wrap with context
try { return await api.get(`/users/${id}`); }
catch (cause) { throw new UserFetchError(`Failed: ${id}`, { cause }); }
```

### Pattern 2: Redundant Nullish Guard (Type-Guaranteed Non-Null)

`??`, `?.`, or `!= null` checks on values the type system or control flow already guarantees non-null.

**Detection**: `value ?? fallback` on non-nullable type · `obj?.prop` on just-created object · `if (x != null)` after line that would throw if null

**Why harmful**: Suggests null is valid when it isn't. Masks real type errors when types change.

**Fix**: Remove the guard. If the type is wrong, fix the type.

```typescript
// BEFORE: items is string[] (never null)
function formatList(items: string[]): string {
  return (items ?? []).join(", ");
}
// AFTER
function formatList(items: string[]): string {
  return items.join(", ");
}
```

### Pattern 3: Fallback Masking Bugs (|| default Hiding Errors)

Using `|| defaultValue` or `?? defaultValue` to silently paper over values that should never be missing.

**Detection**: `config.requiredField || "fallback"` · `array.find(...) ?? defaultItem` when item must exist · `env.VAR || "localhost"` hiding missing config

**Why harmful**: Fallback executes in production, hiding configuration errors or data integrity bugs.

**Fix**: Fail fast with a clear error message.

```typescript
// BEFORE: masks missing config
const dbUrl = process.env.DATABASE_URL || "postgres://localhost:5432/dev";
// AFTER: fail fast at startup
const dbUrl = process.env.DATABASE_URL;
if (!dbUrl) throw new Error("DATABASE_URL is required");

// BEFORE: hides data integrity issue
const user = users.find(u => u.id === id) ?? { id, name: "Unknown" };
// AFTER: surface the real problem
const user = users.find(u => u.id === id);
if (!user) throw new Error(`User ${id} not found`);
```

### Pattern 4: Pokemon Exception (Catch-All Handler)

`catch (e)` catching every exception type with generic handling regardless of cause.

**Detection**: `catch (error)` with generic logging and single return for all types · No `instanceof` checks · `catch (e: any)`

**Why harmful**: Network errors, type errors, auth failures all get same treatment. Critical errors swallowed.

**Fix**: Catch specific error types. Let unexpected errors propagate.

```typescript
// BEFORE: all errors treated the same
try { await processPayment(order); }
catch (error) { return { success: false, message: "Something went wrong" }; }

// AFTER: handle known, propagate unknown
try { await processPayment(order); }
catch (error) {
  if (error instanceof PaymentDeclinedError) return { success: false, message: "Declined" };
  if (error instanceof InsufficientFundsError) return { success: false, message: "Insufficient funds" };
  throw error;
}
```

### Pattern 5: Unreachable Fallback (Dead Default Branch)

`default` in switch or final `else` that can never execute because all cases are covered.

**Detection**: `switch` on enum/union with all variants handled · Exhaustive `if/else if` with trailing `else` · `default: return "unknown"` on type with only known values

**Why harmful**: Dead code adds noise. Worse, a "safe" default silently handles new variants instead of causing compile error.

**Fix**: Remove the dead branch, or convert to `assertNever` for exhaustive checking.

```typescript
// BEFORE: dead default on exhaustive union
type Status = "active" | "inactive" | "pending";
function getLabel(s: Status): string {
  switch (s) {
    case "active": return "Active";
    case "inactive": return "Inactive";
    case "pending": return "Pending";
    default: return "Unknown"; // never reached
  }
}
// AFTER: exhaustive check catches future additions at compile time
function getLabel(s: Status): string {
  switch (s) {
    case "active": return "Active";
    case "inactive": return "Inactive";
    case "pending": return "Pending";
    default: { const _: never = s; throw new Error(`Unhandled: ${_}`); }
  }
}
```

### Pattern 6: Redundant Default Params (Always Provided by Callers)

Parameters with default values that every call site always provides explicitly.

**Detection**: All call sites pass explicit argument · Default matches the only value ever passed

**Why harmful**: Misleads readers into thinking parameter is optional.

**Fix**: Remove the default value.

```typescript
// BEFORE: every caller passes format explicitly
function formatDate(date: Date, format: string = "YYYY-MM-DD"): string { /* ... */ }
formatDate(now, "YYYY-MM-DD");
formatDate(created, "MM/DD/YYYY");
// AFTER
function formatDate(date: Date, format: string): string { /* ... */ }
```

---

## Detection Tooling

### ESLint / TypeScript-ESLint

| Rule | Detects |
|------|---------|
| `no-empty` | Empty catch blocks (P1) |
| `no-useless-catch` | Catch that only re-throws |
| `@typescript-eslint/no-unnecessary-condition` | Nullish guard on non-nullable (P2) |
| `@typescript-eslint/switch-exhaustiveness-check` | Missing exhaustive switch (P5) |

### AST Search / Other Languages

```bash
ast-grep --pattern 'catch ($_) { }' src/                          # Empty catch
comby 'catch (:[e]) { console.:[fn](:[args]); }' '' src/ --match-only  # Log-only catch
ruff check --select E722,BLE001 src/                              # Python: bare/broad except
golangci-lint run --enable errcheck,gosec                         # Go: unchecked errors
```

---

## Judgment Guide — Keep vs Remove

| Context | Keep? | Rationale |
|---------|-------|-----------|
| External API response | **Yes** | Runtime data, no type guarantee |
| User input / form data | **Yes** | Never trust user input |
| File system / network I/O | **Yes** | Failures expected at runtime |
| Environment variables | **Yes** (startup) | Validate once, fail fast |
| Internal function calls | **No** | Type system provides guarantees |
| Values just created/assigned | **No** | Control flow guarantees non-null |
| Exhaustive type unions | **No** | Use `assertNever` instead |
| Post-validation code paths | **No** | Validator already handled |
| 3rd-party library returns | **Maybe** | Check if types are accurate |
| Generated code / ORMs | **Maybe** | Runtime may differ from declared types |

**Rule of thumb**: If the type system or control flow makes a state impossible, defensive code for that state is noise. If runtime conditions can produce the state regardless of types, defensive code is necessary.
