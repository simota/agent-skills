# Assay Recipe — Experimental Proof of Design Claims

> `/nexus assay "<scope>"` — *assay*: subject a material to tests to determine what it actually is. Every codebase makes design claims — in its ADRs, its conventions, its folder structure, its roadmap — and the roster currently **judges** those claims (`atlas` points, `void` proposes, `anneal` prioritizes) without ever **settling** one. Assay takes the load-bearing claims, freezes them as a denominator, and resolves each by an **executed experiment**: add a change and see if it stays local, remove an element and see if anything breaks, rewrite a hotspot and see if it gets simpler, assert a rule and machine-check it everywhere. One oracle: **zero unproven load-bearing claims**.

Read this file before executing the `assay` Recipe.

---

## 1. Nature / When to Use / Boundaries

**"Is this a good design?" has never had an oracle.** It is answered with proxies — coupling metrics, complexity scores, review opinions, a specialist's judgment. Every one of those is a *prediction* about how the code will behave under change, removal, simplification, or rule-checking, and none of them runs the experiment that would settle it. `anneal` is the closest sibling and it is explicitly a *discovery-and-fix* recipe: it surfaces undiagnosed weaknesses from six independent lenses, ranks them by value × risk, and brushes up the top-N. It never asks whether the design's own stated claims are true, and it never proves anything by construction.

Assay's identity is four things no sibling carries together:

1. **The Design Claim Ledger.** Design claims are harvested and frozen as an explicit denominator — from ADRs, architecture docs, and stated conventions, but also from what the code **implicitly claims** (a `domain/` directory claims independence; a plugin interface claims extensibility) and from the roadmap (a planned feature claims "this will be cheap to add"). `anneal` looks for weaknesses; assay looks for **claims**, which is why the two compose rather than overlap.
2. **Four instruments, one ledger.** `ADD` · `SUBTRACT` · `REWRITE` · `ASSERT`. Which instrument a claim gets is determined by the claim's *type*, mechanically — there is no discretion at assignment, because instrument choice is where a design proof would otherwise become a design opinion.
3. **The Adequacy Gate.** All four instruments read the test suite as their sensor. A removal whose diff is zero means "unnecessary" only if the suite actually exercises that element; otherwise it means **"untested"** — a completely different finding, and conflating them is how a design proof produces a dangerous deletion. Phase 0.5 establishes per-element oracle adequacy before any instrument runs, and a scope that cannot support any experiment exits `BLOCK (oracle-inadequate)` with a map of exactly where the codebase is blind.
4. **Refuted is a success.** The oracle counts *unresolved* claims, not *failed* ones. Discovering that a design's central claim is false is the recipe working. The only failure state is "we still do not know."

### Use `assay` for

- A codebase whose design everyone has an opinion about and nobody has evidence for.
- Before a large investment (a rewrite, a re-architecture, an acquisition/due-diligence read) where the stated design needs to be true, not plausible.
- Upstream of `anneal`: assay supplies **measured** value × risk instead of estimated, and hands its refuted claims over as a pre-evidenced slate.
- Settling a recurring architectural argument — the ledger and its experiments outlive the argument.
- Auditing whether a *previous* refactor achieved what it claimed.

### Not this — route to

