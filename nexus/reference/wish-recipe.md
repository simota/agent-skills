# Wish Recipe — Once-in-a-Lifetime Request

> `/nexus wish "<request>"` — the **scarcity-gated, one-shot, quality-ceiling** delivery recipe. The invocation carries the semantics of a lifetime plea: this ONE output must be the best achievable — no "we'll fix it in the next iteration," no routine-quality shortcuts. Deliverable-agnostic: the underlying task (code, document, design, content, plan) is routed to its natural generator, then wrapped in wish machinery — crystallization dialogue, benchmark anchoring, cross-engine tournament, calibrated adversarial gauntlet, reception simulation, and a final two-part exit gate.

Read this file before executing the `wish` Recipe.

**Engine + domain presets.** `wish` factors into a **quality-ceiling engine** (this file: crystallize → anchor → tournament → gauntlet-converge → reception → exit gates, §1-§10) and **domain presets** that fix the rubric and insert deliverable-specific phases. The engine is shared; only the preset varies.

| Preset | Invocation | Blueprint | What the preset fixes |
|--------|-----------|-----------|----------------------|
| `general` (default) | `/nexus wish "<request>"` | this file | Rubric authored at Phase 1 and anchored at Phase 1.5; Scarcity Gate **on** |
| `lp` | `/nexus wish domain=lp` ≡ `/nexus marquee` | `reference/marquee-recipe.md` | Fixed 5-dim LP rubric with machine oracles (Lighthouse/CWV/WCAG); GROUND + PRODUCE phases inserted; Benchmark Anchor fixed to top-of-class LPs; Reception Simulation bound to the LP's target audience; Scarcity Gate **off** (intentional — LP production is legitimately repeatable, objectivity replaces rationing) |

`marquee` is kept as a **named alias for discoverability** and dispatches to `wish domain=lp`; its full blueprint (fixed rubric anchors, funnel[premium] craft-axis production substrate, LP skeptic angles, Marquee Dossier) lives in `reference/marquee-recipe.md`. A preset never weakens the engine's termination bound, exit gates, calibration requirement, or Q9 separation — it may only fix the rubric, add phases, supply its own exemplar set, and state one intentional gate difference.

**Not a preset:** `runway` (flagship in-product UI) deliberately carries **neither the exit gates nor the refutation gauntlet** — it shares only the ceiling ACCEPT. It is a `restyle` escalation, not a wish variant; see `reference/runway-recipe.md`.

---

## 1. Nature / When to Use / Boundaries

**Wish is a quality-ceiling wrapper, not a task shape.** Its identity comes from seven things no sibling recipe carries together:

1. **Scarcity Gate** — "once-in-a-lifetime" is operationalized as **usage transparency + outcome-informed challenge**: every invocation is journaled in the Wish Ledger (§6 Phase 0 schema), surfaced ("this is wish #N; last used <date>; outcomes of prior wishes"), and invocations that classify as routine are challenged with a cheaper-recipe recommendation. A wish invoked weekly is not a wish.
2. **Benchmark Anchor** — the rubric's score-3 descriptors are **sourced from the best existing artifacts of this class**, not invented. A ceiling defined only by the system that generates against it can be satisfied by mediocrity; wish is the only recipe that goes and finds out what excellent actually looks like before deciding what excellent means.
3. **Ceiling ACCEPT** — the convergence bar is raised from converge's `all dims ≥ 2` to **`all dims = 3`** (the rubric ceiling). Wish is the only recipe that targets the top of the scale by contract.
4. **Calibrated evaluation** — evaluators are **two-point calibrated** (against a known-excellent exemplar and a known-routine control) before they score a candidate. An uncalibrated evaluator that awards 3 to a competent-but-ordinary artifact silently converts the ceiling into an average.
5. **Wish Crystallization** — a contract-level dialogue excavates the *true* wish behind the words, including explicit **disappointment criteria** ("what outcome would make you regret spending your lifetime request?").
6. **Cross-engine tournament** — candidates, evaluators, and skeptics are distributed across **different model families** wherever the hub allows, and judged **blind**. Three prompts to one model produce three framings of one set of priors; independence at the priors level is what makes a tournament worth its cost.
7. **Two-part exit gate** — before delivery, a **fresh-context** verifier answers "would a fresh redo be *materially* better than this?" (One-Shot Gate) **and** a blind head-to-head asks "against the best artifact we found, and against our own runner-up, does this one win?" (Comparative Gate). There is no second delivery, so both run.

