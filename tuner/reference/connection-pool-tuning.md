# Connection Pool Tuning Reference

Purpose: Use this file when the bottleneck is connection acquisition, pool exhaustion, or long-lived idle connections — not query plan, not index. Covers pooler selection (PgBouncer / Supavisor / PgCat), pool sizing, prepared-statement cache interactions, idle / max-lifetime tuning, and connection leak detection.

Read in two layers:
- **Quick-Start** — first-pass diagnosis: which pooler, what size, what to monitor.
- **Deep Dive** — lifecycle coordination, leak detection, HikariCP/PgBouncer knobs, anti-patterns.

## Scope Boundary

- **Tuner `connection`**: pool sizing, lifetime tuning, prepared-statement cache behavior, leak detection, wait-event diagnosis at the DB boundary.
- **Schema (elsewhere)**: `max_connections` is a server-side capacity decision that touches schema/workload at DDL time; Schema owns the ceiling, Tuner sizes the pool under that ceiling.
- **Gateway (elsewhere)**: HTTP-layer connection keep-alive, upstream connection pools to API backends — Gateway owns HTTP pool, Tuner owns DB pool.
- **Bolt (elsewhere)**: application-side thread-pool and async runtime sizing that feeds the DB pool — Bolt tunes the producer, Tuner tunes the pool.
- **Forge (elsewhere)**: prototyping connection setup is a throwaway concern; real pool tuning is Tuner's.

If the contention is `acquire_connection` wait → `connection`. If it's `max_connections` rejection at the server → coordinate with Schema. If it's HTTP keep-alive thrash → Gateway.

---

# § Quick-Start

Use this section when the symptom is "connection pressure" or "which pooler should I run" and you need a defensible first answer in minutes.

## Pool Size Formula

```text
pool_size = (core_count * 2) + effective_spindle_count
```

Typical range: `10-20` connections for many applications. For modern SSD/cloud DB: `effective_spindle_count ≈ 1`, so start at `2 × cores + 1` per app instance. The formula is a **ceiling, not a target** — validate against workload and `max_connections` headroom.

## Key PostgreSQL Settings

- `max_connections` — server-side ceiling (Schema-owned)
- `work_mem`
- `shared_buffers`
- `effective_cache_size`

## Monitoring Queries

```sql
-- live state breakdown
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
SELECT count(*) FROM pg_stat_activity WHERE state = 'idle';
SELECT wait_event_type, count(*) FROM pg_stat_activity GROUP BY 1;
```

## Pool Sizing Signals

| Signal | Pool too small | Pool too big |
|--------|---------------|--------------|
| `acquire` wait p99 | > 50ms | ~0ms |
| DB CPU | Low, app waiting | Saturated (context switch storm) |
| `active` / `pool_size` | consistently ≈ 1.0 | consistently < 0.3 |
| Lock contention | Low | High (too many concurrent writers) |
| `max_connections` headroom | Fine | Exhausted — rejected connections |

Total concurrent connections across all app instances × pool_size must stay below `(max_connections − reserved_superuser_connections − replication_slots)`. Aim for ≤ 80% utilization sustained.

## Connection Pooler Comparison (2026-05)

### PgBouncer vs Supavisor vs PgCat

| Feature | PgBouncer | Supavisor | PgCat |
|---------|-----------|-----------|-------|
| Language | C | Elixir (OTP) | Rust |
| Architecture | Single-process | Distributed (OTP) | Multi-process |
| Modes | Session / Transaction / Statement | Session (port 5432) / Transaction (port 6543) | Session / Transaction |
| Prepared statements in transaction mode | **Enabled by default since 1.24.0 (2025-01)** with `max_prepared_statements = 200` (`https://www.crunchydata.com/blog/prepared-statements-in-transaction-mode-for-pgbouncer`); originally added in 1.21 (`https://pganalyze.com/blog/5mins-postgres-pgbouncer-prepared-statements-transaction-mode`) | Named prepared statement support since Supavisor 1.0 | Supported |
| Multi-tenant | Manual (per-database config) | Native (tenant isolation) | Native (sharding) |
| Serverless support | Limited | Excellent (HTTP/WebSocket) | Limited |
| HTTP connections | No | Yes | No |
| WebSocket connections | No | Yes | No |
| Sharding | No | No | Yes (built-in) |
| Performance (50+ connections) | Good | Good (proxies millions of client conns into a stateful native PG pool) | Best |
| Observability | Basic metrics | Prometheus native | Prometheus native |
| Cloud integration | Self-hosted | Supabase native, integrates with Prisma/Drizzle/Psycopg | Self-hosted |

