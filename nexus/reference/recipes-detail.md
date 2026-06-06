# Recipes — Detail

Extended descriptions for verbose Recipe rows. The Recipes table in `SKILL.md` carries the canonical name / subcommand / chain template / Read pointer; this file expands the "When to Use" prose that does not fit on one row.

---

## kaizen

Existing-feature continuous improvement covering perf / UX / code-quality / feature-extension. Differs from `refactor` (internal-only), `optimize` (perf-only), and `feature` (new addition). Scale: 4-8 agents.

**Chain template:**
`(Lens + Pulse?/Echo?/Voice?/Trace?) → Spark → Magi → (Bolt/Tuner ‖ Palette/Prose/Flow ‖ Zen/Sweep ‖ Artisan/Builder)[axis] → Radar → Pulse?/Echo?[re-measure] → Guardian`

Full phase contract (DIAGNOSE/PROPOSE/IMPROVE/VERIFY/SHIP) → `reference/inline-recipes.md`.

---

## apex

Full-cycle auto-implementation: discovery → spec → parallel design → risk gate → loop → ship. With no-args, Phase 0 autonomously discovers the goal. 8-25 agents, high-cost. **Confirm before launch.**

**Chain template:**
`(Phase 0 if no goal) → Discovery (plea+field+echo?) → Ideate (riff) → Verdict (magi) → Spec (accord+void?+scribe?) → Design [Tech (atlas+gateway?+schema?) ‖ UX (Vision sub-orchestrates muse+palette+prose+flow?+frame?+forge+echo)] → Risk Gate (omen+ripple+echo) → Loop (Orbit on Codex CLI drives builder+artisan?+vitrine?+judge+radar+voyager?) → Ship (guardian+launch)`

Read: `reference/apex-recipe.md`, `reference/apex-walkthrough.md`.

---

## essential

Must-have feature **verdict + conditional implementation**. Converges on THE ONE feature without which the product cannot exist. Subtraction-oriented (MVP, core feature, scope reduction).

**Chain template:**
`Plea → Spark → Magi → Rank → AskUserQuestion[Y/N/Modify] → if Y: Sherpa → Builder[codex] → Radar[codex] → Guardian`

Full sequential funnel + verdict + conditional implementation → `reference/inline-recipes.md`.

---

## killer

Killer-feature **verdict + conditional implementation with feature flag**. Converges on THE ONE decisive differentiator via cross-engine triangulation. Default baseline: **Claude + Codex (dual-engine)** — perspective diversity via different prompt frames + WebSearch tool usage. agy optional third axis when AVAILABLE. Addition-and-leap-oriented.

**Chain template:**
`(Compete[claude+WebSearch] ‖ Flux[claude reframe] ‖ Plea[claude empathy] [+ Compete-agy / Flux-agy if AVAILABLE]) → Spark → Magi → AskUserQuestion[Y/N/Modify] → if Y: Sherpa → (Forge[codex] if UI) → Artisan/Builder[codex] → Radar[codex] → judge[multi-engine] → Guardian + flag`

Full cross-engine triangulation + verdict + flagged implementation → `reference/inline-recipes.md`.

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

## transmute

**Cross-language rewrite** preserving behavior (TS→Rust, Go→Rust, Python→Go, JS→TS, …). Idiomatic re-expression verified by **differential parity** against golden oracle. Distinct from `PORTING` / `shift` (same-language migration / native-API modernization) / `refactor`. Strategy: big-bang ‖ strangler-fig ‖ FFI-incremental. 8-20 agents. **Confirm before big-bang.**

**Chain template:**
`Phase 0 Framing → 1 Archaeology (Trail [static-rules + history] ‖ Lens ‖ Atlas?) → 2 Contract (Accord → Mint golden oracle) → 3 Strategy (Magi risk gate + Transmutation Map) → 4 Transmute (Builder/Artisan +grok?+gateway/schema?; rally engine-paradigm COMPETE for high-risk) → 5 Parity Verify (Radar differential ‖ Attest conformance ‖ judge ‖ Voyager?) → 6 Ship (Guardian)`

Read: `reference/transmute-recipe.md`.

---

## package (includes legacy `venture` as `domain=startup`)

**Generalized document-package generator** — **12-domain preset registry**: `startup` (the legacy `venture` blueprint) / generic / research / ai-adoption / legal* / saas / media / growth / career / learning / hiring* / local-gov*. Per-domain swap: directories, role→skill map, traceability anchor (F-/H-/UC-/R-/P-/E-/T-/LO-/I-), risk gates (*=mandatory). Single Phase 0-6 engine. Depth 5-28 agents (`startup` tiers: lite 6-8, mvp(default) 14-18, raise 16-20, full 24-28). **Confirm full depth.**

**Chain template:**
`Phase 0 Framing (preset auto-detect + risk-flag) → 1 Research (preset skills; deep-research for research preset) → 2 Spine [BARRIER: entity-id per anchor] → 3 Parallel Doc Tracks (preset map, waves) → 4 Synthesis → 5 Validate (attest/judge + risk gate + manifest + report + README) → 6 Package`

**`startup` preset chain (legacy `venture` form):**
`Phase 0 → 1 Research (field+compete ‖ plea+cast) → 2 Product Spine [BARRIER: F-001 + MoSCoW] (accord+spark+rank+pulse+void?) → 3 Parallel Doc Tracks, feature_id-bound (Brand / UX / LP / Mktg / Tech / AI / Legal / Test / PM / Mock / Assets) → 4 Overview synthesis → 5 Validate → 6 Package (UTF-8 + zip + lint + unzip test + PII scrub)`

Read: `reference/package-recipe.md`. Startup-preset deep blueprint: `reference/venture-recipe.md`.
