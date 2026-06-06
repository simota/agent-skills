# Cloud DB Optimization Patterns

Purpose: Use this file when optimizing queries for cloud-managed databases (Aurora, Neon, PlanetScale, Tiger Data) or selecting a cloud DB for a project.

Contents:
- 2026-05 managed-Postgres landscape
- Aurora: QPM, Aurora DSQL, Aurora Limitless
- Neon: cold start, branching, 2026 pricing
- PlanetScale: NVMe Metal performance (MySQL + Postgres)
- Tiger Data (ex-Timescale)
- Cloud DB selection comparison
- Migration considerations

---

## 2026-05 Managed-Postgres Landscape

Headline changes vs the prior baseline:

- **Aurora DSQL is GA since 2025-05-27** — PostgreSQL-compatible serverless distributed SQL with active-active multi-region strong consistency, advertised as ~4× faster reads/writes vs competing distributed SQL (`https://aws.amazon.com/about-aws/whats-new/2025/05/amazon-aurora-dsql-generally-available/`, `https://www.infoq.com/news/2025/06/amazon-aurora-dsql-ga/`). Regions as of 2026-05: us-east-1/2, us-west-2, ap-northeast-1/3, eu-west-1/2/3.
- **Aurora PostgreSQL Limitless Database is GA** — built-in sharding for write throughput beyond a single writer; can handle millions of TPS and petabyte data, each shard ≤ 128 TiB, reference tables ≤ 32 TiB (`https://aws.amazon.com/blogs/aws/amazon-aurora-postgresql-limitless-database-is-now-generally-available/`).
- **Neon was acquired by Databricks in May 2025**; 2025 pricing reshuffle dropped storage from $1.75/GB-mo to $0.35/GB-mo and bumped Free tier compute from 50 to 100 CU-hours/month (`https://vela.simplyblock.io/articles/neon-serverless-postgres-pricing-2026/`).
- **Timescale rebranded to Tiger Data in June 2025** (`https://www.tigerdata.com/blog/timescale-becomes-tigerdata`); product surface: Hypercore (hybrid row/columnar), pgvectorscale (Streaming DiskANN), Continuous Aggregates. Open-source extension remains `TimescaleDB`.
- **PlanetScale Postgres on Metal launched 2025-10** — locally-attached NVMe SSD with unlimited IOPS; benchmark instance i8g M-320 (4 vCPU, 32 GB RAM, 937 GB NVMe) tops out around 40k IOPS with the lowest p99 latency in PlanetScale's public benchmarks (`https://www.infoq.com/news/2025/10/planetscale-metal-postgres/`, `https://planetscale.com/benchmarks/vitess`).

---

---

## Aurora: Query Plan Management (QPM)

Aurora PostgreSQL uses `apg_plan_mgmt` for Query Plan Management, preventing plan regression when the optimizer changes plans.

### Version: apg_plan_mgmt v2.9 (Aurora PostgreSQL 16.x+)

```sql
-- Enable QPM
SET rds.force_admin_logging_level = 'debug5';
LOAD 'apg_plan_mgmt';

-- Capture current plans
SELECT apg_plan_mgmt.capture_plan_baselines('automatic');

-- View managed plans
SELECT * FROM apg_plan_mgmt.dba_plans
ORDER BY plan_created DESC;
```

### aurora_stat_plans

`aurora_stat_plans` extends `pg_stat_statements` with plan-level statistics unique to Aurora.

```sql
-- Plans with highest total cost
SELECT queryid, planid,
       total_time / calls AS avg_ms,
       plan_hash,
       calls
FROM aurora_stat_plans
ORDER BY total_time DESC
LIMIT 20;

-- Detect plan changes for a specific query
SELECT queryid, planid, plan_created, calls
FROM aurora_stat_plans
WHERE queryid = '<target_queryid>'
ORDER BY plan_created DESC;
```

### Reader Instance Optimization

