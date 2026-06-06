# Cypress Guide

Purpose: Use this file when a project already relies on Cypress and Voyager must extend or maintain that suite.

Contents:
- Cypress vs Playwright decision boundary
- Project setup, commands, and session patterns
- Network stubbing, CI wiring, and a11y integration

---

## When to Choose Cypress vs Playwright

> Version map (as of 2026-05): Cypress current is **15.15.0** (May 2026). 15.0 shipped 2025-08-20. AI authoring (`cy.prompt`, Studio inline edit, UI Coverage Test Generation) is the main 2025-2026 storyline. Playwright current is **1.60** (May 2026).

| Criteria | Cypress | Playwright |
|----------|---------|------------|
| **Best for** | Component testing, real-time debugging, natural-language authoring (`cy.prompt`) | Cross-browser, complex flows, agentic test loops |
| **Browser support** | Chrome, Edge, Electron, Firefox via WebDriver (Firefox CDP dropped in 15.0) | Chromium / Firefox / WebKit + mobile emulation |
| **Parallel execution** | Paid (Cypress Cloud) | Free, built-in (`workers`, `--shard`) |
| **Network stubbing** | Excellent (`cy.intercept` middleware) | Good (`page.route`, `route.fetch`, `routeWebSocket`) |
| **Learning curve** | Lower | Moderate |
| **Iframe / multi-tab / multi-origin** | `cy.origin` (mature in 15.15 stability fixes) | Full multi-origin support, native multi-tab |
| **Architecture** | In-browser, automation protocols | Out-of-process via CDP / WebDriver BiDi |
| **AI authoring** | `cy.prompt` (beta, generally available 15.13+), Studio inline edit, UI Coverage Test Generation | Test Agents (Planner / Generator / Healer 1.56+), MCP, `@playwright/cli` Skills mode |
| **Node.js floor** | Node 20 LTS (15.0 dropped 18 and 23) | Node 18 LTS minimum (1.59+) |

**Recommendation**: Playwright is the default for new projects. Choose Cypress when (a) the team already runs a Cypress suite, (b) component testing with the Cypress Cloud dashboard / UI Coverage is in scope, or (c) `cy.prompt` natural-language authoring is desired alongside the existing Cypress workflow.

---

## Project Setup

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
    supportFile: 'cypress/support/e2e.ts',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    retries: {
      runMode: 2,
      openMode: 0,
    },
    env: {
      apiUrl: 'http://localhost:3001',
    },
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
    specPattern: 'src/**/*.cy.{js,ts,jsx,tsx}',
  },
});
```

### Directory Structure

```
cypress/
├── e2e/
│   ├── auth/
│   │   ├── login.cy.ts
│   │   └── signup.cy.ts
│   └── checkout/
│       └── purchase.cy.ts
├── fixtures/
│   ├── users.json
│   └── products.json
├── support/
│   ├── commands.ts        # Custom commands
│   ├── e2e.ts             # E2E support file
│   └── component.ts       # Component support file
└── pages/                 # Page Objects (optional)
    ├── login.page.ts
    └── checkout.page.ts
```

---

## Custom Commands

```typescript
// cypress/support/commands.ts
declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      getByTestId(testId: string): Chainable<JQuery<HTMLElement>>;
      apiLogin(email: string, password: string): Chainable<void>;
    }
  }
}

// Login via UI
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.getByTestId('email-input').type(email);
  cy.getByTestId('password-input').type(password);
  cy.getByTestId('login-submit').click();
  cy.url().should('include', '/dashboard');
});

// Login via API (faster)
Cypress.Commands.add('apiLogin', (email: string, password: string) => {
  cy.request('POST', '/api/auth/login', { email, password }).then((response) => {
    window.localStorage.setItem('token', response.body.token);
  });
});

// Get by data-testid
Cypress.Commands.add('getByTestId', (testId: string) => {
  return cy.get(`[data-testid="${testId}"]`);
});

export {};
```

---

## Network Stubbing

```typescript
// cypress/e2e/with-stubs.cy.ts
describe('With API Stubs', () => {
  beforeEach(() => {
    cy.intercept('GET', '/api/products', { fixture: 'products.json' }).as('getProducts');
    cy.intercept('POST', '/api/orders', { statusCode: 201, body: { id: 'order-123' } }).as('createOrder');
  });

  it('displays products from API', () => {
    cy.visit('/products');
    cy.wait('@getProducts');
    cy.getByTestId('product-list').should('be.visible');
  });

  it('handles API error gracefully', () => {
    cy.intercept('GET', '/api/products', { statusCode: 500, body: { error: 'Server error' } });
    cy.visit('/products');
    cy.getByTestId('error-message').should('contain', 'An unexpected error occurred');
  });
});
```

---

## Session Management

```typescript
// cypress/support/e2e.ts
beforeEach(() => {
  cy.session('user-session', () => {
    cy.apiLogin(Cypress.env('TEST_USER_EMAIL'), Cypress.env('TEST_USER_PASSWORD'));
  });
});
```

---

## CI Configuration (GitHub Actions)

```yaml
# .github/workflows/cypress.yml
name: Cypress Tests

