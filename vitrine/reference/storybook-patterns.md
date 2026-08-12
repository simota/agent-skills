# Storybook Patterns & Templates

Comprehensive CSF 3.0 templates, Storybook 8.5+ features, and best practices.

---

## CSF 3.0 Templates

### Basic Component Story

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent, expect } from '@storybook/test';
import { ComponentName } from './ComponentName';

const meta = {
  title: 'Category/ComponentName',
  component: ComponentName,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'Component description here',
      },
    },
  },
// ...
```

### Form Component Story

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent, expect } from '@storybook/test';
import { Input } from './Input';

const meta = {
  title: 'Forms/Input',
  component: Input,
  tags: ['autodocs'],
  argTypes: {
    type: { control: 'select', options: ['text', 'email', 'password', 'number'] },
    size: { control: 'select', options: ['sm', 'md', 'lg'] },
  },
} satisfies Meta<typeof Input>;

export default meta;
// ...
```

---

## Storybook 8.5+ Features

### Vitest Browser Mode Integration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import { storybookTest } from '@storybook/experimental-addon-test/vitest-plugin';

export default defineConfig({
  plugins: [storybookTest()],
  test: {
    browser: {
      enabled: true,
      provider: 'playwright',
      name: 'chromium',
    },
    setupFiles: ['.storybook/vitest.setup.ts'],
  },
});
// ...
```

### React Server Components (RSC) Stories

```typescript
// ServerComponent.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ServerComponent } from './ServerComponent';

const meta = {
  title: 'RSC/ServerComponent',
  component: ServerComponent,
  parameters: {
    // Mark as server component for proper rendering
    nextjs: { appDirectory: true },
  },
  tags: ['autodocs'],
} satisfies Meta<typeof ServerComponent>;

export default meta;
// ...
```

### @storybook/test (Unified Testing)

```typescript
import { fn, expect, within, userEvent, waitFor } from '@storybook/test';
import type { Meta, StoryObj } from '@storybook/react';
import { Form } from './Form';

const meta = {
  component: Form,
  args: {
    // Type-safe mock functions
    onSubmit: fn(),
    onCancel: fn(),
  },
} satisfies Meta<typeof Form>;

export default meta;
type Story = StoryObj<typeof meta>;
// ...
```

### Portable Stories (Test Reuse)

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta = {
  component: Button,
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { variant: 'primary', children: 'Click me' },
};

// ...
```

### beforeEach / afterEach Lifecycle

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { within, userEvent } from '@storybook/test';
import { Modal } from './Modal';

const meta = {
  component: Modal,
  beforeEach: async () => {
    localStorage.clear();
  },
  afterEach: async () => {
    // Cleanup
  },
} satisfies Meta<typeof Modal>;

export default meta;
// ...
```

### Tags for Organization & Filtering

```typescript
const meta = {
  component: Button,
  tags: [
    'autodocs',      // Auto-generate docs
    'component',     // Category tag
    'visual-test',   // Include in visual regression
    '!dev',          // Exclude from dev sidebar
    '!test',         // Exclude from test runs
  ],
} satisfies Meta<typeof Button>;

// Filter in test runner:
// test-storybook --tags="component"
// test-storybook --tags="visual-test"
```

### Theme Testing (Dark Mode)

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta = {
  component: Button,
  parameters: {
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
      ],
    },
  },
  decorators: [
// ...
```

---

## MDX 3 Documentation

### Component Documentation

```mdx
{/* Button.mdx */}
import { Meta, Stories, Primary, Controls, Story } from '@storybook/blocks';
import * as ButtonStories from './Button.stories';

<Meta of={ButtonStories} />

# Button

A button component used as the trigger for user actions.

## Usage

\`\`\`tsx
import { Button } from '@/components/Button';

// ...
```

### MDX with Custom Blocks

```mdx
{/* ComponentDoc.mdx */}
import { Meta, Canvas, Source } from '@storybook/blocks';
import * as Stories from './Component.stories';

<Meta of={Stories} />

# Component Name

## Interactive Demo

<Canvas of={Stories.Default} />

## Code Example

<Source of={Stories.Default} />
// ...
```

---

## Figma Integration

### Figma → Storybook Sync

