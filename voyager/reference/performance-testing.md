# Performance Testing in E2E Context

Purpose: Use this file when Voyager must measure browser performance, enforce budgets, or hand off evidence to Bolt.

Contents:
- Agent boundary and budget thresholds
- Core Web Vitals and Lighthouse integration
- Regression detection, resource analysis, and Bolt handoff fields

---

## Agent Boundary

| Responsibility | Voyager | Bolt | Growth |
|----------------|---------|------|--------|
| **E2E performance measurement** | ✅ Primary | | |
| **Core Web Vitals assertion** | ✅ Primary | | |
| **Lighthouse CI integration** | ✅ Primary | | |
| **Code-level optimization** | | ✅ Primary | |
| **Bundle size reduction** | | ✅ Primary | |
| **Field data analysis (RUM)** | | | ✅ Primary |
| **Performance regression detection** | ✅ E2E context | ✅ Build context | ✅ Field context |

**Rule of thumb**: Voyager **measures and asserts** performance in the browser. Bolt **fixes** the code. Growth **analyzes** real-user data.

---

## Performance Budget Configuration

### Budget JSON File

```json
// performance-budget.json
{
  "metrics": {
    "LCP": { "target": 2500, "warning": 2000, "unit": "ms" },
    "CLS": { "target": 0.1, "warning": 0.05, "unit": "score" },
    "INP": { "target": 200, "warning": 100, "unit": "ms" },
    "TTFB": { "target": 800, "warning": 500, "unit": "ms" },
    "FCP": { "target": 1800, "warning": 1200, "unit": "ms" }
  },
  "resources": {
    "totalPageWeight": { "target": 1500, "unit": "KB" },
    "jsBundle": { "target": 300, "unit": "KB" },
    "cssBundle": { "target": 100, "unit": "KB" },
    "imageTotal": { "target": 500, "unit": "KB" }
  },
// ...
```

### Playwright Config Extension

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    // Enable performance tracing
    trace: 'on-first-retry',
  },
  // Custom metadata for performance budgets
  metadata: {
    performanceBudget: './performance-budget.json',
  },
});
```

---

## Core Web Vitals Measurement

### Custom Performance Fixture

```typescript
// e2e/fixtures/performance.fixture.ts
import { test as base, Page } from '@playwright/test';

type PerformanceMetrics = {
  LCP: number;
  CLS: number;
  INP: number;
  TTFB: number;
  FCP: number;
};

type PerformanceFixtures = {
  measureCWV: (page: Page) => Promise<PerformanceMetrics>;
};

// ...
```

### Using the Performance Fixture

```typescript
// e2e/tests/performance/homepage-cwv.spec.ts
import { test } from '../../fixtures/performance.fixture';
import { expect } from '@playwright/test';
import budget from '../../performance-budget.json';

