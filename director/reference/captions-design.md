# Captions Design Reference

Purpose: Author accessibility-grade captions for demo videos. Cover SRT / WebVTT formats, WCAG 1.2.2 / 1.2.4 compliance, 42-char line limit, reading-speed targets, forced vs closed vs open caption variants, auto-generation (Whisper / Deepgram / Azure) + manual QC.

## Scope Boundary

- **director `captions`**: Caption authoring for demo videos (this document).
- **director `voiceover` (elsewhere)**: TTS narration (captions derive from narration text).
- **director `demo` / `record` (elsewhere)**: Recording orchestration.
- **polyglot (elsewhere)**: i18n for multi-locale captions.
- **prose (elsewhere)**: UX copy guidelines (different domain).

## Why Captions

- **Accessibility**: WCAG 1.2.2 Level A requires captions for prerecorded video with audio; 1.2.4 Level AA for live
- **Sound-off viewing**: LinkedIn / X autoplay without audio; 85% of video viewed muted on social
- **Comprehension**: Non-native speakers, accents, technical jargon
- **SEO**: Search engines index captions → better discovery
- **Legal**: ADA (US), EAA (EU) mandate accessible video for public sector + e-commerce

## Formats

| Format | Extension | Use case |
|--------|-----------|----------|
| **SRT (SubRip)** | .srt | Broadest support (YouTube, Vimeo, most players) |
| **WebVTT** | .vtt | HTML5 `<track>`, styling + positioning, web-first |
| **TTML / IMSC** | .ttml / .xml | Broadcast, Netflix, accessibility-rich |
| **ASS / SSA** | .ass | Advanced styling (karaoke, anime fansubs) |
| **SBV** | .sbv | YouTube internal |
| **SCC** | .scc | US broadcast closed captions |

Default for web: **WebVTT**. Fallback for maximum compatibility: **SRT**.

### SRT Example

```
1
00:00:00,000 --> 00:00:03,500
Welcome to Acme. Let me show you
how it works.

2
00:00:03,500 --> 00:00:07,000
Click settings in the top-right
to open the configuration panel.
```

### WebVTT Example

```
WEBVTT

00:00:00.000 --> 00:00:03.500
Welcome to Acme. Let me show you
how it works.

00:00:03.500 --> 00:00:07.000 align:center line:90%
Click settings in the top-right
to open the configuration panel.

NOTE
Section: Onboarding

00:00:07.000 --> 00:00:10.000 position:50% size:60%
<c.highlight>[Music fades]</c>
```

WebVTT adds positioning, styling cues (CSS classes via `<c.name>`), regions, chapters, and notes.

## Reading Speed Target

| Audience | Max WPM | Max CPS (chars/sec) |
|----------|---------|---------------------|
| Adult general | 180 | 17 |
| Complex technical | 160 | 15 |
| Children (8-12) | 120 | 11 |
| Learners / ESL | 150 | 14 |

CPS = chars per second. If cue text is 100 chars and duration is 5 s → 20 CPS (too fast).  
Rule: **≤ 17 CPS** for general adult audience (BBC, Netflix recommendation).

## Line Length

| Rule | Value |
|------|-------|
| Max chars per line | **42** (BBC), **37-42** (Netflix) |
| Max lines per cue | **2** |
| Min cue duration | **1 second** |
| Max cue duration | **7 seconds** |
| Min gap between cues | **2 frames** (~83ms @ 24fps) |

Line breaks should be linguistically natural (after comma, before preposition, between clauses — not mid-phrase).

## Three Caption Variants

| Variant | Visibility | Use |
|---------|-----------|-----|
| **Closed (CC)** | Toggleable (viewer enables) | Default; platform UI (YouTube, Vimeo) controls |
| **Open** | Burned-in (always visible) | Social feeds (LinkedIn / X autoplay); no toggle |
| **Forced** | Shown only when needed (foreign language, off-screen sound, inaudible) | Bilingual content; accessibility for specific sections |

