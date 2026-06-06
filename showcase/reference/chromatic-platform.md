# Chromatic Platform

## Purpose

Chromatic is the dominant visual review SaaS for Storybook. It's not a generic VRT engine — it's a workflow platform with branch comparison, baseline approval, TurboSnap, and Tokens of Trust. This reference covers Chromatic-specific configuration, monorepo routing, baseline strategy, and the approval-flow design.

## Scope Boundary

- IN scope: Chromatic project setup, baseline approval flow, TurboSnap, branch comparison, monorepo project routing, Tokens of Trust, Webhook integration, design-token review.
- OUT of scope: generic VRT methodology (`vrt`), Percy / Loki / Playwright VR (different platform), Storybook addons broadly (`a11y` / `coverage`), local visual diffing tools, image comparison theory.

## Core Concepts

### What Chromatic Adds Beyond Generic VRT

| Generic VRT (Percy, Loki, Playwright) | Chromatic |
|---------------------------------------|-----------|
| Snapshot diff | Snapshot diff + branch / PR awareness |
| CLI / CI integration | + Web UI for approval |
| Image-only | + Story metadata, Args, parameters |
| Manual baseline approval | + Auto-accept on main, queue on PR |
| One project | + Composition / monorepo project routing |
| All stories every time | + TurboSnap (only changed stories) |
| Static comparison | + Design-token review (Tokens of Trust) |

Chromatic's value is the **workflow** around the visual diff, not the diff engine itself.

### Project Setup

```bash
pnpm add -D chromatic
```

Get a project token from chromatic.com, then:

```bash
npx chromatic --project-token=<token>
```

`.github/workflows/chromatic.yml`:

```yaml
name: Chromatic
on: pull_request
jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # required for TurboSnap
      - uses: actions/setup-node@v4
      - run: pnpm install
      - uses: chromaui/action@v11
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          exitOnceUploaded: true
          onlyChanged: true  # TurboSnap
```

### Baseline Approval Flow

| State | Action |
|-------|--------|
| Story changed | PR check shows visual diff |
| Reviewer approves | Story baseline updates on merge |
| Reviewer denies | PR blocked; developer fixes |
| Auto-accept on main | New baselines absorbed without manual approval |
| Manual baseline override | Force-accept current state as baseline |

Approval responsibility:

- **Designer + engineer** review together for major changes.
- **Engineer alone** for trivial changes (1-2 stories).
- **Component owner** for ownership-defined components.

### TurboSnap

Only re-snapshot stories whose underlying code changed:

```yaml
chromatic:
  command: chromatic --only-changed
```

Requirements:

- Webpack / Vite / Rollup with module dependency tracking.
- `fetch-depth: 0` in CI checkout (full git history).
- TurboSnap-compatible builder (Storybook 7+ + Vite/Webpack 5).

Speedup: **2x-30x** depending on PR size; the dominant Chromatic optimization in 2026.

### Branch Comparison

Chromatic compares each PR's stories against:

- **Default base**: latest accepted main baseline.
- **Branch base**: when PR targets non-main branch (e.g., release/v2).
- **Manual baseline override**: rare; for redesign branches.

Configure via `--baseBranch` flag or `chromatic.baseBranch` config.

### Tokens of Trust

For design-system projects: Chromatic 2024+ surface design-token changes (color, spacing, typography) explicitly.

| Feature | What it does |
|---------|-------------|
| Token diff view | Show which tokens changed and which stories use them |
| Token usage map | "Color #brand-primary used in 47 stories" |
| Token approval | Approve token changes once; cascades to dependent stories |
| Coverage gap | Tokens with no story coverage |

Adopting `Muse`-managed tokens with Chromatic creates an end-to-end design-system review pipeline.

### Monorepo Project Routing

Multiple Storybook instances in one repo (e.g., `apps/web`, `apps/admin`, `packages/ui`):

