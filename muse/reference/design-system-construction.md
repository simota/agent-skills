# Design System Construction

Purpose: Use this reference when building or restructuring the token foundation, file layout, framework integration, or governance baseline for a design system.

## Contents

- Design system layers
- File structure
- Construction phases
- Health metrics
- Framework integration
- Visualization hooks

## Design System Layers

| Layer | Purpose | Typical artifacts |
|------|---------|-------------------|
| Token Foundation | Primitive and semantic token definitions | colors, spacing, typography, shadow, radius |
| Base Styles | Global resets and base mappings | theme roots, typography defaults, surface defaults |
| Component Tokenization | Component-level tokens and usage patterns | buttons, cards, forms, overlays |
| Documentation And Governance | Usage guidance, stories, ownership, drift control | Storybook, docs, lifecycle records |

## File Structure

```text
design-system/
  tokens/
    primitives/
    semantic/
    components/
  styles/
    base.css
    themes.css
  docs/
    guidelines.md
    lifecycle.md
  stories/
```

Rules:

- Tokens are the source of truth.
- Docs and stories must point back to the same token vocabulary.
- Component code should consume semantic or component tokens, not raw values.

## Construction Phases

### Phase 1: Token Foundation

- Define primitives and semantics.
- Set typography and spacing scales.
- Decide light/dark theme strategy.

### Phase 2: Base Styles

- Wire tokens into root styles and theme wrappers.
- Standardize surface, text, and focus defaults.

### Phase 3: Component Tokenization

- Replace hardcoded values.
- Introduce component-level tokens only when reuse or clarity justifies them.

### Phase 4: Documentation And Governance

- Publish stories and token usage docs.
- Track lifecycle states and ownership.
- Establish drift review cadence.

## Health Metrics

| Metric | Target | Meaning |
|-------|--------|---------|
| Token Coverage | `95%+` | Hardcoded values are exceptional, not normal |
| Dark Mode Support | `100%` | No light-only components remain |
| Component Token Usage | `100%` | Components use tokens instead of magic numbers |
| Documentation Currency | `< 1 sprint` stale | Docs keep up with actual implementation |

## Framework Integration

### CSS Custom Properties

- Default recommendation for broad compatibility.
- Use them as the cross-framework token source.

### Tailwind CSS v3

- Map tokens into `theme.extend`.
- Avoid duplicating token values in config and CSS if one source can generate both.

### Tailwind CSS v4

- Use `@theme` and generated CSS variables.
- Keep semantic aliases visible in CSS-first config.

### Panda CSS

- Use `semanticTokens` for mode-aware values.
- Avoid mixing Panda tokens with raw CSS values in components.

### CSS Modules / Scoped Styles

- Import and consume global tokens; do not recreate them locally.

### Vue / Svelte

- Keep tokens global and semantic.
- Scope only component-specific aliases when required.

## Visualization Hooks

Use Canvas when any of the following would unblock design system work:

- palette hierarchy diagrams
- typography scale diagrams
- spacing system diagrams
- dependency views for token adoption
