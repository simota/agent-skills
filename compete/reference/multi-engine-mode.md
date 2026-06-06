# Multi-Engine Mode — Operational Detail

Pattern D Divergence-primary detail for the `multi` Recipe. SKILL.md keeps the activation gist; this file holds the engine-bias rationale, scoring semantics, artifact-merge rules, and degraded-mode matrix.

> See also: `reference/tri-engine-compete.md` (full algorithm, JSON schema, CLUSTER identity rules, subagent prompts) and `_common/MULTI_ENGINE_RECIPE.md` (cross-skill protocol).

## Base Engine Policy (2026-05)

Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. dual-engine is NOT degraded — but for Compete specifically, the third engine's coverage uplift is **larger than for other Pattern D skills** because agy's Google-product / APAC bias patches a structural blind-spot that Claude + Codex share (both under-index large-cap APAC enterprise SaaS).

When agy is UNAVAILABLE, surface this coverage gap explicitly in the Uncommon-Competitors callout and recommend a manual WebSearch sweep for APAC + enterprise segments. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

## Why Multiple Engines for Compete

- **Codex** (GitHub-heavy / OSS / dev tools / indie SaaS) under-indexes large-cap enterprise SaaS and consumer brands.
- **Antigravity (agy)** (Google product / large-cap SaaS / APAC enterprise) under-indexes OSS / indie tools and AI-native startups.
- **Claude** (Anthropic-curated / diverse industries / regulated verticals / AI-native players) under-indexes regional Asia-Pacific players and certain dev-infra niches.

Each engine has structural training-data blind-spots that are **knowable** (we can predict which segments it under-indexes) but **invisible to that engine alone**. Multi-engine fan-out is the only practical way to patch these blind-spots — dual-engine covers two of the three blind-spot axes (codex/claude), tri-engine adds the third (agy).

## Core Mechanics

- Spawn one Agent subagent per AVAILABLE engine in a single message: `compete-codex` + `compete-claude` (dual baseline); add `compete-agy` (tri) when AVAILABLE.
- Run engine availability PREFLIGHT in Compete main context — never delegate detection to subagents (subagent PATH is narrower; see `_common/MULTI_ENGINE_RECIPE.md §PREFLIGHT`).
- Use loose prompts (Role + Target + Output format only). Do NOT pass SWOT templates, 7 Powers rubrics, positioning-map axes, or analysis-template structures to subagents — apply framework rules in SYNTHESIZE, not at FAN-OUT.
- Subagents return structured JSON: `name/aliases/category/positioning/segment/geography/features/strengths/weaknesses/pricing_posture/evidence_sources/source_engine_bias_note`.
- Main context integrates via NORMALIZE → CLUSTER (alias-aware) → SCORE (coverage matrix) → GROUND (WebSearch-mandatory) → SYNTHESIZE → DELIVER.

## Coverage Matrix Scoring (Pattern D, Divergence-Primary)

- `UNIVERSAL` (3/3) — mainstream competitor every engine surfaced. Safe assumption the buying committee knows them. Check for duplication with user's seed list.
- `LIKELY` (2/3) — strong competitor with one blind-spot engine. The missing engine's absence is itself a signal about which segment it under-indexes.
- `VERIFIED-DIVERGENT` (1/3, grounded via WebSearch) — uncommon competitor only one engine surfaced. **Not lower-value than UNIVERSAL** — frequently the breakthrough finding patching "we keep losing deals to someone we cannot name".

## Artifact-Driven Merge

The user's requested artifact (Feature Matrix / Battle Card / Positioning Map / SWOT / Landscape / LLM Visibility) determines output shape. Engine-concurrence tags are **woven into** the artifact, not produced as a separate document. See `reference/tri-engine-compete.md §SYNTHESIZE` for per-artifact integration patterns.

## Mandatory Deliverable — Uncommon Competitors Callout

Every `multi` output must include a dedicated section listing each `VERIFIED-DIVERGENT` competitor with: name, surfacing engine, training-data bias hypothesis (why others missed it), structural blind-spot patched, evidence URL, recommended action. **Never omit** — single most valuable output of tri-engine Compete.

## Engine-Attribution Tag (Mandatory)

`[codex+agy+claude]` (3/3 UNIVERSAL) / `[codex+agy]` etc. (2/3 LIKELY) / `[codex-verified]` / `[agy-verified]` / `[claude-verified]` (1/3 VERIFIED-DIVERGENT).

## WebSearch at GROUND

Mandatory. Never ship a VERIFIED-DIVERGENT competitor based on training knowledge alone. Compete's Core Contract (unsourced claims forbidden) applies with extra force.

## Degraded Modes

| Failure | Action |
|---|---|
| 1 engine down | Continue with 2, note reduced coverage |
| 2 engines down | Single-engine fallback with stricter grounding; disable Uncommon-Competitors callout |
| All engines down | Degrade to default `matrix` Recipe |
| WebSearch unavailable | Mark CANDIDATE clusters as `NEEDS-INFO`; do not ship as VERIFIED-DIVERGENT |
