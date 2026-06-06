# Framework Selection Guide

Purpose: Use this file when Voyager must justify Playwright, Cypress, WebdriverIO, or TestCafe for a given project.

Contents:
- Comparison matrix and decision guide
- Advanced-scenario support and modern Playwright features
- Version requirements and minimal TestCafe fallback patterns

## Framework Comparison

| Criteria | Playwright | Cypress | WebdriverIO | TestCafe |
|----------|------------|---------|-------------|----------|
| **Best for** | Cross-browser, complex flows | DX, component testing | Selenium compat, mobile | Zero-dependency |
| **Browser support** | All + mobile emulation | Chrome, Firefox, Edge | All + real mobile (Appium) | All |
| **Parallel** | Free, built-in | Paid (Cypress Cloud) | Free, built-in | Free, built-in |
| **Multi-tab/iframe** | Full support | Limited | Full support | Limited |
| **Network stubbing** | `page.route` | `cy.intercept` (excellent) | `mock` | `RequestMock` |
| **Architecture** | Out-of-process | In-browser, same-origin | WebDriver protocol | Proxy-based |
| **Learning curve** | Moderate | Low | Moderate | Low |
| **Component testing** | Experimental | Mature | Experimental | None |

## Decision Guide

```
Need cross-browser + mobile emulation? → Playwright
Need real mobile device testing (Appium)? → WebdriverIO
Team already uses Cypress? → Cypress
Need zero-dependency simplicity? → TestCafe
Starting fresh? → Playwright (recommended default)
```

See `playwright-patterns.md` for Playwright details.
See `cypress-guide.md` for Cypress details.

---

## Advanced Scenario Support

| Feature | Playwright | Cypress | WebdriverIO |
|---------|------------|---------|-------------|
| Multi-tab | ✅ Full | ❌ Limited | ✅ Full |
| WebSocket | ✅ Native | ⚠️ Plugin | ✅ Native |
| File download | ✅ Native | ⚠️ Workaround | ✅ Native |
| Offline mode | ✅ Native | ⚠️ Plugin | ⚠️ Limited |
| Performance | ✅ CDP | ❌ N/A | ⚠️ Limited |
| Shadow DOM | ✅ Native | ✅ Native | ⚠️ Plugin |
| iframes | ✅ Full | ⚠️ Same-origin | ✅ Full |

---

## Playwright 1.49+ Modern Features

| Feature | API | Use Case |
|---------|-----|----------|
| **Clock API** | `page.clock.install()` / `.fastForward()` / `.setFixedTime()` | Fake timers, animation control, date-dependent UI |
| **Soft Assertions** | `expect.configure({ soft: true })` | Collect all failures in one test run |
| **Viewport Assertions** | `expect(el).toBeInViewport()` | Lazy loading, infinite scroll verification |
| **API Testing** | `request.get()` / `request.post()` in test | Mix UI + API tests, setup via API |
| **Component Testing** | `@playwright/experimental-ct-react` | React/Vue/Svelte component tests in real browser |

See `playwright-patterns.md` → "Playwright 1.49+ Modern Features" for code examples.

---

## Quick Reference

> For detailed code examples, see the dedicated reference files:

| Topic | Reference |
|-------|-----------|
| Playwright config, Page Object, waits | `playwright-patterns.md` |
| Performance targets (CWV) | `performance-testing.md` |
| CI sharding configuration | `ci-reporting.md` |

---

## TestCafe Basic Patterns

> **Note**: TestCafe adoption has declined. Consider Playwright as the default choice for new projects.

### Basic Test

```typescript
import { Selector } from 'testcafe';

fixture('Login')
  .page('http://localhost:3000/login');

test('successful login', async (t) => {
  await t
    .typeText(Selector('[data-testid="email-input"]'), 'user@example.com')
    .typeText(Selector('[data-testid="password-input"]'), 'Test1234!')
    .click(Selector('[data-testid="login-submit"]'))
    .expect(Selector('[data-testid="dashboard"]').exists)
    .ok();
});

test('shows error for invalid credentials', async (t) => {
  await t
    .typeText(Selector('[data-testid="email-input"]'), 'wrong@example.com')
    .typeText(Selector('[data-testid="password-input"]'), 'wrong')
    .click(Selector('[data-testid="login-submit"]'))
    .expect(Selector('[data-testid="login-error"]').visible)
    .ok();
});
```

### TestCafe Configuration

```json
// .testcaferc.json
{
  "src": "e2e/tests/**/*.testcafe.ts",
  "browsers": ["chrome:headless"],
  "concurrency": 3,
  "reporter": [
    { "name": "spec" },
    { "name": "json", "output": "test-results.json" }
  ],
  "screenshots": {
    "path": "screenshots/",
    "takeOnFails": true
  },
  "quarantineMode": {
    "successThreshold": 1,
    "attemptLimit": 3
  }
}
```

### TestCafe API Mocking

```typescript
import { RequestMock } from 'testcafe';

const mock = RequestMock()
  .onRequestTo('https://api.example.com/users')
  .respond({ users: [{ id: 1, name: 'Test User' }] }, 200, {
    'content-type': 'application/json',
  });

fixture('Dashboard')
  .page('http://localhost:3000/dashboard')
  .requestHooks(mock);

test('displays mocked users', async (t) => {
  await t
    .expect(Selector('[data-testid="user-list"]').childElementCount)
    .eql(1);
});
```

---

## Version Requirements

| Tool | Minimum Version | Recommended | Notes |
|------|----------------|-------------|-------|
| **Playwright** | 1.49+ | 1.50+ | Clock API, Aria Snapshots |
| **Cypress** | 13+ | 13.x | Component testing stable |
| **WebdriverIO** | 9+ | 9.x | New APIs, Appium 2.0 |
| **TestCafe** | 3.5+ | 3.6+ | Declining ecosystem |
| **Node.js** | 18+ | 20 LTS | Required by all frameworks |
| **TypeScript** | 5.0+ | 5.3+ | Recommended for type safety |
