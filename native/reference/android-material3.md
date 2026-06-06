# Android Material 3 (incl. Expressive)

> Google's Material Design 3 reference for the Native skill. Material 3 Expressive-aware (Google I/O 2025).
> Source: <https://m3.material.io/>
> Last validated against secondary sources: 2026-05 (cutoff). For canonical wording, always re-fetch the official URL.

## Scope

Material 3 (M3) is Google's open-source design system for Android, Wear OS, Web, and Flutter. **Material 3 Expressive** (announced Google I/O 2025-05-13) is the largest update since M3's introduction — research-backed evolution covering theming, components, motion, shape, and typography.

This reference is structured to match m3.material.io — **Foundations / Styles / Components / Patterns / Develop** — with Jetpack Compose API mappings and links back into `SKILL.md`.

## Top-level Sections

| Section | Purpose |
|---------|---------|
| **Foundations** | Accessibility, adaptive design, customization, design tokens, interaction states, layout, content design, iconography |
| **Styles** | Visual subsystems — color, typography, shape, motion, elevation, sound |
| **Components** | 30+ reusable UI components |
| **Patterns** | Cross-cutting flows — onboarding, settings, empty states, errors, navigation, layout patterns |
| **Develop** | Platform implementations — Android (Jetpack Compose, Views), Flutter, Web |
| **Expressive** | The 2025 evolution applied across the above |

---

## 1. Material 3 Expressive

The 2025 evolution. **Backed by more user research than any previous M3 update.** Available via **Compose Material 3 1.4+ / BOM 2025.12+**.

### What changed

| Area | M3 (2021) → M3 Expressive (2025) |
|------|----------------------------------|
| **Components** | New: `LoadingIndicator`, `SplitButtonLayout`, `ButtonGroup`, `HorizontalFloatingToolbar` / `VerticalFloatingToolbar`, `FloatingActionButtonMenu`, `FlexibleBottomAppBar`, `SecureTextField`, `HorizontalCenteredHeroCarousel`, `VerticalDragHandle`, `PullToRefreshBox` |
| **Shape** | +35 new shapes in Material Shapes Library; **shape morphing** (animate between shapes during state/interaction) |
| **Motion** | Spring physics system as default; `MotionScheme.expressive()` token set; per-component spring presets |
| **Typography** | Same 15-role type scale; richer emphasis variants; Roboto Flex variable axes (weight, width, optical size) |
| **Color** | Same dynamic color foundation; richer container variants and tonal palettes |
| **Strong Skipping** | Compose Compiler default since Kotlin 2.0.20 — Expressive components designed to be skippable |
| **Pausable Composition** | Compose 1.10 default ON — long compositions yield to frame budget |

### When to apply Expressive

- **New screens / new apps**: default to Expressive components from day 1.
- **Existing apps**: opt in per surface. Start with non-critical screens (settings, secondary tabs) to validate motion/shape adoption with users.
- **Branded / consumer apps**: Expressive is named "Expressive" because it leans into brand personality — strong fit for media, lifestyle, social, retail.
- **Enterprise / utility apps**: still benefit, but adopt conservatively — heavy motion can fatigue daily-use surfaces.

### Adoption checklist

