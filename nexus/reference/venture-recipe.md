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
- Validation Contract
- Conditional Inclusion
- AUTORUN Chain Template
- Failure Escalation
- Cost and Latency Profile

---

## Overview

Venture is a **document-generation fan-out**, not an implementation loop. It differs from `apex` (which ships working code) by producing a **structured multi-format file tree** — Markdown, CSV, JSON, YAML, SQL, HTML/CSS, and Mermaid — packaged as a downloadable zip. The single hard design constraint is **traceability**: a canonical `feature_id` set (F-001, F-002, …) is fixed at Phase 2 and propagated to every downstream track so that user stories, acceptance criteria, test cases (TC-001…), and backlog items (BL-001…) all reference the same features without drift.

The chain is **depth-scaled and mode-overlaid**. A lite run produces a lean prototype dossier with ~6 agents; a full run fans out to all 14 directories with ~24-28 agents. Mode overlays (`mvp-dev` / `fundraising` / `b2b-saas` / `b2c-growth` / `ai-product`) bias *which tracks get depth*, not which tracks exist.

Venture is **not** a default recipe. It is opt-in for the "I have an idea, give me everything a team needs to act on it" request. Confirm before launching at **full depth** (24+ agents).

Because Phase 3 is a large homogeneous parallel sweep, it is a natural candidate for a **native Dynamic Workflow** execution substrate (`reference/managed-agents-mapping.md` §5) when available — Nexus stays the routing/recipe layer (which tracks, what feature_id contract) and delegates the parallel track execution. Fall back to L2 parallel spawn otherwise.

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
- A single PRD or spec → `accord` / `scribe` direct
- A single landing page → `funnel` (or `bazaar` for premium LP)
- Market/competitor research only → `field` / `compete` direct
- Brand system only → `vision` / `muse` direct
- Working feature implementation → `apex` or `feature` recipe
- Must-have / killer feature *decision* → `essential` / `killer` recipe
- Deep multi-source research report → `deep-research`

## Depth Tiers and Mode Overlays

**Depth controls fan-out breadth.** Inferred from the `depth` condition field, or explicit `depth=`.

| Depth | Directories produced | Approx agents | Use |
|-------|----------------------|---------------|-----|
| `lite` (lightweight prototype) | 00, 01(lite), 03, 04(lite), 05 | 6-8 | Fast concept validation, hackathon, idea triage |
| `mvp` (default — MVP build + business prep) | 00-13, lean | 14-18 | The standard full package |
| `raise` (fundraising) | 00-13, research/overview/marketing/KPI deepened | 16-20 | Fundraising-grade |
| `full` (full commercialization) | 00-13, all tracks deep + void/oath/crypt | 24-28 | Production business build — **confirm before launch** |

**Mode overlays bias depth allocation.** Multiple may combine; they reweight tracks, never remove the core 14.

| Overlay | Tracks deepened |
|---------|-----------------|
| `mvp-dev` (default) | 03 product, 04 ux, 05 lp, 07 tech, 10 testing |
| `fundraising` | 00 overview, 01 research, 06 marketing (GTM/pricing), 03 KPI tree, one_page_pitch |
| `b2b-saas` | 07 security/auth, 09 legal/oath, 11 PM (SLA/sales), admin-panel screens in 04 |
| `b2c-growth` | 02 brand, 05 lp, 06 SEO/social/onboarding/retention, 04 onboarding_flow |
| `ai-product` | 08 ai_policy (full), 07 AI/LLM stack, 10 ai_evaluation_cases, human-review workflow |

## Topology

