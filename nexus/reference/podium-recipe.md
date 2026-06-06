# Nexus Podium Recipe Reference

> **"Same source, two stages — the document the reader returns to, the deck the audience remembers."**
>
> **Default baseline: Claude + Codex (dual-engine).** agy is an **optional third axis** when AVAILABLE; dual-engine mode is fully supported and NOT degraded. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy`.

## Contents

- [Overview](#overview)
- [Invocation and Prerequisites](#invocation-and-prerequisites)
- [When to Use Podium](#when-to-use-podium)
- [Topology](#topology)
- [Engine × Team Matrix](#engine--team-matrix)
- [Phase Contracts](#phase-contracts)
- [Output Format Variants](#output-format-variants)
- [Cross-Engine Quorum Rules](#cross-engine-quorum-rules)
- [AUTORUN Chain Template](#autorun-chain-template)
- [Failure Escalation](#failure-escalation)
- [Cost and Latency Profile](#cost-and-latency-profile)
- [Comparison with Single-Skill / Atelier / Summit](#comparison-with-single-skill--atelier--summit)

---

## Overview

Podium is a **content-quality maximization recipe** for documentation and high-quality slide creation. It mobilizes five functional teams (Research / Narrative / Production / Verification / Improvement) across multiple engines to produce a **unified deliverable package** — typically a primary document plus a derived slide deck (or vice versa) — from a single source-of-truth outline.

Where `summit` triangulates strategic code decisions, podium triangulates **prose, narrative arc, visual asset, and format rendering** quality. The recipe is intentionally lighter than summit (15-40 agents vs 32-119) because content artifacts are lower-stakes than production code merges, and most polish iterations are cheap.

**Default baseline: Claude + Codex (dual-engine).** Claude owns prose, narrative judgment, story arc, audience walkthrough, and tone arbitration (irreducibly judgment-heavy). Codex owns code samples, diagram-as-code rendering, slide framework compilation (Marp/reveal.js/Slidev), and format conversion (Morph). agy is added as an optional third axis when AVAILABLE — it contributes long-context source synthesis (1M window for whole-codebase learning docs), multimodal asset reading (existing decks, screenshots, mockups), and AI image generation (Sketch/Ink hero imagery and illustrations).

**Key design decisions:**
- **Doc and Slide are produced in parallel from the same outline** — Phase 2 narrative locks the story arc, Phase 3 forks into Content / Visual / Layout tracks, and the slide deck cross-references the document.
- **Audience analysis is mandatory at Phase 1** (Field) — content without grounded audience model regresses to ChatGPT-residue prose. Echo is reserved for Phase 4 cognitive walkthrough on the finished artifact, not pre-task persona modeling.
- **6×6 rule and WPM budget are enforced at Phase 4** for slides (Stage agent contract).
- **Improvement loop is capped at 2 iterations** (vs summit's 3) — content polish converges faster than code polish; loops are arbitrated by magi.
- **User confirmation is recommended but not mandatory** — podium does not modify production code, so the cost ceiling is much lower than summit/apex. AUTORUN_FULL is acceptable when the user has already confirmed the goal.

---

## Invocation and Prerequisites

### Invocation

```
/nexus podium                          # Goal-supplied mode (current task context)
/nexus podium "<goal>"                 # Explicit goal mode
/nexus podium "<goal>" --format doc    # Force doc-only output
/nexus podium "<goal>" --format slide  # Force slide-only output
/nexus podium "<goal>" --format both   # Default: unified package
```

### Prerequisites (preflight, in Nexus main context)

| Prerequisite | Check | Failure Action |
|--------------|-------|---------------|
| `claude` binary | always available (host) | n/a |
| `codex` binary | `which codex` or fallback paths | warn and continue (Codex tasks fall back to Claude with cost note); abort only if user requested explicit Codex-bound output (slide compilation, large diagram rendering) |
| `agy` binary | `which agy` or fallback paths | **OPTIONAL** — record verdict (AVAILABLE / UNAVAILABLE / RUNTIME-BROKEN). UNAVAILABLE switches to dual-engine; does NOT abort |
| Output format declared | `--format` flag OR detected from goal text | default to `both` if ambiguous |
| Audience profile producible | Phase 1 must produce non-trivial audience model | warn but continue with "generic technical audience" default |

**Why podium has weaker prereqs than summit:** podium produces content artifacts (documents, slides) rather than code changes. Single-engine fallback degrades polish but not correctness. Summit's strict tri-engine requirement was designed for high-stakes code triangulation; podium does not need that level of redundancy.

---

## When to Use Podium

### Use Podium for

- Conference talks and keynote decks where audience impression carries the work
- Onboarding materials that mix written tutorial + companion slides
- Design system documentation (component catalog with usage examples + introduction deck)
- Architecture documentation (ADR/RFC/HLD/LLD with stakeholder presentation deck)
- Technical announcements / launch materials (blog post + sales deck + internal demo)
- Learning materials derived from repo diffs (tome-style learning doc + workshop slides)
- Project retrospectives shipped as both long-form post and exec summary deck
- Public-facing tech articles where visuals and narrative arc carry the message

### Do NOT use Podium for

- Single specification document with no visual / slide need → `scribe` directly
- Single article with no slide derivative → `zine` directly
- Single slide deck with simple structure → `stage` directly
- Code-adjacent docs (JSDoc, README) → `quill` directly
- UX microcopy / error messages → `prose` directly
- Diagrams in isolation → `canvas` directly
- Format conversion of an existing finished document → `morph` directly
- Strategic code decisions → `summit`
- UI design pipeline → `atelier`

### Do NOT use Podium when

- The goal is unclear and no audience can be defined even loosely
- The output target system is not supported by any rendering agent (escalate to user for fallback format)

---

## Topology

```
                  ┌──────────────────────────────────┐
                  │       Nexus (Claude, hub)        │
                  └────────────────┬─────────────────┘
                                   │
       ┌───────────────────────────┼───────────────────────────┐
       │                           │                           │
   Phase 0                     Phase 1                     Phase 2
   FRAMING                     RESEARCH                    NARRATIVE
   (Claude)                    (parallel ‖)                (Claude)
       │                           │                           │
       ▼                           ▼                           ▼
  content_charter        research_brief.json            narrative_lock.yaml
                                                               │
                                                               ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 3 PRODUCTION (3 tracks ‖)     │
                                    │  ┌──────────────────────────────┐    │
                                    │  │ TRACK A: CONTENT             │    │
                                    │  │  Claude judgment-heavy:      │    │
                                    │  │  scribe/zine/prose/saga      │    │
                                    │  │  Codex: quill (code samples) │    │
                                    │  │  agy: tome (long-ctx body)   │    │
                                    │  └──────────────────────────────┘    │
                                    │  ┌──────────────────────────────┐    │
                                    │  │ TRACK B: VISUAL              │    │
                                    │  │  Codex: canvas, vitrine     │    │
                                    │  │  agy: sketch, ink, frame     │    │
                                    │  │  Claude: vision (direction)  │    │
                                    │  └──────────────────────────────┘    │
                                    │  ┌──────────────────────────────┐    │
                                    │  │ TRACK C: LAYOUT / FORMAT     │    │
                                    │  │  Codex: stage, morph         │    │
                                    │  │  agy: figma:figma-use-slides │    │
                                    │  └──────────────────────────────┘    │
                                    │  Convergence: doc ↔ slide cross-refs │
                                    └──────────────────────────────────────┘
                                                               │
                                                               ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 4 VERIFICATION (parallel ‖)   │
                                    │  ├─ Nexus[claim grounding scan]      │
                                    │  ├─ canon (style / brand / a11y)     │
                                    │  ├─ echo (audience walkthrough)      │
                                    │  ├─ palette (visual a11y for slides) │
                                    │  ├─ voyager (slide render check)     │
                                    │  └─ judge (multi-engine review)      │
                                    └──────────────────────────────────────┘
                                                   │
                                  CONFIRMED/LIKELY findings
                                                   │
                                                   ▼
                                    ┌──────────────────────────────────────┐
                                    │  Phase 5 IMPROVEMENT LOOP (max 2×)   │
                                    │  ├─ prose (microcopy polish)         │
                                    │  ├─ canvas (diagram fixes)           │
                                    │  ├─ stage (slide layout)             │
                                    │  ├─ zine/scribe (prose tightening)   │
                                    │  └─ magi arbitrates                  │
                                    └──────────────────────────────────────┘
                                                               │
                                                               ▼
                                                          Phase 6
                                                          PUBLISH
                                              (Morph + Guardian + Launch?)
                                                               │
                                                               ▼
                                                   NEXUS_COMPLETE
