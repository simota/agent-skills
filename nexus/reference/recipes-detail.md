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

**Interactive feature-proposal → locked specification through deep human-in-the-loop dialogue.** Takes a rough idea and refines it conversationally into a sign-off-ready spec carrying **mandatory testable, traceable acceptance criteria**, then **stops at the spec — writes no code**. The discovery half of `spec → feature`/`apex`, mirroring `charter → enact`. Uniquely **defaults to `INTERACTIVE`** (the dialogue is the deliverable); its phase-boundary checkpoints are contract-level, so even AUTORUN cannot skip them. **+Lens reuse-scan grounds it in the existing codebase; draft-persisted & resumable** (`spec resume [<slug>]`); locks only when **both lock preconditions pass — testable L3 ACs + the Spec Quality Gate** (ambiguity/completeness/consistency/testability/scope) — and writes `docs/specs/<slug>.md` per a standard template. Distinct from `essential`/`killer` (which-feature *verdict*, minimal dialogue), `feature`/`apex` (build code), `charter` (whole-repo team design), `converge` (automated grading loop), and `riff` (single-agent brainstorm, no artifact). 3-9 agents × dialogue turns.

**Chain template:**
`FRAME (Plea +Field?/Cast? +Lens?[reuse-scan/constraints]) → ✓confirm-problem + draft-init → EXPAND (Riff ‖ Flux +Compete?) → ✓steer + draft → CHALLENGE (Magi + Void + Ripple +Omen?) → ✓pick + convergence-check + draft → SHAPE (Spark +Rank?) → ✓edit + draft → SPECIFY (Accord +Scribe?/Gateway?/Schema?, L3 ACs+IDs mandatory +Attest?/Echo?) → ✓iterate + draft → LOCK (✓quality-gate: Judge+Attest+Magi? → ✓sign-off → promote draft to docs/specs/<slug>.md per template + Open Questions → ✓build-path: orbit loop (✓engine claude|codex|agy) ‖ apex; fallbacks feature|acceptance|essential|killer)` · resumable via `spec resume [<slug>]`

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

**Faithful product reproduction** — reverse-engineer an *existing* product's observable surface and rebuild it as a complete copy, **verified by differential parity** against a captured baseline (not assertion). The black-box analog of `transmute`: where transmute extracts its oracle *from your own source*, clone captures the oracle by *observing an external product* (UI / behavior / features / data shape / assets). **Platform-agnostic**: `target_type` ∈ live-web | **desktop** (macOS/Win/Linux GUI) | mobile | has-source | api — same Parity Map, capture mechanism varies (web=Vector/Voyager, desktop=Wield/external UI-automation harness). Two principles: **capture-from-evidence** (every reproduced screen is grounded in a captured artifact, never memory) and **fidelity-over-faith** (the copy is diffed against the baseline). Three integrity gates: **Capture Completeness** (every screen/state/flow), **Provenance & Drift** (baseline is a stamped snapshot; re-check before SHIP), **Differential Parity engine** (explicit per-dimension comparators + non-determinism canonicalization, shared discipline with transmute §3a). Distinct from `transmute` (own-source rewrite) / `migrate` (own-system completeness) / `PORTING` (web→native) / `pixel` (single mockup) / `feature` (net-new inspired design). Opens with an **interactive Stack Dialogue** (Phase 0.1, contract-level — AUTORUN cannot skip) that locks the target rebuild stack (per layer, with stack-vs-fidelity tradeoffs explicit) into a Stack Decision Record before capture/build; `stack=` pre-supplies it. Strategy: extract-and-rebuild (default) ‖ scaffold-from-source ‖ incremental-clone ‖ big-bang. 8-24 agents. **Confirm before big-bang full clone.**

