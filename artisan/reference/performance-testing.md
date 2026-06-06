# Performance & Testing

Core Web Vitals, optimization strategies, Testing Trophy, Vitest v2, Storybook integration, RSC testing, and E2E patterns.

---

## 1. Core Web Vitals

| Metric | Target | Measures |
|--------|--------|----------|
| **LCP** (Largest Contentful Paint) | < 2.5s | Main content display speed |
| **INP** (Interaction to Next Paint) | < 200ms | Interaction responsiveness (replaced FID March 2024) |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Visual stability |

---

## 2. Image Optimization

```tsx
import Image from 'next/image';

// LCP image: priority (never lazy load)
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />

// Normal image: auto lazy loading
<Image src="/product.jpg" alt="Product" width={400} height={300} />
```

| Rule | Reason |
|------|--------|
| No `loading="lazy"` on LCP element | Degrades LCP score |
| `fetchpriority="high"` on LCP image | Prioritize loading |
| Always specify `width`/`height` | Prevent CLS |
| Use WebP/AVIF | 25-35% compression improvement over JPEG |
| Use `sizes` for responsive delivery | Prevent oversized images |

---

## 3. Bundle Size Reduction

### Code Splitting

```tsx
import { lazy, Suspense } from 'react';

// Route-based splitting (most effective: 40-60% initial load reduction)
const AdminDashboard = lazy(() => import('./AdminDashboard'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </Suspense>
  );
}
```

### Bundle Analysis Checklist

- [ ] Regular `bundle-analyzer` checks
- [ ] Tree shaking enabled (`sideEffects: false`)
- [ ] Partial imports for large libraries (`import { debounce } from 'lodash-es'`)
- [ ] `next/dynamic` for client-only lazy loading
- [ ] Third-party scripts with `strategy="lazyOnload"`

---

## 4. Rendering Optimization

| Technique | Effect | When |
|-----------|--------|------|
| Server Components as default | Not in JS bundle | All data-display components |
| Suspense streaming | Progressive content display | Slow data fetches |
| React Compiler (React 19) | Auto-memoization | All new code |
| `@tanstack/react-virtual` | List virtualization | 100+ item lists |

### Resource Hints

```html
<link rel="preload" href="/fonts/inter.woff2" as="font" crossorigin />
<link rel="prefetch" href="/dashboard" />
<link rel="dns-prefetch" href="https://api.example.com" />
```

### Performance Budget

| Item | Recommended Limit |
|------|-------------------|
| Total page weight | < 1.5MB |
| JavaScript bundle | < 300KB |
| Time to Interactive | < 3.5s |
| HTTP requests | < 50 |

---

## 5. Testing Trophy

"Write tests. Not too many. Mostly integration." — Kent C. Dodds

| Layer | Tool | Volume | Target |
|-------|------|:---:|--------|
| **Static Analysis** | ESLint, TypeScript | Always | Type errors, lint rules |
| **Unit Test** | Vitest | Few | Pure functions, business logic |
| **Component Test** | Vitest + Testing Library | **Many** | Component behavior |
| **Integration Test** | Vitest + Testing Library | **Most** | Multi-component interactions |
| **Visual Test** | Chromatic / Percy | Medium | Visual regressions |
| **E2E Test** | Playwright | **Few** | Critical user flows |

---

## 6. Vitest v2

### Setup (Next.js)

```ts
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './vitest.setup.ts',
    css: true,
  },
  resolve: { alias: { '@': './src' } },
});
```

```ts
// vitest.setup.ts
import '@testing-library/jest-dom/vitest';
```

### v2 Key Features (July 2024)

| Feature | Details |
|---------|---------|
| **Browser Mode** | Real browser testing via Playwright or WebdriverIO — no jsdom limitations |
| **Workspace** | Multiple project configs in a single Vitest instance |
| **Forks pool** | Default pool changed from `threads` to `forks` for better isolation |
| `--reporter=blob` | CI artifact for merged coverage reports |

### Browser Mode Setup

```ts
// vitest.config.ts (browser mode)
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: 'playwright',
      instances: [{ browser: 'chromium' }],
    },
  },
});
```

---

## 7. Testing Patterns

### Component Test

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';

