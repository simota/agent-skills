# Storytelling Archetypes

Purpose: Pick a duration-locked story blueprint when planning a demo. Each archetype has a beat-by-beat structure, target channel, and hook template. Use this with `scenario-guidelines.md` (hook + pain + show-don't-tell) and `playwright-config.md` (aspect ratios).

## When to Read

- The `scenario` recipe is selecting a duration / structure.
- The user names a channel (TikTok, LinkedIn, Product Hunt, YouTube long-form) and you need the matching shape.
- A demo is creeping past 90 seconds and you must decide between trimming, chaptering, or splitting.
- The user requests "a series" (3×45s) — choose the series archetype.

---

## Archetype Selection Matrix

| Channel / Goal | Recommended Archetype | Length | Aspect |
|---------------|----------------------|--------|--------|
| TikTok / Reels / Shorts | `30s-social-hook` | 21–34s | 9:16 |
| Product Hunt gallery | `60s-producthunt` | 45–60s | 1:1 or 16:9 |
| LinkedIn feed (B2B) | `60s-linkedin` | 15–60s | 4:5 |
| Hero film / sales site | `90s-hero` | 60–90s | 16:9 |
| YouTube long / docs walkthrough | `180s-walkthrough` | 90–180s, chaptered | 16:9 |
| Complex product / new category | `3x45s-series` | 3 × 45s | 16:9 or 9:16 |
| Founder / investor narrative | `60s-founder-led` | 60–90s | 16:9 |
| Agentic visual receipt | `agent-receipt` | 30–120s (no narrative) | 16:9 |

---

## 30s Social Hook (`30s-social-hook`)

**Channel**: TikTok, Reels, YouTube Shorts. **Aspect**: 9:16. **Target completion**: ≥ 70%.

### Beat Sheet

| Time | Beat | Note |
|------|------|------|
| 0:00–0:03 | **Hook** (layered: visual + text + audio) | Show the broken state OR the impossible outcome |
| 0:03–0:10 | **Pain** | One concrete pain (number, screenshot, or reaction) |
| 0:10–0:24 | **Solution** | One Aha — the moment value reveals |
| 0:24–0:28 | **Result** | Visible outcome, no narration needed |
| 0:28–0:30 | **CTA** | Logo + handle / URL, 1.5s minimum |

### Hook Template

> "[Concrete Number] [Unexpected Outcome]." e.g., "5,000 rows → 5 milliseconds."

Layer with text reveal (jump-cut) + screen state change + optional whoosh SFX.

### Anti-Patterns

- Greeting / intro of any kind.
- Voiceover before visual.
- Multi-feature dump — pick **one** Aha.
- 16:9 master cropped to 9:16 (sides lose UI).

---

## 60s Product Hunt (`60s-producthunt`)

**Channel**: Product Hunt gallery + LP embed. **Aspect**: 1:1 (gallery) or 16:9 (LP). **Target**: muted-autoplay-comprehensible.

### Beat Sheet

| Time | Beat | Note |
|------|------|------|
| 0:00–0:05 | **Hook** | Layered hook + 1-line value prop |
| 0:05–0:15 | **Pain** | The legacy / manual workflow being replaced |
| 0:15–0:45 | **Solution** | "Dashboard → workflow → after-state" (2026 PH pattern) |
| 0:45–0:55 | **Result** | Outcome on screen + key metric overlay |
| 0:55–1:00 | **CTA** | Product name + visit / try-it URL |

### Anti-Patterns

- Talking-head opener (PH 2026: demerit; product-first wins).
- Audio-only narration with no captions (PH plays muted in feed).
- Generic startup BGM under entire video — pick a hook moment for the BGM swell only.

---

## 60s LinkedIn (`60s-linkedin`)

**Channel**: LinkedIn feed. **Aspect**: **4:5 (1080×1350) — 2026 default**. **Target**: 15–60s sweet spot.

### Beat Sheet (45s reference)

| Time | Beat | Note |
|------|------|------|
| 0:00–0:03 | **Hook** | Layered hook addressing a workplace pain |
| 0:03–0:12 | **Pain** | "Most teams still do X manually. Here's the cost." |
| 0:12–0:36 | **Solution** | Show the new way with one Aha |
| 0:36–0:42 | **Result** | Quantified outcome (time saved, errors avoided) |
| 0:42–0:45 | **CTA** | Single next step ("Try it free" + URL) |

### Anti-Patterns

- 16:9 reused on 4:5 — top/bottom UI lost.
- "Excited to share..." opener.
- Founder selfie with no product on screen.

---

## 90s Hero (`90s-hero`)

**Channel**: Sales site hero, LinkedIn ads, YouTube pre-roll. **Aspect**: 16:9 (1920×1080). **Target**: feature-rich without losing engagement.

### Beat Sheet

| Time | Beat | Note |
|------|------|------|
| 0:00–0:05 | **Hook** | Visual + text + (optional) founder VO |
| 0:05–0:20 | **Pain** | Show the broken status quo, possibly via B-roll |
| 0:20–1:05 | **Solution** | 3 mini-Aha moments tied to one through-line |
| 1:05–1:20 | **Result** | Outcomes layered (number + emotion + customer logo) |
| 1:20–1:30 | **CTA** | URL + secondary action (docs / pricing) |

### Notes

- Founder-led VO outperforms anonymous narration on LinkedIn / sales.
- B-roll overlays at 70–85% opacity hold visual interest during talk-heavy sections.

---

## 180s Walkthrough (`180s-walkthrough`)

**Channel**: YouTube long, docs page, internal training. **Aspect**: 16:9. **Required**: chapter markers (YouTube chapters or `page.screencast.showChapter()`).

### Beat Sheet (3 minutes, 5 chapters)

| Time | Chapter | Note |
|------|---------|------|
| 0:00–0:15 | **Ch1: Pain** | Hook + pain framing |
| 0:15–0:45 | **Ch2: Setup** | Account / data setup |
| 0:45–1:45 | **Ch3: Aha** | Main feature reveal, 1 Aha |
| 1:45–2:30 | **Ch4: Detail** | Power-user features, integrations |
| 2:30–3:00 | **Ch5: Result + CTA** | Outcome + next step |

### Anti-Patterns

- No chapter markers — YouTube engagement penalty.
- Single Aha stretched across all 3 minutes — viewers leave at 90s.
- Past 2 minutes without chapter / scene change → -40% engagement.

---

## 3×45s Series (`3x45s-series`)

**Channel**: Complex products, new categories, technical deep-dives.  
**Aspect**: 16:9 or 9:16 per platform. **Target**: each ep stands alone AND chains.

### Episode Structure

| Ep | Hook | Focus | CTA |
|----|------|-------|-----|
| **Ep 1: Pain** | "Most teams fail at X" | Establish the category gap | "Watch how we fix it →" |
| **Ep 2: Aha** | "Here's the missing piece" | The core differentiator | "See it for your data →" |
| **Ep 3: Outcome** | "After 30 days with Acme..." | Customer outcome + numbers | "Start your trial" |

### Production Notes

- Shoot all 3 in a single Playwright session if state allows; export per-ep.
- Maintain visual continuity (same brand palette, same on-screen actor / cursor style).
- Per-ep transcript + VideoObject JSON-LD; cross-link with `isPartOf`.

---

## 60s Founder-Led (`60s-founder-led`)

**Channel**: LinkedIn, X, podcast clips. **Aspect**: 16:9 or 4:5. **Target**: trust building.

### Beat Sheet

| Time | Beat | Note |
|------|------|------|
| 0:00–0:05 | **Hook** | Founder face + bold claim |
| 0:05–0:25 | **Why** | Why we built it (90% face, 10% screen) |
| 0:25–0:50 | **Show** | Screen takes over; founder voice continues |
| 0:50–1:00 | **CTA** | Founder asks for the click |

### Notes

- Founder VO outperforms TTS for trust-driven contexts.
- This is the **one** archetype where talking-head is encouraged.
- Use Director to capture the screen segments; mix in an externally recorded founder track at post-production.

---

## Agent Receipt (`agent-receipt`)

**Channel**: PR comments, audit logs, Slack. **Aspect**: 16:9. **Length**: as long as the work takes (30–120s typical). **No narrative arc** — this is evidence.

### Beat Sheet

| Time | Beat | Note |
|------|------|------|
| 0:00–0:03 | **Task chapter** | `showChapter({ title: 'Task: <description>' })` |
| 0:03–end | **Execution** | Real agentic flow; `showActions()` annotates clicks |
| (end) | **Result chapter** | `showChapter({ title: 'Done: <outcome>' })` |

### Notes

- No music, no overlays beyond auto-action annotations.
- Pair with `browser.bind()` so the agent and Director share one browser.
- `onFrame` optional — only enable for live Vision-Model audit.
- Output naming: `agent_receipt_[task]_[date].webm`.

---

## Picking an Archetype: Quick Heuristics

1. Channel is TikTok / Reels / Shorts → `30s-social-hook`.
2. LinkedIn feed → `60s-linkedin` (4:5).
3. Product Hunt → `60s-producthunt` (1:1 or 16:9).
4. YouTube long or docs → `180s-walkthrough` with chapters.
5. Complex product launch → `3x45s-series`.
6. Founder personal brand → `60s-founder-led`.
7. Agentic CI / audit work → `agent-receipt`.
8. Anything past **120s without chapters** → re-pick an archetype that fits, or split into a series.

---

## Cross-References

- Aspect ratios and viewport pairings → `playwright-config.md → Aspect Ratio Presets`.
- Hook design (layered hook, 3-sec rule) → `scenario-guidelines.md → 3-Second Layered Hook`.
- Quality verdict per archetype → `checklist.md → Quality Scorecard (/97)`.
- Transcript + VideoObject for AI citation → `geo-packaging.md`.
- TTS narration per archetype → `voiceover-design.md → Voice Selection Matrix`.