```typescript
// .storybook/preview.ts
import { withDesign } from 'storybook-addon-designs';

export default {
  decorators: [withDesign],
  parameters: {
    design: {
      type: 'figma',
      url: 'https://www.figma.com/file/xxx',
    },
  },
};

// Button.stories.tsx
export const Primary: Story = {
// ...
```

### Design Tokens from Figma

```typescript
// tokens.ts - Generated from Figma Variables
export const tokens = {
  colors: {
    primary: { 50: '#eff6ff', 500: '#3b82f6', 900: '#1e3a8a' },
  },
  spacing: { 1: '4px', 2: '8px', 4: '16px' },
  radius: { sm: '4px', md: '8px', lg: '12px' },
};

// .storybook/preview.ts
import { tokens } from '../src/tokens';

export default {
  parameters: {
    backgrounds: {
// ...
```

---

## Audit Report Format

```markdown
## Vitrine Audit Report: [Project Name]

### Coverage Summary

| Category | Total Components | With Stories | Coverage |
|----------|------------------|--------------|----------|
| Atoms | X | Y | Z% |
| Molecules | X | Y | Z% |
| Organisms | X | Y | Z% |
| Templates | X | Y | Z% |
| **Total** | **X** | **Y** | **Z%** |

### Story Quality Scores

| Component | Variants | A11y | Interactions | Docs | Grade |
...
```

---

## Forge Enhancement Workflow

### Forge Preview → Vitrine Full Coverage

```
Forge (Preview Story)              Vitrine (Full Story)
├─ Default state only              ├─ All variants
├─ Prototypes/ hierarchy           ├─ Components/ hierarchy
├─ tags: ['prototype']             ├─ tags: ['autodocs', 'component']
├─ No interactions                 ├─ Play functions
├─ No a11y config                  ├─ A11y rules configured
└─ TODO comments                   └─ MDX documentation
```

### Enhancement Checklist

```markdown
## Vitrine Enhancement Checklist

### Story Location
- [ ] Move from `Prototypes/` to appropriate category
- [ ] Update title path in meta

### Variant Coverage
- [ ] Add size variants (sm, md, lg)
- [ ] Add color/theme variants
- [ ] Add state variants (default, hover, focus, active, disabled)
- [ ] Add content variants (empty, minimal, maximal)

### Interaction Tests
- [ ] Add play function for primary interaction
- [ ] Add keyboard navigation test
...
```

### Enhancement Template

```typescript
// BEFORE (Forge generated)
const meta = {
  component: ComponentName,
  title: 'Prototypes/ComponentName',
  tags: ['prototype'],
} satisfies Meta<typeof ComponentName>;

export const Preview: Story = {
  args: { /* default only */ },
};

// AFTER (Vitrine enhanced)
const meta = {
  component: ComponentName,
  title: 'Components/ComponentName',
// ...
```

## Storybook 9 / 10 New Features (2025)

### Vitest Addon (Official Integration)

`@storybook/experimental-addon-test` became official in Storybook 9. Runs stories in Vitest browser mode with unified Interaction, Accessibility, and Visual testing.

```typescript
// vitest.config.ts (Storybook 9 recommended)
import { defineConfig } from 'vitest/config';
import { storybookTest } from '@storybook/experimental-addon-test/vitest-plugin';

export default defineConfig({
  plugins: [
    storybookTest({ storybookScript: 'npm run storybook -- --ci' }),
  ],
  test: {
    browser: {
      enabled: true,
      provider: 'playwright',
      name: 'chromium',
      headless: true,
    },
    setupFiles: ['.storybook/vitest.setup.ts'],
  },
});
```

```typescript
// .storybook/vitest.setup.ts
import { setProjectAnnotations } from '@storybook/react';
import * as previewAnnotations from './preview';

const project = setProjectAnnotations([previewAnnotations]);
beforeAll(project.beforeAll);
```

### Tag-Based Filtering (Storybook 9)

Control test and documentation targets with fine-grained tags.

```typescript
const meta = {
  component: Button,
  tags: [
    'autodocs',      // auto-generate docs
    'visual-test',   // Chromatic / Playwright target
    '!test',         // exclude from Vitest
    '!dev',          // exclude from sidebar
  ],
} satisfies Meta<typeof Button>;
```

### CSF Factories (Storybook 10)

