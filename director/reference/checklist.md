# Demo Recording Checklist

Quality gates for each phase of demo video production.

Purpose: Read this when Director must validate demo readiness, playback quality, security hygiene, accessibility, perceptual quality, AI-citation packaging, or final delivery quality.

Contents:
- `Pre-Recording Checklist`: scenario, hook, environment, aspect, and accessibility setup
- `Post-Recording Checklist`: playback, content, security, captions, transcript, and output validation
- `Pre-Delivery Checklist`: packaging, AI-citation, multi-aspect, and reproducibility checks
- `Quick Check (3 minutes)`: rapid go/no-go review
- `Quality Scorecard (/97)`: scoring and release thresholds (2026 expanded)

---

## Pre-Recording Checklist

### Scenario
- [ ] Audience identified
- [ ] Purpose defined (1-2 sentences)
- [ ] Archetype selected (30s social / 60s producthunt / 90s linkedin / 180s walkthrough / 3×45s series)
- [ ] 3-second layered hook designed (visual + text + optional audio)
- [ ] One demo, one feature
- [ ] Story arc defined (Hook → Pain → Solution → Result → CTA)
- [ ] Emphasis points identified
- [ ] Duration plan ≤ 120s OR explicitly chaptered

### Environment
- [ ] Using `playwright.config.demo.ts`
- [ ] Target aspect chosen (16:9 / 9:16 / 4:5 / 1:1) and viewport matches
- [ ] `page.screencast` planned with explicit `size`
- [ ] `recordVideo` `retain-on-failure` safety net configured
- [ ] slowMo appropriate for audience
- [ ] Resolution matches target device / aspect
- [ ] Test data seeded
- [ ] Auth state prepared (storageState)
- [ ] `browser.bind()` configured if MCP/CLI clients will attach

### Accessibility
- [ ] Key screens validated with ARIA snapshots (if applicable)
- [ ] Overlay text meets contrast requirements (≥4.5:1 AA, prefer 7:1 AAA)
- [ ] Caption plan defined: open (burned-in) for muted-autoplay + closed (`.vtt`) for accessibility
- [ ] WCAG 1.2.2 (captions) plan committed for external distribution
- [ ] WCAG 1.2.5 (Audio Description) status decided — needed when visual content isn't fully narrated

---

## Post-Recording Checklist

### Playback
- [ ] Video plays to completion
- [ ] No choppy frames or flickering
- [ ] Text is readable at target resolution and at mobile size
- [ ] Hook locks attention in first 3 seconds (verify by watching with sound off)

### Content
- [ ] All operations visible at demo speed
- [ ] Pacing feels natural (not rushed, not dragging)
- [ ] Overlays readable with sufficient display time
- [ ] Final result displayed long enough (1.5–2s)
- [ ] No 16:9 master reused as-is on 9:16 / 4:5 channels — re-shot or re-framed per aspect

### Security
- [ ] No passwords, tokens, or production data visible
- [ ] No console errors or network errors visible
- [ ] No internal staging URLs, IPs, or feature flags exposed
- [ ] Demo data used (realistic but fictional)

### Captions & Transcript
- [ ] Open-caption (burned-in) variant generated for muted-autoplay channels
- [ ] Closed-caption `.vtt` track generated and synced
- [ ] Transcript (`.vtt` + plaintext) generated
- [ ] Non-dialog cues annotated (`[click]`, `[music swells]`)
- [ ] Caption reading speed ≤ 17 CPS, ≤ 42 chars/line, ≤ 2 lines
- [ ] Product names and homophones manually QC'd (auto-caption WER baseline only)

### Perceptual Quality
- [ ] VMAF ≥ 90 at 1080p (`ffmpeg-quality-metrics --vmaf`)
- [ ] PSNR ≥ 40 dB
- [ ] SSIM ≥ 0.95
- [ ] LUFS normalized to -14 (YouTube/LinkedIn) or -16 (Web), TP ≤ -1 dBTP

### Output
- [ ] Naming convention followed: `[feature]_[action]_[aspect]_[date].webm`
- [ ] MP4 (H.264) conversion generated for universal playback
- [ ] AV1 archival master generated (if hero/archival use case)
- [ ] File size reasonable (~5–8 MB / 30s at 1080p VP9)
- [ ] Saved in `demos/output/` directory with aspect subfolder

---

## Pre-Delivery Checklist

