# `anneal` — Codebase design audit → prioritized behavior-preserving brush-up

**Purpose:** Full phase contract for the `anneal` Recipe — take a codebase (or a scope within it) whose **design** has accumulated undiagnosed weaknesses and loose ends, **surface** them across multiple design dimensions (the enumeration), **prioritize** by value × risk, and **brush them up** with real code changes that **preserve behavior** under a no-regression gate. The corrective, execution-bearing member of the Improve family: where `kaizen` improves *one feature against a target you already chose*, `anneal` **discovers what is wrong with the design across a scope you have not pre-diagnosed, then fixes the prioritized slate**.

**Read when:** Executing the `anneal` Recipe. Authored to `reference/recipe-contract.md` (all 8 elements).

---

## What `anneal` is for

The metaphor is metallurgical annealing: apply a controlled process that **relieves accumulated internal stress** in a structure and leaves it tougher — not a cosmetic polish. A user has a codebase and the sense that *the design has drifted* — abstractions leak, boundaries blur, edge cases are half-handled, conventions diverge, the spec no longer matches the code — but has **not pre-diagnosed exactly what** or **where**. They want a systematic sweep that surfaces the design issues with evidence, ranks them, and **actually brushes up the high-value ones** without breaking what works. The deliverable is **brushed-up code + a named Design Ledger** (issues found → fixed/deferred, Before/After design metrics, residual gap).

`anneal` exists because **design-quality improvement across a scope has a method distinct from the narrower Improve recipes**. `refactor` applies a *known* internal restructure to a *known* target; `optimize` chases a perf number; `kaizen` iterates *one feature* against a *fixed quantified target*; none of them **enumerate undiagnosed design weaknesses across a codebase and then brush up the prioritized slate, behavior-preservingly**. That is exactly a controlled multi-agent protocol: ground the design as-is → critique it from many independent angles → prioritize → fix the slate in a bounded loop → prove no regression + measured design improvement → ship.

**Behavior-preserving by default** (refactor-grade discipline): `anneal` strengthens the *design*, not the *behavior*. A brush-up that silently changes externally-observable behavior is a defect, not an improvement. An issue whose fix *requires* a behavior change is the exception — it is flagged at PRIORITIZE and gated (Ask First), never folded silently into a "design clean-up".

### Default Mode: `AUTORUN`

Each brush-up is scope-bounded and behavior-preserving, so the default Mode is `AUTORUN`, gated by blast radius (see § Confirm / safety gate for the tiers and thresholds; Magi confirms the slate before BRUSH-UP on escalation). Unlike `delve`/`spec`, `anneal` is an **execution** recipe, not a dialogue one — there is no mandatory mid-run conversational checkpoint; its gates are blast-radius gates, not knowledge-junctures.

---

## Target resolution

- **`anneal <target>`** — scopes the audit to a named module / layer / area / package. The default form.
- **`anneal` with no target → whole-codebase design sweep** (the proactive form, analogous to `trim` no-target and `/Nexus` proactive mode but scoped to design quality): MAP builds the full design map, CRITIQUE sweeps every dimension across the repo, and PRIORITIZE caps the BRUSH-UP slate to the **top-N by value × risk** (default 10) with the deferred long-tail recorded — never a silent truncation. No-target runs **default to confirm-before-launch** (a whole-codebase brush-up is higher-stakes than a scoped one) and may escalate to `GUIDED`.
- **`anneal resume`** — re-enter from the last checkpoint (see **Resume**).

---

## Phase contract

`MAP → CRITIQUE → PRIORITIZE → BRUSH-UP → VERIFY → SHIP`

Engine routing follows summit principles throughout: **Codex owns code-gen** (Builder/Zen/Sweep), **Claude owns judgment/measurement** (Lens/Atlas/Canon/Void/Omen/Magi/Ripple/Rank/Radar-gate/Judge/Guardian).

### Phase 1 — MAP (ground the design as-is)
Establish the **real** design before critiquing it — auditing an imagined architecture is the recipe's first failure mode (mirrors `delve` GROUND / `refactor` safety-net). `Lens`[map structure, responsibilities, data flow] unconditionally; +`Atlas`[dependency graph, layering, circular references, God classes, module boundaries] unconditionally (architecture is the headline design surface); +`Grove`?[repo/directory structure] when structure is in scope; +`Trail`?[recent churn / change hotspots — where design stress concentrates, so CRITIQUE digs where it matters]. Output: a **design map** — as-is architecture + responsibilities + hotspots.
- **Scope gate:** under no-target (whole-codebase) or a structural scope, confirm the scope/launch before CRITIQUE (confirm-before-launch). A scoped `anneal <target>` proceeds without a stop.
- **Checkpoint-resume:** see § Resume below.

