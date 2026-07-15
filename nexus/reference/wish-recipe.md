# Wish Recipe — Once-in-a-Lifetime Request

> `/nexus wish "<request>"` — the **scarcity-gated, one-shot, quality-ceiling** delivery recipe. The invocation itself carries the semantics of a lifetime plea: the requester stakes everything on this ONE output, and the executor answers with maximum earnestness — no "we'll fix it in the next iteration," no routine-quality shortcuts. Deliverable-agnostic: the underlying task (code, document, design, content, plan) is routed to its natural generator, then wrapped in wish machinery — crystallization dialogue, tournament generation, adversarial gauntlet, ceiling convergence, and a final One-Shot Gate.

Read this file before executing the `wish` Recipe.

---

## 1. Nature / When to Use / Boundaries

**Wish is a quality-ceiling wrapper, not a task shape.** Its identity comes from four things no sibling recipe carries together:

1. **Scarcity Gate** — "once-in-a-lifetime" is operationalized: usage is journaled and surfaced ("this is wish #N; last used <date>"), and the recipe *challenges* invocations that don't merit lifetime-request cost. A wish invoked weekly is not a wish; anti-inflation is part of the contract.
2. **Ceiling ACCEPT** — the convergence bar is raised from converge's `all dims ≥ 2` to **`all dims = 3`** (the rubric ceiling). Wish is the only recipe that targets the top of the scale by contract.
3. **Wish Crystallization** — a contract-level dialogue excavates the *true* wish behind the words, including explicit **disappointment criteria** ("what outcome would make you regret spending your lifetime request?").
4. **One-Shot Gate** — before delivery, an independent verifier answers "would a fresh redo be *materially* better than this?" — because there is no second delivery.

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

Scale: **10-30 agents × ≤4 cycles, 5-15× `feature` cost** (deliverable-dependent; the wrapped generator dominates). **Confirm-before-launch always** (intentional — same unconditional gate as `summit`; the Scarcity Gate is that confirmation).

---

## 2. Termination Bound

Convergence **loop ≤ N cycles (default N=3)**, plus the One-Shot Gate may grant **exactly one bonus cycle** — hard total 4. Exit reasons use the canonical vocabulary:

