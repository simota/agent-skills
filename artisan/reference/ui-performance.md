# UI Performance Reference

Purpose: Tune a single component or page so it renders fast, stays responsive (INP < 200ms), and ships the smallest reasonable bundle. Measure before and after — every tactic below has a wrong context where it hurts more than it helps.

## Scope Boundary

- **Artisan `perf`**: frontend-component-level tuning inside one component or one page. Memoization, list virtualization, dynamic import, per-route bundle audit.
- **Bolt (elsewhere)**: cross-cutting performance specialist — frontend + backend. Server response time, DB waterfalls, SSR/streaming strategy, app-wide bundle budget, Core Web Vitals program, N+1 fixes.

If the ask is "this table rerenders 12× per keystroke" or "this page ships 400KB of unused JS" → `perf`. If the ask is "our whole app's LCP regressed across all routes" or "cut 30% of API latency" → `Bolt`. Cross-link: Artisan's component delta becomes a data point Bolt can aggregate.

## Workflow

```
ANALYZE  →  measure first: React Profiler / Chrome Performance / `next build` output
         →  identify the actual bottleneck: render count, long tasks, bundle size, or re-layout
         →  check React Compiler status — if on, skip manual memoization

DESIGN   →  pick one tactic per bottleneck (do not stack all of them blindly)
         →  decide virtualization threshold (>100 rows, >50 with rich rows)
         →  decide split boundary (route, modal, chart, rich editor) — keep above-the-fold eager

IMPLEMENT →  apply one tactic, rebuild, re-measure
         →  wire a fallback UI for Suspense-based code splits
         →  verify a11y survives (virtualized rows keep ARIA row/rowheader, dynamic imports keep focus)

VERIFY   →  compare INP / render count / bundle size before vs after
         →  abort the tactic if the delta is not meaningful (< 10% on the target metric)
         →  record the measurement in the deliverable
```

## Memoization (React)

- React Compiler (v1.0) auto-memoizes. If enabled, do NOT add `memo` / `useMemo` / `useCallback` — they add noise and can conflict. Use the `"use no memo"` directive to opt a single component out when needed.
- Without the compiler: memoize only when the Profiler shows wasted renders or a measurably heavy calculation. Premature memoization allocates cache entries on every render for zero gain.

```tsx
// Legitimate use: expensive derived value recomputed on unrelated parent re-render
const totals = useMemo(() => calcTotals(rows), [rows]);

// Legitimate use: stable identity passed to memoized child / effect dep
const handleSelect = useCallback((id) => onSelect(id), [onSelect]);

// Legitimate use: memoize child whose parent re-renders frequently on unrelated state
const Row = memo(function Row({ row }) { /* ... */ });
```

## List Virtualization

- TanStack Virtual (headless, framework-agnostic across React/Vue/Solid) — default pick for new code.
- react-window — simpler API, good for fixed-height rows, smaller bundle than react-virtualized.
- Threshold: virtualize when the list exceeds ~100 rows OR rows are rich (images, charts) beyond ~50.

```tsx
const parentRef = useRef<HTMLDivElement>(null);
const rowVirt = useVirtualizer({
  count: rows.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 48,
  overscan: 8,
});
// Preserve ARIA: role="grid" + role="row" on the virtualized rows; set aria-rowcount to the full count, not the rendered count.
```

## Code Splitting

- `next/dynamic` (Next.js) / `React.lazy` + `<Suspense>` — split below-the-fold or interaction-gated UI (modal content, charts, rich editor, map).
- Keep critical render path eager — above-the-fold and first-interaction UI do NOT benefit from splitting and pay a chunk-fetch round trip.
- Always ship a fallback with stable layout dimensions to avoid CLS.

```tsx
const Chart = dynamic(() => import('./Chart'), {
  ssr: false,
  loading: () => <div className="h-64" aria-busy="true" />,
});
```

## Bundle Audit

- `next build` / Vite's build summary / `rollup-plugin-visualizer` / `source-map-explorer` — read the per-route tree, not a global total.
- Common wins: a single heavy import pulling a whole library (`import _ from 'lodash'` → `import debounce from 'lodash/debounce'`), duplicated polyfills, moment.js where `Intl` would do.
- Per-route budget starting point: ≤ 170KB gzipped JS on the critical route. Adjust to project baseline.

## Anti-patterns

- Wrapping every function in `useCallback` "to be safe" — allocates a new wrapper per render when the consumer isn't a memoized child; pure overhead.
- Wrapping every component in `React.memo` — prop-equality checks cost more than the re-render for cheap leaf components.
- Virtualizing a 30-row list — pays the complexity tax (a11y rework, scroll restoration, focus bugs) for zero perceptible gain.
- Splitting above-the-fold UI — hurts LCP; the fallback flashes before the real content.
- Trusting `React.memo` with unstable prop identity (inline objects/functions) — comparison always fails, re-render always happens.
- Optimizing without measurement — the "fix" often lands nowhere near the actual hot path.

## Handoff

- To `Bolt` when the perf issue is cross-cutting (multiple routes, backend involvement, SSR strategy, CWV program).
- To `Radar` for perf regression tests (render count, bundle-size snapshot).
- To `Vitrine` for a story that demonstrates the fast path (virtualized list / lazy chart).
- To `Muse` only if the perf win depends on token/styling restructure; otherwise keep styling scope stable during the perf pass.
