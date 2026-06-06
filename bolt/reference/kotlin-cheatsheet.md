# Kotlin Performance Cheatsheet (Bolt)

Agent-specific slice for **Bolt** (frontend + backend performance optimization). Baseline assumes Kotlin 2.3+ / K2 compiler (as of 2026-05).

This file does **not** duplicate the source of truth. Read it alongside:

- [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md) — full Kotlin Style Guide, coroutines, Flow patterns, JVM interop
- [`builder/reference/kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md) — full anti-pattern catalogue (boxing, leaks, blocking IO, GlobalScope)
- [`builder/reference/kotlin-language-spec.md`](../../builder/reference/kotlin-language-spec.md) — Kotlin 2.x semantics, K2 compiler, KMP, JVM target, K/Native

The role of this cheatsheet: **interpret JVM profiling signals (JFR, async-profiler, JMH) for Kotlin code, distinguish Kotlin-language perf from JVM-runtime perf, and pick the right benchmark harness before changing code**.

---

## 1. Profiler decision tree (JVM + Kotlin)

```
What slowed down?
├── Wall-clock CPU
│   ├── Linux/macOS prod         → async-profiler (CPU mode) + flamegraph
│   ├── Local dev box             → IntelliJ Profiler (JFR-based, GUI)
│   ├── Microbench               → kotlinx-benchmark (JMH harness)
│   └── Method-level hotspot     → JFR ExecutionSample
├── Allocation pressure / GC
│   ├── "What allocates the most?" → async-profiler --alloc + flamegraph
│   ├── GC pause breakdown        → JFR GarbageCollection events
│   ├── Heap shape / retained     → JFR -> jconsole, or jcmd heapdump + Eclipse MAT
│   └── TLAB churn                → JFR ObjectAllocationInNewTLAB
├── Coroutines
│   ├── "Why is my flow slow?"    → kotlinx.coroutines.debug DebugProbes
│   ├── Suspending state          → JFR thread states, or async-profiler --threads
│   └── Channel backpressure     → metrics on send/receive durations
├── Locks / contention
│   └── JFR JavaMonitorWait + JavaMonitorEnter
├── I/O
│   └── JFR FileRead/FileWrite/SocketRead/SocketWrite
├── Compile (warm-up) overhead
│   └── -XX:+PrintCompilation, JITWatch
└── Startup
    └── JFR (recordOnStart) + -Xlog:class+load, AppCDS profile
```

**Rule**: profile first, hypothesize second, change code third. Kotlin compiles to JVM bytecode, so JVM profilers apply unchanged — but Kotlin-specific signals (inline lambdas, boxing, suspending state machines) need Kotlin-aware interpretation.

### 1.1 async-profiler — the workhorse

```bash
# CPU profile, 30s
asprof -d 30 -f cpu.html -e cpu --jfr=cpu.jfr <pid>

# Allocation profile (samples object allocations)
asprof -d 30 -f alloc.html -e alloc <pid>

# Lock contention
asprof -d 30 -f lock.html -e lock <pid>
```

async-profiler does **stackwalking that includes inlined JIT frames** — Java/JVM-native profilers often hide inlined Kotlin lambdas. For Kotlin, this matters: a `forEach { }` whose body is JIT-inlined disappears from non-async-profiler views.

### 1.2 JFR (Java Flight Recorder)

Built into the JVM, free, low overhead (~1%). Continuous mode for production:

```
-XX:StartFlightRecording=filename=app.jfr,maxage=4h,settings=profile
```

Open in JDK Mission Control (JMC). Best for: GC, lock contention, IO breakdown, allocation hot classes.

### 1.3 IntelliJ Profiler

Sits on JFR + async-profiler. Best ergonomics for dev-time profiling. Cannot run in CI.

---

## 2. kotlinx-benchmark — the right JMH harness

JMH (Java Microbenchmark Harness) handles warm-up, fork isolation, blackhole consumption — all critical for measuring Kotlin code correctly.

```kotlin
@State(Scope.Benchmark)
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.NANOSECONDS)
@Warmup(iterations = 5, time = 1)
@Measurement(iterations = 10, time = 1)
@Fork(value = 2, jvmArgs = ["-Xms2G", "-Xmx2G"])
class MyBench {
    @Param("100", "10000")
    var n: Int = 0

    @Setup fun setup() { /* ... */ }

