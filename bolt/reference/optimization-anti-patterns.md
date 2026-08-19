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
## 3. The Three-Layer Measurement Model
| Layer | Tools | Metrics | Timing |
|---|--------|---------|---------|
| **Development** | React DevTools · Chrome Performance · Lighthouse | Render time · Bundle size · LCP/INP/CLS | Per PR |
| **CI/CD** | Lighthouse CI · webpack-bundle-analyzer · autocannon | Budget overruns · regression detection · throughput | Per merge |
| **Production** | RUM (web-vitals) · Synthetic Monitoring · APM | p50/p75/p95 · error rate · business impact | Continuous |
---
## 5. Integration with Bolt
**Source:** [Stackify: Why Premature Optimization is Evil](https://stackify.com/premature-optimization-evil/) · [Revelo: How to Avoid Premature Optimization](https://www.revelo.com/blog/premature-optimization) · [Landskill: JavaScript Performance Optimization 2026](https://www.landskill.com/blog/javascript-performance-optimization/) · [TechLasi: Software Performance Optimization Tips 2026](https://techlasi.com/savvy/software-performance-optimization-tips/)
