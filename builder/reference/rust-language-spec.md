# Rust Language Spec — Deep Dive Reference

> Companion to `language-idioms.md` §4 (Rust). This file covers the language specification, type system mechanics, async desugaring, macros, unsafe contracts, the memory model, FFI, `no_std`, const evaluation, and the stable/unstable feature timeline in depth. For the short-form idioms table and 20 baseline anti-patterns, see `language-idioms.md` lines 384-700.
>
> Baseline: Rust 1.85+ / Edition 2024 (as of 2026-05).

---

## Table of Contents

1. [Edition 2024 — what actually changed](#1-edition-2024--what-actually-changed)
2. [Ownership, Borrowing, Lifetimes](#2-ownership-borrowing-lifetimes)
3. [Type System](#3-type-system)
4. [Async / await — desugaring and stable surface](#4-async--await--desugaring-and-stable-surface)
5. [Macros](#5-macros)
6. [Unsafe Rust](#6-unsafe-rust)
7. [Memory Model & Concurrency Primitives](#7-memory-model--concurrency-primitives)
8. [FFI / Interop](#8-ffi--interop)
9. [`no_std` and Embedded](#9-no_std-and-embedded)
10. [Const Evaluation](#10-const-evaluation)
11. [Recently Stabilized Features (1.75 → 1.92)](#11-recently-stabilized-features-175--192)
12. [Unstable / Nightly Watch-list](#12-unstable--nightly-watch-list)
13. [Sources](#sources)

> **Cross-links:**
> - Production crate choices, error-handling crates, testing strategy → [`rust-best-practices.md`](./rust-best-practices.md)
> - Concrete misuse of each spec feature (Pin projection, `transmute`, async cancellation, FFI panic) → [`rust-anti-patterns.md`](./rust-anti-patterns.md)
> - Short-form idiom rules (let-else, `?`, newtypes, JoinSet, bounded mpsc) → `language-idioms.md` §4

---

## 1. Edition 2024 — what actually changed

Rust editions are *opt-in language dialects*. Each edition can change syntax, keywords, and some semantics without breaking older crates: every crate declares its edition in `Cargo.toml`, and crates of different editions interoperate at the item level. The compiler is a single rolling codebase; only the front-end behavior changes per edition.

### 1.1 Edition timeline

| Edition | First stable on | Headline changes | Migration command |
|---------|-----------------|------------------|-------------------|
| **2015** | Rust 1.0 (2015-05-15) | Initial edition. Module system uses absolute `::foo` paths from each crate root. `extern crate` required. | — (baseline) |
| **2018** | Rust 1.31 (2018-12-06) | Module path clarity (`crate::` / `use` rules); `async`/`await` reserved; NLL by default; `dyn Trait` syntax mandatory; `try` reserved. | `cargo fix --edition` |
| **2021** | Rust 1.56 (2021-10-21) | Disjoint closure captures (RFC 2229); `IntoIterator` for arrays; `panic!` always formats; `or_patterns` in macro fragments; reserved syntax (`prefix#"…"`, `prefix'…'`); prelude additions (`TryFrom`, `TryInto`, `FromIterator`). | `cargo fix --edition` |
| **2024** | Rust 1.85 (2025-02-20) | Largest edition. See §1.2. | `cargo fix --edition` |

### 1.2 Edition 2024 — full list of breaking-ish changes

Rust 2024 is opt-in but is the **default** for new crates (`cargo new` since 1.85). Migration is handled by `cargo fix --edition`, but a handful of changes require manual review.

| Change | RFC | Effect |
|--------|-----|--------|
| RPIT lifetime capture rules | [RFC 3498](https://rust-lang.github.io/rfcs/3498-lifetime-capture-rules-2024.html) | `-> impl Trait` now captures **all** in-scope lifetimes by default. Use the new `impl Trait + use<'a, T>` syntax (stable since 1.82) to be explicit / opt out. |
| `if let` temporary scope | [RFC 3535](https://rust-lang.github.io/rfcs/3535-if-let-rescope.html) | In `if let PAT = EXPR { … } else { … }`, temporaries in `EXPR` drop **before** the `else` branch (not after the whole `if`). Fixes deadlocks with `Mutex::lock()` in `if let`. |
| Tail expression temporary scope | [RFC 3606](https://rust-lang.github.io/rfcs/3606-temporary-lifetimes-in-tail-expressions.html) | Temporaries created in a block's tail expression drop **before** the block's locals. More predictable RAII order; occasionally requires a `let _x = …;` binding. |
| Never type fallback | — | The fallback type for unresolved `!` is now `!`, not `()`. Mostly a no-op except in unsafe code that relies on `()` fallback through generic bounds; the lint `never_type_fallback_flowing_into_unsafe` is **deny-by-default** in 1.92+. |
| `unsafe extern { … }` blocks | — | `extern "C" { … }` is now `unsafe extern "C" { … }`. Each declared item is implicitly `unsafe fn` unless tagged `safe fn`. |
| `unsafe` attributes | — | `#[no_mangle]`, `#[export_name]`, `#[link_section]` must be wrapped: `#[unsafe(no_mangle)]`. Acknowledges these can violate soundness. |
| `unsafe_op_in_unsafe_fn` warn-by-default | — | Body of an `unsafe fn` is no longer one giant unsafe block. Each unsafe operation needs an explicit `unsafe { … }`. |
| Disallow references to mutable statics | — | `&MY_STATIC` / `&mut MY_STATIC` on a `static mut` is now hard error (was lint). Use `addr_of!` / `addr_of_mut!` or `SyncUnsafeCell`/`Mutex`. |
| `gen` reserved keyword | [RFC 3513](https://rust-lang.github.io/rfcs/3513-gen-blocks.html) | Reserves `gen` for future generator blocks (still unstable). |
| Match ergonomics tightening | — | Some previously-implicit binding modes that mixed move/ref/copy now require explicit annotation. |
| Macro fragment specifiers | — | `expr_2021` introduced; `expr` now matches a wider set in 2024 (e.g. `const { … }` block expressions). |
| Prelude additions | — | `Future`, `IntoFuture` join the prelude. |
| `std::env::set_var`, `remove_var`, `Command::before_exec` | — | Marked `unsafe` (race with other threads reading env). |
| `IntoIterator for Box<[T]>` | — | `Box<[T]>` now yields owned `T` (not `&T`) — may break inference. |
| Rustfmt style edition | — | Style itself is now edition-aware via `style_edition = "2024"`. |
| Cargo: `resolver = "3"` default | — | MSRV-aware version resolver; new feature unification rules. |

Flagged terminology shift: the **`object_safe` lint was renamed `dyn_compatible`** in Edition 2024 (see §3.5). When porting old code, both lint name and diagnostic wording have updated.

### 1.3 Edition compatibility model

- A crate's edition affects **its own** parsing/semantics only.
- A 2024 crate can depend on a 2018 crate and vice versa.
- `std` / `core` is built once and exposes the same items to every edition; the language front-end hides or reveals syntax based on the consuming crate.

---

## 2. Ownership, Borrowing, Lifetimes

### 2.1 Move / Copy semantics

- Every value has exactly one owner. Going out of scope runs the destructor (`Drop::drop`) unless ownership was moved.
- A move is a bitwise copy that *invalidates the source*. The compiler tracks this statically; there is no runtime tombstone.
- `Copy` types skip invalidation: the bits are duplicated and both names remain valid. `Copy` requires `Clone` and implies no destructor.
- Primitives, shared references `&T`, function pointers, and small POD structs with `#[derive(Copy, Clone)]` are typical `Copy` types. `String`, `Vec`, `Box`, anything with `Drop`, and `&mut T` are **not** `Copy`.
- Partial moves out of a struct/enum are allowed and tracked field-by-field. After a partial move, the remaining fields can still be accessed; the whole binding cannot be re-passed by value.

### 2.2 Borrow rules and Non-Lexical Lifetimes (NLL)

The borrow checker enforces:

1. **Aliasing XOR mutation** — at any program point, a place is reachable through either any number of `&T` references **or** exactly one `&mut T`, never both.
2. **References must not outlive their referent**.
3. **No null / dangling** — references are always valid bit-patterns.

NLL (stable since Rust 1.36, default since 1.31 / 2018 edition; uplifted to 2015 in 2022) replaced lexical scope-based liveness with **MIR control-flow graph** based liveness. A borrow ends when it is last used on every path, not at the lexical end of a block:

```rust
let mut v = vec![1, 2, 3];
let first = &v[0]; // borrow starts
println!("{first}"); // last use — NLL ends the borrow here
v.push(4);           // OK: no overlapping live borrow
```

**Polonius** is the next-gen borrow checker (datalog-based, originating with Niko Matsakis). It accepts a strict superset of NLL programs (e.g. the "Problem case #3" with conditional returns). As of 2026-05 Polonius is gated behind `-Zpolonius=next` and being incrementally productionized; the long-term goal is to replace NLL entirely. Two-phase borrow-checking (reserve → activate) remains the pragmatic stop-gap.

### 2.3 Lifetime elision rules

Elision rewrites `fn` signatures only; it never affects types. The compiler applies:

1. Each elided lifetime in **input** position gets a **distinct fresh** lifetime.
2. If there is **exactly one input lifetime** (elided or not), it is assigned to all elided **output** lifetimes.
3. Otherwise, if there is `&self` or `&mut self`, the lifetime of `self` is assigned to all elided output lifetimes.
4. Otherwise, output lifetimes must be written explicitly.

Within `dyn Trait` and `impl Trait`, elided lifetimes desugar to higher-ranked bindings (see §2.4). Within `async fn`, the desugared `impl Future` captures **all** in-scope lifetimes — formalized for RPIT in Edition 2024.

### 2.4 Higher-Ranked Trait Bounds (HRTB) — `for<'a>`

```rust
fn apply<F>(f: F) where F: for<'a> Fn(&'a str) -> &'a str { /* … */ }
```

`for<'a> Fn(&'a str) -> &'a str` means "F implements `Fn(&'a str) -> &'a str` for **every** choice of `'a`" — universally quantified. Without HRTB, `F` would only need to satisfy the bound for one specific `'a`, which is too weak when the caller wants to invoke `f` with references of arbitrary lifetimes.

Closure traits (`Fn`/`FnMut`/`FnOnce`) get HRTB **automatically** in their elided forms: `Fn(&str) -> &str` is sugar for `for<'a> Fn(&'a str) -> &'a str`.

HRTB also appears for trait objects:

```rust
let f: &dyn for<'a> Fn(&'a str) -> &'a str = &|s| s;
```

### 2.5 Variance

Subtyping in Rust exists only between lifetimes (`'long: 'short` ⇒ `'long <: 'short`) and through unsizing coercions. Variance of a type constructor `F<T>` answers: when `Sub <: Super`, is `F<Sub> <: F<Super>` (covariant), reversed (contravariant), or neither (invariant)?

| Constructor | Variance over `'a` | Variance over `T` |
|-------------|-------------------|-------------------|
| `&'a T` | covariant | covariant |
| `&'a mut T` | covariant | **invariant** |
| `*const T` | — | covariant |
| `*mut T` | — | **invariant** |
| `Box<T>`, `Vec<T>`, `Rc<T>`, `Arc<T>` | — | covariant |
| `Cell<T>`, `RefCell<T>`, `UnsafeCell<T>` | — | **invariant** |
| `fn(T) -> U` | — | **contra**variant in `T`, covariant in `U` |
| `PhantomData<T>` | — | covariant (default) |
| `dyn Trait + 'a` | covariant in `'a` | — |

A user struct's variance is the meet (most restrictive) of the variances induced by each field. Invariance is "infectious".

### 2.6 PhantomData

`PhantomData<T>` is a zero-sized marker that **tells the compiler the type parameter or lifetime is logically present** even though no field uses it. Used for:

- **Variance control** (the only way to manually set variance):

  | Want | Use |
  |------|-----|
  | covariant in `T` | `PhantomData<T>` or `PhantomData<&'_ T>` |
  | contravariant in `T` | `PhantomData<fn(T)>` |
  | invariant in `T` | `PhantomData<fn(T) -> T>` or `PhantomData<*mut T>` |

- **Drop check** (`#[may_dangle]` + `PhantomData<T>` to mark "we own a `T`").
- **Carry an unused lifetime** to enforce a borrow relationship the type doesn't otherwise have.

### 2.7 `'static` bound

The `'static` lifetime means *"can live for the entire program"*. As a bound (`T: 'static`) it means *"`T` contains no references with shorter lifetimes"* — **not** "`T` is forever stored in static memory". Owned types like `String` and `Vec<u8>` are `'static`. `thread::spawn` requires the closure to be `'static` because the thread can outlive any non-static caller frame (unlike `thread::scope`, stable since 1.63, which allows borrowing parent locals).

> Common confusion: `&'a T` vs `T: 'a`. They're different. `&'a T` requires `T: 'a` (every reference inside `T` must outlive `'a`), but `T: 'a` does not imply `T` is itself a reference. See [`rust-anti-patterns.md` §2](./rust-anti-patterns.md#2-lifetime-pitfalls) for the catalog of lifetime misconceptions.

---

## 3. Type System

### 3.1 Generics

Monomorphized at compile time: each instantiation becomes a fresh copy of the code. Generic parameters can be types, lifetimes, or `const` values (§3.4). Bounds use `where`-clauses or inline `<T: Trait + ?Sized>`.

`?Sized` opts a parameter **out** of the default `Sized` bound (which is implicit on every type parameter). `?Sized` is currently the only "opt-out" syntactic class.

### 3.2 Traits — associated types vs generic parameters

- **Associated types** — a single implementation chooses one type per impl (`Iterator::Item`). Use when "the type is a function of `Self`".
- **Generic trait parameters** — multiple impls per `Self`, one per choice (`From<T>`, `Add<Rhs>`). Use when "the type is an input from the user".

Conversion is impossible after the fact; this is the API-design trade-off most often re-litigated.

### 3.3 GATs — Generic Associated Types (stable 1.65)

GATs let associated types carry their own lifetimes / type / const parameters. The textbook example is `LendingIterator`:

```rust
trait LendingIterator {
    type Item<'a> where Self: 'a;
    fn next<'a>(&'a mut self) -> Option<Self::Item<'a>>;
}
```

This expresses "items borrow from `self`", which the regular `Iterator` cannot, because `Item` is a single type chosen per impl.

GATs unlocked zero-copy parsing, streaming iterators, and database row APIs that previously required `unsafe` or callback hacks. Stable on Rust 1.65 (2022-11-03) after a six-year gestation.

### 3.4 Const generics

| Feature | Stable in |
|---------|-----------|
| `min_const_generics` — integer / bool / char `const N: usize` parameters | 1.51 |
| Trait bounds + where-clauses on `const` params | 1.51 |
| Const generic expressions in some positions (`feature(generic_const_exprs)`) | **unstable** |
| Inline `const { … }` blocks in expression position | 1.79 |
| `feature(adt_const_params)` — user types as const params | partial / unstable |
| Explicitly inferred const arguments (`Foo::<{_}>` style) | 1.89 |

Inline const blocks (1.79) execute at compile time in expression position and can use in-scope generics — useful for `[const { None }; N]`-style array initialization without `Copy`.

The remaining gap is "full" const generic *expressions*: `[u8; N + M]` style. RFC discussions for `min_generic_const_args` and `generic_const_exprs` are ongoing; a stable subset is a 2026 project goal.

### 3.5 Trait object safety — renamed to "dyn compatibility" (2024)

A trait is **dyn-compatible** (previously: "object-safe") if it can be used behind `dyn Trait`. Requirements:

- No method has a `Self: Sized` bound (unless `where Self: Sized`).
- No method returns `Self` by value or takes `Self` by value.
- No method has generic type parameters (lifetimes are fine).
- No associated functions (must be methods on `&self`/`&mut self`/`self`).
- No associated constants (until recently; some relaxations stable in 2024–2025).
- Supertraits must be dyn-compatible.

The Rust 2024 edition renamed the lint `object_safe` → `dyn_compatible` and updated diagnostics accordingly.

### 3.6 Trait upcasting (stable 1.86, 2025-04-03)

`&dyn Sub` coerces to `&dyn Super` when `Sub: Super`, without manual boilerplate. The vtable is updated by the compiler. Especially useful with `Any`:

```rust
trait MyTrait: std::any::Any { /* … */ }
fn into_any(x: Box<dyn MyTrait>) -> Box<dyn Any> { x } // OK in 1.86+
```

Raw pointers to trait objects still require manual care — leaking a raw pointer with the wrong vtable into safe code is UB.

### 3.7 Sealed trait pattern

A trait that can be *used* publicly but only *implemented* inside the defining crate. Idiomatic implementation:

```rust
mod private {
    pub trait Sealed {}
}

pub trait PublicAPI: private::Sealed {
    fn method(&self);
}

// Only the defining crate can write impls because the public path includes
// a name (`private::Sealed`) that isn't exported.
```

Used in `std`: `core::error::Error::type_id` is sealed via a private supertrait, allowing the lib team to evolve the trait without breaking downstream impls.

### 3.8 The never type `!`

Status as of 2026-05: the never type is **named** stable in patterns and return types (`fn foo() -> !`), but using `!` as a **value** in arbitrary expression positions is still gated by `feature(never_type)`. Edition 2024 flips the fallback (when an unresolved `!` must be assigned a concrete type) from `()` to `!`. From 1.92, lints catching the few unsafe-soundness cases are deny-by-default. Full stabilization is tracked by the Never Type Initiative (rust-lang/never-type-initiative).

---

## 4. Async / await — desugaring and stable surface

### 4.1 The `Future` trait

```rust
pub trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

`async fn` / `async { … }` desugar to anonymous types implementing `Future`. The state machine is generated by the compiler from the suspension points (every `.await`). `async fn foo()` is essentially `fn foo() -> impl Future`.

### 4.2 `Pin` and `Unpin`

Self-referential futures need to stay at a fixed memory address between polls. `Pin<P>` is a pointer wrapper that *prevents safe code from moving the pointee*. `Unpin` is an auto-trait marking "moving me is fine after pinning"; nearly all standard types implement `Unpin` automatically (the exception is types containing `PhantomPinned`).

- `Pin<&mut T>` cannot be safely converted to `&mut T` unless `T: Unpin`.
- `Pin::new(&mut x)` is safe for `T: Unpin`; otherwise use the `pin!` macro (1.68+) or `Box::pin`.
- The `poll` method takes `self: Pin<&mut Self>` so that the compiler enforces the pin invariant for every executor.

> Hand-rolling Pin projection is one of the most common UB sources in custom futures. Always use `pin-project-lite` or `pin-project`. See [`rust-anti-patterns.md` §9.7](./rust-anti-patterns.md#9-unsafe-pitfalls-high-stakes).

### 4.3 Executors vs runtimes

Rust ships the `Future` trait and `core::task::{Waker, Context, Poll}` in std/core, but **no executor**. A runtime (Tokio, async-std, smol, embassy) provides: a reactor (epoll/kqueue/IOCP/io_uring or hardware interrupts), a task scheduler, timer wheel, and channel primitives. This separation lets embedded `no_std` users pick their own scheduler.

### 4.4 `async fn` in traits — RPITIT and AFIT (stable 1.75)

```rust
trait MyService {
    async fn handle(&self, req: Request) -> Response;
    // sugar for:
    fn handle(&self, req: Request) -> impl Future<Output = Response> + '_;
}
```

Constraints stabilized in 1.75:

- **Not dyn-compatible** by default. Each impl's returned future has a different concrete type/size, so no static vtable can store it. For `dyn`, use the `async_trait` crate (boxes futures), wait for the `dyn-async-fn` work, or use the `trait_variant` crate to project to `Send`-bounded versions.
- **No automatic `Send` bound**. The returned future inherits whatever captured state's `Send`-ness. Use `trait_variant::make` (or hand-write a `SendService: MyService` supertrait) when both static dispatch and `Send` are required.

Rust 1.78 stabilized async-fn-in-trait with **concrete signatures**, allowing trait authors to write `fn handle(&self) -> impl Future<Output = R> + Send` directly to declare `Send` futures.

### 4.5 `async` closures (stable 1.85)

```rust
let f = async |x: u32| -> u32 { x.await_something().await };
```

Three new traits in the prelude:

- `AsyncFnOnce` — analogous to `FnOnce`, consumes captures.
- `AsyncFnMut`  — analogous to `FnMut`.
- `AsyncFn`     — analogous to `Fn`.

Crucially, async closures can borrow from captures across `.await` points, which a plain closure returning `impl Future` could not (the borrowed `Self` would need to outlive every awaiter). This eliminates a long-standing pain point in combinators like `Stream::then` and retry loops.

### 4.6 Lifetime capture rules (Edition 2024)

`-> impl Future + '_` (and `-> impl Trait + '_`) now capture **all in-scope lifetimes by default**. Use the explicit `use<'a, T>` bound (stable 1.82) to narrow:

```rust
fn parse<'a>(s: &'a str) -> impl Iterator<Item = &'a str> + use<'a> {
    s.split(' ')
}
```

This brings RPIT semantics in line with `async fn` (which already captured everything) and removes the need for the `Captures<'a>` workaround crate.

### 4.7 Cancellation safety

A future is "cancellation safe" if dropping it mid-poll leaves observable state consistent. Spec relevance:

- Dropping a future runs `Drop::drop` on every captured local **and** every partial state-machine value. Async destructors (`AsyncDrop`) are **unstable** as of 2026-05.
- `select!` macros routinely drop the losing branch's future — any I/O partially issued must be cleanable. This is a *library* property, not a language guarantee; `tokio::io::AsyncReadExt::read` is documented cancellation-safe, `tokio::io::AsyncWriteExt::write_all` is not.

> For the catalog of cancel-safe and cancel-unsafe primitives plus the `select!` rewrite pattern, see [`rust-anti-patterns.md` §4](./rust-anti-patterns.md#4-async--await-pitfalls-extensive).

### 4.8 `Send` / `Sync` propagation for futures

The compiler-generated future captures every variable held across a `.await`. The future is `Send` iff every such captured type is `Send`. This is why `MutexGuard` (from `std::sync`) across `.await` makes a future `!Send` and why `tokio::sync::MutexGuard` is used instead. Lint `must_not_suspend` (unstable) flags types you should not hold across await points.

---

## 5. Macros

### 5.1 Declarative macros — `macro_rules!`

Pattern-matching syntactic transformations. The arrow `=>` separates matcher from transcriber. Fragment specifiers:

| Specifier | Matches |
|-----------|---------|
| `item` | top-level item (fn, struct, …) |
| `block` | `{ … }` block expression |
| `stmt` | statement (without trailing `;`) |
| `pat`, `pat_param` | pattern (with vs. without `|`) |
| `expr` | expression (2024: includes `const { … }`); use `expr_2021` for old semantics |
| `ty` | type |
| `ident` | identifier |
| `path` | path |
| `tt` | single token tree (most flexible) |
| `meta` | meta-item (inside `#[…]`) |
| `lifetime`, `literal`, `vis` | as named |

`$x:ident`, repetition `$( … )*` / `+` / `?`, and recursive expansion are supported. **Hygiene** is partial: identifiers introduced in the macro are in a separate "scope" from caller identifiers, but module/type paths are *not* hygienic and must use absolute paths or `$crate::…`.

### 5.2 Procedural macros

Three flavors, all live in a separate crate marked `proc-macro = true`:

- **Derive** — `#[derive(MyTrait)]` — generate impls for the annotated item.
- **Attribute** — `#[my_attr] fn foo() { … }` — replace/transform an item.
- **Function-like** — `my_macro!(…)` — replace a call site with arbitrary tokens.

### 5.3 The `proc_macro2` / `syn` / `quote` workflow

Standard procedural macro architecture:

| Crate | Role |
|-------|------|
| `proc_macro` (built-in) | The "boundary" crate. Tokens cross the proc-macro ABI as `proc_macro::TokenStream`. |
| `proc_macro2` | Pure-Rust mirror that works in non-proc-macro crates (tests, libraries). Same API surface. Conversion via `.into()`. |
| `syn` | Parser. Provides `parse_macro_input!` and a full Rust AST. |
| `quote` | Token generator. `quote! { fn #name() { … } }` for hygienic interpolation. |

Hygiene control: every token has a **`Span`**. `Span::call_site()` resolves identifiers at the call site (caller's scope). `Span::def_site()` resolves at the macro definition (stable in newer versions). `Span::mixed_site()` is the macro-rules-like default — generated names are hygienic, references to existing names are not.

For user-facing diagnostics, use `quote::quote_spanned! { input_span => ... }` so error spans point at the user's bad input rather than the macro definition. Return `syn::Error::new(span, "msg").to_compile_error()` instead of `panic!` from a proc-macro body.

Debugging: `cargo expand` (cargo subcommand), `RUSTFLAGS="-Z unpretty=expanded"` on nightly, or `dbg!(&token_stream)`.

---

## 6. Unsafe Rust

### 6.1 What `unsafe` unlocks

The `unsafe` keyword grants exactly five new abilities:

1. Dereference a raw pointer (`*const T`, `*mut T`).
2. Call an `unsafe fn` (including FFI functions).
3. Read or write a mutable static (`static mut`).
4. Access a `union` field.
5. Implement an `unsafe trait` (e.g. `Send`, `Sync`, `GlobalAlloc`).

Everything else (e.g. integer overflow in debug, leaking memory, calling `panic!`) is *not* unsafe; it's safe but possibly logically wrong.

In 2024, `unsafe_op_in_unsafe_fn` is warn-by-default: an unsafe operation inside an `unsafe fn` body must still be wrapped in `unsafe { … }`.

### 6.2 Canonical undefined behaviors (Rust Reference)

1. **Data races.**
2. Dereferencing dangling or unaligned pointers.
3. Reading uninitialized memory at scalar types (`bool`, `char`, references, integers when read at integer type).
4. Breaking pointer aliasing rules: `&T` must not be mutated through any path (except interior mutability via `UnsafeCell`); `&mut T` must be exclusively accessed.
5. Mutating bytes that are immutable (e.g. inside a `const`, `&T` of a non-`UnsafeCell`, promoted temporaries).
6. Producing an invalid value at its type:
   - `bool` not `0`/`1`
   - `char` outside `0..=0x10FFFF` or a surrogate
   - `!` ever existing as a value
   - `fn` pointer that is null
   - reference / `Box` that is null, dangling, unaligned, or points to an invalid value
   - enum discriminant outside the valid set
7. Calling a function with the wrong call ABI (e.g. `"C"` instead of `"system"`).
8. Unwinding across an FFI boundary not declared `"C-unwind"`.
9. Executing code with `#[target_feature]` on hardware that lacks the feature.
10. Misusing inline assembly to violate any of the above.

> This is the canonical UB list. Concrete misuse patterns (`mem::transmute` between non-`#[repr(transparent)]` types, `Vec::set_len` without writing, `MaybeUninit::assume_init` too early, `Box::from_raw` from a non-Box pointer) live in [`rust-anti-patterns.md` §9](./rust-anti-patterns.md#9-unsafe-pitfalls-high-stakes).

### 6.3 Stacked Borrows → Tree Borrows

Both are *operational models* used to give precise meaning to aliasing-rule violations so tools like Miri can flag UB. Neither is normative yet — the official aliasing model is still being formalized.

- **Stacked Borrows** (Jung et al., 2019) — each location carries a stack of "borrow tags"; reborrowing pushes, going out of scope pops. Rejects ~54% more crate test cases than Tree Borrows, including some patterns that unsafe authors rely on.
- **Tree Borrows** (Villani et al., PLDI 2025, **Distinguished Paper**) — replaces the stack with a tree, modelling reborrow relationships more precisely. Strictly more permissive while still ruling out the optimisations Rust actually performs. Available in Miri via `-Zmiri-tree-borrows`; the Miri team is migrating it toward default behavior. Practical guidance for `unsafe` authors as of 2026-05: pass both models when possible; expect Tree Borrows to become the eventual default.

Example of a pattern Stacked Borrows rejects but Tree Borrows accepts (simplified):

```rust
// `&mut T` that is converted to a raw pointer, then a sibling `&T` is
// reborrowed from the same parent, and the raw pointer is used afterwards.
// Stacked Borrows pops the raw pointer's tag when the sibling shared reference
// is created. Tree Borrows tracks them as siblings in the tree and permits
// the raw read as long as no write occurs through it after the sibling read.
fn pattern(v: &mut [u32]) {
    let p = v.as_mut_ptr();          // raw, derived from `&mut [u32]`
    let _shared: &[u32] = &v[..];    // sibling shared reborrow
    // Reading through `p` here is rejected by Stacked Borrows,
    // accepted by Tree Borrows (no concurrent write through p).
    let _x = unsafe { *p };
}
```

### 6.4 `UnsafeCell<T>`

The only legal way to obtain `&mut T` from `&UnsafeCell<T>`. Has the language-level magic of *opting out* of the immutability invariant on shared references — `Cell`, `RefCell`, `Mutex`, `RwLock`, `OnceCell` all wrap it. `UnsafeCell` does **not** synchronize; you still need atomics, fences, or locking to be data-race free.

`UnsafeCell<T>` is `!Sync` by default; types built on top opt back into `Sync` manually (e.g. `Mutex<T>: Sync where T: Send`).

### 6.5 SAFETY-comment template

Every `unsafe` block needs a `// SAFETY:` block documenting why the invariants hold:

```rust
// SAFETY:
// - `ptr` was returned by `Box::into_raw` from the matching `Box::<T>::new` call.
// - No other reference / pointer to `*ptr` exists at this point.
// - We have exclusive ownership and are about to transfer it.
let boxed = unsafe { Box::from_raw(ptr) };
```

The lint `clippy::undocumented_unsafe_blocks` enforces this on demand; pair with `clippy::missing_safety_doc` on `pub unsafe fn` signatures.

---

## 7. Memory Model & Concurrency Primitives

### 7.1 `Send` / `Sync` auto-traits

- `Send` — values can be transferred to another thread.
- `Sync` — `&T` can be shared between threads (equivalently `T: Sync` iff `&T: Send`).

Both are **unsafe auto-traits**: derived automatically from fields, opt out with `impl !Send for Foo {}` (unstable) or `PhantomData<*const ()>`. Implementing them manually requires `unsafe impl`.

Examples:

- `Rc<T>: !Send, !Sync` (refcount is non-atomic).
- `Arc<T>: Send + Sync where T: Send + Sync` (atomic refcount).
- `Cell<T>: Send if T: Send`, `!Sync` (single-threaded interior mutation).
- `Mutex<T>: Send + Sync where T: Send`.
- `MutexGuard<'_, T>: !Send` on some platforms (pthread mutex can only be unlocked from the locking thread); `Sync` if `T: Sync`.

### 7.2 Data race definition (Rust Reference)

A data race occurs when:

1. Two or more threads concurrently access the same memory location, and
2. At least one access is a write, and
3. At least one access is non-atomic, and
4. The accesses are not synchronized by `happens-before` (locks, atomic release/acquire pairs, thread::spawn/join, …).

Data races are **always UB**. The borrow checker plus `Send`/`Sync` statically rules them out for safe code; `unsafe` code must uphold them by construction.

### 7.3 Atomics and memory ordering

`std::sync::atomic::{AtomicBool, AtomicUsize, AtomicI32, …, AtomicPtr<T>}`. Rust adopts the C++20 memory model exactly. Ordering enum:

| Ordering | Load? | Store? | RMW? | Meaning |
|----------|-------|--------|------|---------|
| `Relaxed` | ✓ | ✓ | ✓ | No ordering with other ops; only atomicity of the operation itself. Use for counters not protecting other data. |
| `Acquire` | ✓ | — | ✓ | Subsequent ops in this thread cannot be reordered before this load. Pairs with `Release` on the writer side. |
| `Release` | — | ✓ | ✓ | Prior ops in this thread cannot be reordered after this store. Pairs with `Acquire`. |
| `AcqRel` | — | — | ✓ | RMW only: Acquire on the load half, Release on the store half. |
| `SeqCst` | ✓ | ✓ | ✓ | All `SeqCst` operations form a single total order observed by all threads. Strongest, most expensive. |

`compiler_fence` and `fence` provide standalone barriers (no associated data). `std::sync::atomic::Ordering` is `#[non_exhaustive]`-like only by convention; the variants are fixed.

### 7.4 `std::sync` vs `parking_lot`

`std::sync::Mutex` historically wrapped pthread/CRITICAL_SECTION; since Rust 1.62 it has a custom futex-backed implementation on Linux and a SRWLOCK-backed implementation on Windows — performance is competitive with `parking_lot::Mutex` in most cases, and the std version supports poisoning (panic in critical section ⇒ `lock()` returns `Err`). `parking_lot` is still preferred when you need:

- `RwLock` with writer-preference fairness configurable
- non-poisoning semantics
- `Condvar::wait_for` with sub-millisecond resolution on older platforms

### 7.5 Channels

- `std::sync::mpsc` — multi-producer single-consumer, unbounded (`channel()`) or bounded (`sync_channel(n)`). Rewritten in Rust 1.67 on top of `crossbeam-channel` for ~2× throughput improvement.
- `crossbeam_channel` — MPMC, supports `select!`, more flexible.
- `tokio::sync::mpsc` — async-aware, bounded variant required for backpressure.
- `flume` — drop-in MPSC/MPMC, async-aware.

---

## 8. FFI / Interop

### 8.1 `extern "C"` and ABIs

Function ABIs supported by `extern "ABI"`: `"Rust"` (default), `"C"`, `"system"`, `"cdecl"`, `"stdcall"`, `"fastcall"`, `"vectorcall"`, `"thiscall"`, `"aapcs"`, `"win64"`, `"sysv64"`, `"C-unwind"`, `"system-unwind"` (the `-unwind` variants permit panics across the boundary).

In Edition 2024, an `extern` block must be written as `unsafe extern "C" { … }`; the *block* is unsafe to declare. Items inside are implicitly `unsafe fn` unless tagged `safe fn` (stable 1.82).

### 8.2 `#[repr]` layouts

| Repr | Layout |
|------|--------|
| Default `#[repr(Rust)]` | **Unspecified**. Fields may be reordered for optimal packing. Niche optimizations apply (e.g. `Option<&T>` is the size of `&T`). |
| `#[repr(C)]` | C-compatible struct layout, fields in declaration order, padding per platform C ABI. Enums become `int` with platform integer type (size = platform `int`, except where target ABI says otherwise). |
| `#[repr(transparent)]` | Single non-ZST field; same ABI and layout as that field. |
| `#[repr(packed(N))]` / `#[repr(packed)]` | Alignment of `N` (default 1). Creating a reference to a misaligned field is UB. |
| `#[repr(u8)]` … `#[repr(i128)]` (1.89+) | Enum discriminant size. |
| `#[repr(align(N))]` | Force minimum alignment. |

`#[repr(C)]` does **not** make all aspects of layout the same as C — passing a `#[repr(C)]` struct *by value* through FFI can still differ in calling conventions (small-struct return on x86-64 SysV ABI). Pass by pointer for safety, or use `cxx` which inserts shims.

### 8.3 Binding generators

| Tool | Direction | Notes |
|------|-----------|-------|
| `bindgen` | C → Rust | LLVM-libclang based; handles complex headers, generates unsafe FFI types. |
| `cbindgen` | Rust → C | Parses Rust source, emits `.h` files. Limited to a Rust subset (`#[repr(C)]` types only). |
| `cxx` | Rust ↔ C++ | Bidirectional, type-safe shims. Owns both sides of the boundary; safer than raw FFI. |
| `autocxx` | C++ → Rust (cxx-based) | Generates `cxx` bridges from C++ headers automatically. |
| `pyo3`, `napi-rs`, `jni`, `rb-sys`, `tauri` | Higher-level | Provide language-specific safe wrappers (Python, Node, JVM, Ruby). |

### 8.4 `#[no_mangle]` and symbol names

Default Rust mangling encodes the full path + crate disambiguator (e.g. `_RNvCsXXX_4mycrate8my_func`). `#[no_mangle]` (2024: `#[unsafe(no_mangle)]`) exports the bare identifier; `#[export_name = "foo"]` overrides with a chosen symbol name. Soundness hazard: duplicate symbols across crates = linker error or silent UB.

### 8.5 Panic across FFI

Panicking through a frame compiled with `"C"` ABI is **undefined behavior**. Use `"C-unwind"` (stable 1.71) if you intentionally want to propagate, or wrap callbacks in `catch_unwind` to defuse panics at the boundary:

```rust
extern "C" fn cb(x: i32) -> i32 {
    std::panic::catch_unwind(|| do_thing(x)).unwrap_or(-1)
}
```

> Common FFI panic patterns and their fixes live in [`rust-anti-patterns.md` §9.8](./rust-anti-patterns.md#9-unsafe-pitfalls-high-stakes).

---

## 9. `no_std` and Embedded

### 9.1 The std / alloc / core split

| Crate | Requires | Contains |
|-------|----------|----------|
| `core` | Nothing (no OS, no heap) | Primitive types, traits, iterators, atomics, `mem`, `ptr`, `Result`/`Option`, `Future` trait, formatting. Always available. |
| `alloc` | A `GlobalAlloc` and `alloc_error_handler` | `Box`, `Vec`, `String`, `Rc`, `Arc`, collections (`BTreeMap`, …). |
| `std` | An OS with threads, files, networking, time | Re-exports core + alloc, adds `std::fs`, `std::net`, `std::sync`, `std::thread`, `std::process`. |

### 9.2 `#![no_std]` crate setup

```rust
#![no_std]

extern crate alloc;   // optional, if you want a heap

use core::panic::PanicInfo;

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! { loop {} }

#[global_allocator]
static A: MyAllocator = MyAllocator;

// Pre-1.68 also needed:
// #[alloc_error_handler]
// fn oom(_: core::alloc::Layout) -> ! { loop {} }
```

`alloc_error_handler` defaults to panicking since Rust 1.68; explicit handler only needed in `no_std` environments where panicking is itself unwanted.

### 9.3 Target triples

`<arch>-<vendor>-<sys>-<abi>`, e.g. `thumbv7em-none-eabihf`, `riscv32imc-unknown-none-elf`, `wasm32-unknown-unknown`, `x86_64-pc-windows-msvc`, `aarch64-apple-darwin`.

Three target tiers:

- **Tier 1** — guaranteed to work, full test coverage (x86_64 Linux, macOS, Windows; aarch64 Linux/Darwin).
- **Tier 2** — guaranteed to build, may not run all tests.
- **Tier 3** — best-effort; may break across versions.

Embedded ecosystem: `embedded-hal` (HAL traits), `embassy` (async on microcontrollers), `RTIC` (Real-Time Interrupt-driven Concurrency).

---

## 10. Const Evaluation

### 10.1 What `const fn` can do, by release

| Version | Added capability |
|---------|------------------|
| 1.31 | `const fn` MVP — basic arithmetic, no control flow. |
| 1.46 | `if`/`else`, `match` (later), `loop`, `while` were added incrementally. |
| 1.46–1.55 | Various stdlib functions become `const` (`mem::replace`, `Option::unwrap` for `Copy` etc.). |
| 1.57 | `const panic!`. |
| 1.61 | Generic bounds in `const fn`. |
| 1.64 | `&mut T` and `*mut T` in *some* const contexts. |
| 1.79 | Inline `const { … }` blocks in expression position. |
| 1.83 | `&mut`, `*mut`, `&Cell`, `*const Cell` allowed inside const fn bodies; references to statics in const initializers; many stdlib methods become const (`UnsafeCell::get_mut`, `slice::first_mut`, …). |
| 1.85 | Many `Layout` methods, `mem::size_of_val`, `mem::align_of_val`, `MaybeUninit::write`, `ptr::swap`, `mem::swap`, float operations become const. |

What `const fn` **cannot** do (as of 2026-05):

- Allocate (`Box::new`, `Vec::new` are `const` but cannot push).
- Call non-`const` trait methods (no `T: Add` arithmetic generically; `+` on primitives works because it's an intrinsic).
- Float NaN bit patterns are not stable in const context (deterministic but some operations are forbidden).
- Use `?` operator (until `const` `Try` lands).
- Iterate via `for` (`Iterator::next` is not const).

### 10.2 Const generic expressions

Stable: `[T; N]` where `N: usize` is a const param.

Unstable (`feature(generic_const_exprs)`): `[T; N + 1]`, `[T; { size_of::<T>() }]`, arbitrary const expression in array length / type position.

A constrained subset (`min_generic_const_args`) is on the 2026 roadmap and will likely be the first to stabilize.

### 10.3 Const traits

Not yet stable. The `feature(const_trait_impl)` unstable feature lets traits declare const fn methods (`impl const Add for Foo { … }`). This is the key blocker for using `+`, `==`, `Default::default()` etc. generically in const fn. The const-traits project group has it as a 2026 stabilization goal but the surface is large (`?const T: Trait` opt-out syntax, syntactic implications, effect polymorphism).

---

## 11. Recently Stabilized Features (1.75 → 1.92)

Quick reference for what shipped in the last ~25 releases.

| Version | Date | Major language / stdlib changes |
|---------|------|---------------------------------|
| **1.75** | 2023-12-28 | `async fn` in traits (AFIT) + return-position `impl Trait` in traits (RPITIT). `pointer::byte_offset/add/sub` family. |
| **1.76** | 2024-02-08 | ABI-compat documentation, `type_name_of_val`, `Result::inspect`, `Arc::unwrap_or_clone`, `ptr::addr_eq`, `std::hash::DefaultHasher`. |
| **1.77** | 2024-03-21 | C-string literals (`c"…"`). `async fn` recursion via indirection. THIR unsafeck. `offset_of!` macro. |
| **1.78** | 2024-05-02 | `#[diagnostic::on_unimplemented]` namespace. AFIT with concrete return types. `Arc::unwrap_or_clone`/`Rc::unwrap_or_clone`. `slice::chunk_by`. Hard error on matching `NaN`. |
| **1.79** | 2024-06-13 | Inline `const { … }` blocks in expressions. Associated-type bounds in trait bounds (`T: IntoIterator<Item: Display>`). Automatic temp-lifetime-extension in `match` / `if`. |
| **1.80** | 2024-07-25 | Exclusive ranges `0..5` in patterns. `LazyLock`, `LazyCell` stable. Boxed slice `IntoIterator`. |
| **1.81** | 2024-09-05 | `Error` in `core` (usable from `no_std`). `#[expect(lint)]` attribute. New sort algorithms (driftsort / ipnsort). `PanicInfo` → `PanicHookInfo` rename. |
| **1.82** | 2024-10-17 | `use<…>` bound syntax for explicit RPIT lifetime capture. `safe` items in `unsafe extern`. `&raw const`/`&raw mut` to create raw pointers without going through `&`. CFG name/value checking via `--check-cfg`. |
| **1.83** | 2024-11-28 | `&mut`, `*mut`, `&Cell`, `*const Cell` allowed in `const`. References to statics in const initializers. `M::N` path syntax. |
| **1.84** | 2025-01-09 | MSRV-aware resolver opt-in (`resolver = "3"`). `Pin::as_deref_mut`. Strict provenance APIs stable (`ptr::without_provenance`, `expose_provenance`, `with_addr`). |
| **1.85** | 2025-02-20 | **Edition 2024 stable.** **Async closures** + `AsyncFn`/`AsyncFnMut`/`AsyncFnOnce`. Many const-fn additions. `Future`/`IntoFuture` in prelude. |
| **1.86** | 2025-04-03 | **Trait upcasting** (`&dyn Sub` → `&dyn Super`). `#[target_feature]` on safe fns. `HashMap::get_disjoint_mut`, `slice::get_disjoint_mut`. `missing_abi` warn-by-default. |
| **1.87** | 2025-05 | Unsafe `std::arch` intrinsics converted to safe via target-feature mechanism. Inline-asm sym/labels improvements. |
| **1.88** | 2025-06-26 | **`let` chains stabilized in Edition 2024** (`if let A = a && let B = b && cond { … }`). **Naked functions**. `cfg(true)` / `cfg(false)`. Slice `as_chunks` family. |
| **1.89** | 2025-08-07 | Explicit `_` const arguments. `#[repr(u128)]` / `#[repr(i128)]`. New target features (AVX-512, SHA-512, SM3/SM4, LoongArch extensions). |
| **1.90** | 2025-09 | (incremental: stdlib const-stabilizations, lints). |
| **1.91** | 2025-11 | (incremental). |
| **1.92** | 2025-12 | `never_type_fallback_flowing_into_unsafe` and `dependency_on_unit_never_type_fallback` are now **deny-by-default**. Continued never-type stabilization push. |

---

## 12. Unstable / Nightly Watch-list

What's likely to ship in the next 2–4 releases, ordered by maturity.

| Feature | Tracking | Status | Why it matters |
|---------|----------|--------|----------------|
| **`gen` blocks** | [RFC 3513](https://rust-lang.github.io/rfcs/3513-gen-blocks.html) | Implementation working on nightly; iterator-yielding generators (no resume args). `gen` keyword reserved in 2024. | Replaces hand-rolled state machines and the `genawaiter` crate for ordinary iterators. |
| **Async generators (`async gen`)** | Same RFC | Nightly. | The async equivalent — `Stream` from a coroutine. |
| **Try blocks (`try { … }`)** | tracking #31436 | Nightly long-standing; design churn over `?` semantics. | Lets `?` work inside an expression without a wrapping function. |
| **Specialization** (`min_specialization`) | tracking #31844 | `min_specialization` used internally by std (`Vec::extend`); full `specialization` ICE-prone. Soundness research ongoing. | Lets a generic impl be overridden by a more specific one (e.g. fast path for `Vec`-of-`Copy`). |
| **Const traits** | const-traits project group | `feature(const_trait_impl)` on nightly. | Unblocks `+`, `==`, iteration in `const fn`. |
| **`generic_const_exprs`** | tracking #76560 | Nightly, complex; `min_generic_const_args` likely first to land. | `[u8; N + 1]` style expressions in types. |
| **Async drop (`AsyncDrop`)** | RFC + impl | Early nightly. | Allows awaiting in destructors — needed for graceful task/IO shutdown. |
| **`dyn`-compatible AFIT** | async fundamentals initiative | Workarounds exist (`async_trait`, `trait_variant`). | Native `dyn AsyncTrait` without boxing each call. |
| **`super let`** | RFC 3676 | Nightly. | Lets a `let` outlive its block — useful for borrow patterns in proc-macro output. |
| **Pattern types** | RFC 3535 family | Early nightly. | `u32 is 1..` for compiler-verified range types. |
| **`!` (never) as a value type** | Never Type Initiative | Lints tightening, full type stabilization staged. | First-class `!` everywhere. |
| **`feature(unsized_locals)`, `unsized_fn_params`** | Long-stalled | Re-evaluated. | Removes most uses of `Box<dyn …>` purely for sizing. |
| **`offset_of!` for enum variants** | Stable for structs in 1.77; variant support nightly. | | Safer alternative to manual layout pokes. |
| **`extern "rust-call"` stabilization** | n/a | Internal-only currently. | Would let users impl `Fn*` traits without nightly. |

---

## Sources

### Official Rust documentation

- [The Rust Reference — Behavior considered undefined](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)
- [The Rust Reference — Never type](https://doc.rust-lang.org/reference/types/never.html)
- [The Rustonomicon — Subtyping and Variance](https://doc.rust-lang.org/nomicon/subtyping.html)
- [The Rustonomicon — Higher-Rank Trait Bounds](https://doc.rust-lang.org/nomicon/hrtb.html)
- [The Rustonomicon — What Unsafe Can Do](https://doc.rust-lang.org/nomicon/what-unsafe-does.html)
- [The Rustonomicon — Send and Sync](https://doc.rust-lang.org/nomicon/send-and-sync.html)
- [The Rustonomicon — Races](https://doc.rust-lang.org/nomicon/races.html)
- [The Rustonomicon — FFI](https://doc.rust-lang.org/nomicon/ffi.html)
- [The Rustonomicon — Atomics](https://doc.rust-lang.org/nomicon/atomics.html)
- [std::sync::atomic::Ordering](https://doc.rust-lang.org/std/sync/atomic/enum.Ordering.html)
- [std::cell::UnsafeCell](https://doc.rust-lang.org/std/cell/struct.UnsafeCell.html)
- [std::marker::Sync](https://doc.rust-lang.org/stable/std/marker/trait.Sync.html)
- [std::marker::Unpin](https://doc.rust-lang.org/std/marker/trait.Unpin.html)
- [std::pin module](https://doc.rust-lang.org/std/pin/)
- [core::alloc::GlobalAlloc](https://doc.rust-lang.org/core/alloc/trait.GlobalAlloc.html)

### Edition guide

- [Rust 2024 Edition Guide — Index](https://doc.rust-lang.org/edition-guide/rust-2024/index.html)
- [Rust 2024 — RPIT lifetime capture](https://doc.rust-lang.org/edition-guide/rust-2024/rpit-lifetime-capture.html)
- [Rust 2024 — If let temporary scope](https://doc.rust-lang.org/edition-guide/rust-2024/temporary-if-let-scope.html)
- [Rust 2024 — Tail expression temporary scope](https://doc.rust-lang.org/edition-guide/rust-2024/temporary-tail-expr-scope.html)
- [Rust 2024 — Never type fallback](https://doc.rust-lang.org/edition-guide/rust-2024/never-type-fallback.html)
- [Rust 2021 — Disjoint capture in closures](https://doc.rust-lang.org/edition-guide/rust-2021/disjoint-capture-in-closures.html)

### Release blog posts

- [Announcing Rust 1.75.0 — async fn / RPIT in traits](https://blog.rust-lang.org/2023/12/21/async-fn-rpit-in-traits/)
- [Announcing Rust 1.83.0](https://blog.rust-lang.org/2024/11/28/Rust-1.83.0/)
- [Announcing Rust 1.85.0 and Rust 2024](https://blog.rust-lang.org/2025/02/20/Rust-1.85.0/)
- [Announcing Rust 1.86.0](https://blog.rust-lang.org/2025/04/03/Rust-1.86.0/)
- [Announcing Rust 1.88.0](https://blog.rust-lang.org/2025/06/26/Rust-1.88.0/)
- [Generic associated types to be stable in Rust 1.65](https://blog.rust-lang.org/2022/10/28/gats-stabilization/)
- [Non-lexical lifetimes (NLL) fully stable](https://blog.rust-lang.org/2022/08/05/nll-by-default/)

### RFCs

- [RFC 0387 — Higher-Ranked Trait Bounds](https://rust-lang.github.io/rfcs/0387-higher-ranked-trait-bounds.html)
- [RFC 0738 — Variance](https://rust-lang.github.io/rfcs/0738-variance.html)
- [RFC 2094 — Non-Lexical Lifetimes](https://rust-lang.github.io/rfcs/2094-nll.html)
- [RFC 2229 — Disjoint capture in closures](https://github.com/rust-lang/rfcs/blob/master/text/2229-capture-disjoint-fields.md)
- [RFC 2920 — Inline const](https://rust-lang.github.io/rfcs/2920-inline-const.html)
- [RFC 3324 — dyn upcasting coercion](https://rust-lang.github.io/rfcs/3324-dyn-upcasting.html)
- [RFC 3498 — Lifetime capture rules 2024](https://rust-lang.github.io/rfcs/3498-lifetime-capture-rules-2024.html)
- [RFC 3513 — gen blocks](https://rust-lang.github.io/rfcs/3513-gen-blocks.html)
- [RFC 3606 — Temporary lifetimes in tail expressions](https://rust-lang.github.io/rfcs/3606-temporary-lifetimes-in-tail-expressions.html)

### Project goals & initiatives

- [Const Traits project goal (2025h1)](https://rust-lang.github.io/rust-project-goals/2025h1/const-trait.html)
- [Full Const Generics project goal (2026)](https://rust-lang.github.io/rust-project-goals/2026/const-generics.html)
- [Never Type Initiative](https://rust-lang.github.io/never-type-initiative/)
- [Async fundamentals: async fn in dyn trait](https://rust-lang.github.io/async-fundamentals-initiative/explainer/async_fn_in_dyn_trait.html)
- [NLL Working Group](https://rust-lang.github.io/compiler-team/working-groups/nll/)
- [Polonius project](https://github.com/rust-lang/polonius)

### Memory model & research

- [Tree Borrows paper (PLDI 2025)](https://iris-project.org/pdfs/2025-pldi-treeborrows.pdf)
- [From Stacks to Trees — Ralf Jung blog](https://www.ralfj.de/blog/2023/06/02/tree-borrows.html)
- [What's "new" in Miri (2025) — Ralf Jung](https://www.ralfj.de/blog/2025/12/22/miri.html)
- [Miri repository (rust-lang/miri)](https://github.com/rust-lang/miri/)
- [Mara Bos — Rust Atomics and Locks (memory ordering chapter)](https://mara.nl/atomics/memory-ordering.html)

### FFI & tooling

- [bindgen — rust-lang/rust-bindgen](https://github.com/rust-lang/rust-bindgen)
- [CXX — cxx.rs](https://cxx.rs/context.html)

### Sealed traits

- [A definitive guide to sealed traits in Rust — Predrag Gruevski](https://predr.ag/blog/definitive-guide-to-sealed-traits-in-rust/)
- [Rust API Guidelines — Future proofing](https://rust-lang.github.io/api-guidelines/future-proofing.html)
