# Modern Native Stack Reference (2026)

**Purpose:** Latest stack reference for pure-native iOS Swift + Android Kotlin.
**Read when:** Setting up a new project, modernizing an existing project, deciding on `@Observable` / Swift 6.3 / Compose Strong Skipping / Type-safe Navigation / Liquid Glass / Material 3 Expressive adoption.

> Out of scope: React Native, Flutter, Kotlin Multiplatform, Compose Multiplatform. Pure-native only.

---

## iOS — Swift 6.3 / SwiftUI / iOS 26

### Observation framework — `@Observable` (2026 default)

The `@Observable` macro introduced in Swift 5.9+ / iOS 17+ replaces the `ObservableObject + @Published` pattern as the standard. Property-level tracking means only properties actually read inside `body` trigger re-evaluation.

```swift
// Before (legacy)
final class CartViewModel: ObservableObject {
    @Published var items: [CartItem] = []
    @Published var isLoading = false
}

// 2026 default
@Observable
@MainActor
final class CartViewModel {
    private(set) var items: [CartItem] = []
    private(set) var isLoading = false
    @ObservationIgnored private var token: String?  // not tracked

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }
        items = (try? await CartService.shared.fetchItems()) ?? []
    }
}
```

Pitfalls:
- Declare `@State private var model = MyModel()` **once at the top-level View** instead of `@StateObject`. If a child View re-declares it with `@State`, it is re-initialized every render.
- Migrate from `@EnvironmentObject` to `@Environment(MyModel.self)` (becomes Optional, eliminating injection-missing crashes).
- Use `@ObservationIgnored` to exclude caches, tokens, and other properties not tied to View updates.

### Swift 6.2 Approachable Concurrency (Xcode 26)

`Complete Concurrency Checking` is the default in Swift 6.0. Swift 6.2 introduces **Default Actor Isolation = MainActor** as the default for new Xcode 26 projects, plus two new compiler defaults: `infer isolated conformances` and `nonisolated(nonsending)` enforcement.

Key behavior change: **non-isolated async functions inherit the caller's isolation by default** in Swift 6.2 — a function called from `@MainActor` stays on the main actor unless explicitly opted out.

```swift
// Swift 6.2: implicitly @MainActor unless @concurrent
final class HomeViewModel {  // implicit @MainActor
    private(set) var feed: [Post] = []

    @concurrent  // explicitly run in background, off the main actor
    private func decode(_ data: Data) async throws -> [Post] {
        return try JSONDecoder().decode([Post].self, from: data)
    }

    func load() async throws {
        let data = try await fetcher.get()
        feed = try await decode(data)  // background hop, then back to MainActor
    }
}
```

| Pattern | Use |
|---------|-----|
| (default `@MainActor`) | UI-driven ViewModel / Repository |
| `@concurrent` | Run explicitly in background (Swift 6.2+) — opt out of caller-inherited isolation |
| `nonisolated` | Pure helper that does not touch shared state |
| `actor` | Shared mutable state |
| `Sendable` | Types crossing actor boundaries |
| `Task { [weak self] in }` | Open-ended tasks. Prefer the `.task { }` modifier inside Views |
| `AsyncSequence` | Streams |

**Migration strategy for existing projects:**
- New projects in Xcode 26: Default MainActor isolation is on automatically.
- Existing projects: opt in per target via `-default-isolation MainActor` (build settings) or `defaultIsolation(MainActor.self)` in `Package.swift`.
- Raise `SWIFT_STRICT_CONCURRENCY` from `targeted → complete` per module.
- Swift 6.2 typically cuts strict-concurrency errors by 50%+ thanks to caller-isolation inheritance and implicit MainActor — re-run the migrator before hand-fixing each error.

### SwiftData vs Core Data selection (2026)

SwiftData reached production-ready in 2026 — the relationship and migration regressions from year one are addressed. Still, Core Data is the right choice in several cases.

