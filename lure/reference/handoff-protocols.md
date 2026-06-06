# Handoff Protocols

How `lure` brokers work between stages and how it dispatches each delegate. Every delegate call carries a `LURE_STAGE_BUNDLE`. Every stage exit produces a `STAGE_REPORT`. There is no free-form delegation in `lure`.

---

## `LURE_STAGE_BUNDLE` Schema (Canonical)

The canonical envelope for every delegate invocation. SKILL.md presents a minimum payload view; this file is the source of truth.

```yaml
LURE_STAGE_BUNDLE:
  Recipe: premium | lead-gen | saas | ecom | event | magnet
  Stage: DISCOVER | AUDIENCE | STRATEGY | STRUCTURE | DESIGN | BUILD | OPTIMIZE | VERIFY | LAUNCH
  Delegate: <agent name>
  Primary_Promise: <one sentence; locked at UNDERSTAND/RECIPE phase via Two-Promise Probe>
  Target_Persona: <persona ID or summary; from Audience stage onward>
  CVR_Target: <industry-calibrated value from conversion-playbook.md; from Strategy stage onward>
  Brand_System_Ref:
    path: <path to brand system record; mandatory from STRUCTURE onward>
    vision_archetype_locked: true | false
    saga_story_locked: true | false
    compete_positioning_locked: true | false
  Axis_Targets:
    design_rubric: ">= 20/27"          # Hero-Contract Legibility added as 9th criterion
    motion_rubric: ">= 15/20"
    brand_rubric: ">= 17/24"           # Trust-Signal Density added as 6th criterion
    ia_rubric: ">= 15/20"
    geo_rubric: ">= 15/20"             # /20 scale only — never /100
    lighthouse_mobile: { perf: ">=90", accessibility: ">=95", best_practices: ">=95", seo: ">=95" }
    cwv: { lcp_s: "<=2.5", inp_ms: "<=200", cls: "<=0.1", ttfb_ms: "<=800", fcp_s: "<=1.8" }
    a11y_baseline: WCAG_2.2_AA         # stretch AAA where feasible
    motion_inp_contribution_ms: "<=50" # hard ceiling, not aspiration
  Upstream_Outputs:
    - artifact: <path or summary>
      source_stage: <stage>
      source_agent: <agent>
  Constraints:
    tokens_source: <path to design tokens or "TBD">
    brand_direction: <path to direction.md or "TBD">
    framework: <react | vue | svelte | astro | static>
    locales: [<bcp47 codes> or single locale]
    asset_weight_budget: { hero_image_kb: 200, hero_video_mb: 2, font_total_kb: 100 }
  Success_Criteria:
    - <stage-gate criterion this delegate must hit>
  Provenance:
    project_state: .agents/lure/{project}.json
    decisions_log: .agents/lure.md
  Open_Questions:
    - <unresolved item the delegate should flag, not silently decide>
```

**Rule**: bundle must be complete for the stage being dispatched. Missing fields above the stage's "from" line are blocking. `Brand_System_Ref` must have all three `*_locked` flags `true` before any STRUCTURE-stage bundle is emitted (Brand System triple lock).

## AUTORUN-Gate Matrix

When `_AGENT_CONTEXT.mode = AUTORUN` or `AUTORUN_FULL`, the following stage activities MUST emit `_STEP_COMPLETE.Status = NEED_INFO` and pause — they never proceed silently:

| Trigger | Action |
|---------|--------|
| Brand System triple lock incomplete at STRATEGY exit | NEED_INFO with missing piece (archetype / story / positioning) |
| External paid API would be called (Sketch image gen, Clay 3D, etc.) | NEED_INFO with budget estimate |
| Recipe switch mid-pipeline | NEED_INFO with artifact-compatibility list |
| Fan-out would exceed 5 concurrent delegates (including cross-stage specialists) | NEED_INFO with batching proposal |
| `Brief carries two unrelated value propositions` detected | NEED_INFO with one-promise question |
| Stage gate fails twice in a row | NEED_INFO with repair-or-cut choice |
| External API outage > 2 retries (Frame/Figma MCP, Sketch) | NEED_INFO with fallback options |
| Sentinel high-severity finding requires Builder dispatch | NEED_INFO with routing recommendation |

