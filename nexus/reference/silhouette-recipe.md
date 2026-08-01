# Silhouette Recipe — Distinction Proof for a Product Surface

> `/nexus silhouette "<surface or product>"` — strip the logo and see whether anyone can still tell it is yours. The **anti-genericness** member of the Quality-Max design wing: sweep the category's visual prior art, pre-commit the ordinary moves everyone makes, then prove the surface is **identifiable at above-chance rate in a blind test** against competitor surfaces — without buying that distinctiveness with usability. `hallmark` runs the logo-swap test on a *brand identity*; `silhouette` runs it on the *product surface itself*, which is where the genericness actually shows.

Read this file before executing the `silhouette` Recipe.

---

## 1. Nature / When to Use / Boundaries

**A tournament that maximizes craft can converge on the category average.** Every team reads the same design systems, adopts the same component library, and arrives at the same competent, forgettable screen. `runway` will happily push that screen to `all dims = 3`: it is genuinely well-made, and it is also indistinguishable from four competitors. Nothing in the roster asks whether it is *ours*.

Silhouette's identity is four things no sibling carries together:

1. **Sameness Ledger, pre-committed.** A blind panel enumerates the category's ordinary design moves **before seeing our surface** — the same pre-commitment discipline `eureka` uses for its `OBVIOUS` test. "We're distinctive" cannot be claimed in hindsight against a ledger written after the fact.
2. **Inverted-polarity visual sweep.** Prior art is researched to *avoid*, not to reach (`clone` reproduces, `wish` reaches, `silhouette`/`eureka` avoid). The competitor set is simultaneously the sameness evidence and the blind-test distractor pool.
3. **Blind Recognition Test as the oracle.** Branding stripped, our surface is mixed with K competitor surfaces and a fresh panel is asked to attribute them. The pass threshold is **declared before the measurement**, expressed against chance (1/(K+1)). This is the only design oracle in the roster that is a measured rate rather than a rubric score.
4. **Distinctiveness must be free.** A hard constraint, not a preference: a11y and task friction may not regress. Weirdness that costs usability is rejected inside the loop, so the recipe cannot succeed by making the product strange. Every surviving distinctive move must also **derive from a brand truth** — a Hallmark Charter value, a stated positioning, a real product property — never from arbitrary novelty.

### Use `silhouette` for

- A surface that scores well on craft and still "looks like every other AI/SaaS product."
- Post-`runway` or post-`restyle` verification that the winner is distinctive, not just competent.
- A category diagnosis before a redesign: *what are the default moves here, and which ones are we making?*
- Establishing a defensible visual position when the brand is settled but the product surface has drifted to convention.

### Not this — route to

| Not this | Route to | Why |
|----------|----------|-----|
| Create the brand identity (values / voice / visual core) | `hallmark` | Silhouette tests a *surface*; it consumes a settled identity as its derivation source. No brand truths to derive from → `hallmark` first |
| Propagate a settled brand across every touchpoint | `rebrand` | Completeness, not distinctiveness |
| Maximize craft quality of a flagship surface | `runway` | Orthogonal: a runway winner can be generic, and silhouette's Phase 2 can run as an added runway rubric dimension (§10) |
| Improve an existing surface to a standard bar | `restyle` | Improve family; no distinctiveness oracle |
| Competitive/positioning analysis with no design change | `compete` (skill) | Research only |
| Invent a novel *mechanism* (not a look) | `eureka` | Same pre-commit discipline, different object: mechanism novelty vs visual distinctiveness |
| Prove the surface is usable under hostile conditions | `crucible` | Floor proof; silhouette holds that floor constant but does not raise it |

**Scale: 14-30 agents × ≤3 cycles, 5-9× `feature` cost.** Per-phase: P0 ≈ 1 · P1 ≈ 3 (blind default-move panel) · P1.5 ≈ 3-6 (visual prior-art sweep) · P2 ≈ 3-4 (recognition panel + sameness scoring) · P3 ≈ 3-6 per cycle (direction + implementation + re-measure + regression guards) · P4 ≈ 3 (fresh panel + derivation check) · P5 ≈ 1.

*Range derivation* (convention: `reference/recipe-contract.md` §1 element 7): floor = one surface, ACCEPT on cycle 1 → 1+3+3+3+3+... = **14**; ceiling = a surface set, 3 cycles, wide competitor pool → 1+3+6+4+(6×3=18 with shrinking re-measures ≈ 14)+3+1 = **30**. **Confirm-before-launch always** (intentional parity with `runway`/`wish`).