```sql
-- Route read-only queries to Reader endpoint
-- Application connection string pattern:
-- writer: cluster-xxx.cluster-rds.amazonaws.com
-- reader: cluster-xxx.cluster-ro-rds.amazonaws.com

-- Identify read-heavy queries for reader offload
SELECT query, calls, total_time / calls AS avg_ms
FROM pg_stat_statements
WHERE query NOT ILIKE '%insert%'
  AND query NOT ILIKE '%update%'
  AND query NOT ILIKE '%delete%'
ORDER BY calls DESC
LIMIT 20;
```

### Aurora-Specific Settings

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| `apg_plan_mgmt.capture_plan_baselines` | `automatic` | Auto-capture for all queries |
| `apg_plan_mgmt.use_plan_baselines` | `true` | Enforce captured plans |
| `apg_plan_mgmt.plan_retention_period` | `32` days | Adjust based on workload stability |
| `aurora_max_babelfish_tds_connections` | — | Only for Babelfish; irrelevant for standard PG |

---

## Aurora DSQL vs Aurora PostgreSQL Limitless (2026-05)

These are two **different** AWS products that both promise scale-out Postgres compatibility. Pick correctly:

| Aspect | Aurora DSQL | Aurora PostgreSQL Limitless |
|--------|-------------|-----------------------------|
| GA date | 2025-05-27 | 2024-11 (re:Invent), GA on PG 16+ |
| Compatibility | PostgreSQL wire protocol (subset of SQL/features) | Full Aurora PostgreSQL |
| Topology | Multi-region active-active, strong consistency, serverless | Single-region sharded with router/shard nodes |
| Sharding model | Transparent global commit (transparent to app) | Sharded tables + reference tables; **shard key required** on writes |
| Write scale ceiling | Auto-scales (no shard math) | Millions of TPS across shards; 128 TiB / shard, 32 TiB reference table |
| Strong fit | Globally distributed apps, multi-region writes | Single-region apps that outgrew a single Aurora writer |
| Limitations | Extension list narrower than Aurora; PG version may lag stock PG | Cross-shard transactions and queries pay coordinator latency |

Tuner heuristic:
- **One region, single-writer bottleneck** → Aurora Limitless (preserve full PG feature set).
- **Multi-region writes with strong consistency** → Aurora DSQL.
- **Either** → verify the extension list (pgvector, PostGIS, pg_partman) and the PG major version on the target before locking in.

For Aurora DSQL, the operational story removes most pool tuning (no instance class, no `max_connections` ceiling) but adds new constraints: each transaction's latency includes Quorum-based commit, so **chatty per-row transactions degrade quickly** — prefer batched writes and avoid long-running read-after-write loops.

---

## Neon: Cold Start Optimization (2026-05)

Neon uses a serverless architecture with compute auto-suspend. Cold starts occur when a suspended compute resumes. Following the **May 2025 Databricks acquisition**, the pricing model was rebalanced (`https://vela.simplyblock.io/articles/neon-serverless-postgres-pricing-2026/`):

- Storage: **$0.35 / GB-mo** (down from $1.75)
- Free tier: 100 CU-hours / 0.5 GB storage
- Launch: $5/mo minimum, $0.14 / CU-hour, 10 branches included
- Scale: $0.26 / CU-hour, 25 branches included, $1.50 / extra branch-month

### Cold Start Baseline

| Scenario | Typical Latency |
|----------|----------------|
| Compute suspended (auto-suspend) | 300–500ms (p99 ≈ 500ms) |
| Warm compute | < 5ms |
| Connection pool (Pooled mode) | < 100ms via Supavisor-compatible Neon proxy (sub-100ms post-wake) |

### Reducing Cold Start Impact

**1. Disable auto-suspend for latency-sensitive workloads**

```bash
# Neon CLI
neon projects update <project-id> --suspend-timeout 0
# Or set via Neon Console: Project Settings → Compute → Auto-suspend timeout
```

