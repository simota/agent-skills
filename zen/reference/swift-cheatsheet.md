# Swift Refactoring Cheatsheet (Swift 6.2+)

Purpose: Zen-flavored slice of the Swift knowledge base — code-smell-to-idiom transformations, naming hygiene, magic-number cleanup, and refactor anti-patterns. Behavior-preserving only.

Baseline: **Swift 6.2+, Xcode 26, Approachable Concurrency**.

Source of truth (do not duplicate here):
- Bad-pattern catalog → [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md)
- Target idioms / API Design Guidelines → [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md)
- Language surface (typed throws, `@Observable`, region isolation, `~Copyable`, macros) → [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md)

Companion: [`language-patterns.md`](./language-patterns.md) holds the cross-language Swift quick-pattern set. Read this file for refactor-specific transformations.

---

## Contents

- [Smell → Idiom Map](#smell--idiom-map)
- [Function Extraction Signals (Swift-specific)](#function-extraction-signals-swift-specific)
- [Naming Hygiene (Swift API Design Guidelines)](#naming-hygiene-swift-api-design-guidelines)
- [Magic Numbers and Strings](#magic-numbers-and-strings)
- [Concurrency Refactors (Approachable Concurrency)](#concurrency-refactors-approachable-concurrency)
- [Refactor Anti-Patterns to Avoid](#refactor-anti-patterns-to-avoid)
- [Refactor Checklist](#refactor-checklist)

---

## Smell → Idiom Map

| Smell | Idiom | Notes |
|-------|-------|-------|
| `if let x = a { if let y = x.b { ... } }` nested | Comma-chained `if let x, let y = ...` (5.7+) / `guard let x, let y` early-return | Removes rightward drift; preferred over `flatMap` chains for readability |
| `if let x = x` re-bind | `if let x` shorthand (5.7+) | Drops the redundant `= x` |
| Manual `Result<T, E>` propagation through callbacks | `try` + typed throws `throws(E)` (6.0+) | Typed throws give compile-time error precision without `Result` ceremony |
| `Combine` `Publishers` chain for one-shot fetch | `AsyncSequence` / `async` function | Reserve Combine for genuinely streaming UI bindings |
| `class C: ObservableObject` + `@Published var x` | `@Observable class C { var x }` (5.9+) | One macro, finer-grained tracking, no Combine subscription cost |
| Completion-handler-style callbacks | `async throws -> T` + `withCheckedThrowingContinuation` at the seam | Don't bridge layer-by-layer; bridge once at the boundary |
| `delegate` protocol with one optional method | `AsyncSequence` or `@Observable` | Use delegates only when you genuinely need synchronous push from UIKit/AppKit |
| `for c in s { result += String(c) }` | `var s = ""; s.reserveCapacity(n); s.append(c)` | `+=` on `String` reallocates; `reserveCapacity` removes copies |
| `for i in 0..<xs.count { ... xs[i] ... }` | `for x in xs` / `for (i, x) in xs.enumerated()` | Removes bounds-checking redundancy; clearer intent |
| `final class` holding only value-typed properties | `struct` | Reach for `class` only when you need reference identity or inheritance |
| Singleton via `private init` + `static let shared` | Same — but pass via DI when feature-scope | Singletons hide testability; keep `shared` only for stateless utilities |
| `@MainActor` applied at the top of the file | Per-type / per-method isolation (6.2 Approachable Concurrency) | `nonisolated(nonsending)` + `@concurrent` give finer control |
| `Task { ... }` floating inside `viewDidLoad`/`init` | `async let` / `TaskGroup` inside a structured parent | Floating `Task` leaks cancellation; structured forms inherit cancellation |
| `withCheckedContinuation` to wrap a delegate | `AsyncStream<T>` builder | Stream APIs map naturally onto delegate push |
| `XCTest` `func testFoo()` + `XCTAssertEqual` | Swift Testing `@Test func foo()` + `#expect` (Xcode 16+) | Macro-based, parameterized via `@Test(arguments:)`, parallel by default |
| Force-unwrap `try!` / `!` in non-test code | `try` + typed throws / `guard let`, `??` | `!` is a deferred runtime crash; cost of `?` is one branch |
| `as!` downcast without runtime guarantee | `as?` + `else throw` / `else return default` | Same as force-unwrap but worse — type information is lost at compile time |
| `let userID: String` plus other `String` IDs everywhere | `struct UserID: Hashable, Codable, Sendable { let value: UUID }` | Primitive-obsession fix; compiler stops you from passing `OrderID` where `UserID` is expected |
| Long type signature repeated in many places | `typealias` at file scope / `some Protocol` opaque return | `typealias` for type aliases; `some` for hiding concrete generic params |
| Repeated boolean argument `foo(silent: true, dry: true, force: false)` | Option set / enum cases (`Options.silent.union(.dry)`) | Boolean-blindness anti-pattern; the call site reads like flag soup |
| Reference-typed view model passed to SwiftUI body | `@Observable` final class + `@State` / `@Bindable` (5.9+) | Removes `@StateObject` boilerplate and Combine machinery |

### Selected before/after snippets

#### Nested `if let` → chained binding

```swift
// Before
if let user = user {
    if let address = user.address {
        if let city = address.city {
            return city
        }
    }
}
return nil

// After (5.7+)
if let user, let address = user.address, let city = address.city {
    return city
}
return nil
```

#### `Result`-style propagation → typed throws

```swift
// Before
enum FetchError: Error { case decode, network }

func loadUser(id: UUID) async -> Result<User, FetchError> {
    switch await api.fetch(id) {
    case .success(let data):
        guard let u = try? JSONDecoder().decode(User.self, from: data) else {
            return .failure(.decode)
        }
        return .success(u)
    case .failure:
        return .failure(.network)
    }
}

// After (Swift 6.0+)
func loadUser(id: UUID) async throws(FetchError) -> User {
    let data = try await api.fetch(id)
    do { return try JSONDecoder().decode(User.self, from: data) }
    catch { throw .decode }
}
```

#### `ObservableObject` → `@Observable`

```swift
// Before
final class CounterVM: ObservableObject {
    @Published var count = 0
}

// After (5.9+)
@Observable
final class CounterVM {
    var count = 0
}
```

#### Force-unwrap `!` → `guard let`

```swift
// Before
let url = URL(string: "https://example.com/\(path)")!
session.dataTask(with: url) { ... }.resume()

// After
guard let url = URL(string: "https://example.com/\(path)") else {
    throw URLError(.badURL)
}
```

#### Primitive ID → typed wrapper

```swift
// Before
func ban(userID: String, byAdmin adminID: String) { /* easy to swap args */ }

// After
struct UserID: Hashable, Codable, Sendable { let value: UUID }
struct AdminID: Hashable, Codable, Sendable { let value: UUID }

func ban(userID: UserID, byAdmin adminID: AdminID) { /* compiler-enforced */ }
```

#### Bool arg → option set

```swift
// Before
func sync(silent: Bool, force: Bool, dryRun: Bool) { /* ... */ }
sync(silent: true, force: false, dryRun: true)   // What does this mean?

// After
struct SyncOptions: OptionSet, Sendable {
    let rawValue: Int
    static let silent  = SyncOptions(rawValue: 1 << 0)
    static let force   = SyncOptions(rawValue: 1 << 1)
    static let dryRun  = SyncOptions(rawValue: 1 << 2)
}
func sync(_ options: SyncOptions) { /* ... */ }
sync([.silent, .dryRun])
```

#### Floating `Task` → structured `async let`

```swift
// Before — `Task` leaks cancellation; parent does not await
func refresh() {
    Task { await loadUser() }
    Task { await loadFeed() }
}

// After
func refresh() async throws {
    async let user = loadUser()
    async let feed = loadFeed()
    _ = try await (user, feed)   // cancellation propagates correctly
}
```

#### XCTest → Swift Testing

```swift
// Before
final class AdderTests: XCTestCase {
    func testAdds() {
        XCTAssertEqual(adder.add(2, 3), 5)
    }
}

// After
import Testing

@Suite struct AdderTests {
    @Test func adds() {
        #expect(adder.add(2, 3) == 5)
    }

    @Test(arguments: [(2, 3, 5), (0, 0, 0), (-1, 1, 0)])
    func cases(a: Int, b: Int, expected: Int) {
        #expect(adder.add(a, b) == expected)
    }
}
```

---

## Function Extraction Signals (Swift-specific)

Extract a helper when you see:

1. **A closure capturing 4+ values from the enclosing scope** — promote to a named method with explicit parameters. Captures hide control flow.
2. **Repeated optional unwrapping of the same chain** in 3+ call sites — extract a `private func` returning the unwrapped or `throw`-ing value.
3. **Nested `do-try-catch` chains > 2 deep** — each layer should resolve one error domain; flatten by extracting per-domain helpers that throw typed errors.
4. **SwiftUI body block > 60 lines** — extract a child view; SwiftUI's diff cost rises with body depth.
5. **`@MainActor` method doing 80% off-main work** — extract the off-main portion into a `nonisolated` helper; keep the `@MainActor` method as the UI sync point.
6. **`switch` with shared post-processing across arms** — extract the post-processing as a helper; arms reduce to value construction.

Counter-signals (do NOT extract):
- 3-line block used in one place; inlining is clearer.
- A helper that requires more isolation annotations than the inlined version.
- A function whose name would be `do{Original}Helper` — that means the original needed renaming, not splitting.

---

## Naming Hygiene (Swift API Design Guidelines)

Follow Apple's Swift API Design Guidelines [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md) §1 exactly. Rename targets that violate any of these:

| Item Kind | Convention | Example |
|-----------|-----------|---------|
| Type, protocol, enum, struct, class, actor | `UpperCamelCase` | `OrderRepository`, `URLSession` |
| Function, method, variable, property, enum case | `lowerCamelCase` | `loadUser(id:)`, `pendingOrders` |
| Generic type parameter | `UpperCamelCase`, descriptive | `Element`, `Failure`, not `T` unless universally generic |
| Constants | `lowerCamelCase` (Swift differs from C/Rust here) | `defaultTimeout`, `maxRetries` |
| Acronyms | All caps if standalone, `lowerCamelCase` if mid-identifier | `urlSession`, `decodeURL`, `HTTPClient` |

### Argument labels

- Use a **preposition** when the argument modifies the receiver: `array.insert(x, at: 0)`, `view.add(_:to:)`.
- Use **the verb's natural English**: `move(to:)`, not `move(toPosition:)`.
- **Omit needless words**: `removeElement(_:)` → `remove(_:)` when the receiver type is `Set<Element>`.
- **First-argument label** required unless the type is wholly described by the function name: `min(_:_:)` omits labels, `print(_:terminator:)` keeps them.

### Protocol names

- **Capability**: `-able` / `-ible` / `-ing` suffix — `Equatable`, `Hashable`, `Codable`, `AsyncSequence`.
- **What-it-is**: noun — `Collection`, `Sequence`, `Numeric`.
- **Avoid `IFoo`/`FooProtocol`** Java-isms — anti-patterns §4.

### Boolean property names

- Read as English assertions: `view.isHidden`, `string.isEmpty`, `array.contains(x)`.
- Avoid double negatives: `isNotEmpty` → use `!isEmpty`.

### Error type names

- Conform to `Error`; name ends with `Error`: `DecodingError`, `NetworkError`.
- Cases do NOT repeat the type prefix: `NetworkError.timeout`, not `NetworkError.networkTimeout`.

---

## Magic Numbers and Strings

Surface signals:

- `Duration.seconds(30)` or `TimeInterval(30)` scattered across files → extract `static let requestTimeout: Duration = .seconds(30)`.
- `if retries < 3` literal → `static let maxRetries = 3`.
- Repeated `"com.acme.app.notification"` string keys → `extension Notification.Name { static let userDidLogin = Self("com.acme.app.notification.userDidLogin") }`.

Rules:

- Prefer `static let` over computed property for compile-time constants.
- Namespace constants on the type they belong to:

```swift
extension HTTPClient {
    static let defaultTimeout: Duration = .seconds(30)
    static let maxRetries: Int = 3
}
```

- For URLs, declare typed wrappers; don't pass `String` everywhere and rely on `URL(string:)!`.
- For asset / SF Symbol names, prefer Xcode 15+ generated asset symbols or an `enum` namespace; never sprinkle raw `"icon.gear"` literals.

Anti-signal: a constant used in exactly one place may belong as a `let` next to the use site.

---

## Concurrency Refactors (Approachable Concurrency)

Swift 6.2's Approachable Concurrency mode changes default isolation. Refactor targets:

### `@MainActor` everywhere → fine-grained isolation

```swift
// Before — heavy hammer
@MainActor
final class OrderService {
    func fetchAll() async -> [Order] { /* 90% pure compute */ }
    func render() { /* needs main */ }
}

// After (6.2)
final class OrderService {
    nonisolated func fetchAll() async -> [Order] { /* runs anywhere */ }
    @MainActor func render() { /* explicitly main */ }
}
```

### `withCheckedContinuation` → `AsyncStream` builder

```swift
// Before
func observe(_ name: Notification.Name) -> AsyncStream<Notification> {
    AsyncStream { cont in
        let token = NotificationCenter.default.addObserver(forName: name, object: nil, queue: nil) {
            cont.yield($0)
        }
        cont.onTermination = { _ in NotificationCenter.default.removeObserver(token) }
    }
}
```

(That's already the post-refactor form — the smell is *manual continuation handling for every delegate*. Convert push-style delegates to `AsyncStream` once at the boundary.)

### `@unchecked Sendable` retrofit → real `Sendable`

`@unchecked` mutes the compiler, not the data race. Replace with:
- `actor` for mutable shared state.
- `let` properties on a `final class` with all `Sendable` fields.
- Mutex-backed wrapper if you genuinely need `class` semantics: `Mutex<T>` (6.0+).

---

## Refactor Anti-Patterns to Avoid

Things that look like refactors but degrade the design:

| Anti-pattern | Why it hurts | Better path |
|--------------|--------------|-------------|
| Retrofitting `!` IUO (`var x: User!`) to "fix" optionals | Defers the crash to runtime; the field is logically required but the type system doesn't enforce it | Constructor injection + non-optional `let user: User` |
| Wrapping every value type in a `class` because "easier mutation" | Reference semantics + ARC overhead + shared-state bugs; loses copy-on-write benefits | `struct` + `inout` parameters; reach for `class` only when you need identity |
| Mass migrating Combine → AsyncSequence on stable code | Big diff, no behavior win, breaks downstream subscriptions | Migrate only at the natural seam (new feature, new view) |
| Sprinkling `@MainActor` to silence warnings | UI thread bottleneck; turns the whole app into a serial queue | Per-method isolation; `nonisolated` where compute is pure |
| `as!` to suppress a compile error | Same as force-unwrap — runtime crash deferred | `as?` + early-return; or `throws` typed init |
| Replacing `class` with `struct` reflexively | Some types are correctly reference types (identity, observation, large mutating state) | Use the semantics test: "does identity matter?" |
| Bulk renaming with Xcode refactor across a public API | Breaks callers; SemVer-level change disguised as cleanup | Public-API renames need deprecation: `@available(*, deprecated, renamed:)` |
| Removing `try?` to "use proper errors" without handling | Replaces silent nil with crashing throw | Decide at the call site: silently fail (`try?`) vs propagate (`try`) vs handle (`do/catch`) — never reflexively |
| Extracting every closure into a named method | Disrupts locality; SwiftUI bodies and result builders read worse | Extract only when reuse, testability, or 4+ captures justify it |

---

## Refactor Checklist

Run before declaring a Swift refactor done:

1. **Build clean**: `swift build` or Xcode `Cmd+B`. No warnings.
2. **Lints pass**: `swiftlint --strict` (or whatever the project pins).
3. **Format**: `swift-format lint --recursive .` (or `swiftformat --lint .`).
4. **Tests stay green**: `swift test` / `xcodebuild test`.
5. **No new `try!` / `!` IUO / `as!`** outside test code.
6. **Concurrency check passes**: `swift build -strict-concurrency=complete` (or `SWIFT_STRICT_CONCURRENCY=complete`).
7. **Public API surface unchanged** (or intentionally changed): if you maintain a library, diff `swift package diagnose-api-breaking-changes`.
8. **SwiftUI previews still build** if you touched views.
9. **Swift Testing or XCTest discovery still finds renamed cases** — `xcodebuild test -only-testing:...`.
10. **No `@unchecked Sendable` introduced** without an accompanying SAFETY comment.

If any of these change unexpectedly, the refactor altered behavior — back out and reframe.

---

## Where to dig deeper

- Bad-pattern catalog: [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md)
- Target idioms: [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md)
  - §1 API Design Guidelines, §2 Concurrency, §7 Testing, §8 Performance
- Language surface: [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md)
  - Typed throws (§6.2), `@Observable` (§8.2), Approachable Concurrency (§3.11), `~Copyable` (§2.2), macros (§5)
