# Nexus Venture Recipe Reference

**Purpose:** Generate a comprehensive, cross-functional **business documentation package** from a single business idea — research → product spine → ~11 parallel documentation tracks → overview synthesis → traceability/validation → multi-format file tree + zip. The package is consumable by founders, PMs, designers, engineers, marketers, sales, investors, QA, and legal without further translation.
**Read when:** User invokes `/nexus venture`, or asks for a complete business/product documentation set ("business plan package", "MVP dossier", "startup documentation set", "investor material bundle") that spans planning, branding, product, UX, LP, marketing, tech, AI policy, legal, testing, PM, mock data, and assets together.

> **`venture` is the `startup` preset of the generalized `package` recipe.** `/nexus venture` ≡ `/nexus package domain=startup`. The shared engine (domain-agnostic Phase 0-6) and the full domain-preset registry live in `reference/package-recipe.md`; this file is the startup preset's detailed 14-directory blueprint and per-file → agent mapping. Read this file for startup detail, package-recipe.md for the engine and other domains.

> **Generated-content language:** the documents written into the package follow the CLI output-language config (`settings.json` `language`). This reference file and all recipe instructions are English; the produced package is in the user's configured output language. File names, IDs, schema keys, and code stay English.

## Contents
- Overview
- Invocation Modes
- When to Use Venture
- Depth Tiers and Mode Overlays
- Topology
- Phase 0: Framing
- Phase Contracts (1 → 6)
- Traceability Anchor (the core design constraint)
- Directory → File → Agent Mapping (14 directories)
- Output and Packaging
- Conditional Inclusion
- AUTORUN Chain Template
- Failure Escalation

---

## Overview

Venture is a **document-generation fan-out**, not an implementation loop. It differs from `apex` (which ships working code) by producing a **structured multi-format file tree** — Markdown, CSV, JSON, YAML, SQL, HTML/CSS, and Mermaid — packaged as a downloadable zip. The single hard design constraint is **traceability**: a canonical `feature_id` set (F-001, F-002, …) is fixed at Phase 2 and propagated to every downstream track so that user stories, acceptance criteria, test cases (TC-001…), and backlog items (BL-001…) all reference the same features without drift.

The chain is **depth-scaled and mode-overlaid**. A lite run produces a lean prototype dossier with ~6 agents; a full run fans out to all 14 directories with ~24-28 agents. Mode overlays (`mvp-dev` / `fundraising` / `b2b-saas` / `b2c-growth` / `ai-product`) bias *which tracks get depth*, not which tracks exist.

Venture is **not** a default recipe. It is opt-in for the "I have an idea, give me everything a team needs to act on it" request. Confirm before launching at **full depth** (24+ agents).

## Invocation Modes

| Form | Behavior |
|------|----------|
| `/nexus venture <business idea + optional conditions>` | Standard. Parse idea + optional condition fields, apply default mode (`mvp-dev` + business-prep) and inferred depth, run Phase 0-6. |
| `/nexus venture` (no idea) | Escalate: a business idea is mandatory. Ask for the idea (clarify carve-out) — do **not** auto-invent a venture. |
| `/nexus venture depth=<lite\|mvp\|raise\|full> mode=<...> idea="<X>"` | Explicit depth + mode overlay. `mode` accepts comma-separated overlays. |

Optional condition fields are parsed when present and otherwise filled with documented reasonable assumptions written into `00_overview/assumptions.md`:
`target` / `region` / `platform` / `phase` / `revenue_model` / `team` / `tech_pref` / `budget` / `launch_timing` / `tone` / `depth`.

## When to Use Venture

Use Venture when the request matches **at least 3** of:

- A business/product idea exists but documentation does not — greenfield or pre-MVP.
- Output must serve **multiple roles at once** (Biz + Dev + Design + Marketing + Legal + QA).
- Multiple file formats are required (not just Markdown — CSV/JSON/YAML/SQL/HTML/CSS).
- A single source of truth with cross-document consistency is needed (feature_id traceability).
- The deliverable is a *package to hand off*, not a single artifact.
- Investor / decision-maker summary material is part of the ask.

