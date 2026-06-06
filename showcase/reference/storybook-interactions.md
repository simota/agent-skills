# Storybook Interactions / Play Function Reference

Purpose: Embed user-flow tests directly inside stories via the `play` function. Interactions execute in a real browser, validate behavior with `@storybook/test` (Storybook 8+, replaces `@storybook/jest` + `@storybook/testing-library`), and integrate with addon-vitest for CI runs and the Interactions panel for in-UI debugging. Stories become double-duty artifacts: living documentation and component-level tests.

## Scope Boundary

- **showcase `interaction`**: in-story play functions that exercise a single component's primary user flow (click, fill, submit) and assert visible output. Runs inside the Storybook iframe.
- **showcase `story` (default, elsewhere)**: static variant/state authoring without interaction logic.
- **showcase `vrt` (elsewhere)**: visual snapshot diffing — checks pixels after a play function runs, but does not assert behavior.
- **showcase `csf3` (elsewhere)**: format migration — separate concern from interaction authoring.
- **artisan (elsewhere)**: production component implementation. Play functions never modify component code.
- **forge (elsewhere)**: prototype play scenarios are throwaway; promote to interaction tests only after the prototype graduates.
- **voyager (elsewhere)**: cross-page E2E journeys (login → checkout → confirmation). Play functions stop at the component boundary.
- **echo `walkthrough` (elsewhere)**: persona-based qualitative cognitive walkthrough, not automated assertions.
- **radar (elsewhere)**: unit/integration tests outside Storybook. Use `composeStories` to reuse a story-with-play in Vitest.

## Workflow

```
SCAN     →  inventory stories with interactive elements (forms, buttons, dropdowns, modals)
         →  flag stories without play functions on interactive components

PLAN     →  pick the primary user flow per component (1 happy path, 1-2 critical edges)
         →  decide query strategy: getByRole > getByLabelText > getByText > getByTestId

WRITE    →  import { within, userEvent, expect } from '@storybook/test'
         →  scope queries to canvasElement; await every userEvent; assert visible state

VERIFY   →  run in Storybook UI → check Interactions panel for step trace
         →  run via addon-vitest in CI; confirm no waitForTimeout, no real network

HANDOFF  →  pass coverage delta to Radar; flag cross-page flows for Voyager
```

## API Surface (Storybook 10 / `@storybook/test`)

| Import | Purpose | Replaces (legacy) |
|--------|---------|-------------------|
| `within(canvasElement)` | Scope queries to story root | `@testing-library/react` `within` |
| `userEvent.setup()` | Realistic user input simulation | `@storybook/testing-library` `userEvent` |
| `fireEvent.<event>` | Low-level synthetic events when `userEvent` is too coarse | `@storybook/testing-library` `fireEvent` |
| `expect(...).toBe...` | Jest-style assertions (jest-mock-equivalent) | `@storybook/jest` `expect` |
| `fn()` | Spy / mock function for arg callbacks | `@storybook/jest` `jest.fn` |
| `waitFor` / `findBy*` | Async settle helpers | `@testing-library` waitFor |

## Code-Pattern Table

| Pattern | When to use | Snippet |
|---------|-------------|---------|
| Scoped canvas query | Every play function | `const canvas = within(canvasElement)` |
| Accessible click | Buttons, links, role-bearing controls | `await userEvent.click(canvas.getByRole('button', { name: /submit/i }))` |
| Form fill | Inputs with label association | `await userEvent.type(canvas.getByLabelText('Email'), 'a@b.co')` |
| Async appearance | Element renders after promise | `expect(await canvas.findByText('Saved')).toBeInTheDocument()` |
| Spy on arg callback | Verify event handler fired | `args: { onSubmit: fn() }` then `expect(args.onSubmit).toHaveBeenCalledOnce()` |
| Step grouping | Multi-stage flows in Interactions panel | `await step('Fill form', async () => { ... })` |
| Inline test (CSF Factories) | Attach a test to a story | `Story.test('submits', async ({ canvas, userEvent }) => { ... })` |

## Anti-Patterns

- Using `waitForTimeout` or arbitrary `setTimeout` — flaky on slow CI; use `waitFor`/`findBy*` predicates that converge on real DOM state.
- Querying with `getByTestId` when a semantic query exists — sacrifices a free a11y check; reserve `data-testid` for non-semantic wrappers only.
- Calling real network APIs from play functions — couples tests to infra and leaks credentials. Use MSW handlers in `parameters.msw` or `sb.mock` for module-level mocks.
- Writing multi-page flows in a play function — once the test crosses route boundaries, ownership belongs to Voyager. Split or hand off.
- Forgetting `await` on `userEvent` calls — userEvent v14+ is async. Missing `await` swallows assertions silently and produces false-green results.
- Asserting on implementation details (class names, prop values via DOM attributes) — assert on visible output the user perceives. Class assertions break on style refactors.
- Skipping the Interactions panel during authoring — debugging blind via stack traces wastes hours; the panel offers step-through with DOM snapshots per step.
- Mixing `@storybook/jest` + `@storybook/testing-library` imports in Storybook 8+ — both are deprecated; consolidate to `@storybook/test`.
- Reusing a play function across visual-regression and interaction roles without tagging — VRT runs capture only the final DOM; interaction tests capture every step. Tag with `play-test` vs `visual-test` to route correctly.

## Integration with addon-vitest (Storybook 10)

- Stories with play functions become Vitest browser-mode tests automatically — no separate `.test.ts` needed.
- `composeStories` becomes optional; CSF Factories `.test()` method attaches assertions inline and excludes them from sidebar via `tags: ['!autodocs']` or custom tag filters.
- Coverage from interaction runs merges with unit coverage in Vitest's reporter — single coverage source for stories + units.

## Handoff

- **To Artisan**: component changes required to make a flow testable (missing `aria-label`, ungrouped form fields). Provide failing query as evidence.
- **To Voyager**: flows that cross page boundaries or require auth state — escalate with the play function as the seed scenario.
- **To Frame (Figma)**: missing interaction states in design (loading, error, success) discovered while authoring play steps — feed back for design coverage.
- **To Radar**: flows that overlap unit-test territory (pure prop logic, no DOM); recommend conversion to Vitest unit tests via `composeStories` when DOM rendering adds no signal.
