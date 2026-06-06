# Flamegraph Regression Reference

Purpose: CPU/memory hotspot regression diagnosis using Brendan Gregg's flamegraph technique. Captures stack samples at a known-good and known-bad commit, generates a differential flamegraph (red = hotter, blue = cooler), then narrows the offending commit by combining with `bisect`. Surfaces *where* time is being spent, while bisect surfaces *when* it started being spent there.

## Scope Boundary

- **trail `flame`**: flamegraph-driven regression localization. Produces hotspot diff + suspect commit set, hands the offending function to bisect for commit pinpointing.
- **trail `regression` / `bisect` (elsewhere)**: assume the regression is binary (test passes / fails). `flame` adds quantitative hotspot evidence when the symptom is "slower" not "broken".
- **trail `blame` / `history` (elsewhere)**: post-flame archaeology — once the offending function is identified, `blame` answers *who/when/why*.
- **Scout (elsewhere)**: current-state RCA without git-history axis. Use Scout when the regression is unrelated to a recent commit.
- **Bolt (elsewhere)**: forward optimization. `flame` localizes a regression; Bolt optimizes the result. Do not use `flame` to greenfield-optimize hotspots that were always slow.
- **Triage (elsewhere)**: incident response. `flame` is post-incident root cause; Triage is during-incident containment.
- **Builder (elsewhere)**: implements the fix. `flame` outputs the suspect commit + hotspot; Builder reverts or patches.

## Workflow

```
SCOPE    →  define regression metric (p50/p99/RSS), good rev, bad rev, workload
         →  pick profiler: perf (Linux native), async-profiler (JVM), pprof (Go),
            py-spy (Python), Instruments/dtrace (macOS)

CAPTURE  →  record N samples at good rev under controlled workload
         →  record N samples at bad rev under identical workload
         →  fold stacks → collapsed format (one stack per line, count suffix)

DIFF     →  difffolded.pl good.folded bad.folded > diff.folded
         →  flamegraph.pl --negate diff.folded > diff.svg
         →  identify red (hotter) frames; ignore noise < 1% delta

NARROW   →  hand offending frame/function to `bisect` with -L:func:file as the
            test trigger; bisect script measures the function's sample share
         →  use custom terms: `git bisect terms --term-old fast --term-new slow`

REPORT   →  hotspot diff (top 5 hotter frames) + suspect commit + confidence
         →  hand off to Bolt (optimize) or Builder (revert)
```

## Tool Selection

| Profiler | Runtime | Sampling | Strength | Caveat |
|----------|---------|----------|----------|--------|
| `perf record -F 99 -g` | Linux native (C/C++/Rust) | 99 Hz frame pointer | Kernel + user combined | Needs `--call-graph dwarf` for inlined frames |
| async-profiler | JVM (Java/Kotlin/Scala) | AsyncGetCallTrace | No safepoint bias | Needs `-XX:+UnlockDiagnosticVMOptions -XX:+DebugNonSafepoints` |
| pprof | Go | Built-in `runtime/pprof` | Native, low overhead | Goroutine stacks need `-blockprofile` for off-CPU |
| py-spy | Python (CPython) | External, no GIL impact | Production-safe sampling | Native extensions show as `<native>` |
| rbspy | Ruby (CRuby) | External | Production-safe | Older Ruby versions need build flags |
| dotnet-trace | .NET | EventPipe | Cross-platform | Needs `--format speedscope` for flamegraphs |
| Instruments | macOS native | Time Profiler | Symbol resolution | Export to `.trace` then convert |

## Differential Flamegraph Reading

| Color | Meaning | Action |
|-------|---------|--------|
| Deep red | Sample share grew significantly (>5% absolute) | Primary suspect — bisect this frame |
| Pink | Modest growth (1-5%) | Secondary suspect — confirm before bisecting |
| White | No change | Ignore |
| Light blue | Modest decrease | Was optimized; benign |
| Deep blue | Large decrease | Possible mismeasurement — verify workload parity |

## Hotspot Confirmation Thresholds

| Metric | Tolerance | Confidence |
|--------|-----------|------------|
| Frame sample share delta | ≥ 5% absolute | High |
| Frame sample share delta | 2-5% | Medium — repeat capture |
| Frame sample share delta | < 2% | Noise — ignore |
| Workload variance (CV) | < 5% | Capture is comparable |
| Workload variance (CV) | ≥ 10% | Re-capture under tighter control |
| Sample count | ≥ 10,000 per side | Statistically meaningful |

## Bisect Integration

For perf regressions, write a `bisect run` script that:
1. Builds the target.
2. Runs the workload under the profiler for a fixed wall-clock window.
3. Folds the stacks and computes the share of the offending frame.
4. Exits 0 (`fast`) if share < threshold, 1 (`slow`) if share ≥ threshold, 125 if the build/profile fails.

Use `git bisect terms --term-old fast --term-new slow` so the language matches the metric, not "good/bad".

## Memory Flamegraph Variant

Same workflow, different sampler:
- `perf record -e page-faults` for RSS regressions on Linux.
- `heaptrack` for C/C++ allocation flamegraphs.
- async-profiler `-e alloc` for JVM allocation hotspots.
- `tracemalloc` + `flameprof` for Python allocation profiles.
Treat allocation-site frames the same as CPU frames in the diff.

## Anti-Patterns

- Comparing flamegraphs from different workloads — even small input differences invalidate the diff. Pin workload, dataset, and warmup.
- Profiling without warmup — JIT-heavy runtimes (JVM, V8) show false hotspots in cold runs. Discard the first 10-20% of samples.
- Frame pointer omission — `perf` without `--call-graph dwarf` (or compiled without `-fno-omit-frame-pointer`) produces broken stacks; the diff becomes meaningless.
- Treating a 1% frame delta as a regression — sampling noise dominates below ~2% absolute. Set thresholds before reading the diff.
- Skipping symbol resolution — flamegraphs full of `0xdeadbeef` or `[unknown]` cannot be acted on. Verify debug symbols at both revisions before capture.
- Bisecting on absolute wall-clock instead of frame share — wall-clock includes cold cache, GC, and noise. Frame-share-based bisect is more stable.
- Ignoring off-CPU time — many "regressions" are lock contention or I/O wait, invisible in CPU flamegraphs. Add an off-CPU flamegraph (`-e sched:sched_switch`) when CPU diff looks flat but latency rose.
- Using `good`/`bad` terms for performance bisects — `fast`/`slow` (or `old`/`new`) keeps the team from arguing about whether slow code is "bad enough". Always set custom terms.

## Handoff

- **To `bisect`**: offending frame + threshold script → narrows to single commit.
- **To Bolt**: confirmed hotspot frame + diff SVG + suspect commit → forward optimization. Bolt owns the rewrite.
- **To Builder**: suspect commit SHA + recommended action (revert vs. patch) → implementation.
- **To Specter**: if the diff implicates lock/contention frames or async/await stacks → escalate via TRAIL_TO_SPECTER_HANDOFF (`_common/INVESTIGATION_ESCALATION.md`).
- **To Radar**: if no perf regression test existed → request benchmark coverage so this regression class is caught next time.
- **To Scout**: if the diff is flat but the symptom persists → Scout investigates non-history-bound causes (config drift, env var, data shape).