```

---

## Engine × Team Matrix

| | Claude (hub — narrative, judgment, audience) | Codex (sandbox — code samples, rendering, compilation) | Antigravity / agy (long-context, multimodal, AI imagery) |
|---|---|---|---|
| **Research** | Lens (codebase mapping for technical docs), Harvest (PR-derived material) | Quill (extract from JSDoc / existing API docs) | Field (audience persona + Search-grounded external sources), Tome (1M-context git-diff → learning material), Frame (multimodal extract from existing decks/screenshots) |
| **Narrative** | Accord (L0-L1 staged elaboration), Zine (story arc for articles), Scribe (spec structure), Stage (slide narrative arc), Cue (storyboard for presentation-heavy work), Magi (depth vs breadth arbitration), Void (scope cut) | — | — |
| **Production: Content** | Scribe (PRD/SRS/HLD/LLD body), Zine (article body + hook), Prose (microcopy, headings, CTAs), Saga (product narrative) | Quill (code samples with proper JSDoc/TSDoc), Vitrine (component usage examples) | Tome (long-ctx learning-doc body), Scribe[long-ctx] (large spec bodies > 200K tokens) |
| **Production: Visual** | Vision (visual direction), Muse (brand tokens application) | Canvas (Mermaid / draw.io diagram code), Vitrine (Storybook-style examples), Dot (pixel art via code) | Sketch (Gemini-native hero / cover / illustration imagery), Ink (SVG icon system), Frame (multimodal context extraction from existing visual references) |
| **Production: Layout** | Prism (NotebookLM steering prompt design) | Stage (Marp / reveal.js / Slidev compilation), Morph (intermediate MD ↔ DOCX/PPTX/PDF/HTML conversion) | `figma:figma-use-slides` (Figma Slides — when target is Figma) |
| **Verification** | Echo (persona walkthrough on finished artifact), Vision (design direction review), Magi (verdict arbitration), Nexus[claim-grounding scan] (token-level cross-reference between artifact claims and research_brief.source_facts — kept inside Nexus rather than spawned, see Phase 4) | Voyager (slide render-and-screenshot check), Radar?[testable assertions in technical docs] | Canon (style / brand / WCAG-AA / ISO 25010 compliance), Palette (visual a11y from screenshots), Attest (only when the artifact is itself a spec being verified against a separate normative document — otherwise claim-grounding stays in Nexus) |
| **Improvement** | Prose (microcopy polish), Zine (prose tightening), Scribe (spec body refinement), Vision (design direction refinement), Magi (improvement-selection arbitration) | Canvas (diagram fixes), Stage (slide layout adjustment), Morph (re-render), Quill (code sample cleanup) | Sketch (re-generate imagery if rejected), Tome (re-extract from updated diff) |

**Cross-engine routing rules:**
- If a task **generates prose, narrative, or judgment** → Claude (irreducibly judgment-heavy)
- If a task **compiles or renders structured content** (slide framework, format conversion, diagram-as-code) → Codex
- If a task **needs > 200K tokens of source context** (whole codebase / large repo diff / multiple long specs) → agy
- If a task **generates or extracts from images** (AI imagery, mockup reading, screenshot analysis) → agy
- If a task **requires explicit creative divergence** (alternative hero imagery, alternative slide concepts) → agy via rally[engine-paradigm COMPETE]
- If `agy` is UNAVAILABLE, agy-bound tasks fall back: AI imagery → skipped with placeholder (user adds later), long-ctx → Claude with `sonnet` 1M variant if doc fits, multimodal → Claude vision

**Engine distribution targets (dual-engine baseline):**

| Engine | Target share of total agent-minutes | Rationale |
|--------|-------------------------------------|-----------|
| **Claude** | ~45-50% | Prose / narrative / judgment / audience — irreducible |
| **Codex** | ~30-35% | Rendering / compilation / code samples / format |
| **agy** | ~15-25% | When AVAILABLE: imagery + long-ctx; when UNAVAILABLE: absorbed by Claude |

Phase 6 PUBLISH includes an "Engine Distribution Audit" in the execution report so engine drift can be detected.

---

## Phase Contracts

### Phase 0: Framing (Claude only, 1-2 agents, 3-5 min)

**Input:** User request (`/nexus podium "<goal>"` with optional `--format`)

**Agents:**
1. Nexus[classify] — output format detection (doc / slide / both), depth, brand context
2. Accord[L0 vision] — staged elaboration of goal and audience (skip if user gave explicit charter)

**Output:** `content_charter.yaml`

```yaml
goal: "<explicit content goal>"
mode: greenfield | refresh               # greenfield = new artifact; refresh = improve existing doc/deck
existing_assets:                         # required when mode == refresh; ignored when greenfield
  - { path_or_url: "...", role: primary_doc | primary_deck | reference | brand_sample }
