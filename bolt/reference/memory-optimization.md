# Memory Footprint Optimization Reference

Purpose: Reduce steady-state memory usage of an application — browser tab or Node.js process — without changing behavior. The subcommand profiles retained size, identifies the dominant retainers, removes them, and confirms the baseline holds after repeated activity.

## Scope Boundary

- **Bolt `memory`** (this Recipe): *measure and reduce* app-process memory footprint. Trim retained size, remove unintentionally-held references, pick `WeakMap`/`WeakRef` where identity caches would pin GC. Output is bytes saved and a stable baseline across N repetitions.
- **Specter**: *find the bug* — race conditions, deadlocks, resource leaks (unclosed file handles, unreleased DB connections, dangling timers). Specter produces reproduction steps and hands off to Builder for the fix.
- **Overlap — "resource leak"**: Specter finds the leak (bug: who leaks, when, why). Bolt `memory` trims the fat (design: what could be smaller even without bugs). If the heap grows unboundedly under a deterministic loop → Specter. If the heap is simply larger than necessary at steady state → Bolt `memory`.
- **Tuner**: DB-internal memory (PostgreSQL `shared_buffers`, `work_mem`, plan cache). Bolt `memory` is the app-process side of the client. Out of scope here.
- **Bolt `bundle`**: ship fewer JS bytes. Bundle size and heap size correlate but are not the same — a 50 kB library can easily retain 5 MB at runtime.
- **Bolt `cache`**: unbounded caches are both a memory *and* a cache-hygiene issue. Always cap with TTL or LRU size; then the remainder is `memory`.

Default: if the ticket says "leak" with reproduction steps → Specter. If it says "RSS is high" or "tab grows to 1 GB over a day" → `memory`.

## Workflow

```
PROFILE   →  frontend:  Chrome DevTools → Memory → Heap snapshot
             take 3 snapshots around a repeating action (search, route switch, modal open/close)
             filter "Objects allocated between snapshot 1 and 2" persisting to 3
          →  backend:   node --inspect + --heapsnapshot-signal=SIGUSR2
             capture before/during/after load; diff with heap-profiler
          →  baseline: RSS, JS heap used, detached DOM count, listener count

SELECT    →  pick ONE of: detached-DOM fix · listener cleanup · cache cap · WeakMap swap
          →  target: reduce retained size by ≥10% OR remove unbounded growth class
          →  ignore noise < 1 MB unless it grows per-operation

OPTIMIZE  →  the usual patterns:
             - remove closures over large scopes (React: stale state in effects)
             - cleanup in useEffect return / componentWillUnmount
             - AbortController for fetch / IntersectionObserver / ResizeObserver
             - switch identity-keyed Map → WeakMap
             - bound caches with TTL or LRU size
             - release big objects explicitly at end of scope (= null) in long-lived modules

VERIFY    →  re-run the same repetition; compare snapshots
          →  baseline check: after 10× the action, heap should return to ~start
          →  no detached DOM growth; listener count stable

PRESENT   →  Before / After: RSS, JS heap, retained-size top offenders
          →  leak-vs-fat classification — if bug, handoff to Specter
          →  baseline watch recommendation
```

## Heap Snapshot Diffing — Frontend

Chrome DevTools → Memory → "Heap snapshot":

1. Warm the page; force GC (trash-can icon).
2. Snapshot 1 (baseline).
3. Perform the action once. Force GC. Snapshot 2.
4. Repeat action once. Force GC. Snapshot 3.
5. In Snapshot 3, switch view to "Objects allocated between snapshots 1 and 2" — objects that survived both GCs indicate retention.
6. Sort by "Retained size". Inspect "Retainers" panel to trace why each object is held.

Classic retainers: `window` closure, React `useRef` that was never nulled, uncleaned `addEventListener`, long-lived array that keeps appending.

## Detached DOM Nodes

Search snapshot for "Detached HTMLDivElement" (or similar). Count should be ~0 after GC. Common causes:

- Component stored a DOM ref in module-level state and never cleared on unmount.
- Event handler outside the component closed over the DOM node.
- jQuery-era code: `$(node).data('handler', fn)` — retains both.

Fix: explicitly null refs on unmount; use `WeakRef` for debugging holds.

## Node.js Heap Profiling

```bash
# Snapshot on signal (no restart needed)
node --heapsnapshot-signal=SIGUSR2 app.js
kill -USR2 <pid>   # drops Heap.<timestamp>.heapsnapshot

# Continuous allocation sampling
clinic heapprofiler -- node app.js

# Rising-baseline detection: sample RSS every minute during sustained load
# expected pattern: rise → plateau → flat. Monotonic rise = leak.
```

Inspect in Chrome DevTools (drag `.heapsnapshot` into Memory panel). Same retained-size + retainer analysis applies.

## WeakMap / WeakRef Patterns

```ts
// BAD: Map keyed by object identity — blocks GC of the key object
const cache = new Map<User, Profile>();

// GOOD: WeakMap releases when User is unreferenced elsewhere
const cache = new WeakMap<User, Profile>();

// WeakRef for caches where the *value* should be reclaimable
const icons = new Map<string, WeakRef<HTMLImageElement>>();
const get = (k: string) => icons.get(k)?.deref();
```

Rules: `WeakMap` keys must be objects. `WeakRef` is a last resort — don't branch on `deref()` presence inside hot paths.

## Anti-Patterns

- Calling `global.gc()` in production Node to "fix" memory — masks the retention, doesn't remove it.
- Adding an LRU cache around an unbounded cache — still unbounded without a size cap.
- Using `WeakRef` for correctness (as opposed to memory hygiene) — reads may observe missing values non-deterministically.
- Treating "memory goes up" as a leak without GC-forced measurement — the heap naturally grows between GCs.
- Blaming a library before checking app-side listener cleanup.

## Handoff

- **→ Specter**: heap grows unboundedly under deterministic repetition, or suspected concurrency hold (unresolved promise, dangling timer, unclosed connection).
- **→ Builder**: Specter's reproduction + this profiling's pointer → Builder implements the fix.
- **→ Bolt `cache`**: uncapped cache is the root cause; needs TTL / LRU design.
- **→ Bolt `bundle`**: shipped library is disproportionately heavy at runtime — consider replacement.
- **→ Tuner**: retained size points at DB driver buffers — likely pool sizing, not app leak.
- **→ Beacon**: add RSS / heap-used SLI and a rising-baseline alert so regressions are caught early.
