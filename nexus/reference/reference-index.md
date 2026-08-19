# Nexus Decision-Point Reference Index

This is a progressive-disclosure index for Nexus decision points, not a file manifest. `SKILL.md` § Workflow owns always-hot references; `recipes-index.md` owns the exact Recipe registry. Read only the group that matches the current decision.

When product versions, model names, CLI flags, or availability differ between a Nexus reference and `_common/CLI_COMPATIBILITY.md`, the `_common` file is authoritative and current official documentation must be checked before execution.

| Decision point | Read |
|----------------|------|
| Recipe matched | `reference/recipes-index.md` → the row's exact `Read` files; family distinctions → `reference/recipes-detail.md`; inline contracts → `reference/inline-recipes.md`; authoring contract → `reference/recipe-contract.md` |
| Product/MVP delivery | `reference/deliver-recipe.md`; scope evidence → `reference/delivery-decision-matrix.md`; recovery → `reference/delivery-anti-stall-engine.md`; exit validation → `reference/delivery-exit-criteria-validation.md` |
| Intent/routing | `reference/signal-keywords.md`, `reference/intent-clarification.md`, `reference/confidence-scoring.md`, `reference/routing-matrix.md`, `reference/task-battery.md` |
| Proactive/profile invocation | `reference/proactive-mode.md`, `reference/pack-subcommand.md`, `_common/SKILL_PACKS.md` |
| Hub authoring/runtime | `reference/hub-authoring.md`, `reference/execution-layers.md`, `reference/adaptive-prompt-policy.md`, `reference/context-strategy.md`, `_common/CLI_COMPATIBILITY.md` |
| Engine-specific spawn authoring | `_common/OPUS_5_AUTHORING.md`, `_common/CODEX_ORCHESTRATION.md`, `_common/AGY_ORCHESTRATION.md` |
| Execution shape and structural rejection | `reference/orchestration-patterns.md`, `reference/routing-matrix.md` § Chain Design Rejection Rules, `_common/PARALLEL.md` |
| Handoff/merge | `_common/HANDOFF.md`, `reference/handoff-validation.md`, `reference/conflict-resolution.md` |
| Error/recovery | `reference/error-handling.md`, `reference/guardrails.md` |
| Loop entry | `_common/LOOP_PRECONDITIONS.md`, `_common/FINDING_LEDGER.md`, `reference/evaluator-loop-protocol.md`, `reference/loop-engineering-primitives.md` |
| Verification depth | `_common/EVIDENCE_LADDER.md`, `_common/PROOF_CARRYING.md`, `_common/GROWTH_BRAND_PROOF.md`, `_common/ADVERSARIAL_REFUTATION.md` |
| Verdict/parity | `reference/verdict-gate.md`, `_common/DIFFERENTIAL_PARITY.md` |
| Dialogue/doc/research | `reference/dialogue-protocol.md`, `reference/doc-quality-protocol.md`, `reference/research-grounding.md` |
| Image/design numeric evidence | `_common/IMAGE_INPUT.md`, `_common/PROPORTION_AND_SPACING.md` |
| Harness failure/debt | `_common/HARNESS_DEBT.md` |
| AUTORUN envelope | `reference/autorun-schema.md` |

Per-Recipe files are never loaded by glob. Resolve the selected row in `recipes-index.md` and load only its declared `Read` files.
