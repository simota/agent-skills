# Database Migration Reference

## Tooling Snapshot (2026-05)

| Tool | What it owns | When to reach for it |
|------|----------------|-----------------------|
| Flyway / Alembic / Liquibase / Knex / Prisma Migrate | versioned forward-only / up-down migration files | the steady-state migration framework — keep it as the single source of history |
| **pgroll** (Xata) | runs PostgreSQL schema migrations as Expand/Contract automatically (creates virtual schemas, dual-writes via triggers, then contracts) | new project, or any PG project where Expand/Contract has been informal — pgroll formalises it |
| pg_osc / pg_repack | one-off large-table changes (column type, table rewrite) | when an Expand/Contract is impractical for a single table because of size |
| GitHub Schemio / sqlfluff / Atlas | drift detection + lint over migrations as code | CI gate; pair with the framework above, do not replace it |

Pick *one* framework as the source of truth; layer pgroll / pg_osc / Atlas on top as needed. Mixing two frameworks in the same repo is a near-guaranteed history-conflict source.

## Zero-Downtime Schema Migration: Expand-Contract Pattern

Every schema change follows three stages — never alter/drop in a single migration. As of `PostgreSQL 11+`, adding a column **with a default** is instant (the default is stored in the system catalog and applied on read with no table rewrite or long lock) — earlier guidance against "add column with default" no longer applies.

### Stage 1: Expand (additive only)
- Add new columns (nullable, or with a default on PG `11+`)
- Add new tables
- Add new indexes with `CREATE INDEX CONCURRENTLY` (and never inside an explicit transaction)
- **Never:** rename, drop, or change types in this stage

### Stage 2: Migrate (dual-write + backfill)
- Application writes to both old and new columns
- Backfill old data into new columns
- Verify data consistency

### Stage 3: Contract (remove old)
- Stop writing to old columns
- Drop old columns, indexes, constraints
- **Only after** verifying no code references old schema

### Example: Rename column
```sql
-- Stage 1: Expand
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);

-- Stage 2: Migrate (application code)
-- Write to both: UPDATE users SET name = $1, display_name = $1 WHERE id = $2
-- Backfill:
UPDATE users SET display_name = name WHERE display_name IS NULL;

-- Verify:
SELECT COUNT(*) FROM users WHERE display_name IS NULL AND name IS NOT NULL;
-- Must be 0

-- Stage 3: Contract (after deploy + verification)
ALTER TABLE users DROP COLUMN name;
```

## Dual-Write Pattern

For migrating data between storage systems (old DB → new DB, or old table → new table).

```typescript
class DualWriteUserRepository implements UserRepository {
  constructor(
    private oldRepo: OldUserRepository,
    private newRepo: NewUserRepository,
    private phase: 'dual-write' | 'read-new' | 'new-only'
  ) {}

  async save(user: User): Promise<void> {
    switch (this.phase) {
      case 'dual-write':
        // Write to both, read from old
        await Promise.all([
          this.oldRepo.save(user),
          this.newRepo.save(user),
        ]);
        break;
      case 'read-new':
        // Write to both, read from new
        await Promise.all([
          this.oldRepo.save(user),
          this.newRepo.save(user),
        ]);
        break;
      case 'new-only':
        // Write only to new
        await this.newRepo.save(user);
        break;
    }
  }

  async findById(id: string): Promise<User | null> {
    switch (this.phase) {
      case 'dual-write':
        return this.oldRepo.findById(id);
      case 'read-new':
      case 'new-only':
        return this.newRepo.findById(id);
    }
  }
}
```

### Dual-Write Phase Progression
```
Phase 1: dual-write    → Write both, read old    (verify writes match)
Phase 2: read-new      → Write both, read new    (verify reads match)
Phase 3: new-only      → Write new only           (old becomes archive)
Phase 4: cleanup       → Drop old storage
```

## Concurrent Migration Safety: Advisory Locks Are Mandatory

The single most common "silent data corruption" pattern in 2026 deployments: **two CI runners (or two pods) execute the same migration concurrently** because no advisory lock is held. The migration framework's own bookkeeping is consistent, but the underlying schema operations race — partially-applied DDL, duplicated backfill rows, half-built indexes.

Lock acquisition must be the **first line of every migration job**, not a wrapper around the dangerous DDL.

```sql
-- PostgreSQL: take a session-scoped advisory lock keyed on the migration version.
-- xx_unique_key is the same integer for every runner; only one will get the lock.
SELECT pg_advisory_lock(948751302);   -- or a hash of the migration name
-- ... run the migration ...
SELECT pg_advisory_unlock(948751302);
```

Most modern frameworks (Flyway, Liquibase, Knex, Prisma Migrate, Alembic with `op.execute("SELECT pg_advisory_lock(...)")`) ship advisory-lock hooks — turn them on. pgroll wraps this for you.

