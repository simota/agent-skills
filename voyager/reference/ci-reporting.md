# CI/CD Integration & Reporting

Purpose: Use this file when Voyager must integrate E2E suites into CI, reporting, and artifact collection.

Contents:
- GitHub Actions workflows and sharding
- Reporters, video modes, and artifact retention
- Prioritization and performance-budget gates

---

## GitHub Actions (Playwright)

### Basic Workflow

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
# ...
```

### Sharded CI (4 Parallel Jobs)

```yaml
# .github/workflows/e2e-sharded.yml
name: E2E Tests (Sharded)

on:
  push:
    branches: [main]

jobs:
  e2e:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]

# ...
```

---

## Test Reporters

### Playwright HTML Reporter

```typescript
// playwright.config.ts
export default defineConfig({
  reporter: [
    ['html', {
      outputFolder: 'playwright-report',
      open: 'never', // 'always', 'never', 'on-failure'
    }],
    ['json', { outputFile: 'test-results.json' }],
    ['junit', { outputFile: 'test-results.xml' }], // For CI integration
    process.env.CI ? ['github'] : ['list'],
  ],
});
```

### Allure Reporter

```bash
npm install -D allure-playwright allure-commandline
```

```typescript
// playwright.config.ts
export default defineConfig({
  reporter: [
    ['allure-playwright', {
      outputFolder: 'allure-results',
      detail: true,
      suiteTitle: true,
    }],
  ],
});
```

```typescript
// e2e/tests/with-allure.spec.ts
import { test, expect } from '@playwright/test';
import { allure } from 'allure-playwright';

test('user can complete purchase', async ({ page }) => {
  await allure.epic('E-Commerce');
  await allure.feature('Checkout');
  await allure.story('Complete Purchase');
  await allure.severity('critical');

  await allure.step('Navigate to product', async () => {
    await page.goto('/products/1');
  });

  await allure.step('Add to cart', async () => {
// ...
```

```yaml
# CI: Generate and upload Allure report
- name: Generate Allure Report
  run: npx allure generate allure-results --clean -o allure-report

- name: Upload Allure Report
  uses: actions/upload-artifact@v4
  with:
    name: allure-report
    path: allure-report
```

### Custom Slack Reporter

```typescript
// e2e/reporters/slack-reporter.ts
import type { FullResult, Reporter, TestCase, TestResult } from '@playwright/test/reporter';

class SlackReporter implements Reporter {
  private failures: { test: string; error: string }[] = [];

  onTestEnd(test: TestCase, result: TestResult) {
    if (result.status === 'failed') {
      this.failures.push({
        test: test.title,
        error: result.error?.message || 'Unknown error',
      });
    }
  }

// ...
```

```typescript
// playwright.config.ts
export default defineConfig({
  reporter: [
    ['html'],
    ['./e2e/reporters/slack-reporter.ts'],
  ],
});
```

---

## Video Recording

### Configuration Options

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    video: {
      mode: 'on-first-retry', // Recommended for CI
      size: { width: 1280, height: 720 },
    },
  },
  outputDir: 'test-results/',
});
```

### Video Mode Comparison

| Mode | Description | CI Usage | Storage |
|------|-------------|----------|---------|
| `'off'` | No recording | Production runs | Minimal |
| `'on'` | Always record | Debug sessions | High |
| `'retain-on-failure'` | Keep failed only | Recommended for CI | Medium |
| `'on-first-retry'` | Record on retry | Balanced approach | Low-Medium |

### Per-Test Video Control

```typescript
// Override video mode for specific test file
test.use({ video: 'on' });

test.describe('Visual Flow Tests', () => {
  test('user signup journey', async ({ page }) => {
    // This test will always be recorded
  });
});
```

### Accessing Video in Tests

```typescript
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== 'passed') {
    const video = page.video();
    if (video) {
      const path = await video.path();
      await testInfo.attach('failure-video', {
        path: path,
        contentType: 'video/webm',
      });
    }
  }
});
```

### CI Artifact Configuration

```yaml
# Upload only on failure (saves storage)
- name: Upload test videos
  uses: actions/upload-artifact@v4
  if: failure()
  with:
    name: test-videos
    path: test-results/**/*.webm
    retention-days: 7
```

### Video Best Practices

| Practice | Description |
|----------|-------------|
| **Use `retain-on-failure` in CI** | Saves storage while keeping debug evidence |
| **720p for most tests** | Sufficient quality, reasonable file size |
| **1080p for visual regression** | When pixel detail matters |
| **Close context to finalize** | Video file incomplete until context closes |
| **Set retention policy** | CI artifacts: 7-30 days |
| **Don't record stable tests** | Disable for well-established tests |

---

## Test Prioritization in CI

### Critical-First Execution

```yaml
# .github/workflows/e2e-prioritized.yml
jobs:
  smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - name: Smoke tests (fast gate)
        run: npx playwright test --grep @smoke
        timeout-minutes: 5

  critical:
    needs: smoke
    runs-on: ubuntu-latest
# ...
```

---

## Performance Budget CI Check

### Lighthouse CI GitHub Actions

```yaml
# Add to existing e2e workflow
- name: Lighthouse CI
  run: npx lhci autorun
  env:
    LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
```

### Budget Violation PR Blocking

```json
// lighthouserc.json - assertions block PR on violation
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["error", { "minScore": 0.9 }],
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
      }
    }
  }
}
```

See `performance-testing.md` for detailed Lighthouse CI integration and performance budget configuration.
