# Bug Pattern Catalog

Common bug patterns Judge detects during code review, with examples and detection strategies.

---

## Null/Undefined Patterns

| Pattern | Example | Severity | Detection |
|---------|---------|----------|-----------|
| Optional chaining missing | `user.profile.name` | HIGH | No `?.` on nullable chain |
| Unchecked array access | `items[0].id` | MEDIUM | No length check before access |
| Destructure from null | `const { id } = user` | HIGH | No nullish check before destructure |
| Promise without catch | `fetch().then()` | MEDIUM | Missing `.catch()` or try/catch |

```typescript
// BAD: Null access risk
const userName = user.profile.name;

// GOOD: Safe access
const userName = user?.profile?.name ?? 'Anonymous';
```

---

## Off-by-One Errors

| Pattern | Example | Severity | Detection |
|---------|---------|----------|-----------|
| Array bounds | `for (i <= arr.length)` | HIGH | Using `<=` with length |
| Slice end | `arr.slice(0, length)` | MEDIUM | Verify inclusive/exclusive |
| Substring end | `str.substring(0, len - 1)` | MEDIUM | Check if -1 is intentional |
| Pagination | `page * size` vs `(page - 1) * size` | HIGH | 0-based vs 1-based confusion |

```typescript
// BAD: Off-by-one
for (let i = 0; i <= items.length; i++) { // Reads past end
  process(items[i]);
}

// GOOD: Correct bounds
for (let i = 0; i < items.length; i++) {
  process(items[i]);
}
```

---

## Race Conditions

| Pattern | Example | Severity | Detection |
|---------|---------|----------|-----------|
| State update race | `setState` after unmount | HIGH | Async without cleanup |
| Shared mutable state | Multiple async writers | CRITICAL | No mutex/lock pattern |
| Check-then-act | `if (exists) delete` | HIGH | Time gap between check and action |
| Event handler race | Multiple click handlers | MEDIUM | No debounce/disable |

```typescript
// BAD: Race condition
useEffect(() => {
  fetchData().then(setData); // May set after unmount
}, []);

// GOOD: Cleanup prevents race
useEffect(() => {
  let cancelled = false;
  fetchData().then(data => {
    if (!cancelled) setData(data);
  });
  return () => { cancelled = true; };
}, []);
```

---

## Resource Leaks

| Pattern | Example | Severity | Detection |
|---------|---------|----------|-----------|
| Event listener leak | `addEventListener` without remove | MEDIUM | Missing cleanup in useEffect |
| Timer leak | `setInterval` without clear | MEDIUM | No clearInterval in cleanup |
| Subscription leak | `subscribe()` without unsubscribe | MEDIUM | Observable without teardown |
| Connection leak | Open DB/socket without close | HIGH | Missing finally/cleanup |

---

## API Contract Violations

| Pattern | Example | Severity | Detection |
|---------|---------|----------|-----------|
| Wrong HTTP method | POST for read operation | MEDIUM | Semantic method mismatch |
| Missing required field | API expects `id`, sends `userId` | HIGH | Field name mismatch |
| Type mismatch | String where number expected | HIGH | Type coercion issues |
| Missing error handling | 4xx/5xx not handled | MEDIUM | Only happy path coded |
