# React Cosmos Reference

Purpose: React Cosmos 6+ is a fixture-based React component explorer positioned as the lightweight alternative to Storybook. Fixtures are plain React modules — every default-exported JSX tree becomes a navigable variant. Cosmos boasts the fastest hot-reload loop for component-only React work and the simplest mental model: "render this component with these props, in isolation." Recommended for React-only projects with minimal addon needs, or teams allergic to Storybook's config surface.

## Scope Boundary

- **vitrine `cosmos`**: React Cosmos 6+ fixture authoring (`*.fixture.tsx`), decorator chains, multi-instance prop iteration, Vite/Webpack bundler config. Cosmos-specific decisions.
- **vitrine `story` (default, elsewhere)**: Storybook CSF authoring. Cosmos and Storybook can coexist (`*.stories.tsx` + `*.fixture.tsx` in the same repo) but choose one as the primary docs surface.
- **vitrine `catalog` (elsewhere)**: hierarchy planning. Cosmos derives hierarchy from filesystem only — no `title` field; folder structure IS the catalog.
- **vitrine `vrt` (elsewhere)**: visual regression. Cosmos has weaker first-party VRT — Chromatic does not support Cosmos; use Playwright VRT or Loki against the Cosmos URL.
- **vitrine `interaction` (elsewhere)**: Cosmos has no built-in play-function equivalent; use Vitest browser-mode + React Testing Library against the fixture export directly.
- **vitrine `mdx` (elsewhere)**: Cosmos has no MDX docs system; use README files or external docs sites.
- **artisan (elsewhere)**: production component code. Fixtures observe; never modify.
- **forge (elsewhere)**: throwaway prototype renders — Cosmos's lightness makes it tempting for prototyping, but the artifact is still throwaway until promoted.
- **voyager (elsewhere)**: E2E. Cosmos fixtures are isolated by design; cross-page flows belong in Voyager.
- **echo `walkthrough` (elsewhere)**: persona walkthrough is qualitative; Cosmos provides the surface to demo, not the methodology.

## Workflow

```
SCAN     →  detect cosmos.config.json or react-cosmos in package.json
         →  inventory existing fixtures vs components; flag coverage gaps

PLAN     →  decide bundler (Vite via @cosmos/vite-plugin or Webpack 5)
         →  decide decorator strategy: global (cosmos.decorator.tsx) vs scoped (per-folder)
         →  decide control approach: useFixtureInput / useFixtureSelect / useValue

WRITE    →  default export = primary fixture; named exports = variants
         →  wrap providers in decorators, not in each fixture

VERIFY   →  cosmos dev server: every fixture renders without error
         →  test reuse: import fixture default export in Vitest for component-level tests

HANDOFF  →  if VRT needed → Playwright VRT against Cosmos URL
         →  if rich docs needed → reconsider Storybook (Cosmos has no MDX equivalent)
```

## Fixture Format

| Form | Shape | Use case |
|------|-------|----------|
| Single fixture | `export default <Button>Click</Button>` | One variant per file |
| Multi-fixture | `export const Primary = ...; export const Secondary = ...;` | Variants in one file |
| Function fixture | `export default () => { ... return <Button /> }` | Hooks needed (useFixtureInput) |
| Object fixture | `export default { component: <Button />, ... }` (Cosmos 6+) | Metadata + render |

## Code-Pattern Table

| Pattern | Use case | Snippet |
|---------|----------|---------|
| Multi-instance props | Render same component with N prop sets | `export default [<Button size="sm" />, <Button size="md" />, <Button size="lg" />]` |
| Interactive control (string) | Editable input in Cosmos UI | `const [label] = useFixtureInput('label', 'Click me')` |
| Interactive control (select) | Dropdown variant picker | `const [v] = useFixtureSelect('variant', { options: ['primary', 'secondary'] })` |
| Stateful control | Driven by component state | `const [val, setVal] = useValue('count', { defaultValue: 0 })` |
| Global decorator | Theme/Router/Provider for all fixtures | `src/cosmos.decorator.tsx` exports a default React component wrapping `children` |
| Scoped decorator | Provider for one folder | `src/components/Form/cosmos.decorator.tsx` |
| Lazy fixture | Code-split heavy fixtures | `export default () => import('./Heavy').then(m => <m.default />)` (with Suspense decorator) |
| Server fixture (Cosmos 6+) | Server-component-style fixture | `*.server.fixture.tsx` |