| Condition | Choice |
|-----------|--------|
| iOS 17+ only / SwiftUI-centric / new project | **SwiftData** (fits 80%+ of new projects) |
| iOS 16 support required | Core Data |
| `NSCompoundPredicate` / `NSFetchedResultsController` / advanced migration | Core Data |
| Large-scale data / strict performance requirements | Core Data (SwiftData still has slow paths in 2026) |
| Migrating an existing Core Data store with custom mappings | Core Data — migrating to SwiftData is high-cost |

Known SwiftData production issues to watch in 2026:
- Optional transformable values only migrate cleanly when the default is `nil` — non-nil defaults still trip the migrator.
- CloudKit + SwiftData schema migration has open edge cases; teams running mixed-environment shops still set up workarounds.
- WWDC25 added no major new features to Core Data nor to Core Data ↔ SwiftData bridging — plan for the bridge layer to stay where it is.

**Recommendation**: For new SwiftUI apps targeting iOS 17+, default to SwiftData. If you depend on CloudKit sync, run an end-to-end migration drill on a representative store before committing.

```swift
// SwiftData (iOS 17+)
@Model
final class Item {
    @Attribute(.unique) var id: UUID
    var name: String
    var createdAt: Date

    init(id: UUID = UUID(), name: String, createdAt: Date = .now) {
        self.id = id
        self.name = name
        self.createdAt = createdAt
    }
}

// View
struct ItemListView: View {
    @Query(sort: \Item.createdAt) private var items: [Item]
    @Environment(\.modelContext) private var context

    var body: some View {
        List(items) { Text($0.name) }
    }
}
```

### Navigation — `NavigationStack` (iOS 16+)

```swift
@Observable
final class HomeCoordinator {
    var path = NavigationPath()

    func openProduct(_ id: String) { path.append(Route.product(id)) }
}

enum Route: Hashable {
    case product(String)
    case cart
}

struct HomeRoot: View {
    @State private var coordinator = HomeCoordinator()

    var body: some View {
        NavigationStack(path: $coordinator.path) {
            HomeView()
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .product(let id): ProductDetailView(id: id)
                    case .cart: CartView()
                    }
                }
        }
        .environment(coordinator)
    }
}
```

**Forbidden pattern:** Do not put `NavigationSplitView` inside a `NavigationStack` (regression bug still known on iOS 18). `NavigationSplitView` belongs at the top, with `NavigationStack` nested inside it.

### Liquid Glass (iOS 26 / WWDC25)

The largest visual redesign since iOS 7, introduced in iOS 26 / iPadOS 26 / macOS Tahoe / watchOS / tvOS 26.

| Element | Description |
|---------|-------------|
| Liquid Glass material | Real-time translucent / reflective / refractive material applied to controls, navigation, widgets, icons |
| Dynamic tab-bar shrink | Tab bar shrinks on scroll, expands on stop — standard behavior |
| 4-variant icons | Must provide light / dark / **tinted** / **clear** variants. Apple ships the Icon Composer tool |
| Lock screen content | Subjects dynamically tuck behind UI for depth |
| New SwiftUI APIs | `glassEffect()` modifier, `GlassEffectContainer` for grouped views, hardware-aware corner radii |

```swift
// SwiftUI: apply Liquid Glass material
struct CardView: View {
    var body: some View {
        VStack { Text("Card") }
            .padding()
            .glassEffect()  // Liquid Glass material
    }
}

// Group multiple glass elements for coordinated animations
GlassEffectContainer {
    CardView()
    ActionButton()
}
```

**Auto-adoption**: Recompiling an existing SwiftUI app with Xcode 26 gives standard navigation bars, tab bars, and toolbars Liquid Glass automatically — no code changes required for native controls.

Adoption policy:
- iOS 26 target → Liquid Glass by default, verify legibility (translucency must keep contrast)
- iOS 17 / 18 target → Standard SwiftUI; ensure no breakage on iOS 26 devices when material renders
- iOS 27 (next major) **removes the opt-out** — full adoption is required, not optional. Plan migration before the iOS 27 cycle
- From **2026-04-28** all App Store submissions require Xcode 26 + iOS 26 SDK
- Do not bring transparency-dependent designs back to iOS 17 / 18 deployment targets

### New surfaces on iOS 18 / iOS 26