**Model selection (Plan-and-Execute):** the Phase 1 default-move panel, the Phase 4 derivation check, and threshold adjudication are judgment-heavy → plan-tier (opus / Fable 5). The recognition panels, sweep, and implementation → Sonnet 5 default. The recognition panel is **engine-diverse where the hub allows** (`_common/CLI_COMPATIBILITY.md §4`) — a single model family attributing surfaces carries one set of visual priors, which is exactly the bias the test is meant to exclude.

---

## 2. Termination Bound

Convergence **`loop ≤ 3 cycles (default N=3)`**. Exit reasons use the canonical vocabulary:

| Exit reason | Silhouette-specific meaning |
|-------------|----------------------------|
| `ACCEPT` / `target-met` | the Phase 4 **fresh-panel** blind attribution rate meets the pre-declared threshold **and** the derivation check passes (every distinctive move traces to a brand truth) **and** neither a11y nor task friction regressed from the Phase 2 baseline. All four conditions are one oracle: the Distinction Contract |
| `diminishing-returns (Δ < ε)` | attribution rate moved < 10 percentage points between cycles while still below threshold — report which moves were tried and why they did not register |
| `cap-reached` | 3 cycles below threshold → deliver the Sameness Ledger + the best surface with its measured rate and the named residual |
| `BLOCK` | **`convention-locked`** — the category's conventions are load-bearing for usability (regulated, safety-critical, or deeply learned interfaces) and every tested deviation cost friction. A legitimate delivery, not a failure: the honest finding is *distinctiveness must come from voice, content, motion, or mechanism, not layout* — hand off to `hallmark`/`prose`/`flow`/`eureka` |

On any non-`ACCEPT` exit the recipe reports the measured attribution rate, the chance baseline, and the surviving sameness items. A rate without its chance baseline is meaningless and is never reported alone.

**The threshold is declared before the first measurement** (Phase 1, ratified with the user) and may not be lowered mid-run. Lowering it after seeing the result converts the oracle into a formality; a threshold that turns out to be unreachable exits `cap-reached` with the number, not with a softer bar.

## 3. Confirm / Safety Gate

- **Phase 0 framing: Confirm before launch — always** (unconditional; intentional parity with `runway`/`wish`, not drift). Surfaces: the target surface(s), the category definition and competitor-pool size K, the proposed pass threshold against chance, the cost envelope, and — when the ask is really a craft-quality ask — a recommendation of `runway`/`restyle` instead.
- **Phase 1 Distinction Contract: contract-level checkpoint; AUTORUN cannot skip.** The category definition, K, and the threshold are the oracle. A category drawn too wide ("software") makes any surface distinctive; drawn too narrow it makes distinction impossible. The user ratifies the boundary.
- **Phase 1.5 competitor set: contract-level.** The user confirms the pool before it becomes both the sameness denominator and the distractor set — a pool missing the obvious competitor invalidates every downstream measurement, and that is cheap to catch here.
- **Phase 3 implementation: standard Ask First tiers** (brand-level token changes, 10+ files) apply unchanged. A distinctive move that changes brand tokens escalates to `hallmark`, never decided inside the loop.
- On a Fable 5 hub the Phase 0 gate subsumes the F8 cost gate — one confirmation, not two.

## 4. Resume

**Checkpoint-resume** (≥ 4 phases; `silhouette resume`): persist the Distinction Contract (category, K, threshold) at Phase 1 exit; persist the **pre-committed Sameness Ledger** and the competitor set with citations at Phase 1.5 exit — re-running the sweep on resume both re-spends and risks a *different* ledger, which would silently move the denominator; persist each cycle's attribution rate, the surface state, and the a11y/friction baselines at every Phase 3 boundary. The Phase 1 ledger is never regenerated after a candidate exists — that is the whole point of pre-commitment.

---

## 5. Phase Contract (AUTORUN chain template)

