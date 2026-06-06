# Performance Investigation Reference

Purpose: Profiler-driven RCA for latency, throughput, and CPU-hotspot bugs. Produces a localized hot-path, root-cause category, and fix brief for Bolt.

## Contents

- When to use `perf`
- Signal triage
- Profiling strategy by stack
- Root-cause categories
- Command recipes
- Output template
- Handoff criteria

## When to Use

- p95/p99 latency regression
- throughput ceiling lower than expected
- CPU saturation without business-volume increase
- timeout incidents traced to specific endpoint or job
- user-reported "slow" with measurable baseline

**Skip** if: no profiler access → recommend Beacon instrument first.

## Signal Triage

| Signal | First action | Expected artifact |
|--------|--------------|-------------------|
| latency regression | bisect via `trail` then profile old vs new | flamegraph diff |
| steady-state slow | capture production profile (60s minimum) | flamegraph + top-N hot functions |
| spike / burst | capture sampling during event | timeline trace |
| cold-start slow | separate cold vs warm profile | two flamegraphs |
| CI benchmark regression | run benchmark under profiler locally | call-count + cumulative time |

## Profiling Strategy by Stack

| Stack | Tool | Invocation | Output |
|-------|------|------------|--------|
| Node.js | `0x`, `clinic flame`, `--prof` | `clinic flame -- node app.js` | flamegraph HTML |
| Python | `py-spy`, `scalene`, `cProfile` | `py-spy record -o out.svg --pid <pid>` | flamegraph SVG |
| Go | `pprof` | `go tool pprof -http=: profile.pb` | interactive web |
| Java/JVM | `async-profiler`, JFR | `./profiler.sh -d 30 -f out.html <pid>` | flamegraph HTML |
| Rust | `cargo flamegraph`, `perf` | `cargo flamegraph --bin app` | flamegraph SVG |
| Ruby | `stackprof`, `rbspy` | `rbspy record --pid <pid>` | flamegraph |
| Browser | DevTools Performance tab | Record → Analyze | main-thread trace |
| PostgreSQL | `EXPLAIN ANALYZE`, `pg_stat_statements` | handoff to Tuner | query plan |

Prefer **sampling** profilers in production (minimal overhead); **instrumentation** profilers for CI/bench.

## Root-Cause Categories

Classify the dominant hot path into one category:

| Category | Signature | Typical fix (for Bolt) |
|----------|-----------|------------------------|
| **N+1 query** | many short DB calls per request | eager load / batch / dataloader |
| **Algorithmic complexity** | single function dominates, O(n²) visible | algorithm swap, memoization |
| **Cold cache / no cache** | repeated identical expensive calls | add cache layer (with invalidation design) |
| **Serialization** | JSON/protobuf encode/decode in hot path | streaming, binary format, schema trim |
| **GC / allocation pressure** | GC time > 10% in profile | object pooling, reduce transient allocations |
| **I/O blocking** | sync I/O in request path | async / parallel I/O |
| **Lock contention** | threads waiting on mutex | finer-grained locks, lock-free, shard |
| **Over-fetching** | unused data loaded | column projection, field masks |
| **Missing index** | full table scan in plan | handoff to Tuner for index design |
| **Framework overhead** | middleware/router dominates | reduce chain, precompile routes |

## Command Recipes

```bash
# Node: capture 30s flame
clinic flame --on-port 'autocannon -d 30 http://localhost:3000/api' -- node app.js

# Python: live attach
py-spy top --pid $(pgrep -f myapp)
py-spy record -o flame.svg --pid $(pgrep -f myapp) --duration 60

# Go: 30s CPU profile
curl -o cpu.pb http://localhost:6060/debug/pprof/profile?seconds=30
go tool pprof -http=: cpu.pb

# Async-profiler (Java)
./async-profiler/profiler.sh -d 30 -f flame.html $(pgrep -f myapp)

# compare before/after (bisect-driven)
git checkout $OLD_SHA && <run profiler> > before.svg
git checkout $NEW_SHA && <run profiler> > after.svg
```

## Output Template

```markdown
## Scout Performance Investigation

**Symptom**: `/api/search` p95 rose 180ms → 820ms over 2 weeks
**Confidence**: 0.87 (HIGH)
**Baseline**: `v2.14.0` (180ms) — current `v2.16.3` (820ms)

### Profile Summary

- Tool: `py-spy record -d 60 --pid 12345`
- Dominant function: `search_service.py:normalize_query` — 62% of samples
- Hot path: `handler → normalize_query → regex.compile (inside loop)`

### Root Cause

**Category**: Algorithmic complexity + missing cache
**Evidence**:
1. `regex.compile` called per request, pattern is static (flamegraph frame count = N requests × 12 patterns)
2. commit `a1b2c3d` (v2.15.0) moved compile inside the request handler
3. local reproduction: 4.2ms → 180μs after hoisting compile out of loop

### Fix Brief (for Bolt)

- Hoist 12 static regex compiles to module level
- Add micro-benchmark asserting `< 5ms` per normalize_query call
- Consider `re2` if pattern set grows

### Impact

- p95: 820ms → 195ms (96% reduction, estimated)
- CPU: -35% steady-state
- No behavior change (pure perf fix)

### Handoff

→ **Bolt**: implement hoist + benchmark
→ **Radar**: add regression benchmark to CI (threshold 10ms)
```

## Handoff Criteria

| Condition | Target | Handoff |
|-----------|--------|---------|
| Clear fix category | Bolt | `SCOUT_TO_BUILDER_HANDOFF` with category + brief |
| Missing index / query plan issue | Tuner | query plan + EXPLAIN output |
| Concurrency / lock contention | Specter | thread dump + lock trace |
| Framework choice questionable | Atlas | architectural review |
| Unclear after profiling | `consensus` Recipe | multi-engine hypothesis |

## Anti-Patterns

- Optimizing without profiling ("I think it's slow here")
- Profiling dev-mode builds (include debug overhead)
- Single-run profiles (variance can mislead; capture 3+ and compare)
- Ignoring GC / allocator (common hidden hot path)
- Fixing the second-largest frame (always attack the dominant one first)
