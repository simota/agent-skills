# Implementation Patterns

Playwright implementation patterns for demo video recording.

Purpose: Read this when Director needs concrete Playwright implementation patterns for scenes, auth, overlays, interaction effects, performance demos, comparison layouts, narration, persona-aware flows, or ARIA validation.

Contents:
- `page.screencast Patterns (2026 PRIMARY)`: 1.59 Stable API recipes
- `3-Second Layered Hook Implementation`: opening pattern that holds the first 3 seconds
- `Vision-Stream (onFrame)`: JPEG streaming to Vision Models for agentic loops
- `Multi-Aspect Recording`: orchestrating 16:9 / 9:16 / 4:5 / 1:1 from one scenario
- `B-roll Overlay Pattern`: 70–85% opacity overlay with caption-safe positioning
- `Basic Test Structure`: scene organization with `test.step()`
- `Authentication Patterns`: API login, localStorage, and storage-state setup
- `File Upload Pattern` / `Smooth Scroll Pattern`: common demo interactions
- `Overlay` / `Highlight` / `Cursor` / `Interaction Feedback`: viewer-guidance helpers
- `Scenario Recording System`: reusable step-driven recording orchestration
- `Performance Visualization System`: Core Web Vitals overlays and performance framing
- `Before/After Comparison Mode`: redesign and comparison layouts
- `AI Narration System`: narration helpers and synchronization
- `Progress Bar` / `Spotlight`: visual emphasis helpers
- `Page Transition Wait Pattern`: state-change pacing rules
- `Test Data Factory`: realistic demo data setup
- `Persona-Aware Demo Recording`: Echo-driven persona timing patterns
- `ARIA Snapshot Validation`: accessibility validation during demos
- `Complete Demo Example`: integrated reference pattern

---

## page.screencast Patterns (2026 PRIMARY)

`page.screencast` is the **primary** recording API since Playwright 1.59 (2026-04). It supports precise start/stop, chapters, auto-action annotations, custom overlays, and a JPEG-frame callback (`onFrame`) — all of which Director relies on for narrative video production.

### Chaptered Demo (replaces single-shot `recordVideo`)

```typescript
// demos/specs/checkout-chaptered.spec.ts
import { test } from '@playwright/test';

test('checkout — chaptered demo', async ({ page }) => {
  const sc = await page.screencast.start({
    path: 'demos/output/checkout_complete_16x9_20260515.webm',
    size: { width: 1920, height: 1080 },
    quality: 90,
  });

  // Auto-annotate clicks/fills/navigations
  await sc.showActions({ position: 'top-right', duration: 600, fontSize: 22 });

  await sc.showChapter({
    title: 'Chapter 1 — Add to cart',
    description: 'Pick a product and add it to the cart.',
    duration: 2000,
  });
  await page.goto('/products/awesome');
  await page.getByRole('button', { name: 'Add to cart' }).click();

  await sc.showChapter({
    title: 'Chapter 2 — Checkout',
    description: 'Frictionless single-screen checkout.',
  });
  await page.goto('/checkout');
  await page.getByLabel('Email').pressSequentially('demo@acme.test', { delay: 80 });
  await page.getByRole('button', { name: 'Pay $39.80' }).click();

  await sc.showOverlay({
    html: `<div class="aha">⚡ Done in 8 seconds</div>`,
    duration: 2500,
  });

  await sc.stop();
});
```

### Replacing Custom Overlay Helpers

Prefer `screencast.showActions()` over hand-rolled cursor / click highlighters when:
- The demo's visual emphasis is "what did the user just click?"
- The recording is for a developer / power-user audience.

Use custom overlays (`showOverlay({ html })`) when:
- You need brand-styled callouts.
- You need a chart, code block, or animated metric on screen.
- The narrative beat is "the result" (callout the number / outcome).

---

## 3-Second Layered Hook Implementation

Goal: by 3 seconds in, the viewer has seen a visual change, read a 3–5 word hook, and (optionally) heard a sound cue.

```typescript
test('hook — schema-drift problem', async ({ page }) => {
  const sc = await page.screencast.start({
    path: 'demos/output/migrate_hook_16x9_20260515.webm',
    size: { width: 1920, height: 1080 },
  });

  // T+0.0s: Visual — broken state on screen immediately
  await page.goto('/playground?seed=broken-migration');

  // T+0.3s: Text hook overlay (3-5 words, big bold)
  await sc.showOverlay({
    html: `
      <div style="
        position:fixed; inset:0;
        display:flex; align-items:flex-end; justify-content:center;
        padding-bottom:48px; pointer-events:none;">
        <div style="
          background:#E11D48; color:white;
          padding:20px 36px; border-radius:14px;
          font:800 56px/1.1 Inter, sans-serif;
          letter-spacing:-0.02em;">
          Schema drift broke prod.
        </div>
      </div>`,
    duration: 2400,
  });

  // T+0.5s: Optional audio cue via SFX overlay (HTML5 audio injected into page)
  await page.evaluate(() => {
    const a = new Audio('/assets/whoosh.mp3');
    a.volume = 0.4; a.play();
  });

  // T+3.0s: Continue into Pain → Solution
  await page.waitForTimeout(2400);
  await sc.showChapter({ title: 'The pain', duration: 1500 });
  // ...
  await sc.stop();
});
```

