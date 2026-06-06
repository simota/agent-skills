# Headline Patterns

## Purpose

The headline is the only thing 80% of social-feed scrollers will see. A perfect article behind a weak headline never gets clicked. This reference catalogs CTR-tested patterns, length budgets per platform, and the variant-and-rank workflow.

## Scope Boundary

- IN scope: title formula generation, variant ranking, platform-specific length tuning, A/B candidate scoring, anti-clickbait calibration.
- OUT of scope: opening hook (`hook-design.md`), SEO keyword placement (delegate to `growth`), social card / OG text (delegate to `growth`), in-body H2 wording (covered by `article-patterns.md`).

## Core Concepts

### Title vs Hook vs Lede

Confused often. Distinct functions:

| Element | Where | Job |
|---------|-------|-----|
| Title | Feed / RSS / search result | Earn the click |
| Hook | First sentence after click | Earn the second paragraph |
| Lede | First paragraph + nut graf | Earn the third screen |

A headline that earns the click but disappoints the lede produces "click and bounce" — the worst outcome for both reader and author. Always check title and lede are on the same promise.

### CTR-Tested Title Formulas

| Formula | Pattern | Example |
|---------|---------|---------|
| Number | `[N] [thing] [outcome]` | "30,000行のコードを削除して学んだ7つのこと" |
| Number-direct | `[Concrete N] [verb past] [stake]` | "We deleted 30,000 lines and made the app 4× faster" |
| How-to | `[Outcome] without [pain]` | "How to ship Friday without breaking Monday" |
| Curiosity Gap | `[Surprising claim], and [counter-intuitive reason]` | "Why our most reliable service had no tests" |
| Contrarian | `[Common belief] is wrong. Here's why.` | "Microservicesは間違いだった。3年後の振り返り" |
| Question | `[Question reader has been afraid to ask]?` | "なぜあなたのテストスイートは信頼されないのか？" |
| Promise | `The [adjective] guide to [topic]` | "実用本位の RAG 設計ガイド" |
| Negative | `Stop [doing X] / Don't [do Y]` | "Stop using `useEffect` for data fetching" |
| Listicle | `[N] [thing] every [persona] should [verb]` | "全エンジニアが知るべき5つの Postgres インデックス" |
| Story | `[Concrete moment / scene from a real event]` | "金曜20時、Slackに「本番落ちてます」が流れた" |
| Versus | `[A] vs [B]: [verdict / question]` | "BM25 vs Hybrid Search: どちらを本番で使うべきか" |
| Year-stamp | `[Topic] in [year]: [shift]` | "Building a Rails app in 2026: what changed" |

### Headline Anti-Patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| "本記事では〜について書きました" | ChatGPT residue; signals low-effort. |
| "[Topic] の話" / "〜してみた" without payoff | No promise to the reader. |
| All-caps clickbait ("YOU WON'T BELIEVE …") | Triggers feed-skim avoidance among technical readers. |
| Generic "Tips and Tricks" | Zero differentiation; semantic noise. |
| Three colons or two em-dashes | Title becomes unparseable on mobile. |
| Brand-first ("[Company] launches …") | Reader-cost first, reader-benefit second is the wrong order. |
| Question with obvious yes/no answer | Wastes the slot. |
| Buzzword stacking ("AI-powered cloud-native serverless …") | Indicates the author has nothing concrete to say. |

### Length Budgets by Platform

Length matters because feeds truncate. Aim for the platform's no-ellipsis budget.

| Platform | Pixel / char budget | Notes |
|----------|--------------------|-------|
| note (web list) | ~50–60 全角 chars | Mobile truncation often around 30; front-load the payoff. |
| Zenn | ~60 chars | Emoji counts as 2 chars. |
| Qiita | ~70 chars | Tag + title together get ranked. |
| dev.to | ~60–80 chars (English) | Cover image often more important than title length. |
| X / Twitter share | ~70 chars + URL | Card preview takes most of the visual real estate. |
| LinkedIn | ~70–100 chars | First line stops at ~ 140 in feed; title rarely reaches that. |
| Google search snippet | ~50–60 chars (English) / ~28 全角 (Japanese mobile) | Beyond the cap, ellipsis hides the payoff. |
| Bluesky / Mastodon shares | Title only on the embed card | Length less critical; specificity wins. |

### Specificity Beats Adjectives

Compare:

- "A faster way to write tests" → vague
- "Cut Jest test runtime from 14m to 90s by isolating snapshot serializers" → specific

Specific titles trade slightly lower volume for much higher relevance and shareability. For technical content, specificity also signals that the author actually did the thing.

### The Promise Test

Read the title aloud. Now finish the sentence:
*"If I read this article, I will be able to ___ ."*

If you cannot finish the sentence, the title has no promise. Promiseless titles get scrolled.

### Honesty Calibration

Curiosity-gap titles work but easily slide into clickbait. The test: by paragraph 3, has the article delivered on the promise? If not, the title was a lie. Lies cost reader trust and platform credibility — both expensive and slow to rebuild.

