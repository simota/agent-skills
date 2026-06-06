# Rust Code-Review Cheatsheet (Judge)

Agent-specific slice for **Judge** (multi-engine code review — bugs / security / logic / intent). Baseline assumes Rust 1.85+ / Edition 2024 (as of 2026-05).

This file does **not** duplicate the source of truth. Read it alongside:

- [`builder/reference/rust-best-practices.md §1 Rust API Guidelines`](../../builder/reference/rust-best-practices.md) — full C-* checklist (the canonical review oracle)
- [`builder/reference/rust-best-practices.md §2 Error handling`](../../builder/reference/rust-best-practices.md) — thiserror / anyhow / snafu decision tree
- [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) — 120+ anti-patterns with clippy IDs, especially §4 async and §9 unsafe
- [`builder/reference/rust-language-spec.md`](../../builder/reference/rust-language-spec.md) — Edition 2024 changes, dyn compatibility, unsafe rules

The role of this cheatsheet: **a priority-ordered checklist + engine-routing rules + clippy policy + false-positive guide so review effort focuses on findings worth fixing**.

---

## 1. Priority checklist — highest signal first

Numbered roughly by signal-to-noise ratio. The top items catch real bugs; the bottom items catch style drift.

### Tier 1 — Unsafety, deadlocks, leaks (block merge)

