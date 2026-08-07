# Testing Research Rationale

Purpose: full rationale, examples, and source citations behind the compressed Core Contract bullets in SKILL.md. Read this when you need to justify a testing decision with evidence, not just apply the rule.

## Verification-first is the dominant practice

Anthropic's Claude Code best practices name verification the "single highest-leverage thing" you can give an AI coding agent. Lock the verifier (test, snapshot, screenshot, expected stdout, type signature, schema) *before* implementation lands; never accept code whose verifier was written by the same model that wrote the code. [Source: code.claude.com/docs/en/best-practices]

## Detect Tautological Tests and Coverage Hacking

When code and tests are both AI-generated, blind spots are shared and `100%` line coverage can hide a mutation score as low as `20.32%` (≈ 80% latent bugs undetected). Reject any test that matches one of the canonical Tautological Test patterns: (1) asserts only that a field exists, (2) asserts only that a call happened, (3) asserts only "no exception was thrown", (4) mirrors the implementation's exact arithmetic, (5) only checks length / count, (6) uses snapshot as the sole oracle. Require at least one behavioural assertion per public path. [Source: codeintelligently.com — AI Generated Tests False Confidence; keelcode.dev — AI Tests Safety Illusion]

## Use Mutation Score as the ceiling, not Coverage

Coverage is a Goodhart-vulnerable floor metric (target → tautological tests). Mutation score (Stryker / mutmut / Pitest) is the ceiling that measures whether tests actually *catch* defects. Recommended thresholds: `break: 50`, `low: 60`, `high: 80`. Teams hitting `high: 80` in CI report ~70% fewer production bugs vs coverage-only teams. Apply mutation gate to changed files only (incremental mutation) to keep CI under 5 minutes. [Source: stryker-mutator.io/docs; medium.com/@jaychopra05 — 100% Code Coverage Is a Lie]

## FlakyGuard-class auto-repair for flaky tests

Uber Go monorepo results: 47.6% repair / 51.8% acceptance / SOTA +22pp. Never auto-fix in a CI loop — the agent must propose a diff to a human-reviewable branch. Standardise the flaky root-cause taxonomy: (a) test-order dependency, (b) async/timer race, (c) network/clock non-determinism, (d) DB state leak, (e) random seed leak, (f) parallelisation contention. Datadog Bits AI Dev Agent extends this with trace-history-driven PR triggers when the flaky case correlates with a production span. [Source: emergentmind.com — FlakyGuard; datadoghq.com — Bits AI Test Optimization]

## Metamorphic Relations solve the Oracle Problem

When the expected output is hard to compute but a transformation-of-input → transformation-of-output relationship is known, encode it as a metamorphic relation: e.g. `sort(reverse(xs)) ≡ sort(xs)`, `f(x + 0) ≡ f(x)`, `serialize(deserialize(s)) ≡ s` (round-trip). Metamorphic testing complements property-based testing — PBT generates inputs, metamorphic relations supply the oracle. Adoption is still low in the LLM-testing literature (4 of 36 oracle-automation studies), so this is a high-leverage axis to introduce. [Source: dl.acm.org/doi/10.1145/3798226; arxiv.org/html/2405.12766v1]

## Flaky-rate and coverage benchmarks (Critical Constraints elaboration)

- Flaky-rate guidance: healthy `< 1%`, investigation trigger `> 2%` over rolling window, warning `1-5%`, critical `> 5%` (Source: TestDino Benchmark 2026). In large industrial projects, 11–27% of tests exhibit flaky behavior, accounting for 5–16% of build failures (Source: Ranorex 2026, Harness 2026). Team-level prevalence is growing: 26% of teams experienced test flakiness in 2025, up from 10% in 2022 (Source: Bitrise Mobile Insights 2025).
- Top 3 flaky root causes, in priority order: (1) async wait/timing issues, (2) concurrency and shared state (up to 15% of flaky failures in large CI pipelines, Source: Ranorex 2026), (3) test order dependency (Source: accelq.com, TestDino 2026).
- Flaky cost benchmark: flaky tests consume ~2.5% of developer productive time (~1 FTE per 50 engineers); quantify team-specific cost to justify quarantine investment (Source: Atlassian Engineering 2026). Google reports 16% and Microsoft 13% of all test failures are flaky. 84% of CI pass-to-fail transitions at Google are caused by flaky tests, not real regressions (Source: Google Testing Research) — most "failures" engineers investigate are noise, making quarantine ROI extremely high.
- Mutation score guidance: `90%+` excellent, `75-89%` good, `60-74%` acceptable, `< 60%` poor. Pair property-based tests with mutation testing to boost scores — hypothesis + mutmut improved async code scores from 70% → 92% (Source: johal.in 2026).
- Test Impact Analysis (TIA) and predictive test selection: enterprise deployments report up to 80% faster test execution and 40% shorter build times (Source: CloudBees Smart Tests 2026, Frontiers AI-augmented CI/CD 2026). Evaluate platform-native TIA (Azure DevOps, CloudBees, Launchable) before building custom selection logic.
- Modern CI platforms (Bitbucket, Harness) now offer built-in AI-powered flaky detection and auto-quarantine — leverage platform-native capabilities before building custom solutions (Source: Atlassian Engineering 2026, Harness 2026).

## Additional test-layer detail (Test Mix section elaboration)

- Property-based testing pairing with mutation testing boosts kill scores from 70% to 92% on async code (Source: johal.in 2026). Use `fast-check` 4.x (JS/TS; `@fast-check/vitest` for Vitest integration), `hypothesis` (Python), `proptest` (Rust). See [fast-check.dev](https://fast-check.dev/) for current API.
- Mutation testing: StrykerJS 7.0+ supports Vitest and Node Tap runners natively (Source: [stryker-mutator.io/blog/announcing-stryker-js-7](https://stryker-mutator.io/blog/announcing-stryker-js-7/)). Watch for equivalent mutants (false survivors) and tool-specific timeouts in distributed CI (>200ms latency causes Stryker .NET failures; apply exponential backoff, Source: johal.in 2026). Stryker .NET now uses ML to prune equivalent mutants, reducing noise by 30% (Source: johal.in 2026). Agentic mutation tools (mewt for Rust/Solidity) enable LLM-guided mutant generation targeting high-risk code paths (Source: Trail of Bits 2026).
- AI-assisted test generation: LLM-powered mutation testing (e.g., Meta ACH) generates targeted tests for undetected faults, making mutation testing practical at enterprise scale (Source: Meta Engineering 2025, momentic.ai 2026). AI-assisted flaky repair (FlakyGuard) achieves 47.6% automated repair rate with 51.8% developer acceptance on reproducible flaky tests (Source: ASE 2025).