### Variant Generation

Always generate 5–10 variants before committing. The first title is rarely the best. Use the variant table:

| Variant | Formula | Length | Specificity | Promise |
|---------|---------|--------|-------------|---------|
| V1 | Number | 42 chars | Medium | "learn 7 lessons" |
| V2 | Contrarian | 38 chars | High | "rethink microservices" |
| V3 | Story | 48 chars | High | "live the incident" |
| V4 | How-to | 52 chars | Medium | "ship without breakage" |
| V5 | Question | 35 chars | High | "diagnose your tests" |

Score each on a 5-point scale across: feed-stopping power, specificity, promise clarity, scroll-resistance, lede-fidelity. Top 3 go to the author or A/B test if the platform supports it.

### Platform-Tone Calibration

| Platform | Voice |
|----------|-------|
| note | Author-first, narrative permitted, em-dashes welcome |
| Zenn | Engineer peer; slightly drier than note; emojis at start are part of the style |
| Qiita | Tip-direct; Tips系 / 解説系 with domain term up front |
| dev.to | Friendly, hooky, often ends with `?`; emojis common |
| X thread head | Punchy, sentence-fragment OK |
| LinkedIn | Outcome-oriented, "lessons" / "what we learned" framing |

A title tuned for note ("夏の夜、Postgres が止まった話") underperforms on Qiita; the same content for Qiita might be ("Postgres メモリ枯渇の原因特定 — pg_stat_activity 起点の調査メモ").

## Workflow

1. **Articulate the promise** — finish "if I read this, I will be able to ___ ".
2. **Pick 3 formulas** that fit the article shape (e.g., Number, Contrarian, Story).
3. **Generate 5–10 variants** across formulas.
4. **Trim to platform length budget** — note ≤ 60 全角, dev.to ≤ 80 chars, etc.
5. **Run the Promise Test** on each variant; cut promiseless ones.
6. **Run the Honesty Test** — does the article deliver?
7. **Score on 5 axes** (stop-power, specificity, promise, scroll-resistance, lede-fidelity).
8. **Recommend top 3** with rationale; let the author choose.
9. **Cross-check tonal fit** with platform voice before publish.

## Output Template

```yaml
headline_design:
  promise: "After reading, the reader can diagnose flaky tests with bisect-style isolation."
  platform: zenn
  length_budget_chars: 60
  variants:
    - id: V1
      formula: number
      title: "テストを信頼できない7つの理由と、修復のための診断手順"
      length: 32_zenkaku
      scores:
        stop_power: 3
        specificity: 4
        promise: 4
        scroll_resistance: 3
        lede_fidelity: 5
    - id: V2
      formula: contrarian
      title: "テストを増やすほど信頼が下がる理由"
      length: 19_zenkaku
      scores:
        stop_power: 5
        specificity: 3
        promise: 4
        scroll_resistance: 5
        lede_fidelity: 4
    - id: V3
      formula: how_to
      title: "Flaky test を bisect で特定する実践手順"
      length: 23_zenkaku
      scores:
        stop_power: 4
        specificity: 5
        promise: 5
        scroll_resistance: 4
        lede_fidelity: 5
  recommended:
    primary: V3   # highest weighted score; specificity + promise dominate
    secondary: V2 # for X-thread teaser
    tertiary: V1  # for LinkedIn version
  honesty_check: PASS  # promise delivered by paragraph 3
```

## Anti-Patterns

- Committing to V1 without generating alternatives.
- Optimizing for keyword stuffing over reader promise — Growth's job, not Zine's.
- Using a curiosity-gap title with no payoff in the first 3 paragraphs.
- Identical title across platforms despite different audiences and tones.
- Title that doesn't match the lede — feels like a bait-and-switch.
- Two punctuation marks fighting for attention (colon + em-dash + question mark).
- Brand or product name as the first word for content marketing — readers detect ads instantly.
- "Part 2" without recap — strands new readers.
- Year-stamping evergreen content — locks in obsolescence.

## Deliverable Contract

A headline package is complete when:

- The promise is articulated explicitly.
- 5–10 variants generated across at least 3 formulas.
- All variants fit the platform length budget.
- Each variant scored on the 5 axes.
- Honesty check passes against the actual article.
- Top 3 recommendations with rationale.
- Per-platform variant if cross-posting.

## References

- David Ogilvy, *Ogilvy on Advertising* (1983) — original "five times more people read the headline than the body" claim.
- BuzzSumo, *Headline Effectiveness Report* (2023) — formula performance data.
- Conductor / SearchEngineLand studies on number-led titles.
- Brian Dean, *Backlinko* — H1 / title length and CTR analyses.
- Andy Crestodina, *Orbit Media* — promise-test methodology.
- Ann Handley, *Everybody Writes* (2nd ed., 2022) — clickbait vs curiosity calibration.
- Nieman Lab — journalism headline research, 2018 onward.
