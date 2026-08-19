# Swift Architecture Cheatsheet (Swift 6.2+)
Purpose: Atlas-flavored slice of the Swift knowledge base — SwiftPM target architecture patterns, protocol-based DI, visibility hygiene, circular-dep detection, public-API surface management, and ADR triggers specific to Swift.
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Module Visibility Hygiene
| Modifier | Reachable from |
|----------|----------------|
| `private` | Same scope only (and same-file extensions) |
| `fileprivate` | Same file |
| `internal` (default) | Same module |
| `package` (5.9+) | Same SwiftPM package (across targets) |
| `public` | Any module that imports this one — but CANNOT be subclassed/overridden |
| `open` | Public AND subclassable/overridable from outside the module |
- **`package` is the underused middle ground**
- **Façade pattern with `@_exported import` (use sparingly)**
### Sealed protocol pattern (prevent downstream impls)
- You want forward-compat freedom to add methods (no breaking-change risk from downstream impls).
- The protocol represents a closed enumeration of behaviors.
- **Visibility audit signal**
---
## Circular Dependency Detection
### Tools
| Tool | Scope | Use For |
|------|-------|---------|
| `swift package show-dependencies --format dot` | Workspace package graph | Visualize package edges |
| `swift package dump-package` | Single package target graph (JSON) | Programmatic dep analysis |
| Xcode "Target Dependencies" build phase | Per-target | Catches Xcode-project-level cycles |
| Periphery | Code-level cross-target unused/circular | Useful for finding hidden coupling |
| `swift-package-list` plugin | List target deps in CI | Enforce "Domain depends on nothing" rules |
### Common circular smells in Swift
1. **App → Adapter → App via delegate callback.** The Adapter layer calls back into Application services through a registered delegate. Fix: invert — protocol owned by Application, Adapter implements it.
2. **Target A re-exports types from Target B, while Target B uses protocols defined in Target A.** Compiles but creates "if you import either, you import both" coupling. Fix: move shared types into a `SharedKernel` / `Common` target.
3. **File cycle inside a target**: `OrderService.swift` uses types from `OrderModel.swift` which uses types from `OrderService.swift`. Swift allows it within one target but muddies reasoning. Fix: extract shared types into a parent or sibling file/module.
4. **Test code reaching into production via `@testable import` shortcuts that grow into a backdoor.** Fix: define a clean test-only API explicitly; don't rely on `internal` shortcuts.
---
## God-Target Split Signals
- **Compile time > 60s** for a clean incremental rebuild of one target.
- **`dependencies:` array has > 8 entries** suggesting bundled concerns.
- **Package contains exactly one target** + tests — the package is a fiction.
- **Library API surface mixes unrelated bounded contexts** (e.g., `Billing.Charge` and `Catalog.Product` in the same target).
- **A single file > 2000 LOC** without natural sub-files.
- **PRs from different teams routinely touch the same target** — change ownership is unclear.
- **DocC generation takes > 30s** — too many concerns documented at once.
---
## SwiftPM `Package.swift` Patterns
- **Modern minimal `Package.swift`**
- **Package Traits (Swift 6.1+)**
### `swiftSettings:` upcoming features
| Setting | What it does |
|---------|--------------|
| `InternalImportsByDefault` | `import Foo` becomes `internal import Foo`; tightens export surface |
| `ExistentialAny` | Requires `any` keyword on existential types (Swift 6.0+ default but warning-only in 5.x) |
| `IsolatedDefaultValues` | Property default initializers run in isolation context |
| `StrictConcurrency` (experimental) | Treat data-race issues as errors (now default in 6.0) |
---
## Public API Surface Management
- **Symbol graphs**
### `swift package diagnose-api-breaking-changes` (libraries only)
- Removed `public` symbols.
- Changed function signatures.
- Removed enum cases (if not `@frozen`-protected).
- **`@frozen` and `@unknown default` discipline**
### Version-bump rules of thumb (SemVer)
| Change | SemVer impact |
|--------|---------------|
| Add a `public` symbol | minor |
| Add an enum case to a non-`@frozen` enum | minor (with `@unknown default` requirement) |
| Add an enum case to a `@frozen` enum | major |
| Add a requirement to a public protocol | major (downstream conformers break) — unless protocol is sealed |
| Add a default-implemented requirement to a public protocol | minor |
| Raise platform minimum version | major; major+CHANGELOG |
| Remove or rename anything `public` | major |
---
## ADR Triggers Specific to Swift
- **Async runtime / server framework.** Vapor (Tokio-equivalent maturity) vs Hummingbird (NIO-direct, lighter) vs Smoke. Each affects extractors, middleware, and team ramp.
- **Default isolation adoption (Swift 6.2).** Whether to adopt `nonisolated(nonsending)` as the package default, per-target opt-in, or stick with current isolation. Affects every concurrency annotation in the codebase.
- **Embedded Swift adoption.** Whether to target Embedded Swift for a subset of the codebase (microcontrollers, kernel modules) — significant subset-of-Swift restrictions, no ARC by default, no `String`.
- **C++ interop adoption.** Whether to import C++ directly (Swift 5.9+, refined 6.2). Cost: build complexity; ABI brittleness.
- **SwiftUI vs UIKit vs AppKit** as primary UI framework (or hybrid). Affects testability strategy and concurrency model significantly.
- **`@Observable` vs `ObservableObject`** migration cadence — moving wholesale is a big diff; running both is bridge code.
- **SwiftPM vs CocoaPods vs Carthage.** CocoaPods is in maintenance mode in 2026; new projects should default to SwiftPM. Document if you stay on CocoaPods.
- **Library Evolution adoption.** Enabling `-enable-library-evolution` adds ABI stability guarantees but limits inlining; required for OS-included frameworks, optional otherwise.
- **MSRV (minimum Swift version) policy.** "Latest stable" vs "Stable - 1" vs "Pinned to Xcode N". Affects which language features the team may adopt.
- **Swift Testing vs XCTest** migration timing. Swift Testing is the new default but XCTest remains supported; mixed strategy works.
- **Error strategy.** Untyped `throws` vs typed `throws(E)` (6.0+) vs `Result<T, E>` vs domain-specific error monad. Once chosen for an API surface, hard to change.
- **Build system.** Pure SwiftPM vs Xcode project vs Bazel. Bazel cost is high; only when monorepo with multi-language.
---
## Architecture Anti-Patterns
| Anti-pattern | Why it hurts | Better path |
|--------------|--------------|-------------|
| **God Package**: one package, 100k LOC, all concerns inside | Compile times explode; PRs collide; module boundaries are advisory; consumers must accept all targets | Layered or feature-sliced split with `package` access for cross-target internals |
| **One-target package**: `Package.swift` declares exactly one target plus tests | The package is a fiction; refactor-friction signals more targets are warranted | Split into Domain/Application/Adapter targets the day the package crosses 5k LOC |
| **Reflexive `public` for everything** | Public is the most expensive access level — every change is breaking | Use `internal` (default), `package` for cross-target, `public` only when crossing the package boundary |
| **`@_exported import` everywhere as "convenience"** | Downstream couples to internal target structure; refactor cost is downstream cost | Curated façade target with explicit `public` re-exports |
| **Force-unwrap-driven module boundaries** | `let x = SomeModule.shared!.foo!` chains hide the actual contract; refactor breaks runtime | Constructor injection across module seams; `!` is a signal you skipped designing the boundary |
| **Protocols added "for testability" with one impl** | Indirection without benefit; doubles the codebase; obscures the actual call graph | Introduce the protocol only when ≥ 2 impls exist (prod + fake) or polymorphism need emerges |
| **Mixed Library Evolution settings across same product** | ABI dance between targets; inlining suppressed unnecessarily | Decide library-evolution per-product; document in ADR |
| **`@MainActor` on the top-level App + every type** | Serializes the whole app on the UI thread; performance ceiling locked low | Per-method `@MainActor` for UI sync points; `nonisolated` everywhere else |
| **Hilt-style "everything is `Arc<Mutex<T>>`" via `final class` + `@MainActor`** | Hides ownership design; UI thread contention | Actors, structured concurrency, value types where possible |
| **Mixing Combine + Swift Concurrency + closures in the same layer** | Three concurrency models per file means three sets of bugs | Pick one per layer; bridge at the boundary only |
