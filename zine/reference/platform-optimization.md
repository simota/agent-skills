# Platform Optimization

**Purpose:** Platform-specific tuning for note / Zenn / Qiita / dev.to. Same draft, different platforms = different length, metadata, tone, and discoverability levers.
**Read when:** FRAME phase (deciding platform) and PUBLISH phase (applying platform-specific metadata).

## Platform Decision Matrix

| Factor | note | Zenn | Qiita | dev.to |
|--------|------|------|-------|--------|
| Audience | 日本語読者、ビジネス/クリエイティブも混在 | 日本語エンジニア、技術コミュニティ | 日本語エンジニア、Tips志向 | English global, friendly dev community |
| Length sweet spot | 3000-6000字 | 2000-5000字 | 1500-4000字 | 1000-2500 words |
| Tone expectation | Personal, narrative OK | Technical, clean | Technical, Tips-first | Friendly, conversational |
| Code-heavy welcomed | Moderate | High | Very high | High |
| Narrative-first welcomed | Very high | Moderate | Low | High |
| Monetization path | 有料記事, マガジン購読, サポート | 本販売 (書籍機能), 企業スポンサー | Organizations (企業), LGTM社内評価 | Official cross-post traffic, dev community brand |
| Series feature | マガジン | Book (paid) + トピック | Organization series weak | Series feature (native) |
| GitHub integration | No | Yes (.md commit-based publish) | No | Yes (markdown-friendly API) |
| SEO default | Good (note.com authority) | Good (trending boost) | Good (trending boost) | Good (dev.to authority) |

---

## note

### Core Characteristics

