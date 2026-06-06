# Story Coverage

## Purpose

A component without a story is invisible to designers, untested for visual regression, and unfindable in the catalog. Story coverage is the percentage of components that have at least one story; advanced metrics include state coverage, prop-permutation coverage, and viewport coverage. This reference defines metrics, tooling, and CI gates.

## Scope Boundary

- IN scope: story-coverage metrics, addon-coverage / addon-test (Storybook 9+), CI gates, gap reporting, naming conventions, state vs prop coverage, viewport coverage.
- OUT of scope: code coverage (use `radar` / Vitest / Jest), test coverage as code unit tests (separate domain), generic Storybook patterns (`story` / `catalog`), visual regression methodology (`vrt`), Chromatic-specific (`chromatic`).

## Core Concepts

### Coverage Levels

| Level | Definition | Target |
|-------|-----------|--------|
| L1 — File coverage | % components that have a `.stories.*` file | 95%+ |
| L2 — State coverage | % component states represented (default, disabled, loading, error) | 80%+ |
| L3 — Prop-permutation coverage | % distinct prop combos with stories | 50%+ for combinatorially relevant components |
| L4 — Viewport coverage | % stories run at multiple viewports | 70%+ for layout-sensitive components |
| L5 — Theme coverage | % stories run at light + dark | 90%+ for design-system projects |

L1 is the baseline; L2-L5 are progressive maturity.

### Storybook 9+ Built-in Coverage

Storybook 9 introduced `addon-coverage` reports during local dev:

```bash
pnpm add -D @storybook/addon-coverage
```

`.storybook/main.ts`:

```ts
export default {
  addons: ['@storybook/addon-coverage'],
};
```

Reports per-component which stories exist; flags missing.

### addon-test (Storybook 9+)

`@storybook/addon-test` integrates Vitest for story testing — including coverage.

```bash
pnpm add -D @storybook/addon-test vitest
```

Configuration:

```ts
// .storybook/main.ts
export default {
  addons: ['@storybook/addon-test'],
};

// vitest.config.ts
import { defineWorkspace } from 'vitest/config';
export default defineWorkspace([
  {
    extends: 'vite.config.ts',
    plugins: [storybookTest({ configDir: '.storybook' })],
    test: {
      browser: { enabled: true, name: 'chromium' },
    },
  },
]);
```

Vitest then runs every story as a test, producing coverage reports.

### Manual Story Coverage Audit

For projects without addon-coverage:

```sh
# List components without stories
comm -23 \
  <(find src/components -name '*.tsx' | sed 's/\.tsx$//' | sort) \
  <(find src/components -name '*.stories.*' | sed 's/\.stories\..*//' | sort)
```

Or scripted with package.json:

```json
{
  "scripts": {
    "stories:coverage": "node scripts/check-stories.js"
  }
}
```

Where `scripts/check-stories.js` enumerates components and reports missing.

### State Coverage Definition

| Component | Required states |
|-----------|----------------|
| Button | default, hover, active, focus, disabled, loading |
| Input | empty, filled, focus, error, disabled, readonly |
| Modal | open, closing, with-content, scrollable |
| Card | default, with-image, with-actions, loading, empty |
| List | empty, single-item, many-items, loading, error |
| Form | pristine, dirty, validating, submitted, error |

State coverage requires explicit story-per-state, not args toggling alone.

### Prop-Permutation Coverage

For components with combinatorial props (e.g., size × variant × color), full permutation is impractical. Strategy:

| Approach | When |
|----------|------|
| Pairwise / orthogonal | Combinatorial reduction (PICT, all-pairs); covers 80% defects with 20% tests |
| State-machine | Define legal combinations; cover each |
| Equivalence classes | Group equivalent props (size: sm/md/lg; cover one per class) |
| Args matrix story | Single story with `argTypes.matrix` to render all combos |
| Visual regression specifically | Cover at least default + 1-2 variant axes |