Route elsewhere when the task is:
- A single PRD or spec → `scribe[unified]` / `scribe` direct
- A single landing page → `funnel` (or `funnel[premium]` for premium LP)
- Market/competitor research only → `field` / `compete` direct
- Brand system only → `vision` / `muse` direct
- Working feature implementation → `apex` or `feature` recipe
- Must-have / killer feature *decision* → `essential` / `killer` recipe
- Deep multi-source research report → `deep-research`

## Depth Tiers and Mode Overlays

**Depth controls fan-out breadth.** Inferred from the `depth` condition field, or explicit `depth=`. Tier semantics and cost bands are the engine's (`reference/package-recipe.md` § Cost and Latency Profile); the table below is the **startup delta** — it renames the default tier (`mvp`, not `standard`), binds each tier to startup directories, and narrows the agent counts, which are canonical for `venture` where they differ from the engine's.

| Depth | Directories produced | Approx agents | Use |
|-------|----------------------|---------------|-----|
| `lite` (lightweight prototype) | 00, 01(lite), 03, 04(lite), 05 | 6-8 | Fast concept validation, hackathon, idea triage |
| `mvp` (default — MVP build + business prep) | 00-13, lean | 14-18 | The standard full package |
| `raise` (fundraising) | 00-13, research/overview/marketing/KPI deepened | 16-20 | Fundraising-grade |
| `full` (full commercialization) | 00-13, all tracks deep + void/canon[regulatory]/crypt | 24-28 | Production business build — **confirm before launch** |

Venture is not free. Budget guardrails (Nexus chain confirmation for 5+ agent chains, full-depth confirmation, no-secrets package scrub) are enforced. For repeated ventures with a stable house style, propose a Sigil-generated project skill to amortize the chain design cost.

**Mode overlays bias depth allocation.** Multiple may combine; they reweight tracks, never remove the core 14.

| Overlay | Tracks deepened |
|---------|-----------------|
| `mvp-dev` (default) | 03 product, 04 ux, 05 lp, 07 tech, 10 testing |
| `fundraising` | 00 overview, 01 research, 06 marketing (GTM/pricing), 03 KPI tree, one_page_pitch |
| `b2b-saas` | 07 security/auth, 09 legal/canon[regulatory], 11 PM (SLA/sales), admin-panel screens in 04 |
| `b2c-growth` | 02 brand, 05 lp, 06 SEO/social/onboarding/retention, 04 onboarding_flow |
| `ai-product` | 08 ai_policy (full), 07 AI/LLM stack, 10 ai_evaluation_cases, human-review workflow |

## Topology

```
Phase 0          Phase 1                Phase 2 [BARRIER]      Phase 3 [11 tracks, waves]         Phase 4          Phase 5              Phase 6
[Framing]        [Research]             [Product Spine]        (feature_id-bound; see Phase        [Overview]       [Integrate+Validate] [Package]
┌────────────┐   ┌──────────────────┐   ┌──────────────────┐    Contracts § Phase 3 table below)  ┌───────────┐    ┌────────────────┐   ┌──────────┐
│ parse idea │──▶│ field+compete    │──▶│ scribe[unified]+spark     │───▶┌────────────────────────────┐───▶│ spark     │───▶│ attest/judge   │──▶│ write    │
│ +mode/depth│   │ ‖ echo[demand]+cast      │   │ +rank+pulse      │    │ 02,04-13 parallel doc tracks│    │ +scribe   │    │ traceability   │   │ tree+zip │
│ +clarify≤3 │   │ (web-grounded or │   │ ═══ F-001… +     │    └────────────────────────────┘    │ +magi     │    │ +manifest+lint │   │ +report  │
└────────────┘   │  research_todo)  │   │  MoSCoW FIXED ═══│                                      └───────────┘    └────────────────┘   └──────────┘
                 └──────────────────┘   └──────────────────┘
```

Hub-and-spoke is preserved: Nexus is the only top-level orchestrator. **Phase 2 is a hard barrier** — no Phase 3 track may start until the canonical `feature_id` + MoSCoW table exists, because every track (testing, PM, KPI, LP) references it. Phase 3 tracks are mutually independent (separate output files, no shared mutable state) and reconverge only at Phase 5 validation. With 11 tracks, Phase 3 exceeds the ≤7-per-hub cap and is run as **waves** (or a native Dynamic Workflow); group dependent file-writers so no two agents write the same file.

## Phase 0: Framing

