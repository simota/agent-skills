# Mobile Testing Reference

Purpose: Build an E2E test harness around a **shipped mobile application** (an app the team is releasing to users). Validate critical journeys on real or emulated devices, in a CI-scalable way, with device-farm execution for matrix coverage. Covers framework selection, device-farm strategy, Page Object design, locator rules, concrete WebdriverIO + Appium configuration patterns, real-device session capabilities, Playwright mobile-emulation alternatives, and mobile-specific test recipes.

Contents:
- Scope boundary and agent ownership
- Framework selection (strategic)
- Device farm strategy (strategic)
- Locator / accessibility-id rules
- Framework-specific config snippets (WebdriverIO, Appium, Playwright mobile emulation)
- Common flake taxonomy and test patterns
- CI shape and anti-patterns
- 2025-2026 trend update

## Cross-Reference

| You need | Read |
|----------|------|
| Cloud session control (tunnels, parallel session caps, credential management, cost-tier strategy), provider integration tables for App Automate / Real Device Cloud / AWS Device Farm / Firebase Test Lab | `cloud-testing.md` |

## Scope Boundary

- **Voyager `mobile`**: E2E harness around a production-bound mobile app. Owns test design, Page Object for mobile, device matrix, device-farm integration.
- **Forge `mobile`**: throwaway mobile PoC (Expo / RN / Flutter), native capabilities stubbed, ≤4h time-box. Not released, not tested at matrix scale.
- **Native**: builds and ships the mobile app — navigation architecture, offline strategy, store review. Owns the app under test.
- **Voyager `playwright`**: mobile-browser emulation of a web app. If the product is a PWA, that recipe is the right tool. `mobile` is for native / React Native binaries.

If the artifact is an `.ipa` / `.apk` / `.aab` being shipped, → `mobile`. If it is Chromium mobile-viewport tests, → `playwright` with emulation.

## Agent Boundary

| Responsibility | Voyager | Vector | Artisan |
|----------------|---------|-----------|---------|
| **Mobile E2E tests** | ✅ Primary | | |
| **Mobile browser tasks** | | ✅ Primary | |
| **Mobile UI components** | | | ✅ Primary |

**Rule of thumb**: Voyager owns mobile E2E test design and execution. Vector handles one-off mobile browser tasks. Artisan implements responsive mobile components.

---

## Framework Selection

| Framework | Pick when | Skip when |
|-----------|-----------|-----------|
| **Detox** | React Native app, fastest feedback (grey-box, syncs with RN bridge), deterministic | Non-RN native app; true black-box required |
| **Maestro** | Cross-platform YAML DSL, lowest authoring cost, excellent for smoke flows, CI-simple | Deep programmatic logic, complex fixtures |
| **Appium** | Cross-platform native + hybrid, widest device matrix, WebDriver-compatible | Team wants minimal YAML DSL; speed over breadth |
| **XCUITest / Espresso** | Platform-native only (iOS-only or Android-only product); tight integration with native build pipeline | Cross-platform suite, shared test authoring |

Default matrix strategy: **Detox for RN smoke** + **Maestro for cross-platform critical paths** + **Appium on device farm** for the release-gate matrix.

### Playwright Emulation vs Real Device

Use Playwright emulation for responsive layout + basic mobile UX. Use real devices (Appium) for native features + real performance testing.

| Feature | Playwright Emulation | Real Device |
|---------|---------------------|-------------|
| **Viewport / user-agent** | ✅ Accurate | ✅ Native |
| **Touch events** | ✅ Simulated | ✅ Native |
| **Device rotation** | ⚠️ Viewport resize only | ✅ Accelerometer |
| **Push notifications** | ❌ Not supported | ✅ Native |
| **Camera / GPS** | ⚠️ Permission grants only | ✅ Native |
| **App install / deep links** | ❌ Browser only | ✅ Native |
| **Performance (real)** | ❌ Desktop CPU/GPU | ✅ Device constraints |
| **Gestures (swipe/pinch)** | ⚠️ Basic via touchscreen | ✅ Native |

## Workflow