### Use `wish` for

- A request the user explicitly frames as their most important ask: "this is the one," "your absolute best," "the favor of a lifetime."
- One-shot deliverables with no revision opportunity (a decisive proposal, a flagship document, a make-or-break artifact) of **any** type — code, prose, design, plan.
- When the user wants the *recipe itself* to guarantee that nothing was left on the table.

### Not this — route to

| Not this | Route to | Why |
|----------|----------|-----|
| Strategic/release-critical **code** quality-max with engine triangulation | `summit` | Summit's five-team multi-engine tournament is purpose-built for code-heavy strategic work |
| Iterate an existing deliverable to a defined bar (`all dims ≥ 2` suffices) | `converge` | Standard rubric loop; no scarcity/ceiling/one-shot semantics needed |
| Full feature lifecycle discovery→ship | `apex` | Apex owns the build lifecycle; wish owns the quality ceiling |
| Doc + slide package quality | `podium` | Content-production five-team pipeline |
| Proof-carrying merge gate | `acceptance` | Merge adjudication, not one-shot delivery |
| Routine tasks a user casually calls "best quality" | the natural recipe | Scarcity Gate exists precisely to catch this — recommend the cheaper path |

**Scale: 27-102 agents × ≤5 cycles (+1 bonus), 10-28× `feature` cost** (deliverable-dependent; the wrapped generator dominates). Per-phase formula: P0-P1 ≈ 2 · P1.5 ≈ 3-6 (exemplar sweep + anchor authoring) · P2 ≈ 8-14 (3-5 cross-engine candidates + blind judge panel + calibration pass) · P3 ≈ 4-8 Evaluators/cycle + 2-4 skeptics per near-ceiling cycle, ×1.6 while dual-lineage is active · P3.5 ≈ 3-5 personas · P4 ≈ 3 (One-Shot verifier + 2 comparative judges) · P5 ≈ 2.

*Range derivation* (convention: `reference/recipe-contract.md` §1 element 7): floor = S/M, ACCEPT on cycle 1 → 2+3+8+(4+2)+3+3+2 = **27**; ceiling = L/XL, 6 cycles (N=5 + bonus), dual-lineage cycles 1-2 at ×1.6, skeptics on 3 near-ceiling cycles → 2+6+14+(8×1.6×2 + 8×4 + 4×3 ≈ 70)+5+3+2 = **102**. **Confirm-before-launch always** (intentional — same unconditional gate as `summit`; the Scarcity Gate is that confirmation) **with a declared budget envelope** (§4).

**Model selection (Plan-and-Execute):** Phase 1 Crystallization, the Phase 1.5 anchor ratification, and both Phase 4 gate verdicts are judgment-heavy → plan-tier (opus / Fable 5). Phase 2 generators, Phase 3 Evaluators/skeptics, and Phase 3.5 personas → Sonnet 5 default, per SKILL.md § Core Contract. Cross-engine distribution overrides the per-tier default where the §6 Phase 2 mandate applies.

---

## 2. Termination Bound

Convergence **`loop ≤ N cycles (default N=3, N=5 when scope = L/XL and the budget envelope allows)`**, plus the exit gates may grant **exactly one bonus cycle** — hard total N+1 (6 when N=5, 4 on the N=3 default). Exit reasons use the canonical vocabulary:

| Exit reason | Wish-specific meaning |
|-------------|----------------------|
| `ACCEPT` / `target-met` | **all scored rubric dimensions = 3 on calibrated evaluators** produces a *candidate ACCEPT*; the refutation panel then **ratifies** it (surviving attacks = 0 → true ACCEPT) or **demotes** it to REVISE with each surviving attack as feedback δ. The rubric is the single termination oracle; the panel is a ratification step inside it, never a parallel second oracle |
| `diminishing-returns (Δ < ε)` | weighted score Δ < 0.2 between cycles (`evaluator-loop-protocol.md` values verbatim). If surviving attacks > 0 when this fires, the exit is a **plateau-with-open-attacks** — reported as such with every open attack listed, never presented as a clean plateau |
| `cap-reached` | the cycle cap (+ ≤1 bonus) without ratified ceiling ACCEPT |
| `budget-reached` | the §4 envelope ceiling hit mid-loop → deliver best-so-far with the residual gap; a wish never overruns its declared envelope silently |
| `BLOCK` | un-fixable within scope, or Agent Tennis — escalate |

On any non-`ACCEPT` exit the recipe reports best-so-far + the residual gap vs the ceiling. Because the ceiling is often unreachable, a clean `diminishing-returns` (no open attacks) is an *honorable* exit: the Fulfillment Report states exactly which dimensions plateaued below 3 and why.

**Scope→cycle rule.** S/M scope keeps N=3 — a small deliverable that has not reached the ceiling in three calibrated cycles is plateaued, not under-iterated. N=5 is available only when the deliverable is L/XL **and** the envelope covers it; the choice is stated at the Scarcity Gate, not discovered mid-loop.

## 3. Confirm / Safety Gate

