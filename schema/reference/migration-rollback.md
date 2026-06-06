# Migration Rollback Reference

Purpose: Design reverse-migration DDL and data-recovery plans for every forward migration. Ensure every production-deployed migration has a tested rollback path before deploy.

## Contents

- Rollback readiness checklist
- Reversible vs destructive changes
- Dual-write and expand-contract
- Backfill strategy
- Command recipes
- Anti-patterns

## Rollback Readiness Checklist

Before approving any migration:

- [ ] Reverse DDL script exists
- [ ] Data restoration plan for dropped data (backup / dual-write / re-derivation)
- [ ] Dual-write window documented for schema changes visible to application
- [ ] Tested on staging clone of production data volume
- [ ] Rollback SLO defined (e.g., ≤ 15 min for P0, ≤ 1 h for P1)
- [ ] Downstream systems (replicas, analytics, caches) handled

If any item fails, **Ask First** before deploy.

## Reversible vs Destructive

| Change | Reversible? | Strategy |
|--------|-------------|----------|
| `ADD COLUMN ... NULL` | ✓ | `ALTER TABLE t DROP COLUMN c` |
| `ADD COLUMN ... NOT NULL DEFAULT x` | ✓ | drop column |
| `ADD COLUMN ... NOT NULL` (no default) | ✓ only if column unpopulated | drop column |
| `CREATE INDEX` | ✓ | `DROP INDEX` |
| `CREATE TABLE` | ✓ | `DROP TABLE` |
| `DROP COLUMN` | **destructive** | needs data backup + recovery plan |
| `DROP TABLE` | **destructive** | needs backup + recovery plan |
| `ALTER COLUMN TYPE` (lossy cast) | **destructive** | needs expand-contract |
| `RENAME COLUMN` | ✓ | `ALTER TABLE t RENAME COLUMN x TO y` |
| `ADD FOREIGN KEY` | ✓ | `DROP CONSTRAINT` |
| `ADD CHECK CONSTRAINT` | ✓ | `DROP CONSTRAINT` |
| `UPDATE` (data migration) | **destructive** | needs before-state backup |
| `TRUNCATE` | **destructive** | needs full backup |

Destructive migrations **must** use expand-contract + dual-write (see below).

## Expand-Contract Pattern

For any column rename, type change, or drop:

```
Phase 1 (EXPAND):
  - Add new column/table alongside old
  - App writes to BOTH old and new (dual-write)
  - App reads from OLD (stable)

Phase 2 (BACKFILL):
  - Batch-copy historical old → new
  - Verify row counts + sample integrity

Phase 3 (CUTOVER):
  - App reads from NEW
  - Keep dual-write for grace period (1-7 days)
  - Monitor for discrepancies

Phase 4 (CONTRACT):
  - Stop writing to OLD
  - After confidence window (7-30 days), drop OLD
```

Rollback from any phase:
- Phase 1/2: drop new column (old still authoritative)
- Phase 3: revert read switch (data still in both)
- Phase 4: **not rollbackable without restore** — never skip confidence window

## Dual-Write Implementation

Application-side (most common):

```python
def save_user(user):
    # Phase 1-3: write to both
    db.execute("UPDATE users SET email = %s WHERE id = %s", email, id)
    db.execute("UPDATE users SET email_v2 = %s WHERE id = %s", email_new_format, id)
    # Phase 4: stop old write
```

Trigger-based (when app can't be changed):

```sql
CREATE FUNCTION sync_email_to_v2() RETURNS TRIGGER AS $$
BEGIN
  NEW.email_v2 = normalize(NEW.email);
  RETURN NEW;
END; $$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_email
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION sync_email_to_v2();
```

## Backfill Strategy

For large tables (> 1M rows), batch with progress tracking:

```sql
-- Resumable batch update
DO $$
DECLARE
  last_id BIGINT := 0;
  batch_size INT := 10000;
  rows_updated INT;
BEGIN
  LOOP
    UPDATE users
    SET email_v2 = normalize(email)
    WHERE id > last_id AND email_v2 IS NULL
    AND id <= last_id + batch_size;

    GET DIAGNOSTICS rows_updated = ROW_COUNT;
    EXIT WHEN rows_updated = 0;

    last_id := last_id + batch_size;
    COMMIT;  -- release locks, avoid bloat
    PERFORM pg_sleep(0.1);  -- throttle
  END LOOP;
END $$;
```

Verify:

```sql
-- Row count match
SELECT COUNT(*) FROM users WHERE email_v2 IS NULL AND email IS NOT NULL;
-- Expect 0
```

## Command Recipes

### Version-controlled migrations

Tool examples:
```bash
# Flyway
flyway migrate
flyway undo              # requires paid Teams edition

# Alembic (Python)
alembic upgrade head
alembic downgrade -1     # reverse last migration

# Liquibase
liquibase update
liquibase rollbackCount 1

# Rails / ActiveRecord
rails db:migrate
rails db:rollback STEP=1

# Prisma
npx prisma migrate resolve --rolled-back <migration_name>
```

### PITR (point-in-time recovery) as last resort

```bash
# Postgres WAL-based PITR (requires continuous archiving)
pg_basebackup ... + restore WAL up to timestamp
```

Never rely on PITR as first-line rollback — RTO/RPO too large.

## Rollback Plan Template

```markdown
# Migration: 20260424_add_billing_email

## Forward
```sql
ALTER TABLE users ADD COLUMN billing_email VARCHAR(255);
CREATE INDEX idx_users_billing_email ON users(billing_email);
```

## Reverse
```sql
DROP INDEX idx_users_billing_email;
ALTER TABLE users DROP COLUMN billing_email;
```

## Data Impact
- 0 rows changed on forward (column nullable)
- Data loss on reverse: yes, if any rows populated after forward deploy
- Mitigation: backup table snapshot before reverse

## Dual-write window
- N/A (additive only)

## Rollback SLO
- 2 min (DDL only, no data reshape)

## Tested on
- staging clone of prod (2.4M rows) on 2026-04-23
- duration: forward 1.8s, reverse 0.9s
```

## Anti-Patterns

- Writing forward migration without reverse at the same commit
- Skipping dual-write for column rename (breaks in-flight app instances)
- Skipping confidence window before drop (no recovery if bug surfaces)
- Batch updates without throttling (lock contention, replication lag)
- Testing only on empty dev DB (missing data-volume issues)
- "We'll just restore from backup if something goes wrong" (RTO mismatch)
- Amending migrations that already ran in prod (state drift)
- Non-deterministic backfill (different run = different data)
- Forgetting to update ORM schema cache after reverse

## Handoffs

- **Schema → Builder**: emits application-side dual-write diff
- **Schema → Tuner**: if backfill is slow, query plan analysis
- **Schema → Beacon**: add alert on discrepancy rate during dual-write
- **Schema → Gear**: update deploy scripts to stage migration before app
- **Schema → Launch**: feeds rollback plan into release `rollback` Recipe
