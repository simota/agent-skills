# Kotlin Refactoring Cheatsheet (Kotlin 2.3+ / K2)

Purpose: Zen-flavored slice of the Kotlin knowledge base — code-smell-to-idiom transformations, naming hygiene, scope-function discipline, and refactor anti-patterns. Behavior-preserving only.

Baseline: **Kotlin 2.3+, K2 compiler, KSP2 default**.

Source of truth (do not duplicate here):
- Bad-pattern catalog → [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md)
- Target idioms / Style Guide / Effective Kotlin → [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md)
- Language surface (K2, context parameters preview, sealed/value classes) → [`builder/reference/kotlin-language-spec.md`](../../builder/reference/kotlin-language-spec.md)

Companion: [`language-patterns.md`](./language-patterns.md) holds the cross-language Kotlin quick-pattern set. Read this file for refactor-specific transformations.

---

## Contents

- [Smell → Idiom Map](#smell--idiom-map)
- [Function Extraction Signals (Kotlin-specific)](#function-extraction-signals-kotlin-specific)
- [Naming Hygiene (Kotlin Style Guide)](#naming-hygiene-kotlin-style-guide)
- [Scope Function Decision Matrix](#scope-function-decision-matrix)
- [Magic Numbers and Strings](#magic-numbers-and-strings)
- [Coroutine / Flow Refactors](#coroutine--flow-refactors)
- [Refactor Anti-Patterns to Avoid](#refactor-anti-patterns-to-avoid)
- [Refactor Checklist](#refactor-checklist)

---

## Smell → Idiom Map

| Smell | Idiom | Notes |
|-------|-------|-------|
| `if (x != null) { if (y != null) { ... } }` nested | `?.let { ... }` chain, `?:` Elvis fallback, or single `if (x != null && y != null)` | Smart-cast still works under the `&&` form |
| `if/else` ladder dispatching on value | `when` expression | `when` is exhaustive on sealed types; the compiler catches missing branches |
| Java-style getters/setters | Kotlin property | `fun getName() = name` → `val name: String`; custom getter only when value is computed |
| `var` reflex when `val` works | `val` + functional transform | Prefer immutability; `var` is allowed but should be local and short-lived |
| `try { ... } catch (e: Exception) { }` swallowed | Typed catch (`catch (e: IOException)`) or `runCatching { ... }.getOrElse` | Never catch `Exception`/`Throwable` blindly — that includes `CancellationException` (anti-patterns §2) |
| `Channel<T>` for last-value state | `StateFlow<T>` | `StateFlow` is conflated, has `value`, and is hot |
| `Channel<T>` for fire-and-forget events | `SharedFlow<T>` (or `Channel` only when you need send-suspension semantics) | `SharedFlow` allows replay buffer; `Channel` is for hand-off |
| `LiveData<T>` on Android | `StateFlow<T>` + `collectAsStateWithLifecycle` (Compose) | LiveData is legacy; Flow integrates with coroutines |
| Manual builder class with mutable setters | `data class` + `copy(...)` | Builders survive only when you cross JVM boundaries that need fluent setters |
| Anonymous `object : OnClickListener` for SAM | Lambda when SAM is `fun interface` (Kotlin) | Java SAM autoconverts; Kotlin needs `fun interface` to autoconvert |
| `Pair<First, Second>` or `Triple<...>` overuse | `data class Position(val x: Int, val y: Int)` | Pair/Triple lose names; readability tanks at the call site |
| `data class UserId(val value: String)` | `@JvmInline value class UserId(val value: String)` | No boxing on the JVM hot path |
| `companion object { fun util() = ... }` for pure utility | Top-level function | Companion is for static-like access from Java only; pure functions belong at top level |
| Java `Optional<T>` | Nullable `T?` | Don't import `java.util.Optional` into Kotlin code; nullable is the idiom |
| `lateinit var` reflex for DI | Constructor injection where possible | `lateinit` is for framework-init (Spring `@Autowired`, Android `Inject`); not a general-purpose nullable workaround |
| kapt annotation processor | KSP2 | KSP2 is the default since Kotlin 2.0; kapt is legacy. Migration is per-processor (anti-patterns §13, §14) |
| `runBlocking { ... }` in app code | `viewModelScope`/`lifecycleScope`/`coroutineScope { }` | `runBlocking` is for `main()` and tests only; in app code it blocks the calling thread |
| Context receivers (experimental, deprecated 2.0+) | Context parameters preview (2.3) or extension functions | Context receivers were never stabilized; rewrite to extension fns or context parameters |
| `if (list.isEmpty()) return; list.forEach { ... }` | `list.takeIf { it.isNotEmpty() }?.forEach { ... }` OR keep the guard — depends on readability | Don't reach for `takeIf` if `if` reads better |
| `list.filter { ... }.map { ... }.first()` | `list.firstOrNull { predicate }?.let { transform(it) }` | Short-circuits; avoids allocating intermediate lists |

### Selected before/after snippets

#### Nested null check → `?.let`

```kotlin
// Before
fun cityOf(user: User?): String? {
    if (user != null) {
        if (user.address != null) {
            if (user.address.city != null) {
                return user.address.city
            }
        }
    }
    return null
}

// After
fun cityOf(user: User?): String? =
    user?.address?.city
```

#### `if/else` ladder → `when`

```kotlin
// Before
fun statusOf(code: Int): String {
    if (code == 200) return "ok"
    else if (code in 300..399) return "redirect"
    else if (code in 400..499) return "client error"
    else if (code >= 500) return "server error"
    else return "unknown"
}

// After
fun statusOf(code: Int): String = when (code) {
    200      -> "ok"
    in 300..399 -> "redirect"
    in 400..499 -> "client error"
    in 500..599 -> "server error"
    else     -> "unknown"
}
```

#### `Pair` overuse → `data class`

```kotlin
// Before
fun parseCoord(s: String): Pair<Int, Int> { /* ... */ }
val p = parseCoord("3,4")
println(p.first)  // What does .first mean here?

// After
data class Coord(val x: Int, val y: Int)
fun parseCoord(s: String): Coord { /* ... */ }
val c = parseCoord("3,4")
println(c.x)
```

#### Primitive ID → `value class`

```kotlin
// Before
fun ban(userId: String, byAdmin: String) { /* easy to swap */ }

// After
@JvmInline value class UserId(val value: String)
@JvmInline value class AdminId(val value: String)

fun ban(userId: UserId, byAdmin: AdminId) { /* compiler-enforced, zero JVM overhead */ }
```

#### `LiveData` → `StateFlow`

```kotlin
// Before
class CounterVM : ViewModel() {
    private val _count = MutableLiveData(0)
    val count: LiveData<Int> = _count
    fun inc() { _count.value = (_count.value ?: 0) + 1 }
}

// After
class CounterVM : ViewModel() {
    private val _count = MutableStateFlow(0)
    val count: StateFlow<Int> = _count.asStateFlow()
    fun inc() { _count.update { it + 1 } }
}
```

#### `runCatching` over silent `catch`

```kotlin
// Before
fun parse(s: String): Int {
    return try { s.toInt() } catch (e: Exception) { 0 }   // swallows CancellationException too
}

// After
fun parse(s: String): Int =
    s.toIntOrNull() ?: 0
// or for arbitrary blocks:
fun fetch(): Result<Data> = runCatching { client.fetch() }
```

#### Companion utility → top-level function

```kotlin
// Before
class StringTools {
    companion object {
        fun slugify(s: String): String = s.lowercase().replace(' ', '-')
    }
}
StringTools.slugify("Hello World")

// After
// in StringTools.kt
fun slugify(s: String): String = s.lowercase().replace(' ', '-')

slugify("Hello World")
```

---

## Function Extraction Signals (Kotlin-specific)

Extract a helper when you see:

1. **A lambda block > 15 lines** — particularly inside `apply`/`also`/`let`/`run` chains. Long lambdas read worse than named functions.
2. **Nested scope-function chains** (`x.let { it.also { it.apply { ... } } }`) — almost always means one of them was unnecessary. Pick one tool per layer.
3. **Three or more repeated `?.let { }` blocks on the same shape** — extract a `private fun` that returns the unwrapped value (or `null`).
4. **`when` arms with shared post-processing** — extract the post-processing as a free function; arms reduce to value construction.
5. **`Flow` chain > 5 operators inline** — break at named intermediate Flows; each named step becomes a `private fun ...: Flow<X>`.
6. **A `class` with one public method** — convert to a top-level extension function or a `fun interface` if multiple impls exist.

Counter-signals (do NOT extract):
- A 3-line block used in one place — inline it.
- A helper that requires `internal` visibility just to be referenced once — keep inline.
- An extracted function that needs 5+ parameters threading through — that means you extracted at the wrong seam.

---

## Naming Hygiene (Kotlin Style Guide)

Follow the official Kotlin Coding Conventions [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) §1.

| Item Kind | Convention | Example |
|-----------|-----------|---------|
| Package | All lowercase, no underscore | `com.acme.billing` |
| Class, interface, object, typealias | `UpperCamelCase` | `OrderRepository`, `BillingScope` |
| Function, property, parameter, local | `lowerCamelCase` | `loadUser(id)`, `pendingOrders` |
| Compile-time constant (`const val`) | `SCREAMING_SNAKE_CASE` | `const val MAX_RETRIES = 3` |
| Top-level / object `val` immutable, non-const | `lowerCamelCase` | `val defaultClient = HttpClient(...)` |
| Enum entry | `UpperCamelCase` (preferred) or `SCREAMING_SNAKE_CASE` (allowed) | `Status.Active`, `Status.ACTIVE` — pick one and be consistent |
| Type parameter | `UpperCamelCase`, descriptive | `Element`, `Failure`, not `T` unless universally generic |
| Test function | Backticks allowed for readable names | `` fun `returns null when input is blank`() `` |

### Function naming

- **Returns Boolean**: prefix with `is`/`has`/`can` — `isEmpty()`, `hasNext()`, `canRetry()`.
- **Pure transform**: noun-or-adjective phrase — `String.uppercase()`, not `String.toUppercase()` (the `to` prefix is reserved for type conversion).
- **Mutating action**: imperative verb — `MutableList<T>.add(x)`, `Channel.send(x)`.
- **Factory**: `Type.of(x)` or `fun Type(x: ...)` constructor-style invocation — `Path.of("a", "b")`, `Result.success(x)`.

### Interface naming

- Capability: noun or `-able` — `Closeable`, `Iterable`, `Comparable`.
- Avoid `IFoo` / `FooInterface` Java-isms — anti-patterns §17.

### Property naming

- Read as English assertion for `Boolean`: `view.isVisible`, `string.isBlank()`.
- Avoid double negatives: `isNotEmpty` exists for symmetry but if you can use the positive form, do.

---

## Scope Function Decision Matrix

Kotlin's five scope functions are easy to misuse. Pick one with intent:

| Function | Lambda receiver | Returns | Use when |
|---------|------------------|---------|----------|
| `let` | `it` | Lambda result | Run a block on a non-null value (`x?.let { ... }`); transform-and-rebind |
| `also` | `it` | Receiver | Side effect on an object inside a builder chain; debug logging without breaking the chain |
| `apply` | `this` | Receiver | Configure an object before returning it (`Person().apply { name = "A"; age = 1 }`) |
| `run` | `this` | Lambda result | Call multiple methods on an object and return something derived |
| `with` | `this` | Lambda result | Same as `run` but argument-style: `with(builder) { ... }` |

### Refactor signals

- `let { it.foo() }` — could be plain `?.foo()`. Drop `let`.
- `also { it.foo() }` returning a value you discard — that's `apply` semantics.
- `apply { return foo }` — `apply` returns the receiver; you wanted `run`.
- Two scope functions stacked on the same object — almost always one is redundant.

```kotlin
// Bad — double scope function
user?.let { it.also { logger.info("got user $it") } }

// Good — one scope function, clear intent
user?.also { logger.info("got user $it") }
```

See anti-patterns §11 for the full catalog of scope-function pitfalls.

---

## Magic Numbers and Strings

Surface signals:

- `30.seconds` / `30_000L` scattered across files → extract `private const val REQUEST_TIMEOUT_MS = 30_000L` or `private val requestTimeout = 30.seconds`.
- `if (attempts < 3) ...` → `private const val MAX_ATTEMPTS = 3`.
- Repeated `"X-Request-Id"` HTTP header literals → `object Headers { const val REQUEST_ID = "X-Request-Id" }`.

Rules:

- Prefer `const val` for compile-time primitives (`Int`, `String`, `Boolean`). It inlines at every callsite.
- For non-primitive constants, `val` at top level or `companion object`.
- Group related constants in an `object`:

```kotlin
object HttpClientDefaults {
    const val MAX_RETRIES = 3
    val requestTimeout: Duration = 30.seconds
}
```

- For `Duration`, use the extension properties (`30.seconds`, `5.minutes`) — clearer than raw `Long` ms.
- For paths/URLs/regex patterns, prefer typed wrappers, not raw `String`.

Anti-signal: a constant used in exactly one place may belong as a `val` next to the use site.

---

## Coroutine / Flow Refactors

### Suspended block emitting events → Flow

```kotlin
// Before — manual callback collection
suspend fun observeTicks(out: (Int) -> Unit) {
    for (i in 0..Int.MAX_VALUE) {
        delay(1.seconds)
        out(i)
    }
}

// After
fun ticks(): Flow<Int> = flow {
    for (i in 0..Int.MAX_VALUE) {
        delay(1.seconds)
        emit(i)
    }
}
```

### `runBlocking` in production → structured scope

```kotlin
// Before — blocks the calling thread
fun handleRequest(req: Request) {
    val data = runBlocking { repo.fetch(req.id) }
    respond(data)
}

// After — suspending all the way down
suspend fun handleRequest(req: Request) {
    val data = repo.fetch(req.id)
    respond(data)
}
```

### `GlobalScope.launch` → structured scope

```kotlin
// Before — leaks; no parent supervises
GlobalScope.launch { sync() }

// After — bound to a real lifecycle
class Sync(private val scope: CoroutineScope) {
    fun start() = scope.launch { sync() }
}
```

See anti-patterns §2 (Coroutines) for the full catalog.

---

## Refactor Anti-Patterns to Avoid

Things that look like refactors but degrade the design:

| Anti-pattern | Why it hurts | Better path |
|--------------|--------------|-------------|
| Reflexive `List → Sequence` conversion for "perf" | For lists < ~1000 elements, `List.map` beats `Sequence` due to iterator overhead | Benchmark first; reach for `Sequence` only on large data or infinite/streaming sources |
| Reflexive `inline fun` everywhere | JVM bytecode bloat per callsite; longer compile times | `inline` is for higher-order functions where you want to inline the lambda — not for one-liner pure functions |
| Making everything `open` "for testability" | Kotlin is final-by-default for a reason — open-by-default invites subclass-coupling bugs (Effective Java item 19) | Inject interfaces; subclass only on types designed for it |
| Reflexive `data class` for every type | `data class` is for value-equality bags; misusing it on entities makes `equals`/`hashCode` mutable-bound | Use `data class` for DTOs/value objects; regular `class` for entities with identity |
| Catch-all `runCatching { ... }` swallowing `CancellationException` | Cancellation is *exceptional* — swallowing it breaks structured concurrency | `runCatching` since Kotlin 1.6 re-throws `CancellationException`; older code may not |
| Bulk migrating `kapt` → KSP without testing | Some kapt processors have not been ported; build breaks silently | Migrate one processor at a time; verify generated code matches |
| Hilt + Koin in the same module | Two DI containers mean two ownership models; every binding is a coin flip | Pick one per module; usually Hilt on Android, Koin on KMP |
| Replacing `class` with `object` for "stateless utility" | Singletons are hard to test; `object` is a global | Top-level functions, or DI-supplied dependency |
| Removing `@JvmStatic` because "Kotlin doesn't need it" | Breaks Java consumers calling `Foo.method()` instead of `Foo.Companion.method()` | Keep `@JvmStatic` until you confirm no Java caller; treat as public-API change |
| Bulk converting `Pair`/`Triple` to `data class` everywhere | Some Pairs are legitimately positional (Kotlin stdlib `Map.Entry.toPair()`) | Convert only where names add meaning; leave map-iteration Pairs alone |

---

## Refactor Checklist

Run before declaring a Kotlin refactor done:

1. **Build clean**: `./gradlew assemble` — no warnings under `-Werror`.
2. **Lints pass**: `./gradlew detekt ktlintCheck`.
3. **Tests stay green**: `./gradlew test` (JUnit/Kotest).
4. **K2 compiler builds**: ensure `kotlin.languageVersion=2.0` (or newer) in `gradle.properties` and the build doesn't regress.
5. **No new `!!` not-null assertions** outside test/main code.
6. **No new `catch (e: Exception)` / `catch (e: Throwable)`** without a comment explaining why; re-throw `CancellationException` if you do.
7. **No new `runBlocking`** outside `main()` or tests.
8. **No new `GlobalScope`** — must be `viewModelScope`, `lifecycleScope`, or a constructor-injected `CoroutineScope`.
9. **Public API surface unchanged** (or intentionally changed): `./gradlew apiCheck` if using `binary-compatibility-validator`.
10. **KMP `expect`/`actual` still align** if you touched `commonMain` — `./gradlew kotlinNativeBinaries iosX64Test` (or your KMP target set).

If any of these change unexpectedly, the refactor altered behavior — back out and reframe.

---

## Where to dig deeper

- Bad-pattern catalog: [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md)
  - §1 Null safety, §2 Coroutines, §3 Type/Generics, §11 Scope functions, §17 API Design
- Target idioms: [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md)
  - §1 Style Guide, §2 Effective Kotlin picks, §3 Coroutines, §8 Performance
- Language surface: [`builder/reference/kotlin-language-spec.md`](../../builder/reference/kotlin-language-spec.md)
  - §1 K2 timeline, §2 Type system, §4 Coroutines, §10 Context parameters, §13 K2 specifics
