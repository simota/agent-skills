# Voiceover Design Reference

Purpose: Design TTS narration for product demo videos. Cover voice selection (ElevenLabs / OpenAI TTS / Azure Neural / Google Cloud TTS), SSML pacing markup, breathing pauses, LUFS normalization for video, Playwright timeline sync via ffmpeg, and accessibility (Audio Description per WCAG 1.2.5).

## Scope Boundary

- **director `voiceover`**: TTS narration for demo videos (this document).
- **director `demo` / `record` / `scenario` / `onboard` (elsewhere)**: Scenario + recording orchestration.
- **director `captions` (elsewhere)**: On-screen captions (complements voiceover).
- **tone `voice` / `lufs` (elsewhere)**: Game / non-video voice generation + loudness normalization.
- **Cue (elsewhere)**: Video script narrative authoring (pre-voiceover).
- **Builder (elsewhere)**: Rendering pipeline code beyond ffmpeg stubs.

## When to Voice Over

- Product feature demos requiring narration
- Onboarding videos (step-by-step guidance)
- Tutorials / how-to content
- Conference talk recordings (pre-recorded variant)
- YouTube / LinkedIn product announcements
- Internal training materials

## Provider Comparison (2026 — current benchmark)

Ranked by Inworld TTS Arena 2026 Elo + qualitative fit.

