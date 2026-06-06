# Modern Selector Strategy & Accessibility-First Testing

Purpose: Use this file when Voyager must choose stable selectors, apply ARIA snapshots, or justify accessibility-first locator decisions.

Contents:
- Selector priority ladder and fallback flow
- `getByRole()` patterns and known limits
- ARIA snapshots versus DOM snapshots
- Accessibility-first form and interaction testing
- Integration with automated axe-core checks

## Selector Priority Ladder

| Priority | Selector | Why it is preferred | Example |
|----------|----------|---------------------|---------|
| `1` | `getByRole()` | Closest to user interaction and accessibility semantics | `getByRole('button', { name: 'Submit' })` |
| `2` | `getByLabel()` | Best default for form controls | `getByLabel('Email')` |
| `3` | `getByPlaceholder()` | Acceptable for unlabeled form fields | `getByPlaceholder('Search...')` |
| `4` | `getByText()` | Useful when visible copy is stable and unique | `getByText('Welcome back')` |
| `5` | `getByTestId()` | Intentional escape hatch | `getByTestId('checkout-form')` |
| `6` | CSS / XPath | Last resort only | `page.locator('.btn')` |

### Fallback Flow

```text
Does the element expose an accessible role?
  -> Yes: use getByRole()
  -> No
Does the form control have a label?
  -> Yes: use getByLabel()
  -> No
Does it have a stable placeholder?
  -> Yes: use getByPlaceholder()
  -> No
Does it have unique visible text?
  -> Yes: use getByText()
  -> No
Can you add a test-specific attribute?
  -> Yes: use getByTestId()
  -> No: CSS/XPath only as a documented last resort
```

## `getByRole()` Patterns

### Basic Usage

```typescript
await page.getByRole('button', { name: 'Save changes' }).click();
await page.getByRole('link', { name: 'Sign up' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
await page.getByRole('checkbox', { name: 'Agree to terms' }).check();
await expect(page.getByRole('heading', { level: 1 })).toHaveText('Dashboard');
await page.getByRole('navigation').getByRole('link', { name: 'Home' }).click();
```

### Filtering and Scoping

```typescript
await page.getByRole('checkbox', { name: 'Newsletter', checked: true });
await page.getByRole('tab', { name: 'Settings', selected: true });
await page.getByRole('treeitem', { expanded: true });

const dialog = page.getByRole('dialog');
await dialog.getByRole('button', { name: 'Confirm' }).click();

// Hidden elements should be rare and intentional
await page.getByRole('button', { name: 'Menu', includeHidden: true });
```

### Known Limits

| Limit | Symptom | Preferred response |
|-------|---------|--------------------|
| Same role and same name | Multiple buttons resolve to the same target | Scope to a region or fallback to `getByTestId` |
| Dynamic content | Accessible name changes frequently | Use `getByTestId` if semantics are unstable |
| Shadow DOM | Accessibility tree is incomplete | Use `locator()` plus piercing or `getByTestId` |
| Custom components without ARIA | Element has no usable role | Fix the component semantics first |
| Complex tables or grids | Cell targeting is ambiguous | Combine `getByRole('cell')` with filters |

## ARIA Snapshots

ARIA snapshots test semantics instead of raw DOM shape.

```typescript
await expect(page.getByRole('navigation')).toMatchAriaSnapshot(`
  - navigation:
    - link "Home"
    - link "Products"
    - link "About"
    - link "Contact"
`);

await expect(page.getByRole('form')).toMatchAriaSnapshot(`
  - form:
    - textbox
    - textbox
    - button "Submit"
`);
```

### ARIA vs DOM Snapshots

| Dimension | ARIA snapshot | DOM snapshot |
|-----------|---------------|--------------|
| Stability | Higher, because it is semantics-first | Lower, because markup churn breaks it |
| Readability | Higher | Lower |
| Accessibility signal | Built in | None |
| Best fit | Navigation, forms, dialogs, user-facing semantics | Detailed structural assertions only |

## Accessibility-First Testing

Principle:

```text
Write tests the way a screen-reader or keyboard user experiences the UI.
If the test breaks because accessible semantics disappeared, the test found a real problem.
```

### Prefer Semantic Interactions

```typescript
// Implementation-coupled
await page.locator('#submit-btn').click();
await page.locator('.error-msg').isVisible();

// Accessibility-first
await page.getByRole('button', { name: 'Submit order' }).click();
await expect(page.getByRole('alert')).toContainText('Invalid email');
```

### Accessibility-First Form Example

```typescript
test('submits the registration form', async ({ page }) => {
  await page.getByLabel('Full name').fill('John Doe');
  await page.getByLabel('Email address').fill('john@example.com');
  await page.getByLabel('Password').fill('SecurePass123');
  await page.getByRole('checkbox', { name: 'I agree to terms' }).check();
  await page.getByRole('button', { name: 'Create account' }).click();
  await expect(page.getByRole('status')).toContainText('Account created');
});
```

### Common Roles

| Role | Typical HTML | Common use |
|------|--------------|------------|
| `button` | `<button>`, `<input type="submit">` | Click action |
| `link` | `<a href>` | Navigation |
| `textbox` | `<input type="text">`, `<textarea>` | Text input |
| `checkbox` | `<input type="checkbox">` | Toggle |
| `heading` | `<h1>` to `<h6>` | Structure |
| `navigation` | `<nav>` | Navigation region |
| `dialog` | `<dialog>` | Modal |
| `alert` | `role="alert"` | Error or success message |
| `status` | `role="status"` | Status update |
| `form` | `<form>` | Form region |
| `list` / `listitem` | `<ul>/<li>` | Lists |
| `table` / `row` / `cell` | `<table>/<tr>/<td>` | Tables |

## axe-core Integration

```typescript
import AxeBuilder from '@axe-core/playwright';

test('checkout page is accessible', async ({ page }) => {
  await page.goto('/checkout');

  await page.getByLabel('Card number').fill('4111111111111111');
  await page.getByRole('button', { name: 'Pay now' }).click();

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### Problems This Strategy Exposes Early

| Problem | Signal |
|---------|--------|
| Missing form label | `getByLabel()` cannot find the control |
| Missing button role | `getByRole('button')` cannot find the control |
| Broken keyboard flow | `Tab` or `Enter` navigation fails |
| Poor color contrast | axe-core reports a violation |
| Duplicate IDs | axe-core reports a violation |

Sources: [Playwright: Locators](https://playwright.dev/docs/locators) · [Playwright: Accessibility Testing](https://playwright.dev/docs/accessibility-testing) · [Playwright: ARIA Snapshots](https://playwright.dev/docs/aria-snapshots) · [Components.Guide: Accessibility-First Playwright](https://components.guide/accessibility-first/playwright) · [Cam McHenry: Accessible Playwright Tests](https://camchenry.com/blog/how-i-write-accessible-playwright-tests) · [Momentic: Limits of getByRole](https://momentic.ai/resources/the-limits-of-playwright-getbyrole-when-semantic-locators-arent-enough)
