# Recipes — Detail

Extended descriptions for verbose Recipe rows. The Recipes table in `SKILL.md` carries the canonical name / subcommand / chain template / Read pointer; this file expands the "When to Use" prose that does not fit on one row.

---

## kaizen

Existing-feature continuous improvement covering perf / UX / code-quality / feature-extension. **PDCA loop, not single-pass**: improves against a quantified target and stops on target-met or diminishing-returns. Differs from `refactor` (internal-only), `optimize` (perf-only), and `feature` (new addition). Scale: 4-8 agents (× cycles, default cap 3).

**Chain template:**
`(Lens + Pulse?/Echo?/Voice?/Trace?)[baseline] → Spark → Magi[axes + target + stop] → ⟲{ (Bolt/Tuner ‖ Palette/Prose/Flow ‖ Zen/Sweep ‖ Artisan/Builder)[axis] → Radar[+cross-axis guard] → Pulse?/Echo?[re-measure vs target] }⟲ → Void[stop-confirm] → Guardian`

The `⟲{…}⟲` block loops until target-met OR diminishing-returns OR iteration cap. Full phase contract (DIAGNOSE+BASELINE / PROPOSE+TARGET / IMPROVE / VERIFY+LOOP / SHIP) → `reference/inline-recipes.md`.

---

## apex

Full-cycle auto-implementation: discovery → spec → parallel design → risk gate → loop → ship. With no-args, Phase 0 autonomously discovers the goal. 8-25 agents, high-cost. **Confirm before launch.**

**Chain template:**
`(Phase 0 if no goal) → Discovery (plea+field+echo?) → Ideate (riff) → Verdict (magi) → Spec (accord+void?+scribe?) → Design [Tech (atlas+gateway?+schema?) ‖ UX (Vision sub-orchestrates muse+palette+prose+flow?+frame?+forge+echo)] → Risk Gate (omen+ripple+echo) → Loop (Orbit on Codex CLI drives builder+artisan?+vitrine?+judge+radar+voyager?) → Acceptance Verification (attest: AC-conformance gate) → Ship (guardian+launch)`

Guarded by a run-level budget envelope (hard-abort at ceiling) + cross-phase checkpoint-resume. `attest` gates Ship on accord's L3 ACs (convergence ≠ correctness).

Read: `reference/apex-recipe.md`, `reference/apex-walkthrough.md`.

---

## charter

**Repo-wide analysis → self-driving Charter, team design included — stops at the document.** Document-first planning recipe; the execution half is `enact`. Where `apex` discovers a *feature* and ships it in one shot, `charter` reads the *whole repository*, distills a durable Charter artifact (`docs/CHARTER.md` + `CHARTER.roster.yaml`) that designs the team (§5 roster + §6 orchestration plan) and §10 checklists (pre-flight / per-package Definition-of-Done / progress tracker / final delivery) without building or running it. The team becomes a pure function of the document, so `enact` (or a future session) reconstructs the identical team and gates each boundary on the checklists. Distinct from `apex` (feature-centric, one-shot), `goal` (loop config only), `package` (docs only). The §5/§6 design is **multi-engine by default** (`engines=claude+codex`): Claude Code for plan/design/review, Codex CLI (model `gpt-5.5`) for build loops + high-volume parallel coding (Orbit sub-hub pinned to Codex, per-engine prereqs + `fallback_engine` recorded for `enact`). Modes: autonomous (no-args) / objective-supplied / `scope=` / `out=` / `engines=`. 5-15 agents (analysis + authoring only). No execution → no Confirm Gate.

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

## spec

**Interactive feature-proposal → locked specification through deep human-in-the-loop dialogue.** Takes a rough idea and refines it conversationally into a sign-off-ready spec carrying **mandatory testable acceptance criteria**, then **stops at the spec — writes no code**. The discovery half of `spec → feature`/`apex`, mirroring `charter → enact`. Uniquely **defaults to `INTERACTIVE`** (the dialogue is the deliverable); its phase-boundary checkpoints are contract-level, so even AUTORUN cannot skip them. Distinct from `essential`/`killer` (which-feature *verdict*, minimal dialogue), `feature`/`apex` (build code), `charter` (whole-repo team design), `converge` (automated grading loop), and `riff` (single-agent brainstorm, no artifact). 3-8 agents × dialogue turns.

**Chain template:**
`FRAME (Plea +Field?/Cast?) → ✓confirm-problem → EXPAND (Riff ‖ Flux +Compete?) → ✓steer → CHALLENGE (Magi + Void + Ripple +Omen?) → ✓pick + convergence-check → SHAPE (Spark +Rank?) → ✓edit → SPECIFY (Accord +Scribe?/Gateway?/Schema?, L3 ACs mandatory +Attest?/Echo?) → ✓iterate → LOCK (✓sign-off → docs/specs/<slug>.md + Open Questions → recommend /nexus feature|apex|acceptance)`

Full phase contract (FRAME / EXPAND / CHALLENGE / SHAPE / SPECIFY / LOCK), boundaries, and anti-patterns → `reference/spec-recipe.md`.

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