- **Control Center API** — `ControlWidgetToggle`, `AppIntentControlValueProvider` to add toggles / value providers to Control Center / Lock Screen / Action Button
- **Live Activities + Dynamic Island** — `ActivityKit` / max 8h active + 4h stale / payload ~4KB / APNs `apns-priority` 5 recommended. Advertising / marketing copy is forbidden
- **App Intents + Apple Intelligence** — Surfaces in Spotlight / Siri / Action Button. Use `opensAppWhenRun = false` for "answer without opening the app" UX
- **Foundation Models framework** — On-device ~3B quantized + Private Cloud Compute fallback. The primary uplift opportunity for Web→Native migrations

### Core principles (recap)

`Clarity / Deference / Depth / Consistency`. In the Liquid Glass era, **Deference (yielding to content)** is reinforced.

---

## Android — Kotlin 2.4+ / Jetpack Compose / Material 3 Expressive

### Kotlin 2.x (K2 compiler default)

- 2.0 makes K2 the default. 2.1.20+ ships full default-argument support for abstract `@Composable` functions.
- 2.2 ships **Context Parameters** in beta (replacement for Context Receivers, named and explicit).
- IntelliJ 2025.1 makes K2 the default — compile times drop by 40%+.

### Jetpack Compose best practices (2026)

#### Type-Safe Navigation (Navigation 2.8+)

```kotlin
@Serializable data object Home
@Serializable data class Profile(val userId: String)
@Serializable data class Cart(val showCheckout: Boolean = false)

NavHost(navController, startDestination = Home) {
  composable<Home> { HomeScreen(onUserClick = { navController.navigate(Profile(it)) }) }
  composable<Profile> { backStack ->
    val args: Profile = backStack.toRoute()
    ProfileScreen(args.userId)
  }
  composable<Cart> { backStack -> CartScreen(backStack.toRoute<Cart>()) }
}
```

Hand-written string routes (`"home"`) are legacy. Use `@Serializable` data class / data object for compile-time type checks.

#### Stable Types & Strong Skipping Mode (2026 update)

Compose Compiler 1.5.4+ ships **Strong Skipping Mode** as the default. With it on, all restartable composables become skippable, and the runtime compares **unstable** parameters by **instance reference (`===`)** before re-executing the composable.

**Important 2026 best-practice shift**: The old advice "always wrap collections in `ImmutableList`" is no longer the default recommendation.

- Strong Skipping does NOT change a type's stability — `List`, `Set`, `Map` remain unstable. It changes how the **runtime** handles unstable parameters: it compares by reference and skips when the same instance is passed.
- `kotlinx.collections.immutable` `ImmutableList` / `PersistentList` is **stable** and uses `equals()`. For lists this is `O(N)`, so for large feeds the comparison plus the conversion cost can be net-negative versus passing the original `List` by reference.
- Today's guidance: pass `List<T>` straight from your data source. Reach for `ImmutableList` only when (a) you have measured a real recomposition problem in Compose Compiler Reports, AND (b) the producer can hand back the same instance when nothing changed.

Still recommended:

- Wrap data classes that look stable but contain unstable types with `@Immutable`.
- Lambdas inside LazyListScope `items` are not in composable scope — wrap them with `remember(key) { ... }` to stop fresh allocation per frame.
- Do not generate new instances with identical content every frame from `ViewModel` state. Reuse the previous list / data class when nothing changed.

```kotlin
// OK in 2026 — Strong Skipping handles `List` by referential equality
data class FeedUiState(
    val items: List<Post> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
)

// Still useful when the producer might return new instances of equal content,
// or for type-safety / immutability contracts
@Immutable
data class FeedSnapshot(val items: ImmutableList<Post>)
```

Validate stability with the Compose Compiler Report — `kotlinc -P plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=...` — before optimizing further.

#### Coroutines + Flow (UI side)

- **`collectAsStateWithLifecycle()`** is mandatory (stops collection across Lifecycle changes).
- **StateFlow**: persistent UI state.
- **SharedFlow**: one-shot events (Navigation, Snackbar, real-time notifications). Default `replay = 0, BufferOverflow.DROP_OLDEST`.

