# Native Architecture Mapping (MAP phase)

Translate the web architecture surfaced in `web-analysis-checklist.md` into **two separate native architectures** — one for iOS, one for Android. The mapping is per-screen and per-feature. Never produce a single unified spec.

---

## Default Architectures

### iOS — SwiftUI + MVVM-C

```
[ App ]
  └─ Composition Root (DI container)
      ├─ Coordinator(s)            ← navigation
      │    ├─ Tab / Stack / Sheet drivers
      │    └─ Deep-link router
      ├─ Feature Modules
      │    ├─ View (SwiftUI)
      │    ├─ ViewModel (@Observable, async/await)
      │    ├─ UseCase (pure async functions)
      │    └─ Repository (protocol + impl)
      ├─ Services
      │    ├─ APIClient (URLSession + async/await)
      │    ├─ AuthService (ASWebAuthenticationSession + Keychain)
      │    ├─ Storage (SwiftData / Core Data / FileManager)
      │    └─ Push, Analytics, Logger, FeatureFlags
      └─ Design System (Tokens, Components)
```

**Why MVVM-C:**
- SwiftUI is declarative; the View needs a thin observable VM that drives state.
- Coordinators centralize navigation so deep links, programmatic flows, and modal sheets stay testable.
- `@Observable` (Swift 5.9+) replaces `ObservableObject` boilerplate; pair with `@Bindable` in the View.

### Android — Jetpack Compose + MVVM (or MVI for high-state-complexity screens)

```
[ App ]
  └─ Application + DI (Hilt)
      ├─ NavHost (Navigation Compose, type-safe routes)
      │    └─ Deep-link handler (App Links)
      ├─ Feature Modules
      │    ├─ Screen Composable (UiState in, events out)
      │    ├─ ViewModel (StateFlow<UiState>)
      │    ├─ UseCase (suspend / Flow)
      │    └─ Repository (interface + impl)
      ├─ Services
      │    ├─ Network (Ktor or Retrofit + OkHttp)
      │    ├─ Auth (AppAuth + Custom Tabs + EncryptedSharedPreferences)
      │    ├─ Storage (Room + DataStore)
      │    └─ Push, Analytics, Logger, FeatureFlags
      └─ Design System (Material 3 theme, Tokens, Components)
```

**Why MVVM with single UiState:**
- Compose recomposes on state change; a single `StateFlow<UiState>` per screen avoids torn renders.
- MVI is justified when a screen has many discrete intents (e.g., complex forms, real-time editor) — use a `Reducer<UiState, Intent>` pattern.

---

## Per-Screen Mapping Template

For every web route, produce one row of this table. Treat the table as the canonical handoff to `Native`.

| Web route | Auth-gated | Render mode | iOS screen (SwiftUI View + VM + Coordinator entry) | Android screen (Composable + ViewModel + NavGraph entry) | Notes |
|-----------|-----------|-------------|-----|-----|-------|
| `/` | No | CSR | `HomeView` + `HomeViewModel` (root tab `Home`) | `HomeScreen` + `HomeViewModel` (start destination) | — |
| `/products/[id]` | No | SSR → CSR | `ProductDetailView` + `ProductDetailViewModel` (push from Home) | `ProductDetailScreen` + `ProductDetailViewModel` (nav arg `id: String`) | Image-heavy; pre-warm cache |
| `/cart` | Yes | CSR | `CartView` + `CartViewModel` (modal sheet) | `CartScreen` + `CartViewModel` (top-level destination) | Tab on Android, sheet on iOS — divergence intentional |
| `/checkout/*` | Yes | CSR | `CheckoutCoordinator` (multi-step flow) | `CheckoutGraph` (nested NavGraph) | IAP / Apple Pay / Google Pay branch |

> Divergence is fine. Document it. The web app's IA is not the source of truth — platform conventions are.

---

## Navigation Translation