As the engine's Phase 0 (`reference/package-recipe.md` § Shared Engine) — parse + resolve depth/mode + WebSearch availability check (`01_research/references.md` if grounded, else `01_research/research_todo.md`) + ≤3 clarify gate, each with a stated fallback assumption so work proceeds without a reply. Clarify only on: business domain unidentifiable, target extremely unclear, B2C vs B2B fork, high-risk domain (legal/medical/finance/security), content may be impermissible.

Startup-specific contract fields (extend `package_contract`, `entity_anchor: F-`):

```yaml
venture_contract:
  idea: <one-paragraph normalized idea>
  audience_tone: <startup | investor | internal | enterprise | dev>
  business_model: B2C | B2B | API | marketplace | hybrid
  output_dir: project_document_package
  zip_name: project_document_package_<slug>.zip   # [A-Za-z0-9_-] only
```

## Phase Contracts

### Phase 1: Research (01_research)

| Agent | Role | Required |
|-------|------|----------|
| `field` | Market background, trends, JTBD synthesis, interview/survey design; WebSearch-grounded with sources → `references.md` (or `research_todo.md` if ungrounded) | Yes |
| `compete` | Direct + indirect competitor analysis, differentiation gap, positioning input | Yes (skip at `lite`) |
| `echo[demand]` | Synthetic user demands / pain points / unmet needs across personas | Yes |
| `cast` | Persona generation → `personas.md` | Conditional: depth ≥ mvp |

**Outputs:** `market_research.md`, `user_research_plan.md`, `interview_script.md`, `survey_questions.md`, `personas.md`, `jobs_to_be_done.md`, `competitor_analysis.md`, `trend_analysis.md`, `references.md`, `research_todo.md`.
**Exit gate:** Uncertain claims are flagged as hypotheses; every external claim has a source ref or a research_todo entry.

### Phase 2: Product Spine (03_product) — BARRIER

