# Multi-Engine Design Direction

Shared engine selection, capability/authorization gates, dispatch, capture, attribution and degraded-mode policy: `_common/MULTI_ENGINE_RECIPE.md` and `_common/CLI_COMPATIBILITY.md`. This reference defines only the domain payload and integration rules.

Default flow for `/vision multi`. Run subagents in parallel — one per AVAILABLE engine — to generate **divergent UX/design directions** for the same brief, integrate results across two axes (concurrence + divergence), and deliver a **Portfolio of complementary directions** that the user selects between before downstream handoff to Muse / Palette / Flow / Forge.

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE (spectrum coverage) → GROUND (brand/persona/a11y) → SYNTHESIZE (Portfolio-only) → DELIVER
```

### 1. SCOPE

Define the design brief once. All selected subagents share the same scope:

- Operating mode (`REDESIGN` / `NEW_PRODUCT` / `TREND_APPLICATION` / `LINEAR_RESTRAINT` / `SPATIAL` / `AI_INTERFACE`)
- Product surface (marketing site / SaaS dashboard / mobile app / spatial / AI agent UI)
- Brand anchor (existing palette, typography, voice keywords, anti-keywords — if any)
- Persona target (primary persona from Cast registry if available)
- Business outcome anchor (conversion lift / task-success / retention / brand repositioning)
- Constraints (WCAG 2.2 AA mandatory, brand identity locks, technical platform limits)
- Forbidden directions (explicit anti-patterns or off-brand aesthetics)

Do NOT include the design-trend taxonomy, principle vocabulary, or aesthetic spectrum in the SCOPE — those apply during SYNTHESIZE. Let each engine reach for its own training-data priors.

### 2. PREFLIGHT — engine availability (Vision main context, never delegated)

Use the canonical probe from `_common/MULTI_ENGINE_RECIPE.md §2`. Probe `codex`, `agy`, and `claude` binaries with fallback paths. Apply the strict availability verdict matrix unchanged.

### 3. FAN-OUT — parallel subagents

Dispatch one independent task per selected, authorized engine using the shared CLI adapter for genuine parallel execution. Each subagent has independent context and generates **2–3 design directions** for the brief.

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `direction-codex` | Codex CLI | Authorized invocation via `_common/CLI_COMPATIBILITY.md` |
| `direction-agy` | Antigravity CLI | Authorized headless/native dispatch → `_common/CLI_COMPATIBILITY.md` §9; validate outputs under `_common/MULTI_ENGINE_RECIPE.md` §3.5 |
| `direction-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule** (per `_common/SUBAGENT.md` MULTI_ENGINE): pass only Role + Target + Output format. Do NOT pass the V.A.I.R.E. rubric, 2026 trend taxonomy, design-system anti-patterns, or aesthetic vocabulary lists. Vision main context applies framework rules at SYNTHESIZE.

#### Required JSON output schema

```json
{
  "engine": "codex|agy|claude",
  "directions": [
    {
      "concept_name": "Short evocative concept name (e.g., 'Quiet Industrial', 'Liquid Confidence')",
      "principles": [
        "3–5 design principles that govern this direction (each one short, declarative, testable)"
      ],
      "aesthetic_language": {
        "spectrum_position": "modernist | skeuomorphic | maximalist | minimalist | brutalist | expressive | calm | spatial | retro-futurist",
        "color_strategy": "Palette logic — saturation/temperature/contrast posture",
        "typography_strategy": "Display + body pairing, weight contrast, variable-font usage if any",
        "surface_treatment": "Flat / layered / glass / depth-token strategy",
        "imagery_strategy": "Photography vs illustration vs 3D vs generative — and tone"
      },
      "interaction_language": {
        "motion_posture": "Restrained | playful | physical | cinematic — and reason",
        "feedback_pattern": "How the system signals state changes",
        "input_modality_priority": "Pointer / touch / voice / gaze — ranked",
        "ai_disclosure_pattern": "If AI-interface: how the system shows reasoning / control / undo (required for AI_INTERFACE mode)"
      },
      "reference_style_influences": [
        "Concrete references — products, art movements, brands, OS design languages (e.g., 'Linear app restraint', 'Material 3 Expressive', 'Apple Liquid Glass', 'Swiss editorial')"
      ],
      "persona_fit": "Why this direction serves the named persona's emotional and functional needs",
      "business_outcome_link": "Which target metric this direction is hypothesized to move and how (e.g., 'Restraint reduces decision fatigue → time-on-task -15%')",
      "risk_areas": [
        "Where this direction breaks (brand drift, a11y, novelty cost, AI-trust)"
      ],
      "downstream_handoff_hint": {
        "muse": "Token themes to define (color, spacing, motion, depth)",
        "palette": "Interaction polish priorities (focus rings, hover, dead-state coverage)",
        "flow": "Motion choreography keywords",
        "forge": "Which surface to prototype first to de-risk this direction"
      }
    }
  ],
  "engine_notes": "Optional: what aesthetic bias this engine knows it brings"
}
```

