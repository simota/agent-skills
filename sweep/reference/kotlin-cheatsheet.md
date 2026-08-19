# Kotlin Cleanup Cheatsheet (Kotlin 2.3+ / K2)
Purpose: Sweep-flavored slice of the Kotlin knowledge base — what dead-code / unused-import / orphan-dep tools each catch, what is safe to remove, and what looks dead but isn't (reflection, Spring DI, Parcelize, KSP-generated code, JVM interop).
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Tooling Matrix
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
- **Recommended combined sweep**
---
## Tread-Carefully Categories (Kotlin Landmines)
### Reflection-accessed symbols
- `KClass.declaredMemberProperties` / `memberProperties`
- `KClass.memberFunctions` / `declaredMemberFunctions`
- `Class.getDeclaredField(...)`
- `MethodHandles.lookup()` patterns
### Spring DI auto-wiring
- Checking `@ComponentScan` paths in your `Application.kt`.
- Searching for the bean type in `@Autowired`/`@Inject`/constructor params.
- Running `./gradlew bootRun` and looking for `NoSuchBeanDefinitionException`.
- **kotlinx.serialization fields**
- **`@Parcelize` data class fields (Android)**
- **`@JvmField` / `@JvmStatic` for Java interop**
- **`@JvmOverloads` generated overloads**
- **KSP2 / kapt-generated code references**
- **`lateinit` properties**
- **`data class` synthesized members**
- **Compose `@Composable` functions**
- **Convention plugins in `buildSrc` / `build-logic`**
- **`@OptIn` propagation**
---
## Unused Imports in Kotlin
- **`import ... as` aliases**: Detekt understands these; older Ktlint versions had false-positives.
- **Wildcard imports**: `import kotlinx.coroutines.flow.*` — neither tool can prove all members are unused; they're flagged with `WildcardImports` style rule, not `UnusedImports`.
- **kotlinx.serialization plugins** sometimes inject imports the user didn't write; verify before flagging.
- **`@file:JvmName(...)` annotations** don't count as imports but their target file references must be preserved.
---
## Gradle / Multi-Module Cleanup
### Unused dependencies
- `unusedDependencies` — declared in `dependencies { }` but no code references the package.
- `usedTransitiveDependencies` — used directly but only declared transitively (you should declare them explicitly).
- `incorrectConfiguration` — declared as `implementation` but should be `api` (or vice versa).
- Reflective use (Spring auto-config) — register exceptions in the plugin config.
- Build-script-only dependencies (e.g., `classpath("...")` in old syntax).
### Dead Gradle modules
- No other module has `implementation(project(":dead-module"))` in `dependencies`.
- No `settings.gradle.kts` `include(":dead-module")` is required by an active path.
- No CI workflow runs `./gradlew :dead-module:test`.
- Module's last commit was > 6 months ago.
- **Version catalog cleanup (`libs.versions.toml`)**
- **Unused convention plugins**
- **Cross-module visibility tightening**
---
## kapt → KSP2 Migration Cleanup
- **Before (kapt era)**
### After (KSP2)
- The `id("org.jetbrains.kotlin.kapt")` plugin declaration (when no kapt remains).
- Any `kapt(...)` dependency lines for processors that have a KSP port.
- The `kapt { correctErrorTypes = true }` block.
- Any `kapt`-specific Gradle properties in `gradle.properties`.
- Not every processor has KSP support yet (check the processor's release notes).
- Migrate one processor at a time; verify generated code matches.
- KSP2's incremental cache is in `build/kspCaches/...` — delete on first migration build.
---
## Cleanup Workflow
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
- Bad-pattern catalog: [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
  - §7 Java Interop, §13 Gradle/KSP, §14 K2 Migration
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
- Cross-language tooling matrix: [`language-patterns.md`](./language-patterns.md)
