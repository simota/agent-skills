# Cloud Testing Services

Purpose: Use this file when Voyager must run browser **or native mobile** suites on BrowserStack, Sauce Labs, LambdaTest, AWS Device Farm, Firebase Test Lab, or a similar cloud matrix.

Contents:
- Agent boundary and cloud vs local decision rules
- Provider integration templates (web browsers + native mobile App Automate / Real Device Cloud)
- Cost, security, and troubleshooting rules

## Cross-Reference

| You need | Read |
|----------|------|
| Native mobile E2E framework selection (Detox / Maestro / Appium / XCUITest / Espresso), device-farm tier matrix (PR / nightly / release), concrete WebdriverIO + Appium configuration for cloud sessions, mobile-specific patterns (rotation, push, airplane mode) | `mobile-testing.md` (start there) |
| Web browser cloud session config, tunnels, parallel session caps, cost-tier strategy | this file |

## Native Mobile Cloud Sessions (App Automate / Real Device Cloud)

For native mobile cloud orchestration, use the App Automate / Real Device Cloud variants of the providers below:

| Farm | Native mobile entry point | Strength | Watch for |
|------|--------------------------|----------|-----------|
| **BrowserStack App Automate** | Appium / Detox / XCUITest / Espresso, real-device parallel sessions; **App Percy** bundled visual AI | Broadest real-device matrix, tight CI integrations | Per-minute cost scales fast; prune matrix before enabling |
| **Sauce Labs Real Device Cloud** | Strong Appium support, enterprise SSO | Detailed device logs, reliable iOS pool | iOS pool capacity fluctuates at release time |
| **AWS Device Farm** | Pay-per-minute, integrates with CodeBuild/CodePipeline | Cheapest steady-state for AWS-native shops | Slower session acquisition than BS/SL |
| **Firebase Test Lab** | Android-only, Robo-crawler included | Cheapest Android matrix, virtual + physical devices | iOS unsupported — pair with BS/SL for full coverage |
| **LambdaTest HyperExecute** | Real-device + KaneAI test generation; rebranded **TestMu AI** as of 2026-01 | Modular per-product billing (Live, Automation, HyperExecute, SmartUI, KaneAI, TestManager) | Combined-product seat cost can exceed $650/month — confirm scope before enabling |

Concrete WebdriverIO + Appium capability examples for App Automate / Real Device Cloud live in `mobile-testing.md` (BrowserStack and Sauce Labs sections). The web Playwright capability examples below remain unchanged for browser-only matrices.

### Firebase Test Lab — 2025-2026 lifecycle status

As of 2026-04, **Firebase Test Lab is actively maintained** with no published deprecation or sunset notice. Recent updates include refreshed iOS default devices and additions to the device catalog. It continues to support Robo tests, instrumentation tests, Game Loop tests, and XCTest. Source (official docs, last updated 2026-04-23): <https://firebase.google.com/docs/test-lab>

**Do not confuse with Firebase Studio**, a separate Firebase product (cloud IDE) that **is** being shut down: shutdown phase begins 2026-03-19, full shutdown 2027-03-22, with new workspace creation disabled 2026-06-22. Firebase Test Lab is unaffected. Source: <https://farhanabhatt.com/firebase-studio-shutdown-announced-google-reveals-next-move/>

Also note **Firebase Dynamic Links** was deprecated with final shutdown 2025-08-25 — also unrelated to Test Lab. Source: <https://firebase.google.com/support/dynamic-links-faq>

### Selecting a device farm (2026 selection criteria)

| Choose | When |
|--------|------|
| **BrowserStack App Automate** | Need broadest real-device matrix on PR-blocking smoke; want App Percy visual AI bundled; iOS + Android parity required |
| **Sauce Labs Real Device Cloud** | Enterprise SSO / SAML required; need deep device logs; already on Sauce for web |
| **AWS Device Farm** | AWS-native shop with CodeBuild / CodePipeline; cost-sensitive steady-state regression; can tolerate slower session acquisition |
| **Firebase Test Lab** | Android-only product or Android-heavy matrix; want Robo crawler for exploratory smoke; cost is the primary driver |
| **LambdaTest HyperExecute / TestMu AI** | Need modular billing per capability (esp. Live + Automation only); want KaneAI generative test authoring; cross-browser web + mobile in one vendor |