1. **`unsafe` blocks: SAFETY comment present?**
   - Every `unsafe { ... }` MUST carry a `// SAFETY: <invariants proven here>` comment. Without it the reviewer cannot verify, and "unsafe rot" sets in.
   - Tool: `clippy::undocumented_unsafe_blocks` (deny in CI).
   - See [anti-patterns §9.13](../../builder/reference/rust-anti-patterns.md#9-unsafe-pitfalls-high-stakes) + [language-spec §6.5](../../builder/reference/rust-language-spec.md#65-safety-comment-template).

2. **`.unwrap()` / `.expect()` in non-test code: justified?**
   - In libraries: replace with `?` or a typed error.
   - In binaries: only acceptable with an `// INVARIANT: ...` comment proving infallibility.
   - Tool: `clippy::unwrap_used`, `clippy::expect_used` (deny in libs, warn in bins).

3. **`std::sync::MutexGuard` (or `parking_lot::MutexGuard`) held across `.await`**
   - Future becomes `!Send`; either won't compile under `tokio::spawn` *or* causes deadlocks under contention.
   - Tool: `clippy::await_holding_lock` (deny).
   - See [anti-patterns §4.A](../../builder/reference/rust-anti-patterns.md#4a-mutexguard-across-await--minimal-reproduction).

4. **`tokio::spawn` orphan tasks (handle dropped)**
   - Panics in orphaned tasks are silently swallowed → bugs fester.
   - Fix: `JoinSet` or `TaskTracker` retains handles; on join error check `is_panic()`.
   - See [anti-patterns §4.C](../../builder/reference/rust-anti-patterns.md#4c-orphan-task--panic-vanishes).

5. **Mutable global state (`static mut` or unprotected `static`)**
   - `static mut` is deprecated in Edition 2024 — multiple mutable references trivially obtainable, instant UB.
   - Fix: `LazyLock<Mutex<T>>` or `OnceLock<T>` (stable since 1.70).
   - See [anti-patterns §9.17](../../builder/reference/rust-anti-patterns.md#9-unsafe-pitfalls-high-stakes).

### Tier 2 — Public API correctness (block merge for library crates)

6. **`Box<dyn Error>` in library public API**
   - Public errors should be a concrete `thiserror`-derived enum so callers can match.
   - `anyhow::Error` / `Box<dyn Error>` is for binary code, not crate boundaries.
   - See [best-practices §2 Error handling](../../builder/reference/rust-best-practices.md#2-error-handling-patterns--deep).

7. **`#[non_exhaustive]` missing on enums/structs likely to grow**
   - Adding a variant to a public enum is a breaking change without `#[non_exhaustive]`.
   - Add to all public error enums, status enums, and config structs.

8. **Re-exporting types from a transitive dep without owning the version**
   - If `mycrate v1.0` re-exports `tokio::sync::Mutex`, bumping `tokio` becomes a `mycrate` breaking change.
   - Either re-export from a workspace dep with version control, or newtype.

9. **Feature flag mutual exclusion**
   - Cargo features must be *additive*. If `--features a,b` doesn't compile, `--all-features` breaks (CI failure waiting to happen).
   - See [best-practices §3.4](../../builder/reference/rust-best-practices.md#34-feature-flags--additive-only).

10. **Public struct with public fields**
    - Locks in representation; no future invariants. `pub struct User { pub email: String }` can never validate `email` without a breaking change.
    - C-STRUCT-PRIVATE violation in [best-practices §1.10](../../builder/reference/rust-best-practices.md#110-future-proofing).

### Tier 3 — Design smells (review comment, not block)

11. **Clone-to-escape-borrow-checker**
    - `let s = self.field.clone();` to call `&mut self.method(...)` — borrows could be redesigned.
    - Often signals struct should be split (`SplitBorrow` pattern, see [anti-patterns §1.B](../../builder/reference/rust-anti-patterns.md#1b-split-borrows-escape-hatch)).

12. **Manual lifetime annotation the compiler would elide**
    - `fn foo<'a>(x: &'a str) -> &'a str` is just noise; elision rules already produce that.
    - See [language-spec §2.3](../../builder/reference/rust-language-spec.md#23-lifetime-elision-rules).

13. **`async fn` in public trait without considering RPITIT / async-trait split**
    - Static-dispatch (RPITIT) is allocation-free but not object-safe.
    - `#[async_trait]` allocates per call but allows `dyn Trait`.
    - The choice matters; reviewer flags missing intent.
    - See [best-practices §8.7](../../builder/reference/rust-best-practices.md#87-async-fn-in-traits--the-static-vs-dynamic-split).

14. **`Drop` impl that may panic or call fallible I/O**
    - Panic in `Drop` during unwinding = process abort. Use `if thread::panicking() { return; }` guard, or expose `close() -> Result<...>`.
    - See [anti-patterns §7.9 + §7.B](../../builder/reference/rust-anti-patterns.md#7-trait-design-pitfalls).

15. **`Default` / `Clone` impl that does I/O or takes a lock**
    - Both are expected to be cheap and infallible. Use a `Builder` or `try_clone() -> Result<...>` instead.

---

## 2. Intent-vs-code mismatch signals (Rust-specific)

Judge's distinctive capability is catching when the code does something *other than what the author intended*. Rust-specific signals:

| Mismatch signal | What to ask |
|-----------------|------------|
| Function named `with_*` / `into_*` but takes `&self` | Per C-CONV: `into_` consumes (`self`), `as_` borrows. Name conflicts with signature → ambiguous to callers |
| Returns `Result<T, E>` but the only caller `.unwrap()`s | Either the error is impossible (use `T` directly) or `unwrap` is a bug |
| Generic bound looser than docstring promises | `fn foo<T: Clone>(...)` but doc says "for any hashable T" — bound is wrong direction |
| `#[must_use]` missing on a builder / fluent return | Builder pattern that returns `Self` but the caller drops it on the floor |
| `pub` on a fn the docs say is internal | `pub(crate)` was intended; public exposure widens the API surface accidentally |
| `Vec<T>` returned where docs say "stream of T" | Should be `impl Iterator<Item = T>` or `impl Stream<Item = T>` |
| Function uses `tokio::spawn` but the doc says "blocking" | Task escapes function scope, lifetime confusion likely |
| `impl Display` body uses `format!(...)` then writes the string | Should use `write!(f, ...)` directly — avoids the intermediate alloc; see [anti-patterns §7.8](../../builder/reference/rust-anti-patterns.md#7-trait-design-pitfalls) |

---

## 3. Clippy lint policy

The default clippy lints are too noisy for review; Judge applies a policy.

### 3.1 Elevate to `deny` (block merge)

```toml
# In .cargo/config.toml or Cargo.toml [lints.clippy]
unwrap_used               = "deny"
expect_used               = "deny"        # except in tests; allow per-mod via #![cfg_attr(test, allow(...))]
await_holding_lock        = "deny"
await_holding_refcell_ref = "deny"
undocumented_unsafe_blocks = "deny"
missing_safety_doc        = "deny"        # public unsafe fn must document # Safety
mem_forget                = "deny"        # leaks resources; almost never intentional
indexing_slicing          = "deny"        # in hot-path / lib code; replace with .get(i)
panic                     = "deny"        # explicit `panic!()` in library code
todo                      = "warn"        # warn in PR; deny in release
unimplemented             = "warn"
dbg_macro                 = "deny"        # dbg! in committed code is always a bug
print_stdout              = "deny"        # in libraries; use tracing
```

### 3.2 Keep as `warn` (style, low confidence)

- `clippy::pedantic` family — useful but noisy; consider per-file `#![warn(clippy::pedantic)]` on new code only.
- `clippy::nursery` — experimental lints; review value before adopting.
- `clippy::cargo` — packaging hygiene (warn in CI, fix at release time).

### 3.3 Default-allow (false-positive heavy)

- `clippy::module_name_repetitions` — common in re-export modules (`fn user::user_repo()`); usually a legitimate naming choice.
- `clippy::needless_pass_by_value` — wrong for `Drop` types where consumption is intentional.
- `clippy::missing_errors_doc` / `clippy::missing_panics_doc` — useful goal but noisy on internal code; opt-in per crate.
- `clippy::redundant_pub_crate` — sometimes by design for re-export discipline.
- `clippy::module_inception` — canonical pattern (`foo::foo::Foo`) is fine in many layouts.
- `clippy::similar_names` — flags `request` vs `response` as similar; rarely actionable.

### 3.4 Per-crate context

- **Hot-path / perf-critical crate**: enable `clippy::indexing_slicing` deny + `clippy::redundant_clone` deny.
- **Library crate published to crates.io**: also deny `clippy::missing_safety_doc`, `clippy::result_large_err`, `clippy::large_enum_variant`.
- **CLI binary**: relax `clippy::print_stdout` (it's the CLI), keep `clippy::unwrap_used` warn.
- **Test code**: blanket `#[cfg_attr(test, allow(clippy::unwrap_used, clippy::expect_used))]` is fine.

---

## 4. API Guidelines audit (C-* checklist highlights)

The full C-* checklist (37 items) lives in [`rust-best-practices.md §1`](../../builder/reference/rust-best-practices.md#1-rust-api-guidelines--full-c--checklist). For a PR review, prioritize these:

| ID | Highest-signal violation | Why it matters in review |
|----|--------------------------|--------------------------|
| **C-CASE** | `pub fn getUser()` instead of `get_user()` | API users feel non-idiomatic immediately |
| **C-GETTER** | `pub fn get_id(&self)` where only one `id` exists | Should be `id()` per Rust naming |
| **C-CONV** | `into_` taking `&self` (or `as_` returning owned) | Name lies about cost — caller surprise |
| **C-COMMON-TRAITS** | Public type missing `Debug` | Cannot be logged via `tracing` / `dbg!` |
| **C-GOOD-ERR** | Error type missing `Send + Sync + 'static` | Can't be sent across threads or stored in `anyhow::Error` |
| **C-SEND-SYNC** | Type contains `Rc` but is documented as thread-safe | Silent compile failure at use site |
| **C-EXAMPLE** | Public fn with no `# Examples` | First barrier to adoption |
| **C-FAILURE** | Public fallible fn with no `# Errors` / `# Panics` | Callers can't reason about failure modes |
| **C-NEWTYPE** | `fn transfer(from: u64, to: u64, amount: u64)` | Argument transposition is a compile-time error with newtypes |
| **C-CUSTOM-TYPE** | `bool` parameter | `fn open(p, true)` is unreadable; replace with enum |
| **C-VALIDATE** | Validation re-done at every layer | Either validate once at boundary or pass a validated newtype |
| **C-STRUCT-PRIVATE** | Public struct with `pub` fields | Locks representation forever (breaking-change tax) |
| **C-SEALED** | Public trait used by external crates without sealed marker | Once shipped, adding a required method = breaking change |
| **C-DTOR-FAIL** | `Drop::drop` calls fallible I/O with `.unwrap()` | Panic in Drop during unwind = process abort |

---

## 5. Edition 2024 migration smells

If the codebase is on Edition 2024 (default since 1.85), watch for legacy patterns that didn't get migrated.

| Smell | Edition 2024 form | Source |
|-------|------------------|--------|
| `#[no_mangle]` | `#[unsafe(no_mangle)]` | [language-spec §1.2](../../builder/reference/rust-language-spec.md#12-edition-2024--full-list-of-breaking-ish-changes) |
| `#[export_name = "..."]` | `#[unsafe(export_name = "...")]` | Same |
| `#[link_section = "..."]` | `#[unsafe(link_section = "...")]` | Same |
| `extern "C" { ... }` | `unsafe extern "C" { ... }` with `safe fn` / `unsafe fn` per item | Same |
| `unsafe fn body { unsafe op }` (whole body) | Each unsafe op in its own `unsafe { ... }` block | `unsafe_op_in_unsafe_fn` lint |
| `&MY_STATIC` on `static mut` | `&raw const MY_STATIC` or migrate to `Mutex` / `OnceLock` | Hard error in 2024 |
| "object safe" in docs / comments | "dyn compatibility" — terminology renamed | [language-spec §3.5](../../builder/reference/rust-language-spec.md#35-trait-object-safety--renamed-to-dyn-compatibility-2024) |
| `fn returns_impl<'a>(x: &'a Foo) -> impl Trait` | Add `+ use<'a>` to constrain capture explicitly | RFC 3498 |
| `std::env::set_var` without `unsafe` | Now requires `unsafe { ... }` | Edition 2024 |
| `if let PAT = expr.lock() { ... } else { ... }` | Temporary scope changed — re-verify locks aren't held in the else | RFC 3535 |

---

## 6. Cross-engine review tactics (Claude / Codex / agy)

Judge orchestrates multiple engines. Rust files have specific routing affinity:

| File / pattern | Primary engine | Secondary | Why |
|----------------|---------------|----------|-----|
| `unsafe` block heavy (FFI, custom allocators, `Pin` projection) | **Codex** | Claude | Codex was trained on sandboxed exec including borrow-check failure cases |
| Public API surface (`pub` items, trait definitions) | **Claude** | Codex | Claude is stronger at API/doc design coherence + naming conventions |
| Async correctness (Tokio, cancel-safety, `select!`) | **Both** (run both) | — | Failure modes are subtle; multi-engine cross-check pays off |
| Macro-heavy code (proc-macros, declarative macros) | **Claude** | agy | Claude handles syn/quote AST reasoning well |
| Performance hot path (criterion-backed claims) | **Codex** | Claude | Codex can run/verify benchmark deltas in its sandbox |
| Error type design (`thiserror` / `anyhow` choice) | **Claude** | Codex | Library-vs-app boundary is a design call |
| Build / Cargo config (`Cargo.toml`, `deny.toml`, CI) | **Claude** | agy | Documentation cross-reference matters more than codegen |
| `no_std` / embedded | **Codex** | — | Sandboxed verification of target builds |

**Grounding step (mandatory)**: every Rust review finding must cite a clippy lint, a Rust Reference section, or one of the `builder/reference/rust-*.md` rows. Free-text "this looks wrong" is rejected by Judge's grounding filter.

---

## 7. Common false positives (don't ship these as findings)

| False positive | Why it's NOT a bug |
|---------------|---------------------|
| `clippy::needless_pass_by_value` on a `Drop` type | Consuming the value to run its destructor is the whole point |
| `clippy::module_inception` (`mod foo { struct Foo; }`) | Canonical Rust layout — one module per type |
| `clippy::module_name_repetitions` (`user::UserRepo`) | Standard re-export discipline (caller writes `user::UserRepo`, not `user::Repo`) |
| `clippy::missing_const_for_fn` on a fn that calls a non-const fn | Can't be const without ecosystem-wide constness; flagging it is noise |
| `clippy::large_types_passed_by_value` on `Copy` types | If it's `Copy`, the by-value pass is a register move, not a stack copy |
| "Function has `&mut self` but doesn't mutate" | May be deliberate for `Drop` invariants or future-proofing API |
| "Generic bound `T: Clone` unused in body" | The compiler removes it; sometimes a doc-only constraint |
| `clippy::single_match` on a `match` with a `// TODO` for future variants | Author left it open deliberately |
| `unsafe fn` with no `unsafe` operations | Sometimes the contract is `pub unsafe fn` to signal "caller upholds X" even when the body itself is safe |
| `#[allow(clippy::unwrap_used)]` in `examples/` | Examples optimize for clarity, not error handling |
| `clippy::too_many_arguments` on builder/visitor methods | The Builder pattern intentionally fans out; the lint should be `#[allow]`-ed at the method |

---

## 8. Judge-specific routing rules for Rust

1. **No finding without a citation.** Every finding must reference a clippy lint, an API-guideline ID, an anti-pattern row, or a Rust Reference URL. "Looks wrong" gets dropped.
2. **Tier 1 findings block merge.** `unsafe` without SAFETY, MutexGuard across await, orphan task, `static mut` — these are not "style". They get the highest severity.
3. **Library vs binary distinction.** `.unwrap()` in `src/main.rs` of a CLI is acceptable with an INVARIANT comment; the same in a `lib.rs` is Tier 2.
4. **Edition matters.** Check `edition = "2024"` in `Cargo.toml`. If 2021, apply the older clippy defaults; if 2024, raise the bar (unsafe attribute migrations, etc.).
5. **Multi-engine cross-check on async + unsafe.** These two domains are subtle enough that the marginal cost of running both Claude and Codex pays off.
6. **False-positive filter (§7) runs before publishing.** Don't burn reviewer trust on noise.
7. **Suggest, don't dictate, on style.** "Consider `Cow<'a, str>` if borrow sometimes works" not "must change to Cow". Save imperative tone for Tier 1 + Tier 2.

---

## Sources

- Rust API Guidelines — https://rust-lang.github.io/api-guidelines/checklist.html
- Clippy lint reference — https://rust-lang.github.io/rust-clippy/master/index.html
- The Rustonomicon (unsafe rules) — https://doc.rust-lang.org/nomicon/
- The Rust Reference — https://doc.rust-lang.org/reference/
- Rust Edition 2024 guide — https://doc.rust-lang.org/edition-guide/rust-2024/
- Tokio "Async: What You Need to Know" — https://tokio.rs/tokio/topics/async
- Source of truth for all underlying knowledge:
  - [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md) (API guidelines, error handling, async, async-trait split)
  - [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) (120+ anti-patterns with clippy mapping)
  - [`builder/reference/rust-language-spec.md`](../../builder/reference/rust-language-spec.md) (Edition 2024, dyn compatibility, unsafe rules)
