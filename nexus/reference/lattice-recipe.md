# Lattice Recipe — Design-System Coherence Proof

> `/nexus lattice "<scope>"` — prove that every UI surface actually derives from the design system, with **zero unjustified deviation**, verified by an independent re-scan rather than by a counter. `rebrand` proves the completeness of a *brand change*; `lattice` proves the completeness of *system conformance* in steady state — the drift that accumulates with no brand change at all: the hardcoded hex, the magic `13px`, the fourth one-off button, the duplicate token that means the same thing.

Read this file before executing the `lattice` Recipe.

---

## 1. Nature / When to Use / Boundaries

**Design systems are built, then assumed.** `muse` defines tokens. `vitrine` catalogs components. `restyle` improves one surface. Nobody ever proves that the product *uses* the system — and system drift is silent by construction: every individual deviation is defensible in isolation, and the aggregate is a product that looks assembled by five teams.

Lattice's identity is four things no sibling carries together:

1. **Frozen denominator, proven residue.** Inherited verbatim from `migrate`/`rebrand`: enumerate the total surface *before* any edit, and establish completeness by an **independent re-scan finding zero**, never by the forward counter reaching M.
2. **Three-way deviation classification.** Every deviation is `residue` (a raw value with a token equivalent — the *surface* is wrong), `gap` (no token or component exists — the *system* is wrong), or `justified` (intentional, with a recorded reason and owner). Recipes that only detect "non-conforming values" force system gaps to be papered over with the nearest wrong token; the classification is what makes lattice fix the right thing.
3. **Justified deviations are preserved, not erased.** The output of a conformance run is not "everything is a token now." A deliberate exception with a stated reason and an owner is a healthy part of a system; an *undocumented* one is the defect. Lattice makes the exception set explicit and small, rather than pretending it is empty.
4. **Appearance parity as the safety oracle.** Swapping a raw value for a token must not change what renders. The visual diff is the parity oracle per `_common/DIFFERENTIAL_PARITY.md` — a "conformance fix" that shifts a layout by 2px is a defect, and the recipe catches it inside the loop rather than at review.

### Use `lattice` for

- A codebase where the design system exists on paper and the product has drifted from it.
- Post-`rebrand` or post-`layer` hardening: the tokens are right, but are they *used*?
- Preparing a component library extraction — the deviation ledger is the extraction backlog.
- Onboarding a team onto an existing system, where the honest first question is how far the code actually is from it.

### Not this — route to

| Not this | Route to | Why |
|----------|----------|-----|
| Old brand → new brand across every touchpoint | `rebrand` | Migration completeness with a change of identity; lattice is steady-state conformance with no identity change |
| Design the token architecture itself | `muse` (skill) | Lattice *consumes* a system; with none in place, it has no denominator |
| Document components / build the catalog | `vitrine` (skill) | Cataloging, not conformance proof |
| Improve how a surface looks | `restyle` / `runway` | Visual quality; lattice is behaviour- and appearance-preserving by contract |
| Code/architecture design weaknesses | `anneal` | Code design, not visual-system conformance |
| Delete dead code / unused files | `sweep` (skill) | Lattice removes only what its own proof orphans (Phase 5), gated |
| Technical change completeness (API, dependency, framework) | `migrate` | Same RESIDUE-GATE discipline, different object |
| Prove surfaces are usable / distinctive | `crucible` / `silhouette` | Different oracles entirely |

**Scale: 10-22 agents, 3-7× `feature` cost** (parity with `rebrand`, which shares the machinery). Per-phase: P0-P1 ≈ 2-3 (inventory) · P2 ≈ 2-4 (scan, parallel by surface batch) · P3 ≈ 3-8 per cycle (reconcile batches + regression) · P4 ≈ 2 (independent re-scan, looped to dry) · P5 ≈ 1 (decommission) · P6 ≈ 1. **Confirm tier: Ask First** on big-bang strategy / 10+ files (intentional parity with `rebrand`/`migrate` — a conformance sweep inherently touches 10+ files, so Ask First fires **once at launch**, and again before the destructive Phase 5 cut).