- [ ] Demo meets original objectives
- [ ] UI matches current product state
- [ ] Scenario document saved for reproducibility
- [ ] Metadata recorded (date, version, environment, aspect)
- [ ] Output formats match distribution channels (WebM/MP4/AV1/GIF)
- [ ] **Transcript `.vtt` + plaintext attached for external distribution**
- [ ] **VideoObject JSON-LD schema generated with `hasPart` chapters, `transcript`, `thumbnailUrl`**
- [ ] Thumbnail set generated per platform (YouTube 1280×720, LinkedIn 1200×627, X 1600×900, Product Hunt 1200×1200)
- [ ] A/B thumbnail variants prepared (face-first vs product-first; default product-first for B2B / dev-tools)
- [ ] WCAG verdict recorded: 1.2.2 (captions), 1.2.4 (live, if applicable), 1.2.5 (AD)
- [ ] If multi-aspect: 16:9 + 9:16 + 4:5 variants exported and verified

---

## Quick Check (3 minutes)

```
[] Hook lands in 0–3s (sound off)
[] Plays to the end
[] Followable pace
[] No confidential information
[] Clear result
[] Captions sync (spot-check 3 points)
[] VMAF / PSNR / SSIM verdict logged
[] Transcript + VideoObject JSON-LD attached
[] Correct filename, aspect, and format
```

---

## Quality Scorecard (/97)

Rate each item. Most items 1–5; some items have higher max points reflecting 2026 priorities (hook, aspect, multilingual, perceptual quality).

| # | Category | Item | Score | Max |
|---|----------|------|-------|-----|
| S1 | **Story** | Clear beginning / ending | | 5 |
| S2 | **Story** | Appropriate pacing | | 5 |
| S3 | **Story** | Effective emphasis points | | 5 |
| S4 | **Story** | One Aha moment (no feature-dump) | | 3 |
| S5 | **Story** | Pain established within 10s | | 3 |
| H1 | **Hook (3s)** | Layered hook (visual + text + optional audio) present in 0–3s | | 5 |
| H2 | **Hook (3s)** | No splash / greeting / talking-head opener | | 3 |
| H3 | **Hook (3s)** | Single, concrete hook message (3–5 words) | | 2 |
| L1 | **Length** | Duration ≤ 120s or properly chaptered | | 5 |
| L2 | **Length** | Length matches archetype / channel | | 3 |
| A1 | **Aspect** | Output aspect matches distribution channel | | 5 |
| A2 | **Aspect** | If multi-channel: per-aspect variants generated (not crop-reused) | | 3 |
| V1 | **Visual** | Resolution / source quality (1080p+) | | 5 |
| V2 | **Visual** | Overlay readability (contrast, size, mobile-safe) | | 3 |
| V3 | **Visual** | Brand consistency (colors, fonts, motion) | | 3 |
| T1 | **Technical** | Stability / reproducibility | | 5 |
| T2 | **Technical** | Selector robustness | | 3 |
| T3 | **Technical** | Wait strategy (locator-based, not timeout-based) | | 3 |
| C1 | **Captions** | Closed caption `.vtt` present and synced | | 5 |
| C2 | **Captions** | Open (burned-in) variant for muted-autoplay channels | | 3 |
| C3 | **Captions** | SDH cues (`[click]`, `[music]`) included | | 2 |
| C4 | **Multilingual** | EN + JA captions minimum; auto-translate + human QC | | 3 |
| W1 | **WCAG 2.2** | 1.2.2 Captions Level A | | 3 |
| W2 | **WCAG 2.2** | 1.2.5 Audio Description Level AA (when visual-only content exists) | | 3 |
| Q1 | **Perceptual** | VMAF ≥ 90 at 1080p | | 3 |
| Q2 | **Perceptual** | PSNR ≥ 40 dB / SSIM ≥ 0.95 | | 2 |
| Q3 | **Perceptual** | LUFS within target (-14 / -16, TP ≤ -1 dBTP) | | 2 |
| P1 | **Platform** | Captions / aspect / file size match channel spec | | 3 |
| P2 | **Platform** | Thumbnail set generated per platform | | 2 |
| P3 | **Platform** | A/B thumbnail variants prepared | | 2 |
| G1 | **GEO / AI-citation** | Transcript (`.vtt` + plaintext) packaged | | 3 |
| G2 | **GEO / AI-citation** | VideoObject JSON-LD with chapters + transcript | | 3 |
| G3 | **GEO / AI-citation** | YouTube + secondary mention plan (boost AI citation up to 325%) | | 2 |
| D1 | **Data** | Realism | | 2 |
| D2 | **Data** | Confidential info excluded | | 3 |
| **Total** | | | | **/97** |

### Score Assessment

- **80–97**: Ship clean — production-ready
- **70–79**: Ship with minor fixes — log follow-ups
- **50–69**: Ship with major fixes — re-shoot weakest scenes
- **< 50**: Reshoot — review from scenario and hook
