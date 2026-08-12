# Nexus Reference Index

Full Read-When index for every `reference/` and `_common/` file Nexus consults. `SKILL.md` § Reference Map carries only the always-hot rows and points here for the rest.

Read only the files that match the current decision point. Files already indexed by the Workflow table's Read-When column (routing-matrix, agent-chains, confidence-scoring, execution-phases, guardrails, error-handling, output-formats, the anti-pattern catalogs) are not repeated here — the Workflow row is their index.

| File | Read When |
|------|-----------|
| `reference/recipes-index.md` | **The complete Recipes table** — a subcommand matched at Dispatch and you need its chain template + `Read` reference, or you are scanning the registry |
| `reference/<recipe>-recipe.md`, `reference/apex-walkthrough.md` | Per-Recipe phase contracts, chain templates, cost profiles (+ apex Mermaid walkthroughs); filename = the `Read` column of `recipes-index.md` |
| `reference/recipes-detail.md` · `reference/inline-recipes.md` · `reference/recipe-contract.md` | Recipe Families axis prose · full contracts for `kaizen`/`essential`/`killer`/`trim` · authoring or normalizing a recipe (8 required elements) |
| `reference/quell-recipe.md` | `/nexus quell` — review-to-zero fix loop: Finding Ledger, disposition integrity, oscillation detection, termination bounds, `profile=general\|refactor` |
| `reference/signal-keywords.md` · `reference/routing-explanation.md` · `reference/task-battery.md` | Canonical Signal Keywords table · explaining why a chain was chosen · verifying a routing-machinery change before merge |
| `reference/proactive-mode.md` · `reference/pack-subcommand.md` · `_common/SKILL_PACKS.md` | `/Nexus` no-task next-action recommendations · `/nexus pack` profile switch (settings.json edit, backup, diff, confirm) · pack membership matrix and profile catalog |
| **Hub authoring (per engine)** — `reference/hub-authoring.md`, `_common/OPUS_5_AUTHORING.md`, `_common/CODEX_ORCHESTRATION.md`, `_common/AGY_ORCHESTRATION.md` | Per-engine authoring, spawn-template variants, model selection, execution-layer key rules, Fable 5 F-principles · Claude Code P1-P12 · Codex C1-C6 · agy A1-A6 |
| `reference/execution-layers.md` · `reference/adaptive-prompt-policy.md` · `reference/context-strategy.md` | Per-CLI prereqs, runtime notes, agy headless mitigations + template · tailoring each spawn prompt to project + session · how context flows between agents |
| **Loop discipline** — `_common/LOOP_PRECONDITIONS.md`, `reference/evaluator-loop-protocol.md`, `reference/loop-engineering-primitives.md` | The five-point gate before **any** agent loop (completion oracle · hard-stop bound · maker ≠ checker · persistent memory · drift awareness) · Generator-Evaluator separation that `converge` executes · mapping a loop onto per-CLI primitives |
| `_common/PARALLEL.md` | Parallel branch definitions, file ownership, merge, rollback |
| **Shared verdict/parity/refutation contracts** — `reference/verdict-gate.md`, `_common/DIFFERENTIAL_PARITY.md`, `_common/ADVERSARIAL_REFUTATION.md` | Verdict recipes (`essential`/`killer`/`trim` + graft flag) · parity discipline where a recipe claims "verified by differential parity" · skeptic-panel discipline where a verdict gates on "refute ×2-3" |
| `reference/dialogue-protocol.md` · `reference/doc-quality-protocol.md` · `reference/research-grounding.md` | Contract-level dialogue (`spec`/`delve` mandatory, `gedanken` INTERACTIVE, `clone` Stack Dialogue) · document deliverables — reader contract, grounding, Doc Quality Gate · web-research sweep + Evidence Ledger |
| `_common/PROOF_CARRYING.md` · `_common/GROWTH_BRAND_PROOF.md` | `/nexus acceptance` Tier policy + G1-G10 — **mandatory before `acceptance`** · `layer=c` (alias `growth-acceptance`) Layer C + Insight Ledger + Brand Compiler + G11-G15 |
| `_common/PROPORTION_AND_SPACING.md` · `_common/IMAGE_INPUT.md` | A design-recipe rubric axis needs a defensible sourced number · the routing request carries an image (five-stage pipeline at CLASSIFY; screenshot-driven chains add the Visual Fix Loop at VERIFY) |
| `reference/official-skill-categories.md` · `reference/managed-agents-mapping.md` | Official use-case categories + 5 canonical patterns · Managed Agents / Outcomes / Dreaming / Webhooks mapping + Dynamic Workflows |
| `reference/autorun-schema.md` | Emitting the AUTORUN `_STEP_COMPLETE` block — Nexus-specific Output/Next schema |

