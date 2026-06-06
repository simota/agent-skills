# Property-Based Testing Reference

Purpose: Use this file to design property-based tests that validate invariants across generated inputs in Siege's `property` subcommand. Property-based testing replaces a handful of hand-picked cases with hundreds of generated cases plus automatic shrinking, catching edge cases unit tests miss (empty, boundary, unicode, negative-zero, concurrent interleaving) without hand-enumerating them.

## Scope Boundary

- **Siege `property`**: invariant design, generator authoring, shrinking tuning, stateful / model-based properties. Produces properties that run in the normal unit-test suite or a dedicated nightly job.
- **Radar (elsewhere)**: example-based unit tests, edge-case tests discovered by hand, coverage improvement on normal tests. If the ask is "add tests that exercise line X," route to Radar.
- **Mint (elsewhere)**: realistic factory data for integration tests, seed datasets, fixtures. Property-based generators and Mint factories can share shapes but serve different purposes (generators explore; factories represent).
- **Siege `fuzz` (sibling)**: byte-level coverage-guided fuzzing of parsers and native code. Property testing is structured, generator-driven, and fast; fuzzing is bytes-driven and long-running.
- **Attest (elsewhere)**: spec conformance verification. A property-based test states "for all inputs X, output satisfies P"; a conformance test states "for this AC, this scenario passes." They complement but do not replace each other.

If the invariant is "some property holds for all inputs in domain D" → `property`. If it is "this specific scenario passes" → Radar. If it is "any byte sequence must not crash the parser" → `fuzz`.

## Tool Selection

| Library | Language | Pick when | Notable features |
|---------|----------|-----------|------------------|
| fast-check | TS / JS | Default for JS/TS projects, vitest/jest integration | Async properties, arbitraries, model-based `commands` |
| Hypothesis | Python | Default for Python, pytest plugin | Database of falsifying examples, `@given`, `@rule` for stateful |
| jqwik | Java (JUnit 5) | JVM projects on JUnit 5 | `@Property`, exhaustive for small domains, action sequences |
| ScalaCheck | Scala | Scala / sbt projects | The original lineage for the JVM; tight with Cats/cats-effect |
| PropEr / QuickCheck | Erlang / Haskell / OCaml | Actor-system or FP-heavy codebases | Gold-standard shrinking, stateful `proper_statem` |
| Rapid | Go | Go projects needing shrinking | Better shrinker than `testing/quick`, supports state machines |
| proptest | Rust | Rust projects | Regression file, strategy combinators, async via runtime |
| Kotest property | Kotlin | Kotlin multiplatform | Coroutine-aware, integrated with Kotest runner |

Default for a new JS/TS project: **fast-check inside the normal test runner**. For Python: **Hypothesis with `@given`** invoked from pytest.

## Workflow

```
DEFINE    →  name the invariant in plain language ("round-trip", "idempotent", "monotonic", "commutative", "never crashes")
          →  identify the input domain and its boundaries
          →  decide property kind (pure / stateful / model-based)

DESIGN    →  pick generators; start from built-ins, compose via map/filter/chain
          →  cap input size; avoid filter-heavy generators that starve the shrinker
          →  decide shrink strategy — custom shrink only when default shrinks to uninteresting cases

EXECUTE   →  run 100-1000 cases at PR tier, 10k+ in nightly
          →  seed from a stored "falsifying example database" when available
          →  record reproducing seed on any failure

ANALYZE   →  read the shrunk counter-example, not the first failing one
          →  classify: real bug / weak invariant / bad generator / flaky timing
          →  if generator is biased (never explores X), widen, don't weaken the property

REPORT    →  invariant, generator shape, shrunk counter-example, fix owner
          →  regression: add the shrunk example as an explicit unit test too
```

## Property Taxonomy

| Kind | Shape | Example |
|------|-------|---------|
| Round-trip | `decode(encode(x)) === x` | JSON serialize/parse, base64, protobuf |
| Inverse | `reverse(reverse(x)) === x` | list reverse, inverse matrix, undo/redo stack |
| Idempotent | `f(f(x)) === f(x)` | normalize, dedupe, sort, trim |
| Commutative | `f(a, b) === f(b, a)` | set union, addition, max |
| Associative | `f(f(a,b),c) === f(a,f(b,c))` | string concat, monoids |
| Invariant-preserving | `inv(x) → inv(f(x))` | balanced tree stays balanced after insert |
| Monotonic | `a ≤ b → f(a) ≤ f(b)` | pagination offset, priority queue order |
| Oracle-equivalent | `fast(x) === reference(x)` | optimized impl vs naive reference impl |
| Never-throws | `f(x)` never throws for any `x` in domain | robustness of parsers under the type system |

