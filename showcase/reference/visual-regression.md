# Visual Regression Testing

Strategies and tooling for visual regression testing with Storybook and React Cosmos.

---

## Strategy Comparison

| Tool | Cost | CI Integration | Storybook Support | Cosmos Support | Best For |
|------|------|----------------|-------------------|----------------|----------|
| **Chromatic** | Paid (free tier) | Excellent | Native | ❌ | Design systems |
| **Playwright** | Free | Manual setup | Via test runner | Via export | Budget-conscious |
| **Percy** | Paid | Good | Via addon | ❌ | Enterprise |
| **Loki** | Free | Manual setup | Native | ❌ | Local testing |
| **Lost Pixel** | Free (OSS) | GitHub Action | Via URL | Via URL | Open source projects |

---

## Chromatic Setup

### Installation & Configuration

```typescript
// .storybook/main.ts
export default {
  addons: ['@chromatic-com/storybook'],
};
```

```json
// package.json
{
  "scripts": {
    "chromatic": "chromatic --project-token=$CHROMATIC_PROJECT_TOKEN",
    "chromatic:ci": "chromatic --exit-zero-on-changes --auto-accept-changes main"
  }
}
```

### GitHub Actions Workflow

```yaml
# .github/workflows/chromatic.yml
name: Chromatic
on: push

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
      - run: npm ci
      - uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          exitZeroOnChanges: true
```

### Chromatic Best Practices

```typescript
// Skip animations to avoid flaky tests
export const AnimatedButton: Story = {
  parameters: {
    chromatic: {
      disableSnapshot: false,
      delay: 300, // Wait for animation to settle
      diffThreshold: 0.063, // Tolerance for sub-pixel rendering
    },
  },
};

// Capture multiple viewports
export const Responsive: Story = {
  parameters: {
    chromatic: {
      viewports: [320, 768, 1200],
    },
  },
};

// Skip flaky stories
export const AnimatedLoader: Story = {
  parameters: {
    chromatic: { disableSnapshot: true },
  },
};
```

---

## Playwright Visual Testing

### Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './visual-tests',
  snapshotDir: './visual-tests/__snapshots__',
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,
      threshold: 0.2,
    },
  },
  use: {
    baseURL: 'http://localhost:6006', // Storybook URL
  },
  webServer: {
    command: 'npm run storybook -- --ci',
    port: 6006,
    reuseExistingServer: !process.env.CI,
  },
});
```

### Visual Test Examples

```typescript
// visual-tests/button.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Button visual tests', () => {
  test('default state', async ({ page }) => {
    await page.goto('/iframe.html?id=components-button--default');
    await expect(page.locator('.sb-show-main')).toHaveScreenshot('button-default.png');
  });

  test('all variants', async ({ page }) => {
    await page.goto('/iframe.html?id=components-button--all-variants');
    await expect(page.locator('.sb-show-main')).toHaveScreenshot('button-variants.png');
  });

  test('hover state', async ({ page }) => {
    await page.goto('/iframe.html?id=components-button--default');
    await page.locator('button').hover();
    await expect(page.locator('.sb-show-main')).toHaveScreenshot('button-hover.png');
  });

  test('dark mode', async ({ page }) => {
    await page.goto('/iframe.html?id=components-button--dark-mode');
    await expect(page.locator('.sb-show-main')).toHaveScreenshot('button-dark.png');
  });
});
```

### Responsive Visual Testing

```typescript
// visual-tests/responsive.spec.ts
import { test, expect, devices } from '@playwright/test';

const viewports = [
  { name: 'mobile', ...devices['iPhone 13'] },
  { name: 'tablet', ...devices['iPad'] },
  { name: 'desktop', viewport: { width: 1280, height: 720 } },
];

for (const device of viewports) {
  test(`Card component - ${device.name}`, async ({ browser }) => {
    const context = await browser.newContext(device);
    const page = await context.newPage();
    await page.goto('/iframe.html?id=components-card--default');
    await expect(page.locator('.sb-show-main')).toHaveScreenshot(
      `card-${device.name}.png`
    );
    await context.close();
  });
}
```

---

## Storybook Test Runner

### Configuration

```typescript
// .storybook/test-runner.ts
import type { TestRunnerConfig } from '@storybook/test-runner';
import { toMatchImageSnapshot } from 'jest-image-snapshot';

const config: TestRunnerConfig = {
  setup() {
    expect.extend({ toMatchImageSnapshot });
  },
  async postVisit(page, context) {
    const image = await page.screenshot();
    expect(image).toMatchImageSnapshot({
      customSnapshotsDir: `__snapshots__/${context.id}`,
      customSnapshotIdentifier: context.name,
      failureThreshold: 0.01,
      failureThresholdType: 'percent',
    });
  },
};

export default config;
```

```json
// package.json
{
  "scripts": {
    "test-storybook": "test-storybook",
    "test-storybook:ci": "test-storybook --coverage --browsers chromium",
    "test-storybook:visual": "test-storybook --tags='visual-test'"
  }
}
```

---

## Tags for Visual Testing

```typescript
// Include in visual regression
const meta = {
  component: Button,
  tags: ['autodocs', 'visual-test'],
} satisfies Meta<typeof Button>;

// Exclude specific story (animation causes flaky tests)
export const Animated: Story = {
  tags: ['!visual-test'],
  args: { animated: true },
};

// Run only visual tests:
// test-storybook --tags="visual-test"
```

---

## Visual Test Workflow

```
1. Baseline Capture
   └─ First run creates __snapshots__/

2. Development
   └─ Run local visual tests to catch regressions

3. PR Check
   └─ CI compares against baseline
   └─ Fails if unexpected visual changes

4. Review
   └─ Visual diffs in PR (Chromatic/Percy dashboard)
   └─ Accept or reject changes

5. Update Baseline
   └─ Merge updates snapshots for main branch
```

---

## CI/CD Integration

### GitHub Actions (Playwright Visual Tests)

```yaml
# .github/workflows/visual-tests.yml
name: Visual Regression
on: pull_request

jobs:
  visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install chromium
      - run: npm run build-storybook
      - run: npx http-server storybook-static -p 6006 &
      - run: npx wait-on http://localhost:6006
      - run: npx playwright test visual-tests/
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: visual-diffs
          path: visual-tests/__snapshots__/*-diff.png
```

### Lost Pixel (Free OSS Alternative)

```json
// lostpixel.config.ts
import { CustomProjectConfig } from 'lost-pixel';

export const config: CustomProjectConfig = {
  storybookShots: {
    storybookUrl: './storybook-static',
  },
  generateOnly: true,
  failOnDifference: true,
};
```

## Storybook Test Widget (Storybook 9)

Storybook 9 adds a built-in Test Widget that runs all story tests in watch mode.

### Setup

```typescript
// .storybook/main.ts (Storybook 9)
export default {
  addons: ['@storybook/experimental-addon-test'],
};
```

### CI Workflow

```yaml
# .github/workflows/storybook-tests.yml
name: Storybook Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npm run build-storybook -- --quiet
      - name: Serve and test
        run: |
          npx concurrently -k -s first \
            "npx http-server storybook-static --port 6006 --silent" \
            "npx wait-on tcp:6006 && npm run test-storybook"
```