```
PLAN       → list critical journeys (login, purchase, onboarding, push-notif handling)
           → pick frameworks per journey (smoke vs matrix vs platform-specific)
           → decide device matrix tier (local sim/emu → device farm → real-device release gate)
           → define real-device flake budget (quarantine bucket separate from logic flake)

AUTOMATE   → Page Object per screen (mobile POM — design around user intent, not view hierarchy)
           → use accessibility IDs (iOS accessibilityIdentifier, Android contentDescription)
           → never use text-based locators for localized strings unless the test is locale-specific
           → stub network at the app boundary (mock server / MSW native / WireMock)

STABILIZE  → retry only transient device noise (ADB disconnect, sim crash); never retry logic failures
           → separate device-specific quarantine from logic quarantine
           → collect video + device logs on failure; wire to CI artifacts

SCALE      → route matrix runs to BrowserStack / Sauce Labs / AWS Device Farm
           → shard by device, not by test
           → release-gate tier = real devices on 3+ OS versions; PR tier = 1 sim + 1 emu
```

## Device Farm Strategy

| Farm | Strength | Watch for |
|------|----------|-----------|
| **BrowserStack App Automate** | Broadest real-device matrix, Appium + Detox + XCUITest, parallel sessions | Per-minute cost scales fast; prune matrix before enabling |
| **Sauce Labs Real Device Cloud** | Strong Appium support, enterprise SSO, detailed logs | iOS pool capacity fluctuates at release time |
| **AWS Device Farm** | Pay-per-minute, integrates with CodeBuild/CodePipeline | Slower session acquisition than BS/SL |
| **Firebase Test Lab** | Android-only, cheap, Robo-crawler included | No iOS — pair with BS/SL for full coverage |

Rule of thumb: local simulators/emulators for the dev loop; one farm for the PR-blocking smoke; a second farm / real-device lab for release gate. Never run the PR gate on real devices — flake budget and cost both explode.

## Locator Strategy

Mobile has no DOM. Use accessibility trees:

```ts
// Detox (React Native)
await element(by.id('login-submit')).tap();  // testID prop on the component

// Appium (cross-platform)
await driver.$('~login-submit').click();     // ~ prefix = accessibility id

// Maestro (YAML)
- tapOn:
    id: "login-submit"
```

Priority: `accessibilityIdentifier` / `testID` > accessibility label > text. Text locators break on localization and A/B copy tests.

## Flake Management

Mobile E2E has **two independent flake sources**:

1. **Logic flake**: race conditions, missing waits, state bleed. Same remediation as web E2E — replace sleeps with condition-based waits.
2. **Device flake**: simulator crashes, ADB disconnects, farm session timeout, network flap. Quarantine separately; retry budget applies only here.

Do not mix the two. A logic flake hidden in a device-flake retry policy ships a bug to production. Tag quarantined tests with `@flaky-device` vs `@flaky-logic`.

## Anti-Patterns

- Running the full device matrix on every PR — 45+ min wait, cost explosion, noise. Keep PR gate on 2 devices, push matrix to nightly + release.
- Text-based locators on localized screens — translation changes break the suite.
- Real push notifications in tests — permission dialog races, APNs/FCM deliverability noise. Stub the push payload at the app boundary.
- Testing with the production backend — rate limits, real charges, real user data. Always route to a staging or mock API.
- One giant `beforeAll` that logs in via UI — slow, flaky, and couples every test to the login screen. Use `storageState` equivalents (Detox: launch-args with auth token; Appium: pre-set keychain/SharedPrefs).
- Skipping biometric / camera / permission tests "because they are hard" — at least stub them; route real-hardware validation to Native.

## CI Shape

- PR tier: 1 iOS sim + 1 Android emu, smoke tag only, < 10 min.
- Nightly tier: 3-5 device classes on a farm, regression + smoke.
- Release gate: real devices on the oldest and newest supported OS versions per platform.
- Never block a PR on the full matrix — cost and flake budget both collapse.

## Handoff

- To **Native**: a failure that reproduces as a bug in the app (not the test).
- To **Voyager `playwright`**: PWA or responsive web in a mobile viewport.
- To **Siege**: load / background-kill / low-memory verification.
- To **Probe**: mobile DAST (reverse-engineering protection, cert pinning bypass checks).

