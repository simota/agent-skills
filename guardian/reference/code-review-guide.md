# Code Review Guide

Purpose: Keep Guardian's reviewer recommendations aligned with practical review focus, turnaround goals, and ownership rules.

## Contents

- Human vs automated review focus
- CODEOWNERS defaults
- Turnaround targets
- AI-assisted review usage
- Anti-patterns

## Focus Separation

| Human reviewers should focus on | Automation should handle |
|---------------------------------|--------------------------|
| correctness and logic | style and formatting |
| design and architecture | static analysis |
| security-sensitive behavior | dependency vulnerability scans |
| performance implications | routine test execution |
| readability and maintainability | repeatable lint checks |

## CODEOWNERS Guidance

Example:

```text
# .github/CODEOWNERS
/src/compiler/    @my-org/compiler-team
/src/frontend/    @my-org/frontend-team
/src/api/         @my-org/backend-team
*.sql             @my-org/dba-team
package.json      @my-org/platform-team
pnpm-lock.yaml    @my-org/platform-team
```

Rules:
- GitHub uses `last-match-wins`.
- Prefer team-based ownership over a single named reviewer.
- Require platform review for dependency or lockfile changes.

## Turnaround Targets

| Metric | Elite benchmark | Guardian target |
|--------|-----------------|-----------------|
| Time to first review | `< 4h` | `<= 4h` |
| Time to merge | `< 6h` | `<= 24h` |

Most effective lever:
- keep PR size near `200-400` lines when possible

## AI-Assisted Review

Use AI as a first-pass assistant, not the final decision-maker.

Typical tools:
- `CodeRabbit`
- `GitHub Copilot`
- `Cursor Bugbot`
- `Claude Code`

Recommended split:
- AI finds routine issues and suspicious patterns
- humans decide architecture, intent, risk, and tradeoffs

## Anti-Patterns

| Pattern | Why it hurts | Safer alternative |
|---------|--------------|-------------------|
| rubber stamping | no real review signal | require meaningful comments or checklist completion |
| bike shedding | time wasted on low-value debate | push style debate to linters and formatter rules |
| knowledge silos | review bottlenecks and fragility | rotate ownership and enforce CODEOWNERS coverage |
| over-helping | reviewer rewrites instead of reviewing | give direction, let the author apply the fix |
| endless "one more thing" requests | scope creep during review | log follow-up issues for non-blocking work |
| self-merge without review | quality gate bypass | protect branches and require approval |
