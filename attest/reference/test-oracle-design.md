# Test Oracle Design Reference

Purpose: Choose the right test oracle per acceptance criterion. The "oracle problem" is determining whether a test passed: when expected output is unknown, prohibitively expensive, or non-deterministic, you need an oracle pattern beyond simple `assert(actual == expected)`. Cover golden master, metamorphic, differential, model-based, consistency, statistical, and human-in-the-loop oracles.

## Scope Boundary

- **attest `oracle`**: Test oracle pattern selection (this document).
- **attest `verify` (elsewhere)**: Compliance verdict from spec.
- **attest `property` (elsewhere)**: Property generators with their own oracles.
- **Builder (elsewhere)**: Implementing the oracle.
- **Radar (elsewhere)**: Authoring example tests against the oracle.
- **Oracle (the agent, distinct from this concept)**: AI/ML evaluation; unrelated to test oracles.

## The Oracle Problem

A test oracle is the mechanism that decides PASS/FAIL. For most code, the oracle is a hard-coded expected value. But:

- Output is too complex (image, ML model output)
- Expected value is unknown (numerical solver, simulation)
- Many valid outputs (sorting unstable, set ops)
- Non-deterministic (concurrent, distributed)
- Expected value depends on impl (golden test post-implementation)

These call for a different oracle pattern.

## Seven Oracle Patterns

| Pattern | Use when | Strength | Risk |
|---------|----------|----------|------|
| **Specification** | Spec gives explicit expected output | Authoritative | Spec ambiguity → wrong oracle |
| **Reference impl** | A simpler/slower correct version exists | High confidence | Reference may have bugs too |
| **Differential** | Two impls of same spec | Mutual checking | Both may share a flaw |
| **Metamorphic** | Expected output unknown but relations hold | Tests untestable code | Relations need design care |
| **Golden master** | Legacy / migration | Pinning current behavior | Pins bugs as "correct" |
| **Statistical** | Non-deterministic (ML, randomized) | Distribution-aware | Flaky on tight thresholds |
| **Consistency** | Cross-state invariant | Catches drift | Doesn't catch "wrong but consistent" |
| **Human review** | Subjective (UX, NL gen) | Final arbiter | Slow, costly, biased |

## Pattern 1: Specification Oracle

```python
def test_iban_validation():
    assert validate_iban("GB82WEST12345698765432") == True
    assert validate_iban("GB82WEST12345698765431") == False  # invalid checksum
```

Use when: AC names exact expected outputs.
Strong if: spec is precise, examples cover the partition.

## Pattern 2: Reference Implementation Oracle

```python
def test_optimized_matches_reference():
    for case in random_cases:
        assert optimized_solver(case) == reference_solver(case)
```

The reference is slower, simpler, obviously correct. Use to validate optimized impls (FFT, hash tables, JIT).

```rust
// Reference
fn fib_ref(n: u32) -> u64 {
    if n < 2 { n as u64 } else { fib_ref(n-1) + fib_ref(n-2) }
}
// Optimized
proptest! {
    #[test]
    fn fib_optimized_matches(n in 0u32..30) {
        prop_assert_eq!(fib_iter(n), fib_ref(n));
    }
}
```

## Pattern 3: Differential Oracle

```typescript
test('json parsers agree', () => {
  fc.assert(fc.property(fc.jsonValue(), (v) => {
    const a = parserA.parse(JSON.stringify(v));
    const b = parserB.parse(JSON.stringify(v));
    expect(a).toEqual(b);
  }));
});
```

Use when: multiple impls of the same spec exist (compilers, parsers, crypto libs, browsers). Used in fuzzers like `csmith`, `Csmith`, `jsfunfuzz`, libFuzzer differential mode.

Limitation: shared bug across impls is invisible.

## Pattern 4: Metamorphic Testing

When you don't know `f(x)` but you know relationships between `f(x)` and `f(x')`.

```python
# Search engine: relevance ranking
def test_metamorphic_search():
    r1 = search("python testing")
    r2 = search("Python Testing")  # case change shouldn't matter
    assert r1 == r2

    r3 = search("python testing tutorial")  # adding term refines
    assert set(r3) <= set(r1)  # new results are subset of broader

# Numerical: integral
def test_integral_metamorphic():
    a, b, c = 0, 5, 10
    f = lambda x: x**2
    assert abs(integrate(f, a, c) - (integrate(f, a, b) + integrate(f, b, c))) < 1e-9