- **Phase 0 Scarcity Gate: Confirm before launch — always** (unconditional, intentional parity with summit's gate; not drift). The prompt surfaces: Wish Ledger count, last-use date and prior outcomes, **the budget envelope and cycle cap being authorized** (§4), and — when the task classifies as routine (§6 Phase 0 heuristics) — an explicit recommendation of the cheaper recipe. The user may override; the override is journaled.
- **Phase 1 Wish Crystallization: contract-level checkpoint; AUTORUN cannot skip.** The dialogue *is* the deliverable's foundation (same tier as `spec` dialogue).
- **Phase 1.5 anchor ratification: contract-level.** The sourced score-3 anchors are shown to the user before the rubric freezes — an anchor the user rejects ("that exemplar is not what I mean by excellent") is corrected here, where it costs one turn, not at Phase 4, where it costs the run.
- **Rubric amendment (§7): contract-level, at most once.** Re-opening a frozen rubric mid-loop requires user ratification.
- Standard Ask First tiers (L4 security / destructive / 10+ files) apply unchanged to the wrapped generator.
- On a Fable 5 hub, the Scarcity Gate subsumes the F8 cost gate — one confirmation, not two.

## 4. Budget Envelope

Wish is the most expensive per-deliverable recipe in the roster, and "spare nothing" is a quality instruction, not a spending one. A **pre-declared envelope** — agent count ceiling, cycle cap, and token/cost ceiling — is authorized at the Scarcity Gate alongside the scarcity confirmation, and tracked across every phase (`budget.spent()` semantics where the harness exposes them).

- The estimate presented at Phase 0 is labeled **"preliminary — refined after Phase 1 crystallization and Phase 1.5 anchoring"**, since the rubric's dimension count and the exemplar set are unknown at Phase 0. The refined envelope is restated once, at the Phase 1.5 checkpoint, and that is the number the run is held to.
- Hitting the ceiling exits `budget-reached` (§2) — **deliver best-so-far with the residual gap**, never a silent stop and never an unrequested overrun.
- Optional escalations that push past the envelope (a fourth tournament candidate, the dual-lineage carry, N=5 cycles) are named at the gate as *what the envelope buys*, so the user authorizes a shape, not a blank cheque.

## 5. Resume

**Checkpoint-resume** (≥ 4 phases): persist the Wish Contract + Ceiling Rubric at Phase 1 exit; **the Evidence Ledger + sourced anchors + calibration set at Phase 1.5 exit** (re-running an exemplar sweep on resume both wastes the spend and risks a *different* anchor set, which would silently move the ceiling); at Phase 2 exit persist **every candidate's full artifact content plus the blind-judge scores and the salvage list** (not just the winner — the dual-lineage carry and the Comparative Gate both need the runner-up); persist each cycle's score trajectory, calibration verdicts, and surviving attacks at each Phase 3 cycle boundary. An interrupted wish resumes mid-convergence with its trajectory intact.

---

## 6. Phase Contract (AUTORUN chain template)

```
Phase 0   SCARCITY GATE ★Confirm-before-launch (always) — classify + Wish Ledger check + preliminary envelope; routine task → recommend cheaper recipe (override journaled)
   ▼
Phase 1   CRYSTALLIZE ★contract-level dialogue (AUTORUN cannot skip; plan-tier) — Wish Contract + draft Ceiling Rubric + Evaluator roster
   ▼
Phase 1.5 BENCHMARK ANCHOR ★contract-level ratification — sourced exemplar set + control → rubric freezes, envelope restated (§4)
   ▼
Phase 2   TOURNAMENT ‖ 3-5 cross-engine candidates → two-point calibration pass → blind judging → winner + runner-up + salvage list
   ▼
Phase 3   GAUNTLET-CONVERGE loop — ceiling ACCEPT per §2; dual-lineage on L/XL; staged refutation once dims ≥ 2; on-demand rubric amendment (§7); near-ceiling Omen pre-mortem
   ▼
Phase 3.5 RECEPTION SIMULATION — named-recipient personas meet the artifact cold, no rubric/history → findings enter as rubric evidence
   ▼
Phase 4   EXIT GATES — (a) One-Shot Gate (fresh-context redo-value verdict) + (b) Comparative Gate (blind vs exemplar + vs runner-up); together grant at most one bonus cycle
   ▼
Phase 5   DELIVER — Fulfillment Report + Unexplored-Space Ledger + Wish Ledger append (Guardian if code)
```

Each phase's full mechanics are in the prose rules that follow (Phase 0 Wish Ledger schema, Phase 1 rubric-drafting rules, Phase 1.5 anchoring rules, Phase 2 cross-engine mandate, §7 Calibration & Rubric Amendment) — the diagram above is the sequence, not the specification.

**Phase 0 — Wish Ledger schema and routine heuristics.** The ledger lives under a `## Wish Ledger` heading in `.agents/nexus.md` (create on first use); Phase 0 counts entries rather than parsing prose:

```yaml
- wish: 3                    # sequence number
  date: 2026-07-16
  intent: "<one-line Wish Contract goal>"
  exit_reason: ACCEPT | diminishing-returns | cap-reached | budget-reached | BLOCK
  dims_at_ceiling: "4/5"
  comparative: won | split | lost-to-exemplar | lost-to-runner-up
  override: false            # true when the user overrode a routine-task challenge
  outcome: pending           # pending | satisfied | partial | regretted
```

The `outcome` field is backfilled lazily: at the NEXT wish's Phase 0, ask one line — "did wish #N-1 (<date>) satisfy its disappointment criteria?" — giving the Scarcity Gate real signal, not just a counter. **Routine-task heuristics** (any 2 of 3 → routine → challenge): (a) the request maps cleanly onto an existing chain template with no one-shot/irreversibility framing; (b) the phrasing carries none of the wish signal anchors (`reference/signal-keywords.md`); (c) the preliminary cost estimate is within ~2× the natural recipe's own baseline.

**Phase 1 — rubric drafting rules.** 3-5 dimensions; each score-3 descriptor is **task-specific** (never the generic "exceeds best practices"). The Wish Contract additionally names the **recipient(s)** — who this artifact is actually for — because Phase 3.5 cannot simulate a reception without one, and a one-shot deliverable with no named audience is usually an under-crystallized wish.

**Phase 1.5 — anchoring rules.** The sweep follows `reference/research-grounding.md` (tiered sources, per-claim verification, cited Evidence Ledger). What it changes:
- **Anchors become sourced.** "Score 3 = matches or exceeds `<exemplar>` on `<property>`" replaces an invented superlative. Reachability is then *demonstrated* rather than sanity-checked — an artifact scoring 3 exists, and it is in the ledger.
- **A control is required.** Without a low anchor, calibration is one-sided and cannot detect an evaluator that scores everything high.
- **No exemplar found** (genuinely novel deliverable class) → say so explicitly, fall back to Magi/Omen reachability sanity-check on invented anchors (the pre-anchoring behavior), and **record the fallback in the Fulfillment Report** — an unanchored ceiling is a weaker claim and must not read as an anchored one.
- **Do not copy the exemplar.** It calibrates the bar; reproducing it is `clone`'s job and a different recipe. The Comparative Gate asks whether ours *wins*, not whether it *resembles*.

**Phase 2 — cross-engine diversity mandate.** Where the hub can reach more than one engine (`_common/CLI_COMPATIBILITY.md §4`), the tournament distributes candidates across model families — e.g. Claude Code / Codex CLI (`gpt-5.6-sol` for design-shaped work) / agy (Gemini 3.7 Flash High). Rules: **at most one candidate per (engine, angle) pair**; the judge panel is likewise engine-diverse; a single-engine run **declares the monoculture** in the Fulfillment Report rather than presenting three same-model samples as a tournament. Blind judging is not optional — a judge that knows which engine produced which candidate carries a prior about the answer.

**Evaluator roster by deliverable class** (default mapping — Phase 1 selects Evaluators matching the contract's actual dimensions; a dimension with no matching specialist gets a purpose-prompted general evaluator, still Generator-excluded):

| Deliverable class | Dimension → Evaluator defaults | Reception personas (Phase 3.5) |
|-------------------|--------------------------------|-------------------------------|
| Code / feature | correctness→Radar · code quality→Judge · UX→Echo/Palette · spec conformance→Attest · E2E→Voyager | the maintainer inheriting it · the on-call engineer · the end user |
| Document | Doc Quality Gate W12 (`doc-quality-protocol.md`) as a dimension · grounding→Attest · standards→Canon | the decision-maker who acts on it · the skeptic in the room · the reader with no context |
| Plan / strategy | trade-off soundness→Magi · market/competitive fit→Magi/Compete · internal consistency→Attest | the person who must execute it · the person funding it · the competitor reading it |
| Design / visual | craft→Vision · usability→Palette/Echo · a11y→Canon · motion→Flow | the first-time visitor · the returning user · the brand owner |

## 7. Calibration & Rubric Amendment

**Two-point calibration (Phase 2, and re-run whenever the Evaluator roster changes).** Before any candidate is scored, each evaluator scores the **exemplar** and the **control** on its dimension. The expected shape is exemplar ≈ 3, control ≈ 1-2.

| Calibration outcome | Meaning | Action |
|---------------------|---------|--------|
| exemplar < 3 | the anchor is unreachable as written, or the evaluator is severe | re-word the anchor (Phase 1.5 material) or re-prompt the evaluator — resolve **before** scoring candidates |
| control = 3 | the evaluator inflates; every subsequent 3 is meaningless | re-prompt with the control named as an explicit score-1-2 reference; a second inflation replaces the evaluator |
| exemplar ≈ 3 ∧ control ≤ 2 | calibrated | proceed |

An **uncalibrated evaluator's score cannot produce a ceiling ACCEPT** — this is the mechanism that keeps `all dims = 3` from degrading into "everyone said 3." Calibration verdicts are recorded per evaluator in the Fulfillment Report.

**Rubric amendment (at most once per wish, contract-level).** A frozen rubric that cannot express a real quality failure is worse than no rubric, because the loop will converge to a ceiling on the wrong axis. Amendment is allowed when **all four** hold: (a) a refutation attack or reception failure survives; (b) no existing dimension can express it (re-scoring it under a current dimension is the first attempt, always); (c) the user ratifies the new/altered dimension; (d) the current artifact is **re-scored on the amended rubric**, so the trajectory stays comparable. The amendment, its trigger, and the re-scored delta are recorded. A second amendment request is refused — at that point the wish is under-crystallized and the honest exit is `BLOCK` with the finding, not a third rubric.

## 8. Output Report — **Fulfillment Report** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Wish Contract recap** — goal, ACs, disappointment criteria, named recipients, each classified per Acceptance Provenance (Q15)
- **Benchmark anchoring** — exemplar set + control with citations (Evidence Ledger size, per-tier source count), which anchors were sourced vs invented, and the **no-exemplar fallback flag** if it fired
- **Calibration record** — per evaluator: exemplar score, control score, verdict (calibrated / re-prompted / replaced)
- **Tournament** — candidate count, **engine distribution** (or a declared monoculture), blind-judge scores, winner + runner-up, salvage items carried
- **Score trajectory** — per-cycle weighted scores per dimension; ceiling dims reached vs plateaued; lineage-merge decision if dual-lineage ran
- **Gauntlet ledger** — refutations raised / killed / survived-then-fixed; **open attacks listed explicitly on any plateau-with-open-attacks exit**
- **Rubric amendment** — trigger, change, re-scored delta (omit the section entirely when none)
- **Reception simulation** — per-persona verdict + friction points + which entered the rubric as evidence + any unresolved reception failure
- **Exit gates** — One-Shot verdict with cited evidence, **Comparative verdict (vs exemplar / vs runner-up) with the property named on any loss**, bonus-cycle usage, advisory second verdicts if any
- **Exit reason** (§2 vocabulary) + residual gap vs ceiling (empty only on ACCEPT) + **budget spent vs envelope**
- **Unexplored-Space Ledger** — what was deliberately *not* pursued: tournament angles not run, salvage items rejected and why, dimensions traded off against each other, escalations the envelope did not buy. A one-shot deliverable's honest claim is not "nothing was left on the table" but "here is exactly what was left, and why" — this section is what makes that claim auditable
- **Wish Ledger entry** — the §6 schema entry as recorded (`outcome: pending`)

## 9. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Wish inflation ("everything is a lifetime request") | Scarcity Gate: ledger count + prior outcomes surfaced + 2-of-3 routine heuristics (Phase 0) |
| Solving the stated ask, missing the true wish | Crystallization dialogue + disappointment criteria (Phase 1, contract-level) |
| "Best quality" left undefined → vibe acceptance | Ceiling Rubric frozen with task-specific score-3 anchors |
| **A ceiling invented by the same system that must reach it** | **Phase 1.5 Benchmark Anchor: score-3 descriptors sourced from best-in-class exemplars with citations; user ratifies before freeze** |
| **Everyone scores 3 and the ceiling means nothing** | **Two-point calibration (§7): exemplar + control scored before any candidate; an uncalibrated evaluator cannot produce a ceiling ACCEPT** |
| Unreachable-by-construction or trivially-reachable ceiling | Reachability *demonstrated* by an exemplar that scores 3 (Phase 1.5), Magi/Omen sanity-check only in the no-exemplar fallback |
| First-idea anchoring (one attempt iterated) | Tournament: 3-5 independent diverse-angle candidates + salvage from the field (Phase 2) |
| **Model monoculture presented as a tournament** | **Cross-engine mandate (§6 Phase 2): one candidate per (engine, angle); a single-engine run declares the monoculture in the report** |
| **Halo effect in judging** (the "best" engine's candidate wins on reputation) | **Blind judging: provenance stripped until scores are recorded** |
| **Convergence destroying value the tournament found** | **Dual-lineage carry through cycles 1-2 + lineage merge gate; Comparative Gate re-tests the final artifact against the retained runner-up** |
| Tournament cost blowup on small deliverables | S/M scope competes at outline level; only L/XL justifies full builds and dual-lineage (Phase 2, §4) |
| Plausible-but-not-actually-best output | Staged adversarial refutation panel once dims ≥ 2 + ratification of candidate ACCEPTs (Phase 3) |
| Dual-oracle conflict (rubric vs refutation vs reception) | Single oracle ladder: dims = 3 → candidate ACCEPT → panel ratifies or demotes (§2); reception findings enter as *evidence* on existing dimensions, never as a parallel gate |
| Plateau exit masking open attacks | `diminishing-returns` with survivors > 0 must report as plateau-with-open-attacks (§2, §8) |
| Disappointment criterion silently regressing mid-loop | Each criterion is a score-0 trigger on a rubric dimension (Phase 1 mapping; Phase 3 Evaluators check every cycle) |
| **Converging to a ceiling on the wrong axis** | **Bounded rubric amendment (§7): once, user-ratified, with the artifact re-scored so the trajectory stays comparable** |
| **A rubric-perfect artifact its actual recipient bounces off** | **Phase 3.5 Reception Simulation: named recipients meet it cold, no rubric, no loop history; unresolved failures are named residuals** |
| Evaluator mis-fit for non-code deliverables | Deliverable-class roster table + Phase 1 roster selection rule (§6) |
| Generator grades its own work | GAN separation per `evaluator-loop-protocol.md`; both Phase 4 gates are fresh-context/blind (Q9, second application) |
| Unbounded pursuit of an unreachable ceiling | §2 cycle cap (+1 bonus) + diminishing-returns exit; second gate verdicts advisory-only |
| **Open-ended spend on a "spare nothing" instruction** | **§4 budget envelope; `budget-reached` delivers best-so-far, never a silent overrun** |
| Loop-on-loop blowup when the inner task is apex/kaizen/summit-shaped | Flatten rule cited from `converge-recipe.md` §4 — wish owns the single loop |
| Silent under-delivery on a one-shot | Fulfillment Report residual-gap section; non-ACCEPT exits always report best-so-far |
| **"Nothing was left on the table" as an unfalsifiable claim** | **Unexplored-Space Ledger (§8): angles not run, salvage rejected, trade-offs taken, escalations not bought — stated, not implied** |

## 10. Shared-Protocol References

| Protocol | What wish takes from it | Wish-specific specialization |
|----------|------------------------|------------------------------|
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, score scale, aggregation, Δ < 0.2 | ACCEPT raised to all dims = 3 **on calibrated evaluators**, with panel ratification (§2) |
| `reference/research-grounding.md` | Tiered sources, per-claim verification, cited Evidence Ledger | Phase 1.5 sweeps for *exemplars of excellence* rather than a reproduction target; the ledger's output is the rubric's anchor set + the calibration control |
| `reference/converge-recipe.md` §4 | Flatten rule for loop-owning inner recipes | — |
| `reference/dialogue-protocol.md` | Question craft, Assumption Ledger, checkpoint presentation | Disappointment-criteria excavation and recipient-naming are **wish-original** — built on its question-craft rules |
| `_common/ADVERSARIAL_REFUTATION.md` | Skeptic panel, polarity, exclusions, engine diversity | Target claim = "this is the best achievable output"; staged (dims ≥ 2 only) + ratification duty |
| `reference/autonomy-quality-protocol.md` | Intent contract (Q1-Q3), producer ≠ verifier (Q9), Acceptance Provenance (Q15) | Q9 discharged twice by design: per-dimension in Phase 3, then fresh-context/blind at both Phase 4 gates |
| `reference/doc-quality-protocol.md` | W1-W12 for document deliverables | W12 becomes a rubric dimension |
| `_common/CLI_COMPATIBILITY.md` §4 | Per-engine model map and spawn prerequisites | The Phase 2 cross-engine distribution and the engine-diverse judge panel resolve against it |

Neighbor routing (summit / converge / the natural recipe) is the § 1 "Not this — route to" table above; no separate decision tree is needed.
