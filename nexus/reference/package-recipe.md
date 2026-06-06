# Nexus Package Recipe Reference

**Purpose:** Generalized **document-package generator** — turn a single theme/idea/problem into a comprehensive, cross-functional, multi-format file tree (Markdown, CSV, JSON, YAML, SQL, HTML/CSS, Mermaid) + zip, for any of a registry of **domain presets**. One shared engine; per-domain blueprints swap the directory layout, the role→skill mapping, the distinctive outputs, the traceability anchor, and the risk gates.
**Read when:** User invokes `/nexus package` (optionally `domain=<preset>`), or asks for a complete documentation package in a domain covered by the preset registry below (research plan, AI-adoption plan, legal/compliance pack, media-operation kit, growth-experiment plan, generic project package, …).

> **`venture` is the `startup` preset of this recipe.** `/nexus venture` ≡ `/nexus package domain=startup`. The startup blueprint's full per-file detail lives in `reference/venture-recipe.md`; this file is the canonical **engine + preset registry**.
>
> **Generated-content language** follows the CLI output-language config; this reference and all recipe instructions are English. File names, IDs, schema keys, and code stay English.

## Contents
- Overview
- Relationship to venture and other recipes
- Invocation
- The Shared Engine (domain-agnostic Phase 0-6)
- Generalized Traceability Anchor
- Domain Preset Registry
- Preset Auto-Detection
- Per-Preset Blueprints (startup / generic / research / ai-adoption / legal / saas / media / growth)
- Risk Gates
- Conditional Inclusion
- AUTORUN Chain Template
- Failure Escalation
- Cost and Latency Profile

---

## Overview

`package` factors the venture recipe into **engine + blueprint**. Every domain package shares the same skeleton — Phase 0 framing → Phase 1 research → Phase 2 spine (canonical entity-id barrier) → Phase 3 parallel doc tracks → Phase 4 overview synthesis → Phase 5 integrate/validate → Phase 6 zip. Only the **blueprint** varies: which directories exist, which specialist owns each track, which files are distinctive, what the traceability anchor is, and which risk gates fire.

This keeps Nexus to **one recipe** instead of a dozen near-identical ones (Core Rule: minimum viable chain; avoid recipe sprawl). Adding a new domain = adding one row to the Preset Registry, not a new recipe.

## Relationship to venture and other recipes

| Recipe | Relationship |
|--------|--------------|
| `venture` | The `startup` preset. Kept as a named alias for discoverability; dispatches to `package domain=startup`. Full blueprint in `reference/venture-recipe.md`. |
| `apex` | Ships **working code**. `package` ships **documents**. Route to apex when the deliverable is an implemented feature, not a plan. |
| `kaizen` | **Executes** improvement of a shipped feature. The `growth` preset produces a **measurement/experiment plan package** — planning, not execution. Route to kaizen to actually change code. |
| `growth-acceptance` | A **merge lifecycle gate**. The `growth` preset is a planning package, not a gate. |
| `deep-research` | A cited research **report**. The `research` preset produces a full research **operations package** (design + literature + data + analysis + validation), and may invoke `deep-research` inside Phase 1. |
| `accord` / `scribe` / `funnel` / `clause` direct | Single-artifact requests. `package` is for multi-role, multi-file handoff packages. |

## Invocation

| Form | Behavior |
|------|----------|
| `/nexus package domain=<preset> <theme + conditions>` | Explicit preset. Run the engine with that blueprint. |
| `/nexus package <theme>` | Auto-detect preset from theme at Phase 0 (semantic match to the registry); confirm the detected preset if ambiguous. |
| `/nexus venture <idea>` | Alias → `package domain=startup`. |
| `… depth=<lite\|standard\|raise\|full> mode=<...>` | Depth + mode overlays (same semantics as venture). |

