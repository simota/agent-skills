# Playwright Configuration for Demo Recording

Configuration guide for demo video recording with Playwright **1.59 ("Agentic Release", 2026-04)**.

Purpose: Read this when Director must choose demo-specific Playwright configuration, recording APIs, aspect-ratio presets, device profiles, output formats, naming conventions, environment variables, CI, or troubleshooting steps.

Contents:
- `Recording API Selection`: `page.screencast` (primary, 1.59 Stable) vs `recordVideo` (failure receipts)
- `Basic Configuration`: demo-dedicated Playwright config
- `Aspect Ratio Presets`: 16:9 / 9:16 / 4:5 / 1:1 with viewport + video.size pairings
- `Device-Specific Project Settings`: desktop, mobile, and tablet presets
- `Video Recording Settings`: video mode, resolution, and codec matrix (VP9 / AV1 / H.264)
- `page.screencast API Recipes`: start/stop, showActions, showChapter, showOverlay, onFrame
- `Vision-Stream (onFrame)`: JPEG streaming to Vision Models
- `slowMo Configuration Guide`: pace ranges and usage rules
- `Output Formats and Conversion`: WebM baseline plus MP4/AV1/GIF conversion
- `Output File Naming Conventions`: canonical demo naming patterns
- `Environment Variables`: `.env.demo` defaults
- `CI/CD Configuration`: GitHub Actions recording flow
- `Directory Structure`: expected demo file layout
- `Browser Engine Notes`: Chrome for Testing (v1.57+), browser.bind (v1.59 Stable), incremental snapshot
- `Playwright MCP vs CLI for Agentic Recording`: decision matrix for receipt capture
- `Troubleshooting`: common recording failures and fixes

---

## Recording API Selection

Since Playwright **1.59** (April 2026, "Agentic Release"), `page.screencast` is the **primary** recording API for Director. `recordVideo` remains useful for failure-only receipts and legacy single-page full-session captures.

| API | When to use | Strengths | Weaknesses |
|-----|-------------|-----------|------------|
| **`page.screencast` (PRIMARY)** | Most demos, multi-chapter narratives, agentic flows, onFrame Vision-loop | Precise start/stop, chapters, action overlays, JPEG onFrame, per-scene control | Slightly more code than `recordVideo` |
| `recordVideo` | `retain-on-failure` debug receipts, "just capture the whole session" | Zero per-test setup, automatic file lifecycle | One page per context, no chapters, no overlays, scales viewport silently to 800×800 |

Both APIs silently downscale to **800×800** when `size` is omitted. **Always set `size` explicitly.**

```ts
// PRIMARY: page.screencast (Playwright ≥ 1.59)
const screencast = await page.screencast.start({
  path: 'demos/output/checkout_complete_16x9_20260515.webm',
  size: { width: 1920, height: 1080 },
  quality: 90,           // 1–100, JPEG-frame quality
  // onFrame: (jpegBuffer, ts) => stream to Vision Model
});
await screencast.showChapter({ title: 'Step 1 — Add to cart', duration: 2000 });
await screencast.showActions({ position: 'top-right', duration: 500, fontSize: 24 });
// ... demo flow ...
await screencast.stop();

// SECONDARY: recordVideo (failure receipts)
use: {
  video: { mode: 'retain-on-failure', size: { width: 1920, height: 1080 } }
}
```

---

## Basic Configuration

### Demo-Dedicated Configuration File

```typescript
// playwright.config.demo.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // === Test Settings ===
  testDir: './demos/specs',
  timeout: 180000,         // 3 minutes (long-form demos with chapters)
  retries: 0,              // Demos should be deterministic
  workers: 1,              // Sequential execution for consistent timing

  // === Reporters ===
  reporter: [
    ['list'],
    ['html', { outputFolder: 'demos/report' }],
  ],

  use: {
    // === Browser Settings ===
    headless: false,
    launchOptions: {
      slowMo: 500,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-infobars',
      ],
    },

    // === Video Settings (recordVideo fallback for failure receipts) ===
    video: {
      mode: 'retain-on-failure',
      size: { width: 1920, height: 1080 },   // explicit — Playwright scales to 800×800 if omitted
    },

    // === Default 16:9 viewport (override per project for 9:16 / 4:5 / 1:1) ===
    viewport: { width: 1920, height: 1080 },
    locale: 'ja-JP',
    timezoneId: 'Asia/Tokyo',

    // === Network (deterministic demo runs) ===
    serviceWorkers: 'block',
  },
});
```

