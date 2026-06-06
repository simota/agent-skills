# Stealth Mode (Anti-Detection within ToS-Compliant Boundaries)

Reference for Vector's `stealth` recipe. Covers TLS / JA3 / JA4 fingerprinting, behavioral humanization, residential proxy rotation, and major anti-bot system handling (Cloudflare, Akamai, PerimeterX, DataDome).

> **Authorization Gate**: Stealth mode is for legitimate research, accessibility-tool building, or monitoring of services where automation is permitted. Refuse to apply stealth techniques when (a) target ToS prohibits automation, (b) intent is bypassing rate limits / paywall / CAPTCHA, or (c) the user cannot articulate authorization. ToS verification is mandatory before deployment.

---

## 1. Authorization Checklist (Required before applying any stealth technique)

| Check | Requirement |
|---|---|
| ToS reviewed | Read site ToS / robots.txt / opt-out signals |
| Automation permitted? | Explicit allow / silent on automation / explicit deny |
| Use case justification | Research / accessibility / monitoring / authorized pentesting |
| Rate-limit respect | Stay within published limits (or much below if undocumented) |
| Personal data scope | None / aggregate-only / authorized PII handling |
| User authority | User has the right to operate against this domain |

**Refuse** when ToS deny is explicit OR user cannot articulate authorization. Document refusal in `.vector/refusal-log.md`.

---

## 2. Fingerprinting Surfaces

### TLS Fingerprinting (JA3 / JA4)
- Modern anti-bot systems (Cloudflare Bot Management, Akamai Bot Manager, F5 Distributed Cloud) hash TLS ClientHello: cipher order, extensions, supported groups, signature algorithms.
- **Headless Chromium TLS fingerprint differs from real Chrome** — even with custom UA, JA4 reveals automation.
- Mitigation: `curl-impersonate`, `tls-client` (Go), `playwright-extra` with stealth plugin, or run via real Chrome binary (not headless-shell).

### HTTP/2 Fingerprinting (Akamai HTTP/2 fingerprint)
- Frame ordering, settings frame parameters, window updates, header pseudo-header order
- Less commonly fingerprinted but some sophisticated systems (Akamai Bot Manager Premium) use it.

### Browser fingerprinting (canvas, WebGL, fonts, audio context)
- Site-side JS reads:
  - `navigator.webdriver` (must be `false`)
  - `navigator.plugins`, `navigator.languages`, `navigator.platform`
  - WebGL renderer/vendor strings (`UNMASKED_VENDOR_WEBGL`)
  - Canvas-rendered text hashes
  - AudioContext fingerprint
  - Font enumeration via measureText
- Mitigation: `playwright-extra` + `puppeteer-extra-plugin-stealth` patches most of these.

### Behavioral fingerprinting
- Mouse trajectory (straight line vs Bézier curve)
- Click dwell time (50-150ms human; 0-10ms bot)
- Scroll pattern (smooth inertia vs jump)
- Keystroke cadence (variance)
- Time-of-day patterns (24/7 = bot)

---

## 3. Behavioral Humanization

### Mouse movement
```js
async function humanMove(page, fromX, fromY, toX, toY, steps = 25) {
  const cp1 = { x: fromX + (toX - fromX) * (0.3 + Math.random() * 0.2),
                y: fromY + (toY - fromY) * (0.3 + Math.random() * 0.2) + 50 * (Math.random() - 0.5) };
  const cp2 = { x: fromX + (toX - fromX) * (0.6 + Math.random() * 0.2),
                y: fromY + (toY - fromY) * (0.6 + Math.random() * 0.2) - 30 * (Math.random() - 0.5) };
  for (let i = 0; i <= steps; i++) {
    const t = i / steps;
    const x = (1 - t) ** 3 * fromX + 3 * (1 - t) ** 2 * t * cp1.x + 3 * (1 - t) * t ** 2 * cp2.x + t ** 3 * toX;
    const y = (1 - t) ** 3 * fromY + 3 * (1 - t) ** 2 * t * cp1.y + 3 * (1 - t) * t ** 2 * cp2.y + t ** 3 * toY;
    await page.mouse.move(x, y);
    await new Promise(r => setTimeout(r, 8 + Math.random() * 12));
  }
}
```