---

## Playwright Mobile Emulation (Snippets)

### Device Emulation

```typescript
// playwright.config.ts
import { devices } from '@playwright/test';

export default defineConfig({
  projects: [
    { name: 'mobile-chrome', use: { ...devices['Pixel 7'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 14'] } },
    { name: 'tablet', use: { ...devices['iPad Pro 11'] } },
  ],
});
```

### Touch & Gesture Simulation

```typescript
test('swipe to delete item', async ({ page }) => {
  await page.goto('/todo');

  const item = page.getByTestId('todo-item-1');
  const box = await item.boundingBox();

  // Simulate swipe left
  await page.touchscreen.tap(box!.x + box!.width - 10, box!.y + box!.height / 2);
  await page.mouse.move(box!.x + box!.width - 10, box!.y + box!.height / 2);
  await page.mouse.down();
  await page.mouse.move(box!.x + 10, box!.y + box!.height / 2, { steps: 10 });
  await page.mouse.up();

  await expect(page.getByTestId('delete-confirm')).toBeVisible();
});

test('pinch to zoom on map', async ({ page }) => {
  await page.goto('/map');

  // Dispatch touch events for pinch gesture
  await page.evaluate(() => {
    const map = document.querySelector('[data-testid="map-container"]')!;
    const rect = map.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    const touch1 = new Touch({ identifier: 0, target: map, clientX: cx - 50, clientY: cy });
    const touch2 = new Touch({ identifier: 1, target: map, clientX: cx + 50, clientY: cy });
    map.dispatchEvent(new TouchEvent('touchstart', { touches: [touch1, touch2] }));

    const touch1End = new Touch({ identifier: 0, target: map, clientX: cx - 100, clientY: cy });
    const touch2End = new Touch({ identifier: 1, target: map, clientX: cx + 100, clientY: cy });
    map.dispatchEvent(new TouchEvent('touchmove', { touches: [touch1End, touch2End] }));
    map.dispatchEvent(new TouchEvent('touchend', { touches: [] }));
  });
});
```

---

## WebdriverIO + Appium (Native Apps)

### Setup

```bash
# Install dependencies
npm install -D webdriverio @wdio/cli @wdio/appium-service @wdio/mocha-framework

# Install Appium
npm install -g appium
appium driver install uiautomator2  # Android
appium driver install xcuitest       # iOS
```

### Configuration

```typescript
// wdio.conf.ts
export const config: WebdriverIO.Config = {
  runner: 'local',
  specs: ['./e2e/mobile/**/*.spec.ts'],
  capabilities: [{
    platformName: 'Android',
    'appium:deviceName': 'Pixel 7',
    'appium:platformVersion': '14',
    'appium:automationName': 'UiAutomator2',
    'appium:app': './app/build/outputs/apk/debug/app-debug.apk',
  }],
  services: ['appium'],
  framework: 'mocha',
};
```

### Native App Test Example

```typescript
describe('Login Flow (Native)', () => {
  it('should login with valid credentials', async () => {
    const emailInput = await $('~email-input');  // accessibility id
    await emailInput.setValue('test@example.com');

    const passwordInput = await $('~password-input');
    await passwordInput.setValue('Test1234!');

    const loginButton = await $('~login-button');
    await loginButton.click();

    const dashboard = await $('~dashboard-screen');
    await expect(dashboard).toBeDisplayed();
  });
});
```

---

## Real Device Testing (Cloud)

### BrowserStack App Automate

```typescript
// wdio.conf.browserstack.ts
export const config: WebdriverIO.Config = {
  user: process.env.BROWSERSTACK_USERNAME,
  key: process.env.BROWSERSTACK_ACCESS_KEY,
  hostname: 'hub.browserstack.com',
  capabilities: [{
    platformName: 'Android',
    'appium:deviceName': 'Google Pixel 7',
    'appium:platformVersion': '14.0',
    'appium:app': process.env.BROWSERSTACK_APP_URL,
    'bstack:options': {
      projectName: 'Mobile E2E',
      buildName: process.env.GITHUB_SHA || 'local',
      sessionName: 'Login Flow',
    },
  }],
};
```

