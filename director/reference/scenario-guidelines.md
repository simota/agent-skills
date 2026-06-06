# Scenario Design Guidelines

Principles, templates, and best practices for demo video scenario design.

Purpose: Read this when Director must design a story arc, tune pacing, select overlay timing, adapt the demo to an audience, or review scenario quality before recording.

Contents:
- `3-Second Layered Hook`: hook design rules for 70% drop-off prevention
- `Storytelling Structure`: hook → pain → solution → result framing
- `Show Don't Tell Techniques`: B-roll, before/after split, caption-aware overlay
- `Scenario Templates`: full and quick planning templates
- `Operation Granularity Design`: step sizing rules for viewer comprehension
- `Wait Strategy`: explicit waits vs pacing pauses
- `Overlay Display Patterns`: overlay timing and style rules
- `Audience-Specific Adjustments`: new user, existing user, investor, developer variants
- `Time Allocation Guidelines`: duration guidance by scope (including 2-min engagement cliff)
- `Platform Length Targets (2026)`: per-platform optimal lengths
- `Director vs AI Video Generators`: when to record vs when to generate
- `Scenario Anti-Patterns`: must-avoid pacing and structure mistakes
- `Test Data Realism`: realism and privacy rules
- `Scenario Review Checklist`: pre-recording quality review

---

## 3-Second Layered Hook

TikTok / Reels / Shorts drop **~70% of viewers** in the first 3 seconds. LinkedIn / YouTube are kinder but the principle holds: the first 3 seconds decide whether the demo gets watched at all. A **layered hook** (visual + textual + optional audio simultaneously) holds attention **~3× longer** than a single-channel opening.

### Hook Composition

| Channel | Bad | Good |
|---------|-----|------|
| Visual | Generic landing page, brand splash | Concrete problem state (overflowing inbox, broken dashboard, stuck deployment) |
| Text overlay | "Welcome to Acme" | "Excel breaks at 50k rows. Watch this." (3–5 words, bold, big) |
| Audio (optional) | Silence + corporate stinger | Quick whoosh / typewriter / heartbeat aligned with text reveal |
| Motion | Static screenshot | Zoom-in on broken element, jump-cut, or speed-ramp |

### Hook Templates

| Template | Pattern | Example |
|----------|---------|---------|
| **Problem-Shock** | "Show the broken state first" | Visual: red error toast. Text: "Your CI just failed for the 4th time today." |
| **Outcome-First** | "Show the future first, then reveal how" | Visual: green ✅ in 8s. Text: "Ship in 8 seconds." |
| **Question-Hook** | "Pose the question viewers ask" | Text: "Why does deploy take 20 minutes?" |
| **Numeric-Hook** | "Concrete number that contradicts expectations" | Text: "5,000 rows → 5 milliseconds." |
| **Reaction-Hook** | "Show a real person's expression of relief / surprise" | Used for stakeholder / investor demos with founder-led VO |

### Hook Anti-Patterns

| Anti-Pattern | Why bad | Fix |
|--------------|---------|-----|
| Open on logo / splash | Wastes the first 1–2 sec | Cut the splash; logo can appear at the end |
| Generic landing-page opener | No pain context, low retention | Skip to the broken state or the outcome |
| Voiceover before visual | Audio plays before viewer's eye locks on screen | Visual + text first; voice can come at 1.5s |
| "Hi everyone, today we'll be..." | Talking-head opener; instant drop on social | Cut all greetings; start in-action |
| One-channel hook (text only OR visual only) | Lower 3-sec retention | Layer two channels minimum |

---

## Show Don't Tell Techniques

Demos communicate value when viewers **see** the outcome — not when narration **describes** it. Director patterns for 2026:

### B-roll Overlay (70–85% opacity, 3–7s clips)

Cut to supporting footage (real product UI, data, mobile capture) at 70–85% opacity over a stable base scene. Holds visual interest while extending narration.

```
0:00–0:08  Base scene: dashboard (full opacity)
0:08–0:15  B-roll overlay: mobile capture of same data (75% opacity)
0:15–0:22  Base scene returns; B-roll dissolves out
```

### Before / After Split-Screen

Legacy flow on left, new flow on right, synced timeline. Use for redesigns, migrations, AI-vs-manual comparisons.

- Sync points: shared start, shared end ("both reach the same outcome — one in 30s, one in 4 minutes").
- Letterbox the right side as the "after" loads to emphasize speed delta.

### Caption-Aware B-roll Positioning

