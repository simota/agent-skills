# Platform UX Adaptation

Translate web UX into Apple HIG (iOS) and Material Design 3 (Android). The two are different in philosophy — accept divergence as a feature, not a bug.

---

## Core Principle

> Web designers think in pages and breakpoints. iOS thinks in flows and gestures. Android thinks in screens and shared transitions. **Never ship the same UI on both with only color adjustments.**

---

## 2026 Update — What changed since 2024

### iOS — Liquid Glass (iOS 26, WWDC25)

The **biggest visual redesign since iOS 7**, applied across iOS 26 / iPadOS 26 / macOS Tahoe / watchOS / tvOS 26.

- **Liquid Glass material**: translucent, refractive, real-time-rendered surfaces for controls, navigation, widgets, icons.
- **Dynamic shrinking tab bar**: tab bar shrinks during scroll and expands when scrolling stops. Plan for this in tab-heavy designs.
- **Icons require 4 variants**: light / dark / tinted / clear. Use Apple's Icon Composer.
- **Lock-screen content** can dynamically tuck behind subjects (depth illusion).
- New SwiftUI / UIKit / AppKit APIs for materials and corner radii (hardware-aware).

Port action:
- **From 2026-04-28**, all App Store Connect uploads must be built with **Xcode 26 + iOS 26 SDK** — Liquid Glass is **applied by default** to native UI components when built with the iOS 26 SDK regardless of the deployment target. Verify navigation bars / tab bars / toolbars / sheets visually on iOS 26 *and* legacy deployment targets.
- If targeting iOS 26 → Liquid Glass adoption is the default. Document any deviation explicitly.
- If targeting iOS 17/18 → still build with the iOS 26 SDK; design must work *visually* on iOS 26 devices (legible at scale; no broken assumptions about translucency).
- WWDC 2026 runs **2026-06-08 to 2026-06-12**; iOS 27 announcement may shift the recommended target during P2/P3 — revisit the UX adaptation plan after the conference.

### iOS — iOS 18 / iOS 26 surfaces to plan around

- **Control Center API** (`ControlWidgetToggle`, `AppIntentControlValueProvider`) — apps can add toggles to Control Center, Lock Screen, and Action Button. New native capability beyond the "Push / Biometrics / Camera" set.
- **Live Activities + Dynamic Island** — `ActivityKit` allows up to 8h active + 4h stale. Payload ~4KB. APNs `apns-priority` 5 for normal updates. Advertising / marketing copy is forbidden by Apple.
- **App Intents + Apple Intelligence** (iOS 18+, expanding through 26) — surface domain operations to Spotlight / Siri / Action Button. 12 domains (Books, Camera, Spreadsheets, etc.). Use `opensAppWhenRun = false` for "answer without opening the app" UX.
- **Foundation Models framework** (on-device LLM) — built-in `~3B` quantized model + Private Cloud Compute fallback. Web→Native uplift opportunity for AI features.

### Android — Material 3 Expressive (Google I/O 2025)

Announced at Google I/O 2025 as the new design language. Rolled out to Pixel devices via **Android 16 QPR1 (2025-09)** with refreshes to notifications, Quick Settings, lock screen, and launcher. **`androidx.compose.material3:material3:1.4.0` shipped stable on 2025-09-24** (promoting a set of previously experimental APIs); the **fully Expressive component set is currently in `1.5.0-alpha`** as of 2026-05. Backed by 46 user studies / 18,000 participants.

Five core pillars: **Color · Shape · Size · Motion · Containment**.

New / updated components:
- **LoadingIndicator / ContainedLoadingIndicator** — replaces indeterminate `CircularProgressIndicator` for sub-5s waits; loops through 7 morphing shapes.
- **PullToRefreshBox** — official Material 3 component (replaces ad-hoc implementations).
- **DockedToolbar / FloatingToolbar** — `BottomAppBar` is deprecated. FloatingToolbar supports horizontal/vertical with FAB combinations.
- **Carousel** — official component for image/video collections.
- **Shape Library** — 35 new shapes; shape morphing; variable fonts.
- **Spring-based motion engine** — physics-based for natural feedback.

### Android — Material You / Dynamic Color

