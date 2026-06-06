# Property-Based Testing Reference

Purpose: Generalize spec ACs into properties (universally-quantified invariants) and emit framework-specific code. Cover Hypothesis (Python), fast-check (JS/TS), jqwik (Java), proptest (Rust), ScalaCheck, and FsCheck. Replace example-based tests with adversarial-by-design generators that include shrinking and stateful machines.

## Scope Boundary

- **attest `property`**: Property derivation + framework-specific authoring (this document).
- **attest `bdd` (elsewhere)**: Example-based BDD scenarios.
- **Radar (elsewhere)**: Edge-case test addition (complementary, not property-based).
- **Mint (elsewhere)**: Static fixture / factory generation.
- **Siege `mutation` (elsewhere)**: Mutation testing of test quality (orthogonal).

## Property vs Example

| Test type | Shape | Coverage |
|-----------|-------|----------|
| Example | "For input `[3, 1, 2]`, sort returns `[1, 2, 3]`" | One case |
| Property | "For all lists L, sort(L) is sorted AND a permutation of L" | Infinite cases (sampled) |

Properties find bugs you didn't think of. Examples confirm bugs you knew about.

## The Six Property Patterns

| Pattern | Shape | Example |
|---------|-------|---------|
| **Invariant** | `P(x)` always holds after operation | `len(sort(L)) == len(L)` |
| **Round-trip** | `decode(encode(x)) == x` | JSON, base64, serialization |
| **Idempotency** | `f(f(x)) == f(x)` | normalize, sort, deduplicate |
| **Commutativity** | `f(x, y) == f(y, x)` | set union, integer addition |
| **Associativity** | `f(f(x, y), z) == f(x, f(y, z))` | string concat, monoid ops |
| **Oracle (model)** | `f(x) == referenceImpl(x)` | optimized vs reference impl |

Plus stateful machines: properties that hold across a sequence of operations (used for testing state machines, caches, databases).

## Hypothesis (Python)

```python
from hypothesis import given, strategies as st
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant

@given(st.lists(st.integers()))
def test_sort_invariant(xs):
    sorted_xs = sorted(xs)
    assert len(sorted_xs) == len(xs)
    assert all(a <= b for a, b in zip(sorted_xs, sorted_xs[1:]))
    assert sorted(sorted_xs) == sorted_xs  # idempotent

@given(st.text())
def test_json_roundtrip(s):
    import json
    assert json.loads(json.dumps(s)) == s

@given(st.dictionaries(st.text(), st.integers()))
def test_merge_commutativity(d1):
    d2 = {"k": 1}
    assert {**d1, **d2} == {**d2, **d1} or set(d1.keys()) & {"k"}
```

Stateful (cache LRU example):
```python
class LRUCacheMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.cache = LRUCache(capacity=3)
        self.model = {}

    @rule(key=st.text(), value=st.integers())
    def put(self, key, value):
        self.cache.put(key, value)
        self.model[key] = value
        if len(self.model) > 3:
            self.model.pop(next(iter(self.model)))

    @rule(key=st.text())
    def get(self, key):
        assert self.cache.get(key) == self.model.get(key)

    @invariant()
    def size_invariant(self):
        assert self.cache.size() <= 3

TestLRU = LRUCacheMachine.TestCase
```

## fast-check (JS/TS)

```typescript
import fc from 'fast-check';

test('sort invariant', () => {
  fc.assert(fc.property(fc.array(fc.integer()), (xs) => {
    const s = [...xs].sort((a, b) => a - b);
    expect(s.length).toBe(xs.length);
    for (let i = 1; i < s.length; i++) expect(s[i-1] <= s[i]).toBe(true);
  }));
});

test('JSON round-trip', () => {
  fc.assert(fc.property(fc.jsonValue(), (v) => {
    expect(JSON.parse(JSON.stringify(v))).toEqual(v);
  }));
});
```

Stateful (model-based):
```typescript
class CacheCommand implements fc.Command<Cache, Map<string, number>> {
  constructor(readonly key: string, readonly value: number) {}
  check = () => true;
  run(model: Map<string, number>, real: Cache) {
    real.put(this.key, this.value);
    model.set(this.key, this.value);
    if (model.size > 3) model.delete(model.keys().next().value);
    expect(real.size()).toBeLessThanOrEqual(3);
  }
}
```