> Demos primarily use **`page.screencast`** inside tests for chapter control. `recordVideo` in this config exists as a safety net for unexpected failures and as a fallback for very long single-context sessions.

---

## Aspect Ratio Presets

Pick the aspect from the distribution channel **before** writing the recording. Reusing a 16:9 master on 9:16 or 4:5 crops the sides and loses key UI.

| Aspect | Use case | Viewport | `video.size` / `screencast.start({ size })` | Notes |
|--------|----------|----------|-----|-------|
| `16:9` | Web hero, YouTube, X (16:9), Vimeo, embeds | `1920×1080` | `1920×1080` | Default master. 1280×720 only for inline/GIF |
| `9:16` | TikTok, Reels, Shorts, IG Stories, TikTok cover | `1080×1920` | `1080×1920` | Mobile UA + touch; 21–34s optimal for TikTok |
| `4:5` | LinkedIn feed (2026 default), IG feed | `1080×1350` | `1080×1350` | 15–60s B2B sweet spot |
| `1:1` | Product Hunt gallery, Slack/Discord preview | `1080×1080` | `1080×1080` | Square; 45–60s gallery |

### Project Matrix (typical)

```typescript
projects: [
  {
    name: 'demo-16x9',
    use: {
      ...devices['Desktop Chrome'],
      viewport: { width: 1920, height: 1080 },
      video: { mode: 'retain-on-failure', size: { width: 1920, height: 1080 } },
    },
  },
  {
    name: 'demo-9x16-mobile',
    use: {
      ...devices['iPhone 15 Pro'],   // touch + UA
      viewport: { width: 1080, height: 1920 },
      video: { mode: 'retain-on-failure', size: { width: 1080, height: 1920 } },
      deviceScaleFactor: 1,
    },
  },
  {
    name: 'demo-4x5-linkedin',
    use: {
      ...devices['Desktop Chrome'],
      viewport: { width: 1080, height: 1350 },
      video: { mode: 'retain-on-failure', size: { width: 1080, height: 1350 } },
    },
  },
  {
    name: 'demo-1x1-producthunt',
    use: {
      ...devices['Desktop Chrome'],
      viewport: { width: 1080, height: 1080 },
      video: { mode: 'retain-on-failure', size: { width: 1080, height: 1080 } },
    },
  },
]
```

### Aspect-Aware Re-framing

For 9:16 / 4:5, the same DOM rarely frames well. Strategies:

- **Layout switch**: drive the app's responsive breakpoint (use `Mobile` device preset).
- **CSS injection**: inject demo-only stylesheet to enlarge the hero region.
- **Scroll-and-focus**: use `smoothScrollTo()` + `evaluate(scale)` to zoom on the active widget.
- **Overlay padding**: pad top/bottom letterbox bars for non-responsive screens; show chapter overlays in the bars.

---

## Device-Specific Project Settings

### Desktop Settings

```typescript
{
  name: 'demo-desktop',
  use: {
    ...devices['Desktop Chrome'],
    viewport: { width: 1280, height: 720 },
    launchOptions: {
      slowMo: 500,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-infobars',
      ],
    },
    video: {
      mode: 'on',
      size: { width: 1280, height: 720 },
    },
  },
}
```

### Mobile Settings

