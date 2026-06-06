# Mobile Emulation

Reference for Vector's `mobile` recipe. Covers device descriptors, viewport / UA / touch / geolocation / timezone configuration, network throttling, iOS Safari / Android Chrome divergence, and validation patterns.

> **Emulation is not equivalent to a real device.** Camera, biometrics, push notifications, WebGL precision, and battery-related behaviors require real-device testing or BrowserStack / Sauce Labs Real Device Cloud.

---

## 1. Built-in Device Descriptors

Playwright ships with `devices` from `@playwright/test`:

```js
import { devices } from '@playwright/test';

const context = await browser.newContext({
  ...devices['iPhone 15 Pro'],
});
```

### Common descriptors
- `iPhone 15 Pro`, `iPhone 15`, `iPhone 14 Pro Max`, `iPhone SE`
- `Pixel 8`, `Pixel 7`, `Pixel 5`
- `Galaxy S9+`, `Galaxy Tab S4`
- `iPad Pro 11`, `iPad Mini`

### What a descriptor sets
- `viewport`: `{ width, height }` (CSS pixels)
- `userAgent`: device-matching UA
- `deviceScaleFactor`: 2-3 (DPR)
- `isMobile`: true (enables touch)
- `hasTouch`: true
- `defaultBrowserType`: typically `webkit` for iOS, `chromium` for Android

### Reality check
- iOS descriptors run on Chromium/WebKit Playwright build, not real iOS Safari
- Real iOS Safari WebKit features (e.g., backdrop-filter quirks, `-webkit-fill-available`, viewport units handling) may differ
- For true iOS testing: BrowserStack, Sauce Labs, or local Xcode Simulator

---

## 2. Custom Mobile Context

When built-in descriptor doesn't fit:

```js
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },         // iPhone 15 logical
  deviceScaleFactor: 3,
  isMobile: true,
  hasTouch: true,
  userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_2 like Mac OS X) ' +
             'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Mobile/15E148 Safari/604.1',
  locale: 'ja-JP',
  timezoneId: 'Asia/Tokyo',
  geolocation: { latitude: 35.6762, longitude: 139.6503 },
  permissions: ['geolocation'],
  colorScheme: 'dark',  // OS dark mode
  reducedMotion: 'reduce',  // accessibility setting
});
```

---

## 3. Touch Gestures

### Tap (single)
```js
await page.getByRole('button', { name: 'Submit' }).tap();
```

### Long press
```js
const el = page.getByTestId('item');
const box = await el.boundingBox();
await page.touchscreen.tap(box.x + box.width / 2, box.y + box.height / 2);
await page.waitForTimeout(800);
```

### Swipe (horizontal)
```js
async function swipe(page, fromX, fromY, toX, toY, durationMs = 300) {
  await page.touchscreen.tap(fromX, fromY);  // initiate touch
  const steps = 20;
  for (let i = 1; i <= steps; i++) {
    const x = fromX + (toX - fromX) * (i / steps);
    const y = fromY + (toY - fromY) * (i / steps);
    await page.touchscreen.tap(x, y);
    await page.waitForTimeout(durationMs / steps);
  }
}
// Note: Playwright lacks native swipe API; use page.touchscreen primitives or evaluate TouchEvents
```

### Pinch zoom (use evaluate)
```js
await page.evaluate(() => {
  const el = document.querySelector('#zoomable');
  el.dispatchEvent(new TouchEvent('touchstart', { /* multi-touch points */ }));
  // Build TouchEvent with two changedTouches at varying distances
});
```

---

## 4. Network Throttling

