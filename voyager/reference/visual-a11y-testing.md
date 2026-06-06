# Visual Regression & Accessibility Testing

Purpose: Use this file when Voyager must verify screenshots, keyboard access, or automated accessibility rules.

Contents:
- Visual snapshot configuration and update rules
- axe-core, keyboard, and WCAG checks
- Responsive and SaaS-backed visual regression patterns

---

## Visual Regression Testing

### Snapshot Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,           // Allow small differences
      threshold: 0.2,               // Pixel comparison threshold
      animations: 'disabled',       // Disable animations for consistency
    },
  },
  updateSnapshots: process.env.UPDATE_SNAPSHOTS ? 'all' : 'missing',
});
```

### Visual Test Examples

```typescript
// e2e/tests/visual/homepage.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage matches snapshot', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Full page screenshot
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
    });
  });

  test('login form matches snapshot', async ({ page }) => {
// ...
```

### Snapshot Update Commands

```bash
# Update all snapshots
npx playwright test --update-snapshots

# Update specific test snapshots
npx playwright test visual/homepage.spec.ts --update-snapshots
```

### Visual Regression Best Practices

| Practice | Description |
|----------|-------------|
| **Disable animations** | Set `animations: 'disabled'` in config |
| **Wait for networkidle** | Ensure all resources loaded before screenshot |
| **Use element screenshots** | More stable than full-page for component changes |
| **Set explicit viewport** | Avoid viewport-dependent diffs |
| **Mock dynamic content** | Dates, random data, ads cause false positives |
| **Use `maxDiffPixels`** | Allow tolerance for anti-aliasing differences |

---

## Accessibility Testing (axe-core + Playwright)

### Setup

```typescript
// e2e/utils/a11y-helpers.ts
import { Page, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

export async function checkA11y(page: Page, options?: {
  includedImpacts?: ('critical' | 'serious' | 'moderate' | 'minor')[];
  disableRules?: string[];
}) {
  const axeBuilder = new AxeBuilder({ page });

  if (options?.disableRules) {
    axeBuilder.disableRules(options.disableRules);
  }

  const results = await axeBuilder.analyze();
// ...
```

### A11y Test Examples

```typescript
// e2e/tests/a11y/pages.spec.ts
import { test, expect } from '@playwright/test';
import { checkA11y } from '../../utils/a11y-helpers';

test.describe('Accessibility', () => {
  test('homepage has no critical a11y violations', async ({ page }) => {
    await page.goto('/');
    await checkA11y(page, { includedImpacts: ['critical', 'serious'] });
  });

  test('login form is accessible', async ({ page }) => {
    await page.goto('/login');

    // Check form elements have labels
    await expect(page.getByLabel('Email address')).toBeVisible();
// ...
```

### Keyboard Navigation Testing

```typescript
test('navigation is keyboard accessible', async ({ page }) => {
  await page.goto('/');

  // Tab through navigation
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Home' })).toBeFocused();

  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Products' })).toBeFocused();

  // Enter key activates link
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/.*products/);
});

// ...
```

### A11y Rules Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  metadata: {
    a11y: {
      // Skip rules for known issues (document why)
      disableRules: [
        // 'color-contrast', // Tracked in JIRA-123
      ],
      includedImpacts: ['critical', 'serious'],
    },
  },
});
```

### WCAG Compliance Checklist

| Level | Rule | Test Approach |
|-------|------|---------------|
| **A** | Non-text content has alt text | `axe-core` auto-check |
| **A** | Keyboard accessible | Manual tab testing |
| **A** | Focus order is logical | Tab sequence test |
| **A** | Color is not sole indicator | Visual + axe check |
| **AA** | Color contrast ≥ 4.5:1 | `axe-core` auto-check |
| **AA** | Text resizable to 200% | Viewport zoom test |
| **AA** | Focus visible | CSS `:focus-visible` check |
| **AA** | Error identification | Form validation test |

---

## Color Vision Simulation

### Emulate Color Deficiencies

```typescript
test.describe('Color vision accessibility', () => {
  const colorSchemes = [
    { name: 'protanopia', emulation: 'achromatopsia' },
    { name: 'deuteranopia', emulation: 'deuteranopia' },
    { name: 'tritanopia', emulation: 'tritanopia' },
  ];

  for (const { name, emulation } of colorSchemes) {
    test(`UI is usable with ${name}`, async ({ page }) => {
      const client = await page.context().newCDPSession(page);
      await client.send('Emulation.setEmulatedVisionDeficiency', {
        type: emulation,
      });

      await page.goto('/dashboard');
// ...
```

### Forced Colors Mode (High Contrast)

```typescript
test('works in forced-colors mode', async ({ browser }) => {
  const context = await browser.newContext({
    forcedColors: 'active',
  });
  const page = await context.newPage();

  await page.goto('/');

  // Elements should be visible in high contrast
  await expect(page.getByRole('navigation')).toBeVisible();
  await expect(page.getByRole('main')).toBeVisible();

  // Screenshot for visual verification
  await expect(page).toHaveScreenshot('homepage-forced-colors.png');

// ...
```

---

## Aria Snapshots for Accessibility

> See also `playwright-patterns.md` → "Playwright 1.50+ Features" for code examples.

```typescript
test('navigation landmark structure', async ({ page }) => {
  await page.goto('/');

  // Verify accessible navigation structure
  await expect(page.getByRole('navigation')).toMatchAriaSnapshot(`
    - navigation:
      - link "Home"
      - link "Products"
      - link "About"
  `);
});

test('form accessibility', async ({ page }) => {
  await page.goto('/contact');

// ...
```

---

## Visual Testing SaaS Integration

### Percy (BrowserStack)

```typescript
// Install: npm install -D @percy/playwright @percy/cli
import { test } from '@playwright/test';
import percySnapshot from '@percy/playwright';

test('homepage visual test', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  // Percy handles cross-browser screenshots
  await percySnapshot(page, 'Homepage');
});

test('responsive visual test', async ({ page }) => {
  await page.goto('/products');

// ...
```

```yaml
# .github/workflows/visual.yml (Percy CI)
- name: Percy Visual Test
  run: npx percy exec -- npx playwright test --grep @visual
  env:
    PERCY_TOKEN: ${{ secrets.PERCY_TOKEN }}
```

### Chromatic (Storybook)

```typescript
// For component-level visual testing with Storybook
// Install: npm install -D chromatic

// package.json
{
  "scripts": {
    "chromatic": "chromatic --project-token=$CHROMATIC_PROJECT_TOKEN"
  }
}
```

```yaml
# .github/workflows/chromatic.yml
- name: Chromatic Visual Review
  uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    buildScriptName: build-storybook
```

> **Voyager + Showcase boundary**: Voyager owns E2E visual regression (full-page). Showcase + Chromatic owns component-level visual testing.

---

## Responsive Visual Regression Matrix

### Multi-Viewport Testing

```typescript
const VIEWPORTS = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1280, height: 720 },
  { name: 'wide', width: 1920, height: 1080 },
];

for (const vp of VIEWPORTS) {
  test.describe(`Visual: ${vp.name} (${vp.width}x${vp.height})`, () => {
    test.use({ viewport: { width: vp.width, height: vp.height } });

    test('homepage', async ({ page }) => {
      await page.goto('/');
      await page.waitForLoadState('networkidle');
      await expect(page).toHaveScreenshot(`homepage-${vp.name}.png`, {
// ...
```

### Responsive Breakpoint Assertions

```typescript
test('layout switches at breakpoints', async ({ page }) => {
  await page.goto('/products');

  // Desktop: grid layout
  await page.setViewportSize({ width: 1280, height: 720 });
  const desktopGrid = page.getByTestId('product-grid');
  await expect(desktopGrid).toHaveCSS('display', 'grid');
  await expect(desktopGrid).toHaveCSS('grid-template-columns', /repeat/);

  // Tablet: 2-column
  await page.setViewportSize({ width: 768, height: 1024 });
  await expect(desktopGrid).toHaveCSS('grid-template-columns', /repeat\(2/);

  // Mobile: single column
  await page.setViewportSize({ width: 375, height: 667 });
// ...
```
