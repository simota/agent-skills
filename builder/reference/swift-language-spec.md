# Swift Language Spec — Deep Dive Reference

> Companion to the broader Swift knowledge in this `builder/reference/` directory. This file covers the language specification, type system mechanics, concurrency model, ownership, macros, and the stable feature timeline in depth. The `native` skill complements this for SwiftUI / Liquid Glass / iOS-platform-specific concerns.
>
> Baseline: Swift 6.2+ / Xcode 26 (as of 2026-05). Field-A flagged Swift 6.3 (Mar 2026) outlook where relevant.

---

## Table of Contents

1. [Version Timeline & Major Shifts](#1-version-timeline--major-shifts)
2. [Ownership Model (post 5.9)](#2-ownership-model-post-59)
3. [Concurrency Model](#3-concurrency-model)
4. [Type System](#4-type-system)
5. [Macros (5.9+)](#5-macros-59)
6. [Error Handling](#6-error-handling)
7. [Result Builders](#7-result-builders)
8. [Property Wrappers vs Macros](#8-property-wrappers-vs-macros)
9. [Memory Model & ARC](#9-memory-model--arc)
10. [C / C++ / Objective-C Interop & Embedded Swift](#10-c--c--objective-c-interop--embedded-swift)
11. [Module System & Access Control](#11-module-system--access-control)
12. [Per-Release Feature Table (5.10 → 6.2)](#12-per-release-feature-table-510--62)
13. [Unstable / In-Evolution Features (Swift 6.3 Outlook)](#13-unstable--in-evolution-features-swift-63-outlook)
14. [Code Examples — Non-obvious mechanics](#14-code-examples--non-obvious-mechanics)
15. [Sources](#sources)

> **Cross-links:**
> - Production library choices, error-handling crates, testing strategy → [`swift-best-practices.md`](./swift-best-practices.md)
> - Concrete misuse of each spec feature (`@unchecked Sendable` traps, actor reentrancy bugs, force unwraps, FFI) → [`swift-anti-patterns.md`](./swift-anti-patterns.md)
> - SwiftUI / Liquid Glass / iOS HIG / Apple Intelligence / Foundation Models → [`../../native/SKILL.md`](../../native/SKILL.md)

---

## 1. Version Timeline & Major Shifts

Swift evolved from a deliberately small async story (5.0) into a language with first-class concurrency safety, ownership, macros, and a viable embedded subset. The shifts that matter for 2026 code:

| Version | Release | Major language shifts |
|---------|---------|------------------------|
| 5.0 | 2019-03 | **ABI stability** on Apple platforms (binary compatibility) |
| 5.5 | 2021-09 | `async`/`await`, structured concurrency (`Task`, `TaskGroup`, `async let`), `actor`, `Sendable`, `@MainActor`, `@globalActor` (SE-0296, SE-0297, SE-0302, SE-0304, SE-0306, SE-0316) |
| 5.6 | 2022-03 | `any` keyword for existentials (SE-0335); `#unavailable` |
| 5.7 | 2022-09 | **Primary associated types** (`Collection<Int>`), `some` in parameter position, opaque-result improvements, generics shorthand, distributed actors (SE-0336/0344/0341) |
| 5.8 | 2023-03 | Conditional unwrap simplification, `swift-syntax` mainlined |
| 5.9 | 2023-09 | **Macros** (SE-0382, SE-0389, SE-0397), **parameter packs / variadic generics** (SE-0393, SE-0398), `~Copyable` noncopyable structs/enums (SE-0390), `consuming`/`borrowing`/`consume` (SE-0366, SE-0377), `package` access (SE-0386), C++ interop (SE-0407), `if`/`switch` expressions (SE-0380) |
| 5.10 | 2024-03 | **Complete strict-concurrency checking** opt-in, `nonisolated(unsafe)` keyword, full data-isolation closes Swift 5 isolation holes |
| 6.0 | 2024-09 | **Swift 6 language mode**: complete concurrency default-on; **typed throws** `throws(E)` stable (SE-0413); **region-based isolation** (SE-0414); **sending** parameters (SE-0430); **noncopyable generics** (SE-0427); 128-bit integers (SE-0425); `count(where:)`; `@attached(body)` macros (SE-0415); Swift Testing; `Synchronization` module — `Atomic` (SE-0410) + `Mutex` (SE-0433); Embedded Swift first ship |
| 6.1 | 2025-03 | Refinements to region-based isolation; diagnostic groups; misc. Sendable inference improvements |
| 6.2 | 2025-09 | **Approachable Concurrency**: `nonisolated(nonsending)` default for async functions, `@concurrent` attribute, `-default-isolation MainActor` mode (SE-0461 family); **raw identifiers** (SE-0451); `weak let`; `InlineArray` `[N of T]`; `Span` / `MutableSpan` (SE-0447, SE-0467); `Observations` async sequence; method key paths; opt-in strict memory safety; safer C++ interop |
| 6.3 (Mar 2026) | — | Embedded Swift exits experimental; Android official target; embedded LLDB; further Approachable Concurrency refinements |

Two policy shifts dominate 2026 code:

- **Strict concurrency is mandatory.** Swift 6 mode treats every data-race possibility as a compile error.
- **"Approachable Concurrency" inverts the async default.** In Swift 6.2 with the upcoming-feature flag enabled (or under `-default-isolation MainActor`), `async` no longer hops off the caller's actor by default — code "stays put" unless you explicitly opt into parallelism with `@concurrent`.

This is the **single largest semantic change of 2026**. See §3.11.

---

## 2. Ownership Model (post 5.9)

Swift's ownership story is layered on top of ARC. Three families of features:

### 2.1 Parameter ownership modifiers (SE-0377, Swift 5.9)

- `borrowing` — function accesses the value without taking ownership; no bond/release pair for class instances. Roughly C++ const&. Borrowed parameters cannot be consumed inside the body.
- `consuming` — caller transfers ownership; function may consume (deinit / move) the value. Compiler will diagnose continued use of the consumed binding at the call site (for `~Copyable` types).
- Both are mutually exclusive with `inout`. Both make the parameter binding non-implicitly-copyable inside the function body — explicit `copy x` is required to materialize a copy.

```swift
func sum(_ data: borrowing Data) -> Int        // no ARC traffic for class containers
func handoff(_ pipe: consuming Pipe)           // pipe is destroyed inside; caller loses it
```

### 2.2 `~Copyable` (noncopyable) types (SE-0390, Swift 5.9; generics SE-0427, Swift 6.0)

`~Copyable` *suppresses* the otherwise-default `Copyable` conformance. Instances have at most one owner at a time, modeled on Rust's move semantics.

```swift
struct FileHandle: ~Copyable {
    private let fd: Int32
    init(path: String) throws(POSIXError) { /* … */ }
    deinit { close(fd) }
}

func readAll(_ h: borrowing FileHandle) -> Data { /* … */ }
```

Key rules:

- Cannot be stored in `Array`, `Dictionary`, `Set`, etc. *unless* the container is itself written to be noncopyable-aware.
- `class` instances are always `Copyable` because references are copyable; `~Copyable` applies to `struct`/`enum`.
- `deinit` is supported on `~Copyable` `struct`/`enum` (new for value types).

In Swift 6.0 (SE-0427), generic parameters can be `~Copyable`:

```swift
func consumeBoth<T: ~Copyable, U: ~Copyable>(_ a: consuming T, _ b: consuming U) { … }
```

Subsequent stdlib proposal SE-0437 generalized `Optional<Wrapped: ~Copyable>` and `Result<Success: ~Copyable, Failure>`, enabling `Optional<FileHandle>` etc.

### 2.3 `consume` operator (SE-0366, Swift 5.9)

`consume x` ends the lifetime of binding `x` and yields its current value:

```swift
var pipe = makePipe()         // var so we can rebind later
let owned = consume pipe      // pipe is no longer usable here
// use(pipe)                  // compile error
```

For `~Copyable` types this is the only way to transfer ownership out of a binding without `consuming` parameter convention.

### 2.4 `~Escapable` (SE-0446, Swift 6.2)

A second suppressible constraint. `~Escapable` types cannot outlive the scope of their creation — they cannot be returned, captured by escaping closures, or stored where the lifetime could exceed the producer's lifetime. This is the foundation for `Span` (SE-0447), which is a non-escapable view onto contiguous memory:

```swift
extension Array {
    var span: Span<Element> { /* compiler-guaranteed safe view */ }
}

let arr = [1, 2, 3]
let view: Span<Int> = arr.span    // borrowing; cannot escape arr's lifetime
```

`~Escapable` and lifetime-dependency annotations (`@lifetime` family) are still on a maturation curve — see §13.

---

## 3. Concurrency Model

Swift's concurrency model has four pillars: **structured tasks**, **actors**, **Sendable**, and **isolation regions**. The 2026 baseline assumes **Swift 6 language mode** with strict concurrency checking and the Swift 6.2 "approachable" defaults.

### 3.1 async/await fundamentals (Swift 5.5)

`async` functions can suspend. `await` is the suspension point. Suspending does *not* block the current thread — the runtime parks the task and schedules other work.

```swift
func fetch(_ url: URL) async throws(URLError) -> Data {
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}
```

### 3.2 Structured concurrency

Three primitives in increasing order of dynamism:

| Primitive | Use when | Cancellation |
|-----------|----------|--------------|
| `async let x = …` | Fixed, small fan-out known at compile time | On scope exit (auto) |
| `withTaskGroup(of:)` / `withThrowingTaskGroup(of:)` | Dynamic fan-out, results collected | On scope exit; results harvested via `for await` |
| `withDiscardingTaskGroup(returning:)` / `withThrowingDiscardingTaskGroup` (SE-0381, 5.9) | Long-running fan-out where individual results aren't needed (servers, supervisors) | Cleans up child tasks as they finish — no per-task accumulation |

`async let` and task groups are *structured*: parent waits for children at scope exit. Child tasks inherit the parent's task-local values and priority, and cancellation propagates parent → child automatically.

```swift
func loadDashboard() async throws -> Dashboard {
    async let user   = api.user()
    async let recent = api.recent()
    async let stats  = api.stats()
    return try await Dashboard(user: user, recent: recent, stats: stats)
}
```

### 3.3 Unstructured tasks

`Task { … }` creates an unstructured top-level task — useful at the boundary between sync and async (e.g., a SwiftUI button handler). Unstructured tasks **do not** inherit cancellation from their lexical parent; they live until they finish or are explicitly cancelled via their handle. `Task.detached { … }` additionally drops task-local context and isolation inheritance.

### 3.4 Cancellation model (cooperative)

- `Task.isCancelled` / `try Task.checkCancellation()` — explicit polling.
- `withTaskCancellationHandler(operation:onCancel:)` — for bridging non-cooperative APIs (e.g., URLSession data tasks pre-async, file watchers).
- Cancellation is **cooperative**: a cancelled task continues running until it yields at an `await` *and* the awaited operation honors cancellation. `Task.sleep` and `URLSession`'s async methods throw `CancellationError` on cancel.

```swift
func download(_ url: URL) async throws -> Data {
    try await withTaskCancellationHandler {
        try await session.data(from: url).0
    } onCancel: {
        session.invalidateAndCancel()   // sync, escape hatch
    }
}
```

### 3.5 Sendable & data-race safety

`Sendable` marks types safe to transfer across isolation boundaries. Conformance is checked, but:

- Value types whose stored members are all `Sendable` get **auto-conformance** in the same module.
- `actor` types are implicitly `Sendable` (their isolation handles synchronization).
- `final class` instances with only `let` `Sendable` stored properties can conform — or use `@unchecked Sendable` (assert by hand).
- Closures use the **type attribute** `@Sendable` to require captures be Sendable.
- `nonisolated(unsafe)` (5.10) is the escape hatch on storage when you've manually proven safety.

```swift
struct UserID: Sendable { let raw: UUID }      // auto

final class Logger: Sendable {                 // manual final + immutable
    let queue: DispatchQueue
    init(queue: DispatchQueue) { self.queue = queue }
}

let f: @Sendable (Int) -> Int = { $0 + 1 }
```

For the runtime trap behavior when `@unchecked Sendable` is mis-applied to closure-bearing types, see [`swift-anti-patterns.md` §3.3](./swift-anti-patterns.md#33-unchecked-sendable-runtime-crash-mode).

### 3.6 Actors

```swift
actor Counter {
    private var value = 0
    func incr() { value += 1 }          // isolated; cross-actor calls need await
    nonisolated let id: UUID = UUID()   // immutable, callable from anywhere
    nonisolated func describe() -> String { "Counter(\(id))" }
}

let c = Counter()
await c.incr()       // cross-actor hop → await required
print(c.id)          // nonisolated — no await
```

Key rules:

- All actor-isolated methods are implicitly `async` when called from outside.
- **Actor reentrancy**: when an isolated method suspends at `await`, *other* tasks may run on the actor before the suspended one resumes. Therefore `self.state` may have changed across an `await`. Always re-validate after suspension. See [`swift-anti-patterns.md` §3.2](./swift-anti-patterns.md#32-actor-reentrancy-the-classic-state-stale-bug).

### 3.7 Global actors & `@MainActor`

A global actor is a singleton actor referred to by an attribute:

```swift
@globalActor actor Database {
    static let shared = Database()
}

@Database func upsert(_ row: Row) { … }   // hopped to Database on call
```

`@MainActor` is the canonical example — all UI code runs there. In Swift 6.2 you can additionally compile with `-default-isolation MainActor` so *every* declaration in the module is `@MainActor` unless explicitly marked otherwise — ideal for app targets. For SwiftUI-specific patterns layered on this, see [`../../native/SKILL.md`](../../native/SKILL.md).

### 3.8 Isolated parameters (SE-0313 / SE-0420)

A function can take an isolation parameter to operate on whichever actor the caller is using:

```swift
func mutate(_ actor: isolated Counter) {
    actor.value += 1     // synchronous — already isolated
}
```

`isolated (any Actor)?` (SE-0420) lets generic helpers inherit caller isolation.

### 3.9 Region-based isolation (SE-0414, Swift 6.0; refined 6.1)

The compiler tracks *isolation regions* — sets of non-`Sendable` values whose lifetimes are entangled. A value can be safely sent across an isolation boundary if its region is *disconnected* (no live aliases outside the call). This eliminates many false positives:

```swift
func send() async {
    let widget = Widget()         // non-Sendable, fresh region
    await store.add(widget)       // OK: region is disconnected at the call
    // widget no longer usable here (it was "sent")
}
```

The key is that the compiler reasons about *which uses can race*, not whether the type is annotated `Sendable`. Result: less ceremony, fewer `Sendable` conformances needed in app code.

### 3.10 `sending` parameters (SE-0430, Swift 6.0)

Marks a parameter or result as transferred between isolation domains. Used by library authors to declare APIs that take ownership of a non-Sendable value safely:

```swift
func enqueue(_ work: sending () -> Void) { … }
```

The compiler then proves the caller's region is disconnected at the call site.

### 3.11 `nonisolated(nonsending)` & `@concurrent` (Swift 6.2 — the biggest 2026 semantic change)

This is the **defaults flip** of 6.2. Pre-6.2, an `async` `nonisolated` function would hop to the global concurrent executor and run there. Code on `@MainActor` calling it would leave the main thread.

Under Swift 6.2's *approachable concurrency* (upcoming feature `NonisolatedNonsendingByDefault`), `nonisolated` async functions instead default to **`nonisolated(nonsending)`**: they run on the caller's actor (no hop). Parameters effectively gain `sending` semantics. This makes async functions behave like sync functions for actor placement.

To explicitly opt back into "may run anywhere" semantics, use `@concurrent`:

```swift
nonisolated(nonsending) func parse(_ raw: Data) async throws -> Item { … }
//  ^ runs on caller's actor — no hop, no Sendable parameter requirement.

@concurrent
func crunch(_ data: Data) async -> Stats { … }
//  ^ may run on any thread of the cooperative pool; parameters must be Sendable.
```

Mental model:

| Attribute | Where it runs | Parameter requirements |
|-----------|---------------|------------------------|
| Default (`nonisolated`) pre-6.2 | Cooperative pool (any thread) | Implicitly Sendable-checked |
| `nonisolated(nonsending)` (6.2 default) | Caller's actor | Sending semantics (transferable) |
| `@concurrent` (6.2) | Cooperative pool | Sendable required |
| `@MainActor` | Main actor | Sendable required at boundary |

Plus 6.2 ships `-default-isolation MainActor` for *the entire module* to be MainActor-by-default — a big quality-of-life win for UI-heavy targets.

**Swift 6.3 outlook (Mar 2026):** the migration tooling and diagnostics continue to mature; the feature flag is on a path toward becoming the default in Swift 7. Expect refinements based on community migration experience. See [`swift-best-practices.md` §2.2](./swift-best-practices.md#22-approachable-concurrency-se-0466--default-isolation) for the production-side decision matrix.

### 3.12 `AsyncSequence` family

- `AsyncSequence` — async analog of `Sequence`; `for try await x in seq { … }`.
- `AsyncStream<T>` / `AsyncThrowingStream<T, Failure>` (SE-0314, Swift 5.5+) — bridge callback-based APIs into AsyncSequence. Buffering policy (`bufferingNewest` / `bufferingOldest` / `unbounded`) configurable at construction.
- `Observations` (Swift 6.2) — an `AsyncSequence` of transactional state changes for `@Observable` types.

```swift
let stream = AsyncStream<Event> { continuation in
    let sub = NotificationCenter.default.addObserver(...) { n in
        continuation.yield(Event(n))
    }
    continuation.onTermination = { _ in NotificationCenter.default.removeObserver(sub) }
}

for await event in stream { handle(event) }
```

### 3.13 Continuations

`withCheckedContinuation` / `withCheckedThrowingContinuation` — bridge a completion-handler API into async/await. Checked variants verify that `resume` is called *exactly once*. `withUnsafe…` skip the check for perf-critical paths.

```swift
func legacyFetch() async throws -> Data {
    try await withCheckedThrowingContinuation { cont in
        legacy.fetch { data, err in
            if let err { cont.resume(throwing: err) } else { cont.resume(returning: data!) }
        }
    }
}
```

For the double-resume and never-resume pitfalls and a verified safe wrapper, see [`swift-anti-patterns.md` §3.6](./swift-anti-patterns.md#36-continuation-safety-wrapper).

### 3.14 Low-level synchronization (Swift 6.0)

The `Synchronization` module ships two primitives:

- `Atomic<Value: AtomicRepresentable>` (SE-0410) — must be declared `let` (compiler diagnoses `var` to prevent accidental exclusivity issues).
- `Mutex<State>` (SE-0433) — cross-platform `os_unfair_lock` analog, unconditionally `Sendable`, works with both `Copyable` and `~Copyable` value types thanks to noncopyable generics.

`Mutex` is the recommended primitive when actor's async-only access pattern is too heavy (e.g., synchronous hot paths). Actors remain preferred for higher-level state.

---

## 4. Type System

### 4.1 Protocols, `some`, `any`

- `some P` — opaque type. The compiler picks one concrete type; callers can't see it. Available in return position (5.1), and in **parameter position** (5.7). In param position `func f(_ x: some Sequence<Int>)` is shorthand for a generic.
- `any P` — boxed existential (5.6). Heap-allocated, dynamic dispatch. Required when the protocol has `Self`/associated-type requirements **unless** the existential is constrained.
- **Primary associated types** (SE-0346, Swift 5.7) let you write `Collection<Int>` (where `Element == Int`) at use sites, both in `some` and `any` positions.

```swift
func process(_ xs: some Collection<Int>) { … }   // generic, no box
func describe(_ xs: any Collection<Int>) { … }   // existential, dynamic
```

Cheat sheet:

- Returns of a concrete-but-private type → `some`.
- Heterogeneous storage / type erasure → `any`.
- Without primary associated types, `any Collection` (unbound) can't be subscripted or iterated — most uses need `<Int>` constraint.

### 4.2 Generics: parameter packs (SE-0393, Swift 5.9; SE-0398 variadic types)

Variadic generics let one function or type abstract over an arbitrary number of types/values:

```swift
struct Tuple<each Element> {
    var values: (repeat each Element)
}

func zip<each S: Sequence>(_ seqs: repeat each S)
    -> [(repeat (each S).Element)] { … }

// At call site:
let z = zip([1,2,3], ["a","b","c"], [true,false,true])
// inferred: zip<Array<Int>, Array<String>, Array<Bool>>
```

Keywords:

- `each T` — reference to a pack element.
- `repeat <pattern>` — pack expansion; the pattern is instantiated once per element.
- Iteration: `for value in repeat each pack { … }` (Swift 6.0, SE-0408).

Practical impact: SwiftUI's "10 views per ViewBuilder" limit dissolved once variadic generics shipped.

### 4.3 Conditional & retroactive conformances

- Conditional conformance (existing): `extension Array: Equatable where Element: Equatable { }`.
- **Retroactive conformance warning** (SE-0364, Swift 5.9+): conforming a type you don't own to a protocol you don't own (e.g., `Foundation.URL: Identifiable` from your module) triggers a warning. Silence with `extension URL: @retroactive Identifiable { … }` — and only do it when you accept the duplicate-conformance risk.

### 4.4 Constrained existentials

`any Collection<Int>` is a *constrained existential* (SE-0353, 5.7). Without the constraint, many operations on `any Collection` are unusable because associated types are erased.

### 4.5 `~Copyable` as a generic constraint (SE-0427, Swift 6.0)

`<T: ~Copyable>` opts the type parameter out of requiring `Copyable`. Used heavily by stdlib types in 6.0+ (`Optional<Wrapped: ~Copyable>`, `Result<Success: ~Copyable, _>`, `Mutex<State: ~Copyable>`).

This is one of the **largest type-system additions of Swift 6.0** — together with typed throws (§6.2) and region-based isolation (§3.9). It enables move-only abstractions inside the generic system without requiring noncopyable-aware containers everywhere.

---

## 5. Macros (Swift 5.9+)

Macros are *Swift code that generates Swift code*. They run at compile time via a separate process (the macro plugin) and operate on SwiftSyntax trees.

### 5.1 Two flavors

- **Freestanding** macros (SE-0382): `#foo(...)` — used in expression or declaration position. Examples: `#warning("…")`, `#expect(...)` in Swift Testing.
- **Attached** macros (SE-0389): `@Foo` on a declaration. They can add peers, accessors, members, attributes, extensions, or function bodies.

### 5.2 Attached macro roles (SE-0389 + SE-0415)

| Role | Adds | Example |
|------|------|---------|
| `peer` | Sibling declarations at the same scope | Generate a `…CodingKeys` enum next to a struct |
| `accessor` | Getters/setters/observers on a property | Bridge a property to backing storage |
| `member` | New members inside the type/extension | `@Observable` adds `_$observationRegistrar` |
| `memberAttribute` | Attaches further attributes to existing members | Mark all stored properties `@MainActor` |
| `extension` | Adds an extension (often for conformance) | `@Observable` adds `: Observable` conformance |
| `body` (SE-0415, Swift 6.0) | Synthesizes or rewrites a function body | Logging, tracing wrappers |

A single macro can declare multiple roles (`@attached(member, names: ...) @attached(extension, ...) macro Observable() = ...`).

### 5.3 SwiftSyntax plugin architecture

A macro package has two products:

1. **Library** — declares the macro: `@freestanding(expression) macro stringify<T>(_ value: T) -> (T, String) = #externalMacro(module: "MyMacrosPlugin", type: "StringifyMacro")`
2. **Executable plugin** (`CompilerPlugin`) — implements the macro by emitting SwiftSyntax nodes. Runs as a sandboxed subprocess invoked by the compiler.

```swift
import SwiftSyntax
import SwiftSyntaxMacros
import SwiftCompilerPlugin

public struct StringifyMacro: ExpressionMacro {
    public static func expansion(
        of node: some FreestandingMacroExpansionSyntax,
        in context: some MacroExpansionContext
    ) -> ExprSyntax {
        guard let arg = node.arguments.first?.expression else {
            return "(.empty, \"\")"
        }
        return "(\(arg), \(literal: arg.description))"
    }
}

@main struct MyMacrosPlugin: CompilerPlugin {
    let providingMacros: [Macro.Type] = [StringifyMacro.self]
}
```

### 5.4 Hygiene

`MacroExpansionContext.makeUniqueName(_:)` generates collision-free identifiers — essential for emitting helper names that won't conflict with user code. Macros can't (by design) refer to identifiers from the call-site scope unless explicitly captured via the syntax tree.

### 5.5 Diagnostics

Macros emit warnings/errors via `context.diagnose(_:)`, with attached fix-its built from SwiftSyntax. Production macros (e.g., `@Observable`, `@AddCompletionHandler`) ship rich diagnostics.

### 5.6 Common stdlib & framework macros

| Macro | Role | Ships with |
|-------|------|------------|
| `@Observable` | member + extension | Observation (5.9) |
| `@DebugDescription` | member | Stdlib (6.0) |
| `@Test`, `@Suite`, `#expect`, `#require` | various | Swift Testing (6.0) |
| `@Entry` | accessor | SwiftUI 2024 |
| `@Model` | member + extension | SwiftData |

---

## 6. Error Handling

### 6.1 Classic `throws`

Functions declared `throws` may throw *any* `Error`:

```swift
func parse(_ s: String) throws -> Int { … }
```

Call sites use `try`, `try?` (→ `Optional`), or `try!` (trap on throw). `rethrows` propagates throwing-ness from closure parameters; with typed throws it becomes redundant in many cases.

### 6.2 Typed throws (SE-0413, stable in Swift 6.0)

You can now declare the error type:

```swift
enum ParseError: Error { case empty, badChar(Character) }

func parse(_ s: String) throws(ParseError) -> Int { … }
```

Key relationships:

- `throws` (untyped) is exactly `throws(any Error)`.
- A non-throwing function is exactly `throws(Never)`.
- Catch blocks see a typed error: `do { … } catch { /* error: ParseError */ }`.

`do throws(MyErr) { … }` explicitly types the do-block, useful when inference would otherwise widen to `any Error`.

When to use:

- **Internal APIs** with a closed, stable error set — strong typing pays off.
- **Public library APIs** — usually keep untyped `throws` for flexibility; otherwise adding a case is source-breaking.

For the full production decision matrix, see [`swift-best-practices.md` §3.2](./swift-best-practices.md#32-typed-throws-swift-60--when-worth-it).

**Swift 6.3 outlook:** closure-side inference for typed throws (SE-0413 originally proposed it, then deferred) is still pending. Until it lands, generic closures often widen back to `throws(any Error)`, limiting typed-throws utility in higher-order code.

### 6.3 `Result<Success, Failure>`

Pre-async-await idiom; remains useful for serializing failures over Combine, storing failures in arrays, or passing them through `@Sendable` closures. With SE-0437, `Result<Success: ~Copyable, Failure>` works for noncopyable success types.

### 6.4 Async + throws

Async throws compose: `func f() async throws(NetworkError) -> Data`. Cancellation is delivered as a thrown `CancellationError` (untyped). When mixing with typed throws, the function must list a type that can represent both your domain errors and cancellation, or rethrow `CancellationError` as `any Error`.

---

## 7. Result Builders

Originally `@_functionBuilder` (pre-5.4, internal), stabilized as `@resultBuilder` in SE-0289 (Swift 5.4).

A type marked `@resultBuilder` provides static methods the compiler calls to lower a DSL-style body into a single expression:

| Static method | Purpose |
|---------------|---------|
| `buildBlock(_:)` | Required. Combines siblings. |
| `buildExpression(_:)` | Optional. Wraps each statement. |
| `buildOptional(_:)` | Handles `if` without `else`. |
| `buildEither(first:)` / `buildEither(second:)` | Handles `if/else` and `switch`. |
| `buildArray(_:)` | Handles `for` loops. |
| `buildLimitedAvailability(_:)` | Handles `if #available`. |
| `buildFinalResult(_:)` | Final post-processing. |
| `buildPartialBlock(first:)` / `buildPartialBlock(accumulated:next:)` (SE-0348, 5.7) | Recursive pairwise build — reduces overload explosion from O(arity!) to O(arity²). |

```swift
@resultBuilder enum Bullets {
    static func buildBlock(_ parts: String...) -> String {
        parts.map { "• \($0)" }.joined(separator: "\n")
    }
    static func buildEither(first: String) -> String  { first }
    static func buildEither(second: String) -> String { second }
    static func buildOptional(_ part: String?) -> String { part ?? "" }
}

@Bullets var list: String {
    "Apples"
    "Bananas"
    if includeCitrus { "Oranges" } else { "" }
}
```

SwiftUI's `ViewBuilder`, regex builders, and Swift Testing's `#expect` matchers all use this machinery.

---

## 8. Property Wrappers vs Macros

### 8.1 Property wrappers (SE-0258, Swift 5.1)

`@propertyWrapper` wraps a property with backing storage exposing `wrappedValue` and (optionally) `projectedValue` (accessed via `$x`).

Limitations that motivated macros:

- One wrapper per property.
- `wrappedValue` is one concrete type; can't synthesize protocol conformances on the *outer* type.
- Hard to mutate sibling properties or generate methods.

### 8.2 Macros take over

- `@Observable` (member + extension macro) supersedes `@Published`/`ObservableObject`. It rewrites the class to register reads through an `ObservationRegistrar`, so SwiftUI can track *per-property* reads in a view instead of triggering on every change of an `ObservableObject`.
- Inside an `@Observable` class, you no longer mark properties `@Published`; mixing the two is forbidden.
- State ownership pairing:
  - `ObservableObject` + `@StateObject` (legacy)
  - `@Observable` + `@State` (Swift 5.9+/iOS 17+)

```swift
@Observable
final class CartModel {
    var items: [Item] = []
    var total: Decimal = 0
}

struct CartView: View {
    @State private var model = CartModel()       // owning instance
    var body: some View { Text("\(model.total)") }
}
```

Property wrappers remain the right tool for things that *aren't* state observation: `@AppStorage`, `@Environment`, `@FocusState`, `@Binding`, `@FetchRequest`.

For the iOS-17+ `@StateObject` → `@State` init-lifecycle gotcha (init now runs on every view rebuild), see [`swift-anti-patterns.md` §7.2](./swift-anti-patterns.md#72-observable-vs-observableobject-init-lifecycle-gotcha). SwiftUI-specific binding patterns belong in [`../../native/SKILL.md`](../../native/SKILL.md).

---

## 9. Memory Model & ARC

### 9.1 ARC fundamentals

Classes are reference-counted. Each instance has three counts internally — strong, unowned, and weak (the latter via side tables). Value types (`struct`, `enum`) are not reference-counted unless they transitively contain class fields.

### 9.2 Reference qualifiers

| Qualifier | Storage | Lifetime guarantee | Crash on dangling |
|-----------|---------|--------------------|-------------------|
| (default) `strong` | non-Optional or Optional | Keeps referent alive | N/A |
| `weak` | Optional only | Goes to `nil` when referent deallocs | No |
| `unowned` | non-Optional | Asserts referent outlives reference | Yes (assertion) |
| `unowned(unsafe)` | non-Optional | Same as unowned but no runtime check | Use-after-free if violated |

Capture lists for closures: `[weak self]` (Optional), `[unowned self]` (non-Optional, must outlive), or implicit strong.

### 9.3 Reference cycles

Swift does not cycle-collect. Two classes that hold strong refs to each other (directly or via a closure capture) leak. Break with `weak`/`unowned`. Classic cycle: `parent → child.parent` should be `weak`.

For the catalog of cycle shapes and `[weak self]` / `[unowned self]` decision matrices, see [`swift-anti-patterns.md` §2](./swift-anti-patterns.md#2-reference-cycle-pitfalls).

### 9.4 `weak let` (Swift 6.2)

Until 6.2, `weak` required `var` because the runtime needed to write `nil` into the variable on deallocation. In 6.2, `weak let` is permitted — the binding is *re-readable* as Optional but cannot be reassigned by user code; the runtime zeroes it on dealloc.

### 9.5 `final class` performance

`final class` allows the compiler to devirtualize calls (no vtable lookup), which matters in hot paths. In Swift 6 strict-concurrency mode, `final class` is also a prerequisite for many `Sendable` conformances on classes (along with `let`-only stored properties of `Sendable` types).

### 9.6 `class` vs `struct` semantics

- `struct` — value semantics, copied on assignment, no ARC on the value itself (CoW for stdlib collections).
- `class` — reference semantics, identity, deinit, inheritance, ARC.
- Defaults strongly favor `struct`; reach for `class` for identity, shared mutable state behind synchronization (actor wraps a class internally), large objects whose copying would be wasteful, or interop with Objective-C / inheritance hierarchies.

### 9.7 Objective-C bridging

- `@objc` exposes a Swift declaration to ObjC's dynamic runtime. Required for KVO, `#selector`, NSCoding (manual), some `NotificationCenter` patterns.
- `NSObject` subclasses automatically expose much of their surface to ObjC.
- `autoreleasepool { … }` remains relevant when calling Cocoa APIs in tight loops (e.g., `UIImage` from `CGImage`); pure Swift code does not need it.

---

## 10. C / C++ / Objective-C Interop & Embedded Swift

### 10.1 C interop

- Modular C headers imported as Swift modules (`import Darwin.POSIX`, etc.).
- `@_cdecl("name")` exposes a Swift function with C ABI. Underscored → not part of stable language, but widely used.
- `@convention(c)` declares a function type uses the C calling convention — required when passing Swift closures to C APIs taking function pointers. Captures are forbidden.
- `@convention(block)` for Objective-C block ABI.

```swift
@_cdecl("swift_compute") public func compute(_ x: Int32) -> Int32 { x * x }

let cb: @convention(c) (Int32) -> Int32 = { x in x + 1 }
qsort_b(/* … */ cb /* … */)
```

### 10.2 C++ interop (Swift 5.9+, stabilizing through 6.2)

- Enable via `-cxx-interoperability-mode=default` (or SwiftPM `interoperabilityMode: .Cxx`).
- `import CxxStdlib` exposes `std.string`, `std.vector<T>`, etc. — the `std` namespace becomes a Swift `enum` (a namespace tool).
- Move-only C++ types map to Swift `~Copyable`. Use the `SWIFT_NONCOPYABLE` annotation on the C++ side.
- Swift 6.0 added support for default arguments, virtual methods, and richer template handling.
- Swift 6.2 added a **safe interop mode** that flags unsafe pointer / span uses at compile time; `std::span<T>` now bridges to `Span<T>`.

```swift
import CxxStdlib
let s: std.string = "hello"      // implicit bridge from String literal
print(String(s))                 // back to Swift String
```

### 10.3 ABI stability

- Swift has had **ABI stability on Apple platforms since 5.0** (2019). Compiled apps can link against the system Swift runtime; library evolution mode (`-enable-library-evolution`) opts in to *resilient* APIs (additive changes possible).
- Cross-platform ABI is *not* stable on Linux/Windows; recompilation against the toolchain you ship with is required.
- The `@abi` attribute (SE-0476, Swift 6.2) lets library evolution authors describe ABI-stable surfaces independent of source-level changes.

### 10.4 Embedded Swift

- A language subset compiled in mode targeting bare metal (ARM Cortex-M, RISC-V, etc.).
- Enabled via `-enable-experimental-feature Embedded` (still flagged through 6.2; **exits experimental in Swift 6.3 / Mar 2026**).
- No runtime, no class metadata, no reflection, no full Foundation. `String`, `any` for class-constrained protocols, `InlineArray`, and `Span` are available as of 6.2.
- `@_unavailableInEmbedded` marks APIs that should fall out of the embedded slice.
- Use case: firmware, microcontrollers, secure enclaves. Swift MMIO (0.1.x, 2025) generates register interfaces from CMSIS SVD files.

See [`swift-best-practices.md` §10](./swift-best-practices.md#10-embedded-swift) for target triples, the embedded-vs-C-vs-Rust decision matrix, and the build invocation.

---

## 11. Module System & Access Control

### 11.1 Access levels (Swift 6.2 baseline)

| Level | Visible from |
|-------|--------------|
| `private` | Same scope (and same-file extensions) |
| `fileprivate` | Same file |
| `internal` (default) | Same module |
| `package` (SE-0386, 5.9) | Same Swift package |
| `public` | Other modules; not subclassable / overridable externally |
| `open` | `public` + subclassable / overridable externally |

The `package` modifier closes a long-standing gap: a multi-module package wanted to share APIs between its own modules without exposing them publicly to package consumers. Pre-`package`, the only options were `public` (over-exposed) or `@_spi` (underscored, fragile).

### 11.2 Import controls

- `import` (default): re-exposes nothing.
- `@_implementationOnly import` (underscored, deprecated in favor of SE-0409): hide the dependency from clients.
- `internal import` / `package import` (SE-0409, Swift 5.10/6.0): proper access-controlled imports — the imported module is invisible to consumers above that level.

### 11.3 Module aliasing (SE-0339)

SwiftPM supports aliasing modules to avoid name clashes when two packages publish the same module name:

```swift
.product(name: "Logging", package: "swift-log", moduleAliases: ["Logging": "SwiftLog"])
```

In code: `import SwiftLog` → resolves to the aliased module.

---

## 12. Per-Release Feature Table (5.10 → 6.2)

| Feature | SE | 5.10 | 6.0 | 6.1 | 6.2 |
|---------|----|------|-----|-----|-----|
| Complete strict concurrency (opt-in) | — | ✓ | (default) | — | — |
| Swift 6 language mode | — | — | ✓ | — | — |
| Typed throws `throws(E)` stable | 0413 | — | ✓ | — | — |
| Region-based isolation | 0414 | — | ✓ | refined | refined |
| `sending` parameters | 0430 | — | ✓ | — | — |
| `nonisolated(unsafe)` keyword | — | ✓ | — | — | — |
| Noncopyable generics | 0427 | — | ✓ | — | — |
| Noncopyable stdlib primitives (Optional, Result, …) | 0437 | — | ✓ | — | — |
| 128-bit integers | 0425 | — | ✓ | — | — |
| `count(where:)` | 0420* | — | ✓ | — | — |
| `Synchronization.Atomic` | 0410 | — | ✓ | — | — |
| `Synchronization.Mutex` | 0433 | — | ✓ | — | — |
| `@attached(body)` macros | 0415 | — | ✓ | — | — |
| `@DebugDescription` macro | 0440 | — | ✓ | — | — |
| Embedded Swift (experimental) | — | preview | ✓ | improved | improved |
| Diagnostic groups for warnings | — | — | — | ✓ | extended |
| Nonescapable types `~Escapable` | 0446 | — | — | preview | ✓ |
| `Span` / `MutableSpan` | 0447 / 0467 | — | — | preview | ✓ |
| Span on stdlib types (`Array.span`) | 0456 | — | — | — | ✓ |
| `InlineArray` (`[N of T]`) | 0453* | — | — | — | ✓ |
| Raw identifiers (backtick free-form) | 0451 | — | — | — | ✓ |
| `nonisolated(nonsending)` default for async | 0461* | — | — | — | ✓ (opt-in feature flag) |
| `@concurrent` attribute | 0461* | — | — | — | ✓ |
| `-default-isolation MainActor` | 0466* | — | — | — | ✓ |
| `weak let` | — | — | — | — | ✓ |
| `@abi` attribute (library evolution) | 0476 | — | — | — | ✓ |
| Warning control settings in SwiftPM | 0480 | — | — | — | ✓ |
| Method key paths | — | — | — | — | ✓ |
| Opt-in strict memory safety | — | — | — | — | ✓ |
| Subprocess library | — | — | — | — | ✓ |
| Observations async sequence | — | — | — | — | ✓ |
| Swift Testing exit testing / attachments | — | — | — | — | ✓ |
| WebAssembly (Wasm) supported target | — | — | — | preview | ✓ |
| Safe C++ interop mode | — | — | — | — | ✓ |

*Proposal numbers marked with `*` are approximate / part of a closely-related cluster; consult the swift-evolution dashboard for canonical SE IDs.

---

## 13. Unstable / In-Evolution Features (Swift 6.3 Outlook)

These are *not* yet stable as of 6.2; design or shipping behavior may shift. Swift 6.3 (Mar 2026) consolidates several of these.

### 13.1 Lifetime dependencies & full `~Escapable` ergonomics

SE-0446 ships `~Escapable`, but the surface for *expressing* lifetime dependencies (which value's lifetime governs which) is still in pitch/review (the `@lifetime` family). Swift 6.2 contains preview support; the syntax around "this Span depends on that Array" may evolve before stabilization.

### 13.2 Noncopyable generics in the stdlib (continued)

SE-0437 covered Optional and Result. Collections (`Array<Element: ~Copyable>`), generic algorithms (`map`, `filter`), and `Sequence`/`IteratorProtocol` over `~Copyable` are still being worked through — moving an iterator's `next()` to yield non-copyable elements requires careful API design.

### 13.3 Distributed actors

Distributed actors (Swift 5.7) and the swift-distributed-actors cluster library remain **beta**. Xcode 16.3 fixed a long-standing class-based actor system compiler crash, but the cluster library has not declared 1.0. Production use should be guarded.

### 13.4 Embedded Swift production-readiness

On track to exit experimental in **Swift 6.3 (Mar 2026)**. Until then expect API churn — particularly around `StaticString`, `print`, and Foundation subsetting. LLDB support for breakpoint/step/inspect on bare-metal ARM and RISC-V also arrives in 6.3.

### 13.5 Ownership control over collections

There's ongoing exploration of "borrowed Array" / "owned Array" distinctions and how `consume`/`borrow` should interact with `Sequence`/`for` loops. Watch for SE proposals during the 6.3 cycle.

### 13.6 AsyncStream successors / `Observations`

`Observations` (Swift 6.2) is a first move toward *transactional* state streams — observing a group of mutations as a single event rather than per-property. The general "AsyncStream successor" story (typed errors, multi-consumer, backpressure) is still under discussion.

### 13.7 `@concurrent` / `nonisolated(nonsending)` feedback loop

The 6.2 defaults change (NonisolatedNonsendingByDefault) is shipping as an *upcoming feature flag* — adopting it pre-Swift 7 is opt-in. Migration tooling is shipping alongside. Expect refinements based on community migration experience before Swift 7's hard cutover. Swift 6.3 sharpens the diagnostics.

### 13.8 Closure inference for typed throws

SE-0413 originally proposed inference for closure `throws(E)`; that part was deferred. Until it lands, generic closures often widen back to `throws(any Error)` — limiting typed-throws utility in higher-order code.

### 13.9 Android as official target (Swift 6.3)

Swift 6.3 promotes Android from community port to an officially supported target. Implication: Kotlin Multiplatform-style "share business logic" architectures become available with pure Swift; cross-compile from macOS / Linux to Android via the swiftly toolchain.

---

## 14. Code Examples — Non-obvious mechanics

### 14.1 Typed throws + async + cancellation

```swift
enum NetworkError: Error { case status(Int), decoding(any Error) }

func fetchProfile(_ id: UserID) async throws(NetworkError) -> Profile {
    do {
        let (data, response) = try await URLSession.shared.data(from: profileURL(id))
        guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
            throw NetworkError.status((response as? HTTPURLResponse)?.statusCode ?? -1)
        }
        return try JSONDecoder().decode(Profile.self, from: data)
    } catch let urlErr as URLError {
        throw .status(urlErr.errorCode)
    } catch let decErr as DecodingError {
        throw .decoding(decErr)
    }
    // CancellationError? — currently must be widened or handled by re-throwing as `any Error`.
}
```

### 14.2 Parameter packs: type-safe heterogeneous zip

```swift
func zip<each S: Sequence>(_ seqs: repeat each S)
    -> [(repeat (each S).Element)]
{
    var iterators = (repeat (each seqs).makeIterator())
    var result: [(repeat (each S).Element)] = []
    while true {
        // pack expansion in a tuple literal
        let tuple = (repeat (each iterators).next())
        // tuple is (Optional<E1>, Optional<E2>, …); if any is nil, stop
        // (in practice you'd use a helper to short-circuit)
        // …
        break
    }
    return result
}
```

### 14.3 `~Copyable` resource handle

```swift
struct Connection: ~Copyable {
    private let raw: OpaquePointer
    init(host: String) throws(ConnError) {
        guard let p = c_open(host) else { throw .openFailed }
        self.raw = p
    }
    consuming func close() { c_close(raw) }   // consuming → cannot use after
    deinit { c_close(raw) }                   // safety net if forgotten
}

func use(_ c: borrowing Connection) { /* read-only */ }

var c = try Connection(host: "db.local")
use(c)
c.close()   // explicit hand-off; binding `c` is unusable below
// use(c)   // compile error
```

### 14.4 Attached `body` macro for tracing

```swift
@attached(body)
public macro Traced() = #externalMacro(module: "TracingMacros", type: "TracedMacro")

@Traced func work() async throws -> Int { try await compute() }
//  ↓ expands to
// func work() async throws -> Int {
//     let span = Tracer.begin("work")
//     defer { span.end() }
//     return try await compute()
// }
```

### 14.5 `@concurrent` vs `nonisolated(nonsending)` placement

```swift
@MainActor final class UI {
    var label: String = ""
    func render() async {
        let parsed = await parseInline(rawInput)          // stays on MainActor
        let stats  = await crunchOnPool(rawInput)         // hops off MainActor
        label = "\(parsed) — \(stats)"                     // back on MainActor
    }
}

nonisolated(nonsending)
func parseInline(_ raw: String) async -> Parsed { … }    // runs on caller (MainActor here)

@concurrent
func crunchOnPool(_ raw: String) async -> Stats { … }    // explicitly off-actor; CPU-heavy
```

### 14.6 Structured task cancellation with bridge

```swift
func tailLog(_ path: String) async throws -> AsyncStream<String> {
    AsyncStream { continuation in
        let watcher = FileWatcher(path: path)
        watcher.onLine = { continuation.yield($0) }
        watcher.start()
        continuation.onTermination = { _ in watcher.stop() }
    }
}

await withTaskCancellationHandler {
    for await line in try await tailLog("/var/log/app.log") {
        if Task.isCancelled { break }
        print(line)
    }
} onCancel: {
    // synchronous escape — invoked off-task on cancel
    print("cancelled tail")
}
```

---

## Sources

### Swift.org official documentation & release blog

- [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
- [Swift 6.2 Released (Sep 2025)](https://www.swift.org/blog/swift-6.2-released/)
- [Swift 6.3 Released (Mar 2026)](https://www.swift.org/blog/swift-6.3-released/)
- [What's new in Swift: December 2025](https://www.swift.org/blog/whats-new-in-swift-december-2025/)
- [Library Evolution in Swift](https://www.swift.org/blog/library-evolution/)
- [Embedded Swift — Get Started](https://www.swift.org/get-started/embedded/)
- [Embedded Swift Examples](https://www.swift.org/blog/embedded-swift-examples/)
- [Swift for WebAssembly Getting Started](https://www.swift.org/documentation/articles/wasm-getting-started.html)
- [ABI Stability and More](https://www.swift.org/blog/abi-stability-and-more/)

### Swift Evolution proposals (canonical specification)

- [SE-0258 — Property Wrappers](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0258-property-wrappers.md)
- [SE-0289 — Result Builders](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0289-result-builders.md)
- [SE-0296 / 0297 / 0302 / 0304 / 0306 / 0316 — Concurrency stack (async/await, Task, async let, actor, Sendable, global actors)](https://github.com/swiftlang/swift-evolution/tree/main/proposals)
- [SE-0335 — Existential `any`](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0335-existential-any.md)
- [SE-0346 — Primary Associated Types](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0346-light-weight-same-type-syntax.md)
- [SE-0353 — Constrained Existentials](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0353-constrained-existential-types.md)
- [SE-0364 — Warning for Retroactive Conformances](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0364-retroactive-conformance-warning.md)
- [SE-0366 — `consume` Operator](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0366-move-function.md)
- [SE-0377 — `borrowing` / `consuming` Parameter Conventions](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0377-parameter-ownership-modifiers.md)
- [SE-0381 — Discarding Task Groups](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0381-task-group-discard-results.md)
- [SE-0382 — Freestanding Macros](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0382-expression-macros.md)
- [SE-0386 — `package` Access Modifier](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0386-package-access-modifier.md)
- [SE-0389 — Attached Macros](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0389-attached-macros.md)
- [SE-0390 — Noncopyable Types](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0390-noncopyable-structs-and-enums.md)
- [SE-0393 — Parameter Packs](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0393-parameter-packs.md)
- [SE-0397 — Freestanding Declaration Macros](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0397-freestanding-declaration-macros.md)
- [SE-0398 — Variadic Types](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0398-variadic-types.md)
- [SE-0407 — C++ Interop](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0407-mixed-language-targets.md)
- [SE-0408 — Pack Iteration](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0408-pack-iteration.md)
- [SE-0409 — Access-level on Import Statements](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0409-access-level-on-imports.md)
- [SE-0410 — Atomics](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0410-atomics.md)
- [SE-0413 — Typed Throws](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0413-typed-throws.md)
- [SE-0414 — Region-Based Isolation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0414-region-based-isolation.md)
- [SE-0415 — Function Body Macros](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0415-function-body-macros.md)
- [SE-0420 — Inheritance of Actor Isolation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0420-inheritance-of-actor-isolation.md)
- [SE-0425 — 128-bit Integer Types](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0425-int128.md)
- [SE-0427 — Noncopyable Generics](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0427-noncopyable-generics.md)
- [SE-0430 — Transferring Parameters and Results (`sending`)](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0430-transferring-parameters-and-results.md)
- [SE-0433 — Mutex](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0433-mutex.md)
- [SE-0437 — Noncopyable Standard Library Primitives](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0437-noncopyable-stdlib-primitives.md)
- [SE-0446 — Nonescapable Types `~Escapable`](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0446-non-escapable.md)
- [SE-0447 — Span](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0447-span-access-shared-contiguous-storage.md)
- [SE-0451 — Raw Identifiers](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0451-raw-identifiers.md)
- [SE-0461 — `nonisolated(nonsending)` Default for Async (cluster)](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md)
- [SE-0467 — MutableSpan](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0467-MutableSpan.md)
- [SE-0476 — `@abi` Attribute](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0476-abi-attribute.md)
- [SE-0480 — Warning Control Settings in SwiftPM](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0480-warning-control-settings.md)

### Apple Developer Documentation

- [AsyncStream](https://developer.apple.com/documentation/swift/asyncstream)
- [AsyncSequence](https://developer.apple.com/documentation/swift/asyncsequence)
- [withTaskCancellationHandler](https://developer.apple.com/documentation/swift/withtaskcancellationhandler(operation:oncancel:))
- [DiscardingTaskGroup](https://developer.apple.com/documentation/swift/discardingtaskgroup)
- [Migrating to Swift 6](https://www.swift.org/migration/documentation/migrationguide/)

### Swift Forums (accepted-with-modifications + active pitches)

- [forums.swift.org — Swift Evolution category](https://forums.swift.org/c/evolution/18) (pitch + review threads referenced from proposals above)
- [Concurrency category — `@concurrent` and default isolation pitches](https://forums.swift.org/c/development/concurrency/)

### Practitioner explainers (corroborating, for non-obvious mechanics only)

- [Donny Wals — What is `@concurrent` in Swift 6.2?](https://www.donnywals.com/what-is-concurrent-in-swift-6-2/)
- [SwiftLee — Swift 6.2 Concurrency Changes](https://www.avanderlee.com/concurrency/swift-6-2-concurrency-changes/)
- [Matt Massicotte — SE-0414 Region-Based Isolation](https://www.massicotte.org/concurrency-swift-6-se-0414/)
- [Matt Massicotte — SE-0430 sending parameters](https://www.massicotte.org/concurrency-swift-6-se-0430/)
- [Hacking with Swift — What's new in Swift (per-version)](https://www.hackingwithswift.com/articles/categories/whats-new-in-swift)

For any feature still tagged "in evolution" in §13, defer to the canonical SE proposal status before quoting behavior.
