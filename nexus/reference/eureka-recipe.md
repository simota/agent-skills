# Eureka Recipe — Novelty-Proven Invention

> `/nexus eureka "<problem or domain>"` — the **invention** recipe: dissolve a contradiction that current solutions accept as given, and **prove the result is new** against a cited prior-art record rather than assuming it. Wish-class in cost and rigor; where `wish` maximizes the *execution* of a known deliverable, `eureka` establishes that the deliverable is *worth existing at all* — novel, valuable, buildable, defensible, and yours to build.

Read this file before executing the `eureka` Recipe.

---

## 1. Nature / When to Use / Boundaries

**The roster could recombine but not invent.** `graft` transplants a concept that already works elsewhere. `fuse` synthesizes products that already exist. `killer` picks the strongest differentiator from a candidate set nobody checked for novelty. `spark` proposes features from data and logic already in the repo. `gedanken` reasons about a claim without producing an artifact. Each is useful, and none of them ever asks the question that decides whether something is an invention: **has this already been done, and if not, why has nobody done it?**

Eureka's identity is five things no sibling carries together:

1. **Contradiction extraction** — an invention is what dissolves a trade-off that everyone else treats as a law of nature. Phase 1 names the contradiction explicitly ("faster *requires* more expensive"), because a problem statement that does not name one usually describes a task, not an invention opportunity.
2. **Prior-Art Ledger** — a cited, tiered record of what already exists, **inverted in polarity from every other sweep in the roster**: `clone` researches to *reproduce*, `wish` researches to *reach*, `eureka` researches to *avoid*. It is the denominator novelty is measured against, and no candidate survives without a stated delta from its nearest neighbor in it.
3. **Failure archaeology** — the sweep's highest-value output is not what exists but **what was tried and abandoned, and why**. Those reasons are the real constraints. An invention that has not beaten them is a repeat of a known failure, which is the most expensive kind of "novel."
4. **Reduction to practice** — the minimum artifact that demonstrates the mechanism, built **falsification-first**: the spike is designed to kill the mechanism, not to demo it. This is the line between an invention and an idea, and it is a contract-level requirement, not an optional add-on.
5. **Pentad Gate** — novelty · value · feasibility · defensibility · **freedom-to-operate**. Four of these exist scattered across other recipes; FTO exists nowhere, and an invention blocked by someone else's rights is not an asset regardless of how good it is.

### Use `eureka` for

- A standing constraint the team has stopped questioning — "this is just how it works in our domain."
- A deliberate search for a defensible, non-obvious mechanism: a technical approach, a product mechanic, an algorithm, a process, a business model.
- Work where being *first* matters and being *wrong about being first* is expensive.
- A request framed as invention: "invent something," "is there a genuinely new way," "nobody has solved this."

### Not this — route to

| Not this | Route to | Why |
|----------|----------|-----|
| Transplant a mechanism that demonstrably works in another domain | `graft` | Known-good concept, host-fit is the work — eureka *uses* transplant as one of six generators, but its output must still clear the Novelty Gate |
| Synthesize a product from ≥2 existing sources | `fuse` | Recombination of known surfaces, no novelty claim |
| Decide **which** differentiator to bet on, from candidates already in hand | `killer` | Verdict on a known set; no prior-art proof, no reduction to practice |
| Propose features from existing data/logic | `spark` (skill) | Feature ideation inside the known solution space |
| Reason rigorously about a claim, no artifact | `gedanken` | Thought experiment; eureka must build something that can fail |
| Reframe a stuck problem, single pass | `flux` (skill) | One reframing lens; eureka runs six generators and proves the survivor |
| Maximize the execution quality of a **known** deliverable | `wish` | Execution ceiling, not novelty |
| Build a thing whose direction is already settled | `spec` → `apex` | No novelty question to answer — the invention gates would be pure overhead |

**Build the invention once it is proven** is *not* routed out: it is `eureka ship=true` (§1a), the opt-in continuation that carries the ratified mechanism through `spec` → `apex` in one run.

### 1a. Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus eureka "<problem or domain>"` | **Invention-only (default, `ship=false`).** Phases 0-8; stops at the Invention Dossier + a recommended handoff. |
| `/nexus eureka "<...>" ship=true` | **End-to-end.** Phases 0-8, then the **Ship Gate (Phase 8.5)** and, only if all six preconditions hold, Phases 9-12: specify → build → **novelty regression check** → ship. |

