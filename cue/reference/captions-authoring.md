# Captions and Subtitle Authoring Reference

Purpose: Author subtitle, SDH (Subtitles for the Deaf and Hard-of-hearing), and closed-caption files with correct timing, readable line breaks, accessibility compliance, and the right delivery format per platform. A caption that can't be read in time is worse than no caption at all.

> **2026 baseline.** Automated transcription (Whisper-large family, AssemblyAI, Deepgram Nova-3, ElevenLabs) consistently lands the *first pass* at word-level timing accuracy under 0.5s for English. The 2026 caption-authoring workflow is **AI transcribes → human re-segments + re-times to phrase boundaries → CPS / line-length pass → ship**. AI alone reliably misses: speaker turn boundaries, music / SFX brackets for SDH, brand-name casing, and CPS budgeting under reading-speed limits. Treat the AI output as raw material, never as a deliverable.

## Scope Boundary

- **cue `captions`**: SRT / VTT / ASS authoring, timing, reading-speed limits, SDH additions, burn-in vs soft-sub decisions.
- **cue `localize` (elsewhere)**: translated captions / dubbing scripts for multi-locale delivery — run after base captions are locked.
- **cue `narration` (elsewhere)**: source narration script — captions derive from this.
- **Polyglot (elsewhere)**: i18n key extraction for UI copy — not applicable to time-coded captions, but owns any surrounding UI strings.
- **Warden (elsewhere)**: accessibility gate evaluation (WCAG 1.2.2 / 1.2.3 pass/fail).

If the hypothesis is "can a hearing-impaired viewer follow this video?" → `captions`. If it's "can a Spanish speaker follow this video?" → `localize`.

## Format Selection

| Format | Use when | Skip when |
|--------|----------|-----------|
| SRT (.srt) | YouTube, Vimeo, most players, simplest authoring | Need styling, positioning, or karaoke effects |
| WebVTT (.vtt) | HTML5 `<track>`, styling via cue settings, positioning | Legacy DVD / broadcast pipelines |
| ASS / SSA (.ass) | Karaoke, fan-sub styling, anime workflows, complex positioning | Accessibility-first delivery (many screen readers skip ASS) |
| SCC / CEA-608/708 | Broadcast TV, FCC compliance, OTT re-broadcast | Web-only delivery |
| TTML / DFXP | Netflix, broadcast archive, IMSC profile | Simple web delivery |

Default for web delivery: **WebVTT**. Default for YouTube/Vimeo upload: **SRT**.

## Workflow

```
INGEST    →  receive narration script + final video timecodes (or timed transcript)
          →  confirm target format (SRT / VTT / ASS) and accessibility goal (captions vs SDH)

SEGMENT   →  split narration into caption cues at natural phrase boundaries
          →  enforce max chars per line and max lines per cue
          →  verify reading speed (CPS / WPM) for every cue

TIME      →  anchor in-time to spoken onset ±80ms
          →  hold cue for min 1.0s, max 7.0s
          →  leave ≥2 frames gap between consecutive cues (prevents flicker)

ENRICH    →  (SDH only) add [music], [laughter], [door slams], speaker IDs
          →  (multi-speaker) identify speakers: "- Alex: …" / ">> NAME:" / color coding
          →  mark non-translated proper nouns, preserve branded casing

VERIFY    →  run CPS scanner, line-length scanner, overlap detector
          →  viewer test: can the slowest reader finish each cue?
          →  export in target format; for broadcast, validate against platform spec sheet
```

## Line and Reading Limits

| Metric | Limit | Source / rationale |
|--------|-------|--------------------|
| Max chars per line | 42 (Western), 37 (BBC), 16-ish (JA full-width) | Netflix / BBC / CPC standards |
| Max lines per cue | 2 | 3 lines occludes video, drops retention |
| Min cue duration | 1.0s (≥ 20 frames at 24fps) | Below this, cue flashes unreadably |
| Max cue duration | 7.0s | Longer cues break attention loop |
| Reading speed — adults | 17 CPS (≈200 WPM) | Netflix default |
| Reading speed — kids | 13 CPS | Children's content ceiling |
| Reading speed — SDH | 21 CPS hard ceiling | Only when content is time-critical |
| Min gap between cues | 2 frames (≈83ms at 24fps) | Prevents visual flicker |

CPS = characters per second, excluding spaces in most counters. Over-budget cues get split or the line is edited for brevity.

