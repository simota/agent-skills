# Crucible Recipe — Operability Proof under Adversarial Conditions

> `/nexus crucible "<surface or flow>"` — the **floor** member of the Quality-Max design wing: prove that every critical task still completes when the conditions are not ideal. Where `runway` raises the ceiling of how a surface *looks and feels* under a rubric, `crucible` proves the *floor* — that the surface remains operable for a user with low vision, one hand, a screen reader, a bad network, an empty database, a 10,000-row list, or a 40-character localized label. The oracle is **binary task completion per condition cell**, not a score.

Read this file before executing the `crucible` Recipe.

---

## 1. Nature / When to Use / Boundaries

**Crucible is a proof, not an evaluation.** Its identity comes from four things no sibling carries together:

1. **Binary oracle.** Every cell of the matrix is `PASS` (the task completed) or `FAIL` (it did not). There is no 2-of-3. A rubric score can average away a condition in which the product is unusable; a completion ledger cannot.
2. **Declared denominator.** The Critical Task Set and the Condition Set are ratified *before* any run, so "we tested it" becomes "we tested exactly these N cells, and here are the M we deliberately dropped." Coverage that is chosen after seeing the results is not coverage.
3. **Adversarial conditions, not personas.** `runway`/`restyle` ask a persona how a surface *feels*. Crucible puts the same task in front of a degraded environment and asks whether it *finishes*. Feeling is a ceiling question; finishing is a floor question, and only one of them is a defect when it fails.
4. **Content reality as a first-class axis.** Designs are validated on happy-path content. The empty state, the overflowing list, the missing avatar, the maximum-length label, and the RTL string are conditions in the matrix, not edge cases someone remembers to check.

### Use `crucible` for

- A surface that is already visually good and needs to be proven *usable* — the natural successor to a `runway` or `restyle` run.
- Pre-launch hardening of a critical flow (signup, checkout, recovery, onboarding) where a single unusable condition is a revenue or compliance event.
- Answering "is this accessible?" with evidence rather than a compliance checklist — WCAG conformance is a *condition* in the matrix, not the whole matrix.
- Retrofitting confidence onto an inherited surface whose real-world behaviour nobody has ever measured.

### Not this — route to

| Not this | Route to | Why |
|----------|----------|-----|
| Maximize the visual/craft quality of a flagship surface | `runway` | Ceiling recipe; crucible proves the floor and does not judge taste |
| Improve an existing surface's design to a standard bar | `restyle` | Improve family; direction-driven, no completion proof |
| Check conformance to a named standard (WCAG / OWASP / HIG) | `canon` (skill) | Standards adjudication — crucible *uses* it as one condition, and a mechanical pass is not a completion proof |
| A task that fails under **ideal** conditions | `bug` | Phase 2 routes it out by contract — a broken happy path is a defect, not a condition failure |
| System load, chaos, resilience of the backend | `siege` (skill) | Crucible is siege for the *interface*; siege owns the system |
| One named a11y fix | `palette` (skill) | Minimum viable chain |
| E2E regression suite authoring | `voyager` (skill) | Crucible *uses* Voyager to execute cells; it does not own the suite |
| Prove the design is distinguishable from competitors | `silhouette` | Distinctiveness, not operability |

**Scale: 16-34 agents × ≤3 cycles, 5-11× `feature` cost.** Per-phase: P0-P1 ≈ 2 · P1.5 ≈ 1-2 (matrix reduction) · P2 ≈ 2-3 (ideal-condition baseline) · P3 ≈ 6-12 executors + 2-4 remediators **per cycle** · P4 ≈ 3-4 (independent full re-run) · P5 ≈ 1.

*Range derivation (keep reconciled when a phase figure changes):* floor = 3 tasks × a reduced 8-cell matrix, ACCEPT on cycle 1 → 2+1+2+(6+2)+3+1 = **16**; ceiling = 5 tasks × a reduced 20-cell matrix, 3 cycles → 2+2+3+(12+2 on cycle 1, +5 and +4 on the shrinking re-runs of cycles 2-3 ≈ 23)+4+1 = **34**. The stated range is the sum of the per-phase figures, not an independent estimate. **Confirm-before-launch always** (intentional parity with `runway`/`summit`).