```typescript
{
  name: 'demo-mobile-ios',
  use: {
    ...devices['iPhone 12'],
    launchOptions: { slowMo: 600 },
    video: {
      mode: 'on',
      size: { width: 390, height: 844 },
    },
    hasTouch: true,
  },
}

{
  name: 'demo-mobile-android',
  use: {
    ...devices['Pixel 5'],
    launchOptions: { slowMo: 600 },
    video: {
      mode: 'on',
      size: { width: 393, height: 851 },
    },
    hasTouch: true,
  },
}
```

### Tablet Settings

```typescript
{
  name: 'demo-tablet',
  use: {
    ...devices['iPad Pro 11'],
    launchOptions: { slowMo: 550 },
    video: {
      mode: 'on',
      size: { width: 834, height: 1194 },
    },
  },
}
```

---

## High-Fidelity Capture (HiDPI / 4K)

Three independent knobs raise demo quality. Combine for the sharpest result.

### Knob 1: `deviceScaleFactor` (HiDPI rendering)

The single biggest win. Renders internally at DPR=2 (or 3) and downsamples to `video.size`, giving Retina-class fonts and icons even in a 1080p file.

```typescript
// Context option (preferred — Playwright-native)
use: {
  viewport: { width: 1920, height: 1080 },
  deviceScaleFactor: 2,                          // HiDPI
  video: { mode: 'on', size: { width: 1920, height: 1080 } },
}

// Or via Chrome flag (equivalent, browser-wide)
launchOptions: {
  args: ['--force-device-scale-factor=2'],
}
```

| `deviceScaleFactor` | Effect | File size | When to use |
|---------------------|--------|-----------|-------------|
| `1` (default) | 1:1 pixel mapping | baseline | inline GIF, low-cost CI |
| **`2` (recommended)** | Retina rendering, AA-smooth fonts | same as 1× | **default for external demos** |
| `3` | iPhone-Pro-class density | same as 1× | small-screen / mobile-only |

> The video file resolution **does not change** — only the rendered DPI does. If you want a literal 4K file, raise `viewport` + `video.size` to `3840×2160` (Knob 2 below).

### Knob 2: Native 4K capture

Use only when archival or YouTube hero quality is needed — file size triples vs 1080p HiDPI.

```typescript
{
  name: 'demo-4k',
  use: {
    viewport: { width: 3840, height: 2160 },
    deviceScaleFactor: 1,                         // already at 4K natively
    video: { mode: 'on', size: { width: 3840, height: 2160 } },
    launchOptions: {
      args: [
        '--enable-features=VaapiVideoEncoder',    // GPU encode where available
        '--disable-gpu-vsync',
      ],
    },
  },
}
```

Encode hint: convert WebM → AV1 for delivery (`-c:v libsvtav1 -crf 32`); H.264 at 4K balloons file size.

### Knob 3: Anti-aliasing & rendering flags

Stabilize fonts and motion across CI / local / headed / headless.

```typescript
launchOptions: {
  args: [
    '--force-device-scale-factor=2',             // HiDPI (alt to context option)
    '--font-render-hinting=none',                // platform-consistent font rendering
    '--disable-gpu-vsync',                       // avoid vsync tearing in screencast
    '--disable-features=PaintHolding,LazyFrameLoading', // prevent frame skips
    '--disable-background-timer-throttling',     // smooth animations in headed mode
    '--disable-renderer-backgrounding',
    '--disable-blink-features=AutomationControlled',
  ],
}
```

### Knob 4: Codec & post-encode

```bash
# Raise capture-side codec from VP8 → VP9
PLAYWRIGHT_VIDEO_CODEC=vp9 npx playwright test --config=playwright.config.demo.ts

# Post-encode to visually lossless H.264 (CRF 18) for distribution
ffmpeg -i demo.webm -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -movflags +faststart -c:a aac -b:a 192k demo.mp4

# Archival AV1 (smaller, slower encode)
ffmpeg -i demo.webm -c:v libsvtav1 -crf 30 -preset 6 -pix_fmt yuv420p10le \
  -c:a libopus demo_av1.mp4
```

