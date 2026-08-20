# Parametric Output Protocol (Common)

> **Tier:** `domain` — activates when the task's subject matches. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

**Purpose**: Emit design/config values as **parametric options** (3-5 step ranges with labeled extremes) rather than single hard-coded values, so users can pick direction with minimal re-prompting. Inspired by Claude Design by Anthropic Labs (2026-04-17): "custom sliders (made by Claude)".

**Scope**: Used by `muse`, `palette`, `flow`, `atelier`, and any skill producing values where exploration beats single-shot decision.

---

## When to Use

| Situation | Parametric? |
|-----------|-------------|
| Adjustable visual parameter (spacing/density/accent intensity) | ✓ Yes |
| Ambiguous user preference ("more compact" vs "more relaxed") | ✓ Yes |
| Multiple valid values along a spectrum (easing, duration, weight) | ✓ Yes |
| Single correct answer (contrast ratio 4.5, WCAG AA) | ✗ No — emit the value |
| Hard constraint (brand primary color = #0ea5e9) | ✗ No — emit the constraint |
| Binary choice (dark mode / light mode) | ✗ No — use variant, not slider |

---

## Output Format

### Syntax

```
<parameter_name>: [label_1=value_1 / label_2=value_2 / ... / label_n=value_n]
```

- **Labels** are short, contrast-forming words (tight/base/airy, quiet/base/bold).
- **Values** are machine-usable (px, ms, hex, numbers, named tokens).
- **Always include a `base`** (or equivalent neutral option) as the default.
- **3-5 steps** — fewer is too coarse, more is decision paralysis.

### Examples

```yaml
spacing_density: [tight=4px / base=8px / airy=16px]
accent_intensity: [quiet=slate-400 / base=sky-500 / bold=sky-600 / loud=sky-700]
motion_speed: [fast=150ms / base=250ms / slow=400ms / dramatic=600ms]
corner_radius: [sharp=0 / soft=4px / base=8px / pill=9999px]
text_weight: [light=300 / base=400 / medium=500 / bold=700]
```

### Multi-parameter blocks

```yaml
variants:
  density: [compact=3 / base=4 / relaxed=6]
  accent:  [cyan=#06b6d4 / amber=#f59e0b / violet=#8b5cf6]
  pace:    [calm=slow / base=base / energetic=fast]
```

---

## User Interaction Patterns

### Mode A: Default-and-offer

Emit the parametric block, apply `base` values to the deliverable, and offer the alternatives for selection.

```
I've built the hero section with base values. If you want to explore:

spacing_density: [tight=4px / base=8px / airy=16px]
accent_intensity: [quiet / base / bold]

Reply with e.g. "go airy + bold" to regenerate.
```

### Mode B: Multi-variant generation

When the task is small (single component, single page), generate all variants at once and present side-by-side.

```
Generated 3 variants:
- V1 (tight + quiet)
- V2 (base + base) ← recommended
- V3 (airy + bold)
```

### Mode C: Slider UI (when host supports it)

When the host UI can render parametric sliders (future integration), emit the block with `render_as: slider` so the harness knows to show interactive controls.

```yaml
spacing_density:
  values: [tight=4px / base=8px / airy=16px]
  render_as: slider
  default: base
```

If the host doesn't support sliders, fall back to Mode A automatically.

---

## Rules

1. **Always label endpoints** — `[4px / 8px / 16px]` forces the user to interpret; `[tight=4px / base=8px / airy=16px]` gives them direction.
2. **Keep labels short and oppositional** — one word each, ideally forming a visible spectrum (quiet↔loud, tight↔airy, calm↔energetic).
3. **Base is mandatory** — one option must be the neutral/safe default; apply it immediately to the deliverable.
4. **3-5 steps max** — research shows decision quality degrades past 5 options for continuous parameters.
5. **Use real values, not abstractions** — `tight=4px` is actionable; `tight=small` is not.
6. **Don't parametrize hard constraints** — contrast ratios, brand colors, a11y minimums are values, not sliders.
7. **Integrate with registry** — when parametric output resolves, update `.agents/design-system/` only if user explicitly commits the change (see `_common/design-system-registry.md`).

---

## Handoff Integration

Inside `DESIGN_INTENT_HANDOFF`, parametric options live under `Variants`:

```yaml
DESIGN_INTENT_HANDOFF:
  Intent: "..."
  Tokens: "registry:default"
  Variants:
    density: [compact=3 / base=4 / relaxed=6]
    accent: [cyan=#06b6d4 / amber=#f59e0b]
  Next: Forge (generate 2 variants: base+cyan, relaxed+amber)
```

Downstream agents that don't understand parametric syntax MUST pick the `base` option and continue; they must NOT fabricate choices.

---

## Anti-patterns

1. **Unbounded numeric options** — "pick any spacing" is not parametric; it's abdicating decision-making.
2. **Parametrizing decisions that should be made upstream** — brand voice, target audience, platform choice are Vision/scribe[unified] concerns, not sliders.
3. **Emitting parametric output without a default** — always apply `base` to the deliverable; don't stall waiting for selection.
4. **Inventing labels mid-stream** — establish the spectrum upfront; don't introduce `nuclear=64px` without warning.
5. **Overloading single slider** — one parameter per block. Compound effects (density + accent) require multi-parameter blocks, not mashed-up sliders.