**Model selection (Plan-and-Execute):** Phase 1 task/condition declaration and the Phase 4 gate adjudication are judgment-heavy → plan-tier (opus / Fable 5). Cell execution, remediation, and re-runs → Sonnet 5 default.

---

## 2. Termination Bound

Convergence **`loop ≤ 3 cycles (default N=3)`**. Exit reasons use the canonical vocabulary:

| Exit reason | Crucible-specific meaning |
|-------------|--------------------------|
| `ACCEPT` / `target-met` | the Phase 4 independent full-matrix re-run finds **zero open critical cells** — and zero cells that passed earlier and now fail (remediation regression) |
| `diminishing-returns (Δ < ε)` | a cycle closed **no new cell**. With a binary oracle the ε is not a score delta: one full cycle producing zero newly-passing cells is the plateau signal. Report every open cell with the reason it resisted |
| `cap-reached` | 3 cycles with open cells remaining → deliver the ledger with each open cell named, classified `wont-fix` / `needs-redesign` / `needs-platform-support` |
| `BLOCK` | the surface cannot be made operable without a premise change (the flow itself is wrong) → recommend `restyle`/`feature`/`flux` reframe; or Agent Tennis → escalate |

On any non-`ACCEPT` exit the recipe reports the pass rate **and the identity of every failing cell** — a percentage without the cell list is not a result. An 85% pass rate that hides "screen-reader users cannot complete checkout" is worse than no number.

**Non-critical cells never block.** The Critical Task Set (Phase 1) is what the gate is measured on; cells outside it are recorded as findings and handed off, never used to fail the run.

## 3. Confirm / Safety Gate

- **Phase 0 framing: Confirm before launch — always** (unconditional; intentional parity with `runway`/`summit`, not drift). Surfaces: the target surface, the proposed Critical Task Set size, the condition-set breadth, the reduced cell count, and the cost envelope — plus, when the ask is really a single a11y fix or a visual improvement, an explicit recommendation of the cheaper path (`palette` direct / `restyle`).
- **Phase 1 declaration: contract-level checkpoint; AUTORUN cannot skip.** The Critical Task Set *is* the denominator of the proof. A task set the user does not recognize as theirs produces a proof about the wrong product.
- **Phase 1.5 matrix reduction: contract-level.** The dropped cells are shown before they are dropped — a silently truncated matrix reads as full coverage in the report, which is the one failure this recipe must never commit.
- **Phase 3 remediation: standard Ask First tiers** (10+ files, brand-level token changes) apply unchanged.
- On a Fable 5 hub the Phase 0 gate subsumes the F8 cost gate — one confirmation, not two.

## 4. Resume

**Checkpoint-resume** (≥ 4 phases; `crucible resume`): persist the ratified Critical Task Set + Condition Set + the reduced matrix **with its dropped-cell record** at Phase 1.5 exit; persist the Phase 2 ideal-condition baseline; persist the full cell result table at each Phase 3 cycle boundary. A resumed run re-executes only open cells in Phase 3 — but Phase 4 always re-runs the **entire** matrix, because a resumed remediation is exactly when a passed cell silently regresses.

---

## 5. Phase Contract (AUTORUN chain template)