CRF guide: `14` lossless, `18` visually lossless (recommended for masters), `22` standard, `28` aggressive.

### Knob 5: `page.screencast` quality

```typescript
await page.screencast.start({
  path: 'demo.webm',
  size: { width: 1920, height: 1080 },
  quality: 95,                                    // 1–100 (JPEG-frame quality, default ~80)
});
```

`quality: 90–95` recommended for external demos; below 80 visible compression.

### Combined Recipe (recommended default for 2026)

```typescript
// playwright.config.demo.ts — 1080p HiDPI default
projects: [
  {
    name: 'demo-16x9-hidpi',
    use: {
      viewport: { width: 1920, height: 1080 },
      deviceScaleFactor: 2,
      video: { mode: 'retain-on-failure', size: { width: 1920, height: 1080 } },
      launchOptions: {
        args: [
          '--font-render-hinting=none',
          '--disable-gpu-vsync',
          '--disable-features=PaintHolding',
          '--disable-blink-features=AutomationControlled',
        ],
      },
    },
  },
]
```

```typescript
// In-test capture with page.screencast quality=95
const sc = await page.screencast.start({
  path: 'demos/output/feature_16x9_hidpi_20260515.webm',
  size: { width: 1920, height: 1080 },
  quality: 95,
});
```

### Quality vs Cost Matrix

| Setup | Render cost | File size | Visual sharpness | When |
|-------|-------------|-----------|------------------|------|
| 720p, scale=1, VP8 | low | small | mediocre | inline GIF / quick PR receipt |
| 1080p, scale=1, VP9 | medium | medium | good | standard internal demos |
| **1080p, scale=2, VP9, quality=95** | medium-high | medium | **excellent** | **default for external demos** |
| 4K native, scale=1, AV1 | high | large | archival | YouTube hero / 4K masters |

### Verification

After capture, verify perceptual quality with `reference/quality-metrics.md` (VMAF/PSNR/SSIM). HiDPI capture should comfortably clear VMAF ≥ 92 at 1080p.

### Caveats

- HiDPI doubles GPU work — verify CI keeps 30 fps. If not, drop `deviceScaleFactor` to 1 or move CI to a GPU runner.
- `--force-device-scale-factor` overrides Playwright's `deviceScaleFactor` context option. Pick one, not both.
- Some sites detect HiDPI and serve `@2x` images; this is usually what you want for demos, but watch for sites that downscale instead.
- Headless mode with HiDPI rendering can differ slightly from headed; pin `channel: 'chrome'` or run headed for hero captures.

---

## Video Recording Settings

### Video Modes

| Mode | Use Case | File Generation |
|------|----------|-----------------|
| `'on'` | Always record (legacy) | Video for all tests |
| `'retain-on-failure'` | Only on failure | Default for `recordVideo` safety net |
| `'on-first-retry'` | On retry | For CI (not used in demos) |
| `'off'` | No recording | Development/debugging |

> Prefer `page.screencast` start/stop inside the test for primary capture. Use `recordVideo: 'retain-on-failure'` as a debug receipt fallback.

### Resolution Settings (1080p is the new baseline)

| Resolution | Use Case | Approx. File Size (1080p VP9) |
|------------|----------|-------------------------------|
| 1920×1080 (1080p) | Master, YouTube, LinkedIn, hero | ~8 MB / 30s |
| 1080×1920 (9:16 vertical) | TikTok, Reels, Shorts | ~7 MB / 30s |
| 1080×1350 (4:5) | LinkedIn 2026 default | ~6 MB / 30s |
| 1080×1080 (1:1) | Product Hunt gallery | ~5 MB / 30s |
| 1280×720 (720p) | Inline / GIF source / older embeds | ~4 MB / 30s |
| 3840×2160 (4K) | YouTube hero, archival master | ~30 MB / 30s |

### Codec Selection Matrix (2026)

