# Pure-Native Mobile Patterns (iOS Swift / Android Kotlin)

**Purpose:** Pure-native navigation, state management, offline, and platform adaptation patterns.
**Read when:** Adopting standard SwiftUI / Compose patterns.

---

## Navigation Patterns

> For version compatibility, migration notes, and the `NavigationSplitView` regression on iOS 18, see `modern-stack.md` § Navigation — `NavigationStack` (iOS 16+) and § Type-Safe Navigation (Navigation 2.8+).

### iOS — `NavigationStack` + Coordinator

```swift
@Observable
final class HomeCoordinator {
    var path = NavigationPath()
    func openProfile(_ userId: String) { path.append(Route.profile(userId)) }
    func openSettings() { path.append(Route.settings) }
}

enum Route: Hashable {
    case profile(String)
    case settings
}

struct ContentView: View {
    @State private var coordinator = HomeCoordinator()

    var body: some View {
        NavigationStack(path: $coordinator.path) {
            HomeView()
                .navigationDestination(for: Route.self) { route in
                    switch route {
                    case .profile(let id): ProfileView(userId: id)
                    case .settings: SettingsView()
                    }
                }
        }
        .environment(coordinator)
    }
}
```

### Android — Navigation Compose 2.8+ (type-safe)

```kotlin
@Serializable data object Home
@Serializable data class Profile(val userId: String)
@Serializable data object Settings

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = Home) {
        composable<Home> {
            HomeScreen(
                onProfileClick = { navController.navigate(Profile(it)) },
                onSettingsClick = { navController.navigate(Settings) },
            )
        }
        composable<Profile> { backStack ->
            val args: Profile = backStack.toRoute()
            ProfileScreen(args.userId)
        }
        composable<Settings> { SettingsScreen() }
    }
}
```

---

## Deep Link Configuration

### iOS — Universal Links (AASA)

Add `applinks:example.com` under `Signing & Capabilities → Associated Domains`. Host `https://example.com/.well-known/apple-app-site-association` on the server:

```json
{
  "applinks": {
    "details": [{
      "appIDs": ["TEAM_ID.com.example.app"],
      "components": [{ "/": "/profile/*" }, { "/": "/settings" }]
    }]
  }
}
```

```swift
struct ContentView: View {
    @State private var coordinator = HomeCoordinator()

    var body: some View {
        NavigationStack(path: $coordinator.path) { ... }
            .onOpenURL { url in coordinator.handle(url) }
    }
}

extension HomeCoordinator {
    func handle(_ url: URL) {
        // /profile/123 → path.append(.profile("123"))
    }
}
```

Custom schemes (`myapp://`) are fallback only. Make Universal Links the primary path.

### Android — App Links (assetlinks.json)

`AndroidManifest.xml`:

```xml
<activity android:name=".MainActivity">
    <intent-filter android:autoVerify="true">
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="https" android:host="example.com" />
    </intent-filter>
</activity>
```

Host `https://example.com/.well-known/assetlinks.json` on the server:

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.app",
    "sha256_cert_fingerprints": ["SHA256:..."]
  }
}]
```

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        intent?.data?.let { handleDeepLink(it) }
        setContent { /* ... */ }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        intent.data?.let { handleDeepLink(it) }
    }
}
```

> **Firebase Dynamic Links was retired in 2025**. Operate AASA / assetlinks.json directly. If attribution is required, adopt Branch / AppsFlyer / Adjust as your MMP.

---

## State Management Patterns

> For `@Observable` migration from `ObservableObject`, Swift 6.2 caller-isolation, Strong Skipping Mode stability rules, and `ImmutableList` guidance, see `modern-stack.md` § Observation framework — `@Observable` and § Stable Types & Strong Skipping Mode.

### iOS — `@Observable` + per-feature ViewModel

```swift
@Observable
@MainActor
final class CartViewModel {
    private(set) var items: [CartItem] = []
    private(set) var isLoading = false
    private(set) var error: Error?

    private let repository: CartRepository

    init(repository: CartRepository) { self.repository = repository }

    func load() async {
        isLoading = true
        defer { isLoading = false }
        do {
            items = try await repository.fetchCart()
        } catch {
            self.error = error
        }
    }

    func add(_ item: CartItem) async {
        items.append(item)  // optimistic
        do {
            try await repository.addItem(item)
        } catch {
            items.removeAll { $0.id == item.id }  // rollback
            self.error = error
        }
    }
}

struct CartView: View {
    @State private var viewModel: CartViewModel

    init(repository: CartRepository) {
        _viewModel = State(initialValue: CartViewModel(repository: repository))
    }

    var body: some View {
        List(viewModel.items) { item in CartItemRow(item: item) }
            .task { await viewModel.load() }
    }
}
```

