# Framework Alternatives

Component catalog tools beyond Storybook for different frameworks and use cases.

---

## Tool Comparison

| Tool | Framework | Format | Docs | Addons | Performance | Best For |
|------|-----------|--------|------|--------|-------------|----------|
| **Storybook** | React/Vue/Svelte/Angular | CSF 3.0 | Rich (MDX) | 400+ | Medium | Design systems |
| **React Cosmos** | React | Fixtures | Minimal | Built-in | Fast | React dev |
| **Histoire** | Vue/Svelte | Stories | Built-in | Growing | Fast | Vue/Svelte |
| **Ladle** | React | CSF-like | Basic | Limited | Very fast | Large React codebases |
| **Storybook for Svelte** | Svelte | CSF 3.0 | Full | Full | Medium | Svelte design systems |

---

## Histoire (Vue / Svelte)

### Overview

Histoire is a story-based component explorer built specifically for Vue and Svelte, offering a lightweight alternative to Storybook with native framework integration.

### Vue Setup

```bash
npm install --save-dev histoire @histoire/plugin-vue
```

```typescript
// histoire.config.ts
import { defineConfig } from 'histoire';
import { HstVue } from '@histoire/plugin-vue';

export default defineConfig({
  plugins: [HstVue()],
  setupFile: '/src/histoire-setup.ts',
  tree: {
    groups: [
      { id: 'atoms', title: 'Atoms' },
      { id: 'molecules', title: 'Molecules' },
      { id: 'organisms', title: 'Organisms' },
    ],
  },
});
```

### Vue Story Example

```vue
<!-- Button.story.vue -->
<script setup lang="ts">
import Button from './Button.vue';

const variants = ['primary', 'secondary', 'ghost'] as const;
</script>

<template>
  <Story title="Components/Button" group="atoms">
    <!-- Default variant -->
    <Variant title="Default">
      <Button>Click me</Button>
    </Variant>

    <!-- All variants -->
    <Variant title="All Variants">
      <div style="display: flex; gap: 1rem">
        <Button v-for="v in variants" :key="v" :variant="v">
          {{ v }}
        </Button>
      </div>
    </Variant>

    <!-- With controls -->
    <Variant title="Playground">
      <template #controls="{ state }">
        <HstText v-model="state.label" title="Label" />
        <HstSelect v-model="state.variant" title="Variant" :options="variants" />
        <HstCheckbox v-model="state.disabled" title="Disabled" />
      </template>
      <template #default="{ state }">
        <Button :variant="state.variant" :disabled="state.disabled">
          {{ state.label }}
        </Button>
      </template>
    </Variant>

    <!-- Disabled state -->
    <Variant title="Disabled">
      <Button disabled>Disabled</Button>
    </Variant>
  </Story>
</template>
```

### Svelte Setup (Histoire)

```bash
npm install --save-dev histoire @histoire/plugin-svelte
```

```typescript
// histoire.config.ts
import { defineConfig } from 'histoire';
import { HstSvelte } from '@histoire/plugin-svelte';

export default defineConfig({
  plugins: [HstSvelte()],
});
```

### Svelte Story Example

```svelte
<!-- Button.story.svelte -->
<script lang="ts">
  import type { Hst } from '@histoire/plugin-svelte';
  import Button from './Button.svelte';

  export let Hst: Hst;

  let variant = 'primary';
  let disabled = false;
</script>

<Hst.Story title="Components/Button" group="atoms">
  <Hst.Variant title="Default">
    <Button>Click me</Button>
  </Hst.Variant>

  <Hst.Variant title="Playground">
    <svelte:fragment slot="controls">
      <Hst.Select bind:value={variant} title="Variant"
        options={['primary', 'secondary', 'ghost']} />
      <Hst.Checkbox bind:value={disabled} title="Disabled" />
    </svelte:fragment>
    <Button {variant} {disabled}>Button</Button>
  </Hst.Variant>
</Hst.Story>
```

---

## Ladle (React - Lightweight)

### Overview

Ladle is a drop-in replacement for Storybook that uses Vite for near-instant startup and hot module replacement. It supports a subset of CSF format.

### Setup

```bash
npm install --save-dev @ladle/react
```

```json
// package.json
{
  "scripts": {
    "ladle": "ladle serve",
    "ladle:build": "ladle build"
  }
}
```

### Configuration

```typescript
// .ladle/config.mjs
export default {
  stories: 'src/**/*.stories.{ts,tsx}',
  port: 61000,
  addons: {
    a11y: { enabled: true },
    action: { enabled: true },
    control: { enabled: true },
    mode: { enabled: true },
    rtl: { enabled: true },
    source: { enabled: true },
    theme: { enabled: true },
    width: { enabled: true },
  },
};
```

### Story Example (CSF-compatible)