output_format: doc | slide | both        # default: both
primary_artifact: doc | slide            # which is canonical when both
audience:
  who: "<persona summary>"
  knowledge_level: novice | intermediate | expert | mixed
  expected_attention_minutes: N          # for slides; or reading_time_minutes for docs
brand:
  tone: technical | editorial | playful | formal | mixed
  visual_language: "<reference link or 'derive from existing assets'>"
  forbidden_phrases: ["In this article we will", "Recently, X has been trending", "delve into", ...]   # user supplies language-specific banned phrases; substitute the matching set for non-English content
constraints:
  page_or_slide_budget: N                # hard cap
  embargo_or_deadline: "<ISO date or null>"
  forbidden_topics: [...]
materialize_images: true | false         # if true, Phase 6 runs Sketch-authored generation code; if false, ship code only
cost_budget:
  max_agents: 53
  max_wall_time_minutes: 130
  max_loops: 2
risk_tier: routine | external-facing | release-critical
user_acknowledged: true | false
```

**Mode behavior:**
- `greenfield` — Phase 1 builds source/audience from scratch. Frame and Tome run only if the user provides reference materials (codebase, market sources).
- `refresh` — Phase 1 mandatorily runs Frame (multimodal extraction from `existing_assets` of role `primary_deck` or `brand_sample`) and/or scribe-equivalent extraction for `primary_doc`. Phase 2 Narrative team is instructed to preserve the existing story spine unless Phase 4 verification flags a CRITICAL issue with it. Improvement loops favor surgical edits over rewrites.

**Gate:** If `risk_tier == release-critical` (external press, regulatory, customer-facing keynote) → require explicit user confirmation before proceeding.

---

### Phase 1: Research Team (parallel, 3-6 agents, 5-12 min)

**Input:** `content_charter.yaml`

**Parallel branches (engine-strength routing):**

```yaml
parallel:
  - branch: audience_grounding
    engine: agy | claude          # agy preferred for fresh Search grounding
    agents: [field]
    mission: build the audience persona — who they are, what they already know, what they care about, what makes them tune out. Field (not Echo) owns this because the work is grounded fact-gathering about a target population, not UI walkthrough simulation. Echo is reserved for Phase 4 cognitive walkthrough on the finished artifact.
    output: audience_brief.json

  - branch: source_aggregation
    engine: claude | codex
    agents:
      - lens          # if technical doc derived from codebase
      - harvest       # if release notes / PR-derived
      - quill         # if API docs / JSDoc extraction
    mission: gather and validate primary source material from internal systems
    output: source_brief.json

  - branch: long_context_synthesis     # conditional: agy AVAILABLE AND large source
    engine: agy
    agents: [tome, frame]
    mission: 1M-ctx synthesis of large diffs / long specs / multimodal references; Frame extracts context from existing decks or screenshots when `mode == refresh`
    output: agy_research.json

  - branch: external_grounding         # conditional: external-facing content
    engine: agy | claude
    agents: [field]
    mission: web/external grounding via Search; market positioning if announcement (this is a second Field invocation focused on external positioning, separate from the audience_grounding branch)
    output: external_brief.json
```

**Synthesis:** Nexus aggregates branches into `research_brief.json` with source attribution per fact.

**Output:** `research_brief.json`
```yaml
audience_model: {...}
source_facts:
  - { claim: "...", source: "...", confidence: 0.0-1.0 }