### Dwell time (between hover and click)
```js
async function humanClick(page, selector) {
  await page.locator(selector).hover();
  await page.waitForTimeout(80 + Math.random() * 120);
  await page.locator(selector).click();
}
```

### Jittered request delay (replace fixed sleep)
```js
function jitter(baseMs, variancePercent = 30) {
  const delta = baseMs * variancePercent / 100;
  return baseMs + (Math.random() * 2 - 1) * delta;
}
await page.waitForTimeout(jitter(2000, 40));  // 1200-2800ms
```

### Scroll humanization
```js
async function humanScroll(page, totalY) {
  const chunks = 8 + Math.floor(Math.random() * 5);
  for (let i = 0; i < chunks; i++) {
    await page.mouse.wheel(0, totalY / chunks);
    await page.waitForTimeout(40 + Math.random() * 80);
  }
}
```

---

## 4. Residential Proxy Rotation

### Proxy types (in order of detection difficulty)

| Type | Cost | Detection by sophisticated systems |
|---|---|---|
| Datacenter (AWS/GCP/DO IPs) | $ | Trivial — IP reputation databases flag instantly |
| ISP / static residential | $$ | Moderate — clean but reused across customers |
| Rotating residential | $$$ | Hard — real consumer IPs, geo-distributed |
| Mobile (4G/5G NAT) | $$$$ | Hardest — millions of users behind same IP |

### Rotation strategies
- **Per-request** (highest stealth, breaks session continuity — only for stateless reads)
- **Per-session** (one IP per browser context — preferred for logged-in flows)
- **Sticky** (same IP for N minutes, then rotate — middle ground)

### Geo-matching
- IP geo should match: target language, timezone (`Intl.DateTimeFormat().resolvedOptions().timeZone`), `navigator.language`, currency in cookies
- Mismatch (US IP + JST timezone + English UA) = automation signal

### Provider integration (example for Bright Data / Oxylabs)
```js
const browser = await chromium.launch({
  proxy: {
    server: 'http://brd.superproxy.io:33335',
    username: `brd-customer-${id}-zone-${zone}-session-${Math.random().toString(36).slice(2)}`,
    password: process.env.BRIGHTDATA_PASS,
  },
});
```

---

## 5. Anti-Bot System Handling

### Cloudflare (Turnstile, Bot Management)
- JS challenge: requires real JS execution + correct TLS fingerprint
- Turnstile (replacing reCAPTCHA): non-interactive widget, resolves via real browser + clean fingerprint
- 5-second JS check ("Checking your browser..."): handled by waiting `page.waitForLoadState('networkidle')`
- Bot Management score: aggregated from TLS + HTTP/2 + JS challenges + behavior — single signal failure tanks score
- **Bypass services**: FlareSolverr, ZenRows — use only with authorization

### Akamai Bot Manager
- Sensor data: collected via `/akam/11/...` POST with encoded device telemetry
- Sec-CH-UA client hints must be consistent (Chrome version + platform must align)
- Mouse + keyboard event ratio analyzed
- Mitigation: `playwright-extra-stealth` + behavioral humanization + residential IP

### PerimeterX / HUMAN
- Heavy canvas + WebGL fingerprinting
- Px sensor cookie required for subsequent requests
- Mitigation: full Chrome (not headless-shell), `playwright-extra-stealth`

### DataDome
- IP reputation + behavioral + JS challenge
- DataDome cookie required after CAPTCHA solve
- Mitigation: residential proxy + CAPTCHA-solver service for logged-in flows (with authorization)

### CAPTCHA solver (only with authorization)
- 2Captcha, Anti-Captcha, CapMonster Cloud
- $0.5-3 per solve depending on type
- **Never use to bypass anti-fraud** — only for accessibility (vision-impaired user proxy) or authorized testing