```
Phase 0   FRAMING ★Confirm-before-launch (always)
          Nexus[surface + task-set size + condition breadth + reduced cell count + cost envelope
               + cheaper-path recommendation → palette direct / restyle]
   ▼
Phase 1   DECLARE ★contract-level checkpoint (AUTORUN cannot skip; plan-tier)
          Echo ‖ Palette ‖ Pulse? → CRITICAL TASK SET (3-5 tasks; each with an OBSERVABLE
          success definition — "the order confirmation is reachable and readable", not
          "checkout feels smooth")
          → CONDITION SET selected from the §6 axes (sensory · motor · cognitive/context ·
            environment · content reality), each with a REPRODUCIBLE setup
          → ✓user ratifies both → the denominator FREEZES
   ▼
Phase 1.5 MATRIX REDUCTION ★contract-level
          Matrix[minimum covering set over (task × condition); pairwise by default,
                 full cross-product only when the cell count is small]
          → REDUCED MATRIX + explicit DROPPED-CELL RECORD (never a silent truncation)
   ▼
Phase 2   BASELINE — every critical task under IDEAL conditions
          Voyager[happy-path execution] + Echo[walkthrough]
          → any FAIL here EXITS the recipe → route to `bug` (a broken happy path is a defect;
            proving it also breaks under stress is spend with no information)
   ▼
Phase 3   TRIAL loop ⟲ {
          EXECUTE ‖ cells by axis:
            sensory        → Palette[screen-reader-only run] ‖ Canon[WCAG 1.4.10 reflow /
                             1.4.11 contrast, mechanical] ‖ Echo[low-vision persona at 200-400% zoom]
            motor          → Voyager[keyboard-only path] ‖ Palette[target size WCAG 2.5.8/2.5.5
                             per _common/PROPORTION_AND_SPACING.md §6]
            cognitive      → Echo[first-run no-onboarding ‖ interrupted-and-returning ‖
                             non-native reader]
            environment    → Voyager[throttled network / offline mid-action / small + large
                             viewport / dark mode]
            content reality→ Radar[fixture generation: empty · overflow · missing asset ·
                             max-length label · RTL · long localized string]
                             → Voyager/Pixel[render + complete the task against each fixture]
          → FAILURE LEDGER (cell, task, condition, where it broke, repro)
          → REMEDIATE (Artisan ‖ Palette ‖ Prose[copy that overflows] ‖ Flow[motion/reduced-motion]
            ‖ Muse[token fix] ‖ Polyglot?[l10n string handling])
          → RE-RUN failed cells only
          }⟲  loop ≤ 3 cycles (default 3)
   ▼
Phase 4   FLOOR GATE — INDEPENDENT full-matrix re-run (producer ≠ verifier, Q9)
          fresh executors, no Phase 3 history: re-run EVERY cell, not only the remediated ones
          → PASS = zero open critical cells ∧ zero regressions on previously-passing cells
          → any regression is reported as loudly as an open cell: remediation that trades one
            condition for another has not moved the floor, it has moved the hole
   ▼
Phase 5   DELIVER — Operability Proof + Guardian (if code shipped)
```

### 6. Condition axes (the default set)

Phase 1 selects from these; a surface-specific axis may be added, and any axis may be dropped **on the record**. Numbers cite `_common/PROPORTION_AND_SPACING.md` evidence tiers — Tier 1-2 (spec / published system) are requirements, Tier 3 conventions are stated as conventions, Tier 4 folklore is never a pass criterion.

| Axis | Default conditions |
|------|-------------------|
| **Sensory** | screen-reader-only · 200% zoom · 400% reflow (WCAG 1.4.10) · low contrast environment · colour-vision deficiency · dark mode |
| **Motor** | keyboard-only · one-handed / thumb-reach on a small viewport · minimum target size (WCAG 2.5.8 24×24, 2.5.5 44×44) · reduced motion |
| **Cognitive / context** | first run with no onboarding · interrupted mid-task and returning · non-native reader · returning after 30 days |
| **Environment** | throttled/flaky network · offline mid-action · smallest supported viewport · largest supported viewport · slow device |
| **Content reality** | empty (0 items) · overflow (10k items) · missing image/avatar · maximum-length label · RTL · longest localized string · unusual characters |