### Profiles (CDP-based)
```js
const client = await context.newCDPSession(page);
await client.send('Network.enable');

// Slow 3G
await client.send('Network.emulateNetworkConditions', {
  offline: false,
  downloadThroughput: 50 * 1024 / 8,    // 50 Kbps
  uploadThroughput: 20 * 1024 / 8,
  latency: 2000,                         // 2000ms RTT
});

// Fast 3G
await client.send('Network.emulateNetworkConditions', {
  offline: false,
  downloadThroughput: 1.5 * 1024 * 1024 / 8,   // 1.5 Mbps
  uploadThroughput: 750 * 1024 / 8,
  latency: 562.5,
});

// 4G
await client.send('Network.emulateNetworkConditions', {
  offline: false,
  downloadThroughput: 4 * 1024 * 1024 / 8,
  uploadThroughput: 3 * 1024 * 1024 / 8,
  latency: 170,
});

// Offline
await client.send('Network.emulateNetworkConditions', {
  offline: true, downloadThroughput: 0, uploadThroughput: 0, latency: 0,
});
```

### CPU throttling
```js
await client.send('Emulation.setCPUThrottlingRate', { rate: 4 });  // 4x slower
```

### Use case
- Performance budget validation under low-end mobile conditions
- Testing offline-first behaviors
- Reproducing user-reported slowness on 3G networks

---

## 5. iOS Safari vs Android Chrome Divergence

| Concern | iOS Safari | Android Chrome | Mitigation |
|---|---|---|---|
| `100vh` includes URL bar | Yes (jumps when scrolling) | No | Use `100dvh` (dynamic viewport) |
| `position: sticky` | Sometimes broken in scroll containers | Works | Test both; fallback to JS scroll listener |
| `backdrop-filter` | Spotty older iOS | Works | Provide solid fallback |
| Smooth scroll inertia | Native momentum | Less momentum | `-webkit-overflow-scrolling: touch` (legacy) |
| Date input | Native picker, no styling | Some styling | Custom date picker for cross-platform parity |
| File input camera capture | `<input type="file" accept="image/*" capture="environment">` | Same | Test on real device |
| Push notifications | Limited (PWA from iOS 16.4 only on home-screen apps) | Full | Document limitation |
| WebGL extensions | Subset of Android | Most extensions | Feature-detect each |
| Hover state on tap | Yes (sticky) | No | Disable `:hover` styles for touch via media query |
| Audio autoplay | Blocked without gesture | Mostly blocked | User-gesture-gated audio init |
| Vibration API | Not supported | Supported | Feature-detect |
| `position: fixed` + virtual keyboard | Element pushed up, often clipped | Better behavior | Use `visualViewport` API |
| Form autofill UI | Yellow background highlight | None | Document expected behavior |

### Hover detection for touch devices
```css
@media (hover: hover) and (pointer: fine) {
  .button:hover { background: var(--hover); }
}
```

---

## 6. Touch Target Validation

### Minimum sizes
- iOS HIG: **≥ 44 × 44 pt**
- Material Design: **≥ 48 × 48 dp**
- WCAG 2.5.5 (AAA): **≥ 44 × 44 px**, with 8px minimum spacing

### Programmatic validation
```js
const buttons = page.locator('button, a, [role="button"], input[type="submit"]');
const undersized = await buttons.evaluateAll(els =>
  els.filter(el => {
    const r = el.getBoundingClientRect();
    return (r.width < 44 || r.height < 44);
  }).map(el => ({
    tag: el.tagName,
    text: el.textContent?.trim().slice(0, 30),
    size: `${el.getBoundingClientRect().width}x${el.getBoundingClientRect().height}`,
  }))
);
console.log('Undersized targets:', undersized);
```

### Spacing check
```js
// Check 8px minimum gap between adjacent tappable elements
const gaps = await page.evaluate(() => {
  const elements = [...document.querySelectorAll('button, a')];
  const issues = [];
  for (let i = 0; i < elements.length; i++) {
    for (let j = i + 1; j < elements.length; j++) {
      const a = elements[i].getBoundingClientRect();
      const b = elements[j].getBoundingClientRect();
      const gapX = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
      const gapY = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
      if (gapX > 0 && gapY > 0 && gapX < 8 && gapY < 8) {
        issues.push({ a: elements[i].textContent?.slice(0, 20), b: elements[j].textContent?.slice(0, 20) });
      }
    }
  }
  return issues;
});
```

