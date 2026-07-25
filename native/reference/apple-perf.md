# Apple Platform Performance Reference (2026)

Agent-specific slice for **Native** — measurement and optimization for iOS/iPadOS/macOS Swift + SwiftUI apps. Baseline assumes Swift 6.3 / Xcode 26 (as of 2026-07).

This file does **not** duplicate `reference/xcrun-cli.md` §3 (`xctrace` CLI mechanics) or `bolt/reference/swift-cheatsheet.md` (ARC/COW/generic-specialization level Swift perf). Read it alongside:

- [`reference/xcrun-cli.md`](xcrun-cli.md) §3 — `xctrace` CLI invocations, `--launch` vs `--attach`, export/parse
- [`bolt/reference/swift-cheatsheet.md`](../../bolt/reference/swift-cheatsheet.md) — language-level Swift perf (ARC, COW, `@inlinable`, autoreleasepool)
- [`reference/modern-stack.md`](modern-stack.md) — `@Observable`, Swift 6.2/6.3 Approachable Concurrency, SwiftData baseline facts

The role of this reference: **what to measure before touching code, which SwiftUI/launch/memory/concurrency patterns cause the regressions Native ships, and how to wire perf budgets into field telemetry and CI.**

---

## 1. Measurement-first discipline

**Never optimize without a captured baseline.** Capture a trace on the target device class (not the simulator, not the newest device in the drawer) before and after any change; a "faster" diff with no before/after trace is not a verified fix.

### 1.1 Decision table — which Instrument answers which question

| Question | Instrument / template | Notes |
|----------|----------------------|-------|
| "Why did this view re-render / what's driving `body`?" | **SwiftUI** template (Instruments 26+) | Lanes: View Body, View Properties, Core Animation Commits, Time Profiler — shows exact view + update reason per frame |
| "Where is wall-clock CPU going?" | **Time Profiler** | Sample at 1ms; symbolicate against a dSYM that matches the binary UUID |
| "Where are allocations happening / growing?" | **Allocations** | Mark Generation to isolate one user action's delta |
| "Did anything leak?" | **Leaks** | Pair with Memory Graph Debugger in Xcode for retain-cycle traversal |
| "Did a frame miss its deadline?" | **Animation Hitches** | Reports hitch time ratio per interval; correlates with the render loop stages |
| "Is app launch slow, and in which phase?" | **App Launch** | Splits pre-main / post-main and marks `UIApplicationMain` / first-frame |
| "Is the raw frame rate or GPU-bound?" | **Core Animation** (FPS track) | Confirms whether a hitch is CPU-render-side or GPU-composite-side |
| "Is a network call the actual bottleneck?" | **Network** | `URLSession` `taskMetrics` overlay — DNS / TLS / TTFB / body transfer split |
| "Is the main thread blocked >250ms?" | **Hangs** | Distinct from Time Profiler — flags user-visible unresponsiveness specifically |
| "Is an actor/Task the bottleneck?" | **Swift Concurrency** template | Task lifetimes, actor hop visualization, priority inversions |

**Rule**: profile on-device → hypothesize → change one variable → re-profile. Trust the trace over intuition — SwiftUI's diffing and Swift's ARC make manual reasoning about "what re-renders" unreliable past trivial view trees.

### 1.2 CLI capture

Cross-reference `reference/xcrun-cli.md` §3 for full `xctrace` mechanics (`--launch` vs `--attach`, `export --xpath`). Quick pointers specific to the templates above:

```bash
# App launch trace (fresh process, not attach)
xcrun xctrace record --template 'App Launch' --launch -- /path/App.app/App

# Animation Hitches during a scripted UI test run
xcrun xctrace record --template 'Animation Hitches' --device <UDID> --attach <pid> --time-limit 30s

# SwiftUI instrument (Instruments 26+) — confirm exact template string locally,
# `xcrun xctrace list templates` naming has shifted across Instruments versions (unverified exact string for your installed version)
xcrun xctrace record --template 'SwiftUI' --launch -- /path/App.app/App
```

`xcrun xctrace list templates` is the source of truth for exact strings on the active Xcode install — template names have changed release to release (e.g. some Instruments versions list `SwiftUI System Trace` rather than `SwiftUI`); do not hardcode a string into CI without verifying it against the CI runner's Xcode.

---

## 2. SwiftUI render performance

### 2.1 Identity: structural vs explicit

SwiftUI diffs by **structural identity** (view type + position in the view tree) unless you supply **explicit identity** via `.id(_:)`. Two failure modes:

