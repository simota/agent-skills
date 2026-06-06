# Mutation Testing Reference

Purpose: Measure an existing test suite's effectiveness by injecting small code faults (mutants) and checking whether the tests catch them. Survived mutants signal weak or missing assertions. This recipe covers author-side, per-module mutation runs — strengthening unit-test assertions day-to-day.

## Scope Boundary

- **Radar `mutation`**: author-side, code-quality mutation testing. Run a tool against a focused module, analyze survivors, harden assertions, and set a local CI mutation-score threshold. Complements `unit` / `coverage`.
- **Siege `mutation`**: program-level mutation strategy — tiered CI (PR < 5 min / nightly < 30 min / release full), operator selection at scale (fault-driven vs generic), equivalent-mutant pruning infrastructure, mutation as a resilience gate, enterprise wiring (e.g., Meta ACH, Stryker .NET ML pruning). Radar hands off here when the program needs architecture, not per-module improvement.

Rule of thumb: if the task is "strengthen the assertions in `order-calculator.ts`", use Radar `mutation`. If the task is "design the organization's mutation testing program and CI tiering", route to Siege.

## Tool Matrix

| Language | Tool | Runner command | Notes |
|----------|------|----------------|-------|
| TS / JS | StrykerJS 7.0+ | `npx stryker run` | Vitest, Jest, Node Tap, Jasmine, Mocha runners supported; `stryker.config.mjs`. Source: [stryker-mutator.io/blog/announcing-stryker-js-7](https://stryker-mutator.io/blog/announcing-stryker-js-7/) |
| Java / Kotlin | PIT | `mvn org.pitest:pitest-maven:mutationCoverage` | Pair with pitest-junit5-plugin; JUnit 6 compat via pitest-junit5-plugin update |
| Python | mutmut (default), cosmic-ray (advanced operators) | `mutmut run`, `cosmic-ray init` | mutmut is simpler; cosmic-ray for custom operators |
| Rust | cargo-mutants | `cargo mutants` or `cargo mutants --test-tool nextest` | Focus with `--file` and `--function` flags; nextest mode runs mutants in parallel for large workspaces. Source: [mutants.rs](https://mutants.rs/) |
| .NET | Stryker.NET 4.13+ | `dotnet stryker` | Microsoft Testing Platform (MTP) runner support in preview (Mar 2026); ML-based equivalent-mutant pruning (~30% noise reduction). Source: [stryker-mutator.io/blog/stryker-net-mtp-runner](https://stryker-mutator.io/blog/stryker-net-mtp-runner/) |

## Workflow

```
SCAN    →  confirm the target module already has ≥ 80% line coverage
        →  if not, run `coverage` first — mutation on low coverage is wasted compute

LOCK    →  scope to ONE module (file, package, or function set)
        →  set --timeout, --concurrency, and mutant operator set
        →  record current mutation score as baseline

PING    →  run the tool, classify results:
             Killed / Survived / Timeout / No-coverage / Equivalent
        →  for each surviving non-equivalent mutant:
             – add an assertion that would kill it
             – or tighten an existing assertion's expected value

VERIFY  →  re-run; compute new score; confirm no test was loosened
        →  wire a threshold into the module's CI job
```

## Survived-Mutant Analysis

A surviving mutant shows one of three things:
1. **Weak assertion** — test ran the code but didn't check the outcome. Fix: add / strengthen `expect`.
2. **Missing case** — no test exercised that branch. Fix: add a targeted test.
3. **Equivalent mutant** — the mutated code is functionally identical to the original (e.g., `i <= n` vs `i < n + 1` in an unreachable path). Triage, don't chase.

## Equivalent-Mutant Triage

Equivalent mutants are unavoidable and inflate apparent weakness. Keep a per-module allowlist:

```jsonc
// .stryker-equivalents.json
[
  { "mutator": "EqualityOperator", "file": "src/parser.ts", "line": 42, "reason": "Loop bound; <= and <+1 equivalent here" }
]
```

Review the allowlist during `mutation` handoff to prevent it becoming a dumping ground. Stryker .NET and Meta ACH (2025+) ship ML-assisted equivalent-mutant pruning — prefer tooling over hand-curation at scale.

## CI Integration

Local (module-scoped) thresholds:

- **Critical modules** (payments, auth, data integrity): fail CI under **85% mutation score**, target **95%**.
- **Standard modules**: fail under **60%**, target **75%**.
- **Legacy / exploratory**: measure only; no gate.

PR-tier mutation job: scope to git-diff changed files only; keep wall time < 5 min. Full-suite runs belong to nightly — escalate to Siege for the program design.

```yaml
# .github/workflows/mutation-pr.yml (sketch)
- run: npx stryker run --mutate "$(git diff --name-only origin/main | grep -E '\\.(ts|tsx)$' | xargs)"
- run: node scripts/assert-mutation-score.mjs --min 75
```

## Anti-Patterns

- Running mutation testing on code with < 80% coverage — most survivors will be "no coverage", signal-free noise.
- Chasing 100% mutation score — equivalent mutants make this unachievable; stop at the target.
- Letting mutation runs into the default `push` CI lane without a timeout — full suites can run hours.
- Using mutation score as the only quality signal — it complements, not replaces, branch coverage and property-based tests.
- Ignoring survived mutants in new code while chasing survivors in legacy code — new-code ratchet matters more.

## 2026 Rationale: The AI-Generated-Code Safety Net

By 2026 the empirical case for mutation testing has shifted from "nice-to-have for legacy auditing" to **"required safety net on any module touched by AI codegen"**. Independent reports from 2026 ("Mutation Testing: The Missing Safety Net for AI-Generated Code", `alexop.dev` on Vitest browser mode + AI agents, `johal.in` Stryker .NET / MutPy guide) converge on the same observation:

- AI assistants produce tests that hit lines but **omit meaningful assertions** — `80%` line coverage with weak assertions catches almost nothing.
- Branch coverage cannot distinguish "the test ran the branch" from "the test would notice if the branch's behavior changed". Mutation testing can.
- The mutation algorithm is mechanical enough that an AI coding agent can perform it manually when no tool exists for the language (apply mutant → run test → restore → record).

Operational guidance:

1. **Gate AI-authored modules on mutation score, not branch coverage.** Critical modules: `≥ 85%` mutation score; standard: `≥ 60%`. Branch coverage alone passes too easily on AI-generated suites.
2. **Run mutation testing in the same PR that introduces AI-authored code.** Deferring it to nightly lets the "passes-but-asserts-nothing" failure mode reach main.
3. **Pair with property-based tests** (`fast-check`, Hypothesis, `proptest`) — they kill whole mutant families at once and reduce the assertion-tightening workload.
4. **Use ML-assisted equivalent-mutant pruning** where the tooling supports it (Stryker .NET reports `~30%` noise reduction in 2026 builds) — equivalent mutants compound on AI-generated code because the model often emits semantically redundant guard clauses that are by definition equivalent.

## Pair With

- **Property-based tests** (fast-check, Hypothesis, proptest): hypothesis + mutmut on async code has been reported to lift scores from 70% → 92% (johal.in 2026). Property tests kill whole classes of mutants at once.
- **Branch coverage** — chase uncovered branches first, then run mutation.

## Handoff

- Program-level strategy, operator tuning at scale, tiered CI design → `Siege`.
- Survivors that require production-code refactor to be killable → `Zen`.
- New assertions that require test-data factories → `Mint`.
- Threshold policy / PR-gate governance → `Guardian`.
