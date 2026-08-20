# Tome Recipe Registry

The full Recipe table for `tome`. `tome/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Learning Doc | `learn` | ✓ | Standard `learning_doc` generation. Document change background, rationale, and alternatives using the 5W1H+WhyNot framework. Applies normal `SCOPE → EXTRACT → ANALYZE → COMPOSE → REVIEW` workflow. | `reference/output-templates.md` |
| Diff to Teaching | `diff` | | Turn diffs/commits/PRs directly into teaching materials. Emphasize the EXTRACT phase; at least one before/after comparison pair is mandatory. | `reference/patterns.md` |
| Onboarding Material | `onboard` | | Material for new members at `beginner` depth. Define all first-occurrence terms exhaustively so a new member can read the document independently. | `reference/output-templates.md` |
| Design Decision Record | `record` | | `decision_record` generation. Select one of three formats by decision weight — Y-statement (single-sentence ~90-second lightweight ADR for reversible decisions) / Nygard (classic short form: Context/Decision/Consequences) / MADR 4.0.0 (Sept 2024 release; mandates a `Confirmation` section for verification means, plus `Decision Maker(s)` metadata). One decision per record, strictly. [Source: adr.github.io; github.com/adr/madr/releases] | `reference/output-templates.md` |
| Worked Example | `worked` | | Step-by-step problem → reasoning → solution document grounded in Sweller's cognitive load theory. Annotate expert thought process, common errors, and "why it works." For learning sequences, design faded-guidance progression. | `reference/worked-example.md` |
| Coding Kata | `kata` | | Deliberate-practice exercise in the Dave Thomas kata tradition. Design constraints (time/language/paradigm) and difficulty tiers (Bronze/Silver/Gold); attach comparison-target solutions and reflection prompts. | `reference/coding-kata.md` |
| Quickstart Guide | `quickstart` | | ≤15-minute first-success path. Strictly narrow prerequisites; place "you should see..." anchors at success-verification points. Troubleshooting in decision-tree form. | `reference/quickstart-guide.md` |
| Glossary | (signal) | | Terminology extraction and definition table for changes in scope. Triggered by `glossary` / `terms` signal keywords. | `reference/output-templates.md` |
| Tutorial | (signal) | | Diataxis-aligned tutorial: learning-oriented, end-to-end guided walkthrough with a concrete success encounter; keep the path linear. Triggered by `tutorial` / `learning path` / `guided`. | `reference/output-templates.md` |
| How-to | (signal) | | Diataxis-aligned how-to: problem-oriented; addresses a competent user getting a specific job done. Triggered by `how-to` / `recipe` / `solve`. | `reference/output-templates.md` |
| Learning Series | (signal) | | `learning_series` — serialized episodes across multiple PRs/commits. Triggered by `batch` / `sprint` / `series`. Each episode independently readable. | `reference/output-templates.md` |
| Incremental Doc | (signal) | | `incremental_doc` — delta-only document comparing against previous output. Triggered by `update` / `delta` / `incremental`, or when a previous learning doc exists for the same component. | `reference/output-templates.md` |
| Article | `article` | | External technical article from a concept, draft, learning doc, or retrospective. The platform is a parameter chosen at FRAME — `note` (Japanese long-form: 目次, 3-5 tags, magazine context, hook, CTA) · `zenn` (engineer-focused: emoji, Tech/Idea type, up to 5 topics) · `qiita` (code-heavy tip: TL;DR, up to 5 tags) · `devto` (English: cover spec, up to 4 tags, canonical URL when cross-posted). | `reference/article-patterns.md`, `reference/article-hook-design.md`, `reference/article-platform-optimization.md` |
| Article Series | `article-series` | | External article-series design, index maintenance, cross-links, cadence, and tonal continuity. | `reference/article-series-management.md` |
| Headline | `headline` | | Generate and score platform-calibrated title variants without clickbait. | `reference/article-headline-patterns.md` |
| Repurpose | `repurpose` | | Adapt one canonical article into platform variants and atomic content assets. | `reference/article-content-repurposing.md`, `reference/article-handoffs.md` |
| Interview | `interview` | | Reshape a transcript, podcast, talk, or AMA into a voice-preserving Q&A article. | `reference/article-interview-format.md` |
