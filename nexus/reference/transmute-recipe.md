# Transmute Recipe — Cross-Language Rewrite

> `/nexus transmute` — rewrite a codebase/module from a source language to a target language **preserving externally observable behavior**, expressed **idiomatically** in the target language and **verified by differential parity** against a golden oracle extracted from the source.

Read this file before executing the `transmute` Recipe. Phase contracts, the Transmutation Map, strategy selection, and failure escalation are defined here.

---

## 1. When to Use / Boundaries

Use `transmute` for **language-pair crossings**: TS→Rust, Go→Rust, Python→Go, JS→TS, Java→Kotlin (cross-language semantics, not the same-runtime case), Ruby→Go, etc.

| Not this | Route to | Why |
|----------|----------|-----|
| Web → iOS/Android native | `PORTING` (Port→Native) | Platform paradigm shift, not arbitrary language pair |
| Same-language framework migration (Express→Fastify, Vue2→Vue3) | `migrate case=framework` (drives `shift`) | Language unchanged; needs completeness sweep not parity oracle |
| Arch / middleware / mock→prod sweep needing no-omission guarantee | `migrate` (case=arch/middleware/mock-to-prod) | Completeness via RESIDUE-GATE, no language crossing |
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
Phase 1 ARCHAEOLOGY ∥  Trail[extract implicit business rules + invariants]
                       Lens[map current structure, data flow, public surface]
                       Atlas?[architecture + module/dependency boundaries]   (if subsystem/whole)
                       Trail?[git history → why-decisions behind non-obvious code]  (optional)
                       → output: behavior contract draft, source-language-independent
Phase 2 CONTRACT       Scribe[unified: author language-NEUTRAL behavior spec + acceptance criteria]
                       → Radar[generate golden I/O fixtures from the SOURCE impl = differential oracle]
                       → ORACLE GATE: adequacy (covers source branches/error-paths/boundaries) + determinism contract (below)
Phase 3 STRATEGY       Magi[arbitrate big-bang|strangler-fig|FFI + RISK GATE]
                       → confirm Transmutation Map (type / error / concurrency / memory) for the pair
Phase 3.5 PILOT        Transmute ONE small representative module end-to-end (Phase 4 + Phase 5 in full)
                       before scaling out. Every pilot failure amends the Transmutation Map (§4),
                       not just the piloted files.
                       GATE: pilot module reaches parity with no un-mapped idiom → scale out.
Phase 4 TRANSMUTE      Builder/Artisan[idiomatic target-language implementation]
                       +builder?[parser/DSL-heavy modules]  +gateway?/schema?[API/DB boundaries]
                       rally[engine-paradigm COMPETE] for high-risk modules → 2-3 idiomatic variants, pick best
                       Parity failure traced to a mapping rule → amend the Transmutation Map and
                       regenerate the module; do not hand-patch the emitted code (§4)
Phase 5 PARITY VERIFY ∥ Radar[differential + property tests against Phase 2 oracle; multi-lang incl. Rust]
                       Attest[conformance vs Scribe[unified] contract]
                       judge[IDIOM review: idiomatic target-lang vs transliterated?]
                       Voyager?[E2E parity]  (if app-level)
