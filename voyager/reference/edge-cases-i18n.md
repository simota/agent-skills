# Edge Cases & i18n Testing

Purpose: Use this file when E2E coverage must exercise locale, timezone, storage, offline, or network-condition edge cases.

Contents:
- Timezone and locale validation
- Cookie, storage, and third-party-cookie behavior
- Network throttling, timeout, and offline scenarios

---

## Timezone Variation

### Context Timezone Settings

```typescript
test.describe('Timezone-sensitive features', () => {
  test('shows correct local time in Tokyo', async ({ browser }) => {
    const context = await browser.newContext({
      timezoneId: 'Asia/Tokyo',
    });
    const page = await context.newPage();

    await page.goto('/dashboard');
    const displayedTime = await page.getByTestId('local-time').textContent();
    expect(displayedTime).toMatch(/JST|GMT\+9/);

    await context.close();
  });

  test('shows correct local time in New York', async ({ browser }) => {
// ...
```

### Clock API + Timezone

```typescript
test('scheduled event displays correctly across timezones', async ({ browser }) => {
  const timezones = ['America/Los_Angeles', 'Europe/London', 'Asia/Tokyo'];

  for (const tz of timezones) {
    const context = await browser.newContext({ timezoneId: tz });
    const page = await context.newPage();

    await page.clock.install({ time: new Date('2024-06-15T12:00:00Z') });
    await page.goto('/events/123');

    // Event should show in local time
    const eventTime = await page.getByTestId('event-time').textContent();
    expect(eventTime).toBeTruthy();

    await context.close();
// ...
```

### Timezone Matrix Test

| Timezone | UTC Offset | Use Case |
|----------|-----------|----------|
| `America/Los_Angeles` | -8/-7 | US West Coast |
| `America/New_York` | -5/-4 | US East Coast |
| `Europe/London` | 0/+1 | UK (DST edge cases) |
| `Asia/Tokyo` | +9 | Japan (no DST) |
| `Pacific/Auckland` | +12/+13 | Date line edge case |

---

## Localization / i18n

### Locale Settings

```typescript
test.describe('Multi-language support', () => {
  const locales = [
    { locale: 'en-US', expectedText: 'Welcome' },
    { locale: 'ja-JP', expectedText: 'ようこそ' },
    { locale: 'de-DE', expectedText: 'Willkommen' },
  ];

  for (const { locale, expectedText } of locales) {
    test(`displays correctly in ${locale}`, async ({ browser }) => {
      const context = await browser.newContext({ locale });
      const page = await context.newPage();

      await page.goto('/');
      await expect(page.getByTestId('welcome-heading')).toContainText(expectedText);

// ...
```

### RTL Layout Verification

```typescript
test('Arabic layout is RTL', async ({ browser }) => {
  const context = await browser.newContext({ locale: 'ar-SA' });
  const page = await context.newPage();

  await page.goto('/');

  // Check document direction
  const dir = await page.evaluate(() => document.documentElement.dir);
  expect(dir).toBe('rtl');

  // Verify visual alignment
  const nav = page.getByTestId('main-nav');
  const box = await nav.boundingBox();
  const viewport = page.viewportSize()!;
  // Nav should be on the right side for RTL
// ...
```

### Translation Key Missing Detection

```typescript
test('no missing translation keys on critical pages', async ({ page }) => {
  const missingKeys: string[] = [];

  // Intercept console warnings for missing translations
  page.on('console', (msg) => {
    const text = msg.text();
    // Common i18n library warning patterns
    if (
      text.includes('Missing translation') ||
      text.includes('i18next::translator') ||
      text.match(/\bt\(['"][^'"]+['"]\).*not found/)
    ) {
      missingKeys.push(text);
    }
  });
// ...
```

### Number / Date / Currency Formatting

```typescript
test('formats currency correctly per locale', async ({ browser }) => {
  const cases = [
    { locale: 'en-US', expected: '$1,234.56' },
    { locale: 'ja-JP', expected: '￥1,235' },
    { locale: 'de-DE', expected: '1.234,56 €' },
  ];

  for (const { locale, expected } of cases) {
    const context = await browser.newContext({ locale });
    const page = await context.newPage();

    await page.goto('/product/123');
    const price = await page.getByTestId('product-price').textContent();
    expect(price?.trim()).toContain(expected);

// ...
```