### Sauce Labs Real Devices

```typescript
// wdio.conf.saucelabs.ts
export const config: WebdriverIO.Config = {
  user: process.env.SAUCE_USERNAME,
  key: process.env.SAUCE_ACCESS_KEY,
  hostname: 'ondemand.us-west-1.saucelabs.com',
  capabilities: [{
    platformName: 'iOS',
    'appium:deviceName': 'iPhone 15',
    'appium:platformVersion': '17',
    'appium:app': 'storage:filename=app.ipa',
    'sauce:options': {
      appiumVersion: '2.0',
      name: 'iOS E2E Tests',
    },
  }],
};
```

---

## Mobile-Specific Test Patterns

### Device Rotation

```typescript
it('handles orientation change', async () => {
  await driver.setOrientation('PORTRAIT');
  const portraitNav = await $('~mobile-nav');
  await expect(portraitNav).toBeDisplayed();

  await driver.setOrientation('LANDSCAPE');
  const landscapeNav = await $('~desktop-nav');
  await expect(landscapeNav).toBeDisplayed();
});
```

### Push Notification Testing

```typescript
it('receives push notification', async () => {
  // Trigger notification via API
  await fetch(`${API_URL}/test/send-push`, {
    method: 'POST',
    body: JSON.stringify({ userId: 'test-user', message: 'New order received' }),
  });

  // Wait for notification (Android)
  await driver.openNotifications();
  const notification = await $('android=new UiSelector().textContains("New order")');
  await expect(notification).toBeDisplayed();

  await notification.click();

  const orderScreen = await $('~order-detail-screen');
  await expect(orderScreen).toBeDisplayed();
});
```

### Network Condition Testing (Mobile)

```typescript
it('handles offline mode gracefully', async () => {
  await driver.toggleAirplaneMode();

  const offlineMsg = await $('~offline-message');
  await expect(offlineMsg).toBeDisplayed();

  await driver.toggleAirplaneMode();

  const syncComplete = await $('~sync-complete');
  await expect(syncComplete).toBeDisplayed();
});
```

---

## CI Configuration for Mobile

### GitHub Actions + Appium

```yaml
# .github/workflows/mobile-e2e.yml
name: Mobile E2E Tests

on:
  push:
    branches: [main]

jobs:
  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci

      - name: Start Android Emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 34
          target: google_apis
          arch: x86_64
          script: npx wdio run wdio.conf.ts

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mobile-e2e-report
          path: allure-results/

  ios-cloud:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - name: Run iOS tests on BrowserStack
        run: npx wdio run wdio.conf.browserstack.ts
        env:
          BROWSERSTACK_USERNAME: ${{ secrets.BROWSERSTACK_USERNAME }}
          BROWSERSTACK_ACCESS_KEY: ${{ secrets.BROWSERSTACK_ACCESS_KEY }}
          BROWSERSTACK_APP_URL: ${{ secrets.BROWSERSTACK_APP_URL }}
```

---

## 2025-2026 Trend Update (as of 2026-04)

### Framework lifecycle status

