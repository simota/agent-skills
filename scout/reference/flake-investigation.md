# Flake Investigation Reference

Purpose: Triage intermittent / non-deterministic bugs and flaky tests. Measure reproducibility, classify the non-determinism source, and route to the right specialist (Specter for concurrency, Radar for test infra, Builder for code, Scaffold for env).

## Contents

- When to use `flake`
- Reproducibility score
- Non-determinism categories
- Evidence collection
- Command recipes
- Output template
- Handoff criteria

## When to Use

- CI test passes locally but fails in pipeline (or vice versa)
- Same test passes and fails on rerun without code change
- Bug only reproduces "sometimes"
- Works for some users/environments and not others
- Time-of-day or load-dependent failures

**Skip** if: fully deterministic once reproduction steps are known → `bug` Recipe.

## Reproducibility Score

Run the failing scenario **N times** (typically N = 20–50) and compute:

```
flip_rate = failures / total_runs
```

| Flip rate | Class | Next action |
|-----------|-------|-------------|
| 1.0 | deterministic | not flaky — use `bug` Recipe |
| 0.5–0.99 | high flake | fixable by investigation |
| 0.1–0.5 | medium flake | may need stress / soak tests |
| 0.01–0.1 | low flake | hard — consider quarantine + monitor |
| < 0.01 | rare | accept or quarantine; do not block CI |

Always record **which configuration** (commit, OS, concurrency level, seed, load).

## Non-Determinism Categories

| Category | Signal | Specialist |
|----------|--------|------------|
| **Timing / race** | passes in isolation, fails in parallel | **Specter** (handoff) |
| **Shared mutable state** | order of tests matters, one test pollutes another | Specter / Radar |
| **Time-of-day dependency** | `Date.now()`, midnight, DST, timezone | Tempo |
| **Clock / timer** | `setTimeout` tuning, polling intervals | Specter |
| **External dependency** | network / DNS / 3rd-party API | Scaffold (mocking) |
| **Resource exhaustion** | passes fresh, fails under load | Siege |
| **Randomness without seed** | `Math.random()` in test fixtures | Radar |
| **Floating-point** | epsilon comparisons | Radar |
| **Concurrency / async ordering** | promise/goroutine/thread order | Specter |
| **Filesystem / tempdir** | file collision between parallel tests | Radar |
| **Port / socket binding** | EADDRINUSE in parallel runs | Scaffold |
| **CI-only** | passes local, fails CI | environment drift — Scaffold |
| **Memory-pressure induced** | OOM or swap changes behavior | `memory` Recipe |
| **Flaky test code itself** | sleep-based waits, poll without retry | Radar |

## Evidence Collection

Collect in order:

1. **Reproduce rate** (N runs, confidence interval)
2. **Failure signature** — exact error, stack, logs, screenshots
3. **Environmental vars** that differ across runs (CPU count, OS, timezone, seed)
4. **Test isolation test** — run the single test alone 20× ; run with peers 20×
5. **Ordering test** — shuffle test order, check if failures correlate with specific predecessors
6. **Concurrency test** — vary parallel workers (1, 2, 4, 8) ; plot flip rate
7. **Timing test** — add artificial delays (10ms, 100ms, 1s) at suspect points
8. **Seed test** — fix any RNG seed ; confirm determinism returns

### Signature Fingerprint

For each failure, hash:
```
sha1(error_class + top_3_stack_frames + error_message_template)
```

Cluster failures by signature. A single flake may have 2–3 related signatures (same bug, different racing lines).

## Command Recipes

```bash
# Loop N times and record pass/fail
for i in $(seq 1 50); do
  <test command> > run_$i.log 2>&1 && echo "$i PASS" || echo "$i FAIL"
done | tee flake.log
echo "flip rate: $(grep -c FAIL flake.log) / 50"

# Run single test in isolation
go test -run TestSuspect ./... -count=50
pytest -k test_suspect --count=50
npm test -- --testNamePattern 'suspect' --runInBand

# Force parallelism to expose races
go test -race -p 16 ./...
pytest -n 16
npm test -- --maxWorkers=16

# Shuffle test order
go test -shuffle=on ./...
pytest -p no:randomly   # or reverse

# Fix RNG seed to confirm determinism
PYTHONHASHSEED=0 GODEBUG=randautoseed=0 <test>

# Capture system state on failure
<test> || {
  date; uptime; free -h; df -h
  ps auxf | head -50
  env | sort
}
```

### Load-correlated flake

```bash
# Vary CPU load and measure flip rate
for cpu_load in 0 25 50 75 95; do
  stress --cpu $(nproc) --cpu-load $cpu_load --timeout 60s &
  flip=$(run_test_loop 20)
  kill %1
  echo "load=$cpu_load flip=$flip"
done
```

## Output Template

```markdown
## Scout Flake Investigation

**Target**: `TestOrderProcessing_ConcurrentConfirm` (Go)
**Flip rate**: 0.34 (17/50) in `-p 16`, 0.00 (0/50) in `-p 1`
**Confidence**: 0.78 (HIGH — class identified)

### Reproducibility

| Config | Runs | Pass | Fail | Flip rate |
|--------|------|------|------|-----------|
| serial `-p 1` | 50 | 50 | 0 | 0.00 |
| parallel `-p 4` | 50 | 43 | 7 | 0.14 |
| parallel `-p 16` | 50 | 33 | 17 | 0.34 |
| `-race -p 16` | 20 | 8 | 12 | 0.60 + data race detected |

### Signature

- Error: `panic: concurrent map writes`
- Stack top: `order.Confirm → inventory.Reserve → inventory.cache.Set`
- Go race detector: data race on `inventory.cache` (unsynchronized map)

### Classification

**Category**: Concurrency / race — shared mutable state
**Evidence**:
1. Flip rate increases monotonically with parallelism
2. `-race` detector flags unsynchronized map access
3. Isolation (-p 1) is fully deterministic

### Root Cause Hypothesis

`inventory.cache` is a plain `map[string]Item` accessed by multiple goroutines without mutex. Added in commit `x7y8z9` (moved from sync.Map for "performance").

### Handoff

→ **Specter**: confirm race analysis, propose synchronization primitive (sync.Map vs RWMutex vs shard)
→ **Radar**: add `-race` to CI; flake-quarantine this test until fix lands
→ **Bolt**: implement fix per Specter's design
```

## Handoff Criteria

| Condition | Target | Reason |
|-----------|--------|--------|
| Data race / concurrency confirmed | **Specter** | concurrency specialty |
| Test-code flake (sleep waits, shared tempdir) | **Radar** | test-infra fix |
| Timezone / clock / cron | **Tempo** | time-aware design |
| CI-only (env drift) | **Scaffold** | env reproducibility |
| Load-correlated | **Siege** + Specter | stress validation |
| Can't classify after N=50 | `consensus` Recipe | multi-engine hypothesis |

## Quarantine Policy

If flip rate is 0.01–0.1 and no clear fix within investigation budget:

1. Tag test `@flaky` (not merged to main test suite)
2. Run in separate CI job (non-blocking)
3. Track in `.flaky-tests.md` with flip rate and last-seen date
4. Re-investigate after 30 days or when flip rate doubles

**Never** simply retry-until-pass without documentation — that hides the bug.

## Anti-Patterns

- "Just re-run it" — masks the underlying race
- Adding `sleep` to "fix" flakes — creates time-dependent tests
- Running N=3 and concluding (statistically meaningless)
- Only testing in isolation (misses parallelism bugs)
- Ignoring `-race` or equivalent detector output
- Fixing symptoms (add retry) instead of root cause (fix race)
