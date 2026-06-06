# Playwright Patterns

Purpose: Default implementation patterns for Playwright-based Voyager work.

Contents:
- Project setup, Page Objects, and authentication state
- Waits, data setup, sharding, and tag-based execution
- Modern Playwright APIs, mocking, cross-browser coverage, and flake prevention

---

## Project Setup

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results.json' }],
    process.env.CI ? ['github'] : ['list'],
  ],
  use: {
// ...
```

### Directory Structure

```
e2e/
├── fixtures/
│   ├── test-data.ts        # Test data factory
│   └── index.ts            # Custom fixtures
├── pages/
│   ├── base.page.ts        # Base page class
│   ├── login.page.ts       # Login page
│   ├── home.page.ts        # Home page
│   └── checkout.page.ts    # Checkout page
├── tests/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── signup.spec.ts
│   ├── checkout/
│   │   └── purchase.spec.ts
...
```

## Page Object Model

### Base Page Class

```typescript
// e2e/pages/base.page.ts
import { Page, Locator, expect } from '@playwright/test';

export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async goto(path: string = '') {
    await this.page.goto(path);
  }

  async waitForPageLoad() {
// ...
```

### Page Implementation

```typescript
// e2e/pages/login.page.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './base.page';

export class LoginPage extends BasePage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = this.getByTestId('email-input');
    this.passwordInput = this.getByTestId('password-input');
    this.submitButton = this.getByTestId('login-submit');
// ...
```

### Component Page Object

```typescript
// e2e/pages/components/header.component.ts
import { Page, Locator } from '@playwright/test';

export class HeaderComponent {
  readonly page: Page;
  readonly userMenu: Locator;
  readonly logoutButton: Locator;
  readonly notificationBell: Locator;

  constructor(page: Page) {
    this.page = page;
    this.userMenu = page.getByTestId('user-menu');
    this.logoutButton = page.getByTestId('logout-button');
    this.notificationBell = page.getByTestId('notification-bell');
  }
// ...
```

---

## Authentication Handling

### Storage State Setup

```typescript
// e2e/auth.setup.ts
import { test as setup, expect } from '@playwright/test';
import path from 'path';

const authFile = path.join(__dirname, '.auth/user.json');

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByTestId('email-input').fill(process.env.TEST_USER_EMAIL!);
  await page.getByTestId('password-input').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByTestId('login-submit').click();
  await page.waitForURL('**/dashboard');
  await expect(page.getByTestId('user-menu')).toBeVisible();
  await page.context().storageState({ path: authFile });
});
```

### Multiple Users

```typescript
// e2e/fixtures/index.ts
import { test as base, Page } from '@playwright/test';

type TestFixtures = {
  adminPage: Page;
  userPage: Page;
};

export const test = base.extend<TestFixtures>({
  adminPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: '.auth/admin.json',
    });
    const page = await context.newPage();
    await use(page);
// ...
```

---

## Wait Strategies

### Recommended Waits

```typescript
// ✅ GOOD: Wait for specific conditions
await expect(page.getByTestId('result')).toBeVisible();
await expect(page.getByTestId('status')).toContainText('Complete');
await page.waitForURL('**/confirmation');
await page.waitForLoadState('networkidle');
await page.waitForResponse(resp =>
  resp.url().includes('/api/orders') && resp.status() === 200
);
await expect(page.getByTestId('submit')).toBeEnabled();
```

### Custom Wait Helpers

```typescript
// e2e/utils/wait-helpers.ts
import { Page, expect } from '@playwright/test';

export async function waitForToast(page: Page, message: string) {
  const toast = page.getByRole('alert');
  await expect(toast).toContainText(message);
  await expect(toast).toBeHidden({ timeout: 5000 });
}

export async function waitForModalClose(page: Page) {
  await expect(page.getByRole('dialog')).toBeHidden();
}
```

### Avoid These

```typescript
// ❌ BAD: Arbitrary timeout
await page.waitForTimeout(2000);

// ❌ BAD: Fixed delay before action
await new Promise(r => setTimeout(r, 1000));
await page.click('button');
```

---

## Test Data Management

### API-Based Setup

```typescript
// e2e/utils/api-helpers.ts
import { APIRequestContext } from '@playwright/test';

export class ApiHelpers {
  constructor(private request: APIRequestContext) {}

  async createUser(data: { email: string; name: string }) {
    const response = await this.request.post('/api/users', { data });
    return response.json();
  }

  async createProduct(data: { name: string; price: number }) {
    const response = await this.request.post('/api/products', { data });
    return response.json();
  }
// ...
```

### Test Data Factory

```typescript
// e2e/fixtures/test-data.ts
import { faker } from '@faker-js/faker/locale/ja';

export const TestData = {
  user: {
    valid: () => ({
      email: faker.internet.email(),
      password: 'Test1234!',
      name: faker.person.fullName(),
    }),
    invalid: {
      email: 'invalid-email',
      password: '123',
    },
  },
// ...
```

---

## Parallel Execution

### Sharding Configuration

```bash
# Run sharded: npx playwright test --shard=1/4
```

> See `ci-reporting.md` → "Sharded CI" for full GitHub Actions sharding workflow.

### Test Isolation

```typescript
// ✅ GOOD: Tests are independent
test.describe('User Management', () => {
  test('can create user', async ({ page, request }) => {
    const user = TestData.user.valid();
    // ... test with unique data
  });

  test('can delete user', async ({ page, request }) => {
    // Create own test data, don't depend on previous test
    const api = new ApiHelpers(request);
    const user = await api.createUser(TestData.user.valid());
    // ... test deletion
  });
});
```

---

## Playwright Modern Features (1.49 baseline)

> Version map (as of 2026-05): **1.60 (May 2026 — current)**, 1.59 (Apr 2026), 1.58 (Mar 2026), 1.57 (Jan 2026), 1.56 (Nov 2025). Pin `@playwright/test` `^1.59` if your project already depends on screencast / browser-bind / `playwright-cli` flows; pin `^1.60` if you need HAR tracing or `locator.drop()`. Treat 1.56 as the floor for Test Agents (Planner / Generator / Healer).

### Clock API (Fake Timers)

```typescript
// Control time for animations, timers, and date-dependent UI
test('shows countdown timer', async ({ page }) => {
  // Install fake timers
  await page.clock.install({ time: new Date('2024-12-31T23:59:00') });

  await page.goto('/countdown');
  await expect(page.getByTestId('timer')).toContainText('1:00');

  // Advance time by 30 seconds
  await page.clock.fastForward(30000);
  await expect(page.getByTestId('timer')).toContainText('0:30');

  // Jump to midnight
  await page.clock.setFixedTime(new Date('2025-01-01T00:00:00'));
  await expect(page.getByTestId('celebration')).toBeVisible();
// ...
```

### expect.configure (Soft Assertions)

```typescript
// Collect all failures instead of stopping at first
test('dashboard shows all widgets', async ({ page }) => {
  const softExpect = expect.configure({ soft: true });

  await page.goto('/dashboard');

  // All assertions run even if some fail
  await softExpect(page.getByTestId('revenue-widget')).toBeVisible();
  await softExpect(page.getByTestId('users-widget')).toBeVisible();
  await softExpect(page.getByTestId('orders-widget')).toBeVisible();
  await softExpect(page.getByTestId('chart-widget')).toBeVisible();

  // Custom timeout per assertion group
  const slowExpect = expect.configure({ timeout: 10000 });
  await slowExpect(page.getByTestId('analytics-loaded')).toBeVisible();
// ...
```

### Viewport Assertions (toBeInViewport)

```typescript
test('lazy-loaded images appear on scroll', async ({ page }) => {
  await page.goto('/gallery');

  const thirdImage = page.getByTestId('image-3');

  // Not in viewport initially
  await expect(thirdImage).not.toBeInViewport();

  // Scroll down
  await thirdImage.scrollIntoViewIfNeeded();

  // Now visible in viewport
  await expect(thirdImage).toBeInViewport();
  await expect(thirdImage).toBeInViewport({ ratio: 0.5 }); // At least 50% visible
});
```

### API Testing Integration

```typescript
import { test, expect } from '@playwright/test';

// Mix UI and API tests in the same suite
test('API: create user then verify in UI', async ({ page, request }) => {
  // API step: create user
  const response = await request.post('/api/users', {
    data: { name: 'E2E User', email: 'e2e@example.com' },
  });
  expect(response.ok()).toBeTruthy();
  const user = await response.json();

  // UI step: verify user appears in admin panel
  await page.goto('/admin/users');
  await expect(page.getByText('E2E User')).toBeVisible();

// ...
```

### Component Testing (Experimental)

```typescript
// playwright-ct.config.ts
import { defineConfig } from '@playwright/experimental-ct-react';

export default defineConfig({
  testDir: './src',
  testMatch: '**/*.pw.tsx',
  use: {
    ctPort: 3100,
  },
});

// src/components/Button.pw.tsx
import { test, expect } from '@playwright/experimental-ct-react';
import { Button } from './Button';

// ...
```

---

## Cross-Browser Testing

### Browser Matrix

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    // CI: All browsers
    ...(process.env.CI ? [
      { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
      { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
      { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    ] : [
      // Local: Chrome only for speed
      { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    ]),
  ],
});
```

### Mobile Testing

```typescript
test.describe('Mobile', () => {
  test.use({ ...devices['iPhone 12'] });

  test('mobile navigation works', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByTestId('mobile-menu')).toBeVisible();
    await expect(page.getByTestId('desktop-nav')).toBeHidden();
  });
});
```

---

## API Mocking & Interception

### Mock API Responses

```typescript
test('handles API error gracefully', async ({ page }) => {
  await page.route('**/api/products', route =>
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Server error' }),
    })
  );

  await page.goto('/products');
  await expect(page.getByTestId('error-message')).toBeVisible();
});
```

### Intercept and Modify

```typescript
test('modifies API response', async ({ page }) => {
  await page.route('**/api/user', async route => {
    const response = await route.fetch();
    const json = await response.json();
    json.isPremium = true;
    await route.fulfill({ response, json });
  });

  await page.goto('/dashboard');
  await expect(page.getByTestId('premium-badge')).toBeVisible();
});
```

---

## Flaky Test Prevention

### Common Causes & Solutions

| Cause | Symptom | Solution |
|-------|---------|----------|
| **Timing issues** | Random failures | Use proper waits, not timeouts |
| **Shared state** | Fails when parallel | Isolate test data |
| **Animation** | Screenshot diffs | Disable animations |
| **Network** | Timeout errors | Mock/intercept APIs |
| **Order dependency** | Fails in isolation | Make tests independent |
| **Race conditions** | Intermittent failures | Wait for specific conditions |

### Retry Configuration

> See `debug-monitoring.md` → "Smart Retry Strategies" for retry configuration, conditional retry, and per-test overrides.

### Flaky Test Investigation

```typescript
// Run test multiple times: npx playwright test --repeat-each=10 tests/checkout.spec.ts
test.describe('Flaky Investigation', () => {
  test.use({ trace: 'on', video: 'on' });

  test('potentially flaky test', async ({ page }, testInfo) => {
    console.log(`Attempt: ${testInfo.retry + 1}`);
    page.on('console', msg => console.log(msg.text()));

    // Add visual markers in video for debugging
    await page.evaluate((attempt) => {
      const marker = document.createElement('div');
      marker.style.cssText = 'position:fixed;top:0;left:0;background:red;color:white;padding:10px;z-index:99999';
      marker.textContent = `Attempt ${attempt}`;
      document.body.appendChild(marker);
    }, testInfo.retry + 1);
// ...
```

---

## Test Execution Optimization

### Tag-Based Prioritization

```typescript
// Tag tests by priority
test('@critical: user can complete checkout', async ({ page }) => {
  // Business-critical path
});

test('@smoke: homepage loads', async ({ page }) => {
  // Smoke test - quick verification
});

test('@regression: restored cart survives page reload', async ({ page }) => {
  // Regression test for specific bug
});
```

```bash
# Run by tag
npx playwright test --grep @critical        # Critical only
npx playwright test --grep @smoke           # Smoke tests
npx playwright test --grep-invert @regression  # Exclude regression
```

### Parallel vs Sequential Decision

| Scenario | Strategy | Config |
|----------|----------|--------|
| Independent CRUD tests | **Parallel** | `fullyParallel: true` |
| Shared resource (single DB user) | **Sequential** | `test.describe.configure({ mode: 'serial' })` |
| State machine flow | **Sequential** | Steps depend on prior state |
| Cross-browser same test | **Parallel** | Different projects, same tests |

---

## Playwright 1.50+ Features

### Aria Snapshots (Stable)

```typescript
// Verify accessible structure of components
test('navigation has correct aria structure', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('navigation')).toMatchAriaSnapshot(`
    - navigation:
      - link "Home"
      - link "Products"
      - link "About"
      - link "Contact"
  `);
});

test('form has accessible labels', async ({ page }) => {
  await page.goto('/signup');
// ...
```

### toPass (Polling-Based Assertions)

```typescript
// Retry assertion until it passes (polling)
test('data syncs eventually', async ({ page }) => {
  await page.goto('/dashboard');

  // Poll until condition is met (default 5s timeout)
  await expect(async () => {
    const count = await page.getByTestId('item-count').textContent();
    expect(Number(count)).toBeGreaterThan(0);
  }).toPass({ timeout: 10000, intervals: [500, 1000, 2000] });
});

test('external service responds', async ({ request }) => {
  await expect(async () => {
    const response = await request.get('/api/external-status');
    expect(response.ok()).toBeTruthy();
// ...
```

### Box Model Assertions

```typescript
test('sidebar has correct dimensions', async ({ page }) => {
  await page.goto('/dashboard');

  const sidebar = page.getByTestId('sidebar');
  await expect(sidebar).toHaveCSS('width', '280px');

  const box = await sidebar.boundingBox();
  expect(box!.width).toBe(280);
  expect(box!.height).toBeGreaterThan(500);
});

test('modal is centered on screen', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('open-modal').click();

// ...
```

### Route.fetch Improvements

```typescript
test('modifies response headers', async ({ page }) => {
  await page.route('**/api/**', async (route) => {
    const response = await route.fetch();
    const headers = response.headers();

    await route.fulfill({
      response,
      headers: { ...headers, 'x-test-mode': 'true' },
    });
  });

  await page.goto('/dashboard');
});

test('conditional response modification', async ({ page }) => {
// ...
```

---

## Playwright v1.51 Features

### locator.filter({ visible: true })

```typescript
// Filter locators to only visible elements
test('only visible items are interactable', async ({ page }) => {
  await page.goto('/list');

  // Get all items, then filter to visible ones only
  const visibleItems = page.getByRole('listitem').filter({ visible: true });
  const count = await visibleItems.count();

  expect(count).toBeGreaterThan(0);
  await visibleItems.first().click();
});
```

### Component Testing Package Changes (v1.51)

As of v1.51, the following CT packages are in maintenance mode (no new features):
- `@playwright/experimental-ct-vue2` — maintenance only
- `@playwright/experimental-ct-solid` — maintenance only

Active packages: `@playwright/experimental-ct-react`, `@playwright/experimental-ct-vue`, `@playwright/experimental-ct-svelte`

---

## Playwright v1.52 Features

### Aria Snapshot Enhancements

```typescript
// /children option — assert partial aria tree
test('form contains required fields', async ({ page }) => {
  await page.goto('/signup');

  await expect(page.locator('form')).toMatchAriaSnapshot(`
    - form:
      /children: contain
      - textbox "Email"
      - textbox "Password"
  `);
});

// /url option — verify link URLs
test('nav links have correct hrefs', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('navigation')).toMatchAriaSnapshot(`
    - navigation:
      - link "Home" [/url: "/"]
      - link "Docs" [/url: "/docs"]
  `);
});

// ref option — reference elements for assertions
test('aria ref usage', async ({ page }) => {
  await page.goto('/dashboard');

  await expect(page.locator('.sidebar')).toMatchAriaSnapshot(`
    - navigation [ref=mainNav]:
      - link "Dashboard"
      - link "Settings"
  `);
});
```

### testProject.workers

```typescript
// playwright.config.ts — per-project worker override
export default defineConfig({
  workers: 4, // global default
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
      workers: 1, // Safari is resource-intensive — limit concurrency
    },
  ],
});
```

### failOnFlakyTests

```typescript
// playwright.config.ts — fail CI if any test is detected as flaky
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  failOnFlakyTests: !!process.env.CI, // Treat flaky as failure in CI
});
```

> `failOnFlakyTests: true` causes the run to exit with a non-zero code when any test passes on retry. Use this in CI to prevent flaky tests from silently masking instability.

---

## Playwright v1.56 Features — Test Agents (Planner / Generator / Healer)

Released 2025-11. Introduces the agentic test-authoring loop that Voyager now treats as the default Playwright authoring pattern for AI-driven workflows.

```bash
# 1. Planner — explores the running app and emits a Markdown plan
npx playwright test --plan "Test the login flow"
#   -> specs/login.md

# 2. Generator — turns the plan into a real test file
npx playwright test --generate
#   -> tests/login.spec.ts

# 3. Run + Heal — Healer either repairs the test or files a bug
npx playwright test
npx playwright test --heal

# 4. Full loop — plan -> generate -> run -> heal, repeated
npx playwright test --loop
```

Companion observability APIs shipped alongside agents:

```typescript
// Read structured runtime signals from inside a test without instrumenting console.log
const messages = page.consoleMessages();   // structured console events
const errors   = page.pageErrors();        // uncaught exceptions
const requests = page.requests();          // navigation + fetch requests

// UI Mode also gains snapshot-update controls and single-worker execution for agents.
```

> Adopt agents **after** the suite already has stable auth, locators, fixtures, and a review gate. See `ai-powered-e2e-testing.md` for the adoption ladder.

---

## Playwright v1.57 Features — Chrome for Testing + Speedboard

Released 2026-01.

- **Default channel switched to Chrome for Testing** (`chrome-headless-shell` in headless). Affects memory footprint in constrained CI runners; pin `channel: 'chromium'` if reproducibility or memory ceilings are hard requirements. Arm64 Linux still defaults to Chromium.
- **HTML report Speedboard** ranks tests by execution time — use it before reaching for sharding.
- **`webServer.wait`** accepts a regex against stdout/stderr so config can wait for the framework's actual ready message instead of polling a URL.
- **Service Worker network event routing + console message support** — fixes a long-standing blind spot for PWA / offline test coverage.

```typescript
// playwright.config.ts
export default defineConfig({
  webServer: {
    command: 'pnpm dev',
    url: 'http://localhost:3000',
    wait: /ready in \d+ms/, // 1.57+ regex on dev-server stdout
    reuseExistingServer: !process.env.CI,
  },
  use: {
    channel: 'chromium', // pin if Chrome for Testing memory footprint is a problem
  },
});
```

---

## Playwright v1.58 Features — Timeline + CLI Foundations

Released 2026-03.

- **Timeline tab in the HTML report Speedboard** — visualises wait bottlenecks and slow phases per test. Read this before adding shards or workers.
- **Playwright CLI (`@playwright/cli`)** lands as an agent-friendly entry point. Snapshots and screenshots are written to disk and selectively read by the agent — measured around **~27 K tokens per task vs ~114 K via MCP** (≈4× reduction, up to 10× on longer sessions). Microsoft's 2026 guidance now prefers CLI over MCP for coding-agent integration.
- **Removed**: legacy `_react` / `_vue` engine selectors, the `devtools` launch option, and the long-deprecated `Page#accessibility` API. Migrate to `getByRole` / `getByLabel` and to `page.accessibility.snapshot()` replacements via `toMatchAriaSnapshot`.

```bash
# Agent-friendly CLI usage
npx playwright-cli show                # dashboard of bound browsers
npx playwright-cli test --debug=cli    # attach a CLI debugger an agent can drive
```

---

## Playwright v1.59 Features — Screencast + Browser Bind

Released 2026-04. The release that turned Playwright into a first-class substrate for agentic workflows.

### page.screencast — Agentic Video Receipts

```typescript
test('checkout — receipt video', async ({ page }) => {
  const screencast = await page.screencast.start({
    path: 'artifacts/checkout.webm',
    showActions: true,           // highlights clicked / typed elements
  });

  await screencast.showChapter('Cart review');
  await page.getByRole('button', { name: 'Checkout' }).click();

  await screencast.showChapter('Payment');
  await page.getByLabel('Card number').fill('4242424242424242');
  await page.getByRole('button', { name: 'Pay' }).click();

  await screencast.showOverlay({ html: '<h1>Done</h1>' });
  await screencast.stop();
});
```

> `recordVideo` still records the whole test. `page.screencast` gives the agent precise start/stop, action annotations, chapter overlays, and live frame streaming for vision models — use it when you need a reviewable artefact, not raw playback.

### browser.bind + playwright-cli show — Distributed Observability

```typescript
// Long-lived browser an external CLI / MCP / agent can attach to
const browser = await chromium.launch();
await browser.bind({ name: 'voyager-shared-chrome' });
// `playwright-cli show` lists every bound browser across hosts.
```

### Trace exploration from the command line

```bash
# Parse a trace without a UI — agent- and CI-friendly
npx playwright trace path/to/trace.zip --json | jq '.actions[]'
# Inspect a single step interactively from CLI
npx playwright trace path/to/trace.zip --action=42
```

### New locator + snapshot APIs

```typescript
// Describe locators in traces / reports (improves debug readability)
const submit = page.getByRole('button', { name: 'Submit' }).describe('checkout-submit');
console.log(await submit.description()); // 'checkout-submit'

// Match accessible description directly
await expect(page.getByRole('img', { description: 'Profile photo' })).toBeVisible();

// Snapshot the live accessibility tree
const aria = await page.ariaSnapshot();

// Normalise text (whitespace / case) for assertions
await expect(page.getByTestId('total').normalize()).toHaveText('JPY 1,200');

// Interactive locator picker (replaces deprecated `Page.pause` flows)
await page.pickLocator();

// Reset / replace storage state mid-test
await context.setStorageState({ cookies: [], origins: [] });
```

### Async disposables

```typescript
test('auto-cleanup with await using', async ({ browser }) => {
  await using context = await browser.newContext();
  await using page    = await context.newPage();
  await page.goto('/dashboard');
  // context + page disposed automatically when the block exits
});
```

---

## Playwright v1.60 Features — HAR Tracing + Drop + Test Abort

Released 2026-05 (current).

### HAR as a first-class tracing primitive

```typescript
test('records HAR alongside trace', async ({ page }) => {
  await page.tracing.startHar({ path: 'artifacts/checkout.har', mode: 'minimal' });
  await page.goto('/checkout');
  await page.getByRole('button', { name: 'Pay' }).click();
  await page.tracing.stopHar();
});
```

> HAR recording is now wired into the tracing API instead of being a context-level afterthought. Pair with `trace: 'on-first-retry'` to keep CI artefacts cheap on green runs.

### locator.drop — drag-and-drop + clipboard / file

```typescript
test('drag file onto upload zone', async ({ page }) => {
  const dropZone = page.getByTestId('upload-zone');
  await dropZone.drop({
    files: ['fixtures/avatar.png'],
  });
  await expect(page.getByText('avatar.png')).toBeVisible();
});

test('reorder list via drag', async ({ page }) => {
  const itemA = page.getByRole('listitem', { name: 'Item A' });
  const itemB = page.getByRole('listitem', { name: 'Item B' });
  await itemA.drop({ target: itemB });
});
```

### Aria snapshot bounding boxes (for vision models)

```typescript
// Include each element's bounding box in the snapshot — consumed by AI agents
const snapshot = await page.ariaSnapshot({ boxes: true });
```

### test.abort — fail fast from fixtures or route handlers

```typescript
test('abort when backend signals broken contract', async ({ page }, testInfo) => {
  await page.route('**/api/health', async (route) => {
    const res = await route.fetch();
    if (res.status() === 503) {
      testInfo.abort('Backend reported permanent outage — no point retrying'); // 1.60+
    }
    return route.fulfill({ response: res });
  });

  await page.goto('/dashboard');
});
```

### Other 1.60 changes worth noting

- New cookie property `partitionKey` on `browserContext.cookies()` / `addCookies()` for partitioned-cookie save/restore.
- `apiRequest.newContext({ maxRedirects })` to cap redirect chains in API tests.
- `routeWebSocket` (introduced in 1.59, hardened in 1.60) intercepts, modifies, and mocks WebSocket frames from both `page` and `browserContext`.
- `Locator.ariaRef()` is deprecated — use `getByRole({ description })` or `toMatchAriaSnapshot` with `[ref=…]`.

---

## Component Testing — Status by Framework (2026-05)

`@playwright/experimental-ct-*` packages remain experimental. Current support tier:

| Package | Status | Notes |
|---------|--------|-------|
| `@playwright/experimental-ct-react` | Active | Primary target; works with Vite-based React 19 setups. |
| `@playwright/experimental-ct-vue` (Vue 3) | Active | Vite-based Vue 3 only. |
| `@playwright/experimental-ct-svelte` | Active | Vite-based; tracks Svelte 5 runes. |
| `@playwright/experimental-ct-vue2` | Maintenance — no new features (1.51+) | Migrate to Vue 3 or pin a 1.5x release. |
| `@playwright/experimental-ct-solid` | Maintenance — no new features (1.51+) | Same migration advice. |

See `component-testing.md` for the cross-tool comparison (Playwright CT vs Cypress CT vs Storybook Interactions).