## PostgreSQL Major Version Upgrade

### Pre-upgrade checklist
- [ ] Check extension compatibility: `SELECT * FROM pg_available_extensions;`
- [ ] Check deprecated features: review release notes for breaking changes
- [ ] Backup: `pg_dump` or filesystem backup
- [ ] Test on staging with production data snapshot
- [ ] Check replication slot compatibility (logical replication)
- [ ] Estimate downtime (pg_upgrade --link is faster)

### pg_upgrade procedure
```bash
# 1. Stop old cluster
pg_ctl -D /var/lib/postgresql/15/main stop

# 2. Run upgrade check
pg_upgrade \
  --old-datadir=/var/lib/postgresql/15/main \
  --new-datadir=/var/lib/postgresql/16/main \
  --old-bindir=/usr/lib/postgresql/15/bin \
  --new-bindir=/usr/lib/postgresql/16/bin \
  --check

# 3. Execute upgrade (--link for speed, uses hard links)
pg_upgrade \
  --old-datadir=/var/lib/postgresql/15/main \
  --new-datadir=/var/lib/postgresql/16/main \
  --old-bindir=/usr/lib/postgresql/15/bin \
  --new-bindir=/usr/lib/postgresql/16/bin \
  --link

# 4. Start new cluster
pg_ctl -D /var/lib/postgresql/16/main start

# 5. Update statistics
/usr/lib/postgresql/16/bin/vacuumdb --all --analyze-in-stages

# 6. Delete old cluster (after verification)
./delete_old_cluster.sh
```

### Logical replication migration (zero-downtime)
For when downtime is unacceptable:
1. Set up logical replication from old to new cluster
2. Verify replication lag < threshold
3. Switch application connections to new cluster
4. Verify application works
5. Drop replication, decommission old cluster

## Data Backfill Patterns

### Batch backfill with progress tracking
```typescript
async function backfillInBatches(options: {
  tableName: string;
  batchSize: number;
  transform: (row: Record<string, unknown>) => Record<string, unknown>;
  where?: string;
}): Promise<BackfillResult> {
  const { tableName, batchSize, transform, where } = options;
  let processed = 0;
  let lastId = 0;

  while (true) {
    const rows = await db.query(
      `SELECT * FROM ${tableName}
       WHERE id > $1 ${where ? `AND ${where}` : ''}
       ORDER BY id LIMIT $2`,
      [lastId, batchSize]
    );

    if (rows.length === 0) break;

    const updates = rows.map(row => {
      const transformed = transform(row);
      return db.query(
        `UPDATE ${tableName} SET ${
          Object.keys(transformed).map((k, i) => `${k} = $${i + 2}`).join(', ')
        } WHERE id = $1`,
        [row.id, ...Object.values(transformed)]
      );
    });

    await Promise.all(updates);
    processed += rows.length;
    lastId = rows[rows.length - 1].id;

    // Log progress
    console.log(`Backfill ${tableName}: ${processed} rows processed, last_id=${lastId}`);

    // Yield to avoid locking
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  return { tableName, processed };
}
```

## Migration Rollback Procedures

### Schema rollback checklist
1. **Before migration:** snapshot current schema (`pg_dump --schema-only`)
2. **Create reverse migration** alongside forward migration
3. **Test rollback** on staging before production
4. **Monitor after deploy** — set rollback window (e.g., 24 hours)
5. **After rollback window:** remove old schema artifacts

### Data rollback strategies

| Scenario | Strategy | Complexity |
|----------|----------|-----------|
| Added column with default | Drop column | Low |
| Renamed column (Expand-Contract) | Revert application to read old column | Low |
| Data transformation (backfill) | Restore from backup or reverse transform | Medium |
| Table split/merge | Dual-write makes rollback trivial | Low |
| Cross-service data migration | Keep old service running in shadow mode | Medium |
| Schema type change | Use Expand-Contract, old column still exists | Low |

## Migration Verification Queries

```sql
-- Verify row counts match after migration
SELECT
  (SELECT COUNT(*) FROM old_table) AS old_count,
  (SELECT COUNT(*) FROM new_table) AS new_count,
  (SELECT COUNT(*) FROM old_table) - (SELECT COUNT(*) FROM new_table) AS diff;

-- Verify no NULL values in migrated column
SELECT COUNT(*) AS null_count
FROM users
WHERE new_column IS NULL AND old_column IS NOT NULL;

-- Verify data integrity after transform
SELECT o.id, o.old_value, n.new_value
FROM old_table o
JOIN new_table n ON o.id = n.id
WHERE n.new_value != expected_transform(o.old_value)
LIMIT 100;

-- Check for orphaned records
SELECT COUNT(*) FROM child_table c
LEFT JOIN parent_table p ON c.parent_id = p.id
WHERE p.id IS NULL;
```
