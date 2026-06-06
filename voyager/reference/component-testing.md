# Component Testing (Browser) Reference

Purpose: Test individual UI components — or small compositions — **inside a real browser** with a real DOM, real CSS layout, real events, and real accessibility tree. This sits between Radar `unit` (Node / jsdom) and Voyager `playwright` (full-page E2E).

## Scope Boundary

- **Voyager `component`**: real browser, real DOM, real layout. Mounts one component or one small composition. No routing, no global app shell.
- **Radar `unit`**: Node / jsdom, no real layout, no real `pointerdown`, no real focus. Much faster, much cheaper, but cannot verify hover, focus-visible, CSS-driven visibility, ResizeObserver, IntersectionObserver, or pointer capture.
- **Voyager `playwright`**: full-page E2E — routing, auth, multi-page journeys. Component tests should not mount the full app.
- **Vitrine**: owns Storybook stories as the documentation and catalog surface. This recipe executes tests **against those stories** (via the `play` function or the Storybook test runner) rather than re-inventing the mount setup.
- **Voyager `visual`**: screenshot diffing. Often combined with component tests, but the recipe is orthogonal — visual tests can run over stories too.

If the test needs real layout or pointer semantics on a single component → `component`. If it needs a full user flow across screens → `playwright`. If jsdom is enough → Radar `unit`.

## Framework Selection

| Framework | Pick when | Skip when |
|-----------|-----------|-----------|
| **Playwright Component Testing** | Team already runs Playwright E2E; want a unified runner; need cross-browser (Chromium + WebKit + Firefox) per component | Project is Cypress-first |
| **Cypress Component Testing** | Project already uses Cypress; Vite/webpack dev server is configured; team prefers Cypress's time-travel debugger | No Cypress elsewhere — introducing it just for CT is overhead |
| **Storybook Interactions** (`play` + `@storybook/test`) | Stories are the source of truth for UI; Vitrine already maintains them; want tests colocated with documentation | No Storybook adoption |
| **Vitest Browser Mode** | Already on Vitest; want the unit-test ergonomics with real-browser fidelity | Need cross-browser matrix (Chromium-only by default via Playwright provider) |

Default: **If stories exist → run tests over stories** (Storybook test runner or Playwright + Storybook). Otherwise **Playwright Component Testing** for Playwright shops, **Cypress CT** for Cypress shops.

## Workflow

```
PLAN       → identify component(s) and the behaviors browser layout is required for
             (hover, focus ring, ResizeObserver, IntersectionObserver, CSS :has(), @container)
           → check: does a Storybook story already cover this case? If yes → test the story
           → pick framework based on existing stack

AUTOMATE   → mount the component in isolation (no Router, no global Provider tree
             unless the behavior under test requires it — then mount only that Provider)
           → assert with `getByRole` / `getByLabel` / `getByTestId` — same priority as E2E
           → drive interactions via real `page.click` / `userEvent` — never call handler props directly

STABILIZE  → wait on accessibility state, not on `setTimeout` (`expect(locator).toBeFocused()`)
           → mock network via Playwright route / MSW; never hit a real backend from a CT
           → isolate fixtures per test; reset any module-level state

SCALE      → shard by component directory
           → combine with `visual` recipe for screenshot coverage of key states
```

## Mount Pattern (Playwright CT + Storybook)

```ts
// Button.ct.spec.tsx
import { test, expect } from '@playwright/experimental-ct-react';
import { Primary } from './Button.stories';  // reuse the story

test('primary button reaches focus ring on Tab', async ({ mount, page }) => {
  const component = await mount(<Primary />);
  await page.keyboard.press('Tab');
  await expect(component).toBeFocused();
  // Real layout — can assert computed styles
  await expect(component).toHaveCSS('outline-style', 'solid');
});
```

Testing the story — not a parallel mount — keeps Vitrine as the single source of truth.

## What Component Testing Catches That Unit Testing Misses

- **Focus management**: `focus-visible`, focus traps, `inert`, roving tabindex.
- **Layout-dependent behavior**: ResizeObserver, IntersectionObserver, `@container` queries, `:has()`.
- **Pointer semantics**: `pointerdown` vs `click`, `setPointerCapture`, drag-and-drop.
- **Real CSS**: transitions, `prefers-reduced-motion`, z-index stacking, overflow clipping.
- **Accessibility tree as rendered**: `getByRole` in a real accessibility tree behaves differently from jsdom.

If the behavior under test is none of the above → Radar `unit` is faster and cheaper. Do not push unit-testable logic into the browser.

## Integration With Vitrine

- Vitrine writes and maintains stories (CSF 3.0 / Factories).
- Voyager `component` executes tests against those stories via the `play` function (`@storybook/test`) or a Playwright + Storybook runner.
- Visual regression over stories → combine with `visual` recipe.
- New behavior coverage requires coordinating: Vitrine adds the story variant → Voyager tests assert the play function + interactions.

## Anti-Patterns

- Mounting the full application tree in a component test — that is a Playwright E2E without routing.
- Duplicating a story's mount just to write the test — test the story, keep one source of truth.
- Asserting on the component's internal state or props — test observable behavior, not implementation.
- Testing trivial components in the browser — a stateless label that renders `{children}` belongs in Radar `unit`.
- Hitting a real backend from a CT — mock at the network boundary.
- Skipping roles / labels and reaching for `data-testid` first — same accessibility-first priority as E2E.
- Running the full matrix (Chromium + WebKit + Firefox) per component by default — pick one per PR, expand at release.

## CI Considerations

- Component tests are mid-cost: a browser boots once per worker, but no full app. Target **1-3 s per test** as a budget; anything above likely has an unmocked network or an oversized mount tree.
- Shard by component directory and run in parallel — most CT runners support it out of the box.
- Reuse the same HTML reporter and trace tooling as Playwright E2E when on Playwright CT; a single dashboard makes triage cheaper.
- Run cross-browser (WebKit + Firefox) only on release branches unless the behavior is browser-specific.

## Handoff

- To **Radar**: the behavior is jsdom-safe — move it down the pyramid.
- To **Vitrine**: a story does not yet exist for the variant under test; add it first.
- To **Voyager `playwright`**: the scenario needs multiple screens or real routing.
- To **Voyager `visual`**: add screenshot coverage over the same stories.
- To **Palette**: a real accessibility gap was found; route the finding for a11y remediation.
