# Wish Recipe — Once-in-a-Lifetime Request

> `/nexus wish "<request>"` — the **scarcity-gated, one-shot, quality-ceiling** delivery recipe. The invocation carries the semantics of a lifetime plea: this ONE output must be the best achievable — no "we'll fix it in the next iteration," no routine-quality shortcuts. Deliverable-agnostic: the underlying task (code, document, design, content, plan) is routed to its natural generator, then wrapped in wish machinery — crystallization dialogue, tournament generation, adversarial gauntlet, ceiling convergence, and a final One-Shot Gate.

Read this file before executing the `wish` Recipe.

---

## 1. Nature / When to Use / Boundaries

**Wish is a quality-ceiling wrapper, not a task shape.** Its identity comes from four things no sibling recipe carries together:

1. **Scarcity Gate** — "once-in-a-lifetime" is operationalized as **usage transparency + outcome-informed challenge**: every invocation is journaled in the Wish Ledger (§5 Phase 0 schema), surfaced ("this is wish #N; last used <date>; outcomes of prior wishes"), and invocations that classify as routine are challenged with a cheaper-recipe recommendation. A wish invoked weekly is not a wish.
2. **Ceiling ACCEPT** — the convergence bar is raised from converge's `all dims ≥ 2` to **`all dims = 3`** (the rubric ceiling). Wish is the only recipe that targets the top of the scale by contract.
3. **Wish Crystallization** — a contract-level dialogue excavates the *true* wish behind the words, including explicit **disappointment criteria** ("what outcome would make you regret spending your lifetime request?").
4. **One-Shot Gate** — before delivery, a **fresh-context** independent verifier answers "would a fresh redo be *materially* better than this?" — because there is no second delivery.

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

**Scale: 15-40 agents × ≤4 cycles, 6-18× `feature` cost** (deliverable-dependent; the wrapped generator dominates). Per-phase formula: P0-P1 ≈ 2 · P2 ≈ 6-9 (3 candidates + judge panel) · P3 ≈ 3-6 Evaluators/cycle + 2-3 skeptics on near-ceiling cycles only · P4-P5 ≈ 2. **Confirm-before-launch always** (intentional — same unconditional gate as `summit`; the Scarcity Gate is that confirmation).

**Model selection (Plan-and-Execute):** Phase 1 Crystallization and the Phase 4 One-Shot Gate verdict are judgment-heavy → plan-tier (opus / Fable 5). Phase 2 generators and Phase 3 Evaluators/skeptics → Sonnet 5 default, per SKILL.md § Core Contract.

---

## 2. Termination Bound

Convergence **loop ≤ N cycles (default N=3)**, plus the One-Shot Gate may grant **exactly one bonus cycle** — hard total 4. Exit reasons use the canonical vocabulary:

| Exit reason | Wish-specific meaning |
|-------------|----------------------|
| `ACCEPT` / `target-met` | **all scored rubric dimensions = 3** produces a *candidate ACCEPT*; the refutation panel then **ratifies** it (surviving attacks = 0 → true ACCEPT) or **demotes** it to REVISE with each surviving attack as feedback δ. The rubric is the single termination oracle; the panel is a ratification step inside it, never a parallel second oracle |
| `diminishing-returns (Δ < ε)` | weighted score Δ < 0.2 between cycles (`evaluator-loop-protocol.md` values verbatim). If surviving attacks > 0 when this fires, the exit is a **plateau-with-open-attacks** — reported as such with every open attack listed, never presented as a clean plateau |
| `cap-reached` | 3 cycles (+ ≤1 bonus) without ratified ceiling ACCEPT |
| `BLOCK` | un-fixable within scope, or Agent Tennis — escalate |

On any non-`ACCEPT` exit the recipe reports best-so-far + the residual gap vs the ceiling. Because the ceiling is often unreachable, a clean `diminishing-returns` (no open attacks) is an *honorable* exit: the Fulfillment Report states exactly which dimensions plateaued below 3 and why.