Cross-cutting state (auth, theme, network) goes through `@Environment` or a DI container. Do not pile 10+ slices into a global store.

### Android — `StateFlow<UiState>` + ViewModel

```kotlin
@Immutable
data class CartUiState(
    val items: ImmutableList<CartItem> = persistentListOf(),
    val isLoading: Boolean = false,
    val error: String? = null,
)

@HiltViewModel
class CartViewModel @Inject constructor(
    private val repository: CartRepository,
) : ViewModel() {
    private val _ui = MutableStateFlow(CartUiState())
    val ui: StateFlow<CartUiState> = _ui.asStateFlow()

    fun load() {
        viewModelScope.launch {
            _ui.update { it.copy(isLoading = true) }
            repository.fetchCart().fold(
                onSuccess = { items ->
                    _ui.update { it.copy(items = items.toImmutableList(), isLoading = false) }
                },
                onFailure = { e ->
                    _ui.update { it.copy(error = e.message, isLoading = false) }
                },
            )
        }
    }

    fun add(item: CartItem) {
        viewModelScope.launch {
            // optimistic
            val previous = _ui.value.items
            _ui.update { it.copy(items = (previous + item).toImmutableList()) }
            repository.addItem(item).onFailure {
                _ui.update { it.copy(items = previous, error = it.error?.message) }
            }
        }
    }
}

@Composable
fun CartScreen(viewModel: CartViewModel = hiltViewModel()) {
    val ui by viewModel.ui.collectAsStateWithLifecycle()  // mandatory
    LaunchedEffect(Unit) { viewModel.load() }

    LazyColumn {
        items(ui.items, key = { it.id }) { item ->  // key is mandatory
            CartItemRow(item)
        }
    }
}
```

---

## Offline-First Patterns

### iOS — Repository + write queue

```swift
actor WriteQueue {
    private var pending: [PendingWrite] = []
    private let storage: WriteQueueStorage

    init(storage: WriteQueueStorage) {
        self.storage = storage
        Task { pending = await storage.load() }
    }

    func enqueue(_ write: PendingWrite) async {
        pending.append(write)
        await storage.persist(pending)
    }

    func flush(client: APIClient) async {
        for write in pending {
            do {
                try await client.send(write)
                pending.removeAll { $0.id == write.id }
            } catch {
                if write.retryCount > 5 { pending.removeAll { $0.id == write.id } }
                else { /* keep, increment retry */ }
            }
        }
        await storage.persist(pending)
    }
}
```

Flush on network restore:

```swift
import Network

@Observable
final class NetworkMonitor {
    private(set) var isConnected = true
    private let monitor = NWPathMonitor()

    init() {
        monitor.pathUpdateHandler = { [weak self] path in
            Task { @MainActor in self?.isConnected = path.status == .satisfied }
        }
        monitor.start(queue: DispatchQueue.global(qos: .background))
    }
}
```

### Android — Repository + WorkManager

```kotlin
class WriteQueueWorker(
    appContext: Context,
    params: WorkerParameters,
) : CoroutineWorker(appContext, params) {
    override suspend fun doWork(): Result {
        val pending = pendingWriteDao.getAll()
        for (write in pending) {
            runCatching { apiClient.send(write) }
                .onSuccess { pendingWriteDao.delete(write.id) }
                .onFailure {
                    if (write.retryCount > 5) pendingWriteDao.delete(write.id)
                    else pendingWriteDao.incrementRetry(write.id)
                }
        }
        return if (pendingWriteDao.getAll().isEmpty()) Result.success() else Result.retry()
    }
}

// Enqueue on launch / network restore
val request = OneTimeWorkRequestBuilder<WriteQueueWorker>()
    .setConstraints(Constraints.Builder()
        .setRequiredNetworkType(NetworkType.CONNECTED)
        .build())
    .build()
WorkManager.getInstance(context).enqueueUniqueWork(
    "write-queue",
    ExistingWorkPolicy.KEEP,
    request,
)
```

Network monitoring:

```kotlin
class NetworkMonitor(context: Context) {
    private val cm = context.getSystemService(ConnectivityManager::class.java)
    val isConnected: Flow<Boolean> = callbackFlow {
        val callback = object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) { trySend(true) }
            override fun onLost(network: Network) { trySend(false) }
        }
        cm.registerDefaultNetworkCallback(callback)
        awaitClose { cm.unregisterNetworkCallback(callback) }
    }.distinctUntilChanged()
}
```

---

## Platform Adaptation Pattern

iOS / Android live in **separate codebases**. Follow each language's idioms. Where commonality is required, align the API contract / Design Tokens at a higher layer.

