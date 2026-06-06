# iOS Human Interface Guidelines (HIG)

> Apple's design guidelines reference for the Native skill. iOS 26 / Liquid Glass-aware.
> Source: <https://developer.apple.com/design/human-interface-guidelines/>
> Last validated against secondary sources: 2026-05 (cutoff). For canonical wording, always re-fetch the official URL.

## Scope

HIG is Apple's design contract across **iOS 26, iPadOS 26, macOS Tahoe 26, watchOS 26, tvOS 26, visionOS 26** — a unified design language introduced at WWDC 2025 (2025-06-09). Native uses HIG as the platform-convention baseline before scaffolding any iOS feature.

This reference is structured the same way HIG is — **Platforms / Foundations / Patterns / Components / Inputs / Technologies** — with implementation hooks back into `SKILL.md` and other `reference/` files.

## Top-level Categories

| Category | Purpose |
|----------|---------|
| **Platforms** | Per-OS adaptation rules (iOS/iPadOS/macOS/watchOS/tvOS/visionOS); shared design language across all six in iOS 26 era |
| **Foundations** | Color, typography, layout, materials, motion, accessibility, inclusion, privacy — the baseline visual system |
| **Patterns** | Cross-cutting interaction patterns (navigation, search, onboarding, modality, settings, feedback, charts, drag-and-drop) |
| **Components** | Concrete UI building blocks (bars, buttons, selection, lists, content views, presentation views) |
| **Inputs** | Touch gestures, keyboard, pointer, pencil, voice, game controllers, eyes (visionOS) |
| **Technologies** | Framework-specific integration (SwiftUI, WidgetKit, App Intents, Live Activities, Apple Intelligence, etc.) |

---

## 1. Liquid Glass (iOS 26)

**The defining iOS 26 design change.** A system-wide material that combines optical glass with fluid, context-adaptive behavior. The first major visual evolution since iOS 7.

### Variants

| Variant | Behavior | Use |
|---------|----------|-----|
| **Regular** | Background blur + refraction + specular highlights; adapts to underlying content luminance | Default for navigation chrome |
| **Clear** | Higher transparency, minimal blur | Used by system in specific places (e.g., dynamic tab-bar shrink) |

### Where to apply (`.glassEffect()` allowed)

- **Tab bars** — floating capsule inset from edge; 2-5 tabs; search may render as a separate Liquid Glass "island"
- **Navigation bars** — top chrome; transitions from translucent → blurred as content scrolls
- **Toolbars** — bottom action bars
- **Sheets / Popovers** — modal surfaces
- **Alerts** — system-rendered, no opt-in needed
- **Floating buttons / controls** — when they sit above content as navigation chrome

### Where NOT to apply

- **Content layers**: lists, tables, cards, body text, media. Liquid Glass on content destroys legibility.
- **Static cells**: list rows look essentially unchanged from prior iOS — do not force `.glassEffect()` on them.
- **Backgrounds**: full-screen Liquid Glass is reserved for the system (Lock Screen, Control Center). App backgrounds stay opaque.

### Critical rules

- **Hierarchy through depth, not contrast** — interface importance is communicated via translucency, refraction, and depth, not via color saturation or size deltas.
- **Standard SwiftUI components on iOS 26 receive Liquid Glass automatically on Xcode 26 recompile.** Do not force-opacify them to "hide" the effect — collides with system behavior and produces visual glitches.
- **Adapt content, not chrome.** If Liquid Glass over content looks wrong, change the content layout (more padding, opaque background sections) — never disable the chrome material.
- **Accessibility risk**: Liquid Glass relies on translucency. Respect `accessibilityReduceTransparency` and `accessibilityIncreaseContrast` (system handles automatically when you use standard components; verify in custom views).

### Fallback (iOS 17/18)

- Standard `Material` (`.regularMaterial`, `.thinMaterial`) on iOS 17/18 — looks intentional, not broken.
- Avoid `if #available(iOS 26, *)` branching per call site; design your component once and let the system render appropriately.

### Icon variants (Icon Composer)

iOS 26 requires **4 icon variants** for App Store submission:

