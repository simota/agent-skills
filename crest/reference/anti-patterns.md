# Anti-Patterns

**Purpose:** Self-branding anti-pattern detection rules and platform-specific pitfalls.
**Read when:** REFINE phase of any mode — apply AP checks to all outputs before delivery.

---

## Core Anti-Patterns (AP-1 ~ AP-7)

Applied to **every** Crest output. All must pass before delivery.

### AP-1: Resume Dump

**Signal:** Raw skill/experience lists without narrative, context, or impact framing.

| Detection | Examples |
|-----------|---------|
| Bullet-only format | "Python, Java, Go, React, AWS, Docker, K8s..." |
| No impact statements | "5年の経験" without what was achieved |
| Technology laundry list | GitHub bio listing 20+ technologies |

**Fix:**
- Convert each item to impact format: "Achieved [quantitative result] in [outcome] with [Technology]"
- Limit to 5-8 core technologies aligned with niche
- Add narrative arc: why you chose this path, what you learned

**Severity:** Medium — fixable by restructuring existing content.

---

### AP-2: Vanity Metrics

**Signal:** Metrics cited for impressiveness without demonstrating real impact.

| Detection | Examples |
|-----------|---------|
| Stars without usage | "My repo has 500 stars" (but 0 dependents) |
| Followers without engagement | "10K followers" (but 0.1% engagement) |
| Lines of code | "100K行のコードを書きました" |

**Fix:**
- Pair every vanity metric with an impact metric (see `metrics-guide.md`)
- Replace "stars" with "weekly downloads" or "contributor count"
- Replace "followers" with "engagement rate" or "inbound opportunities"

**Severity:** Medium — misleads audience and recruiters.

---

### AP-3: Niche Absence

**Signal:** Positioning so broad that it provides no differentiation.

| Detection | Examples |
|-----------|---------|
| L0 positioning | "フルスタックエンジニア", "何でもやります" |
| No domain specified | Pure technology listing without industry context |
| Contradictory signals | Cloud expert + Mobile expert + ML expert + Blockchain expert |

**Fix:**
- Apply Tech×Domain×Perspective framework (`positioning-frameworks.md`)
- Target L2 minimum, L3 ideal
- If genuinely multi-skilled, pick one niche for branding and mention others as secondary

**Severity:** High — without niche, all other branding efforts are diluted.

---

### AP-4: Channel Scatter

**Signal:** Inconsistent messaging, positioning, or persona across platforms.

| Detection | Examples |
|-----------|---------|
| Different headlines | LinkedIn: "Backend Engineer" / GitHub: "Full-stack Developer" / X: "Tech Enthusiast" |
| Tone mismatch | Professional on LinkedIn, trolling on X |
| Abandoned channels | Last LinkedIn post 2 years ago, active on X |

**Fix:**
- Create unified positioning statement and adapt (not change) per platform
- Audit all channels quarterly for consistency
- Deactivate or redirect channels you don't maintain

**Severity:** High — confuses audience and weakens brand recognition.

---

### AP-5: AI Ghost

**Signal:** Content that sounds generated, lacks personality, or is indistinguishable from AI output.

| Detection | Examples |
|-----------|---------|
| Generic phrasing | "In today's rapidly evolving tech landscape..." |
| No personal anecdotes | Technical content without "I" or personal experience |
| Perfect but soulless | Grammatically perfect but reads like documentation |
| Template-obvious | Every article follows identical structure |

**Fix:**
- Add 1+ personal anecdote per article (failure, surprise, learning moment)
- Include opinions and hot takes (with reasoning)
- Use conversational language specific to your personality
- Break templates occasionally with unique formats

**Severity:** High (growing) — audiences increasingly detect and distrust AI-generated content.

---

### AP-6: Employer Leak

**Signal:** Public content that exposes employer confidential information.

| Detection | Examples |
|-----------|---------|
| Architecture details | "弊社では[specific internal system]を使って..." |
| Unreleased features | Discussing upcoming product features publicly |
| Internal metrics | Revenue, user counts, internal KPIs |
| Code snippets | Actual production code from employer |

**Fix:**
- Generalize: "あるFinTech企業で" instead of naming the employer
- Abstract: describe patterns and principles, not specific implementations
- Get approval: when in doubt, run content by your manager
- Time-delay: wait 6-12 months before discussing past projects in detail

**Severity:** Critical — can result in termination or legal action.

---

### AP-7: Stagnation Mask

**Signal:** Brand that only showcases past achievements with no evidence of current growth.

| Detection | Examples |
|-----------|---------|
| Old dates only | All achievements are 2+ years old |
| No learning signals | No "currently learning" or "exploring" content |
| Static profiles | GitHub/LinkedIn unchanged for 6+ months |
| Defensive posture | Positioning only on past authority, avoiding new topics |

