# E2E Debug & Monitoring

Purpose: Use this file when Voyager must explain, reproduce, or stabilize failing browser tests.

Contents:
- HAR capture and replay
- Console, trace, CPU, and coverage diagnostics
- Slow-test analytics and retry strategy

---

## HAR Analysis

### Recording HAR Files

```typescript
// e2e/fixtures/har.fixture.ts
import { test as base, BrowserContext } from '@playwright/test';
import path from 'path';

export const test = base.extend<{ harContext: BrowserContext }>({
  harContext: async ({ browser }, use, testInfo) => {
    const harPath = path.join(testInfo.outputDir, 'network.har');

    const context = await browser.newContext({
      recordHar: {
        path: harPath,
        mode: 'full',
        urlFilter: /\/(api|graphql)\//,
      },
    });
// ...
```

### Replaying from HAR

```typescript
test('replays API responses from HAR', async ({ page }) => {
  // Use recorded HAR for deterministic responses
  await page.routeFromHAR('e2e/fixtures/recorded.har', {
    url: '**/api/**',
    update: false, // Set true to update HAR
    notFound: 'fallback', // Fall back to network if not in HAR
  });

  await page.goto('/dashboard');
  await expect(page.getByTestId('data-loaded')).toBeVisible();
});
```

### Failure Network Analysis

```typescript
// e2e/fixtures/network-logger.fixture.ts
import { test as base, Page } from '@playwright/test';

type NetworkLog = {
  url: string;
  method: string;
  status: number;
  duration: number;
  size: number;
};

export const test = base.extend<{ networkLogs: NetworkLog[] }>({
  networkLogs: async ({ page }, use, testInfo) => {
    const logs: NetworkLog[] = [];

// ...
```

## Browser Console Error Detection

### Auto-Collection Fixture

```typescript
// e2e/fixtures/console.fixture.ts
import { test as base, ConsoleMessage } from '@playwright/test';

type ConsoleFixture = {
  consoleErrors: ConsoleMessage[];
  consoleWarnings: ConsoleMessage[];
};

export const test = base.extend<ConsoleFixture>({
  consoleErrors: async ({ page }, use, testInfo) => {
    const errors: ConsoleMessage[] = [];

    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg);
// ...
```

### Auto-Fail on Console Errors

```typescript
// e2e/fixtures/strict-console.fixture.ts
import { test as base, expect } from '@playwright/test';

export const test = base.extend<{ strictConsole: void }>({
  strictConsole: [async ({ page }, use) => {
    const errors: string[] = [];

    // Allowlist known non-critical errors
    const allowlist = [
      'ResizeObserver loop',
      'favicon.ico',
      'chrome-extension://',
    ];

    page.on('console', (msg) => {
// ...
```

---

## Trace Viewer Integration

### Advanced Trace Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    trace: {
      mode: 'on-first-retry',
      screenshots: true,
      snapshots: true,
      sources: true,
    },
  },
});
```

### Custom Annotations

```typescript
test('checkout flow with annotations', async ({ page }, testInfo) => {
  // Add custom annotations to trace
  await testInfo.attach('test-context', {
    body: JSON.stringify({
      testUser: 'user@test.com',
      environment: process.env.NODE_ENV,
      timestamp: new Date().toISOString(),
    }),
    contentType: 'application/json',
  });

  await test.step('Navigate to cart', async () => {
    await page.goto('/cart');
    await expect(page.getByTestId('cart-items')).toBeVisible();
  });
// ...
```

### Trace on Every Failure

```typescript
// e2e/fixtures/trace.fixture.ts
import { test as base } from '@playwright/test';

export const test = base.extend({
  page: async ({ page, context }, use, testInfo) => {
    // Start tracing for every test
    if (process.env.TRACE_ALL) {
      await context.tracing.start({ screenshots: true, snapshots: true });
    }

    await use(page);

    // Save trace on failure
    if (testInfo.status !== 'passed' && process.env.TRACE_ALL) {
      const tracePath = testInfo.outputPath('trace.zip');
// ...
```

---

## CPU / Memory Profiling

### CDP Integration

```typescript
// e2e/tests/performance/memory.spec.ts
import { test, expect } from '@playwright/test';

test('no memory leaks on repeated navigation', async ({ page }) => {
  const client = await page.context().newCDPSession(page);

  // Take initial heap snapshot
  await client.send('HeapProfiler.enable');
  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');

  const initialMetrics = await page.evaluate(() => ({
    jsHeapSize: (performance as any).memory?.usedJSHeapSize,
  }));

// ...
```

### JS Coverage Analysis

```typescript
test('JavaScript coverage meets minimum', async ({ page }) => {
  await page.coverage.startJSCoverage();
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // Interact with key features
  await page.getByTestId('nav-products').click();
  await page.waitForURL('**/products');

  const coverage = await page.coverage.stopJSCoverage();

  // Calculate usage ratio
  let totalBytes = 0;
  let usedBytes = 0;

// ...
```

---

## Test Execution Analytics

### Slowest Test Identification

```typescript
// e2e/reporters/slow-test-reporter.ts
import type { FullResult, Reporter, TestCase, TestResult } from '@playwright/test/reporter';

class SlowTestReporter implements Reporter {
  private results: { title: string; duration: number; file: string }[] = [];

  onTestEnd(test: TestCase, result: TestResult) {
    this.results.push({
      title: test.title,
      duration: result.duration,
      file: test.location.file,
    });
  }

  onEnd(result: FullResult) {
// ...
```

### Flaky Rate Tracking

```typescript
// e2e/reporters/flaky-tracker.ts
import type { Reporter, TestCase, TestResult } from '@playwright/test/reporter';
import fs from 'fs';

class FlakyTracker implements Reporter {
  private flakyTests: { title: string; file: string; retries: number }[] = [];

  onTestEnd(test: TestCase, result: TestResult) {
    if (result.status === 'passed' && result.retry > 0) {
      this.flakyTests.push({
        title: test.title,
        file: test.location.file,
        retries: result.retry,
      });
    }
// ...
```

---

## Smart Retry Strategies

### Conditional Retry

```typescript
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
});
```

### Custom Retry Logic

```typescript
// e2e/utils/retry-helpers.ts
import { test, expect } from '@playwright/test';

/**
 * Retry with exponential backoff for external service checks.
 */
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  options: { maxRetries?: number; baseDelay?: number } = {},
): Promise<T> {
  const { maxRetries = 3, baseDelay = 1000 } = options;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
// ...
```

### Per-Test Retry Override

```typescript
test.describe('Stable tests', () => {
  test.describe.configure({ retries: 0 });

  test('deterministic test', async ({ page }) => {
    // No retries - must pass first time
  });
});

test.describe('External service tests', () => {
  test.describe.configure({ retries: 3 });

test('third-party API test', async ({ page }) => {
    // Extra retries for external dependencies
  });
});
```