## converge

**Quality-convergence loop** — the invocable entry point for the Generator-Evaluator pattern (`reference/evaluator-loop-protocol.md`). A Generator produces/revises; **independent** Evaluators score against a Rubric tied to a Sprint Contract; the loop runs until ACCEPT or a hard bound. Execution-control, not a task shape (exposed as a subcommand because it carries a Contract/Rubric/bounds args the Mode table can't). Two forms: `converge` (standalone) and `converge <recipe>` (inner recipe as Generator). **Mandatory termination bounds**: max_cycles (3) / token_budget / diminishing-returns ε / BLOCK escalation — no unbounded run. **Flatten rule**: wrapping a loop-recipe (kaizen/apex/summit) uses its *generator agents*, not its loop, so converge owns the single termination oracle (avoids loop-on-loop blowup + dueling oracles). 4-10 agents × cycles (cap 3). Distinct from `kaizen` (metric-PDCA on existing features) and `goal` (unattended setup).

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

**Faithful product reproduction** — reverse-engineer an *existing* product's observable surface and rebuild it as a complete copy, **verified by differential parity** against a captured baseline (not assertion). The black-box analog of `transmute`: where transmute extracts its oracle *from your own source*, clone captures the oracle by *observing an external product* (UI / behavior / features / data shape / assets). **Platform-agnostic**: `target_type` ∈ live-web | **desktop** (macOS/Win/Linux GUI) | mobile | has-source | api — same Parity Map, capture mechanism varies (web=Vector/Voyager, desktop=Wield/external UI-automation harness). Two principles: **capture-from-evidence** (every reproduced screen is grounded in a captured artifact, never memory) and **fidelity-over-faith** (the copy is diffed against the baseline). Three integrity gates: **Capture Completeness** (every screen/state/flow), **Provenance & Drift** (baseline is a stamped snapshot; re-check before SHIP), **Differential Parity engine** (explicit per-dimension comparators + non-determinism canonicalization, shared discipline with transmute §3a). Distinct from `transmute` (own-source rewrite) / `migrate` (own-system completeness) / `PORTING` (web→native) / `pixel` (single mockup) / `feature` (net-new inspired design). Strategy: extract-and-rebuild (default) ‖ scaffold-from-source ‖ incremental-clone ‖ big-bang. 8-24 agents. **Confirm before big-bang full clone.**

**Chain template:**
`Phase 0 Framing (target_type + provenance stamp + robustness obstacles) → 1 Capture (Vector/Voyager crawl+screenshot+network | Wield desktop ‖ Frame/Pixel design-extract ‖ Lens? ‖ Schema? ‖ Echo/Trace? ‖ PDM/Lens feature-inventory ‖ Ink/Pixel? asset-extract) → 2 Spec+Baseline (Scribe/Accord spec → stamped parity baseline + Capture Completeness Gate + Provenance & Drift Gate) → 3 Architect (Magi capture-strategy gate + Parity Map; Atlas?/Muse?) → 4 Rebuild (Forge→Artisan/Builder + Pixel pixel-accurate +gateway/schema?+flow?; rally COMPETE for fidelity-critical screens) → 5 Parity Verify (Pixel/Voyager visual ‖ Radar/Voyager behavioral ‖ Attest feature ‖ Pixel/Frame asset ‖ judge fidelity; drift re-check; loop ≤3) → 6 Ship (Guardian + Fidelity Report incl. provenance + drift status)`

Read: `reference/clone-recipe.md`.

---

## package (includes legacy `venture` as `domain=startup`)

**Generalized document-package generator** — **12-domain preset registry**: `startup` (the legacy `venture` blueprint) / generic / research / ai-adoption / legal* / saas / media / growth / career / learning / hiring* / local-gov*. Per-domain swap: directories, role→skill map, traceability anchor (F-/H-/UC-/R-/P-/E-/T-/LO-/I-), risk gates (*=mandatory). Single Phase 0-6 engine. Depth 5-28 agents (`startup` tiers: lite 6-8, mvp(default) 14-18, raise 16-20, full 24-28). **Confirm full depth.**

**Chain template:**
`Phase 0 Framing (preset auto-detect + risk-flag) → 1 Research (preset skills; deep-research for research preset) → 2 Spine [BARRIER: entity-id per anchor] → 3 Parallel Doc Tracks (preset map, waves) → 4 Synthesis → 5 Validate (attest/judge + risk gate + manifest + report + README) → 6 Package`

**`startup` preset chain (legacy `venture` form):**
`Phase 0 → 1 Research (field+compete ‖ plea+cast) → 2 Product Spine [BARRIER: F-001 + MoSCoW] (accord+spark+rank+pulse+void?) → 3 Parallel Doc Tracks, feature_id-bound (Brand / UX / LP / Mktg / Tech / AI / Legal / Test / PM / Mock / Assets) → 4 Overview synthesis → 5 Validate → 6 Package (UTF-8 + zip + lint + unzip test + PII scrub)`

Read: `reference/package-recipe.md`. Startup-preset deep blueprint: `reference/venture-recipe.md`.
