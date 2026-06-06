# Atomic Step Decomposition Reference

Purpose: Break tasks into ≤15-minute atomic steps that pass the INVEST checklist. Each step has a testable exit criterion, a reversibility classification, and an explicit commit-point contract. Eliminates the "6-hour mega-step" anti-pattern.

## Scope Boundary

- **sherpa `atomic`**: ≤15-minute step contracts, INVEST check, reversibility classification (this document).
- **sherpa `epic` (elsewhere)**: Top-level epic breakdown. Default entry; atomic-step depth happens inside.
- **sherpa `story` (elsewhere)**: Feature-level story decomposition. One story → multiple atomic steps.
- **sherpa `walking-skeleton` (elsewhere)**: Thinnest end-to-end slice. Often the first atomic step of a greenfield epic.
- **sherpa `vertical-slice` (elsewhere)**: End-to-end slice orientation. Atomic steps live inside vertical slices.

## INVEST Checklist per Step

| Letter | Criterion | Check |
|--------|-----------|-------|
| I | Independent | No other in-progress step blocks this one |
| N | Negotiable | Details can be refined; scope is clear |
| V | Valuable | Moves the epic forward in a concrete way |
| E | Estimable | You can predict time within ± 30% |
| S | Small | ≤ 15 minutes at the target pace |
| T | Testable | Has a single, observable exit criterion |

If a step fails any letter, **decompose further** or **re-scope**.

## Step Contract Template

```markdown
### Step [N]: [Name]

- **Goal**: [one-sentence outcome]
- **Size**: ≤ 15 min
- **Prerequisite**: [Step N-1 complete OR "none"]
- **Exit criterion**: [single observable test — "X file exists with Y content", "test Z passes", "URL W returns 200"]
- **Reversibility**: [reversible / expand-contract / one-way]
- **Agent**: [Builder / Scout / Judge / ...]
- **Commit point**: [yes / no / conditional]
- **Rollback plan**: [how to undo if this goes wrong]
```

## Reversibility Classification

| Class | Definition | Commit strategy |
|-------|-----------|-----------------|
| Reversible | Pure code / config that can be reverted with `git revert` | Commit freely |
| Expand-contract | Schema or API additions; must complete contract phase before removal | Commit after expand + test; contract in separate step |
| One-way | Data deletion, destructive migration, external-system state change | Approval gate + snapshot before commit |

Every atomic step must declare its class. One-way steps require explicit operator approval before execution.

## Commit Point Contract

Default rule: **commit after every reversible green step** unless:
- The step is mid-refactor and tests don't pass yet.
- The next step immediately amends this one's code and is < 5 min.

Explicit commit-point markers:

```
[ ] Step 1 — install dependency          [commit: yes]
[ ] Step 2 — add type definitions         [commit: yes]
[ ] Step 3 — implement getUser()          [commit: after tests pass]
[ ] Step 4 — wire into router             [commit: yes]
[ ] Step 5 — add integration test         [commit: yes]
[ ] Step 6 — deploy to preview env        [commit-point irrelevant; deploy is the action]
```

## Decomposition Heuristics

### Time-Box First

If a task is "> 1 hour" or "I don't know", break it down.

### Find the Single Test

What is the one thing you would observe to say "this step is done"? That is your exit criterion. If you need two tests, it's two steps.

### Separate Creation from Modification

- Step A: create the file
- Step B: add the logic
- Step C: wire in the caller
- Step D: add tests

Each is independently testable and commit-worthy.

### Separate Code from Config

- Step X: write the function
- Step Y: add the environment variable / feature flag
- Step Z: enable in staging

### Separate Happy Path from Error Handling

- Step M: happy path works
- Step N: error case 1 handled
- Step O: error case 2 handled

