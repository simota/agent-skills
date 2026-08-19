# Recipe: `runway` — Flagship UI design tournament

**Purpose:** Flagship UI design tournament — parallel design directions → persona-panel judging → ceiling convergence (all rubric dims = 3) for the surfaces that define the product. The **design member of the Quality-Max family**: where `summit` maximizes strategic *code* quality via engine triangulation and `podium` maximizes *content* quality, `runway` maximizes the **visible design quality of a flagship surface** — top page, core product screen, first-run onboarding — by competing N orthogonal design directions against each other and converging the winner to the rubric ceiling. Not an Improve-family iteration: `restyle` refines one direction to a standard bar (all dims ≥ 2); `runway` stages a tournament and targets **all dims = 3**.

**Read when:** Executing the `runway` Recipe.

---

## Invocation & target resolution

```
/nexus runway <surface>          # scope: the flagship screen / component / flow to maximize
/nexus runway                    # no target → Nexus proposes flagship candidates (by visibility × brand weight), user picks ONE
```

- `runway` always operates on **one surface per run** — the tournament cost only pays off on a surface that defines the product. Multi-surface asks are split into sequential runs (or routed to `restyle` when standard bar suffices).
- A `restyle` run whose ✓direction-gate surfaces **multiple strong competing directions** escalates here — that tie is runway's entry signal.

**Default Mode:** `AUTORUN_FULL` after the Phase 0 gate — but Phase 0 itself is unconditional (below).

---

## Termination Bound

Convergence **loop ≤ 3 cycles (default 3)**. Exit reasons use the canonical vocabulary:

