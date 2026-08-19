# Guard Clause Delta

Purpose: Zen semantic-preservation contract for flattening nested control flow. Guard-clause syntax is model-known.

## Transformation Rules

- Invert only conditions whose early exit is behaviorally equivalent.
- Preserve condition evaluation order, short-circuiting, exceptions, logging, mutations, and resource cleanup.
- Keep validation guards separate from side-effecting work.
- Use language-native propagation (`?`, `defer`, `try/finally`, typed narrowing) without changing error shape.
- Prefer a linear happy path, but extract a predicate or responsibility when guard lists become another form of complexity.

Guard clauses generally reduce nesting/cognitive complexity, not cyclomatic branch count. Report the metric that actually changed.

## Verification

- Existing focused tests pass unchanged.
- Every input returns or throws the same externally observable result.
- Error precedence remains the same when multiple preconditions fail.
- Cleanup and transaction boundaries still execute.
- Type narrowing and nullability behavior remain sound.

If repeated guard preambles reveal cross-cutting policy, propose a named validation boundary; route architecture changes to Atlas rather than introducing middleware implicitly.
