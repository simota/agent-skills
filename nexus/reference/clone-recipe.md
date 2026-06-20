# Clone Recipe — Faithful Product Reproduction

> `/nexus clone` — reproduce an existing product **completely and faithfully** by reverse-engineering its observable surface (UI / behavior / features / data shape), synthesizing a reconstruction spec, rebuilding it, and **verifying the copy against the original by differential parity** — not by assertion.

Read this file before executing the `clone` Recipe. Phase contracts, the Parity Map, capture-strategy selection, and failure escalation are defined here.

> **Naming note.** The Recipe subcommand `clone` (alias `replicate`) is distinct from the **`Trace` skill** (session-replay analysis) that this Recipe *spawns* in Phase 1. "Clone the product" = the Recipe; "Trace skill" = one capture tool inside it. Bare `trace` deliberately does **not** route to this Recipe (it reaches the Trace skill) — do not conflate them.

---

## 1. When to Use / Boundaries

Use `clone` to **reproduce a whole product (or a self-contained product area) faithfully** from its observable surface — a legacy product being rebuilt on a new stack, an authorized reference implementation, a design you own, or an internal app whose source is lost. The defining trait: the target is treated as a **black box (or grey box)** — fidelity is *measured* against the original, not assumed.

| Not this | Route to | Why |
|----------|----------|-----|
| Cross-language rewrite of **your own source** (TS→Rust) | `transmute` | White-box; parity oracle extracted *from* the source, not observed externally |
| Same-system arch / framework / middleware / mock→prod sweep | `migrate` | Change-completeness on an existing codebase, no external target to reproduce |
| Web → iOS/Android native reproduction | `PORTING` (Port→Native) | Platform paradigm shift, native parity rules |
| Pixel-accurate **single mockup/screenshot** → code | `pixel` (skill direct) | One image, no product-wide feature/behavior capture or parity loop |
| New product *inspired by* a reference (not a faithful copy) | `feature` / `apex` | Net-new design, no parity baseline to converge against |
| Extract design context from a Figma file | `frame` (skill direct) | Single-source design extraction, no full-product rebuild + verify |

**Two non-negotiable principles:**
1. **Reproduce from evidence, not memory.** Every reproduced screen, flow, and behavior is grounded in a **captured artifact** (screenshot, recorded interaction, observed API response). "Rebuild what I remember of it" is rejected — capture is the entry condition for the spec (Phase 1 → Phase 2 gate).
2. **Fidelity over faith.** The copy's match to the original is *proven* by diffing the rebuild against the Phase 2 parity baseline (visual / behavioral / feature / data), not asserted. A clone that "looks done" but was never diffed against the captured baseline is incomplete.

Scale: 8–22 agents (capture-heavy), mid-to-high cost. **Confirm before launch when strategy = big-bang full clone** (whole product in one cutover).

---

## 2. Capture Strategy (selected at Phase 3 gate)

| Strategy | When | Mechanism | Risk |
|----------|------|-----------|------|
| **extract-and-rebuild** (default) | Black box; no source access | Observe surface → neutral spec → rebuild from scratch on the target stack | Low–med — fidelity bounded by capture completeness |
| **scaffold-from-source** | Source available (grey/white box) | Fork structure + assets, re-express on the new stack, parity-verify the seams | Low — structure reused, but still diff-verified |
| **incremental-clone** (screen-by-screen) | Large product, live system | Reproduce one screen/flow at a time, each independently parity-gated | Low — each increment verifiable & shippable |
| **big-bang full clone** | Small/self-contained product | Whole reproduction, single cutover | High — **requires user confirmation** |

Capture-source bindings: **live web** = Vector/Voyager (crawl, screenshot, network observe) + Frame/Pixel (design extraction); **has Figma** = Frame (design context); **has source** = Lens (structure map); **mobile** = Snap/Voyager (native UI capture); **API-backed** = Schema (infer data model from observed responses).

---

## 3. Phase Contract (AUTORUN chain template)

