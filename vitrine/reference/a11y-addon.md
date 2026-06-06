# Storybook a11y Addon

## Purpose

Storybook's `@storybook/addon-a11y` runs axe-core on every story, surfacing WCAG violations during development. Wired correctly, it catches the cheapest a11y failures (contrast, missing labels, role mismatch) before they ship. Wired carelessly, it floods the panel with false positives and gets disabled.

## Scope Boundary

- IN scope: addon-a11y configuration, per-story rules, CI failure thresholds, role-aware keyboard testing in stories, axe-core rule selection.
- OUT of scope: full WCAG 2.2 audit (delegate to `palette` `a11y` subcommand or `canon`), production-runtime a11y (`palette`), screen-reader testing (manual), color-token contrast design (`muse`), legal compliance (`oath` / `clause`), focus animation (`flow`).

## Core Concepts

### What addon-a11y Catches (and Doesn't)

axe-core is **deterministic static analysis**: it catches what HTML and computed styles can reveal.

| Catches | Misses |
|---------|--------|
| Color contrast (computed) | Visual hierarchy issues |
| Missing alt / aria-label | Whether alt text is *meaningful* |
| ARIA role mismatch | Whether keyboard order makes *sense* |
| Missing form labels | Whether error messages are *helpful* |
| Heading order skips | Whether semantic structure is *useful* |
| Tab index issues | Whether focus is *trapped properly* |
| Landmark structure | Whether layout works for screen readers |

A clean axe report is a **floor**, not a ceiling. Pair with manual screen-reader testing for full coverage.

### Installation (Storybook 8.x / 9.x / 10.x)

```bash
pnpm add -D @storybook/addon-a11y
```

Add to `.storybook/main.ts`:

```ts
export default {
  addons: [
    // ...other addons
    '@storybook/addon-a11y',
  ],
};
```

Storybook 9+ ships with addon-vitest integration; addon-a11y can run as part of Test Runner.

### Per-Story Configuration

Default: every story is checked.

Override per story or component via `parameters.a11y`:

```ts
// Disable for a specific story (justify in comment)
export const Decorative: Story = {
  parameters: {
    a11y: { disable: true }, // pure decoration; no semantic content
  },
};

// Custom rule set per story
export const ColorContrast: Story = {
  parameters: {
    a11y: {
      config: {
        rules: [
          { id: 'color-contrast', enabled: true },
          { id: 'aria-allowed-attr', enabled: false },
        ],
      },
    },
  },
};

// Element-level test target
export const Modal: Story = {
  parameters: {
    a11y: {
      element: '[role="dialog"]',
    },
  },
};
```

### Global Configuration

`.storybook/preview.ts`:

```ts
import type { Preview } from '@storybook/react';

const preview: Preview = {
  parameters: {
    a11y: {
      // axe-core configuration
      config: {
        rules: [
          { id: 'color-contrast', enabled: true },
          { id: 'region', enabled: false }, // landmark not relevant in component context
        ],
      },
      options: {
        runOnly: {
          type: 'tag',
          values: ['wcag2a', 'wcag2aa', 'wcag22aa'], // 2026 default
        },
      },
    },
  },
};

export default preview;
```

### Common Rule Tweaks

| Rule | Default | When to disable | Note |
|------|---------|-----------------|------|
| `region` | enabled | Component-isolated stories — landmarks belong on the page | Re-enable for full-page stories |
| `page-has-heading-one` | enabled | Component stories | Re-enable for page stories |
| `landmark-one-main` | enabled | Component stories | Re-enable for page stories |
| `color-contrast` | enabled | Never disable globally | Per-story disable only with token-rationale |
| `aria-required-parent` | enabled | Stand-alone child component (e.g., MenuItem alone) | Document the parent context |
| `aria-allowed-attr` | enabled | Custom-component temporary phase | Track in a remediation issue |

### CI Integration with Test Runner