## SDH vs Standard Captions

Standard captions transcribe spoken dialogue only. SDH adds everything else a hearing viewer perceives.

| Element | Standard | SDH |
|---------|----------|-----|
| Dialogue | Yes | Yes |
| Speaker ID (multi-speaker) | Sometimes | Always |
| Sound effects | No | Yes — `[door slams]`, `[phone rings]` |
| Music cues | No | Yes — `[upbeat music]`, `♪ song lyrics ♪` |
| Laughter / reactions | No | Yes — `[laughter]`, `[sighs]` |
| Off-screen narration | Yes | Yes, marked as `[narrator]:` |
| Silence / pause | No | Only when narratively significant |

Deliver SDH when the platform requires WCAG 1.2.2 (pre-recorded captions) and 1.2.3 (audio description or transcript) compliance. **ADA compliance deadline**: as of April 24, 2026, US public entities serving populations over 50,000 must meet WCAG 2.1 Level AA (DOJ final rule, April 2024) — this covers video captions, audio description, and keyboard-accessible player controls [Source: testparty.ai/blog/video-captioning-requirements].

## SRT Cue Example

```
12
00:01:23,480 --> 00:01:26,720
- Alex: We ship every Friday.
- Priya: Even during incident response?

13
00:01:26,800 --> 00:01:28,600
[phone rings]
```

Two frames gap: cue 12 ends at `26,720` and cue 13 starts at `26,800` (80ms). Cue 12 is a two-line multi-speaker cue with dash prefix.

## Burn-in vs Soft-Sub Tradeoffs

| | Burn-in (hardsub) | Soft-sub (sidecar or embedded) |
|-|-------------------|-------------------------------|
| Viewer can toggle off | No | Yes |
| Survives re-share on social | Yes | Often stripped |
| Supports multi-language | No (one per export) | Yes (switchable tracks) |
| Search-indexable | No | Yes |
| Styling control | Full | Limited to format capability |
| Accessibility certification | Counts | Counts when default-on or discoverable |

Default for YouTube/Vimeo: **soft-sub (upload SRT)** so viewers toggle and search works. Default for TikTok / Reels / Shorts reshare: **burn-in** so captions survive download and repost.

## Auto-Caption Polish Workflow

Platform auto-captions (YouTube ASR, Whisper, etc.) are a starting point, not a deliverable. Always polish:

1. **Proper nouns pass**: fix product names, people, places that ASR misheard.
2. **Punctuation pass**: ASR often omits commas; restore them where pacing needs them.
3. **Homophone pass**: "their / there / they're", "lead / led", product-specific terms.
4. **Segment pass**: ASR splits on silence, not on sense — merge and re-split on clause boundaries.
5. **CPS pass**: ASR-generated cues frequently exceed 21 CPS; split or edit.
6. **Number / unit pass**: "two thousand twenty four" → "2024"; "gigabytes" → "GB" when visual is tight.
7. **Brand voice pass**: enforce capitalization (GitHub not Github), hyphenation (sign-in not sign in), terminology.

Budget: ~2-3× video runtime for a full polish pass on a 3-minute video.

## Anti-Patterns

- ❌ Three-line cues — steals video real estate, drops retention.
- ❌ Verbatim filler transcription ("uh", "um", "you know") in non-documentary content.
- ❌ Captions that lead the audio by more than 200ms — feels like spoilers and breaks sync perception.
- ❌ ALL-CAPS cues for emphasis (except short shouts) — cuts reading speed ~15%.
- ❌ Auto-captions uploaded without polish — WCAG compliance is about quality, not existence.
- ❌ Mixing burn-in and soft-sub on the same export — viewers get double captions on toggle.
- ❌ Translating captions before base SRT is locked — retiming translated cues costs more than the original pass.

## Handoff

On completion, hand off:

- **To `localize`**: locked base-language SRT/VTT with speaker IDs, pronunciation notes for product names, glossary of non-translatable terms, and runtime caption-budget summary.
- **To Director / Reel**: burn-in position spec (safe area, font, size, stroke) if delivery is hardsub.
- **To Warden**: caption file + video file pairing for WCAG 1.2.2 / 1.2.3 accessibility gate evaluation.
- **To user**: caption file in target format, CPS/line-length validation report, and a one-line note on any passages that required editorial compression to hit reading speed.