```

Common metamorphic relations (MRs):
- **Permutation**: `sort(perm(L)) == sort(L)`
- **Scaling**: `mean(L * 2) == 2 * mean(L)`
- **Symmetry**: `cos(-x) == cos(x)`
- **Composition**: `f(f(x)) == f(x)` (idempotent), or `g(f(x)) == h(x)`
- **Subset**: query refinement → result subset
- **Translation invariance**: image classifier output stable under small shift

Critical for: ML systems, search ranking, numerical methods, graphics, simulators (where ground truth is hard).

## Pattern 5: Golden Master

```python
def test_invoice_render_matches_golden():
    actual = render_invoice(fixture_invoice)
    golden = read_file("tests/golden/invoice_001.html")
    assert actual == golden, save_diff_for_review(actual, golden)

# Update flow:
# pytest --update-golden  # write current output as new golden
# git diff tests/golden/  # human review
```

Use when: refactoring legacy without spec; migration A → B; complex outputs (HTML render, AST dump). Workflow: implementation produces baseline → freeze as golden → future runs compare.

Risks:
- Pins bugs as "correct" (run before refactor; don't introduce after).
- Whitespace, ID, timestamp churn → false fails (normalize first).
- Tempting to "regenerate" instead of investigating diff (DON'T).

## Pattern 6: Statistical Oracle

For non-deterministic systems (ML, randomized algos, distributed).

```python
def test_classifier_accuracy():
    accuracy = evaluate(model, test_set)
    assert accuracy > 0.85, f"Accuracy regression: {accuracy}"

def test_load_balancer_distribution():
    counts = simulate_requests(n=10000, lb=lb)
    chi_sq = chi_square(counts, expected_uniform)
    assert chi_sq.pvalue > 0.01  # uniform distribution
```

Use Chi-square / KS test / confidence intervals — not point comparison. Set thresholds that catch regression but not noise (calibrate on history).

## Pattern 7: Consistency Oracle

```python
def test_cache_db_consistency():
    user = create_user("alice")
    cache_value = cache.get(user.id)
    db_value = db.find_user(user.id)
    assert cache_value == db_value

def test_event_count_consistency():
    events = audit.fetch_user_events(user_id)
    assert events.count("login") == metrics.login_count(user_id)
```

Cross-system invariants. Use to catch silent drift between cache/DB, primary/replica, log/metric.

## Pattern 8: Model-Based Oracle (Stateful)

```python
class CacheModel:
    def __init__(self): self.dict = {}
    def put(self, k, v): self.dict[k] = v
    def get(self, k): return self.dict.get(k)

# Test under random sequences
for seq in random_command_sequences:
    real = LRUCache(capacity=3)
    model = CacheModel()
    for cmd in seq:
        cmd.apply(real)
        cmd.apply(model)
        assert real.get(cmd.key) == model.get(cmd.key)
```

Use with stateful property tests (Hypothesis RuleBasedStateMachine, fast-check Commands).

## Pattern 9: Human-in-the-Loop

```python
@pytest.mark.skipif(not RUN_HUMAN, reason="manual review")
def test_generated_summary():
    output = llm.summarize(article)
    save_for_review(article, output)
    # Human reviewer confirms quality next morning
```

Subjective: UX copy quality, image generation, NL generation. Pair with cheaper proxies (length, profanity filter, factuality eval) for CI; full human review on a sample.

## AC → Oracle Selection

| AC characteristic | Oracle |
|-------------------|--------|
| "Output equals X" with concrete value | Specification |
| "Output equals reference impl" | Reference |
| "Two implementations agree" | Differential |
| "Output unknown but relation R holds" | Metamorphic |
| "Refactor preserves behavior" | Golden master |
| "Statistical accuracy ≥ N%" | Statistical |
| "State invariant I holds" | Consistency or Model-based |
| "Subjective quality" | Human + cheaper proxy |

## Choosing Multiple Oracles

A robust suite layers oracles:

```
Spec (explicit examples) — fast feedback
+ Property (forall) with metamorphic relations — exploration
+ Differential against reference — confidence
+ Golden for complex outputs — pinning
+ Statistical for stochastic — distribution check
+ Consistency for cross-system invariants — drift detection
```

## Workflow

```
EXTRACT     →  per AC, identify what makes "correct" determinable
            →  classify into the seven patterns

DESIGN      →  primary oracle: best-fit pattern
            →  secondary: cheaper proxy for fast feedback

DERIVE MRs  →  for metamorphic: enumerate relations from spec invariants
            →  document each MR with rationale

GOLDEN      →  freeze only behavior verified correct (not just current output)
            →  normalization rules (timestamps, IDs)
            →  regen policy: human review required

STATISTICAL →  baseline measurement; thresholds with margin
            →  flake budget; rerun rule

