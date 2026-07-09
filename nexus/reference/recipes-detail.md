# Recipes — Detail

Extended descriptions for verbose Recipe rows. The Recipes table in `SKILL.md` carries the canonical name / subcommand / chain template / Read pointer; this file expands the "When to Use" prose that does not fit on one row.

---

## Recipe Families (mental model + within-family disambiguation)

Canonical home for the full family taxonomy + within-family axes. SKILL.md `### Recipe Families` keeps a compact grouping + one-line axis; this table carries the full axis prose and the overloaded-anchor REDIRECT escalations. The Recipes table below (and in SKILL.md) is flat; these families group it and name the axis that separates confusable siblings. **When an input fits a family but not a specific recipe, use the axis to pick — or, for an overloaded anchor, run the one-question REDIRECT (`reference/intent-clarification.md`).**

| Family | Recipes | Distinguishing axis within the family |
|--------|---------|----------------------------------------|
| **Fix** | `bug` · `security` | fault class: defect vs vulnerability |
| **Improve** (existing code) | `refactor` · `optimize` · `kaizen` · `anneal` | refactor = apply a *known* internal restructure (known scope) · optimize = perf-only (a number) · kaizen = multi-axis polish of *one feature* vs a known target · **anneal = *discover* undiagnosed design weaknesses across a scope → brush up the prioritized slate, behavior-preserving**. **`improve`/`polish`/`enhance` is overloaded across all four → REDIRECT** (`audit the design` / `brush up the codebase` / `harden the architecture` → `anneal`; `improve a feature vs a target` → `kaizen`; `known single restructure` → `refactor`; `iterate to a quality bar` → `converge` in the **Loop** family). |
| **Loop** (autonomous / iterative execution) | `loop` · `goal` · `converge` | **loop = dispatcher / front-door**: classify the loop's shape + gate on loop-engineering preconditions (verifiable oracle · external hard-stop · maker≠checker · persistent memory · drift-aware) + route · goal = native `/goal` *setup only* (no run) · converge = in-session rubric Generator-Evaluator quality loop. **The runner itself is the `orbit` skill** — `loop` delegates unattended runs to it, never re-implements it. Underspecified `make a loop`/`automate with a loop`/`run until done` → `loop`; an explicit shape → the sibling direct. |
| **Build** (new) | `feature` · `apex` · `playable` | feature = single guided build · apex = general discovery→ship one-shot (8-25 agents) · **playable = game-specialized all-in-one (Quest design→Glance UI/UX→Tick impl→Dot assets) with a vertical-slice-first gate** |
| **Discover → build pairs** | `spec`→`feature`/`apex` · `charter`→`enact` · `layer`→`sigil`-authoring | spec = one feature *spec* (dialogue) · charter = whole-repo *team + work plan* · layer = whole-repo *reusable operating layer* (project skills + recipes + workflows + routing map). All stop at a design; the pair runs it. **`layer` vs `charter`**: charter plans *what work to do + who does it* (one delivery); layer designs *what reusable tooling the repo should have* (persists). **`layer` vs `sigil`**: layer designs the coordinated *set* (Loom), sigil authors *one* skill body. |
| **Reason** (no code) | `gedanken` · `delve` | output = insight, not a build. **gedanken** = abstract thought-experiment about a claim/hypothesis (construct→reason→perturb→refute→conclude); **delve** = grounded deep-dive into a *shipped* feature → evolution directions (deepen/broaden/reframe). Axis: abstract-hypothetical vs grounded-existing-feature. Both orchestrate `magi`/`flux`; trivial "what if" → `flux`/`magi`, trivial "what could we do with X" → `riff`/`spark` direct. **`delve` vs `kaizen`** (discover directions vs execute vs a target): `evolve`/`improve a feature` is overloaded → REDIRECT. |
| **Comprehend** (reverse-engineer existing code → understanding artifact, no code) | `cartograph` · `chronicle` | output = a grounded documentation artifact of *what exists*, not insight/evolution and not a build. **Within-family axis: space vs time.** **cartograph** = reverse-engineer a feature/system **across multiple repos** from the code → **bird's-eye architecture diagrams + design document** (scope→map-per-repo→correlate-seams→synthesize→diagram→document→ground-verify); a **spatial-structure snapshot** of how it works *today*, grounded in **code citations**. **chronicle** = reverse-engineer a repo's **commit history** → **era timeline + narrative storylines + inferred ethos + history document** along **two axes** — time (**eras**) × theme (**storylines**: feature-lineage · defect-&-resilience · improvement · **decisions** → reconstructed ADR-style decision log) — then **DISTILL** infers the project's **ethos/worldview** (design philosophy · value hierarchy · conventions · product thesis) from the *patterns* (scope→survey→segment-2-axis→excavate-turning-points+thread-beats→synthesize-weave→distill-ethos→diagram→document→ground-verify); a **temporal-evolution arc** of how it *got here* **& what it believes**, grounded in **commit SHAs** (ethos tenets pattern-grounded + refutation-gated, labeled inferred), people-neutral (no rankings). Axis vs the Reason family: **document-what-exists/how-it-evolved** (backward, comprehension) vs **reason/evolve** (forward). vs `delve` (one shipped feature, dialogue, evolution directions) · `charter` (one repo → team+work plan) · `pdm` (plan-vs-code status) · `clone` (black-box external → *rebuild*). Single repo / one diagram → `lens`/`atlas`/`canvas` direct; one period's PR report → `harvest` direct; one diff to teach → `tome` direct; one archaeology question → `trail` direct (minimum viable chain). |
| **Verdict** (which feature) | `essential` · `killer` · `trim` | essential = THE must-have · killer = THE differentiator · trim = remove dead-weight (inverse). Shared gate: `reference/verdict-gate.md`. |
| **Reproduce & Synthesize** | `clone` · `fuse` · `graft` · `transmute` · `migrate` | source count/fidelity: clone = 1 source faithful · fuse = ≥2 sources synthesized · graft = host+donor *concept* (rejects surface copy) · transmute = own-source cross-language · migrate = own-system change-completeness. Shared discipline: `_common/DIFFERENTIAL_PARITY.md`. **`differential parity` alone is ambiguous → REDIRECT.** |
| **Quality-Max** (expensive, confirm) | `acceptance` · `growth-acceptance` · `summit` · `podium` | acceptance = proof-carrying merge (G1-10) · growth-acceptance = post-launch lifecycle (G11-15) · summit = pre-merge quality tournament · podium = content/slide quality |
| **Document package** | `package` (incl. `venture`) | 12-domain preset registry |
| **Meta / control** | `classify` · `proactive` · `pack` | routing · project scan · skill-profile |

---

## kaizen

Existing-feature continuous improvement covering perf / UX / code-quality / feature-extension. **PDCA loop, not single-pass**: improves against a quantified target and stops on target-met or diminishing-returns. Differs from `refactor` (internal-only), `optimize` (perf-only), and `feature` (new addition). Scale: 4-8 agents (× ≤3 cycles).

**Chain template:**
`(Lens + Pulse?/Echo?/Voice?/Trace?)[baseline] → Spark → Magi[axes + target + stop] → ⟲{ (Bolt/Tuner ‖ Palette/Prose/Flow ‖ Zen/Sweep ‖ Artisan/Builder)[axis] → Radar[+cross-axis guard] → Pulse?/Echo?[re-measure vs target] }⟲ → Void[stop-confirm] → Guardian`

The `⟲{…}⟲` block loops until target-met OR diminishing-returns OR iteration cap. Full phase contract (DIAGNOSE+BASELINE / PROPOSE+TARGET / IMPROVE / VERIFY+LOOP / SHIP) → `reference/inline-recipes.md`.

---

## anneal