| Variant | Use |
|---------|-----|
| **Light** | Default; light system appearance |
| **Dark** | Dark system appearance |
| **Tinted** | User-selected tint mode (monochrome with accent) |
| **Clear** | Liquid Glass-style translucent (light/dark) |

Tool: **Icon Composer** (Xcode 26). Export targets all four from one source.

→ Implementation: `SKILL.md` Native Stack Defaults / Liquid Glass scope row, `reference/modern-stack.md`

---

## 2. Foundations

### Color

- **Semantic colors first** (`Color.primary`, `Color.accentColor`, `Color(.systemBackground)`, etc.) — auto-adapt to Light Mode / Dark Mode / Increase Contrast / High Contrast.
- **Asset catalog color sets** support Any/Light/Dark + High Contrast variants. Always provide both light/dark; provide HC variants when the contrast ratio against background drops below WCAG AA in dynamic conditions.
- **Tint color** (`.accentColor` / `.tint(_:)`) applied to interactive elements. Liquid Glass refracts/inherits surrounding context — do not hard-code colors that fight system tints.
- **Avoid color-only signals** — pair color with shape, label, or icon. Color-only is inaccessible for color-blind users and conflicts with tinted icon mode.

### Typography (San Francisco)

- **SF Pro Text** — 19pt and below; optimized tracking for legibility at body sizes.
- **SF Pro Display** — 20pt and above; tighter tracking for large display copy.
- **SF Rounded** — rounded variant; use sparingly for friendly contexts.
- **SF Mono** — monospaced; code, fixed-width data.
- **New York** — serif; long-form reading contexts (Books, News).
- **SF Symbols** — 6,000+ system icons with weight/scale variants; align with text baseline.

**Dynamic Type — mandatory.** Use `Font.body`, `Font.title`, etc. via the text-style API; resolve via `.font(.body)` not `.font(.system(size: 17))`. Honors user-selected text size (xSmall → AX5).

| Text style | Default size (Large) | Use |
|-----------|---------------------|-----|
| `largeTitle` | 34pt | Top-level screen titles |
| `title` / `title2` / `title3` | 28 / 22 / 20pt | Section headers |
| `headline` | 17pt (semibold) | Emphasized body |
| `body` | 17pt | Default reading |
| `callout` / `subheadline` | 16 / 15pt | Secondary body |
| `footnote` / `caption` / `caption2` | 13 / 12 / 11pt | Supporting text |

### Layout

- **Touch target minimum: 44×44 points.** Smaller targets see ≥25% tap-error rates and fail accessibility audits.
- **Safe areas**: respect `safeAreaInsets` (Dynamic Island, Home Indicator, status bar). Use `.ignoresSafeArea()` only for full-bleed media.
- **Margins**: 16pt default horizontal margin on iPhone, 20pt on iPad. Use `Layout` API or `.padding(.horizontal)` with `EdgeInsets` from the environment.
- **Edge-to-edge content**: in iOS 26, content typically extends behind translucent chrome — design backgrounds to look coherent under blurred glass.

### Materials (pre-Liquid Glass)

Standard `Material` system (still relevant for iOS 17/18 fallback and as a content-layer alternative):

| Material | Translucency |
|----------|--------------|
| `.ultraThinMaterial` | Most translucent |
| `.thinMaterial` | |
| `.regularMaterial` | Default |
| `.thickMaterial` | |
| `.ultraThickMaterial` | Most opaque |

### Motion

- **Reduce Motion**: honor `accessibilityReduceMotion` — replace parallax/spring with cross-fades.
- **Default spring**: SwiftUI `.spring()` and `.smooth` / `.snappy` / `.bouncy` presets (iOS 17+) — prefer presets over manual `response`/`dampingFraction`.
- **Live Activities** and **App Intents UI** have their own motion budgets — see `reference/push-notifications.md`.

### Accessibility

- **VoiceOver labels** on every interactive element: `.accessibilityLabel`, `.accessibilityHint`, `.accessibilityValue`.
- **Dynamic Type**: see above.
- **Color contrast**: minimum WCAG AA (4.5:1 normal, 3:1 large text); validate with Accessibility Inspector.
- **Reduce Transparency / Increase Contrast / Differentiate Without Color**: honor system flags; do not gate features on visual perception alone.
- **VoiceOver Rotor**: enable navigation by headings, links, form controls — use `.accessibilityRotor` for custom rotors when justified.
- **Switch Control / Voice Control / AssistiveTouch**: ensure focus order is logical (`.accessibilitySortPriority`).

