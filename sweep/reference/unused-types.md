# Unused Type Decisions

Load for `types`; use `reference/cleanup-protocol.md`. Identify the actual TS/Flow project graph, configured analyzer/compiler, supported target matrix and declaration entry points before proposing removals. Verify CLI options in the installed tool; do not overwrite project strictness/configuration during detection.

## Reachability and Classification

| Candidate | Gate / action |
|---|---|
| Hard-orphan type | ≥95 candidate confidence with tool evidence and independent consumer search across source, tests, declaration files, stories, docs and JS JSDoc |
| Transitively unused types | ≥90 only after proving the entire subgraph unreachable from supported entry points; re-run after each approved batch until no new orphans appear |
| Generic constraint | A constraint on a reachable generic **is a consumer**. Keep it. When the enclosing type is itself unreachable, evaluate both as a transitive group. |
| Deprecated re-export | Deprecation/sunset is not disuse. Existing consumers require a Shift migration handoff; public package compatibility must be checked before removal. |
| Re-export chain | Trace to consumers; preserve public entry paths. Flattening must not force external consumers onto private deep imports. |
| `any` accumulation | Quantify by file/module and hand off to Quill; neither a deletion candidate nor permission for a typing rewrite. |

## Hidden Consumers

Protect ambient/module-augmenting `.d.ts`, package `types`/`exports` and tsconfig `files`/`include` roots; JSDoc types used by JS checking; generic constraints and inferred/router types; generated schemas, decorators/codecs and their runtime values; Storybook `Meta` and Figma Code Connect `*.figma.ts` consumers. Check actual generation/discovery configuration. A type graph must not be confused with a runtime-value graph.

## Verification and Output

Handoff approved small batches to Builder. Run the project's compiler/type checks against the baseline, including declaration emission/public API checks and supported strict settings. Separately label additional strict probes; a new stricter configuration is not the original baseline. Run tests and applicable Storybook/codegen/Code Connect checks. Re-scan to detect newly orphaned groups and confirm retained public imports still resolve.

Report Scope, tools/configuration, counts/paths/confidence for hard-orphan/transitive/deprecated/re-export findings, protected consumers, `any` counts/handoff, and before/after type/build/test results. Do not assert bundle savings for erased types without measuring emitted artifacts.

Constraint semantics: https://www.typescriptlang.org/docs/handbook/2/generics.html#generic-constraints (checked 2026-09-17). The presence of `extends` is usage, not pollution by itself.
