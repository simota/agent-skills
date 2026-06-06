# Ink Examples

## Example 1: Custom Icon Set (5 icons)

### Design Spec

```yaml
grid: 24x24
stroke_width: 2px
corner_radius: 2px
padding: 2px
style: outline
color: currentColor
icons:
  - dashboard
  - settings
  - notification
  - user
  - search
```

### Generated Icons

```svg
<!-- icon-dashboard -->
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round"
     role="img" aria-label="Dashboard">
  <title>Dashboard</title>
  <rect x="3" y="3" width="7" height="9" rx="2"/>
  <rect x="14" y="3" width="7" height="5" rx="2"/>
  <rect x="14" y="12" width="7" height="9" rx="2"/>
  <rect x="3" y="16" width="7" height="5" rx="2"/>
</svg>

<!-- icon-settings -->
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
     fill="none" stroke="currentColor" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round"
     role="img" aria-label="Settings">
  <title>Settings</title>
  <circle cx="12" cy="12" r="3"/>
  <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/>
</svg>
```

## Example 2: SVG Sprite Bundle

```html
<!-- icons.svg -->
<svg xmlns="http://www.w3.org/2000/svg" style="display:none">
  <defs>
    <symbol id="icon-dashboard" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="7" height="9" rx="2"/>
      <rect x="14" y="3" width="7" height="5" rx="2"/>
      <rect x="14" y="12" width="7" height="9" rx="2"/>
      <rect x="3" y="16" width="7" height="5" rx="2"/>
    </symbol>
    <symbol id="icon-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="11" cy="11" r="8"/>
      <line x1="21" y1="21" x2="16.65" y2="16.65"/>
    </symbol>
  </defs>
</svg>

<!-- Usage -->
<svg class="icon" width="24" height="24" role="img" aria-label="Dashboard">
  <use href="icons.svg#icon-dashboard"/>
</svg>
```

## Example 3: Icon Consistency Audit Report

```markdown
## Icon Audit Report

### Summary
- Icons audited: 24
- Consistent: 18 (75%)
- Issues found: 6

### Issues

| Icon | Issue | Fix |
|------|-------|-----|
| `notification` | stroke-width: 1.5 (expected: 2) | Increase to 2px |
| `arrow-left` | Corner radius: 0 (expected: 2) | Add rx="2" |
| `close` | Missing aria-label | Add aria-label="Close" |
| `menu` | viewBox: "0 0 20 20" (expected: "0 0 24 24") | Normalize to 24x24 |
| `upload` | Uses inline style | Convert to attributes |
| `download` | Inconsistent padding (1px vs 2px) | Adjust paths for 2px padding |
```
