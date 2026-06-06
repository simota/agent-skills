# Swift Performance Cheatsheet (Bolt)

Agent-specific slice for **Bolt** (frontend + backend performance optimization). Baseline assumes Swift 6.2+ / Xcode 26 (as of 2026-05).

This file does **not** duplicate the source of truth. Read it alongside:

- [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md) — full API guidelines, concurrency, value-type discipline, frameworks
- [`builder/reference/swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md) — full anti-pattern catalogue (force unwrap, retain cycles, ARC mistakes, perf footguns)
- [`builder/reference/swift-language-spec.md`](../../builder/reference/swift-language-spec.md) — Swift 6.2 strict concurrency, isolation regions, Embedded Swift constraints

The role of this cheatsheet: **decide what to measure with Instruments, when an optimization is worth the trade, and how to interpret Swift-specific signals (ARC, COW, generic specialization, autoreleasepool) before reaching for code changes**.

---

## 1. Profiler decision tree (Instruments + os_signpost)

```
What slowed down?
├── Wall-clock CPU
│   ├── App launch / cold start    → Instruments: App Launch template
│   ├── Hot loop / scrolling jank  → Instruments: Time Profiler (sample @ 1ms)
│   ├── Server-side (Linux)        → perf record + samply, or `swift-collections-benchmark`
│   └── Continuous in production   → MetricKit (iOS) / OSLog signposts + Instruments diff
├── Memory growth / leaks
│   ├── "Where do allocs happen?"   → Instruments: Allocations + Mark Generation
│   ├── "Did anything leak?"        → Instruments: Leaks (Mach-O symbolicated)
│   ├── Strong reference cycles     → Instruments: Cycles (Memory Graph Debugger)
│   └── VM growth, dirty pages      → Instruments: VM Tracker
├── Concurrency
│   ├── Main-thread stalls          → Instruments: Hangs (catches >250ms blocks)
│   ├── Actor contention            → Instruments: Swift Concurrency template
│   ├── Task scheduling             → Same — visualize task lifetimes
│   └── DispatchQueue saturation    → Instruments: System Trace + Counters
├── Energy / battery
│   └── Instruments: Energy Log + MetricKit MXEnergyMetric
├── Network
│   └── Instruments: Network + URLSession metrics (`taskMetrics`)
└── Binary size / launch
    ├── Per-section breakdown       → Instruments: App Launch + linker map
    └── DEAD_CODE_STRIPPING audit   → `xcrun size -m`, `bloaty` on the Mach-O
```

**Rule**: profile first, hypothesize second, change code third. Almost every "I'm sure it's X" intuition about Swift hot paths is wrong by ≥30%, and Swift's ARC + generic specialization make it especially counter-intuitive.

### 1.1 OSSignposter — the right way to mark intervals

```swift
import os

let signposter = OSSignposter(subsystem: "com.app.render", category: "frame")

func renderFrame() {
    let state = signposter.beginInterval("render", id: signposter.makeSignpostID())
    defer { signposter.endInterval("render", state) }
    // ... work
}
```

Open Instruments → os_signpost template → see your intervals correlated with Time Profiler samples and System Trace. This is the cheapest, lowest-overhead way to mark hot paths in production builds (signposts compile out under `OS_LOG_DISABLED`).

The legacy `os_signpost` C API still works but `OSSignposter` (Swift wrapper, iOS 15+ / macOS 12+) is the modern entry point.

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

PGO status: Swift compiler has experimental Profile-Guided Optimization (`-profile-generate` / `-profile-use`) but it is **not** production-stable for Apple-platform shipping apps as of 2026-05. Server-side Swift on Linux can benefit, but the toolchain is rougher than Rust's `cargo pgo`. Track [SE roadmap](https://github.com/swiftlang/swift/blob/main/docs/OptimizerDesign.md) for updates.

---

## 3. Cross-module inlining: `@inlinable` + `@usableFromInline`

By default, public Swift functions are *not* inlined across module boundaries — the optimizer cannot see the body. For a hot library function:

```swift
@inlinable
public func hotMath(_ x: Int) -> Int {
    helper(x) &* 31  // must call public or @usableFromInline things only
}

@usableFromInline
internal func helper(_ x: Int) -> Int { x + 7 }
```

**Trade-offs**:

- Body becomes part of the ABI surface — changing it after shipping is technically a breaking change.
- Speeds up cross-module hot paths by 2–10x for tiny functions that would otherwise be a call+ARC.
- Adds compile time for callers.

**When to use**: small (< 10 LOC) cross-module hot functions, mostly in standard-library-style internal frameworks. Not for app code (which is one module).

See [best-practices §5 — Generics + protocol-oriented design](../../builder/reference/swift-best-practices.md) for the generic specialization pipeline.

---

## 4. Copy-On-Write (COW) tuning

`Array`, `String`, `Dictionary`, `Set`, `Data` all use COW. Mutation triggers a copy iff `isUniquelyReferenced(&buffer)` returns false.

### 4.1 Common COW pitfalls

| Anti-pattern | Why it bites | Fix |
|--------------|-------------|-----|
| Passing `Array` to a closure that holds another reference, then mutating | Mutation triggers copy on every call | Use `inout`, or `withContiguousMutableStorageIfAvailable` |
| `var arr = self.field; arr.append(x); self.field = arr` | Two refs alive at append → copy | Mutate in place: `self.field.append(x)` |
| `lazy var` holding an `Array` whose backing is read elsewhere | Lazy backing + reads = multiple refs | Use a private stored property |
| `for x in array.indices { array[x] = ... }` on a struct-stored array shared via property | Same | Mutate via `withUnsafeMutableBufferPointer` |

### 4.2 `reserveCapacity` for growable collections

```swift
var result = [Int]()
result.reserveCapacity(expectedCount)   // single alloc
for x in input { result.append(transform(x)) }
```

Without `reserveCapacity`, `Array` grows geometrically (doubles), incurring `O(log N)` reallocations on cold paths.

### 4.3 `ContiguousArray<T>` over `Array<T>` for value types

`Array<T>` bridges to `NSArray`, which means for `T: AnyObject` it can hold an `__SwiftDeferredNSArray` indirection. `ContiguousArray<T>` skips the bridge entirely:

```swift
var pixels = ContiguousArray<UInt8>(repeating: 0, count: 4 * width * height)
```

Use when:

- You know the element type is a Swift value type or class that does **not** need ObjC interop.
- Hot loop where you want the simplest possible memory layout.
- You're going to call `withContiguousStorageIfAvailable` / `withUnsafeBufferPointer` anyway.

---

## 5. Unsafe buffer pointers in hot loops

```swift
extension Array where Element: AdditiveArithmetic {
    func fastSum() -> Element {
        self.withUnsafeBufferPointer { buf in
            var s = Element.zero
            for i in 0..<buf.count { s += buf[i] }
            return s
        }
    }
}
```

Why this is faster: `subscript(_:)` on `Array` does a bounds check + COW uniqueness check per access. `UnsafeBufferPointer` is just pointer arithmetic; the bounds check happens once (when constructing the slice).

**Auto-vectorization** in Swift requires:

- Flat `for i in 0..<n` loop shape (not `forEach`, not `for x in collection`).
- No early `return` / `break` in the loop body.
- Element type matches a vector lane (`Float`, `Double`, fixed-width `Int`).
- `-O` enabled.

Inspect the resulting assembly with `swiftc -emit-assembly -O foo.swift | grep movaps` (look for SSE/NEON instructions).

---

## 6. ARC + autoreleasepool placement

Swift's ARC inserts `bond`/`release` calls around reference-type values. For `Foundation` types in tight loops, autoreleased objects (`NSString`, `NSData`, `Date`, `DateFormatter`) accumulate in the **outer** autorelease pool until the run loop tick.

### 6.1 The autoreleasepool fix

```swift
for url in manyURLs {
    autoreleasepool {
        let data = try Data(contentsOf: url)
        process(data)
    }
}
```

Without the inner pool, `Data(contentsOf:)` builds up `NSConcreteData` instances that are released only at the next runloop iteration — peak RSS spikes proportional to `manyURLs.count`.

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

Inspect ARC traffic via Instruments → "Swift ARC Calls" instrument (Xcode 14+).

---

## 7. `JSONDecoder` reuse (heavyweight init)

`JSONDecoder()` and `JSONEncoder()` are surprisingly expensive to construct — they allocate userInfo, key strategies, date strategies, and an internal `_JSONDecoder` graph.

```swift
// Anti-pattern: per-request decoder
func decode<T: Decodable>(_ data: Data) -> T {
    JSONDecoder().decode(T.self, from: data)    // alloc on every call
}

// Better
private let sharedDecoder: JSONDecoder = {
    let d = JSONDecoder()
    d.keyDecodingStrategy = .convertFromSnakeCase
    d.dateDecodingStrategy = .iso8601
    return d
}()
```

For server-side / batch use, a per-thread or per-actor decoder is fine — `JSONDecoder` is `Sendable`-safe when not mutated. Profile says: 30–60% of decode time on hot endpoints comes from decoder construction, not parsing.

Equivalent applies to `ISO8601DateFormatter`, `NumberFormatter`, `DateFormatter`, `RegularExpression` (`NSRegularExpression`), and `XMLParser` / `Scanner`.

---

## 8. `Date()` and clock allocations

`Date()` calls `gettimeofday` (or `CFAbsoluteTimeGetCurrent`) plus allocates a struct. In a hot loop:

```swift
// Anti-pattern: timestamp every iteration
for event in events {
    log("event at \(Date())")
}

// Better: capture once per batch
let now = Date()
for event in events { log("event at \(now)") }

// Best (perf-critical telemetry): monotonic clock
let t0 = ContinuousClock.now
for event in events { /* ... */ }
let elapsed = ContinuousClock.now - t0
```

`ContinuousClock` and `SuspendingClock` (Swift 5.7+) avoid the `Date` struct and use monotonic time — both faster and immune to wall-clock jumps.

---

## 9. String performance

### 9.1 `reserveCapacity` for builders

```swift
var sql = ""
sql.reserveCapacity(estimatedSize)
sql += "SELECT "
for col in columns { sql += col; sql += ", " }
```

Without `reserveCapacity`, the underlying `_StringStorage` reallocates as the string grows.

### 9.2 Avoid `+` concat chains

```swift
// Bad: each + allocates a new String
let s = a + b + c + d

// Better: single alloc
let s = "\(a)\(b)\(c)\(d)"

// Best for builder loops
var s = String(); s.reserveCapacity(estimate)
s += a; s += b; s += c; s += d
```

String interpolation has been optimized in Swift 5.5+ to emit a single `String.init(stringInterpolation:)` with a `StringInterpolation` buffer that pre-sizes.

### 9.3 Zero-copy construction with `unsafeUninitializedCapacity`

```swift
let s = String(unsafeUninitializedCapacity: 16) { buffer in
    // Fill buffer in-place; return actual count
    return fillBuffer(buffer)
}
```

For numeric → string conversions, UUID formatting, or fixed-format codes, this avoids the intermediate `Array<UInt8>` + copy that `String(decoding:as:)` does.

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

Apple deprecating `@Published` → `@Observable` macro (Swift 5.9+) — the per-property observation overhead dropped ~5x.

---

## 11. SwiftUI performance — defer to native skill

SwiftUI rendering cost (body re-evaluation, dependency tracking, diff, render) is a deep topic owned by the **native** skill. Key cross-cutting signals Bolt watches for:

- `@State` of large struct → entire view tree re-evaluates on any field change → split state.
- `ForEach` without stable `id:` → diff is O(n²).
- Implicit `AnyView` wrapping in conditional content → defeats compile-time type optimization.
- `.task { }` modifier inside `.id(...)`-changing parents → task re-runs unexpectedly.

For SwiftUI-specific perf advice, route to native. Bolt's role is profiler interpretation, not SwiftUI architecture.

---

## 12. Embedded Swift (`-Osize`) constraints

Embedded Swift (Swift 6+ feature for microcontrollers / kernel / no_stdlib targets):

- No reflection (`Mirror`), no existential containers (`Any`), no class hierarchies with dynamic dispatch unless `final`.
- Compiled with `-Osize` always.
- Generic specialization is mandatory (no runtime generic dispatch).
- `String` is opt-in; default is `StaticString`.
- No exception handling (`try?`/`throws` work; `try!` panics).

**Bolt's role for embedded**: confirm the stdlib subset cost is understood. A `print(...)` call drags in `String` machinery; replace with `swift_log_println_static` or platform-specific output.

See [language-spec §10 — Embedded Swift](../../builder/reference/swift-language-spec.md) for the constraint list.

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

For server-side workloads, defer to:

- NIO / Channel: SwiftNIO `EventLoopGroup` size = physical cores (not logical) for CPU-bound.
- Connection pool: PostgresNIO / RediStack pool sizing via `maxConnections` — measure under load.
- JSON: `JSONDecoder` reuse (per-actor or per-channel).
- Memory: Linux server Swift uses glibc allocator by default; switching to `mimalloc` via `LD_PRELOAD` can win 5–15% on alloc-heavy workloads.

PGO: server-side Swift on Linux can experiment with `-profile-generate` / `-profile-use` since the Xcode toolchain isn't involved. Still rougher than Rust.

See [best-practices §8](../../builder/reference/swift-best-practices.md) for the server-side crate matrix.

---

## 15. Anti-pattern table (top signals during review)

See [`swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md) for the full catalogue.

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
| Excessive `@MainActor` annotations | Confines work to main; opposite of perf intent — see [anti-patterns §3](../../builder/reference/swift-anti-patterns.md) |

---

## 16. Bolt-specific routing rules

When Bolt is reviewing a Swift performance complaint, in order:

1. **Demand an Instruments trace.** Without a Time Profiler / Allocations / Hangs trace, the first action is to capture one.
2. **OSSignposter > print > XCTest.measure for production marking.** Cheap and compiles out.
3. **ARC traffic before unsafe.** A `final class` + `unowned` + autoreleasepool placement covers 70% of Swift perf complaints.
4. **JSON / Date / Regex / Formatter reuse is free perf.** Cheapest possible 5-minute win.
5. **SwiftUI perf** = defer to native skill.
6. **Embedded Swift** = different rule set; defer to language-spec §10.
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
- Source of truth: [`builder/reference/swift-best-practices.md`](../../builder/reference/swift-best-practices.md), [`swift-anti-patterns.md`](../../builder/reference/swift-anti-patterns.md), [`swift-language-spec.md`](../../builder/reference/swift-language-spec.md)