`ship=true` is **opt-in and never inferred** — an invention ask is not automatically a build ask, and the recipe's own Phase 0 gate exists to catch invention framing on routine work. Two envelopes are declared separately (invention / build); the build envelope is confirmed at Phase 8.5, not at Phase 0, because its size only becomes knowable once the mechanism is settled.

The continuation **collapses rather than repeats**: `spec` enters with the Invention Handoff Packet (§6a) and its FRAME/EXPAND/CHALLENGE phases become validation, exactly as `apex` collapses when it consumes a Spec Handoff Packet (`reference/apex-recipe.md` § Input Contracts). Re-running Riff/Flux/Magi/Void over a mechanism already killed-or-survived at Phases 3, 4 and 6 is drift (Q7), not diligence.

**Scale: 22-55 agents × ≤3 cycles (+1 re-ideation), 9-24× `feature` cost.** Per-phase: P0-P1 ≈ 2 · P1.5 ≈ 4-8 (prior-art sweep is the heaviest research phase in the roster) · P2 ≈ 6-9 (six generators, cross-engine) · P3 ≈ 2-4 · P4 ≈ 5-7 (pentad, parallel) · P5 ≈ 2-5 (spike) · P6 ≈ 4-6 Evaluators/cycle + 2-3 skeptics · P7-P8 ≈ 2. **`ship=true` adds +10-28** (P9 ≈ 2-4 collapsed spec · P10 ≈ 8-25 apex · P11 ≈ 1 Attest) → **combined 32-83 agents, 13-33× `feature` cost, ≈ 1.5× the invention-only run**. **Confirm-before-launch always** (wish-class parity; the Phase 0 framing gate is that confirmation) **with a declared budget envelope**; `ship=true` confirms a **second** time at the Ship Gate.

**Model selection (Plan-and-Execute):** Phase 1 crystallization, Phase 3 novelty adjudication, and the Phase 4 pentad verdicts are judgment-heavy → plan-tier (opus / Fable 5). Generators, evaluators, skeptics, and the Phase 5 spike → Sonnet 5 default. The Phase 2 generator pool is **cross-engine** (§4). Under `ship=true`, Phase 9's AC authoring is plan-tier (the novelty delta must survive translation into an AC) and Phase 10 inherits apex's own model map unchanged.

---

## 2. Termination Bound

Convergence **`loop ≤ N cycles (default N=3)`**, plus at most **one full re-ideation** (return to Phase 2 with the failure reasons as added constraints) — hard total 4 passes through the loop. Exit reasons use the canonical vocabulary:

| Exit reason | Eureka-specific meaning |
|-------------|------------------------|
| `ACCEPT` / `target-met` | all five rubric dimensions = 3 on calibrated evaluators → *candidate ACCEPT*; the skeptic panel then ratifies (surviving attacks = 0) or demotes to REVISE. The rubric is the single termination oracle; the panel ratifies inside it |
| `diminishing-returns (Δ < ε)` | weighted score Δ < 0.2 between cycles (`evaluator-loop-protocol.md` verbatim); survivors > 0 → **plateau-with-open-attacks**, reported with every open attack listed |
| `cap-reached` | cycles exhausted without a ratified invention → deliver the best candidate with its unmet dimensions named |
| `budget-reached` | envelope ceiling hit → best-so-far + residual gap, never a silent overrun |
| `BLOCK` | escalate. Two named sub-reasons, both **legitimate deliveries, not failures**: **`prior-art saturation`** (every candidate collided with cited prior art across both ideation passes) and **`FTO blocked`** (the surviving mechanism is likely encumbered — §5) |

**`ship=true` does not extend the invention loop.** The cap stays `loop ≤ 3 cycles` + one re-ideation; the build inherits `apex`'s own bounds and budget envelope, and the two never trade against each other — a build overrun exits `budget-reached` on the **build** envelope and delivers the frozen dossier plus partial implementation, never re-opens the invention. Only an `ACCEPT` exit reaches Phase 9 (§3); every other exit reason ends the run at Phase 8 with its dossier, which is the invention-only delivery and a complete one.

**A `BLOCK (prior-art saturation)` run still ships its Invention Dossier.** The Prior-Art Ledger and the failure archaeology are the expensive part of this recipe, and "here is everything that has been tried in this space, here is why each attempt failed, and here is why the obvious next move is not new" is a genuinely valuable answer to "invent something." Delivering it as a null result rather than forcing a weak invention is the honest exit — and a run that produces it has told the user something they could not have known cheaply.

## 3. Confirm / Safety Gate