```
Phase 0          Phase 1                Phase 2 [BARRIER]      ┌──────────── Phase 3: Parallel Doc Tracks ──────────────┐   Phase 4         Phase 5            Phase 6
[Framing]        [Research]             [Product Spine]        │  (each track consumes the canonical feature_id table)   │   [Overview]      [Integrate+Validate] [Package]
┌────────────┐   ┌──────────────────┐   ┌──────────────────┐   │ 02 Brand    vision+muse+prose+tone                      │   ┌───────────┐   ┌────────────────┐  ┌──────────┐
│ parse idea │   │ field       │   │ accord (PRD)     │   │ 04 UX       palette+canvas+echo+prose                   │   │ spark     │   │ attest/judge   │  │ write    │
│ +conditions│──▶│ +compete         │──▶│ +spark (features)│──▶│ 05 LP       funnel+prose                                │──▶│ +scribe   │──▶│ traceability   │─▶│ tree     │
│ +mode/depth│   │ ‖ plea +cast     │   │ +rank (MoSCoW)   │   │ 06 Mktg     funnel/bazaar+pulse+experiment                │   │ +magi     │   │ matrix         │  │ +zip -r  │
│ +clarify≤3?│   │ (WebSearch       │   │ +pulse (KPI)     │   │ 07 Tech     atlas+schema+gateway+beacon+gear+crypt?     │   │ (00_*)    │   │ +manifest.csv  │  │ +syntax  │
│ +web check │   │  grounded or     │   │ ═══ F-001… +     │   │ 08 AI       oracle                                      │   │           │   │ +validation_*  │  │  lint    │
└────────────┘   │  research_todo)  │   │  MoSCoW FIXED ═══│   │ 09 Legal    clause+cloak+oath?+omen+ripple            │   │           │   │ +README        │  │ +report  │
                 └──────────────────┘   └──────────────────┘   │ 10 Test     matrix+radar?+mint                          │   └───────────┘   └────────────────┘  └──────────┘
                                                               │ 11 PM       sherpa+rank+scribe                          │
                                                               │ 12 Mock     mint                                        │
                                                               │ 13 Assets   sketch+canvas                               │
                                                               └────────────────────────────────────────────────────────┘
```

Hub-and-spoke is preserved: Nexus is the only top-level orchestrator. **Phase 2 is a hard barrier** — no Phase 3 track may start until the canonical `feature_id` + MoSCoW table exists, because every track (testing, PM, KPI, LP) references it. Phase 3 tracks are mutually independent (separate output files, no shared mutable state) and reconverge only at Phase 5 validation. With 11 tracks, Phase 3 exceeds the ≤7-per-hub cap and is run as **waves** (or a native Dynamic Workflow); group dependent file-writers so no two agents write the same file.

## Phase 0: Framing

**Purpose:** Establish the contract for the whole package before any agent spawns.

1. **Parse** the business idea + optional condition fields. Missing fields → documented assumptions (written to `00_overview/assumptions.md`), do not block.
2. **Resolve depth + mode overlays** (defaults: `depth=mvp`, `mode=mvp-dev` + business prep).
3. **WebSearch availability check.** If browsing is available, Phase 1 research is grounded with sources in `01_research/references.md`. If unavailable, all items needing fresh data are enumerated in `01_research/research_todo.md` and marked as hypotheses (not asserted as fact).
4. **Clarify gate (max 3 questions).** Ask **only** if one of these would materially change the package: (a) business domain unidentifiable, (b) target extremely unclear, (c) B2C vs B2B forks the whole package, (d) high-risk domain (legal/medical/finance/security), (e) content may be impermissible. Even when asking, state the fallback assumption so work can proceed without a reply.
5. **Emit the framing contract** bound to all downstream phases:

```yaml
venture_contract:
  idea: <one-paragraph normalized idea>
  depth: lite | mvp | raise | full
  modes: [mvp-dev, business-prep, ...]
  audience_tone: <startup | investor | internal | enterprise | dev>
  business_model: B2C | B2B | API | marketplace | hybrid
  output_language: <from CLI config>
  web_grounding: available | unavailable
  assumptions: [(field, assumed_value, why), ...]
  output_dir: project_document_package
  zip_name: project_document_package_<slug>.zip   # [A-Za-z0-9_-] only
```

## Phase Contracts

### Phase 1: Research (01_research)

| Agent | Role | Required |
|-------|------|----------|
| `field` | Market background, trends, JTBD synthesis, interview/survey design; WebSearch-grounded with sources → `references.md` (or `research_todo.md` if ungrounded) | Yes |
| `compete` | Direct + indirect competitor analysis, differentiation gap, positioning input | Yes (skip at `lite`) |
| `plea` | Synthetic user demands / pain points / unmet needs across personas | Yes |
| `cast` | Persona generation → `personas.md` | Conditional: depth ≥ mvp |

**Outputs:** `market_research.md`, `user_research_plan.md`, `interview_script.md`, `survey_questions.md`, `personas.md`, `jobs_to_be_done.md`, `competitor_analysis.md`, `trend_analysis.md`, `references.md`, `research_todo.md`.
**Exit gate:** Uncertain claims are flagged as hypotheses; every external claim has a source ref or a research_todo entry.

