# TS/JS Testing Delta

Purpose: Radar defaults that remain after removing model-known AAA, naming, and boilerplate examples.

## Repository-First Rules

- Use the repository's runner, helpers, factories, and assertion style before introducing a new test stack.
- Prefer semantic React Testing Library queries: role or label first; `testId` only when no user-facing selector exists.
- Use MSW at HTTP boundaries when the repository already supports it; include error, timeout, and malformed-response paths.
- Prefer small factories with explicit overrides over large shared fixtures.
- Use Testcontainers only when engine behavior, migrations, transactions, or queries are part of the claim.

## Boundary Decision

| Dependency | Default | Escalate when |
|---|---|---|
| Pure/local code | no mock | nondeterministic collaborator exists |
| HTTP | MSW or existing boundary stub | schema drift requires a contract test |
| Database | repository fake/stub | real SQL behavior is under test |
| Time/randomness | fake clock / fixed seed | never use wall-clock sleeps |
| Browser journey | hand off to Voyager | page navigation or browser state matters |

## Version-Sensitive Notes

- Vitest 4.x requires Vite 6+ and Node 20+; confirm the installed version before using `coverage.changed` or tags.
- Jest 30 changed supported Node/TypeScript/jsdom baselines; use the local lockfile and official docs rather than this file for exact compatibility.

## Verification

- One observable behavior per test unless assertions describe one atomic outcome.
- No real network, clock, random seed, or shared mutable fixture in deterministic unit tests.
- Coverage commands come from package scripts or repository config, not invented defaults.
- Route production seams exposed by test design to Zen; route CI runner/caching constraints to Gear.
