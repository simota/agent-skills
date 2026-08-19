# Perceptual Quality Metrics

Purpose: Numerically verify demo video quality with VMAF, PSNR, SSIM, and LUFS before shipping. Used by the `quality` recipe and the `/97` scorecard's perceptual section.

## When to Read

- Running the `quality` recipe explicitly.
- Pre-delivery: verifying VMAF / PSNR / SSIM before declaring a demo shippable.
- CI: integrating perceptual quality into the demo pipeline.
- Reshoot decisions: "is this video objectively below ship threshold?"

---

## Why Perceptual Metrics Matter

Subjective playback checks miss artifacts that **viewers will see** on different devices:
- Banding on dark gradients (mobile OLED amplifies).
- Macroblocking during high-motion B-roll.
- Audio loudness inconsistency across platforms (LinkedIn -16, YouTube -14).

VMAF (Netflix's metric) and SSIM correlate with human perception far better than visual eyeballing. PSNR adds a raw signal floor. Numeric thresholds turn "looks fine" into "ships."

---

## Targets (1080p baseline)

| Metric | Floor | Target | Ship Gate | Notes |
|--------|-------|--------|-----------|-------|
| **VMAF** | ≥ 75 | ≥ 90 | ≥ 90 | Below 75 = reshoot or re-encode |
| **PSNR** | ≥ 35 dB | ≥ 40 dB | ≥ 40 dB | Below 35 = high noise/macroblocking |
| **SSIM** | ≥ 0.92 | ≥ 0.95 | ≥ 0.95 | Structural similarity |
| **LUFS (integrated)** | -23 to -12 | -14 (YT/LI) or -16 (Web) | within ±1 of target | True Peak ≤ -1 dBTP |
| **TP (True Peak)** | ≤ 0 dBTP | ≤ -1 dBTP | ≤ -1 dBTP | Prevents clipping on transcode |

At 4K, expect ~3–5 VMAF points lower for the same encode settings — adjust ship gate to ≥ 87.

---

## Computing VMAF / PSNR / SSIM

Use [ffmpeg-quality-metrics](https://github.com/slhck/ffmpeg-quality-metrics) — a Python CLI wrapping ffmpeg's libvmaf.

### Install

```bash
pip install ffmpeg-quality-metrics
# requires ffmpeg ≥ 5.0 with --enable-libvmaf
```

### Single-File Score vs Lossless Reference

```bash
# Compare encoded vs lossless master
ffmpeg-quality-metrics demo_encoded.mp4 demo_master.webm \
  --metrics vmaf psnr ssim \
  --output json > quality.json
```

If there's no lossless reference (one-pass capture), encode at a known-good profile and compare against itself at lower bitrate to expose the floor:

```bash
# Generate a high-quality reference from the master
ffmpeg -i demo_master.webm -c:v libx264 -preset veryslow -crf 14 ref.mp4
ffmpeg-quality-metrics demo_encoded.mp4 ref.mp4 --metrics vmaf psnr ssim
```

### Parsing JSON

```python
import json
with open('quality.json') as f:
    d = json.load(f)
print(d['global']['vmaf']['vmaf']['average'])  # ≥ 90
print(d['global']['psnr']['psnr_avg']['average'])  # ≥ 40
print(d['global']['ssim']['ssim_avg']['average'])  # ≥ 0.95
```

---

## LUFS Verification

LUFS is **integrated loudness** averaged over the file. Use ffmpeg's `loudnorm` filter in analysis mode:

```bash
ffmpeg -i demo.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2> lufs.txt
```

Look for:
```
"input_i" : "-15.7",   ← integrated LUFS BEFORE normalization
"input_tp": "-0.4",    ← True Peak BEFORE
```

### Apply Normalization

```bash
# Two-pass loudnorm for accurate target (YouTube/LinkedIn = -14)
ffmpeg -i demo.mp4 \
  -af "loudnorm=I=-14:TP=-1:LRA=7:measured_I=-15.7:measured_TP=-0.4:measured_LRA=8.3:measured_thresh=-26.4:offset=-0.05:linear=true" \
  -c:v copy -c:a aac -b:a 192k demo_loud.mp4
```

For demos with narration: aim for **-14 LUFS** on YouTube / LinkedIn, **-16 LUFS** on Web / Vimeo, **-23 LUFS** on broadcast (rare for product demos).

---

## Reshoot Decision Logic

```
IF VMAF < 75 OR PSNR < 35 OR SSIM < 0.92:
    → RESHOOT (likely capture-side problem: low bitrate, dropped frames, viewport scaling)
ELIF VMAF < 90:
    → RE-ENCODE (try VP9 → AV1 or lower CRF; don't reshoot)
ELIF LUFS outside target ±1:
    → RE-MASTER AUDIO (apply loudnorm; don't reshoot)
ELSE:
    → SHIP
```

---

## CI Integration

```yaml
# .github/workflows/demo-quality.yml
name: Demo Quality Gate
on:
  workflow_dispatch:
  pull_request:
    paths:
      - 'demos/output/**'

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install ffmpeg + libvmaf
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg
          ffmpeg -filters | grep libvmaf
      - name: Install ffmpeg-quality-metrics
        run: pip install ffmpeg-quality-metrics
      - name: Score demos
        run: |
          for f in demos/output/*.mp4; do
            ref="${f%.mp4}_ref.mp4"
            ffmpeg -i "$f" -c:v libx264 -preset veryslow -crf 14 "$ref" -y
            ffmpeg-quality-metrics "$f" "$ref" --metrics vmaf psnr ssim --output json > "${f%.mp4}.json"
          done
      - name: Gate
        run: |
          python scripts/quality_gate.py demos/output/*.json
```

`quality_gate.py` exits non-zero if any clip is below VMAF 90 / PSNR 40 / SSIM 0.95.

---

## Capture-Side Quality Tips (prevent low scores upstream)

| Cause | Symptom | Fix |
|-------|---------|-----|
| `video.size` omitted | Output downsized to 800×800, low VMAF | Always pass `size` explicitly |
| 30 fps default + high-motion content | Choppy, low SSIM | Disable motion-heavy intros, or upgrade to AV1 |
| `slowMo` too aggressive | Long stalls; loudnorm reads silence as LUFS hit | Use `waitForTimeout` for pacing instead of `slowMo` |
| CI headless rendering | Font anti-aliasing differs from headed | Run demos headed where possible; pin Chrome for Testing build |
| VP8 default codec | Smaller, lower quality than VP9 | Set `PLAYWRIGHT_VIDEO_CODEC=vp9` |
| Long single-page session | Bitrate falls as file grows | Use `page.screencast.start/stop` per chapter |

---

## Audio Quality (paired with LUFS)

| Issue | Tool | Fix |
|-------|------|-----|
| Sibilance ("s", "sh") in TTS | ffmpeg deesser, iZotope RX, Fabfilter Pro-DS | De-ess at -6 dB threshold |
| Narration drowns under BGM | ffmpeg sidechain | Duck BGM -18 dB during narration |
| Inconsistent volume across clips | loudnorm two-pass | Normalize all clips before mixing |
| BGM not commercially licensed | Switch to ElevenLabs Music or Suno Pro+ | Day-1 commercial use both providers |

---

## Cross-References

- LUFS deeper dive → `voiceover-design.md → LUFS for Video`.
- WCAG audio description → `captions-design.md → WCAG Compliance`.
- Reshoot vs re-encode anti-patterns → `scenario-guidelines.md → Scenario Anti-Patterns`.
- Scorecard mapping → `checklist.md → Quality Scorecard (/97)` (rows Q1, Q2, Q3).

---

## References

- VMAF: github.com/Netflix/vmaf
- ffmpeg-quality-metrics: github.com/slhck/ffmpeg-quality-metrics
- ffmpeg loudnorm: ffmpeg.org/ffmpeg-filters.html#loudnorm
- "Understanding VMAF / PSNR / SSIM" — FastPix (2026)
- YouTube audio loudness: support.google.com/youtube — -14 LUFS reference
- AES TD1004 loudness recommendation for online media
