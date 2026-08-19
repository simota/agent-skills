# Converge Recipe — Quality-Convergence Loop

> `/nexus converge` — iterate a deliverable to convergence via **Generator-Evaluator separation**: a Generator produces/revises, **independent** Evaluators score it against a Rubric tied to a Sprint Contract, and the loop runs until **ACCEPT** or a hard termination bound. This is the invocable entry point for `reference/evaluator-loop-protocol.md` — it adds nothing to that protocol except **explicit termination bounds** and an invocation surface.

Read this file before executing the `converge` Recipe. The two invocation forms, the flatten rule for loop-recipes, and the termination contract are defined here. The Contract / Rubric / Generator-Evaluator triangle itself lives in `reference/evaluator-loop-protocol.md` — read that for the spec.

---

## 1. Nature / When to Use / Boundaries

**Converge is execution control, not a task shape** (Recipes are normally task shapes — converge is the exception, exposed as a subcommand because the Mode table carries only confirmation cadence, and converge needs to carry args: a Contract, a Rubric, and bounds). It wraps *iteration* around a generator.

Use `converge` when a single deliverable must reach a **rubric-defined quality bar** through iteration, with the integrity guarantee that **the generator never grades its own work**. If one pass suffices, you do not need it.

**Two invocation forms:**

| Form | Meaning |
|------|---------|
| `converge` (standalone) | An existing/target deliverable + a Rubric; iterate Generator↔Evaluator to convergence. |
| `converge <recipe> …` | Run the inner Recipe as the per-cycle **Generator**, with converge owning the loop and termination. **Subject to the flatten rule (§4).** |

| Not this | Route to | Why |
|----------|----------|-----|
| Existing shipped feature, improve vs a **metric** (perf/UX/quality) | `kaizen` | Metric-target PDCA, not rubric Generator-Evaluator |
| **Unattended** long-running loop setup (oracle + hard-stop, no code run) | `goal` | converge is attended, in-session, and actually runs generators/evaluators |
| Full implementation discovery→ship with an internal loop | `apex` | converge exposes only the loop, for a single deliverable |
| Just need the pattern spec, not an invocation | read `evaluator-loop-protocol.md` | converge *executes* it; the protocol *defines* it |

Scale: 4-10 agents × cycles (cap 3 default). Mid cost (multiplied by cycle count). **Confirm before launch when `max_cycles` is raised above 3, or when a wrapped Tier-S recipe is the generator.**

---

## 2. Termination Contract — the integrity backbone

The bare evaluator-loop can run forever or devolve into "Agent Tennis" (Generator and Evaluator disagreeing without progress). Converge's entire reason to be a Recipe rather than a loose pattern is that it **mandates a provable stop**. Every run declares all four bounds up front:

| Bound | Default | Stop behavior |
|-------|---------|---------------|
| `max_cycles` | 3 | Hard ceiling — stop + report best-so-far. Raising > 3 is **Confirm-before-launch**. |
| `token_budget` | run-level | Stop + report when exhausted (shared pool, not per-cycle). |
| diminishing-returns | **weighted score Δ < 0.2 between cycles** (`evaluator-loop-protocol.md` termination table) | If the aggregate weighted rubric score improves by < 0.2 versus the prior cycle, stop + report (further iteration not worth it). |
| `BLOCK` escalation | — | If Aggregate verdict is BLOCK (un-fixable within scope, or Agent Tennis), stop + escalate to user. Agent Tennis = Nexus core circuit-breaker definition: two agents disagreeing on the same point 3+ turns without progress. |

**ACCEPT condition is the protocol's, not a new one:** `ACCEPT` iff **every scored rubric dimension ≥ 2** (`evaluator-loop-protocol.md` Score Scale / Aggregation). This is the only *success* exit; diminishing / max_cycles / budget / BLOCK are *bounded* exits that still deliver the best result with an honest convergence report. No run is unbounded.

---

## 3. Phase Contract (AUTORUN chain template)

```
CONTRACT ── Scribe[unified: author the Sprint Contract (acceptance spec) + Rubric (0-3 dims)]
            (skip authoring if caller supplies both; else generate before the loop)
   ▼
┌─ LOOP (until ACCEPT | bound hit per §2) ───────────────────────────────────┐
│  GENERATE   inner recipe (flattened per §4) OR task agent[produce / revise] │
│  EVALUATE ∥ one independent Evaluator per scored rubric dimension           │
│             ★ the Generator MUST NOT be an Evaluator (GAN separation)        │
│  AGGREGATE  Magi[all dims ≥ 2 → ACCEPT | any dim < 2 → REVISE(feedback δ)    │
│             | any Evaluator BLOCK or persistent split → BLOCK]               │
│  GATE  ACCEPT (all dims ≥ 2) → exit loop                                     │
│        REVISE → carry feedback δ into next cycle's GENERATE                  │
│        Δweighted<0.2 (diminishing) → stop+report ; max_cycles/budget → stop  │
│        BLOCK → stop + escalate                                              │
└────────────────────────────────────────────────────────────────────────────┘
   ▼
DELIVER ── convergence report: cycles run, per-cycle score trajectory,
           exit reason (ACCEPT | DIMINISHING | MAX_CYCLES | BUDGET | BLOCK),
           final verdict + residual gaps
```