## Delegate Outage Protocol

| Delegate | Outage Symptom | Fallback Path |
|---------|---------------|---------------|
| **Frame** (Figma MCP 5xx) | get_design_context fails | Manual screenshot bundle from user; downgrade Code Connect to handwritten mapping |
| **Sketch** (image-gen timeout) | hero asset not produced | Ink (vector illustration) or Haul (licensed stock with license check) |
| **Clay** (3D API failure) | model not produced | Static hero illustration via Ink/Sketch; defer 3D to post-launch |
| **Voyager** (BrowserStack/SauceLabs outage) | E2E run fails | Local Playwright run on representative devices; flag risk in Launch dossier |

Triggers OUTAGE recovery: 2 consecutive retries fail with same error class within 5 min.

## State Persistence Discipline

`.agents/lure/{project}.json` is updated by `lure` only. Delegates return values; they do not write state. Write protocol:

1. Read current state.
2. Compute merged state (append-only on `decisions_log`, replace-or-insert on `stages.<STAGE>`).
3. Write to `.agents/lure/{project}.json.tmp`.
4. Atomic rename `.tmp` → `.agents/lure/{project}.json`.

`decisions_log` is append-only; never rewrite or reorder past entries. Each entry has `{ts, decision, by, reason}`.

---

## Delegate-Specific Handoffs

### To Researcher (DISCOVER)

```yaml
Delegate: Researcher
Task: "Identify category structure, market signals, top 3 trends for <Primary_Promise>"
Required_Output:
  - category_definition
  - market_signals: [size, growth, segments]
  - top_3_insights: with citations
Constraints:
  scope: <consumer | B2B | both>
  region: <geo>
```

### To Compete (DISCOVER)

```yaml
Delegate: Compete
Task: "Teardown top 3–5 competitor LPs for <Primary_Promise>"
Required_Output:
  - competitor_list
  - feature_matrix
  - positioning_map
  - top_2_differentiation_hooks
  - ai_brand_visibility_snapshot
Constraints:
  exclude: <competitors to skip>
```

### To Cast (AUDIENCE)

```yaml
Delegate: Cast
Task: "Generate <n=1..3> personas for <Primary_Promise> targeting <segment>"
Required_Output:
  - persona_cards: name, role, goals, frictions, JTBD, channel, decision_driver
  - primary_persona_id
Constraints:
  registry: .agents/cast/registry.json  # reuse if applicable
```

### To Pulse (STRATEGY)

```yaml
Delegate: Pulse
Task: "Design KPI tree, funnel events, CVR target for <Recipe>"
Required_Output:
  - kpi_tree: primary (CVR) + 3..5 secondary
  - funnel_events: ordered event taxonomy
  - cvr_target:
      median: <from playbook>
      top_quartile: <from playbook>
      top_decile: <from playbook>
      chosen_target: <usually median × 1.5 → top-quartile>
      traffic_source_qualifier: <warm | cold | mixed>   # for lead-magnet, B2B contact, newsletter
      recipe_alignment_check: <recipe ↔ playbook row identifier>  # MUST match
  - north_star_metric
  - mention_rate_target: <for GEO measurement, ≥15% mention in AI-search>
  - citation_rate_target: <baseline + 30% via Growth/Beacon>
Constraints:
  industry_baseline_ref: conversion-playbook.md
  alignment_check: |
    if Recipe != row.recipe_id in conversion-playbook.md, FAIL fast.
    if traffic_source_qualifier missing for lead-magnet/B2B/newsletter, FAIL fast.
```

### To Funnel (STRUCTURE)

```yaml
Delegate: Funnel
Task: "Build LP structure for <Recipe> with primary persona <persona_id>"
Required_Output:
  - wireframe_outline: hero + 5..7 sections
  - cta_strategy: above-fold + repeat CTA placement
  - form_design: field list + progressive disclosure plan (if form-driven)
  - copy_direction_brief: headline angle + benefit framing + objection list + proof type
Constraints:
  framework_choice: <e.g., AIDA / PAS / BAB / 4Ps>
  one_promise_rule: enforced
```