## 3. Confirm / Safety Gate

- **Phase 0 Scarcity Gate: Confirm before launch — always** (unconditional, intentional parity with summit's gate; not drift). The prompt surfaces: Wish Ledger count, last-use date and prior outcomes, the estimated cost envelope (**labeled "preliminary — refined after Phase 1 crystallization"**, since the rubric's dimension count is unknown at Phase 0), and — when the task classifies as routine (§5 Phase 0 heuristics) — an explicit recommendation of the cheaper recipe. The user may override; the override is journaled.
- **Phase 1 Wish Crystallization: contract-level checkpoint; AUTORUN cannot skip.** The dialogue *is* the deliverable's foundation (same tier as `spec` dialogue).
- Standard Ask First tiers (L4 security / destructive / 10+ files) apply unchanged to the wrapped generator.
- On a Fable 5 hub, the Scarcity Gate subsumes the F8 cost gate — one confirmation, not two.

## 4. Resume

**Checkpoint-resume** (≥ 4 phases): persist the Wish Contract + Ceiling Rubric at Phase 1 exit; at Phase 2 exit persist **the winning candidate's full artifact content plus the salvage-list content** (not just judge scores — Phase 3 resume must never re-run the tournament); persist each cycle's score trajectory + surviving attacks at each Phase 3 cycle boundary. An interrupted wish resumes mid-convergence with its trajectory intact.

---

## 5. Phase Contract (AUTORUN chain template)

```
Phase 0  SCARCITY GATE ★Confirm-before-launch (always)
         Nexus[classify + Wish Ledger check + outcome backfill + preliminary cost]
         → routine task detected → recommend cheaper recipe (override journaled)
   ▼
Phase 1  CRYSTALLIZE ★contract-level dialogue (AUTORUN cannot skip; plan-tier model)
         → Wish Contract (goal + ACs + non-goals + disappointment criteria)
         → Ceiling Rubric (3-5 dims, task-specific score-3 anchors, reachability-checked;
            each disappointment criterion mapped to a score-0 trigger on a dimension)
         → Evaluator roster selected per deliverable class (table below)
   ▼
Phase 2  TOURNAMENT ‖ 3 independent candidates from angles derived at Crystallization
         S/M scope → outline-level competition, winner promoted to one full build
         L/XL scope → 3 full builds (generator flattened per converge-recipe.md §4)
         → judge panel = the Phase 3 Evaluator roster scoring vs the frozen Ceiling Rubric
         → winner + salvage list (informal cherry-pick from runners-up — NOT the graft recipe;
            fed as starting input to Phase 3 cycle 1's Generator, no separate synthesis agent)
   ▼
Phase 3  GAUNTLET-CONVERGE loop ≤ 3 cycles (evaluator-loop-protocol.md machinery,
         ceiling ACCEPT per §2; Generator excluded from Evaluators; Sonnet 5 default)
         every cycle   ‖: independent Evaluators per rubric dim (disappointment criteria
                          fire automatically via their score-0 triggers)
         staged        ‖: refutation panel per _common/ADVERSARIAL_REFUTATION.md — spawned
                          ONLY once all dims ≥ 2 (early cycles are obviously non-ceiling;
                          skeptic spend is reserved for candidates that could be "best
                          achievable"); panel also ratifies candidate ACCEPTs (§2)
   ▼
Phase 4  ONE-SHOT GATE — fresh-context independent verifier (plan-tier model), spawned with
         ONLY the Wish Contract + Ceiling Rubric + final artifact — no loop history.
         The information asymmetry is the design: Phase 3 discharges Q9 per-dimension
         inside the loop; this is a SECOND, differently-scoped Q9 application — a holistic
         fresh-eyes redo-value judgment, not rubric re-scoring.
         MATERIALLY-BETTER requires evidence: name (i) a specific dimension currently < 3
         that a redo would plausibly move to 3 with a stated approach, or (ii) a specific
         disappointment-criterion violation in the artifact. A bare "could be better" = NO.
         → MATERIALLY-BETTER → exactly one bonus cycle (hard total 4) → re-gate once;
           the second gate's verdict is ADVISORY ONLY — Phase 5 delivers unconditionally,
           a second MATERIALLY-BETTER becomes a residual-gap note, never another cycle
         → NO → deliver
   ▼
Phase 5  DELIVER — Fulfillment Report + Wish Ledger append (Guardian if code)
```

