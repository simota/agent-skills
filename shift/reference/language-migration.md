# Language Migration Reference

Purpose: Execute a language-level transition — adding or strengthening a type system, crossing a runtime major version, or porting across a language break. Covers JS → TS, TS non-strict → `strict`, Python 2 → 3 residual pockets, Node LTS major bumps, Go toolchain/module upgrades, and Java 8 → 17/21. The focus is runtime-behavior diffs and incremental rollout, not syntactic rewrites alone.

## Scope Boundary

- **Shift `lang`**: executes a specific language / runtime transition with inference strategy, staged strictness, and runtime-behavior-diff verification.
- **Shift `migrate` (default)**: general migration planning at the architectural layer.
- **Shift `framework`**: framework version jumps — may trigger a `lang` follow-up (e.g., Spring Boot 3 requires Java 17+).
- **Zen**: refactor within the current language version — no runtime or type-system change.
- **Horizon**: detects end-of-life runtimes — produces the input, does not execute.

If the request is "enable `strict: true`" → `lang`. If it is "add types to one file for readability" → Zen.

## Common Migration Paths

| From → To | Mechanical | Semantic / runtime diff |
|-----------|------------|-------------------------|
| JS → TS | Rename `.js` → `.ts`, add `tsconfig`, allowJs during transition | `any` creep, interop with untyped deps, `esModuleInterop` behavior, runtime shape vs declared type drift |
| TS loose → `strict` | Enable flags one at a time (`noImplicitAny` → `strictNullChecks` → `strictFunctionTypes` → `strictPropertyInitialization`) | Uncovered null paths, variance in callback params, DI container init order |
| Python 2 → 3 residual | `2to3`, `print`/`except` syntax, `unicode_literals` | `str` vs `bytes` boundary, integer division, dict ordering assumptions, `__hash__` defaults |
| Node 18 → 20 → 22 LTS | `engines` bump, lockfile regen | `fetch` globally available, `--experimental-*` flag removals, V8 behavior (e.g., regex, Intl), deprecated OpenSSL algos, corepack behavior; Node 22 LTS: `require(esm)` synchronous support (behind `--experimental-require-module` until stable), native `WebSocket` client, Maglev JIT on by default |
| Python 3.11/3.12 → 3.13 / 3.14 | `pyproject.toml` / `setup.cfg` target bump, lockfile regen | 3.13: free-threaded CPython (GIL-optional, experimental build `--disable-gil`), JIT compiler (tier-2, experimental), `locals()` semantics change; 3.14: deferred evaluation of annotations (`from __future__ import annotations` behavior becomes default) — run full async/threading test suite before promoting |
| Go 1.N → 1.N+x | `go mod tidy`, toolchain directive | `GOPROXY` / checksum changes, loop-var scoping (1.22+), generics adoption, deprecated stdlib (`io/ioutil`) |
| Java 8 → 17 / 21 | Module path, removed APIs (`sun.misc.Unsafe` paths) | Records / sealed types opt-in, virtual threads (21) scheduler diffs, GC default change (G1 → ZGC), strong encapsulation of JDK internals |
| Java 17 / 21 → 25 | OpenRewrite `UpgradeToJava25` recipe (when available); `jdeps --jdk-internals` for encapsulation gaps | Virtual thread pinning audit (`synchronized` + native), Project Leyden class-data sharing, pattern matching completeness |

Capture project-specific diffs you encounter in `.agents/shift.md`.

## Type-Inference Strategy (JS → TS / loose → strict)

Order matters — do not attempt the strictest config on day one.

1. **`allowJs` + `checkJs: false`**: compile passes, no type coverage yet.
2. **File-by-file opt-in** via `// @ts-check` on JS or rename leaf modules first (utils / pure functions) before entry points.
3. **`noImplicitAny`**: surfaces the untyped surface area — expect many findings; triage into `unknown` (validate at boundary) vs `any` (explicit tech-debt comment with ticket).
4. **`strictNullChecks`**: highest-value flag; run in isolation, fix null paths, then commit.
5. **`strictFunctionTypes` + `strictPropertyInitialization`**: lower-volume fixes, enable together.
6. **`noUncheckedIndexedAccess`**: last — high noise, high value for correctness.

