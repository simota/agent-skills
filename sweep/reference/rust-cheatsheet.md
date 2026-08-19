# Rust Cleanup Cheatsheet (Edition 2024 / 1.85+)
Purpose: Sweep-flavored slice of the Rust knowledge base — what dead-code / unused-dep / orphan-file tools each catch, what is safe to remove, and what looks dead but isn't (FFI, `cfg`, derive-fed, proc-macro-emitted).
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Tooling Matrix
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
- **Recommended combined sweep (stable)**
- **Nightly augmentation**
---
## Tread-Carefully Categories (Rust Landmines)
### FFI / linker-retained symbols
- Search the entire repository, including non-Rust code, for the symbol name.
- Check `.so` / `.dylib` / `.dll` consumers (Python `ctypes`, Node `ffi-napi`, C headers in `include/`).
- If in doubt, ask. FFI removals are post-release bug sources.
- **`#[used]` and `#[link_section]`**
- **`#[cfg(feature = "...")]` items**
- **`#[cfg(test)]` items**
- **Trait impls referenced via trait objects**
- **`#[derive(...)]`-fed items**
- **`Drop` impls**
- **Procedural macro outputs**
---
## Unused Imports in Rust
| Lint | Catches |
|------|---------|
| `clippy::redundant_imports` | `use foo::Bar; use foo::Bar;` and similar |
| `clippy::single_component_path_imports` | `use serde;` (rare, mostly noise) |
| `clippy::wildcard_imports` | `use foo::*;` outside prelude / re-export modules |
| `unused_imports` | Builtin — straightforward unused `use` items |
| `unused_qualifications` | `std::vec::Vec::new()` when `Vec` is in scope |
---
## Workspace-Wide Cleanup
### Dead workspace members
- No other workspace crate has it in `[dependencies]`.
- No `[[bin]]` / `[[example]]` references it.
- No CI workflow runs `cargo test -p <crate>`.
- **Version drift in `[workspace.dependencies]`**
- **`cargo workspaces` plugin**
- **Public API tracking**
---
## Feature Flag Cleanup
- **Unused features (no consumer)**
### Mutually-exclusive features that break `--all-features`
1. Splitting into separate crates, or
2. Using a sentinel error: `compile_error!("Cannot enable both runtime-tokio and runtime-async-std")`.
- **Dead conditional `cfg`**
---
## Cleanup Workflow
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
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
- Cross-language tooling matrix: [`language-patterns.md`](./language-patterns.md)
