# Sweep Language-Specific Patterns Reference

Purpose: language-specific detection tooling, fallback rules, and common false-positive cases.

Scope boundary:
- This file = **per-language tooling** (knip/vulture/staticcheck/cargo-udeps choice and fallback hierarchy).
- `false-positives.md` = **cross-language detection patterns** (dynamic loading, framework conventions, magic strings, risk matrix).
- `troubleshooting.md` = **recovery procedures** when tool output misleads (ts-prune/depcheck re-export false-positive flow, backup restore).

## Contents

1. TypeScript / JavaScript
2. Python
3. Go
4. Rust
5. Swift
6. Kotlin
7. Language-agnostic risk patterns

## TypeScript / JavaScript

### `knip`-First Strategy

`knip` is the primary tool for TS/JS projects. It replaces `ts-prune`, `depcheck`, and `unimported` for files, exports, dependencies, and types.

```bash
npx knip --reporter compact
npx knip --reporter json
npx knip --include files
npx knip --include exports
npx knip --include dependencies
```

### Fallback Tools

Use these only when `knip` is unavailable, unsupported, or failing:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `ts-prune` | Unused exports | Export-only fallback |
| `depcheck` | Unused dependencies | Dependency-only fallback |
| `unimported` | Unused files | File-only fallback |

```bash
npx ts-prune --error
npx depcheck --ignores="@types/*,eslint-*"
```

### Common False Positives

- Dynamic imports with template literals
- Re-export barrels such as `index.ts`
- Type-only exports
- Framework convention files

## Python

| Tool | Purpose | Usage |
|------|---------|-------|
| `vulture` | Dead code | `vulture src/ --min-confidence 80` |
| `autoflake` | Unused imports | `autoflake --check .` |
| `pip-autoremove` | Package review | `pip-autoremove --list` |

Common false positives:
- `__init__.py`
- dunder methods
- decorator-driven routes and tasks

```bash
vulture src/ whitelist.py --min-confidence 80
autoflake --check --remove-all-unused-imports -r .
```

## Go

| Tool | Purpose | Usage |
|------|---------|-------|
| `staticcheck` | Unused code | `staticcheck -checks U1000 ./...` |
| `deadcode` | Reachability review | `deadcode -test ./...` |
| `go mod tidy` | Dependency cleanup | `go mod tidy -v` |

Common false positives:
- interface implementations
- exported public API
- `init()` functions
- CGO glue

## Rust

| Tool | Purpose | Usage |
|------|---------|-------|
| `cargo udeps` | Unused dependencies | `cargo +nightly udeps` |
| `cargo clippy` | Dead code warnings | `cargo clippy -- -W dead_code` |

```bash
cargo +nightly udeps
cargo +nightly udeps --workspace
cargo clippy -- -W dead_code
```

### Edition 2024 / 1.85+ Deep-Dive

The table above is the language-patterns quick lookup. For Rust-specific cleanup landmines — including:

- Full tooling matrix (`cargo machete`, `cargo unused-features`, `cargo bloat`, `cargo-modules`, `cargo expand`)
- Safe-to-remove vs tread-carefully categories
- FFI symbol landmines (`#[no_mangle]`, `#[unsafe(no_mangle)]`, `#[used]`, `#[link_section]`)
- `#[cfg(feature = "...")]` / `#[cfg(test)]` / `#[derive]`-fed / `Drop` impl pitfalls
- Workspace-wide cleanup, version drift in `[workspace.dependencies]`
- Feature flag cleanup workflow

→ Read [`rust-cheatsheet.md`](./rust-cheatsheet.md).

Upstream sources of truth (do not duplicate):

- Cargo / dependency pitfalls: [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) §10
- Cargo & toolchain 2026 stack: [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md) §4
- Edition 2024 cleanup nuances: [`builder/reference/rust-language-spec.md`](../../builder/reference/rust-language-spec.md)

## Swift