For a Button with size (3) × variant (4) × color (3) = 36 combos:
- Pairwise: 12 stories.
- Equivalence classes: 4 stories.
- Args matrix: 1 story rendering all 36.

### Viewport Coverage

Layout-sensitive components benefit from viewport stories:

```ts
export const Mobile: Story = {
  parameters: { viewport: { defaultViewport: 'mobile1' } },
};

export const Tablet: Story = {
  parameters: { viewport: { defaultViewport: 'tablet' } },
};

export const Desktop: Story = {
  parameters: { viewport: { defaultViewport: 'desktop' } },
};
```

Or use `addon-viewport` decorator to apply viewport switching globally.

### Coverage Targets by Project Stage

| Stage | L1 | L2 | L3 | L4 | L5 |
|-------|-----|-----|-----|-----|-----|
| MVP | 60% | 30% | 10% | 0% | 0% |
| Growth | 80% | 60% | 30% | 30% | 50% |
| Mature | 95% | 80% | 50% | 70% | 90% |
| Design system | 100% | 95% | 80% | 90% | 100% |

Setting overly aggressive targets early creates story-noise (1-line stories with no variant); targets should escalate with team / catalog maturity.

### CI Gates

Three gate strategies:

| Gate | Behavior |
|------|----------|
| Block PR if L1 drops below threshold | New components must have stories |
| Warn-only on L1 drop | Soft enforcement |
| Time-decay | Tolerate gaps for 30 days, then block |

GitHub Actions example:

```yaml
- name: Story coverage
  run: pnpm stories:coverage
- name: Comment coverage
  uses: actions/github-script@v7
  with:
    script: |
      const cov = require('./coverage/stories.json');
      if (cov.l1 < 95) {
        core.setFailed(`Story coverage L1 ${cov.l1}% below threshold 95%`);
      }
```

### Gap Report Format

```
Story Coverage Report
=====================
L1 (file coverage):  87% (153/176)
L2 (state coverage):  62%
L3 (prop combinations): 34%
L4 (viewport):  41%
L5 (theme):  72%

Missing stories (23 components):
  - src/components/AsyncBoundary.tsx
  - src/components/CalloutGroup.tsx
  - src/components/DateRangePicker.tsx
  ...

Missing critical states:
  - Button (no error state)
  - Input (no readonly state)
  - Modal (no closing transition)
  ...

Trend (last 30 days):
  L1: 84% → 87% (+3%)
  L2: 58% → 62% (+4%)
```

### Story Quality vs Coverage

100% coverage with 1-line trivial stories is worse than 80% with rich stories. Quality dimensions:

| Dimension | Check |
|-----------|-------|
| Args set | Each story has meaningful args, not defaults only |
| Description | Story describes the use-case in 1 line |
| Play function | Interaction stories have `play` |
| Realistic data | No `lorem ipsum` placeholder; use realistic content |
| Edge cases | Long text, empty arrays, error states represented |

Avoid coverage-gaming: the metric is to drive value, not the other direction.

### Naming Conventions

| Convention | Example |
|------------|---------|
| `Default` | The most common usage |
| `Disabled` / `Loading` / `Error` | Single-state variants |
| `WithIcon` / `WithBadge` | Compositional variants |
| `Mobile` / `Tablet` / `Desktop` | Viewport variants |
| `Dark` / `HighContrast` | Theme variants |
| `LongText` / `EmptyList` | Edge-case variants |

Consistent naming enables auto-generated docs and easier review.

### Per-Component Coverage File

For complex components, ship a `.coverage.md` next to the component:

```md
# Button Story Coverage

L2 States: 6/6 ✓
- default ✓
- hover ✓
- active ✓
- focus ✓
- disabled ✓
- loading ✓

L3 Prop Permutations: 12/36 (pairwise sufficient)
- size × variant covered
- size × color covered
- variant × color covered

Edge cases:
- LongLabel ✓
- IconOnly ✓
- KeyboardFocus ✓ (with play function)
```

