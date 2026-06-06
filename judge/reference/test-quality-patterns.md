# Test Quality Patterns

Detection heuristics for test quality issues. Judge evaluates test quality; Radar addresses test gaps; Zen improves test readability.

---

## Overview

Test quality assessment evaluates whether tests are reliable, maintainable, and effective at catching regressions. Low test quality is often worse than low coverage — unreliable tests erode CI trust.

**Judge's role:** Evaluate test quality, report findings with severity.
**Radar's role:** Fix test logic, add missing tests, resolve flaky tests.
**Zen's role:** Improve test readability and structure.

---

## 5 Test Quality Categories

### 1. Test Isolation Violations

**What to detect:** Tests that share mutable state or depend on execution order.

**Detection heuristics:**
- Global variable mutation without reset in `afterEach`/teardown
- Shared database/file state between tests without cleanup
- Tests that pass individually but fail when run together
- Missing `beforeEach` reset for shared fixtures
- Static class properties modified in tests

**Examples:**

```typescript
// BAD: Shared mutable state
let counter = 0;

test('increment', () => {
  counter++;
  expect(counter).toBe(1);
});

test('check counter', () => {
  expect(counter).toBe(0); // FAILS because previous test mutated state
});
```

```typescript
// GOOD: Isolated state
test('increment', () => {
  let counter = 0;
  counter++;
  expect(counter).toBe(1);
});
```

**Severity:** HIGH — Isolation violations cause non-deterministic test behavior.

### 2. Flaky Test Indicators

**What to detect:** Tests likely to produce intermittent failures.

**Detection heuristics:**
- `setTimeout`/`sleep`/time-based waits in tests
- Reliance on system clock (`new Date()`, `Date.now()`)
- Network calls without mocks
- File system operations without temp directories
- Race conditions in async test setup
- Order-dependent assertions on unordered collections (Set, Map)

**Examples:**

```typescript
// BAD: Timing-dependent
test('debounce calls handler after delay', async () => {
  const handler = vi.fn();
  debounce(handler, 100)();
  await new Promise(r => setTimeout(r, 150)); // Flaky: timing-sensitive
  expect(handler).toHaveBeenCalled();
});
```

```typescript
// GOOD: Use fake timers
test('debounce calls handler after delay', () => {
  vi.useFakeTimers();
  const handler = vi.fn();
  debounce(handler, 100)();
  vi.advanceTimersByTime(100);
  expect(handler).toHaveBeenCalled();
  vi.useRealTimers();
});
```

**Severity:** HIGH — Flaky tests undermine CI reliability and developer trust.

### 3. Missing Edge Case Tests

**What to detect:** Tests that only cover the happy path.

**Detection heuristics:**
- No test for null/undefined inputs
- No test for empty arrays/strings
- No test for boundary values (0, -1, MAX_INT)
- No test for error/exception paths
- No test for concurrent/async edge cases
- Function has 3+ code paths but only 1-2 test cases

**Assessment approach:**
```
For each public function:
  1. Count code paths (if/else, switch, try/catch)
  2. Count test cases covering that function
  3. Flag if test_cases < code_paths × 0.7
```

**Severity:** MEDIUM — Missing edge cases allow regressions to slip through.

### 4. Over-Mocking

**What to detect:** Tests that mock so heavily they test the mocking framework instead of the code.

**Detection heuristics:**
- 5+ mock setups per test file
- Mocking internal implementation details (private methods, internal state)
- Mocking the system under test itself
- Mock return values that don't match real API contracts
- Assertions on mock call order (implementation testing)

**Examples:**

```typescript
// BAD: Over-mocked — tests the mock, not the code
test('processOrder', async () => {
  vi.spyOn(orderService, 'validate').mockReturnValue(true);
  vi.spyOn(orderService, 'calculateTotal').mockReturnValue(100);
  vi.spyOn(orderService, 'applyDiscount').mockReturnValue(90);
  vi.spyOn(paymentService, 'charge').mockResolvedValue({ id: 'pay_1' });
  vi.spyOn(emailService, 'send').mockResolvedValue(undefined);
  vi.spyOn(inventoryService, 'reserve').mockResolvedValue(true);

  await orderService.process(order);

  expect(paymentService.charge).toHaveBeenCalledWith(90);
  expect(emailService.send).toHaveBeenCalledTimes(1);
});
```

```typescript
// GOOD: Minimal mocking at boundaries
test('processOrder charges correct total', async () => {
  const mockPayment = { charge: vi.fn().mockResolvedValue({ id: 'pay_1' }) };
  const service = new OrderService(mockPayment);

  const result = await service.process(buildOrder({ items: [item(50), item(40)] }));

  expect(mockPayment.charge).toHaveBeenCalledWith(90);
  expect(result.status).toBe('completed');
});
```

