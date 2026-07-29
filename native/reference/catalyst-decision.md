# Mac Catalyst vs Native Decision

> Decision framework for bringing an existing app to Mac: Mac Catalyst, native SwiftUI/AppKit, or a shared-core two-target architecture.
> Last validated against secondary sources: 2026-07.

## When this reference applies

An **iPad app is the source** and the destination is a Mac app — the Core Contract "distribution channel decided before scaffolding" already assumes a Mac target exists; this file resolves the earlier question of *how the Mac target gets built*. If there is no existing iPad/iOS codebase (Mac-first, greenfield), skip straight to `reference/scenes.md` — native SwiftUI is the only sane starting point (§7 explains why Catalyst is never the default for a Mac-first app).

---

## 1. Decision framework

Work through these axes in order — each can independently rule Catalyst out.

### 1.1 Existing codebase state

| Codebase state | Signal |
|-----------------|--------|
| UIKit-heavy, mature iPad app, want Mac fast | Catalyst is viable — start here |
| SwiftUI-only iPad app already | SwiftUI multiplatform single-target (§5) is usually a better fit than Catalyst |
| No existing app / greenfield | Native SwiftUI for macOS, full stop — Catalyst has nothing to port |
| Heavy AppKit-only requirements anticipated (custom `NSToolbar` behavior, deep menu bar, XPC helpers) | Native AppKit/SwiftUI or shared-core (§6) — Catalyst cannot reach these |

### 1.2 Target fidelity

| Target fidelity | Best fit |
|-------------------|----------|
| "Runs on Mac, functionally complete" (utility/companion app) | Catalyst, iPad idiom (§3) |
| "Feels like a Mac app" (menu bar depth, pointer idioms, dense toolbars) | Catalyst, Mac idiom (§3) with real investment, or native |
| "Indistinguishable from a Mac-first app" (power-user tool, pro app) | Native SwiftUI/AppKit or shared-core (§6) |

### 1.3 Team size and feature surface

| Team size | Feature surface | Recommendation |
|-----------|------------------|-----------------|
| Small team, small feature surface, tight timeline | Catalyst, iPad idiom — fastest path to "it exists on Mac" |
| Small-to-mid team, willing to invest in Mac-specific polish over time | Shared-core two-target (§6) — front-loads a bit more setup, pays off as Mac-specific work grows |
| Mid-to-large team, Mac is a first-class platform for the product | Native SwiftUI/AppKit from the start, or shared-core if iOS/Mac logic genuinely overlaps |

### 1.4 Feature surface specifics

If **any** of the following are required, Catalyst is disqualified regardless of team size — jump to native or shared-core:

- Menu-bar-only utility app (`MenuBarExtra`, `LSUIElement`)
- XPC helper tools / `SMAppService` privileged services
- Deep `NSToolbar`/`NSToolbarItem` customization beyond what SwiftUI `.toolbar` exposes
- Document-based app with `NSDocument`-level control (versions, custom autosave timing)
- Services menu (`NSServices`) provider implementation
- Advanced `NSPasteboard` type negotiation beyond `Transferable`
- Custom window chrome (`NSWindowStyleMask` beyond title-bar toggling)

---

## 2. Effort / fidelity trade-off