```kotlin
class HomeViewModel : ViewModel() {
    private val _ui = MutableStateFlow(FeedUiState(persistentListOf()))
    val ui: StateFlow<FeedUiState> = _ui.asStateFlow()

    private val _events = MutableSharedFlow<Event>(replay = 0)
    val events: SharedFlow<Event> = _events.asSharedFlow()
}
```

### Architecture (2026)

| Pattern | Where it fits |
|---------|--------------|
| **MVVM** (Now in Android style) | Mid-size / standard screens. Aggregate state into a single sealed/data `UiState` |
| **MVI / Reducer** | Screens with high state complexity (forms, real-time editing) |
| **MV** (pattern) | Small to medium scope where the View consumes an `@Observable` model directly (mirrors the SwiftUI side) |

Do not hold Compose state in the ViewModel. View → ViewModel back-references leak. Expose a `StateFlow<UiState>` only.

### DI (2026)

| Item | Hilt | Koin |
|------|------|------|
| Resolution | Compile time | Runtime |
| Error detection | Compile time | Runtime |
| Best fit | Large / multi-module / enterprise | Small to medium / fast startup |
| Jetpack integration | Official ViewModel / WorkManager support | Community |

### Material 3 Expressive (announced 2025-05)

New components (all available in Compose Material 3 and Material 3 Adaptive 1.2+):

- **LoadingIndicator / ContainedLoadingIndicator** — For waits under 5s, morphs through 7 shapes via the `polygons` parameter. Indeterminate `CircularProgressIndicator` is legacy.
- **PullToRefreshBox** — Official Material 3 component for pull-to-refresh.
- **FloatingToolbar / DockedToolbar** — `BottomAppBar` is deprecated. `FloatingToolbar` supports horizontal and vertical orientations and pairs with a FAB. `FloatingToolbarScrollBehavior` controls hide / shrink on scroll for a clean look.
- **Carousel** — Image / video collections.
- **Shape Library** — 35 new shapes + shape morphing + variable fonts.
- **NavigationSuiteScaffold** — Adaptive primary navigation that switches between bottom bar (compact), navigation rail (medium), and navigation drawer (expanded) based on `WindowSizeClass`. Default for new adaptive apps.
- **ListDetailPaneScaffold / SupportingPaneScaffold / ThreePaneScaffold** — Multi-pane layouts for tablets, foldables, and desktop windows.

**Physics-based spring motion engine** delivers natural feedback for dismissals, shape morphing, and predictive back.

```kotlin
@Composable
fun AdaptiveNav() {
    val info = currentWindowAdaptiveInfo()
    NavigationSuiteScaffold(
        navigationSuiteItems = {
            item(selected = true, onClick = { }, icon = { Icon(Icons.Default.Home, null) }, label = { Text("Home") })
            item(selected = false, onClick = { }, icon = { Icon(Icons.Default.Search, null) }, label = { Text("Search") })
        },
    ) {
        // Content; Suite picks bar / rail / drawer for you
    }
}
```

### Dynamic Color (API 31+)

```kotlin
@Composable
fun AppTheme(
    dynamicColor: Boolean = true,  // Material You
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            if (isSystemInDarkTheme()) dynamicDarkColorScheme(LocalContext.current)
            else dynamicLightColorScheme(LocalContext.current)
        }
        isSystemInDarkTheme() -> darkColorScheme()
        else -> lightColorScheme()
    }
    MaterialTheme(colorScheme = colorScheme, content = content)
}
```

Hard-coded colors are forbidden. Reference semantic tokens such as `MaterialTheme.colorScheme.surface`.

### New Compose features (BOM 2025.05.01+)

- Official Autofill support (autofill hints on TextField)
- Auto-sizing text (font size auto-adjusts to parent container)
- Visibility tracking
- Animate bounds modifier
- Pausable Composition (split work across frames)
- Background text prefetch
- **Navigation 3** (fine-grained back stack control)

### Adaptive Layouts (Window Size Class)