| Not this | Route to | Why |
|----------|----------|-----|
| Discover undiagnosed design weaknesses and **fix** the prioritized slate | `anneal` | Discovery + repair; assay proves claims and repairs only what its own experiments proved safe. **`assay` → `anneal` is a measure→fix pair** |
| Apply a **known** internal restructure to a known target | `refactor` | Nothing to prove; the decision is already made |
| Adjudicate a PR for merge | `acceptance` / `summit` | Change-scoped gates; assay is codebase-scoped and change-independent |
| Predict the blast radius of a change **without implementing it** | `ripple` (skill) | Assay's ADD instrument implements the change to measure it; ripple estimates |
| Run mutation/load/chaos testing as the goal | `siege` (skill) | Assay *uses* siege at Phase 0.5 as its adequacy sensor |
| Raise coverage / repair flaky tests | `radar` (skill) | The remedy assay recommends on `BLOCK (oracle-inadequate)` |
| Report spec ↔ implementation conformance | `attest` / `pdm` | Conformance to a *written spec*; assay proves *design* claims, most of which are unwritten |
| Prove token/component conformance in the UI | `lattice` | Same ASSERT shape, visual denominator |
| Cross-language rewrite / change completeness | `transmute` / `migrate` | Different object entirely |
| Cut scope / propose YAGNI removals | `void` (skill), `trim` | Propose-only; assay's SUBTRACT instrument **executes** the removal experiment. **Judged vs experimented is the boundary** |

**Scale: 24-55 agents, 8-16× `feature` cost.** Per-phase: P0 ≈ 1 · P0.5 ≈ 2-4 (mutation + coverage per candidate element) · P1 ≈ 4-7 (claim harvest across doc, code, and history sources) · P2 ≈ 1 (mechanical assignment, plan-tier) · P3 ≈ 12-27 (ADD 3-6 rehearsals · SUBTRACT 3-8 element batches · REWRITE 3 panelists × 1-3 hotspots · ASSERT 2-4) · P4 ≈ 3-5 adjudicators · P5 ≈ 0 (`apply=false`) or 2-4 · P6 ≈ 1.

*Range derivation* (convention: `reference/recipe-contract.md` §1 element 7): floor = narrow scope, `apply=false`, no re-experiment → 1+2+4+1+12+3+0+1 = **24**; ceiling = whole-codebase scope, `apply=true`, one re-experiment round (+5) → 1+4+7+1+27+5+4+1+5 = **55**. **Confirm-before-launch always** (intentional parity with `wish`/`summit`/`eureka`) **with a declared budget envelope**; `apply=true` confirms a **second** time at Phase 5.

**Model selection (Plan-and-Execute):** Phase 1 claim harvesting, Phase 2 instrument assignment, and the Phase 4 adjudication are judgment-heavy → plan-tier (opus / Fable 5). Experiment execution (rehearsal implementations, removals, rewrites, fitness-function authoring) → Sonnet 5 default. The REWRITE panel is **engine-diverse where the hub allows** (`_common/CLI_COMPATIBILITY.md §4`) — three attempts from one model family are three framings of one set of priors, and "nobody could simplify it" is only evidence if the somebodies were independent.

### 1a. Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus assay "<scope>"` | **Proof-only (default, `apply=false`).** Phases 0-4, 6. Ships the Design Proof; every refuted claim is handed to `anneal`. |
| `/nexus assay "<scope>" apply=true` | **Proof + constructive apply.** Adds Phase 5: applies **only** changes whose safety the experiment itself established — a removal whose diff was zero under an adequate oracle, a REWRITE winner that passed the identical suite. Everything else still routes to `anneal`. |

`apply=true` is **opt-in and never inferred** — proving a claim false is not authorization to act on it, and the two decisions are made on different information (mirrors `eureka ship=true`).

---

## 2. Termination Bound

**`loop ≤ 2 experiment rounds per claim`** — an inconclusive or invalid experiment may be re-designed **once**, because an instrument defect and a design defect are different findings and the first must not be reported as the second. The run as a whole is bounded by the Phase 1 claim cap (top-N load-bearing claims, N declared at Phase 0), not by a global cycle count.

Exit reasons use the canonical vocabulary:

| Exit reason | Assay-specific meaning |
|-------------|-----------------------|
| `ACCEPT` / `target-met` | **zero `UNPROVEN` load-bearing claims** — every claim in the frozen ledger is `PROVEN` or `REFUTED`, each with its experiment attached. `REFUTED` counts toward ACCEPT: the oracle measures resolution, not favorability |
| `diminishing-returns (Δ < ε)` | an experiment round resolved **no new claim** — report each remaining `UNPROVEN` claim with the instrument that failed on it and why |
| `cap-reached` | the second round closed with claims still `UNPROVEN` → deliver the ledger with each unresolved claim **named** and its blocker classified `instrument-limited` / `oracle-limited` / `scope-limited` |
| `budget-reached` | the declared envelope ceiling hit mid-run → deliver resolved claims plus the unresolved list; never a silent overrun and never an unrequested one |
| `BLOCK` | **`oracle-inadequate`** — Phase 0.5 found the suite cannot support *any* instrument on this scope. A **legitimate delivery, not a failure**: the run ships the **blind-spot map** (which elements have no behavioral coverage, ranked by blast radius) and routes to `radar`/`siege`. Knowing precisely where a codebase cannot be reasoned about is a real answer to "is this a good design" — arguably the most important one |

On any non-`ACCEPT` exit the recipe reports resolved vs unresolved **by claim name**. A percentage is never reported alone: "78% of claims resolved" hides which load-bearing claim is still a guess, and that is the only actionable fact.

## 3. Confirm / Safety Gate

- **Phase 0 framing: Confirm before launch — always** (unconditional; intentional parity with `wish`/`summit`/`eureka`, not drift). Surfaces: the scope, the claim cap N, the instrument mix, the **budget envelope**, and — when the request is really "find and fix what's wrong" rather than "prove what we claim" — an explicit recommendation of `anneal` instead.
- **Phase 1 Claim Ledger: contract-level checkpoint; AUTORUN cannot skip.** The ledger *is* the denominator. A claim the user does not recognize as theirs produces a proof about a design nobody holds; a missing load-bearing claim makes an `ACCEPT` meaningless.
- **Phase 3 SUBTRACT experiments: Ask First (destructive).** A removal experiment deletes code. It runs on a throwaway branch/worktree by contract, but the blast-radius gate applies as it would to any write.
- **Phase 3 ADD experiments: the rehearsal implementations are discarded by contract.** They are measurement apparatus, not deliverables — carrying one forward into the working tree is a contract violation, not a shortcut (§6).
- **Phase 5 apply (`apply=true` only): Confirm before launch — unconditional; blocks in `AUTORUN`/`AUTORUN_FULL`.** The first gate authorized spending on *knowledge*; this one authorizes *changing the codebase*, on different information. Preconditions, checked in order — the first miss ends the run at Phase 6 with the failed precondition named:

  | # | Precondition | Why a miss forbids applying |
  |---|--------------|------------------------------|
  | ① | The change was produced **by** an experiment, not designed after it | Anything else is an unproven edit wearing a proof's badge — route to `anneal` |
  | ② | The relevant element passed the Phase 0.5 Adequacy Gate | A zero-diff removal on an unexercised element is "untested", not "safe" (§1.3) |
  | ③ | Exit reason is not `BLOCK (oracle-inadequate)` | The sensor was unreliable for the whole scope |
  | ④ | A separate apply budget is declared and confirmed | The proof envelope is already spent |

- Standard Ask First tiers (L4 security / destructive / 10+ files) apply unchanged.
- On a Fable 5 hub the Phase 0 gate subsumes the F8 cost gate — one confirmation, not two.

## 4. Resume

**Checkpoint-resume** (≥ 4 phases; `assay resume`): persist the **Adequacy Gate results** at Phase 0.5 exit (re-running mutation testing on resume is both the most expensive re-spend in the recipe and a risk of a *different* adequacy verdict, which would silently move what "unnecessary" means); persist the **frozen Claim Ledger** at Phase 1 exit — re-harvesting is how a denominator quietly shrinks; persist per-claim experiment state, verdicts, and discarded-rehearsal confirmations at each Phase 3 boundary. A resumed run re-experiments only `UNPROVEN` claims; Phase 4 always adjudicates the **full** ledger.

---