If an engine returns free-form Markdown, ask its subagent to re-emit as JSON before integrating.

### 4. NORMALIZE

Parse the usable JSON outputs into a unified direction list. Tag each direction with its source engine. Preserve per-engine wording — different phrasings of the same `aesthetic_language` may reveal different angles on the same concept.

### 5. CLUSTER — same direction across engines

Group directions that share **the same design concept expressed in different vocabularies**. Two directions match when **all of**:

- Same `spectrum_position` (or two adjacent spectrum positions — e.g., `minimalist` + `calm` may cluster; `brutalist` + `calm` will not)
- Same `motion_posture` class (restrained / playful / physical / cinematic)
- Same `surface_treatment` class (flat / layered / glass / depth)
- Overlapping `reference_style_influences` (at least one shared concrete reference, OR clearly belonging to the same canonical movement)

**Critical CLUSTER rule for Vision (different from Spark):** Keep the same concept expressed in **different idioms** as **separate clusters**. Two engines proposing "minimalist" but one referencing Swiss editorial and the other referencing Apple HIG are *different directions* worth surfacing separately — the visual idiom is the deliverable. Cluster only when both the concept AND the visual idiom overlap.

Record the set of engines that produced each cluster. Preserve all per-engine wording variants of `principles`, `aesthetic_language`, and `reference_style_influences` for use in SYNTHESIZE.

### 6. SCORE — spectrum coverage + concurrence

Vision scores on **two axes**:

#### 6.1 Concurrence axis (per cluster)

| Engines in cluster | Label | Interpretation |
|--------------------|-------|----------------|
| 3 / 3 | `UNIVERSAL` | All engines independently chose this direction — broadly defensible aesthetic, low risk of brand confusion. May also indicate training-data common ground (a popular but "obvious" direction — flag if it matches a competitor too closely). |
| 2 / 3 | `LIKELY` | Two engines concur; one took a different angle — note what the dissenting engine surfaced instead. |
| 1 / 3 | `CANDIDATE → VERIFIED-DIVERGENT` | Only one engine arrived here. Often a unique aesthetic angle from that engine's training data; sometimes a low-quality random direction. Must pass GROUND (step 7) to ship. |

**Vision rule (Pattern D, identical to Spark)**: `VERIFIED-DIVERGENT` directions are **not automatically lower-value** than `UNIVERSAL`. The brand-defining direction often comes from the engine with non-overlapping aesthetic priors. Surface both axes in the final Portfolio.

#### 6.2 Spectrum coverage axis (across the full direction set)

After SCORING by concurrence, check that the surviving directions span an informative slice of the aesthetic spectrum. Reference the canonical positions:

`modernist · skeuomorphic · maximalist · minimalist · brutalist · expressive · calm · spatial · retro-futurist`

Coverage goals:

- **Spread**: at least 2 distinct `spectrum_position` values across the Portfolio (otherwise the user has no real choice — escalate as "low coverage, consider re-running with explicit divergence prompts")
- **Contrast**: at least one direction should sit clearly opposite the most-concurrent direction on the spectrum (e.g., if `UNIVERSAL` = `minimalist`, surface at least one `expressive` or `maximalist` `VERIFIED-DIVERGENT` if grounded)
- **Mode-appropriate skew**: in `LINEAR_RESTRAINT` mode, suppress `maximalist`/`brutalist`; in `SPATIAL` mode, prioritize `spatial`; in `AI_INTERFACE` mode, every direction MUST include a non-empty `ai_disclosure_pattern`

If spectrum coverage is poor (all surviving directions cluster within one position), flag this in the Portfolio summary and recommend a second `multi` run with an explicit divergence-bias prompt (e.g., "produce one direction outside the minimalist tradition").

