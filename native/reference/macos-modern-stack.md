# Modern macOS Stack Reference (2026)

**Purpose:** Current-as-of-2026 technology baseline for pure-native macOS apps (SwiftUI for macOS + AppKit interop).
**Read when:** Setting up a new Mac app, modernizing an existing one, or deciding on a macOS deployment target / API availability gate.
**Format model:** Structured like [`reference/modern-stack.md`](modern-stack.md) (read first for the iOS/Android baseline and shared Swift 6.3 concurrency model — not duplicated here). Scope here is macOS only.

> Out of scope: Mac Catalyst stack specifics (see `reference/catalyst-decision.md`), iOS/Android (see `reference/modern-stack.md`).

---

## 1. Swift 6.3 + Xcode 26 toolchain

- **Xcode 26.x** is the current major line; point releases through 2026 (26.3, 26.4, 26.6 as of 2026-07) ship incremental Swift 6.3 compiler updates, SDK updates (`macOS 26.x SDK`), and Instruments/tooling improvements — Xcode 26.4 (2026-03-24) shipped the largest Instruments update of the Xcode 26 cycle; Xcode 26.6 added Agent Client Protocol support and expanded Preview Snapshot MCP tooling.
- **Minimum macOS to run Xcode 26**: verify per point release — recent point releases (e.g., Xcode 26.6) require the matching Tahoe point release (`macOS Tahoe 26.2+` for Xcode 26.6) on the development machine itself; this is independent of your app's deployment target.
- **Swift 6.3** carries forward Swift 6.2's Approachable Concurrency model (default `MainActor` isolation for new targets, `@concurrent` for explicit background work) — see `reference/modern-stack.md` §Swift 6.2 Approachable Concurrency for the full mechanism; it applies identically on macOS targets.
- New macOS targets created in Xcode 26 get default `MainActor` isolation automatically; existing macOS targets opt in via `-default-isolation MainActor` build setting or `defaultIsolation(MainActor.self)` in `Package.swift`.

---

### Code example — default MainActor isolation opt-in for an existing target

```swift
// Package.swift — existing target opting into Swift 6.2/6.3 default MainActor isolation
let package = Package(
    name: "MyAppCore",
    targets: [
        .target(
            name: "MyAppCore",
            swiftSettings: [
                .defaultIsolation(MainActor.self),
                .enableUpcomingFeature("StrictConcurrency")
            ]
        )
    ]
)
```

For an Xcode project target (not SPM), set `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` in Build Settings rather than annotating every type — this matches the automatic default new Xcode 26 targets receive.

---

## 2. macOS version support matrix

| Baseline | Version | Released | What it unlocks |
|----------|---------|----------|-------------------|
| **Tahoe** | macOS 26 | 2025-09-15 | Liquid Glass chrome (sidebar/toolbar/menu bar/Dock), `.icon` format + Icon Composer, latest `.inspector()`/`Table`/`MenuBarExtra` refinements, Foundation Models framework, final macOS release supporting Intel Macs |
| **Sequoia** | macOS 15 | 2024-09 | `.inspector()` modifier (macOS 14+ carried forward), `SMAppService` (macOS 13+ carried forward), iPhone Mirroring, still receiving security updates in 2026 (15.7 as of 2025-09) |
| **Sonoma** | macOS 14 | 2023-09 | `.inspector()` modifier introduced, widgets on desktop, still receiving security updates in 2026 (14.8 as of 2025-09) |

### Typical minimum-deployment-target choice

- **New Mac app, no legacy constraint**: target **Sequoia 15** as the practical floor — captures `.inspector()`, `SMAppService`, and modern `NavigationSplitView` behavior while still reaching users who haven't upgraded to Tahoe yet. Gate Liquid Glass-specific chrome behind Tahoe availability checks only where you deliberately want a visually distinct pre-Tahoe fallback (most standard SwiftUI chrome adapts automatically on Xcode 26 recompile — see `reference/mac-hig.md` §1).
- **App requiring Liquid Glass / Foundation Models / `.icon` format as core features**: target **Tahoe 26** directly — do not attempt to backport these.
- **Broad-reach utility app / legacy AppKit codebase**: **Sonoma 14** floor is defensible if the team is not yet ready to drop it; confirm no Tahoe-only API is a hard requirement before committing to this floor.
- Since Xcode 14, the historical absolute floor for Xcode itself is macOS 10.13 High Sierra, but SwiftUI-forward apps in 2026 have no practical reason to target anything below Sonoma — verify against your actual API surface rather than assuming the Xcode-supported floor is a reasonable product floor.

