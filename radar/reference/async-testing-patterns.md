# Async Testing Patterns

Purpose: Use this when the target code depends on async scheduling, concurrency, streams, channels, or timeouts.

Contents:

- JS / TS async rules
- Python async rules
- Go concurrency rules
- Rust async rules
- Timeout strategy
- Race detection

## TypeScript / JavaScript

Rules:

- Prefer `async/await` plus explicit `await`.
- Use `findBy*` or `waitFor` for eventual UI states.
- Use fake timers for debounce, retries, and scheduled behavior.
- Use `Promise.allSettled` tests when partial success matters.

## Python

Rules:

- Use `pytest.mark.asyncio` for coroutine tests.
- Use `httpx.AsyncClient` or framework-native async clients for HTTP boundaries.
- Apply per-test timeout markers to slow integration paths.

## Go

Rules:

- Use `t.Parallel()` only when shared state is fully isolated.
- Prefer channels, contexts, and `WaitGroup` over sleeps.
- Always run `go test -race` in CI for concurrent code.

Must-keep commands:

```bash
go test -race ./...
go test -race -coverprofile=coverage.out ./...
go test -timeout 60s ./...
```

## Rust

Rules:

- Use `#[tokio::test]` for async code.
- Use `flavor = "multi_thread"` only when concurrency itself is under test.
- Use `tokio::time::timeout` for timeout paths and channel-based assertions for ordering.

## Timeout Strategy

| Test type | Default | Max |
|-----------|---------|-----|
| Unit | `5s` | `10s` |
| Integration | `30s` | `60s` |
| Contract | `15s` | `30s` |
| E2E | `60s` | `120s` |
| Performance | `120s` | `300s` |

Framework notes:

- Vitest: `testTimeout`, `hookTimeout`, `teardownTimeout`
- pytest: `timeout = 30`, override per test when needed
- Go: CLI `-timeout`
- Rust nextest: `slow-timeout`

## Race Condition Detection & Prevention

### Common Symptoms

| Symptom | Likely cause | Detection |
|---------|--------------|-----------|
| Passes locally, fails in CI | Timing assumptions | `-race`, `--repeat`, `-count=10` |
| Intermittent assertions | Shared mutable state | Per-test isolation |
| Deadlock | Missing timeout or signal | Add context or timeout |
| Wrong event order | Assumed scheduling | Synchronization primitive |

### Prevention Rules

- Replace sleeps with synchronization.
- Freeze or fake time where possible.
- Keep state local to each test.
- Repeat async fixes `10+` times when validating stability.

## Quick Reference

| Language | Async test | Race detection | Timeout control |
|----------|------------|----------------|-----------------|
| TS / JS | `async/await`, `waitFor` | repeat runs | `testTimeout` |
| Python | `@pytest.mark.asyncio` | repeat runs | `@pytest.mark.timeout` |
| Go | goroutines + channels | `go test -race` | `go test -timeout` |
| Rust | `#[tokio::test]` | repeat plus channel assertions | `tokio::time::timeout` |
