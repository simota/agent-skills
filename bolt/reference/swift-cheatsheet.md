# Swift Performance Cheatsheet (Bolt)
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## 1. Profiler decision tree (Instruments + os_signpost)
**Rule**: profile first, hypothesize second, change code third. Almost every "I'm sure it's X" intuition about Swift hot paths is wrong by ≥30%, and Swift's ARC + generic specialization make it especially counter-intuitive.
- **1.1 OSSignposter — the right way to mark intervals**
---
## 2. Compiler optimization levels
| Flag | When | Trade |
|------|------|-------|
| `-Onone` | Debug | No optimization; debug-friendly; **never ship** |
| `-O` | Default Release | Speed-oriented; generic specialization, inlining, ARC opt |
| `-Osize` | Size-critical (Embedded, watchOS, App Clip) | 5–15% slower; meaningfully smaller `.text` |
| `-Owholemodule` | (Default in modern Xcode) | Cross-file inlining; required for true generic specialization |
| `-whole-module-optimization` | Same; explicit form in SwiftPM / scripts | Always on for release in Xcode 14+ |
**Key insight**: without WMO, the compiler cannot inline across files in the same module. Cross-module inlining requires `@inlinable` (see §3).
---
## 3. Cross-module inlining: `@inlinable` + `@usableFromInline`
**Trade-offs**:
- Body becomes part of the ABI surface — changing it after shipping is technically a breaking change.
- Speeds up cross-module hot paths by 2–10x for tiny functions that would otherwise be a call+ARC.
- Adds compile time for callers.
**When to use**: small (< 10 LOC) cross-module hot functions, mostly in standard-library-style internal frameworks. Not for app code (which is one module).
---
## 4. Copy-On-Write (COW) tuning
### 4.1 Common COW pitfalls
| Anti-pattern | Why it bites | Fix |
|--------------|-------------|-----|
| Passing `Array` to a closure that holds another reference, then mutating | Mutation triggers copy on every call | Use `inout`, or `withContiguousMutableStorageIfAvailable` |
| `var arr = self.field; arr.append(x); self.field = arr` | Two refs alive at append → copy | Mutate in place: `self.field.append(x)` |
| `lazy var` holding an `Array` whose backing is read elsewhere | Lazy backing + reads = multiple refs | Use a private stored property |
| `for x in array.indices { array[x] = ... }` on a struct-stored array shared via property | Same | Mutate via `withUnsafeMutableBufferPointer` |
- **4.2 `reserveCapacity` for growable collections**
### 4.3 `ContiguousArray<T>` over `Array<T>` for value types
- You know the element type is a Swift value type or class that does **not** need ObjC interop.
- Hot loop where you want the simplest possible memory layout.
- You're going to call `withContiguousStorageIfAvailable` / `withUnsafeBufferPointer` anyway.
---
## 5. Unsafe buffer pointers in hot loops
**Auto-vectorization** in Swift requires:
- Flat `for i in 0..<n` loop shape (not `forEach`, not `for x in collection`).
- No early `return` / `break` in the loop body.
- Element type matches a vector lane (`Float`, `Double`, fixed-width `Int`).
- `-O` enabled.
---
## 6. ARC + autoreleasepool placement
### 6.1 The autoreleasepool fix
**When you need autoreleasepool**:
- Tight `for` loop calling Foundation / Objective-C bridging APIs.
- Background work that does not return to a runloop (no autorelease pool drain).
- Image-processing loops (`UIImage`, `CGImage`, `CIImage` allocate via NS).
**When you don't**:
- Pure Swift code (no NS bridging).
- Code already inside a SwiftUI view or async task (system manages pools).
### 6.2 ARC traffic reduction patterns
| Pattern | ARC effect |
|---------|-----------|
| Pass class via `let` (capture) | retain + release per scope |
| Pass class via `inout` | No extra ARC (lvalue passed) |
| `unowned` over `weak` in closure capture | 1 less atomic op per access |
| Avoid `Array<SomeClass>` in hot path | Each element retained on read |
| Use `final class` | Devirtualizes; enables more inlining |
---
## 10. Combine vs AsyncSequence: cost model
| Property | Combine | AsyncSequence |
|----------|---------|---------------|
| Subscription | Hot (publishers active before subscriber) | Cold (work starts on `for await`) |
| Cancellation | Cancellable token, must store | Task cancellation, automatic in `Task` |
| Memory per subscriber | Heavier — Subscriber, Subscription, DemandManagement chain | Lighter — Task local state |
| Backpressure | Demand-based (`Subscriber.demand`) | Pull-based by definition |
| Performance | Better for many synchronous-ish events | Better for I/O-bound streams |
| Apple's roadmap | Maintained, not deprecated, but new APIs ship `AsyncSequence` | Forward direction |
**Routing**:
- New code: prefer `AsyncSequence` / `AsyncStream`.
- Migrating UIKit: Combine still useful for `UIControl.publisher`-style adapters.
- High-frequency event streams (>10k/s): Combine often wins on raw throughput.
- Long-lived observation chains: AsyncSequence is easier to cancel correctly.
---
## 12. Embedded Swift (`-Osize`) constraints
- No reflection (`Mirror`), no existential containers (`Any`), no class hierarchies with dynamic dispatch unless `final`.
- Compiled with `-Osize` always.
- Generic specialization is mandatory (no runtime generic dispatch).
- `String` is opt-in; default is `StaticString`.
- No exception handling (`try?`/`throws` work; `try!` panics).
**Bolt's role for embedded**: confirm the stdlib subset cost is understood. A `print(...)` call drags in `String` machinery; replace with `swift_log_println_static` or platform-specific output.
---
## 13. Linker size: strip, dead-code stripping, framework cost
| Lever | Effect | How |
|-------|--------|-----|
| `DEAD_CODE_STRIPPING = YES` | Removes unused symbols | Xcode build setting (default YES) |
| `STRIP_INSTALLED_PRODUCT = YES` + `STRIP_STYLE = all` | Removes symbol table | Build settings; lose backtraces |
| `OTHER_LDFLAGS += -ld_classic` | Old linker (legacy fallback) | Avoid unless ld64-bug workaround |
| `ENABLE_USER_SCRIPT_SANDBOXING = YES` | Tightens scripts | Hygiene, not perf |
| Static vs dynamic framework | Static: 1 load, larger binary. Dynamic: smaller binary, slower launch | `MACH_O_TYPE = staticlib` or build the dep as static via SwiftPM |
| `xcrun size -m App.app/App` | Per-segment size view | Pre-ship audit |
**Static framework win**: dynamic frameworks add a `dlopen` per startup. iOS app launch perf studies show 30–80ms per dynamic framework on cold launch. If a framework is used in your app only (not shared), build it static.
**Dead-code stripping** doesn't strip generic code that *might* be specialized — if you `@inlinable` a generic without it being used, the linker often retains the body. Audit via `nm -gU App.app/App | grep <expected-strip>`.
---
## 14. Server-side Swift (Vapor / Hummingbird) perf
- NIO / Channel: SwiftNIO `EventLoopGroup` size = physical cores (not logical) for CPU-bound.
- Connection pool: PostgresNIO / RediStack pool sizing via `maxConnections` — measure under load.
- JSON: `JSONDecoder` reuse (per-actor or per-channel).
- Memory: Linux server Swift uses glibc allocator by default; switching to `mimalloc` via `LD_PRELOAD` can win 5–15% on alloc-heavy workloads.
---
## 15. Anti-pattern table (top signals during review)
| Anti-pattern | Fix |
|--------------|-----|
| `JSONDecoder()` constructed per call | Static / per-actor shared decoder |
| `Date()` in hot loop for telemetry | `ContinuousClock.now`, captured once per batch |
| `String` concat with `+` chain | Single interpolation or `reserveCapacity` + `+=` |
| `Array<NSObject>` in hot path | `ContiguousArray` or unsafe buffer pointer |
| `for x in arr` with bounds-checked `subscript` | `withUnsafeBufferPointer` for arithmetic loops |
| Missing `autoreleasepool` around Foundation loops | Wrap iteration body |
| `lazy var` of a heavy struct read concurrently | Make eager, or wrap in actor |
| `Codable` with `userInfo` mutated per call | Reset / reuse pattern, or fresh decoder if state is real |
| `DateFormatter` constructed per format | Static `ISO8601DateFormatter` |
| `NSRegularExpression` constructed per match | Static `let pattern = try! NSRegularExpression(...)` |
| `@Published` for large structs | `@Observable` macro (Swift 5.9+) |
| Excessive `@MainActor` annotations | Confines work to main; opposite of perf intent — see [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding) |
---
## 16. Bolt-specific routing rules
1. **Demand an Instruments trace.** Without a Time Profiler / Allocations / Hangs trace, the first action is to capture one.
2. **OSSignposter > print > XCTest.measure for production marking.** Cheap and compiles out.
3. **ARC traffic before unsafe.** A `final class` + `unowned` + autoreleasepool placement covers 70% of Swift perf complaints.
4. **JSON / Date / Regex / Formatter reuse is free perf.** Cheapest possible 5-minute win.
5. **SwiftUI perf** = defer to native skill.
6. **Embedded Swift** = different rule set; verify its configured constraints through the [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding).
7. **No fix without a measurement.** Every recommendation Bolt sends to Builder should include the expected delta and the Instruments template that will confirm it.
---
## Sources
- WWDC — "Discover concurrency in SwiftUI", "Demystify Swift performance", "Explore Swift performance"
- Swift Performance Manual — https://developer.apple.com/documentation/xcode/improving-your-app-s-performance
- Swift ARC Calls instrument — Xcode 14+ Instruments template
- `OSSignposter` reference — https://developer.apple.com/documentation/os/ossignposter
- `ContinuousClock` — https://developer.apple.com/documentation/swift/continuousclock
- Embedded Swift roadmap — https://github.com/apple/swift/blob/main/docs/EmbeddedSwift/EmbeddedSwiftStatus.md
- SE-0388 — Convenience Async[Throwing]Stream.makeStream
- General semantics and version-sensitive claims: [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