CONSISTENCY →  cross-system invariants; alarm on drift
            →  pair with monitoring

HUMAN       →  sample size; reviewer instructions; rotation
            →  cheaper automated proxy for CI gating

CI          →  fast oracles: PR; slow + statistical: nightly
            →  golden updates require code review

HANDOFF     →  Builder: implement oracle code
            →  Radar: example tests against the oracle
            →  Siege mutation: validate oracle catches mutants
```

## Output Template

```markdown
## Test Oracle Plan: [Module / AC set]

### Per-AC Oracle Mapping
| AC | Pattern | Justification | Cost |
|----|---------|---------------|------|
| AC-001 | Specification | Spec lists 3 concrete examples | Low |
| AC-002 | Metamorphic | Expected output unknown; symmetry MR holds | Med |
| AC-003 | Differential | Reference impl in legacy code | Med |
| AC-004 | Golden master | Pre-migration HTML render baseline | Med (review) |
| AC-005 | Statistical | Stochastic ML model; accuracy threshold | High |
| AC-006 | Consistency | Cache ↔ DB invariant | Low |

### Metamorphic Relations
- MR1: permutation invariance — sort(perm(L)) == sort(L)
- MR2: scaling — sum(L*2) == 2*sum(L)
- MR3: subset refinement — search(q + extra) ⊆ search(q)

### Golden Files
- Path: tests/golden/
- Normalization: strip timestamps, UUIDs
- Update policy: human review + label approved-by

### Statistical Thresholds
- Accuracy ≥ 0.85 (95% CI lower bound)
- Distribution chi-square p > 0.01

### Consistency Invariants
- Cache value == DB value (eventual; max 5s lag)
- Audit count == metric count (per hour bucket)

### Human Review Plan
- Sample: 50 random outputs / week
- Reviewers: 2-of-3 majority
- Rubric: clarity (1-5), accuracy (1-5)
- Cheaper proxy: length 50-200 words, profanity filter

### Mutation Testing
- Run Siege mutation against oracle suite
- Mutants killed: target ≥ 70%

### Handoffs
- Builder: implement reference impl + golden update tooling
- Radar: example tests against each oracle
- Siege: mutation campaign to validate oracles
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| `assert actual == expected` when output is non-deterministic | Use statistical or metamorphic |
| Golden master regenerated without review | Require human approval; CI rejects auto-regen |
| Differential with two impls sharing a library | At least one impl must be independently derived |
| Statistical threshold tighter than measurement noise | Calibrate; add margin; rerun N times |
| Metamorphic relation derived from impl, not spec | MRs must come from spec / domain truth |
| Human review without rubric | Define rubric; train reviewers; measure agreement |
| Cheaper proxy as full replacement for human | Proxy gates fast feedback; human samples final |
| Consistency oracle but no monitoring on prod | Same invariant should also alarm in production |
| Golden file with timestamps / random IDs | Normalize before comparison |
| Reference impl that's actually optimized impl renamed | Reference must be obviously correct, not equivalent |
| One oracle for everything | Layer: spec + property + golden + consistency |
| Oracle without mutation-test validation | Mutation reveals oracle blind spots |

## Deliverable Contract

When `oracle` completes, emit:

- **Per-AC oracle mapping** with justification.
- **Metamorphic relations** documented with rationale.
- **Golden file** management plan + normalization.
- **Statistical thresholds** with calibration data.
- **Consistency invariants** + cross-system pairing.
- **Human review** plan with rubric and cheaper proxy.
- **Mutation testing** validation plan.
- **Handoffs**: Builder, Radar, Siege.

## References

- "The Oracle Problem in Software Testing: A Survey" — Barr, Harman, McMinn, Shahbaz, Yoo (TSE 2015)
- "Metamorphic Testing: A Review of Challenges and Opportunities" — Chen et al. (ACM CSUR 2018)
- T.Y. Chen — original metamorphic testing paper (1998)
- "Approximation-Based Test Oracles for Numerical Programs" — Wong et al.
- *Working Effectively with Legacy Code* — Michael Feathers (golden master concept)
- Approval Tests — approvaltests.com (Llewellyn Falco)
- John Hughes — QuickCheck shrink + property semantics
- "Differential Fuzzing" — Csmith, jsfunfuzz, libFuzzer modes
- "Statistical Testing of Software" — Trammell, *Software Testing in the Real World*
- *Specification by Example* — Gojko Adzic
- ISO/IEC/IEEE 29119-4 — test techniques (oracles, MRs)
- Coq / Lean — formal verification as ultimate oracle (when affordable)