| Exit reason | Runway-specific meaning |
|-------------|------------------------|
| `ACCEPT` / `target-met` | **all rubric dims = 3** (the ceiling — raised from restyle's target-score bar; intentional parity with wish's Ceiling ACCEPT) |
| `diminishing-returns (Δ < ε)` | weighted score Δ < 0.2 between cycles (`evaluator-loop-protocol.md` values verbatim) — an honorable exit when the ceiling is out of reach; report which dims plateaued and why |
| `cap-reached` | 3 cycles without ceiling ACCEPT |
| `BLOCK` | un-fixable within scope (e.g. the surface's premise is wrong → recommend Flux reframe or `feature`), or Agent Tennis — escalate |

On any non-`ACCEPT` exit the recipe reports best-so-far + the residual gap per rubric dimension.

## Confirm / Safety Gate

- **Phase 0 Framing: Confirm before launch — always** (unconditional; intentional parity with `summit`/`wish` gates, not drift). The prompt surfaces: the chosen surface, the tournament plan (3 directions), the estimated cost envelope (4-10× `feature`), and — when the ask is really a single-direction polish — an explicit recommendation of the cheaper path (`restyle`).
- **✓rubric-gate** (end of Phase 1): the Design Ceiling Rubric (dims + score-3 anchors) is presented before the tournament spends. Contract-level checkpoint; AUTORUN cannot skip — the rubric *is* the termination oracle and judging standard for everything downstream.
- Standard **Ask First** tiers apply unchanged: brand-level token changes, 10+ files.
- On a Fable 5 hub the Phase 0 gate subsumes the F8 cost gate — one confirmation, not two.

## Resume

**Checkpoint-resume** (≥ 4 phases; `runway resume`): persist the Ceiling Rubric at Phase 1 exit; at Phase 2 exit persist **the winning direction's full prototype + Design Brief plus the salvage-list content** (never re-run the tournament on resume); persist each cycle's per-dimension score trajectory at each Phase 3 cycle boundary.

---

## Chain template

```
Phase 0  FRAMING ★Confirm-before-launch (always)
         Nexus[surface selection + tournament plan + cost envelope
              + cheaper-path recommendation when single-direction polish suffices → restyle]
   ▼
Phase 1  GROUND ‖ (Echo[persona walkthrough + friction baseline] ‖ Palette[heuristics + a11y baseline]
         ‖ Compete[competitor surface benchmark] +Frame?[Figma context] +Voice?[user signals])
         → Vision drafts the Design Ceiling Rubric (4-6 dims, task-specific score-3 anchors,
           reachability-checked by Magi) → ✓rubric-gate ★contract-level
   ▼
Phase 2  TOURNAMENT ‖ 3 orthogonal directions [brand-led / usability-led / trend-led — replaced
         by surface-specific axes when GROUND surfaces them], each direction:
         Vision[direction brief] → Forge[prototype] + Muse[token sketch]
         → judge panel = Echo×personas ‖ Palette ‖ Magi[brand-fit], scoring vs the frozen Rubric
         → winner + salvage list (informal cherry-pick from runners-up, fed to Phase 3 cycle 1)
   ▼
Phase 3  CONVERGE ⟲{ IMPLEMENT (Artisan[components/styles] ‖ Flow?[motion] ‖ Muse[token-first]
                     ‖ Ink?[icons/assets])
                     → EVALUATE (Echo[re-walkthrough vs rubric] + Palette[a11y ≥ baseline]
                     + Radar[no-regression]) }⟲  loop ≤ 3 cycles (default 3)
   ▼
Phase 4  VERIFY (Voyager?[visual regression + responsive] + Judge[multi-engine diff review])
   ▼
Phase 5  SHIP (Guardian[phased commits + PR embedding the Runway Board])
```

Engine routing follows summit principles: **Codex owns code-gen** (Artisan / Flow / Muse-apply / Ink / Forge), **Claude owns judgment** (Echo / Palette / Vision / Magi / Judge / Guardian). Parallel branch ownership per `_common/PARALLEL.md` — tournament directions and Phase 3 sub-surfaces never share mutable state.

## Phase contract

- **Phase 1 GROUND (parallel)** — Echo/Palette establish the quantified friction + a11y baseline (entry condition for Phase 3, as in restyle); Compete benchmarks the surface against best-in-class competitors so score-3 anchors are grounded in observed exemplars, not vibes. Vision synthesizes into the **Design Ceiling Rubric**: 4-6 dims (e.g. hierarchy, craft, motion, consistency, brand expression, emotional impact), each with a task-specific score-3 anchor; Magi sanity-checks reachability before the ✓rubric-gate freezes it.
- **Phase 2 TOURNAMENT (parallel)** — three independent Vision direction briefs from orthogonal angles; each direction gets a Forge prototype (hero-state fidelity, not full build) + Muse token sketch. The judge panel is the **same Evaluator roster Phase 3 will use** (Echo personas, Palette, Magi brand-fit), scoring against the frozen Rubric — panel and loop share one standard. Winner promoted; runners-up mined for a salvage list.
- **Phase 3 CONVERGE (the loop)** — evaluator-loop machinery per `reference/evaluator-loop-protocol.md`: implement cluster = Generator, Echo/Palette = independent Evaluators (Generator-excluded), Rubric = single termination oracle. **Muse token-first rule** and **a11y ≥ baseline** and **Radar no-regression** are hard gates every cycle, inherited from restyle discipline.
- **Phase 4 VERIFY** — Voyager visual-regression/responsive pass when a browser harness exists; Judge multi-engine review of the final diff (producer ≠ verifier, Q9).
- **Phase 5 SHIP** — Guardian phased commits; PR embeds the Runway Board.

---

## The eight contract elements

| # | Element | Contract |
|---|---------|----------|
| 1 | Termination bound | `loop ≤ 3 cycles (default 3)`; exits `ACCEPT` (all dims = 3) · `diminishing-returns (Δ < ε)` · `cap-reached` · `BLOCK`. Non-`ACCEPT` exits report best-so-far + residual gap per dimension. |
| 2 | Confirm / safety gate | Phase 0 Framing: **Confirm before launch — always** (intentional parity with summit/wish). ✓rubric-gate: contract-level checkpoint; AUTORUN cannot skip. Standard **Ask First** on brand-token changes / 10+ files. |
| 3 | Resume | **checkpoint-resume** (6 phases; `runway resume` — Rubric, winning prototype + salvage list, and score trajectory persisted at phase/cycle boundaries). |
| 4 | Output report | Named **Runway Board** — per-direction tournament score comparison, salvage-from-losers record, per-cycle score trajectory per dimension, a11y result vs baseline, exit reason + residual gap, Before/After captures. |
| 5 | Failure Modes Prevented | Consolidated section below. |
| 6 | Boundaries / vs neighbors | Section below + Decision Tree. |
| 7 | Scale | **12-30 agents × ≤3 cycles, 4-10× cost** (tournament ≈ 9-12 agents · converge ≈ 4-6/cycle · verify ≈ 2-4). |
| 8 | Shared-protocol refs | `reference/evaluator-loop-protocol.md` (Generator-Evaluator separation, Δ < 0.2, single oracle; ACCEPT raised to all dims = 3); `_common/PARALLEL.md` (tournament + implement ownership); `reference/autonomy-quality-protocol.md` (intent contract Q1-Q3, producer ≠ verifier Q9, Acceptance Provenance Q15). Verdict/refutation/parity protocols: `N/A` (no verdict claim, no reproduction claim). |

## Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Premature convergence on the first plausible direction | Tournament: 3 orthogonal directions independently prototyped and panel-judged before any full build (Phase 2) |
| "Best design" left undefined → taste-driven judging | Design Ceiling Rubric frozen at ✓rubric-gate with task-specific score-3 anchors grounded in Compete benchmarks (Phase 1) |
| Beauty regressing usability or accessibility | Echo friction score must improve AND Palette a11y ≥ baseline — hard gate every cycle (Phase 3) |
| Presentation change breaking behavior contracts | Radar no-regression is a hard gate every cycle — runway changes presentation, never contracts (Phase 3) |
| Token-system erosion via one-off flagship styling | Muse token-first rule: recurring values tokenized before Artisan writes ad-hoc styles (Phase 3) |
| Tournament cost spent on a non-flagship surface | Phase 0 gate surfaces cost + recommends `restyle` when single-direction polish suffices; one surface per run |
| Judge panel and loop applying different standards | The Phase 2 judge panel IS the Phase 3 Evaluator roster, both scoring the same frozen Rubric |
| Losing good ideas from losing directions | Salvage list mined from runners-up, fed as input to converge cycle 1 (Phase 2) |
| Unbounded pursuit of an unreachable ceiling | `loop ≤ 3 cycles (default 3)` + honorable diminishing-returns exit with per-dim plateau reporting |
| Generator grading its own work | GAN separation per `evaluator-loop-protocol.md`; Phase 4 Judge is a fresh multi-engine verifier (Q9) |

## Boundaries

- **vs `restyle`** — restyle refines **one direction** to a **standard bar** (rubric target scores, all dims ≥ 2 semantics) at medium cost; runway competes **multiple directions** and targets the **ceiling (all dims = 3)** at 4-10× cost. Escalation path: a restyle ✓direction-gate with multiple strong competing directions → runway. De-escalation: a runway ask on a non-flagship surface → restyle.
- **vs `summit`** — summit is the multi-engine tournament for strategic *code*; runway is the tournament for *visible design*. A flagship surface needing both deep logic and design maximization → summit with a Vision-led design team, or sequential summit → runway.
- **vs `podium`** — podium maximizes *content* (docs/slides); runway maximizes *product UI*.
- **vs `marquee`** — marquee is the acquisition-side sibling: a **conversion-driven landing page** with CRO/SEO/Trust as first-class rubric dims and machine oracles (Lighthouse/CWV). Runway = **in-product flagship surface** where conversion is not the organizing dimension. LP ask → marquee.
- **vs `wish`** — wish is deliverable-agnostic with a Scarcity Gate; runway is design-specialized with **no Scarcity Gate** (flagship-surface maximization is a repeatable, legitimate need — intentional difference, stated to prevent drift). A wish whose deliverable is a flagship UI surface may route its generator through runway's tournament.
- **vs `kaizen`** — kaizen improves one feature against a quantified metric target; runway maximizes design quality against a ceiling rubric.
- **vs `vision` / `atelier` / `funnel[premium]` skills** — vision direct = direction only, no execution; atelier = full design-to-impl pipeline (prototypes/assets/persistent design system) without tournament or ceiling semantics; bazaar = the LP studio pipeline (marquee's substrate, not runway's).

### Decision Tree

```
Maximize the design quality of something?
├─ landing page / acquisition surface (conversion is the point) → marquee
├─ docs / slides / content → podium
├─ strategic code (logic-heavy) → summit
├─ product UI surface
│  ├─ not flagship / standard bar (≥ 2) suffices → restyle
│  ├─ direction decision only → vision direct
│  ├─ pipeline-wide design system + assets → atelier skill
│  └─ flagship surface, ceiling quality, multiple directions worth competing → runway ✓
└─ deliverable-agnostic "most important ask of my life" → wish
```

## Add-ons

+Flux at GROUND when the surface's premise (not execution) is the problem · +Vector/vitrine for Before/After visual-evidence capture in the Runway Board · +Field for real-user research beyond persona simulation · +Experiment to A/B the shipped winner against the old surface when traffic allows · +Canon for formal WCAG conformance.