**2. Use Pooled Connection Mode**

```
# Direct connection (cold start possible)
postgresql://user:pass@ep-xxx.neon.tech/dbname

# Pooled connection (Neon proxy manages pool, no cold start for pool)
postgresql://user:pass@ep-xxx-pooler.neon.tech/dbname?pgbouncer=true
```

**3. Keep-alive Pattern (for serverless functions)**

```typescript
// Warm the connection before the critical path
export async function warmDb(sql: NeonQueryFunction) {
  await sql`SELECT 1`;
}

// Call at function init (outside handler)
const warmPromise = warmDb(sql);
export async function handler(event) {
  await warmPromise; // ensures warm connection
  // ... actual query
}
```

### Copy-on-Write (CoW) Branching

Neon's CoW architecture enables instant database branches for development and testing.

```bash
# Create a branch from production snapshot
neon branches create --name preview/feature-xyz --parent main

# Use branch connection string
neon connection-string preview/feature-xyz
```

**Use cases:**
- Preview environments per PR: ~0ms branch creation
- Load testing against production data snapshot
- Schema migration testing before applying to main

---

## PlanetScale: NVMe Metal Performance (MySQL and Postgres, 2026-05)

PlanetScale Metal runs on locally-attached NVMe SSD (not network-attached storage), offering predictable low-latency for high-throughput OLTP. **PlanetScale Postgres on Metal launched 2025-10** (`https://www.infoq.com/news/2025/10/planetscale-metal-postgres/`), bringing the same architecture to PG workloads previously locked to the MySQL/Vitess engine.

### Performance Characteristics

| Metric | Typical Value |
|--------|---------------|
| Query latency (simple SELECT) | 1–3ms |
| Write throughput (single shard) | 10K–50K QPS |
| Connection overhead | Low (Vitess connection pooling; PG path uses standard PG protocol with Metal-local backend) |
| Storage I/O | NVMe, local (not network-attached); benchmark instance i8g M-320 tops out ~40k IOPS |
| Public benchmark instance | i8g M-320: 4 vCPU, 32 GB RAM, 937 GB NVMe (`https://planetscale.com/benchmarks/vitess`) |

PlanetScale also added **vector data type support** alongside the relational MySQL surface, removing the need for a sidecar vector DB for moderate-scale embedding workloads.

### Vitess Query Optimization

PlanetScale uses Vitess under the hood. Key patterns:

```sql
-- Always use shard key in WHERE clause for cross-shard query avoidance
-- Shard key is typically the primary key or a defined vindex

-- Good: hits single shard
SELECT * FROM orders WHERE user_id = 12345 LIMIT 10;

-- Problematic: scatter query (hits all shards)
SELECT COUNT(*) FROM orders WHERE status = 'pending';
```

### Schema Change Safety

```sql
-- PlanetScale uses gh-ost for non-blocking schema changes
-- Deploy requests handle schema migrations — no direct DDL in production
-- Always test schema changes on a branch first
```

---

## Tiger Data (ex-Timescale, 2026-05)

Timescale rebranded to **Tiger Data** in June 2025 (`https://www.tigerdata.com/blog/timescale-becomes-tigerdata`). The product surface for query tuning purposes:

- **Hypercore engine**: hybrid row + columnar storage on top of Hypertables; reads automatically pick row store for hot range/key access, columnar store for analytic scans. Tune by sizing the row-store window (typically days to weeks).
- **Continuous Aggregates**: incrementally-maintained materialised views — the recommended substitute for plain `MATERIALIZED VIEW` on time-series tables.
- **pgvectorscale**: Streaming DiskANN index, separate from upstream pgvector HNSW/IVFFlat. Use when the working set exceeds RAM and recall@k tolerance allows.
- Open-source extension remains `TimescaleDB`; the managed cloud product is **Tiger Cloud** (scales to petabytes per `https://www.tigerdata.com/blog/timescale-becomes-tigerdata`).