describe('Counter', () => {
  it('increments count on click', async () => {
    const user = userEvent.setup(); // v14+: always use setup()
    render(<Counter initialCount={0} />);
    await user.click(screen.getByRole('button', { name: /increment/i }));
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

### API Mocking (MSW v2)

```ts
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/products', () => {
    return HttpResponse.json([{ id: 1, name: 'Product A' }]);
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Testing Library Query Priority

```
1. getByRole       ← Highest priority (improves a11y too)
2. getByLabelText  ← Form elements
3. getByText       ← Non-interactive elements
4. getByTestId     ← Last resort only
```

**Principle:** Test user-visible behavior, not implementation details.

---

## 8. RSC Testing Strategies

| Component Type | Testing Method |
|---------------|---------------|
| Sync Server/Client Component | Vitest + Testing Library |
| Async Server Component | **Playwright E2E** (Vitest cannot render async SC directly) |
| Server Actions | Vitest unit test (call function directly) |
| Server → Client data flow | E2E with Playwright |

```tsx
// Server Action unit test
import { describe, it, expect } from 'vitest';
import { createTodo } from './actions';

describe('createTodo', () => {
  it('validates and creates', async () => {
    const fd = new FormData();
    fd.set('title', 'Test Todo');
    const result = await createTodo({}, fd);
    expect(result.success).toBe(true);
  });

  it('returns errors for invalid input', async () => {
    const fd = new FormData();
    fd.set('title', '');
    const result = await createTodo({}, fd);
    expect(result.errors).toBeDefined();
  });
});
```

---

## 9. Storybook 8.5+ Integration

### Vitest Browser Mode via Storybook

```ts
// .storybook/vitest.setup.ts
import { setProjectAnnotations } from '@storybook/react';
import * as projectAnnotations from './preview';

setProjectAnnotations(projectAnnotations);
```

| Feature | Details |
|---------|---------|
| `@storybook/experimental-addon-test` | Run component tests inside Storybook via Vitest |
| Portable Stories | Import stories into Vitest tests: `composeStories(meta)` |
| Play functions | Interactive tests within stories, runnable by Vitest |

### Portable Stories

```tsx
import { composeStories } from '@storybook/react';
import * as stories from './Button.stories';

const { Primary, Disabled } = composeStories(stories);

it('renders primary button', () => {
  render(<Primary />);
  expect(screen.getByRole('button')).toBeInTheDocument();
});
```

---

## 10. E2E (Playwright)

```ts
import { test, expect } from '@playwright/test';

test('complete checkout flow', async ({ page }) => {
  await page.goto('/products');
  await page.click('[data-testid="product-1"] button');
  await expect(page.locator('[data-testid="cart-count"]')).toHaveText('1');
  await page.click('[data-testid="checkout-button"]');
  await page.fill('[name="email"]', 'test@example.com');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/\/order-confirmation/);
});
```

**E2E scope:** Revenue-critical paths only — signup → purchase → payment confirmation.

---

## 11. Anti-Patterns

### Performance

| # | Anti-pattern | Problem | Fix |
|---|-------------|---------|-----|
| 1 | `loading="lazy"` on LCP element | LCP score degradation | `priority` / `fetchpriority="high"` |
| 2 | Images without width/height | CLS issues | Explicit size specification |
| 3 | Excessive prefetching | Negates code splitting benefits | Critical paths only |
| 4 | Lab-only testing | Diverges from real user conditions | RUM measurement |
| 5 | Uncontrolled third-party scripts | Largest CWV threat | `lazyOnload` + impact monitoring |

### Testing

| # | Anti-pattern | Problem | Fix |
|---|-------------|---------|-----|
| 1 | Excessive snapshot tests | Meaningless update noise | Behavior-based tests |
| 2 | Testing implementation details | Breaks on refactor | User-perspective assertions |
| 3 | Too many E2E tests | Slow, flaky | Integration-test-centric |
| 4 | Overusing mocks | Not true integration | Minimal mocking + MSW |
| 5 | `getByTestId` overuse | Misses a11y improvement | `getByRole` first |
| 6 | `fireEvent` instead of `userEvent` | Doesn't simulate real interactions | `userEvent.setup()` |

**Source:** [Vitest v2 Blog](https://vitest.dev/blog/vitest-2.0) · [Vitest Browser Mode](https://vitest.dev/guide/browser/) · [Storybook Testing](https://storybook.js.org/docs/writing-tests) · [Testing Library Best Practices](https://testing-library.com/docs/guiding-principles) · [MSW v2 Migration](https://mswjs.io/docs/migrations/1.x-to-2.x) · [web.dev CWV](https://web.dev/articles/vitals)