### To Prose (STRUCTURE)

```yaml
Delegate: Prose
Task: "Write copy v1 for wireframe outline"
Required_Output:
  - headline + sub-headline (3 variants each for later A/B)
  - hero_cta_micro
  - benefit_block_copy (3..5)
  - objection_handling_copy
  - faq_copy (3..5 Q/A)
  - error_state_microcopy
Constraints:
  voice_and_tone: <from Vision or brand guide>
  reading_level: FK <range>
```

### To Vision (DESIGN)

```yaml
Delegate: Vision
Task: "Set creative direction for <Primary_Promise>, persona <persona_id>"
Required_Output:
  - direction.md: archetype, mood, type direction, palette intent, motion intent
  - rationale: why this direction wins for this persona
Constraints:
  brand_guide_ref: <path or "greenfield">
  archetype_constraints: <if locked>
```

### To Muse (DESIGN)

```yaml
Delegate: Muse
Task: "Produce tokens matching Vision direction"
Required_Output:
  - tokens.json (DTCG-aligned): color, type, spacing, radius, motion
  - apply_plan: where tokens go in codebase
Constraints:
  contrast_minimum: WCAG_2.2_AA
  existing_tokens_ref: <path or "new system">
```

### To Forge (BUILD)

```yaml
Delegate: Forge
Task: "Prototype the LP on Muse tokens"
Required_Output:
  - working_prototype: framework <choice>, tokens applied, no hardcoded values
  - lighthouse_prototype_score
Constraints:
  framework: <from Constraints>
  scope: "prototype only, not production"
```

### To Artisan (BUILD)

```yaml
Delegate: Artisan
Task: "Productionize the Forge prototype"
Required_Output:
  - production_code: type-safe, lint-clean, build-passing
  - component_structure
  - data_contracts (if any)
Constraints:
  tokens_source: <Muse output path>
  perf_budget: <from Constraints>
  framework_idioms: <e.g., RSC for Next.js, Composition API for Vue>
```

### To Growth (OPTIMIZE)

```yaml
Delegate: Growth
Task: "Run four-pillar optimization: SEO + SMO + CRO + GEO"
Required_Output:
  - seo_audit: meta, OGP, JSON-LD, heading hierarchy, alt text
  - smo_spec: social share cards (Twitter/X, OG)
  - cro_recommendations: CTA, form, exit-intent
  - geo_score: AI-citation readiness ≥ 90
Constraints:
  target_keywords: <from brief or Researcher>
  structured_data_types: <Product | Article | Event | Course | FAQ as applicable>
```

### To Bolt (OPTIMIZE)

```yaml
Delegate: Bolt
Task: "Hit perf budget"
Required_Output:
  - lighthouse_mobile: Perf ≥ 90, Acc ≥ 95, BP ≥ 95, SEO ≥ 95
  - cwv: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1
  - optimization_log: what changed and why
Constraints:
  preserve: motion intent (coordinate with Flow), copy fidelity (no truncation)
```

### To Judge (VERIFY)

```yaml
Delegate: Judge
Task: "Tri-engine review of production LP code"
Required_Output:
  - findings: P1/P2/P3 with grounding
  - intent_alignment_verdict
  - ship_recommendation: GO | NO_GO | CONDITIONAL
Constraints:
  spec_source: <Structure stage wireframe + copy spec>
  fail_on: any unresolved P1 or P2
```

### To Voyager (VERIFY)

```yaml
Delegate: Voyager
Task: "E2E test suite for LP"
Required_Output:
  - test_suite: happy path + form submit + CTA flows + error states + visual regression
  - run_result: green
  - a11y_test_result: AA pass
Constraints:
  framework: <Playwright | Cypress | WebdriverIO>
  ci_integration: <yes | no>
```

### To Launch (LAUNCH)

```yaml
Delegate: Launch
Task: "Release plan for LP"
Required_Output:
  - version
  - rollout_strategy: full | staged | canary
  - rollback_plan
  - feature_flag (if applicable)
  - changelog_entry
Constraints:
  release_window: <from user or default>
  dependent_systems: <e.g., analytics, CRM webhook, email automation>
```

---

## Stage Output → Next-Stage Input Map

