# Kotlin Code-Review Cheatsheet (Judge)
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## 1. Priority checklist — highest signal first
### Tier 1 — Crashes, leaks, concurrency bugs (block merge)
1. **`!!` force-unwrap: justified?**
   - In libraries: replace with `?:` Elvis throw or typed null handling.
   - In app code: acceptable only with an `// INVARIANT: ...` comment proving non-null (e.g., view binding post-`onViewCreated`).
   - Detekt: `UnsafeCallOnNullableType`, `RethrowCaughtException`.
2. **`runBlocking { }` outside `main` / tests**
   - `runBlocking` in an HTTP handler / Android UI lifecycle = DoS surface. Blocks the calling thread (event loop, UI thread) until the body completes.
   - Fix: propagate `suspend` up the stack, or use a dedicated `CoroutineScope.launch { }`.
   - Detekt: `RunBlockingPlugin` (custom; not default).
3. **`GlobalScope.launch { }` — leak**
   - `GlobalScope` is parent-less; the coroutine outlives the calling context. No cancellation propagation.
   - Fix: a scoped `CoroutineScope` (lifecycle-bound on Android, `coroutineScope { }` block in pure code).
   - Detekt: `GlobalCoroutineUsage`.
4. **`StateFlow.value = value.copy()` — race condition**
   - `value =` is atomic; `value.copy()` reads then writes — interleaved updates lose data.
   - Fix: `_state.update { it.copy(...) }` (available since coroutines 1.4).
   - High-frequency mutation hotspot in Compose ViewModels.
5. **`async { ... }.await()` with exception swallow**
   - `async` without `.await()` retains the failure; if the surrounding scope's `Job` is not awaited, the exception goes nowhere.
   - Patterns to flag: `val d = async { fail() }` with no `.await()` later, or `try { d.await() } catch (e) { /* swallow */ }`.
6. **`lateinit var` in long-lived class without enforced init**
   - Access before init throws `UninitializedPropertyAccessException`. Acceptable when the framework guarantees init order (Android Fragment); suspicious otherwise.
   - Audit: `lateinit` properties should have a `init` block or a `@PostConstruct`-style guarantee documented.
   - Fix where possible: constructor inject, `by lazy { ... }`, or nullable + ?.let pattern.
7. **`runCatching { }` over typed Result without rethrow**
   - `runCatching` catches all `Throwable`s including `CancellationException` (cancels coroutine — must rethrow!).
   - Fix: explicit try/catch on the specific exception types you handle; or `runCatching { ... }.onFailure { if (it is CancellationException) throw it }`.
8. **Public mutable `MutableList`/`MutableMap` where `List`/`Map` would do**
   - Exposing the mutable interface lets callers mutate internal state behind your back.
   - Fix: `val items: List<T> get() = _items` with `private val _items: MutableList<T>`.
   - Convention: prefix backing mutable with `_`.
9. **`companion object` with eager-init heavy state**
   - Kotlin `object` / `companion object` is initialized lazily but synchronized via class init lock. Heavy work in `init { ... }` blocks subsequent first-access.
   - Fix: `by lazy { ... }` for individual fields; defer expensive init.
10. **Java interop annotations missing**
    - `@JvmStatic`, `@JvmOverloads`, `@JvmField`, `@JvmName`, `@Throws` — when this code will be called from Java.
    - Missing `@JvmOverloads` on a function with default parameters → Java callers can't use defaults.
    - Missing `@Throws(...)` → Java callers see `Exception` even though the function declares specific throws.
    - Flag only if Java-side callers are confirmed (library target, multi-language module).
### Tier 2 — Public API correctness (block merge for library targets)
11. **`internal` visibility for things actually called by external module**
    - Kotlin `internal` = module-private. If accessed via `@JvmName` from another module, brittle.
12. **`open class` / `open fun` without explicit reason**
    - Kotlin default is `final`. Marking `open` invites extension; often unintentional. Flag for "is this extension point intentional?"