## 7. Output Report — **Operability Proof** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Denominator** — the ratified Critical Task Set + Condition Set, the reduced matrix size, and the **dropped-cell record** with the reduction rationale
- **Baseline** — Phase 2 ideal-condition result (and the `bug` routing if it fired)
- **Cell matrix** — the full task × condition grid with per-cell `PASS`/`FAIL`/`DROPPED`/`N-A`, cycle by cycle
- **Failure Ledger** — every failure found, its repro, its remediation, and its final state
- **Regression record** — any previously-passing cell broken by a remediation, and how it was resolved
- **Floor Gate verdict** — the independent full re-run result (producer ≠ verifier attested)
- **Open cells** — on any non-`ACCEPT` exit: each open cell **named**, with `wont-fix` / `needs-redesign` / `needs-platform-support` and an owner. Never a bare percentage
- **Exit reason** (§2 vocabulary) + pass rate + the residual list
- **Handoff** — cells needing a design change → `restyle`/`runway`; cells needing a capability → `feature`; standing regression coverage → `voyager`

## 8. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| "It's accessible" asserted from a compliance checklist | WCAG checks are one *axis*; the oracle is task completion under that condition (§1.1, §6) |
| A condition is discovered only after launch | Declared Condition Set ratified before the run (Phase 1), reduced on the record (Phase 1.5) |
| Coverage chosen after seeing results | The denominator freezes at Phase 1; dropped cells are recorded, never silently truncated |
| A score averages away an unusable condition | Binary per-cell oracle — no aggregation into a passing average (§1.1) |
| Happy-path defect burned as a stress-test finding | Phase 2 baseline exits to `bug` before any condition spend |
| Remediation trades one condition for another | Phase 4 re-runs the **whole** matrix; regressions are reported as loudly as open cells |
| Producer grades its own fix | Phase 4 uses fresh executors with no Phase 3 history (Q9) |
| Combinatorial explosion of task × condition | Phase 1.5 pairwise reduction via `matrix`, with the dropped set stated |
| Happy-path content hiding real-world breakage | Content reality is an axis with generated fixtures (`radar`), not an afterthought |
| A percentage standing in for a result | §2 and §7 both forbid a pass rate without the failing-cell list |
| Persona *opinion* substituted for completion evidence | Echo is an executor here, not a judge; its output is a completion verdict + repro |
| Spend on a surface that is not yet good | Phase 0 recommends `restyle`/`runway` first when the ask is really a quality ask |

## 9. Shared-Protocol References

| Protocol | What crucible takes from it | Crucible-specific specialization |
|----------|----------------------------|----------------------------------|
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, cycle cap, flatten rule | The Evaluator is a **binary executor**, not a scorer; the termination oracle is an empty Failure Ledger, not a score threshold |
| `reference/autonomy-quality-protocol.md` | Intent contract (Q1-Q3), producer ≠ verifier (Q9), evidence-bound claims (Q10), Acceptance Provenance (Q15) | Q10 is native: every cell verdict carries a repro, and unexercised cells are `DROPPED`, never implied-pass |
| `_common/PROPORTION_AND_SPACING.md` | Evidence tiers (§1), touch targets, measure, reflow numbers | Tier 1-2 numbers become pass criteria; Tier 4 folklore may never be one (§6) |
| `reference/doc-quality-protocol.md` | W1-W12 for the delivered proof document | W12 applies to the Operability Proof itself |
| `reference/verdict-gate.md` | — | `N/A` — crucible delivers a proof, not a which-feature verdict |
| `_common/ADVERSARIAL_REFUTATION.md` | — | `N/A` **with reason**: the oracle is binary and reproducible, so a skeptic panel adds no information an independent re-run does not already provide. The Phase 4 fresh-executor re-run is the refutation |

## 10. Decision Tree vs Neighbors

```
Is the question "does the task finish?" (operability) or "is it good?" (quality)?
  QUALITY → runway (flagship ceiling) / restyle (standard bar) / kaizen (one feature vs a metric)
  OPERABILITY ↓
Does the task fail under IDEAL conditions?
  YES → bug (crucible's Phase 2 routes this out by contract)
  NO ↓
Is the scope the interface, or the system behind it?
  SYSTEM (load, chaos, resilience) → siege skill
  INTERFACE ↓
Is one named accessibility fix already identified?
  YES → palette skill direct (minimum viable chain)
  NO  → crucible — declare → reduce → baseline → trial ⟲ → independent full re-run → prove
```
