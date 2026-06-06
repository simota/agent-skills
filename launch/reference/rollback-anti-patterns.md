# Rollback & Recovery Anti-Patterns

Purpose: Use this file when you need rollback design, database migration safety, recovery timing, or post-rollback obligations.

## Contents

1. Rollback anti-patterns
2. Why DB rollback is hard
3. Forward-compatible migration pattern
4. Layered rollback model
5. Post-rollback process
6. Launch enforcement points

## 1. Rollback Anti-Patterns

| ID | Anti-pattern | What goes wrong | Guardrail |
|----|--------------|-----------------|-----------|
| `RB-01` | Untested rollback | First real rollback fails in production | Test rollback in staging before release |
| `RB-02` | Optimistic DB rollback | Down migrations fail in partial states | Prefer forward-compatible migrations; use backup / restore for true DB recovery |
| `RB-03` | Ignoring data loss | Recreated columns do not restore deleted data | Delay destructive removal by `2 releases` |
| `RB-04` | Unknown rollback time | SLA and incident decisions become guesswork | Measure RTO per rollback method |
| `RB-05` | Single rollback method | One failed method leaves no safe fallback | Keep multiple rollback options ready |
| `RB-06` | No forward plan after rollback | Teams stop at recovery and delay the real fix | Create the next-step plan within `24 hours` |
| `RB-07` | Ignoring stateful resources | App rollback leaves DB, cache, or queue inconsistent | Include all stateful resources in rollback planning |

## 2. Why DB Rollback Is Hard

Main issues:

- partial migration application
- data loss on destructive changes
- deployment version and DB state drift

Operational rule:

- do not assume down migrations are safe enough to be the primary recovery plan

## 3. Forward-Compatible Migration Pattern

### Expand-Contract

1. `Expand`
   - add new schema elements
   - keep old structure working
2. `Migrate`
   - copy or transform data
   - cut reads and writes over progressively
3. `Contract`
   - remove old structure `1-2 releases later`

Benefits:

- app rollback often avoids DB rollback
- destructive changes are delayed
- data loss risk is reduced

### Fast recovery pattern

- apply DB changes before app rollout when they are forward-compatible
- roll back only the app first
- postpone destructive DB cleanup

## 4. Layered Rollback Model

| Level | Method | RTO | Risk | Use when |
|-------|--------|-----|------|---------|
| `L1` | feature flag disable | `< 1 minute` | very low | feature is flag-controlled |
| `L2` | deployment / container rollback | `2-5 minutes` | low | DB unchanged or forward-compatible |
| `L3` | config revert + traffic shift | `5-15 minutes` | medium | blue-green or canary environment exists |
| `L4` | DB restore + full rollback | `15-60 minutes` | high | DB change is incompatible |

Escalation rule:

- if only `L4` is viable, require stakeholder approval

## 5. Post-Rollback Process

### Immediate

- verify service health
- notify stakeholders
- create incident ticket
- assess blast radius

### Within `24 hours`

- identify root cause
- define forward fix or next-release plan
- analyze why pre-release validation missed it

### Within `1-7 days`

- run postmortem
- update tests, release gates, and rollback plan

## 6. Launch Enforcement Points

- Block release if rollback test is missing (`RB-01`).
- Recommend `Expand-Contract` for DB changes that would otherwise rely on unsafe down migrations (`RB-02`).
- Delay destructive schema cleanup by `2 releases` where possible (`RB-03`).
- Require multiple rollback methods (`RB-05`).
- Require stakeholder approval for `L4` rollback scenarios.
