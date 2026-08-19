# Android/Compose Performance Reference (2026)

Agent-specific slice for **Native** — measurement and optimization for Android Kotlin + Jetpack Compose apps. Baseline assumes Kotlin 2.4+ (K2 compiler) / Compose 1.11 / Material 3 Expressive (BOM 2026.05), as of 2026-07.

This file does **not** duplicate `bolt/reference/kotlin-cheatsheet.md` §13 (JVM/Kotlin-language-level Compose bytecode notes, Flow perf, build performance). Apply `builder/reference/implementation-policy.md` when Kotlin or Compose behavior depends on the detected toolchain. Read it alongside:

- [`bolt/reference/kotlin-cheatsheet.md`](../../bolt/reference/kotlin-cheatsheet.md) §13 — Bolt's high-level watch list; this file is where Bolt defers to for actual Compose runtime mechanics
- [`reference/modern-stack.md`](modern-stack.md) § Stable Types & Strong Skipping Mode — the 2026 stability/Strong-Skipping policy this file assumes as baseline
- [`reference/patterns.md`](patterns.md) § Android — controlling Compose recomposition — code-pattern examples this file does not re-show
- [`reference/android-material3.md`](android-material3.md) — M3 Expressive component API surface (`LoadingIndicator`/`Carousel`/spring motion have render-cost implications noted here)
- [`reference/adb-cli.md`](adb-cli.md) §9 — full `adb shell perfetto` / `dumpsys gfxinfo` command reference; this file only points at the commands relevant to a given symptom

The role of this reference: **what to measure before touching code, which recomposition/startup/frame/memory patterns cause the regressions Native ships, and how to wire perf budgets into field telemetry and CI.**

---

## 1. Measurement-first discipline

**Never optimize without a captured baseline.** Capture on the target device class (mid-tier physical device, not the emulator, not the newest flagship in the drawer) before and after any change; a "faster" diff with no before/after measurement is not a verified fix.

### 1.1 Decision table — which tool answers which question

| Question | Tool | Notes |
|----------|------|-------|
| "Why did this composable recompose / how often?" | **Layout Inspector** recomposition counts (Android Studio) | Per-composable recomposition + skip counts, color-coded overlay on the running app |
| "Which composables are skippable/restartable, and what makes a class unstable?" | **Compose Compiler Metrics/Reports** (`composeCompiler { metricsDestination / reportsDestination }`) | Static, build-time — no device needed; the primary tool for stability diagnosis (§3.2) |
| "Where is wall-clock CPU going?" | **Android Studio Profiler** — CPU Profiler (System Trace / Callstack Sample) | Method traces, thread state, main-thread blocking |
| "Where are allocations happening / growing?" | **Android Studio Profiler** — Memory Profiler | Heap dump, allocation tracking, GC event overlay |
| "Is the app draining battery / waking the radio unnecessarily?" | **Android Studio Profiler** — Energy Profiler | Wakelocks, location requests, network radio state |
| "Did a frame miss its deadline, and where in the pipeline?" | **Perfetto / System Tracing** (`adb shell perfetto`, ui.perfetto.dev) | Full system trace — UI thread, RenderThread, GPU, other processes |
| "What's the CPU/RenderThread split for frames, in percentiles?" | **Macrobenchmark** `FrameTimingMetric` | Automated, CI-friendly, P50/P90/P95/P99 distribution — not a one-off inspection |
| "Is cold/warm/hot startup slow, and by how much?" | **Macrobenchmark** `StartupTimingMetric` | `timeToInitialDisplayMs` (first frame) + `timeToFullDisplayMs` (fully drawn) |
| "Is a specific function/algorithm the bottleneck, isolated from the app?" | **Microbenchmark** (`androidx.benchmark.junit4.BenchmarkRule`) | JIT-warmed, isolated method-level timing — not UI/frame-level |
| "Quick jank signal without setting up a benchmark module?" | **`adb shell dumpsys gfxinfo <package>`** | One-shot frame-render stats; full command reference → `reference/adb-cli.md` §3 |
| "Real-time jank frequency and cause, cheap enough to ship in production?" | **JankStats** (`androidx.metrics:metrics-performance`) | Per-frame jank callback with a reported reason string; the field-telemetry-friendly option (§9) |

**Rule**: profile on-device → hypothesize → change one variable → re-profile. Trust the measured trace over intuition — Compose's positional memoization and skipping rules make manual reasoning about "what recomposes" unreliable past trivial composable trees.

---

## 2. Tooling

### 2.1 Android Studio Profiler

Unified CPU / Memory / Energy / Network profiler windows, attachable to a running debug or profileable-release process. Use System Trace mode for main-thread/RenderThread correlation; use Callstack Sample mode for hot-function identification. Profileable builds (`android:profileable="true"` in the manifest, or `<profileable>` in a release-adjacent build variant) let you profile close-to-release performance without a full debuggable build's overhead.

### 2.2 Compose Compiler Metrics / Reports