- **Phase 0 framing gate: Confirm before launch — always** (unconditional, intentional parity with `wish`/`summit`). Surfaces: the declared contradiction, the budget envelope, the estimated prior-art sweep breadth, and — when the request is a **known solution to a known problem** — a recommendation to route to `feature`/`spark`/`graft` instead. Invention framing on routine work is this recipe's inflation risk, and the gate is where it is caught.
- **Phase 1 Contradiction Crystallization: contract-level checkpoint; AUTORUN cannot skip.** A contradiction the user does not recognize as theirs produces an invention nobody wanted.
- **Phase 1.5 Prior-Art ratification: contract-level.** The user confirms the ledger's scope before it becomes the novelty denominator — a sweep that missed the obvious neighbor makes every downstream novelty verdict wrong, and that is cheap to catch here and expensive to catch at Phase 7.
- **Phase 5 reduction-to-practice: Ask First** whenever the spike touches anything real (external services, production data, credentials, cost-bearing resources). A spike is an experiment, and experiments get the same blast-radius treatment as any other write.
- **FTO finding: Ask First, and stop the autonomous path.** §5 states the boundary: this is a **research signal, not legal advice**, and a likely-blocking right is surfaced to the user for a human decision, never worked around or silently discounted.
- **Phase 8.5 Ship Gate (`ship=true` only): Confirm before launch — unconditional; blocks in `AUTORUN`/`AUTORUN_FULL`.** The first gate approved spending on an *invention*; this one approves spending on a *product*, and the two are different decisions made on different information. All six preconditions must hold, checked in order — the first miss ends the run at Phase 8 and delivers the dossier with the failed precondition named:

  | # | Precondition | Why a miss forbids building |
  |---|--------------|------------------------------|
  | ① | Exit reason = `ACCEPT` | `cap-reached` / `budget-reached` / plateau-with-open-attacks / `BLOCK` all mean the invention was *not* ratified — building one is committing to an unfinished verdict |
  | ② | Surviving skeptic attacks = 0 | An open refutation is an unpriced risk; the build would make it expensive to act on |
  | ③ | FTO carries no likely-blocking signal | Building on likely-encumbered rights is strictly worse than not building; per §5 this stops the autonomous path regardless of `ship=true` |
  | ④ | ENABLEMENT = 3 | A mechanism only its inventor can build cannot be handed to a spec — the Phase 9 translation would silently reinvent it |
  | ⑤ | Spike survived falsification (Phase 5) | A falsified mechanism has no reduction to practice to build from |
  | ⑥ | A **separate build budget envelope** is declared and confirmed | The invention envelope is already spent; an implicit build budget is how a 9-24× run becomes a 33× one unannounced |

- **Phase 9 spec translation: contract-level checkpoint; AUTORUN cannot skip.** One question only — *does this spec still describe the invention?* The rest of `spec`'s dialogue is collapsed (§1a), so this is the single place a mechanism→spec mistranslation is catchable before code exists.
- **Phase 10 build: apex's own gates run unchanged.** Consuming an upstream packet removes *re-derivation*, never *verification* (`apex-recipe.md` § Input Contracts contract rule). The Risk Gate, acceptance verification, and Ask First tiers apply as they would in a standalone apex run.
- Standard Ask First tiers (L4 security / destructive / 10+ files) apply unchanged.

## 4. Resume

**Checkpoint-resume:** persist the Invention Contract + contradiction at Phase 1 exit; **the Prior-Art Ledger + failure archaeology at Phase 1.5 exit** (it is the single most expensive artifact in the run, and a re-swept ledger would silently move the novelty denominator, invalidating every earlier verdict); the full candidate set with per-candidate novelty verdicts at Phase 3 exit; spike code and results at Phase 5 exit; per-cycle scores and surviving attacks at each Phase 6 boundary. A re-ideation pass **reuses the persisted ledger** rather than re-sweeping.

**`ship=true` adds one checkpoint and one freeze.** The Invention Dossier is **frozen at the Ship Gate** and is never re-opened by a downstream phase — a build that discovers a problem returns to Phase 9 (spec revision) or stops, but it may not edit the novelty verdict that authorized it. A run interrupted during the build resumes at **Phase 9 or 10 against the frozen dossier**; Phases 1.5-7 never re-run, because a re-swept ledger would move the novelty denominator under a decision already made on the old one.

---

## 5. Phase Contract (AUTORUN chain template)