## 5. Phase Contract (AUTORUN chain template)

```
Phase 0    FRAMING ★Confirm-before-launch (always)
           Nexus[scope + claim cap N + instrument mix + BUDGET ENVELOPE + apply mode
                + cheaper-path recommendation → anneal when the ask is "find and fix"]
   ▼
Phase 0.5  ADEQUACY GATE                          [every instrument reads the suite as its sensor]
           Siege[mutation testing on candidate elements] ‖ Radar[behavioral coverage map]
           → per-element ADEQUATE / BLIND verdict, ranked by blast radius
           → NO element adequate on this scope → EXIT `BLOCK (oracle-inadequate)`:
             ship the BLIND-SPOT MAP + route to radar/siege (a legitimate delivery, §2)
           → partial adequacy → instruments are restricted to adequate elements; BLIND elements
             are recorded as `oracle-limited`, never silently experimented on
   ▼
Phase 1    CLAIM HARVEST ★contract-level checkpoint (AUTORUN cannot skip; plan-tier)
           Atlas[architecture claims: layering, boundaries, dependency direction]
           ‖ Lens[what the code structure implicitly claims — a `domain/` dir claims
             independence; a plugin seam claims extensibility]
           ‖ Grove?[structural claims] ‖ Trail[claims the history implies: "this area is stable"]
           ‖ doc sweep [ADRs, README, CONTRIBUTING, conventions] ‖ roadmap
             [planned work implies "this will be cheap to add"]
           → DESIGN CLAIM LEDGER: `id / claim / source / type / blast-radius / load-bearing?`
           → top-N load-bearing claims selected by blast radius → ✓user ratifies
             → the DENOMINATOR FREEZES (deferred claims recorded, never silently dropped)
   ▼
Phase 2    INSTRUMENT ASSIGNMENT (mechanical — claim TYPE determines the instrument, §6)
           change-cost claim  → ADD        necessity claim   → SUBTRACT
           complexity claim   → REWRITE    rule claim        → ASSERT
           → a claim matching no instrument is recorded `instrument-limited` and NOT
             adjudicated by opinion — an unmeasurable claim stays unproven, by contract
   ▼
Phase 3    EXPERIMENT ‖ pipeline — per claim, independently, NO barrier between instruments
           ADD      : Trail/roadmap-sourced real changes ×3-6 → each implemented by an
                      independent agent in a THROWAWAY worktree (isolation: worktree)
                      → measure files touched · layers crossed · locality · unrelated-test
                        breakage · turns → IMPLEMENTATIONS DISCARDED (§6)
           SUBTRACT : remove the element on a throwaway branch ★Ask First → build + suite +
                      behavioral diff per _common/DIFFERENTIAL_PARITY.md (two-reading split: §1.3)
                      → zero diff ∧ ADEQUATE → UNNECESSARY (refutes the necessity claim)
                      → zero diff ∧ BLIND     → UNTESTED (`oracle-limited`)
                      → diff present           → NECESSARY, and the failing test IS the
                        recorded reason the element exists
           REWRITE  : pre-committed, engine-diverse panel (3) attempts a simpler implementation
                      passing the IDENTICAL suite, each blind to the others
                      → any success → ACCIDENTAL complexity (proven by construction)
                      → all fail    → ESSENTIAL complexity (evidenced, with the attempts logged)
           ASSERT   : the claim is compiled into an EXECUTABLE fitness function (import rules,
                      dependency-direction query, boundary check) → full-scope scan
                      → violations classified `violation` (code is wrong) / `constraint-gap`
                        (the rule cannot express reality — the RULE is amended) /
                        `justified` (reason + owner recorded, preserved not erased)
                      → independent re-scan looped UNTIL DRY (2× consecutive zero)
           → inconclusive or invalid experiment → ONE re-design permitted (§2)
   ▼
Phase 4    ADJUDICATE — experimenter ≠ adjudicator (Q9), plan-tier
           each claim → PROVEN | REFUTED | UNPROVEN, each bound to its experiment record
           → an `UNPROVEN` claim may NEVER be closed by argument; the oracle counts it open
           → ACCEPT iff zero UNPROVEN load-bearing claims (§2)
   ▼
Phase 5    APPLY ★Confirm-before-launch (apply=true only; preconditions ①-④ per §3)
           apply ONLY experiment-proven-safe changes (zero-diff removals on adequate elements;
           REWRITE winners that passed the identical suite; ASSERT `constraint-gap` rule
           amendments)
           → Radar[no-regression] + Guardian → Hone?[Drift Sentinel: the ASSERT fitness
             functions become CI checks so the proof does not decay]
   ▼
Phase 6    DELIVER — Design Proof + handoff of every REFUTED claim to `anneal` as a
           pre-evidenced slate
```