**Phase 0 — Wish Ledger schema and routine heuristics.** The ledger lives under a `## Wish Ledger` heading in `.agents/nexus.md` (create on first use); Phase 0 counts entries rather than parsing prose:

```yaml
- wish: 3                    # sequence number
  date: 2026-07-16
  intent: "<one-line Wish Contract goal>"
  exit_reason: ACCEPT | diminishing-returns | cap-reached | BLOCK
  dims_at_ceiling: "4/5"
  override: false            # true when the user overrode a routine-task challenge
  outcome: pending           # pending | satisfied | partial | regretted
```

The `outcome` field is backfilled lazily: at the NEXT wish's Phase 0, ask one line — "did wish #N-1 (<date>) satisfy its disappointment criteria?" — giving the Scarcity Gate real signal, not just a counter. **Routine-task heuristics** (any 2 of 3 → routine → challenge): (a) the request maps cleanly onto an existing chain template with no one-shot/irreversibility framing; (b) the phrasing carries none of the wish signal anchors (`reference/signal-keywords.md`); (c) the preliminary cost estimate is within ~2× the natural recipe's own baseline.

**Phase 1 — Ceiling Rubric authoring rules.** 3-5 dimensions; each score-3 descriptor is **task-specific** (never the generic "exceeds best practices"); Magi (or Omen) sanity-checks **reachability** — at least one conceivable exemplar output could score 3 on every dimension — before the rubric freezes. Tournament angles are derived from axes surfaced in the dialogue (default: conservative-proven / aggressive-novel / hybrid; replace with task-specific axes when the dialogue surfaces them).