| Web pattern | iOS pattern | Android pattern |
|-------------|-------------|-----------------|
| Top-level tabs (header nav) | `TabView` (3-5 tabs) | `NavigationBar` (Material 3, 3-5 destinations) |
| Sidebar / hamburger drawer | `NavigationSplitView` (iPad) / `Menu` button (iPhone) | `ModalNavigationDrawer` |
| Linear flow (onboarding, signup) | `NavigationStack` push | `NavController` push |
| Modal dialog | `.sheet` / `.fullScreenCover` | `ModalBottomSheet` / `Dialog` |
| Inline edit-in-place | Sheet or detail push | Bottom sheet or detail push |
| Browser back button | Swipe-back / nav-back, `dismiss` env | System back, `popBackStack()` |
| URL as deep link | Universal Links (AASA) → router | App Links (assetlinks.json) → router |
| Persistent left nav (desktop) | `NavigationSplitView` columns (iPad/Mac) | Adaptive layout: `NavigationRail` (large screens) |
| Tabs that change URL | Tab + per-tab nested `NavigationStack` (each tab keeps its own stack) | Multiple top-level back stacks (Compose NavHost supports this) |
| Modal route (`/settings` opens over `/`) | `.sheet` or full-screen cover | Top-level destination or bottom sheet |

> **Anti-pattern:** Mapping a 5-level web breadcrumb directly to a 5-deep stack. Re-conceive as 1-2 levels max with content denormalization.

---

## State Management Translation

| Web pattern | iOS pattern | Android pattern |
|-------------|-------------|-----------------|
| Global Redux / Pinia store with > 10 slices | Per-feature ViewModels + a small `AppState` for cross-cut (auth, theme, network) | Per-feature ViewModels + `appState: StateFlow<AppState>` |
| `useState` / `useReducer` local | `@State` / `@Observable` VM properties | `var state by mutableStateOf` / VM `MutableStateFlow` |
| Server-state cache (`react-query`) | Repository + actor-isolated cache + `AsyncSequence` | Repository + Flow + Room cache as source of truth |
| Form state (`react-hook-form`) | Per-form `@Observable FormViewModel` with `@Validated` properties | Per-form ViewModel + `StateFlow<FormState>` + Compose validation |
| Optimistic UI | VM applies optimistic state → repository commits → rollback on failure | VM emits optimistic UiState → use case commits → rollback on failure |
| Cross-tab sync (`BroadcastChannel`) | N/A — not portable; use server push + local DB | N/A — same |
| URL-as-state | Decode at deep-link arrival, never as ongoing source | Decode at NavArgs, never ongoing |

> **Critical:** Do not port a 30-slice Redux store as one giant `AppState`. Decompose into feature ViewModels. Cross-cutting state (current user, theme, network) belongs in a small shared `AppState`.

---

## Data Fetching Translation

| Web | iOS | Android |
|-----|-----|---------|
| `fetch` / `axios` | URLSession + `async/await` (or Alamofire) | Ktor or Retrofit + OkHttp |
| Apollo Client (GraphQL) | Apollo iOS (codegen + normalized cache) | Apollo Kotlin (codegen + normalized cache) |
| `react-query` cache | Repository pattern + actor-isolated cache + memory + disk tiers | Repository pattern + Room as single source of truth + memory cache |
| WebSocket | URLSessionWebSocketTask (or Starscream) | OkHttp WebSocket / Ktor WebSocket |
| SSE | EventSource via URLSession streams | OkHttp / custom SSE client |
| Service Worker offline cache | URLCache + per-feature offline tier (T1+) | OkHttp cache + Room (T1+) |

Cache invalidation: model your repository tiers explicitly — **memory → disk → network** with TTLs. Web `react-query` defaults (5 min stale time) are reasonable starting values.

---

## Module Decomposition

### iOS (Swift Package Manager)

```
Packages/
  AppCore/              ← cross-cutting: networking, auth, design tokens, logger
  Features/
    Home/               ← View + VM + UseCase + Repository
    ProductDetail/
    Cart/
    Checkout/
    Account/
  DesignSystem/         ← tokens, components, icons
App/
  iOSApp/               ← composition root, AppDelegate, entitlements
```

### Android (Gradle multi-module)

