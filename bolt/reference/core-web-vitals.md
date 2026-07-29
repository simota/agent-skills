# Core Web Vitals Optimization Details

## 2026 Thresholds and Headline Stats

| Metric | "Good" | "Needs Improvement" | "Poor" |
|--------|--------|----------------------|--------|
| LCP — Largest Contentful Paint | `≤ 2.5 s` | `2.5 – 4.0 s` | `> 4.0 s` |
| INP — Interaction to Next Paint | `≤ 200 ms` | `200 – 500 ms` | `> 500 ms` |
| CLS — Cumulative Layout Shift | `≤ 0.1` | `0.1 – 0.25` | `> 0.25` |

2026 calibration anchors (use these to prioritise where Bolt spends fix budget):

- **Only ~48% of mobile origins pass all three Core Web Vitals at p75 (CrUX)** — LCP mobile pass rate sits around 52–62%; CLS has the highest pass rate of the three. Always treat CrUX/RUM as authoritative over lab tools — a page that passes Lighthouse but fails CrUX at p75 is the most common false-confidence trap. [Source: corewebvitals.io 2026 guide, https://www.corewebvitals.io/core-web-vitals]
- **INP is the most commonly failed CWV** — `~43%` of measured sites fail the `200 ms` threshold at p75. Treat any new feature touching the main thread as an INP risk by default. INP replaced FID as a Core Web Vital on 2024-03-12; do not import `onFID` from `web-vitals` v5+, it was removed.
- **Images dominate LCP** — they are the LCP element on `~72%` of mobile pages. The LCP fight is almost always an image fight; backend TTFB is a secondary lever for that workload.
- **WebP is the 2026 default image format** — `~97%` browser support, `25–34%` smaller than JPEG at equivalent quality, fast decode. Reserve AVIF for hero / above-the-fold assets where the extra `40–60%` payload reduction is worth the heavier decode CPU (especially on low-end mobile).
- **Never lazy-load the LCP element.** `loading="lazy"` on the hero image is the most common regression introduced by well-meaning "performance" PRs.

## LCP Optimization

### Issue: Large hero image
Fix:
- Add `loading="eager"` and `fetchpriority="high"`
- Use next/image with priority prop
- Preload critical images
- Serve responsive sizes via `srcset`/`sizes` so mobile doesn't download the desktop asset
```html
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

<img
  src="/hero-800.webp"
  srcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Hero description"
  fetchpriority="high"
  decoding="async"
/>
```

### Issue: Unoptimized image format
Fix:
- Serve AVIF with WebP and JPEG fallback via `<picture>` — AVIF is ~40–60% smaller than JPEG (~95% browser support, 2026)
- Caution: AVIF decode is CPU-heavy; on low-end mobile devices, WebP may yield better LCP due to faster decode
```html
<picture>
  <source srcset="/hero.avif" type="image/avif">
  <source srcset="/hero.webp" type="image/webp">
  <img src="/hero.jpg" alt="..." width="1200" height="630"
       loading="eager" fetchpriority="high">
</picture>
```

### Issue: Web fonts blocking or delaying the LCP element
Fix:
- Preload the critical font file so it doesn't wait behind the CSS parse
- Use `font-display: swap` to avoid a blank-text render blocking paint
```html
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>

<style>
@font-face {
  font-family: 'Main Font';
  src: url('/fonts/main.woff2') format('woff2');
  font-display: swap;
}
</style>
```

### Issue: Render-blocking CSS/JS
Fix:
- Inline critical CSS
- Defer non-critical JavaScript
- Use `<link rel="preload">` for critical resources

### Issue: Slow server response (TTFB)
Fix:
- Enable caching (CDN, HTTP cache)
- Optimize backend queries
- Use edge computing (Vercel Edge, Cloudflare Workers)

### Issue: Client-side rendering delay
Fix:
- Use SSR/SSG for above-the-fold content
- Stream HTML with React Suspense
- Avoid hydration waterfalls
```typescript
// Next.js - prefer SSG/SSR for LCP-critical pages over client fetching
export async function getStaticProps() {
  const data = await fetchCriticalData();
  return { props: { data }, revalidate: 3600 };
}
```

---

## INP Optimization

INP measures the worst interaction latency on the page, decomposed into 3 phases — target the specific phase that's failing rather than applying every fix blindly:

1. **Input Delay** — time from user action to event handler start (caused by long tasks blocking the main thread)
2. **Processing Time** — time spent executing event handlers
3. **Presentation Delay** — time from handler completion to next frame paint

### Issue: Long JavaScript tasks (Input Delay)
Fix:
- Break long tasks with `await scheduler.yield()` (stable in Chrome 129+/Firefox since 2025-08/Edge 129+; **Safari has not implemented it** — ship a `setTimeout(0)` fallback)
- Use Web Workers for heavy computation
- Debounce/throttle event handlers
- Split hydration with React's `prerender` / Server Components so the main thread isn't blocked rebuilding the whole client tree on first input

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
    if (i % 50 === 0) await yieldToMain();
  }
}
```

```typescript
// worker.ts — offload heavy computation off the main thread entirely
self.onmessage = (e) => {
  const result = heavyComputation(e.data);
  self.postMessage(result);
};