**2026-05 update**: `max_prepared_statements > 0` is now the **PgBouncer 1.24+ default**, which removes the historical silent re-parse penalty for JDBC/asyncpg/pg-protocol-binary clients in transaction mode. Audit any PgBouncer install on `<1.24` and either upgrade or explicitly set `max_prepared_statements = 200`.

**Supavisor port convention** (Supabase, in effect since 2025-02-28): port `5432` is session mode and port `6543` is transaction mode. The legacy session-mode-on-6543 layout was deprecated. Update connection strings before assuming the historical mapping.

### When to Use Each

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Serverless / edge functions | Supavisor | HTTP/WebSocket, no persistent TCP required |
| Multi-tenant SaaS | Supavisor | Tenant isolation, per-tenant pool |
| High connection count (50+) | PgCat | Lower latency per connection at scale |
| Sharded PostgreSQL | PgCat | Built-in shard routing |
| Traditional server deployment | PgBouncer | Battle-tested, simple configuration |
| Supabase hosted | Supavisor | Already integrated in Supabase platform |

### Supavisor Configuration Patterns

```toml
# supavisor.toml — multi-tenant example
[global]
proxy_port = 5432

[[tenants]]
id = "tenant_123"
db_host = "db.tenant-123.example.com"
db_port = 5432
db_name = "postgres"
pool_size = 10
mode = "transaction"
```

### PgCat Configuration Patterns

```toml
# pgcat.toml — sharding example
[general]
host = "0.0.0.0"
port = 5432
pool_size = 20

[pools.mydb]
mode = "transaction"
default_role = "any"

[pools.mydb.shards.0]
database = "shard0"
servers = [["shard0-db.internal", 5432, "primary"]]

[pools.mydb.shards.1]
database = "shard1"
servers = [["shard1-db.internal", 5432, "primary"]]
```

## PostgREST Pool Size Rule

When using PostgREST alongside a connection pooler:

```text
PostgREST pool size ≤ (pooler max_connections) / (number of PostgREST instances)
```

- PostgREST opens one connection per pool slot at startup
- Exceeding pooler limits causes connection exhaustion
- Recommended: set `db-pool` in PostgREST config to `(max_connections * 0.8) / instances`

```ini
# postgrest.conf
db-pool = 10                          # per instance
db-pool-acquisition-timeout = 10      # seconds to wait for a pool slot
db-pool-max-lifetime = 1800           # recycle connections every 30 min
```

---

# § Deep Dive

Use this section once a pooler is chosen and the question is "how do I tune the pool I have" — lifetime coordination, prepared-statement cache, leak detection, HikariCP/PgBouncer knobs.

## Pooler Mode Implications

| Mode | Holds connection for | Prepared statements | Notes |
|------|----------------------|---------------------|-------|
| Session | Entire client session | Preserved across queries | Default; highest compatibility |
| Transaction | One transaction | Lost between txns — app cache invalidated | PgBouncer default; incompatible with server-side prepared statements unless `prepared_statements = true` (PgBouncer 1.21+) |
| Statement | One statement | Always lost | Rarely worth the fragility |

PgBouncer 1.21+ supports server-side prepared statements in transaction mode via `max_prepared_statements`. **PgBouncer 1.24.0 (2025-01) made this the default** with `max_prepared_statements = 200` (`https://www.crunchydata.com/blog/prepared-statements-in-transaction-mode-for-pgbouncer`). On PgBouncer `<1.24`, frameworks relying on prepared statements (JDBC, asyncpg, pg-protocol binary) silently degrade to re-parse on every query — verify the installed version before assuming compatibility.

## HikariCP Tuning (JVM)

```properties
# HikariCP: defaults that matter
maximumPoolSize      = 20                # 2×cores + 1, per app instance
minimumIdle          = maximumPoolSize   # keep pool full for latency-sensitive apps
connectionTimeout    = 3000              # ms; fail fast, do not queue indefinitely
idleTimeout          = 600000            # 10min; <= maxLifetime
maxLifetime          = 1800000           # 30min; must be < DB's idle_in_transaction_session_timeout and pooler server_lifetime
keepaliveTime        = 60000             # 1min; catches NAT timeouts before query
leakDetectionThreshold = 60000           # 60s; logs suspected leak sites
```

Key rules:
- `maxLifetime` must be strictly less than any TCP idle timeout between app and DB (NAT, firewall, pooler `server_idle_timeout`) — otherwise HikariCP hands out a connection the kernel already tore down.
- Setting `minimumIdle = maximumPoolSize` trades startup cost for predictable latency; set lower only if pool creation is cheap and traffic is bursty.

## PgBouncer Tuning