| Framework | Status | Source |
|-----------|--------|--------|
| **Appium 3.x** | GA since **2025-08-07**. JSONWP fully removed (W3C-only). `appium:` capability prefix is mandatory. Driver/plugin decoupling is now the default; install only what you need (`--use-drivers`, `--use-plugins`). Node 20.19+ / npm 10+. Express 5 internally. New `X-Appium-Is-Sensitive` HTTP header masks secrets in logs. Inspector hostable in-process (`appium plugin install inspector`). Migration impact is smaller than 2.x; treat 3.x as a cleanup release. Source: <https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/> · <https://appium.io/docs/en/3.1/guides/migrating-2-to-3/> | Official |
| **Detox** | New Architecture officially supported on **RN 0.77.x – 0.84.x** (covers RN 0.79+). Practical friction reported on RN 0.81+ in some CI setups — pin Detox to a tested combo before upgrading. Source: <https://github.com/wix/Detox/issues/4799> · <https://github.com/wix/Detox/issues/4832> | GitHub Issues |
| **Maestro** | Maestro Studio (visual flow recorder), **Maestro Cloud** (binary upload + scheduled runs + PR-trigger), and **MaestroGPT** / AI test analysis (LLM-powered failure summaries beyond pass/fail) shipped through 2025. Lowest authoring cost remains the differentiator. Source: <https://docs.maestro.dev/maestro-flows/workspace-management/ai-test-analysis> · <https://docs.maestro.dev/maestro-studio/run-cloud-tests-from-maestro-studio> | Official |
| **XCUITest / Swift Testing** | Xcode 26 / Swift 6.2 introduced Swift Testing macros (`@Test`, `#expect`, parameterized arguments, exit tests, ranged confirmations, test scoping traits). Swift Testing has **no UI automation story yet** — XCUITest remains the only native UI driver as of 2026-04. XCTest stays fully supported for legacy + UI suites. Source: <https://developer.apple.com/xcode/swift-testing/> · <https://forums.swift.org/t/whats-new-in-testing-swift-6-2-xcode-26/80688> | Official |
| **Espresso + Compose UI Test** | `Modifier.testTag` + `testTagsAsResourceId` semantic remains the Espresso ↔ Compose interop bridge (Compose 1.2.0-alpha08+). **Robolectric 4.16** (released 2025-Q3) adds Android 16 / SDK 36 / Baklava support and requires JDK 21; introduces `ResourcesMode.NATIVE` for SDK 36 only. Robolectric 4.14/4.15 do **not** support Baklava — upgrade to 4.16 before targeting SDK 36 in JVM tests. Source: <https://github.com/robolectric/robolectric/releases/tag/robolectric-4.16> · <https://developer.android.com/develop/ui/compose/testing/interoperability> | Official |
| **WebDriver BiDi** | W3C Editor's Draft, living standard, continuously evolving. Appium 3.2 docs expose a BiDi reference, and Selenium / WebdriverIO surface BiDi via the `webSocketUrl` session field. A formal **mobile profile** has not landed at W3C as of 2026-04 — treat BiDi-on-mobile as exploratory and stay on classic WebDriver for production gates. Source: <https://w3c.github.io/webdriver-bidi/> · <https://appium.io/docs/en/3.2/reference/api/bidi/> | W3C / Appium |

### Appium 3.x capability handling (released 2025-08-07)

Appium 3.x makes the `appium:` capability prefix mandatory and drops JSONWP entirely (W3C-only). Existing 2.x configs will fail at session creation if non-standard caps are not prefixed. Decoupled drivers/plugins mean the CI runner only installs what is needed; Inspector can now be hosted in-process via `appium plugin install inspector`. Sensitive headers are masked with `X-Appium-Is-Sensitive`. Source: <https://appium.io/docs/en/3.1/blog/2025/08/07/-appium-3/> · <https://appium.io/docs/en/3.1/guides/migrating-2-to-3/>

```typescript
// Appium 3.x: every non-W3C cap MUST carry the appium: prefix
capabilities: [{
  // W3C standard caps (no prefix)
  platformName: 'Android',
  // Appium-specific (prefix mandatory)
  'appium:deviceName': 'Pixel 7',
  'appium:platformVersion': '14',
  'appium:automationName': 'UiAutomator2',
  'appium:app': './app/build/outputs/apk/debug/app-debug.apk',
}]
```

CI prerequisites for Appium 3.x: Node.js >= 20.19.0, npm >= 10. Install only the drivers and plugins you need:

```bash
appium driver install uiautomator2
appium driver install xcuitest
appium plugin install images          # only if used
appium --use-drivers=uiautomator2,xcuitest --use-plugins=images
```

### Swift Testing (Xcode 26 / Swift 6.2) vs XCUITest

Swift Testing (`@Test`, `#expect`, parameterized arguments, exit tests, ranged confirmations, scoping traits) is the modern unit-test framework for new code. **It does not yet have a UI automation story** — XCUITest is still the only native iOS UI driver as of 2026-04, and XCTest remains fully supported for legacy and UI tests. Mix Swift Testing for logic tests with XCUITest for UI flows in the same target. Source: <https://developer.apple.com/xcode/swift-testing/> · <https://forums.swift.org/t/whats-new-in-testing-swift-6-2-xcode-26/80688>

