# Multi-Language Testing

Purpose: Language-specific testing defaults for Radar outside the TS/JS baseline. Read this when the repo is Python, Go, Rust, or Java.

Contents:

- language detection
- idiomatic test patterns per language
- async and mocking defaults
- coverage commands and thresholds

## Language Detection

| Indicator | Language | Default Framework | Coverage Tool |
|-----------|----------|-------------------|---------------|
| `pytest.ini` / `pyproject.toml` | Python | pytest | coverage.py / pytest-cov |
| `go.mod` | Go | `testing` / testify | `go test -cover` |
| `Cargo.toml` | Rust | `cargo test` | tarpaulin / llvm-cov |
| `pom.xml` / `build.gradle` | Java | JUnit 5 | JaCoCo |
| `vitest.config.*` / `jest.config.*` | TypeScript / JS | Vitest / Jest | v8 / istanbul |

## Python

### Defaults

- Use `pytest.mark.parametrize` for boundary coverage.
- Use fixtures for setup and cleanup.
- Use `pytest-asyncio` 1.x (GA May 2025) for async code — major version requires `asyncio_mode` configuration and drops the legacy auto-detection mode. See [pytest-asyncio.readthedocs.io](https://pytest-asyncio.readthedocs.io/) for migration guide.
- Use `pytest-mock` or `unittest.mock` for external effects.

```python
@pytest.mark.parametrize("input_val,expected", [
    ("", True),
    ("  ", True),
    (None, True),
    ("hello", False),
])
def test_is_blank(input_val, expected):
    assert is_blank(input_val) == expected
```

```python
@pytest.fixture
def db_session():
    session = create_test_session()
    yield session
    session.rollback()
    session.close()
```

Coverage commands:

```bash
pytest --cov=src --cov-report=html --cov-report=term
pytest --cov=src --cov-fail-under=80
pytest --cov=src --cov-report=term-missing
```

## Go

### Defaults

- Prefer table-driven tests for input matrices.
- Use `require` for setup checks and `assert` for multiple follow-up expectations.
- Use `httptest` for handler tests.
- Generate mocks with gomock or mockery instead of handwritten deep stubs.

```go
func TestAdd_TableDriven(t *testing.T) {
    tests := []struct {
        name string
        a    int
        b    int
        want int
    }{
        {name: "positive", a: 2, b: 3, want: 5},
        {name: "zero", a: 0, b: 3, want: 3},
    }

    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            assert.Equal(t, tc.want, Add(tc.a, tc.b))
        })
    }
}
```

Coverage commands:

```bash
go test ./... -cover
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out -o coverage.html
go test ./... -cover | grep -E "coverage: [0-7][0-9]\\." && exit 1 || echo "OK"
```

## Rust

### Defaults

- Keep unit tests in-module for private behavior and integration tests in `tests/` for public API.
- Use parameterized tests for edge matrices.
- Use `tokio::test` for async code.
- Prefer `cargo-nextest` in CI for faster, isolated test runs (up to 3x faster than `cargo test`; per-test process isolation; RustRover 2026.1 adds native nextest IDE integration). Source: [nexte.st](https://nexte.st/)
- `cargo-mutants` integrates with nextest: `cargo mutants --test-tool nextest` for parallel mutant runs.

```rust
#[test_case("", true; "empty")]
#[test_case("  ", true; "whitespace")]
#[test_case("hello", false; "valid")]
fn is_blank_cases(input: &str, expected: bool) {
    assert_eq!(is_blank(input), expected);
}
```

### Tooling Selection (2026)

| Concern | Tool | When to reach for it |
|---------|------|----------------------|
| Property-based | `proptest` (default) / `quickcheck` | Invariants over a generated input domain. proptest has richer shrinking + a persisted regression corpus (`proptest-regressions/`); quickcheck is lighter for simple `Arbitrary` cases. |
| Snapshot | `insta` | Lock complex output (serialized structs, rendered text, error chains). `cargo insta review` for the accept/reject workflow; prefer inline snapshots for small values. |
| Benchmark / perf-regression | `criterion` | Statistical micro-benchmarks with regression detection across runs. Keep in `benches/`, not in the unit suite (don't gate PRs on noisy bench numbers — track trend). |
| Fuzzing | `cargo-fuzz` (libFuzzer) | Parsers, decoders, untrusted-input boundaries. **Requires nightly, Unix-only** (no Windows). Seed a corpus; distinct from proptest — fuzzing is coverage-guided and unbounded. |
| UB in `unsafe` | `cargo +nightly miri test` | Any crate with `unsafe`, raw pointers, or FFI. Catches use-after-free, OOB, and invalid-value UB the normal test run cannot. Gate critical `unsafe` modules in a nightly CI job. |
| Concurrency permutations | `loom` | Lock-free / atomics / hand-rolled synchronization. Exhaustively explores interleavings under `#[cfg(loom)]` — `tokio::test` alone cannot find these races. |

```rust
// proptest: invariant over a generated domain
proptest! {
    #[test]
    fn roundtrip_encode_decode(s in ".*") {
        prop_assert_eq!(decode(&encode(&s)), s);
    }
}

// insta: snapshot a complex value (review with `cargo insta review`)
insta::assert_yaml_snapshot!(parse_config(input)?);

// async: tokio::test with explicit flavor + timeout to surface hangs
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn fetches_within_budget() {
    let r = tokio::time::timeout(Duration::from_secs(2), fetch(url)).await;
    assert!(r.is_ok(), "fetch exceeded budget (possible deadlock)");
}
```

Coverage commands — **prefer `cargo-llvm-cov`** (LLVM source-based, the accurate default); `tarpaulin` is faster but ptrace-based and less precise on branch/`async` coverage. Note `llvm-cov` has known limitations on Windows GNU/MSVC targets.

```bash
cargo llvm-cov --html --output-dir coverage/   # accurate, source-based (default choice)
cargo llvm-cov --fail-under-lines 80           # CI gate
cargo tarpaulin --out html --output-dir coverage/  # faster, lower precision — Linux-first
```

## Java

### Defaults

- Use JUnit 5.12+ or JUnit 6 (GA Sep 2025; requires Java 17+) with `@Nested` for scenario grouping. JUnit 6 adds `@ParameterizedClass`, Kotlin `suspend fun` test support, and unified versioning. See [junit.org/junit5/docs/current/user-guide/](https://junit.org/junit5/docs/current/user-guide/) and [docs.junit.org/6.0.3/release-notes.html](https://docs.junit.org/6.0.3/release-notes.html).
- Use parameterized tests for boundary matrices.
- Use Mockito only at true collaboration boundaries.

```java
@ParameterizedTest
@CsvSource({
  "'', true",
  "'  ', true",
  "hello, false"
})
void isBlankCases(String input, boolean expected) {
  assertEquals(expected, StringUtils.isBlank(input));
}
```

JaCoCo threshold example:

```xml
<rule>
  <element>BUNDLE</element>
  <limits>
    <limit>
      <counter>LINE</counter>
      <value>COVEREDRATIO</value>
      <minimum>0.80</minimum>
    </limit>
  </limits>
</rule>
```

## Cross-Language Rules

| Concern | Preferred Pattern |
|---------|-------------------|
| Setup sprawl | Extract factories or fixtures, not opaque mega-helpers |
| Async | Use framework-native async support, not sleeps |
| External calls | Mock/stub by boundary |
| Coverage | Enforce a minimum threshold in CI and inspect diff coverage separately |
| Readability | Prefer explicit behavior names over numbered tests |

## Quick Reference

| Language | Best First Move |
|----------|-----------------|
| Python | Parametrize edge cases and add fixture cleanup |
| Go | Table-driven test plus `httptest` or gomock |
| Rust | In-module unit test or `test_case` matrix |
| Java | JUnit 5 parameterized test plus JaCoCo gate |