Configured via the Kotlin 2.x Compose compiler Gradle plugin's `composeCompiler {}` extension (this DSL replaced the pre-2.0 `composeOptions { kotlinCompilerExtensionVersion }` + `freeCompilerArgs` mechanism — do not use the old form on Kotlin 2.x):

```kotlin
// build.gradle.kts (module level, wherever the compose compiler plugin is applied)
composeCompiler {
    metricsDestination = layout.buildDirectory.dir("compose_metrics")
    reportsDestination = layout.buildDirectory.dir("compose_reports")
}
```

Run a build (`./gradlew :app:assembleRelease` or any compile task) and inspect the output:

- **`*-module.json`** (from `metricsDestination`) — aggregate counts: total composables, skippable %, restartable %, stable classes vs unstable classes, stable parameters vs unstable parameters.
- **`*-composables.csv` / `*-classes.csv`** (from `reportsDestination`) — per-composable and per-class detail: `skippable`, `restartable`, `readonly`, and for classes, `stable` with the specific field that breaks stability listed inline (e.g. `unstable class Foo { var name: String }` — a `var` breaks stability even for an otherwise-simple type).

Reading the output: a composable marked **not skippable** either takes an unstable parameter or the compiler could not prove all parameters stable — cross-reference the class report for the exact unstable member. A raw lambda capturing an unstable value (rather than a stored method reference) commonly shows up here as the culprit.

Feature flags — the compiler exposes a typed `featureFlags` set instead of raw compiler args:

```kotlin
composeCompiler {
    featureFlags = setOf(
        ComposeFeatureFlag.StrongSkipping,          // on by default; explicit here for clarity
        ComposeFeatureFlag.OptimizeNonSkippingGroups,
    )
}
```

### 2.3 Layout Inspector recomposition counts

Android Studio's Layout Inspector (attach to a running debug session) overlays live recomposition + skip counts per composable in the running UI hierarchy. Use it to confirm a Compose Compiler Report hypothesis against actual runtime behavior — the report says a composable is skippable; Layout Inspector confirms whether it's actually being skipped in the interaction you care about.

### 2.4 Macrobenchmark

`androidx.benchmark:benchmark-macro-junit4` — JUnit4 `MacrobenchmarkRule` drives the target app as a separate installed APK and measures across full process boundaries:

```kotlin
@RunWith(AndroidJUnit4::class)
class FeedStartupBenchmark {
    @get:Rule val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun startupCompilationDefault() = benchmarkRule.measureRepeated(
        packageName = "com.example.app",
        metrics = listOf(StartupTimingMetric(), FrameTimingMetric()),
        iterations = 10,
        startupMode = StartupMode.COLD,
        compilationMode = CompilationMode.DEFAULT,   // installs a Baseline Profile, mirrors real users
    ) {
        pressHome()
        startActivityAndWait()
    }
}
```

