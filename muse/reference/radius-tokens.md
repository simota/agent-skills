# Radius Tokens Reference

Purpose: Border-radius is brand-personality made measurable. Sharp `0px` radii read as serious / industrial; large radii read as friendly / playful; pill (`9999px`) radii anchor input fields and CTAs in many modern brands. Radius tokens encode this *spectrum* as a system, with component-aware mappings so a single brand-personality lever can retune the whole product without touching components.

## Scope Boundary

- **muse `radius`**: defines `radius.*` scale, `corner-set.*` tokens (per-corner combinations), and component-radius mappings. Authors brand-personality spectrum (sharp ↔ rounded).
- **flow (elsewhere)**: implements radius *transitions* (e.g. card morphs on press). Does not define values.
- **vision (elsewhere)**: chooses brand personality (sharp / soft / pill) — direction only.
- **palette (elsewhere)**: fixes interaction affordance (hit-area, tap target). Radius affects perceived hit area but Muse owns the token; Palette owns the interaction call.
- **muse `tokens` / `theme`**: general token system and theming; route here for radius specifically.

## Workflow

```
SURVEY    →  audit current radii: count distinct values across components
              (e.g. button 4px, card 8px, modal 12px, input 6px, pill 9999px — 5 values, OK)
              detect off-scale radii (3px, 5px, 7px → likely accidents from imported designs)

DEFINE    →  pick 6-7 step scale (none / xs / sm / md / lg / xl / full)
              decide brand position on sharp ↔ rounded spectrum
              author corner-set tokens for asymmetric components (top-rounded sheet, etc.)
              map components → semantic radius (button → radius.md, card → radius.lg)

VALIDATE  →  W3C DTCG v2025.10: $type: dimension with px values
              cross-component visual coherence (modal corners ≥ card corners, never less)
              accessibility: don't lose hit-area when applying full-pill to small icons

PRESENT   →  radius scale visual ladder, brand-spectrum slider, component map
              handoff to Artisan with semantic-to-component table
```

## Radius Scale

| Token | Value | Use |
|-------|-------|-----|
| `radius.none` | `0px` | Sharp / industrial brand, data tables, spreadsheets |
| `radius.xs` | `2px` | Subtle softening — checkboxes, tags |
| `radius.sm` | `4px` | Small UI — buttons (compact), inputs (default) |
| `radius.md` | `8px` | Standard UI — buttons, inputs, small cards (default) |
| `radius.lg` | `12px` | Cards, panels, popovers |
| `radius.xl` | `16px` | Modal dialogs, hero cards, marketing surfaces |
| `radius.2xl` | `24px` | Expressive cards, illustration containers |
| `radius.full` | `9999px` | Pill buttons, avatars, badges, chips |

Anchor: `radius.md` (8px) is the SaaS/dashboard default; shift to `radius.lg` for consumer/marketing brands.

## Brand-Personality Spectrum

| Brand mode | Default button | Default card | Modal | Vibe |
|------------|----------------|--------------|-------|------|
| **Sharp** | `radius.none` | `radius.xs` | `radius.sm` | Industrial, B2B, data-heavy |
| **Crisp** | `radius.sm` | `radius.md` | `radius.md` | Modern enterprise (default SaaS) |
| **Soft** | `radius.md` | `radius.lg` | `radius.xl` | Consumer, friendly |
| **Pillowed** | `radius.lg` | `radius.xl` | `radius.2xl` | Playful, lifestyle |
| **Pill-first** | `radius.full` | `radius.lg` | `radius.xl` | Modern marketing, fintech |

Switching brand mode = swapping a single resolver document. Component code does not change.

## Component-Aware Radius

Components don't reference `radius.lg` directly — they reference `radius.component.{name}`:

| Component token | Maps to (Crisp default) | Notes |
|----------------|--------------------------|-------|
| `radius.component.button` | `{radius.md}` | Pill variant uses `{radius.full}` |
| `radius.component.input` | `{radius.sm}` | Slightly tighter than buttons |
| `radius.component.card` | `{radius.lg}` | Outer-most surface |
| `radius.component.modal` | `{radius.xl}` | Larger than card to feel "lifted" |
| `radius.component.popover` | `{radius.md}` | Smaller than card to feel "transient" |
| `radius.component.avatar` | `{radius.full}` | Always pill |
| `radius.component.badge` | `{radius.full}` | Always pill |
| `radius.component.tag` | `{radius.sm}` | Slight softening |
| `radius.component.toast` | `{radius.lg}` | Match card |
| `radius.component.image` | `{radius.md}` | Inside cards: inherit parent |

## Corner-Set Tokens (Asymmetric)

For sheets, tabs, and segmented surfaces:

| Token | Top-left | Top-right | Bottom-right | Bottom-left | Use |
|-------|----------|-----------|--------------|-------------|-----|
| `corner-set.top` | `radius.lg` | `radius.lg` | `0` | `0` | Bottom sheet, top-attached card |
| `corner-set.bottom` | `0` | `0` | `radius.lg` | `radius.lg` | Top sheet, bottom-attached toast |
| `corner-set.start` | `radius.md` | `0` | `0` | `radius.md` | Segmented control (first), RTL-aware |
| `corner-set.end` | `0` | `radius.md` | `radius.md` | `0` | Segmented control (last), RTL-aware |

Use logical properties (`border-start-start-radius`) so RTL flips automatically.

```jsonc
{
  "radius": {
    "md": { "$value": "8px", "$type": "dimension" },
    "component": {
      "button": { "$value": "{radius.md}", "$type": "dimension" }
    }
  }
}
```

## Naming Conventions

- T-shirt scale for primitives: `none / xs / sm / md / lg / xl / 2xl / full`.
- Component aliases: `radius.component.{name}` — never `button-radius` (flat namespace pollution).
- Corner-set tokens: `corner-set.{position}` where position is logical (`start` / `end` / `top` / `bottom`), not physical (`left` / `right`).
- Brand-mode resolver: `radius.brand.{sharp|crisp|soft|pillowed|pill-first}.json` selectable via DTCG resolver.
- Use `dimension` `$type`, not `borderRadius` (DTCG v2025.10 standardizes on `dimension`).

## Anti-Patterns

- Hardcoded radii in components (`border-radius: 8px`) — brand-mode swap impossible; theme tuning requires file-by-file edits.
- Naming radii by component (`radius.button`, `radius.card`, `radius.modal`) directly without scale primitives — no reuse, scale drift accumulates.
- Mixing physical corner properties (`border-top-left-radius`) when RTL is in scope — use `border-start-start-radius` and corner-set tokens.
- Single radius for everything (`radius.default = 8px`) applied to button, card, modal, avatar — flattens visual hierarchy; modals should look more contained than cards.
- Pill (`9999px`) on small square icons — radius exceeds half the side, producing the same circle as `50%` but inheriting the wrong intent; use `radius.full` only when content is text/horizontally elongated.
- Off-scale values from imported Figma frames (3px, 5px, 7px, 10px) — audit and snap to nearest scale stop; document any intentional exceptions.
- Forgetting nested-radius rule — when a child has padding inside a rounded parent, child radius should be `parent.radius - padding` to avoid concentric mismatch.
- Animating radius across non-token values — break tokens, breaks brand-mode swap; animate by changing the token reference, not the literal value.

## Handoff

- **To Artisan**: component-radius mapping table (Button → `radius.component.button`), corner-set token usage for sheets and segmented controls.
- **To Flow**: radius transition tokens for shape-morph animations (button → pill on hover, card → modal expansion).
- **To Vision**: brand-mode selection review — radius is one of the loudest brand-personality levers; confirm direction.
- **To Palette**: when full-pill on small touch targets reduces perceived hit area, reconcile interaction-priority.
- **To Polyglot**: corner-set tokens use logical properties; verify RTL preview in Showcase.
- **To Showcase**: radius scale ladder catalog with brand-mode toggle (sharp ↔ pill-first preview).