key_quotes: [...]
visual_references: [...]
gaps_to_address: [...]     # facts requested but not findable — Phase 2 must decide how to handle
```

**Gate:** If `gaps_to_address.critical > 0` → pause, present to user before Phase 2 (typical critical gap: "we claim a 40% improvement but no source backs it").

---

### Phase 2: Narrative Team (Claude, 2-4 agents, 5-10 min)

**Input:** `content_charter.yaml` + `research_brief.json`

**Agents (route by output_format):**

| output_format | Primary agent | Secondary agents |
|---------------|--------------|-----------------|
| `doc` (article/blog) | Zine[story arc] | Prose[hook], Accord[L1 outline], Magi[depth-vs-breadth] |
| `doc` (technical spec) | Scribe[structure] | Accord[L1 outline], Void[scope cut], Magi |
| `doc` (learning material) | Tome[narrative] | Scribe[structure], Zine[hook], Magi |
| `slide` | Stage[narrative arc] | Cue[storyboard], Prose[slide titles], Magi |
| `both` | Stage[arc] ‖ Zine/Scribe/Tome[arc] | Cue, Prose, Magi[arbitrate cross-format alignment] |

**Process:**
1. Each primary agent produces a narrative arc skeleton tailored to its format
2. When `output_format == both`, Magi runs a **convergence check**: doc and slide must share the same story spine (Problem → Tension → Insight → Solution → CTA, or equivalent for the genre) but differ in depth and cadence
3. Void aggressively cuts scope when over budget — slide deck loses ~30% breadth vs the doc by default
4. Prose locks page/slide titles and section headings against the agreed arc

**Output:** `narrative_lock.yaml`
```yaml
story_spine:
  pattern: "Problem-Tension-Insight-Solution-CTA" | "Tutorial" | "Listicle" | ...
  beats:
    - id: B1
      role: hook
      doc_treatment: "<2-3 sentence treatment>"
      slide_treatment: "<title + 1-line subtitle>"
      duration_or_pages: "<seconds for slide / paragraphs for doc>"
    - id: B2
      ...
budget_distribution:
  doc:   { sections: N, target_word_count: N }
  slide: { count: N, total_minutes: N, wpm: 140 }
visual_anchors:
  - { beat_id: B1, type: hero-image | diagram | screenshot | icon-grid, brief: "..." }
cross_references:
  - { doc_section: "...", slide_index: N }
```

**Gate:** Narrative lock is the cross-format contract — once signed off, Phase 3 tracks proceed in parallel and may not redesign the spine without restarting Phase 2.

---

### Phase 3: Production Team (3 parallel tracks, 6-18 agents, 15-45 min)

When `output_format == both`, three tracks run concurrently and converge via cross-reference resolution. When `doc` only, Track C runs only Morph (no Stage). When `slide` only, Track A focuses on slide-body content (no long-form doc body).

---

**Track A: Content** (3-7 agents, 10-30 min) — Claude-heavy

```yaml
content_track:
  coordinator: nexus (no agent-coordinator; nexus aggregates)
  parallel:
    - branch: prose_body
      engine: claude
      agents (route by format):
        - { if: article,         use: [zine] }
        - { if: technical_spec,  use: [scribe] }
        - { if: learning,        use: [tome, scribe] }
        - { if: product_story,   use: [saga] }
      mission: produce body prose tied to narrative_lock beats
      output: body_doc.md

    - branch: slide_body
      engine: claude
      agents: [cue, prose]
      mission: slide-by-slide content blocks (titles + bullets + speaker notes) authored from the storyboard. Cue owns narrative beats and speaker notes; Prose owns slide titles and bullet phrasing. Stage is NOT used at this branch — Stage's job is compilation (Track C), not content-only authoring
      output: slide_content.yaml

    - branch: code_samples
      engine: codex
      agents: [quill, vitrine]
      mission: verified, compilable code samples with proper JSDoc/TSDoc; component usage examples
      output: code_blocks.json

    - branch: long_context_body          # conditional: agy AVAILABLE AND large source
      engine: agy
      agents: [tome, scribe]
      mission: long-ctx body (whole-codebase learning doc, multi-spec reconciliation)
      output: long_body.md
```

**Track B: Visual** (2-6 agents, 8-25 min)

```yaml
visual_track:
  coordinator: vision (claude — direction only)
  parallel:
    - branch: direction
      engine: claude
      agents: [vision, muse]
      mission: visual language direction + token application
      output: visual_direction.yaml

    - branch: diagrams_as_code
      engine: codex
      agents: [canvas, vitrine]
      mission: Mermaid / draw.io / Storybook examples for each visual_anchor of type diagram or component
      output: diagrams/ (set of .mmd / .drawio / .stories.tsx)

    - branch: imagery
      engine: agy
      agents: [sketch, ink]
      mission: |
        Sketch produces Gemini-API image-generation CODE (Python/JS) for hero/cover/illustration imagery — it does NOT itself emit PNG files.
        Ink produces SVG icon system source directly (SVG is code).
        For visual_anchors of type image: Sketch authors `gen_<anchor_id>.py` (or .js); Phase 6 PUBLISH executes the code under the user's GEMINI_API_KEY to materialize `assets/<anchor_id>.png` (or skip+placeholder if the user defers execution).
        For visual_anchors of type icon: Ink emits `assets/<icon>.svg` directly with no execution step needed.
      output: |
        image_generation_code/  (Python/JS files from Sketch — runnable but not yet run)
        assets/icons/           (SVG files from Ink — final form)
      materialization_step: Phase 6 PUBLISH runs `image_generation_code/*` if `--materialize-images` flag is set; otherwise PR/output preserves the code and Phase 6 records a `#TODO(user): run scripts under GEMINI_API_KEY` note in the execution report
      fallback_if_agy_unavailable: Sketch and Ink skipped — placeholder TODO with image_brief.txt for the user to author manually