13. **`sealed class` / `sealed interface` without `@Serializable` / `@JsonClassDiscriminator`**
    - Polymorphic serialization needs explicit discriminator. Otherwise round-trip loses the variant.
14. **`Enum` with mutable companion-stored state**
    - Enum instances are singletons; mutating their state mutates global state. Almost always a bug.
15. **`expect` declaration without `actual` for all targets in KMP**
    - K2 compiler is stricter; missing `actual` is a compile error per target. Flag during multi-target review.
### Tier 3 — Design smells (review comment, not block)
16. **`data class` with `var` properties**
    - `data class` is intended for immutable value carriers (good `equals`, `hashCode`, `copy`). Mutable vars break the value semantics (a `Map` keyed by it can corrupt).
    - Sometimes intentional (mutable builder); flag for justification.
17. **`object` used purely as a namespace (no state)**
    - `object Constants { const val FOO = 1 }` is acceptable, but consider `top-level const val` or `package-level` declarations as the more idiomatic form.
18. **`String?` everywhere instead of typed enum**
    - `fun setMode(mode: String)` with valid values "auto" / "manual" / "off" — replace with `enum class Mode`.
19. **`Pair<A, B>` / `Triple<A, B, C>` for non-trivial returns**
    - Use a named `data class` for clarity. `Pair` is fine for trivial cases (map entries) but harms call-site readability.
20. **`when` over Boolean (`when { true -> ... false -> ... }`)**
    - Use `if/else` for binary. `when` is for >2 cases or pattern matching.