```
Phase 0   FRAMING ★Confirm-before-launch (always)
          Nexus[surface + category + competitor pool size K + proposed threshold + envelope
               + cheaper-path recommendation → runway (craft) / restyle (standard bar)]
   ▼
Phase 1   PRE-COMMIT ★contract-level checkpoint (AUTORUN cannot skip; plan-tier)
          BLIND default-move panel — Vision ‖ Muse ‖ Palette, given the CATEGORY ONLY and
          explicitly NOT our surface:
            "enumerate the design moves a competent team in this category makes as a matter
             of course" (layout skeleton · type stack · colour move · component idiom ·
             motion idiom · imagery idiom · copy pattern)
          → SAMENESS LEDGER, frozen and timestamped BEFORE any candidate is seen
          → DISTINCTION CONTRACT: category boundary · K · pass threshold vs chance 1/(K+1)
            · the brand truths distinctive moves must derive from (Hallmark Charter / stated
              positioning / real product property)
          → ✓user ratifies
   ▼
Phase 1.5 SWEEP ★contract-level ratification            [research to AVOID, not to reach]
          Compete ‖ Vector?[capture competitor surfaces] ‖ Frame? — per
          reference/research-grounding.md (tiered sources, cited Evidence Ledger),
          polarity INVERTED per eureka's Prior-Art Ledger
          → COMPETITOR SET (K surfaces, branding-strippable, cited)
          → ledger enrichment: which pre-committed moves are actually observed, and at what rate
          → ✓user ratifies the pool → the denominator FREEZES
   ▼
Phase 2   MEASURE — the baseline
          (a) BLIND RECOGNITION TEST: our surface + K competitor surfaces, wordmarks / product
              names / logos / brand-unique colour stripped, presented in randomized order to a
              fresh, engine-diverse panel that has NOT seen the Sameness Ledger
              → attribution rate vs chance 1/(K+1)
          (b) SAMENESS SCORE: % of our surface's load-bearing design decisions that appear
              verbatim in the pre-committed ledger
          (c) BASELINES CAPTURED: Palette[a11y] + Echo[task friction] — the constraint floor
              for Phase 3
   ▼
Phase 3   DIVERGE loop ⟲ {
          Vision[distinctive direction DERIVED from a named brand truth — never novelty for
                 its own sake; each move states the truth it expresses]
          → implement (Muse[tokens] ‖ Artisan ‖ Flow?[motion signature] ‖ Ink?[icon/illustration
            signature] ‖ Prose?[voice on the surface])
          → RE-MEASURE (a) fresh panel each cycle, (b) sameness score
          → CONSTRAINT CHECK (hard, non-negotiable): Palette[a11y ≥ baseline] +
            Echo[task friction ≤ baseline] + Radar[no-regression]
            → any distinctiveness gain purchased with friction is REJECTED and reverted;
              the move is recorded in the ledger as "distinctive but not free"
          }⟲  loop ≤ 3 cycles (default 3)
   ▼
Phase 4   ATTRIBUTION GATE (both parts; one oracle — the Distinction Contract)
          (a) FRESH-PANEL BLIND TEST — a panel that saw none of the prior rounds, no ledger,
              no history (producer ≠ verifier, Q9): attribution rate ≥ the pre-declared
              threshold
          (b) DERIVATION CHECK — plan-tier: every distinctive move traces to a named brand
              truth. A move that traces to nothing is decoration; it is stripped, and the
              surface is re-measured without it
          → both pass ∧ constraints held → ACCEPT
   ▼
Phase 5   DELIVER — Distinction Dossier + Guardian (if code shipped)
```

## 6. Measuring attribution honestly

- **Chance is stated, always.** With K competitors the baseline is 1/(K+1). A 40% attribution rate is strong at K=9 and worthless at K=1. Every reported rate carries its K.
- **Panels are fresh per measurement.** A panel that has seen our surface before is measuring memory, not distinctiveness. Phase 2, each Phase 3 cycle, and Phase 4 use different panels.
- **Strip more than the logo.** Wordmark, product name, brand-unique colour token, and any copy naming the product are removed. Leaving the brand colour in makes the test trivially passable and proves nothing about the design.
- **K ≥ 3.** Below that the test cannot separate distinctiveness from a coin flip; Phase 0 refuses a smaller pool and expands the category boundary instead.
- **A single surface is a weak claim; a set is a strong one.** When the scope is a product rather than a screen, sample 2-4 surfaces and report per-surface rates — a distinctive marketing page attached to a generic product interior is a known and reportable pattern.

## 7. Output Report — **Distinction Dossier** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Distinction Contract** — category boundary, K, pre-declared threshold, the brand truths in scope
- **Sameness Ledger** — the pre-committed default moves with their timestamp, plus the observed rate of each in the competitor set, plus **which ones we were making at baseline**
- **Competitor set** — the K surfaces with citations (per `reference/research-grounding.md` tiers)
- **Measurement trajectory** — attribution rate per cycle **with its chance baseline**, sameness score per cycle, panel composition per measurement
- **Distinctive moves** — each surviving move, the brand truth it derives from, and its measured contribution; moves rejected as "distinctive but not free" listed with their friction cost
- **Constraint record** — a11y and task-friction baselines vs final; any reverted move
- **Attribution Gate** — fresh-panel verdict, derivation-check verdict, stripped decorative moves
- **Exit reason** (§2 vocabulary) + final rate vs threshold vs chance + surviving sameness items
- **Handoff** — `convention-locked` exits name the non-layout channels to pursue (voice → `hallmark`/`prose`, motion → `flow`, mechanism → `eureka`)