```

**Track C: Layout / Format** (1-4 agents, 5-15 min)

```yaml
layout_track:
  coordinator: nexus
  agents:
    - if: output_format includes slide
      use: [stage]
      engine: codex
      mission: compile slide_content.yaml + assets + diagrams into Marp/reveal.js/Slidev project
      output: slides/ (runnable slide project)

    - if: output_format includes doc AND target_format in {DOCX, PPTX, PDF, HTML}
      use: [morph]
      engine: codex
      mission: cross-format conversion (intermediate MD → target)
      output: dist/

    - if: target_platform == Figma Slides
      use: [figma:figma-use-slides]
      engine: agy (or claude if agy UNAVAILABLE)
      mission: Figma Slides deck via Figma MCP (the skill is namespaced under the figma plugin — must invoke as `figma:figma-use-slides`, not bare `figma-use-slides`)
      output: figma_slides_url
```

**Convergence step (after all three tracks complete):**

1. Nexus merges `body_doc.md` + `slide_content.yaml` + `assets/` + `diagrams/` + `image_generation_code/` into the slide framework via Stage
2. Cross-references in `narrative_lock.yaml` are resolved (doc section ↔ slide index)
3. Code samples (Track A) are injected into both doc and slide layouts
4. Visual direction (Track B) is applied to slide theme
5. File-level conflicts resolved via `_common/PARALLEL.md` ownership rules

**Engine attribution tagging (per file, mandatory):** every file produced in Phase 3 is tagged in `manifest.yaml` with the engine that produced it: `[claude-prose]`, `[claude-cue]`, `[codex-canvas]`, `[codex-stage]`, `[codex-quill]`, `[agy-sketch]`, `[agy-ink]`, `[agy-frame]`, `[agy-tome]`. The manifest feeds Phase 6's Engine Distribution Audit and lets the user trace any quality issue back to the engine that owned the file. Files touched by multiple engines list all attributions in order of contribution magnitude.

**Checkpoint:** after each track completes, persist outputs (Core Rule: 4+ step chains need checkpoint-resume).

**Output:** working doc artifact + working slide deck + asset bundle + cross-reference map.

---

### Phase 4: Verification Team (parallel, 3-6 agents, 8-20 min)

**Parallel branches:**

```yaml
parallel:
  - branch: claim_grounding
    engine: agy | claude
    owner: nexus (internal check, not a spawned specialist)
    mission: every factual claim in body must trace back to a row of research_brief.source_facts. Nexus reads the produced body + slide_content and does direct token-level cross-reference against source_brief.json + agy_research.json. Optionally promote to `attest` ONLY when the artifact is itself a spec being verified against a separate normative document (e.g., "this onboarding doc claims to teach API X, verify all claims match the API X spec") — in that case attest's spec-compliance contract applies; otherwise the check is plain grounded-claim verification and stays in Nexus
    output: claim_audit.json

  - branch: style_brand_a11y
    engine: claude | agy
    agents: [canon]
    mission: brand tone compliance + WCAG-AA for slides + forbidden_phrases scan + 6×6 rule + WPM budget check
    output: compliance_report.json

  - branch: audience_walkthrough
    engine: claude
    agent: echo
    mission: persona walks through final artifact (read doc front-to-back / sit through slide deck); reports friction, jargon density, hook strength, CTA clarity
    output: persona_friction.json

  - branch: visual_a11y
    engine: agy
    agent: palette
    mission: contrast / readability / scale / motion safety on rendered slides (multimodal screenshot read)
    output: visual_a11y.json

  - branch: render_check
    engine: codex
    agent: voyager (or stage in dry-run mode)
    mission: slide framework actually compiles and previews; doc target formats actually render (DOCX/PPTX/PDF open without errors)
    output: render_log.json

  - branch: multi_engine_review
    engine: judge (built-in multi-engine fan-out)
    mission: overall quality review — prose quality, narrative coherence, slide impact
    output: judge_findings.json
```

**Quorum rules:** same labeling as summit (CONFIRMED / LIKELY / CANDIDATE / MINORITY) but applied to content findings:

| Concurrence | Finding Severity | Action |
|-------------|------------------|--------|
| CONFIRMED (≥3 branches agree) | CRITICAL (claim ungrounded, render-broken, brand violation, persona blocker) | Force Phase 5 |
| CONFIRMED | HIGH (clarity, hook weak, slide overrun) | Force Phase 5 |
| LIKELY (2 branches agree) | CRITICAL or HIGH | Force Phase 5 |
| LIKELY | MEDIUM | Annotate, deliver with caveat |
| CANDIDATE (1 branch) | any | Grounding verification by Nexus → if VERIFIED → treat as LIKELY |

**Specific gates:**
- `claim_audit.json`: zero un-cited factual claims allowed in `risk_tier ∈ {external-facing, release-critical}`
- `compliance_report.json`: zero `forbidden_phrases` matches; WCAG-AA contrast ≥ 4.5:1 for body text on slides
- `persona_friction.json`: no "tune-out point" reported within first 3 slides or first 200 words of doc
- `render_log.json`: zero compilation errors; preview generates without crash

**Output:** `verification_report.md` with engine-attributed findings and quorum verdict.

---

### Phase 5: Improvement Team (PDCA loop, 2-5 agents per loop, max 2 loops)

**Driver:** orbit (autonomous loop runner) — same as summit but capped at 2 iterations

**Per-loop process:**

```yaml
loop_iteration:
  parallel_improvement_proposals:
    - branch: prose_polish
      engine: claude
      agents: [prose, zine, scribe]
      mission: tighten body, remove ChatGPT-residue, strengthen hook, adjust pacing
      output: prose_diffs.md

    - branch: visual_fixes
      engine: codex | agy
      agents: [canvas, sketch, ink]
      mission: redraw diagrams flagged unreadable; regenerate imagery flagged off-brand
      output: visual_diffs.json

    - branch: layout_adjustment
      engine: codex
      agents: [stage, morph]
      mission: slide layout adjustments (over-budget cuts, framework re-themes); format-conversion fixes
      output: layout_diffs.json

    - branch: direction_refinement       # if visual a11y or brand violations
      engine: claude
      agent: vision
      mission: tighten visual direction; update muse tokens if brand mismatch

  arbitration:
    agent: magi
    role: select-improvements-to-apply (prioritize CRITICAL > HIGH > MEDIUM; reject style-only loops)
    output: applied_improvements.yaml

  apply_loop:
    if applied_improvements.non_empty:
      → Phase 3 (re-execute affected tracks only — not full Phase 3 rerun)
      → Phase 4 (re-verify affected gates)
      → check Phase 4 quorum:
          if CONFIRMED/LIKELY CRITICAL still present → next iteration (up to max_loops)
          else → exit loop, proceed to Phase 6
    else:
      → exit loop, proceed to Phase 6
