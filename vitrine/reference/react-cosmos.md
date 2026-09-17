# React Cosmos: Fixture Delivery

Load for `cosmos` authoring or migration. Read the installed package versions, existing fixtures, bundler configuration, and package scripts before changing them. Keep one primary component-documentation surface; coexistence with Storybook needs a migration owner and exit condition.

## Minimal fixture contract

A fixture module default-exports a React node, a component, or an object whose keys name variants. Do not copy Storybook named-export conventions into Cosmos. Adapt this single format example to real component props:

```tsx
import { Button } from './Button';

export default {
  Ready: <Button>Save</Button>,
  Disabled: <Button disabled>Save</Button>,
};
```

For stateful variants, use named React components and Hooks rather than disabling hook lint. Controls must use APIs exported by the installed `react-cosmos/client` version; do not invent a control signature from a remembered release.

## Configuration and isolation

| Decision | Required action |
|---|---|
| Bundler | Match the app's real aliases, CSS, assets, environment substitutions, and bundler. For the documented Vite integration the plugin is `react-cosmos-plugin-vite`, enabled in `cosmos.config.json`; do not install a guessed `@cosmos/vite-plugin`. |
| Providers | Default-export a component receiving `children` from `cosmos.decorator.tsx`. Directory scope determines affected fixtures; outer directories wrap inner ones. Reset mutable stores/query caches between fixtures. |
| Global CSS | Use the documented `globalImports` setting so global styles precede fixture styles; do not silently change cascade order by importing all CSS from a decorator. |
| Network | Initialize mocks before rendering; unexpected requests fail visibly. No real production API, credentials, or write requests in fixtures. |
| Async/lazy content | Exercise loading, resolved, and error states with a supported React/bundler path. A promise-returning fixture or a `*.server.fixture.tsx` suffix does not establish RSC support. Verify the installed integration and renderer. |
| MDX | Check the bundler's MDX configuration and fixture extensions. MDX fixtures exist; do not claim Cosmos categorically lacks MDX or equate them with Storybook Doc Blocks. |
| Export/VRT | Use the installed CLI/package scripts for dev and static export. Verify the actual renderer URL and external VRT adapter; do not promise compatibility from a vendor-name table. |

## Verification and handoff

- Render every added/changed variant and relevant decorator scope; check console errors, missing assets, default/focus/disabled/loading/error states, and mock leakage.
- Reopen fixtures in another order to detect leaked state. Verify static export separately when it is a deliverable; a working dev server is insufficient.
- Verify real fixture coverage against the component's supported states, not merely file count. Record unrendered states and reasons; do not call them covered.
- Fixtures observe production components. A fixture-only production prop or component behavior change goes to Artisan; isolated interaction assertions go to Radar; cross-page flows go to Voyager. Missing design variants go to Frame.
- For migration, map each existing fixture/state to the destination and preserve providers, mocks, accessibility checks, and baseline ownership. Delete the old surface only after parity verification.
- Keep server exposure local unless broader access is authorized. Do not upgrade dependencies or publish visual baselines merely to demonstrate an example.

## Official lookup points

Checked 2026-09-17; use the installed-version documentation when it differs. Offline: use project-pinned docs/configuration; mark unavailable feature claims unverified.

- https://reactcosmos.org/docs/fixtures/fixture-modules — export shape, named stateful components, MDX fixtures.
- https://reactcosmos.org/docs/fixtures/decorators — directory composition and global CSS ordering.
- https://reactcosmos.org/docs/getting-started — select the actual bundler; follow its configuration and CLI links rather than copying an unrelated framework tutorial.
