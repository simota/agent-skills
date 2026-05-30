# Mockups

Visual evidence and reference designs that demonstrate principles. Mockups are **supporting artifacts**, not the source of truth — the principles files are. Store accepted reference designs and Do/Don't comparisons here.

## What to store
- **Reference mockups** for an accepted principle (the "Do" made concrete).
- **Before/After pairs** when a principle was created from feedback (shows the fix).
- Static images (`.png`/`.svg`), self-contained HTML prototypes (from `forge`), or Figma export links in a `.md` sidecar.

## Naming convention
```
mockups/
  P-CORE-control-feedback__do.png
  P-CORE-control-feedback__dont.png
  P-FE-responsive-320__do.png
  FB-20260115-double-save__before.png
  FB-20260115-double-save__after.png
```
- Prefix with the **principle slug** (`P-<scope>-<slug>`) or **feedback ID** (`FB-YYYYMMDD-<slug>`) it belongs to so links never rot.
- Use `__do` / `__dont` / `__before` / `__after` suffixes for comparisons.
- For Figma sources, add `P-<scope>-<slug>__name.md` with the file URL + node id (bridge via `frame` / Figma MCP).

## Linking
Reference mockups from principle entries (in `principles/*.md`) and from feedback entries by filename, e.g. `Do: see mockups/P-CORE-control-feedback__do.png`.
