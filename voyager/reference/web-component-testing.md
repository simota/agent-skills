# Web Component Testing

Purpose: Use this file when Voyager must test Web Components, Shadow DOM elements, Lit components, or Stencil components with Playwright or Cypress.

Contents:
- Playwright automatic Shadow DOM piercing
- Open vs Closed Shadow DOM handling
- Lit component test strategies
- Stencil component testing with @stencil/playwright
- Async Shadow Root wait patterns
- Aria Snapshot with Shadow DOM

---

## Playwright and Shadow DOM

### Automatic Piercing (Open Shadow DOM)

Playwright automatically traverses open Shadow DOM when using standard locators. No special handling is required for most cases:

```typescript
// Playwright pierces open shadow roots transparently
// Assume <my-button> has a shadow root containing <button>
test('shadow DOM button is clickable', async ({ page }) => {
  await page.goto('/');

  // Standard locators work through open Shadow DOM
  await page.getByRole('button', { name: 'Submit' }).click();
  await page.getByLabel('Email address').fill('test@example.com');
  await page.getByText('Welcome').isVisible();
});
```

### Querying Inside a Specific Host Element

```typescript
test('component internals are accessible', async ({ page }) => {
  await page.goto('/');

  // Scope to the web component host
  const myCard = page.locator('my-card');

  // Locators inside the component pierce its shadow root automatically
  await expect(myCard.getByRole('heading')).toContainText('Card Title');
  await myCard.getByRole('button', { name: 'Read more' }).click();
});
```

---

## Open vs Closed Shadow DOM

| Mode | Playwright behavior | Recommended approach |
|------|---------------------|----------------------|
| **Open** (`mode: 'open'`) | Automatic piercing — standard locators work | Use standard ARIA/role locators |
| **Closed** (`mode: 'closed'`) | Cannot traverse — shadow root is inaccessible | Test via public attributes, events, or `page.evaluate` |

### Closed Shadow DOM Workarounds

```typescript
// Option 1: Test observable behavior (preferred)
test('closed shadow component emits correct events', async ({ page }) => {
  await page.goto('/');

  const eventReceived = page.waitForEvent('custom-event', { timeout: 3000 }).catch(() => null);
  await page.locator('my-closed-component').click();
  // Verify side effects rather than internal DOM
  await expect(page.getByTestId('result')).toContainText('activated');
});

// Option 2: Evaluate inside the shadow root (escape hatch — document and review)
test('closed shadow DOM via evaluate', async ({ page }) => {
  await page.goto('/');

  const innerText = await page.evaluate(() => {
    const host = document.querySelector('my-closed-component');
    // Access internals only if exposed via the element's own API
    return (host as any).shadowRoot?.querySelector('.status')?.textContent;
  });

  expect(innerText).toBe('ready');
});
```

> Warning: Closed Shadow DOM tests via `evaluate` are brittle. Raise an architecture concern and prefer testing through public APIs.

---

## Lit Component Testing

### E2E Strategy: Use Standard Playwright Locators

```typescript
// my-button.ts (Lit component)
// <my-button label="Submit" variant="primary"></my-button>
// shadow root: <button part="base" aria-label="Submit">Submit</button>

test('Lit button renders and is interactive', async ({ page }) => {
  await page.goto('/components/button');

  const button = page.getByRole('button', { name: 'Submit' });
  await expect(button).toBeVisible();
  await expect(button).toBeEnabled();
  await button.click();

  await expect(page.getByTestId('click-count')).toContainText('1');
});
```

### Unit Testing Lit Components: @web/test-runner

For isolated unit tests of Lit components (not E2E), use `@web/test-runner` instead of Playwright:

```typescript
// src/my-button.test.ts
import { fixture, html, expect } from '@open-wc/testing';
import { MyButton } from './my-button.js';

it('renders with label', async () => {
  const el = await fixture<MyButton>(html`<my-button label="Submit"></my-button>`);
  const button = el.shadowRoot!.querySelector('button')!;
  expect(button.textContent?.trim()).to.equal('Submit');
});
```

> Rule: Use Playwright E2E for journey-level tests. Use `@web/test-runner` for component-level unit tests.

---

## Stencil Component Testing

### @stencil/playwright Adapter

Stencil provides an official Playwright adapter that handles hydration timing automatically:

```bash
npm install --save-dev @stencil/playwright
```

```typescript
// stencil.config.ts — enable e2e testing
import { Config } from '@stencil/core';

export const config: Config = {
  namespace: 'my-components',
  testing: {
    browserHeadless: 'new',
  },
};
```