**Model selection (Plan-and-Execute):** Phase 2 deviation classification and the Phase 3 gap-vs-residue adjudication are judgment-heavy → plan-tier (opus / Fable 5); the scan, the mechanical replacement, and the re-scan → Sonnet 5 default, with `haiku` acceptable for pure grep-shaped scan passes.

---

## 2. Termination Bound

Reconciliation **`loop ≤ 3 cycles (default N=3)`**, plus the Phase 4 RESIDUE-GATE runs **until dry** (two consecutive independent re-scans finding zero), which is a convergence condition, not a cycle. Exit reasons use the canonical vocabulary:

| Exit reason | Lattice-specific meaning |
|-------------|-------------------------|
| `ACCEPT` / `target-met` | the independent re-scan finds **zero unclassified deviations and zero unjustified residue** twice consecutively, with appearance parity held on every batch |
| `diminishing-returns (Δ < ε)` | a cycle closed no new deviation class — report the open ledger with each remaining item's blocker |
| `cap-reached` | 3 cycles with residue remaining → deliver the Deviation Ledger with per-item ownership; the proof is explicitly **not** claimed |
| `BLOCK` | the system itself cannot express what the product needs (gaps outnumber residue, or a gap requires a design decision the run cannot make) → route to `muse` for a system extension, or `hallmark` when the gap is a brand-level decision. A legitimate delivery: the ledger *is* the system backlog |