| Agent | Role | Required |
|-------|------|----------|
| `scribe[unified]` | PRD (L0→L3), user stories, acceptance criteria, IA, non-functional requirements, release plan | Yes |
| `spark` | Feature catalog with `feature_id` (F-001…), `name`, `description`, `user_value`, `mvp_or_later`, related KPI/test/backlog stubs | Yes |
| `rank` | MoSCoW classification (Must / Should / Could / Won't for MVP) | Yes |
| `pulse` | KPI tree + product metrics, each KPI linked to feature_id(s) | Yes (skip at `lite`) |
| `void` | YAGNI scope cut (keep MVP lean) | Conditional: depth = full or scope bloat |

**Outputs:** `prd.md`, `feature_catalog.md`, `mvp_scope.md`, `roadmap.md`, `user_stories.md`, `acceptance_criteria.md`, `kpi_tree.md`, `information_architecture.md`, `product_metrics.md`, `release_plan.md`.
**Exit gate (HARD):** The canonical **feature_id table** (F-001… with MoSCoW tier + mvp_or_later) is finalized and emitted in `_AGENT_CONTEXT` to every Phase 3 track. No Phase 3 agent starts before this. MVP scope must not contain Won't-have items; roadmap and mvp_scope must agree.

### Phase 3: Parallel Documentation Tracks

Each track receives the framing contract + canonical feature_id table. Tracks write to disjoint files. Run in waves to respect the per-hub cap.

| Track | Dir | Agents | Key outputs |
|-------|-----|--------|-------------|
| Brand | 02 | `vision` (direction) → `muse` (`design_tokens.json`) ‖ `prose` (copy/voice) | brand_strategy, naming_candidates (≥20), positioning, brand_voice, messaging_framework, visual_direction, design_tokens.json, copy_examples, brand_checklist |
| UX/UI | 04 | `palette` (usability/states) ‖ `canvas` (Mermaid wireframes) ‖ `echo` (walkthrough) ‖ `prose` (empty/error/loading copy) | ux_flows, screen_specifications, wireframes_mermaid, component_inventory, state_design, onboarding_flow, accessibility_guidelines, responsive_design_policy |
| LP | 05 | `funnel` (`index.html` + `styles.css` + lp_copy + conversion) ‖ `prose` (microcopy) | lp_copy, index.html, styles.css, faq, conversion_strategy, seo_metadata, analytics_plan |
| Marketing | 06 | `funnel`/`funnel[premium]` (GTM/channels) ‖ `pulse` (metrics) ‖ `experiment` (`growth_experiments.md`) | go_to_market_strategy, channel_strategy, pricing_strategy, content_marketing_plan, launch_plan, social_posts (30-day), email_sequences, pr_plan, sales_material_outline, growth_experiments |
| Tech | 07 | `atlas` (architecture+Mermaid) → `schema` (`database_schema.sql`) ‖ `gateway` (`api_design_openapi.yaml`) ‖ `beacon` (monitoring) ‖ `gear` (CI/CD) ‖ `crypt`? (auth/crypto) | system_architecture, tech_stack, data_model, database_schema.sql, api_design_openapi.yaml, data_pipeline, auth_and_permissions, security_privacy, monitoring_observability, infrastructure_plan, ci_cd_plan, technical_risks |
| AI Policy | 08 | `oracle` (AI usage, prompts, eval, guardrails, human review, logging) | ai_usage_policy, prompt_design, evaluation_policy, hallucination_risk_controls, human_review_workflow, model_selection, ai_logging_policy, ai_disclaimer_templates |
| Legal/Risk | 09 | `canon[legal]` (ToS/Privacy/Cookie drafts) ‖ `cloak` (privacy/PII) ‖ `canon[regulatory]`? (compliance_checklist) ‖ `omen`+`ripple` (`risk_register.md`) | legal_considerations, data_rights_policy, privacy_policy_draft, terms_of_service_draft, cookie_policy_draft, risk_register, compliance_checklist |
| Testing | 10 | `matrix` qa-scenario (`test_cases.csv` TC-001…, mapped to feature_id) ‖ `radar` (strategy + `ai_evaluation_cases.csv`) | test_strategy, test_cases.csv, qa_checklist, ai_evaluation_cases.csv, performance_test_plan, security_test_plan, accessibility_test_plan, release_checklist |
| PM | 11 | `sherpa` (`backlog.csv` BL-001…, mapped to feature_id) ‖ `rank` (priority) ‖ `scribe` (RACI/milestones) | backlog.csv, milestones, team_structure, budget_estimate, raci_matrix, decision_log, meeting_cadence, outsourcing_plan |
| Mock Data | 12 | `radar` (fictional sample data only) | sample_users.json, sample_events.json, sample_content.csv, sample_notifications.json, sample_settings.json, sample_logs.json |
| Assets | 13 | `builder[image]` (image_generation_prompts) ‖ `canvas` (diagram_index) | README, icon_direction, image_generation_prompts, diagram_index |

**Per-file writing convention:** every Markdown file includes these sections — Purpose / Intended readers / Assumptions / Body / MVP treatment / Future expansion / Next steps / Related files. CSV/JSON/YAML/SQL/HTML/CSS must be real, loadable, syntactically valid structures.

**Legal disclaimer rule:** all 09 legal content states that professional/legal counsel review is required — never asserted as definitive legal advice.

### Phase 4: Overview Synthesis (00_overview)

Run **after** Phase 3 so the overview reflects (not predicts) the package.

| Agent | Role |
|-------|------|
| `spark` | product_concept, one_page_pitch (for investors / collaborators) |
| `scribe` | executive_summary, decision_summary, 90_day_action_plan |
| `magi` | (depth ≥ raise) sanity-check success conditions, risks, business model coherence |

**Outputs:** `executive_summary.md`, `product_concept.md`, `one_page_pitch.md`, `assumptions.md`, `decision_summary.md`, `90_day_action_plan.md`.

### Phase 5: Integration and Validation

| Agent | Role |
|-------|------|
| `attest` / `judge` | Build the **traceability matrix** and adversarially check consistency across artifacts |
| Nexus (internal) | Generate `document_manifest.csv`, `validation_report.md`, `README.md`; run format syntax checks |

**Traceability matrix verifies:** feature_id↔user_story, feature_id↔acceptance_criteria, feature_id↔test_cases.csv, feature_id↔backlog.csv, KPI↔feature, LP value-prop↔brand message, risk↔mitigation, AI usage↔evaluation case.
**Consistency checks:** idea↔all docs; MVP not over-scoped; MVP vs future not conflated; tech stack ↔ DB/API/infra; target↔LP↔channel↔pricing; tests exist for major features; AI eval cases exist if AI is used; legal/privacy/security noted.
**`validation_report.md` also records:** directory/file completeness vs the depth tier's required set; CSV/JSON/YAML/SQL/HTML/CSS syntax validity (lint command results); post-unzip usability (file count + structure from `unzip -l`).

### Phase 6: Package

As the engine's Phase 6 (`reference/package-recipe.md` § Shared Engine, incl. the format syntax lint commands) — write tree (UTF-8) → syntax lint → zip → expansion test → secrets/PII scrub. Startup-specific naming: tree root `project_document_package/`, archive `project_document_package_<slug>.zip`.

## Traceability Anchor (core design constraint)

As the engine's Generalized Traceability Anchor (`reference/package-recipe.md` § Generalized Traceability Anchor) — the `F-001` entity-id barrier at Phase 2, passed verbatim into every Phase 3 `_AGENT_CONTEXT` handoff; tracks reference existing IDs only, never mint new ones. Startup-specific ID formats: features `F-001`, test cases `TC-001`, backlog `BL-001`. Phase 5 fails the package if any `TC-`/`BL-` item references a non-existent `F-`, or any Must-have feature lacks a user story / AC / test case.

## Output and Packaging

- **Deliverable is a filesystem tree + zip**, not a chat-embedded "download link" (CLI has no download concept). The final report gives the **absolute path** to the zip.
- Directory structure matches the canonical layout exactly (`project_document_package/` with `00_overview` … `13_assets` + top-level `README.md`, `document_manifest.csv`, `validation_report.md`).
- `document_manifest.csv` columns: `path,title,purpose,target_reader,status,related_files,priority`.
- `risk_register.md` columns: `risk_id,category,description,likelihood,impact,mitigation,owner,status`.
- `test_cases.csv` columns: `id,feature_id,category,feature,scenario,precondition,steps,expected_result,priority`.
- `ai_evaluation_cases.csv` columns: `id,input,expected_behavior,risk_type,evaluation_criteria,pass_fail`.
- `backlog.csv` columns: `id,epic,feature_id,task,description,priority,owner,estimate,dependency,status`.
- `growth_experiments.md` items: `experiment_id,hypothesis,target_segment,channel,action,success_metric,duration,required_assets,priority`.

## Conditional Inclusion

| Condition | Add | Skip |
|-----------|-----|------|
| depth = lite | — | 02, 06, 07-deep, 08, 09, 10, 11, 12, 13 (keep 00/01-lite/03/04-lite/05) |
| mode includes ai-product | full 08 + ai_evaluation_cases + human_review | — (08 never skipped in this mode) |
| business_model = B2B / b2b-saas | canon[regulatory], security_privacy deepened, sales_material, SLA in 11 | — |
| business_model = B2C / b2c-growth | 02 brand deep, 05 LP, SEO/social/onboarding in 06 | — |
| UI surface absent (API/infra product) | — | 04 UX, 05 LP (replace with API docs emphasis in 07) |
| Figma in workflow | frame (extract tokens) | — |

(`depth = full` and `web_grounding = unavailable` rows are as the engine's Conditional Inclusion — see `reference/package-recipe.md`.)

## AUTORUN Chain Template

```
Nexus AUTORUN venture idea="<X>" depth=<...> mode=<...>
  ── Phase 0 Framing ──────────────────────────────────
  → as package AUTORUN Phase 0 (`reference/package-recipe.md`), fixed to preset=startup (no
    auto-detect); clarify gate: domain/target/B2X-fork/high-risk/impermissible (else assume)
  → emit venture_contract
  ── Phase 1 Research ─────────────────────────────────
  → field(market+trend+JTBD, web-grounded|research_todo)
  ‖ compete(direct+indirect+diff)?        # skip at lite
  ‖ echo[demand](user demands) → cast(personas)?  # cast if depth≥mvp
  ── Phase 2 Product Spine [BARRIER] ──────────────────
  → scribe[unified](PRD+stories+AC+IA+NFR+release)
  → spark(feature_catalog: F-001… + mvp_or_later)
  → rank(MoSCoW)  → pulse(KPI tree ↔ feature_id)?
  → void(YAGNI)?                          # depth=full or bloat
  → ═══ EMIT canonical feature_id table → bind to all Phase 3 ═══
  ── Phase 3 Parallel Doc Tracks (waves, feature_id-bound) ─
  → [Brand]  vision → muse(design_tokens.json) ‖ prose
  ‖ [UX]     palette ‖ canvas(mermaid) ‖ echo ‖ prose(states)
  ‖ [LP]     funnel(index.html+styles.css+copy) ‖ prose
  ‖ [Mktg]   funnel/funnel[premium] ‖ pulse ‖ experiment(growth_experiments)
  ‖ [Tech]   atlas(arch+mermaid) → schema(schema.sql) ‖ gateway(openapi.yaml)
                                  ‖ beacon ‖ gear ‖ crypt?
  ‖ [AI]     oracle(policy+prompts+eval+guardrails+human_review)
  ‖ [Legal]  canon[legal](ToS/Privacy/Cookie) ‖ cloak ‖ canon[regulatory]? ‖ omen+ripple(risk_register)
  ‖ [Test]   matrix qa-scenario(test_cases.csv TC-001 ↔ F-id) ‖ radar(strategy + ai_eval_cases.csv)
  ‖ [PM]     sherpa(backlog.csv BL-001 ↔ F-id) ‖ rank ‖ scribe(raci/milestones)
  ‖ [Mock]   radar(sample_*.json/csv — fictional only)
  ‖ [Assets] builder[image](image_prompts) ‖ canvas(diagram_index)
  ── Phase 4 Overview Synthesis (post-tracks) ─────────
  → spark(concept+one_page_pitch) ‖ scribe(exec_summary+decision+90day)
  → magi(coherence)?                      # depth≥raise
  ── Phase 5 Integrate + Validate ─────────────────────
  → as package AUTORUN Phase 5 (`reference/package-recipe.md`) — traceability matrix + cross-doc
    consistency + universal grounding gate + document_manifest.csv/validation_report.md/README.md
    + syntax lint (no legal/ai-adoption risk gate; startup carries none)
  ── Phase 6 Package ──────────────────────────────────
  → as package AUTORUN Phase 6 (`reference/package-recipe.md`); startup naming:
    project_document_package/ tree → project_document_package_<slug>.zip
```

## Output Report

`venture` emits the engine's **Package Manifest Report** (`reference/package-recipe.md` § Output Report) with the `startup` preset's inventory — no separate report name. The startup-specific traceability anchor (`feature_id`) and distinctive files are listed in § Output and Packaging above.

## Termination Bound / Resume

Both inherited from the `package` engine (`reference/package-recipe.md`): **Termination bound `N/A`** (non-loop, single forward pass) and **checkpoint-resume** with the Phase 2 `feature_id` list frozen across resumes. This blueprint adds neither.

## Shared-Protocol References

`venture` cites the engine's protocol set rather than re-deriving it — `reference/doc-quality-protocol.md` (W1-W12, discharged by the engine's Phase 5 validation), `reference/autonomy-quality-protocol.md` (intent contract, Acceptance Provenance), and `_common/TRACEABILITY.md` (the `feature_id` anchor). See `reference/package-recipe.md` for how each is applied.

## Failure Modes Prevented

`venture` is the `startup` **preset** of the `package` engine and prevents failures through the engine's consolidated controls — entity-id barrier, Universal Grounding Gate, per-preset Risk Gates, cross-doc consistency, and format lint. See `reference/package-recipe.md` § Failure Modes Prevented; this blueprint adds no preset-specific failure modes beyond the `startup` risk-gate row tabulated there.

## Failure Escalation

| Failure | Detected by | Escalation |
|---------|-------------|------------|
| Business idea missing | Phase 0 | Ask for the idea — do not invent a venture |
| MVP over-scoped (Won't-have leaked) | Phase 5 / void | Re-run rank or void, downgrade scope |
| tech_stack ↔ schema/API mismatch | Phase 5 | Return Tech track |
| LP copy ↔ brand mismatch | Phase 5 | Return LP/Brand track |

5 further rows (domain-unidentifiable clarify gate, Phase 2 entity-table barrier, dangling entity-id reference, format-lint failure, secrets/PII scrub) inherit the engine's Failure Escalation verbatim — see `reference/package-recipe.md` § Failure Escalation.
