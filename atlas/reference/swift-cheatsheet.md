# Swift Architecture Cheatsheet (Swift 6.2+)

Purpose: Atlas-flavored slice of the Swift knowledge base — SwiftPM target architecture patterns, protocol-based DI, visibility hygiene, circular-dep detection, public-API surface management, and ADR triggers specific to Swift.

Baseline: **Swift 6.2+, Xcode 26, SwiftPM with `package` access level**.

Source of truth (do not duplicate here):
- Project structure & SwiftPM → [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md)
- Protocol design pitfalls → [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md) §4
- API design pitfalls → [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md) §7
- Module system, access control, ABI → [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md) §11

---

## Contents

- [SwiftPM Target Architecture Patterns](#swiftpm-target-architecture-patterns)
- [Protocol DI: Generic vs Existential](#protocol-di-generic-vs-existential)
- [Module Visibility Hygiene](#module-visibility-hygiene)
- [Circular Dependency Detection](#circular-dependency-detection)
- [God-Target Split Signals](#god-target-split-signals)
- [SwiftPM `Package.swift` Patterns](#swiftpm-packageswift-patterns)
- [Public API Surface Management](#public-api-surface-management)
- [Refactoring Playbooks](#refactoring-playbooks)
- [ADR Triggers Specific to Swift](#adr-triggers-specific-to-swift)
- [Architecture Anti-Patterns](#architecture-anti-patterns)

---

## SwiftPM Target Architecture Patterns

Three production patterns. Pick one per system; mixing causes layering chaos.

### Layered (Clean / Hexagonal)

Targets organized by architectural layer; dependencies flow one direction only.

```
MyApp/
├── Package.swift                # single package with multiple targets
├── Sources/
│   ├── Domain/                  # Pure value types + protocols; zero I/O
│   ├── Application/             # Use-cases composing Domain + ports
│   ├── AdapterPostgres/         # Implements Domain protocols via Postgres driver
│   ├── AdapterHTTP/             # Vapor / Hummingbird routes -> Application
│   └── App/                     # Thin executable target: wires adapters into Application
└── Tests/
    └── ApplicationTests/        # Tests with in-memory adapter
```

Dependency rule (enforced by SwiftPM target graph):

```
App ──> AdapterHTTP ──> Application ──> Domain
        AdapterPostgres ──> Application ──> Domain
```

`Domain` depends on **nothing inside the package**. Verify with `swift package show-dependencies --format json | jq`.

### Feature-Sliced (Bounded Contexts)

Top-level targets per bounded context; each target may itself follow hex/clean internally.

```
Sources/
├── Billing/         # has Domain/Application/Adapter submodules inside
├── Catalog/
├── Identity/
└── SharedKernel/    # cross-context primitives (Money, UserID)
```

Cross-context dependencies go via `SharedKernel` only. No `Billing → Catalog` direct edges.

### Single Library + Executable

Smallest pattern. Library target exposes API; `.executableTarget` holds entry points.

```swift
let package = Package(
    name: "MyTool",
    targets: [
        .target(name: "MyTool"),
        .executableTarget(name: "mytool", dependencies: ["MyTool"]),
        .executableTarget(name: "mytool-admin", dependencies: ["MyTool"]),
    ]
)
```

Use when:
- Project is one bounded context.
- Library is reusable as a dependency.
- ≤ ~20k LOC; growth past that should trigger a Layered split.

### Multi-Package Monorepo

When packages are independently versioned/published, split into separate `Package.swift` directories with `dependencies: [.package(path: "../OtherPackage")]`. Use when teams release independently. Adds CI cost; only do this past ~5 active teams.

---

## Protocol DI: Generic vs Existential

Two ways to inject a dependency through a protocol. Choose deliberately.

### Generic parameter (`<R: OrderRepository>`)

```swift
public struct CreateOrderUseCase<R: OrderRepository> {
    let repo: R

    public func run(_ cmd: NewOrder) async throws -> Order { /* ... */ }
}
```

- **Compile-time monomorphized** (with whole-module optimization). Each `R` produces a separate optimized function.
- **Zero indirection** — direct call after specialization.
- **Cost**: binary-size growth (one copy per `R`), slower compile, error messages mention concrete types.
- **Use when**: hot path, the impl is known at the call site, you need `R.AssociatedType` to vary, the protocol has `associatedtype` requirements.

### Opaque parameter (`some Protocol`, Swift 5.7+)

```swift
public struct CreateOrderUseCase {
    let repo: some OrderRepository
    // ^ requires init-time concrete; less useful for DI but very useful for return types
}
```

`some` works best on **return types** to hide the concrete type. As a stored property, it pins one specific concrete type.

### Existential (`any Protocol`)

```swift
public struct CreateOrderUseCase {
    let repo: any OrderRepository

    public func run(_ cmd: NewOrder) async throws -> Order { /* ... */ }
}
```

- **Runtime dispatch** via existential container (vtable + value witness).
- **One function body** regardless of how many impls exist — smaller binary, faster compile.
- **Cost**: ~ns-scale dispatch overhead, existential limitations (no `Self` requirements, no `static` requirements, limits with `associatedtype` — though Swift 5.7+ relaxed many).
- **Use when**: composition root with N impls, plugin registry, less perf-critical layers, the protocol is `dyn`-clean.

### Decision matrix

| Scenario | Choose |
|----------|--------|
| 1 impl in prod, 1 fake in tests | Either; `any` is fewer angle brackets |
| Hot path (>100k calls/sec) | Generic `<R>` |
| Protocol has `associatedtype` (`Element`, `Failure`) | Generic, unless you use Swift 5.7+ constrained existentials |
| Plugin registry (`[String: any Renderer]`) | `any` (only option) |
| Protocol has `static func make() -> Self` | `any` is impossible — must be generic |
| Cross-module, library exposes the protocol | Provide both via free function or use `any` for ergonomics |

For full guidance, see best-practices §6 (Architecture) and anti-patterns §4 (Protocol design).

---

## Module Visibility Hygiene

Swift 6.2's six-rung visibility ladder. Use the tightest that compiles.

| Modifier | Reachable from |
|----------|----------------|
| `private` | Same scope only (and same-file extensions) |
| `fileprivate` | Same file |
| `internal` (default) | Same module |
| `package` (5.9+) | Same SwiftPM package (across targets) |
| `public` | Any module that imports this one — but CANNOT be subclassed/overridden |
| `open` | Public AND subclassable/overridable from outside the module |

### `package` is the underused middle ground

```swift
// Before — leaking implementation detail via `public` to share across targets
public struct OrderInternals { /* used by AdapterPostgres + Application, not by App consumers */ }

// After (5.9+)
package struct OrderInternals { /* only visible inside the SwiftPM package */ }
```

`package` is the right level for "cross-target internal." Reach for `public` only when you publish to other Swift packages.

### Façade pattern with `@_exported import` (use sparingly)

```swift
// Sources/MyAppFacade/MyAppFacade.swift
@_exported import Application
@_exported import Domain
// Consumer just writes: import MyAppFacade
```

`@_exported` is underscored (semi-private), but it's the only way to re-export modules. Use for top-level library entry points; avoid in app code.

### Sealed protocol pattern (prevent downstream impls)

```swift
public protocol Renderer {
    static var sealed: Sealed { get }    // sentinel only this module can satisfy
    func render(_ doc: Doc) -> Output
}

public struct Sealed { fileprivate init() {} }

// Only this module can conform — `Sealed` has a fileprivate init.
public struct SVGRenderer: Renderer {
    public static let sealed = Sealed()
    public func render(_ doc: Doc) -> Output { /* ... */ }
}
```

Use when:
- You want forward-compat freedom to add methods (no breaking-change risk from downstream impls).
- The protocol represents a closed enumeration of behaviors.

### Visibility audit signal

If `xcrun swift-symbolgraph-extract` shows items you didn't mean to expose, tighten visibility before the next release.

---

## Circular Dependency Detection

Swift does **not** allow circular target dependencies at compile time, but circular file/module dependencies inside a target AND logical circularity (A's protocol, impl-in-B, B calls A) can still emerge.

### Tools

| Tool | Scope | Use For |
|------|-------|---------|
| `swift package show-dependencies --format dot` | Workspace package graph | Visualize package edges |
| `swift package dump-package` | Single package target graph (JSON) | Programmatic dep analysis |
| Xcode "Target Dependencies" build phase | Per-target | Catches Xcode-project-level cycles |
| Periphery | Code-level cross-target unused/circular | Useful for finding hidden coupling |
| `swift-package-list` plugin | List target deps in CI | Enforce "Domain depends on nothing" rules |

Example:

```bash
swift package show-dependencies --format dot | dot -Tsvg > deps.svg
swift package dump-package | jq '.targets[] | {name, dependencies}'
```

### Common circular smells in Swift

1. **App → Adapter → App via delegate callback.** The Adapter layer calls back into Application services through a registered delegate. Fix: invert — protocol owned by Application, Adapter implements it.

2. **Target A re-exports types from Target B, while Target B uses protocols defined in Target A.** Compiles but creates "if you import either, you import both" coupling. Fix: move shared types into a `SharedKernel` / `Common` target.

3. **File cycle inside a target**: `OrderService.swift` uses types from `OrderModel.swift` which uses types from `OrderService.swift`. Swift allows it within one target but muddies reasoning. Fix: extract shared types into a parent or sibling file/module.

4. **Test code reaching into production via `@testable import` shortcuts that grow into a backdoor.** Fix: define a clean test-only API explicitly; don't rely on `internal` shortcuts.

---

## God-Target Split Signals

When a single target becomes a kitchen sink, productivity collapses. Signals worth a split:

- **Compile time > 60s** for a clean incremental rebuild of one target.
- **`dependencies:` array has > 8 entries** suggesting bundled concerns.
- **Package contains exactly one target** + tests — the package is a fiction.
- **Library API surface mixes unrelated bounded contexts** (e.g., `Billing.Charge` and `Catalog.Product` in the same target).
- **A single file > 2000 LOC** without natural sub-files.
- **PRs from different teams routinely touch the same target** — change ownership is unclear.
- **DocC generation takes > 30s** — too many concerns documented at once.

Splitting playbook → see [Refactoring Playbooks](#refactoring-playbooks).

---

## SwiftPM `Package.swift` Patterns

### Modern minimal `Package.swift`

```swift
// swift-tools-version: 6.2
let package = Package(
    name: "Widgets",
    platforms: [.macOS(.v14), .iOS(.v17)],
    products: [.library(name: "Widgets", targets: ["Widgets"])],
    targets: [
        .target(name: "Domain", swiftSettings: [
            .enableUpcomingFeature("InternalImportsByDefault"),
            .enableUpcomingFeature("ExistentialAny"),
        ]),
        .target(name: "Application", dependencies: ["Domain"]),
        .target(name: "AdapterPostgres", dependencies: ["Application"]),
        .target(name: "Widgets", dependencies: ["Application", "AdapterPostgres"]),
        .testTarget(name: "ApplicationTests", dependencies: ["Application"]),
    ],
    swiftLanguageVersions: [.v6]
)
```

### Package Traits (Swift 6.1+)

Traits are SwiftPM's answer to Cargo features. Declare `traits:` at the package level and gate code via `.define("FLAG", .when(traits: ["TraitName"]))` in `swiftSettings`. Use traits instead of ad-hoc `#if` for compile-time variants.

### `swiftSettings:` upcoming features

Adopt new defaults proactively:

| Setting | What it does |
|---------|--------------|
| `InternalImportsByDefault` | `import Foo` becomes `internal import Foo`; tightens export surface |
| `ExistentialAny` | Requires `any` keyword on existential types (Swift 6.0+ default but warning-only in 5.x) |
| `IsolatedDefaultValues` | Property default initializers run in isolation context |
| `StrictConcurrency` (experimental) | Treat data-race issues as errors (now default in 6.0) |

---

## Public API Surface Management

### Symbol graphs

```bash
xcrun swift-symbolgraph-extract \
  -module-name Widgets \
  -target arm64-apple-macos14 \
  -output-dir symbolgraphs/ \
  -I .build/debug
```

The emitted `.symbols.json` is your public-API contract. Diff between releases to detect surface changes.

### `swift package diagnose-api-breaking-changes` (libraries only)

```bash
swift package diagnose-api-breaking-changes <previous-tag>
```

Catches:
- Removed `public` symbols.
- Changed function signatures.
- Removed enum cases (if not `@frozen`-protected).

CI integration: block PRs whose diff is non-empty without a version bump justification.

### `@frozen` and `@unknown default` discipline

```swift
@frozen public enum AppError: Error {
    case notFound
    case conflict
    // ABI-frozen: cannot add new cases without major version bump.
}

public enum AppEvent {
    case userLoggedIn
    case userLoggedOut
    // NOT @frozen: adding new cases is a minor-version-safe change for resilient libraries.
}

// Downstream MUST handle:
switch event {
case .userLoggedIn: ...
case .userLoggedOut: ...
@unknown default: ...   // forward-compat for non-frozen enums
}
```

Apply `@frozen` only to enums whose case list is genuinely closed. For evolving enums, leave non-frozen and document that consumers must use `@unknown default`.

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

## Refactoring Playbooks

### Strangler-Fig: replace legacy impl behind a trait

```swift
// Package.swift traits:
traits: [
    .trait(name: "NewRenderer"),
    .default(enabledTraits: []),     // default off — opt-in
]

// Sources/Renderer/Renderer.swift
#if WIDGETS_NEW_RENDERER
public typealias DefaultRenderer = V2.SVGRenderer
#else
public typealias DefaultRenderer = V1.SVGRenderer
#endif
```

Phases:
1. Ship `NewRenderer` opt-in.
2. Make `NewRenderer` enabled by default; keep the legacy path available.
3. Remove the legacy path in the next major release.

### Branch by Abstraction

1. Introduce a protocol abstracting the operation.
2. Both old impl and new impl satisfy the protocol.
3. Inject via DI at the composition root.
4. Swap default impl. Old impl is now deletable.

### Target Split Protocol

Splitting one target into two (e.g., `Widgets` → `WidgetsCore` + `WidgetsCLI`):

1. **Create the new target** in `Package.swift`: `.target(name: "WidgetsCore")`.
2. **Move source files** physically: `git mv Sources/Widgets/Core/*.swift Sources/WidgetsCore/`.
3. **Add the new target as a dependency** of the old one: `.target(name: "Widgets", dependencies: ["WidgetsCore"])`.
4. **Adjust visibility**: items that crossed the old file boundary as `internal` must now be `public` or `package`. Prefer `package` for cross-target internals.
5. **Re-export for source compat during transition**: `@_exported import WidgetsCore` in `Widgets.swift`.
6. **Update tests** to target the new module.
7. **Fix DocC** — symbol graph paths change.
8. **Update CI** to test both targets independently if they have separate test targets.
9. **Verify**: `swift build`, `swift test`, symbol-graph diff.

### Inverting a Circular Dependency

```
Before:  App ─uses─> Adapter ─delegate─> App   (logical cycle via callback)
After:   Domain (defines protocol P)
         App     ─uses─> Domain
         Adapter ─impls─> P (from Domain)
         App     ─composes─> Adapter at startup
```

Steps:
1. Extract the protocol into the lowest layer (`Domain` or `SharedKernel`).
2. Move the impl to `Adapter`, depending only on `Domain`.
3. Wire at `App`/executable target.
4. Delete the old direct edge from `Adapter` back to `App`.

---

## ADR Triggers Specific to Swift

Document the decision when one of these arises:

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

ADR format → use Scribe's `adr` recipe (Nygard or MADR). Atlas owns the architectural tradeoff analysis; Scribe authors the artifact.

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

For full anti-pattern catalog: [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md) §4 (Protocols) and §7 (API Design).

---

## Where to dig deeper

- Project structure & SwiftPM: [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md) §3, §4
- Domain architecture patterns: [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md) §6
- Protocol design pitfalls: [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md) §4
- API design pitfalls: [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md) §7
- Module system & access control: [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md) §11
- Approachable Concurrency (6.2): [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md) §3.11