Storybook 8.4+ provides `@storybook/test-runner` which can run a11y checks in CI:

```bash
pnpm add -D @storybook/test-runner @axe-core/playwright
```

`.storybook/test-runner.ts`:

```ts
import { getStoryContext } from '@storybook/test-runner';
import { injectAxe, checkA11y } from 'axe-playwright';

export default {
  async preVisit(page) {
    await injectAxe(page);
  },
  async postVisit(page, context) {
    const storyContext = await getStoryContext(page, context);
    if (storyContext.parameters?.a11y?.disable) return;

    await checkA11y(page, '#storybook-root', {
      detailedReport: true,
      detailedReportOptions: { html: true },
      axeOptions: storyContext.parameters?.a11y?.config,
    });
  },
};
```

CI command:

```bash
pnpm test-storybook --ci
```

### Failure Thresholds

| Strategy | When |
|----------|------|
| Fail on any violation | Strict; ideal for new projects starting clean |
| Fail on critical / serious only | Existing projects with backlog |
| Warn-only mode | Migration phase; track in Slack / Discord report |
| Allowlist with expiry | Specific known-issues with date for resolution |

For an existing codebase, **start with critical-only**, ratchet to "any" over 3-6 months. Failing-the-build-on-everything from day 1 produces flag fatigue and gets disabled.

### Severity Calibration

axe rule severities:

| Severity | Examples |
|----------|----------|
| Critical | Image without alt; no keyboard access |
| Serious | Color contrast fail; ARIA mismatch |
| Moderate | Heading skip; landmark issue |
| Minor | Best-practice deviations |

Map to CI: critical / serious always block; moderate warns; minor logs.

### Interaction Test + a11y

Combine `play` functions with a11y to test keyboard / focus flow:

```ts
import { userEvent, within } from '@storybook/test';
import { expect } from '@storybook/jest';

export const KeyboardOpen: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const trigger = canvas.getByRole('button', { name: 'Open' });
    await userEvent.tab();
    expect(trigger).toHaveFocus();
    await userEvent.keyboard('{Enter}');
    expect(canvas.getByRole('dialog')).toBeVisible();
  },
};
```

This catches role / keyboard issues that static axe analysis misses.

### Anti-Pattern: The "Just Disable It" Trap

When a rule fails, the temptation is `parameters: { a11y: { disable: true } }`. Resist:

| Wrong response | Right response |
|----------------|----------------|
| Disable globally | Disable on one story with rationale comment |
| Disable forever | Open issue, set 30-day expiry |
| Disable because "stylesheet bug" | Fix the stylesheet |
| Disable region rule everywhere | Disable only for component-isolated stories |
| Disable color-contrast | Never; it's the highest-value catch |

Document every disable with a one-line `// reason:` comment.

### Reporting

Useful CI outputs:

| Format | Use |
|--------|-----|
| GitHub Actions annotation | Per-story PR comment |
| HTML report (axe-html-reporter) | Detailed shareable report |
| JSON | Dashboards / time-series |
| Slack notification | Daily summary |
| Storybook Composition | Aggregate across multi-repo monorepos |

### Storybook 10 + addon-mcp

Storybook 10's `addon-mcp` enables AI agents to read story states and a11y findings programmatically — a future direction for AI-assisted a11y triage.

### Multi-Story Component Patterns

For components with many states (Button-default, Button-disabled, Button-loading, etc.):

| Pattern | Recommendation |
|---------|---------------|
| One story per state | Each state runs a11y; catch state-specific issues |
| Story-as-state-machine | Use args; toggle to test each state |
| Decorator-based theme switching | Run a11y per theme variant (light + dark) |

### Dark-Mode Coverage

Color contrast rules run against the rendered theme. Ensure stories cover:

| Variant | Coverage |
|---------|----------|
| Light theme | Default story |
| Dark theme | Decorator-overridden duplicate or theme switcher |
| High-contrast | Optional but valuable for compliance projects |

