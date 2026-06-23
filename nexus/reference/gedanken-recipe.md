# `gedanken` — Structured thought-experiment reasoning

**Purpose:** Full phase contract for the `gedanken` Recipe — take a question, hypothesis, premise, or design tension and reason about it rigorously **inside a constructed hypothetical, under controlled variation**, to surface hidden assumptions, derive non-obvious implications, and establish what would falsify the conclusion. **Writes no code.** The general-purpose reasoning recipe — the disciplined analog of a classic *Gedankenexperiment* (Galileo's falling bodies, Einstein's elevator, Schrödinger's cat, Rawls' veil of ignorance, the Chinese room).

**Read when:** executing the `gedanken` Recipe. Authored to `reference/recipe-contract.md` (all 8 elements).

---

## What `gedanken` is for

A user has a **claim to pressure-test, a counterfactual to explore, or a design tension to reason through** — "what happens if we assume X?", "does this principle survive its own limiting case?", "what would have to be true for Y to work?" — and wants a *rigorous* answer, not a brainstorm and not a build. The deliverable is a **reasoning artifact**: the experiment, its result, the assumptions it rests on, and the observation or argument that would overturn it.

`gedanken` exists because thought experiments have a *method* — construct an idealized scenario, isolate one variable, push it to a limit, observe what the reasoning forces — and that method is exactly a controlled multi-agent protocol: construct → reason from independent lenses → perturb → refute → conclude. It is the **exploratory** reasoning recipe, distinct from `magi` (which delivers a *decision*) — `gedanken` is often `magi`'s upstream.

### Default Mode: `AUTORUN_FULL`
Autonomous reasoning runs end-to-end. Use `INTERACTIVE` when the user wants a Socratic back-and-forth (each phase boundary becomes a steer point) — that is a Mode choice, not a contract requirement (unlike `spec`, whose checkpoints are contract-level). There is **no confirm/safety gate**: `gedanken` writes no code and takes no destructive action (same posture as `charter`).

---

## Phase contract

`FRAME → CONSTRUCT → REASON → PERTURB → REFUTE → CONCLUDE`

### Phase 1 — FRAME (the question + its hidden premises)
Pin the exact question/hypothesis, the **givens** (premises taken as true for the experiment), the **scope** (what is inside the hypothetical vs out), and what a *useful* answer looks like ("so what" — what real decision or belief this informs). **Surface the implicit assumptions up front** — the failure mode of every thought experiment is a premise smuggled into the setup that does the conclusion's work invisibly. `Magi`[frame the question + enumerate stated and implicit assumptions]; +`Flux`[challenge the framing itself — is this even the right question?]; +`Lens`/`Compete`[ground the hypothetical in the real codebase / market when it concerns one].
- Output: a precise question, an explicit assumption ledger (stated + implicit), and the answer-shape.

### Phase 2 — CONSTRUCT (build the hypothetical, choose the form)
Build the idealized scenario: the setup, the **controlled variable(s)**, and the *ceteris paribus* isolation (what is held equal). **Pick the thought-experiment archetype** (menu below) — naming the form makes the reasoning auditable and exposes where it can break. `Flux`[construct scenario + select archetype]; +`Cast`[persona-anchored scenario when the question is about people]; +`Matrix`[lay out the variation axes when more than one variable matters].

**Archetype menu:**
| Form | Move | Classic example |
|------|------|-----------------|
| **limiting-case** | take a variable to 0 / ∞ / its boundary | Galileo's falling bodies |
| **counterfactual** | change one historical/given fact, replay | "if the cache didn't exist…" |
| **reductio ad absurdum** | assume the claim, derive a contradiction | many impossibility proofs |
| **isolation-of-variable** | hold all else equal, vary one | Einstein's elevator (gravity vs acceleration) |
| **analogy-transfer** | map to a domain where intuition is strong | Maxwell's demon (thermodynamics ← agency) |
| **inversion** | assume the opposite, see what breaks | "what if users *wanted* the error?" |
| **veil-of-ignorance** | reason without knowing your position | Rawls' fairness |

### Phase 3 — REASON ∥ (independent multi-perspective derivation)
Independent reasoners work the scenario from **distinct lenses** (hub-spoke, no shared mutable state — independence is the point). `Magi` Logos (logic) / Pathos (lived effect) / Sophia (wisdom/values) ‖ `Flux`[cross-domain analogy] ‖ a domain specialist when the question is technical (`Atlas` architecture · `Helm` business/economics · `Oracle` AI/ML · `Ripple` systemic impact). Each derives the implications the scenario *forces* under its lens.
- Output: per-lens implication sets, with agreements and divergences marked.