```
Phase 0   FRAMING GATE ★Confirm-before-launch (always)
          Nexus[classify: is this an invention ask or a known-solution ask?] + budget envelope
          → known solution to a known problem → recommend feature / spark / graft (override journaled)
   ▼
Phase 1   CONTRADICTION CRYSTALLIZATION ★contract-level dialogue (plan-tier)
          Plea[who suffers, and what they do today] ‖ Flux[what is assumed to be fixed]
          → name the CONTRADICTION explicitly: "<better X> requires <worse Y>" — the trade-off the
            domain accepts as a law. No contradiction nameable → this is a task, not an invention;
            say so and route out.
          → INVENTION CONTRACT: contradiction · who it binds · what "dissolved" looks like ·
            non-goals · constraint budget (what may NOT be spent: cost, latency, complexity, trust)
   ▼
Phase 1.5 PRIOR-ART SWEEP ★contract-level ratification      [inverted polarity: research to AVOID]
          deep-research ‖ Compete ‖ Canon? ‖ Seek? — sweep patents/applications, papers, standards,
          OSS implementations, shipped products, and ADJACENT INDUSTRIES that face the same
          contradiction under a different name (per reference/research-grounding.md, tiers reweighted
          per §6 below — for prior art, patents and peer-reviewed work outrank vendor claims)
          → PRIOR-ART LEDGER (cited, tiered, per-claim verified) = the NOVELTY DENOMINATOR
          → FAILURE ARCHAEOLOGY: for each abandoned attempt, WHY it failed (physics / economics /
            adoption / timing / regulation). These become Phase 2 constraints and Phase 4 value tests.
          → ✓user ratifies ledger scope ("is the obvious neighbor in here?") → ledger freezes
   ▼
Phase 2   IDEATION DIVERGENCE ‖ six STRUCTURALLY-DIFFERENT generators, cross-engine where the hub
          allows (one generator per (engine, heuristic) pair — different priors, not just different
          prompts). Each generator states its output as a MECHANISM (how it works), never a wish:
          ① contradiction-dissolution — separate the trade-off in time / space / condition / scale
          ② cross-domain transplant  — Flux/graft-mechanism: who else solved this contradiction?
          ③ constraint inversion     — what becomes possible if the binding constraint were free,
                                       or 10× worse (forcing a different architecture)?
          ④ first-principles rebuild — discard the incumbent decomposition, rebuild from the physics
                                       / economics / user job upward
          ⑤ scaling-law extrapolation— what is newly possible at 10× cheaper/faster/more abundant
                                       that was uneconomic when the incumbents were designed?
          ⑥ latent-need inversion    — Plea: the workaround users built themselves IS the spec
          → candidate mechanisms (typically 8-15 raw, deduplicated to 4-8 distinct mechanisms)
   ▼
Phase 3   NOVELTY GATE — every candidate diffed against the frozen Prior-Art Ledger (plan-tier)
          per candidate → nearest prior art (cited) + the DELTA, verdict:
            COLLISION   → killed WITH THE CITATION (the recipe's core discipline; a kill here is
                          the cheapest possible outcome and is recorded, never quietly dropped)
            INCREMENTAL → survives ONLY if the increment is the load-bearing part of the value
            NOVEL       → advances
          **A candidate that cannot state how it differs from its nearest prior art is not an
          invention — it is an unexamined idea, and it is killed as such.**
          → all candidates COLLISION → one re-ideation (Phase 2 with failure archaeology as added
            constraints); a second exhaustion exits BLOCK (prior-art saturation) WITH the dossier
   ▼
Phase 4   PENTAD GATE ‖ five independent axes (survive all five, or die named)
          NOVELTY        Attest/Judge — re-verify the Phase 3 delta adversarially, not on trust
          VALUE          Plea ‖ Compete ‖ Rank — does dissolving THIS contradiction matter, to whom,
                         and enough to change behavior? (the failure archaeology's "nobody adopted
                         it" reasons are re-run as tests here)
          FEASIBILITY    Atlas ‖ Forge — reduction-to-practice SKETCH: buildable with available
                         means, on what budget, with what unknowns
          DEFENSIBILITY  Compete — moat class + time-to-copy, per _common/ADVERSARIAL_REFUTATION.md
                         and killer's discipline: buildable-emergent moats are NOT auto-downgraded
          FTO            Clause — is the mechanism likely encumbered by others' rights?
                         **Research signal, not legal advice** (§ boundary below)
   ▼
Phase 5   REDUCTION TO PRACTICE ★the line between invention and idea
          Forge/Builder[the MINIMUM artifact that demonstrates the mechanism] — a spike, a computed
          model, a measured demo. NOT the product.
          **Falsification-first:** the spike is designed to KILL the mechanism. Its success criterion
          is stated BEFORE it runs, and Radar (not the builder) judges the result — the mechanism
          survives only if a genuine attempt to break it failed.
          → mechanism falsified → back to Phase 2 (within the re-ideation budget) or BLOCK
   ▼
Phase 6   GAUNTLET-CONVERGE loop ≤ 3 cycles (evaluator-loop-protocol.md; ceiling ACCEPT per §2;
          Generator excluded from Evaluators)
          rubric dims: NOVELTY · VALUE · FEASIBILITY · DEFENSIBILITY · ENABLEMENT
          calibration : the NEAREST PRIOR ART is the natural calibration set — it must score
                        NOVELTY 0 and FEASIBILITY 3 (it exists). An evaluator that scores the
                        nearest prior art above 0 on novelty is miscalibrated and is re-prompted
                        before it may score a candidate (wish §7 discipline, prior-art-anchored)
          skeptics   ‖: refute-polarity panel once all dims ≥ 2 — "this is prior art [citation]",
                        "nobody will change behavior for this", "it cannot be built at that budget",
                        "a competitor copies it in a quarter"
   ▼
Phase 7   DISCLOSURE — state the invention so someone else can build it
          Scribe/Accord[Disclosure Package]: mechanism · claims (what is being asserted as new) ·
          enabling detail · prior-art delta with citations · reduction-to-practice evidence ·
          known limitations · FTO notes. ENABLEMENT is a scored rubric dimension precisely because
          an invention only its inventor can build is not yet transferable.
   ▼
Phase 8   DELIVER — Invention Dossier + handoff: spec (specify it) → apex (build it) ·
          killer (if it is a product bet needing a go/no-go) · graft (if a variant should be
          transplanted elsewhere) · clause (if the user wants real legal review)
          → ship=false (default) → RUN ENDS HERE
   ▼
══════════ ship=true only — the opt-in end-to-end continuation ══════════════════════════════
   ▼
Phase 8.5 SHIP GATE ★Confirm-before-launch (unconditional; blocks in AUTORUN_FULL)
          Six preconditions, ALL required (§3 table): ACCEPT exit · 0 surviving attacks · no
          blocking FTO signal · ENABLEMENT=3 · spike survived · separate build envelope declared.
          → any miss → END AT PHASE 8 with the dossier and the failed precondition NAMED
          → all hold → FREEZE the dossier (never re-opened downstream) + emit the
            INVENTION HANDOFF PACKET (§6a)
   ▼
Phase 9   SPECIFY — spec, entered with the packet: FRAME ‖ EXPAND ‖ CHALLENGE COLLAPSE TO
          VALIDATION (the direction was chosen at Phase 3 and adversarially refuted at Phases 4
          and 6 — re-running Riff/Flux/Magi/Void over a ratified mechanism is drift, not diligence)
          Accord/Scribe[L3 ACs, plan-tier]:
            · the Phase 5 FALSIFICATION CRITERION becomes an AC verbatim
            · the NOVELTY DELTA is written in as a MUST-HAVE AC — a *testable requirement*, never
              a description in a preamble. This is what makes it defensible at Phase 11.
            · constraint budget → non_goals; FTO notes → declared constraint, not re-litigated
          ★contract-level checkpoint (one question): does this spec still describe the invention?
          → Spec Handoff Packet (spec-recipe.md § Handoff contract) + the NOVELTY INVARIANT
   ▼
Phase 10  BUILD & SHIP — apex consuming the Spec Handoff Packet (its Phases 1-4 collapse per
          apex-recipe.md § Input Contracts). Apex's gates run UNCHANGED — a consumed packet
          removes re-derivation, never verification. The invention adds exactly one constraint:
          **NOVELTY INVARIANT** — the load-bearing delta may not be simplified, deferred, or
          scoped out. A scope cut that removes it is a GATE FAILURE that returns to Phase 9,
          not a trade-off the build may make on its own.
          **The spike is EVIDENCE, NOT A FOUNDATION.** It was built to be killed, not extended;
          production re-derives from the Disclosure Package. Promoting spike code is forbidden.
   ▼
Phase 11  NOVELTY REGRESSION CHECK ★before ship
          Attest[does the SHIPPED artifact still embody the CLAIMED mechanism?] — checked against
          the frozen Disclosure Package claims by an agent that did not build it (Q9).
          → eroded → back to Phase 10 with the eroded claim named
          → eroded a second time → SHIP THE BUILD WITH THE NOVELTY CLAIM RETRACTED and say so in
            the dossier. An honest feature beats a false invention claim, and a silently-eroded
            claim is the one failure this whole recipe exists to prevent.
   ▼
Phase 12  DELIVER — frozen Invention Dossier + apex Delivery Report + Novelty Regression verdict
```

