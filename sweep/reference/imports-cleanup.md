# Import Cleanup Decisions

Load for `imports`; apply `reference/cleanup-protocol.md`. Resolve configured lint/compiler/bundler tools instead of copying a versioned tool catalog.

| Candidate | Decision / evidence |
|---|---|
| Hard-unused binding | ≥95 candidate confidence only after source/test/docs verification **and module-initialization checks**. An unused binding does not mean its import has no side effects. |
| Side-effect import | Protect binding-free imports (`ImportDeclaration.specifiers.length === 0`), CSS/polyfills/decorator registration, and side effects of bound imports. Never auto-remove. |
| Type-only usage | Propose `import type` only after checking emitted JS and required initialization under the actual compiler/module settings; promotion can remove module execution. |
| Duplicate imports | Consolidate only when import kind, attributes, module semantics and initialization ordering remain equivalent. |
| Barrel | Preserve published `exports`/entry points and external consumers. For internal-only barrels, measure the actual compiler/bundle cost before proposing direct imports; no assumed speedup or purity annotation on arbitrary re-exports. |

## Cycles

Use the configured graph tool and distinguish runtime from type-only edges. Original triage bands: HIGH = load-time 2-cycle; MEDIUM = 3+-node cycle; LOW = exclusively type-only cycle. Confirm actual initialization behavior; node count alone does not prove a runtime failure. Send structural cycle remediation to Atlas with the graph and evidence. Replacing an edge with lazy loading does not prove the architectural cycle disappeared.

## Batch Verification and Output

Handoff to Builder; cap each import-edit batch at 50 imports per file **and** the SKILL's ≤10 files. Preserve required initialization; run the same build, tests and lint; compare emitted bundle size and cycle graph (must not increase). Report missing baseline/unsupported checks rather than claiming improvement. Public API changes require separate confirmation.

Output: Scope, Language, actual tools/configuration; counts and paths for HardUnused, SideEffect, Duplicate, TypeOnly, cycles by severity and Barrels; per-item confidence/guard evidence; before/after build, tests, lint, bundle and cycle results; Builder execution / Atlas structural handoff.

Canonical emit semantics: https://www.typescriptlang.org/tsconfig/verbatimModuleSyntax.html (checked 2026-09-17). Verify the installed compiler's behavior; do not conflate the introduction of type import syntax with availability of `verbatimModuleSyntax`.
