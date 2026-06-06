# Elevation Tokens Reference

Purpose: Define elevation as a semantic surface system — not a list of `box-shadow` strings. Elevation tokens map z-depth tiers (`surface-1` ... `surface-5`) to layered shadow recipes that adapt to light/dark mode. The goal: a designer can ask "what's the resting elevation of a card?" and get a single token, while the rendered shadow remains theme-correct, accessible, and consistent across components.

## Scope Boundary

- **muse `elevation`**: defines `elevation.*` tokens (shadow stacks) and `surface.*` tokens (semantic z-tiers). Authors layered-shadow recipes and dark-mode inversion strategy.
- **flow (elsewhere)**: implements elevation *transitions* (e.g. card lifts on hover) using these tokens. Does not define them.
- **vision (elsewhere)**: sets brand depth feel (flat / soft / dramatic) — direction only.
- **palette (elsewhere)**: fixes interaction affordance (clickability, focus states) — not elevation token values.
- **muse `theme`**: owns dark-mode color tokens; this reference owns dark-mode *shadow* tokens that compose with theme colors.

## Workflow

```
SURVEY    →  audit existing shadows: count distinct box-shadow values, find drift
              (e.g. card 0 1px 3px, modal 0 8px 24px, popover 0 4px 12px — 12 variants total)

DEFINE    →  choose tier count (5 is Material standard; 3 is enough for flat brands)
              author each tier as 2-3 layered shadows (key + ambient + optional rim)
              author dark-mode variants — usually higher opacity, plus optional inner-light rim
              map semantic surfaces (surface-1 = card, surface-3 = popover, surface-5 = modal)

VALIDATE  →  every elevation token has a dark-mode pair
              shadows compose without "muddy halo" on dark surfaces
              DTCG $type: shadow with array $value for layered shadows (v2025.10)

PRESENT   →  elevation ladder visual, light/dark token table, semantic surface mapping
              handoff to Artisan with surface-tier component mapping
```

## Elevation Scale

| Token | Tier | Use | Light shadow | Dark shadow strategy |
|-------|------|-----|--------------|---------------------|
| `elevation.0` | flat | Body, base canvas | `none` | `none` (use surface color shift instead) |
| `elevation.1` | resting | Cards, list items | `0 1px 2px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.10)` | `0 1px 2px rgba(0,0,0,0.40)` + lighter surface |
| `elevation.2` | raised | Buttons (hover), chips | `0 2px 4px rgba(0,0,0,0.06), 0 4px 6px rgba(0,0,0,0.08)` | `0 2px 4px rgba(0,0,0,0.50)` |
| `elevation.3` | floating | Popovers, dropdowns | `0 4px 8px rgba(0,0,0,0.08), 0 8px 16px rgba(0,0,0,0.10)` | `0 4px 12px rgba(0,0,0,0.60)` |
| `elevation.4` | overlay | Drawers, sticky bars | `0 8px 16px rgba(0,0,0,0.10), 0 16px 32px rgba(0,0,0,0.12)` | `0 8px 24px rgba(0,0,0,0.65)` |
| `elevation.5` | modal | Dialogs, full overlays | `0 16px 32px rgba(0,0,0,0.12), 0 24px 48px rgba(0,0,0,0.16)` | `0 16px 40px rgba(0,0,0,0.70)` |

Layered shadows (key + ambient) produce realistic depth — a single shadow at high blur looks like a fog patch, not a lifted surface.

## Semantic Surface Tiers

| Token | Maps to | Components |
|-------|---------|------------|
| `surface.0` | `elevation.0` | Page background |
| `surface.1` | `elevation.1` | Cards, panels, table rows |
| `surface.2` | `elevation.2` | Hover/raised state |
| `surface.3` | `elevation.3` | Menus, popovers, dropdowns |
| `surface.4` | `elevation.4` | Drawers, snackbars |
| `surface.5` | `elevation.5` | Modal dialogs, full-screen overlays |

Surface tokens decouple components from raw shadow values — components reference `surface.3`, not `elevation.3`.

## Dark-Mode Shadow Inversion

Material Design 3 guidance: dark mode reduces shadow visibility (low contrast against dark backgrounds). Two strategies:

| Strategy | Approach | Trade-off |
|----------|----------|-----------|
| **Higher opacity** | Same blur radii, alpha bumped 0.40-0.70 | Shadows visible but can feel heavy |
| **Surface-color shift** | Each elevation tier uses a *lighter* surface color (`#1E1E1E`, `#222`, `#262626`...); shadows are minimal | Cleaner, matches Material 3 — but requires surface color tokens per tier |

Recommended: combine — light surface shifts for tiers 1-3, modest shadows for tiers 4-5.

```jsonc
{
  "elevation": {
    "3": {
      "$value": [
        { "color": "{shadow.color.umbra}", "offsetX": "0", "offsetY": "4px", "blur": "8px", "spread": "0" },
        { "color": "{shadow.color.penumbra}", "offsetX": "0", "offsetY": "8px", "blur": "16px", "spread": "0" }
      ],
      "$type": "shadow"
    }
  }
}
```

DTCG v2025.10 supports shadow arrays natively — Style Dictionary v5 emits them as multi-layer `box-shadow`.

## Naming Conventions

- Numeric elevation: `elevation.{0..5}` — small integer ladder.
- Semantic surface: `surface.{0..5}` — same range, mapped 1:1.
- Shadow color tokens: `shadow.color.umbra` (key), `shadow.color.penumbra` (ambient), `shadow.color.rim` (optional dark-mode top edge).
- Dark variants live in resolver document or `[data-theme="dark"]`, not as separate tokens (`elevation.3.dark` is an anti-pattern — it leaks theme into the scale).

## Anti-Patterns

- Single-layer shadows (`box-shadow: 0 4px 12px rgba(0,0,0,0.1)`) — flat and foggy; no depth. Use 2-3 layered shadows.
- Elevation tier per component (`elevation.card`, `elevation.modal`) — couples scale to component names; reuse breaks when a popover needs the same shadow as a card.
- Hardcoded shadow strings in dark mode (`box-shadow: 0 4px 12px rgba(0,0,0,0.6)`) — inversion logic scattered across files; rename or theme-flip impossible.
- Using shadows alone for dark-mode depth — shadows on `#000` are nearly invisible. Always pair with surface color shifts.
- Excessive elevation tiers (8+ levels) — Material settled on 5 tiers because users cannot perceive more; extra steps create noise.
- Same shadow for hover and focus — shadows for *depth* and ring for *focus* are different signals; keep them separate (`elevation.*` vs `focus-ring.*`).
- Ignoring forced-colors mode — Windows High Contrast strips shadows; ensure surface boundaries are visible via border-color fallback.
- Animating elevation via raw box-shadow strings instead of token swaps — tokens enable theme-aware transitions; raw strings break when theme changes mid-animation.

## Handoff

- **To Artisan**: surface-tier mapping (Card → `surface.1`, Dialog → `surface.5`), elevation transition tokens for hover states.
- **To Flow**: elevation transition recipes (card lift: `surface.1` → `surface.2` over `duration.150`).
- **To Palette**: when elevation conflicts with focus visibility (heavy shadow on focused element drowns the ring), reconcile interaction-priority.
- **To Vitrine**: elevation ladder catalog with light/dark/forced-colors previews.
- **To Vision**: elevation policy review when brand expression requires flat (no shadows) vs. dramatic (heavy depth).
