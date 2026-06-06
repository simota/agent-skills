# Swift Code-Review Cheatsheet (Judge)

Agent-specific slice for **Judge** (multi-engine code review — bugs / security / logic / intent). Baseline assumes Swift 6.2+ / Xcode 26 (as of 2026-05).

This file does **not** duplicate the source of truth. Read it alongside:

- [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md) — Swift API Design Guidelines, error handling, concurrency, value-type discipline
- [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md) — force-unwrap, retain cycle, ARC, concurrency pitfalls
- [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md) — Swift 6 strict concurrency, isolation regions, `Sendable`, ownership

The role of this cheatsheet: **a priority-ordered checklist + engine-routing rules + SwiftLint policy + false-positive guide so review effort focuses on findings worth fixing**.

---

## 1. Priority checklist — highest signal first

Numbered roughly by signal-to-noise ratio. The top items catch real crashes / data races; the bottom items catch style drift.

### Tier 1 — Crashes, data races, leaks (block merge)

1. **`try!` / `as!` / `!` (force-unwrap) in non-test code: justified?**
   - In libraries: replace with `guard let` / `try?` / typed throw.
   - In app code: only acceptable with an `// INVARIANT: ...` comment proving infallibility (e.g., `Bundle.main.url(forResource:)` for a known static asset shipped in the bundle).
   - SwiftLint rules: `force_try`, `force_cast`, `force_unwrap`, `implicitly_unwrapped_optional`.
   - See [anti-patterns §1](../../builder/reference/swift-anti-patterns.md).

2. **`@unchecked Sendable`: lock held? immutable witness?**
   - `@unchecked Sendable` opts out of the Sendable checker. Every use MUST carry a comment explaining the synchronization (lock, actor, immutable storage).
   - Without justification, the type can be raced from multiple isolation domains → undefined behavior under Swift 6 strict concurrency.
   - See [best-practices §7](../../builder/reference/swift-best-practices.md) and [language-spec §4 — Sendable](../../builder/reference/swift-language-spec.md).

3. **`nonisolated(unsafe)`: justified or escape hatch?**
   - `nonisolated(unsafe) let / var` opts a property out of actor isolation. Acceptable for immutable letters; suspicious on `var`.
   - Should be paired with an explicit synchronization mechanism (OSAllocatedUnfairLock, `DispatchQueue`, atomic) and a comment.
   - Hot finding under Swift 6 migration audits.

4. **`Continuation` resume-once invariant**
   - `withCheckedContinuation` / `withUnsafeContinuation` MUST resume exactly once. Resuming zero times = leak; resuming twice = trap.
   - `withCheckedContinuation` traps in debug; `withUnsafeContinuation` is silent UB. Audit for every code path → exactly one resume.
   - Common bug: callback API that calls back on multiple events; wrap with `CheckedContinuation` + guard via `Atomic<Bool>`.
   - See [anti-patterns §4](../../builder/reference/swift-anti-patterns.md).

5. **`Task { }` without `[weak self]` retain**
   - `Task { await self.work() }` strong-captures `self` for the task's lifetime. If the task is long-running and stored on `self`, retain cycle.
   - Fix: `Task { [weak self] in await self?.work() }` or store the task in a property and cancel in `deinit`.
   - SwiftLint: `weak_delegate`, custom rules for `Task { ... self ... }`.

6. **Actor reentrancy: state read-after-`await` assumes no change**
   - Inside an actor, after `await`, the actor's state may have changed (reentrancy). Code that reads `self.x`, awaits something, then uses the *original* `self.x` is buggy.
   - Audit pattern: any `await` followed by a read of a previously-cached property.
   - See [language-spec §4.3 — actor reentrancy](../../builder/reference/swift-language-spec.md).

7. **`@MainActor` everywhere as escape hatch**
   - Marking everything `@MainActor` silences the concurrency checker without fixing the underlying isolation problem. Cost: every call from background → main-thread hop.
   - Audit ratio: if more than ~30% of types are `@MainActor`, the author is using it as a checker bypass.
   - Push state ownership into actors; expose `@MainActor` only at the UI boundary.

