# Rust Performance Cheatsheet (Bolt)
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## 1. Profiler decision tree
**Rule**: profile first, hypothesize second, change code third. Almost every "I'm sure it's X" intuition about hot paths is wrong by ≥30%.
---
## 2. Allocator selection table
| Workload signal | Allocator | One-line install |
|-----------------|-----------|------------------|
| Default starting point in 2026 | `mimalloc` | `#[global_allocator] static A: MiMalloc = MiMalloc;` |
| Heavy long-lived alloc churn, lots of cores | `tikv-jemallocator` | `#[global_allocator] static A: Jemalloc = Jemalloc;` |
| Contention-heavy multi-thread server | `snmalloc-rs` | `#[global_allocator] static A: SnMalloc = SnMalloc;` |
| Embedded / WASM / size-critical | keep system, or `wee_alloc` (WASM) | — |
**Measurement protocol**: switch one allocator, re-run the same `criterion` / `divan` bench, compare. Don't switch based on internet folklore — workloads differ.
---
## 3. SIMD decision
| Goal | Recommendation (2026) |
|------|----------------------|
| Stable portable SIMD now | `wide` crate |
| Tight x86/ARM intrinsics | `std::arch::x86_64` + `is_x86_feature_detected!` runtime gating |
| Future-proof (RFC 2366 tracking) | Mark TODO; migrate to `std::simd` when stabilized |
| Easiest auto-vectorization wins | `#[inline(always)]` on hot inner loop + flat `for i in 0..n` loop shape (no early-exit) |
| Legacy | Do **not** add `packed_simd` to new code (unmaintained) |
- Keep loop bodies branch-free (use `if-else → arithmetic`).
- Bound the iteration count visibly to LLVM (`for i in 0..N` where `N` is a const, or `chunks_exact(4)`).
- Avoid floating-point reductions unless `-ffast-math` is acceptable (it usually isn't — silent precision loss).
---
## 5. Build Profile Choices
- **5.1 Production binary — max speed**
- **5.2 Production binary with backtraces**
- **5.3 Day-to-day "release-ish" (90% of the win, 50% of the build cost)**
- **5.4 Size-critical (CLI, WASM, embedded)**
---
## 6. PGO + BOLT — when worth the build complexity
| Codebase signal | Use PGO? | Use BOLT? |
|-----------------|---------|-----------|
| CPU-bound long-running server | YES — 10–20% typical | YES — adds 5–15% on top |
| Short-lived CLI | Usually not — instrumentation cost > runtime |  No |
| Crypto / hashing inner loop | YES — branch predictor benefits compound | YES |
| Mostly I/O bound | Skip — won't move the needle | Skip |
| You don't have a representative workload | **Don't bother.** Bad profile data is worse than none | **Don't bother.** |
---
## 9. Async perf — Tokio-specific signals
### 9.1 Runtime flavor
| Use case | Flavor | Why |
|----------|--------|-----|
| HTTP / DB / network service | `tokio::main(flavor = "multi_thread")` | Default; work-stealing across cores |
| CLI / single-threaded glue | `tokio::main(flavor = "current_thread")` | Lower scheduler overhead, no work-steal cost |
| Per-core sharding | Spawn one `current_thread` runtime per worker, pin via `core_affinity` | Specialized — use only after measurement |
| Embedded / WASM | `smol` or `embassy` (not Tokio) | Tokio drags too much in |
### 9.2 Worker thread count
- Default: `num_cpus::get()` (= logical cores).
- DB-heavy services: drop to physical cores (hyperthreading hurts under DB contention).
- Tune via `tokio::runtime::Builder::worker_threads(N)` + measure with `tokio-console`.
### 9.3 `spawn_blocking` discipline
- Use for CPU-bound work that would block a worker for > ~10 µs.
- Default pool size: 512 threads. Cap with `max_blocking_threads(N)` if you genuinely care.
- **Wrong use**: holding any tokio sync primitive (`Mutex`, `Notify`) inside a `spawn_blocking` body — defeats the purpose.
### 9.4 Contention diagnosis
| Signal | Tool | Action |
|--------|------|--------|
| Tasks waking but not progressing | `tokio-console` "busy" column | Look for lock contention or shared `Arc<Mutex<>>` |
| One worker hot, others idle | `samply` | Likely a `current_thread` mismatch or pinned future |
| Latency spikes correlated with GC pauses | (Rust has no GC) → check allocator | Try mimalloc / jemalloc |
| Task starvation | `tokio-metrics::TaskMonitor` | Look for `poll_count_histogram` outliers — long polls |
**Cancellation safety** is a perf concern too: a future cancelled mid-state-change may force a retry, doubling the cost of every cancellation.
---
## 10. Benchmark methodology
| Tool | When |
|------|------|
| `criterion` | Default — statistical regression detection, HTML reports, established |
| `divan` | Modern (2024+) — lower overhead, better small-fn measurement, faster CI runs |
| `iai-callgrind` | Deterministic instruction-count benchmarks (no noise from sibling load) |
| End-to-end load (`drill`, `wrk`, `vegeta`) | Always — micro can lie. Validate micro wins at the service level |
**Microbench fallacies**:
- Optimizing a function the caller never invokes on the hot path.
- Black-boxing input that the compiler proves constant → measuring constant folding.
- Single-thread bench of a primitive used multi-threaded in prod.
- Forgetting `divan::black_box` / `criterion::black_box` around inputs and outputs.
**Decision rule**: if a micro-bench shows a 20% win, the end-to-end service better show ≥ 5% — otherwise the hot path is elsewhere.
---
## 11. Compile-time performance (separate axis)
| Lever | Effect | Cost |
|-------|--------|------|
| `cargo build --timings` | HTML view of per-crate build time | Zero — always run before optimizing |
| `[workspace.dependencies]` pinning | Saves duplicate version-bump rebuild storms | Zero |
| `sccache` | Distributed compile cache | Setup; pays for itself on CI |
| `mold` linker (Linux) | 5–10× faster final link | `RUSTFLAGS="-C link-arg=-fuse-ld=mold"` |
| `cargo-chef` (Docker) | Layer-cache deps separately from app code | Slightly more complex Dockerfile |
| `[profile.dev] opt-level = 1` | Fixes slow `regex` / `num-bigint` in debug | Slightly slower dev compile |
| `dyn Trait` instead of generics on internal APIs | Cuts monomorphization → smaller binary, faster compile | Vtable dispatch cost (usually negligible off hot path) |
---
## 12. Bolt-specific routing rules
1. **Demand a profile.** If the user has no flamegraph / samply / tokio-console output, the first action is to capture one.
2. **Allocator before unsafe.** A `mimalloc` swap is one line. SIMD is a week.
3. **Anti-pattern table (§8) is the first 5-minute pass.** Most "slow Rust" is a `Vec::insert(0)` or a `clone()` in a loop.
4. **Async slowness ≠ CPU slowness.** Don't reach for `rayon` when the issue is a blocked Tokio worker — see §9.
5. **Compile-time is a separate concern.** Don't conflate "slow build" with "slow runtime".
6. **No fix without a measurement.** Every recommendation Bolt sends to Builder should include the expected delta and the benchmark that will confirm it.
---
## Sources
- The Rust Performance Book — https://nnethercote.github.io/perf-book/
- samply — https://github.com/mstange/samply
- tokio-console — https://github.com/tokio-rs/console
- cargo flamegraph — https://github.com/flamegraph-rs/flamegraph
- cargo-pgo — https://github.com/Kobzol/cargo-pgo
- llvm-bolt — https://github.com/llvm/llvm-project/tree/main/bolt
- criterion.rs — https://github.com/bheisler/criterion.rs
- divan — https://github.com/nvzqz/divan
- mimalloc-rs / tikv-jemallocator / snmalloc-rs (crates.io)
- mold linker — https://github.com/rui314/mold
- cargo-bloat — https://github.com/RazrFalcon/cargo-bloat
- Rust API Guidelines — https://rust-lang.github.io/api-guidelines/checklist.html
- General semantics and version-sensitive claims: [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