on: [push, pull_request]

jobs:
  cypress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Cypress run
        uses: cypress-io/github-action@v6
        with:
          build: npm run build
          start: npm start
          wait-on: 'http://localhost:3000'
        env:
          CYPRESS_TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          CYPRESS_TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}

      - name: Upload screenshots
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: cypress-screenshots
          path: cypress/screenshots

      - name: Upload videos
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: cypress-videos
          path: cypress/videos
```

---

## Cypress axe-core Integration (A11y)

```typescript
// cypress/support/commands.ts
import 'cypress-axe';

Cypress.Commands.add('checkA11y', (context?: string, options?: any) => {
  cy.injectAxe();
  cy.checkA11y(context, options, (violations) => {
    violations.forEach((violation) => {
      const nodes = violation.nodes.map(n => n.target.join(', ')).join('\n  ');
      cy.log(`${violation.id} (${violation.impact}): ${violation.description}\n  ${nodes}`);
    });
  });
});

// cypress/e2e/a11y.cy.ts
describe('Accessibility', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.injectAxe();
  });

  it('has no detectable a11y violations on load', () => {
    cy.checkA11y(null, {
      includedImpacts: ['critical', 'serious'],
    });
  });
});
```

---

## Version Notes

### Cypress 14 Breaking Changes

- **Angular**: Support for Angular v17.2.0 and below removed
- **Vue 2 / Svelte 3-4**: Moved to separate packages (`@cypress/vue2`, `@cypress/svelte3`)
- **JIT compilation**: Default for Component Testing (no more `devServer.options.webpackConfig`)
- **`cy.intercept` resourceType**: `resourceType` filter option deprecated — use `middleware: true` or `on('before:http:request')` instead
- **`ElementSelector` renamed**: `ElementSelector` type renamed to `Selector` in TypeScript definitions
- **Node.js**: Minimum version is now Node.js v22

```typescript
// ❌ Deprecated in Cypress 14
cy.intercept({ resourceType: 'xhr' }, handler);

// ✅ Use middleware or event-based approach
cy.intercept('**/api/**', { middleware: true }, (req) => {
  req.on('before:response', (res) => {
    // inspect/modify response
  });
});
```

### Cypress 15.0 Breaking Changes (2025-08-20)

- **Node.js**: Support for Node.js 18 and 23 removed (minimum: Node.js 20 LTS)
- **glibc**: Linux glibc < 2.31 is no longer supported (affects older CentOS/Debian)
- **`cy.stub` 3-argument form**: `cy.stub(object, method, replacerFn)` removed — use `.returns()` / `.callsFake()` instead
- **Webpack 4, Vite 4, Angular 17**: dropped from Component Testing — upgrade to Webpack 5 / Vite 7+ / Angular 19+
- **Firefox via CDP**: removed — Firefox now runs through WebDriver BiDi only
- **`Cypress.SelectorPlayground` renamed to `Cypress.ElementSelector`**; old name removed
- **`tsx` replaces `ts-node`** as the default TypeScript config loader
- **Component testing**: dropped `create-react-app`, `@vue/cli-service`, and older React / Vue / Angular versions
- **Added**: Studio inline editing, React 19 / Angular 19 / Vite 7 support, Next.js 16 component testing

```typescript
// ❌ Removed in Cypress 15
cy.stub(myObj, 'method', () => 'stubbed');

// ✅ Current approach
cy.stub(myObj, 'method').returns('stubbed');
// or
cy.stub(myObj, 'method').callsFake(() => 'stubbed');
```

```typescript
// Cypress 15 — Next.js 16 component testing config
// cypress.config.ts
import { defineConfig } from 'cypress';
import { devServer } from '@cypress/next';

export default defineConfig({
  component: {
    devServer,
    specPattern: 'src/**/*.cy.{ts,tsx}',
  },
});
```

### Cypress 15.x Highlights Since GA

| Version | Date | Highlight |
|---------|------|-----------|
| 15.0.0 | 2025-08-20 | Studio inline edit; Node 20 floor; SelectorPlayground → ElementSelector |
| 15.8.0 | 2025-12-16 | Experimental fast visibility checks; Angular 21 + zoneless component testing |
| 15.10.0 | 2026-02-03 | `Cypress.env()` deprecated → new `cy.env()` command; `Cypress.expose()` API; `allowCypressEnv` toggle |
| 15.11.0 | 2026-02-25 | `--pass-with-no-tests` flag; Brotli compression in proxy; React SSR hydration via bootstrap injection |
| 15.13.0 | 2026-03-24 | **`cy.prompt` reaches beta — no config required**; Studio supports adding tests while focused on a single test |
| 15.14.0 | 2026-04-16 | TypeScript 6 + Vite 8 component testing; automatic command-log memory eviction |
| 15.15.0 | 2026-05-12 | `cy.end()` deprecated (start a new chain instead); proxy fixes for empty-body responses with `Content-Length`; multi-origin (`cy.origin`) stability improvements |

> Pin `cypress@^15.13` if you intend to use `cy.prompt` in real specs. Pin `cypress@^15.15` if you depend on multi-origin stability or TypeScript 6.

### `cy.env()` / `Cypress.expose()` Migration (15.10+)

```typescript
// ❌ Deprecated in 15.10
const apiUrl = Cypress.env('apiUrl');