## jqwik (Java)

```java
import net.jqwik.api.*;

class SortProperties {
    @Property
    boolean sortedListIsSorted(@ForAll List<Integer> xs) {
        List<Integer> sorted = xs.stream().sorted().toList();
        return IntStream.range(1, sorted.size())
            .allMatch(i -> sorted.get(i-1) <= sorted.get(i));
    }

    @Property
    boolean roundtripJson(@ForAll("jsonValue") String s) throws Exception {
        return objectMapper.readValue(objectMapper.writeValueAsString(s), String.class).equals(s);
    }
}
```

## proptest (Rust)

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn sort_is_sorted(mut xs: Vec<i32>) {
        xs.sort();
        for w in xs.windows(2) { assert!(w[0] <= w[1]); }
    }

    #[test]
    fn json_roundtrip(s: String) {
        let json = serde_json::to_string(&s).unwrap();
        let back: String = serde_json::from_str(&json).unwrap();
        assert_eq!(s, back);
    }
}
```

## ScalaCheck

```scala
import org.scalacheck.Prop.forAll

property("sort idempotent") = forAll { (xs: List[Int]) =>
  xs.sorted == xs.sorted.sorted
}

property("set union commutative") = forAll { (a: Set[Int], b: Set[Int]) =>
  (a union b) == (b union a)
}
```

## FsCheck (.NET)

```csharp
using FsCheck.Xunit;

public class SortProps {
    [Property]
    public bool SortIsSorted(List<int> xs) {
        var s = xs.OrderBy(x => x).ToList();
        return s.Zip(s.Skip(1)).All(p => p.First <= p.Second);
    }
}
```

## AC → Property Translation

| AC pattern | Property |
|------------|----------|
| "X must be unique" | `forall xs: nub(map f xs).length == map f xs.length` (per group) |
| "Result is monotonic in input" | `forall x, y: x <= y => f(x) <= f(y)` |
| "Encoding round-trips" | `forall x: decode(encode(x)) == x` |
| "Commutative operation" | `forall x, y: f(x, y) == f(y, x)` |
| "Associative operation" | `forall x, y, z: f(f(x,y),z) == f(x,f(y,z))` |
| "Idempotent operation" | `forall x: f(f(x)) == f(x)` |
| "Conserves count" | `forall xs: len(f(xs)) == len(xs)` |
| "Preserves invariant I" | `forall x: I(x) => I(f(x))` |
| "Cache + DB consistent" | stateful: every op on cache mirrored on model |
| "Output matches reference" | `forall x: optimized(x) == reference(x)` |

## Generators

| Domain | Generator |
|--------|-----------|
| Integers in range | `st.integers(min_value=0, max_value=100)` / `fc.integer({min: 0, max: 100})` |
| Email-like strings | composite: `st.from_regex(r"\w+@\w+\.\w+")` |
| Date/time | `st.datetimes(min_value=epoch)` / `fc.date()` |
| UUID | `st.uuids()` / `fc.uuid()` |
| Recursive (tree, AST) | `st.recursive(...)` / `fc.letrec(...)` |
| Custom domain (Order) | composite from primitives + `assume()` constraints |
| Subset of valid inputs | `assume()` to filter; or `filter_map` style |

## Shrinking

When a property fails, frameworks automatically shrink the input to the minimal counterexample. Free with built-in generators; custom strategies need to define shrink:
- **Hypothesis**: built-in shrink for all `strategies.*`.
- **fast-check**: built-in for all `fc.*`; `fc.commands` for stateful.
- **jqwik / proptest / ScalaCheck**: built-in.
- Custom generator: implement shrinker (rarely needed for typical types).

## Workflow

```
EXTRACT      →  spec ACs → identify invariants
             →  list testable claims with quantifiers ("for all", "exists")

CLASSIFY     →  per claim: invariant / round-trip / idempotent / commutative / associative / oracle
             →  stateful sequences if mutable

GENERATORS   →  base types → domain types via composition
             →  filter (assume) for valid-input subsets
             →  recursive for trees / nested data

