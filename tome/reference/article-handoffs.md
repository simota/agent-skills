# Handoffs

**Purpose:** Structured handoff templates for incoming sources (User / Tome / Saga / Launch) and outgoing destinations (Growth / Prose / Stage / Canvas / Saga / Scribe / Nexus).
**Read when:** Receiving a handoff at FRAME, or preparing a deliverable handoff at PUBLISH.

---

## Incoming Handoffs

### From User → Tome

User inputs come in three shapes. Detect the shape at FRAME.

#### Shape 1: Concept-only

User gives a topic or thesis, no draft:

```
「Claude Skillsの連載、次は#09 Forgeを書きたい。Forgeはprototype担当のエージェント。」
```

**Tome response at FRAME:**
- Confirm platform (defaults to established series platform — here, note).
- Confirm this is #09 in the existing series.
- Re-read #00 Overview + #08 (previous episode) before drafting.
- Re-read series bible in `.agents/PROJECT.md`.
- Proceed to DRAFT. Generate full article from scratch.

#### Shape 2: Rough draft

User gives existing prose, wants restructuring / polish:

```
「こんな感じで書いたんだけど、もっと引きが強くできる？」[attached rough draft]
```

**Tome response at FRAME:**
- Read the full draft.
- Identify: what the draft is trying to say (thesis), what's working, what's throat-clearing, where the hook fails.
- Confirm with user: preserve voice vs full restructure?
- Proceed to STRUCTURE → POLISH (skip DRAFT, augment instead).

#### Shape 3: Source material → article

User gives raw material (git log, notes, PR descriptions, screenshots), wants Tome to author from scratch:

```
「このPR群から、月次の振り返り記事書いて」[attached PR list / git log]
```

**Tome response at FRAME:**
- Read all source material.
- Ask: platform, tone, retrospective vs announcement vs tutorial framing.
- Run Tome's learning workflow first when the source is raw git diffs, then pass the grounded learning document into publication mode.
- Proceed to DRAFT.

---

### From Tome Learning Mode → Tome Publication Mode

Learning mode generates grounded documents from git diffs and decision history. Publication mode reshapes that output for an external audience.

**Mode-transition format:**

```yaml
TOME_LEARNING_TO_ARTICLE_HANDOFF:
  source_commits: [commit hashes / range]
  learning_doc: [path to Tome's output]
  key_decisions:
    - decision: [what was decided]
      rationale: [why]
      impact: [what changed]
  technical_claims:
    - claim: [technical fact from diffs]
      grounding: [file/line reference]
  target_audience: [internal team | onboarding | external]
  suggested_platform: [if Tome has context, suggest]
```

**Publication-mode actions on receipt:**

1. Read the learning document verbatim — preserve all technical claims as-is.
2. Identify 1-2 most interesting decisions as the article's thesis (the learning document may list 10; a good article has 1-2 payloads, not 10).
3. Convert chronological / decision-order to reader-order (hook-first, not history-first).
4. Add hook, narrative framing, CTA.
5. Mask internal-only details (client names, unreleased features) before publish.

**Preservation rule:** Do not reword grounded technical claims. If the learning document says "changed from Redis pub/sub to NATS JetStream for at-least-once semantics", keep that phrasing; wrap narrative around it, don't rephrase.

---

### From Saga → Tome

Saga writes product narratives (customer stories, scenario sagas). Sometimes those narratives want a technical blog variant.

**Handoff format (Saga → Tome):**

```yaml
SAGA_TO_TOME_HANDOFF:
  narrative: [path to Saga's customer-story output]
  protagonist: [customer / persona]
  conflict: [what problem they had]
  resolution: [how the product solved it]
  technical_backstory: [what engineering happened behind the scenes]
  external_tone_fit: [platform / audience Saga thinks this could land on]
```

**Tome actions on receipt:**

1. The customer story goes in the background, not foreground — external tech blog readers want the engineering perspective.
2. Reshape: Saga leads with customer; Tome leads with engineering challenge.
3. Credit the customer only if they've consented and Saga confirms.
4. Output: technical retrospective pattern (context → journey → lessons) with the customer story as the anchor moment.

---

### From Launch → Tome

Launch collects GitHub PR data and generates work reports. PR-heavy periods seed release / retrospective posts.

**Handoff format (Launch → Tome):**

```yaml
LAUNCH_TO_TOME_HANDOFF:
  period: [YYYY-MM-DD to YYYY-MM-DD]
  prs: [list of PR titles, authors, labels, impact summaries]
  themes: [Launch's auto-extracted themes — e.g., "performance", "a11y", "refactor"]
  notable_shipped_features: [list]
  notable_deprecated: [list]
  suggested_article_types:
    - "monthly release post"
    - "retrospective on X migration"
```

