# Token Lifecycle Management

Purpose: Use this reference when introducing, adopting, deprecating, or removing tokens, or when a token change may affect multiple components or teams.

> **2026 lifecycle addition: AI-consumer surface stays in sync with the lifecycle.** A token's `STABLE` → `DEPRECATE` → `REMOVE` arc only completes when the **published DTCG JSON** (and any accompanying `tokens.md` / `llms.txt` reference) ships the updated value. AI coding assistants cache the token file from their last retrieval; an in-Figma deprecation that has not yet been pushed to the DTCG source-of-truth means agents keep generating UI against the obsolete token. Treat "DTCG JSON updated + AI-consumer surface refreshed" as a hard gate before `DEPRECATE → REMOVE`.

## Contents

- Lifecycle state machine
- Phase definitions
- Transition rules
- Proposal template
- Deprecation notice
- Migration guide
- Impact analysis
- Agent integration
- Version tagging

## Lifecycle State Machine

```text
PROPOSE -> ADOPT -> STABLE -> DEPRECATE -> REMOVE
```

## Phase Definitions

| State | Meaning | Typical duration | Entry condition | Exit condition |
|------|---------|------------------|-----------------|----------------|
| `PROPOSE` | New token under review with rationale | `1 sprint` | Token request submitted | Approved or rejected |
| `ADOPT` | Token is available and recommended while old value may coexist | `1-2 sprints` | Proposal approved | Used in `3+ components` |
| `STABLE` | Default token for product use | indefinite | Proven adoption | Replacement or redesign exists |
| `DEPRECATE` | Token is scheduled for removal and migration is active | `2 sprints` | Replacement defined | Usage reaches `0%` |
| `REMOVE` | Token is removed from source | after migration | Deprecation complete | N/A |

## Transition Rules

| Transition | Gate | Required action |
|-----------|------|-----------------|
| `PROPOSE -> ADOPT` | Clear rationale and naming fit | Add token, document usage, publish examples |
| `ADOPT -> STABLE` | Usage in `3+ components` | Remove temporary status note, add to documentation |
| `STABLE -> DEPRECATE` | Better replacement or structural change exists | Announce deprecation, publish migration guide |
| `DEPRECATE -> REMOVE` | Usage reaches `0%` and migration is complete | Remove token, close migration issue |

Rules:

- Ask first before deprecating or removing `STABLE` tokens.
- Treat rename as a migration, not as an in-place replacement.
- Breaking value changes follow semantic versioning.

## Token Proposal Template

```yaml
TOKEN_PROPOSAL:
  name:
  layer: Primitive | Semantic | Component
  purpose:
  replacement_for:
  expected_reuse:
  light_mode_value:
  dark_mode_value:
  breaking_change: false
  approver:
  review_required: true
  review_reason:
  rationale:
```

## Token Deprecation Notice

```md
## Token Deprecation Notice
- Deprecated token:
- Replacement token:
- Reason:
- Effective date:
- Removal target:
- Affected components:
```

### Migration Steps

1. Identify affected components and stories.
2. Update token references.
3. Verify light and dark mode.
4. Run token audit.
5. Confirm usage has dropped to `0%`.

### Deprecation Warning (CSS)

```css
/* DEPRECATED: replace --color-text-tertiary with --color-text-muted before removal */
```

### Deprecation Warning (Tailwind)

```ts
// DEPRECATED: use text-muted instead of text-tertiary
```

## Migration Guide Template

```yaml
TOKEN_MIGRATION:
  scope:
  mapping:
    - from:
      to:
  steps:
    - search_and_replace:
  rollback:
    strategy:
    risk:
  validation:
    - dark_mode
    - token_audit
    - docs
```

## Impact Analysis Checklist

### `PROPOSE -> ADOPT`

- Is the token reused or expected to be reused?
- Does it conflict with naming or existing semantics?
- Does dark mode need separate values?
- Has the approver accepted the proposal and is the review reason documented?

### `STABLE -> DEPRECATE`

- Which components, stories, and docs reference it?
- Is there a safe migration path?
- Does Ripple need to assess downstream impact?

### `DEPRECATE -> REMOVE`

- Has usage reached `0%`?
- Have docs and examples been updated?
- Is the semver impact recorded?
- Has Storybook usage dropped to zero and has a removal review completed?

## Integration With Other Agents

| Agent | Use it for |
|------|------------|
| Vision | Validate direction for major token changes |
| Palette | Re-check accessibility and UX clarity |
| Ripple | Impact analysis before stable deprecation or rename |
| Vitrine | Storybook and documentation updates |
| Judge | Review token migration consistency |
| Flow | Motion token changes |

## Version Tagging Convention

| Change | Version impact |
|-------|----------------|
| Non-breaking value adjustment | Patch |
| New token addition | Minor |
| Rename, removal, structural breaking change | Major |