### 7. GROUND — verify CANDIDATE/DIVERGENT directions (Vision main context, never delegated)

For every `CANDIDATE / DIVERGENT` cluster, the Vision main context must apply these grounding checks:

1. **Brand-fit check** — does the direction respect the stated brand anchor (palette, voice, anti-keywords)? If the direction violates a brand lock without acknowledging it as a deliberate repositioning move, mark `REJECTED-BRAND-DRIFT`.
2. **Persona-fit check** — does `persona_fit` reasoning hold against the named persona (ideally from Cast registry)? Generic "young professionals" framing fails. If contradicts a real Cast persona, mark `REJECTED-PERSONA-MISMATCH`.
3. **Accessibility check** — does `aesthetic_language.color_strategy` and `surface_treatment` retain WCAG 2.2 AA contrast (4.5:1 text / 3:1 UI components)? Glassmorphism, low-contrast minimalism, and brutalist high-contrast inversions are the common failure cases. If a direction implies sub-AA contrast, mark `REJECTED-A11Y` unless the direction itself documents the mitigation.
4. **Reference-existence check** — are the `reference_style_influences` real movements/products? Engines occasionally fabricate brand names. If hallucinated, mark `REJECTED-HALLUCINATION` and downgrade the cluster.
5. **Outcome-link check** — does `business_outcome_link` tie to a measurable metric, not "looks more modern"? Vague aesthetic claims fail.
6. **AI-disclosure check** (only when mode = `AI_INTERFACE`) — does `interaction_language.ai_disclosure_pattern` cover explainability AND user override? Silent prediction-driven UI without override is the top 2026 AI-interface failure pattern; mark `REJECTED-AI-TRUST` if missing.
7. **Mark each as** `VERIFIED-DIVERGENT` (keep), `REJECTED-{reason}` (drop), or `NEEDS-INFO` (ask the user).

For `UNIVERSAL` and `LIKELY` clusters, do a lightweight spot-check on a11y and AI disclosure only — three engines rarely converge on something that violates WCAG 2.2 AA simultaneously, but it does happen with low-contrast minimalism.

### 8. SYNTHESIZE — Portfolio-only (no Compete merge by default)

**Vision differs from Spark here**: design direction is a **selection decision the user must make**, not a synthesis the agent should perform. Vision does NOT collapse multiple directions into one "best" direction by default — that would erase the divergence that makes multi-engine valuable for design.

#### Portfolio Merge (Vision default)

Always emit a **direction Portfolio** of 3–5 complementary directions:

1. Keep all `UNIVERSAL`, `LIKELY`, and `VERIFIED-DIVERGENT` clusters that survived GROUND.
2. Cap at top 5 directions; if more survive, drop the lowest-`business_outcome_link` clarity directions first.
3. Order by: `UNIVERSAL` first (safe baseline), then `LIKELY`, then `VERIFIED-DIVERGENT` (breakthrough candidates). Within tier, prioritize spectrum spread.
4. For each direction, present a **one-page design-direction card**:
   - Concept name + engine-attribution tag + concurrence label
   - 3–5 principles (merged best wording across engines if multi-engine)
   - Aesthetic language (spectrum position, color/typography/surface/imagery)
   - Interaction language (motion, feedback, input priority, AI disclosure if applicable)
   - Reference style influences (deduped across engines)
   - Persona fit and business-outcome link
   - Risk areas
   - Downstream handoff hints (Muse / Palette / Flow / Forge — see §9)
5. Emit a single Portfolio document at `docs/design/PORTFOLIO-direction-[topic]-[date].md`.
6. **Recommendation footer**: identify Vision's lead-recommended direction with explicit concurrence/divergence reasoning (e.g., "Lead = Direction B (UNIVERSAL, lowest novelty cost); challenger = Direction D (VERIFIED-DIVERGENT, highest brand-repositioning upside)").

#### Compete Merge (opt-in only — `multi --compete`)

When the user explicitly requests a single direction (e.g., "I just want one — pick the best"), Vision falls back to a Compete merge:

1. Rank by `UNIVERSAL > LIKELY > VERIFIED-DIVERGENT` with spectrum-fit tiebreaker.
2. Re-mix best wording per field across engine variants of the winning cluster.
3. Emit a single direction document at `docs/design/DIRECTION-[name].md` with `engine_concurrence` front matter and an "Alternative directions considered" appendix.

