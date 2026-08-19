# Kotlin Performance Cheatsheet (Bolt)
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## 1. Profiler decision tree (JVM + Kotlin)
**Rule**: profile first, hypothesize second, change code third. Kotlin compiles to JVM bytecode, so JVM profilers apply unchanged — but Kotlin-specific signals (inline lambdas, boxing, suspending state machines) need Kotlin-aware interpretation.
- **1.1 async-profiler — the workhorse**
- **1.2 JFR (Java Flight Recorder)**
- **1.3 IntelliJ Profiler**
---
## 2. kotlinx-benchmark — the right JMH harness
**Required**:
- `@Warmup` ≥ 5 iterations (JIT warms up after ~10k invocations).
- `@Fork` ≥ 2 (eliminates JVM-state-dependent noise).
- `Blackhole.consume(...)` (otherwise JIT removes the dead computation).
- `@Param` for sweeping N — small N is dominated by setup cost.
---
## 3. Sequence vs List — the 2025–2026 reality
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
---
## 8. JIT warmup + benchmark semantics
1. Interpreted (slow, but cheap to invoke)
2. C1 (quick JIT, lower optimization)
3. C2 (full JIT, ~10k invocations before triggers)
**Implication for perf measurement**:
- First N invocations of a function run interpreted, then C1, then C2.
- The same code can be 20x faster after warmup.
- A benchmark without `@Warmup` measures interpreted/C1 — irrelevant for production.
- One-shot CLI / batch jobs may run mostly interpreted → AOT / CDS matters.
- `-XX:+PrintCompilation` to see compile decisions.
- JITWatch GUI to visualize compile log.
- `-XX:CompileThreshold=N` to lower the C2 trigger (for benchmarks only).
---
## 10. Project Loom — virtual threads vs `Dispatchers.IO`
| Approach | Cost per blocked op | When |
|----------|---------------------|------|
| `Dispatchers.IO` (default 64 threads, expandable to 1024) | OS thread + context switch | Existing kotlinx.coroutines code |
| Virtual thread executor (`Executors.newVirtualThreadPerTaskExecutor()`) | ~few KB; no OS thread | New blocking-IO services |
| `Dispatchers.IO.limitedParallelism(N)` | Same as `Dispatchers.IO` | Bounding concurrent IO |
**However**: virtual threads do not help CPU-bound work. And `synchronized` blocks in virtual threads still pin to the OS carrier thread (will be fixed in JDK 23+).
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
**Implication**: `launch` per item in a hot loop is expensive. Batch with `flow`, `chunked`, or `parMap`.
---
## 12. Flow operator costs
- The terminal collector (`collect`, `toList`, `first`).
- Buffer operators (`buffer(n)`, `conflate`, `flowOn(dispatcher)`).
- Concurrency operators (`flatMapMerge`, `combine`, `zip`).
**Common Flow perf footguns**:
- `flatMapMerge(concurrency = Int.MAX_VALUE)` — unbounded parallelism crashes.
- `buffer()` without thought — adds latency floor for hot paths.
- `flowOn` repeated mid-chain — multiple dispatcher hops, each 500ns+.
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
---
## 15. Kotlin/Native (KMP) perf
- LLVM-backed; no JIT, no warm-up.
- No GC pauses to tune; the new K/Native memory manager (since 1.7.20) is concurrent mark-sweep with sub-ms pauses on most workloads.
- No `inline fun` warm-up advantage — already compiled.
- Sequence vs List benchmarks differ — measure on the actual target.
---
## 16. Anti-pattern table (top signals during review)
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
1. **Demand a profile.** Without async-profiler / JFR / IntelliJ Profiler, the first action is to capture one.
2. **JIT warmup discipline.** A benchmark without `@Warmup` is folklore. Reject perf claims from unwarmed numbers.
3. **Boxing audit first.** `List<Int>`, `Pair<Int,Int>`, nullable primitives — cheapest 5-minute wins.
4. **Loom > new threads** for blocking-IO services on JDK 21+. Use virtual-thread executor as `CoroutineDispatcher`.
5. **GC choice is a knob, not a panacea.** ZGC for tail latency, G1 for default. Don't switch without JFR pause histogram.
6. **Compose UI perf** = defer to native skill.
7. **K/Native perf** = different rule set; verify the configured target and runtime through the [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding).
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
- General semantics and version-sensitive claims: [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
