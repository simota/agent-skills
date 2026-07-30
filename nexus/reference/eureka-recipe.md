# Eureka Recipe — Novelty-Proven Invention

> `/nexus eureka "<problem or domain>"` — the **invention** recipe: dissolve a contradiction that current solutions accept as given, and **prove the result is both new and not the ordinary next move** against a cited prior-art record rather than assuming it. Wish-class in cost and rigor; where `wish` maximizes the *execution* of a known deliverable, `eureka` establishes that the deliverable is *worth existing at all* — new, non-ordinary, valuable, buildable, and defensible.

Read this file before executing the `eureka` Recipe.

---

## 1. Nature / When to Use / Boundaries

**The roster could recombine but not invent.** `graft` transplants a concept that already works elsewhere. `fuse` synthesizes products that already exist. `killer` picks the strongest differentiator from a candidate set nobody checked for novelty. `spark` proposes features from data and logic already in the repo. `gedanken` reasons about a claim without producing an artifact. Each is useful, and none of them ever asks the question that decides whether something is an invention: **has this already been done, and if not, why has nobody done it?**

### What `eureka` means by "invention"

A **breakthrough way of solving a problem, that is not a routine move and does not quietly charge the bill somewhere else.** Three conditions, all required, and nothing else:

1. **It dissolves the problem in a way current practice does not** — not a margin on how the problem is already handled, but a different way of getting the result. Operationalized as the Phase 1 contradiction.
2. **It is not the obvious next step** — new against what already exists (Phase 3 `COLLISION` test) *and* not the move a competent practitioner working this problem would reach as a matter of course (Phase 3 `OBVIOUS` test). "New" without this second half is how a routine substitution gets called an invention.
3. **The sacrifice is gone, not relocated** — a mechanism that improves X without worsening Y, while silently paying in complexity, operational burden, trust, another stakeholder's time, or *later* (technical debt, lock-in), has **re-priced** the trade-off rather than dissolved it. A relocation is legitimate only when it is **accounted and lands on an axis the Invention Contract declared free** — trading memory for latency when memory is genuinely free is exactly generator ③'s work. An **unaccounted** payment is a kill. Operationalized as the Phase 4 **Sacrifice Ledger** gate.

Conditions 1-2 make it *new*; condition 3 makes it *real*. Most "breakthroughs" that survive scrutiny for a quarter and then get reverted failed condition 3, not the first two: the cost did not vanish, it moved to a column nobody was reading.

**The frame is engineering, not law.** *Prior art*, *enablement*, and *reduction to practice* are used here in their plain engineering sense: what already exists, whether someone else can build it from the write-up, whether it was actually built and tested. The recipe borrows the *discipline* of examined novelty and nothing else — rights, licensing and patentability are **out of scope at every phase** (route those to `clause`; see the Not-this table).

Eureka's identity is six things no sibling carries together:

1. **Contradiction extraction** — an invention is what dissolves a trade-off that everyone else treats as a law of nature. Phase 1 names the contradiction explicitly ("faster *requires* more expensive"), because a problem statement that does not name one usually describes a task, not an invention opportunity.
2. **Prior-Art Ledger** — a cited, tiered record of what already exists, **inverted in polarity from every other sweep in the roster**: `clone` researches to *reproduce*, `wish` researches to *reach*, `eureka` researches to *avoid*. It is the denominator both Phase 3 tests are measured against: no candidate survives without a stated delta from its nearest neighbor in it (`COLLISION`), **and** no candidate survives if that delta is a routine move from the same ledger (`OBVIOUS`). The ledger is what makes "not ordinary" checkable instead of asserted.
3. **Failure archaeology** — the sweep's highest-value output is not what exists but **what was tried and abandoned, and why**. Those reasons are the real constraints. An invention that has not beaten them is a repeat of a known failure, which is the most expensive kind of "novel."
4. **Reduction to practice** — the minimum artifact that demonstrates the mechanism, built **falsification-first**: the spike is designed to kill the mechanism, not to demo it. This is the line between an invention and an idea, and it is a contract-level requirement, not an optional add-on.
5. **Blind ordinariness test** — novelty alone lets a routine substitution pass as an invention, so every candidate also faces the **Routine-Move Test**: a pre-committed panel proposes the ordinary next moves *before any candidate exists*, so "anyone would have done this" is settled by reproduction rather than by hindsight. Nothing else in the roster asks whether a new thing is also a **non-ordinary** thing. Survivors then clear the **Tetrad Gate** — novelty · value · feasibility · defensibility — four axes that exist scattered across other recipes but are nowhere gated together.
6. **Sacrifice accounting** — the trade-off the invention claims to dissolve is checked for **relocation**, across every axis a real system pays on, including *time* (paid later) and *other people* (paid by someone not in the room). A candidate that merely moved the cost is not an invention, and the ledger is what makes "nothing was sacrificed" a checked claim instead of a sales line. This is why a **free lunch raises scrutiny rather than confidence** here: the usual explanation for one is an axis nobody counted.

### Use `eureka` for

- A standing constraint the team has stopped questioning — "this is just how it works in our domain."
- A deliberate search for a defensible, non-obvious mechanism: a technical approach, a product mechanic, an algorithm, a process, a business model.
- Work where being *first* matters and being *wrong about being first* is expensive.
- A request framed as invention: "invent something," "is there a genuinely new way," "nobody has solved this."

### Not this — route to

| Not this | Route to | Why |
|----------|----------|-----|
| Transplant a mechanism that demonstrably works in another domain | `graft` | Known-good concept, host-fit is the engineering work, and `graft` makes no novelty claim. `eureka` uses transplant as one of six generators and judges the result as a **composite** (mechanism + local adaptation) against a domain-scoped denominator — so a transplant survives only when **the adaptation itself is non-ordinary** (Phase 3 `OBVIOUS` test). Routine import → route to `graft` |
| Synthesize a product from ≥2 existing sources | `fuse` | Recombination of known surfaces, no novelty claim |
| Decide **which** differentiator to bet on, from candidates already in hand | `killer` | Verdict on a known set; no prior-art proof, no reduction to practice |
| Propose features from existing data/logic | `spark` (skill) | Feature ideation inside the known solution space |
| Reason rigorously about a claim, no artifact | `gedanken` | Thought experiment; eureka must build something that can fail |
| Reframe a stuck problem, single pass | `flux` (skill) | One reframing lens; eureka runs six generators and proves the survivor |
| Maximize the execution quality of a **known** deliverable | `wish` | Execution ceiling, not novelty |
| Build a thing whose direction is already settled | `spec` → `apex` | No novelty question to answer — the invention gates would be pure overhead |
| Rights, licensing, patentability, freedom to operate | `clause` (skill) | **Out of scope.** `eureka` judges novelty and non-ordinariness as engineering facts; no phase of it produces or is competent to produce a legal conclusion |

**Build the invention once it is proven** is *not* routed out: it is `eureka ship=true` (§1a), the opt-in continuation that carries the ratified mechanism through `spec` → `apex` in one run.

### 1a. Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus eureka "<...>" depth=scout` | **Novelty scout (light).** Phases 1 → 1.5 → 2′ (3 generators) → 3, then stop. Delivers a **Novelty Scout Report**, not an Invention Dossier: candidates with `COLLISION`/`OBVIOUS`/`NOVEL` verdicts and their evidence, but **no proof** — no tetrad, no spike, no convergence, and `ACCEPT` is unreachable by construction. **11-14 agents, 3-5× `feature` cost, one confirmation point.** |
| `/nexus eureka "<problem or domain>"` | **Invention-only (default, `ship=false`).** Phases 0-8; stops at the Invention Dossier + a recommended handoff. |
| `/nexus eureka "<...>" ship=true` | **End-to-end.** Phases 0-8, then the **Ship Gate (Phase 8.5)** and, only if all five preconditions hold, Phases 9-12: specify → build → **novelty regression check** → ship. |

The three forms are one escalation ladder — *is it new?* → *is it an invention?* → *build it* — and each rung is priced separately so the cheap question never carries the expensive question's bill. **`depth=scout` and `ship=true` are mutually exclusive**: a scout cannot ratify an invention, so it can never satisfy Ship Gate ①, and the combination is refused with that reason rather than silently upgraded.

**`depth=scout` — what it is for, and what it must never be read as.** The question "has someone already done this?" is worth answering on its own, and until now the roster answered it only inside a 32-62-agent run: `spark`/`graft`/`feature` are cheaper but **none of them judges novelty**, which left "just check whether this is new" with no proportionate owner. Scout is that owner. Its contract:

- **Phases:** 1 (contradiction, plan-tier) → 1.5 (prior-art sweep, single-pass — adjacent-industry search still mandatory, failure archaeology recorded but not exhaustive) → 2′ (**3** generators instead of six: contradiction-dissolution · cross-domain transplant · first-principles rebuild, ‖ a **2-agent** blind ordinary-move panel) → 3 (both novelty tests) → deliver.
- **One confirmation point**, not three: the Phase 1 contradiction and the Phase 1.5 ledger scope are ratified **together** at the sweep's exit. There is **no unconditional Phase 0 launch gate** — the always-confirm rule exists because a wish-class run is expensive, and at 3-5× it is not. The Phase 0 *triage* still runs, as a one-line declaration (invention question vs known-solution question → route out), just without a stop.
- **No loops, no re-ideation, no spike.** Phases 4-8 do not exist here, so §2's cycle budget is not merely unspent — it is inapplicable.
- **Exits (two only):** `NOVEL-CANDIDATES` — *n* candidates survived with stated, cited deltas, every one labelled **UNPROVEN** · `SATURATED` — everything died `COLLISION` or `OBVIOUS`, with the citations and panel proposals as evidence. **Neither is an `ACCEPT`**, and a scout survivor is never described as an invention: it is a candidate that has not yet been refuted, valued, sketched for feasibility, **audited for a relocated sacrifice (Phase 4's Sacrifice Ledger)**, or built. A scout answers definition conditions **1 and 2 only** (§1) — condition 3 is untested there, which is why a scout result can look like a free lunch and still be one that has never been priced.
- **Promotion is cheap by design.** A full run started from a scout **re-enters at Phase 2 against the frozen ledger** — the sweep is never re-run (§4's rule: a re-swept ledger silently moves the novelty denominator), the scout's 2-agent panel proposals carry forward and are topped up to the full 3-agent panel (blindness is preserved: the panel never saw a candidate), and the scout's adjudicated candidates enter the full field with their verdicts intact. Promotion therefore costs the *remaining* phases: **+21-46 agents** — derived as 3 more generators (3-6) + Phase 3 re-adjudication incl. the panel top-up (3-4) + P4 (5-8) + P5 (2-5) + P6 (6-21) + P7-8 (2), floor **21**, ceiling **46** — not a fresh 32-62. **Scout + promotion (32-60) is therefore never more expensive than the full run (32-62)**, which is what makes the cheap rung safe to try first rather than a gamble.

`ship=true` is **opt-in and never inferred** — an invention ask is not automatically a build ask, and the recipe's own Phase 0 gate exists to catch invention framing on routine work. Two envelopes are declared separately (invention / build); the build envelope is confirmed at Phase 8.5, not at Phase 0, because its size only becomes knowable once the mechanism is settled.

The continuation **collapses rather than repeats**: `spec` enters with the Invention Handoff Packet (§6c) and its FRAME/EXPAND/CHALLENGE phases become validation, exactly as `apex` collapses when it consumes a Spec Handoff Packet (`reference/apex-recipe.md` § Input Contracts). Re-running Riff/Flux/Magi/Void over a mechanism already killed-or-survived at Phases 3, 4 and 6 is drift (Q7), not diligence.

**Scale: 32-62 agents × ≤3 cycles (+1 re-ideation), 9-24× `feature` cost.** Per-phase: P0-P1 ≈ 2 · P1.5 ≈ 4-8 (prior-art sweep is the heaviest research phase in the roster) · P2 ≈ 6-9 (six generators, cross-engine) · P3 ≈ 5-7 (both tests: novelty diff + the 3-agent blind ordinary-move panel, which launches at Phase 2 but is costed here) · P4 ≈ 5-8 (tetrad + the Sacrifice Ledger gate: Void, ‖ Omen and the `FREE-LUNCH` skeptic at the ceiling) · P5 ≈ 2-5 (spike) · P6 ≈ 4-6 Evaluators **per cycle** + 2-3 skeptics (run-wide) · P7-P8 ≈ 2. **`ship=true` adds +11-30** (P9 ≈ 2-4 collapsed spec · P10 ≈ 8-25 apex · P11 ≈ 1 Attest) → **combined 43-92 agents, 13-33× `feature` cost, ≈ 1.3-1.5× the invention-only run**.

*Range derivation (keep reconciled when a phase figure changes):* floor = 1 cycle → 2+4+6+5+5+2+(4+2)+2 = **32**; ceiling = 3 cycles → 2+8+9+7+8+5+(6×3+3)+2 = **62**. The stated range is the sum of the per-phase figures for a **single ideation pass**, not an independent estimate. The one permitted re-ideation re-runs Phases 2-5 — P2 + P3 (including a fresh ordinary-move panel) + P4 + P5 — adding **≈ 18-28 agents** on top of the stated range; remaining Phase 6 cycles are already budgeted (§2). **Confirm-before-launch always** (wish-class parity; the Phase 0 framing gate is that confirmation) **with a declared budget envelope**; `ship=true` confirms a **second** time at the Ship Gate. **`depth=scout` is the one exception to always-confirm** — its derivation is P1 ≈ 1-2 · P1.5 ≈ 3-4 · P2′ ≈ 5 (3 generators + 2-agent panel) · P3 ≈ 2-3 → floor **11**, ceiling **14**, and at that price the launch gate costs more than the run it guards.

**Model selection (Plan-and-Execute):** Phase 1 crystallization, Phase 3 novelty adjudication, and the Phase 4 tetrad verdicts are judgment-heavy → plan-tier (opus / Fable 5). Generators, evaluators, skeptics, and the Phase 5 spike → Sonnet 5 default. The Phase 2 generator pool is **cross-engine** (§4). Under `ship=true`, Phase 9's AC authoring is plan-tier (the novelty delta must survive translation into an AC) and Phase 10 inherits apex's own model map unchanged.

---

## 2. Termination Bound

Convergence **`loop ≤ N cycles (default N=3)`**, plus at most **one full re-ideation** (return to Phase 2 with the failure reasons as added constraints).

**`depth=scout` has no loop at all.** It runs Phases 1 → 1.5 → 2′ → 3 once and exits `NOVEL-CANDIDATES` or `SATURATED` (§1a) — the cycle budget, the re-ideation, `ACCEPT`, `cap-reached` and `BLOCK` are **inapplicable, not merely unused**. One exit reason below does survive: **`budget-reached`** — a scout whose envelope runs out mid-sweep delivers the partial ledger and whatever verdicts exist, labelled as a **partial denominator** so no absence of a collision is read as evidence of novelty.

**Two returns, one cycle budget.** The Phase 6 convergence cycles and the Phase 2 re-ideation are different loops, and they are bounded by one shared counter so the run cannot silently double:

- The Phase 6 cycle count is **run-wide, not per candidate set**. A re-ideation delivers a fresh candidate field but **does not reset the counter** — cycles already spent stay spent.
- A re-ideation is therefore permitted only while **≥ 1 Phase 6 cycle remains**; with the budget exhausted, the triggering condition exits instead (`cap-reached` at Phase 6, `BLOCK (prior-art saturation)` at Phase 3, `BLOCK` at Phase 5).
- **Both** re-ideation triggers — Phase 3 total collision and Phase 5 falsification — draw on the **same single** re-ideation, whichever fires first.

Hard ceiling for the whole run: **3 Phase 6 cycles + 1 pass back through Phases 2-5**, never 3 cycles *per* ideation.

**An accepted Pivot Advisory (§6a) does not buy cycles.** Which budget it draws on depends on what it changes, and none of the three options is silent: a **scope widening** (ledger re-swept as a delta, contradiction unchanged) is charged to the research envelope and re-freezes the ledger; a **constraint change** (contradiction unchanged, Phase 2 constraints replaced) consumes **the one re-ideation** like any other return; a **re-stated contradiction** invalidates the frozen ledger and every verdict measured against it, so it is **a new run under a new envelope**, confirmed as such (§3) — never a continuation that keeps the old counters.

Exit reasons use the canonical vocabulary:

| Exit reason | Eureka-specific meaning |
|-------------|------------------------|
| `ACCEPT` / `target-met` | all five rubric dimensions = 3 on calibrated evaluators → *candidate ACCEPT*; the skeptic panel then ratifies (surviving attacks = 0) or demotes to REVISE. The rubric is the single termination oracle; the panel ratifies inside it |
| `diminishing-returns (Δ < ε)` | weighted score Δ < 0.2 between cycles (`evaluator-loop-protocol.md` verbatim); survivors > 0 → **plateau-with-open-attacks**, reported with every open attack listed |
| `cap-reached` | cycles exhausted without a ratified invention → deliver the best candidate with its unmet dimensions named |
| `budget-reached` | envelope ceiling hit → best-so-far + residual gap, never a silent overrun |
| `BLOCK` | escalate. One named sub-reason, and it is a **legitimate delivery, not a failure**: **`prior-art saturation`** (across both ideation passes every candidate either collided with cited prior art or was an ordinary move — the space is exhausted *and* the exhaustion is evidenced) |

**`ship=true` does not extend the invention loop.** The cap stays `loop ≤ 3 cycles` + one re-ideation; the build inherits `apex`'s own bounds and budget envelope, and the two never trade against each other — a build overrun exits `budget-reached` on the **build** envelope and delivers the frozen dossier plus partial implementation, never re-opens the invention. Only an `ACCEPT` exit reaches Phase 9 (§3); every other exit reason ends the run at Phase 8 with its dossier, which is the invention-only delivery and a complete one.

**A `BLOCK (prior-art saturation)` run still ships its Invention Dossier.** The Prior-Art Ledger and the failure archaeology are the expensive part of this recipe, and "here is everything that has been tried in this space, here is why each attempt failed, and here is why the obvious next move is not new" is a genuinely valuable answer to "invent something." Delivering it as a null result rather than forcing a weak invention is the honest exit — and a run that produces it has told the user something they could not have known cheaply.

## 3. Confirm / Safety Gate

**`depth=scout` collapses this section to one stop:** the combined contradiction + ledger-scope ratification at Phase 1.5 exit. No launch gate, no separate Phase 1 checkpoint, no Ship Gate (the mode cannot reach it), and no Phase 5 spike gate (there is no spike). The Pivot Advisory rule below applies unchanged — it is the cheapest place in the recipe to learn the framing is wrong. Standard Ask First tiers still apply. Everything else in this section describes the full run.

- **Phase 0 framing gate: Confirm before launch — always** (unconditional, intentional parity with `wish`/`summit`). Surfaces: the declared contradiction, the budget envelope, the estimated prior-art sweep breadth, and — when the request is a **known solution to a known problem** — a recommendation to route to `feature`/`spark`/`graft` instead. Invention framing on routine work is this recipe's inflation risk, and the gate is where it is caught.
- **Phase 1 Contradiction Crystallization: contract-level checkpoint; AUTORUN cannot skip.** A contradiction the user does not recognize as theirs produces an invention nobody wanted.
- **Phase 1.5 Prior-Art ratification: contract-level.** The user confirms the ledger's scope before it becomes the novelty denominator — a sweep that missed the obvious neighbor makes every downstream novelty verdict wrong, and that is cheap to catch here and expensive to catch at Phase 7.
- **Acting on a Pivot Advisory: contract-level checkpoint; AUTORUN cannot skip.** Emitting one is free and non-blocking (§6a); *adopting* one that re-states the frozen contradiction or re-scopes the frozen Prior-Art Ledger invalidates every novelty verdict measured against them, so it needs the user's word — and the run never re-frames itself silently. Declining is journaled in the Decision Ledger and the run continues on the declared framing. A `WRONG-RECIPE` advisory is the one case that recommends **leaving** eureka; it too is the user's call, never an automatic route-out mid-run.
- **Phase 5 reduction-to-practice: Ask First** whenever the spike touches anything real (external services, production data, credentials, cost-bearing resources). A spike is an experiment, and experiments get the same blast-radius treatment as any other write.
- **Phase 8.5 Ship Gate (`ship=true` only): Confirm before launch — unconditional; blocks in `AUTORUN`/`AUTORUN_FULL`.** The first gate approved spending on an *invention*; this one approves spending on a *product*, and the two are different decisions made on different information. All five preconditions must hold, checked in order — the first miss ends the run at Phase 8 and delivers the dossier with the failed precondition named:

  | # | Precondition | Why a miss forbids building |
  |---|--------------|------------------------------|
  | ① | Exit reason = `ACCEPT` | `cap-reached` / `budget-reached` / plateau-with-open-attacks / `BLOCK` all mean the invention was *not* ratified — building one is committing to an unfinished verdict |
  | ② | Surviving skeptic attacks = 0 | An open refutation is an unpriced risk; the build would make it expensive to act on |
  | ③ | ENABLEMENT = 3 | A mechanism only its inventor can build cannot be handed to a spec — the Phase 9 translation would silently reinvent it |
  | ④ | Spike survived falsification (Phase 5) | A falsified mechanism has no reduction to practice to build from |
  | ⑤ | A **separate build budget envelope** is declared and confirmed | The invention envelope is already spent; an implicit build budget is how a 9-24× run becomes a 33× one unannounced |

  Preconditions ①②③④ re-verify facts an `ACCEPT` exit already entails (②③ are inside the §2 ACCEPT definition; ④ gates entry to Phase 6) — **deliberately**: the Ship Gate is a spend gate, and re-checking entailed facts against the frozen record is cheap insurance against a mis-recorded exit. ⑤ is the only genuinely new information at this gate.

- **Phase 9 spec translation: contract-level checkpoint; AUTORUN cannot skip.** One question only — *does this spec still describe the invention?* The rest of `spec`'s dialogue is collapsed (§1a), so this is the single place a mechanism→spec mistranslation is catchable before code exists.
- **Phase 10 build: apex's own gates run unchanged.** Consuming an upstream packet removes *re-derivation*, never *verification* (`apex-recipe.md` § Input Contracts contract rule). The Risk Gate, acceptance verification, and Ask First tiers apply as they would in a standalone apex run.
- Standard Ask First tiers (L4 security / destructive / 10+ files) apply unchanged.

## 4. Resume

**Checkpoint-resume:** persist the Invention Contract + contradiction at Phase 1 exit; **the Prior-Art Ledger + failure archaeology at Phase 1.5 exit** (it is the single most expensive artifact in the run, and a re-swept ledger would silently move the novelty denominator, invalidating every earlier verdict); **the Ordinary-Move Set** (produced blind, before any candidate is known — re-deriving it after the candidates exist would destroy exactly the hindsight-freedom it is built for) and the full candidate set with per-candidate `COLLISION`/`OBVIOUS`/`INCREMENTAL`/`NOVEL` verdicts at Phase 3 exit — **the persisted candidate set and the emitted Idea Ledger (§6a) are the same artifact, one stored and one shown**, so a resumed run never re-derives ideas the user has already seen; **every Pivot Advisory with its outcome** (`accepted`/`declined`/`unanswered`) at each emission boundary, so a resumed run neither re-raises a declined advisory nor loses an unanswered one; spike code and results at Phase 5 exit; per-cycle scores and surviving attacks at each Phase 6 boundary. A re-ideation pass **reuses the persisted ledger** rather than re-sweeping.

**`depth=scout` persists for promotion, not just for resume.** Its ledger, 2-agent panel proposals, and adjudicated Idea Ledger are written at the same boundaries, so a later full run enters at Phase 2 against the frozen artifacts (§1a) instead of re-sweeping — and a scout that is never promoted has still left the expensive artifact behind for the next attempt.

**`ship=true` adds one checkpoint and one freeze.** The Invention Dossier is **frozen at the Ship Gate** and is never re-opened by a downstream phase — a build that discovers a problem returns to Phase 9 (spec revision) or stops, but it may not edit the novelty verdict that authorized it. A run interrupted during the build resumes at **Phase 9 or 10 against the frozen dossier**; Phases 1.5-7 never re-run, because a re-swept ledger would move the novelty denominator under a decision already made on the old one. A Phase 11 `RETRACTED` outcome does **not** edit the frozen dossier: the Ship-Gate-time verdict stands as recorded, and the retraction is a **separate Novelty Regression verdict** layered alongside it (§6) — the freeze rule and the retraction never conflict.

---

## 5. Phase Contract (AUTORUN chain template)

**`depth=scout` runs the marked subset only:** Phase 0 triage without its stop → 1 → 1.5 (the single ★) → 2′ (3 generators, 2-agent panel) → 3 → **Novelty Scout Report**. Phases 4-12 belong to the full run.

```
Phase 0   FRAMING GATE ★Confirm-before-launch (always — declaration only, no stop under depth=scout)
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
          deep-research ‖ Compete ‖ Canon? ‖ Seek? — sweep papers, standards, OSS implementations,
          shipped products, engineering write-ups/talks, and ADJACENT INDUSTRIES that face the same
          contradiction under a different name (per reference/research-grounding.md, tiers reweighted
          per §6 below — peer-reviewed work and standards outrank vendor claims)
          → PRIOR-ART LEDGER (cited, tiered, per-claim verified) = the NOVELTY DENOMINATOR
          → FAILURE ARCHAEOLOGY: for each abandoned attempt, WHY it failed (physics / economics /
            adoption / timing / tech readiness). These become Phase 2 constraints and Phase 4 value
            tests.
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
          ‖ BLIND ORDINARY-MOVE PANEL (3 agents) — launched here, consumed at Phase 3. Given the
            contradiction + the frozen ledger ONLY; never the candidates, never each other.
            Each proposes the top 3 moves a competent practitioner would make from that start.
          → ORDINARY-MOVE SET, frozen before Phase 3 opens (pre-commitment = hindsight immunity)
          ⇥ INTERIM OUTPUT — **IDEA LEDGER v1** (raw): every candidate emitted to the user before any
            gate judges it, deduplication shown rather than silently applied (§6a). Informational,
            NOT a gate — it never blocks AUTORUN and never asks for a selection.
            + **PIVOT ADVISORY** if a detector fires (§6a) — CONTRADICTION-DRIFT / DENOMINATOR-
              CLUSTER / ADOPTION-BLIND / WRONG-RECIPE: "a different direction looks more promising,
              here is the evidence". Emitting is free; ACTING on one that breaks a freeze is ★.
   ▼
Phase 3   NOVELTY GATE — TWO tests against the frozen Prior-Art Ledger (plan-tier)
          "is it new?" AND "is it ordinary?" — a candidate must pass both
          per candidate → nearest prior art (cited) + the DELTA + the ROUTE to that delta, verdict:
            COLLISION   → killed WITH THE CITATION — the delta does not exist (the recipe's core
                          discipline; a kill here is the cheapest possible outcome and is recorded,
                          never quietly dropped)
            OBVIOUS     → killed — the delta exists but is a ROUTINE MOVE from the ledger: a
                          standard combination, a like-for-like substitution, a parameter or scale
                          change, or the step the field was already heading toward. Judged by the
                          ROUTINE-MOVE TEST (see below), never by an evaluator's impression.
            INCREMENTAL → survives ONLY if the increment is the load-bearing part of the value
            NOVEL       → advances
          **A candidate that cannot state how it differs from its nearest prior art is not an
          invention — it is an unexamined idea, and it is killed as such.** A candidate that CAN
          state the difference but whose difference anyone would have reached is not an invention
          either — it is ordinary work, and OBVIOUS is where it is caught.
          ⇥ INTERIM OUTPUT — **IDEA LEDGER v2** (adjudicated): the same ideas with each verdict and
            its evidence attached (§6a). This is the emission that makes the kills legible while the
            run is still cheap to redirect.
            + **PIVOT ADVISORY** — the richest emission point: FRAMING-IS-THE-ORDINARY-MOVE fires
              here when the Ordinary-Move Set covers the WHOLE field (everything OBVIOUS), which
              means re-ideating the same framing would repeat the same death.
          ⇤ depth=scout ENDS HERE → NOVELTY SCOUT REPORT (§6b): exit NOVEL-CANDIDATES (survivors,
            each labelled UNPROVEN) or SATURATED (all killed, with evidence) + promotion estimate
            + SALVAGE LEDGER (§7 — a SATURATED scout is the cheapest field map + route-out there is).
            No tetrad, no spike, no convergence, no ACCEPT — by construction, not by omission.
          → all candidates COLLISION or OBVIOUS → THE one re-ideation (Phase 2 with failure
            archaeology as added constraints), if unspent AND ≥1 Phase 6 cycle remains (§2);
            otherwise, or on a second exhaustion, exit BLOCK (prior-art saturation) WITH the dossier
   ▼
Phase 4   TETRAD GATE ‖ four independent axes (survive all four, or die named)
          NOVELTY        Attest/Judge — re-verify the Phase 3 delta AND its OBVIOUS verdict
                         adversarially, not on trust
          VALUE          Plea ‖ Compete ‖ Rank — does dissolving THIS contradiction matter, to whom,
                         and enough to change behavior? (the failure archaeology's "nobody adopted
                         it" reasons are re-run as tests here)
          FEASIBILITY    Atlas ‖ Forge — reduction-to-practice SKETCH: buildable with available
                         means, on what budget, with what unknowns
          DEFENSIBILITY  Compete — moat class + time-to-copy, per _common/ADVERSARIAL_REFUTATION.md
                         and killer's discipline: buildable-emergent moats are NOT auto-downgraded
          ⌐ GATE, NOT AN AXIS — **SACRIFICE LEDGER** (runs ‖ with the tetrad; binary, never scored)
            Void[what is being paid, and by whom] ‖ Omen?[what is paid LATER] — account every axis:
            cost · latency/throughput · complexity & maintainability · reliability · security ·
            privacy · user effort · ops burden · OTHER STAKEHOLDERS · future debt / lock-in
            verdicts: DISSOLVED           → the sacrifice is gone on every accounted axis
                      DISPLACED-DECLARED  → it moved onto an axis the Phase 1 constraint budget
                                            declared FREE → passes, and the move is stated in the
                                            dossier as part of the mechanism (not a footnote)
                      DISPLACED-HIDDEN    → it moved onto an undeclared axis, or onto one the
                                            constraint budget says may NOT be spent → **KILLED**
                      FREE-LUNCH          → dominates everywhere with nothing relocated → does NOT
                                            pass yet: one extra skeptic runs with a single brief —
                                            "name the axis we failed to count" — and only a failed
                                            search promotes it to DISSOLVED
   ▼
Phase 5   REDUCTION TO PRACTICE ★the line between invention and idea
          Forge/Builder[the MINIMUM artifact that demonstrates the mechanism] — a spike, a computed
          model, a measured demo. NOT the product.
          **Falsification-first:** the spike is designed to KILL the mechanism. Its success criterion
          is stated BEFORE it runs, and Radar (not the builder) judges the result — the mechanism
          survives only if a genuine attempt to break it failed.
          → mechanism falsified → ⇥ **PIVOT ADVISORY** (third and last emission point — what the
            falsification says about the framing, not just about this mechanism), then back to
            Phase 2 on THE one re-ideation, if unspent AND ≥1 Phase 6 cycle remains
            (§2 — Phase 3 and Phase 5 share it); otherwise BLOCK
   ▼
Phase 6   GAUNTLET-CONVERGE loop ≤ 3 cycles (evaluator-loop-protocol.md; ceiling ACCEPT per §2;
          Generator excluded from Evaluators)
          rubric dims: NOVELTY · VALUE · FEASIBILITY · DEFENSIBILITY · ENABLEMENT
                        (the tetrad's four + ENABLEMENT, measurable only after Phase 5 — see below)
          calibration : the NEAREST PRIOR ART is the natural calibration set — it must score
                        NOVELTY 0 and FEASIBILITY 3 (it exists). An evaluator that scores the
                        nearest prior art above 0 on novelty is miscalibrated and is re-prompted
                        before it may score a candidate (wish §7 discipline, prior-art-anchored)
          skeptics   ‖: refute-polarity panel once all dims ≥ 2 — "this is prior art [citation]",
                        "nobody will change behavior for this", "it cannot be built at that budget",
                        "a competitor copies it in a quarter"
          → exit ACCEPT / diminishing-returns / cap-reached / budget-reached per §2
   ▼
Phase 7   DISCLOSURE — state the invention so someone else can build it
          Scribe/Accord[Disclosure Package]: mechanism · claims (what is being asserted as new) ·
          enabling detail · prior-art delta with citations · reduction-to-practice evidence ·
          known limitations. ENABLEMENT is a scored rubric dimension precisely because
          an invention only its inventor can build is not yet transferable.
   ▼
Phase 8   DELIVER — Invention Dossier + handoff: spec (specify it) → apex (build it) ·
          killer (if it is a product bet needing a go/no-go) · graft (if a variant should be
          transplanted elsewhere)
          + **SALVAGE LEDGER (§7)** — every kill and every non-ACCEPT exit routed or explicitly
            discarded: COLLISION → graft/feature (a proven mechanism, citation attached) · OBVIOUS/
            INCREMENTAL → kaizen/optimize · DISPLACED-HIDDEN → feature/kaizen WITH the cost declared,
            or magi if the trade needs an owner · VALUE-fail → killer/compete · FEASIBILITY-fail →
            dated re-check trigger · DEFENSIBILITY-fail → spec→apex as parity work · ENABLEMENT ≤2 →
            scribe/quill until transferable. Recommendation only — never auto-spawned.
          → ship=false (default) → RUN ENDS HERE
   ▼
══════════ ship=true only — the opt-in end-to-end continuation ══════════════════════════════
   ▼
Phase 8.5 SHIP GATE ★Confirm-before-launch (unconditional; blocks in AUTORUN/AUTORUN_FULL)
          Five preconditions, ALL required (§3 table): ACCEPT exit · 0 surviving attacks ·
          ENABLEMENT=3 · spike survived · separate build envelope declared.
          → any miss → END AT PHASE 8 with the dossier and the failed precondition NAMED
          → all hold → FREEZE the dossier (never re-opened downstream) + emit the
            INVENTION HANDOFF PACKET (§6c)
   ▼
Phase 9   SPECIFY — spec, entered with the packet: FRAME ‖ EXPAND ‖ CHALLENGE COLLAPSE TO
          VALIDATION (the direction was chosen at Phase 3 and adversarially refuted at Phases 4
          and 6 — re-running Riff/Flux/Magi/Void over a ratified mechanism is drift, not diligence)
          Accord/Scribe[L3 ACs, plan-tier]:
            · the Phase 5 FALSIFICATION CRITERION becomes an AC verbatim
            · the NOVELTY DELTA is written in as a MUST-HAVE AC — a *testable requirement*, never
              a description in a preamble. This is what makes it defensible at Phase 11.
            · constraint budget → non_goals (scope bound on every downstream spawn)
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

**Phase 1.5 — prior-art tier reweighting.** `reference/research-grounding.md` owns the sweep contract (tiered sources, per-claim verification, cited ledger). Eureka's specialization is the **polarity and the weighting**: prior art is strongest where it is most independently examined, so **peer-reviewed papers, standards, and inspectable implementations (OSS, published benchmarks) outrank vendor claims and marketing** — the inverse of the fidelity sweeps, where first-party product docs sit at T1. A vendor's "world's first" is T2 *intent* and never settles novelty. Adjacent-industry search is mandatory, not optional: the same contradiction is usually named differently in another field. Note what those entries are *for* — a foreign-domain match is **not** an automatic kill (the denominator is domain-scoped; see the Phase 3 composite rule), it is the input that decides whether importing the mechanism here is the ordinary move.

**Phase 2 — generator independence.** Six heuristics is the point: three prompts to one model produce three framings of one set of priors, and invention is exactly the task where priors are the constraint. Distribute across engines where the hub allows (`_common/CLI_COMPATIBILITY.md §4`); a single-engine run **declares the monoculture** in the dossier. Generators do not see each other's output before submitting — cross-pollination happens at Phase 3, after each has committed.

**Phase 3 — the Routine-Move Test (how `OBVIOUS` is decided).** "Would anyone have reached this?" is unanswerable by asking an evaluator who has already seen the answer — hindsight makes every good idea look inevitable. So it is decided by **reproduction, not judgment**:

- A **blind ordinary-move panel** of 3 agents launches **concurrently with the Phase 2 generators** and is given only the **contradiction + the frozen Prior-Art Ledger** — never the candidates, and never each other's output.
- Each proposes the **top 3 next moves** a competent practitioner would make from that starting point. Their union is the **Ordinary-Move Set**, produced *before* any candidate is known and therefore uncontaminated by hindsight.
- At Phase 3 each candidate is matched against the set **semantically, not by wording**. Appearing in **≥ 2 of the 3** proposal sets → `OBVIOUS`, killed, and the matching proposals are recorded as the evidence (the same way a `COLLISION` is recorded with its citation).
- The panel runs **once per ideation pass** — the ledger is frozen, so one set serves every candidate in that pass; a re-ideation runs a fresh panel because its added constraints change what "ordinary" means.

The evidence bar is symmetric with `COLLISION`: a candidate is never killed on an assertion that it is ordinary, only on named proposals that independently reached it.

**Phase 3 — cross-domain candidates are judged as composites.** The novelty denominator is **domain-scoped**: the ledger entries in the *target* domain. A mechanism that exists in another field is **not by itself a `COLLISION`** — the candidate is the composite of *mechanism + the adaptation that makes it work here*, and the delta is stated against that composite. What the foreign entry does is set the bar for the **other** test: if importing it is the routine move — the blind panel proposed it — the candidate dies `OBVIOUS`, not `COLLISION`. This is precisely the `eureka`/`graft` line: `graft` transplants a concept whose host-fit is engineering work and never claims the result is new; `eureka` keeps a transplant only when **the adaptation itself is non-ordinary**, and says so with the panel's output as evidence. The Phase 1.5 adjacent-industry sweep therefore feeds **both** tests — it is raw material, never an automatic kill list.

**Phase 4 → Phase 6 — four axes, then five dimensions.** The Tetrad Gate scores `NOVELTY · VALUE · FEASIBILITY · DEFENSIBILITY`; the convergence rubric scores those four **plus ENABLEMENT**. ENABLEMENT is absent at Phase 4 for a structural reason, not an oversight: transferability can only be judged against a mechanism that has been **reduced to practice**, so it becomes measurable only after Phase 5 and enters at the first scoring gate that follows.

**Phase 4 — why the Sacrifice Ledger is a gate and not a fifth axis.** The question it answers is *accounting*, not *quality*: either every axis a real system pays on has been checked and the payment is where the Invention Contract said it may be, or it has not. Scoring that 0-3 would let a partially-accounted candidate average its way past a hole in the ledger — which is exactly the failure the gate exists to prevent — and would also let an evaluator trade "we sacrificed something significant" against a high novelty score. So it returns one of four verdicts, one of which kills. Two consequences worth stating: (a) **`DISPLACED-DECLARED` is a pass, not a grudging one** — relocating a cost onto an axis that is genuinely free is a legitimate invention mechanism (generator ③'s constraint inversion is built on it), and the recipe refuses to punish it; what it refuses to allow is the relocation going *unstated*, so the move becomes part of the mechanism description in the dossier. (b) **`FREE-LUNCH` raises the bar instead of lowering it** — a candidate that appears to cost nothing anywhere is the single most likely place for an unaccounted axis, so it earns one extra skeptic whose only brief is to find the missing column. A free lunch that survives a dedicated search for its price is the strongest result this recipe can produce; one that is simply never audited is its most expensive failure.

Neither list contains a rights or freedom-to-operate axis, and that is deliberate: **whether someone else holds rights over a mechanism has no bearing on whether it is an invention**, and an evaluator's guess about third-party rights must never be able to push a candidate to `ACCEPT` or hold it back. Rights, licensing and patentability are out of scope for the whole recipe (§1 Not-this → `clause`).

**Phase 6 — ENABLEMENT scale (0-3).** Scored against the candidate's mechanism statement plus its Phase 5 reduction-to-practice record — *not* against the Phase 7 Disclosure Package, which does not exist yet. Phase 7 formalizes what a 3 already demonstrated; it never rescues a lower score.

| Score | Meaning |
|-------|---------|
| **3** | A competent team outside this run could build the mechanism from the stated mechanism + spike record alone. Ship Gate precondition ③ requires this. |
| **2** | Buildable from those, plus bounded clarification on named open points. |
| **1** | Requires tacit context held only by the agents that produced it — the write-up describes *that* it works, not *how*. |
| **0** | Only its inventor can build it: the mechanism is stated as an outcome, with the enabling step missing or hand-waved. |

A candidate scoring ENABLEMENT ≤ 2 can still reach a complete Invention Dossier — enablement is a transferability property, not a novelty one — but it cannot reach `ACCEPT` (which needs all five dims = 3) and therefore cannot reach `ship=true`.

**Phases 9-11 — why the continuation is not just "then run apex".** Three things change when a build follows an invention, and all three are the reason this lives inside `eureka` rather than as a suggested next command. (a) **The delta is the deliverable.** A normal build optimizes for shipping; an invention build must ship *the weird part*, and the weird part is exactly what a builder under time pressure simplifies away first. The Novelty Invariant + Phase 11 regression check make that erosion a gate failure instead of an unnoticed one. (b) **The verdict must not follow the code.** Freezing the dossier at the Ship Gate stops the build from retroactively softening the novelty claim to match what got built. (c) **The spike is a trap.** It is the nearest thing to working code and it was deliberately built to fail — treating it as a starting point imports a design chosen for falsifiability, not for production.

## 6. Output Report — **Invention Dossier** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Invention Contract** — the contradiction, who it binds, what "dissolved" means, constraint budget, each element classified per Acceptance Provenance (Q15)
- **Prior-Art Ledger** — cited entries by tier, sweep breadth (domains and adjacent industries covered), and what the user ratified as in-scope
- **Failure archaeology** — prior attempts, why each failed, and how the surviving mechanism beats that reason (or why the reason no longer holds)
- **Ordinary-Move Set** — the blind panel's proposals, stated as produced *before* any candidate existed. It is a deliverable in its own right: "here is what anyone would have tried" is the map of the ordinary, and it is what makes the surviving mechanism's non-ordinariness legible to a reader who was not in the run
- **Candidate field** — the **final state of the Idea Ledger** (§6a), already emitted mid-run at Phases 2 and 3: every candidate with its generator heuristic, engine, nearest prior art, delta, the route to that delta, and verdict. Kills carry their evidence: `COLLISION` **with its citation**, `OBVIOUS` **with the matching ordinary-move proposals**. A killed candidate is evidence, not waste. Cross-domain candidates state the composite explicitly (foreign mechanism + local adaptation) so the domain-scoped denominator is auditable
- **Pivot Advisory ledger** — every advisory emitted (detector · evidence · proposed re-framing · expected gain · cost) with its outcome: `accepted` (and what it changed), `declined` (with the user's reason), or `unanswered` (emitted, no decision available — the run continued on the declared framing). Omit the subsection only when no detector fired
- **Tetrad results** — per axis (novelty · value · feasibility · defensibility): verdict + evidence
- **Sacrifice Ledger** — every accounted axis with what the mechanism pays on it (including *later* and *whose*), the gate verdict (`DISSOLVED` / `DISPLACED-DECLARED` / `FREE-LUNCH`), and for a declared displacement **which constraint-budget line permitted it**. On `FREE-LUNCH`, the extra skeptic's search and what it failed to find is part of the record — an unaudited free lunch is never reported as one
- **Reduction to practice** — what was built, the falsification criterion declared **before** the run, the result, and who judged it
- **Score trajectory** — per-cycle per-dimension scores + the prior-art calibration record (nearest prior art scored 0 on novelty by each evaluator)
- **Gauntlet ledger** — refutations raised / killed / survived-then-fixed; open attacks listed on any plateau exit
- **Disclosure Package** — mechanism, claims, enabling detail, limitations
- **Exit reason** (§2) + residual gap + budget spent vs envelope
- **Salvage Ledger** (§7) — for every kill and every non-`ACCEPT` exit: `route:<recipe>` with the handover content and a ready-to-run command, or `discard(<reason>)`. ≤ 3 routes, ranked by expected value; **no candidate leaves the run unaccounted**. A `FEASIBILITY`-failed candidate additionally carries its **re-check trigger** (the constraint whose price change would revive it)
- **Handoff** — recommended next recipe with the packet it carries

**Under `ship=true`** the delivery adds, in this order: the **Ship Gate record** (each of the five preconditions with its verdict — including on a refusal, where the failed precondition is the delivery), the **apex Delivery Report** (its own named report, unchanged), and the **Novelty Regression verdict** (`intact` | `repaired-in-cycle-2` | `RETRACTED`, with the eroded claim named on anything but `intact`). The dossier is emitted **even when the build fails** — the invention was proven before the build began, and a failed implementation does not un-prove it.

### 6a. Idea Ledger + Pivot Advisory — the interim emission (contract-level, every run)

The ideas are a deliverable in their own right, not a byproduct of reaching one survivor: Phase 2 typically produces 8-15 raw mechanisms and Phase 3 kills most of them, so a run that only reports the winner throws away the majority of what it paid for — and hides it exactly while a redirect would still be cheap. So the ledger is **emitted mid-run, twice**, in addition to appearing in the final dossier:

| Emission | Where | Contains |
|----------|-------|----------|
| **v1 — raw** | Phase 2 exit, before any gate | Every candidate as generated, pre-judgment. Deduplication is **shown, not silently applied**: merged ideas are listed with what they merged into |
| **v2 — adjudicated** | Phase 3 exit | The same ideas with `COLLISION` / `OBVIOUS` / `INCREMENTAL` / `NOVEL` and each verdict's evidence attached |
| **v3 — re-ideation** | Phase 2 re-entry exit, only if the one re-ideation fires | The fresh candidate field, with the added constraints that produced it named, appended to v2 rather than replacing it |

Per-idea fields (stable across all versions, so v2 reads as a diff of v1):

`id` · `mechanism` (one line, *how it works* — never a wish) · `generator` (which of the six heuristics) · `engine` (which model produced it, so a monoculture is visible) · `dedup_into` (if merged) · then from v2: `nearest_prior_art` (cited) · `delta` · `route_to_delta` · `verdict` · `evidence` (the citation for a `COLLISION`, the matching ordinary-move proposals for an `OBVIOUS`) · **`salvage`** (`route:<recipe>` with what to hand over, or `discard(<reason>)` — per §7; every kill carries one, so a killed idea leaves the run with a destination rather than into a void).

**Contract rules.** (a) **Informational, never a gate** — the emission does not block, does not ask the user to pick, and does not exist in `AUTORUN`/`AUTORUN_FULL` as a stop; the recipe's confirmation points are unchanged (§3). A user *may* redirect after reading one, but nothing waits for them to. (b) **Kills are emitted, not filtered** — a ledger that lists only survivors defeats the purpose; a killed idea plus its evidence is the run's densest output. (c) **Survives interruption** — the ledger is emitted at each boundary and persisted (§4), so a run cancelled at Phase 5 has already delivered its idea field rather than losing it. (d) **No re-scoring** — v2 attaches verdicts already produced by Phase 3; the emission never triggers extra agents, so the scale figures in §1a are unchanged.

#### Pivot Advisory — "a different direction looks more promising, and here is the evidence"

Ideation produces evidence not just about the candidates but about the **framing that produced them**, and that evidence arrives *after* the framing was frozen. A run that notices its direction is the wrong one and grinds to a weak `ACCEPT` anyway has wasted the most expensive thing it bought. So each Idea Ledger emission carries a **Pivot Advisory** whenever a named detector fires on artifacts the run has already produced:

| Detector | Fires when | The pivot it proposes |
|----------|-----------|----------------------|
| `CONTRADICTION-DRIFT` | ≥ 2 of the six generators dissolve a **different** trade-off than the Phase 1 declared one, and the adjacent one scores higher on the Phase 4 VALUE evidence | Re-state the contradiction — the run is solving a neighbor of the stated problem, and the neighbor is the better problem |
| `FRAMING-IS-THE-ORDINARY-MOVE` | the Ordinary-Move Set covers **the whole candidate field** (everything dies `OBVIOUS`) | The framing itself is the routine one: attack a *different* binding constraint, per generator ③'s inversion, rather than re-running the same one |
| `DENOMINATOR-CLUSTER` | every `COLLISION` cites one prior-art cluster, **and** an unswept adjacent field keeps surfacing in the sweep's periphery | Shift or widen the ledger scope before spending another ideation pass against a denominator that is the wrong shape |
| `ADOPTION-BLIND` | the failure archaeology's adoption reasons apply to **every** surviving candidate under this framing, and a named neighboring framing avoids them | Re-frame toward the version prior attempts failed to reach, instead of repeating their failure with a newer mechanism |
| `WRONG-RECIPE` | the highest-value direction turns out to be a routine import (→ `graft`), a known solution (→ `feature`/`spec`), or a pick-from-candidates verdict (→ `killer`) | Route out and stop paying invention-grade cost for work that is not invention — the Phase 0 gate's question, re-asked with evidence that only existed later |

Each advisory states, in this order: **detector · evidence** (candidate ids, ledger citations, or ordinary-move proposals — never an impression) · **proposed re-framing** (the restated contradiction or the shifted scope, concretely) · **expected gain** (which rubric dimension it would move, and why) · **what it costs** (re-sweep delta / the one re-ideation / a fresh run) · **the decision it asks for**.

**Contract rules.** (a) **Evidence-bound or not emitted** (Q10) — an advisory exists only when a named detector fires on a produced artifact; "maybe try another angle" is forbidden, and zero advisories is the normal case on a well-framed run. (b) **Emitting is free, acting is gated.** A pivot that would change the **frozen** Phase 1 contradiction or the **frozen** Phase 1.5 ledger scope invalidates every novelty verdict measured against them, so **acting on it is a contract-level confirmation (§3) that AUTORUN cannot skip** — the run never re-frames itself silently, because an invention nobody framed is an invention nobody wanted. (c) **Bounded** — ≤ 3 advisories per emission, deduplicated across emissions (a detector that already fired is not re-reported unless its evidence changed), and at most three emission points: Phase 2, Phase 3, and Phase 5 on a falsified spike. (d) **Free to detect** — detectors are hub-side pattern matches over artifacts already in hand; no extra spawn, so §1a's scale figures are unchanged. Cost appears only if a pivot is *accepted*, and then it is declared as one of the three costs above. (e) **Declining is recorded, not re-litigated** — a declined advisory goes into the Decision Ledger (Q4-Q6) with the user's reason and is not raised again by the same detector. (f) **A `BLOCK (prior-art saturation)` delivery carries its advisories** — "this framing is exhausted, and here is the framing that is not" is the whole value of a null result.

### 6b. Novelty Scout Report (`depth=scout`, named)

A **separately named deliverable, deliberately not called a dossier** — the word would claim proof this mode does not produce. It contains: the **contradiction** (as ratified) · the **Prior-Art Ledger** with sweep breadth · the **failure archaeology** (recorded, not exhaustive) · the **Ordinary-Move Set** from the 2-agent panel · the **Idea Ledger v2** (all candidates, verdicts, evidence) · any **Pivot Advisory** · the **exit reason** (`NOVEL-CANDIDATES` | `SATURATED`) · and a **promotion estimate**: which phases a full run would add, what it would cost (+20-46 agents), and what it would then be able to claim.

**Every survivor is labelled `UNPROVEN`** and the report says what is missing in one line: not adversarially refuted, not valued, no feasibility sketch, not reduced to practice. A scout answers *is it new and non-ordinary?* — nothing more — and the report is written so a reader who skims it cannot mistake it for a ratified invention.

### 6c. Invention Handoff Packet (`ship=true`, emitted at Phase 8.5)

Machine-consumable, mirroring the Spec Handoff Packet's shape so Phase 9 consumes it without re-parsing prose:

| Field | Content | Consumed by |
|-------|---------|-------------|
| `mechanism` | the Disclosure Package's mechanism statement | Phase 9 problem statement + direction — **pre-settled, not re-elicited** |
| `contradiction` + `binds_whom` | the Phase 1 Invention Contract | Phase 9 FRAME validation (replaces the Plea/Socratic pass) |
| `novelty_delta` + `nearest_prior_art` (cited) | the load-bearing difference and what it differs *from* | Phase 9 **must-have AC**; Phase 10 Novelty Invariant; Phase 11 regression oracle |
| `falsification_criterion` + `spike_result` | what would have killed the mechanism, and that it did not | Phase 9 AC verbatim; Phase 10 verification set |
| `constraint_budget` | what may NOT be spent (cost, latency, complexity, trust) | `non_goals` → scope bound on every downstream spawn (P8) |
| `prior_art_ledger_ref` | the frozen ledger + failure archaeology | Phase 10 Risk Gate input (each abandoned attempt's failure reason is a pre-mortem entry) |
| `residual_gap` | anything the invention run left unmet | Decision Ledger seed (Q4-Q6) — never silently dropped |

**Contract rule (inherited):** Phase 9/10 **do not re-open the settled invention**. A build that finds the mechanism unbuildable as specified returns to Phase 9, and if Phase 9 cannot spec it without dissolving the delta, the run stops and reports — it never quietly ships the generic version.

## 7. Salvage Routing — value below the invention bar

**Failing the invention bar is not the same as being worthless, and this recipe is the most likely place in the roster to produce valuable things that fail it.** A `COLLISION` means someone already built it — which makes it a *known-good mechanism*, not a dead end. An `OBVIOUS` kill means it is a sound, cheap improvement nobody bothered to make. A `DISPLACED-HIDDEN` kill means a real change with a real price. Discarding those because they are not *inventions* would throw away most of what a 32-62-agent run learned.

So **every kill and every non-`ACCEPT` exit carries a salvage verdict**: either `route:<recipe>` with what to hand over, or `discard(<reason>)` — stated, never silent.

| Killed / exited as | What it still is | Salvage route |
|--------------------|------------------|---------------|
| `COLLISION` (cited prior art exists **and works**) | a proven mechanism, with a reference implementation attached | **`graft`** to transplant it into this host · **`feature`**/`spec` to just build the known solution · `clone` if the cited artifact itself is the target |
| `OBVIOUS` (real delta, routine move) | a sound improvement the field has not bothered to make — cheap, low-risk, still worth doing | **`kaizen`** (polish one feature to a target) · **`optimize`** if the delta is a performance number · `feature` if it is net-new surface |
| `INCREMENTAL`, increment not load-bearing | a margin, correctly priced as a margin | **`kaizen`** · `anneal` if it is really a design cleanup |
| `DISPLACED-HIDDEN` (§1 condition 3) | a genuine change whose cost was found — the Sacrifice Ledger *is* the deliverable | **`feature`**/`kaizen` **with the ledger attached as a declared cost**, so the trade is made knowingly · **`magi`** when the trade is a decision someone must own |
| Tetrad **VALUE** fail (new, non-ordinary, nobody changes behavior) | a curiosity, possibly a differentiator in another market | **`killer`** (is it a bet worth placing?) · `compete` for positioning · else `discard` with the adoption reason named |
| Tetrad **FEASIBILITY** fail (novel, valuable, unbuildable *now*) | a **dated bet** — generator ⑤'s scaling-law logic run backwards | `gedanken` to reason it further, **plus a re-check trigger recorded in the dossier**: the specific constraint whose price change would make it buildable. A "no, not yet" with its condition stated is a different artifact from a "no" |
| Tetrad **DEFENSIBILITY** fail (new, valuable, trivially copyable) | table stakes — worth building, just not a moat | **`spec` → `apex`** positioned as parity work · `compete` to reposition · never sold internally as a moat |
| **Phase 5 falsified spike** | a disproven hypothesis **with a measurement** — the expensive part of a negative result | record the falsification + the number in the dossier; `gedanken` if the mechanism deserves re-derivation, `omen` if the failure mode generalizes to the roadmap |
| **ENABLEMENT ≤ 2** (works, not transferable) | a mechanism that exists only in this run's heads | `scribe`/`quill` to write it up until it *is* transferable — then it can re-enter at Phase 6. `spec` cannot consume it as-is (Ship Gate ③) |
| `SATURATED` / `BLOCK (prior-art saturation)` | a **map of the field** plus why every attempt failed | `compete` (positioning against what exists) · `graft` (import the best existing mechanism) · `feature` (build the known solution deliberately) |
| `cap-reached` / plateau-with-open-attacks | the best candidate, with its unmet dimensions named | **`killer`** for a go/no-go on it as a bet · re-enter later at Phase 6 against the frozen ledger, not from scratch |

**Contract rules.** (a) **No silent discards** — a candidate leaves the run either routed or explicitly discarded with a reason; "not an invention" is a verdict on the definition (§1), never a judgment that the thing is useless. (b) **Recommendation, not auto-continuation** — salvage routes are emitted with the handover content and a ready-to-run command; the run does **not** spawn another recipe on its own, because that would spend an envelope the user never approved (`ship=true` is the one continuation this recipe pays for, and it is opt-in). (c) **Bounded** — at most three routes per run, ranked by expected value; the rest are listed as discards. (d) **Related to, but distinct from, `WRONG-RECIPE`** — that Pivot Advisory detector fires *mid-run* to stop paying invention cost early (§6a); salvage runs *after* the verdicts and is about extracting value from what the run already produced. Both can fire in the same run without contradiction. (e) **`depth=scout` salvages too** — a `SATURATED` scout is the cheapest possible version of this table: 11-14 agents spent, a field map delivered, and a route out.

## 8. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **Reinventing something that already ships** | Prior-Art Ledger as the novelty denominator + Phase 3 `COLLISION` kill-with-citation; no candidate advances without a stated delta |
| **Ordinary work called an invention** — the delta is real but is a standard combination, a like-for-like substitution, or a parameter/scale change anyone would have made | Phase 3 `OBVIOUS` verdict, decided by the blind Routine-Move Test rather than by an evaluator's impression; killed with the matching proposals as evidence |
| **Hindsight obviousness** — an evaluator who has seen the answer judges it inevitable, killing real inventions | The ordinary-move panel is **blind and pre-committed**: it runs concurrently with Phase 2 on the ledger alone, never sees a candidate, and its set is frozen before Phase 3 opens |
| **Cross-domain transplant auto-killed by its own source** — generator ② imports a mechanism, and the Phase 1.5 adjacent-industry entry it came from reads as prior art | Domain-scoped denominator + composite judgment (mechanism + local adaptation); a foreign entry sets the `OBVIOUS` bar, never an automatic `COLLISION`. Routine imports route to `graft` instead |
| **Repeating a known failure** ("nobody does this" because it was tried and it failed) | Failure archaeology at Phase 1.5; the reasons become Phase 2 constraints and Phase 4 value tests |
| **Novelty for its own sake** (new, and nobody cares) | Tetrad VALUE axis + the adoption-failure reasons re-run as tests |
| **A re-priced trade-off sold as a dissolved one** — X improves, Y holds, and the bill lands on complexity, ops burden, trust, another team, or next quarter | **Sacrifice Ledger** gate (§5, Phase 4): every axis accounted including *later* and *whose*; `DISPLACED-HIDDEN` is a kill, and definition condition 3 (§1) makes this constitutive rather than advisory |
| **A legitimate cost relocation punished as a defect** — trading memory for latency when memory is genuinely free is generator ③'s whole point | `DISPLACED-DECLARED` **passes**, on one condition: the move lands on an axis the Phase 1 constraint budget declared free, and it is stated as part of the mechanism rather than buried |
| **Unaudited free lunch** — a candidate that appears to cost nothing anywhere is accepted because nobody looked | `FREE-LUNCH` does not pass on sight: one extra skeptic runs with the single brief "name the axis we failed to count", and only a failed search promotes it to `DISSOLVED` |
| **Science fiction** (novel, valuable, unbuildable) | Tetrad FEASIBILITY sketch + Phase 5 reduction to practice as a contract requirement |
| **Trivially copyable "invention"** | Tetrad DEFENSIBILITY (moat class + time-to-copy), buildable-emergent moats not auto-downgraded |
| **Idea mistaken for invention** (a claim with no artifact) | Phase 5 falsification-first spike, judged by Radar rather than its builder |
| **Demo-driven self-deception** (the spike was built to succeed) | Falsification criterion declared before the run; producer ≠ judge (Q9) |
| **An invention only its inventor can build** | ENABLEMENT as a scored rubric dimension on a defined 0-3 scale (§5, Phase 6 note) + the Phase 7 Disclosure Package; ENABLEMENT = 3 is Ship Gate precondition ③ |
| **Generator monoculture** (six prompts, one set of priors) | Six structurally-different heuristics, cross-engine distribution, no cross-pollination before commitment; monoculture declared when unavoidable |
| **Novelty grading inflation** (everything looks new to a generous evaluator) | Prior-art-anchored calibration: the nearest prior art must score NOVELTY 0 / FEASIBILITY 3, or the evaluator is re-prompted |
| **Contradiction never named** → a task dressed as an invention | Phase 1 requires an explicit "<better X> requires <worse Y>"; unnameable → route out |
| **Invention framing on routine work** | Phase 0 gate recommends `feature`/`spark`/`graft` when the ask is a known solution to a known problem |
| **Invention-grade cost for a novelty question** — "is this already out there?" is answered by a 32-62-agent run because nothing cheaper judges novelty | **`depth=scout`** (§1a): 11-14 agents, one confirmation, ledger + adjudicated candidates, promotion re-enters at Phase 2 against the frozen ledger |
| **A scout result mistaken for a proven invention** | Separately named **Novelty Scout Report** (never "dossier"), every survivor labelled `UNPROVEN` with what is missing stated, `ACCEPT` unreachable by construction, and `depth=scout` + `ship=true` refused as mutually exclusive |
| **The idea field invisible until the end** — 8-15 mechanisms are generated, most are killed at Phase 3, and the user sees none of them until Phase 8 (or none at all if the run is cancelled at Phase 5) | **Idea Ledger emitted mid-run** at Phase 2 (raw) and Phase 3 (adjudicated), kills included with their evidence, persisted at the same boundaries (§6a, §4) |
| **Silent deduplication** — near-duplicate mechanisms are merged before the user ever sees the variants | Dedup is **shown, not applied silently**: the v1 ledger lists merged ideas with their `dedup_into` target |
| **Framing lock-in** — the run learns mid-ideation that a neighboring direction is the better one, but the contradiction is frozen, so it grinds to a weak `ACCEPT` on the wrong problem | **Pivot Advisory** with five named detectors on already-produced artifacts (§6a), emitted at Phases 2, 3 and 5; a `BLOCK` delivery carries it too |
| **Silent self-re-framing** — the run quietly switches the contradiction or the ledger scope, invalidating every verdict measured against the frozen versions | Emitting an advisory is free; **acting** on one is a contract-level confirm AUTORUN cannot skip (§3), and the run continues on the declared framing until the user says otherwise |
| **Pivot chasing** — advisories become a licence to wander, and the run never converges | Evidence-bound or not emitted, ≤ 3 per emission, deduplicated across emissions, only three emission points, declined ones not re-raised by the same detector |
| **Value below the invention bar thrown away** — a `COLLISION` (someone already built it, so it *works*), an `OBVIOUS` (a cheap improvement nobody made), or a priced trade-off is discarded because it is "not an invention" | **Salvage Routing** (§7): every kill and non-`ACCEPT` exit carries `route:<recipe>` with its handover content or an explicit `discard(<reason>)`; `salvage` is a required Idea Ledger field, so silence is not a valid outcome |
| **Auto-spending on the salvage route** — the run notices a `kaizen` opportunity and starts building it on an envelope nobody approved | Salvage is **recommendation-only** with a ready-to-run command; `ship=true` remains the sole continuation this recipe pays for, and it is opt-in |
| **"No, not yet" reported as "no"** — a novel, valuable mechanism dies on feasibility and the condition that would revive it is lost | `FEASIBILITY`-failed candidates carry a **dated re-check trigger**: the specific constraint whose price change makes them buildable (generator ⑤ run backwards) |
| **A null result thrown away** | `BLOCK (prior-art saturation)` still ships the dossier — the ledger and failure archaeology are the run's most valuable artifact |
| **Unbounded search for a breakthrough** | `loop ≤ 3` + exactly one re-ideation + budget envelope with `budget-reached` best-so-far delivery |
| **Cycle-budget double-spend** — a re-ideation silently buys a fresh set of convergence cycles, doubling the run | §2 two-returns-one-budget rule: the Phase 6 counter is run-wide and a re-ideation does not reset it; Phase 3 and Phase 5 draw on the *same* single re-ideation |
| **Novelty erosion during the build** (`ship=true`) — the load-bearing delta is simplified away and a generic feature ships under an invention's name | Novelty Invariant at Phase 10 (a scope cut removing the delta is a gate failure, not a trade-off) + Phase 11 regression check by a non-builder + `RETRACTED` as an honest terminal verdict |
| **The verdict follows the code** — the novelty claim is softened after the fact to match what got built | Dossier **frozen** at the Ship Gate; no downstream phase may edit the novelty verdict that authorized it |
| **Spike promoted to production** — a design chosen for falsifiability becomes the architecture | Phase 10 contract: the spike is evidence, not a foundation; production re-derives from the Disclosure Package |
| **Building an unratified invention** | Ship Gate preconditions ①②③④ — only an `ACCEPT` exit with zero surviving attacks, ENABLEMENT = 3, and a surviving spike reaches Phase 9 |
| **Silent cost escalation from invention into product** | `ship=true` is opt-in and never inferred; a **second** unconditional confirm with a **separate** build envelope (precondition ⑤) |
| **Re-running settled discovery** (invention proven, then spec re-brainstorms it) | Phase 9 collapses FRAME/EXPAND/CHALLENGE against the Invention Handoff Packet; re-litigating a ratified mechanism is drift (Q7) |

## 9. Shared-Protocol References

| Protocol | What eureka takes from it | Eureka-specific specialization |
|----------|--------------------------|-------------------------------|
| `reference/research-grounding.md` | Tiered sources, per-claim verification, cited Evidence Ledger | **Inverted polarity** (research to avoid, not reproduce) + prior-art tier reweighting (papers/standards/inspectable implementations over vendor claims) + mandatory adjacent-industry search + failure archaeology as a required output |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, score scale, aggregation, Δ < 0.2 | Ceiling ACCEPT (all 5 dims = 3) with prior-art-anchored calibration |
| `_common/ADVERSARIAL_REFUTATION.md` | Skeptic panel, evidence-vs-novelty, polarity, aggregation, exclusions | Target claim = "this is new, wanted, buildable, and defensible"; the protocol's **unproven-because-new** rule is load-bearing here — an invention cannot be refuted for lacking evidence that can only exist after it is built |
| `reference/dialogue-protocol.md` | Question craft, Assumption Ledger, checkpoint presentation | Contradiction extraction is **eureka-original**, built on its question-craft rules |
| `reference/verdict-gate.md` | Verdict card, Yes/No/Modify, flag + KPI + kill criterion | Applied at the Phase 8 handoff when the invention is carried forward as a product bet (the `killer` path) |
| `reference/autonomy-quality-protocol.md` | Intent contract (Q1-Q3), producer ≠ verifier (Q9), evidence-bound claims (Q10), Acceptance Provenance (Q15) | Q9 applied twice: Radar judges the spike it did not build, and the skeptic panel is generator-excluded |
| `_common/CLI_COMPATIBILITY.md` §4 | Per-engine model map and spawn prerequisites | The six-generator cross-engine distribution resolves against it |
| `reference/doc-quality-protocol.md` | W1-W12 for document deliverables | The Disclosure Package is a document deliverable; ENABLEMENT subsumes W12 and adds transferability |
| `reference/spec-recipe.md` § Handoff contract | Spec Handoff Packet schema + the "downstream does not re-open settled decisions" contract rule | `ship=true` Phase 9: entered *with* the Invention Handoff Packet (§6c), so FRAME/EXPAND/CHALLENGE collapse to validation; the novelty delta is added as a **must-have AC** |
| `reference/apex-recipe.md` § Input Contracts | Packet-consuming collapse of apex Phases 1-4; "a packet removes re-derivation, never verification" | `ship=true` Phase 10: apex's gates run unchanged, plus one eureka-only constraint — the **Novelty Invariant**, enforced by the Phase 11 regression check |

## 10. Decision Tree vs Neighbors

```
Is the ask a BREAKTHROUGH way of solving something — new, AND not the ordinary next move?
  NO ↓
    known solution to a known problem?          → feature / spark
    mechanism proven elsewhere, routine port?   → graft  (non-routine adaptation → stay here)
    combine ≥2 existing products?               → fuse
    pick the best bet from candidates in hand?  → killer
    reason about a claim, no artifact?          → gedanken
    maximize execution of a known deliverable?  → wish
  YES ↓
Can you name the contradiction it dissolves ("<better X> requires <worse Y>")?
  NO  → it is a task or a preference, not an invention — route out and say why
  YES ↓
Does the dissolution hold up when you ask WHO PAYS, and WHEN?
  the cost just moved somewhere undeclared → not an invention by this recipe's definition (cond. 3);
    it may still be a good change — Salvage Routing (§7) sends it to feature / kaizen with the
    Sacrifice Ledger attached as a declared cost, or to magi when the trade needs an owner
  the cost moved onto a genuinely free axis, and you will declare it → stay here (DISPLACED-DECLARED)
  nothing is paid anywhere → stay here, and expect the FREE-LUNCH audit rather than applause
   ▼
Is being FIRST load-bearing (and being wrong about first, expensive)?
  NO  → graft / spark are cheaper and sufficient
  YES ↓
Do you need it PROVEN, or do you just need to know whether it is new?
  just check  → eureka depth=scout — ledger + adjudicated candidates, 11-14 agents, one confirm,
                every survivor UNPROVEN; promote later at +21-46 against the frozen ledger
  proven      → eureka — crystallize the contradiction → prior-art ledger + failure archaeology
        → six-generator divergence ‖ blind ordinary-move panel
        → novelty gate: COLLISION (kill w/ citation) · OBVIOUS (kill w/ proposals) → tetrad gate
        → falsification-first reduction to practice → gauntlet-converge → disclosure → deliver
          ↓
        Do you also want it BUILT in this run?
          NO  → ship=false (default) — dossier + handoff; run spec → apex later if it earns it
          YES → ship=true — Ship Gate (5 preconditions, second confirm, separate build envelope)
                → collapsed spec → apex → novelty regression check → ship
                (any precondition missed → ends at the dossier, precondition named)
```
