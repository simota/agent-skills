# Principle Entry Template

Copy this block into the right layer file (`core` / `frontend` / `ios` / `android`) during the PROMOTE step.

## ID scheme (collision-free + discoverable)
Use a **kebab-case slug**, not a running number: `P-<SCOPE>-<slug>`.
- `P-CORE-control-feedback`, `P-FE-keyboard-focus`, `P-IOS-safe-area`, `P-AND-predictive-back`.
- Slugs never collide on concurrent appends (no shared counter) and read as their own index.
- If a slug is already taken, the principle already exists — update it instead of adding a duplicate.

```markdown
### P-<SCOPE>-<slug> — <one-line imperative title>
- **Statement:** <single testable rule — what must be true>
- **Rationale:** <why this matters; the cost of violating it> [Source: <feedback IDs or standard>]
- **Scope:** core | frontend | ios | android
- **Tags:** <navigation | forms | a11y | feedback | motion | content | layout | error | ...>  (1-3, for INDEX.md)
- **Source feedback:** <FB-YYYYMMDD-slug[, ...]> | baseline
- **Do:** <concrete positive example>
- **Don't:** <concrete anti-example>
- **Token:** <design-token name if the quantitative part is encoded via muse, else —>
- **Status:** proposed | accepted | deprecated
- **Added:** YYYY-MM-DD · **Last reviewed:** YYYY-MM-DD
<!-- if deprecated: move the entry under the file's `## Archive (deprecated)` section and add: -->
- **Superseded by:** P-<SCOPE>-<slug>
```

## Rules
- **Statement must be testable.** A reviewer (human or `canon`) can decide pass/fail on a real screen.
- **Core vs platform:** put it in `core` only if true on every platform; otherwise it is a platform delta. A platform delta must not contradict an accepted `core` principle.
- **No principle without evidence:** `Source feedback` is required (use `baseline` only for seeded defaults).
- **Tags are mandatory** — they drive `INDEX.md` discoverability once principles grow past a handful.
- **Deprecate, don't delete:** move superseded entries to the file's `## Archive (deprecated)` section so the active list (what ENFORCE reads) stays lean.
- **Link mockups** that demonstrate the rule via `mockups/` filenames in Do/Don't where helpful.