Type-safe story definitions with less boilerplate.

```typescript
// CSF Factories (Storybook 10)
import { config } from '#.storybook/preview';

const { story } = config.meta({ component: Button });
export const Primary = story({ args: { variant: 'primary' } });
```

## Play Function Best Practices (Storybook 9)

### mount Hook for Before-Render Setup

```typescript
export const WithPreloadedData: Story = {
  play: async ({ canvasElement, mount }) => {
    await mount(<Button variant="primary">Click me</Button>);
    const canvas = within(canvasElement);
    await userEvent.click(canvas.getByRole('button'));
    await expect(canvas.getByText('Clicked!')).toBeInTheDocument();
  },
};
```

### step for Complex Flow Organization

```typescript
export const CheckoutFlow: Story = {
  play: async ({ canvasElement, step }) => {
    const canvas = within(canvasElement);

    await step('Add item to cart', async () => {
      await userEvent.click(canvas.getByRole('button', { name: 'Add' }));
      await expect(canvas.getByText('Cart: 1')).toBeInTheDocument();
    });

    await step('Checkout', async () => {
      await userEvent.click(canvas.getByRole('button', { name: 'Buy' }));
      await expect(canvas.getByRole('dialog')).toBeVisible();
    });
  },
};
```

### Accessibility Check in Play Functions

```typescript
import { checkA11y } from '@storybook/addon-a11y/playwright';

export const AccessibleForm: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.tab();
    await checkA11y(canvasElement);
  },
};
```

## Portable Stories (composeStories)

Reuse stories in Jest / Vitest unit tests. Eliminates test setup duplication.

### Setup (Vitest)

```typescript
// vitest.setup.ts
import { setProjectAnnotations } from '@storybook/react';
import * as previewAnnotations from './.storybook/preview';

const annotations = setProjectAnnotations([previewAnnotations]);
beforeAll(annotations.beforeAll);
```

### composeStories (All Stories)

```typescript
// Button.test.tsx
import { render, screen } from '@testing-library/react';
import { composeStories } from '@storybook/react';
import * as stories from './Button.stories';

const { Primary, Secondary, Disabled } = composeStories(stories);

describe('Button', () => {
  test('Primary renders', () => {
    render(<Primary />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  test('Disabled state', () => {
    render(<Disabled />);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  test('Runs play function', async () => {
    const { container } = render(<Primary />);
    await Primary.run({ canvasElement: container });
  });
});
```

### composeStory (Single Story + Overrides)

```typescript
import { composeStory } from '@storybook/react';
import meta, { Primary as PrimaryStory } from './Button.stories';

const PrimaryJa = composeStory(PrimaryStory, meta, {
  globals: { locale: 'ja' },
});

test('Japanese locale', async () => {
  const { container } = render(<PrimaryJa />);
  await PrimaryJa.run({ canvasElement: container });
});
```

## Design Token Documentation

### storybook-design-token Addon

Extract tokens from CSS/SCSS annotations and generate visual documentation.

```bash
npm install --save-dev storybook-design-token
```

```typescript
// .storybook/main.ts
export default {
  addons: ['storybook-design-token'],
};
```

### CSS Annotations

```css
/* tokens.css */
:root {
  /**
   * @tokens Colors
   * @presenter Color
   */
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;

  /**
   * @tokens Spacing
   * @presenter Spacing
   */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-4: 16px;
}
```

### MDX Integration

```mdx
{/* DesignTokens.mdx */}
import { Meta } from '@storybook/blocks';
import { DesignTokenDocBlock } from 'storybook-design-token/dist/doc-blocks';

<Meta title="Design System/Tokens" />

# Design Tokens

<DesignTokenDocBlock categoryName="Colors" viewType="card" />
<DesignTokenDocBlock categoryName="Spacing" viewType="table" />
```


---

## Per-Recipe Authoring Rules (SKILL.md excerpt)

- For `interaction` recipe: import test utilities exclusively from `@storybook/test` (Storybook 8+ unified package) — never from deprecated `@storybook/jest` or `@storybook/testing-library`. Always `await` `userEvent` calls (v14+ is async), scope queries via `within(canvasElement)`, and prefer `findBy*`/`waitFor` over `waitForTimeout`. Use `step()` to group multi-stage flows for the Interactions panel. Stop play functions at the component boundary; cross-page flows hand off to Voyager.

