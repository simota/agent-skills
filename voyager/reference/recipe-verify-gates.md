# Recipe VERIFY Gates (Full Detail)

**Purpose:** Full per-Recipe behavior notes and VERIFY gate detail for `## Subcommand Dispatch` in SKILL.md — SKILL.md keeps only the one-line summary; read this file for the complete rationale and gate list.
**Read when:** Executing any Recipe below and you need the full VERIFY checklist, not just the summary line.

Each `VERIFY` gate applies **in addition to** Voyager's universal discipline: accessible selectors first, POM by user intent, zero fixed-delay waits, fresh context per test, risk tags, never modify app code (report/hand off).

## `playwright` — full Playwright E2E suite generation

Apply POM; selector-accessibility-first.

**VERIFY**: accessible selectors are primary (`getByRole`/`getByLabel`/`getByText` before `getByTestId`; never CSS-class/positional as primary); zero `page.waitForTimeout` (auto-wait + web-first assertions only); fresh browser context per test (no shared state); risk tag applied (`@critical`/`@smoke`/`@regression`); budgets held (suite ≤10min, test ≤2min, flake <3%).

## `page-object` — design POM classes from existing tests or screen specs

Reusability + maintainability.

**VERIFY**: Page Objects modeled around user intents, not DOM structure; no god-object (≥50 methods → split by intent/component); zero CSS-class/positional primary selectors; methods reusable across tests.

## `auth` — login / OAuth / MFA flows

Use `storageState` for auth reuse across tests.

**VERIFY**: `storageState` reused (auth not re-driven through the UI every test); zero hard-coded credentials (env/secret-injected); auth setup never skipped; OAuth/MFA branches covered where in scope; tests stay isolated.

## `a11y` — integrate axe-core or Playwright a11y checks to auto-detect WCAG violations

**VERIFY**: axe-core paired with Intelligent Guided Tests — NEVER sign off "a11y covered" from automation alone (axe ceiling ≈57% of WCAG); keyboard-navigation flow exercised; each finding cites the WCAG criterion.

## `visual` — screenshot diff with baseline management and diff-report config

**VERIFY**: dynamic regions masked at source (timestamps / prices / IDs) — pixel thresholds NOT raised to silence diffs; percent threshold for responsive layouts vs pixel threshold for high-precision components; visual-regression tier chosen deliberately (pixel / perceptual / Visual AI); 1–2px blur for anti-aliasing before touching numeric threshold.

## `api` — user-journey E2E through API-only (no UI)

Use `APIRequestContext` to chain HTTP → persisted state → downstream-API assertion in one flow. Always include ≥1 cross-endpoint state check (e.g. POST `/orders` → GET `/orders/:id` → GET `/inventory` must agree). Define mock-vs-real backend toggle at PLAN (env-driven); pin real backend for critical-path smoke. Follow up with Gateway/contract-test handoff when schema drift risk is high. Distinct from Radar `integration` (backend internals) and Probe `api` (security DAST).

**VERIFY**: ≥1 cross-endpoint state check present (POST→GET→downstream agree); mock-vs-real backend toggle defined at PLAN; real backend pinned for critical-path smoke; contract-test handoff queued when schema-drift risk is high; stays journey-level (backend internals → Radar, security DAST → Probe).

## `mobile` — E2E for a shipped app (not PoC)

Detox for RN grey-box, Maestro for cross-platform smoke (lowest authoring cost), Appium for widest device matrix; route through a device farm once ≥3 device combos. Distinct from Forge `mobile` (PoC) and Native (production build). Real-device flake dominates — quarantine device-specific noise separately from logic flake.

**VERIFY**: PR gate runs smoke only on 1 sim + 1 emu (full matrix NEVER on PRs → nightly); release gated on real devices for oldest + newest supported OS per platform; accessibility-id locators used; device-specific flake quarantined separately from logic flake (two-axis taxonomy).

## `component` — component tests in a real browser

Real DOM/events/CSS — distinct from Radar `unit` (Node/jsdom). Playwright CT for Playwright-native stacks, Cypress CT when project uses Cypress, Storybook Interactions (`play` + `@storybook/test`) when stories are the source of truth. If Vitrine owns stories, execute against them rather than duplicating mount setup. Scope each test to one component — page-level belongs in `playwright`.

**VERIFY**: runs in a real browser (real DOM/events/CSS — not jsdom); each test scoped to ONE component (page-level → `playwright`); executes against Vitrine-owned stories rather than duplicating mount setup when stories exist.