Closed is preferred when platform supports toggle. Open for social media autoplay.

## Forced Captions Examples

```
[phone rings]
[crowd cheering]
[whispers in Japanese] Kochira desu.
♪ upbeat electronic music ♪
```

Sound-effect descriptions and non-dialog audio cues are required per WCAG 1.2.2.

## Auto-Generation (2026)

| Tool | WER (approx) | Speed | Best for |
|------|--------------|-------|----------|
| **GPT-4o-Transcribe** | **~4.1%** (2026 leader) | Fast | Primary pipeline; multilingual, low WER |
| **OpenAI Whisper large-v3** | ~5.3% | Medium | Offline, privacy, batch; baseline fallback |
| **Deepgram Nova-3** | high | Fast (< realtime) | Production pipelines, streaming |
| **Azure Speech-to-Text** | high (enterprise) | Fast | Azure stacks |
| **Google Cloud STT v2** | high | Fast | Multilingual global |
| **Rev.ai** | very high (human-assisted) | Slow | High-stakes / regulated content |
| **Descript** | high + UI polish | Interactive | Podcast / interview workflow |
| **Loom AI** | high | Instant | Loom-hosted demos; auto-chapters + 50+ langs |
| **YouTube auto-captions** | mid | Instant | Quick-and-dirty only; always QC |

> Whisper v4 is **not** publicly released as of 2026-05. Use GPT-4o-Transcribe as the 2026 default; Whisper large-v3 remains the open-source fallback. Always QC auto-generated captions — homophones (to/too/two), product-name typos, punctuation errors.

### Recommended Pipeline (2026)

```
audio.wav
   ↓
GPT-4o-Transcribe   →   raw .vtt
   ↓
human QC pass       →   fix homophones, product names, punctuation
   ↓
   ├──→ closed-caption .vtt (for accessibility / search)
   ├──→ open / burned-in (ffmpeg `subtitles` filter for muted-autoplay)
   └──→ DeepL / GPT-4o translation  →  per-locale .vtt  →  human review
```

For multilingual: GPT-4o (source-aware translation) outperforms DeepL on demo-context idioms, but DeepL is faster for bulk locale fan-out. Always human-review **product names** in target languages.

## FFmpeg Auto-Caption Pipeline

```bash
# Extract audio from video
ffmpeg -i demo.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav

# Transcribe with Whisper
whisper audio.wav --model large-v3 --language en --output_format vtt

# Result: audio.vtt (needs QC before use)

# Embed as soft-subtitle track
ffmpeg -i demo.mp4 -i audio.vtt \
  -c:v copy -c:a copy -c:s webvtt \
  demo_captioned.mp4
```

## Burning In Captions (Open)

For social video:

```bash
# Using subtitles filter
ffmpeg -i demo.mp4 -vf \
  "subtitles=captions.vtt:force_style='FontName=Helvetica,FontSize=22,PrimaryColour=&Hffffff,BackColour=&H80000000,BorderStyle=3,Outline=1,Shadow=0'" \
  -c:a copy demo_captioned.mp4
```

Font: sans-serif (Helvetica, Arial, Inter), 22-28pt for 1080p.  
Background: semi-transparent black for contrast.  
Outline: 1px for readability.

## Styling (WebVTT CSS)

```css
::cue {
  background: rgba(0, 0, 0, 0.75);
  color: white;
  font-family: Inter, sans-serif;
  font-size: 1.4em;
}

::cue(.highlight) {
  color: #ffd700;
  font-weight: bold;
}
```

## WCAG Compliance

| Criterion | Requirement |
|-----------|-------------|
| **1.2.2 Captions (Prerecorded)** | Level A | Captions provided for prerecorded audio in video |
| **1.2.4 Captions (Live)** | Level AA | Live captions for synchronous video |
| **1.2.5 Audio Description** | Level AA | AD for prerecorded video (if visual-only content) |
| **1.2.6 Sign Language (Prerecorded)** | Level AAA | Optional; sign-language track |
| **1.2.8 Media Alternative** | Level AAA | Full text transcript alternative |