```typescript
// src/components/my-input/my-input.e2e.ts
import { test, expect } from '@stencil/playwright';

test.describe('my-input', () => {
  test('accepts user input', async ({ page }) => {
    await page.goto('/my-input');

    // @stencil/playwright waits for Stencil hydration automatically
    const input = page.locator('my-input').getByRole('textbox');
    await input.fill('Hello Stencil');
    await expect(input).toHaveValue('Hello Stencil');
  });

  test('emits ionInput event', async ({ page }) => {
    await page.goto('/my-input');

    const eventFired = page.waitForFunction(() =>
      (window as any).__testEvents?.includes('ionInput')
    );

    await page.locator('my-input').getByRole('textbox').type('test');
    await eventFired;
  });
});
```

### Hydration Timing

Without the Stencil adapter, components may not be hydrated when Playwright interacts with them. The adapter adds an automatic wait:

```typescript
// Without adapter — may fail intermittently
await page.locator('my-component').click(); // Component may not be hydrated

// With adapter — safe
import { test } from '@stencil/playwright';
test('hydration is handled', async ({ page }) => {
  await page.goto('/');
  // Adapter ensures hydration before interactions
  await page.locator('my-component').getByRole('button').click();
});
```

---

## Async Shadow Root Wait Patterns

For cases where Shadow DOM is attached asynchronously (e.g., lazy-loaded components):

```typescript
// Wait for the shadow root to be attached
async function waitForShadowRoot(page: Page, selector: string) {
  await page.waitForFunction((sel) => {
    const el = document.querySelector(sel);
    return el !== null && el.shadowRoot !== null;
  }, selector);
}

test('lazy-loaded component shadow DOM is ready', async ({ page }) => {
  await page.goto('/');

  // Trigger lazy load
  await page.getByRole('button', { name: 'Load component' }).click();

  // Wait for shadow root to be available
  await waitForShadowRoot(page, 'my-lazy-component');

  // Now safe to interact
  await expect(
    page.locator('my-lazy-component').getByRole('status')
  ).toContainText('loaded');
});
```

### Polling with toPass

```typescript
test('async component renders content', async ({ page }) => {
  await page.goto('/');

  // Component renders asynchronously
  await expect(async () => {
    const text = await page.locator('my-async-component').getByRole('heading').textContent();
    expect(text).toBeTruthy();
  }).toPass({ timeout: 5000 });
});
```

---

## Aria Snapshot with Shadow DOM (Playwright v1.50+)

Aria Snapshots work through Shadow DOM automatically on open shadow roots:

```typescript
test('web component has correct ARIA structure', async ({ page }) => {
  await page.goto('/');

  // Aria snapshot pierces open shadow root
  await expect(page.locator('my-navigation')).toMatchAriaSnapshot(`
    - navigation:
      - list:
        - listitem:
          - link "Home"
        - listitem:
          - link "Products"
        - listitem:
          - link "About"
  `);
});
```

### v1.50+ Enhancements for Shadow DOM

```typescript
// /children option — match aria tree with children assertion
await expect(page.locator('my-form')).toMatchAriaSnapshot(`
  - form:
    /children: contain
    - textbox "Email"
    - textbox "Password"
`);

// /url option — verify link URLs inside shadow DOM
await expect(page.locator('my-nav')).toMatchAriaSnapshot(`
  - navigation:
    - link "GitHub" [/url: "https://github.com/"]
`);
```

---

## Common Patterns

### Custom Element Registration Check

```typescript
// Verify the component is registered before interacting
test('custom element is registered', async ({ page }) => {
  await page.goto('/');

  const isRegistered = await page.evaluate(
    (tag) => customElements.get(tag) !== undefined,
    'my-component'
  );

  expect(isRegistered).toBe(true);
});
```

### Part and Slot Testing

```typescript
// Test slot content
test('default slot renders children', async ({ page }) => {
  await page.goto('/');

  // Content in slots is in the light DOM — no shadow piercing needed
  await expect(page.locator('my-card').getByText('Card content')).toBeVisible();
});

// CSS part is an implementation detail — test behavior, not parts
// ❌ Avoid: page.locator('my-component::part(base)')
// ✅ Prefer: page.locator('my-component').getByRole('region')
```

Sources: [Playwright Shadow DOM docs](https://playwright.dev/docs/locators#shadow-piercing) · [Lit Testing Guide](https://lit.dev/docs/tools/testing/) · [@stencil/playwright](https://github.com/ionic-team/stencil/tree/main/src/testing/playwright) · [Open WC Testing](https://open-wc.org/docs/testing/testing-package/)
