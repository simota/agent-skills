# Fuse Recipe — Synthesizing a New Product from Multiple Captured Sources

> `/nexus fuse` — reproduce the observable surfaces of **two or more existing products**, then **synthesize them into a single new product** — adopting selected elements from each source, merging overlapping ones, and adding net-new connective tissue — verified by a **dual oracle**: adopted elements by differential parity against their *source* baseline, merged/net-new elements by spec conformance, and the whole by a **coherence gate**.

Read this file before executing the `fuse` Recipe. Phase contracts, the Fusion Map, the dual-oracle rule, the coherence gate, and conflict resolution are defined here. The **per-source + fusion-level web research sweep** that grounds fidelity is specified in `reference/research-grounding.md`.

> **Relationship to `clone`.** `fuse` is the **multi-source synthesis extension** of `clone`. It reuses clone's entire capture + provenance + differential-parity machinery **per source** (§2 below points back to `clone-recipe.md`), and adds the three things clone cannot express because clone has exactly one baseline and reproduces it faithfully: (1) a **Fusion Map** that assigns every element of the *new* product a provenance and a resolution, (2) a **selective/dual oracle** (parity for adopted, spec for synthesized), and (3) a **coherence gate** that proves the result is one product, not a patchwork of two. Cloning one product → `clone`. Cloning N and welding them into one → `fuse`.

---

## 1. When to Use / Boundaries

Use `fuse` to **build a new product by combining the reproduced surfaces of two or more existing products** — e.g. "take Product A's editor and Product B's collaboration model and make one tool," "merge our two internal apps into a unified successor," "rebuild a competitor's data layer under our own product's UX." The defining trait: there are **≥2 capture baselines** and the deliverable is **intentionally not a faithful copy of any single one** — it is a *reconciliation* of them into a coherent whole.

`sources` ∈ {2..N} (designed for 2; generalizes to N — the Fusion Map and conflict ledger scale per pairwise/among-source overlap). Each source carries its own `target_type` ∈ { live-web | desktop | mobile | has-source | api } and is captured by clone's per-platform mechanism (§2).

| Not this | Route to | Why |
|----------|----------|-----|
| Faithful reproduction of **one** product | `clone` | Single baseline, fidelity *is* the goal — no synthesis, no Fusion Map |
| Net-new product merely **inspired by** references (no reproduced surface) | `feature` / `apex` | No capture baselines to reconcile; design is original, not adopted-and-merged |
| Merge/upgrade across **your own** codebase (consolidate two of your repos) | `migrate` (`case=arch`) | White-box, own-system completeness — no external surface to capture/parity |
| Cross-language rewrite of your own source | `transmute` | One white-box oracle from source, not multi-source observed reconciliation |
| Combine two **designs** in Figma (no full product rebuild) | `frame` + `vision` | Single-stage design composition, no capture/parity/coherence loop |
| Decide *which* features the fused product should have (verdict only, no build) | `essential` / `killer` / `spec` | Verdict/spec discovery; `fuse` is build+verify. Pair `spec`→`fuse` for discovery-then-synthesis |

**Three non-negotiable principles** (the first two inherited from `clone`, the third is the synthesis core):
1. **Reproduce from evidence, not memory.** Every adopted screen/flow/behavior is grounded in a **captured artifact** from its source (clone §1). The Fusion Map may not assign provenance to a source element that was never captured.
2. **Selective fidelity, explicit synthesis.** An element **adopted** from a source is held to that source's baseline by differential parity (clone discipline). An element **merged or invented** has **no baseline** and is held to a spec + acceptance criteria instead (feature discipline). The two oracles are never confused: a "blend" may not skip parity by *claiming* it is adopted, and an adopted-as-is element may not skip parity by *claiming* it is a blend.
3. **One product, not a Frankenstein.** The synthesis is proven **coherent** — one visual language, one interaction grammar, one terminology, one reconciled data model — by the Coherence Gate (§3c). A working but stylistically/conceptually fractured weld of two products is a *failed* fuse, not a partial success.

