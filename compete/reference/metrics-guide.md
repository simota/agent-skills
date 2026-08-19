# Metrics Guide

**Purpose:** Channel-specific KPI definitions, Brand Health Score calculation, and platform algorithm insights.
**Read when:** AUDIT or MEASURE mode — user needs brand health diagnosis or performance tracking.

---

## Brand Health Score (BHS)

### Overview

A composite score (0-100) measuring overall brand presence across channels. Calculated per-channel then aggregated.

### Calculation

```
BHS = Σ (Channel_Score × Channel_Weight) / Σ Channel_Weight
```

### Channel Weights (Default)

| Channel | Weight | Rationale |
|---------|--------|-----------|
| GitHub | 25 | Technical credibility foundation |
| LinkedIn | 20 | Professional network and visibility |
| Tech Blog (Qiita/Zenn/own) | 20 | SEO and thought leadership |
| X (Twitter) | 15 | Real-time presence and networking |
| Conference/Talks | 10 | Authority and community reputation |
| YouTube/Video | 5 | Growing but optional |
| Newsletter | 5 | Deep audience relationship |

**Rule:** Weights are adjustable based on user's goals. Career-focused → increase LinkedIn. OSS-focused → increase GitHub. Thought leadership → increase Blog/Talks.

---

## Channel Scorecards

### GitHub (0-100)

| Factor | Weight | Scoring Criteria |
|--------|--------|-----------------|
| Profile README | 15 | Exists with positioning, tech stack, featured work |
| Pinned Repos | 20 | 4-6 repos with clear READMEs, aligned with niche |
| Contribution Consistency | 20 | Regular commits (weekly+), not just bursts |
| Repo Documentation | 15 | READMEs, CONTRIBUTING, clear code comments |
| Stars/Forks (relative) | 10 | Growth trend matters more than absolute count |
| OSS Contributions | 10 | PRs to external projects in your niche |
| Community Engagement | 10 | Issues, discussions, code reviews |

### LinkedIn (0-100)

| Factor | Weight | Scoring Criteria |
|--------|--------|-----------------|
| Headline Optimization | 15 | Contains tech stack + domain keywords |
| About Section | 20 | Positioning statement + quantified achievements |
| Experience (Impact) | 20 | Results-first descriptions with metrics |
| Featured Content | 15 | 3-5 pinned items, updated quarterly |
| Posting Activity | 15 | 2+ posts/month with engagement |
| Endorsements/Recs | 10 | Skills endorsed, recommendations from peers |
| Profile Completeness | 5 | Photo, banner, contact info, certifications |

### Qiita (0-100)

| Factor | Weight | Scoring Criteria |
|--------|--------|-----------------|
| Contribution Score | 20 | Total Contribution value (platform metric) |
| Article Quality | 25 | LGTM rate per article, technical accuracy |
| Tag Consistency | 15 | Articles cluster around niche-related tags |
| Stock Count | 15 | Articles bookmarked for reference |
| Posting Frequency | 15 | 2+ articles/month for growth phase |
| Organization | 10 | Active in org if employed (team branding) |

### Zenn (0-100)

| Factor | Weight | Scoring Criteria |
|--------|--------|-----------------|
| Article Likes | 20 | Like count and growth trend |
| Book Publication | 20 | Published Books (systematic content series) |
| Scrap Activity | 10 | Active learning log via Scraps |
| Follower Growth | 15 | Monthly follower increase |
| Content Depth | 20 | Long-form, code-heavy, original analysis |
| Badge Revenue | 15 | Badges received (audience willingness to pay) |

### note (0-100)

| Factor | Weight | Scoring Criteria |
|--------|--------|-----------------|
| Suki (Like) Count | 20 | Engagement rate per article |
| Follower Growth | 15 | Monthly increase |
| Content Variety | 15 | Mix of free + premium content |
| Revenue | 20 | Paid article sales, magazine subscribers |
| Cross-audience Reach | 20 | Non-engineer engagement (comments, shares) |
| Posting Consistency | 10 | Regular cadence maintained |

### X / Twitter (0-100)

| Factor | Weight | Scoring Criteria |
|--------|--------|-----------------|
| Bio Optimization | 10 | Positioning + niche keywords |
| Follower Quality | 15 | Industry-relevant followers vs bots |
| Engagement Rate | 25 | Replies + RTs + likes / impressions |
| Thread Quality | 20 | Well-structured technical threads |
| Posting Consistency | 15 | Daily or near-daily activity |
| Network Effects | 15 | Interactions with peers, mentions, spaces |

### YouTube (0-100)