## 6. Instrument discipline

- **Assignment is mechanical.** Claim type → instrument, per the Phase 2 table. Letting an agent choose the instrument reintroduces exactly the judgment the recipe exists to replace.
- **Rehearsals are apparatus, not output.** Every ADD implementation is discarded. A rehearsal that looks good is the most tempting contract violation in this recipe: it was written to be *measured*, under no review, against no acceptance criteria. Carrying one forward is forbidden; the change it rehearsed goes through `feature`/`anneal` like any other work.
- **Zero diff has two readings** (§1.3 owns the rule) — the Adequacy Gate, not the instrument, picks between them.
- **The REWRITE panel is pre-committed and blind.** Panelists are briefed and their attempt is scoped *before* seeing each other's work, so "nobody could simplify it" is a reproduction result rather than a consensus (the discipline `eureka` uses for its ordinary-move panel).
- **ASSERT amends rules, not just code.** A constraint that reality contradicts may be the wrong constraint; forcing the code to a wrong rule is worse than the drift. `constraint-gap` is a first-class outcome, and it changes the rule.
- **Justified exceptions are preserved.** An intentional deviation with a recorded reason and an owner is a healthy part of a design; an undocumented one is the defect (inherited from `lattice`).

### 6a. Measurement discipline (stochastic instruments)

Applies when an instrument's verdict comes from a model run, an agent loop, or any benchmark rather than a deterministic check. Sources: `anthropic.com/engineering/demystifying-evals-for-ai-agents` (2026-01-09), `.../infrastructure-noise` (2026-02-05).

- **Declare `pass@k` or `pass^k` before running, never "success rate".** `pass@k` = at least one of k attempts succeeds — right for exploratory claims where one hit settles it. `pass^k` = **all** k attempts succeed — the only honest metric for a claim about production behavior, and it collapses fast (0.9 single-run → 0.59 at `pass^5`). A load-bearing claim proven at `pass@k` is `UNPROVEN`, not proven.
- **A total failure indicts the instrument first.** `0%` across a full run means "the experiment is broken" until the transcript proves otherwise. Read the raw run before recording a refutation.
- **A saturated instrument measures nothing.** At ~100% the instrument only detects regressions; it can no longer discriminate the claim. Record it as `instrument-limited`, do not record the claim as proven.
- **Grade the outcome, not the path.** Checking that the code took a specific route rejects valid alternatives and manufactures false refutations.
- **Environment is an experimental variable.** Resource headroom alone moved Terminal-Bench 2.0 scores by **6 percentage points** (p<0.01). Pin and record CPU/RAM/timeout alongside the measurement, keep the ceiling near 3× per-task spec, and set the guaranteed allocation and the kill threshold separately. **A margin under ~3 points on a stochastic instrument is not a result** — either widen the gap, run across multiple times and days, or record `instrument-limited`.
- **Panels amplify contamination.** A multi-agent configuration produced unintended solutions at **3.7× the single-agent rate** (0.87% vs 0.24%) — including a model that identified the benchmark and decrypted its answer key (`.../eval-awareness-browsecomp`). On the REWRITE panel, treat an anomalously expensive run (»median tokens) as a contamination signal and re-read the transcript before scoring it.