**Evaluator roster by deliverable class** (default mapping — Phase 1 selects Evaluators matching the contract's actual dimensions; a dimension with no matching specialist gets a purpose-prompted general evaluator, still Generator-excluded):

| Deliverable class | Dimension → Evaluator defaults |
|-------------------|--------------------------------|
| Code / feature | correctness→Radar · code quality→Judge · UX→Echo/Palette · spec conformance→Attest · E2E→Voyager |
| Document | Doc Quality Gate W12 (`doc-quality-protocol.md`) as a dimension · grounding→Attest · standards→Canon |
| Plan / strategy | trade-off soundness→Magi · market/competitive fit→Helm/Compete · internal consistency→Attest |

## 6. Output Report — **Fulfillment Report** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Wish Contract recap** — goal, ACs, disappointment criteria, each classified per Acceptance Provenance (Q15)
- **Score trajectory** — per-cycle weighted scores per dimension; ceiling dims reached vs plateaued
- **Gauntlet ledger** — refutations raised / killed / survived-then-fixed; **open attacks listed explicitly on any plateau-with-open-attacks exit**
- **One-Shot Gate verdict** — redo assessment with its cited evidence + bonus-cycle usage (+ advisory second verdict if any)
- **Exit reason** (§2 vocabulary) + residual gap vs ceiling (empty only on ACCEPT)
- **Wish Ledger entry** — the §5 schema entry as recorded (`outcome: pending`)

## 7. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Wish inflation ("everything is a lifetime request") | Scarcity Gate: ledger count + prior outcomes surfaced + 2-of-3 routine heuristics (Phase 0) |
| Solving the stated ask, missing the true wish | Crystallization dialogue + disappointment criteria (Phase 1, contract-level) |
| "Best quality" left undefined → vibe acceptance | Ceiling Rubric frozen at Phase 1 with task-specific score-3 anchors + reachability check |
| Unreachable-by-construction or trivially-reachable ceiling | Magi/Omen reachability sanity check before rubric freeze (Phase 1) |
| First-idea anchoring (one attempt iterated) | Tournament: 3 independent diverse-angle candidates + salvage from runners-up (Phase 2) |
| Tournament cost blowup on small deliverables | S/M scope competes at outline level; only L/XL justifies 3 full builds (Phase 2) |
| Plausible-but-not-actually-best output | Staged adversarial refutation panel once dims ≥ 2 + ratification of candidate ACCEPTs (Phase 3) |
| Dual-oracle conflict (rubric vs refutation state) | Single oracle ladder: dims = 3 → candidate ACCEPT → panel ratifies or demotes (§2) |
| Plateau exit masking open attacks | `diminishing-returns` with survivors > 0 must report as plateau-with-open-attacks (§2, §6) |
| Disappointment criterion silently regressing mid-loop | Each criterion is a score-0 trigger on a rubric dimension (Phase 1 mapping; Phase 3 Evaluators check every cycle) |
| Evaluator mis-fit for non-code deliverables | Deliverable-class roster table + Phase 1 roster selection rule (§5) |
| Generator grades its own work | GAN separation per `evaluator-loop-protocol.md`; One-Shot Gate verifier is fresh-context (Q9, second application) |
| Unbounded pursuit of an unreachable ceiling | loop ≤ 3 (+1 bonus, hard total 4) + honorable diminishing-returns exit (§2); second gate verdict advisory-only |
| Loop-on-loop blowup when the inner task is apex/kaizen/summit-shaped | Flatten rule cited from `converge-recipe.md` §4 — wish owns the single loop |
| Silent under-delivery on a one-shot | Fulfillment Report residual-gap section; non-ACCEPT exits always report best-so-far |

## 8. Shared-Protocol References

| Protocol | What wish takes from it | Wish-specific specialization |
|----------|------------------------|------------------------------|
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, score scale, aggregation, Δ < 0.2 | ACCEPT raised to all dims = 3 with panel ratification (§2) |
| `reference/converge-recipe.md` §4 | Flatten rule for loop-owning inner recipes | — |
| `reference/dialogue-protocol.md` | Question craft, Assumption Ledger, checkpoint presentation | Disappointment-criteria excavation is **wish-original** (not defined in the protocol) — built on its question-craft rules |
| `_common/ADVERSARIAL_REFUTATION.md` | Skeptic panel, polarity, exclusions | Target claim = "this is the best achievable output"; staged (dims ≥ 2 only) + ratification duty |
| `reference/autonomy-quality-protocol.md` | Intent contract (Q1-Q3), producer ≠ verifier (Q9), Acceptance Provenance (Q15) | Q9 discharged twice by design: per-dimension in Phase 3, then a fresh-context holistic second application at the One-Shot Gate |
| `reference/doc-quality-protocol.md` | W1-W12 for document deliverables | W12 becomes a rubric dimension |

## 9. Decision Tree vs Neighbors

```
User frames the request as their single most important ask / one-shot / favor of a lifetime?
  NO  → the natural recipe for the task shape (feature/bug/package/…)
  YES ↓
Is it strategic/release-critical CODE work wanting multi-engine triangulation?
  YES → summit (wish's Scarcity Gate will recommend this itself)
  NO ↓
Is "good enough" (all dims ≥ 2) actually acceptable, with revision chances later?
  YES → converge (standard bar, cheaper)
  NO ↓
Scarcity Gate: does the ledger show wish used recently for routine work?
  YES → challenge + recommend cheaper recipe (user may override, journaled)
  NO  → wish — crystallize → tournament → gauntlet-converge → One-Shot Gate → deliver
```
