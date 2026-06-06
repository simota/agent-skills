# Flaky Test Guide

Purpose: Diagnose, stabilize, and monitor nondeterministic tests. Read this when a test passes sometimes and fails sometimes, especially in CI.

Contents:

- common causes and fixes
- retry and quarantine rules
- statistical detection
- CI-environment mitigation

## Common Causes And Fixes

| Cause | Symptom | Preferred Fix |
|------|---------|----------------|
| Race condition | Passes locally, fails in CI | Explicit async synchronization, proper await points |
| Timing dependency | Intermittent timeout | Fake timers, deterministic clocks |
| Order dependency | Fails when isolated or shuffled | Reset state in `beforeEach` / `afterEach` |
| Shared state | Only fails after other suites | Isolate data and global state |
| Real network | Slow or inconsistent failures | MSW or boundary mocks |
| Date / locale / timezone | CI-only formatting or calendar failures | Fix `TZ`, locale, and mocked time |
| Viewport / environment | Different runners, different result | Explicit config in test setup |

## First-Line Fixes

### Replace Sleeps

```typescript
// Bad
await new Promise((r) => setTimeout(r, 500));

// Good
await waitFor(() => {
  expect(screen.getByText('Success')).toBeInTheDocument();
});
```

### Fake Timers

```typescript
vi.useFakeTimers();
fireEvent.change(input, { target: { value: 'test' } });
await vi.advanceTimersByTimeAsync(500);
expect(mockSearch).toHaveBeenCalledWith('test');
vi.useRealTimers();
```

### Isolation

```typescript
beforeEach(() => {
  mockDb = new MockDatabase();
  service = new UserService(mockDb);
});

afterEach(() => {
  mockDb.reset();
  vi.clearAllMocks();
});
```

## Retry Strategy

Retries are for diagnosis and temporary containment, not the final fix.

### CI Defaults

| Tool | Suggested Setting |
|------|-------------------|
| GitHub Action wrapper | `max_attempts: 3` |
| Vitest | `retry: process.env.CI ? 2 : 0` |
| Jest | `retryTimes: process.env.CI ? 2 : 0` |
| pytest | `--reruns 3 --reruns-delay 2` |

```yaml
- name: Run tests with retry
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 10
    max_attempts: 3
    retry_on: error
    command: npx vitest run --reporter=junit --outputFile=test-results.xml
```

## Quarantine Rules

Only quarantine when the team cannot fix immediately and there is a linked follow-up.

```typescript
test.skip('flaky: payment webhook processing', () => {
  // TODO(radar): Fix flaky test - race condition in webhook handler
  // Ticket: PROJ-1234
});
```

Never skip silently.

## Prevention Checklist

- no real timers when fake timers are possible
- no real network calls in non-E2E tests
- no shared mutable state across tests
- no time, locale, or timezone assumptions
- no hidden dependency on run order
- no arbitrary delay in place of a condition
- test passes in isolation and across repeated runs

## Statistical Detection

### Repeated Execution

```bash
npx vitest run --repeat=10
pytest --count=10
go test -count=10 ./...
cargo nextest run --retries 0 -j 1 --run-ignored=all
```

### Health Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Flaky Rate | `< 1%` | `1-5%` | `> 5%` |
| MTBF | `> 50 runs` | `10-50` | `< 10` |
| Flaky Clusters | `0` | `1-2` | `> 2` |

## CI Environment Differences

| Factor | Local | CI Risk | Mitigation |
|--------|-------|---------|------------|
| CPU / memory | Often larger locally | Parallel timing changes | Reduce worker count or raise only justified timeouts |
| Timezone | Local TZ | Date drift | Force `TZ=UTC` |
| Locale | User locale | Formatting drift | Force locale in config |
| Network | Lower latency | Timeout drift | Mock external calls |
| Parallelism | Often less aggressive | Shared-state failures | Isolate test data and globals |

### Environment Hardening

```typescript
const TIMEOUT_MULTIPLIER = process.env.CI ? 3 : 1;

export default defineConfig({
  test: {
    env: { TZ: 'UTC' },
    testTimeout: 10000 * TIMEOUT_MULTIPLIER,
    hookTimeout: 30000 * TIMEOUT_MULTIPLIER,
  },
});
```

## Escalation Rules

- If a suite is flaky and root cause is still unknown after repeated runs, collect logs and move to `FLAKY` mode.
- If retries hide a real functional failure, remove retries and investigate immediately.
- If the flaky rate exceeds `5%`, treat it as a release-risk issue, not a local annoyance.

## 2026 Cost Anchor: Why Flakiness Is a P1, Not Toil

Recent 2026 industry surveys put the cost of a flaky-test culture at **`~6–8` engineer-hours per developer per week** in lost productivity (rerun cycles, lost trust in CI, time wasted re-investigating already-known noise). That dominates the cost of most "quality" line items — treat any flaky-rate over the warning threshold above as a release-risk discussion, not a maintenance task.

## Quarantine-First Policy (2026 default)

Blind retries hide signal and let real regressions slip through alongside genuine flakes. The 2026 preferred posture is **quarantine first, then fix**:

1. **Detect** with rerun statistics (`vitest run --repeat`, `pytest --count`, `cargo nextest --retries 0 -j 1`).
2. **Quarantine** with an explicit `test.skip` linked to a ticket — never silently `xfail`.
3. **Run quarantined tests in a separate CI lane** so they cannot block PRs but also cannot be forgotten — fail the build when the quarantine queue exceeds the policy threshold (default: `1%` of total tests).
4. **Fix at root** with the table at the top of this file; do not rely on `retry: 2` as the steady state.

This sequence is now built into many CI platforms (CircleCI Test Insights, BuildPulse, Datadog CI Visibility, GitHub Actions test-reporter integrations) — pick one and wire the quarantine queue into the dashboard rather than carrying it in code comments.

## AI Codegen Failure Mode: Tests That Cannot Detect Regressions

When the underlying test was AI-generated (Claude Code / Cursor / Copilot agents), the most common reason for "passes locally, fails in CI" is *not* a race condition — it is that the assertion only checks call-shape, not behavior, and CI exposes a difference the test was never going to detect. Before running the flaky playbook on an AI-generated test:

- Verify the test fails when the relevant production code is mutated (`mutation-testing.md`).
- Verify the test asserts on **business outcome**, not on mock-call sequence or string contents of a synthesised log line.
- If neither passes, the test is not flaky — it is structurally insufficient; rewrite rather than stabilise.