**Chain template:**
`Phase 0 Framing (target_type + provenance stamp + robustness obstacles) → 0.1 Stack Dialogue (INTERACTIVE, contract-level — AUTORUN cannot skip: fingerprint original stack ‖ Lens/Atlas read user repo/constraints → layered AskUserQuestion runtime→frontend→styling→state→backend→data→build→deploy, surface stack-vs-fidelity tradeoffs → lock Stack Decision Record; `stack=` confirms not explores) → 0.5 Research Sweep (deep-research[+Compete?] → cited Evidence Ledger: T1 docs/design-system/API-ref/changelog → T4 community; reference/research-grounding.md → completeness denominator + exact values + version/drift; research-first, capture-authoritative) → 1 Capture (Vector/Voyager crawl+screenshot+network | Wield desktop ‖ Frame/Pixel design-extract ‖ Lens? ‖ Schema? ‖ Echo/Trace? ‖ PDM/Lens feature-inventory ‖ Ink/Pixel? asset-extract) → 2 Spec+Baseline (Scribe/Accord spec → stamped parity baseline + Capture Completeness Gate + Provenance & Drift Gate) → 3 Architect (Magi capture-strategy gate + Parity Map; Atlas?/Muse?) → 4 Rebuild (Forge→Artisan/Builder + Pixel pixel-accurate +gateway/schema?+flow?; rally COMPETE for fidelity-critical screens) → 5 Parity Verify (Pixel/Voyager visual ‖ Radar/Voyager behavioral ‖ Attest feature ‖ Pixel/Frame asset ‖ judge fidelity; drift re-check; loop ≤3) → 6 Ship (Guardian + Fidelity Report incl. provenance + drift status)`

Read: `reference/clone-recipe.md`.

---

## fuse