```kotlin
val windowSizeClass = currentWindowAdaptiveInfo(supportLargeAndXLargeWidth = true).windowSizeClass

when (windowSizeClass.windowWidthSizeClass) {
    WindowWidthSizeClass.COMPACT -> SingleColumnLayout()
    WindowWidthSizeClass.MEDIUM -> TwoPaneLayout()
    WindowWidthSizeClass.EXPANDED, WindowWidthSizeClass.LARGE, WindowWidthSizeClass.EXTRA_LARGE -> ThreePaneLayout()
}
```

New classes: **large** / **extra-large** (Compose Adaptive Layouts 1.2+). Supports trifolds / foldables / connected displays.

### Edge-to-Edge (enforced at API 36)

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()  // mandatory at targetSdk 36
        super.onCreate(savedInstanceState)
        setContent {
            // Each screen handles insets via Modifier.windowInsetsPadding() / WindowInsets.systemBars etc.
        }
    }
}
```

`R.attr#windowOptOutEdgeToEdgeEnforcement` is deprecated and inert at API 36.

### Predictive Back (default ON at API 36)

```kotlin
@Composable
fun MyScreen(onBack: () -> Unit) {
    BackHandler(enabled = true) { onBack() }
    // ...
}
```

`onBackPressed()` is no longer dispatched. Use `OnBackPressedDispatcher` (Activity) or Compose `BackHandler`.

### Foreground Service Types (Android 14+)

```xml
<!-- AndroidManifest.xml -->
<service
    android:name=".SyncService"
    android:foregroundServiceType="dataSync" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
```

On API 35+, `dataSync` / `mediaProcessing` are capped at **6 hours per 24 hours**. Starting a foreground service from background is forbidden in principle since API 31+.

### Room 2.7+ (2026)

- Room 2.7+ supports KMP (when needed). Even in pure-native, Room is the Android standard.
- DataStore (Preferences + Proto) is the standard. SharedPreferences is legacy.
- Sensitive data → EncryptedSharedPreferences or Tink-encrypted DataStore + Android Keystore.

### Jetpack Glance (App Widgets)

For new widgets, prefer Glance (Compose runtime). Hand-written RemoteViews are legacy. Battery-optimized and integrated with `PreferencesDataStore`.

---

## OS version / performance baseline (early 2026)

### iOS

| Item | Value |
|------|-------|
| Recommended minimum iOS | **17 (recommended)** / 16 acceptable / 26+ if Liquid Glass / Foundation Models |
| Cold-start target | < 500 ms (flagship) / < 2 s (mid-range) |
| Crash-free sessions | ≥ 99.85% |
| App Bundle ceiling | 4 GB |
| Cellular download cap | 200 MB |
| Xcode + iOS SDK | **Xcode 26 + iOS 26 SDK required from 2026-04-28** |

### Android

| Item | Value |
|------|-------|
| Recommended minimum API | **API 28 (Android 9)** default / API 31+ if Material You / Photo Picker |
| targetSdk (current) | **35 mandatory since 2025-08-31** |
| targetSdk (mandatory) | **36 starting 2026-04** for all new app submissions and updates on Google Play |
| 16KB Page Size | **Required for all submissions starting 2025-11-01**; Google Play **rejects** non-compliant new submissions and updates after **2026-05-31**. Set `useLegacyPackaging = false` in Gradle and rebuild every NDK dep |
| Edge-to-edge enforcement | **API 36 removes the opt-out** — `enableEdgeToEdge()` is mandatory; `R.attr#windowOptOutEdgeToEdgeEnforcement` is deprecated and inert |
| Predictive Back default ON | **API 36** — `KeyEvent.KEYCODE_BACK` no longer dispatched, `onBackPressed()` no longer called. Use `OnBackPressedDispatcher` or Compose `BackHandler` |
| Cold-start target | < 500 ms / Vitals threshold 5s |
| Baseline Profile | 40-50% reduction in production (Meta, Trello, etc.) |
| 16KB performance gain | Launch time -3.16% (up to -30%), power -4.56%, hot start -4.48%, cold start -6.6% |

---

## Library quick reference (2026)

### iOS

