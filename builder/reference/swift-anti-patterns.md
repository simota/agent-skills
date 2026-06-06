# Swift Anti-Patterns — Deep Dive Reference

> Companion to the broader Swift knowledge in this `builder/reference/` directory. This file covers language-level anti-patterns, pitfalls, footguns, and smells — what NOT to do, why it bites, and how to fix it. The `native` skill complements this for SwiftUI / Liquid Glass / iOS-platform-specific concerns.
>
> Baseline: Swift 6.2+ / Xcode 26 (as of 2026-05). Field-A flagged Swift 6.3 (Mar 2026) outlook where relevant.

> **Rule of thumb:** "If the compiler complains in Swift 6, it is almost always right. Suppressing the diagnostic (`@unchecked Sendable`, `nonisolated(unsafe)`, `try!`, `as!`) is admitting defeat, not winning."

---

## Table of Contents

1. [Force-unwrap / force-try / IUO pitfalls](#1-force-unwrap--force-try--iuo-pitfalls)
2. [Reference cycle pitfalls](#2-reference-cycle-pitfalls)
3. [Concurrency pitfalls (Swift 6.2 era)](#3-concurrency-pitfalls-swift-62-era)
4. [Type system pitfalls](#4-type-system-pitfalls)
5. [Error handling pitfalls](#5-error-handling-pitfalls)
6. [Performance pitfalls](#6-performance-pitfalls)
7. [Property wrapper / Macro pitfalls](#7-property-wrapper--macro-pitfalls)
8. [Memory pitfalls](#8-memory-pitfalls)
9. [Initialization pitfalls](#9-initialization-pitfalls)
10. [Closure & function pitfalls](#10-closure--function-pitfalls)
11. [Swift Package Manager pitfalls](#11-swift-package-manager-pitfalls)
12. [Testing pitfalls](#12-testing-pitfalls)
13. [Documentation pitfalls](#13-documentation-pitfalls)
14. [API design pitfalls](#14-api-design-pitfalls)
15. [Appendix A: SwiftLint quick-reference & starter config](#appendix-a-swiftlint-quick-reference--starter-config)
16. [Appendix B: Cross-section pattern map](#appendix-b-cross-section-pattern-map)
17. [Appendix C: Confidence and sources](#appendix-c-confidence-and-sources)
18. [Sources](#sources)

> **Cross-links:**
> - Canonical language semantics being violated (typed throws, Sendable, region isolation, `~Copyable`, `@concurrent`) → [`swift-language-spec.md`](./swift-language-spec.md)
> - Positive guidance, production library choices, testing strategy, migration cheatsheet → [`swift-best-practices.md`](./swift-best-practices.md)
> - SwiftUI / Liquid Glass / iOS HIG / Apple Intelligence / Foundation Models specifics → [`../../native/SKILL.md`](../../native/SKILL.md)

## How to read each section

Each section is a **table** of the form:

| # | Anti-pattern | Why it bites | Fix | SwiftLint / SwiftFormat rule |
|---|--------------|--------------|-----|------------------------------|

Plus **code snippets** for non-obvious cases.

For SwiftLint rule status:

- `default` — enabled out of the box
- `opt-in` — must be enabled in `.swiftlint.yml`
- `analyzer` — requires `swiftlint analyze` (slower, needs build)
- `—` — no SwiftLint rule (rely on code review or compiler)

---

## 1. Force-unwrap / force-try / IUO pitfalls

The dot-bang family (`!`, `try!`, `as!`, `Optional!`) replaces a compile-time concern (handle the nil/error/cast case) with a **runtime trap** (`EXC_BAD_INSTRUCTION` / `Fatal error: Unexpectedly found nil`).
These traps account for the **single largest class of Swift production crashes** observed in the wild.

### 1.1 Catalog

| #   | Anti-pattern                                  | Why it bites                                                                                                                              | Fix                                                                                              | SwiftLint                              |
| --- | --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | -------------------------------------- |
| 1.1 | `value!` on Optional                          | Crashes at runtime on `nil`; no recovery path; produces the famously useless "Unexpectedly found nil" message.                            | `guard let value else { … }`, `if let value`, `value ?? default`, optional chaining `value?.foo` | `force_unwrapping` (opt-in)            |
| 1.2 | `try! someThrows()`                           | Crashes on any thrown error; obliterates error context.                                                                                   | `try` inside `do/catch`, or `try? someThrows()` if you genuinely want `nil` on failure.          | `force_try` (default)                  |
| 1.3 | `as! ConcreteType`                            | Crashes on cast failure; usually a sign the API surface returns `Any` / `AnyObject` when it should be generic or typed.                   | `as?` + `guard let`, or redesign the API to return the concrete type.                            | `force_cast` (default)                 |
| 1.4 | `var label: UILabel!` (IUO) **outside** IB    | Crashes on any access before set; IUO is contagious — once one slips into a public API surface, callers can't reason about nullability.   | Plain `Optional`, lazy init, or a stored non-optional with a designated initializer.             | `implicitly_unwrapped_optional` (opt-in) |
| 1.5 | `try!` "just for prototypes" left in shipping | Prototypes ship. `try!` shipped is a time bomb.                                                                                           | Replace with `do/catch` and an explicit shipping decision (log + recover, or fatal with message). | `force_try`                            |
| 1.6 | `Bundle.main.path(forResource:)!`             | Misses a forgotten `Copy Bundle Resources`; ship-stopper bug that only fires on customer devices.                                         | `guard let path = Bundle.main.path(forResource:...) else { return … }` or `Bundle.module` in SPM. | `force_unwrapping`                     |
| 1.7 | `URL(string:)!` on literals                   | A typo is a crash; URL initialiser is not constexpr.                                                                                      | Use `URL(string:)` + tested helper, or `URL.init(filePath:)` for files. Swift 6 introduces compile-time URL macros — see `#URL("…")` in some packages. | `force_unwrapping`                     |
| 1.8 | `dict[key]!` after `dict[key] != nil` check   | Race-y in concurrent code; redundant work; obscures intent.                                                                               | `if let v = dict[key] { … }` — single lookup, no force-unwrap.                                  | —                                      |
| 1.9 | `arr.first!` / `arr.last!`                    | Crash on empty array; common in chained `filter`/`map`/`first`.                                                                           | `arr.first.map(handle)`, or `guard let first = arr.first else { return }`.                       | `force_unwrapping`                     |
| 1.10| `[String: Any]` JSON access via `dict["k"]!`  | Both the key lookup and the `as!` cast on the right side trap; double exposure.                                                           | `Codable` with concrete types, or `JSONDecoder()` into a struct.                                 | —                                      |
| 1.11| `Optional<Optional<T>>` double-wrap force     | Common in `dict[key]?` followed by `!!`. Each `!` is a separate trap.                                                                     | Flatten with `dict[key, default: …]`, `flatMap`, or restructure.                                | —                                      |

### 1.2 Justified force-unwraps (and how to make them safer)

There is a small set of cases where force-unwrap is **defensible** — but each should be paired with a justification comment and ideally a test:

| Case | Justification | Mitigation |
|------|---------------|------------|
| `@IBOutlet weak var label: UILabel!` | IB guarantees the outlet is wired by the time `viewDidLoad` runs. | Prefer storyboards-less code; or use `@IBOutlet weak var label: UILabel?` and `guard let` in viewDidLoad. |
| `URL(string: "https://example.com")!` for a known-good literal | Literal is verified at code review. | Wrap in a typed `Endpoint` enum so the construction site is reviewable. |
| `Calendar.current.date(byAdding: ...)!` for a known-valid arithmetic | Calendar always returns a value for typed-correct input. | Even so, prefer `Calendar.current.date(byAdding:...).orFatal("reason")` — a helper that logs the reason. |
| Test code: `try XCTUnwrap(value)` (not `value!`) | Tests should fail soft. | Always prefer `XCTUnwrap`/`#require` over `!` in test code. |

### 1.3 Code: defensible force-unwrap helper

```swift
// Better than naked `!`: documents intent, logs reason on crash.
extension Optional {
    func orFatal(_ reason: @autoclosure () -> String,
                 file: StaticString = #fileID,
                 line: UInt = #line) -> Wrapped {
        guard let self else {
            fatalError("Unexpected nil: \(reason())", file: file, line: line)
        }
        return self
    }
}

// Use site documents the invariant:
let id = user.id.orFatal("user fetched after sign-in must have id")
```

### 1.4 IUO contagion example

```swift
// Bad — IUO leaks into public API surface
public struct UserSession {
    public var profile: UserProfile!   // Anyone reading this type now must
                                       // reason about *when* profile is set.
}

// Fix
public struct UserSession {
    public var profile: UserProfile?           // Optional surface, OR
}
// or, with a designated initializer:
public struct UserSession {
    public let profile: UserProfile            // Non-optional, required at init.
}
```

---

## 2. Reference cycle pitfalls

Swift's ARC is deterministic, not garbage-collected. A cycle is a leak — period. The four classic shapes:

```
parent <-> child       (mutual strong refs)
self -> closure -> self
NotificationCenter -> observer
Timer.scheduledTimer(target:selector:) -> target
```

See [`swift-language-spec.md` §9](./swift-language-spec.md#9-memory-model--arc) for the canonical ARC semantics being violated.

### 2.1 Catalog

| #    | Anti-pattern                                                                                | Why it bites                                                                                                  | Fix                                                                                                       | SwiftLint                                  |
| ---- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| 2.1  | `delegate` stored as strong reference                                                       | Protocols often delegate back to the owner → cycle.                                                           | Mark `weak var delegate: SomeDelegate?`. Protocol must be `AnyObject`-bound.                              | `weak_delegate` (opt-in)                   |
| 2.2  | `var onTap: () -> Void = { self.handle() }` (escaping closure stored as property)           | Closure captures self strongly; self owns closure → cycle.                                                    | `var onTap: () -> Void = { [weak self] in self?.handle() }`                                               | —                                          |
| 2.3  | `someAPI.completion = { self.foo() }` and `someAPI` is retained for the view's lifetime     | Same cycle, hidden behind a one-shot-feeling API.                                                             | `[weak self]` or break ownership: have the caller own the API, not vice versa.                            | —                                          |
| 2.4  | `NotificationCenter.default.addObserver(self, …)` without matching `removeObserver`         | Pre-iOS 9 leaked; modern frameworks auto-remove on `deinit` of self, but the **block-based** API does NOT.    | Save the returned `NSObjectProtocol` token, call `removeObserver(token)` on deinit/disappear.             | `notification_center_detachment` (opt-in)  |
| 2.5  | `NotificationCenter.default.addObserver(forName:object:queue:using:)` block captures `self` | The token is owned by the system; block lives until removed; strong `self` → leak.                            | Capture `[weak self]` and store the returned token to remove it.                                          | —                                          |
| 2.6  | `Timer.scheduledTimer(timeInterval:target:selector:userInfo:repeats:)` with `target: self`  | Run loop retains the timer; timer retains the target → cycle. Worse: a repeating timer never invalidates.     | Use the block-based `Timer.scheduledTimer(withTimeInterval:repeats:)` + `[weak self]` + `invalidate()` in deinit. | —                                          |
| 2.7  | Combine `sink { value in self.handle(value) }` without `[weak self]`, stored on self        | `AnyCancellable` is owned by self; sink captures self → cycle. Memory never reclaimed until app exit.         | `sink { [weak self] v in self?.handle(v) }` and `.store(in: &cancellables)`.                              | —                                          |
| 2.8  | `.assign(to: \.prop, on: self)` (Combine)                                                   | `assign(to:on:)` retains the target. Use of `\.prop, on: self` → retain cycle.                                | Use `.assign(to: &$published)` (the `&$` form binds lifetime to the Published). Or `[weak self]` + `sink`. | —                                          |
| 2.9  | `Task { await self.work() }` stored as `currentTask` on self                                 | Task captures self strongly; self owns the Task handle → cycle until the Task finishes (but if it loops, never). | `Task { [weak self] in await self?.work() }` + cancel in deinit.                                          | —                                          |
| 2.10 | Parent ↔ child reference types (both class)                                                  | Mutual strong refs leak.                                                                                      | Decide ownership: parent owns child strongly, child holds `weak` parent reference.                        | —                                          |
| 2.11 | Caching `self`-bound closures into a registry/dictionary                                     | Registry outlives the owner; closure pins self forever.                                                       | Weak-key tables, `NSMapTable.weakToWeak`, or a `weak self` capture inside the closure body.               | —                                          |
| 2.12 | `lazy var x = { self.compute() }()`                                                          | The trailing-closure-evaluated `lazy var` captures self; the result is a value (no cycle) — BUT a `lazy var` whose **value type contains a closure that captures self** is a cycle. | If the lazy value is a closure type, `[weak self]` inside; if a value type, no cycle. | — |

### 2.2 Closure capture: weak vs unowned vs strong

```swift
// Pattern 1: weak self (most common; safe but may be nil)
api.fetch { [weak self] result in
    guard let self else { return }
    self.handle(result)
}

// Pattern 2: unowned (faster, but crashes if self is gone)
api.fetch { [unowned self] result in
    self.handle(result)   // CRASH if `self` deallocated mid-flight
}

// Pattern 3: weak + early bind (Swift 5.7+)
api.fetch { [weak self] result in
    guard let self else { return }
    self.handle(result)    // `self` here is non-optional Wrapped
}
```

**Rule of thumb:**

- Long-lived escaping closures (Combine sinks, timers, NotificationCenter blocks, stored properties): **`[weak self]`**.
- Closure that runs once and is guaranteed to outlive self? Don't use `unowned` "for performance" — the perf delta is negligible and `unowned` is a crash waiting for an edge case.
- Non-escaping closures (the closure runs synchronously before the function returns — e.g., `forEach`, `map`, `filter`): **no capture list needed**; no cycle possible.

### 2.3 NotificationCenter block-based observer leak

```swift
// Bad — token discarded; observer fires forever, closure retains self.
NotificationCenter.default.addObserver(
    forName: .didLogin, object: nil, queue: .main
) { _ in
    self.refresh()    // strong self capture
}

// Fix
final class Controller {
    private var loginToken: NSObjectProtocol?

    func subscribe() {
        loginToken = NotificationCenter.default.addObserver(
            forName: .didLogin, object: nil, queue: .main
        ) { [weak self] _ in
            self?.refresh()
        }
    }

    deinit {
        if let t = loginToken { NotificationCenter.default.removeObserver(t) }
    }
}
```

### 2.4 Task retain-cycle subtlety

A common misunderstanding: "`Task { ... }` is short-lived, so I don't need `[weak self]`."

True for fire-and-forget tasks **whose handle you discard**. False if you store the `Task` to cancel later:

```swift
// Bad — cycle until Task finishes (or forever, if it's a stream loop).
final class StreamController {
    var task: Task<Void, Never>?
    func start() {
        task = Task {
            for await update in stream {
                self.handle(update)
            }
        }
    }
}

// Fix
func start() {
    task = Task { [weak self] in
        for await update in stream {
            guard let self else { return }
            self.handle(update)
        }
    }
}
deinit { task?.cancel() }
```

Donny Wals's nuance: don't write `guard let self = self else { return }` as the **first line** — that immediately captures a strong reference for the whole closure. Instead, unwrap `self` only at the call site and let it go out of scope between awaits.

---

## 3. Concurrency pitfalls (Swift 6.2 era)

This is the section with the largest set of footguns in 2026. Swift 6.0 made the strict-concurrency checks **errors** instead of warnings, and 6.2 added **default actor isolation** (per-module opt-in to `@MainActor`-by-default) plus `@concurrent` for explicit background hops. With great power, great new ways to break things.

See [`swift-language-spec.md` §3 Concurrency Model](./swift-language-spec.md#3-concurrency-model) for the canonical isolation rules being violated, and [`swift-best-practices.md` §2](./swift-best-practices.md#2-concurrency-best-practices-swift-62-era) for the positive decision matrix.

### 3.1 Catalog

| #     | Anti-pattern                                                                                                          | Why it bites                                                                                                                          | Fix                                                                                                                                       | SwiftLint                                       |
| ----- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| 3.1   | `@unchecked Sendable` to silence a compiler error                                                                     | Silences the diagnostic without fixing the underlying race. Suppresses checks on function-typed stored properties → **runtime crash** when called from the wrong actor. | Use an actor, value type, or a `sending` parameter. Reserve `@unchecked Sendable` for types with verified internal locking. | `unchecked_sendable_via_isolated` (opt-in)      |
| 3.2   | `nonisolated(unsafe)` on a global `var`                                                                               | Equivalent to disabling concurrency checking on that property. Compiles, races at runtime.                                            | Wrap in an `actor`, make it `@MainActor` if UI-related, or use a lock + `@unchecked Sendable` with verified safety.                       | `nonisolated_unsafe` (opt-in)                   |
| 3.3   | `@MainActor` everywhere as escape hatch                                                                               | Forces UI and non-UI code through the main actor; serialises background work; defeats concurrency.                                    | Default actor isolation **per module**, with `@concurrent` on async fns that need a background hop. Models stay `nonisolated`/`Sendable`. | —                                               |
| 3.4   | Actor reentrancy: mutating actor state across an `await`                                                              | Another task can re-enter the actor at the await point; state assumed earlier may be different on resume.                             | Read state, do the async work, then **re-check** state before mutating. Or factor the async work out of the actor.                        | `actor_reentrancy_state_mutation` (opt-in)      |
| 3.5   | `Task { … }` spawned without storing the handle and without cancellation                                              | Task can outlive the spawning context; no way to cancel; may double-fire if spawned in a re-rendered view body.                       | Either use structured `async let` / `TaskGroup`, or store and `cancel()` the handle in deinit/onDisappear.                                 | —                                               |
| 3.6   | `try await Task.sleep(nanoseconds: 1_000_000_000)` as "wait for X"                                                    | `Task.sleep` does not implement timeouts — it is just a delay. Wrapping `withThrowingTaskGroup` around it for timeout is verbose and error-prone. | Use `withTimeout(seconds:)` helper or `Task.sleep(for: .seconds(1))` + explicit cancellation chain.                                       | —                                               |
| 3.7   | `withCheckedContinuation` where `resume` may be called twice                                                          | Runtime trap on second resume. The compiler does not catch double-resume.                                                             | Wrap the continuation in an actor-or-locked-guard; nil-out and check before resuming. Or migrate to native `async`/`AsyncSequence`.       | —                                               |
| 3.8   | `withCheckedContinuation` where `resume` may never be called                                                          | Task hangs forever; runtime logs `SWIFT TASK CONTINUATION MISUSE: leaked its continuation` after some delay.                          | Audit every callback path; ensure exactly one resume.                                                                                     | —                                               |
| 3.9   | `withUnsafeContinuation` "for performance" without proving safety                                                     | No double-resume protection at all.                                                                                                   | Stay on `withCheckedContinuation` until profiling proves it's a bottleneck (it virtually never is).                                       | —                                               |
| 3.10  | `DispatchQueue.main.async { … }` inside an async function                                                              | Mixes GCD + structured concurrency; defeats the executor model; can deadlock if the function is already on MainActor.                  | `await MainActor.run { … }` or mark the function `@MainActor`.                                                                            | —                                               |
| 3.11  | `await someActor.foo()` while holding an `os_unfair_lock`                                                              | Suspending while holding a non-async lock is a deadlock-prone footgun and **undefined behavior** for `os_unfair_lock`.                | Use `Mutex` (Swift 6.2 `Synchronization` module), or never `await` while a lock is held.                                                  | —                                               |
| 3.12  | `actor` with `init(...)` that calls main-actor isolated APIs                                                           | Pre-6.0 actor init could not safely access isolated state; 6.0 fixed this but the API contract still surprises.                       | Keep actor `init` simple; do `MainActor.run` setup from an explicit `start()` method.                                                     | —                                               |
| 3.13  | `Sendable` struct with a `class` (non-Sendable) field                                                                  | Compiler accepts because struct conformance auto-derives; the class field can still be mutated under the rug.                         | Make the class itself `Sendable` (or wrap in actor / `let` with a value type). Strict concurrency catches this in Swift 6.                | —                                               |
| 3.14  | `@preconcurrency import Foundation` permanently                                                                       | Suppresses concurrency warnings from the imported module; intended as a migration aid, not a permanent shield.                        | Use `@preconcurrency` per-symbol or in a transitional file; remove as the dependency updates.                                              | —                                               |
| 3.15  | Cross-actor await chain forms a cycle (A → B → A)                                                                      | Deadlock.                                                                                                                              | Decouple via a `nonisolated` helper or by moving the function out of the actor.                                                            | —                                               |
| 3.16  | `Task.detached { … }` to "escape" MainActor                                                                            | Loses caller's isolation, priority inheritance, and structured-task cancellation. Code now runs on the global executor.                | Use `nonisolated async` or `@concurrent` (Swift 6.2) to opt a specific function into background execution.                                | —                                               |
| 3.17  | Async function that suspends, takes a long time, but doesn't `await Task.checkCancellation()`                          | Tasks can be cancelled but the work runs to completion regardless; UI hangs on dismissal.                                              | Add `try Task.checkCancellation()` at logical checkpoints, or use `Task.sleep` which is cancellation-aware.                                | —                                               |
| 3.18  | `Task.isCancelled` inside a `DispatchQueue.global().async { … }` block                                                 | The dispatch block runs outside the task's cancellation context; `Task.isCancelled` is always `false`.                                 | Stay inside structured concurrency. Don't bridge through GCD.                                                                              | —                                               |
| 3.19  | `final class` `@MainActor` with a stored `var someTask: Task<Void, Never>?` that the deinit can't cancel               | `deinit` of a `@MainActor` class is itself `@MainActor`-isolated; cancellation from background-spawned cleanup paths fails.            | Use `Task { @MainActor in self.someTask?.cancel() }` in a controlled `tearDown()` method, not in deinit.                                   | —                                               |
| 3.20  | `let cache: [String: Image]` global without an actor wrapper                                                            | Mutable globals are race city. Compiler will warn in strict mode.                                                                      | Move into an `actor Cache { … }` or mark `@MainActor` if access pattern is UI-only.                                                        | —                                               |
| 3.21  | "I'll make it Sendable later" → `@unchecked Sendable` left for years                                                   | Hidden races, hard to debug, no compiler help. Code reviewers stop noticing.                                                           | Time-box `@unchecked Sendable` adoption: every one needs a `// TODO(concurrency)` and a tracking issue.                                    | —                                               |
| 3.22  | `func work() async throws { … }` with `try await` inside a `for` loop, no `TaskGroup`                                  | Sequential awaits — no parallelism. The loop blocks on each iteration.                                                                 | `withThrowingTaskGroup` (or `async let` for small fan-out) for parallel work.                                                              | —                                               |
| 3.23  | `MainActor.assertIsolated()` in production code that runs on background                                                | Crashes the app on every miss; useful in DEBUG, dangerous in RELEASE.                                                                  | Use `#if DEBUG` guards, or `MainActor.preconditionIsolated()` which is no-op in release.                                                   | —                                               |
| 3.24  | `init(@escaping () -> Void)` storing a closure on a Sendable struct                                                    | Closure may not be Sendable; struct claims it is.                                                                                      | Mark the closure parameter `@Sendable` and the type alias `@Sendable (…) -> …`.                                                            | —                                               |

### 3.2 Actor reentrancy: the classic state-stale bug

```swift
actor Cache {
    private var data: [String: Data] = [:]

    // Bad — state can change during the await.
    func fetch(key: String) async throws -> Data {
        if let cached = data[key] { return cached }
        let fresh = try await network.fetch(key)   // suspension point
        data[key] = fresh                          // could OVERWRITE a value
                                                   // another task wrote during await
        return fresh
    }
}
```

The fix: re-check after the await.

```swift
actor Cache {
    private var data: [String: Data] = [:]

    func fetch(key: String) async throws -> Data {
        if let cached = data[key] { return cached }
        let fresh = try await network.fetch(key)
        // Re-check: another task may have populated this key during the await.
        if let stillCached = data[key] { return stillCached }
        data[key] = fresh
        return fresh
    }
}
```

Or, for true deduplication, store `Task` handles per key:

```swift
actor Cache {
    private var pending: [String: Task<Data, Error>] = [:]

    func fetch(key: String) async throws -> Data {
        if let task = pending[key] { return try await task.value }
        let task = Task { try await network.fetch(key) }
        pending[key] = task
        return try await task.value
    }
}
```

### 3.3 `@unchecked Sendable` runtime crash mode

Jared Sinclair's documented case: `@unchecked Sendable` suppresses **compile-time** checks but not **runtime** actor-isolation assertions:

```swift
final class Box<T>: @unchecked Sendable {
    var value: T
    init(_ value: T) { self.value = value }
}

@main struct MyApp {
    static func main() {
        let closure: (String) -> Void = { print($0) }
        // Closure was *created* in main-actor scope (implicit),
        // so it carries that isolation tag at runtime.
        let box = Box(closure)
        DispatchQueue.global().async {
            box.value("crash!")   // dispatch_assert_queue failure
        }
    }
}
```

Compiles clean, crashes on first background call. Fix: type the closure as `@Sendable`:

```swift
typealias LogSink = @Sendable (String) -> Void
```

### 3.4 Default actor isolation (Swift 6.2): when to opt in

Swift 6.2 introduces module-level **default actor isolation** (`-default-isolation MainActor`). Donny Wals's rule:

| Module type | Opt-in to MainActor default? |
|-------------|-------------------------------|
| **App target** (UI-heavy) | Yes — eliminates most isolation warnings, write concurrent code explicitly |
| **UI package** | Yes — everything is MainActor anyway |
| **Networking / data / domain package** | No — design as Sendable values + actors |
| **Reusable library / SDK** | No — caller decides isolation |

Opting in does NOT remove the need to think about concurrency — it changes the **default direction**. With it on, you mark async work as `@concurrent` to explicitly hop off main.

### 3.5 The `withTimeout` helper (because `Task.sleep` is not a timeout)

```swift
func withTimeout<T: Sendable>(
    seconds: TimeInterval,
    operation: @escaping @Sendable () async throws -> T
) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        group.addTask { try await operation() }
        group.addTask {
            try await Task.sleep(for: .seconds(seconds))
            throw TimeoutError()
        }
        let result = try await group.next()!
        group.cancelAll()
        return result
    }
}

struct TimeoutError: Error {}
```

### 3.6 Continuation safety wrapper

```swift
// Safe wrapper: guarantees resume is called exactly once.
final class CheckedContinuationOnce<T, E: Error>: @unchecked Sendable {
    private let lock = NSLock()
    private var continuation: CheckedContinuation<T, E>?

    init(_ continuation: CheckedContinuation<T, E>) {
        self.continuation = continuation
    }
    func resume(returning value: T) {
        lock.lock(); defer { lock.unlock() }
        guard let c = continuation else { return }
        continuation = nil
        c.resume(returning: value)
    }
    func resume(throwing error: E) {
        lock.lock(); defer { lock.unlock() }
        guard let c = continuation else { return }
        continuation = nil
        c.resume(throwing: error)
    }
}
```

(This is one of the rare `@unchecked Sendable` cases that is genuinely justified — the lock provides verified synchronization.)

---

## 4. Type system pitfalls

### 4.1 Catalog

| #    | Anti-pattern                                                                              | Why it bites                                                                                              | Fix                                                                                            | SwiftLint                              |
| ---- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------- |
| 4.1  | `String` for an entity ID (`func find(_ id: String)`)                                      | Primitive obsession; nothing prevents passing a username where you meant a user ID, or a chat ID for a user ID. | Wrap: `struct UserID: Hashable { let value: String }`. Tagged types in Swift 5.10+ help further. | —                                      |
| 4.2  | `any P` for a single value where `some P` would do                                         | Existential boxing: heap allocation, dynamic dispatch, can't be inlined.                                  | Use `some P` for parameters/returns. Reach for `any P` only for heterogeneous collections.     | `existential_any` (opt-in)             |
| 4.3  | `some P` where the collection is heterogeneous                                             | `some P` is a *single* concrete type. `[some View]` is one type repeated, NOT mixed.                       | Use `[any View]` for true heterogeneous arrays.                                                | —                                      |
| 4.4  | Protocol with associated type forced into existential pre-Swift 5.7                        | Used to require `any` boxing tricks and `AnyP` type erasers.                                              | Swift 5.7+: `any P` with primary associated types. Swift 6: `any P<.Element == T>`.            | —                                      |
| 4.5  | Generic constraints over-specified: `<T: Hashable & Codable & Sendable & Comparable>`      | Forces every call site to satisfy the union; reduces reuse; couples the API.                              | Minimum viable constraint. Add more only when a method body demands it.                        | —                                      |
| 4.6  | Conditional conformance forgotten: `extension Array: Equatable where Element: Equatable`   | The standard library already provides this. Manual conformance creates duplicate-witness warnings.        | Don't redeclare — use the stdlib's conditional conformance.                                    | —                                      |
| 4.7  | `class Foo` for a value-semantic type                                                       | Reference semantics where copy-semantics is desired → aliasing bugs.                                      | Make it a `struct` unless identity or shared mutable state is required.                        | `final_class` (opt-in)                 |
| 4.8  | `final class Foo` then later removing `final` for testing override                          | `final` is an optimisation contract; removing it for tests is a code smell.                               | Use protocol-based abstractions for testability; keep `final`.                                 | —                                      |
| 4.9  | Force-cast `as!` instead of generics                                                        | Type erasure that should be type-preserving.                                                              | Generics. If you can't, `as?` + a clear error path.                                            | `force_cast`                           |
| 4.10 | `Any` used as a value type ("we'll figure it out later")                                   | All type safety lost; usually the start of a Stringly-typed disaster.                                     | Enum with associated values, or a protocol with a small surface, or generics.                  | —                                      |
| 4.11 | `Self` in a non-final class returned from a method, then subclasses break                  | `Self` constraints propagate to subclasses; the subclass must return its own Self.                       | Either `final` the class, or use a protocol with `Self` requirements.                          | —                                      |
| 4.12 | `Optional<Optional<T>>` from `try?` on `try value?.method() ?? fallback`                   | Double-optional unwrapping requires `??` chaining; readability craters.                                   | `flatMap`, restructure with `do/catch`, or extract a helper.                                   | —                                      |

### 4.2 Existential overhead — measured

Existentials box the value, store a witness table pointer, and dispatch dynamically. A `func foo<T: P>(_: T)` is monomorphised; a `func foo(_: any P)` is not.

```swift
// Costly:
func process(items: [any Drawable]) { items.forEach { $0.draw() } }

// Cheap:
func process<D: Drawable>(items: [D]) { items.forEach { $0.draw() } }
```

For a homogeneous array, the generic version may be ~5–10x faster on tight loops. **But** use `any` when the array genuinely contains mixed types.

### 4.3 Primary associated types

```swift
// Pre-5.7: required AnyCollection type eraser.
let strings: AnyCollection<String> = …

// 5.7+:
let strings: any Collection<String> = …

// 6.0+: with where clauses for richer constraints.
let nums: any Sequence<Int> & Sendable = …
```

For canonical semantics on `some` / `any` / primary associated types / `~Copyable` constraints, see [`swift-language-spec.md` §4](./swift-language-spec.md#4-type-system).

---

## 5. Error handling pitfalls

Error handling is where production stability is decided. The most common smells are silent failure (`try?` everywhere, empty catches) and lossy wrapping.

### 5.1 Catalog

| #    | Anti-pattern                                                                       | Why it bites                                                                                                              | Fix                                                                                                  | SwiftLint                              |
| ---- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 5.1  | `try? someThrows()` everywhere (swallows error)                                    | You see `nil` but lose the **why**: timeout vs auth failure vs missing record produce identical `nil`.                    | `do { try … } catch { logger.error(error) }`; or typed throws to make the error type explicit.       | —                                      |
| 5.2  | `try!` in production                                                                | Crashes on any throw, including transient (network blip).                                                                  | Replace with `do/catch`. `try!` is OK in **constants** known at compile time, never in IO.           | `force_try` (default)                  |
| 5.3  | Custom `enum MyError: Error` without `LocalizedError`                              | `error.localizedDescription` returns the bridged Cocoa string `"The operation couldn't be completed. (MyModule.MyError error 0)"`. | Conform to `LocalizedError`, provide `errorDescription`.                                              | —                                      |
| 5.4  | Empty `catch { }` block                                                             | Silent failure; debugging is impossible.                                                                                  | At minimum: `logger.error(error)`. Better: re-throw or take an action.                                | `empty_catch` (custom)                 |
| 5.5  | `catch let error as NSError` losing the original Swift `Error` type                | NSError loses associated values and the typed throw chain.                                                                | `catch let error as MyError` (typed catch). Avoid bridging unless you must.                          | —                                      |
| 5.6  | `Result<T, Error>` returned from a function that should `throws`                   | Two error-handling paradigms in one codebase → inconsistency.                                                              | `func work() async throws -> T`. Use `Result` only at framework boundaries.                          | —                                      |
| 5.7  | `throws` everywhere when typed throws would scope the error                        | Loses the type info; every catch must handle "any" error.                                                                 | Swift 6: `func work() throws(MyError) -> T`. Exhaustive switching inside catch.                      | —                                      |
| 5.8  | Wrapping errors lossily: `throw MyError.network` (dropping the underlying error)   | Root cause is gone; debugging from logs is guesswork.                                                                     | `throw MyError.network(underlying: error)` with an associated value, or use `_underlyingError`.       | —                                      |
| 5.9  | Throwing custom errors without `Equatable` (then asserting in tests)               | Tests can't `XCTAssertEqual` on the error.                                                                                | Make `MyError: Equatable` when possible (no associated values that aren't Equatable).                | —                                      |
| 5.10 | `do { try x() } catch { throw error }` (no-op re-throw)                            | Adds a layer with no value; defeats inlining.                                                                             | Remove the `do/catch` and let the throw propagate.                                                    | `redundant_optional_initialization` (closest stdlib equivalent — no exact rule) |
| 5.11 | Throwing from `init` then ignoring the error site                                  | Callers may need to know which init parameter caused it; generic error makes that opaque.                                  | Specific error cases per validation point.                                                            | —                                      |
| 5.12 | Returning `Result<T, Never>` where `T` would do                                    | Unnecessary boxing.                                                                                                       | Just return `T`. `Result<T, Never>` is only useful in API-shape-driven generic contexts.              | —                                      |
| 5.13 | `try await x() ?? fallback` (assumes `try?` semantics) — mis-typed                 | `??` doesn't apply to `try await`. Compiler error, but in mixed try/await chains it confuses.                              | `(try? await x()) ?? fallback`.                                                                       | —                                      |

### 5.2 LocalizedError pattern

```swift
enum LoginError: Error, LocalizedError, Equatable {
    case invalidCredentials
    case rateLimited(retryAfter: TimeInterval)
    case serverError(statusCode: Int)

    var errorDescription: String? {
        switch self {
        case .invalidCredentials:
            return String(localized: "Incorrect email or password.")
        case .rateLimited(let retryAfter):
            return String(localized: "Too many attempts. Try again in \(Int(retryAfter)) seconds.")
        case .serverError(let code):
            return String(localized: "Server error (\(code)). Please try again.")
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .invalidCredentials: return String(localized: "Reset your password if you've forgotten it.")
        case .rateLimited: return nil
        case .serverError: return String(localized: "If this keeps happening, contact support.")
        }
    }
}
```

### 5.3 Typed throws (Swift 6.0+)

```swift
func authenticate(email: String, password: String) async throws(LoginError) -> Session {
    let response = try await api.login(email: email, password: password)
    // Compiler enforces: only LoginError can be thrown.
    guard response.success else { throw LoginError.invalidCredentials }
    return Session(token: response.token)
}

// Caller: catch is exhaustive WITHOUT a default.
do {
    let session = try await authenticate(email: e, password: p)
} catch LoginError.invalidCredentials {
    ...
} catch LoginError.rateLimited(let retry) {
    ...
} catch LoginError.serverError(let code) {
    ...
}
// No `catch { ... }` needed — exhaustive over LoginError.
```

For the typed-throws decision matrix and language semantics, see [`swift-language-spec.md` §6.2](./swift-language-spec.md#62-typed-throws-se-0413-stable-in-swift-60) and [`swift-best-practices.md` §3.2](./swift-best-practices.md#32-typed-throws-swift-60--when-worth-it).

### 5.4 Avoid the "catch and log" anti-pattern at the wrong layer

```swift
// Bad — utility catches and returns nil. Caller has no idea what failed.
extension UserDefaults {
    func decodedData<T: Decodable>(_ type: T.Type, forKey key: String) -> T? {
        guard let data = data(forKey: key) else { return nil }
        do { return try JSONDecoder().decode(type, from: data) }
        catch {
            print("Decode failed: \(error)")   // swallowed
            return nil
        }
    }
}

// Good — throw, let the caller decide.
extension UserDefaults {
    func decodedData<T: Decodable>(_ type: T.Type, forKey key: String) throws -> T? {
        guard let data = data(forKey: key) else { return nil }
        return try JSONDecoder().decode(type, from: data)
    }
}
```

---

## 6. Performance pitfalls

### 6.1 Catalog

| #    | Anti-pattern                                                                          | Why it bites                                                                                              | Fix                                                                                              | SwiftLint                                |
| ---- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| 6.1  | `var arr: [Int] = []; for i in 0..<1_000_000 { arr.append(i) }` without `reserveCapacity` | Geometric growth still allocates O(log N) times; for known sizes that's pure waste.                       | `arr.reserveCapacity(1_000_000)` first.                                                          | —                                        |
| 6.2  | `reserveCapacity` in a loop                                                           | Reserving repeatedly defeats Swift's growth strategy and ends up SLOWER than not reserving at all.        | One reserve, before the loop. Or none — Swift's amortised O(1) is usually fine.                  | —                                        |
| 6.3  | String building with `+`: `s = s + chunk` in a loop                                   | Each `+` is a new allocation. Quadratic in total length.                                                  | `s.append(chunk)`, or use `String(unsafeUninitializedCapacity:)` for the rare hot path.          | —                                        |
| 6.4  | Creating a `JSONDecoder` per call                                                     | Decoders are heavyweight; they allocate userInfo tables, formatters, key-decoding caches.                  | Store a shared decoder per type/configuration. (Decoders are Sendable in Swift 6.)              | —                                        |
| 6.5  | Creating a `DateFormatter` per call                                                   | DateFormatter is extremely heavy (locale, calendar, timezone all parsed).                                  | Cache per-format DateFormatter, or use `Date.ISO8601FormatStyle()` (cheap, Sendable).            | —                                        |
| 6.6  | `Date()` allocations in a tight loop                                                  | `Date()` is cheap-ish but inside tight loops adds up; allocation pressure.                                 | Read once outside the loop; or use `ContinuousClock().now`.                                      | —                                        |
| 6.7  | `for item in collection.filter { ... }.map { ... }` (no lazy)                         | Materialises the filtered array, then maps. Two passes + intermediate allocation.                          | `collection.lazy.filter { … }.map { … }.forEach { … }` — one pass.                                | —                                        |
| 6.8  | `arr.count > 0` instead of `!arr.isEmpty`                                              | For Strings, `count` is O(N); for LinkedLists, O(N). isEmpty is O(1).                                     | `arr.isEmpty` / `!arr.isEmpty`.                                                                   | `empty_count` (opt-in)                   |
| 6.9  | `arr.first { $0.matches } != nil` to test existence                                   | Allocates an Optional<Element> with the value; readability cost.                                          | `arr.contains { $0.matches }`.                                                                   | `contains_over_first_not_nil` (opt-in)   |
| 6.10 | `arr.filter { $0.matches }.count > 0`                                                  | Allocates the entire filtered array just to count.                                                        | `arr.contains { $0.matches }`.                                                                   | `contains_over_filter_count` (opt-in)    |
| 6.11 | `arr.filter { $0.matches }.isEmpty`                                                    | Same allocation issue.                                                                                    | `!arr.contains { $0.matches }`.                                                                   | `contains_over_filter_is_empty` (opt-in) |
| 6.12 | `arr.sorted().first` / `arr.sorted().last`                                            | O(N log N) sort to get one element.                                                                       | `arr.min()` / `arr.max()` — O(N).                                                                | `sorted_first_last` (opt-in)             |
| 6.13 | `for i in 0..<arr.count { use(arr[i]) }`                                              | Indexed access is fine for Array but breaks for Sequence; verbose.                                        | `for item in arr { use(item) }`.                                                                  | —                                        |
| 6.14 | Mutating `var arr = otherArr` then mutating `arr` while keeping `otherArr` around     | Defeats COW: the assignment + mutation triggers a copy you may not want.                                   | If you need a shared write, design around an actor or a single owner.                              | —                                        |
| 6.15 | `lazy var x = { ... }()` closure that captures self strongly                          | Cycle. Also: lazy is non-Sendable by default; surprising in concurrent code.                              | Avoid lazy on `class`; use `private var x: T?` with explicit lazy semantics.                       | —                                        |
| 6.16 | `NSPredicate` on `Codable` data manually filtered                                      | NSPredicate is interpreted at runtime; Swift native filter is monomorphised.                              | `arr.filter { $0.field == value }`.                                                              | —                                        |
| 6.17 | Foundation calls in a tight loop without `autoreleasepool`                            | Pre-ARC, NSString/NSData created at autorelease pool boundary; in Swift these are bridged.                | Wrap hot Foundation-call loops in `autoreleasepool { … }` if profiling shows memory pressure.    | —                                        |
| 6.18 | `try await x()` in `for` loop where calls are independent                              | Sequential await — no parallelism.                                                                        | `withThrowingTaskGroup` or `async let`.                                                            | —                                        |
| 6.19 | `Dictionary` with `String` keys hot path                                              | String hashing is non-trivial; on hot paths, integer or enum keys win.                                    | Use an int/enum keyed dictionary; or cache the hash.                                              | —                                        |
| 6.20 | `print(...)` left in shipping                                                          | `print` is unbuffered and synchronous; can be a measurable slowdown.                                      | `Logger` (os_log) or strip with `#if DEBUG`.                                                       | —                                        |
| 6.21 | `String(reflecting:)` / `String(describing:)` in hot path                              | Reflection is dynamic and slow.                                                                            | `CustomStringConvertible.description`.                                                            | —                                        |
| 6.22 | `Array(Set(arr))` to dedupe — order-destroying surprise                                | The order of the result is unspecified.                                                                   | `var seen = Set<T>(); arr.filter { seen.insert($0).inserted }`.                                   | —                                        |

### 6.2 reserveCapacity nuance

```swift
// Wrong: repeated reserve.
var items: [Item] = []
for batch in batches {
    items.reserveCapacity(items.count + batch.count)  // Bad — defeats geometric growth
    items.append(contentsOf: batch)
}

// Right: reserve once with the known total.
var items: [Item] = []
items.reserveCapacity(batches.reduce(0) { $0 + $1.count })
for batch in batches { items.append(contentsOf: batch) }

// Or, just trust the standard library if you don't know the total:
var items: [Item] = []
for batch in batches { items.append(contentsOf: batch) }   // O(1) amortised
```

### 6.3 Decoder/Formatter reuse

```swift
// Bad — allocates a decoder per call.
extension Data {
    func decoded<T: Decodable>(_ type: T.Type) throws -> T {
        try JSONDecoder().decode(type, from: self)
    }
}

// Good — shared decoder with configuration.
enum JSON {
    static let decoder: JSONDecoder = {
        let d = JSONDecoder()
        d.keyDecodingStrategy = .convertFromSnakeCase
        d.dateDecodingStrategy = .iso8601
        return d
    }()
}

extension Data {
    func decoded<T: Decodable>(_ type: T.Type) throws -> T {
        try JSON.decoder.decode(type, from: self)
    }
}
```

Note: `JSONDecoder` is `Sendable` from Swift 6, so a shared static is safe across actors.

---

## 7. Property wrapper / Macro pitfalls

### 7.1 Catalog

| #   | Anti-pattern                                                                       | Why it bites                                                                                                  | Fix                                                                                          | SwiftLint                              |
| --- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------- |
| 7.1 | `@Published var foo` inside an `@Observable`-macro class                            | `@Observable` makes ALL stored properties observable. Adding `@Published` is wrong (Published is `ObservableObject`-specific). | Remove `@Published` — `@Observable` handles it.                                              | —                                      |
| 7.2 | Mixing `@StateObject` and `@Observable` ("drop-in" replacement)                     | Not a drop-in. With `ObservableObject` + `@StateObject`, init runs once. With `@Observable` + `@State`, init runs **every** view rebuild. | Use `@State` (not `@StateObject`) with `@Observable` types. Ensure init is cheap.            | —                                      |
| 7.3 | Expensive work in `@Observable` class init                                          | Init may run many times per view lifecycle. UserDefaults reads, notification registration, file IO all replay. | Lazy or one-shot the work behind a static or a `Task { … }` triggered after binding.         | —                                      |
| 7.4 | `@State` outside a `View` (e.g., on a class)                                       | Warning; semantics are undefined. `@State` is owned by SwiftUI's render tree.                                | Use `@Observable` for class state, `@State` only on `View` structs.                          | —                                      |
| 7.5 | `@ObservedObject` for an instance the view *creates*                                 | View ownership semantics: `@ObservedObject` does not own; if you create the instance in the view body, it leaks/recreates on each render. | `@StateObject` for ownership, `@ObservedObject` for borrowed.                                | —                                      |
| 7.6 | Macro plugin failed to load → silent build failure or red squiggles                | Macros need a plugin executable; if the plugin can't be built or trust isn't granted, you may see vague errors. | Inspect Issue Vector carefully; rerun Xcode > Settings > Locations > "Manage Macros".     | —                                      |
| 7.7 | `@Observable` on a model used in lists with stable identity                         | Equality / Identity is auto-derived; if `id` changes or is computed, lists thrash.                            | Conform to `Identifiable` explicitly; ensure `id` is stable.                                  | —                                      |
| 7.8 | Custom property wrapper with non-Sendable `wrappedValue`                            | Sendable inference may surface a warning across an isolation boundary.                                       | Make wrappers Sendable when used across actors; or keep them per-actor.                       | —                                      |
| 7.9 | `@Environment(\.someValue)` where `someValue` is non-Sendable                       | Strict concurrency error.                                                                                    | Use a Sendable wrapper or make the environment value `@MainActor`.                            | —                                      |
| 7.10 | Macro-generated init missing for properties added after the macro expansion was cached | Stale macro cache.                                                                                            | Clean build folder; restart Xcode.                                                            | —                                      |
| 7.11 | Forgetting `@MainActor` on an `@Observable` class with UI side effects             | Background mutations to UI-bound properties; tearing.                                                         | `@MainActor @Observable final class ...` for UI models.                                       | —                                      |

> SwiftUI binding semantics (`@StateObject` vs `@State` ownership, `@Bindable` patterns, view-tree rebuild rules) belong in [`../../native/SKILL.md`](../../native/SKILL.md).

### 7.2 Observable vs ObservableObject init lifecycle gotcha

```swift
// PRE-iOS 17 — init runs ONCE for the View's lifetime.
final class OldVM: ObservableObject {
    @Published var items: [Item] = []
    init() {
        // Heavy work — fine because called once.
        load()
    }
}
struct OldView: View {
    @StateObject private var vm = OldVM()
    var body: some View { ... }
}

// iOS 17+ — init runs EVERY time SwiftUI rebuilds the view.
@Observable final class NewVM {
    var items: [Item] = []
    init() {
        load()    // Bad — runs many times per second under heavy update.
    }
}
struct NewView: View {
    @State private var vm = NewVM()
    var body: some View { ... }
}
```

The fix: make `@Observable` types cheap to construct, defer work to a `.task` modifier.

```swift
@Observable final class NewVM {
    var items: [Item] = []
    func load() async { /* ... */ }
}
struct NewView: View {
    @State private var vm = NewVM()
    var body: some View {
        List(vm.items) { … }
            .task { await vm.load() }
    }
}
```

---

## 8. Memory pitfalls

(Some overlap with section 2 — this section is about *non-cycle* leaks: objects that never deinit because something external holds them.)

### 8.1 Catalog

| #   | Anti-pattern                                                                                  | Why it bites                                                                                                  | Fix                                                                                              |
| --- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 8.1 | `URLSessionDataTask` started, never cancelled, view disappears                                 | Network response retains its delegate / completion → retains view model.                                       | Cancel the task in `deinit` or `onDisappear`.                                                    |
| 8.2 | `URLSession.shared.dataTaskPublisher(...).sink(...)` without `.store(in:)`                     | AnyCancellable deallocates immediately; subscription dies; no result.                                          | `.store(in: &cancellables)`.                                                                     |
| 8.3 | `NotificationCenter.default.addObserver(forName:..., using: { … })` token discarded            | Closure runs forever; can't be removed.                                                                       | Save the token, removeObserver on deinit.                                                        |
| 8.4 | `CADisplayLink` / `CVDisplayLink` not invalidated                                              | Retains target; runs forever.                                                                                 | `invalidate()` in deinit.                                                                        |
| 8.5 | `KVO addObserver(self, ...)` without remove                                                    | Pre-Swift KVO leaks; modern `observe(\.path) { ... }` is auto-cleaned. The `NSKeyValueObservation` returned must be stored. | Use the modern block-based KVO; store the returned `NSKeyValueObservation`.                       |
| 8.6 | Global mutable cache without eviction                                                          | Memory grows unbounded.                                                                                       | `NSCache` with `countLimit` / `totalCostLimit`, or an LRU implementation.                         |
| 8.7 | Image caches keyed on URL with no `purge` on memory warning                                    | Memory pressure crash on devices with low RAM.                                                                | `NSCache` (already responds to memory warnings) or custom + `UIApplication.didReceiveMemoryWarningNotification`. |
| 8.8 | `Task { … }` returning `Task<Void, Never>` stored on `self`, where self is `@MainActor` class with Task firing infinitely | Task pins self.                                                                                                | Cancel task on deinit equivalent (tearDown method); use `[weak self]` inside the task body.       |
| 8.9 | Singleton holding references to view controllers / view models for "convenience"               | View hierarchy never deinits.                                                                                 | Don't store transient state in singletons. Use a registry with explicit lifecycle.                |
| 8.10 | `@MainActor` class with deinit that tries to do main-actor work                                | deinit isolation in Swift 6 is subtle; some deinit work may not run on main actor.                            | Move teardown to an explicit `stop()` method; keep deinit minimal.                                |
| 8.11 | `UIViewControllerRepresentable.makeCoordinator` creates a strong-self-capturing closure         | View ↔ coordinator cycle in SwiftUI bridges.                                                                  | Use weak captures in coordinator-held closures.                                                   |

---

## 9. Initialization pitfalls

### 9.1 Catalog

| #    | Anti-pattern                                                                                    | Why it bites                                                                                                                  | Fix                                                                                              |
| ---- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 9.1  | `init?` failable for input validation (returns nil silently)                                     | Caller has no idea **why**; multiple validation rules collapse to a single `nil`.                                              | `init() throws` with typed throws and specific error cases.                                       |
| 9.2  | `convenience init` that calls another convenience that calls another → infinite chain           | Compiler catches direct cases; deep chains compile and stack-overflow at runtime.                                              | Diagram the init graph; ensure every chain terminates at a designated initialiser.                |
| 9.3  | `required init?(coder:)` boilerplate everywhere — `fatalError("init(coder:) has not been implemented")` | `fatalError` shipped in NIB-decoding paths crashes when storyboard inflation happens unexpectedly.                              | If you don't use storyboards, mark the class `final` and avoid `NSCoder` paths. Or implement properly. |
| 9.4  | `Decodable` synthesised on a struct containing a non-`Decodable` property                       | Compile error in newer Swift; pre-5.5 it crashed at decode-time.                                                                | Make the property `Decodable`, or write a custom `init(from:)`.                                   |
| 9.5  | Superclass init call out of order                                                                | Two-phase init violation; compiler should catch, but some patterns slip (e.g., calling self methods before super init).         | Initialise all subclass properties first, then `super.init(...)`.                                |
| 9.6  | `actor` init that calls `await` on its own isolated method                                       | Pre-6.0 actor init couldn't be `async`; even now, accessing isolated state before `init` completes can deadlock in some paths. | Keep actor init synchronous and cheap; do async setup in an explicit `start()` method.            |
| 9.7  | `@MainActor` class default init invoked from background context                                  | Swift 6 strict concurrency error.                                                                                              | Initialise on main, or mark the init `nonisolated` if it doesn't touch isolated state.            |
| 9.8  | `Decodable` synth on `@MainActor` struct — protocol conformance crosses isolation               | "Main actor-isolated initializer 'init(from:)' cannot satisfy nonisolated protocol requirement."                                | Mark the conformance `nonisolated`, or decode off-main and hop the result to main.                |
| 9.9  | `required init` forgotten on a subclass that inherits a `required` init                          | Compile error.                                                                                                                 | Mark the subclass `final` (if final, you can omit `required init?(coder:)` by overriding with a fatal). |
| 9.10 | Custom `init(from decoder: Decoder)` that doesn't handle all keys                               | Silent truncation: missing keys throw, but extra keys are silently ignored.                                                   | Test round-trip encode→decode for every model.                                                    |
| 9.11 | `init()` with side effects (logging, analytics, notifications)                                  | `init` runs in unexpected contexts (tests, previews, mock decoders).                                                          | Move side effects to explicit `start()` / `viewDidLoad()` / `.task`.                              |
| 9.12 | Using `class` for a model with no identity, then leaking via init                                | Reference semantics + init side effects = surprise aliasing.                                                                  | `struct`. If you must use class, document identity rules.                                         |

### 9.2 Decodable + MainActor isolation conflict

```swift
// Bad — @MainActor struct that's Decodable.
@MainActor
struct User: Decodable {
    let id: String
    let name: String
}
// Compiler: Main actor-isolated initializer 'init(from:)' cannot be used to
// satisfy nonisolated protocol requirement.

// Fix 1: nonisolated conformance.
@MainActor
struct User: Decodable {
    nonisolated init(from decoder: Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        id = try c.decode(String.self, forKey: .id)
        name = try c.decode(String.self, forKey: .name)
    }
    let id: String
    let name: String
    enum CodingKeys: String, CodingKey { case id, name }
}

// Fix 2: Don't isolate the model. Models are value types; isolate the
// store/manager, not the model.
struct User: Decodable, Sendable {
    let id: String
    let name: String
}
```

---

## 10. Closure & function pitfalls

### 10.1 Catalog

| #     | Anti-pattern                                                                          | Why it bites                                                                                                  | Fix                                                                                              |
| ----- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 10.1  | Capturing a `var` and assuming current-value semantics                                | Closures capture by reference for var, by value for let in some cases — surprising.                            | `[localCopy = currentValue]` in the capture list to snapshot at definition time.                  |
| 10.2  | `@escaping` forgotten on a stored closure                                              | Compile error if obvious; subtle when the closure is conditionally stored (e.g., behind an if).               | Mark `@escaping` whenever the closure is held past the function's return.                         |
| 10.3  | Escaping closure not marked `@Sendable` in concurrent code                            | Sendable struct holds it; strict concurrency error.                                                           | `@Sendable (T) -> Void`.                                                                          |
| 10.4  | `@autoclosure` for late evaluation forgotten                                          | Caller has to wrap in `{ … }` every time, or the expression is evaluated eagerly.                              | `func log(_ msg: @autoclosure () -> String)`.                                                     |
| 10.5  | `@autoclosure @escaping` on a stored closure that pins side-effecting work             | Side effects don't run when expected; debugging is "huh?".                                                    | Reserve `@autoclosure` for cheap expressions (errors, defaults).                                  |
| 10.6  | Function type ABI change: adding a parameter to a public closure type                  | Source-breaking for callers. Worse: silently breaks ABI in resilient modules.                                  | Wrap closure types in a struct or use a builder.                                                  |
| 10.7  | `() -> ()` instead of `() -> Void` (or vice versa)                                    | Style inconsistency only — equivalent. Mostly a `swiftformat` issue.                                          | Pick one; the team's swiftformat config enforces.                                                 |
| 10.8  | `weak` capture of a value type (struct, enum)                                          | Value types can't be `weak`. Compiler error.                                                                  | Capture explicitly: `[copy = value]` to snapshot.                                                 |
| 10.9  | `unowned(unsafe)` "for performance"                                                    | Crashes-or-corrupts-memory if accessed post-dealloc.                                                          | `unowned` (safe), or `weak`.                                                                      |
| 10.10 | Trailing closure ambiguity with overloads                                              | Multiple trailing closures matched the wrong overload; the compiler may not warn.                              | Use parameter labels: `start(onSuccess: { … })`.                                                  |
| 10.11 | `@escaping (Result<T, Error>) -> Void` instead of `async throws -> T`                  | Old callback API in async code's clothing; can't chain, can't propagate cancellation.                          | `async throws` with structured concurrency.                                                       |
| 10.12 | Captured closure mutating captured `var` from multiple threads                         | Data race.                                                                                                    | Capture into an actor / lock, or use a sendable snapshot.                                         |
| 10.13 | Trailing closure crossing semicolons / multi-line ambiguity                            | `foo { ... }` vs `foo(); { ... }` ambiguity. Rare but real.                                                   | Always include explicit parens when ambiguity is possible.                                        |

### 10.2 Snapshot capture

```swift
var counter = 0
let increment = { counter += 1 }
let snapshot = { [counter] in print(counter) }   // captures by value

counter = 100
increment()   // counter is now 101
snapshot()    // prints 0 (the value at capture time)
```

---

## 11. Swift Package Manager pitfalls

### 11.1 Catalog

| #     | Anti-pattern                                                                                 | Why it bites                                                                                              | Fix                                                                                              |
| ----- | -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 11.1  | `// swift-tools-version:` missing or wrong                                                    | Build fails; or worse, builds with unintended toolchain defaults.                                          | Always specify; match the minimum Swift version your code uses.                                  |
| 11.2  | `dependencies: [.package(url:..., branch: "main")]`                                          | Non-deterministic; CI is unreproducible; downstream packages that pin versions can't depend on you.        | `.upToNextMajor(from: "1.2.0")` or `.exact("1.2.3")`.                                            |
| 11.3  | Missing `platforms:` declaration                                                             | Package may build with wrong deployment target; runtime crashes on `@available` paths.                     | `platforms: [.iOS(.v16), .macOS(.v13)]`.                                                          |
| 11.4  | `enableUpcomingFeature("BareSlashRegexLiterals")` in `swiftSettings` of a library             | Downstream targets inherit unexpected language modes; breaking changes propagate.                          | Confine `enableUpcomingFeature` to internal targets; document for consumers.                      |
| 11.5  | `package` access level used between packages                                                 | `package` is intra-package only. Cross-package access requires `public`.                                  | Mark needed APIs `public`.                                                                        |
| 11.6  | `.binaryTarget(name:, url:, checksum:)` checksum drift                                       | Checksum doesn't match → build fails. Worse: in a private mirror, mismatched checksum can compromise.     | Recompute checksum after every xcframework update.                                                |
| 11.7  | Mixing branch and version requirements across the dep graph                                  | SPM resolution fails because branch and version dependency requirements can't be mixed.                   | Standardise on version requirements; remove branch-based dependencies before publishing.          |
| 11.8  | Forgetting `resources:` declaration                                                          | Assets bundled into target Bundle.main, then crash on access.                                              | `resources: [.process("Assets")]`.                                                                |
| 11.9  | Using `Bundle.main` for resources from an SPM module                                          | Resources live in `Bundle.module`, not `Bundle.main`.                                                     | `Bundle.module.url(forResource: ...)`.                                                            |
| 11.10 | Test target depending on the package via product name, not target name                       | Causes weird "unable to find target" errors during resolution.                                            | Depend on the target via `.target(name: "MyTarget")` in dependencies of the test target.          |
| 11.11 | Putting CocoaPods + SPM dependencies of the same library in the same project                  | Double-symbol linker errors, or worse, two copies of the same class at runtime.                           | Pick one. Migrate fully.                                                                          |
| 11.12 | Plugins that don't have access to binary targets                                              | Known SPM limitation: plugins (build plugins, command plugins) can't depend on `.binaryTarget`.            | Wrap binary in a source target that the plugin depends on.                                        |
| 11.13 | Hard-coded local paths in `dependencies: [.package(path: "/Users/me/foo")]`                  | Breaks for every other developer.                                                                          | Relative path `../foo`, or use a Swift package registry.                                          |
| 11.14 | `Package.swift` runs side-effects at parse time                                              | Parsing runs in a sandbox; side effects break resolution.                                                  | `Package.swift` should be a pure description.                                                     |

---

## 12. Testing pitfalls

### 12.1 Catalog

| #     | Anti-pattern                                                                                  | Why it bites                                                                                                  | Fix                                                                                              |
| ----- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 12.1  | `XCTAssertEqual(actual, expected)` with no message                                            | Failure log just shows two values; debugging large structs is misery.                                          | `XCTAssertEqual(actual, expected, "User \(userID) profile mismatch")`.                            |
| 12.2  | `XCTAssert(condition)` for what should be `XCTAssertEqual` / `XCTAssertNil`                  | Loses comparison context in failure.                                                                          | Use the specific assertion.                                                                       |
| 12.3  | `let value = optional!` in test (instead of `XCTUnwrap`)                                     | Crashes the test runner; can prevent subsequent tests from running.                                           | `let value = try XCTUnwrap(optional)`. Or in Swift Testing: `try #require(optional)`.            |
| 12.4  | `wait(for: [expectation], timeout: 10)` in an async test                                      | Blocks the test runner; with strict concurrency, can deadlock.                                                 | `await fulfillment(of: [expectation], timeout: 10)`.                                              |
| 12.5  | `XCTestExpectation` fulfilled twice                                                           | `XCTestExpectation` traps on double-fulfill (by design).                                                       | Use `expectedFulfillmentCount`; or guard with a flag.                                             |
| 12.6  | `@MainActor` on EVERY test class for convenience                                              | All tests run serially on main; parallel test runs become serial.                                              | Only `@MainActor` tests that actually touch main-actor APIs.                                      |
| 12.7  | Snapshot tests of timestamped output                                                          | Snapshots include `Date()` — every CI run diffs.                                                              | Inject a `now: () -> Date` clock; freeze for tests.                                               |
| 12.8  | Test order dependence (test A sets up global state that test B uses)                          | XCTest may parallelise; order is unstable; CI flakes.                                                          | Each test sets up its own state; teardown cleans up.                                              |
| 12.9  | Tests sharing a global singleton without reset                                                | Cross-test state pollution; flaky failures.                                                                    | Reset in `tearDown` or use DI to inject a fresh instance per test.                               |
| 12.10 | `Thread.sleep(...)` in async tests                                                            | Blocks the test thread; defeats async runtime.                                                                | `try await Task.sleep(for: .milliseconds(100))`.                                                  |
| 12.11 | Network in unit tests                                                                          | Flaky, slow, dependent on internet.                                                                            | Mock at the URLSession or repository layer.                                                       |
| 12.12 | Date/Calendar in tests using `Calendar.current`                                                | Time zone differences make tests fail on CI in different regions.                                              | Fixed `Calendar(identifier: .gregorian)` with explicit timezone.                                  |
| 12.13 | `XCTAssertThrowsError(...) { error in XCTAssertEqual(error, expected) }` without typed cast  | Comparing `Error` is `Error` is `Error` — they're not Equatable.                                              | Cast: `XCTAssertEqual(error as? MyError, .someCase)`. Or typed throws.                            |
| 12.14 | Combine test that subscribes then doesn't store the cancellable                              | Subscription dies before publisher emits; test "passes" without exercising code.                              | `.store(in: &cancellables)` even in tests.                                                        |
| 12.15 | Swift Testing `@Test` function marked `async` but not awaiting the operation                  | Test passes without asserting.                                                                                | Audit all `async` tests; ensure operations are awaited.                                           |

### 12.2 Async test migration: from expectations to `await`

```swift
// Old
func testFetchUser() {
    let exp = expectation(description: "fetch")
    sut.fetchUser { result in
        XCTAssertEqual(result, .success(User(id: "1")))
        exp.fulfill()
    }
    wait(for: [exp], timeout: 5)
}

// New (XCTest)
func testFetchUser() async throws {
    let user = try await sut.fetchUser()
    XCTAssertEqual(user, User(id: "1"))
}

// New (Swift Testing)
@Test func fetchUser() async throws {
    let user = try await sut.fetchUser()
    #expect(user == User(id: "1"))
}
```

For positive Swift Testing patterns (parameterized tests, traits, confirmations, snapshot testing) see [`swift-best-practices.md` §5](./swift-best-practices.md#5-testing-strategy).

---

## 13. Documentation pitfalls

### 13.1 Catalog

| #     | Anti-pattern                                                                                | Why it bites                                                                                                  | Fix                                                                                              |
| ----- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 13.1  | `public func foo(...)` with no `///` comment                                                | Library consumers have no docs; DocC generates empty pages.                                                   | Document every public symbol. Lint with `missing_docs`.                                          |
| 13.2  | `///` comment that just repeats the name                                                    | "fetches user — fetches the user". Adds noise, not signal.                                                    | Document **why** and **side effects**, not what.                                                  |
| 13.3  | `@available(*, deprecated)` without `message:`                                              | Caller sees "deprecated" with no migration path; ignores it.                                                  | `@available(*, deprecated, message: "Use newName(_:) instead — it accepts an Int now.")`.        |
| 13.4  | `@available(*, deprecated, renamed: "...")` pointing to a moved symbol                       | The renamed reference fails to resolve; Xcode shows "Symbol not found".                                       | Verify the renamed target exists; mark with the full module path if needed.                       |
| 13.5  | DocC catalog with broken `<doc:>` links                                                     | Generation succeeds with warnings; consumers see a broken page.                                                | CI-fail on DocC warnings: `xcodebuild docbuild -workspace ... | grep -i warning`.                |
| 13.6  | `///` on `internal` or `private` for performative reasons                                    | Wastes time, not surfaced anywhere.                                                                            | Comment internal where helpful for maintainers; don't enforce.                                    |
| 13.7  | DocC `@Tutorial` files committed without testing the build                                   | Tutorials reference assets that aren't bundled; doc generation fails silently.                                | Run `swift package generate-documentation` in CI.                                                 |
| 13.8  | Deprecation messages without a version: `"deprecated"` instead of `"deprecated in 3.2"`     | Maintainers can't grep for old deprecations.                                                                  | Always include version: `@available(*, deprecated, message: "Removed in 4.0. Use ...")`.         |
| 13.9  | DocC missing `// Mark:` section markers in long files                                       | DocC navigation flat; users can't jump.                                                                       | `// MARK: - Public API`, `// MARK: - Private`.                                                    |
| 13.10 | `/** ... */` block comments instead of `///`                                                | Both supported; mixed style is jarring.                                                                       | Pick one (almost always `///`).                                                                   |

### 13.2 Good deprecation pattern

```swift
@available(*, deprecated, message: "Use `fetchUser(id:)` — accepts a UserID instead of String. Removed in 4.0.", renamed: "fetchUser(id:)")
public func fetchUser(_ id: String) async throws -> User {
    try await fetchUser(id: UserID(value: id))
}

public func fetchUser(id: UserID) async throws -> User { … }
```

---

## 14. API design pitfalls

### 14.1 Catalog

| #     | Anti-pattern                                                                                       | Why it bites                                                                                                                       | Fix                                                                                              |
| ----- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 14.1  | `public class Foo` when `Foo` is a value-semantic data bag                                          | Reference semantics surprises consumers; harder to make `Sendable`.                                                                | `public struct Foo`. If you need identity, `final class` + `Identifiable`.                       |
| 14.2  | `public init() { … }` synthesised on a frozen-looking struct that should NOT have public init       | Removing init later is source-breaking.                                                                                            | Explicit private init; provide factory methods or builders.                                       |
| 14.3  | Public function accepting `[String: Any]`                                                          | Untyped, unverifiable, every call site re-invents conventions.                                                                     | Concrete struct with `Codable`. Or a typed builder.                                              |
| 14.4  | `public enum Status { case ok, error, pending }` without `@frozen`                                  | Future cases can be added; consumers must `default` their switches. Without `@frozen`, you cannot make assumptions in inlined paths. | If the enum is genuinely stable, `@frozen`. Otherwise document that new cases may be added.       |
| 14.5  | `@frozen` on an enum that subsequently needs new cases                                              | Adding cases is now a breaking ABI change.                                                                                          | Conservative: don't mark `@frozen` unless you're certain.                                         |
| 14.6  | `extension Array: Identifiable` (retroactive conformance to stdlib protocol)                       | Swift 5.9 warns; 6.0 may error: "Conformance of imported type 'Array' to imported protocol 'Identifiable'…".                       | Avoid retroactive conformances to types you don't own. Wrap in your own type.                    |
| 14.7  | `@available(iOS 16.0, *)` on new APIs forgotten                                                    | Crash on older OS; the symbol isn't there.                                                                                          | Always mark new APIs `@available`; CI on multiple deployment targets.                            |
| 14.8  | Public function with default-parameter-value changes (source-breaking)                              | Default changes: callers who didn't pass the param now see different behavior.                                                     | Document default changes loudly; bump major.                                                      |
| 14.9  | Public typealias to a complex generic that later needs different generics                          | Removing the typealias is source-breaking.                                                                                          | Use typealiases sparingly in public API.                                                          |
| 14.10 | Public `init(...)` that throws — easy to forget the throw                                          | Subclasses inheriting init may not preserve throwing.                                                                                | Document the throwing contract; use typed throws.                                                |
| 14.11 | Public function returning `[String: Any]` (the JSON-bag pattern)                                    | Same as 14.3 but on the return side.                                                                                                | Codable struct.                                                                                  |
| 14.12 | Public class without `final` (when not designed for inheritance)                                    | Consumers may subclass; you become coupled to their assumptions.                                                                    | `public final class` by default; `open class` only when inheritance is part of the contract.     |
| 14.13 | Public protocol with default implementations that callers can't see                                 | Surprising behavior; callers think the protocol is "simple" but it has hidden methods.                                              | Document default impls in the protocol's `///`.                                                  |
| 14.14 | Public types missing `Sendable` conformance                                                         | Strict-concurrency consumers must `@unchecked` their way around.                                                                    | `public struct Foo: Sendable { ... }` whenever possible.                                          |
| 14.15 | Public initializer accepting `Any` / `AnyObject` for "flexibility"                                  | Type erasure poisons the API; consumers must dynamic-cast.                                                                          | Generics or protocols with concrete witness types.                                               |
| 14.16 | Public function with multiple overloads differing only by closure shape                              | Trailing-closure ambiguity at call sites; type inference picks the wrong one.                                                      | Distinct names: `subscribe(onValue:)`, `subscribe(onResult:)`.                                   |
| 14.17 | Public `static let shared = MyClass()` (singleton anti-pattern)                                     | Hidden global state; testing is hard; lifecycle is opaque.                                                                          | Inject dependencies; use a Composition Root.                                                     |
| 14.18 | Public `nonisolated(unsafe) static var counter = 0`                                                 | Caller has no way to know this is concurrency-broken.                                                                                | Wrap in actor or `@MainActor`.                                                                   |
| 14.19 | `public protocol Foo { associatedtype X }` then using `[any Foo]` everywhere                        | Existential boxing is expensive; consumers can't reason about the X.                                                                | Primary associated types: `protocol Foo<X> { associatedtype X }`, then `any Foo<Int>`.           |
| 14.20 | Public function that takes a non-`@Sendable` closure but is called from concurrent contexts        | Concurrency error at consumer site; consumer can't fix without forking.                                                            | `@Sendable` closures in public API by default.                                                   |

### 14.2 Retroactive conformance — the new rules

```swift
// Bad — warning in 5.9, may error in some 6.x configurations
extension URL: Identifiable {
    public var id: URL { self }
}

// Fix 1: Use a wrapper.
struct IdentifiableURL: Identifiable {
    let value: URL
    var id: URL { value }
}

// Fix 2: if you accept the risk and must do it.
extension URL: @retroactive Identifiable {
    public var id: URL { self }
}
// The @retroactive marker is required in Swift 6 to silence the warning.
// Document why and accept the global-uniqueness risk.
```

### 14.3 Public init synth pitfall (Sendable breakage)

```swift
// Bad
public struct Config: Sendable {
    public var maxRetries: Int = 3
    // Compiler synthesises a public init(maxRetries: Int = 3)
    // — once shipped, adding more fields breaks all callers using positional args.
}

// Fix: Explicit, controlled init.
public struct Config: Sendable {
    public var maxRetries: Int

    public init(maxRetries: Int = 3) {
        self.maxRetries = maxRetries
    }
}
// Now adding fields with default values is non-breaking.
```

### 14.4 @frozen tradeoffs

| Case | `@frozen`? |
|------|-----------|
| `enum Bool { case `true`, `false` }` | yes (stdlib) |
| `enum HTTPMethod { .get, .post, .put, … }` (rare extensions) | maybe — RFC-bounded, but new methods do exist (`PATCH` was added late) |
| `enum NetworkError { … }` (your domain) | usually NO — keep room to add cases |
| `enum LogLevel { .debug, .info, .warn, .error }` | leaning yes — stable set |
| Public `struct` layout | `@frozen` rare; only for low-level interop types |

---

## Appendix A: SwiftLint quick-reference & starter config

### A.1 Default (enabled out of the box)

- `force_cast` — `as!`
- `force_try` — `try!`
- `weak_delegate` *(opt-in in newer versions; verify)*
- `redundant_self`
- `redundant_optional_initialization`
- `unused_optional_binding`
- `redundant_string_enum_value`
- `redundant_void_return`
- `legacy_constructor` / `legacy_constant` / `legacy_random` / `legacy_hashing` / `legacy_cggeometry_functions` / `legacy_nsgeometry_functions` / `legacy_objc_type`
- `empty_count` (opt-in in some configurations)

### A.2 Opt-in (recommended for new codebases)

- `force_unwrapping` — `!`
- `implicitly_unwrapped_optional`
- `implicit_optional_initialization`
- `contains_over_filter_count`
- `contains_over_filter_is_empty`
- `contains_over_first_not_nil`
- `sorted_first_last`
- `reduce_boolean`
- `yoda_condition`
- `existential_any`
- `unchecked_sendable_via_isolated` (newer rule)
- `nonisolated_unsafe` (newer rule)
- `async_without_await`
- `incompatible_concurrency_annotation`
- `unhandled_throwing_task`
- `notification_center_detachment`

### A.3 Analyzer rules (need `swiftlint analyze`)

- `unused_declaration`
- `unused_import`
- `typesafe_array_init`

### A.4 Suggested `.swiftlint.yml` starter (high-signal opt-ins)

```yaml
opt_in_rules:
  - force_unwrapping
  - implicitly_unwrapped_optional
  - contains_over_filter_count
  - contains_over_filter_is_empty
  - contains_over_first_not_nil
  - sorted_first_last
  - empty_count
  - reduce_boolean
  - existential_any
  - async_without_await
  - unhandled_throwing_task

disabled_rules:
  - todo                # team-decision: tolerate TODOs

line_length:
  warning: 140
  error: 200
```

---

## Appendix B: Cross-section pattern map

When debugging real production issues, the symptom maps to a section:

| Symptom                                                    | Section to check |
|------------------------------------------------------------|------------------|
| EXC_BAD_INSTRUCTION on `!` somewhere                       | 1 (force-unwrap) |
| Memory grows monotonically, no leaks reported              | 2 (cycles), 8 (memory) |
| `SWIFT TASK CONTINUATION MISUSE` log                       | 3.7–3.9 (continuations) |
| Sporadic crash on "dispatch_assert_queue"                  | 3.1, 3.3 (@unchecked / wrong actor) |
| UI updates lag / occasionally don't apply                  | 3.4 (actor reentrancy), 7.2 (Observable lifecycle) |
| App hangs on dismissal of a screen                         | 3.17 (cancellation), 2.6 (Timer) |
| Tests pass locally, flake on CI                            | 12.8, 12.12 (order / timezone) |
| New version of a public API breaks consumers' builds       | 14.2, 14.4, 14.5, 14.8 |
| Decoder throws "type mismatch" on production               | 5.8 (lossy wrapping), 9.10 |
| Build slow, "type-checked timeout"                         | 4.2 (existential), 4.5 (over-specified generics) |

---

## Appendix C: Confidence and sources

This document synthesises:

- **Apple official:** Swift API Design Guidelines, Migrating to Swift 6 guide, DocC documentation, Swift Evolution proposals (SE-0335 `existential any`, SE-0364 retroactive conformance warning, SE-0413 typed throws, SE-0192 frozen enums, SE-0272 binary dependencies, SE-0337 incremental migration).
- **Compiler diagnostics:** Swift 6.0 / 6.1 / 6.2 strict-concurrency diagnostic messages and runtime trap signatures.
- **SwiftLint / SwiftFormat:** rule directories at `realm.github.io/SwiftLint/rule-directory.html` and `github.com/nicklockwood/SwiftFormat/blob/main/Rules.md`.
- **Community reference posts:** Hacking with Swift, Swift by Sundell, Donny Wals, SwiftLee (Antoine van der Lee), Jared Sinclair, Jesse Squires, Holy Swift, Fatbobman, Quality Coding, theswiftdev.com, fline.dev, Doug Gregor's compiler corner.
- **Swift Forums threads:** continuation misuse, MainActor protocol conformance, default actor isolation, retroactive conformance, Sendable design.

Confidence levels:

- **High** — Sections 1, 2, 5, 6, 11, 12 (well-established patterns).
- **High** — Section 3 (current as of Swift 6.2 release; default isolation behaviour verified against Donny Wals's post 2025-Q4).
- **Medium-high** — Section 4 (existential overhead numbers vary by benchmark; the qualitative direction is well-established).
- **Medium** — Section 7 (Observable lifecycle behaviour has evolved between Xcode 15 → 26; cross-version differences may apply).
- **High** — Sections 13, 14 (API design guidance is stable).

Limitations:

- SwiftLint rule names evolve; some rules listed as "opt-in" may have flipped to default or been renamed. Verify against your installed SwiftLint version.
- The Swift 6.2 `@concurrent` keyword and module-level default isolation are still settling into community patterns — usage guidance may shift through 2026.
- Some pitfalls (3.11 on `os_unfair_lock` + await) are documented in the lock's `man` page and Swift Forums but lack a single canonical "thou shalt not" reference; they are widely-acknowledged folklore rather than codified.

---

## Sources

### Apple official

- [Swift API Design Guidelines](https://www.swift.org/documentation/api-design-guidelines/)
- [Migrating to Swift 6](https://www.swift.org/migration/documentation/migrationguide/)
- [Apple Developer — DocC](https://developer.apple.com/documentation/docc)
- [Swift 6.2 Released](https://www.swift.org/blog/swift-6.2-released/)

### Swift Evolution proposals (anti-pattern-relevant)

- [SE-0192 — Frozen Enums](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0192-non-exhaustive-enums.md)
- [SE-0272 — Binary Dependencies](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0272-swiftpm-binary-dependencies.md)
- [SE-0335 — Existential `any`](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0335-existential-any.md)
- [SE-0337 — Incremental Migration](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0337-support-incremental-migration-to-concurrency-checking.md)
- [SE-0364 — Retroactive Conformance Warning](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0364-retroactive-conformance-warning.md)
- [SE-0413 — Typed Throws](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0413-typed-throws.md)
- [SE-0414 — Region-Based Isolation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0414-region-based-isolation.md)
- [SE-0430 — Transferring Parameters and Results (`sending`)](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0430-transferring-parameters-and-results.md)

### Linting & formatting

- [SwiftLint rule directory](https://realm.github.io/SwiftLint/rule-directory.html)
- [SwiftLint repository](https://github.com/realm/SwiftLint)
- [SwiftFormat rules](https://github.com/nicklockwood/SwiftFormat/blob/main/Rules.md)

### Swift Forums (canonical discussion threads)

- [forums.swift.org — Continuation misuse threads](https://forums.swift.org/search?q=continuation%20misuse)
- [forums.swift.org — Default actor isolation discussion](https://forums.swift.org/search?q=default%20actor%20isolation)
- [forums.swift.org — Sendable design](https://forums.swift.org/c/development/concurrency/)

### Practitioner explainers

- [Donny Wals — Concurrency posts (`@concurrent`, default isolation, Task timeout)](https://www.donnywals.com/)
- [SwiftLee (Antoine van der Lee) — Concurrency series](https://www.avanderlee.com/category/concurrency/)
- [Matt Massicotte — SE-0414, SE-0430 explainers](https://www.massicotte.org/)
- [Jared Sinclair — `@unchecked Sendable` runtime crash analysis](https://jaredsinclair.com/)
- [Jesse Squires — `@Observable` is not a drop-in replacement](https://www.jessesquires.com/blog/2024/09/09/swift-observable-macro/)
- [Fatbobman — Default Actor Isolation: New Problems from Good Intentions](https://fatbobman.com/en/posts/default-actor-isolation/)
- [Swift with Majid — Mastering Task Groups, Typed Throws](https://swiftwithmajid.com/)
- [NSHipster — Foundation Error Protocols](https://nshipster.com/swift-foundation-error-protocols/)
- [Nonstrict — The Four Audiences of Swift Errors](https://nonstrict.eu/blog/2026/the-four-audiences-of-swift-errors/)
- [Swift by Sundell — Propagating user-facing errors](https://www.swiftbysundell.com/articles/propagating-user-facing-errors-in-swift/)

*End of reference. Total scope: 14 sections, ~180 cataloged anti-patterns, 3 appendices, ~25 code-level examples.*