| Codec | Container | Use Case | Browser Support | Pros | Cons |
|-------|-----------|----------|-----------------|------|------|
| **VP9** | WebM | Playwright default, web embed | Chrome / FF / Edge / Safari (macOS 14+) | Free, decent compression, browser native | Larger than AV1 |
| **AV1** | WebM / MP4 | Archival master, high-compression delivery | Chrome / FF / Edge / Safari (macOS 16+) | 15-20% smaller than VP9, 30-50% smaller than HEVC at same quality | Slower encode |
| **H.264 (libx264)** | MP4 | Universal playback, Slack / email / Premiere | All players | Universal support, AAC pairs well | Largest file |
| **HEVC (libx265)** | MP4 | 4K + HDR delivery | Safari + recent Chrome | HDR10 / HDR10+ support | Patent/licensing concerns |
| VP8 | WebM | Legacy only | All browsers | Universal WebM fallback | Deprecated by VP9 |

```bash
# Playwright env override
PLAYWRIGHT_VIDEO_CODEC=vp9 npx playwright test --config=playwright.config.demo.ts

# Convert to AV1 (high-compression delivery)
ffmpeg -i demo.webm -c:v libsvtav1 -crf 35 -preset 6 -c:a libopus demo_av1.webm

# Convert to H.264 MP4 (universal)
ffmpeg -i demo.webm -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 192k demo.mp4
```

> **HDR / 120fps**: Playwright outputs SDR VP8/VP9 only. For HDR10+ or 120fps deliverables, transcode in post (HEVC/AV1) or route the requirement to AI video generators (Sora 2 / Veo 3.1 / Runway Gen-4.5) — Director cannot produce native HDR from the browser.

---

## page.screencast API Recipes

`page.screencast` (v1.59 Stable) is the primary recording API. It exposes start/stop, chapter markers, action overlays, custom overlays, and a JPEG-frame callback (`onFrame`) for Vision streaming.

### Methods

| Method | Required params | Default | Purpose |
|--------|-----------------|---------|---------|
| `start({ path, size, quality, onFrame })` | `path` | size scales to 800×800 if omitted | Begin capture |
| `stop()` | — | — | End capture, flush file |
| `showActions({ position, duration, fontSize })` | — | top-right / 500ms / 24px | Auto-annotate user actions in the recording |
| `hideActions()` | — | — | Stop auto-annotating |
| `showChapter({ title, description, duration })` | `title` | duration 2000ms | Display a chapter card |
| `showOverlay({ html, duration })` | `html` | — | Display arbitrary HTML overlay |
| `showOverlays()` / `hideOverlays()` | — | — | Toggle visibility globally |

### Standard Chapter Pattern

```typescript
const screencast = await page.screencast.start({
  path: 'demos/output/onboard_signup_16x9_20260515.webm',
  size: { width: 1920, height: 1080 },
  quality: 90,
});

await screencast.showActions(); // auto-annotate clicks, fills, navigations

await screencast.showChapter({ title: 'Chapter 1', description: 'Sign up in 30 seconds' });
await page.goto('/signup');
await page.getByLabel('Email').pressSequentially('demo@acme.test', { delay: 80 });

await screencast.showChapter({ title: 'Chapter 2', description: 'Connect your data' });
// ...

await screencast.stop();
```

### Custom Overlay (HTML)

```typescript
await screencast.showOverlay({
  html: `
    <div style="position:fixed;bottom:48px;left:50%;transform:translateX(-50%);
                background:rgba(0,0,0,0.85);color:#fff;
                padding:16px 32px;border-radius:12px;font:600 24px Inter;">
      ⚡ 5x faster than Excel
    </div>
  `,
  duration: 2500,
});
```

### Multi-Chapter Series (3×45s blueprint)

```typescript
for (const chapter of chapters) {
  const sc = await page.screencast.start({
    path: `demos/output/${feature}_${chapter.slug}_16x9_20260515.webm`,
    size: { width: 1920, height: 1080 },
  });
  await sc.showChapter({ title: chapter.title });
  await chapter.run(page);
  await sc.stop();
}
```

---