### Phase 2: Product Spine (03_product) — BARRIER

| Agent | Role | Required |
|-------|------|----------|
| `accord` | PRD (L0→L3), user stories, acceptance criteria, IA, non-functional requirements, release plan | Yes |
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
| Brand | 02 | `vision` (direction) → `muse` (`design_tokens.json`) ‖ `prose` (copy) ‖ `tone` (voice) | brand_strategy, naming_candidates (≥20), positioning, brand_voice, messaging_framework, visual_direction, design_tokens.json, copy_examples, brand_checklist |
| UX/UI | 04 | `palette` (usability/states) ‖ `canvas` (Mermaid wireframes) ‖ `echo` (walkthrough) ‖ `prose` (empty/error/loading copy) | ux_flows, screen_specifications, wireframes_mermaid, component_inventory, state_design, onboarding_flow, accessibility_guidelines, responsive_design_policy |
| LP | 05 | `funnel` (`index.html` + `styles.css` + lp_copy + conversion) ‖ `prose` (microcopy) | lp_copy, index.html, styles.css, faq, conversion_strategy, seo_metadata, analytics_plan |
| Marketing | 06 | `funnel`/`bazaar` (GTM/channels) ‖ `pulse` (metrics) ‖ `experiment` (`growth_experiments.md`) | go_to_market_strategy, channel_strategy, pricing_strategy, content_marketing_plan, launch_plan, social_posts (30-day), email_sequences, pr_plan, sales_material_outline, growth_experiments |
| Tech | 07 | `atlas` (architecture+Mermaid) → `schema` (`database_schema.sql`) ‖ `gateway` (`api_design_openapi.yaml`) ‖ `beacon` (monitoring) ‖ `gear` (CI/CD) ‖ `crypt`? (auth/crypto) | system_architecture, tech_stack, data_model, database_schema.sql, api_design_openapi.yaml, data_pipeline, auth_and_permissions, security_privacy, monitoring_observability, infrastructure_plan, ci_cd_plan, technical_risks |
| AI Policy | 08 | `oracle` (AI usage, prompts, eval, guardrails, human review, logging) | ai_usage_policy, prompt_design, evaluation_policy, hallucination_risk_controls, human_review_workflow, model_selection, ai_logging_policy, ai_disclaimer_templates |
| Legal/Risk | 09 | `clause` (ToS/Privacy/Cookie drafts) ‖ `cloak` (privacy/PII) ‖ `oath`? (compliance_checklist) ‖ `omen`+`ripple` (`risk_register.md`) | legal_considerations, data_rights_policy, privacy_policy_draft, terms_of_service_draft, cookie_policy_draft, risk_register, compliance_checklist |
| Testing | 10 | `matrix` qa-scenario (`test_cases.csv` TC-001…, mapped to feature_id) ‖ `radar`? (strategy) ‖ `mint` (`ai_evaluation_cases.csv`) | test_strategy, test_cases.csv, qa_checklist, ai_evaluation_cases.csv, performance_test_plan, security_test_plan, accessibility_test_plan, release_checklist |
| PM | 11 | `sherpa` (`backlog.csv` BL-001…, mapped to feature_id) ‖ `rank` (priority) ‖ `scribe` (RACI/milestones) | backlog.csv, milestones, team_structure, budget_estimate, raci_matrix, decision_log, meeting_cadence, outsourcing_plan |
| Mock Data | 12 | `mint` (fictional sample data only) | sample_users.json, sample_events.json, sample_content.csv, sample_notifications.json, sample_settings.json, sample_logs.json |
| Assets | 13 | `sketch` (image_generation_prompts) ‖ `canvas` (diagram_index) | README, icon_direction, image_generation_prompts, diagram_index |

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

### Phase 6: Package

Nexus internal (Bash):

1. Write the full `project_document_package/` tree to the working directory (UTF-8).
2. **Syntax lint** before zipping — JSON (`python3 -m json.tool` or `jq`), YAML (`python3 -c "import yaml,sys;yaml.safe_load(...)"`), SQL (basic parse), HTML/CSS (structural), CSV (header presence). Record results in `validation_report.md`.
3. `zip -r project_document_package_<slug>.zip project_document_package/` — zip name uses `[A-Za-z0-9_-]` only.
4. **Expansion test:** `unzip -l` the archive; report file count and top-level structure.
5. Ensure no secrets / API keys / real personal data / temp files are included.