Scale: 12–32 agents (two-or-more capture branches + a reconciliation/coherence layer on top of clone's footprint), high cost. **Confirm before launch** when `strategy = big-bang full fusion` OR `sources ≥ 3`.

---

## 2. Source Capture (per source — reuses `clone`)

Capture is **clone's Phase 0.5 + Phase 1, run once per source**, producing one stamped baseline per source. Do not re-derive it here — apply `clone-recipe.md` §2 (Capture Strategy), §2a (Capture Robustness), §3b (Provenance & Drift), **and the Phase 0.5 research sweep (`reference/research-grounding.md`)** **independently for each source**, then carry all baselines forward into the Fusion Map.

- **Per-source research sweep** — each source gets its own web Evidence Ledger (`reference/research-grounding.md`), **scoped to the slice it contributes** to the fusion, so each adopted slice's completeness denominator + exact values are research-grounded. Plus **one fusion-level** competitive/positioning sweep (`+Compete`) that informs the **Fusion Thesis** (Phase 0) and the **Conflict Ledger** rationale (§3a) — knowing *why* each product designed a contested element the way it did sharpens the reconciliation decision.

- **Per-source capture strategy** — each source picks its own clone strategy (`extract-and-rebuild` default | `scaffold-from-source` if you own/license it | `incremental` | …) and its own capture-source binding by `target_type` (web=Vector/Voyager, desktop=Wield/external harness, has-source=Lens, api=Schema, …).
- **Per-source provenance stamp** (clone §3b) — every source baseline is stamped with *its* target version/build, capture date, environment, locale, pinned account/seed. The Fusion Report (§8) lists **one stamp per source**; a source baseline without a stamp is rejected at the Phase 2 gate exactly as in clone.
- **Per-source coverage** — clone's Capture Completeness Gate (clone §3a) applies per source *for the surface area that source contributes to the fusion*. You need not capture all of Product B if only B's billing flow is being adopted — but you must capture **every screen/state/flow of B's billing flow** (coverage gate scoped to the adopted slice), and the Fusion Map must declare that scoping so the un-captured remainder of B is an explicit, named non-goal, never a silent omission.
- **Drift** — clone's drift re-check (clone §3b) runs per source before SHIP; a source that shipped a new version mid-fusion re-stamps and re-captures *its adopted slice*, never re-tunes the fused product toward a moved source.

> The capture layer is platform-agnostic and mixed-platform: Product A may be `live-web` and Product B `desktop`. Each is captured by its own mechanism into a common Fusion Map; the synthesized product targets one chosen stack (declared at Phase 0).

---

## 3. Phase Contract (AUTORUN chain template)

```
Phase 0 FRAMING        Nexus internal: enumerate sources (A, B, …) + each target_type; declare the target stack of the
                       NEW product; record the FUSION THESIS (one line: what new product emerges, and why these sources);
                       per-source provenance stamps (§2) + robustness obstacles (clone §2a).
                       Big-bang full fusion OR sources ≥ 3 → confirm with user.
Phase 1 CAPTURE     ∥  Per source, run clone Phase 0.5 RESEARCH SWEEP (deep-research → per-source Evidence Ledger,
                       reference/research-grounding.md) → then clone Phase 1 (Vector/Voyager | Wield | Frame/Pixel |
                       Lens? | Schema? | Echo/Trace? | PDM/Lens feature-inventory | Ink/Pixel? asset-extract) → one
                       stamped baseline per source. Branches are hub-spoke, no shared mutable state. Scope each source's
                       research + coverage to the slice it contributes (§2), and capture that slice completely (clone §3a).
                       +1 fusion-level Compete sweep → informs the Fusion Thesis + Conflict Ledger rationale.
Phase 2 FUSION MAP  →  Spark[synthesis ideation vs the Fusion Thesis] → Magi[conflict arbitration]
   + SPEC               Build the FUSION MAP (§3a): decompose every source into elements; assign each element of the
                        NEW product a provenance {adopt-A | adopt-B | merge | net-new | drop} + resolution rationale
                        + ORACLE {parity-vs-A | parity-vs-B | spec-AC}. Resolve every A/B conflict → Conflict Ledger.
                        Accord/Scribe[author the synthesis spec + L3 ACs for every merge/net-new element].
                        → FUSION MAP GATE (§3a) + SELECTIVE-ORACLE GATE (§3b) + COHERENCE CONTRACT draft (§3c)
                        + IP / TRADE-DRESS GATE (§3d)
Phase 3 ARCHITECT      Magi[fusion strategy + gate] → Atlas[unified architecture that hosts both heritages]
                       Muse[reconcile A's + B's design tokens into ONE token system] → Schema?[reconcile data models
                       into one] → Gateway?[reconcile API contracts] → confirm the Verification Map (§4) per element
Phase 4 BUILD          adopted elements → Pixel/Forge→Artisan/Builder[reproduce against that source's baseline — clone
                       discipline] ‖ merged/net-new → Forge→Artisan/Builder[build to spec + ACs — feature discipline]
                       +flow?[reconcile motion] +polyglot?[reconcile locales]
                       rally[engine COMPETE] for fidelity-critical adopted screens AND for hard merges
Phase 5 DUAL VERIFY ∥  (a) SELECTIVE PARITY — each adopted element diffed vs its SOURCE baseline (clone §3c engine,
                          canonicalized): Pixel/Voyager visual, Radar/Voyager behavioral, Pixel/Frame asset
                       (b) SPEC CONFORMANCE — each merged/net-new element vs its L3 ACs: Attest (no baseline parity)
                       (c) COHERENCE GATE (§3c) — one visual language ∧ one interaction grammar ∧ one terminology
                          ∧ one reconciled data model: Echo/Palette[interaction+terminology coherence],
                          Pixel/Frame[visual coherence vs the unified token system], Atlas/Schema[data coherence]
                       (d) judge[SYNTHESIS review: coherent new product vs patchwork weld? provenance honored?]
                       → DRIFT RE-CHECK per source (clone §3b); FUSION-MAP COVERAGE re-check (every element verified
                         by its assigned oracle — no adopted element skipped parity, no net-new skipped ACs)
                       → loop to Phase 4 on any failing element/dimension (loop ≤ 3 cycles (default 3))
Phase 6 SHIP           Guardian[PR + FUSION REPORT: per-source provenance + per-element provenance/oracle/result
                       + Conflict Ledger resolutions + coherence verdict + IP posture + incremental scope]
```

**Parallelism:** Phase 1 source-capture branches and Phase 5 verifiers run concurrently (hub-spoke, no shared mutable state). Phase 4 elements parallelize under `isolation: worktree` when the build splits into independent screens/flows.

**Checkpoint-resume:** ≥4 phases → persist each source's Phase 1 baseline, the Phase 2 Fusion Map, and per-element Phase 4 outputs at boundaries so an interrupted run resumes from the last completed element.

### 3a. Fusion Map Gate (Phase 2 — the synthesis backbone)

The Fusion Map is the core artifact of this recipe — it is to `fuse` what the Parity Baseline is to `clone`. It decomposes every source into elements and assigns each element of the **new** product a provenance, a resolution rationale, and an **oracle**. Without it, "synthesize A and B" has no contract and parity has no per-element target.

**Schema** (one row per element of the new product — across the dimensions of §4):

| Field | Meaning |
|-------|---------|
| `element` | A screen / feature / behavior / data-entity / asset of the **new** product |
| `source_A_form` | How A renders/implements it (or `—` if A lacks it), grounded in A's baseline |
| `source_B_form` | How B renders/implements it (or `—` if B lacks it), grounded in B's baseline |
| `resolution` | `adopt-A` \| `adopt-B` \| `merge` \| `net-new` \| `drop` |
| `rationale` | *Why* this resolution — tied to the Fusion Thesis; mandatory for every `merge`/`drop` and every resolved conflict |
| `oracle` | `parity-vs-A` \| `parity-vs-B` \| `spec-AC` — **derived from resolution** (adopt-X ⟹ parity-vs-X; merge/net-new ⟹ spec-AC; drop ⟹ none) |
| `conflict?` | `true` when A and B both have the element in incompatible forms → must appear in the Conflict Ledger with its resolution |

**Two gates Phase 2 must clear before Phase 5 may trust the map:**

- **Completeness gate** — every element of the *new* product appears in the Fusion Map with a non-empty `resolution` and `oracle`; and every *captured source element* is accounted for as adopted, merged, or explicitly `drop`ped (with rationale). No orphan source elements ("captured but never decided") and no orphan new elements ("built but not on the map"). A `drop` is a first-class, *recorded* decision — silently leaving a source feature out is a coverage failure, not a synthesis choice.
- **Conflict-resolution gate** — every `conflict? = true` row has a recorded resolution + rationale in the **Conflict Ledger**. Conflicts are the substance of fusion: two navigation models, two data schemas for "the same" entity, two auth flows, two terminologies. Magi arbitrates each against the Fusion Thesis; an unresolved conflict blocks Phase 3 (you cannot build a coherent product over an undecided conflict).

### 3b. Selective-Oracle Gate (the dual oracle — fuse's signature departure from clone)

The shared differential-parity kernel — parity-over-faith, oracle adequacy + non-determinism canonicalization, comparator/harness, provenance/drift — is owned by `_common/DIFFERENTIAL_PARITY.md` (and applied per source via clone §3a–§3c, §2). fuse's specialization is the **selective/dual oracle**: per-element, the oracle is assigned by the Fusion Map. `clone` has one oracle: parity vs the single baseline. `fuse` has **two, assigned per element by the Fusion Map**, and the integrity of the whole recipe depends on never confusing them:

- **Adopted element (`adopt-A`/`adopt-B`) → differential parity vs that source's baseline.** Held to clone's §3c engine *against the source it came from*: visual SSIM/pixel-delta, behavioral fixtures, asset perceptual-hash — all canonicalized (clone §3c non-determinism rules). An adopted element that "looks about right" but was never diffed against its source baseline is unverified — exactly the false-fidelity clone guards against.
- **Merged / net-new element (`merge`/`net-new`) → spec conformance vs L3 ACs.** Has **no single baseline** (it is a deliberate blend or invention), so differential parity is *meaningless* — demanding byte-parity here spuriously fails every synthesis. Held instead to Accord's L3 acceptance criteria via Attest (feature discipline). The merge *may* inherit partial constraints from both sources (e.g. "preserve A's keyboard shortcuts AND B's data export schema") — those become testable ACs, not a parity diff.

**Gate:** every Fusion Map row is verified by **the oracle its resolution dictates** — no `adopt-*` row downgraded to spec-AC to dodge a hard parity diff, no `merge`/`net-new` row failed by a parity diff it can't satisfy. Phase 5's Fusion-Map coverage re-check asserts this mapping held for every row. This is the single most common way a fuse run silently goes wrong: an adopted element relabeled "merge" to escape parity, or a genuine blend failed against a baseline that was never the right oracle.

### 3c. Coherence Gate (Phase 5 — proving it is *one* product)

The signature risk of fusion is the **Frankenstein product**: every individual element passes its own oracle, yet the assembled whole is an incoherent patchwork — A's visual language beside B's, two button styles, two terminologies for the same concept, two mental models. clone never faces this (one source ⟹ inherent coherence); `fuse` must *prove* coherence as a first-class gate, because per-element verification cannot detect a whole-product seam.

Four coherence dimensions, each independently gated:

| Coherence dimension | What "coherent" means | Verified by |
|---------------------|------------------------|-------------|
| **Visual** | One reconciled token system (color/type/spacing/components) across all screens — not A-tokens on adopted-A screens beside B-tokens on adopted-B screens | Pixel/Frame vs the Phase 3 unified token system |
| **Interaction** | One navigation grammar, one validation/feedback pattern, one gesture/shortcut vocabulary — adopted flows are *re-grammared* into the unified model, not pasted in raw | Echo/Palette cognitive walkthrough across cross-source flows |
| **Conceptual / terminology** | One mental model and one name per concept — not A's "workspace" next to B's "project" for the same entity; not two overlapping settings surfaces | Echo/Prose terminology audit + Magi concept-model check |
| **Data** | One reconciled schema — entities that A and B both model are unified (not duplicated), relationships consistent, no shadow second source-of-truth | Atlas/Schema schema-coherence review |

**Tension with selective parity (resolved explicitly).** Re-grammaring an adopted flow into the unified interaction model can *lower* its visual/behavioral parity score against its source baseline — that is **correct and expected**: where the Fusion Map says "adopt A's *capability* but under the unified grammar," the oracle for the *changed* aspects shifts from parity-vs-A to spec-AC, and only the *preserved* aspects stay under parity. The Fusion Map records this split per element (`adopt-A, grammar=unified`) so Phase 5 knows which aspects to parity-diff and which to AC-check — coherence never silently voids parity, and parity never blocks coherence; the Map adjudicates.

**Gate:** all four coherence dimensions pass, AND judge's synthesis review returns "coherent new product," before SHIP. A fuse where every element parity-passes but the coherence gate fails is **not shippable** — it is the exact failure this recipe exists to prevent.

### 3d. Provenance & IP / Trade-Dress Gate (multi-source attribution)

Combining the reproduced trade dress, assets, and distinctive UI of **two or more** products raises sharper IP and confusability questions than cloning one. Two controls:

- **Per-element attribution** — the Fusion Map's `resolution` doubles as an attribution ledger: every adopted element names the source it reproduces. The Fusion Report (§8) surfaces this so "what did we take from whom" is answerable per element, not hand-waved.
- **IP / trade-dress posture** — each adopted asset and each piece of distinctive trade dress carries a license/IP posture (reuse-if-licensed / faithful-recreation / **redesign-to-de-risk**), exactly as clone's Asset dimension but **across multiple rights-holders**. Merging two products' distinctive looks can produce a result confusable with — or derivative of — either; flag such rows for `redesign-to-de-risk` and record the posture. This is a **recorded posture, not legal advice** — surface it for human/legal sign-off, never silently reuse copyrighted trade dress from multiple sources.

**Gate:** every adopted asset/trade-dress element has a recorded IP posture; rows flagged `redesign-to-de-risk` are routed to a net-new/recreated treatment (their oracle flips to spec-AC) before SHIP.

---

## 4. Verification Map (extends clone's Parity Map with the oracle column)

Magi confirms the relevant dimensions in Phase 3; Phase 4 builds against them; Phase 5 verifies each **by the oracle the Fusion Map assigned**. The five dimensions are clone's, plus the per-element oracle split and the whole-product coherence row.

| Dimension | Adopted element oracle (parity-vs-source) | Merged/net-new oracle (spec-AC) | Whole-product (coherence) |
|-----------|-------------------------------------------|----------------------------------|---------------------------|
| **Visual** | Pixel/Voyager SSIM/pixel-delta vs source baseline (clone §3c) | Attest vs visual ACs | One unified token system (§3c) |
| **Behavioral** | Radar/Voyager fixtures vs source baseline, canonicalized | Attest vs behavioral ACs | One interaction grammar (§3c) |
| **Feature** | Attest: adopted feature present ∧ reachable ∧ parity-faithful | Attest: merged/net-new feature meets ACs | No duplicated/overlapping features |
| **Data / API** | Shape/contract diff vs source baseline | Attest vs reconciled-schema ACs | One reconciled schema (§3c) |
| **Asset** | Pixel/Frame perceptual-hash vs source manifest (+IP posture §3d) | Faithful recreation / net-new vs ACs | Consistent asset language |

> Build *idiomatically on the new product's chosen stack*. Adopted elements are faithful in **observable result** for the aspects the Fusion Map preserves — re-expressed in the target framework's idioms and re-grammared into the unified interaction model. Faithfulness is per-aspect, governed by the Fusion Map, not whole-element.

---

## 5. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Frankenstein product** (every element passes its own oracle; the whole is an incoherent patchwork) | Coherence Gate (§3c) — visual/interaction/conceptual/data coherence + judge synthesis review, gated before SHIP |
| **Oracle confusion** (adopted element relabeled "merge" to dodge parity; or net-new failed by a meaningless parity diff) | Selective-Oracle Gate (§3b) — oracle derived from resolution; Phase 5 coverage re-check asserts the mapping held per row |
| **Orphan element** (a source feature captured but never decided; a feature built but not on the map) | Fusion Map completeness gate (§3a) — every new element and every captured source element accounted for; `drop` is a recorded decision |
| **Unresolved conflict built over** (two nav models / two schemas welded without a decision) | Conflict-resolution gate (§3a) — every `conflict?` row resolved + rationale in the Conflict Ledger before Phase 3 |
| **Memory-based synthesis** (blended from impression, not captured artifacts) | Per-source clone Phase 1 capture is a mandatory entry condition (§2); the Fusion Map can't reference an un-captured element |
| **Thin per-source baseline** (adopted slice under-captured) | clone §3a coverage gate, scoped to each source's contributed slice (§2) |
| **Stale source** (a source shipped a new version mid-fusion) | clone §3b drift re-check per source; re-capture the adopted slice, never re-tune the fused product toward a moved source |
| **Coherence-vs-parity false conflict** (re-grammaring an adopted flow tanks its parity score and reads as a regression) | §3c explicit split — Fusion Map records preserved-aspects (parity) vs changed-aspects (spec-AC) per element |
| **Multi-source IP/trade-dress risk** (a result confusable with or derivative of either source) | IP / Trade-Dress Gate (§3d) — per-element attribution + posture; `redesign-to-de-risk` rows flipped to net-new before SHIP |
| **Silent feature loss in the merge** (an adopted feature dropped while welding) | Feature dimension Attest (§4) vs the Fusion Map's adopted set; drop must be an explicit `drop` row |

## 6. Add-ons

- `+Spec` (run `spec` first) — when *which* elements to take from each source is itself unsettled: `spec → fuse` (discovery-then-synthesis, mirroring `charter → enact`).
- `+Schema` / `+Gateway` — when fusing two data models / two API contracts into one reconciled schema/contract is load-bearing.
- `+Muse` / `+Vision` — heavy design-token reconciliation when A's and B's visual languages diverge sharply (Muse owns the unified token system; Vision directs the reconciled look).
- `+Flow` — when motion/interaction vocabularies must be reconciled, not just pasted.
- `+Polyglot` — when sources ship different locale sets that must be unified.
- `+Wield` / `+Snap` — desktop / native-mobile source capture (mixed-platform fusion).
- `+Sherpa` — decompose a large fusion into atomic per-element build steps.
- `+Siege` — when the fused product must meet a performance envelope drawn from either source.
- `+Sentinel` / `+Clause` — when the multi-source IP/trade-dress posture (§3d) needs a security/legal-surface pass before sign-off.

## 7. Decision Tree vs Neighbors

```
Building a product from EXISTING products' captured surfaces?
  NO  → faithful copy of ONE product? → clone
        net-new, only inspired by references (no captured surface)? → feature / apex
        consolidate YOUR OWN repos/systems? → migrate (case=arch)
        cross-language rewrite of your source? → transmute
        which-features verdict / spec only (no build)? → essential / killer / spec
  YES → exactly one source, fidelity is the goal? → clone
        ≥2 sources, synthesized into one new product (not a faithful copy of any)?
              → fuse   (decide which to take per element, resolve conflicts, prove coherence)
              unsure which elements to take from each? → spec → fuse
```

## 8. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus a **Fusion Report**:
- **Research Grounding** — per-source Evidence Ledger summary + the fusion-level positioning sweep that informed the Thesis/Conflict Ledger (`reference/research-grounding.md` §6).
- **Fusion Thesis** + the chosen target stack of the new product.
- **Per-source provenance stamps** (one per source: target version/build, capture date, environment/OS, app/browser version, locale, pinned account/seed) + capture mechanism per source + per-source drift status (no-drift / re-captured / deferred).
- **Fusion Map** — per-element `resolution` / `oracle` / `rationale`, including the preserved-vs-changed aspect split for re-grammared adopted elements (§3c).
- **Conflict Ledger** — every A/B (… /N) conflict and how it was resolved against the Thesis.
- **Selective-parity results** — per adopted element: visual SSIM/pixel-delta, behavioral pass rate, asset match vs *its source* baseline.
- **Spec-conformance results** — per merged/net-new element: AC coverage (Attest).
- **Coherence verdict** — visual / interaction / conceptual / data coherence results + judge synthesis verdict (coherent new product vs patchwork).
- **IP / trade-dress posture** — per-element attribution + posture (reuse-licensed / faithful-recreation / redesigned-to-de-risk).
- **Incremental scope** — which elements synthesized this PR, which remain; each increment re-stamped with the source versions it was verified against. For incremental fusion, each increment is a separate shippable PR carrying its own per-source stamps + accreted parity/AC regression harness.