- **Compose BOM `2026.05.00`** is the current stable BOM (maps to Compose 1.11.1); `2025.12.00` and earlier are still supported. Use the BOM rather than pinning individual Compose libraries.
- Dynamic Color: API 31+. Use `dynamicLightColorScheme()` / `dynamicDarkColorScheme()` with feature detection. Hard-coded colors are forbidden — use `MaterialTheme.colorScheme.surface` and friends.
- Pausable Composition (Compose December '25 / BOM 2025.12.00) brings scroll performance on par with classic Views — adopt when porting long lists from web.

### Android — Edge-to-Edge enforcement (API 36)

- `R.attr#windowOptOutEdgeToEdgeEnforcement` is **deprecated and disabled** at targetSdk 36.
- Design every screen with `Modifier.windowInsetsPadding()` / `WindowInsets.systemBars` from day 1.
- This is a hard policy gate: targetSdk 36 apps that don't handle insets correctly will look broken.

### Android — Predictive Back (default ON, API 36)

- targetSdk 36: predictive back gesture animations are default ON for back-to-home, cross-task, cross-activity.
- `onBackPressed()` is **no longer dispatched**. Use `OnBackPressedDispatcher` (Activity) or `BackHandler` (Compose).
- Plan back-stack semantics carefully when porting from web's history-stack model.

### Android — Adaptive forced resizability (sw ≥ 600dp, API 36)

- For displays with smallest width ≥ 600dp at targetSdk 36, the following Manifest / runtime constraints are **ignored**:
  - `screenOrientation`, `resizableActivity`, `minAspectRatio`, `maxAspectRatio`
  - `setRequestedOrientation()` / `getRequestedOrientation()`
- Exceptions: games (`appCategory="game"`), screens < sw 600dp, user override.
- Temporary opt-out: `PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY` (expires API 37).
- **Window Size Class**: compact / medium / expanded / **large** / **extra-large** (new). Use Compose Adaptive Layouts 1.2+ for foldable / trifold support.

### Android — Glance for App Widgets

- **Jetpack Glance** (Compose-runtime-based) is the recommended path for new widgets. RemoteViews directly is legacy.
- Battery-friendly, integrates with `PreferencesDataStore`.

### Cross-platform UX shifts

- **Photo Picker / Photo Picker Everywhere** — On Android, use Photo Picker by default. Holding `READ_MEDIA_IMAGES` for non-essential reasons is out of policy since 2025-05-28.
- **Credential Manager (Android) / Passkey (iOS)** — System-managed credential UI, not custom auth screens. See `data-and-auth-porting.md`.
- **AI feature disclosure UI** — App Store 5.1.2(i) requires explicit consent UI naming the third-party AI provider before any user data leaves the device. Plan this UI flow at MVP, not post-MVP.

### OS Baselines (2026 recommendation)

| Platform | Default min | Aggressive | Conservative |
|----------|-------------|------------|--------------|
| iOS | **17** (SwiftData, `@Observable`, latest SwiftUI APIs) | iOS 26 (Liquid Glass + Foundation Models) | iOS 16 (Core Data, no SwiftData) |
| Android | API 28 (Android 9) | API 31 (Material You / SplashScreen / Photo Picker) | API 24 (legacy Java time APIs, more polyfills) |

`targetSdk` (Android): 35 mandatory since 2025-08-31, expect 36 during 2026.

---

---

## Navigation

| Concern | iOS (HIG) | Android (Material 3) |
|---------|-----------|----------------------|
| Top-level structure | Tab bar (3-5 tabs) at bottom; root of `TabView` | Navigation bar (3-5 destinations); `NavigationBar` |
| Hierarchy depth | Push via `NavigationStack`; ≤ 3 levels comfortable | Push via NavController; back-stack supports more depth |
| Back affordance | Top-left chevron + edge-swipe | System back button + top-left back arrow |
| Modal | `.sheet` (drag handle), `.fullScreenCover` | `ModalBottomSheet`, `Dialog`, full-screen |
| Detail view | Push, or large-screen `NavigationSplitView` | Push, or `TwoPaneLayout` for tablet/foldable |
| Bottom sheet | Resizable sheet (iOS 16+) | `ModalBottomSheet` (default Material 3) |
| Toolbar position | Top, with large title; bottom toolbar for actions | Top app bar (small/center/medium/large variants) |
| FAB | Not idiomatic | Material FAB for primary action when appropriate |
| Search | `.searchable` modifier on top | `SearchBar` Composable, often docked |

**Divergence to expect:**
- iOS rarely uses FAB; primary action goes to toolbar.
- Android predictive back (API 34+) and gesture nav change choreography.
- iPad supports multi-column `NavigationSplitView`; Android tablets use adaptive layouts.

---

## Gestures

| Gesture | iOS | Android |
|---------|-----|---------|
| Edge swipe back | System (default in `NavigationStack`) | System back gesture (predictive on 14+) |
| Swipe-to-action (rows) | `.swipeActions` modifier | `SwipeToDismissBox` |
| Pull-to-refresh | `.refreshable` modifier | `PullToRefreshBox` |
| Long-press menu | `.contextMenu` (system-rendered) | `DropdownMenu` after long-press |
| Drag and drop | `.draggable` / `.dropDestination` | `DragAndDrop` API (Android 7+, mature 8+) |
| Pinch to zoom | `MagnificationGesture` | `pointerInput` with detectTransformGestures |
| Haptics | `Haptic` modifier / `UIFeedbackGenerator` | `Vibrator` / `HapticFeedback` |

Don't translate web hover states 1:1. Mobile has no hover. Use long-press for "more info" patterns and tap for primary action.

---

## Typography & Type Scale

| iOS | Android |
|-----|---------|
| `.font(.largeTitle)`, `.title`, `.headline`, `.body`, `.caption`; system Dynamic Type | Material 3 type scale: `displayLarge`, `headlineLarge`, `titleLarge`, `bodyLarge`, `labelLarge`; respects `fontScale` |
| Default font: SF Pro / SF Compact | Default font: Roboto (or product Sans for Google apps) |
| Custom font: `Asset Catalog` + `Info.plist` | Custom font: `res/font/` + `FontFamily` |

**Rule:** Use the platform's semantic type scale. Don't port web's "16px / 14px / 12px" stack literally — use Dynamic Type / `fontScale` so accessibility settings work.

---

## Color, Theming, Dark Mode

| iOS | Android |
|-----|---------|
| Asset Catalog colors with `Any`/`Dark` appearance | Material 3 ColorScheme + `darkColorScheme()` |
| Dynamic colors via `Color(.systemBackground)` etc. | Dynamic Color from wallpaper (API 31+) |
| Symbol colors via `tint` | `MaterialTheme.colorScheme.primary` |
| Tint vs accent | `accentColor` modifier | `colorScheme.primary` / `secondary` |

**Mandatory:** Both platforms ship with full dark-mode support if the web product has it. Dark mode is a baseline expectation, not a feature.

---

## Motion & Animation

| iOS | Android |
|-----|---------|
| SwiftUI `withAnimation`, `.animation(.spring())` | Compose `AnimatedVisibility`, `animateContentSize`, `Modifier.animateContentSize` |
| Symbol effects (`.symbolEffect`) iOS 17+ | Material motion: shared transitions, container transform |
| Default curves: spring, ease | Material 3 motion durations and easings |
| Reduce Motion respected via `accessibilityReduceMotion` | `LocalDensity.current.fontScale` and `Settings.Global.ANIMATOR_DURATION_SCALE` |

Never ship motion that ignores Reduce Motion / Animator scale. Both stores penalize accessibility failures.

---

## Iconography

| iOS | Android |
|-----|---------|
| SF Symbols (5,000+ glyphs, multi-color, hierarchical) | Material Symbols / Material Icons |
| Custom: SVG → Asset Catalog vector | Custom: vector drawables |
| Tab bar icons: SF Symbol filled/outlined pair | Nav bar icons: outlined for unselected, filled for selected |

Use SF Symbols on iOS by default. Custom icons require justification.

---

## Lists, Cards, Empty States

| iOS | Android |
|-----|---------|
| `List`, `LazyVStack`, `Section`; insets edge-to-edge or grouped | `LazyColumn`, `LazyVerticalGrid`; cards via `Card` Composable |
| Plain vs grouped vs inset list styles | Card styles: filled, elevated, outlined |
| Pull-to-refresh + bottom-edge load-more | Pull-to-refresh + `LazyPagingItems` |
| Empty state: text + symbol + optional CTA | Empty state: illustration + text + CTA |

---

## Forms & Input

| Concern | iOS | Android |
|---------|-----|---------|
| Single-line input | `TextField` | `OutlinedTextField` / `TextField` |
| Multi-line | `TextEditor` | Same Composables, multi-line config |
| Validation | `.onChange`, ViewModel validation | Compose state + ViewModel validation |
| Keyboard avoidance | Built into ScrollView | `Modifier.imePadding()`, edge-to-edge handling |
| Autofill | `.textContentType` | Autofill framework hints + Credential Manager for passwords |
| Date / time | `DatePicker` | `DatePicker` / `TimePicker` Material 3 |
| Picker | `Picker` (segmented, wheel, menu) | `DropdownMenu`, `SegmentedButton` |

**Critical:** Both platforms have password-manager integration (iOS Keychain, Android Credential Manager). Web `<input type="password">` patterns must use the right `textContentType` / Autofill hints to populate password managers.

---

## A11y

| iOS | Android |
|-----|---------|
| VoiceOver labels via `.accessibilityLabel`, `.accessibilityHint` | TalkBack labels via `Modifier.semantics { contentDescription = … }` |
| Dynamic Type | Font scale |
| Reduce Motion | Animator scale |
| Switch Control | Switch Access |
| Voice Control | Voice Access |
| Color contrast: WCAG AA minimum | Same |

A11y must be designed at blueprint, not retrofitted. Document `accessibilityLabel` / `contentDescription` per component in the design handoff.

---

## OS Integration

| Capability | iOS | Android |
|-----------|-----|---------|
| Share | UIActivityViewController / `ShareLink` | `ACTION_SEND` Intent |
| Open URL | `openURL` env / `Link` | Intent.ACTION_VIEW |
| Mail / SMS | `MFMailComposeViewController` / `MFMessageComposeViewController` | Intent.ACTION_SENDTO |
| Calendar | EventKit | CalendarContract |
| Contacts | Contacts framework | ContactsContract |
| Photos | PhotosUI / PHPickerViewController | PhotoPicker (modern) |
| Files | UIDocumentPickerViewController | Storage Access Framework |
| Maps | MapKit | Maps SDK / OSM |
| Sign in with Apple | AuthenticationServices | (Required for App Store if any third-party login is offered) |
| Sign in with Google | (one option among many) | Credential Manager (recommended) |
| Biometric auth | LocalAuthentication (Face ID / Touch ID) | BiometricPrompt |

---

## Permissions UX

| iOS | Android |
|-----|---------|
| `Info.plist` usage descriptions are mandatory; missing string = crash | Manifest permission + runtime request |
| Pre-prompt rationale before system dialog | Pre-prompt rationale before system dialog |
| One-time / While Using App / Always (location) | `ACCESS_FINE_LOCATION` / `ACCESS_COARSE_LOCATION` / background tier |
| Settings deep link via `UIApplication.openSettingsURLString` | `Settings.ACTION_APPLICATION_DETAILS_SETTINGS` |
| Notification permission: explicit request (iOS 12+) | Notification permission: explicit request (API 33+) |

> **Never** request permissions on app launch. Always trigger contextually with a custom rationale screen.

---

## Errors, Loading, Empty States

| State | iOS | Android |
|-------|-----|---------|
| Loading | `ProgressView` (spinner / progress bar) | `CircularProgressIndicator` / `LinearProgressIndicator` |
| Skeleton | Custom shimmer view | Custom shimmer (e.g., `placeholder` modifier) |
| Error | Inline error or sheet; `Alert` for blocking | Snackbar (transient), Dialog (blocking), inline error |
| Empty | Title + symbol + optional CTA | Title + illustration + CTA |
| Offline banner | Top inset banner with retry | Snackbar with retry, or persistent top banner |

---

## Web → Native UX Patterns

| Web pattern | iOS | Android |
|-------------|-----|---------|
| Modal centered dialog | Sheet (.sheet) or Alert | ModalBottomSheet or Dialog |
| Toast | Use sparingly; system notification or status banner | Snackbar |
| Hover tooltip | Long-press accessibility hint, or "i" button | Long-press tooltip (Material 3) |
| Sticky header | `.toolbar(.hidden, for: .navigationBar)` + custom | `LargeTopAppBar` collapsed/expanded |
| Sidebar nav | iPad split view; iPhone tab bar | Navigation drawer or bottom nav |
| Multi-column layout | NavigationSplitView (iPad) | TwoPaneLayout / adaptive (foldables, tablets) |
| Footer | Toolbar bottom buttons | Bottom app bar (Material 3) |
| Breadcrumb | Avoid; collapse to push stack | Avoid; collapse to push stack |

---

## OS Version Baselines (Recommended)

| Platform | Default min | Aggressive | Conservative |
|----------|-------------|------------|--------------|
| iOS | 16 | 17 (SwiftData, `@Observable`) | 15 (legacy NavigationView pain) |
| Android | API 28 (Android 9) | API 31 (Material You dynamic color) | API 24 (older Java time, more polyfills) |

Document choice and excluded-user percentage from web analytics.

---

## Output Skeleton

```markdown
# Platform UX Adaptation Plan: <App Name>

## Navigation
- iOS top-level: TabView with N tabs ([list])
- Android top-level: NavigationBar with N destinations ([list])
- Modal patterns: …
- Deep-link routing: …

## Gestures
- Pull-to-refresh: ✓ on N screens
- Swipe-to-action: ✓ on M lists
- Long-press menus: …

## Type & Color
- Type scale: HIG default / Material 3 default
- Dark mode: ✓
- Dynamic Color (Android): ✓ / ✗
- Custom font: …

## Motion
- Default curves: …
- Reduce Motion respect: ✓

## A11y
- VoiceOver labels: documented per component
- TalkBack labels: documented per component
- Min contrast: WCAG AA

## Permissions
- Pre-prompt rationale screens: [list]
- Permissions requested: [list with timing]

## OS baselines
- iOS NN (excludes ~X% of users)
- API NN (excludes ~Y% of users)

## Web→Native UX deltas
- [list of deliberate divergences with rationale]
```

This plan is consumed by `Native` (implementation) and `Vision`/`Muse` (design system tuning).
