# Swift Cleanup Cheatsheet (Swift 6.2+)

Purpose: Sweep-flavored slice of the Swift knowledge base — what dead-code / unused-import / orphan-symbol tools each catch, what is safe to remove, and what looks dead but isn't (Objective-C runtime, KVO, Interface Builder, Codable synthesis, macros).

Baseline: **Swift 6.2+, Xcode 26, SwiftPM with traits**.

Source of truth (do not duplicate here):
- Bad-pattern catalog → [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md)
- Toolchain / library matrix → [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md)
- Module system, access control, ABI → [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md) §11

Companion: [`language-patterns.md`](./language-patterns.md) holds the cross-language tooling matrix. Read this file for Swift-specific landmines and project-scale cleanup.

---

## Contents

- [Tooling Matrix](#tooling-matrix)
- [Safe-to-Remove Categories](#safe-to-remove-categories)
- [Tread-Carefully Categories (Swift Landmines)](#tread-carefully-categories-swift-landmines)
- [Unused Imports in Swift](#unused-imports-in-swift)
- [SwiftPM Cleanup](#swiftpm-cleanup)
- [Feature Trait / `#if` Cleanup](#feature-trait--if-cleanup)
- [Cleanup Workflow](#cleanup-workflow)

---

## Tooling Matrix

What each tool actually catches. Run them as a combined sweep — no single tool covers the full surface.

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

### Recommended combined sweep

```bash
# 1. SwiftLint with unused rules enabled
swiftlint lint --strict --reporter emoji

# 2. Periphery — the heavy hitter
periphery scan \
  --workspace MyApp.xcworkspace \
  --schemes MyApp \
  --retain-public \
  --retain-objc-accessible

# 3. swift build with strict flags
swift build -Xswiftc -warnings-as-errors

# 4. Symbol-graph diff (libraries only)
xcrun swift-symbolgraph-extract \
  -module-name MyLib \
  -target arm64-apple-macos14 \
  -output-dir build/symbolgraphs \
  -I build/Modules
```

`.periphery.yml` example for an app:

```yaml
workspace: MyApp.xcworkspace
schemes: [MyApp]
retain_public: false                    # apps have no public consumers
retain_objc_accessible: true            # don't kill @objc symbols
retain_objc_annotated: true
retain_assign_only_properties: false
external_encodable_protocols: [Codable, Decodable, Encodable]
exclude:
  - "**/Generated/**"
  - "**/Vendor/**"
```

---

## Safe-to-Remove Categories

Items in these categories can typically be removed after a single reachability check:

1. **`private` / `fileprivate` symbols not referenced.** Compiler warns directly; SwiftLint `unused_declaration` confirms.
2. **`internal` symbols not referenced anywhere in the module.** Periphery flags these; verify by full-text search for the identifier in the workspace.
3. **Unused `import` statements.** SwiftLint `unused_import`. Note: `import` of a module whose types appear only in protocol conformances (via transitive `import`) can be legitimately unused — Periphery understands this.
4. **Test fixtures referenced by no `@Test` (Swift Testing) or `func test*` (XCTest).** Look for stale helpers in `Tests/Support/` or `XCTestCase` subclasses with all methods deleted.
5. **`fileprivate` extension methods never called within the file.** Same as `private` but scoped wider; still safe.
6. **Unused `@available(*, deprecated)` items whose deprecation period has expired.** Confirm via `git log` that no caller has reappeared.
7. **Dead Xcode targets** (an `App-Demo` target nobody builds) — verify by searching the workspace `xcscheme` files and CI configuration.
8. **Unused `package` symbols (Swift 5.9+)** — `package` access is cross-target within a SwiftPM package; if no other target imports the declaring module's `package` symbols, they're dead.

Workflow: flag → confirm via reachability check → remove → run `swift build && swift test` → commit in a small focused PR.

---

## Tread-Carefully Categories (Swift Landmines)

Items that LOOK dead but break the world when removed. Do **not** delete without explicit verification.

### `@objc` / `@objcMembers` symbols

```swift
@objc
final class AnalyticsBridge: NSObject {
    @objc func trackEvent(_ name: String) { /* called from Objective-C code */ }
}

@objcMembers
final class Settings: NSObject {
    var theme: String = "light"   // accessed via KVC / NSKeyValueCoding
}
```

These symbols are consumed by **Objective-C runtime message passing** — the Swift compiler cannot prove they're reachable, because the consumer doesn't go through Swift call sites. **Never auto-delete** an `@objc` declaration without verifying:
- No `.m`/`.mm`/`.h` file references the selector name.
- No `NSSelectorFromString("...")` / `Selector("...")` / `#selector(...)` call uses it.
- No `NSClassFromString("...")` instantiation refers to it.

### `dynamic` properties

```swift
class Model: NSObject {
    @objc dynamic var name: String = ""   // observed via KVO
}
```

`dynamic` means "this property uses Obj-C dispatch and is KVO-observable." Removing it changes binary-compatibility for observers. KVO observers use string keypaths the compiler can't trace.

### `@IBInspectable` / `@IBOutlet` / `@IBAction`

```swift
final class MyView: UIView {
    @IBOutlet weak var label: UILabel!
    @IBInspectable var cornerRadius: CGFloat = 0
    @IBAction func didTap(_ sender: Any) { }
}
```

Consumed by Interface Builder via the storyboard/XIB. Removing them breaks the UI at runtime — Xcode does not flag this at compile time. Verify by searching `.storyboard` and `.xib` files (they're XML) for the property/selector name.

### `@_cdecl` exports

```swift
@_cdecl("my_library_init")
public func myLibraryInit() -> Int32 { return 0 }
```

C ABI export — consumed by C/C++/Python/JNI hosts the compiler cannot see. Same rule as Rust `#[no_mangle]`: never auto-delete.

### `Codable` synthesis members

```swift
struct Config: Codable {
    let host: String
    let port: Int
    // Synthesized init(from:) and encode(to:) — invisible to greps.
}
```

If you also wrote a custom `init(from decoder:)` that "looks unused", removing it changes the wire format silently — there's no synthesized version to fall back on because the custom one shadows it.

### `Mirror` / `objc` reflection consumers

```swift
struct Settings {
    var theme: String
    var soundEnabled: Bool
}

// Elsewhere: settings dump via Mirror(reflecting:) — fields look unused under name search
```

Search for `Mirror(reflecting:`, `JSONEncoder().encode(`, `NSKeyValueCoding`, `value(forKey:)` before removing fields.

### `@available(*, deprecated)` items

```swift
@available(*, deprecated, renamed: "newAPI")
public func oldAPI() { /* still referenced by old call sites */ }
```

Deprecated does NOT mean dead. Removing pulls the rug on consumers who haven't migrated. Bump major version when you actually remove.

### `#if DEBUG` / `#if canImport(...)` blocks

```swift
#if DEBUG
extension User {
    static let mock = User(id: .init(), name: "Mock")
}
#endif
```

"Unused" in `Release` builds, fully consumed in `Debug` builds (tests, previews). Always compile both configurations before declaring dead.

### Protocol witnesses consumed via type-erasure

```swift
protocol Renderer {
    func render(_ doc: Doc) -> Output
}

final class SvgRenderer: Renderer { /* ... */ }

// Elsewhere: stored as `any Renderer` in a registry — Periphery sees the conformance, may not the impl call sites
```

`any Renderer` / `Box<dyn>`-equivalent erasure hides callsites. Periphery's `--retain-public` and protocol-conformance-aware modes help; verify by grep for `as Renderer` and `any Renderer`.

### Macro-emitted symbols

```swift
@Observable
final class Counter {
    var count = 0
    // Macro emits ObservationRegistrar, _$observationRegistrar, etc. — invisible to source
}
```

Don't try to delete macro-generated members. They aren't in the source. Use `xcrun -sdk macosx swiftc -dump-ast` or `-print-ast-after-macros` to see what's actually emitted.

### `@main` and SwiftUI `App` entry points

```swift
@main
struct MyApp: App { /* ... */ }
```

Consumed by the runtime; no caller in Swift code. Don't delete `@main` just because nobody "calls" it.

---

## Unused Imports in Swift

SwiftLint catches most cases:

```bash
swiftlint lint --quiet --reporter github-actions-logging \
  --enable-rule unused_import \
  --enable-rule unused_declaration
```

Caveats:

- **Re-export imports**: `@_exported import Foo` — used by downstream importers; SwiftLint shouldn't flag, but verify.
- **Conditional imports**: `#if canImport(UIKit) import UIKit #endif` — only "used" on platforms that have UIKit; sweep per platform.
- **Protocol-conformance-only imports**: importing `Combine` only because your file conforms to `ObservableObject` — SwiftLint may flag; Periphery is more accurate.
- **`@testable import`** in test targets — required for `internal` access; never flag as unused.

swift-format also detects some redundant imports with `--strict`:

```bash
swift-format lint --strict --recursive Sources/ Tests/
```

---

## SwiftPM Cleanup

### Unused dependencies in `Package.swift`

There's no `cargo-machete` equivalent yet for Swift; the manual sweep is:

```bash
# 1. List declared dependencies
swift package show-dependencies --format json | jq '.dependencies[].identity'

# 2. For each declared dep, grep for `import <ModuleName>` in Sources/
for dep in $(swift package show-dependencies --format json | jq -r '.dependencies[].identity'); do
  if ! grep -r -l --include='*.swift' "import $dep" Sources/ > /dev/null; then
    echo "Candidate for removal: $dep"
  fi
done
```

False positives:
- Build-tool plugins (`.plugin(name:, package:)`) — used by SwiftPM commands, not via `import`.
- Macros declared with `.macro(name:targets:)` — consumed via `@Macro` attribute, not `import`.
- Resource-only dependencies — included for asset bundling.

### Dead package targets

```swift
// Package.swift
.target(name: "OldFeature", dependencies: ["..."])   // not in any product, never tested
```

Signal: no other target depends on it AND it's not in any `.library`/`.executable` product.

### `swift package show-dependencies --format tree`

Lists transitive deps. If you see a crate at multiple versions, consider unifying via `dependencies:` pinning.

### Package traits (Swift 6.1+)

Traits replace ad-hoc `Package.swift` conditional compilation. If a trait is declared but no other target enables it, it can be removed.

```swift
.package(url: "...", traits: ["MetricsBackend"])    // is "MetricsBackend" still used?
```

Search `.product(name:package:traits:)` callsites; if the trait is never selected, drop it.

---

## Feature Trait / `#if` Cleanup

### Stale `#if` blocks

```swift
#if EXPERIMENTAL_CACHE                  // feature renamed last year
private func experimentalPath() { /* dead */ }
#endif
```

Strip these in the same PR that removes the trait/build setting.

### Compile-time-only flags

```swift
#if canImport(UIKit)
import UIKit
#endif
```

If your minimum platform now always has `UIKit`, the `#if` is decorative — but leave it if you also build on Linux/server. Verify by reading `Package.swift` platforms.

### Build-config attributes that are always-on

```swift
#if DEBUG
let logger = ConsoleLogger()
#else
let logger = ConsoleLogger()           // identical body
#endif
```

Collapse to a single declaration.

### Deprecated `#if swift(>=...)`

```swift
#if swift(>=5.7)
// modern path
#else
// pre-5.7 fallback path that nobody runs
#endif
```

If your `swift-tools-version` already pins ≥5.7, the fallback is dead.

---

## Cleanup Workflow

Recommended ordering for a Swift cleanup pass:

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

- Bad-pattern catalog: [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md)
- Toolchain & libraries (2026 stack): [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md)
- Module system & access control: [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md) §11
- Cross-language tooling matrix: [`language-patterns.md`](./language-patterns.md)
