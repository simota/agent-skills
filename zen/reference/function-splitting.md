# Function Splitting Delta

Purpose: Zen behavior-preserving seam and verification contract. Extraction patterns are model-known.

## Trigger Signals

Consider splitting when measured cognitive complexity is high, responsibilities or abstraction levels mix, I/O and transformation are entangled, or local variables form distinct lifetimes. Length alone is not proof.

Do not split a tightly coupled algorithm, measured hot path, or coherent sequential procedure merely to satisfy a line threshold. Avoid one-use helpers that make navigation harder.

## Workflow

1. Pin current observable behavior with focused tests or characterization coverage.
2. Identify seams at data transformations, I/O boundaries, commands/queries, resource lifetime, or independent policy decisions.
3. Name the responsibility and design explicit inputs/outputs before extraction.
4. Extract one seam at a time and run the focused verification after each step.
5. Measure complexity and readability; inline a split that increased coupling or parameter plumbing.

## Verification

- Same results, exceptions, side effects, ordering, and resource cleanup.
- No duplicated policy or hidden shared state introduced.
- Dependencies and parameters do not grow without a clearer boundary.
- Performance-sensitive paths retain measured baseline behavior.

Route type problems to Quill, dead branches to Zen `dead`/Sweep, layer-boundary problems to Atlas, and measured regressions to Bolt.
