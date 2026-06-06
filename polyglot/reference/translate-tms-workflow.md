# Translation Workflow and TMS Integration Reference

Purpose: Use this file to design the translation pipeline Polyglot's `translate` subcommand owns: TMS integration (Lokalise / Crowdin / Phrase / Smartling), translation-memory reuse, source-string change detection, translator briefing, QA checks, and release coordination. The goal is every new/changed string reaches a qualified translator with enough context, and nothing merges to `main` with broken placeholders or missing translations.

## Scope Boundary

- **Polyglot `translate`**: TMS integration, translation-memory strategy, source-string diff detection, translator briefing, placeholder/HTML QA, release workflow.
- **Prose (elsewhere)**: source-language copy authoring — the English string that enters the TMS. `translate` moves strings through the pipeline; Prose writes them.
- **Artisan (elsewhere)**: framework-specific extraction output format (ICU JSON, PO, XLIFF, ARB) from the codebase. `translate` consumes the extracted payload; Artisan configures the extractor.
- **Accord (elsewhere)**: spec-level L10n requirements (SLAs, target-locale list, quality tier). `translate` operationalizes the spec.

If the ask is "wire Lokalise webhook / set translator brief / add placeholder QA gate" → `translate`. If it is "write the English copy" → Prose. If it is "configure i18next extractor" → Artisan.

## TMS Platform Selection

| TMS | Strengths | Best for |
|-----|-----------|----------|
| Lokalise | Fastest API, strong i18n format support (ICU, Android XML, iOS strings, Flutter ARB), GitHub Action | Mobile + web with mixed formats |
| Crowdin | Community translation support, rich in-context editor, Figma plugin | Open source projects, community contributions |
| Phrase (Strings + TMS) | Enterprise workflow automation, branching, advanced QA | Large enterprise with review workflows |
| Smartling | Translation memory depth, LQA tooling, best-in-class for high-volume marketing | Marketing-heavy sites, regulated industries |
| Transifex | GitLab/GitHub native flows, resource-file-oriented | Open source, doc-heavy projects |
| Locize | Format-preserving (writes whatever you give it — MF1 / MF2 / plain), i18next-native, CDN-served | i18next-first projects, MF2 pilot |

Selection rules:
- Project already has one → keep it. Never multi-TMS the same string set.
- Pick based on **source format and translator pool**, not dashboard UI preferences.
- Verify the TMS supports **ICU MessageFormat 1**. MF2 support remains spotty across major TMS platforms as of 2026-05 — Crowdin's monthly release notes had no MF2 mentions through the first half of 2026, Lokalise and Phrase have not announced first-class MF2, and most format-preserving stores (Locize) simply forward the message text. Treat MF2 as a `12-24` month migration target, not a 2026 default.

### LLM-Based Translation Loop (2026 supplement)

A growing pattern in 2026 pairs the TMS with an **LLM translation step** as the first pass:

- `i18n-actions/ai-i18n` (GitHub Action) — extracts strings from XLIFF / JSON, sends only the diff to an LLM provider (Anthropic / OpenAI / Ollama), commits results back to the repo. Drop-in alternative to Lokalise / Phrase / Crowdin for small / medium projects.
- For larger projects: keep the TMS as the system of record, but configure its **MT engine** to use an LLM (Claude / GPT-4-class) for the pre-translation pass before human review. Reports show LLM pre-translation outperforms classical neural MT for many languages, and reduces the human-reviewer workload by ~`30-50%` on routine UI copy.

Hard rule: LLM-generated translations **must pass through a human reviewer** for any user-facing copy that ships. The LLM pass is "draft", not "ship". Legal / regulatory copy (privacy notice, ToS, financial disclosures) MUST be human-translated and reviewed; never auto-ship LLM output for those surfaces.

## Source → TMS → Target Pipeline

```
AUTHOR     →  Prose writes English copy; keys land in source JSON
EXTRACT    →  CI extracts new/changed keys; diffs against last TMS sync
PUSH       →  Push source changes to TMS branch (not main) via API
TRANSLATE  →  TMS assigns to translator; TM suggests reuse; MT pre-fills optionally
REVIEW     →  LQA / second pair of eyes on brand + legal strings
PULL       →  CI pulls finalized translations into the repo (PR, not main)
QA GATE    →  Placeholder parity, HTML tag integrity, length budget, missing-key check
MERGE      →  PR merges after QA + human review
RELEASE    →  Feature flag or locale-by-locale rollout
```

Rules:
- **Source changes push on every PR merge that touches i18n keys**, not on a nightly cron — translators work against stale copy otherwise.
- **Translated pulls land as PRs**, never direct-to-main — CI QA gates must run.
- **Never hand-edit** a translated file in the repo; changes must round-trip through the TMS or TM divergence accumulates.

## Source-String Change Detection

When a source string changes, the TMS must re-translate (not silently reuse the old translation).

| Change type | Correct behavior |
|-------------|------------------|
| New key | Assign for translation, no TM match yet |
| Typo fix, no meaning change | Mark as `no-review` / auto-approve same translation |
| Semantic change ("Log in" → "Sign in") | Invalidate existing translations; re-translate |
| Placeholder added/removed | Hard-fail QA; requires translator attention |
| ICU plural branch added | Translator must cover new category per locale |

Most TMS platforms handle this automatically via TM fuzzy matching: ≥95% → auto-reuse, 75-95% → translator review, <75% → new. If rolling your own, hash the normalized (lowercase, whitespace-collapsed, punctuation-stripped) source to detect meaning-preserving edits vs semantic changes.

