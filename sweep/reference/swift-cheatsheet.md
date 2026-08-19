# Swift Cleanup Cheatsheet (Swift 6.2+)
Purpose: Sweep-flavored slice of the Swift knowledge base — what dead-code / unused-import / orphan-symbol tools each catch, what is safe to remove, and what looks dead but isn't (Objective-C runtime, KVO, Interface Builder, Codable synthesis, macros).
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Tooling Matrix
| Tool | Catches | Misses | Notes |
|------|---------|--------|-------|
| `swiftc -warnings-as-errors` (or `-Wunused-result`) | Unused `@discardableResult`-missing returns, unused `let` bindings | Cross-module unused public symbols, runtime-consumed symbols | Free — already runs in every build |
| SwiftLint `unused_declaration` | `internal`/`fileprivate`/`private` symbols not referenced anywhere | Reflection-accessed, `@objc`-bridged, IB-consumed | Build-into-Xcode integration; configurable via `.swiftlint.yml` |
| SwiftLint `unused_import` | `import Foo` declarations never used | Conditional imports `#if canImport(Foo)` | Pair with `unused_declaration` for full sweep |
| SwiftLint `unused_setter_value` | Custom setter that ignores `newValue` | — | Cheap detection of incomplete property implementations |
| SwiftLint `unused_optional_binding` | `if let _ = x` patterns (could be `if x != nil`) | — | Style + clarity fix |
| SwiftLint `unused_capture_list` | `[weak self]` captures that are never referenced | — | Catches stale closures after refactor |
| [Periphery](https://github.com/peripheryapp/periphery) | Cross-module unused declarations including `public` items in app targets | Items consumed via Obj-C runtime, IB, Codable synthesis (without exclusions) | The de-facto Swift dead-code analyser; requires Xcode build to feed it |
| `xcrun swift-symbolgraph-extract` | Public symbol graph per module | Internal items | Useful for diffing public API across releases |
| Xcode "Unused Declarations" build setting | Compiler-emitted unused warnings | Same as `swiftc` | `SWIFT_TREAT_WARNINGS_AS_ERRORS=YES` makes them blocking |
| `swift package show-dependencies` | Direct + transitive SPM deps | Not "unused" — just lists | Use as input to manual triage |
| swift-format `--lint` | Style + some unused-imports detection | Less aggressive than SwiftLint here | Apple's own tool; good baseline |
- **Recommended combined sweep**
---
## Tread-Carefully Categories (Swift Landmines)
### `@objc` / `@objcMembers` symbols
- No `.m`/`.mm`/`.h` file references the selector name.
- No `NSSelectorFromString("...")` / `Selector("...")` / `#selector(...)` call uses it.
- No `NSClassFromString("...")` instantiation refers to it.
- **`dynamic` properties**
- **`@IBInspectable` / `@IBOutlet` / `@IBAction`**
- **`@_cdecl` exports**
- **`Codable` synthesis members**
- **`Mirror` / `objc` reflection consumers**
- **`@available(*, deprecated)` items**
- **`#if DEBUG` / `#if canImport(...)` blocks**
- **Protocol witnesses consumed via type-erasure**
- **Macro-emitted symbols**
- **`@main` and SwiftUI `App` entry points**
---
## Unused Imports in Swift
- **Re-export imports**: `@_exported import Foo` — used by downstream importers; SwiftLint shouldn't flag, but verify.
- **Conditional imports**: `#if canImport(UIKit) import UIKit #endif` — only "used" on platforms that have UIKit; sweep per platform.
- **Protocol-conformance-only imports**: importing `Combine` only because your file conforms to `ObservableObject` — SwiftLint may flag; Periphery is more accurate.
- **`@testable import`** in test targets — required for `internal` access; never flag as unused.
---
## SwiftPM Cleanup
### Unused dependencies in `Package.swift`
- Build-tool plugins (`.plugin(name:, package:)`) — used by SwiftPM commands, not via `import`.
- Macros declared with `.macro(name:targets:)` — consumed via `@Macro` attribute, not `import`.
- Resource-only dependencies — included for asset bundling.
- **Dead package targets**
- **`swift package show-dependencies --format tree`**
- **Package traits (Swift 6.1+)**
---
## Conditional Compilation Cleanup
- **Stale `#if` blocks**
- **Compile-time-only flags**
- **Build-config attributes that are always-on**
- **Deprecated `#if swift(>=...)`**
---
## Cleanup Workflow
1. **Baseline** — `swift build -c release` + `swift test`. Capture compile time and binary size.
2. **Run the combined sweep** — SwiftLint + Periphery + `swift build -Xswiftc -warnings-as-errors`.
3. **Triage by category** — file each finding into Safe-to-Remove vs Tread-Carefully.
4. **For each Tread-Carefully**, run the verifying check (`@objc` grep, storyboard grep, `Codable` field search, macro AST dump).
5. **Delete in atomic commits** — one logical group per commit. Never mix "remove unused dep" with "rename module."
6. **Re-run sweep + tests** — `swift test`, `xcodebuild test`, `swiftlint lint --strict`.
7. **Diff public surface** (libraries only) — compare symbol graphs from before/after.
8. **Measure** — re-check compile time, `.ipa`/`.app` size, dep count.
9. **Document the deletion rationale** in the PR description, especially for `@objc` / `Codable` / `@available` adjacent removals.
---
## Where to dig deeper
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
- Cross-language tooling matrix: [`language-patterns.md`](./language-patterns.md)