## 7. Output Report — **Design Proof** (named)

Emitted inside `NEXUS_COMPLETE` on top of the base `## Nexus Execution Report`:

- **Adequacy record** — per-element ADEQUATE/BLIND verdict with mutation/coverage evidence, and the **blind-spot map** ranked by blast radius (shipped even on a passing run — it is the map of what this proof could not reach)
- **Design Claim Ledger** — every claim with `source · type · instrument · verdict`, load-bearing set separated from deferred, with the deferral rationale
- **Experiment records** — per claim: what was run, the measurement, and the raw verdict. ADD: files touched / layers crossed / locality / unrelated breakage per rehearsed change. SUBTRACT: diff result + adequacy + the failing test that justifies a `NECESSARY` verdict. REWRITE: each panelist's attempt and outcome. ASSERT: the fitness function, violation classes, and the two-consecutive-zero re-scan record
- **Refuted claims** — the headline section. Each false claim, the experiment that refuted it, and its handoff target
- **Discarded-rehearsal attestation** — confirmation that every ADD implementation was destroyed (§6)
- **Unresolved claims** — each `UNPROVEN` claim **by name**, with `instrument-limited` / `oracle-limited` / `scope-limited`. Never a bare percentage
- **Applied changes** (`apply=true`) — what was applied, which precondition set authorized each, and the no-regression evidence
- **Drift Sentinel** — ASSERT fitness functions installed as CI checks, or the reason none were
- **Exit reason** (§2 vocabulary) + **budget spent vs envelope**
- **Handoff** — the refuted-claim slate for `anneal` (pre-evidenced, so anneal's CRITIQUE phase collapses to validation), coverage gaps for `radar`/`siege`, behavior-changing consequences for `feature`/`migrate`

## 8. Failure Modes Prevented

| Failure | Mitigation |
|---------|-----------|
| **"Good design" asserted from proxy metrics, or an instrument chosen to get the desired answer** | Four instruments that *execute* rather than estimate, oracle counts resolved claims not scores, mechanical claim-type → instrument assignment (§1, Phase 2) |
| **A zero-diff removal read as "unnecessary"** | Adequacy Gate — zero diff on a BLIND element is `UNTESTED`, a different verdict entirely (§1.3) |
| Mutation testing skipped because it is slow, or the proof decays the week after delivery | Phase 0.5 is a gate, not an option, checkpointed so resume never re-spends it (§4); ASSERT fitness functions become CI checks via `hone` (Phase 5, §7) |
| A rehearsal implementation shipped because it looked good | Rehearsals are discarded by contract, with an attestation in the report (§6, §7) |
| An unmeasurable claim adjudicated by opinion, or the denominator chosen after seeing results | `instrument-limited` claims stay `UNPROVEN` and Phase 4 forbids closing by argument; the ledger freezes at the contract-level Phase 1 gate (§1, §3) |
| Refuted claims treated as a failed run, or **a codebase that cannot be reasoned about, reported as fine** | `REFUTED` counts toward `ACCEPT`; `BLOCK (oracle-inadequate)` is a legitimate delivery shipping the blind-spot map (§2) |
| Forcing code to comply with a wrong rule, or intentional exceptions erased as violations | ASSERT's `constraint-gap` (amends the rule) and `justified` (reason + owner, preserved) classes (§6) |
| "Nobody could simplify it" from three prompts to one model, or the experimenter grading its own experiment | REWRITE panel is pre-committed, blind, engine-diverse (§1a, §6); Phase 4 adjudicators are independent of the experimenters (Q9) |
| Proving knowledge then silently changing the codebase, or an unproven edit riding out under a proof's badge | `apply=true` is opt-in with its own confirm and four preconditions, incl. precondition ① — the change must have been *produced by* an experiment (§1a, §3) |
| Instrument defect reported as a design defect, or open-ended spend on a whole-codebase scope | One permitted re-design per claim; claim cap N + budget envelope declared at Phase 0 (§2, §3) |
| Duplicating `anneal` | Claims vs weaknesses; prove vs fix — the pair composes as a measure→fix sequence (§1, §10) |

## 9. Shared-Protocol References

| Protocol | What assay takes from it | Assay-specific specialization |
|----------|-------------------------|-------------------------------|
| `_common/DIFFERENTIAL_PARITY.md` | Parity-over-faith, **oracle adequacy**, comparator/harness discipline | Oracle adequacy is promoted from a caveat to a **gating phase** (0.5); the behavioral diff is the SUBTRACT instrument's verdict |
| `reference/evaluator-loop-protocol.md` | Generator-Evaluator separation, flatten rule, bounded rounds | The Evaluator is an **experiment adjudicator**; the oracle is ledger resolution, not a score threshold |
| `reference/autonomy-quality-protocol.md` | Intent contract (Q1-Q3), Decision Ledger (Q4-Q6), producer ≠ verifier (Q9), evidence-bound claims (Q10), Acceptance Provenance (Q15) | Q10 is the whole recipe: no design claim is reported resolved without its experiment record attached |
| `_common/ADVERSARIAL_REFUTATION.md` | Pre-commitment, blind panels, engine diversity, exclusions | The REWRITE panel refutes "this complexity is essential" **by construction** (producing a simpler implementation) rather than by argument |
| `reference/lattice-recipe.md` | Three-way classification (`violation`/`gap`/`justified`), RESIDUE-GATE until dry, Drift Sentinel | The ASSERT instrument is lattice's machinery applied to **architectural** rules instead of design tokens |
| `reference/anneal-recipe.md` | The design-dimension enumeration, evidence-tied ledger discipline | assay → anneal is a **measure→fix pair**: refuted claims arrive pre-evidenced, so anneal's CRITIQUE collapses to validation |
| `reference/research-grounding.md` | — | `N/A` **with reason**: assay's evidence is generated by executed experiments on the codebase itself, not gathered from external sources |
| `reference/doc-quality-protocol.md` | W1-W12 | Applies to the Design Proof document |
| `reference/verdict-gate.md` | — | `N/A` — assay resolves claims; it delivers no which-feature verdict |
| `_common/CLI_COMPATIBILITY.md §4` | Per-engine model map | The REWRITE panel's engine diversity resolves against it |

## 10. Composition with `anneal` (the measure→fix pair)

```
assay  → proves/refutes the claims → REFUTED slate, pre-evidenced, with measured blast radius
anneal → consumes that slate → prioritizes (now on measured, not estimated, value × risk)
         → brushes up, behavior-preserving → Design Ledger
```

Running `anneal` alone remains correct and is the cheaper default — its CRITIQUE phase discovers weaknesses without needing a claim to test. Running `assay` first is warranted when the *stated* design is what is in question, when the investment downstream is large, or when the team's prioritization is deadlocked on competing opinions. The pair should never be nested as one loop (`converge-recipe.md` §4 flatten rule); they run in sequence, each owning its own gates.

## 11. Decision Tree vs Neighbors

Not sure this is assay's job at all? → §1 Not-this table (weakness discovery → `anneal`, decided restructure → `refactor`, PR review → `acceptance`/`summit`, etc.). The one branch not covered there:

```
Can the test suite detect a behavior change on the elements in question?
  NO        → radar / siege first — assay would exit BLOCK (oracle-inadequate) and say exactly this
  PARTIALLY → assay runs, restricted to adequate elements, BLIND ones recorded oracle-limited
  YES       → assay — harvest claims → freeze → assign instruments → experiment
              (ADD ‖ SUBTRACT ‖ REWRITE ‖ ASSERT) → adjudicate → prove
              → hand the refuted slate to anneal
```
