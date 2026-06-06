# Kotlin Architecture Cheatsheet (Kotlin 2.3+ / K2)

Purpose: Atlas-flavored slice of the Kotlin knowledge base — Gradle multi-module architecture patterns, interface-based DI, visibility hygiene, circular-dep detection, public-API surface management, and ADR triggers specific to Kotlin.

Baseline: **Kotlin 2.3+, K2 compiler, KSP2 default, Gradle 8.x with version catalogs**.

Source of truth (do not duplicate here):
- Project structure & Gradle → [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) §5
- Architecture patterns (Clean / MVI / repository) → [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) §11
- API design pitfalls → [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md) §17
- Class hierarchy pitfalls → [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md) §4

---

## Contents

- [Gradle Multi-Module Architecture Patterns](#gradle-multi-module-architecture-patterns)
- [Interface-Based DI: Hilt / Koin / kotlin-inject](#interface-based-di-hilt--koin--kotlin-inject)
- [Module Visibility Hygiene](#module-visibility-hygiene)
- [Circular Dependency Detection](#circular-dependency-detection)
- [God-Module Split Signals](#god-module-split-signals)
- [Version Catalogs and Convention Plugins](#version-catalogs-and-convention-plugins)
- [Public API Surface Management](#public-api-surface-management)
- [Refactoring Playbooks](#refactoring-playbooks)
- [ADR Triggers Specific to Kotlin](#adr-triggers-specific-to-kotlin)
- [Architecture Anti-Patterns](#architecture-anti-patterns)

---

## Gradle Multi-Module Architecture Patterns

Three production patterns. Pick one per system; mixing causes layering chaos.

### Layered (Clean / Hexagonal)

Modules organized by architectural layer; dependencies flow one direction only.

```
my-app/
├── settings.gradle.kts
├── build.gradle.kts
├── gradle/
│   └── libs.versions.toml         # version catalog
├── build-logic/                   # convention plugins
├── domain/                        # Pure types + interfaces, no Android/JVM I/O
├── application/                   # Use-cases composing domain + ports
├── adapter-jpa/                   # Implements domain interfaces via Hibernate/JPA
├── adapter-http/                  # Ktor/Spring routes -> Application
└── app/                           # Thin entry: wires adapters into application
```

Dependency rule (enforced at Gradle level):

```
app ──> adapter-http ──> application ──> domain
        adapter-jpa ──> application ──> domain
```

`domain` depends on **nothing inside the project**. Verify with `./gradlew :domain:dependencies --configuration implementation`.

### Feature-Sliced (Bounded Contexts)

Top-level modules per bounded context; each module may itself follow hex/clean internally.

```
modules/
├── billing/         # has Domain/Application/Adapter packages inside
├── catalog/
├── identity/
└── shared-kernel/   # cross-context primitives (Money, UserId)
```

Cross-context dependencies go via `shared-kernel` only. No `billing → catalog` direct edges.

### Kotlin Multiplatform (KMP) Source Set Hierarchy

```
shared/
├── src/
│   ├── commonMain/kotlin/        # Pure logic, runs everywhere
│   ├── commonTest/kotlin/
│   ├── jvmMain/kotlin/           # JVM-only paths
│   ├── androidMain/kotlin/       # Android-specific
│   ├── iosMain/kotlin/           # iOS via K/N
│   ├── iosX64Main/, iosArm64Main/, iosSimulatorArm64Main/
│   └── jsMain/kotlin/
```

Use the default hierarchy template (Kotlin 1.9.20+) — declares the source-set graph automatically. Avoid manual `dependsOn` wiring.

### Single Module + Subpackages

Smallest pattern. One `:app` module with package-based separation.

```
src/main/kotlin/com/acme/
├── domain/
├── application/
├── adapter/
└── App.kt
```

Use when:
- Project is one bounded context.
- ≤ ~10k LOC; growth past that should trigger a Gradle split.

---

## Interface-Based DI: Hilt / Koin / kotlin-inject

Three production DI choices. Pick deliberately.

### Hilt (Android-only, Dagger-based)

`@Module` + `@InstallIn` + `@Provides` / `@Binds`; constructor-injected `@HiltViewModel`. Compile-time generated (KSP2 since Hilt 2.48). Zero runtime DI reflection cost. **Cost**: Android-only; tightly coupled to `Application`/`Activity`/`ViewModel`. **Use when**: Android-only app, team familiar with Dagger/Hilt.

### Koin (KMP-friendly, runtime DSL)

`module { single<T> { ... }; viewModel { ... } }` + `startKoin { modules(appModule) }`. Runtime DSL — no annotation processing. KMP-friendly (Android, JVM, Native, JS). **Cost**: runtime resolution (slower first-call); errors surface at runtime, not compile time. **Use when**: KMP, server-side Kotlin, or teams allergic to Dagger ceremony.

### kotlin-inject (KSP2, KMP-friendly)

`@Component abstract class` with `@Provides` methods; KSP2 generates the wiring. Compile-time safe and KMP-friendly. **Cost**: smaller community than Hilt/Koin; Android integration is partly hand-rolled. **Use when**: KMP + compile-time safety + post-Dagger fatigue.

### Decision matrix

| Scenario | Choose |
|----------|--------|
| Android-only app, large team | Hilt |
| KMP, mixed Android + iOS + server | Koin or kotlin-inject |
| KMP + compile-time safety mandatory | kotlin-inject |
| Server-side Kotlin (Ktor/Spring) | Spring DI (Spring) / Koin (Ktor) |
| Library exposes DI integration | Provide neither — accept constructor params |

See best-practices §11 (Architecture patterns) for the full DI comparison.

---

## Module Visibility Hygiene

Kotlin's four-rung visibility ladder. Use the tightest that compiles.

| Modifier | Reachable from |
|----------|----------------|
| `private` (top-level) | Same file |
| `private` (class member) | Same class |
| `protected` (class member) | Class + subclasses (no top-level form) |
| `internal` | Same Gradle module |
| `public` (default) | Everywhere |

Kotlin has **no `package-private`** like Java. `internal` replaces it at the Gradle-module level — not the package level.

### `internal` is the underused middle ground

```kotlin
// Before — leaking implementation detail via `public` to share within a module
public class OrderInternals { /* used in adapter and application packages, not by app */ }

// After
internal class OrderInternals { /* only visible inside this Gradle module */ }
```

`internal` is the right level for "cross-package within one Gradle module." Reach for `public` only when you publish artifacts.

### Sealed interfaces (prevent downstream impls)

```kotlin
sealed interface Renderer {
    fun render(doc: Doc): Output
}

class SvgRenderer : Renderer { /* same module only */ }
class PngRenderer : Renderer { /* same module only */ }
```

Use when:
- You want forward-compat freedom to add methods (no breaking-change risk from downstream impls).
- The interface represents a closed enumeration of behaviors.

Sealed interfaces also enable exhaustive `when`:

```kotlin
fun describe(r: Renderer): String = when (r) {
    is SvgRenderer -> "vector"
    is PngRenderer -> "raster"
    // compiler enforces all branches
}
```

### Explicit-API mode for libraries

```kotlin
// build.gradle.kts (library module)
kotlin {
    explicitApi()    // requires explicit visibility + return types on public API
}
```

Catches accidentally-public symbols at compile time. Always enable for published libraries.

---

## Circular Dependency Detection

Gradle does not allow circular module dependencies at configuration time, but circular intra-module dependencies (Class A → Class B → Class A) AND logical circularity (interface in module X, impl in Y, Y calls X) can still emerge.

### Tools

| Tool | Scope | Use For |
|------|-------|---------|
| `./gradlew :module:dependencies` | Per-module direct + transitive | Inspect what a module actually pulls in |
| `./gradlew projectDependencyGraph` | Workspace-level module graph | Visualize module-to-module edges |
| IntelliJ "Dependency Structure Matrix" | Per-module class-level coupling | Find unintended class-level cycles |
| Konsist | Test-style architecture rules | Enforce "no class in domain may depend on infra" rules in CI |
| `gradle-dependency-analysis-plugin buildHealth` | Misplaced configurations | Detect `implementation` that should be `api` |
| Detekt `Indentation` + `LongMethod` proxy | Coupling smells | Indirect signal |

Example:

```bash
./gradlew :app:dependencies --configuration implementation
./gradlew projectDependencyGraph    # if Project Health Plugin installed
```

Konsist example:

```kotlin
// src/test/kotlin/architecture/LayeringTest.kt
class LayeringTest {
    @Test
    fun `domain does not depend on adapter`() {
        Konsist.scopeFromModule("domain")
            .files
            .assertFalse { it.hasImport { import -> import.name.startsWith("com.acme.adapter") } }
    }
}
```

### Common circular smells in Kotlin

1. **App → Infra → App via callback registration.** The Infra layer calls back into Application services through a registered lambda. Fix: invert via an interface owned by `application`; `infra` implements it.

2. **Module A re-exports types from Module B, while Module B uses interfaces defined in Module A.** Compiles but creates an "if you import either, you import both" coupling. Fix: move the shared types into a `shared-kernel` / `common` module.

3. **Package cycle inside a module**: `package a` uses items from `package b` which uses items from `package a`. Kotlin allows it but muddies reasoning. Fix: extract shared items into a parent or sibling package.

4. **Test code reaching into prod code via `internal` shortcuts that grow into a backdoor.** Fix: keep a clean test-only API; use `@VisibleForTesting` annotation if necessary.

---

## God-Module Split Signals

When a single module becomes a kitchen sink, productivity collapses. Signals worth a split:

- **Compile time > 30s** for a clean incremental rebuild of one module.
- **`dependencies { }` block has > 15 entries** suggesting bundled concerns.
- **`:app` module contains domain + adapter + UI code** — Android template default that ages badly.
- **`commonMain` (KMP) > 100 source files** — split into feature sub-modules per bounded context.
- **A single file > 2000 LOC** without natural sub-files.
- **PRs from different teams routinely touch the same module** — change ownership is unclear.
- **Gradle build report shows one module as 80% of build time** — split required.
- **Module exposes classes from 3+ unrelated bounded contexts** as `public` API.

Splitting playbook → see [Refactoring Playbooks](#refactoring-playbooks).

---

## Version Catalogs and Convention Plugins

### Version catalog (`libs.versions.toml`)

Single source of truth for versions and plugin IDs:

```toml
[versions]
kotlin = "2.3.0"; coroutines = "1.10.0"; ktor = "3.1.0"

[libraries]
kotlinx-coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version.ref = "coroutines" }
ktor-server-core = { module = "io.ktor:ktor-server-core", version.ref = "ktor" }

[plugins]
kotlin-jvm = { id = "org.jetbrains.kotlin.jvm", version.ref = "kotlin" }

[bundles]
testing = ["junit-jupiter"]
```

Member modules use `alias(libs.plugins.kotlin.jvm)` in `plugins { }` and `implementation(libs.kotlinx.coroutines.core)` in `dependencies { }`.

### Convention plugins in `build-logic/`

Modern (Gradle 7+) replacement for `buildSrc/`. Convention plugins are applied via `id("acme.kotlin.library")` and keep build files DRY. Benefits over `buildSrc/`: incremental (no full-project recompile), composable, and itself testable as a Gradle build.

---

## Public API Surface Management

### `binary-compatibility-validator` (libraries only)

```kotlin
// root build.gradle.kts
plugins {
    id("org.jetbrains.kotlinx.binary-compatibility-validator") version "0.16.0"
}
```

Generates `.api` files capturing the public bytecode surface. CI checks against committed `.api` files; any drift fails the build.

```bash
./gradlew apiCheck      # verify no drift
./gradlew apiDump       # update .api files (after intentional changes)
```

### `@PublishedApi` and `@JvmField` discipline

```kotlin
// Library code:
internal const val MAGIC = 42

@PublishedApi
internal const val PUBLIC_MAGIC = 42    // accessible from public inline functions

inline fun foo() = PUBLIC_MAGIC         // would otherwise need MAGIC public
```

`@PublishedApi internal` is the "internal-but-visible-to-inline-callers" qualifier — narrower than `public` but accessible from public inline bodies.

### Version-bump rules of thumb (SemVer)

| Change | SemVer impact |
|--------|---------------|
| Add a `public` symbol | minor |
| Add a method to a sealed interface | minor (no downstream impls possible) |
| Add a method to an open interface | major (downstream impls break) |
| Add a default-implemented method to an interface | minor (mostly safe; Java consumers may compile but binary-incompat) |
| Remove or rename anything `public` | major |
| Change a `@JvmField` to a property with getter | major (Java consumers see API shape change) |
| Add an enum entry | minor (Kotlin `when` exhaustive consumers get a warning; Java is fine) |
| Migrate `kapt` → `KSP2` in published library | minor (consumers transparent) |
| Raise Kotlin / JVM target | typically minor for K1→K2; consult `gradle/libs.versions.toml` |

---

## Refactoring Playbooks

### Strangler-Fig: replace legacy impl behind a feature flag

```kotlin
// build.gradle.kts
sourceSets {
    main {
        kotlin.srcDirs += if (project.hasProperty("useNewRenderer")) {
            file("src/main-new/kotlin")
        } else {
            file("src/main-old/kotlin")
        }
    }
}
```

Better: use DI to swap at runtime:

```kotlin
val renderer: Renderer = if (config.featureFlags.newRenderer) {
    SvgRendererV2()
} else {
    SvgRendererV1()
}
```

Phases:
1. Ship V2 behind feature flag, off by default.
2. Enable V2 for internal users.
3. Enable V2 by default; keep V1 available.
4. Remove V1 in the next major release.

### Branch by Abstraction

1. Introduce an interface abstracting the operation.
2. Both old impl and new impl satisfy the interface.
3. Inject via DI at the composition root.
4. Swap default impl. Old impl is now deletable.

### Module Split Protocol

Splitting one module into two (e.g., `:widgets` → `:widgets-core` + `:widgets-cli`):

1. **Create the new module**: `mkdir widgets-core && touch widgets-core/build.gradle.kts`.
2. **Update `settings.gradle.kts`**: `include(":widgets-core")`.
3. **Move source physically**: `git mv widgets/src/main/kotlin/.../core/* widgets-core/src/main/kotlin/.../`.
4. **Add new module as dependency**: `widgets/build.gradle.kts` gets `implementation(project(":widgets-core"))`.
5. **Adjust visibility**: items that crossed the old module boundary as `internal` must now be `public`. Add `@PublishedApi` if you need inline access only.
6. **Use `api` configuration** if downstream consumers of `:widgets` need transitive access to `:widgets-core` types.
7. **Re-export for source compat** via typealias:
   ```kotlin
   // widgets/src/main/kotlin/com/acme/widgets/Compat.kt
   typealias Renderer = com.acme.widgets.core.Renderer
   ```
8. **Update tests** to target the new module's test source set.
9. **Verify**: `./gradlew assemble test apiCheck`.

### Inverting a Circular Dependency

```
Before:  app ─uses─> infra ─callback─> app   (logical cycle)
After:   domain (defines interface I)
         app    ─uses─> domain
         infra  ─impls─> I (from domain)
         app    ─composes─> infra at startup
```

Steps:
1. Extract the interface into the lowest layer (`domain` or `shared-kernel`).
2. Move the impl to `infra`, depending only on `domain`.
3. Wire at the composition root (`app`).
4. Delete the old direct edge from `infra` back to `app`.

---

## ADR Triggers Specific to Kotlin

Document the decision when one of these arises:

- **Async runtime / framework choice.** Coroutines is the default; record an ADR if you mix with RxJava, Project Reactor, or Java `CompletableFuture` across the same module.
- **Server-side framework.** Ktor (Kotlin-native, suspend-first) vs Spring Boot (mature, Java-rooted) vs Micronaut. Affects every controller, every DI integration. See best-practices §6 (Server-side Kotlin).
- **Gradle DSL.** Kotlin DSL (`build.gradle.kts`) vs Groovy DSL — Kotlin DSL is the default for new projects since 2024 but slower to configure; document if you mix.
- **kapt vs KSP2.** KSP2 is the default since Kotlin 2.0; document explicitly if any processor remains on kapt.
- **DI framework.** Hilt vs Koin vs kotlin-inject vs Spring DI (see [Interface-Based DI](#interface-based-di-hilt--koin--kotlin-inject)). Once chosen, switching cost is high.
- **KMP target selection.** Which platforms to support (Android, iOS, JVM, JS, Native, Wasm). Each adds CI cost and constrains API design (Sendable-equivalent on Native).
- **Compose Multiplatform vs platform-native UI.** Sharing UI via Compose Multiplatform vs implementing native UIs per platform (link to `native` skill). Major architectural commitment.
- **MVI vs MVVM.** Compose-heavy apps often pick MVI (state + intent + reducer); MVVM works on traditional View systems. Affects state-flow design throughout.
- **Repository pattern with Flow returns vs Result returns.** `Flow<List<T>>` for reactive, `suspend fun -> Result<T, E>` for one-shot with explicit error. Decide per repository.
- **`expect`/`actual` strategy in KMP.** Heavy `expect`/`actual` per-platform-impl vs interfaces-with-platform-impl-injection. The latter is usually cleaner; document the policy.
- **Error strategy.** Exceptions vs `Result<T>` (kotlin.Result) vs Arrow `Either<E, T>` vs sealed-class outcomes. Pick one per layer; mixing is the smell.
- **Kotlin/JVM target version (`-jvm-target`).** 17 / 21 / 25. Affects which `java.util.*` types you may use; locks team into a JVM floor.

ADR format → use Scribe's `adr` recipe (Nygard or MADR). Atlas owns the architectural tradeoff analysis; Scribe authors the artifact.

---

## Architecture Anti-Patterns

| Anti-pattern | Why it hurts | Better path |
|--------------|--------------|-------------|
| **God `:app` module**: domain + UI + adapter + tests all in one module | Compile times explode; PRs collide; module boundaries become advisory; KMP migration impossible later | Layered or feature-sliced split; convention plugins to keep build files DRY |
| **`expect`/`actual` for every platform difference** (KMP) | Combinatorial complexity; can't share tests; every new platform requires new `actual` | Common-by-default with platform-specific impl injected via DI; `expect`/`actual` only for genuinely-no-common-shape APIs |
| **Hilt + Koin in the same module** | Two DI containers means two ownership models; every binding is a coin flip | Pick one per module; usually Hilt on Android, Koin on KMP/server, kotlin-inject when both apply |
| **kapt remaining after K2 migration** | Build slowdown; some K2 features unavailable; missing future compat | Migrate processors to KSP2 one at a time; track outstanding `kapt(...)` lines as tech debt |
| **`open` everywhere** ("for testability") | Kotlin is final-by-default for a reason — open-by-default invites subclass-coupling bugs | Inject interfaces; subclass only on types designed for it (frameworks, base impls) |
| **All-public Gradle module API surface** | Downstream pins to internal structure; refactor cost is downstream cost | `internal` for non-API; explicit-api mode on libraries |
| **`:domain` depending on Android types** (`Context`, `Bundle`, `View`) | Couples pure logic to Android; can't unit-test without instrumentation; KMP impossible | `:domain` is pure Kotlin (or `commonMain` in KMP); Android types only in `:adapter-android` |
| **Mixed `implementation` and `api` configurations without convention** | Transitive deps leak unpredictably; ABI changes ripple | Use `api` only when a type appears in your public signature; everything else is `implementation` |
| **Channel as state holder** | `Channel` is for hand-off; `StateFlow` is for state. Misuse causes mysterious lost-update bugs | `StateFlow` for last-value state; `SharedFlow` for events; `Channel` only when send-suspension semantics are needed |
| **`runBlocking { }` at the app entry** as the "main" suspend bridge | Blocks the calling thread; loses structured concurrency benefits | `suspend fun main()` (Kotlin 1.4+) — first-class supported |

For full anti-pattern catalog: [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md) §4 (Class hierarchy), §13 (Gradle/KSP), §17 (API Design).

---

## Where to dig deeper

- Project structure & Gradle: [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) §5
- Architecture patterns: [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) §11
- Multiplatform best practices: [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) §4
- Class hierarchy pitfalls: [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md) §4
- API design pitfalls: [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md) §17
- KMP & K2 specifics: [`builder/reference/kotlin-language-spec.md`](../../builder/reference/kotlin-language-spec.md) §5, §13