| Stage | Produces | Consumed By |
|-------|----------|-------------|
| DISCOVER | category_definition, competitors, pain quotes | AUDIENCE, STRATEGY, STRUCTURE |
| AUDIENCE | personas, journey map, unmet needs | STRATEGY, STRUCTURE, DESIGN, VERIFY |
| STRATEGY | KPI tree, CVR target, funnel events | STRUCTURE, BUILD, OPTIMIZE, LAUNCH |
| STRUCTURE | wireframe, copy v1, form spec | DESIGN, BUILD, VERIFY |
| DESIGN | direction.md, tokens, a11y baseline, assets | BUILD, OPTIMIZE, VERIFY |
| BUILD | production code, prototype, motion impl | OPTIMIZE, VERIFY |
| OPTIMIZE | Lighthouse 90+, GEO 90+, first variant | VERIFY, LAUNCH |
| VERIFY | Judge ship-go, Voyager green, Attest 95%+ | LAUNCH |
| LAUNCH | release dossier, live LP, analytics live | (downstream Experiment runs) |

---

## Receiving Handoffs

### From Nexus (`NEXUS_TO_LURE_HANDOFF`)

Schema in `_common/HANDOFF.md`. `lure` reads `Constraints`, `Scope`, and `Acceptance_Criteria`, selects Recipe, and emits its first `LURE_STAGE_BUNDLE`.

### From Judge (`JUDGE_TO_LURE_FEEDBACK`)

When Judge sends feedback on a previously shipped LP:

```yaml
JUDGE_TO_LURE_FEEDBACK:
  Findings: <P1/P2/P3 list>
  Affected_Stages: [VERIFY, OPTIMIZE]  # what should have caught this
  Suggested_Fix: <agent + scope>
```

`lure` either re-enters at Optimize or Verify (scoped repair) or escalates to user.

---

## Emitting Outbound Handoffs

### To Atelier (`LURE_TO_ATELIER_HANDOFF`)

When delegating the whole design pipeline (multi-artifact bundle):

```yaml
LURE_TO_ATELIER_HANDOFF:
  Trigger: "LP + slide + 1-pager + marketing captures bundle"
  Primary_Promise: <one sentence>
  Persona: <persona_id>
  Brand_Direction: <path to direction.md or "needs Vision">
  Artifacts_Requested:
    - landing_page
    - slide_deck
    - 1_pager
    - hero_assets
  Tokens_Source: <existing or "needs Muse">
  Return_Schedule: "single closed-loop pipeline"
```

### To Nexus (`LURE_TO_NEXUS_ESCALATE`)

When scope exceeds LP axis:

```yaml
LURE_TO_NEXUS_ESCALATE:
  Reason: <multi-page site | full product | infra | brand identity>
  LP_Slice_Completed: <stages cleared so far>
  Open_Items: <what remains>
  Recommended_Routing: <next orchestrator or chain>
```

### To User (`LURE_PROGRESS_REPORT`)

After each stage gate:

```yaml
LURE_PROGRESS_REPORT:
  Recipe: <recipe>
  Stage_Reached: <stage>
  Gate_Outcome: PASS | FAIL_REPAIR | FAIL_ESCALATE | CONDITIONAL_PASS
  Artifacts: [<paths>]
  Open_Items: [<list>]
  Next: <stage to advance or question to user>
  ETA_Remaining_Stages: <count>
```

---

## Persistence

State per project lives at `.agents/lure/{project}.json`:

```json
{
  "project": "<id>",
  "recipe": "premium",
  "primary_promise": "...",
  "primary_persona": "...",
  "cvr_target": 0.05,
  "perf_budget": { "lcp_s": 2.5, "inp_ms": 200, "cls": 0.1 },
  "stages": {
    "DISCOVER": { "status": "PASS", "delegates": ["researcher","compete","voice"], "artifacts": ["..."] },
    "AUDIENCE": { "status": "PASS", "delegates": ["cast","echo","plea"], "artifacts": ["..."] },
    "...": {}
  },
  "decisions_log": [
    { "ts": "2026-05-16T10:00:00Z", "decision": "primary persona = ICP-1", "by": "user" }
  ]
}
```