**Completeness is never claimed from the forward counter.** "We converted 214 of 214 values" is a progress report, not a proof; only the independent re-scan produces `ACCEPT` (inherited from `migrate`'s non-negotiable #2).

## 3. Confirm / Safety Gate

- **Phase 0 precondition + framing: Ask First** on the big-bang-vs-batched strategy and on the inevitable 10+ file blast radius (intentional parity with `rebrand`/`migrate`; fires once at launch, not per batch). Surfaces: the system of record, the frozen surface count, the strategy, and the estimated deviation volume.
  **Precondition:** a system of record must exist (a token set, a component library, or a Hallmark Charter). None → the run stops and routes to `muse` (tokens) / `vitrine` (catalog) first. Lattice **never invents the system mid-sweep** — the same rule that sends a brandless `rebrand` to `hallmark`.
- **Phase 2 ledger ratification: contract-level checkpoint; AUTORUN cannot skip** — but only for the `gap` and `justified` classes. Mechanical `residue` needs no ratification; a **gap** means the system will be extended (a design decision), and a **justified** deviation means an exception is being blessed with an owner. Both are decisions the user owns.
- **Phase 5 DECOMMISSION: Ask First (destructive).** Removing orphaned one-off components and duplicate tokens is gated on the Phase 4 proof passing — never before, and never on the forward counter.
- Standard Ask First tiers (L4 security / destructive / 10+ files) apply unchanged.

## 4. Resume

**Checkpoint-resume** (≥ 4 phases; `lattice resume`): persist the frozen inventory (the denominator) at Phase 1 exit — **re-enumerating on resume is how a denominator silently shrinks**; persist the classified Deviation Ledger at Phase 2 exit; persist per-batch completion + appearance-parity results at each Phase 3 cycle boundary. Phase 4 always re-scans the **full** frozen inventory on resume, never the remaining batches only.

---

## 5. Phase Contract (AUTORUN chain template)

```
Phase 0   PRECONDITION + FRAMING ★Ask First (strategy + 10+ files, once at launch)
          system of record present? (tokens / component library / Hallmark Charter)
            → NO: stop, route to muse (tokens) / vitrine (catalog) — never invent it mid-sweep
          Nexus[scope + strategy: batched (default) vs big-bang + envelope]
   ▼
Phase 1   INVENTORY — freeze the denominator
          Lens[enumerate every UI surface + every style-bearing declaration:
               components, pages, stylesheets, inline styles, theme files, email templates,
               chart/config palettes, icon sets] ‖ Grove?[structure] ‖ Ripple[blast radius]
          → FROZEN INVENTORY (the denominator; never re-enumerated mid-run)
   ▼
Phase 2   SCAN ‖ per surface batch → DEVIATION LEDGER, three-way classified
          Muse[token conformance] ‖ Vitrine?[component conformance] ‖ Zen?[duplication]
          ┌ residue    : a raw value with a token equivalent (hardcoded hex, magic px,
          │              re-implemented component)              → the SURFACE is wrong
          ├ gap        : no token/component exists for a real need → the SYSTEM is wrong
          └ justified  : intentional deviation → needs a RECORDED REASON + an OWNER
          → ✓user ratifies the `gap` and `justified` classes ★contract-level
            (mechanical `residue` needs no ratification)
   ▼
Phase 3   RECONCILE loop ⟲ {  per batch
          gap        → Muse[extend the system: add the token/component, versioned] → the
                       deviation is re-classified as residue and then replaced
          residue    → Artisan/Muse[replace the raw value with the token / the one-off with
                       the component]
          justified  → record reason + owner in the ledger; the surface is NOT changed
          → APPEARANCE PARITY (the safety oracle, per _common/DIFFERENTIAL_PARITY.md):
            Voyager[visual regression, diff within the declared tolerance] +
            Radar[no-regression] + Palette[a11y ≥ baseline]
            → a conformance fix that changes what renders is a DEFECT: revert, re-classify
              as `gap` (the token was not equivalent after all)
          }⟲  loop ≤ 3 cycles (default 3)
   ▼
Phase 4   RESIDUE-GATE — INDEPENDENT re-scan of the FULL frozen inventory (producer ≠ verifier)
          fresh scanners with no Phase 3 history; looped UNTIL DRY (2× consecutive zero)
          → PASS = zero unclassified deviations ∧ zero unjustified residue
          → completeness is NEVER read off the forward counter (migrate non-negotiable #2)
   ▼
Phase 5   DECOMMISSION ★Ask First (destructive; gated on the Phase 4 proof)
          remove now-orphaned one-off components, duplicate tokens, dead theme entries
          → Radar[no-regression] + Voyager[visual regression] after the cut
   ▼
Phase 6   DELIVER — Coherence Proof + Drift Sentinel handoff + Guardian
          Hone?[a CI/pre-commit hook derived from the ledger so the proof does not decay —
                 the scan that produced the proof becomes the guard that preserves it]
```

## 6. What counts as a deviation

Scoped by the system of record; the default scan surface:

| Class | Examples |
|-------|----------|
| **Colour** | raw hex/rgb where a token exists · a near-duplicate token (`#3B82F6` vs `#3b82f7`) · a hardcoded state colour |
| **Spacing** | magic pixel values off the scale · ad-hoc negative margins · one-off gap values (defensible scale values → `_common/PROPORTION_AND_SPACING.md` §3) |
| **Type** | font-size/line-height/weight outside the scale · a second font stack · hardcoded `letter-spacing` |
| **Component** | a re-implemented button/input/modal · a copy-pasted variant that should be a prop · a component bypassing the library's a11y wiring |
| **Radius / elevation / motion** | shadow and radius values off the scale · durations and easings outside the motion tokens |
| **Breakpoint / grid** | ad-hoc media queries · container widths off the grid |
| **Semantics** | a token used for a meaning it does not carry (`--danger` for an accent) — a conformance pass that only greps values misses this, so classification is model-judged, not purely mechanical |

## 7. Output Report — **Coherence Proof** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **System of record** — what the denominator was measured against, and its version
- **Frozen inventory** — surface count + declaration count at freeze time (the denominator)
- **Deviation Ledger** — every deviation with its class (`residue` / `gap` / `justified`), its surface, and its resolution; **the justified set listed in full with reasons and owners** — this section is the deliverable, not an appendix
- **System extensions** — every `gap` that became a new token/component, with the decision that authorized it
- **Appearance parity** — per-batch visual-diff results, tolerance used, and every reverted "fix" that turned out to change rendering
- **RESIDUE-GATE** — the independent re-scan record: rounds run, count per round, the two consecutive zeros (or the residue that remains)
- **Decommission** — what was removed, and the proof it was gated on
- **Exit reason** (§2 vocabulary) + conformance rate + the open ledger on any non-`ACCEPT` exit
- **Drift Sentinel** — the CI/pre-commit check handed off (or the reason none was installed)

## 8. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Completeness claimed from the forward counter | RESIDUE-GATE: independent re-scan of the full inventory, looped to dry (Phase 4, `migrate` non-negotiable #2) |
| Denominator shrinking mid-run | Inventory frozen at Phase 1 and never re-enumerated; resume re-scans the frozen set (§4) |
| **System gaps papered over with the nearest wrong token** | Three-way classification: a `gap` extends the system, it does not get force-fitted (§1.2, Phase 3) |
| Intentional exceptions erased as "non-conforming" | `justified` is a first-class class with a recorded reason and owner, preserved in the report (§1.3, §7) |
| A "conformance fix" that moves the layout | Appearance parity per `_common/DIFFERENTIAL_PARITY.md` inside the loop; violations revert and re-classify (Phase 3) |
| Semantic misuse invisible to a grep | Classification is model-judged, not purely mechanical (§6 Semantics row) |
| Running with no system to conform to | Phase 0 precondition routes to `muse`/`vitrine`; the system is never invented mid-sweep (§3) |
| Destructive cleanup before the proof | Phase 5 DECOMMISSION gated on the Phase 4 pass, Ask First (§3) |
| Producer verifying its own sweep | Phase 4 uses fresh scanners with no Phase 3 history (Q9) |
| The proof decaying the week after it is delivered | Phase 6 Drift Sentinel: the scan becomes a CI/pre-commit check via `hone` |
| Confusing this with a brand migration | §1 and the routing table: identity change → `rebrand`; steady-state conformance → `lattice` |
| Unbounded scope on a large codebase | Batched strategy by default; Ask First at launch names the batch plan and the envelope |

## 9. Shared-Protocol References

| Protocol | What lattice takes from it | Lattice-specific specialization |
|----------|---------------------------|--------------------------------|
| `reference/migrate-recipe.md` | The three non-negotiables: freeze the denominator · prove residue don't trust the counter · delete only after the proof | Applied to design-system conformance in **steady state** (no identity change), with a three-way deviation classification migrate does not need |
| `reference/rebrand-recipe.md` | RESIDUE-GATE shape, per-surface batching, decommission gating | Same machinery, different denominator: the token/component system rather than an old→new brand mapping |
| `_common/DIFFERENTIAL_PARITY.md` | Parity-over-faith, oracle adequacy, comparator discipline | The parity oracle is the **rendered appearance**: a token swap must be visually identical within a declared tolerance |
| `_common/PROPORTION_AND_SPACING.md` | Spacing scales, type scales, grid, touch targets, §1 evidence tiers | When a `gap` must be filled, the new token's value is justified from Tier 1-2 sources, never Tier 4 folklore |
| `reference/autonomy-quality-protocol.md` | Q9 producer ≠ verifier, Q10 evidence-bound claims, Q15 Acceptance Provenance | Q10 native: "conformant" is only claimed with the two-consecutive-zero re-scan record attached |
| `reference/evaluator-loop-protocol.md` | Cycle cap, flatten rule | The reconcile loop; the RESIDUE-GATE's until-dry condition sits outside the cycle count |
| `reference/doc-quality-protocol.md` | W1-W12 | Applies to the Coherence Proof document |
| `reference/verdict-gate.md` | — | `N/A` — lattice proves a property; it delivers no which-feature verdict |

## 10. Decision Tree vs Neighbors

```
Does a design system of record exist (tokens / component library / Brand Book)?
  NO  → muse (design the tokens) / vitrine (catalog) first — lattice has no denominator
  YES ↓
Is the brand identity CHANGING?
  YES → rebrand (old→new propagation, completeness-proven)
  NO ↓
Is the goal to change how it LOOKS, or to prove it derives from the system?
  LOOKS → restyle (standard bar) / runway (flagship ceiling)
  DERIVES ↓
Is the object visual conformance, or code/architecture design?
  CODE DESIGN → anneal
  VISUAL SYSTEM → lattice — freeze → scan+classify → reconcile ⟲ → residue-gate to dry
                  → decommission → install the sentinel
```
