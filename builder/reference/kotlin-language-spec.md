# Kotlin Language Spec — Deep Dive Reference

> Companion to the broader Kotlin knowledge in this `builder/reference/` directory. This file covers the language specification, K2 compiler semantics, type system, coroutines language surface, multiplatform mechanics, property/operator/annotation/reflection systems, and the stable/preview feature timeline in depth. The [`native` skill](../../native/SKILL.md) complements this for Jetpack Compose / Material 3 Expressive / Android-platform-specific concerns.
>
> Baseline: Kotlin 2.3.20 (2026-03 stable) with 2.4-RC2 on EAP; K2 compiler is the only frontend.

---

## Table of Contents

1. [Version Timeline & K2 Compiler Shift](#1-version-timeline--k2-compiler-shift)
2. [Type System Fundamentals](#2-type-system-fundamentals)
3. [Class Hierarchy Semantics](#3-class-hierarchy-semantics)
4. [Coroutines — Suspend, Dispatchers, Structured Concurrency](#4-coroutines--suspend-dispatchers-structured-concurrency)
5. [Multiplatform (KMP) Basics](#5-multiplatform-kmp-basics)
6. [Inline Functions & Reified Generics](#6-inline-functions--reified-generics)
7. [Property System](#7-property-system)
8. [Operator Overloading](#8-operator-overloading)
9. [Coroutines Safety Model](#9-coroutines-safety-model)
10. [Context Receivers → Context Parameters](#10-context-receivers--context-parameters)
11. [Annotations & Reflection](#11-annotations--reflection)
12. [Compiler Plugins](#12-compiler-plugins)
13. [K2 Compiler Specifics](#13-k2-compiler-specifics)
14. [Java Interop Subtleties](#14-java-interop-subtleties)
15. [Recently Stabilized (2.0 → 2.3) — Per-Release Feature Table](#15-recently-stabilized-20--23--per-release-feature-table)
16. [Unstable / Experimental Watch-list](#16-unstable--experimental-watch-list)
17. [Sources](#17-sources)

> **Cross-links:**
> - Production library choices, Gradle setup, KMP testing, Ktor/Exposed, dispatcher decisions, 2023→2026 migration cheatsheet → [`kotlin-best-practices.md`](./kotlin-best-practices.md)
> - Concrete misuse of each spec feature (null safety, coroutines, smart casts, value class boxing, KSP/KAPT pitfalls, K2 migration breakage) → [`kotlin-anti-patterns.md`](./kotlin-anti-patterns.md)
> - For Compose UI authoring, Material 3 Expressive, Android platform APIs, predictive back, Live Activities → [`native` skill](../../native/SKILL.md). This document only covers the Compose Compiler **plugin** angle.

---

## 1. Version Timeline & K2 Compiler Shift

| Release | Date | Key items |
|---|---|---|
| 1.9.0 | 2023-07 | Last K1-default release. `data object` stable. K2 still opt-in via `-language-version 2.0`. |
| 1.9.20 | 2023-11 | K2 Beta, hierarchical project structure on by default. |
| **2.0.0** | 2024-05-21 | **K2 compiler Stable** for JVM/Native/Wasm/JS. New JVM IR backend default. `enumEntries<T>()` stable. `AutoCloseable` stable. `invokedynamic` default for lambda generation. Smart cast improvements (local var refinement, OR-type tests, properties with function types, inline lambda capture). |
| 2.0.20 | 2024-08 | Phase 1 of data-class `copy` visibility realignment (warns when `copy` is more permissive than primary constructor; `@ConsistentCopyVisibility` / `@ExposedCopyVisibility`). KMP source-set hierarchy fixes. |
| 2.1.0 | 2024-11 | Preview: guard conditions in `when`, multi-dollar interpolation, non-local `break`/`continue`. Stable: `@SubclassOptInRequired`, improved overload resolution, exhaustive `when` over sealed types without redundant `else`. |
| 2.1.20 | 2025-03 | KMP Kotlin→Java direct actualization, KSP2 (Symbol Processing) further matured. |
| **2.2.0** | 2025-06-23 | **Stable**: guard conditions, non-local `break`/`continue`, multi-dollar interpolation. **Preview**: context parameters (`context(name: Type)` replacing context receivers), context-sensitive resolution, `@all:` use-site target meta-target, nested type aliases. Unified warning management (`-Xwarning-level=...`). `-jvm-default` (replaces `-Xjvm-default`). `JvmExposeBoxed` for value classes. Base64 + HexFormat stable. KSP1 deprecated. |
| **2.3.0** | 2025-12 | **Stable**: nested type aliases, data-flow-based exhaustiveness checks, `return` in expression bodies with explicit return type. **Experimental**: explicit backing fields (`field = ...`), unused-return-value checker (`-Xreturn-value-checker`). JDK 25 bytecode target. |
| 2.3.20 | 2026-03 | Name-based destructuring (preview). Current production-stable baseline. |
| 2.4-RC2 | 2026 EAP | Explicit backing fields promoted toward Stable. Data-flow exhaustiveness consolidation. **Preview only — do not adopt for production.** |

**K2 frontend**: a unified semantic data structure (FIR — Frontend IR) replacing K1's PSI-driven, multi-pass model. JetBrains reports ~2× clean-build speed-up on representative JVM projects and up to **94%** improvement on some build profiles, alongside better multiplatform architecture (single frontend across JVM/Native/JS/Wasm) and higher IDE analysis throughput.

Since Kotlin 2.0, **K2 is the only frontend** — there is no K1 fallback shipped with the compiler. Plugin authors who relied on the K1 `ExtensionPoint` model had to migrate to `FirExtension` (see §13.3).

---

## 2. Type System Fundamentals

### 2.1 Nullability

Kotlin's type system distinguishes nullable from non-nullable types at the type level:

```kotlin
val a: String  = "abc"  // non-nullable; cannot be assigned null
var b: String? = "abc"  // nullable
b = null                // OK
```

Operators:

| Operator | Meaning |
|---|---|
| `?.` | Safe call — returns `null` if receiver is `null`. |
| `?:` | Elvis — left-hand value if non-null, else right-hand. Right-hand may be `throw` or `return`. |
| `!!` | Asserts non-null; throws `NullPointerException` if `null`. |
| `as?` | Safe cast — returns `null` on cast failure rather than throwing. |

Sources of `NullPointerException` in pure Kotlin: explicit `throw NullPointerException()`, `!!`, `lateinit` accessed too early (`UninitializedPropertyAccessException` is the actual subtype), uninitialized superclass leaking `this`, and Java interop.

### 2.2 Platform types (`T!`)

A Java type with no nullability annotation surfaces in Kotlin as a *platform type*. Notation `T!` is non-denotable (you cannot write it in source) and means "either `T` or `T?`". The compiler suppresses null-checks at platform-type boundaries but does not insert intrinsic checks until you assign to a strictly typed Kotlin variable.

Mapping examples:

| Java | Kotlin |
|---|---|
| `String` | `String!` |
| `List<String>` | `(Mutable)List<String!>!` |
| `Foo<? extends Bar>` | `Foo<out Bar!>!` |
| `Foo<? super Bar>` | `Foo<in Bar!>!` |
| Raw `List` | `List<*>!` |

Recognized annotations include JetBrains (`org.jetbrains.annotations`), JSpecify (`@NullMarked` for default-non-null modules), JSR-305, Android `androidx.annotation`, FindBugs, Eclipse, Lombok. Configure via `-Xnullability-annotations=@<pkg>:<level>` (`level` ∈ `ignore` / `warn` / `strict`).

Reference: [kotlinlang.org/docs/java-interop.html](https://kotlinlang.org/docs/java-interop.html).

### 2.3 Smart casts

The compiler narrows a value's type after a check, *when it can prove the value cannot change between the check and the use*.

Smart-cast scenarios (2.0+ added support marked **`* new in 2.0`**):

```kotlin
// (a) is-check followed by use
fun length(x: Any): Int? {
    if (x is String) return x.length // smart-cast to String
    return null
}

// (b) Null check
fun greet(name: String?) {
    if (name != null) println(name.uppercase()) // smart-cast to String
}

// (c) * new in 2.0: local Boolean carrying the is-result
fun petAnimal(animal: Any) {
    val isCat = animal is Cat
    if (isCat) animal.purr()       // smart-cast through Boolean local
}

// (d) * new in 2.0: type tests with logical OR widening to common supertype
interface Status { fun signal() }
interface Ok : Status
interface Postponed : Status
fun check(s: Any) {
    if (s is Postponed || s is Ok) s.signal() // common supertype Status
}

// (e) * new in 2.0: smart cast survives capture in inlined lambda
inline fun runOnce(body: () -> Unit) { body() }
class Holder(val provider: (() -> Unit)?) {
    fun process() {
        if (provider != null) provider() // no safe-call needed in 2.0
    }
}
```

Smart cast preconditions:
- `val` property, `val` local, or `var` local *not modified between check and use and not captured by a mutating lambda*.
- For properties: `open` / custom-getter / delegated properties are not smart-castable because the getter could observe state changes.
- Compiler proves all branching paths refine the type identically.

For the common refusal cases (smart cast on `var` property, `open val`, cross-module property, custom getter), see [`kotlin-anti-patterns.md` §10](./kotlin-anti-patterns.md#10-smart-cast-pitfalls).

### 2.4 Contracts (`kotlin.contracts.contract { }`)

Contracts let library authors *teach* the compiler about runtime behavior to unlock smart-casts and definite-assignment analyses normally invisible to it. Marked `@ExperimentalContracts`.

```kotlin
import kotlin.contracts.*

@OptIn(ExperimentalContracts::class)
fun String?.requireNonEmpty(): String {
    contract { returns() implies (this@requireNonEmpty != null) }
    require(!this.isNullOrEmpty())
    return this!!
}

@OptIn(ExperimentalContracts::class)
inline fun <R> withLock(lock: Any, block: () -> R): R {
    contract { callsInPlace(block, InvocationKind.EXACTLY_ONCE) }
    synchronized(lock) { return block() }
}
```

Effects:
- `returns().implies(boolean)` / `returns(value).implies(...)` — postconditions on return value.
- `returnsNotNull().implies(...)` — when result is non-null.
- `callsInPlace(lambda, kind)` with `InvocationKind ∈ { EXACTLY_ONCE, AT_LEAST_ONCE, AT_MOST_ONCE, UNKNOWN }`.

Constraints (today):
- Must be the *first* statement of the function body.
- Only top-level / member functions; not extensions on generics with complex bounds.
- Right-hand of `implies` is restricted to `true`, `false`, `null`, an `is` check, or a `!= null` check.

Inline functions are *implicitly* `callsInPlace(UNKNOWN)` unless they have an explicit contract; 2.0 added an implicit assumption that lets smart-casts flow into captured lambdas as shown above.

Reference: [`kotlin.contracts.contract`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.contracts/contract.html).

### 2.5 Generics & variance

**Declaration-site variance** (applied where the type parameter is declared):

```kotlin
interface Source<out T> {        // producer: T appears only in out-positions
    fun next(): T
}

interface Sink<in T> {           // consumer: T appears only in in-positions
    fun put(value: T)
}

val anySource: Source<Any>    = (object : Source<String> { override fun next() = "" })
val stringSink: Sink<String>  = (object : Sink<Any>     { override fun put(value: Any) {} })
```

**Use-site projection** (applied at the use site, for invariant types):

```kotlin
fun copy(from: Array<out Any>, to: Array<Any>) { /* read only */ }
fun fill(dest: Array<in String>, value: String) { /* write String */ }
```

**Star projection (`Foo<*>`)**: equivalent to `Foo<out TUpper>` for read access and `Foo<in Nothing>` for write access.

**Multiple bounds** via `where`:

```kotlin
fun <T> sumSorted(items: List<T>): List<T>
    where T : Comparable<T>, T : Cloneable { ... }
```

**Type erasure**: At runtime, `List<Int>` and `List<String>` share the same `Class`. `is List<Int>` is a compile error; `is List<*>` works. The single escape hatch is `reified` (see §6).

**Definitely-non-null types `T & Any`** (since 1.7): a way to *narrow* an upper-bounded type parameter to non-null:

```kotlin
interface Game<T> { fun load(x: T): T }          // T may be nullable
interface ArcadeGame<T> : Game<T> {
    override fun load(x: T & Any): T & Any        // refuses null at runtime even if T?
}
```

Useful when overriding a Java method whose parameter is `@NotNull` while keeping `T` generic.

### 2.6 Type aliases

```kotlin
typealias Predicate<T> = (T) -> Boolean
typealias NodeSet      = Set<Node>
```

- Top-level aliases existed since 1.1.
- **Nested type aliases** (preview in 2.2, **Stable in 2.3.0**): aliases inside classes/interfaces/objects. They may not capture outer-class type parameters.

```kotlin
class Dijkstra<NodeId> {
    typealias Visited = Set<NodeId>          // ERROR — captures outer T
    typealias VisitedRaw = Set<Any?>         // OK
    private fun step(visited: VisitedRaw, ...) = ...
}
```

### 2.7 Intersection / union

Kotlin has no first-class intersection or union types except for `T & Any`. When you use `&` elsewhere, it surfaces as a compiler-internal intersection in type inference (e.g., the result of merging multiple upper bounds), not as user-writable syntax. The "Rich Errors" KEEP (KEEP-0441) explores adding structured union-like error returns; **not yet stable**.

---

## 3. Class Hierarchy Semantics

### 3.1 `open` / `final` (closed by default)

All classes and members are `final` (closed for extension) by default. To allow subclassing or overriding, mark with `open`:

```kotlin
open class Shape { open fun area(): Double = 0.0 }
class Circle(val r: Double) : Shape() {
    override fun area() = Math.PI * r * r
}
```

`abstract`, `sealed`, and `enum class` are implicitly open w.r.t. their declared members where it makes sense.

### 3.2 `data class`

Auto-generates `equals` / `hashCode` / `toString` / `componentN()` / `copy()`.

Constraints:
- Must have at least one parameter in the primary constructor.
- Primary-constructor parameters must be `val` or `var`.
- Cannot be `open` / `abstract` / `sealed` / `inner`.

**Data-class copy visibility realignment (2.0.20 → 2.2/2.3)**: Historically `copy()` was always `public`, even when the primary constructor was `private` — leaking instantiation paths. The transition:

| Phase | Version | Behavior |
|---|---|---|
| 1 | 2.0.20 | Warning when copy visibility exceeds primary-ctor visibility. Suppress with `@ConsistentCopyVisibility` (recommended) or `@ExposedCopyVisibility` (keeps old behavior). Or `-Xconsistent-data-class-copy-visibility`. |
| 2 | 2.1/2.2 | Warning becomes error unless annotated. |
| 3 | 2.2/2.3 | `copy()` defaults to the primary-ctor visibility unless `@ExposedCopyVisibility`. |

Reference: [`@ConsistentCopyVisibility`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-consistent-copy-visibility/), [`@ExposedCopyVisibility`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-exposed-copy-visibility/).

### 3.3 `value class` (replaces `inline class`)

Identity-less, single-property wrapper. The `inline class` keyword (1.3–1.4) was replaced by `value` + `@JvmInline` in 1.5.

```kotlin
@JvmInline
value class Password(private val s: String) {
    init { require(s.length >= 8) }
    constructor(first: String, second: String) : this("$first$second")
}
```

Specification:
- Exactly one property in the primary constructor.
- `init` block and secondary constructors allowed.
- May implement interfaces but not extend a class; always `final`.
- Identity comparison (`===`) is forbidden.
- *Boxed* representation used when as generic, interface, nullable, or array element; *unboxed* when used as the value class itself.
- JVM method signatures are **mangled** (hash suffix) to prevent platform clashes; opt out per declaration with `@JvmName`.
- 2.2+: `@JvmExposeBoxed` generates a non-mangled, Java-friendly boxed variant. Module-wide via `-Xjvm-expose-boxed`.
- Properties: simple computable only; no `lateinit`, no delegated properties; backing fields not user-controllable.
- Delegation: `class Wrapper(val w: I) : I by w` is allowed.

**Boxing edge cases** (a frequent footgun — see [`kotlin-anti-patterns.md` §3.8](./kotlin-anti-patterns.md#3-type--generics-pitfalls)):

```kotlin
@JvmInline
value class UserId(val v: String)

fun lookup(id: UserId) {}                  // unboxed (call-site uses raw String)
fun all(): List<UserId> = listOf()         // BOXED (generic → List<Object>)
val opt: UserId? = null                    // BOXED (nullable needs object header)
interface IdConsumer { fun take(id: Any) } // BOXED (interface upcast)
```

Use cases: type-safe wrappers (`UserId`, `Email`, `Meters`) without runtime overhead in the hot path.

Reference: [Inline (Value) Classes](https://kotlinlang.org/docs/inline-classes.html), [`@JvmInline`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-inline/), [KEEP — Inline classes](https://github.com/Kotlin/KEEP/blob/master/proposals/inline-classes.md).

### 3.4 `sealed class` / `sealed interface`

Closed hierarchy known at compile time. Used to make `when` exhaustively checkable.

Rules:
- Direct subclasses must reside in the **same package and same module** as the sealed declaration. Indirect subclasses are unconstrained.
- A direct subclass must have a stable name (no anonymous / local).
- Sealed class constructors are `protected` or `private` only.
- `enum class` may *implement* but not *extend* a sealed type.
- `fun interface` cannot be `sealed`.

Sealed classes form a tree (single-superclass inheritance); sealed interfaces form a DAG because of multiple-interface inheritance — the exhaustiveness algorithm walks the DAG.

```kotlin
sealed interface Result<out T>
data class Ok<T>(val value: T) : Result<T>
data class Err(val cause: Throwable) : Result<Nothing>

fun <T> handle(r: Result<T>) = when (r) {  // no `else` needed
    is Ok  -> r.value
    is Err -> throw r.cause
}
```

KMP caveat: in common code with `expect`/`actual`, an `else` branch is still required when the sealed hierarchy is `expect`.

**Sealed evolution across module boundaries** is binary-breaking — adding a variant in version N+1 forces every downstream exhaustive `when` to fail to compile. See [`kotlin-anti-patterns.md` §4.6 and §17.3](./kotlin-anti-patterns.md#4-class-hierarchy-pitfalls) for the policy options (freeze hierarchy, document `else -> handleUnknown` policy, or fall back to `abstract class`).

Reference: [Sealed classes and interfaces](https://kotlinlang.org/docs/sealed-classes.html), [`sealed-interface-freedom.md` KEEP](https://github.com/Kotlin/KEEP/blob/master/proposals/sealed-interface-freedom.md).

### 3.5 `object` declarations and `companion object`

- `object Foo { ... }`: thread-safe lazy singleton.
- `companion object` inside a class: per-class singleton; members can be accessed as `ClassName.member`.
- `data object` (stable since 1.9): generates `toString` / `equals` / `hashCode` matching name-based identity, suitable for "marker" cases in sealed hierarchies:

```kotlin
sealed interface UiState
data object Loading : UiState
data class Loaded(val items: List<Item>) : UiState
data object Empty : UiState
```

### 3.6 `enum class`

Enum entries are first-class objects; can carry state and override methods per entry.

```kotlin
enum class Op(val symbol: String) {
    PLUS("+")  { override fun apply(a: Int, b: Int) = a + b },
    MINUS("-") { override fun apply(a: Int, b: Int) = a - b };
    abstract fun apply(a: Int, b: Int): Int
}
```

`Enum.entries` (Stable in 2.0, KEEP `enum-entries.md`) replaces `Enum.values()`. `entries` returns a cached `EnumEntries<T>` (a `List<T>`) — same instance on every call; `values()` allocated a fresh array.

```kotlin
for (op in Op.entries) println(op.symbol)

inline fun <reified T : Enum<T>> printAll() = enumEntries<T>().forEach(::println)
```

### 3.7 Interfaces, abstract, delegation

- An `interface` may declare abstract members and methods with default bodies; it cannot hold state (no backing field).
- `abstract class` may hold state.
- Multiple interface inheritance: disambiguate with `super<I>` qualifier:

```kotlin
interface A { fun f() = println("A") }
interface B { fun f() = println("B") }
class C : A, B {
    override fun f() {
        super<A>.f(); super<B>.f()
    }
}
```

- Class delegation (`by`):

```kotlin
interface Repo { fun load(id: Int): Item }
class CachingRepo(real: Repo, private val cache: MutableMap<Int, Item>) : Repo by real {
    override fun load(id: Int) = cache.getOrPut(id) { /* fall through */ TODO() }
}
```

The compiler emits forwarding methods to the delegate for every member of `Repo` not overridden in `CachingRepo`.

---

## 4. Coroutines — Suspend, Dispatchers, Structured Concurrency

The single largest topic for 2026 Kotlin code is `kotlinx.coroutines` (library, not language — but the `suspend` keyword and the `kotlin.coroutines` package are in the language).

### 4.1 `suspend` functions

A `suspend fun` is a function whose continuation can be captured by the compiler so it can be paused and resumed without blocking a thread. They may only be called from:
- another `suspend` function;
- a coroutine builder (`launch`, `async`, `runBlocking`, `runTest`, `flow { }`, etc.).

Under the hood, the compiler adds a hidden `Continuation<T>` parameter (CPS transform).

```kotlin
suspend fun fetch(): Result {
    val a = api.callA()      // suspends, does not block
    val b = api.callB()
    return Result(a, b)
}
```

### 4.2 `CoroutineScope` and `CoroutineContext`

`CoroutineContext` is an indexed set of `Element`s; standard elements:
- `Job` (or its `Deferred<T>` subtype for `async`) — lifecycle + cancellation.
- `ContinuationInterceptor` / `CoroutineDispatcher` — which thread executes the resumption.
- `CoroutineExceptionHandler` — root-only catcher for uncaught exceptions.
- `CoroutineName` — debug name.

`CoroutineScope` carries one `CoroutineContext`. New coroutines launched in a scope inherit that context, **overlaying** with any context elements passed at the builder site.

```kotlin
val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO + CoroutineName("worker"))
scope.launch(CoroutineName("subtask") + Dispatchers.Default) {
    // context: SupervisorJob() + Dispatchers.Default + CoroutineName("subtask")
}
```

### 4.3 Structured concurrency

Builders launched on a scope are *children* of that scope's `Job`. Properties:
1. Parent waits for all children before completing.
2. If parent is cancelled, all children are cancelled recursively (`CancellationException`).
3. In a regular `Job`, an exception in any child cancels siblings and the parent. In a `SupervisorJob`, child failures do not bubble (siblings continue).

`coroutineScope { }` vs `supervisorScope { }`:

```kotlin
suspend fun loadAll() = coroutineScope {
    val a = async { loadA() }
    val b = async { loadB() }   // if loadB throws, a is cancelled
    a.await() to b.await()
}

suspend fun loadAllIndependent() = supervisorScope {
    val a = async { loadA() }
    val b = async { loadB() }   // failure in b does not cancel a
    runCatching { a.await() } to runCatching { b.await() }
}
```

### 4.4 Builders

| Builder | Returns | Use |
|---|---|---|
| `launch { }` | `Job` | Fire-and-forget. Uncaught exception → propagates to parent. |
| `async { }` | `Deferred<T>` | Concurrent computation. Exception thrown by `await()`. |
| `runBlocking { }` | `T` | Bridge from blocking to suspending (CLI `main`, tests). **Do not** use inside Android UI / server framework callbacks. |
| `withContext(ctx) { }` | `T` | Switch context for the duration of `block`. Suspends until block completes. |
| `coroutineScope { }` / `supervisorScope { }` | `T` | Create a child scope; suspend until children complete. |

### 4.5 Dispatchers

- `Dispatchers.Default` — shared pool sized to `max(2, CPUs)`; CPU-bound work.
- `Dispatchers.IO` — elastic pool (default cap = 64); blocking I/O.
- `Dispatchers.Main` — platform UI thread (Android/JavaFX/Swing); availability via `Main` artifact.
- `Dispatchers.Unconfined` — runs the resumption on the resuming thread; testing / specialized only.

Custom dispatcher from a JVM `Executor`:

```kotlin
val pool = Executors.newFixedThreadPool(4).asCoroutineDispatcher()

// JVM 21+ virtual threads — interop via Project Loom:
val loomDispatcher = Executors.newVirtualThreadPerTaskExecutor().asCoroutineDispatcher()
```

`Dispatchers.Default` and `Dispatchers.IO` share a worker pool but enforce their respective parallelism limits; `withContext(Dispatchers.IO)` does not necessarily switch threads, only re-tags the limiter. (`limitedParallelism(n)` produces a child dispatcher with bounded parallelism.)

### 4.6 Cooperative cancellation

Cancellation is **cooperative**: a coroutine is cancelled only at *suspension points* (or when it explicitly checks). After cancellation, suspending calls throw `CancellationException`.

```kotlin
launch {
    repeat(1_000_000) { i ->
        if (!isActive) return@launch   // cooperative check
        ensureActive()                  // throws CE if cancelled
        yield()                         // suspension point + cancellation check
        compute(i)
    }
}
```

Special: `CancellationException` is **transparent** to structured concurrency — it cancels the current coroutine but does *not* cancel the parent (unlike other exceptions). It is also ignored by `CoroutineExceptionHandler`.

`withContext(NonCancellable) { }` — protect a cleanup block from cancellation while still allowing it to suspend:

```kotlin
try { work() }
finally {
    withContext(NonCancellable) {
        release()  // can call suspending close even after parent cancelled
    }
}
```

### 4.7 Timeouts

```kotlin
withTimeout(1.seconds) { fetch() }        // throws TimeoutCancellationException on timeout
withTimeoutOrNull(1.seconds) { fetch() }  // returns null on timeout
```

`TimeoutCancellationException` is a `CancellationException` subtype — caught structurally; `withTimeoutOrNull` swallows it for you.

### 4.8 Exception propagation rules (concise restatement)

| Construct | First failure behavior |
|---|---|
| `launch` inside `coroutineScope` | Cancels scope; propagates to caller of `coroutineScope`. |
| `launch` inside `supervisorScope` | Only cancels that child. Goes to `CoroutineExceptionHandler` from that child's context. |
| `async` inside any scope | Captured in `Deferred`; surfaces at `.await()`. In a regular `coroutineScope`, the original exception *also* cancels the scope at the moment the `async` body throws. |
| Multiple sibling failures | First exception wins; later ones attached as `suppressed`. |

Reference: [Coroutine exceptions handling](https://kotlinlang.org/docs/exception-handling.html).

### 4.9 `Flow`

`Flow<T>` is a cold asynchronous stream — code in the builder runs once per collection:

```kotlin
fun primes(): Flow<Int> = flow {
    var n = 2
    while (true) {
        if (isPrime(n)) emit(n)
        n++
    }
}
```

Intermediate operators (returning a new `Flow`, not suspending): `map`, `filter`, `transform`, `take`, `onEach`, `onStart`, `onCompletion`, `catch`, `retry`, `flatMapConcat`, `flatMapMerge`, `flatMapLatest`, `combine`, `zip`, `buffer`, `conflate`, `flowOn`, `cancellable`, `debounce`, `sample`, `distinctUntilChanged`.

Terminal operators (suspending, start collection): `collect`, `collectLatest`, `toList`, `toSet`, `first`, `single`, `reduce`, `fold`, `count`, `launchIn`.

**Context preservation**: emission and collection share the collector's coroutine context. `withContext` *inside* a `flow { }` block is illegal. Use `flowOn(ctx)` to set the upstream context:

```kotlin
flow {
    for (i in 1..3) { Thread.sleep(100); emit(i) }      // runs on Default
}
.flowOn(Dispatchers.Default)
.collect { println(it) }                                // collector context
```

`collectLatest` cancels the previous emission's downstream block when a new value arrives:

```kotlin
flow.collectLatest { value -> render(value); delay(300) } // restarts render on next value
```

**Exception transparency**: emitters must not wrap `emit` in `try/catch`. Use the `catch` operator for upstream errors; downstream errors should be handled around `collect`:

```kotlin
flow { emit(1); error("boom") }
    .catch { e -> emit(-1) }
    .collect { println(it) }
```

**Cancellation**: `flow { }` builder calls `ensureActive()` on each emit; cold flows from iterables (`(1..n).asFlow()`) do *not*, so use `.cancellable()` for them.

### 4.10 Hot flows: `StateFlow` and `SharedFlow`

- `StateFlow<T>` — single-value, conflated, replay = 1, always has a current value (`.value`). Best for UI state.
- `SharedFlow<T>` — multi-subscriber broadcast with configurable `replay`, `extraBufferCapacity`, `onBufferOverflow ∈ { SUSPEND, DROP_LATEST, DROP_OLDEST }`.

```kotlin
class CounterVm {
    private val _state = MutableStateFlow(0)
    val state: StateFlow<Int> = _state.asStateFlow()

    fun increment() = _state.update { it + 1 }   // atomic CAS-style update
}
```

`MutableStateFlow.update { current -> new }` is the canonical atomic mutator (since `kotlinx.coroutines 1.6`). `compareAndSet` is also available.

`SharedFlow` for one-shot events ("show snackbar"):

```kotlin
val events = MutableSharedFlow<UiEvent>(extraBufferCapacity = 16)
```

### 4.11 `channelFlow` and `callbackFlow`

`channelFlow { ... send(...) ... }` — builder for flows whose producers run concurrently or originate in a separate scope; uses a backing channel.
`callbackFlow { ... awaitClose { unregister() } }` — bridge a callback-based API into Flow. Must call `awaitClose` (and *should* register cleanup there) to honor structured cancellation.

```kotlin
fun locationFlow(client: LocationClient): Flow<Location> = callbackFlow {
    val listener = LocationListener { loc -> trySend(loc) }
    client.register(listener)
    awaitClose { client.unregister(listener) }
}
```

### 4.12 `kotlinx.coroutines.test`

```kotlin
@Test fun example() = runTest {       // returns TestScope with virtual time
    val job = launch { delay(10_000); println("done") }
    advanceTimeBy(5_000); runCurrent()  // halfway
    advanceUntilIdle()                  // run until all coroutines idle
    job.join()
}
```

- `runTest { }` — replaces deprecated `runBlockingTest`. Uses `StandardTestDispatcher` with a `TestCoroutineScheduler` controlling virtual time.
- `TestScope` — receiver type; exposes `currentTime`, `runCurrent()`, `advanceTimeBy(ms)`, `advanceUntilIdle()`.
- `UnconfinedTestDispatcher` — eager dispatch; useful for tight unit tests where you don't care about order.
- `Dispatchers.setMain(testDispatcher)` / `Dispatchers.resetMain()` swap `Main` for tests.

Reference: [`kotlinx-coroutines-test`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/).

### 4.13 Virtual threads (Project Loom) interop (JVM 21+)

Pattern:

```kotlin
val loom = Executors.newVirtualThreadPerTaskExecutor().asCoroutineDispatcher()
withContext(loom) {
    // Blocking I/O here yields the virtual thread to the JVM — orders of magnitude
    // higher concurrency than Dispatchers.IO for blocking calls.
}
```

Caveats:
- Virtual threads do *not* eliminate the need for `suspend` — they help only when you call blocking APIs you cannot make suspending.
- Pinning (synchronized monitors, native frames) still pins the carrier thread.
- `Dispatchers.IO` already does an analogous thing (large pool sized for blocking workloads) but caps at 64 threads — Loom dispatchers are effectively unbounded.

Reference: [Running Kotlin coroutines on Loom's virtual threads](https://kt.academy/article/dispatcher-loom).

---

## 5. Multiplatform (KMP) Basics

KMP is the language-level project layout; Compose Multiplatform is a separate library. K2 fully supports KMP as a first-class platform.

### 5.1 Source-set layout

Canonical hierarchy (since 1.9.20 default):

```
src/
  commonMain/        // shared across all targets
  commonTest/
  jvmMain/  jvmTest/
  androidMain/  androidUnitTest/  androidInstrumentedTest/
  iosMain/  iosTest/
    iosX64Main/  iosArm64Main/  iosSimulatorArm64Main/
  linuxX64Main/
  wasmJsMain/  wasmWasiMain/
  jsMain/
```

Intermediate sets like `nativeMain`, `appleMain`, `iosMain` come from the default hierarchy template:

```kotlin
kotlin {
    applyDefaultHierarchyTemplate()   // earlier: useDefault()
    jvm(); androidTarget(); iosX64(); iosArm64(); iosSimulatorArm64()
}
```

### 5.2 `expect` / `actual`

```kotlin
// commonMain
expect fun deviceId(): String
expect class Logger() {
    fun log(level: Level, message: String)
}
expect val platformName: String

// androidMain
actual fun deviceId(): String = android.provider.Settings.Secure.getString(...)
actual class Logger { actual fun log(level: Level, message: String) { ... } }
actual val platformName: String = "Android"
```

Rules:
- Every `expect` declaration must have a matching `actual` in every leaf platform source set, in the same package, with matching signature.
- An `actual` may be **more visible** than the `expect` (e.g., `internal expect` actualized as `public actual`).
- `actual typealias` is allowed when the platform already has a type that fits — common for adapting `java.time.LocalDate`, etc.

```kotlin
// commonMain
expect class UUID
// jvmMain
actual typealias UUID = java.util.UUID
```

- `expect enum class`: actuals may add **additional** enum entries; consumers in common must still cover with `else`.
- `expect annotation class`: may be `@OptionalExpectation` so it need not be actualized on every target.

### 5.3 Relaxed `expect class` (2.1+)

Since 2.1, `expect class` is no longer required to be *purely* abstract; default implementations are permitted in the expect declaration. Status remains **Beta**; suppress the warning with `-Xexpect-actual-classes`. Actuals may extend platform classes:

```kotlin
// commonMain
expect class CommonError() : Throwable {
    val tag: String
}
// jvmMain
actual class CommonError actual constructor() : IOException() {
    actual val tag: String = "JVM"
}
```

Reference: [Expected and actual declarations](https://kotlinlang.org/docs/multiplatform/multiplatform-expect-actual.html), [Hierarchical project structure](https://kotlinlang.org/docs/multiplatform-hierarchy.html).

### 5.4 Kotlin→Java direct actualization (2.1+)

Preview: a Kotlin `expect` declaration can be actualized by a *Java* class on the JVM target without an intermediate `actual typealias`. KEEP: `kmp-kotlin-to-java-direct-actualization.md` (KT-67202).

### 5.5 Kotlin/Native interop snippets

```kotlin
import kotlinx.cinterop.*

@CName("kotlin_entry_point")          // export symbol name for C callers
fun entryPoint(): Int = 0

memScoped {                            // allocate native memory tied to lexical scope
    val buf = allocArray<ByteVar>(1024)
    nativeApi.fill(buf, 1024)
}
```

`@CName(...)` overrides the generated C symbol; required for stable ABI when producing shared libraries. `kotlinx.cinterop` exposes `CPointer`, `CValuesRef`, `memScoped { }`, `staticCFunction { }`.

### 5.6 Compose Multiplatform touch-points

Not a language feature, but bears mention because the Compose compiler plugin recognizes `@Composable` annotations. From Compose Multiplatform 1.7+ the toolchain is officially aligned with Kotlin K2. **Compose UI authoring itself — composables, state hoisting, side-effects, Material 3 Expressive — belongs to the [`native` skill](../../native/SKILL.md), not here.**

---

## 6. Inline Functions & Reified Generics

### 6.1 `inline fun`

The compiler copies the function body into each call site, including the bodies of any lambda parameters not marked otherwise. Benefits:
- Eliminates the allocation of a `Function<N>` object per lambda.
- Permits **non-local return** from lambdas (`return` exits the enclosing function).
- Required prerequisite for `reified` type parameters.

Drawbacks: increases bytecode size; public inline functions cannot reference `private`/`internal` symbols unless those are `@PublishedApi`.

### 6.2 `noinline`

Per-parameter opt-out — keep this lambda boxed (so it can be stored or passed):

```kotlin
inline fun render(crossinline header: () -> String, noinline footer: () -> String): String {
    val cached: () -> String = footer  // OK because noinline keeps it as a function reference
    return header() + "\n" + cached()
}
```

### 6.3 `crossinline`

Per-parameter; permits inlining but forbids non-local return — required when the lambda is invoked from a nested scope (e.g., inside an anonymous `object`):

```kotlin
inline fun runOnExecutor(executor: Executor, crossinline body: () -> Unit) {
    executor.execute { body() }   // body is invoked from a Runnable; non-local return would escape
}
```

### 6.4 `reified T`

Only allowed on `inline fun`. The compiler substitutes the actual type argument at each call site, so `T::class`, `is T`, `as T`, and `T::class.java` all work:

```kotlin
inline fun <reified T : Any> Any?.castOrNull(): T? = this as? T

inline fun <reified T> List<*>.allOf(): List<T> = filterIsInstance<T>()

inline fun <reified T> moshiAdapter(moshi: Moshi): JsonAdapter<T> = moshi.adapter(T::class.java)
```

Reference: [Inline functions](https://kotlinlang.org/docs/inline-functions.html).

---

## 7. Property System

### 7.1 `val` vs `var`

`val` = read-only reference (the value itself may be mutable). `var` = mutable reference.

### 7.2 Custom accessors and `field`

```kotlin
class User {
    var name: String = ""
        get() = field.trim()
        set(value) {
            require(value.isNotBlank())
            field = value
        }
}
```

- `field` is the implicit backing field; available only inside accessors.
- The compiler emits a backing field only if `field` is referenced or default accessors are used.
- `const val` cannot have custom accessors; must be a compile-time `String`/primitive.
- `lateinit` cannot have custom accessors.

### 7.3 `lateinit var`

Defers initialization, preserving non-null typing.

Restrictions:
- `var` only; no custom accessors.
- Type must be non-null **reference** (`String`, `Repo`, ...). **Not** primitives (`Int`, `Boolean`, `Double`) — use `by Delegates.notNull()` for those.
- Can be checked with `::name.isInitialized`.

```kotlin
class Activity {
    lateinit var binding: Binding
    fun onCreate() { binding = inflate() }
    fun foo() { if (::binding.isInitialized) binding.render() }
}
```

Accessing an uninitialized `lateinit` throws `kotlin.UninitializedPropertyAccessException`.

### 7.4 `const val`

Compile-time constant; inlined at use sites and exposed to Java as a `public static final` field.

```kotlin
const val MAX_RETRIES = 5
const val GREETING = "hello"
```

Constraints: only `String` / `Boolean` / `Byte` / `Short` / `Int` / `Long` / `Float` / `Double` / `Char` literals (or `const`-folded expressions). No custom getters. Must be top-level or `object` member.

### 7.5 Delegated properties (`by`)

```kotlin
val expensive by lazy { compute() }                         // thread-safe by default
var observed by Delegates.observable("init") { _, o, n -> log("$o -> $n") }
var vetoed   by Delegates.vetoable(0) { _, _, new -> new >= 0 }
var injected by Delegates.notNull<Int>()
val nameFromMap by mapOf("name" to "Alice")                 // map-backed
```

Delegate contracts:

```kotlin
class ReadOnlyDelegate<R, T> {
    operator fun getValue(thisRef: R, property: KProperty<*>): T = TODO()
}

class ReadWriteDelegate<R, T> {
    operator fun getValue(thisRef: R, property: KProperty<*>): T = TODO()
    operator fun setValue(thisRef: R, property: KProperty<*>, value: T) {}
}
```

`PropertyDelegateProvider`: lets a factory choose a delegate based on the owner and property name:

```kotlin
class Eager<T>(private val value: T) {
    operator fun provideDelegate(thisRef: Any?, prop: KProperty<*>): ReadOnlyProperty<Any?, T> {
        check(prop.name.startsWith("e")) { "Eager properties must start with 'e'" }
        return ReadOnlyProperty { _, _ -> value }
    }
}

val ePort by Eager(8080)
```

`LazyThreadSafetyMode`:

| Mode | Semantics |
|---|---|
| `SYNCHRONIZED` (default) | Locks; one initialization across threads. |
| `PUBLICATION` | Multiple threads may run the initializer; first published value wins. |
| `NONE` | No locking, single-threaded use only. Fastest. |

For the cost-vs-safety tradeoffs in hot paths and the `lazy` overhead on every access, see [`kotlin-anti-patterns.md` §6.1-6.2 (`LazyThreadSafetyMode` decision matrix)](./kotlin-anti-patterns.md#6-property-delegation-pitfalls).

### 7.6 Explicit backing fields (preview in 2.3, target-stable 2.4)

```kotlin
val city: StateFlow<String>
    field: MutableStateFlow<String> = MutableStateFlow("")
```

Replaces the `private _city` + public `city` boilerplate. Opt-in: `-Xexplicit-backing-fields`. KEEP: `explicit-backing-fields.md` (KT-14663). **2.4-RC2 promotes this toward Stable — preview only in 2.3, do not adopt for production until 2.4 GA.**

---

## 8. Operator Overloading

Marked with `operator fun`. Mapping table (complete):

| Expression | Translation |
|---|---|
| `+a` | `a.unaryPlus()` |
| `-a` | `a.unaryMinus()` |
| `!a` | `a.not()` |
| `a++` (postfix) | `a.inc()` (stores old, returns old) |
| `a--` | `a.dec()` |
| `++a` | `a.inc()` (returns new) |
| `--a` | `a.dec()` (returns new) |
| `a + b` | `a.plus(b)` |
| `a - b` | `a.minus(b)` |
| `a * b` | `a.times(b)` |
| `a / b` | `a.div(b)` |
| `a % b` | `a.rem(b)` |
| `a..b` | `a.rangeTo(b)` |
| `a..<b` | `a.rangeUntil(b)` (since 1.7.20) |
| `a in b` | `b.contains(a)` |
| `a !in b` | `!b.contains(a)` |
| `a[i]` | `a.get(i)` |
| `a[i] = v` | `a.set(i, v)` |
| `a()` | `a.invoke()` |
| `a(x, y)` | `a.invoke(x, y)` |
| `a == b` | `a?.equals(b) ?: (b === null)` |
| `a != b` | `!(a?.equals(b) ?: (b === null))` |
| `a < b` / `>` / `<=` / `>=` | from `a.compareTo(b)` |
| `a += b` | `a.plusAssign(b)` if defined and returns `Unit`; **else** `a = a + b` |
| `a -= b` | `a.minusAssign(b)` …same fallback |
| `a *= b`, `/=`, `%=` | same pattern |

**Augmented-assignment ambiguity** rule: if both `plusAssign(b)` *and* `plus(b)` exist for `a` (with `plus` returning a subtype of `a`'s type), the compiler **reports an error** rather than silently picking one.

Identity operators `===` and `!==` are **not** overloadable.

**`infix` functions**: a non-operator way to call binary functions without `.` or parentheses:

```kotlin
infix fun Int.pow(n: Int): Int { var r = 1; repeat(n) { r *= this }; return r }
val eight = 2 pow 3
```

Constraints: must be a member or extension function, exactly one parameter, no varargs, no default value.

Reference: [Operator overloading](https://kotlinlang.org/docs/operator-overloading.html).

---

## 9. Coroutines Safety Model

### 9.1 `Mutex`

`kotlinx.coroutines.sync.Mutex` is a *coroutine-aware* mutual exclusion primitive — suspends rather than blocks.

```kotlin
val mutex = Mutex()
mutex.withLock {
    // critical section
}
```

`withLock` is preferred over manual `lock()` / `unlock()` to ensure cancellation safety.

### 9.2 `Semaphore`

`kotlinx.coroutines.sync.Semaphore(permits = N)` — counted suspension semaphore.

```kotlin
val limit = Semaphore(permits = 10)
flow.map { limit.withPermit { fetch(it) } }
```

### 9.3 `kotlinx.atomicfu`

Multiplatform atomic primitives. JVM target compiles to `java.util.concurrent.atomic.*` / `VarHandle`; Native uses platform atomics; JS becomes plain assignments (single-threaded).

```kotlin
val state = atomic(0)
fun increment() { state.update { it + 1 } }    // CAS loop
```

Backs `MutableStateFlow.update`.

### 9.4 Cancellation cooperation primitives

| API | Effect |
|---|---|
| `isActive` | `Boolean` property on `CoroutineScope` and `Job` — checks cancellation. |
| `ensureActive()` | Throws `CancellationException` if not active. |
| `yield()` | Suspension point + active check + chance for fair scheduling. |
| `withContext(NonCancellable) { }` | Run block even after parent cancelled (cleanup). |

### 9.5 Flow exception transparency

A flow is **transparent** to exceptions: any non-`CancellationException` thrown by emitters must propagate to the collector unchanged. Wrapping `emit` in `try/catch` is a runtime error. Use:
- `.catch { e -> ... }` for upstream errors.
- `try/catch` around `collect { }` for downstream errors.
- `.onEach { check(...) }.catch { }` to combine.

---

## 10. Context Receivers → Context Parameters

### 10.1 Why

Functions sometimes need an *implicit* additional context (`Logger`, `CoroutineScope`, `Transaction`, `Density` on Compose) without making it the extension receiver. Pre-2.2 options were:
- Extension functions: only one receiver, must rename `this`.
- Lambda receivers / DSL builders: only works inside lambda blocks.
- Manual parameter threading.

### 10.2 Context receivers (revoked)

The earlier experimental `context(Logger, CoroutineScope) fun foo() { ... }` (KEEP-259 — context receivers) introduced *receivers*, which conflated dispatch and composition and produced confusing scope resolution. **Revoked** in favor of context parameters.

### 10.3 Context parameters (preview in 2.2, KEEP-0367)

```kotlin
interface UserService {
    fun findUser(id: Int): User
    fun log(msg: String)
}

context(users: UserService)
fun byId(id: Int): User {
    users.log("looking up $id")
    return users.findUser(id)
}

// Underscore name when you don't need to reference the context value:
context(_: UserService)
fun greetFirst() = byId(1).also { println("Hi ${it.name}") }
```

Key differences from context receivers:
- A context parameter is **not** automatically a receiver — you must use its name (or `_`) when referring to its members.
- Resolution is unambiguous.
- The compiler can synthesize a unique implementation choice (no "which `this`?" ambiguity).

**Migration from context receivers**: the `context(Foo, Bar) fun ...` syntax is gone. Rewrite as `context(foo: Foo, bar: Bar) fun ...` and explicitly call members via `foo.something()` / `bar.something()`. If you previously used the receiver-style `this@Foo.something()`, capture the parameter name and switch to `foo.something()`.

Status (2026-05): **preview**; enabled with `-Xcontext-parameters`. Callable references to context-parameter functions land in 2.3. IntelliJ IDEA support since 2025.1. Replaces context receivers entirely.

Alternatives still appropriate in many cases:
- Extension functions (`fun Logger.foo()`).
- DSL receivers with lambdas (`buildString { ... }`).
- Plain parameter passing (when the dependency does not need to be implicit at the call site).

Reference: [Context parameters](https://kotlinlang.org/docs/context-parameters.html), [KEEP-0367](https://github.com/Kotlin/KEEP/blob/main/proposals/KEEP-0367-context-parameters.md), [Update on Context Parameters blog](https://blog.jetbrains.com/kotlin/2025/04/update-on-context-parameters/).

---

## 11. Annotations & Reflection

### 11.1 Declaring annotations

```kotlin
@Target(AnnotationTarget.CLASS, AnnotationTarget.FUNCTION)
@Retention(AnnotationRetention.RUNTIME)
@Repeatable
@MustBeDocumented
annotation class Audited(val by: String)

@Audited("alice")
@Audited("bob")
class Order
```

`AnnotationTarget` values: `CLASS`, `ANNOTATION_CLASS`, `TYPE_PARAMETER`, `PROPERTY`, `FIELD`, `LOCAL_VARIABLE`, `VALUE_PARAMETER`, `CONSTRUCTOR`, `FUNCTION`, `PROPERTY_GETTER`, `PROPERTY_SETTER`, `TYPE`, `EXPRESSION`, `FILE`, `TYPEALIAS`.

`AnnotationRetention`: `SOURCE` / `BINARY` / `RUNTIME` (default `RUNTIME`).

### 11.2 Use-site targets

For Kotlin properties that compile to multiple JVM artifacts (field, getter, setter), specify which artifact the annotation lands on:

```kotlin
class User(
    @field:Json("user_id") val id: String,
    @get:JvmName("getEmail") val email: String,
    @param:Inject val tracker: Tracker,
)
```

2.2 added `@all:` (preview) which propagates the annotation to *all* applicable targets (`param`, `property`, `field`, `get`, `setparam`, JVM `RECORD_COMPONENT`):

```kotlin
data class User(@all:Email val email: String)
```

Also new in 2.2: `-Xannotation-default-target=param-property` changes the default target priority order to `param → property → field`.

### 11.3 JVM interop annotations

| Annotation | Effect |
|---|---|
| `@JvmStatic` | On a `companion object` member, emit a true `static` method on the enclosing class. |
| `@JvmField` | Expose property as a `public` field — no getter/setter. |
| `@JvmOverloads` | Generate overloads for each default-parameter combination, callable from Java. |
| `@JvmName("X")` | Override the JVM method/file name. |
| `@JvmInline` | Required marker for `value class` on JVM. |
| `@JvmRecord` | Compile a `data class` to a Java 16+ `record`. |
| `@JvmExposeBoxed` | (2.2+) Add a non-mangled boxed entry point for inline value class methods. |
| `@JvmSerializableLambda` | Keep `LambdaMetafactory`-generated lambdas serializable. |
| `@JvmSuppressWildcards` / `@JvmWildcard` | Control generic wildcard generation in Java signatures. |
| `@Throws(IOException::class)` | Emit `throws` clause for checked-exception consumers in Java. |
| `@JvmDefault*` | (legacy — replaced by the `-jvm-default` compiler option in 2.2). |

### 11.4 Reflection

`kotlin-reflect` is a separate dependency on JVM (`org.jetbrains.kotlin:kotlin-reflect`). Key types:

```kotlin
val klass: KClass<User>     = User::class
val fn:    KFunction1<User,String> = User::name.getter
val prop:  KProperty1<User,String> = User::name
val ctor:  KFunction1<String,User> = ::User

println(klass.qualifiedName)
println(prop.get(User("Alice")))   // "Alice"
println(klass.memberProperties.map { it.name })
```

`::name` produces a callable reference. Bound references attach a receiver:

```kotlin
val u = User("Alice")
val bound: () -> String = u::name.getter
```

JVM bridges: `KClass.java`, `KProperty.javaField`, `KFunction.javaMethod`.

Reference: [Reflection](https://kotlinlang.org/docs/reflection.html), [Annotations spec](https://kotlinlang.org/spec/annotations.html).

### 11.5 KAPT vs KSP (KSP1 deprecated → KSP2 only)

- **KAPT** — wraps `javac`'s annotation-processor API by lowering Kotlin sources to Java stubs first. Slow; fragile w.r.t. Kotlin-only types (inline classes, sealed). **Deprecated** end-of-life: KAPT remains for legacy processors, but Google/JetBrains push KSP. AGP 9+ has dropped first-class KAPT integration.
- **KSP** — Kotlin-native symbol processor API.
  - **KSP1** — operated as a compiler plugin against K1; **deprecated since 2.2.0; will not support Kotlin ≥ 2.3**.
  - **KSP2** (stable as of `2.0.0` of the `com.google.devtools.ksp` plugin; default since `2.0.0`) — standalone source generator that runs against K2's frontend APIs shared with IntelliJ IDEA/Android Lint. Faster, supports newer language features.

Migration path: replace `kapt("...")` with `ksp("...")` in `build.gradle.kts`. Verify all your processors have KSP support — Room, Hilt, Dagger (2.51+), Moshi codegen, Koin annotations are all KSP-ready. If one isn't, isolate it in a module with `kapt.use.k2=false` as a temporary holdout.

Reference: [KSP](https://kotlinlang.org/docs/ksp-overview.html), [`google/ksp` KSP2 doc](https://github.com/google/ksp/blob/main/docs/ksp2.md), [Migrate from kapt to KSP](https://kotlinlang.org/docs/ksp-kapt-migration.html).

---

## 12. Compiler Plugins

Stable compiler plugins ship with Kotlin:

| Plugin | Purpose |
|---|---|
| `kotlinx.serialization` | Generate serializers (JSON/CBOR/Protobuf/HOCON) from `@Serializable` classes. Multiplatform; compile-time, no reflection. |
| `kotlinx.parcelize` | Generate `Parcelable` (Android) from `@Parcelize` classes. |
| `all-open` | Open classes annotated with the supplied set (e.g., `@org.springframework.stereotype.Component`) — Spring/Hibernate need open classes for CGLIB proxies. |
| `no-arg` | Generate a synthetic zero-arg constructor for classes annotated with the supplied set (JPA `@Entity`). |
| `sam-with-receiver` | For specified Java SAM interfaces, treat the first parameter as a receiver in Kotlin lambdas (HotSpot / Gradle DSL friendliness). |
| `kotlin-jpa` | Combination of `all-open` + `no-arg` configured for JPA. |
| `kotlin-spring` | `all-open` preconfigured for Spring annotations. |
| `kotlinx.power-assert` | Enriches `assert(...)` / `check(...)` failure messages with sub-expression values; toggle which functions to instrument via `kotlin { powerAssert { functions = listOf("kotlin.assert", ...) } }`. |
| `Compose Compiler` | Recognizes `@Composable`, generates the skipping/restartable wrappers, performs strong skipping, lambda memoization, and (from Compose Multiplatform 1.7+) emits Compose-Multiplatform-ready bytecode. The plugin moved into the Kotlin distribution itself starting at 2.0.0 via the `kotlin("plugin.compose")` Gradle plugin. |

Reference: [Compiler plugins overview](https://kotlinlang.org/docs/compiler-plugins-overview.html).

---

## 13. K2 Compiler Specifics

### 13.1 New frontend (FIR)

K1's pipeline interleaved resolution, type checking, and IR generation across multiple passes operating on PSI. K2 introduces **FIR (Frontend IR)** — a single semantic data structure built once per compilation unit.

Effects:
- ~2× faster clean builds on average; >90% on some Android projects (`kotlinx-coroutines`, `square/anvil` benchmarks).
- Unified across JVM/JS/Native/Wasm — previously, each backend had its own frontend tweaks.
- Smart-cast improvements (see §2.3) are emergent properties of the new control-flow analysis.
- Error messages now point closer to the actual constraint violation (no more `inferred type ... but ... was expected` cascades several lines away).

### 13.2 IR backend

JVM IR backend has been the default since Kotlin 1.5; in 2.0 the *new* JVM IR backend reaches stable maturity and emits invokedynamic-based lambdas by default. Native IR backend stabilized in 2.0; Wasm IR is on track for stable in 2.x.

### 13.3 Plugin migration to K2

Compiler-plugin authors had to migrate from K1's `ExtensionPoint` model to K2's `FirExtension` family. Stable APIs as of 2.2.0:
- `FirDeclarationGenerationExtension`
- `FirSupertypeGenerationExtension`
- `FirStatusTransformerExtension`
- `FirAdditionalCheckersExtension`

KSP2 is *not* a compiler plugin — it's a standalone process consuming the analyzer's stable APIs. This made KAPT-style "I'm a javac processor" patterns more cleanly portable.

Reference: [K2 compiler performance benchmarks (JetBrains)](https://blog.jetbrains.com/kotlin/2024/04/k2-compiler-performance-benchmarks-and-how-to-measure-them-on-your-projects/).

### 13.4 K2 behavior tightening to plan around

A handful of K1-tolerated patterns are now compile errors under K2. See [`kotlin-anti-patterns.md` §14 (K2 Migration Pitfalls)](./kotlin-anti-patterns.md#14-k2-migration-pitfalls) for the full list; key items:

- **Open property without initializer**: K1 allowed deferred init via `init {}`. K2 forbids — `open val x: Int` with assignment in `init` errors. Fix by initializing at declaration or using a private backing field.
- **Synthetic setter on projected type**: K1 silently allowed `container.foo = value` where `container: Container<*>`; K2 errors (type-safe).
- **Java primitive array nullability**: K2 honors `int @Nullable []` properly.
- **Common code calling platform overload**: K1 occasionally resolved platform-specific overloads from `commonMain`; K2 enforces strict source-set boundaries — silent resolution changes can break behavior. Audit your `commonMain` resolution sites.

---

## 14. Java Interop Subtleties

### 14.1 Platform-type ↔ Kotlin boundary

Casting a platform type to a *strict* Kotlin type may insert a runtime intrinsic null-check (`Intrinsics.checkNotNull`). If a Java method returns `null` and you assigned it to a `String`, the throw happens at the assignment site, not at the use site — that is by design.

Mitigation:
- Treat unfamiliar Java APIs as nullable until proven otherwise.
- Apply nullability annotations or JSpecify `@NullMarked` on the Java side.

### 14.2 Properties to getter/setter

Kotlin properties map to Java getters/setters by JavaBean naming:

| Kotlin | Java getter | Java setter |
|---|---|---|
| `val name: String` | `String getName()` | — |
| `var enabled: Boolean` | `boolean getEnabled()` | `void setEnabled(boolean)` |
| `var isActive: Boolean` | `boolean isActive()` | `void setActive(boolean)` |

`@JvmField` collapses property + getters into a public field. `@JvmName` overrides the generated name for individual accessors:

```kotlin
@get:JvmName("isReady")
val ready: Boolean = true
```

### 14.3 Default parameters and Java

Java cannot call Kotlin methods that use default values without an overload. `@JvmOverloads` synthesizes the cascade:

```kotlin
@JvmOverloads
fun greet(name: String = "World", times: Int = 1) { repeat(times) { println("Hi $name") } }
// From Java:
// greet("Alice", 3);  greet("Alice");  greet();
```

### 14.4 Checked exceptions

Kotlin does not enforce Java checked exceptions. To make a Kotlin method appear `throws` to Java consumers, declare `@Throws`:

```kotlin
@Throws(IOException::class)
fun readAll(path: Path): String = Files.readString(path)
```

### 14.5 Top-level functions on JVM

A file `foo/Util.kt` containing `fun bar()` compiles to class `foo.UtilKt` with method `static bar()`. Override the synthetic class name with `@file:JvmName("Utility")` at the top of the file. Coalesce multiple files into one class with `@file:JvmMultifileClass` + matching `@file:JvmName(...)` on every file.

### 14.6 Inline value classes and Java (`@JvmExposeBoxed`, 2.2+)

By default, inline value classes are **mangled** — `fun handle(p: Password)` becomes `handle-<hash>(String)` so an overload `fun handle(s: String)` is distinguishable. From Java, only the mangled name is callable.

Solutions:
- Annotate the function: `@JvmName("handlePassword") fun handle(p: Password)`.
- 2.2+: annotate the value class with `@JvmExposeBoxed` (or set `-Xjvm-expose-boxed` module-wide) to generate a boxed-form, non-mangled symbol. Two entry points then coexist; consumers pick by language.

```kotlin
@JvmInline
@JvmExposeBoxed                 // 2.2+: also emit Java-friendly non-mangled boxed entry point
value class Password(val raw: String)

fun authenticate(p: Password) { /* ... */ }
// Kotlin callers: authenticate(Password("..."))   — uses unmangled, unboxed (raw String) variant
// Java callers:  authenticate(new Password("...")) — uses the boxed entry point
```

Reference: [Java interop](https://kotlinlang.org/docs/java-interop.html), [Calling Kotlin from Java](https://kotlinlang.org/docs/java-to-kotlin-interop.html).

---

## 15. Recently Stabilized (2.0 → 2.3) — Per-Release Feature Table

| Feature | First seen | Stable in | Notes |
|---|---|---|---|
| K2 compiler (frontend + IR) | 1.7 preview | 2.0 | Default, all targets. Only frontend in 2.3+. |
| `Enum.entries` (`enumEntries<T>()`) | 1.8.20 preview | 2.0 | Replaces `values()`. |
| Stable `AutoCloseable` | 1.8 | 2.0 | `kotlin.AutoCloseable`. |
| Data class consistent `copy` visibility | 2.0.20 warn | 2.2/2.3 enforced | Use `@ConsistentCopyVisibility`. |
| `@SubclassOptInRequired` | 1.8 preview | 2.1 | Opt-in to extend an experimental API. |
| Improved overload resolution (generic vs functional) | 1.9 | 2.1 | Member ≡ extension behavior. |
| Exhaustive `when` over sealed without redundant `else` | 1.9 warn | 2.1 | Compiler enforces tightening. |
| Guard conditions in `when` | 2.1 preview | 2.2 | `is X if cond ->`. |
| Multi-dollar interpolation | 2.1 preview | 2.2 | `$$"... $literal ..."`. |
| Non-local `break` / `continue` (inline lambdas) | 2.1 preview | 2.2 | |
| Nested type aliases | 2.2 preview | 2.3 | KEEP `nested-typealias.md`. |
| Data-flow-based exhaustiveness | 2.2.20 preview | 2.3 | KEEP-0442. |
| Return in expression bodies with explicit type | 2.2 opt-in | 2.3 | Allows `return` shortcut inside `= ...`. |
| `kotlin.time.Instant` | 2.1 preview | 2.3 | KEEP `instant.md`. |
| `Uuid` | 2.0.20 preview | (still preview) | `kotlin.uuid.Uuid`. |
| Base64 / HexFormat | 1.8/1.9 preview | 2.2 | `Base64.Default/UrlSafe/Mime/Pem`. |
| Stable `kotlin-metadata-jvm` | 2.0 | 2.0 | Replaces `kotlinx-metadata-jvm`. |
| Explicit backing fields (`field = ...`) | 2.3 experimental | targeted 2.4 | `-Xexplicit-backing-fields`. |
| Unused-return-value checker | 2.3 experimental | (preview) | `-Xreturn-value-checker`. |

---

## 16. Unstable / Experimental Watch-list

(2026-05 snapshot. **Preview only — do not adopt for production unless explicitly marked Stable above.**)

| Item | Status | KEEP / Issue |
|---|---|---|
| Context parameters | Preview (2.2+); callable refs land in 2.3 | KEEP-0367 / KT-10468 |
| Context-sensitive resolution (enum / sealed) | Preview (2.2 → enhanced 2.3) | KT-16768 |
| Name-based destructuring | Preview (2.3.20) | KT-19627 |
| Explicit backing fields | Experimental (2.3) → Stable in 2.4-RC2 | KT-14663 |
| Unused-return-value checker | Experimental (2.3) | KT-12719 |
| `@all:` use-site target meta + new default rules | Preview (2.2) | KT-73255 |
| `JvmExposeBoxed` (boxed entry points for `value class`) | Experimental (2.2) | KT-28135 |
| Common atomics & atomic arrays in stdlib | Preview (2.2) | KT-62423 (`common-atomics.md`) |
| KMP Kotlin→Java direct actualization | Preview (2.1) | KT-67202 |
| `Uuid` in stdlib | Preview (2.0.20) | KT-31880 |
| `CoroutineContext` as a context parameter | KEEP discussion | KEEP-0443 / KT-15555 |
| Rich Errors (typed errors return) | KEEP discussion | KEEP-0441 / KT-68296 |
| Compile-time constants (extended) | KEEP discussion | KEEP-0444 / KT-22505 |
| Static members / static extensions | KEEP discussion | KT-11968 |
| Collection literals | KEEP discussion | KT-43871 |
| Immutability support | Exploration | KT-77734 |
| Kotlin/JS GC roadmap; K/N memory-model evolution | In progress | (no public KEEP yet) |
| Wasm GC, Wasm stable | Wasm-JS reaches Beta in late 2025; Wasm-WASI Preview | — |
| K/N: Latin-1 string storage | Experimental (2.2) | `kotlin.native.binary.latin1Strings` |
| K/Wasm: Latin-1 UTF-8 string literals | Stable in 2.3 | — |
| KAPT | Deprecated lifecycle | Use KSP2 |
| KSP1 | Deprecated since 2.2; removed for Kotlin 2.3+ | Use KSP2 |
| Revoked: Context receivers | Replaced by context parameters | KEEP-259 → KEEP-0367 |
| Revoked: Java synthetic property references | Reverted | KT-8575 |

---

## 17. Sources

### Kotlin official docs

- [Kotlin docs root](https://kotlinlang.org/docs/)
- [What's new in Kotlin 2.0.0](https://kotlinlang.org/docs/whatsnew20.html)
- [What's new in Kotlin 2.1.0](https://kotlinlang.org/docs/whatsnew21.html)
- [What's new in Kotlin 2.2.0](https://kotlinlang.org/docs/whatsnew22.html)
- [What's new in Kotlin 2.3.0](https://kotlinlang.org/docs/whatsnew23.html)
- [Kotlin language features and proposals (canonical evolution table)](https://kotlinlang.org/docs/kotlin-language-features-and-proposals.html)
- [Null safety](https://kotlinlang.org/docs/null-safety.html)
- [Generics: in, out, where](https://kotlinlang.org/docs/generics.html)
- [Sealed classes and interfaces](https://kotlinlang.org/docs/sealed-classes.html)
- [Inline value classes](https://kotlinlang.org/docs/inline-classes.html)
- [Delegated properties](https://kotlinlang.org/docs/delegated-properties.html)
- [Inline functions](https://kotlinlang.org/docs/inline-functions.html)
- [Operator overloading](https://kotlinlang.org/docs/operator-overloading.html)
- [Annotations spec](https://kotlinlang.org/spec/annotations.html)
- [Reflection](https://kotlinlang.org/docs/reflection.html)
- [Java interop](https://kotlinlang.org/docs/java-interop.html)
- [Calling Kotlin from Java](https://kotlinlang.org/docs/java-to-kotlin-interop.html)
- [Flow](https://kotlinlang.org/docs/flow.html)
- [Coroutine context and dispatchers](https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html)
- [Coroutine exception handling](https://kotlinlang.org/docs/exception-handling.html)
- [Cancellation and timeouts](https://kotlinlang.org/docs/cancellation-and-timeouts.html)
- [Expected and actual declarations](https://kotlinlang.org/docs/multiplatform/multiplatform-expect-actual.html)
- [Hierarchical project structure](https://kotlinlang.org/docs/multiplatform-hierarchy.html)
- [Context parameters](https://kotlinlang.org/docs/context-parameters.html)
- [KSP overview](https://kotlinlang.org/docs/ksp-overview.html)
- [Compiler plugins overview](https://kotlinlang.org/docs/compiler-plugins-overview.html)
- [Migrate from kapt to KSP](https://kotlinlang.org/docs/ksp-kapt-migration.html)

### JetBrains Kotlin blog

- [K2 compiler performance benchmarks (2024-04)](https://blog.jetbrains.com/kotlin/2024/04/k2-compiler-performance-benchmarks-and-how-to-measure-them-on-your-projects/)
- [Kotlin 2.2.0 Released (2025-06)](https://blog.jetbrains.com/kotlin/2025/06/kotlin-2-2-0-released/)
- [Kotlin 2.3.0 Released (2025-12)](https://blog.jetbrains.com/kotlin/2025/12/kotlin-2-3-0-released/)
- [Kotlin 2.3.20 Released (2026-03)](https://blog.jetbrains.com/kotlin/2026/03/kotlin-2-3-20-released/)
- [Update on Context Parameters (2025-04)](https://blog.jetbrains.com/kotlin/2025/04/update-on-context-parameters/)

### KEEP repository

- [KEEP-0367 Context parameters](https://github.com/Kotlin/KEEP/blob/main/proposals/KEEP-0367-context-parameters.md)
- [Context receivers (revoked)](https://github.com/Kotlin/KEEP/blob/master/proposals/context-receivers.md)
- [Sealed interface freedom](https://github.com/Kotlin/KEEP/blob/master/proposals/sealed-interface-freedom.md)
- [Inline classes](https://github.com/Kotlin/KEEP/blob/master/proposals/inline-classes.md)
- [Nested type aliases](https://github.com/Kotlin/KEEP/blob/master/proposals/nested-typealias.md)
- [`google/ksp` KSP2 doc](https://github.com/google/ksp/blob/main/docs/ksp2.md)

### API references

- [`kotlin.contracts.contract`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.contracts/contract.html)
- [`@JvmInline`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.jvm/-jvm-inline/)
- [`@ConsistentCopyVisibility`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-consistent-copy-visibility/) / [`@ExposedCopyVisibility`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-exposed-copy-visibility/)
- [`kotlinx-coroutines-test`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/)
- [`StateFlow`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-state-flow/) / [`SharedFlow`](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-shared-flow/)

### Engineering deep-dives

- [Roman Elizarov — Structured concurrency](https://elizarov.medium.com/structured-concurrency-722d765aa952)
- [Roman Elizarov — Shared Flows, Broadcast Channels](https://elizarov.medium.com/shared-flows-broadcast-channels-899b675e805c)
- [Manuel Vivo — A safer way to collect flows (`repeatOnLifecycle`)](https://manuelvivo.dev/coroutines-addrepeatingjob)
- [kt.academy — Running Kotlin coroutines on Loom's virtual threads](https://kt.academy/article/dispatcher-loom)
- [Effective Kotlin Item 39 — sealed classes and interfaces](https://kt.academy/article/ek-sealed-classes)
- [Effective Kotlin Item 51 — inline functions](https://kt.academy/article/ek-inline-functions)
- [Effective Kotlin Item 52 — value classes](https://kt.academy/article/ek-value-classes)
