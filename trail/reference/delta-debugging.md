# Delta Debugging Reference

Purpose: Automated minimization of failure-inducing inputs via Zeller & Hildebrandt's `ddmin` algorithm. Where `git bisect` minimizes the *commit set* that introduces failure, delta debugging minimizes the *input/state set* that triggers it. Combine the two to attack flaky tests, large failing test cases, and config-driven regressions where the offending change is too coarse to revert.

## Scope Boundary

- **trail `delta`**: input/state minimization via ddmin. Produces 1-minimal failing input + reproduction script.
- **trail `regression` / `bisect` (elsewhere)**: minimize the *commit* axis. `delta` minimizes the *input* axis. Often run sequentially: bisect to find the commit, ddmin to find the smallest input that exposes the bug introduced by that commit.
- **trail `flame` (elsewhere)**: localizes performance regressions; `delta` localizes correctness/flakiness regressions.
- **Scout (elsewhere)**: current-state RCA on a known reproducer. `delta` runs *before* Scout to obtain a small reproducer.
- **Radar (elsewhere)**: writes new tests including the minimized case; `delta` produces the input, Radar formalizes it.
- **Builder (elsewhere)**: implements the fix using the minimized reproducer.
- **Triage (elsewhere)**: incident response; `delta` is for post-incident or pre-fix minimization, not live mitigation.

## Workflow

```
SCOPE    →  define oracle: a deterministic test(input) → {PASS, FAIL, UNRESOLVED}
         →  identify granularity: characters, lines, AST nodes, JSON keys, events
         →  set time budget (ddmin is O(n²) worst case, ~O(n log n) typical)

REDUCE   →  partition input into n chunks (start n=2)
         →  for each chunk: test(input \ chunk)
            ├── FAIL → recurse on input \ chunk (n stays the same)
            ├── PASS or UNRESOLVED → try complement
            └── all chunks tried → increase granularity (n = 2n), recurse
         →  terminate when n > |input| (1-minimal)

VERIFY   →  the minimized input must still FAIL deterministically
         →  re-run K times (K=10 for flaky-test minimization) to confirm

REPORT   →  minimized input + reduction ratio + oracle script + reproduction steps
         →  hand off to Builder (fix) or Radar (regression test)
```

## ddmin Pseudocode

```
ddmin(input, n):
  while |input| >= 2:
    chunks = split(input, n)
    # Phase 1: try removing each chunk
    for chunk in chunks:
      reduced = input \ chunk
      if test(reduced) == FAIL:
        input = reduced
        n = max(n - 1, 2)
        goto while
    # Phase 2: try removing complement of each chunk
    for chunk in chunks:
      reduced = chunk
      if test(reduced) == FAIL:
        input = reduced
        n = 2
        goto while
    # No progress at this granularity — increase
    if n >= |input|: break
    n = min(2 * n, |input|)
  return input  # 1-minimal
```

Three outcomes per `test()` call: PASS (reduction failed), FAIL (reduction succeeded — recurse), UNRESOLVED (test inconclusive — treat as PASS to be safe).

## Application Contexts

| Input Type | Granularity | Oracle | Notes |
|------------|-------------|--------|-------|
| Failing test case (10k LOC) | AST nodes / statements | Test runner exit code | Use C-Reduce for C/C++, creduce-style for others |
| Large JSON/YAML config | Top-level keys → leaf values | App startup + smoke test | Preserve required schema fields as guards |
| Event sequence (replay log) | Individual events | Replay engine | Order matters — ddmin removes, doesn't reorder |
| Network trace | Individual packets / requests | Reproduction harness | Pair with `tcpreplay` or `mitmproxy` |
| Flaky test source | Lines / setup steps | Run test 10×; FAIL if any flake | Increases oracle latency 10× — budget accordingly |
| Compiler crash input | Program tokens / functions | Compiler exit code 139 | Classic ddmin use case |

## `git bisect run` Integration

Bisect and ddmin compose:

1. Run `git bisect run` to find the breaking commit C.
2. Check out C. The full failing input may be huge.
3. Run `ddmin` against the same oracle to minimize the input.
4. Hand off `(C, minimized_input)` — a precise, small reproducer.

For flaky regressions, embed ddmin *inside* the bisect oracle: the bisect script uses a minimized input that's known to expose the flake quickly, reducing per-iteration runtime.

## Flaky Test Minimization

| Setting | Value | Rationale |
|---------|-------|-----------|
| Oracle reruns | 10× | Catch flake rate ≥ 30% with high confidence |
| FAIL threshold | ≥ 1 failure in 10 | Conservative — preserves any flake signal |
| Budget multiplier | 5-10× normal ddmin | Each oracle call is K× slower |
| Granularity start | Setup blocks, fixtures, teardown order | Flakes often live in shared state |
| Stop criterion | 1-minimal OR budget exhausted | Partial reduction still useful |

## When to Use vs. Traditional Bisect

| Symptom | Use bisect | Use delta | Use both |
|---------|-----------|-----------|----------|
| Test passed yesterday, fails today | ✓ | | |
| Test fails on 50KB input, passes on small inputs | | ✓ | |
| Regression bisects to a commit but that commit is huge / unrevertable | | | ✓ |
| Flaky test introduced "somewhere this sprint" | | | ✓ |
| Config file change broke something — but config has 800 keys | | ✓ | |
| Property-based test found a 200-step counterexample | | ✓ | |

Property-based testing tools (Hypothesis, fast-check, QuickCheck) ship their own shrinkers — those are domain-aware ddmin variants. Use built-in shrinking when the test framework provides it; reach for ddmin when the input crosses tool boundaries (e.g., generated input fed into a separate process).

## Anti-Patterns

- Non-deterministic oracle without rerun guard — ddmin will produce a "minimized" input that doesn't actually reproduce. Always verify with K reruns at the end.
- Granularity too fine from the start — character-level on a 100KB file makes ddmin O(n²) on 100K chars. Start coarse (lines, AST nodes), refine only when stuck.
- Ignoring UNRESOLVED — treating "test crashed before reaching assertion" as FAIL leads ddmin down a wrong path. Map ambiguous outcomes to UNRESOLVED → PASS.
- Minimizing across syntactically invalid states — removing a `{` from JSON makes the test fail for the wrong reason. Use structure-aware reducers (C-Reduce, picireny, hdd) for grammar-bound inputs.
- Confusing 1-minimal with global minimum — ddmin finds *a* 1-minimal, not *the* smallest. Two ddmin runs from different starting partitions can yield different minimums.
- Using ddmin where a property-based shrinker would do — Hypothesis/fast-check shrinkers are faster and structure-aware. Reach for raw ddmin only when no shrinker applies.
- No time budget — ddmin can spiral on adversarial inputs. Always cap wall-clock and ship the best partial result on timeout.
- Skipping the verify step — the minimized output must independently reproduce. Without final verification, you may report a coincidence.
- Discarding the oracle script — the script is part of the deliverable. Without it, the next engineer cannot rerun or extend the minimization.

## Handoff

- **To `bisect`**: minimized input as the bisect oracle's test fixture → faster per-iteration runs.
- **To Builder**: minimized reproducer + oracle script + suspect commit → fix implementation.
- **To Radar**: 1-minimal input → formalize as regression test (deterministic, fast, scoped).
- **To Scout**: minimized reproducer for current-state RCA when no breaking commit exists (`delta` only).
- **To Specter**: if minimization implicates timing/ordering (race-only-with-event-sequence-X) → escalate via TRAIL_TO_SPECTER_HANDOFF.
- **To Triage**: minimized input as the post-incident artifact for the postmortem.
