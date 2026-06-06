# Kotlin Best Practices — Deep Dive Reference

> Companion to the broader Kotlin knowledge in this `builder/reference/` directory. This file covers production best practices, coding conventions, dispatcher decisions, KMP setup, Gradle/KSP wiring, the production library matrix, and the 2023→2026 migration cheatsheet in depth. The [`native` skill](../../native/SKILL.md) complements this for Jetpack Compose / Material 3 Expressive / Android-platform-specific concerns — Compose UI implementation is intentionally out of scope here.
>
> Baseline: Kotlin 2.3.20 (2026-05 stable) with 2.4-RC2 on EAP; K2 compiler is the only frontend.

---

## Table of Contents

1. [Kotlin Style Guide (Official Coding Conventions)](#1-kotlin-style-guide-official-coding-conventions)
2. [Effective Kotlin (Marcin Moskala) — 2026 Picks](#2-effective-kotlin-marcin-moskala--2026-picks)
3. [Coroutines Best Practices (2026 era)](#3-coroutines-best-practices-2026-era)
4. [Multiplatform (KMP) Best Practices](#4-multiplatform-kmp-best-practices)
5. [Project Structure & Gradle](#5-project-structure--gradle)
6. [Server-side Kotlin](#6-server-side-kotlin)
7. [Testing Strategy](#7-testing-strategy)
8. [Performance Practices](#8-performance-practices)
9. [Memory & Threading](#9-memory--threading)
10. [Production Library Matrix (2026 Baseline)](#10-production-library-matrix-2026-baseline)
11. [Architecture Patterns in Kotlin](#11-architecture-patterns-in-kotlin)
12. [Documentation](#12-documentation)
13. [Release & Distribution](#13-release--distribution)
14. [2023 → 2026 Migration Cheatsheet](#14-2023--2026-migration-cheatsheet)
15. [Appendix A — Quick-Reference Decision Cheat Sheets](#15-appendix-a--quick-reference-decision-cheat-sheets)
16. [Sources](#16-sources)

> **Cross-links:**
> - Language spec details (K2, smart casts, value classes, context parameters, KSP2, expect/actual, JVM interop annotations) → [`kotlin-language-spec.md`](./kotlin-language-spec.md)
> - Concrete anti-patterns mapped to Detekt/Ktlint rules (256+ items across 17 categories) → [`kotlin-anti-patterns.md`](./kotlin-anti-patterns.md)
> - For Compose UI authoring, Material 3 Expressive, predictive back, Live Activities, App Intents, Privacy Manifest → [`native` skill](../../native/SKILL.md). Use Kotlin/JVM patterns here for ViewModel/business-logic layers, not for `@Composable` UI.

---

## 1. Kotlin Style Guide (Official Coding Conventions)

Source of truth: <https://kotlinlang.org/docs/coding-conventions.html>. The conventions are enforced by IntelliJ / Android Studio default code style when `kotlin.code.style=official` is set in `gradle.properties` (mandatory in 2026 — required for K2 IDE behaviour to align).

### 1.1 Naming

| Element | Convention | Example |
|---|---|---|
| Package | lowercase, no underscores | `org.example.project`, `org.example.myProject` |
| Class / Object / Interface / Enum class / Annotation | UpperCamelCase | `class DeclarationProcessor`, `object EmptyProcessor` |
| Function / Property / Local var | lowerCamelCase | `fun processDeclarations()`, `val declarationCount = 1` |
| Constants (`const val`, or top-level/object `val` with no custom getter on immutable data) | SCREAMING_SNAKE_CASE | `const val MAX_COUNT = 8`, `val USER_NAME_FIELD = "UserName"` |
| Mutable top-level / object property holding logical "constant" but mutable type | camelCase | `val mutableCollection: MutableSet<String> = HashSet()` |
| Backing property | `_` prefix | `private val _items = mutableListOf<E>(); val items: List<E> get() = _items` |
| Test method | backticked `` `should do X` `` or underscored `should_do_X` | `` @Test fun `emits loading then success`() `` |
| Acronym (2 letters) | both uppercase | `IOStream`, `URLParser` |
| Acronym (3+ letters) | first letter only | `XmlFormatter`, `HttpInputStream`, `Json` |

**File names**: 1 primary class → match class name (`UserRepository.kt`). Multiple related top-level declarations → descriptive UpperCamelCase (`Extensions.kt`, `StringUtils.kt` — but avoid meaningless `Util`). Don't dump unrelated declarations in `Utils.kt`.

**KMP file suffix convention**: `commonMain/kotlin/Platform.kt`, `jvmMain/kotlin/Platform.jvm.kt`, `iosMain/kotlin/Platform.ios.kt`, `androidMain/kotlin/Platform.android.kt`. The platform suffix is required only on top-level declaration files that have `actual` counterparts; class files don't need the suffix.

### 1.2 `val` vs `var` discipline

- Default to `val`. Use `var` only when reassignment is essential.
- Prefer immutable collection interfaces (`List<T>`, `Set<T>`, `Map<K, V>`) for parameters and return types — even if the underlying is mutable. Never expose `MutableList` from a public API unless mutation is the contract.

```kotlin
// Bad
fun validate(actual: String, allowed: HashSet<String>) { /* ... */ }

// Good
fun validate(actual: String, allowed: Set<String>) { /* ... */ }
```

### 1.3 Expression-body functions

Use for single-expression returns. Omit the explicit return type only when it's obvious (literals, simple calls).

```kotlin
fun double(x: Int) = x * 2                               // type inferred
fun formatName(p: Person): String = "${p.first} ${p.last}"  // explicit type for public API
```

For library-public functions, always declare the return type explicitly even with expression body — protects against accidental signature drift.

### 1.4 Trailing-lambda convention

The lambda passed as the last argument must be outside the parens. Don't repeat the function-call parens when the lambda is the only argument.

```kotlin
list.filter { it > 10 }                       // good
list.filter({ it > 10 })                      // bad
list.fold(0) { acc, e -> acc + e }            // good — lambda last, other args in parens
```

Multiline lambda with explicit parameters: parameters and `->` on the first line; body indented.

```kotlin
foo { ctx: Context, env: Env ->
    ctx.configureEnv(env)
    env.commit()
}
```

If the parameter list is long enough to force a wrap, put `->` on its own line.

### 1.5 Named arguments policy

Required (style guide) in these cases:
- More than one parameter of the same type → name them.
- Any `Boolean` parameter at a call site (avoids `drawSquare(10, 10, 100, 100, true)` mystery).
- Constructor calls with many parameters and most defaulted.

```kotlin
// Bad
drawSquare(10, 10, 100, 100, true)

// Good
drawSquare(x = 10, y = 10, width = 100, height = 100, fill = true)
```

### 1.6 Modifier order (canonical)

```
public / protected / private / internal
expect / actual
final / open / abstract / sealed / const
external
override
lateinit
tailrec
vararg
suspend
inner
enum / annotation / fun  // (the "fun" modifier on interfaces)
companion
inline / value
infix
operator
data
```

Annotations always precede modifiers. Single-line for empty annotations on properties; multiline for class/function-level annotations with parameters.

### 1.7 Formatting

- **Indent**: 4 spaces, no tabs.
- **Line length**: 120 columns (style guide is not explicit, but IntelliJ default; common team convention).
- **Trailing commas**: encouraged at declaration sites and call sites with line breaks. Helps git diffs and IDE reorder operations.

```kotlin
class Person(
    val firstName: String,
    val lastName: String,
    val age: Int,                  // trailing comma
)
```

- **Blank lines**: between top-level declarations, between class members of different kinds (props vs methods), between `when` branches with multi-line bodies.
- **Class body order**: properties → init blocks → secondary constructors → methods → companion object. Don't sort alphabetically or by visibility — group by responsibility.
- **`when` branches**: short single-expression branches stay on one line; multi-line branches separated by blank line and use braces.

### 1.8 Idiomatic preferences

| Prefer | Avoid |
|---|---|
| `if` / `when` / `try` as expressions returning a value | Imperative reassignment in branches |
| `for (i in 0..<n)` (open-end) | `for (i in 0..n - 1)` |
| String templates: `"$name has ${items.size}"` | String concatenation with `+` |
| `trimIndent()` / `trimMargin()` for multi-line literals | Embedded `\n` |
| Property when getter is cheap, deterministic, non-throwing | Function when no side effects |
| Extension functions liberally | Static `Utils` classes |
| Default parameter values | Overload chains |
| `it` for short non-nested lambdas | `lambda { it -> ... }` — declare name only when nesting/disambiguation needed |
| Higher-order functions (`filter`, `map`, `fold`) | `for` loop with mutation |
| Single-expression `when` for nullable `Boolean?`: `when (value) { true -> ...; false -> ...; null -> ... }` | `if (value)` on `Boolean?` |

### 1.9 Library-author additional requirements

- Explicit public visibility on every declaration (use `explicitApi()` strict mode in `build.gradle.kts`).
- Explicit return types for public functions and property types (don't rely on inference).
- KDoc on every public member (overrides exempt unless adding behavior).

```kotlin
kotlin {
    explicitApi()  // ENFORCE in library modules
}
```

---

## 2. Effective Kotlin (Marcin Moskala) — 2026 Picks

`kt.academy` hosts the public version. The items below are the highest-impact ones for a 2026 production codebase. Numbers reflect the 3rd edition arrangement.

### 2.1 Item: minimize visibility (rest-of-contract)

Use the most restrictive visibility (`private` > `internal` > `protected` > `public`). `internal` in libraries also requires `@PublishedApi` for inline-function reach. Strict default to `private` for properties unless callers need them.

### 2.2 Item: maintain consistency in returning values

If a sibling function returns `Result<T>`, don't make a peer throw. Either all may throw, or all return Result/Either. Inconsistency forces callers into defensive branches.

### 2.3 Item: use property delegation

```kotlin
class View {
    val title: String by lazy { computeTitle() }           // lazy, thread-safe
    var selected: Boolean by Delegates.observable(false) { _, old, new ->
        if (old != new) listeners.forEach { it.onChange(new) }
    }
    val context: Context by lazyNone { /* not thread-safe, faster */ }
}
```

- `lazy { }` (default `LazyThreadSafetyMode.SYNCHRONIZED`) for shared state; `LazyThreadSafetyMode.NONE` when confined to a single thread.
- `Delegates.observable` for change notification.
- `Delegates.vetoable` to gate assignments.
- `lateinit` is faster than `Delegates.notNull()` and should be the default for late-init non-primitive refs. `notNull()` is the fallback for primitives (`Int`, `Long`, `Boolean`) where `lateinit` is unavailable.
- Custom delegates: implement `ReadWriteProperty<T, V>` / `ReadOnlyProperty<T, V>` with operator-fun `getValue`/`setValue`. Use for config-driven properties (`val port by SystemProperty("app.port", default = 8080)`).

### 2.4 Item: avoid unnecessary object creation

- Use `Sequence` for **multi-step pipelines on large collections with early termination** — `asSequence()` only pays off when chained ops > 2 and N is large enough that lazy short-circuit matters (e.g. `.take(10)` over a huge list).
- For **small lists or single-step pipelines, plain `List` is faster** (Kotlin's `filter`, `map` on `List` are `inline`, so the lambda doesn't allocate — see §8).
- Reuse `Comparator` via `compareBy` rather than rebuilding inside hot loops.
- Reuse `Regex` objects — compile once at top-level or `private val`.

### 2.5 Item: use `inline` for higher-order functions crossing boundaries

`inline fun <T> measure(block: () -> T): T = ...` — the lambda is inlined, no `Function0` allocation, and `crossinline`/`noinline` give fine control. Don't inline large bodies (bytecode bloat) or recursive functions.

### 2.6 Item: prefer `Sequence` only when pipeline depth justifies it

```kotlin
// Use sequence — many ops, huge collection, early termination
val first10 = items.asSequence()
    .map { it.transform() }
    .filter { it.valid }
    .map { it.score() }
    .take(10)
    .toList()

// Use plain List — single op, modest N, no early exit
val active = users.filter { it.active }
```

See §8 for the 2025-2026 empirical break-even — the old "Sequence wins on 2+ ops" rule has inverted in modern JIT conditions.

### 2.7 Item: leverage immutability + `data class copy`

```kotlin
data class User(val id: UserId, val name: String, val email: Email)

val updated = user.copy(email = newEmail)
```

`copy()` keeps the rest of the state immutable. Combine with sealed-class state hierarchies (§11). Never mutate `data class` properties (avoid `var` inside `data class`).

### 2.8 Item: use `@JvmInline value class` for type-safe primitives

```kotlin
@JvmInline value class UserId(val raw: Long)
@JvmInline value class Email(val raw: String)

fun lookup(id: UserId): User? { /* ... */ }

lookup(user.email)  // compile error — different value classes
```

- Replaces type aliases when **type safety** matters. `typealias` does not give compile-time discrimination.
- Pitfalls: lost inlining when the wrapper crosses an interface boundary, lost inlining when nullable on primitive (`UserId?` boxes if underlying is primitive), arrays of value classes need `IntArray`/`LongArray` underneath or they box. See [`kotlin-anti-patterns.md` §3.8](./kotlin-anti-patterns.md#3-type--generics-pitfalls).

---

## 3. Coroutines Best Practices (2026 era)

### 3.1 `suspend fun` discipline

- A `suspend fun` should be **main-safe** by default: the caller can invoke it from any dispatcher without worrying about blocking. Inside the function, switch dispatchers via `withContext(Dispatchers.IO) { ... }` when the work blocks.
- Don't sprinkle `Dispatchers.X` in the caller. Push dispatcher choice into the function that knows the work shape.

```kotlin
class UserRepository(private val api: UserApi, private val db: UserDao) {
    suspend fun fetchUser(id: UserId): User = withContext(Dispatchers.IO) {
        api.getUser(id.raw).also { db.upsert(it) }
    }
}
```

### 3.2 Never `runBlocking` in production code

`runBlocking { }` is for `main()` entry points (CLI tools, tests). It blocks the calling thread. In server / library / Android code, this defeats structured concurrency and causes thread-pool starvation.

**Exception**: top of `main()`, JVM shutdown hooks, JNI bridges, and `kotlinx.coroutines.test.runTest` (which uses `runBlocking` under the hood but with a test scheduler).

### 3.3 Scope ownership rules

- **ViewModel scope**: `viewModelScope` (Android) — cancelled in `onCleared()`.
- **Application scope**: a custom `CoroutineScope(SupervisorJob() + Dispatchers.Default)` held by a long-lived singleton; survives screen rotations / process backgrounding.
- **Request scope** (server): one scope per HTTP request, cancelled when the response is sent. Ktor wires this automatically via `PipelineContext.coroutineContext`.
- **Library**: never launch into `GlobalScope`. Accept a `CoroutineScope` parameter or expose a `suspend fun`.

### 3.4 `Dispatchers.IO.limitedParallelism(n)` for bounded pools

Use when a downstream resource has a hard concurrency limit (DB connection pool, rate-limited API, external service quota).

```kotlin
class GeocodingService(client: HttpClient) {
    private val dispatcher = Dispatchers.IO.limitedParallelism(8)  // hard cap = 8
    suspend fun geocode(addr: String): LatLng = withContext(dispatcher) { ... }
}
```

**Caveat**: `Dispatchers.IO` is normally elastic (up to ~64 threads, growable on demand). `limitedParallelism` views inherit IO's thread pool but cap their slice. **Don't** artificially limit IO when the bottleneck is upstream — that wastes IO's elasticity. Use only when there's a real downstream limit. **Create the limited dispatcher once in a DI module**; re-creating it per call site produces unrelated views with no shared limit (a frequent footgun).

### 3.5 `Flow` over `LiveData` / `Channel` in app code

| Use case | Choose | Rationale |
|---|---|---|
| Single-shot async result | `suspend fun` returning `T` | Coroutines, not streams |
| Cold async stream (DB query, file read) | `Flow<T>` | Lazy, cancellable, structured |
| Hot UI state (current screen state) | `StateFlow<T>` | Always has a value, conflates, lifecycle-friendly |
| Hot events (one-shot navigation, errors) | `SharedFlow<T>` with `replay=0, extraBufferCapacity≥1` | Events don't replay on subscribe |
| Multi-consumer broadcast | `SharedFlow<T>` | Replaces deprecated `BroadcastChannel` |
| Producer-consumer queue | `Channel<T>` | Lower-level; for plumbing only |

`LiveData` is fine on legacy Android codebases but new code uses `StateFlow` + `collectAsStateWithLifecycle()` (Compose) or `lifecycleScope.launch { repeatOnLifecycle(STARTED) { flow.collect { ... } } }` (Views). UI-layer collection is covered by the [`native` skill](../../native/SKILL.md); the ViewModel-side flow shape decisions belong here.

### 3.6 `MutableStateFlow.update { }` over `.value = .value.copy()`

```kotlin
// Bad: race
_state.value = _state.value.copy(loading = false, items = newItems)

// Good: atomic CAS loop
_state.update { current -> current.copy(loading = false, items = newItems) }
```

`update` retries on conflict — safe for concurrent writers. Same applies to `updateAndGet`, `getAndUpdate`.

### 3.7 Common Flow operators (idiomatic)

| Operator | Use for |
|---|---|
| `combine(a, b) { x, y -> ... }` | Latest from each input |
| `zip(a, b) { x, y -> ... }` | Pair-wise (waits for both) |
| `flatMapLatest { ... }` | Cancel previous on new emission — search-as-you-type |
| `flatMapConcat { ... }` | Sequential per emission |
| `flatMapMerge { ... }` | Parallel per emission with concurrency limit |
| `debounce(300.milliseconds)` | Throttle bursty inputs (search box) |
| `sample(1.seconds)` | Periodic sampling of fast emissions |
| `distinctUntilChanged()` | Skip duplicate consecutive values |
| `onEach { }` | Side effects in the pipeline |
| `catch { e -> emit(fallback) }` | Upstream error → recover |
| `retryWhen { e, attempt -> ... }` | Retry policy |
| `stateIn(scope, started, initial)` | Hot conversion of a cold Flow into a StateFlow |
| `shareIn(scope, started, replay)` | Multi-consumer fan-out |

### 3.8 Testing with `runTest` and `TestDispatcher`

```kotlin
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.UnconfinedTestDispatcher

class UserViewModelTest {
    @Test fun `loads user on init`() = runTest {
        val vm = UserViewModel(FakeRepo(), UnconfinedTestDispatcher(testScheduler))
        advanceUntilIdle()
        assertEquals(User("Alice"), vm.state.value.user)
    }
}
```

- `runTest { }` uses virtual time — `delay(1.hours)` is instant.
- `StandardTestDispatcher` (queued, manual `advanceTimeBy` / `advanceUntilIdle`) for tests that need explicit ordering.
- `UnconfinedTestDispatcher` (greedy, immediate) for simple tests where ordering doesn't matter.
- Inject the dispatcher into production code — don't hard-code `Dispatchers.IO` in classes you test.

### 3.9 Test Flow with Turbine

```kotlin
@Test fun `emits loading then success`() = runTest {
    repo.users.test {
        assertEquals(Loading, awaitItem())
        assertEquals(Success(listOf(alice)), awaitItem())
        cancelAndIgnoreRemainingEvents()
    }
}
```

Don't roll your own `flow.toList()` collector — race conditions. `Turbine` 1.x handles timing, cancellation, and assertion of terminal events (`awaitComplete()`, `awaitError()`).

### 3.10 Structured cancellation discipline

- Never catch `CancellationException` to silence it. If you must catch (e.g., to clean up), rethrow:

```kotlin
try {
    work()
} catch (e: CancellationException) {
    cleanup()
    throw e          // rethrow!
} catch (e: Throwable) {
    log.error(e)
}
```

- Prefer `try-finally` or `Job.invokeOnCompletion { cause -> ... }` for cleanup.
- `coroutineScope { }` propagates cancellation downward and exceptions upward; `supervisorScope { }` isolates failures of children.
- Wrap suspending cleanup in `withContext(NonCancellable)` to survive parent cancellation.

For 28 concrete coroutines pitfalls (including the `withContext(SupervisorJob())` no-op trap and `flowOn` on `StateFlow` being silently ignored), see [`kotlin-anti-patterns.md` §2](./kotlin-anti-patterns.md#2-coroutines-pitfalls).

---

## 4. Multiplatform (KMP) Best Practices

KMP is **production-ready in 2026** — Netflix, Cash App, McDonald's run it in production. Compose Multiplatform iOS is stable since 1.8.0 (May 2025); CMP-Web is Beta since 1.9.0 (Oct 2025); CMP 1.11.0 shipped May 2026.

### 4.1 When to start `commonMain`

Start common-first if **business logic, data layer, or analytics** are 60%+ of the codebase. Don't commonize UI on day 1 unless the project explicitly targets shared UI (CMP).

### 4.2 `expect` / `actual` minimization

Prefer common abstractions + impl-by-injection over `expect class`:

```kotlin
// Bad: hard to test, hard to mock, increases expect/actual surface
expect class PlatformLogger {
    fun log(msg: String)
}

// Good: interface in commonMain, implementations injected per target
// commonMain
interface Logger { fun log(msg: String) }

// androidMain
class AndroidLogger(private val tag: String) : Logger {
    override fun log(msg: String) = Log.d(tag, msg)
}

// iosMain
class IosLogger : Logger {
    override fun log(msg: String) = NSLog(msg)
}
```

Rules of thumb:
- Use `expect fun` instead of `expect class` when possible (smaller surface).
- Keep `expect/actual` for low-level platform primitives only (file paths, time, crypto, system calls).
- For business types, use interfaces + DI.

### 4.3 Target hierarchy template

`applyDefaultHierarchyTemplate()` (or `applyDefaultHierarchyTemplate(template) { ... }` for customization) gives the standard tree without manual `sourceSets { ... }` plumbing.

```kotlin
// build.gradle.kts
kotlin {
    androidTarget()
    iosX64(); iosArm64(); iosSimulatorArm64()
    jvm()
    js(IR) { browser(); nodejs() }
    wasmJs { browser() }

    applyDefaultHierarchyTemplate()   // gives commonMain → nativeMain → appleMain → iosMain etc.

    sourceSets {
        commonMain.dependencies {
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.ktor.client.core)
        }
        androidMain.dependencies {
            implementation(libs.ktor.client.okhttp)
        }
        iosMain.dependencies {
            implementation(libs.ktor.client.darwin)
        }
    }
}
```

The default template provides intermediate source sets: `nativeMain` (Linux + macOS + iOS + watchOS + tvOS + Windows + Android Native), `appleMain` (macOS + iOS + watchOS + tvOS), `iosMain` (iosX64 + iosArm64 + iosSimulatorArm64). Write platform-shared code at the most specific common ancestor.

### 4.4 Compose Multiplatform vs platform-native UI decision

| Choose CMP when... | Choose platform-native UI when... |
|---|---|
| Brand-led design, identical visuals across iOS/Android/Desktop/Web | Platform-idiomatic UX matters (HIG, Material 3 Expressive) |
| Internal tools, B2B dashboards, prototype velocity | Consumer-facing app where ratings depend on platform feel |
| Team is Compose-fluent, no SwiftUI talent | iOS team owns iOS, Android team owns Android (Conway's Law) |
| Logic + UI together justifies single skill set | Logic shared via KMP, UI per platform (recommended for new consumer apps in 2026) |

The most common 2026 production pattern: **KMP for data/business/networking + per-platform UI (Compose on Android via the [`native` skill](../../native/SKILL.md), SwiftUI on iOS)**.

### 4.5 Library choice — prefer `kotlinx-*` first

| Need | First choice | Fallback |
|---|---|---|
| Serialization | `kotlinx.serialization` | Jackson (Spring), moshi (Android-only) |
| Networking | Ktor client | OkHttp + Retrofit (Android-only) |
| DB | SQLDelight (KMP) / Room KMP | Realm Kotlin |
| DI | Koin (KMP) / kotlin-inject | Hilt (Android-only) |
| Date/time | `kotlinx-datetime` | `java.time` (JVM-only) |
| Atomics | `kotlinx-atomicfu` | `java.util.concurrent.atomic` (JVM-only) |
| Logging | `kotlin-logging` (JVM) / `kermit` (KMP) | SLF4J directly |
| Concurrency | `kotlinx.coroutines` | RxJava (legacy) |
| File I/O | `kotlinx-io` | `java.io` (JVM-only) |

### 4.6 Expect-by-injection pattern

For DI-style platform substitution without `expect class`:

```kotlin
// commonMain
interface DateFormatter {
    fun format(instant: Instant): String
}
class GreetingViewModel(private val formatter: DateFormatter) { /* ... */ }

// androidMain
class AndroidDateFormatter(locale: Locale) : DateFormatter { /* uses java.text.DateFormat */ }

// iosMain
class IosDateFormatter(locale: NSLocale) : DateFormatter { /* uses NSDateFormatter */ }

// Koin module
val platformModule = module {
    single<DateFormatter> { AndroidDateFormatter(Locale.getDefault()) }  // androidMain
}
```

### 4.7 `kotlinx-io` for KMP I/O

`kotlinx-io` 0.5+ provides `Buffer`, `Source`, `Sink` — a Kotlin-native, multiplatform I/O abstraction. Built around a `Buffer` (linked-list of segments — cheap growth and copy). Use it instead of `java.io.InputStream` for any code that runs in `commonMain`.

```kotlin
import kotlinx.io.Buffer
import kotlinx.io.readString

val buffer = Buffer().also { it.writeString("hello") }
val s: String = buffer.readString()
```

---

## 5. Project Structure & Gradle

### 5.1 Kotlin DSL (`build.gradle.kts`) over Groovy

Mandatory in 2026. Groovy `.gradle` files are legacy. Kotlin DSL gives type-safe accessors, IDE refactoring, and consistent language with the rest of the project.

### 5.2 Version catalog (`libs.versions.toml`)

```toml
# gradle/libs.versions.toml
[versions]
kotlin = "2.3.20"
ktor = "3.4.0"
coroutines = "1.10.0"
serialization = "1.9.0"
ksp = "2.3.20-2.0.0"
compose = "1.11.0"

[libraries]
kotlinx-coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }
kotlinx-coroutines-test = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-test", version.ref = "coroutines" }
kotlinx-serialization-json = { module = "org.jetbrains.kotlinx:kotlinx-serialization-json", version.ref = "serialization" }
ktor-client-core = { module = "io.ktor:ktor-client-core", version.ref = "ktor" }
ktor-client-okhttp = { module = "io.ktor:ktor-client-okhttp", version.ref = "ktor" }
ktor-client-darwin = { module = "io.ktor:ktor-client-darwin", version.ref = "ktor" }
turbine = "app.cash.turbine:turbine:1.2.0"
mockk = "io.mockk:mockk:1.13.13"
kotest-runner-junit5 = "io.kotest:kotest-runner-junit5:5.9.1"

[plugins]
kotlin-multiplatform = { id = "org.jetbrains.kotlin.multiplatform", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
compose-multiplatform = { id = "org.jetbrains.compose", version.ref = "compose" }
```

Reference in `build.gradle.kts`:

```kotlin
plugins {
    alias(libs.plugins.kotlin.multiplatform)
    alias(libs.plugins.kotlin.serialization)
}

dependencies {
    implementation(libs.kotlinx.coroutines.core)
    testImplementation(libs.turbine)
    testImplementation(libs.mockk)
}
```

### 5.3 Convention plugins (`build-logic`)

Use `build-logic` (an included build) over `buildSrc` — better build cache, isolated classpath.

```
project-root/
├── build-logic/
│   ├── settings.gradle.kts
│   └── convention/
│       ├── build.gradle.kts
│       └── src/main/kotlin/
│           ├── kotlin-common.gradle.kts
│           ├── kotlin-library.gradle.kts
│           └── kotlin-multiplatform.gradle.kts
├── app/
│   └── build.gradle.kts
└── settings.gradle.kts
```

```kotlin
// build-logic/convention/src/main/kotlin/kotlin-library.gradle.kts
plugins {
    kotlin("jvm")
}

kotlin {
    jvmToolchain(21)
    explicitApi()  // libraries must be explicit
    compilerOptions {
        allWarningsAsErrors.set(true)
        freeCompilerArgs.addAll(
            "-Xjsr305=strict",
            "-Xjvm-default=all",
        )
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}
```

Apply in module:

```kotlin
plugins {
    id("kotlin-library")
}
```

### 5.4 Required `gradle.properties` flags (2026 baseline)

```properties
kotlin.code.style=official
org.gradle.caching=true
org.gradle.configuration-cache=true
org.gradle.parallel=true
org.gradle.jvmargs=-Xmx4096M -Dfile.encoding=UTF-8 -XX:+UseG1GC
kotlin.incremental=true
kotlin.mpp.enableCInteropCommonization=true
ksp.useKSP2=true   # KSP2 is the default in 2026; explicit for clarity
```

### 5.5 KSP2 over KAPT (KAPT is deprecated path)

KAPT is in formal deprecation for K2. KSP2 is the only annotation processor going forward and is 1.5x-2x faster.

- Room: `ksp(libs.androidx.room.compiler)`
- Moshi: `ksp(libs.moshi.codegen)`
- Hilt: `ksp(libs.hilt.compiler)` (Hilt added KSP support in 2.48+)
- Dagger: `ksp(libs.dagger.compiler)` (KSP2 supported since 2.51)
- Koin annotations: `ksp(libs.koin.ksp.compiler)`

Migration: in `build.gradle.kts` replace `kapt("...")` with `ksp("...")`. Verify all your processors have KSP support; if one doesn't, you can keep `kapt.use.k2=false` for that module only.

### 5.6 Gradle compatibility (2026)

- Gradle 8.10+ (required for Kotlin 2.2 / K2 features).
- Gradle 9.x (released late 2025) — adds improved configuration cache, dependency-verification UX, Java 21 toolchain auto-provision.
- AGP (Android Gradle Plugin) 8.7+ for Android with Kotlin 2.2; AGP 9 ships in 2026 alongside `targetSdk 36` and drops first-class KAPT support.

---

## 6. Server-side Kotlin

### 6.1 Ktor 3.x as 2026 default for new services

**Ktor 3.4.0 (Jan 2026)** is the current line. Built on coroutines from day 1, no annotation processing, no reflection-heavy magic, native server support (Kotlin/Native server is alpha but real). Highlights of 3.4:
- OpenAPI generation
- Zstd compression support
- Duplex streaming for OkHttp engine
- Structured concurrency integration with HTTP request lifecycle

Choose Ktor for: greenfield services, microservices, KMP-shared server+client, teams who like minimal frameworks.

### 6.2 Ktor server recommended structure

```
src/main/kotlin/com/example/
├── Application.kt           # main() and EngineMain
├── config/                  # HOCON / env loading
├── plugins/                 # ContentNegotiation, Auth, Compression, etc.
├── controller/              # route definitions
├── service/                 # business logic
├── repository/              # data access (Exposed / R2DBC)
├── domain/                  # entities, value objects, sealed states
└── dto/                     # request/response DTOs (kotlinx.serialization @Serializable)
```

```kotlin
fun main(args: Array<String>) = EngineMain.main(args)

fun Application.module() {
    configureSecurity()
    configureSerialization()
    configureMonitoring()
    configureRouting()
}

fun Application.configureRouting() {
    routing {
        usersRoute()
        ordersRoute()
    }
}

fun Route.usersRoute() {
    val service: UserService by application.inject()
    route("/users") {
        get { call.respond(service.list()) }
        post {
            val req = call.receive<CreateUserRequest>()
            call.respond(HttpStatusCode.Created, service.create(req))
        }
    }
}
```

### 6.3 Ktor essentials

- **JSON**: install `ContentNegotiation` with `kotlinx.serialization`. Set `ignoreUnknownKeys = true` for forward-compat with the producer.
- **DB pool**: HikariCP for JDBC; for R2DBC use the driver's native pool (e.g., `r2dbc-pool`).
- **Validation**: `RequestValidation` plugin + `konform` / `valiktor` for richer rules.
- **Tracing**: `MicrometerMetrics` plugin + OpenTelemetry instrumentation.
- **Authentication**: `Authentication` plugin with `jwt` / `bearer` / `session` providers.

### 6.4 Spring Boot + Kotlin (when team is Spring-shop)

Spring Boot 3.x has first-class Kotlin support: `spring-boot-starter-web` for MVC, `spring-boot-starter-webflux` for reactive. `kotlin-spring` plugin auto-opens classes for Spring proxying.

For coroutines on Spring WebFlux: use `kotlinx.coroutines.reactor` bridge — `suspend fun` controllers, `Flow<T>` returns, `awaitSingle()` / `awaitFirstOrNull()` to convert `Mono` / `Flux`.

```kotlin
@RestController
class UserController(private val service: UserService) {
    @GetMapping("/users/{id}")
    suspend fun getUser(@PathVariable id: Long): User =
        service.findById(id) ?: throw NotFoundException()

    @GetMapping("/users")
    fun listUsers(): Flow<User> = service.streamAll()
}
```

### 6.5 Server DB choice

| DB style | Pick | Why |
|---|---|---|
| Synchronous JDBC, Kotlin-friendly DSL | **Exposed 1.0** (Jan 2026 GA) | Type-safe DSL or DAO, transparent transactions |
| Reactive R2DBC | **Exposed R2DBC** (new in 1.0) or **jOOQ + jooq-kotlin-coroutines** | Non-blocking with Kotlin coroutines bridge |
| Spring shop | **Spring Data JPA + Hibernate** (sync) / **Spring Data R2DBC** (reactive) | Existing ecosystem |
| Type-safe SQL queries, multi-dialect | **jOOQ Kotlin DSL** | Best SQL-first experience |
| KMP | **SQLDelight** (server side can use it too) | Type-safe `.sq` files compiled to Kotlin |

### 6.6 Server best practices

- **Structured concurrency in request handlers**: launch children via `coroutineScope { ... }`; failures cancel siblings, all are tied to the request lifecycle.
- **Don't block IO threads**: never call JDBC inside an `event-loop` thread in WebFlux/Ktor without `withContext(Dispatchers.IO)` or a dedicated dispatcher.
- **Idempotency keys** for POSTs that mutate.
- **Structured logging**: SLF4J + JSON encoder; include `requestId`/`traceId` via MDC.

---

## 7. Testing Strategy

### 7.1 Stack (2026 default)

| Layer | Tool |
|---|---|
| Test runner | **JUnit 5** (Jupiter) |
| Assertions (idiomatic) | **kotlin-test** (stdlib) or **Kotest assertions** (`shouldBe`, `shouldContain`) |
| Mocking | **MockK 1.13+** (Kotlin-native; over Mockito) |
| Flow testing | **Turbine 1.x** |
| Coroutines | `kotlinx.coroutines.test` (`runTest`, `TestDispatcher`) |
| Property-based | **Kotest** (`PropertyContext`, `Arb<T>`, `forAll { }`) |
| Behavior spec / BDD | **Kotest** (`BehaviorSpec`, `FunSpec`, `DescribeSpec`) |
| Power assertions | **Kotlin Power-Assert plugin** (compiler plugin, official since 2.0) |
| Integration | **Testcontainers** (with `org.testcontainers:testcontainers-kotlin` or the official Java API) |
| Microbench | **kotlinx-benchmark** (KMP-aware) or JMH (JVM only) |

### 7.2 Kotest example styles

```kotlin
class CartTest : BehaviorSpec({
    given("an empty cart") {
        val cart = Cart()
        `when`("adding an item") {
            cart.add(Item("apple", 2))
            then("size becomes 1") { cart.size shouldBe 1 }
            then("total reflects the price") { cart.total shouldBe 200 }
        }
    }
})

// Property-based
class StringTest : FunSpec({
    test("reverse twice == identity") {
        checkAll(Arb.string()) { s -> s.reversed().reversed() shouldBe s }
    }
})
```

### 7.3 MockK example

```kotlin
class UserServiceTest {
    @Test fun `returns cached user on second call`() = runTest {
        val repo = mockk<UserRepo>()
        coEvery { repo.fetch(UserId(1)) } returns alice

        val service = UserService(repo)
        service.get(UserId(1))
        service.get(UserId(1))

        coVerify(exactly = 1) { repo.fetch(UserId(1)) }  // cached
    }
}
```

- `coEvery { } returns ...` for `suspend` functions.
- `every { } returns ...` for sync.
- `coVerify { }` / `verify { }` for assertion of calls.
- `mockkStatic(::globalFn)` for top-level functions and static methods.
- `mockkObject(MyObject)` for Kotlin `object`s.

### 7.4 Turbine example

```kotlin
@Test fun `viewmodel emits sequence`() = runTest {
    val vm = MyViewModel(repo, UnconfinedTestDispatcher(testScheduler))
    vm.state.test {
        assertEquals(State.Initial, awaitItem())
        vm.load()
        assertEquals(State.Loading, awaitItem())
        assertEquals(State.Success(data), awaitItem())
        ensureAllEventsConsumed()
    }
}
```

### 7.5 Power-Assert

```kotlin
// build.gradle.kts
plugins { kotlin("plugin.power-assert") version "2.3.20" }
powerAssert {
    functions = listOf("kotlin.assert", "kotlin.test.assertEquals", "kotlin.test.assertTrue")
}

// On failure, you get the diagram of which sub-expression failed:
//   assert(user.address.city == "NYC")
//          |    |       |
//          |    |       "LA"
//          |    Address(...)
//          User(...)
```

### 7.6 Parameterized tests

```kotlin
@ParameterizedTest
@CsvSource("1,1", "2,4", "3,9", "10,100")
fun `square is correct`(input: Int, expected: Int) {
    assertEquals(expected, square(input))
}
```

Kotest version:

```kotlin
class SquareTest : FunSpec({
    withData(1 to 1, 2 to 4, 3 to 9) { (n, expected) ->
        square(n) shouldBe expected
    }
})
```

### 7.7 Test discipline

- For every happy path test, write at least one error-case test.
- Don't share `var` state across tests in the same class — use `@BeforeEach` or fresh instances inside the test.
- Tests collecting Flow → always Turbine. Never `flow.toList()` (race) or `flow.first()` (only first value).
- Inject the `CoroutineDispatcher` so tests can substitute `UnconfinedTestDispatcher` / `StandardTestDispatcher`.

For 10 concrete testing pitfalls (including `runBlocking` in tests, missing `Dispatchers.setMain`, multiple `TestDispatcher` instances with different schedulers), see [`kotlin-anti-patterns.md` §15](./kotlin-anti-patterns.md#15-testing-pitfalls).

---

## 8. Performance Practices

### 8.1 Sequence vs Iterable break-even (2025-2026 update — conventional wisdom inverted)

**Old advice (pre-2024)**: "Use Sequence for chains of 2+ ops on large collections."
**2025+ measurements (Chris Banes, JMH benchmarks)**: in modern JIT conditions, **plain `List` is nearly always faster for collection sizes < 10,000 and pipeline depth ≤ 3**, because Kotlin's `filter`/`map`/etc. on `Iterable` are `inline` and lose lambda allocation; Sequence has per-element function-call overhead that doesn't vanish.

**Updated rule**:
- ≤ 2-3 ops or small N → `List` operations.
- Many ops AND large N AND early termination (`take`, `first`, `firstOrNull`) → `Sequence`.
- Generative / infinite streams → `Sequence` (the only option).

### 8.2 `inline` for higher-order functions

```kotlin
inline fun <T, R> T.measureNs(block: T.() -> R): Pair<R, Long> {
    val start = System.nanoTime()
    val result = block()
    return result to (System.nanoTime() - start)
}
```

- Eliminates the `Function0` / `Function1` object allocation.
- Allows non-local `return` from inside the lambda (returns from the enclosing function).
- `crossinline` when the lambda is captured in another lambda (no non-local return).
- `noinline` to opt out a single lambda parameter from inlining.

**Don't** `inline` large bodies — bytecode bloat at every call site. **Don't** inline functions that recurse on themselves.

### 8.3 Avoid spurious boxing on JVM

- `IntArray`, `LongArray`, `DoubleArray` over `Array<Int>` etc. (no boxing).
- Primitives in generics box: `List<Int>` is `List<java.lang.Integer>` underneath. If hot, use specialized collections (`IntArray`, Eclipse Collections, Trove).
- `kotlin.Result<T>` boxes its value — fine for cold paths, expensive in hot loops; prefer a sealed class `Outcome<T>` if hot.

### 8.4 `@JvmInline value class` for zero-cost wrappers

```kotlin
@JvmInline value class Pixels(val raw: Int)
@JvmInline value class Meters(val raw: Double)

fun draw(width: Pixels, height: Pixels) { /* ... */ }
```

At runtime, `Pixels(10)` is just the `Int` 10. Static methods replace instance methods. **Caveats** (see also language spec §3.3 and anti-patterns §3.8):
- Crossing an interface boundary forces boxing.
- Nullable underlying primitive forces boxing.
- Arrays box (`Array<Pixels>` is `Array<Pixels>` not `IntArray`).

### 8.5 `lateinit` over nullable for late-init dependencies

```kotlin
class Activity {
    private lateinit var binding: ActivityBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        binding = ActivityBinding.inflate(layoutInflater)
    }
}
```

- Avoids `?.` everywhere.
- Throws `UninitializedPropertyAccessException` if read before assign — fail-fast.
- Not for primitives (use `Delegates.notNull()` or default to `0`).

### 8.6 JIT warmup for benchmarks

A naive `for` loop benchmark in `main()` is dominated by JIT warm-up. Always use a benchmark harness:
- **JMH** (`org.openjdk.jmh`) for JVM, with warmup iterations.
- **kotlinx-benchmark** (KMP-aware, wraps JMH on JVM + native benchmark on K/Native + WasmJs).

```kotlin
@State(Scope.Benchmark)
class SequenceBenchmark {
    val list = (1..10_000).toList()

    @Benchmark fun listChain() = list.map { it * 2 }.filter { it > 100 }.sum()
    @Benchmark fun sequenceChain() = list.asSequence().map { it * 2 }.filter { it > 100 }.sum()
}
```

### 8.7 Hot-path micro-optimizations

- `String.intern()` rarely justified after JDK 7 (string table is much better).
- `lazyOf(value)` for cheap pre-computed lazies (vs `lazy { value }` which allocates a sync block).
- `buildList { }`, `buildMap { }`, `buildString { }` over manual `mutableListOf().also { ... }`.

---

## 9. Memory & Threading

### 9.1 Coroutine leak detection

```kotlin
// Production: install DebugProbes early
import kotlinx.coroutines.debug.DebugProbes

fun main() {
    DebugProbes.install()
    // ...
}

// Dump live coroutines on demand (e.g., from a debug endpoint)
DebugProbes.dumpCoroutines()
```

- `kotlinx-coroutines-debug` artifact provides `DebugProbes`, coroutine name in stack traces, and `Job.invokeOnCompletion` introspection.
- In tests, install probes inside `runTest` to catch orphaned jobs.
- **Do not ship `kotlinx-coroutines-debug` to production.** It adds heavyweight instrumentation; confine to `testImplementation` / `debugImplementation`.

### 9.2 `Job.invokeOnCompletion` for cleanup

```kotlin
val job = scope.launch { work() }
job.invokeOnCompletion { cause ->
    when (cause) {
        null -> log.info("completed normally")
        is CancellationException -> log.info("cancelled")
        else -> log.error("failed", cause)
    }
}
```

### 9.3 Off-heap data via `kotlinx-io 0.5+`

For KMP-compatible binary protocols (e.g., parsing TLV, framed binary), use `kotlinx-io`'s `Buffer` — a linked-list of segments that grow without copying. Avoids `java.nio.ByteBuffer` (JVM-only) and is memory-efficient.

### 9.4 Threading model

- **JVM**: traditional thread-pool model. `Dispatchers.Default` is fixed (≈ CPU count); `Dispatchers.IO` is elastic (up to 64).
- **Kotlin/Native (1.7.20+)**: new memory model — shared mutable state allowed across threads, GC, no more `frozen` objects. Coroutines work natively.
- **Project Loom virtual threads + coroutines**: experimental. You can wrap a `newVirtualThreadPerTaskExecutor()` into a `CoroutineDispatcher`. For pure blocking-IO workloads, a virtual-thread dispatcher can be ~30× faster than `Dispatchers.IO` on JDK 21+. Wait for the official `Dispatchers.LOOM` (or equivalent) before committing in production — the coroutines team has signalled deeper integration is being designed.

```kotlin
// Experimental Loom interop
val loomDispatcher = Executors.newVirtualThreadPerTaskExecutor()
    .asCoroutineDispatcher()

suspend fun fetchAll(urls: List<String>): List<Response> = withContext(loomDispatcher) {
    urls.map { async { http.get(it) } }.awaitAll()
}
```

### 9.5 `atomicfu` for KMP-friendly atomics

```kotlin
import kotlinx.atomicfu.atomic

class Counter {
    private val count = atomic(0)
    fun inc() = count.incrementAndGet()
    fun current() = count.value
}
```

- Compiles to JVM `AtomicInteger`, K/Native atomics, JS volatile field, Wasm atomics.
- Replaces `java.util.concurrent.atomic.AtomicInteger` (JVM-only) when you want KMP.

---

## 10. Production Library Matrix (2026 Baseline)

### 10.1 HTTP

| Need | Library | Notes |
|---|---|---|
| Server | **Ktor 3.4+** | Default for new KMP/JVM services |
| Server (Spring shop) | Spring Boot 3.x + Kotlin | Webflux for reactive, MVC for sync |
| Client (KMP) | **Ktor client 3.x** | OkHttp engine on Android, Darwin on iOS, Java on JVM, JS on Web |
| Client (Android-only legacy) | OkHttp + Retrofit | Mature but Android-only |
| Client (JVM-only) | java.net.http (`HttpClient`) | Standard since JDK 11 |

### 10.2 Database

| Need | Library | Notes |
|---|---|---|
| JVM sync, type-safe DSL | **Exposed 1.0+** | DSL or DAO; Jan 2026 GA |
| JVM reactive | **Exposed R2DBC** (new in 1.0) or `jOOQ + jooq-kotlin-coroutines` | jOOQ adds richer SQL coverage |
| Spring | Spring Data JPA (sync) / Spring Data R2DBC (reactive) | Existing ecosystem |
| KMP | **SQLDelight** | `.sq` files compile to Kotlin; multi-target |
| Android-shared-with-KMP | **Room KMP** (since Room 2.7+) | If already a Room codebase |
| Realtime / sync | Realm Kotlin | If you need MongoDB Realm sync |

### 10.3 Serialization

| Need | Library |
|---|---|
| KMP / Kotlin-native | **`kotlinx.serialization`** (default) — JSON, ProtoBuf, CBOR, XML |
| Spring | Jackson Kotlin module (`com.fasterxml.jackson.module.kotlin`) |
| Android only | Moshi (with KSP) |
| ProtoBuf with rich code gen | `kotlinx.serialization.protobuf` or `protobuf-kotlin` (official) |
| Avro | `avro4k` |

### 10.4 DI

| Need | Library |
|---|---|
| KMP | **Koin 4.x** (no codegen, easy iOS interop) — first choice |
| KMP with compile-time checks | **kotlin-inject** (KSP-based, Dagger-style) |
| KMP newer entrant | **Metro** (compile-time, fast) |
| Android-only | Hilt — fastest start, but no iOS / no KMP |

### 10.5 Logging

| Need | Library |
|---|---|
| JVM | **`io.github.oshai:kotlin-logging`** (wraps SLF4J) — `private val log = KotlinLogging.logger {}` |
| KMP | **Kermit** (Touchlab) — platform-specific backends |
| Server structured logs | SLF4J + `logstash-logback-encoder` JSON encoder |

### 10.6 Reactive / async

| Need | Library |
|---|---|
| Default | `kotlinx.coroutines` + `Flow` |
| Spring WebFlux | Project Reactor (`Mono` / `Flux`) — bridge with `kotlinx-coroutines-reactor` |
| RxJava migration | `kotlinx-coroutines-rx3` for incremental migration |

### 10.7 Crypto

| Need | Library |
|---|---|
| JVM, FIPS, full algorithm coverage | **BouncyCastle + bc-kotlin** (Kotlin DSL on top of BC) |
| KMP, modern algorithms, OpenSSL backend | **`cryptography-kotlin`** (by whyoleg) — wraps OpenSSL 3.x / WebCrypto / JCA |
| KMP, BouncyCastle-pattern | **KmpCrypto** (skolson) |

### 10.8 CLI

| Need | Library |
|---|---|
| Default | **Clikt 4.x** — Kotlin-idiomatic, type-safe options/args/subcommands |
| Lightweight | `kotlinx.cli` (official, simpler) |
| Spring CLI | Spring Shell |

### 10.9 Networking lower-level

| Need | Library |
|---|---|
| KMP TCP/UDP | **`ktor-network`** |
| KMP I/O primitives | **`kotlinx-io`** (Buffer/Source/Sink) |

### 10.10 Date / time

| Need | Library |
|---|---|
| KMP | **`kotlinx-datetime`** (Instant moved to stdlib in Kotlin 2.2, datetime 0.7.0+ uses `kotlin.time.Instant`) |
| JVM only | `java.time` (use it directly — kotlinx-datetime just wraps and harmonizes) |
| `Clock` abstraction | `kotlin.time.Clock.System` (stdlib since 2.2) — inject for testability |

### 10.11 Atomics

| Need | Library |
|---|---|
| KMP | **`kotlinx-atomicfu`** |
| JVM-only | `java.util.concurrent.atomic` |

### 10.12 Validation

| Need | Library |
|---|---|
| Kotlin-idiomatic DSL | **Konform** (`Validation<T> { ... }` builder) |
| Bean Validation 3.0 style | **Valiktor** |
| Spring | `jakarta.validation` (Hibernate Validator) |

### 10.13 State machine

| Need | Library |
|---|---|
| DSL state machine | `Tinder/StateMachine` (Kotlin DSL) |
| MVI framework | **FlowMVI** (highly featured), **Ballast**, **MVIKotlin** (KMP), **Decompose** (navigation + MVI for KMP) |

### 10.14 Compose Multiplatform (UI when shared UI is justified)

- **Compose Multiplatform 1.11.0** (May 2026) — stable on Android, iOS, Desktop; web target is Beta.
- Use when brand-led identical visuals matter or for B2B/internal tools. For consumer apps where platform feel matters → native UI per platform with shared KMP business logic (UI implementation itself is covered by the [`native` skill](../../native/SKILL.md)).

---

## 11. Architecture Patterns in Kotlin

### 11.1 Clean / Hexagonal

```kotlin
// domain (pure Kotlin, no framework deps)
interface UserRepository {
    suspend fun findById(id: UserId): User?
    suspend fun save(user: User)
}

class CreateUserUseCase(private val repo: UserRepository, private val clock: Clock) {
    suspend operator fun invoke(req: CreateUserCommand): UserId {
        val user = User(UserId.new(), req.name, req.email, clock.now())
        repo.save(user)
        return user.id
    }
}

// adapter (infrastructure, depends on domain)
class JdbcUserRepository(private val db: Database) : UserRepository {
    override suspend fun findById(id: UserId): User? = /* ... */
    override suspend fun save(user: User) = /* ... */
}
```

- Domain layer has zero framework imports.
- Adapters depend on domain interfaces, never the reverse.

### 11.2 MVVM on Android (legacy-friendly)

```kotlin
class UserViewModel(private val repo: UserRepository) : ViewModel() {
    private val _state = MutableStateFlow<UiState>(UiState.Initial)
    val state: StateFlow<UiState> = _state.asStateFlow()

    fun load(id: UserId) {
        viewModelScope.launch {
            _state.update { UiState.Loading }
            runCatching { repo.findById(id) }
                .onSuccess { _state.update { UiState.Success(it) } }
                .onFailure { e -> _state.update { UiState.Error(e.message ?: "Unknown") } }
        }
    }
}

sealed interface UiState {
    data object Initial : UiState
    data object Loading : UiState
    data class Success(val user: User?) : UiState
    data class Error(val message: String) : UiState
}
```

The View/Composable side of this pattern (`collectAsStateWithLifecycle`, `repeatOnLifecycle`) belongs to the [`native` skill](../../native/SKILL.md).

### 11.3 MVI with reducers

```kotlin
sealed interface Intent {
    data class Load(val id: UserId) : Intent
    data object Refresh : Intent
}

sealed interface UiState {
    data object Loading : UiState
    data class Loaded(val user: User) : UiState
    data class Failed(val cause: Throwable) : UiState
}

class UserStore(private val repo: UserRepository) {
    private val _state = MutableStateFlow<UiState>(UiState.Loading)
    val state: StateFlow<UiState> = _state

    fun send(intent: Intent) = viewModelScope.launch {
        _state.update { reduce(it, intent) }
    }

    private suspend fun reduce(current: UiState, intent: Intent): UiState = when (intent) {
        is Intent.Load -> runCatching { repo.findById(intent.id) }
            .fold({ UiState.Loaded(it!!) }, { UiState.Failed(it) })
        Intent.Refresh -> current
    }
}
```

### 11.4 Repository pattern with Flow

```kotlin
interface UserRepository {
    fun observeUser(id: UserId): Flow<User?>          // cold; subscribers reactivate as data changes
    suspend fun refresh(id: UserId)                    // one-shot side effect
}

class DefaultUserRepository(
    private val api: UserApi,
    private val cache: UserCache,
) : UserRepository {
    override fun observeUser(id: UserId): Flow<User?> = cache.observe(id)

    override suspend fun refresh(id: UserId) {
        val fresh = api.getUser(id.raw)
        cache.put(fresh)
    }
}
```

### 11.5 Sealed-class state modeling

```kotlin
sealed interface Result<out T> {
    data class Success<T>(val value: T) : Result<T>
    data class Failure(val cause: Throwable) : Result<Nothing>
    data object Loading : Result<Nothing>
}

// Exhaustive when
fun render(r: Result<User>) = when (r) {
    is Result.Success -> showUser(r.value)
    is Result.Failure -> showError(r.cause)
    Result.Loading -> showSpinner()
}
```

`sealed interface` (since 1.5) and `data object` (since 1.9) are 2026 best-practice for sum types in Kotlin.

### 11.6 Result-type alternatives

| Choice | When |
|---|---|
| **stdlib `kotlin.Result<T>`** | Quick wrap; **don't return it from public APIs** (KEEP-warning); fine for `catching { }` scope |
| **`Arrow Either<E, A>`** | Domain errors as types; railway-oriented programming; effects DSL (`either { ... }`) |
| **`kotlin-result` (michaelbull)** | Lightweight, multiplatform, no Arrow dependency; `Result<V, E>` with explicit error generic |
| **Custom sealed class `Outcome<T, E>`** | Domain-specific; no boxing overhead vs `kotlin.Result` |

```kotlin
// Arrow Either example
import arrow.core.Either
import arrow.core.raise.either

sealed interface CreateUserError {
    data object EmailInvalid : CreateUserError
    data object DuplicateEmail : CreateUserError
    data class Repository(val cause: Throwable) : CreateUserError
}

suspend fun createUser(req: CreateUserRequest): Either<CreateUserError, UserId> = either {
    val email = Email.parse(req.email).bind()              // short-circuits on Left
    ensure(!repo.emailExists(email)) { CreateUserError.DuplicateEmail }
    val user = User(UserId.new(), req.name, email)
    runCatching { repo.save(user) }
        .getOrElse { raise(CreateUserError.Repository(it)) }
    user.id
}
```

### 11.7 Context parameters (Kotlin 2.2 preview → 2.3 callable refs)

Replacing the experimental context receivers. Stabilizing in 2.3 (Jun-Jul 2026).

```kotlin
context(logger: Logger)
fun doWork(input: String) {
    logger.info("processing $input")
    // ...
}

context(logger = ConsoleLogger())
{
    doWork("hello")
}
```

Don't refactor early — wait for 2.3 stable and tooling support. Full migration detail (including the rename from `context(Foo, Bar) fun` to `context(foo: Foo, bar: Bar) fun`) is in [`kotlin-language-spec.md` §10](./kotlin-language-spec.md#10-context-receivers--context-parameters).

---

## 12. Documentation

### 12.1 KDoc syntax

```kotlin
/**
 * Looks up a user by their identifier.
 *
 * Uses an in-memory cache first; falls back to the network when the cache
 * is cold. The returned user is guaranteed to be non-null on success.
 *
 * @param id the unique identifier; must match the format of [UserId].
 * @return the user, or `null` if no user with [id] exists.
 * @throws NetworkException when the upstream fetch fails after retries.
 * @sample com.example.docs.lookupUserSample
 */
suspend fun lookupUser(id: UserId): User? { /* ... */ }
```

| Tag | Use for |
|---|---|
| `@param name desc` | parameter documentation |
| `@return desc` | return value |
| `@throws ExceptionType desc` / `@exception` | declared/checked exceptions |
| `@sample fully.qualified.fn` | embed a code sample |
| `@receiver desc` | extension function receiver |
| `@property name desc` | property of a class (used in class-level KDoc) |
| `@constructor desc` | primary constructor (class-level KDoc) |
| `@see [Type]`, `@see fully.qualified.name` | cross-reference |
| `@since 1.2.0` | version added |
| `@suppress` | hide from generated docs |

**Inline references**: `[symbol]` resolves to the symbol in the current scope. Prefer `[id]` over `` `id` `` in prose — IDE shows it as a link.

### 12.2 Dokka

- **Dokka 2.x** (KSP-based) is the generator.
- For multi-module: apply `org.jetbrains.dokka` in each module, then aggregate in the root.

```kotlin
// root build.gradle.kts
plugins {
    id("org.jetbrains.dokka") version "2.0.0"
}

subprojects {
    apply(plugin = "org.jetbrains.dokka")
}

tasks.dokkaHtmlMultiModule {
    outputDirectory.set(rootDir.resolve("docs/api"))
}
```

- Output format: `dokkaHtml` (default), `dokkaGfm` (GitHub Markdown), `dokkaJekyll`.
- **GitHub Pages hosting**: push the `docs/api/` output to a `gh-pages` branch via GitHub Actions.

### 12.3 Documentation conventions

- KDoc only on public/internal API (don't document `private`).
- First sentence is the summary — appears in completion popups.
- Avoid restating the signature: a function named `addUser(user: User)` doesn't need "Adds a user." as its only line.
- Use `@sample` for non-trivial usage; samples live in a separate `samples/` source set.

---

## 13. Release & Distribution

### 13.1 Versioning

- **SemVer 2.0.0** strictly: `MAJOR.MINOR.PATCH`.
- Pre-release: `1.0.0-alpha01`, `1.0.0-rc1`.
- API breaks → MAJOR bump. Use the **binary-compatibility-validator** plugin to lock the public API surface:

```kotlin
plugins { id("org.jetbrains.kotlinx.binary-compatibility-validator") version "0.16.3" }
```

### 13.2 Publishing — Sonatype Central Portal (new since 2024)

Since June 2024, **OSSRH (`oss.sonatype.org`) is replaced by Central Portal (`central.sonatype.com`)**. All new namespaces must register on the Portal.

**Authentication**:
1. Register namespace on Central Portal.
2. Verify domain ownership via TXT DNS or GitHub repo proof.
3. Generate user token (Portal account settings).

**Gradle setup** (recommended: `vanniktech/gradle-maven-publish-plugin` — handles Central Portal, signing, javadoc):

```kotlin
plugins {
    id("com.vanniktech.maven.publish") version "0.30.0"
}

mavenPublishing {
    publishToMavenCentral()
    signAllPublications()
    coordinates("com.example", "my-library", "1.0.0")
    pom {
        name.set("My Library")
        description.set("A useful library")
        inceptionYear.set("2026")
        url.set("https://github.com/example/my-library")
        licenses { license { name.set("Apache-2.0"); url.set("...") } }
        developers { developer { id.set("alice"); name.set("Alice") } }
        scm { url.set("..."); connection.set("..."); developerConnection.set("...") }
    }
}
```

The plugin automatically:
- Builds sources JAR, javadoc JAR (via Dokka if applied).
- Signs all artifacts with GPG.
- Uploads to Central Portal.
- Handles staging → release transition.

**JReleaser** is an alternative for complex multi-target releases (binaries + tarballs + docker images alongside JARs).

### 13.3 KMP publishing

KMP artifacts include multiple targets. The Kotlin Multiplatform Gradle Plugin auto-generates per-target publications when `maven-publish` is applied:

```
com.example:my-library:1.0.0              → root, metadata
com.example:my-library-jvm:1.0.0          → JVM target
com.example:my-library-android:1.0.0      → Android target
com.example:my-library-iosarm64:1.0.0     → iOS arm64 target
com.example:my-library-iossimulatorarm64  → iOS simulator arm64
...
```

`vanniktech` plugin handles this transparently.

### 13.4 Reproducible builds

```kotlin
tasks.withType<AbstractArchiveTask> {
    isPreserveFileTimestamps = false
    isReproducibleFileOrder = true
}
```

Set `SOURCE_DATE_EPOCH` env var in CI for deterministic timestamps.

### 13.5 Release automation

- Tag-driven: `v1.0.0` Git tag triggers GitHub Actions → publish.
- Conventional commits → auto-generate CHANGELOG.md via `conventional-changelog` or `kotlin-semantic-release`.

---

## 14. 2023 → 2026 Migration Cheatsheet

| 2023 idiom / library | 2026 replacement | Notes |
|---|---|---|
| `LiveData<T>` | `StateFlow<T>` | Use `collectAsStateWithLifecycle()` in Compose; `repeatOnLifecycle(STARTED)` in Views. `LiveData` still works but new code uses StateFlow. |
| `kapt(...)` | `ksp(...)` | KAPT deprecated for K2. KSP2 default in Kotlin 2.2+. Library compatibility: Room, Moshi, Hilt, Dagger 2.51+, Koin annotations all support KSP. Drop `kapt.use.k2=false` only for blockers. |
| `Channel<T>` for events | `SharedFlow<T>` with `extraBufferCapacity = 1, onBufferOverflow = DROP_OLDEST` | Channels are still the right tool for producer-consumer queues; for **broadcast events** use SharedFlow. |
| `BroadcastChannel<T>` | `SharedFlow<T>` | `BroadcastChannel` is deprecated since coroutines 1.4. |
| `Pair<First, Second>` returned from a function | `data class` with named fields | "`Pair`" hides intent at call sites. |
| `data class` with 20 fields modelling identity-only types | `@JvmInline value class XxxId(val raw: ...)` | Type-safe ID separation; near-zero cost. |
| `Spring Boot` for greenfield microservice (no Spring history) | **Ktor 3.x** | Lighter, coroutines-first, KMP-friendly. Keep Spring when team is Spring-shop or you need Spring ecosystem (Cloud, Security, Data). |
| `Mockito` (`-kotlin`) | **MockK** | Native Kotlin support, coroutines (`coEvery` / `coVerify`), object/static mocking. |
| Java `CompletableFuture<T>` | `suspend fun` + `await()` bridge | `future.await()` from `kotlinx-coroutines-jdk8`. |
| `java.time.Instant` in `commonMain` | `kotlin.time.Instant` (Kotlin 2.2+) | Moved from `kotlinx-datetime` into stdlib; KMP-friendly. |
| `runBlocking { }` in test | `runTest { }` | Virtual time, test dispatcher, structured cancellation. |
| `GlobalScope.launch` | Scoped coroutine (`viewModelScope`, request scope, custom `CoroutineScope`) | `GlobalScope` is for top-level entry points only. |
| `Mockito Inline` for static / object mocking | `mockkStatic` / `mockkObject` | Built into MockK. |
| Groovy `build.gradle` | `build.gradle.kts` Kotlin DSL | Required for K2 type-safe accessors and convention plugins. |
| Inline dependency strings in `build.gradle.kts` | **`gradle/libs.versions.toml` version catalog** | Single source of truth; type-safe accessors. |
| `buildSrc` for convention plugins | `build-logic` included build | Better build cache, isolated classpath. |
| `kotlin.android.extensions` (synthetic views) | View Binding (Android) or Compose | `kotlin-android-extensions` is removed since Kotlin 1.8. |
| Coroutines `withContext(Dispatchers.IO + name)` (custom CoroutineName) | `Dispatchers.IO.limitedParallelism(n, name)` | Named limited views since coroutines 1.8. |
| `kotlinx-coroutines-core-jvm` direct dep | `kotlinx-coroutines-core` (Gradle resolves variant) | Don't pin platform-specific artifacts. |
| Custom Result type wrapping `Try<T>` (Arrow 1.x) | `Either<E, A>` (Arrow 2.x) or `kotlin-result.Result<V, E>` | Arrow 2.x dropped `Try`. |
| `@Parcelize` on Java-only Android | KMP-safe `@Serializable` + parcel adapter | If you need KMP, drop `@Parcelize`. |
| `kapt` for Dagger | `ksp` for Dagger 2.51+ | 2× faster builds. |
| Direct `kotlinx-coroutines-rx2` usage | `kotlinx-coroutines-rx3` | RxJava 2 EOL since 2021; migrate to RxJava 3 then to Flow. |
| `kotlin-serialization 1.6` `@Serializable` with Java `Date` field | `kotlinx-datetime` `Instant` + `kotlinx-serialization 1.9` | Old `Date` serializers are deprecated. |
| Context receivers (`context(Foo)`) experimental | **Context parameters** (Kotlin 2.3 callable refs) | Migrate after 2.3 GA. |
| OSSRH (`oss.sonatype.org`) publishing | **Sonatype Central Portal** (`central.sonatype.com`) | OSSRH retired in 2024; use `vanniktech/gradle-maven-publish-plugin` for the new flow. |

---

## 15. Appendix A — Quick-Reference Decision Cheat Sheets

### Coroutine dispatcher choice

```
CPU-bound work       → Dispatchers.Default     (≈ CPU cores)
File / DB / Network  → Dispatchers.IO          (elastic, up to 64)
UI thread (Android)  → Dispatchers.Main        (or Main.immediate)
Bounded resource     → Dispatchers.IO.limitedParallelism(n)   // create ONCE in DI
Test                 → UnconfinedTestDispatcher / StandardTestDispatcher
```

### Flow vs StateFlow vs SharedFlow

```
Single-shot async   → suspend fun
Cold stream         → Flow<T>
Hot state           → StateFlow<T>          (always has value, conflates)
Hot events          → SharedFlow<T>         (no replay, buffered)
Internal queue      → Channel<T>            (low-level, prefer Flow above)
```

### Visibility modifier rule of thumb

```
default     → public            (Kotlin's default)
library     → explicitApi()     (force authors to declare)
member      → private           (smaller surface = fewer bugs)
across modules in same project → internal
```

### Scope-function decision matrix

| Function | Receiver inside | Returns        | Use when                                            |
| -------- | --------------- | -------------- | --------------------------------------------------- |
| `let`    | `it`            | lambda result  | Transform / chain on nullable / produce new value   |
| `also`   | `it`            | receiver       | Side effect (log / track) — return same object      |
| `apply`  | `this`          | receiver       | Configure / mutate — return same object             |
| `run`    | `this`          | lambda result  | Compute over receiver — return computed value       |
| `with`   | `this` (arg)    | lambda result  | Like `run` but for non-receiver case (older style)  |

### `requireNotNull` vs `checkNotNull` vs `!!`

| Situation                                                        | Use                  | Throws                          |
| ---------------------------------------------------------------- | -------------------- | ------------------------------- |
| Validating a **function argument** (public/external entry point) | `requireNotNull(x)`  | `IllegalArgumentException`      |
| Validating **internal state** of an object                       | `checkNotNull(x)`    | `IllegalStateException`         |
| You **truly know** it's not null and want a value (private code) | `x!!` (rarely)       | `NullPointerException`          |
| External boundary — user input / parsed JSON                     | `?: throw DomainException(...)` | domain-specific exception |

### `LazyThreadSafetyMode` decision matrix

| Mode             | Locking         | Threads compute            | Result published                 | When to use                                                                              |
| ---------------- | --------------- | -------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------- |
| `SYNCHRONIZED` (default) | Lock            | Only one (others wait)     | One value                        | Multi-threaded access + initializer is expensive AND idempotent. Safe default.           |
| `PUBLICATION`    | CAS (lock-free) | Possibly many concurrently | First-wins CAS                   | Multi-threaded access + initializer is **cheap** (re-running fine).                      |
| `NONE`           | None            | Possibly many concurrently | **Undefined** if cross-thread    | Single-thread only (UI-only data, init phase). Use with care.                            |

---

## 16. Sources

### Kotlin official

- [Kotlin Coding Conventions — Official Docs](https://kotlinlang.org/docs/coding-conventions.html)
- [What's new in Kotlin 2.0.0 (K2)](https://kotlinlang.org/docs/whatsnew20.html)
- [What's new in Kotlin 2.2.0](https://kotlinlang.org/docs/whatsnew22.html)
- [What's new in Kotlin 2.3.0](https://kotlinlang.org/docs/whatsnew23.html)
- [Compatibility guide for Kotlin 2.0.x](https://kotlinlang.org/docs/compatibility-guide-20.html)
- [Kotlin Multiplatform Hierarchy Template](https://kotlinlang.org/docs/multiplatform-hierarchy.html)
- [Stability of supported KMP platforms](https://kotlinlang.org/docs/multiplatform/supported-platforms.html)
- [Migrate from kapt to KSP](https://kotlinlang.org/docs/ksp-kapt-migration.html)
- [Gradle Best Practices — Kotlin Docs](https://kotlinlang.org/docs/gradle-best-practices.html)
- [Power-assert compiler plugin](https://kotlinlang.org/docs/power-assert.html)
- [Update on Context Parameters — The Kotlin Blog](https://blog.jetbrains.com/kotlin/2025/04/update-on-context-parameters/)

### JetBrains blog (release-tier)

- [Ktor 3.4.0 Release — The Kotlin Blog (Jan 2026)](https://blog.jetbrains.com/kotlin/2026/01/ktor-3-4-0-is-now-available/)
- [Exposed 1.0 Release — The Kotlin Blog (Jan 2026)](https://blog.jetbrains.com/kotlin/2026/01/exposed-1-0-is-now-available/)
- [Compose Multiplatform 1.11.0 — The Kotlin Blog (May 2026)](https://blog.jetbrains.com/kotlin/2026/05/compose-multiplatform-1-11-0/)
- [KotlinConf'26 Keynote Highlights](https://blog.jetbrains.com/kotlin/2026/05/kotlinconf26-keynote-highlights/)

### Effective Kotlin (Marcin Moskala) on kt.academy

- [Item 52: Inline value classes](https://kt.academy/article/ek-value-classes)
- [Item 54: Prefer Sequences for big collections](https://kt.academy/article/ek-sequence)
- [Property delegation](https://kt.academy/article/ak-property-delegation)
- [Coroutines Dispatchers](https://kt.academy/article/cc-dispatchers)
- [Running Kotlin coroutines on Project Loom's virtual threads](https://kt.academy/article/dispatcher-loom)

### Engineering deep-dives

- [Roman Elizarov — Shared Flows, Broadcast Channels](https://elizarov.medium.com/shared-flows-broadcast-channels-899b675e805c)
- [Manuel Vivo — StateFlow and SharedFlow](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [Manuel Vivo — Testing Kotlin flows on Android](https://developer.android.com/kotlin/flow/test)
- [Chris Banes — Should you use Kotlin Sequences for Performance?](https://chrisbanes.me/posts/use-sequence/)
- [kotlinx.coroutines `limitedParallelism` API](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-dispatcher/limited-parallelism.html)

### Library landing pages

- [Dokka — Kotlin/dokka GitHub](https://github.com/Kotlin/dokka)
- [Ktor Application Structure](https://ktor.io/docs/server-application-structure.html)
- [kotlinx-io — Kotlin/kotlinx-io GitHub](https://github.com/Kotlin/kotlinx-io)
- [kotlinx-atomicfu — Kotlin/kotlinx-atomicfu GitHub](https://github.com/Kotlin/kotlinx-atomicfu)
- [kotlinx-benchmark — Kotlin/kotlinx-benchmark GitHub](https://github.com/Kotlin/kotlinx-benchmark)
- [kotlinx.serialization Releases](https://github.com/Kotlin/kotlinx.serialization/releases)
- [Koin KMP Advanced Patterns](https://insert-koin.io/docs/reference/koin-mp/kmp/)
- [MockK — mockk.io](https://mockk.io/)
- [Kotest](https://kotest.io/)
- [kotlin-result — michaelbull GitHub](https://github.com/michaelbull/kotlin-result)
- [cryptography-kotlin — whyoleg GitHub](https://github.com/whyoleg/cryptography-kotlin)
- [kotlin-logging — oshai GitHub](https://github.com/oshai/kotlin-logging)
- [vanniktech/gradle-maven-publish-plugin Releases](https://github.com/vanniktech/gradle-maven-publish-plugin/releases)
- [Kotlin Multiplatform Tutorial: Ktor + SQLDelight](https://kotlinlang.org/docs/multiplatform/multiplatform-ktor-sqldelight.html)