WRITE        →  one property per spec invariant
             →  use framework's @given / fc.property / @Property syntax
             →  set generation count (default: 100; raise for cheap properties)

SHRINK       →  rely on built-ins
             →  custom only if domain types lack shrink

STATEFUL     →  if behavior depends on history:
                command-based (fast-check) / RuleBasedStateMachine (Hypothesis)
             →  model = simple reference implementation
             →  invariants checked between commands

REGRESSION   →  on failure, save the seed and counterexample
             →  add as @example regression test

CI           →  PR run: 100 cases per property
             →  nightly: 10000 cases + edge corpus
             →  fail-fast on shrink-stable counterexample

HANDOFF      →  Builder: implement fix
             →  Radar: complementary edge tests
             →  attest report: property-coverage matrix
```

## Output Template

```markdown
## Property Test Package: [Module]

### Property Inventory
| ID | Property | Pattern | Generator | Framework cmd |
|----|----------|---------|-----------|---------------|
| P1 | sort produces sorted output | invariant | List<int> | @given(st.lists(st.integers())) |
| P2 | encode/decode round-trips | round-trip | str | @given(st.text()) |
| P3 | merge is commutative | commutativity | (Map, Map) | @given(maps, maps) |
| P4 | LRU cache size ≤ capacity | stateful | command sequence | RuleBasedStateMachine |

### Code
[full test code, framework-specific]

### Generators
- Custom domain types: [list]
- Constraints (assume): [list]

### Run Configuration
- PR run: 100 cases × N properties
- Nightly: 10000 cases
- Seed pinning: [yes/no]

### Coverage vs Spec
| Spec AC | Property | Status |
|---------|----------|--------|
| AC-001 | P1, P2 | covered |
| AC-002 | P3 | covered |
| AC-003 | (none) | UNCOVERED |

### Known Counterexamples
- [seed] / [shrunk input] / [why]

### Handoffs
- Builder: implement spec gap fix
- Radar: edge-case examples for fast feedback
- attest: property-coverage matrix in compliance report
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Re-implementing the impl in the property | Properties express *what*, not *how* |
| Tests without `assume`/filter on invalid inputs | Use generator constraints; don't shotgun |
| Catching exceptions silently in property | Properties should fail loudly; explicit `pytest.raises` if expected |
| Ignoring shrunk counterexample | Always inspect; shrink reveals minimal cause |
| Stateful tests without model | Need a reference; model = simple oracle |
| One mega-property | Split per claim; failures must point to one rule |
| Property + example mixed | Property asserts the invariant; examples pin known cases |
| Generator yields invalid data | Use `filter` / `assume` or compose only valid cases |
| Random seed not captured on failure | Frameworks save seeds; check the report and pin |
| Cases too low (default 100) for cheap props | Raise to 1000-10000 for fast properties |
| Cases too high for slow props | Profile; lower count + nightly long run |
| Skipping stateful properties for state machines | Stateful is where bugs hide for caches/DBs |
| Round-trip on lossy operations | Round-trip property requires bijection |
| No oracle for complex algorithms | Reference impl + diff = strongest oracle |

## Deliverable Contract

When `property` completes, emit:

- **Property inventory** with pattern classification.
- **Code** for the chosen framework.
- **Generators** including custom domain types.
- **Run configuration** (count, nightly).
- **Coverage map** against spec ACs.
- **Counterexample log** of known shrunk cases.
- **Handoffs**: Builder, Radar, attest.

## References

- Hypothesis — hypothesis.readthedocs.io (Python)
- fast-check — fast-check.dev (JS/TS)
- jqwik — jqwik.net (JVM)
- proptest — github.com/proptest-rs/proptest (Rust)
- ScalaCheck — scalacheck.org
- FsCheck — fscheck.github.io
- *Property-Based Testing with PropEr, Erlang, and Elixir* — Fred Hebert
- John Hughes — original QuickCheck paper (Haskell, 2000)
- Scott Wlaschin — "An introduction to property-based testing"
- "Choosing properties for property-based testing" — F# for Fun and Profit
- "Don't Write Tests" — John Hughes (StrangeLoop talk)
- ISO/IEC/IEEE 29119 — testing techniques (boundary, equivalence partitioning)
