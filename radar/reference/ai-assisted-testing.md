# AI-Assisted Testing & Modern Trends (2026-05 snapshot)

Purpose: Use AI to accelerate testing without delegating judgment. Read this when Radar is asked to generate tests with AI assistance or evaluate AI-generated test suites.

Contents:

- AI usage boundaries
- self-healing limits
- AI-generated code testing strategy
- Radar integration rules

## Current State

Use these numbers as directional context, not as deployment criteria:

- AI-assisted test creation can reduce drafting time by roughly `50-70%`
- AI-generated tests often require substantial rewrite; assume `> 70%` may need revision
- human review remains mandatory even when generated tests look plausible
- A widely-cited 2026 observation: AI assistants (Claude Code, Cursor, Copilot) produce **plausible tests that pass without asserting anything meaningful** — `80%` line coverage with weak assertions catches almost nothing. Treat coverage and AI-generated test counts as inputs, not as quality signals.
- Mutation testing is now **table stakes** for any suite touched by AI generation; see `mutation-testing.md`. Stryker (JS/TS), PIT (Java), MutPy / mutmut (Python), Stryker.NET, and `cargo-mutants` (Rust) are the 2026 production toolchains.

## Tooling Snapshot (2026-05)

| Layer | 2026 default | Notes |
|-------|---------------|-------|
| Unit / integration (JS / TS) | **Vitest** for new projects; Jest 30 for incumbent codebases | Vitest 4.x: `~5x` faster cold start, `~28x` faster watch reruns than Jest 30; native browser mode replaces JSDOM for component tests |
| E2E (web) | **Playwright** | `~33M` weekly npm downloads, `~45%` adoption among QA pros; built-in auto-waiting and a first-party MCP server + agent-mode for natural-language test generation (TestDino, ZeroStep, Bug0 sit on top of this) |
| Self-healing E2E | Playwright + AI rewrite tools | Use to recover from selector / locator drift only; never to reinterpret intended product behavior — see `## Self-Healing Test Boundaries` |
| Mutation testing | Stryker / PIT / MutPy / Stryker.NET / cargo-mutants | Required companion when the underlying code is AI-generated |

## AI Test Generation Rules

AI can help with:

- first-pass edge-case enumeration
- boring scaffolding for test files
- variant generation for existing assertions
- flaky-log clustering and hypothesis generation

AI cannot replace:

- meaningful assertion design
- business-priority judgment
- deciding whether a test belongs at unit, integration, or E2E level

## Review Checklist For AI-Generated Tests

- assertions are meaningful and non-empty
- tests can actually fail when behavior regresses
- edge cases include null, empty, boundary, and error conditions where relevant
- mocks reflect plausible reality
- no optimistic assumptions hide failure modes
- non-deterministic inputs are controlled

## Self-Healing Test Boundaries

| Level | What It Can Repair | Automation Level |
|------|---------------------|------------------|
| L1 | Selector drift and obvious locator changes | High |
| L2 | Small flow changes | Medium, review required |
| L3 | Business-logic drift | Low, human decision required |

Use self-healing only to recover from presentation drift, not to reinterpret intended product behavior.

## AI-Generated Code Testing Strategy

When the underlying code is AI-generated:

1. treat property-based testing as strongly preferred
2. use mutation testing when the generated tests themselves are AI-assisted
3. add contract tests for generated clients or API layers
4. apply security scanning as a non-optional companion

## Breaking the Implementation-Test Loop

The failure this section prevents: one agent writes the code, the tests, and the explanation from one reading of the spec, every test passes, and the behavior is wrong — because the same misunderstanding produced both sides. The suite is now *pinning* the bug, so the correct fix arrives as "a change that breaks tests". Full mechanism, provenance table, and independence calibration → `_common/EVIDENCE_LADDER.md` §2.

Authoring procedure, cheapest step first — stop when the change's evidence floor is met:

| Step | Action | What it buys |
|------|--------|--------------|
| 1 | Before generating anything, put **invariants, worked examples, counterexamples, and non-goals** in the task text | the expectation now has a source outside the code |
| 2 | Write the oracle in a context that has **not seen the implementation** — before it exists, or in a separate session | removes the shared-context correlation |
| 3 | Add one **E4 mechanism** on the changed surface: a property, a mutation run scoped to the diff, or a differential against the pre-change path | detects a class of failure E3 structurally cannot |
| 4 | Record in the PR **what the tests prove and what they do not** | makes the residual visible instead of implied |

Provenance question to ask of every assertion under review: *where did this expected value come from?* If the answer is "from reading the implementation" or "the same session that wrote the code", the assertion documents current behavior and cannot detect that the behavior is wrong. Rewrite it from the spec, a domain example, a published test vector, a production record, or a domain owner's confirmation.

Prompt shapes that cause this failure:

- `"add tests for this file"` — no intent given, so the model asserts whatever it can observe; produces brittle implementation-detail tests
- `"make the tests pass"` — makes the test the variable and the code the constant, exactly backwards for a regression
- asking the same session that just wrote the feature to "verify it works" — E0 evidence formatted as E3

Prompt shape that avoids it: state the behavioral contract, the boundaries, the failure paths, and the invariants **first**, and ask for tests against that contract — never against the file.

## Radar Integration

| Radar Phase | AI Helps With | Human Must Still Decide |
|-------------|---------------|-------------------------|
| `SCAN` | detect likely gaps and risky files | priority and business impact |
| `LOCK` | estimate complexity | what is worth testing now |
| `PING` | draft tests and variants | final assertions and scope |
| `VERIFY` | cluster flaky signals and suggest fixes | whether the fix is real and sufficient |
| `FLAKY` | pattern mining across repeated failures | root-cause confirmation |

## AI Auto-Fix in CI: Regression Cascade Risk

When AI agents encounter test failures in CI, they may attempt autonomous fix cycles:

1. Agent observes a failing test (actually flaky, not a real regression)
2. Agent "fixes" code by adding unnecessary error handling or workarounds
3. New CI run hits a different flaky test
4. Agent attempts to fix that one too — compounding regressions

**Prevention rules:**

- Always verify whether a failure is flaky vs. a genuine regression before applying code changes
- Use flaky detection data (rerun history, quarantine lists) as input before any auto-fix attempt
- Limit autonomous retry-fix cycles to a single iteration; escalate to human after one failed fix
- Never let an AI agent modify production code in response to a test failure without confirming the failure is reproducible and deterministic

Source: Frontiers AI-augmented CI/CD framework 2026; industry-wide pattern reports

## Default Guardrail

Treat AI-generated tests as draft material until a human has:

- reviewed the assertions
- run the tests
- confirmed the tests fail when they should
- removed optimistic or duplicated cases