```

**Circuit breakers:**

| Condition | Action |
|-----------|--------|
| `loop_count >= 2` (default max) | Exit loop, deliver with caveat about remaining issues |
| Agent Tennis: prose ↔ canon disagreement 3+ turns | Trip breaker, escalate prose-style dispute to user |
| Magi rejects all proposed improvements as style-only | Exit loop, treat as converged |
| All CRITICAL / HIGH findings resolved | Exit loop early (success path) |

---

### Phase 6: Publish (Claude + Codex, 1-4 agents, 3-10 min)

**Agents:**
1. **Image materialization (conditional)** — if `--materialize-images` flag AND `image_generation_code/` exists from Track B Visual: run the Sketch-authored scripts under the user's `GEMINI_API_KEY` to produce final `assets/<anchor>.png`. Owned by Nexus (Bash execution), not a separate spawned agent. If the flag is omitted, the code is kept as-is and a `#TODO(user): execute image_generation_code/*` note is added to the execution report.
2. Morph[finalize] — produce all target formats (MD/DOCX/PPTX/PDF/HTML) and bundle. Runs AFTER image materialization so that final imagery is embedded in PPTX/PDF (otherwise placeholders ship).
3. Guardian[PR-prep] — when artifact is committed to repo: classify changes, commit strategy
4. Launch[release-plan] — when artifact is a release announcement: versioning, CHANGELOG section, embargo handling

**Output:** `NEXUS_COMPLETE` with the full evidence trail:

```markdown
## Nexus Execution Report

Task: <goal>
Chain: podium (5-team, dual-engine | tri-engine)
Mode: AUTORUN_FULL

### Output Artifacts
- Primary doc:   <path>           [format: <type>]
- Slide deck:    <path or URL>    [framework: Marp | reveal.js | Slidev | Figma]
- Asset bundle:  <path>            [N images, M diagrams, K icons]
- Distribution:  [DOCX, PPTX, PDF, HTML] generated in dist/

### Phase Results
| Phase | Status | Engine Attribution | Key Output |
| ...

### Engine Contributions
- Claude:    <prose / narrative / direction / audience>
- Codex:     <slide compilation / diagrams / format conversion / code samples>
- agy:       <imagery / long-ctx synthesis / multimodal extraction>  [or "skipped — UNAVAILABLE"]

### Quorum Summary
- CONFIRMED findings:   N (all resolved | N remaining)
- LIKELY findings:      N
- Minority signals:     N

### Improvement Loop Summary
- Loops executed:       N / 2
- Improvements applied: N
- Circuit breaker:      yes / no

### Verification
- Claim grounding:      N un-cited claims (0 in external-facing)
- Brand compliance:     pass / fail (forbidden phrases: N)
- 6×6 / WPM budget:     pass / fail
- WCAG-AA contrast:     pass / fail
- Render:               doc OK, slide OK
- judge:                N findings (severity breakdown)
- Persona walkthrough:  N friction points

### Engine Distribution Audit
- Claude:  X% (target ~45-50%)
- Codex:   X% (target ~30-35%)
- agy:     X% (target ~15-25%)
- Drift:   within | outside target

### Summary
<status, recommended next steps, follow-ups>

### Cost
- Wall time:        N minutes
- Total agents:     N
- Estimated tokens: ~N K
```

---

## Output Format Variants

| `--format` flag | output_format | Track A | Track B | Track C |
|----------------|---------------|---------|---------|---------|
| `doc` (or detected article/blog/spec) | doc only | body_doc.md only | full | Morph (no Stage) |
| `slide` (or detected deck/keynote) | slide only | slide_content.yaml only | full | Stage only |
| `both` (default) | both | body_doc.md + slide_content.yaml | full | Stage + Morph |
| `notebooklm` | doc + NotebookLM input | body_doc.md | full | Prism + Morph |
| `figma-slides` | slide via Figma | slide_content.yaml | full | `figma:figma-use-slides` + Stage (fallback) |

**Primary artifact rule:**
- `output_format == doc` → doc is canonical, slide is optional summary
- `output_format == slide` → slide is canonical, doc is optional reading material
- `output_format == both` → user declares `primary_artifact` in charter; if omitted, default to slide (slide narrative drives), but cross-references are bidirectional

---

## Cross-Engine Quorum Rules

Applied in Phase 4 (Verification). Same labels as summit; treatment adapted for content findings.

