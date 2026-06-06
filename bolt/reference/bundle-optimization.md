# Bolt Bundle Size Optimization

Tree shaking, code splitting, and library alternatives.

---

## Analyzing Bundle Size

```bash
# Next.js built-in analyzer
ANALYZE=true npm run build

# Webpack bundle analyzer
npm install --save-dev webpack-bundle-analyzer

# Source map explorer
npm install --save-dev source-map-explorer
npx source-map-explorer 'dist/**/*.js'

# bundlephobia: Check package size before installing
# https://bundlephobia.com/package/lodash
```

---

## Tree Shaking Best Practices

```typescript
// ❌ Bad: Imports entire library
import _ from 'lodash';
const result = _.groupBy(items, 'category');

// ✅ Good: Import specific function
import groupBy from 'lodash/groupBy';
const result = groupBy(items, 'category');

// ✅ Better: Use lodash-es for tree shaking
import { groupBy } from 'lodash-es';

// ❌ Bad: Barrel exports prevent tree shaking
// utils/index.ts
export * from './string';
export * from './array';
export * from './date';

// ✅ Good: Direct imports
import { formatDate } from '@/utils/date';
```

---

## Code Splitting Patterns

```typescript
// Route-based splitting (React Router)
import { lazy, Suspense } from 'react';

const routes = [
  {
    path: '/dashboard',
    element: lazy(() => import('./pages/Dashboard')),
  },
  {
    path: '/settings',
    element: lazy(() => import('./pages/Settings')),
  },
];

// Component-based splitting for heavy components
const HeavyChart = lazy(() => import('./components/HeavyChart'));
const MarkdownEditor = lazy(() => import('./components/MarkdownEditor'));

function Dashboard() {
  return (
    <div>
      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart data={data} />
      </Suspense>
    </div>
  );
}

// Library-based splitting
const PDFViewer = lazy(() =>
  import('react-pdf').then(module => ({
    default: module.Document
  }))
);
```

---

## Dynamic Imports

```typescript
// Load heavy libraries on demand
async function exportToPDF(data: ReportData) {
  const { jsPDF } = await import('jspdf');
  const doc = new jsPDF();
  // ...
}

// Conditional feature loading
async function initAnalytics() {
  if (process.env.NODE_ENV === 'production') {
    const { init } = await import('@/lib/analytics');
    init();
  }
}

// Locale-based loading
async function loadLocale(locale: string) {
  const messages = await import(`./locales/${locale}.json`);
  return messages.default;
}
```

---

## Library Alternatives

| Heavy Library | Size | Lightweight Alternative | Size |
|--------------|------|------------------------|------|
| moment | 290kB | date-fns | 13kB (tree-shakeable) |
| lodash | 72kB | lodash-es / native | 0-5kB |
| axios | 14kB | native fetch / ky | 0-3kB |
| uuid | 9kB | crypto.randomUUID() | 0kB |
| classnames | 1kB | clsx | 0.5kB |
| numeral | 17kB | Intl.NumberFormat | 0kB |
| validator | 50kB | zod / valibot | 13kB / 6kB |
| chart.js | 200kB | lightweight-charts | 45kB |
| draft-js | 200kB | tiptap / lexical | 40kB |

```typescript
// Replace moment with date-fns
// ❌ Before
import moment from 'moment';
moment(date).format('YYYY-MM-DD');
moment(date).add(1, 'day');

// ✅ After
import { format, addDays } from 'date-fns';
format(date, 'yyyy-MM-dd');
addDays(date, 1);

// Replace lodash with native
// ❌ Before
import { debounce, groupBy, uniq } from 'lodash';

// ✅ After: Native alternatives
const uniq = <T>(arr: T[]): T[] => [...new Set(arr)];

const groupBy = <T>(arr: T[], key: keyof T): Record<string, T[]> =>
  arr.reduce((acc, item) => {
    const group = String(item[key]);
    (acc[group] ??= []).push(item);
    return acc;
  }, {} as Record<string, T[]>);

// Replace axios with fetch
// ❌ Before
import axios from 'axios';
const { data } = await axios.get('/api/users');

// ✅ After
const data = await fetch('/api/users').then(r => r.json());
```

---

## Next.js Specific Optimizations

```typescript
// next.config.js
module.exports = {
  // Enable experimental optimizations
  experimental: {
    optimizePackageImports: ['@heroicons/react', 'lucide-react'],
  },

  // Analyze bundle
  webpack: (config, { isServer }) => {
    if (process.env.ANALYZE) {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          reportFilename: isServer ? '../analyze/server.html' : './analyze/client.html',
        })
      );
    }
    return config;
  },
};

// Optimize imports in components
// ❌ Bad: Loads all icons
import * as Icons from '@heroicons/react/24/outline';

// ✅ Good: Loads only used icons
import { HomeIcon, UserIcon } from '@heroicons/react/24/outline';
```

