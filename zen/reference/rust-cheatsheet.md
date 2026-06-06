# Rust Refactoring Cheatsheet (Edition 2024 / 1.85+)

Purpose: Zen-flavored slice of the Rust knowledge base — code-smell-to-idiom transformations, renaming hygiene, magic-number cleanup, macro hygiene, and refactor anti-patterns. Behavior-preserving only.

Baseline: **Rust 1.85+, Edition 2024, resolver = "3"**.

Source of truth (do not duplicate here):
- Bad-pattern catalog → [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md)
- Target idioms / API Guidelines → [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md)
- Language surface (Edition 2024, AFIT, GATs, let-else, LazyLock, `use<…>`) → [`builder/reference/rust-language-spec.md`](../../builder/reference/rust-language-spec.md)

Companion: [`language-patterns.md`](./language-patterns.md) holds the cross-language Rust quick-pattern set. Read this file for refactor-specific transformations.

---

## Contents

- [Smell → Idiom Map](#smell--idiom-map)
- [Function Extraction Signals (Rust-specific)](#function-extraction-signals-rust-specific)
- [Renaming Hygiene (C-CASE / API Guidelines)](#renaming-hygiene-c-case--api-guidelines)
- [Magic Numbers and Strings](#magic-numbers-and-strings)
- [Macro Hygiene Refactors](#macro-hygiene-refactors)
- [Refactor Anti-Patterns to Avoid](#refactor-anti-patterns-to-avoid)
- [Refactor Checklist](#refactor-checklist)

---

## Smell → Idiom Map

| Smell | Idiom | Notes |
|-------|-------|-------|
| Nested `if let Some(x) = a { if let Some(y) = x.b() {...} }` | `?` on `Option` / `let-else` / `Option::and_then` | Edition 2024 makes `?` on `Option` flow naturally in `-> Option<_>` |
| `match` with one arm of interest, `_` fallthrough | `if let` / `let-else` | `let-else` (1.65+) avoids rightward drift on early-return paths |
| `match x { Some(v) => v, None => return default }` | `x.unwrap_or(default)` / `x.unwrap_or_else(\|\| ...)` | `unwrap_or_default()` when `T: Default` |
| Manual `Result` propagation via `match` | `?` operator + `anyhow::Context::context()` / `eyre` | Reserve `match` for branching on the error variant |
| `String` concat with `+` in a loop | `String::with_capacity(n)` + `push_str` / `write!` | See best-practices §6 (Performance) |
| Repeated `.clone()` to silence borrowck | Borrow refactor / `Cow<'_, T>` / move semantics | Anti-pattern §1; `clone()` hides a design problem |
| `&Vec<T>` / `&String` / `&PathBuf` in function signatures | `&[T]` / `&str` / `&Path` | API Guidelines C-COMMON-CONVERSIONS; accept the broader view type |
| Boolean parameter on a public API | Enum or typestate (`enum Mode { Strict, Lenient }`) | Boolean-blindness anti-pattern §13 |
| Primitive obsession on IDs (`String` user_id) | Newtype: `struct UserId(Uuid);` with `Display` / `From` | API Guidelines C-NEWTYPE |
| `Vec<bool>` / repeated tagged tuples | Enum + struct refactor (one tag, struct fields) | Tighten invariants — "make illegal states unrepresentable" |
| Hand-rolled builder with 6+ optional fields | `#[bon::builder]` (or `derive_builder`) | Best-practices §9 |
| `lazy_static!` / `once_cell::sync::Lazy` | `std::sync::LazyLock` (1.80+) | Std-native, no extra dep |
| Long `impl Trait` chain whose hidden captures bite users | Add `use<...>` bound for explicit capture (1.82+) | `fn foo<'a>() -> impl Trait + use<'a>` |
| `#[async_trait]` shim everywhere | Native AFIT (`async fn` in trait, 1.75+) | Keep `async-trait` only when `dyn Trait` is required |
| Excess `'a` lifetime annotations | Rely on lifetime elision | Compiler infers in 95% of cases; explicit only at ambiguity |
| `Box<dyn Error>` in library code | `thiserror`-derived typed enum | Best-practices §2 |
| Deep `if/else` ladders dispatching on enum | `match` exhaustively + extract per-variant helper | Compiler enforces exhaustiveness on enum changes |
| `.unwrap()` / `.expect()` in non-test paths | `?` + typed error | Anti-pattern §5 |
| `for i in 0..xs.len() { xs[i] ... }` | `for x in &xs` / `xs.iter().enumerate()` | Removes bounds checks; clearer intent |

### Selected before/after snippets

#### Nested `if let` → `?`

```rust
// Before
fn city_of(user: Option<&User>) -> Option<String> {
    if let Some(u) = user {
        if let Some(addr) = &u.address {
            if let Some(city) = &addr.city {
                return Some(city.clone());
            }
        }
    }
    None
}

// After
fn city_of(user: Option<&User>) -> Option<String> {
    Some(user?.address.as_ref()?.city.as_ref()?.clone())
}
```

#### `match` early-return → `let-else`

```rust
// Before
let user = match repo.find(id) {
    Some(u) => u,
    None => return Err(NotFound),
};

// After
let Some(user) = repo.find(id) else {
    return Err(NotFound);
};
```

#### `&Vec<T>` → `&[T]`

```rust
// Before
fn sum(xs: &Vec<i64>) -> i64 { xs.iter().sum() }

// After — also accepts arrays, slices, smallvec, etc.
fn sum(xs: &[i64]) -> i64 { xs.iter().sum() }
```

#### Bool parameter → enum

```rust
// Before
fn render(text: &str, html_escape: bool) { /* ... */ }
render(msg, true);  // What does `true` mean at the call site?

// After
enum Escape { Html, None }
fn render(text: &str, escape: Escape) { /* ... */ }
render(msg, Escape::Html);
```

#### Primitive ID → newtype

```rust
// Before
fn ban(user_id: String, by_admin: String) { /* easy to swap */ }

// After
#[derive(Clone, Debug, Eq, PartialEq, Hash)]
pub struct UserId(uuid::Uuid);

#[derive(Clone, Debug, Eq, PartialEq, Hash)]
pub struct AdminId(uuid::Uuid);

fn ban(user_id: UserId, by_admin: AdminId) { /* compiler-enforced */ }
```

#### `lazy_static!` → `LazyLock`

```rust
// Before
use once_cell::sync::Lazy;
static CONFIG: Lazy<Config> = Lazy::new(load_config);

// After (1.80+)
use std::sync::LazyLock;
static CONFIG: LazyLock<Config> = LazyLock::new(load_config);
```

#### RPIT capture leak → `use<…>`

```rust
// Before — '_ lifetime captured implicitly under Edition 2024 RPIT capture rules
fn names<'a>(users: &'a [User]) -> impl Iterator<Item = &str> { /* ... */ }

// After — explicit, future-proof
fn names<'a>(users: &'a [User]) -> impl Iterator<Item = &str> + use<'a> { /* ... */ }
```

#### `#[async_trait]` shim → AFIT

```rust
// Before — extra heap alloc per call
#[async_trait]
trait Repo { async fn find(&self, id: Uuid) -> Option<User>; }

// After (1.75+) — native, zero-cost
trait Repo {
    fn find(&self, id: Uuid) -> impl Future<Output = Option<User>> + Send;
}
// Keep #[async_trait] only when you actually need `dyn Repo`.
```

---

## Function Extraction Signals (Rust-specific)

Extract a helper when you see:

1. **Lifetime juggling > 2 parameters with explicit `'a`** — extract a helper that owns its inputs, or accepts `Cow<'_, T>`. The new helper's signature usually elides automatically.
2. **Repeated `?`-chains all wrapping the same `.context("loading X")`** — extract a typed helper that returns a domain-specific error; the call site loses the noise.
3. **`match` arms with shared post-processing** — extract the post-processing as a free function or closure; arms reduce to value computation.
4. **Long iterator chain with named intermediates** — break at the named binding; each becomes a self-documenting helper (`fn active_orders(&self) -> impl Iterator<Item = &Order>`).
5. **`unsafe` block doing 3+ unrelated things** — extract each into its own `unsafe fn` (or safe wrapper around a single `unsafe`) with a documented `# Safety` contract. See anti-patterns §9.
6. **Closures capturing 4+ variables** — promote to a named struct + `impl Fn` or a free function with explicit parameters.

Counter-signals (do NOT extract):
- A 3-line block used in one place; inlining is clearer.
- A helper that requires more lifetime annotations than the inlined version.

---

## Renaming Hygiene (C-CASE / API Guidelines)

Follow the Rust API Guidelines C-CASE conventions exactly:

| Item Kind | Convention | Example |
|-----------|-----------|---------|
| Crate, module, function, method, variable | `snake_case` | `parse_header`, `user_repo` |
| Type, trait, enum variant | `UpperCamelCase` | `UserRepo`, `OrderState::Pending` |
| Constant, static | `SCREAMING_SNAKE_CASE` | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Type parameter | Single uppercase letter or `UpperCamelCase` | `T`, `Key`, `Error` |
| Lifetime | Short lowercase | `'a`, `'src`, `'de` (serde convention) |
| Feature flag | `kebab-case` | `feature = "tokio-runtime"` |

### Trait names

- **Capability traits = noun-er or noun-or**: `Reader`, `Writer`, `Iterator`, `Visitor`.
- **Conversion traits = `From` / `Into` / `TryFrom` / `TryInto`**. Do NOT invent ad-hoc converter traits.
- **Predicate-like traits = verb**: `Display`, `Debug`, `Hash`, `Clone`.
- **Avoid `IFoo` / `FooImpl` Java-isms** — anti-pattern §13.

### Error type names

- End with `Error`: `ParseError`, `ConfigError`, `RepoError`.
- Library errors: enum with `#[derive(thiserror::Error)]`.
- Application/CLI errors: `anyhow::Error` or `eyre::Report` (no need to name).
- Variants do NOT end with `Error`: `ParseError::InvalidHeader`, not `ParseError::InvalidHeaderError`.

### Constructor and conversion naming

- `new` — infallible, simple case. `with_*` — variant constructors. `try_new` / `try_from` — fallible.
- `into_*` — consuming conversion. `as_*` — borrowed conversion (cheap). `to_*` — borrowed conversion (allocates).

---

## Magic Numbers and Strings

Surface signals:

- `Duration::from_secs(30)` literal scattered across files → extract `const REQUEST_TIMEOUT: Duration = Duration::from_secs(30);`.
- `if attempts < 3` → `const MAX_ATTEMPTS: u32 = 3;`.
- Repeated `&str` literal in `enum` discriminators or message bodies → `const SIGNAL_NAME: &str = "...";` or move to a `mod constants`.

Rules:

- Prefer `const` over `let` for compile-time values. `const` is inlined at every use; `let` allocates a stack slot.
- For runtime-constructed values (e.g., `HashMap` config), prefer `LazyLock` over a runtime call per use.
- Group related constants in a `mod constants` or alongside the type they belong to:

```rust
impl HttpClient {
    const DEFAULT_TIMEOUT: Duration = Duration::from_secs(30);
    const MAX_RETRIES: u32 = 3;
}
```

- For `Duration`, always use the unit-bearing constructor (`from_secs`, `from_millis`) — never `Duration::new(30, 0)`.
- For paths, prefer `Path::new("foo")` constants via `LazyLock<&'static Path>` if reused.

Anti-signal: a constant used in exactly one place may belong as a `let` binding next to the use site instead.

---

## Macro Hygiene Refactors

Common refactors for `macro_rules!`:

### Capture leaks → use `$crate::`

```rust
// Before — breaks when caller doesn't have `Result` in scope or shadows it
macro_rules! bail {
    ($msg:expr) => { return Err(Error::new($msg)); };
}

// After — hygienic; works regardless of caller's imports
macro_rules! bail {
    ($msg:expr) => { return Err($crate::Error::new($msg)); };
}
```

### Repetition with separators

```rust
// Before — repeats glue manually
macro_rules! sum {
    ($a:expr) => { $a };
    ($a:expr, $b:expr) => { $a + $b };
    ($a:expr, $b:expr, $c:expr) => { $a + $b + $c };
}

// After — one rule covers N
macro_rules! sum {
    ($($x:expr),+ $(,)?) => { 0 $(+ $x)+ };
}
```

### Trailing-comma tolerance

Always allow `$(,)?` at the end of repetition groups. Users will expect it.

### Hygiene escape hatch

When a macro must use the caller's identifier, take it as a parameter (`$name:ident`) rather than naming it literally inside the macro.

For broader macro pitfalls (token-tree fragility, ambiguous fragment specifiers, recursion-limit failures), see anti-patterns §8.

---

## Refactor Anti-Patterns to Avoid

Things that look like refactors but degrade the design:

| Anti-pattern | Why it hurts | Better path |
|--------------|--------------|-------------|
| Wrapping every borrow in `Arc<T>` to dodge lifetimes | Hides ownership; allocator and atomic-refcount cost; "Rc-everywhere" code reads like Java | Trace actual ownership; introduce `&T` boundaries; use `Cow` where appropriate |
| Wrapping shared state in `Arc<Mutex<T>>` as the default | Becomes a contention bottleneck and a deadlock surface | Channels / actors / per-thread state; `RwLock` only when reads dominate; `parking_lot` over `std::sync` for hot paths |
| Cloning to silence borrowck (`.clone()` sprinkles) | Each clone hides a design decision; perf regression invisible to PR review | Borrow refactor; restructure call graph; `Cow<'_, T>` |
| Generic-over-everything (`fn foo<T, U, V, W>`) | Monomorphization blowup; opaque error messages; compile-time inflation | Concrete types at API boundary; generics only where polymorphism is actually used |
| Over-decomposing tiny functions across modules | Reader has to jump 5 files to read one logical operation | Inline back; locality > file-count |
| Introducing a trait for one impl | "Pattern theatre"; trait adds indirection with zero benefit | Keep concrete; introduce trait only when 2+ impls exist or testing needs a seam |
| Replacing `match` with `if let` chain on enums | Loses exhaustiveness checking on enum change | Keep `match` for enums; `if let` only on `Option`/`Result` short paths |
| Bulk `cargo fix --edition` then commit | Mixes mechanical and semantic changes | Separate PRs: one for mechanical migration, follow-ups for idiom adoption |
| Re-exporting everything from `lib.rs` ("flat public API") | Loses module boundaries; downstream pins to internal structure | `pub use` only the curated public surface; mark rest `pub(crate)` |
| Removing lifetime annotations the compiler "doesn't need" | Sometimes the elided lifetime is wrong even when compiles | Leave annotation if it documents intent at API boundary; remove only inside private fns |

---

## Refactor Checklist

Run before declaring a Rust refactor done:

1. **Build clean**: `cargo check --workspace --all-targets`.
2. **Lints pass**: `cargo clippy --workspace --all-targets -- -D warnings`.
3. **Format**: `cargo fmt --all -- --check`.
4. **Tests stay green**: `cargo nextest run --workspace` (or `cargo test`).
5. **Doc-tests still compile**: `cargo test --doc`.
6. **Public API surface unchanged** (or intentionally changed): `cargo public-api diff` against the previous tag.
7. **Bench did not regress** for hot paths: `cargo bench --bench <name>` if benchmarks exist.
8. **Edition / MSRV** unchanged unless this PR explicitly bumps them. Confirm `rust-version` in `Cargo.toml`.
9. **No new `unsafe` block without a `// SAFETY:` comment** (anti-patterns §9).
10. **No new `.unwrap()` / `.expect()` outside tests and `main`** (anti-patterns §5).

If any of these change unexpectedly, the refactor altered behavior — back out and reframe.

---

## Where to dig deeper

- Bad-pattern catalog: [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md)
  - §1 Ownership & Borrowing, §3 Type System, §5 Error Handling, §7 Trait Design, §8 Macros, §13 API Design
- Target idioms: [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md)
  - §1 API Guidelines C-* checklist, §2 Error handling, §6 Performance, §11 Documentation
- Language surface: [`builder/reference/rust-language-spec.md`](../../builder/reference/rust-language-spec.md)
  - Edition 2024 rules, AFIT, GATs, let-else, LazyLock, `use<…>` precise capture