→ EU Accessibility Act (EAA) EN 301 549 conformance from 2025-06-28 — see `reference/store-compliance.md`.

### Inclusion

- **Inclusive language**: avoid gendered defaults, ableist metaphors ("crazy", "blind to"), idioms that don't translate. Hand off copy to `Polyglot` for review.
- **Representation**: imagery, avatars, default names should not skew to a single demographic.
- **Localization**: Bidirectional (RTL) layout, ICU plurals, locale-aware date/number formats — see `reference/patterns.md`.

### Privacy

- **Required Reasons API** declarations in `PrivacyInfo.xcprivacy` (mandatory since 2024-05; 3rd-party SDKs since 2025-02-12).
- **Permission requests**: soft pre-prompt before system dialog; first denial is sticky (only Settings can re-grant).
- **Data minimization**: request the smallest permission scope (e.g., `WhenInUse` not `Always` for location); request only when needed in context.
- **App Tracking Transparency (ATT)**: required for cross-app tracking; mandatory prompt copy rules.

→ Hand off to `Cloak`. Detail: `reference/store-compliance.md`.

---

## 3. Patterns

Cross-cutting interaction patterns. Map each to SwiftUI primitives.

| Pattern | When | SwiftUI |
|---------|------|---------|
| **Top-level navigation** | 2-5 main app sections | `TabView` (Liquid Glass capsule on iOS 26) |
| **Hierarchical navigation** | Drill-down (list → detail) | `NavigationStack` + `NavigationLink` |
| **Multi-column** | iPad / foldable / Mac | `NavigationSplitView` (2- or 3-column) |
| **Modal presentation** | Self-contained task | `.sheet`, `.fullScreenCover`, `.popover`, `.alert`, `.confirmationDialog` |
| **Search** | Find within content | `.searchable` — renders as dedicated Liquid Glass island in iOS 26 tab bars |
| **Onboarding** | First-run + feature discovery | Minimal screens (3-5 max); skip-by-default; honor Reduce Motion |
| **Settings** | App preferences | `Form` with `Section` / `LabeledContent` / Toggles / Pickers — match Settings.app conventions |
| **Empty states** | Zero data | `ContentUnavailableView` (iOS 17+) — built-in label + system image + description |
| **Feedback (haptic)** | Confirmation, success, error | `SensoryFeedback` API (iOS 17+); never for ambient/decorative haptics |
| **Pull to refresh** | Re-fetch list | `.refreshable { }` — system handles spinner positioning under Liquid Glass |
| **Drag and drop** | Cross-app transfer | `Transferable` protocol (iOS 16+); declare `UTType` |
| **Sharing** | Out-of-app | `ShareLink` — never custom share UI for system data types |
| **Live Activities** | Real-time updates on Lock Screen / Dynamic Island | ActivityKit; max 8h active + 4h stale; ~4KB payload — see `reference/push-notifications.md` |

### Modality rules

- **Use sparingly** — modals interrupt flow. Reserve for self-contained, must-complete tasks.
- **Always provide a cancel path** — top-leading "Cancel" + top-trailing "Done"/"Save" on sheets.
- **`.fullScreenCover` only when truly full-screen** (e.g., onboarding, immersive content). Default to `.sheet` for everything else.
- **Sheet detents** (`.presentationDetents([.medium, .large])`): respect natural content height; avoid forcing `.large` for short forms.

---

## 4. Components

### Bars

| Component | SwiftUI | Notes |
|-----------|---------|-------|
| **Navigation bar** | `.toolbar { ToolbarItem(placement: .topBarLeading) {} }` | Title via `.navigationTitle()`; `.toolbarTitleDisplayMode(.inline | .large)` |
| **Tab bar** | `TabView { Tab("Home", ...) {} }` | 2-5 tabs; persistent; Liquid Glass capsule on iOS 26 |
| **Toolbar** | `.toolbar` with `.bottomBar` placement | Action verbs; Liquid Glass on iOS 26 |
| **Side bar** | `NavigationSplitView` sidebar column | iPad / Mac; not iPhone |
| **Status bar** | Managed by system | `.statusBarHidden()` only for immersive content |

