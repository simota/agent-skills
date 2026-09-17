# Language-Specific Reachability Guards

Use the SKILL's primary detection tooling; resolve available commands/plugins against the installed version. Cross-language scan protection is in `reference/cleanup-protocol.md`; recovery is there too.

| Language | False-positive guards |
|---|---|
| TS/JS | Knip first; use a scoped alternative only when unavailable/incompatible, reporting coverage loss. Preserve framework entries, re-export/public barrels, dynamic imports and type consumers; never suppress all `index` or `@types` findings. Load the imports/types/dependency recipe reference for its specific decision. |
| Python | Check `__init__.py`, dunder methods, decorator-registered routes/tasks and any deliberate whitelist before treating absent calls as dead code. |
| Go | Check interface dispatch, external exports, `init()` and CGO consumers. Manifest rewriting is implementation, not a read-only scan. |

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

Language/toolchain claims are subject to `_common/builder/reference/implementation-policy.md` § Language and Toolchain Grounding.