---

## 6. Playwright Stealth Setup

### Recommended stack
```bash
npm i -D playwright playwright-extra puppeteer-extra-plugin-stealth
```

```js
import { chromium } from 'playwright-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';

chromium.use(StealthPlugin());

const browser = await chromium.launch({
  headless: 'new',  // or false for debugging
  args: [
    '--disable-blink-features=AutomationControlled',
    '--disable-features=IsolateOrigins,site-per-process',
  ],
});

const context = await browser.newContext({
  viewport: { width: 1920, height: 1080 },
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
  locale: 'ja-JP',
  timezoneId: 'Asia/Tokyo',
  permissions: ['geolocation'],
  geolocation: { latitude: 35.6762, longitude: 139.6503 },
});
```

### Patches that StealthPlugin handles
- `navigator.webdriver` → `false`
- WebGL vendor strings
- Chrome runtime
- Permissions API mock
- iframe contentWindow
- Plugin/MimeTypes consistency
- Notification.permission default

---

## 7. Detection Self-Test

Before deploying to production, validate stealth:
- Run against `https://bot.sannysoft.com/` — most checks should be green
- Run against `https://abrahamjuliot.github.io/creepjs/` — score should be in human range
- Use `intoli.com/blog/not-possible-to-block-chrome-headless` as historical reference

---

## 8. Common Pitfalls

| Pitfall | Detection | Avoidance |
|---|---|---|
| Headless-shell binary | Trivial — `HeadlessChrome` in UA, missing fonts | Use full Chromium with `headless: 'new'` |
| Datacenter IP | IP reputation database hit | Residential proxy with geo-match |
| `navigator.webdriver = true` | One-line JS check | StealthPlugin or manual override |
| Fixed-interval requests | Behavioral fingerprint | Jitter (20-50% variance) |
| Same User-Agent across 10K requests | Bot signal | Rotate per session within sane Chrome version range |
| UA lying about version (Chrome 131 with Chrome 119 features) | Mismatch detection | Match UA to actual binary version |
| 24/7 traffic | Behavioral pattern | Schedule active-hours only if mimicking human |
| No referrer | Direct-bot signal | Set realistic referrer chain |
| Identical cookie state across IPs | Account-sharing detection | One context per identity |
| Missing client hints (Sec-CH-UA) | Older bot signature | Modern Playwright handles automatically |

---

## 9. Decision Walkthrough Template

```
Target: ____________________
ToS check: allowed / silent / denied
robots.txt: allowed / denied
Authorization: ___________ (research / accessibility / monitoring / pentesting / OTHER → REFUSE)

Anti-bot detected: Cloudflare / Akamai / PerimeterX / DataDome / Custom / None
Bot score self-test: ___ / 100 (creepjs)

Mitigation stack:
  □ playwright-extra + StealthPlugin
  □ Full Chromium (not headless-shell)
  □ Residential proxy (provider: ____, geo: ____)
  □ Behavioral humanization (mouse curve, jitter, dwell)
  □ Geo-consistent locale + timezone + UA
  □ Per-session IP / cookie isolation

Rate limit:
  Documented: ____ req/min
  Applied: ____ req/min (≤ 50% of documented)
  Backoff on 429: exponential + jitter

Logging:
  Refusal/exception log: .vector/refusal-log.md
  Request log: .vector/stealth-runs/<date>.jsonl
```

---

## 10. References
- Cloudflare Bot Management documentation
- Akamai Bot Manager Premium overview
- JA3 / JA4 fingerprinting (Salesforce / FoxIO)
- `playwright-extra` and `puppeteer-extra-plugin-stealth` repositories
- `curl-impersonate` (TLS fingerprint matching)
- intoli.com and abrahamjuliot.github.io/creepjs (testing tools)
- EU AI Act Article 53 (GPAI compliance with content owner opt-out signals)