**Tome actions on receipt:**

1. Pick ONE theme to anchor the article. Launch may suggest 3; a good article has 1 thesis.
2. Identify the PR that best embodies the theme (hero PR).
3. Zoom into the hero PR's story; the other PRs become supporting evidence.
4. Draft as: Retrospective pattern (if past-looking) or Announcement pattern (if forward-looking).

---

## Outgoing Handoffs

### Tome → Growth

Growth handles SEO / SMO / OGP / GEO (AI citation optimization). Tome delivers the canonical article + seed metadata; Growth adds keyword research, schema, social cards.

**Handoff format (Tome → Growth):**

```yaml
TOME_TO_GROWTH_HANDOFF:
  canonical_article:
    path: [Markdown file path]
    word_count: [count]
    platform: [note | Zenn | Qiita | dev.to | cross-post]
    target_reader: [persona description]
  title_candidates:
    - "[Candidate 1]"
    - "[Candidate 2]"
    - "[Candidate 3]"
  meta_description_draft: [~155 chars, ~120 chars for JP]
  h_tag_outline:
    - H1: "[Title]"
    - H2: "[Section 1]"
    - H2: "[Section 2]"
    ...
  og_text: [social card copy, ~100 chars]
  series_context: [if applicable — index URL, episode number]
  unlocked_claims: [verified technical claims that can be cited]
  growth_asks:
    - "Keyword research on [topic]"
    - "JSON-LD Article schema"
    - "Twitter/X card variant"
    - "OG image brief for Builder image-recipe handoff"
```

**Scope boundary:** Tome does not do keyword research, ranking strategy, AI-citation optimization (GEO), or JSON-LD schemas — all Growth territory.

---

### Tome → Prose

Prose polishes microcopy / UX strings / CTAs. Tome hands off articles that contain embedded UI copy requiring consistent voice.

**Handoff format (Tome → Prose):**

```yaml
TOME_TO_PROSE_HANDOFF:
  article_path: [Markdown file path]
  microcopy_instances:
    - location: [line reference]
      text: "[current text]"
      context: [what this button/label/CTA is for]
  cta_block: [the article's closing CTA text]
  voice_guide: [link to series bible / voice doc]
  polish_scope: ["CTA only" | "all microcopy" | "voice tone consistency pass"]
```

**Typical case:** Article includes a screenshot with a "Subscribe" button; in-body sidebar with a signup CTA; closing CTA. Prose ensures these match product's in-app microcopy voice (not generic marketing voice).

---

### Tome → Stage

Stage converts long-form to slide decks (Marp / reveal.js / Slidev) with WPM-calibrated pacing.

**Handoff format (Tome → Stage):**

```yaml
TOME_TO_STAGE_HANDOFF:
  article_path: [Markdown file path]
  article_word_count: [count]
  target_talk_length: [minutes — e.g., 20, 30, 45]
  key_beats:
    - beat: "[1-2 sentence summary]"
      suggested_slide_count: [1-3]
    - beat: "[1-2 sentence summary]"
      suggested_slide_count: [1-3]
  key_visuals_needed:
    - [diagram / chart / screenshot]
  audience: [conference type — e.g., JSConf JP, internal team, webinar]
  slide_framework_preference: [Marp | reveal.js | Slidev | no preference]
```

**Scope boundary:** Tome provides the narrative beats; Stage owns slide pacing (WPM calibration), visual design, transitions, and framework-specific output.

---

### Tome → Canvas

Canvas generates Mermaid / ASCII / draw.io diagrams. Tome articles often need supporting figures (architecture diagrams, sequence flows, decision trees).

**Handoff format (Tome → Canvas):**

```yaml
TOME_TO_CANVAS_HANDOFF:
  article_path: [Markdown file path]
  figure_requests:
    - location: [H2 section where figure belongs]
      purpose: [what the figure illustrates]
      type: [flowchart | sequence | class | ER | state | C4 | journey]
      source_content: [prose or code the figure should visualize]
      output_format: [Mermaid | ASCII | draw.io]
```

**Typical case:** A deep-dive article about event-driven architecture needs a sequence diagram showing the happy path and a failure-mode diagram. Tome hands off the prose describing each; Canvas generates the Mermaid.

---

### Tome → Saga

Sometimes a tech blog article has a strong customer-story angle that warrants reshaping for marketing. Tome hands off to Saga for customer-narrative reshape.

**Handoff format (Tome → Saga):**

```yaml
TOME_TO_SAGA_HANDOFF:
  article_path: [Markdown file path]
  technical_story: [1-3 sentences of the engineering angle]
  customer_angle: [1-3 sentences of the customer-value angle]
  persona_hint: [who the customer is, anonymized]
  consent_status: [customer-approved | anonymized | permission-pending]
  requested_output: [marketing site case study | customer testimonial page | pitch-deck slide]
```

