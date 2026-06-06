# Inline Recipes — `kaizen` / `essential` / `killer`

**Purpose:** Full phase contracts for the three Recipes that have no separate reference file. SKILL.md `## Subcommand Dispatch` keeps only a summary; this file holds the complete contracts.

**Read when:** Executing one of `kaizen`, `essential`, or `killer` Recipes.

---

## `kaizen` — Multi-axis improvement of an existing feature

- **Phase 1 DIAGNOSE (parallel)** — Lens[map-current-implementation] unconditionally; conditionally add Pulse[KPI-measure] if metrics instrumentation exists, Echo[UX-walkthrough] if UI surface, Voice[sentiment]/Trace[session-replay] if user-feedback or session data is available. Goal: multi-signal picture of how the feature behaves and where it falls short.
- **Phase 2 PROPOSE (sequential)** — Spark[improvement-spec, **constrained to enhancing existing data/logic** — not new feature ideation] → Magi[axis-prioritize] selects **one or two** axes from `{perf, UX, code-quality, feature-extension}`; rejects "improve everything" plans because kaizen is iterative and scope-bounded.
- **Phase 3 IMPROVE (axis-bounded, parallel within axis)** — perf → Bolt[frontend]/Tuner[explain]; UX → Palette[usability]/Prose[microcopy]/Flow[motion]; code-quality → Zen[refactor]/Sweep[dead-code]; feature-extension → Artisan[component]/Builder[api]. Independent sub-axes parallel; dependent ones serialize.
- **Phase 4 VERIFY** — Radar[regression] gates non-regression on existing behavior; if Pulse/Echo ran in Phase 1, re-run them for Before/After comparison.
- **Phase 5 SHIP** — Guardian[PR-prep] produces PR with embedded Before/After report.
- **Boundaries**: vs `refactor` (internal-only, no external delta) — kaizen explicitly improves externally-observable quality alongside internal hygiene. vs `optimize` (perf-only) — kaizen treats perf as one axis. vs `feature` (new capability) — kaizen polishes a shipped feature.
- **Anti-patterns prevented**: (1) "rewrite the whole module under improvement banner" (Magi's axis-cap forces scope discipline), (2) "improve without measuring" (Phase 1 diagnostics mandatory), (3) "improvement that regresses something else" (Phase 4 Radar + re-measure).
- **Add-ons**: +Scout for deeper root-cause when Lens insufficient, +Atlas for structural change, +Ripple for cross-module impact before committing to an axis.

---

## `essential` — Single must-have verdict + conditional implementation

- **Phase 1-4 Verdict (sequential refinement funnel)** — Plea[claude pain-extraction] → Spark[claude spec] → Magi[claude necessity-arbitration] → Rank[claude MoSCoW-must]. Each step narrows the previous output; parallelization would force redundant re-synthesis. Subtraction-oriented — Magi's Sophia filters "Should-have" posing as "Must-have".
- **Convergence rule**: Rank's MoSCoW output filtered to **the single top Must-have** (highest necessity score). Tie-break: defer to Magi's Sophia; still tied → escalate to user via AskUserQuestion with tied candidates.
- **Phase 5 DELIVER verdict via AskUserQuestion** — card format: `## Essential Verdict / Recommended must-have: <single feature> / Why: <2-3 lines> / Source of conviction: Plea→Spark→Magi→Rank summary / Considered but rejected: <2-3 alternatives, one-line reasons> / → Build this? [Yes / No / Modify]`.
- **Phase 6 Conditional Implementation (only if Yes)**: Sherpa[claude atomic-decomposition] → Builder[codex] → Radar[codex] → Guardian[claude] → DELIVER working feature + tests + PR. Engine routing follows summit principles (Codex owns code-gen, Claude owns judgment).
- **If No**: DELIVER verdict artifact as "decided-not-to-build" record; do not run Phase 6.
- **If Modify**: capture user input (what to change), loop back to Phase 1 with the modification as additional constraint.
- **Failure mode prevented**: over-engineering (Phase 1-5) + unbounded implementation scope (Phase 6 inherits the single-feature constraint).
- **Add-ons**: +Void for aggressive scope cut, +Accord for atomic-unit specs in Phase 1-4.

---

## `killer` — Single differentiator verdict + conditional flagged implementation

- **Phase 1 (parallel hub-spoke, cross-engine triangulation, dual-engine baseline)** — Default baseline distributes Phase 1 branches across **both Claude and Codex** to preserve perspective independence at the model-priors level (not just prompt-frame level): Compete[**claude** + WebSearch tool for current market gap-analysis, framed as "industry analyst"] ‖ Flux[**codex** sandbox-execution priors, framed as "what would the market gap look like in code / infrastructure / developer-experience terms" — Codex's GitHub-heavy training surfaces gaps a market-focused model misses] ‖ Plea[**claude** empathy/latent-needs, framed as "user advocate"]. **Optional agy lift (when AVAILABLE at PREFLIGHT)**: Compete adds a second branch on agy (Search-grounded for fresher market data than Claude's training cutoff), Flux adds a second branch on agy (Deep Think mode for cross-domain analogy generation) — agy's training-data priors give an additional independence axis. Failure mode prevented: model-monoculture in the triangulation step. Engine-attribution tags: `[claude-compete]`, `[codex-flux]`, `[claude-plea]` for the dual-engine baseline; add `[agy-search]`, `[agy-deepthink]` when the optional lift is active.
- **Phase 2 (sequential synthesis)** — Spark[claude] aggregates the independent perspectives into **the single most decisive killer feature** → Magi[claude] binary Go/No-Go.
- **Convergence rule**: Spark MUST synthesize one feature (not a ranked list); Magi delivers binary Go/No-Go. Tie-break: Magi forces selection via strategic-impact criterion (market timing × differentiation depth × feasibility); NO-GO still surfaces runner-up with "weakest-link" annotation.
- **Phase 4 DELIVER verdict via AskUserQuestion** — card with perspective-attributed evidence (mark which frame produced which insight; note which branches were agy-backed vs Claude-frame-only) + Magi verdict (GO confidence H/M/L | NO-GO reason) → Ship this? [Yes / No / Modify].
- **Phase 5 Conditional Implementation (only if Yes)**: Sherpa[claude decomposition] → if `ui_dimension != none`: Forge[codex prototype-validation] → Artisan[codex frontend-production] → Builder[codex backend/logic] → Radar[codex edge cases for differentiator] → judge[claude multi-engine review — killer features are high-stakes] → Guardian[claude] **with feature-flag recommendation** for controlled rollout (differentiation risk) → DELIVER working feature + tests + PR + flag config + rollout plan.
- **If No**: DELIVER "decided-not-to-ship" strategic record.
- **If Modify**: loop back to Phase 1 with modification (e.g., "reframe around X constraint" → Flux re-runs with updated directive).
- **Add-ons**: +Riff for iterative deep-dive on Spark output in Phase 2, +Field for additional market trend grounding in Phase 1.

---

## Visualizations

Mermaid flow diagrams (render via mermaid.live or compatible viewer):
- [`essential-recipe-flow.mmd`](essential-recipe-flow.mmd) — verdict funnel + conditional impl branch
- [`killer-recipe-flow.mmd`](killer-recipe-flow.mmd) — cross-engine triangulation topology
