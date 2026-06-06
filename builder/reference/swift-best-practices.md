# Swift Best Practices — Deep Dive Reference

> Companion to the broader Swift knowledge in this `builder/reference/` directory. This file covers best practices and what-to-use for Swift the language across iOS, macOS, server-side, and embedded. The `native` skill complements this for SwiftUI / Liquid Glass / iOS-platform-specific concerns.
>
> Baseline: Swift 6.2+ / Xcode 26 (as of 2026-05). Field-A flagged Swift 6.3 (Mar 2026) outlook where relevant.

---

## Table of Contents

1. [Swift API Design Guidelines (Full)](#1-swift-api-design-guidelines-full)
2. [Concurrency Best Practices (Swift 6.2 Era)](#2-concurrency-best-practices-swift-62-era)
3. [Error Handling Patterns](#3-error-handling-patterns)
4. [Modules & Package Design](#4-modules--package-design)
5. [Testing Strategy](#5-testing-strategy)
6. [Performance](#6-performance)
7. [Memory Hygiene](#7-memory-hygiene)
8. [Server-Side Swift](#8-server-side-swift)
9. [Production Library Matrix (2026)](#9-production-library-matrix-2026)
10. [Embedded Swift](#10-embedded-swift)
11. [Cross-Platform Packaging](#11-cross-platform-packaging)
12. [Documentation (DocC)](#12-documentation-docc)
13. [2023→2026 Migration Cheatsheet](#13-20232026-migration-cheatsheet)
14. [Sources](#sources)

> **Cross-links:**
> - Canonical language semantics, type system, concurrency model details → [`swift-language-spec.md`](./swift-language-spec.md)
> - Concrete misuse of each practice (`@unchecked Sendable`, force-unwrap families, actor reentrancy bugs, allocation traps) → [`swift-anti-patterns.md`](./swift-anti-patterns.md)
> - SwiftUI / Liquid Glass / iOS HIG / Apple Intelligence / Foundation Models → [`../../native/SKILL.md`](../../native/SKILL.md)

---

## 1. Swift API Design Guidelines (Full)

Authoritative source: <https://www.swift.org/documentation/api-design-guidelines/>. This is the canonical Apple-blessed style for any Swift code intended for reuse.

### 1.1 Fundamentals

- **Clarity at the point of use is the most important goal.** APIs are declared once but used many times. Optimize for the call site, not the declaration site.
- **Clarity is more important than brevity.** Compact code is a side effect of Swift's type system, never a goal.
- **Write a documentation comment for every declaration.** "If you are having trouble describing your API's functionality in simple terms, you may have designed the wrong API." Use single-sentence summary ending with a period, then paragraphs. Use markdown and symbol commands (`- Parameter`, `- Returns`, `- Throws`, `- Note`, `- Precondition`, `- Postcondition`, `- Complexity`).

```swift
/// Returns a "view" of `self` containing the same elements in
/// reverse order.
///
/// - Complexity: O(1)
func reversed() -> ReverseCollection
```

### 1.2 Naming — Promote Clear Usage

**Include all necessary words to avoid ambiguity.**

```swift
// Bad — Ambiguous (remove which x?)
employees.remove(x)

// Good — Clear
employees.remove(at: x)
```

**Omit needless words.** Every word should carry meaning at the use site. Avoid repeating type info already on the parameter.

```swift
// Bad
public mutating func removeElement(_ member: Element) -> Element?
allViews.removeElement(cancelButton)

// Good
public mutating func remove(_ member: Element) -> Element?
allViews.remove(cancelButton)
```

**Name variables, parameters, and associated types according to roles, not types.**

```swift
// Bad
var string = "Hello"
class ProductionLine { func restock(from widgetFactory: WidgetFactory) }

// Good
var greeting = "Hello"
class ProductionLine { func restock(from supplier: WidgetFactory) }
```

**Compensate for weak type information.** For `Any`, `NSObject`, `Int`, `String`, etc., precede with a noun describing role.

```swift
// Bad — vague
func add(_ observer: NSObject, for keyPath: String)
grid.add(self, for: graphics)

// Good — clear
func addObserver(_ observer: NSObject, forKeyPath path: String)
grid.addObserver(self, forKeyPath: graphics)
```

### 1.3 Naming — Strive for Fluent Usage

Method names should read as grammatical English phrases at the use site:

```swift
x.insert(y, at: z)            // "x, insert y at z"
x.subviews(havingColor: y)    // "x's subviews having color y"
x.capitalizingNouns()         // "x, capitalizing nouns"
```

**Factory methods start with `make`:**

```swift
x.makeIterator()
factory.makeWidget(gears: 42, spindles: 14)
```

**First arguments of initializers and factory methods should not form a phrase with the base name.**

```swift
// Good
let foreground = Color(red: 32, green: 64, blue: 128)
let newPart = factory.makeWidget(gears: 42, spindles: 14)

// Bad
let foreground = Color(havingRGBValuesRed: 32, green: 64, andBlue: 128)
```

### 1.4 Side-Effects Govern Verb-vs-Noun

- **No side effects → noun phrase**: `x.distance(to: y)`, `i.successor()`.
- **Side effects → imperative verb**: `print(x)`, `x.sort()`, `x.append(y)`.

**Mutating / nonmutating pairs** must be named consistently:

| Pattern | Mutating | Nonmutating | Example |
|---------|----------|-------------|---------|
| Verb (no direct object) | imperative | past participle | `reverse()` / `reversed()` |
| Verb (direct object) | imperative | present participle | `stripNewlines()` / `strippingNewlines()` |
| Noun-natured | `form` prefix | bare noun | `formUnion(_:)` / `union(_:)` |

```swift
// noun-natured:
x = y.union(z)      // nonmutating
y.formUnion(z)      // mutating
```

### 1.5 Boolean Discipline

Boolean methods/properties read as assertions about the receiver:

```swift
x.isEmpty
line1.intersects(line2)
```

Boolean properties use `is`/`has`/`should`/`can`/`will` prefixes.

### 1.6 Protocol Naming

- **What something IS** → use a noun: `Collection`, `Sequence`.
- **What something CAN DO** → suffix `-able`, `-ible`, or `-ing`: `Equatable`, `Comparable`, `ProgressReporting`.

### 1.7 Argument-Label Conventions

**Omit labels** when arguments can't be usefully distinguished (typically same-type peers):

```swift
min(number1, number2)
zip(sequence1, sequence2)
```

**Value-preserving initializers** omit the first label:

```swift
extension String { init(_ x: BigInt, radix: Int = 10) }
text += String(veryLargeNumber, radix: 16)
```

**Narrowing conversions** require descriptive labels (`truncating:`, `saturating:`, etc.) — the conversion is lossy and the user must opt into a strategy.

**Prepositional first labels** must begin at the preposition (`from:`, `with:`, `for:`, `of:`, `in:`, `at:`, `having…:`):

```swift
x.removeBoxes(havingLength: 12)
view.dismiss(animated: false)
```

**Exception**: when two args form one abstraction (e.g., 2D coordinates), the preposition attaches to the base name:

```swift
a.moveTo(x: b, y: c)
a.fadeFrom(red: b, green: c, blue: d)
```

**Default-valued parameters always have labels** because they can be omitted; place them toward the end of the parameter list.

### 1.8 Types vs. Initializers

Initializers convert from another representation: `String(42)`. Factories `make…` are the alternative when a richer abstraction is appropriate (e.g., the type wants name dispatch instead of label-only dispatch).

### 1.9 Special Cases

- **Tuple members and closure parameters** should be labeled — they appear in documentation and improve readability.
- **Unconstrained generics** (`Element == Any`) need extra-clear overload sets to avoid ambiguity. Use `contentsOf:` when consuming a sequence.

```swift
public mutating func append<S: Sequence>(contentsOf newElements: S)
    where S.Element == Element
```

### 1.10 File Reference Macros

For diagnostics or logging:

- `#fileID` — production-recommended (compact, privacy-preserving).
- `#filePath` — full path, for development tooling only.
- `#file` — legacy Swift 5.2-and-earlier compatibility.

---

## 2. Concurrency Best Practices (Swift 6.2 Era)

Swift 6.2 (Sep 2025) introduced **Approachable Concurrency** — the largest concurrency UX change since Swift 5.5. Swift 6.3 (Mar 2026) consolidates it. For canonical language semantics see [`swift-language-spec.md` §3](./swift-language-spec.md#3-concurrency-model).

### 2.1 Decision Tree: When to Use What

| Need | Choose | Rationale |
|------|--------|-----------|
| Shared mutable state accessed asynchronously | `actor` | Async serial access, no manual locks |
| Shared mutable state accessed synchronously | `Mutex<T>` (Synchronization) | Stdlib lock, no `async` needed |
| Pure value with no identity, crossable | `Sendable struct` | Best — no synchronization needed |
| All UI / view-model code | `@MainActor` | Single executor, no surprises |
| Per-domain global state | custom `@globalActor` | Used sparingly; usually `actor` is enough |
| Bridging old completion-handler API | `withCheckedContinuation` / `withCheckedThrowingContinuation` | Standard adapter |
| Fan-out over a collection | `withTaskGroup` / `withThrowingTaskGroup` | Structured, cooperative cancellation |
| Bounded stream of events | `AsyncSequence` / `AsyncStream` | Standard library, type-safe |

### 2.2 Approachable Concurrency (SE-0466 + Default Isolation)

New Xcode 26 projects default the `defaultIsolation` build setting to `MainActor`. Module-wide declarations become `@MainActor` unless explicitly `nonisolated`.

- **New projects**: opt in. Removes ~80% of "spurious" Sendable warnings for typical UI apps.
- **Existing projects**: opt-in deliberately. Mass `@MainActor` inference can hide latent threading bugs and silently move work to the main thread.

Per-package or per-target via `Package.swift`:

```swift
.target(
    name: "MyKit",
    swiftSettings: [
        .defaultIsolation(MainActor.self),         // Swift 6.2+
        .swiftLanguageMode(.v6),
    ]
)
```

Per Donny Wals's module-type rule of thumb:

| Module type | Opt-in to MainActor default? |
|-------------|-------------------------------|
| **App target** (UI-heavy) | Yes — eliminates most isolation warnings, write concurrent code explicitly |
| **UI package** | Yes — everything is MainActor anyway |
| **Networking / data / domain package** | No — design as Sendable values + actors |
| **Reusable library / SDK** | No — caller decides isolation |

Opting in does NOT remove the need to think about concurrency — it changes the **default direction**. With it on, mark async work as `@concurrent` to explicitly hop off main.

### 2.3 `@concurrent` — Explicit Background Work

In Swift 6.2, `nonisolated async` functions **inherit caller isolation** by default (SE-0461). To explicitly hop to the global concurrent executor, use `@concurrent`:

```swift
@concurrent
nonisolated func heavyParse(_ data: Data) async throws -> Report {
    // Always runs on the global concurrent executor,
    // regardless of caller isolation.
}
```

Rules:

- Only valid on `nonisolated` functions.
- Not valid with global actors or custom isolation.
- Use sparingly — most calls should inherit isolation for predictability.

### 2.4 Region-Based Isolation (SE-0414) & `sending` (SE-0430)

Region-based isolation lets the compiler reason that a non-`Sendable` value has only one owner at a time, so it can safely cross isolation boundaries without conformance.

```swift
// Before SE-0414: compile error unless Profile is Sendable.
// In Swift 6: legal — `profile` is the only reference in this region.
let profile = Profile()
profile.populate()
await db.save(profile)        // "sent" into actor
// Using `profile` here would warn — region transferred.
```

The `sending` keyword marks a parameter as transferring ownership across an isolation boundary:

```swift
// Standard library:
public func withCheckedContinuation<T>(
    function: String = #function,
    _ body: (CheckedContinuation<T, Never>) -> Void
) async -> sending T
```

Use `sending` for APIs that accept non-Sendable values that the caller relinquishes. Common for: builders, factory closures, parser results, decoded objects.

### 2.5 `actor` vs `class` + Lock — Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| Async caller, async-safe API | `actor` |
| Sync caller cannot await | `class` + `Mutex<T>` |
| Need re-entrancy control | Custom executor + `actor` |
| Read-mostly with rare writes | `class` + `OSAllocatedUnfairLock` or `Mutex` with a snapshot pattern |
| State is read-only after init | `let` on a `Sendable` value |

Avoid double-jumping through `actor` for synchronous-only code paths; `Mutex<T>` is faster and clearer.

### 2.6 `Mutex<T>` & Synchronization Framework (Swift 6.0)

```swift
import Synchronization

final class Counter: Sendable {
    private let value = Mutex<Int>(0)

    func increment() {
        value.withLock { $0 += 1 }
    }

    var current: Int { value.withLock { $0 } }
}
```

Backed by `os_unfair_lock` (Darwin), `futex` (Linux), `SRWLOCK` (Windows). Generic constraint `~Copyable` enforces single ownership. Use when you need synchronous access without `await`.

`Atomic<Int>` and friends are available via the same `Synchronization` module for lock-free counters and flags.

### 2.7 Structured Concurrency Over Unstructured `Task { }`

Rules:

- Prefer `async let` and `withTaskGroup` over `Task { }` whenever the lifetime is bounded by a parent.
- Unstructured `Task { }` is for "fire-and-forget" — analytics, background save — but always store the handle if you need cancellation.
- `Task.detached` only when truly orphaned (logging, crash reporter, deferred cleanup).
- `withDiscardingTaskGroup` (Swift 5.9+) when child task results aren't needed — frees memory eagerly.

```swift
// Bad — unstructured leak risk
func loadAll(ids: [UUID]) async -> [User] {
    var users: [User] = []
    for id in ids {
        Task { users.append(await load(id)) }  // race + no cancellation
    }
    return users
}

// Good — structured fan-out
func loadAll(ids: [UUID]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask { try await load(id) }
        }
        return try await group.reduce(into: []) { $0.append($1) }
    }
}
```

### 2.8 Cancellation Propagation

- Cancellation is **cooperative**. Tasks aren't killed; they receive a signal.
- Check at safe points: `try Task.checkCancellation()` or `Task.isCancelled`.
- `URLSession`, `AsyncSequence` iteration, and most stdlib `async` APIs check automatically.
- Use `addTaskUnlessCancelled` in groups to avoid scheduling new work after cancellation.

```swift
func longProcess() async throws -> Result {
    for chunk in chunks {
        try Task.checkCancellation()
        try await process(chunk)
    }
    return finalize()
}
```

### 2.9 `AsyncSequence` Adoption

For 2026 net-new code, prefer `AsyncSequence`/`AsyncStream` over `Combine` publishers (Combine is in long-term maintenance and Apple has not extended it for Swift Concurrency). `swift-async-algorithms` fills the gap left by Combine's operators:

```swift
import AsyncAlgorithms

// Debounced search:
for await query in searchInput.values.debounce(for: .milliseconds(300)) {
    try await search(query)
}
```

### 2.10 Avoiding Actor Reentrancy Bugs

Actors are **reentrant**: an `await` inside an actor method can interleave with other actor methods. Common bug pattern:

```swift
actor Cache {
    private var value: Value?

    func load() async -> Value {
        if let value { return value }
        let fetched = await api.fetch()   // suspension!
        value = fetched                    // may overwrite a concurrent load
        return fetched
    }
}
```

Fixes:

1. **Snapshot before suspending** — cache an in-flight `Task` so concurrent callers share it.
2. **Use `nonisolated(unsafe)`** for known-pure state, then guard with an explicit lock.
3. **Add an internal `Task` registry** — classic single-flight pattern.

```swift
actor Cache {
    private var inflight: [Key: Task<Value, Error>] = [:]

    func load(_ key: Key) async throws -> Value {
        if let task = inflight[key] { return try await task.value }
        let task = Task<Value, Error> { try await api.fetch(key) }
        inflight[key] = task
        defer { inflight[key] = nil }
        return try await task.value
    }
}
```

See [`swift-anti-patterns.md` §3](./swift-anti-patterns.md#3-concurrency-pitfalls-swift-62-era) for the full catalog of concurrency anti-patterns and runtime traps.

---

## 3. Error Handling Patterns

### 3.1 `throws` vs `Result` vs `Optional`

| Use case | Choice | Why |
|----------|--------|-----|
| Sync function may fail with rich info | `throws` | Idiomatic, integrates with `try`/`do-catch` |
| Async return needs error in non-throwing context (e.g., `Combine`, callbacks) | `Result<T, E>` | Concrete value, no `try` needed |
| "Absence" is normal and not an error | `Optional<T>` | Don't conflate `nil` with failure |
| Multiple errors per call (validation aggregation) | `Result<[T], [Error]>` or custom | `throws` is single-error |

Anti-pattern: returning `Result` from a `throws` function. Pick one.

### 3.2 Typed Throws (Swift 6.0+) — When Worth It

Syntax: `func foo() throws(MyError) -> Bar`. For canonical language semantics see [`swift-language-spec.md` §6.2](./swift-language-spec.md#62-typed-throws-se-0413-stable-in-swift-60).

**Use typed throws when:**

- The error type is a **closed enum** the caller must exhaustively handle.
- The function is performance-sensitive and the caller benefits from monomorphization (typed throws avoid existential boxing).
- Public library API where error types are a stable part of the contract.
- Embedded Swift — `any Error` boxing is expensive in constrained environments.

**Skip typed throws when:**

- The error set is open / unbounded (e.g., catches anything from `URLSession`, `JSONDecoder`, etc.) — `throws` (= `throws(any Error)`) is more flexible.
- Inner errors may evolve across versions — locked-in typed throws becomes a breaking change.
- Async functions that aggregate many child errors — typically the union is `any Error`.

Apple's own recommendation: **untyped `throws` is still the default**. Use typed throws as a sharpening tool, not a default.

```swift
// Good — closed enum, worth typing
enum PINEntryError: Error {
    case tooShort, tooLong, invalidCharacters
}

func validatePIN(_ pin: String) throws(PINEntryError) -> PIN {
    if pin.count < 4 { throw .tooShort }
    if pin.count > 8 { throw .tooLong }
    if pin.contains(where: { !$0.isNumber }) { throw .invalidCharacters }
    return PIN(pin)
}

// Call site — exhaustive catch by construction:
do {
    let pin = try validatePIN(input)
} catch .tooShort, .tooLong {
    showError("PIN must be 4-8 digits")
} catch .invalidCharacters {
    showError("PIN must be numeric")
}
```

### 3.3 Error Hierarchies — One Enum per Service/Module

The recommended pattern is **one error enum per layer/service**, with explicit wrapping when boundaries are crossed:

```swift
enum NetworkError: Error {
    case offline
    case timeout
    case http(status: Int, body: Data?)
    case decoding(any Error)         // wraps lower-layer
}

enum FeatureError: LocalizedError {
    case network(NetworkError)
    case validation(String)
    case rateLimited(retryAfter: Duration)

    var errorDescription: String? {
        switch self {
        case .network(.offline): "You're offline. Reconnect and try again."
        case .network(.timeout): "Request took too long."
        case .network(.http(let status, _)): "Server returned \(status)."
        case .network(.decoding): "Unexpected response from the server."
        case .validation(let msg): msg
        case .rateLimited(let retry): "Try again in \(retry.formatted())."
        }
    }
}
```

Map between layers explicitly — the UI must never see raw `URLError` or `DecodingError`. This keeps internal changes from rippling outward.

### 3.4 `LocalizedError`, `RecoverableError`, `CustomNSError`

For user-facing errors on Apple platforms:

- **`LocalizedError`** — adds `errorDescription`, `failureReason`, `recoverySuggestion`, `helpAnchor`. Bridges to `NSError.localizedDescription` etc.
- **`RecoverableError`** — adds `recoveryOptions` and `attemptRecovery(optionIndex:)`. Used by AppKit for "Retry / Cancel" sheets.
- **`CustomNSError`** — adds stable `errorCode` and `errorDomain` for analytics (Sentry, Crashlytics).

A common production pattern:

```swift
enum APIError: LocalizedError, CustomNSError {
    case noConnection
    case unauthorized
    case serverError(statusCode: Int)

    static var errorDomain: String { "com.example.api" }
    var errorCode: Int {
        switch self {
        case .noConnection: 1001
        case .unauthorized: 1002
        case .serverError(let code): code
        }
    }
    var errorDescription: String? { /* localized */ }
}
```

### 3.5 The Four Audiences of Swift Errors

Per the Nonstrict article (2026), think about who reads each error:

1. **The compiler** — typed throws helps here.
2. **The catching code** — pattern-matchable cases.
3. **The end user** — `LocalizedError.errorDescription`.
4. **The developer in logs / crash reports** — `CustomDebugStringConvertible` + analytics fields.

Design each error type to serve all four; don't conflate them.

---

## 4. Modules & Package Design

### 4.1 `Package.swift` 6.0+ Manifest

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "MyKit",
    platforms: [
        .iOS(.v17), .macOS(.v14), .tvOS(.v17), .watchOS(.v10), .visionOS(.v1)
    ],
    products: [
        .library(name: "MyKit", targets: ["MyKit"]),
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-log.git", from: "1.6.0"),
        .package(url: "https://github.com/apple/swift-collections.git", from: "1.1.0"),
    ],
    targets: [
        .target(
            name: "MyKit",
            dependencies: [
                .product(name: "Logging", package: "swift-log"),
                .product(name: "Collections", package: "swift-collections"),
            ],
            swiftSettings: [
                .swiftLanguageMode(.v6),
                .defaultIsolation(MainActor.self),     // 6.2+ approachable
                .enableUpcomingFeature("ExistentialAny"),
                .enableUpcomingFeature("InternalImportsByDefault"),
            ]
        ),
        .testTarget(
            name: "MyKitTests",
            dependencies: ["MyKit"],
            swiftSettings: [.swiftLanguageMode(.v6)]
        ),
    ],
    swiftLanguageModes: [.v6]
)
```

Notes:

- `swiftLanguageVersions` is deprecated → use `swiftLanguageModes`.
- Per-target `.swiftLanguageMode(.v5)` lets you stage migration target-by-target.
- `swift-tools-version: 6.0` brings the new manifest API and `package` access level.

### 4.2 `package` Access Level (SE-0386, Swift 5.9+)

Five levels: `private` < `fileprivate` < `internal` < **`package`** < `public` < `open`.

- `package`-level symbols are visible to **other targets in the same `Package.swift`** but not externally.
- Solves the "I need to share between `Core` and `UI` targets without exposing to consumers" problem without ugly `@_spi` workarounds.
- The compiler passes `-package-name <id>` to enforce; the `packageAccess: true` flag is on by default.

```swift
// In target Core:
package struct InternalCache { /* ... */ }

// In target UI (same Package.swift): can use InternalCache.
// External consumer of the library: cannot.
```

### 4.3 Library Evolution & ABI

Apply only to **binary frameworks shipped to others** (mostly Apple's own SDKs). For first-party app code don't bother.

When you must:

- `@inlinable` — exposes the function body to importers' optimizer (cross-module specialization). Body becomes part of ABI.
- `@usableFromInline` — internal symbol visible to `@inlinable` consumers. ABI-public, source-internal.
- `@frozen` — declares a struct/enum's layout fixed. Adding cases is a breaking change.
- `@_implementationOnly import` (replaced by `internal import` in 6.0+) — hides dependency from the public ABI.

```swift
@inlinable
public func clamp<T: Comparable>(_ x: T, to range: ClosedRange<T>) -> T {
    @usableFromInline func _impl(_ x: T) -> T { /* … */ }
    return _impl(x)
}
```

**Implementation-only imports** (Swift 6.0+): `internal import Foo` keeps `Foo` symbols private to the module. Reduces public ABI surface, faster compile, no transitive leak.

### 4.4 Conditional Compilation

```swift
#if canImport(UIKit)
import UIKit
typealias PlatformImage = UIImage
#elseif canImport(AppKit)
import AppKit
typealias PlatformImage = NSImage
#endif

#if compiler(>=6.2)
// Use approachable-concurrency-only API
#endif

#if canImport(SwiftUI, _version: "5.0")
// Version-gated import (6.0+ supports version check)
#endif

#if os(Linux)
// Server-side only
#endif
```

Use `canImport(...)` over `os(...)` when the criterion is "does this framework exist?" — survives Apple porting frameworks across platforms.

### 4.5 Multi-Platform Package Layout

```
MyPackage/
├── Package.swift
├── Sources/
│   ├── MyCore/              # platform-neutral logic
│   ├── MyCoreApple/         # #if canImport(Darwin) extensions
│   └── MyCoreLinux/         # #if os(Linux) extensions
├── Tests/
│   └── MyCoreTests/
└── README.md
```

Conditional dependencies in `Package.swift`:

```swift
.target(
    name: "MyCore",
    dependencies: [
        .product(name: "Logging", package: "swift-log"),
        .product(
            name: "AsyncHTTPClient",
            package: "async-http-client",
            condition: .when(platforms: [.linux, .macOS])
        ),
    ]
)
```

---

## 5. Testing Strategy

### 5.1 Swift Testing vs XCTest — 2026 Default

**Default for new projects: Swift Testing** (`import Testing`, `@Test`, `#expect`). It's the official replacement.

| Capability | XCTest | Swift Testing |
|------------|--------|---------------|
| Test discovery | Subclass `XCTestCase` | `@Test` macro, any function |
| Assertion | `XCTAssertEqual(a, b)` | `#expect(a == b)` |
| Required precondition | `XCTUnwrap` | `try #require(value)` |
| Parameterization | Loops by hand | `@Test(arguments: …)` |
| Test grouping | Class boundaries | `@Suite` types |
| Parallelism | Process-per-test | In-process tasks (`.serialized` opt-out) |
| Concurrency | Awkward `@MainActor` | First-class `async`/`await`, default isolated to `nonisolated` |
| Conditional skip | `XCTSkip` | `.disabled(...)`, `.enabled(if:)` traits |
| Tags / filter | None | `@Tag` enums |
| Time-bounded | `XCTestExpectation` | `.timeLimit(.minutes(1))` trait |
| Async expectation | `XCTestExpectation.fulfill()` | `confirmation { ... }` |

### 5.2 Parameterized Tests with `arguments:`

```swift
import Testing

@Test("isEmail validates well-formed addresses",
      arguments: [
        "alice@example.com",
        "b@c.io",
        "user+tag@domain.co.uk",
      ])
func validEmails(_ input: String) {
    #expect(EmailValidator.isValid(input))
}

@Test(arguments: zip(["12", "ab12", "abcd"],
                     [false, false, true]))
func passwordStrength(input: String, expected: Bool) {
    #expect(PasswordValidator.isStrong(input) == expected)
}

// Cartesian product (2x3 = 6 invocations):
@Test(arguments: [Locale.en_US, Locale.ja_JP],
                 [CurrencyCode.usd, .jpy, .eur])
func formatCurrency(locale: Locale, currency: CurrencyCode) async {
    let formatter = CurrencyFormatter(locale: locale, currency: currency)
    #expect(formatter.format(100) != nil)
}
```

### 5.3 Suites and Traits

```swift
@Suite("Cart calculations", .tags(.checkout, .billing), .serialized)
struct CartTests {
    let cart = Cart()

    @Test("Total with no discount")
    func plainTotal() {
        cart.add(Item(price: 100), quantity: 3)
        #expect(cart.total == 300)
    }

    @Test("Coupon applies before tax",
          .bug("https://example.atlassian.net/browse/CART-42"),
          .timeLimit(.seconds(2)))
    func couponOrdering() async throws {
        cart.apply(Coupon.tenPercent)
        let invoice = try await cart.finalize()
        #expect(invoice.subtotal == 270)
    }

    @Test(.disabled("flaky on CI — investigation in CART-91"))
    func legacyPath() { /* ... */ }
}

extension Tag {
    @Tag static var checkout: Self
    @Tag static var billing: Self
}
```

Common traits:

- `.serialized` — disables parallelism for this suite or test.
- `.timeLimit(.seconds(n))` — fail-fast on hangs.
- `.disabled("reason")` / `.enabled(if:)` — conditional skip.
- `.tags(...)` — for `swift test --filter` / CI sharding.
- `.bug("URL")` — auto-link in Xcode UI.

### 5.4 Async Confirmations

```swift
@Test func observerReceivesEvent() async {
    await confirmation("event fired", expectedCount: 1) { confirm in
        let observer = Observer { event in
            #expect(event.kind == .updated)
            confirm()
        }
        await publisher.publish(.updated)
    }
}
```

`confirmation` replaces `XCTestExpectation.fulfill()`. The default `expectedCount` is `1`; you can pass `.unbounded` or a range.

### 5.5 `XCTest` — When to Keep It

Keep XCTest specifically for:

- **`XCUITest`** UI automation (out of this skill's scope — see the `snap` skill).
- **`XCTMetric`** performance tests with baselines (`measure(metrics:)`).
- **Existing very large test suites** where migration cost exceeds benefit; the two frameworks coexist in the same target.

### 5.6 Snapshot Testing

`swift-snapshot-testing` (PointFree) is the standard. Works with **both XCTest and Swift Testing** as of v1.17+:

```swift
import SnapshotTesting
import Testing

@Test func loginScreenSnapshot() {
    let vc = LoginViewController()
    assertSnapshot(of: vc, as: .image(on: .iPhone16Pro))
}
```

Inline snapshot testing (PointFree, 2024) keeps the expected value next to the test:

```swift
@Test func defaultConfig() {
    let json = encoder.encode(Config())
    assertInlineSnapshot(of: json, as: .json) {
        """
        { "version": 1, "theme": "system" }
        """
    }
}
```

### 5.7 `@MainActor` Test Policy

- Swift Testing tests are **`nonisolated` by default**. Mark a `@Suite` or `@Test` `@MainActor` explicitly when testing UI/observable code.
- XCTest is implicitly `@MainActor` — Swift Testing requires the opt-in.

```swift
@MainActor
@Suite struct ViewModelTests {
    @Test func updateBindings() async throws {
        let model = LoginViewModel()
        model.email = "a@b.com"
        #expect(model.isFormValid)
    }
}
```

### 5.8 Fixture Organization

```
Tests/
└── MyKitTests/
    ├── Fixtures/
    │   ├── ValidResponse.json
    │   └── ExpiredToken.json
    ├── Helpers/
    │   ├── TestClient.swift
    │   └── XCTAssertEqualish.swift
    ├── CartTests.swift
    └── CartTests+Edge.swift
```

Load fixtures via SPM `resources: [.copy("Fixtures")]` in the test target. Avoid storing assertions in fixtures — keep them in the test body.

For testing-side anti-patterns (`XCTestExpectation` double-fulfill, `Thread.sleep` in async tests, etc.), see [`swift-anti-patterns.md` §12](./swift-anti-patterns.md#12-testing-pitfalls).

---

## 6. Performance

### 6.1 Instruments — The First Step

For Apple platforms always profile before optimizing. Open **Instruments** (Xcode > Open Developer Tool > Instruments). Templates:

| Template | Use for |
|----------|---------|
| Time Profiler | CPU hotspots, main-thread blocking |
| Allocations | Object lifetime, leaks, churn |
| Leaks | Reference cycles |
| Network | URLSession traffic |
| Counters | Hardware events (cache misses, branch mispredicts) |
| Hangs | Main-thread stalls > 250ms |
| Points of Interest | Signposts you emit |

### 6.2 `OSSignposter` (Replaces `os_signpost`)

```swift
import os

private let signposter = OSSignposter(
    subsystem: "com.example.app",
    category: .pointsOfInterest
)

func process(_ batch: [Item]) async {
    let state = signposter.beginInterval("process", id: signposter.makeSignpostID())
    defer { signposter.endInterval("process", state) }
    for item in batch { await handle(item) }
}

// Single-event signposts:
signposter.emitEvent("cache miss", "key=\(key)")
```

Use `category: .pointsOfInterest` to surface signposts in Instruments' Points of Interest lane.

### 6.3 Optimization Knobs

- **`-O`** — release default (optimize for speed).
- **`-Osize`** — optimize for binary size; useful on watchOS, embedded, libraries shipped in app extensions.
- **`-O` + `-whole-module-optimization`** — default in release; enables cross-function specialization within a module.
- **`@inlinable`** — exposes body across modules so client modules can specialize generics.
- **`@inline(__always)`** — force-inline (rarely needed; compiler is usually right).
- **`final`** on classes, properties, methods → enables devirtualization.
- **Generic specialization** triggers automatically when types are known at the call site within the same module; `@inlinable` extends it cross-module.

### 6.4 Copy-on-Write & `ContiguousArray`

- `Array<T>` is COW. Copy is O(1) until written. Concatenation, indexing, slicing all preserve sharing.
- `ContiguousArray<T>` skips Objective-C bridging — use for `Array<class>` when the array never crosses to ObjC (e.g., internal caches, image processing buffers). Avoids the dynamic dispatch overhead.
- For raw memory access at hot spots:

```swift
let result: Int = numbers.withUnsafeBufferPointer { buffer in
    var sum = 0
    for i in 0..<buffer.count { sum &+= buffer[i] }
    return sum
}
```

`withUnsafeBufferPointer` skips bounds checks and ARC traffic inside the closure — measurable speedup on tight numeric loops.

### 6.5 Autoreleasepool

Even in Swift, `autoreleasepool { }` matters when calling Foundation/AppKit/UIKit APIs that produce autoreleased objects in tight loops (e.g., image processing, JSON parsing in batch). Without it, memory grows until the runloop drains.

```swift
for chunk in chunks {
    autoreleasepool {
        let image = UIImage(data: chunk)
        process(image)
    }
}
```

### 6.6 Pattern: Lazy Initialization with `Mutex`

For thread-safe lazy init without an actor (sync use):

```swift
final class Heavy: Sendable {
    private let cache = Mutex<Cached?>(nil)

    var value: Cached {
        cache.withLock { cached in
            if let cached { return cached }
            let new = compute()
            cached = new
            return new
        }
    }
}
```

### 6.7 Embedded / Size Optimization

`-Osize` and `-O` differ mainly in unrolling and inlining heuristics. Embedded Swift defaults to `-Osize` and excludes reflection, metatype lookups, generic non-final methods, weak/unowned, Codable, etc. — saving hundreds of KB.

For performance anti-patterns (decoder-per-call, sorted-first, filter-count-zero, reserveCapacity in a loop), see [`swift-anti-patterns.md` §6](./swift-anti-patterns.md#6-performance-pitfalls).

---

## 7. Memory Hygiene

### 7.1 ARC Recap

- All Swift classes use ARC. Strong references hold; weak/unowned don't.
- `weak` → `Optional` reference that nils out when target deallocates. Mandatory for delegates, observers, parent pointers.
- `unowned` → non-optional, non-retaining. **Crashes** on access after target dealloc. Use only when lifetime is guaranteed ≥ holder.
- `unowned(unsafe)` → no runtime check; classic dangling pointer if wrong. Almost never use.

### 7.2 Closure Capture List Rules

Default rule: any closure stored on `self` that captures `self` creates a retain cycle. Break it with a capture list:

```swift
// Bad — cycle: self -> request -> completion -> self
final class Loader {
    var request: Request?
    func start() {
        request = Request().onComplete { result in
            self.handle(result)        // strong self captured
        }
    }
}

// Good
final class Loader {
    var request: Request?
    func start() {
        request = Request().onComplete { [weak self] result in
            guard let self else { return }
            self.handle(result)
        }
    }
}
```

Decision matrix:

| Closure outlives `self`? | Closure runs while `self` may be deallocated? | Capture |
|--------------------------|----------------------------------------------|---------|
| No (e.g., synchronous map) | No | implicit strong — no capture list needed |
| Yes, but `self` is known alive (`UIViewController` action, `Task` bound to view's lifecycle) | No | `[weak self]` defensive default |
| Yes, but `self` is **definitely** alive for closure's whole life | No | `[unowned self]` (rare; usually overkill) |
| Yes, async background work | Yes | `[weak self]` always |

Apple's own samples use `[weak self]` defensively almost everywhere; `[unowned]` is reserved for delegate-relationship semantics where lifetime is structurally guaranteed.

### 7.3 Capturing Specific Values

Capture lists also let you snapshot a value:

```swift
let id = currentID
Task { [id] in
    await report(forID: id)        // snapshot, doesn't read mutable currentID
}
```

This is also how you make a closure `Sendable`: capture only `Sendable` values explicitly.

### 7.4 Cancellable Discipline (Combine Legacy)

```swift
final class FeedViewModel {
    private var cancellables = Set<AnyCancellable>()

    func bind() {
        api.feedPublisher
            .receive(on: DispatchQueue.main)
            .sink { [weak self] feed in self?.items = feed }
            .store(in: &cancellables)
    }
}
```

For new code prefer `AsyncSequence`; cancellation is automatic via the surrounding `Task`.

### 7.5 Common Cycles to Watch

- Parent ↔ child views/controllers — child holds `weak` reference to parent.
- Delegates — delegate property must be `weak`.
- Notification observers stored in `self` — call `removeObserver` in `deinit`.
- Timer / `DispatchSourceTimer` — both hold their target strongly until invalidated.
- Combine's `assign(to:on:)` strongly captures the target — use `assign(to: &$prop)` (publisher version) or `sink + [weak self]`.

For full cycle catalog and code-level fixes, see [`swift-anti-patterns.md` §2](./swift-anti-patterns.md#2-reference-cycle-pitfalls).

---

## 8. Server-Side Swift

### 8.1 Framework Choice — Vapor vs Hummingbird

| Framework | Status (2026-05) | Pick for |
|-----------|------------------|----------|
| Vapor 4.x | Production-stable | Existing Vapor apps; large ecosystem (Fluent, Leaf, JWTKit) |
| Vapor 5.x | Alpha → beta during 2026 | New apps wanting Vapor's batteries + Swift 6 native concurrency |
| Hummingbird 2.x | Stable | Lightweight services, micro-services, projects wanting minimal abstraction over `swift-nio` |
| Raw `swift-nio` | Stable | High-performance protocols, gRPC servers, niche transports |

**Vapor 5** (in development through 2026) sits on top of Hummingbird's HTTP server, brings gRPC, SSE, async body streaming, and full Swift Foundation. It is the "convergence" release.

**Hummingbird 2** highlights:

- Result-builder routing.
- Modern Swift Concurrency (no `EventLoopFuture` in user code).
- Smaller dependency tree than Vapor.

### 8.2 HTTP Client — `async-http-client`

The standard HTTP client for non-Apple platforms (and the recommended choice on Linux/server). Apple platforms can still use `URLSession`.

```swift
import AsyncHTTPClient

let client = HTTPClient(eventLoopGroupProvider: .singleton)
defer { try? client.syncShutdown() }

var request = HTTPClientRequest(url: "https://api.example.com/users")
request.method = .GET
request.headers.add(name: "Authorization", value: "Bearer \(token)")

let response = try await client.execute(request, timeout: .seconds(10))
let body = try await response.body.collect(upTo: 10 * 1024 * 1024)
```

Reuse a single `HTTPClient` for the process — internal connection pooling is amortized.

### 8.3 Database Drivers

| Database | Driver | Notes |
|----------|--------|-------|
| PostgreSQL | `vapor/postgres-nio` | Async `PostgresClient`; preferred over PostgresKit |
| SQLite | `groue/GRDB.swift` | Best ergonomics; v7+ supports Swift Concurrency. **Client-side only — not for production servers.** |
| SQLite (server) | `vapor/sqlite-nio` | NIO-based, server-suitable |
| MongoDB | `orlandos-nl/MongoKitten` 7.x | Async client |
| Redis | `swift-server/RediStack` | NIO-based |

Preferred pattern: `PostgresClient` for connection management, hand-rolled query helpers; reach for **Fluent** when you want an ORM, **raw PostgresNIO** when you want SQL with type-safe row decoding.

### 8.4 Observability Stack

The "Swift on Server" observability triplet:

| Concern | Package | Notes |
|---------|---------|-------|
| Logging | `apple/swift-log` | Vendor-neutral façade; backends to OSLog / stdout / Sentry |
| Metrics | `apple/swift-metrics` | Backend to Prometheus / StatsD via `swift-prometheus` etc. |
| Tracing | `apple/swift-distributed-tracing` | OpenTelemetry-compatible via `swift-otel/swift-otel` |

```swift
import Logging, Metrics, Tracing

let logger = Logger(label: "feed.service")
logger.info("starting", metadata: ["build": "\(buildID)"])

Counter(label: "feed.requests", dimensions: [("endpoint", "/feed")]).increment()

try await withSpan("loadFeed") { span in
    span.attributes["user.id"] = userID
    return try await loadFeed(userID)
}
```

Wire OpenTelemetry export with `swift-otel`:

```swift
import OTel
let otel = try OTel.bootstrap(
    serviceName: "feed-api",
    detectors: [.environment(), .process()]
)
```

### 8.5 Background Jobs

Vapor's `queues` package or, for lower-level, `swift-nio` scheduled tasks combined with `swift-distributed-actors` for cluster-aware workloads. For most apps, an external Redis-backed queue (BullMQ, Sidekiq) reached over HTTP is simpler than embedded job runners.

---

## 9. Production Library Matrix (2026)

| Domain | Library | Maintainer | Notes |
|--------|---------|------------|-------|
| **HTTP server** | Vapor 4.x / 5.x | Vapor team | Full framework; ORM, templating, JWT |
| | Hummingbird 2.x | Adam Fowler / SSWG | Light; Swift Concurrency-native |
| **HTTP client** | URLSession (Apple) | Apple | Default on Darwin |
| | AsyncHTTPClient | swift-server | Linux + cross-platform |
| **HTTP types** | swift-http-types | Apple | Shared `HTTPRequest`/`HTTPResponse` across client+server |
| **DB (PG)** | postgres-nio | Vapor | Async PostgreSQL client |
| **DB (MySQL)** | mysql-nio | Vapor | Async MySQL client |
| **DB (SQLite)** | GRDB.swift v7 | Gwendal Roué | Best mobile/local DB |
| **DB (SQLite server)** | sqlite-nio | Vapor | NIO-based |
| **DB (Mongo)** | MongoKitten 7 | Orlandos-NL | Async Mongo |
| **ORM (server)** | Fluent | Vapor | Ships with Vapor; PG/MySQL/SQLite |
| **JSON** | Codable (stdlib) | Apple | Default |
| | swift-json | Various | Performance path when Codable is too slow |
| **Logging façade** | swift-log | Apple | Standard |
| | OSLog / Logger | Apple | Apple platforms backend |
| **Metrics** | swift-metrics | Apple | Standard |
| **Tracing** | swift-distributed-tracing | Apple | OTel-compatible |
| | swift-otel | community | OTLP export |
| **DI** | swift-dependencies | PointFree | Modern environment-style DI; works great with TCA but also standalone |
| | Factory | Michael Long | Property-wrapper-based; older but lightweight |
| | Manual protocol + init injection | — | Often sufficient |
| **Reactive (legacy)** | Combine | Apple | Maintenance mode — use for legacy or RxSwift migration only |
| **Reactive (current)** | AsyncSequence | Apple | Default for 2026 net-new |
| | swift-async-algorithms | Apple | Operators (debounce, merge, chunked, etc.) |
| **Crypto** | swift-crypto | Apple | Wraps CryptoKit on Darwin, re-implements on Linux/Windows |
| **JWT** | JWTKit | Vapor | Standard for server JWT |
| **CLI** | swift-argument-parser | Apple | Declarative CLI w/ subcommands, completions |
| **Macros** | swift-syntax | Apple | For macro authors |
| **Collections** | swift-collections | Apple | OrderedSet, OrderedDictionary, Deque, BitSet |
| **Algorithms** | swift-algorithms | Apple | Combinations, chunked, windows, etc. |
| **Markdown** | swift-markdown | Apple | CommonMark + GFM |
| **WebSocket** | WebSocketKit (Vapor) / Hummingbird WS | Vapor/HB | Server-side |
| **gRPC** | grpc-swift v2 | Apple/SSWG | Pure-Swift, async/await |
| **Image** | swift-image | Various | Server image processing |
| **Snapshot test** | swift-snapshot-testing | PointFree | Standard |
| **Composable arch** | swift-composable-architecture | PointFree | Optional, opinionated app architecture |

**Selection heuristic**:

- Prefer libraries with **active 2025–2026 releases** and **non-trivial maintainer** (Apple, Vapor, PointFree, swift-server WG).
- Avoid libraries that don't ship Swift 6 language mode compatibility — they will block your migration.
- For DI, manual init injection scales further than newcomers think; reach for `swift-dependencies` when you want test-time substitution at scale.

---

## 10. Embedded Swift

### 10.1 Status (2026-05)

- **Swift 6.2**: Embedded Swift still experimental. Requires `-enable-experimental-feature Embedded`.
- **Swift 6.3 (Mar 2026)**: Embedded Swift exits experimental. LLDB support for breakpoint/step/inspect on bare-metal ARM and RISC-V.

### 10.2 Target Triples

| Architecture | Triple example |
|--------------|----------------|
| ARM Cortex-M0+ | `armv6m-none-none-eabi` |
| ARM Cortex-M4 | `armv7em-none-none-eabi` (with FP: `armv7em-none-none-eabihf`) |
| ARM Cortex-M33 | `armv8m.main-none-none-eabi` |
| RISC-V 32-bit | `riscv32-none-none-eabi` |
| WebAssembly | `wasm32-unknown-wasi` (via Swift SDK for WASI) |
| ESP32-C6 (RISC-V) | `riscv32-esp-elf` |

### 10.3 What's Excluded in Embedded Mode

- Reflection (`Mirror`).
- `Any` and `AnyObject` existentials in dynamic dispatch.
- Codable (which depends on reflection).
- ObjC interop.
- Most of Foundation.
- `weak` / `unowned`.
- Non-final generic methods.
- Throwing inside generic context (mostly).

What you DO get:

- Generics with monomorphization.
- Protocols (as constraints, no existentials).
- Structs, enums, classes.
- Property wrappers, result builders.
- Macros.

### 10.4 Build

```bash
swiftc \
    -target armv7em-none-none-eabi \
    -enable-experimental-feature Embedded \
    -wmo -Osize \
    -c LED.swift Main.swift \
    -o firmware.o
```

Apple provides example projects (`apple/swift-embedded-examples`) for Raspberry Pi Pico (RP2040), STM32, ESP32-C3/C6, and nRF52840.

### 10.5 When to Choose Embedded Swift Over C / Rust

**Choose Embedded Swift when:**

- Team is iOS/macOS-fluent; reuse of Swift skill is valuable.
- Sharing code with a companion iOS app (same types in firmware and app).
- Memory safety + ergonomics matter more than the last 5% of code size.
- Targeting Apple's own embedded surfaces (Secure Enclave-adjacent, accessory development).

**Choose C when:**

- Targeting an architecture without Swift LLVM backend support.
- Vendor SDK is C-only and FFI overhead matters.
- ROM/RAM budget is brutal (sub-32KB).

**Choose Rust when:**

- Need mature embedded ecosystem (RTIC, embassy).
- Need formal verification or memory-safety guarantees without runtime.
- Targeting safety-critical (ISO 26262, IEC 61508).

### 10.6 `@_unavailableInEmbedded`

Internal attribute (subject to change) marks symbols that don't compile in Embedded mode. Library authors targeting both regular and Embedded Swift sprinkle this across reflection-dependent APIs.

```swift
@_unavailableInEmbedded
public func description<T>(of value: T) -> String { String(reflecting: value) }
```

For library authors today, the safer pattern is `#if hasFeature(Embedded)` or `#if !$Embedded` (subject to evolution).

---

## 11. Cross-Platform Packaging

### 11.1 Deployment Target Strategy

For a library:

- **Lowest target = lowest customer you'll support.** Look at App Store device usage: as of 2026, iOS 17 captures ~95% of active iPhones. Targeting iOS 17 unlocks `@Observable`, Swift Concurrency-native APIs.
- For server/Linux libs, pick the lowest LTS distro you'll support (typically Ubuntu 22.04+).

### 11.2 `@available` & `#available`

```swift
@available(iOS 17.0, macOS 14.0, *)
public struct Money: Sendable { /* uses iOS 17 stdlib */ }

@available(iOS, deprecated: 18.0, message: "Use the async version instead")
public func legacyLoad(completion: @escaping (Data?) -> Void) { /* … */ }

func showWindow() {
    if #available(iOS 17.0, *) {
        modernPresenter.show()
    } else {
        legacyPresenter.show()
    }
}

func showWindowGuard() {
    guard #available(iOS 17.0, *) else { return legacyShow() }
    modernPresenter.show()
}
```

`#unavailable` is the inverse — useful for early-return on old OS:

```swift
guard #unavailable(iOS 18.0) else { /* iOS 18+ path */ return }
```

### 11.3 Platform Configuration in `Package.swift`

```swift
platforms: [
    .iOS(.v17),
    .macOS(.v14),
    .tvOS(.v17),
    .watchOS(.v10),
    .visionOS(.v1),
    .macCatalyst(.v17),
    .driverKit(.v23),
]
```

Linux deployment is implicit (no `platforms:` entry needed).

### 11.4 Multi-Platform Conditional Dependencies

```swift
dependencies: [
    .package(url: "https://github.com/swift-server/async-http-client", from: "1.21.0"),
    .package(url: "https://github.com/apple/swift-crypto", from: "3.0.0"),
],
targets: [
    .target(
        name: "MyLib",
        dependencies: [
            .product(
                name: "AsyncHTTPClient",
                package: "async-http-client",
                condition: .when(platforms: [.linux, .android, .windows])
            ),
            .product(name: "Crypto", package: "swift-crypto"),
        ]
    )
]
```

### 11.5 Per-Platform Sources Layout

```
Sources/MyKit/
├── Core/                     # all platforms
├── Apple/                    # `#if canImport(Foundation)` + Darwin specifics
├── Linux/                    # `#if os(Linux)`
└── Wasm/                     # `#if arch(wasm32)`
```

Avoid platform-specific subdirectories unless they reduce `#if` noise meaningfully.

---

## 12. Documentation (DocC)

### 12.1 Triple-Slash Comments

```swift
/// Loads the user profile from the network.
///
/// This call uses the shared session and respects the global cache policy.
///
/// - Parameters:
///   - id: Unique user identifier.
///   - forceRefresh: If `true`, bypasses the cache.
/// - Returns: A fully populated ``Profile`` for the given user.
/// - Throws: ``NetworkError`` when offline or the response is malformed.
/// - Complexity: O(1) network call; O(n) where n is profile size for decoding.
public func loadProfile(
    id: UUID,
    forceRefresh: Bool = false
) async throws -> Profile
```

### 12.2 `.docc` Bundle

```
Sources/MyKit/MyKit.docc/
├── MyKit.md                          # landing page
├── Articles/
│   ├── GettingStarted.md
│   └── AdvancedUsage.md
├── Resources/
│   └── architecture.png
└── Tutorials/
    └── BuildYourFirstFeature.tutorial
```

Landing page format:

```markdown
# ``MyKit``

A summary sentence about the framework.

## Overview

Longer explanation here.

## Topics

### Getting Started

- <doc:GettingStarted>
- ``Profile``
- ``ProfileLoader``

### Errors

- ``NetworkError``
```

### 12.3 Tutorials

```
@Tutorial(time: 30) {
    @Intro(title: "Build Your First Feature") {
        ...
        @Image(source: "intro.png", alt: "")
    }

    @Section(title: "Add the package") {
        @ContentAndMedia { ... }
        @Steps {
            @Step { Open `Package.swift` and add the dependency. }
            ...
        }
    }
}
```

### 12.4 Generate Documentation

For a Swift package (using the `swift-docc-plugin`):

```bash
# Preview locally:
swift package --disable-sandbox preview-documentation --target MyKit

# Build a static archive:
swift package --allow-writing-to-directory ./docs \
    generate-documentation --target MyKit \
    --output-path ./docs \
    --transform-for-static-hosting \
    --hosting-base-path my-repo
```

For an Xcode project: **Product → Build Documentation**.

### 12.5 Hosting on GitHub Pages

CI workflow (`.github/workflows/docs.yml`):

```yaml
name: Deploy DocC
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  build:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - run: |
          swift package --allow-writing-to-directory docs \
            generate-documentation --target MyKit \
            --disable-indexing \
            --transform-for-static-hosting \
            --hosting-base-path my-repo \
            --output-path docs
      - uses: actions/upload-pages-artifact@v3
        with: { path: docs }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
    steps:
      - uses: actions/deploy-pages@v4
```

Set `--hosting-base-path` to the repo name so `<base href>` resolves correctly under `https://<user>.github.io/<repo>/`.

### 12.6 DocC Discipline

- One sentence summary first, blank line, then paragraphs.
- Link types with double backticks: `` ``Profile`` `` resolves to the `Profile` symbol.
- Use `## Topics` curation to organize the auto-generated page.
- Don't write filler comments (`/// Returns the value` on a property). Let the type speak.
- For internal-only documentation use plain `// MARK:` and `/// ` — DocC won't surface internal symbols.

---

## 13. 2023→2026 Migration Cheatsheet

| From (2023) | To (2026) | Notes |
|-------------|-----------|-------|
| `Combine` (`@Published`, `Publisher`) | `AsyncSequence` + `swift-async-algorithms` | New code. Keep Combine for SwiftUI integrations and existing pipelines that work fine. |
| `ObservableObject` + `@Published` + `@StateObject` | `@Observable` class + `@State` / `@Bindable` | iOS 17+. Test for init-side-effects when migrating `@StateObject → @State` — see [`swift-anti-patterns.md` §7.2](./swift-anti-patterns.md#72-observable-vs-observableobject-init-lifecycle-gotcha). |
| `completion: @escaping (Result<T, Error>) -> Void` | `async throws -> T` | Use `withCheckedThrowingContinuation` for incremental migration. |
| Hand-rolled DI (singletons, init injection sprawl) | `swift-dependencies` (PointFree) | When test substitution is painful. Otherwise stay with init injection. |
| `XCTest` | `Swift Testing` (`@Test`, `#expect`) | New tests in Swift Testing; XCTest remains for XCUITest + XCTMetric. |
| Custom locks (`NSLock`, `DispatchSemaphore`, `os_unfair_lock`) | `Mutex<T>` from `Synchronization` | Swift 6.0+, iOS 18+ minimum. |
| `actor SomeUI { … }` with everything `@MainActor`-forced | Approachable Concurrency default isolation | New projects opt in via `defaultIsolation` + `nonisolated` where work belongs off main. |
| `@MainActor` annotated on every type for simplicity | Module-default `MainActor` + targeted `@concurrent` | Swift 6.2+ `defaultIsolation(MainActor.self)`. |
| `@_implementationOnly import` | `internal import` | Swift 6.0+ formal access modifier on imports. |
| `swiftLanguageVersions: [.v5]` | `swiftLanguageModes: [.v6]` | Package manifest renaming + per-target `.swiftLanguageMode(.v6)`. |
| Untyped `throws` for closed error enums | `throws(MyError)` typed throws | When exhaustive catch matters or in performance-sensitive paths. |
| Linux-only branches doing C bridging | Embedded Swift target | When binary lives on a microcontroller or bare-metal CPU. |
| Webpack/Vite for in-browser code | Swift compiled to WebAssembly (Swift 6.2 WASI SDK) | When you want to share Swift business logic with a web frontend. |
| `os_signpost(_:log:name:)` C-style API | `OSSignposter` Swift API | iOS 15+, clearer state object pattern. |
| `print()` / `NSLog()` | `Logger` / `OSLog` / `swift-log` | Even for hobby projects — auto-redacts privacy-marked values, persists across reboots. |
| `URLSession.shared.dataTask(with:completionHandler:)` | `URLSession.shared.data(from:)` async | Async/await everywhere. |
| `DispatchQueue.global().async { … }` | `Task { … }` or `@concurrent` function | Structured concurrency surfaces lifetime + cancellation. |
| `NotificationCenter.default.addObserver(…)` (closure variant) | `notifications(named:)` `AsyncSequence` | iOS 15+ native async API. |
| `@objc dynamic var foo` with KVO | `@Observable` + `withObservationTracking` | New observation model. |
| Custom singleton DI registry | `swift-dependencies` `@Dependency` | Test override built in. |

### 13.1 Mass `@Published → @Observable` Migration

```swift
// Before (2023)
final class FeedViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var isLoading = false
}

struct FeedView: View {
    @StateObject var model = FeedViewModel()
    var body: some View {
        List(model.items) { Text($0.title) }
    }
}

// After (2026, iOS 17+)
@Observable
final class FeedViewModel {
    var items: [Item] = []
    var isLoading = false
}

struct FeedView: View {
    @State var model = FeedViewModel()
    var body: some View {
        List(model.items) { Text($0.title) }
    }
}
```

Caveat: `@State` reinitializes the value on view-identity change; `@StateObject` did not. Audit any model with side-effecting `init` before swapping. SwiftUI-specific binding patterns belong in [`../../native/SKILL.md`](../../native/SKILL.md).

### 13.2 Completion-Handler → `async/await`

```swift
// Before
func fetchUser(id: UUID, completion: @escaping (Result<User, Error>) -> Void) {
    URLSession.shared.dataTask(with: url) { data, _, error in
        if let error { return completion(.failure(error)) }
        guard let data else { return completion(.failure(URLError(.zeroByteResource))) }
        do { completion(.success(try JSONDecoder().decode(User.self, from: data))) }
        catch { completion(.failure(error)) }
    }.resume()
}

// After
func fetchUser(id: UUID) async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Bridging while incrementally migrating callers:
func fetchUser(id: UUID, completion: @escaping (Result<User, Error>) -> Void) {
    Task {
        do { completion(.success(try await fetchUser(id: id))) }
        catch { completion(.failure(error)) }
    }
}
```

### 13.3 `@MainActor` everywhere → Approachable Concurrency

Step-by-step:

1. **Audit current `@MainActor` annotations**: which are truly UI-bound, which are there because "everything was async-unsafe"?
2. **Enable approachable concurrency** in `Package.swift`:
   ```swift
   swiftSettings: [.defaultIsolation(MainActor.self)]
   ```
3. **Remove explicit `@MainActor`** from types now inferred as MainActor by default.
4. **Add `nonisolated`** to functions that should run off the main thread (`parseJSON`, `compressImage`).
5. **Add `@concurrent`** to functions that must always run on the global executor regardless of caller.
6. **Re-run the test suite under TSan** — Approachable Concurrency reduces *false positives*, not *real races*.

---

## Sources

### Core Swift Documentation

- [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
- [Swift 6.2 Released](https://www.swift.org/blog/swift-6.2-released/)
- [Swift 6.3 Released](https://www.swift.org/blog/swift-6.3-released/)
- [What's new in Swift: December 2025](https://www.swift.org/blog/whats-new-in-swift-december-2025/)
- [What's new in Swift: March 2026](https://www.swift.org/blog/whats-new-in-swift-march-2026/)
- [Library Evolution in Swift](https://www.swift.org/blog/library-evolution/)
- [Embedded Swift Get Started](https://www.swift.org/get-started/embedded/)
- [Embedded Swift Examples](https://www.swift.org/blog/embedded-swift-examples/)
- [Swift for WebAssembly Getting Started](https://www.swift.org/documentation/articles/wasm-getting-started.html)
- [Swift Packages — Testing](https://www.swift.org/packages/testing.html)
- [Announcing ArgumentParser](https://www.swift.org/blog/argument-parser/)

### Swift Evolution Proposals (production-relevant)

- [SE-0193 — Cross-module Inlining and Specialization](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0193-cross-module-inlining-and-specialization.md)
- [SE-0304 — Structured Concurrency](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0304-structured-concurrency.md)
- [SE-0386 — Package Access Modifier](https://github.com/apple/swift-evolution/blob/main/proposals/0386-package-access-modifier.md)
- [SE-0410 — Atomics](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0410-atomics.md)
- [SE-0414 — Region-Based Isolation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0414-region-based-isolation.md)
- [SE-0430 — Transferring Parameters and Results](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0430-transferring-parameters-and-results.md)
- [SE-0441 — Formalize Language Mode Terminology](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0441-formalize-language-mode-terminology.md)

### Concurrency

- [Default Actor Isolation in Swift 6.2 (SwiftLee)](https://www.avanderlee.com/concurrency/default-actor-isolation-in-swift-6-2/)
- [Swift 6.2 Concurrency Changes (SwiftLee)](https://www.avanderlee.com/concurrency/swift-6-2-concurrency-changes/)
- [Approachable Concurrency in Swift 6.2 (SwiftLee)](https://www.avanderlee.com/concurrency/approachable-concurrency-in-swift-6-2-a-clear-guide/)
- [What is @concurrent in Swift 6.2? (Donny Wals)](https://www.donnywals.com/what-is-concurrent-in-swift-6-2/)
- [Should you opt-in to Swift 6.2's Main Actor isolation? (Donny Wals)](https://www.donnywals.com/should-you-opt-in-to-swift-6-2s-main-actor-isolation/)
- [Setting default actor isolation in Xcode 26 (Donny Wals)](https://www.donnywals.com/setting-default-actor-isolation-in-xcode-26/)
- [Exploring concurrency changes in Swift 6.2 (Donny Wals)](https://www.donnywals.com/exploring-concurrency-changes-in-swift-6-2/)
- [SE-0414 Region Based Isolation (Massicotte)](https://www.massicotte.org/concurrency-swift-6-se-0414/)
- [SE-0430 sending parameters (Massicotte)](https://www.massicotte.org/concurrency-swift-6-se-0430/)
- [Mastering Task Groups in Swift (Majid)](https://swiftwithmajid.com/2025/02/04/mastering-task-groups-in-swift/)
- [Implementing Task timeout with Swift Concurrency (Donny Wals)](https://www.donnywals.com/implementing-task-timeout-with-swift-concurrency/)
- [Default Actor Isolation: New Problems from Good Intentions (fatbobman)](https://fatbobman.com/en/posts/default-actor-isolation/)
- [Sendable NSManagedObjectContext (fatbobman)](https://fatbobman.com/en/posts/sendable-nsmanagedobjectcontext/)

### Synchronization & Mutex

- [Synchronization Framework in Swift 6 (Jacob's Tech Tavern)](https://blog.jacobstechtavern.com/p/the-synchronisation-framework)
- [Modern Swift Lock: Mutex & the Synchronization Framework (SwiftLee)](https://www.avanderlee.com/concurrency/modern-swift-lock-mutex-the-synchronization-framework/)

### Error Handling

- [Type-safe and user-friendly error handling in Swift 6](https://theswiftdev.com/2025/type-safe-and-user-friendly-error-handling-in-swift-6/)
- [Typed Throws in Swift (Majid)](https://swiftwithmajid.com/2024/08/20/typed-throws-in-swift/)
- [Typed Throws in Swift 6 (Yusuf Gürel)](https://medium.com/@gurelyusuf/typed-throws-in-swift-6-c9c7ab1f6501)
- [LocalizedError protocols (NSHipster)](https://nshipster.com/swift-foundation-error-protocols/)
- [Propagating user-facing errors in Swift (Sundell)](https://www.swiftbysundell.com/articles/propagating-user-facing-errors-in-swift/)
- [The Four Audiences of Swift Errors (Nonstrict, 2026)](https://nonstrict.eu/blog/2026/the-four-audiences-of-swift-errors/)

### Package Management

- [Using Swift 6 Language Mode in SPM (Donny Wals)](https://www.donnywals.com/setting-the-swift-language-mode-for-an-spm-package/)
- [Building a Swift package using the Swift 6 language mode (Pol Piella)](https://www.polpiella.dev/swift-6-language-mode/)
- [SwiftLanguageMode.v6 (docs.swift.org)](https://docs.swift.org/swiftpm/documentation/packagedescription/swiftlanguagemode/v6/)

### Testing

- [Swift Testing (GitHub)](https://github.com/swiftlang/swift-testing)
- [Swift Testing Complete Guide 2026 (Swift Crafted)](https://swiftcrafted.dev/article/complete-guide-swift-testing-first-test-advanced-patterns)
- [Implementing parameterized tests (Apple Docs)](https://developer.apple.com/documentation/testing/parameterizedtesting)
- [Parameterized tests in Swift (SwiftLee)](https://www.avanderlee.com/swift-testing/parameterized-tests-reducing-boilerplate-code/)
- [Swift Testing support for SnapshotTesting (PointFree)](https://www.pointfree.co/blog/posts/146-swift-testing-support-for-snapshottesting)
- [Inline Snapshot Testing (PointFree)](https://www.pointfree.co/blog/posts/113-inline-snapshot-testing)
- [swift-snapshot-testing (GitHub)](https://github.com/pointfreeco/swift-snapshot-testing)

### Performance

- [Swift OptimizationTips (GitHub)](https://github.com/swiftlang/swift/blob/main/docs/OptimizationTips.rst)
- [Measuring performance with os_signpost (Donny Wals)](https://www.donnywals.com/measuring-performance-with-os_signpost/)
- [How to profile with Instruments and os_signposts (Pol Piella)](https://www.polpiella.dev/time-profiler-instruments/)
- [OSSignposter docs (Apple)](https://developer.apple.com/documentation/os/ossignposter)
- [withUnsafeBufferPointer (Apple Docs)](https://developer.apple.com/documentation/swift/contiguousarray/withunsafebufferpointer(_:))
- [Understanding @inlinable (SwiftRocks)](https://swiftrocks.com/understanding-inlinable-in-swift)
- [ABI Stability and More (Swift.org)](https://www.swift.org/blog/abi-stability-and-more/)

### Server-Side Swift

- [Vapor 5 Materializes the Future (InfoQ)](https://www.infoq.com/news/2024/09/swift-vapor-5-roadmap/)
- [The Future of Vapor](https://blog.vapor.codes/posts/the-future-of-vapor/)
- [Vapor (GitHub)](https://github.com/vapor/vapor)
- [What's new in Hummingbird 2](https://swiftonserver.com/whats-new-in-hummingbird-2/)
- [PostgresNIO (GitHub)](https://github.com/vapor/postgres-nio)
- [async-http-client (GitHub)](https://github.com/swift-server/async-http-client)
- [swift-distributed-tracing (GitHub)](https://github.com/apple/swift-distributed-tracing)
- [swift-otel (GitHub)](https://github.com/swift-otel/swift-otel)
- [opentelemetry-swift](https://opentelemetry.io/docs/languages/swift/)

### Production Libraries

- [swift-dependencies (PointFree)](https://github.com/pointfreeco/swift-dependencies)
- [swift-crypto (Apple)](https://github.com/apple/swift-crypto)
- [swift-log (Apple)](https://github.com/apple/swift-log)
- [swift-argument-parser docs](https://apple.github.io/swift-argument-parser/documentation/argumentparser/)
- [GRDB.swift (groue)](https://github.com/groue/GRDB.swift)
- [swift-async-algorithms](https://github.com/apple/swift-async-algorithms)

### Embedded Swift

- [Go small with Embedded Swift (WWDC24)](https://developer.apple.com/videos/play/wwdc2024/10197/)
- [Embedded Swift on ESP32-C6 (Espressif)](https://developer.espressif.com/blog/build-embedded-swift-application-for-esp32c6/)
- [Swift 6.3 What to Expect Spring 2026](https://www.atelier-socle.com/en/articles/swift-6-3-preview)
- [State of Swift 2026 (DevNewsletter)](https://devnewsletter.com/p/state-of-swift-2026/)

### Cross-Platform

- [Platform-specific code in Swift Packages (Pol Piella)](https://www.polpiella.dev/platform-specific-code-in-swift-packages/)
- [Swift @available attributes](https://www.freiwald.dev/posts/swift-available-attributes/)
- [Swift API Availability (NSHipster)](https://nshipster.com/available/)
- [SDK conditional code with canImport version (Eidinger)](https://blog.eidinger.info/sdk-conditional-code-with-canimportmodule-version-1234)

### DocC

- [swift-docc (GitHub)](https://github.com/swiftlang/swift-docc)
- [swift-docc-plugin Publishing to GitHub Pages](https://github.com/swiftlang/swift-docc-plugin/blob/main/Sources/SwiftDocCPluginDocumentation/SwiftDocCPlugin.docc/Publishing%20to%20GitHub%20Pages.md)
- [Generating Documentation for Hosting Online](https://swiftlang.github.io/swift-docc-plugin/documentation/swiftdoccplugin/generating-documentation-for-hosting-online/)
- [Publishing DocC as Static Website on GitHub Pages](https://www.createwithswift.com/publishing-docc-documention-as-a-static-website-on-github-pages/)

### Observation

- [Migrating to Observable (Apple Docs)](https://developer.apple.com/documentation/SwiftUI/Migrating-from-the-observable-object-protocol-to-the-observable-macro)
- [@Observable Macro performance increase (SwiftLee)](https://www.avanderlee.com/swiftui/observable-macro-performance-increase-observableobject/)
- [@Observable is not a drop-in replacement (Jesse Squires)](https://www.jessesquires.com/blog/2024/09/09/swift-observable-macro/)