Open captions occupy bottom 15% of the frame. B-roll and overlays must avoid this band. CapCut / Descript auto-detect captions; if hand-authoring, reserve the bottom strip.

### Speed Ramping

Boring middle sections (data loading, API roundtrips) get 2–4× speed-up. Critical reveals stay real-time. ffmpeg: `setpts=0.5*PTS` for 2× speed.

### Cursor as Storyteller

The cursor is the camera. Move it deliberately:
- Hover before clicking (200–400ms) — signals intent.
- Slow approach to the Aha button.
- Cursor halo / pulse on key interactive elements (`implementation-patterns.md` → Cursor helpers).

---

---

## Storytelling Structure

Design demos as **stories**, not operation sequences. Follow the **Hook → Pain → Solution → Result → CTA** arc.

```
Hook (0–3s)    Pain (3–10s)    Solution (10–40s)    Result (40–55s)    CTA (55–60s)
-----------    --------------  -------------------- -----------------  -------------
Layered hook   Show the broken Demonstrate the      Show the outcome   Single next
visual+text    workflow / cost / new way              & emotion          step
hook
```

### Five-Act Application (60s default)

| Phase | Duration | Purpose | Example (Migration tool) |
|-------|----------|---------|--------------------------|
| **Hook** | 0–3s | Lock attention | Visual: SQL error toast. Text: "Schema drift broke prod." |
| **Pain** | 3–10s | Establish stakes | Show manual diff process across 3 environments |
| **Solution** | 10–40s | Show the new way | One-click migration plan + preview + apply |
| **Result** | 40–55s | Emotional payoff | Green checkmarks across all envs, founder's reaction |
| **CTA** | 55–60s | Single next step | "Try it free → acme.dev/migrate" |

Skip phases as the archetype dictates (`storytelling-archetypes.md`): a 30s social hook collapses Pain into Hook; a 180s walkthrough expands Solution into multiple chapters.

---

## Scenario Templates

### Standard Template

```markdown
## Demo Request: [Feature Name]

### Target Audience
- [ ] New users (onboarding)
- [ ] Existing users (new feature introduction)
- [ ] Investors / Stakeholders
- [ ] Sales / Marketing
- [ ] Internal documentation

### Demo Objective
What should viewers understand after watching this demo?
> [Describe in 1-2 sentences]

### Prerequisites
- Login state: [ ] Not logged in [ ] Logged in [ ] Admin
- Initial data: [Description of required data]
- Environment: [ ] Development [ ] Staging [ ] Demo-dedicated

### Story Flow

#### 1. Opening (5-10 seconds)
**Scene**: [First screen to display]
**Message**: [Context to convey to viewers]
**Overlay**: [ ] Yes [ ] No
> Overlay text: "[Text]"

#### 2. Main Action (20-40 seconds)
**Step list**:
1. [Action 1] -> [Expected result]
2. [Action 2] -> [Expected result]
3. [Action 3] -> [Expected result]

**Emphasis points**:
- [X seconds]: [What to emphasize]

#### 3. Closing (5-10 seconds)
**Scene**: [Final screen to display]
**Message**: [Impression to leave with viewers]
**Overlay**: [ ] Yes [ ] No
> Overlay text: "[Text]"

### Test Data Requirements
| Data Type | Content | Notes |
|-----------|---------|-------|
| User | demo@example.com | Display name: Demo User |

### Recording Settings
- Resolution: [ ] 1280x720 (recommended) [ ] 1920x1080 [ ] 375x667 (mobile)
- slowMo: [ ] 500ms (standard) [ ] 700ms (form-heavy) [ ] 1000ms (slow)
- Max duration: [XX] seconds
- Output formats: [ ] WebM [ ] MP4 [ ] GIF
```

### Quick Template

```markdown
## Quick Demo: [Feature Name]

**Audience**: [Who is this for?]
**Objective**: [What to convey?]
**Duration**: [XX seconds]

**Flow**:
1. [Screen] - [Action] - [Result]
2. [Screen] - [Action] - [Result]
3. [Screen] - [Action] - [Result]

**Test Data**: [Required data]
**Settings**: [Resolution] / slowMo [X]ms
```

---

## Operation Granularity Design

| Operation Type | Recommended Granularity | Reason |
|---------------|------------------------|--------|
| Button click | 1 action = 1 step | Clear separation |
| Form input | Split by field | Input content is visible |
| Page transition | Wait for completion | Recognize screen change |
| Animation | Wait until complete | Avoid incomplete states |