---

## Bolt `bundle` Recipe

Purpose: Reduce total JS/TS shipped to the browser. The subcommand runs an analyzer-driven audit, identifies the largest controllable wins, and applies them without breaking runtime behavior. All changes are byte-quantified in PROFILE and VERIFY.

### Scope Boundary

- **Bolt `bundle`** (this Recipe): app-wide bundle-size reduction — what ships per route, per chunk, per library, per duplicate copy across lockfile. Output is kB saved per route and updated per-route budget.
- **Artisan `perf`**: single-component render tuning — `React.memo`, list virtualization, event-handler stability. Fixes "this one component is slow."
- **Bolt `frontend` / `render`**: re-render reduction and React Compiler verification. Does not change shipped bytes.
- **Gear**: build-system config (webpack/Vite/Rollup upgrade paths, minifier choice). Bolt `bundle` emits the optimization; Gear lands config changes ≥1 file wide.
- **Shift** (`detect`/`modernize`): modernize deprecated libraries entirely (migration PoC). Bolt `bundle` picks the replacement when the driver is size.

Rule of thumb: if the kB on disk don't change, it's not `bundle`.

### Workflow

```
PROFILE   →  run analyzer (rollup-plugin-visualizer / webpack-bundle-analyzer / source-map-explorer)
          →  capture baseline: total kB (gzip + brotli), per-route kB, top-10 modules by size
          →  check for duplicate copies (`npm ls <pkg>` / `pnpm why`)
          →  list barrel files that re-export broadly (index.ts fanning out)

SELECT    →  pick ONE of: tree-shake fix · route/feature split · dynamic import · library swap
          →  target: ≥10% of chunk or ≥30 kB absolute — whichever is larger
          →  rank by: user-visible impact × reversibility × test blast radius

OPTIMIZE  →  apply the single change; keep type surface stable
          →  if swapping a lib, update all call sites in one PR
          →  if splitting a route, verify the `Suspense`/loading boundary exists

VERIFY    →  re-run analyzer; diff kB per chunk
          →  run lint + test + build; confirm no SSR/hydration break
          →  record gzip + brotli delta; INP should not regress

PRESENT   →  Before/After table (route, kB, %), risks, follow-ups
          →  if a budget was added, emit the CI config snippet
```

### Analyzer Quick Reference

| Tool | Best for | Command |
|------|----------|---------|
| `rollup-plugin-visualizer` | Vite / Rollup / SvelteKit | plugin → `dist/stats.html` |
| `webpack-bundle-analyzer` | Webpack / Next.js (webpack mode) | `ANALYZE=true next build` |
| `source-map-explorer` | Any emitted sourcemap | `npx source-map-explorer 'dist/**/*.js'` |
| `@next/bundle-analyzer` | Next.js (official) | `withBundleAnalyzer` in `next.config.js` |
| Vite `--report` | Vite (built-in JSON) | `vite build --report` |

### Patterns

- **Barrel-file removal**: `export * from './foo'` chains defeat tree-shaking for consumers that don't import by deep path. Convert to explicit re-exports, or let consumers import the deep path directly. Verify with before/after analyzer.
- **Dynamic import for cold paths**: PDF/chart/rich-editor/markdown-parser libraries load on first use, not on mount. Wrap in `React.lazy` or `await import()` behind the click.
- **Per-route budget**: add `performance.maxEntrypointSize` (webpack) or size-limit / bundlewatch to CI. Fail the build when a route grows >5%.
- **Dependency dedup**: `npm dedupe` / `pnpm dedupe`; check for multi-version `react-is`, `tslib`, `@emotion/*`, ICU data.

### Anti-Patterns

- Swapping `lodash` → `lodash-es` without confirming the bundler actually tree-shakes it (some configs re-bundle all of lodash-es).
- Adding `next/dynamic` without `ssr: false` when the module references `window` — breaks SSR, not the bundle.
- "Optimizing" a library that's already shaken to <5 kB — measure first.
- Code-splitting the shell route — forces an extra RTT on every user.
- Removing `moment` one call site at a time over weeks — land the swap atomically.

### Handoff

- **→ Gear**: when the fix requires build-config changes (webpack rule, Vite plugin, tsconfig `"moduleResolution"`).
- **→ Shift** (`modernize` recipe): when the only viable path is retiring a legacy library entirely (jQuery, moment, draft-js).
- **→ Artisan**: when the analyzer surfaced a large component that needs restructuring, not just splitting.
- **→ Radar**: add bundle-size regression test to CI (size-limit, bundlewatch).
