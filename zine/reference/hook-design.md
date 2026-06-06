# Hook Design

**Purpose:** Design the opening 100-300 characters that determine whether the article is read past the first screen.
**Read when:** DRAFT phase (before writing the body) and POLISH phase (cutting ChatGPT-residue openers).

## Why Hooks Matter More on Tech Platforms Than Anywhere Else

Tech-blog readers are hyper-literate in skip-signals. They've been trained by years of ChatGPT output, AI-generated content farms, and SEO-juiced "the ultimate guide" posts. The moment they see `本記事では〜` or `In this article, we will discuss`, the scroll wheel moves.

Your hook has one job: earn the second paragraph. Not the whole article. Just the second paragraph.

---

## The Five Hook Patterns

### Pattern 1: Contradiction Hook

**Formula:** `[Commonly accepted truth]. [Twist that undercuts it].`

**When it works:** You have a counter-intuitive insight. The "twist" half is what you'll spend the article proving.

**Examples:**

> CSS-in-JSは最高のDXを提供する。本番環境にデプロイするまでは。

> マイクロサービスはスケールする。ただし組織が先にスケールしていれば、だ。

> Reactは学びやすい。Reactらしく書くのは難しい。

> Type-safetyはバグを防ぐ。コンパイルが通った後に発見されるバグに対しては。

> The simplest API is the REST API. Until you have to version it.

**Why it works:** The reader's brain auto-completes the conventional wisdom, then the twist creates cognitive dissonance. They must read on to resolve it.

**Anti-examples:**
- "CSS-in-JSには一長一短がある。" — no twist, no tension.
- "CSS-in-JSは良くも悪くもある。" — flabby both-sides framing.

---

### Pattern 2: Number Hook

**Formula:** `[Concrete, surprising number + what happened].`

**When it works:** You have a measurable metric that's unexpected. Numbers create immediate credibility and specificity.

**Examples:**

> 30,000行のコードを削除した結果、起動時間が4倍速くなった。

> 月額$48,000のDatadog請求を、$6,000に下げた3ヶ月間の話。

> Playwrightのテスト実行時間を22分から3分に縮めた、1つの設定変更。

> We deleted 12,000 lines of CSS and the page got faster.

> 47人のエンジニアに「PRレビューで最も時間を溶かす瞬間」を聞いた結果。

**Why it works:** Numbers are concrete in a way prose isn't. The reader can't argue with "22 minutes to 3 minutes" — they can only be curious about how.

**Anti-examples:**
- "大幅に高速化しました" — vague, feels like marketing.
- "かなり削減できた" — no number = no credibility.

**Caveat:** Fabricating numbers is a trust-destroying act. Only use real numbers you can back up. If you can't disclose the exact number, say "約4倍" or "roughly an order of magnitude" — readers accept approximation but not fiction.

---

### Pattern 3: Scene Hook

**Formula:** `[Concrete moment in time, sensory detail, specific actor].`

**When it works:** The story has a clear anchor moment you can describe in 1-2 sentences. Scene hooks pull readers into narrative mode.

**Examples:**

> 金曜20時、Slackに「本番落ちてます」の一文が流れた。CTOはちょうど寿司を握り始めたところだった。

> 2023年11月、Datadogのレイテンシーグラフが右肩上がりを続けていた。見ない日が増えていた。

> 「このコード、誰が書いたんですか？」とジュニアに聞かれて、私はgit blameを打った。表示されたのは、3年前の自分の名前だった。

> It was 3am. The deploy had succeeded. Production was on fire.

**Why it works:** Sensory specificity makes the story feel real. "Friday 8pm, Slack" is harder to skip than "we had an incident recently".

**Anti-examples:**
- "先日、インシデントがありました。" — no scene, no anchor.
- "最近、パフォーマンスの問題に直面することが多くなってきました。" — time vague, actor vague.

---

### Pattern 4: Question Hook (Real, Not Rhetorical)

**Formula:** `[A question the reader honestly doesn't know the answer to, which the article will answer].`

**When it works:** The reader shares the uncertainty. The question must be one you actually answer, not a rhetorical device.

**Examples:**

> なぜあなたのテストスイートは信頼されないのか？

> React Server Componentsは、いつ既存のSSRを置き換えるのか？

> Postgresのインデックスが効かなくなる瞬間は、どう検知する？

> Why does `npm install` take 3 minutes on your laptop but 40 seconds on your coworker's?

**Why it works:** Questions activate the reader's curiosity loop — they will feel incomplete until the answer arrives.

**Anti-examples:**
- "あなたは〜を知っていますか？" — rhetorical, insulting.
- "〜について考えたことはありますか？" — vague, no specific question.
- "〜とはなんでしょうか？" — lazy, the article should show not ask.

**Critical rule:** Answer the question. If you open with a question and then don't answer it directly (or pivot to a tangent), the reader feels cheated.

---

### Pattern 5: Stake Hook

**Formula:** `[What the reader loses by not reading this] / [Specific consequence].`

**When it works:** The reader has skin in the game — a near-term risk they're either ignoring or underestimating.