// ✅ New runtime-aware command
cy.env('apiUrl').then((apiUrl) => {
  cy.visit(`${apiUrl}/dashboard`);
});

// ✅ Cypress.expose — explicitly publish config values to the spec
// cypress.config.ts
export default defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // expose only safe values; the rest stay node-side
      return { ...config };
    },
  },
});

// Spec
Cypress.expose('build', { version: process.env.BUILD_VERSION });
```

> Set `allowCypressEnv: false` in config to fail fast on the deprecated path during migration.

---

## `cy.prompt()` — Natural-Language Test Authoring (15.13+ beta)

`cy.prompt` converts natural-language steps into executable Cypress commands at runtime. The LLM evaluates the live DOM, generates selectors, and produces Cypress code; once recorded, the generated commands run without inference cost. When a selector breaks between runs, Cypress regenerates that step automatically (self-healing).

```typescript
// cypress/e2e/checkout.cy.ts
describe('Checkout — natural language', () => {
  it('completes the purchase flow', () => {
    cy.visit('/');
    cy.prompt('Add the first product to the cart');
    cy.prompt('Open the cart and click checkout');
    cy.prompt('Fill in test card 4242 4242 4242 4242 with future expiry');
    cy.prompt('Submit the order');
    cy.contains('Order confirmed').should('be.visible');
  });
});
```

```typescript
// cypress.config.ts — opt out of the prompt cache for a single spec
export default defineConfig({
  e2e: {
    experimentalPrompt: {
      cache: 'on',        // 'on' | 'off' | 'record-only'
      provider: 'cloud',  // requests routed through Cypress Cloud
    },
  },
});
```

### Review checklist for `cy.prompt`-authored tests

- [ ] Each generated step has at least one explicit business assertion (`should('contain', ...)`, `should('have.length', ...)`) — `cy.prompt` validates intent, not correctness.
- [ ] Self-heal events are surfaced in the Cypress Cloud run; silent regenerations cannot ride along.
- [ ] Selectors that the prompt generates respect the project's `data-testid` convention before falling back to text or position.
- [ ] No critical-path test relies *only* on `cy.prompt` — pair with a deterministic baseline assertion (URL, API state, persisted record).
- [ ] Auth, payments, and other side-effecting steps are stubbed (`cy.intercept`) before letting `cy.prompt` drive.

> `cy.prompt` is also exposed inside Cypress Studio: record a flow, right-click to add assertions, and Studio embeds the same `cy.prompt` calls into the spec. UI Coverage Test Generation closes coverage gaps by generating `cy.prompt`-based specs directly from coverage-gap reports.

---

## Studio + UI Coverage (Cypress 15)

- **Studio inline editing**: Record interactions and edit the resulting test inside the Cypress App — no leaving for an external editor. Driven by `experimentalStudio` until 15.13+, on by default for paid Cloud tiers afterwards.
- **UI Coverage Test Generation**: Reads the Cloud UI Coverage report and emits Cypress specs targeting screens / states the existing suite has never visited. Use it to close gaps, not as the primary authoring surface.
- **Selector Playground (now ElementSelector)**: available to all users in open mode since 15.8.

```typescript
// cypress.config.ts — enable Studio for local exploration
export default defineConfig({
  e2e: {
    experimentalStudio: true, // opt in until it ships on by default
  },
});
```

---

## WebDriver BiDi / Firefox

Cypress 15 removed Firefox-via-CDP support; Firefox runs through WebDriver BiDi. No spec changes are required, but CI images must include a BiDi-capable `geckodriver` and Firefox 128 ESR or newer. If a legacy pipeline pinned `--browser firefox` against CDP, expect an error like `firefox: cdp is no longer supported, use bidi`.

---

## Routing for Newer Cypress Patterns

- `cy.prompt` flows → also covered in `reference/ai-powered-e2e-testing.md` (cross-tool comparison with Playwright Test Agents and Stagehand).
- Self-healing review gate → `reference/ai-powered-e2e-testing.md` (shared review checklist).
- UI Coverage delivery → coordinate with `pulse` for KPI tracking and `judge` for the quality gate.
