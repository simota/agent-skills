# Advanced Testing Techniques

Purpose: High-leverage patterns beyond the basic unit/integration stack. Read this when a normal test is not enough to protect the behavior.

Contents:

- property-based testing
- contract testing
- mutation testing
- snapshot strategy
- Testcontainers

## Property-Based Testing

Use property-based tests when the behavior is better expressed as an invariant than as a small fixed example set.

### Good Fits

| Scenario | Property |
|----------|----------|
| Encode / decode | roundtrip returns the original value |
| Sorting / filtering | output stays sorted and length expectations hold |
| Parsing / validation | valid inputs are accepted, invalid ones are rejected |
| Business rules | totals never go negative, discounts never exceed price |

### Minimal Examples

```typescript
fc.assert(
  fc.property(fc.array(fc.integer()), (arr) => {
    const sorted = [...arr].sort((a, b) => a - b);
    const sortedTwice = [...sorted].sort((a, b) => a - b);
    expect(sorted).toEqual(sortedTwice);
  })
);
```

```python
@given(st.lists(st.integers()))
def test_sort_idempotent(values):
    assert sorted(sorted(values)) == sorted(values)
```

```go
rapid.Check(t, func(t *rapid.T) {
    arr := rapid.SliceOf(rapid.Int()).Draw(t, "arr")
    sort.Ints(arr)
    sorted := append([]int(nil), arr...)
    sort.Ints(arr)
    assert.Equal(t, sorted, arr)
})
```

## Contract Testing

Use contract tests when teams or services can drift independently.

### When To Use

- frontend to backend API boundaries
- service-to-service HTTP or RPC boundaries
- third-party integrations where payload shape matters
- event-driven schemas that must remain compatible

### Pact Shape

```typescript
await provider
  .addInteraction()
  .given('user 1 exists')
  .uponReceiving('a request for user 1')
  .withRequest('GET', '/api/users/1')
  .willRespondWith(200, {
    body: { id: '1', name: 'Test User' },
  });
```

Consumer and provider verification belong in the same contract chain. Do not stop at consumer-side generation.

## Mutation Testing

Mutation testing measures whether tests detect intentionally introduced faults.

### Default Thresholds

```json
{
  "thresholds": {
    "high": 80,
    "low": 60,
    "break": 50
  }
}
```

### Interpretation

| Mutation Score | Rating | Action |
|----------------|--------|--------|
| `90%+` | Excellent | Maintain, focus on changed code |
| `75-89%` | Good | Target important survivors |
| `60-74%` | Acceptable | Improve systematically |
| `< 60%` | Poor | Treat as a meaningful quality gap |

### When To Use

- critical business logic
- high line coverage but low confidence
- pre-refactor validation for risky modules

### Exclusion Rules

Common exclusions:

- generated files
- config-only modules
- type declarations
- mocks and test helpers
- log-message-only literals

### Performance Rules

| Option | Recommendation |
|--------|----------------|
| `concurrency` | CPU cores minus one |
| `coverageAnalysis: perTest` | Always enable when supported |
| `incremental` | Enable for repeat runs |
| `timeoutMS` | `10-30s` depending on suite cost |

## Snapshot Strategy

Use snapshots only for stable, intentional output shapes.

Good fits:

- serialized UI output with controlled noise
- formatter output
- structured API responses with stable fields

Avoid snapshots for:

- fast-changing copy
- large DOM trees hiding important assertions
- dynamic timestamps, IDs, and unstable ordering unless normalized

Prefer inline snapshots for small outputs; use file snapshots sparingly.

## Testcontainers

Use Testcontainers when correctness depends on a real service implementation.

```typescript
const container = await new PostgreSqlContainer().start();
const connectionString = container.getConnectionUri();
```

Best fits:

- repository or migration behavior
- queue or broker integration
- cross-service integration with realistic startup order

Avoid when:

- a pure unit test would prove the same behavior
- the repository has no container pattern and the setup cost dominates the value

## Test Pyramid Revisited

| Layer | Radar Role |
|-------|------------|
| Unit | Primary default |
| Property-based | Stress the invariant surface |
| Integration | Real boundaries with limited setup |
| Contract | Service compatibility |
| Mutation | Verify test strength |
| E2E | Hand off to Voyager |

## Quick Rules

- Reach for property-based tests when examples start missing edge space.
- Reach for contract tests when two deployable units must agree.
- Reach for mutation testing only after the normal suite is already credible.
- Reach for Testcontainers when a fake would hide the real failure mode.
