# Content Repurposing

## Purpose

One canonical article should become many deliverables across platforms — note, Zenn, Qiita, dev.to, X threads, LinkedIn posts, newsletter, and atomic social cards — without lossy translation or duplicate-content penalties. Repurposing multiplies reach 5–10× per hour invested compared to writing fresh.

## Scope Boundary

- IN scope: canonical-to-variant transformation, atomic asset extraction (threads, quote cards, snippets), platform-specific re-tone, canonical URL strategy, scheduling cadence.
- OUT of scope: original article authoring (`note`/`zenn`/`qiita`/`devto`), SEO duplicate-content audit (delegate to `growth`), social ad creative (different domain), video cuts (delegate to `cue`/`director`), thumbnail design (delegate to `director`).

## Core Concepts

### Hub-and-Spoke Model

Treat one platform as the **hub** (canonical home) and the others as **spokes** (variants linking back).

| Hub Choice | When |
|------------|------|
| Personal blog / company blog | When SEO authority should accrue to your own domain |
| note | JP-first, magazine series, paid content |
| Zenn | Engineer-first, code-heavy, OSS context |
| dev.to | English global reach, cross-post via `canonical_url` |

Spokes use `canonical_url` (dev.to / Medium support this natively) or a "originally posted at" link to avoid duplicate-content SEO penalty.

### The 1 → 5 → 25 Multiplier

A single 3,000-word article should yield:

| Level | Count | Output |
|-------|-------|--------|
| 1 | 1 | Canonical long-form |
| 5 | 5 | Platform variants — note / Zenn / Qiita / dev.to / LinkedIn long-form |
| 25 | 20+ | Atomic assets — X thread, LinkedIn post, quote cards (5–10), code snippets, single-tip posts, newsletter blurb, Bluesky post, Mastodon share, podcast talking point, video script outline |