```
Phase 0 FRAMING        Nexus internal: detect (target_type: live-web|has-source|mobile|api), scope (whole|area),
                       define what "complete copy" covers (visual ∧ behavioral ∧ feature ∧ data), capture feasibility.
                       Big-bang full clone → confirm with user.
Phase 1 CAPTURE     ∥  Vector/Voyager[crawl UI, capture per-screen screenshots, observe network/API traffic]
                       Frame/Pixel[extract design system: tokens, layout, components from screenshots/Figma]
                       Lens?[map current structure + public surface]            (if source available)
                       Schema?[infer data model + API contract from observed responses]  (if API-backed)
                       Echo/Trace?[walk the flows; session-replay behavior if logs exist]
                       PDM/Lens[enumerate the FULL feature inventory in scope]
                       → output: capture corpus (screenshots + flow recordings + API shapes + feature list)
Phase 2 SPEC+BASELINE  Scribe/Accord[author reconstruction spec from the capture corpus + acceptance criteria]
                       → establish the PARITY BASELINE = golden reference set (reference screenshots per screen/state,
                         recorded behavior fixtures, API contract, feature checklist) = the fidelity oracle
                       → CAPTURE COMPLETENESS GATE (§3a)
Phase 3 ARCHITECT      Magi[arbitrate capture strategy + CAPTURE GATE]
                       Atlas?[clone architecture + module boundaries]   Muse?[design tokens from extracted design]
                       → confirm Parity Map (visual / behavioral / feature / data) targets for this product
Phase 4 REBUILD        Forge→Artisan/Builder[reproduce screens + logic on the target stack]
                       Pixel[pixel-accurate reproduction from reference screenshots]
                       +gateway?/schema?[API/DB boundaries]   +flow?[animations/interactions]
                       rally[engine COMPETE] for high-fidelity-critical screens → variants, pick closest
Phase 5 PARITY VERIFY ∥ Pixel/Voyager[VISUAL parity: screenshot diff vs Phase 2 reference set, per screen/state]
                       Radar/Voyager[BEHAVIORAL parity: flow + state-transition + edge-case fixtures]
                       Attest[FEATURE parity: coverage vs the Phase 1 feature inventory]
                       judge[FIDELITY review: faithful copy vs approximate look-alike?]
                       → loop to Phase 4 on any dimension below its parity threshold (cap 3 cycles)
Phase 6 SHIP           Guardian[PR with Fidelity Report + per-screen parity scores + incremental scope]
```

**Parallelism:** Phase 1 capture branches and Phase 5 verifiers run concurrently (hub-spoke, no shared mutable state). Phase 4 screens may parallelize under `isolation: worktree` when incremental-clone splits the rebuild into independent screens/flows.

**Checkpoint-resume:** ≥4 phases → persist the Phase 1 capture corpus, Phase 2 parity baseline, and per-screen Phase 4 outputs at boundaries so an interrupted run resumes from the last completed screen.

### 3a. Capture Completeness Gate (Phase 2 — the integrity backbone of "fidelity over faith")

Parity is only as strong as the baseline. A green visual diff on three captured screens out of forty is *false confidence*, not a faithful copy. Phase 2 must clear two gates before Phase 5 may trust the baseline:

