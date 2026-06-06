# Dashboard Prototyping Reference

Purpose: Validate a single dashboard hypothesis (layout, widget mix, filter model, chart choice) in ≤4h with seeded mock data. Skip real data wiring, skip color-token polish, skip full filter matrices.

## Scope Boundary

- **Forge `dashboard`**: throwaway admin / analytics screen, one layout, one widget set, mock time-series.
- **Artisan (elsewhere)**: production dashboard implementation (real data hooks, pagination, loading states, error boundaries).
- **Muse (elsewhere)**: design tokens, chart palette governance, dark-mode color mapping.
- **Pulse (elsewhere)**: KPI definition and event taxonomy — Pulse answers *what* to measure; `dashboard` answers *what does it look like*.

## Charting Library Selection

| Library | Pick when | Skip when |
|---------|-----------|-----------|
| **Recharts** | React, simple line/bar/pie, sensible defaults, <5 chart types | High density (>10k points), custom interactions |
| **ECharts** | Dense data, candlestick, geo maps, heatmap, large series | Bundle size matters, static charts only |
| **Chart.js** | Vanilla JS or small React wrapper, minimal deps | Complex zooming / brushing / annotation |
| **Visx / D3** | Custom chart type is the hypothesis | You are prototyping layout, not chart invention |
| **Tremor** | Analytics dashboard template, shadcn-style | Custom chart types dominate |

Default: **Recharts** for React React-based PoC. **ECharts** when the hypothesis is "can this handle dense trading / telemetry data?"

## Workflow

```
SCAFFOLD  →  declare dashboard hypothesis (what question does this answer?)
          →  pick layout (grid / split / tabs / single-view)
          →  list widgets (≤6 for PoC; anything more is scope creep)
          →  pick one charting library, one mock-data seed

STRIKE    →  build layout shell first (grid, responsive break, header, filter slot)
          →  wire each widget to a deterministic mock generator
          →  make one filter (date range or dimension) actually change the data
          →  virtualize tables beyond 100 rows — use TanStack Virtual or react-window

COOL      →  resize to mobile / tablet / desktop — flag broken widgets
          →  verify empty state, single-data-point state, loading skeleton
          →  note skipped: real data, saved views, export, drill-down

PRESENT   →  ADOPT / ITERATE / DISCARD
          →  if ADOPT: hand off to Artisan for production component build
```

## Deterministic Mock Time-Series

Seed every generator so the demo is reproducible and reviewers see the same numbers twice.

```ts
// mock/time-series.ts
function seededRandom(seed: number): () => number {
  let x = seed;
  return () => {
    x = (x * 1103515245 + 12345) & 0x7fffffff;
    return x / 0x7fffffff;
  };
}

export function generateSeries(
  seed: number,
  points: number,
  baseline: number,
  noise: number,
): { t: string; v: number }[] {
  const rand = seededRandom(seed);
  const now = Date.now();
  return Array.from({ length: points }, (_, i) => ({
    t: new Date(now - (points - i) * 86400000).toISOString(),
    v: Math.round(baseline + (rand() - 0.5) * noise),
  }));
}
```

Drift the series just enough that filters visibly change the chart. Don't fake spikes that imply real product behavior — reviewers will remember them.

## Layout Patterns

| Pattern | Pick when |
|---------|-----------|
| Top header + 2×3 KPI grid + full-width chart | Executive / exec-summary dashboards |
| Left sidebar filter + right canvas | Exploratory analytics, >5 filter dimensions |
| Top filter bar + single stacked column | Operational dashboards (incident / order queue) |
| Tabbed panels | Multiple related views on same dataset |

Commit to one pattern in SCAFFOLD. Swapping patterns mid-STRIKE burns the time-box.

## Table Virtualization

Beyond ~100 rows, non-virtualized tables cause scroll jank that distracts reviewers from the hypothesis.

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';

// render 50k rows at 60fps — keeps focus on layout/filter hypothesis
```

If the hypothesis is *table layout* specifically, 20 hand-crafted rows beats 50k virtualized — the point is what rows look like, not scroll perf.

## Time-Box Anti-Patterns

- ❌ Add a second charting library "because pie looks better in D3".
- ❌ Polish dark-mode color palette — hand off to Muse if ADOPT.
- ❌ Wire real API "just to prove it". Deterministic mocks make the demo reproducible.
- ❌ Build saved-views / export / print — out of scope for PoC.
- ❌ Pixel-match an existing dashboard screenshot — that's Pixel's job, not Forge's.

## What Goes in the Handoff to Artisan

- Layout grid definition (column count, gaps, breakpoints).
- Widget list with mock-data shape per widget.
- Filter contract: which filter maps to which widget, which dimensions change data.
- Charting library chosen and why.
- Known skipped: real API, pagination, export, saved views, permission-aware widgets, i18n.
- Hypothesis outcome: did this answer the business question? What layout change would you try next?
