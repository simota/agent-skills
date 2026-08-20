# Voyager Recipe Registry

The full Recipe table for `voyager`. `voyager/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Playwright Suite | `playwright` | ✓ | Playwright E2E test suite creation | `reference/playwright-patterns.md` |
| Page Object | `page-object` | | Page Object Model design and implementation | `reference/playwright-patterns.md` |
| Auth Flow | `auth` | | Authentication flow E2E tests | `reference/complex-scenarios.md` |
| Accessibility | `a11y` | | Accessibility automated testing | `reference/visual-a11y-testing.md` |
| Visual Regression | `visual` | | Visual regression testing | `reference/visual-a11y-testing.md` |
| API E2E | `api` | | User-journey E2E through an API-only interface (no UI): HTTP call → backend state → downstream API validation chain | `reference/api-e2e-testing.md` |
| Mobile E2E | `mobile` | | E2E testing for shipped mobile apps (Detox / Maestro / Appium / device farm) | `reference/mobile-testing.md` |
| Component Test | `component` | | Component tests executed in a real browser (Playwright CT / Cypress CT / Storybook Interactions) | `reference/component-testing.md` |
| iOS XCUITest & Snapshots | `ios` | | XCUITest, identifier audit, screenshot/App Store snapshot, CI, device-farm, or xcresult work; select `xcuitest|identifier|screenshot|appstore|ci|farm|xcresult` mode | `reference/xcuitest-patterns.md`, matching `reference/ios-*.md` or `reference/fastlane-snapshot.md` |
