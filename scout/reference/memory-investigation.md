# Memory Investigation Reference

Purpose: Heap-snapshot-driven RCA for OOM, memory leaks, and GC pressure. Identifies retention path, leak class, and hands off a fix brief to Bolt or Specter.

## Contents

- When to use `memory`
- Leak vs bloat vs pressure
- Heap-capture strategy
- Retention-path analysis
- Command recipes
- Output template
- Handoff criteria

## When to Use

- OOM kills in production (`signal 9`, `CrashLoopBackOff`, `OOMKilled`)
- RSS/heap grows without bound (sawtooth → flat vs monotonic rise)
- GC time percentage climbing
- Latency correlated with GC pauses
- Long-running process memory bloat

**Skip** if: symptom is CPU, not memory → `perf` Recipe.

## Leak vs Bloat vs Pressure

Classify the symptom before profiling — different investigations.

| Class | Signal | Investigation |
|-------|--------|---------------|
| **Leak** | monotonic rise across GC cycles | heap diff across time |
| **Bloat** | steady high but stable | heap snapshot analysis (dominators) |
| **GC pressure** | allocation rate high, heap OK | allocation profile |
| **Fragmentation** | heap has room but allocator fails | allocator-specific tool (jemalloc stats, etc) |
| **Off-heap** | RSS high, heap flat | native allocations (DirectByteBuffer, mmap, FFI) |

## Heap-Capture Strategy

| Stack | Tool | Capture |
|-------|------|---------|
| Node.js | Chrome DevTools, `heapdump`, `--inspect` | `kill -USR2 <pid>` with heapdump, or DevTools → Memory → Heap snapshot |
| Python | `tracemalloc`, `memray`, `objgraph` | `memray run app.py` → `memray flamegraph out.bin` |
| Go | `pprof heap` | `go tool pprof http://.../debug/pprof/heap` |
| Java/JVM | `jmap`, `Eclipse MAT`, JFR | `jmap -dump:format=b,file=heap.hprof <pid>` |
| Ruby | `memory_profiler`, `derailed_benchmarks` | gem-based, per-request reports |
| Rust | `heaptrack`, `bytehound`, `dhat` | `heaptrack ./binary` |
| Browser | DevTools Memory tab | snapshot 1 → action → snapshot 2 → diff |
| Containers | `docker stats`, `kubectl top pod` | RSS trend |

Minimum capture cadence for leaks: **3 snapshots** spaced by meaningful workload (e.g., t=0, 10min, 30min after start). Diff reveals growing object classes.

## Retention-Path Analysis

For each suspicious object class:

1. Identify **dominator** — the object keeping it alive
2. Trace **retaining path** from GC root
3. Classify retention:
   - **Intentional cache** → check eviction policy
   - **Event listener not removed** → lifecycle bug
   - **Closure over large context** → capture scope bug
   - **Global registry growing** → missing cleanup
   - **Timer / interval not cleared** → teardown gap
   - **Module-level cache with no bound** → design flaw

### Common Leak Patterns

| Pattern | Detection | Fix |
|---------|-----------|-----|
| Event emitter listener accumulation | listener count > threshold | `removeListener` or AbortController |
| Closure capture of large parent | retained object is closure, parent should be GC'd | restructure to break reference |
| Unbounded cache (Map / Object) | size grows linearly with requests | LRU with max size or TTL |
| Detached DOM nodes | nodes in heap but not in document | null refs, remove listeners |
| Timer holding context | interval ID never cleared | `clearInterval` in teardown |
| Async task queue never drained | pending tasks grow | backpressure, bounded queue |
| Circular ref with non-GC | object graph with strong cycle | weak refs, break cycle |
| Native allocation leak | RSS grows, heap flat | audit FFI / Buffer / mmap |

## Command Recipes

```bash
# Node: heapdump + diff
npm i heapdump
# in code: require('heapdump') ; kill -USR2 <pid> writes heapdump-<ts>.heapsnapshot
# compare in Chrome DevTools Memory panel (Comparison view)

# Python: memray
pip install memray
memray run --live app.py          # live TUI
memray run -o profile.bin app.py
memray flamegraph profile.bin
memray tree profile.bin           # allocation tree
memray stats profile.bin          # top allocators

# Go: heap profile
curl -o heap.pb http://localhost:6060/debug/pprof/heap
go tool pprof -http=: heap.pb
# in pprof: top, list <func>, web

# Java: heap dump + MAT
jmap -dump:live,format=b,file=heap.hprof <pid>
# open in Eclipse MAT → Leak Suspects report

# RSS vs heap timeline
while true; do
  ps -o pid,rss,vsz -p <pid>
  echo "---"
  sleep 10
done
```

### Growth-rate sanity check

```
Leak rate (bytes/request) = (RSS_later - RSS_earlier) / requests_between
```

If constant across windows → deterministic leak. If only under specific path → scope the trigger.

## Output Template

```markdown
## Scout Memory Investigation

**Symptom**: pod `api-worker-*` OOMKilled every ~6h, 512MB limit
**Confidence**: 0.81 (HIGH)
**Class**: Leak (monotonic rise)

### Capture Summary

- Tool: `memray run --live worker.py`
- Snapshots at t=0, t=30m, t=2h
- Heap growth: 80MB → 180MB → 420MB
- Leak rate: ~2.8MB/min, correlates with `/ingest` RPS

### Retention Path

```
GC root → IngestService._cache (dict)
       → list of 42,318 WebhookPayload instances
       → each holds `raw_body: bytes` (~10KB)
```

### Root Cause

**Pattern**: Unbounded module-level cache
**Evidence**:
1. `ingest/service.py:_cache` is a `dict[str, WebhookPayload]`, added on every call, never deleted
2. No TTL, no max-size, no eviction
3. commit `e4f5g6h` (v3.2.0) introduced the cache "for dedup" but dedup key is per-request, so collisions are rare

### Fix Brief (for Bolt)

- Replace `_cache: dict` with `_cache: TTLCache(maxsize=1000, ttl=300)`
- Add metric: `cache_size_gauge`
- Add OOM canary: CI test loading 10,000 payloads and asserting heap < 100MB

### Handoff

→ **Bolt**: implement TTLCache swap + metrics
→ **Beacon**: add `memory_rss` SLO + alert at 80% of limit
→ **Radar**: add memory regression test harness
```

## Handoff Criteria

| Condition | Target | Reason |
|-----------|--------|--------|
| Clear retention path + fix | Bolt | `SCOUT_TO_BUILDER_HANDOFF` |
| Off-heap / native leak | Specter | resource management specialty |
| GC pressure from allocation rate | Bolt + Tuner | may combine with DB layer |
| Fragmentation / allocator issue | Specter | system-level diagnosis |
| Unable to reproduce locally | `prod` Recipe | use production traces |

## Anti-Patterns

- Looking at heap snapshot size alone (bloat ≠ leak)
- Single snapshot leak hunting (need diff across time)
- Ignoring RSS vs heap divergence (off-heap leaks hide)
- Optimizing smallest growing class (attack the dominator)
- Assuming GC will "eventually" clean (strong refs prevent it)