**Codebase design audit → prioritized behavior-preserving brush-up.** The corrective, execution-bearing member of the Improve family: where `kaizen` improves *one feature against a target you already chose*, `anneal` **discovers undiagnosed design weaknesses across a scope you have not pre-diagnosed, then brushes up the prioritized slate**. Surface design issues from six independent dimensions (architecture / code-smell / standards / over-engineering / under-specified design = edge cases & invariants / **specification = spec↔code conformance & drift, AC traceability, undocumented behavior**), prioritize by value × risk, and fix the slate with real code that **preserves behavior** (refactor-grade discipline) — gated by a dual VERIFY (no-regression + Before/After design-metric proof). The metallurgical metaphor: relieve accumulated internal *design stress* and leave the structure tougher, not cosmetic polish. `<target>` scopes the audit; **no target → whole-codebase sweep** (confirm-before-launch, slate capped to top-N by value × risk, long-tail recorded). Default Mode `AUTORUN` with the Phase 3 slate gate (Ask First on 10+ files / `PUBLIC_API` / `DATA` / any `behavior-changing` fix). Named **Design Ledger**; checkpoint-resume (`anneal resume`). Engine routing follows summit principles (Codex code-gen / Claude judgment). Distinct from `refactor` (known restructure, known scope), `optimize` (perf number), `kaizen` (one feature vs known target), `delve` (no code — evolution directions), `trim` (remove features), `summit`/`acceptance` (PR-gated), and the spec-axis neighbors `spec` (author a *new* spec) / `attest`·`pdm` (report-only conformance) / `acceptance` (PR gate). 6-16 agents × ≤3 cycles, medium-to-high cost (cost scales with slate size, not codebase size — PRIORITIZE is the governor).

**Chain template:**
`MAP (Lens[map design] + Atlas[deps/layering/God-class/boundaries] +Grove?/Trail?) → ✓scope-gate (confirm-before-launch when no-target/structural) → CRITIQUE (Atlas[architecture] ‖ Zen[code smells] ‖ Canon[standards/ISO-25010] ‖ Void[over-engineering/YAGNI] ‖ Omen[under-specified/edge-cases/invariants] ‖ Attest/PDM[spec: spec↔code drift/AC traceability/undocumented behavior] +Gateway?/Schema?/Sentinel?; → evidence-tied Design-Issue Ledger; false-positive filter + skeptic pass per _common/ADVERSARIAL_REFUTATION.md) → PRIORITIZE (Ripple[blast-radius] + Rank[value×risk×effort] + Magi[slate; defer long-tail; flag behavior-changing]) → ✓slate-gate → BRUSH-UP [Radar safety-net green-before → ⟲{ (Atlas+Builder ‖ Zen ‖ Void+Sweep ‖ Gateway+Builder ‖ Schema+Builder ‖ Accord/Scribe+Radar[spec: update stale spec / lock undocumented behavior; code-conformance → flag behavior-changing]) per _common/PARALLEL.md → re-critique touched area }⟲ loop ≤3 cycles (default 3): ACCEPT | diminishing-returns (Δ<ε) | cap-reached | BLOCK ] → VERIFY (Radar[regression same-suite-same-result] + Atlas/Canon/Attest[Before/After design + spec-drift metrics] + cross-axis guard + Judge[multi-engine diff review]) → SHIP (Guardian[phased small-scope commits + Design Ledger + ADRs])`

Full phase contract (MAP / CRITIQUE / PRIORITIZE / BRUSH-UP / VERIFY / SHIP), Failure Modes Prevented, and boundaries → `reference/anneal-recipe.md`. Wrap in a rubric-graded loop via `converge anneal`.

---

## apex

Full-cycle auto-implementation: discovery → spec → parallel design → risk gate → loop → ship. With no-args, Phase 0 autonomously discovers the goal. 8-25 agents, high-cost. **Confirm before launch.**

**Chain template:**
`(Phase 0 if no goal) → Discovery (plea+field+echo?) → Ideate (riff) → Verdict (magi) → Spec (accord+void?+scribe?) → Design [Tech (atlas+gateway?+schema?) ‖ UX (Vision sub-orchestrates muse+palette+prose+flow?+frame?+forge+echo)] → Risk Gate (omen+ripple+echo) → Loop (Orbit on Codex CLI drives builder+artisan?+vitrine?+judge+radar+voyager?) → Acceptance Verification (attest: AC-conformance gate) → Ship (guardian+launch)`

Guarded by a run-level budget envelope (hard-abort at ceiling) + cross-phase checkpoint-resume. `attest` gates Ship on accord's L3 ACs (convergence ≠ correctness).

Read: `reference/apex-recipe.md`, `reference/apex-walkthrough.md`.

---

## playable

**All-in-one game production** — concept → playable, shippable game via the game cluster, under a vertical-slice-first gate. The game-domain specialization of `apex`: routes design to Quest, UI/UX to Glance, implementation to Tick, assets to Dot (never generic Builder for game systems). 8-22 agents, high-cost. **Confirm before launch.**

**Chain template:**
`CONCEPT (quest[frame] +flux?/magi?) → DESIGN (quest[gdd/balance/economy] → glance[hud/menu/nav/a11y] ‖ weave?[FSM]) → SLICE (forge[vertical slice] → echo[playtest] → vertical-slice gate) → PRODUCE [tick[loop/ecs/state/physics/netcode/save] ‖ dot[assets]] → INTEGRATE (tick wires glance UI + dot assets; +builder? non-game backend; +flow? UI motion) → VERIFY (radar[sim/determinism] + echo[UX] + glance[a11y/glanceability] + bolt?[frame budget]) → SHIP (guardian +launch?)`

Signature discipline: **prove the core loop is fun in a vertical slice before producing breadth** (SLICE gate). Game acceptance = core-loop fun (playtest) · determinism (if required) · a11y baseline · frame budget — not just "tests pass". Loop ≤ 3 cycles at SLICE (fun-loop) and VERIFY (fix-loop). Emits a named **Playable Report**. Residual gaps (e.g. audio — no audio specialist in the current roster) are surfaced, not hidden. vs `apex` (general) / `clone` (reproduce existing game) / GAME sub-chains in `agent-chains.md` (components).

Read: `reference/playable-recipe.md`.

---

## charter

**Repo-wide analysis → self-driving Charter, team design included — stops at the document.** Document-first planning recipe; the execution half is `enact`. Where `apex` discovers a *feature* and ships it in one shot, `charter` reads the *whole repository*, distills a durable Charter artifact (`docs/CHARTER.md` + `CHARTER.roster.yaml`) that designs the team (§5 roster + §6 orchestration plan) and §10 checklists (pre-flight / per-package Definition-of-Done / progress tracker / final delivery) without building or running it. The team becomes a pure function of the document, so `enact` (or a future session) reconstructs the identical team and gates each boundary on the checklists. Distinct from `apex` (feature-centric, one-shot), `goal` (loop config only), `package` (docs only). The §5/§6 design is **multi-engine by default** (`engines=claude+codex`): Claude Code for plan/design/review, Codex CLI (model `gpt-5.6-terra`, C3.0 variant tiering) for build loops + high-volume parallel coding (Orbit sub-hub pinned to Codex, per-engine prereqs + `fallback_engine` recorded for `enact`). Modes: autonomous (no-args) / objective-supplied / `scope=` / `out=` / `engines=`. 5-15 agents (analysis + authoring only). No execution → no Confirm Gate.

**Chain template:**
`Phase 0 Framing → 1 Comprehensive Analysis (lens ‖ atlas ‖ grove? ‖ trail? ‖ sentinel?/canon?/sweep?/pulse?) → 2 Objective+WBS (spark+rank? → sherpa → accord + magi?/omen?/ripple?) → 3 Charter Authoring incl. team design (scribe +accord trace, void? → finalize §5 roster + §6 plan → write docs/CHARTER.md + roster.yaml) → DELIVER (recommend /nexus enact)`

Read: `reference/charter-recipe.md`.

---

## enact

