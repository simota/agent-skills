# Boundary Value Strategy

**Purpose:** Systematic boundary value and edge case data generation.
**Read when:** Identifying edge cases for comprehensive test data coverage.

---

## Boundary Value Analysis (BVA) Matrix

### String Fields

| Boundary | Value | Purpose |
|----------|-------|---------|
| Empty | `""` | Required field validation |
| Whitespace-only | `" "`, `"\t"`, `"\n"` | Trim/strip validation |
| Single char | `"a"` | Minimum length edge |
| Max length | `"a".repeat(MAX)` | Length constraint |
| Max length + 1 | `"a".repeat(MAX + 1)` | Overflow detection |
| Unicode | `"日本語テスト"` | CJK handling |
| Emoji | `"😀🎉"` | Multi-byte handling |
| RTL | `"مرحبا"` | Right-to-left text |
| Special chars | `"<script>alert(1)</script>"` | XSS prevention |
| SQL injection | `"'; DROP TABLE users; --"` | SQL injection prevention |
| Null bytes | `"test\x00data"` | Binary safety |
| Very long | `"a".repeat(1_000_000)` | Memory/perf stress |

### Numeric Fields

| Boundary | Value | Purpose |
|----------|-------|---------|
| Zero | `0` | Division, empty state |
| Negative one | `-1` | Sign boundary |
| MIN_SAFE_INTEGER | `-9007199254740991` | JS number limit |
| MAX_SAFE_INTEGER | `9007199254740991` | JS number limit |
| Float precision | `0.1 + 0.2` | Floating point issues |
| NaN | `NaN` | Invalid number handling |
| Infinity | `Infinity` | Overflow handling |
| Negative zero | `-0` | Edge equality |
| Very small float | `Number.EPSILON` | Precision boundary |
| Currency edge | `9999.99`, `0.01` | Financial calculations |

### Date/Time Fields

| Boundary | Value | Purpose |
|----------|-------|---------|
| Epoch | `1970-01-01T00:00:00Z` | Epoch handling |
| Pre-epoch | `1969-12-31T23:59:59Z` | Negative timestamp |
| Far future | `9999-12-31T23:59:59Z` | Year overflow |
| Leap day | `2024-02-29` | Leap year validation |
| DST spring | `2024-03-10T02:30:00` (US) | DST gap |
| DST fall | `2024-11-03T01:30:00` (US) | DST overlap |
| Timezone edge | `2024-01-01T00:00:00+14:00` | Max timezone offset |
| Millisecond | `2024-01-01T00:00:00.999Z` | Subsecond precision |

### Array/Collection Fields

| Boundary | Value | Purpose |
|----------|-------|---------|
| Empty | `[]` | Empty collection |
| Single item | `[item]` | Off-by-one |
| Max length | `Array(MAX).fill(item)` | Capacity limit |
| Duplicates | `[a, a, a]` | Uniqueness logic |
| Nested | `[[1, [2, [3]]]` | Deep nesting |
| Mixed types | `[1, "a", null, true]` | Type coercion |

### Nullable / Optional Fields

| Boundary | Value | Purpose |
|----------|-------|---------|
| null | `null` | Explicit null |
| undefined | `undefined` | Missing value (JS) |
| Missing key | `{}` (field omitted) | Schema validation |
| Empty string vs null | `""` vs `null` | Equivalence check |

---

## Combinatorial Edge Cases

### Pairwise Boundary Combination

Generate combinations that cover each pair of boundary values at least once.

```typescript
function* boundaryPairs<T>(boundaries: Record<string, T[]>) {
  const keys = Object.keys(boundaries);
  for (let i = 0; i < keys.length; i++) {
    for (let j = i + 1; j < keys.length; j++) {
      for (const vi of boundaries[keys[i]]) {
        for (const vj of boundaries[keys[j]]) {
          yield { [keys[i]]: vi, [keys[j]]: vj };
        }
      }
    }
  }
}

// Usage
const userBoundaries = {
  name: ['', 'a'.repeat(255), '日本語', '<script>'],
  age: [0, -1, 150, NaN],
  email: ['', 'invalid', 'a@b.c', 'a'.repeat(254) + '@x.co'],
};
```

---

## Property-Based Testing Generators

### Arbitraries for Common Types

```typescript
// fast-check arbitraries
import fc from 'fast-check';

const userArbitrary = fc.record({
  name: fc.string({ minLength: 1, maxLength: 255 }),
  email: fc.emailAddress(),
  age: fc.integer({ min: 0, max: 150 }),
  role: fc.constantFrom('user', 'admin', 'moderator'),
  tags: fc.array(fc.string(), { maxLength: 10 }),
});

fc.assert(
  fc.property(userArbitrary, (user) => {
    const result = validateUser(user);
    return result.isValid || result.errors.length > 0;
  })
);
```

```python
# Hypothesis strategies
from hypothesis import given, strategies as st

@given(
    name=st.text(min_size=1, max_size=255),
    age=st.integers(min_value=0, max_value=150),
    email=st.emails(),
)
def test_user_creation(name, age, email):
    user = create_user(name=name, age=age, email=email)
    assert user.id is not None
```

---

## Domain-Specific Boundaries

### E-Commerce

| Field | Boundaries |
|-------|-----------|
| Price | `0.00`, `0.01`, `9999999.99`, negative |
| Quantity | `0`, `1`, `MAX_INT`, negative |
| Discount | `0%`, `100%`, `> 100%` |
| Coupon code | expired, not-yet-valid, already-used, case-sensitive |

### Authentication

| Field | Boundaries |
|-------|-----------|
| Password | min-length, max-length, all-same-char, common-password |
| Token | expired, malformed, revoked, empty |
| Session | expired, concurrent, different-device |
| MFA code | `000000`, `999999`, expired, replay |

### Financial

| Field | Boundaries |
|-------|-----------|
| Amount | `0.00`, `0.001` (sub-cent), `MAX`, currency-specific decimals |
| Exchange rate | `0`, `1`, very small, very large |
| Account balance | exactly zero, negative (overdraft), max |
