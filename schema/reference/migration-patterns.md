# Migration Patterns

Purpose: Use this file when planning safe schema changes, rollback, or framework-specific migration commands. Tool baseline: 2026-05.

Contents:
1. Safe change decision tree
2. Expand-contract pattern
3. Zero-downtime index creation
4. Framework commands
5. Pre-migration checklist
6. Zero-downtime DDL toolchain (Atlas / pgroll / Squawk / Strong Migrations / pg-osc / gh-ost)

## Safe Change Decision Tree

```text
Schema change needed
├── Adding new?
│   ├── New table -> CREATE TABLE (safe)
│   ├── New nullable column -> ADD COLUMN (safe)
│   ├── New NOT NULL column -> Expand-contract
│   └── New index -> Online / concurrent creation
├── Modifying existing?
│   ├── Rename column -> Expand-contract
│   ├── Change type -> Verify conversion safety first
│   ├── Add constraint -> Validate existing data first
│   └── Change default -> Usually safe
└── Removing?
    ├── Drop column -> Backup first, then phased removal
    ├── Drop table -> Backup required, irreversible
    ├── Drop index -> Safe, but verify query impact
    └── Drop constraint -> Safe, but verify integrity risk
```

## Expand-Contract Pattern

| Phase | Goal | Required actions |
|------|------|------------------|
| Expand | Introduce the new structure safely | Add new column/table, keep it nullable, dual-write if needed |
| Migrate | Backfill and validate | Batch copy data, validate consistency, add `NOT NULL` only after backfill |
| Contract | Remove the old structure | Switch reads, remove sync path, drop old column only after verification |

## Zero-Downtime Index Creation

```sql
-- PostgreSQL
CREATE INDEX CONCURRENTLY idx_name ON table_name(column_name);

-- MySQL 8.0+
ALTER TABLE t
  ADD INDEX idx_name (col),
  ALGORITHM=INPLACE,
  LOCK=NONE;
```

## Framework Migration Commands

| Framework | Create | Run | Rollback |
|-----------|--------|-----|----------|
| Prisma 7 | `prisma migrate dev --name [name]` | `prisma migrate deploy` | `prisma migrate resolve --rolled-back` |
| TypeORM | `typeorm migration:generate -n [Name]` | `typeorm migration:run` | `typeorm migration:revert` |
| Drizzle | `drizzle-kit generate` | `drizzle-kit migrate` | Manual (write reverse migration) |
| Knex | `knex migrate:make [name]` | `knex migrate:latest` | `knex migrate:rollback` |
| Alembic | `alembic revision --autogenerate -m "name"` | `alembic upgrade head` | `alembic downgrade -1` |
| Liquibase 5 | changeset YAML/SQL | `liquibase update` | `liquibase rollbackCount 1` (AI-generated rollback assistance since 5.0, Sep 2025) |
| Atlas v1 | `atlas migrate diff` | `atlas migrate apply` | `atlas migrate down` (declarative, HCL/SQL/ORM source) |
| pgroll | `pgroll start <migration>` | `pgroll complete` | `pgroll rollback` (zero-downtime, dual-schema views) |

## Pre-Migration Checklist

- Backup is available and verified
- Migration was tested on production-like data
- Rollback path was tested or explicitly marked backup-required
- Lock duration was estimated
- Disk space and index-build impact were checked
- Low-traffic window is selected if blocking work remains
- Post-migration monitoring is prepared

---

## Drizzle ORM Best Practices

