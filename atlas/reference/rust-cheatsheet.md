# Rust Architecture Cheatsheet (Edition 2024 / 1.85+)

Purpose: Atlas-flavored slice of the Rust knowledge base — workspace architecture patterns, trait-based DI, visibility hygiene, circular-dep detection, public-API surface management, and ADR triggers specific to Rust.

Baseline: **Rust 1.85+, Edition 2024, resolver = "3"**.

Source of truth (do not duplicate here):
- Project structure & cargo workspaces → [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md) §3
- Domain architecture patterns → [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md) §10
- Trait design pitfalls → [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) §7
- API design pitfalls → [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) §13

---

## Contents

- [Workspace Architecture Patterns](#workspace-architecture-patterns)
- [Trait-Based DI: Generic vs `dyn`](#trait-based-di-generic-vs-dyn)
- [Module Visibility Hygiene](#module-visibility-hygiene)
- [Circular Dependency Detection](#circular-dependency-detection)
- [God-Crate Split Signals](#god-crate-split-signals)
- [Workspace `Cargo.toml` Patterns](#workspace-cargotoml-patterns)
- [Public API Surface Management](#public-api-surface-management)
- [Refactoring Playbooks](#refactoring-playbooks)
- [ADR Triggers Specific to Rust](#adr-triggers-specific-to-rust)
- [Architecture Anti-Patterns](#architecture-anti-patterns)

---

## Workspace Architecture Patterns

Three production patterns. Pick one per system; mixing causes layering chaos.

### Layered (Clean / Hexagonal)

Crates organized by architectural layer; dependencies flow one direction only.

```
workspace/
├── Cargo.toml                 # [workspace] root
├── crates/
│   ├── domain/                # Pure types + traits, no I/O
│   │   └── src/lib.rs         # User, Order, OrderRepo (trait), ...
│   ├── application/           # Use-cases composing domain + ports
│   │   └── src/lib.rs         # CreateOrderUseCase, ...
│   ├── adapter-postgres/      # Implements domain traits via sqlx
│   ├── adapter-http/          # Axum routes -> calls application
│   └── bin-api/               # Thin main: wires adapters into application
```

Dependency rule (enforced at workspace level):

```
bin-api ──> adapter-http ──> application ──> domain
            adapter-postgres ──> application ──> domain
```

`domain` depends on **nothing inside the workspace**. Verify with `cargo tree -p domain --workspace`.

### Feature-Sliced (Bounded Contexts)

Top-level crates per bounded context; each crate may itself follow hex/clean internally.

```
workspace/
├── crates/
│   ├── billing/        # has its own domain/application/adapter modules inside
│   ├── catalog/
│   ├── identity/
│   └── shared-kernel/  # cross-context primitives (Money, UserId)
```

Cross-context dependencies go via `shared-kernel` only. No `billing → catalog` direct edges.

### Bin + Lib

Smallest pattern. Library crate exposes API; `bin/` directory holds entry points.

```
my-tool/
├── Cargo.toml
└── src/
    ├── lib.rs         # public API
    └── bin/
        ├── tool.rs    # main CLI
        └── admin.rs   # admin CLI
```

Use when:
- Project is one bounded context.
- Library is reusable as a dependency.
- ≤ ~20k LOC; growth past that should trigger a Layered split.

---

## Trait-Based DI: Generic vs `dyn`

Two ways to inject a dependency through a trait. Choose deliberately.

### Generic parameter (`<R: OrderRepo>`)

```rust
pub struct CreateOrderUseCase<R: OrderRepo> {
    repo: R,
}

impl<R: OrderRepo> CreateOrderUseCase<R> {
    pub fn run(&self, cmd: NewOrder) -> Result<Order, AppError> { /* ... */ }
}
```

- **Compile-time monomorphized**. Each `R` produces a separate optimized function.
- **Zero indirection** — calls inline; perf is identical to direct call.
- **Cost**: binary-size growth (one copy per `R`), slower compile, error messages mention concrete types.
- **Use when**: hot path, the impl is known at the call site, you need `R::AssociatedType` to vary.

### Trait object (`Arc<dyn OrderRepo>`)

```rust
pub struct CreateOrderUseCase {
    repo: Arc<dyn OrderRepo + Send + Sync>,
}

impl CreateOrderUseCase {
    pub fn run(&self, cmd: NewOrder) -> Result<Order, AppError> { /* ... */ }
}
```

- **Runtime dispatch** via vtable.
- **One function body** regardless of how many impls exist — smaller binary, faster compile.
- **Cost**: vtable lookup per call (~ns-scale), `dyn`-safe trait constraints (no generic methods, no `Self: Sized`).
- **Use when**: composition root with N impls, plugin systems, swap-impl-at-runtime, less perf-critical layers.

### Decision matrix

| Scenario | Choose |
|----------|--------|
| 1 impl in prod, 1 fake in tests | Either works; `dyn` is fewer angle brackets |
| Hot path (>100k calls/sec) | Generic |
| Trait needs async fn (AFIT 1.75+) | Generic (AFIT trait isn't `dyn`-safe without `async-trait` shim) |
| Plugin registry (`HashMap<&str, Box<dyn Trait>>`) | `dyn` (only option) |
| Trait has `fn foo<T>(&self, x: T)` | `dyn` is impossible — must be generic |
| Cross-crate, library exposes the trait | Provide both; consumer chooses |

For full guidance, see best-practices §10 (Domain architecture) and anti-patterns §7 (Trait Design).

---

## Module Visibility Hygiene

Rust gives you a five-rung visibility ladder. Use the tightest that compiles.

| Modifier | Reachable from |
|----------|----------------|
| (none, default) | Same module only |
| `pub(self)` | Same module (explicit form of default) |
| `pub(super)` | Parent module |
| `pub(in path::to::mod)` | Within the named path |
| `pub(crate)` | Entire crate |
| `pub` | Public API — anyone who depends on this crate |

### Façade pattern with `pub use`

```rust
// crates/billing/src/lib.rs
mod domain;        // private modules
mod application;
mod adapter;

// Curated public surface — change at will, internals stay private
pub use application::{Charge, ChargeError, Subscription};
pub use domain::{Money, Currency};
// Note: adapter is NOT re-exported — internal only.
```

Downstream code imports `billing::Charge` without coupling to the internal `application` module path.

### Sealed trait pattern (prevent downstream impls)

```rust
mod private { pub trait Sealed {} }

pub trait Renderer: private::Sealed {
    fn render(&self, doc: &Doc) -> Output;
}

// Only YOU can add new impls — downstream cannot extend the trait set.
impl private::Sealed for SvgRenderer {}
impl Renderer for SvgRenderer { /* ... */ }
```

Use sealed traits when:
- You want forward-compat freedom to add methods (no breaking-change risk from downstream impls).
- The trait represents a closed enumeration of behaviors (Rust API Guidelines C-SEALED).

### Visibility audit signal

If `cargo public-api list` shows items you didn't mean to expose, tighten visibility before the next release. See [Public API Surface Management](#public-api-surface-management).

---

## Circular Dependency Detection

Rust does **not** allow circular crate dependencies at compile time, but circular module dependencies inside a crate AND logical circularity (A's trait, impl-in-B, B calls A) can still emerge.

### Tools

| Tool | Scope | Use For |
|------|-------|---------|
| `cargo-modules structure` | Per-crate module graph | Diagnose `mod` cycles, orphan modules, deep nesting |
| `cargo-depgraph` | Workspace-level crate graph | Visualize crate→crate edges, find unintended deps |
| `cargo tree --workspace` | Direct/transitive dep tree | Inspect what a crate actually pulls in |
| `cargo tree --duplicates` | Version conflicts across deps | Find unintended version splits (a sign of weak workspace mgmt) |
| `cargo-deny check bans` | Policy-driven dep audit | Enforce "no X depends on Y" rules in CI |

Example:

```bash
cargo install cargo-modules cargo-depgraph
cargo modules structure --package billing
cargo depgraph --workspace-only | dot -Tsvg > deps.svg
```

### Common circular smells in Rust

1. **`app → infra → app` via callback registration.** The infra layer calls back into application services through a registered closure or trait object. Fix: invert via a trait owned by `app`; `infra` implements it.

2. **Crate A re-exports types from Crate B, while Crate B uses traits defined in Crate A.** Compiles but creates an "if you import either, you import both" coupling. Fix: move the shared types into a `shared-kernel` / `common` crate.

3. **Module cycle inside a crate**: `mod a` uses items from `mod b` which uses items from `mod a`. Rust allows it within one crate but it muddies reasoning. Fix: extract shared items into a parent or sibling module.

4. **Test code reaching into prod code via `pub(crate)` shortcuts that grow into a backdoor.** Fix: keep a clean `pub(crate)` test API or use `#[cfg(test)] pub` only.

---

## God-Crate Split Signals

When a single crate becomes a kitchen sink, productivity collapses. Signals worth a split:

- **Compile time > 60s** for a clean incremental rebuild of one crate.
- **`[features]` table has > 8 entries** suggesting bundled concerns (each feature represents a hidden sub-crate).
- **Workspace contains exactly one crate** + `examples/` + `tests/` — the workspace is a fiction.
- **`lib.rs` re-exports everything** (`pub use crate::*;`) — there is no module boundary.
- **A single file > 2000 LOC** without natural sub-modules.
- **PRs from different teams routinely touch the same crate** — change ownership is unclear.
- **`cargo doc` for the crate takes > 30s** — it's documenting too many concerns at once.

Splitting playbook → see [Refactoring Playbooks](#refactoring-playbooks).

---

## Workspace `Cargo.toml` Patterns

### `[workspace.dependencies]` (1.64+)

Single source of truth for version + features:

```toml
# Cargo.toml (workspace root)
[workspace]
members = ["crates/*"]
resolver = "3"                  # Edition 2024 default

[workspace.package]
version      = "0.7.0"
edition      = "2024"
rust-version = "1.85"
authors      = ["Acme <eng@acme.example>"]
license      = "Apache-2.0"
repository   = "https://github.com/acme/widgets"

[workspace.dependencies]
serde   = { version = "1.0", features = ["derive"] }
tokio   = { version = "1", features = ["full"] }
anyhow  = "1"
thiserror = "1"

# Member crate:
# [package]
# name = "widgets-domain"
# version.workspace = true
# edition.workspace = true
# rust-version.workspace = true
#
# [dependencies]
# serde.workspace = true
# thiserror.workspace = true
```

### `[workspace.lints]` (1.74+)

Cross-crate lint configuration — one place to set lints for the whole workspace:

```toml
[workspace.lints.rust]
unsafe_code = "deny"
missing_docs = "warn"

[workspace.lints.clippy]
all = "warn"
pedantic = "warn"
unwrap_used = "warn"
expect_used = "warn"

# Member crate inherits via:
# [lints]
# workspace = true
```

### `resolver = "3"`

Edition 2024 default. Improves feature unification — prefers feature-isolation between dev-deps and normal deps. Set explicitly even on Edition 2021 workspaces that have been audited to be compatible.

For full toolchain detail → best-practices §4.

---

## Public API Surface Management

### `cargo-public-api`

Track every change to the public surface across releases:

```bash
cargo install cargo-public-api
cargo public-api list                       # current surface
cargo public-api diff v0.6.0..v0.7.0        # what changed
```

CI integration: fail the PR if the diff is non-empty without a version bump justification. Block accidental SemVer breakage.

### `cargo-semver-checks`

Detects breaking changes before release:

```bash
cargo install cargo-semver-checks
cargo semver-checks check-release           # against last published version
```

Catches things `cargo public-api` does not flag explicitly (e.g., struct field reorder for `#[repr(C)]`, `MSRV` raise).

### `#[non_exhaustive]` discipline

```rust
#[non_exhaustive]
pub enum AppError {
    NotFound,
    Conflict,
    // future variants here are NOT a breaking change for downstream `match`
}

#[non_exhaustive]
pub struct Config {
    pub host: String,
    pub port: u16,
    // future fields don't break struct literal init for our own internal code,
    // and downstream construction must use a builder.
}
```

Apply `#[non_exhaustive]` from day one on any public enum or struct that may grow. Removing it later is itself a breaking change.

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

## Refactoring Playbooks

### Strangler-Fig: replace legacy impl behind a feature flag

```toml
[features]
default = ["old-impl"]
old-impl = []
new-impl = []
```

```rust
#[cfg(feature = "new-impl")]
pub use crate::renderer::v2::SvgRenderer;

#[cfg(all(feature = "old-impl", not(feature = "new-impl")))]
pub use crate::renderer::v1::SvgRenderer;
```

Phases:
1. Ship `new-impl` opt-in.
2. Make `new-impl` the default; keep `old-impl` available.
3. Remove `old-impl` in the next major release.

### Branch by Abstraction

1. Introduce a trait abstracting the operation.
2. Both old impl and new impl satisfy the trait.
3. Inject via DI at the composition root.
4. Swap default impl. Old impl is now deletable.

### Crate Split Protocol

Splitting one crate into two (e.g., `widgets` → `widgets-core` + `widgets-cli`):

1. **Create the new crate**: `cargo new --lib crates/widgets-core`.
2. **Move modules** physically: `git mv crates/widgets/src/core.rs crates/widgets-core/src/lib.rs`.
3. **Update `[workspace] members`** in the root `Cargo.toml`.
4. **Add the new crate as a dependency** of the old one: `widgets/Cargo.toml` gets `widgets-core = { path = "../widgets-core" }`.
5. **Adjust visibility**: items that crossed the old module boundary as `pub(crate)` must now be `pub`. Add `#[non_exhaustive]` while you're at it.
6. **Re-export for source-compat** during transition: in old crate, `pub use widgets_core::*;`.
7. **Fix doc-tests** — paths in `///` examples change.
8. **Update CI** to test both crates.
9. **Verify**: `cargo build --workspace`, `cargo test --workspace`, `cargo public-api diff` on both.

### Inverting a Circular Dependency

```
Before:  app ─uses─> infra ─callback─> app   (circular)
After:   domain (defines trait T)
         app    ─uses─> domain
         infra  ─impls─> T (from domain)
         app    ─composes─> infra at startup
```

Steps:
1. Extract the trait into the lowest layer (`domain` or `shared-kernel`).
2. Move the impl to `infra`, depending only on `domain`.
3. Wire at `bin/`.
4. Delete the old direct edge from `infra` back to `app`.

---

## ADR Triggers Specific to Rust

Document the decision when one of these arises:

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

ADR format → use Scribe's `adr` recipe (Nygard or MADR). Atlas owns the architectural tradeoff analysis; Scribe authors the artifact.

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

For full anti-pattern catalog: [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) §7 (Trait Design) and §13 (API Design).

---

## Where to dig deeper

- Project structure & workspaces: [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md) §3
- Cargo & toolchain (2026 stack): [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md) §4
- Domain architecture patterns: [`builder/reference/rust-best-practices.md`](../../builder/reference/rust-best-practices.md) §10
- Trait design pitfalls: [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) §7
- API design pitfalls: [`builder/reference/rust-anti-patterns.md`](../../builder/reference/rust-anti-patterns.md) §13
- Edition 2024 language surface: [`builder/reference/rust-language-spec.md`](../../builder/reference/rust-language-spec.md)