| Exit reason | Wish-specific meaning |
|-------------|----------------------|
| `ACCEPT` / `target-met` | **all scored rubric dimensions = 3** (ceiling — deliberately above the protocol's ≥ 2 default) AND the refutation panel's surviving attacks = 0 |
| `diminishing-returns (Δ < ε)` | weighted score Δ < 0.2 between cycles (`evaluator-loop-protocol.md` values verbatim) |
| `cap-reached` | 3 cycles (+ ≤1 bonus) without ceiling ACCEPT |
| `BLOCK` | un-fixable within scope, or Agent Tennis — escalate |

On any non-`ACCEPT` exit the recipe reports **best-so-far + the residual gap vs the ceiling** — a wish never ends silently. Because the ceiling is often unreachable, `diminishing-returns` is an *honorable* exit: the Fulfillment Report states exactly which dimensions plateaued below 3 and why.

## 3. Confirm / Safety Gate

- **Phase 0 Scarcity Gate: Confirm before launch — always** (unconditional, intentional parity with summit's gate; not drift). The prompt surfaces: wish ledger count + last-use date, estimated cost envelope, and — when the task classifies as routine — an explicit recommendation of the cheaper recipe. The user may override; the override is journaled.
- **Phase 1 Wish Crystallization: contract-level checkpoint; AUTORUN cannot skip.** The dialogue *is* the deliverable's foundation (same tier as `spec` dialogue).
- Standard Ask First tiers (L4 security / destructive / 10+ files) apply unchanged to the wrapped generator.
- On a Fable 5 hub, the Scarcity Gate subsumes the F8 cost gate — one confirmation, not two.

## 4. Resume

**Checkpoint-resume** (≥ 4 phases): persist the Wish Contract + Ceiling Rubric at Phase 1 exit, tournament candidates + judge scores at Phase 2 exit, and each cycle's score trajectory + surviving refutations at each Phase 3 cycle boundary. An interrupted wish resumes mid-convergence with its trajectory intact — a lifetime request is never restarted from zero.

---

## 5. Phase Contract (AUTORUN chain template)

```
Phase 0  SCARCITY GATE ★Confirm-before-launch (always)
         Nexus[classify + wish-ledger check (.agents/nexus.md) + cost envelope]
         → routine task detected → recommend cheaper recipe (override journaled)
   ▼
Phase 1  CRYSTALLIZE ★contract-level dialogue (AUTORUN cannot skip)
         dialogue per reference/dialogue-protocol.md:
         true wish behind the words · what "best" means HERE · disappointment criteria
         → Wish Contract (goal + ACs + non-goals + disappointment criteria)
         → Ceiling Rubric (0-3 dims; ACCEPT = all dims = 3)
   ▼
Phase 2  TOURNAMENT ‖ 3 independent candidates from assigned diverse angles
         (generator = the task's natural recipe/agents, flattened per
          converge-recipe.md §4 when the inner recipe owns a loop)
         → judge panel scores vs Ceiling Rubric → winner + graft list from runners-up
   ▼
Phase 3  GAUNTLET-CONVERGE loop ≤ 3 cycles (evaluator-loop-protocol.md machinery,
         ceiling ACCEPT per §2 above; Generator excluded from Evaluators)
         each cycle ‖: independent Evaluators per rubric dim
                    ‖: refutation panel per _common/ADVERSARIAL_REFUTATION.md —
                       skeptics attack "this is the best achievable";
                       each surviving refutation → feedback δ for next cycle
   ▼
Phase 4  ONE-SHOT GATE — independent verifier (producer ≠ verifier, Q9):
         disappointment-criteria sweep vs Wish Contract
         + verdict "would a fresh redo be MATERIALLY better?"
         → MATERIALLY-BETTER → exactly one bonus cycle (hard total 4) → re-gate once
         → NO → deliver
   ▼
Phase 5  DELIVER — Fulfillment Report + wish-ledger append (Guardian if code)
```

**Evaluator topology** and score aggregation are the protocol's (`evaluator-loop-protocol.md`) — wish adds only the ceiling ACCEPT and the parallel refutation panel. Default dimension → Evaluator mapping (Radar/Judge/Echo/Palette/Attest/Voyager) applies per deliverable type; document deliverables add the `doc-quality-protocol.md` W12 gate as a rubric dimension.

---

## 6. Output Report — **Fulfillment Report** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Wish Contract recap** — goal, ACs, disappointment criteria, each classified per Acceptance Provenance (Q15)
- **Score trajectory** — per-cycle weighted scores per dimension; ceiling dims reached vs plateaued
- **Gauntlet ledger** — refutations raised / killed / survived-then-fixed
- **One-Shot Gate verdict** — redo assessment + bonus-cycle usage
- **Exit reason** (§2 vocabulary) + residual gap vs ceiling (empty only on ACCEPT)
- **Wish ledger** — this invocation's entry (#N, date, exit reason)

## 7. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Wish inflation ("everything is a lifetime request") | Scarcity Gate: journaled usage count surfaced + routine-task challenge (Phase 0) |
| Solving the stated ask, missing the true wish | Crystallization dialogue + disappointment criteria (Phase 1, contract-level) |
| "Best quality" left undefined → vibe acceptance | Ceiling Rubric frozen at Phase 1; ACCEPT = all dims = 3, cited every cycle |
| First-idea anchoring (one attempt iterated) | Tournament: 3 independent diverse-angle candidates + graft from runners-up (Phase 2) |
| Plausible-but-not-actually-best output | Adversarial refutation panel attacks "best achievable" every cycle (Phase 3) |
| Generator grades its own work | GAN separation per `evaluator-loop-protocol.md`; One-Shot Gate verifier is also independent (Q9) |
| Unbounded pursuit of an unreachable ceiling | loop ≤ 3 (+1 bonus, hard total 4) + diminishing-returns Δ < 0.2 honorable exit (§2) |
| Loop-on-loop blowup when the inner task is apex/kaizen/summit-shaped | Flatten rule cited from `converge-recipe.md` §4 — wish owns the single loop |
| Silent under-delivery on a one-shot | Fulfillment Report residual-gap section + non-ACCEPT exits always report best-so-far |

## 8. Shared-Protocol References

| Protocol | What wish takes from it | Wish-specific specialization |
|----------|------------------------|------------------------------|
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, score scale, aggregation, Δ < 0.2 | ACCEPT raised to all dims = 3 (§2) |
| `reference/converge-recipe.md` §4 | Flatten rule for loop-owning inner recipes | — |
| `reference/dialogue-protocol.md` | Question craft, Assumption Ledger, checkpoint presentation | Disappointment-criteria excavation (Phase 1) |
| `_common/ADVERSARIAL_REFUTATION.md` | Skeptic panel, polarity, exclusions | Target claim = "this is the best achievable output" |
| `reference/autonomy-quality-protocol.md` | Intent contract (Q1-Q3), producer ≠ verifier (Q9), Acceptance Provenance (Q15) | One-Shot Gate implements Q9 at delivery |
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