| Label | Definition | Default Trust |
|-------|------------|---------------|
| CONFIRMED | 3+ verification branches independently surface the same finding | High — proceed without grounding |
| LIKELY | 2 branches surface the same finding | Medium — proceed but flag |
| CANDIDATE | 1 branch surfaces a finding | Low — requires grounding verification by Nexus before action |
| MINORITY | 1 branch surfaces a finding that other branches explicitly considered and rejected | Very low — log as transparency, do not act |

### Grounding verification protocol (for CANDIDATE findings)

Nexus (in main context) reads the actual artifact section referenced by the finding and classifies:

| Verdict | Definition | Treatment |
|---------|------------|-----------|
| VERIFIED | Finding accurately describes a real issue | Promote to LIKELY |
| REJECTED | Finding does not match artifact reality | Discard, log as engine false positive |
| MITIGATED | Finding describes a real issue addressed elsewhere | Discard with note |
| STYLE-ONLY | Finding is preference, not correctness or clarity | Discard unless Phase 5 has spare loop budget |
| NEEDS-INFO | Cannot verify without external context | Escalate to user |

---

## AUTORUN Chain Template

```yaml
recipe: podium
mode: AUTORUN_FULL
required_confirmation: false   # only required for risk_tier == release-critical
prerequisites:
  - claude_available: true
  - codex_available:  true (warn if false, fall back to Claude)
  - agy_available:    optional (record verdict, dual-engine mode if false)
  - cost_acknowledged: optional

phase_chain:
  - phase: 0_framing
    agents: [nexus.classify, accord]
    engine: claude
    duration_minutes: [3, 5]
    gate: if risk_tier == release-critical → user_confirmation

  - phase: 1_research
    parallel:
      - { engine: agy | claude, agents: [field], mission: audience persona grounding }
      - { engine: claude | codex, agents: [lens, harvest, quill] }   # source aggregation
      - if: agy AVAILABLE AND (source_size > 200K_tokens OR mode == refresh)
        parallel_sub:
          - { engine: agy, agents: [tome, frame] }
      - if: external_facing
        parallel_sub:
          - { engine: agy | claude, agents: [field], mission: external positioning grounding }
    synthesis: nexus_aggregate
    duration_minutes: [5, 12]
    gate: gaps_to_address.critical == 0

  - phase: 2_narrative
    engine: claude
    agents_route_by_format:
      doc_article:   [zine, prose, accord, magi]
      doc_technical: [scribe, accord, void, magi]
      doc_learning:  [tome, scribe, zine, magi]
      slide:         [stage, cue, prose, magi]
      both:          [zine | scribe | tome, stage, cue, prose, magi]
    duration_minutes: [5, 10]
    gate: narrative_lock.yaml signed off

  - phase: 3_production
    parallel_tracks:
      - track: content
        parallel:
          - { engine: claude, agents: [zine | scribe | tome | saga] }
          - { engine: claude, agents: [cue, prose], mission: slide content blocks (titles + bullets + speaker notes) — Stage is NOT used here, only at Track C for compilation }
          - { engine: codex,  agents: [quill, vitrine] }
          - if: agy AVAILABLE AND long_context
            parallel_sub: { engine: agy, agents: [tome, scribe] }
      - track: visual
        coordinator: vision (claude)
        parallel:
          - { engine: claude, agents: [vision, muse] }
          - { engine: codex,  agents: [canvas, vitrine] }
          - if: agy AVAILABLE
            parallel_sub: { engine: agy, agents: [sketch, ink] }
      - track: layout
        agents_by_target:
          - if: includes_slide,         use: [stage],      engine: codex
          - if: target_format_needed,   use: [morph],      engine: codex
          - if: target == figma_slides, use: [figma:figma-use-slides], engine: agy
    convergence: cross_reference_resolution
    duration_minutes: [15, 45]
    checkpoint: after_each_track

  - phase: 4_verification
    parallel:
      - { owner: nexus_internal, scan: claim_grounding_token_cross_reference }
      - { engine: agy | claude,  agent: attest, if: artifact_is_spec_verified_against_normative_doc }
      - { engine: claude | agy,  agent: canon }
      - { engine: claude,        agent: echo }
      - { engine: agy,           agent: palette }
      - { engine: codex,         agent: voyager (or stage --dry-run) }
      - { agent: judge, mode: multi-engine-builtin }
    quorum: cross_branch
    duration_minutes: [8, 20]

  - phase: 5_improvement
    driver: orbit
    max_loops: 2
    arbiter: magi
    circuit_breakers:
      - agent_tennis_3_turns
      - magi_rejects_all_proposals
      - loops_exceeded
    per_loop_minutes: [8, 15]

  - phase: 6_publish
    agents: [morph, guardian?, launch?]
    engine: codex + claude
    output: NEXUS_COMPLETE
    duration_minutes: [3, 8]
```

---

## Failure Escalation

| Failure | Detection Phase | Mitigation | Escalation Threshold |
|---------|----------------|-----------|--------------------|
| codex unreachable | Preflight | Warn; Codex tasks fall back to Claude (cost note in report) | Continue |
| agy unreachable | Preflight | Switch to dual-engine; imagery skipped with placeholder TODO | Continue |
| `gaps_to_address.critical > 0` | Phase 1 | Pause, present to user — typical: "claim has no source" | Immediate |
| narrative_lock not signed off after 2 attempts | Phase 2 | Escalate to user — usually means goal is too broad | Immediate |
| render fails | Phase 4 | Force Phase 5 loop with stage + morph re-run | Always |
| Brand `forbidden_phrases` match in external-facing | Phase 4 | Force Phase 5 loop with prose rewrite | Always |
| Persona reports tune-out in first 3 slides | Phase 4 | Force Phase 5 loop with stage + prose rewrite | Always |
| WCAG-AA contrast fail | Phase 4 | Force Phase 5 with muse + palette + vision | Always |
| Loop count >= 2 with CRITICAL still present | Phase 5 exit | Deliver with explicit "unresolved CRITICAL" caveat | Always |
| Agent Tennis (prose ↔ canon 3+ turns) | Phase 5 loop | Circuit breaker, escalate prose-style dispute to user | Always |
| Total wall time > 2× estimate | Per-phase | Pause, present time-vs-quality trade-off to user | Always |

