# Voyager Reference Index

Every `reference/` file `voyager` owns, and the condition that makes it worth
reading. `voyager/SKILL.md` keeps only the shared-contract rows and a pointer here.

**Read this when** you need a reference and the Recipe registry did not already
name it, or when scanning what this skill can consult at all.

---

| File | Read this when |
|------|----------------|
| [playwright-patterns.md](reference/playwright-patterns.md) | Playwright is the default or current framework |
| [framework-selection.md](reference/framework-selection.md) | You must choose or justify the framework |
| [cypress-guide.md](reference/cypress-guide.md) | The project already uses Cypress |
| [visual-a11y-testing.md](reference/visual-a11y-testing.md) | Visual regression, keyboard flows, or WCAG checks |
| [selector-accessibility-first.md](reference/selector-accessibility-first.md) | Selector rules, ARIA snapshots, or fallback criteria |
| [ci-reporting.md](reference/ci-reporting.md) | Wiring CI, sharding, artifacts, or reporters |
| [performance-testing.md](reference/performance-testing.md) | Core Web Vitals, Lighthouse CI, or browser performance budgets |
| [complex-scenarios.md](reference/complex-scenarios.md) | Multi-tab, iframe, file, WebSocket, offline, or Shadow DOM behavior |
| [environment-management.md](reference/environment-management.md) | Docker, preview envs, auth setup, mail capture, local-only E2E |
| [ephemeral-env-test-data.md](reference/ephemeral-env-test-data.md) | Test isolation, factories, preview environments, network interception |
| [debug-monitoring.md](reference/debug-monitoring.md) | Diagnosing flake, console issues, traces, HARs, or retries |
| [edge-cases-i18n.md](reference/edge-cases-i18n.md) | Timezone, locale, cookie, storage, offline, or network-condition cases matter |
| [cloud-testing.md](reference/cloud-testing.md) | Cloud device sessions (BrowserStack / Sauce / LambdaTest / Device Farm / Test Lab) — matrices, tunnels, parallel caps, cost tiers, credentials |
| [mobile-testing.md](reference/mobile-testing.md) | Artifact is a shipping `.ipa`/`.apk`/`.aab` or RN bundle — framework selection, mobile POM, accessibility-id locators, flake taxonomy, device-farm tiers, Appium config, rotation/push/airplane patterns. **Start here for native mobile E2E.** |
| [2026-best-practices.md](reference/2026-best-practices.md) | Source citations and version notes — Test Agents, CLI-vs-MCP, axe-core ceiling, flake loops, visual-regression tiers, Appium 3 BiDi, flake/budget thresholds |
| [e2e-anti-patterns.md](reference/e2e-anti-patterns.md) | Suite architecture, anti-pattern checks, or flaky-prevention thresholds |
| [ai-powered-e2e-testing.md](reference/ai-powered-e2e-testing.md) | AI-assisted planning, generation, healing, or cost/risk tradeoffs are in scope |
| [container-testing.md](reference/container-testing.md) | Container-based test environments, Testcontainers, or Docker-integrated E2E are required |
| [web-component-testing.md](reference/web-component-testing.md) | Shadow DOM, Lit, Stencil, or Web Component testing is required |
| [api-e2e-testing.md](reference/api-e2e-testing.md) | E2E through an API-only interface — `APIRequestContext` chains, mock-vs-real toggle, contract-test follow-up |
| [component-testing.md](reference/component-testing.md) | Component tests in a real browser (Playwright CT, Cypress CT, Storybook Interactions) |
| [xcuitest-patterns.md](reference/xcuitest-patterns.md) | Authoring stable XCUITest suites or Swift Screen Objects (`ios` recipe) |
| [ios-identifier-strategy.md](reference/ios-identifier-strategy.md) | Designing or auditing the accessibility-identifier contract |
| [ios-screenshot-strategies.md](reference/ios-screenshot-strategies.md) | Capturing deterministic UI-test screenshots or regression evidence |
| [fastlane-snapshot.md](reference/fastlane-snapshot.md) | Producing localized App Store screenshots across device matrices |
| [ios-ci-integration.md](reference/ios-ci-integration.md) | Wiring xcodebuild, xcresulttool, simulator pools, or remote XCUITest farms into CI |
| [recipe-verify-gates.md](reference/recipe-verify-gates.md) | Per-Recipe behavior and the full VERIFY checklist |
| [OPUS_5_AUTHORING.md](../_common/OPUS_5_AUTHORING.md) | Sizing the test plan, calibrating effort to risk tier, front-loading journey scope at PLAN. Critical: P3, P6. |
| [PROOF_CARRYING.md](../_common/PROOF_CARRYING.md) | Invoked from `nexus acceptance` Phase 2 (UI flows + visual regression, Layer 2 oracles) and Phase 3 (adversarial UI personas). Findings need non-trivial exploration logs — empty ones are rejected. |
| `reference/autorun-schema.md` | Emitting the AUTORUN `_STEP_COMPLETE` block — Voyager-specific Output/Next schema. |