8. **`IBOutlet` force-unwrap (`@IBOutlet var label: UILabel!`)**
   - Legacy Interface Builder pattern; modern alternative: SwiftUI or programmatic outlets with `let` + initializer injection.
   - Migration: in new UIKit code, prefer `@IBOutlet var label: UILabel? = nil` + guarded access; in SwiftUI, the question doesn't arise.

9. **Missing `[weak self]` / `[unowned self]` capture lists in closures**
   - Closures stored as properties (delegates, completion handlers held in dictionaries) need explicit capture lists.
   - Heuristic: any closure that escapes the function (`@escaping`) accessing `self` needs a capture list.
   - SwiftLint: `escaping_self`, `unowned_variable_capture`.
   - See [anti-patterns §2](../../builder/reference/swift-anti-patterns.md).

10. **`URLSession` certificate validation customization**
    - Custom `URLSessionDelegate.urlSession(_:didReceive:completionHandler:)` overriding `URLAuthenticationChallenge` is a security-critical surface. Hardcoded pinning may be intentional; turning off validation entirely (`URLCredential(trust: protectionSpace.serverTrust!)` blindly) is a finding.
    - Audit: every `disposition: .useCredential` in delegate code should justify *why* the certificate was trusted.

### Tier 2 — Public API correctness (block merge for library targets)

11. **`Error` type missing `Sendable` conformance**
    - Errors are thrown across isolation boundaries. Without `Sendable`, Swift 6 mode emits a warning escalating to error.
    - Fix: `enum AppError: Error, Sendable { ... }`.

12. **Public enum without `@unknown default`**
    - Apple frameworks ship `@frozen` and `@unknown` enums. Switching over them without `@unknown default` produces warnings; over a non-frozen enum, a future case is silently mishandled.

13. **Public protocol with associated type but no `AnyXxx` erasure or primary associated type**
    - With Swift 5.7+ primary associated types (`protocol P<T>`), opaque erasure is easier. Public protocols with associated types and no primary marker force callers to invent `AnyP` boilerplate.

14. **Public struct with `public` fields holding invariants**
    - `public struct User { public var email: String }` — locks in representation; no future invariant. Any validation requires a breaking change.
    - Prefer `public private(set) var` with a `public init(...)` validator.

15. **Missing `Sendable` on protocols whose implementations cross actors**
    - If a protocol type is passed across actor boundary, its conformances need `Sendable`. Forgetting it propagates the constraint to every implementor.

### Tier 3 — Design smells (review comment, not block)

16. **Force-unwrap of literals (`URL(string: "https://...")!`)**
    - Static literals are infallible at compile time but Swift can't prove it. SwiftLint `force_unwrap` flags; fix is `// swiftlint:disable:next force_unwrap` with a comment, or migrate to `URL.appendingPathComponent`-style builders.

17. **`Result<T, Error>` callbacks where `async throws` would do**
    - On Swift 5.5+, `async throws` is the idiomatic shape. Result-based callbacks are 2025 legacy; migration smell.

18. **`Combine.Publisher` in new code where `AsyncSequence` would do**
    - Same direction — Apple's new APIs ship `AsyncSequence`. Combine is maintained but not the forward path.

19. **`@Published` for large structs**
    - `@Published` emits the entire value on any change. For large structs, use `@Observable` macro (Swift 5.9+) which has per-property observation.

20. **`XCTest` instead of Swift Testing**
    - Swift Testing (Swift 5.10+, Xcode 16+) is the new framework. Migration smell when new tests still use XCTest.

---

## 2. Intent-vs-code mismatch signals (Swift-specific)

Judge's distinctive capability is catching when the code does something *other than what the author intended*. Swift-specific signals:

| Mismatch signal | What to ask |
|-----------------|------------|
| Function named `make*` or `create*` returning a `Result<T, E>` | "Make" implies infallibility per API guidelines — should it throw, or rename? |
| `func foo()` with `@discardableResult` but doc says "result is important" | Either rename to `foo_get*` or remove `@discardableResult` |
| Generic bound looser than docstring promises | `func foo<T: Sendable>(...)` but docs say "any value" — `T: Sendable` bound is intentional |
| `nonisolated func` accessing actor-isolated state via closure | The closure captures actor state without await; usually a missing isolation annotation |
| `weak var delegate` but the API says "owning relationship" | Naming mismatch — "delegate" usually weak; "controller" usually strong |
| `init(...)` is failable (`init?`) but callers all force-unwrap | Either make it non-failable with validation in body, or the callers are misusing |
| Function uses `Task.detached` but doc says "scoped" | Detached escapes structured concurrency — usually a bug |
| `_ = await x` (discarding result of async fn) | Either fire-and-forget intent (use `Task { _ = ... }`) or the result was load-bearing |
| `@escaping` closure stored without `[weak self]` | Almost always a retain cycle in the making |
| Async function returning `Result<T, E>` instead of throwing | Swift 5.5+ idiom is `async throws -> T`; `async -> Result<T, E>` is a sign of API translation lag |