**Phase 1.5 — prior-art tier reweighting.** `reference/research-grounding.md` owns the sweep contract (tiered sources, per-claim verification, cited ledger). Eureka's specialization is the **polarity and the weighting**: prior art is strongest where it is most examined, so **patents/applications, peer-reviewed papers, and standards outrank vendor claims and marketing** — the inverse of the fidelity sweeps, where first-party product docs sit at T1. A vendor's "world's first" is T2 *intent* and never settles novelty. Adjacent-industry search is mandatory, not optional: the same contradiction is usually named differently in another field, and that is where the cheapest collision is found.

**Phase 2 — generator independence.** Six heuristics is the point: three prompts to one model produce three framings of one set of priors, and invention is exactly the task where priors are the constraint. Distribute across engines where the hub allows (`_common/CLI_COMPATIBILITY.md §4`); a single-engine run **declares the monoculture** in the dossier. Generators do not see each other's output before submitting — cross-pollination happens at Phase 3, after each has committed.

**Phases 9-11 — why the continuation is not just "then run apex".** Three things change when a build follows an invention, and all three are the reason this lives inside `eureka` rather than as a suggested next command. (a) **The delta is the deliverable.** A normal build optimizes for shipping; an invention build must ship *the weird part*, and the weird part is exactly what a builder under time pressure simplifies away first. The Novelty Invariant + Phase 11 regression check make that erosion a gate failure instead of an unnoticed one. (b) **The verdict must not follow the code.** Freezing the dossier at the Ship Gate stops the build from retroactively softening the novelty claim to match what got built. (c) **The spike is a trap.** It is the nearest thing to working code and it was deliberately built to fail — treating it as a starting point imports a design chosen for falsifiability, not for production.

