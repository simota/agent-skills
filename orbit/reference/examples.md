# Orbit Examples

Purpose: load this when matching a live issue to a known Orbit scenario. Each example is intentionally short and keeps only the details that affect classification, escalation, or required output.

## Contents

1. Verification gap
2. Dirty-start scope risk
3. State drift
4. Contract missing
5. Tool failure
6. Parallel-loop contamination
7. Sequential-loop handoff gap
8. Loop-of-loops inner failure
9. Pre-flight failure
10. Branch-isolation squash

## Scenario Table

| Example | Core input | Expected Orbit result |
|---------|------------|-----------------------|
| A. `VERIFY_GAP` | `done.md` exists, last `progress.md` entry shows failed lint, footer says `DONE` | `status_assessment: VERIFY_GAP`, `recommended_next_action: CONTINUE`, handoff to Radar |
| B. `COMMIT_SCOPE_RISK` dirty start | dirty baseline exists and new iteration changes are scoped to fresh paths | `status_assessment: COMMIT_SCOPE_RISK`, next action is candidate-only staging, handoff to Guardian |
| C. `STATE_DRIFT` | `state.env` says `NEXT_ITERATION=11`, `progress.md` ends at `9` | `status_assessment: STATE_DRIFT`, rebuild state from progress evidence, handoff to Builder |
| D. `CONTRACT_MISSING` | `goal.md` missing, `progress.md` empty, no footer evidence | `severity: P1`, rebuild contract files, emit `NEXUS_LOOP_STATUS: READY`, handoff to Nexus |
| E. `TOOL_FAILURE` | `runner.log` shows repeated executor failure and no new iteration entry | `severity: P2`, classify failures separately, bounded retry first, escalate to `P1` only after budget exhaustion |
| F. Cross-loop `COMMIT_SCOPE_RISK` | parallel loops stage each other's files | `severity: P1`, unstage, isolate scopes per loop, handoff to Guardian |
| G. Sequential handoff gap | successor loop says "continue from loop-1" but has no measurable ACs or handoff checklist | `severity: P1`, rebuild successor contract, trigger `ON_GOAL_CONTRACT_WEAK`, handoff to Nexus |
| H. Loop-of-loops scoped failure | inner loop fails repeatedly while outer loop continues | `severity: P1`, classify inner failure independently, update outer progress, do not start dependent inner loops |
| I. `PREFLIGHT:FAIL` | disk below `100MB`, stale lock exists, checksum valid | stale lock auto-clears, disk failure aborts run before iteration start |
| J. Branch-isolation squash | `BRANCH_ISOLATION=true`, `SQUASH_ON_DONE=true`, verify `PASS`, iter branch has 8 commits | squash to summary branch, commit once, delete iteration branch, final footer `DONE` |

## Notes

- Example D preserves the `ON_GOAL_CONTRACT_WEAK` trigger because it changes contract recovery behavior.
- Example G preserves sequential handoff enforcement because it distinguishes "done file exists" from "prerequisites independently verified."
- Example I preserves the `100MB` pre-flight threshold and stale-lock auto-clear behavior.
- Example J preserves the `BRANCH_ISOLATION` plus `SQUASH_ON_DONE` completion path.