### Phase 2 — CRITIQUE (the enumeration — multi-dimensional design audit)
The enumeration proper — surface design weaknesses from **independent** angles (hub-spoke, no shared mutable state — independence is what makes the audit broad). Each lens owns one design dimension:
- `Atlas`[**architecture**: coupling/cohesion, layering violations, circular deps, God classes, missing or leaky abstractions, ADR-worthy decisions]
- `Zen`[**code-level design smells**: naming, function shape, duplication, dead abstractions, primitive obsession, magic values]
- `Canon`[**standards / maintainability**: ISO 25010 maintainability, convention/API conformance, with citations]
- `Void`[**over-engineering / YAGNI**: speculative generality, premature abstraction, design that is *too much* — the inverse smell, so BRUSH-UP does not only ever *add* structure]
- `Omen`[**under-specified design**: under-handled edge cases, fragile invariants, missing error/timeout/retry paths, latent race conditions, implicit contracts]
- `Attest`/`PDM`[**specification — spec ↔ code conformance & drift**: does the implementation match its documented spec / contract / acceptance criteria? Separate *the code drifted from intent* (a defect) from *the spec went stale* (correct code, outdated doc); audit AC **traceability + coverage** (per `_common/TRACEABILITY.md` IDs), contract **completeness / clarity / testability**, and flag **undocumented load-bearing behavior** (behavior with no spec at all). Where a scope genuinely has no spec artifacts, this lens degrades to the undocumented-behavior flag rather than dropping out]
- +`Gateway`?[API design weaknesses — versioning, breaking-change surface, REST/GraphQL consistency] when an API surface exists
- +`Schema`?[data-model design — normalization, index/relation design, migration debt] when a DB surface exists
- +`Sentinel`?[security-relevant design weaknesses] — surfaces design-level concerns but **defers confirmed vulnerabilities to the `security` recipe**, not brushed up here
- **Output: a Design-Issue Ledger** — each issue carries `id / dimension / location (file:line) / severity / one-line description / evidence`. **Every issue is evidence-tied** (no hunches) — this is the entry condition for PRIORITIZE, mirroring `trim`'s evidence gate.
- **False-positive filter (anti-bikeshed):** an "issue" enters the ledger only if it carries a concrete cost — correctness risk, change-amplification, comprehension tax, or a cited standards violation. Pure taste / cosmetic-only items are demoted and noted, not slated. For contested issues, run a light skeptic pass per `_common/ADVERSARIAL_REFUTATION.md` ("is this a real design defect, or a preference?") so a preference cannot consume a brush-up cycle.

### Phase 3 — PRIORITIZE (rank + scope the brush-up slate)
Bound the work — *boil-the-ocean* is the second failure mode. `Ripple`[blast-radius / risk per issue — fixing a design issue can ripple widely] + `Rank`[value × risk × effort, e.g. WSJF / ICE / Cost-of-Delay] + `Magi`[arbitrate the **brush-up slate**: which issues this run, which to defer]. The slate is the top-N by value × risk; the deferred long-tail is recorded in the Ledger, never silently dropped.
- **Behavior-change flag:** any slated issue whose fix would change externally-observable behavior is marked `behavior-changing` and split out — it does **not** ride the behavior-preserving brush-up; it routes to `feature`/`bug`/`migrate` or is confirmed explicitly (Ask First).
- **Slate gate (contract-level under AUTORUN):** confirm the slate before BRUSH-UP when it touches **10+ files**, crosses structural module boundaries, or any target's blast radius is `PUBLIC_API` / `DATA` (Ask First). A small, internal-only slate proceeds.
- **Checkpoint-resume:** see § Resume below.

### Phase 4 — BRUSH-UP (execute the fixes — bounded loop, behavior-preserving)
The actual brush-up. **Safety-net first** (refactor discipline): `Radar`[claude-gated] establishes a **green baseline before any code is touched** — green-before is the entry condition (`refactor` SAFETY-NET). Then fix per issue class, engine-routed:
| Issue class | Plan (Claude) | Apply (Codex) |
|-------------|---------------|---------------|
| architecture / boundary | `Atlas` (+ ADR for the decision) | `Builder` |
| code design smell | `Zen` | `Zen` |
| over-engineering / dead | `Void` | `Sweep` / `Zen` |
| API design | `Gateway` | `Builder` |
| data-model design | `Schema` | `Builder` (+ migration) |
| specification / spec-drift | `Attest`/`PDM` (locate) → `Scribe[unified]`/`Scribe` (spec) | `Radar` (lock contract with a characterization test) |