Pick one per property. A property testing three invariants at once is three properties wearing a trench coat.

## Generator Design

```ts
// fast-check: well-shaped generator
import fc from 'fast-check';

// Good: composed from primitives, natural shrink path, no filter
const userArb = fc.record({
  id: fc.uuid(),
  email: fc.emailAddress(),
  age: fc.integer({ min: 0, max: 150 }),
  tags: fc.array(fc.string({ minLength: 1, maxLength: 20 }), { maxLength: 10 }),
});

test('user serialization round-trips', () => {
  fc.assert(fc.property(userArb, (u) => {
    expect(parseUser(serializeUser(u))).toEqual(u);
  }));
});
```

```python
# Hypothesis: composite strategy with explicit shrink
from hypothesis import given, strategies as st

@st.composite
def balanced_tree(draw, max_depth=4):
    if max_depth == 0 or draw(st.booleans()):
        return ('leaf', draw(st.integers()))
    return ('node', draw(balanced_tree(max_depth - 1)), draw(balanced_tree(max_depth - 1)))

@given(balanced_tree())
def test_depth_is_bounded(tree):
    assert depth(tree) <= 5
```

Rules:
- **Compose, don't filter**: `fc.integer().filter(n => n > 0)` wastes cycles; use `fc.integer({ min: 1 })`.
- **Bound sizes**: unbounded arrays or strings slow runs and distort shrink paths.
- **Keep shrink natural**: if you need a custom shrinker, the domain is probably wrong.

## Stateful / Model-Based Testing

When the system under test has state (cache, queue, store, reducer), test sequences of commands against a simplified reference model.

```ts
// fast-check model-based: LRU cache vs plain-Map reference
class GetCommand implements fc.Command<Model, LRU> {
  constructor(readonly key: string) {}
  check = () => true;
  run(m: Model, r: LRU) {
    expect(r.get(this.key)).toEqual(m.get(this.key));
    m.touch(this.key);
  }
}
// ...SetCommand, EvictCommand
fc.assert(fc.property(
  fc.commands([fc.constant(new GetCommand('a')), /* ... */], { maxCommands: 50 }),
  (cmds) => fc.modelRun(() => ({ model: new Model(3), real: new LRU(3) }), cmds)
));
```

Rules:
- Reference model should be the **simplest possible implementation** — a plain dict, a list, a pure function. Complex reference models re-introduce the bug you are testing for.
- Cap command-sequence length. 50-200 is usually enough; 10k commands just slows shrinking.
- Print the failing command sequence verbatim; let the shrinker produce the minimum.

## Anti-Patterns

- Property restates the implementation: `expect(sort(x)).toEqual(sort(x))` — tautology; it passes for any `sort`.
- Filter-heavy generators: `.filter(x => x.valid)` that rejects >50% of cases starves the shrinker and bloats runtime.
- Tests with no shrunk output in the failure message — re-run with the library's verbose/shrink-report mode.
- Running 10k cases in PR tier — keeps budget reasonable at 100-1000 per property; push huge runs to nightly.
- Silencing flaky properties with `{ numRuns: 10 }` — the property is probably non-deterministic; fix the test, not the count.
- Deleting a falsifying-example database entry to make CI green — it is a regression record; commit the reproducer as an explicit test.
- Using stateful model-based testing for pure functions — use plain properties; state machines add cost without benefit.
- Treating generator coverage as code coverage — property testing explores the input domain, not line coverage. Pair with Radar.

## Handoff

**To Radar:**
- Shrunk counter-examples that should become permanent example-based regression tests.
- Domain boundaries that property testing surfaced and that deserve explicit named tests.

**To Builder:**
- Bugs the properties found — minimized reproducer plus the violated invariant statement.

**To Mint:**
- Generators that describe valid domain objects; Mint may reuse the shape for realistic factory output.

**To Siege `fuzz` (sibling):**
- If properties time out on structured inputs, fuzz the underlying parser directly for deeper coverage.

**Escape hatches / follow-ups:**
- `#TODO(agent): promote nightly property suite` when PR-tier runtime exceeds budget.
- `#TODO(agent): widen generator` when a property passes but a class of inputs is clearly unreached.