```typescript
// Button.stories.tsx (Ladle - CSF-like)
import type { Story } from '@ladle/react';
import { Button } from './Button';

export const Primary: Story = () => (
  <Button variant="primary">Primary Button</Button>
);

// With args controls
Primary.args = {
  variant: 'primary',
  children: 'Primary Button',
};

Primary.argTypes = {
  variant: {
    control: { type: 'select' },
    options: ['primary', 'secondary'],
  },
};

export const AllVariants: Story = () => (
  <div style={{ display: 'flex', gap: '1rem' }}>
    <Button variant="primary">Primary</Button>
    <Button variant="secondary">Secondary</Button>
    <Button variant="ghost">Ghost</Button>
  </div>
);

// Meta configuration
export default {
  title: 'Components/Button',
};
```

### Global Provider

```typescript
// .ladle/components.tsx
import type { GlobalProvider } from '@ladle/react';
import { ThemeProvider } from '../src/theme';

export const Provider: GlobalProvider = ({ children }) => (
  <ThemeProvider>{children}</ThemeProvider>
);
```

### Ladle vs Storybook Performance

| Metric | Storybook | Ladle |
|--------|-----------|-------|
| Cold start | 5-15s | <1s |
| HMR | 1-3s | <100ms |
| Build (100 stories) | 30-60s | 5-10s |
| Bundle size | ~5MB | ~500KB |

---

## Storybook for Svelte

### Setup

```bash
npx storybook@latest init --type svelte
```

### Svelte CSF 3.0 Story

```typescript
// Button.stories.ts
import type { Meta, StoryObj } from '@storybook/svelte';
import Button from './Button.svelte';

const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: { control: 'select', options: ['primary', 'secondary'] },
  },
} satisfies Meta<Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { variant: 'primary', label: 'Click me' },
};

export const Secondary: Story = {
  args: { variant: 'secondary', label: 'Click me' },
};
```

### Svelte Native Story Format

```svelte
<!-- Button.stories.svelte (Svelte CSF) -->
<script context="module">
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import Button from './Button.svelte';

  const { Story } = defineMeta({
    title: 'Components/Button',
    component: Button,
    tags: ['autodocs'],
  });
</script>

<Story name="Primary" args={{ variant: 'primary', label: 'Click me' }} />

<Story name="All Variants">
  <div style="display: flex; gap: 1rem;">
    <Button variant="primary">Primary</Button>
    <Button variant="secondary">Secondary</Button>
    <Button variant="ghost">Ghost</Button>
  </div>
</Story>
```

---

## Storybook for Vue

### Vue CSF 3.0 Story

```typescript
// Button.stories.ts
import type { Meta, StoryObj } from '@storybook/vue3';
import Button from './Button.vue';

const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: { control: 'select', options: ['primary', 'secondary'] },
    onClick: { action: 'clicked' },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { variant: 'primary', label: 'Click me' },
};

export const WithSlot: Story = {
  render: (args) => ({
    components: { Button },
    setup() { return { args }; },
    template: '<Button v-bind="args"><template #icon>★</template>With Icon</Button>',
  }),
};
```

---

## Decision Guide

### Choose Storybook When:
- Building a design system with comprehensive documentation
- Need rich addon ecosystem (a11y, Chromatic, Figma, etc.)
- Team includes designers who review components
- Multi-framework project (React + Vue + Svelte)

### Choose React Cosmos When:
- React-only project with fast iteration needs
- Performance is critical (large component library)
- Prefer fixture-based approach over story-based
- Want zero-config setup with Vite

### Choose Histoire When:
- Vue or Svelte project
- Want native framework integration without adapters
- Prefer lightweight tooling with built-in controls
- Don't need the full Storybook addon ecosystem

### Choose Ladle When:
- React project where Storybook is too slow
- Need near-instant startup and HMR
- Can live with fewer addons
- Want CSF-compatible format for easy migration

### Use Multiple Tools:
- **Cosmos (dev) + Storybook (docs)**: Best of both worlds for React
- **Histoire (dev) + Storybook (docs)**: Vue/Svelte equivalent
- **Ladle (dev) + Chromatic (visual)**: Fast dev with visual regression

## AI-Assisted Story Generation (2025)

### Approach Comparison

| Approach | Tool | Characteristics |
|----------|------|----------------|
| LLM prompt | Claude Code / GPT | Conversational CSF 3.0 generation |
| CLI tool | auto-story-generator | Prop type analysis + auto-generation |
| PR integration | Claude Code + hooks | Auto-commit stories on PR creation |
| IDE plugin | Cursor / Copilot | Right-click component to generate |

### auto-story-generator Addon

```bash
npm install --save-dev @takuma-ru/auto-story-generator
```

```typescript
// .storybook/main.ts
export default {
  addons: [
    {
      name: '@takuma-ru/auto-story-generator',
      options: {
        fileType: 'tsx',
        componentPath: 'src/components/**/*.tsx',
      },
    },
  ],
};
```

### Claude Code Story Generation Prompt

```markdown
<!-- .claude/commands/generate-story.md -->
Read the component file and generate a CSF 3.0 story:
- Use `satisfies Meta<typeof ComponentName>`
- Set controls based on prop types (boolean → checkbox, union → select)
- Add play functions for interactive elements
- Include `tags: ['autodocs']`
- Create at least 3 variants (Default, Loading/Disabled, Error)
```