| Strategy | Setup |
|----------|-------|
| Single Chromatic project | Composition: aggregate stories from all sub-builds |
| Multiple Chromatic projects | One project per Storybook; route via `--project-token` per workflow |
| Filter projects | Use `chromatic.json` per package |

For UI-library + consumer-app split:

- Library project tracks the `packages/ui` Storybook.
- Each consumer app may compose the library and add app-specific stories.
- TurboSnap routes diffs to the correct project.

### Composition

Storybook Composition lets one Storybook reference another:

```ts
// .storybook/main.ts
export default {
  refs: {
    'ui-lib': {
      title: 'UI Library',
      url: 'https://main--abc123.chromatic.com',
    },
  },
};
```

Chromatic supports composed Storybook reviews — a PR in the UI library shows downstream impact in the consumer app.

### Webhook Integration

Chromatic webhooks fire on:

- Build complete.
- Build approved / denied.
- Baseline accepted.
- New version published.

Integrate with:

- Slack / Discord — design-review notifications.
- Linear / GitHub Issues — auto-create issue on denial.
- PR comment bots — embed Chromatic links.

### Cost / Snapshot Budget

Chromatic prices on snapshots / month:

| Plan | Snapshots / month | Use |
|------|-------------------|-----|
| Free | 5,000 | Solo / OSS |
| Standard | 30,000 / 50,000 | Small teams |
| Pro | 100,000+ | Larger orgs |

Snapshot budget control:

| Lever | Effect |
|-------|--------|
| TurboSnap | -50% to -90% snapshots |
| `--exit-once-uploaded` | Don't wait for build = faster CI |
| Skip stories with parameter | `parameters: { chromatic: { disable: true } }` for CI-irrelevant stories |
| Viewport selection | Default 320px + 1200px; override for high-coverage components |
| Theme selection | Test light + dark; skip experimental themes |

### Skip Patterns

Skip a story from Chromatic without removing it from Storybook:

```ts
export const InternalDebug: Story = {
  parameters: {
    chromatic: { disable: true },
  },
};

export const StableLayoutOnly: Story = {
  parameters: {
    chromatic: {
      // Test only desktop viewport
      viewports: [1200],
    },
  },
};

export const PausedAnimations: Story = {
  parameters: {
    chromatic: {
      // Pause animations for stable snapshot
      pauseAnimationAtEnd: true,
    },
  },
};
```

### Animation / Loading Handling

Snapshots capture moments. For animated components:

| Strategy | Use |
|----------|-----|
| `pauseAnimationAtEnd: true` | End-state snapshot |
| `delay: 500` | Wait for animation to settle |
| `disable: true` | Hard-to-stabilize animations |
| Multiple stories per state | Snapshot each phase explicitly |

Loading states require deterministic data — mock fetch / use `parameters.mockData`.

### Cross-Browser

Chromatic snapshots in:

- Chrome (default).
- Firefox (paid plans).
- Safari (paid plans).
- Edge (paid plans).

Cross-browser typically multiplies snapshot count. Reserve for components with known browser-specific bugs.

### Visual Test in Storybook 9+

Storybook 9 ships with built-in visual testing via Chromatic integration. Side-panel UI reviews diffs before pushing.

### When NOT to Use Chromatic

| Scenario | Alternative |
|----------|-------------|
| Strict on-prem requirement | Loki, Percy on-prem |
| OSS hobby project below free tier | Default to free; otherwise Loki |
| Page-level visual regression (full-page screenshots) | Playwright VR / Percy |
| Cross-browser required and budget tight | Playwright VR |

## Workflow

1. **Sign up** at chromatic.com; get project token.
2. **Install** chromatic CLI dependency.
3. **Wire CI** with `chromaui/action` GitHub Action.
4. **Enable TurboSnap** with `--only-changed`.
5. **Configure baseline branch** (usually `main`).
6. **Set approval policy** — who can approve, designer + engineer pairing.
7. **Add Skip patterns** for non-visual / animated stories.
8. **Set viewport list** — default 320 + 1200; override per-story if needed.
9. **Configure Webhooks** for Slack / Linear / PR-bot.
10. **Adopt Tokens of Trust** if design-system project.
11. **Set up Composition** if monorepo.
12. **Track snapshot budget** — monthly cap with margin.
13. **Quarterly review** — denied builds, time-to-approve, snapshot costs.