**Examples:**

> これを読まないと、来月のインシデントは確実にあなたから始まる。

> あなたのCI/CD pipelineは、おそらく今この瞬間もシークレットを漏らしている。そして誰も気づいていない。

> Node 18はEOL、しかし本番の半分はまだ動いている。明日からの3週間で起こること。

> 2026年、TypeScript 6.xへの移行コストは、今年の1.5倍になる。

**Why it works:** Losses feel stronger than gains (prospect theory). A stake hook triggers loss aversion and makes skipping the article feel expensive.

**Anti-examples:**
- "〜を理解しておくとよいでしょう" — passive, no stake.
- "知っておいて損はない〜" — damning with faint praise.

**Ethical rule:** Don't manufacture fake stakes. If the "cost of not reading" is actually trivial, readers who follow through feel manipulated and won't return.

---

## Hook Anti-patterns (Cut on Sight)

These openers signal ChatGPT-residue or SEO-content-farm origin. Strip them in POLISH.

| Anti-pattern | Why it fails | Cut to |
|--------------|--------------|--------|
| `本記事では〜について書きます` | Promises meta-info instead of delivering content | Delete, start with the actual content |
| `今回は〜について説明します` | Meta-framing, no hook | Delete, start with the actual content |
| `最近〜が話題です` | Vague appeal to trend, no specificity | Replace with specific event/metric |
| `こんにちは、〜です` | Greeting openers drain attention unless brand voice | Cut unless established brand voice |
| `本記事を通じて〜を学んでいただければと思います` | Preemptive meta-summary; reader hasn't read yet | Delete |
| `In this article, we will discuss` | English-language ChatGPT tell | Delete |
| `As developers, we often face...` | Generic "we" opening | Replace with specific scenario |
| `Have you ever wondered...` | Rhetorical, feels manipulative | Replace with real question or cut |
| `〜とはなんでしょうか？` | Article should show not ask | Show, don't ask |
| `皆さんは〜をご存知ですか？` | Patronizing rhetorical | Delete |
| `近年、〜の重要性が高まっています` | SEO-content-farm opening | Replace with specific trigger |

---

## Platform-Specific Hook Considerations

### note

- **First-line bold effect.** note renders the first line with slight emphasis in article previews. A short, punchy first line (under 40 chars) outperforms long ones.
- **目次 auto-generation** works from H2/H3, so hook sits *above* the TOC — it must land before the reader hits the TOC scroll.
- **Social preview (Twitter Card, OGP)** pulls the first 140 chars — design the hook to work as both first paragraph and OG description.

### Zenn

- **Emoji title icon** sits before the title; pick one that reinforces the hook type (🔥 for stakes, 📉 for numbers, 🤔 for questions).
- **Technical readers skim for code blocks first** — if your article is teaching code, the first code block can act as a visual hook. Consider putting a concise "before/after" snippet within the first 30% of the article.
- **Trending feed preview** shows ~60 chars; front-load the specificity.

### Qiita

- **TL;DR opening convention.** Many Qiita readers expect a `## TL;DR` or `## 要約` section. The hook can either precede this (narrative-first) or BE the TL;DR (direct-first). Direct-first is more common on Qiita.
- **LGTM is code-quality-biased.** Qiita's engagement skews toward "I'll come back to this" bookmarking. A strong utility-signal in the hook ("この3行で〜が解決する") performs well.

### dev.to

- **Cover image 1000×420** sits above the title, so the hook competes with the image for attention. If you have a cover image, the first line should complement, not duplicate, the image's message.
- **Tag feed preview** is short (~100 chars in many clients). Front-load.
- **"Discuss" / "Read more" convention** — dev.to readers often click into discuss tags and comments. A question hook that explicitly invites debate ("am I wrong?") performs well.
- **Emoji-heavy culture** — moderate emoji use in the hook is acceptable on dev.to where it would be considered unprofessional on Zenn/Qiita.

---

## Hook Testing Protocol

Before committing to a hook, run these three mental tests:

1. **The feed-skim test.** Imagine your hook appearing in a list of 20 other article titles + first lines on X, Bluesky, or RSS. Does your hook stop the scroll?
2. **The second-paragraph test.** Would a reader who read only the hook naturally want to read the next paragraph? The hook shouldn't resolve its own tension.
3. **The ChatGPT-residue test.** Read the hook aloud. Does it sound like you, or does it sound like an AI trying to sound like a tech blog? If the latter, rewrite.

---

## Hook Iteration Workflow

1. **Draft three hook variants** covering different patterns (e.g., one contradiction + one number + one scene).
2. **Pick the pattern that matches the article's actual insight** — if your payload is a surprising metric, use number hook; if your payload is a perspective shift, use contradiction hook.
3. **Tighten to 100-300 characters.** Longer hooks lose; too-short hooks lack specificity.
4. **Confirm the hook doesn't spoil the article.** The hook should foreshadow, not summarize.
5. **Sanity-check against anti-patterns.** Strip any residue phrases before locking.

---

> *"The hook is a door, not a summary. Open it just enough to let the reader walk through."*
