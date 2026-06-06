# Mobile Touch Patterns Reference

Purpose: Design touch-first UX where every primary action sits within thumb reach, every tap target survives fat-finger error, every gesture has a discoverable affordance, and the keyboard does not eat the input field. Mobile UX is not desktop UX scaled down — it is a different ergonomic contract.

## Scope Boundary

- **Palette `mobile`**: thumb-zone layout, tap-target sizing, gesture affordances, haptic feedback, safe-area handling, keyboard-avoidance, one-handed operation, responsive-breakpoint interaction shifts.
- **Palette `a11y` (elsewhere)**: WCAG 2.2 SC 2.5.8 (target size minimum), SC 2.5.7 (dragging movements) conformance audit.
- **Flow (elsewhere)**: gesture animation choreography (swipe-to-dismiss curve, pull-to-refresh elasticity).
- **Prose (elsewhere)**: CTA label length on narrow screens, mobile error-message copy tightening.
- **Artisan (elsewhere)**: production React Native / Flutter / SwiftUI / Jetpack Compose implementation, native gesture recognizer wiring, platform-specific haptic APIs.

If the question is "does this feel right on a phone held in one hand?" → `mobile`. If it's "does the React Native gesture handler code work?" → Artisan. If it's "does this pass WCAG target-size SC?" → `a11y`.

## Thumb Zone Map

Steven Hoober's research (reconfirmed UX Magazine 2025) shows 49% of users operate phones one-handed and 75% use thumb-dominant grips. Plan primary actions inside the reachable arc.

```
┌─────────────────────┐
│  HARD  │  OK   │ OK │   Top edge:     status, identity, non-primary
├────────┼───────┼────┤
│   OK   │  OK   │ OK │   Middle:       content, secondary actions
├────────┼───────┼────┤
│  NAT   │  NAT  │NAT │   Bottom arc:   primary CTA, tab bar, FAB
└─────────────────────┘
    (right-hand thumb-dominant user)
```

| Zone | Place here | Avoid placing here |
|------|-----------|--------------------|
| Natural (bottom 1/3) | Primary CTA, tab bar, FAB, search trigger | Destructive action (accidental taps) |
| OK (middle) | Content, secondary actions, filters | Time-critical primary actions |
| Hard (top corners) | Back, identity, contextual "more" menu | Frequent primary action |

Mirror the layout for left-handed users via system detection when possible. Don't hardcode right-hand assumption.

## Tap Target Sizing

| Standard | Minimum | Ideal | Source |
|----------|---------|-------|--------|
| WCAG 2.2 SC 2.5.8 | 24×24px CSS | — | W3C 2023 |
| Apple HIG | 44×44pt | 44×44pt | Apple 2025 |
| Material Design | 48×48dp | 48×48dp | Google 2025 |
| Fitts's Law practical | 44×44px | 48×48+ | Hoober 2024 |

Rules:
- Treat 44×44 CSS px as the **baseline**, 48×48 as the comfortable target. The 24×24 WCAG floor exists only because some controls (inline links in prose) cannot expand.
- When visual size is constrained, expand the hit area via padding or `::before` pseudo-element. Visual 16×16 icon with 44×44 hit area is correct; 16×16 hit area is never correct.
- Minimum spacing between adjacent targets: 8px (ideally matches target-size value, per Fitts).
- Inline text links are the most common target-size exemption. When possible, use a button style for important inline actions.

```css
.icon-button {
  width: 24px;  /* visual */
  height: 24px;
  position: relative;
}
.icon-button::before {
  /* Expanded hit area */
  content: '';
  position: absolute;
  inset: -12px; /* 24 + 12*2 = 48px hit zone */
}
```

## Gesture Affordances

Hidden gestures are a usability tax. Every custom gesture must have a visible alternative or onboarding hint.

| Gesture | Expected affordance | Alternative (required) |
|---------|--------------------|-----------------------|
| Swipe to dismiss | Partial drag reveal, edge cue | Close button in header |
| Pull to refresh | Spinner + text at top on drag | Refresh button / auto-refresh |
| Long-press menu | Tactile haptic at activation threshold | Visible "more" button |
| Pinch to zoom | Pinch icon on first view | Zoom +/- buttons for a11y |
| Swipe between tabs | Animated page indicator | Tappable tab bar |
| Two-finger gesture | Never for critical action | Mandatory alternative (WCAG 2.5.7) |