| Tool | Purpose | Usage |
|------|---------|-------|
| `swiftlint` | Unused declarations, unused imports, unused captures | `swiftlint lint --strict` |
| Periphery | Cross-module unused declarations | `periphery scan --workspace MyApp.xcworkspace --schemes MyApp` |
| `swiftc -warnings-as-errors` | Builtin unused-result and dead-code warnings | `swift build -Xswiftc -warnings-as-errors` |
| `xcrun swift-symbolgraph-extract` | Public symbol surface diff (libraries) | See cheatsheet |

Common false positives:
- `@objc` / `@objcMembers` / `dynamic` (consumed via Obj-C runtime, KVO)
- `@IBOutlet` / `@IBAction` / `@IBInspectable` (consumed by Interface Builder)
- `Codable` synthesized members
- Macro-emitted symbols
- `#if DEBUG` / `#if canImport(...)` blocks

### Swift 6.2 Deep-Dive

The table above is the language-patterns quick lookup. For Swift-specific cleanup landmines — including:

- Full tooling matrix (SwiftLint rules, Periphery config, symbol graphs)
- Safe-to-remove vs tread-carefully categories
- Obj-C runtime landmines (`@objc`, `@objcMembers`, `dynamic`, `@_cdecl`)
- Interface Builder consumers (`@IBOutlet`, `@IBAction`, `@IBInspectable`)
- `Codable` synthesis, `Mirror` reflection, macro-emitted symbols
- SwiftPM dependency cleanup, package traits cleanup
- `#if DEBUG` / `#if swift(>=...)` stale-block removal

→ Read [`swift-cheatsheet.md`](./swift-cheatsheet.md).

Upstream sources of truth (do not duplicate):

- Bad-pattern catalog: [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md)
- Toolchain & libraries: [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md)
- Module system & access control: [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md) §11

## Kotlin

| Tool | Purpose | Usage |
|------|---------|-------|
| Detekt | Unused private/internal members, imports, parameters | `./gradlew detekt` |
| IntelliJ "Unused declaration" inspection | Cross-module unused symbols | `./gradlew qodana` (CI) |
| `gradle-dependency-analysis-plugin` | Unused dependencies, misplaced configurations | `./gradlew buildHealth` |
| `-Xexplicit-api=strict` | Library public-API exposure | `./gradlew assemble -PkotlinExplicitApi=strict` |
| Ktlint | Unused imports (style) | `./gradlew ktlintCheck` |

Common false positives:
- Reflection-accessed (`KClass.declaredMemberProperties`, Spring component scanning)
- `@Component` / `@Service` / `@Repository` (Spring auto-detect)
- `@SerialName` fields on `Serializable` types (consumed by kotlinx.serialization)
- `@Parcelize` data class fields
- `@JvmField` / `@JvmStatic` / `@JvmOverloads` (Java interop)
- KSP2 / kapt generated code references
- `lateinit` properties (init via DI / framework)
- `data class` synthesized members (`copy`, `componentN`)
- Compose `@Composable` callable signatures
- Convention plugins in `buildSrc/` / `build-logic/`

### Kotlin 2.3+ / K2 Deep-Dive

The table above is the language-patterns quick lookup. For Kotlin-specific cleanup landmines — including:

- Full tooling matrix (Detekt rules, IntelliJ inspections, dependency analysis plugin)
- Safe-to-remove vs tread-carefully categories
- Reflection / Spring DI / kotlinx.serialization landmines
- `@Parcelize`, `@JvmField`/`@JvmStatic`/`@JvmOverloads` removal pitfalls
- KSP2 / kapt-generated code, `lateinit`, `data class` synthesis
- Gradle multi-module cleanup, version catalog cleanup
- kapt → KSP2 migration cleanup

→ Read [`kotlin-cheatsheet.md`](./kotlin-cheatsheet.md).

Upstream sources of truth (do not duplicate):

- Bad-pattern catalog: [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md)
- Gradle / build toolchain: [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) §5
- K2 specifics: [`builder/reference/kotlin-language-spec.md`](../../builder/reference/kotlin-language-spec.md) §13

## Language-Agnostic Risk Patterns

Files frequently misdetected across stacks:
- entry points such as `main.*`, `index.*`, `app.*`
- config files such as `*.config.*`, `.*rc`
- test fixtures and mocks
- generated code such as `*.generated.*`
- documentation and docs-linked assets
