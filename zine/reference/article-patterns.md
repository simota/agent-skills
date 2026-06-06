# Article Patterns

**Purpose:** Canonical article structure templates — pick one before drafting, don't let the draft find its own shape mid-write.
**Read when:** FRAME phase — after platform/tone confirmed, before DRAFT begins.

## Contents

- Pattern 1: Problem → Tension → Insight → Solution → CTA (deep-dive default)
- Pattern 2: Tutorial
- Pattern 3: Listicle
- Pattern 4: Retrospective
- Pattern 5: Deep-dive Technical
- Pattern 6: Announcement
- Pattern Selection Matrix
- Anti-patterns

---

## Pattern 1: Problem → Tension → Insight → Solution → CTA

**When to use:** Default for deep-dive articles, opinion pieces, "I learned X the hard way" posts. Works across all platforms.

**Skeleton:**

```
1. HOOK (100-300 chars)
   - See hook-design.md for the five hook patterns
     (contradiction / number / scene / question / stake),
     formulas, anti-patterns, and per-platform tuning.

2. PROBLEM (200-400 chars)
   - Make the reader feel the pain
   - "You've probably tried X. It doesn't work because Y."

3. TENSION (300-600 chars)
   - Twist the knife
   - "Worse, the common fix (Z) makes it harder to debug."
   - "Most advice online misses the actual root cause."

4. INSIGHT (400-800 chars)
   - The frame shift / the "aha"
   - "It turns out the problem isn't X at all — it's W."
   - This is the payload readers take away

5. SOLUTION (600-1500 chars)
   - Concrete, actionable, code-level if applicable
   - Show the fix, not just describe it

6. CTA (100-300 chars)
   - Single-verb action: 試す / 購読する / GitHubで見る
   - Optional: link to follow-up article in series
```

**Pattern-1 specific guidance:** the HOOK→PROBLEM seam is the load-bearing transition. The hook foreshadows the contradiction; the PROBLEM section grounds it in concrete pain (specific incident, code path, metric). Pick a hook pattern in `hook-design.md`, then write PROBLEM so it reads as the next sentence after the hook — not a restart.

**Anti-pattern:** Skipping TENSION. Going straight from PROBLEM → SOLUTION reads like documentation, not an article. The tension is what makes readers keep scrolling.

---

## Pattern 2: Tutorial

**When to use:** Step-by-step instruction. Reader arrives with a specific goal ("set up X", "migrate Y to Z"). Strong on Qiita, Zenn, dev.to.

**Skeleton:**

```
1. HOOK (100-200 chars)
   - "完了すると〜できるようになる" — state the end state
   - Or: "これを試した人の90%が詰まるポイントを先に書く" — stake hook

2. PREREQUISITES (100-300 chars)
   - Version numbers (Node 20.x, Python 3.11+, etc.)
   - OS assumptions
   - Required accounts / API keys
   - Estimated time

3. STEPS (numbered, each independently verifiable)
   Step 1: [Action]
     - Command / code
     - Expected output
     - "If you see X, do Y"

   Step 2: [Action]
     - ...

   Step N: [Action]
     - ...

4. GOTCHAS (bulleted)
   - Common errors with fixes
   - Version-specific traps
   - "If it doesn't work" checklist

5. WHAT'S NEXT (CTA)
   - Link to deeper reading
   - Next tutorial in series
   - "Try variation X" suggestion
```

**Example opener:**

> Claude Codeでカスタムスキルを作る手順を書きます。15分で完走でき、最後には `/my-skill` と打つと発火する自作スキルが動いている状態になります。
>
> 前提: Claude Code v2.x以降、macOS/Linux、`~/.claude/skills/` への書き込み権限。

**Anti-pattern:** Steps that skip expected output. Readers need to confirm they're on the right path at every step — "you should see X" is not decoration, it's the handrail.

---

## Pattern 3: Listicle

**When to use:** Curated collection with a through-line. "5 tools I actually use", "10 anti-patterns in async code". Works well on note, dev.to; use sparingly on Zenn/Qiita (technical readers suspect clickbait).

