# macOS Human Interface Guidelines (HIG)

> Apple's design guidelines reference for Native's macOS scope. macOS 26 "Tahoe" / Liquid Glass-aware.
> Source: <https://developer.apple.com/design/human-interface-guidelines/platforms/designing-for-macos>
> Last validated against secondary sources: 2026-07. For canonical wording, always re-fetch the official URL.

## Scope

This reference covers **macOS divergence only**. Shared HIG foundations (color, typography, Dynamic Type philosophy, motion/reduce-motion principles, inclusion, privacy posture) are documented once in [`native/reference/ios-hig.md`](../../native/reference/ios-hig.md) §2 — read that first for the cross-platform baseline introduced at WWDC 2025 (2025-06-09). This file documents where and how a **Mac app** departs from that baseline: menu bar, window chrome, pointer/hover, keyboard-first interaction, and Mac-only components.

Do not restate iOS component tables here — cross-reference them. A macOS app that reads like a scaled-up iPhone app has failed this HIG, regardless of code quality.

---

## 1. Liquid Glass on macOS — chrome only

macOS Tahoe 26 adopts the same Liquid Glass material introduced across iOS/iPadOS/macOS/watchOS/tvOS 26, but Mac's chrome surfaces differ from iOS's: there is no tab bar or bottom toolbar equivalent — the surfaces are **sidebar, toolbar, menu bar, and Dock**.

### Where Liquid Glass applies on Mac

| Surface | Behavior |
|---------|----------|
| **Menu bar** | Fully transparent by default in Tahoe 26 (`NSApplication` inherits system behavior automatically); user can toggle a solid background in System Settings → Menu Bar → "Show menu bar background" — do not fight this preference in-app |
| **Sidebar** (`NavigationSplitView` first column) | Floating Liquid Glass panel that reflects/refracts content beneath it; standard `List(selection:)` sidebar style receives this automatically on Xcode 26 recompile |
| **Toolbar** | Unified with title bar, Liquid Glass material, `ToolbarItem` groups render as glass segments |
| **Window controls / traffic lights** | Rounder window corners in Tahoe 26; traffic lights sit on the glass chrome, not opaque title bar |
| **Dock** | System-owned; app icons render inside Liquid Glass Dock tile — no app-side opt-out |
| **Popovers / sheets** | Same system material as iOS — no manual `.glassEffect()` needed for standard `.popover`/`.sheet` |

### Where NOT to apply (content layers)

- **Document content, canvas, list row backgrounds, table cell content, text views** — Liquid Glass on content destroys legibility and is explicitly out of scope per Apple's Tahoe guidance.
- **Custom content-area backgrounds** — keep opaque or use standard `Material` (`.regularMaterial`) if translucency is wanted for a content-adjacent panel; do not apply `.glassEffect()`.
- Do not manually force `.glassEffect()` onto standard `NavigationSplitView`/`.toolbar` components — Xcode 26 recompilation applies it system-wide already; manual application risks double-compositing.

### Critical rules (Mac-specific)

- **Respect the user's "Show menu bar background" toggle** — do not paint a custom opaque bar behind `MenuBarExtra` content to override it.
- **Known Tahoe 26 rough edges** (as of 2026-07, still present in some system apps per community reports): mismatched corner radii between adjacent floating panels, uneven toolbar heights when mixing custom `ToolbarItem` groups with system-provided ones. Test custom toolbar item padding against system defaults rather than assuming visual parity.
- **`accessibilityReduceTransparency` / `accessibilityIncreaseContrast`** apply on Mac exactly as on iOS — verify custom `NSViewRepresentable` chrome honors them; standard SwiftUI chrome does automatically.

### Fallback (Sonoma 14 / Sequoia 15)

- Standard `Material` (`.regularMaterial`, `.thinMaterial`) — this is what unified toolbar/sidebar already looked like pre-Tahoe; no visual regression.
- Do not gate every call site behind `if #available(macOS 26, *)` — design the component once; let system rendering vary per OS.

