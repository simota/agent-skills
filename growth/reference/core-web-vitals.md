# Core Web Vitals Optimization Guide

> **2026 baseline (CrUX):** Only ~48% of mobile origins pass all three Core Web Vitals; ~43% of sites still fail the INP < 200ms threshold at p75, making INP the most commonly failed CWV. LCP mobile pass rate sits around 52–62%; CLS has the highest pass rate. INP replaced FID as a Core Web Vital on 2024-03-12. Always treat CrUX/RUM as authoritative — Lighthouse-passing + CrUX-failing is the most common Growth blind spot. [Source: corewebvitals.io 2026 guide, https://www.corewebvitals.io/core-web-vitals; web.dev/articles/inp]

## LCP (Largest Contentful Paint) - Target: < 2.5s

### Optimize Hero Images

```html
<!-- Preload critical hero image -->
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

<!-- Responsive images with srcset -->
<img
  src="/hero-800.webp"
  srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Hero description"
  fetchpriority="high"
  decoding="async"
/>
```

### Optimize Fonts

```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

<!-- Font display swap to prevent FOIT -->
<style>
@font-face {
  font-family: 'Main Font';
  src: url('/fonts/main.woff2') format('woff2');
  font-display: swap;
}
</style>
```

### Server-Side Rendering / Static Generation

```typescript
// Next.js - Prefer SSG/SSR for LCP-critical pages
export async function getStaticProps() {
  const data = await fetchCriticalData();
  return { props: { data }, revalidate: 3600 };
}
```

## INP (Interaction to Next Paint) - Target: < 200ms

### Thresholds

| Rating | INP Value |
|--------|-----------|
| Good | ≤ 200ms |
| Needs Improvement | 200–500ms |
| Poor | > 500ms |

### INP Component Breakdown

INP measures the worst interaction latency, decomposed into 3 phases:

1. **Input Delay** — time from user action to event handler start (caused by long tasks blocking main thread)
2. **Processing Time** — time spent executing event handlers
3. **Presentation Delay** — time from handler completion to next frame paint

### Reduce Input Delay: Break Up Long Tasks

> **scheduler.yield() browser support (2026-05):** Chrome 129+ (stable since 2024-10), Firefox (since 2025-08), Edge 129+. **Safari has not implemented it** — ship a `setTimeout(0)` / MessageChannel polyfill for Safari users. Not yet Baseline. [Source: caniuse.com — Scheduler API: yield, https://caniuse.com/mdn-api_scheduler_yield]

```typescript
// Use scheduler.yield() with a safe fallback for Safari and older browsers
async function yieldToMain(): Promise<void> {
  if ('scheduler' in window && 'yield' in (window as any).scheduler) {
    return (window as any).scheduler.yield();
  }
  return new Promise(resolve => setTimeout(resolve, 0));
}

async function processLargeDataset(items: string[]): Promise<void> {
  for (let i = 0; i < items.length; i++) {
    processItem(items[i]);
    // Yield every 50 items to keep input delay low
    if (i % 50 === 0) await yieldToMain();
  }
}
```

### Diagnose with Long Animation Frames (LoAF) API

LoAF shipped stable in **Chrome 123 (2024-03)** and is the recommended primary diagnostic for INP. Each LoAF entry exposes the slow rendering update's `scripts[]`, `renderStart`, `styleAndLayoutStart`, and `duration` so you can attribute INP to a specific script/source-location. Use it in production via `PerformanceObserver` (entry type `long-animation-frame`) — `longtask` is now considered legacy for INP diagnosis. [Source: Chrome for Developers — Long Animation Frames API, https://developer.chrome.com/docs/web-platform/long-animation-frames]

```typescript
new PerformanceObserver((list) => {
  for (const entry of list.getEntries() as PerformanceLongAnimationFrameTiming[]) {
    if (entry.duration < 50) continue;
    const worstScript = entry.scripts.sort((a, b) => b.duration - a.duration)[0];
    navigator.sendBeacon('/analytics', JSON.stringify({
      loaf_duration_ms: entry.duration,
      blocking_duration_ms: entry.blockingDuration,
      source: worstScript?.sourceURL,
      function: worstScript?.sourceFunctionName,
      invoker: worstScript?.invoker,
    }));
  }
}).observe({ type: 'long-animation-frame', buffered: true });
```

### Optimize Processing Time: Minimize Event Handlers

```typescript
import { memo, useMemo, useCallback } from 'react';
import { useDebouncedCallback } from 'use-debounce';

// Memoize expensive components to skip re-renders
const ExpensiveList = memo(({ items }: { items: string[] }) => (
  <ul>{items.map(item => <li key={item}>{item}</li>)}</ul>
));

function SearchPage() {
  const [query, setQuery] = React.useState('');
  const [results, setResults] = React.useState<string[]>([]);

  // Debounce to limit processing frequency
  const handleSearch = useDebouncedCallback(async (value: string) => {
    const data = await fetchResults(value);
    setResults(data);
  }, 300);

  // Throttle scroll handler
  const handleScroll = useCallback(
    throttle(() => { /* scroll logic */ }, 100),
    []
  );

  return (
    <>
      <input onChange={e => { setQuery(e.target.value); handleSearch(e.target.value); }} />
      <ExpensiveList items={results} />
    </>
  );
}
```

### Reduce Presentation Delay: DOM & CSS Optimizations

```css
/* CSS containment: limit layout/paint scope */
.card {
  contain: layout paint;
}

/* content-visibility: skip rendering off-screen content */
.below-fold-section {
  content-visibility: auto;
  contain-intrinsic-size: 0 500px; /* estimated height */
}
```

```typescript
// Defer non-critical UI updates using startTransition
import { startTransition } from 'react';

function FilterPanel({ onFilter }: { onFilter: (f: string) => void }) {
  const handleChange = (value: string) => {
    // Mark heavy state update as non-urgent
    startTransition(() => {
      onFilter(value);
    });
  };
  return <select onChange={e => handleChange(e.target.value)}>{/* options */}</select>;
}
```

### Measure INP with RUM

```typescript
import { onINP, type INPMetricWithAttribution } from 'web-vitals/attribution';

onINP((metric: INPMetricWithAttribution) => {
  const { name, value, rating, attribution } = metric;
  const { interactionType, interactionTime, inputDelay, processingDuration, presentationDelay } = attribution;

  // Send breakdown to analytics for per-interaction debugging
  navigator.sendBeacon('/analytics', JSON.stringify({
    metric: name,
    value,
    rating,
    interactionType,
    interactionTime,
    inputDelay,
    processingDuration,
    presentationDelay,
  }));
});
```

### Debounce/Throttle Event Handlers

```typescript
import { useDebouncedCallback } from 'use-debounce';

function SearchInput() {
  const handleSearch = useDebouncedCallback((value: string) => {
    // Expensive search operation
    performSearch(value);
  }, 300);

  return <input onChange={(e) => handleSearch(e.target.value)} />;
}
```

### Use Web Workers for Heavy Computation

```typescript
// worker.ts
self.onmessage = (e) => {
  const result = heavyComputation(e.data);
  self.postMessage(result);
};

// component.tsx
const worker = new Worker(new URL('./worker.ts', import.meta.url));
worker.postMessage(data);
worker.onmessage = (e) => setResult(e.data);
```

### Avoid Long Tasks

```typescript
// Break up long tasks with scheduler.yield() or setTimeout
async function processItems(items: Item[]) {
  for (const item of items) {
    processItem(item);
    // Yield to main thread periodically
    if (shouldYield()) {
      await new Promise(resolve => setTimeout(resolve, 0));
    }
  }
}
```

## CLS (Cumulative Layout Shift) - Target: < 0.1

### Reserve Space for Dynamic Content

```css
/* Reserve space for images */
.image-container {
  aspect-ratio: 16 / 9;
  background-color: #f0f0f0;
}

/* Reserve space for ads */
.ad-slot {
  min-height: 250px;
}
```

### Prevent Font-Induced Layout Shift

```css
/* Use size-adjust for fallback fonts */
@font-face {
  font-family: 'Fallback';
  src: local('Arial');
  size-adjust: 105%;
  ascent-override: 95%;
  descent-override: 22%;
  line-gap-override: 0%;
}

body {
  font-family: 'Main Font', 'Fallback', sans-serif;
}
```

### Avoid Inserting Content Above Existing Content

```tsx
// BAD: Toast appears and pushes content down
<div>
  {showToast && <Toast />}
  <MainContent />
</div>

// GOOD: Toast overlays without shifting
<div>
  <MainContent />
  {showToast && <Toast className="fixed bottom-4 right-4" />}
</div>
```

### Set Dimensions on Media Elements

```html
<!-- Always include width and height -->
<img src="photo.jpg" width="800" height="600" alt="Photo" />
<video width="1280" height="720" poster="poster.jpg"></video>
<iframe width="560" height="315" src="..."></iframe>
```

## Performance Monitoring

> **web-vitals v5 (2026-05):** Current line is **web-vitals 5.2.x** on npm. `onFID` was removed when INP officially replaced FID in 2024 — do not import it. Use `web-vitals/attribution` to ship LoAF-based INP attribution (`attribution.longAnimationFrameEntries`) for production debugging. [Source: GoogleChrome/web-vitals on npm, https://www.npmjs.com/package/web-vitals]

```typescript
// Report Core Web Vitals — web-vitals v5+
import { onCLS, onLCP, onINP, onTTFB, onFCP, type Metric } from 'web-vitals';

function sendToAnalytics(metric: Metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating, // good | needs-improvement | poor
    id: metric.id,
    navigationType: metric.navigationType,
  });
  navigator.sendBeacon('/analytics', body);
}

onCLS(sendToAnalytics);
onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onTTFB(sendToAnalytics);
onFCP(sendToAnalytics);
```