## Translation Memory Reuse

TM is the leverage: identical past strings reuse their past translations.

| Scenario | TM leverage |
|----------|-------------|
| "Save" button repeated across 40 screens | 100% reuse after first translation |
| "Save as PDF" vs "Save" | 60-80% match — translator reviews, TM suggests |
| Segmented marketing paragraph | Sentence-level TM for shared intros |
| ICU plural form | TM matches per-branch, not whole block |

Rules:
- **Segment at sentence level**, not paragraph — longer segments kill reuse rate.
- **Context key is part of the fingerprint** — same English string in different contexts ("Save" as verb vs "Save" as noun) are different TM entries if keyed differently.
- **TM is locale-pair specific** (en→ja TM ≠ en→zh TM). Never merge across pairs.

## Translator Briefing

Every TMS key should carry enough context that the translator does not have to guess. Minimum:

| Field | Purpose |
|-------|---------|
| Description / note | What this string is for, in UX terms (not dev jargon) |
| Max length | Hard cap in characters or pixels, especially for buttons/tabs |
| Screenshot or URL | Rendered location — Figma link, production URL, or Chromatic story |
| Placeholders list | `{name}`, `{count}`, and what each means |
| Tone | brand voice (formal / casual / playful) |
| References | Glossary terms used |

```json
{
  "key": "checkout.button.confirm",
  "value": "Confirm order",
  "description": "Primary CTA on checkout review page. Must be assertive.",
  "maxLength": 20,
  "screenshot": "https://app.com/checkout#review",
  "tone": "confident, action-oriented"
}
```

Without briefing, translators default to literal translation, and "Save" in Japanese becomes "保存" (file save) when you meant "セーブ" (game save).

## QA Checks (CI gate)

Every translation PR must pass these before merge. Fail-fast, not advisory.

| Check | Fails on |
|-------|----------|
| Placeholder parity | `{name}` appears in source but not in translation (or vice versa) |
| HTML tag integrity | `<b>` opened but not closed; `<a>` missing in translated string |
| ICU syntax | Malformed plural/select blocks |
| CLDR category coverage | Locale missing a required plural category |
| Length budget | Translation exceeds `maxLength` for the key |
| No source leakage | English text appears unchanged in a locale that should have been translated |
| Character set | CJK in Latin-only locales or vice versa |
| Encoding | Smart quotes, BOM, ZWNJ in unexpected places |

Placeholder parity check: compare sorted `{\w+}` matches between source and target; any mismatch fails the build.

## Release Workflow

Merging translated strings is not the release — rollout is.

| Rollout strategy | When |
|------------------|------|
| Ship all locales together | Small product, <5 locales, translations complete |
| Locale-by-locale flag | New market launch; one locale at a time |
| Beta locale marker | 50-95% coverage; user sees fallback for missing keys with visible beta badge |
| Hold release until N% coverage | Regulated markets (legal requires 100%) |

Rules:
- **Never release a locale at <95% coverage without a fallback policy** configured and documented.
- **Surface fallback transparently** — if Japanese falls back to English for 50 keys, log and monitor.
- **Legal and safety strings must be 100%** before the locale is live. Gate releases on those namespaces explicitly.

## Anti-Patterns

- Hand-editing `locales/ja.json` in the repo — diverges from TMS, next pull overwrites the fix silently.
- Pushing new source strings once per sprint instead of per PR — translators always work against stale copy.
- Using MT (machine translation) on legal, safety, or regulated strings without human LQA — liability exposure.
- Flattening ICU plural blocks into MT as a single string — MT returns a single form for all counts.
- Running translator QA only in staging — production deploy is first time placeholder breaks are caught.
- Mixing TMS projects across products — TM pollution (a button label in product A suggests a wrong translation for product B).
- Omitting screenshots for UI-constrained strings — button overflows on narrow mobile in German.
- Assuming TM fuzzy match ≥75% is safe to auto-accept — 75% can change meaning; review threshold is ≥95%.
- Disabling placeholder QA to "unblock release" — a silent `{name}` drop ships broken greetings in production.
- Translating variable names / API keys / CSS class names — broken application.
- Single-translator model with no review step on brand/legal/marketing — Voice and tone drift locale-to-locale.

## Handoff

**To Prose:**
- Source strings that need rewriting for translatability (ambiguous "Save", idioms, cultural references).
- Strings with no `description` context — Prose writes the brief.

**To Artisan:**
- Extractor format corrections when the TMS rejects the emitted JSON/XLIFF shape.
- Missing context-key metadata in extracted output (description/maxLength fields).

**To `pluralize` subcommand:**
- ICU plural blocks entering the TMS must be marked as `no-flatten` — route to `pluralize` for category-coverage validation per locale.

**To `locale` subcommand:**
- Target-locale list must match the app's locale negotiation — `translate` pushes to TMS only locales `locale` actually resolves.

**To Accord:**
- Locale coverage SLA escalations when a release target cannot be met.

**To Radar:**
- QA test matrix for placeholder/HTML/ICU parity; regression tests for past translation bugs.

**To Gear:**
- CI pipeline wiring: TMS webhook handler, translation-PR auto-merge rules (after QA passes), coverage reporting.

**Escape hatches / follow-ups:**
- `#TODO(agent): add placeholder QA gate` when CI lacks one.
- `#TODO(agent): wire TMS webhook` when source changes are not pushed on PR merge.
- `#TODO(agent): backfill translator briefs` when keys lack description/screenshot metadata.