**Skeleton:**

```
1. HOOK (150-300 chars)
   - Anchor theme — why these N, why now, why together
   - "Not a best-of list. A list of N tools that survived 6 months of daily use."

2. ITEM 1
   - Name + one-line pitch
   - Why it matters (2-4 sentences)
   - Concrete example / screenshot / code
   - Caveat / when-not-to-use

3. ITEM 2 ... ITEM N
   - Same shape, parallel structure

4. SYNTHESIS (200-400 chars)
   - What connects these N items — the through-line
   - What the list is actually saying beyond the items

5. CTA
   - "Which did I miss? Reply with your list."
   - Link to related deep-dive
```

**Key rule:** The through-line earns the list format. If the N items don't share a deeper thesis, the article is a dump — rewrite as separate posts or kill it.

**Ideal N:** 5-9. Fewer than 5 = each item deserves its own post. More than 9 = reader skim-scrolls.

**Example opener:**

> 過去1年で試した開発ツールのうち、半年以上使い続けた5つだけ残った。話題になった派手なものほど早く落ちた。残ったのは地味で、再起動後も起動している、そんなツール群だ。

**Anti-pattern:** Items that don't share a through-line ("10 cool npm packages"). Without the through-line, readers don't know why you grouped them — the article reads as random.

---

## Pattern 4: Retrospective

**When to use:** Project reflection, migration story, postmortem, "we rewrote X" narrative. Strong on note (日本語長文に向く), dev.to (post-mortem culture established).

**Skeleton:**

```
1. HOOK (200-400 chars)
   - Scene hook: concrete moment that started it
   - Or number hook: the metric that forced the change
   - "2023年11月、Datadogのレイテンシーグラフが右肩上がりを続けていた。"

2. CONTEXT (300-600 chars)
   - Where we started — stack, team size, constraints
   - What the original decision optimized for
   - Why it made sense at the time (no 20/20 hindsight)

3. JOURNEY (1000-3000 chars)
   - Chronological, honest
   - Include the wrong turns — readers learn more from "we tried X and it failed because Y" than from clean narratives
   - Mark decision points with the info you had at the time

4. LESSONS (400-800 chars)
   - What we'd tell past-self
   - What's transferable vs project-specific
   - What still isn't solved

5. CTA
   - "Happy to talk through specifics — reach out."
   - Or link to the open-source artifact if one resulted
```

**Key rule:** Honest retrospectives land harder than polished ones. If every decision looks smart in retrospect, readers smell sanitization.

**Internal-leak checklist before publish:**
- [ ] Client/customer names masked or explicitly cleared
- [ ] Unreleased features not mentioned
- [ ] Internal service names / infrastructure details removed
- [ ] Team member names only with their consent
- [ ] Specific cost numbers / revenue numbers only if publicly disclosed

**Example opener:**

> Datadogの月次請求が$48kを超えた日、CTOが会議室でiPadを静かに置いた。誰も何も言わなかった。翌週、私たちはログ基盤を作り直すことになった。

**Anti-pattern:** The "everything went smoothly" retrospective. If nothing went wrong, it's marketing, not a retrospective.

---

## Pattern 5: Deep-dive Technical

**When to use:** Mechanism explainers, architecture posts, "how X actually works" articles. Strong on Zenn, Qiita, dev.to. Can work on note if framed with narrative entry.

**Skeleton:**

```
1. HOOK (150-300 chars)
   - Question hook (real, not rhetorical)
   - Or contradiction hook ("The common explanation is X. That explanation is wrong.")

2. HISTORY / CONTEXT (400-800 chars)
   - Where this mechanism came from
   - What problem it was designed to solve
   - Why previous approaches didn't work

3. MECHANISM (1500-4000 chars)
   - How it actually works — no hand-waving
   - Diagrams where useful (hand off to Canvas)
   - Code-level detail when relevant
   - Reference the spec / source / paper

4. IMPLICATIONS / TRADE-OFFS (500-1000 chars)
   - What this enables
   - What this costs
   - When it's the wrong choice

5. CTA
   - Link to spec / source reading
   - Follow-up article in series
   - "Try implementing a minimal version"
```

