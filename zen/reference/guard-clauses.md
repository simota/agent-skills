# Guard Clauses Reference

Purpose: Convert deeply nested `if` structures to early returns / guard clauses. Reduces cyclomatic complexity and makes the "happy path" linear.

## The Pattern

### Before (arrow-head anti-pattern)

```js
function processOrder(order) {
  if (order) {
    if (order.items && order.items.length) {
      if (order.user) {
        if (order.user.active) {
          // happy path buried 4 levels deep
          return charge(order);
        } else {
          throw new Error('inactive user');
        }
      } else {
        throw new Error('no user');
      }
    } else {
      throw new Error('no items');
    }
  } else {
    throw new Error('no order');
  }
}
```

### After (flat with guards)

```js
function processOrder(order) {
  if (!order) throw new Error('no order');
  if (!order.items?.length) throw new Error('no items');
  if (!order.user) throw new Error('no user');
  if (!order.user.active) throw new Error('inactive user');

  return charge(order);
}
```

## Transformation Rules

### Rule 1: Invert outer guard, return/throw early

```js
// Before
if (X) {
  // big body
}
// Nothing after

// After
if (!X) return;
// big body (unindented)
```

### Rule 2: Chain multiple guards top-to-bottom

Order matters — cheapest/most-likely-failure first for fast-path optimization.

```js
function canBookAppointment(user, slot) {
  if (!user) return false;              // fastest check
  if (!user.verified) return false;
  if (!slot) return false;
  if (slot.booked) return false;
  if (slot.date < Date.now()) return false;
  if (!user.planAllows(slot.type)) return false;  // slowest
  return true;
}
```

### Rule 3: Flatten `else { error }` to leading guard

```js
// Before
if (validInput(x)) {
  doWork(x);
} else {
  throw new Error('invalid');
}

// After
if (!validInput(x)) throw new Error('invalid');
doWork(x);
```

### Rule 4: Loop early-continue

```js
// Before
for (const item of items) {
  if (item.active) {
    if (item.price > 0) {
      process(item);
    }
  }
}

// After
for (const item of items) {
  if (!item.active) continue;
  if (item.price <= 0) continue;
  process(item);
}
```

### Rule 5: Extract deeply nested condition

If guards still leave pyramid, extract the inner block into a helper:

```js
// After guard conversion still nested
function handle(req) {
  if (!req) return;
  if (req.type === 'A') {
    if (req.priority === 'high') {
      // 20 lines
    } else {
      // 15 lines
    }
  } else if (req.type === 'B') {
    // 30 lines
  }
}

// Split + guards
function handle(req) {
  if (!req) return;
  if (req.type === 'A') return handleA(req);
  if (req.type === 'B') return handleB(req);
  throw new Error(`unknown type: ${req.type}`);
}

function handleA(req) {
  if (req.priority === 'high') return handleAHigh(req);
  return handleANormal(req);
}
// ...
```

## Language-Specific Idioms

### Go

```go
func process(order *Order) (Result, error) {
  if order == nil {
    return Result{}, errors.New("no order")
  }
  if len(order.Items) == 0 {
    return Result{}, errors.New("no items")
  }
  // happy path
}
```

### Python

```python
def process(order):
    if not order:
        raise ValueError("no order")
    if not order.items:
        raise ValueError("no items")
    # happy path
```

### Rust

Idiomatic Rust uses `?` + guard clauses together:

```rust
fn process(order: Option<Order>) -> Result<Receipt, Error> {
    let order = order.ok_or(Error::NoOrder)?;
    if order.items.is_empty() {
        return Err(Error::NoItems);
    }
    // happy path
}
```

### TypeScript narrowing

```ts
function process(order: Order | null): Receipt {
  if (!order) throw new Error('no order');
  // `order` is now narrowed to Order — no non-null assertions needed
  return charge(order);
}
```

## Anti-Patterns

### Anti-pattern: Multiple return is confusing

Myth. Early returns at top (guards) + single happy-path return at bottom is a well-established readable pattern. The "single return" style made sense pre-C89 when resources needed manual cleanup — modern languages with RAII / defer / try-finally don't need it.

### Anti-pattern: Guard clauses that do work

```js
// Bad — guard does side effect
if (!user) { logger.warn('no user'); return null; }

// Better — one effect per line
if (!user) {
  logger.warn('no user');
  return null;
}
```

Prefer clarity over line count when side effects are involved.

### Anti-pattern: Deep chain still hiding a loop invariant

```js
for (const x of items) {
  if (!validA(x)) continue;
  if (!validB(x)) continue;
  if (!validC(x)) continue;
  if (!validD(x)) continue;
  process(x);
}
```

If you have 4+ guards per loop iteration, extract a predicate:

```js
function shouldProcess(x) {
  return validA(x) && validB(x) && validC(x) && validD(x);
}

for (const x of items) {
  if (!shouldProcess(x)) continue;
  process(x);
}
```

## Measurement

Report before/after:

| Metric | Before | After |
|--------|--------|-------|
| Max nesting depth | 4 | 1 |
| Cyclomatic complexity | 7 | 7 (same — guards don't reduce branches) |
| Cognitive complexity | 18 | 6 |
| Line count | 24 | 18 |

**Cognitive complexity** is the key metric — guards dramatically reduce nesting penalty.

## Verification

- Tests pass unchanged
- Same exceptions thrown in same order
- Short-circuit evaluation preserved
- No change in return values for any input

## Handoff

- If guards reveal duplicated validation: extract shared `assertX()` or predicate
- If guards make function too trivial (1 line + 1 call): inline the function into caller
- If multiple functions share guard preambles: consider a middleware/decorator pattern (`/atlas` for architectural advice)
