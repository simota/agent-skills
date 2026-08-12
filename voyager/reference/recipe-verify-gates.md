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


## Per-Recipe Behavior (SKILL.md excerpt)

Behavior notes per Recipe (full VERIFY gate detail in `reference/recipe-verify-gates.md`) — each gate applies **in addition to** Voyager's universal discipline (accessible selectors first, POM by user intent, zero fixed-delay waits, fresh context per test, risk tags, never modify app code — report/hand off).
- `playwright`: full Playwright E2E suite. VERIFY: accessible selectors primary, zero fixed-delay waits, fresh context per test, risk tag applied, budgets held.
- `page-object`: POM classes from existing tests/specs. VERIFY: modeled around user intent (not DOM), no god-object (≥50 methods → split), zero CSS-class/positional primary selectors.
- `auth`: login/OAuth/MFA flows via `storageState`. VERIFY: auth reused not re-driven per test, zero hard-coded credentials, setup never skipped, tests isolated.
- `a11y`: axe-core / Playwright a11y checks. VERIFY: paired with Intelligent Guided Tests (axe ceiling ≈57% WCAG — never "covered" from automation alone), keyboard flow exercised, findings cite WCAG criterion.
- `visual`: screenshot diff + baseline management. VERIFY: dynamic regions masked at source (not threshold-raised), tier (pixel/perceptual/Visual AI) chosen deliberately, anti-aliasing blur before threshold changes.
- `api`: API-only journey via `APIRequestContext`. VERIFY: ≥1 cross-endpoint state check, mock-vs-real toggle defined at PLAN, real backend pinned for critical-path smoke, stays journey-level (backend internals → Radar, DAST → Probe).
- `mobile`: shipped-app E2E (Detox/Maestro/Appium, device farm at ≥3 combos). VERIFY: PR gate = 1 sim + 1 emu only (full matrix → nightly), release gated on oldest+newest OS per platform, accessibility-id locators, device flake quarantined from logic flake.
- `component`: real-browser component tests (not jsdom). VERIFY: one component per test (page-level → `playwright`), executes against Vitrine-owned stories when they exist.

### Signal Keywords → Recipe

For natural-language input without an explicit subcommand. Subcommand match wins if both apply. See `## Reference Map` for the file pointer associated with each Recipe.

| Keywords | Recipe |
|----------|--------|
| `playwright`, `e2e`, `browser test`, `journey test` | `playwright` |
| `cypress`, `cy.` | `playwright` (Cypress branch — read `cypress-guide.md`) |
| `visual regression`, `screenshot`, `pixel diff` | `visual` |
| `accessibility`, `a11y`, `axe`, `WCAG` | `a11y` |
| `auth flow`, `login test`, `session` | `auth` |
| `CI`, `pipeline`, `sharding`, `parallel` | `playwright` (CI scope — read `ci-reporting.md`) |
| `flaky`, `flake`, `retry`, `instability` | `playwright` (flake diagnosis — read `debug-monitoring.md`) |
| `mobile emulation`, `mobile viewport`, `responsive E2E`, `PWA mobile` | `playwright` (mobile emulation — read `mobile-testing.md`) |
| `native mobile E2E`, `appium`, `detox`, `maestro`, `xcuitest`, `espresso`, `.ipa`, `.apk`, `.aab` | `mobile` |
| `device farm`, `browserstack app automate`, `app percy`, `sauce labs real device`, `aws device farm`, `firebase test lab`, `lambdatest`, `hyperexecute`, `testmu ai`, `real device`, `parallel session`, `cloud session`, `remote webdriver`, `appium server`, `appium 3`, `webdriver bidi` | `mobile` (device-farm tier — read `cloud-testing.md` + `mobile-testing.md`) |
| `foldable`, `galaxy z fold`, `pixel fold`, `window size class`, `compact medium expanded`, `stage manager`, `split view`, `multi-window`, `posture` | `mobile` (adaptive/foldable — read `mobile-testing.md`) |
| `privacy manifest`, `PrivacyInfo.xcprivacy`, `required reason api`, `tracking domain`, `privacy sandbox`, `data access auditing` | `mobile` (privacy-aware — read `mobile-testing.md`) |
| `applitools`, `app percy`, `testrigor`, `mabl`, `native visual ai`, `self-healing mobile`, `vision ai`, `maestro ai` | `visual` / `mobile` (native visual AI — read `ai-powered-e2e-testing.md` + `mobile-testing.md`) |
| `container`, `testcontainers`, `docker test` | `playwright` (container — read `container-testing.md`) |
| `web component`, `shadow DOM`, `lit`, `stencil` | `component` (read `web-component-testing.md`) |
| `AI test`, `MCP`, `self-healing`, `codegen`, `playwright cli` | `playwright` (AI lifecycle — read `ai-powered-e2e-testing.md`) |
| `screencast`, `video receipt`, `visual proof`, `recording` | `playwright` (screencast — read `ai-powered-e2e-testing.md`) |
| `API test`, `request context`, `backend verify` | `api` |
| complex multi-agent task | Hand off to Nexus per `_common/BOUNDARIES.md` |
| unclear request | Default `playwright`; clarify via `framework-selection.md` |

### Handoff Thresholds

Operational thresholds that trigger a recipe choice or a cross-agent handoff (distinct from per-recipe behavior, which is documented under `## Subcommand Dispatch`):

- For shipped mobile apps: never run the full device matrix on PRs — keep PR gate on 1 sim + 1 emu (smoke only), push the matrix to nightly, gate releases on real devices for oldest + newest supported OS per platform.
- If E2E flake rate exceeds 10%, prioritize flake stabilization before adding new tests.
- If suite duration exceeds 10 min, investigate sharding, parallelization, or test pruning before scaling further.
- If coverage is `<80%` or the issue belongs lower in the test pyramid, hand off to `Radar`.
- If flake or regression root cause may be outside the test suite, hand off to `Scout`.
- If CI pipeline ownership, secrets, or general infra becomes the main work, hand off to `Gear`; Voyager owns only E2E-specific test config.
- If measured browser performance regressions need code fixes, hand off to `Bolt` after capturing metrics and evidence.
- If load, chaos, or resilience testing is required, hand off to `Siege`.
- If the request is interactive browser operation, not reusable E2E automation, hand off to `Vector`.
- If the request matches another agent's primary role, route to that agent per `_common/BOUNDARIES.md`.