**Anti-pattern**: starting on a logo splash or a clean landing page. The viewer's eye lands on nothing and they bounce.

---

## Vision-Stream (onFrame)

`onFrame` streams JPEG frames to a callback. Use it to feed a Vision Model (GPT-4o vision, Claude vision) for live narration, agentic feedback loops, or visual QA.

```typescript
import { test } from '@playwright/test';

let lastSent = 0;
const FPS_LIMIT = 2;  // 2 fps to a Vision API is plenty for narrative agents

test('agent watches the screen', async ({ page }) => {
  const sc = await page.screencast.start({
    path: 'demos/output/agent_session_20260515.webm',
    size: { width: 1280, height: 720 },
    quality: 80,
    onFrame: async (jpegBuffer, tsMs) => {
      if (tsMs - lastSent < 1000 / FPS_LIMIT) return;
      lastSent = tsMs;
      // Pseudocode — replace with your Vision client
      await visionClient.observe({
        image: jpegBuffer.toString('base64'),
        prompt: 'Describe the user-visible state. Flag anomalies.',
      });
    },
  });

  // Agent / demo workflow runs as normal Playwright code
  await page.goto('/dashboard');
  // ...

  await sc.stop();
});
```

> **Cost guard**: throttle to 1–4 fps. Without throttling, a 60s demo sends ~1,800 frames to the Vision API.

---

## Multi-Aspect Recording

Drive a single scenario through multiple aspect-tuned viewports. Each aspect gets its own `page.screencast` recording.

```typescript
// demos/specs/checkout-multi-aspect.spec.ts
import { test } from '@playwright/test';

const ASPECTS = [
  { name: '16x9', viewport: { width: 1920, height: 1080 } },
  { name: '9x16', viewport: { width: 1080, height: 1920 } },
  { name: '4x5',  viewport: { width: 1080, height: 1350 } },
  { name: '1x1',  viewport: { width: 1080, height: 1080 } },
];

for (const aspect of ASPECTS) {
  test.describe(`Aspect: ${aspect.name}`, () => {
    test.use({ viewport: aspect.viewport });

    test(`checkout — ${aspect.name}`, async ({ page }) => {
      const sc = await page.screencast.start({
        path: `demos/output/checkout_complete_${aspect.name}_20260515.webm`,
        size: aspect.viewport,
        quality: 90,
      });
      await sc.showActions();

      // Aspect-aware re-framing (inject layout overrides for 9:16 / 4:5)
      if (aspect.name === '9x16' || aspect.name === '4x5') {
        await page.addStyleTag({
          content: `
            .sidebar { display: none !important; }
            .hero { font-size: 3rem !important; }
          `,
        });
      }

      await page.goto('/products/awesome');
      await page.getByRole('button', { name: 'Add to cart' }).click();
      // ...

      await sc.stop();
    });
  });
}
```

Or via `playwright.config.demo.ts` `projects` matrix — see `playwright-config.md → Aspect Ratio Presets`.

---

## B-roll Overlay Pattern

B-roll at 70–85% opacity over a stable base scene extends narration without losing visual interest. Position B-roll to avoid the bottom 15% (caption-safe band).

```typescript
async function showBRoll(
  page: Page,
  imageUrl: string,
  opts: { duration: number; opacity?: number; position?: 'top' | 'center' }
) {
  const opacity = opts.opacity ?? 0.78;
  const top = opts.position === 'top' ? '5%' : '20%';

  await page.evaluate(
    ({ url, op, top, dur }) => {
      const img = document.createElement('img');
      img.src = url;
      img.style.cssText = `
        position:fixed; top:${top}; left:50%; transform:translateX(-50%);
        max-width:60vw; max-height:55vh;
        opacity:${op};
        z-index:9998;
        border-radius:12px;
        box-shadow:0 12px 48px rgba(0,0,0,0.4);
        transition:opacity 400ms ease;
      `;
      img.dataset.broll = 'true';
      document.body.appendChild(img);
      setTimeout(() => {
        img.style.opacity = '0';
        setTimeout(() => img.remove(), 400);
      }, dur - 400);
    },
    { url: imageUrl, op: opacity, top, dur: opts.duration }
  );
}

// Usage
await showBRoll(page, '/demo-assets/mobile-capture.png', {
  duration: 4000,
  opacity: 0.8,
  position: 'top',
});
```

---

---

## Basic Test Structure

### Standard Demo Test (using test.step)

Use `test.step()` to organize scenes — provides structured reporting and pinpoints failures to exact scenes.

