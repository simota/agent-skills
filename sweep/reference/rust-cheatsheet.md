# Rust Cleanup Cheatsheet (Edition 2024 / 1.85+)

Purpose: Sweep-flavored slice of the Rust knowledge base — what dead-code / unused-dep / orphan-file tools each catch, what is safe to remove, and what looks dead but isn't (FFI, `cfg`, derive-fed, proc-macro-emitted).

Baseline: **Rust 1.85+, Edition 2024, resolver = "3"**.

Source of truth (do not duplicate here):
- Cargo / dependency pitfalls → [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) §10
- Cargo toolchain / 2026 stack → [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md) §4
- Edition 2024 cleanup behavior → [`builder/reference/rust-language-spec.md`](../../builder/reference/rust-language-spec.md)

Companion: [`language-patterns.md`](./language-patterns.md) holds the cross-language tooling matrix (knip / vulture / staticcheck / cargo-udeps). Read this file for Rust-specific landmines and workspace-scale cleanup.

---

## Contents

- [Tooling Matrix](#tooling-matrix)
- [Safe-to-Remove Categories](#safe-to-remove-categories)
- [Tread-Carefully Categories (Rust Landmines)](#tread-carefully-categories-rust-landmines)
- [Unused Imports in Rust](#unused-imports-in-rust)
- [Workspace-Wide Cleanup](#workspace-wide-cleanup)
- [Feature Flag Cleanup](#feature-flag-cleanup)
- [Cleanup Workflow](#cleanup-workflow)

---

## Tooling Matrix

What each tool actually catches. Run them as a combined sweep — no single tool covers the full surface.

| Tool | Catches | Misses | Notes |
|------|---------|--------|-------|
| `cargo clippy -- -W dead_code` | Unused private items, unused fields, unused variants | Anything behind `#[allow(dead_code)]`, items reachable via `pub` API but not actually called, proc-macro outputs | Built into stable Rust; the cheapest first pass |
| `cargo +nightly udeps` | Dependencies declared in `Cargo.toml` but not referenced in any reachable code | Build-script-only deps, dev-deps used only in doc-tests in some setups | Requires nightly; original tool, slower |
| `cargo machete` | Same as `udeps` but runs on stable | Same misses; lighter check, faster | Preferred when stable-only environment |
| `cargo unused-features` | Feature flags declared in `Cargo.toml` but never selected by any consumer | Features referenced only behind nested feature-of-feature paths | Useful before deleting `[features]` entries |
| `cargo +nightly rustc -- -W unused-extern-crates` | `extern crate foo;` declarations with no use | Modern `use` imports (Edition 2018+) | Mostly relevant for legacy crates |
| `cargo +nightly rustc -Z unstable-options --pretty=expanded` | Reveals what proc-macros / `#[derive]` actually emit | Nothing about reachability | Use when you suspect "dead" items are actually emitted by a macro |
| `cargo bloat --crates` | Largest binary-size contributors | Source-level dead code | Proxy signal — a large crate you barely use is a deletion candidate |
| `cargo-modules structure` | Visualizes module / item graph for one crate | Cross-crate workspace edges | Helps decide whether a module is leaf-reachable |
| `cargo tree -e features` | Where features are actually pulled in (and by whom) | Whether the feature is exercised at runtime | Trace transitively-enabled features before deletion |

### Recommended combined sweep (stable)

```bash
cargo clippy --workspace --all-targets -- -W dead_code -W unused
cargo machete                                                       # unused crate deps
cargo unused-features analyze                                       # unused feature flags
cargo tree -e features --workspace                                  # confirm before deletion
cargo bloat --release --crates --workspace                          # size signal
```

### Nightly augmentation

```bash
cargo +nightly udeps --workspace --all-targets
cargo +nightly rustc -- -W unused-extern-crates
```

---

## Safe-to-Remove Categories

Items in these categories can typically be removed after a single Lens/Scout reachability check:

1. **`#[allow(dead_code)]` annotations + the item they suppress.** If clippy without the allow flags the item AND no test / no `pub` API / no FFI symbol references it, drop both.
2. **Unused crate features declared in `Cargo.toml`.** Confirm via `cargo metadata --format-version=1 | jq` that no consumer's `default-features` or explicit `features = [...]` selects it.
3. **Re-exports nobody imports.** `pub use foo::Bar;` at the crate root with zero downstream importers (verify via `cargo public-api` and / or grep across the workspace).
4. **Test-only fixtures referenced by no `#[test]`, `#[tokio::test]`, `#[rstest]`, or `#[proptest]`.** Includes `tests/common/` helpers used by no integration test.
5. **`pub(crate)` items not consumed within the crate.** These can never escape — if local use is gone, the item is dead.
6. **`mod foo;` declarations whose `foo.rs` / `foo/mod.rs` is empty or contains only items in category 1.**
7. **`[dev-dependencies]` entries with no `#[cfg(test)]` consumer.** `cargo machete` flags these.
8. **`build.rs` outputs that nobody includes via `include!`, `OUT_DIR`, or `env!`.** Check `target/<profile>/build/<crate>-*/out/` for orphans.

Workflow: flag → confirm via reachability check → remove → run `cargo check --workspace --all-targets --all-features` → commit in a small focused PR.

---

## Tread-Carefully Categories (Rust Landmines)

Items that LOOK dead but break the world when removed. Do **not** delete without explicit verification.

### FFI / linker-retained symbols

```rust
// Looks unused — clippy may not even flag it, but downstream consumers depend on it.
#[no_mangle]
pub extern "C" fn my_lib_init() -> i32 { 0 }

#[unsafe(no_mangle)]                  // Edition 2024 spelling — same meaning
pub extern "C" fn another_export() {}

#[export_name = "specific_symbol"]
pub extern "C" fn renamed_for_ffi() {}
```

These symbols are consumed by C / C++ / Python / JNI / Wasm hosts that the Rust compiler cannot see. **Never** auto-delete an `#[no_mangle]`, `#[export_name]`, `#[unsafe(no_mangle)]`, or `extern "C" fn` exported item.

Verify before delete:
- Search the entire repository, including non-Rust code, for the symbol name.
- Check `.so` / `.dylib` / `.dll` consumers (Python `ctypes`, Node `ffi-napi`, C headers in `include/`).
- If in doubt, ask. FFI removals are post-release bug sources.

### `#[used]` and `#[link_section]`

```rust
#[used]
static REGISTRATION_HOOK: extern "C" fn() = init_hook;

#[link_section = ".init_array"]
#[used]
static GLOBAL_CTOR: extern "C" fn() = before_main;
```

Linker keeps these even though no Rust code references them. Removing breaks startup hooks, GPU shader registration, plugin systems.

### `#[cfg(feature = "...")]` items

```rust
#[cfg(feature = "tracing-otlp")]
pub fn export_to_otlp() { /* ... */ }
```

"Unused" in the current feature set means "used in another feature set". `cargo udeps`/`machete` know to combine with `--all-features`. Always run the sweep with `--all-features` AND with each feature-combination that ships in CI before removing.

### `#[cfg(test)]` items

```rust
#[cfg(test)]
pub(crate) fn fake_clock() -> impl Clock { /* ... */ }
```

These appear unused under release builds. Verify by running `cargo check --tests` and `cargo nextest run` before removing.

### Trait impls referenced via trait objects

```rust
impl Renderer for SvgRenderer { /* ... */ }
// Called as `Box<dyn Renderer>::render(...)` from a registry — never directly.
```

`cargo clippy -- -W dead_code` cannot trace `dyn Trait` dispatch. Search for `dyn Renderer` / `Box<dyn Renderer>` / `&dyn Renderer` patterns before deletion.

### `#[derive(...)]`-fed items

```rust
#[derive(Serialize)]      // expands to an `impl Serialize for Config`
pub struct Config { /* ... */ }
```

The derived impl is auto-generated; removing the type breaks consumers, removing the derive breaks the wire format. `cargo expand` (or `cargo +nightly rustc -- -Zunpretty=expanded`) reveals the generated items.

### `Drop` impls

```rust
impl Drop for ConnectionGuard { fn drop(&mut self) {} }
```

Even an empty `Drop` changes whether the struct is "trivially-destructible" — removing it can shift drop ordering, change `const` eligibility, and reorder destructor effects across the whole program. **Never** remove a `Drop` impl as cleanup.

### Procedural macro outputs

Proc macros (`#[tokio::main]`, `#[derive(Builder)]`, `sqlx::query!`, `#[axum::debug_handler]`) emit items the compiler sees but greps can't find. Use `cargo expand` to inspect.

---

## Unused Imports in Rust

`cargo fmt` does NOT remove unused imports. Use clippy:

```bash
cargo clippy --workspace --all-targets -- \
  -W clippy::redundant_imports \
  -W clippy::single_component_path_imports \
  -W unused_imports
```

Related lints worth turning on for cleanup PRs:

| Lint | Catches |
|------|---------|
| `clippy::redundant_imports` | `use foo::Bar; use foo::Bar;` and similar |
| `clippy::single_component_path_imports` | `use serde;` (rare, mostly noise) |
| `clippy::wildcard_imports` | `use foo::*;` outside prelude / re-export modules |
| `unused_imports` | Builtin — straightforward unused `use` items |
| `unused_qualifications` | `std::vec::Vec::new()` when `Vec` is in scope |

Edition 2024 nuance: the prelude grew (`Future`, `IntoFuture`); previously-needed explicit imports may now warn as redundant. Run cleanup right after an edition migration to capture the easy wins.

Nested `use` consolidation example:

```rust
// Before
use crate::db::User;
use crate::db::Order;
use crate::db::Invoice;

// After — clippy can suggest, rustfmt does NOT do this automatically
use crate::db::{Invoice, Order, User};
```

---

## Workspace-Wide Cleanup

Workspaces accumulate dead crates, dead members, and version drift. Sweep them with workspace-level tools.

### Dead workspace members

```bash
cargo metadata --format-version=1 | jq -r '.workspace_members[]'
# Cross-reference against actual usage; an unused crate compiles but ships nothing.
```

Signals a member crate is dead:
- No other workspace crate has it in `[dependencies]`.
- No `[[bin]]` / `[[example]]` references it.
- No CI workflow runs `cargo test -p <crate>`.

### Version drift in `[workspace.dependencies]`

Rust 1.64+ supports `[workspace.dependencies]` to unify versions. If members still declare versions individually, consolidate:

```toml
# Cargo.toml (workspace root)
[workspace.dependencies]
serde   = { version = "1.0", features = ["derive"] }
tokio   = { version = "1", features = ["full"] }
anyhow  = "1"

# crates/foo/Cargo.toml
[dependencies]
serde   = { workspace = true }
tokio   = { workspace = true }
anyhow  = { workspace = true }
```

Detection: `cargo tree --duplicates` lists crates compiled at multiple versions — usually a workspace-unification opportunity.

### `cargo workspaces` plugin

```bash
cargo install cargo-workspaces
cargo workspaces list                 # show members
cargo workspaces changed              # which members changed vs base
cargo workspaces exec cargo check     # run a command in every member
```

Helpful for confirming "this PR really only touches X" before mass deletes.

### Public API tracking

```bash
cargo install cargo-public-api
cargo public-api diff <prev-tag>      # what changed in the public surface
```

If cleanup accidentally removes a `pub` item, the diff shows it. Block release on it.

---

## Feature Flag Cleanup

Feature flags rot fast. Three deletion-worthy categories:

### Unused features (no consumer)

```bash
cargo unused-features analyze --output-file features.json
```

Outputs the set of declared features not selected by `default`, any other feature, or any consumer crate. Safe to delete after verification.

### Mutually-exclusive features that break `--all-features`

```toml
[features]
runtime-tokio = ["dep:tokio"]
runtime-async-std = ["dep:async-std"]    # both can't coexist — but --all-features tries
```

CI usually runs `cargo check --all-features`; if it fails, the feature design is broken. Fix by:
1. Splitting into separate crates, or
2. Using a sentinel error: `compile_error!("Cannot enable both runtime-tokio and runtime-async-std")`.

### Dead conditional `cfg`

```rust
#[cfg(feature = "experimental-cache")]   // feature was renamed last year
fn experimental_path() { /* dead */ }
```

After feature deletion, the `#[cfg(feature = "...")]` blocks become permanently unreachable. Strip them in the same PR.

---

## Cleanup Workflow

Recommended ordering for a Rust cleanup pass:

1. **Baseline** — `cargo check --workspace --all-targets --all-features`. Capture compile time.
2. **Run the combined stable sweep** (see [Tooling Matrix](#tooling-matrix)).
3. **Triage by category** — file each finding into Safe-to-Remove vs Tread-Carefully.
4. **For each Tread-Carefully**, run the verifying check (FFI grep, `cargo expand`, `--all-features` build).
5. **Delete in atomic commits** — one logical group per commit. Never mix "remove unused dep" with "rename module".
6. **Re-run the sweep + tests** — `cargo nextest run --workspace`, `cargo test --doc`, `cargo clippy -- -D warnings`.
7. **Diff public API** — `cargo public-api diff` to confirm no accidental surface change.
8. **Measure** — re-check compile time, binary size (`cargo bloat`), and dep count (`cargo tree --depth 1 --workspace | wc -l`).
9. **Document the deletion rationale** in the PR description, especially for FFI / `cfg` / `Drop` adjacent removals.

---

## Where to dig deeper

- Cargo / dependency pitfalls: [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) §10
- Cargo & toolchain 2026 stack: [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md) §4
- Edition 2024 cleanup nuances (prelude growth, `unsafe extern`, `gen` keyword): [`builder/reference/rust-language-spec.md`](../../builder/reference/rust-language-spec.md)
- Cross-language tooling matrix: [`language-patterns.md`](./language-patterns.md)