### Compose UI Test ↔ Espresso interop & Robolectric 4.16

Espresso reaches Compose nodes through the Compose semantics tree by enabling `testTagsAsResourceId = true` on a composable subtree (Compose 1.2.0-alpha08+). For JVM tests targeting Android 16 / SDK 36 (Baklava), upgrade to **Robolectric 4.16** (released 2025-Q3) on **JDK 21**; older 4.14/4.15 do not support Baklava. Robolectric 4.16 introduces `ResourcesMode.NATIVE` (SDK 36 only). Source: <https://github.com/robolectric/robolectric/releases/tag/robolectric-4.16> · <https://developer.android.com/develop/ui/compose/testing/interoperability>

```kotlin
// Compose composable: opt the subtree into resource-id semantics for Espresso
Box(
  Modifier.semantics { testTagsAsResourceId = true }.testTag("checkout-submit")
) { /* ... */ }
```

### Adaptive / foldable testing

- Compose Material 3 `WindowSizeClass` exposes **compact / medium / expanded** breakpoints (plus large / extra-large in newer adaptive libraries). Test layouts at every breakpoint AND at fold/unfold posture transitions. Source: <https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes>
- Concrete devices to cover at release-gate tier as of 2026-04: Galaxy Z Fold 7 (and the leaked **Wide-form** Z Fold 8 expected ~2026-07), Pixel 10 Pro Fold (first IP68 foldable), iPad Pro with Stage Manager / Split View. Source: <https://9to5google.com/2026/04/26/samsung-galaxy-z-fold-8-wide-leak/>
- Add at least one **fold ↔ unfold posture transition** smoke test — state preservation across hinge events is the foldable-specific bug class web E2E never sees.

```kotlin
// Drive layout under each WindowSizeClass breakpoint and verify the right pane appears.
@RunWith(AndroidJUnit4::class)
class AdaptiveLayoutTest {
  @Test fun showsListDetailOnExpanded() {
    composeTestRule.setContent {
      val widthSize = WindowWidthSizeClass.Expanded
      // ...assert dual-pane visible
    }
  }
}
```

For real-device fold/unfold posture coverage, target Galaxy Z Fold (incl. expected wide-form Z Fold 8 in 2026-07), Pixel 10 Pro Fold (IP68), and large-screen iPad Pro with Stage Manager. Add at least one fold ↔ unfold posture transition test to the release-gate tier — state-loss bugs across hinge events are foldable-specific. Source: <https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes> · <https://9to5google.com/2026/04/26/samsung-galaxy-z-fold-8-wide-leak/>

### WebDriver BiDi for mobile (status as of 2026-04)

WebDriver BiDi remains a W3C **Editor's Draft** — a living standard with continuous additions. Appium 3.2 docs include a BiDi reference, and Selenium 4 / WebdriverIO surface BiDi via the `webSocketUrl` session field. A formal **mobile profile** has not been ratified as of 2026-04. Treat BiDi-on-mobile as exploratory; keep production gates on classic WebDriver until a stable mobile profile lands. Source: <https://w3c.github.io/webdriver-bidi/> · <https://appium.io/docs/en/3.2/reference/api/bidi/>

### Privacy Manifest impact on the test harness

- Apple's Privacy Manifest enforcement: **2024-05-01** for new App Store submissions, **2025-02-12** for new privacy-impacting third-party SDKs. Required-reason API categories include disk space, active keyboard, user defaults, file timestamp, and system boot time. Source: <https://developer.apple.com/documentation/bundleresources/privacy-manifest-files> · <https://developer.apple.com/news/?id=3d8a9yyh>
- **Test-side implication**: any XCUITest helper, Appium driver, mock SDK, or analytics-stub bundled into the test target must declare its own `PrivacyInfo.xcprivacy`. App Store Connect aggregates app + SDK manifests; a missing test SDK reason can block a TestFlight build. Add a CI step that diffs the merged manifest before release.