**FTO boundary (contract-level).** The FTO axis produces a **research signal**: "this mechanism resembles claims in `<cited right>`; a human should review before commercial commitment." It is **not legal advice**, never a clearance opinion, and never a basis for designing around a specific claim. A likely-blocking finding stops the autonomous path and surfaces to the user (§3). Recording "no blocking art found in this sweep" is permitted; recording "this is clear to practice" is not.

## 6. Output Report — **Invention Dossier** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Invention Contract** — the contradiction, who it binds, what "dissolved" means, constraint budget, each element classified per Acceptance Provenance (Q15)
- **Prior-Art Ledger** — cited entries by tier, sweep breadth (domains and adjacent industries covered), and what the user ratified as in-scope
- **Failure archaeology** — prior attempts, why each failed, and how the surviving mechanism beats that reason (or why the reason no longer holds)
- **Candidate field** — every candidate with its generator heuristic, engine, nearest prior art, delta, and verdict (`COLLISION` kills are listed **with their citations** — a killed candidate is evidence, not waste)
- **Pentad results** — per axis: verdict + evidence; FTO stated as a research signal with its boundary
- **Reduction to practice** — what was built, the falsification criterion declared **before** the run, the result, and who judged it
- **Score trajectory** — per-cycle per-dimension scores + the prior-art calibration record (nearest prior art scored 0 on novelty by each evaluator)
- **Gauntlet ledger** — refutations raised / killed / survived-then-fixed; open attacks listed on any plateau exit
- **Disclosure Package** — mechanism, claims, enabling detail, limitations
- **Exit reason** (§2) + residual gap + budget spent vs envelope
- **Handoff** — recommended next recipe with the packet it carries

**Under `ship=true`** the delivery adds, in this order: the **Ship Gate record** (each of the six preconditions with its verdict — including on a refusal, where the failed precondition is the delivery), the **apex Delivery Report** (its own named report, unchanged), and the **Novelty Regression verdict** (`intact` | `repaired-in-cycle-2` | `RETRACTED`, with the eroded claim named on anything but `intact`). The dossier is emitted **even when the build fails** — the invention was proven before the build began, and a failed implementation does not un-prove it.

### 6a. Invention Handoff Packet (`ship=true`, emitted at Phase 8.5)

Machine-consumable, mirroring the Spec Handoff Packet's shape so Phase 9 consumes it without re-parsing prose:

| Field | Content | Consumed by |
|-------|---------|-------------|
| `mechanism` | the Disclosure Package's mechanism statement | Phase 9 problem statement + direction — **pre-settled, not re-elicited** |
| `contradiction` + `binds_whom` | the Phase 1 Invention Contract | Phase 9 FRAME validation (replaces the Plea/Socratic pass) |
| `novelty_delta` + `nearest_prior_art` (cited) | the load-bearing difference and what it differs *from* | Phase 9 **must-have AC**; Phase 10 Novelty Invariant; Phase 11 regression oracle |
| `falsification_criterion` + `spike_result` | what would have killed the mechanism, and that it did not | Phase 9 AC verbatim; Phase 10 verification set |
| `constraint_budget` | what may NOT be spent (cost, latency, complexity, trust) | `non_goals` → scope bound on every downstream spawn (P8) |
| `fto_notes` | the research signal + its boundary | Phase 10 declared constraint — carried, never re-litigated as legal advice |
| `prior_art_ledger_ref` | the frozen ledger + failure archaeology | Phase 10 Risk Gate input (each abandoned attempt's failure reason is a pre-mortem entry) |
| `residual_gap` | anything the invention run left unmet | Decision Ledger seed (Q4-Q6) — never silently dropped |

**Contract rule (inherited):** Phase 9/10 **do not re-open the settled invention**. A build that finds the mechanism unbuildable as specified returns to Phase 9, and if Phase 9 cannot spec it without dissolving the delta, the run stops and reports — it never quietly ships the generic version.

## 7. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Reinventing something that already ships** | Prior-Art Ledger as the novelty denominator + Phase 3 kill-with-citation; no candidate advances without a stated delta |
| **Repeating a known failure** ("nobody does this" because it was tried and it failed) | Failure archaeology at Phase 1.5; the reasons become Phase 2 constraints and Phase 4 value tests |
| **Novelty for its own sake** (new, and nobody cares) | Pentad VALUE axis + the adoption-failure reasons re-run as tests |
| **Science fiction** (novel, valuable, unbuildable) | Pentad FEASIBILITY sketch + Phase 5 reduction to practice as a contract requirement |
| **Trivially copyable "invention"** | Pentad DEFENSIBILITY (moat class + time-to-copy), buildable-emergent moats not auto-downgraded |
| **Invention blocked by someone else's rights** | Pentad FTO axis as a research signal + Ask First stop; nothing else in the roster asks this |
| **Idea mistaken for invention** (a claim with no artifact) | Phase 5 falsification-first spike, judged by Radar rather than its builder |
| **Demo-driven self-deception** (the spike was built to succeed) | Falsification criterion declared before the run; producer ≠ judge (Q9) |
| **An invention only its inventor can build** | ENABLEMENT as a scored rubric dimension + the Phase 7 Disclosure Package |
| **Generator monoculture** (six prompts, one set of priors) | Six structurally-different heuristics, cross-engine distribution, no cross-pollination before commitment; monoculture declared when unavoidable |
| **Novelty grading inflation** (everything looks new to a generous evaluator) | Prior-art-anchored calibration: the nearest prior art must score NOVELTY 0 / FEASIBILITY 3, or the evaluator is re-prompted |
| **Contradiction never named** → a task dressed as an invention | Phase 1 requires an explicit "<better X> requires <worse Y>"; unnameable → route out |
| **Invention framing on routine work** | Phase 0 gate recommends `feature`/`spark`/`graft` when the ask is a known solution to a known problem |
| **A null result thrown away** | `BLOCK (prior-art saturation)` still ships the dossier — the ledger and failure archaeology are the run's most valuable artifact |
| **Unbounded search for a breakthrough** | `loop ≤ 3` + exactly one re-ideation + budget envelope with `budget-reached` best-so-far delivery |
| **FTO signal mistaken for legal clearance** | §5 boundary: research signal only, "no blocking art found in this sweep" permitted, "clear to practice" forbidden |
| **Novelty erosion during the build** (`ship=true`) — the load-bearing delta is simplified away and a generic feature ships under an invention's name | Novelty Invariant at Phase 10 (a scope cut removing the delta is a gate failure, not a trade-off) + Phase 11 regression check by a non-builder + `RETRACTED` as an honest terminal verdict |
| **The verdict follows the code** — the novelty claim is softened after the fact to match what got built | Dossier **frozen** at the Ship Gate; no downstream phase may edit the novelty verdict that authorized it |
| **Spike promoted to production** — a design chosen for falsifiability becomes the architecture | Phase 10 contract: the spike is evidence, not a foundation; production re-derives from the Disclosure Package |
| **Building an unratified invention** | Ship Gate precondition ①②⑤ — only an `ACCEPT` exit with zero surviving attacks and a surviving spike reaches Phase 9 |
| **Building on encumbered rights** | Ship Gate precondition ③ — a likely-blocking FTO signal stops the continuation, not just the autonomous path |
| **Silent cost escalation from invention into product** | `ship=true` is opt-in and never inferred; a **second** unconditional confirm with a **separate** build envelope (precondition ⑥) |
| **Re-running settled discovery** (invention proven, then spec re-brainstorms it) | Phase 9 collapses FRAME/EXPAND/CHALLENGE against the Invention Handoff Packet; re-litigating a ratified mechanism is drift (Q7) |

## 8. Shared-Protocol References

| Protocol | What eureka takes from it | Eureka-specific specialization |
|----------|--------------------------|-------------------------------|
| `reference/research-grounding.md` | Tiered sources, per-claim verification, cited Evidence Ledger | **Inverted polarity** (research to avoid, not reproduce) + prior-art tier reweighting (patents/papers over vendor claims) + mandatory adjacent-industry search + failure archaeology as a required output |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, score scale, aggregation, Δ < 0.2 | Ceiling ACCEPT (all 5 dims = 3) with prior-art-anchored calibration |
| `_common/ADVERSARIAL_REFUTATION.md` | Skeptic panel, evidence-vs-novelty, polarity, aggregation, exclusions | Target claim = "this is new, wanted, buildable, and defensible"; the protocol's **unproven-because-new** rule is load-bearing here — an invention cannot be refuted for lacking evidence that can only exist after it is built |
| `reference/dialogue-protocol.md` | Question craft, Assumption Ledger, checkpoint presentation | Contradiction extraction is **eureka-original**, built on its question-craft rules |
| `reference/verdict-gate.md` | Verdict card, Yes/No/Modify, flag + KPI + kill criterion | Applied at the Phase 8 handoff when the invention is carried forward as a product bet (the `killer` path) |
| `reference/autonomy-quality-protocol.md` | Intent contract (Q1-Q3), producer ≠ verifier (Q9), evidence-bound claims (Q10), Acceptance Provenance (Q15) | Q9 applied twice: Radar judges the spike it did not build, and the skeptic panel is generator-excluded |
| `_common/CLI_COMPATIBILITY.md` §4 | Per-engine model map and spawn prerequisites | The six-generator cross-engine distribution resolves against it |
| `reference/doc-quality-protocol.md` | W1-W12 for document deliverables | The Disclosure Package is a document deliverable; ENABLEMENT subsumes W12 and adds transferability |
| `reference/spec-recipe.md` § Handoff contract | Spec Handoff Packet schema + the "downstream does not re-open settled decisions" contract rule | `ship=true` Phase 9: entered *with* the Invention Handoff Packet (§6a), so FRAME/EXPAND/CHALLENGE collapse to validation; the novelty delta is added as a **must-have AC** |
| `reference/apex-recipe.md` § Input Contracts | Packet-consuming collapse of apex Phases 1-4; "a packet removes re-derivation, never verification" | `ship=true` Phase 10: apex's gates run unchanged, plus one eureka-only constraint — the **Novelty Invariant**, enforced by the Phase 11 regression check |

## 9. Decision Tree vs Neighbors

```
Is the ask "find/create something genuinely NEW", with novelty that must hold up?
  NO ↓
    known solution to a known problem?          → feature / spark
    a mechanism proven elsewhere, port it here? → graft
    combine ≥2 existing products?               → fuse
    pick the best bet from candidates in hand?  → killer
    reason about a claim, no artifact?          → gedanken
    maximize execution of a known deliverable?  → wish
  YES ↓
Can you name the contradiction it dissolves ("<better X> requires <worse Y>")?
  NO  → it is a task or a preference, not an invention — route out and say why
  YES ↓
Is being FIRST load-bearing (and being wrong about first, expensive)?
  NO  → graft / spark are cheaper and sufficient
  YES → eureka — crystallize the contradiction → prior-art ledger + failure archaeology
        → six-generator divergence → novelty gate (kill with citations) → pentad gate
        → falsification-first reduction to practice → gauntlet-converge → disclosure → deliver
          ↓
        Do you also want it BUILT in this run?
          NO  → ship=false (default) — dossier + handoff; run spec → apex later if it earns it
          YES → ship=true — Ship Gate (6 preconditions, second confirm, separate build envelope)
                → collapsed spec → apex → novelty regression check → ship
                (any precondition missed → ends at the dossier, precondition named)
```