**Hard rule:** podium does NOT silently degrade quality. If a CRITICAL claim cannot be grounded and the user cannot supply a source, the artifact is delivered with that claim explicitly marked `[UNVERIFIED]` rather than removed silently — transparency over cosmetic completeness.

---

## Cost and Latency Profile

### Per-phase profile (both formats; subtract slide-only or doc-only agents as appropriate)

| Phase | Agents (both / single) | Parallel | Wall Time | Tokens |
|-------|------------------------|----------|-----------|--------|
| 0 FRAMING | 1-2 / 1-2 | 1 | 3-5 min | ~20K |
| 1 RESEARCH | 4-8 / 3-5 | 3-4 | 5-12 min | ~150-250K |
| 2 NARRATIVE | 3-5 / 2-4 | 1 | 5-10 min | ~80K |
| 3 PRODUCTION | 8-18 / 5-12 | 3 tracks | 15-45 min | ~350-900K |
| 4 VERIFICATION | 4-6 / 4-5 | 5-6 | 8-20 min | ~150-250K |
| 5 IMPROVEMENT (per loop) | 3-5 / 2-4 | 2-4 | 8-15 min | ~100-180K |
| 6 PUBLISH | 1-4 / 1-3 | 1-2 | 3-10 min | ~30-50K |

### Total envelopes

| Scenario | Agents | Wall Time | Tokens |
|----------|--------|-----------|--------|
| Single-format, no loops | 16-32 | 35-90 min | ~750K-1.5M |
| Both formats, no loops | 21-43 | 39-100 min | ~880K-1.8M |
| Both formats, 1 loop | 24-48 | 47-115 min | ~980K-2.0M |
| Both formats, 2 loops (max) | 27-53 | 55-130 min | ~1.1M-2.2M |

### Cost comparison

| Recipe | Agents | Wall Time | Relative $ Cost |
|--------|--------|-----------|------------------|
| Single skill (`stage` / `zine` / `scribe`) | 1 | 3-15 min | ~0.5-1× (baseline lite) |
| `feature` | 3-5 | 5-15 min | 1× (baseline) |
| `podium` single-format, no loops | 16-32 | 35-90 min | 3-5× |
| `podium` both formats, no loops | 21-43 | 39-100 min | 4-6× |
| `podium` both formats, 2 loops | 27-53 | 55-130 min | 5-8× |
| `apex` | 8-25 | 30-90 min | 4-8× |
| `summit` | 32-119 | 49-193 min | 7-25× |

**Rule of thumb:** podium costs 3-8× a typical `feature` chain. Use when the content artifact's polish materially affects external perception (audience impression, technical credibility, sales conversion) — not for internal scratch notes. For internal-only routine docs, prefer single-skill direct call.

---

## Comparison with Single-Skill / Atelier / Summit

| Dimension | Single skill (Zine/Stage/Scribe) | `atelier` | `podium` | `summit` |
|-----------|----------------------------------|-----------|----------|----------|
| **Purpose** | Narrow content task | UI design pipeline (Vision→Muse→Forge→Artisan→Vitrine→Canvas) | Doc + Slide content artifact (cross-format) | Strategic code decision |
| **Output** | Single artifact (article OR deck OR spec) | Implemented UI + design system | Doc + Slide + assets package | Working code + verification trail |
| **Engines** | 1 (Claude usually) | Mixed (atelier picks per step) | 2-3 (Claude + Codex, agy optional) | 2-3 (Claude + Codex, agy optional) |
| **Teams** | 1 | Sub-orchestration (design-domain) | 5 (Research / Narrative / Production / Verification / Improvement) | 5 (Analysis / Design / Execution / Verification / Improvement) |
| **Verification** | Self-only | Vitrine + Canvas audit | Multi-branch cross-engine quorum on content | Multi-engine quorum on code |
| **Loop** | None | None (single-pass pipeline) | Max 2 loops (magi-arbitrated) | Max 3 loops (magi-arbitrated) |
| **Agents** | 1 | 5-10 | 16-53 | 32-119 |
| **Wall time** | 3-15 min | 20-60 min | 35-130 min | 49-193 min |
| **Cost vs feature** | 0.5-1× | 2-4× | 3-8× | 7-25× |
| **agy required** | No | No | No (optional) | No (optional) |
| **User confirm** | No | No | Only for release-critical | Mandatory |
| **Best for** | One-off narrow content | UI component design and code | Conference deck + article, design system docs, onboarding kit, retrospective package | Architecture pivots, release-critical launches, large refactors |

### Decision tree

```
Is the goal a single narrow content task with no cross-format need?
  └─ YES → single skill (zine / stage / scribe / quill / tome / morph)
  └─ NO ↓

Is the goal a UI design + code pipeline?
  └─ YES → atelier
  └─ NO ↓

Does the content artifact need polished prose AND polished visuals AND
  (cross-format OR audience walkthrough OR claim grounding)?
  └─ NO  → single skill (or chain manually via Nexus classify)
  └─ YES ↓

Is the work a strategic code decision (architecture / release-critical)?
  └─ YES → summit
  └─ NO ↓

Is the artifact external-facing (audience > internal team)?
  └─ Confirm risk_tier, then → podium
  └─ Otherwise → podium with risk_tier = routine (no confirmation gate)
```