| Factor | Weight | Scoring Criteria |
|--------|--------|-----------------|
| Subscriber Count | 15 | Growth trend over absolute |
| Watch Time | 25 | Total and per-video average |
| Upload Consistency | 20 | Regular schedule maintained |
| Audience Retention | 20 | Average % watched per video |
| Shorts Performance | 10 | View count and conversion to subscribers |
| Community Tab | 10 | Polls, posts, engagement |

### Conference/Talks (0-100)

| Factor | Weight | Scoring Criteria |
|--------|--------|-----------------|
| Talk Count (annual) | 20 | 2+ talks/year minimum |
| Venue Scale | 15 | Mix of local → regional → national |
| Slide Publication | 20 | Speaker Deck/SlideShare with views |
| Post-talk Content | 20 | Blog recap, video recording available |
| CFP Acceptance Rate | 15 | Track record of acceptances |
| Audience Feedback | 10 | Ratings, comments, follow-up connections |

---

## Platform Algorithm Insights

### X (Twitter) — Signal Weights (2026)

| Signal | Relative Weight | Actionable Insight |
|--------|----------------|-------------------|
| Reply | 27× like value | Reply to others' content actively |
| Conversation (multi-reply) | 150× like value | Engage in technical discussions |
| Bookmark | 5× like value | Create save-worthy reference content |
| External link (technical articles) | Boosted (2026 shift) | Links to dev.to, Substack, personal blogs now algorithmically promoted — combine with thread summary for best reach |
| Hashtags | 1-2 niche: +21% / 3+: −40% | Minimal use; algorithm relies on semantic embeddings |
| Initial velocity | Critical (30-60 min) | Post when audience is active |
| Premium account | ~4× reach boost vs free | Consider Premium for consistent developer content |

> Note: X reversed its external link suppression policy in early 2026 specifically for article/blog links. Non-Premium accounts still see weaker median engagement on linked posts. [Source: Sprout Social — Twitter Algorithm 2026](https://sproutsocial.com/insights/twitter-algorithm/)

### YouTube — Ranking Factors

| Factor | Weight (2025-2026) | Actionable Insight |
|--------|-------------------|-------------------|
| Viewer satisfaction | High | Optimize for watch-through, not clicks |
| Long-term retention | High | Build returning viewers |
| Click-through rate | Medium | Thumbnail + title optimization |
| Watch time | Medium | 8-15 min sweet spot for tutorials |
| Shorts views | Growing | 700B+ daily views; use for discovery |

### TikTok — Key Metrics

| Metric | Priority | Target |
|--------|----------|--------|
| Watch time (% completion) | #1 | > 70% completion |
| First 3 seconds retention | Critical | Hook immediately |
| Engagement rate | Benchmark | > 3.15% (platform average) |
| Share rate | High value | Create shareable moments |

### Instagram — Algorithm (2025-2026)

| Signal | Impact | Strategy |
|--------|--------|----------|
| DM shares | #1 ranking signal | Create content people want to send |
| Saves | High | Carousel tutorials get saved |
| Reels reach | Primary discovery | 2-4 Reels per week |
| SEO keywords | Growing (Google index) | Keywords in captions + screen text |

---

## KPI Tracking Template

### Monthly Report Format

```markdown
## Brand Health Report — [Month YYYY]

### Overall BHS: [Score]/100 (MoM change: +/-[N])

### Channel Summary
| Channel | Score | Trend | Key Metric | Action |
|---------|-------|-------|------------|--------|
| GitHub | [N] | [↑↓→] | [key metric] | [next action] |
| LinkedIn | [N] | [↑↓→] | [key metric] | [next action] |
| Blog | [N] | [↑↓→] | [key metric] | [next action] |
| X | [N] | [↑↓→] | [key metric] | [next action] |
| Talks | [N] | [↑↓→] | [key metric] | [next action] |

### Top Wins
- [Win 1]
- [Win 2]

### Gaps Identified
- [Gap 1 + remediation]
- [Gap 2 + remediation]

### Next Month Focus
- [Priority 1]
- [Priority 2]
```

---

## Vanity Metrics vs Impact Metrics

| Vanity Metric | Why It Misleads | Impact Alternative |
|--------------|----------------|-------------------|
| GitHub stars | Can be gamed, no usage indicator | Downloads, dependent repos, contributor count |
| Twitter followers | Bots, inactive accounts | Engagement rate, reply quality, DM conversations |
| Page views | Empty traffic | Time on page, scroll depth, return visits |
| LinkedIn connections | Mass connecting | Profile views from target audience, inbound messages |
| YouTube subscribers | Inactive subscribers | Average view %, returning viewers, comments |

**Rule:** Always pair a vanity metric with an impact metric. AP-2 (Vanity Metrics) applies when only vanity metrics are cited.
