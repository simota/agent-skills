# Rust Performance Cheatsheet (Bolt)

Agent-specific slice for **Bolt** (frontend + backend performance optimization). Snapshot context (not authority): Rust 1.85+ / Edition 2024 (as of 2026-05). Detect the repository toolchain before applying version-specific guidance.

This file does **not** duplicate the source of truth. Read it alongside:

- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)

The role of this cheatsheet: **decide what to measure, with which tool, and how to interpret the result before reaching for an optimization**.

---

## 1. Profiler decision tree

```
What slowed down?
├── Wall-clock CPU on a hot path
│   ├── Linux production       → perf + cargo flamegraph
│   ├── Cross-platform / 2026  → samply  (recommended default)
│   ├── macOS dev box          → cargo flamegraph (dtrace)
│   └── Long-running server    → pprof-rs (HTTP endpoint, always-on)
├── RSS climbing / OOM
│   ├── "Where do allocs happen?"  → dhat-rs (massif-like)
│   ├── "Which crate bloats?"      → cargo-bloat
│   └── Cache miss / churn         → heaptrack + perf c2c
├── Async tasks stuck / starved
│   ├── Which task is busy?        → tokio-console
│   ├── Why is runtime stalled?    → tokio-metrics + tracing spans
│   └── Worker contention          → samply + filter on tokio-runtime-worker
├── Binary size
│   └── cargo bloat --release --crates
└── Compile time
    └── cargo build --timings  +  cargo build -Z self-profile (nightly)
```

**Rule**: profile first, hypothesize second, change code third. Almost every "I'm sure it's X" intuition about hot paths is wrong by ≥30%.

---

## 2. Allocator selection table

The default glibc allocator is famously slow under multi-threaded contention. Before reaching for unsafe or SIMD, swap the allocator.

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

Auto-vectorization hints:

- Keep loop bodies branch-free (use `if-else → arithmetic`).
- Bound the iteration count visibly to LLVM (`for i in 0..N` where `N` is a const, or `chunks_exact(4)`).
- Avoid floating-point reductions unless `-ffast-math` is acceptable (it usually isn't — silent precision loss).


---

## 4. `#[inline]` policy (when it matters)

| Annotation | Apply when |
|------------|-----------|
| (none — default) | 95% of cases. Trust the compiler |
| `#[inline]` | Small (< ~10 LOC) cross-crate hot fn — without LTO, cross-crate calls are *not* inlined by default |
| `#[inline(always)]` | Profile proves LLVM left a hot fn uninlined. Document the profile evidence in a comment |
| `#[inline(never)]` | Splitting a giant fn for I-cache, or forcing a benchmark boundary |
| `#[cold]` | Error paths, slow paths, panic shims — keeps the hot path's I-cache clean |

**Interaction with LTO**: with `lto = "fat"`, `#[inline]` matters much less — the linker has the whole program. With `lto = "thin"` or `false`, cross-crate inlining still benefits from explicit hints.


---

## 5. Build-profile recipes

### 5.1 Production binary — max speed

```toml
[profile.release]
lto              = "fat"
codegen-units    = 1
panic            = "abort"
strip            = "symbols"
opt-level        = 3
```

Build time ~2-3x slower; binary 10-30% faster than default release.

### 5.2 Production binary with backtraces

```toml
[profile.release-with-debug]
inherits = "release"
debug    = "line-tables-only"   # enough for symbolicated panics + flamegraphs
strip    = "none"
```

### 5.3 Day-to-day "release-ish" (90% of the win, 50% of the build cost)

```toml
[profile.release-fast-compile]
inherits      = "release"
lto           = "thin"
codegen-units = 16
```

### 5.4 Size-critical (CLI, WASM, embedded)

```toml
[profile.release-small]
inherits  = "release"
opt-level = "z"    # or "s" for slightly faster code at small size cost
lto       = "fat"
strip     = "symbols"
panic     = "abort"
```

`opt-level = "z"` can be **slower** than `"s"` — measure. Don't blindly pick `"z"`.


---

## 6. PGO + BOLT — when worth the build complexity

| Codebase signal | Use PGO? | Use BOLT? |
|-----------------|---------|-----------|
| CPU-bound long-running server | YES — 10–20% typical | YES — adds 5–15% on top |
| Short-lived CLI | Usually not — instrumentation cost > runtime |  No |
| Crypto / hashing inner loop | YES — branch predictor benefits compound | YES |
| Mostly I/O bound | Skip — won't move the needle | Skip |
| You don't have a representative workload | **Don't bother.** Bad profile data is worse than none |

Automation: `cargo pgo` covers instrument → run → merge → rebuild. BOLT requires `llvm-bolt` (Linux ELF only) — used internally by the Rust project to optimize rustc itself.


---

## 7. Zero-copy pattern selector

| Want | Reach for | Cost / caveat |
|------|-----------|---------------|
| API that may borrow or own | `Cow<'_, str>` / `Cow<'_, [u8]>` | One enum discriminant per value |
| Cheap-clone read-only byte buffer | `bytes::Bytes` | Reference counted; standard in tokio/hyper |
| Many short-lived allocs with shared lifetime | `bumpalo::Bump` arena | Drop arena → drop all at once; can't free individually |
| Zero-copy JSON | `serde(borrow)` + `&'de str` fields | Requires `serde::Deserialize<'de>` + lifetime threading |
| In-memory layout as wire format | `rkyv` | Nano-second reads; loses serde ergonomics + needs schema discipline |
| Read-only buffer shared across tasks | `Arc<[u8]>` | One alloc, many views |


---

## 8. Hot-path anti-pattern table (top signals during review)

Numbered by anti-pattern file.

| Anti-pattern | Fix | Clippy |
|--------------|-----|--------|
| Gratuitous `.clone()` on hot path | `&T`, or `Cow<'a, T>` if sometimes owned | `clippy::redundant_clone` |
| `s + &t + &u` chain | `format!("{s}{t}{u}")` (single alloc) | `clippy::string_add` |
| `String::new()` + `push_str` in loop | `String::with_capacity(estimate)` | — |
| `Vec::insert(0, x)` | `VecDeque::push_front` (O(1)) | — |
| `Vec::remove(0)` | `VecDeque::pop_front` or `swap_remove` if order doesn't matter | — |
| `HashMap` for tiny maps (< ~16 entries) | `Vec<(K, V)>` linear scan | — |
| `Box<dyn Trait>` on hot path | Enum dispatch (`enum Op { A, B }`) | — |
| `Arc<RwLock<T>>` write-heavy | Default to `Arc<Mutex<T>>` — switch only if reads dominate 10× | — |
| Missing `#[inline]` on small cross-crate fn | `#[inline]` on small (< 10 LOC) cross-crate hot fns | — |
| Re-creating `Regex` in loop | `static RE: LazyLock<Regex> = LazyLock::new(...)` | `clippy::regex_creation_in_loops` |
| `HashMap` SipHash for trusted-input lookup | `ahash::AHashMap` or `rustc_hash::FxHashMap` | — |
| `Result<T, BigError>` (big payload) | `Result<T, Box<BigError>>` | `clippy::result_large_err` |
| `Vec::contains` for membership in large set | `HashSet` | — |

**Why this list matters for Bolt**: these are *measured* wins, not folklore. Clippy already catches most — turn the lints on (see judge's clippy policy).

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

Tokio runtime depth: [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding).

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

Benchmark crate detail: [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding).

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

`cargo bloat --release --crates` to find which dependency is 30% of your binary.


---

## 12. Bolt-specific routing rules

When Bolt is reviewing a Rust performance complaint, in order:

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