### Phase 4 — PERTURB (controlled variation — the heart)
Push the scenario to discover which conclusions are **robust** vs **assumption-dependent**: change a key premise, take a variable to its limit, invert a given, run the counterfactual branch. `Matrix`[systematic variation across the Phase-2 axes] + `Flux`[limit-case / inversion] ; +`Omen`[failure-mode variation when the question is risk-shaped].
- **Termination bound:** variation rounds `≤ 3 cycles (default 3)`; stop on `robustness-established` (conclusions stable across variations) / `diminishing-insight` (Δ < ε — new variations reveal nothing new) / `cap-reached`. On any non-robust stop, report **which conclusions are robust and which are frame-dependent** — never present a frame-dependent result as universal.

### Phase 5 — REFUTE (adversarial stress test)
A skeptic panel attacks the conclusion per `_common/ADVERSARIAL_REFUTATION.md` (refute ×2-3, cross-engine for prior-diversity), each from a distinct angle: **smuggled-premise** (the conclusion was baked into the setup), **false-analogy** (the archetype's mapping breaks), **equivocation** (a term shifted meaning mid-argument), **frame-dependence** (the result is an artifact of the chosen framing). Apply the evidence-vs-novelty discipline: distinguish "the conclusion is *wrong*" (a real defeater) from "the conclusion is *frame-dependent*" (a scope limit, recorded, not a kill).
- Majority refute-on-evidence → the conclusion fails or is Modified; survives → carries to CONCLUDE with its surviving/failed attacks recorded.

### Phase 6 — CONCLUDE (honest synthesis)
`Magi`[synthesize] states: the **conclusion(s)**; the **confidence**; the **load-bearing assumptions** (what the conclusion depends on — pulled from the FRAME ledger + PERTURB); the **falsifier** (the observation or argument that would overturn it — mandatory; an unfalsifiable conclusion is flagged as such); and the **transfer** (what it implies for the real question/decision). **Name the epistemic status honestly:** a *proof* (reductio that held), a strong *intuition pump*, or merely *suggestive*. `Scribe`?[write the Gedanken Report]. Optional handoff: feed the conclusion to `magi` (decision), `verdict-gate` recipes (`essential`/`killer`), or `spec` (if it resolved *what* to build).

---

## Resume

Checkpoint-resume: 6 phases → persist the FRAME assumption ledger, the CONSTRUCT scenario+archetype, the per-lens REASON outputs, and the PERTURB results at each boundary so an interrupted run resumes from the last completed phase rather than re-deriving.

## Output — Gedanken Report

`NEXUS_COMPLETE` with the base `## Nexus Execution Report` plus the named **Gedanken Report**:
- **Question** + answer-shape (what a useful answer looks like).
- **Assumption ledger** — stated + implicit premises (FRAME).
- **Scenario(s) + archetype** — the constructed hypothetical and the form(s) used (CONSTRUCT).
- **Per-lens reasoning** — implications by lens, agreements/divergences (REASON).
- **Variation results** — which conclusions are **robust** vs **frame-dependent**, with the perturbations run (PERTURB).
- **Refutations** — attacks survived and attacks that landed (REFUTE).
- **Conclusion** — claim + confidence + **load-bearing assumptions** + **falsifier** + **transfer to the real decision** + **epistemic status** (proof / intuition-pump / suggestive).

## Failure Modes Prevented

| Failure (thought-experiment fallacy) | Mitigation |
|--------------------------------------|------------|
| **Smuggled premise** (the conclusion was baked into the setup) | FRAME implicit-assumption ledger + REFUTE smuggled-premise angle |
| **False analogy** (the archetype's mapping silently breaks) | CONSTRUCT names the archetype explicitly + REFUTE false-analogy angle |
| **Frame-lock** (only one framing tried, result is an artifact of it) | REASON multi-lens + PERTURB inversion + REFUTE frame-dependence |
| **Unfalsifiable conclusion** (sounds deep, predicts nothing) | CONCLUDE mandates a falsifier; flags one that has none |
| **Intuition pump mistaken for proof** | CONCLUDE names epistemic status (proof / pump / suggestive) honestly |
| **Confirmation reasoning** (reasoned only toward the desired answer) | REFUTE adversarial panel (evidence-vs-novelty) |
| **Frame-dependent result sold as universal** | PERTURB separates robust from assumption-dependent conclusions |

## Boundaries / vs neighbors

- **vs `magi`** — `magi` delivers a *decision* (Go/No-Go, trade-off arbitration); `gedanken` *explores* a hypothetical's implications and is often `magi`'s upstream. A request that wants "decide X" → `magi`; "reason through what X would imply" → `gedanken`.
- **vs `riff`** — `riff` diverges (generates ideas); `gedanken` converges rigorously toward a conclusion under controlled variation. Brainstorm → `riff`; pressure-test → `gedanken`.
- **vs `omen`** — `omen` enumerates *failure modes* (a risk-focused thought experiment); `gedanken` is general (any hypothesis/scenario) and uses `omen` inside PERTURB when the question is risk-shaped.
- **vs `flux`** — `flux` is a single reframing/assumption-challenge move; `gedanken` *orchestrates* `flux` + `magi` + `omen` + `matrix` into a full protocol with an output contract. A one-off "reframe this" → `flux` direct.
- **vs `helm`** — `helm` simulates *business* scenarios with financial/market models; `gedanken` is domain-agnostic abstract reasoning.
- **vs `spec` / `charter`** — those produce *buildable* artifacts (a spec, a team charter); `gedanken` produces an *insight* artifact and writes no build plan (though it can hand off to `spec` if it resolved *what* to build).
- **vs `converge`** — `converge` is an automated quality grading loop over a generator; `gedanken` is open-ended exploratory reasoning, not a graded loop.

**Decision tree:**
```
Want a rigorous answer about a hypothetical / claim (no code)?
  NO  → decide between options? → magi · generate ideas? → riff · enumerate risks? → omen
        one-off reframe? → flux · simulate a business case? → helm
  YES → trivial single "what if"? → flux / magi direct (minimum viable chain)
        otherwise (construct → reason → perturb → refute → conclude) → gedanken
              resolved WHAT to build and want a spec? → gedanken → spec
              resolved a decision and want it arbitrated? → gedanken → magi
```

## Scale

3-9 agents × variation depth. Light by agent count (a focused experiment is FRAME→CONSTRUCT→one Magi→REFUTE→CONCLUDE ≈ 4 agents); deep when REASON fans across many lenses and PERTURB runs the full variation matrix. Like `spec`, the value is in reasoning depth, not fan-out width.

## Shared protocols & Add-ons

- **Shared:** REFUTE → `_common/ADVERSARIAL_REFUTATION.md` (skeptic panel, evidence-vs-novelty, polarity). Downstream handoff → `nexus/reference/verdict-gate.md` / `magi` / `spec`.
- **Add-ons:** +`Lens`/`Compete` (ground the hypothetical in a real system/market in FRAME), +`Cast` (persona-anchored scenario), +`Matrix` (systematic multi-axis variation in PERTURB), +`Omen` (failure-mode variation), +`Atlas`/`Helm`/`Oracle`/`Ripple` (domain-specialist lens in REASON), +`Scribe` (author the Gedanken Report).

## Chain template
`FRAME (Magi[frame + stated/implicit assumption ledger] +Flux?[challenge framing] +Lens?/Compete?[ground in real system]) → CONSTRUCT (Flux[build hypothetical + pick archetype: limiting-case|counterfactual|reductio|isolation|analogy|inversion|veil] +Cast?/Matrix?) → REASON ∥ (Magi Logos/Pathos/Sophia ‖ Flux cross-domain ‖ domain-specialist?[Atlas|Helm|Oracle|Ripple]) → PERTURB (Matrix[axis variation] + Flux[limit/invert] +Omen?; variation rounds ≤ 3 cycles (default 3), stop on robustness-established | diminishing-insight | cap-reached → mark robust vs frame-dependent) → REFUTE (refute×2-3 per _common/ADVERSARIAL_REFUTATION.md — smuggled-premise|false-analogy|equivocation|frame-dependence) → CONCLUDE (Magi synthesize: conclusion + confidence + load-bearing assumptions + falsifier + transfer + epistemic status; Scribe?[Gedanken Report]) [NO CODE]`

Resumable: checkpoint per phase. Optional handoff to `magi` / `spec` / verdict recipes at CONCLUDE.