---

## 3. SwiftLint policy

The default SwiftLint rules are useful but noisy; Judge applies a policy.

### 3.1 Elevate to error (block merge)

```yaml
# .swiftlint.yml
opt_in_rules:
  - force_try               # treat all `try!` as error
  - force_unwrap            # treat `!` as error outside tests
  - force_cast              # treat `as!` as error
  - implicitly_unwrapped_optional  # `var x: T!` outside IBOutlets
  - missing_docs             # public symbols need docs
  - private_outlet           # IBOutlets should be private
  - prohibited_super_call    # custom config — list lifecycle methods
  - weak_delegate            # delegates default weak
  - escaping_self            # capture-list discipline
  - unowned_variable_capture # unowned needs scrutiny
  - no_fallthrough_only      # fallthrough-only case is suspect
  - empty_count              # `count == 0` → `isEmpty`
  - empty_string             # `string == ""` → `isEmpty`
  - private_unit_test        # tests must be private
  - identifier_name          # naming convention
  - line_length              # 120 default

# Block merge on these
error_thresholds:
  force_try: 0
  force_unwrap: 0
  force_cast: 0
  implicitly_unwrapped_optional: 0
```

### 3.2 Keep as warning

- `function_body_length` (lower bar for review attention, not block)
- `type_body_length`
- `cyclomatic_complexity`
- `nesting`
- `line_length` (>120 char) — warn at 120, error at 200

### 3.3 Default-allow (false-positive heavy)

- `type_name` flags `URL` / `UI` / `API` as too short — these are intentional acronyms.
- `identifier_name` flags `i`, `j`, `n` in numeric loops — intentional.
- `force_unwrap` on `IBOutlet` legacy code — pre-migration. Migrate; don't fight.
- `unused_optional_binding` flags `if let _ = x` — sometimes intentional for side-effect checking.

### 3.4 Per-target context

- **Library target** (Swift Package Manager `lib`): elevate `missing_docs`, `private_over_fileprivate` to error; add `explicit_acl` (require explicit `public` / `internal` markers).
- **App target**: relax `missing_docs`; keep crash-causing rules at error.
- **Test target**: blanket disable `force_try`, `force_unwrap`, `implicitly_unwrapped_optional` — tests can use them.
- **Embedded Swift target**: also disable `missing_docs` (embedded code is internal); raise bar on heap-allocating patterns.

---

## 4. Swift API Guidelines audit

The full Swift API Design Guidelines reference is in [`swift-best-practices.md §1`](../../builder/reference/swift-best-practices.md). For a PR review, prioritize:

| Principle | High-signal violation | Why it matters |
|-----------|----------------------|----------------|
| **Clarity at the point of use** | `func remove(at: Int)` instead of `func remove(at index: Int)` | Caller reads `array.remove(at: 5)`; both are fine, but inconsistent within the codebase is a smell |
| **Omit needless words** | `func removeElement(_ element: T)` should be `func remove(_ element: T)` | API guideline §3.1 |
| **Name based on side effects** | Mutating: `sort()`, non-mutating: `sorted()`. Mismatch is misleading | Found via `mutating func sortAscending(...)` (no past tense → not the non-mutating sibling) |
| **Boolean methods read as assertions** | `func empty() -> Bool` should be `var isEmpty: Bool` | Convention |
| **Parameter naming** | `func add(to user: User)` reads "add to user"; `func add(user: User)` reads "add user" — choose intent | API guidelines §2 |
| **Use type-suffixed constants for clarity** | `private let TIMEOUT = 30` should be `private let timeoutSeconds: TimeInterval = 30` | Unit + type implicit in name |
| **`init` signatures consistent with similar types** | `Foo(name:)` vs `Foo(named:)` inconsistent across codebase | Convention |
| **Generic constraints in `where` clause** | `func foo<T: Hashable & Equatable>(...)` (Hashable implies Equatable, redundant) | Cleanliness |
| **Document `throws`, `Returns`, `Parameters`** | Public `throws` fn without `/// - Throws:` doc | Documentation discipline |