**Fix:**
- Add "Currently exploring" section to profiles
- Share learning journey content (TIL posts, Zenn Scraps)
- Update profiles quarterly
- Mix authority content (what you know) with growth content (what you're learning)

**Severity:** Medium — erodes trust over time as audience perceives stagnation.

---

## Platform-Specific Anti-Patterns

### Qiita

| Anti-Pattern | Signal | Impact | Fix |
|-------------|--------|--------|-----|
| **Opinion Post (ポエム)** | Subjective article without technical evidence | Low ratings + flame risk | Always back up with code or official documentation |
| **Stale Content** | Articles left unchanged for years | Reader confusion + trust erosion | Update regularly or add "this article is outdated" note |
| **Tag Abuse** | Adding many loosely related tags | Flagged as spam | 2-3 niche tags + 1-2 general tags |
| **Multi-Post** | Simple copy from other sites | Community backlash | Add platform-specific unique value |

### Zenn

| Anti-Pattern | Signal | Impact | Fix |
|-------------|--------|--------|-----|
| **Shallow Mass Production** | Short articles posted daily | Quality drop + follower churn | Focus on 1-2 deep articles per week |
| **Incomplete Book** | Paid Book abandoned mid-update | Refund risk + trust loss | Complete before monetizing, or state clearly |
| **Scrap Overuse** | Only Scraps, no full articles | Increased noise | Scraps are drafts; the goal is a full article |

### note

| Anti-Pattern | Signal | Impact | Fix |
|-------------|--------|--------|-----|
| **Overpriced Articles** | Thin content at high price | Low ratings + refunds | Provide unique value proportional to price |
| **Code-Heavy on note** | Excessive code blocks on note | Hard to read | Put code on Qiita/Zenn; use note for context and background |
| **Excessive Self-Promotion** | Every article is self-promotion | Follower churn | 80% value delivery, 20% promotion ratio |

### X (Twitter)

| Anti-Pattern | Signal | Impact | Fix |
|-------------|--------|--------|-----|
| **External Link in Body** | URL in main tweet text | 50-90% reach reduction | Place links in reply instead |
| **RT/Like Only** | No original opinions shared | Zero presence | Quote RT + add your opinion |
| **Controversy Participation** | Actively joining flame wars | Brand damage | Only participate in constructive discussions |
| **Follow-Back Farming** | Mass follow → unfollow | Account quality degradation | Grow through organic engagement |

### YouTube

| Anti-Pattern | Signal | Impact | Fix |
|-------------|--------|--------|-----|
| **Clickbait** | Thumbnail/title mismatches content | Viewer drop-off + trust loss | Use accurate yet compelling titles |
| **Long Intro** | 2+ minutes before the main topic | Early abandonment | Deliver value within 30 seconds |
| **Irregular Posting** | Inconsistent upload intervals | Algorithm disadvantage | Fixed schedule (e.g. weekly) |
| **Shorts-Only** | Only Shorts, no long-form content | Monetization disadvantage + lack of authority | Long-form:Shorts = 1:3-5 ratio |

### TikTok / Instagram Reels

| Anti-Pattern | Signal | Impact | Fix |
|-------------|--------|--------|-----|
| **Weak Opening** | First 3 seconds are boring | Instant swipe-away | Hook at the start (question, surprise, contrast) |
| **Over-Editing** | Too much time spent on high-end edits | Lower posting frequency + lack of authenticity | Prioritize authenticity (31% higher engagement) |
| **Horizontal Video Reuse** | YouTube video simply cropped to vertical | Hard to watch | Shoot as vertical video or re-edit properly |

---

## Anti-Pattern Audit Template

Output this with every Crest deliverable:

```markdown
## Anti-Pattern Check Results

| # | Check | Status | Note |
|---|-------|--------|------|
| AP-1 | Resume Dump | ✅/⚠️/❌ | [detail] |
| AP-2 | Vanity Metrics | ✅/⚠️/❌ | [detail] |
| AP-3 | Niche Absence | ✅/⚠️/❌ | [detail] |
| AP-4 | Channel Scatter | ✅/⚠️/❌ | [detail] |
| AP-5 | AI Ghost | ✅/⚠️/❌ | [detail] |
| AP-6 | Employer Leak | ✅/⚠️/❌ | [detail] |
| AP-7 | Stagnation Mask | ✅/⚠️/❌ | [detail] |

Platform-specific checks: [list applicable platform checks]
```

**Delivery rule:** All AP-1~AP-7 must be ✅ or ⚠️ (with documented mitigation). Any ❌ blocks delivery.