---

## 7. Mobile-Specific Test Patterns

### Orientation change
```js
const portrait = await browser.newContext({ ...devices['iPhone 15 Pro'] });
const landscape = await browser.newContext({ ...devices['iPhone 15 Pro landscape'] });
```

### Safe area insets (notched devices)
```css
.app {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
}
```
Validate visually with screenshot — Playwright honors safe-area insets in context.

### Virtual keyboard
- iOS: fixed/sticky elements may clip when keyboard opens
- Use `visualViewport.height` to compute keyboard-aware layout
- Test by focusing an input → screenshot to confirm critical UI remains visible

### Pull-to-refresh
- iOS Safari and Android Chrome both have native PTR
- To suppress in PWA: `overscroll-behavior-y: contain`

---

## 8. What Emulation Cannot Test

| Feature | Why emulation fails | Real-device required |
|---|---|---|
| Camera / biometrics | No hardware emulation | Yes |
| Push notifications | Requires device APNs/FCM | Yes |
| WebGL precision | Desktop GPU vs mobile GPU differs | Recommended |
| Battery API behaviors | No power source emulation | Yes |
| Performance under thermal throttling | No thermal model | Yes |
| Real iOS WebKit quirks | Playwright WebKit is not iOS Safari | Yes |
| Carrier-specific features (RCS, MMS) | No carrier emulation | Yes |
| Gestures with edge swipes (back gesture) | OS-level gesture | Yes |

For these: use BrowserStack Real Device, Sauce Labs Real Devices, or local hardware via WebDriver Agent (iOS) / ADB (Android).

---

## 9. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Testing only desktop UA, assuming responsive CSS works | Always run mobile profile in CI |
| Forgetting `hasTouch: true` → hover styles fire | Use built-in device descriptor |
| Using `vh` units → URL bar jumps on iOS | Switch to `dvh` / `svh` / `lvh` |
| 44px touch target unverified | Programmatic validation in CI |
| Network throttling forgotten → 4G assumption | Throttle to Slow 3G in perf tests |
| Geolocation permission unset | Pass `permissions: ['geolocation']` |
| `position: fixed` element disappears with keyboard | Test focus + screenshot |
| Device pixel ratio 1 used → blurry screenshots | Set `deviceScaleFactor: 2-3` |
| Emulating "iOS Safari" via Chrome UA → false confidence | Document gap, recommend real-device for risk paths |

---

## 10. Decision Walkthrough Template

```
Target device: ____________________
Built-in descriptor: __________ (or "custom")
Viewport: ___ x ___
DPR: ___
Locale: ____ Timezone: ____ ColorScheme: ____

Network throttling: Slow3G / Fast3G / 4G / unmetered
CPU throttling: 1x / 4x / 6x

Touch tests required:
  □ Tap targets ≥ 44px
  □ Spacing ≥ 8px
  □ Swipe gestures
  □ Long press

Cross-OS divergence checks:
  □ 100vh / 100dvh handling
  □ position: sticky in scroll containers
  □ Hover-only desktop interactions have mobile fallback
  □ Audio/video autoplay gated by user gesture
  □ Virtual keyboard does not obscure critical UI

Real-device fallback needed for:
  □ Camera / file capture
  □ Push notifications
  □ WebGL-heavy 3D
  □ Biometrics / WebAuthn
```

---

## 11. References
- Playwright `devices` source (built-in descriptors)
- Apple iOS Human Interface Guidelines (touch targets)
- Material Design spec (touch targets, gestures)
- WCAG 2.5.5 Target Size (AAA)
- CDP `Network.emulateNetworkConditions` and `Emulation.setCPUThrottlingRate`
- BrowserStack / Sauce Labs Real Device Cloud (when emulation is insufficient)