→ Implementation: `SKILL.md` Core Contract "Liquid Glass scope" row, `reference/layout-patterns.md`, `reference/macos-modern-stack.md`.

---

## 2. Menu bar — the app's primary command surface

Unlike iOS, where in-view controls carry most affordances, **the menu bar is the canonical, always-present command surface** on Mac. Every meaningful, repeatable action should be reachable from a menu, independent of window state or current selection.

### Non-negotiable rules

- **Standard top-level menu order**: App menu (named after the app) → File → Edit → View → [app-specific menus] → Window → Help. Do not reorder File/Edit/View/Window/Help, and do not omit Window or Help even for simple apps — `Commands` scene modifiers should extend, not replace, the system-provided defaults (`CommandGroup(replacing:)` only when truly superseding a default item).
- **App menu** contains: About, Settings… (⌘,), Services submenu, Hide/Hide Others/Show All, Quit (⌘Q). SwiftUI's `Settings` scene wires the Settings… item automatically when a `Settings { }` scene is declared.
- **Every command must be reachable via menu even when it also exists as a toolbar button or context-menu item.** A toolbar-only action with no menu equivalent fails discoverability and keyboard-only workflows.
- **Menu items reflect current state**: disable (don't hide) items unavailable for the current selection; use `isEnabled` bindings, not conditional item removal, so users can predict menu shape.
- **Ellipsis convention**: append `…` to any menu item that opens a dialog/sheet requiring further input before completing (e.g., "Export…", "Find…"). Omit it for immediate actions ("Save", "Duplicate").
- **Keyboard shortcut conventions** (do not deviate without strong justification) — full table in `reference/menu-commands.md` §4.
- **`MenuBarExtra`** (menu-bar-only utility apps): use `.menuBarExtraStyle(.window)` for rich custom content, `.menu` for a simple system-styled menu. Pair with `LSUIElement = true` in Info.plist to suppress a Dock icon and app-switcher entry when the app has no main window. See `reference/scenes.md` for scene wiring and `reference/menu-commands.md` for `Commands`/`CommandGroup` API detail.

→ Implementation: `reference/menu-commands.md` (full `Commands`/`CommandGroup`/`CommandMenu` API), `SKILL.md` Always list.

---

## 3. Window chrome, title bar, full-screen, tiling

### Title bar and traffic lights

- **Traffic lights** (close/minimize/zoom, red/yellow/green) are top-leading, fixed system position — never relocate or restyle them.
- **Unified toolbar**: default modern style; title bar and toolbar share one visual band (`.toolbar` content sits in the same chrome as the title). Avoid the legacy separated title-bar-then-toolbar look except when replicating a document-heavy legacy app intentionally.
- **Title bar text**: reflects the window/document title; for document-based apps, clicking the title reveals the proxy-icon path menu (handled automatically by `DocumentGroup`/`NSDocument` — do not build a custom equivalent).
- **`.windowStyle`/`.windowToolbarStyle`** (SwiftUI): `.unifiedCompact` for utility windows with minimal chrome, `.unified` as the general default.

### Full-screen and tiling

- **Full-screen** (green traffic light or ⌃⌘F): the app must remain usable — do not hide menu bar-dependent-only functionality; auto-hiding menu bar/Dock in full-screen is system behavior, not something the app manages.
- **Window tiling** (Stage Manager era, macOS 13+ tiling via drag-to-edge or Window menu "Move & Resize"): honor `NSWindow` resizable/minimum-size constraints (`.frame(minWidth:minHeight:)`) so tiling doesn't clip essential controls. Provide sensible `idealWidth`/`idealHeight` via `.defaultSize()`.
- **Multi-window apps**: each `WindowGroup` instance should be independently resizable and closable without side effects on sibling windows; use `SceneStorage`/`NSUserActivity` for restoration (see `reference/scenes.md`).

### Anti-pattern: fixed-size, non-resizable windows

Except for utility panels (About box, small `MenuBarExtra` popover windows), Mac users expect windows to resize, tile, and enter full-screen. Hardcoding a fixed window size for a primary app window is a strong signal of an iPad-app-shaped Mac app (§10).

→ Implementation: `reference/scenes.md` (window/scene composition, restoration).

---

## 4. Sidebar-first information architecture

Mac apps with hierarchical content default to a **3-column `NavigationSplitView`**: sidebar (navigation/filter) → content list → detail. This is the Mac-native analog to iOS's `TabView`-first navigation — Mac has no bottom tab bar convention; sidebar takes its place as primary navigation for apps with more than a handful of top-level sections.

| iOS pattern | Mac equivalent | Notes |
|-------------|-----------------|-------|
| `TabView` (2-5 sections) | Sidebar with equivalent sections as `List` rows | Mac reserves tabs for document-internal view switching (e.g., browser tabs), not app-level navigation |
| `NavigationStack` drill-down | Sidebar selection + detail column | Avoid deep push-navigation stacks on Mac; flatten to sidebar selection where possible |
| Bottom toolbar actions | Top unified toolbar `ToolbarItem`s | No bottom chrome convention on Mac |

- Sidebar sections use `List(selection:)` with `NavigationLink(value:)` or a bound selection model — not manual `Button` rows.
- **`.inspector()` modifier (macOS 14+)** adds a right-side detail/properties panel independent of the sidebar — use it for contextual metadata/properties, not as a second navigation surface. See `reference/layout-patterns.md`.
- Collapse behavior: sidebar should support user-driven collapse (⌘⌥S convention) without losing selection state.

---

## 5. Pointer, hover, and why Mac design differs from touch

Mac is a **pointer-first, indirect-manipulation** platform — this is the single largest interaction-model divergence from iOS/iPadOS, and it changes affordance design, not just input handling.

- **Hover is a first-class state.** Every interactive element should communicate hover (`.onHover`, `.hoverEffect` where applicable) — buttons highlight, table rows show reveal-on-hover action icons, links show pointer cursor changes. Touch has no hover equivalent, so iOS-ported components frequently omit this entirely.
- **Cursor rects**: change the pointer shape (`NSCursor.pointingHand`, `.resizeLeftRight`, `.iBeam`, etc.) over draggable dividers, resize handles, and clickable non-button elements. In SwiftUI, use `.onHover { NSCursor... }` or `.pointerStyle()` (macOS 15+, WWDC24) rather than leaving the default arrow over every control.
- **Reveal-on-hover controls**: list-row action buttons (delete, favorite, quick actions) should appear on row hover and stay hidden otherwise — reduces visual noise versus always-visible icon buttons, which read as cluttered on a dense pointer-driven UI.
- **Tooltips (`.help()`)**: every icon-only toolbar button, and any control whose purpose isn't obvious from its label, needs a tooltip. Touch interfaces have no tooltip equivalent (no persistent hover), so this is easy to omit when porting.
- **Precision affordances**: because pointer input is far more precise than touch, Mac controls can be smaller and denser (§6) — but must still show clear hover/pressed states since there is no touch "highlight on tap" feedback loop to substitute.
- **Right-click / secondary click**: every object that supports contextual actions needs a context menu (`.contextMenu { }`) — this is the Mac equivalent of iOS's long-press action sheet, but expected far more pervasively (on nearly every list row, canvas object, and text selection).

---

## 6. Keyboard-first expectations

Mac users, especially power users, expect near-total mouse-free operation. This is a harder requirement than iOS's keyboard support (external keyboard is optional there; on Mac, keyboard-primary is the default assumption).

- **Full Keyboard Access** (System Settings → Keyboard → Full Keyboard Access): when enabled, Tab/Shift-Tab must move focus through *all* controls, not just text fields (the macOS default without this setting). Test your view hierarchy with it enabled — custom `Button`/`Toggle`-like views built from `Shape`+`.onTapGesture` are invisible to it unless properly exposed as accessibility elements.
- **Focus rings**: visible focus indication (`.focusable()`, `@FocusState`) on every control reachable via Tab — do not suppress the system focus ring for a "cleaner" look; it is the primary way sighted keyboard-only users track position.
- **Tab traversal order**: should follow visual/logical layout (left-to-right, top-to-bottom, sidebar-before-detail). Verify order explicitly for custom layouts — `.focusable()` on ad hoc `ZStack` compositions doesn't guarantee a sane default order.
- **Shortcut discoverability**: every `.keyboardShortcut()` binding must have a corresponding, visible menu item showing that shortcut (SwiftUI does this automatically when the shortcut is attached via a `Commands` menu item — do not attach shortcuts only to invisible/global key handlers, which are undiscoverable).
- **Escape and Return semantics**: Esc cancels/dismisses (sheets, popovers); Return confirms the default/primary action in dialogs — wire `.keyboardShortcut(.cancelAction)` / `.keyboardShortcut(.defaultAction)` rather than hand-rolled key handling.

---

## 7. Control sizes and macOS-specific density

Mac supports denser layouts than iOS because of pointer precision (§5) and typically larger viewport/window sizes.

| Control size | SwiftUI | Typical use |
|--------------|---------|-------------|
| `.mini` | `.controlSize(.mini)` | Dense inspector rows, compact toolbars |
| `.small` | `.controlSize(.small)` | Default in inspector panels, secondary toolbars |
| `.regular` | `.controlSize(.regular)` (default) | Standard window content |
| `.large` | `.controlSize(.large)` | Primary CTAs in dialogs, onboarding |
| `.extraLarge` (macOS 14+) | `.controlSize(.extraLarge)` | Rare — hero actions only |

- **No 44×44pt minimum touch target rule on Mac** — that constraint is touch-specific (see `native/reference/ios-hig.md` §2 Layout). Mac controls can be considerably smaller since pointer clicks are precise; a 20-24pt icon button with a hover state is normal in a dense toolbar.
- **Table row height**: default `Table` row height is denser than an iOS `List` row — do not pad Mac table rows to iOS list-row height "for consistency"; it reads as wasted space.
- **Window minimum content width**: set realistic `.frame(minWidth:)` based on your densest toolbar/sidebar combination, not an iPad-derived minimum.

### Standard controls: Mac-only vs shared with iOS

| Control | Mac-only | Shared (SwiftUI cross-platform) | Notes |
|---------|:---:|:---:|-------|
| `Table` | | ✓ (macOS 12+/iOS 16+) | Primarily a Mac/iPad pattern; rare on iPhone |
| `NSToolbar`-backed `.toolbar` unification | ✓ | | Mac's title-bar+toolbar merge has no iOS equivalent |
| `MenuBarExtra` | ✓ | | No iOS analog |
| `Commands`/`CommandGroup`/`CommandMenu` | ✓ | | Menu bar is Mac/iPad-with-hardware-keyboard-specific |
| `.inspector()` | | ✓ (macOS 14+/iOS 17+) | Renders as a side panel on both, but far more common on Mac |
| `NSPopover`-backed `.popover` | | ✓ | Anchored popover is a Mac-native idiom that also exists on iPad |
| `.contextMenu` (right-click) | | ✓ | Shared API, but expected far more pervasively on Mac (§5) |
| Traffic-light window controls | ✓ | | No iOS window-chrome equivalent |
| `NSSplitView`/`NavigationSplitView` 3-column | | ✓ (also iPad) | Sidebar-first IA is shared with iPad, absent on iPhone |
| Drag-to-resize panes | ✓ | | Touch has no precise drag-divider equivalent |

---

## 8. Dock icon, badging, and Dock menu

- **App icon in the Dock**: the running-app indicator is a system-drawn dot beneath the icon — do not draw a custom equivalent.
- **Badging**: `NSApplication.shared.dockTile.badgeLabel` sets a numeric/text badge (unread count, etc.) — keep it short (1-3 characters typical); update it from a single source of truth to avoid drift from in-window counts.
- **Dock menu**: right-click (or click-and-hold) on the Dock icon shows a menu — implement `applicationDockMenu(_:)` (AppKit, via `NSApplicationDelegate`) to add app-specific quick actions (e.g., "New Window", recent documents). SwiftUI has no direct scene-level API for this; bridge via `NSApplicationDelegateAdaptor`.
- **Bounce-once vs bounce-until-clicked**: use `NSApplication.requestUserAttention(.informationalRequest)` (single bounce) for low-priority background completion, `.criticalRequest` (bounces until app is activated) sparingly — reserve for events that truly need the user's attention.

---

## 9. Notifications and Notification Center on Mac

- Mac notifications use the same `UserNotifications` framework as iOS (`UNUserNotificationCenter`) — request authorization, schedule via `UNNotificationRequest`, same categories/actions API.
- **Notification Center placement**: right-edge panel (Control Center + widgets + notifications), invoked from the menu bar clock/date or a trackpad/Magic Mouse swipe — app code has no control over presentation chrome, only content.
- **Do Not Disturb / Focus modes**: respect system suppression; do not attempt to work around Focus filtering with `.criticalAlert` (`UNNotificationInterruptionLevel.critical`) unless the notification is genuinely critical (e.g., recording-in-progress alerts) — critical alerts require a special entitlement and App Review justification.
- **Banner vs Alert style** is a user preference (System Settings → Notifications) per-app — do not assume banners auto-dismiss; some users configure Alerts (persist until dismissed).

---

## 10. Spotlight, Continuity, Handoff, Universal Control

| Technology | Mac touchpoint | API |
|-----------|-----------------|-----|
| **Spotlight** | Surface in-app content/actions in system search | `CSSearchableItem`/`CSSearchableIndex` (Core Spotlight), or App Intents for action-style entries |
| **Handoff** | Resume an in-progress task from iPhone/iPad on Mac (or vice versa) | `NSUserActivity` with `isEligibleForHandoff = true` — same API as iOS Handoff |
| **Universal Control** | User drags pointer/keyboard across a nearby iPad/Mac as one input surface | System-level; no app opt-in required, but drag & drop / pointer hover behavior (§5) should be robust since Universal Control routes real pointer events |
| **Continuity Camera / Universal Clipboard / AirDrop** | Import content from iPhone camera, shared clipboard, file sharing | `NSItemProvider`/`NSPasteboard` (Universal Clipboard is transparent), `AVFoundation` capture device enumeration includes Continuity Camera automatically |

→ Cross-device state continuity: pair with `reference/documents.md` (iCloud document sync) and `reference/scenes.md` (`NSUserActivity` restoration).

---

## 11. macOS accessibility

Shared accessibility principles (VoiceOver labels, Dynamic Type, WCAG contrast) live in [`native/reference/ios-hig.md`](../../native/reference/ios-hig.md) §2 Accessibility. Mac-specific divergence:

- **VoiceOver on Mac** navigates via the **VoiceOver cursor** and **rotor**, driven primarily by keyboard (VO modifier + arrows) rather than touch gestures — ensure custom controls expose correct `accessibilityRole`/`accessibilityLabel`/`accessibilityValue` via `NSAccessibility` protocols (AppKit) or SwiftUI's `.accessibilityElement`/`.accessibilityLabel` modifiers; the rotor's "Web Spot"/table/landmark navigation differs from iOS's simplified rotor.
- **Full Keyboard Access** (§6) has no iOS equivalent of this scope — iOS assumes touch as primary and keyboard as supplementary; Mac explicitly supports full mouse-free operation as a first-class accessibility mode, not just a power-user feature.
- **Increase Contrast**: `NSWorkspace.shared.accessibilityDisplayShouldIncreaseContrast` (or SwiftUI `@Environment(\.accessibilityIncreaseContrast)`) — verify custom-drawn borders/dividers remain visible when enabled; standard `Material`/Liquid Glass surfaces respond automatically.
- **Reduce Motion / Reduce Transparency**: `@Environment(\.accessibilityReduceMotion)` / `\.accessibilityReduceTransparency` — same API surface as iOS; Mac's Liquid Glass sidebar/toolbar (§1) is the surface most likely to need a Reduce Transparency fallback (falls back to an opaque or near-opaque material automatically for standard components; verify for custom chrome).
- **Accessibility Inspector** (bundled with Xcode): audit target — run against your app's window hierarchy to catch missing labels/roles before relying on manual VoiceOver testing. Treat a clean Accessibility Inspector pass as a `VERIFY` phase gate for accessibility-sensitive features, alongside the `hig` Recipe audit.

---

## 12. Dark Mode, accent color, vibrancy/materials

- **Dark Mode**: system-wide (`NSApp.effectiveAppearance`), same semantic-color-first approach as iOS (`Color.primary`, asset-catalog Any/Light/Dark color sets) — see `native/reference/ios-hig.md` §2 Color for the shared foundation.
- **Accent color**: users pick a system accent color (System Settings → Appearance) that flows into `Color.accentColor`/`.tint(_:)` automatically for standard controls — do not hardcode brand colors over interactive elements unless there's a strong product reason to override the user's system-wide choice (and if so, expose it as an app-level preference, not a hardcoded default).
- **Vibrancy** (`NSVisualEffectView` / `.background(.regularMaterial)` in SwiftUI): the pre-Liquid-Glass translucency mechanism, still relevant for Sonoma/Sequoia fallback (§1) and for content-adjacent panels that shouldn't take full Liquid Glass treatment. `NSVisualEffectView.Material` includes `.sidebar`, `.headerView`, `.menu`, `.popover`, `.hudWindow` — pick the semantic material matching the surface, not an arbitrary blur level.

---

## 13. App icon requirements (Icon Composer, macOS 26 era)

macOS Tahoe 26 introduces the **`.icon` format** (folder-based, replacing flat `.icns` for new submissions), authored via **Icon Composer** (bundled with Xcode 26 / available standalone from Apple Developer).

### Variants required

| Variant | Trigger |
|---------|---------|
| **Default (Light)** | Standard light appearance |
| **Dark** | Dark appearance |
| **Clear Light** | Light appearance, Liquid Glass "clear" tinted mode |
| **Clear Dark** | Dark appearance, Liquid Glass "clear" tinted mode |
| **Tinted Light** | User-selected monochrome tint, light |
| **Tinted Dark** | User-selected monochrome tint, dark |

- Icon Composer lets you compose foreground layers (crafted in any design tool) plus a background layer, apply effects/transparency, and define these variant appearances from one source; it exports the `.icon` bundle for Xcode.
- **Backward compatibility**: apps still supporting Sonoma/Sequoia deployment targets need a legacy flat icon set alongside the new `.icon` — community reports (2025-08) confirm separate-icon handling is required when straddling both OS eras; verify current Xcode 26.x behavior at build time rather than assuming automatic down-conversion `(unverified — confirm per Xcode 26.x point release, as backward-compat tooling has been actively evolving through the 26.x cycle)`.
- Continue exporting standard flat PNG sizes (16pt through 1024pt @1x/@2x) for any distribution path or tooling that doesn't yet consume `.icon` bundles.

→ Implementation: `reference/distribution.md` (packaging), `reference/macos-modern-stack.md` (Xcode 26 toolchain).

---

## 14. Anti-pattern: "iPad-app-shaped Mac app"

The most common Mac HIG failure is a Catalyst or SwiftUI-multiplatform app that never adapts past its iPad layout. Diagnose and correct:

| Anti-pattern | Symptom | Correction |
|--------------|---------|------------|
| No menu bar commands | All actions live only in toolbar buttons or in-view controls | Mirror every meaningful action into `Commands`/`CommandGroup` (§2) |
| Fixed/non-resizable window | Window can't tile, resize, or go full-screen usefully | Set sensible `.frame(minWidth:minHeight:)`, support full-screen (§3) |
| No hover states | Buttons/rows look identical whether pointer is over them or not | Add `.onHover`, reveal-on-hover row actions, cursor rects (§5) |
| Touch-sized everything | 44pt-minimum controls throughout, sparse padding | Adopt `.controlSize()` density appropriate to pointer input (§6) |
| No keyboard shortcuts / Tab traversal | Every action requires a click; Tab does nothing useful | Wire `.keyboardShortcut()`, verify Full Keyboard Access traversal (§6) |
| Bottom tab bar ported as-is | iOS `TabView` pattern used for app-level navigation | Convert to sidebar-first `NavigationSplitView` (§4) |
| No right-click context menus | Users can't get contextual actions without hunting a toolbar | Add `.contextMenu` to list rows, canvas objects, text selections (§5) |
| Single-window-only architecture | App can't open a second document/window | Support `WindowGroup` multi-instance + restoration (§3, `reference/scenes.md`) |
| No Dock menu / badge | App ignores Dock-level interaction entirely | Implement `applicationDockMenu(_:)`, wire badge to a single state source (§8) |
| iOS-style full-bleed opaque tab content mistaken for Liquid Glass chrome | Custom `.glassEffect()` slapped onto content/list rows | Restrict Liquid Glass to chrome only — sidebar/toolbar/menu bar (§1) |

This table is the practical checklist for the `hig` Recipe audit (`SKILL.md` Recipes table) — run it against any Catalyst-sourced or multiplatform-SwiftUI app before calling a Mac port "done." See `reference/catalyst-decision.md` for the deeper Catalyst-vs-native decision this anti-pattern usually stems from.

---

## Sources

- [Designing for macOS — Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/platforms/designing-for-macos) — Apple, accessed 2026-07
- [What's new in the updates for macOS Tahoe 26 — Apple Support](https://support.apple.com/en-us/122868) — accessed 2026-07
- [macOS 26 Tahoe review: Power under glass — Six Colors](https://sixcolors.com/post/2025/09/macos-26-tahoe-review-power-under-glass/) — 2025-09
- [macOS 26 Tahoe: The MacStories Review](https://www.macstories.net/stories/macos-26-tahoe-the-macstories-review/2/) — 2025-09
- [Updating application icons for macOS 26 Tahoe and Liquid Glass — Successful Software](https://successfulsoftware.net/2025/09/26/updating-application-icons-for-macos-26-tahoe-and-liquid-glass/) — 2025-09-26
- [Michael Tsai — Separate Icons for macOS Tahoe vs. Earlier](https://mjtsai.com/blog/2025/08/08/separate-icons-for-macos-tahoe-vs-earlier/) — 2025-08-08
- [Michael Tsai — macOS Tahoe's New Theming System](https://mjtsai.com/blog/2025/06/19/macos-tahoes-new-theming-system/) — 2025-06-19
- [Liquid Glass in SwiftUI: Official Best Practices for iOS 26 / macOS Tahoe — DEV Community](https://dev.to/diskcleankit/liquid-glass-in-swift-official-best-practices-for-ios-26-macos-tahoe-1coo) — accessed 2026-07
- Sibling reference: [`native/reference/ios-hig.md`](../../native/reference/ios-hig.md) — shared HIG foundations (color, typography, Dynamic Type, motion, privacy)

`#TODO(agent)`: re-fetch <https://developer.apple.com/design/human-interface-guidelines/platforms/designing-for-macos> directly (site required JS rendering / redirected during authoring) to validate section structure against Apple's canonical Mac HIG page.