---

## 3. SwiftUI-on-macOS API availability table

| Building block | API | Availability | Notes |
|-----------------|-----|:---:|-------|
| Window scene | `WindowGroup` | macOS 11+ | Baseline scene type |
| Preferences window | `Settings { }` scene | macOS 13+ | Wires ⌘, and App menu "Settings…" automatically |
| Menu-bar-only app | `MenuBarExtra` | macOS 13+ | `.window`/`.menu` styles; pair with `LSUIElement` |
| Document-based app | `DocumentGroup` + `FileDocument`/`ReferenceFileDocument` | macOS 13+ (`FileDocument`), macOS 13+ (`DocumentGroup` on Mac) | See `reference/documents.md` |
| Sidebar/detail/inspector 3-column | `NavigationSplitView` | macOS 13+ | Do not nest inside `NavigationStack` — same forbidden pattern as iOS (`reference/modern-stack.md`) |
| Detail/properties side panel | `.inspector(isPresented:)` | macOS 14+ | Independent of sidebar; see `reference/layout-patterns.md` |
| Tabular data | `Table` + `TableColumn` | macOS 12+ | Primarily Mac/iPad pattern |
| Toolbar | `.toolbar { ToolbarItem }` | macOS 11+ | Unified with title bar by default on modern `.windowStyle` |
| Drag & drop / cross-app transfer | `Transferable` + `.draggable`/`.dropDestination` | macOS 13+ | Declare `UTType`; see `reference/drag-drop-services.md` |
| Command menu customization | `Commands`/`CommandGroup`/`CommandMenu` | macOS 11+ | See `reference/menu-commands.md` |
| Liquid Glass material | `.glassEffect()` / `GlassEffectContainer` | macOS 26+ | Chrome only — see `reference/mac-hig.md` §1; standard components adopt it automatically on Xcode 26 recompile without code changes |
| Observation | `@Observable` macro | macOS 14+ | Same 2026-default guidance as iOS — see `reference/modern-stack.md` §Observation framework |
| Symbol effects | `.symbolEffect()` | macOS 14+ | Shared with iOS |
| Scene restoration | `SceneStorage` | macOS 11+ | Combine with `NSUserActivity` for deeper state — see `reference/scenes.md` |

`@available` gate pattern:

```swift
if #available(macOS 26, *) {
    // Tahoe-specific behavior — only where standard component auto-adoption isn't sufficient
} else {
    // Sequoia/Sonoma fallback — standard Material, not Liquid Glass
}
```

Prefer designing the component once and letting system rendering vary (per `reference/mac-hig.md` §1) over per-callsite `#available` branching — reserve explicit gates for genuinely Tahoe-only capabilities (Liquid Glass APIs, Foundation Models, `.icon` format tooling).

---

## 4. Persistence on Mac

### Code example — SwiftData model + Keychain-backed secret, sandbox-aware

```swift
import SwiftData

@Model
final class Project {
    @Attribute(.unique) var id: UUID
    var name: String
    var lastOpened: Date
    // Security-scoped bookmark data for a user-selected folder outside the app container.
    // Must be re-resolved (startAccessingSecurityScopedResource) on every launch — see
    // reference/sandbox-entitlements.md for the full bookmark lifecycle.
    var folderBookmark: Data?

    init(id: UUID = UUID(), name: String, lastOpened: Date = .now) {
        self.id = id
        self.name = name
        self.lastOpened = lastOpened
    }
}

// View
struct ProjectListView: View {
    @Query(sort: \Project.lastOpened, order: .reverse) private var projects: [Project]
    @Environment(\.modelContext) private var context

    var body: some View {
        Table(projects) {
            TableColumn("Name", value: \.name)
            TableColumn("Last Opened") { Text($0.lastOpened, style: .date) }
        }
    }
}
```

Keychain items in a sandboxed Mac app default to an app-specific access group; add the `keychain-access-groups` entitlement only when a helper tool or XPC service (see `reference/xpc-helpers.md`) needs to share the same keychain item — do not request broader keychain sharing than the actual helper-tool boundary requires.

