# Controller & Console Navigation

**Purpose:** Focus-based navigation, the focus graph, platform button conventions, glyphs, input remapping, and touch zones.
**Read when:** Designing navigation for controllers/consoles (or any non-pointer input) (`nav` recipe).

## Contents
- Focus-based, not pointer-based
- The focus graph
- Default focus, wrap & back
- Platform button conventions
- Button prompts & glyph swapping
- Input remapping UX
- Touch & mobile
- Pitfalls

---

## Focus-based, not pointer-based

On a controller there is no cursor. One element is **focused** (highlighted); the stick/D-pad moves focus between elements; a button confirms; another cancels. This is fundamentally different from mouse hover/click and must be designed, not assumed.
- Every interactive element needs a clear **focused state** (not just hover styling).
- The player must always be able to tell what is focused at a glance (strong highlight, not a subtle tint).
- Don't port a mouse UI to console by adding a virtual cursor unless the genre demands it (RTS/strategy) — native focus nav is faster and expected.

---

## The focus graph

Specify, per screen, how focus moves — a directed graph over the focusable elements:
- **Nodes**: every focusable element.
- **Edges**: for each of up/down/left/right, which element focus moves to.
- Keep movement **spatially intuitive** (down goes to the element visually below). Avoid surprising jumps.
- For grids/lists, define edge behavior at boundaries (stop, wrap, or jump to next group).

```
Settings screen focus graph (vertical list):
  [Display]  ⇅
  [Audio]    ⇅   default focus: Display
  [Controls] ⇅   up from Display: wrap to Quit (or stop)
  [Accessibility] ⇅
  [Quit]         down from Quit: stop
  back/cancel (B/Circle): → previous screen
```

---

## Default focus, wrap & back

- **Default focus**: focus a sensible element the instant a screen opens (the primary action or first item). Never open with nothing focused.
- **Wrap vs stop**: decide whether moving past the last item wraps to the first or stops. Lists often stop; grids often wrap horizontally. Be consistent within a screen.
- **Back/cancel**: bind a consistent button to go back one screen everywhere; it must always work and always do the same thing.
- Restore focus to the **invoking element** when returning from a sub-screen (don't reset to top).

---

## Platform button conventions

Confirm/cancel placement and meaning differ by platform and region — respect them:
- **Xbox**: A = confirm, B = cancel.
- **PlayStation**: Cross = confirm, Circle = cancel (note: historically swapped in Japan; modern PS5 standardizes Cross = confirm globally).
- **Nintendo**: A = confirm, B = cancel (physically swapped layout vs Xbox).
- Don't hardcode "the bottom button" semantics — map to confirm/cancel intents and let the platform layer resolve.

---

## Button prompts & glyph swapping

- Show **contextual prompts** next to the action they trigger ("Ⓐ Interact", "Ⓧ Reload").
- **Swap glyphs to match the detected device** (Xbox vs PS vs Switch vs keyboard) — showing the wrong glyph set is a top immersion/usability complaint. Re-detect on input-device change mid-session.
- For keyboard/mouse, show key caps; update live if the player remaps.
- Keep a single source of truth: action → current binding → glyph, so prompts and remap UI never disagree.

---

## Input remapping UX

- Allow **full remapping** (accessibility + preference); detect and warn on conflicts.
- Offer **toggle vs hold** for actions like aim/crouch/sprint.
- Provide **sensitivity / dead-zone / invert-Y** for sticks; aim-assist options.
- Show the current binding everywhere prompts appear; "reset to default" per scheme.

---

## Touch & mobile

- No hover; design for **thumb reach** — primary actions in bottom corners/zones, avoid the center-top (hard to reach one-handed).
- **Large hit targets** (≥ ~9mm / 44pt); space them to avoid mis-taps.
- Use platform **gesture conventions** (swipe, long-press) but always offer a visible button alternative.
- On-screen virtual sticks/buttons need adjustable position/size/opacity.

---

## Pitfalls

- Porting a mouse UI to console with a virtual cursor instead of focus nav.
- No clear focused state, or a focus highlight too subtle to see.
- Opening a screen with nothing focused.
- Unintuitive focus jumps (down goes somewhere unexpected).
- Inconsistent back/cancel binding across screens.
- Wrong platform glyphs (Xbox prompts on a PlayStation).
- No remapping → locks out players who need alternative bindings.
- Touch UI with center-screen primary actions or tiny targets.
