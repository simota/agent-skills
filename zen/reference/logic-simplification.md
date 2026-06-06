# Logic Simplification Reference

Purpose: Collapse verbose conditionals, ternary chains, redundant transformations, and boolean-returning conditionals into concise equivalents. **Behavior-preserving only** — no functional change, only clarity.

## Simplification Patterns

### 1. Boolean-returning conditional

```js
// Before
if (condition) { return true; } else { return false; }
// After
return condition;

// Before
return condition ? true : false;
// After
return condition;

// Before
return !condition ? false : true;
// After
return condition;
```

### 2. Redundant negation

```js
// Before
if (!(a === b))
// After
if (a !== b)

// Before
if (!items.some(x => !x.active))  // all items active
// After
if (items.every(x => x.active))
```

### 3. Nested ternary

```js
// Before (cognitive nightmare)
const status = isActive ? (isPremium ? 'premium-active' : 'active') : (isPremium ? 'premium-inactive' : 'inactive');

// After (lookup or guard)
const status =
  isActive && isPremium ? 'premium-active'
  : isActive ? 'active'
  : isPremium ? 'premium-inactive'
  : 'inactive';

// Or: lookup table (if 4+ states)
const status = STATUS_MAP[`${isActive}-${isPremium}`];
```

### 4. Redundant else after return

```js
// Before
if (condition) {
  return early;
} else {
  doWork();
  return result;
}
// After
if (condition) return early;
doWork();
return result;
```

### 5. Double iteration

```js
// Before
const filtered = items.filter(x => x.active);
const mapped = filtered.map(x => x.name);
// After (clearer intent + one pass)
const names = items.filter(x => x.active).map(x => x.name);
// Or single reduce if profiler shows perf matters
const names = items.reduce((acc, x) => x.active ? [...acc, x.name] : acc, []);
```

### 6. Chained `if ... return x; if ... return y;`

```js
// Before
if (type === 'A') { return handleA(); }
if (type === 'B') { return handleB(); }
if (type === 'C') { return handleC(); }
return handleDefault();

// After (dispatch table — clearer when 4+ branches)
const handlers = { A: handleA, B: handleB, C: handleC };
return (handlers[type] || handleDefault)();
```

### 7. Collapsed conditionals

```js
// Before
if (user) {
  if (user.active) {
    if (user.permissions.includes('admin')) {
      grantAccess();
    }
  }
}

// After
if (user?.active && user.permissions?.includes('admin')) {
  grantAccess();
}
```

### 8. Redundant null check after type guard

```ts
// Before
function getName(user: User | null): string {
  if (user === null) return 'anonymous';
  if (user.name === null || user.name === undefined) return 'anonymous';
  return user.name;
}

// After
function getName(user: User | null): string {
  return user?.name ?? 'anonymous';
}
```

## When NOT to Simplify

- If "verbose" version is clearer for domain context (don't sacrifice readability for terseness)
- If simplification changes evaluation order with side effects
- If tests assert on intermediate state (breaking tests isn't behavior-preservation)
- If the pattern is idiomatic in the project codebase (consistency wins)

## Verification

Every simplification must:

1. Pass existing unit tests unchanged
2. Produce identical output for all input combinations (use property-based test if unsure)
3. Preserve short-circuit evaluation semantics
4. Preserve exception type and message
5. Not introduce new dependencies or imports

## Handoff

- Complexity-driven simplification (cognitive complexity > 15): pair with `/zen split` for function extraction
- Magic-number laden branches: pair with `/zen constants`
- Type-unsafe branches: may need `/quill` for stricter types first
