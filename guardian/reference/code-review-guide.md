# Code Review Guide

Purpose: Keep Guardian's reviewer recommendations aligned with practical review focus, turnaround goals, and ownership rules.

## Contents

- Human vs automated review focus
- Review reconstruction cost
- Approval scope
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

## Review Reconstruction Cost

Before a reviewer can judge anything, they rebuild context the diff does not carry. That rebuilding is most of the slow part of a slow review, and it is a property of the PR and the system — not of how fast the reviewer reads. Diagnose it by symptom:

| What is being rebuilt | Symptom | Fix in the PR, not in the reviewer |
|-----------------------|---------|-------------------------------------|
| Problem | "what breaks today?" gets re-asked in the thread | state the failure and its trigger in `## Summary` |
| Baseline | reviewer reconstructs current behavior from the diff | before/after, or a characterization test |
| Intent | comments evaluate the implementation, never the goal | one sentence of intent that the tests and metrics trace back to |
| Diff navigation | the same files are opened repeatedly | declare a reading order; isolate mechanical commits |
| Architecture | structural debate begins *after* review starts | hoist the decision to design review; link the ADR |
| Evidence | test names do not say what they prove | map each claim to the test that supports it |
| Operations | no one can say how a post-merge failure would be noticed | name the signal and the stop condition |

Diagnostic: if a reviewer cannot say **what they need to check** within the first few minutes, fix the intent–boundary–evidence connection before touching the diff. More description is not the fix — a shorter path to the decision is. A PR body that grows past the point where `## Review focus` is findable has raised reconstruction cost, not lowered it.

## Approval Scope

An approval records that *one reviewer*, against *the diff at that moment*, judged *a stated range* safe to proceed. It is not a correctness certificate, and stacking more of them does not make it one — approvals from eight code owners who each read one file leave the integration unjudged, which is how a fully-approved PR ships with nobody having looked at the data flow.

On boundary-crossing or specialist-routed PRs, reviewers state the range:

```
Approved:      API compatibility · failure semantics · test strategy
Not reviewed:  query performance under production volume · rollout dashboard
```

- `Not reviewed` is the load-bearing half — it is what stops "someone must have checked that".
- Name one **integrator** who owns the change as a whole whenever more than two reviewers are involved; local owners approve regions, the integrator approves the change.
- Re-approval is decided by whether the *judgment* changed, not by diff size: behavior, contract, risk, or evidence moved; a reviewed file gained semantic changes; conflicts were hand-resolved; the base moved and the integration result differs. A one-line change that invalidates the reasoning needs re-approval; a comment typo fix does not.

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
| sizing review by diff line count | a one-line identity/schema/contract change outranks a 400-line refactor | size the review by blast radius and reversibility; use line count only to budget reading time (`SKILL.md` § PR size principle — two sizes, two uses) |
| splitting a mechanical diff to satisfy a line threshold | strands the codebase in a mixed old/new state across many PRs and makes completeness unverifiable | keep it whole; review the transformation rule and exclusions (`pr-split-strategy.md` § Visual Size Exception) |
| approval count treated as evidence | many approvers, no one owning the operational outcome (review theater) | name one decision owner and one operational owner |
