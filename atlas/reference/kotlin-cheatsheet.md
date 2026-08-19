# Kotlin Architecture Cheatsheet (Kotlin 2.3+ / K2)
Purpose: Atlas-flavored slice of the Kotlin knowledge base — Gradle multi-module architecture patterns, interface-based DI, visibility hygiene, circular-dep detection, public-API surface management, and ADR triggers specific to Kotlin.
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Module Visibility Hygiene
| Modifier | Reachable from |
|----------|----------------|
| `private` (top-level) | Same file |
| `private` (class member) | Same class |
| `protected` (class member) | Class + subclasses (no top-level form) |
| `internal` | Same Gradle module |
| `public` (default) | Everywhere |
- **`internal` is the underused middle ground**
### Sealed interfaces (prevent downstream impls)
- You want forward-compat freedom to add methods (no breaking-change risk from downstream impls).
- The interface represents a closed enumeration of behaviors.
- **Explicit-API mode for libraries**
---
## Circular Dependency Detection
### Tools
| Tool | Scope | Use For |
|------|-------|---------|
| `./gradlew :module:dependencies` | Per-module direct + transitive | Inspect what a module actually pulls in |
| `./gradlew projectDependencyGraph` | Workspace-level module graph | Visualize module-to-module edges |
| IntelliJ "Dependency Structure Matrix" | Per-module class-level coupling | Find unintended class-level cycles |
| Konsist | Test-style architecture rules | Enforce "no class in domain may depend on infra" rules in CI |
| `gradle-dependency-analysis-plugin buildHealth` | Misplaced configurations | Detect `implementation` that should be `api` |
| Detekt `Indentation` + `LongMethod` proxy | Coupling smells | Indirect signal |
### Common circular smells in Kotlin
1. **App → Infra → App via callback registration.** The Infra layer calls back into Application services through a registered lambda. Fix: invert via an interface owned by `application`; `infra` implements it.
2. **Module A re-exports types from Module B, while Module B uses interfaces defined in Module A.** Compiles but creates an "if you import either, you import both" coupling. Fix: move the shared types into a `shared-kernel` / `common` module.
3. **Package cycle inside a module**: `package a` uses items from `package b` which uses items from `package a`. Kotlin allows it but muddies reasoning. Fix: extract shared items into a parent or sibling package.
4. **Test code reaching into prod code via `internal` shortcuts that grow into a backdoor.** Fix: keep a clean test-only API; use `@VisibleForTesting` annotation if necessary.
---
## God-Module Split Signals
- **Compile time > 30s** for a clean incremental rebuild of one module.
- **`dependencies { }` block has > 15 entries** suggesting bundled concerns.
- **`:app` module contains domain + adapter + UI code** — Android template default that ages badly.
- **`commonMain` (KMP) > 100 source files** — split into feature sub-modules per bounded context.
- **A single file > 2000 LOC** without natural sub-files.
- **PRs from different teams routinely touch the same module** — change ownership is unclear.
- **Gradle build report shows one module as 80% of build time** — split required.
- **Module exposes classes from 3+ unrelated bounded contexts** as `public` API.
---
## Build Configuration Deltas
- **Version catalog (`libs.versions.toml`)**
- **Convention plugins in `build-logic/`**
---
## Public API Surface Management
- **`binary-compatibility-validator` (libraries only)**
- **`@PublishedApi` and `@JvmField` discipline**
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
## ADR Triggers Specific to Kotlin
- **Async runtime / framework choice.** Coroutines is the default; record an ADR if you mix with RxJava, Project Reactor, or Java `CompletableFuture` across the same module.
- **Server-side framework.** Ktor, Spring Boot, and Micronaut impose different controller and DI boundaries. Preserve the repository framework unless migration is explicitly in scope.
- **Gradle DSL.** Kotlin DSL (`build.gradle.kts`) vs Groovy DSL — Kotlin DSL is the default for new projects since 2024 but slower to configure; document if you mix.
- **kapt vs KSP2.** KSP2 is the default since Kotlin 2.0; document explicitly if any processor remains on kapt.
- **DI framework.** Hilt vs Koin vs kotlin-inject vs Spring DI. Once chosen, switching cost is high.
- **KMP target selection.** Which platforms to support (Android, iOS, JVM, JS, Native, Wasm). Each adds CI cost and constrains API design (Sendable-equivalent on Native).
- **Compose Multiplatform vs platform-native UI.** Sharing UI via Compose Multiplatform vs implementing native UIs per platform (link to `native` skill). Major architectural commitment.
- **MVI vs MVVM.** Compose-heavy apps often pick MVI (state + intent + reducer); MVVM works on traditional View systems. Affects state-flow design throughout.
- **Repository pattern with Flow returns vs Result returns.** `Flow<List<T>>` for reactive, `suspend fun -> Result<T, E>` for one-shot with explicit error. Decide per repository.
- **`expect`/`actual` strategy in KMP.** Heavy `expect`/`actual` per-platform-impl vs interfaces-with-platform-impl-injection. The latter is usually cleaner; document the policy.
- **Error strategy.** Exceptions vs `Result<T>` (kotlin.Result) vs Arrow `Either<E, T>` vs sealed-class outcomes. Pick one per layer; mixing is the smell.
- **Kotlin/JVM target version (`-jvm-target`).** 17 / 21 / 25. Affects which `java.util.*` types you may use; locks team into a JVM floor.
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