| Mechanism | Use | Sandbox interaction |
|-----------|-----|----------------------|
| **SwiftData** (macOS 14+) | Default for new SwiftUI-centric apps — same 2026 production-ready guidance as iOS (`reference/modern-stack.md` §SwiftData vs Core Data) | Store lives in app container; CloudKit sync requires iCloud entitlement + container identifier |
| **Core Data** | Advanced migration, `NSFetchedResultsController`, large-scale/perf-sensitive data, or an existing Core Data store with custom mappings | Same sandbox container rules as SwiftData |
| **`UserDefaults` / `@AppStorage`** | Small scalar preferences | Sandboxed apps get an app-scoped defaults domain automatically — no extra entitlement |
| **File-based + iCloud Documents** | Document-based apps (`DocumentGroup`/`NSDocument`) | Requires `com.apple.security.app-sandbox` + iCloud Documents entitlement; user-selected file access needs security-scoped bookmarks (see `reference/sandbox-entitlements.md`) for locations outside the app's own container |
| **Keychain** | Credentials, tokens, secrets | `Keychain Sharing` entitlement required to share items across an app + helper/XPC target; sandboxed apps get an app-specific keychain access group by default — do not assume unscoped keychain access like a pre-sandbox Mac app |

**Sandbox interaction is the Mac-specific wrinkle absent on iOS**: every persistence choice above must be cross-checked against the App Sandbox entitlement baseline (`reference/sandbox-entitlements.md`) — a Mac app can silently lose file access across relaunch if security-scoped bookmarks aren't wired for non-container file locations, a failure mode iOS's sandbox model doesn't have in the same form (iOS apps rarely reference arbitrary user-selected files outside their own container/Photos/Files picker flows).

---

## 5. Networking + background work on Mac

| Need | Mechanism | Notes |
|------|-----------|-------|
| HTTP / API calls | `URLSession` + async/await | Identical API surface to iOS (`reference/modern-stack.md` §Library quick reference) |
| Periodic background work while app may not be frontmost | `NSBackgroundActivityScheduler` | Mac-only — no direct iOS equivalent (`BGTaskScheduler` is iOS-specific); coalesces with system power/thermal state, not a hard-scheduled timer |
| Work that must run even when the app itself isn't launched | Launch Agents / Launch Daemons via `SMAppService` (macOS 13+) | See `reference/xpc-helpers.md` for registration lifecycle — Native's `SKILL.md` Always list mandates `SMAppService` over legacy `SMJobBless`/manual `launchctl` |
| Privileged helper process | XPC service + `SMAppService` | See `reference/xpc-helpers.md` |

`NSBackgroundActivityScheduler` is the Mac-appropriate analog to iOS's `BGTaskScheduler` for "do periodic work when convenient" — the two are not API-compatible and should not be abstracted behind a shared cross-platform interface without an adapter layer.

---

## 6. Swift Concurrency posture

Shared with iOS — see `reference/modern-stack.md` §Swift 6.2 Approachable Concurrency for the full model (default `MainActor` isolation, `@concurrent` for explicit background work, caller-isolation inheritance). No Mac-specific concurrency divergence: the same `@Observable` + `@MainActor`-by-default + `@concurrent` pattern applies to macOS targets identically.

```swift
// macOS ViewModel — identical pattern to iOS
@Observable
final class DocumentListViewModel {  // implicit @MainActor (Xcode 26 new target default)
    private(set) var documents: [DocumentSummary] = []

    @concurrent
    private func loadFromDisk() async throws -> [DocumentSummary] {
        // off-main-actor work
    }

    func refresh() async throws {
        documents = try await loadFromDisk()
    }
}
```

Migration guidance for existing macOS targets (opt-in per target, raise `SWIFT_STRICT_CONCURRENCY` from `targeted` → `complete`) is identical to the iOS guidance — no separate Mac migration path exists.

---

## 7. Observability

