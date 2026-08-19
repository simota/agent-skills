# Unit-Test Architecture Delta

Purpose: Scope and handoff contract for Radar `unit`. General AAA structure, test-double definitions, and naming conventions are model-known.

## Scope

- `unit`: establish or repair unit-test architecture, boundaries, determinism, and double selection.
- `coverage`: fill measured gaps using the existing architecture.
- `edge`: extend an existing suite with boundary and failure cases.
- `integration`: use when real DB, cache, queue, filesystem, or downstream protocol behavior is part of the claim.
- Voyager owns browser-level journeys; Siege owns resilience programs.

## Required Decisions

- Identify the observable unit boundary and collaborators.
- Choose the weakest sufficient double; do not mock values or private internals.
- Inject clocks, IDs, randomness, I/O, and repositories rather than patching global state.
- Preserve repository naming and fixture conventions.
- Record any production seam needed to make the unit deterministic.

## Verification

- No real network, wall clock, filesystem, database, or sleep inside unit tests.
- Same seed and input produce the same result.
- Assertions prove outcomes or necessary collaborator contracts, not implementation trivia.
- Shared mutable fixtures and order-dependent tests are absent.

## Handoff

- Production globals or mixed concerns -> Zen with the required seams.
- Surviving mutants -> Radar `mutation`.
- Real infrastructure required for the claim -> Radar `integration`.