A component that passes light-mode contrast may fail dark-mode contrast.

## Workflow

1. **Install addon-a11y** in Storybook config.
2. **Set global rules** in `preview.ts` — wcag2aa or wcag22aa default.
3. **Audit existing stories** — count violations, severity-binned.
4. **Define disable policy** — per-story rationale required; expiry dates.
5. **Configure test-runner** for CI a11y checks.
6. **Set CI threshold** — start critical-only; ratchet over months.
7. **Add interaction tests** for keyboard / focus paths.
8. **Add dark-mode story variants** to catch theme-specific contrast.
9. **Set up reporting** — GitHub annotations + HTML aggregator.
10. **Schedule quarterly review** of disabled rules; clear expired exceptions.

## Output Template

```yaml
a11y_addon_setup:
  storybook_version: 10.3.3
  addon_a11y_version: 9.x_compatible
  global_config:
    rule_set: wcag22aa
    disabled_globally: [region, page-has-heading-one, landmark-one-main]
    disable_rationale: component_isolated_stories
  ci:
    runner: storybook_test_runner
    threshold: critical_serious_block
    moderate: warn
    minor: log
    expiry_for_disables: 30_days
  reporting:
    github_actions_annotations: yes
    html_report: yes
    slack_daily_summary: yes
  story_coverage:
    a11y_run_per_story: 100_pct
    interaction_tests_with_a11y: 35_pct
    dark_mode_variants: 80_pct
  baseline_violations:
    critical: 0
    serious: 12
    moderate: 47
    minor: 88
  remediation_plan:
    critical_serious_resolve_by: 2026_05_15
    moderate_resolve_by: 2026_07_15
  quarterly_review_date: 2026_07_25
```

## Anti-Patterns

- Disabling addon-a11y globally because it's "noisy" — fix the rules instead.
- `parameters.a11y.disable: true` on every story — no a11y signal.
- Color-contrast rule disabled — highest-value rule.
- Test-runner not integrated in CI — local-only checks miss regressions.
- Failing build on minor / moderate from day 1 on existing project — flag fatigue.
- No expiry on disable rationale — disables become permanent.
- Single light-theme story without dark coverage — half the contrast surface untested.
- Component-isolated stories with `region` rule enabled — false positives flood report.
- Ignoring critical / serious in PR comments — they ship.
- No interaction tests — static a11y misses keyboard / focus issues.
- Disabling `aria-allowed-attr` instead of fixing — accumulating debt.
- Storybook 8 with no plan to migrate to 9/10 — addon ecosystem moves on.

## Deliverable Contract

An a11y-addon setup is complete when:

- addon-a11y installed and configured globally.
- Rule set documented (wcag2aa / wcag22aa).
- Disable policy with rationale + expiry documented.
- Test-runner integrated in CI.
- Failure threshold appropriate to project age.
- Dark-mode variants covered.
- Interaction tests for keyboard paths.
- Baseline violation count recorded.
- Remediation plan with dates.
- Quarterly review scheduled.

## References

- W3C WCAG 2.2 (2023) — and ratified ISO/IEC 40500:2025.
- axe-core documentation — github.com/dequelabs/axe-core.
- Storybook docs, *Accessibility addon* — storybook.js.org/docs/writing-tests/accessibility-testing.
- Deque Systems, *Accessibility Maturity Model*.
- WebAIM Million 2025 — accessibility baseline data.
- Storybook 10 release notes (2026) — addon-mcp, addon-vitest, addon-test.
- Marcy Sutton, *Accessibility for Web Designers* (2018; updated talks).
- Lindsey Kopacz, *A11y Project*.
- Adrian Roselli, *Underestimated Obstacles to Better Web Accessibility* — practical guide.
- Storybook + Chromatic blog posts on accessibility-as-test.
- @storybook/test-runner + axe-playwright integration docs.
- Wickerwork / Sentry / Microsoft Fluent — production a11y test harness references.