- Primary JP platform for long-form content. Not exclusively tech — readers mix business/creative/lifestyle, so tech-bubble jargon needs more unpacking.
- **マガジン** = series container. Readers subscribe to a magazine to get notifications on new episodes. Critical for multi-episode series.
- **目次 auto-generation** from H2/H3 headings. A clear hierarchy produces a clear TOC.
- Paid articles, supporter tips (サポート), and magazine subscriptions are native monetization.
- **AI学習対価還元プログラム** (started August 1, 2025): note provides creator text to partnered AI companies and returns revenue to creators. Opt-out is available. Covers free/paid articles and membership content (images/audio/video excluded). Source: [help-note.com FAQ](https://www.help-note.com/hc/ja/articles/44723422427417)
- **AI流入**: note is ranked #2 as a source cited by AI assistants (after Wikipedia) as of 2025, due to its concentration of first-hand experience and primary-source writing. Source: [note.com/info](https://note.com/info/n/n49bbcbdefe1a)
- Google capital tie-up (January 2025): note raised ~¥489M from Google and announced a partnership to develop features using Gemini.

### Metadata

| Field | Rule |
|-------|------|
| タイトル | 32字程度が推奨。モバイルで見切れにくい |
| 見出し画像 | 1280×670 推奨。iPhone横幅フィット |
| タグ | 3-5個。1つをprimary (最も狭い粒度), 残り2-4をbroader discoverability |
| マガジン | 連載は必ず所属させる。単発でも関連マガジンがあれば追加 |
| 有料設定 | 全文無料 / 一部有料 / 全文有料 — 序盤200-400字は必ず無料で読めるよう配置 |
| AI学習提供設定 | デフォルトON。提供したくないコンテンツはヘルプセンターから除外設定可 |

### Hook / Structure / CTA

- **Hook**: note-literate readers (特にクリエイター層) skip at `本記事では`. Use scene or contradiction hooks aggressively.
- **Structure**: First line bold effect + TOC above-the-fold = 目次 が見えるまでにhookが完結している必要がある。H2を6-8個以下に抑えると TOCが見やすい。
- **CTA**: マガジン購読, サポート (投げ銭), 次回 (series), SNSシェア。複数CTAは読者を迷わせるので **1つに絞る** のが鉄則。
- Closing: 「〜と思っています。」「〜という気がしています。」などのpersonal-tone closingが効きやすい。formalすぎると note らしくない。

### Anti-patterns on note

- Pure changelog dump (readers expect narrative wrapping).
- Over-technical jargon without unpacking — note audience includes non-engineer readers even for tech articles.
- Treating magazines as an afterthought — add to the right magazine *at publish time*, not later.

---

## Zenn

### Core Characteristics

- Built for engineers. Technical rigor expected.
- **GitHub-linked articles** (`zenn-cli`) = articles as `.md` files in a repo, publish via `git push`. Enables version control and collaborative editing.
- **Article types**: `Tech` (技術記事) vs `Idea` (ポエム・考察). Pick one at publish — different discoverability pools.
- **Scrap** = live note/thread format, separate from articles. Use for work-in-progress exploration or Q&A-style threads, not for finalized articles. Since March 2025, scraps support **限定公開 (unlisted)** — useful for draft-stage exploration or team-internal threads. Source: [info.zenn.dev](https://info.zenn.dev/2025-03-05-release-unlisted-scrap)
- **Book feature** = paid long-form (several chapters). For a deep series you want to monetize, a Zenn Book is often stronger than a series of articles.
- **Publication Pro** (2025): Organization-level publications can now force-unpublish member articles (admin control). Dashboard scrap management gained filter + sort (December 2025). Source: [info.zenn.dev](https://info.zenn.dev/)

### Metadata

| Field | Rule |
|-------|------|
| emoji (絵文字) | 1字。トピックを象徴するもの (📉, 🚀, 🔥, 🤔, 🧪 等) |
| type | `Tech` or `Idea`. 迷ったら Tech |
| topics | 最大5つ。公式トピック (react, typescript 等) を優先。独自トピックは避ける |
| published | false で下書き、true で公開 |
| published_at | 予約投稿可能 (`zenn-cli` 限定) |

### Hook / Structure / CTA

- **Hook**: Technical readers are patient enough for 1-2 paragraphs of setup, but still reject `本記事では` openers. Contradiction and question hooks work particularly well on Zenn.
- **Structure**: Code-first readers scan for the first code block. Place a "before/after" or "minimal reproduction" code snippet in the first 30% of the article to signal value immediately.
- **CTA**: GitHub リンク (repo, code example), 続編の Scrap, トピック購読, Twitter share。Zenn readers respond well to "here's the repo, fork it" CTAs.
- Closing: 「以上です」でもZennでは許容される (技術記事のdry closureは期待内)。ただし CTA は別途必要。

### GitHub integration workflow

1. `npx zenn-cli init` in the repo
2. `npx zenn-cli new:article --slug {slug}`
3. Edit the front-matter + body in `.md`
4. `git push` to the linked repo → Zenn auto-publishes on next sync

The canonical version lives in git. Useful for: series where articles reference each other's code examples (can pin to commit hash), or articles you want co-authored via PR review.

### Anti-patterns on Zenn

- Posting as `Idea` when it's actually technical (and vice versa) — mismatched article type drops discoverability.
- More than 5 topics — the 6th silently drops, but also reads as SEO-spammy.
- Treating Scrap as a blog — Scrap is designed for threads/exploration, not polished articles.

---

## Qiita

### Core Characteristics

- Longest-running JP engineer platform. Heavy Tips / how-to culture.
- **TL;DR / 要約 convention** — readers expect a summary at the top, sometimes as the entire takeaway.
- **LGTM** (formerly いいね) = bookmark + upvote hybrid. Signal of "I'll come back to this" more than "I agree".
- **Organizations** = company/team accounts. Articles posted under an Organization feed into that org's page (useful for tech-brand building).
- **タグ** are the primary discoverability mechanism — trending tags drive most traffic.

### Metadata

| Field | Rule |
|-------|------|
| タグ | 5個まで。1つをprimary tech (react, python 等), 残りをサブテクや問題領域 |
| Organization | 所属している場合は選択。個人記事なら空 |
| 限定共有 | 下書き共有に使える (URL-only access) |
| LGTM | いいね から改称 (2020)。現在は LGTM で統一 |

### Hook / Structure / CTA

- **Hook**: Qiita readers skim heavily. A strong `## TL;DR` at the top can function as the hook — directly state the 1-3 line takeaway.
- **Structure**: `## TL;DR` → `## 問題` → `## 解決` → `## 詳細` is the default scaffold. Deviation from this shape is fine but should be deliberate.
- **Code blocks dominate** — Qiita articles are often 40-60% code. Use language hints (` ```typescript`, ` ```bash`) aggressively for syntax highlighting.
- **CTA**: GitHub Gist / repo link, 関連記事 internal-link, Qiita follow, X (Twitter) share. LGTM への誘導は逆効果 (押し付けがましい)。
- Closing: 「以上です」「参考になれば幸いです」で締めるのが Qiita 文化 (note ほど personal tone を期待されない)。

### Archive vs Update strategy

Qiita articles age fast — framework versions, CLI tools, API surface all change. Two options for old-but-popular articles:

- **Archive**: Add a top-level banner like `> **注意**: この記事は2021年の情報です。現在のX.Yでは〜`. Readers appreciate honesty; SEO traffic keeps flowing.
- **Update-in-place**: Rewrite while preserving the URL. Add `## 更新履歴` at the bottom. Preserves SEO equity while keeping content current.

Never silently let articles rot — Qiita's credibility depends on information freshness.

### Anti-patterns on Qiita

- Narrative-heavy openers (`金曜20時にSlackが〜`) — Qiita readers want the Tip fast, the story is a distraction.
- Skipping TL;DR — readers who can't find the summary in 3 seconds bounce.
- Monetization pitches — Qiita has no native paid content; promotional content hurts LGTM rates.

---

## dev.to

### Core Characteristics

- Primary English-speaking dev community with friendly, less-gatekeeping culture.
- **Cover image** (1000×420 recommended) sits prominently above the title — affects feed skim rate.
- **Liquid tags** (e.g., `{% youtube VIDEO_ID %}`, `{% github USER/REPO %}`, `{% codepen URL %}`) enable rich embeds without raw HTML.
- **Series feature** (native) — specify `series: "your series name"` in front-matter, dev.to auto-generates prev/next navigation across episodes.
- **Cross-post friendly** — `canonical_url` front-matter field tells search engines the primary location, avoiding duplicate-content penalty when cross-posting from your own blog or Zenn/note.

### Metadata (front-matter)

```yaml
---
title: "Your article title"
published: false
description: "1-2 sentence meta description, ~155 chars for SEO"
tags: javascript, typescript, webdev, tutorial  # max 4
cover_image: https://example.com/cover-1000x420.png
series: "Agent Skills Field Guide"  # optional, for series nav
canonical_url: https://note.com/yourname/n/primary-version
---
```

### Tag strategy

- Maximum **4 tags**. Over-4 silently drops the extras.
- Mix: 1 primary tech (`javascript`), 1 topic (`webdev`), 1 content-type (`tutorial` / `discuss` / `showdev`), 1 niche (`typescript` / `react`).
- Avoid hyper-broad like `programming` — too competitive.

### Hook / Structure / CTA

- **Hook**: dev.to culture rewards friendliness. Question hooks that invite discussion ("am I wrong?", "what would you do?") perform well.
- **Structure**: Scannable H2s, short paragraphs (2-4 sentences), generous code block use. Readers on mobile are common — avoid unbroken walls.
- **Emoji is accepted** — moderate emoji use in H2 headings (🚀 Getting Started, 🔧 Setup, 🎯 Conclusion) is cultural norm, not cringe.
- **CTA**: Discuss tag, GitHub repo, follow on dev.to, X (Twitter), Bluesky. "Let me know what you think in the comments" actually gets comments here, unlike most platforms.
- Closing: Conversational sign-offs ("Happy coding!", "Let me know your thoughts!") are fine on dev.to where they would feel amateur elsewhere.

### Cross-post strategy

If primary publish is note (Japanese) and you want dev.to English reach:

1. Publish on note first (canonical).
2. Translate + adapt to English (not literal translation — idioms, examples, cultural references should all adjust).
3. Set `canonical_url` in dev.to front-matter to the note URL.
4. Adjust length — dev.to English audiences prefer 1000-2500 words, shorter than note's 3000-6000字 norm.
5. Adjust examples — Japanese-context examples (「〇〇商社の本番環境」) may not resonate; swap for globally-familiar scenarios.

### Anti-patterns on dev.to

- Literal translation of Japanese articles — cultural references and idiom mismatches kill readability.
- Cover image that's just the title in bold (every other article does this; stand out).
- Missing `canonical_url` on cross-posts — SEO duplicate-content penalty affects both locations.
- Tags over 4 — the 5th+ silently drops, looks sloppy.

---

## SEO Considerations for Tech Blog Platforms (2025-2026)

Tech platforms (note, Zenn, Qiita, dev.to) inherit the domain's SEO authority, so on-page SEO is less make-or-break than on a self-hosted blog. Still:

| Lever | Impact | Applied by |
|-------|--------|-----------|
| Title length + specificity | Medium | You (platform-agnostic) |
| H-tag hierarchy (H1 → H2 → H3) | Medium | You (ensures crawl + reader parsing) |
| First 155 chars / first 40-60 words (atomic answer) | High | You — put conclusion/answer in first 1/3 of article; 44.2% of AI citations come from this zone |
| Internal links to other articles | Medium | You (boost within-platform navigation) |
| Canonical URL (cross-post) | High for cross-post | You (in front-matter for dev.to; in URL settings for note/Zenn) |
| Keywords naturally in H2s | Low | You (don't stuff, don't avoid) |
| Schema.org JSON-LD | Medium | Platform auto (you don't control) |
| Page load speed | Low (platform-hosted) | Platform |
| E-E-A-T signals (author credibility, sourcing) | High (2025+) | You — cite sources, link primary docs, use real names/profiles |

### Google AI Overviews & Bing Generative Search (2025-2026)

AI Overviews appeared on 48% of all Google queries as of March 2026 (up from 34.5% in December 2025), reducing organic CTR by 15-46% depending on query type. However, pages that earn citations _inside_ AI Overviews can see CTR increases of up to 35%. Key tactics for earning AI citations:

- Front-load a self-contained answer (40-60 words) that directly addresses the title question.
- 85% of AI Overview citations come from content published in the last two years — freshness matters more than ever.
- Transparent sourcing and E-E-A-T signals (first-hand experience, named author, cited sources) increase AI citation probability.
- Keyword stuffing is actively penalized by Google's December 2025 and February 2026 updates; write for readers, not crawlers.

Source: [stackmatix.com AI Overviews 2026](https://www.stackmatix.com/blog/google-ai-overview-seo-impact), [Semrush AI Overviews Study 2025](https://www.semrush.com/blog/semrush-ai-overviews-study/)

**Growth handoff**: if SEO strategy matters (product launch post, evergreen educational content), hand off to Growth after draft completion with: title candidates (3-5), meta description draft, H-tag outline, target keyword list. Zine does not do keyword research.

---

## OG Image Strategy

Each platform handles OG images differently:

- **note**: 見出し画像 = OG image (1280×670). Same asset for article cover and social share.
- **Zenn**: Auto-generated OG card with emoji + title on colored background. No custom override via zenn-cli.
- **Qiita**: Auto-generated OG card. No custom upload.
- **dev.to**: `cover_image` = OG image (1000×420). Custom upload.

For custom OG asset generation (beyond platform default), hand off to Growth (OG/social card design) or Sketch (image generation).

---

## Quick-Reference Checklist per Platform

**note:**
- [ ] First line < 40 chars, designed for bold rendering
- [ ] 見出し画像 1280×670
- [ ] タグ 3-5 (1 primary, 2-4 broader)
- [ ] マガジン に追加 (if series)
- [ ] 有料設定確認 (全文無料 / 一部有料 / 全文有料)
- [ ] 目次が自動生成されることを前提にH2/H3階層を整える

**Zenn:**
- [ ] emoji 1字, article type (Tech / Idea), topics max 5
- [ ] 冒頭30%にcodeブロック配置 (technical readers scan for code)
- [ ] GitHub連携ならリポジトリのmain branchにpushでpublish
- [ ] published: false で下書き確認

**Qiita:**
- [ ] `## TL;DR` or `## 要約` at top
- [ ] tags max 5 (1 primary tech + 2-4 sub)
- [ ] Organization所属の場合は選択
- [ ] コードブロックの言語ヒント正確に
- [ ] 古い記事なら `> **注意**: この記事は〜` の注記を検討

**dev.to:**
- [ ] Front-matter: title, description (~155 chars), tags (max 4), cover_image (1000×420)
- [ ] `canonical_url` if cross-posting
- [ ] `series:` if part of a series (auto prev/next nav)
- [ ] Scannable H2s, short paragraphs (mobile readers common)
- [ ] Emoji in H2 headings is acceptable (cultural norm)
