# Swift Refactoring Cheatsheet (Swift 6.2+)
Purpose: Zen-flavored slice of the Swift knowledge base — code-smell-to-idiom transformations, naming hygiene, magic-number cleanup, and refactor anti-patterns. Behavior-preserving only.
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Function Extraction Signals (Swift-specific)
1. **A closure capturing 4+ values from the enclosing scope** — promote to a named method with explicit parameters. Captures hide control flow.
2. **Repeated optional unwrapping of the same chain** in 3+ call sites — extract a `private func` returning the unwrapped or `throw`-ing value.
3. **Nested `do-try-catch` chains > 2 deep** — each layer should resolve one error domain; flatten by extracting per-domain helpers that throw typed errors.
4. **SwiftUI body block > 60 lines** — extract a child view; SwiftUI's diff cost rises with body depth.
5. **`@MainActor` method doing 80% off-main work** — extract the off-main portion into a `nonisolated` helper; keep the `@MainActor` method as the UI sync point.
6. **`switch` with shared post-processing across arms** — extract the post-processing as a helper; arms reduce to value construction.
- 3-line block used in one place; inlining is clearer.
- A helper that requires more isolation annotations than the inlined version.
- A function whose name would be `do{Original}Helper` — that means the original needed renaming, not splitting.
---
## Naming Hygiene (Swift API Design Guidelines)
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
- **Avoid `IFoo`/`FooProtocol`** Java-isms when the repository follows Swift API naming conventions.
### Boolean property names
- Read as English assertions: `view.isHidden`, `string.isEmpty`, `array.contains(x)`.
- Avoid double negatives: `isNotEmpty` → use `!isEmpty`.
### Error type names
- Conform to `Error`; name ends with `Error`: `DecodingError`, `NetworkError`.
- Cases do NOT repeat the type prefix: `NetworkError.timeout`, not `NetworkError.networkTimeout`.
---
## Concurrency Refactors (Approachable Concurrency)
- **`@MainActor` everywhere → fine-grained isolation**
- **`withCheckedContinuation` → `AsyncStream` builder**
### `@unchecked Sendable` retrofit → real `Sendable`
- `actor` for mutable shared state.
- `let` properties on a `final class` with all `Sendable` fields.
- Mutex-backed wrapper if you genuinely need `class` semantics: `Mutex<T>` (6.0+).
---
## Refactor Anti-Patterns to Avoid
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