```typescript
// demos/specs/demo-login.spec.ts
import { test, expect } from '@playwright/test';
import { showOverlay } from '../helpers/overlay';
import { DemoData } from '../helpers/data';

test.describe('Demo: Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('shows complete login experience', async ({ page }) => {
    await test.step('Scene: Opening — Landing page', async () => {
      await showOverlay(page, 'Let\'s log in', 2000);
      await page.waitForTimeout(1000); // Pacing pause
    });

    await test.step('Scene: Login form input', async () => {
      await page.getByRole('link', { name: 'Login' }).click();
      await expect(page.getByLabel('Email')).toBeVisible();

      await page.getByLabel('Email').fill(DemoData.user.email);
      await page.waitForTimeout(400);

      await page.getByLabel('Password').fill(DemoData.user.password);
      await page.waitForTimeout(400);
    });

    await test.step('Scene: Submit and redirect', async () => {
      await page.getByRole('button', { name: 'Login' }).click();
      await page.waitForURL('**/dashboard');
      await expect(page.getByText('Welcome')).toBeVisible();
    });

    await test.step('Scene: Closing — Dashboard', async () => {
      await showOverlay(page, 'Login complete!', 2000);
      await page.waitForTimeout(1500);
    });
  });
// ...
```

---

## Authentication Patterns

### Pattern 1: API-based Pre-authentication

```typescript
// demos/helpers/auth.ts
import { Page, BrowserContext } from '@playwright/test';

export async function loginViaApi(context: BrowserContext): Promise<void> {
  const response = await context.request.post('/api/auth/login', {
    data: {
      email: 'demo@example.com',
      password: 'DemoPass123',
    },
  });

  if (!response.ok()) {
    throw new Error('Demo login failed');
  }
}
// ...
```

### Pattern 2: LocalStorage-based

```typescript
// demos/helpers/auth.ts
export async function setAuthState(page: Page, token: string): Promise<void> {
  await page.evaluate((t) => {
    localStorage.setItem('auth_token', t);
  }, token);
}

// Usage
test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await setAuthState(page, 'demo-jwt-token');
  await page.reload();
});
```

### Pattern 3: Storage State File

```typescript
// demos/auth.setup.ts
import { test as setup } from '@playwright/test';
import path from 'path';

const authFile = path.join(__dirname, '.auth/demo-user.json');

setup('authenticate demo user', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('demo@example.com');
  await page.getByLabel('Password').fill('DemoPass123');
  await page.getByRole('button', { name: 'Login' }).click();
  await page.waitForURL('**/dashboard');
  await page.context().storageState({ path: authFile });
});

// ...
```

---

## File Upload Pattern

### Image Upload Demo

```typescript
// demos/specs/demo-upload.spec.ts
import { test, expect } from '@playwright/test';
import path from 'path';

test('shows profile image upload', async ({ page }) => {
  await page.goto('/profile/edit');

  // Focus on upload button
  await showOverlay(page, 'Changing profile image', 2000);

  // File selection
  const fileInput = page.locator('input[type="file"]');
  await fileInput.setInputFiles(path.join(__dirname, '../fixtures/avatar.png'));

  // Wait for preview display
// ...
```

---

## Smooth Scroll Pattern

### Natural Scroll Behavior

```typescript
// demos/helpers/scroll.ts
import { Page } from '@playwright/test';

export async function smoothScrollTo(
  page: Page,
  selector: string,
  options: { duration?: number; position?: 'center' | 'start' | 'end' } = {}
): Promise<void> {
  const { duration = 500, position = 'center' } = options;

  await page.evaluate(
    ({ sel, dur, pos }) => {
      const element = document.querySelector(sel);
      if (!element) return;

// ...
```

---

## Overlay Helper Functions

### Complete Overlay System

```typescript
// demos/helpers/overlay.ts
import { Page } from '@playwright/test';

interface OverlayOptions {
  position?: 'top' | 'center' | 'bottom';
  style?: 'info' | 'success' | 'warning' | 'error';
  duration?: number;
}

const styleColors = {
  info: 'rgba(0, 0, 0, 0.85)',
  success: 'rgba(16, 185, 129, 0.9)',
  warning: 'rgba(245, 158, 11, 0.9)',
  error: 'rgba(239, 68, 68, 0.9)',
};
// ...
```

---

## Element Highlight Pattern

### Emphasize Specific Element

```typescript
// demos/helpers/highlight.ts
import { Page } from '@playwright/test';

export async function highlightElement(
  page: Page,
  selector: string,
  options: { duration?: number; color?: string; label?: string } = {}
): Promise<void> {
  const { duration = 2000, color = '#3b82f6', label } = options;

  await page.evaluate(
    ({ sel, dur, col, lbl }) => {
      const element = document.querySelector(sel);
      if (!element) return;

// ...
```

---

## Mouse Cursor Simulation

### Visual Mouse Movement

```typescript
// demos/helpers/cursor.ts
import { Page } from '@playwright/test';

export async function showCursor(page: Page): Promise<void> {
  await page.evaluate(() => {
    const cursor = document.createElement('div');
    cursor.id = 'demo-cursor';
    cursor.style.cssText = `
      position: fixed;
      width: 20px;
      height: 20px;
      background: rgba(59, 130, 246, 0.5);
      border: 2px solid #3b82f6;
      border-radius: 50%;
      z-index: 99999;