```ini
# pgbouncer.ini — transaction-mode baseline
pool_mode = transaction
default_pool_size = 20            # per user+db pair
min_pool_size = 5
reserve_pool_size = 5             # emergency slots above default_pool_size
reserve_pool_timeout = 3          # seconds to wait before using reserve
server_lifetime = 1800            # recycle server conn every 30min
server_idle_timeout = 600         # close idle server conn after 10min
max_client_conn = 1000            # client-side ceiling
max_prepared_statements = 200     # default in 1.24+; required to set explicitly on 1.21-1.23 for prepared stmt in txn mode
query_wait_timeout = 120          # client waits at most 2min for a server slot
```

## Prepared Statement Cache

- JDBC `prepareThreshold` (default 5) means the driver switches to a server-side prepared statement after the 5th execution. Server-side prepared statements are per-physical-connection; if the pool rotates connections faster than the cache warms up, you pay the parse cost forever.
- On PgBouncer in transaction mode without `max_prepared_statements`, each query re-parses → CPU burn on the DB. Measure with `pg_stat_statements.plans`.
- Node.js `pg` / `asyncpg` / `SQLAlchemy` typically disable prepared statements automatically when they detect PgBouncer — verify, don't assume.

## Connection Leak Detection

Symptoms:
- Pool utilization trends upward over hours with no traffic increase.
- `pg_stat_activity.state = 'idle in transaction'` count grows.
- App recovers after restart.

Detection:

```sql
-- idle in transaction > 5min
SELECT pid, usename, application_name, state, state_change, query
FROM pg_stat_activity
WHERE state = 'idle in transaction'
  AND state_change < now() - interval '5 minutes';
```

Server-side guardrails:

```sql
-- postgresql.conf
idle_in_transaction_session_timeout = '5min'
statement_timeout = '30s'          -- per-role override for long jobs
```

App-side: enable `leakDetectionThreshold` (HikariCP), `pool.options.connectionTimeoutMillis` + `idleTimeoutMillis` (node-postgres), or explicit `async with` context managers (asyncpg, psycopg3) — the leak is almost always a missing `close()` on an error path, not the pool.

## Idle / Max-Lifetime Coordination

All three layers must agree on a lifetime ordering:

```
app maxLifetime  <  pooler server_lifetime  <  DB idle_in_transaction_session_timeout  <  network idle timeout (NAT/firewall)
```

If any inner layer outlives its outer layer, the outer layer tears down a connection the inner layer still hands to the app → intermittent "connection already closed" errors under load.

## Anti-Patterns

- Setting `maximumPoolSize` to a large round number (50, 100) because "more is faster" — contention and context switching dominate past `2×cores + few`.
- Running transaction-mode PgBouncer with a framework that uses server-side prepared statements, without enabling `max_prepared_statements` — silent per-query reparse, invisible in app logs.
- Ignoring `idle in transaction` growth because the app "works fine" — the leak surfaces only during a DB failover or restart when recycled connections expose dangling transactions.
- Setting `maxLifetime` ≥ pooler `server_lifetime` — recycling misalignment produces flaky connection errors attributed to "the network."
- Sizing every app instance's pool independently without summing against `max_connections` — a 10-instance deploy with `pool_size = 20` demands 200 backend slots before any reserved or superuser connections.
- Using a pool at all for serverless/edge (Lambda, Cloudflare Workers) without a stateful pooler in front — each cold start opens a fresh connection, overwhelming `max_connections`; use Supavisor/RDS Proxy/PgBouncer as a front door.
- Treating `connectionTimeout = 30000ms` as a safe default — long timeouts mask a too-small pool by hiding queue depth in tail latency; fail fast at 3-5s and scale the pool if rejection rate climbs.

## Handoff / Next Steps

After a `connection` recommendation:

- **To Schema** (via `TUNER_TO_SCHEMA`): when `max_connections` itself must rise — that's a server capacity change, not just a pool resize.
- **To Builder** (via `TUNER_TO_BUILDER`): close-on-error patterns, transaction scoping fixes, removal of explicit `BEGIN` on read paths that don't need a transaction, async context manager adoption.
- **To Bolt** (via `TUNER_TO_BOLT`): application thread-pool or async-runtime sizing — if app concurrency × pool_size per instance mismatches DB capacity, the ceiling is in the app.
- **To Beacon** (via `TUNER_TO_BEACON`): dashboards for `active` / `idle` / `idle in transaction` counts, `acquire` wait p99, rejected connection rate; alert on pool utilization > 80% sustained 5min.

Deliverable artifacts: per-instance pool config, lifetime-ordering check, prepared-statement compatibility note, leak-detection query, wait-event baseline.
