# Kotlin Anti-Patterns — Deep Dive Reference

> Companion to the broader Kotlin knowledge in this `builder/reference/` directory. This file covers anti-patterns, pitfalls, footguns, and Detekt/Ktlint smells organized into 17 categories, with each row attributed to a Detekt/Ktlint rule where one exists. Compose UI quirks and Android UI lifecycle issues are **out of scope** here — those belong to the [`native` skill](../../native/SKILL.md). The Compose section in §9 is intentionally narrow: it covers only the **Compose Compiler plugin** angle, not UI patterns.
>
> Baseline: Kotlin 2.3.20 (2026-05 stable) with 2.4-RC2 on EAP; K2 compiler is the only frontend.
>
> Format per section: a quick-reference table of anti-patterns, followed by code snippets for non-obvious cases. Detekt rule reference base: `detekt.dev/docs/rules/<ruleset>/<RuleName>`. Ktlint rules use the canonical `ktlint_standard_*` ids.

---

## Table of Contents

1. [Null Safety Pitfalls](#1-null-safety-pitfalls)
2. [Coroutines Pitfalls](#2-coroutines-pitfalls)
3. [Type / Generics Pitfalls](#3-type--generics-pitfalls)
4. [Class Hierarchy Pitfalls](#4-class-hierarchy-pitfalls)
5. [Companion Object Pitfalls](#5-companion-object-pitfalls)
6. [Property Delegation Pitfalls](#6-property-delegation-pitfalls)
7. [Java Interop Pitfalls](#7-java-interop-pitfalls)
8. [Collection Pitfalls](#8-collection-pitfalls)
9. [Compose Compiler-as-Plugin (NOT UI) Pitfalls](#9-compose-compiler-as-plugin-not-ui-pitfalls)
10. [Smart Cast Pitfalls](#10-smart-cast-pitfalls)
11. [Scope Function Pitfalls](#11-scope-function-pitfalls)
12. [String Pitfalls](#12-string-pitfalls)
13. [Gradle / KSP Pitfalls](#13-gradle--ksp-pitfalls)
14. [K2 Migration Pitfalls](#14-k2-migration-pitfalls)
15. [Testing Pitfalls](#15-testing-pitfalls)
16. [Multiplatform Pitfalls](#16-multiplatform-pitfalls)
17. [API Design Pitfalls](#17-api-design-pitfalls)
18. [Appendix A — Detekt / Ktlint Rule Quick-Lookup Index](#appendix-a--detekt--ktlint-rule-quick-lookup-index)
19. [Sources](#sources)

> **Cross-links:**
> - Language spec (smart cast preconditions, value-class boxing rules, `expect`/`actual`, coroutines exception propagation, K2 frontend) → [`kotlin-language-spec.md`](./kotlin-language-spec.md)
> - Production library choices, dispatcher decisions, KSP2 migration, 2023→2026 migration cheatsheet → [`kotlin-best-practices.md`](./kotlin-best-practices.md)
> - For Compose UI authoring patterns and recomposition pitfalls (state hoisting, remember misuse, stability) → [`native` skill](../../native/SKILL.md). §9 below only addresses the compiler plugin wiring.

---

## 1. Null Safety Pitfalls

| #   | Anti-pattern                                          | Why it bites                                                                                                                                                                    | Fix                                                                                            | Detekt / Ktlint rule                                                                                                |
| --- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 1.1 | `!!` force-unwrap as a default reflex                 | `NullPointerException` at runtime — defeats the entire purpose of Kotlin null safety. Crash bypasses any `?:` fallback paths.                                                   | Use `?.` (safe call), `?:` (Elvis), `requireNotNull`/`checkNotNull` with intent-bearing message. | `potential-bugs/UnsafeCallOnNullableType`, `potential-bugs/UnnecessaryNotNullOperator`                              |
| 1.2 | Double-bang pyramid `a!!.b!!.c!!`                     | One stack trace line, no information about which `!!` failed. Brittle: any nullable upstream blows up.                                                                          | Chain with `?.`, terminate with Elvis; for invariants extract a `requireNotNull(...) { "ctx" }`. | `potential-bugs/UnsafeCallOnNullableType`                                                                            |
| 1.3 | `map[key]!!` on a `Map.get`                           | `Map<K, V>` returns `V?` for absent keys — `!!` masks "I assumed this key existed" as a generic NPE.                                                                            | Use `map.getValue(key)` (throws `NoSuchElementException` with key name) or `getOrElse`.        | `potential-bugs/MapGetWithNotNullAssertionOperator`                                                                  |
| 1.4 | Platform-type trap from Java (`String!`)              | Java returns are imported as platform types — no compile-time null check. `String!` silently becomes `String`; the NPE only fires at first dereference.                         | Always annotate Java with `@Nullable`/`@NotNull`, or wrap in Kotlin with explicit `String?`.   | `potential-bugs/HasPlatformType`                                                                                     |
| 1.5 | `lateinit var` accessed before init                   | Throws `UninitializedPropertyAccessException` (subclass of `RuntimeException`) — different from `NullPointerException`, often missed in catch filters.                          | Prefer constructor injection; if forced, guard with `::prop.isInitialized` or use `by lazy {}`. | `potential-bugs/LateinitUsage` (configurable)                                                                        |
| 1.6 | `lateinit` for nullable types                         | Doesn't compile — yet devs work around with `lateinit var x: Foo? = null` (defeating intent) or `by Delegates.notNull<Foo?>()` (semantically nonsensical).                       | Use `var x: Foo? = null` (plain nullable) and accept the safe-call overhead.                  | n/a (compiler rejects the obvious form)                                                                              |
| 1.7 | `?.let { } ?: ...` when both branches mutate state    | If the `let` block legitimately returns `null` (last expression nullable), the Elvis fallback fires — both branches execute. Looks like if/else, but isn't.                     | Use explicit `if (x != null) { ... } else { ... }` when both branches have side effects.       | n/a (semantic — needs human review)                                                                                  |
| 1.8 | `requireNotNull` vs `checkNotNull` vs `!!` confusion  | `!!` throws raw `NullPointerException` (no context); `requireNotNull` → `IllegalArgumentException` (argument contract); `checkNotNull` → `IllegalStateException` (state contract). Picking wrong type breaks downstream error filters. | Use the decision matrix in §1.A below. | `style/UseRequireNotNull`, `style/UseCheckNotNull` (suggest preconditions over `!!`).                                |
| 1.9 | Null-check on mutable property                        | `if (foo.bar != null) foo.bar.doIt()` — `foo.bar` is a `var`, may change between check and use. No smart cast either.                                                            | Capture to local `val`: `val b = foo.bar ?: return; b.doIt()`.                                  | `potential-bugs/NullCheckOnMutableProperty`                                                                          |
| 1.10 | `?: throw IllegalStateException(...)` boilerplate    | Reinvents `checkNotNull`/`requireNotNull` with messy stack trace and no value-extraction.                                                                                       | `val b = foo.bar ?: error("bar missing")` or `requireNotNull(foo.bar)`.                          | `style/UseCheckOrError`                                                                                              |
| 1.11 | Safe call on already-non-nullable type                | `?.` on a non-nullable value — silently no-op, but reads like "this could be null" and confuses reviewers; also costs a needless branch.                                         | Remove the `?.`. Compiler/IDE warning helps.                                                    | `potential-bugs/UnnecessarySafeCall`, `potential-bugs/UnnecessaryNotNullCheck`                                       |
| 1.12 | `nullable.toString()` returning `"null"`              | When the receiver is nullable, `toString()` yields the literal `"null"` string — silently shows up in user-facing logs/UI.                                                       | Use `nullable?.toString() ?: "<absent>"` or guard explicitly.                                  | `potential-bugs/NullableToStringCall`                                                                                |
| 1.13 | Unsafe cast `x as Foo` on nullable / unknown          | `ClassCastException` (or `TypeCastException`) at runtime.                                                                                                                       | Use `as?` safe cast + Elvis: `(x as? Foo) ?: return`.                                          | `style/SafeCast`, `potential-bugs/UnsafeCast`, `potential-bugs/CastNullableToNonNullableType`                        |
| 1.14 | Returning `null` to mean "not found AND error"        | Caller can't distinguish "not present" from "operation failed". Bug rabbit-hole.                                                                                                | Return `Result<T?>` or a sealed result type. Reserve `null` for legitimate "absent".            | n/a (design rule)                                                                                                    |
| 1.15 | Platform type leaking into public API                 | A public function returns `someJavaCall()` directly — the inferred signature is platform `String!`, making call sites guess null-ability. Breaks consumers in unexpected ways.   | Annotate the return explicitly: `fun foo(): String? = ...` or `fun foo(): String = requireNotNull(...)`.| `potential-bugs/HasPlatformType`                                                                                     |
| 1.16 | Elvis chain hiding shadowed exception                 | `value ?: throw IOException()` inside a coroutine swallows the original cause; replace with `value ?: error(...)` and lose `IOException` type entirely.                          | Pass the original cause: `?: throw IOException("missing", cause)`.                              | n/a                                                                                                                  |
| 1.17 | `(foo as String?).orEmpty()` on platform type         | Pattern looks defensive but encourages keeping the platform type — fragile when Java contract changes.                                                                          | Strongly type at the Java boundary; do not paper over with `orEmpty`.                          | `style/UselessCallOnNotNull`                                                                                         |

### 1.A `requireNotNull` vs `checkNotNull` vs `!!` decision matrix

| Situation                                                        | Use                  | Throws                          |
| ---------------------------------------------------------------- | -------------------- | ------------------------------- |
| Validating a **function argument** (public/external entry point) | `requireNotNull(x)`  | `IllegalArgumentException`      |
| Validating **internal state** of an object                       | `checkNotNull(x)`    | `IllegalStateException`         |
| You **truly know** it's not null and want a value (private code) | `x!!` (rarely)       | `NullPointerException`          |
| External boundary — user input / parsed JSON                     | `?: throw DomainException(...)` | domain-specific exception       |

```kotlin
// BAD
fun fetchUser(id: String?): User {
    val safe = id!!                        // 1.1 raw NPE
    val cached = cache[safe]!!             // 1.3 should be getValue(safe)
    val name = user.profile!!.name!!.uppercase()  // 1.2 double-bang pyramid
    return cached
}

// GOOD
fun fetchUser(id: String?): User {
    requireNotNull(id) { "id must not be null" }          // 1.8 IAE — argument contract
    val cached = cache.getValue(id)                       // 1.3 NoSuchElementException with key
    val name = user.profile?.name?.uppercase()            // 1.2 chain safely
        ?: error("profile.name missing for $id")          // 1.10 ISE — state contract
    return cached
}
```

```kotlin
// BAD 1.7 — let + Elvis with both-branch side effects
user?.let {
    analytics.track("login", it)        // executes if user != null
    null                                // explicit null return → Elvis fires below
} ?: analytics.track("anonymous_login") // BOTH branches fire when user != null but block returns null

// GOOD
if (user != null) {
    analytics.track("login", user)
} else {
    analytics.track("anonymous_login")
}
```

---

## 2. Coroutines Pitfalls

| #    | Anti-pattern                                                       | Why it bites                                                                                                                                                                                                                                  | Fix                                                                                                                                          | Detekt rule                                              |
| ---- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 2.1  | `GlobalScope.launch { ... }`                                       | No parent Job → unstoppable, leaks past component lifetime. No `CoroutineExceptionHandler` → crash on unhandled exception. Hardcodes context, blocks testability.                                                                              | Inject a `CoroutineScope` (viewModelScope / lifecycleScope / a domain scope). For truly app-lifetime tasks, inject an explicit `externalScope`. | `coroutines/GlobalCoroutineUsage`                         |
| 2.2  | `runBlocking { ... }` in production code (esp. inside `suspend`)   | Blocks calling thread. On UI thread → ANR / frozen UI. Inside a `suspend` function it defeats the whole point of coroutines. New IntelliJ 2026 inspection now flags it inline.                                                                | Use `coroutineScope { }` for structured concurrency; `withContext(ctx) { }` for context change.                                                | (IntelliJ inspection — `RunBlockingInSuspendFunction`)    |
| 2.3  | Blocking I/O on `Dispatchers.Default` or `Main`                    | `Default` has only `cores` threads; blocking calls (JDBC, sync HTTP, `Thread.sleep`) stall CPU-bound work. `Main` blocks UI.                                                                                                                  | Wrap blocking calls in `withContext(Dispatchers.IO) { }`. Pass dispatcher in (don't hardcode).                                               | `coroutines/SleepInsteadOfDelay`, `coroutines/InjectDispatcher` |
| 2.4  | `async { }` without `await()`                                      | Exceptions are stored in the `Deferred` until awaited — if never awaited, they're silently lost (the *async exception swallow*). Different from `launch`, which propagates immediately.                                                       | Use `launch` when you don't need the result. Use `async` **only** in pairs with `await()`/`awaitAll()`.                                       | (IntelliJ — `UnusedDeferred`)                            |
| 2.5  | `try { ... } catch (e: Exception) { ... }` inside coroutine        | Catches `CancellationException` and swallows cancellation — the coroutine becomes uncancellable. The parent thinks it cancelled; the child keeps running.                                                                                     | Either catch specific exceptions only, or **rethrow** `CancellationException`: `if (e is CancellationException) throw e`.                    | `coroutines/SuspendFunSwallowedCancellation`              |
| 2.6  | `runCatching { suspendingFn() }`                                   | `runCatching` catches `Throwable`, including `CancellationException`. Same problem as 2.5, with a friendlier API.                                                                                                                              | Use plain `try`/`catch` with explicit types, or `kotlin.Result.runCatching` only around non-suspending blocks. Patch: rethrow CE manually.    | `coroutines/SuspendFunSwallowedCancellation`              |
| 2.7  | `withContext(SupervisorJob()) { ... }`                             | A frequently shipped bug. `withContext` **always uses a regular Job** internally — the passed `SupervisorJob` is ignored. Children's failures still cancel siblings.                                                                          | Use `supervisorScope { }` instead.                                                                                                            | (IntelliJ — `JobAsCoroutineStarterArgument`)              |
| 2.8  | `withContext(sameDispatcher)` chain                                | Each call is a no-op switch but still allocates a `ScopeCoroutine` and re-walks the context. Hot path → GC pressure.                                                                                                                          | Group `withContext` calls; if context is identical, drop the wrapper.                                                                         | n/a (manual review)                                       |
| 2.9  | `Flow.collect { heavyCpuWork(it) }` on `Main`                      | Heavy mapping on the collector's dispatcher — UI freeze if collected from `Main`.                                                                                                                                                              | `.flowOn(Dispatchers.Default)` upstream of the heavy operator, then collect on `Main`. (`flowOn` only affects upstream operators.)            | n/a                                                       |
| 2.10 | `flowOn` on a `StateFlow` / `SharedFlow`                           | **No effect.** `StateFlow.flowOn(...)` silently returns the same flow — `flowOn` (also `conflate`, `cancellable`, `distinctUntilChanged`, `buffer(CONFLATED/RENDEZVOUS)`) is documented to be ignored on shared/state flows.                  | Move the dispatcher switch into the producer side (`.shareIn(scope, ... started)` with upstream `flowOn`).                                    | n/a (doc'd behaviour)                                    |
| 2.11 | `state.value = state.value.copy(...)` for non-atomic update        | Two coroutines reading + copying + writing concurrently → lost update. Last writer wins, intermediate change lost.                                                                                                                            | Use `state.update { it.copy(...) }` or `getAndUpdate { ... }` (extension functions, lock-free CAS).                                          | n/a (semantic)                                            |
| 2.12 | `MutableSharedFlow()` (default) for state                          | `replay = 0`, `extraBufferCapacity = 0`, `BufferOverflow.SUSPEND` — late subscribers miss everything, emitters suspend if no collector.                                                                                                       | For state: use `StateFlow`. For events: `MutableSharedFlow(extraBufferCapacity = 64, onBufferOverflow = DROP_OLDEST)` (or `replay = 1`).      | n/a                                                       |
| 2.13 | `Channel<T>()` where `SharedFlow` fits                             | Channel is single-consumer: a second collector steals events. Tied to lifecycle of receiver — hard to fan-out.                                                                                                                                 | `MutableSharedFlow` (multi-consumer hot stream) is the modern default for one-shot events; reserve `Channel` for back-pressured rendezvous.   | n/a                                                       |
| 2.14 | `Job` cancellation forgotten in lifecycle                          | `scope.launch { while (true) work() }` without ever calling `scope.cancel()` (or using `viewModelScope`) → leaks past view destruction.                                                                                                       | Always tie scope to lifecycle (`viewModelScope`, `lifecycleScope`); avoid manual `Job` references that escape.                               | n/a                                                       |
| 2.15 | Child `async { }`.`await()` swallowing CE silently                 | When parent scope is cancelled while the child `async` is in flight, `await()` throws `CancellationException` — which a generic `catch (e: Throwable)` swallows. Looks like "task finished normally".                                         | Specific `catch`; or `ensureActive()` after `await`.                                                                                          | `coroutines/SuspendFunSwallowedCancellation`              |
| 2.16 | `supervisorScope` vs `coroutineScope` chosen wrong                 | `coroutineScope` propagates **any** child failure up, cancelling siblings. `supervisorScope` isolates failures. Picking the wrong one either kills your other parallel calls or silently ignores failures.                                    | Decision rule: independent siblings (e.g., "load N feeds, partial success OK") → `supervisorScope`. All-or-nothing → `coroutineScope`.        | n/a                                                       |
| 2.17 | Shared mutable state inside `flow { emit(...) }`                   | `flow { }` is cold but the lambda runs on each collection. Shared `var counter` across emissions → race when multiple collectors run on different dispatchers.                                                                                | Keep flow lambdas **pure**. Move state to the producer scope, expose as `StateFlow`.                                                          | n/a                                                       |
| 2.18 | `combine(stateA, stateB) { a, b -> ... }` with mutable upstream    | `combine` emits a value when **any** upstream produces — only the latest values. If `stateA` is being mutated in steps that must be atomic (e.g., paired field updates), `combine` may emit intermediate inconsistent states.                  | Combine related state into a single `data class` and update atomically via `update { it.copy(...) }`.                                         | n/a                                                       |
| 2.19 | `Dispatchers.Unconfined` for normal work                           | Resumes on the thread that **resumed the continuation** — fragile, often Main; defeats dispatcher reasoning.                                                                                                                                  | Use `Default` / `IO` / `Main` explicitly. `Unconfined` is for advanced scenarios only.                                                        | n/a                                                       |
| 2.20 | `Thread.sleep` inside a coroutine                                  | Blocks the worker thread, starving other coroutines on the same dispatcher.                                                                                                                                                                    | `delay(...)` (suspending equivalent).                                                                                                         | `coroutines/SleepInsteadOfDelay`                          |
| 2.21 | `suspend fun foo(): Flow<T>`                                       | A `Flow` is already a cold lazy value — adding `suspend` requires the caller to be in a coroutine just to **obtain** the flow, then again to collect. Confusing layering.                                                                     | Return `Flow<T>` from a non-suspending function. Initial values can come from `onStart { emit(initial) }`.                                    | `coroutines/SuspendFunWithFlowReturnType`                 |
| 2.22 | `suspend fun foo(): X` taking a `CoroutineScope` receiver          | Ambiguous: caller's `Job` or the suspend caller's? Bad layering of structured concurrency.                                                                                                                                                    | Either drop the receiver, or change to a non-suspending function on a scope.                                                                  | `coroutines/SuspendFunWithCoroutineScopeReceiver`         |
| 2.23 | `coroutineContext` instead of `currentCoroutineContext()`          | Inside a suspending function, the property `coroutineContext` is **the caller's**, not the resumed one. In nested scopes you get the wrong context.                                                                                            | Use `currentCoroutineContext()` (the function).                                                                                               | (IntelliJ — `CoroutineContextProperty`)                   |
| 2.24 | `deferreds.map { it.await() }`                                     | Sequential — defeats parallelism. Also, if one fails, the still-running ones aren't cancelled.                                                                                                                                                | Use `awaitAll(deferreds)` — concurrent await, fails fast and cancels siblings.                                                                | (IntelliJ — `MissingAwaitAll`)                            |
| 2.25 | `suspendCoroutine { ... }` for low-level wrapping                  | Not cancellable — when parent scope cancels, the underlying callback continues; the `Continuation` is leaked.                                                                                                                                  | `suspendCancellableCoroutine { cont -> cont.invokeOnCancellation { ... } }`.                                                                  | (IntelliJ — `SuspendCancellableCoroutine`)                |
| 2.26 | Suspending call inside `finally` without `withContext(NonCancellable)` | Once the coroutine is cancelled, any suspending call in `finally` immediately throws `CancellationException` → cleanup never finishes (file not closed, transaction not rolled back).                                                          | Wrap cleanup: `finally { withContext(NonCancellable) { rollback() } }`.                                                                       | `coroutines/SuspendFunInFinallySection`                   |
| 2.27 | `@Test fun foo() = runBlocking { ... }`                            | Real time used (no virtual `delay`-skip), real dispatchers, no leak detection — tests hang or flake.                                                                                                                                          | `runTest { ... }` (kotlinx-coroutines-test). See §15.                                                                                          | `coroutines/CoroutineLaunchedInTestWithoutRunTest`        |
| 2.28 | Calling `Dispatchers.IO.limitedParallelism(N)` per call site       | Each call creates a **new** view → no shared limit. Connection-pool starvation prevention fails.                                                                                                                                              | Create the limited dispatcher **once** in a DI module; inject it.                                                                             | n/a                                                       |

### 2.A Visual: `launch` vs `async` exception propagation

```kotlin
// launch propagates immediately → handler fires
GlobalScope.launch(handler) { throw IOException() }  // handler sees IOException

// async stores in Deferred → silent until await
val d = scope.async { throw IOException() }
// no exception yet
d.await()  // NOW throws
```

```kotlin
// 2.5 — silently broken cancellation
suspend fun load() {
    try {
        repository.fetch()
    } catch (e: Exception) {       // catches CancellationException!
        log.warn("fetch failed", e)  // swallows cancellation → coroutine zombie
    }
}

// 2.5 — fix
suspend fun load() {
    try {
        repository.fetch()
    } catch (e: CancellationException) {
        throw e                    // re-throw — propagate cancellation
    } catch (e: IOException) {
        log.warn("fetch failed", e)
    }
}
```

```kotlin
// 2.7 — withContext does NOT honor SupervisorJob
withContext(Dispatchers.IO + SupervisorJob()) {       // BUG: SupervisorJob ignored
    launch { throw RuntimeException("a") }            // cancels sibling 'b' anyway
    launch { delay(1000); println("b done") }         // never prints
}

// 2.7 — fix
supervisorScope {
    launch(Dispatchers.IO) { throw RuntimeException("a") }
    launch(Dispatchers.IO) { delay(1000); println("b done") }  // prints
}
```

```kotlin
// 2.11 — non-atomic StateFlow update
data class UiState(val count: Int = 0, val lastUser: String = "")
val state = MutableStateFlow(UiState())

// BAD — race
state.value = state.value.copy(count = state.value.count + 1)

// GOOD — atomic, lock-free CAS
state.update { it.copy(count = it.count + 1) }
```

```kotlin
// 2.26 — cleanup eaten by cancellation
suspend fun useResource() {
    val resource = openResource()
    try {
        process(resource)
    } finally {
        resource.close()              // suspending close — throws CancellationException, file leaked
    }
}

// Fix
suspend fun useResource() {
    val resource = openResource()
    try {
        process(resource)
    } finally {
        withContext(NonCancellable) { resource.close() }
    }
}
```

---

## 3. Type / Generics Pitfalls

| #    | Anti-pattern                                                | Why it bites                                                                                                                                                                                                | Fix                                                                                                                                          | Detekt rule                          |
| ---- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| 3.1  | Overuse of `Any` / `Any?` in public API                     | Caller must cast → unsafe, brittle to refactors. Reads like the API author "doesn't know".                                                                                                                  | Sealed hierarchy, generic with bounds, or marker object instead of `Any?` for "no data".                                                     | n/a (design)                          |
| 3.2  | Missing variance annotation (`out` / `in`)                  | `Producer<Cat>` not assignable to `Producer<Animal>` even though logically it should be. Callers resort to use-site projection (`Producer<out Animal>`) at every call.                                       | Declare site variance: `interface Producer<out T>` for read-only, `Consumer<in T>` for write-only.                                           | n/a                                   |
| 3.3  | Use-site projection where declaration-site is possible      | Pollutes every signature with `out`/`in`. Hides intent.                                                                                                                                                     | If the class is truly co/contravariant, use declaration-site.                                                                                | n/a                                   |
| 3.4  | `inline fun <T>` without `reified` when `T::class` needed   | `Class<T>` reflection / `T::class.java` fails at compile time — devs work around by passing `clazz: Class<T>` as a parameter, defeating the inline-typed API.                                              | Add `reified T`: `inline fun <reified T> typeOf(): KClass<T> = T::class`.                                                                    | n/a                                   |
| 3.5  | Inline lambda escaping → compile error without `crossinline` | Passing the lambda to a non-inlined context (object literal, another lambda, deferred call) causes "Non-local return is not allowed".                                                                       | Mark `crossinline lambda: () -> Unit`.                                                                                                       | n/a (compiler)                        |
| 3.6  | `inline fun` with a non-inlining lambda parameter           | Some lambdas are only stored, not invoked — inlining them is wasteful (every call site duplicates closure init).                                                                                            | Mark `noinline` on lambdas that escape: `inline fun foo(action: () -> Unit, noinline callback: () -> Unit)`.                                  | n/a                                   |
| 3.7  | `inline` on a huge function                                 | Body copied to every call site → bytecode bloat (DEX 64K limit on Android, slower JIT warm-up).                                                                                                             | Inline **small** higher-order functions. Detekt has rules to cap inline size.                                                                 | (custom rule)                         |
| 3.8  | Value class boxed when used as generic / nullable / interface | `value class UserId(val v: String)`: as `List<UserId>` or `UserId?` or `Any` (interface), the value is boxed at runtime — losing the zero-cost benefit.                                                     | Document the boxing rules; use plain `String` typealias if heavy boxing is anticipated; or accept the box in cold paths.                     | n/a                                   |
| 3.9  | Generic class with deeply nested bounds                     | `class Repo<T : Comparable<T>, U : Map<K, T>, K : Enum<K>>` — caller must spell all of them.                                                                                                                | Decompose; consider non-generic facade.                                                                                                       | n/a                                   |
| 3.10 | `vararg` followed by spread `*arr`                          | The spread operator **copies** the array. In a hot loop, allocations dominate.                                                                                                                              | Use `vararg` only when needed; for static cases, pass the array directly via constructors when possible.                                     | `performance/SpreadOperator`          |
| 3.11 | `Array<Int>` instead of `IntArray`                          | `Array<Int>` is `Integer[]` (boxed); `IntArray` is `int[]`. Up to ~23× perf gap in tight loops, plus heap churn.                                                                                            | Use specialized primitive arrays: `IntArray`, `LongArray`, `DoubleArray`, etc.                                                                | `performance/ArrayPrimitive`          |

```kotlin
// 3.1 — Any? as "no value"
fun lookup(key: String): Any? = ...                           // caller forced to cast

// fix — sealed type
sealed interface Lookup<out V> {
    data class Found<V>(val value: V) : Lookup<V>
    object NotFound : Lookup<Nothing>
}

// 3.2 — declaration-site variance
// BAD — invariant, callers can't pass Producer<Cat> where Producer<Animal> expected
interface Producer<T> { fun produce(): T }

// GOOD
interface Producer<out T> { fun produce(): T }   // covariant; can use Cat as Animal

// 3.4 — reified type parameter
inline fun <reified T> Bundle.parcelable(key: String): T? =
    if (Build.VERSION.SDK_INT >= 33) getParcelable(key, T::class.java)
    else @Suppress("DEPRECATION") getParcelable(key) as? T

// 3.5 — crossinline
inline fun runLater(crossinline block: () -> Unit) {
    Handler(Looper.getMainLooper()).post { block() }  // escaped lambda → must be crossinline
}

// 3.6 — noinline for lambdas that escape but aren't worth inlining
inline fun foo(
    immediate: () -> Unit,                // inlined
    noinline deferred: () -> Unit,        // not inlined — can be stored in a field
) {
    val store: () -> Unit = deferred       // legal because of noinline
    immediate()
}

// 3.8 — value class boxing
@JvmInline
value class UserId(val v: String)
fun lookup(id: UserId) {}                  // unboxed
fun all(): List<UserId> = listOf()         // boxed (generic) — List<Object> at JVM level
val opt: UserId? = null                    // boxed (nullable) — needs object header for null bit
interface IdConsumer { fun take(id: Any) } // boxed (interface upcast)

// 3.11 — IntArray vs List<Int>
val xs: List<Int> = (1..1_000_000).toList()    // Integer[] under the hood → ~16MB, GC pressure
xs.sum()                                        // unboxes per element

val ys: IntArray = IntArray(1_000_000) { it }   // int[] → ~4MB, contiguous
ys.sum()                                        // primitive loop — JIT-friendly
```

---

## 4. Class Hierarchy Pitfalls

| #    | Anti-pattern                                              | Why it bites                                                                                                                                                                            | Fix                                                                                                                                       | Detekt rule                                                    |
| ---- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| 4.1  | `open class` everywhere by Java reflex                    | Kotlin is **final by default for a reason** (fragile base class). Reflexively `open`-ing every class invites broken Liskov contracts and binary-incompat changes.                       | Default to `final`. Open only what is designed for inheritance, with documented contract.                                                  | n/a                                                            |
| 4.2  | `data class` with mutable `var` properties                | Mutating a property changes `hashCode()` → object is "lost" in `HashSet`/`HashMap`. Breaks the equality contract.                                                                       | All data class properties `val`; create new instances via `copy(...)`.                                                                     | `style/DataClassShouldBeImmutable`                              |
| 4.3  | `equals` overridden without `hashCode`                    | Violates Object contract: equal objects must hash equal. Hash-based collections silently misbehave.                                                                                     | Always override both. IDE/Detekt warns.                                                                                                    | `potential-bugs/EqualsWithHashCodeExist`                        |
| 4.4  | `data class` inheritance without thinking                 | Pre-1.1 data classes can't extend each other (now allowed but error-prone). `equals` only considers primary-constructor props; properties defined in the body are excluded.            | Prefer composition; if extending, double-check `equals`/`hashCode` scope.                                                                  | n/a                                                            |
| 4.5  | Exposing `MutableList<T>` from a class                    | Callers mutate state without going through methods → uncontrollable invariants. Encapsulation broken.                                                                                  | Expose `List<T>`; keep `mutableListOf` `private`.                                                                                          | `potential-bugs/DontDowncastCollectionTypes`                    |
| 4.6  | `sealed class` in cross-module **public** API             | Adding a variant in version N+1 is **binary-breaking** for downstream `when` exhaustiveness. Most consumers compile-fail.                                                                | Use `sealed interface` (more flexible) and consider `abstract class` if true extensibility is needed. Document evolution policy.            | n/a                                                            |
| 4.7  | `enum class` with behavior diverging per constant         | `enum` enforces same-shape members. Heavy when-branches creep in. Hard to evolve.                                                                                                       | Convert to `sealed class` with `data object` variants.                                                                                     | n/a                                                            |
| 4.8  | `object : Listener { ... }` for a single-method interface | Verbose anonymous object — Kotlin supports SAM conversion / functional interfaces directly.                                                                                            | Use a lambda with `fun interface` or SAM-converted Java interface.                                                                         | `style/ObjectLiteralToLambda`                                   |
| 4.9  | `inner class` retaining outer reference                   | Holds an implicit reference to the outer instance → leak when the outer is meant to be short-lived (Fragment / Activity / ViewModel).                                                  | Use `class` (nested, not inner) when no outer access is required.                                                                          | `style/UnnecessaryInnerClass`                                   |
| 4.10 | `abstract class` with no abstract members                 | Just `open class` with extra step. No abstract API → no actual abstraction.                                                                                                            | Make concrete (or, if pure contract, interface).                                                                                           | `style/AbstractClassCanBeConcreteClass`, `AbstractClassCanBeInterface` |
| 4.11 | `protected` member in a `final class`                     | `protected` is meaningless without inheritance — accessible only inside the class itself, same as `private`.                                                                            | Switch to `private`.                                                                                                                       | `style/ProtectedMemberInFinalClass`                             |
| 4.12 | Inheriting from `Any` explicitly                          | `class Foo : Any()` — pointless; every class implicitly extends `Any`.                                                                                                                  | Drop it.                                                                                                                                   | `style/UnnecessaryInheritance`                                  |

```kotlin
// 4.2 — mutable data class destroying HashSet semantics
data class Tag(var name: String)
val set = hashSetOf(Tag("a"))
set.first().name = "b"
println("a" in set.map { it.name })   // false
println(Tag("b") in set)              // false — different hash bucket
// the set is corrupted

// 4.6 — sealed evolution problem
// module-api 1.0
sealed class Event { data class Login(...) : Event(); data class Logout(...) : Event() }

// module-api 1.1 adds:
sealed class Event { ...; data class TokenRefresh(...) : Event() }
// Every downstream `when (event)` that was exhaustive now MUST compile-fail
// → binary incompatible change.
```

---

## 5. Companion Object Pitfalls

| #   | Anti-pattern                                                       | Why it bites                                                                                                                                                                                                   | Fix                                                                                                              | Detekt rule         |
| --- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------- |
| 5.1 | Using `companion object` as a "namespace" for unrelated utilities  | Generates a synthetic inner class + extra static `Companion.INSTANCE` field. More bytecode + tighter coupling than top-level functions.                                                                       | Use top-level functions in a `package.kt` file. They're cleaner and JIT-friendlier.                              | n/a                 |
| 5.2 | Heavy initialization inside `companion object { init { ... } }`    | The `init` block runs on class load — eager DB / network / file I/O at startup. Hard to mock.                                                                                                                  | Lazy init via `by lazy { }` or DI.                                                                               | n/a                 |
| 5.3 | `const val` misused on non-primitive                               | `const val LIST = listOf("a")` — compile error. Devs sometimes reach for `@JvmField val` and lose the compile-time `static final` benefit.                                                                     | Keep `const val` for compile-time constants only (primitives + `String`). For others, plain `val` in companion. | n/a                 |
| 5.4 | Companion-enclosed constants for static-only values                | `class Foo { companion object { const val MAX = 10 } }` works but generates redundant boilerplate compared to top-level `const val MAX = 10`.                                                                  | Top-level `const val`. Companion only when scoping to the class is semantically valuable.                        | n/a                 |
| 5.5 | Companion as a factory bag holding singletons                      | Hidden lifecycle; the companion lives as long as the class is loaded. Test isolation hell.                                                                                                                     | Explicit factory + DI.                                                                                           | n/a                 |
| 5.6 | `@JvmStatic` forgotten on companion methods exposed to Java        | Java callers must write `Foo.Companion.bar()` instead of `Foo.bar()`. Looks accidental.                                                                                                                        | Annotate intended-as-static members with `@JvmStatic`.                                                           | n/a                 |

```kotlin
// 5.1/5.4 — bloated companion
class Calc {
    companion object {
        const val MAX = 100
        fun sumOfSquares(n: Int) = (1..n).sumOf { it * it }
    }
}
// Generated bytecode: Calc$Companion class + INSTANCE field.

// fix
const val CALC_MAX = 100
fun sumOfSquares(n: Int) = (1..n).sumOf { it * it }

// 5.2 — heavy companion init
class ApiClient {
    companion object {
        init {
            // Runs on first class load — EAGER. Hard to mock; breaks test isolation.
            loadCertificates()
            warmupConnectionPool()
        }
    }
}

// fix — lazy
class ApiClient(
    certificates: () -> CertStore = { loadCertificates() },
    pool: () -> ConnectionPool = { warmupConnectionPool() },
) {
    private val certs by lazy(LazyThreadSafetyMode.PUBLICATION) { certificates() }
    private val connPool by lazy(LazyThreadSafetyMode.PUBLICATION) { pool() }
}

// 5.6 — @JvmStatic for Java
class Logger {
    companion object {
        @JvmStatic                          // Java: Logger.log(...)
        fun log(msg: String) = println(msg)

        fun warnNoStatic(msg: String) { }    // Java: Logger.Companion.warnNoStatic(...) — ugly
    }
}
```

---

## 6. Property Delegation Pitfalls

| #   | Anti-pattern                                            | Why it bites                                                                                                                                                              | Fix                                                                                                       | Detekt rule |
| --- | ------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ----------- |
| 6.1 | `by lazy { }` default `SYNCHRONIZED` mode in hot paths  | Default uses a lock + double-checked-locking. Per-access overhead in tight loops, even after init.                                                                        | Pick `LazyThreadSafetyMode.PUBLICATION` (CAS, racy init OK) or `NONE` (single-thread guarantee).          | n/a         |
| 6.2 | `by lazy(LazyThreadSafetyMode.NONE) {}` used cross-thread | If the property is accessed from another thread, behaviour is **unspecified**. May double-init, throw, or return torn value.                                              | Use `NONE` only when the access thread is known constant (UI thread, init flow).                          | n/a         |
| 6.3 | `lateinit var` for nullable                             | Forbidden by compiler — devs work around with `lateinit var x: Foo? = null` (semantically vacuous, always non-null).                                                      | Use `var x: Foo? = null`.                                                                                 | n/a         |
| 6.4 | Property delegate retaining heavy state                 | A custom `ReadWriteProperty` instance captures the owning class implicitly. Long-lived delegates (e.g., on object singletons) retain entire object graphs.               | Use `WeakReference` inside the delegate; or release in lifecycle callbacks.                              | n/a         |
| 6.5 | `Delegates.observable` handler that throws              | The handler runs synchronously on assignment. An exception in the handler propagates back to the setter — and other observers (if chained) never fire.                  | Wrap handler body in `runCatching { }` (rethrow CE for coroutines).                                       | n/a         |
| 6.6 | Fragment-view delegate without auto-clear               | `private val binding by viewBinding<T>()` keeps a reference to the view past `onDestroyView` → Activity context leaks via view tree.                                     | Use an "auto-clear-on-destroy" delegate (FragmentViewBindingDelegate pattern). (UI-lifecycle detail — see [`native` skill](../../native/SKILL.md) for full lifecycle coverage.) | n/a         |

### 6.A `LazyThreadSafetyMode` decision matrix

| Mode             | Locking        | Threads compute   | Result published                 | When to use                                                   |
| ---------------- | -------------- | ----------------- | -------------------------------- | ------------------------------------------------------------- |
| `SYNCHRONIZED` (default) | Lock           | Only one (others wait) | One value                        | Multi-threaded access + initializer is expensive AND idempotent. Safe default. |
| `PUBLICATION`    | CAS (lock-free) | Possibly many concurrently | First-wins CAS                   | Multi-threaded access + initializer is **cheap** (re-running fine).            |
| `NONE`           | None           | Possibly many concurrently | **Undefined** if cross-thread    | Single-thread only (UI-only data, init phase). Use with care.                  |

```kotlin
// 6.1 — hot path with synchronized lazy
class Renderer {
    private val cache by lazy { computeExpensiveAtlas() }     // SYNCHRONIZED default
    fun draw() = cache.use()                                    // lock-acquire per call
}

// fix
class Renderer {
    private val cache by lazy(LazyThreadSafetyMode.PUBLICATION) { computeExpensiveAtlas() }
    fun draw() = cache.use()
}

// 6.4 — delegate retains heavy state
class Cache : ReadWriteProperty<Any?, Int> {
    private var value: Int = 0
    private val expensiveLog = mutableListOf<String>()     // grows unbounded over the property's life
    override fun getValue(thisRef: Any?, property: KProperty<*>) = value.also { expensiveLog += "get" }
    override fun setValue(thisRef: Any?, property: KProperty<*>, value: Int) {
        this.value = value
        expensiveLog += "set"
    }
}
// If used by a long-lived companion or top-level property, `expensiveLog` outlives the app session.

// 6.5 — observable swallowing exceptions
var name by Delegates.observable("") { _, old, new ->
    notifyListeners(old, new)      // if a listener throws, the setter throws — `name` was already changed!
}

// fix
var name by Delegates.observable("") { _, old, new ->
    runCatching { notifyListeners(old, new) }
        .onFailure { e ->
            if (e is CancellationException) throw e
            log.warn("listener failed", e)
        }
}
```

---

## 7. Java Interop Pitfalls

| #   | Anti-pattern                                                      | Why it bites                                                                                                                                                                          | Fix                                                                                                                  | Detekt rule    |
| --- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------- |
| 7.1 | Default arguments without `@JvmOverloads`                         | Java callers can't use the Kotlin default — they must pass every argument. Bridge methods missing.                                                                                  | `@JvmOverloads fun foo(a: Int, b: Int = 0)` generates Java overloads.                                                | n/a            |
| 7.2 | `@JvmField` on a `var` exposed publicly                           | Java code can assign `null` despite Kotlin declaring `var name: String` — bypasses Kotlin null check; NPE on next Kotlin read.                                                       | Avoid `@JvmField` on cross-language mutable state, or annotate Java sources with `@NotNull`.                          | n/a            |
| 7.3 | Missing `@JvmName` on overloads sharing JVM signature              | `fun List<Int>.sum(): Int` and `fun List<String>.sum(): String` compile in Kotlin but **same JVM signature** — clash.                                                                | `@JvmName("sumInts")` / `@JvmName("sumStrings")`.                                                                    | n/a            |
| 7.4 | Missing `@Throws` for checked exceptions thrown into Java          | Kotlin doesn't have checked exceptions; Java caller doesn't know to catch `IOException`. Silent crash, lost stack info.                                                              | `@Throws(IOException::class) fun read()` signals the checked exception in the JVM signature.                          | n/a            |
| 7.5 | Java-style getters/setters in Kotlin (`getFoo()` / `setFoo()`)     | Bypasses property syntax (`obj.foo`) → ugly call sites, extra Kotlin sugar overhead.                                                                                                 | Use `val foo: T` / `var foo: T`. Annotate with `@get:JvmName("getFoo")` only if Java callers expect a custom name.   | n/a            |
| 7.6 | `KFunction.call` reflection in hot path                            | Goes through slow reflection. Allocations + box.                                                                                                                                     | Capture as a lambda, or use `kotlin-reflect` only at init.                                                            | n/a            |
| 7.7 | Returning `kotlin.Result<T>` to Java                              | Java doesn't see `Result` nicely — it's a value class that boxes; Java sees `Object`. Painful interop.                                                                               | Expose a Java-friendly equivalent (sealed result, or `Optional` + custom exception).                                 | n/a            |
| 7.8 | Returning `kotlin.Unit` from a Java-callable function             | Java sees `Unit.INSTANCE` — surprising; functional callers can't treat as `void`.                                                                                                    | Annotate the Kotlin function as `Unit`-returning is fine, but for Java-callable APIs prefer `Void` return + `null`.  | n/a            |
| 7.9 | Lambdas with default args exposed to Java SAM conversion           | `fun <T> action(block: (T, Int) -> Unit = { _, _ -> })` — Java can't supply a default; SAM bridge gets confused.                                                                     | Provide both: one Java-overload that accepts SAM, one Kotlin-overload with defaults.                                 | n/a            |
| 7.10 | `internal` modifier exposed to Java                                | Kotlin `internal` mangles names but is still callable from Java (with mangled name). Devs assume true privacy.                                                                       | Document; for actual privacy use `private` (file-level for top-level decls).                                          | n/a            |

```kotlin
// 7.1 — JvmOverloads
class Banner @JvmOverloads constructor(
    val title: String,
    val subtitle: String = "",
    val cta: String? = null,
)
// Java sees: Banner(String), Banner(String,String), Banner(String,String,String).

// 7.2 — @JvmField on var defeats Kotlin nullability
class Config {
    @JvmField var apiKey: String = "default"
}
// Java code:
//   Config c = new Config();
//   c.apiKey = null;                  // Java has no idea apiKey is non-null!
//   Kotlin code reading c.apiKey.length → NPE

// 7.3 — JvmName clash
@JvmName("filterInts")
fun List<Int>.filterPositive() = filter { it > 0 }
@JvmName("filterDoubles")
fun List<Double>.filterPositive() = filter { it > 0 }
// Without @JvmName, both compile to filterPositive(Ljava/util/List;)Ljava/util/List; — clash.

// 7.4 — @Throws for Java callers
@Throws(IOException::class)
fun readConfig(path: Path): Config { /* may throw IOException */ }
// Now Java sees:  public Config readConfig(Path) throws IOException;

// 7.10 — internal is NOT private to Java
internal class SecretImpl { fun secret() = "🔑" }
// Java can call:
//   SecretImpl$default$/* mangled */.secret();
// Use `private` for true privacy at the file level.
```

---

## 8. Collection Pitfalls

| #    | Anti-pattern                                                   | Why it bites                                                                                                                                                            | Fix                                                                                                                                                | Detekt rule                                       |
| ---- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| 8.1  | Exposing `MutableList`/`MutableSet`/`MutableMap`               | Caller can mutate internal state. Encapsulation broken.                                                                                                                 | Expose `List`/`Set`/`Map`; keep mutable variant private.                                                                                           | n/a                                               |
| 8.2  | Eager `.map { }.filter { }.map { }` on large collection        | Each step allocates a new `ArrayList` of size ≈N. For N=10⁶ that's 3 lists.                                                                                             | `list.asSequence().map { }.filter { }.map { }.toList()` — single-pass, no intermediate lists.                                                       | `performance/CouldBeSequence`                     |
| 8.3  | Sequence overhead on tiny collections                          | Sequences have setup overhead — ~9% slower than eager `.map` for small N and simple ops.                                                                                | Use sequences for **large** N or **3+** chained ops. For small fixed data, eager `.map { }` is faster. (See [`kotlin-best-practices.md` §8.1](./kotlin-best-practices.md#81-sequence-vs-iterable-break-even-2025-2026-update--conventional-wisdom-inverted) for the 2025-2026 break-even data.) | n/a (judgement)                                   |
| 8.4  | Repeated `Iterable.toList()` on a sequence                     | Re-iterates each time → re-runs upstream operators. Sequences are not memoized.                                                                                         | Convert to list **once** and cache. Or use `Iterable`/`List` from the start.                                                                       | n/a                                               |
| 8.5  | `List<Int>` for hot numeric work                               | Boxed `Integer` per element → 16 bytes object header + reference. 4–23× slower than `IntArray` (`int[]`).                                                              | `IntArray`, `LongArray`, `DoubleArray`.                                                                                                            | `performance/ArrayPrimitive`                      |
| 8.6  | `mutableListOf<T>()` then exposing                             | Concrete `ArrayList<T>` leaks; consumers depend on its (mutable) API.                                                                                                  | Convert at boundary: `return result.toList()` (immutable copy).                                                                                    | n/a                                               |
| 8.7  | `.toMutableList()` copy where in-place ok                      | Allocates a new `ArrayList`; the old list is garbage.                                                                                                                  | If you own the list and it's already mutable, mutate it.                                                                                          | n/a                                               |
| 8.8  | `forEach` on an `IntRange` instead of `for` loop               | The `forEach` lambda boxes the `Int` argument; allocates an iterator. The plain `for` is a `for-i` loop on the JVM.                                                    | `for (i in 0 until n) { ... }`.                                                                                                                    | `performance/ForEachOnRange`                      |
| 8.9  | `assertEquals(setA, setB)` with `List` arg                     | `Set` equality is unordered, `List` equality is ordered — mismatched types silently fail.                                                                              | Use matching collection types in both sides; or `containsExactlyInAnyOrder`.                                                                       | n/a                                               |
| 8.10 | `list.find { ... } != null`                                    | Allocates and binds the matched element just to discard it.                                                                                                            | `list.any { ... }` (no allocation).                                                                                                                | `style/UseAnyOrNoneInsteadOfFind`                 |
| 8.11 | `list.flatMap { it.children }.size`                            | Allocates the intermediate `flatMap` list just to count.                                                                                                               | `list.sumOf { it.children.size }`.                                                                                                                  | `style/UseSumOfInsteadOfFlatMapSize`              |
| 8.12 | `list.filter { ... }.first()`                                  | Filter materializes the full filtered list; only first needed.                                                                                                         | `list.first { ... }`.                                                                                                                              | n/a                                               |
| 8.13 | `map.containsKey(k) && map[k] != null`                         | Double lookup. Also brittle if value can legitimately be `null`.                                                                                                       | Use `map[k] ?: default`; or for true presence-check, `k in map`.                                                                                  | n/a                                               |
| 8.14 | Downcasting a `List` to `MutableList`                          | `(list as MutableList)` — `ClassCastException` if the underlying impl is immutable. Even when it works, breaks encapsulation contract.                                  | Make a copy: `list.toMutableList()`.                                                                                                               | `potential-bugs/DontDowncastCollectionTypes`      |
| 8.15 | `var list = mutableListOf<T>()`                                | `var` + mutable collection: TWO mutation axes (reassign + mutate). Reasoning hell.                                                                                     | Pick one: `val list = mutableListOf<T>()` OR `var list = listOf<T>()`.                                                                              | `potential-bugs/DoubleMutabilityForCollection`    |

```kotlin
// 8.2 — eager chain
val result = bigList.map { it.upper() }.filter { it.startsWith("A") }.map { it.length }
// For N=10^6, allocates: ArrayList(10^6) + ArrayList(~filtered) + ArrayList(~filtered)
// Each step iterates the previous list end-to-end → 3 full passes.

// fix
val result = bigList.asSequence()
    .map { it.upper() }
    .filter { it.startsWith("A") }
    .map { it.length }
    .toList()
// Single pass; intermediate lambdas chained; only the final list is allocated.

// 8.3 — but tiny collections lose to sequence overhead
val tiny = listOf(1, 2, 3, 4)
tiny.asSequence().map { it * 2 }.filter { it > 4 }.toList()   // ~9% SLOWER than eager
tiny.map { it * 2 }.filter { it > 4 }                          // 4-element extra alloc, but no setup cost

// 8.5 — primitive boxing
fun sumBoxed(xs: List<Int>): Int = xs.sum()           // unbox per element from Integer[]
fun sumPrimitive(xs: IntArray): Int = xs.sum()        // primitive int[] — JIT vectorizes

// 8.8 — forEach on range allocates iterator + boxes
(0..1_000_000).forEach { i -> work(i) }               // BAD — Iterator + Integer boxing
for (i in 0..1_000_000) work(i)                        // GOOD — pure for-i loop

// 8.10 — find vs any
if (list.find { it.id == target } != null) ...         // allocates the found element, then discards
if (list.any { it.id == target }) ...                  // returns Boolean — zero allocation

// 8.11 — flatMap then size
items.flatMap { it.children }.size                     // builds intermediate list
items.sumOf { it.children.size }                       // no allocation

// 8.15 — double mutability
var list = mutableListOf<Int>()
list += 1            // mutation
list = mutableListOf(2, 3)   // reassignment
// Reasoning: was it cleared? Was it modified? Both axes leaked.

// fix
val list = mutableListOf<Int>()        // pick mutation
list += 1
list += listOf(2, 3)
```

---

## 9. Compose Compiler-as-Plugin (NOT UI) Pitfalls

> **Scope note**: Compose UI patterns — state hoisting, `remember` misuse, recomposition pitfalls, Modifier order, stable parameters, `derivedStateOf` — are **out of scope** here. They belong to the [`native` skill](../../native/SKILL.md). This section covers only the **compiler plugin** wiring angle.

| #   | Anti-pattern                                                | Why it bites                                                                                                                                                                                                  | Fix                                                                                                                              | Detekt rule |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| 9.1 | Compose compiler plugin enabled on non-UI module            | Slows compile; some plugin assumptions (Composable stability inference) leak into non-UI code. Build cache churn.                                                                                             | Enable `org.jetbrains.kotlin.plugin.compose` only on modules that need it.                                                       | n/a         |
| 9.2 | Compose compiler version not version-locked to Kotlin       | Pre-1.5.0-compose: Compose compiler was a separate dependency requiring exact-match with Kotlin. Mismatch → cryptic FIR errors.                                                                              | Use the new official `org.jetbrains.kotlin.plugin.compose` Gradle plugin (Kotlin 2.0+) — version is implicitly Kotlin's.         | n/a         |
| 9.3 | `@Composable` on suspending or returning-Flow function      | Compose runtime expects pure rendering; mixing suspension or hot streams in composables creates re-composition storms.                                                                                       | Keep `@Composable` non-suspending; surface state via `collectAsStateWithLifecycle()` in the UI module (see [`native` skill](../../native/SKILL.md)). | n/a (UI)    |
| 9.4 | Compose compiler reports turned off                         | Without `metricsDestination` + `reportsDestination`, you can't see what's marked stable / restartable. Performance regressions invisible.                                                                    | Enable Compose compiler reports in CI.                                                                                            | n/a         |

---

## 10. Smart Cast Pitfalls

| #    | Anti-pattern                                                       | Why it bites                                                                                                                                                                                                  | Fix                                                                                                                  | Detekt rule          |
| ---- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------- |
| 10.1 | Smart cast on `var` property                                       | Even after `if (foo.bar != null)`, the compiler refuses smart cast — `bar` could change between check and use (potentially by another thread or by overridden getter).                                       | Copy to local `val`: `val b = foo.bar ?: return`.                                                                    | `style/CanBeNonNullable` (where applicable) |
| 10.2 | Smart cast on `open val`                                            | Subclass can override the getter to return different values on each call. Compiler refuses smart cast.                                                                                                       | Mark `final val`, or copy to local `val`.                                                                            | n/a                  |
| 10.3 | Smart cast on property from external module                         | Other modules can change behaviour without recompile of the consumer; compiler conservatively refuses.                                                                                                       | Local `val` copy.                                                                                                    | n/a                  |
| 10.4 | Custom getter property smart cast                                   | Custom getter implies side effects; compiler refuses.                                                                                                                                                        | Local `val` copy.                                                                                                    | n/a                  |
| 10.5 | Smart cast after `is` then mutation                                 | `if (x is String) { x = "" }` — after the assignment, the smart cast is lost on the next line (the property reassignment "broke" the narrowing).                                                              | Don't reassign in the smart-cast scope.                                                                              | n/a                  |
| 10.6 | Using `!!` to "force" what a smart cast won't grant                 | The smart cast refusal is **the warning** — `!!` papers over the unsafety, then NPE later.                                                                                                                   | Fix the underlying assignment pattern: local val, or restructure.                                                    | n/a                  |
| 10.7 | Bang-bang on a delegate property                                    | `lateinit` / `by lazy` properties don't always support smart cast either; the delegate may re-resolve on each access.                                                                                        | Cache reads in local `val`.                                                                                          | n/a                  |

```kotlin
// 10.1 — smart cast refused on var
class Holder {
    var name: String? = null
    fun greet() {
        if (name != null) {
            println(name.length)   // ERROR: Smart cast to 'String' is impossible — 'name' is a mutable property
        }
    }
}

// fix
class Holder {
    var name: String? = null
    fun greet() {
        val n = name ?: return
        println(n.length)
    }
}

// 10.2 — smart cast refused on open val
open class Animal {
    open val name: String? = "default"
}
class Cat : Animal() {
    private var counter = 0
    override val name: String?
        get() = if (counter++ % 2 == 0) "Tom" else null    // returns different value per call!
}
fun greet(a: Animal) {
    if (a.name != null) {
        println(a.name.length)    // ERROR: Smart cast impossible — could be overridden with custom getter
    }
}

// fix
fun greet(a: Animal) {
    val n = a.name ?: return
    println(n.length)
}

// 10.3 — smart cast refused on external module property
// Module-A exposes:
//   class External { val data: String? = "x" }
// Module-B consumes:
import com.external.External
fun process(e: External) {
    if (e.data != null) {
        println(e.data.length)   // ERROR — even though `data` is val, smart cast across module boundary disabled
                                  // (Module-A could ship a new version with custom getter)
    }
}
// fix — local val copy
fun process(e: External) {
    val d = e.data ?: return
    println(d.length)
}

// 10.4 — custom getter
class Generator {
    val next: Int
        get() = Random.nextInt()      // every read different — smart cast forbidden
}

// 10.6 — !! to force what smart cast won't
class Form { var name: String? = null }
fun render(f: Form) {
    if (f.name != null) {
        renderName(f.name!!)         // 1.1 anti-pattern in disguise — race-prone
    }
}
// fix — capture
fun render(f: Form) {
    val n = f.name ?: return
    renderName(n)
}
```

### 10.A K2 smart-cast improvements

K2 broadens smart casts where K1 refused. Don't write old workarounds anymore:

```kotlin
// K1: needed explicit cast or local copy. K2: works.
fun describe(any: Any) {
    val isString = any is String
    if (isString) {
        println(any.length)              // K2 smart casts via Boolean local
    }
}

// K2: smart cast through || across common supertype
sealed interface Status
data class Postponed(val until: Long) : Status
data class Declined(val reason: String) : Status
data class Accepted(val at: Long) : Status

fun summarize(s: Status) {
    if (s is Postponed || s is Declined) {
        // K2 smart casts to a common interface if one exists
    }
}

// K2: smart cast on function-type property
class Holder(val provider: (() -> Unit)?) {
    fun fire() {
        if (provider != null) {
            provider()                   // K2 — direct call without provider?.invoke()
        }
    }
}
```

See [`kotlin-language-spec.md` §2.3](./kotlin-language-spec.md#23-smart-casts) for the full 2.0 smart-cast widening list.

---

## 11. Scope Function Pitfalls

| #    | Anti-pattern                                              | Why it bites                                                                                                                                          | Fix                                                                                                       | Detekt rule                  |
| ---- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------- |
| 11.1 | `?.let { it.foo() }` for unconditional dereference        | Allocates a lambda, hides intent. `?.foo()` is shorter.                                                                                               | `obj?.foo()`.                                                                                             | `style/UnnecessaryLet`       |
| 11.2 | Nested scope-fn pyramid `let { apply { also { run { ... } } } }` | Reader must track shifting `it`/`this`. Cognitive cliff.                                                                                              | Flatten with early returns and named vals.                                                                | n/a                          |
| 11.3 | `apply { someBoolean = true }` returning `Unit` to caller  | `apply` returns the receiver; using it as if it returned `Unit` is fine — but the inverse pattern (returning `apply { ... }` from a `Unit` function) reads wrong. | Use `also { }` if you want side-effect + receiver; `run { }` if you want the lambda result.              | `style/UnnecessaryApply`     |
| 11.4 | `also { it.foo() }` where `apply { foo() }` is clearer    | When all calls are on the receiver, `apply` (using `this`) is shorter.                                                                                | `apply { foo() }`.                                                                                        | `style/AlsoCouldBeApply`     |
| 11.5 | `let` for null-check when `if (x != null)` is plain       | `it` adds indirection. For two-branch logic (`?.let { } ?: ...`), explicit `if` is cleaner (and avoids 1.7).                                          | `if (x != null) { } else { }`.                                                                            | n/a                          |
| 11.6 | `with(obj) { ... }` on nullable receiver                  | `with` doesn't safe-call. Crash if you forget.                                                                                                        | `obj?.run { ... }`.                                                                                       | n/a                          |
| 11.7 | Confusing `let`/`also`/`apply`/`run`/`with` choice         | Mixed `this`/`it`, mixed return types → "what does this block return?" guessing.                                                                      | Use the decision matrix below.                                                                            | n/a                          |

### 11.A Scope-function decision matrix

| Function | Receiver inside | Returns        | Use when                                            |
| -------- | --------------- | -------------- | --------------------------------------------------- |
| `let`    | `it`            | lambda result  | Transform / chain on nullable / produce new value   |
| `also`   | `it`            | receiver       | Side effect (log / track) — return same object      |
| `apply`  | `this`          | receiver       | Configure / mutate — return same object             |
| `run`    | `this`          | lambda result  | Compute over receiver — return computed value       |
| `with`   | `this` (arg)    | lambda result  | Like `run` but for non-receiver case (older style)  |

```kotlin
// 11.1 — unnecessary let
user?.let { it.refresh() }      // wasteful
user?.refresh()                  // same effect, no lambda alloc, no `it`

// 11.2 — pyramid
user?.let {
    it.profile?.apply {
        run {
            name = name.uppercase()
        }
    }
}

// fix
val profile = user?.profile ?: return
profile.name = profile.name.uppercase()

// 11.4 — also vs apply
file.also { it.delete() }       // BAD — every reference uses `it.`
file.apply { delete() }          // GOOD — implicit `this`, cleaner

// 11.6 — `with` on nullable
with(nullableUser) {            // BAD — `with` doesn't safe-call
    println(name)                // NPE if nullableUser is null
}

nullableUser?.run {              // GOOD — null-safe
    println(name)
}
```

---

## 12. String Pitfalls

| #    | Anti-pattern                                                | Why it bites                                                                                                                                                              | Fix                                                                                                                          | Detekt rule                            |
| ---- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 12.1 | Multi-line `"""..."""` without `.trimIndent()`              | Leading whitespace preserved → indented source produces indented runtime string (broken SQL, malformed JSON).                                                              | `"""...""".trimIndent()` (or `.trimMargin("|")`).                                                                            | `style/TrimMultilineRawString`         |
| 12.2 | `$secret` interpolation in logs                              | `logger.info("login token=$token")` — secrets in production logs / crash reports.                                                                                          | Mask/redact: `logger.info("login token=${token.take(4)}…")`.                                                                  | n/a (custom rule)                      |
| 12.3 | `String.format("%s %d", x, y)` argument mismatch             | Compile passes; runtime `MissingFormatArgumentException` or `IllegalFormatConversionException`.                                                                            | Use Kotlin interpolation `"$x $y"`; only use `format` for true `%d`/`%f` formatting.                                          | n/a                                    |
| 12.4 | `"...".format()` without explicit `Locale`                   | Default locale: `1.5` formatted as `"1,5"` in fr-FR — breaks JSON serialization, URLs.                                                                                    | `"%.2f".format(Locale.ROOT, 1.5)` or use `String.format(Locale.ROOT, ...)`.                                                  | `potential-bugs/ImplicitDefaultLocale` |
| 12.5 | `Pattern.compile(...)` cargo-cult                            | Kotlin has `Regex` — clearer and supports multi-line / find/replace properly.                                                                                              | Use `Regex` or `"...".toRegex()`.                                                                                            | n/a                                    |
| 12.6 | Escaped string when raw is clearer                           | `"\\d{3}-\\d{4}"` is harder to read than `"""\d{3}-\d{4}"""`.                                                                                                              | Raw triple-quoted string.                                                                                                    | `style/StringShouldBeRawString`        |
| 12.7 | `string.toUpperCase()` / `toLowerCase()` (deprecated)        | Locale-dependent → Turkish-`i` bug. Deprecated since 1.5.                                                                                                                  | `uppercase()` / `lowercase()` (locale-aware default `ROOT`).                                                                  | `potential-bugs/Deprecation`           |
| 12.8 | `string1 == string2` confused with reference equality        | `==` in Kotlin is structural (`equals`); `===` is referential. Comers from Java often write `equals(...)`.                                                                | Use `==` for value, `===` only for identity. Detekt catches `===` on `String`.                                              | `potential-bugs/AvoidReferentialEquality` |
| 12.9 | `nullable?.toString()` producing `"null"` literal             | If the safe-call short-circuits, `?.toString()` is `null`; using `nullable.toString()` (without `?.`) yields literal `"null"`.                                            | `nullable?.toString() ?: "<none>"`.                                                                                          | `potential-bugs/NullableToStringCall`  |

```kotlin
// 12.1
val sql = """
    SELECT *
    FROM users
    WHERE id = ?
""".trimIndent()   // <-- forgotten = SQL parse error on leading spaces

// 12.2 — secret leak
log.info("Login as ${user.email} token=${user.bearerToken}")     // token in production logs
// fix — mask
log.info("Login as ${user.email} token=${user.bearerToken.take(4)}…")

// 12.4 — locale bug
val price = "%.2f".format(1234.56)         // BAD — fr-FR: "1234,56" (broken JSON / URL)
val price = "%.2f".format(Locale.ROOT, 1234.56)  // GOOD — "1234.56" always

// 12.7 — deprecated case conversion
"foo".toUpperCase()    // DEPRECATED — Turkish-i bug: "i".toUpperCase() == "İ" on tr-TR
"foo".uppercase()      // locale-independent default (Locale.ROOT)
"foo".uppercase(Locale.getDefault())    // explicit if locale matters

// 12.8 — referential equality on String
val a: String? = "hi"
val b: String? = "hi"
println(a === b)        // true / false depending on JVM intern — undefined behaviour
println(a == b)         // true (structural)
```

---

## 13. Gradle / KSP Pitfalls

| #    | Anti-pattern                                                          | Why it bites                                                                                                                                                                                                     | Fix                                                                                                                                            |
| ---- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| 13.1 | Still using **KAPT** after KSP migration is available                 | KAPT creates Java stubs for annotation processors — orders of magnitude slower than KSP. Now incompatible with the "built-in Kotlin" plugin (AGP 9+). KSP1 is also retired for Kotlin ≥ 2.3.                     | Migrate to **KSP2** module by module. Many libs (Room, Hilt, Moshi codegen) have first-class KSP support.                                     |
| 13.2 | Compose compiler plugin version drift from Kotlin                     | With the old `androidx.compose.compiler:compiler` artifact, you had to pin **exactly** to Kotlin version (e.g., Kotlin 1.9.22 ↔ Compose Compiler 1.5.10). Mismatch → cryptic FIR error.                          | Use Kotlin 2.0+ official `org.jetbrains.kotlin.plugin.compose` plugin (version implicit from Kotlin).                                          |
| 13.3 | `implementation` vs `api` confusion (everything `api`)                | `api` exposes the dependency to consumers' compile classpath → bigger consumer compile graph → slower incremental builds, and consumers couple tightly to your transitive deps.                                  | `implementation` by default; `api` only when the type appears in your public API.                                                              |
| 13.4 | Missing `libs.versions.toml` version catalog                          | Version strings duplicated across modules — drift, dependabot churn, hard to upgrade a single library.                                                                                                          | One `gradle/libs.versions.toml` with `[versions]`, `[libraries]`, `[bundles]`, `[plugins]`.                                                    |
| 13.5 | `kotlin.code.style=official` missing                                  | Without it, IDE applies its own conventions; PRs flap on indentation/style.                                                                                                                                     | Add to `gradle.properties`.                                                                                                                    |
| 13.6 | JVM target mismatch between modules                                   | Module A `jvmTarget = 11`, Module B `jvmTarget = 17` → cross-module inlines fail at runtime with `UnsupportedClassVersionError`.                                                                                  | Pin one target via `subprojects { kotlin { jvmToolchain(17) } }`.                                                                              |
| 13.7 | `kotlin.parallel.tasks.in.project=true` without isolation             | Parallel module compile is great — but if your build script uses `Project.afterEvaluate` to share state, parallel triggers race.                                                                                | Audit `afterEvaluate`; prefer configuration-cache-friendly patterns.                                                                            |
| 13.8 | Stale `kotlinx-coroutines-debug` in production                        | Adds heavyweight instrumentation; allowed in dev, ships to prod by accident → 10–30% perf hit on coroutine-heavy paths.                                                                                          | Confine to `testImplementation` / `debugImplementation`.                                                                                       |
| 13.9 | KSP processor in `wrong` source set                                   | `ksp(...)` on `androidMain` vs `commonMain` in KMP can silently produce no output; symbols missing at compile.                                                                                                  | Add to the right `ksp(<configuration>)` per target.                                                                                            |

```kotlin
// 13.2 — Compose compiler version mismatch (LEGACY pattern, Kotlin <2.0)
// build.gradle.kts
android {
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.10"   // had to match Kotlin 1.9.22 EXACTLY
    }
}
// Bump Kotlin → 1.9.24 without bumping Compose Compiler → cryptic IR error.

// 13.2 — modern fix (Kotlin 2.0+)
// settings.gradle.kts
plugins {
    id("org.jetbrains.kotlin.plugin.compose") version "2.3.20"
}
// Version of Kotlin Compose Compiler plugin is implicit — same as Kotlin compiler.
```

```toml
# 13.4 — libs.versions.toml
# gradle/libs.versions.toml
[versions]
kotlin = "2.3.20"
coroutines = "1.10.0"

[libraries]
kotlinx-coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }
kotlinx-coroutines-android = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-android", version.ref = "coroutines" }

[plugins]
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
compose-compiler = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
```

---

## 14. K2 Migration Pitfalls

| #    | Anti-pattern                                                         | Why it bites                                                                                                                                                                                              | Fix                                                                                                                       |
| ---- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 14.1 | Custom compiler plugin still on K1 frontend API                       | K2 has a new FIR-based frontend extension API. Plugins using old frontend hooks (resolve, type-check) won't load; build fails with cryptic error.                                                       | Update to plugin versions supporting K2; check authors' release notes. AtomicFU/Serialization/Parcelize updated in 2.x. |
| 14.2 | `kotlin.compilerOptions.languageVersion` ahead of `apiVersion`        | `languageVersion = "2.1"` but `apiVersion = "1.9"` — some 2.1 syntax compiles but resolves to 1.9 stdlib symbols that don't exist → link error at runtime.                                              | Keep both in sync, or upgrade `apiVersion` together.                                                                       |
| 14.3 | Open property without initializer                                     | K1 allowed deferred initialization in `init {}`. K2 forbids — `open val x: Int` with `init { this.x = 1 }` fails.                                                                                       | Initialize at declaration, or move to private backing field with public read-only accessor.                                |
| 14.4 | Synthetic setter on projected type                                    | K1 silently allowed `container.foo = value` where `container: Container<*>`. K2 errors (type-safe).                                                                                                     | Use explicit method or remove projection.                                                                                  |
| 14.5 | Java primitive array nullability now enforced                         | K2 honors Java `int @Nullable []` annotation properly — code that ignored the nullability now fails compile.                                                                                            | Add explicit null check.                                                                                                   |
| 14.6 | Common code calling platform overload                                  | K1 sometimes resolved platform-specific overloads from `commonMain`; K2 enforces strict source-set boundaries → resolution changes silently break behavior.                                              | Audit `commonMain` calls that resolved to platform-specific functions. Add `expect/actual`.                               |
| 14.7 | OldStackOverflow advice still being followed                          | K2 error messages changed names ("inference variable X" → different). Searching for old error text returns advice that no longer applies (e.g., suggesting `lateinit` where K2's smarter smart cast suffices). | Re-search for the new error text; consult the K2 migration guide instead of cached SO threads.                            |
| 14.8 | `@OptIn` not added for experimental K2 features                       | Some 2.x stdlib pieces (`kotlin.uuid.Uuid`, `kotlin.time.Clock`) still require `@OptIn(ExperimentalUuidApi::class)` etc. Forgotten → compile warning becomes error in lint-strict CI.                    | Add the opt-in annotation at module level (`-opt-in` compiler arg) or function level.                                     |
| 14.9 | Falling back to `-language-version 1.9` permanently                   | K2 rollback works but locks the module out of newer language features (data objects, multi-dollar interpolation, smart cast on union).                                                                  | Fix forward; treat rollback as time-boxed.                                                                                 |

```kotlin
// 14.3 — open property without initializer (K1 OK, K2 ERROR)
open class Base {
    open val a: Int                    // K2 ERROR: open val must have initializer
    init { this.a = 1 }                // K2 ERROR: cannot defer initialization
}

// fix — initialize at declaration, or use private backing
open class Base {
    open val a: Int = 1
}
// or
class Base {
    private val _a: Int
    val a: Int get() = _a
    init { _a = 1 }
}

// 14.6 — common code calling platform overload (silent behaviour change)
// commonMain
expect fun foo(x: Any)
fun callCommon() {
    foo(42)        // K1: might resolve to JVM `foo(Int)` overload. K2: strictly resolves to common `foo(Any)`.
}

// jvmMain
actual fun foo(x: Any) = println("any: $x")
fun foo(x: Int) = println("int: $x")       // never called from common code under K2!

// 14.8 — opt-in for experimental APIs
@file:OptIn(ExperimentalUuidApi::class)
import kotlin.uuid.Uuid
fun makeId(): Uuid = Uuid.random()
```

---

## 15. Testing Pitfalls

| #    | Anti-pattern                                                            | Why it bites                                                                                                                                                                                                  | Fix                                                                                                                  | Detekt rule                                       |
| ---- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| 15.1 | `runBlocking { ... }` in a test                                          | Real time → `delay(1000)` actually waits 1s; tests slow; relies on real dispatchers (flakey). Plus: no leak detection.                                                                                       | `runTest { ... }` (kotlinx-coroutines-test). `delay` is auto-skipped via virtual time.                                | `coroutines/CoroutineLaunchedInTestWithoutRunTest`|
| 15.2 | Missing `Dispatchers.setMain(testDispatcher)` setup                     | Production code calling `Dispatchers.Main` inside ViewModel → `IllegalStateException: Module with the Main dispatcher had failed to initialize`.                                                              | `Dispatchers.setMain(StandardTestDispatcher())` in `@Before` (or extension/rule).                                    | n/a                                               |
| 15.3 | Multiple `TestDispatcher` instances, different schedulers                | Each test-dispatcher has its own scheduler unless shared → `advanceTimeBy` only affects one.                                                                                                                 | Pass `testScheduler` from `runTest`'s receiver: `StandardTestDispatcher(testScheduler)`.                              | n/a                                               |
| 15.4 | Hot `Flow.collect` leaking past test                                    | Collecting from a hot `StateFlow` inside `runTest` without a `Job` → coroutine outlives the test, asserts pass but coroutine still running → 60s timeout or interference with next test.                     | Collect in a child `launch`; cancel at test end. Or use `Flow.test { }` (Turbine).                                    | n/a                                               |
| 15.5 | MockK `relaxed = true` for everything                                    | All unstubbed methods return defaults — wrong stub or missing stub silently passes; bug hidden.                                                                                                              | Use `relaxed = true` sparingly; prefer explicit `every { } returns ...`. Use `relaxUnitFun = true` if only Unit methods need relaxing. | n/a                                               |
| 15.6 | Parallel tests sharing MockK static state                                | `clearAllMocks()` in `@AfterAll` is **not thread-safe**. JUnit 5 parallel mode + MockK can flake with `MockKException: every/verify run twice`.                                                              | Add `MockKExtension.RequireParallelTesting` annotation, or disable parallel for that class.                          | n/a                                               |
| 15.7 | `assertEquals(expectedList, actualSet)`                                  | List vs Set: different ordering semantics → false negative or false positive.                                                                                                                                | Convert: `assertEquals(expected.toSet(), actual)` or use `containsExactlyInAnyOrder`.                                | n/a                                               |
| 15.8 | Test order dependency (static singleton state)                           | One test mutates a `companion object` cache; second test reads stale data → flaky.                                                                                                                           | Reset singletons in `@BeforeEach`. Better: avoid singletons / use DI.                                                | n/a                                               |
| 15.9 | `verify { service.foo() }` with no `every` on the same                  | MockK's strict mode requires all calls to be stubbed (default with `mockk<T>()`); `verify` after `relaxed = false` mock can silently fail if a different method was invoked.                                  | Either stub everything or use `verify(exactly = 0)` for "this method was NOT called".                                | n/a                                               |
| 15.10 | `@Test fun foo(): Job = scope.launch { ... }`                          | Returns a `Job`, test framework treats return as result; coroutine actually runs **after** the test method returns → no assertion. Common when migrating from `runBlocking`.                                  | Return `Unit`; use `runTest`.                                                                                         | n/a                                               |

```kotlin
// 15.1 — bad
@Test
fun loadsData() = runBlocking {
    delay(1000)   // takes 1 real second
    val data = viewModel.load()
    assertEquals(...)
}

// fix
@Test
fun loadsData() = runTest {       // virtual time
    delay(1000)                    // 0 ms wall-clock
    val data = viewModel.load()
    assertEquals(...)
}

// 15.4 — leak
@Test
fun stateUpdates() = runTest {
    viewModel.uiState.onEach { ... }.launchIn(this)   // collects forever; test waits 60s
}

// fix — Turbine
@Test
fun stateUpdates() = runTest {
    viewModel.uiState.test {
        assertEquals(Idle, awaitItem())
        viewModel.load()
        assertEquals(Loaded(...), awaitItem())
    }
}
```

---

## 16. Multiplatform Pitfalls

| #    | Anti-pattern                                                  | Why it bites                                                                                                                                                                                     | Fix                                                                                                                                  |
| ---- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| 16.1 | `java.time.Instant` in `commonMain`                           | JDK type — not available on Native or JS. Compile fails when adding targets.                                                                                                                     | `kotlinx.datetime.Instant` (or `kotlin.time.Instant` from 2.x stdlib in modern projects).                                            |
| 16.2 | `java.util.UUID` in `commonMain`                              | Same reason — JDK-only.                                                                                                                                                                          | `kotlin.uuid.Uuid` (`@OptIn(ExperimentalUuidApi::class)`).                                                                            |
| 16.3 | Subtle `expect` / `actual` signature mismatch                 | `expect fun foo(x: Int): String` vs `actual fun foo(x: Int): String?` (return null introduced on Android only). K1 sometimes compiled; K2 strict — but even when compiling, runtime contract diverges. | Generate the `actual` skeleton from `expect` via IDE; CI check that signatures match exactly. K2 enforces visibility rules — actual may be more permissive. |
| 16.4 | Library in `commonMain` that has only JVM artifact            | Compile succeeds for JVM target; Native/JS targets fail with "no such artifact". Spotted very late.                                                                                              | Always check artifact coordinates: prefer `kotlinx-*` or libraries marked KMP-compatible (`...-multiplatform`).                       |
| 16.5 | Worker-init-in-companion (Native, historical)                 | Pre-Kotlin/Native New Memory Model (1.7.20), top-level / companion mutable state was frozen — assignment crashed at runtime. Code from old tutorials still circulates.                          | Adopt the new memory model (default since 1.7.20); remove `@SharedImmutable` / `freeze()` calls.                                      |
| 16.6 | JS interop wrapping cost                                      | Calling JS from Kotlin/JS via `external` declarations triggers wrapping; in hot paths, allocations dominate.                                                                                     | Batch JS calls; cache wrappers; use raw `dynamic` for performance-critical paths.                                                     |
| 16.7 | `expect class` with abstract method without `expect override` | K2 strict: an `expect class` that extends an abstract base must declare `expect override fun ...()` for inherited abstracts.                                                                     | Add `expect override`.                                                                                                                |
| 16.8 | Coroutines version mismatch across modules                    | `kotlinx-coroutines-core` and `kotlinx-coroutines-android` at different versions → `IncompatibleClassChangeError` at runtime.                                                                    | Use a version catalog and one version reference for all coroutines artifacts.                                                         |
| 16.9 | `internal` actual exposed publicly via `actual typealias`     | `expect internal class Foo` + `actual typealias Foo = PublicClass` → leaks intentional encapsulation.                                                                                            | Match visibility; or wrap.                                                                                                            |

```kotlin
// 16.1 — JDK type in common
// commonMain — BAD
import java.time.Instant       // unresolved on Native / JS targets!
data class Event(val at: Instant)

// fix
import kotlinx.datetime.Instant
data class Event(val at: Instant)

// 16.3 — expect/actual signature drift
// commonMain
expect fun parse(input: String): User

// androidMain — drift! return type is nullable
actual fun parse(input: String): User? = ...   // CONTRACT VIOLATION
// (K1 sometimes accepted; K2 catches more cases, but custom builds can still drift)

// 16.7 — K2 strict expect with abstract base
abstract class FileSystem { abstract fun listFiles() }
expect open class PlatformFs() : FileSystem {
    expect override fun listFiles()        // K2 requires explicit `expect override`
}
```

---

## 17. API Design Pitfalls

| #    | Anti-pattern                                                                  | Why it bites                                                                                                                                                                              | Fix                                                                                                                                |
| ---- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 17.1 | Default-arg functions exposed to Java without `@JvmOverloads`                  | Java callers can't omit args; library "looks like" it has multiple overloads in Kotlin but only one in Java.                                                                            | `@JvmOverloads`.                                                                                                                   |
| 17.2 | Functions overloaded only by inline-class param                                | `fun foo(x: UserId)` and `fun foo(x: SessionId)` — on JVM both compile to `foo(Ljava/lang/String;)`. Clash.                                                                              | `@JvmName("fooUser")` / `@JvmName("fooSession")`.                                                                                  |
| 17.3 | `sealed class` evolution across module boundary without policy                 | Adding a variant breaks downstream `when` exhaustiveness — binary-breaking change.                                                                                                       | Either freeze the hierarchy, document a `else -> handleUnknown(...)` policy, or use `abstract class`.                              |
| 17.4 | Missing `@Deprecated` with `ReplaceWith`                                       | Caller has to read changelog to find the new API.                                                                                                                                       | `@Deprecated("...", ReplaceWith("newFn()"))` provides a one-click migration in IDE.                                                |
| 17.5 | Public top-level functions polluting auto-import                               | `fun render(node: Node)` at the package root — every consumer accidentally imports it as their `render`.                                                                                | Scope into an `object Renderer { fun render(...) }` or extension function on a domain receiver.                                    |
| 17.6 | Returning a concrete `ArrayList` / `LinkedHashMap`                             | Consumer becomes coupled to the implementation; downcasting to `MutableList` becomes legal even if you intended immutability.                                                            | Return `List<T>` (immutable view) and copy: `return result.toList()`.                                                              |
| 17.7 | Functions with 4+ positional parameters                                        | Call sites unreadable; nullable/default args fragile.                                                                                                                                   | Use a `data class Params(...)` or named args + `@JvmOverloads`.                                                                    |
| 17.8 | Functions named identically across DSL receiver scopes                          | Inside nested receiver scopes, the inner overrides the outer silently. Hard to debug.                                                                                                   | Use `@DslMarker` on the DSL annotation; prevents inner scopes from accessing outer's same-named functions.                         |
| 17.9 | Exposing `Flow<*>` mutability via `MutableSharedFlow`                          | Caller can `emit(...)` — encapsulation broken.                                                                                                                                          | Expose `SharedFlow<T>`; keep `MutableSharedFlow<T>` `private`.                                                                     |
| 17.10 | Returning `Flow<Result<T>>` everywhere                                        | Double error-channel (`Result` vs flow's error termination). Confusing collectors.                                                                                                      | Either `Flow<T>` + `catch { }` for errors, OR `Flow<Result<T>>` for streaming successes (e.g., paging). Don't mix.                |
| 17.11 | Public extension function on a third-party type                               | If the third-party library later adds a member with the same signature, the **member wins** (extension is shadowed) → callers silently get different behaviour.                          | Confine extensions to types you control, or namespace under an `object`/file with explicit imports.                                |
| 17.12 | `companion object` named factory (`Companion.invoke`) instead of constructor   | Hides constructor visibility behind `operator fun invoke`. Confusing to API consumers.                                                                                                  | Prefer real `constructor` with `@JvmStatic`-friendly factory in companion if needed.                                              |
| 17.13 | `@OptIn` on every callsite instead of file/module                              | Boilerplate, easy to forget. New consumer in the same file does opt-in by accident.                                                                                                     | `@file:OptIn(...)` once per file, or `-opt-in=...` compiler flag for module-wide ack.                                              |

```kotlin
// 17.4 — Deprecated with ReplaceWith — gives IDE one-click fix
@Deprecated(
    message = "Use loadUsers() (suspending) instead",
    replaceWith = ReplaceWith("loadUsers()"),
    level = DeprecationLevel.WARNING,        // ERROR after a release
)
fun fetchUsers(): List<User> = runBlocking { loadUsers() }

// 17.6 — leaking ArrayList
fun loadAll(): ArrayList<User> = ...        // BAD — consumer relies on Mutable

// fix
fun loadAll(): List<User> = ...             // returns the immutable interface

// 17.7 — too many positional params
fun renderBanner(title: String, subtitle: String, cta: String, color: Int, dismissible: Boolean, autoHide: Long)
// call site:
renderBanner("Welcome", "back", "OK", 0xFFEEEEEE.toInt(), true, 5000L)   // unreadable

// fix — data class
data class BannerSpec(
    val title: String,
    val subtitle: String = "",
    val cta: String? = null,
    val color: Int = 0xFFEEEEEE.toInt(),
    val dismissible: Boolean = true,
    val autoHide: Long? = null,
)
fun renderBanner(spec: BannerSpec)

// 17.8 — DslMarker prevents accidental outer-scope leak
@DslMarker
annotation class HtmlDsl

@HtmlDsl class Html { fun head(block: Head.() -> Unit) {} }
@HtmlDsl class Head { fun title(block: () -> String) {} }

fun page() = Html().apply {
    head {
        title { "Hello" }
        // head { ... }      // ERROR — outer Html.head is inaccessible from Head receiver
    }
}

// 17.9 — mutable shared flow leaked
class Events {
    val stream = MutableSharedFlow<Event>(replay = 0, extraBufferCapacity = 64)  // exposed!
}

// fix
class Events {
    private val _stream = MutableSharedFlow<Event>(replay = 0, extraBufferCapacity = 64)
    val stream: SharedFlow<Event> = _stream.asSharedFlow()
    fun publish(e: Event) { _stream.tryEmit(e) }
}

// 17.11 — extension shadowed by future member
// Library v1
class External(val name: String)
// My code adds extension:
fun External.greet() = "hi, $name"
external.greet()             // calls my extension — works

// Library v2 adds:
class External(val name: String) { fun greet() = "official hi" }
// My code still compiles BUT external.greet() now calls the MEMBER, not the extension.
// Silent behaviour change.
```

---

## Appendix A — Detekt / Ktlint Rule Quick-Lookup Index

Rules referenced above, grouped by ruleset:

### `potential-bugs`

`AvoidReferentialEquality`, `CastNullableToNonNullableType`, `CastToNullableType`, `Deprecation`, `DontDowncastCollectionTypes`, `DoubleMutabilityForCollection`, `EqualsAlwaysReturnsTrueOrFalse`, `EqualsWithHashCodeExist`, `HasPlatformType`, `IgnoredReturnValue`, `ImplicitDefaultLocale`, `LateinitUsage`, `MapGetWithNotNullAssertionOperator`, `MissingPackageDeclaration`, `MissingSuperCall`, `MissingUseCall`, `NullCheckOnMutableProperty`, `NullableToStringCall`, `UnnecessaryNotNullCheck`, `UnnecessaryNotNullOperator`, `UnnecessarySafeCall`, `UnsafeCallOnNullableType`, `UnsafeCast`, `WrongEqualsTypeParameter`

### `coroutines`

`CoroutineLaunchedInTestWithoutRunTest`, `GlobalCoroutineUsage`, `InjectDispatcher`, `RedundantSuspendModifier`, `SleepInsteadOfDelay`, `SuspendFunInFinallySection`, `SuspendFunSwallowedCancellation`, `SuspendFunWithCoroutineScopeReceiver`, `SuspendFunWithFlowReturnType`

### `performance`

`ArrayPrimitive`, `CouldBeSequence`, `ForEachOnRange`, `SpreadOperator`, `UnnecessaryInitOnArray`, `UnnecessaryPartOfBinaryExpression`, `UnnecessaryTemporaryInstantiation`, `UnnecessaryTypeCasting`

### `style` (selection)

`AbstractClassCanBeConcreteClass`, `AbstractClassCanBeInterface`, `AlsoCouldBeApply`, `CanBeNonNullable`, `DataClassContainsFunctions`, `DataClassShouldBeImmutable`, `MagicNumber`, `MayBeConstant`, `ObjectLiteralToLambda`, `ProtectedMemberInFinalClass`, `SafeCast`, `StringShouldBeRawString`, `TrimMultilineRawString`, `UnnecessaryAny`, `UnnecessaryApply`, `UnnecessaryInheritance`, `UnnecessaryInnerClass`, `UnnecessaryLet`, `UseAnyOrNoneInsteadOfFind`, `UseCheckNotNull`, `UseCheckOrError`, `UseRequire`, `UseRequireNotNull`, `UseSumOfInsteadOfFlatMapSize`, `UselessCallOnNotNull`, `VarCouldBeVal`, `WildcardImport`

### Ktlint (selection)

`ktlint_standard_no-wildcard-imports`, `ktlint_standard_import-ordering`, `ktlint_standard_no-unused-imports`, `ktlint_standard_trailing-comma-on-call-site`, `ktlint_standard_trailing-comma-on-declaration-site`, `ktlint_standard_max-line-length`

### IntelliJ inspections (2026)

`RunBlockingInSuspendFunction`, `JobAsCoroutineStarterArgument`, `UnusedDeferred`, `MissingAwaitAll`, `CoroutineContextProperty`, `SuspendCancellableCoroutine`, `SuspiciousImplicitCoroutineScopeReceiver`

---

## Sources

### Coroutines / Flow

- [Kotlin docs — Coroutine exceptions handling](https://kotlinlang.org/docs/exception-handling.html)
- [Kotlin docs — StateFlow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-state-flow/)
- [Kotlin docs — SharedFlow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-shared-flow/)
- [Kotlin docs — GlobalScope (Delicate API)](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-global-scope/)
- [Android Developers — Best practices for coroutines](https://developer.android.com/kotlin/coroutines/coroutines-best-practices)
- [Android Developers — Testing Kotlin coroutines](https://developer.android.com/kotlin/coroutines/test)
- [Android Developers — StateFlow and SharedFlow](https://developer.android.com/kotlin/flow/stateflow-and-sharedflow)
- [Roman Elizarov — Structured concurrency](https://elizarov.medium.com/structured-concurrency-722d765aa952)
- [Manuel Vivo — A safer way to collect flows](https://manuelvivo.dev/coroutines-addrepeatingjob)
- [Manuel Vivo — repeatOnLifecycle API design story](https://manuelvivo.dev/repeatonlifecycle)
- [JetBrains — New IntelliJ Kotlin coroutine inspections (2026)](https://blog.jetbrains.com/idea/2026/03/intellij-idea-s-new-kotlin-coroutine-inspections-explained/)
- [kt.academy — Exception handling in Kotlin Coroutines](https://kt.academy/article/cc-exception-handling)
- [kt.academy — Kotlin Coroutines dispatchers](https://kt.academy/article/cc-dispatchers)
- [kt.academy — Testing Kotlin Coroutines](https://kt.academy/article/cc-testing)
- [kt.academy — SharedFlow and StateFlow](https://kt.academy/article/cc-sharedflow-stateflow)

### Detekt / Ktlint

- [Detekt — potential-bugs ruleset](https://detekt.dev/docs/rules/potential-bugs/)
- [Detekt — coroutines ruleset](https://detekt.dev/docs/rules/coroutines/)
- [Detekt — style ruleset](https://detekt.dev/docs/rules/style/)
- [Detekt — performance ruleset](https://detekt.dev/docs/rules/performance/)
- [Ktlint](https://pinterest.github.io/ktlint/)
- [Android Kotlin style guide](https://developer.android.com/kotlin/style-guide)

### Null safety / Smart cast

- [Kotlin docs — Null safety](https://kotlinlang.org/docs/null-safety.html)
- [Kotlin Discussions — Smart cast impossible across modules](https://discuss.kotlinlang.org/t/what-is-the-reason-behind-smart-cast-being-impossible-to-perform-when-referenced-class-is-in-another-module/2201)
- [Baeldung — Preconditions with Kotlin (requireNotNull / checkNotNull)](https://www.baeldung.com/kotlin/preconditions)

### Type / generics / value classes / inline

- [Kotlin docs — Inline functions](https://kotlinlang.org/docs/inline-functions.html)
- [Kotlin docs — Inline value classes](https://kotlinlang.org/docs/inline-classes.html)
- [Kotlin docs — Generics: in, out, where](https://kotlinlang.org/docs/generics.html)
- [Baeldung — Difference Between crossinline and noinline](https://www.baeldung.com/kotlin/crossinline-vs-noinline)
- [Dave Leeds — Inline Classes and Autoboxing](https://typealias.com/guides/inline-classes-and-autoboxing/)

### Class hierarchy / sealed / data classes

- [Kotlin docs — Sealed classes and interfaces](https://kotlinlang.org/docs/sealed-classes.html)
- [Kotlin docs — Inheritance](https://kotlinlang.org/docs/inheritance.html)
- [Kotlin docs — Data classes](https://kotlinlang.org/docs/data-classes.html)
- [kt.academy — Effective Kotlin: sealed classes](https://kt.academy/article/ek-sealed-classes)
- [kt.academy — Effective Kotlin: prefer composition over inheritance](https://kt.academy/article/ek-composition)
- [kt.academy — Effective Kotlin: limit mutability](https://kt.academy/article/ek-mutability)
- [kt.academy — Effective Kotlin: respect hashCode contract](https://kt.academy/article/ek-hashcode)

### Companion / property delegation / scope functions

- [Kotlin docs — Delegated properties](https://kotlinlang.org/docs/delegated-properties.html)
- [Kotlin docs — Scope functions](https://kotlinlang.org/docs/scope-functions.html)
- [Kotlin docs — LazyThreadSafetyMode](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-lazy-thread-safety-mode/)
- [Baeldung — Best Practices for Using Constants in Kotlin](https://www.baeldung.com/kotlin/constants-best-practices)

### Java interop

- [Kotlin docs — Calling Kotlin from Java](https://kotlinlang.org/docs/java-to-kotlin-interop.html)
- [Android Developers — Kotlin-Java interop guide](https://developer.android.com/kotlin/interop)

### Collections / Sequences / Performance

- [Kotlin docs — Sequences](https://kotlinlang.org/docs/sequences.html)
- [Kotlin docs — Arrays](https://kotlinlang.org/docs/arrays.html)
- [Chris Banes — Should you use Kotlin Sequences for Performance?](https://chrisbanes.me/posts/use-sequence/)
- [kt.academy — Effective Kotlin: prefer sequences for big collections](https://kt.academy/article/ek-sequence)
- [Baeldung — IntArray vs Array<Int>](https://www.baeldung.com/kotlin/intarray-vs-arrayint)
- [Detekt issue #1245 — Prefer IntArray over Array<Int>](https://github.com/detekt/detekt/issues/1245)

### Strings

- [Kotlin docs — Strings](https://kotlinlang.org/docs/strings.html)
- [Kotlin docs — Strings in Java and Kotlin](https://kotlinlang.org/docs/java-to-kotlin-idioms-strings.html)

### Gradle / Compose plugin / Versions

- [Gradle — Version Catalogs](https://docs.gradle.org/current/userguide/version_catalogs.html)
- [Gradle — Best Practices for Dependencies](https://docs.gradle.org/current/userguide/best_practices_dependencies.html)
- [Android Developers — Compose Compiler Gradle plugin](https://developer.android.com/develop/ui/compose/compiler)
- [Android Developers — Migrate from kapt to KSP](https://developer.android.com/build/migrate-to-ksp)
- [Kotlin docs — Migrate from kapt to KSP](https://kotlinlang.org/docs/ksp-kapt-migration.html)

### K2 migration

- [Kotlin docs — K2 compiler migration guide](https://kotlinlang.org/docs/k2-compiler-migration-guide.html)
- [Kotlin docs — What's new in Kotlin 2.1.20](https://kotlinlang.org/docs/whatsnew2120.html)

### Testing

- [Kotlin docs — kotlinx-coroutines-test](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/)
- [Kotlin docs — runTest](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/kotlinx.coroutines.test/run-test.html)
- [MockK](https://mockk.io/)

### Multiplatform

- [Kotlin docs — Expected and actual declarations](https://kotlinlang.org/docs/multiplatform/multiplatform-expect-actual.html)
- [Kotlin docs — KMP compatibility guide](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html)
- [kotlinx-datetime](https://github.com/Kotlin/kotlinx-datetime)
