# Transmute Recipe — Cross-Language Rewrite

> `/nexus transmute` — rewrite a codebase/module from a source language to a target language **preserving externally observable behavior**, expressed **idiomatically** in the target language and **verified by differential parity** against a golden oracle extracted from the source.

Read this file before executing the `transmute` Recipe. Phase contracts, the Transmutation Map, strategy selection, and failure escalation are defined here.

---

## 1. When to Use / Boundaries

Use `transmute` for **language-pair crossings**: TS→Rust, Go→Rust, Python→Go, JS→TS, Java→Kotlin (cross-language semantics, not the same-runtime case), Ruby→Go, etc.

| Not this | Route to | Why |
|----------|----------|-----|
| Web → iOS/Android native | `PORTING` (Port→Native) | Platform paradigm shift, not arbitrary language pair |
| Same-language framework migration (Express→Fastify, Vue2→Vue3) | `shift` | Language unchanged |
| Dependency / deprecated-API modernization | `shift detect`/`modernize` | No language crossing |
| Internal cleanup, same language | `refactor` / `kaizen` | No language crossing |
| Cross-platform prototype (RN/Flutter/KMP) | `forge` | Prototype, not behavior-preserving rewrite |

**Two non-negotiable principles:**
1. **Idiomatic re-expression, not transliteration.** Map source idioms to *target* idioms. A literal line-by-line port that "looks like Go written in Rust" is a defect — `judge` Phase 5 rejects it.
2. **Differential parity over faith.** Behavior equivalence is *proven* by running both implementations against the same golden I/O set (Phase 2 oracle), not asserted.

Scale: 8–20 agents, mid-to-high cost. **Confirm before launch when strategy = big-bang.**

---

## 2. Migration Strategy (selected at Phase 3 risk gate)

| Strategy | When | Mechanism | Risk |
|----------|------|-----------|------|
| **strangler-fig** (default) | Live system, module boundaries exist | Replace one module at a time; old + new coexist behind a seam | Low — each increment independently verifiable & revertible |
| **FFI-incremental** | Hot-path subset, or runtime must stay | New language exposed as native lib called from the old runtime | Medium — FFI boundary marshalling cost & safety |
| **big-bang** | Small/self-contained, or greenfield-equivalent | Whole rewrite, single cutover | High — **requires user confirmation** |

FFI boundaries by pair: **TS→Rust** = napi-rs / neon (Node Native Addon) or WASM; **Go→Rust** = cgo / `cdylib`; **Python→Rust** = PyO3 / maturin; **Python→Go** = gRPC sidecar or cgo-exported shared lib.

---

## 3. Phase Contract (AUTORUN chain template)

```
Phase 0 FRAMING        Nexus internal: detect (source_lang, target_lang), scope (module|subsystem|whole),
                       strategy candidate, parity-test feasibility. Big-bang → confirm with user.
Phase 1 ARCHAEOLOGY ∥  Fossil[extract implicit business rules + invariants]
                       Lens[map current structure, data flow, public surface]
                       Atlas?[architecture + module/dependency boundaries]   (if subsystem/whole)
                       Trail?[git history → why-decisions behind non-obvious code]  (optional)
                       → output: behavior contract draft, source-language-independent
Phase 2 CONTRACT       Accord[author language-NEUTRAL behavior spec + acceptance criteria]
                       → Mint[generate golden I/O fixtures from the SOURCE impl = differential oracle]
Phase 3 STRATEGY       Magi[arbitrate big-bang|strangler-fig|FFI + RISK GATE]
                       → confirm Transmutation Map (type / error / concurrency / memory) for the pair
Phase 4 TRANSMUTE      Builder/Artisan[idiomatic target-language implementation]
                       +grok?[parser/DSL-heavy modules]  +gateway?/schema?[API/DB boundaries]
                       rally[engine-paradigm COMPETE] for high-risk modules → 2-3 idiomatic variants, pick best
Phase 5 PARITY VERIFY ∥ Radar[differential + property tests against Phase 2 oracle; multi-lang incl. Rust]
                       Attest[conformance vs Accord contract]
                       judge[IDIOM review: idiomatic target-lang vs transliterated?]
                       Voyager?[E2E parity]  (if app-level)
Phase 6 SHIP           Guardian[PR with Before/After parity report + strangler increment scoping]
```

**Parallelism:** Phase 1 branches run concurrently (hub-spoke, no shared mutable state). Phase 5 verifiers run concurrently. Phase 4 modules may parallelize under `isolation: worktree` when a strangler-fig splits the rewrite into independent modules.

**Checkpoint-resume:** ≥4 phases → persist Phase 1 contract, Phase 2 oracle, and per-module Phase 4 outputs at boundaries so an interrupted run resumes from the last completed module.

---

## 4. Transmutation Map

The core knowledge of this recipe. Magi confirms the relevant table in Phase 3; Builder applies it in Phase 4; judge audits adherence in Phase 5.

### TS → Rust

