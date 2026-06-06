# Design System Anti-Patterns

Purpose: Use this file when defining token architecture, screening design-system debt, or setting governance rules.

Contents:
- `DS-01` to `DS-08`
- token architecture
- theme strategy
- governance rules

## Anti-pattern Catalog

| ID | Anti-pattern | Risk | Response |
|----|--------------|------|----------|
| `DS-01` | Token sprawl | consistency collapse | use a `Reference -> Semantic -> Component` model |
| `DS-02` | Appearance-based naming | renaming pain on brand change | use semantic naming |
| `DS-03` | Hardcoded values | token drift | lint and CI checks |
| `DS-04` | Redundant tokens | confusion and maintenance cost | regular token audits |
| `DS-05` | Design/code naming mismatch | team misalignment | shared vocabulary |
| `DS-06` | Abrupt token deletion | downstream breakage | staged deprecation |
| `DS-07` | Theme-blind token model | dark-mode or multi-brand rewrite | theme-aware semantics |
| `DS-08` | Missing rationale and docs | misuse and drift | usage notes required |

## Token Architecture

| Layer | Role | Naming guidance |
|-------|------|-----------------|
| `Reference` | raw values only | `category.value` |
| `Semantic` | intent and theme mapping | `category.purpose.state` |
| `Component` | component-specific bindings | `component.property.variant.state` |

Good examples:
- `color.primary.default`
- `color.primary.hover`
- `text.heading.lg`
- `space.layout.section`

Bad examples:
- `color.blue`
- `--color1`
- `button-blue-big`
- `primary`

## Theme Strategy

- Keep components theme-agnostic.
- Switch themes by remapping semantic tokens to reference tokens.
- Support at least:
  - light/dark themes
  - high-contrast theme where required
  - reduced-motion handling

## Governance Rules

- New tokens must declare which layer they belong to.
- Token removals must follow deprecation: warning -> alternative -> removal.
- Detect hardcoded values in CI.
- Keep Figma Variables and code tokens aligned.
- Review `DS-01` to `DS-08` during `REVIEW` mode.

## AI-Readable Token Guidelines (2025-2026)

Tokens must carry semantic intent so AI tools make context-aware decisions:

| Quality | Example | Problem |
|---------|---------|---------|
| Good | `color-feedback-error` | AI understands intent |
| Good | `spacing-component-button-padding` | AI understands context |
| Bad | `color-red-500` | AI cannot infer purpose |
| Bad | `spacing-4` | AI cannot infer usage |

Additional anti-patterns:

| ID | Name | Symptom | Fix |
|----|------|---------|-----|
| `DS-09` | AI-unreadable tokens | AI generates wrong values | Add intent context to token names |
| `DS-10` | Static design system (no MCP) | AI agents lack real-time token/component data | Integrate Figma MCP server for live token sync |
| `DS-11` | Token/code naming divergence | AI suggestions break design system rules | Supply structured rules file to AI agents |

## Dark Mode Token Integration (2025-2026)

Semantic tokens must be theme-agnostic. Mode switching remaps semantic tokens to reference tokens.

Required semantic token categories:
- `color.background.surface` (not `color.white` / `color.gray-900`)
- `color.text.primary` / `color.text.secondary`
- `color.border.default`
- `color.feedback.error` / `warning` / `success` / `info`
- `color.interactive.primary` / `hover` / `active` / `disabled`

CSS `light-dark()` (modern approach):
```css
:root { color-scheme: light dark; }
.surface { background: light-dark(#ffffff, #111111); }
```

Anti-pattern DS-07 (Theme-blind token model) is the most common cause of dark-mode rewrites. Adopt semantic tokens from day one.