Optional condition fields (the collection's "common input sheet") populate the framing contract; missing → documented assumptions in `00_*/assumptions.md`:
`theme` / `background` / `problem` / `audience` / `region` / `objective` / `deliverable_use` / `budget` / `timeline` / `team` / `existing_assets` / `tech_pref` / `monetization_kpi` / `avoid` / `legal_safety_notes` / `depth`.

## The Shared Engine (domain-agnostic Phase 0-6)

Identical to venture's engine; only the blueprint binds differ.

| Phase | Role | Output |
|-------|------|--------|
| **0 Framing** | Parse theme + conditions; resolve preset, depth, modes; WebSearch availability check (else `research_todo.md`); ≤3 clarify only on domain-unidentifiable / high-risk; emit `package_contract` | contract bound to all phases |
| **1 Research** | Preset's research skills, WebSearch-grounded; sources → `references.md` | research dir |
| **2 Spine [BARRIER]** | Preset's spine skills produce the **canonical entity-id table** (see anchor below) | entity list bound to every Phase 3 track |
| **3 Parallel Tracks** | Preset's track→skill map, each consuming the entity-id table, writing disjoint files (run in waves, ≤7/hub) | all domain dirs |
| **4 Overview** | spark + scribe (+ magi at depth ≥ raise) synthesize after tracks | overview dir |
| **5 Integrate+Validate** | attest/judge build the traceability matrix + cross-doc consistency; Nexus writes `document_manifest.csv`, `validation_report.md`, `README.md`; format syntax lint | manifest + report + README |
| **6 Package** | Write tree (UTF-8) → `zip -r` → `unzip -l` test → secrets/PII scrub → report absolute zip path | zip |

`package_contract` (Phase 0 emit):
```yaml
package_contract:
  preset: startup | generic | research | ai-adoption | legal | saas | media | growth
  theme: <normalized one-paragraph theme>
  depth: lite | standard | raise | full
  modes: [...]
  entity_anchor: <id prefix per preset, e.g. F- / H- / UC- / R- / P- / E->
  output_language: <from CLI config>
  web_grounding: available | unavailable
  risk_flags: [legal | medical | finance | safety | public-equity | none]
  assumptions: [(field, assumed_value, why), ...]
  output_dir: <preset>_package
  zip_name: <preset>_package_<slug>.zip   # [A-Za-z0-9_-] only
```

## Generalized Traceability Anchor

venture's "feature_id (F-001) barrier" generalizes to a **canonical entity-id barrier** — Phase 2 fixes the domain's primary entity list before any Phase 3 track runs, and every track references existing IDs only (never mints new ones). Phase 5 fails the package on dangling references or unmapped primary entities.

| Preset | Primary entity (Phase 2 barrier) | Anchor | Downstream chains (must reference) |
|--------|----------------------------------|--------|------------------------------------|
| startup / saas | Feature | `F-001` | user story ↔ AC ↔ `TC-001` ↔ `BL-001`, KPI↔feature |
| generic | Initiative / measure | `M-001` | measure ↔ backlog ↔ `TC-001`, goal↔KPI, risk↔mitigation |
| research | Hypothesis / research question | `H-001` | hypothesis ↔ methodology ↔ finding ↔ source, claim↔evidence |
| ai-adoption | Use case | `UC-001` | use case ↔ prompt ↔ `EVAL-001` ↔ human-review rule |
| legal | Risk / policy clause | `R-001` | risk ↔ mitigation ↔ policy clause ↔ lawyer-review point |
| media | Content pillar | `P-001` | pillar ↔ episode/article ↔ channel ↔ metric |
| growth | Hypothesis / experiment | `H-001` / `E-001` | hypothesis ↔ experiment ↔ metric ↔ learning-log entry |
| career | Target role | `T-001` | self-analysis ↔ market/salary ↔ positioning ↔ skill-gap ↔ job-search ↔ asset |
| learning | Learning objective | `LO-001` | objective ↔ curriculum ↔ material ↔ assessment (alignment matrix) |
| hiring | Role | `R-001` | role ↔ JD ↔ competency ↔ rubric ↔ scorecard ↔ onboarding |

## Domain Preset Registry

| Preset | Subcommand | Directories | Spine skills (Phase 2) | Track skills (Phase 3) | Risk gate |
|--------|-----------|-------------|------------------------|------------------------|-----------|
| **startup** | `package domain=startup` / `venture` | 00_overview … 13_assets (14) | accord+spark+rank+pulse | vision/muse/prose/tone ‖ palette/canvas/echo ‖ funnel ‖ pulse/experiment ‖ atlas/schema/gateway/beacon/gear/crypt ‖ oracle ‖ clause/cloak/oath/omen/ripple ‖ matrix/radar/mint ‖ sherpa/scribe ‖ sketch/canvas | standard |
| **generic** | `package domain=generic` | 00_overview,01_research,02_strategy,03_design,04_execution,05_assets,06_evaluation,07_operations | accord+spark+rank | field ‖ accord/canvas ‖ sherpa/scribe ‖ mint ‖ matrix ‖ omen+ripple | standard |
| **research** | `package domain=research` | 00_research_design,01_literature,02_data,03_analysis,04_outputs,05_validation | accord(question/hypothesis/methodology)+rank | field (+`deep-research` skill via Skill tool, not a spawned track agent) ‖ schema/mint(data) ‖ magi(analysis) ‖ scribe(outputs) ‖ canon+cloak(rigor/ethics) | ethics/bias; medical/policy → expert |
| **ai-adoption** | `package domain=ai-adoption` | 00_overview,01_use_cases,02_data,03_prompt,04_system,05_policy,06_training,07_evaluation,08_rollout | accord(use_cases)+spark+rank | oracle(prompts/RAG/eval) ‖ cloak+sentinel(data/security) ‖ schema(data) ‖ scribe(policy/training) ‖ gear(rollout) ‖ matrix+mint(eval+hallucination cases) ‖ oath(governance) | hallucination + data-sensitivity + human-in-loop mandatory |
| **legal** | `package domain=legal` | 00_overview,01_policy,02_contracts,03_risk,04_operations,05_security_privacy | clause(policy/clause map)+omen | clause(ToS/Privacy/AI/cookie/moderation) ‖ cloak(PII/consent/data-rights) ‖ oath(checklist) ‖ crypt(incident/breach) ‖ oracle(ai_usage_policy) ‖ omen+ripple(legal_risk_register) | **HIGH — mandatory expert-review gate** |
| **saas** | `package domain=saas` | 00_vision,01_product,02_ai_system,03_integrations,04_technology,05_gtm,06_operations,07_testing | accord+spark+rank+pulse | oracle(ai_system) ‖ atlas/schema/gateway(tech) ‖ scribe(product/ops) ‖ funnel/bazaar+pulse(gtm) ‖ gear(integrations/CI) ‖ matrix+mint(testing) | standard (defaults to b2b-saas + ai-product modes) |
| **media** | `package domain=media` | 00_strategy,01_content,02_brand,03_distribution,04_monetization,05_operations,06_assets | accord(content pillars)+spark+rank | cue(scripts/episodes) ‖ prose(articles/tone) ‖ vision/muse(brand/visual) ‖ field(SEO) ‖ funnel(monetization/sponsorship) ‖ pulse(analytics) | copyright/attribution/ad-compliance (clause-light) |
| **growth** | `package domain=growth` | 00_current_state,01_hypotheses,02_experiments,03_design,04_measurement,05_execution | pulse(funnel/baseline)+experiment(hypotheses)+rank(RICE) | experiment(ab_test/backlog) ‖ funnel(friction/flows) ‖ palette/prose(ui_variants/copy_tests) ‖ pulse(event_tracking/dashboard) ‖ magi(opportunity) | standard — **planning only; route to kaizen for execution** |
| **career** | `package domain=career` | 00_self_analysis,01_market_research,02_positioning,03_learning,04_job_search,05_assets,06_execution | ascent(self-analysis → target-role + skill-gap) | ascent(owns whole arc) ‖ field(market/salary) ‖ compete(positioning frameworks) ‖ crest(engineer channel branding) ‖ scribe/prose(asset polish) ‖ canvas(roadmap) | irreversible moves (quit-before-income/relocation/visa); unsourced salary = ASSUMPTION; no legal/tax/financial advice; no fabricated credentials |
| **learning** | `package domain=learning` | 00_learning_goal,01_curriculum,02_materials,03_assessment,04_support,05_progress,06_instructor | agora(objectives → curriculum, Bloom's alignment owner) | agora(curriculum/assessment) ‖ field(topic) ‖ canvas(learning-path) ‖ morph(format) ‖ matrix(hands-on practice) ‖ scribe(formal syllabus) | ALIGNMENT_GAP / ORPHAN_ASSESSMENT; regulated domain (medical/legal/finance/safety/certification) → official-syllabus confirmation |
| **hiring** | `package domain=hiring` | 00_strategy,01_roles,02_candidate_experience,03_onboarding,04_evaluation,05_culture,06_risk | guild(role → JD/competency)+scribe | guild(process/JD/rubric/onboarding) ‖ cast(candidate personas) ‖ prose(outreach/comms) ‖ helm?(headcount/org) ‖ oath(labor-law escalation) | **labor-law / anti-discrimination / PII → lawyer review; protected-class criteria removed, not encoded** |

## Preset Auto-Detection

When `domain=` is omitted, Phase 0 resolves the preset from the theme. Detection is deterministic:

1. **Explicit `domain=` always wins.** Skip detection.
2. **Score the theme's English intent against the signal table below; pick the highest-scoring preset.**
3. Apply the **precedence rules** when more than one row matches.
4. Apply the **confidence gate** — confirm or fall back when the match is weak or tied.

### Theme → Preset signal table

| Theme intent signals (semantic, language-agnostic) | Preset |
|----------------------------------------------------|--------|
| New business/product from an idea, MVP, monetize a concept, investor/pitch material, launch a new venture | `startup` |
| The product *is* software sold as a service — multi-tenant platform, pricing tiers, productization of a tool, AI product platform | `saas` |
| Research question / hypothesis / methodology / literature review / academic or policy study / survey analysis / reproducibility | `research` |
| Adopting or rolling out AI internally, RAG design, prompt library, AI governance, LLM workflow automation, AI enablement/training | `ai-adoption` |
| The deliverable itself is a legal/compliance pack — ToS, Privacy Policy, AI usage policy, contracts, data rights, legal risk register | `legal` |
| Content/editorial operation — YouTube/podcast/blog/newsletter, editorial calendar, channel growth, audience monetization, content pillars | `media` |
| Improving an **existing** product's metrics — funnel/CVR/churn, A/B experiments, growth hypotheses, retention (planning a measurement program) | `growth` |
| Personal career — job change, side-business, independence, portfolio, interview, salary negotiation | `career` |
| Curriculum / course / training design, lesson plans, assessment, learning program | `learning` |
| Recruitment / hiring process, job descriptions, interview rubrics, onboarding, org design | `hiring` |
| Generic project/initiative/plan that matches none of the above (strategy → execution → operations) | `generic` |

### Precedence rules (multiple matches)

- **legal vs other**: if the *deliverable* is the legal pack → `legal`. If legal is one concern inside a broader build → the broader preset (startup/saas/…) with its legal track, not the `legal` preset.
- **startup vs saas**: `saas` only when the product itself is software-sold-as-a-service (platform, tenancy, pricing tiers). Otherwise `startup`.
- **startup vs growth**: launching something new → `startup`. Improving something already shipped → `growth`.
- **growth (this preset) vs `kaizen`/`growth-acceptance`/`experiment` (other recipes)**: `package domain=growth` produces a **planning package** only. If the user wants to *execute* an improvement → route to `kaizen`; to *gate a merge* with growth proof → `growth-acceptance`; for a *single A/B test design* → `experiment` direct. State the chosen routing in the report.
- **ai-adoption vs saas**: building/selling an AI product → `saas`. Adopting AI for internal operations → `ai-adoption`.
- **research vs `deep-research` (recipe)**: a full research *operations package* (design + literature + data + analysis + validation dirs) → `research` preset. A single cited *report* → `deep-research` direct.

### Confidence gate

| Condition | Action |
|-----------|--------|
| Single clear top preset | Proceed with it (state the detected preset in the opening line of the run). |
| Top-2 within a close margin | Confirm preset with the user (present the top 2 + one-line rationale each). In `AUTORUN_FULL`, pick the higher and state the assumption + the alternative. |
| No row scores (theme unmatched) | Fall back to `generic`; surface "matched no specialized preset → generic" in the report. |
| Novel domain with no matching preset/skill (none of the 12 fit) | Use `generic`, and emit a **gap note**: "<domain> has no dedicated preset/skill — produced via generic; recommend a dedicated skill via `architect` if this recurs." Mark with `#TODO(agent): promote <domain> to a first-class preset once a dedicated skill exists`. |

## Per-Preset Blueprints

Each preset's distinctive outputs (beyond README/manifest/validation_report) and per-file conventions. The per-file Markdown convention (Purpose / Intended readers / Assumptions / Body / MVP-or-current treatment / Future expansion / Next steps / Related files) applies to all presets. CSV/JSON/YAML/SQL/HTML/CSS must be real, loadable, syntactically valid.

### startup
Full 14-directory blueprint with per-file → agent mapping: **`reference/venture-recipe.md`**. Distinctive: one_page_pitch, design_tokens.json, index.html LP, database_schema.sql, api_design_openapi.yaml, test_cases.csv, backlog.csv, growth_experiments.md, risk_register.md.

### generic
Lightest preset (the collection's "universal"). Distinctive: `00_overview/{summary,goals,assumptions,decision_summary,90_day_action_plan}`, `01_research/{context,stakeholder_map,current_state,benchmark,references,research_todo}`, `02_strategy/{strategy,positioning,success_metrics,roadmap,risk_register}`, `03_design/{requirements,workflows,information_architecture,templates,diagrams_mermaid}`, `04_execution/{action_plan,backlog.csv,timeline,owners,raci_matrix}`, `05_assets/{examples,copy_templates,data_templates.csv,mock_data.json}`, `06_evaluation/{test_cases.csv,checklist,metrics,review_process}`, `07_operations/{operating_model,governance,maintenance,improvement_cycle}`. No brand/LP. Use when the domain doesn't match a richer preset.

### research
Distinctive: `research_question.md`, `hypothesis.md`, `methodology.md`, `limitations.md`, `literature_review.md`, `source_matrix.csv`, `annotated_bibliography.md`, `coding_scheme.md`, `findings_template.md`, `peer_review_checklist.md`, `reproducibility_checklist.md`, `bias_and_ethics.md`. Phase 1 may invoke the `deep-research` skill (via the Skill tool — it is a harness skill, not a `skills/`-path spawnable agent) for grounded literature. Anchor: hypothesis_id `H-001` ↔ methodology ↔ finding ↔ `source_matrix.csv` row. **Validity gate**: every claim traces to a source or a research_todo entry; reproducibility + bias/ethics files mandatory.

### ai-adoption
Distinctive: `prompt_library.md`, `role_based_prompts.md`, `evaluation_prompts.md`, `ai_evaluation_cases.csv`, `hallucination_test_cases.csv`, `forbidden_use_cases.md`, `human_review_rules.md`, `rag_source_plan.md`, `model_selection.md`, `rollout_plan.md`. Anchor: use_case_id `UC-001` ↔ prompt ↔ `ai_evaluation_cases.csv` (`EVAL-001`) ↔ human_review_rule. **Mandatory gates**: every use case has ≥1 eval case + a human-review rule; high-risk use cases (medical/finance/legal) carry forbidden-use entries.

### legal
Distinctive: `privacy_policy_draft.md`, `terms_of_service_draft.md`, `ai_usage_policy.md`, `cookie_policy.md`, `moderation_policy.md`, `nda_template.md`, `vendor_contract_checklist.md`, `data_processing_agreement_outline.md`, `legal_risk_register.md`, `compliance_checklist.md`, `lawyer_review_points.md`, `data_rights_matrix.md`, `consent_management.md`, `incident_response.md`, `breach_response_checklist.md`. Anchor: risk_id `R-001` ↔ mitigation ↔ policy clause ↔ lawyer_review_point. **HIGH-RISK gate (mandatory)**: every legal document carries an explicit "draft only — not legal advice — professional/legal counsel review required" disclaimer; Phase 5 **fails** the package if any draft lacks a `lawyer_review_points.md` reference. Surface the expert-review requirement in the final report.

### saas
= startup blueprint re-keyed to the SaaS dirs, defaulting to `b2b-saas` + `ai-product` mode overlays. Distinctive: `package_type_catalog.md`, `generation_flow.md`, `prompt_orchestration.md`, `agent_workflow.md`, `validation_engine.md`, `model_selection.md`, `zip_export.md`, integration plans (`notion_export.md`, `github_integration.md`, `figma_linear_jira_plan.md`), `database_schema.sql`, `api_design_openapi.yaml`, `pricing.md`, `package_quality_score.md`, `ai_eval_cases.csv`. Reuse startup's tech + GTM tracks; add the AI-system track from the ai-adoption preset.

### media
Distinctive: `content_pillars.md`, `editorial_calendar.csv`, `episode_ideas.md`, `article_templates.md`, `tone_of_voice.md`, `visual_guidelines.md`, `thumbnail_guidelines.md`, `channel_strategy.md`, `seo_strategy.md`, `newsletter_strategy.md`, `sponsorship_plan.md`, `product_funnel.md`, `production_workflow.md`, `scripts.md`, `analytics_dashboard_plan.md`. Anchor: content_pillar_id `P-001` ↔ episode/article ↔ channel ↔ metric. **Coverage note (known gap)**: no single skill owns editorial strategy — assembled from `cue` (scripts/episodes) + `prose` (articles/tone) + `field` (SEO) + `vision/muse` (visual) + `funnel`/`pulse` (monetization/analytics). Lossy vs a dedicated editor skill; flag to user. Risk: copyright/attribution/ad-disclosure — add `clause` (light) for sponsorship/ad-compliance review.

### growth
Distinctive: `funnel_analysis.md`, `friction_points.md`, `opportunity_matrix.md`, `growth_hypotheses.md`, `experiment_backlog.csv`, `ab_test_plan.md`, `success_metrics.md`, `prioritization_rice.csv`, `improved_flows.md`, `copy_tests.md`, `ui_variants.md`, `event_tracking_plan.md`, `dashboard_spec.md`, `analysis_template.md`, `learning_log.md`. Anchor: hypothesis_id `H-001` / experiment_id `E-001` ↔ metric ↔ learning-log entry. **Dedup discipline**: this preset produces a *planning package* only. If the user wants to actually implement an improvement → route to `kaizen`; to gate a merge with growth proof → `growth-acceptance`; for a single A/B test design → `experiment` direct. State this routing in the final report when growth is selected.

### career
Owner skill: `ascent`. Distinctive: `strengths_weaknesses.md`, `achievement_inventory.md`, `salary_research.md`, `skill_gap_analysis.md`, `positioning.md`, `elevator_pitch.md`, `portfolio_strategy.md`, `target_company_list.csv`, `application_tracker.csv`, `outreach_templates.md`, `cover_letter_templates.md`, `negotiation_strategy.md`, `90_day_plan.md`. Anchor: target_role `T-001` ↔ self-analysis ↔ market/salary ↔ positioning ↔ job-search ↔ asset. Engineer-specific channel branding → hand to `crest`. **Risk**: irreversible moves (quit-before-income / relocation / visa) flagged; salary claims without a source marked `ASSUMPTION — confirm`; no legal/tax/financial advice asserted as fact; never fabricate achievements/credentials.

### learning
Owner skill: `agora`. Distinctive: `learning_objectives.md`, `prerequisite_check.md`, `outcome_definition.md`, `lesson_plans.md`, `quizzes.csv`, `rubric.md`, `self_assessment.md`, `progress_checkpoints.md`, `study_tracker.csv`, `coaching_prompts.md`, `common_mistakes.md`, `alignment_matrix.md`. Anchor: learning objective `LO-001` (Bloom's-leveled) ↔ curriculum ↔ material ↔ assessment, via the alignment matrix. **Gate**: every objective has ≥1 aligned assessment (`ALIGNMENT_GAP` fails) and every assessment maps to an objective (`ORPHAN_ASSESSMENT` fails); objectives use measurable verbs; regulated domains (medical/legal/finance/safety/certification) require official-syllabus confirmation.

### hiring
Owner skill: `guild`. Distinctive: `recruitment_strategy.md`, `job_descriptions.md`, `competency_matrix.md`, `interview_rubric.md`, `scorecards.csv`, `candidate_journey.md`, `outreach_templates.md`, `communication_templates.md`, `onboarding_plan_30_60_90.md`, `first_week_checklist.md`, `performance_review_template.md`, `culture.md`, `bias_reduction_checklist.md`. Anchor: role `R-001` ↔ JD ↔ competency ↔ rubric ↔ scorecard ↔ onboarding. Candidate persona depth → `cast`; regulatory framework audit → `oath`. **HIGH-RISK gate (mandatory)**: labor-law / anti-discrimination / PII content is advisory only — every such doc carries a "requires labor-law (lawyer) review before use" disclaimer; **protected-class screening criteria must be removed, not encoded**; Phase 5 fails on encoded protected-class criteria.

## Risk Gates

| Risk flag | Trigger preset(s) | Gate |
|-----------|-------------------|------|
| legal | legal (always); any preset with legal drafts | Mandatory "not legal advice / expert review required" disclaimer on every legal doc; Phase 5 fails on missing `lawyer_review_points` reference |
| medical / finance / safety | any (from theme) | Phase 0 surfaces high-risk; mark all domain claims as hypotheses; recommend domain-expert review in final report |
| labor-law / anti-discrimination | hiring | Every hiring-law doc carries "requires lawyer review"; protected-class screening criteria removed, not encoded (Phase 5 fails on encoded criteria) |
| alignment (learning) | learning | Phase 5 fails on `ALIGNMENT_GAP` (objective w/o assessment) or `ORPHAN_ASSESSMENT` (assessment w/o objective); regulated domains need official-syllabus confirmation |
| hallucination / data-sensitivity | ai-adoption, saas | Every use case requires an eval case + human-review rule; forbidden-use entries for high-risk use cases |

## Conditional Inclusion

| Condition | Add | Skip |
|-----------|-----|------|
| depth = lite | — | deep tracks; keep overview + research-lite + spine + one primary track |
| depth = full | void (scope cut), oath, crypt, deeper scribe | — |
| web_grounding = unavailable | `research_todo.md` (enumerate lookups, mark hypotheses) | live `references.md` sourcing |
| preset = legal/ai-adoption | risk gate (mandatory) | — |
| preset = media | clause-light (ad/sponsorship) | heavy tech tracks |
| theme has UI/product surface (generic/research/etc.) | borrow startup's UX/LP tracks | — |

## AUTORUN Chain Template

```
Nexus AUTORUN package domain=<preset> theme="<X>" depth=<...> mode=<...>
  ── Phase 0 Framing ──────────────────────────────────
  → parse theme + condition fields → resolve preset (auto-detect if omitted)
  → web_grounding check → risk-flag scan
  → clarify gate (≤3 Qs only on domain-unidentifiable / high-risk; else assume)
  → emit package_contract (entity_anchor per preset)
  ── Phase 1 Research ─────────────────────────────────
  → preset.research_skills (web-grounded | research_todo)
       research preset → may invoke deep-research
  ── Phase 2 Spine [BARRIER] ──────────────────────────
  → preset.spine_skills → ═══ EMIT canonical entity-id table (F-/H-/UC-/R-/P-/E-) ═══
       → bind to every Phase 3 track
  ── Phase 3 Parallel Doc Tracks (waves, entity-id-bound) ─
  → preset.track_skills (disjoint files; ≤7/hub per wave)
  ── Phase 4 Overview Synthesis (post-tracks) ─────────
  → spark + scribe (+ magi if depth≥raise)
  ── Phase 5 Integrate + Validate ─────────────────────
  → attest/judge(traceability matrix per preset anchor + cross-doc consistency)
  → risk gate (legal/ai-adoption presets) → fail on missing disclaimer/eval/review
  → Nexus: document_manifest.csv + validation_report.md + README.md + syntax lint
  ── Phase 6 Package ──────────────────────────────────
  → write tree (UTF-8) → zip -r <preset>_package_<slug>.zip
  → unzip -l test → secrets/PII scrub
  → report: zip path, file count, main contents, validation, caveats + routing notes
```

## Failure Escalation

| Failure | Detected by | Escalation |
|---------|-------------|------------|
| Preset ambiguous from theme | Phase 0 | Confirm detected preset (or ask among top 2) |
| Theme/domain unidentifiable | Phase 0 clarify gate | ≤3 questions with fallback assumptions |
| Phase 2 entity table incomplete | spine skills | Block Phase 3; re-run spine — barrier must not be bypassed |
| Track references non-existent entity-id | Phase 5 traceability | Return that track for correction |
| Legal draft missing review reference | Phase 5 legal gate | Fail package; add `lawyer_review_points`, re-validate |
| AI use case missing eval/human-review | Phase 5 ai gate | Return ai-adoption track |
| Format syntax invalid | Phase 6 lint | Fix file, re-lint before zipping |
| Secrets/PII detected | Phase 6 scrub | Remove and re-package; never ship |
| Novel domain outside the 12 presets | Phase 0 | Use `generic` + flag the missing dedicated skill; recommend `architect` for a new skill if recurring |

## Cost and Latency Profile

| Depth | Approx agents | Approx cost |
|-------|---------------|-------------|
| lite | 5-8 | Low |
| standard (default) | 12-18 | Medium |
| raise | 16-20 | Medium-High |
| full | 22-28 | High — **confirm before launch** |

Same guardrails as venture (5+ agent chain confirmation, full-depth confirmation, no-secrets scrub). When a native Dynamic Workflow substrate is available, delegate the Phase 3 parallel sweep to it and keep Nexus as the entity-id-contract + validation layer.

## Coverage Map vs the source collection

| Source prompt | Preset | Status |
|---------------|--------|--------|
| 01 startup_launch | startup | ✅ (= venture) |
| 11 package_generator_saas | saas | ✅ |
| 00 universal | generic | ✅ |
| 05 research | research | ✅ |
| 02 ai_adoption | ai-adoption | ✅ |
| 09 legal_compliance | legal | ✅ (high-risk gate) |
| 10 growth_optimization | growth | ✅ (planning-only; dedup vs kaizen/growth-acceptance) |
| 07 media_operation | media | ✅ (known editorial-skill gap, lossy) |
| 03 career_strategy | career | ✅ (owner skill `ascent`; irreversible-move + salary-source gates) |
| 04 learning | learning | ✅ (owner skill `agora`; Bloom's alignment gate) |
| 06 hiring_org | hiring | ✅ (owner skill `guild`; labor-law lawyer-review gate) |
| 00 pdca_prompt | — | ❌ out of scope (prompt-improvement meta — route to `architect` / `quality-iteration`) |
| 12 templates (input sheet / quality gate) | — | ♻️ folded into Phase 0 framing contract / Phase 5 validation contract |

All 12 source domains except the meta prompt-improvement prompt now have first-class presets backed by a dedicated owner skill. A novel domain outside these 12 still falls back to `generic` with a surfaced gap note; promote it once a dedicated skill exists (propose via `architect`).