---

## 5. Migration smells

Codebases on older Swift versions often have legacy patterns that didn't get migrated. Smells to flag during review:

| Old pattern | Modern (Swift 6.2 + Xcode 26) | Source |
|-------------|------------------------------|--------|
| `Combine` publishers in new code | `AsyncSequence` / `AsyncStream` | Apple's new APIs ship AsyncSequence |
| `@Published var foo` for large structs | `@Observable` macro (Swift 5.9+) | Per-property observation |
| Completion-handler API (`func fetch(completion: (Result<T, Error>) -> Void)`) | `async throws -> T` | Swift Concurrency idiom |
| `XCTAssertEqual` etc. | `#expect(a == b)` (Swift Testing) | Swift Testing, Xcode 16+ |
| `DispatchQueue.main.async { ... }` | `@MainActor` or `await MainActor.run { ... }` | Concurrency-aware UI updates |
| `unowned var delegate` | `weak var delegate` unless ownership analysis proves otherwise | Lifetime discipline |
| Class-only `protocol Foo: class` | `protocol Foo: AnyObject` | Swift 4.1+ |
| `@objc dynamic` (used only for KVO) | `@Observable` or Swift Combine observation | KVO is legacy on Swift types |
| `Thread.current.isMainThread` | `MainActor.assumeIsolated { }` (Swift 5.9+) | Concurrency-aware thread check |
| `try await Task.sleep(nanoseconds:)` | `try await Task.sleep(for: .seconds(1))` | Swift 5.7+ clock API |
| `Result<T, Error>` async return | `async throws -> T` | Idiomatic since Swift 5.5 |
| `URLSession.shared.dataTask(with:...).resume()` callback | `try await URLSession.shared.data(for: request)` | Swift Concurrency |

---

## 6. Cross-engine review tactics (Claude / Codex / agy)

Judge orchestrates multiple engines. Swift files have specific routing affinity:

| File / pattern | Primary engine | Secondary | Why |
|----------------|---------------|----------|-----|
| Type-system / generic-heavy code (custom protocol witnesses, conditional conformance) | **Codex** | Claude | Swift type inference is sophisticated; Codex is strong on type-system reasoning |
| Public API surface (`public` items, protocol design, init signatures) | **Claude** | Codex | Claude is stronger at Apple-platform conventions / docs / naming |
| Concurrency correctness (actors, Sendable, isolation regions) | **Both** (run both) | — | Failure modes are subtle; multi-engine cross-check pays off |
| Macro-heavy code (Swift macros, `@Observable`, `@Macro`) | **Claude** | agy | Claude handles AST + macro expansion reasoning well |
| SwiftUI body composition / view hierarchies | **Claude** | Codex | Apple-platform UX conventions dominate |
| Server-side Swift / NIO / Vapor | **Codex** | Claude | Codex's broader server-side training helps |
| Embedded Swift | **Codex** | — | Stdlib subset knowledge + LLVM-target reasoning |
| Long-context KMP-style projects (Swift + Kotlin shared) | **agy** | Claude | Long-context bookkeeping |

**Grounding step (mandatory)**: every Swift review finding must cite a SwiftLint rule, an API guidelines section, a Swift Evolution proposal, or one of the `builder/reference/swift-*.md` rows. Free-text "this looks wrong" is rejected by Judge's grounding filter.

---

## 7. Common false positives (don't ship these as findings)

