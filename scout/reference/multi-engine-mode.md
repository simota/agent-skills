# Multi-Engine Mode (Scout)

Detailed reference for the `multi` Recipe. Top-level mechanics summary lives in `SKILL.md §Multi-Engine Mode`; full tri-engine algorithm in `reference/tri-engine-investigate.md`; cross-skill protocol in `_common/MULTI_ENGINE_RECIPE.md`.

## Activation

- Explicit `multi` subcommand.
- Any explicit user request for parallel investigation / cross-engine root cause comparison / consensus RCA.
- Auto-promoted from default `bug` Recipe when 3 hypotheses stall without progress.

Goal: break single-engine hypothesis lock-in by fanning out across AVAILABLE engines with non-overlapping training-data priors; synthesize a Primary RCA backed by consensus plus Alternative Hypotheses preserved from divergence.

## Base Engine Policy (2026-05)

Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT.

For Scout: dual-engine baseline (Codex sandbox-execution priors + Claude judgment) breaks the most common hypothesis lock-in cases; agy adds whole-codebase 1M-context investigation when reachable.

Pattern H scoring under dual-engine: Primary = 2/2 CONFIRMED; Alternative = 1/2 grounded; LIKELY unreachable.

See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

## Pattern Type: H (Hybrid)

Both axes carry value. Concurrence raises confidence on the primary root cause; divergence preserves alternative hypotheses as pre-grounded verification branches for Builder.

## Core Mechanics

- Spawn one Agent subagent per AVAILABLE engine in a single message: `investigate-codex` + `investigate-claude` (dual-engine baseline); add `investigate-agy` (tri-engine) when AVAILABLE. Per `reference/tri-engine-investigate.md`.
- Run engine availability PREFLIGHT in Scout main context — never delegate detection to subagents (subagent PATH is narrower; see `_common/MULTI_ENGINE_RECIPE.md §2`).
- Use loose prompts (Role + Symptom evidence + Reproduction state + Ruled-out hypotheses + Output format only). Do NOT pass 5-Whys templates, Fishbone categories, Causal Graph rules, or Scout's confidence rubric — apply RCA frameworks at SYNTHESIZE, not at FAN-OUT. Each engine's training-data priors should drive root cause hypothesis diversity.
- Subagents return structured JSON with 1-3 hypotheses each (symptom, root-cause-hypothesis, causal-chain, evidence, reproduction-steps, affected-areas, severity, confidence, rca_method, ruled_out); main context integrates via NORMALIZE → CLUSTER → SCORE → GROUND → SYNTHESIZE.

## CLUSTER Rule (Scout-Specific)

Group by **root cause hypothesis identity**, NOT by symptom. Engines always agree on the symptom; they may diverge on the root cause — that divergence is exactly what Pattern H preserves.

Same root cause class + same primary affected component + same causal-chain shape = same cluster. Different layers (app vs lib vs infra), different mechanisms (logic vs race vs resource), or different ultimate fix locations = different clusters.

## Confidence Axis (Per-Cluster)

- `CONFIRMED` (3/3) — high confidence in root cause; spot-check at GROUND.
- `LIKELY` (2/3) — strong; note what the missing engine surfaced instead — that often becomes an alternative hypothesis.
- `CANDIDATE` (1/3) — must pass GROUND to ship as Primary or Alternative.

## Perspective Axis (Cross-Cluster)

- `CONVERGENT` — all surviving clusters reduce to one root cause class; ship a single high-confidence RCA.
- `DIVERGENT-N` — N ≥ 2 surviving clusters reflect genuinely different root cause hypotheses. Primary RCA = top-ranked cluster. Remaining N-1 ship as Alternative Hypotheses with verification ordering.
- **A `DIVERGENT` result is not a failure of multi mode — it is the precise signal multi-engine investigation is designed to produce.**

## GROUND Protocol (Scout Main Context, Never Delegated)

- Read every cited `affected_areas` and `causal_chain` step location with the Read tool.
- Reject clusters with hallucinated code paths, broken causal chains, or upstream-mitigated failures.
- Attempt reproduction using each cluster's `reproduction_steps` when tractable; `VERIFIED` = code + repro both pass, `LIKELY-VERIFIED` = code passes + repro inconclusive.
- Never ship a Primary RCA without at least one `VERIFIED` cluster (use `INVESTIGATE-FURTHER` Fix Prompt verb if only `LIKELY-VERIFIED` clusters survive).

## SYNTHESIZE — Primary + Alternative with Verification Ordering

- Primary RCA ships with full investigation report shape (per `reference/output-format.md`), confidence and perspective tags, and an LLM Fix Prompt block (suppressed if Primary is only `LIKELY-VERIFIED`).
- Alternative Hypotheses ship as separate blocks, each with root cause hypothesis, causal chain, evidence, suggested verification step, and engine-attribution tag.
- Explicit `## Verification Order` block instructs Builder: try Primary first; if symptom persists after Primary fix, verify Alternative #1 by [step]; etc. This eliminates the "fix didn't work, re-investigate from scratch" cycle.

## Engine-Attribution + Perspective Tags (Mandatory)

- 3/3: `[codex+agy+claude]` + `[CONVERGENT]` (if also the only surviving cluster)
- 2/3: `[codex+agy]` etc. + `[CONVERGENT]` or `[DIVERGENT-N → primary/alt-i]`
- 1/3 grounded: `[codex-verified]` / `[agy-verified]` / `[claude-verified]` + `[DIVERGENT-N → alt-i]`

## Degraded Modes

- 1 engine down → continue with 2 (clusters capped at `LIKELY`).
- 2 down → single-engine RCA, every hypothesis is `CANDIDATE`, Alternative Hypotheses section omitted.
- All 3 down → degrade to default `bug` Recipe.