### Buttons

| Component | SwiftUI | Use |
|-----------|---------|-----|
| **Standard button** | `Button("Save") { }` | Default action |
| **Bordered / Borderless** | `.buttonStyle(.bordered)` / `.borderless` | Visual emphasis |
| **Bordered Prominent** | `.buttonStyle(.borderedProminent)` | Primary CTA |
| **Plain** | `.buttonStyle(.plain)` | Text-like; no chrome |
| **Glass** (iOS 26) | `.buttonStyle(.glass)` | Liquid Glass treatment |
| **Toggle** | `Toggle(isOn:)` | Binary state; never repurpose as button |
| **Menu** | `Menu("...") { Button(...) }` | Grouped actions; supports submenus |
| **Link** | `Link("Open", destination:)` | External URL; system handles |
| **ShareLink** | `ShareLink(item:)` | System share sheet |

### Selection

| Component | SwiftUI |
|-----------|---------|
| **Picker** (segmented / wheel / menu / inline) | `Picker(...)` with `.pickerStyle()` |
| **Date Picker** | `DatePicker(...)` with `.compact` / `.wheel` / `.graphical` |
| **Stepper** | `Stepper(value:)` |
| **Slider** | `Slider(value:)` |
| **Toggle** | `Toggle(...)` |
| **Checkbox-like** | Use Toggle with `.toggleStyle(.button)` (iOS 16+) |

### Lists & content

| Component | SwiftUI | Notes |
|-----------|---------|-------|
| **List** | `List { }` | `.plain` / `.grouped` / `.insetGrouped` / `.sidebar` styles |
| **Form** | `Form { Section { } }` | Settings-style; use Section for groups |
| **DisclosureGroup** | Expandable | Section accordion |
| **Grid** | `Grid` / `LazyVGrid` / `LazyHGrid` | Use `LazyVGrid` for scroll |
| **Table** | `Table(data) { TableColumn(...) }` (iOS 16+) | iPad/Mac primarily |

### Presentation views

| Component | SwiftUI |
|-----------|---------|
| **Sheet** | `.sheet(isPresented:)` |
| **Full-screen cover** | `.fullScreenCover(isPresented:)` |
| **Popover** | `.popover(isPresented:)` (iPad/Mac); falls back to sheet on iPhone |
| **Alert** | `.alert(_, isPresented:)` |
| **Confirmation Dialog** | `.confirmationDialog(...)` |
| **Inspector** (iOS 17+) | `.inspector(isPresented:)` — iPad/Mac side panel |

---

## 5. Inputs

| Input | Notes |
|-------|-------|
| **Touch** | Standard taps, swipes; honor 44×44 min target; `.onTapGesture`, `.swipeActions` |
| **Long press** | `.onLongPressGesture` — consider Apple's haptic + preview pattern |
| **Drag** | `Transferable` for cross-app; `.draggable` / `.dropDestination` |
| **Keyboard** | `.keyboardType()`, `.submitLabel(.go)`, `.focused($field, equals:)`; honor hardware keyboard shortcuts via `.keyboardShortcut` |
| **Pencil (iPad)** | `PencilKit` — `PKCanvasView`; respect `UIPencilInteraction` system preferences |
| **Voice (Siri)** | App Intents framework — declare intents in `AppIntent.intent` files; donate from app for prediction |
| **Apple Intelligence** | On-device summarization, Writing Tools, Image Playground — declare entry points via App Intents |
| **Game controllers** | `GameController` framework; map standard controls |
| **Eyes (visionOS)** | Indirect gaze + pinch; out of iOS scope |

### Hardware-specific iOS 26

- **Camera Control** (iPhone 16+) — `AVCaptureControl` framework
- **Action Button** (iPhone 15 Pro+) — App Intents donation surfaces here
- **Dynamic Island** — Live Activities + standard system updates; never animate it for marketing

---

