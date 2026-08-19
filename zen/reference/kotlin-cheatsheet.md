# Kotlin Refactoring Cheatsheet (Kotlin 2.3+ / K2)
Purpose: Zen-flavored slice of the Kotlin knowledge base — code-smell-to-idiom transformations, naming hygiene, scope-function discipline, and refactor anti-patterns. Behavior-preserving only.
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Function Extraction Signals (Kotlin-specific)
1. **A lambda block > 15 lines** — particularly inside `apply`/`also`/`let`/`run` chains. Long lambdas read worse than named functions.
2. **Nested scope-function chains** (`x.let { it.also { it.apply { ... } } }`) — almost always means one of them was unnecessary. Pick one tool per layer.
3. **Three or more repeated `?.let { }` blocks on the same shape** — extract a `private fun` that returns the unwrapped value (or `null`).
4. **`when` arms with shared post-processing** — extract the post-processing as a free function; arms reduce to value construction.
5. **`Flow` chain > 5 operators inline** — break at named intermediate Flows; each named step becomes a `private fun ...: Flow<X>`.
6. **A `class` with one public method** — convert to a top-level extension function or a `fun interface` if multiple impls exist.
- A 3-line block used in one place — inline it.
- A helper that requires `internal` visibility just to be referenced once — keep inline.
- An extracted function that needs 5+ parameters threading through — that means you extracted at the wrong seam.
---
## Naming Hygiene (Kotlin Style Guide)
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
- Avoid `IFoo` / `FooInterface` Java-isms when the repository follows Kotlin naming conventions.
### Property naming
- Read as English assertion for `Boolean`: `view.isVisible`, `string.isBlank()`.
- Avoid double negatives: `isNotEmpty` exists for symmetry but if you can use the positive form, do.
---
## Coroutine / Flow Refactor Signals
- **Suspended block emitting events → Flow**
- **`runBlocking` in production → structured scope**
- **`GlobalScope.launch` → structured scope**
---
## Refactor Anti-Patterns to Avoid
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
