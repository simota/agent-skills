# Vertical Short-Form Video Script Reference

Purpose: Author 9:16 short-form scripts (TikTok / Instagram Reels / YouTube Shorts) optimized for sound-off autoplay, thumb-scroll retention, and loopable endings. A Shorts script lives or dies in the first 3 seconds — everything else is scaffolding for that hook.

> **2026 stack note.** End-to-end AI shorts pipelines (FlowShorts and similar) chain script → AI image / video gen → ElevenLabs VO → burned-in TikTok-style captions → auto-post to YouTube Shorts / TikTok / Reels. They are appropriate for **high-volume social ATL distribution** where retention metrics matter more than brand fidelity, and they are *inappropriate* for high-trust product launches or campaign hero work where every frame is reviewed. Treat this Shorts recipe as the human-authored / brand-grade path; treat the AI pipeline as the volume-channel companion. The 3-second hook rule, sound-off legibility, and pattern-interrupt cadence below apply to both — AI tooling does not loosen the retention math.

## Scope Boundary

- **cue `shorts`**: hook-first 15-60s vertical script, captions-on-screen spec, loop design, platform length targeting.
- **cue `script` (default, elsewhere)**: long-form or horizontal product demos, full structure templates.
- **Reel (elsewhere)**: terminal-session recording for CLI demos — use if the Short is a code/CLI reveal.
- **Director (elsewhere)**: Playwright-driven browser captures for product screen content in the Short.
- **Tone (elsewhere)**: BGM selection, sound-effect punctuation, trending-audio cue specs.

If the hypothesis is "will a thumb-scroller stop?" → `shorts`. If it's "does the full feature story land?" → default `script`.

## Workflow

```
BRIEF     →  pick platform (TikTok / Reels / Shorts), pick target length
          →  identify the single payoff the viewer gets for stopping
          →  confirm sound-off viability (85%+ watch muted on feed)

HOOK      →  draft 3-second hook using a template below
          →  layer visual + textual + auditory (3x retention vs single-layer)
          →  put the payoff promise on-screen as burned-in caption

BEAT      →  plan pattern interrupts every 2-3 seconds (cut, zoom, text flip)
          →  script the 1 message — no secondary points
          →  caption every spoken line (burn-in, not soft-sub)

LOOP      →  design final frame to visually or narratively loop to frame 1
          →  place CTA either at 70% mark (pre-loop) or in caption overlay

REVIEW    →  verify total ≤ platform sweet spot
          →  verify hook is legible with sound off
          →  verify no dead frames > 1.5s
```

## Platform Length Sweet Spots

| Platform | Max | Sweet spot | Notes |
|----------|-----|------------|-------|
| TikTok | 60 min (upload) / 10 min (in-app) | 15-30s | 21-34s range hits ~62% completion; viral threshold 70%+ [Source: metricool.com, 2025] |
| Instagram Reels | 20 min (in-app) / <15 min (upload) | 15-60s | Algorithm favours <90s for reach; 7-15s best for discovery; expanded to 20 min late 2025 [Source: inro.social, 2025] |
| YouTube Shorts | 3 min (180s) | 15-60s | Max expanded from 60s on Oct 15, 2024; music restriction: >60s requires royalty-free only; >60s with Content ID claim blocked globally [Source: support.google.com/youtube/answer/15424877] |
| LinkedIn video | 10 min | 30-90s | Professional tone, captions required — 80%+ watch muted |

Default: write to 21-30s unless the user specifies otherwise. Going longer is a trade — more story, fewer loops.

## 3-Second Hook Templates

| Hook type | Opening line pattern | Use when |
|-----------|----------------------|----------|
| Contrarian | "Everyone tells you to X. Don't." | Audience has a dominant assumption to break |
| Stat shock | "87% of [audience] are doing [thing] wrong." | You own a proprietary data point |
| Before/After reveal | Split screen cold-open, no setup | Visual transformation is the payoff |
| Question | "What if [audience] could [outcome] in [constraint]?" | Aspirational product promise |
| Stakes | "If you [do thing], stop. Here's why." | Warning / loss aversion angle |
| Cliffhanger | "Watch what happens when I [action]…" | Tool / feature has a surprise result |
| Pattern match | "POV: you just [relatable situation]" | Audience-identity driven |

