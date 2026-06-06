# Partition Strategies Reference

Purpose: Select and design table partitioning for large-scale tables. Covers range, list, hash, and time-based partitioning with pruning behavior, maintenance, and migration from non-partitioned tables.

## Contents

- When to partition
- Strategy selection
- Partition pruning
- Maintenance (auto-create, drop)
- Migration from non-partitioned
- Command recipes
- Anti-patterns

## When to Partition

Consider partitioning when any of:

- Table > 100M rows or > 100 GB
- Sequential scans unavoidable on hot path (no selective index helps)
- Data retention requires bulk-delete (monthly / yearly cleanup)
- Query pattern naturally partitions (per-tenant, per-date, per-region)
- Index bloat / maintenance cost on single large table

**Don't partition** when:

- Table < 10M rows (overhead exceeds benefit)
- Query pattern crosses many partitions (pruning doesn't help)
- Joins across partitions dominate workload
- OLTP workload with high cardinality, low skew

## Strategy Selection

| Strategy | When | Key benefit |
|----------|------|-------------|
| **Range** (time, id) | time-series / append-only, retention policies | easy drop-old-partitions |
| **List** (category, region) | bounded discrete key, per-category ops | direct pruning, parallel maintenance |
| **Hash** | even distribution across N partitions, no natural key | uniform size, parallel scan |
| **Time-based (subset of range)** | logs, events, metrics | rolling window + cold storage tiering |
| **Composite** (hash-of-tenant within range-of-date) | multi-tenant + time | both dimensions prunable |

### Decision Flow

```
Is there a natural time axis?
  ├─ Yes → Range by date (monthly/weekly)
  └─ No
      Is there a bounded categorical key (< 100 values)?
        ├─ Yes → List by category
        └─ No → Hash (8, 16, 32, or 64 partitions)
```

## Partition Pruning

For partitioning to help, queries **must** filter on the partition key.

### Good (prunes):
```sql
SELECT * FROM orders WHERE order_date >= '2026-04-01' AND order_date < '2026-05-01';
-- Planner touches only April partition
```

### Bad (no pruning):
```sql
SELECT * FROM orders WHERE total > 1000;
-- Planner scans ALL partitions
```

### Check pruning

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT ... FROM orders WHERE ...;
-- Look for "Partitions: orders_2026_04" (pruned) vs "Partitions: 24 scanned" (bad)
```

## Time-Based Maintenance

### Auto-create future partitions

```sql
-- pg_partman 5.x (recommended for Postgres 14+)
-- 5.0+ supports only declarative partitioning; trigger-based partitioning is removed.
SELECT partman.create_parent(
  p_parent_table => 'public.events',
  p_control => 'created_at',
  p_type => 'range',
  p_interval => '1 month',
  p_premake => 3   -- 3 months ahead
);

-- pg_partman 5.2.4+ supports UUIDv7 as partition key (and any text column
-- decodable to a time value); pair with PostgreSQL 18 uuidv7() to combine
-- the K-sortable PK and the partition key.
```

Pattern without pg_partman: cron job runs daily to create next partition.

**PostgreSQL 18 note:** pg_partman manages `UNLOGGED` via its template table because PG 18 removed the ability to set the `UNLOGGED` flag on a partition-set parent.

### Auto-drop old partitions

```sql
-- Retention = 12 months
SELECT partman.run_maintenance();
-- Drops partitions older than configured retention

-- Or manually:
ALTER TABLE events DETACH PARTITION events_2025_04;
DROP TABLE events_2025_04;  -- or archive to cold storage first
```

### Cold-storage tiering

```sql
-- Detach warm, export, attach foreign table for queries if needed
ALTER TABLE events DETACH PARTITION events_2024_01;
\copy events_2024_01 TO 's3://.../events_2024_01.parquet'
DROP TABLE events_2024_01;
-- Optional: CREATE FOREIGN TABLE over parquet in S3 for cold queries
```

## Migration from Non-Partitioned

**Zero-downtime migration** (preferred for large tables):

```
Phase 1: Create partitioned sibling
  CREATE TABLE orders_new (LIKE orders INCLUDING ALL)
    PARTITION BY RANGE (order_date);
  CREATE TABLE orders_new_2026_01 PARTITION OF orders_new
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
  -- ... create all partitions ...

Phase 2: Dual-write
  App writes to both orders and orders_new

Phase 3: Backfill
  INSERT INTO orders_new SELECT * FROM orders;

Phase 4: Swap
  BEGIN;
    ALTER TABLE orders RENAME TO orders_old;
    ALTER TABLE orders_new RENAME TO orders;
  COMMIT;

Phase 5: Cleanup (after confidence window)
  DROP TABLE orders_old;
```

For smaller tables, Postgres 12+ `ATTACH PARTITION` can convert in place but requires exclusive lock.

## Command Recipes

### Postgres Range Partitioning

```sql
CREATE TABLE events (
  id BIGSERIAL,
  tenant_id BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL,
  payload JSONB
) PARTITION BY RANGE (created_at);

-- Monthly partitions
CREATE TABLE events_2026_04 PARTITION OF events
  FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE events_2026_05 PARTITION OF events
  FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');

-- Default (catch-all, avoid in prod — create partitions proactively)
CREATE TABLE events_default PARTITION OF events DEFAULT;
```

### List Partitioning

```sql
CREATE TABLE users (
  id BIGSERIAL,
  region TEXT NOT NULL,
  email TEXT
) PARTITION BY LIST (region);

CREATE TABLE users_na PARTITION OF users FOR VALUES IN ('us', 'ca', 'mx');
CREATE TABLE users_eu PARTITION OF users FOR VALUES IN ('de', 'fr', 'uk');
CREATE TABLE users_apac PARTITION OF users FOR VALUES IN ('jp', 'sg', 'au');
```

### Hash Partitioning

```sql
CREATE TABLE activity (
  user_id BIGINT NOT NULL,
  occurred_at TIMESTAMPTZ,
  action TEXT
) PARTITION BY HASH (user_id);

CREATE TABLE activity_p0 PARTITION OF activity FOR VALUES WITH (MODULUS 8, REMAINDER 0);
CREATE TABLE activity_p1 PARTITION OF activity FOR VALUES WITH (MODULUS 8, REMAINDER 1);
-- ... up to MODULUS 8, REMAINDER 7
```

### Composite (hash within range)

```sql
CREATE TABLE events (
  id BIGSERIAL,
  tenant_id BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_04 PARTITION OF events
  FOR VALUES FROM ('2026-04-01') TO ('2026-05-01')
  PARTITION BY HASH (tenant_id);

CREATE TABLE events_2026_04_p0 PARTITION OF events_2026_04
  FOR VALUES WITH (MODULUS 4, REMAINDER 0);
-- ... MODULUS 4, REMAINDER 1..3
```

## Partition Size Guidelines

| Partitions per parent | Concern |
|----------------------|---------|
| < 10 | probably doesn't need partitioning |
| 10–1000 | healthy range |
| 1000–10,000 | check planner overhead (`pg_stat_plans`) |
| > 10,000 | planning cost noticeable; consider sub-partitioning or archiving |

Per-partition target size: 10 GB – 100 GB for OLAP, 1 GB – 10 GB for OLTP.

## Anti-Patterns

- Partitioning tiny tables (< 10M rows) "just in case"
- Default partition as dumping ground (becomes giant)
- Partition key not in query predicate (no pruning)
- No auto-create cron → inserts fail when new month arrives
- Dropping partitions without archiving (irrecoverable data loss)
- Too many partitions (> 10K without sub-partitioning) → planner slowdown
- Hash partitioning on low-cardinality key (uneven distribution)
- Cross-partition unique constraints (can't be enforced natively)
- Assuming global indexes — each partition has its own index, maintenance cost is per-partition
- Forgetting VACUUM/ANALYZE on new partitions

## Partitioning vs Time-Series Engines (2026-05)

When the partition key is time and the workload is read-heavy analytics on append-only data, a dedicated time-series engine may outperform plain Postgres partitioning.

| Option | When to choose | Schema implications |
|--------|----------------|---------------------|
| Native Postgres 18 partitioning + pg_partman 5.2.x | OLTP with retention; modest analytic load; want vanilla Postgres | Range by time; hash-by-tenant nested if multi-tenant |
| Tiger Data (TimescaleDB rebrand, 2025-06-17) **Hypercore** | Time-series analytics — hybrid row/columnar storage with `add_columnstore_policy` automating row→column conversion on aged chunks | Hypertables auto-partition on first timestamp column; v2.23+ supports partitioning on UUIDv7 columns directly |
| Citus 13 (Feb 2025, PG 17.2 base) distributed tables | Need horizontal scale beyond a single Postgres node | `create_distributed_table` with shard key = `tenant_id`; reference tables for shared dimensions; `MERGE` distributed-execution supported in 13 |

## Handoffs

- **Schema → Tuner**: verify pruning via EXPLAIN after partitioning
- **Schema → Gear**: add pg_partman cron or maintenance script
- **Schema → Shard**: composite (hash-in-range) migrates naturally to sharded cluster (Citus 13 distributed tables, Aurora DSQL, Spanner)
- **Schema → Beacon**: alert on partition creation failure, disk growth per-partition
- **Schema → Stream**: time-based partitions align with ETL date-keyed pipelines
