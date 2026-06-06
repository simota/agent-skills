# Accessibility Implementation Reference

Purpose: Harden an Artisan-owned component or page to WCAG 2.2 AA at the implementation level. This recipe wires semantics, ARIA, keyboard paths, focus management, and screen reader affordances into a production frontend file — not a product-wide usability redesign.

## Scope Boundary

- **Artisan `a11y`**: tactical, file-scoped a11y hardening. ARIA attributes, keyboard paths, focus management, visible focus, target size, reduced motion, live regions.
- **Palette (elsewhere)**: product-level usability and interaction-quality improvement (cognitive load, feedback design, flow-level a11y review).
- **Canon (elsewhere)**: repo-wide WCAG gap audit and standards compliance mapping.

If the ask is "make this modal accessible and keyboard-usable" → `a11y`. If the ask is "our sign-up flow is confusing for users with low digital literacy" → `Palette`. If the ask is "prove this app meets WCAG 2.2 AA across all pages" → `Canon`.

## Workflow

```
ANALYZE  →  identify interactive role (button / link / dialog / combobox / tab / disclosure)
         →  list required states (hover / focus / active / disabled / loading / error / selected)
         →  list keyboard contract (Tab, Shift+Tab, Enter, Space, Esc, Arrow, Home/End)
         →  check WCAG 2.2 AA new criteria (focus appearance, target size 24x24, dragging)

DESIGN   →  pick semantic HTML first (button, a, dialog, details); ARIA only to fill gaps
         →  decide focus trap vs focus return (modals, popovers)
         →  decide live region politeness (polite for status, assertive for errors)
         →  pick labels: visible label > aria-labelledby > aria-label (last resort)

IMPLEMENT →  wire ARIA role/state/property only where semantics miss
         →  add keyboard handlers matching WAI-ARIA Authoring Practices
         →  manage focus on mount/unmount (roving tabindex for composite widgets)
         →  respect prefers-reduced-motion for animations

VERIFY   →  keyboard-only walkthrough
         →  screen reader smoke test (VoiceOver / NVDA / TalkBack)
         →  axe-core or Lighthouse a11y scan
         →  contrast + target-size + focus-visible manual check
```

## Patterns

```tsx
// Dialog: semantic <dialog> with focus trap + return
<dialog
  ref={dialogRef}
  aria-labelledby="dlg-title"
  aria-describedby="dlg-desc"
  onClose={handleClose}
>
  <h2 id="dlg-title">Confirm delete</h2>
  <p id="dlg-desc">This action cannot be undone.</p>
  {/* initial focus lands on the safe/cancel action */}
  <button autoFocus onClick={handleClose}>Cancel</button>
  <button onClick={handleConfirm}>Delete</button>
</dialog>

// Live region for async status
<div role="status" aria-live="polite">{status}</div>

// WCAG 2.2: target size 24x24 minimum, 44x44 recommended
<button className="min-h-[44px] min-w-[44px] focus-visible:ring-2">
  Save
</button>

// Roving tabindex (composite widgets: tabs, menus, toolbar)
<div role="tablist" onKeyDown={handleArrowKeys}>
  {tabs.map((t, i) => (
    <button
      key={t.id}
      role="tab"
      aria-selected={i === active}
      tabIndex={i === active ? 0 : -1}
    >{t.label}</button>
  ))}
</div>
```

## Anti-patterns

- Using `<div onClick>` for interactive controls — loses keyboard activation, focus, and screen reader role. Use `<button>`.
- `aria-label` on elements that already have a visible text label — label gets duplicated or overridden by the aria-label.
- Focus traps without focus return on close — user loses their place in the page.
- Replacing the browser's default focus outline with nothing (`outline: none`) and no replacement — WCAG 2.4.7 + 2.4.11 violation.
- Placing `tabindex="0"` on non-interactive content — clutters the tab order and confuses screen readers.
- Animating essential feedback without honoring `prefers-reduced-motion` — vestibular-trigger risk.
- `aria-hidden="true"` on a focusable element — leaves a ghost tab stop that SR users can't perceive.

## WCAG 2.2 AA Checklist (per component)

- [ ] Semantic HTML before ARIA.
- [ ] All interactive elements reachable by Tab and usable by Enter/Space.
- [ ] Visible focus indicator meeting 2.4.11 (Focus Appearance) contrast and size.
- [ ] Target size ≥ 24×24 CSS px (SC 2.5.8), prefer 44×44.
- [ ] Dragging operations have a non-drag alternative (SC 2.5.7).
- [ ] Errors announced to assistive tech via `role="alert"` or `aria-live`.
- [ ] Form fields have programmatic labels; errors linked via `aria-describedby`.
- [ ] Modal/popover: focus trapped, Esc closes, focus returns to trigger.
- [ ] `prefers-reduced-motion` respected for non-essential animation.
- [ ] Color is not the only means of conveying state.

## Handoff

- To `Palette` if flow-level confusion or cognitive-load issues surface during testing.
- To `Canon` if the component-level fixes reveal a recurring repo-wide pattern that needs audit.
- To `Radar` for axe-core / keyboard / screen reader regression tests on the hardened component.
- To `Showcase` for a11y-annotated stories that lock the behavior.