- For `mdx` recipe: start every component with Autodocs (`tags: ['autodocs']`); promote to hand-authored MDX only when narrative, multi-page guides, or custom JSX is required. Always bind via `<Meta of={meta} />`, embed stories with `<Canvas of={Story} />` (never re-define stories inline — Storybook 7+ deprecates `<Story name="...">` with JSX children), and register `'../src/**/*.mdx'` in `.storybook/main.ts`. Generate prop tables with `<ArgTypes>` rather than hand-written Markdown.

- For `cosmos` recipe: recommend React Cosmos only for React-only projects valuing minimal config and fastest hot reload, where Chromatic / MCP / MDX / multi-framework support are not required. Coexistence with Storybook is permitted short-term but designate one tool as primary to avoid maintenance drift. Cosmos has no native play-function or VRT — wire Vitest browser-mode for interactions and Playwright VRT/Lost Pixel/Loki for visual diff.


## Output Routing Table (SKILL.md excerpt)

| Signal | Approach | Primary output | Read next |
|--------|----------|----------------|-----------|
| `story`, `storybook`, `CSF`, `stories.tsx` | Story creation (CSF 3.0) | Story files + autodocs | `reference/storybook-patterns.md` |
| `fixture`, `cosmos`, `fixture.tsx` | Cosmos fixture creation | Fixture files + decorators | `reference/react-cosmos-guide.md` |
| `audit`, `coverage`, `missing stories` | Story coverage audit | Health report (reuse rate, a11y pass rate, design-code alignment) + action items | `reference/storybook-patterns.md` |
| `visual regression`, `VRT`, `chromatic`, `screenshot`, `applitools` | Visual regression setup | Test config + CI workflow | `reference/visual-regression.md` |
| `migrate`, `CSF 2`, `upgrade storybook`, `storybook 9`, `storybook 10`, `ESM migration` | CSF / Storybook version migration (8→9, 9→10 ESM-only) | Updated story files + addon-vitest config + ESM conversion + report | `reference/storybook-patterns.md` |
| `metrics`, `design system health`, `reuse rate` | Design system metrics | Metrics dashboard spec (reuse rate, a11y pass, alignment) | `reference/storybook-patterns.md` |
| `histoire`, `ladle`, `alternative` | Alternative tool setup | Tool config + story files | `reference/framework-alternatives.md` |
| `play function`, `interaction test` | Interaction testing | Play functions + test setup | `reference/storybook-patterns.md` |
| `portable stories`, `composeStories` | Story reuse in tests | Test files with composed stories | `reference/storybook-patterns.md` |
| `design token`, `token docs` | Token documentation | MDX docs + token config | `reference/storybook-patterns.md` |
| `test codegen`, `record test`, `no-code test` | Test Codegen setup | Test Codegen addon config + recorded play functions | `reference/storybook-patterns.md` |
| `sb.mock`, `automock`, `module mock` | Module mocking with sb.mock | Mock config + story files | `reference/storybook-patterns.md` |
| `story generation`, `generate stories from UI` | Story Generation from UI | Generated story files | `reference/storybook-patterns.md` |
| `CSF factories`, `type-safe stories` | CSF factories migration (9.1+) | Updated story files with factories API | `reference/storybook-patterns.md` |
| `.test method`, `inline test`, `story test` | CSF Factories `.test` attachment | Stories with `.test` + tag exclusion config | `reference/storybook-patterns.md` |
| `tag filter`, `hide stories`, `sidebar filter` | Tag exclusion filtering | Storybook config with tag-based inclusion/exclusion | `reference/storybook-patterns.md` |
| `mcp`, `addon-mcp`, `AI manifest`, `agent context` | MCP addon setup for AI agent integration | addon-mcp config + manifest optimization | `reference/storybook-patterns.md` |
| `RSC`, `server component`, `react server` | RSC story creation (experimental) | Story files with module mocking for async server components | `reference/storybook-patterns.md` |
| `git change`, `change detection`, `modified stories` | Git change detection filtering (10.3+) | Storybook config with status-value filtering | `reference/storybook-patterns.md` |
| unclear story request | Story creation (default) | Story files + autodocs | `reference/storybook-patterns.md` |
