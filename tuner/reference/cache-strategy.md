# Query Cache Strategy Reference

Purpose: Use this file when the bottleneck is repeat-read latency that no index or rewrite can flatten, and the right answer is a cache layer at the DB or application boundary. Covers Redis/Memcached sizing, PostgreSQL `shared_buffers`, hit-rate targets, TTL design, and invalidation patterns. Optimize for read-heavy, tolerant-of-staleness workloads first; leave real-time reads uncached.

## Scope Boundary

- **Tuner `cache`**: query-result and DB-layer caching — Redis/Memcached in front of SQL, PostgreSQL `shared_buffers` / effective cache size, result-set cache, cache-aside/write-through patterns at the repository layer.
- **Gateway (elsewhere)**: HTTP-response cache, CDN/edge cache, `Cache-Control`/`ETag` design, API-gateway-level caching — owned by Gateway, not Tuner.
- **Schema (elsewhere)**: design-time denormalization, materialized views, computed columns — decided at DDL time, not at query time.
- **Forge (elsewhere)**: throwaway cache mocks in prototypes. Real TTL/invalidation design is Tuner's.

If the cache sits between HTTP client and API → Gateway. If the cache sits between repository and SQL → `cache`. If the "cache" is physical storage (MV, denormalized column) → Schema.

## Decision Matrix

| Read pattern | Volatility | Recommended cache | TTL |
|--------------|-----------|-------------------|-----|
| User profile | Low (minutes) | Redis cache-aside | 1h |
| Product catalog | Medium | Redis cache-aside | 10min |
| Session / auth token | Low | Redis (write-through) | session lifetime |
| Feature flags | Low | In-process LRU + Redis | 30s in-proc, 5min Redis |
| Search results (popular queries) | High | Redis, keyed by normalized query | 60s |
| Search results (tail queries) | High | No cache — cache hit rate too low |  — |
| Analytics aggregates | Low | Materialized view (Schema owns) | refresh schedule |
| Real-time inventory / pricing | High | No cache, or ≤5s TTL with stampede guard | ≤5s |

Rule of thumb: cache when read:write ratio ≥ 10:1 and staleness tolerance ≥ TTL. Below that, invalidation cost exceeds the win.

## Hit-Rate Targets

| Layer | Target hit rate | Meaning below target |
|-------|-----------------|----------------------|
| PostgreSQL `shared_buffers` | ≥ 99% on OLTP | Undersized buffer pool or working set exceeds RAM |
| Application Redis cache | ≥ 80% on hot paths | Keys churn too fast, TTL too short, or cardinality too high |
| CDN/edge (Gateway owns) | ≥ 90% on static | See Gateway reference, not this one |

Measure `shared_buffers` hit rate:

```sql
SELECT sum(heap_blks_hit) * 100.0 / nullif(sum(heap_blks_hit + heap_blks_read), 0) AS hit_pct
FROM pg_statio_user_tables;
```

Size `shared_buffers` at 25% of RAM as the baseline; raise toward 40% only if the working set is demonstrably larger and the OS page cache is not doing the work.

## Cache-Aside vs Write-Through

| Pattern | Read path | Write path | Use when |
|---------|-----------|-----------|----------|
| Cache-aside (lazy) | App → cache miss → DB → populate cache | App → DB, invalidate key | Default for most workloads; tolerates cache outage |
| Write-through | App → cache → DB (cache always authoritative on write) | App → cache + DB together | Session stores, counters, write-heavy hot keys |
| Write-behind (write-back) | App → cache, async flush to DB | Background worker flushes | Avoid unless durability loss is acceptable |
| Read-through | App → cache, cache loads from DB on miss | App → DB, cache refresh | When cache library owns the DB client |

Cache-aside template (pseudo-code):

```ts
async function getUser(id: string): Promise<User> {
  const key = `user:${id}`;
  const hit = await redis.get(key);
  if (hit) return JSON.parse(hit);
  const row = await db.query('SELECT ... FROM users WHERE id = $1', [id]);
  await redis.set(key, JSON.stringify(row), 'EX', 3600); // 1h TTL
  return row;
}

async function updateUser(id: string, patch: Partial<User>): Promise<void> {
  await db.query('UPDATE users SET ... WHERE id = $1', [id, ...]);
  await redis.del(`user:${id}`); // invalidate, do not refresh here
}
```

## Invalidation Patterns

Cache correctness is an invalidation problem, not a storage problem.

| Pattern | When correct | Risk |
|---------|-------------|------|
| TTL-only | Staleness tolerance ≥ TTL | Inconsistent window equal to TTL |
| Delete-on-write | Single-writer per key | Race: reader repopulates stale value after delete |
| Set-on-write | Value is cheap to compute at write time | Drift if reads and writes diverge in logic |
| Versioned keys (`user:v2:{id}`) | Schema or serialization change | Old keys linger until TTL |
| Tag-based invalidation | Groups of keys change together (e.g., product list) | Needs Redis tagging support or secondary index |

Stampede guard for hot keys (TTL expiry on popular item causes thundering herd):

```ts
// Probabilistic early expiration
function shouldRecompute(ttlRemaining: number, beta = 1.0): boolean {
  const delta = computeCostSeconds; // estimate of DB fetch cost
  return Math.random() < Math.exp(-beta * ttlRemaining / delta);
}
```

Or use a per-key mutex / `SET NX EX` lock so only one caller repopulates.

## Anti-Patterns

- Caching authoritative state without invalidation — e.g., user balance in Redis with no write-through → drift produces money bugs.
- Using TTL as a correctness boundary for user-visible data — "eventually consistent" is a property you design, not a side effect of forgetting to invalidate.
- Caching at multiple layers with different TTLs and no coordination — in-process + Redis + CDN all cache the same object with staggered expiries, making the stale window unpredictable.
- Caching tail queries (long-tail search) — near-zero hit rate, memory wasted, eviction pressure on hot keys.
- Caching large result sets (multi-MB JSON) in Redis — serialization cost exceeds query cost; prefer paginated keys or a materialized view.
- Setting identical TTL on all keys and letting them expire simultaneously — synchronized expiry causes cache stampede on hot paths.
- Using `KEYS *` or `SCAN` on every request for invalidation — O(N) Redis traversal blocks the event loop; use tag indices or versioned keys instead.
- Confusing `shared_buffers` sizing with OS page cache — doubling `shared_buffers` above 40% of RAM starves the OS cache and typically reduces total hit rate.

## Handoff / Next Steps

After a `cache` recommendation:

- **To Schema** (via `TUNER_TO_SCHEMA`): if the real fix is a materialized view, denormalized column, or computed column — cache is a read-time workaround, Schema owns design-time denormalization.
- **To Builder** (via `TUNER_TO_BUILDER`): repository-layer cache-aside integration, key-naming convention, invalidation hooks on write paths, stampede-guard wrapper.
- **To Gateway** (outside Tuner): if caching should move up to HTTP/edge layer because the response (not the query) is what repeats — Gateway owns `Cache-Control`, `ETag`, `Vary`, CDN config.
- **To Beacon** (via `TUNER_TO_BEACON`): hit-rate, miss-rate, eviction-rate, p99 of cache-miss path dashboards; alert on hit rate falling below target.

Deliverable artifacts: cache key schema, TTL table per key class, invalidation rules per write path, hit-rate monitoring query, stampede-guard decision for each hot key.