---

## Agent Boundary

| Responsibility | Voyager | Gear | Scaffold |
|----------------|---------|------|----------|
| **Cloud test config** | ✅ Primary | | |
| **CI + cloud integration** | ✅ E2E config | ✅ Pipeline | |
| **Cloud account/infra** | | | ✅ Primary |

**Rule of thumb**: Voyager owns cloud testing configuration and browser matrices. Gear owns CI pipeline integration. Scaffold owns cloud account provisioning.

---

## Cloud vs Local Decision Guide

| Factor | Local | Cloud |
|--------|-------|-------|
| **Speed** | Fast (no network latency) | Slower (remote browsers) |
| **Cost** | Free | Per-minute billing |
| **Browser coverage** | Limited to installed | All browsers + versions |
| **Real devices** | ❌ Emulation only | ✅ Real mobile devices |
| **Parallelism** | Limited by machine | Scalable |
| **Debugging** | Full trace/video | Limited (varies by provider) |

**Decision**: Use local for development + CI smoke tests. Use cloud for cross-browser matrix + real device testing.

---

## BrowserStack Integration

### Playwright Configuration

```typescript
// playwright.config.ts (BrowserStack)
const bsCapabilities = (browser: string, os: string, osVersion: string) => ({
  browser,
  os,
  os_version: osVersion,
  'browserstack.username': process.env.BROWSERSTACK_USERNAME,
  'browserstack.accessKey': process.env.BROWSERSTACK_ACCESS_KEY,
  'browserstack.playwrightVersion': '1.49.0',
  project: process.env.CI ? 'CI E2E' : 'Local E2E',
  build: process.env.GITHUB_SHA || `local-${Date.now()}`,
});

export default defineConfig({
  projects: [
    // Local: fast feedback
    { name: 'local-chromium', use: { ...devices['Desktop Chrome'] } },

    // Cloud: cross-browser matrix
    {
      name: 'bs-chrome-win',
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.browserstack.com/playwright?caps=${encodeURIComponent(
            JSON.stringify(bsCapabilities('chrome', 'Windows', '11'))
          )}`,
        },
      },
    },
    {
      name: 'bs-safari-mac',
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.browserstack.com/playwright?caps=${encodeURIComponent(
            JSON.stringify(bsCapabilities('playwright-webkit', 'OS X', 'Sonoma'))
          )}`,
        },
      },
    },
    {
      name: 'bs-firefox-win',
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.browserstack.com/playwright?caps=${encodeURIComponent(
            JSON.stringify(bsCapabilities('playwright-firefox', 'Windows', '11'))
          )}`,
        },
      },
    },
  ],
});
```

### BrowserStack Local (Tunnel)

```typescript
// e2e/global-setup.ts
import { exec } from 'child_process';

async function globalSetup() {
  if (process.env.BROWSERSTACK_LOCAL === 'true') {
    const tunnel = exec(
      `BrowserStackLocal --key ${process.env.BROWSERSTACK_ACCESS_KEY} --local-identifier ${process.env.GITHUB_SHA || 'local'}`
    );
    await new Promise(resolve => setTimeout(resolve, 5000));
    process.env.__BS_TUNNEL_PID = String(tunnel.pid);
  }
}

export default globalSetup;
```

---

## Sauce Labs Integration

### Playwright Configuration

```typescript
// playwright.config.ts (Sauce Labs)
export default defineConfig({
  projects: [
    {
      name: 'sauce-chrome',
      use: {
        connectOptions: {
          wsEndpoint: `wss://ondemand.${process.env.SAUCE_REGION || 'us-west-1'}.saucelabs.com/playwright?caps=${encodeURIComponent(
            JSON.stringify({
              browserName: 'chromium',
              browserVersion: 'latest',
              platformName: 'Windows 11',
              'sauce:options': {
                username: process.env.SAUCE_USERNAME,
                accessKey: process.env.SAUCE_ACCESS_KEY,
                name: 'E2E Tests',
                build: process.env.GITHUB_SHA || `local-${Date.now()}`,
              },
            })
          )}`,
        },
      },
    },
  ],
});
```

### Sauce Connect (Tunnel)

```bash
sc -u $SAUCE_USERNAME -k $SAUCE_ACCESS_KEY \
  --tunnel-name "e2e-${GITHUB_SHA:-local}" \
  --region us-west-1