| Failure | Symptom | Fix |
|---------|---------|-----|
| Missing explicit identity in a `ForEach` (index-based) | Diff falls back to positional matching; row state (e.g. `@State` inside a row) leaks onto the wrong item after insert/delete | `ForEach(items, id: \.stableID)` — never `id: \.self` on a mutable struct, never the array index |
| `.id()` applied too broadly (e.g. on a container whenever any child's derived value changes) | SwiftUI treats the entire subtree as a **new** view — full re-init, animations don't interpolate, `@State` resets | Scope `.id()` to the smallest node that actually needs identity reset; prefer `.animation(value:)`/`onChange` over forcing identity churn |

### 2.2 `@Observable` vs `ObservableObject` granularity

`@Observable` (Swift 5.9+ / iOS 17+) tracks **per-property** access inside `body` — only properties actually read trigger invalidation. `ObservableObject` + `@Published` invalidates on **any** published-property change regardless of whether `body` reads it.

```swift
@Observable @MainActor
final class FeedModel {
    private(set) var posts: [Post] = []
    private(set) var isRefreshing = false   // reading only `posts` in a child view
}                                            // means `isRefreshing` changes do NOT re-run that child's body
```

Practical implication: splitting one large `@Observable` model into narrower ones is usually unnecessary — the granularity is already per-property. The real risk is a view reading *more* of the model than it renders (e.g. destructuring the whole struct into local `let`s at the top of `body`), which re-couples it to every field.

### 2.3 `EquatableView` / `.equatable()`

For a leaf view whose `body` is expensive to compute relative to an equality check, wrap it so SwiftUI can skip `body` entirely on unchanged input:

```swift
struct ChartView: View, Equatable {
    let dataPoints: [Double]
    static func == (l: Self, r: Self) -> Bool { l.dataPoints == r.dataPoints }
    var body: some View { /* expensive chart draw */ }
}
// call site
ChartView(dataPoints: points).equatable()
```

Use when: `body` cost clearly exceeds the `==` cost, and the view is called from a parent that re-renders more often than the view's actual inputs change (common in list rows re-rendering because a sibling column changed). Verify the win with the SwiftUI Instrument's View Body lane before and after — `Equatable` conformance with a naive `==` can itself become the bottleneck on large arrays.

### 2.4 `LazyVStack` / `List` diffing cost

- `List` performs identity-based diffing on every data change; large heterogeneous lists with unstable `id` values pay an `O(n)` or worse re-diff every update.
- `LazyVStack` defers view creation until scroll-visible, but each newly-visible row still pays full `body` evaluation cost — a heavy row `body` (e.g. inline image decode, date formatting without a cached formatter) turns into scroll hitches, not launch cost.
- Prefer flattening deeply nested `List { Section { ForEach { ... } } }` hierarchies when the SwiftUI Instrument shows View Body time concentrated in container views rather than leaf rows.

### 2.5 Avoiding `AnyView`

`AnyView` erases the concrete view type, defeating SwiftUI's compile-time view-tree diffing — every `AnyView`-wrapped subtree is treated as opaque and re-diffed structurally rather than skipped. Prefer `@ViewBuilder` conditional returns or `Group` for branching content:

```swift
// Anti-pattern
var body: some View {
    if condition { AnyView(ViewA()) } else { AnyView(ViewB()) }
}

// Preferred — compiler synthesizes a matching opaque type per branch
@ViewBuilder
var body: some View {
    if condition { ViewA() } else { ViewB() }
}
```

### 2.6 `onChange` vs `task(id:)`

| Modifier | Semantics | Use when |
|----------|-----------|----------|
| `.onChange(of:)` | Fires a synchronous closure on value change; you manage any async work yourself (cancellation is manual) | Simple side effects, no async work, or work that must not be cancelled mid-flight |
| `.task(id:)` | Cancels the previous `Task` automatically when `id` changes, then starts a new structured `Task` | Any async fetch keyed on a changing value (search-as-you-type, detail-pane reload on selection change) — avoids the classic "old response overwrites new" race |

### 2.7 Detecting expensive `body` recomputation

```swift
var body: some View {
    let _ = Self._printChanges()   // debug-only; strip before shipping
    // ...
}
```

`Self._printChanges()` prints which stored property triggered the most recent `body` call — the fastest way to confirm a hypothesis ("is this view re-rendering because of `isLoading`, or because of the whole `posts` array?") without opening Instruments. Confirm the finding with the SwiftUI Instrument's View Body lane, since `_printChanges()` is best-effort and undocumented as a stable API (Apple: debug-only, not for shipping code).

### 2.8 `@State` placement and closure-driven view-graph thrash

- Declare `@State private var model = Model()` **once, at the owning view** — a child view that re-declares the same model with `@State` re-initializes it every time the child is recreated (see `reference/patterns.md` for the `@Observable` ownership rule Native enforces).
- Unstable closures passed as view parameters (e.g. a freshly-allocated `{ viewModel.doThing() }` built inline in a parent's `body`) can appear as "changed" input to a child even when semantically identical, because closures are not `Equatable` by identity in the general case — this defeats `EquatableView` and can trigger re-diffing of an otherwise-stable subtree. Prefer stored closures/methods (`viewModel.doThing`) over inline closures rebuilt every `body` pass when the child is perf-sensitive.

---

## 3. Launch time

### 3.1 Pre-main vs post-main

- **Pre-main**: everything from process exec to your `main()`/`@main` entry — dylib loading, rebase/binding, ObjC class registration, static initializers. Measure with `DYLD_PRINT_STATISTICS=1` (add as an env var in the Xcode scheme, or `export DYLD_PRINT_STATISTICS=1` for a CLI launch) — output breaks down dylib loading time, rebase/bind time, ObjC setup time, and the slowest initializers.
- **Post-main**: everything you control — `AppDelegate`/`App.init`, first-screen setup, initial network/DB work before first frame. This is normally the larger, more tractable share of launch time.
- Apple's longstanding public guidance: keep total launch (pre-main + post-main to first frame) under ~400ms where possible; the hard OS-enforced ceiling before the system kills an unresponsive launch is on the order of 20s (`(unverified)` exact current OS value — has shifted across OS versions, treat as an outer bound not a target).

### 3.2 dyld 4 improvements

dyld4 (current architecture since iOS 15/Xcode 13-era, still current in Xcode 26) replaced the closure-caching model with memory-mapped `PrebuiltLoader` objects shareable across processes, consolidating loader logic into the dyld shared cache itself rather than splitting between kernel-loaded dyld and userspace `libdyld.dylib`. Practical effect for Native: launch-time dylib-loading cost is dominated by **how many distinct dynamic frameworks** you link, not by dyld internals you can tune — the lever is framework count and static-vs-dynamic choice (§3.3), not dyld flags.

### 3.3 Static vs dynamic framework cost

| Choice | Load cost | Binary size | When |
|--------|-----------|-------------|------|
| Dynamic framework | Extra `dlopen` + rebase/bind per framework at every cold launch (~tens of ms each, additive) | Smaller per-binary, shared across app extensions | Framework is genuinely shared across an app + multiple extensions/widgets |
| Static framework / static lib | Zero extra load step — linked into the single Mach-O | Larger single binary | Framework is used by the main app target only |

Audit with `xcrun size -m App.app/App` and count linked dynamic frameworks via `xcrun otool -L App.app/App` — every first-party framework used only by the main target is a static-linking candidate.

### 3.4 Deferring work off the critical path

- Anything not needed for the first rendered frame (analytics SDK init, non-critical prefetch, background sync setup) belongs after `sceneDidBecomeActive` / first `onAppear`, not in `App.init` or `AppDelegate.didFinishLaunching`.
- Defer via `Task.detached(priority: .background)` or `.task { }` on the first screen, not synchronous work in `init`.
- SwiftData/Core Data container setup is a common hidden launch cost — open the store off the main actor when the schema doesn't gate first-frame content.

### 3.5 MetricKit `MXAppLaunchMetric` + Organizer

`MXAppLaunchMetric` reports device-launch-time histograms aggregated from real user devices (`MXMetricPayload.applicationLaunchMetrics`) — this is the only source of true field launch-time data; Instruments only ever profiles the device under your hand. Cross-check `MXAppLaunchMetric` percentiles against Xcode Organizer's **Launch Time** report (App Store Connect-sourced, all users, no MetricKit integration required on your part) to catch regressions Instruments won't see (e.g. cold storage / low-end-device-specific launch cost).

---

## 4. Hitches & scrolling

- **Hitch time ratio** — total hitch time in an interval ÷ interval duration, in ms/s. Apple's stated bands: **< 5 ms/s** = good, mostly imperceptible; **5–10 ms/s** = user-noticeable; **≥ 10 ms/s** = distracting, treat as a blocking regression.
- Measure with the **Animation Hitches** Instruments template locally, and `MXAnimationMetric` (MetricKit) in the field — the field number is the one that matters for release gating, since device/thermal/background-load conditions vary far more than a dev machine.
- **Main-thread blocking sources** to check first when a hitch shows up: synchronous image decode on the main thread, `body` recomputation triggered by an unrelated state field (§2.2), synchronous Core Data/SwiftData fetches during scroll, layout passes triggered by `GeometryReader` misuse.
- **Image decode off-main**: decode (not just load) large images on a background queue/Task before handing a `UIImage`/`Image` to SwiftUI — `UIImage(data:)` defers decode to first draw, which lands on the main thread at scroll time unless pre-decoded.
- **Prefetching**: for `List`/`LazyVStack` with remote images or heavy row content, prefetch N rows ahead of the visible window (`onAppear` on a not-yet-visible sentinel row, or a dedicated prefetch API in the image library) so decode/network cost lands before the row scrolls into view, not during.

---

## 5. Memory

### 5.1 Footprint limits and jetsam

iOS enforces a per-process resident-memory ceiling (jetsam limit) that scales with device RAM class — roughly on the order of ~2GB on recent 4GB-RAM devices in practice, materially lower on older/lower-RAM devices, and app extensions get a substantially tighter limit than the foreground app `(unverified precise current per-device-class table — Apple does not publish exact numbers and they shift by device; profile with the **Memory** gauge / Allocations on the actual target device class rather than budgeting to a memorized number)`. Backgrounded/suspended apps are jetsam-killed first under memory pressure to protect the foreground app.

### 5.2 Memory graph debugger + retain cycles

Xcode's Memory Graph Debugger (▶ the memory-graph icon while debugging, or `Debug Memory Graph`) surfaces reference cycles directly, including two SwiftUI/`@Observable`-specific patterns:

| Pattern | Cycle | Fix |
|---------|-------|-----|
| `@Observable` model capturing `self` in an escaping closure (e.g. stored `Task` or delegate callback) | Model → closure → model | `[weak self]` in the closure; unwrap at the top |
| SwiftUI `.onReceive`/Combine subscription stored on a class holding a strong reference back to the publisher's owner | Owner → subscription → owner | `weak` reference to owner inside the subscription closure, or scope the subscription to view lifetime via `.task`/`.onChange` instead of hand-rolled Combine storage |

### 5.3 Autorelease behavior

See `bolt/reference/swift-cheatsheet.md` §6 for the full ARC/autoreleasepool treatment — the Native-specific addition is: image-processing and Core Data/SwiftData fetch loops that bridge through Foundation/CoreGraphics types (`UIImage`, `CGImage`, `NSManagedObject` faults) are the most common source of autorelease buildup inside a SwiftUI `.task { }` that iterates, since SwiftUI's own task/render loop does not drain an inner pool for you mid-iteration.

### 5.4 Image/asset memory

- **`UIGraphicsImageRenderer`** — preferred over `UIGraphicsBeginImageContextWithOptions` for any programmatic image rendering; manages its own backing store and avoids the older API's manual context lifecycle bugs.
- **Downsample before display, not after** — decoding a full-resolution source image then letting SwiftUI/UIKit scale it down for display keeps the full decoded bitmap in memory. Use `CGImageSourceCreateThumbnailAtIndex` with `kCGImageSourceThumbnailMaxPixelSize` set to the actual display size (in points × scale) to decode directly at target resolution:

```swift
func downsampledImage(at url: URL, maxDimensionInPixels: CGFloat) -> CGImage? {
    let sourceOptions = [kCGImageSourceShouldCache: false] as CFDictionary
    guard let source = CGImageSourceCreateWithURL(url as CFURL, sourceOptions) else { return nil }
    let downsampleOptions = [
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceShouldCacheImmediately: true,
        kCGImageSourceCreateThumbnailWithTransform: true,
        kCGImageSourceThumbnailMaxPixelSize: maxDimensionInPixels,
    ] as CFDictionary
    return CGImageSourceCreateThumbnailAtIndex(source, 0, downsampleOptions)
}
```

Measured wins from this pattern are typically large — e.g. a 5120×2880 source rendered at thumbnail size can drop from tens of MB resident to single-digit MB, since the full-resolution bitmap is never decoded.

---

## 6. Concurrency perf

Cross-reference `reference/modern-stack.md` § Swift 6.2 Approachable Concurrency for the `@concurrent` / default-MainActor-isolation mechanics — this section covers the **cost model**, not the syntax.

- **Main-actor hop cost**: every `await` that crosses from a background context back to `@MainActor` (or vice versa) is a real scheduling hop, not free. In Swift 6.2's caller-inherited-isolation model, an unmarked `async` function called from `@MainActor` code **stays on MainActor** — this eliminates accidental hops that Swift 6.0/6.1 code often paid for implicitly, but means CPU-bound work needs an explicit `@concurrent` to actually leave the main actor.
- **`@concurrent` vs default isolation**: default (implicit `@MainActor` in Xcode 26 new-project settings) is correct for UI-driving ViewModels/Repositories; reach for `@concurrent` only for work that is provably CPU-bound and doesn't touch UI state — decoding, image processing, diffing large collections.
- **Actor contention**: an actor serializes all access to its isolated state — a single actor fielding high-frequency calls from many tasks becomes a bottleneck identical in shape to a single-threaded lock. Profile with the **Swift Concurrency** Instruments template to see queueing time on the actor's mailbox, not just wall-clock per call.
- **`Task` explosion**: spawning one `Task` per list item / per event in a tight loop (e.g. inside a `ForEach` or a `for` loop over a large collection) creates real scheduler overhead per task even when each does little work. Prefer a single structured `Task` that iterates, or `TaskGroup` with a bounded concurrency limit, over unbounded fan-out.
- **Priority inversion**: a low-priority `Task` holding an actor while a high-priority `Task` waits on the same actor causes priority inversion; Swift's cooperative pool does priority-donation to mitigate this automatically, but chronic inversion (visible as a high-priority task's Time Profiler samples showing wait rather than execution) usually indicates the actor is doing too much low-priority work inline — move it to a separate, lower-contention actor.

---

## 7. Field telemetry

### 7.1 MetricKit

`MXMetricPayload` is delivered daily (typically) via `MXMetricManagerSubscriber`, aggregating real-device data:

| Metric | What it reports |
|--------|-----------------|
| `MXAppLaunchMetric` | Launch-time histograms (see §3.5) |
| `MXAnimationMetric` | Hitch time ratio (see §4) |
| `MXSignpostMetric` | Aggregated stats for any custom `os_signpost`/`OSSignposter` interval you've instrumented — the mechanism for shipping your own perf markers into field telemetry |
| `MXMemoryMetric` | Peak memory, average suspended memory |
| `MXCPUMetric`, `MXDiskIOMetric`, `MXNetworkTransferMetric` | Resource-usage aggregates |

### 7.2 `os_signpost` custom intervals

```swift
import os
let signposter = OSSignposter(subsystem: "com.app.feed", category: "load")

func loadFeed() async {
    let state = signposter.beginInterval("feedLoad", id: signposter.makeSignpostID())
    defer { signposter.endInterval("feedLoad", state) }
    // ...
}
```

Wrap any interval you want visible both in local Instruments traces (Time Profiler / os_signpost template correlation) **and** in field `MXSignpostMetric` aggregates — this is the lowest-overhead way to bridge local profiling and production telemetry with the same instrumentation code (see `bolt/reference/swift-cheatsheet.md` §1.1 for the API detail).

### 7.3 Xcode Organizer regressions + CI perf budgets

- Xcode Organizer's **Launch Time**, **Hangs**, and **Disk Writes** reports aggregate real App Store user data without any MetricKit integration work — check these on every release, not just when a user files a complaint.
- Treat cold-start / hitch-ratio / memory-footprint targets as **CI gates**, not aspirational docs: a scripted UI test that launches the app, captures an `App Launch` or `Animation Hitches` trace via `xctrace`, and fails the build if the measured value regresses past a checked-in baseline is the only reliable way to prevent silent perf drift across a team. Pair with `reference/xcrun-cli.md` §3's `xctrace export --xpath` for parsing the trace into a comparable number in CI.

---

## 8. Anti-pattern table

| Signal | Why it bites | Fix |
|--------|--------------|-----|
| `AnyView` used for conditional branching | Erases type; defeats compile-time diffing | `@ViewBuilder` conditional return |
| `ForEach(array.indices)` or `id: \.self` on mutable structs | Positional diffing leaks row state across insert/delete | `ForEach(items, id: \.stableID)` |
| `.id()` applied to a large container on frequent state change | Forces full subtree re-init, breaks animation interpolation | Scope `.id()` to the smallest node; use `onChange`/`.animation(value:)` instead |
| Destructuring a whole `@Observable` model into local `let`s at top of `body` | Re-couples the view to every property, defeating per-property tracking | Read only the fields the view renders |
| Inline closures rebuilt every `body` pass passed to perf-sensitive children | Breaks `EquatableView`/reference-equality skip checks | Stored method reference / `remember`-style caching |
| `UIImage(data:)` handed straight to a `List` row without pre-decode | Decode happens on main thread at scroll time | Background decode via `CGImageSourceCreateThumbnailAtIndex` before display |
| One `Task { }` spawned per loop iteration over a large collection | Scheduler overhead per task dominates small per-item work | Single structured `Task` or bounded `TaskGroup` |
| CPU-bound work left on default (MainActor-inherited) isolation | Blocks UI responsiveness despite `async` | Explicit `@concurrent` |
| `App.init` / `didFinishLaunching` doing non-critical setup synchronously | Delays first frame | Defer to post-first-frame `.task { }` |
| Full-resolution image decode for thumbnail display | Peak memory far exceeds displayed size | Downsample at decode time, not after |
| Missing `weak self` in `@Observable` model's stored `Task`/closure | Retain cycle, model never deallocates | `[weak self]` + guard/unwrap |
| Shipping `Self._printChanges()` calls | Debug-only, undocumented API surface, console noise in production | Strip before release; use Instruments for shipped-build investigation |

---

## 9. Routing rules

| Situation | Route to | Why |
|-----------|----------|-----|
| SwiftUI `body`/render/diffing perf, view-graph thrash, launch/hitch/memory on Apple platforms | **Native** (this file) | Platform- and framework-specific measurement + fix |
| Swift language-level perf: ARC, COW, generic specialization, `@inlinable`, autoreleasepool mechanics, Combine vs AsyncSequence cost model | **Bolt** (`bolt/reference/swift-cheatsheet.md`) | Language/runtime level, not SwiftUI-specific |
| Algorithmic complexity, data-structure choice independent of platform | **Bolt** | General profiling discipline, cross-platform |
| Slow SQL query / Core Data fetch predicate / index design feeding a SwiftUI list | **Tuner** (query/index layer) → Native consumes the result | Query plan optimization is Tuner's domain; Native owns the render-side consumption |
| SLO/alerting on field launch-time or hitch-ratio regressions, dashboarding MetricKit aggregates over time | **Beacon** | Observability/SLO design, not one-off measurement |
| "This got slower sometime in the last N releases, bisect it" | **Trail** | Git-history/regression bisection is Trail's domain; Native supplies the metric to bisect against |
| New feature scaffolding that happens to need offline/persistence design | **Native** `offline` Recipe (`reference/patterns.md`) | Architecture decision, not a perf regression |

---

## Sources

- [Optimize SwiftUI performance with Instruments — WWDC25](https://developer.apple.com/videos/play/wwdc2025/306/) (2025-06)
- [Meet the new MetricKit — WWDC26](https://developer.apple.com/videos/play/wwdc2026/222/) (2026-06)
- [MXAppLaunchMetric — Apple Developer Documentation](https://developer.apple.com/documentation/metrickit/mxapplaunchmetric)
- [MXSignpostMetric — Apple Developer Documentation](https://developer.apple.com/documentation/metrickit/mxsignpostmetric)
- [Avoid hitches and discover the Render Loop — WWDC21](https://a11y-guidelines.orange.com/en/mobile/ios/wwdc/nota11y/2021/21hitches/) (hitch time ratio bands)
- [Analyze hangs with Instruments — WWDC23](https://developer.apple.com/videos/play/wwdc2023/10248/)
- [`dyld4` design doc — apple-oss-distributions/dyld](https://github.com/apple-oss-distributions/dyld/blob/main/doc/dyld4.md)
- [The Mystery Behind View Equality — SwiftUI Lab](https://swiftui-lab.com/equatableview/) (`EquatableView` mechanics)
- [Optimizing views in SwiftUI using EquatableView — Swift with Majid](https://swiftwithmajid.com/2020/01/22/optimizing-views-in-swiftui-using-equatableview/)
- [Identifying High Memory Use with Jetsam Event Reports — Apple Developer Documentation](https://developer.apple.com/tutorials/data/documentation/xcode/identifying-high-memory-use-with-jetsam-event-reports.md)
- [`CGImageSourceCreateThumbnailAtIndex` downsampling technique — Swift Senpai](https://swiftsenpai.com/development/reduce-uiimage-memory-footprint/)
- Source of truth: [`bolt/reference/swift-cheatsheet.md`](../../bolt/reference/swift-cheatsheet.md), [`reference/modern-stack.md`](modern-stack.md), [`reference/xcrun-cli.md`](xcrun-cli.md)
