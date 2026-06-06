# Test Code Refactoring Guide

Purpose: Use this file when the target is test readability, fixture structure, helper hygiene, or the Zen vs Radar boundary.

## Contents
- [Overview](#overview)
- [Test Code Smell Catalog](#test-code-smell-catalog)
- [Test Refactoring Recipes](#test-refactoring-recipes)
- [Cross-Framework Patterns](#cross-framework-patterns)
- [Zen vs Radar Boundary](#zen-vs-radar-boundary)
- [Test Refactoring Report Template](#test-refactoring-report-template)

Test-specific code smells and refactoring recipes for improving test quality without changing what is tested.

---

## Overview

Test code deserves the same care as production code. Poor test structure leads to:
- **Flaky tests** that erode CI trust
- **Slow test suites** that developers skip
- **Hard-to-maintain tests** that get deleted instead of updated
- **False confidence** from tests that don't actually verify behavior

**Zen's role:** Refactor test **structure** for readability and maintainability.
**Radar's role:** Create new tests, improve coverage, fix test logic.

---

## Test Code Smell Catalog

### 10 Test Smells

| # | Smell | Detection | Severity | Recipe |
|---|-------|-----------|----------|--------|
| 1 | **Duplicated Setup** | Same `beforeEach`/setup repeated across files | HIGH | Extract Test Fixture |
| 2 | **Helper Sprawl** | 10+ test helpers in a single file, unclear naming | MEDIUM | Extract Test Helper |
| 3 | **Assertion Roulette** | Multiple assertions without messages, unclear which failed | HIGH | Reduce Assertion Roulette |
| 4 | **Mystery Guest** | Test depends on external file/DB/env without explicit setup | HIGH | Introduce Test Data Builder |
| 5 | **Eager Test** | One test verifies too many behaviors | MEDIUM | Split into focused tests |
| 6 | **Obscure Test** | Intent unclear; reader can't tell what's being tested | HIGH | Improve Test Readability |
| 7 | **Code Duplication** | Copy-pasted assertions or setup across test cases | MEDIUM | Extract Parameterized Test |
| 8 | **Hard-Coded Data** | Magic strings/numbers in assertions without explanation | LOW | Introduce Named Test Constants |
| 9 | **Conditional Logic** | if/else/switch inside test code | MEDIUM | Split into separate test cases |
| 10 | **Dead Test** | Skipped/commented-out tests that are never re-enabled | LOW | Remove or re-enable |

### Smell Detection Heuristics

```
Duplicated Setup:   >3 test files with identical beforeEach/setUp blocks
Helper Sprawl:      >10 helper functions in one test utility file
Assertion Roulette: >3 assertions in one test without message/label
Mystery Guest:      Test reads from file system, env var, or DB without setup
Eager Test:         Single test function with >5 distinct assertions on different properties
Obscure Test:       Test name doesn't describe behavior ("test1", "testHelper")
Code Duplication:   >3 test cases with identical assertion patterns
Hard-Coded Data:    Strings like "John", "test@example.com" without named constants
Conditional Logic:  if/switch statement inside test body (not in helper)
Dead Test:          test.skip / @pytest.mark.skip / t.Skip() without issue link
```

---

## Test Refactoring Recipes

### Recipe 1: Extract Test Fixture

**Smell:** Duplicated Setup across multiple test files

**Before:**
```typescript
// user.test.ts
describe('UserService', () => {
  let db: Database;
  let userService: UserService;

  beforeEach(async () => {
    db = await createTestDatabase();
    await db.migrate();
    await db.seed('users');
    userService = new UserService(db);
  });

  afterEach(async () => {
    await db.cleanup();
  });
// ...
```

**After:**
```typescript
// fixtures/database.fixture.ts
export function useDatabaseFixture() {
  let db: Database;

  beforeEach(async () => {
    db = await createTestDatabase();
    await db.migrate();
    await db.seed('users');
  });

  afterEach(async () => {
    await db.cleanup();
  });

  return { getDb: () => db };
// ...
```

### Recipe 2: Extract Test Helper

**Smell:** Helper Sprawl — too many helpers with unclear purpose

**Before:**
```typescript
// test-utils.ts (90+ lines of mixed helpers)
export function createUser(overrides?) { ... }
export function createAdmin(overrides?) { ... }
export function createOrder(user, overrides?) { ... }
export function createProduct(overrides?) { ... }
export function mockAuth(user) { ... }
export function mockPayment(amount) { ... }
export function assertUserEquals(actual, expected) { ... }
export function assertOrderValid(order) { ... }
export function setupTestServer() { ... }
export function cleanupTestServer() { ... }
// ... 15 more functions
```

**After:**
```typescript
// test-helpers/factories.ts
export function createUser(overrides?: Partial<User>): User { ... }
export function createAdmin(overrides?: Partial<User>): User { ... }
export function createOrder(user: User, overrides?: Partial<Order>): Order { ... }
export function createProduct(overrides?: Partial<Product>): Product { ... }

// test-helpers/mocks.ts
export function mockAuth(user: User): MockAuth { ... }
export function mockPayment(amount: number): MockPayment { ... }

// test-helpers/assertions.ts
export function assertUserEquals(actual: User, expected: User): void { ... }
export function assertOrderValid(order: Order): void { ... }

// test-helpers/server.ts
// ...
```

### Recipe 3: Reduce Assertion Roulette

**Smell:** Multiple assertions without labels; failure message is unclear

**Before:**
```typescript
test('user creation', () => {
  const user = createUser({ name: 'Alice', email: 'alice@test.com' });

  expect(user.id).toBeDefined();
  expect(user.name).toBe('Alice');
  expect(user.email).toBe('alice@test.com');
  expect(user.role).toBe('user');
  expect(user.createdAt).toBeInstanceOf(Date);
  expect(user.isActive).toBe(true);
});
```

**After:**
```typescript
describe('user creation', () => {
  const user = createUser({ name: 'Alice', email: 'alice@test.com' });

  test('assigns a unique ID', () => {
    expect(user.id).toBeDefined();
  });

  test('sets provided name and email', () => {
    expect(user.name).toBe('Alice');
    expect(user.email).toBe('alice@test.com');
  });

  test('defaults role to user', () => {
    expect(user.role).toBe('user');
  });
// ...
```

**Alternative (when splitting is excessive):** Add assertion messages:
```typescript
test('user creation sets all defaults', () => {
  const user = createUser({ name: 'Alice', email: 'alice@test.com' });

  expect(user.id).toBeDefined();
  expect(user).toMatchObject({
    name: 'Alice',
    email: 'alice@test.com',
    role: 'user',
    isActive: true,
  });
  expect(user.createdAt).toBeInstanceOf(Date);
});
```

### Recipe 4: Introduce Test Data Builder

**Smell:** Mystery Guest — test depends on implicit external data

**Before:**
```typescript
test('order total calculation', () => {
  // Where does this order come from? What are its properties?
  const order = getOrderFromFixtureFile('order-123.json');
  const total = calculateTotal(order);
  expect(total).toBe(150.00); // Why 150? Mystery values
});
```

**After:**
```typescript
test('order total sums item prices with quantity', () => {
  const order = buildOrder({
    items: [
      buildOrderItem({ price: 50.00, quantity: 2 }),  // 100.00
      buildOrderItem({ price: 25.00, quantity: 2 }),   // 50.00
    ],
  });

  const total = calculateTotal(order);

  expect(total).toBe(150.00);
});

// test-helpers/builders.ts
function buildOrder(overrides: Partial<Order> = {}): Order {
// ...
```

### Recipe 5: Extract Parameterized Test

**Smell:** Code Duplication — same test logic repeated with different data

**Before:**
```typescript
test('validates email: valid format', () => {
  expect(isValidEmail('user@example.com')).toBe(true);
});
test('validates email: with subdomain', () => {
  expect(isValidEmail('user@sub.example.com')).toBe(true);
});
test('validates email: missing @', () => {
  expect(isValidEmail('userexample.com')).toBe(false);
});
test('validates email: missing domain', () => {
  expect(isValidEmail('user@')).toBe(false);
});
test('validates email: empty string', () => {
  expect(isValidEmail('')).toBe(false);
});
```

**After:**
```typescript
// Vitest/Jest
describe.each([
  { input: 'user@example.com',     expected: true,  desc: 'valid format' },
  { input: 'user@sub.example.com', expected: true,  desc: 'subdomain' },
  { input: 'userexample.com',      expected: false, desc: 'missing @' },
  { input: 'user@',                expected: false, desc: 'missing domain' },
  { input: '',                     expected: false, desc: 'empty string' },
])('validates email: $desc', ({ input, expected }) => {
  test(`"${input}" → ${expected}`, () => {
    expect(isValidEmail(input)).toBe(expected);
  });
});
```

**pytest:**
```python
@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("user@sub.example.com", True),
    ("userexample.com", False),
    ("user@", False),
    ("", False),
])
def test_validate_email(email, expected):
    assert is_valid_email(email) == expected
```

**Go:**
```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name     string
        email    string
        expected bool
    }{
        {"valid format", "user@example.com", true},
        {"subdomain", "user@sub.example.com", true},
        {"missing @", "userexample.com", false},
        {"missing domain", "user@", false},
        {"empty string", "", false},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := ValidateEmail(tt.email)
// ...
```

### Recipe 6: Improve Test Readability (AAA Structure)

**Smell:** Obscure Test — intent is unclear, setup/action/assertion are intermixed

**Before:**
```typescript
test('test1', async () => {
  const s = new Service(mockDb);
  mockDb.find.mockResolvedValue({ id: 1, n: 'A', s: 'active' });
  const r = await s.get(1);
  expect(r).not.toBeNull();
  expect(r.n).toBe('A');
  mockDb.find.mockResolvedValue(null);
  const r2 = await s.get(999);
  expect(r2).toBeNull();
});
```

**After:**
```typescript
describe('Service.get', () => {
  test('returns user when found', async () => {
    // Arrange
    const service = new Service(mockDb);
    mockDb.find.mockResolvedValue({ id: 1, name: 'Alice', status: 'active' });

    // Act
    const result = await service.get(1);

    // Assert
    expect(result).toEqual({
      id: 1,
      name: 'Alice',
      status: 'active',
    });
// ...
```

**AAA Guidelines:**
- **Arrange:** Set up preconditions and inputs
- **Act:** Execute the behavior under test (one action per test)
- **Assert:** Verify the expected outcome
- Separate sections with blank lines or `// Arrange / Act / Assert` comments
- One behavior per test function

---

## Cross-Framework Patterns

### Vitest / Jest

| Smell | Detection | Tool |
|-------|-----------|------|
| Duplicated beforeEach | Compare across `*.test.ts` files | Manual / grep |
| Missing cleanup | `afterEach`/`afterAll` absent with side effects | ESLint plugin |
| Snapshot overuse | >10 `.toMatchSnapshot()` per file | Count snapshots |

**Key refactoring patterns:**
- `describe.each` / `test.each` for parameterized tests
- `vi.fn()` / `jest.fn()` for mock consolidation
- Custom matchers via `expect.extend()` for domain assertions

### pytest

| Smell | Detection | Tool |
|-------|-----------|------|
| Fixture sprawl | >20 fixtures in `conftest.py` | Count fixtures |
| Parametrize duplication | Same test repeated with different data | Look for copy-paste |
| Missing marks | No `@pytest.mark.slow` / `@pytest.mark.integration` | Audit marks |

**Key refactoring patterns:**
- `@pytest.fixture` scoping (`function`, `class`, `module`, `session`)
- `@pytest.mark.parametrize` for data-driven tests
- `conftest.py` hierarchy for shared fixtures
- Factory fixtures (fixtures that return factories)

### Go testing

| Smell | Detection | Tool |
|-------|-----------|------|
| Missing subtests | No `t.Run()` usage | grep for `func Test` without `t.Run` |
| Helper without t.Helper() | Helper functions that don't call `t.Helper()` | Manual review |
| Table test inconsistency | Mixed table-driven and individual tests | Audit patterns |

**Key refactoring patterns:**
- Table-driven tests with `t.Run` subtests
- `t.Helper()` for proper error location in helpers
- `t.Cleanup()` for resource cleanup
- `testify/suite` for fixture-based test organization

### Rust testing

| Smell | Detection | Tool |
|-------|-----------|------|
| Missing #[should_panic] | Error tests that catch instead of panic | Manual review |
| Test module sprawl | Inline `#[cfg(test)]` modules > 200 lines | Line count |
| Missing test attributes | Tests without `#[test]` or `#[tokio::test]` | Compiler warnings |

**Key refactoring patterns:**
- `rstest` for parameterized tests and fixtures
- Separate `tests/` directory for integration tests
- `proptest` for property-based testing
- `mockall` for trait mocking

---

## Zen vs Radar Boundary

| Task | Zen | Radar |
|------|-----|-------|
| Restructure test file organization | **Primary** | |
| Rename test functions for clarity | **Primary** | |
| Extract shared test fixtures | **Primary** | |
| Convert to parameterized tests | **Primary** | |
| Apply AAA structure | **Primary** | |
| Remove dead/skipped tests | **Primary** | |
| Consolidate test helpers | **Primary** | |
| Create new test cases | | **Primary** |
| Increase coverage for uncovered code | | **Primary** |
| Add edge case tests | | **Primary** |
| Fix test logic bugs | | **Primary** |
| Add integration/E2E tests | | **Primary** |
| Fix flaky tests (timing/logic) | | **Primary** |
| Improve test assertions (logic) | Readability only | **Logic changes** |

**Rule of thumb:**
- If it changes **what** is tested → Radar
- If it changes **how** tests are structured → Zen
- If it changes **test behavior** → Radar
- If it changes **test readability** → Zen

---

## Test Refactoring Report Template

```markdown
## Test Refactoring Report: [test file/module]

### Summary
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Test Files | X | Y | ±Z |
| Test Cases | X | Y | ±Z |
| Duplicated Setup Blocks | X | Y | -Z |
| Test Helpers | X | Y | ±Z |
| Average Assertions/Test | X | Y | -Z |
| Dead/Skipped Tests | X | 0 | -X |

### Smells Resolved
- [x] [Smell]: [What was fixed] → [Recipe applied]

...
```