---
## 2. Intent-vs-code mismatch signals (Kotlin-specific)
| Mismatch signal | What to ask |
|-----------------|------------|
| Function named `getXxx()` in Kotlin code | Use property syntax (`val xxx`); `get` prefix is Java convention |
| `suspend fun` whose body never actually suspends | Caller incurs continuation cost for nothing; consider non-suspending |
| `Flow<T>` where `suspend fun(): T` would do (no streaming) | Single-value future shouldn't be a Flow |
| `Result<T>` returned but caller `.getOrThrow()`s everywhere | Either the failure is impossible, or callers should `try` instead |
| `runCatching { }` where intent is "convert exception → Result" but caught CancellationException | Coroutine cancellation broken; usually a bug |
| `companion object` with `fun create(...)` but the class has a `public` constructor | Either make constructor `internal` or remove the factory |
| Generic `where` bound `T : Any` but doc says "any value" | `T : Any` excludes nullable — doc and bound disagree |
| `@JvmStatic` on a Kotlin-only API | Annotation cost without Java callers; misleading |
| `lazy { }` in a long-lived singleton holding a leaked Context | Common Android leak pattern |
| `flow { emit(x) }` for a single emission | Should be `flowOf(x)` or just a `suspend fun` |
| `coroutineScope { launch { } }` instead of just `launch { }` | Wrapping `launch` in `coroutineScope` is rarely needed; usually a no-op |
| `withContext(Dispatchers.IO) { ... }` for non-blocking code | Dispatcher hop without justification; perf cost |
---
## 3. Detekt policy
- **3.1 Elevate to error (block merge)**
### 3.2 Keep as warning
- `style.MagicNumber` — many false positives for `0`, `1`, `2`; warn but don't block.
- `style.MaxLineLength` (120) — warn at 120, error at 200 for hard outliers.
- `naming.*` rules — warn; rarely worth blocking on style alone.
- `complexity.LongMethod` — warn; the existence of long methods may be intentional in DSL builders.
### 3.3 Default-allow (false-positive heavy)
- `style.UseDataClass` — sometimes a regular class with custom `equals` is intentional.
- `style.UnnecessaryAbstractClass` — abstract base classes in framework code are intentional even without abstract members.
- `style.MatchingDeclarationName` — files containing multiple top-level functions break this; Kotlin allows it.
- `naming.FunctionNaming` for tests with `fun \`should do something\`()` — backticked test names are idiomatic.
- `complexity.TooManyFunctions` on DSL builder objects — they're supposed to fan out.
### 3.4 Per-target context
- **Library module published to Maven**: elevate `formatting` (ktlint) to error; require KDoc on all `public` items via `documentation.UndocumentedPublicClass` + `UndocumentedPublicFunction`.
- **Android module**: enable `ResourceCleanup`, `LeakingThis`; relax `Indentation` if Android Studio default conflicts with ktlint.
- **Test module**: blanket disable `MagicNumber`, `MaxLineLength`, `TooGenericExceptionCaught` — tests can be loose.
- **KMP common module**: enable `expect-actual` audit; flag platform-specific imports in common.
---
## 4. Kotlin Style Guide audit
| Principle | High-signal violation | Why it matters |
|-----------|----------------------|----------------|
| **Idiomatic null handling** | `if (x != null) x.method() else null` | Should be `x?.method()` |
| **Property syntax over getter/setter** | `fun getName(): String = _name` | `val name: String get() = _name` |
| **Extension functions over utility classes** | `class StringUtils { fun reverse(s: String) }` | `fun String.reverse() = ...` |
| **Type inference for locals** | `val x: Int = 5` | `val x = 5` (inferred); reserve explicit types for public API |
| **Single-expression functions** | `fun double(x: Int): Int { return x * 2 }` | `fun double(x: Int) = x * 2` |
| **Data classes for value types** | `class Point(val x: Int, val y: Int) { override equals... }` | `data class Point(val x: Int, val y: Int)` |
| **Sealed classes for closed hierarchies** | `enum` with discriminator + per-case state | `sealed class` / `sealed interface` |
| **Trailing commas** | (style) | Style guide allows; consistency within file |
| **`when` for multi-branch** | `if/else if/else if/else` chain | `when (x) { is A -> ... is B -> ... }` |
| **Coroutines for async** | Callbacks / RxJava in new code | `suspend fun` / `Flow` |
---
## 5. K2 + 2023→2026 migration smells
| Old pattern | Modern (Kotlin 2.3 + K2) | Source |
|-------------|--------------------------|--------|
| `kapt` annotation processing | KSP2 (`com.google.devtools.ksp`) | KSP2 is the path forward; kapt deprecated |
| Compose compiler version not matching Kotlin | Use `kotlin-compose-compiler-plugin` (Kotlin 2.0+) | Bundled, no version-sync issue |
| `context receivers` (`context(Foo) fun ...`) | `context parameters` (Kotlin 2.0+ preview) or remove | Old context-receiver syntax deprecated |
| `LiveData` in non-Compose code | `StateFlow` / `SharedFlow` | Coroutines-native; lifecycle-aware via `repeatOnLifecycle` |
| `Channel` for state | `StateFlow` / `MutableStateFlow` | Channel is for one-time events; StateFlow for state |
| `Pair<...,...>` overused for ID + label | `data class XxxView(val id: Long, val label: String)` | Readability + KDoc |
| Raw `data class UserId(val id: Long)` for typed IDs | `@JvmInline value class UserId(val id: Long)` | Zero-cost wrapper |
| `LiveData.observe(viewLifecycleOwner) { }` | `lifecycleScope.launch { flow.collect { } }` + `repeatOnLifecycle` | Coroutines-native |
| `kotlinx.coroutines.flow.combine` for non-stream use | Convert to `suspend fun` with parallel `async` | Don't use Flow for single emissions |
| `CoroutineScope(Dispatchers.X)` ad-hoc | Lifecycle-bound scope (lifecycleScope / viewModelScope) | Cancellation discipline |
| `MutableState<T>` exposed publicly in ViewModel | Expose `State<T>` (immutable read view); keep `MutableState` private | Encapsulation |
| `init { runBlocking { ... } }` in non-test init | Refactor to lazy / suspend init | DoS in init |
---
## 7. Common false positives (don't ship these as findings)
| False positive | Why it's NOT a bug |
|---------------|---------------------|
| `data class User(var id: Long, val name: String)` with `var` for builder pattern | Sometimes data classes are deliberately mutable for `copy`-builder flows; flag for justification, don't block |
| `runCatching { }` with cancellation-rethrow comment in body | If `if (e is CancellationException) throw e` is present, it's correct |
| Scope-function chain (`x?.let { }?.run { }?.also { }`) | Sometimes intentional DSL; don't reject without measuring readability |
| `companion object` factory + `public` constructor | Sometimes `public` constructor exists for tests; factory for prod |
| `UnsafeCallOnNullableType` on `binding!!` in Android Fragment after `onViewCreated` | Standard pattern; binding is guaranteed non-null at that lifecycle |
| `MagicNumber` flagging `0`, `1`, `-1`, `2` | Almost always intentional; default-disable these |
| `UseDataClass` on a class with non-`val` constructor params used only as builder | Builder pattern intentionally uses non-data class |
| Detekt `TooGenericExceptionCaught` on `catch (e: Exception)` in a top-level error boundary | Top-level boundaries should catch broadly to prevent crashes |
| `MaxLineLength` violations on URLs / paths in string literals | Can't be wrapped without breaking the URL; suppress at the line |
| `ReturnFromFinally` warning for cleanup that swallows exceptions intentionally | Sometimes desired (lock release should not throw); flag for review |
| `RedundantSuspendModifier` on a public API method that *will* suspend in some impl | Future-proofing public API; intentional |
| `MatchingDeclarationName` on a file with several related top-level functions (`Conversions.kt`) | Kotlin's strength — top-level fn collections |
| `UnusedPrivateMember` on `private val` used by reflection (e.g., `kotlinx.serialization`) | Compiler can't see reflective use |
---
## 9. Judge-specific routing rules for Kotlin
1. **No finding without a citation.** Every finding must reference a detekt rule, ktlint rule, Style Guide section, KEEP, or anti-pattern row. "Looks wrong" gets dropped.
2. **Tier 1 findings block merge.** `!!` without justification, `runBlocking` outside main/tests, `GlobalScope.launch`, StateFlow race, swallowed CancellationException — not "style". Highest severity.
3. **Library vs app distinction.** `!!` in app `Activity.onCreate` with framework guarantee is acceptable; in a library `lib.kt` it's Tier 2.
4. **JDK target matters.** Project on JDK 21 → virtual-threads / pattern matching available; on JDK 17 → flag forward-looking-only patterns.
5. **Multi-engine cross-check on coroutines.** Suspension / cancellation / Flow correctness is subtle enough that running both Claude and Codex pays off.
6. **False-positive filter (§7) runs before publishing.** Don't burn reviewer trust on noise.
7. **Suggest, don't dictate, on style.** "Consider `StateFlow` over `Channel` for state" not "must change". Save imperative tone for Tier 1 + Tier 2.
8. **Defer Compose UI / Material 3 design questions** to native skill; Judge keeps the data-race / lifecycle layer.
9. **K2 vs K1.** Verify `kotlin.experimental.tryK2=true` is absent and Kotlin version ≥ 2.0 (K2 is default). If on K1, flag migration smells as Tier 3.
---
## Sources
- Kotlin Style Guide — https://kotlinlang.org/docs/coding-conventions.html
- detekt rules reference — https://detekt.dev/docs/rules/overview/
- ktlint rules — https://pinterest.github.io/ktlint/latest/rules/standard/
- Kotlin Coroutines Guide — https://kotlinlang.org/docs/coroutines-guide.html
- Kotlin Improvement Proposals (KEEPs) — https://github.com/Kotlin/KEEP
- KSP — https://kotlinlang.org/docs/ksp-overview.html
- Kotlin 2.0 / K2 migration — https://kotlinlang.org/docs/k2-compiler-migration-guide.html
- Compose compiler stability — https://developer.android.com/jetpack/compose/performance/stability
- Apply the [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding) to version-sensitive findings.