// ...
```

---

## Visual Interaction Feedback System

Visual feedback for user interactions during demo recording. These helpers enhance the viewer's understanding of what's happening on screen by providing clear visual cues for clicks, taps, swipes, and keyboard input.

### Overview

| Effect | Use Case | Default Duration |
|--------|----------|------------------|
| Click Ripple | Desktop click visualization | 600ms |
| Tap Indicator | Mobile/tablet touch feedback | 500ms |
| Swipe Trail | Swipe gesture visualization | 800ms |
| Keystroke Overlay | Keyboard shortcut display | 1500ms |

### Click Ripple Effect

Material Design-inspired ripple effect for mouse clicks.

```typescript
// demos/helpers/interaction-feedback.ts
import { Page } from '@playwright/test';

interface ClickRippleOptions {
  duration?: number;
  color?: string;
  maxRadius?: number;
}

export async function showClickRipple(
  page: Page,
  x: number,
  y: number,
  options: ClickRippleOptions = {}
): Promise<void> {
// ...
```

### Touch Tap Indicator

Pulsing circular indicator for mobile touch interactions.

```typescript
// demos/helpers/interaction-feedback.ts

interface TapIndicatorOptions {
  duration?: number;
  radius?: number;
  color?: string;
}

export async function showTapIndicator(
  page: Page,
  x: number,
  y: number,
  options: TapIndicatorOptions = {}
): Promise<void> {
  const { duration = 500, radius = 30, color = 'rgba(59, 130, 246, 0.8)' } = options;
// ...
```

### Swipe Trail Visualization

SVG-based arrow line showing swipe direction.

```typescript
// demos/helpers/interaction-feedback.ts

interface SwipeTrailOptions {
  duration?: number;
  color?: string;
  strokeWidth?: number;
  showArrow?: boolean;
}

export async function showSwipeTrail(
  page: Page,
  startX: number,
  startY: number,
  endX: number,
  endY: number,
// ...
```

### Keystroke Overlay

Badge-style display for keyboard shortcuts and key presses.

```typescript
// demos/helpers/interaction-feedback.ts

interface KeystrokeOverlayOptions {
  duration?: number;
  position?: 'top' | 'bottom';
  size?: 'small' | 'medium' | 'large';
  theme?: 'dark' | 'light';
}

const keySizes = {
  small: { fontSize: '12px', padding: '4px 8px', gap: '4px' },
  medium: { fontSize: '16px', padding: '8px 12px', gap: '8px' },
  large: { fontSize: '20px', padding: '12px 16px', gap: '10px' },
};

// ...
```

### Unified Configuration System

Enable automatic interaction feedback with a single configuration call.

```typescript
// demos/helpers/interaction-feedback.ts

interface InteractionFeedbackConfig {
  showCursor?: boolean;
  showClickRipple?: boolean;
  showTapIndicator?: boolean;
  showSwipeTrail?: boolean;
  showKeystrokeOverlay?: boolean;
  colors?: {
    cursor?: string;
    ripple?: string;
    tap?: string;
    swipe?: string;
  };
  keystrokePosition?: 'top' | 'bottom';
// ...
```

---

## Scenario Recording System

Automatic documentation of demo actions for reproducibility.

### Scenario Recorder Helper

```typescript
// demos/helpers/scenario-recorder.ts
import { Page } from '@playwright/test';

interface RecordedAction {
  timestamp: number;
  elapsed: number;
  type: 'navigate' | 'click' | 'fill' | 'select' | 'check' | 'wait' | 'overlay' | 'scroll';
  selector?: string;
  value?: string;
  description?: string;
}

interface ScenarioRecording {
  startTime: number;
  actions: RecordedAction[];
// ...
```

### Enhanced Demo Test with Recording

```typescript
// demos/specs/demo-checkout-recorded.spec.ts
import { test, expect } from '@playwright/test';
import { enableScenarioRecording, generateScenarioDoc } from '../helpers/scenario-recorder';
import { showOverlay } from '../helpers/overlay';
import fs from 'fs/promises';
import path from 'path';

test.describe('Demo: Checkout Flow (Recorded)', () => {
  test('complete checkout with auto-documentation', async ({ page }, testInfo) => {
    const recorder = await enableScenarioRecording(page);

    // === Scene 1: Product Page ===
    await page.goto('/products/sample-a');
    await page.waitForLoadState('networkidle');

// ...
```

### Wrapper Functions for Auto-Logging

```typescript
// demos/helpers/recorded-actions.ts
import { Page, Locator } from '@playwright/test';

export function createRecordedActions(page: Page) {
  return {
    async click(locator: Locator, description?: string) {
      const selector = await locator.evaluate(el => {
        // Get a readable selector
        return el.getAttribute('data-testid')
          || el.getAttribute('aria-label')
          || el.tagName.toLowerCase();
      });
      await page.evaluate(
        ({ sel, desc }) => (window as any).__recordAction?.('click', desc || `Click ${sel}`),
        { sel: selector, desc: description }
// ...
```

---

## Performance Visualization System

Real-time performance metrics overlay for demo recordings.

### Performance Overlay Helper

```typescript
// demos/helpers/performance-overlay.ts
import { Page } from '@playwright/test';

type MetricType = 'lcp' | 'cls' | 'inp' | 'fcp' | 'ttfb' | 'requests' | 'transfer' | 'dom' | 'heap';
type Position = 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';
type Theme = 'dark' | 'light' | 'transparent';
type DisplayMode = 'compact' | 'detailed';

interface PerformanceOverlayOptions {
  metrics?: MetricType[];
  position?: Position;
  theme?: Theme;
  mode?: DisplayMode;
  updateInterval?: number;
  showThresholds?: boolean;
// ...
```

### Performance Comparison Demo

Record before/after performance comparison for optimization demos.

```typescript
// demos/helpers/performance-comparison.ts
import { Page } from '@playwright/test';
import { capturePerformanceSnapshot } from './performance-overlay';

interface ComparisonResult {
  before: Record<string, number | null>;
  after: Record<string, number | null>;
  improvements: Record<string, { value: number; percentage: number }>;
}

export async function showComparisonOverlay(
  page: Page,
  before: Record<string, number | null>,
  after: Record<string, number | null>
): Promise<void> {
// ...
```

### Usage Examples

#### Basic Performance Demo

```typescript
// demos/specs/demo-performance.spec.ts
import { test, expect } from '@playwright/test';
import { enablePerformanceOverlay, disablePerformanceOverlay } from '../helpers/performance-overlay';
import { showOverlay } from '../helpers/overlay';

test.describe('Demo: Dashboard Performance', () => {
  test('show page load performance metrics', async ({ page }) => {
    // Enable overlay before navigation
    await page.goto('about:blank');
    await enablePerformanceOverlay(page, {
      metrics: ['lcp', 'cls', 'inp', 'requests', 'transfer'],
      position: 'top-right',
      theme: 'dark',
      mode: 'detailed',
    });
// ...
```

#### Before/After Comparison Demo

```typescript
// demos/specs/demo-optimization-comparison.spec.ts
import { test } from '@playwright/test';
import {
  enablePerformanceOverlay,
  capturePerformanceSnapshot,
  disablePerformanceOverlay,
} from '../helpers/performance-overlay';
import { showComparisonOverlay, hideComparisonOverlay } from '../helpers/performance-comparison';
import { showOverlay } from '../helpers/overlay';

test.describe('Demo: Performance Optimization Results', () => {
  test('compare before and after optimization', async ({ page }) => {
    // === Part 1: Before (simulate slow version) ===
    await showOverlay(page, 'Before: Original Implementation', 2000);

// ...
```

#### Network-Focused Demo

```typescript
// demos/specs/demo-api-optimization.spec.ts
import { test } from '@playwright/test';
import { enablePerformanceOverlay } from '../helpers/performance-overlay';
import { showOverlay } from '../helpers/overlay';

test.describe('Demo: API Optimization', () => {
  test('show reduced network requests', async ({ page }) => {
    await page.goto('about:blank');

    // Focus on network metrics
    await enablePerformanceOverlay(page, {
      metrics: ['requests', 'transfer', 'ttfb'],
      position: 'bottom-right',
      theme: 'transparent',
      mode: 'compact',
// ...
```

---

## Before/After Comparison Mode

Side-by-side comparison recording for improvements, redesigns, and A/B demos.

### Comparison Mode Helper

```typescript
// demos/helpers/comparison-mode.ts
import { Browser, BrowserContext, Page } from '@playwright/test';
import { capturePerformanceSnapshot } from './performance-overlay';

type ComparisonLayout = 'split' | 'pip' | 'sequential';
type PipPosition = 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right';

interface ComparisonOptions {
  layout: ComparisonLayout;
  beforeUrl: string;
  afterUrl: string;
  labels?: {
    before?: string;
    after?: string;
  };
// ...
```

### Split Screen Divider Overlay

```typescript
// demos/helpers/split-divider.ts
import { Page } from '@playwright/test';

interface DividerOptions {
  color?: string;
  width?: number;
  showDragHandle?: boolean;
}

export async function addSplitDivider(
  page: Page,
  options: DividerOptions = {}
): Promise<void> {
  const { color = 'rgba(255, 255, 255, 0.3)', width = 2, showDragHandle = false } = options;

// ...
```

### Sequential Transition Helper

```typescript
// demos/helpers/transition-effects.ts
import { Page } from '@playwright/test';

type TransitionType = 'wipe' | 'fade' | 'slide' | 'zoom';
type Direction = 'left' | 'right' | 'up' | 'down';

interface TransitionOptions {
  type?: TransitionType;
  direction?: Direction;
  duration?: number;
  showLabel?: boolean;
  label?: string;
}

export async function showTransitionOverlay(
// ...
```

### Usage Examples

#### Split Screen Comparison Demo

```typescript
// demos/specs/demo-split-comparison.spec.ts
import { test } from '@playwright/test';
import { createComparisonDemo } from '../helpers/comparison-mode';
import { showOverlay } from '../helpers/overlay';

test.describe('Demo: UI Redesign Comparison', () => {
  test('split screen before/after', async ({ browser }) => {
    const comparison = await createComparisonDemo(browser, {
      layout: 'split',
      beforeUrl: '/dashboard?theme=legacy',
      afterUrl: '/dashboard?theme=modern',
      labels: { before: 'Current Design', after: 'New Design' },
      showMetrics: true,
    });

// ...
```

#### Sequential Transition Demo

```typescript
// demos/specs/demo-sequential-comparison.spec.ts
import { test } from '@playwright/test';
import { showTransitionOverlay } from '../helpers/transition-effects';
import { showOverlay } from '../helpers/overlay';
import { enablePerformanceOverlay, disablePerformanceOverlay } from '../helpers/performance-overlay';

test.describe('Demo: Performance Improvement', () => {
  test('before then after with transition', async ({ page }) => {
    // === Before ===
    await showOverlay(page, 'Before: Original Implementation', 2000);

    await enablePerformanceOverlay(page, {
      metrics: ['lcp', 'requests', 'transfer'],
      position: 'top-right',
    });
// ...
```

#### A/B Test Variant Demo

```typescript
// demos/specs/demo-ab-test.spec.ts
import { test } from '@playwright/test';
import { createComparisonDemo } from '../helpers/comparison-mode';

test.describe('Demo: A/B Test Variants', () => {
  test('compare checkout flow variants', async ({ browser }) => {
    const comparison = await createComparisonDemo(browser, {
      layout: 'split',
      beforeUrl: '/checkout?variant=control',
      afterUrl: '/checkout?variant=streamlined',
      labels: { before: 'Control', after: 'Variant B' },
      showMetrics: false,
    });

    // Synchronized checkout flow
// ...
```

---

## AI Narration System

Automatic voice narration generation for demo videos using TTS APIs.

### Narration Script Generator

```typescript
// demos/helpers/narration-script.ts
import { RecordedAction } from './scenario-recorder';

interface NarrationSegment {
  time: number;       // Start time in ms
  duration?: number;  // Optional duration
  text: string;       // Narration text
  pause?: number;     // Pause after segment in ms
}

type NarrationStyle = 'tutorial' | 'marketing' | 'technical' | 'conversational';
type NarrationPace = 'slow' | 'moderate' | 'fast';
type NarrationPersonality = 'friendly' | 'professional' | 'enthusiastic' | 'neutral';

interface ScriptGeneratorOptions {
// ...
```

### Web Speech API (Browser Built-in TTS)

Free, no API key required. Uses browser's built-in speech synthesis.

```typescript
// demos/helpers/web-speech-tts.ts
import { Page } from '@playwright/test';
import { NarrationSegment } from './narration-script';
import fs from 'fs/promises';
import path from 'path';

interface WebSpeechOptions {
  voice?: string;        // Voice name (e.g., 'Google US English', 'Samantha')
  lang?: string;         // Language code (e.g., 'en-US', 'ja-JP')
  rate?: number;         // Speech rate 0.1-10 (default: 1)
  pitch?: number;        // Pitch 0-2 (default: 1)
  volume?: number;       // Volume 0-1 (default: 1)
}

interface WebSpeechNarrationOptions extends WebSpeechOptions {
// ...
```

### Real-Time Narration Demo Example

```typescript
// demos/specs/demo-with-live-narration.spec.ts
import { test } from '@playwright/test';
import { speakAndWait, getAvailableVoices } from '../helpers/web-speech-tts';
import { showOverlay } from '../helpers/overlay';

test.describe('Demo: Live Narration with Web Speech API', () => {
  test.beforeAll(async ({ browser }) => {
    // List available voices (for debugging)
    const page = await browser.newPage();
    const voices = await getAvailableVoices(page);
    console.log('Available voices:', voices.slice(0, 10));
    await page.close();
  });

  test('dashboard demo with live narration', async ({ page }) => {
// ...
```

### Playwright Config for Audio Capture

```typescript
// playwright.config.narration.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './demos/specs',
  timeout: 180000,
  retries: 0,
  workers: 1,

  use: {
    // Enable audio for Web Speech API
    launchOptions: {
      args: [
        '--autoplay-policy=no-user-gesture-required',
        '--enable-speech-dispatcher',
// ...
```

### Voice Selection Helper

```typescript
// demos/helpers/voice-selector.ts
import { Page } from '@playwright/test';

interface VoiceInfo {
  name: string;
  lang: string;
  localService: boolean;
  default: boolean;
}

// Recommended voices by platform and language
export const recommendedVoices = {
  'en-US': {
    mac: ['Samantha', 'Alex', 'Karen'],
    windows: ['Microsoft David', 'Microsoft Zira'],
// ...
```

### Usage: Simple Narrated Demo

```typescript
// demos/specs/demo-simple-narration.spec.ts
import { test } from '@playwright/test';
import { createNarratedDemo } from '../helpers/voice-selector';

test('simple narrated demo', async ({ page }) => {
  const narrator = await createNarratedDemo(page, 'en-US');

  await page.goto('/');
  await narrator.speak('Welcome to our application.');

  await page.getByRole('link', { name: 'Features' }).click();
  await narrator.speak('Here are our key features.');

  await page.waitForTimeout(2000);
  await narrator.speak('Thank you for watching!');
// ...
```

---

## Progress Bar Helper

Display demo progress at the top or bottom of the screen with step-based or percentage-based modes.

```typescript
// demos/helpers/progress-bar.ts
import { Page } from '@playwright/test';

interface ProgressBarOptions {
  position?: 'top' | 'bottom';
  mode?: 'steps' | 'percentage' | 'timed';
  steps?: number;
  duration?: number;  // for timed mode (ms)
  color?: string;
  backgroundColor?: string;
  height?: number;
  showLabel?: boolean;
}

export async function showProgressBar(
// ...
```

---

## Spotlight Effect Helper

Highlight specific UI elements by darkening the surrounding area with SVG mask technique.

```typescript
// demos/helpers/spotlight.ts
import { Page } from '@playwright/test';

interface SpotlightOptions {
  padding?: number;
  opacity?: number;
  color?: string;
  label?: string;
  labelPosition?: 'top' | 'bottom' | 'left' | 'right';
  borderRadius?: number;
  animated?: boolean;
}

export async function spotlight(
  page: Page,
// ...
```

---

## Combined Usage: Progress Bar + Spotlight

Example demonstrating both visual effects working together for a guided tour demo.

```typescript
// demos/specs/demo-onboarding.spec.ts
import { test } from '@playwright/test';
import { showProgressBar, updateProgress, hideProgressBar } from '../helpers/progress-bar';
import { spotlight, clearSpotlight, moveSpotlight } from '../helpers/spotlight';

test.describe('Demo: Onboarding Flow', () => {
  test('guided tour with progress and spotlight', async ({ page }) => {
    // Initialize progress bar
    await showProgressBar(page, { position: 'top', steps: 4 });

    await page.goto('/dashboard');
    await updateProgress(page, 1, 'Welcome');

    // Spotlight: Navigation menu
    await spotlight(page, '[data-testid="nav-menu"]', {
// ...
```

---

### Device-Specific Presets

Pre-configured settings for common demo scenarios.

```typescript
// demos/helpers/interaction-presets.ts
import { Page } from '@playwright/test';
import { enableInteractionFeedback, InteractionFeedbackConfig } from './interaction-feedback';

export const InteractionPresets: Record<string, InteractionFeedbackConfig> = {
  desktop: {
    showCursor: true,
    showClickRipple: true,
    showTapIndicator: false,
    showSwipeTrail: false,
    showKeystrokeOverlay: true,
    keystrokePosition: 'bottom',
  },
  mobile: {
    showCursor: false,
// ...
```

### Usage Examples

#### Desktop Demo Example

```typescript
// demos/specs/demo-desktop-workflow.spec.ts
import { test, expect } from '@playwright/test';
import { enableDesktopFeedback, disableInteractionFeedback } from '../helpers/interaction-presets';
import { showOverlay } from '../helpers/overlay';

test.describe('Demo: Desktop Workflow with Visual Feedback', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/dashboard');
    await enableDesktopFeedback(page);
  });

  test.afterEach(async ({ page }) => {
    await disableInteractionFeedback(page);
  });

// ...
```

#### Mobile Demo Example

```typescript
// demos/specs/demo-mobile-gestures.spec.ts
import { test, expect, devices } from '@playwright/test';
import { enableMobileFeedback, disableInteractionFeedback } from '../helpers/interaction-presets';
import { showSwipeTrail, showTapIndicator } from '../helpers/interaction-feedback';
import { showOverlay } from '../helpers/overlay';

test.describe('Demo: Mobile App with Touch Feedback', () => {
  test.use({ ...devices['iPhone 14 Pro'] });

  test.beforeEach(async ({ page }) => {
    await page.goto('/mobile/gallery');
    await enableMobileFeedback(page);
  });

  test.afterEach(async ({ page }) => {
// ...
```

---

## Page Transition Wait Pattern

### Stable Transition Wait

```typescript
// demos/helpers/navigation.ts
import { Page, expect } from '@playwright/test';

export async function waitForPageReady(page: Page): Promise<void> {
  // DOM load complete
  await page.waitForLoadState('domcontentloaded');
  // Network idle
  await page.waitForLoadState('networkidle');
  // Additional stabilization wait
  await page.waitForTimeout(300);
}

export async function navigateAndWait(
  page: Page,
  action: () => Promise<void>,
// ...
```

---

## Test Data Factory

### Preparing Demo Data

```typescript
// demos/helpers/data.ts
export const DemoData = {
  user: {
    email: 'demo@example.com',
    password: 'DemoPass123',
    name: 'Demo User',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Demo',
  },

  address: {
    postalCode: '150-0001',
    country: 'Japan',
    city: 'Tokyo',
    street: '1-2-3 Shibuya',
    building: 'Demo Building 101',
// ...
```

---

## Persona-Aware Demo Recording

### Echo Integration Patterns

When Echo provides persona behavior profiles, use these patterns to create believable persona-specific demos.

#### Persona Configuration Helper

```typescript
// demos/helpers/persona.ts
import { Page } from '@playwright/test';

export interface PersonaBehavior {
  name: string;
  slowMo: number;
  readingMultiplier: number;
  hesitationPoints: string[];
  hesitationDuration: number;
  overlayDuration: number;
  typingSpeed: 'fast' | 'normal' | 'slow' | 'hunt-and-peck';
}

export const PersonaBehaviors: Record<string, PersonaBehavior> = {
  senior: {
// ...
```

#### Persona-Aware Wait Helper

```typescript
// demos/helpers/persona-wait.ts
import { Page } from '@playwright/test';
import { PersonaBehavior, getPersona } from './persona';

export async function personaWait(
  page: Page,
  baseTime: number,
  persona?: PersonaBehavior
): Promise<void> {
  const p = persona || getPersona();
  const adjustedTime = Math.round(baseTime * p.readingMultiplier);
  await page.waitForTimeout(adjustedTime);
}

export async function hesitate(
// ...
```

#### Persona-Aware Typing Helper

```typescript
// demos/helpers/persona-typing.ts
import { Page } from '@playwright/test';
import { PersonaBehavior, getPersona } from './persona';

const typingSpeeds = {
  fast: 30,
  normal: 60,
  slow: 120,
  'hunt-and-peck': 250,
};

export async function personaFill(
  page: Page,
  selector: string,
  value: string,
// ...
```

### Persona Demo Test Example

```typescript
// demos/specs/demo-checkout-persona.spec.ts
import { test, expect } from '@playwright/test';
import { getPersona, PersonaBehavior } from '../helpers/persona';
import { hesitate, personaWait, showPersonaOverlay } from '../helpers/persona-wait';
import { personaFillByLabel } from '../helpers/persona-typing';
import { DemoData } from '../helpers/data';

test.describe('Demo: Checkout Flow (Persona-Aware)', () => {
  let persona: PersonaBehavior;

  test.beforeAll(() => {
    // Get persona from environment: DEMO_PERSONA=senior npx playwright test
    persona = getPersona(process.env.DEMO_PERSONA);
    console.log(`Recording demo for persona: ${persona.name}`);
  });
// ...
```

### Playwright Config for Persona Demos

```typescript
// playwright.config.persona.ts
import { defineConfig, devices } from '@playwright/test';
import { PersonaBehaviors } from './demos/helpers/persona';

// Get persona from environment
const personaName = process.env.DEMO_PERSONA || 'newbie';
const persona = PersonaBehaviors[personaName.toLowerCase()];

export default defineConfig({
  testDir: './demos/specs',
  timeout: 180000, // 3 minutes for slow personas
  retries: 0,
  workers: 1,

  use: {
// ...
```

### Running Persona Demos

```bash
# Record demo for different personas
DEMO_PERSONA=senior npx playwright test --config=playwright.config.persona.ts
DEMO_PERSONA=newbie npx playwright test --config=playwright.config.persona.ts
DEMO_PERSONA=powerUser npx playwright test --config=playwright.config.persona.ts

# Output files will be in:
# demos/output/senior/
# demos/output/newbie/
# demos/output/poweruser/
```

---

## ARIA Snapshot Validation

Validate accessibility tree at key demo moments to ensure demos showcase accessible UI.

### Basic ARIA Validation in Demo

```typescript
// demos/helpers/aria-validation.ts
import { Page, expect, Locator } from '@playwright/test';

/**
 * Validate accessibility structure at a key demo moment.
 * Use sparingly — at scene transitions or result screens.
 */
export async function validateAriaAt(
  locator: Locator,
  expectedSnapshot: string
): Promise<void> {
  await expect(locator).toMatchAriaSnapshot(expectedSnapshot);
}
```

### Usage in Demo Test

```typescript
import { test, expect } from '@playwright/test';

test('dashboard demo with a11y validation', async ({ page }) => {
  await test.step('Scene: Dashboard loaded', async () => {
    await page.goto('/dashboard');
    await expect(page.getByRole('main')).toBeVisible();

    // Validate key navigation structure is accessible
    await expect(page.getByRole('navigation')).toMatchAriaSnapshot(`
      - navigation:
        - link "Home"
        - link "Settings"
        - link "Profile"
    `);
  });

  await test.step('Scene: Data table', async () => {
    await page.getByRole('link', { name: 'Reports' }).click();
    await expect(page.getByRole('table')).toBeVisible();

    // Validate table has proper headers
    await expect(page.getByRole('table')).toMatchAriaSnapshot(`
      - table:
        - rowgroup:
          - row:
            - columnheader "Date"
            - columnheader "Revenue"
            - columnheader "Status"
    `);
  });
});
```

### When to Use ARIA Validation in Demos

| Scenario | Use ARIA? | Reason |
|----------|-----------|--------|
| Navigation structure | Yes | Core a11y landmark |
| Form inputs | Yes | Label association critical |
| Data tables | Yes | Header structure matters |
| Decorative elements | No | Not semantically important |
| Animations/transitions | No | Visual-only concerns |

---

## Complete Demo Example

### E-Commerce Checkout Demo

```typescript
// demos/specs/demo-checkout.spec.ts
import { test, expect } from '@playwright/test';
import { showOverlay, showStep, showSuccess } from '../helpers/overlay';
import { smoothScrollTo } from '../helpers/scroll';
import { DemoData, seedDemoData } from '../helpers/data';

test.describe('Demo: Product Purchase Flow', () => {
  test.beforeEach(async ({ page, context }) => {
    // Login via API
    await context.request.post('/api/auth/login', {
      data: { email: DemoData.user.email, password: DemoData.user.password },
    });
    await seedDemoData(page);
  });

// ...
```