| Tool | macOS availability | Notes |
|------|:---:|-------|
| `OSLog` | Available | Same API as iOS; use subsystem/category conventions matching your bundle ID |
| `os_signpost` | Available | Instruments-visible performance markers; same API as iOS |
| **MetricKit** | Available since **macOS 12** | Diagnostic + performance metric reports arrive via `MXMetricManagerSubscriber` — this availability *differs from what might be assumed*: MetricKit is not iOS-only, but Mac apps must actively subscribe (`MXMetricManager.shared.add(subscriber:)`) the same as iOS; verify report cadence and payload completeness on Mac specifically rather than assuming iOS parity, as the diagnostic report categories that fire depend on OS-level triggers that differ per platform `(partially unverified — MetricKit's base availability on macOS 12+ is confirmed; exact per-report-type parity with iOS in the 2026 SDK is not independently confirmed here)` |
| Accessibility Inspector | Available | Bundled with Xcode; see `reference/mac-hig.md` §11 |
| Instruments | Available | Largest update in the Xcode 26 cycle shipped with Xcode 26.4 (2026-03-24) |

---

## 8. Notable deprecations to avoid in new code

| Deprecated | Use instead |
|------------|--------------|
| `SMJobBless` | `SMAppService` (macOS 13+) — required by `SKILL.md` Always list |
| Manual `launchctl` install of LaunchAgents/LaunchDaemons | `SMAppService.agent`/`.daemon` registration |
| `NSDocument`-only apps for new SwiftUI-first projects | `DocumentGroup` + `FileDocument`/`ReferenceFileDocument` (drop to `NSDocument` only where SwiftUI's document model doesn't reach — see `reference/documents.md`) |
| `.icns`-only icon delivery for new Tahoe-targeted submissions | `.icon` format via Icon Composer (see `reference/mac-hig.md` §13), while retaining a legacy flat icon set for pre-Tahoe deployment targets |
| Legacy `ObservableObject` + `@Published` for new view models | `@Observable` macro (macOS 14+) |
| Ungated full-disk/broad file-system entitlements as a default | Security-scoped bookmarks + Powerbox-mediated pickers (see `reference/sandbox-entitlements.md`) |

---

## 9. Apple-silicon / universal-binary + Rosetta

- **Universal binary** (arm64 + x86_64) remains the standard build configuration for apps distributing outside a pure Apple-Silicon-only deployment story — Xcode's default "Universal" build setting covers this without extra configuration.
- **Tahoe 26 is the final macOS release supporting Intel Macs** — plan the Intel-support sunset explicitly: apps intending to support Sonoma/Sequoia/Tahoe across their full deployment window still need the Intel slice; apps targeting only Tahoe-and-later as their floor should evaluate whether Intel support is still worth the build/test matrix cost, since the next major release drops it.
- **Rosetta 2** translates x86_64 binaries on Apple Silicon automatically — relevant mainly for third-party dependencies/frameworks that haven't shipped arm64 builds; verify all SPM/XCFramework dependencies ship native arm64 slices before assuming Rosetta coverage is unnecessary.

---

## 10. On-device intelligence on Mac

- **Foundation Models framework**: available on **macOS 26+** (alongside iOS 26/iPadOS 26/visionOS 26) — gives direct Swift API access to the same on-device LLM powering Apple Intelligence, including multimodal prompts (image + text) and Vision-framework tool calling (OCR, barcode) from within a session.
- **Availability gating is a runtime check, not just an `@available` gate**: the model only runs on Apple-Intelligence-eligible hardware, with Apple Intelligence enabled, in supported regions — check model availability (`SystemLanguageModel.default.availability`) before creating a session, and design a graceful fallback path for ineligible devices/regions rather than gating the entire feature behind `#available(macOS 26, *)` alone.
- **Server-side scale-out**: for larger context windows or frontier reasoning beyond the on-device model's scope, the same `LanguageModelSession` API surface can drive a server-side model via the `ClaudeForFoundationModels` package referenced in `reference/modern-stack.md` §New surfaces on iOS 18 / iOS 26 — this applies identically to Mac targets using Foundation Models, since the framework and package are shared across iOS/iPadOS/macOS/visionOS 26.

---

## 11. Choose this stack when — summary table