Rule: the hook must be legible as text-on-screen by frame 30 (≈1s at 30fps). If a viewer reads the hook and scrolls, that's a passed filter — not a loss.

## Pattern Interruption Cadence

Short-form retention curves drop off between visual stimuli. Plan an interrupt every 2-3 seconds:

- Hard cut to a new angle or subject.
- Zoom punch-in / punch-out (120-140% scale, 6-8 frames).
- Text overlay appears or swaps (new key phrase).
- B-roll insert for 0.5-1s.
- Caption style change (color flash, shake) on emphasis words.

A 30s Short should have **8-12 interrupt beats**. Fewer than 6 reads as sluggish; more than 15 reads as frantic.

## Captions-On-Screen Requirements

85%+ of feed viewers watch muted. Captions are mandatory, not optional.

- **Burn-in for Shorts delivery** unless the platform caption editor is mandatory — burn-in guarantees fidelity and styling.
- Max 7 words per caption card — one breath unit per card.
- Font min 42-48pt on 1080×1920 canvas; stroke or background plate for legibility over b-roll.
- Place inside safe area: top 220px and bottom 340px are obscured by platform UI on TikTok / Reels.
- Sync caption transitions to spoken word onset within ±2 frames.

## Loopable Ending Design

Instagram Reels and TikTok both count re-watches toward the engagement signal. Design endings to invite a second watch.

Two loop patterns:

1. **Visual loop**: the final frame matches the first frame in composition, so the autoplay cut is invisible. Example: hand reaching for a product enters frame 1, hand places the product in final frame → loops into the "reach" shot.
2. **Narrative loop**: the final line is a question or tease that is answered in the hook. Example: hook says "Here's the fix", outro says "Still confused? Watch from the top." — literal invite to re-watch.

Avoid: outro cards, subscribe stingers, long logo fades. Every frame after the payoff is retention loss.

## CTA Placement

A Short has one CTA. Place it once.

| Placement | When | Caveat |
|-----------|------|--------|
| Caption bar (persistent) | Growth / follow CTAs | Doesn't interrupt the beat |
| 70% timestamp, spoken | Conversion / click-through | Delivered before loop point so it lands pre-rewatch |
| Pinned comment handoff | Link / URL CTAs | TikTok / Reels hide bio links; pinned comment is canonical |
| On-screen text only | Product name / handle | Leave auditory space for the payoff |

Never stack CTAs. "Follow, like, comment, share, and click the link" is zero CTAs.

## Anti-Patterns

- ❌ Slow build-up before the hook — 50-60% drop-off happens in the first 3 seconds.
- ❌ Sound-dependent hook (a joke that needs audio) without a text-on-screen equivalent.
- ❌ Native platform soft-captions as the only caption layer — get stripped on reshare.
- ❌ Horizontal 16:9 footage center-cropped into 9:16 — leaves dead bars and signals low-effort repost.
- ❌ Multiple messages in one Short — one Short, one idea, one payoff.
- ❌ Outro cards and logo stingers after the payoff — every post-payoff frame drops completion rate.
- ❌ CTA stack ("like, comment, share, follow, subscribe") — pick one.

## Handoff

On completion, hand off:

- **To Director / Reel**: list of segments that need screen or terminal capture, with aspect (9:16) and duration per clip.
- **To Tone**: trending-audio reference or original BGM spec, SFX punctuation cues per beat, final-frame audio treatment for loop.
- **To user**: burn-in caption sheet (timestamp, copy, style), hook rationale (which template and why), and platform-specific export spec (1080×1920, H.264, ≤30Mbps).