**Default behavior**: when the user invokes plain `multi` without `--compete`, always produce a Portfolio. Vision's view is that design direction is owned by the user/team; Vision's job is to surface a curated, defensible option set.

#### Engine-attribution rule (both strategies)

Every shipped direction carries:

- Concurrence label: `UNIVERSAL` / `LIKELY` / `VERIFIED-DIVERGENT`
- Engine tag: `[codex+agy+claude]` (3/3) / `[codex+agy]` etc. (2/3) / `[codex-verified]` / `[agy-verified]` / `[claude-verified]` (1/3 grounded)

### 9. DELIVER — downstream handoff preparation

The Portfolio is the deliverable, but Vision must also prepare downstream-ready handoff packets so Muse / Palette / Flow / Forge can pick up the selected direction without re-litigating it.

For each direction in the Portfolio, include a **downstream handoff stub**:

| Downstream agent | Handoff stub content |
|------------------|----------------------|
| `Muse` (tokens) | Token themes to define: color ramp logic, spacing scale, motion duration/easing tokens, depth tokens (if `SPATIAL` or glassmorphism); DTCG v2025.10 format expected |
| `Palette` (usability) | Interaction polish priorities: focus-ring style, hover/active/disabled feedback intensity, dead-state coverage, target-size compliance |
| `Flow` (motion) | Motion choreography keywords: enter/exit pattern, page-transition character, micro-interaction tone, reduced-motion fallback strategy |
| `Forge` (prototype) | First surface to prototype: highest-risk-to-de-risk screen, success criteria for the prototype, expected reviewer cohort |
| `Frame` (Figma MCP) | Figma library expectations: component naming convention, variant axes, token-cascade strategy |
| `Prose` (UX copy) | Voice keywords (5) and anti-keywords (5) implied by this direction's `aesthetic_language` and `interaction_language` |

The user selects one direction from the Portfolio; the selected direction's handoff stubs become the input contract for downstream agents.

---

## Parallel Subagent Prompt Skeleton

Use the canonical spawn/capture template in `_common/CLI_COMPATIBILITY.md` with the JSON schema in this reference. Spawn once per selected available engine, not a fixed three. Add these domain fields; the main context owns normalization, grounding and synthesis.

**Role:**
Generate {N=2-3} design directions for the brief below. You are one of the selected engines working independently — do not try to be exhaustive; surface what your aesthetic training-data priors suggest is most promising. Diverge from safe defaults if your training data points to a stronger angle.

**Target:**
- Operating mode: {REDESIGN | NEW_PRODUCT | TREND_APPLICATION | LINEAR_RESTRAINT | SPATIAL | AI_INTERFACE}
- Product surface: {marketing site | SaaS dashboard | mobile app | spatial | AI agent UI}
- Brand anchor: {existing palette, typography, voice keywords, anti-keywords — or "open"}
- Persona target: {persona name and JTBD — or "open"}
- Business outcome anchor: {conversion lift | task-success | retention | brand repositioning}
- Constraints: WCAG 2.2 AA mandatory; {brand locks}; {platform limits}
- Forbidden directions: {explicit anti-patterns or off-brand aesthetics — or "none"}

**Constraints:**
- Each direction names a concrete CONCEPT, not a generic adjective ("Quiet Industrial" not "Modern")
- Each direction occupies a specific spectrum_position — name it
- Each direction includes at least 3 concrete reference_style_influences (real products, movements, OS design languages)
- Each direction lists at least one risk_area
- Each direction links to a measurable business_outcome
- WCAG 2.2 AA contrast is non-negotiable; explicitly state how the color/surface strategy maintains 4.5:1 text / 3:1 UI contrast
- If mode = AI_INTERFACE: every direction MUST populate interaction_language.ai_disclosure_pattern with explainability AND user override
- Do not write implementation code — direction documents only
- Do not invent brand names or design movements; if you cite a reference, it must be a real, identifiable artifact

## Degraded Modes

Use `_common/MULTI_ENGINE_RECIPE.md` § Engine Availability Modes and its actual-engine denominator. A healthy Claude+Codex pair is the normal dual-engine baseline, not a 2/3 degraded result.

