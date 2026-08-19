# Shift Recipes — Per-Recipe Behavior Detail

Full behavior notes for each Shift Recipe. `SKILL.md`'s `## Subcommand Dispatch` section carries a one-line summary per recipe and points here for the detail below.

## `plan` (default)

General migration planning — strategy selection (Strangler Fig / Branch by Abstraction / Parallel Run / Big Bang), scope assessment, risk matrix. Use when the migration type is not yet decided or is architectural rather than framework/language-specific.

## `codemod`

AST transform authoring — prefer ast-grep/jssg for cross-language or large-scale rewrites, jscodeshift or ts-morph for deep JS/TS semantics, LibCST for Python. Always dry-run before batch execution. Mechanical rewrite only — semantic verification still belongs to `verify`.

## `strangler`

Strangler Fig implementation design — façade routing plan, old/new coexistence boundaries, migration sequence. Guard against façade-bottleneck (façade accumulating routing logic) and technical-layer decomposition (should be domain-boundary).

## `verify`

Before/after behavioral-equivalence proof — golden fixtures, request replay, diff classification (expected / regression / benign). Required gate before removing compatibility layers in `COMPLETE`.

## `framework`

Framework major-version migration (Vue 2→3, React 18→19, React CRA→Next.js, Next.js 15→16, Angular major, Svelte 4→5, Rails major, Spring Boot 2→3, Spring Boot 3→4, Express→Fastify/Hono). Produces a feature-parity checklist, adapter/compat shim plan, dual-run validation harness, and deprecation-warning triage. Consumes `detect`'s "framework deprecated" findings as input.

- For React 19: the React team co-published codemods with codemod.com covering `Context.Provider`, `forwardRef`, `useContext→use` rewrites ([codemod.com React 18→19 guide](https://docs.codemod.com/guides/migrations/react-18-19)).
- For Next.js 15→16: run `npx @next/codemod upgrade 16`; key changes are Cache Components and async `params`/`searchParams`.
- For Svelte 4→5: run `npx sv migrate svelte-5` or migrate per-component in VS Code; slots replaced by snippets.
- For Spring Boot 3→4: requires Java 21+, Jakarta EE 11, Spring Framework 7 — use OpenRewrite `UpgradeSpringBoot_4_0` recipe ([Moderne blog, 2025](https://www.moderne.ai/blog/spring-boot-4x-migration-guide)).

Distinct from `plan`: `plan` chooses the strategy in the abstract; `framework` executes a specific framework transition with domain-specific gotchas.

## `lang`

Language / runtime migration (JS→TS, TS `strict` staged enablement, Python 2→3 residual, Node LTS majors, Go toolchain, Java 8→17/21). Drives incremental type-inference strategy (leaves first, one `strict` sub-flag per PR) and runtime-behavior-diff verification (same deterministic workload on old + new runtime). Hand off crypto/TLS runtime diffs to Sentinel.

## `deprecate`

Feature / API sunset orchestration — deprecation period, usage telemetry, Sunset HTTP header (RFC 8594), client migration docs, staged removal playbook with reversible rollback flag. Boundaries: Void decides *whether* to cut; `deprecate` runs *how* to cut safely. Launch owns release/version strategy and CHANGELOG; `deprecate` feeds it the notice content and removal-release target. Use when the surface being removed has external or cross-team callers.

## `detect` (absorbed from horizon)

Identify deprecated / outdated / unmaintained libraries via `npm audit`, maintenance signals (last-publish, contributors, GH issues), health scoring, and EOL runtime check. Emit replacement report — proposed alternatives, bundle-impact estimate, migration path (which Recipe handles execution: `modernize` / `framework` / `lang` / `deprecate`). Boundary: `detect` discovers; downstream Recipes execute. Gear escalates here when patch/minor reveals major-version-behind or EOL deps.

## `modernize` (absorbed from horizon)

Swap library with modern native API (Temporal > moment/date-fns, structuredClone > lodash.cloneDeep, fetch > axios/node-fetch, Intl > i18n libs, URLSearchParams > URI.js, Iterator helpers > lodash chains, Set methods > lodash set ops, Object.groupBy > lodash.groupBy, native WebSocket > ws, native glob() > glob pkg, `--env-file` > dotenv, native TS stripping > ts-node, URLPattern > path-to-regexp, node:test > jest/mocha for simple suites, node:sqlite > better-sqlite3). Quantify bundle-size delta (≤ 170KB initial JS compressed budget), caniuse coverage ≥ 95% for target browsers, and P99 latency ≤ baseline + 20%. Require ≥ 6 months post-stable-release before recommending adoption. Produce isolated PoC, not core rewrite — keep self-contained and easy to discard. Hand off Node 24+, Python 3.13, Java 25+ deep version diffs to `lang`.

## `radar` (absorbed from horizon)

Evaluate emerging technologies against maturity matrix before any recommendation — require ≥ 6 months post-stable-release, ≥ 1K GitHub stars or equivalent ecosystem signal, active maintenance (commits within last 90 days), and team learning-curve realism. Produce technology radar (adopt / trial / assess / hold rings) with browser/runtime compatibility matrix and supply-chain provenance check (npm provenance attestations, `npm audit signatures`, pnpm `trustPolicy: no-downgrade`, OIDC Trusted Publishing posture, release cooldown ≥ 72h for new versions / ≥ 60d for new packages per CIS Supply Chain Security Benchmark). Output is advisory — Magi makes the organizational decision; deep supply-chain forensics (worm campaigns, IoC matching) belong to `chain[malware-scan]`.


## Per-Recipe Behavior (SKILL.md excerpt)

Behavior notes per Recipe (full detail → `reference/recipes-detail.md`):
- `plan`: Default. Strategy selection + scope + risk matrix when migration type is undecided or architectural.
- `codemod`: AST transform authoring (ast-grep/jssg cross-language, jscodeshift/ts-morph JS/TS, LibCST Python); always dry-run; semantic verification belongs to `verify`.
- `strangler`: Strangler Fig design — façade routing, coexistence boundaries, sequence; guard against façade-bottleneck and technical-layer decomposition.
- `verify`: Before/after behavioral-equivalence proof (golden fixtures, replay, diff classification); gate before removing compat layers in `COMPLETE`.
- `framework`: Framework major-version migration with feature-parity checklist, compat shim, dual-run, deprecation triage; consumes `detect` findings. Per-framework codemod commands (React 19, Next.js 16, Svelte 5, Spring Boot 4) in reference.
- `lang`: Language/runtime migration with incremental type-inference and runtime-behavior-diff; hand off crypto/TLS diffs to Sentinel.
- `deprecate`: API sunset orchestration; Void decides *whether*, `deprecate` runs *how*; Launch owns release/CHANGELOG. Use when removed surface has external/cross-team callers.
- `detect` (absorbed from horizon): Identify deprecated/outdated/unmaintained libraries + replacement report + migration path; discovers only, downstream Recipes execute.
- `modernize` (absorbed from horizon): Swap library with native API; quantify bundle/caniuse/P99 gates; isolated PoC, not core rewrite; hand off deep version diffs to `lang`.
- `radar` (absorbed from horizon): Evaluate emerging tech against maturity matrix + provenance check; advisory only, Magi decides, forensics to `chain[malware-scan]`.