Each error case is a discrete, testable step.

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| "Implement feature X" as one step | Break into creation / logic / wiring / tests |
| "Refactor module Y" | Split into individual small refactors with tests in between |
| Step with no exit criterion ("improve performance") | Add concrete metric ("reduce P95 from 500ms to 200ms") |
| 3+ hour "investigation" step | Time-box to 30 min; if not done, step is "document findings and re-plan" |
| Mixing reversible and one-way in one step | Always isolate one-way |
| No commit between steps | Lose progress on failure; commit freely |
| "TBD" dependencies | Resolve before breaking down; otherwise mark as blocked |

## Example Decomposition

### Input (too big)

> "Add user authentication with OAuth, email verification, and 2FA."

### Output (atomic steps)

```
Walking skeleton (first):
1. Add OAuth redirect endpoint (thinnest) — 10 min — Builder
2. Hardcode test provider that always succeeds — 5 min — Builder
3. Wire login button → redirect → callback → session cookie — 15 min — Builder
4. E2E test: click login, land on dashboard — 10 min — Voyager
5. [COMMIT: "feat(auth): walking skeleton login"]

Real OAuth:
6. Add Google OAuth provider config — 10 min — Builder
7. Replace hardcoded provider — 10 min — Builder
8. Handle OAuth error response — 10 min — Builder
9. Add OAuth integration test — 10 min — Radar
10. [COMMIT: "feat(auth): google oauth"]

Email verification:
11. Add verification token schema (expand) — 10 min — Schema
12. Add send-verification endpoint — 15 min — Builder
13. Add verify-token endpoint — 15 min — Builder
14. Gate login on verified_at not null — 5 min — Builder
15. Add integration test — 15 min — Radar
16. [COMMIT: "feat(auth): email verification"]

2FA:
17. Add TOTP secret schema (expand) — 10 min — Schema
18. Add enable-2fa endpoint — 15 min — Builder
19. Add verify-2fa endpoint — 15 min — Builder
20. Add 2fa gate at login — 10 min — Builder
21. Add integration test — 15 min — Radar
22. [COMMIT: "feat(auth): totp 2fa"]

Reversibility:
- Steps 1-10: reversible (code + new feature)
- Steps 11, 17: expand-contract (new nullable columns)
- No one-way steps in this decomposition
```

## Quality Gate Before Starting

Before handing an atomic step to an executor (Builder / Scout / Radar):

- [ ] All INVEST letters pass.
- [ ] Exit criterion is a single observable fact.
- [ ] Reversibility classified.
- [ ] Commit-point decision made.
- [ ] No unresolved prerequisite.
- [ ] Target agent identified.
- [ ] Time-box ≤ 15 min.
- [ ] If one-way: approval gate documented.

## Deliverable Contract

When `atomic` completes, emit:

- **Step list** with full contract per step (name, goal, size, prerequisite, exit criterion, reversibility, agent, commit point, rollback).
- **Walking-skeleton identification** (which step is the thinnest end-to-end).
- **Commit-point plan** (explicit markers between steps).
- **Reversibility summary** (count of reversible / expand-contract / one-way).
- **Handoff**: Builder (default execution), Scout (investigation-first), Radar (testing-first).

## References

- Bill Wake — "INVEST in Good Stories, and SMART Tasks"
- Kent Beck — "Test-Driven Development by Example" (small steps)
- Dave Farley / Jez Humble — "Continuous Delivery" (small, reversible changes)
- Mayer Coglan — Refactoring in ≤ 10-minute steps
- Allen Holub — Small batch sizes in software development
- DORA 2025 — State of AI-Assisted Software Development: PR size up 51%, review time up 441%; small atomic commits directly counteract this trend. [dora.dev/research/2025/dora-report/](https://dora.dev/research/2025/dora-report/)
- SAFe 6.0 / "Reimagining SAFe" (2024–2025) — Story refinement: features broken into user stories with owners, acceptance criteria, estimates, tasks, risks, and dependencies. [framework.scaledagile.com/whats-new-in-safe-6-0/](https://framework.scaledagile.com/whats-new-in-safe-6-0/)
