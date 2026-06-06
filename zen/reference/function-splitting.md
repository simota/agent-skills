# Function Splitting Reference

Purpose: Split long or cognitively complex functions along responsibility seams. Stronger than `extract` — designs boundaries first, splits in stages, verifies each step.

## When to Trigger

| Signal | Threshold |
|--------|-----------|
| Function length | > 50 lines |
| Cognitive complexity | > 15 (SonarSource metric) |
| Cyclomatic complexity | > 10 |
| Parameter count | > 5 |
| Multiple return-value types | mixed concerns |
| Multiple levels of nested control flow | > 3 |

**Don't split** when:
- Function is intrinsically sequential with tight coupling (e.g., tokenizer state machine)
- Splitting creates many tiny helpers used only once
- Performance-critical hot path (profile first)

## Splitting Workflow

```
1. IDENTIFY seams: data boundaries, I/O boundaries, transformation stages
2. NAME each proposed sub-function for its responsibility
3. DESIGN signatures (inputs, outputs, no hidden state)
4. EXTRACT one at a time, run tests after each
5. VERIFY cognitive complexity reduction
6. INLINE if a split turns out worse (willingness to undo)
```

## Seam Detection Heuristics

### 1. Blank-line separation

```js
function processOrder(order) {
  // --- validation ---
  if (!order.items.length) throw new Error('empty');
  for (const item of order.items) {
    if (item.quantity < 1) throw new Error('invalid quantity');
  }

  // --- pricing ---
  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  const tax = subtotal * 0.1;
  const total = subtotal + tax;

  // --- persistence ---
  db.insert('orders', { ...order, total });
  emailer.send(order.user.email, 'receipt', { total });
  return total;
}
```

Seams = blank lines. Natural splits: `validateOrder`, `priceOrder`, `persistAndNotify`.

### 2. Variable scope lifetime

Variables defined on line N, last used on line N+M, unused afterward → that block can be extracted.

### 3. Comment-marked phases

`// step 1:`, `// now do X`, `/* --- initialization --- */` comments signal extraction candidates.

### 4. Level-of-abstraction mixing

Lines doing high-level (`authorize(user)`) next to low-level (`bytes[i] ^= 0x1F`) → split into levels.

## Split Patterns

### Pattern A: Pipeline

```js
// Before (60 lines)
function importCsv(path) {
  // read + parse + validate + transform + persist
}

// After
function importCsv(path) {
  const raw = readFile(path);
  const rows = parseCsv(raw);
  const valid = validateRows(rows);
  const records = transformToRecords(valid);
  return persistRecords(records);
}
```

Each helper is independently testable with small inputs.

### Pattern B: Command/Query separation

Split when function both mutates state AND returns data derived from new state.

```js
// Before
function createUserAndGetWelcomeEmail(data) {
  const user = db.insert('users', data);
  auditLog.record('user_created', user.id);
  return buildWelcomeEmail(user);
}

// After
function createUser(data) {
  const user = db.insert('users', data);
  auditLog.record('user_created', user.id);
  return user;
}
function buildWelcomeEmail(user) { /* ... */ }

// Caller
const user = createUser(data);
const email = buildWelcomeEmail(user);
```

### Pattern C: Guard + Core + Cleanup

```js
// Before — all intermixed
function processFile(path) {
  if (!path) throw new Error('no path');
  const fh = openFile(path);
  try {
    if (fh.size === 0) return null;
    // ... 40 lines of processing ...
    fh.flush();
    audit.log(path);
    return result;
  } finally {
    fh.close();
  }
}

// After
function processFile(path) {
  assertPath(path);
  return withFile(path, processFileContents);
}

function assertPath(path) {
  if (!path) throw new Error('no path');
}

function withFile(path, fn) {
  const fh = openFile(path);
  try { return fn(fh); } finally { fh.close(); }
}

function processFileContents(fh) {
  if (fh.size === 0) return null;
  // ... 40 lines → further split if still complex
}
```

### Pattern D: Strategy extraction

Multiple branches that each do a coherent thing → named strategies.

```js
// Before
function format(value, kind) {
  if (kind === 'currency') { /* 20 lines */ }
  else if (kind === 'percent') { /* 15 lines */ }
  else if (kind === 'date') { /* 25 lines */ }
  else { return String(value); }
}

// After
const FORMATTERS = {
  currency: formatCurrency,
  percent: formatPercent,
  date: formatDate,
};
function format(value, kind) {
  return (FORMATTERS[kind] ?? String)(value);
}
```

## Naming Proposed Splits

Each split must have a name that describes **what it returns** (for query) or **what it does** (for command). Weak names signal a bad seam.

Bad names (rethink split):
- `doStuff`, `helper`, `process`, `handleIt`
- `part1`, `step2`

Good names:
- `calculateTax`, `fetchUserProfile`, `normalizeEmail`
- `assertPayloadShape`, `withTransaction`, `emitAuditEvent`

## Step-by-Step Execution

1. **Create failing test** that pins the current function's full behavior (if missing)
2. **Extract one seam** as a private helper (e.g., `_validateOrder`)
3. **Run tests** — if fail, undo and pick different seam
4. **Inline any temporary var** that's now unused in outer scope
5. **Repeat** for next seam
6. **Measure**: before/after cognitive complexity, line count, param count

## Rollback Checkpoints

Commit after each successful extraction with message `refactor(X): extract <helper> from <parent>`. If final state is worse than original, revert; keep only the extractions that improved clarity.

## Verification

- All tests pass at every intermediate commit
- Cognitive complexity per function < 15 (or at least reduced)
- No duplicated code across splits
- No parameter count inflation (> 5 args signals missing grouping → introduce options object)
- Each helper is independently testable

## Handoff

- If split reveals bad types: `/quill` for type improvements
- If splits surface dead branches: `/zen dead`
- If splits surface architectural issue (wrong layer): `/atlas` for restructure
- If hot path split degrades perf: revert, use `/bolt` for targeted optimization