```typescript
// Bad: Too coarse (viewer can't follow)
await page.fill('#email', 'demo@example.com');
await page.fill('#password', 'password');
await page.click('#submit');

// Good: Appropriate granularity with locator-based waits
await page.locator('#email').pressSequentially('demo@example.com', { delay: 80 });
await expect(page.locator('#email')).toHaveValue('demo@example.com');

await page.locator('#password').pressSequentially('password', { delay: 80 });
await page.waitForTimeout(300); // Deliberate pacing pause

await page.click('#submit');
await expect(page.locator('#dashboard')).toBeVisible();
```

---

## Wait Strategy

### Prefer Locator-Based Waits for State Changes

Use `waitForTimeout()` **only** for deliberate pacing pauses. For all state changes, use explicit waits:

| Scene | Strategy | Example |
|-------|----------|---------|
| Element appears | `expect(locator).toBeVisible()` | After click, modal appears |
| Page navigation | `page.waitForURL()` | After login redirect |
| Network idle | `page.waitForLoadState('networkidle')` | After page load |
| Animation complete | `expect(locator).toHaveCSS()` | After transition |

### Pacing Pauses (waitForTimeout)

Use **only** for viewer comprehension — these are intentional delays, not state waits:

| Scene | Recommended Wait | Purpose |
|-------|-----------------|---------|
| After screen display | 500-1000ms | Viewer recognizes screen |
| After input | 300-500ms | Verify input content |
| Before button click | 200-300ms | Prepare for next action |
| After page transition | 1000-1500ms | Recognize new screen |
| Important result display | 1500-2000ms | Emphasize result |
| During overlay display | Based on text length | Until reading complete |

### Overlay Display Time Formula

```
Overlay display time = (character count x 100ms) + 500ms
```

Example: "Login successful" (16 chars) = 16 x 100 + 500 = 2100ms

---

## Overlay Display Patterns

### Step Explanation Overlay

```typescript
await showOverlay(page, 'Step 1: Enter email address', 2000);
```

### Highlight Overlay

```typescript
await showHighlight(page, '#submit-button', 'Click here!');
```

### Success/Error Overlay

```typescript
await showSuccessOverlay(page, 'Registration complete!');
await showErrorOverlay(page, 'An error occurred');
```

### Overlay Style Guide

| Property | Recommended Value | Reason |
|----------|------------------|--------|
| Background | rgba(0,0,0,0.8) | Readability |
| Text color | #FFFFFF | Contrast |
| Border radius | 8px | Soft impression |
| Padding | 16px 32px | Comfortable appearance |
| Font size | 18-24px | Readability |
| Position | Bottom center | Doesn't interfere with operation |

---

## Audience-Specific Adjustments

### For New Users
- Don't skip basic operations
- Avoid or explain technical terms
- Emphasize success experience

### For Existing Users
- Quick basic operations
- Focus on new features
- Emphasize differences from previous version

### For Investors/Stakeholders
- Emphasize business value
- Differentiation from competitors
- Imply scalability

### For Developers
- Include technical details
- Show API integration
- Customization points

---

## Time Allocation Guidelines

### Duration by Scope

| Duration | Use Case | Notes |
|----------|----------|-------|
| Under 30 seconds | Social hook, ads, looped hero | TikTok-friendly 21–34s |
| 30-60 seconds | Standard feature demo, Product Hunt gallery | Best completion rate (~71%) |
| 60-90 seconds | LinkedIn / YouTube optimal | Balance of substance + engagement |
| 90-120 seconds | Complex flows, presentation | Approaching the cliff — chapterize |
| **Over 120 seconds — HARD CAP** | **HARD CAP — split or chapterize** | Engagement drops ~40% past 2 minutes |

### Engagement Benchmarks (2026)

Use these benchmarks to calibrate the duration budget, not as hard limits.

| Metric | Value | Implication |
|--------|-------|-------------|
| First-3-sec drop-off (TikTok/Reels) | ~70% | Layered hook is non-negotiable |
| Videos under 90s repeat-view rate | ~50% | Treat 90s as the engagement ceiling for top-of-funnel demos |
| B2B average video length (2026) | ~76s | Compressed from prior years; audiences expect shorter demos |
| Sub-60s video completion rate | ~71% (mobile) | Sub-60s is optimal for social and top-of-funnel |
| 60-90s completion rate | ~60% | Best engagement/substance trade-off for feature demos |
| 120s+ engagement loss | ~40% drop | **Hard cap; switch to chaptered or series format** |
| 9:16 mobile completion rate | ~76% | Vertical wins on mobile vs 54% for 16:9 |
| 9:16 ad viewability | ~90% vs 14% (16:9) | Vertical massively outperforms for paid placement |
| Interactive demo engagement | ~2× vs walkthrough | Hand off to Supademo / Arcade when interactivity wins |