> **Medium note (2025-2026)**: Medium Partner Program has undergone multiple paywall/earnings restructurings since November 2025 — search-driven traffic, new-member conversion, and broader distribution to non-Boosted stories now all affect earnings. Ongoing eligibility requires 5+ stories published within the last 6 months. Source: [medium.com Partner Program blog](https://medium.com/blog/partner-program-update-starting-january-1-were-rewarding-writing-more-broadly-4907e149e38c). Evaluate Medium as a spoke carefully; `canonical_url` is supported via "Import a story". For JP-first content, Medium is generally lower priority than Zenn/Qiita.

Don't aim for all 25 every time; aim for the highest-leverage 8–10 per article.

### Variant Translation, Not Copy-Paste

Real repurposing **adapts**:

| Dimension | Adaptation |
|-----------|------------|
| Length | note 4000字 → dev.to 1500 words is not just translation; it's a re-pacing |
| Voice | note 一人称で良い → Qiita では具体手順中心 |
| Code samples | dev.to may include English comments; Zenn keeps Japanese; note often hides verbose code in 折りたたみ |
| Hook | Hook reset for each platform's audience expectation |
| CTA | note → "次回記事を購読" / dev.to → "follow me on X" / LinkedIn → "what's your experience?" |
| Title | Per-platform tone (see `headline-patterns.md`) |
| Length budget | Each platform's no-ellipsis title cap |
| Tags | Different taxonomy per platform |
| Image | OGP / cover image / thumbnail varies per platform |

### Atomic Asset Catalog

| Asset | From | Format |
|-------|------|--------|
| X thread | First 6–10 sentences of canonical | Tweet 1 = hook, 2–N = beats, last = CTA + canonical link |
| LinkedIn post | Listicle section or contrarian beat | 3 lines hook, body, "what's your take?" close |
| Quote card | One-sentence insight | 1080×1080 image, branded, no logo dominance |
| Bluesky / Mastodon | Hook + canonical link | < 300 chars; Bluesky MAU ~1.5-3M (as of Oct 2025, down 40% YoY); strongest among developers, journalists, researchers |
| Newsletter blurb | TL;DR + link | 60–120 words |
| Code snippet card | Code block + 1-line caption | Carbon / ray.so / shiki render |
| Single-tip post | One paragraph from the listicle | Stand-alone "did you know" framing |
| Podcast talking point | Ledger of section headings | 3–5 talking points for solo or guest spot |
| Video outline | H2 hierarchy + voiceover lines | Hand off to `cue` for production |
| Slide-flash | 6–10 slides | Hand off to `stage` |

### Canonical URL Strategy

| Platform | Native canonical support |
|----------|-------------------------|
| dev.to | `canonical_url:` in front-matter — first-class |
| Medium | "Republished" via "Import a story" or `canonical_url` query param |
| Hashnode | `canonical:` in front-matter |
| Substack | Link in footer ("Originally published at …") |
| note | No native canonical; rely on first-publish primacy |
| Zenn | No native canonical; the URL hierarchy itself is the signal |
| Qiita | No native canonical; uses self-hosted only |

For Google ranking, the rule is: publish on the canonical hub first, wait 24–72 hours for indexing, then publish spokes with explicit canonical URL pointing back. Reverse order can flip the canonical to the wrong domain.

### Cadence

Don't publish all variants the same day — saturates feeds and looks spammy.

| Time | Action |
|------|--------|
| Day 0 | Hub publishes (canonical) |
| Day 0 | X thread teaser (4–6 hours after) |
| Day 1 | LinkedIn post variant |
| Day 2 | First spoke (Zenn or dev.to) with canonical pointing to hub |
| Day 4 | Second spoke (Qiita or Medium) |
| Day 7 | Newsletter feature |
| Day 14 | Quote card series begins (drip across week) |
| Day 30 | "Best of" round-up post on hub if multi-article series |

### Re-Engagement Without Re-Posting

For evergreen content, plan re-shares at 30 / 90 / 180 days with refreshed framing:

| Refresh Type | Example |
|--------------|---------|
| Anniversary | "1 year later: how this advice held up" |
| Counter | "Why I changed my mind about X" |
| Application | "Three teams that used this technique" |
| Update | "2026 edition: what's new" |

Each refresh is a new article, not a repost — original article gets internal link from the refresh.

### Translation vs Localization

Cross-language repurposing (Japanese → English or vice versa) is **localization, not translation**:

- Examples and metaphors must change (yakitori → BBQ; 麻雀 → poker).
- Frameworks named differently (Qiita → Stack Overflow / Medium reference).
- Tone calibration: Japanese tech audience often prefers reserved, English audience often prefers bolder claims.
- LLM auto-translation produces detectable seams; always have a human review or rewrite key sections.

## Workflow

1. **Identify the hub** — which platform is the canonical home?
2. **Publish on the hub first** and wait for index.
3. **Plan the variant set** — pick 3–5 spokes from the platform table.
4. **Plan the atomic set** — 5–10 assets from the catalog.
5. **Adapt each variant** — title, length, voice, examples, CTA. Not copy-paste.
6. **Set canonical URLs** explicitly on platforms that support it.
7. **Schedule with cadence** — drip across 1–2 weeks.
8. **Track performance** per spoke — find which platform pulls hardest for this content shape.
9. **Plan refresh** at 30 / 90 / 180 days for evergreen pieces.

## Output Template

```yaml
repurposing_plan:
  hub:
    platform: own_blog
    canonical_url: https://example.com/posts/flaky-tests
    publish_date: 2026-04-25
  spokes:
    - platform: dev.to
      title: "Diagnose flaky tests with bisect-style isolation"
      length_target_words: 1500
      canonical_url_in_frontmatter: yes
      voice: "friendly english, slightly hooky"
      cta: "follow me on Bluesky"
      publish_date: 2026-04-27
    - platform: zenn
      title: "Flaky test を bisect で特定する実践手順"
      length_target_chars: 4500
      voice: "engineer peer, code-forward"
      cta: "コメントで実例お待ちしてます"
      publish_date: 2026-04-29
  atomic_assets:
    - type: x_thread
      tweet_count: 8
      hook_first_tweet: "テストを増やすほど信頼が下がる理由"
      publish_date: 2026-04-25T18:00
    - type: linkedin_post
      angle: "contrarian outcome lesson"
      length_chars: 1200
      publish_date: 2026-04-26
    - type: quote_card
      count: 5
      key_insights: ["...", "...", "...", "...", "..."]
      drip_schedule: "every 2 days"
    - type: newsletter_blurb
      length_words: 90
      publish_date: 2026-05-02
  refresh_plan:
    - days_post_publish: 30
      type: counter
      title: "What I'd change one month later"
    - days_post_publish: 180
      type: anniversary
      title: "Six months of bisect-driven test debugging"
```

## Anti-Patterns

- Copy-pasting identical text to every platform — feeds detect duplicates and downrank.
- Publishing spokes before the hub — flips canonical to the wrong domain.
- Skipping `canonical_url` on dev.to / Medium where it's native.
- Same-day publish across all platforms — looks spammy, dilutes own attention budget.
- Identical hook on X thread and LinkedIn — different audiences, different angles.
- Translating idioms literally instead of localizing — alienates the target audience.
- Quote card series with 5 cards in 1 day — same audience saturation problem.
- Ignoring a high-CTR platform because it "feels off-brand" — let data update the brand.
- Refreshing by re-posting the same URL — no new value; missed opportunity for an internal-link gain.

## Deliverable Contract

A repurposing plan is complete when:

- Hub platform identified with canonical URL.
- Spoke list (3–5) with adapted title / length / voice / CTA per platform.
- Atomic asset list (5–10) with formats and drip schedule.
- Canonical URL strategy confirmed per platform.
- Cadence calendar drafted (1–2 weeks).
- Refresh plan scheduled for evergreen pieces.
- Localization notes if cross-language.

## References

- Gary Vaynerchuk, *Crushing It!* (2018) — content multiplication / pillar-and-cluster framework.
- Andy Crestodina, *Orbit Media Studios* — content atomization research.
- Ross Hudgens, *Siege Media* — repurposing playbooks for SEO-resilient cross-posting.
- [dev.to Editor Guide](https://dev.to/p/editor_guide) — cross-posting and `canonical_url` field (official docs).
- Ahrefs Blog, *Duplicate Content* (2024) — when canonical works and when it doesn't.
- [Sprout Social, *Bluesky Growth Statistics 2026*](https://sproutsocial.com/insights/bluesky-statistics/) — platform reach data for distribution decisions.
- [Semrush AI Overviews Study 2025](https://www.semrush.com/blog/semrush-ai-overviews-study/) — canonical placement vs AI citation rates.
- [Medium Partner Program January 2026 Update](https://medium.com/blog/partner-program-update-starting-january-1-were-rewarding-writing-more-broadly-4907e149e38c) — earnings model changes affecting cross-post strategy.