- Compose BOM ≥ **2025.12** / Material 3 artifact ≥ **1.4.0**
- Kotlin **≥ 2.0.20** (Strong Skipping); Compose Compiler bundled with Kotlin since 2.0.0
- Use new spring tokens via `MaterialTheme.motionScheme` (don't hard-code `tween(300)`)
- Migrate `BottomAppBar` → `FlexibleBottomAppBar` where height flexibility helps
- Replace indeterminate `CircularProgressIndicator` → `LoadingIndicator` (richer motion, accessibility-improved announcements)
- Add `FloatingToolbar` for contextual actions where you previously stuffed icons into the top app bar

→ Implementation: `SKILL.md` Native Stack Defaults / UI row, `reference/modern-stack.md`

---

## 2. Foundations

### Accessibility

- **TalkBack labels**: `Modifier.semantics { contentDescription = ... }` or `Modifier.clearAndSetSemantics`.
- **Touch target minimum: 48×48 dp** (M3 baseline; matches Android platform). Use `Modifier.minimumInteractiveComponentSize()` to enforce.
- **Color contrast**: WCAG AA (4.5:1 normal, 3:1 large). M3's tonal palette generation respects this when seed color is appropriate.
- **TalkBack focus order**: `Modifier.semantics { isTraversalGroup = true; traversalIndex = ... }`.
- **Live regions**: `Modifier.semantics { liveRegion = LiveRegionMode.Polite }` for snackbars, error messages.
- **Reduce animations**: respect `Settings.Global.ANIMATOR_DURATION_SCALE == 0f` and `accessibilityManager.isReduceMotionEnabled`.

### Adaptive design

**Window Size Classes** (compact / medium / expanded / **large** / **extra-large** — last two added in 2025):

| Size class | Width range | Devices |
|-----------|-------------|---------|
| Compact | <600dp | Phones |
| Medium | 600-840dp | Small tablets, foldables unfolded |
| Expanded | 840-1200dp | Large tablets, ChromeOS |
| Large | 1200-1600dp | Desktop, large foldables |
| Extra-large | ≥1600dp | Desktop monitors |

API: `androidx.compose.material3.adaptive` 1.2+. Use `NavigationSuiteScaffold` (compact → NavigationBar; medium → NavigationRail; expanded → PermanentNavigationDrawer) for adaptive top-level navigation. Use `ListDetailPaneScaffold` / `SupportingPaneScaffold` / `ThreePaneScaffold` for list-detail and supporting layouts.

### Customization

- **Theme builder approach**: pick seed color → tonal palette generation → light + dark schemes → component override.
- **Dynamic Color** (API 31+): `dynamicLightColorScheme(context)` / `dynamicDarkColorScheme(context)` extracts palette from user wallpaper.
- **Brand override**: provide a fixed `ColorScheme` when brand is non-negotiable; still respect dark/light + Reduce Transparency.

### Design tokens

Single source of truth for style values. M3 publishes:

| Token namespace | Examples |
|----------------|----------|
| **Color** (`--md-sys-color-*`) | `primary`, `onPrimary`, `primaryContainer`, `onPrimaryContainer`, `surface`, `surfaceVariant`, `outline`, `error`, `errorContainer`, … |
| **Typography** (`--md-sys-typescale-*`) | `display-large`, `headline-medium`, `body-small`, `label-large`, … |
| **Shape** (`--md-sys-shape-*`) | `corner-none` / `extra-small` / `small` / `medium` / `large` / `extra-large` / `full` + 35 Expressive shapes |
| **Motion** (`--md-sys-motion-*`) | `easing-emphasized`, `easing-standard`, `duration-short1` … `duration-extra-long4`, + Expressive spring tokens |
| **Elevation** (`--md-sys-elevation-*`) | `level0` … `level5` (0/1/3/6/8/12 dp) |
| **State** (`--md-sys-state-*`) | Hover/focus/pressed/dragged opacity overlays |

Compose: tokens are exposed via `MaterialTheme.colorScheme`, `MaterialTheme.typography`, `MaterialTheme.shapes`, `MaterialTheme.motionScheme` (Expressive).

### Interaction states

| State | Visual |
|-------|--------|
| Enabled | Default |
| Disabled | Reduced opacity (typically 38% content, 12% container) |
| Hovered | State layer overlay 8% on container |
| Focused | State layer overlay 12% + focus indicator |
| Pressed | State layer overlay 12% + ripple |
| Dragged | State layer overlay 16% |

Always use `InteractionSource` + `indication`; never hand-roll state opacity per component.

### Layout

- **Compact baseline grid**: 4dp (icons + tight spacing), 8dp (component-internal), 16dp (default padding).
- **Margins**: 16dp default screen edge; 24dp on medium+.
- **Material spacing tokens**: `padding-small` (8dp), `medium` (16dp), `large` (24dp) — use via M3 component defaults.
- **Edge-to-edge**: `enableEdgeToEdge()` (mandatory under API 36 — `windowOptOutEdgeToEdgeEnforcement` removed); use `WindowInsets.systemBars` / `Modifier.windowInsetsPadding()` to respect inset regions.

### Content design

- **Voice and tone**: clear, concise, conversational; don't over-apologize for errors.
- **Sentence case** for buttons / titles (not Title Case).
- **Action labels are verbs**: "Save", "Delete", "Send" — not "OK".
- **Error messages**: state the problem, suggest the fix, link to action when possible.
- **Empty states**: explain what's missing + how to add the first item.

→ Hand off copy to `Prose` (UX writing) and `Polyglot` (localization).

### Iconography

- **Material Symbols** — variable-font icon library. Three styles: Outlined (default), Rounded, Sharp. Three optical sizes: 20 / 24 / 40dp. Four weights: 100/300/400/700.
- **Compose**: `androidx.compose.material.icons.Icons.Outlined.*` etc. (canonical 24dp set bundled with `material-icons-extended` artifact). For variable-font Material Symbols use the `compose-icons` library or import SVGs.
- **Always pair icon with text label** when an action is non-obvious or the user is keyboard-only.

---

## 3. Styles

### Color

**Color roles** (the M3 paradigm — semantic, not brand-positional):

| Role | Use | Pair |
|------|-----|------|
| **Primary** | Main brand color, primary actions | `onPrimary` (text/icons on Primary) |
| **Primary Container** | Standout containers, FAB | `onPrimaryContainer` |
| **Secondary** | Less prominent components, accents | `onSecondary` |
| **Secondary Container** | Filter chips, tonal buttons | `onSecondaryContainer` |
| **Tertiary** | Contrasting accents, balance Primary | `onTertiary` |
| **Tertiary Container** | Highlighted info | `onTertiaryContainer` |
| **Error** | Error states | `onError` |
| **Error Container** | Error backgrounds | `onErrorContainer` |
| **Background** | Default screen | `onBackground` |
| **Surface** | Card / sheet / dialog | `onSurface` |
| **Surface Variant** | Subtle surface contrast | `onSurfaceVariant` |
| **Outline** | Borders, dividers | — |
| **Outline Variant** | Less prominent borders | — |
| **Inverse Surface** | Snackbar, inverse contexts | `inverseOnSurface` |
| **Inverse Primary** | Primary on inverse surface | — |
| **Scrim** | Modal scrim | — |

Compose access: `MaterialTheme.colorScheme.primary`, etc.

**Dynamic Color** (API 31+): `dynamicLightColorScheme(LocalContext.current)`. Fall back to brand `ColorScheme` on API < 31 or when user has overridden.

### Typography

**15 type roles**, each defines size / weight / line-height / letter-spacing / font:

| Category | Role | Default size |
|----------|------|--------------|
| Display | `displayLarge` | 57sp |
| | `displayMedium` | 45sp |
| | `displaySmall` | 36sp |
| Headline | `headlineLarge` | 32sp |
| | `headlineMedium` | 28sp |
| | `headlineSmall` | 24sp |
| Title | `titleLarge` | 22sp |
| | `titleMedium` | 16sp |
| | `titleSmall` | 14sp |
| Body | `bodyLarge` | 16sp |
| | `bodyMedium` | 14sp |
| | `bodySmall` | 12sp |
| Label | `labelLarge` | 14sp |
| | `labelMedium` | 12sp |
| | `labelSmall` | 11sp |

Compose: `MaterialTheme.typography.bodyLarge`. Apply via `Text(..., style = MaterialTheme.typography.bodyLarge)`.

**Roboto Flex** variable font support: weight, width, optical size axes — supported in Expressive's emphasis variants.

### Shape

| Token | Corner radius |
|-------|---------------|
| `none` | 0dp |
| `extraSmall` | 4dp |
| `small` | 8dp |
| `medium` | 12dp |
| `large` | 16dp |
| `extraLarge` | 28dp |
| `full` | 50% (pill) |

Compose: `MaterialTheme.shapes.medium` returns `RoundedCornerShape(12.dp)`.

**Material Shapes Library (Expressive)**: 35 new shapes (squircle, scallop, cookie, etc.) + **shape morphing** API for animating between shapes during interaction. Use `MaterialShapes.Cookie9Sided`, `MaterialShapes.Scallop`, etc.

### Motion

**Easing tokens**:

| Token | Curve | Use |
|-------|-------|-----|
| `Standard` | `cubic-bezier(0.2, 0, 0, 1)` | Default in/out |
| `StandardDecelerate` | `(0, 0, 0, 1)` | Entering content |
| `StandardAccelerate` | `(0.3, 0, 1, 1)` | Exiting content |
| `Emphasized` | `(0.2, 0, 0, 1)` (default emphasis) | Important transitions |
| `EmphasizedDecelerate` | | Hero entrances |
| `EmphasizedAccelerate` | | Hero exits |

**Duration tokens**: `short1` (50ms) → `extraLong4` (1000ms). Pick by content complexity, not aesthetic preference.

**Expressive — spring system**: `MotionScheme.expressive()` exposes spring-based animations as defaults. Components use spring physics for state transitions, gestures, and shape morphing. Access via `MaterialTheme.motionScheme.defaultSpatialSpec()`, etc.

### Elevation

| Level | Elevation | Use |
|-------|-----------|-----|
| `level0` | 0dp | Background |
| `level1` | 1dp | Card resting |
| `level2` | 3dp | Slightly raised |
| `level3` | 6dp | FAB resting |
| `level4` | 8dp | Top app bar (scrolled) |
| `level5` | 12dp | Modal / FAB pressed |

Compose: `Surface(tonalElevation = ..., shadowElevation = ...)`. M3 prefers **tonal elevation** (color shift) over shadow on Surface (especially in dark mode).

### Sound

- **Sparingly**. Avoid notification fatigue.
- Use system sounds (`ToneGenerator`, `SoundPool`) for confirmations.
- Match haptic + sound for stronger feedback.

---

## 4. Components (Jetpack Compose API)

### Action

| Component | Compose API | Notes |
|-----------|-------------|-------|
| **Button** | `Button`, `FilledTonalButton`, `OutlinedButton`, `ElevatedButton`, `TextButton` | Default `Button` = filled |
| **Icon Button** | `IconButton`, `IconToggleButton`, `FilledIconButton`, `OutlinedIconButton`, `FilledTonalIconButton` | |
| **FAB** | `FloatingActionButton`, `SmallFloatingActionButton`, `LargeFloatingActionButton`, `ExtendedFloatingActionButton` | |
| **Split Button (Expressive)** | `SplitButtonLayout` | Two adjacent actions sharing a container |
| **Button Group (Expressive)** | `ButtonGroup` | Multiple related actions, even spacing |
| **FAB Menu (Expressive)** | `FloatingActionButtonMenu` | FAB that expands to a vertical menu of actions |
| **Floating Toolbar (Expressive)** | `HorizontalFloatingToolbar`, `VerticalFloatingToolbar` | Contextual floating action bar with optional attached FAB |
| **Toggle Button** | `ToggleButton`, `FilledIconToggleButton` | |

### Communication

| Component | Compose API |
|-----------|-------------|
| **Badge** | `Badge`, `BadgedBox` |
| **Snackbar** | `SnackbarHost`, `Snackbar` |
| **Loading Indicator (Expressive)** | `LoadingIndicator` (linear or circular; richer motion than `CircularProgressIndicator`) |
| **Linear Progress** | `LinearProgressIndicator` |
| **Circular Progress** | `CircularProgressIndicator` (legacy — prefer `LoadingIndicator` for new code) |
| **Tooltip** | `PlainTooltip`, `RichTooltip` |

### Containment

| Component | Compose API | Notes |
|-----------|-------------|-------|
| **Card** | `Card`, `OutlinedCard`, `ElevatedCard` | |
| **Dialog** | `AlertDialog`, `Dialog` (raw) | |
| **Divider** | `HorizontalDivider`, `VerticalDivider` | |
| **List Item** | `ListItem` | Headline + supporting text + leading/trailing |
| **Bottom Sheet** | `ModalBottomSheet`, `BottomSheetScaffold` | |
| **Side Sheet** | `ModalNavigationDrawer`, `PermanentNavigationDrawer`, `DismissibleNavigationDrawer` | |
| **Carousel (Expressive)** | `HorizontalUncontainedCarousel`, `HorizontalMultiBrowseCarousel`, `HorizontalCenteredHeroCarousel` | |

### Navigation

| Component | Compose API | Notes |
|-----------|-------------|-------|
| **Navigation Bar** | `NavigationBar` + `NavigationBarItem` | Bottom; 3-5 destinations |
| **Navigation Rail** | `NavigationRail` + `NavigationRailItem` | Side; for medium width |
| **Navigation Drawer** | `ModalNavigationDrawer`, `PermanentNavigationDrawer` | Side panel; for expanded width |
| **Top App Bar** | `TopAppBar`, `CenterAlignedTopAppBar`, `MediumTopAppBar`, `LargeTopAppBar` | |
| **Bottom App Bar** | `BottomAppBar` (legacy), `FlexibleBottomAppBar` (Expressive) | |
| **Tabs** | `TabRow`, `ScrollableTabRow`, `PrimaryTabRow`, `SecondaryTabRow` | |
| **Search Bar** | `SearchBar`, `DockedSearchBar` | |
| **Navigation Suite Scaffold** | `NavigationSuiteScaffold` | Adaptive (Bar / Rail / Drawer by Window Size Class) |

### Selection

| Component | Compose API |
|-----------|-------------|
| **Checkbox** | `Checkbox`, `TriStateCheckbox` |
| **Radio** | `RadioButton` |
| **Switch** | `Switch` |
| **Slider** | `Slider`, `RangeSlider` |
| **Chip** | `AssistChip`, `FilterChip`, `InputChip`, `SuggestionChip`, `ElevatedAssistChip`, `ElevatedFilterChip`, `ElevatedSuggestionChip` |
| **Date Picker** | `DatePicker`, `DateRangePicker`, `DatePickerDialog` |
| **Time Picker** | `TimePicker`, `TimeInput` |
| **Segmented Button** | `SingleChoiceSegmentedButtonRow`, `MultiChoiceSegmentedButtonRow` |

### Text Input

| Component | Compose API | Notes |
|-----------|-------------|-------|
| **Text Field** | `TextField` (filled), `OutlinedTextField` | |
| **Secure Text Field (Expressive)** | `SecureTextField` | Password-masking text field with system-managed secure storage |
| **Search Field** | `SearchBar` (above) | |

### Layout primitives

| Component | Compose API |
|-----------|-------------|
| **Scaffold** | `Scaffold` |
| **List Detail Pane Scaffold** | `ListDetailPaneScaffold` (adaptive) |
| **Supporting Pane Scaffold** | `SupportingPaneScaffold` (adaptive) |
| **Three Pane Scaffold** | `ThreePaneScaffold` (adaptive) |
| **Pull To Refresh** | `PullToRefreshBox` |
| **Drag Handle** | `VerticalDragHandle` |

---

## 5. Patterns

### Top-level navigation

- **2-5 destinations** in Navigation Bar; use Navigation Rail / Drawer for 6+.
- **Stay persistent** — destinations don't appear/disappear by context.
- Adaptive: `NavigationSuiteScaffold` swaps the surface (Bar/Rail/Drawer) automatically across Window Size Classes.

### Hierarchical navigation

- **Navigation Compose 2.8+ type-safe** — `@Serializable data class` destinations.
- Stack: `NavController.navigate(Destination(...))`.
- Deep links: `navDeepLink<Destination>()` with `App Links` (`assetlinks.json`) — see `reference/deeplink-routing.md`.

### Predictive back (API 36 default ON)

- Use `BackHandler` (Compose) / `OnBackPressedDispatcher` (Views).
- Manifest: `android:enableOnBackInvokedCallback="true"`.
- For Compose: `PredictiveBackHandler` for custom predictive animations.
- **Never** use `onBackPressed()` / `KEYCODE_BACK` — not invoked at targetSdk 36.

### Search

- `SearchBar` for in-app search at top level (expandable).
- `DockedSearchBar` for embedded search.
- Use Window Size Class to decide expanded vs docked.

### Onboarding

- Minimal screens (3-5 max); skip-by-default.
- Honor reduced animations.
- Never gate core app entry on permission grants — use soft pre-prompt + graceful degradation (see `reference/platform-permissions.md`).

### Empty states

- Headline + supporting text + primary action.
- Use `Icon` + `Text` + `Button` in a `Column`; consider `ListItem`-derived layout for in-list empties.

### Settings

- `Scaffold` + `LazyColumn` with `ListItem` rows + `Switch` / `RadioButton` / `Card` groupings.
- Match Settings app conventions: section headers, supporting text under headlines.

### Feedback

- **Snackbar** for transient confirmation (auto-dismiss).
- **AlertDialog** for blocking decisions only.
- **Haptic** via `HapticFeedback.performHapticFeedback(...)` (Compose `LocalHapticFeedback`); never decorative.
- **Sound** sparingly.

### Edge-to-edge

- `enableEdgeToEdge()` in `Activity.onCreate()` — mandatory under API 36.
- Apply `Modifier.windowInsetsPadding(WindowInsets.systemBars)` where chrome must respect insets.
- Use `Scaffold` — handles insets automatically when configured.

### Pull to refresh

- `PullToRefreshBox` (Expressive) — modern API replacing older `SwipeRefresh` patterns.

---

## 6. Develop (Compose-first)

### Versions to track

| Artifact | Min for Expressive |
|----------|-------------------|
| **Compose BOM** | **2025.12** + |
| **Material 3** | **1.4.0** + |
| **Kotlin** | **2.0.20** + (Strong Skipping default) |
| **Compose Compiler** | Bundled with Kotlin since 2.0.0 |
| **Compose Adaptive** | **1.2** + (Large / Extra-large size classes) |
| **Navigation Compose** | **2.8** + (Type-safe routes) |
| **AGP** | **8.5.1** + (16KB native libs) |
| **NDK** | **r28** + (default-aligned 16KB) |
| **Target SDK** | **36** mandatory by 2026-08-31 (Play) |

### State and lifecycle

- **Strong Skipping**: stable types skipped automatically. But **does NOT make types stable** — still apply `@Stable` / `@Immutable` or use `kotlinx.collections.immutable` (`PersistentList`, `ImmutableList`) for high-frequency unstable params.
- **`collectAsStateWithLifecycle()`** — mandatory for flows in UI.
- **`remember` keys** — match all observable deps; missing key causes stale state.

### Theming

```kotlin
MaterialTheme(
    colorScheme = if (useDynamic) dynamicLightColorScheme(LocalContext.current) else BrandLightScheme,
    typography = AppTypography,
    shapes = AppShapes,
    motionScheme = MaterialMotionScheme.expressive(),   // M3 Expressive
) { content() }
```

### Dark mode

- `isSystemInDarkTheme()` — switch between `lightColorScheme()` and `darkColorScheme()`.
- Provide explicit `dynamicDarkColorScheme()` for API 31+.
- Avoid hard-coding `Color.White` / `Color.Black` — use `MaterialTheme.colorScheme.surface` etc.

---

## Implementation Hooks

| Material 3 concern | Where Native implements it |
|-------------------|---------------------------|
| Compose + Material 3 Expressive adoption | `SKILL.md` Native Stack Defaults / UI row, `expressive` Recipe |
| Type-safe Navigation Compose 2.8+ | `SKILL.md` Navigation row, `reference/patterns.md` |
| Strong Skipping + immutable types | `SKILL.md` UI row |
| Window Size Classes (incl. Large / Extra-large) | `SKILL.md` Adaptive row |
| Edge-to-edge + predictive back (API 36) | `SKILL.md` edge_to_edge_predictive_back |
| Dynamic Color (API 31+) | `SKILL.md` android_m3_expressive |
| Material Symbols + variable fonts | `reference/patterns.md` |
| Credential Manager (Passkey) + Sign-in-with-Google | `passkey` Recipe, `SKILL.md` Auth row |
| FCM + Notification Channels (POST_NOTIFICATIONS) | `push-notifications.md`, `push` Recipe |
| App Links (assetlinks.json) | `deeplink-routing.md`, `deeplink` Recipe |
| WorkManager + Foreground Service Types | `bg-execution.md`, `bg` Recipe |
| Data Safety + Privacy classifications | `store-compliance.md`, `privacy` Recipe |
| 16KB native libs + targetSdk 36 | `SKILL.md` Build row, `store-compliance.md` |
| Staged rollout (Play) | `release-rollout.md`, `rollout` Recipe |

---

## Cross-Platform Notes (M3 scope, Android focus)

| Surface | M3 status |
|---------|-----------|
| **Android (mobile/tablet/foldable)** | Primary — Compose Material 3 + Expressive |
| **Wear OS** | M3 Expressive design language — `androidx.wear.compose.material3` (separate artifact) |
| **Android TV** | Compose for TV with M3 adaptation; not yet full Expressive parity |
| **Android Auto / Automotive OS** | Custom design constraints; not pure M3 |
| **Flutter** | `flutter_material` package — tracks M3 with lag |
| **Web** | `@material/web` — independent component set; mirrors M3 but separate API surface |

Native scope is iOS + Android mobile. Wear / TV / Auto are not Native's default scope unless explicitly requested.

---

## Versioning & Drift

- **Google I/O** annually (May) — Material updates typically announced here.
- **Compose BOM** updated quarterly — track via `androidx.compose:compose-bom-alpha` for previews.
- **Target SDK 36** mandatory on Google Play from **2026-08-31** for new apps and updates.
- **16KB native lib alignment** required on new releases since **2025-11-01**.
- **Material 3 Expressive stable** — confirmed in Compose Material 3 1.4+; APIs marked `@ExperimentalMaterial3ExpressiveApi` on earlier alphas; graduates to stable per-component.

`#TODO(agent)`: re-fetch <https://m3.material.io/> and <https://developer.android.com/jetpack/androidx/releases/compose-material3> via a JS-capable fetcher to validate exact `1.4.x` patch versions, `@ExperimentalMaterial3ExpressiveApi` graduation status per component, and any new Expressive components added after 2026-05.

---

## Authoritative URLs

| Topic | URL |
|-------|-----|
| M3 root | <https://m3.material.io/> |
| Foundations | <https://m3.material.io/foundations> |
| Styles | <https://m3.material.io/styles> |
| Components | <https://m3.material.io/components> |
| M3 Expressive blog | <https://m3.material.io/blog/building-with-m3-expressive> |
| Develop (Android) | <https://m3.material.io/develop/android> |
| M3 in Compose | <https://developer.android.com/develop/ui/compose/designsystems/material3> |
| Compose Material 3 releases | <https://developer.android.com/jetpack/androidx/releases/compose-material3> |
| Material Symbols | <https://fonts.google.com/icons> |
