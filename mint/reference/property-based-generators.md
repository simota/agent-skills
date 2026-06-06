# Property-Based Testing Data Generators

**Purpose:** Design data generators for property-based and fuzz testing.
**Read when:** Building custom arbitraries/strategies for property-based tests.

> **2026 framing.** Property-based generators became more load-bearing in 2026 specifically because they survive the AI-generated test problem: a Claude Code / Cursor-authored test suite often hits 80% line coverage with assertions too weak to catch real regressions (see `radar/reference/ai-assisted-testing.md`). Property tests kill whole families of mutants at once because they assert on *invariants* (idempotence, commutativity, round-trip), not on a fixed expected string the AI happened to emit. Treat property tests as the **AI-codegen safety net**, not an optional add-on, for any module touched by AI authoring.

---

## Concept

Property-based testing generates many random inputs to verify that properties (invariants) hold. Mint designs the **generators** (arbitraries/strategies) that produce these inputs.

```
Generator → Random Input → Function Under Test → Property Check
                ↑                                      ↓
            Mint's job                           Radar's job
```

---

## Generator Design Patterns

### 1. Composite Generator

Build complex objects from simpler generators.

```typescript
import fc from 'fast-check';

// Primitive generators
const emailGen = fc.emailAddress();
const nameGen = fc.string({ minLength: 1, maxLength: 100 });
const roleGen = fc.constantFrom('user', 'admin', 'moderator');

// Composite
const userGen = fc.record({
  name: nameGen,
  email: emailGen,
  role: roleGen,
  age: fc.integer({ min: 0, max: 150 }),
  tags: fc.array(fc.string(), { maxLength: 5 }),
});

// Relational composite
const orderGen = fc.record({
  user: userGen,
  items: fc.array(
    fc.record({
      productId: fc.integer({ min: 1 }),
      quantity: fc.integer({ min: 1, max: 100 }),
      price: fc.float({ min: 0.01, max: 99999.99 }),
    }),
    { minLength: 1, maxLength: 50 }
  ),
  status: fc.constantFrom('pending', 'paid', 'shipped'),
});
```

### 2. Weighted Distribution Generator

Control the probability distribution of generated values.

```typescript
const orderStatusGen = fc.frequency(
  { weight: 60, arbitrary: fc.constant('paid') },
  { weight: 20, arbitrary: fc.constant('pending') },
  { weight: 10, arbitrary: fc.constant('shipped') },
  { weight: 5, arbitrary: fc.constant('cancelled') },
  { weight: 5, arbitrary: fc.constant('refunded') },
);
```

### 3. Dependent Generator

Later values depend on earlier ones.

```typescript
const dateRangeGen = fc.tuple(
  fc.date({ min: new Date('2020-01-01'), max: new Date('2025-12-31') }),
).chain(([start]) =>
  fc.tuple(
    fc.constant(start),
    fc.date({ min: start, max: new Date(start.getTime() + 30 * 86400000) }),
  )
);
// Guarantees: end >= start, within 30 days
```

### 4. Domain-Specific Generator

Encode business rules into the generator itself.

```typescript
// Valid credit card number (Luhn algorithm)
const creditCardGen = fc.string({ minLength: 15, maxLength: 16 })
  .filter(s => /^\d+$/.test(s))
  .map(s => {
    const digits = s.split('').map(Number);
    // Apply Luhn check digit
    let sum = 0;
    for (let i = digits.length - 2; i >= 0; i -= 2) {
      let d = digits[i] * 2;
      if (d > 9) d -= 9;
      digits[i] = d;
    }
    sum = digits.reduce((a, b) => a + b, 0);
    digits[digits.length - 1] = (10 - (sum % 10)) % 10;
    return digits.join('');
  });

// Valid Japanese phone number
const jpPhoneGen = fc.tuple(
  fc.constantFrom('070', '080', '090'),
  fc.stringOf(fc.constantFrom('0','1','2','3','4','5','6','7','8','9'), { minLength: 8, maxLength: 8 }),
).map(([prefix, rest]) => `${prefix}-${rest.slice(0,4)}-${rest.slice(4)}`);
```

---

## Shrinking Strategy

When a property fails, the framework **shrinks** the failing input to find the minimal counterexample.

```typescript
// Custom shrinkable generator
const positiveIntGen = fc.nat().map(n => n + 1);
// Shrinks toward 1 (smallest positive integer)

// Array that shrinks both length and elements
const sortedArrayGen = fc.array(fc.integer())
  .map(arr => arr.sort((a, b) => a - b));
// Shrinks toward [] or [0]
```

### Tips for Shrink-Friendly Generators

1. Prefer `map` over `filter` — filtered values can't be shrunk
2. Build from small primitives — each piece shrinks independently
3. Avoid `filter` with low acceptance rates — slow and poor shrinking
4. Use `chain` for dependent values — preserves shrinkability

---

## Common Property Patterns

| Property | Generator Needs | Example |
|----------|----------------|---------|
| Roundtrip | Any valid input | `decode(encode(x)) === x` |
| Idempotency | Any valid input | `f(f(x)) === f(x)` |
| Invariant | Domain-constrained | `sort(xs).length === xs.length` |
| Commutativity | Pairs of inputs | `f(a,b) === f(b,a)` |
| Monotonicity | Ordered pairs | `a <= b → f(a) <= f(b)` |
| No-crash | Adversarial inputs | `f(x)` does not throw |

---

## Integration with Radar

Mint designs generators; Radar writes properties and assertions.

```yaml
MINT_TO_RADAR_HANDOFF:
  generators:
    - name: userGen
      file: "tests/generators/user.gen.ts"
      properties_to_test:
        - "User creation roundtrip through serialization"
        - "Email validation accepts all generated emails"
        - "Age boundary values handled correctly"
    - name: orderGen
      file: "tests/generators/order.gen.ts"
      properties_to_test:
        - "Order total equals sum of item prices × quantities"
        - "Order status transitions are valid"
```