- **Coverage gate** — the capture corpus must cover **every screen, every reachable state (empty / loading / error / populated / auth'd-vs-anon), and every flow** in scope, not just the landing page and the happy path. Drive the live target through its navigation graph (Voyager) and enumerate states explicitly; require the parity baseline to hold a reference artifact for each. If a screen or state was never captured, it cannot be parity-verified — **expand the corpus before Phase 5**, or mark the gap as out-of-scope in the Fidelity Report (never silently omit it).
- **Fidelity-tolerance contract** — pixel-exact equality is the wrong bar for **incidental rendering variance**: anti-aliasing, font-hinting across platforms, dynamic/timestamped content, randomized feeds, A/B-varied layouts, animation mid-frames. For each dimension, declare what is **semantically significant vs incidental**, and set per-screen diff tolerances (mask dynamic regions, normalize fonts, freeze clock/seed, compare at a declared SSIM/pixel-delta threshold). Otherwise visual parity either **spuriously fails** on incidental variance or **masks real divergence** under a too-loose threshold.

**Gate:** Phase 5 parity verification runs against a baseline that has passed both gates. A baseline that is landing-page-only OR compares raw against dynamic content is rejected — fix it in Phase 2, do not proceed to trust it.

---

## 4. Parity Map

The core knowledge of this recipe. Magi confirms the relevant dimensions in Phase 3; Builder/Pixel reproduce against them in Phase 4; the Phase 5 verifiers audit each dimension independently.

| Dimension | What "faithful" means | Captured by (Phase 1) | Verified by (Phase 5) | Threshold (default) |
|-----------|----------------------|------------------------|------------------------|---------------------|
| **Visual** | Layout, spacing, color, typography, component look, responsive breakpoints match per screen/state | Vector/Voyager screenshots; Frame/Pixel design tokens | Pixel/Voyager screenshot diff (masked, normalized) | ≥ declared SSIM / ≤ pixel-delta per screen |
| **Behavioral** | Interactions, navigation, state transitions, validation, edge-case responses behave identically | Echo/Trace flow recordings; Voyager interaction traces | Radar/Voyager behavior fixtures | 100% of recorded flows green |
| **Feature** | Every feature in the inventory is present and reachable | PDM/Lens feature inventory | Attest coverage vs inventory | 100% covered or explicitly deferred |
| **Data / API** | Data model shape, API contract, and field semantics match the observed surface | Schema inference from observed responses | contract/shape diff (gateway/schema) | shape-equivalent; semantics spot-checked |

> Reproduce *idiomatically on the target stack* — a faithful copy is faithful in **observable result**, not in internal implementation. Re-expressing the original's UI in the target framework's idioms is correct; transliterating its internal code (when source exists) is not the goal — `judge` Phase 5 distinguishes faithful-result from cargo-cult-internals.

---

## 5. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Memory-based rebuild** (reproduced from impression, not artifacts) | Phase 1 capture corpus is a mandatory entry condition for Phase 2 |
| **Thin baseline → false fidelity** (3 screens captured, 40 exist) | Phase 2 coverage gate: corpus must hold an artifact per screen/state/flow; expand or explicitly defer before Phase 5 trusts it |
| **Spurious visual-diff failure on incidental variance** (AA, fonts, timestamps, A/B) | Phase 2 fidelity-tolerance contract: declare significant-vs-incidental, mask dynamic regions, normalize fonts, freeze clock/seed, compare at declared threshold |
| **Approximate look-alike accepted as a copy** | `judge` fidelity review (Phase 5) + per-dimension thresholds block "close enough" |
| **Happy-path-only behavior** (error/empty/loading states missing) | Phase 1 explicit state enumeration + Phase 2 coverage gate require every reachable state |
| **Feature drop-out** (a screen built, a feature silently lost) | Attest feature-parity coverage vs the Phase 1 inventory (Phase 5) |
| **"Reproduce everything at once" risk blindness** | Magi capture-strategy gate (Phase 3) prefers incremental-clone; big-bang needs user confirm |
| **Internal transliteration instead of idiomatic re-expression** | Parity Map "observable result, not internals" + judge review |

## 6. Add-ons

- `+Snap` — native iOS UI capture/verification when the target is a mobile app.
- `+Flow` — when motion/animation fidelity is part of "complete copy".
- `+Schema` / `+Tuner` — when the data layer and query behavior must be reproduced, not just the UI.
- `+Seek` — when search/ranking behavior is a reproduced feature.
- `+Sherpa` — decompose a large incremental-clone into atomic per-screen steps.
- `+Polyglot` — when the original ships multiple locales that must be reproduced.
- `+Siege` — load/throughput parity when the clone must match the original's performance envelope.

## 7. Decision Tree vs Neighbors

```
Reproducing an EXISTING product faithfully (parity-verified)?
  NO  → cross-language rewrite of your own source? → transmute | arch/framework/mock→prod sweep? → migrate
        | net-new design inspired by a reference? → feature/apex | single mockup→code? → pixel
  YES → target is mobile-native from a Web app? → PORTING (Port→Native)
        single Figma source, no full rebuild? → frame
        otherwise (whole product, fidelity-verified) → clone
```

## 8. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus a **Fidelity Report**: per-screen visual parity scores (SSIM/pixel-delta vs threshold), behavioral-fixture pass rate, **capture coverage (screens/states/flows captured vs enumerated, with any deferred gaps named)**, **fidelity-tolerance contract (which regions/aspects were masked vs compared raw)**, feature-parity coverage vs inventory, fidelity-review verdict, and incremental scope (which screens reproduced this PR, which remain). For incremental-clone runs, each increment is a separate shippable PR.
