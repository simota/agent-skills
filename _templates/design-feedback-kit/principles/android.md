# Android Principles — deltas only

Android-specific rules layered on top of `core.md`, aligned with Material Design (Material 3 / M3 Expressive). Add here only platform-specific rules (back navigation, system bars, Material idioms, predictive back). Schema: `_templates/principle-entry.md`. ID prefix: `P-AND-<slug>`.

---

### P-AND-predictive-back — Honor system back and predictive back
- **Statement:** The system back gesture/button always works and supports predictive-back animation; never trap the user.
- **Rationale:** Core Android navigation contract; Android 14+ predictive back. [Source: baseline — Material 3]
- **Scope:** android
- **Tags:** navigation
- **Source feedback:** baseline
- **Do:** `OnBackPressedDispatcher` / predictive-back APIs, Compose `BackHandler`.
- **Don't:** intercept back to block exit without reason.
- **Token:** —
- **Status:** accepted · **Added:** 2026-01-01 · **Last reviewed:** 2026-01-01

### P-AND-edge-to-edge — Edge-to-edge with inset-aware layouts
- **Statement:** Draw edge-to-edge and apply window insets so content is never hidden behind system bars or the navigation area.
- **Rationale:** targetSdk 35+ edge-to-edge default; Material guidance. [Source: baseline]
- **Scope:** android
- **Tags:** layout
- **Source feedback:** baseline
- **Do:** `WindowInsets`, `Modifier.safeDrawingPadding()`.
- **Don't:** assume opaque system bars.
- **Token:** —
- **Status:** accepted · **Added:** 2026-01-01 · **Last reviewed:** 2026-01-01

---

<!-- PROMOTE step appends new Android-specific principles above this line. -->

## Archive (deprecated)

<!-- Superseded principles move here. ENFORCE ignores this section. -->