    @Benchmark fun listApproach(bh: Blackhole) {
        bh.consume(items.filter { it > 0 }.map { it * 2 })
    }

    @Benchmark fun sequenceApproach(bh: Blackhole) {
        bh.consume(items.asSequence().filter { it > 0 }.map { it * 2 }.toList())
    }
}
```

**Required**:

- `@Warmup` ≥ 5 iterations (JIT warms up after ~10k invocations).
- `@Fork` ≥ 2 (eliminates JVM-state-dependent noise).
- `Blackhole.consume(...)` (otherwise JIT removes the dead computation).
- `@Param` for sweeping N — small N is dominated by setup cost.

Without these, a microbench can be off by 100x or measure the JIT decision rather than the code.

See [best-practices §6](../../builder/reference/kotlin-best-practices.md) for full performance section.

---

## 3. Sequence vs List — the 2025–2026 reality

Folklore: "Sequence is lazy, therefore faster". Reality (measured on Kotlin 2.x + JDK 21):

| Workload | Winner | Why |
|----------|--------|-----|
| `list.map { }.filter { }.sum()`, N=1000 | **List** (1.3–2x) | Lambda devirtualization, eager arrays cache-friendly |
| Same chain, N=1,000,000 | **List** or tie | Allocation overhead amortized; JIT specializes the chain |
| 5+ ops, large N, early termination via `first { }` / `take(N)` | **Sequence** | Avoids materializing intermediate collections |
| Sequence inside a hot per-frame loop | **Inline `for`** | Both lose to a plain loop |

**Rule**:

- Don't reach for `asSequence()` without measurement.
- 2–3 op chains on List are usually fastest.
- Sequence wins on early termination over huge N, or 5+ chained ops on millions.

This is a JVM/JIT artifact — on Kotlin/Native the picture differs.

See [`kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md) for the "lazy is free" anti-pattern.

---

## 4. Inline higher-order functions (`inline fun`)

Kotlin lambdas compile to `Function0/1/...` instances *per call site* unless the function is `inline`. For high-frequency higher-order calls:

```kotlin
// inline — no Function1 alloc, no virtual call
inline fun <T> measure(block: () -> T): T {
    val start = System.nanoTime()
    val result = block()
    println("took ${System.nanoTime() - start} ns")
    return result
}
```

**When to apply `inline`**:

- Function takes a lambda AND is called frequently (hot path).
- Function is small (< 15–20 LOC bytecode-emitted).
- Crossing module boundary (lambdas can't be inlined across module without `inline`).

**When NOT**:

- Function is large — code bloat at every call site.
- Function takes a `Function*` you store somewhere (no point — must materialize).
- Function is rarely called.

`crossinline` and `noinline` modifiers control which lambdas participate in inlining. See [best-practices §3](../../builder/reference/kotlin-best-practices.md).

The JIT *may* inline non-`inline` functions if they're sufficiently hot, but `inline fun` is a **bytecode-level** guarantee — no warm-up needed.

---

## 5. Boxing — the silent perf tax

| Type | Boxes? | Cost |
|------|--------|------|
| `Int` as `Int` (typed param/local) | No | Native primitive |
| `Int` in `List<Int>` | **Yes** | Boxed to `Integer`, heap alloc per element |
| `Int` in `IntArray` | No | Native `int[]` |
| `Int?` (nullable) | **Yes** | Always boxed |
| `Pair<Int, Int>` | **Yes** (both) | Two box allocations + Pair alloc |
| `T : Number` generic | **Yes** | Generic erasure forces boxing |
| `@JvmInline value class Foo(val i: Int)` used as `Foo` | No (mostly) | Compiles to underlying `int` |
| Same value class **as parameter to a generic** | **Yes** | Boxing at the boundary |
| Same value class **in nullable position** | **Yes** | Box to distinguish null |

**Common boxing hotspots Bolt watches for**:

- `List<Int>` used as a numeric buffer → switch to `IntArray` / `LongArray`.
- `Map<Int, Int>` → `Int2IntHashMap` from Eclipse Collections / fastutil.
- Math sequences with nullable accumulator (`var sum: Int? = 0`) — every iteration boxes.
- `Pair<Int, Int>` returned from a hot function → use a `@JvmInline value class` with a `Long` encoding both ints.

Visualize boxing in async-profiler `--alloc` flamegraph — look for `Integer.valueOf` / `Long.valueOf` frames.

---

## 6. `@JvmInline value class` — zero-cost wrappers (mostly)

```kotlin
@JvmInline
value class UserId(val value: Long)

fun byId(id: UserId): User { /* compiles to: byId-XXXX(long) */ }
```

**Erasure rules** (when boxing happens):

- Used as the value class: no box.
- Used through a generic: boxed.
- Used in nullable position (`UserId?`): boxed (to distinguish null).
- Used as receiver for an interface method: boxed.
- Cross-language (Java code calling it): name-mangled, but still boxed on Java side.

For 90% of typed-ID use cases, value classes are free. The remaining 10% (generic collection of value classes, nullable in hot path) need profiling.

See [best-practices §4](../../builder/reference/kotlin-best-practices.md).

---

## 7. `lateinit` vs nullable — late-init pattern

```kotlin
// Anti-pattern in DI/Android: nullable for late init
private var component: Component? = null
fun use() { component!!.run() }   // null-check + bang every call

// Better
private lateinit var component: Component
fun use() { component.run() }     // direct access; one-time init check
```

`lateinit` skips the null-check per access. Reads compile to a direct field load with an `UninitializedPropertyAccessException` thrown if accessed before init.

**Doesn't work for**:

- Primitive types (`Int`, `Long` etc — they have a default zero).
- Properties with custom getter/setter.
- Top-level / object properties (Kotlin 1.2+ allows it; earlier versions don't).

For Compose / Coroutines code, prefer `lazy { }` or constructor injection over `lateinit` — `lateinit` is a code smell unless the framework forces it (Android Fragment.onAttach, etc.).

---

## 8. JIT warmup + benchmark semantics

JVM JIT (HotSpot C2) tiers:

1. Interpreted (slow, but cheap to invoke)
2. C1 (quick JIT, lower optimization)
3. C2 (full JIT, ~10k invocations before triggers)

**Implication for perf measurement**:

- First N invocations of a function run interpreted, then C1, then C2.
- The same code can be 20x faster after warmup.
- A benchmark without `@Warmup` measures interpreted/C1 — irrelevant for production.
- One-shot CLI / batch jobs may run mostly interpreted → AOT / CDS matters.

Tools:

- `-XX:+PrintCompilation` to see compile decisions.
- JITWatch GUI to visualize compile log.
- `-XX:CompileThreshold=N` to lower the C2 trigger (for benchmarks only).

---

## 9. GC tuning

| GC | When | Trade |
|----|------|-------|
| **G1GC** (default since JDK 9) | General-purpose, balanced | Pause goal `MaxGCPauseMillis=200` default |
| **ZGC** (production-ready JDK 21+) | Latency-critical, multi-GB heap | Sub-millisecond pauses; ~2-15% throughput cost |
| **Shenandoah** (Red Hat OpenJDK) | Same target as ZGC | Equivalent pause goals; different impl |
| **Parallel** (legacy) | Throughput-only batch | Highest throughput, longest pauses |
| **Epsilon** (no-op) | Short-lived test/CLI | Allocates until OOM; perf is allocator only |

**For long-running Kotlin servers**: ZGC is the modern default (JDK 21+). Set `-XX:+UseZGC -Xmx<heap>`. Verify via JFR pause histogram.

**For short-lived CLI / build tools**: G1 default is fine. Worry about Class Data Sharing (CDS) for startup more than GC.

### 9.1 CDS (Class Data Sharing) for startup

```bash
# Generate
java -XX:ArchiveClassesAtExit=app.jsa -jar app.jar

# Use
java -XX:SharedArchiveFile=app.jsa -jar app.jar
```

CDS reduces startup time 20–50% by sharing pre-parsed class metadata across JVM boots. Critical for CLI tools that run once per invocation (e.g., Gradle worker JVMs).

AppCDS extends this — see [best-practices §8](../../builder/reference/kotlin-best-practices.md).

---

## 10. Project Loom — virtual threads vs `Dispatchers.IO`

JDK 21+ ships virtual threads (Project Loom). For blocking IO:

| Approach | Cost per blocked op | When |
|----------|---------------------|------|
| `Dispatchers.IO` (default 64 threads, expandable to 1024) | OS thread + context switch | Existing kotlinx.coroutines code |
| Virtual thread executor (`Executors.newVirtualThreadPerTaskExecutor()`) | ~few KB; no OS thread | New blocking-IO services |
| `Dispatchers.IO.limitedParallelism(N)` | Same as `Dispatchers.IO` | Bounding concurrent IO |

2025 benchmarks: virtual threads roughly 30x faster for blocking-IO-heavy workloads (file reads, JDBC calls, blocking HTTP), because the OS thread is no longer the unit of concurrency.

**However**: virtual threads do not help CPU-bound work. And `synchronized` blocks in virtual threads still pin to the OS carrier thread (will be fixed in JDK 23+).

Bridging Loom + coroutines:

```kotlin
val loomDispatcher = Executors.newVirtualThreadPerTaskExecutor().asCoroutineDispatcher()

suspend fun work() = withContext(loomDispatcher) {
    blockingIO()   // each call gets its own virtual thread
}
```

For new server code with heavy JDBC / file IO, this is the modern path. See [best-practices §5](../../builder/reference/kotlin-best-practices.md).

---

## 11. Coroutine overhead

| Operation | Cost (approx, JIT-warm) |
|-----------|------------------------|
| `launch { ... }` | ~50–200 ns + Job alloc |
| `async { ... }.await()` | ~100–300 ns + Deferred alloc |
| `suspend` function call (no actual suspension) | ~5–20 ns (essentially zero) |
| Actual suspension + resume | ~500 ns – several µs (depends on dispatcher hop) |
| `withContext(Dispatchers.Default)` (dispatcher hop) | 500ns–1µs |
| Channel `send` / `receive` (uncontended) | ~100–200 ns |

**Implication**: `launch` per item in a hot loop is expensive. Batch with `flow`, `chunked`, or `parMap`. See [anti-patterns](../../builder/reference/kotlin-anti-patterns.md).

Structured concurrency overhead (the parent `CoroutineScope` cancellation propagation) is essentially free; the cost is in the dispatch and continuation suspension.

---

## 12. Flow operator costs

Most intermediate `Flow` operators (`map`, `filter`, `transform`) are essentially free at the call site — they wrap a single lambda. The cost is dominated by:

- The terminal collector (`collect`, `toList`, `first`).
- Buffer operators (`buffer(n)`, `conflate`, `flowOn(dispatcher)`).
- Concurrency operators (`flatMapMerge`, `combine`, `zip`).

```kotlin
flow.map { transform(it) }                    // ~free
    .filter { predicate(it) }                 // ~free
    .buffer(64)                               // allocs a Channel
    .flowOn(Dispatchers.Default)              // dispatcher switch
    .collect { emit(it) }                     // terminal, the real cost
```

**Common Flow perf footguns**:

- `flatMapMerge(concurrency = Int.MAX_VALUE)` — unbounded parallelism crashes.
- `buffer()` without thought — adds latency floor for hot paths.
- `flowOn` repeated mid-chain — multiple dispatcher hops, each 500ns+.

---

## 13. Compose UI — defer to native skill

Jetpack Compose perf (recomposition, `remember` choices, `derivedStateOf`, `stable`/`immutable` annotations, bytecode growth from the Compose compiler plugin) is owned by the **native** skill.

What Bolt watches for at a high level:

- Compose compiler produces ~2–4x more bytecode than equivalent Kotlin. Methods can exceed JIT inlining thresholds.
- `@Stable` / `@Immutable` annotations control re-composition skipping — wrong annotation = perf regression.
- `remember { }` with capturing lambda → equality issue → recomposition loop.

For Compose-specific guidance, route to native. Bolt's role is profiler interpretation, not Compose architecture.

---

## 14. Build performance

| Lever | Effect | How |
|-------|--------|-----|
| **KSP2 over kapt** | 2-5x faster annotation processing | Use `com.google.devtools.ksp` plugin instead of `kapt` |
| **Gradle config cache** | Cold builds 30-50% faster after first run | `--configuration-cache` (Gradle 8+) |
| **Parallel build** | Multi-module saturates cores | `org.gradle.parallel=true` in `gradle.properties` |
| **Build cache** | Reuses compiled outputs across machines | `org.gradle.caching=true` + remote cache server |
| **Incremental compilation** | Kotlin 2.x improved K2 incrementality | Default on; verify with `--info` |
| **K2 compiler** | 2x faster Kotlin compilation vs K1 | Default in 2.0+; verify `kotlin.experimental.tryK2=true` if older |
| **Single-file rebuild** | Avoids full module recompile | Ensure no `internal` cross-file leaks |

`kapt` is **deprecated** for new projects — migrate to KSP2 (different annotation processor model). See [best-practices §9](../../builder/reference/kotlin-best-practices.md).

---

## 15. Kotlin/Native (KMP) perf

When code targets K/Native (iOS, embedded, server-side Linux without JVM):

- LLVM-backed; no JIT, no warm-up.
- No GC pauses to tune; the new K/Native memory manager (since 1.7.20) is concurrent mark-sweep with sub-ms pauses on most workloads.
- No `inline fun` warm-up advantage — already compiled.
- Sequence vs List benchmarks differ — measure on the actual target.

K/Native perf is more comparable to Swift/Rust than to JVM Kotlin. Defer detailed K/Native tuning to [language-spec §7 — K/Native runtime](../../builder/reference/kotlin-language-spec.md).

---

## 16. Anti-pattern table (top signals during review)

See [`kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md) for the full catalogue.

| Anti-pattern | Fix |
|--------------|-----|
| `asSequence()` reflex without measurement | Default to List; measure before switching |
| `forEach { }` in inner hot loop | Plain `for` loop or `inline fun` wrapper |
| `List<Int>` for numeric buffer | `IntArray` / `LongArray` |
| `Pair<Int, Int>` in hot path | `@JvmInline value class Pos(val packed: Long)` |
| `runBlocking` in non-test code | `suspend` propagation up the call stack |
| `GlobalScope.launch` | A scoped `CoroutineScope` |
| `launch` per element in hot stream | `flow { }.chunked(N).flatMapMerge { }` |
| Synchronized blocks on virtual threads | Mutex / Semaphore (Loom-friendly primitives) |
| `Dispatchers.IO` without `limitedParallelism` for batch jobs | `Dispatchers.IO.limitedParallelism(N)` |
| `lateinit` in hot per-frame property | Constructor inject or `lazy` |
| Repeated `JsonElement` traversal | Decode to typed `@Serializable` model once |
| `kapt` in 2026 project | Migrate to KSP2 |

---

## 17. Bolt-specific routing rules

When Bolt is reviewing a Kotlin performance complaint, in order:

1. **Demand a profile.** Without async-profiler / JFR / IntelliJ Profiler, the first action is to capture one.
2. **JIT warmup discipline.** A benchmark without `@Warmup` is folklore. Reject perf claims from unwarmed numbers.
3. **Boxing audit first.** `List<Int>`, `Pair<Int,Int>`, nullable primitives — cheapest 5-minute wins.
4. **Loom > new threads** for blocking-IO services on JDK 21+. Use virtual-thread executor as `CoroutineDispatcher`.
5. **GC choice is a knob, not a panacea.** ZGC for tail latency, G1 for default. Don't switch without JFR pause histogram.
6. **Compose UI perf** = defer to native skill.
7. **K/Native perf** = different rule set; defer to language-spec §7.
8. **No fix without a measurement.** Every recommendation includes the expected delta and the JMH/profile artifact that will confirm it.

---

## Sources

- async-profiler — https://github.com/async-profiler/async-profiler
- JMH (Java Microbenchmark Harness) — https://github.com/openjdk/jmh
- kotlinx-benchmark — https://github.com/Kotlin/kotlinx-benchmark
- kotlinx.coroutines debug probes — https://github.com/Kotlin/kotlinx.coroutines/blob/master/kotlinx-coroutines-debug/README.md
- JEP 444 Virtual Threads — https://openjdk.org/jeps/444
- JEP 439 Generational ZGC — https://openjdk.org/jeps/439
- JDK Mission Control — https://www.oracle.com/java/technologies/jdk-mission-control.html
- Kotlin K2 compiler announcement — https://kotlinlang.org/docs/k2-compiler-migration-guide.html
- Kotlin Symbol Processing (KSP) — https://kotlinlang.org/docs/ksp-overview.html
- Source of truth: [`builder/reference/kotlin-best-practices.md`](../../builder/reference/kotlin-best-practices.md), [`kotlin-anti-patterns.md`](../../builder/reference/kotlin-anti-patterns.md), [`kotlin-language-spec.md`](../../builder/reference/kotlin-language-spec.md)
