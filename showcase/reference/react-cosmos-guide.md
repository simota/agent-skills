# React Cosmos Guide

Comprehensive React Cosmos 6 guide for component development and testing.

---

## React Cosmos vs Storybook

| Aspect | Storybook | React Cosmos |
|--------|-----------|--------------|
| **Setup** | Heavier, more config | Lightweight, zero-config |
| **Startup** | 5-15s (large projects) | <2s (Vite-based) |
| **Documentation** | Rich (MDX, autodocs) | Minimal (fixture-based) |
| **Addons** | Extensive ecosystem | Limited, built-in essentials |
| **Performance** | Slower on large projects | Fast, tree-shaking |
| **HMR** | Good | Excellent (per-fixture) |
| **Best For** | Design systems, docs | Fast iteration, testing |
| **File Convention** | `*.stories.tsx` | `*.fixture.tsx` |

### When to Use Which

| Scenario | Tool |
|----------|------|
| Design system documentation | Storybook |
| Rapid component iteration | React Cosmos |
| Visual regression testing | Storybook (Chromatic) |
| Isolated component development | React Cosmos |
| Component catalog for designers | Storybook |
| Internal dev tool | React Cosmos |
| Both (recommended for large projects) | Cosmos for dev + Storybook for docs |

---

## Cosmos 6 Configuration

### Basic Setup

```bash
npm install --save-dev react-cosmos react-cosmos-plugin-vite
```

```json
// cosmos.config.json
{
  "plugins": ["react-cosmos-plugin-vite"],
  "staticPath": "public",
  "watchDirs": ["src"],
  "exclude": [
    "**/*.test.*",
    "**/*.spec.*",
    "**/*.stories.*",
    "**/node_modules/**"
  ],
  "dom": {
    "containerQuerySelector": "#root"
  },
  "ui": {
// ...
```

### Vite Plugin Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  // Cosmos uses Vite config automatically
});
```

### With Next.js

```json
// cosmos.config.json
{
  "plugins": ["react-cosmos-plugin-next"],
  "experimentalRendererUrl": true
}
```

### Package Scripts

```json
{
  "scripts": {
    "cosmos": "cosmos",
    "cosmos:export": "cosmos-export"
  }
}
```

---

## Fixture Patterns

### Basic Multi-Variant Fixture

```typescript
// Button.fixture.tsx
import { Button } from './Button';