## Vision-Stream (onFrame)

`onFrame(jpegBuffer, timestampMs)` fires for each captured frame. Use it to stream live JPEGs to a Vision Model (GPT-4o vision, Claude vision) for "agent watches the screen" loops, live narration, or QA-by-vision.

```typescript
const screencast = await page.screencast.start({
  path: 'demos/output/agent_session_20260515.webm',
  size: { width: 1280, height: 720 },
  quality: 80,
  onFrame: async (jpeg, ts) => {
    // throttle to ~1 fps for Vision API cost control
    if (ts - lastSent < 1000) return;
    lastSent = ts;
    await visionClient.send({
      image: jpeg.toString('base64'),
      prompt: 'What is the user doing right now? Anything off-screen-worthy?',
    });
  },
});

// agent loop runs as normal Playwright code
await page.goto('/dashboard');
// ...
await screencast.stop();
```

> **Cost guard**: `onFrame` fires at ~30 fps. Always throttle (1–4 fps is plenty for narrative agents). Without throttling, a 60s demo = 1,800 Vision calls.

---

## slowMo Configuration Guide

### slowMo Values by Use Case

| Use Case | slowMo (ms) | Description |
|----------|-------------|-------------|
| Quick demo | 300 | For experienced users |
| Standard demo | 500 | General demo |
| Beginner-focused | 700 | Show slowly and carefully |
| Form-heavy | 600-700 | Show input content |
| Presentation | 800-1000 | Explain while showing |

### Dynamic slowMo Adjustment

```typescript
test('demo emphasizing form input', async ({ page }) => {
  // Normal speed for navigation
  await page.goto('/signup');

  // Slow for form input (adjust with manual wait)
  await page.getByLabel('Name').fill('Demo User');
  await page.waitForTimeout(500); // Additional pacing pause

  await page.getByLabel('Email').fill('demo@example.com');
  await page.waitForTimeout(500);

  // Normal speed for button click
  await page.getByRole('button', { name: 'Register' }).click();
});
```

---

## Output Formats and Conversion

### Default Output (WebM)

Playwright natively outputs WebM (VP8). For broader compatibility, convert to MP4 or GIF.

### FFmpeg Post-Processing Helper

```typescript
// demos/helpers/video-convert.ts
import { execSync } from 'child_process';
import path from 'path';

/**
 * Convert WebM to MP4 (H.264) for universal playback
 */
export function convertToMp4(webmPath: string): string {
  const mp4Path = webmPath.replace(/\.webm$/, '.mp4');
  execSync(
    `ffmpeg -i "${webmPath}" -c:v libx264 -preset fast -crf 22 -c:a aac "${mp4Path}" -y`,
    { stdio: 'pipe' }
  );
  return mp4Path;
}

/**
 * Convert WebM to GIF for embedding in docs/README
 */
export function convertToGif(webmPath: string, opts?: { width?: number; fps?: number }): string {
  const { width = 640, fps = 10 } = opts ?? {};
  const gifPath = webmPath.replace(/\.webm$/, '.gif');
  execSync(
    `ffmpeg -i "${webmPath}" -vf "fps=${fps},scale=${width}:-1:flags=lanczos" "${gifPath}" -y`,
    { stdio: 'pipe' }
  );
  return gifPath;
}
```

### Auto-Conversion in afterEach

```typescript
import { convertToMp4, convertToGif } from '../helpers/video-convert';

test.afterEach(async ({ page }, testInfo) => {
  const video = page.video();
  if (!video) return;

  const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const baseName = `${testInfo.title.replace(/\s+/g, '_')}_${date}`;
  const webmPath = `demos/output/${baseName}.webm`;

  await video.saveAs(webmPath);

  // Generate MP4 for Slack/email/presentations
  convertToMp4(webmPath);

  // Generate GIF for README/docs (optional)
  // convertToGif(webmPath, { width: 800, fps: 12 });

  await testInfo.attach('demo-video', { path: webmPath, contentType: 'video/webm' });
});
```

