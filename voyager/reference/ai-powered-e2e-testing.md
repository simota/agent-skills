# AI-Powered E2E Testing & Playwright MCP/Agents (2026-05)

Purpose: Use this file when Voyager must plan, generate, review, or heal tests with AI assistance.

Contents:
- MCP vs CLI vs Test Agents tradeoffs and token costs
- Planner / Generator / Healer roles
- Browser-agent landscape (Stagehand, Skyvern, Browser-Use, Computer Use, Chrome DevTools MCP)
- Cypress `cy.prompt` parity
- Auth blockers, review gate, adoption ladder, cost metrics

> Stack snapshot (2026-05): Playwright **1.60** (Test Agents 1.56+, screencast / browser.bind 1.59+), `@playwright/cli` Skills mode preferred over MCP for coding agents (~4× cheaper tokens), Cypress **15.15** with `cy.prompt` beta GA in 15.13. Browser-agent space consolidated to five production-grade stacks: **Playwright + Claude, Stagehand v3, Skyvern, Browser-Use, Anthropic Computer Use / OpenAI CUA**. Chrome DevTools MCP is the dominant **observation** plane; Playwright MCP and `playwright-cli` remain the **action** plane.

## AI Delivery Modes for Playwright

| Mode | Version floor | Primary use | Approx tokens / test | Tradeoff |
|------|---------------|-------------|----------------------|----------|
| `@playwright/cli` Skills mode | 1.58+ | Coding-agent integration (Claude Code / Codex / Cursor) at scale | **~27K** | Snapshot-on-disk, agent reads selectively; preferred default in 2026 |
| Playwright MCP | 1.55+ (MCP server v0.0.7x line) | Interactive exploration, autonomous-agent workflows that require the MCP protocol | **~114K** | Highest context quality, highest token + RTT cost |
| Playwright Test Agents (Planner / Generator / Healer) | **1.56+** | Plan → generate → run → heal loops on top of either CLI or MCP | Variable (loop-dependent) | Powerful, but only valuable once auth/locators/fixtures are stable |
| Chrome DevTools MCP | npm `chrome-devtools-mcp` | Debugging / performance / network observation during AI workflows | Variable | Observation-first; limited driving (Puppeteer under the hood) |

Rules of thumb:

- **Default: `@playwright/cli`** when the host is a coding agent. Microsoft's 2026 guidance ([dev.microsoft.com — Complete Playwright End-to-End Story 2026](https://developer.microsoft.com/blog)) treats CLI as the primary path and MCP as the fallback for protocol-bound autonomous workflows.
- **MCP** when the agent runs outside the editor and needs the MCP standard's live streaming.
- **Test Agents** only when the suite already has stable auth, locators, fixtures, and a human review gate.
- **Chrome DevTools MCP** sits *alongside* either path for performance traces, console logs, source-mapped stack traces, and Lighthouse audits.

## MCP Model

The MCP approach routes AI actions through browser tools backed by the accessibility tree instead of brittle DOM selectors.

```typescript
// Brittle DOM-style interaction
await page.click('div.checkout-btn-v3');

// Stable semantic target
// Role: button, Name: "Checkout"
```

Why this matters:
- Better resilience to selector churn
- Lower need for vision-only tooling
- Closer alignment with accessibility-first locator strategy

### MCP Server Options (2026-05)

| Server | Driver | Notes |
|--------|--------|-------|
| **Microsoft Playwright MCP** (`playwright-mcp`) | Playwright | Default official option, accessibility-tree-first. Now published to the official MCP Registry on each release; supports drag-and-drop (`browser_drop`), multi-tab extension mode, and isolated-mode browser-launch serialization. |
| **Chrome DevTools MCP** (`chrome-devtools-mcp`) | Puppeteer | Google's official 29-tool surface for **debugging / performance / network**. Headline tools: `performance_start_trace` / `performance_stop_trace`, Lighthouse audit, CrUX integration, source-mapped console messages, screenshot, network inspection. Pair with Playwright MCP when an agent needs to both act and diagnose. |
| **ExecuteAutomation MCP** | Playwright | Alternative implementation with extra automation primitives. |
| **Midscene.js (v1.0 GA)** | Vision-language model | Pure-vision routing (`aiAct`, `aiQuery`, `aiAssert`, `aiLocate`, `aiWaitFor`); supports Qwen3-VL / Doubao-1.6-vision / Gemini-3-pro / UI-TARS; cross-platform (web, Android, iOS, HarmonyOS, Linux, macOS, Windows). Use when the accessibility tree is unavailable or the target is a non-web canvas. |

