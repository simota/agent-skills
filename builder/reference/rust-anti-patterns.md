# Rust Anti-Patterns — Deep Dive Reference

> Companion to `language-idioms.md` §4 (Rust). This file catalogs 256 anti-patterns across 14 categories — ownership, lifetimes, type system, async, error handling, performance, traits, macros, unsafe, cargo/deps, testing, security, API design, and WASM/embedded/`no_std`. Each row pairs the smell with the fix and the Clippy lint that catches it. The 40+ enforceable Clippy lints are gathered in a copy-pasteable `[lints.clippy]` block at the bottom. For the short-form idioms table and 20 baseline anti-patterns, see `language-idioms.md` lines 384-700.
>
> Baseline: Rust 1.85+ / Edition 2024 (as of 2026-05).

---

## Table of Contents

1.  [Ownership & Borrowing Pitfalls](#1-ownership--borrowing-pitfalls)
2.  [Lifetime Pitfalls](#2-lifetime-pitfalls)
3.  [Type System Pitfalls](#3-type-system-pitfalls)
4.  [Async / Await Pitfalls (Extensive)](#4-async--await-pitfalls-extensive)
5.  [Error Handling Pitfalls](#5-error-handling-pitfalls)
6.  [Performance Pitfalls](#6-performance-pitfalls)
7.  [Trait Design Pitfalls](#7-trait-design-pitfalls)
8.  [Macro Pitfalls](#8-macro-pitfalls)
9.  [Unsafe Pitfalls (High-Stakes)](#9-unsafe-pitfalls-high-stakes)
10. [Cargo / Dependency Pitfalls](#10-cargo--dependency-pitfalls)
11. [Testing Pitfalls](#11-testing-pitfalls)
12. [Security Pitfalls](#12-security-pitfalls)
13. [API Design Pitfalls](#13-api-design-pitfalls)
14. [WASM / Embedded / `no_std` Pitfalls](#14-wasm--embedded--no_std-pitfalls)
15. [Cross-Cutting Clippy Lint Quick Reference](#cross-cutting-clippy-lint-quick-reference)
16. [Sources](#sources)

> **Cross-links:**
> - Spec semantics behind each footgun (Pin, variance, UB list, atomics, FFI ABI) → [`rust-language-spec.md`](./rust-language-spec.md). The canonical UB list lives in [`rust-language-spec.md §6.2`](./rust-language-spec.md#62-canonical-undefined-behaviors-rust-reference).
> - Recommended crates / patterns to replace each anti-pattern with → [`rust-best-practices.md`](./rust-best-practices.md)
> - The 20 baseline anti-patterns (unwrap in prod, &Vec<T> params, etc.) → `language-idioms.md` §4. This file *extends* that baseline.

> **Convention in tables**: `Clippy` column references lint names as they appear in [rust-lang.github.io/rust-clippy/master/index.html](https://rust-lang.github.io/rust-clippy/master/index.html) (default level varies — `pedantic` / `restriction` must be opted in).

---

## 1. Ownership & Borrowing Pitfalls

The single largest source of new-Rust frustration. The pattern is almost always "reach for `.clone()` / `Arc<Mutex<T>>` / interior mutability when the right fix is to redesign ownership."

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 1.1 | `.clone()` to escape the borrow checker | Hides the ownership question, allocates on hot paths, makes data flow opaque to readers | Take a `&T` / `&mut T`, split borrows, restructure functions to take ownership when needed | `clippy::redundant_clone`, `clippy::clone_on_copy` |
| 1.2 | Defensive `.to_owned()` / `.to_string()` on every input | Same as above; `String` allocation on each call masks the issue | Accept `&str` / `impl AsRef<str>` / `impl Into<String>` — defer allocation to the boundary that actually needs to own | `clippy::str_to_string`, `clippy::string_to_string` |
| 1.3 | `Rc<RefCell<T>>` cycles without `Weak` | Reference-count cycles never get dropped — silent memory leak ([Arc docs](https://doc.rust-lang.org/std/sync/struct.Arc.html)) | Break exactly one back-edge per cycle with `Rc::downgrade` / `Arc::downgrade`; upgrade returns `Option<Rc<T>>` so callers handle the "parent dropped" case | — |
| 1.4 | `Arc<Mutex<T>>` for every field | Preemptive sharing assumes contention you don't have. Adds atomic ops, virtual address indirection, and **poisoning surface** to non-shared data | Decide ownership first. `Arc` only when actually shared across tasks/threads. Inner `Mutex` only when actually mutated under sharing | — |
| 1.5 | `RefCell<T>` for "convenience" interior mutability | Moves borrow checking to runtime — `borrow_mut()` panics on conflict; tests may pass and prod panics | Make the function take `&mut self`. Use `Cell<T>` for `Copy` types. Use `OnceCell` for write-once | — |
| 1.6 | Holding a `&` to a field then calling `&mut self` method | E0502: "cannot borrow as mutable because it is also borrowed as immutable" | Split borrows (destructure `self`), use `mem::take` / `mem::replace` to swap out the field, or refactor so the `&mut` method doesn't need the borrowed field | — |
| 1.7 | Returning `&T` to local data (`fn f() -> &str { let s = String::new(); &s }`) | Dangling reference — caught at compile time but trips up newcomers who then over-clone | Return owned `String`; or take a buffer parameter; or use `Cow<'a, str>` to defer the allocation decision | — |
| 1.8 | `Vec::iter().collect::<Vec<_>>()` round-trip just to re-iterate | Allocates twice (the original + the new `Vec`), no semantic gain | Pass the iterator through; reuse `.iter()` or `.into_iter()` directly | `clippy::needless_collect` |
| 1.9 | `&Vec<T>` / `&String` / `&PathBuf` parameters | Forces caller to have exactly that owned type — `&[T]` / `&str` / `&Path` work for arrays, literals, slices, etc. | `&[T]` / `&str` / `&Path` everywhere unless you genuinely need the owned API | `clippy::ptr_arg` |
| 1.10 | Passing `Vec<T>` by value when you only read it | Forces the caller to give up ownership and forces a `clone()` at the call site | `&[T]` parameter; the caller keeps ownership | `clippy::needless_pass_by_value` |
| 1.11 | Passing big `Copy` structs by value to hot inner loops | Even `Copy` involves a memcpy; for ≥16 bytes the win usually goes to `&T` | `&T` for parameter; `#[derive(Copy)]` only on types ≤ 2 words | `clippy::large_types_passed_by_value` |
| 1.12 | `clone()` then mutate (`let mut v = orig.clone(); v.push(x)`) when `orig` is discarded right after | Wasted alloc — you owned the original | Pass `orig` by value (`mut orig: Vec<_>`) or `std::mem::take(&mut orig)` | `clippy::redundant_clone` |
| 1.13 | `if let Some(x) = map.get(&k) { ... } else { map.insert(k, v); }` (double lookup) | Two hash operations; also runs afoul of NLL when the `else` arm needs `&mut map` | `map.entry(k).or_insert_with(\|\| v)` | `clippy::map_entry` |
| 1.14 | `vec.iter().find(...).is_some()` | Allocates an option, awkward | `vec.iter().any(...)` | `clippy::search_is_some` |
| 1.15 | Manual `Drop` impl on a type whose only resource is owned `Vec` / `Box` | Drop is already automatic, recursive, and correct. Manual drop disables struct field reordering and may suppress optimizations | Remove the `impl Drop`; rely on automatic recursive drop | — |
| 1.16 | `*self = Self::new()` inside a method to "reset" | Drops the old `self`, then runs `Self::new`. Fine, but readers panic about the second `Self::new` if it does I/O | `*self = Default::default()` or factor reset logic into a dedicated method with a clear name | — |
| 1.17 | `let _ = mutex.lock()` to "drop immediately" | `let _ = expr` **drops `expr` at end of statement**, not immediately, when there's a temporary involved; the guard is held for *zero* statements but readers misread the intent | Use `drop(mutex.lock())` for clarity, or just `mutex.lock();` + immediate scope exit | `clippy::let_underscore_lock` |
| 1.18 | Splitting one method into "ref" + "mut" variants on the same struct | Code duplication; the borrow checker often allows a single `&mut self` to do both | One `&mut` method; if read-only access is needed during call, restructure | — |

### 1.A `Rc<RefCell<T>>` cycle — concrete example

```rust
// LEAKS — parent → child via Rc, child → parent via Rc. Refcount never reaches 0.
struct Node { parent: Option<Rc<RefCell<Node>>>, children: Vec<Rc<RefCell<Node>>> }

// FIX — child → parent via Weak. Upgrade returns Option<Rc<T>>; caller handles "parent dropped".
struct Node {
    parent:   Option<Weak<RefCell<Node>>>,
    children: Vec<Rc<RefCell<Node>>>,
}
```

### 1.B Split-borrows escape hatch

```rust
// E0502: cannot borrow `self` as mutable because field `a` is borrowed
fn step(&mut self) {
    let a_ref = &self.a;        // immutable borrow of a
    self.b.push(a_ref.clone()); // mutable borrow of b — but compiler sees borrow of *self*
}

// FIX 1 — destructure to make the split borrow obvious
fn step(&mut self) {
    let Self { a, b } = self;
    b.push(a.clone());
}
```

### 1.C `Arc<Mutex<T>>` everywhere — when `&mut T` would do

```rust
// BAD — preemptive sharing, no actual contention
struct Pipeline {
    stages: Vec<Arc<Mutex<Stage>>>,    // each stage shared "just in case"
    metrics: Arc<Mutex<Metrics>>,       // mutated only by one task
}

impl Pipeline {
    fn run(&self) {
        for s in &self.stages {
            let s = s.lock().unwrap();   // every call: atomic + mutex acquire
            s.process();
        }
        self.metrics.lock().unwrap().record();
    }
}

// GOOD — only share what's actually shared
struct Pipeline {
    stages: Vec<Stage>,                  // owned exclusively by Pipeline
    metrics: Metrics,                    // mutated through &mut self
}

impl Pipeline {
    fn run(&mut self) {
        for s in &mut self.stages { s.process(); }
        self.metrics.record();
    }
}

// If a separate task genuinely needs metrics, expose a snapshot:
fn metrics_snapshot(&self) -> MetricsSnapshot { self.metrics.snapshot() }
```

---

## 2. Lifetime Pitfalls

The pretzelhammer blog "[Common Rust Lifetime Misconceptions](https://github.com/pretzelhammer/rust-blog/blob/master/posts/common-rust-lifetime-misconceptions.md)" catalogs the canonical confusions; this section condenses them.

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 2.1 | Adding explicit `<'a>` annotations the compiler would have elided | Pollutes signatures, signals more constraint than the function actually has, breaks downstream inference | Trust elision: one input ref → output ref, `&self` → ref tied to self. Annotate only when the borrow checker actually fails | `clippy::needless_lifetimes` |
| 2.2 | `&'static str` in function params (`fn log(msg: &'static str)`) | Excludes any `&str` that came from a runtime allocation; caller must `Box::leak` or store in a static | Use plain `&str` unless you provably need the value to live for program lifetime | — |
| 2.3 | `'static` bound on a generic (`T: 'static`) added "to make it compile" | Excludes all types borrowing from anything — usually means you `Box`-ed something that didn't need it, or held a value across a Send boundary that didn't need to | Inspect the *real* lifetime requirement: tasks spawned to a runtime do need `'static`; many other uses don't | — |
| 2.4 | Confusing `&'a T` with `T: 'a` | They're different: `&'a T` requires `T: 'a` (every reference inside `T` must outlive `'a`), but `T: 'a` does not imply `T` is a reference | Read `T: 'a` as "type `T` is valid for at least `'a`"; not "value has lifetime `'a`" | — |
| 2.5 | `Box<dyn Trait>` instead of `Box<dyn Trait + 'a>` | Defaults to `Box<dyn Trait + 'static>`, which silently rejects borrowed inputs | Add the explicit `'a`; or design the trait so impls own their data | — |
| 2.6 | Lifetime variance bugs (`Cell<&'a T>` used invariantly) | `Cell<&'a T>` is invariant in `'a`; you can't subtype it. Mixing scopes inside a `Cell` of refs is one of the classic "why won't this compile" footguns | Use `Cell<T>` of owned data; or wrap in `Cell<&'static T>` with `Box::leak`; or rethink the architecture. See variance table in [`rust-language-spec.md §2.5`](./rust-language-spec.md#25-variance) | — |
| 2.7 | `for<'a>` (higher-ranked trait bounds) used where impl-Trait would suffice | Steep error messages, GAT-style mistakes | Prefer `impl FnMut(&Item)` over `for<'a> FnMut(&'a Item)` unless the caller actually needs to choose `'a` | — |
| 2.8 | `&'a self` in a trait method then matching with `'a` in impls | Trait elision says it's `fn m<'b>(&'b self)`. Constraining to `'a` everywhere in impls couples unrelated methods through `'a` | Use elision; let each method bind its own lifetime | — |
| 2.9 | Returning `&str` borrowed from a local `String` built via `format!` | Dangling — caught at compile time but trips people into excess cloning | Return `String`; or pass a `&mut String` to write into; or use `Cow<'_, str>` if the borrowed case dominates | — |
| 2.10 | `Pin<&mut Self>` projection by hand inside a future | `Pin` invariants are easy to break (e.g. moving a field that's structurally pinned) | Use `pin-project-lite` or `pin-project`; never hand-roll unless you've proved every field's pinning status | — |
| 2.11 | Reading `<'a>` "backwards" — treating it as a value | `<'a>` *declares* a placeholder the compiler will pick; it's not a value | Read `fn foo<'a>(x: &'a T)` as "there exists some `'a` ≥ the call site such that..." | — |
| 2.12 | Holding a `&str` reference to a value inside an `Rc<RefCell<String>>` across `borrow_mut` | The `Ref<'_, String>` only lives for the borrow scope; `&str` from it dangles after the scope ends | Clone the string out of the borrow; or restructure to hold the borrow guard for the right scope | — |

---

## 3. Type System Pitfalls

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 3.1 | Over-generic `fn f<T: Trait>(t: T)` for every interface | Monomorphization bloats binary, slows compile, can defeat inlining via instruction-cache thrash | Use `&dyn Trait` when the function isn't on a hot path and binary size matters | — |
| 3.2 | Under-generic — concrete `&Vec<T>` parameters | Type-locks the API to one storage backing | Generalize: `&[T]`, `impl IntoIterator<Item = T>`, etc. | `clippy::ptr_arg` |
| 3.3 | Deeply nested `Option<Result<Option<T>, E>>` | Cognitive overload, awkward `?` chains | Define a domain enum (`enum Outcome { Found(T), Missing, Failed(E) }`) or use `Result<Option<T>, E>` consistently | — |
| 3.4 | Primitive-obsession: `String` for IDs, dates, money | Mix up `user_id` and `org_id` at the call site; no compile-time discrimination | Newtype each ID: `pub struct UserId(pub Uuid);` Implements zero-cost type safety per [SoftwareMill's newtype guide](https://softwaremill.com/mastering-rust-patterns-vol-1-rust-newtypes/) | — |
| 3.5 | Wildcard `_` arm matching on enums you control | When a new variant is added, the `_` arm silently catches it — bug latency | Match each variant explicitly; or mark enum `#[non_exhaustive]` only at crate boundary and use a `_` arm only **with a `// new variants land here intentionally`** comment | `clippy::wildcard_enum_match_arm` |
| 3.6 | `enum E { A, B, C }` with no `#[non_exhaustive]` on a public enum that may grow | Adding a variant becomes a major-version break | Mark with `#[non_exhaustive]` from day 1 of public API — but only if you actually plan to grow it; per [predr.ag](https://predr.ag/blog/some-rust-breaking-changes-do-not-require-major-version/), this is the most common silent breakage | — |
| 3.7 | `T::default()` for types where default has no meaningful semantics | Hidden zero values propagate (e.g. `Duration::default() == 0s`), causing silent off-by-N | Don't implement `Default` for domain types unless zero-state is genuinely valid | — |
| 3.8 | `i32` for everything (including indexes, counts, sizes) | Sign confusion, overflow on small int, mixing with `usize` from slices | `usize` for sizes/indexes, `u32`/`u64` for explicit ranges, `i32` only when negatives are required | — |
| 3.9 | `as` conversions everywhere | `as` truncates silently (`1000u32 as u8 == 232`), loses precision on float→int, and is impossible to grep for | `u8::try_from(x)?` / `i32::from(u16)` / `u32::cast_from(...)` with the `cast` crate. Disable `as` via `#![deny(clippy::as_conversions)]` in safety-critical code | `clippy::as_conversions`, `clippy::cast_possible_truncation`, `clippy::cast_sign_loss` |
| 3.10 | `bool` parameter on a public function (`fn open(force: bool)`) | Call site `f.open(true)` is unreadable | Two-variant enum (`enum Force { Yes, No }`) or a typed builder | `clippy::fn_params_excessive_bools` |
| 3.11 | `Result<T, ()>` | Erases what failed | Use `Option<T>` (`None` = failed) or a real error type | `clippy::result_unit_err` |
| 3.12 | `Box<T>` field for "indirection" with no other reason | Adds an allocation; the type is the same size as `Box<T>` | Inline the field; or use `Option<Box<T>>` for genuinely-optional heap allocation | `clippy::redundant_allocation` |
| 3.13 | `Vec<Box<dyn Trait>>` inside a struct that's always used homogeneously | Loses inlining, dispatches via vtable on every call | Use enum dispatch (`enum Variant { A(A), B(B) }`) or generic with monomorphization at the use site | — |
| 3.14 | `match` on `bool` (`match x { true => ..., false => ... }`) | Always less readable than `if`/`else` | `if x { ... } else { ... }` | `clippy::match_bool` |

### 3.A Newtype for IDs

```rust
// PROBLEM — easy to swap arguments
fn transfer(from: String, to: String, amount: u64) { ... }
transfer(to_id, from_id, 100); // compiles, silently wrong

// FIX — distinct types
pub struct UserId(pub Uuid);
pub struct AccountId(pub Uuid);
pub struct Cents(pub u64);

fn transfer(from: AccountId, to: AccountId, amount: Cents) { ... }
transfer(to.into(), from.into(), Cents(100)); // forces conversion, eyes catch swap
```

---

## 4. Async / Await Pitfalls (Extensive)

Async Rust is where the biggest production bugs live in 2026. Sources: [Alice Ryhl's blog](https://ryhl.io/blog/async-what-is-blocking/), [tokio shared-state tutorial](https://tokio.rs/tokio/tutorial/shared-state), [Oxide RFD-400 cancel safety](https://rfd.shared.oxide.computer/rfd/0400), [tokio select! docs](https://docs.rs/tokio/latest/tokio/macro.select.html). Spec background on cancellation safety: [`rust-language-spec.md §4.7`](./rust-language-spec.md#47-cancellation-safety).

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 4.1 | Blocking sync I/O inside async (`std::fs::read`, `std::thread::sleep`, `reqwest::blocking`) | Stalls the runtime worker thread; in production with high concurrency, this **looks fine in dev** with 8 cores and explodes under load | `tokio::fs`, `tokio::time::sleep`, `reqwest` async client. For unavoidable blocking → `tokio::task::spawn_blocking` | — |
| 4.2 | CPU-bound work in async (`for x in big_vec { hash(x) }` directly in `async fn`) | Same root cause — async tasks can't yield mid-loop, monopolize the worker | `spawn_blocking` for short tasks; `rayon` for parallel CPU work; cooperative yielding via `tokio::task::yield_now().await` in long loops | — |
| 4.3 | Holding `std::sync::MutexGuard` across `.await` | `MutexGuard` is `!Send` — your future becomes `!Send` and `tokio::spawn` rejects it. Worse: even if it's `Send` (parking_lot fair mutex), you can deadlock waiting on a task that needs the lock | Scope the lock: `{ let g = m.lock().unwrap(); g.x = 1; } // drop here`. Avoid carrying `MutexGuard` past `.await` boundaries | `clippy::await_holding_lock` |
| 4.4 | `tokio::sync::Mutex` for everything | The async mutex is heavier than `std::sync::Mutex` and has cancel-safety footguns — cancelling a `lock()` call loses your queue position | Default to `std::sync::Mutex` and never hold across `.await`. Use `tokio::sync::Mutex` only when you provably *must* hold the lock across an await | — |
| 4.5 | `RefCell::borrow_mut()` held across `.await` | Same as 4.3 — `RefMut` is `!Send`, future poisoned | Same fix: scope the borrow before the await | `clippy::await_holding_refcell_ref` |
| 4.6 | `tokio::spawn(fut)` and dropping the `JoinHandle` | The task **keeps running** — orphaned — and **panics are silently swallowed**. ([JoinHandle docs](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html)) | Store handles in `JoinSet`; or `.await` them; or use a supervisor pattern with `tokio::task::JoinSet::join_next` to propagate panics | — |
| 4.7 | `select!` branches that aren't cancel-safe | The losing branches are **dropped mid-future** — partial state, lost reads from streams, etc. ([Oxide RFD-400](https://rfd.shared.oxide.computer/rfd/0400)) | Only put cancel-safe futures in `select!`; common safe ones: `tokio::sync::mpsc::Receiver::recv`, `tokio::time::sleep`, AsyncRead/AsyncWrite combinators returning `Poll::Pending` on incomplete. Wrap stateful work in a task and select on its `Receiver` | — |
| 4.8 | `select!` without `biased;` when shutdown/error must always be polled | Default round-robin random polling means a hot stream can starve the shutdown branch | `tokio::select! { biased; _ = shutdown.changed() => { ... }, msg = stream.recv() => { ... } }` | — |
| 4.9 | `futures::executor::block_on(fut)` inside an `async fn` running on tokio | Deadlocks: blocks the worker that's executing it; current-thread runtime deadlocks instantly | Use `.await` instead. If you absolutely need to bridge sync→async, use `tokio::runtime::Handle::current().block_on(fut)` from `spawn_blocking` only | — |
| 4.10 | `tokio::sync::mpsc::unbounded_channel` for inter-task communication | No backpressure — producer outruns consumer until OOM. [tokio issue #4321](https://github.com/tokio-rs/tokio/issues/4321) documents memory leaks under sustained back-pressure | `mpsc::channel(N)` with a chosen N. Picking a number is the *point* — it forces you to think about backpressure | — |
| 4.11 | `Pin` projection mistakes — moving a structurally-pinned field | Self-referential futures become invalid; UB if the field is a future that registered a waker pointing to the old location | Use `pin-project-lite`; mark `#[pin]` precisely; never expose `&mut field` for pinned fields | — |
| 4.12 | `#[tokio::main]` inside a library | Forces every consumer onto tokio and the multi-thread runtime; obscures the actual entry point | `#[tokio::main]` lives in `src/bin/*` only. Libraries are runtime-agnostic — use `tokio::sync` (which only needs the rt feature) or expose `Stream`/`Future` directly | — |
| 4.13 | `async fn` in a trait returning non-`Send` future used with `tokio::spawn` | Per [baby steps' Send-bounds post](https://smallcultfollowing.com/babysteps/blog/2023/02/01/async-trait-send-bounds-part-1-intro/), native async traits (1.75+) don't yet let you require `Send` futures; spawning fails compile | Use `async-trait` for `dyn` use cases until RTN matures; or use `impl Future<Output=...> + Send` on individual methods | — |
| 4.14 | Storing `Vec<JoinHandle<()>>` and never awaiting | Same as 4.6 — orphaned tasks, swallowed panics | `JoinSet` with periodic `join_next()` drain; or a supervisor that awaits all on shutdown | — |
| 4.15 | `.fuse()` missing on a future polled after completion | Polling a completed future is allowed to panic; in `select!` loops, re-polling a finished branch breaks invariants | Use `FusedFuture` from `futures::future::Fuse`; or rebuild the future each loop iteration when semantically appropriate | — |
| 4.16 | `tokio::time::sleep(d).await` inside a hot loop without `tokio::task::yield_now()` consideration | `sleep` is cooperative; if there's no `.await` in the loop body, the worker can be monopolized | Either `sleep_until` for absolute deadlines, or `interval` with `tick()` for steady cadence | — |
| 4.17 | `Stream::next` borrowing pitfall (`while let Some(x) = stream.next().await { ... }`) | The `Pin<&mut Self>` from `next()` borrows `stream` exclusively — you can't call any other `&mut stream` method inside the loop | Use `tokio_stream::StreamExt::next` with explicit pinning, or `while let Some(x) = stream.try_next().await? {}` from `TryStreamExt` | — |
| 4.18 | Channel-based actor with `mpsc::Sender::send` from a `Drop` impl | `Drop` is sync, `send` is async — you can't `.await`. `try_send` may fail under load and silently drop the shutdown signal | Use `tokio::sync::mpsc::UnboundedSender::send` (which is sync) for shutdown signals only — but be aware of the unbounded warning. Or restructure shutdown via an atomic flag + watch channel | — |
| 4.19 | `Arc<tokio::sync::RwLock<HashMap<K, V>>>` for cache hot paths | Per [Tokio shared-state tutorial](https://tokio.rs/tokio/tutorial/shared-state): the lock contends, and async `RwLock` is heavier than sync. Per Telex's mutex-vs-rwlock pattern, RwLock only wins under heavy read concurrency | `std::sync::RwLock` if not held across await; `DashMap` for true high-concurrency hash maps; sharded locking | — |
| 4.20 | Long-running task with no cancellation token | Process shutdown can't drain in-flight work | `tokio_util::sync::CancellationToken` passed to every task; tasks check `is_cancelled()` at every yield point | — |
| 4.21 | `loop { let permit = sem.acquire().await?; tokio::spawn(work(permit)) }` without checking shutdown | Spawned tasks outlive the loop, can't be joined | Combine with `JoinSet`: `set.spawn(work(permit))` so shutdown drains them | — |
| 4.22 | Hot-loop polling without yielding (`loop { if cond { break; } }` inside `async fn`) | Monopolizes the worker | `tokio::task::yield_now().await` inside the loop, or restructure as a notify-based wait | — |
| 4.23 | `async move` capturing `&self` for a spawned task | `&self` lifetime can't be `'static` → compile error; users then `.clone()` everything | Take `Arc<Self>` and `Arc::clone(&self)` into the spawn; or restructure so the task doesn't reference `self` | — |
| 4.24 | `block_in_place` in a current-thread runtime | `block_in_place` only works on the multi-thread runtime; panics on `current_thread` | Use `spawn_blocking` instead, which works on both | — |
| 4.25 | `tokio::join!` instead of `try_join!` when any task can error | `join!` waits for *all* futures regardless of errors; if one returns `Err`, others still consume resources | `try_join!` short-circuits on first error; better cancellation semantics | — |

### 4.A `MutexGuard` across `.await` — minimal reproduction

```rust
use std::sync::Mutex;
use tokio::time::{sleep, Duration};

async fn bad(m: &Mutex<i32>) {
    let mut g = m.lock().unwrap();
    *g += 1;
    sleep(Duration::from_millis(10)).await;  // ← MutexGuard alive — future is !Send
    *g += 1;
}
// tokio::spawn(bad(&m)) fails: `MutexGuard<'_, i32>` is not `Send`
```

```rust
// FIX — scope the lock so the guard is dropped before .await
async fn good(m: &Mutex<i32>) {
    {
        let mut g = m.lock().unwrap();
        *g += 1;
    } // ← guard dropped here
    sleep(Duration::from_millis(10)).await;
    {
        let mut g = m.lock().unwrap();
        *g += 1;
    }
}
```

### 4.B `select!` cancel-safety footgun

```rust
// BAD — read_exact is NOT cancel-safe. If `timeout` wins, the partial bytes are lost.
loop {
    tokio::select! {
        result = socket.read_exact(&mut buf) => { /* handle */ }
        _      = tokio::time::sleep(Duration::from_secs(1)) => { /* tick */ }
    }
}

// GOOD — wrap the cancel-unsafe future in its own task with a stable receiver,
// then select on the receiver (recv IS cancel-safe).
let (tx, mut rx) = tokio::sync::mpsc::channel(8);
tokio::spawn(async move {
    let mut buf = [0; 1024];
    while let Ok(n) = socket.read_exact(&mut buf).await {
        if tx.send(buf[..n].to_vec()).await.is_err() { break; }
    }
});

loop {
    tokio::select! {
        biased;
        Some(msg) = rx.recv() => { /* handle */ }
        _         = tokio::time::sleep(Duration::from_secs(1)) => { /* tick */ }
    }
}
```

### 4.C Orphan task — panic vanishes

```rust
// BAD — handle dropped, panic silently swallowed
tokio::spawn(async {
    panic!("oh no");
});
// No log, no exit code change, problem festers.

// GOOD — JoinSet propagates
let mut set = tokio::task::JoinSet::new();
set.spawn(async { panic!("oh no") });
while let Some(res) = set.join_next().await {
    if let Err(e) = res {
        if e.is_panic() { std::panic::resume_unwind(e.into_panic()); }
    }
}
```

### 4.D Unbounded channel memory blow-up

```rust
// BAD — fast producer, slow consumer: memory grows without bound
let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel();

tokio::spawn(async move {
    loop {
        let event = poll_kafka().await;        // 100K/sec
        let _ = tx.send(event);                // never blocks
    }
});

tokio::spawn(async move {
    while let Some(e) = rx.recv().await {
        write_to_postgres(&e).await;            // 1K/sec
        // → queue grows ~99K events/sec until OOM
    }
});

// GOOD — bounded channel applies backpressure
let (tx, mut rx) = tokio::sync::mpsc::channel(1024);

tokio::spawn(async move {
    loop {
        let event = poll_kafka().await;
        if tx.send(event).await.is_err() { break; }   // ← awaits when full
    }
});
// Producer naturally slows to consumer rate; upstream Kafka backpressure kicks in.
```

### 4.E Blocking inside async — the silent killer

```rust
// BAD — looks fine on a dev box with 8 cores, dies in prod
async fn handle_request(req: Request) -> Response {
    let data = std::fs::read("/var/cache/blob")?;     // sync I/O
    std::thread::sleep(Duration::from_millis(100));   // blocks the worker
    parse(&data)                                       // CPU on the worker
}

// GOOD — yield to runtime, offload blocking
async fn handle_request(req: Request) -> Response {
    let data = tokio::fs::read("/var/cache/blob").await?;
    tokio::time::sleep(Duration::from_millis(100)).await;
    tokio::task::spawn_blocking(move || parse(&data)).await?
}
```

---

## 5. Error Handling Pitfalls

Sources: [Caroline Morton's anyhow/thiserror guide](https://www.carolinemorton.co.uk/blog/rust-error-handling-anyhow-thiserror/), [Luca Palmieri's deep dive](https://www.lpalmieri.com/posts/error-handling-rust/), [Rust10x error handling](https://rust10x.com/best-practices/error-handling). See also [`rust-best-practices.md §2`](./rust-best-practices.md#2-error-handling-patterns--deep) for the four-crate decision tree.

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 5.1 | `Box<dyn Error>` in library public API | Callers can't match on variants — must downcast or string-match. Per the [thiserror/anyhow guide](https://www.carolinemorton.co.uk/blog/rust-error-handling-anyhow-thiserror/): "Using `Box<dyn std::error::Error>` throws away type information." | Concrete `thiserror` enum at crate boundary; let `anyhow` aggregate at binary boundary | — |
| 5.2 | `anyhow::Error` in library public API | Same as 5.1 — opaque. `anyhow` is for binaries / scripts. | `thiserror` for library; document the error enum | — |
| 5.3 | `.unwrap()` / `.expect()` in production library code | Every unwrap is a potential panic / DoS surface. Hard to grep for "what bombs at 3am". | Return `Result`; allow `unwrap` only in `main`, tests, or with `// SAFETY: <invariant>` proof | `clippy::unwrap_used`, `clippy::expect_used` |
| 5.4 | `panic!` for control flow (e.g. "this string is invalid, panic") | Same; especially bad when reached from external input | `Result<_, ParseError>`; reserve `panic!` for "we promised it couldn't happen but it did" | `clippy::panic`, `clippy::panic_in_result_fn` |
| 5.5 | Swallowing errors with `let _ = risky();` | Drops the `Result` — no log, no propagation. The "I'll fix it later" landmine | Either `?`-propagate, `.expect("...")` with proof, or explicit `if let Err(e) = ... { tracing::warn!(...) }`. `let _ = ...` is acceptable **only** with an inline comment explaining why | `clippy::let_underscore_must_use` |
| 5.6 | Missing `.context()` chains (`anyhow`) | Top-level error reads "file not found" with zero hint about *which* file or *why* it was being read | `.with_context(\|\| format!("loading config {path:?}"))?` on every `?` boundary where a human will read the result | — |
| 5.7 | `?` returning the wrong error type — proliferating `From` impls | When `fn f() -> Result<T, MyErr>` calls something returning `io::Error`, you need `From<io::Error> for MyErr` — but stacking `From` impls makes upstream changes silently re-route errors | Centralize `From` impls; or wrap with `.map_err(MyErr::Io)?` for explicit conversion at the call site | — |
| 5.8 | `eprintln!("error: {}", e)` for errors | No structured fields, no level, no traceability | `tracing::error!(error = %e, "operation failed")` — pairs with `tracing-subscriber` for structured logs | — |
| 5.9 | Mixing `thiserror` and `anyhow` in the same public API surface | Confuses consumers about whether they should `match` or `display` | `thiserror` for the library, `anyhow` only inside binaries that consume it | — |
| 5.10 | Single `enum AppError { ... }` with 50 variants for an entire app | "God error" — most call sites can only fail in 2-3 ways, but signatures imply 50 | Per-module error enums; use `#[error(transparent)]` + `#[from]` to compose | — |
| 5.11 | Stringly-typed errors (`Result<T, String>`) | No type info, can't pattern-match, formats lost | At minimum `thiserror`; at minimum `Box<dyn Error + Send + Sync>` if you need a quick prototype | — |
| 5.12 | `Result<T, E>` returned from `Drop` impl by panicking | Drop can't return Result; panicking from Drop during unwind aborts the process (see §7.9) | Either: log via `tracing::error!` and continue; or expose an explicit `close()` method that returns Result | — |
| 5.13 | `unwrap_or_default()` masking a parse failure that should have surfaced | Silent zeros downstream | `.unwrap_or_default()` only when default is genuinely the desired fallback; otherwise `?` | — |
| 5.14 | `.ok()` to convert `Result` to `Option` without logging | Silent error swallow — the most common variant of 5.5 | If you must discard, log it: `.map_err(\|e\| tracing::warn!(?e)).ok()` | — |
| 5.15 | `#[error("...")]` with embedded `{:?}` debug formatting | Per OWASP: leaks internal details into user-facing error messages | Use `{}` Display formatting in user-facing variants; `{:?}` only when target audience is the developer log | — |
| 5.16 | `assert!`/`assert_eq!` for runtime input validation | Asserts can be optimized out in `release` only via `debug_assert!`; regular `assert!` is on in release too, but it panics — bad input → process down | Validate with `Result`; reserve `assert!` for invariants that cannot fail given upstream contracts | — |
| 5.17 | Calling `.unwrap()` on `Result` returned from cross-thread `recv()` | `recv()` returns `Err(RecvError)` when the channel is closed (normal shutdown!) — `unwrap` panics on every clean shutdown | Match: `Ok(msg) => process(msg), Err(_) => break;` | — |

### 5.A `thiserror` library + `anyhow` app

```rust
// lib.rs
#[derive(thiserror::Error, Debug)]
pub enum ConfigError {
    #[error("file {0:?} not readable")]
    Io(#[from] std::io::Error),
    #[error("toml parse: {0}")]
    Parse(#[from] toml::de::Error),
    #[error("missing required field {0}")]
    MissingField(&'static str),
}

pub fn load(path: &Path) -> Result<Config, ConfigError> { ... }

// main.rs
use anyhow::Context;
fn main() -> anyhow::Result<()> {
    let cfg = config::load(Path::new("app.toml"))
        .context("loading startup config")?;
    ...
}
```

---

## 6. Performance Pitfalls

Sources: [The Rust Performance Book](https://nnethercote.github.io/perf-book/heap-allocations.html), [Llogiq's perf pitfalls](https://llogiq.github.io/2017/06/01/perf-pitfalls.html). For the profile-first toolkit (samply / pprof-rs / dhat / flamegraph) and allocator/SIMD/PGO advice, see [`rust-best-practices.md §6`](./rust-best-practices.md#6-performance-practices).

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 6.1 | Gratuitous `.clone()` on hot paths | Heap alloc per call; pointer chase | Take `&T`; use `Cow<'a, T>` if you sometimes need ownership | `clippy::redundant_clone` |
| 6.2 | `s + &t + &u + &v` string concatenation | Each `+` allocates a fresh `String`; O(n²) allocs for N pieces | `format!("{s}{t}{u}{v}")` (single alloc) or `String::with_capacity(estimated).push_str(...)` for known-large outputs | `clippy::string_add` |
| 6.3 | `String::new()` + `push_str` in a loop, no capacity hint | Reallocates ~log₂(N) times | `String::with_capacity(estimated_size)` upfront | — |
| 6.4 | `Vec::new()` + `push` in a loop, no capacity hint | Same — quasi-doubling means 0/4/8/16/32… reallocs | `Vec::with_capacity(n)` when n is known; `Vec::from_iter` when iterator is `ExactSizeIterator` | — |
| 6.5 | `vec.insert(0, x)` | O(n) — every element shifted right | `VecDeque::push_front` (O(1)); or build reversed and `.reverse()` once | `clippy::inefficient_to_string` (related) |
| 6.6 | `vec.remove(0)` | Same — O(n) shift | `VecDeque::pop_front`; or `vec.swap_remove(0)` if order doesn't matter | — |
| 6.7 | `HashMap<K, V>` for tiny maps (< ~16 entries) | Hash + heap alloc dwarfs the gain; cache-unfriendly | `Vec<(K, V)>` + linear scan; or `indexmap::IndexMap` for ordered; or `[(K, V); N]` slice on stack | — |
| 6.8 | `Box<dyn Trait>` for short-lived polymorphism on hot paths | vtable dispatch defeats inlining; allocation per object | Enum dispatch (`enum Op { A(A), B(B) }`); or generic + monomorphization | — |
| 6.9 | `Arc<RwLock<T>>` for write-heavy workloads | RwLock writers wait for *all* readers; under heavy writes, throughput collapses below Mutex | Per [Telex's pattern](https://telex-tui.github.io/blog/rust-patterns-arc-mutex.html): "Default to Mutex." Use RwLock only when reads dominate by ≥ 10× | — |
| 6.10 | `&self` method taking large struct by reference but cloning internally | Caller paid for the borrow, you negate it | Either take `self` by value (consume), or refactor to not clone | `clippy::redundant_clone` |
| 6.11 | Missing `#[inline]` on small cross-crate hot functions | Without LTO, cross-crate fns don't inline by default; trivial accessors then cost a call | `#[inline]` on small (< ~10 LOC) cross-crate functions; `#[inline(always)]` very sparingly | — |
| 6.12 | Default `chrono` (heavy: timezones, wasm-bindgen) | Bloat + transitive deps | `time` crate is leaner; or `jiff` (modern, 2024+); or `chrono` with default-features off + specific features | — |
| 6.13 | `format!("{}", x)` for `Display` when `x` is already a `String` | Unnecessary allocation | Just `x.clone()` if you need owned, or pass `&x` if borrow works | `clippy::useless_format` |
| 6.14 | `to_string()` for cheap conversion (`123_i32.to_string()`) | Allocates; many call sites don't need owned `String` | `format!("{n}")` no faster; better: `write!(buf, "{n}")?` into a reusable buffer; or `itoa` for hot integer→string | — |
| 6.15 | `Vec<String>` when `Vec<&'static str>` would do (constant labels) | Each `String` is a heap alloc | `&'static str` constants; or `Cow<'static, str>` if some are runtime | — |
| 6.16 | `&Vec<T>::iter().cloned().collect::<Vec<_>>()` for a copy | Iterates + reallocates | `vec.clone()` is the same and clearer; or `vec.to_owned()` | `clippy::iter_cloned_collect` |
| 6.17 | Re-creating regex inside a hot loop | `Regex::new` is expensive (DFA compilation) | `lazy_static!` / `LazyLock`: `static RE: LazyLock<Regex> = LazyLock::new(\|\| Regex::new(...).unwrap());` | `clippy::regex_creation_in_loops` |
| 6.18 | `HashMap` with default `SipHash` for performance-critical lookup tables where DoS isn't a concern | SipHash is anti-DoS, not the fastest | `ahash::AHashMap` or `rustc_hash::FxHashMap` for trusted-input maps | — |
| 6.19 | `Result<T, BigError>` returned where `BigError` is hundreds of bytes | Stack frames inflate; `Result` is `max(T, E)` bytes | `Result<T, Box<BigError>>` to keep happy path small (LLVM may also optimize this); `clippy::result_large_err` flags it | `clippy::result_large_err`, `clippy::large_enum_variant` |
| 6.20 | `Vec::contains` for membership in a large set | O(n) linear scan | `HashSet` / `BTreeSet` (O(1) / O(log n)) | — |
| 6.21 | Sorting then `dedup` on a `Vec` you'll only check membership of | Sorts the whole vec unnecessarily | Build a `HashSet` directly | — |
| 6.22 | `clone().into_iter()` instead of `iter().cloned()` / `iter().copied()` | Allocates the temp `Vec` | `iter().cloned()` or `iter().copied()` (for `Copy`) | `clippy::cloned_instead_of_copied` |

---

## 7. Trait Design Pitfalls

Sources: [Rust Reference: orphan rule](https://rust-lang.github.io/chalk/book/clauses/coherence.html), [Drop docs](https://doc.rust-lang.org/std/ops/trait.Drop.html), [Nomicon: unwinding](https://doc.rust-lang.org/nomicon/unwinding.html). For the dyn-compatibility (object-safety) rules in detail, see [`rust-language-spec.md §3.5`](./rust-language-spec.md#35-trait-object-safety--renamed-to-dyn-compatibility-2024).

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 7.1 | Extension trait that pollutes the prelude (`impl<T> MyExt for T`) | Every type in scope now has your methods; auto-complete chaos; method name collisions silent | Scope the impl to specific traits/types; don't blanket impl unless you own the trait | — |
| 7.2 | Blanket `impl<T: Display> MyTrait for T` (you own `MyTrait`) | Locks you out of impls for specific `Display` types because they'd conflict with the blanket | Per [the orphan rule guide](https://www.slingacademy.com/article/understanding-coherence-rules-why-orphan-rules-restrict-certain-generic-impls/): keep blankets minimal; consider an explicit derive macro instead | — |
| 7.3 | Trying to `impl ForeignTrait for ForeignType` | Orphan rule rejection — you can't implement a trait you don't own for a type you don't own | Newtype: `pub struct MyVec(pub Vec<T>); impl Display for MyVec { ... }` | — |
| 7.4 | `Box<dyn Trait + Send + Sync + 'static>` without checking object safety | Object-unsafe traits (Self in signature, generic methods) can't be made into trait objects | Either: split into object-safe sub-traits; or use enum dispatch | — |
| 7.5 | Missing `Send`/`Sync` bounds on a trait used across threads | Compile error at the use site, far from the trait definition — confusing | If trait is meant to cross threads, document and add `: Send + Sync` (or auto-traits flow through impl) | — |
| 7.6 | Required associated type with no default (`type Item;`) | Every impl must define it; if it's almost always the same, this is friction | Provide a sensible default (Edition 2024 lets associated types have defaults in some forms) or split the trait | — |
| 7.7 | `Default` impl that performs I/O | `Default::default()` is expected to be cheap and infallible | Use a `Builder` or `try_new()` for I/O; `Default` is for in-memory zero state | — |
| 7.8 | `Display` impl that allocates inside `fmt` | Called from `format!`, error paths, panic messages — allocating in panic-handling can panic again | Write directly to `f` via `write!(f, "...", ...)` — no intermediate `String` | `clippy::format_in_format_args` |
| 7.9 | `Drop` impl that can panic | Per [Drop docs](https://doc.rust-lang.org/std/ops/trait.Drop.html) and [the Nomicon](https://doc.rust-lang.org/nomicon/unwinding.html): panic inside `Drop` during unwinding = process abort. | `if std::thread::panicking() { return; }` guard, or design Drop to never panic (log instead) | — |
| 7.10 | `Clone` impl that does I/O / takes a lock | Same as Default — Clone is expected to be O(size) and infallible | Provide `try_clone()` returning `Result` for the I/O case; don't impl `Clone` | — |
| 7.11 | Hash impl that disagrees with Eq | `a == b` must imply `hash(a) == hash(b)`; violating this breaks HashMap silently (lookups miss) | Derive both, or write both by hand carefully; if you derive `PartialEq` but skip `Hash`, document why | `clippy::derive_hash_xor_eq` |
| 7.12 | `Ord` impl inconsistent with `PartialOrd` (or with `Eq`) | Sorts can deadlock / loop / produce wrong order; HashMap-style collections silently misbehave | Derive when possible; if hand-implementing, ensure `partial_cmp == Some(cmp)` everywhere | `clippy::derive_ord_xor_partial_ord` |
| 7.13 | `PartialEq` only impl (no `Eq`) for a type that *is* equality-comparable | Can't use as HashMap key | Add `Eq` (it's a marker trait — empty body) | — |
| 7.14 | `Iterator::next` impl that allocates per call | Heap traffic per element; defeats the point of iterators | Maintain state in the iterator struct; yield references when ownership allows | — |
| 7.15 | Designing a trait then changing its method signature post-1.0 release | Major-version break — even adding a required method | Provide a default implementation; or release as `Trait2` and deprecate `Trait`; or use sealed traits | — |
| 7.16 | "Sealed trait" without a sealed marker | Users can implement your trait → you can't add required methods | Add `mod private { pub trait Sealed {} } pub trait MyTrait: private::Sealed {}` with `impl Sealed` only inside your crate | — |

### 7.A Object-safety failure

```rust
// PROBLEM — Self in return position breaks object safety
trait Builder {
    fn add(self, item: Item) -> Self;  // ← returns Self
}
let b: Box<dyn Builder> = ...; // ERROR: trait is not object safe

// FIX — split into object-safe core + object-unsafe extensions
trait BuilderCore {
    fn add_mut(&mut self, item: Item);   // object-safe
}
trait BuilderExt: BuilderCore + Sized {
    fn add(mut self, item: Item) -> Self { self.add_mut(item); self }
}
impl<T: BuilderCore + Sized> BuilderExt for T {}
```

### 7.B Drop panic disaster

```rust
impl Drop for Resource {
    fn drop(&mut self) {
        self.handle.close().expect("close failed");  // ← BAD: panic in drop during unwind = abort
    }
}

// FIX
impl Drop for Resource {
    fn drop(&mut self) {
        if let Err(e) = self.handle.close() {
            tracing::error!(?e, "Resource::drop close failed");
            // Don't panic — even if we're not unwinding, abort risk is too high.
        }
    }
}
```

---

## 8. Macro Pitfalls

Sources: [Rust Reference: macros by example](https://doc.rust-lang.org/reference/macros-by-example.html), [procedural macros](https://doc.rust-lang.org/reference/procedural-macros.html), [recursion limit attribute](https://doc.rust-lang.org/reference/attributes/limits.html). See also [`rust-language-spec.md §5`](./rust-language-spec.md#5-macros) for fragment specifiers, hygiene model, and the syn/quote workflow.

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 8.1 | `macro_rules!` that captures user identifiers unintentionally | Mixed-site hygiene: locals are hygienic but non-local items aren't, leading to silent shadowing of user code | Use fully-qualified paths (`::std::option::Option::Some`); declare locals with `$crate::__private::*` names | — |
| 8.2 | `macro_rules!` recursion blowing the default limit (128) | "recursion limit reached" error; users hit this in nested usages | Restructure to TT-munch in larger chunks; or `#![recursion_limit = "256"]` in the consumer crate with a comment | — |
| 8.3 | `macro_rules!` that uses `#[recursion_limit]` to *avoid* fixing exponential expansion | Hides a real algorithmic problem | Rewrite to be O(n) in tokens; or convert to proc-macro | — |
| 8.4 | Proc-macro that produces tokens at `Span::call_site()` everywhere | Errors point to the macro invocation, not the user's bad input | `quote::quote_spanned! { input_span => ... }`; preserve user spans for diagnostics | — |
| 8.5 | Derive macro with hidden runtime cost (e.g. `#[derive(Display)]` calling `format!` internally) | Users don't expect derives to allocate | Document; provide a slim alternative; never silently introduce I/O or alloc | — |
| 8.6 | Proc-macro crate without `proc-macro = true` in `Cargo.toml` | Won't be loaded as a proc-macro; cryptic compile error | `[lib] proc-macro = true` | — |
| 8.7 | Proc-macro crate with non-proc-macro dependencies pulled into consumer | Proc-macro crates only execute at compile time on the host. Heavy deps slow every consumer's compile | Keep proc-macro deps minimal (`syn` features tuned, no `tokio`); split into proc-macro + runtime crates | — |
| 8.8 | `macro_rules!` invoked recursively with growing token trees | Compiler hangs; per [Rust issue #105830](https://github.com/rust-lang/rust/issues/105830), some patterns bypass the recursion limit | TT-munching with explicit termination; consider proc-macro for non-trivial cases | — |
| 8.9 | Procedural macro that `panic!`s on bad input | User sees backtrace from proc-macro — not actionable | Return `syn::Error::new(span, "msg").to_compile_error()` — user gets a clean compile error with span | — |
| 8.10 | Proc-macro with arbitrary side effects (file writes, network) | Per [safety-critical guidelines #365](https://github.com/rustfoundation/safety-critical-rust-coding-guidelines/issues/365): "Procedural macros can have arbitrary side effects, which can exhaust compiler resources or expose a vulnerability" | Pure token transforms only; if codegen needs build context, use `build.rs` (which is explicit) | — |
| 8.11 | Endless loop inside proc-macro | Compiler hangs (not caught by compiler) | Always have a token budget / depth limit; test with `cargo expand` on adversarial input | — |
| 8.12 | `macro_rules!` matching `$e:expr` then using it twice — re-evaluating side effects | `$e` is a token-level capture; `$e + $e` evaluates `$e` twice | Bind to a local: `{ let __tmp = $e; __tmp + __tmp }` | — |
| 8.13 | `macro_rules!` that doesn't use `#[macro_export]` and expects cross-crate visibility | Macro is crate-local; consumers get "cannot find macro" | `#[macro_export]` for public macros; or `pub use` from a public mod for proc-macro-like control | — |

---

## 9. Unsafe Pitfalls (High-Stakes)

Sources: [The Rustonomicon: transmutes](https://doc.rust-lang.org/nomicon/transmutes.html), [Nomicon: what unsafe does](https://doc.rust-lang.org/nomicon/what-unsafe-does.html). The canonical UB list lives in [`rust-language-spec.md §6.2`](./rust-language-spec.md#62-canonical-undefined-behaviors-rust-reference); the Stacked vs Tree Borrows model in [`§6.3`](./rust-language-spec.md#63-stacked-borrows--tree-borrows); the SAFETY-comment template in [`§6.5`](./rust-language-spec.md#65-safety-comment-template).

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 9.1 | `mem::transmute` between non-`#[repr(transparent)]` types | Layout is unspecified — `transmute::<Foo, Bar>(...)` is UB even if `Foo` and `Bar` have the same fields | `#[repr(transparent)]` only between exact wrapper types; `bytemuck::cast` for plain-old-data; `bytemuck::Pod` derive for stronger guarantees | `clippy::transmute_*` family |
| 9.2 | `mem::transmute::<&'a T, &'b T>(...)` to extend a lifetime | Per the [Nomicon](https://doc.rust-lang.org/nomicon/transmutes.html): "Extending a lifetime or shortening an invariant lifetime is advanced, very unsafe Rust" — produces dangling refs at runtime | Design ownership; or use `Arc` to share; or accept the borrow constraint | — |
| 9.3 | Raw pointer aliasing — `&mut T` while `*mut T` exists pointing to the same data | UB: aliasing rules apply to `&mut` exclusively, but interaction with raw pointers under Stacked Borrows / Tree Borrows is subtle | Single source of `&mut` access; use `UnsafeCell` for interior mutability through pointers; run Miri to catch | — |
| 9.4 | Creating `&mut T` from `*mut T` while another `&T` to the same data exists | Same — `&` and `&mut` may not co-exist | Reborrow tracking; consider `core::cell::UnsafeCell` if interior mutability is genuinely needed | — |
| 9.5 | Sending `!Send` across threads via `unsafe impl Send` | Type might use `Rc`, `Cell`, or thread-local under the hood — sending corrupts state | Make a `Send` newtype; or wrap in `Mutex`; never just `unsafe impl Send` without a SAFETY comment proving why | — |
| 9.6 | Breaking `UnsafeCell` invariants (e.g. constructing `&UnsafeCell<T>` then `&mut T` via `.get()` while another `&T` exists) | UnsafeCell is the **only** legal way to mutate through `&` — but it doesn't auto-prevent aliasing | Borrow-rule manually; `Cell`/`RefCell`/`Mutex` (safe wrappers) preferred | — |
| 9.7 | `Pin` invalidation — moving a structurally-pinned value via `Pin::get_unchecked_mut` | UB: pinned values cannot be moved; futures, intrusive lists, self-refs all break | `pin-project` for the projection rules; don't expose `&mut` to pinned fields | — |
| 9.8 | FFI panic propagation — Rust panic crossing into C | UB: panics unwinding into C-ABI frames | `std::panic::catch_unwind` at every FFI boundary; convert to error code | — |
| 9.9 | `Vec::from_raw_parts(ptr, len, cap)` with wrong allocator / layout | UB: the global allocator must own the pointer; mismatched cap → free with wrong size class | Only pair with `Vec::into_raw_parts` (or `into_boxed_slice` + `Box::into_raw`); never construct from `malloc()` pointers | — |
| 9.10 | `MaybeUninit::assume_init` before all fields are initialized | UB: reads uninitialized memory | Use `MaybeUninit::write` for each field; track init state in your own bookkeeping; assume_init only when proven complete | — |
| 9.11 | `Vec::set_len(n)` without having written to those slots | UB: future reads are uninitialized | Only `set_len` after writing via `ptr::write` to `n` slots; or use `Vec::resize_with` for safe init | — |
| 9.12 | `slice::from_raw_parts(ptr, len)` with `len` exceeding the underlying allocation | UB: out-of-bounds read | Track exact len at the source; consider `slice::from_raw_parts_mut` only with proof that no other access exists | — |
| 9.13 | `unsafe` block with no `// SAFETY:` comment | Reviewers can't verify; "unsafe rot" sets in | Mandatory `// SAFETY: <invariant proven here>` for every `unsafe` block — enforced by `clippy::undocumented_unsafe_blocks` | `clippy::undocumented_unsafe_blocks` |
| 9.14 | Holding raw pointer across realloc-capable Vec operations | After `vec.push`/`vec.reserve`, prior `vec.as_ptr()` may dangle | Re-derive pointers after any operation that can grow capacity | — |
| 9.15 | `transmute::<Vec<&i32>, Vec<Option<&i32>>>(v)` | Per the [Nomicon](https://doc.rust-lang.org/nomicon/transmutes.html): "Transmuting between types like `Vec<&i32>` and `Vec<Option<&i32>>` can result in Undefined Behavior" — `Option<&T>` is niche-optimized to be the same size, but `Vec`'s internal cap may differ | Map element-wise; don't transmute container generics | — |
| 9.16 | `Box::from_raw(ptr)` on a pointer not from `Box::into_raw` | UB: deallocator mismatch | Only pair with `into_raw`; document every FFI ownership transfer | — |
| 9.17 | `static mut` for global state | Per [the Rust footgun list](https://gist.github.com/ErnWong/f5c1e915a4defd32e3cdeb5693ab8062): "`static mut` is a footgun" — multiple paths to obtain `&mut`, aliasing UB | `LazyLock<Mutex<T>>` or `OnceLock<T>` (1.70+); `static mut` is deprecated in Edition 2024 | — |
| 9.18 | `transmute` to convert function pointers between calling conventions | UB unless ABIs match exactly | Use a thunk function; or `extern "C" fn` wrappers | — |
| 9.19 | Casting `*const T` → `*mut T` to bypass `&` borrow rules | UB if any other `&T` exists — defeats the entire memory model | Restructure; if you need shared mutation, use `Cell`/`RefCell`/`Mutex` | — |
| 9.20 | `unsafe fn` exposed publicly without documenting the contract | Users invoke unsafely with no idea what invariants they must uphold | Mandatory `# Safety` doc section listing every caller obligation | `clippy::missing_safety_doc` |

### 9.A Mandatory SAFETY comment template

```rust
// SAFETY:
// - `ptr` was returned by `Box::into_raw` from the matching `Box::<T>::new` call.
// - No other reference / pointer to `*ptr` exists at this point.
// - We have exclusive ownership and are about to transfer it.
let boxed = unsafe { Box::from_raw(ptr) };
```

### 9.B Transmute footgun — same layout ≠ legal transmute

```rust
// BAD — Foo and Bar have identical layouts BUT no repr(transparent) bridge
struct Foo { a: u32, b: u32 }
struct Bar { c: u32, d: u32 }
let f = Foo { a: 1, b: 2 };
let b: Bar = unsafe { std::mem::transmute(f) };   // UB: layouts are unspecified

// GOOD — repr(C) or repr(transparent), and bytemuck for plain-old-data
#[repr(C)] struct Foo { a: u32, b: u32 }
#[repr(C)] struct Bar { c: u32, d: u32 }
// SAFETY: both are repr(C) with identical field types/order — same layout.
let b: Bar = unsafe { std::mem::transmute(f) };

// BETTER — bytemuck derives the safety obligation away
#[derive(bytemuck::Pod, bytemuck::Zeroable, Clone, Copy)]
#[repr(C)] struct Foo { a: u32, b: u32 }
#[derive(bytemuck::Pod, bytemuck::Zeroable, Clone, Copy)]
#[repr(C)] struct Bar { c: u32, d: u32 }
let b: Bar = bytemuck::cast(f);   // safe, checked at compile time
```

### 9.C FFI panic propagation

```rust
// BAD — panic crossing into C is UB
#[no_mangle]
pub extern "C" fn rust_callback(x: i32) -> i32 {
    if x < 0 { panic!("negative") }   // ← UB: unwinds into C ABI
    x * 2
}

// GOOD — catch_unwind at the boundary, return sentinel
#[no_mangle]
pub extern "C" fn rust_callback(x: i32) -> i32 {
    let result = std::panic::catch_unwind(|| {
        assert!(x >= 0, "negative");
        x * 2
    });
    result.unwrap_or(-1)   // sentinel value the C caller checks
}
```

---

## 10. Cargo / Dependency Pitfalls

Sources: [Cargo Book: features](https://doc.rust-lang.org/cargo/reference/features.html), [Cargo Workspace Feature Unification Pitfall](https://nickb.dev/blog/cargo-workspace-and-the-feature-unification-pitfall/), [SemVer Compatibility reference](https://doc.rust-lang.org/cargo/reference/semver.html). See also [`rust-best-practices.md §3-§4`](./rust-best-practices.md#3-project-structure--cargo-workspaces) for workspace patterns and the 2026 toolchain matrix.

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 10.1 | `foo = "*"` version spec | Unbounded major-version drift; one `cargo update` away from breakage | Pin minimum: `foo = "1.2"` (means `>=1.2.0, <2.0.0`); for libraries, the minimum should be the lowest version you've tested with | — |
| 10.2 | Mutually exclusive feature flags (`feature_a` disables `feature_b`) | Violates Cargo's additive-features contract — `cargo build --all-features` fails; downstream crates that enable both get cryptic errors. Per [the Cargo Book](https://doc.rust-lang.org/cargo/reference/features.html#feature-unification) | Features must be additive. Use separate crates for the exclusive choice; or runtime config | — |
| 10.3 | Enabling `default-features` of a heavy dep when you only need one feature | Pulls in everything — bloat, transitive deps, sometimes platform-specific code that breaks builds | `chrono = { version = "0.4", default-features = false, features = ["clock"] }` | — |
| 10.4 | Transitive duplicate crate versions (two `rand` majors) | Bigger binary, longer compile, sometimes runtime conflict (e.g. global thread RNG state) | `cargo tree -d` to find; upgrade lowest matchers; fork if necessary | — |
| 10.5 | Workspace dep inherited as `{ workspace = true }` but consumer wants different features | Per the [workspace feature pitfall](https://nickb.dev/blog/cargo-workspace-and-the-feature-unification-pitfall/): features are union — you can't subtract | Define base in workspace, opt-in additional features in member crate. Or split into two deps | — |
| 10.6 | Missing `[package.metadata.docs.rs]` for libraries published with features | docs.rs builds without your features, docs are wrong | `[package.metadata.docs.rs] all-features = true` or selective | — |
| 10.7 | No `rust-version = "1.85"` declared | Users on older toolchains get cryptic errors mid-compile | Set `rust-version` to the lowest MSRV you support; bumping it is a semver consideration | — |
| 10.8 | Publishing without `cargo publish --dry-run` | Path-deps to local crates, missing `include`/`exclude`, files >10MB rejected mid-publish | Always dry-run; also `cargo package --list` to inspect | — |
| 10.9 | `build.rs` that hits the network | Reproducibility ruined; offline / sandboxed builds fail; supply-chain risk | Vendor required artifacts; document inputs in `Cargo.toml [build-dependencies]`; never `curl` in build.rs | — |
| 10.10 | `[dependencies] foo = { path = "../foo" }` published to crates.io | Path overrides ignored on publish — but local dev uses path, crates.io users get registry version. Drift between dev and publish | Use `[patch.crates-io]` for local override during dev; publish only with version spec | — |
| 10.11 | No `Cargo.lock` committed for a binary crate | Reproducible builds broken — every CI run resolves fresh | `Cargo.lock` checked in for binaries, gitignored for libraries (historically; modern guidance: commit for both, regenerate as needed) | — |
| 10.12 | `default-features = true` with overlapping features across workspace members causing feature unification surprises | Member A enables `serde` feature on `foo`; member B doesn't — but build of A's bin includes B's `foo` with serde unintentionally | Use `resolver = "2"` (default in Edition 2021+); audit `cargo tree -e features` | — |
| 10.13 | `cargo install` for project-level CLI tooling | Each developer might have different versions; CI may fail | `cargo install --locked` or pin via [cargo-binstall](https://github.com/cargo-bins/cargo-binstall) + `rust-toolchain.toml`; or use `cargo run --bin tool` | — |
| 10.14 | Yanking a published version without a replacement | Downstream solvers may resolve to yanked anyway with warning; broken transitive deps in non-locked builds | Yank only after publishing a fixed patch version; communicate in CHANGELOG | — |
| 10.15 | Massive feature flag matrix (`feature_a + feature_b + feature_c × 10 combos`) | CI can't realistically test all; consumers hit unbuildable combos | Reduce to ≤ ~5 independent features; explicit `[features] full = ["a", "b", "c"]` for "everything" | — |
| 10.16 | Optional dep without corresponding feature gate | `optional = true` but no `feature = ["dep:..."]` — dep is pulled by anyone who depends on you | `[features] foo = ["dep:foo-crate"]` and gate code with `#[cfg(feature = "foo")]` | — |
| 10.17 | `[lib] crate-type = ["cdylib", "rlib"]` for what should be a normal lib | Doubles compile time; `cdylib` is for FFI consumers only | Only `cdylib` when you need a `.so`/`.dll`/`.dylib` for C/Python/etc | — |
| 10.18 | Using `git` deps (`foo = { git = "..." }`) in published crates | Forbidden on crates.io (rightly); local-only dev pattern bleeds into publish | Fork to crates.io if you need a patch; or vendor; never `git` dep in published code | — |

---

## 11. Testing Pitfalls

Sources: [A Preliminary Study of Fixed Flaky Tests in Rust Projects on GitHub (arxiv 2502.02760)](https://arxiv.org/html/2502.02760v1), [Tokio testing topics](https://tokio.rs/tokio/topics/testing). For the seven-layer testing strategy (rstest, proptest, insta, testcontainers, wiremock, cargo-fuzz, miri, cargo-mutants), see [`rust-best-practices.md §5`](./rust-best-practices.md#5-testing-strategy--the-seven-layers).

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 11.1 | Tests sharing global state via `static mut` / `lazy_static!` | Parallel `cargo test` reorders; tests pass alone, fail together | Per-test setup; or `serial_test::serial`; or scoped fixtures | — |
| 11.2 | Tests that depend on execution order | Same root cause; nextest randomizes by default | Independent tests; init / teardown idempotent | — |
| 11.3 | `tokio::time::sleep` in tests as a synchronization mechanism | Flaky under load — passes locally, fails in CI | `tokio::time::pause()` + advance manually; or `tokio::sync::Notify` for explicit synchronization | — |
| 11.4 | Snapshot tests on `HashMap` iteration order | Rust randomizes HashMap order per program startup — snapshot drifts | `BTreeMap` for deterministic order; or `insta::assert_yaml_snapshot!` (sorts keys) | — |
| 11.5 | Snapshot tests including timestamps / UUIDs / random IDs | Drift on every run | `insta::assert_snapshot!(@r"<filter>")` with redactions; or `insta_filters` macro for regex normalization | — |
| 11.6 | `.unwrap()` in test bodies that masks the actual failure | Backtrace points to unwrap, not to the test assertion that should have caught it | `assert_eq!(actual, expected, "context")` with messages; `expect("clear context")` if unwrap is unavoidable | — |
| 11.7 | `#[ignore]` accumulation | Tests rot, eventually the suite is "100% passing" but only because 30% is ignored | Issue tracker reference required on every `#[ignore]`; periodic audit; CI gate "no new ignores without ticket" | — |
| 11.8 | No negative tests (only happy path) | Bugs in error handling go uncaught | Mandatory error-case tests; property tests on parse-then-validate | — |
| 11.9 | Mocking internal collaborators instead of boundaries | Tests assert on call patterns, break on refactors | Mock external services (HTTP, DB) at the trait boundary; let internal code flow naturally | — |
| 11.10 | `#[tokio::test]` with `flavor = "current_thread"` for tests that actually need multi-thread (e.g. testing `Send` futures) | Compile passes but test doesn't validate the threading invariant | `#[tokio::test(flavor = "multi_thread", worker_threads = 4)]` when testing concurrency | — |
| 11.11 | Integration tests that hit real services | Flaky, slow, may corrupt prod data | Mock at HTTP level (`wiremock`, `mockito`); record/replay via `vcr`-style tools | — |
| 11.12 | `assert!(result.is_ok())` instead of `result.unwrap()` or pattern match | Loses the error info — test failure says "left: false right: true" with no clue | `let Ok(v) = result else { panic!("expected Ok, got {:?}", result) };` — or `assert!(matches!(result, Ok(_)), "got {:?}", result)` | `clippy::assertions_on_result_states` |
| 11.13 | `cargo test --release` only | Most builds are debug; debug-only `debug_assert!`s + overflow checks don't run in release | Run both `cargo test` and `cargo test --release` in CI; default debug for quick iteration | — |
| 11.14 | `#[should_panic]` without message specification | Test passes if *any* panic happens — including panics from setup, not the code under test | `#[should_panic(expected = "specific message")]` | — |
| 11.15 | Property tests with poor shrinking (`proptest! { fn p(x: Vec<i32>) ... }`) | Failures report huge unreadable inputs | Use generators with bounded sizes (`prop::collection::vec(0..100, 0..50)`); commit `proptest-regressions/` to lock in shrinks | — |
| 11.16 | `criterion` benchmarks committed without baseline saved | Can't tell if a perf regression is real | `cargo bench -- --save-baseline main` then compare; commit a perf-budget file | — |
| 11.17 | `#[test]` async fn without `#[tokio::test]` | Test compiles but doesn't run — silently skipped or "doesn't await" warnings | `#[tokio::test]` (or equivalent for other runtimes) | — |
| 11.18 | Tests that depend on the system clock (`SystemTime::now()`) | Fail on slow CI; daylight saving; year rollover | Inject a clock trait: `trait Clock { fn now(&self) -> Instant; }`; in tests use a `FakeClock` | — |
| 11.19 | Tests that bind to a hardcoded port | CI parallelism → "Address already in use" flake | Bind to `:0` and read the actual port from the listener | — |
| 11.20 | Test fixtures with non-deterministic IDs (UUIDs) leaking into assertions | Snapshot drift; cross-test contamination | Use deterministic seeds (`uuid::Uuid::from_u128(1)`); or test-scoped IDs via builders | — |

---

## 12. Security Pitfalls

Sources: [Pitfalls of Safe Rust (corrode)](https://corrode.dev/blog/pitfalls-of-safe-rust/), [Rust Security Handbook](https://github.com/yevh/rust-security-handbook), [What 44 CVEs Tell You About Rust's Safety Boundary](https://dev.to/arthurpro/what-44-cves-tell-you-about-rusts-safety-boundary-2cl7). For the constructive secret-handling and TLS stack, see [`rust-best-practices.md §7`](./rust-best-practices.md#7-security-practices).

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 12.1 | `.unwrap()` on parsed user input | Panic = DoS. Per corrode: "Every unwrap, expect, slice index, and unchecked arithmetic operation in input-handling code is a potential denial of service" | Validate at the boundary; return error; reject malformed | `clippy::unwrap_used` |
| 12.2 | Logging secrets via `tracing::info!("token: {token}")` | Tokens, API keys, PII end up in logs / log shippers / SaaS observability vendors | `secrecy::Secret<String>` (which excludes itself from Debug/Display); `zeroize` for in-memory wipe; log only redacted fingerprints | — |
| 12.3 | No `Drop` zeroize for in-memory secrets | Decommissioned heap pages may contain key material until reuse | `zeroize::Zeroize` derive + `ZeroizeOnDrop`; `secrecy::SecretBox` wrapper | — |
| 12.4 | TOCTOU between `Path::exists()` then `File::open()` | Per [Pitfalls of Safe Rust](https://corrode.dev/blog/pitfalls-of-safe-rust/): "TOCTOU on path operations is the largest cluster of vulnerabilities in recent audits" — attacker can swap the path between check and use | Open and check atomically: `File::open` returns `Err(NotFound)` if missing; use `OpenOptions::create_new(true)` to atomically fail if exists; use `openat`/`O_NOFOLLOW` via `cap-std` crate for sandboxed file access | — |
| 12.5 | `Command::new("sh").arg(format!("rm {}", user_input))` | Classic command injection — `;` / `&&` in user input | `Command::new("rm").arg(user_path)` — separate args, no shell. Never `sh -c` with interpolated input | — |
| 12.6 | Deserializing untrusted YAML / TOML / Bincode | YAML in particular: aliases can construct enormous structures (billion-laughs); Bincode trusts size prefixes | Use JSON for untrusted input (no aliases, simple grammar); set size limits on parser; consider `serde_json::de::from_reader` with a length-limited reader | — |
| 12.7 | Unbounded `regex::Regex::find` on attacker input | Per the [regex crate docs](https://docs.rs/regex): "The regex crate considers DoS with untrusted patterns a security vulnerability only if time is not linear" — meaning **patterns from users are unbounded** even if the engine is linear in pattern size × input | If pattern from user: `RegexBuilder::size_limit` + `dfa_size_limit`; reject patterns over a length budget; consider `regex-lite` for tighter resource bounds | — |
| 12.8 | `serde::Deserialize` for domain types that have invariants | Invariants bypassed: a `NonZero<u32>` field actually got 0 from JSON | Deserialize into a `Dto` struct, then `TryFrom<Dto>` enforces invariants (see [API Design pitfall 13.20](#13-api-design-pitfalls)) | — |
| 12.9 | Integer arithmetic without overflow handling on attacker-influenced values | Debug: panic. Release: wraps. Either is exploitable | `checked_add` / `saturating_add` / `wrapping_add` explicitly; enable `overflow-checks = true` in release for security-critical crates | `clippy::arithmetic_side_effects` |
| 12.10 | `tokio::time::timeout` missing on outbound HTTP / RPC calls | Slow / hung remote ⇒ exhausted task pool ⇒ DoS | Wrap every external call in `timeout(d, fut)`; tune `d` per dependency | — |
| 12.11 | Constant-time comparison for secrets via `==` | `==` short-circuits on first mismatch → timing leak of secret length and prefix | `subtle::ConstantTimeEq::ct_eq` for tokens, MACs, password hashes | — |
| 12.12 | Random secrets via `rand::thread_rng()` | Per [`rand` 0.9+](https://docs.rs/rand/latest/rand/) docs: `ThreadRng` is fine for general use, but for crypto-grade you want `OsRng` / `getrandom` | `getrandom::getrandom(&mut bytes)?` for crypto seeds; `rand::rngs::OsRng` for `Rng` interface | — |
| 12.13 | Panic-free crate with `slice[idx]` indexing on parsed input | Out-of-bounds → panic → DoS | `slice.get(idx).ok_or(Err::OutOfBounds)?`; `clippy::indexing_slicing` to enforce | `clippy::indexing_slicing` |
| 12.14 | Path traversal: `Path::new("/data").join(user_input)` | If `user_input = "../../etc/passwd"`, `join` resolves it | Canonicalize: `let p = base.join(user).canonicalize()?; if !p.starts_with(base) { return Err(...) }`; or strip path components manually; use `cap-std::Dir` for capability-based FS | — |
| 12.15 | XML / HTML output via string interpolation | XSS / injection | Use `askama` / `tera` / `maud` which escape by default; explicit `html_escape::encode_text` for raw output | — |
| 12.16 | Trusting `Content-Length` to allocate (`Vec::with_capacity(content_length)`) | Attacker says 4 GB → OOM crash | Cap allocation: `Vec::with_capacity(content_length.min(MAX_BODY))`; or stream-process with a budget | — |
| 12.17 | `tokio::sync::Semaphore::new(usize::MAX)` for rate limiting | "Unlimited" semaphore = no rate limit | Use a real rate-limit crate (`governor`); semaphores cap concurrent count, not rate | — |
| 12.18 | Forgetting `#[derive(Zeroize)]` on a struct containing a `Vec<u8>` secret | `Drop` doesn't wipe the heap memory | `#[derive(Zeroize, ZeroizeOnDrop)]` on the struct | — |
| 12.19 | `unwrap` on `env::var("API_KEY")` at startup | Panic with backtrace exposes the env var name to anyone reading stderr | `env::var("API_KEY").map_err(\|_\| AppErr::MissingEnv)?` — error without leaking the value (which is `Err` here anyway, but the pattern matters for `expect` calls) | — |
| 12.20 | `Debug` derive on a struct containing secrets | `{:?}` prints them in logs / panics | Manual `Debug` impl that redacts; `secrecy::Secret<T>` (default-redacts) | — |

### 12.A TOCTOU safe pattern

```rust
// BAD
if path.exists() {                  // T = time of check
    let f = File::open(path)?;      // U = time of use; attacker swapped here
}

// GOOD
match File::open(path) {            // single syscall, atomic
    Ok(f)  => process(f)?,
    Err(e) if e.kind() == ErrorKind::NotFound => create_default()?,
    Err(e) => return Err(e.into()),
}
```

### 12.B Secret handling

```rust
use secrecy::{Secret, ExposeSecret};
use zeroize::Zeroize;

#[derive(Zeroize, ZeroizeOnDrop)]
struct Credentials {
    username: String,
    password: Secret<String>,   // not in Debug, zeroed on drop
}

// At use site, narrow exposure:
fn auth(creds: &Credentials) -> Result<Token, AuthErr> {
    let p = creds.password.expose_secret();
    verify(&creds.username, p)        // p borrow ends here
}
```

### 12.C Command injection — separate args, no shell

```rust
// BAD — shell metacharacters in user_input can execute arbitrary commands
let output = Command::new("sh")
    .arg("-c")
    .arg(format!("convert {} out.png", user_input))     // ← injection
    .output()?;

// GOOD — separate args, no shell interpolation
let output = Command::new("convert")
    .arg(user_input)            // ← passed as a single argv slot, no shell parsing
    .arg("out.png")
    .output()?;
```

### 12.D Path traversal prevention

```rust
// BAD — user_input = "../../etc/passwd" escapes the base
let path = Path::new("/var/data").join(user_input);
let content = fs::read(path)?;

// GOOD — canonicalize and verify containment
fn safe_join(base: &Path, user: &str) -> Result<PathBuf, FsError> {
    let candidate = base.join(user).canonicalize()?;
    let base      = base.canonicalize()?;
    if !candidate.starts_with(&base) {
        return Err(FsError::PathEscape);
    }
    Ok(candidate)
}

// BEST — capability-based FS via cap-std (no traversal possible by construction)
use cap_std::fs::Dir;
let base = Dir::open_ambient_dir("/var/data", cap_std::ambient_authority())?;
let f = base.open(user_input)?;   // can't escape `base` regardless of input
```

---

## 13. API Design Pitfalls

Sources: [SemVer Compatibility (Cargo Book)](https://doc.rust-lang.org/cargo/reference/semver.html), [predr.ag's tooling/breakage post](https://predr.ag/blog/semver-in-rust-tooling-breakage-and-edge-cases/), [RFC 1105: API Evolution](https://rust-lang.github.io/rfcs/1105-api-evolution.html). The full C-* checklist this list complements lives in [`rust-best-practices.md §1`](./rust-best-practices.md#1-rust-api-guidelines--full-c--checklist).

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 13.1 | Re-exporting transitive dep types in public API (`pub use reqwest::Client`) | Consumers pin to your version of `reqwest`; bumping it is a major break of *your* crate. Per predr.ag: "1 in 6 of the top 1000 Rust crates has violated semantic versioning at least once" — this is a common cause | Wrap in a newtype: `pub struct HttpClient(reqwest::Client)`. Re-export only types you own. If you must expose the underlying type, document the semver coupling | — |
| 13.2 | Too-broad `pub` (everything is `pub`) | Every public item is a semver commitment. Hidden impl detail leaks become required | Default to `pub(crate)`; `pub` only on intentional surface. Audit with `cargo public-api` | — |
| 13.3 | Missing `#[must_use]` on `Builder::build()` / `Iterator`-returning fns / `Result`-likes | Consumers call the method, discard the result, code does nothing | `#[must_use = "this Builder must be built"]` / `#[must_use = "iterators are lazy"]` | `clippy::must_use_candidate` |
| 13.4 | No `#[non_exhaustive]` on a public enum that will grow | Per the [Cargo book SemVer reference](https://doc.rust-lang.org/cargo/reference/semver.html): adding a variant to a non-`#[non_exhaustive]` enum is a major break — caught the Rust community hundreds of times in the top 1000 crates | Mark `#[non_exhaustive]` from 1.0 if growth is expected; the cost is callers can't match exhaustively (and must use `_`) | — |
| 13.5 | Adding `#[non_exhaustive]` to an existing public enum/struct | Per the [Cargo SemVer rules](https://doc.rust-lang.org/cargo/reference/semver.html#non-exhaustive): "Adding `#[non_exhaustive]` to an existing struct, enum, or variant is almost always a breaking change" | Plan attribute from 1.0; if added later, treat as major version bump | — |
| 13.6 | Builder that takes `&mut self` and returns `&mut Self` instead of `self` | Forces builders to live in a local; can't chain on a temporary; awkward when ownership transitions to `build()` | Take `self`, return `Self`; or take `&mut self`, return `&mut Self`, but never mix the two patterns in one builder | — |
| 13.7 | Adding a required arg to an existing fn | Breaking change for all callers | Add as optional via `Option<T>` parameter; or use a config struct; or introduce `fn_v2()` and deprecate the old | — |
| 13.8 | Public struct with all `pub` fields (`pub struct Config { pub a: u32, pub b: String }`) | Any field addition breaks struct-literal construction at call sites | Either: `#[non_exhaustive]` + builder; or `Config::new(a, b).with_c(c)`; or accept struct-literal construction means commitment | — |
| 13.9 | `impl Iterator for Foo` without `impl IntoIterator for &Foo` | Users can iterate by value but not by reference; ergonomic gap | Implement both; or use the `for &Foo` / `for &mut Foo` pattern | — |
| 13.10 | Returning `Box<dyn Iterator<Item = T>>` from public fn | Forces vtable dispatch on every `.next()` call; consumers can't compose efficiently | Return `impl Iterator<Item = T>` (RPIT) — keeps it generic and inlines | — |
| 13.11 | Generic `T` with `where T: Clone + Send + Sync + 'static` (over-constrained) | Locks out reasonable types; per [LogRocket overconstrained APIs](https://blog.logrocket.com/improving-overconstrained-rust-library-apis/): unnecessary `Clone` is a common cause | Add only the bounds your impl uses. If you don't clone in the body, don't require `Clone` | `clippy::needless_pass_by_value` (related) |
| 13.12 | Library exposes `&str` everywhere, consumer needs `Cow<'_, str>` | Each conversion costs a copy | Accept `impl Into<Cow<'_, str>>` for "borrow if you can, own if you must" | — |
| 13.13 | Adding a default method to a public trait without `Self: Sized` consideration | If method uses `Self` by value, it breaks `dyn Trait` impls (object safety) | Audit object safety; use `where Self: Sized` for methods that shouldn't be on trait objects | — |
| 13.14 | Public method named `unwrap` / `expect` (collision with `Result`/`Option`) | Shadows std methods at the call site → cryptic errors | Rename: `into_inner`, `inner_unchecked`, `unwrap_inner` | — |
| 13.15 | Returning iterator that captures a lifetime that should have been elided (`fn iter(&self) -> impl Iterator<Item = &T> + 'static`) | `'static` excludes references to `self` — wrong | `fn iter(&self) -> impl Iterator<Item = &T> + '_` | — |
| 13.16 | Re-exporting a macro without matching its imports | Macros use `$crate` but rely on the consumer's import paths — re-export breaks unless `pub use` from the same path | `pub use crate::my_macro` plus document the import; or use proc-macro with `#[macro_export]` | — |
| 13.17 | Public function with > 4 positional parameters | Call sites become unreadable, easy to swap | Config struct + builder; or named-args proc macro | `clippy::too_many_arguments` |
| 13.18 | `Default::default()` impl returning a partially-valid state | Consumers `Foo::default()` then forget to set required fields → runtime errors | If a meaningful default doesn't exist, don't impl `Default`; require explicit constructor | — |
| 13.19 | Public type with `pub fn new() -> Self` but no `Default` impl (when the new takes no args) | Inconsistent — users do `Foo::new()` here, `Bar::default()` there | If `new()` takes no args, implement `Default` for it; `clippy::new_without_default` flags this | `clippy::new_without_default` |
| 13.20 | `impl Deserialize for DomainEntity` directly | Bypasses invariants (negative ages, empty names) at the deserialization boundary | DTO pattern: `#[derive(Deserialize)] struct DomainEntityDto { ... }` + `impl TryFrom<DomainEntityDto> for DomainEntity { type Error = ValidationError; ... }` | — |
| 13.21 | Trait with associated constants that vary widely across impls | Const fields can't be made `const fn` post-hoc; changing values is a break | Use methods instead for non-trivially-shared values | — |
| 13.22 | `pub mod internal` that's not really internal | Users find it, use it, you can't remove it without major bump | `#[doc(hidden)] pub mod __internal` for compiler-visible-but-not-public; document instability | — |
| 13.23 | Async fn in public trait without considering Send-ness | Per [baby steps' Send-bounds posts](https://smallcultfollowing.com/babysteps/blog/2023/02/01/async-trait-send-bounds-part-1-intro/): some consumers need `Send` futures (for `tokio::spawn`), some don't | For libraries, prefer `async-trait` until the language stabilizes Send-aware async-fn-in-traits; or expose `impl Future + Send` manually | — |

### 13.A Newtype wrapper for re-export

```rust
// BAD — leaks reqwest's semver into yours
pub use reqwest::Client;   // bump reqwest 0.11 → 0.12 = your major bump

// GOOD — wrap, keep your API stable across reqwest versions
pub struct HttpClient {
    inner: reqwest::Client,
}
impl HttpClient {
    pub fn new() -> Self { Self { inner: reqwest::Client::new() } }
    pub async fn get(&self, url: &str) -> Result<String, HttpError> {
        self.inner.get(url).send().await?.text().await.map_err(Into::into)
    }
}
```

### 13.B DTO pattern for invariant-preserving deserialization

```rust
#[derive(Deserialize)]
struct UserDto {
    name: String,
    age: i32,
}

pub struct User {
    name: String,
    age: u8,        // ← invariant: 0..=120
}

impl TryFrom<UserDto> for User {
    type Error = ValidationError;
    fn try_from(d: UserDto) -> Result<Self, Self::Error> {
        if d.name.is_empty() { return Err(ValidationError::EmptyName); }
        let age = u8::try_from(d.age)
            .ok()
            .filter(|&a| a <= 120)
            .ok_or(ValidationError::BadAge)?;
        Ok(User { name: d.name, age })
    }
}
```

---

## 14. WASM / Embedded / `no_std` Pitfalls

Sources: [The Embedded Rust Book — Panicking](https://docs.rust-embedded.org/book/start/panicking.html), [Cloudflare's making Rust Workers reliable](https://blog.cloudflare.com/making-rust-workers-reliable/), [`no_std` Playbook](https://hackmd.io/@alxiong/rust-no-std). For the std / alloc / core split and target triples, see [`rust-language-spec.md §9`](./rust-language-spec.md#9-no_std-and-embedded).

| # | Anti-pattern | Why it bites | Fix | Clippy |
|---|---|---|---|---|
| 14.1 | `use std::*` in a `#![no_std]` crate | Link errors at the consumer; `core::*` is the right import root for primitives, `alloc::*` for heap | `use core::...` for primitives, `extern crate alloc; use alloc::...` for heap collections | `clippy::std_instead_of_core` |
| 14.2 | `panic = "unwind"` in embedded (default Cargo.toml) | Embedded targets often have no unwinder — link fails, or runtime aborts mid-unwind. Per [Embedded Book](https://docs.rust-embedded.org/book/start/panicking.html): unwinding is rarely available on bare-metal | `[profile.release] panic = "abort"` — and provide a `panic-handler` (e.g. `panic-halt`, `panic-probe`) | — |
| 14.3 | `thread_local!` in WASM | WASM has one thread; many targets compile but TLS init is subtle, and atomics/threads-aware WASM features change semantics | `static` for global single-thread state on WASM; `LazyLock` (now via `std` 1.80+) where appropriate | — |
| 14.4 | `std::time::Instant::now()` in WASM | Per `instant` crate docs: WASM's `Instant::now()` panics or returns wrong values pre-monotonic-clock browser support | Use the `instant` crate (drop-in for `std::time::Instant` that works on wasm32-unknown-unknown); or `web_time` / `web-sys::Performance::now()` | — |
| 14.5 | `std::collections::HashMap` in `no_std` | Not available in `core` or `alloc` (needs `std::collections::hash_map::RandomState`) | `hashbrown::HashMap` (drop-in, `no_std` compatible) | — |
| 14.6 | `lto = "fat"` on small embedded targets | Memory-hungry — small build machines OOM during link | `lto = "thin"`; or `lto = false` and rely on `-C codegen-units=1` | — |
| 14.7 | `panic = "abort"` without a global allocator on `no_std` | Each panic leaks the panic-info infrastructure; or there's no formatter — cryptic abort with no message | `defmt` / `defmt-rtt` for log output; `panic-probe` to forward over debugger | — |
| 14.8 | Async code on WASM with `tokio` | tokio depends on threads, mio — incompatible with `wasm32-unknown-unknown` | `wasm-bindgen-futures::spawn_local`; or `async-executor` single-threaded; or `worker::send::SendWrapper` for Cloudflare Workers | — |
| 14.9 | `std::panic::catch_unwind` on `wasm32-unknown-unknown` (panic=abort target) | No-op — the panic still aborts. Per Cloudflare's article on [making Rust Workers reliable](https://blog.cloudflare.com/making-rust-workers-reliable/): catch_unwind in panic=abort doesn't recover | Use `wasm32-unknown-emscripten` (has unwinder) — but heavyweight; or compile with `panic=unwind` once browser exception-handling support stabilizes | — |
| 14.10 | Large `Vec` allocation on embedded with `#[global_allocator]` | Heap fragments, eventual `AllocError` mid-execution | Pre-allocate at boot; or use `heapless::Vec<T, N>` (stack-allocated bounded vec) | — |
| 14.11 | `format!("{}", x)` on embedded — pulls `core::fmt` | `core::fmt` is massive — adds ~80 KB to binary | `ufmt` for minimal formatting; or `defmt` (logger-side formatting) | — |
| 14.12 | `std::sync::Mutex` in `no_std` | Doesn't exist | `spin::Mutex` or `critical-section::Mutex` (interrupt-disabling) for bare-metal | — |
| 14.13 | WASM module that exposes `panic` via `console.error` from inside a request | Recursive panic if console isn't available (e.g. in Cloudflare Workers without `console` binding) | Use `console_error_panic_hook` only in dev; in prod, return a structured error response | — |
| 14.14 | `wasm-bindgen` 0.2 with default features on size-critical builds | Pulls `wee_alloc`, `console_error_panic_hook` — bloat | `default-features = false`; opt into only what you need | — |
| 14.15 | Floating-point on no_FPU embedded (e.g. cortex-m0) | Soft-float pulls KB of code; multiplication is slow | `fixed` crate for fixed-point; or `libm` for explicit soft-float | — |
| 14.16 | `assert!`/`debug_assert!` left enabled in shipped firmware | Each assert pulls a panic-info string — bloats binary | `[profile.release] debug-assertions = false` (default); strip strings via `panic-immediate-abort` | — |
| 14.17 | `Box::leak` on embedded for "permanent" allocs | Heap grows monotonically; on long-running embedded, eventually exhausts | Use `static mut` with `MaybeUninit` (unsafe but bounded); or `cortex-m-rt`'s `#[init]` for once-only static init | — |
| 14.18 | Generic functions with many monomorphizations on embedded | Flash blows out from code bloat | `Box<dyn Trait>` (with allocator) or hand-erase via function pointer; design for monomorphization budget | — |

---

## Cross-Cutting Clippy Lint Quick Reference

The following lints are worth enabling in nearly every Rust project. Many are `allow` by default (pedantic, restriction) — opt in via `Cargo.toml`:

```toml
[lints.clippy]
# correctness — should already be deny
unwrap_used = "warn"             # §5.3
expect_used = "warn"             # §5.3
panic_in_result_fn = "warn"      # §5.4
await_holding_lock = "deny"      # §4.3
await_holding_refcell_ref = "deny"  # §4.5
arc_with_non_send_sync = "deny"

# performance
redundant_clone = "warn"         # §6.1
needless_pass_by_value = "warn"  # §1.10
needless_collect = "warn"        # §1.8
result_large_err = "warn"        # §6.19
large_enum_variant = "warn"      # §6.19
regex_creation_in_loops = "warn" # §6.17

# correctness/style
ptr_arg = "warn"                 # §1.9
must_use_candidate = "warn"      # §13.3
new_without_default = "warn"     # §13.19
result_unit_err = "warn"         # §3.11
match_bool = "warn"              # §3.14
wildcard_enum_match_arm = "warn" # §3.5

# pedantic — selectively
cast_possible_truncation = "warn" # §3.9
cast_sign_loss = "warn"          # §3.9
cast_lossless = "warn"
cloned_instead_of_copied = "warn" # §6.22

# restriction — enable for safety-critical
undocumented_unsafe_blocks = "deny"   # §9.13
indexing_slicing = "warn"             # §12.13
arithmetic_side_effects = "warn"      # §12.9
missing_safety_doc = "deny"           # §9.20
```

Author for Edition 2024 + Rust 1.85+; verify each lint exists at your target MSRV with `cargo clippy --explain <lint>`.

---

## Summary Statistics

| Section | Anti-patterns | Code snippets |
|---|---|---|
| 1. Ownership & Borrowing | 18 | 3 |
| 2. Lifetimes | 12 | 0 |
| 3. Type System | 14 | 1 |
| 4. Async / Await | 25 | 5 |
| 5. Error Handling | 17 | 1 |
| 6. Performance | 22 | 0 |
| 7. Trait Design | 16 | 2 |
| 8. Macros | 13 | 0 |
| 9. Unsafe | 20 | 3 |
| 10. Cargo / Deps | 18 | 0 |
| 11. Testing | 20 | 0 |
| 12. Security | 20 | 4 |
| 13. API Design | 23 | 2 |
| 14. WASM / Embedded | 18 | 0 |
| **Total** | **256** | **21** |

Cross-referenced **40+ Clippy lints by name** for tooling alignment.

---

## Sources

- [rust-clippy lint catalog](https://rust-lang.github.io/rust-clippy/master/index.html)
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/) — esp. [transmutes](https://doc.rust-lang.org/nomicon/transmutes.html), [unwinding](https://doc.rust-lang.org/nomicon/unwinding.html)
- [Common Rust Lifetime Misconceptions (pretzelhammer)](https://github.com/pretzelhammer/rust-blog/blob/master/posts/common-rust-lifetime-misconceptions.md)
- [Awesome List of Rust Footguns](https://gist.github.com/ErnWong/f5c1e915a4defd32e3cdeb5693ab8062)
- [Pitfalls of Safe Rust — corrode](https://corrode.dev/blog/pitfalls-of-safe-rust/)
- [Async: What is Blocking? — Alice Ryhl](https://ryhl.io/blog/async-what-is-blocking/)
- [Shared state — tokio tutorial](https://tokio.rs/tokio/tutorial/shared-state)
- [Cancelling async Rust — sunshowers](https://sunshowers.io/posts/cancelling-async-rust/)
- [RFD 400: Dealing with cancel safety in async Rust — Oxide](https://rfd.shared.oxide.computer/rfd/0400)
- [tokio::select! docs](https://docs.rs/tokio/latest/tokio/macro.select.html)
- [tokio JoinHandle docs](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html)
- [Tokio unbounded MPSC memory issue #4321](https://github.com/tokio-rs/tokio/issues/4321)
- [async-trait Send bounds — baby steps](https://smallcultfollowing.com/babysteps/blog/2023/02/01/async-trait-send-bounds-part-1-intro/)
- [Announcing async fn in traits — Rust Blog](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/)
- [Error handling thiserror + anyhow guide — Caroline Morton](https://www.carolinemorton.co.uk/blog/rust-error-handling-anyhow-thiserror/)
- [Error Handling in Rust: A Deep Dive — Luca Palmieri](https://www.lpalmieri.com/posts/error-handling-rust/)
- [The Definitive Guide to Error Handling in Rust](https://www.howtocodeit.com/guides/the-definitive-guide-to-rust-error-handling)
- [The Rust Performance Book — Heap allocations](https://nnethercote.github.io/perf-book/heap-allocations.html)
- [Rust Performance Pitfalls — Llogiq](https://llogiq.github.io/2017/06/01/perf-pitfalls.html)
- [Cargo SemVer Compatibility](https://doc.rust-lang.org/cargo/reference/semver.html)
- [Some Rust breaking changes don't require a major version — predr.ag](https://predr.ag/blog/some-rust-breaking-changes-do-not-require-major-version/)
- [Cargo Features](https://doc.rust-lang.org/cargo/reference/features.html)
- [Cargo Workspace Feature Unification Pitfall — nickb.dev](https://nickb.dev/blog/cargo-workspace-and-the-feature-unification-pitfall/)
- [Rust Reference: macros by example](https://doc.rust-lang.org/reference/macros-by-example.html)
- [Rust Reference: procedural macros](https://doc.rust-lang.org/reference/procedural-macros.html)
- [Recursion limit attribute](https://doc.rust-lang.org/reference/attributes/limits.html)
- [Drop docs](https://doc.rust-lang.org/std/ops/trait.Drop.html)
- [Coherence — chalk book](https://rust-lang.github.io/chalk/book/clauses/coherence.html)
- [Understanding orphan rules — Sling Academy](https://www.slingacademy.com/article/understanding-coherence-rules-why-orphan-rules-restrict-certain-generic-impls/)
- [Newtype pattern — SoftwareMill](https://softwaremill.com/mastering-rust-patterns-vol-1-rust-newtypes/)
- [Tokio testing topics](https://tokio.rs/tokio/topics/testing)
- [A Preliminary Study of Fixed Flaky Tests in Rust Projects (arxiv 2502.02760)](https://arxiv.org/html/2502.02760v1)
- [Rust Security Handbook — yevh](https://github.com/yevh/rust-security-handbook)
- [What 44 CVEs Tell You About Rust's Safety Boundary](https://dev.to/arthurpro/what-44-cves-tell-you-about-rusts-safety-boundary-2cl7)
- [Improving overconstrained Rust library APIs — LogRocket](https://blog.logrocket.com/improving-overconstrained-rust-library-apis/)
- [Embedded Rust Book — Panicking](https://docs.rust-embedded.org/book/start/panicking.html)
- [Making Rust Workers reliable — Cloudflare](https://blog.cloudflare.com/making-rust-workers-reliable/)
- [no_std Playbook — HackMD](https://hackmd.io/@alxiong/rust-no-std)
- [Tokio shared state mutex guidance](https://tokio.rs/tokio/tutorial/shared-state)
- [Rust Patterns #19: Arc Mutex vs Arc RwLock — Telex](https://telex-tui.github.io/blog/rust-patterns-arc-mutex.html)
- [Common Mistakes with Rust Async — Qovery](https://www.qovery.com/blog/common-mistakes-with-rust-async)
- [Top 5 Tokio Runtime Mistakes — Techbuddies](https://www.techbuddies.io/2026/03/21/top-5-tokio-runtime-mistakes-that-quietly-kill-your-async-rust/)