## Cookie & Storage Edge Cases

### Cookie Consent Flow

```typescript
test('cookie consent banner appears and persists', async ({ page }) => {
  await page.goto('/');

  // Banner should appear
  await expect(page.getByTestId('cookie-banner')).toBeVisible();

  // Accept cookies
  await page.getByTestId('accept-cookies').click();
  await expect(page.getByTestId('cookie-banner')).toBeHidden();

  // Reload - banner should not reappear
  await page.reload();
  await expect(page.getByTestId('cookie-banner')).toBeHidden();

  // Verify consent cookie exists
// ...
```

### localStorage / sessionStorage

```typescript
test('saves user preferences to localStorage', async ({ page }) => {
  await page.goto('/settings');

  // Change theme
  await page.getByTestId('theme-dark').click();

  // Verify localStorage
  const theme = await page.evaluate(() =>
    localStorage.getItem('user-theme')
  );
  expect(theme).toBe('dark');

  // Reload and verify persistence
  await page.reload();
  await expect(page.getByTestId('theme-dark')).toBeChecked();
// ...
```

### Third-Party Cookie Blocking

```typescript
test('app works without third-party cookies', async ({ browser }) => {
  // Create context that blocks third-party cookies (like Safari)
  const context = await browser.newContext({
    // Simulate strict cookie policy
    bypassCSP: false,
  });
  const page = await context.newPage();

  // Block third-party cookies via route
  await page.route('**/*', (route) => {
    const url = route.request().url();
    if (!url.includes('localhost') && route.request().resourceType() === 'document') {
      route.abort();
    } else {
      route.continue();
// ...
```

---

## Network Condition Simulation

### Route-Based Throttling

```typescript
test('shows loading state on slow connection', async ({ page }) => {
  // Simulate slow API responses
  await page.route('**/api/**', async (route) => {
    // Add 3 second delay
    await new Promise(r => setTimeout(r, 3000));
    await route.continue();
  });

  await page.goto('/dashboard');

  // Loading skeleton should be visible
  await expect(page.getByTestId('loading-skeleton')).toBeVisible();

  // Content eventually loads
  await expect(page.getByTestId('dashboard-content')).toBeVisible({ timeout: 10000 });
// ...
```

### Network Speed Profiles

```typescript
// e2e/utils/network-profiles.ts
export const NETWORK_PROFILES = {
  'slow-3g': {
    offline: false,
    downloadThroughput: (500 * 1024) / 8,  // 500 Kbps
    uploadThroughput: (500 * 1024) / 8,
    latency: 400,
  },
  'fast-3g': {
    offline: false,
    downloadThroughput: (1.6 * 1024 * 1024) / 8,  // 1.6 Mbps
    uploadThroughput: (750 * 1024) / 8,
    latency: 150,
  },
  'regular-4g': {
// ...
```

### Timeout Testing

```typescript
test('handles API timeout gracefully', async ({ page }) => {
  // Simulate timeout - never respond
  await page.route('**/api/data', (route) => {
    // Don't call route.continue() or route.fulfill()
    // This simulates a hung connection
  });

  await page.goto('/data-view');

  // App should show timeout message
  await expect(page.getByTestId('timeout-error')).toBeVisible({ timeout: 15000 });
  await expect(page.getByTestId('retry-button')).toBeVisible();
});

test('retries failed requests', async ({ page }) => {
// ...
```

### Complete Offline Scenario

```typescript
test('queues actions while offline and syncs on reconnect', async ({ page, context }) => {
  await page.goto('/todo');
  await page.waitForLoadState('networkidle');

  // Go offline
  await context.setOffline(true);

  // Add item while offline
  await page.getByTestId('new-todo-input').fill('Offline task');
  await page.getByTestId('add-todo-btn').click();

  // Item should appear locally
  await expect(page.getByText('Offline task')).toBeVisible();
  await expect(page.getByTestId('sync-pending')).toBeVisible();

// ...
```
