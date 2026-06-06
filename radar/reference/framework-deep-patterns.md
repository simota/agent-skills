# Framework Deep Patterns

Purpose: Advanced framework-specific patterns that matter once the basic test structure is already sound. Read this only when the repository needs a framework-specific optimization or debugging feature.

Contents:

- Vitest and Jest deep patterns
- pytest plugin and fixture structure
- Go and Rust advanced patterns
- JUnit 5 extensions

## Vitest Deep

### Workspace Strategy

Use workspace projects when unit and integration tests need different environments or budgets.

```typescript
export default [
  {
    extends: './vitest.config.ts',
    test: { name: 'unit', include: ['src/**/*.test.ts'], environment: 'node' },
  },
  {
    extends: './vitest.config.ts',
    test: { name: 'integration', include: ['tests/integration/**/*.test.ts'] },
  },
];
```

Commands:

```bash
npx vitest --project=unit
npx vitest --project=integration
npx vitest --workspace
```

### Pool Selection

| Pool | Isolation | Speed | Use When |
|------|-----------|-------|----------|
| `threads` | Medium | Fast | Default |
| `forks` | High | Medium | Global state or native side effects |
| `vmThreads` | Low | Fastest | Pure unit suites only |

### Browser Mode

Use browser mode only when DOM or browser APIs are the real risk. Otherwise keep tests in node/jsdom for speed.

## Jest Deep

### Transformer Choice

| Transformer | Speed | Best Fit |
|------------|-------|----------|
| `@swc/jest` | Fast | TypeScript projects that only need transpilation |
| `esbuild-jest` | Fast | Simple JS/TS without decorator support |
| `babel-jest` | Medium | Existing Babel-heavy projects |
| `ts-jest` | Slow | Rare cases where transformer-level TS behavior matters |

### Debugging Open Handles

```bash
npx jest --detectOpenHandles --forceExit
npx jest --logHeapUsage
node --inspect-brk node_modules/.bin/jest --runInBand
```

## pytest Deep

### Useful Plugins

| Plugin | Purpose |
|--------|---------|
| `pytest-asyncio` | Async tests |
| `pytest-timeout` | Per-test timeouts |
| `pytest-xdist` | Parallel execution |
| `pytest-mock` | Better mocking |
| `pytest-factoryboy` | Factory-backed fixtures |
| `pytest-randomly` | Randomized order to expose hidden coupling |

### Fixture Layout

Keep `conftest.py` layered:

- root: global fixtures
- unit: lightweight fakes and mocks
- integration: containers, real clients, seeded data
- e2e: browser or external orchestration only if the repo already uses it

## Go Testing Deep

### High-Value Patterns

- mark helpers with `t.Helper()`
- use `t.Cleanup()` instead of ad-hoc teardown stacks
- combine subtests with `t.Run`
- use `t.Parallel()` only with proven state isolation

## Rust Testing Deep

### Tool Selection

| Need | Preferred Tool |
|------|----------------|
| Async runtime | `tokio::test` |
| Parameterized cases | `rstest` or `test-case` |
| Property-based testing | `proptest` |
| Faster CI runner | `cargo-nextest` |

Prefer deterministic examples over locale-specific literals unless the test is truly about encoding or locale.

## JUnit 5 Deep

Use these advanced features only when they increase clarity:

- `@Nested` for scenario grouping
- extensions for reusable setup or custom assertions
- Testcontainers integration when Java services need a real dependency

## Quick Reference

| Framework | Reach For This First |
|-----------|----------------------|
| Vitest | workspace split and pool selection |
| Jest | transformer and open-handle debugging |
| pytest | plugin choice and fixture layout |
| Go | `t.Helper`, `t.Cleanup`, subtests |
| Rust | `tokio::test`, `rstest`, nextest |
| JUnit 5 | `@Nested`, extensions, targeted Testcontainers |