### Format Selection Guide

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| WebM | Web embedding, internal | Small size, native output | Limited player support |
| MP4 | Slack, email, presentations | Universal playback | Larger file, needs FFmpeg |
| GIF | README, docs, PRs | Inline display, no player | Large file, no audio, lower quality |

---

## Output File Naming Conventions

Naming encodes feature, action, aspect, and date for fast filtering and CDN routing.

| Pattern | Example | Use Case |
|---------|---------|----------|
| `[feature]_[action]_[aspect]_[date].webm` | `checkout_complete_16x9_20260515.webm` | Feature demo (default) |
| `[feature]_[action]_9x16_[date].webm` | `checkout_complete_9x16_20260515.webm` | TikTok / Reels / Shorts |
| `[feature]_[action]_4x5_[date].webm` | `checkout_complete_4x5_20260515.webm` | LinkedIn |
| `[feature]_[action]_1x1_[date].webm` | `checkout_complete_1x1_20260515.webm` | Product Hunt |
| `onboarding_step[N]_[aspect]_[date].webm` | `onboarding_step1_16x9_20260515.webm` | Onboarding |
| `release_v[version]_[feature]_[aspect].webm` | `release_v3.0_newui_16x9.webm` | Release introduction |
| `agent_receipt_[task]_[date].webm` | `agent_receipt_pr-review_20260515.webm` | Agentic visual receipt |

---

## Environment Variables

```bash
# .env.demo
DEMO_BASE_URL=http://localhost:3000
DEMO_USER_EMAIL=demo@example.com
DEMO_USER_PASSWORD=DemoPass123
```

```typescript
// playwright.config.demo.ts
import dotenv from 'dotenv';
dotenv.config({ path: '.env.demo' });

export default defineConfig({
  use: {
    baseURL: process.env.DEMO_BASE_URL,
  },
});
```

---

## CI/CD Configuration

### Demo Recording with GitHub Actions

```yaml
# .github/workflows/demo-recording.yml
name: Record Demo Videos

on:
  workflow_dispatch:
    inputs:
      feature:
        description: 'Feature to demo'
        required: true
        default: 'all'

jobs:
  record:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - name: Record demos
        run: npx playwright test --config=playwright.config.demo.ts
      - name: Convert to MP4
        run: |
          sudo apt-get install -y ffmpeg
          for f in demos/output/*.webm; do
            ffmpeg -i "$f" -c:v libx264 -preset fast -crf 22 "${f%.webm}.mp4" -y
          done
      - uses: actions/upload-artifact@v4
        with:
          name: demo-videos
          path: |
            demos/output/*.webm
            demos/output/*.mp4
```

---

## Directory Structure

```
demos/
├── specs/           # Demo test files
├── helpers/         # Helper functions (overlay, auth, data, video-convert)
├── fixtures/        # Test data, images
├── output/          # Generated videos (WebM + MP4 + GIF)
└── report/          # HTML reports
```

---

## Browser Engine Notes

### Chrome for Testing (v1.57+)

Since Playwright 1.57, demos use Chrome for Testing builds instead of vanilla Chromium.

| Mode | Runtime | Notes |
|------|---------|-------|
| Headed (standard for demos) | `chrome` | Default for visible recordings |
| Headless | `chrome-headless-shell` | Used for CI and audio-enabled runs |

Chrome for Testing may render fonts and anti-aliasing slightly differently from Chromium. When upgrading Playwright across major versions, re-check overlay text clarity, brand colors, and icon crispness on existing demos.

Pin a specific channel only when reproducibility or CI memory footprint is critical:

```typescript
use: {
  channel: 'chromium', // fall back to legacy Chromium build
}
```

### browser.bind() for Shared Sessions (v1.59 Stable)

`browser.bind()` exposes a launched browser instance over WebSocket to `@playwright/cli`, `@playwright/mcp`, and other clients **simultaneously**. Use this when the demo script and an agentic receipt client (or a Claude/Cursor MCP loop) should share one browser — avoids launching duplicate Chromes and doubling memory.