**Execute a Charter end-to-end.** The execution half of the `charter → enact` pair: reads an existing Charter, **constructs the team from §5 roster** (bind role→skill→spawn + verify prereqs), **orchestrates §4 work breakdown** via the §6 plan (spawn per package; Orbit sub-loop for build iterations; checkpoints + guardrails; hub-spoke aggregate), then verifies §7 and ships. Updates §9 Execution Log so the Charter stays the living source of truth; `resume` restarts from the last checkpoint. No analysis/planning — the Charter is the complete contract; a missing/invalid section stops at Phase 1 rather than improvising. **Runs to completion (enforced under AUTORUN_FULL):** no mid-run stops for progress, recoverable failures (retry→fallback_engine→Scout+Builder→alt owner→`SKIPPED(blocked)`+continue), or cost; loops until every §4 package is terminal (SUCCESS/PARTIAL/SKIPPED). Only intentional stops = §8 safety red lines (L4/destructive/out-of-scope) + no-valid-Charter precondition. Honesty preserved: §7 failures delivered truthfully, not masked. **The orchestrator streams every progress event to an append-only run-log file** (`docs/CHARTER.run.log.md`, override `log=`); Charter §9 holds only a pointer + summary, and `resume` restarts from the run-log tail. ★ Gate is announce-and-proceed (no objection window); GUIDED/INTERACTIVE re-introduce stops. Modes: `enact <path>` (default `docs/CHARTER.md`) / `dry-run` (construct + verify only) / `resume`. 6-30+ agents.

**Chain template:**
`read Charter (validate §3-§8) → Phase 1 Team Construction (bind role→skill→spawn, verify prereqs, sub-orch setup, dry-run check) → ★ Confirm → Phase 2 End-to-End Orchestration (spawn per §4 package in §6 order; orbit sub-loop; parallel + file ownership; append §9) → Phase 3 Verify+Deliver (radar?/judge? → §7 gates → guardian?/launch? → update Charter §9)`

Read: `reference/enact-recipe.md`.

---

## layer

**Design + stand up a repo's operating layer — Loom designs, Sigil authors, Nexus registers.** The Nexus surface over the **Loom** agent (project-scoped analogue of Architect). Where `charter` designs a *team + work plan* to deliver a body of work, `layer` designs the *reusable operating layer* a repository should carry: which project-local skills encode its conventions, which repo-tailored recipes chain them, which skill-and-agent workflows coordinate project outcomes, and a routing map (single-owner per task domain; ecosystem-owned tasks deferred, never duplicated). Loom **designs the system and delegates the threads** — it never writes a skill body, runs a chain, or authors a hook: Loom blueprints, Sigil authors each body (9+/12), Nexus registers recipes/workflows/routing map, Latch/Orbit take hooks/loops. Mechanism choice per task uses `_common/MECHANISM_SELECTION.md` for hook/rule/subagent/skill; `recipe`/`workflow` are Loom-local. Each designed workflow carries a formal topology + `≤ 5` phases (no Bag-of-Agents). Distinct from `charter` (team+work plan, one delivery), `sigil`/SKILL_GEN (one skill body), `spec` (one feature spec). Modes: whole-repo (no-args) / `<scope>` / `design-only` (stop at the blueprint, charter-style) / `resume` / `engines=`. **Confirm-before-launch** (DELEGATE writes files + changes routing); `≥10` skills or established-routing changes → Ask First. Named report: **Operating-Layer Blueprint** (+ Layer Report tail in full mode). Checkpoint-resume (`layer resume`). 5-15 agents (design-only 3-6); Low-Medium cost.

**Chain template:**
`Phase 0 Frame (detect repo/stack/scope/existing-layer/mode) → 1 Survey (loom drives ‖ lens(structure) ‖ atlas?(arch→topology) + read .claude/ layer + sigil inventory?; greenfield→infer from manifests/CI/history) → 2 Design (loom: coverage matrix + suite plan + recipes + workflows[topology,≤5] + routing map) → 3 ★Confirm blueprint (design-only stops here) → 4 Delegate (parallel: sigil×N author bodies 9+/12 ‖ latch hooks ‖ orbit loop specs → nexus registers recipes/workflows/routing map ‖ grove docs placement) → 5 Verify (loom 14-item + sigil 9+/12 + routing single-owner + workflow topology/≤5) → DELIVER Layer Report`

Read: `reference/layer-recipe.md`.

---

## spec

**Interactive feature-proposal → locked specification through deep human-in-the-loop dialogue.** Takes a rough idea and refines it conversationally into a sign-off-ready spec carrying **mandatory testable, traceable acceptance criteria**, then **stops at the spec — writes no code**. The discovery half of `spec → feature`/`apex`, mirroring `charter → enact`. **Defaults to `INTERACTIVE`** (with `delve`; the dialogue is the deliverable); its phase-boundary checkpoints are contract-level, so even AUTORUN cannot skip them. **+Lens reuse-scan grounds it in the existing codebase; draft-persisted & resumable** (`spec resume [<slug>]`); locks only when **both lock preconditions pass — testable L3 ACs + the Spec Quality Gate** (ambiguity/completeness/consistency/testability/scope/provenance) — and writes `docs/specs/<slug>.md` per a standard template; the dialogue itself is conducted per `reference/dialogue-protocol.md` (question craft, Assumption Ledger, Provenance Gate). Distinct from `essential`/`killer` (which-feature *verdict*, minimal dialogue), `feature`/`apex` (build code), `charter` (whole-repo team design), `converge` (automated grading loop), and `riff` (single-agent brainstorm, no artifact). 3-9 agents × dialogue turns.

**Chain template:**
`FRAME (Plea +Field?/Cast? +Lens?[reuse-scan/constraints]) → ✓confirm-problem + draft-init → EXPAND (Riff ‖ Flux +Compete?) → ✓steer + draft → CHALLENGE (Magi + Void + Ripple +Omen?) → ✓pick + convergence-check + draft → SHAPE (Spark +Rank?) → ✓edit + draft → SPECIFY (Accord +Scribe?/Gateway?/Schema?, L3 ACs+IDs mandatory +Attest?/Echo?) → ✓iterate + draft → LOCK (✓quality-gate: Judge+Attest+Magi? → ✓sign-off → promote draft to docs/specs/<slug>.md per template + Open Questions → ✓build-path: orbit loop (✓engine claude|codex|agy) ‖ apex; fallbacks feature|acceptance|essential|killer)` · resumable via `spec resume [<slug>]`

Full phase contract (FRAME / EXPAND / CHALLENGE / SHAPE / SPECIFY / LOCK), boundaries, and anti-patterns → `reference/spec-recipe.md`.

---

## gedanken