| Use | Pick |
|-----|------|
| HTTP | URLSession + async/await (or Alamofire) |
| GraphQL | Apollo iOS (codegen + normalized cache + persisted queries) |
| Image | Kingfisher / SDWebImageSwiftUI / Nuke |
| Logging | OSLog + os_signpost |
| Crash | Firebase Crashlytics / Sentry |
| Analytics | Firebase / Amplitude / Segment |
| Feature Flags | LaunchDarkly / Unleash |

### Android

| Use | Pick |
|-----|------|
| HTTP | Retrofit + OkHttp + Coroutines (or Ktor) |
| GraphQL | Apollo Kotlin (codegen + normalized cache + persisted queries) |
| Image | Coil 3 (Compose-friendly), Glide |
| Logging | Timber + okhttp logging interceptor (debug only) |
| Crash | Firebase Crashlytics / Sentry |
| Analytics | Firebase / Amplitude / Segment |
| Feature Flags | LaunchDarkly / Unleash |

---

## Native Stack Defaults Quick-Reference Table (2026)

| Layer | iOS | Android |
|-------|-----|---------|
| Language | Swift 6.3 (Approachable Concurrency / default MainActor, Xcode 26) | Kotlin 2.4+ (K2 default) |
| UI | SwiftUI + **Liquid Glass** on iOS 26 (`.glassEffect()` chrome only); classic SwiftUI on iOS 17/18 | Compose 1.11 + **Material 3 Expressive** (BOM 2026.05 / M3 1.4+); Strong Skipping default |
| Architecture | MV / MVVM / MVVM-C / TCA; `@Observable` default | MVVM (Now-in-Android) / MVI for complex-state |
| Async | async/await + AsyncSequence + structured concurrency | Coroutines + Flow + `collectAsStateWithLifecycle()` (mandatory) |
| DI | swift-dependencies / Factory / manual composition root | Hilt (enterprise) or Koin (KMP-friendly) |
| Navigation | `NavigationStack` + Coordinator; `NavigationSplitView` for iPad / foldable | Navigation Compose 2.8+ type-safe (Kotlin Serialization) |
| Networking | URLSession + async/await; Apollo iOS (GraphQL Persisted Queries) | Retrofit + OkHttp / Ktor; Apollo Kotlin |
| Persistence | **SwiftData** (iOS 17+, `VersionedSchema` from day one) or Core Data; Keychain + Secure Enclave for secrets | **Room 2.8+** + DataStore; secrets via Tink-encrypted DataStore (EncryptedSharedPreferences deprecated) |
| Auth | **Passkeys (FIDO2) first**: iOS 26 `ASAuthorizationAccountCreationProvider`; iOS 17/18 `ASAuthorizationController`; Sign in with Apple required alongside third-party | **Credential Manager** (Passkey + Password + Sign-in-with-Google); ~15min biometric re-auth |
| Push | APNs + **Live Activities** (ActivityKit) | FCM + **Notification Channels** (mandatory) |
| Deep links | Universal Links (AASA) + scheme fallback | App Links (assetlinks.json); Firebase Dynamic Links retired |
| Biometrics | LocalAuthentication (re-auth only) | BiometricPrompt (re-auth only) |
| Widgets | WidgetKit + iOS 18 Control Center API | **Jetpack Glance** for new widgets |
| AI (on-device) | **Foundation Models** + Apple Intelligence | **ML Kit GenAI APIs** + Gemini Nano (AICore) |
| Adaptive | NavigationSplitView + Window Size Classes | Compose Adaptive 1.2+; WSC (compact/medium/expanded/large/extra-large) |
| Privacy | **`PrivacyInfo.xcprivacy`** Required Reasons API (3rd-party SDKs since 2025-02-12) | **Data Safety form** (all tracks) |
| Build | Xcode 26 + SPM (iOS 26 SDK required 2026-04-28) | Gradle + Kotlin DSL + **AGP 8.5.1+ / NDK r28+**; **16KB native libs required since 2025-11-01** |
| Min-OS / target | iOS 17 default (iOS 16 acceptable) | API 28 default; **targetSdk 36 mandatory by 2026-08-31** (edge-to-edge enforced, predictive back default ON, sw600dp+ forces resizeable) |

---

> Out of scope: React Native, Flutter, Kotlin Multiplatform, Compose Multiplatform. This reference covers pure-native only.