WCAG 2.2 SC 2.5.7 (Dragging Movements): any drag action must have a single-pointer alternative (tap, button). Multi-touch gestures must have a single-touch alternative.

## Haptic Feedback Vocabulary

Haptics are a feedback channel. Use them sparingly and consistently.

| Action | iOS | Android |
|--------|-----|---------|
| Selection change (picker, segmented control) | `selection` / `UIImpactFeedbackGenerator.light` | `HapticFeedbackConstants.CLOCK_TICK` |
| Successful action (save, confirm) | `notificationSuccess` | `CONFIRM` |
| Warning | `notificationWarning` | `REJECT` |
| Error (form invalid, destructive denied) | `notificationError` | `REJECT` |
| Button press (context menu open) | `impactMedium` | `LONG_PRESS` |

Rules:
- Respect system "Reduce Motion" / "Reduce Haptics" settings.
- Never haptic for scroll, keystroke, or normal navigation — it becomes noise.
- Pair haptic with visual feedback; never rely on haptic alone (a11y gap).

## Safe Area and Insets

Use `env(safe-area-inset-*)` (web) / `SafeAreaView` (RN) / `safeAreaInsets` (SwiftUI) — never hardcode padding for notches, home indicators, or Dynamic Island.

```css
.bottom-bar {
  padding-bottom: max(12px, env(safe-area-inset-bottom));
}
.header {
  padding-top: max(12px, env(safe-area-inset-top));
}
```

Test on: iPhone with notch, iPhone with Dynamic Island, Android with gesture-nav, Android with three-button nav, iPad in split view, landscape orientation.

## Keyboard Avoidance

When the software keyboard opens, the layout must remain usable.

- Input field must scroll into view above the keyboard (not hidden behind it). iOS: automatic for native inputs. Web: `scroll-padding-bottom` + `element.scrollIntoView({block: 'center'})`.
- Primary submit CTA must remain reachable. On narrow viewports, consider keyboard-anchored "Done" or "Next" bar.
- Don't animate the layout on keyboard open/close; let the OS handle it. Custom animations produce a fight-with-OS jitter.
- Use correct `inputmode` / `keyboardType`: `numeric`, `decimal`, `email`, `tel`, `url`, `search` — wrong keyboard is a major friction source.

## Anti-Patterns

- ❌ Primary CTA in top-right corner (hard zone) on a scrollable content screen.
- ❌ 16×16 icon with 16×16 hit area (barely passes WCAG 24, fails Apple/Material, fails in practice).
- ❌ Hover-only affordance (tooltip, dropdown preview) — hover does not exist on touch.
- ❌ Swipe-to-delete without an undo or a visible delete button alternative.
- ❌ Pinch-to-zoom disabled on images (`maximum-scale=1`) — WCAG 1.4.4 violation and poor low-vision UX.
- ❌ Haptic on every scroll tick or keystroke — becomes fatigue noise.
- ❌ Hardcoded `padding-bottom: 20px` ignoring safe-area — CTA gets covered by home indicator.
- ❌ `<input type="text">` for a phone number — wrong keyboard, no numeric pad.
- ❌ Tap target <32px because "it matches desktop" — desktop cursor is 1px, thumb is ~44px.
- ❌ Long-press as the only path to a destructive action — undiscoverable without onboarding.

## Handoff

- **→ Artisan**: React Native / Flutter / SwiftUI / Jetpack Compose production implementation, native gesture recognizers, platform haptic APIs, keyboard-accessory view.
- **→ Flow**: swipe-to-dismiss animation curve, pull-to-refresh elasticity, sheet drag-to-close easing, haptic + motion synchronization.
- **→ Prose**: CTA label length tightening (mobile shows less horizontal copy), mobile error-message voice.
- **→ a11y recipe**: WCAG 2.2 SC 2.5.7 (drag alternative) and SC 2.5.8 (target size) audit, VoiceOver / TalkBack rotor testing.
- **→ Native (outside palette)**: deep store-review checklist, offline strategy, push-permission UX, navigation architecture.
