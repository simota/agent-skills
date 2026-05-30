# iOS Principles — deltas only

iOS-specific rules layered on top of `core.md`, aligned with Apple Human Interface Guidelines (HIG). Add here only platform-specific rules (gestures, system integration, HIG idioms, Liquid Glass / iOS 26 conventions). Schema: `_templates/principle-entry.md`. ID prefix: `P-IOS-<slug>`.

---

### P-IOS-safe-area — Respect safe areas and Dynamic Type
- **Statement:** Layouts honor safe-area insets and scale with Dynamic Type up to the largest accessibility sizes without truncation or overlap.
- **Rationale:** HIG; notch/Home-indicator and accessibility text scaling. [Source: baseline — Apple HIG]
- **Scope:** ios
- **Tags:** layout, a11y
- **Source feedback:** baseline
- **Do:** SwiftUI `.safeAreaInset`, scalable fonts, `ViewThatFits` for large text.
- **Don't:** hardcode point sizes that clip at AX5.
- **Token:** —
- **Status:** accepted · **Added:** 2026-01-01 · **Last reviewed:** 2026-01-01

### P-IOS-native-nav — Use platform-native navigation and gestures
- **Statement:** Honor the system back-swipe, standard navigation stacks, and native controls before introducing custom alternatives.
- **Rationale:** Muscle memory; HIG consistency. [Source: baseline]
- **Scope:** ios
- **Tags:** navigation
- **Source feedback:** baseline
- **Do:** `NavigationStack`, sheets, edge-swipe back.
- **Don't:** custom back buttons that break interactive pop.
- **Token:** —
- **Status:** accepted · **Added:** 2026-01-01 · **Last reviewed:** 2026-01-01

---

<!-- PROMOTE step appends new iOS-specific principles above this line. -->

## Archive (deprecated)

<!-- Superseded principles move here. ENFORCE ignores this section. -->
