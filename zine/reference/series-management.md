# Series Management

**Purpose:** Multi-episode tech blog series require different discipline than one-shot articles — index coherence, cross-links, cadence, tonal continuity. Treat series as a product, not a playlist.
**Read when:** FRAME phase (new series kickoff or integrating an episode into existing series) and PUBLISH phase (updating index + cross-links).

## Why Series Need Their Own Discipline

A standalone article has one job: stand alone. A series episode has three:

1. Stand alone enough that first-time readers get value without reading prior episodes.
2. Reward readers who have been following — callbacks, terminology continuity, narrative threads.
3. Serve the series arc — advance the thesis, don't just exist as another post tagged "series X".

Skip any of these and the series breaks. #1 broken = new readers bounce. #2 broken = loyal readers feel ignored. #3 broken = the series becomes a bag of loosely-related posts with the same prefix.

---

## Index Article Design

The **index article** (often named `#00 Overview`, `Part 0: Introduction`, or similar) is the anchor readers return to. It's also the single most-updated file in the series.

### What the index article contains

```markdown
# [Series Title]

**[One-line thesis of the series]**

[200-400 chars: what this series argues, who it's for, what reader will take away]

## Episode List

- [x] #00 Overview — this article
- [x] #01 [Title] — [one-sentence teaser]
- [x] #02 [Title] — [one-sentence teaser]
- [ ] #03 [Title] — [planned teaser, link added on publish]
- [ ] #04 [Title] — (planned)

## How to Read This Series

[Reading order: chronological / any order / must-read first 3 / etc.]

## Release Cadence

[Weekly Monday 10:00 JST / Biweekly / As-ready — state explicitly]

## About

[Author context, why this series exists]
```

### Update discipline

Every new episode must, in the same pass:

1. Add the episode to the index's Episode List (change `[ ]` to `[x]`, add link).
2. Update the index's "How to read" if the new episode changes the reading order (e.g., "must-read first 3" changes to "first 4").
3. Consider whether the series thesis paragraph needs refinement — a mid-series episode sometimes clarifies the thesis, and the index should reflect.
4. Commit both files together (`feat(series): publish #09 Forge and update index`).

**Anti-pattern:** Publishing the episode and "updating the index later". Later never happens. Readers who land on the index see an outdated list and lose trust.

---

## Cross-Reference Strategy

### Top-of-episode navigation

Every non-index episode opens with a nav strip:

```markdown
> 連載「[Series Title]」第N回。前回: [#N-1 Title]。
> 目次: [#00 Overview]
```

For English (dev.to):

```markdown
> Part N of the "[Series Title]" series. Previous: [#N-1 Title].
> Index: [#00 Overview]
```

### Bottom-of-episode navigation

Every non-index episode closes (before CTA) with:

```markdown
---

- 前回: [#N-1 Title]
- 次回 (予定): [#N+1 Working Title] — [one-line teaser]
- 目次に戻る: [#00 Overview]
```

`次回 (予定)` = tentative. If the series might skip around, say so. If a future episode's title is locked, link it directly.

### In-body back-references

When episode #07 refers to a concept established in #03, link explicitly:

```markdown
（[#03 Concept](link) で触れた「〇〇」を、ここでは実装に落とす。）
```

Readers who skipped #03 have a way back. Readers who remember #03 get a little dopamine hit of continuity. Both wins.

---

## Release Cadence

State the cadence **explicitly in the index article** so readers know what to expect.

| Cadence | Pros | Cons | Fit |
|---------|------|------|-----|
| **Weekly (fixed day/time)** | Reader habit, RSS compatibility, predictable | Pressure, may sacrifice quality for schedule | Established series, author with reliable time |
| **Biweekly** | Breathing room for research-heavy episodes | Readers may lose context between episodes | Deep-dive technical series |
| **Burst (2-3 in a week, gap, burst)** | Natural for topic clusters, momentum | Unpredictable, RSS readers get clumps | Narrative arcs, project retrospectives |
| **As-ready** | Quality over schedule | Series drifts, readers forget it exists | Experimental series, side projects |

**Commitment lever:** If you're writing publicly, a stated weekly cadence forces discipline. The cost is burn-out; the benefit is compounding readership.

**Recovery lever:** When a stated cadence slips (missed a week), address it in the next episode opening: "先週は休載した。理由は〜。今週の #07 から再開する。" Readers respect honesty more than silent gaps.

---

## Naming Convention

Pick one and commit for the entire series:

| Convention | Example | When it fits |
|------------|---------|--------------|
| `#NN Title` | `#00 Overview`, `#01 Concept` | JP / note convention, short and scannable |
| `Part N: Title` | `Part 0: Introduction`, `Part 1: Setup` | English / dev.to convention |
| `Episode NN — Title` | `Episode 01 — Concept` | Longer form, works for narrative-heavy series |
| `[Series]: Title` | `Agent Skills: Forge` | When episode order doesn't matter |