```
:app                    ← composition root, manifest, DI graph
:core
  :core:network
  :core:auth
  :core:database
  :core:designsystem
  :core:common
:feature
  :feature:home
  :feature:productdetail
  :feature:cart
  :feature:checkout
  :feature:account
```

> Mirror the web feature folders only when they map cleanly. If the web app is organized by route and the natural mobile organization is by feature domain, **regroup**. Architecture mapping is a re-conception, not a copy.

---

## Concurrency Model

| iOS | Android |
|-----|---------|
| `async/await`, `Task`, structured concurrency | `suspend` functions, `CoroutineScope` (`viewModelScope`) |
| `actor` for shared mutable state | `Mutex` / `StateFlow` for shared mutable state |
| `AsyncSequence` for streams | `Flow` for streams |
| `@MainActor` for UI-bound state | `Dispatchers.Main` (Compose enforces this for state writes) |
| Avoid GCD (`DispatchQueue`) in new code; use Swift Concurrency | Avoid `Thread`, `AsyncTask`; use Coroutines |

Swift 6 strict concurrency is the default. **Swift 6.2 + Xcode 26** ship **Approachable Concurrency** (`SWIFT_APPROACHABLE_CONCURRENCY=YES`): new projects default to **MainActor isolation for all code** and `NonisolatedNonsendingByDefault` lets `nonisolated async` functions inherit the caller's isolation — fewer `Sendable` boundary errors. Opt into background execution with `@concurrent` / explicit `nonisolated`. Annotate boundaries with `@MainActor` or `Sendable` correctly; do not silence concurrency warnings.

Kotlin 2.2.20 + K2 is the 2026 baseline. JetBrains' coming Swift export work for KMP coroutines + flows is in active development; track for downstream impact on iOS interop.

---

## Dependency Injection

| iOS | Android |
|-----|---------|
| Composition root: `@main` `App` struct + `Container` | Hilt `@HiltAndroidApp`, `@Module`, `@Provides` |
| Lightweight option: `swift-dependencies` (`@Dependency`) | Lightweight option: Koin (better for KMP shared modules) |
| Test seams: protocol-based abstractions, in-memory fakes | Test seams: interfaces, fakes, `@TestInstallIn` modules |

---

## OS Baseline Decision

| Baseline | Rationale | Trade-off |
|----------|-----------|-----------|
| iOS 17+ | SwiftData, `@Observable`, latest SwiftUI APIs | Excludes ~10-15% of users at release time |
| iOS 16+ (default) | Broad coverage, NavigationStack stable, async/await stable | Use Core Data instead of SwiftData; use `ObservableObject` if needed |
| iOS 15+ | Wider coverage | Substantial `NavigationView` workarounds; not recommended |
| API 34+ (Android 14) | Latest behaviors, predictive back, photo picker stable | Excludes most active users |
| API 28+ (Android 9, default) | ~98% device coverage | Some Material 3 features need polyfills |
| API 24+ (Android 7) | Maximum coverage | Outdated Java time APIs, Kotlin coroutines older patterns |

Pick a baseline at MAP phase, justify it from the survey (especially if web analytics show a long-tail of older devices), and document.

---

## MAP Output Skeleton

```markdown
# Native Architecture Map: <App Name>

## iOS Architecture
- Pattern: SwiftUI + MVVM-C
- Min iOS: 16
- DI: …
- Module layout: …

## Android Architecture
- Pattern: Compose + MVVM (or MVI per screen)
- Min API: 28
- DI: Hilt
- Module layout: …

## Per-screen mapping
| Web route | iOS | Android | Notes |
| …         | …   | …       | …     |

## Navigation translation
- Tabs: …
- Modals: …
- Deep links: …

## State translation
- Global → per-feature VMs: …
- AppState (cross-cut): …
- Form state: …

## Data fetching
- iOS client: …
- Android client: …
- Cache tiers: memory / disk / network

## Concurrency
- iOS: Swift 6 strict
- Android: Coroutines + Flow

## OS baseline rationale
- iOS NN because …
- API NN because …
```

This map feeds `BLUEPRINT` and `HANDOFF`.