Never enable `strict: true` wholesale on a large codebase in one PR. A 500-error PR is unreviewable and unrevertable.

## Runtime Behavior Diffs

Type-system changes do not alter runtime. Runtime / version bumps do — these are the real risks:

- **Node LTS**: run the full test suite on the new major *before* the `engines` bump. Watch for `punycode` removal, `util._extend` removal, weak cipher defaults, `fetch` body streaming changes. Node 22 LTS: `require(esm)` allows synchronous import of ES modules (reduces the CJS→ESM migration surface); native `WebSocket` eliminates `ws` dependency for simple cases; Maglev JIT changes warm-up latency profile — re-benchmark latency-sensitive paths.
- **Go**: 1.22 loop-variable semantics change silently — `go vet` flags some cases but not all; audit goroutine-in-loop call sites manually.
- **Java 17 / 21**: default charset is UTF-8 from 18+ (was platform-dependent) — file I/O round-trips may change. Virtual threads expose pinning on `synchronized` / native methods.
- **Python 3.13**: free-threaded build (`--disable-gil`) is opt-in and experimental — do not enable in production without extensive concurrency testing. JIT tier-2 compiler is also experimental; disable with `PYTHON_JIT=0` if benchmarks regress. `locals()` snapshot semantics changed — code that mutated `locals()` breaks silently.
- **Python 3**: `dict` ordering is insertion-ordered from 3.7 — code that relied on set-like ordering now silently depends on insertion order.

Verification pattern: run the same deterministic workload on old and new runtimes, compare output byte-for-byte (or with a normalizer for timestamps). Diff the two. Unexplained diffs block promotion.

## Workflow (overlays ASSESS → ... → COMPLETE)

```
ASSESS   →  pin source / target versions exactly (runtime + stdlib minor)
         →  inventory: files by language, existing type coverage %, deprecated-API usage
         →  capture CI matrix — does it already test target version?

PLAN     →  incremental strictness ladder or file-conversion order (leaves first)
         →  runtime-diff test harness (deterministic workload, old vs new)
         →  flag strategy: compiler flag per phase, not per file

PREPARE  →  scaffold type stubs / declaration files for untyped deps
         →  add CI lane running target runtime in parallel (not replacing)
         →  codemod for mechanical rewrites (e.g., `ioutil` → `io`/`os`, `print` → `print()`)

EXECUTE  →  one strictness flag or one file batch per PR
         →  keep green on both old and new runtime until cutover
         →  resolve each flag's findings before enabling the next

VERIFY   →  type coverage % target met (e.g., ≥95% non-any)
         →  runtime-diff harness: zero unexplained diffs
         →  benchmark: startup / hot-path within envelope

COMPLETE →  drop old runtime from CI matrix
         →  remove `allowJs` / compat shims
         →  document type-debt ledger (remaining `any` / `unknown` with tickets)
```

## Anti-Patterns

- Declaring `any` everywhere to "get it compiling" — ships type pollution that later readers trust.
- Bumping Node major in the lockfile without the CI matrix catching it on the old major first.
- Enabling `strict: true` + every sub-flag simultaneously — findings cannot be triaged.
- Porting Python 2 → 3 by running `2to3` and calling it done — `str`/`bytes` issues surface only at I/O boundaries.
- Upgrading Java major and switching GC at the same time — perf regressions become unattributable.
- Leaving `// @ts-ignore` / `# type: ignore` without a linked ticket — becomes permanent.

## Handoff

- → `Builder`: per-phase conversion tasks with file list and target flag.
- → `Radar`: runtime-diff harness; add tests at the boundaries where `str`/`bytes`, null/undefined, or numeric precision surfaced diffs.
- → `Gear`: CI matrix updates, runtime-image bumps, lockfile regen.
- → `Sentinel`: review crypto/TLS-related runtime changes (OpenSSL default diffs, JDK TLS changes).
- ← `Horizon`: consumes "runtime EOL" findings as the trigger.