## Traceability Anchor (core design constraint)

The single most important property is that **one canonical feature list flows through the entire package**. This is enforced structurally:

- Phase 2 is a **barrier** — the feature_id table (F-001…) is produced before any track that references features.
- ID formats are fixed: features `F-001`, test cases `TC-001`, backlog `BL-001`.
- The feature_id table is passed verbatim in every Phase 3 `_AGENT_CONTEXT` handoff (Testing, PM, KPI, UX, LP). Tracks must reference existing IDs, never mint new feature IDs.
- Phase 5 fails the package if any test case or backlog item references a non-existent feature_id, or any Must-have feature lacks a user story / AC / test case.

Without this barrier, parallel tracks would independently invent inconsistent feature sets — the dominant failure mode of naive "generate everything at once" prompts.

## Output and Packaging

- **Deliverable is a filesystem tree + zip**, not a chat-embedded "download link" (CLI has no download concept). The final report gives the **absolute path** to the zip.
- Directory structure matches the canonical layout exactly (`project_document_package/` with `00_overview` … `13_assets` + top-level `README.md`, `document_manifest.csv`, `validation_report.md`).
- `document_manifest.csv` columns: `path,title,purpose,target_reader,status,related_files,priority`.
- `risk_register.md` columns: `risk_id,category,description,likelihood,impact,mitigation,owner,status`.
- `test_cases.csv` columns: `id,feature_id,category,feature,scenario,precondition,steps,expected_result,priority`.
- `ai_evaluation_cases.csv` columns: `id,input,expected_behavior,risk_type,evaluation_criteria,pass_fail`.
- `backlog.csv` columns: `id,epic,feature_id,task,description,priority,owner,estimate,dependency,status`.
- `growth_experiments.md` items: `experiment_id,hypothesis,target_segment,channel,action,success_metric,duration,required_assets,priority`.

## Validation Contract

`validation_report.md` records:
- Directory/file completeness vs the depth tier's required set.
- MVP scope ↔ roadmap non-conflict.
- feature_catalog ↔ user_stories ↔ test_cases ↔ backlog correspondence (traceability matrix result).
- tech_stack ↔ database_schema.sql ↔ api_design_openapi.yaml coherence.
- LP copy ↔ brand strategy alignment.
- Legal/risk notes present; AI eval/guardrail/human-review present if AI is used.
- CSV header presence; JSON/YAML/SQL/HTML/CSS syntax validity (with the lint command results).
- Post-unzip usability (file count + structure from `unzip -l`).

## Conditional Inclusion

| Condition | Add | Skip |
|-----------|-----|------|
| depth = lite | — | 02, 06, 07-deep, 08, 09, 10, 11, 12, 13 (keep 00/01-lite/03/04-lite/05) |
| depth = full | void, oath, crypt, deeper scribe | — |
| mode includes ai-product | full 08 + ai_evaluation_cases + human_review | — (08 never skipped in this mode) |
| business_model = B2B / b2b-saas | oath, security_privacy deepened, sales_material, SLA in 11 | — |
| business_model = B2C / b2c-growth | 02 brand deep, 05 LP, SEO/social/onboarding in 06 | — |
| web_grounding = unavailable | research_todo.md (enumerate needed lookups, mark hypotheses) | live references.md sourcing |
| UI surface absent (API/infra product) | — | 04 UX, 05 LP (replace with API docs emphasis in 07) |
| Figma in workflow | frame (extract tokens) | — |

## AUTORUN Chain Template