## Workflow

1. **Audit baseline** — count components, count stories.
2. **Compute L1-L5** with chosen tooling.
3. **Set targets** by project stage.
4. **Define state coverage** per component class.
5. **Adopt addon-coverage** (Storybook 9+) for runtime reports.
6. **Adopt addon-test** for vitest-driven story tests.
7. **Configure CI gate** — block PR / warn / time-decay.
8. **Generate gap report** and assign components to owners.
9. **Track trend** — weekly L1-L5 percentages.
10. **Review story quality** quarterly — kill trivial stories; deepen rich ones.
11. **Set per-component coverage docs** for complex components.

## Output Template

```yaml
story_coverage:
  project_stage: growth
  components_total: 176
  stories_total: 412
  metrics:
    l1_file_coverage: 87
    l2_state_coverage: 62
    l3_prop_permutation: 34
    l4_viewport: 41
    l5_theme: 72
  targets:
    l1: 95
    l2: 80
    l3: 50
    l4: 70
    l5: 90
  ci_gate:
    strategy: block_pr_if_l1_below
    threshold_l1: 95
    time_decay: false
  tooling:
    addon_coverage: yes
    addon_test: yes
    vitest_workspace: configured
  gap_report:
    missing_components: 23
    critical_state_gaps: [Button_error, Input_readonly, Modal_closing]
  story_quality_audit:
    last_run: 2026_04_15
    trivial_stories_to_kill: 8
    stories_to_deepen: 14
  trend_30d:
    l1: "84_to_87"
    l2: "58_to_62"
  per_component_coverage_docs: yes_for_design_system
```

## Anti-Patterns

- 100% L1 with 1-line trivial stories — coverage gaming.
- No state coverage requirement — half the component states untested.
- Pairwise / equivalence-class missing on combinatorially-large components — exponential story explosion.
- CI gate at 100% L1 from day 1 — blocks every PR; teams disable.
- L1 only without L2-L5 — false sense of completeness.
- Story file with single `Default` story for every component — no variation.
- Stories using `lorem ipsum` — fake data hides real edge cases.
- No viewport stories on layout-sensitive components.
- Single light-theme stories on dark-mode-supporting product.
- Story names not following conventions — auto-docs / discoverability fails.
- Trend not tracked — coverage drifts down silently.
- Quality audit not done quarterly — trivial stories accumulate.
- addon-test ignored on Storybook 9+ project — missing free Vitest integration.
- Per-component `.coverage.md` for trivial components — overhead.
- Manual coverage script that doesn't update — stale; uses git pre-commit hook to refresh.
- Setting L3 100% target — combinatorial impossibility.

## Deliverable Contract

A story-coverage plan is complete when:

- L1-L5 metrics measured.
- Targets set per project stage.
- State coverage requirements defined per component class.
- addon-coverage / addon-test installed (Storybook 9+).
- CI gate configured (block / warn / time-decay).
- Gap report generated with owner assignment.
- Trend tracking weekly.
- Quality audit cadence (quarterly).
- Per-component coverage docs for complex / design-system components.

## References

- Storybook docs, *Test runner* and *Coverage*.
- @storybook/addon-coverage and @storybook/addon-test documentation.
- Vitest workspace docs — vitest.dev/guide/workspace.
- Glenn Halverson — *Story-Driven Development* (Chromatic blog).
- Brian Lonsdorf — *Combinatorial UI Testing* (talks).
- IEEE *Pairwise Testing* — combinatorial test reduction theory.
- Microsoft PICT tool — pairwise test generator.
- Brad Frost, *Atomic Design* (2016) — component-class taxonomy.
- Adam Wathan / Steve Schoger, *Refactoring UI* — state coverage rationale.
- Storybook 10 release notes (2026) — built-in coverage panel.
- BPS World, *Storybook Story Coverage in Production*.
- Microsoft Fluent UI, Shopify Polaris, Adobe Spectrum — public design-system coverage benchmarks.
