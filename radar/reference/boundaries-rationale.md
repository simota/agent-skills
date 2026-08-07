# Boundaries Rationale

Purpose: full justification and source citations behind the compressed `Never` list in SKILL.md. The SKILL.md list states the rule; this file explains why.

- **Write assertion-free tests** — surviving mutants show 41.62% of weak tests fail to exercise assertion boundaries adequately (Source: IEEE ICST 2026 Mutation Workshop — https://conf.researchr.org/home/icst-2026/mutation-2026).
- **Use arbitrary delays such as `waitForTimeout`** — async wait/timing issues are the #1 cause of flaky tests, with academic research finding 45% of all flaky test fixes address async timing (Source: TestDino Flaky Test Benchmark 2026, accelq.com 2026). Use `waitFor`, `findBy*`, deterministic clocks, or explicit retry with context instead.
- **Depend on external services without mocks or stubs** — third-party instability cascades into false failures and blocks CI pipelines.
- **Train teams to ignore test results by leaving flaky tests in the main pipeline** — quarantine immediately and fix in dedicated sessions.
- **Let AI agents auto-fix flaky failures in CI loops without verifying flaky vs. real regression first** — autonomous retry-fix cycles cause regression cascades (observed pattern: multiple iterations, zero real bugs fixed, introduced regressions and wasted compute). Always confirm the failure is a genuine regression before applying code changes (Source: Frontiers AI-augmented CI/CD 2026).
