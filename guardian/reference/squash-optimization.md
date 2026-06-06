# Squash Optimization Reference

Purpose: Score adjacent commits, group squash candidates, synthesize better messages, and keep attribution and rollback safety intact.

## Contents

- Pairwise scoring
- Decision thresholds
- Group detection
- Message synthesis
- Sequence optimization
- Verification and rollback
- Orbit boundary

## Pairwise Scoring

Evaluate adjacent commit pairs across six weighted factors:

| Factor | Weight | Important rules |
|--------|--------|-----------------|
| Temporal proximity | `15` | same minute `+15`, within `10m` `+12`, beyond `1 week` `-5` |
| Subject relationship | `25` | identical prefix `+25`, WIP/fixup `+20+`, opposing concerns `-15`, different logical units `-25` |
| File overlap | `20` | full overlap `+20`, high overlap `+15`, no overlap `-5`, lockfile-only `-10` |
| Author attribution | `15` | same author `+15`, different author `-10`, multi-author chain `-15` |
| Atomicity impact | `15` | improves atomicity `+15`, breaks bisectability `-15` |
| Test coupling | `10` | test with implementation `+10`, standalone test `-5` |

## Decision Thresholds

```yaml
squash_thresholds:
  strong_squash: ">= +30"
  suggest_squash: "+15 to +29"
  neutral: "-14 to +14"
  keep_separate: "<= -15"
```

Force squash examples:
- `WIP`
- `fixup!`
- `squash!`
- `tmp`
- `forgot`
- `oops`
- `fix typo`
- `address review`

Force keep examples:
- unrelated authors without attribution
- lockfile-only commits
- security commits
- revert commits

## Group Detection

Group using:
1. pairwise scores
2. logical concern consistency
3. author safety
4. file overlap
5. bisectability

Limits:
- warning at `5` commits or `20` files per group
- hard max `8` commits or `30` files per group
- if `>3` distinct concerns appear, split the group

## Message Synthesis

Message construction rules:
- choose the strongest non-noise anchor commit
- preserve scope and intent
- add `Co-authored-by:` when attribution matters
- explain rationale in the body only when useful

## Sequence Optimization

Default flow:
1. detect noise commits
2. score adjacent pairs
3. form candidate groups
4. generate synthesized commit messages
5. produce a rebase plan or keep-separate advice

## Verification and Rollback

Immediate checks:
- diff integrity
- build or test verification when available
- author attribution preserved

Rollback plan:
- create a backup branch before rewrite
- reset to backup if post-squash verification fails

CI recommendation:
- rerun the relevant build/test gate after squash

## Orbit-Guardian Squash Boundary

Orbit owns loop-iteration squash execution.

Guardian owns:
- non-loop squash analysis
- PR-preparation squash advice
- message synthesis
- attribution review
- post-squash verification guidance