## Output Template

```yaml
chromatic_setup:
  project_token_secret: CHROMATIC_PROJECT_TOKEN
  monorepo_strategy: composition
  projects:
    - id: ui_library
      path: packages/ui
      base_branch: main
    - id: consumer_app
      path: apps/web
      base_branch: main
      composes: ui_library
  ci:
    action: chromaui/action@v11
    fetch_depth: 0_for_turbosnap
    only_changed: yes
    exit_once_uploaded: yes
  approval_policy:
    default_branch: main
    auto_accept_on_main: yes
    pr_requires_review: yes
    reviewers: [designer, engineer]
    deny_blocks_merge: yes
  turbosnap:
    enabled: yes
    expected_snapshot_reduction_pct: 70
  viewports: [320, 1200]
  skip_patterns:
    chromatic_disable_for: [debug_stories, performance_test_stories]
    pause_animations: [loading, transitions]
  tokens_of_trust:
    enabled: yes
    token_source: muse_handoff
  webhooks:
    slack: design_review_channel
    linear: visual_regression_project
  budget:
    plan: standard
    snapshots_monthly_cap: 50000
    expected_usage: 18000
  quarterly_review_date: 2026_07_25
```

## Anti-Patterns

- TurboSnap disabled on monorepo — burns the snapshot budget.
- `fetch-depth: 1` in CI — TurboSnap fails silently.
- Auto-accepting all main builds without review — broken visuals slip in.
- Cross-browser on every PR — multiplies cost without proportional value.
- Snapshotting animated components without pause / delay — flaky baselines.
- One big Chromatic project for monorepo with 10+ apps — review noise.
- No Skip patterns — debug / experiment stories burn snapshots.
- Reviewer pool of 1 person — bottleneck.
- Webhook to no-one — denials missed.
- No Tokens of Trust adoption when design-system mature — manual review of cascading changes.
- Storybook 8 stuck on legacy Chromatic API — migrate to Storybook 9+ for visual-test panel.
- Composition without versioning the upstream — ref breaks.
- Custom CI action instead of `chromaui/action` — re-implement TurboSnap detection.
- Snapshot for every viewport from 320 to 1920 px — diminishing return.
- Manual baseline override "to clear noise" — destroys diff history.
- No quarterly cost / approval-time review — cost / process drift unnoticed.
- Self-approving own PRs — defeats review purpose.

## Deliverable Contract

A Chromatic setup is complete when:

- Project token in CI secrets.
- Chromatic action wired in CI with TurboSnap + fetch-depth 0.
- Approval policy documented (who can approve, deny-blocks-merge).
- Skip patterns defined for non-visual / animated stories.
- Viewport list set with rationale.
- Webhooks wired to Slack / Linear / PR-bot.
- Tokens of Trust enabled if design-system project.
- Composition configured if monorepo.
- Snapshot budget tracked with monthly cap.
- Quarterly review scheduled.

## References

- Chromatic Documentation — chromatic.com/docs.
- TurboSnap docs — chromatic.com/docs/turbosnap.
- Tokens of Trust announcement (Chromatic, 2024).
- Storybook 9 release notes — built-in visual testing.
- Storybook Composition docs.
- Norbert de Langen (Storybook lead) — talks on Chromatic + Storybook integration.
- Tom Coleman / Dominic Nguyen / Zoltan Olah (Chromatic founders) — design-system review framing.
- Visual Regression Testing community — github.com/topics/visual-regression-testing.
- Percy / Loki / Applitools comparison articles (2024-2026) for cross-platform decisions.
- Microsoft Fluent UI / Shopify Polaris / Adobe Spectrum — public Chromatic-based design-system pipelines.
- chromaui/action GitHub repo.