| Provider | TTS Arena Elo | TTFA (first-audio) | Voices | Strength | Best for |
|----------|---------------|--------------------|--------|----------|----------|
| **Inworld Realtime TTS 1.5-Max** | **1,236 (#1)** | low | curated set + cloning | overall quality leader 2026 | high-stakes demos, investor / hero |
| **ElevenLabs v3** | 1,179 (#2) | ~150ms | 70+ languages, cloning, **Audio Tags** | emotional control, multilingual | brand voice, multilingual, expressive |
| **OpenAI Realtime TTS** | 1,106 (#4) | ~200ms | curated set | API simplicity, latency | quick iteration, dev workflows |
| **Cartesia Sonic-3** | 1,054 (#10) | **90ms** (Turbo: 40ms) | curated set | lowest latency in class | live narration, agentic loops |
| **OpenAI TTS (tts-1-hd)** | n/a | ~300ms | 6 voices | predecessor of Realtime | legacy / fixed-script narration |
| **Azure Neural TTS** | n/a | ~200ms | 400+ multilingual | enterprise, accessibility | regulated / public-sector |
| **Google Cloud TTS (Studio)** | n/a | ~300ms | 220+ voices | global locales | i18n-heavy decks |
| **Amazon Polly Neural** | n/a | ~200ms | 60+ voices | AWS pipelines | AWS-native stacks |
| **Coqui / local XTTS** | n/a | varies | open-source clone | offline / privacy | air-gapped, regulated |
| **Descript Overdub** | n/a | interactive | clone-based | podcast UX | iterative editing |

**Defaults (2026)**:
- **Quality-first**: Inworld Realtime TTS 1.5-Max (highest Elo).
- **Brand voice + emotion**: ElevenLabs v3 with Audio Tags.
- **Lowest latency / live agentic loops**: Cartesia Sonic-3 (40–90ms TTFA).
- **Founder-led / personal trust**: real human voice. AI TTS is now indistinguishable from human in blind tests for short narration — pick by brand consistency, not quality.

### ElevenLabs v3 Audio Tags

v3 introduces inline bracketed tags that control emotion / delivery without SSML. Tags are append-friendly to plain text:

```
"Schema drift broke production. [whispers] Again. [sighs] Most teams still diff three environments by hand. [shouts] Stop. [pauses] There's a better way."
```

Common tags: `[whispers]`, `[shouts]`, `[laughs]`, `[sighs]`, `[pauses]`, `[excited]`, `[sad]`, `[calm]`. Combine with SSML for finer pacing. Test sparingly — overusing tags reads as theatrical, not authentic.

## Voice Selection Matrix

| Demo type | Voice character | Pace |
|-----------|-----------------|------|
| Product announcement | Energetic, confident | 160-170 WPM |
| Onboarding | Friendly, measured | 140-150 WPM |
| Technical tutorial | Clear, authoritative | 150-160 WPM |
| Investor demo | Professional, trust | 150-160 WPM |
| Fun / casual | Conversational, warm | 160-180 WPM |
| Accessibility / AD | Neutral, clear | 140-150 WPM |

## SSML Pacing

Speech Synthesis Markup Language is the cross-provider spec for pacing. Core tags:

```xml
<speak>
  <p>
    <s>Welcome to Acme.<break time="400ms"/></s>
    <s>Let me show you how it works.</s>
  </p>
  <p>
    Click <emphasis level="moderate">here</emphasis> to create
    <prosody rate="90%">your first project.</prosody>
    <break time="800ms"/>
    <phoneme alphabet="ipa" ph="əˈkmi">Acme</phoneme>
  </p>
</speak>
```

Key tags:
- `<break time="500ms"/>` — pause
- `<prosody rate="90%" pitch="+2st">` — rate / pitch adjustment
- `<emphasis level="moderate">` — stress
- `<phoneme alphabet="ipa" ph="...">` — custom pronunciation
- `<say-as interpret-as="ordinal">3</say-as>` — "third"
- `<audio src="sfx.wav"/>` — insert audio

Not all providers support all tags. Test per provider.

## Pacing Guidelines

Target WPM = (total words) / (total duration in minutes).

Natural speech: 130-160 WPM.  
Demo narration: 150-160 WPM (brisk, engaging).  
Onboarding: 140-150 WPM (clearer, easier to follow).  
Tutorials: 150-160 WPM.  
Audio Description (AD) per WCAG 1.2.5: 140-170 WPM, gaps between visual events.

### Breathing & Pauses

```
Sentence end:    400-600ms pause
Comma / clause:  200-300ms
Section break:   800-1200ms
Post-CTA:        1000ms (let viewer see result)
Before emphasis: 200ms (anticipation)
```

Real humans breathe every 10-15 seconds. TTS sounds unnatural without these.

## Playwright Timeline Sync

Demo video timeline = Playwright action timestamps. Sync narration to action cues.

```typescript
// Playwright: emit timestamps to a sidecar JSON
await test.step('open settings', async () => {
  timeline.push({ time: performance.now(), event: 'open_settings' });
  await page.click('[data-test=settings]');
});

await test.step('toggle dark mode', async () => {
  timeline.push({ time: performance.now(), event: 'toggle_dark' });
  await page.click('[data-test=dark-toggle]');
});
```

Narration script (annotated with cues):
```yaml
narration:
  - cue: open_settings
    text: "Open settings from the top-right."
    duration_ms: 1500
  - cue: toggle_dark
    text: "Now enable dark mode."
    duration_ms: 1200
```

## FFmpeg Audio Sync

```bash
# Generate TTS audio
curl -X POST https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{"model":"tts-1-hd","voice":"nova","input":"Welcome..."}' \
  --output narration.mp3

# LUFS normalize to -16 LUFS (YouTube target)
ffmpeg -i narration.mp3 -af \
  "loudnorm=I=-16:TP=-1:LRA=7" \
  narration_normalized.wav

# Overlay on video (Playwright .webm)
ffmpeg -i demo.webm -i narration_normalized.wav \
  -c:v copy -c:a aac -b:a 192k \
  -map 0:v -map 1:a \
  demo_with_voiceover.mp4
```

## LUFS for Video

| Platform | Target LUFS | True Peak |
|----------|-------------|-----------|
| YouTube | **-14** | -1 dBTP |
| LinkedIn | **-14** (updated 2026) | -1 dBTP |
| Vimeo | -16 to -23 | -1 dBTP |
| Web / self-host | -16 | -1 dBTP |
| Broadcast TV (EBU R128) | -23 | -1 dBTP |
| Podcast | -16 | -1 dBTP |
| TikTok / Reels / Shorts | -14 to -16 | -1 dBTP |

**Default**: -14 LUFS for YouTube + LinkedIn (the two primary demo destinations in 2026). -16 LUFS for self-host / Vimeo / docs. Verify True Peak ≤ -1 dBTP to prevent clipping on transcode. Hand off to **tone `lufs`** for deeper loudness analysis; perceptual quality verification via `reference/quality-metrics.md`.

## De-essing

TTS voices often produce harsh sibilance ("s", "sh", "t"). Apply de-esser:

```bash
ffmpeg -i narration.wav -af \
  "deesser=i=0.05:m=0.5:f=0.5:s=o" \
  narration_deessed.wav
```

Or use Fabfilter Pro-DS / iZotope RX for professional output.

## Accessibility (WCAG 1.2.5 Audio Description)

If video has visual content that narration doesn't cover, AD track required.

- Primary track: main narration
- Extended AD: separate audio track describing visuals for sight-impaired users
- Pauses in main narration synced to visual-only moments
- AD voice distinct from narration

Use `<track kind="descriptions">` in HTML5 video or `<audiodescription>` in IMSC/TTML.

## Workflow

```
SCRIPT       →  receive scenario (from director `scenario`)
             →  extract timeline cues

VOICE        →  provider + voice selection per demo type
             →  clone / register if brand voice

SSML         →  insert pacing (sentence / section / CTA)
             →  phoneme for product names
             →  emphasis at key moments

SYNTHESIZE   →  TTS API call
             →  iterate on pronunciation / pace per take

CLEANUP      →  de-esser
             →  breathing pauses if TTS lacks
             →  remove click artifacts

LUFS         →  normalize to platform target (-16 default)
             →  True Peak ≤ -1 dBTP

SYNC         →  align to Playwright timeline cues
             →  adjust silence / trim to match action timing

MIX          →  ffmpeg overlay + encode
             →  BGM mix if applicable (-18 dB vs narration)

ACCESS       →  generate caption track (hand off to director `captions`)
             →  AD track if visual-only content exists
             →  WCAG 1.2.5 compliance

DELIVER      →  MP4 (H.264 + AAC 192kbps) per platform

HANDOFF      →  director `captions`: caption generation
             →  director `thumbnail`: thumbnail design
             →  tone `lufs`: final loudness QC
             →  Builder: build-pipeline integration
```

## Output Template

```markdown
## Voiceover Plan: [Demo]

### Scenario Summary
- Duration: [N seconds]
- Cue count: [N]
- Total words: [N]
- Target WPM: [150-160]

### Voice
- Provider: [ElevenLabs / OpenAI TTS / Azure Neural]
- Voice ID: [nova / Rachel / en-US-JennyNeural]
- Language: [en-US / ja-JP / ...]
- Gender / character: [friendly female / authoritative male]

### Script with SSML
```xml
<speak>
  <p>
    <s>Welcome to Acme.<break time="400ms"/></s>
    ...
  </p>
</speak>
```

### Cue-to-Text Map
| Cue | Playwright action | Text | Duration (ms) |
|-----|-------------------|------|---------------|
| open_settings | click settings | "Open settings from the top-right." | 1500 |
| toggle_dark | click toggle | "Now enable dark mode." | 1200 |

### Audio Pipeline
1. TTS generation: [provider API call]
2. De-esser: [ffmpeg or tool]
3. LUFS: [-16 LUFS, TP -1 dBTP]
4. Overlay: [ffmpeg command]

### Accessibility
- Captions: [auto / manual; hand off to director `captions`]
- Audio Description: [yes / no]
- WCAG 1.2.5 compliance: [pass / needs work]

### Handoffs
- director `captions`: SRT / WebVTT
- director `thumbnail`: thumbnail
- tone `lufs`: loudness QC
- Builder: build-pipeline integration
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Monotonic TTS with no pacing marks | Add SSML breaks, prosody, emphasis |
| Pronunciation of product name wrong | `<phoneme ph="...">` override |
| WPM too fast (180+) | Cap at 160-170 for narration |
| No breathing pauses | 400-600ms at sentence boundaries |
| Peak-normalize instead of LUFS | -16 LUFS with TP limit |
| Harsh sibilance | De-esser pass required |
| Audio out of sync with video action | Align to timeline cues; trim silence |
| Skipping captions | WCAG 1.2.2 requires; cheap insurance |
| Voice change mid-demo | Consistent voice per demo |
| Brand voice cloned without consent | Legal + ethical check; ElevenLabs / Descript have clone consent rules |
| Generating 100 variants; no iteration | 3-5 takes at key cues; refine best |
| No test on target device (mobile / TV) | Test playback on actual devices |
| Ignoring locale (EN only for global product) | Multilingual voices; test each language |
| BGM -6 dB under narration (drowns) | BGM -18 dB; duck further during narration |
| SSML that only one provider understands | Test across OpenAI + ElevenLabs; fallback plain text |
| No source control on script | Commit SSML + cue map alongside Playwright script |

## Deliverable Contract

When `voiceover` completes, emit:

- **Scenario summary** with duration + cues + WPM.
- **Voice choice** (provider / ID / language / character).
- **SSML script** with pacing markup.
- **Cue-to-text map** aligned to Playwright timeline.
- **Audio pipeline** (TTS → de-esser → LUFS → overlay).
- **Accessibility plan** (captions + AD + WCAG).
- **Handoffs**: director captions, director thumbnail, tone lufs, Builder.

## References

- ElevenLabs — elevenlabs.io (v3 models)
- OpenAI TTS — platform.openai.com/docs/guides/text-to-speech
- Azure Neural TTS — learn.microsoft.com/azure/ai-services/speech-service
- Google Cloud TTS — cloud.google.com/text-to-speech
- Amazon Polly — docs.aws.amazon.com/polly
- Descript — descript.com (Overdub)
- Coqui TTS — github.com/coqui-ai/TTS
- SSML 1.1 specification — w3.org/TR/speech-synthesis11/
- WCAG 2.1 Guideline 1.2 Time-based Media — w3.org/TR/WCAG21
- EBU R128 loudness — tech.ebu.ch/docs/r/r128.pdf
- ffmpeg loudnorm — ffmpeg.org/ffmpeg-filters.html#loudnorm
- *Sound for Film and Television* — Tomlinson Holman
- Fabfilter Pro-DS — fabfilter.com (professional de-esser)
- iZotope RX — izotope.com (audio restoration)
- Audio Description style guide — fcc.gov, DCMP Clearinghouse
- IMSC / TTML2 spec — w3.org/TR/ttml2/
- Descript + ElevenLabs voice-clone consent frameworks
- "Narration Pacing for Explainer Videos" — Vidyard / Wistia whitepapers
- "OpenAI TTS vs ElevenLabs benchmark" — community comparisons