## 8. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Craft-maximized into the category average** | The oracle is attribution rate, not a craft rubric — a `runway` winner can fail here (§1) |
| Distinctiveness claimed in hindsight | The Sameness Ledger is pre-committed and frozen before any candidate is seen (Phase 1) |
| The panel's own priors decide the answer | Fresh, engine-diverse panels; blind presentation; randomized order (§6) |
| Brand colour left in, test trivially passed | Strip wordmark + product name + brand-unique colour + naming copy (§6) |
| Threshold quietly lowered to reach ACCEPT | Declared at Phase 1, ratified, immutable; unreachable → `cap-reached` with the number (§2) |
| Rate reported without context | Every rate carries K and the chance baseline (§6, §7) |
| **Distinctiveness bought with usability** | Hard constraint inside the loop: a11y ≥ baseline ∧ friction ≤ baseline, violations reverted (Phase 3) |
| Novelty for its own sake | Derivation check: every surviving move traces to a named brand truth or is stripped (Phase 4b) |
| Category drawn to guarantee the answer | Category boundary + K ratified at the contract-level Phase 1 gate; K ≥ 3 enforced |
| Competitor pool missing the obvious rival | Phase 1.5 contract-level ratification of the pool before it becomes the denominator |
| Memory mistaken for recognition | A different panel per measurement (§6) |
| A distinctive landing page over a generic product | Multi-surface sampling with per-surface rates (§6) |
| Running with no brand to derive from | Phase 0 precondition: no settled identity → route to `hallmark` first |
| Forcing distinction on a convention-locked category | `BLOCK (convention-locked)` is a legitimate delivery with a named alternative channel (§2) |

## 9. Shared-Protocol References

| Protocol | What silhouette takes from it | Silhouette-specific specialization |
|----------|------------------------------|-----------------------------------|
| `reference/research-grounding.md` | Tiered sources, per-claim verification, cited Evidence Ledger | **Inverted polarity** (shared with `eureka`): the sweep produces a denominator to *avoid*, and the same set doubles as the blind-test distractor pool |
| `_common/ADVERSARIAL_REFUTATION.md` | Skeptic panel, polarity, exclusions, engine diversity | The claim under attack is "this surface is distinctive"; the refutation is *executed as a measurement* (blind attribution) rather than argued |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, cycle cap, flatten rule | The Evaluator is a measurement panel; the oracle is a rate against a pre-declared threshold |
| `reference/autonomy-quality-protocol.md` | Q1-Q3 intent contract, Q9 producer ≠ verifier, Q10 evidence-bound claims, Q15 | Q9 discharged with a fresh panel at Phase 4; Q10 native — no distinctiveness claim without its measured rate and K |
| `_common/PROPORTION_AND_SPACING.md` | §1 evidence tiers | A distinctive move may **not** be justified by Tier 4 folklore (golden ratio, Z-pattern); §10 contradictions apply |
| `reference/hallmark-recipe.md` | The logo-swap discipline | Hallmark swaps a competitor's logo *into* our identity; silhouette strips *all* logos and measures attribution across a pool — the surface-level generalization |
| `reference/dialogue-protocol.md` | Question craft, checkpoint presentation | Phase 1 contract ratification only (D1-D4) |
| `reference/verdict-gate.md` | — | `N/A` — silhouette proves a property; it does not deliver a which-feature verdict |

## 10. Integration with `runway`

Silhouette's Phase 2 measurement can run **inside** a `runway` tournament as an added rubric dimension ("Distinction: attribution rate ≥ threshold at K"), turning the ceiling recipe's blind spot into one of its scored axes. Use that form when a flagship surface is being *created*; use the standalone recipe when an *existing* product needs the diagnosis — the standalone run additionally produces the Sameness Ledger, which the embedded form does not, and which is reusable across every later surface.

When both run, silhouette's threshold is declared at runway's Phase 1 rubric gate and inherits runway's cycle cap — the two never nest as separate loops (`converge-recipe.md` §4 flatten rule).

## 11. Decision Tree vs Neighbors

```
Is there a settled brand identity to derive distinctive moves from?
  NO  → hallmark first (silhouette cannot pass its derivation check without one)
  YES ↓
Is the question "is it well made?" or "is it recognizably ours?"
  WELL MADE → runway (flagship ceiling) / restyle (standard bar)
  OURS ↓
Is the surface being created now, or already shipped?
  CREATED NOW → runway with silhouette's Phase 2 as a rubric dimension (§10)
  ALREADY SHIPPED ↓
Is the object a look, or a mechanism?
  MECHANISM → eureka (novelty-proven invention; same pre-commit discipline)
  LOOK → silhouette — pre-commit → sweep → measure → diverge ⟲ → fresh-panel gate → prove
```
