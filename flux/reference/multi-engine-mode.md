# Multi-Engine Mode (SKILL.md detail)

Detailed prose for the Multi-Engine Mode section of `flux/SKILL.md`. The SKILL.md retains a short summary; this file holds the full rationale, mechanics, scoring tables, GROUND categories, and degraded-mode rules.

For algorithm, JSON schema, prompt skeletons, and step-by-step flow, see `tri-engine-reframe.md`. For the cross-skill Pattern D protocol, see `_common/MULTI_ENGINE_RECIPE.md`.

---

## When to activate

Activated by the `multi` Recipe (or any explicit user request for parallel reframing / cross-engine perspective comparison). Multi-engine reframe generation follows Pattern D (Divergence-primary) per `_common/MULTI_ENGINE_RECIPE.md` — but Flux pushes the pattern further than Spark or Plea because **divergent reframes are the literal product**, not a side effect.

## Base Engine Policy (2026-05)

Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. For Flux specifically, agy's Deep Think mode and 1M-context cross-domain analogy generation make the tri-engine uplift **larger than for other Pattern D skills** — but dual-engine (Claude's broad-domain reasoning + Codex's GitHub-priors as alternative-domain analogy source) still produces meaningful divergence and is the default. When agy is UNAVAILABLE, compensate by explicitly framing each Claude branch with a different reframing technique (Bisociation / SCAMPER / TRIZ inversion / Oblique Strategies) to widen prompt-frame diversity. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

## Why multiple engines for reframing

Vertical reasoning reinforces existing thought structures (de Bono). A single engine — no matter how capable — is structurally bounded by its training-data prior and can only produce inversions consistent with that prior. Multiple independent engines (Codex/GitHub-heavy, Claude/Anthropic-curated baseline; Antigravity/Google-product-heavy when AVAILABLE) each apply *their own* implicit prior to the same problem, producing reframes that no single engine can reach alone. The breakthrough perspective shift almost always comes from the engine the others could not duplicate.

## Core mechanics

- Spawn one Agent subagent per AVAILABLE engine in a single message: `reframe-codex` + `reframe-claude` (dual-engine baseline); add `reframe-agy` (tri-engine) when AVAILABLE. Per `tri-engine-reframe.md`.
- Run engine availability PREFLIGHT in Flux main context — never delegate detection to subagents (subagent PATH is narrower).
- Use loose prompts (Role + Target + Output format only). Do NOT pass framework names (Bisociation, SCAMPER, TRIZ, Oblique Strategies), Cynefin classification rules, or ASN-test criteria to subagents — apply those at SYNTHESIZE. Each engine's training-data prior must drive divergence freely.
- Subagents return structured JSON; main context integrates via NORMALIZE → CLUSTER → SCORE → GROUND → SYNTHESIZE.

## Two-axis scoring (Flux-specific structure)

| Axis | Labels | Notes |
|------|--------|-------|
| Concurrence | `UNIVERSAL` (3/3), `LIKELY` (2/3), `VERIFIED-DIVERGENT` (1/3 after grounding) | How many engines reached the reframe |
| Novelty | `HIGH`, `MEDIUM`, `LOW` (drop) | How much new action surface the reframe opens vs. the original framing |

**Critical Flux rule (does NOT exist in Spark, opposite of Judge): `VERIFIED-DIVERGENT × HIGH` reframes occupy the top section of the Portfolio output, ahead of `UNIVERSAL` reframes.** Flux's entire premise is that breakthrough perspective shifts come from outside the consensus prior; multi-engine reframing makes that operational by treating single-engine divergence as a feature, not a defect.

## CLUSTER difference from Spark

Two reframes targeting the same `original_assumption` but with different `inverted_form` are kept as **separate clusters** under a shared `assumption_root` heading — not merged. A single assumption can be inverted along multiple axes (negation / scale-shift / time-shift / observer-shift); collapsing them destroys divergent value.

## Merge strategy: Portfolio-only by default

Compete merge — choosing "the best reframe" — recreates the consensus prior the user came to Flux to escape. `multi --compete` is offered only on explicit request and even then alternatives are preserved in an appendix, because the "second-best" reframe often becomes the breakthrough once the user encounters the problem in a new context.

## Engine-attribution tag (mandatory on every shipped reframe)

`[codex+agy+claude]` (3/3) / `[codex+agy]` etc. (2/3) / `[codex-verified]` (1/3 verified-divergent). For DIVERGENT reframes, append a second tag explaining *why divergence is informative here*: `[divergent: cross-domain-prior]`, `[divergent: scale-shift-prior]`, `[divergent: contrarian-prior]`.

## GROUND checks (Flux main context, never delegated)

ASN test (Actionability / Specificity / Novelty), hallucinated-domain check (cross-domain analogies plausible to an expert), synonym-substitution check, bias-blind-spot check (does the reframe inherit the same bias as the original framing?).

Rejection categories: `REJECTED-ASN`, `REJECTED-HALLUCINATION`, `REJECTED-SYNONYM`, `REJECTED-BIAS-INHERITED`.

## Degraded modes

- 1 engine down → continue with 2.
- 2 down → single-engine fallback with stricter ASN/bias-blind-spot grounding; flag that divergence-value is severely reduced (recommend falling back to standard `reframe` Recipe).
- All down → degrade to standard `reframe` Recipe (DEEP pipeline).
