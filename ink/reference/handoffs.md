# Ink Handoff Templates

## Receiving Handoffs

### From Vision (Art Direction)

```yaml
VISION_TO_INK_HANDOFF:
  source: Vision
  content:
    style_direction: "[modern | playful | corporate | minimal]"
    mood: "[description]"
    color_palette: ["#hex1", "#hex2"]
    # 2026-05 typical reference libraries
    reference_libraries:
      - "[Lucide 1.16.x | Heroicons 2.2 | Phosphor 2.1 | Tabler 3.44 | Material Symbols VF | Font Awesome 7 | Iconify | custom]"
  request: "Create icon set matching this direction"
```

### From Muse (Design Tokens)

```yaml
MUSE_TO_INK_HANDOFF:
  source: Muse
  content:
    # Prefer DTCG Design Tokens Format Module 2025.10 (W3C CG first stable, 2025-10-28).
    # MIME application/design-tokens+json, files *.tokens.json.
    token_format: "DTCG 2025.10"
    tokens:
      color_primary: "[hex | oklch]"
      color_secondary: "[hex | oklch]"
      spacing_unit: "[dimension token]"
      border_radius: "[dimension token]"
    icon_context: "[where icons will be used]"
  request: "Align icon design with token system"
```

### From Frame (Figma Context)

```yaml
FRAME_TO_INK_HANDOFF:
  source: Frame
  content:
    figma_icons: ["[icon specs from Figma]"]
    grid_size: "[px]"
    style_notes: "[Figma design notes]"
  request: "Implement icons matching Figma specifications"
```

## Sending Handoffs

### To Artisan (Component Integration)

```yaml
INK_TO_ARTISAN_HANDOFF:
  source: Ink
  destination: Artisan
  content:
    icons:
      - name: "[icon-name]"
        svg: "[SVG code or path]"
        props: ["size", "color", "label"]
    component_pattern: "[inline | sprite | component]"
    framework: "[React | Vue | Svelte]"
  request: "Integrate SVG icons as framework components"
```

### To Showcase (Storybook Catalog)

```yaml
INK_TO_SHOWCASE_HANDOFF:
  source: Ink
  destination: Showcase
  content:
    icon_set:
      name: "[icon set name]"
      icons: ["[icon name list]"]
      grid: "[size]"
      styles: ["[outline | filled | duotone]"]
    design_spec:
      stroke_width: "[px]"
      corner_radius: "[px]"
  request: "Create Storybook stories for icon catalog"
```