## Storybook vs Cosmos Decision Tree

| Signal | Choose Storybook | Choose Cosmos |
|--------|------------------|---------------|
| Framework | React + Vue + Svelte + Angular | React only |
| Team size | 5+ engineers, design system at scale | 1-4 engineers, app-internal components |
| VRT need | Chromatic / built-in visual testing | Playwright VRT manually wired |
| Interaction tests | Play functions + addon-vitest | External Vitest using fixture imports |
| Rich docs | MDX, Doc Blocks, Autodocs | README / external docs |
| Addon ecosystem | 200+ addons (a11y, design-tokens, MSW, etc.) | Minimal — by design |
| Hot reload speed | Fast (10+ ESM-only) | Fastest (smallest runtime) |
| Config surface | `.storybook/` directory, multiple files | `cosmos.config.json` (often empty) |
| AI/MCP integration | `addon-mcp` available | None |
| Default recommendation | Most teams | React-only + minimalist + speed-first |

Rule: Storybook is the safe default. Recommend Cosmos when (1) framework is React-only, (2) team explicitly values minimal config and fastest hot reload, (3) addon ecosystem (Chromatic, MCP, design-tokens) is not required.

## Anti-Patterns

- Adopting Cosmos for a multi-framework monorepo — Cosmos is React-only; Vue/Svelte components have no path forward and require a second tool.
- Wrapping providers inline in every fixture — duplication and drift; use `cosmos.decorator.tsx` (global) or folder-level decorators.
- Recreating Storybook's addon ecosystem in Cosmos — if you find yourself building a11y panel, design-token sidebar, and VRT integration manually, you've chosen the wrong tool. Migrate to Storybook.
- Using fixtures as integration tests — fixtures import services or fetch real APIs become flaky. Mock at decorator level (MSW, mock providers) or in fixture function bodies.
- Promising Chromatic compatibility — Chromatic does not support Cosmos. VRT requires Playwright/Lost Pixel/Loki against the dev server URL.
- Coexistence without ownership decision — running both `*.stories.tsx` and `*.fixture.tsx` indefinitely doubles maintenance. Pick a primary; the other is migration debt.
- Ignoring server fixtures in RSC projects — Cosmos 6+ supports `*.server.fixture.tsx`; falling back to client-only fixtures hides RSC-specific bugs.
- Using `useValue` when component state is the source of truth — creates a parallel state and confuses the demo. Reach for `useFixtureInput`/`useFixtureSelect` for explicit controls.
- Skipping `cosmos.config.json` bundler declaration — Cosmos defaults differ from app bundler; misalignment causes silent CSS-modules or alias resolution failures.

## Vite / Webpack Integration

- **Vite**: install `react-cosmos` + `react-cosmos-plugin-vite`. Cosmos picks up `vite.config.ts` aliases, plugins, and CSS handling automatically. Fastest path; recommended for new projects.
- **Webpack 5**: install `react-cosmos` + `react-cosmos-plugin-webpack`. Point `cosmos.config.json` at `webpack.config.js`. Heavier but matches CRA/legacy stacks.

## Handoff

- **To Artisan**: components requiring fixture-only props (e.g., `__cosmosOverride`) are leaky abstractions; request component-side refactor.
- **To Voyager**: cross-page user journeys cannot be expressed in fixtures by design; hand off the user flow as a Voyager E2E scenario.
- **To Frame (Figma)**: missing variants discovered during fixture authoring → request design coverage update; map fixture names to Figma component variants for Code Connect.
- **To Radar**: fixture default exports are directly importable in Vitest; recommend converting interaction-flavored fixtures into Vitest browser-mode tests rather than building a Cosmos play-function shim.
- **To Vitrine `story` (peer)**: when Cosmos limits become decisive (need MCP, MDX, Chromatic, multi-framework), migrate fixtures to CSF — many fixtures map 1:1 to CSF stories.
