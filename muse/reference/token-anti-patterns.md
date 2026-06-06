# Design Token Anti-Patterns

Purpose: Use this reference when token naming, hierarchy, reuse, lifecycle, or code/Figma alignment looks unstable.

## Contents

- Token anti-pattern catalog
- Naming rules
- Hierarchy rules
- Governance checks
- Muse review checklist

## Token Anti-Pattern Catalog

| ID | Anti-pattern | Signal | Risk | Correction |
|----|--------------|--------|------|-----------|
| `DT-01` | Over-tokenization | Token count `> component count x 3`; multiple tokens map to the same intent | Discovery and maintenance collapse | Tokenize at reusable group level; keep one-off values local |
| `DT-02` | Under-tokenization | Primitive tokens are used directly in product code | Theme changes require mass rewrites | Insert a semantic layer for product use |
| `DT-03` | Value-based naming | Names encode appearance instead of purpose | Brand or theme shifts break semantics | Rename by role, such as `color-text-secondary` |
| `DT-04` | Over-qualified naming | Names exceed `3-4` meaningful segments | Usage becomes error-prone | Keep names short and intent-driven |
| `DT-05` | Wrong mode targeting | Dark/light variants applied to typography or unrelated properties | Mode switching changes non-visual intent | Limit mode variants primarily to color and shadow |
| `DT-06` | Single-use tokens | A token appears in only one place | Token file bloat | Promote only values reused in `2+ components` |
| `DT-07` | Source mismatch | Figma and code diverge on names or values | Design and implementation drift | Establish one source of truth plus automated sync |
| `DT-08` | Unversioned change | Token changes have no lifecycle or changelog | Breaking impact is invisible | Require semantic versioning and changelog entries |

## Naming Rules

- Prefer purpose over appearance.
- Keep names scannable and stable.
- Use the same vocabulary across code, docs, and design files.

## Hierarchy Rules

- Product code should consume semantic tokens, not primitives.
- Component tokens should compose semantic tokens.
- Consolidate `3+` same-value tokens when they represent the same semantic meaning.

## Governance Checks

- Single-use token? Keep it local until reuse exists.
- Primitive used directly in a component? Route through a semantic alias.
- New token with no lifecycle note? Add state and rationale.
- Missing version or migration notes for a breaking token change? Block until documented.

## Muse Review Checklist

- `DT-01`: prune token sprawl and duplicated semantics.
- `DT-02`: add missing semantic aliases.
- `DT-03`: rename appearance-based tokens.
- `DT-06`: demote one-off tokens back to constants.
- `DT-07`: reconcile Figma and code before rollout.
