# Rust Architecture Cheatsheet (Edition 2024 / 1.85+)
Purpose: Atlas-flavored slice of the Rust knowledge base — workspace architecture patterns, trait-based DI, visibility hygiene, circular-dep detection, public-API surface management, and ADR triggers specific to Rust.
- General semantics and version-sensitive claims → [grounding gate](../../builder/reference/implementation-policy.md#language-and-toolchain-grounding)
---
## Module Visibility Hygiene
| Modifier | Reachable from |
|----------|----------------|
| (none, default) | Same module only |
| `pub(self)` | Same module (explicit form of default) |
| `pub(super)` | Parent module |
| `pub(in path::to::mod)` | Within the named path |
| `pub(crate)` | Entire crate |
| `pub` | Public API — anyone who depends on this crate |
- **Façade pattern with `pub use`**
### Sealed trait pattern (prevent downstream impls)
- You want forward-compat freedom to add methods (no breaking-change risk from downstream impls).
- The trait represents a closed enumeration of behaviors (Rust API Guidelines C-SEALED).
- **Visibility audit signal**
---
## Circular Dependency Detection
### Tools
| Tool | Scope | Use For |
|------|-------|---------|
| `cargo-modules structure` | Per-crate module graph | Diagnose `mod` cycles, orphan modules, deep nesting |
| `cargo-depgraph` | Workspace-level crate graph | Visualize crate→crate edges, find unintended deps |
| `cargo tree --workspace` | Direct/transitive dep tree | Inspect what a crate actually pulls in |
| `cargo tree --duplicates` | Version conflicts across deps | Find unintended version splits (a sign of weak workspace mgmt) |
| `cargo-deny check bans` | Policy-driven dep audit | Enforce "no X depends on Y" rules in CI |
### Common circular smells in Rust
1. **`app → infra → app` via callback registration.** The infra layer calls back into application services through a registered closure or trait object. Fix: invert via a trait owned by `app`; `infra` implements it.
2. **Crate A re-exports types from Crate B, while Crate B uses traits defined in Crate A.** Compiles but creates an "if you import either, you import both" coupling. Fix: move the shared types into a `shared-kernel` / `common` crate.
3. **Module cycle inside a crate**: `mod a` uses items from `mod b` which uses items from `mod a`. Rust allows it within one crate but it muddies reasoning. Fix: extract shared items into a parent or sibling module.
4. **Test code reaching into prod code via `pub(crate)` shortcuts that grow into a backdoor.** Fix: keep a clean `pub(crate)` test API or use `#[cfg(test)] pub` only.
---
## God-Crate Split Signals
- **Compile time > 60s** for a clean incremental rebuild of one crate.
- **`[features]` table has > 8 entries** suggesting bundled concerns (each feature represents a hidden sub-crate).
- **Workspace contains exactly one crate** + `examples/` + `tests/` — the workspace is a fiction.
- **`lib.rs` re-exports everything** (`pub use crate::*;`) — there is no module boundary.
- **A single file > 2000 LOC** without natural sub-modules.
- **PRs from different teams routinely touch the same crate** — change ownership is unclear.
- **`cargo doc` for the crate takes > 30s** — it's documenting too many concerns at once.
---
## Workspace Configuration Deltas
- **`[workspace.dependencies]` (1.64+)**
- **`[workspace.lints]` (1.74+)**
- **`resolver = "3"`**
---
## Public API Surface Management
- **`cargo-public-api`**
- **`cargo-semver-checks`**
- **`#[non_exhaustive]` discipline**
### Version-bump rules of thumb
| Change | SemVer impact |
|--------|---------------|
| Add a `pub` item | minor |
| Add an enum variant to a non-`#[non_exhaustive]` enum | major |
| Add an enum variant to a `#[non_exhaustive]` enum | minor |
| Add a method to a public trait | major (downstream impls break) — unless trait is sealed |
| Add a default method body to a public trait | minor (sealed trait), still possibly major (unsealed) |
| Raise MSRV | usually major; at minimum minor with prominent CHANGELOG note |
| Remove or rename anything `pub` | major |
---
## ADR Triggers Specific to Rust
- **Async runtime selection.** Tokio is the default; record an explicit ADR if you pick `async-std`, `smol`, `glommio`, or a custom executor. Cost: ecosystem fragmentation.
- **Allocator switch.** `jemalloc` / `mimalloc` / `tikv-jemallocator` vs `system` malloc. Record measured impact.
- **DB layer choice.** `sqlx` (compile-time SQL check, async-native) vs `sea-orm` (active-record-ish) vs `diesel` (sync, mature, macro-heavy). Each has long-term ramifications for query style, tooling, and CI.
- **HTTP framework.** `axum` (Tower-based, current default) vs `actix-web` (mature, separate runtime model) vs `poem` / `rocket`. Affects extractors, middleware, and team ramp.
- **Async-trait strategy.** Native AFIT (1.75+) vs `#[async_trait]` crate. Required when traits must be `dyn Trait`-safe.
- **Workspace shape.** Flat vs layered vs feature-sliced. Record the rule (e.g., "domain depends on nothing").
- **MSRV policy.** "Stable - 6 months" vs "latest stable" vs "pin to LTS". Affects which language features the team may adopt.
- **Edition migration timing.** When to flip from 2021 → 2024 globally; mixed-edition workspaces are supported but increase reasoning cost.
- **`unsafe` policy.** "No `unsafe` outside the `ffi/` module" vs "any `unsafe` requires two reviewers + `# Safety` doc". Record + enforce via lint or CODEOWNERS.
- **Error strategy.** `thiserror` (library) vs `anyhow` (binary) vs custom typed enum vs `eyre` + custom report handler. Affects every layer.
- **Serialization strategy.** `serde` (de facto) vs `bincode` (binary perf) vs Cap'n Proto / Protobuf for cross-language. Document why.
- **Public API stability commitment.** SemVer strict vs unstable-pre-1.0 vs "0.x is breaking forever". Affects downstream upgrade cost.
---
## Architecture Anti-Patterns
| Anti-pattern | Why it hurts | Better path |
|--------------|--------------|-------------|
| **God workspace**: one crate, 100k LOC, all concerns inside | Compile times explode; PRs collide; module boundaries become advisory; downstream consumers must accept all features | Layered or feature-sliced split; `[workspace.dependencies]` to unify versions |
| **Feature-flag-as-architecture**: gating entire modules behind `#[cfg(feature = "x")]` to simulate separate crates | Combinatorial CI matrix; `cargo check --all-features` flaky; consumers confused about which features are mutually exclusive | Actual crate split |
| **`Arc<Mutex<T>>` everywhere as DI substitute** | Hides ownership design; mutex contention; deadlock risk; obscures who-owns-what | Channels / actors; per-task state; `dyn`-trait or generic for composition |
| **Re-export everything from `lib.rs`** | Downstream pins to internal structure; visibility is meaningless; refactor cost is downstream cost | Curated façade via `pub use`; `pub(crate)` for the rest |
| **Traits added "for testability" with one impl** | Indirection without benefit; doubles the codebase; obscures the actual call graph | Introduce the trait only when ≥ 2 impls exist (prod + fake) or a real polymorphism need emerges |
| **Mixed edition / mixed MSRV in workspace** | New language features unusable in shared code; CI must compile multiple toolchains | Unify edition + MSRV at the workspace level via `[workspace.package]` |
| **Implicit version drift across members** | Each member pins a different version of `serde`/`tokio`; `cargo tree --duplicates` lights up | `[workspace.dependencies]` |
| **`pub` types in private modules leaking through inference** | Downstream depends on items they can't name; refactors break inscrutably | Audit with `cargo public-api list`; tighten visibility |