**Scope boundary:** Tome writes for tech audience; Saga writes for buyer / customer audience. Same material, different framing, different outlet.

---

### Tome → Scribe

Scribe converts formats (Markdown → PDF / Word / EPUB / HTML). When a series is mature enough to anthologize, Tome hands off to Scribe.

**Handoff format (Tome → Scribe):**

```yaml
TOME_TO_SCRIBE_HANDOFF:
  source_articles:
    - [article 1 path]
    - [article 2 path]
    - ...
  anthology_title: [title for PDF / book]
  target_format: [PDF | EPUB | Word | HTML standalone]
  cover_asset: [image path if available]
  toc_structure: [chapter ordering, not necessarily publish order]
  styling_preference: [preserve original | unified book styling | minimal]
  front_matter: [preface / acknowledgments / copyright / etc.]
  back_matter: [index / bibliography / about-the-author / etc.]
```

**Typical case:** Series reaches 15+ episodes; user wants PDF zine for download / paid sale. Tome confirms episode ordering, provides front/back matter text, hands off to Scribe for PDF generation.

---

## Nexus ↔ Tome Handoff

When Tome is invoked via Nexus (multi-agent chain), use the standard Nexus handoff format.

**Nexus → Tome (AUTORUN input):**

```yaml
_AGENT_CONTEXT:
  Role: Tome
  Task: "Draft #09 Forge article for 図鑑 series"
  Mode: AUTORUN
  Chain: [User -> Nexus -> Tome[learn] -> Tome[article]]
  Input:
    source: "Tome learning doc at docs/learning/forge-2026-04.md"
    series_context: ".agents/PROJECT.md has 図鑑 series bible"
  Constraints:
    - Platform: note
    - Series: 図鑑-#09
    - Tone: first-person teaching (matches #00-#08)
    - Length: 3500-5000字
    - Language: Japanese
  Expected_Output: "Full article + updated index + Growth handoff seed"
```

**Tome → Nexus (AUTORUN output):**

```yaml
_STEP_COMPLETE:
  Agent: Tome
  Status: SUCCESS
  Output:
    deliverable: "articles/zukan/09-forge.md"
    artifact_type: "Article + Series Index Update"
    parameters:
      platform: note
      series_position: "図鑑-#09"
      hook_type: contradiction
      word_count: 4200
      tone: first-person teaching
      cta_type: next-episode
    files_changed:
      - path: articles/zukan/09-forge.md
        type: created
        changes: "Full #09 Forge article, 4200字"
      - path: articles/zukan/00-overview.md
        type: modified
        changes: "Added #09 to episode list; updated #10 as next planned"
  Handoff:
    Format: TOME_TO_GROWTH_HANDOFF
    Content: "[Full handoff content — title candidates, meta desc, H-outline]"
  Artifacts:
    - articles/zukan/09-forge.md
    - articles/zukan/00-overview.md (diff)
    - metadata/note-tags-09-forge.yaml
  Risks:
    - "LOW CONFIDENCE: Forge's retry policy details — author should verify before publish"
  Next: Growth
  Reason: "SEO/OGP packaging for #09 before publish"
```

---

## Handoff Decision Tree

```
Article deliverable ready
├── Needs SEO / OGP / social packaging?
│   └── → Growth
├── Needs microcopy / CTA voice polish?
│   └── → Prose
├── Will become a talk?
│   └── → Stage
├── Needs diagrams/figures?
│   └── → Canvas
├── Has customer-story angle for marketing?
│   └── → Saga
├── Series mature → anthology?
│   └── → Scribe
└── None of the above → publish directly, notify user
```

Pick at most two downstream agents per article — fanning out to more agents dilutes coherence.


---

## Architecture Diagram

Referenced from `SKILL.md` -> Collaboration.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT PROVIDERS                          │
│  User    → concept / rough draft / retrospective notes      │
│  Tome    → learning doc (git-diff derived)                  │
│  Saga    → product narrative (internal) to reshape external │
│  Launch → PR/release summary seeding release post           │
│  Nexus   → task context, platform & audience decided        │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
            ┌─────────────────┐
            │       Tome      │
            │ Article Author  │
            └────────┬────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT CONSUMERS                          │
│  Growth  → SEO/SMO/OGP packaging, distribution strategy     │
│  Prose   → microcopy polish for CTAs and inline UI strings  │
│  Stage   → slide deck conversion from long-form             │
│  Canvas  → diagram/figure requests for article illustrations│
│  Saga    → narrative reshape to product customer story      │
│  Scribe   → export canonical Markdown to PDF/Word/EPUB zine  │
└─────────────────────────────────────────────────────────────┘
```