**Severity:** MEDIUM — Over-mocking makes tests fragile and gives false confidence.

### 5. Test Readability

**What to detect:** Tests that are hard to understand or maintain.

**Detection heuristics:**
- Test name doesn't describe behavior (`test1`, `testHelper`, `it works`)
- No clear Arrange/Act/Assert structure
- Test body > 30 lines
- Deeply nested describe blocks (> 3 levels)
- Magic values without explanation
- Setup and assertion interleaved

**Examples:**

```typescript
// BAD: Obscure test
test('test1', () => {
  const r = fn({ a: 1, b: 'x', c: true, d: [1, 2] });
  expect(r).toBe(42);
});
```

```typescript
// GOOD: Descriptive test
test('calculateScore returns weighted sum of input values', () => {
  const input = { weight: 1, label: 'x', isActive: true, values: [1, 2] };

  const score = calculateScore(input);

  expect(score).toBe(42);
});
```

**Severity:** LOW — Readability issues slow down debugging but don't cause false results.

---

## Per-File Test Quality Score

### Calculation Formula

```
test_quality_score = (
    isolation      × 0.25 +
    flakiness_free × 0.25 +
    edge_cases     × 0.20 +
    mock_quality   × 0.15 +
    readability    × 0.15
) × 100
```

### Dimension Scoring

| Dimension | Score 1.0 (Perfect) | Score 0.5 (Acceptable) | Score 0.0 (Poor) |
|-----------|-------------------|----------------------|-----------------|
| **Isolation** | All tests isolated, proper cleanup | Some shared state with reset | Global mutable state, order-dependent |
| **Flakiness-free** | No timing deps, all external mocked | Minor timing sensitivity | Real network/FS calls, sleeps |
| **Edge cases** | All code paths tested | Happy path + main error path | Happy path only |
| **Mock quality** | Boundary mocks only, <3 per test | 3-5 mocks, some internal | 5+ mocks, implementation testing |
| **Readability** | Clear names, AAA, <20 lines | Decent names, some structure | Cryptic names, interleaved logic |

### Score Interpretation

| Score | Grade | Meaning |
|-------|-------|---------|
| 90-100 | Excellent | Reliable, maintainable test suite |
| 75-89 | Good | Minor improvements possible |
| 60-74 | Acceptable | Noticeable quality gaps |
| 40-59 | Fair | Significant issues, should improve |
| < 40 | Poor | Tests may be doing more harm than good |

---

## Reporting Format

### In Judge Review Report

Add to the standard review report:

```markdown
### Test Quality Findings

#### Overall Test Quality Score: [X/100] ([Grade])

| Dimension | Score | Key Issue |
|-----------|-------|-----------|
| Isolation | X/100 | [Main finding or "Clean"] |
| Flakiness | X/100 | [Main finding or "Clean"] |
| Edge Cases | X/100 | [Main finding or "Clean"] |
| Mocking | X/100 | [Main finding or "Clean"] |
| Readability | X/100 | [Main finding or "Clean"] |

#### Test Quality Issues

| ID | Category | Severity | File | Issue |
|----|----------|----------|------|-------|
| TQ-001 | Isolation | HIGH | `test/auth.test.ts` | Shared DB state without cleanup |
| TQ-002 | Flakiness | HIGH | `test/api.test.ts` | Real HTTP calls without mock |
| TQ-003 | Readability | LOW | `test/utils.test.ts` | Test names don't describe behavior |
```

---

## Handoff Routing

### To Radar (Test Logic)

Route when: isolation violations, flaky patterns, missing edge cases

```markdown
## JUDGE_TO_RADAR_HANDOFF (Test Quality)

**Review ID**: [PR# or scope]
**Type**: Test Quality Issues

**Findings**:
| ID | Category | File | Issue | Priority |
|----|----------|------|-------|----------|
| TQ-001 | Isolation | `test/auth.test.ts` | Shared DB state | HIGH |
| TQ-002 | Flakiness | `test/api.test.ts` | Real HTTP calls | HIGH |
| TQ-003 | Edge Cases | `test/order.test.ts` | Missing null input test | MEDIUM |

**Request**: Fix isolation issues, add missing edge case tests, eliminate flaky patterns.
```

### To Zen (Test Readability)

Route when: readability issues, structural problems

```markdown
## JUDGE_TO_ZEN_HANDOFF (Test Quality)

**Review ID**: [PR# or scope]
**Type**: Test Readability Improvement

**Findings**:
| ID | Category | File | Issue | Priority |
|----|----------|------|-------|----------|
| TQ-004 | Readability | `test/utils.test.ts` | Obscure test names | LOW |
| TQ-005 | Readability | `test/service.test.ts` | No AAA structure | LOW |

**Request**: Apply test readability refactoring (Recipe 6: AAA structure, clear naming).
```