```typescript
const browser = await chromium.launch({ headless: false });
const ws = await browser.bind({ port: 9222 }); // share with CLI/MCP clients
console.log('Bound at', ws.wsEndpoint());
// demo flow runs here; CLI / MCP clients can attach in parallel
```

Inspect all bound browsers with:

```bash
npx @playwright/cli show   # dashboard UI listing bound sessions
```

Typical scenarios:
- A CI job runs a feature flow while Claude (via MCP) annotates / narrates the same session.
- A Director recording shares the browser with `@playwright/cli` for trace export.
- A Vision-loop agent (`onFrame` consumer) watches the screen while the demo executes.

### Incremental Snapshot Mode (v1.59 default)

v1.59 ships `incremental snapshot` as the default snapshot mode. Long Playwright sessions used to re-send full DOM snapshots per step, ballooning token usage in agentic pipelines. Now only deltas are sent. **No config change needed**; benefit is automatic in 1.59+. For Director's `agentic_video_receipts` capability this reduces per-step token cost noticeably in 30+ step flows.

---

## Playwright MCP vs CLI for Agentic Recording

When agents produce video receipts of automated work, choose the transport based on environment and workload shape.

### Decision Matrix

| Context | Recommended | Rationale |
|---------|-------------|-----------|
| Agent has filesystem access (Claude Code, Cursor, Copilot) | `@playwright/cli` | ~4x token reduction vs MCP (~27k vs ~114k per task) |
| High-throughput receipt capture in CI | `@playwright/cli` | Lower token accumulation across steps |
| Sandboxed environment, no filesystem | Playwright MCP | Only viable transport |
| Exploratory / iterative browser session | Playwright MCP | Preserves persistent browser state across turns |
| Long-running autonomous workflow needing live context | Playwright MCP | Streaming context fits agent loop |

### Decision Shortcut

- Agent has filesystem access → CLI.
- Sandboxed environment → MCP.
- Step count > 10 sequential interactions → CLI (token accumulation compounds per step in MCP).

Microsoft's public guidance (early 2026) recommends CLI for coding agents and reserves MCP for exploratory / autonomous workflows.

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Video not generated | Context not closed | Ensure `page.close()` in afterEach |
| Video cut off midway | Test ends too fast | Add `waitForTimeout(1000)` at end |
| Video is choppy | Machine load | Use `headless: true` or reduce resolution |
| File size too large | High resolution/duration | Lower to 720p, reduce duration |
| WebM won't play | Player doesn't support VP8 | Convert to MP4 with FFmpeg |
| `test-results/` disk bloat | Accumulated `.webm` files (2–5 MB / min at 720p) | Remove or archive after each session; add cleanup to CI |
| Font rendering differs after upgrade | Chrome for Testing vs Chromium | Pin `channel: 'chromium'` or re-record baselines |
| Duplicate browsers in CI | Demo + receipt client launching separately | Use `browser.bind()` to share one browser |
| 9:16 demo crops critical UI | Reused 16:9 viewport for 9:16 capture | Switch viewport + use Mobile device preset; consider CSS injection to re-flow layout |
| 4:5 LinkedIn demo looks cramped | Default 1280×720 viewport with sides padded | Use 1080×1350 viewport directly; design demo at this size |
| `onFrame` runs out of memory / costs too much | Default 30 fps callback | Throttle to 1–4 fps inside callback (`if (ts - lastSent < 250) return;`) |
| Video size is 800×800 despite 1920 viewport | `size` omitted in `screencast.start()` or `recordVideo` | Always pass `size: { width, height }` explicitly |
| VMAF < 90 with default encoder | VP8 default codec, high motion content | Switch to VP9 (`PLAYWRIGHT_VIDEO_CODEC=vp9`) or post-encode with AV1 |
| Transcript missing for new external demo | GEO/AI-citation step skipped | Always run the `geo` recipe before Deliver |