**Multi-source product synthesis** — the synthesis extension of `clone`. Where `clone` reproduces **one** product faithfully against a single baseline, `fuse` captures **two or more** products (clone's full capture/provenance/parity machinery, run per source) and **synthesizes them into one new product**: adopting selected elements from each source, merging overlapping ones, and adding net-new connective tissue. The deliverable is **intentionally not a faithful copy of any single source**, so clone's single-baseline oracle no longer applies — `fuse` adds the three things clone cannot express: a **Fusion Map** (assigns every element of the new product a provenance `{adopt-A|adopt-B|merge|net-new|drop}` + resolution rationale + oracle), a **dual/selective oracle** (adopted elements → differential parity vs *that source's* baseline; merged/net-new → spec+AC conformance — never confused), and a **Coherence Gate** (proves the result is one product — one visual language / interaction grammar / terminology / data model — not a Frankenstein patchwork). Conflicts between sources (two nav models, two schemas for "the same" entity) are resolved in a **Conflict Ledger** (Magi-arbitrated against the Fusion Thesis). Multi-source IP/trade-dress posture is recorded per adopted element. `sources=2..N`, mixed `target_type` allowed. Distinct from `clone` (one source, fidelity *is* the goal), `feature`/`apex` (net-new, only inspired — no captured baselines), `migrate` (own-system consolidation), `transmute` (own-source rewrite). Pair `spec → fuse` when *which* elements to take from each source is itself unsettled. 12-32 agents, high cost. **Confirm before big-bang full fusion OR sources ≥ 3.**

**Chain template:**
`Phase 0 Framing (sources + per target_type + new-product stack + Fusion Thesis + per-source provenance stamps) → 1 Capture ∥ (clone Phase 0.5 research sweep + Phase 1 per source → per-source Evidence Ledger + one stamped baseline each, research+coverage scoped to the adopted slice; +1 fusion-level Compete sweep → Thesis/Conflict rationale; reference/research-grounding.md) → 2 Fusion Map+Spec (Spark synthesis ‖ Magi conflict-arbitration → Fusion Map + Conflict Ledger + Accord/Scribe L3 ACs for merge/net-new → Fusion Map Gate + Selective-Oracle Gate + Coherence Contract + IP/Trade-Dress Gate) → 3 Architect (Magi strategy + Atlas unified arch + Muse reconcile tokens + Schema?/Gateway? reconcile data/API) → 4 Build (adopted=Pixel/Builder clone-discipline ‖ merged/net-new=Forge→Artisan/Builder feature-discipline; rally COMPETE for fidelity-critical + hard merges) → 5 Dual Verify ∥ (selective parity vs source baseline ‖ Attest spec-conformance ‖ Coherence Gate visual/interaction/conceptual/data ‖ judge synthesis review; per-source drift re-check; Fusion-Map coverage re-check; loop ≤3) → 6 Ship (Guardian + Fusion Report)`

Read: `reference/fuse-recipe.md`.

---

## graft

**Concept transplant for innovation** — the extension of `fuse` and the **inverse of `clone` on the fidelity axis**. Where `clone`/`fuse` reproduce *observable surfaces* by parity, `graft` takes **your current owned product** as the *host* (white-box, mapped from source — not captured) and extracts a specific reference product's (the *donor*) important **concepts** — its load-bearing principles/mechanisms, abstracted *away* from the donor's surface — then transplants and adapts them onto the host to produce a **genuinely innovative** product. It **explicitly rejects surface copying** (the opposite of clone): a graft that copies the donor's chrome while missing the idea that made it work has failed. Verified by a **triple oracle** held on *every* graft: **concept-fidelity** (the donor concept's mechanism/effect reproduced, re-expressed originally in the host's surface — Attest+judge, high donor-resemblance is a *smell*) ∧ **host-integrity** (the living product's existing-behavior regression net stays 100% green + declared invariants hold — Radar+Ripple) ∧ **Innovation Gate** (emergent novelty neither host nor donor had, surviving adversarial "this is just a bolt-on/gimmick" refutation + felt-novelty via Echo + defensibility via Compete — borrowing `killer`'s moat/refutation discipline). A graft that is concept-faithful and host-safe but fails the Innovation Gate is delivered honestly as "a feature, not an innovation." Core artifact: **Graft Map** (per donor concept → `adapt`|`hybridize`|`invert`|`reject` + host attachment point + adaptation + per-graft innovation thesis + invariants respected); plus a **Host-Invariant Contract** (value-path/workflow/data/contract non-negotiables) and a per-graft **originality posture** (default: re-implement the idea originally — concept-level transplant is structurally lower IP-risk than surface reproduction). Flux is core (concept distillation + hybridize/invert novelty moves), not optional. Ships behind a feature flag with adoption KPI + kill criterion (killer-style) unless waived at Phase 0. `host=1, donors=1..N`. Distinct from `fuse` (peer external sources, surface synthesis, no owned host), `clone` (surface reproduction), `kaizen` (metric PDCA, no external concept/novelty bar), `feature` (additive, no concept extraction/innovation gate), `killer` (verdict only — pair `killer → graft`). 10-28 agents. **Confirm when invasive to host core OR shipping without a flag.**

**Chain template:**
`Phase 0 Framing (host + donor(s) + Host Invariants + Innovation Thesis) → 1 Ground ∥ (HOST: Lens/Atlas map + PDM inventory + Radar freeze regression net ‖ DONOR: deep-research concept-rationale sweep first [reference/research-grounding.md] → observe→Flux+Magi distill to Concept Catalog/essence ‖ host-domain/competitive sweep → Innovation Thesis) → 2 Graft Map+Spec (Flux novelty moves → Magi select [subtraction] → Graft Map + Accord/Scribe concept-fidelity spec+L3 ACs + Ripple blast radius → Graft Map Gate + Triple-Oracle Gate + Host-Invariant Contract + Originality Posture) → 3 Architect (Magi strategy + Atlas integrate-into-host + Ripple ‖ Omen pre-mortem + Muse? re-express in host tokens) → 4 Build (Forge spike novel graft first → Artisan/Builder onto host under isolation:worktree, regression net stays green; rally COMPETE on high-innovation grafts) → 5 Verify ∥ (concept-fidelity Attest/judge ‖ host-integrity Radar/Ripple ‖ Innovation Gate judge+refute×2-3+Echo+Compete+Magi Go/No-Go; coverage re-check; loop ≤3) → 6 Ship (Guardian + Graft Report + flag[KPI+kill])`

Read: `reference/graft-recipe.md`.

---

## package (includes legacy `venture` as `domain=startup`)

**Generalized document-package generator** — **12-domain preset registry**: `startup` (the legacy `venture` blueprint) / generic / research / ai-adoption / legal* / saas / media / growth / career / learning / hiring* / local-gov*. Per-domain swap: directories, role→skill map, traceability anchor (F-/H-/UC-/R-/P-/E-/T-/LO-/I-), risk gates (*=mandatory). Single Phase 0-6 engine. Depth 5-28 agents (`startup` tiers: lite 6-8, mvp(default) 14-18, raise 16-20, full 24-28). **Confirm full depth.**

**Chain template:**
`Phase 0 Framing (preset auto-detect + risk-flag) → 1 Research (preset skills; deep-research for research preset) → 2 Spine [BARRIER: entity-id per anchor] → 3 Parallel Doc Tracks (preset map, waves) → 4 Synthesis → 5 Validate (attest/judge + risk gate + manifest + report + README) → 6 Package`

**`startup` preset chain (legacy `venture` form):**
`Phase 0 → 1 Research (field+compete ‖ plea+cast) → 2 Product Spine [BARRIER: F-001 + MoSCoW] (accord+spark+rank+pulse+void?) → 3 Parallel Doc Tracks, feature_id-bound (Brand / UX / LP / Mktg / Tech / AI / Legal / Test / PM / Mock / Assets) → 4 Overview synthesis → 5 Validate → 6 Package (UTF-8 + zip + lint + unzip test + PII scrub)`

Read: `reference/package-recipe.md`. Startup-preset deep blueprint: `reference/venture-recipe.md`.