Independent issues run in parallel with **file-ownership isolation** (`_common/PARALLEL.md`); dependent ones serialize. Fixes are **behavior-preserving** — same external contract, better internal design. The spec axis stays behavior-preserving by construction: brush up a *stale spec to match correct code*, add a *missing AC*, or *lock undocumented behavior with a characterization test + a minimal spec*. The other direction — *code that drifted from its intended spec* and needs a code change to conform — is a behavior change, so it is flagged `behavior-changing` at PRIORITIZE and routed to `bug`/`feature`, never silently "fixed" under the design-clean-up banner.
- **Loop:** `loop ≤ 3 cycles (default 3)` (per recipe-contract §2) against the design-quality bar. Each cycle brushes up a slice of the slate, then **re-critiques the touched area** (did the fix introduce a new smell?). The loop machinery — Generator-Evaluator separation, single termination oracle, flatten rule — lives in `reference/evaluator-loop-protocol.md`; this recipe references it rather than re-specifying it. MAP/CRITIQUE/PRIORITIZE/VERIFY/SHIP are single-pass — only this phase iterates.
- **Exit reasons** (recipe-contract §2): `ACCEPT` / `target-met` (slate cleared / design-quality bar reached, no regression) · `diminishing-returns (Δ < ε)` (a cycle yields little measurable design improvement) · `cap-reached` (`loop ≤ 3 cycles`) · `BLOCK` (a fix needs a decision/escalation). On any non-`ACCEPT` exit, `Void` confirms the stop and the recipe **reports best-so-far brushed-up + the residual slate** — never silently stops, never burns cycles past marginal value.

### Phase 5 — VERIFY (the dual gate — no-regression + design-improvement proof)
Two distinct gates; a brush-up must pass **both**:
- **Behavior preservation (the hard gate):** `Radar`[claude regression — same suite, same result]. This is `anneal`'s refactor-grade discipline: a "design improvement" that changes behavior fails the gate (unless it was an explicitly-flagged, confirmed `behavior-changing` item).
- **Design-improvement proof:** `Atlas`/`Canon` **re-measure** the CRITIQUE design metrics (coupling, cyclomatic complexity, dependency-cycle count, standards-violation count) → **Before/After** per dimension; `Attest` re-measures the **spec axis** (spec↔code drift count, AC traceability / coverage). The brush-up must show a *measured* design-metric improvement, not "looks cleaner".
- **Cross-axis guard** (kaizen-style): confirm the brush-up did not trade one design smell for another, or regress a non-worked axis (de-coupling that exploded surface area; a refactor that dropped coverage or hurt perf). If it did, the cycle fails the gate and loops back.
- `Judge`[multi-engine review of the brush-up diff] — design changes are high-stakes; ship only findings worth fixing.

