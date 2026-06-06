# Keyboard Navigation Patterns Reference

Purpose: Design keyboard-primary interfaces where every interactive target is reachable, every focus position is visible, and every shortcut is discoverable. Keyboard navigation is not an accessibility feature bolted on late — it is the spine that a11y, screen readers, and power-user efficiency all hang from.

## Scope Boundary

- **Palette `keyboard`**: tab-order design, focus-ring visibility, skip-link placement, keyboard-shortcut systems (Cmd-K palette, chord shortcuts), modifier-key conventions, roving tabindex for composite widgets, focus-trap for modals.
- **Palette `a11y` (elsewhere)**: WCAG 2.2 conformance audit, screen-reader ARIA semantics, color contrast, cognitive accessibility.
- **Flow (elsewhere)**: focus-transition animation timing, motion-safe focus pulse.
- **Prose (elsewhere)**: shortcut label microcopy ("Press `/` to search"), cheatsheet copy, first-run hint voice.
- **Artisan (elsewhere)**: production React/Vue `useFocusTrap`, `useRovingTabindex`, `useHotkeys` hook implementation, keyboard-event listener performance.

If the question is "can users reach and operate every control by keyboard?" → `keyboard`. If it's "does this pass WCAG 2.1.1 / 2.4.3 / 2.4.11?" → `a11y`. If it's "how do I build a keyboard-accessible combobox in React?" → Artisan.

## Tab-Order Principles

Tab order must follow visual reading order. A mismatched DOM order is the most common keyboard-navigation bug in production.

| Rule | Why | Fix |
|------|-----|-----|
| Use natural DOM order | `tabindex` values > 0 fight browser order | Reorder DOM, not `tabindex` |
| `tabindex="0"` adds non-interactive element to tab order | Only when the element is actually interactive | Prefer native `<button>` / `<a>` |
| `tabindex="-1"` removes from tab order but keeps programmatic focus | Needed for focus management (error summaries, modal roots) | Use for headings inside dialogs |
| Never use `tabindex="1"` or higher | Creates a parallel tab order that confuses every user | Delete; reorder DOM |
| Skip-link first in DOM | Bypasses repeated navigation for keyboard/screen-reader users | `<a href="#main" class="skip-link">Skip to content</a>` |

## Focus Ring Requirements

WCAG 2.2 SC 2.4.11 (Focus Not Obscured) and SC 2.4.13 (Focus Appearance) raised the bar.

- Outline thickness ≥ 2px, contrast ratio ≥ 3:1 against both focused element and adjacent background.
- Focus ring must not be hidden behind sticky headers, cookie banners, or chat widgets.
- Never use `outline: none` without a replacement — `:focus-visible` + custom ring is the correct pattern.
- Offset focus ring from the target by 2–4px so it doesn't get visually eaten by adjacent borders.

```css
/* Default: visible focus ring, only for keyboard users */
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  border-radius: inherit;
}

/* Never this */
*:focus { outline: none; }

/* Sticky header must reserve space — prevents SC 2.4.11 violation */
main { scroll-padding-top: var(--header-height); }
```

## Shortcut System Design

| Pattern | Use for | Example |
|---------|---------|---------|
| Single-key (`/`, `?`) | High-frequency, obvious verbs | `/` opens search, `?` shows cheatsheet |
| Modifier + key (Cmd/Ctrl + K) | Command palette, save, new | `Cmd+K` command palette |
| Chord (G then I) | Navigation-heavy apps | `G I` → go to Inbox (Gmail style) |
| Sequence + escape | Dismissible overlays | `Esc` closes any topmost overlay |

Rules:
- Provide a discoverable cheatsheet (`?` or in help menu). Undocumented shortcuts do not exist to 90% of users.
- Single-key shortcuts must not fire when focus is in a text input or `contenteditable`.
- Respect browser/OS reserved combos: never override `Cmd+W`, `Cmd+T`, `Cmd+R`, `Ctrl+F` for unrelated actions.
- Provide both Mac and Windows/Linux hints in UI: `⌘K` / `Ctrl+K`. Detect platform via `navigator.platform` or `navigator.userAgentData.platform`.

## Modifier-Key Conventions

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Primary modifier | `⌘` (Cmd) | `Ctrl` |
| Secondary modifier | `⌥` (Option) | `Alt` |
| Select range | `⇧` (Shift) | `Shift` |
| Multi-select | `⌘` click | `Ctrl` click |
| Context menu | `⌃` click or two-finger | Right-click / `Menu` key |

Never hardcode `Ctrl` in UI labels — it's wrong on macOS and teaches users the wrong muscle memory.

## Roving Tabindex (Composite Widgets)

Toolbars, menus, radio groups, grids, and tab lists should occupy **one** tab stop, then use arrow keys to move focus internally.

```html
<div role="toolbar" aria-label="Formatting">
  <button tabindex="0">Bold</button>
  <button tabindex="-1">Italic</button>
  <button tabindex="-1">Underline</button>
</div>
```

On ArrowRight/Left: move `tabindex="0"` to the next button, focus it, set the previous to `tabindex="-1"`. This is the pattern specified in WAI-ARIA Authoring Practices for toolbars, menus, tablists, treeviews, and grids.

## Focus Trap (Modals / Dialogs)

- Native `<dialog showModal()>` handles focus trap automatically — prefer it over custom implementations.
- For non-native modals: trap Tab/Shift+Tab inside the dialog, restore focus to the invoking element on close, send initial focus to the first meaningful element (not the close button by default — send to the primary action or heading).
- `Esc` must close the dialog unless the user is mid-destructive-edit.

## Anti-Patterns

- ❌ `outline: none` without `:focus-visible` replacement — strips focus ring for all keyboard users.
- ❌ `tabindex="1"`, `tabindex="2"` — creates a parallel tab order that breaks mental model.
- ❌ Sticky header or cookie banner covering the focused element — WCAG 2.2 SC 2.4.11 fail.
- ❌ Single-key shortcut (`/`, `j`, `k`) firing while user is typing in a textarea.
- ❌ Custom modal without focus trap and focus restoration — keyboard users get lost behind the scrim.
- ❌ Arrow-key navigation in a dropdown that also tabs through each item — doubles the tab stops.
- ❌ Shortcut label showing only `Ctrl+K` on a Mac build, or only `⌘K` on Windows.
- ❌ Keyboard shortcut with no discoverable cheatsheet and no visible affordance.
- ❌ Focus jumping to top of page after route change — land focus on the new page's `<h1>` (with `tabindex="-1"`).

## Handoff

- **→ Artisan**: production hook implementation (`useFocusTrap`, `useRovingTabindex`, `useHotkeys`), event-listener cleanup, SSR considerations.
- **→ Flow**: focus-ring animation (respecting `prefers-reduced-motion`), scroll-into-view easing.
- **→ Prose**: shortcut cheatsheet copy, first-run discovery hint, platform-aware label strings.
- **→ a11y recipe**: WCAG 2.2 SC 2.1.1 / 2.1.2 / 2.4.3 / 2.4.11 / 2.4.13 conformance verification.
- **→ Voyager**: E2E keyboard-only test scripts (Tab, Shift+Tab, Enter, Space, Esc, Arrow keys) covering every critical flow.
