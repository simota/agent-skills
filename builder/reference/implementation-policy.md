# Implementation Decision Policy

Use this reference for decisions that must remain consistent across languages and frameworks. It intentionally does not restate language syntax, framework tutorials, or general design-pattern catalogs that the executing model already knows.

## Authority Order

When sources disagree, apply this order:

1. Repository-local instructions, architecture decisions, and public contracts.
2. Checked-in toolchain configuration, manifests, lockfiles, and generated schemas.
3. Existing code and tests that demonstrate the current convention.
4. Current primary documentation for the detected version.
5. Model knowledge, only for stable concepts that do not affect compatibility or correctness.

Do not introduce a second repository convention merely because it is idiomatic in another ecosystem. If the repository has no convention, choose the smallest reversible design that satisfies the requirement and record the assumption.

## Language and Toolchain Grounding

Before using version-sensitive syntax, APIs, compiler flags, framework behavior, or dependency recommendations:

1. Detect the actual version from repository evidence.
2. Confirm that the relevant compiler, formatter, linter, and test runner are available.
3. Check current primary documentation when repository evidence is insufficient.
4. Verify the result with the repository's compiler, type checker, linter, or tests.

| Ecosystem | Inspect first | Verification oracle |
|-----------|---------------|---------------------|
| TypeScript / JavaScript | `package.json`, lockfile, `tsconfig*.json`, framework config | configured typecheck, lint, and test scripts |
| Go | `go.mod`, `go.work`, build tags, generated files | `go test ./...`, `go vet ./...`, repository linters |
| Python | `pyproject.toml`, lockfile, supported-version metadata, type-checker config | configured tests, type checker, and linter |
| Rust | `Cargo.toml`, `Cargo.lock`, `rust-toolchain*`, feature flags | `cargo check`, `cargo test`, configured Clippy policy |
| Kotlin | Gradle files, version catalog, JVM/KMP targets, compiler plugins | configured Gradle checks and tests |
| Swift | `Package.swift`, Xcode project settings, deployment targets, strict-concurrency settings | `swift build` / `swift test` or project `xcodebuild` workflow |

Rules:

- Never infer a language or framework version from this skill.
- Never add a library because a reference calls it a default; reuse the repository stack unless the requirement proves a gap.
- Treat preview, experimental, deprecated, edition-specific, and platform-specific behavior as unverified until checked against the detected toolchain.
- Compiler and test evidence outrank remembered syntax or a frozen compatibility table.

## Architecture Selection

Choose architecture from demonstrated complexity, not pattern familiarity.

| Evidence | Default decision |
|----------|------------------|
| Simple data entry or single-aggregate CRUD with no cross-field invariants | Direct service plus repository boundary; no tactical DDD ceremony |
| Stable domain vocabulary, meaningful invariants, or behavior-rich entities | Value objects and an aggregate boundary sized to one consistency transaction |
| Multiple teams or conflicting meanings for the same term | Establish bounded contexts and context mapping before tactical DDD |
| Read and write models have independently proven scaling or ownership needs | Consider CQRS; do not split models pre-emptively |
| Audit-grade history, temporal reconstruction, or domain events are primary business data | Evaluate event sourcing with migration, replay, versioning, and operational cost made explicit |
| Multi-step cross-boundary transaction | Prefer idempotent orchestration and an outbox; introduce a saga only when compensation semantics are defined |

Defaults:

- Organize new behavior as a vertical slice while preserving the repository's existing structure.
- Keep domain logic independent from HTTP, persistence, clocks, randomness, and vendor SDKs.
- Add an interface only at a real boundary or a demonstrated substitution seam.
- Escalate database schema design to `schema`, API contract design to `gateway`, and pre-change dependency impact to `ripple`.

## Implementation Boundaries

The `builder/SKILL.md` Core Contract and `_common/CODE_QUALITY.md` are authoritative. Apply these additional decision rules:

- Parse external data once into a trusted type. Preserve the repository's existing validation library and error model.
- Preserve public error semantics. Do not replace exceptions, result values, status codes, or cancellation behavior without contract evidence.
- Retry only classified transient failures, with a bound and idempotency protection where mutation is possible.
- Keep network, database, filesystem, clock, and randomness access at explicit seams so the core behavior can be tested deterministically.
- Prefer generated API types or boundary parsing over handwritten mirrors of external payloads.
- For data-intensive paths, bound input size and fix algorithmic or I/O shape problems before micro-optimization.

## Frontend State Boundary

Builder owns business rules and integration logic; `artisan` owns UI component implementation.

- Reuse the repository's current state-management and form stack.
- Keep ephemeral interaction state local.
- Treat remote data as server state and use the repository's existing request/cache layer.
- Add shared client state only when multiple independent consumers require synchronized client-owned data.
- Do not add a state library, form library, schema library, or fetch abstraction solely because it appears in an example.

## What Belongs in a Reference

Retain reference material only when it provides at least one of:

- a repository-specific default or prohibition;
- a role boundary or handoff contract;
- a decision threshold that changes execution;
- a false-positive guard or failure mode the model is likely to miss;
- an exact output schema or verification workflow.

Do not recreate broad language specifications, generic best-practice catalogs, framework tutorials, or frozen version timelines. For those topics, ground the task in the local toolchain and current primary documentation under the Language and Toolchain Grounding gate.

## Decision Record

For a non-obvious implementation choice, record only the evidence needed for review:

```yaml
ImplementationDecision:
  repository_evidence: "config, existing pattern, test, or contract"
  choice: "smallest design that satisfies the requirement"
  rejected: "closest alternative and why it was not selected"
  verification: "compiler, test, lint, or contract check"
```