```typescript
// drizzle.config.ts — recommended settings
import { defineConfig } from 'drizzle-kit';

export default defineConfig({
  schema: './src/db/schema.ts',
  out: './drizzle',
  dialect: 'postgresql',
  strict: true,     // fail on ambiguous schema changes (column drops, renames)
  verbose: true,    // print SQL statements before execution
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

**Key rules:**
- Always use `strict: true` — prevents silent data-loss migrations.
- Use `verbose: true` in CI to surface generated SQL for review.
- Run `drizzle-kit check` in CI before `drizzle-kit migrate` to detect breaking changes.
- Store generated migration files in version control; never hand-edit them.

---

## Prisma 7 Migration Notes

Prisma 7 replaces the Rust-based query engine with a pure TypeScript implementation.

**Breaking changes from Prisma 6:**
- The `prisma-engines` binary is no longer included; remove it from Dockerfile `COPY` commands.
- `datasource.binaryTargets` is deprecated — remove from `schema.prisma`.
- Cold-start time improves significantly (no native binary load), but first-query memory increases slightly.

**Migration steps:**
```bash
npm install prisma@7 @prisma/client@7
npx prisma generate  # regenerates the TypeScript client
```

**Verify:**
- Remove `binaryTargets = ["native", "linux-musl"]` from `schema.prisma`.
- Remove `prisma-engines` from `.dockerignore` allowlist if present.
- Test connection pooling configuration — `connectionLimit` semantics unchanged.

---

## Shadow Tables Pattern

Shadow tables allow zero-downtime schema changes on high-traffic tables by building the new schema alongside the old one.

**6-step procedure:**

1. **Create** the shadow table with the new schema alongside the original.
   ```sql
   CREATE TABLE orders_v2 (LIKE orders INCLUDING ALL);
   ALTER TABLE orders_v2 ADD COLUMN currency TEXT NOT NULL DEFAULT 'USD';
   ```

2. **Backfill** existing rows from original to shadow in batches.
   ```sql
   INSERT INTO orders_v2
   SELECT *, 'USD' AS currency FROM orders
   WHERE id BETWEEN $batch_start AND $batch_end
   ON CONFLICT (id) DO NOTHING;
   ```

3. **Dual-write** — application writes to both tables simultaneously.

4. **Verify** row counts and checksums between tables.

5. **Cut over** — rename tables atomically.
   ```sql
   BEGIN;
   ALTER TABLE orders RENAME TO orders_old;
   ALTER TABLE orders_v2 RENAME TO orders;
   COMMIT;
   ```

6. **Drop** the old table after a monitoring period (typically 1–7 days).
   ```sql
   DROP TABLE orders_old;
   ```

---

## Zero-Downtime DDL Toolchain (2026-05)

The shadow-table / expand-contract dance is mechanical; reach for tools instead of hand-rolling it. Pick by ecosystem and risk profile.

| Tool | Engine | Strategy | When to pick |
|------|--------|----------|-------------|
| **pgroll** (Xata) | Postgres | Dual-schema views; both old and new schema visible during rollout | Postgres app needs JSON-described migrations with explicit `pgroll start` / `pgroll complete` / `pgroll rollback` phases. Underpins Xata's web UI. |
| **Atlas v1.0** (Ariga, Dec 2025 GA) | Postgres / MySQL / Spanner / Snowflake / ClickHouse / etc. | Declarative HCL/SQL/ORM source → diff → migration plan; canary/parallel rollouts; deployment traces | Multi-engine fleets, schema-as-code review workflows, ORM (GORM / Sequelize / Prisma) source-of-truth. |
| **pg-osc** (shayonj) | Postgres | Trigger-based shadow table + audit-table swap | Postgres `ALTER TABLE TYPE` on > 50 GB table where `ALTER TABLE ... ALTER COLUMN ... TYPE` would hold `ACCESS EXCLUSIVE` too long. |
| **gh-ost** (GitHub) | MySQL | Triggerless; tails binlog (requires RBR), builds ghost table, replays binlog onto ghost, atomic swap | MySQL with heavy write load where pt-osc's trigger overhead is unacceptable. Not resumable. |
| **pt-online-schema-change** (Percona) | MySQL / MariaDB | Trigger-based; synchronous writes to ghost during copy | MySQL with `--resume` requirement (gh-ost can't resume); known/predictable trigger load. |
| **Squawk** | Postgres (lint only) | Static analysis of migration SQL: flags `ALTER TABLE ... ADD COLUMN NOT NULL`, `CREATE INDEX` without `CONCURRENTLY`, unsafe type changes, etc. | Pre-commit hook + CI gate for every Postgres migration. Combine with the toolchain above for runtime safety. |
| **Strong Migrations** (Ankane) | Rails / ActiveRecord (Postgres / MySQL / MariaDB) | Rails-aware static lint; educates with safer rewrite per detected anti-pattern; long migration `statement_timeout` separate from app | Rails repos — the gem of record; require `safety_assured { ... }` to bypass intentionally. |
| **Bytebase 3.16** (Mar 2026) | Postgres / MySQL / Oracle / Spanner / SQL Server / etc. | Web UI + GitOps approval; DBA review queue; environment-staged rollout | Org-wide change-management with role-based approval (DBA gate before prod). |
| **Liquibase 5.0** (Sep 2025) | Multi-engine | YAML/XML/SQL changesets; AI-generated rollback assistance | Java-heavy stacks and orgs already invested in Liquibase changelog format. |

**Decision rules:**
- Default to the framework migration tool (Alembic / TypeORM / Knex / ActiveRecord). Add Squawk in CI for Postgres or Strong Migrations for Rails — both are nearly free.
- Add pgroll or Atlas when you need true dual-schema coexistence (different application versions reading/writing different shapes simultaneously).
- pg-osc / gh-ost / pt-osc are for the single-table type-change problem, not whole-schema migrations.
- Bytebase or Liquibase is the right answer only when org-wide approval workflow trumps tool-of-the-ecosystem.