Tuner posture: route time-series + vector hybrid workloads to Tiger Cloud only when both axes need optimising; for vector-only workloads on stock PG, stay on pgvector 0.8/0.9.

---

## Cloud DB Selection Comparison

| Criteria | Aurora PostgreSQL (Standard / Limitless) | Aurora DSQL | Neon | PlanetScale Metal | Tiger Cloud |
|----------|------------------------------------------|-------------|------|-------------------|-------------|
| Engine | PostgreSQL-compatible | PG-compatible serverless distributed SQL | PostgreSQL (stock) | MySQL or PostgreSQL on NVMe Metal | PostgreSQL + TimescaleDB + Hypercore |
| Scaling model | Vertical + Read replicas; Limitless = native sharding | Auto, multi-region active-active | Serverless (compute/storage separated) | Vertical on NVMe; Vitess shards on MySQL | Hypertables + read replicas |
| Cold start | None | None | 300–500ms (suspendable) | None | None |
| Cost model | Instance + storage; Limitless prices per shard | Per-request + storage | Compute-seconds + storage ($0.35/GB-mo) | Per-instance | Per-instance + storage |
| Best for | Enterprise OLTP; Limitless when single-writer ceiling is the constraint | Multi-region writes with strong consistency | Serverless, dev/test, scale-to-zero | Latency-sensitive OLTP on NVMe | Time-series + analytics + vector hybrid |
| Branching | Snapshot clone | Not applicable | Instant CoW branch (10–25 included) | Schema branch (deploy requests) | Not branching-oriented |
| Connection pooling | RDS Proxy (PgBouncer-compatible) | Built-in | Neon Proxy (built-in pooler) | Vitess (MySQL) / stock PG (Metal Postgres) | Standard PG pooling |
| Multi-region | Global Database (active-active read; single writer) | Native active-active writes | Read replicas | Not native | Read replicas |
| Vector support | pgvector 0.8+ | Limited (verify extension list) | pgvector 0.8+ | Native vector data type (MySQL) | pgvectorscale (DiskANN) |
| Migration tooling | pg_upgrade, DMS | DMS (target only); cannot pg_upgrade from stock PG | pg_dump, logical replication | Planetscale CLI, deploy requests | pg_dump, logical replication |

---

## Migration Considerations

### Migrating to Aurora PostgreSQL

```bash
# Use AWS DMS for online migration
# Or pg_dump/restore for offline migration

# Key checks pre-migration:
# 1. Aurora-incompatible extensions (check aws.extensions)
# 2. Sequence max values (Aurora uses different sequence backend)
# 3. Partitioning behavior (Aurora adds aurora_partition_advisor)
# 4. Custom pg_hba.conf entries (managed by RDS)
```

### Migrating to Neon

```bash
# pg_dump from source
pg_dump -Fc --no-acl --no-owner \
  -h source-host -U source-user source-db > backup.dump

# Restore to Neon
pg_restore -Fc --no-acl --no-owner \
  -d "postgresql://user:pass@ep-xxx.neon.tech/neondb" backup.dump

# Enable logical replication for live migration (Neon supports it)
# Source: set wal_level = logical, max_replication_slots >= 1
```

### Common Migration Pitfalls

| Issue | Aurora | Neon | PlanetScale |
|-------|--------|------|-------------|
| Extensions not supported | `uuid-ossp` (use `gen_random_uuid()`) | PostGIS (check version) | MySQL-only extensions |
| Connection limits | Higher with RDS Proxy | Use pooled endpoint | Vitess handles |
| Prepared statements | Supported | Supported (use `neon` driver) | Limited in sharded setup |
| `LISTEN/NOTIFY` | Supported | Not supported (serverless) | Not supported (MySQL) |
| Transaction semantics | Standard PostgreSQL | Standard PostgreSQL | MySQL MVCC |