> Default routing in 2026: **Playwright MCP for action, Chrome DevTools MCP for observation, Midscene for vision-only canvases**. Reference: [Steve Kinney — Driving vs Debugging the Browser](https://stevekinney.com/writing/driving-vs-debugging-the-browser).

## Playwright Test Agents

### Agent Roles

| Agent | Responsibility | Input | Output |
|-------|----------------|-------|--------|
| Planner | Explore the app and draft a test plan | Natural-language request | Markdown plan in `specs/` |
| Generator | Convert the plan into test code | Markdown plan | TypeScript tests in `tests/` |
| Healer | Attempt to repair a failing test | Failing test plus error context | Updated test code |

### Typical Workflow

```text
1. Plan: npx playwright test --plan "Test the login flow"
   -> generates specs/login.md

2. Generate: npx playwright test --generate
   -> generates tests/login.spec.ts

3. Run: npx playwright test
   -> execute and review the result

4. Heal: npx playwright test --heal
   -> repair and rerun when a failure is reviewable

5. Loop: --loop
   -> repeats plan -> generate -> run -> heal automatically
```

## Primary Blocker: Authentication

Largest adoption blocker:
- AI agents cannot explore behind auth walls without prior setup.
- `storageState` or equivalent auth fixtures must already exist.
- Re-authenticating on every run can trigger rate limits or security alerts.

Required mitigations:
- Save auth state in `auth.setup.ts`.
- Centralize auth in `globalSetup`.
- Prefer dedicated test-only auth tokens or accounts.

## Review Rules for AI-Generated Tests

### Unresolved Risks

| Risk | Effect | Required control |
|------|--------|------------------|
| Test explosion | CI cost grows faster than value | Tagging and pruning |
| Weak business assertions | Tests verify rendering but not correctness | Human-defined acceptance criteria |
| Architecture drift | Duplicated helpers, mixed locator styles, weak assertions | Mandatory human review |
| Debug hallucination | Wrong root-cause explanations sound plausible | Human validation of evidence |
| Stateful workflow complexity | Permissions, onboarding, and multi-step flows are mis-modeled | Human-designed plan plus AI assistance |

### AI Test Review Checklist

```markdown
## AI-Generated E2E Test Review

### Required checks
- [ ] Do assertions verify business behavior?
- [ ] Can the test run independently?
- [ ] Do selectors use `getByRole`, `getByLabel`, or `getByTestId`?
- [ ] Does the test avoid `waitForTimeout()`?
- [ ] Does the test name describe user behavior?

### Architecture checks
- [ ] Does the test follow the existing Page Object Model?
- [ ] Does it reuse existing helpers and fixtures?
- [ ] Is the locator strategy consistent with the suite?
- [ ] Is test data created through APIs or factories?
```

## Team-Based AI Testing

Parallel AI roles work when responsibilities are explicit and routed to the right surface:
- **Functional agent** — happy-path verification through Playwright MCP / `@playwright/cli` (action plane).
- **Accessibility agent** — WCAG checks via axe-core + Intelligent Guided Tests. Acknowledge the ~57% automation ceiling (Deque); do not let an AI agent claim "a11y covered" from automation alone.
- **Performance agent** — Core Web Vitals + Lighthouse via **Chrome DevTools MCP** `performance_start_trace` / `performance_stop_trace` (observation plane).
- **Visual regression agent** — Applitools / App Percy / Chromatic. Pick by tier: pixel-diff (icons), perceptual (Storybook stories), visual AI (complex layouts).
- **Browser-agent for cross-site or RPA-shaped journeys** — Stagehand v3 / Skyvern / Browser-Use, with Browserbase or Anchor Browser as the cloud sandbox.
- **Security probing** is *not* a Voyager role — route to Sentinel / Probe / Vigil. Do not embed security payloads in functional tests.

### Self-Healing Tool Comparison (2026-05)

| Tool | Approach | LLM integration | Notes |
|------|----------|-----------------|-------|
| **Octomind** | Source-level healing (rewrites the Playwright selector and commits the fix back to the repo) | LLM-powered crawl + auto-fix | Discovers tests by exploring the running app; vendor-reported ~78% false-positive reduction and up to 83% maintenance cut on large SaaS suites. Ships an MCP server for agentic loops. |
| **Momentic** | Intent-based locators resolved at each run; layout / context / purpose understanding | Proprietary | Tests live inside the platform — **cannot be exported as code**. Broader multi-layer scope (API / a11y) than Octomind. Lock-in tradeoff. |
| **Midscene.js (v1.0)** | Pure-vision routing on screenshots | Vision-language models (Qwen3-VL, Doubao-1.6, Gemini-3-pro, UI-TARS) | `aiAct` / `aiQuery` / `aiAssert` / `aiLocate` / `aiWaitFor`. Survives full framework migrations. Best fit for canvas / non-DOM surfaces and cross-platform (web + native). |
| **ZeroStep** | Natural-language helper inside Playwright | OpenAI GPT-4 family | Drop-in `ai('click the login button')` for existing Playwright tests. Still active; lower ceiling than full agents but minimal adoption cost. |
| **Cypress `cy.prompt`** | Natural-language step → generated Cypress commands; self-heals selectors on re-run | Cypress Cloud-managed LLM | Beta GA in Cypress 15.13 (2026-03). Auto-regenerates broken steps; pair with UI Coverage Test Generation to close gaps. See `cypress-guide.md`. |
| **Stagehand v3** (Browserbase) | Four primitives (`act` / `extract` / `observe` / `agent`) + CDP-direct driver | Provider-agnostic (Claude, GPT, etc.) | Auto-caches discovered elements / actions (zero LLM calls when cached). v3 is ~44% faster than v2 on iframe / shadow-root flows. Pairs with Browserbase cloud for session replay, CAPTCHAs, agent identity. |
| **Skyvern** | LLM + computer vision over a Playwright-compatible SDK | Claude Sonnet 4 / GPT-4o | Strongest WRITE-task agent (forms, logins, downloads). Bundled CAPTCHA / Cloudflare handling, credential vault, OCR document pipeline. SOC2 Type II, HIPAA. Use when the workload is RPA-shaped. |
| **Browser-Use** | Open-source LLM-to-browser harness | Provider-agnostic (OpenAI, Google, Ollama, etc.) | 78K+ GitHub stars. Reported 89.1% on WebVoyager (586 tasks) — top of the open category as of 2026. Self-healing wrapper; CAPTCHA + 195-country proxy options. |
| **Anthropic Computer Use** | Screenshot + cursor / keyboard control via the Claude API or Claude Code Q1 2026 integration | Claude (Sonnet 4 / Opus 4.7) | GA contract is the API tool + Cowork / Claude Code desktop. Use for cross-app journeys that exit the browser (file system, native dialogs). Pair with prompt-injection scanning. |
| **OpenAI CUA** | Computer-Using Agent (Operator successor) | OpenAI o-series | The OpenAI peer of Computer Use; one of the five production-grade browser-agent stacks recognised in 2026. |
| **Octomind / Stagehand / Skyvern MCP servers** | Same products exposed as MCP tools | — | Use when the agent host (Claude Code, Cursor) already speaks MCP. |

> Retired or de-emphasised in 2026 vs the 2025 list: **Testim** and **Katalon Studio 11** are no longer load-bearing in this comparison — both still exist commercially but have been displaced by Stagehand / Skyvern / Browser-Use / cy.prompt for new projects. Voyager keeps them in scope only when the project already runs them.

### LLM-Generated Test Accuracy (2026 industry benchmarks)

| Metric | Value | Source |
|--------|-------|--------|
| Browser-Use WebVoyager success (586 tasks, open-source category) | **~89.1%** | Browser-Use GitHub / nohacks.co 2026 landscape |
| Skyvern WRITE-task accuracy (forms, logins, downloads) | Strongest in category (vendor-reported) | skyvern.com |
| Octomind source-level healing — false-positive reduction | **~78%** | octomind.dev |
| Stagehand v3 latency improvement vs v2 on iframe / shadow-root | **~44.1%** faster | browserbase.com — Stagehand v3 launch |
| Tests requiring manual correction (general industry, 2026) | ~10% | aggregate (Currents 2026 / Bug0) |

> These figures vary significantly by app complexity, auth complexity, and selector strategy. Treat as directional, not absolute. WebVoyager / SeeAct benchmarks are now the de facto comparators.

Commercial platforms still relevant in 2026: **Octomind, Momentic, Stagehand / Browserbase, Skyvern, Browser-Use, Currents, Bug0, Applitools, App Percy, testRigor, Mabl, MaestroGPT**. Pick by *workflow shape*, not by feature list — see selection guide below.

### Picking the right AI testing surface

- Existing Playwright suite + coding-agent host (Claude Code / Codex / Cursor) → **`@playwright/cli` Skills mode**, escalate to Test Agents (1.56+) for plan→generate→heal loops.
- Existing Cypress suite + non-engineer authors → **`cy.prompt` (Cypress 15.13+)**.
- Pure browser-agent product (no test repo) reaching across many sites → **Stagehand v3** (developer-first) or **Browser-Use** (open-source) on **Browserbase** for cloud sessions.
- RPA-shaped workflow (form-filling, document downloads, CAPTCHAs, credential vault) → **Skyvern**.
- Cross-app journeys that leave the browser → **Anthropic Computer Use** or **OpenAI CUA**.
- Canvas / non-DOM / cross-platform native targets → **Midscene.js** (or MaestroGPT for mobile only; see `mobile-testing.md`).
- Self-healing applied to an existing Playwright repo without rewriting → **Octomind** (source-level fix) or **ZeroStep** (drop-in helper).
- Observation / debugging / performance during AI runs → **Chrome DevTools MCP** alongside whichever action layer is in use.

## Adoption Roadmap (2026)

| Phase | Action | Tooling | Risk |
|-------|--------|---------|------|
| Phase 1: Foundations | Standardise on `getByRole` / `getByLabel` / `getByTestId`, stabilise `playwright.config.ts` or `cypress.config.ts`, lock auth via `storageState` / `cy.session` | Playwright 1.59+ or Cypress 15.10+ | Low |
| Phase 2: CLI-assisted exploration | Drive Playwright via `@playwright/cli` Skills mode (or Cypress Studio + ElementSelector) from the coding agent; review every generated step | `@playwright/cli`, Studio | Low–Medium |
| Phase 3: Planner / Generator (or `cy.prompt`) | Let the agent emit Markdown plans (`specs/`) and codegen specs (`tests/`); human-review each spec before merging | Playwright Test Agents 1.56+, `cy.prompt` 15.13+ | Medium |
| Phase 4: Healer integration | Enable controlled auto-repair on a quarantined tier; require a human merge for any commit the Healer / Octomind / Stagehand auto-cache rewrites | Playwright `--heal`, Octomind auto-fix, Stagehand v3 cache | Medium–High |
| Phase 5: Full loop | `playwright test --loop` or equivalent agent loop; only on suites that already met phases 1-4 metrics | Playwright `--loop`, Stagehand `agent`, Skyvern workflows | High |

Rule: do not jump to phase 5 before the suite already has stable auth, selectors, data strategy, screencast / video receipts, and a review gate. Track flake rate, token spend, and self-heal rewrite volume as gating metrics between phases.

## Cost Metrics

Track:
- Token cost per generated or repaired test
- Monthly AI test spend
- Human review time
- Flaky rate and false-positive rate

Sources (2026 refresh):

- [Playwright Release Notes (1.56–1.60)](https://playwright.dev/docs/release-notes)
- [Currents: State of Playwright AI Ecosystem 2026](https://currents.dev/posts/state-of-playwright-ai-ecosystem-in-2026)
- [Microsoft Developer Blog — Complete Playwright End-to-End Story 2026](https://developer.microsoft.com/blog) (CLI > MCP token recommendation)
- [Steve Kinney — Driving vs Debugging the Browser (Playwright MCP vs Chrome DevTools MCP)](https://stevekinney.com/writing/driving-vs-debugging-the-browser)
- [Chrome DevTools MCP — Chrome for Developers](https://developer.chrome.com/blog/chrome-devtools-mcp)
- [Browserbase — Stagehand v3 launch](https://www.browserbase.com/blog/stagehand-v3)
- [Skyvern — Browser Automation Platform](https://www.skyvern.com/)
- [Browser-Use — GitHub](https://github.com/browser-use/browser-use)
- [Anthropic — Computer Use Tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- [Cypress — `cy.prompt` general launch](https://www.cypress.io/blog/cy-prompt-experimental-launch) · [Cypress AI Features](https://docs.cypress.io/cloud/features/cypress-ai-features)
- [Octomind — Playwright self-healing](https://octomind.dev/product/playwright-self-healing/)
- [Midscene.js v1.0](https://midscenejs.com/introduction)
- [TestDino — Playwright 1.59 Release Notes](https://testdino.com/blog/playwright-release-guide)
- [BrowserStack: Playwright AI Test Generator](https://www.browserstack.com/guide/playwright-ai-test-generator)

---

## Native Mobile AI Testing (2025-2026)

The visual-AI / self-healing tooling that grew up around web E2E now ships native-mobile coverage. Use this section when the artifact is `.ipa`/`.apk`/`.aab` and AI assistance is in scope.

### Tool selection

| Tool | Native mobile coverage | What it does | Watch for | Source |
|------|-----------------------|--------------|-----------|--------|
| **Applitools Eyes 10.22** (2026-01) | iOS + Android native via SDKs; Storybook addon and Figma plugin shipped 2026-01 | Visual AI ignores sub-pixel / anti-aliasing / font-rendering noise; "would a human notice" matching modes (strict / layout / content) | Per-checkpoint cost; needs deterministic data to be valuable | <https://percy.io/blog/visual-regression-testing-tools> · <https://aitestingguide.com/applitools-vs-percy/> |
| **App Percy** (BrowserStack) | iOS + Android real-device visual regression; bundled with App Automate | Runs visual checks on thousands of real devices via the same farm; 2026 added the **Visual Review Agent** that summarises diffs in natural language | Lock-in to BrowserStack; fewer match modes than Applitools | <https://percy.io/blog/app-visual-testing> · <https://aitestingguide.com/applitools-vs-percy/> |
| **testRigor** | iOS + Android native + hybrid; plain-English specs | Vision AI + NLP identifies elements the way a human does (look + meaning), not via DOM/locators — survives full framework migrations | Generative test bloat if not tagged/pruned; verify business assertions, not just rendering | <https://testrigor.com/> · <https://testrigor.com/alternative/mabl/> |
| **Mabl** | Mobile web + native via SDK | Probabilistic learning model accumulates execution history per app; locator self-heal updates without fixed rules | Self-heal can mask regressions if review gate is weak | <https://www.mabl.com/> · <https://www.virtuosoqa.com/post/best-ai-testing-tools> |
| **MaestroGPT / Maestro AI test analysis** | Mobile only (Maestro flows) | LLM-powered failure summary that goes beyond pass/fail; AI-assisted command synthesis inside Maestro Studio | Cloud-only; LLM hallucination on root-cause requires human validation | <https://docs.maestro.dev/maestro-flows/workspace-management/ai-test-analysis> |

### When to choose what

- **Visual regression on a real-device matrix** → App Percy if you are already on BrowserStack; Applitools Eyes when you need richer match modes or design-side Figma comparison.
- **Plain-English authoring on iOS + Android by non-engineers** → testRigor; verify business assertions during review.
- **Self-healing with low ceremony on existing native suites** → Mabl.
- **AI assistance inside an existing Maestro flow set** → MaestroGPT / Maestro AI test analysis. Lowest authoring friction when Maestro is already adopted.

### Review gate for native AI tests

Same as the web review checklist above, plus mobile-specific:
- [ ] Locator strategy is `accessibilityIdentifier` / `testID` / `contentDescription` — not text on a localized screen.
- [ ] Visual diffs mask **dynamic regions** (timestamps, signal bars, battery, push banners) before adjusting numeric thresholds.
- [ ] Self-heal events are surfaced in the report so silent regressions cannot ride along.
- [ ] AI-suggested tests respect the two-axis flake taxonomy (logic vs device) — see `mobile-testing.md`.
