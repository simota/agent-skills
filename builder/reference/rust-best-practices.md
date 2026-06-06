# Rust Best Practices — Deep Dive Reference

> Companion to `language-idioms.md` §4 (Rust). This file covers production best practices, the full Rust API Guidelines (C-* checklist), workspace patterns, the 2026 cargo + toolchain stack, the seven-layer testing strategy, perf practices (allocator/SIMD/PGO/BOLT), the 21-row production crate matrix, structured-concurrency idioms, docs & doctest discipline, release/distribution, and a 2023→2026 migration cheatsheet. For the short-form idioms table and 20 baseline anti-patterns, see `language-idioms.md` lines 384-700.
>
> Baseline: Rust 1.85+ / Edition 2024 (as of 2026-05).

---

## Table of Contents

1. [Rust API Guidelines — full C-* checklist](#1-rust-api-guidelines--full-c--checklist)
2. [Error handling patterns — deep](#2-error-handling-patterns--deep)
3. [Project structure & cargo workspaces](#3-project-structure--cargo-workspaces)
4. [Cargo & toolchain — the 2026 productivity stack](#4-cargo--toolchain--the-2026-productivity-stack)
5. [Testing strategy — the seven layers](#5-testing-strategy--the-seven-layers)
6. [Performance practices](#6-performance-practices)
7. [Security practices](#7-security-practices)
8. [Async ecosystem — structured concurrency](#8-async-ecosystem--structured-concurrency)
9. [Production crate matrix — 2026 baseline](#9-production-crate-matrix--2026-baseline)
10. [Domain architecture patterns](#10-domain-architecture-patterns)
11. [Documentation & doc-tests](#11-documentation--doc-tests)
12. [Release & distribution](#12-release--distribution)
13. [What changed since 2023 — the migration cheatsheet](#13-what-changed-since-2023--the-migration-cheatsheet)
14. [Sources](#sources)

> **Cross-links:**
> - Spec mechanics behind each rule (HRTB, variance, async desugaring, FFI ABI) → [`rust-language-spec.md`](./rust-language-spec.md)
> - Misuse catalog for the patterns below, with Clippy lints to enforce them → [`rust-anti-patterns.md`](./rust-anti-patterns.md)
> - Baseline idioms (let-else, `?`, newtypes, JoinSet, bounded mpsc, thiserror vs anyhow split) → `language-idioms.md` §4

---

## 1. Rust API Guidelines — full C-* checklist

The canonical reference is the **Rust API Guidelines Checklist** maintained by the libs team — every public Rust crate should pass it before 1.0. Source: https://rust-lang.github.io/api-guidelines/checklist.html

The guidelines are grouped into 11 categories. This section reproduces every `C-*` identifier with a short actionable summary and a "violation smell" so reviewers can spot drift.

### 1.1 Naming

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-CASE** | Casing follows RFC 430: `UpperCamelCase` for types/traits, `snake_case` for fns/vars, `SCREAMING_SNAKE_CASE` for consts/statics | `pub fn getUser()`, `pub struct user_id` |
| **C-CONV** | Ad-hoc conversions follow `as_` (borrowed→borrowed, cheap), `to_` (borrowed→owned, expensive), `into_` (owned→owned, consuming) | `User::convert()`, `User::transform()` |
| **C-GETTER** | Getter is bare field name (`user.name()`), not `get_name()` — except `get_*` on collections with index | `pub fn get_id(&self) -> Id` (no other `id` getter exists) |
| **C-ITER** | Collection iterators use `iter()` (`&T`), `iter_mut()` (`&mut T`), `into_iter()` (`T`) | Custom-named `each()`, `walk()`, `traverse()` |
| **C-ITER-TY** | Iterator type names match the producing method: `Vec::iter() -> Iter<'_, T>`, `Vec::into_iter() -> IntoIter<T>` | `Vec::iter() -> VecIterator` |
| **C-FEATURE** | Cargo feature names are free of placeholder words like `use-` or `with-` | `[features] use-tokio = []` instead of `tokio = []` |
| **C-WORD-ORDER** | Names use consistent word order across the crate — pick `decode_utf8` or `utf8_decode` and stick with it | `decode_utf8` + `encode_to_utf8` in the same crate |

### 1.2 Interoperability

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-COMMON-TRAITS** | Eagerly derive/implement `Copy`, `Clone`, `Eq`, `PartialEq`, `Ord`, `PartialOrd`, `Hash`, `Debug`, `Display`, `Default` where semantically valid | Public type with no `Debug` impl |
| **C-CONV-TRAITS** | Use `From`, `Into`, `AsRef`, `AsMut` for conversions — never invent a parallel `fn convert()` method | Hand-rolled `Foo::from_bar(x)` when `From<Bar> for Foo` would fit |
| **C-COLLECT** | Custom collections implement `FromIterator` and `Extend` so callers can `.collect()` into them | Hand-rolled `MyVec::from_iterator(iter)` |
| **C-SERDE** | Data structures provide `Serialize` + `Deserialize` impls (gated behind a feature flag if serde is optional) | Public DTO type missing serde derives |
| **C-SEND-SYNC** | Types are `Send` and `Sync` wherever possible — and the docs note explicitly when they're not | `Rc<T>` in a public type without warning |
| **C-GOOD-ERR** | Error types implement `Error + Display + Debug + Send + Sync + 'static` and surface a meaningful message | `Error::Other(String)` blob, no source chain |
| **C-NUM-FMT** | Custom integer/binary types implement `LowerHex`, `UpperHex`, `Octal`, `Binary` | `MyHash` with only `Display` |
| **C-RW-VALUE** | Generic reader/writer functions take `R: Read` / `W: Write` *by value* (not `&mut`), so callers can pass owned readers without `&mut` rituals | `fn parse(reader: &mut impl Read)` everywhere |

### 1.3 Macros

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-EVOCATIVE** | Macro input syntax visually echoes the generated output | `assert_eq!(expected = 3, actual = result)` (looks invented) |
| **C-MACRO-ATTR** | Item macros compose well with `#[derive(...)]`, `#[cfg(...)]`, `#[doc(...)]` | Macro that strips attributes off the input item |
| **C-ANYWHERE** | Item macros work in module, impl, trait, extern blocks | Macro panics in `impl` blocks |
| **C-MACRO-VIS** | Item macros honor `pub`, `pub(crate)`, etc. on inputs | Macro hardcodes `pub` on every emitted item |
| **C-MACRO-TY** | Type-position macro fragments are flexible (`$t:ty`) | Macro only accepts a single ident |

### 1.4 Documentation

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-CRATE-DOC** | Crate root (`//!`) has overview, motivation, headline example, feature flag map | Empty `lib.rs` with no `//!` |
| **C-EXAMPLE** | Every public item has at least one rustdoc example | `pub fn parse(s: &str) -> Result<Foo, Error>` with no `# Examples` |
| **C-QUESTION-MARK** | Examples use `?`, not `try!` (deprecated), not `unwrap()` | `# Examples` block littered with `.unwrap()` |
| **C-FAILURE** | Function docs include `# Errors`, `# Panics`, `# Safety` sections where applicable | Public fallible fn with no `# Errors` |
| **C-LINK** | Prose uses intra-doc links (`[`Type`]`) to navigate, not bare names | Plain-text "see `Foo`" with no link |
| **C-METADATA** | `Cargo.toml` has `authors`, `description`, `license`, `homepage`, `documentation`, `repository`, `keywords`, `categories` | Crate published with empty `description` |
| **C-RELNOTES** | `CHANGELOG.md` (or release notes) documents every user-visible change | First-time changelog at v3.0 |
| **C-HIDDEN** | `#[doc(hidden)]` on internal items that ended up in the public macro/inherent surface but aren't part of the API contract | Generated `Builder` types polluting rustdoc |

### 1.5 Predictability

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-SMART-PTR** | Smart pointers (`Arc<T>`, `Box<T>`, `Rc<T>`-likes) don't add inherent methods — they only `Deref` to inner | Custom `Arc::for_id(&self)` |
| **C-CONV-SPECIFIC** | Conversions live on the *more specific* type — `String::from(&str)`, not `str::to_string` (it does, but only because str is older) | `From<HashMap<K,V>> for Vec<(K,V)>` placed on `HashMap` |
| **C-METHOD** | A function with an obvious receiver is a method, not a free fn | `fn rotate(v: &mut Vec<T>, n: usize)` instead of `v.rotate(n)` |
| **C-NO-OUT** | Functions return values; out-parameters are not idiomatic Rust | `fn parse(s: &str, out: &mut Foo)` |
| **C-OVERLOAD** | Operator overloads do the unsurprising thing — `a + b` is commutative if mathematically so | `Vec + Vec` doing element-wise concat with surprising semantics |
| **C-DEREF** | `Deref`/`DerefMut` is ONLY for smart pointers (transparent wrappers). Never for "inheritance" or "API extension" | `impl Deref for User { type Target = UserData; }` |
| **C-CTOR** | Constructors are static *inherent* methods (`Foo::new`, `Foo::with_capacity`) — not trait methods | `impl Default for Foo { fn default() ... }` as the only constructor |

### 1.6 Flexibility

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-INTERMEDIATE** | Expose intermediate results — `Vec::pop()` returns the popped value, not just `()` | `fn process()` discards the value it just produced |
| **C-CALLER-CONTROL** | Caller decides where data lives — accept `impl Read`, not `File`; return owned, not boxed | API forces `Box<dyn Trait>` on the caller |
| **C-GENERIC** | Use generics over trait objects when the type is known at call site (monomorphization, inlining) | `fn read(r: &mut dyn Read)` in a hot path |
| **C-OBJECT** | Traits should be object-safe (`dyn Trait`) if there's any chance someone needs trait objects | `trait Foo { fn bar() -> Self; }` (associated fn returning Self breaks dyn) |

### 1.7 Type Safety

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-NEWTYPE** | Wrap raw scalars in a newtype to make illegal mixups a compile error | `fn transfer(from: u64, to: u64, amount: u64)` |
| **C-CUSTOM-TYPE** | Arguments carry meaning in *types*, not `bool` or `Option<()>` — replace `fn open(path, true)` with `fn open(path, Truncate::Yes)` | `fn parse(s: &str, strict: bool)` |
| **C-BITFLAG** | Sets of flags use the `bitflags` crate, not a raw enum | `enum Flags { A=1, B=2, C=4 }` + bitwise math by hand |
| **C-BUILDER** | Complex constructors with optional/many params use a Builder (in 2026: `bon` crate) | `fn new(a, b, c, d, e, f, g, h, i)` |

### 1.8 Dependability

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-VALIDATE** | Functions validate at the *boundary* — once inside, types carry the invariant | Re-checking the same email format at every layer |
| **C-DTOR-FAIL** | `Drop::drop` never fails. If cleanup can fail, expose an explicit `fn close()` that returns `Result` | `Drop::drop` calling fallible I/O with `.unwrap()` |
| **C-DTOR-BLOCK** | `Drop::drop` may block? Provide a non-blocking alternative (`close_async`, `disconnect`) | Async `Drop` impls — async drop is still unstable in 2026 |

### 1.9 Debuggability

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-DEBUG** | Every public type implements `Debug` (even if it just shows the type name) | `impl Debug` missing on errors logged via `tracing` |
| **C-DEBUG-NONEMPTY** | `Debug` output is never empty — at minimum show the type | `impl Debug for Foo { fn fmt() -> fmt::Result { Ok(()) } }` |

### 1.10 Future Proofing

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-SEALED** | Traits intended to be implemented only by the crate use the sealed pattern (private `Sealed` supertrait) | Public trait that secretly assumes finite implementors |
| **C-STRUCT-PRIVATE** | Public structs have private fields — exposing fields locks in representation and forbids invariants | `pub struct User { pub email: String }` — now you can never validate `email` again without a breaking change |
| **C-NEWTYPE-HIDE** | Newtypes hide implementation: don't auto-`Deref<Target=Inner>` or you've leaked the wrapped type | `pub struct UserId(pub Uuid)` defeats the newtype |
| **C-STRUCT-BOUNDS** | Don't repeat trait bounds on the struct definition that are already derivable on impls | `struct Foo<T: Clone> { v: T }` — let the impl block require `Clone` |

### 1.11 Necessities

| ID | Rule | Violation smell |
|----|------|-----------------|
| **C-STABLE** | A 1.0 crate's public deps are themselves 1.0+ (or the API does not re-export pre-1.0 types) | Stable crate v1.5 re-exporting `tokio::sync::Mutex` from `tokio 1.x` (fine — tokio is 1.0+) vs re-exporting a v0.x crate type |
| **C-PERMISSIVE** | The crate and its dep tree are MIT / Apache-2.0 / similarly permissive (or the license is documented loudly) | GPL-3.0 transitive dep without warning |

### 1.12 Sealed-trait recipe (C-SEALED)

The canonical 2026 pattern (stable since long before, but with Edition 2024 it's even more common):

```rust
// In your crate root
pub trait Component: private::Sealed {
    fn render(&self) -> String;
}

mod private {
    pub trait Sealed {}
}

// For each type you want to allow:
pub struct Button { /* ... */ }
impl private::Sealed for Button {}
impl Component for Button { fn render(&self) -> String { /* ... */ } }
```

Downstream crates can *use* `dyn Component` but cannot *implement* it. The compiler error says "private trait `private::Sealed` not satisfied" — document the seal in the trait's rustdoc so users don't waste time trying.

A 2026 alternative discussed in pre-RFC traffic is `pub trait Foo {} ; #[non_exhaustive] impl ...` but that's still unstable; the private-supertrait pattern is the production recipe today.

---

## 2. Error handling patterns — deep

The two-axis taxonomy (`library` vs `application`, `typed` vs `erased`) is the right mental model. The baseline (`language-idioms.md` §4) already covers the basic `thiserror`/`anyhow` split — here's the production-grade detail.

### 2.1 The four crates

| Crate | What it is | When to reach for it |
|-------|-----------|----------------------|
| **`thiserror`** | Derive macro to generate `Error + Display` impls on an enum/struct | Library public error type. One variant per failure mode. |
| **`anyhow`** | Erased `anyhow::Error` (heap-allocated trait object) + `.context()` chain | Application code where the *caller is the operator* — match-on-variant is never needed |
| **`snafu`** | Like `thiserror` + context selectors that produce structured contexts at call site | Cross-crate domains where every error site needs its own context type (large rust projects, GreptimeDB-style) |
| **`eyre`** / `color-eyre` | `anyhow` fork with pluggable reporters (colored, rich) and custom contexts | CLI / interactive tools; binary crates where pretty backtraces matter |

### 2.2 The decision tree

```
Will callers ever match on the error variant?
├── YES → typed error (thiserror or snafu)
│   ├── single crate → thiserror
│   └── multi-crate domain with rich context per call site → snafu
└── NO  → erased error (anyhow / eyre)
    ├── library? → still typed (callers may match later); never expose anyhow in pub API
    └── binary main + glue → anyhow (or eyre if you want pretty output)
```

### 2.3 Hybrid pattern — library + application boundary

The mistake is mixing `anyhow` into a library. The correct hybrid:

- **Library crate**: `thiserror` enum, `Result<T, MyError>` everywhere.
- **Binary crate** depending on the library: `anyhow::Result<T>`, library errors get `.context()` for human-readable framing.

```rust
// libdb/src/lib.rs
#[derive(Debug, thiserror::Error)]
pub enum DbError {
    #[error("connection failed: {0}")]
    Connect(#[source] sqlx::Error),
    #[error("query failed for {query}")]
    Query { query: String, #[source] source: sqlx::Error },
    #[error("constraint violation: {0}")]
    Constraint(String),
}

// app/src/main.rs
use anyhow::Context;
use libdb::DbError;

fn run() -> anyhow::Result<()> {
    let users = libdb::list_users()
        .context("failed to list users for /admin/users")?;
    // libdb::DbError is preserved as the source of the anyhow::Error chain
    Ok(())
}
```

`anyhow::Error::downcast_ref::<DbError>()` is still available if you really need to match — but if you find yourself doing that, the typed error should have been propagated.

### 2.4 The `#[from]` vs `#[source]` rule

| Attribute | Effect | When |
|-----------|--------|------|
| `#[from]` | Generates `From<Inner>` impl — enables `?` direct propagation, no manual mapping | Only when there is *exactly one* variant that wraps `Inner`. Two `#[from]` impls for the same source type = compile error |
| `#[source]` | Marks the field as the error's `source()` (i.e., chain parent), but does NOT generate `From` | When you wrap *and* add context fields (`query: String`) |
| `#[error(transparent)]` | Forwards `Display` and `source()` to the wrapped error | Pure "I'm just a different error type for the same failure" wrappers — preserves the original message |

```rust
#[derive(Debug, thiserror::Error)]
pub enum ApiError {
    // Direct ? propagation works:
    #[error(transparent)]
    Db(#[from] DbError),

    // Context preserved, but no automatic ? — caller must map:
    #[error("validation failed for field {field}")]
    Validation { field: String, #[source] source: ValidationError },

    // Composite — caller writes `e.map_err(ApiError::custom)`
    #[error("unexpected: {0}")]
    Custom(String),
}
```

### 2.5 Result extension traits — the `.context()` pattern (when you don't have anyhow)

In libraries, you can't use `anyhow::Context` (you don't want to drag anyhow into deps). Roll your own extension trait:

```rust
pub trait ResultExt<T, E> {
    fn with_query(self, query: &str) -> Result<T, DbError>;
}

impl<T> ResultExt<T, sqlx::Error> for Result<T, sqlx::Error> {
    fn with_query(self, query: &str) -> Result<T, DbError> {
        self.map_err(|e| DbError::Query { query: query.into(), source: e })
    }
}

// Usage:
let row = sqlx::query("SELECT * FROM users")
    .fetch_one(&pool).await
    .with_query("SELECT * FROM users")?;
```

### 2.6 Panic policy

The 2026 production stance:

1. **Library code**: never panic on input the caller can produce. `unreachable!()` only when a violated invariant means the program is broken, never when bad input could trigger it.
2. **Binary `main`**: `fn main() -> anyhow::Result<()>` so unhandled errors print the chain via `Debug`, not panic.
3. **`unwrap()` / `expect()`**: only in tests, examples, build scripts, prototype `main` — never on a path that runs under load.
4. **`#[track_caller]` on panic helpers**: when you must write a panic helper, decorate it so the panic message points at the *caller*, not your helper.
5. **`std::panic::catch_unwind`**: only at FFI boundaries (Rust callable from C, Python, Wasm host). Use of `catch_unwind` to "recover" inside a Rust app is a code smell — design around it instead.

### 2.7 Retry / recovery patterns

Two production crates:

| Crate | Model | Use |
|-------|-------|-----|
| **`tokio-retry`** | Stream-based — apply a retry policy to any `Future` factory | Per-call retries with simple exponential backoff |
| **`backoff`** (also published as `backon` — different crate) | Builder-based — pluggable backoff strategies (constant, exponential, fibonacci) with jitter | Long-running tasks, daemons, idempotent operations |

```rust
use backoff::{ExponentialBackoffBuilder, future::retry};

retry(
    ExponentialBackoffBuilder::new()
        .with_initial_interval(Duration::from_millis(50))
        .with_max_interval(Duration::from_secs(5))
        .with_max_elapsed_time(Some(Duration::from_secs(30)))
        .build(),
    || async {
        client.get("https://api.example.com").send().await
            .map_err(backoff::Error::transient)
    },
).await?;
```

---

## 3. Project structure & cargo workspaces

The baseline shows a single-crate layout. Real production Rust at scale is a **workspace**, often a **bin+lib hybrid**, with **internal crates** for forced layering.

### 3.1 Workspace organization patterns

#### Pattern A — Layered (Clean / Hexagonal)

```
backend/
├── Cargo.toml                  # [workspace] root
├── Cargo.lock
├── rust-toolchain.toml
├── deny.toml
├── crates/
│   ├── domain/                 # pure: entities, value objects, ports (traits)
│   │   └── src/lib.rs
│   ├── application/            # use cases — depends on domain only
│   │   └── src/lib.rs
│   ├── infra-pg/               # postgres adapter — depends on domain
│   │   └── src/lib.rs
│   ├── infra-redis/            # redis adapter — depends on domain
│   │   └── src/lib.rs
│   ├── http/                   # axum handlers — depends on application
│   │   └── src/lib.rs
│   └── server/                 # bin: wires everything
│       └── src/main.rs
└── xtask/                      # workspace tooling (custom cargo subcmds)
    └── src/main.rs
```

The `domain` crate has zero deps on infra. If you accidentally add `sqlx` to its `Cargo.toml`, `cargo check -p domain` exposes the leak instantly. **Crate boundaries enforce architecture.**

#### Pattern B — Feature-sliced

```
crates/
├── shared/         # cross-cutting types
├── feature-auth/   # full vertical slice: domain + db + http
├── feature-billing/
├── feature-search/
└── server/         # composes all features into one binary
```

Use this when features ship independently or when team ownership maps cleanly to features.

#### Pattern C — Bin+Lib hybrid (single crate)

```
my-tool/
├── src/
│   ├── lib.rs      # all logic lives here
│   └── main.rs     # tiny: `fn main() -> anyhow::Result<()> { my_tool::run() }`
└── tests/
    └── cli.rs      # integration via assert_cmd
```

The lib is testable; the bin is a 5-line shell. This is the default for any CLI more complex than `hello-world`.

### 3.2 `examples/`, `benches/`, `tests/` — the cargo-known directories

| Dir | Compile target | Purpose | Gotcha |
|-----|---------------|---------|--------|
| `tests/` | One binary per `.rs` file | Integration tests — black-box against the crate's public API | Each file is its own crate, so `mod common;` requires `tests/common/mod.rs` (not `tests/common.rs`) |
| `examples/` | One binary per `.rs` file | Compilable examples that ship with the crate — appear in rustdoc | Run with `cargo run --example name` |
| `benches/` | One binary per `.rs` file | `criterion` / `divan` benchmarks | Need `harness = false` in Cargo.toml + criterion dev-dep |
| `build.rs` | Pre-compile step | Code generation, env probing, link config | Avoid heavy work — slows every clean build of every dependent |

### 3.3 Workspace `Cargo.toml` — the 2026 idiomatic root

```toml
[workspace]
resolver = "3"                       # Edition 2024 default — better feature unification
members = ["crates/*", "xtask"]
default-members = ["crates/server"]  # `cargo run` from root → run the server bin

[workspace.package]
edition      = "2024"
rust-version = "1.85"                # MSRV — enforced by CI via cargo-msrv
license      = "MIT OR Apache-2.0"
repository   = "https://github.com/org/backend"

[workspace.dependencies]
# Pin once, inherit everywhere
tokio       = { version = "1.45", features = ["full"] }
axum        = { version = "0.8" }
serde       = { version = "1.0",  features = ["derive"] }
sqlx        = { version = "0.8",  features = ["postgres", "runtime-tokio-rustls"] }
tracing     = "0.1"
thiserror   = "2.0"
anyhow      = "1.0"
jiff        = "0.2"
uuid        = { version = "1.10", features = ["v7", "serde"] }

[workspace.lints.rust]
unsafe_code           = "forbid"     # most workspaces; or "deny" with explicit allows
missing_debug_impls   = "warn"
missing_docs          = "warn"        # public crates
unreachable_pub       = "warn"
unused_lifetimes      = "warn"
unused_must_use       = "deny"

[workspace.lints.clippy]
pedantic            = { level = "warn", priority = -1 }
unwrap_used         = "warn"
expect_used         = "warn"
dbg_macro           = "warn"
todo                = "warn"
print_stdout        = "warn"          # tracing only
print_stderr        = "warn"
indexing_slicing    = "warn"          # forces .get() over [i]
exhaustive_enums    = "warn"          # encourages #[non_exhaustive]
exhaustive_structs  = "warn"
unused_async        = "warn"
```

Member crates pick up the lints with:

```toml
# crates/domain/Cargo.toml
[lints]
workspace = true
```

### 3.4 Feature flags — additive only

This is one of the most violated rules in the ecosystem. **Features compose additively** because Cargo unifies the union across the whole graph. If two flags are mutually exclusive (`std` vs `no_std`, `runtime-tokio` vs `runtime-async-std`), `cargo build --all-features` produces a broken build and tools like `cargo-hack --feature-powerset` give false positives.

#### Correct patterns

```toml
[features]
default = ["json"]
json    = ["dep:serde_json"]
yaml    = ["dep:serde_yaml"]
# adding "yaml" never *removes* "json" — they accumulate
```

#### Wrong patterns (and the fix)

```toml
# WRONG — only one runtime may be active
[features]
runtime-tokio      = []
runtime-async-std  = []

# FIX — separate crates, or a runtime-trait abstraction the user picks
# my-lib-tokio = { ... }
# my-lib-asyncstd = { ... }
```

Helpful tools:

- `cargo-hack --feature-powerset --no-dev-deps check` — builds every subset of features. CI gate.
- `cargo-hack --each-feature` — builds each feature in isolation (faster, less thorough).

### 3.5 `[patch]` and `[replace]` — dependency overrides

| Mechanism | Use | Gotcha |
|-----------|-----|--------|
| `[patch.crates-io]` | Override a transitive dep with a git fork or local path **without** changing any direct deps | Patched dep must be **semver-compatible** with the published version. For incompatible swaps, use a fork that bumps its own version |
| `[patch."https://github.com/foo/bar"]` | Override a git dep | Same compatibility rule |
| `[replace]` | Older, less flexible — deprecated in favor of `[patch]` | Avoid in new code |

```toml
# Cargo.toml at workspace root — force everything to use your fork while a fix lands upstream
[patch.crates-io]
hyper = { git = "https://github.com/my-org/hyper", branch = "fix-issue-1234" }
```

Verify with `cargo tree -i hyper` — confirms the patched version is the one actually selected.

---

## 4. Cargo & toolchain — the 2026 productivity stack

The baseline lists five tools (`cargo-deny`, `cargo-audit`, `cargo-machete`, `cargo-nextest`, `cargo-hack`). The full 2026 stack is below — column "When to add to CI" is opinionated and battle-tested.

| Tool | Purpose | When to add to CI |
|------|---------|-------------------|
| `cargo-nextest` | Parallel test runner with per-test isolation; ~3x faster than `cargo test` for medium+ workspaces; partition support for sharding | Always. Replace `cargo test` in CI |
| `cargo-deny` | Lint dependency graph: licenses, advisories, banned crates, duplicate versions, allowed sources | Always. v0.19 (2026-01) is the current floor |
| `cargo-audit` | RUSTSEC vulnerability scanner against `Cargo.lock` | Always — but cargo-deny includes the same advisory check, so often redundant if cargo-deny is on |
| `cargo-vet` | Mozilla's supply-chain provenance — audit-and-import trusted vetting from peer orgs (Google, Mozilla, Embark) | Larger orgs / orgs with security review SLA. Optional for small teams |
| `cargo-hack` | Run `cargo {check,test,build}` across the feature powerset / per-feature / MSRV matrix | Always for library crates with non-trivial features |
| `cargo-machete` | Fast (text-scan) unused-dep detector — runs on every PR in <2s on huge workspaces | Always — false positives are rare and easy to allowlist |
| `cargo-udeps` | Compile-and-analyze unused-dep detector — slower, requires nightly, more accurate than machete | Optional — run weekly, not per-PR |
| `cargo-msrv` | Find / verify the minimum supported Rust version via binary-search of `cargo check` | Library crates declaring an MSRV. Add `cargo msrv verify` to CI |
| `cargo-semver-checks` | Detect breaking API changes (semver violations) before release | Library crates publishing to crates.io. v0.47 (2026) — runs as a release gate |
| `cargo-public-api` | List + diff the public API surface; complements semver-checks with a human-readable diff in PRs | Library crates; bot-post the API diff on PRs that touch `pub` items |
| `cargo-mutants` | Mutation testing — inserts bugs (operator swaps, default returns) and verifies tests fail | Long-running CI on `main` (weekly) — too slow for per-PR. Aim for 70%+ mutation score |
| `cargo-llvm-cov` | LLVM source-based coverage — region-level, integrates with nextest and codecov | Always — emits `lcov.info` / Cobertura XML |
| `cargo-fuzz` | libFuzzer-based fuzzing for any input-parsing surface | Parsers, deserializers, format readers — add a dedicated fuzz job; nightly toolchain |
| `cargo-flamegraph` | One-shot flamegraph generation via `perf` (Linux) or `dtrace` (macOS) | Local profiling; rarely CI |
| `cargo-expand` | Print code after macro expansion — debugging derive macros, `#[tokio::main]`, etc. | Local only |
| `cargo-asm` / `cargo-show-asm` | Inspect generated assembly per function | Local only — used during hot-path tuning |
| `cargo-bloat` | What part of the binary is biggest? Per-crate / per-fn breakdown | Pre-release size analysis — surface in CI report only |
| `cargo-dist` | Build, sign, and publish multi-platform release archives (binary + checksum + installer scripts) | Bin crates with releases; replaces a custom GitHub Actions setup |
| `cargo-zigbuild` | Cross-compile using `zig` as the linker — handles libc versions trivially, supports apple-darwin universal2 | Bin crates targeting many OSes |
| `cargo-release` | Automate version bump, changelog gen, git tag, publish | Library crates that publish often |
| `cargo-geiger` | Survey `unsafe` blocks across the whole dep tree — flags `unsafe`-heavy deps | Optional — quarterly review or pre-1.0 gate |
| `cross` | Docker-image-based cross compilation (older alternative to zigbuild) | Targets zigbuild doesn't support yet (Windows GNU, BSDs) |
| `cargo-watch` | Re-run on file change — `cargo watch -x check -x test` | Local dev only |
| `cargo-make` | Task runner (heavier than `xtask`-pattern) | When you have many recipes and a polyglot team |

### 4.1 The minimum-viable 2026 CI matrix

```yaml
jobs:
  test:
    steps:
      - uses: actions-rust-lang/setup-rust-toolchain@v1
      - uses: taiki-e/install-action@v2
        with: { tool: cargo-nextest,cargo-deny,cargo-hack,cargo-machete,cargo-llvm-cov }
      - run: cargo fmt --check
      - run: cargo clippy --all-targets --all-features -- -D warnings
      - run: cargo deny check
      - run: cargo machete
      - run: cargo hack --feature-powerset --no-dev-deps check
      - run: cargo llvm-cov nextest --all-features --lcov --output-path lcov.info
      - uses: codecov/codecov-action@v4
        with: { files: lcov.info }

  msrv:
    steps:
      - uses: actions-rust-lang/setup-rust-toolchain@v1
        with: { toolchain: "1.85" }
      - run: cargo check --all-features

  semver:  # library crates only
    if: contains(github.event.pull_request.labels.*.name, 'release')
    steps:
      - uses: obi1kenobi/cargo-semver-checks-action@v2
```

### 4.2 Full `deny.toml` (annotated)

```toml
# https://embarkstudios.github.io/cargo-deny/
[graph]
targets = [
  { triple = "x86_64-unknown-linux-gnu" },
  { triple = "aarch64-apple-darwin"  },
  { triple = "x86_64-pc-windows-msvc" },
]
# Exclude dev-deps from license/ban checks (allow GPL test fixtures, etc.)
exclude-dev = true

[advisories]
# RUSTSEC database mode
version = 2
yanked  = "deny"
ignore  = [
  # "RUSTSEC-YYYY-NNNN", # justify each ignore with a comment and an expiry
]

[licenses]
version = 2
allow = [
  "MIT",
  "Apache-2.0",
  "Apache-2.0 WITH LLVM-exception",
  "BSD-2-Clause",
  "BSD-3-Clause",
  "ISC",
  "Unicode-DFS-2016",
  "Unicode-3.0",     # required by ICU4X after 2024
  "Zlib",
  "MPL-2.0",          # weak copyleft — usually OK; remove if you ship a proprietary binary
  "CC0-1.0",
]
confidence-threshold = 0.93
exceptions = [
  # Per-crate license overrides if needed
]

[bans]
multiple-versions = "warn"      # warn — duplicate-version pressure is real
wildcards         = "deny"      # forbid "*" in dep specs
deny = [
  # Old async runtimes
  { name = "async-std", reason = "we standardize on tokio" },
  # Old TLS
  { name = "openssl", reason = "we use rustls" },
  # Old time crate when migrating to jiff
  # { name = "chrono", reason = "migrating to jiff per ADR-0007" },
]
skip = [
  # Crates allowed to appear in multiple versions during migration windows
]
skip-tree = []

[sources]
unknown-registry = "deny"
unknown-git      = "deny"
allow-git = [
  # "https://github.com/our-org/our-fork",
]
```

---

## 5. Testing strategy — the seven layers

Rust's testing story in 2026 is deeper than `#[test]`. Production codebases compose seven layers; pick the right one for each contract.

| Layer | Tool (2026) | What it catches |
|-------|-------------|-----------------|
| Unit (intra-module) | `#[cfg(test)] mod tests` | Branch logic, edge cases on pure fns |
| Parameterized | `rstest` 0.26 | Tabular variations; fixture injection |
| Property-based | `proptest`, `quickcheck` | Round-trip, idempotency, invariants |
| Snapshot | `insta` | Renderer/formatter output drift |
| Integration (in-process) | `tests/*.rs` | Public API contract |
| Integration (out-of-process) | `assert_cmd` + `predicates` + `testcontainers` + `wiremock` | CLI exit codes, DB-backed flows, HTTP mocks |
| Fuzz / sanitize | `cargo-fuzz`, `afl.rs`, `miri`, asan/tsan/lsan | UB, memory safety on `unsafe`, panic on malformed input |

### 5.1 `rstest` — parameterized + fixtures

Beyond the baseline's `#[case]` matrix, `rstest` shines for **fixtures** that compose:

```rust
use rstest::{fixture, rstest};

#[fixture]
fn pool() -> sqlx::PgPool { /* shared setup */ }

#[fixture]
fn user(#[default("alice")] name: &str) -> User { User::new(name) }

#[rstest]
#[case::admin("alice", true)]
#[case::guest("bob", false)]
#[awt]                                // top-level await — fixtures can be async
async fn authorizes_correctly(
    pool: sqlx::PgPool,
    #[case] user_name: &str,
    #[case] expected: bool,
) {
    // pool injected, parameters from #[case]
}
```

### 5.2 `proptest` vs `quickcheck`

| | proptest | quickcheck |
|---|---|---|
| Shrinking | Integrated, generic, deterministic | Type-specific; can be flaky |
| Strategy ergonomics | `prop::collection::vec(0i32..10, 0..100)` — composable | Macros simpler but less expressive |
| Persistence | Saves failing seeds to `proptest-regressions/` | None |
| 2026 verdict | **Default choice** | Legacy; use only if quickcheck-style traits are needed |

### 5.3 Snapshot testing with `insta`

```rust
#[test]
fn renders_invoice() {
    let invoice = Invoice::demo();
    insta::assert_yaml_snapshot!(invoice, {
        ".timestamp" => "[timestamp]",          // redact non-deterministic fields
        ".id"        => insta::dynamic_redaction(|v, _| format!("[uuid:{}]", v.as_str().unwrap().len())),
    });
}
```

Run `cargo insta review` to accept/reject diffs interactively. `cargo insta accept` in CI is **wrong** — always require human review.

### 5.4 `mockall` vs hand-rolled fakes — when to choose what

| Approach | When |
|----------|------|
| **Hand-rolled fakes** (a struct that implements the same trait with deterministic in-memory state) | **Default**. Fakes are reusable across tests, behave like real impls, don't tie tests to call order |
| **`mockall`** (procedural macro generating `MockTrait` with `expect_*().returning(...)`) | When the contract is complex enough that expressing behavior as an in-memory struct is more work than declaring expectations — e.g., asserting on call order, side-effect sequences |

The baseline correctly prefers "trait injection + hand-rolled fakes." The escalation rule: **add `mockall` only when the test now reads less clearly than the fake would.** Often the cost is invisible until you delete the test six months later and realize it was over-specifying.

### 5.5 `testcontainers-rs`

```rust
use testcontainers::{clients::Cli, images::postgres::Postgres};

#[tokio::test]
async fn user_repo_round_trip() {
    let docker = Cli::default();
    let pg = docker.run(Postgres::default());
    let url = format!("postgres://postgres@localhost:{}/postgres", pg.get_host_port_ipv4(5432));

    let pool = sqlx::PgPool::connect(&url).await.unwrap();
    sqlx::migrate!().run(&pool).await.unwrap();

    let repo = PgUserRepo::new(pool);
    let id = repo.create("alice@example.com").await.unwrap();
    assert_eq!(repo.find(id).await.unwrap().unwrap().email, "alice@example.com");
}
```

The container is dropped when `pg` goes out of scope. **Use the `Cli` once per test, not once per module** — spinning up a container per test is slow but isolating.

### 5.6 `wiremock` (Rust crate) — HTTP mocks

```rust
use wiremock::{matchers::*, Mock, MockServer, ResponseTemplate};

#[tokio::test]
async fn fetches_user_profile() {
    let server = MockServer::start().await;
    Mock::given(method("GET"))
        .and(path("/users/42"))
        .respond_with(ResponseTemplate::new(200).set_body_json(serde_json::json!({
            "id": 42, "name": "alice"
        })))
        .expect(1)                              // assert called exactly once on drop
        .mount(&server).await;

    let client = MyApiClient::new(server.uri());
    let user = client.fetch_user(42).await.unwrap();
    assert_eq!(user.name, "alice");
}
```

### 5.7 `assert_cmd` + `predicates` for CLIs

```rust
use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn prints_version() {
    Command::cargo_bin("mytool").unwrap()
        .arg("--version")
        .assert()
        .success()
        .stdout(predicate::str::starts_with("mytool"))
        .stderr(predicate::str::is_empty());
}

#[test]
fn rejects_bad_input() {
    Command::cargo_bin("mytool").unwrap()
        .arg("--bad-flag")
        .write_stdin("garbage")
        .assert()
        .failure()
        .code(2);                               // exit code precisely 2
}
```

### 5.8 Benchmarks — `criterion` vs `divan`

| | `criterion` | `divan` |
|---|---|---|
| Status | Mature, de facto standard | Newer (~2023+), gaining ground |
| Statistical analysis | Yes (sampling, outliers, regressions, plots) | Lighter, faster |
| Output | HTML reports, baseline persistence, regression detection | Console table; baseline comparison |
| Async support | Via the `tokio` feature | Built-in `#[divan::bench(args = ...)]` |
| 2026 use | **Production performance regressions** (CI gates, release notes) | **Micro-bench iteration loop** (faster compile, plain output) |

### 5.9 Fuzz — `cargo-fuzz` + libfuzzer-sys vs `afl.rs`

```rust
// fuzz/fuzz_targets/parse.rs
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Ok(s) = std::str::from_utf8(data) {
        let _ = my_crate::parse(s); // panic or assertion failure → libfuzzer reports it
    }
});
```

`cargo fuzz run parse -- -max_total_time=60` runs for a minute. Add a nightly CI job that runs for ~5 min per parser; corpus is committed to the repo.

| | `cargo-fuzz` (libfuzzer) | `afl.rs` |
|---|---|---|
| Engine | LLVM libFuzzer | AFL++ |
| Coverage feedback | Inline (sancov) | Forkserver + edge coverage |
| Setup | Easier — `cargo fuzz init` | More involved — needs afl-clang or harness setup |
| 2026 default | **libfuzzer-based `cargo fuzz`** | Reserved for projects needing AFL++'s aggressive mutation strategies |

### 5.10 `miri` — UB detection

```sh
rustup +nightly component add miri
cargo +nightly miri test --lib
```

Miri is an interpreter that catches:

- Out-of-bounds memory access
- Use-after-free
- Invalid `unsafe` (uninit reads, alignment, aliasing violations)
- Data races (with `MIRIFLAGS=-Zmiri-disable-isolation` and `-Zmiri-many-seeds`)

**Slow** — only viable on focused unit tests, not whole integration suites. Run on every PR for `unsafe`-using crates; weekly otherwise. As of 2026-05, the Miri team is migrating Tree Borrows toward default behavior; pass both Stacked and Tree Borrows when possible (see [`rust-language-spec.md` §6.3](./rust-language-spec.md#63-stacked-borrows--tree-borrows)).

### 5.11 Sanitizers — asan / tsan / lsan / msan

```sh
RUSTFLAGS="-Z sanitizer=address" cargo +nightly test --target x86_64-unknown-linux-gnu
RUSTFLAGS="-Z sanitizer=thread"  cargo +nightly test --target x86_64-unknown-linux-gnu
```

Use when you have FFI surfaces or `unsafe` that handles raw pointers. The `-Zbuild-std` flag is sometimes needed for full stdlib instrumentation.

### 5.12 Code coverage — `cargo-llvm-cov`

```sh
cargo install cargo-llvm-cov
cargo llvm-cov nextest --all-features --lcov --output-path lcov.info
cargo llvm-cov nextest --all-features --html         # open target/llvm-cov/html/index.html
```

LLVM source-based instrumentation tracks coverage at the *region* level (not just lines) — more accurate than the older `tarpaulin`-style binary instrumentation. Integrates with codecov, coveralls, gitlab-ci's native Cobertura.

### 5.13 Mutation testing — `cargo-mutants`

```sh
cargo install cargo-mutants
cargo mutants --in-place              # mutate, run tests, report which mutants survived
cargo mutants --in-diff main.diff     # only mutate code changed in the PR
```

Mutants like `x + y` → `x - y`, `if x { ... }` → `if !x { ... }`, `return Ok(v)` → `return Ok(Default::default())`. A surviving mutant means **a test that should have caught this bug didn't exist**. Target ≥70% mutation score.

Run **weekly** on `main`, not per-PR — full runs take hours.

---

## 6. Performance practices

### 6.1 When to profile (and with what)

Rule: **never optimize without a profile**. The compiler is too smart; the hot path is rarely where you think.

| Tool | Platform | Mode | Use |
|------|----------|------|-----|
| `perf` + `cargo flamegraph` | Linux | CPU sampling | First pass — find which fn dominates wall time |
| `samply` | Linux, macOS, Windows | CPU sampling, Firefox Profiler UI | Modern cross-platform replacement for perf+flamegraph; recommended 2026 default |
| `cargo flamegraph` (via dtrace) | macOS | CPU sampling | Same as perf but via dtrace |
| `pprof-rs` (in-process) | Any | CPU + heap sampling, exposed via HTTP endpoint | Always-on profiling in long-running servers |
| `dhat` / `dhat-rs` | Any | Heap allocation analysis | "Why is my RSS climbing?" — finds allocation hot spots |
| `cargo-bloat` | Any | Binary size | "Which crate is 30% of my binary?" |
| Miri / heaptrack | Linux | Memory access patterns | Cache misses, allocation churn |

### 6.2 Allocator choice

The default system allocator on Linux (glibc) is famously slow under multi-threaded contention. Drop-in replacements:

```rust
// In your bin crate's main.rs:
#[global_allocator]
static GLOBAL: mimalloc::MiMalloc = mimalloc::MiMalloc;
```

| Allocator | Crate | Notes (2026) |
|-----------|-------|--------------|
| **mimalloc** | `mimalloc` | Microsoft Research. **Default recommendation** — broad-platform support; ~4% perf gain across the board in rustc's own benchmarks |
| **jemalloc** | `tikv-jemallocator` | Long-standing favorite; the original `jemallocator` crate is unmaintained. Marginally better on some workloads, more memory headroom |
| **snmalloc** | `snmalloc-rs` | Microsoft Research. Best multi-thread scaling on contention-heavy workloads; LLVM/clang dep is heavier |
| **System (default)** | none | Glibc malloc — accept the loss in exchange for zero ops/binary-size cost |

### 6.3 SIMD — `std::simd` status

`std::simd` (a.k.a. `portable_simd`) is **still unstable** as of 1.85 (nightly only). For production:

| Need | Crate | Status |
|------|-------|--------|
| Portable SIMD on stable | `wide` | Maintained, production-ready. Falls back to autovectorization-friendly scalar code |
| Tight x86/ARM intrinsics | `std::arch` | Stable since long ago — `is_x86_feature_detected!("avx2")` runtime gating |
| Future: stable portable SIMD | `std::simd` | Track RFC 2366. Once stabilized, replace `wide`/`packed_simd` |
| Legacy | `packed_simd` | Unmaintained on stable. Don't add to new code |

### 6.4 `#[inline]` policy

| Annotation | When |
|------------|------|
| (default — no annotation) | Almost always. Trust the compiler |
| `#[inline]` | Small, hot, cross-crate functions where the compiler may not inline (cross-crate inlining needs `-Clto` or an inline hint) |
| `#[inline(always)]` | Profile-proven hot fn that LLVM is leaving uninlined. Rare. Document why |
| `#[inline(never)]` | Splits up large fns for instruction-cache friendliness, or to force a function call boundary (debugging, benchmarking) |
| `#[cold]` | Error paths, slow paths. Hints LLVM to put the body in a cold section, improving I-cache locality of the hot path |

### 6.5 PGO and BOLT

Profile-Guided Optimization runs the binary once to gather profile data, then recompiles using the profile. Real-world 10–20% speedups on CPU-bound code.

```sh
# Step 1: build with instrumentation
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" \
    cargo build --release --target x86_64-unknown-linux-gnu

# Step 2: run a representative workload
./target/x86_64-unknown-linux-gnu/release/myapp --bench-workload

# Step 3: merge profiles
llvm-profdata merge -o /tmp/pgo-data/merged.profdata /tmp/pgo-data

# Step 4: rebuild using the profile
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data/merged.profdata" \
    cargo build --release --target x86_64-unknown-linux-gnu
```

BOLT (post-link binary optimizer, Linux ELF only) layered on top of PGO can stack another 5–15% — used internally by the Rust project to optimize rustc itself. For your own binaries, `cargo-pgo` automates the cycle.

### 6.6 Release-profile tuning

`Cargo.toml` for binary crates:

```toml
[profile.release]
lto              = "fat"      # whole-program inlining; build time ~2-3x
codegen-units    = 1          # max optimization at the cost of parallelism
panic            = "abort"    # smaller binary, faster panic path; lose unwind (no catch_unwind)
strip            = "symbols"  # strip debug info; cuts binary 30-60%
opt-level        = 3          # speed; use "z" or "s" for size

[profile.release-with-debug]  # for production with backtraces
inherits = "release"
debug    = "line-tables-only" # symbolicate panics + flamegraphs without bloating to full DWARF
strip    = "none"

[profile.release-fast-compile] # day-to-day "release-ish" builds
inherits      = "release"
lto           = "thin"   # 90% of fat-LTO's benefit at ~1.5x compile time
codegen-units = 16
```

### 6.7 Zero-copy patterns

| Pattern | When |
|---------|------|
| `Cow<'_, str>` | API may borrow or own depending on input — caller decides |
| `bytes::Bytes` (the `bytes` crate) | Reference-counted byte buffer, cheap clone, used heavily in tokio/hyper |
| `bumpalo::Bump` arena | Many short-lived allocations with a shared lifetime — request handling, AST construction. Drop the arena, drop all of them at once |
| `serde(borrow)` | `Deserialize<'de>` with borrowed `&'de str` fields — zero-copy JSON parsing |
| `rkyv` | Zero-copy deserialization — payload is the in-memory layout. Trade serde-ergonomics for nanosecond reads |
| `Arc<[u8]>` over `Vec<u8>` | Read-only buffers shared across tasks/threads — one allocation, many views |

### 6.8 Compile-time performance

This is a separate concern from runtime perf, and 2026 makes it manageable:

- **Workspace deps** (`[workspace.dependencies]`) — pin once, build once. Saves rebuild storms when bumping versions.
- `sccache` — distributed compile cache. CI killer-feature; commute-friendly.
- `lld` / `mold` linker — `RUSTFLAGS="-C link-arg=-fuse-ld=mold"` — 5-10x faster final link on Linux.
- `[profile.dev]` — `opt-level = 1` for deps that are slow at `-O0` (regex, num-bigint).
- `cargo-chef` — Docker layer cache for deps separately from app code.

---

## 7. Security practices

### 7.1 RUSTSEC workflow

`cargo audit` and `cargo deny check advisories` both consume the [RustSec Advisory Database](https://rustsec.org/) — the curated, community-maintained vuln registry.

```yaml
# .github/workflows/security.yml
on:
  push: { branches: [main] }
  schedule: [{ cron: '0 6 * * *' }]   # daily — new CVEs land overnight
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: rustsec/audit-check@v2
        with: { token: ${{ secrets.GITHUB_TOKEN }} }
```

### 7.2 `cargo-vet` — provenance and trust

`cargo-vet` lets you record "I (or someone I trust) reviewed this crate version." Audit imports from peer organizations (Mozilla, Google, Bytecode Alliance, Embark) reduce the per-org cost of vetting the dep tree.

```sh
cargo vet init                        # generates supply-chain/audits.toml and config.toml
cargo vet                             # see what is unaudited
cargo vet diff serde 1.0.190 1.0.193  # what changed between two versions?
cargo vet certify serde 1.0.193       # record an audit
```

In `supply-chain/config.toml`:

```toml
[imports.google]
url = "https://raw.githubusercontent.com/google/rust-crate-audits/main/audits.toml"

[imports.mozilla]
url = "https://hg.mozilla.org/mozilla-central/raw-file/tip/supply-chain/audits.toml"

[imports.embark]
url = "https://raw.githubusercontent.com/EmbarkStudios/rust-ecosystem/main/audits.toml"
```

### 7.3 Secret hygiene — `secrecy` + `zeroize`

```rust
use secrecy::{Secret, ExposeSecret, SecretString};

#[derive(Debug)]   // Debug is safe — SecretString redacts itself
struct Config {
    db_url: String,
    api_key: SecretString,   // [REDACTED] in Debug, no Display
}

fn make_request(cfg: &Config) {
    let key = cfg.api_key.expose_secret();  // explicit, grep-able
    // key is &str — but the wrapping prevents accidental logs / serde leaks
}
```

`zeroize` clears memory on drop:

```rust
use zeroize::Zeroize;

#[derive(Zeroize)]
#[zeroize(drop)]
struct Password(String);
// On drop, the String's bytes are overwritten with zeros before deallocation
```

Combine: `Secret<Zeroizing<Vec<u8>>>` for cryptographic keys — redacted *and* zeroed on drop.

### 7.4 Constant-time comparison — `subtle`

```rust
use subtle::ConstantTimeEq;

if user_token.ct_eq(&stored_token).into() {
    // accept
}
```

Plain `==` on `&[u8]` short-circuits on the first mismatched byte — a timing oracle. `subtle::ConstantTimeEq` runs in constant time regardless of input.

### 7.5 TLS — `rustls` over `native-tls`

The 2026 ecosystem default is **`rustls`**:

| | `rustls` | `native-tls` |
|---|---|---|
| Implementation | Pure Rust | Wraps SChannel (Win), Secure Transport (macOS), OpenSSL (Linux) |
| Memory safety | Yes (no unsafe in the TLS stack) | Inherits whatever the OS provides |
| Cipher policy | Modern only (TLS 1.2+, no RC4, no MD5) | Whatever the OS allows |
| FIPS | `rustls-fips` variant with FIPS-validated crypto | Inherits OS posture |
| Build deps | None — works on Alpine/scratch | Requires OpenSSL headers (frustrating on Alpine/Windows) |
| **2026 default** | **Yes** | Only when interoperability with system trust stores is required and rustls-native-certs isn't enough |

Pick the underlying crypto backend:

```toml
# Use ring (default, BoringSSL-derived) — broadest platform support
rustls = "0.23"

# Or aws-lc-rs (AWS's BoringSSL fork) — FIPS-validatable, faster on aarch64
rustls = { version = "0.23", default-features = false, features = ["aws_lc_rs"] }
```

### 7.6 Crypto crate ecosystem

| Need | Crate |
|------|-------|
| AEAD (AES-GCM, ChaCha20-Poly1305) | `aes-gcm`, `chacha20poly1305` (RustCrypto) |
| Hashing (SHA-2, SHA-3, BLAKE3) | `sha2`, `sha3`, `blake3` |
| Password hashing | `argon2` (RustCrypto) — Argon2id is the 2026 default |
| Public-key (Ed25519, X25519) | `ed25519-dalek`, `x25519-dalek` |
| Postquantum (ML-KEM, ML-DSA) | `pqcrypto`, `ml-kem` |
| Mid-level all-in-one | `ring`, `aws-lc-rs` |
| TLS | `rustls` (consumes one of the above) |

The **RustCrypto** organization is the dominant ecosystem for primitives. `ring` and `aws-lc-rs` provide higher-level "batteries-included" packages used by `rustls`.

### 7.7 `cargo-geiger` — unsafe survey

```sh
cargo install cargo-geiger
cargo geiger --output-format Json > unsafe-report.json
```

Reports the count of `unsafe fn`, `unsafe impl`, and `unsafe` blocks per dep. Use as a quarterly review tool — drives "should we replace this dep?" conversations.

Rule of thumb: **a CVSS-7 vuln in a 20%-unsafe crate is far more urgent than the same CVSS in a 0%-unsafe crate.** Geiger gives you the denominator.

### 7.8 crates.io trusted publishing (2025-2026 rollout)

Since late 2025, crates.io supports OpenID Connect-based trusted publishing — CI workflows authenticate as the publisher without long-lived API tokens. Pattern:

1. `cargo owner --add github:my-org:publish-bots <crate>`
2. In the workflow: `uses: rust-lang/crates-io-auth-action@v1` to mint a short-lived token.
3. `cargo publish` uses the token.

No more `CARGO_REGISTRY_TOKEN` secret. **Adopt for any new publish workflow in 2026.**

> For the catalog of injection/TOCTOU/path-traversal/regex-DoS misuse, see [`rust-anti-patterns.md` §12](./rust-anti-patterns.md#12-security-pitfalls).

---

## 8. Async ecosystem — structured concurrency

The baseline covers `JoinSet`, `tokio::select!`, bounded channels, and the MutexGuard rule. This section adds the **structured-concurrency patterns** that make a tokio program reliable, not just correct.

### 8.1 Runtime choice — Tokio dominates

| Runtime | 2026 niche |
|---------|------------|
| **`tokio`** | **Default for everything except specialized niches.** Net I/O, HTTP, DB, the entire `axum`/`hyper`/`sqlx`/`reqwest`/`tonic` ecosystem |
| `async-std` | Maintenance-mode. Don't pick for new code |
| `smol` / `async-executor` | Tiny embeddable executor — embedded, plugin hosts, sandboxed wasm hosts |
| `glommio` | Thread-per-core io_uring-based — only when you need it; Linux-only |
| `monoio` | Thread-per-core io_uring — niche, similar trade-off to glommio |
| `embassy` | `no_std` async executor for microcontrollers — entirely separate world |

### 8.2 Structured concurrency primitives

```rust
use tokio::task::JoinSet;
use tokio_util::sync::CancellationToken;
use tokio_util::task::AbortOnDropHandle;

// Pattern: bounded task fan-out with cancellation
async fn fetch_all(urls: Vec<String>, cancel: CancellationToken) -> Vec<Result<Body, Err>> {
    let mut set = JoinSet::new();
    for url in urls {
        let token = cancel.clone();
        set.spawn(async move {
            tokio::select! {
                _ = token.cancelled() => Err(Err::Cancelled),
                res = fetch(&url) => res,
            }
        });
    }
    let mut out = Vec::new();
    while let Some(res) = set.join_next().await {
        out.push(res.unwrap_or_else(|join_err| Err(Err::Join(join_err))));
    }
    out
}
```

Key crates:

| Crate | What |
|-------|------|
| `tokio::task::JoinSet` | Dynamic task group with await-all and abort-all |
| `tokio_util::sync::CancellationToken` | Tree-shaped cooperative cancellation. Clone the parent — all clones cancel together |
| `tokio_util::task::AbortOnDropHandle` | Wrap `JoinHandle`; abort when dropped (vs default: detach) |
| `tokio_util::task::TaskTracker` | Track spawned tasks for graceful shutdown without owning them all |
| `tokio_graceful` / `tokio-graceful-shutdown` | High-level shutdown coordinators with signal handling |

### 8.3 Graceful shutdown pattern

```rust
use tokio::signal;
use tokio_util::{sync::CancellationToken, task::TaskTracker};
use std::time::Duration;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cancel = CancellationToken::new();
    let tasks  = TaskTracker::new();

    // 1. Spawn the HTTP server, passing cancel
    tasks.spawn(http_server(cancel.clone()));

    // 2. Spawn background workers
    tasks.spawn(metrics_pump(cancel.clone()));

    // 3. Close the tracker — no new tasks accepted
    tasks.close();

    // 4. Wait for SIGINT or SIGTERM
    let _ = signal::ctrl_c().await;
    tracing::info!("shutdown signal received");

    // 5. Tell everyone to stop
    cancel.cancel();

    // 6. Wait, with a deadline
    match tokio::time::timeout(Duration::from_secs(30), tasks.wait()).await {
        Ok(()) => tracing::info!("clean shutdown"),
        Err(_) => tracing::error!("shutdown timed out — forcing exit"),
    }
    Ok(())
}
```

### 8.4 Backpressure with Tower

Tower (`tower`, `tower-http`) is the middleware layer used by `axum`, `tonic`, and `hyper-util`. Backpressure is built in:

| Layer | What it does |
|-------|--------------|
| `tower::buffer::Buffer` | Bounded queue in front of the service — `poll_ready` returns Pending when full |
| `tower::limit::ConcurrencyLimit` | Bound the number of in-flight requests |
| `tower::limit::RateLimit` | Token-bucket rate limit |
| `tower::load_shed::LoadShed` | Drop new requests when the inner service signals overload |
| `tower::timeout::Timeout` | Per-request timeout |
| `tower::retry::Retry` | Retry policy (with budget — prevents retry storms) |

```rust
use tower::ServiceBuilder;

let service = ServiceBuilder::new()
    .timeout(Duration::from_secs(10))
    .concurrency_limit(1024)
    .rate_limit(100, Duration::from_secs(1))
    .load_shed()
    .service(my_handler);
```

### 8.5 Retry — `tokio-retry` vs `backoff`/`backon`

| Crate | API style | Use |
|-------|-----------|-----|
| `tokio-retry` | Stream/iterator of delays + future factory | Simple, per-call retries |
| `backoff` (now also as `backon`) | Builder + policy + jitter | Long-running, idempotent ops, complex policies |
| `tower::retry::Retry` | Service layer | Retries integrated into the middleware stack with budget |

### 8.6 Cancellation safety — the recurring footgun

A future is **cancellation-safe** if dropping it mid-poll leaves the world in a consistent state. `tokio::select!` requires *every* branch to be cancellation-safe.

Common safe primitives:

- `tokio::sync::mpsc::Receiver::recv` — safe
- `tokio::time::sleep` — safe
- `tokio::time::interval::tick` — safe
- `tokio::io::AsyncReadExt::read` — safe (no partial state)

Common **unsafe** primitives:

- `tokio::io::AsyncReadExt::read_exact` — drops partial reads
- `tokio::io::AsyncBufReadExt::read_line` — drops partial line
- Any future composed inside an `async {}` block where `.await` happens after committing state

**Rule**: when wrapping such futures in `select!`, wrap them in `tokio::spawn` first (or in a state machine you own), or use the `tokio::io::AsyncReadExt::read` (single-shot, returns whatever bytes are available).

### 8.7 `async fn` in traits — the static-vs-dynamic split

Since 1.75 (stable):

```rust
// Static dispatch — no async-trait crate needed
pub trait Repo: Send + Sync {
    async fn find(&self, id: Uuid) -> Result<Option<User>, RepoError>;
}
```

When you need a trait object:

```rust
// `dyn Repo` doesn't work directly with async fn — use async-trait
#[async_trait::async_trait]
pub trait Repo: Send + Sync {
    async fn find(&self, id: Uuid) -> Result<Option<User>, RepoError>;
}

fn make_handler(repo: Arc<dyn Repo>) { /* ... */ }
```

In 2026, the stable workaround for dyn-trait without `async-trait`'s heap allocation per call is **return-position `impl Trait` in traits (RPITIT)**:

```rust
pub trait Repo {
    fn find(&self, id: Uuid) -> impl Future<Output = Result<Option<User>, RepoError>> + Send;
}
// Not object-safe out of the box — but no per-call Box::new for static dispatch
```

Or use the `trait_variant::make` macro for both flavors from one definition.

---

## 9. Production crate matrix — 2026 baseline

This is the extended matrix that replaces and supersedes the 9-row table in the baseline.

### 9.1 HTTP server

| Crate | When |
|-------|------|
| **`axum` 0.8** | **Default.** Tokio-native, Tower-based middleware, type-safe extractors, no macro magic, growing fastest in 2026 |
| `actix-web` 4.x | Highest raw benchmark numbers on synthetic tests; actor model (less common in Rust now); largest community surface |
| `poem` | Pleasant API similar to axum, OpenAPI generation built-in |
| `rocket` 0.5 | Macro-heavy, opinionated, great DX — but slower adoption than axum |
| `salvo` | Newer; not yet a default choice |

### 9.2 HTTP client

| Crate | When |
|-------|------|
| **`reqwest`** | **Default.** Async + blocking, JSON, cookies, redirects, multipart — batteries included. Rustls by default |
| `ureq` | **Blocking only, no async.** Tiny dep tree — good for CLIs that don't pull in tokio |
| `hyper` (raw) | Low-level — when you need fine control over the HTTP state machine, custom transports |
| `isahc` | libcurl-backed; legacy |

### 9.3 gRPC

| Crate | When |
|-------|------|
| **`tonic`** | **Default.** Tokio-native, HTTP/2, code-gen from `.proto`. Now under the CNCF gRPC umbrella |
| `volo` | CloudWeGo's high-perf alternative; mostly relevant in Chinese-tech ecosystems |

### 9.4 Database — SQL

| Crate | Style | When |
|-------|-------|------|
| **`sqlx`** 0.8 | Raw SQL + compile-time verification (live DB or `.sqlx/` offline cache) | **Default for SQL-fluent teams.** Async-native, type-safe |
| **`sea-orm`** 2.0 (Jan 2026) | ActiveRecord-style ORM on top of SQLx | Teams migrating from Rails/Django; relational mapping with derive macros |
| `diesel` 2.3 (Jan 2026) | DSL + compile-time query checks | Sync-first; `diesel-async` adds async. Fastest compile times. Best ergonomics for complex joins |
| `surrealdb-rs` | Native SurrealDB driver | Only when SurrealDB is your DB |
| `rusqlite` | Direct SQLite bindings | Embedded SQLite — `r2d2-sqlite` for pooling, `tokio-rusqlite` for async wrapping |

### 9.5 Database — non-SQL / specialized

| Crate | DB |
|-------|----|
| `redis` (with `tokio-comp` feature) | Redis |
| `mongodb` (official) | MongoDB |
| `aws-sdk-dynamodb` | DynamoDB |
| `elasticsearch` / `opensearch` | ES / OpenSearch |
| `surrealkv` | Embedded KV store from SurrealDB authors |

### 9.6 Connection pooling

| Crate | When |
|-------|------|
| **`bb8`** | Async-only — depends on tokio. Same configuration shape as r2d2. **Default for tokio-only stacks** |
| **`deadpool`** | Async, simpler internal design — fewer features but rock solid; widely adopted |
| `r2d2` | Sync-only — use only for diesel sync code paths |

> Note: `sqlx` includes its own pool — you usually don't reach for bb8/deadpool unless you're driving a raw driver (`tokio-postgres`, `mongodb`).

### 9.7 Caching

| Crate | When |
|-------|------|
| **`moka`** | Thread-safe, async-aware in-process cache with TTL + size eviction. **Default** |
| `cached` | Function-memoization macro — handy for sync code; less powerful than moka |
| `quick_cache` | Smaller dep, simpler eviction; use when moka is overkill |

### 9.8 Serialization

| Crate | Format | When |
|-------|--------|------|
| **`serde`** + **`serde_json`** | JSON | Default for everything |
| `simd-json` | JSON | Drop-in faster JSON — uses SIMD. Useful when JSON parsing is on the hot path |
| `sonic-rs` (CloudWeGo) | JSON | Newer SIMD-JSON variant — sometimes faster than simd-json |
| `rmp-serde` | MessagePack | Binary serde for IPC/storage |
| **`bincode`** 2.0 | Custom binary | Now decoupled from serde — `bincode::Encode/Decode` derive macros (more compact, faster than serde-bincode) |
| `rkyv` | Zero-copy binary | When deserialization cost dominates; reads are pointer arithmetic |
| `prost` | Protobuf | Default for protobuf — used by tonic |
| `flatbuffers` | FlatBuffers | When you need cross-language zero-copy |
| `ciborium` | CBOR | When you need RFC-7049 CBOR |
| `serde_yaml` | YAML | (Note: unmaintained — use `serde_yml` fork as of 2024) |
| `toml` / `toml_edit` | TOML | Config files |

### 9.9 Time & dates

| Crate | When |
|-------|------|
| **`jiff`** | **Default for new code.** DST-aware arithmetic, IANA TZ identifier serialization, conflict detection on TZ rule changes |
| `time` | `no_std`-friendly, fast — for embedded or perf-sensitive paths. Limited TZ support |
| `chrono` | Legacy. Vast ecosystem integration (sqlx/diesel/serde) but TZ handling has subtle pitfalls. Maintain existing code; migrate to jiff for new code |

### 9.10 IDs

| Crate | Variant |
|-------|---------|
| **`uuid`** v1 (feature `v7`) | UUIDv7 — time-ordered, sortable. **Default ID format 2026** |
| `ulid` | ULID — 26 chars, sortable, URL-safe |
| `nanoid` | Short random IDs — URL-safe, no time ordering |
| `cuid2` | Collision-resistant, k-sortable — newer alternative |

### 9.11 Logging / tracing

| Crate | When |
|-------|------|
| **`tracing`** + **`tracing-subscriber`** | **Default.** Structured spans + events, supersedes `log` for new code |
| `tracing-opentelemetry` | Bridge tracing → OTLP exporter |
| `opentelemetry-otlp` | OTLP gRPC/HTTP exporter |
| `tracing-appender` | Non-blocking file appender, rotation |
| `tracing-flame` | Flamegraph generation from tracing spans |
| `log` | Only as the underlying API for libraries that don't depend on tracing — `tracing-log` bridges into tracing-subscriber |

### 9.12 Configuration

| Crate | When |
|-------|------|
| **`figment`** | Layered config (file → env → CLI) with serde — composable Provider model |
| `config` | Older standard — multi-source, hierarchical, less composable than figment |
| `serde_env` | Just env vars → struct |
| `clap` `--env` integration | When CLI flags should fall through to env vars natively |

Combine with `clap` for CLI args, and a final struct that `validator`/`garde`-validates at startup.

### 9.13 CLI

| Crate | When |
|-------|------|
| **`clap`** v4 derive | **Default.** Mature, derive-API, autocompletion via `clap_complete` |
| `bpaf` | Combinatoric API, smaller binary, beautiful help — niche but loved |
| `argh` | Tiny — when binary size matters more than features |
| `pico-args` | Hand-rolled parsing helpers — last resort for ultra-small CLIs |
| `dialoguer` | Interactive prompts (select, multi-select, confirm) |
| `indicatif` | Progress bars, spinners |
| `console` | Colored terminal output, ANSI handling |

### 9.14 TUI

| Crate | When |
|-------|------|
| **`ratatui`** | **Default.** Fork of `tui-rs` after its hiatus; active and rich ecosystem |
| `crossterm` | Cross-platform terminal backend — used by ratatui by default |
| `cursive` | Higher-level widget framework — different mental model from immediate-mode ratatui |

### 9.15 WebSockets

| Crate | When |
|-------|------|
| **`tokio-tungstenite`** | **Default.** Standard WS client/server for tokio. Post-0.26.2 is on par with fastwebsockets |
| `fastwebsockets` | Cloudflare-built, performance-focused. Pick for high-throughput WS gateways |
| `axum::extract::ws` | If you're already on axum and want WS integrated |

### 9.16 Validation

| Crate | When |
|-------|------|
| **`garde`** | **Default 2026.** Async validation, custom validators, no panic-on-invalid; modern API |
| `validator` | Older standard — works but `garde` is the cleaner design |

### 9.17 State machines

| Crate | When |
|-------|------|
| **`statig`** | Hierarchical state machines, async-aware; good for event-driven systems |
| `sm` | Declarative DSL, very explicit, fewer features |
| Typestate (no crate) | When the machine fits in 2-5 states — use phantom-typed structs; compile-time enforcement |

### 9.18 WASM toolchain

| Crate | When |
|-------|------|
| **`wasm-bindgen`** | Browser-targeted Wasm — JS interop |
| **`wit-bindgen`** | Component Model — language-neutral interfaces. Bytecode Alliance |
| `wasmtime` | Host: embed Wasm into a Rust application; supports the Component Model + WIT via `wasmtime::component::bindgen!` |
| `wasmer` | Alternative host runtime |
| `wasm-pack` | Build orchestrator for browser-target Wasm |
| `worker` | Cloudflare Workers Rust SDK |

### 9.19 Embedded

| Crate | When |
|-------|------|
| **`embassy`** | `no_std` async executor + HAL for MCUs — fastest-growing embedded Rust framework |
| `embedded-hal` | The trait standard for sync embedded HALs |
| `embedded-hal-async` | Async sibling |
| `defmt` | Compact log formatting for MCUs — defers formatting to host |
| `probe-rs` | Flashing, debugging, RTT logging via SWD/JTAG |

### 9.20 Game / graphics

| Crate | When |
|-------|------|
| **`bevy`** | Default game engine; ECS-based; growing ecosystem of plugins |
| `wgpu` | Cross-platform GPU API (WebGPU spec) — used by bevy and others |
| `winit` | Windowing |
| `egui` | Immediate-mode GUI; pairs with wgpu/eframe |
| `iced` | Retained GUI with Elm-like architecture |

### 9.21 ML / data

| Crate | When |
|-------|------|
| **`burn`** | Modern Rust-native ML framework with multiple backends (CUDA, Vulkan, WGPU, ndarray) |
| **`candle`** | Hugging Face's minimal ML framework — focus on inference, deployable in production |
| `tch` | Bindings to libtorch — production PyTorch interop |
| `ort` | ONNX Runtime bindings |
| `polars` | DataFrame, ~pandas-equivalent — production data work |
| `arrow-rs` / `parquet` | Apache Arrow / Parquet |

---

## 10. Domain architecture patterns

### 10.1 Hexagonal / Clean / Ports-and-Adapters in Rust

Rust's traits are the natural fit for "ports." The pattern that emerged as canonical in 2026 (post async-fn-in-traits stabilization):

```
domain (pure, no_std-able)
  ↓
  ├── entities & value objects (no I/O)
  ├── port traits: pub trait UserRepo { async fn find(&self, id) -> Result<Option<User>, _> }
  └── domain errors (thiserror)

application (use cases)
  ↓
  ├── service structs: pub struct CreateUser<R: UserRepo, M: Mailer> { repo: R, mailer: M }
  └── application errors (wrap domain + use-case errors)

infra-* (adapters)
  ↓
  └── concrete impls: impl UserRepo for PgUserRepo { ... }

http / cli / worker (drivers)
  ↓
  └── wire domain ports to specific concrete adapters at startup
```

The compile-time payoff: `cargo check -p domain` fails immediately if a `sqlx::` type leaks into the domain crate. Architecture is enforced by the dependency graph, not by code review.

### 10.2 Trait-based DI

```rust
// Application service is generic over its dependencies — no service locator, no Arc<dyn>
pub struct CreateUser<R, M>
where R: UserRepo, M: Mailer
{
    repo: R,
    mailer: M,
}

impl<R: UserRepo, M: Mailer> CreateUser<R, M> {
    pub async fn execute(&self, cmd: CreateUserCmd) -> Result<UserId, CreateUserError> {
        let user = User::try_new(cmd)?;                    // domain validation
        self.repo.insert(&user).await?;                    // port
        self.mailer.send_welcome(&user.email).await?;      // port
        Ok(user.id)
    }
}

// In tests:
let svc = CreateUser { repo: InMemoryUserRepo::default(), mailer: NoopMailer };

// In production:
let svc = CreateUser { repo: PgUserRepo::new(pool), mailer: SendgridMailer::new(api_key) };
```

When you need a trait object (uniform collection of handlers, plugin registry), use `Arc<dyn Trait + Send + Sync>` — pay the dispatch cost only at the seam.

### 10.3 Repository pattern

Don't expose ORM-specific types from the domain. The repo trait should be free of `sqlx::PgConnection`, `diesel::PgConnection`, etc.

```rust
// domain/repo.rs
pub trait UserRepo: Send + Sync {
    async fn insert(&self, user: &User) -> Result<(), RepoError>;
    async fn find(&self, id: UserId) -> Result<Option<User>, RepoError>;
    async fn find_by_email(&self, email: &Email) -> Result<Option<User>, RepoError>;
}

// infra-pg/user_repo.rs
pub struct PgUserRepo { pool: PgPool }

impl UserRepo for PgUserRepo {
    async fn insert(&self, user: &User) -> Result<(), RepoError> {
        sqlx::query!("INSERT INTO users (id, email, ...) VALUES ($1, $2, ...)",
            user.id.0, user.email.as_str())
            .execute(&self.pool).await
            .map_err(RepoError::from)?;
        Ok(())
    }
    // ...
}
```

### 10.4 CQS — Command/Query Separation

Use the type system to enforce CQS at the API boundary:

```rust
// Commands return Result<(), CommandError> — change state, no return data beyond identifiers
pub trait Command { type Output; type Error; async fn execute(self, ctx: &Ctx) -> Result<Self::Output, Self::Error>; }

// Queries return data, must not mutate (Rust can't enforce "no mutation" but type discipline helps)
pub trait Query { type Output; type Error; async fn execute(&self, ctx: &Ctx) -> Result<Self::Output, Self::Error>; }
```

CQS gives you natural seams for read-replicas, read-side caching, and eventual consistency. CQRS (the heavier pattern with separate read/write models) is overkill until proven necessary.

### 10.5 Event sourcing

The 2026 production stack for event sourcing in Rust:

| Layer | Crates |
|-------|--------|
| Event store | `eventstore-rs` (EventStoreDB), or PostgreSQL with `sqlx` + custom append-only tables |
| Serialization | `serde_json` (debuggable), `prost` (compact + schema), `rkyv` (fast read) |
| Projections | Hand-rolled — apply event handlers to read models |
| Aggregates | Plain structs + `pub fn apply(&mut self, event: &Event)` |

There is no single canonical Rust ES framework; `cqrs-es` exists but is light. Most teams hand-roll using domain primitives.

### 10.6 Saga / process manager

Long-running multi-step workflows with compensation:

| Crate | When |
|-------|------|
| `temporal-sdk` | Temporal.io workflows in Rust — production-tested at scale |
| `mq_mailer`-style hand-rolled with `tokio` + persisted state | Light workflows where Temporal's footprint is too heavy |
| `effectum`, `apalis` | Job queue libs — good for fire-and-forget; not full sagas |

The Rust ecosystem is *thinner* here than Java/Go — Temporal is the production default if you need true saga semantics.

### 10.7 Axum extractors as adapters

Axum's extractor system is the perfect "adapter layer" in hexagonal architecture:

```rust
async fn create_user(
    State(svc): State<Arc<CreateUserSvc>>,    // application service
    AuthUser(actor): AuthUser,                 // custom extractor → auth port
    Json(body): Json<CreateUserDto>,           // request DTO
) -> Result<Json<UserResponseDto>, ApiError> {
    let cmd = body.into_command(actor)?;       // DTO → domain command
    let user_id = svc.execute(cmd).await?;     // application service runs
    Ok(Json(UserResponseDto { id: user_id.0 }))
}
```

Where:

- The extractor (`Json`, `Path`, `Query`, `State`, custom `AuthUser`) is the **inbound adapter**.
- The DTO and `into_command` is the **boundary mapper**.
- `svc.execute()` is application code.
- `ApiError`'s `IntoResponse` impl maps domain errors to HTTP status codes (the outbound adapter for errors).

This produces handlers that read like documentation: "given this request, this auth context, this body — run this command, return this response."

---

## 11. Documentation & doc-tests

### 11.1 `///` vs `//!`

| Style | Where | What |
|-------|-------|------|
| `///` | Above an item | Doc comment for that item |
| `//!` | Inside a module/crate | Doc comment for the containing scope (use at the top of `lib.rs` and `mod.rs`) |
| `#[doc = "..."]` | Anywhere | Programmatic equivalent — useful for macros that emit docs |

### 11.2 Doctests as executable specification

```rust
/// Parses a config from a TOML string.
///
/// # Errors
/// Returns [`ConfigError::Syntax`] if the input is not valid TOML.
/// Returns [`ConfigError::Schema`] if required fields are missing.
///
/// # Examples
///
/// ```
/// use my_crate::Config;
///
/// let cfg: Config = my_crate::parse("name = 'demo'")?;
/// assert_eq!(cfg.name, "demo");
/// # Ok::<_, my_crate::ConfigError>(())
/// ```
pub fn parse(s: &str) -> Result<Config, ConfigError> { /* ... */ }
```

Rules:

- Use `?` not `unwrap()` in examples (C-QUESTION-MARK).
- Hide setup lines with `# ` prefix — the line is compiled but not displayed.
- Run `cargo test --doc` in CI — doctests are tests.
- Add `#![doc(test(attr(deny(warnings))))]` at crate root to make doctest warnings fail.

### 11.3 `#[doc(hidden)]`

```rust
#[doc(hidden)]
pub mod __private {
    // Macros need to refer to these by absolute path — they're "pub" but not API.
    pub use std::marker::PhantomData;
}
```

Use for items that must be `pub` for macro expansion but aren't part of the user-facing API.

### 11.4 Intra-doc links

```rust
/// Sends an email via [`Mailer::send`].
///
/// See also: [`crate::error::EmailError`], [`std::io::Error`].
///
/// [`Mailer::send`]: crate::mailer::Mailer::send
pub fn send_email() { /* ... */ }
```

In 2026:

- `[`Type`]` (single backticks-with-trailing-link) auto-resolves to items in scope.
- `[`crate::module::Type`]` for absolute paths.
- `[`Self::method`]` and `[`Self`]` work inside impls.
- `cargo doc -- -D rustdoc::broken_intra_doc_links` to fail CI on broken links.

### 11.5 Feature-gated docs — `cfg(docsrs)`

```rust
#![cfg_attr(docsrs, feature(doc_cfg))]

#[cfg_attr(docsrs, doc(cfg(feature = "postgres")))]
#[cfg(feature = "postgres")]
pub mod postgres { /* ... */ }
```

`docs.rs` builds with `--cfg docsrs` enabled and the nightly compiler, so `doc(cfg(...))` annotations render a "feature: postgres" tag in the published docs. Configure in `Cargo.toml`:

```toml
[package.metadata.docs.rs]
all-features = true
rustdoc-args = ["--cfg", "docsrs"]
```

### 11.6 `cargo doc --no-deps`

Generates docs for your crate only — the default behavior includes the entire dependency tree, which is slow and pollutes output. Always use `--no-deps` for local dev rebuilds:

```sh
cargo doc --no-deps --open
```

### 11.7 Crate-level doc structure (`//!` at the top of `lib.rs`)

A complete `lib.rs` header:

```rust
//! # my_crate
//!
//! Short one-liner of what the crate does.
//!
//! ## Quick start
//!
//! ```
//! use my_crate::Foo;
//! let foo = Foo::new("demo");
//! # let _ = foo;
//! ```
//!
//! ## Feature flags
//!
//! - `default`: includes `json`
//! - `json`: enables JSON serialization via serde
//! - `postgres`: enables the PostgreSQL adapter
//!
//! ## MSRV
//!
//! Rust 1.85+ (Edition 2024).
//!
//! ## Stability
//!
//! Pre-1.0. APIs may change before 1.0.

#![cfg_attr(docsrs, feature(doc_cfg))]
#![warn(missing_docs)]
#![warn(missing_debug_impls)]

// ...
```

---

## 12. Release & distribution

### 12.1 Semver discipline

Rust treats semver strictly — `cargo` resolves `^1.2` to `>=1.2.0, <2.0.0`. Some 2026 nuances:

| Change | Bump |
|--------|------|
| Added new function, type, variant, impl, method | minor |
| Added new struct field (without `#[non_exhaustive]`) | **major** — pattern matches now miss the field |
| Added enum variant (without `#[non_exhaustive]`) | **major** — pattern matches now exhaustive-fail |
| Increased MSRV | minor (by convention; some projects call it major) |
| Added new public trait bound on existing fn | **major** — calls may stop compiling |
| Switched a dep from `0.x` to `0.y` and re-exported its type | **major** |
| Removed `#[doc(hidden)]` from something | minor (now part of API contract) |
| Added `#[doc(hidden)]` to public item | **major** if any user depended on it (none should have) |

Use **`cargo-semver-checks`** in CI to catch most of these automatically.

### 12.2 `cargo-release` workflow

```sh
cargo install cargo-release
cargo release patch --execute   # 0.1.3 → 0.1.4 — bump, commit, tag, publish, push
cargo release minor --execute   # 0.1.3 → 0.2.0
cargo release major --execute   # 0.1.3 → 1.0.0
```

Configure in `release.toml`:

```toml
sign-commit         = true
sign-tag            = true
push-remote         = "origin"
pre-release-replacements = [
  { file="CHANGELOG.md", search="Unreleased", replace="{{version}}" },
  { file="CHANGELOG.md", search="\\[Unreleased\\]: https://github.com/.+/compare/v.+\\.\\.\\.HEAD",
    replace="[Unreleased]: https://github.com/org/repo/compare/v{{version}}...HEAD" },
]
```

### 12.3 Changelog generation — `git-cliff`

`git-cliff` reads conventional-commit messages and renders a CHANGELOG.md:

```sh
cargo install git-cliff
git cliff -o CHANGELOG.md            # full history
git cliff --unreleased               # just since last tag
```

`cliff.toml` defines the template — group `feat:` → "Features", `fix:` → "Bug Fixes", etc.

### 12.4 `cargo-dist` — binary distribution

`cargo-dist` builds release archives (`.tar.gz`, `.zip`, `.msi`, `.dmg`), generates `install.sh` and `install.ps1`, signs artifacts, and uploads to a GitHub Release. Configured entirely in `Cargo.toml`:

```toml
[workspace.metadata.dist]
cargo-dist-version = "0.20.0"
ci                 = "github"
installers         = ["shell", "powershell", "homebrew"]
targets            = [
  "aarch64-apple-darwin",
  "x86_64-apple-darwin",
  "x86_64-unknown-linux-gnu",
  "x86_64-unknown-linux-musl",
  "x86_64-pc-windows-msvc",
]
```

Replaces ~500 lines of hand-rolled GitHub Actions YAML for a typical bin crate.

### 12.5 Cross-compilation

| Tool | Mechanism | Targets |
|------|-----------|---------|
| **`cargo-zigbuild`** | Uses `zig cc` as the C linker — handles glibc versioning trivially; supports `universal2-apple-darwin` (Apple Silicon + Intel in one binary) | Linux, macOS targets; Windows is partial |
| **`cross`** | Docker images per target — slower but works for everything | Linux, Windows GNU, BSDs, embedded |
| Native cross-compile | `rustup target add` + manually-installed C toolchain | Anything if you set up the linker — most work |

`cargo-dist` uses zigbuild + cross under the hood for the targets that need it.

### 12.6 Binary size optimization checklist

In priority order — apply top-down until size is acceptable:

1. **`strip = "symbols"`** in `[profile.release]` — 30-60% reduction, free
2. **`panic = "abort"`** — removes unwinding tables, 10-20% reduction
3. **`lto = "fat"`** — dead-code elimination across crates, 10-25%
4. **`codegen-units = 1`** — better optimization, ~5% size + speed
5. **`opt-level = "z"`** — optimize for size (vs `3` which optimizes speed). 10-30% size reduction; sometimes faster on memory-bound code (better cache locality)
6. **Audit features** — `--no-default-features` and explicit feature opt-in. The biggest wins often come here.
7. **Replace heavy deps** — `regex` (~1MB) → `regex-lite` (~150KB) if you don't need Unicode; `reqwest` → `ureq` for blocking-only CLIs
8. **Run `cargo bloat --release`** — find the actual hogs
9. **Build with `-Zbuild-std=std,panic_abort` and `-Zbuild-std-features=panic_immediate_abort`** (nightly) for ultimate minimization
10. **`upx` post-link compression** — controversial (slow startup, antivirus false-positives) — measure before adopting

```toml
# A balanced "production" profile
[profile.release]
strip         = "symbols"
panic         = "abort"
lto           = "fat"
codegen-units = 1
opt-level     = 3                       # use "z" if size is more critical than speed
overflow-checks = false                 # default in release; mention explicitly
```

### 12.7 Reproducible builds

For a build to be byte-identical across machines:

```toml
[profile.release]
# Avoid embedding build paths
strip = "symbols"

[profile.release.package."*"]
# Force a deterministic codegen unit count
codegen-units = 1
```

Plus `RUSTFLAGS="--remap-path-prefix=$HOME=/build"` to strip user-specific paths. Disable incremental compilation in CI release builds (`CARGO_INCREMENTAL=0`).

### 12.8 Publishing checklist (library crate)

Before `cargo publish`:

- [ ] `cargo deny check` passes
- [ ] `cargo semver-checks` passes (against the last published version)
- [ ] `cargo public-api` diff reviewed
- [ ] `cargo doc --no-deps` builds clean
- [ ] `cargo test --all-features` passes
- [ ] `cargo hack --feature-powerset --no-dev-deps check` passes
- [ ] `cargo msrv verify` against declared `rust-version`
- [ ] `CHANGELOG.md` updated
- [ ] `Cargo.toml` has `description`, `license`, `repository`, `homepage`, `documentation`, `keywords`, `categories`
- [ ] `README.md` includes install + minimal example
- [ ] Tag matches `Cargo.toml` version (`cargo release` does this for you)

---

## 13. What changed since 2023 — the migration cheatsheet

Quick scan for anyone returning to Rust after 2-3 years. **2026 default** ≠ **2023 default** in many places.

| Concern | 2023 default | 2026 default | Why |
|---------|--------------|--------------|-----|
| Edition | 2021 | **2024** | Edition 2024 default with Rust 1.85 (Feb 2025) |
| Date/time | `chrono` | **`jiff`** | DST correctness, IANA TZ ser/de, design from BurntSushi |
| TLS | `native-tls` mixed with `rustls` | **`rustls`** | Pure-Rust, modern ciphers, no OpenSSL build hassles |
| `async fn` in traits | `async-trait` everywhere | **Native** (stable 1.75) — `async-trait` only for `dyn Trait` |
| `lazy_static!` / `once_cell::Lazy` | both | **`std::sync::LazyLock`** (stable 1.80) | Stdlib coverage |
| Trait upcasting | manual `as_super()` | **Native** (stable 1.86) | Less boilerplate |
| Builder pattern | hand-rolled or `derive_builder` | **`bon`** | Compile-time required-field checking via typestate |
| HTTP server | `actix-web` / `warp` / `axum` mixed | **`axum`** | Tower middleware, no-macro, fastest-growing |
| ORM | `diesel` dominant | **`sqlx`** for SQL-fluent teams; `sea-orm` 2.0 for ActiveRecord; `diesel` 2.3 still fine | Async-native ergonomics |
| Test runner | `cargo test` | **`cargo nextest`** | 3x faster, isolation |
| Logging | `log` + `env_logger` | **`tracing`** + `tracing-subscriber` + `tracing-opentelemetry` | Structured spans, OTLP-native |
| JSON | `serde_json` only | `serde_json` + **`sonic-rs`/`simd-json`** on hot paths | SIMD JSON parsing matured |
| Bincode | bincode 1.x via serde | **`bincode` 2.0** native derive (no serde) | More compact, faster, optional serde |
| Cancellation | manual `Arc<AtomicBool>` | **`tokio_util::sync::CancellationToken`** | Tree-shaped propagation |
| Graceful shutdown | hand-rolled | **`tokio_util::task::TaskTracker`** + `tokio_graceful` | Standard idiom |
| Allocator | system default | **`mimalloc`** | ~4% perf gain default, stable cross-platform |
| Configuration | `config-rs` | **`figment`** | Composable providers, serde-first |
| Validation | `validator` | **`garde`** | Modern API, async-aware |
| Test snapshots | manual / `goldenfile` | **`insta`** | Interactive review, dynamic redaction |
| Bench | `criterion` only | `criterion` (CI) + **`divan`** (local iteration) | Divan is faster to iterate on |
| Coverage | `tarpaulin` | **`cargo-llvm-cov`** | LLVM source-based, more accurate, nextest integration |
| Mutation testing | (rare) | **`cargo-mutants`** weekly | Production-viable in 2026 |
| Cross-compile | `cross` | **`cargo-zigbuild`** for Linux/macOS; `cross` for the rest | zig as linker is magic |
| Release | hand-rolled GH Actions | **`cargo-dist`** | One-tool packaging across OSes |
| Publish auth | API token in env | **Trusted Publishing via OIDC** | No long-lived secrets |
| Async ORM trait methods | `#[async_trait]` | **native `async fn`** in traits | 1.75 stabilization |
| MSRV check | manual | **`cargo-msrv verify` in CI** | Toolchain matrix |
| API stability | hand-vetted | **`cargo-semver-checks` + `cargo-public-api`** | Automated semver review |
| WebSocket | `tokio-tungstenite` (slower) | **`tokio-tungstenite` ≥ 0.26.2** (now on par with fastwebsockets) | Recent perf work |

---

## Sources

- **Rust API Guidelines** — https://rust-lang.github.io/api-guidelines/checklist.html — the canonical C-* list reproduced in §1
- **Cargo Book** — https://doc.rust-lang.org/cargo/ — workspaces, features, profiles, semver
- **Rust Performance Book** (Nethercote) — https://nnethercote.github.io/perf-book/ — §6 references
- **Tokio docs** — https://tokio.rs — async patterns, shared state, shutdown
- **RustSec Advisory DB** — https://rustsec.org/ — vuln workflow
- **Embark `cargo-deny` docs** — https://embarkstudios.github.io/cargo-deny/ — §4.2 deny.toml
- **Jiff design** — https://github.com/BurntSushi/jiff/blob/master/DESIGN.md — why jiff over chrono
- **Rust 1.85 / Edition 2024 announcement** — https://blog.rust-lang.org/2025/02/20/Rust-1.85.0.html
- **Cargo 1.93 dev cycle** (2026-01) — https://blog.rust-lang.org/inside-rust/2026/01/07/this-development-cycle-in-cargo-1.93/ — workspace.lints evolution
- **Cargo CVE-2026-5223** — https://blog.rust-lang.org/2026/05/25/cve-2026-5223/ — fresh example of the security workflow
- **Predr.ag — sealed traits** — https://predr.ag/blog/definitive-guide-to-sealed-traits-in-rust/ — §1.12 recipe
- **Luca Palmieri — error handling** — https://www.lpalmieri.com/posts/error-handling-rust/ — §2 deep dive
- **GreptimeDB error handling case study** — https://greptime.com/blogs/2024-05-07-error-rust — large-codebase pattern
- **Master Hexagonal Architecture in Rust** — https://www.howtocodeit.com/guides/master-hexagonal-architecture-in-rust — §10 reference
- **min-sized-rust** — https://github.com/johnthagen/min-sized-rust — §12.6 binary size
- **Rust SQLx vs Diesel vs SeaORM (Reintech, 2026)** — https://reintech.io/blog/diesel-vs-sqlx-vs-seaorm-rust-database-library-comparison-2026 — §9.4 versions
- **bon docs** — https://bon-rs.com/ — §1.7 builder recipe
- **JetBrains — Faster Rust Tests With cargo-nextest (2026-05)** — https://blog.jetbrains.com/rust/2026/05/01/faster-rust-tests-with-cargo-nextest/ — §5 nextest
- **Cargo SemVer Compatibility** — https://doc.rust-lang.org/cargo/reference/semver.html — §12.1
- **WireMock + Testcontainers** — https://wiremock.org/docs/solutions/testcontainers/ — §5 mocking
- **cargo-mutants on Thoughtworks Tech Radar** — https://www.thoughtworks.com/radar/tools/cargo-mutants — §5 mutation testing
- **OpenTelemetry Rust docs** — https://opentelemetry.io/docs/languages/rust/ — §9.11 observability
- **Tokio shared-state tutorial** — https://tokio.rs/tokio/tutorial/shared-state — §8 cancellation/backpressure
- **Tower middleware docs** — https://docs.rs/tower — §8.4
- **tokio-graceful** — https://github.com/plabayo/tokio-graceful — §8.3