- **`StartupTimingMetric`** — reports `timeToInitialDisplayMs` (first frame drawn) and `timeToFullDisplayMs` (app calls `reportFullyDrawn()`).
- **`FrameTimingMetric`** — CPU + RenderThread per-frame duration, aggregated as P50/P90/P95/P99.
- **`CompilationMode`** — `DEFAULT` (installs Baseline Profile, matches real-user post-install state), `None` (no AOT/profile — cold JIT, worst case), `Partial` (profile-guided, configurable interpreted/JIT ratio), `Full` (fully AOT-compiled — best case, not representative of a real user's device state), `Ignore` (assumes the app was already compiled by a prior `CompilationMode.Full()` run — skip in normal workflows). Compare `None` vs `DEFAULT` to quantify what a Baseline Profile is actually buying (§4.1).

Macrobenchmark must run against a **`benchmark` build type** the Baseline Profile Gradle plugin generates — never against `debug` (§8). **Microbenchmark** (`androidx.benchmark:benchmark-junit4`'s `BenchmarkRule`) is the isolated, JIT-warmed method/algorithm sibling — use it for hot-path business logic (parsing, diffing, sorting) feeding a composable, not for measuring the composable itself.

### 2.5 Perfetto / System Tracing

```bash
# Trigger a Perfetto trace with an inline text-proto config
adb shell perfetto -c - --txt -o /data/misc/perfetto-traces/trace.pftrace <<EOF
buffers: { size_kb: 65536 }
data_sources: { config { name: "linux.ftrace" ftrace_config { ftrace_events: "sched/sched_switch" atrace_categories: "gfx" atrace_categories: "view" atrace_apps: "com.example.app" } } }
duration_ms: 10000
EOF
adb pull /data/misc/perfetto-traces/trace.pftrace
# Open at https://ui.perfetto.dev
```

Full `adb shell perfetto` invocation options and the `atrace` category list → `reference/adb-cli.md` §9. For app-specific spans inside a Perfetto trace, wrap code with `androidx.tracing.trace { }` (Kotlin, wraps `Trace.beginSection`/`endSection`):

```kotlin
import androidx.tracing.trace

fun loadFeed() {
    trace("loadFeed") {
        // work shows up as a named slice on the Perfetto timeline
    }
}
```

[Composition tracing](https://developer.android.com/develop/ui/compose/tooling/tracing) is a separate, narrower Studio-integrated mechanism for which composable/recomposition is active during a trace; prefer `trace()` for app-level spans in a Macrobenchmark or field trace.

### 2.6 JankStats

`androidx.metrics:metrics-performance` — per-`Window` jank callback usable in production, not just local profiling:

```kotlin
val jankStats = JankStats.createAndTrack(window) { frameData ->
    if (frameData.isJank) {
        // frameData.frameDurationUiNanos, frameData.states (custom state tags)
        analytics.logJank(frameData)
    }
}
```

Tag the current UI state (`PerformanceMetricsState.getForHierarchy(view).state?.putState("screen", "Feed")`) before frames render so jank reports carry context rather than an anonymous timestamp — this is what makes JankStats useful as field telemetry (§9), not just a local tool.

For a fast, no-setup frame-render snapshot without any of the above setup: `adb shell dumpsys gfxinfo com.example.app` (summary: janky frames, 50/90/95/99th percentile) and `adb shell dumpsys gfxinfo com.example.app framestats` (per-frame timing, last ~120 frames) — good for a quick manual-QA sanity check; Macrobenchmark `FrameTimingMetric` is the CI-grade equivalent. Full flag reference → `reference/adb-cli.md`.

---

## 3. Recomposition

### 3.1 The three phases

Compose's frame pipeline runs three phases per frame: **Composition** (which composables run, producing a description of the UI), **Layout** (measuring and placing that description), **Draw** (rendering pixels). Each phase can be skipped independently — a value read only during Layout/Draw does not need to trigger Composition at all.

**Phase-skipping via lambda-deferred reads**: reading a `State` value directly in a composable's body forces that composable through Composition on every change. Deferring the read into a lambda consumed only at Layout/Draw time skips Composition entirely:

```kotlin
// Triggers recomposition of the whole composable on every scroll pixel
Box(Modifier.offset(x = offsetPx.dp))

// Skips Composition — offsetPx is read directly during the Layout phase
Box(Modifier.offset { IntOffset(offsetPx.roundToInt(), 0) })
```

The same pattern applies to `graphicsLayer { }` (vs. individually-parameterized `Modifier.scale()`/`.alpha()`/`.rotate()`) for animation-driven transforms — `graphicsLayer`'s lambda form reads its inputs at Draw time, so an animating scale/alpha/rotation never re-runs Composition or Layout, only Draw.

### 3.2 Unstable-type diagnosis

A composable becomes **not skippable** when the compiler cannot prove all its parameters stable. Sources of instability:

- Interfaces and classes with `var` properties (even primitives).
- Public constructor parameters typed as `List`, `Set`, or `Map` (Kotlin's standard collection interfaces are treated as unstable — they don't guarantee immutability).
- Any type defined outside the current compilation's module boundary that the compiler cannot introspect (e.g. from a Java dependency, or a Kotlin module compiled without the Compose compiler plugin).

Diagnose with the Compose Compiler Report (§2.2), not guesswork — the classes report names the exact unstable member.

### 3.3 `@Stable` / `@Immutable` contracts

```kotlin
@Immutable   // promise: all public properties are val, and every property's value never changes after construction
data class FeedSnapshot(val items: ImmutableList<Post>)

@Stable      // promise: equals()-stable over time even if fields mutate — mutation always notifies Compose (e.g. via State)
class ScrollController {
    var offset by mutableStateOf(0f)
        private set
}
```

Both are **unenforced compiler promises** — annotating a type that violates the contract (e.g. `@Immutable` on a class with a `var` that mutates outside Compose's snapshot system) causes silent stale-UI bugs, not a compile error. Only annotate when the contract is actually true.

### 3.4 `kotlinx.collections.immutable` and Strong Skipping Mode

**Strong Skipping Mode** is the default since Compose Compiler 1.5.4 and remains default across the Kotlin 2.x (K2) Compose compiler line (explicit opt-out via `ComposeFeatureFlag.StrongSkipping.disabled()`, not something to reach for). With it on:

- All restartable composables become skippable, even ones with unstable parameters.
- The runtime compares unstable parameters by **instance reference (`===`)** rather than refusing to skip outright.
- Lambdas with unstable captures are automatically memoized (no manual `remember` needed for the common case).

**2026 policy shift** (full rationale owned by `reference/modern-stack.md` § Stable Types & Strong Skipping Mode — summary only here): the old blanket advice "wrap every collection in `ImmutableList`" is no longer default. Strong Skipping doesn't change a type's *stability* — `List`/`Set`/`Map` stay unstable — it changes how the *runtime* handles an unstable parameter: compare by reference, skip if unchanged. `kotlinx.collections.immutable`'s `ImmutableList`/`PersistentList` is genuinely stable via `equals()`, but for large lists that's `O(n)` — a net loss over reference comparison unless the producer already returns the same instance on no-change. **Default in 2026**: pass `List<T>` straight through; reach for `ImmutableList` only when a Compose Compiler Report shows a *measured* problem AND the producer can guarantee instance stability.

What Strong Skipping does **not** fix: a lambda capturing a genuinely-changing unstable value each call (memoization only helps identical captures); composables marked `@NonRestartableComposable` or excluded top-level/inline composables; context receivers or generic parameterizations the compiler still can't prove stable under reference comparison. Verify via Compose Compiler Report — do not assume Strong Skipping is a blanket fix.

### 3.5 `derivedStateOf`

Use when a composable's input is a **cheap derivation of a frequently-changing value**, and only the derived boolean/enum/small result — not the raw frequently-changing value — should trigger recomposition:

```kotlin
val showScrollToTopButton by remember {
    derivedStateOf { listState.firstVisibleItemIndex > 0 }
}
```

`listState.firstVisibleItemIndex` changes on every scrolled pixel; `showScrollToTopButton` changes only when crossing the threshold. Without `derivedStateOf`, a composable reading `firstVisibleItemIndex` directly recomposes every scroll frame even though its visible output (the button) rarely changes.

### 3.6 `remember` keys

`remember(key1, key2) { expensiveCompute() }` re-runs the block only when a key changes — omitting keys (bare `remember { }`) means the value survives for the composable's entire lifetime in the composition, which is wrong whenever the computation depends on a changing input. A `remember` with no keys computing from a parameter that does change is a common source of stale-data bugs, distinct from the pure-perf topics elsewhere in this section.

### 3.7 `key()` and `contentType` in lazy lists

```kotlin
LazyColumn {
    items(items = posts, key = { it.id }, contentType = { it.mediaType }) { post ->
        PostRow(post)
    }
}
```

- **`key`** — stabilizes item identity across insertions/reorders/deletions so Compose reuses existing composition state (scroll position, `remember`ed values inside the row) for the same logical item, instead of remounting by position. Omitting `key` on a list that reorders is the single most common cause of visible state-leak-across-rows bugs.
- **`contentType`** — tells Compose which items are layout-compatible for slot reuse. A `LazyColumn` mixing multiple row shapes (text row, image row, ad row) without `contentType` forces Compose to discard and reinflate a slot whenever a scrolled-in item's type differs from the recycled slot's previous occupant type — the same class of win `RecyclerView.getItemViewType()` provides on the View system.

### 3.8 Avoiding state reads in Composition when a lambda would do

Beyond `Modifier.offset { }` (§3.1), the general rule: any `Modifier` or draw-time parameter that accepts a lambda overload exists specifically to let Compose defer the state read past Composition. Prefer the lambda overload (`Modifier.offset { }`, `Modifier.graphicsLayer { }`, `Modifier.drawWithContent { }`) over the value overload (`Modifier.offset()`, individual `.scale()`/`.alpha()`) whenever the backing state changes at animation/scroll frequency rather than at business-logic frequency.

---

## 4. Startup

### 4.1 Baseline Profiles

A Baseline Profile (`baseline-prof.txt`, bundled in the APK/AAB) lists classes/methods ART should AOT-compile or interpret at a higher tier immediately after install, instead of relying on cold JIT warm-up. Generated via the Baseline Profile Gradle plugin + a `BaselineProfileRule` test module:

```kotlin
// build.gradle.kts (app module)
plugins {
    id("androidx.baselineprofile")
}
dependencies {
    baselineProfile(project(":baselineprofile"))
}
```

```kotlin
// :baselineprofile module — generator test
@RunWith(AndroidJUnit4::class)
class StartupBaselineProfile {
    @get:Rule val rule = BaselineProfileRule()

    @Test
    fun generate() = rule.collect(packageName = "com.example.app") {
        pressHome()
        startActivityAndWait()
        // drive the critical user journeys whose classes should be pre-compiled
    }
}
```

The Gradle plugin wires generation into the release build and drops the result into `src/release/generated/baselineProfile/`. **Verification**: run the same journey under Macrobenchmark with `CompilationMode.None` vs `CompilationMode.DEFAULT` (which installs the Baseline Profile) and compare `StartupTimingMetric` — the delta is what the profile is actually buying, not an assumed number. Commonly cited industry figures land in the 20-40% cold-startup-time-reduction range; measure your own app rather than assuming a fixed percentage.

### 4.2 Startup Profiles

A narrower sibling (`startup-prof.txt`) containing only methods flagged startup-critical; D8/R8 use it to control **DEX layout** — placing startup-critical code in the primary DEX file so class loading doesn't pay a multi-DEX lookup cost. Baseline Profiles are a superset covering broader post-startup hot paths; Startup Profiles are DEX-layout-only and startup-scoped. Generated via the same `BaselineProfileRule` infrastructure and the **same Gradle task** as §4.1 — `:app:generateBaselineProfile` (or `:app:generateVariantBaselineProfile` when `mergeIntoMain = false`). There is no separate task: pass `includeInStartupProfile = true` to `rule.collect()` on the journeys that should land in `startup-prof.txt` rather than only `baseline-prof.txt`. `CompilationMode` (§2.4) is the primary lever for isolating "how much of my startup number is the Baseline Profile vs. my own code": `None` (worst case, no AOT help), `Partial` (interpreted/JIT mix, profile-guided — mirrors a real post-install device), `Full` (fully AOT — a ceiling, not a real-world state since Play doesn't ship fully-AOT APKs).

### 4.3 App Startup library

`androidx.startup:startup-runtime`'s `Initializer<T>` interface lets multiple libraries declare startup dependencies and initialize in topologically-sorted order within a single `ContentProvider`, replacing the older pattern of each library registering its own `ContentProvider` (each of which adds real per-provider startup overhead). Use it to consolidate third-party SDK initialization; it does not by itself make initialization work cheaper — it only removes the multi-`ContentProvider` tax.

### 4.4 Avoiding work in `Application.onCreate`

Anything not required to render the first frame — analytics SDK init, non-critical prefetch, background sync scheduling — belongs after first-frame (`Activity.onResume` / a post-frame callback), not synchronously in `Application.onCreate`. `Application.onCreate` runs before any `Activity` starts, so synchronous work here directly extends the pre-first-frame window on every cold start.

### 4.5 Cold / warm / hot definitions and targets

| State | Definition | What's already warm |
|-------|-----------|---------------------|
| **Cold** | Process not running; app not in Recents | Nothing — full process creation, `Application.onCreate`, first `Activity` creation |
| **Warm** | Process still alive; `Activity` was destroyed or app was in background | Process/JVM, but `Activity`/view hierarchy must be recreated |
| **Hot** | `Activity` brought back to foreground from Recents/`onStop` | Everything — just a lifecycle resume, no recreation |

`StartupMode.COLD/WARM/HOT` in `MacrobenchmarkRule.measureRepeated` selects which one a given benchmark exercises — cold is the meaningful target for Baseline Profile verification since it's where AOT/interpretation state matters most. Target: no universally-mandated number, but treat any measured *regression* in `timeToInitialDisplayMs` against your own checked-in baseline as a CI-blocking signal (§9.2) rather than picking an absolute target from a generic guideline.

---

## 5. Jank & frame timing

### 5.1 Frame budget

| Refresh rate | Budget per frame |
|--------------|-------------------|
| 60 Hz | 16.7 ms |
| 90 Hz | 11.1 ms |
| 120 Hz | 8.3 ms |

A frame that misses its budget on a 120Hz device is jank at that device's refresh rate even if it would have been fine at 60Hz — `FrameTimingMetric` and JankStats both compare against the device's actual configured refresh rate, not a hardcoded 16ms.

### 5.2 `FrameTimingMetric` percentiles

Macrobenchmark's `FrameTimingMetric` reports frame-time distribution as P50/P90/P95/P99 across the benchmarked interaction — treat P50 as "typical" and P90/P99 as the tail that actually produces user-visible jank complaints. A regression that only moves P50 slightly but blows out P99 is often worse for perceived quality than a uniform P50 shift, since P99 events are the visible stutters.

### 5.3 Main-thread blocking sources

Check first when a hitch appears:

- Synchronous image decode on the main thread (§5.4).
- A composable's phase-1 (Composition) work triggered by an unrelated state field changing (§3).
- Heavy `LazyColumn` item `body` work — date formatting without a cached `DateTimeFormatter`, inline JSON parsing, synchronous disk reads inside a row composable.
- Over-invalidation via `graphicsLayer` — reading a *non-frame-scoped* state inside a `graphicsLayer { }` block (e.g. reading a `ViewModel`-derived value that changes with normal business-logic frequency rather than animation frequency) forces Draw-phase re-execution as often as Composition-phase would have anyway, without the composable-skipping benefit `graphicsLayer` exists to provide.

### 5.4 Image loading off-main

Use Coil 3's `AsyncImage`/`rememberAsyncImagePainter` — decode happens off the main thread by default via its coroutine-based pipeline. The anti-pattern is loading a `Bitmap` synchronously (e.g. `BitmapFactory.decodeStream` called directly inside a composable or a `LaunchedEffect` without dispatching to `Dispatchers.IO`/`Default`) and handing the decoded result to Compose — the decode itself, not just the network fetch, is the expensive part.

### 5.5 `LazyColumn` item cost

Combine `key` + `contentType` (§3.7) with off-main image decode (§5.4) and cached formatters — a `LazyColumn` row that's individually fast but paying avoidable Composition churn from a missing `key`/`contentType` shows up as a scroll-jank regression that looks like "the row is slow" but is actually "the row is being needlessly recreated."

---

## 6. Memory

### 6.1 Heap dumps and LeakCanary

Android Studio's Memory Profiler captures on-demand heap dumps for manual inspection (dominator tree, retained-size sort). For continuous leak detection during development, **LeakCanary** (Block/Square) auto-dumps on `Activity`/`Fragment`/`ViewModel` destruction and surfaces a leak trace with the retaining reference chain — the standard default for catching leaks before they reach a Macrobenchmark memory regression.

### 6.2 Composition and `remember` leaks

A `remember { }`-captured lambda that closes over a `NavController`, `Context`, or `ViewModel`, then stored somewhere longer-lived than the composable (e.g. handed to a singleton event bus), retains the whole composition's captured scope — mirrors the SwiftUI-side `[weak self]` pattern (`native/reference/apple-perf.md` §5.2): scope the lambda via `DisposableEffect`/`remember(key)`, never hand composable-scoped closures to app-scoped singletons. Separately, `remember { loadEntireDatasetIntoMemory() }` ties that data's lifetime to the composition, not a `ViewModel` — if the composable can be disposed/recreated (inside a `LazyColumn` row, or behind navigation), large data belongs in a `ViewModel`-scoped holder with an explicit `onCleared()`, not in `remember`.

### 6.3 Bitmap memory and `ViewModel` scope leaks

Same downsample-before-decode discipline as iOS (`native/reference/apple-perf.md` §5.4): Coil's `size()`/`Scale` request parameters or `BitmapFactory.Options.inSampleSize` should decode at target display resolution, not full source resolution scaled down after the fact. Separately, a `ViewModel` holding a `View`/`Activity Context`/`NavController` reference outlives its screen if scoped too broadly (e.g. accidentally hoisted to the Activity-scoped `ViewModelStoreOwner` instead of nav-graph- or screen-scoped) — verify scope matches intended screen lifetime.

### 6.4 `collectAsStateWithLifecycle` vs `collectAsState`

- **`collectAsStateWithLifecycle()`** — lifecycle-aware; collection starts at `STARTED` and stops below it, releasing upstream `Flow` resources (and any expensive producer work) while the screen is backgrounded. This is the default choice for `ViewModel`-exposed `StateFlow` in an Android app.
- **`collectAsState()`** — follows Composition lifecycle only, not the Android `Lifecycle`; keeps collecting even while the app is backgrounded unless the composable itself leaves composition. Appropriate for platform-agnostic/local UI state, not for `ViewModel` flows tied to expensive upstream work.

Using `collectAsState()` for a `ViewModel`'s primary state flow is a common source of background CPU/battery cost that shows up in Energy Profiler or Android vitals wakeup metrics, not in a foreground jank trace — a reminder that memory/CPU perf issues aren't always visible in frame-timing tools.

---

## 7. Coroutine/Flow perf on Android

- **Dispatcher choice**: `Dispatchers.Main`/`Main.immediate` for UI-state updates and Compose-observed state; `Dispatchers.Default` for CPU-bound work (parsing, diffing, sorting); `Dispatchers.IO` for blocking I/O (disk, network client calls that block a thread). Launching CPU-bound work on `Main` is the coroutine-world equivalent of blocking the UI thread directly.
- **`flowOn`**: switches the *upstream* dispatcher for everything above it in the chain — place it as close to the actual blocking/CPU-bound operator as possible; a `flowOn` placed too high in the chain drags unrelated cheap operators onto the switched dispatcher for no benefit, and each `flowOn` boundary is a real dispatcher-hop cost (see `bolt/reference/kotlin-cheatsheet.md` §12 for the general Flow-chain cost model this section assumes).
- **`conflate()` / `distinctUntilChanged()`**: `conflate()` drops intermediate emissions when the collector is slower than the producer (appropriate for UI state where only the latest value matters); `distinctUntilChanged()` suppresses recomposition-triggering emissions when the new value structurally equals the previous one — cheap insurance against a producer that emits a new instance with identical content every tick.
- **`stateIn` sharing strategy**: `SharingStarted.WhileSubscribed(stopTimeoutMillis)` (commonly `5000`) keeps the upstream `Flow` alive briefly after the last collector unsubscribes, absorbing configuration-change churn without restarting expensive upstream work; `SharingStarted.Eagerly` starts immediately and never stops (appropriate for app-lifetime singletons only); `SharingStarted.Lazily` starts on first subscriber but never stops once started.
- **`repeatOnLifecycle(Lifecycle.State.STARTED)`**: the `Activity`/`Fragment`-side counterpart to `collectAsStateWithLifecycle` for manually-launched collection in a `LaunchedEffect`/coroutine scope outside Compose's own state APIs — restarts collection on each `STARTED` transition, cancels on `STOP`, avoiding both leaked collection and duplicate collectors across configuration changes.
- **Avoiding per-recomposition `LaunchedEffect` restarts**: `LaunchedEffect(key1)` cancels and relaunches its coroutine whenever `key1` changes identity — the most common bug here is passing an unstable key (a freshly-constructed object, a lambda, or a `List` that's a new instance each recomposition with identical content) that appears to change every recomposition even though nothing meaningful changed, causing the effect to restart continuously. Key on a stable, meaningfully-changing value (an ID, not the whole object).

---

## 8. R8/build-side wins that affect runtime

- **R8 full mode** (`android.enableR8.fullMode=true`, default since AGP 8.0) — more aggressive whole-program optimization than "compat mode" R8; enables additional dead-code elimination and inlining that reduces both method count (helps DEX/startup) and runtime overhead from unused code paths. Requires keep rules to be more precise than compat mode tolerates — verify reflection-based libraries (serialization, DI) ship correct consumer ProGuard rules.
- **Resource shrinking** (`isShrinkResources = true`, paired with `isMinifyEnabled = true`) — removes unused resources the code-shrinker's reachability analysis proves unreferenced; reduces APK size, which affects install-time and, indirectly, cold-start disk I/O for resource lookups.
- **Why benchmarking a debug build is meaningless**: `debuggable = true` disables ART's release-path optimizations, adds JIT/debugger-hook overhead, and disables/alters some Compose compiler optimizations gated on `isDebug`. A debug-build benchmark measures debugger overhead, not user-facing performance, and a debug-build "improvement" can regress in release or vice versa. The Baseline Profile Gradle plugin's generated `benchmark` build type exists precisely to avoid this trap — it mirrors `release` (minified, shrunk, non-debuggable) while using a debug signing config so no production keystore is required locally. Always benchmark against `benchmark`, never `debug`.

---

## 9. Field telemetry

### 9.1 Play Console Android vitals

**User-perceived ANR rate** / **ANR rate** / **multiple-ANR rate** — percentage of daily active users experiencing at least one (or, for multiple-ANR, at least two) ANRs; Play defines an overall bad-behavior threshold (0.47% of DAU) and a per-device-model threshold (8% of DAU on that model) that affect store visibility. **Slow rendering** (`developer.android.com/topic/performance/vitals/render`) covers **excessive slow frames** (rendered below target refresh rate) and **excessive frozen frames** (>0.1% of a session's frames taking >700ms — the "app appears stuck" signal); only available for standard UI Toolkit rendering (Canvas/View hierarchy, which Compose uses), not Vulkan/Unity/Unreal/OpenGL surfaces. **Slow Sessions** is a games-only vitals metric, not applicable to a typical Compose business app.

### 9.2 Firebase Performance + custom Perfetto traces + CI perf gates

Firebase Performance Monitoring gives automatic screen-rendering traces (slow/frozen frame counts per screen) plus custom traces/metrics — the production-telemetry counterpart to local Macrobenchmark runs, aggregated across the real user population rather than a CI device farm. `androidx.tracing.trace { }` spans (§2.6) captured via `adb shell perfetto` in a scripted test add app-specific named intervals for correlating a business operation with a frame-timing regression. Treat cold-start / frame-percentile / memory-footprint targets as **CI gates**, not aspirational docs: a Macrobenchmark test that runs on every PR/release build and fails when `StartupTimingMetric`/`FrameTimingMetric` regresses past a checked-in baseline is the only reliable way to prevent silent perf drift. Run against the `benchmark` build type (§8) on a consistent device/emulator profile to keep CI noise low enough for the gate to be meaningful.

---

## 10. Anti-pattern table

| Signal | Why it bites | Fix |
|--------|--------------|-----|
| `List`/`Set`/`Map` in a `@Composable` parameter list assumed to break skipping | Under Strong Skipping this is often fine by reference — the 2026 default policy changed (§3.4) | Verify via Compose Compiler Report before reflexively wrapping in `ImmutableList` |
| Reading `State` directly in Composition for a value that only affects Layout/Draw (`Modifier.offset(x)`) | Forces full Composition on every animation/scroll tick | Lambda-deferred read: `Modifier.offset { }` / `graphicsLayer { }` |
| Missing `key` in `LazyColumn`/`LazyRow` `items` | Positional recomposition leaks row state across insert/reorder/delete | `items(list, key = { it.id })` |
| Missing `contentType` in a heterogeneous lazy list | Forces slot discard/reinflate instead of reuse when scrolling across item-type boundaries | `items(list, contentType = { it.type })` |
| Bare `remember { }` computing from a changing parameter | Value never recomputes even as inputs change — stale-data bug, not just perf | `remember(key) { ... }` |
| `LaunchedEffect` keyed on an unstable object/lambda/new-instance-list | Effect restarts every recomposition even when nothing meaningful changed | Key on a stable ID/primitive |
| `BitmapFactory.decodeStream` / synchronous decode inside a composable or unstructured coroutine | Main-thread block, or off-main but still full-resolution decode | Coil `AsyncImage` (off-main, request-scaled decode) |
| `collectAsState()` on a `ViewModel`'s primary `StateFlow` | Keeps collecting (and upstream work running) while backgrounded | `collectAsStateWithLifecycle()` |
| Benchmarking a `debug` build type | Debuggable overhead invalidates the measurement | Benchmark against the generated `benchmark` build type |
| Non-critical SDK init synchronous in `Application.onCreate` | Extends pre-first-frame cold-start window | Defer to post-first-frame via `androidx.startup` or explicit post-`onResume` dispatch |
| `@Immutable`/`@Stable` applied to a type that doesn't actually satisfy the contract | Silent stale-UI bugs — Compose trusts the annotation, doesn't verify it | Only annotate types that provably satisfy the promise |
| `graphicsLayer { }` reading a business-logic-frequency (not animation-frequency) state value | Draws every business-logic update at Draw-phase cost, forfeiting the skip benefit `graphicsLayer` exists for | Reserve `graphicsLayer`'s lambda form for genuinely animation/frame-scoped values |

---

## 11. Routing rules

| Situation | Route to | Why |
|-----------|----------|-----|
| Compose recomposition/render/diffing perf, startup/frame/memory on Android | **Native** (this file) | Platform- and framework-specific measurement + fix |
| Kotlin/JVM language-level perf: coroutine/Flow cost model beyond the UI-collection topics here, bytecode growth from the Compose compiler at a JVM level, generic algorithmic Kotlin perf | **Bolt** (`bolt/reference/kotlin-cheatsheet.md`) | Language/runtime level, not Compose-runtime-specific |
| Slow SQL query / Room DAO query plan / index design feeding a `LazyColumn` | **Tuner** (query/index layer) → Native consumes the result | Query plan optimization is Tuner's domain; Native owns the render-side consumption |
| SLO/alerting on field ANR rate, slow/frozen frame rate, or startup-time regressions over time; dashboarding Firebase Performance / Android vitals aggregates | **Beacon** | Observability/SLO design, not one-off measurement |
| "This got slower sometime in the last N releases, bisect it" | **Trail** | Git-history/regression bisection is Trail's domain; Native supplies the metric to bisect against |
| New feature scaffolding that happens to need offline/persistence design | **Native** `offline` Recipe (`reference/patterns.md`) | Architecture decision, not a perf regression |

---

## Sources

- [Compose Compiler Gradle plugin — Android Developers](https://developer.android.com/develop/ui/compose/compiler) (2026)
- [Compose compiler options DSL — Kotlin Documentation](https://kotlinlang.org/docs/compose-compiler-options.html)
- [`metricsDestination` / `reportsDestination` — Kotlin Gradle Plugin API](https://kotlinlang.org/api/kotlin-gradle-plugin/compose-compiler-gradle-plugin/org.jetbrains.kotlin.compose.compiler.gradle/-compose-compiler-gradle-plugin-extension/)
- [`StrongSkipping` feature flag — Kotlin Gradle Plugin API](https://kotlinlang.org/api/kotlin-gradle-plugin/compose-compiler-gradle-plugin/org.jetbrains.kotlin.compose.compiler.gradle/-compose-feature-flag/-companion/-strong-skipping.html)
- [Write a Macrobenchmark — Android Developers](https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview)
- [Capture Macrobenchmark metrics — Android Developers](https://developer.android.com/topic/performance/benchmarking/macrobenchmark-metrics)
- [Baseline Profiles overview — Android Developers](https://developer.android.com/topic/performance/baselineprofiles/overview)
- [Create Baseline Profiles — Android Developers](https://developer.android.com/topic/performance/baselineprofiles/create-baselineprofile)
- [Difference between Baseline Profiles and Startup Profiles — Android Developers](https://developer.android.com/topic/performance/baselineprofiles/difference-baseline-startup)
- [JankStats Library — Android Developers](https://developer.android.com/topic/performance/jankstats)
- [In-process tracing — Android Developers](https://developer.android.com/topic/performance/tracing/in-process-tracing)
- [Composition tracing — Android Developers](https://developer.android.com/develop/ui/compose/tooling/tracing)
- [ATrace: Android system and app trace events — Perfetto Docs](https://perfetto.dev/docs/data-sources/atrace)
- [Slow rendering — Android Developers (Android vitals)](https://developer.android.com/topic/performance/vitals/render)
- [ANRs — Android Developers (Android vitals)](https://developer.android.com/topic/performance/vitals/anr)
- [State and Jetpack Compose (`collectAsStateWithLifecycle`) — Android Developers](https://developer.android.com/develop/ui/compose/state)
- [Enable app optimization with R8 — Android Developers](https://developer.android.com/studio/build/shrink-code)
- Source of truth: [`bolt/reference/kotlin-cheatsheet.md`](../../bolt/reference/kotlin-cheatsheet.md), [`reference/modern-stack.md`](modern-stack.md), [`reference/patterns.md`](patterns.md), [`reference/adb-cli.md`](adb-cli.md)