With one usable engine, a 2–3 direction portfolio may still be offered but must be labeled single-engine; preserve user selection and brand/a11y grounding. With zero, use `direction`. An explicitly requested single direction routes to the ordinary recipe rather than inventing a portfolio winner.

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — canonical Pattern D protocol, PREFLIGHT, FAN-OUT, scoring rubric
- `_common/SUBAGENT.md §MULTI_ENGINE` — base subagent dispatch and loose-prompt rules
- `spark/reference/tri-engine-proposal.md` — sibling Pattern D implementation (proposals); CLUSTER/SCORE pattern mirrored here
- `judge/reference/tri-engine-review.md` — canonical PREFLIGHT and FAN-OUT mechanics
- `vision/reference/design-methodology.md` — full per-mode workflow that the selected direction feeds into
- `vision/reference/design-trends.md` — 2026 trend catalog used at GROUND to validate spectrum coverage
- `vision/reference/brand-strategy.md` — brand-fit check criteria applied during GROUND
- `vision/reference/agent-orchestration.md` — Muse / Palette / Flow / Forge / Frame handoff contracts that downstream stubs feed
- `vision/reference/output-formats.md` — direction-card and Portfolio document templates

---

# Multi-Engine Mode (SKILL.md excerpt)

Activated by the `multi` Recipe (or any explicit request for parallel design-direction generation / cross-engine aesthetic comparison). Mirrors Spark's Pattern D but optimizes for *aesthetic-spectrum coverage and brand-defining divergence* rather than feature ideation. Full algorithm, JSON schema, subagent prompt skeletons, CLUSTER/SCORE/GROUND rules, spectrum-coverage logic, downstream handoff stubs, and degraded modes → `reference/tri-engine-direction.md`.

- **Base engine policy (2026-05)**: default = Claude + Codex (dual-engine, 2 spawns); agy adds a third axis (tri-engine) when AVAILABLE at PREFLIGHT — meaningful for Vision because Antigravity surfaces Material 3 Expressive / Google design-language patterns Claude and Codex under-index. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.
- **Mechanics**: spawn one Agent subagent per AVAILABLE engine in one message (`direction-codex` + `direction-claude`, add `direction-agy` when AVAILABLE); PREFLIGHT runs in Vision main context (never delegate detection); loose prompts only (Role + Target + Output format — no rubric/trend-taxonomy/anti-pattern lists, so each engine's aesthetic priors drive divergence); subagents return JSON, main context runs NORMALIZE → CLUSTER → SCORE → GROUND → SYNTHESIZE → DELIVER.
- **Concurrence scoring (Pattern D, identical to Spark/Echo[demand])**: `UNIVERSAL` (3/3) = safe baseline (check against competitor identity to avoid same-as-everyone aesthetic); `LIKELY` (2/3) = strong with one dissenter; `VERIFIED-DIVERGENT` (1/3, grounded) = often the brand-defining direction, NOT automatically lower-value than UNIVERSAL.
- **Aesthetic-spectrum coverage (Vision-specific second axis)**: surviving directions span ≥2 `spectrum_position` values (modernist · minimalist · brutalist · expressive · calm · spatial · …), with at least one opposite the most-concurrent direction. `LINEAR_RESTRAINT` suppresses maximalist/brutalist; `SPATIAL` requires spatial coverage; `AI_INTERFACE` requires `interaction_language.ai_disclosure_pattern` on every direction.
- **Merge**: `Portfolio` (default) — 3–5 complementary direction cards ordered UNIVERSAL → LIKELY → VERIFIED-DIVERGENT, each with principles / aesthetic + interaction language / references / persona fit / outcome link / risk areas / downstream handoff stubs (Muse/Palette/Flow/Forge/Frame/Prose), plus a lead-recommendation + challenger footer (`docs/design/PORTFOLIO-direction-[topic]-[date].md`). `Compete` (opt-in via `multi --compete`) — a single re-mixed direction (`docs/design/DIRECTION-[name].md`). Portfolio is default because Vision writes no code and direction is a human selection decision — collapsing to one winner erases the aesthetic breadth that makes multi-engine valuable.
- **Engine-attribution tag (mandatory on every shipped direction)**: `[codex+agy+claude]` (3/3) / `[codex+agy]` etc. (2/3) / `[codex-verified]` (1/3 verified-divergent).
