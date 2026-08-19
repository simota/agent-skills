# Rust Refactoring Cheatsheet (Edition 2024 / 1.85+)
Purpose: Zen-flavored slice of the Rust knowledge base — code-smell-to-idiom transformations, renaming hygiene, magic-number cleanup, macro hygiene, and refactor anti-patterns. Behavior-preserving only.
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Function Extraction Signals (Rust-specific)
1. **Lifetime juggling > 2 parameters with explicit `'a`** — extract a helper that owns its inputs, or accepts `Cow<'_, T>`. The new helper's signature usually elides automatically.
2. **Repeated `?`-chains all wrapping the same `.context("loading X")`** — extract a typed helper that returns a domain-specific error; the call site loses the noise.
3. **`match` arms with shared post-processing** — extract the post-processing as a free function or closure; arms reduce to value computation.
4. **Long iterator chain with named intermediates** — break at the named binding; each becomes a self-documenting helper (`fn active_orders(&self) -> impl Iterator<Item = &Order>`).
5. **`unsafe` block doing 3+ unrelated things** — extract each into its own `unsafe fn` (or safe wrapper around a single `unsafe`) with a documented `# Safety` contract.
6. **Closures capturing 4+ variables** — promote to a named struct + `impl Fn` or a free function with explicit parameters.
- A 3-line block used in one place; inlining is clearer.
- A helper that requires more lifetime annotations than the inlined version.
---
## Renaming Hygiene (C-CASE / API Guidelines)
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
## Macro Hygiene Signals
- **Capture leaks → use `$crate::`**
- **Repetition with separators**
- **Trailing-comma tolerance**
- **Hygiene escape hatch**
---
## Refactor Anti-Patterns to Avoid
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
1. **Build clean**: `cargo check --workspace --all-targets`.
2. **Lints pass**: `cargo clippy --workspace --all-targets -- -D warnings`.
3. **Format**: `cargo fmt --all -- --check`.
4. **Tests stay green**: `cargo nextest run --workspace` (or `cargo test`).
5. **Doc-tests still compile**: `cargo test --doc`.
6. **Public API surface unchanged** (or intentionally changed): `cargo public-api diff` against the previous tag.
7. **Bench did not regress** for hot paths: `cargo bench --bench <name>` if benchmarks exist.
8. **Edition / MSRV** unchanged unless this PR explicitly bumps them. Confirm `rust-version` in `Cargo.toml`.
9. **No new `unsafe` block without a `// SAFETY:` comment**.
10. **No new `.unwrap()` / `.expect()` outside tests and `main`**.
