# CSS Token Architecture Anti-Patterns

Purpose: Use this reference when CSS token structure, scope, theming layers, or variable resolution becomes hard to understand or maintain.

## Contents

- CSS token anti-patterns
- Placement rules
- Cascade layer guidance
- Theme switching rules
- Framework cautions
- Muse review checklist

## CSS Token Anti-Patterns

| ID | Anti-pattern | Signal | Correction |
|----|--------------|--------|-----------|
| `CT-01` | Over-nested variables | `var()` resolution chain exceeds `2` steps or reaches `3+` nested stages | Flatten references and resolve values more directly |
| `CT-02` | Raw values mixed with tokens | Components use `HEX`, `RGB`, or ad hoc spacing beside tokens | Replace raw values with semantic tokens |
| `CT-03` | Global pollution | `:root` holds every component token and exceeds roughly `100` tokens | Keep global scope for primitives and semantics; scope component tokens locally |
| `CT-04` | Unstructured categories | Colors, spacing, shadows, and component tokens are mixed together | Group by category and layer |
| `CT-05` | Specificity war | Token overrides rely on `!important` | Use `@layer` and predictable cascade order |
| `CT-06` | Unused token accumulation | Component removal leaves orphaned tokens behind | Audit and delete unused tokens regularly |
| `CT-07` | Missing fallbacks | `var(--token)` has no safe fallback where one is needed | Add fallback values when runtime absence is possible |

## Placement Rules

- `:root`: primitives and semantics only.
- Theme selectors: mode-specific semantic overrides.
- Component scope: component aliases and internal composition.

## Cascade Layer Guidance

Suggested order:

1. tokens
2. base
3. components
4. utilities
5. overrides

Rules:

- Use cascade layers instead of specificity fights.
- Do not solve architecture problems with `!important`.

## Theme Switching Rules

- Theme switching should remap semantics, not rewrite component code.
- Prefer theme wrappers such as `[data-theme="dark"]`.
- Keep fallback behavior explicit.

## Framework Cautions

| Framework | Caution |
|----------|---------|
| Tailwind v4 | Keep semantic aliases visible in `@theme`; do not duplicate raw values blindly |
| Panda CSS | Use semantic tokens for mode-aware values; avoid bypassing them in components |
| CSS Modules / scoped CSS | Consume global token vocabulary instead of cloning values locally |

## Muse Review Checklist

- `CT-01`: flatten nested variable chains.
- `CT-02`: remove raw color and spacing values from components.
- `CT-03`: move component tokens out of `:root` when the root set grows too large.
- `CT-05`: replace `!important` fixes with cascade-layer structure.
- `CT-07`: add fallbacks where missing tokens could break rendering.