| Source idiom | Target mapping |
|--------------|----------------|
| `Promise` / `async`/`await` | `tokio` runtime + `async`/`await` |
| structural typing | `trait` bounds + generics |
| discriminated / tagged union (`{kind: 'a'} \| {kind: 'b'}`) | **`enum` with data — the prime win; exhaustive `match`** |
| exceptions / `throw` | `Result<T, E>` + `?` |
| `null` / `undefined` | `Option<T>` |
| duck typing | trait objects (`dyn Trait`) or generic bounds |
| object spread / structural copy | `#[derive(Clone)]` + explicit clone (no implicit deep copy) |
| `any` | concrete type, `enum`, or `serde_json::Value` at boundaries only |
| npm dependency | crates.io equivalent (map per-dep; flag no-equivalent in Phase 3) |
| incremental boundary | **napi-rs / neon** native addon, or WASM; replace hot-path modules first |

### Go → Rust

| Source idiom | Target mapping |
|--------------|----------------|
| goroutine + channel | `tokio::spawn` + channel (`tokio::sync::mpsc`) — or `std::thread` + `crossbeam` for CPU-bound |
| `interface` | `trait` |
| `(val, err)` multi-return | `Result<T, E>` + `?` |
| **GC** | **ownership / borrow — the hard part; Magi must explicitly design lifetimes & ownership of shared state** |
| `defer` | `Drop` impl, or `scopeguard::defer!` |
| `nil` | `Option<T>` (and `Option<Box<T>>` for nil pointers) |
| struct embedding | composition + trait delegation |
| `panic` / `recover` | `panic!` + `std::panic::catch_unwind`, or prefer `Result` |
| `context.Context` cancellation | `tokio_util::sync::CancellationToken` or `select!` on a cancel channel |
| incremental boundary | cgo / `cdylib` shared lib |

### Python → Go

| Source idiom | Target mapping |
|--------------|----------------|
| duck typing | `interface` (smallest viable method set) |
| exceptions | `(val, error)` return + sentinel/wrapped errors |
| `None` | zero value + `ok` bool, or pointer + nil check |
| list/dict comprehension | explicit `for` + slice/map |
| GIL-bound threading | goroutines (true parallelism — re-examine shared-state assumptions) |
| dynamic attrs / `**kwargs` | explicit struct fields / functional options pattern |
| decorators | higher-order functions / middleware wrappers |
| incremental boundary | gRPC sidecar, or cgo-exported `c-shared` |

### JS → TS (intra-runtime, lower risk)

| Source idiom | Target mapping |
|--------------|----------------|
| implicit `any` | explicit types; `unknown` at boundaries, narrow before use |
| runtime duck checks | discriminated unions + type guards |
| JSDoc | real type annotations / `.d.ts` |
| CommonJS dynamic require | ES modules + typed imports |

> For pairs not tabled here, Magi derives the map from four axes in Phase 3: **type system, error handling, concurrency model, memory model**. Always populate those four before Phase 4.

---

## 5. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Transliteration ("Go-in-Rust") | `judge` idiom review (Phase 5) blocks; `rally engine-paradigm` COMPETE surfaces idiomatic alternatives |
| Behavior regression | Mint golden oracle (Phase 2) + Radar differential/property tests (Phase 5) |
| "Rewrite everything at once" risk blindness | Magi risk gate (Phase 3) prefers strangler-fig; big-bang needs user confirm |
| Source memory assumptions clash with target ownership | Phase 3 explicit lifetime/ownership design (esp. Go→Rust GC→borrow) |
| Concurrency semantics drift (race conditions, ordering) | Concurrency axis in Transmutation Map + property tests on concurrent paths |
| Dependency with no target-language equivalent | Phase 3 flags it; resolve (alternative crate / vendored port / FFI to original) before Phase 4 |
| FFI boundary unsafety | Restrict `unsafe`/marshalling to the seam; Sentinel add-on for the boundary |

## 6. Add-ons

- `+Sentinel` — audit FFI boundary / `unsafe` blocks for memory & injection safety.
- `+Siege` — load/throughput parity when the rewrite's motivation is performance.
- `+Schema` — when persistence layer or serialization format crosses the boundary.
- `+Scout` — deeper root-cause archaeology when Fossil+Lens leave behavior gaps.
- `+Sherpa` — decompose a large strangler-fig migration into atomic per-module steps.
- `+Shift[modernize]` — when the rewrite also modernizes deprecated APIs in the same pass (absorbed from horizon).

## 7. Decision Tree vs Neighbors

```
Crossing a language boundary?
  NO  → same-lang framework change? → shift framework  | dependency modernization? → shift detect/modernize | internal cleanup? → refactor/kaizen
  YES → target is mobile-native platform from a Web app? → PORTING (Port→Native)
        otherwise (arbitrary lang pair, behavior-preserving) → transmute
```

## 8. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus a **Parity Report**: golden-oracle test count + pass rate, differential-test diff summary (must be empty for SHIP), idiom-review verdict, and strangler increment scope (which modules migrated this PR, which remain). For strangler-fig runs, each increment is a separate revertible PR.
