# Kotlin Cleanup Cheatsheet (Kotlin 2.3+ / K2)

Purpose: Sweep-flavored slice of the Kotlin knowledge base — what dead-code / unused-import / orphan-dep tools each catch, what is safe to remove, and what looks dead but isn't (reflection, Spring DI, Parcelize, KSP-generated code, JVM interop).

Baseline: **Kotlin 2.3+, K2 compiler, KSP2 default, Gradle 8.x**.

Source of truth (do not duplicate here):
- Bad-pattern catalog → [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md)
- Gradle / build toolchain → [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) §5
- Visibility, K2 specifics → [`builder/reference/kotlin-language-spec.md`](../../builder/reference/kotlin-language-spec.md) §13

Companion: [`language-patterns.md`](./language-patterns.md) holds the cross-language tooling matrix. Read this file for Kotlin-specific landmines and Gradle-scale cleanup.

---

## Contents

- [Tooling Matrix](#tooling-matrix)
- [Safe-to-Remove Categories](#safe-to-remove-categories)
- [Tread-Carefully Categories (Kotlin Landmines)](#tread-carefully-categories-kotlin-landmines)
- [Unused Imports in Kotlin](#unused-imports-in-kotlin)
- [Gradle / Multi-Module Cleanup](#gradle--multi-module-cleanup)
- [kapt → KSP2 Migration Cleanup](#kapt--ksp2-migration-cleanup)
- [Cleanup Workflow](#cleanup-workflow)

---

## Tooling Matrix

What each tool actually catches. Run them as a combined sweep — no single tool covers the full surface.

| Tool | Catches | Misses | Notes |
|------|---------|--------|-------|
| `kotlinc -Werror -Xexplicit-api=strict` | Public API surface that lacks explicit visibility or types (libraries) | Not "unused" — but flags accidental `public` items | Library mode only; not for app projects |
| Detekt `UnusedPrivateMember` | Unused `private` functions, properties, parameters | `internal`/`public` unused items | Default-enabled rule |
| Detekt `UnusedImports` | `import` declarations with no usage | Wildcard imports (`import foo.*`) | Detect needs the file to compile to be sure |
| Detekt `UnusedParameter` | Function parameters never referenced | Overrides (signatures must match), interface impls | Set `allowedNames` regex if you have callback params with conventional names |
| Detekt `UnusedPrivateClass` | Top-level / nested private classes never used | Same as `UnusedPrivateMember` for class scope | Pair with `UnusedPrivateMember` |
| Detekt `LongParameterList` | Cleanup signal: 6+ params → extract data class | Not "dead" — but identifies sweep candidates | |
| IntelliJ "Unused declaration" inspection | Cross-module unused symbols, including `internal` and `public` (with usage scope) | Reflection-accessed, Spring-component-scanned | Run via `Code → Inspect Code…` or in CI via `qodana` |
| Konsist | Architecture rule + dead-class detection | — | Test-style rules: "no class in `domain` may depend on `infra`" |
| `kotlinx-knit` | Detects drift between code snippets and docs | Not for dead code, but useful for orphan example files | |
| Gradle Dependency Analysis plugin (`gradle-dependency-analysis-plugin`) | Unused dependencies, transitive deps used directly, misplaced configurations (`api` vs `implementation`) | Reflection-loaded classes | The Kotlin/Gradle equivalent of `cargo-machete` |
| `Werror` + `-Xexplicit-api=warning` (mixed mode) | Public API exposure on non-library projects | — | Useful in module APIs |
| R8 / ProGuard (Android) | Bytecode dead-code elimination | Source-level dead code | Runs at release build; useful "ultimate ground truth" but does not propose deletions |

### Recommended combined sweep

```bash
# 1. Detekt (broad)
./gradlew detekt

# 2. Compiler in strict mode (libraries)
./gradlew assemble -PkotlinExplicitApi=strict

# 3. Dependency analysis
./gradlew buildHealth        # gradle-dependency-analysis-plugin

# 4. IntelliJ inspections in CI
./gradlew qodana             # if Qodana is configured
```

Detekt config snippet:

```yaml
# detekt.yml
style:
  UnusedImports:
    active: true
  UnusedParameter:
    active: true
    allowedNames: 'ignored|expected|_'
  UnusedPrivateClass:
    active: true
  UnusedPrivateMember:
    active: true
    allowedNames: ''     # tighten — no exception names
```

---

## Safe-to-Remove Categories

Items in these categories can typically be removed after a single reachability check:

1. **`private` / `internal` members not referenced.** Compiler doesn't always warn for `internal`; Detekt or IntelliJ catches them.
2. **Unused `import` statements.** Detekt `UnusedImports`. Note: `import` of a typealias may legitimately appear unused if only the underlying type is named.
3. **Unused parameters** (after refactor). Detekt `UnusedParameter`. Always check that the function isn't an override; overrides must keep the parameter.
4. **Test fixtures referenced by no `@Test` (JUnit5 / Kotest) or `@RobolectricTest`.** Look for stale helpers in `src/test/kotlin/.../support/`.
5. **`companion object` constants nobody uses.** Detekt + IntelliJ catch these.
6. **Top-level functions/extensions never imported anywhere.** IntelliJ "Unused declaration" inspection.
7. **Dead Gradle modules** — `:app-legacy` that no `:app` includes via `implementation(project(":app-legacy"))`.
8. **Unused `buildSrc` / `build-logic` convention plugins** — convention plugins never applied by any module.
9. **Stale `@OptIn(...)` annotations** for experimental APIs that have since been stabilized.

Workflow: flag → confirm via reachability check → remove → `./gradlew assemble test` → commit in a small focused PR.

---

## Tread-Carefully Categories (Kotlin Landmines)

Items that LOOK dead but break the world when removed. Do **not** delete without explicit verification.

### Reflection-accessed symbols

```kotlin
data class User(val id: String, val name: String, val email: String)

// Elsewhere — invisible to Detekt and IntelliJ:
fun toMap(obj: Any): Map<String, Any?> =
    obj::class.declaredMemberProperties.associate { it.name to it.getter.call(obj) }
```

If you have any of:
- `KClass.declaredMemberProperties` / `memberProperties`
- `KClass.memberFunctions` / `declaredMemberFunctions`
- `Class.getDeclaredField(...)`
- `MethodHandles.lookup()` patterns

…then fields/methods may be consumed reflectively. Search for these APIs before removing properties.

### Spring DI auto-wiring

```kotlin
@Component
class OrderService(private val repo: OrderRepository) { /* ... */ }

@Repository
interface OrderRepository : JpaRepository<Order, Long>
```

Spring's component scanner instantiates `@Component`/`@Service`/`@Repository`/`@Controller`/`@RestController`/`@Configuration` classes via reflection. They look unused — they aren't.

Verify by:
- Checking `@ComponentScan` paths in your `Application.kt`.
- Searching for the bean type in `@Autowired`/`@Inject`/constructor params.
- Running `./gradlew bootRun` and looking for `NoSuchBeanDefinitionException`.

### kotlinx.serialization fields

```kotlin
@Serializable
data class User(
    @SerialName("user_id") val id: String,    // field name accessed only via serializer
    val name: String,
)
```

`@SerialName` is consumed by the generated `serializer()`. Field renaming or removal silently changes wire format.

### `@Parcelize` data class fields (Android)

```kotlin
@Parcelize
data class Args(val id: String, val flags: Int) : Parcelable
```

The Parcelize plugin generates `writeToParcel`/`createFromParcel` based on the declared fields. Removing a field doesn't break Kotlin compile but does break process death restoration silently.

### `@JvmField` / `@JvmStatic` for Java interop

```kotlin
object Constants {
    @JvmField val MAX_RETRIES = 3        // Java sees: public static final int MAX_RETRIES
    @JvmStatic fun log(s: String) { /* Java: Constants.log(s) */ }
}
```

Removing the annotation breaks Java callers compiling against `Constants.MAX_RETRIES` (they'd need `Constants.INSTANCE.MAX_RETRIES` instead). Treat as public API.

### `@JvmOverloads` generated overloads

```kotlin
@JvmOverloads
fun greet(name: String, greeting: String = "Hello") { /* ... */ }
// Generates Java-visible: greet(String) and greet(String, String)
```

Java callers may use the no-default-argument overload. Removing `@JvmOverloads` removes the Java overload silently.

### KSP2 / kapt-generated code references

```kotlin
@Module
@InstallIn(SingletonComponent::class)
interface RepositoryBindings {
    @Binds fun bindOrderRepo(impl: OrderRepoImpl): OrderRepository
}
```

The `@Binds` function looks "unused" because Hilt generates the implementation. Same applies to Room `@Dao`, Moshi adapters, kotlinx.serialization `@Serializable`, sqldelight queries.

Use `./gradlew kspKotlin --info` (or the equivalent kapt task) and inspect the `build/generated/ksp/.../kotlin/` directory before declaring code unused.

### `lateinit` properties

```kotlin
class Activity {
    @Inject lateinit var analytics: Analytics    // init happens via DI
}
```

`lateinit` properties are initialized elsewhere — DI framework, test setup, framework lifecycle (Android `onCreate`, JUnit `@BeforeEach`). Don't treat them as unused because no constructor reference assigns them.

### `data class` synthesized members

```kotlin
data class Coord(val x: Int, val y: Int)
// Compiler synthesizes: equals, hashCode, toString, copy, componentN
```

Component functions look unused in source but are consumed by destructuring (`val (x, y) = coord`). Never remove a `data class`'s declaration just because the synthesized members "aren't called by name."

### Compose `@Composable` functions

```kotlin
@Composable
fun OrderCard(order: Order) { /* ... */ }
```

Compose's compiler plugin matches callable signatures and rewrites them. A `@Composable` function called from a `LazyColumn { items(orders) { OrderCard(it) } }` block may not look "referenced" to some tools.

### Convention plugins in `buildSrc` / `build-logic`

```kotlin
// build-logic/convention/src/main/kotlin/AndroidLibraryConventionPlugin.kt
class AndroidLibraryConventionPlugin : Plugin<Project> { /* ... */ }
```

Applied via `plugins { id("acme.android.library") }`. Tools won't see the application; verify against `gradle.properties` and module `build.gradle.kts` plugin blocks.

### `@OptIn` propagation

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
fun process() = flow { /* ... */ }
```

If you remove the experimental API call but forget to remove `@OptIn`, the annotation lingers without harm; but if you remove `@OptIn` while the experimental API is still used, the build breaks.

---

## Unused Imports in Kotlin

Detekt's `UnusedImports`:

```bash
./gradlew detekt
```

Ktlint's `no-unused-imports`:

```bash
./gradlew ktlintCheck
# auto-fix:
./gradlew ktlintFormat
```

Caveats:

- **`import ... as` aliases**: Detekt understands these; older Ktlint versions had false-positives.
- **Wildcard imports**: `import kotlinx.coroutines.flow.*` — neither tool can prove all members are unused; they're flagged with `WildcardImports` style rule, not `UnusedImports`.
- **kotlinx.serialization plugins** sometimes inject imports the user didn't write; verify before flagging.
- **`@file:JvmName(...)` annotations** don't count as imports but their target file references must be preserved.

---

## Gradle / Multi-Module Cleanup

### Unused dependencies

```bash
# gradle-dependency-analysis-plugin (the Kotlin equivalent of cargo-machete)
./gradlew buildHealth
```

Output categories:
- `unusedDependencies` — declared in `dependencies { }` but no code references the package.
- `usedTransitiveDependencies` — used directly but only declared transitively (you should declare them explicitly).
- `incorrectConfiguration` — declared as `implementation` but should be `api` (or vice versa).

False positives:
- Reflective use (Spring auto-config) — register exceptions in the plugin config.
- Build-script-only dependencies (e.g., `classpath("...")` in old syntax).

### Dead Gradle modules

Signal that a module is dead:
- No other module has `implementation(project(":dead-module"))` in `dependencies`.
- No `settings.gradle.kts` `include(":dead-module")` is required by an active path.
- No CI workflow runs `./gradlew :dead-module:test`.
- Module's last commit was > 6 months ago.

```bash
# List all included modules:
./gradlew projects

# Find who depends on a module:
./gradlew :target-module:dependencyInsight --dependency :candidate-dead-module
```

### Version catalog cleanup (`libs.versions.toml`)

```toml
[versions]
old-library = "1.2.3"    # nobody uses [libraries].xxx mapped to this

[libraries]
unused-lib = { module = "org.example:unused", version.ref = "old-library" }
```

Detection: grep across all `build.gradle.kts` for `libs.unused-lib` references. If zero, remove the entry.

### Unused convention plugins

`buildSrc/` or `build-logic/` plugins that no module applies are dead. Check via:

```bash
grep -r --include='build.gradle.kts' "id(\"acme\\." . | sort -u
```

Cross-reference against the plugin file names. The diff is the dead set.

### Cross-module visibility tightening

After cleanup, run:

```bash
./gradlew apiCheck    # if binary-compatibility-validator is set up
```

If unexpected `public` symbols appear in the `.api` dump, tighten visibility (`internal`) before release.

---

## kapt → KSP2 Migration Cleanup

When migrating, several dependency entries become deletable:

### Before (kapt era)

```kotlin
plugins {
    id("org.jetbrains.kotlin.kapt")
}

dependencies {
    kapt("com.google.dagger:hilt-compiler:2.x")
    kapt("androidx.room:room-compiler:2.x")
    kapt("com.github.bumptech.glide:compiler:4.x")
}
```

### After (KSP2)

```kotlin
plugins {
    id("com.google.devtools.ksp")
}

dependencies {
    ksp("com.google.dagger:hilt-compiler:2.x")     // if Hilt KSP available
    ksp("androidx.room:room-compiler:2.x")
    ksp("com.github.bumptech.glide:ksp:4.x")
}
```

Deletable after migration:
- The `id("org.jetbrains.kotlin.kapt")` plugin declaration (when no kapt remains).
- Any `kapt(...)` dependency lines for processors that have a KSP port.
- The `kapt { correctErrorTypes = true }` block.
- Any `kapt`-specific Gradle properties in `gradle.properties`.

Be careful:
- Not every processor has KSP support yet (check the processor's release notes).
- Migrate one processor at a time; verify generated code matches.
- KSP2's incremental cache is in `build/kspCaches/...` — delete on first migration build.

See anti-patterns §13 and §14 for the full kapt/KSP pitfall list.

---

## Cleanup Workflow

Recommended ordering for a Kotlin cleanup pass:

1. **Baseline** — `./gradlew assemble test`. Capture compile time and `build/libs/*.jar` size.
2. **Run the combined sweep** — Detekt + IntelliJ inspections + `buildHealth`.
3. **Triage by category** — file each finding into Safe-to-Remove vs Tread-Carefully.
4. **For each Tread-Carefully**, run the verifying check (reflection grep, Spring bean check, KSP/kapt generated-code search, `@Parcelize` field audit).
5. **Delete in atomic commits** — one logical group per commit. Never mix "remove unused dep" with "rename module."
6. **Re-run sweep + tests** — `./gradlew clean assemble test detekt`.
7. **Diff public API** (libraries) — `./gradlew apiCheck`.
8. **Measure** — re-check compile time, artifact size, module count.
9. **Document the deletion rationale** in the PR description, especially for reflection-adjacent, DI-adjacent, or `@Jvm*`-adjacent removals.

---

## Where to dig deeper

- Bad-pattern catalog: [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md)
  - §7 Java Interop, §13 Gradle/KSP, §14 K2 Migration
- Gradle / build toolchain: [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) §5
- K2 specifics & visibility: [`builder/reference/kotlin-language-spec.md`](../../builder/reference/kotlin-language-spec.md) §13, §14
- Cross-language tooling matrix: [`language-patterns.md`](./language-patterns.md)