## 6. Technologies

Framework integration points HIG references. See parallel implementation in Native:

| Technology | HIG concern | Native `reference/` |
|-----------|-------------|---------------------|
| **SwiftUI** | All component / layout / pattern API surface | `modern-stack.md`, `patterns.md` |
| **WidgetKit** | Home Screen + Lock Screen + Control Center | `SKILL.md` Widgets row |
| **App Intents + Apple Intelligence** | Discoverability, Shortcuts, Siri, Writing Tools | `SKILL.md` AI on-device row |
| **Live Activities (ActivityKit)** | Lock Screen + Dynamic Island | `push-notifications.md` |
| **StoreKit 2** | Subscription / IAP UI | `store-compliance.md` |
| **Sign in with Apple / Passkeys (ASAuthorization)** | Account flows | `SKILL.md` Auth row, `patterns.md` |
| **MapKit** | Map UI + annotation conventions | — |
| **AVKit / AVFoundation** | Video player chrome | — |
| **Foundation Models** | On-device LLM — 5.1.2(i) disclosure UI rules | `store-compliance.md` |

---

## Implementation Hooks

| HIG concern | Where Native implements it |
|-------------|---------------------------|
| Liquid Glass adoption rules | `SKILL.md` Liquid Glass scope (Boundaries / Always), `liquidglass` Recipe |
| Foundations (Typography, Color, Layout) | `SKILL.md` Native Stack Defaults / Adaptive row |
| Dynamic Type | `SKILL.md` a11y_implementation |
| Privacy + Required Reasons API | `store-compliance.md`, `privacy` Recipe |
| Passkey / Sign in with Apple | `passkey` Recipe, `patterns.md` |
| Push + Live Activities | `push-notifications.md`, `push` Recipe |
| Deep links (Universal Links) | `deeplink-routing.md`, `deeplink` Recipe |
| Background tasks (BGTaskScheduler) | `bg-execution.md`, `bg` Recipe |
| App Store compliance | `store-compliance.md`, `store` Recipe |
| Staged rollout (TestFlight phased) | `release-rollout.md`, `rollout` Recipe |
| Mobile CI/CD (Xcode Cloud) | `mobile-ci-cd.md` |

---

## Cross-Platform Notes (HIG scope, iOS focus)

| Platform | iOS 26-era status |
|----------|-------------------|
| **iPadOS 26** | Same HIG; emphasis on multi-column (`NavigationSplitView`), Stage Manager, external keyboard, Apple Pencil |
| **macOS Tahoe 26** | Same HIG; menu bar, sidebar-first, window chrome, hover states |
| **watchOS 26** | Glanceable; complications; Smart Stack; corner / list / page navigation |
| **tvOS 26** | Focus engine; top shelf; remote-driven navigation |
| **visionOS 26** | Spatial; depth-based layout; gaze + pinch; ornaments |

Native scope is iOS + Android. Other Apple platforms are out of scope unless explicitly requested.

---

## Versioning & Drift

- **WWDC** annually (June) — HIG receives the largest updates immediately after.
- **Xcode 26 + iOS 26 SDK** required for App Store submission from **2026-04-28** — see `SKILL.md` Build row.
- **5.1.2(i) AI disclosure UI** — App Review enforces; design ahead of submission.
- **Liquid Glass icon variants** required for new submissions on iOS 26 SDK builds.

`#TODO(agent)`: re-fetch <https://developer.apple.com/design/human-interface-guidelines/> via a JS-capable fetcher (or read Apple Developer app PDF export) to validate any drift in section structure, component naming, or new technologies introduced after 2026-05.

---

## Authoritative URLs

| Topic | URL |
|-------|-----|
| HIG root | <https://developer.apple.com/design/human-interface-guidelines/> |
| Liquid Glass tech overview | <https://developer.apple.com/documentation/TechnologyOverviews/liquid-glass> |
| Tab bars | <https://developer.apple.com/design/human-interface-guidelines/tab-bars> |
| Typography | <https://developer.apple.com/design/human-interface-guidelines/typography> |
| SF Symbols | <https://developer.apple.com/sf-symbols/> |
| Apple Newsroom — design intro | <https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/> |