**Hard rule:** Don't change the convention mid-series. If you started with `#00`, you're committed to `#NN` for the arc. Changing conventions mid-series (e.g., switching to `Part N` at episode #05) breaks search, breaks bookmarks, breaks the index.

**Zero-indexing vs one-indexing:** `#00 Overview + #01..#N` treats the overview as a "part zero" meta-episode. `#01 Overview + #02..#N` treats overview as the first real episode. Both are valid; pick one and be consistent.

---

## Tonal Continuity (Series Bible)

Multi-episode series need a lightweight **series bible** to maintain consistency. Store it in `.agents/PROJECT.md` or a dedicated `.agents/zine-series-{name}.md`:

```markdown
## Series Bible: [Series Title]

### Voice
- First person / third person: [choice]
- Formality: [です・ます / だ・である / casual]
- Reader address: [あなた / 読者の皆さん / none]

### Recurring terminology
- エージェント (not AI / bot / 助手)
- スキル (not 能力 / capability)
- [Project-specific terms with definitions]

### Cast of characters (if any)
- [Character name]: [role, first appearance]
- [Character name]: [role, first appearance]

### Recurring metaphors
- [Metaphor]: [when introduced, what it represents]

### Phrases to avoid (beyond universal anti-patterns)
- [Series-specific throat-clearing to cut]

### Episode cadence
- Target: [weekly Monday 10:00 JST]
- Grace period: [+3 days before officially "slipped"]

### Thesis
[The series' core argument, 1-3 sentences — this is what every episode should serve]
```

Before drafting a new episode:
1. Re-read the series bible.
2. Re-read the previous episode's last paragraph (continuity check — does the new episode open naturally from where the last one ended?).
3. Check terminology drift — did the last episode start using a word the bible doesn't sanction?

---

## Finale vs Open-ended

Decide at series kickoff:

### Finale-ending series

- Stated episode count from the start (e.g., "全10回の連載").
- Builds toward a concluding thesis, synthesis, or artifact (a book, a framework, a project).
- Final episode explicitly wraps: "#10 結論" or "Part 10: Conclusion".
- **Risk:** Padding. If the thesis is solid at #6, don't extend to #10 for the sake of commitment.

### Open-ended series

- No stated end. Published as long as material exists and author interest holds.
- Risks series drift — becomes a catch-all tag instead of a coherent arc.
- Mitigation: periodic "state of the series" recap episodes (every ~10 episodes) to re-establish thesis and re-hook readers.
- **Example**: "Claude Skills 図鑑" is open-ended — each episode covers one agent, there's no fixed count.

### Hybrid: arc-based open-ended

- Open-ended but organized into explicit arcs.
- "Part 1 (Episodes #01-#10): Fundamentals" → "Part 2 (#11-#20): Advanced".
- Each arc has a mini-finale, but the series continues.

---

## Downstream Conversion: Series as Artifact

A completed or mature series is prime material for downstream artifacts. Plan this from #00, or at least from mid-series:

| Downstream artifact | How series feeds it | Handoff agent |
|---------------------|---------------------|---------------|
| **PDF zine / ebook** | Concatenate + polish + add cover + TOC | Morph (format conversion) |
| **Zenn Book (paid)** | Restructure as chapters, polish continuity | Self (reformat) + Morph |
| **Conference talk deck** | Extract thesis + 3-5 strongest episode arcs | Stage (slides) |
| **Marketing narrative / customer story** | Reshape as product story, not tech retrospective | Saga |
| **Internal onboarding doc** | Reverse-flow: public series → internal training | Tome |
| **Podcast / audio series** | Re-record with conversational adaptation | (External tool) |

**Plan the anthology at #00**: "This series may become a PDF zine / talk / book." The anticipation changes how you write individual episodes — you write with the eventual anthology in mind (callbacks that work in anthology context, not just feed context).

---

## Live Example: "Agent Skills 図鑑" (user's current project)

Context: note series, #00〜#08 完成, next #09 Forge.

**Observed conventions** (inferred from memory context — verify in the project journal):
- Naming: `#NN AgentName`
- Cadence: as-ready (not weekly)
- Platform: note (Japanese, long-form)
- Open-ended: one episode per agent, series continues as new agents land

**When drafting #09 Forge:**
1. Re-read #08's closing paragraph — continuity check.
2. Re-read #00 Overview — has the agent list been updated to include Forge as "planned"? Update now.
3. Check `.agents/PROJECT.md` for any series-specific terminology or tone conventions established #00-#08.
4. Draft #09 Forge with:
   - Top nav: 前回 [#08], 目次 [#00]
   - Bottom nav: 前回 [#08], 次回 (予定) [#10 ???], 目次に戻る
5. On publish: update #00 Overview to mark #09 as published, and (if known) add #10 as planned with working title.
6. Commit: `feat(zine): publish #09 Forge and update series index`.

---

## Series Kickoff Checklist

When starting a new series:

- [ ] Decide platform (note / Zenn / Qiita / dev.to — platform features vary for series)
- [ ] Decide naming convention (`#NN` / `Part N` / other) and commit
- [ ] Decide cadence (weekly / biweekly / burst / as-ready) and state it in #00
- [ ] Decide ending (finale count / open-ended / hybrid-arc)
- [ ] Draft #00 Overview with thesis, episode list (all known episodes as planned), cadence, how-to-read
- [ ] Create series bible in `.agents/PROJECT.md` or `.agents/zine-series-{name}.md`
- [ ] Set up magazine (note) / series (dev.to) / topic (Zenn) for automatic grouping
- [ ] Plan downstream anthology (PDF? book? talk? — or explicitly decide "just episodes")

## Per-Episode Checklist

For every episode after #00:

- [ ] Re-read series bible
- [ ] Re-read previous episode's last paragraph
- [ ] Check for terminology drift
- [ ] Draft with top-nav and bottom-nav strips
- [ ] Update #00 Overview's episode list (planned → published)
- [ ] Update #00's "how to read" if reading order changed
- [ ] Update previous episode's bottom-nav if it had `次回 (予定): TBD` — fill it in now
- [ ] Add to magazine (note) / series (dev.to)
- [ ] Commit with `feat(series): publish #NN Title and update index`