### Phase 6 — SHIP
`Guardian`[PR with the **Design Ledger** report]. **Phased, small-scope commits** — one issue-class per commit/PR where reversibility matters; never a big-bang multi-issue design rewrite in one commit (void's ≈60% fewer-regression-bugs rule). ADRs accompany structural decisions.

---

## Confirm / safety gate

- **Default Mode `AUTORUN`** with the **Phase 3 slate gate** (each brush-up is scope-bounded + behavior-preserving + reversible). Escalate to `GUIDED` when the slate touches 10+ files or structural boundaries.
- **Confirm-before-launch** when `anneal` runs with no target (whole-codebase sweep).
- **Ask First** on `PUBLIC_API` / `DATA` blast radius, 10+ files, or any issue whose fix is `behavior-changing` (intentional — `anneal` is behavior-preserving by default, so a behavior-changing fix is the deliberate exception that must be confirmed, never folded silently into a clean-up).

## Resume

**Checkpoint-resume** (recipe-contract §4): `anneal` has ≥ 4 phases, so it persists phase outputs at each boundary (MAP → design map; CRITIQUE → Design-Issue Ledger; PRIORITIZE → slate + deferred long-tail; BRUSH-UP → per-cycle progress + which slate items are done; VERIFY → Before/After). An interrupted run resumes from the last checkpoint. `anneal resume` reads the checkpoint, summarizes progress-so-far in 3-5 lines, and continues from the last successful boundary — never silently restarts from MAP. The Design Ledger (brushed slate + remaining slate) is the durable state.

## Output — Design Ledger

`NEXUS_COMPLETE` with the base `## Nexus Execution Report` plus the named **Design Ledger**:
- **Design map** — as-is architecture + responsibilities + hotspots (MAP).
- **Issues found** — the full Design-Issue Ledger, by dimension and severity, each evidence-tied (CRITIQUE).
- **Brush-up slate** — issues fixed this run, with the fix per item (PRIORITIZE + BRUSH-UP).
- **Before/After design metrics** — per dimension (coupling, complexity, cycle count, standards violations, spec↔code drift count, AC traceability/coverage) (VERIFY).
- **Behavior-preservation attestation** — regression gate result + cross-axis-guard result.
- **Deferred + residual** — the long-tail not slated this run, plus any `BLOCK`ed items, with why (recorded, never dropped).
- **ADRs** — structural decisions made during the brush-up.
- **Loop trajectory** — cycles run + exit reason.
- **Follow-ups** — recommended next recipe per deferred cluster (`refactor` for a known single restructure, `optimize` for a perf-tagged item, `kaizen` for a feature-vs-target, `trim` for dead-weight features, `security` for a Sentinel-flagged vuln).

## Failure Modes Prevented

| Failure | Mitigation |
|---------|------------|
| **Auditing a strawman** (critiquing an imagined architecture) | MAP grounds in Lens + Atlas before any critique |
| **Boil-the-ocean** (trying to fix every design issue at once) | PRIORITIZE bounds the slate to top-N by value × risk; long-tail deferred + recorded |
| **Bikeshedding / cosmetic-only churn** (re-arranging to taste) | CRITIQUE false-positive filter: an issue needs a concrete cost; contested ones get a skeptic pass |
| **Silent behavior change under a "design improvement" banner** — including "fixing" drifted code to match its spec | VERIFY behavior-preservation hard gate (Radar same-suite-same-result) + the `behavior-changing` flag at PRIORITIZE, which routes those out to `bug`/`feature` rather than folding them into a clean-up. The CRITIQUE spec axis (Attest/PDM conformance + drift) is what surfaces the divergence; only the behavior-preserving direction — brushing up a *stale spec* to match correct code — stays in scope |
| **Trading one smell for another** (de-couple → surface-area explosion) | VERIFY cross-axis guard |
| **Over-engineering as "improvement"** (only ever adding structure) | Void owns the YAGNI/over-engineering dimension in CRITIQUE; Sweep/Void in BRUSH-UP can *remove* |
| **Unmeasured improvement** ("looks cleaner", no proof) | VERIFY re-measures the CRITIQUE metrics → Before/After is mandatory |
| **Undocumented load-bearing behavior** (behavior with no spec, lost on the next change) | spec axis flags it; brush-up locks it with a characterization test + a minimal spec |
| **Big-bang design rewrite** (one giant risky commit) | SHIP phased small-scope commits, one issue-class at a time |
| **Reinventing refactor/kaizen** (doing their job under a new banner) | boundaries below; a known single restructure → `refactor`, a feature-vs-target → `kaizen` |
| **Work lost on interruption** | checkpoint-resume + `anneal resume` from the last boundary |

## Boundaries / vs neighbors

`anneal` always holds the same side: **discover undiagnosed design weaknesses across a scope, then fix the prioritized slate behavior-preservingly**. Each row names the axis and the route out.

| vs neighbor | Axis (neighbor ↔ `anneal`) | Route |
|---|---|---|
| `refactor` | known restructure on a known target ↔ discovery-first enumeration across a scope | a single known restructure → `refactor` direct (minimum viable chain); `anneal`'s per-issue fix often *is* a refactor |
| `optimize` | a perf number ↔ design quality (coupling/cohesion/maintainability/robustness) | perf-tagged issue surfaced by CRITIQUE → `optimize` |
| `kaizen` | known quantified target for **one feature** ↔ undiagnosed weaknesses **across a scope** | design-quality axis on one feature → `kaizen`; broad sweep → `anneal` |
| `converge` | execution-control wrapper ↔ task shape (audit→fix design) | `converge anneal` is valid — it wraps the Phase 4 brush-up generators under one termination oracle |
| `delve` | forward-looking evolution directions for one shipped feature, no code ↔ backward-looking hardening that ships code | expansion → `delve`; hardening → `anneal` |
| `trim` | removes dead-weight features ↔ strengthens the design of features that stay | dead-weight feature noticed here → `trim`; its `SIMPLIFY` (overbuilt-but-necessary) outcome → brushed up here |
| `summit` / `acceptance` | PR/change-gated quality maximization (28-119 agents / proof-carrying merge) ↔ standing-codebase sweep untied to a PR (6-16 agents) | release-critical specific change → `summit`/`acceptance` |
| `atlas` (agent) | single-agent, proposal-only architecture analysis ↔ orchestration adding the prioritize → fix → verify machinery | `atlas` is one CRITIQUE lens *inside* `anneal` |
| `spec` / `attest` / `pdm` (spec-axis neighbors) | author a new spec via dialogue (`spec`) or report conformance/drift without fixing (`attest`/`pdm`) ↔ audit **and brush up** the spec↔code health of existing code | new spec → `spec`; report only → `attest`/`pdm`; gate one PR → `acceptance`; genuine code-conformance defects route out to `bug`/`feature` |

## Scale

6-16 agents × ≤ 3 cycles; medium-to-high cost. A scoped `anneal <target>` with a small slate is the low end (MAP→one or two CRITIQUE lenses→PRIORITIZE→a few brush-ups→VERIFY ≈ 6-8 agents). A whole-codebase no-target sweep fanning every CRITIQUE dimension (the six core lenses + conditional Gateway/Schema/Sentinel) across the repo with a full brush-up loop is the high end. Lighter than `summit` (28-119); heavier than `refactor`. Cost scales with the slate size, not the codebase size — PRIORITIZE is the cost governor.

## Shared protocols & Add-ons

- **Shared:** Phase 4 loop → `reference/evaluator-loop-protocol.md` (Generator-Evaluator separation, single termination oracle, flatten rule). Phase 4 parallel fixes → `_common/PARALLEL.md` (file-ownership isolation, merge, rollback). Engine routing → summit principles (Codex code-gen / Claude judgment, `reference/summit-recipe.md`). CRITIQUE false-positive refutation → `_common/ADVERSARIAL_REFUTATION.md` (skeptic pass on contested issues). Behavior-preservation discipline → the `refactor` recipe (safety-net + same-suite-same-result). Spec-axis AC/REQ traceability → `_common/TRACEABILITY.md` (canonical AC/REQ IDs the `Attest` lens and `Scribe[unified]` brush-up reuse).
- **Add-ons:** +`Scout` for deeper root-cause when an issue's origin is unclear, +`Schema`/`Gateway` when DB/API surfaces are in scope (also listed as conditional CRITIQUE lenses), +`Sentinel` to flag (not fix) security-relevant design weaknesses, +`Trail` to locate design-stress hotspots from churn in MAP, +`Scribe` to author the ADRs / Design Ledger, +`Sherpa` to decompose a large slate into atomic brush-up steps.

## Chain template

`MAP (Lens[design map] + Atlas[deps/layering/boundaries] +Grove? +Trail?) → ✓scope-gate → CRITIQUE (Atlas[architecture] ‖ Zen[code smells] ‖ Canon[standards] ‖ Void[over-engineering] ‖ Omen[under-specified] ‖ Attest/PDM[spec drift] +Gateway?/Schema?/Sentinel? → Design-Issue Ledger) → PRIORITIZE (Ripple[blast-radius] + Rank[value×risk×effort] + Magi[slate]) → ✓slate-gate → BRUSH-UP [Radar safety-net green-before → ⟲{ Atlas+Builder[arch] ‖ Zen[smell] ‖ Void+Sweep[dead/over-built] ‖ Gateway+Builder[API] ‖ Schema+Builder[data] ‖ Scribe[unified]/Scribe+Radar[spec] → re-critique touched area }⟲] → VERIFY (Radar[regression] + Atlas/Canon/Attest[Before/After] + cross-axis guard + Judge[diff review]) → SHIP (Guardian[phased commits + Design Ledger + ADRs])`

Gate content, loop bound, and exit vocabulary are not restated here — see each Phase contract above and § Confirm / safety gate. Resumable via `anneal resume`; optional `converge anneal` wraps the brush-up loop under a single rubric oracle; deferred clusters hand off to `refactor` / `optimize` / `kaizen` / `trim` / `security`.
