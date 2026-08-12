# Profiling Tools Reference

## Frontend Profiling

| Tool | Use Case | Command/Setup |
|------|----------|---------------|
| **React DevTools Profiler** | Component render timing | Browser extension |
| **Chrome DevTools Performance** | JS execution, layout, paint | F12 → Performance |
| **Lighthouse** | Core Web Vitals audit | F12 → Lighthouse |
| **web-vitals** | Real user metrics | `npm i web-vitals` |
| **why-did-you-render** | Unnecessary re-renders | `npm i @welldone-software/why-did-you-render` |

### React Profiling

```typescript
// Enable React Profiler in development
import { Profiler } from 'react';

function onRenderCallback(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
  baseDuration: number,
  startTime: number,
  commitTime: number
) {
  console.log(`${id} ${phase}: ${actualDuration.toFixed(2)}ms`);
}

<Profiler id="MyComponent" onRender={onRenderCallback}>
  <MyComponent />
</Profiler>
```

---

## Backend Profiling

| Tool | Use Case | Command/Setup |
|------|----------|---------------|
| **Node.js --inspect** | CPU profiling, heap | `node --inspect app.js` |
| **clinic.js** | Node.js performance suite | `npx clinic doctor -- node app.js` |
| **0x** | Flame graphs | `npx 0x app.js` |
| **autocannon** | HTTP load testing | `npx autocannon http://localhost:3000` |

### Node.js Profiling Commands

```bash
# CPU profiling with Chrome DevTools
node --inspect-brk app.js
# Open chrome://inspect

# Generate flame graph with 0x
npx 0x app.js
# Creates interactive flame graph

# Load testing with autocannon
npx autocannon -c 100 -d 30 http://localhost:3000/api/users
# -c: connections, -d: duration in seconds

# Memory profiling
node --expose-gc --inspect app.js
# In DevTools: Memory tab → Take heap snapshot
```

---

## Bundle Analysis

```bash
# Next.js bundle analyzer
ANALYZE=true npm run build

# Webpack bundle analyzer
npx webpack-bundle-analyzer stats.json

# Source map explorer
npx source-map-explorer 'dist/**/*.js'

# Bundlephobia (check before installing)
# https://bundlephobia.com/package/lodash
```


## Per-Recipe Behavior + VERIFY Gates (SKILL.md excerpt)

Behavior notes per Recipe:
- `frontend`: Verify React Compiler activation. Measure LCP/INP/CLS → optimize the single largest bottleneck. **VERIFY**: check waterfalls **before** memo/render work; after-metric beats baseline AND clears the CWV "Good" gate (LCP ≤2.5s, INP ≤200ms — ≤150ms for post-March-2026 SEO stability, CLS ≤0.1); no new commit/re-render introduced (React DevTools Profiler).
- `backend`: Target N+1/cache/connection pool. Follow Bolt→Tuner handoff criteria (deep SQL analysis). **VERIFY**: query/span count + p95 captured pre-change; N+1 span count collapses to 1–2 (not N+1); every connection returned via try/finally (no pool leak); any added cache key has a TTL; after-p95 beats baseline; event-loop lag ≤100ms held.
- `render`: Specialize in React re-render reduction. Consider manual memo only when React Compiler is not in use. **VERIFY**: wasted-commit count measured pre/post (React DevTools Profiler) and strictly drops; manual `memo`/`useMemo`/`useCallback` added ONLY when compiler off OR expensive sync compute proven (else it's dead weight under the compiler); identical render output (no behavior change).
- `async`: Convert sequential await to Promise.all. Async waterfall is the top performance root cause (Vercel research). **VERIFY**: parallelize ONLY independent awaits — a dependent chain must stay sequential; total latency captured pre/post and approaches `max(parts)` not `sum(parts)`; partial-failure semantics chosen deliberately (`Promise.all` fail-fast vs `allSettled` tolerant); no shared-state race introduced by reordering.
- `cache`: LRU/Redis/HTTP cache. Always set TTL. Include stampede countermeasures (lock/lease). **VERIFY**: **every** key has a TTL (zero unbounded-growth keys); hot keys carry a stampede guard (lock/lease or `stale-while-revalidate`); hit-rate ↑ and origin load ↓ vs baseline; staleness window is acceptable for the data's correctness contract; cheapest layer tried first (HTTP `stale-while-revalidate` before in-process LRU).
- `bundle`: App-wide JS/TS bundle-size audit. Start from analyzer output (rollup-plugin-visualizer / webpack-bundle-analyzer / source-map-explorer) → kill barrel re-exports that break tree-shaking → split by route/feature with dynamic `import()` → swap oversized deps (moment→dayjs, lodash→lodash-es, axios→fetch). Set a per-route kB budget. Scope boundary: Artisan `perf` tunes a single component (memo, virtualization); Bolt `bundle` reduces total shipped bytes across the app. If the hypothesis is "this one list is slow", route to Artisan. **VERIFY**: analyzer-measured total + per-route kB captured pre/post and falls under the declared budget; the swapped/dead lib is gone from the emitted chunk (not just `package.json`); no barrel re-export reintroduced; dynamic `import()` boundaries don't break SSR/hydration; no runtime behavior change.
- `network`: Client/server delivery-layer tuning. Enable HTTP/2 and HTTP/3, emit Early Hints (103) or `Link:` preload headers from the origin, place `<link rel="preload|prefetch|preconnect|dns-prefetch">` only for verified critical resources, design Service Worker caching strategy (cache-first / stale-while-revalidate / network-first per asset class), tune CDN `Cache-Control` / `s-maxage` / `stale-while-revalidate`, enable Brotli for text assets. Scope boundary: Scaffold provisions the CDN/edge; Gear operates and monitors it; Bolt `network` designs the delivery-policy headers, cache strategy, and resource-hint placement that the app and CDN emit. **VERIFY**: TTFB/LCP captured pre/post and beats baseline; resource hints cover ONLY verified-critical resources (no over-preload — unused preloads warn in console and waste bandwidth); SW strategy matches asset class (network-first for HTML, cache-first for hashed static); CDN `Cache-Control` cannot serve stale mutable data; Brotli confirmed on text responses.
- `memory`: App-process memory footprint reduction. Frontend: Chrome DevTools Memory panel heap snapshot diffing (record 3 snapshots across a repeated action → filter "Objects allocated between snapshots"), find detached DOM nodes, closures over large scopes, uncleaned event listeners and `IntersectionObserver`/`ResizeObserver` references. Backend: Node.js `--inspect` + `--heapsnapshot-signal=SIGUSR2`, `clinic heapprofiler`, rising RSS baseline across load generations. Apply `WeakMap` / `WeakRef` where identity caches would otherwise pin GC. Scope boundary: a leak BUG (race, deadlock, resource leak with reproduction steps) is out of scope; Bolt `memory` removes the FAT (measures footprint, cuts retained size, enforces baseline budgets). If no leak is suspected but memory is simply too large, stay in Bolt. Tuner is DB-internal memory (buffer pools, work_mem) — out of scope here. **VERIFY**: retained size captured pre/post (3-snapshot diff or RSS trend across ≥3 load generations) and strictly drops; zero detached DOM nodes / uncleaned listeners remain in the after-snapshot; baseline does NOT keep rising across generations (rising baseline = unfixed leak bug, out of Bolt scope); `WeakMap`/`WeakRef` applied only where an identity cache was pinning GC.