> For Liquid Glass adoption policy (iOS 26 default, iOS 27 opt-out removal, 2026-04-28 Xcode 26 submission deadline) and the full Material 3 Expressive component catalog (`NavigationSuiteScaffold`, `PullToRefreshBox`, shape library), see `modern-stack.md` § Liquid Glass and § Material 3 Expressive.

### iOS 26 Liquid Glass

```swift
// iOS 26 ships the dedicated glassEffect() modifier
struct MyView: View {
    var body: some View {
        VStack { Text("Hello") }
            .padding()
            .glassEffect()  // Liquid Glass material
    }
}

// Group multiple glass elements for coordinated animations
GlassEffectContainer {
    HeaderCard()
    ActionRow()
}
```

### Android Material 3 Expressive

```kotlin
@Composable
fun MyScreen() {
    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(title = { Text("Home") })
        },
        floatingActionButton = {
            FloatingActionButton(onClick = { /* ... */ }) {
                Icon(Icons.Default.Add, null)
            }
        },
        bottomBar = {
            FloatingToolbar(  // BottomAppBar is deprecated
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                content = { /* actions */ },
            )
        },
    ) { paddings ->
        // ...
    }
}
```

### Edge-to-edge & Predictive Back (API 36)

See `modern-stack.md` § Edge-to-Edge and § Predictive Back for the `enableEdgeToEdge()` + `BackHandler` snippets and the API 36 enforcement timeline. Both are mandatory wiring at `targetSdk 36` — apply once at `MainActivity` setup and per screen as needed.

---

## Performance Patterns

### iOS — debugging body re-evaluation

```swift
struct MyView: View {
    let value: Int
    var body: some View {
        let _ = Self._printChanges()  // debug only — remove before shipping
        Text("\(value)")
    }
}
```

Performance tips:
- For large datasets use `List` (UICollectionView-backed, cell recycling). `LazyVStack` retains cells and is 10×+ slower at the 1,000-item scale.
- `AsyncImage` has no cache. Use Kingfisher / Nuke / SDWebImageSwiftUI.
- Move heavy work off the main actor with `@concurrent`.

### Android — controlling Compose recomposition

```kotlin
// Unstable lambda problem (LazyListScope is not composable scope)
LazyColumn {
    items(list, key = { it.id }) { item ->
        val onClick = remember(item.id) { { /* ... */ } }  // stabilize via remember
        ItemRow(item = item, onClick = onClick)
    }
}

// derivedStateOf — discretize scroll state
val showButton by remember {
    derivedStateOf { listState.firstVisibleItemIndex > 0 }
}
```

Performance tips:
- Always pass `key = { it.id }` to `LazyColumn` `items`.
- Use `@Immutable` annotation or `kotlinx.collections.immutable` for stable types.
- For images, use Coil 3 `AsyncImage` (Compose-optimized).
- Baseline Profile / Startup Profile cuts startup time by 40-50%.

---

## Permission Flow Pattern (soft pre-prompt)

### iOS

```swift
@MainActor
final class PermissionCoordinator {
    func requestNotifications() async -> Bool {
        // 1. status check
        let center = UNUserNotificationCenter.current()
        let settings = await center.notificationSettings()
        if settings.authorizationStatus == .authorized { return true }
        if settings.authorizationStatus == .denied {
            // graceful degradation: show "open Settings" UI
            return false
        }

        // 2. soft pre-prompt UI (custom view)
        guard await showSoftPrePromptUI() else { return false }

        // 3. system request
        return (try? await center.requestAuthorization(options: [.alert, .badge, .sound])) ?? false
    }
}
```

### Android (API 33+)

```kotlin
@Composable
fun NotificationPermissionRequester(onResult: (Boolean) -> Unit) {
    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission(),
        onResult = onResult,
    )
    var showSoftPrePrompt by remember { mutableStateOf(false) }

    if (showSoftPrePrompt) {
        SoftPrePromptDialog(
            onConfirm = {
                showSoftPrePrompt = false
                launcher.launch(Manifest.permission.POST_NOTIFICATIONS)
            },
            onDismiss = { showSoftPrePrompt = false },
        )
    }

    Button(onClick = { showSoftPrePrompt = true }) {
        Text("Enable notifications")
    }
}
```

---

## Testing Patterns (briefly)

| Use | iOS | Android |
|-----|-----|---------|
| Unit test | XCTest / Swift Testing | JUnit 5 + MockK + Turbine (Flow) |
| UI test | XCUITest | Espresso / Compose UI Test / Maestro |
| Snapshot | swift-snapshot-testing | Paparazzi / Roborazzi |
| E2E | Maestro | Maestro / Espresso |

Detail is owned by the handoff to `Radar` / `Voyager`.

---

> Two codebases, two languages, one product bar. Stay faithful to each platform's idioms.