// component.tsx
const worker = new Worker(new URL('./worker.ts', import.meta.url));
worker.postMessage(data);
worker.onmessage = (e) => setResult(e.data);
```

**Diagnose with Long Animation Frames (LoAF):** LoAF shipped stable in Chrome 123 (2024-03) and is the recommended primary diagnostic for INP — `longtask` is now legacy for this purpose. Each entry exposes the slow frame's `scripts[]`, `renderStart`, `styleAndLayoutStart`, and `duration`, letting you attribute INP to a specific script/source-location in production.

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

### Issue: Slow event handlers (Processing Time)
Fix:
- Use `useTransition`/`startTransition` for non-urgent state updates that should not block the input
- Virtualize long lists (`@tanstack/react-virtual`, `react-window`)
- Debounce/throttle handlers that fire on every keystroke or scroll tick
- Rely on **React Compiler 1.0** auto-memoization rather than handwriting `React.memo` — see `react-performance.md`. Manual memoization layered on top of the compiler often regresses INP because it adds dependency-tracking work the compiler already eliminated.

```typescript
import { startTransition } from 'react';
import { useDebouncedCallback } from 'use-debounce';

function FilterPanel({ onFilter }: { onFilter: (f: string) => void }) {
  const handleChange = (value: string) => {
    // Mark heavy state update as non-urgent so it doesn't block the input
    startTransition(() => onFilter(value));
  };
  return <select onChange={e => handleChange(e.target.value)}>{/* options */}</select>;
}

function SearchInput() {
  const handleSearch = useDebouncedCallback((value: string) => {
    performSearch(value); // expensive — limit call frequency
  }, 300);
  return <input onChange={(e) => handleSearch(e.target.value)} />;
}
```

### Issue: Layout thrashing (Presentation Delay)
Fix:
- Batch DOM reads/writes
- Use `requestAnimationFrame` for animations
- Avoid forced synchronous layouts
- Use CSS containment to limit the browser's layout/paint scope, and `content-visibility` to skip rendering off-screen sections

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

### Measurement

```typescript
// Basic INP measurement
import { onINP } from 'web-vitals';

onINP((metric) => {
  console.log('INP:', metric.value);
  // Report to analytics
});
```

```typescript
// Attribution build — breaks INP down by interaction for production debugging
import { onINP, type INPMetricWithAttribution } from 'web-vitals/attribution';

onINP((metric: INPMetricWithAttribution) => {
  const { name, value, rating, attribution } = metric;
  const { interactionType, interactionTime, inputDelay, processingDuration, presentationDelay } = attribution;

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

---

## CLS Optimization

### Issue: Media elements without dimensions
Fix:
```jsx
// Always specify dimensions
<img src="..." width={800} height={600} alt="..." />

// Or use aspect-ratio CSS
<div style={{ aspectRatio: '16/9' }}>
  <img src="..." style={{ width: '100%', height: '100%' }} />
</div>
```
```html
<!-- Same rule applies to video and iframe embeds -->
<video width="1280" height="720" poster="poster.jpg"></video>
<iframe width="560" height="315" src="..."></iframe>
```

### Issue: Ads/embeds causing shifts
Fix:
- Reserve space with min-height
- Use contain-intrinsic-size CSS
- Lazy load below the fold only

### Issue: Web fonts causing FOUT/layout shift
Fix:
- `font-display: swap` with a fallback font of similar metrics avoids invisible text but can still shift layout when the swapped-in font has different glyph widths
- For pixel-tight designs, tune the fallback font's metrics to match the web font so the swap causes no shift at all
```css
font-family: 'Custom Font', system-ui, sans-serif;
font-display: swap;
```
```css
/* Metric-matched fallback: eliminates the shift on font swap entirely */
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

### Issue: Dynamic content insertion
Fix:
- Reserve space for dynamic content
- Use skeleton loaders with fixed dimensions
- Avoid inserting content above existing content — overlay instead of push
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

---

## Web Vitals Monitoring

Current line is **web-vitals 5.2.x** on npm. `onFID` was removed when INP officially replaced FID in 2024 — do not import it. Use `web-vitals/attribution` (see INP Measurement above) for LoAF-based INP attribution in production debugging.

```typescript
// web-vitals integration — web-vitals v5+
import { onLCP, onINP, onCLS, onTTFB, onFCP, type Metric } from 'web-vitals';

function sendToAnalytics(metric: Metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating, // good | needs-improvement | poor
    delta: metric.delta,
    id: metric.id,
    navigationType: metric.navigationType,
  });

  // Use sendBeacon for reliability
  navigator.sendBeacon('/api/vitals', body);
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
onTTFB(sendToAnalytics);
onFCP(sendToAnalytics);
```