```
Nexus AUTORUN venture idea="<X>" depth=<...> mode=<...>
  ── Phase 0 Framing ──────────────────────────────────
  → parse idea + condition fields → resolve depth/modes
  → web_grounding check
  → clarify gate (≤3 Qs only on domain/target/B2X-fork/high-risk/impermissible; else assume)
  → emit venture_contract
  ── Phase 1 Research ─────────────────────────────────
  → field(market+trend+JTBD, web-grounded|research_todo)
  ‖ compete(direct+indirect+diff)?        # skip at lite
  ‖ plea(user demands) → cast(personas)?  # cast if depth≥mvp
  ── Phase 2 Product Spine [BARRIER] ──────────────────
  → accord(PRD+stories+AC+IA+NFR+release)
  → spark(feature_catalog: F-001… + mvp_or_later)
  → rank(MoSCoW)  → pulse(KPI tree ↔ feature_id)?
  → void(YAGNI)?                          # depth=full or bloat
  → ═══ EMIT canonical feature_id table → bind to all Phase 3 ═══
  ── Phase 3 Parallel Doc Tracks (waves, feature_id-bound) ─
  → [Brand]  vision → muse(design_tokens.json) ‖ prose ‖ tone
  ‖ [UX]     palette ‖ canvas(mermaid) ‖ echo ‖ prose(states)
  ‖ [LP]     funnel(index.html+styles.css+copy) ‖ prose
  ‖ [Mktg]   funnel/bazaar ‖ pulse ‖ experiment(growth_experiments)
  ‖ [Tech]   atlas(arch+mermaid) → schema(schema.sql) ‖ gateway(openapi.yaml)
                                  ‖ beacon ‖ gear ‖ crypt?
  ‖ [AI]     oracle(policy+prompts+eval+guardrails+human_review)
  ‖ [Legal]  clause(ToS/Privacy/Cookie) ‖ cloak ‖ oath? ‖ omen+ripple(risk_register)
  ‖ [Test]   matrix qa-scenario(test_cases.csv TC-001 ↔ F-id) ‖ radar? ‖ mint(ai_eval_cases.csv)
  ‖ [PM]     sherpa(backlog.csv BL-001 ↔ F-id) ‖ rank ‖ scribe(raci/milestones)
  ‖ [Mock]   mint(sample_*.json/csv — fictional only)
  ‖ [Assets] sketch(image_prompts) ‖ canvas(diagram_index)
  ── Phase 4 Overview Synthesis (post-tracks) ─────────
  → spark(concept+one_page_pitch) ‖ scribe(exec_summary+decision+90day)
  → magi(coherence)?                      # depth≥raise
  ── Phase 5 Integrate + Validate ─────────────────────
  → attest/judge(traceability matrix + cross-doc consistency)
  → Nexus: document_manifest.csv + validation_report.md + README.md
  → format syntax lint (json/yaml/sql/html/css/csv-header)
  ── Phase 6 Package ──────────────────────────────────
  → write tree (UTF-8) → zip -r project_document_package_<slug>.zip
  → unzip -l expansion test → secrets/PII scrub check
  → report: zip path, file count, main contents, validation result, caveats
```

## Failure Escalation

| Failure | Detected by | Escalation |
|---------|-------------|------------|
| Business idea missing | Phase 0 | Ask for the idea — do not invent a venture |
| Domain unidentifiable / high-risk | Phase 0 clarify gate | Ask ≤3 questions with fallback assumptions stated |
| Phase 2 feature table incomplete | accord/spark | Block Phase 3; re-run spine — barrier must not be bypassed |
| Track references non-existent feature_id | Phase 5 traceability | Return that track for correction |
| MVP over-scoped (Won't-have leaked) | Phase 5 / void | Re-run rank or void, downgrade scope |
| tech_stack ↔ schema/API mismatch | Phase 5 | Return Tech track |
| LP copy ↔ brand mismatch | Phase 5 | Return LP/Brand track |
| Format syntax invalid | Phase 6 lint | Fix the file, re-lint before zipping |
| Secrets/PII detected in tree | Phase 6 scrub | Remove and re-package; never ship |

## Cost and Latency Profile

| Depth | Directories | Approx agents | Approx cost |
|-------|-------------|---------------|-------------|
| lite | 5 | 6-8 | Low |
| mvp (default) | 14 | 14-18 | Medium |
| raise | 14 (research/marketing/overview deep) | 16-20 | Medium-High |
| full | 14 + void/oath/crypt | 24-28 | High — **confirm before launch** |

Venture is not free. Budget guardrails (Nexus chain confirmation for 5+ agent chains, full-depth confirmation, no-secrets package scrub) are enforced. For repeated ventures with a stable house style, propose a Sigil-generated project skill to amortize the chain design cost. When a native Dynamic Workflow substrate is available, delegate the Phase 3 parallel sweep to it and keep Nexus as the feature_id-contract + validation layer.