### Self-Guided Embed Step Count

| Channel | Steps | Notes |
|---------|-------|-------|
| Email / Social | 6-8 | Short attention span, single Aha moment |
| Website / Docs | 8-15 | Tolerates more context and exploration |
| Interactive (Supademo / Arcade) | 10-25 | User self-paces — different medium, different rules |

### Platform-Adapted Pacing (2026)

| Platform | Pacing | Optimal Length | Captions | Aspect Ratio |
|----------|--------|----------------|----------|--------------|
| YouTube (long) | Moderate | 60–180s | Required for mute autoplay | 16:9 (1920×1080) |
| YouTube Shorts | Fast, hook in 3s | 30–60s | Required (open) | 9:16 (1080×1920) |
| LinkedIn feed | Moderate | 15–60s B2B | Required | **4:5 (1080×1350) — 2026 default** |
| LinkedIn (16:9) | Moderate | 60–90s | Required | 16:9 fallback |
| X / Twitter | Fast | ≤60s free / longer with Premium+ | Required | 16:9 or 1:1 |
| Instagram Reels | Fast, hook in 2s | <90s | Required (open) | 9:16 |
| TikTok | Fast, hook in 3s | **21–34s** (Explore-friendly) | Required (open) | 9:16 |
| Product Hunt | Moderate | 45–60s gallery, 60–120s demo | Required + YouTube hosting | 1:1 or 16:9 |
| Website hero | Moderate, looped | 15–30s loop | Optional (muted autoplay) | 16:9 |
| Docs inline | Slow, instructional | 30–90s | Optional | 16:9 |

### Talking-Head Bias (B2B / Dev Tools)

For dev-tool and B2B Product Hunt launches, **talking-head openers are a demerit**. The 2026 industry-Top pattern (Cursor, Linear, Notion, Vercel) is "dashboard → workflow → after-state" without a presenter face. Use talking-head only for stakeholder/investor demos with founder-led VO where trust is the asset.

---

## Director vs AI Video Generators

Director records **real product UI**. AI video generators (Sora 2, Veo 3.1, Runway Gen-4.5) generate footage from prompts. They are complementary, not competitive — pick the right tool per scene.

| Scene | Use | Why |
|-------|-----|-----|
| Real product workflow | **Director (Playwright)** | Reproducible, accurate, on-brand UI |
| Hero opener / abstract metaphor (e.g., "data flowing through pipes") | AI generator | Director can't film abstract concepts |
| B-roll for non-UI moments (office, hands typing) | AI generator | No need to shoot live action |
| Future UI / not-yet-built feature | AI generator | Director needs real DOM |
| Investor / vision film | AI generator + Director cuts | Mix aspirational + concrete |
| Onboarding walkthrough | **Director (Playwright)** | Must match the actual UX |
| Comparison vs competitor (their UI) | **Director** + recorded competitor session (with permission) | Visual proof must be authentic |

When the request mixes both, Director records the real-UI segments; route the AI segments to an AI-video brief (out of Director scope).

---

## Scenario Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Feature dump | 3+ features in 1 demo | 1 demo = 1 feature |
| Too fast | slowMo: 100ms | slowMo: 500-700ms |
| No context | Start immediately with form input | "Let's try XX" to set context |
| Incomplete ending | End on button click | Display result 1-2 seconds |
| Fake data | email: test@test.com, name: aaa | email: demo@example.com, name: Demo User |
| Timeout-only waits | All waits are `waitForTimeout` | Use `toBeVisible()` for state changes |

---

## Test Data Realism

- Fictional but realistic names and emails
- Meaningful numbers ($39.80 instead of $100)
- Use appropriate language for content
- Never use production data or real user information
- Keep data consistent across scenes

---

## Scenario Review Checklist

### Story
- [ ] Has clear starting point
- [ ] What viewer wants to achieve is clear
- [ ] Has satisfying conclusion

### Pacing
- [ ] Uses locator-based waits for state changes
- [ ] Uses `waitForTimeout` only for deliberate pauses
- [ ] No redundant waits

### Data
- [ ] Test data is realistic
- [ ] No confidential information included
- [ ] Data is consistent

### Technical
- [ ] Reproducible scenario
- [ ] No flaky elements
- [ ] All selectors are stable