**Structured thought-experiment reasoning** — take a question / hypothesis / premise / design tension and reason about it rigorously **inside a constructed hypothetical, under controlled variation**, to surface hidden assumptions, derive non-obvious implications, and establish what would falsify the conclusion. **Writes no code.** The disciplined analog of a classic *Gedankenexperiment* (Galileo's falling bodies, Einstein's elevator, Rawls' veil of ignorance). The general-purpose **exploratory-reasoning** recipe: distinct from `magi` (which delivers a *decision* — `gedanken` is often its upstream), `riff` (diverges; `gedanken` converges under variation), `omen` (failure-mode-only; a special case `gedanken` uses in PERTURB), `flux` (a single reframing move; `gedanken` orchestrates it into a protocol), `helm` (business-scenario simulation; `gedanken` is domain-agnostic), and `spec`/`charter` (which produce buildable artifacts; `gedanken` produces an insight). Default Mode `AUTORUN_FULL` (`INTERACTIVE` for Socratic dialogue); no confirm gate (no code). 3-9 agents × variation depth. A trivial one-off "what if" routes to `flux`/`magi` direct (minimum viable chain).

**Chain template:**
`FRAME (Magi[frame + stated/implicit assumption ledger] +Flux?[challenge framing] +Lens?/Compete?[ground in real system]) → CONSTRUCT (Flux[build hypothetical + pick archetype: limiting-case|counterfactual|reductio|isolation|analogy|inversion|veil] +Cast?/Matrix?) → REASON ∥ (Magi Logos/Pathos/Sophia ‖ Flux cross-domain ‖ domain-specialist?[Atlas|Helm|Oracle|Ripple]) → PERTURB (Matrix[axis variation] + Flux[limit/invert] +Omen?; variation rounds ≤3 cycles, stop on robustness-established | diminishing-insight | cap-reached → mark robust vs frame-dependent) → REFUTE (refute×2-3 per _common/ADVERSARIAL_REFUTATION.md — smuggled-premise|false-analogy|equivocation|frame-dependence) → CONCLUDE (Magi synthesize: conclusion + confidence + load-bearing assumptions + falsifier + transfer + epistemic status; Scribe?[Gedanken Report])`

The variation bound and the adversarial REFUTE are contract-level; resumable per phase. Optional handoff at CONCLUDE → `magi` (decision) / `spec` (if it resolved *what* to build) / verdict recipes. Full phase contract, archetype menu, Failure Modes Prevented, and boundaries → `reference/gedanken-recipe.md`.

---

## delve

**Existing-feature deep-dive → evolution-direction dialogue** — take an *already-shipped* feature, excavate it through dialogue past *what it does* to *what is really going on*, surface non-obvious **insights**, and chart **evolution directions** (deepen / broaden / reframe). **Writes no code** — stops at a named **Evolution Map** and hands off to `spec`/`kaizen`/`feature`/`apex`. The grounded-existing-feature member of the Reason family (where `gedanken` is the abstract-hypothetical member) and the discovery upstream of `kaizen`. Distinct from `kaizen` (executes improvement against a fixed quantified target — `delve` discovers *what* to improve and is its upstream), `spec` (shapes a *new* idea into a buildable spec — `delve` excavates an *existing* feature), `gedanken` (reasons about an *abstract* hypothetical — `delve` is grounded in real code/usage), and the verdict recipes `essential`/`killer`/`trim` (which-feature verdict — `delve` maps directions for one feature). Default Mode `INTERACTIVE` (with `spec`, the two dialogue recipes); its three dialogue checkpoints (confirm-feature-as-is / validate-insights / pick-direction) are contract-level, so even AUTORUN cannot skip them. No confirm/safety gate (no code). Draft-persisted & resumable (`delve resume [<slug>]`); writes `docs/evolution/<feature-slug>.md`; the dialogue itself is conducted per `reference/dialogue-protocol.md` (question craft, Assumption Ledger, Provenance check at CHART). 3-9 agents × dive depth. A trivial one-off "what could we do with X?" routes to `riff`/`spark` direct (minimum viable chain).

**Chain template:**
`GROUND (Lens[map current impl] +Pulse?/Trace?/Voice?[usage] +Plea?[job-to-be-done lens]; reason-for-existence ← Socratic dialogue + Lens) → ✓confirm-feature-as-is + draft-init → EXCAVATE (Plea[latent needs] ‖ Flux[challenge baked-in assumptions] ‖ Echo[friction/workarounds] +Field?/Compete?/Trace?) → SURFACE (Magi[synthesize insights] +Spark[name vs existing logic]; deepening loop EXCAVATE↔SURFACE ≤3 cycles (default 3), stop on insight-saturation | diminishing-insight (Δ<ε) | cap-reached → report insights + undug seams) → ✓validate-insights + draft → DIVERGE (Riff ‖ Spark[grounded directions] ‖ Flux[reframe]; tag axis deepen/broaden/reframe + insight-link) → REFUTE (insight: refute×2-3 per _common/ADVERSARIAL_REFUTATION.md — confirmation/no-news/false-pattern → confirmed vs hypothesis; direction: Ripple blast-radius + Magi value×feasibility +Omen?) → CHART (Magi/Spark Evolution Map: ranked directions + axis + recommended next-recipe; Scribe?) → ✓pick-direction → recommend handoff (spec | kaizen | feature | apex | killer | essential)` [NO CODE]

The three dialogue checkpoints and the EXCAVATE↔SURFACE deepening bound are contract-level; resumable via `delve resume [<slug>]`. Full phase contract (GROUND / EXCAVATE / SURFACE / DIVERGE / REFUTE / CHART), Failure Modes Prevented, and boundaries → `reference/delve-recipe.md`.

---

## cartograph

**Multi-repo reverse-engineering → bird's-eye diagrams + design document** — take a feature/system that **spans multiple repositories**, reverse-engineer it **from the code** (white-box, own/accessible source — not black-box observation), stitch the per-repo reads into **one cross-repo model**, and produce a **bird's-eye overview** (aggregated architecture diagrams) **+ a design document** explaining how it works. **Writes no product code** — the deliverable is grounded documentation. The comprehension-and-documentation member of the ecosystem: where `delve` excavates *one shipped feature in one codebase* for *evolution directions* through dialogue, `cartograph` **maps how an existing feature/system is architected across many repos and documents it**. **Grounded-by-construction**: every component, edge, and design decision traces to a code citation; inferred *intent* is labeled and separated from observed *structure*; where code doesn't reveal the answer, it writes **UNKNOWN**, never a fabrication (doc-quality W4-W6). Default Mode `AUTORUN` with a contract-level **SCOPE gate** (confirm the repo set + feature boundary + diagram set before the mapping fan-out — a scope/blast-radius gate, not a dialogue). No destructive-action gate (read-only over source, writes only docs under `docs/architecture/`). `cartograph <feature>` (resolve repos from workspace) · `repos=a,b,c` (explicit set) · no-feature → whole-system map (confirm-before-launch, top-N by centrality). Named **Cartography Map**; checkpoint-resume (`cartograph resume`). Claude-owned throughout (no code-gen phase). Distinct from `delve` (one shipped feature, dialogue, evolution — cartograph documents across repos), `charter` (one repo → team+work plan — cartograph is comprehension not delivery planning), `pdm` (plan-vs-code status — cartograph is pure code reverse-engineering), `clone` (black-box external → *rebuild* in code — cartograph is white-box own-source → *document*, no code), `migrate` (changes the system — cartograph only documents), `package` (domain-preset doc generation — cartograph is code-grounded architecture docs), and the `lens`/`atlas`/`canvas` agents (single-agent/single-repo/single-input — cartograph orchestrates them across N repos with correlation + synthesis + grounding). Single-repo overview → `lens`/`atlas`/`canvas` direct. 5-16 agents × ≤3 grounding cycles; read-heavy, write-light; cost scales with repo count, not lines of code (SCOPE is the governor).

**Chain template:**
`SCOPE (Grove?/Lens[detect repos + roles] + Lens[locate feature entry points per repo] → scope sheet) → ✓SCOPE-gate (contract-level; confirm-before-launch when no-feature/≥5 repos) + draft-init → MAP ∥per-repo (Lens[structure + in-repo data flow + exposed interface surface + owned data] +Atlas?/Trail? per _common/PARALLEL.md → repo cards) → CORRELATE (Atlas[cross-repo dep/integration graph] +Gateway?[API-contract seams] +Stream?[event/data flow] +Schema?[shared data model]; match outbound↔inbound, type each seam, record open seams → unified cross-repo model) → SYNTHESIZE (Magi[bird's-eye model + end-to-end path] + Atlas[style + design decisions]; observed vs inferred, UNKNOWN over fabrication) → DIAGRAM (Canvas[system-context/component ‖ sequence(s) ‖ data-flow/ER ‖ cross-repo dependency], every node/edge model-traceable) → DOCUMENT (Scribe[design doc per doc-quality-protocol, diagrams embedded]) → VERIFY (Judge/Attest[grounding: claims/edges → citations, producer≠verifier] + Doc Quality Gate W12 + coverage check; ⟲ loop ≤3 cycles (default 3) → CORRELATE/SYNTHESIZE on ungrounded/missing, exit ACCEPT | diminishing-returns (Δ<ε) | cap-reached | BLOCK → finalize with open seams + residual gap) → promote docs/architecture/<slug>.md` [NO CODE]

The SCOPE gate and the grounding/coverage bound are contract-level; resumable via `cartograph resume`. Full phase contract (SCOPE / MAP / CORRELATE / SYNTHESIZE / DIAGRAM / DOCUMENT / VERIFY), Failure Modes Prevented, and boundaries → `reference/cartograph-recipe.md`.

---

## chronicle

**Commit-history reverse-engineering → era timeline + narrative storylines + inferred ethos + repository history document** — take a repo (or a `<path>`/component within it) and its **commit history**, reverse-engineer **how it evolved over time** from the git record along **two axes**: the **time axis** — cluster into coherent named **eras**; and the **theme axis** — trace the **storylines** that weave through them: **feature-lineage** (how capabilities were added and grew), **defect-&-resilience** (the bugs fought, notable incidents/regressions, how it hardened), **improvement** (refactor/perf trajectory), and **decisions** (direction/architecture/dependency changes → reconstructed into an ADR-style **decision log** of *what · why · why-not-the-alternative*). Excavate the **turning-point commits + thread beats**, synthesize the **overall arc + per-storyline mini-arcs** (first commit → HEAD), and produce a **history document** (`docs/history/<slug>.md`) with an era-timeline, storyline swimlanes/matrix, and the decision log. Then a dedicated **DISTILL** phase infers the project's **ethos / worldview** — its design philosophy, revealed value hierarchy (which good won when two conflicted), operating conventions, and product thesis — read off the *patterns* in the synthesized history; each tenet is **pattern-grounded (≥3 independent cited events) + counter-evidence-swept + confidence-tiered + adversarial-refutation-gated**, always **labeled inferred, never asserted as the project's official stance**, with an optional **stated-vs-revealed** contrast against README/`CLAUDE.md`. **Writes no product code** — the deliverable is grounded documentation. The story is the **weave**: eras are the *acts*, storylines are the *plot lines*, and the ethos is *who the project turned out to be* — not a flat log, not just a phase list. The **temporal** member of the Comprehend family: where `cartograph` maps a system **across space** (a bird's-eye snapshot of how it works *today*), `chronicle` maps a repo **across time** (the arc of how it *got here*). **Grounded-by-construction**: every era boundary, turning point, storyline beat, decision-log entry, and metric traces to a **commit SHA / tag / PR at a pinned HEAD**; what a commit *changed* is observed (cited), *why* is inferred (labeled) unless the message/PR states it, and where the record doesn't reveal it, writes **UNKNOWN** — never a fabrication; an **invented rejected-alternative fails the VERIFY gate** (doc-quality W4-W6). **People-neutral by contract** (from `trail`/`harvest`): narrates *changes and decisions, not individuals* — contributor data appears only as aggregate era context, never a ranking/leaderboard (a hard VERIFY check). Default Mode `AUTORUN` with a contract-level **SCOPE gate** (confirm repo/path + time window + granularity + **storyline set** + audience + artifact set + pinned HEAD before the survey/excavation fan-out — a scope/blast-radius gate, not a dialogue). No destructive-action gate (read-only over git, writes only docs under `docs/history/`). Forms: `chronicle` (full history) · `chronicle since=<tag\|date\|sha>` (bounded window → narrative changelog) · `chronicle <path>` (one component's history) · `chronicle repos=a,b,c` (cross-repo timeline, confirm-before-launch); the audience may prioritize one storyline (e.g. decision-archaeology → decision thread deep). `> 1500 commits` or `repos ≥ 2` → confirm-before-launch. Named **Chronicle**; checkpoint-resume (`chronicle resume`). Claude-owned throughout (no code-gen phase). Orchestrates `harvest`+`trail` (SURVEY the quantitative shape + thread-seeding by conventional-commit type) + `magi` (SEGMENT into 3-7 eras × storylines, SYNTHESIZE the weave, DISTILL the ethos) + `trail`+`tome`+`atlas`? (EXCAVATE only the top-N turning points per era + top-M beats per storyline — the cost governor; Atlas shapes the decision log) + `flux`?+`lens`? (DISTILL: worldview reframe + stated-vs-revealed contrast) + a **refutation panel** (DISTILL: refute each ethos tenet) + `saga`? (narrative shaping for onboarding/retro/changelog audiences) + `canvas` (era timeline ‖ storyline swimlanes/matrix ‖ velocity xychart ‖ milestone gitgraph ‖ ethos-evolution) + `scribe` (the doc) + `judge`/`attest` (grounding). Distinct from `cartograph` (spatial structure snapshot — chronicle is the temporal arc), `harvest` (one *period's* PR report — chronicle reads the *whole* history into eras+storylines+arc and *uses* harvest as its SURVEY engine), `tome` (one *diff* → teaching doc — a turning-point/thread-beat engine inside chronicle), `trail` (one *regression/archaeology question* — whole-history synthesis is chronicle), `atlas` (authors a *forward* ADR for a live decision — chronicle *reconstructs past* decisions from history), `magi` (deliberates a *live decision* — chronicle-DISTILL infers a *descriptive ethos* from history, decides nothing), `delve` (one feature → evolution *dialogue*, no docs), `charter` (repo → team+work plan — chronicle documents the past, not the plan), `pdm` (plan-vs-code present status). One period's report → `harvest` direct; one diff to teach → `tome` direct; which commit broke X → `trail` direct; a new ADR → `atlas` direct; a live judgment call → `magi` direct (minimum viable chain). 4-14 agents × ≤3 grounding cycles; read-heavy, write-light; **cost scales with era count × (turning-points + storylines × beats) per era + the DISTILL tenet×refutation pass (≤5-7 tenets × 2-3 skeptics), not commit count** (SURVEY is cheap aggregation; EXCAVATE is capped top-N per era + top-M per storyline) — SCOPE (window + granularity + storyline set + whether ethos is in scope) and the caps are the governors.

**Chain template:**
`SCOPE (Trail[confirm repo + history depth + workflow shape: squash/rebase/import/shallow] +Lens?[anchor current state] → scope sheet: repo/path + pinned HEAD + window + granularity + storyline set + audience + artifact set + integrity-note) → ✓SCOPE-gate (contract-level; confirm-before-launch when >1500 commits / repos≥2) + draft-init → SURVEY (Harvest[volume/composition/tags/DORA over time] + Trail[churn/hotspot timeline, merge/revert density]; cheap aggregation + thread-seeding by conventional-commit type, substantive-vs-noise split → history shape + candidate era boundaries + candidate thread pools + aggregate contributor trend) → SEGMENT ×2-axis (Magi[time: cluster into 3-7 named eras ‖ theme: define storyline set (feature/defect/improvement/decisions) + shape across eras] + Trail[confirm each era boundary on a real inflection, cited] → era set + storyline set + era×thread weave skeleton) → EXCAVATE ∥per-turning-point ∥per-thread-beat (Trail[archaeology; defect beats → regression/fix lineage] +Tome[intent/decision from message+PR] +Atlas?[decisions → ADR-style: context/decision/alternatives/consequences] per _common/PARALLEL.md; deep-read only top-N turning points per era + top-M beats per storyline per era; observed change vs inferred why (why-not = inferred/UNKNOWN unless stated), UNKNOWN over fabrication; ✓owner-ratification (Mode-conditional GUIDED/INTERACTIVE: inferred/UNKNOWN → confirmed-by-owner) → turning-point ledger + thread-beat ledger + decision log) → SYNTHESIZE (Magi[weave: overall arc × per-storyline mini-arcs × interplay] +Saga?[narrative shaping — lens on evidence, not fiction]; every beat evidence-linked → woven narrative) → DISTILL (Magi[infer ethos: design-philosophy ‖ value-hierarchy ‖ conventions ‖ product-thesis ‖ ethos-evolution] +Flux?[worldview reframe] +Lens?[stated-vs-revealed]; each tenet ≥3-pattern + counter-evidence + confidence tier + refutation panel (load-bearing) + ✓owner-ratification → the Ethos (≤5-7 tenets, labeled inferred, never fact)) → DIAGRAM (Canvas[era timeline (timeline/gantt) ‖ storyline swimlanes / era×thread matrix ‖ velocity/composition (xychart) ‖ milestone (gitgraph) ‖ decision-log table ‖ ethos-evolution matrix], every element model-traceable) → DOCUMENT (Scribe[Chronicle per doc-quality-protocol, pitched to audience, diagrams embedded: overview/arc/eras/storylines/decision-log/philosophy-&-worldview/turning-points/by-the-numbers/gaps/glossary]) → VERIFY (Judge/Attest[grounding: claims/beats/decision-entries/metrics → SHA/tag/PR @pinned-HEAD, producer≠verifier, invented-alternative fails; +cross-engine option] + people-neutrality check + narrative-fidelity check + ethos-grounding check (≥3-pattern + counter-evidence + tier + refutation-survival, no tenet-as-fact) + Doc Quality Gate W12 + coverage check (every era + every storyline present-or-absent + integrity gaps stated); ⟲ loop ≤3 cycles (default 3) → EXCAVATE/SEGMENT/DISTILL on ungrounded/missing/violation/refuted-tenet, exit ACCEPT | diminishing-returns (Δ<ε) | cap-reached | BLOCK → finalize with UNKNOWNs + integrity gaps + speculative/residual tenets + residual gap) → promote docs/history/<slug>.md + pinned-HEAD attestation` [NO CODE]

The SCOPE gate and the grounding/coverage bound are contract-level; resumable via `chronicle resume`. Full phase contract (SCOPE / SURVEY / SEGMENT / EXCAVATE / SYNTHESIZE / DISTILL / DIAGRAM / DOCUMENT / VERIFY), Failure Modes Prevented, and boundaries → `reference/chronicle-recipe.md`.

---

## essential

Must-have feature **verdict + conditional implementation**. Converges on THE ONE feature without which the product cannot exist. Subtraction-oriented (MVP, core feature, scope reduction).

**Chain template:**
`Plea → Spark → Magi → Rank → AskUserQuestion[Y/N/Modify] → if Y: Sherpa → Builder[codex] → Radar[codex] → Guardian`

Full sequential funnel + verdict + conditional implementation → `reference/inline-recipes.md`.

---

## killer

Killer-feature **verdict + conditional implementation with feature flag**. Converges on THE ONE decisive differentiator via cross-engine triangulation, then **gates the verdict on defensibility (moat) + adversarial refutation** before any build. Default baseline: **Claude + Codex (dual-engine)** — perspective diversity via different prompt frames + WebSearch tool usage. agy optional third axis when AVAILABLE. Addition-and-leap-oriented.

**Chain template:**
`(Compete[claude+WebSearch] ‖ Flux[codex reframe] ‖ Plea[claude empathy] [+ Compete-agy / Flux-agy if AVAILABLE]) → Spark[synthesize one] → {Compete[moat/time-to-copy] + refute×2-3[claude‖codex]} → Magi[Go/No-Go] → AskUserQuestion[Y/N/Modify] → if Y: Sherpa → (Forge[codex] if UI) → Artisan/Builder[codex] → Radar[codex] → judge[multi-engine] → Guardian + flag[KPI + ramp + kill]`

Full cross-engine triangulation + moat/refutation gate + verdict + flagged implementation (with differentiation KPI & kill criterion) → `reference/inline-recipes.md`.

---

## trim

Dead-weight feature **removal verdict + conditional excision** — the inverse of `essential`/`killer`. Applies the **essential axis** (must-have for the core job?) and **killer axis** (defensible differentiator?) as a 2×2 filter over the *existing* feature set: a feature survives if essential **OR** killer; only one that is **neither** and carries real cost (CoK ≥ 7) becomes a removal candidate. Core engine is `void` (YAGNI / Feature Sunset / CoK / blast radius); trim adds the dual-axis judgment + multi-agent *execution* void's propose-only recipes lack. Subtraction-and-removal-oriented. **`trim` with no target → whole-project auto-scan** (PDM full inventory + Void carrying-cost rank → top-N-by-CoK slate; defaults to GUIDED). **Confirm before Phase 5 excision** (semi-destructive; `PUBLIC_API`/`DATA` blast radius → Ask First).

**Chain template:**
`(PDM\|Lens[inventory] ‖ Void[CoK + usage/git/bug evidence]) → {Magi[essential axis] + Compete[killer axis/moat]} → 2×2 verdict → Sentinel-guard + refute×2-3[must-stay] + blast-radius → AskUserQuestion[removal slate Y/N/Modify] → if Y: Sherpa[phased, flag-off-first] → (Sweep[codex] ‖ Builder[codex]) → Radar[codex verify-green-after] → Guardian[removal report]`

Full inventory + dual-axis gate + safety/must-stay refutation + verdict + phased excision → `reference/inline-recipes.md`.

---

## acceptance

**Proof-Carrying PR pipeline v2 — Two-Axis (Code + Design)** for Tier-S/A merges. 14-30 agents Tier-S (UI), 8-21 Tier-A; Tier-B/C auto-downgrade to `feature`. G1-G10 guardrails. Cost: 3-15× vs `feature`. **Confirm before Tier-S launch.** Full Tier policy + G1-G10 + chain → `_common/PROOF_CARRYING.md`, `reference/acceptance-recipe.md`.

**Chain template:**
`Phase 0 tier+ui_dimension → 1 attest → 2A Code Oracles ‖ 2B Design Oracles (via atelier) → 3A/3B Adversaries → 4 judge+attest+canon+frame+vision → guardian joint verdict → G7 human sign-off (Tier-S UI) → 5 beacon+mend → 6 sampling`

Read: `_common/PROOF_CARRYING.md`, `reference/acceptance-recipe.md`.

---

## growth-acceptance

**Layer C lifecycle gate** (Market + Research + Brand axes) for Enterprise org-tier. Extends `acceptance` with pre-design Research Proof + Insight Ledger + Contract, ship-time Market Proof + Brand B.tone, post-launch +14/+30/+90d Measurement Loop. Org Tier gate (Solo abort / SMB Step 1 / Enterprise full). G11-G15 + 3-layer Brand Compiler. Cost: 1.1-8× on top of acceptance. **Confirm Step 3+.** Full lifecycle → `_common/GROWTH_BRAND_PROOF.md`, `reference/growth-acceptance-recipe.md`.

**Chain template:**
`Phase 0 classify → insight Ledger R/O → field?[fresh] → accord+spark Contract → 1 delegate to acceptance → 2 pulse+experiment Market+Incrementality ‖ ledger CAC/LTV ‖ compete cannibalization ‖ funnel+bazaar channel-fit ‖ vision+prose B.tone ‖ clause+oath+cloak+vigil G14 → 3 Measurement → G13 Stop → mend auto-halt → harvest+tome Ledger queue → 4 audits`

Read: `_common/GROWTH_BRAND_PROOF.md`, `reference/growth-acceptance-recipe.md`.

---

## summit

Multi-engine **five-team** quality-maximization. Dual-engine default (Codex ~65-70% / Claude ~30-35%); agy optional third axis when AVAILABLE. 28-119 agents, 49-193 min, 5-25× cost. **Always confirm.** Engine × team matrix + quorum rules → `reference/summit-recipe.md`.

**Chain template:**
`Phase 0 Framing → 1 Analysis ‖ design[Echo/Frame/Palette] → 2 Planning → 3 Design (Vision) ‖ Execution (rally engine-paradigm COLLABORATE) → 4 Verification (judge ‖ Codex dynamic ‖ Echo/Palette) → 5 Improvement (orbit, max 3 loops, magi-arbitrated) → 6 Guardian + Launch + Engine Audit`

Read: `reference/summit-recipe.md`.

---

## podium

**Content-quality maximization** — doc + high-quality slide creation, five teams (Research / Narrative / Production / Verification / Improvement). Dual-engine (Claude prose ~45-50% / Codex compile ~30-35%); agy optional (~15-25%). 16-53 agents, 35-130 min, 3-8× cost. Output_format variants (doc / slide / both / notebooklm / figma-slides). **Confirm release-critical.**

**Chain template:**
`Phase 0 Framing → 1 Research (Field audience ‖ Lens/Harvest/Quill ‖ external grounding) → 2 Narrative (Stage/Zine/Scribe/Tome + Magi) → 3 Production (Content ‖ Visual ‖ Layout) → 4 Verification (claim-grounding ‖ Canon ‖ Echo ‖ Palette ‖ Voyager ‖ judge) → 5 Improvement (orbit, max 2) → 6 Publish`

Read: `reference/podium-recipe.md`.

---

## loop

**Loop-engineering dispatcher & discipline gate** — the front-door for *underspecified* "make this a loop" requests. Does **not** run a loop: classifies the loop's *shape* (native-goal | rubric-quality | unattended-runner | discovery-to-ship), runs the **loop-engineering precondition gate** (verifiable oracle · external hard-stop bound · maker≠checker · persistent memory · drift-awareness — each failed precondition maps to a named anti-pattern: loopmaxxing / overbaking / nodding / amnesiac loop), then **routes to the engine that owns execution** (`goal` / `converge` / `orbit` / `apex`). Nexus stays the routing layer; `orbit` is the execution substrate — `loop` delegates and never re-implements it. Meta/control, not a task shape. The gate is contract-level (AUTORUN cannot skip); unattended `orbit` launches confirm before launch. 1 agent (inline classify + gate) + the routed engine's range. Distinct from `goal` (native `/goal` *setup only* — `loop` may route to it), `converge` (in-session rubric loop — `loop` routes to it), and `orbit` (the runner skill `loop` delegates to).

**Chain template:**
`FRAME (classify SHAPE) → GATE ★contract-level [oracle? bound? maker≠checker? memory? drift-aware? → fail → convert (1 question) or STOP] → ROUTE (native-goal→goal | rubric-quality→converge | unattended-runner→orbit [Confirm before launch] | discovery-to-ship→apex) → DELIVER (Loop Design Record)`

Read: `reference/loop-recipe.md`, `orbit/reference/loop-engineering.md`, `reference/loop-engineering-primitives.md`.

---

## converge

**Quality-convergence loop** — the invocable entry point for the Generator-Evaluator pattern (`reference/evaluator-loop-protocol.md`). A Generator produces/revises; **independent** Evaluators score against a Rubric tied to a Sprint Contract; the loop runs until ACCEPT or a hard bound. Execution-control, not a task shape (exposed as a subcommand because it carries a Contract/Rubric/bounds args the Mode table can't). Two forms: `converge` (standalone) and `converge <recipe>` (inner recipe as Generator). **Mandatory termination bounds**: max_cycles (3) / token_budget / diminishing-returns ε / BLOCK escalation — no unbounded run. **Flatten rule**: wrapping a loop-recipe (kaizen/apex/summit) uses its *generator agents*, not its loop, so converge owns the single termination oracle (avoids loop-on-loop blowup + dueling oracles). 4-10 agents × ≤3 cycles. Distinct from `kaizen` (metric-PDCA on existing features) and `goal` (unattended setup).

**Chain template:**
`CONTRACT (Scribe/Accord author/accept Sprint Contract + Rubric) → LOOP [ GENERATE (inner recipe flattened per rule, or task agent) → EVALUATE ‖ (independent Evaluators: Radar/Judge/Echo/Palette/Attest/Voyager per rubric dim; generator excluded) → AGGREGATE (Magi: ACCEPT | REVISE(δ) | BLOCK) → GATE (ACCEPT exit / REVISE next cycle / Δ<ε or max → stop+report / BLOCK escalate) ] → DELIVER (convergence report: trajectory + exit reason)`

Read: `reference/converge-recipe.md`, `reference/evaluator-loop-protocol.md`.

---

## migrate

**Change-completeness migration** — propagate a wholesale change across the codebase with a proven-complete guarantee (no omission). Cases: `arch` (layered→hexagonal, monolith→modular), `framework` (Express→Fastify, Vue2→Vue3), `middleware` (REST→gRPC, RabbitMQ→Kafka, store swap), `mock-to-prod` (stub/in-memory→real service). `case=lang` forwards to `transmute`. Double-loop: per-batch PLAN→EXECUTE→VERIFY inside an outer completeness loop closed by a **RESIDUE-GATE** (forward counter + independent loop-until-dry re-scan + `matrix` axis-coverage), then a **DECOMMISSION** phase that removes old code *gated on the completeness proof*. Strategy: strangler-fig (default) ‖ parallel-run ‖ big-bang. 6-20 agents. **Confirm whole-system arch / big-bang.**

**Chain template:**
`INVENTORY (Lens all sites ‖ Ripple blast radius → freeze baseline denominator) → STRATEGY (Magi risk gate + Sherpa batch split) → OUTER LOOP [ INNER LOOP: PLAN (Ripple) → EXECUTE (Atlas/Shift/Forge → Builder/Artisan +gateway/schema/stream) → VERIFY (Radar drift==0, fail→rollback batch) ; RESIDUE-GATE (counter complete + residue 2× zero + axes covered) ] → ATTEST (completeness report) → DECOMMISSION [GATE on ATTEST → Sweep detect → Ripple+Lens re-check refs==0 → Builder cut +Void → Radar green → Guardian separate PR]`

Read: `reference/migrate-recipe.md`.

---

## transmute

**Cross-language rewrite** preserving behavior (TS→Rust, Go→Rust, Python→Go, JS→TS, …). Idiomatic re-expression verified by **differential parity** against golden oracle. Distinct from `PORTING` / `shift` (same-language migration / native-API modernization) / `refactor`. Strategy: big-bang ‖ strangler-fig ‖ FFI-incremental. 8-20 agents. **Confirm before big-bang.**

**Chain template:**
`Phase 0 Framing → 1 Archaeology (Trail [static-rules + history] ‖ Lens ‖ Atlas?) → 2 Contract (Accord → Mint golden oracle) → 3 Strategy (Magi risk gate + Transmutation Map) → 4 Transmute (Builder/Artisan +grok?+gateway/schema?; rally engine-paradigm COMPETE for high-risk) → 5 Parity Verify (Radar differential ‖ Attest conformance ‖ judge ‖ Voyager?) → 6 Ship (Guardian)`

Read: `reference/transmute-recipe.md`.

---

## clone

**Faithful product reproduction** — reverse-engineer an *existing* product's observable surface and rebuild it as a complete copy, **verified by differential parity** against a captured baseline (not assertion). The black-box analog of `transmute`: where transmute extracts its oracle *from your own source*, clone captures the oracle by *observing an external product* (UI / behavior / features / data shape / assets). **Platform-agnostic**: `target_type` ∈ live-web | **desktop** (macOS/Win/Linux GUI) | mobile | has-source | api — same Parity Map, capture mechanism varies (web=Vector/Voyager, desktop=Wield/external UI-automation harness). Two principles: **capture-from-evidence** (every reproduced screen is grounded in a captured artifact, never memory) and **fidelity-over-faith** (the copy is diffed against the baseline). Three integrity gates: **Capture Completeness** (every screen/state/flow), **Provenance & Drift** (baseline is a stamped snapshot; re-check before SHIP), **Differential Parity engine** (explicit per-dimension comparators + non-determinism canonicalization, shared discipline with transmute §3a). Distinct from `transmute` (own-source rewrite) / `migrate` (own-system completeness) / `PORTING` (web→native) / `pixel` (single mockup) / `feature` (net-new inspired design). Opens with an **interactive Stack Dialogue** (Phase 0.1, contract-level — AUTORUN cannot skip) that locks the target rebuild stack (per layer, with stack-vs-fidelity tradeoffs explicit) into a Stack Decision Record before capture/build; `stack=` pre-supplies it. Strategy: extract-and-rebuild (default) ‖ scaffold-from-source ‖ incremental-clone ‖ big-bang. 8-24 agents. **Confirm before big-bang full clone.**

**Chain template:**
`Phase 0 Framing (target_type + provenance stamp + robustness obstacles) → 0.1 Stack Dialogue (INTERACTIVE, contract-level — AUTORUN cannot skip: fingerprint original stack ‖ Lens/Atlas read user repo/constraints → layered AskUserQuestion runtime→frontend→styling→state→backend→data→build→deploy, surface stack-vs-fidelity tradeoffs → lock Stack Decision Record; `stack=` confirms not explores) → 0.5 Research Sweep (deep-research[+Compete?] → cited Evidence Ledger: T1 docs/design-system/API-ref/changelog → T4 community; reference/research-grounding.md → completeness denominator + exact values + version/drift; research-first, capture-authoritative) → 1 Capture (Vector/Voyager crawl+screenshot+network | Wield desktop ‖ Frame/Pixel design-extract ‖ Lens? ‖ Schema? ‖ Echo/Trace? ‖ PDM/Lens feature-inventory ‖ Ink/Pixel? asset-extract) → 2 Spec+Baseline (Scribe/Accord spec → stamped parity baseline + Capture Completeness Gate + Provenance & Drift Gate) → 3 Architect (Magi capture-strategy gate + Parity Map; Atlas?/Muse?) → 4 Rebuild (Forge→Artisan/Builder + Pixel pixel-accurate +gateway/schema?+flow?; rally COMPETE for fidelity-critical screens) → 5 Parity Verify (Pixel/Voyager visual ‖ Radar/Voyager behavioral ‖ Attest feature ‖ Pixel/Frame asset ‖ judge fidelity; drift re-check; loop ≤3 cycles) → 6 Ship (Guardian + Fidelity Report incl. provenance + drift status)`

Read: `reference/clone-recipe.md`.

---

## fuse

**Multi-source product synthesis** — the synthesis extension of `clone`. Where `clone` reproduces **one** product faithfully against a single baseline, `fuse` captures **two or more** products (clone's full capture/provenance/parity machinery, run per source) and **synthesizes them into one new product**: adopting selected elements from each source, merging overlapping ones, and adding net-new connective tissue. The deliverable is **intentionally not a faithful copy of any single source**, so clone's single-baseline oracle no longer applies — `fuse` adds the three things clone cannot express: a **Fusion Map** (assigns every element of the new product a provenance `{adopt-A|adopt-B|merge|net-new|drop}` + resolution rationale + oracle), a **dual/selective oracle** (adopted elements → differential parity vs *that source's* baseline; merged/net-new → spec+AC conformance — never confused), and a **Coherence Gate** (proves the result is one product — one visual language / interaction grammar / terminology / data model — not a Frankenstein patchwork). Conflicts between sources (two nav models, two schemas for "the same" entity) are resolved in a **Conflict Ledger** (Magi-arbitrated against the Fusion Thesis). Multi-source IP/trade-dress posture is recorded per adopted element. `sources=2..N`, mixed `target_type` allowed. Distinct from `clone` (one source, fidelity *is* the goal), `feature`/`apex` (net-new, only inspired — no captured baselines), `migrate` (own-system consolidation), `transmute` (own-source rewrite). Pair `spec → fuse` when *which* elements to take from each source is itself unsettled. 12-32 agents, high cost. **Confirm before big-bang full fusion OR sources ≥ 3.**

**Chain template:**
`Phase 0 Framing (sources + per target_type + new-product stack + Fusion Thesis + per-source provenance stamps) → 1 Capture ∥ (clone Phase 0.5 research sweep + Phase 1 per source → per-source Evidence Ledger + one stamped baseline each, research+coverage scoped to the adopted slice; +1 fusion-level Compete sweep → Thesis/Conflict rationale; reference/research-grounding.md) → 2 Fusion Map+Spec (Spark synthesis ‖ Magi conflict-arbitration → Fusion Map + Conflict Ledger + Accord/Scribe L3 ACs for merge/net-new → Fusion Map Gate + Selective-Oracle Gate + Coherence Contract + IP/Trade-Dress Gate) → 3 Architect (Magi strategy + Atlas unified arch + Muse reconcile tokens + Schema?/Gateway? reconcile data/API) → 4 Build (adopted=Pixel/Builder clone-discipline ‖ merged/net-new=Forge→Artisan/Builder feature-discipline; rally COMPETE for fidelity-critical + hard merges) → 5 Dual Verify ∥ (selective parity vs source baseline ‖ Attest spec-conformance ‖ Coherence Gate visual/interaction/conceptual/data ‖ judge synthesis review; per-source drift re-check; Fusion-Map coverage re-check; loop ≤3 cycles) → 6 Ship (Guardian + Fusion Report)`

Read: `reference/fuse-recipe.md`.

---

## graft

**Concept transplant for innovation** — the extension of `fuse` and the **inverse of `clone` on the fidelity axis**. Where `clone`/`fuse` reproduce *observable surfaces* by parity, `graft` takes **your current owned product** as the *host* (white-box, mapped from source — not captured) and extracts a specific reference product's (the *donor*) important **concepts** — its load-bearing principles/mechanisms, abstracted *away* from the donor's surface — then transplants and adapts them onto the host to produce a **genuinely innovative** product. It **explicitly rejects surface copying** (the opposite of clone): a graft that copies the donor's chrome while missing the idea that made it work has failed. Verified by a **triple oracle** held on *every* graft: **concept-fidelity** (the donor concept's mechanism/effect reproduced, re-expressed originally in the host's surface — Attest+judge, high donor-resemblance is a *smell*) ∧ **host-integrity** (the living product's existing-behavior regression net stays 100% green + declared invariants hold — Radar+Ripple) ∧ **Innovation Gate** (emergent novelty neither host nor donor had, surviving adversarial "this is just a bolt-on/gimmick" refutation + felt-novelty via Echo + defensibility via Compete — borrowing `killer`'s moat/refutation discipline). A graft that is concept-faithful and host-safe but fails the Innovation Gate is delivered honestly as "a feature, not an innovation." Core artifact: **Graft Map** (per donor concept → `adapt`|`hybridize`|`invert`|`reject` + host attachment point + adaptation + per-graft innovation thesis + invariants respected); plus a **Host-Invariant Contract** (value-path/workflow/data/contract non-negotiables) and a per-graft **originality posture** (default: re-implement the idea originally — concept-level transplant is structurally lower IP-risk than surface reproduction). Flux is core (concept distillation + hybridize/invert novelty moves), not optional. Ships behind a feature flag with adoption KPI + kill criterion (killer-style) unless waived at Phase 0. `host=1, donors=1..N`. Distinct from `fuse` (peer external sources, surface synthesis, no owned host), `clone` (surface reproduction), `kaizen` (metric PDCA, no external concept/novelty bar), `feature` (additive, no concept extraction/innovation gate), `killer` (verdict only — pair `killer → graft`). 10-28 agents. **Confirm when invasive to host core OR shipping without a flag.**

**Chain template:**
`Phase 0 Framing (host + donor(s) + Host Invariants + Innovation Thesis) → 1 Ground ∥ (HOST: Lens/Atlas map + PDM inventory + Radar freeze regression net ‖ DONOR: deep-research concept-rationale sweep first [reference/research-grounding.md] → observe→Flux+Magi distill to Concept Catalog/essence ‖ host-domain/competitive sweep → Innovation Thesis) → 2 Graft Map+Spec (Flux novelty moves → Magi select [subtraction] → Graft Map + Accord/Scribe concept-fidelity spec+L3 ACs + Ripple blast radius → Graft Map Gate + Triple-Oracle Gate + Host-Invariant Contract + Originality Posture) → 3 Architect (Magi strategy + Atlas integrate-into-host + Ripple ‖ Omen pre-mortem + Muse? re-express in host tokens) → 4 Build (Forge spike novel graft first → Artisan/Builder onto host under isolation:worktree, regression net stays green; rally COMPETE on high-innovation grafts) → 5 Verify ∥ (concept-fidelity Attest/judge ‖ host-integrity Radar/Ripple ‖ Innovation Gate judge+refute×2-3+Echo+Compete+Magi Go/No-Go; coverage re-check; loop ≤3 cycles) → 6 Ship (Guardian + Graft Report + flag[KPI+kill])`

Read: `reference/graft-recipe.md`.

---

## package (includes legacy `venture` as `domain=startup`)

**Generalized document-package generator** — **12-domain preset registry**: `startup` (the legacy `venture` blueprint) / generic / research / ai-adoption / legal* / saas / media / growth / career / learning / hiring* / local-gov*. Per-domain swap: directories, role→skill map, traceability anchor (F-/H-/UC-/R-/P-/E-/T-/LO-/I-), risk gates (*=mandatory). Single Phase 0-6 engine. Depth 5-28 agents (`startup` tiers: lite 6-8, mvp(default) 14-18, raise 16-20, full 24-28). **Confirm full depth.**

**Chain template:**
`Phase 0 Framing (preset auto-detect + risk-flag) → 1 Research (preset skills; deep-research for research preset) → 2 Spine [BARRIER: entity-id per anchor] → 3 Parallel Doc Tracks (preset map, waves) → 4 Synthesis → 5 Validate (attest/judge + risk gate + manifest + report + README) → 6 Package`

**`startup` preset chain (legacy `venture` form):**
`Phase 0 → 1 Research (field+compete ‖ plea+cast) → 2 Product Spine [BARRIER: F-001 + MoSCoW] (accord+spark+rank+pulse+void?) → 3 Parallel Doc Tracks, feature_id-bound (Brand / UX / LP / Mktg / Tech / AI / Legal / Test / PM / Mock / Assets) → 4 Overview synthesis → 5 Validate → 6 Package (UTF-8 + zip + lint + unzip test + PII scrub)`

Read: `reference/package-recipe.md`. Startup-preset deep blueprint: `reference/venture-recipe.md`.