```

---

## LambdaTest Integration

### Playwright Configuration

```typescript
// playwright.config.ts (LambdaTest)
const ltCapabilities = {
  browserName: 'Chrome',
  browserVersion: 'latest',
  'LT:Options': {
    platform: 'Windows 11',
    build: process.env.GITHUB_SHA || `local-${Date.now()}`,
    name: 'E2E Tests',
    user: process.env.LT_USERNAME,
    accessKey: process.env.LT_ACCESS_KEY,
    playwrightClientVersion: '1.49.0',
  },
};

export default defineConfig({
  projects: [
    {
      name: 'lambdatest-chrome',
      use: {
        connectOptions: {
          wsEndpoint: `wss://cdp.lambdatest.com/playwright?capabilities=${encodeURIComponent(
            JSON.stringify(ltCapabilities)
          )}`,
        },
      },
    },
  ],
});
```

---

## CI Integration (GitHub Actions + Cloud)

### Cloud Browser Matrix Workflow

```yaml
# .github/workflows/e2e-cloud.yml
name: E2E Cloud Matrix

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6am

jobs:
  cloud-e2e:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        project: [bs-chrome-win, bs-safari-mac, bs-firefox-win]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - name: Run E2E on ${{ matrix.project }}
        run: npx playwright test --project=${{ matrix.project }}
        env:
          BROWSERSTACK_USERNAME: ${{ secrets.BROWSERSTACK_USERNAME }}
          BROWSERSTACK_ACCESS_KEY: ${{ secrets.BROWSERSTACK_ACCESS_KEY }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: report-${{ matrix.project }}
          path: playwright-report/
```

### Selective Cloud Runs

```yaml
# Run cloud tests only on main branch or when labeled
on:
  push:
    branches: [main]
  pull_request:
    types: [labeled]

jobs:
  cloud-e2e:
    if: |
      github.ref == 'refs/heads/main' ||
      contains(github.event.pull_request.labels.*.name, 'cloud-test')
```

---

## Cost Optimization

### Minimal Browser Matrix

| Tier | Browsers | Use When | Est. Minutes/Run |
|------|----------|----------|-----------------|
| **Smoke** | Chrome (local) | Every PR | 2-5 min |
| **Core** | Chrome + Safari + Firefox (cloud) | Main branch | 10-15 min |
| **Full** | + Mobile Safari + Mobile Chrome (cloud) | Release | 20-30 min |

### Cost-Saving Strategies

| Strategy | Savings | Implementation |
|----------|---------|---------------|
| **Run cloud only on main** | ~70% | CI conditional |
| **Tag-based selection** | ~50% | `--grep @cross-browser` |
| **Scheduled full runs** | ~60% | Nightly/weekly cron |
| **Parallel sharding** | Faster, not cheaper | Reduces wall time |
| **Cache browser install** | ~2 min/run | `actions/cache` |

---

## Security Considerations

### Credential Management

| Practice | Description |
|----------|-------------|
| **CI secrets only** | Never hardcode credentials in config |
| **Rotate keys** | Rotate access keys quarterly |
| **Least privilege** | Use read-only API keys where possible |
| **Tunnel security** | Use named tunnels with unique IDs |
| **Audit logs** | Monitor cloud provider usage dashboards |

### Environment Variable Template

```bash
# .env.cloud (DO NOT commit - add to .gitignore)
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
SAUCE_USERNAME=your_username
SAUCE_ACCESS_KEY=your_access_key
LT_USERNAME=your_username
LT_ACCESS_KEY=your_access_key
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|---------|
| **Timeout on cloud** | Network latency | Increase `timeout` in config (+50%) |
| **Element not found** | Browser version diff | Use stable selectors (`data-testid`) |
| **Tunnel connection fail** | Firewall/proxy | Check corporate proxy settings |
| **Flaky on cloud only** | Timing differences | Add explicit waits, avoid `networkidle` |
| **High cost** | Running all tests on cloud | Use tiered matrix strategy |