| Approach | Setup effort | Mac-native fidelity ceiling | Ongoing maintenance | When it pays off |
|----------|:---:|:---:|:---:|-------------------|
| **Catalyst, iPad idiom** | Lowest — checkbox in target settings | Low — scaled iPad UI, iPad-shaped interactions | Low, but fidelity never improves without idiom switch | Fast Mac availability for a companion/utility app; Mac is not a primary platform |
| **Catalyst, Mac idiom ("Optimize for Mac")** | Medium — per-screen layout adjustments, `#if targetEnvironment(macCatalyst)` branches | Medium — sharper rendering, some Mac-like controls, but menu bar/window/pointer depth still capped (§4) | Medium, grows as more `#if macCatalyst` branches accumulate | Mac is a secondary but real platform; team wants to avoid a second codebase |
| **SwiftUI multiplatform single-target (`#if os(macOS)`)** | Medium — same target, conditional compilation for divergent UI | Medium-high for SwiftUI-expressible surface; still capped for AppKit-only needs | Medium — conditional branches sprawl as platforms diverge further | SwiftUI-only codebase already; platforms stay close in feature set |
| **Shared-core, per-platform UI targets** | Highest — separate UI target, module boundary discipline upfront | High — full native SwiftUI/AppKit on Mac, full native SwiftUI/UIKit on iOS | Lowest long-term — platform UI code never fights the other platform's constraints | Mac is (or is becoming) a first-class platform; team can afford the upfront split |
| **Native AppKit/SwiftUI, Mac-only target** | Highest for teams without an existing shared core; N/A if Mac-first greenfield | Highest — no ceiling | Lowest for Mac-specific work; highest if logic must be kept in sync with iOS by hand | Mac-first app, or Mac fidelity requirements exceed what any shared-core UI layer could express anyway |

---

## 3. "Optimize for Mac" vs "Scaled to Match iPad"

Both are Catalyst build-time idiom settings (Xcode target → Deployment Info → Mac Catalyst).

### Scaled to Match iPad (default when Catalyst is first enabled)

- iOS views and text render at their iPad size, then the system scales the whole interface down (~77%) to match macOS density.
- Minimal layout work — most iPad-idiom UIKit/SwiftUI code works unmodified.
- Consequence: text and controls read as slightly soft/blurry (scaled raster/vector at non-1:1), and interactions still feel iPad-shaped (touch-sized targets, no hover states, no menu bar depth beyond auto-generated items).
- Right choice when: fast Mac availability matters more than Mac-native feel, or the app is a companion/utility tool where users don't expect deep Mac idioms.

### Optimize Interface for Mac ("Mac idiom")

- Views render at 100% scale — text and graphics appear sharp, matching native Mac rendering.
- Unlocks Mac-only visuals/controls not available under the iPad idiom.
- Requires per-screen work: touch-sized targets need `.controlSize()` review, layouts need `#if targetEnvironment(macCatalyst)` branches for hover states and denser spacing, and testing on real window-resize/tiling behavior.
- Trade-off is explicit: a build-setting change takes effect at launch, but the code investment to make full use of it accumulates screen by screen — Apple does not retroactively add Mac idioms to iPad-shaped layout code.
- Known 2026-era gap: even in Mac idiom, some system pickers (e.g., `PHPickerViewController`) have reported unusable behavior specifically when the Catalyst app is configured for the Mac idiom on macOS 26 `(unverified — confirm against current Xcode 26.x point release; this was an open forum report, not confirmed-fixed)`. Treat any Catalyst-wrapped system picker as a fidelity risk to test explicitly, not an assumption.

### Consequences summary

| Idiom | Rendering | Effort | Fidelity |
|-------|-----------|--------|----------|
| Scaled to Match iPad | Scaled down (~77%), softer | Near-zero | iPad-shaped Mac app (§14 anti-pattern in `mac-hig.md`) |
| Optimize for Mac | 1:1, sharp | Per-screen, ongoing | Improved, but still capped below native (§4) |

---

## 4. What Catalyst gives free vs what it never gets right

### Free (system-provided, no code required)

- App runs on Mac at all — process model, window creation, basic lifecycle.
- Standard UIKit/SwiftUI controls translate to roughly-equivalent AppKit-backed rendering.
- Basic menu bar is auto-generated from standard iOS navigation/toolbar items (Edit menu gets Cut/Copy/Paste automatically, for example).
- Sandbox entitlement and code-signing pipeline is the same as any Mac target — no separate signing setup.
- Automatic support for window resizing, full-screen, and basic multi-window (each scene becomes a Mac window).

### Never gets right (even with Mac idiom + heavy `#if macCatalyst` investment)

