# Performance Optimization Anti-Patterns

> Pitfalls of performance optimization, premature optimization, incorrect optimization ordering, and optimizing without measurement

## 1. 10 Major Optimization Anti-Patterns

| # | Anti-Pattern | Symptom | Impact | Countermeasure |
|---|-------------|------|------|------|
| **PO-01** | **Premature optimization** | Code becomes complex before the bottleneck is identified | Reduced readability, higher maintenance cost, no real benefit | Strictly follow measure → identify → optimize order |
| **PO-02** | **Optimizing without measurement** | Optimizing based on "this seems slow" without profiling | The actual bottleneck gets missed | Measure with Chrome DevTools / Lighthouse / clinic.js before starting |
| **PO-03** | **Over-focus on micro-optimization** | Chasing 1ms savings inside a loop while ignoring architectural issues | Larger problems like N+1 queries go unaddressed | Tackle the highest-impact issues first (DB > network > rendering > JS computation) |
| **PO-04** | **Excessive memoization** | Applying useMemo/useCallback/memo to everything | Code complexity increases; memoization cost > recomputation cost | Confirm impact via measurement. Trend toward less manual memoization in the React Compiler era |
| **PO-05** | **Optimizing the wrong layer** | Working hard on the frontend while the backend is the bottleneck | Time wasted on optimizations that show no effect | Profile the entire request lifecycle |
| **PO-06** | **Treating caching as a cure-all** | Trying to solve everything with caching | Consistency issues, memory pressure, hard-to-debug problems | Caching only masks symptoms — fix the root cause (e.g. slow queries) first |
| **PO-07** | **Benchmark/production environment mismatch** | Measuring only in dev, where conditions differ from production | No improvement — or a regression — in production | Combine RUM (Real User Monitoring) with Synthetic Monitoring |
| **PO-08** | **No regression testing** | Can't detect performance regressions after optimizing | New features silently undo the optimization | Performance Budget + CI/CD integration |
| **PO-09** | **Blind trust in libraries** | Adopting libraries claiming to be "lightweight" without verification | Bundle size actually increases, performance worsens | Pre-verify with bundlephobia + measure directly |
| **PO-10** | **Over-focus on a single metric** | Focusing only on LCP, or only on bundle size | Other metrics worsen (e.g. INP regresses, CLS increases) | Evaluate holistically across all 3 Core Web Vitals + business metrics |

---

## 2. The Correct Order of Optimization

```
Optimization in ROI order (for a typical web application):

  1. Database queries (biggest impact)
     - Resolving N+1: 100→1 queries = 40x faster
     - Adding an index: Seq Scan → Index Scan = 10-100x
     - Excluding unneeded columns: SELECT * → needed columns = 2-5x

  2. Network / API
     - Payload reduction: exclude unneeded data = latency improvement
     - Batch API: N requests → 1 request
     - Compression: gzip/brotli = 60-80% reduction in transfer size

  3. Caching strategy
     - HTTP cache: avoid re-requests
     - CDN: edge delivery = improves TTFB
     - Application cache: reduces DB load

  4. Frontend rendering
     - SSR/SSG: speeds up initial paint
     - Code splitting: reduces initial bundle
     - Virtualization: handles large lists

  5. JavaScript computation (smallest impact)
     - Array operation optimization: sorting 250 items < 2ms
     - Heavy computation → Web Worker
     - Debounce/throttle

Note: Starting from 5 is the classic case of PO-03;
      starting from 1 is what professional optimization looks like.
```

---

## 3. The Three-Layer Measurement Model

| Layer | Tools | Metrics | Timing |
|---|--------|---------|---------|
| **Development** | React DevTools · Chrome Performance · Lighthouse | Render time · Bundle size · LCP/INP/CLS | Per PR |
| **CI/CD** | Lighthouse CI · webpack-bundle-analyzer · autocannon | Budget overruns · regression detection · throughput | Per merge |
| **Production** | RUM (web-vitals) · Synthetic Monitoring · APM | p50/p75/p95 · error rate · business impact | Continuous |

```
Why you must never optimize without measuring:

  Human intuition is unreliable:
    - "This function seems slow" → measurement shows it's 2% of rendering
    - "Memoizing this will make it faster" → memoization overhead > recomputation cost
    - "The bundle is big" → actually 80% of it is images

  The correct approach:
    1. Identify the symptom ("page load takes 5 seconds")
    2. Profile to identify the cause ("API response 3s + rendering 1.5s")
    3. Address the largest factor first ("resolve API N+1 → 3s → 0.1s")
    4. Measure the impact ("5s → 2.1s = 58% improvement")
```

---

## 4. Optimization Decision Flowchart

```
When a performance problem is detected:

  1. Did you measure it? → No → measure first, then redo
                          → Yes ↓

  2. Where's the bottleneck?
     ├─ DB query → EXPLAIN ANALYZE → index / N+1 / query rewrite
     ├─ Network → check payload / request count / compression
     ├─ Rendering → check re-renders with React DevTools
     ├─ Bundle size → identify large libraries with bundle-analyzer
     └─ JS computation → identify long tasks with Chrome Performance

  3. Is the change < 50 lines? → No → consider splitting it up
                                → Yes ↓

  4. Do the tests pass? → No → fix
                        → Yes ↓

  5. Did you measure the improvement? → No → measure
                                       → Yes → open a PR (What/Why/Impact/Measurement)
```

---

## 5. Integration with Bolt

```
Usage within Bolt:
  1. Apply the PO-01 through PO-10 checklist in the PROFILE phase
  2. Follow the correct optimization order in the SELECT phase
  3. Leverage the three-layer measurement model in the OPTIMIZE phase
  4. Run regression tests in the VERIFY phase

Quality gates:
  - Optimization proposals with no measurement data → blocked (prevents PO-02)
  - Improvements < 1ms → rejected as micro-optimization (prevents PO-03)
  - useMemo on every function → warn as excessive memoization (prevents PO-04)
  - No performance budget configured → recommend CI integration (prevents PO-08)
```

**Source:** [Stackify: Why Premature Optimization is Evil](https://stackify.com/premature-optimization-evil/) · [Revelo: How to Avoid Premature Optimization](https://www.revelo.com/blog/premature-optimization) · [Landskill: JavaScript Performance Optimization 2026](https://www.landskill.com/blog/javascript-performance-optimization/) · [TechLasi: Software Performance Optimization Tips 2026](https://techlasi.com/savvy/software-performance-optimization-tips/)