**Key rule:** No hand-waving. If you can't explain a step, either learn it or mark it as "out of scope for this post, see [spec link]". Faking explains drops reader trust instantly.

**Example opener:**

> React Server Componentsが「サーバーで動くReact」と説明されるとき、それは技術的には間違っていないが、実装を理解するのには邪魔になる。RSCの本質は、Reactの要素木をシリアライズ可能なストリームに変換する一連の規約だ。

**Anti-pattern:** Explaining by analogy without ever showing the mechanism. Analogies are entry ramps, not the road.

---

## Pattern 6: Announcement

**When to use:** Launches, releases, feature news, OSS publication. Works everywhere but note tends to want narrative wrapping, dev.to likes structured release posts.

**Skeleton:**

```
1. NEWS (1 sentence, bolded or H2)
   - "X is live." / "v2.0をリリースした。"

2. WHY IT MATTERS (300-600 chars)
   - Reader-first: what this changes for the reader
   - NOT: "we built X using Y" (internal framing)
   - YES: "you can now do Z without Y" (reader framing)

3. DEMO (with screenshot / gif / code)
   - Minimum viable example
   - "Here's what it looks like"
   - Include link to full demo / playground

4. WHAT CHANGED (bulleted)
   - Breaking changes first, flagged clearly
   - New features
   - Deprecations with timeline

5. WHERE TO GO (CTA block)
   - Docs link
   - Install command
   - Upgrade guide
   - Issue tracker for feedback
```

**Key rule:** "Why it matters" before "what changed". Changelog-first announcements fail because they demand the reader care before explaining why they should.

**Example opener:**

> **Claude Skills v1.0がリリースされた。**
>
> これで何が変わるかというと、エージェントを一つずつ手動で起動する必要がなくなる。 `/nexus` に投げると、タスクを分解して適切なエージェント連鎖を自動生成し、結果を返す。

**Anti-pattern:** Leading with a changelog dump. Even OSS readers want the "why" before the "what".

---

## Pattern Selection Matrix

| Situation | Pattern | Why |
|-----------|---------|-----|
| "I learned X the hard way" / opinion piece | **1. Problem-Tension-Insight-Solution-CTA** | Default for insight-driven content |
| "How to set up X" / "Migrate from A to B" | **2. Tutorial** | Goal-oriented, step-verifiable |
| "N tools / patterns / mistakes" | **3. Listicle** | Works if through-line is strong |
| "We rewrote X" / "Our migration from Y" | **4. Retrospective** | Chronological, honest, lessons-focused |
| "How X actually works" / mechanism explainer | **5. Deep-dive Technical** | Mechanism-first, no hand-waving |
| "We launched X" / "v2.0 released" | **6. Announcement** | Why-first, then what |
| Unsure | **1. Problem-Tension-Insight-Solution-CTA** | Safe default for almost any topic |

---

## Anti-patterns

Avoid these structural failures regardless of chosen pattern:

- **Encyclopedia-order info dump.** Listing everything the author knows about a topic without a through-line. Symptom: H2 headings are topic areas, not arc beats.
- **Buried lede.** The actual insight appears in section 7. Rewrite so the hook foreshadows it and section 2 or 3 delivers.
- **Orphan sections.** An H2 that doesn't earn its place in the arc. Cut or demote to a bullet under its parent.
- **CTA-less ending.** "Hope this helps!" wastes the one moment readers are most engaged. Replace with specific verb.
- **No reader-breath points.** Unbroken walls of text past 600 characters. Break with subheading, blockquote, code block, or a one-sentence paragraph acting as visual punctuation.
- **Pattern mismatch.** Using Tutorial structure for a deep-dive question ("how does X work" delivered as numbered steps reads as shallow). Match pattern to intent.