| Situation | Stack choice |
|-----------|---------------|
| New Mac app, no legacy AppKit constraint | SwiftUI for macOS, Sequoia 15 floor, `@Observable`, SwiftData, `NavigationSplitView` + `.inspector()` |
| Mac app needs Liquid Glass / Foundation Models / `.icon` as core features | Same stack, Tahoe 26 floor, no pre-Tahoe fallback branching needed for these specific APIs |
| Legacy AppKit codebase, incremental modernization | AppKit retained where it already works, new features in SwiftUI via `NSHostingView`/`NSViewRepresentable` bridging — see `reference/appkit-interop.md` |
| Menu-bar-only utility app | `MenuBarExtra` + `LSUIElement`, Sequoia 15+ floor unless Tahoe-only chrome is required |
| Document-based app, iOS 17+/macOS 14+ shop already on SwiftData | `DocumentGroup` + `FileDocument`, SwiftData for any non-document app state |
| Privileged background work / login item | `SMAppService` (macOS 13+ floor mandatory — never `SMJobBless`) |
| Large-scale/perf-sensitive data model, or existing Core Data store with custom migrations | Core Data over SwiftData — same trade-off as iOS |
| Bringing an iPad app to Mac | Not this reference — see `reference/catalyst-decision.md` first |

---

## Sources

- [Apple's Foundation Models framework unlocks new intelligent app experiences — Apple Newsroom](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/) — 2025-09
- [Meet the Foundation Models framework — WWDC25 Session 286](https://developer.apple.com/videos/play/wwdc2025/286/) — Apple, 2025-06
- [Apple has released macOS 26 Tahoe, and Sequoia 15.7, Sonoma 14.8 — The Eclectic Light Company](https://eclecticlight.co/2025/09/15/apple-has-released-macos-26-tahoe-and-sequoia-15-7-sonoma-14-7-8/) — 2025-09-15
- [What macOS version can my Mac run? macOS 27 compatibility list — Macworld](https://www.macworld.com/article/673697/what-version-of-macos-can-my-mac-run.html) — accessed 2026-07
- [MetricKit — Apple Developer Documentation](https://developer.apple.com/documentation/MetricKit) — accessed 2026-07 (macOS 12+ base availability confirmed)
- [Xcode 26.6 RC 2 Release Notes — Apple Developer Documentation](https://developer.apple.com/go/?id=xcode-26_6-sdk-rn) — accessed 2026-07
- [Xcode 26.4 Features & Swift 6.3 Features — Medium](https://medium.com/@jagadeeshk0810/xcode-26-4-features-swift-6-3-features-a9a5d84261aa) — 2026-03
- Sibling reference: [`reference/modern-stack.md`](modern-stack.md) — shared Swift 6.3 concurrency model, `@Observable` pattern, SwiftData/Core Data trade-off (not duplicated here)

`#TODO(agent)`: independently confirm MetricKit report-type parity between macOS and iOS in the current SDK — flagged `(unverified)` above pending direct Apple documentation cross-check beyond base availability.


## macOS Reference Index (SKILL.md excerpt)

| File | Content |
|------|---------|
| `reference/scenes.md` | `macos` — WindowGroup / Settings / MenuBarExtra / DocumentGroup, multi-window, restoration |
| `reference/mac-hig.md` | Mac HIG — menu bar structure, pointer/hover, keyboard shortcuts, window chrome |
| `reference/menu-commands.md` | Commands / CommandGroup / CommandMenu, menu structure, ⌘-shortcut conventions |
| `reference/appkit-interop.md` | NSViewRepresentable / NSHostingView bridging and AppKit coexistence |
| `reference/documents.md` | Document apps — DocumentGroup, FileDocument, NSDocument, UTType export |
| `reference/layout-patterns.md` | NavigationSplitView sidebar/detail, toolbar groups, `.inspector()` |
| `reference/drag-drop-services.md` | Transferable / `.draggable` / NSPasteboard negotiation, Services menu |
| `reference/sandbox-entitlements.md` | `macdist` — App Sandbox scoping, security-scoped bookmarks, Powerbox pickers |
| `reference/distribution.md` | App Store vs Developer ID, notarytool submit/staple, hardened runtime, Sparkle, DMG/pkg |
| `reference/catalyst-decision.md` | Mac Catalyst vs native AppKit/SwiftUI decision framework |
| `reference/xpc-helpers.md` | XPC privilege separation, SMAppService LaunchAgent/Daemon/login-item registration |
| `reference/macos-xcrun-cli.md` | macOS build/sign/notarize CLI — xcodebuild, codesign, notarytool, spctl, stapler |
| `reference/macos-handoffs.md` | macOS-specific handoff templates |

