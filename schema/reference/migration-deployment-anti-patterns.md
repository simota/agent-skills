# Migration And Deployment Anti-Patterns

Purpose: Use this file when planning risky schema changes, zero-downtime rollout, or rollback strategy.

Contents:
1. Core anti-patterns
2. Zero-downtime phases
3. Dangerous `ALTER TABLE` operations
4. Expand-contract detail
5. Preflight gates

## Core Anti-Patterns

| ID | Anti-pattern | Signal | Safer pattern |
|----|--------------|--------|---------------|
| `MD-01` | Big Bang Migration | One giant migration mixes unrelated changes and becomes hard to rollback | Split into staged, reversible steps |
| `MD-02` | Table Lock Blindness | Blocking `ALTER TABLE` runs on hot or large tables | Prefer nullable add, concurrent index build, online tools, or phased rollout |
| `MD-03` | No Rollback Plan | No `down`, no backup note, no revert test | Require `up`/`down` or explicit backup-required label |
| `MD-04` | Schema + Data Migration Mixed | DDL and heavy data rewrite happen in the same step | Separate schema change from data backfill |
| `MD-05` | Inadequate Planning | No impact map, no dependency review, no staging rehearsal | Review dependencies and rehearse on production-like data |
| `MD-06` | CDC Ignorance | Backfill finishes but new writes are missed | Use CDC, replay, or dual-write during cutover |
| `MD-07` | Observability Gap | No row-count, checksum, lag, or app-health checks | Add live metrics and post-cutover verification |

## Zero-Downtime Phases

| Phase | Goal | Required controls |
|------|------|-------------------|
| Preparation | Understand impact | dependency map, rollback note, rehearsal |
| Bulk load | Move baseline data | bulk copy, defer secondary index work where possible |
| CDC | Keep source and target aligned | lag monitoring, integrity checks |
| Dual writes | Prove new path safely | old+new writes, read verification |
| Cutover | Switch traffic safely | stronger monitoring for `24-48h`, archive old path later |

## Dangerous `ALTER TABLE` Operations

| Operation | Risk | Safer path |
|-----------|------|------------|
| Type change | `ACCESS EXCLUSIVE` risk in PostgreSQL | expand-contract or shadow column |
| `SET NOT NULL` on populated table | table scan / lock risk | add `CHECK ... NOT VALID`, validate, then `SET NOT NULL` |
| `DROP COLUMN` / `DROP TABLE` | destructive, backup-required | phased deprecation, backup, delayed removal |
| Default add on old PostgreSQL | full rewrite risk on PG `<11` | staged approach or engine-aware plan |

Safe PostgreSQL `NOT NULL` path:

```sql
ALTER TABLE t
  ADD CONSTRAINT chk_col_nn CHECK (col IS NOT NULL) NOT VALID;

ALTER TABLE t
  VALIDATE CONSTRAINT chk_col_nn;

ALTER TABLE t
  ALTER COLUMN col SET NOT NULL;

ALTER TABLE t
  DROP CONSTRAINT chk_col_nn;
```

## Expand-Contract Detail

1. Expand: add the new structure and keep it nullable.
2. Dual-write or sync while the app can still read the old field.
3. Backfill in batches for large tables.
4. Validate data and add stricter constraints.
5. Switch reads.
6. Drop the old structure only after verification.

## Preflight Gates

- Migration file is `100+` lines -> split it unless every step is tightly coupled
- Large table (`1,000,000+` rows) + blocking change -> require online strategy or ask-first
- No `down` or no backup-required note -> block the migration
- DDL mixed with heavy backfill -> separate the steps
- No monitoring plan -> add row-count, checksum, lock, and health checks
