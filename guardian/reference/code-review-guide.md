# Code Review Guide

Purpose: Keep Guardian's reviewer recommendations aligned with practical review focus, turnaround goals, and ownership rules.

## Contents

- Human vs automated review focus
- CODEOWNERS defaults
- Turnaround targets
- AI-assisted review usage
- Anti-patterns

## Magnification Alignment

Comments talk past each other when reviewers read the same diff at different magnifications. Before commenting, establish which level the change is *asking* about — from the PR's `## Review focus` block when present (`pr-workflow-patterns.md`), otherwise inferred from the diff:

| Level | The question at this level |
|-------|---------------------------|
| Statement / function | Does this branch preserve the invariant? |
| Module / type | Are the responsibility split and dependency direction sound? |
| Service / contract | What happens to the published contract and its failure modes? |
| Team / org | What does this require of another team's release, ownership, or on-call? |

Two rules follow:

- **Do not require equal depth at every level.** Concentrate on the levels where reversibility is low (persisted state, published contracts, security boundaries) — these are the ones a follow-up PR cannot undo.
- **Weight the review by decision weight, not by diff size.** A one-line change to an identity model, a retention rule, or a public error contract outweighs a 400-line internal refactor. Line count is a proxy for reading time, never for consequence.

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
| sizing review by diff line count | a one-line identity/schema/contract change outranks a 400-line refactor | size the review by blast radius and reversibility |
| approval count treated as evidence | many approvers, no one owning the operational outcome (review theater) | name one decision owner and one operational owner |