| False positive | Why it's NOT a bug |
|---------------|---------------------|
| `force_try` on `try! NSRegularExpression(pattern: "...")` for a known-static pattern | Pattern is a literal; compiler can't prove but runtime is infallible. Allow with `// swiftlint:disable:next force_try // INVARIANT: static pattern` |
| `force_unwrap` on `Bundle.main.url(forResource: "...")!` for a shipped asset | Asset is in the app bundle; failure means broken build, fail fast is correct |
| `implicitly_unwrapped_optional` on `@IBOutlet var label: UILabel!` | Pre-modernization pattern; flag for migration but don't block |
| `force_cast` in test code | Tests intentionally fail-fast on type assumption violation |
| `weak_delegate` on a non-delegate property named `*Delegate` | Some types intentionally retain (e.g., `EnvironmentDelegate` for SwiftUI) |
| `unused_optional_binding` (`if let _ = x`) | Side-effect-checking idiom; sometimes intentional |
| `cyclomatic_complexity` on a switch over many enum cases | Exhaustive switch is the *correct* shape; complexity is mechanical |
| `type_name` on `URL`, `API`, `UI`-prefixed types | Intentional 2-letter acronyms |
| `identifier_name` on numeric loop indices `i`, `j` | Convention |
| `Task.detached` warning in tests | Tests sometimes need detached for setup/teardown |
| "Excessive `@MainActor`" finding in a UIKit-heavy file | UIKit IS main-actor-bound; almost everything `@MainActor` is appropriate |
| `nonisolated` warning on a pure-function utility (no state) | Truly isolated-free utilities don't need actor isolation |
| `redundant_optional_initialization` on `var x: T? = nil` for clarity | Sometimes the explicit nil aids reader; style call |

---

## 8. SwiftUI / Liquid Glass review

SwiftUI rendering correctness, `@State` placement, view-modifier ordering, and Liquid Glass material adoption are **owned by the native skill**. For SwiftUI / Liquid Glass review work, route via:

- Native skill for SwiftUI design correctness, state ownership, view-modifier order, accessibility.
- Judge owns: data-race detection in `@StateObject` / `@ObservedObject` mutations, `await` placement in `.task`, retain cycles inside view closures.

Liquid Glass specifically (Apple's 2026 material): adoption correctness (proper SF Symbol use, accessibility labels, dark/light variants) routes to native; data-race / retain-cycle issues inside Liquid Glass containers route to Judge.

---

## 9. Judge-specific routing rules for Swift

1. **No finding without a citation.** Every finding must reference a SwiftLint rule, an API guideline ID, an anti-pattern row, or a Swift Evolution proposal. "Looks wrong" gets dropped.
2. **Tier 1 findings block merge.** Force-unwrap in non-test, `@unchecked Sendable` without justification, `Continuation` resume invariant, retain cycle — these are not "style". Highest severity.
3. **Library vs app distinction.** `try!` in `main.swift` of a CLI with an `INVARIANT:` comment is acceptable; the same in a Swift Package library is Tier 2.
4. **Swift 6 strict concurrency mode matters.** Check `swiftSettings: [.swiftLanguageMode(.v6)]` or `// swift-tools-version: 6.0`. If 6 mode is on, raise the bar on Sendable / actor isolation findings.
5. **Multi-engine cross-check on concurrency.** Sendable / actor reentrancy / Continuation are subtle enough that running both Claude and Codex pays off.
6. **False-positive filter (§7) runs before publishing.** Don't burn reviewer trust on noise.
7. **Suggest, don't dictate, on style.** "Consider `async throws` over completion-handler" not "must change". Save imperative tone for Tier 1 + Tier 2.
8. **Defer SwiftUI / Liquid Glass design questions** to native skill; Judge keeps the data-race / lifecycle layer.

---

## Sources

- Swift API Design Guidelines — https://www.swift.org/documentation/api-design-guidelines/
- SwiftLint rules reference — https://realm.github.io/SwiftLint/rule-directory.html
- The Swift Programming Language (Swift 6) — https://docs.swift.org/swift-book/
- Swift Evolution proposals — https://github.com/swiftlang/swift-evolution
- Swift Concurrency Migration Guide — https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/
- Swift Testing — https://developer.apple.com/xcode/swift-testing/
- WWDC — "Migrate your app to Swift 6", "Discover concurrency in SwiftUI"
- Source of truth for all underlying knowledge:
  - [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md) (API guidelines, error handling, concurrency, frameworks)
  - [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md) (force-unwrap, retain cycles, ARC, concurrency pitfalls)
  - [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md) (Swift 6 strict concurrency, Sendable, isolation, ownership)
