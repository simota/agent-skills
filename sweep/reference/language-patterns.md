# Sweep Language-Specific Patterns Reference

Purpose: language-specific detection tooling, fallback rules, and common false-positive cases.

Scope boundary:
- This file = **per-language tooling** (knip/vulture/staticcheck/cargo-udeps choice and fallback hierarchy).
- `reference/false-positives.md` = **cross-language detection patterns** (dynamic loading, framework conventions, magic strings, risk matrix).
- `reference/troubleshooting.md` = **recovery procedures** when tool output misleads (ts-prune/depcheck re-export false-positive flow, backup restore).

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

Start with the installed compiler/Clippy dead-code diagnostics; dependency analyzers are candidate generators, not deletion proofs. Select an already-installed compatible analyzer through its documented help, not a cached plugin/version matrix.

Before deletion, verify:
- FFI names against non-Rust consumers and exported headers; linker-retained `#[used]` / `link_section` / exported symbols are not ordinary call-graph roots.
- Trait-object consumers, `Drop`, derives and procedural-macro output; use the installed toolchain's supported expansion tooling, never a copied unstable flag.
- `cfg(feature)`, `cfg(test)`, build scripts, examples, doctests, binaries and CI targets. No importing workspace member does not prove a crate is unused.
- Feature consumers with `cargo tree -e features`. Test the project's supported feature/target combinations; default-feature tests are incomplete, while mutually exclusive features can make blanket `--all-features` invalid.
- External public-API consumers before removing exports or workspace dependencies.

Canonical feature semantics: https://doc.rust-lang.org/cargo/reference/features.html (checked 2026-09-17). Recheck installed syntax and supported feature combinations when changing the build matrix.

## Swift

Use the project's configured compiler warnings and unused-declaration analysis. SwiftLint `unused_declaration` and `unused_import` are **analyzer rules**: an ordinary `swiftlint lint --strict` run is not evidence they ran. Confirm the installed analyzer configuration and required compiler log before claiming coverage.

Before deletion, verify:
- Objective-C files, selector/class-name strings, KVO, `@objc` / `dynamic` and C exports.
- Storyboards/XIBs and `@IBOutlet` / `@IBAction` / `@IBInspectable`; entry points including `@main` and SwiftUI `App`.
- `Codable` synthesis, reflection, macros and protocol witnesses consumed through type erasure.
- Re-exported/conditional imports, test-target consumers and supported platform/build configurations. Inspect deprecated API consumers; deprecation is not disuse.
- SwiftPM build-tool plugins, macros and resources: absence of `import` does not prove the dependency unused. Diff the public symbol surface for library removals.

Analyzer contracts: https://realm.github.io/SwiftLint/unused_declaration.html and https://realm.github.io/SwiftLint/unused_import.html (checked 2026-09-17). Keep version-specific invocation in the installed tool's documentation, not here.

## Kotlin

Use configured Detekt/IDE inspections and Gradle dependency analysis only where the project's installed plugins expose them. Discover actual wrapper tasks; do not assume `qodana`, `buildHealth`, or `apiCheck` exists. Explicit-API mode checks visibility/types, not dead-code reachability; minifier removal is not proof that deleting source is safe.

Before deletion, verify:
- Reflection, Spring component scanning/DI and `lateinit` initialization.
- Serialization and `Parcelize` fields, generated KSP/kapt consumers, data-class synthesis and Compose signatures.
- Java callers and generated `@JvmField` / `@JvmStatic` / `@JvmOverloads` interfaces; file-level JVM naming, import aliases and opt-in propagation.
- Gradle settings, CI task selectors, build-script dependencies, version catalogs, `buildSrc` and convention plugins. Module age is not a deletion signal.
- Compiler/plugin-generated code and published public APIs across supported targets. A processor migration belongs to a separately scoped migration: confirm processor support and compare generated output before removing kapt configuration.

Language/toolchain claims are subject to `../builder/reference/implementation-policy.md` § Language and Toolchain Grounding.

## Language-Agnostic Risk Patterns

Files frequently misdetected across stacks:
- entry points such as `main.*`, `index.*`, `app.*`
- config files such as `*.config.*`, `.*rc`
- test fixtures and mocks
- generated code such as `*.generated.*`
- documentation and docs-linked assets