For product demo videos: 1.2.2 minimum, 1.2.4 if streaming live, 1.2.5 if visual-only content.

## Translation / i18n

Workflow:
1. Produce English master caption
2. Hand off to polyglot / translator
3. Generate locale-specific .vtt / .srt
4. Ship per language (YouTube supports multi-track)

Challenges:
- Reading speed differs per language (JP: slower due to kanji; DE: longer words)
- Line length may need relaxation (JP: 20 full-width chars; AR: RTL direction)
- Cultural references / idioms → localize, don't translate literally

## QC Checklist

```
[ ] All dialog captioned
[ ] Non-dialog audio cues in brackets [music] [sirens]
[ ] Reading speed ≤ 17 CPS per cue
[ ] Max 2 lines per cue; ≤ 42 chars per line
[ ] Min 1s, max 7s duration
[ ] Natural line breaks (not mid-phrase)
[ ] Min 2-frame gap between cues
[ ] No overlapping cues
[ ] Speaker labels for multiple speakers ("John:", "[Narrator]")
[ ] Punctuation consistent
[ ] Product names spelled correctly
[ ] No profanity / placeholder leaks
[ ] Synced to video (spot-check 3-5 points)
[ ] Plays on target platforms (YouTube / Vimeo / LinkedIn / Twitter)
[ ] WCAG 1.2.2 confirmed
```

## Workflow

```
INPUT        →  narration text from director `voiceover`
             →  or auto-transcribe from audio

GENERATE     →  Whisper / Deepgram / Rev.ai per budget
             →  or hand-author from narration script

CHUNK        →  split into cues per 1-7s, ≤ 2 lines, ≤ 42 chars/line
             →  preserve natural phrasing
             →  reading speed ≤ 17 CPS

SOUND CUES   →  add [sfx] / [music] descriptions
             →  speaker labels if multi-voice

TIMING       →  align to audio track
             →  cue boundaries at silence / pause

STYLE        →  WebVTT positioning if needed
             →  CSS styling for color / font

VARIANT      →  CC (soft subtitle track) for toggle platforms
             →  Burned-in (open) for social autoplay
             →  Forced if multi-lang or visual-only

QC           →  checklist pass
             →  spot-check video sync at 3-5 points
             →  platform playback test

DELIVER      →  .srt + .vtt dual export for compat
             →  TTML for broadcast delivery
             →  embedded into MP4 (soft subs) + burned-in open variant

I18N         →  hand off master to polyglot for translation
             →  per-locale variant files

HANDOFF      →  director `voiceover`: narration sync
             →  director `thumbnail`: thumbnail
             →  polyglot: translation
             →  Builder: build pipeline
```

## Output Template

