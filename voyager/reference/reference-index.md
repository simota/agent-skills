# Voyager Reference Index

Every `reference/` file `voyager` owns, and the condition that makes it worth
reading. `voyager/SKILL.md` keeps only the shared-contract rows and a pointer here.

**Read this when** you need a reference and the Recipe registry did not already
name it, or when scanning what this skill can consult at all.

---

| File | Read this when |
|------|----------------|
| `reference/playwright-patterns.md` | Playwright is the default or current framework |
| `reference/cypress-guide.md` | The project already uses Cypress |
| `reference/visual-a11y-testing.md` | Visual regression, keyboard flows, or WCAG checks |
| `reference/selector-accessibility-first.md` | Selector rules, ARIA snapshots, or fallback criteria |
| `reference/performance-testing.md` | Core Web Vitals, Lighthouse CI, or browser performance budgets |
| `reference/environment-management.md` | Docker, preview envs, auth setup, mail capture, local-only E2E |
| `reference/cloud-testing.md` | Cloud device sessions (BrowserStack / Sauce / LambdaTest / Device Farm / Test Lab) — matrices, tunnels, parallel caps, cost tiers, credentials |
| `reference/mobile-testing.md` | Artifact is a shipping `.ipa`/`.apk`/`.aab` or RN bundle — framework selection, mobile POM, accessibility-id locators, flake taxonomy, device-farm tiers, Appium config, rotation/push/airplane patterns. **Start here for native mobile E2E.** |
| `reference/2026-best-practices.md` | Source citations and version notes — Test Agents, CLI-vs-MCP, axe-core ceiling, flake loops, visual-regression tiers, Appium 3 BiDi, flake/budget thresholds |
| `reference/ai-powered-e2e-testing.md` | AI-assisted planning, generation, healing, or cost/risk tradeoffs are in scope |
| `reference/api-e2e-testing.md` | E2E through an API-only interface — `APIRequestContext` chains, mock-vs-real toggle, contract-test follow-up |
| `reference/component-testing.md` | Component tests in a real browser (Playwright CT, Cypress CT, Storybook Interactions) |
| `reference/xcuitest-patterns.md` | Authoring stable XCUITest suites or Swift Screen Objects (`ios` recipe) |
| `reference/ios-identifier-strategy.md` | Designing or auditing the accessibility-identifier contract |
| `reference/ios-screenshot-strategies.md` | Capturing deterministic UI-test screenshots or regression evidence |
| `reference/fastlane-snapshot.md` | Producing localized App Store screenshots across device matrices |
| `reference/ios-ci-integration.md` | Wiring xcodebuild, xcresulttool, simulator pools, or remote XCUITest farms into CI |
| `reference/recipe-verify-gates.md` | Per-Recipe behavior and the full VERIFY checklist |
| `_common/OPUS_5_AUTHORING.md` | Sizing the test plan, calibrating effort to risk tier, front-loading journey scope at PLAN. Critical: P3, P6. |
| `_common/PROOF_CARRYING.md` | Invoked from `nexus acceptance` Phase 2 (UI flows + visual regression, Layer 2 oracles) and Phase 3 (adversarial UI personas). Findings need non-trivial exploration logs — empty ones are rejected. |
| `_common/AUTORUN.md` | Emitting the AUTORUN `_STEP_COMPLETE` block — shared default schema; preserve the `Next` restriction in SKILL.md’s AUTORUN section. |