export default {
  default: <Button>Click me</Button>,

  primary: <Button variant="primary">Primary</Button>,

  secondary: <Button variant="secondary">Secondary</Button>,

  disabled: <Button disabled>Disabled</Button>,

  withIcon: (
    <Button>
      <Icon name="arrow" /> With Icon
// ...
```

### Single Default Fixture

```typescript
// Logo.fixture.tsx
import { Logo } from './Logo';

// Single export = single fixture
export default <Logo size="lg" />;
```

### Fixture with useFixtureInput Controls

```typescript
// Card.fixture.tsx
import { useFixtureInput, useFixtureSelect } from 'react-cosmos/client';
import { Card } from './Card';

export default () => {
  const [title] = useFixtureInput('title', 'Card Title');
  const [description] = useFixtureInput('description', 'Card description text');
  const [variant] = useFixtureSelect('variant', {
    options: ['default', 'outlined', 'elevated'],
    defaultValue: 'default',
  });
  const [showImage] = useFixtureInput('showImage', true);

  return (
    <Card variant={variant}>
// ...
```

### Fixture with useValue (Controlled State)

```typescript
// Counter.fixture.tsx
import { useValue } from 'react-cosmos/client';
import { Counter } from './Counter';

export default {
  controlled: () => {
    const [count, setCount] = useValue('count', { defaultValue: 0 });

    return (
      <Counter
        value={count}
        onChange={setCount}
      />
    );
  },
// ...
```

### Fixture with useFixtureState (Complex State)

```typescript
// TodoList.fixture.tsx
import { useValue } from 'react-cosmos/client';
import { TodoList } from './TodoList';

export default () => {
  const [todos, setTodos] = useValue('todos', {
    defaultValue: [
      { id: 1, text: 'Learn React Cosmos', done: false },
      { id: 2, text: 'Write fixtures', done: true },
    ],
  });

  return (
    <TodoList
      items={todos}
// ...
```

---

## Decorators

### Global Decorator (cosmos.decorator.tsx)

```typescript
// src/cosmos.decorator.tsx (auto-detected by Cosmos)
import { ThemeProvider } from './theme';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import './styles/globals.css';

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

export default ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>
    <ThemeProvider>
      {children}
    </ThemeProvider>
  </QueryClientProvider>
// ...
```

### Scoped Decorator (per-directory)

```typescript
// src/components/forms/cosmos.decorator.tsx
import { FormProvider, useForm } from 'react-hook-form';

export default ({ children }: { children: React.ReactNode }) => {
  const methods = useForm({ defaultValues: {} });
  return <FormProvider {...methods}>{children}</FormProvider>;
};
```

### Fixture-Level Decorator

```typescript
// Modal.fixture.tsx
import { useFixtureInput } from 'react-cosmos/client';
import { ModalProvider } from './ModalProvider';
import { Modal } from './Modal';

const WithModalProvider = ({ children }: { children: React.ReactNode }) => (
  <ModalProvider>{children}</ModalProvider>
);

export default {
  default: () => {
    const [isOpen] = useFixtureInput('isOpen', true);
    const [size] = useFixtureSelect('size', {
      options: ['sm', 'md', 'lg'],
      defaultValue: 'md',
// ...
```

---

## Server Fixtures (Cosmos 6)

### Mocking API Responses

```typescript
// UserProfile.fixture.tsx
import { useFixtureInput } from 'react-cosmos/client';
import { UserProfile } from './UserProfile';

// Mock fetch at fixture level
const mockUser = {
  id: 1,
  name: 'Jane Doe',
  email: 'jane@example.com',
  avatar: '/avatar.jpg',
};

export default {
  default: () => {
    const [loading] = useFixtureInput('loading', false);
// ...
```

### MSW Integration

```typescript
// src/cosmos.decorator.tsx
import { setupWorker } from 'msw/browser';
import { handlers } from './mocks/handlers';

const worker = setupWorker(...handlers);

// Start MSW before rendering fixtures
worker.start({ onUnhandledRequest: 'bypass' });

export default ({ children }: { children: React.ReactNode }) => (
  <>{children}</>
);
```

---

## Lazy Fixtures (Cosmos 6)

### Code-Splitting with Lazy Loading

```typescript
// HeavyChart.fixture.tsx
import { lazy, Suspense } from 'react';

const HeavyChart = lazy(() => import('./HeavyChart'));

export default {
  default: (
    <Suspense fallback={<div>Loading chart...</div>}>
      <HeavyChart data={sampleData} />
    </Suspense>
  ),

  withRealData: () => {
    const Chart = lazy(() => import('./HeavyChart'));
    return (
// ...
```

---

## Visual Snapshots with Cosmos

### Cosmos Export for Visual Testing

```bash
# Export static Cosmos build
npx cosmos-export

# Use Playwright against exported build
npx playwright test --config=cosmos.playwright.config.ts
```

```typescript
// cosmos.playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './cosmos-tests',
  use: {
    baseURL: 'http://localhost:5050',
  },
  webServer: {
    command: 'npx cosmos-export && npx serve cosmos-export',
    port: 5050,
  },
});

// cosmos-tests/visual.spec.ts
// ...
```

---

## Cosmos ↔ Storybook Coexistence

### Directory Structure

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx              # Component
│   │   ├── Button.fixture.tsx      # Cosmos fixture (dev)
│   │   ├── Button.stories.tsx      # Storybook story (docs)
│   │   └── Button.test.tsx         # Unit tests
│   └── ...
├── cosmos.decorator.tsx            # Cosmos global decorator
└── ...
.storybook/                         # Storybook config
cosmos.config.json                  # Cosmos config
```

### Shared Test Utilities

```typescript
// test-utils/render-helpers.ts
// Shared between Cosmos fixtures and Storybook stories

export const mockUser = {
  id: 1,
  name: 'Jane Doe',
  email: 'jane@example.com',
};

export const createMockRouter = (overrides = {}) => ({
  pathname: '/',
  query: {},
  push: () => Promise.resolve(),
  ...overrides,
});
```

### Migration: Storybook → Cosmos

```typescript
// BEFORE: Button.stories.tsx (Storybook CSF 3.0)
const meta = {
  component: Button,
  args: { children: 'Click me' },
} satisfies Meta<typeof Button>;
export default meta;

export const Primary: StoryObj = {
  args: { variant: 'primary' },
};

export const Secondary: StoryObj = {
  args: { variant: 'secondary' },
};

// ...
```

### Migration: Cosmos → Storybook

```typescript
// BEFORE: Button.fixture.tsx (Cosmos)
import { useFixtureSelect } from 'react-cosmos/client';
import { Button } from './Button';

export default () => {
  const [variant] = useFixtureSelect('variant', {
    options: ['primary', 'secondary'],
    defaultValue: 'primary',
  });
  return <Button variant={variant}>Click me</Button>;
};

// AFTER: Button.stories.tsx (Storybook CSF 3.0)
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';
// ...
```

---

## Cosmos Configuration Reference

### Full cosmos.config.json

```json
{
  "plugins": ["react-cosmos-plugin-vite"],
  "staticPath": "public",
  "watchDirs": ["src"],
  "exclude": [
    "**/*.test.*",
    "**/*.spec.*",
    "**/*.stories.*",
    "**/node_modules/**"
  ],
  "dom": {
    "containerQuerySelector": "#root"
  },
  "ui": {
    "playgroundUrl": "http://localhost:5050"
// ...
```

### TypeScript Setup

```json
// tsconfig.json - ensure Cosmos types
{
  "compilerOptions": {
    "types": ["react-cosmos"]
  }
}
```

## React Cosmos 7 (2024-2025)

### Key Changes from v6

| Feature | v6 | v7 |
|---------|----|----|
| React version | 18 | 18 + **19 support** |
| Next.js | 14 | **15 support** |
| Vite plugin | Manual index.html | **Auto-generated** |
| Remote rendering | Basic | **Stable over network** |
| Mobile UI | Not supported | **Slide panel** |

### Installation (v7)

```bash
npm install --save-dev react-cosmos@latest react-cosmos-plugin-vite@latest
```

### Vite Plugin Auto-Config (v7)

```json
// cosmos.config.json (v7 — minimal)
{
  "plugins": ["react-cosmos-plugin-vite"],
  "staticPath": "public"
}
```

### Lazy Mode

Delays fixture imports until opened. Significantly improves startup for large libraries.

```json
// cosmos.config.json
{
  "plugins": ["react-cosmos-plugin-vite"],
  "lazy": true
}
```

### Remote Rendering (v7)

Preview fixtures across multiple browsers and resolutions simultaneously.

```bash
# Start Cosmos in server mode
npx cosmos --host 0.0.0.0

# Connect from another device at http://<local-ip>:5050
```

### Fixture Options API (v6.2+)

```typescript
// Card.fixture.tsx
export default {
  options: {
    fixtureId: { name: 'Card / Default' },
    viewport: { width: 375, height: 667 },
  },
  default: <Card title="Default" />,
};
```
