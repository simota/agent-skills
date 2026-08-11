# Core Contract — Rationale and Sources

Long-form justification, thresholds, and citations behind the Core Contract bullets in
`SKILL.md`. Read when a rule needs its reasoning, a tuning number, or a source.

## TypeScript configuration

Use `strict: true` plus `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, and
`noPropertyAccessFromIndexSignature`. Both TS 6.x (the final JS-based release series) and
tsgo (the Go-native rewrite shipping as TS 7.0 once it reaches feature parity) default
`strict: true` in `tsc --init`, but neither folds those three extra flags into the
`--strict` umbrella — keep all four explicit.

For new projects, target zero TS 6.x deprecation warnings: tsgo hard-removes
`target: es5`, `moduleResolution: "node"`, `baseUrl` without `paths`, and
`esModuleInterop: false`.
Source: [Microsoft TypeScript Blog — A 10x Faster TypeScript](https://devblogs.microsoft.com/typescript/typescript-native-port/)

## Boundary validation

- `.safeParse()` over `.parse()` — `.parse()` throws and can crash the process inside
  Express/Hono handlers. Format failures with `z.prettifyError()` or `z.flattenError()`.
- Define Zod schemas as module-level constants. Recreating a schema per call wastes CPU;
  module-level constants are 2-5x faster for repeated validations.
- Generate API types from OpenAPI specs (`openapi-typescript`) rather than hand-writing
  them — hand-written response types drift from backend reality and fail silently at
  runtime. Zod v4 `.toJSONSchema()` exports boundary schemas as JSON Schema (Draft
  2020-12 by default; `target: "openapi-3.0"` for OpenAPI 3.0 sync), closing the loop
  between runtime validation and API documentation.
  Source: [Zod — JSON Schema conversion](https://zod.dev/json-schema)

## API resilience thresholds

- Categorize before retrying: 4xx is a caller bug (do not retry); 429 backs off with
  `Retry-After`; 5xx uses exponential backoff with 3-5 max attempts.
- Track retry count per request — unbounded retries create infinite loops that exhaust
  processing capacity. Never retry a non-idempotent mutation without an idempotency key.
- Circuit breaker scope is **per endpoint**, not per host. Open after consecutive failures
  (default 5 in 60s; tune by criticality — payment <= 3, search <= 10), half-open after a
  30s-2min cooldown, close on success.

## Type-level design principles

- **Make illegal states unrepresentable.** Prefer discriminated unions
  (`type Order = { state: "draft", items?: Item[] } | { state: "submitted", items: NonEmptyArray<Item>, submittedAt: Date }`)
  over boolean flag soup. The compiler enforces the spec for free, and AI codegen
  self-detects missing branches via exhaustiveness checks.
  Sources: deviq.com — Make Illegal States Unrepresentable (Yaron Minsky);
  learningtypescript.com — Discriminated Unions
- **Parse, don't validate.** At every boundary, parse `unknown` into a fully-typed value
  with one one-way transform (Zod / Valibot / Effect Schema / ArkType). Downstream code
  receives the parsed type and never repeats boundary checks. The parser is the contract;
  the type is the proof.
  Sources: lexi-lambda.github.io — Parse Don't Validate (Alexis King);
  pockit.tools — Zod vs Valibot vs ArkType 2026
- **Return `Result<T, E>`; do not throw across module boundaries.** Railway-Oriented
  Programming via `neverthrow`, Effect-TS, or a hand-rolled discriminated union. Throwing
  forces every caller to defend; a `Result` puts the error path in the type system and
  shrinks AI's wrap-everything-in-try/catch reflex. Reserve throws for non-recoverable
  invariant violations.
  Sources: fsharpforfunandprofit.com — Railway Oriented Programming; effect.website
- **Branded / nominal types for IDs and units.**
  `type UserId = string & { __brand: "UserId" }` — zero runtime cost, prevents the whole
  "passed an `orderId` where a `userId` was expected" bug class. Apply to every domain ID,
  monetary amount, duration, and percentage. Zod v4 `z.string().brand<"UserId">()` is the
  idiomatic constructor.
  Sources: oneuptime.com — Implementing Branded Types in TypeScript 2026;
  learningtypescript.com — Branded Types
- **`using` / `await using`** for disposable resources (DB connections, file handles, HTTP
  clients) guarantees deterministic cleanup on early return or exception.
- **Type `catch` parameters as `unknown`** and narrow with `instanceof` — untyped catch
  allows accessing non-existent properties and hides real error shapes.

## Architecture

- **Functional core, imperative shell.** Pure, deterministic domain logic in the core (no
  I/O, no clocks, no random); side effects (HTTP, DB, filesystem, time) wrapped in a thin
  shell at the edges. The core is what you let AI write and verify with property-based
  tests; the shell is what a human reviews line by line.
  Sources: destroyallsoftware.com/talks/boundaries (Gary Bernhardt);
  kennethlange.com/functional-core-imperative-shell/
- **Vertical Slice Architecture for feature work.** Organise by feature, not by layer: a
  `cancel-subscription` feature lives in `features/cancel-subscription/` with its own
  controller, command, query, handler, validator, and tests — not spread across
  `controllers/`, `services/`, `repositories/`, `dto/`. Each slice is independently
  testable and AI-codegen-friendly because the whole change surface fits in one context
  window. Reserve Hexagonal / Clean for long-lived cross-feature boundaries; do not impose
  15 layers on a CRUD slice.
  Sources: jimmybogard.com/vertical-slice-architecture;
  milanjovanovic.tech/blog/vertical-slice-architecture

## Writing for future agents

**Write LLM-friendly, deterministic code.** Explicit over implicit, boring over clever,
exhaustive over compact. Enumerate edge cases in the type system rather than handling them
with `if (x ?? defaultBehavior)`. Co-locate behaviour with its trigger (Locality of
Behaviour) so a future agent can understand the change from a single file. Avoid
metaprogramming, dynamic dispatch, and reflection unless explicitness is provably worse.
Sources: stackoverflow.blog — Coding Guidelines for AI Agents and People Too (2026);
htmx.org/essays/locality-of-behaviour/

## Verification-first

The single highest-leverage practice for AI-assisted coding. Before writing implementation
code, identify or create the verification path (tests, screenshot diff, expected stdout,
type signature, schema contract) and hand it to the build loop alongside the spec. Code
without a verifier is data, not deliverable. Fix root causes; do not suppress symptoms.
Source: code.claude.com/docs/en/best-practices — Anthropic Claude Code Best Practices

## Impact Scope Check (5 axes)

Run at VERIFY before declaring done. For every modified symbol/file:

1. **Callers/importers** — grep references; nothing broken?
2. **Tests** — related unit/integration/e2e added or updated?
3. **Types/contracts** — TypeScript types, OpenAPI, DB schema, GraphQL consistent?
4. **Configs** — env vars, feature flags, config files propagated?
5. **Docs** — README, CHANGELOG, API docs updated?

Document each axis verdict in the deliverable. If 3+ axes are non-trivially affected, or
uncertainty is high, recommend `ripple` (pre-change impact analysis) before completion.
Never close VERIFY with an axis marked "unchecked".
