# Framework-Specific Review Guide

Targeted review prompts and common issues per framework.

---

## React Review Focus

```bash
codex review --base main "Focus on React patterns: hook dependencies, key props, memo usage, state management, cleanup in useEffect"
```

| Issue | Severity | What to Look For |
|-------|----------|------------------|
| Missing useEffect dependency | HIGH | ESLint exhaustive-deps violations |
| Missing key prop | MEDIUM | Lists without unique keys |
| Unnecessary re-renders | MEDIUM | Objects/functions in deps without useMemo/useCallback |
| State update after unmount | HIGH | Async operations without cleanup |
| Prop drilling | INFO | Pass to Zen for refactoring |

```typescript
// BAD: Missing dependency
useEffect(() => {
  fetchUser(userId);  // userId not in deps
}, []);

// GOOD: Complete dependencies
useEffect(() => {
  fetchUser(userId);
}, [userId]);
```

---

## Next.js Review Focus

```bash
codex review --base main "Focus on Next.js: Server/Client boundaries, use client directive, metadata, data fetching patterns, route handlers"
```

| Issue | Severity | What to Look For |
|-------|----------|------------------|
| Client hook in Server Component | CRITICAL | useState/useEffect without 'use client' |
| Missing 'use client' | HIGH | Interactive component without directive |
| Incorrect data fetching | MEDIUM | fetch in Client Component (should be Server) |
| Missing error.tsx | MEDIUM | Route without error boundary |
| Hardcoded revalidate | LOW | Magic numbers for cache times |

```typescript
// BAD: Hook in Server Component
// app/page.tsx (Server Component by default)
import { useState } from 'react';
export default function Page() {
  const [count, setCount] = useState(0); // Error: useState in Server Component
}

// GOOD: Properly marked Client Component
'use client';
import { useState } from 'react';
export default function Counter() {
  const [count, setCount] = useState(0);
}
```

---

## Express/Node.js Review Focus

```bash
codex review --base main "Focus on Express: middleware order, error handling, async/await patterns, input validation, response handling"
```

| Issue | Severity | What to Look For |
|-------|----------|------------------|
| Missing error middleware | HIGH | No `(err, req, res, next)` handler |
| Async without try/catch | HIGH | async handler without error handling |
| Middleware order wrong | MEDIUM | Auth after route handler |
| No input validation | HIGH | req.body used directly |
| Response after send | MEDIUM | Code after res.send() |

```typescript
// BAD: Async without error handling
app.get('/users', async (req, res) => {
  const users = await db.getUsers(); // Unhandled rejection
  res.json(users);
});

// GOOD: Proper async error handling
app.get('/users', async (req, res, next) => {
  try {
    const users = await db.getUsers();
    res.json(users);
  } catch (error) {
    next(error);
  }
});
```

---

## TypeScript Review Focus

```bash
codex review --base main "Focus on TypeScript: type safety, any usage, type assertions, null checks, generic constraints"
```

| Issue | Severity | What to Look For |
|-------|----------|------------------|
| `any` type usage | MEDIUM | Explicit `any` without justification |
| Unsafe type assertion | HIGH | `as` without runtime check |
| Missing null check | HIGH | Non-null assertion `!` without guarantee |
| Implicit any | MEDIUM | Missing return type on complex functions |
| Type widening issues | LOW | Const assertions missing |

---

## Python Review Focus

```bash
codex review --base main "Focus on Python: type hints, exception handling, resource management, mutable defaults, async patterns"
```

| Issue | Severity | What to Look For |
|-------|----------|------------------|
| Mutable default argument | HIGH | `def f(items=[])` |
| Bare except | MEDIUM | `except:` without specific type |
| Missing context manager | MEDIUM | File/DB open without `with` |
| Missing type hints | LOW | Public API without annotations |
| Unclosed async resource | HIGH | `aiohttp.ClientSession` without `async with` |

---

## Go Review Focus

```bash
codex review --base main "Focus on Go: error handling, goroutine leaks, defer patterns, nil checks, context propagation"
```

| Issue | Severity | What to Look For |
|-------|----------|------------------|
| Ignored error return | HIGH | `result, _ := fn()` on fallible call |
| Goroutine leak | CRITICAL | Goroutine without exit path |
| Missing defer close | MEDIUM | Resource open without `defer .Close()` |
| Nil pointer dereference | HIGH | No nil check after type assertion |
| Missing context cancel | MEDIUM | `context.WithCancel` without `defer cancel()` |
