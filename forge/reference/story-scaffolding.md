# Story Scaffolding Reference

> Purpose: define when Forge should generate preview stories and how to hand them off to Showcase or Artisan.

## Contents

- Generation rules
- Storybook preview template
- React Cosmos fixture template
- Output structure
- `FORGE_TO_SHOWCASE`
- `ARTISAN_HANDOFF`
- Story trigger

## When to Generate Stories

| Scenario | Generate preview stories? |
|---|---|
| UI component prototype | Yes, recommended |
| Backend PoC | No |
| Complex multi-component page | Only for the main component |
| API mock demonstration only | No |

Forge generates a minimal preview story only. Full coverage belongs to Showcase.

## Storybook Preview Template

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { ComponentName } from './ComponentName';

const meta = {
  component: ComponentName,
  title: 'Prototypes/ComponentName',
  tags: ['prototype'],
  parameters: {
    docs: {
      description: {
        component: 'Prototype preview. Full stories are pending from Showcase.',
      },
    },
  },
} satisfies Meta<typeof ComponentName>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Preview: Story = {
  args: {},
};

// TODO(showcase): Add variants, interaction tests, and a11y configuration
```

## React Cosmos Fixture Template

```typescript
import { ComponentName } from './ComponentName';

export default {
  default: <ComponentName />,
  withProps: <ComponentName variant="primary" />,
};

// TODO(showcase): Add broader fixtures and decorators
```

## Story Output Structure

```text
feature/
├── ComponentName.tsx           # required
├── ComponentName.stories.tsx   # optional preview story
├── ComponentName.fixture.tsx   # optional Cosmos fixture
├── types.ts                    # required
├── handlers.ts                 # required
├── errors.ts                   # required
└── forge-insights.md           # required
```

## `FORGE_TO_SHOWCASE`

```markdown
## FORGE_TO_SHOWCASE: Story Enhancement Request

### Prototype Info
- Component: `[path/to/ComponentName.tsx]`
- Preview Story: `[path/to/ComponentName.stories.tsx]`
- Fixture: `[path/to/ComponentName.fixture.tsx]` (if present)

### Current Coverage
- ✅ Default state preview
- ❌ Variants
- ❌ State coverage
- ❌ Interaction tests
- ❌ Accessibility configuration
- ❌ MDX documentation

### Props to Cover
| Prop | Type | Values to test |
|---|---|---|
| variant | string | primary, secondary, outline |
| size | string | sm, md, lg |
| disabled | boolean | true, false |

### Requested Enhancements
1. Move from `Prototypes/` into the final story hierarchy
2. Add variant stories
3. Add interaction tests
4. Add accessibility configuration
5. Add documentation

### Notes
- [Anything learned during prototyping]
```

## `ARTISAN_HANDOFF`

```markdown
## ARTISAN_HANDOFF (from Forge)

### Prototype Summary
- Components: [List of prototyped components]
- Tech stack: [React/Vue + styling approach]
- Demo URL: [Local dev URL if running]

### Production Requirements
- [ ] Replace mock data with real API calls
- [ ] Add proper error handling
- [ ] Handle responsive edge cases
- [ ] Add loading and error states
- [ ] Add component tests

Suggested command: `/Artisan productionize [component]`
```

## Shared Tags Convention

| Tag | Meaning | Owner |
|---|---|---|
| `prototype` | Forge-generated and not production-ready | Forge |
| `autodocs` | Auto-generated documentation | Showcase |
| `visual-test` | Include in visual regression | Showcase |
| `component` | Production component story | Showcase |

## `ON_STORY_GENERATION` Trigger

```yaml
questions:
  - question: "Should Forge generate preview stories with this prototype?"
    header: "Stories"
    options:
      - label: "Yes - Storybook (Recommended)"
        description: "Generate a minimal Storybook preview story"
      - label: "Yes - React Cosmos"
        description: "Generate a React Cosmos fixture"
      - label: "Yes - Both"
        description: "Generate both Storybook and React Cosmos"
      - label: "No - Skip"
        description: "Showcase will create stories from scratch"
    multiSelect: false
```