test.describe('Homepage Performance', () => {
  test('meets Core Web Vitals targets', async ({ page, measureCWV }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const metrics = await measureCWV(page);

    // Assert against budget
    expect(metrics.LCP).toBeLessThanOrEqual(budget.metrics.LCP.target);
    expect(metrics.CLS).toBeLessThanOrEqual(budget.metrics.CLS.target);
// ...
```

### Navigation Timing API

```typescript
// e2e/utils/perf-helpers.ts
import { Page } from '@playwright/test';

export async function getNavigationTiming(page: Page) {
  return page.evaluate(() => {
    const timing = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    return {
      TTFB: timing.responseStart - timing.requestStart,
      FCP: performance.getEntriesByType('paint')
        .find(e => e.name === 'first-contentful-paint')?.startTime ?? 0,
      DOMContentLoaded: timing.domContentLoadedEventEnd - timing.startTime,
      Load: timing.loadEventEnd - timing.startTime,
      DNS: timing.domainLookupEnd - timing.domainLookupStart,
      TLS: timing.connectEnd - timing.secureConnectionStart,
      TransferSize: timing.transferSize,
// ...
```

---

## Lighthouse CI Integration

### Installation & Configuration

```bash
npm install -D @lhci/cli
```

```json
// lighthouserc.json
{
  "ci": {
    "collect": {
      "url": [
        "http://localhost:3000/",
        "http://localhost:3000/login",
        "http://localhost:3000/dashboard"
      ],
      "numberOfRuns": 3,
      "startServerCommand": "npm run start",
      "startServerReadyPattern": "ready on"
    },
    "assert": {
      "assertions": {
// ...
```

### GitHub Actions Integration

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
# ...
```

### Playwright + Lighthouse Combined

```typescript
// e2e/tests/performance/lighthouse.spec.ts
import { test, expect } from '@playwright/test';
import { execSync } from 'child_process';
import fs from 'fs';

test('Lighthouse score meets threshold', async ({ page }) => {
  // Navigate first to warm up
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // Run Lighthouse via CLI
  const url = page.url();
  execSync(`npx lhci collect --url="${url}" --numberOfRuns=1`, {
    stdio: 'pipe',
  });
// ...
```

---

## Performance Regression Detection

### Baseline Comparison

```typescript
// e2e/utils/perf-baseline.ts
import fs from 'fs';
import path from 'path';

const BASELINE_PATH = path.join(__dirname, '../.perf-baseline.json');
const THRESHOLD_PERCENT = 10; // Allow 10% degradation

interface PerfBaseline {
  [page: string]: {
    LCP: number;
    CLS: number;
    TTFB: number;
    FCP: number;
    timestamp: string;
  };
// ...
```

### CI Regression Workflow

```typescript
// e2e/tests/performance/regression.spec.ts
import { test, expect } from '@playwright/test';
import { getNavigationTiming } from '../../utils/perf-helpers';
import { loadBaseline, checkRegression } from '../../utils/perf-baseline';

const baseline = loadBaseline();
const PAGES = ['/', '/dashboard', '/checkout'];

for (const pagePath of PAGES) {
  test(`no performance regression on ${pagePath}`, async ({ page }) => {
    await page.goto(pagePath);
    await page.waitForLoadState('networkidle');

    const timing = await getNavigationTiming(page);

// ...
```

---

## Resource Loading Analysis

### Bundle Size Monitoring

```typescript
// e2e/tests/performance/resources.spec.ts
import { test, expect } from '@playwright/test';
import budget from '../../performance-budget.json';

test('page resources within budget', async ({ page }) => {
  const responses: { url: string; size: number; type: string }[] = [];

  page.on('response', async (response) => {
    const url = response.url();
    const headers = response.headers();
    const size = parseInt(headers['content-length'] || '0', 10);
    const type = headers['content-type'] || '';

    responses.push({ url, size, type });
  });
// ...
```

### Request Count Monitoring

```typescript
test('no excessive API calls on page load', async ({ page }) => {
  const apiCalls: string[] = [];

  page.on('request', (request) => {
    if (request.url().includes('/api/')) {
      apiCalls.push(request.url());
    }
  });

  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');

  // Detect N+1 API call patterns
  const urlCounts = apiCalls.reduce<Record<string, number>>((acc, url) => {
    const path = new URL(url).pathname;
// ...
```

---

## Performance Quick Reference

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| **LCP** | ≤ 2.5s | web-vitals + `page.evaluate()` |
| **CLS** | ≤ 0.1 | web-vitals + `page.evaluate()` |
| **INP** | ≤ 200ms | web-vitals + `page.evaluate()` |
| **TTFB** | ≤ 800ms | Navigation Timing API |
| **FCP** | ≤ 1.8s | Navigation Timing API |
| **Bundle (JS)** | Per budget | `page.on('response')` |
| **Total Weight** | Per budget | `page.on('response')` |

## Handoff to Bolt

When Voyager detects performance issues, hand off to Bolt for code-level optimization with:
- metric name and measured value
- target or budget
- affected page or journey
- evidence such as traces, Lighthouse output, HAR files, or screenshots
- suspected bottleneck when known