| Capability | Why Catalyst caps out |
|------------|------------------------|
| **Menu bar depth** | Auto-generated menu items only cover standard iOS actions; deep custom `Commands`/`CommandGroup` structure (see `reference/mac-hig.md` §2) requires manual `UIMenuBuilder` work that never matches SwiftUI-native `Commands` ergonomics or completeness |
| **Window management** | No native access to `NSWindow`-level behavior (custom title bar styles, `NSWindowStyleMask` combinations, per-window toolbar customization beyond UIKit's `UITitlebar` bridging) |
| **Pointer idioms** | Hover states, cursor rects, and reveal-on-hover patterns (`reference/mac-hig.md` §5) require UIKit's limited `UIHoverGestureRecognizer`/`UIPointerInteraction` bridging — workable but consistently behind native `NSTrackingArea`/SwiftUI `.onHover` fidelity |
| **Sidebar/toolbar fidelity** | `UISplitViewController`-backed sidebars approximate but don't fully match `NavigationSplitView` + native `NSToolbar` unification, especially for Liquid Glass chrome adoption on Tahoe 26 |
| **Drag & drop** | UIKit drag-and-drop APIs bridge to macOS but miss `NSPasteboard` type negotiation depth and `NSDraggingSource`/`NSDraggingDestination` edge cases (see `reference/drag-drop-services.md`) |
| **Printing** | UIKit's `UIPrintInteractionController` bridges to macOS printing but lacks `NSPrintOperation`/`NSPrintPanel` customization depth for complex print layouts |
| **AppKit-only APIs** | XPC helper tools, `SMAppService`, `NSServices` Services menu provider, `NSPasteboard` custom type negotiation, `applicationDockMenu(_:)` — none of these have a Catalyst path; they require dropping to AppKit directly, which partially defeats the point of choosing Catalyst |

**Rule of thumb**: if the feature list includes even one item from the "never gets right" table as a hard requirement (not a nice-to-have), Catalyst should be ruled out at the DETECT phase rather than discovered mid-implementation.

---

## 5. SwiftUI multiplatform single-target (`#if os(macOS)`)

A third option, distinct from Catalyst: one SwiftUI target compiled for both iOS and macOS SDKs, with platform divergence handled via `#if os(macOS)` / `#if os(iOS)` conditional compilation inside shared SwiftUI views.

```swift
struct ContentView: View {
    var body: some View {
        NavigationSplitView {
            SidebarView()
        } detail: {
            DetailView()
        }
        #if os(macOS)
        .toolbar { ToolbarItem { macOnlyToolbarButton } }
        .frame(minWidth: 800, minHeight: 500)
        #else
        .toolbar { ToolbarItem(placement: .navigationBarTrailing) { iosOnlyButton } }
        #endif
    }
}
```

### Where this is the right call

- Codebase is already SwiftUI-only (no legacy UIKit to carry forward) — Catalyst's main value proposition (bridging UIKit) doesn't apply.
- iOS and Mac feature sets are close enough that most view code is genuinely shared, with divergence isolated to layout/chrome details.
- Team wants a single Xcode project/target, not a module split.

### Where it breaks down

- **Divergence grows past chrome-level differences.** Once Mac-specific features accumulate (menu bar `Commands`, `MenuBarExtra`, XPC, document model differences), `#if os(macOS)` blocks sprawl through shared files, and the "single target" advantage becomes a maintenance liability — every shared view risks unintended cross-platform coupling.
- **Business logic and UI aren't already separated.** If view code and domain logic are tangled, conditional compilation multiplies inside the same files that also need platform-specific data flow (e.g., document handling: `DocumentGroup` shape differs meaningfully between iOS and macOS document lifecycles).
- **Signal to move to shared-core (§6)**: when `#if os(macOS)` appears in more than roughly a third of your view files, or when any single view's platform branches exceed ~30% of its body — that is the point to extract a per-platform UI target instead of continuing to conditionally compile one target.

---

## 6. Shared-core architecture (recommended default for serious multiplatform)

The pattern that scales past both Catalyst's ceiling and single-target `#if os()` sprawl: a **platform-agnostic core package** plus **fully native per-platform UI targets**.

### Concrete module layout

```
MyApp/
├── Packages/
│   └── MyAppCore/                    # Swift Package, no UIKit/AppKit/SwiftUI import
│       ├── Sources/
│       │   ├── Models/               # Domain models, Codable types
│       │   ├── Networking/           # URLSession-based API client
│       │   ├── Persistence/          # SwiftData/Core Data models + repositories
│       │   └── UseCases/             # Business logic, platform-agnostic
│       └── Tests/
├── MyApp-iOS/                        # iOS app target
│   ├── Views/                        # SwiftUI, iOS-specific (TabView, NavigationStack)
│   └── App.swift                     # imports MyAppCore
├── MyApp-macOS/                      # macOS app target (Native macos recipe domain)
│   ├── Views/                        # SwiftUI for macOS + AppKit interop where needed
│   ├── Commands/                     # Commands/CommandGroup menu bar structure
│   └── App.swift                     # imports MyAppCore
└── MyApp.xcworkspace                 # ties packages + both app targets together
```

- **`MyAppCore` has zero UI framework imports.** This is the enforceable boundary — if a file in Core imports `SwiftUI`, `UIKit`, or `AppKit`, it belongs in a UI target instead. This constraint is what prevents the `#if os()` sprawl described in §5.
- **Per-platform UI targets are fully native** — `MyApp-macOS` uses `NavigationSplitView`, `Commands`, `MenuBarExtra`, AppKit interop as needed (Native's full macOS scope per `SKILL.md`), with no obligation to resemble the iOS UI structurally.
- **Shared ViewModels are the usual seam**: `@Observable` model types can live in Core if they only depend on Core types, or in a thin per-platform wrapper if they need `NSPasteboard`/`UIPasteboard`-style platform APIs — keep that wrapper layer intentionally thin.

### Effort trade-off

Higher upfront cost than Catalyst (must set up the package boundary, decide what's shared vs not) but the ceiling is native fidelity on both platforms indefinitely — no idiom setting, no scaling artifact, no capped feature set.

---

## 7. "Optimize for Mac" is not a substitute for native — and neither is Catalyst as a default

Per `SKILL.md` Never list: **treat Mac Catalyst as the default path for a Mac-first app is prohibited.** Catalyst exists specifically for porting an *existing iPad app* to Mac with acceptable-not-ideal fidelity and controlled effort. If there is no iPad app to port — greenfield Mac work, or a Mac-first product — start native (§SKILL.md SwiftUI App Scaffold Recipe) or shared-core (§6) if a companion iOS app is also planned from day one. Reaching for Catalyst on a Mac-first app produces exactly the "iPad-app-shaped Mac app" anti-pattern documented in `reference/mac-hig.md` §14.

---

## 8. Migration paths

### Catalyst → shared-core / native (most common direction)

Signals this migration is due (see §9 for the full checklist): Mac-specific feature requests keep hitting Catalyst's ceiling (§4), or `#if targetEnvironment(macCatalyst)` branches have grown as unwieldy as the `#if os(macOS)` sprawl warning in §5.

1. Extract business logic/models into a Core package first (this is valuable regardless of the Catalyst decision, and de-risks the later UI split).
2. Stand up a native `MyApp-macOS` target alongside the existing Catalyst target — do not delete Catalyst until the native target reaches feature parity.
3. Rebuild UI screen-by-screen in the native target, prioritizing the screens hitting Catalyst's ceiling hardest (menu bar structure, document handling, sidebar/toolbar).
4. Cut over distribution to the native target once parity is confirmed; retire the Catalyst target.

### Shared-core / native → Catalyst (rare, but happens)

Occurs when a team over-invested in native Mac fidelity for a low-priority secondary platform and needs to cut maintenance cost. Generally only sensible if the native Mac UI is thin enough that reverting to scaled/optimized Catalyst rendering is an acceptable fidelity regression — evaluate against §2's trade-off table before committing; this direction should be rare enough to treat as an Ask First scenario, not a default response to "Mac maintenance is expensive."

### SwiftUI multiplatform single-target → shared-core

The lower-friction migration: extract the parts of the single target that are pure logic into a Core package first, then split the View layer into per-platform targets once `#if os(macOS)` density crosses the §5 threshold. Because the code was already SwiftUI throughout, this migration keeps most View code — it mainly relocates and removes conditional branches by giving each platform its own file instead of a shared file with branches.

---

## 9. Signals: you have outgrown Catalyst

Any of the following, independently, justifies moving off Catalyst (§8):

| Signal | Why it matters |
|--------|-----------------|
| A requested feature is in the §4 "never gets right" table and is not optional | Catalyst has no path forward without dropping to AppKit anyway — at that point, evaluate whether the AppKit work should live in a native target instead |
| `#if targetEnvironment(macCatalyst)` branches exceed roughly a third of a screen's view code | Diminishing returns — you're paying native-level implementation cost without native-level ergonomics or fidelity ceiling |
| Users/reviewers describe the Mac app as "clearly a ported iPad app" | Direct signal that Mac idiom investment (§3) hasn't closed the fidelity gap, and may not be able to |
| Menu bar structure requests keep exceeding what auto-generated + `UIMenuBuilder` items can express | See §4 Menu bar depth row |
| Team is committing meaningful ongoing engineering time to Mac as a platform | At that point the upfront cost of shared-core (§6) is justified by the platform's priority, not just its current feature count |
| A document-based, XPC-dependent, or menu-bar-only-utility feature is core to the product (not a stretch goal) | These are structurally incompatible with Catalyst (§1.4) — no amount of Catalyst investment reaches them |

---

## 10. Cross-references for boundary clarity

- **`port/`** — owns the *web*→native porting strategy and blueprint (feature parity matrices, BFF redesign, Strangler-Fig phased migration). This file is scoped to *iPad-app*→Mac (Catalyst vs native), a narrower and structurally different decision — Port's parity-matrix methodology is a useful reference pattern if the Mac Catalyst decision is happening as part of a larger web-to-native program, but Port does not own the Catalyst-specific idiom/API trade-offs documented here.
- **iOS/Android scope** — the same Native skill owns iOS/Android pure-native implementation, including the source iPad app that this file assumes as input. `reference/ios-hig.md` and `reference/modern-stack.md` describe the iPad-side baseline being ported from; this file describes only the Mac-side destination decision.
- **Native (`macos` recipe) owns**: everything after the Catalyst-vs-native decision is made — the actual native macOS implementation (`reference/scenes.md`, `reference/menu-commands.md`, `reference/layout-patterns.md`, etc.) and the shared-core `MyApp-macOS` UI target in §6's module layout.

---

## Sources

- [Introduction — Mac Catalyst — Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/technologies/mac-catalyst/introduction) — Apple, accessed 2026-07
- [Optimize the interface of your Mac Catalyst app — WWDC20 Session 10056](https://developer.apple.com/videos/play/wwdc2020/10056/) — Apple, 2020 (idiom mechanics unchanged as of 2026-07 per current HIG page)
- [Specify the UI idiom for your Mac Catalyst app — Microsoft Learn (.NET MAUI)](https://learn.microsoft.com/da-dk/dotnet/maui/mac-catalyst/user-interface-idiom?view=net-maui-8.0) — cross-referenced for idiom scaling percentage, accessed 2026-07
- [PHPickerViewController unusable via Mac Catalyst on macOS 26 when interface is "Scaled to Match iPad" — Apple Developer Forums](https://developer.apple.com/forums/thread/803019) — accessed 2026-07, `(unverified fix status)`
- [Supporting Catalyst's Optimize for Mac with Manual Layout](https://www.highcaffeinecontent.com/blog/20210516-Supporting-Catalysts-Optimize-for-Mac-with-Manual-Layout) — background on manual layout effort under Mac idiom, accessed 2026-07
- Sibling references: [`reference/mac-hig.md`](mac-hig.md) §14 (iPad-app-shaped Mac app anti-pattern), [`reference/macos-modern-stack.md`](macos-modern-stack.md) (current toolchain baseline this decision assumes)