```markdown
## Captions Plan: [Demo]

### Inputs
- Narration script: [path]
- Audio track: [path]
- Language: [en-US / ja-JP / ...]

### Generation
- Tool: [Whisper large-v3 / Deepgram Nova-3 / Rev.ai / Manual]
- QC iterations: [count]

### Format
- Primary: WebVTT (`.vtt`)
- Fallback: SRT (`.srt`)
- TTML if broadcast: [yes / no]

### Specifications
- Line length: [≤42 chars]
- Max lines per cue: 2
- Min/max duration: 1s / 7s
- Target CPS: ≤17
- Font / size: [Inter 22pt / 24pt]
- Variant: [CC / Burned-in / Forced — per distribution]

### Cue Inventory
[total cue count + total duration]
[sample 3-5 cues with timecodes]

### Non-Dialog Cues
[list of [sfx] / [music] descriptions]

### Styling
- WebVTT CSS: [custom / default]
- Position: [center / bottom-center / dynamic]

### Variant Map
| Platform | Variant | File |
|----------|---------|------|
| YouTube | CC (soft) | captions.vtt |
| LinkedIn | Burned-in | demo_burned.mp4 |
| X | Burned-in | demo_burned.mp4 |
| Internal portal | CC + TTML | captions.ttml |

### QC Result
- [ ] 17 CPS max
- [ ] 42 chars / 2 lines max
- [ ] Natural break points
- [ ] Sync spot-check passes
- [ ] Platform playback tested
- [ ] WCAG 1.2.2 pass

### Localization Plan
- Languages: [list]
- Per-lang reading speed adjustment: [notes]
- Translator handoff: [polyglot / vendor]

### Handoffs
- director `voiceover`: narration sync
- director `thumbnail`: thumbnail
- polyglot: translations
- Builder: pipeline
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Auto-captions shipped without QC | Always human-review; homophones + brand names |
| 80-char lines | Cap at 42 (BBC) / 37-42 (Netflix) |
| 20 CPS reading speed | Cap at 17 CPS; split longer cues |
| Mid-phrase line breaks | Break at natural points (comma, clause) |
| Missing sound-effect descriptions | `[sirens]` `[music builds]` required per WCAG |
| Same cue for 10 seconds | Split; min 1s, max 7s |
| No speaker label with multiple voices | `John:`, `[Narrator]`, `[Child]` |
| Burned-in with low contrast | Semi-transparent black background + white text + outline |
| Tiny font on mobile playback | 22-28pt at 1080p minimum |
| Captions cover UI | Position above / below interactive elements |
| Missing TTML for broadcast | Include TTML for regulated delivery |
| Profanity / placeholder text leaked | Final QC pass for `[TODO]`, `[FIXME]` |
| Translation as literal word-for-word | Localize; idioms + reading speed differ |
| Only SRT delivered; WebVTT needed | Dual export standard |
| No YouTube sync; timing drifted | Spot-check 3-5 anchor points after edit |
| Caption track lang mismatch | `<track srclang="en">` matches actual language |

## Deliverable Contract

When `captions` completes, emit:

- **Format choice** (WebVTT primary + SRT fallback + optional TTML).
- **Specifications** (line length, cue duration, CPS target, font).
- **Cue inventory** with count + total duration.
- **Non-dialog cues** listed.
- **Variant map** per distribution platform.
- **QC checklist** result.
- **Localization plan** if multi-language.
- **Handoffs**: director voiceover, director thumbnail, polyglot, Builder.

## References

- WCAG 2.1 Guideline 1.2 Time-based Media — w3.org/TR/WCAG21
- WebVTT spec — w3.org/TR/webvtt1/
- SRT de-facto spec — matroska.org/technical/subtitles.html
- TTML2 / IMSC — w3.org/TR/ttml2/
- BBC Subtitle Guidelines — bbc.github.io/subtitle-guidelines
- Netflix Timed Text Style Guide — partnerhelp.netflixstudios.com/hc/en-us/articles/217350977
- FCC closed captioning rules — fcc.gov
- ADA (US) accessibility — ada.gov
- EAA (EU) — European Accessibility Act (2025)
- OpenAI Whisper — github.com/openai/whisper
- Deepgram Nova-3 — deepgram.com
- Rev.ai — rev.ai
- Azure Speech-to-Text — azure.microsoft.com/products/ai-services/ai-speech
- Google Cloud STT v2 — cloud.google.com/speech-to-text
- Descript — descript.com
- ffmpeg subtitles / assin — ffmpeg.org/ffmpeg-filters.html
- "Subtitle Readability Research" — BBC R&D papers
- "Captioning Key" — DCMP (Described and Captioned Media Program)
- Closed Caption Style Guide — Media Access Group / WGBH
- 3PlayMedia — 3playmedia.com (professional captioning service)
- Kapwing / Amara — online caption editors
- Subtitle Edit — nikse.dk/subtitleedit (open-source)
- Aegisub — aegisub.org (advanced ASS editor)