Phase 6 SHIP           Guardian[PR with Before/After parity report + strangler increment scoping]
```

**Parallelism:** Phase 1 branches run concurrently (hub-spoke, no shared mutable state). Phase 5 verifiers run concurrently. Phase 4 modules may parallelize under `isolation: worktree` when a strangler-fig splits the rewrite into independent modules.

**Checkpoint-resume:** ≥4 phases → persist Phase 1 contract, Phase 2 oracle, and per-module Phase 4 outputs at boundaries so an interrupted run resumes from the last completed module.

### 3a. Oracle Adequacy & Determinism Gate (Phase 2 — the integrity backbone of "parity over faith")

The shared kernel — parity-over-faith, the oracle-adequacy and non-determinism-canonicalization gates, the comparator/harness discipline, and the "spuriously fails / masks real divergence" failure pair — is owned by `_common/DIFFERENTIAL_PARITY.md` (§1–§4). transmute's specialization is the **extracted oracle** (golden I/O fixtures generated from the source impl). Phase 2 must clear two gates before Phase 5 may trust the oracle:

- **Adequacy gate** — the golden corpus must exercise the **source's branches, error paths, and boundary classes**, not just the happy path. Capture the source's code coverage while generating fixtures (run the source under coverage as Radar produces inputs); require the differential corpus to hit the same branches + every `throw`/`error`/`panic` path + each boundary/equivalence class. If coverage falls short, **expand the corpus before Phase 5**. Record the achieved source-coverage % in the Parity Report.
- **Determinism contract** — for the extracted oracle, the source's **incidental non-determinism** (hash/map iteration order — Go map randomized, Rust `HashMap` randomized, Python dict insertion-ordered — timestamps, float ULP differences, locale, RNG, concurrency interleaving) must be canonicalized per the common gate. For each output, declare which aspects are **semantically significant vs incidental**; **canonicalize the incidental aspects on both sides** before comparing (sort order-incidental collections, pin seeds, round floats to a declared tolerance, freeze clock/locale). Phase 5 Radar compares against the canonicalized form.

**Gate:** Phase 5 differential verification runs against an oracle that has passed both gates. An oracle that is happy-path-only OR compares raw non-deterministic output is rejected — fix it in Phase 2, do not proceed to trust it.

---

## 4. Transmutation Map

The core knowledge of this recipe — and its rulebook. Magi confirms the relevant table in Phase 3; the Phase 3.5 pilot amends it before scale-out; Builder applies it in Phase 4 and amends it again whenever a parity failure traces to a mapping rule rather than to one module; judge audits adherence in Phase 5. The map, not the emitted code, is what gets fixed.

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

## 4a. Termination Bound

**`N/A` for a convergence loop** — `transmute` terminates on its **differential-parity oracle** (`_common/DIFFERENTIAL_PARITY.md`): the rewrite is done when the comparator reports zero semantic divergence against the stamped baseline across the agreed corpus. Parity failures return to the per-module fix step; they do not iterate a rubric. A divergence that cannot be closed exits `BLOCK` with the residual divergence set reported, never silently accepted.

## 5. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Transliteration ("Go-in-Rust") | `judge` idiom review (Phase 5) blocks; `rally engine-paradigm` COMPETE surfaces idiomatic alternatives |
| Behavior regression | Radar golden oracle (Phase 2) + Radar differential/property tests (Phase 5) |
| **Thin oracle → false parity** (target diverges on an untested branch yet passes) | Phase 2 adequacy gate: corpus must cover source branches / error paths / boundaries; expand if source-coverage short before Phase 5 trusts it |
| **Spurious parity failure on incidental non-determinism** (map order, timestamps, float ULP, locale, RNG) | Phase 2 determinism contract: declare significant-vs-incidental per output, canonicalize incidental aspects on both sides before comparing, pin seeds/clock |
| **Mapping error found only at full scale** — every module carries the same bad idiom translation | Phase 3.5 PILOT: one module through Phase 4+5 in full before scale-out; failures amend the Transmutation Map |
| **Hand-patched output** — emitted code fixed per file, so the flawed mapping rule survives into later modules | Amend the Transmutation Map and regenerate (Phase 4); fix the rule, not the file |
| "Rewrite everything at once" risk blindness | Magi risk gate (Phase 3) prefers strangler-fig; big-bang needs user confirm |
| Source memory assumptions clash with target ownership | Phase 3 explicit lifetime/ownership design (esp. Go→Rust GC→borrow) |
| Concurrency semantics drift (race conditions, ordering) | Concurrency axis in Transmutation Map + property tests on concurrent paths |
| Dependency with no target-language equivalent | Phase 3 flags it; resolve (alternative crate / vendored port / FFI to original) before Phase 4 |
| FFI boundary unsafety | Restrict `unsafe`/marshalling to the seam; Sentinel add-on for the boundary |

## 6. Add-ons

- `+Sentinel` — audit FFI boundary / `unsafe` blocks for memory & injection safety.
- `+Siege` — load/throughput parity when the rewrite's motivation is performance.
- `+Schema` — when persistence layer or serialization format crosses the boundary.
- `+Scout` — deeper root-cause archaeology when Trail+Lens leave behavior gaps.
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

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus a **Parity Report**: golden-oracle test count + pass rate, **oracle adequacy (source-coverage % the corpus achieved: branches / error-paths / boundary classes)**, **determinism contract (which output aspects were canonicalized vs compared raw)**, differential-test diff summary (must be empty for SHIP), idiom-review verdict, and strangler increment scope (which modules migrated this PR, which remain). For strangler-fig runs, each increment is a separate revertible PR.