**Evaluator topology = one Evaluator per scored rubric dimension** (not a voting panel — verdict aggregates by "all dimensions ≥ 2", per `evaluator-loop-protocol.md`). **Default dimension → Evaluator:** correctness/regression → `Radar`; code quality → `Judge`; UX/usability → `Echo`/`Palette`; spec conformance → `Attest`; E2E behavior → `Voyager`. Score only the dimensions the Rubric declares. Evaluators run concurrently (hub-spoke, no shared mutable state); the Generator of cycle N is excluded from cycle N's Evaluator set. **BLOCK aggregation:** any Evaluator returning BLOCK, or a dimension stuck in REVISE across cycles without score gain (Agent Tennis), escalates the whole run to BLOCK.

**Checkpoint-resume:** persist the Contract, Rubric, and each cycle's score + feedback δ at the GATE boundary so an interrupted run resumes mid-convergence with its trajectory intact.

---

## 3a. Loop Precondition Gate

Run `_common/LOOP_PRECONDITIONS.md` before cycle 1. Two of the five are structural here and pass by construction — #3 (maker ≠ checker) via Generator-Evaluator separation, #2 (hard-stop bound) via `max_cycles` — so the gate reduces to confirming #1 (the rubric *is* the completion oracle; a rubric with no score-3 anchor fails it), #4, and #5. Report the verdict in the Convergence Report.

## 4. Flatten Rule — wrapping a loop-recipe

`converge <recipe>` runs the inner recipe as the Generator. But several recipes **own their own termination loop** (`kaizen` = PDCA cap 3, `apex`, `summit`). Nesting two loops causes **cost blowup** (cycles × inner-cycles) and **dueling termination oracles** (inner metric vs outer rubric).

**Rule:**
- **Inner recipe is non-loop** (`feature`, a single build, `transmute` per-module) → true wrapper: the whole inner recipe is the Generator each cycle.
- **Inner recipe is itself a loop** (`kaizen` / `apex` / `summit`) → **flatten**: use the inner recipe's *generator agents*, not its loop. Converge owns the single outer loop and the sole termination contract.

**Which agents flatten cleanly:**
- `kaizen` → **well-defined**: its generator agents are `Bolt`/`Tuner`/`Palette`/etc. (the worked example below).
- `apex` / `summit` → flattening means using only their **build/generation-phase** agents (apex's Builder/loop body; summit's execution-team generators), dropping their internal risk-gate/improvement loops. This is **advanced and rarely worth it** — wrapping summit (28-119 agents) in an outer loop multiplies an already-huge cost. Prefer running apex/summit standalone (they already converge internally) and reserve `converge <recipe>` for non-loop generators.

**Worked example — `converge kaizen`:**
- ❌ Do NOT run full kaizen (its own ≤3 PDCA cycles) inside each converge cycle.
- ✅ Use kaizen's **improvement agents** (`Bolt`/`Tuner`/`Palette`/…) as the GENERATE step. converge's independent Evaluators + Rubric own the gate; kaizen's internal Check is **demoted to a pre-filter** (a cheap self-screen before external scoring), never the termination gate.
- Result: one loop, one oracle, kaizen's improvement muscle + converge's rubric gate + restored Generator≠Evaluator separation (the external evaluator sits above kaizen's self-check).

This flatten rule is what makes "converge kaizen-like" coherent instead of a loop-on-loop anti-pattern.

---

## 5. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| Generator grades its own work (self-assessment bias) | Generator of cycle N excluded from cycle N's Evaluators (GAN separation, §3) |
| Unbounded / forever loop | `max_cycles` + `token_budget` hard bounds (§2) |
| Agent Tennis (disagree without progress) | diminishing-returns Δweighted<0.2 stop + BLOCK escalation via Nexus circuit-breaker (§2) |
| **Inventing a fuzzy ACCEPT/stop oracle** | converge cites the protocol's concrete values verbatim (all dims ≥ 2; Δweighted < 0.2), never new vocabulary (§2, §3) |
| **Loop-on-loop blowup when wrapping kaizen/apex/summit** | Flatten rule (§4): inner generator agents only, converge owns the single loop |
| **Dueling termination oracles** (inner metric vs outer rubric) | Flatten: converge's rubric is the sole gate; inner Check demoted to pre-filter |
| "Looks good" subjective acceptance | Rubric (0-3 graduated dims) replaces vibe; all dimensions ≥ 2 required for ACCEPT |
| Rubric drift mid-loop | Contract + Rubric frozen at CONTRACT phase; cited every cycle |

---

## 6. Decision Tree vs Neighbors

```
Need to iterate a deliverable to a quality bar?
  NO  → single pass → the relevant recipe directly
  YES → bar is a METRIC on an existing shipped feature? → kaizen
        bar is unattended + machine-checkable, setup only? → goal
        bar is a RUBRIC, attended, run generator+independent evaluators now? → converge
          wrapping another recipe as generator? apply the flatten rule (§4)
```

`converge` is the invocable Generator-Evaluator loop with bounds; `kaizen` is metric-PDCA on existing features; `goal` sets up unattended loops; `evaluator-loop-protocol.md` is the spec converge executes.

---

## 7. Output

`NEXUS_COMPLETE` with the standard `## Nexus Execution Report` plus a **Convergence Report**:
- The Sprint Contract + Rubric used (or that the caller supplied them).
- Per-cycle score trajectory (each dimension, 0-3) and the aggregate.
- **Exit reason**: ACCEPT | DIMINISHING | MAX_CYCLES | BUDGET | BLOCK.
- Generator/Evaluator assignment per cycle (proof of separation).
- For `converge <recipe>`: whether the inner recipe was wrapped whole or flattened (§4), and which inner agents served as Generator.
- Residual gaps if exit ≠ ACCEPT.
