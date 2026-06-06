# Caching Strategy

Purpose: Use this reference when Harvest should trade API freshness for speed, lower rate-limit risk, or repeated query efficiency.

## Contents

- Cache types and TTLs
- Storage layout
- Cache policies
- Invalidation rules
- Cleanup limits

## Cache Types And TTLs

| Cache type | TTL | Storage | Use case |
|------------|:---:|---------|----------|
| PR list | `5 min` | File | Recent PR queries |
| PR details | `15 min` | File | Individual PR metadata |
| User stats | `1 hour` | File | Contributor summaries |
| Repository info | `24 hours` | File | Stable repo metadata |
| Query results | `15 min` | File | Aggregated report inputs |
| Rate limit | `1 min` | Memory | API quota tracking |

Merged PR lists may safely use a longer TTL (`15 min`) because merged state is immutable.

## Storage Layout

```text
.harvest/
  cache/
    pr-lists/
    pr-details/
    users/
    queries/
    meta/
```

Keep cache entries repository-scoped and JSON-based.

## Key Patterns

Examples:

```text
{repo}:{state}:{limit}:{filters_hash}
{repo}:{query_type}:{date_range}
```

## Cache Policies

These policies are part of the handoff/behavior contract:

| Policy | Behavior |
|--------|----------|
| `prefer_cache` | Use cache if valid, fetch on miss |
| `force_refresh` | Invalidate and fetch fresh data |
| `cache_only` | Return cached data only; fail on miss |
| `no_cache` | Fetch fresh data and do not write cache |

`prefer_cache` is the default.

## Invalidation Rules

| Trigger | Invalidate |
|---------|------------|
| PR merged | PR list cache for that repo |
| PR created | Open-PR list cache |
| Manual refresh | Matching query cache |
| Date range change | Query-result cache |
| Report generation | None; read valid cache if present |

## Guardian Integration

Preserve this inbound contract:

```yaml
GUARDIAN_TO_HARVEST_HANDOFF:
  request: "release_notes"
  tag_range:
    from: "v1.1.0"
    to: "v1.2.0"
  cache_policy: "prefer_cache"
```

## Cleanup Limits

| Limit | Value |
|-------|-------|
| Max cache size | `100 MB` |
| Max entries | `1000` |
| Max age | `7 days` |

Cleanup rules:
- Remove entries older than `7 days`.
- Prune if total size exceeds `100 MB`.
- Keep metrics in `meta/metrics.json` if cache-hit tracking is enabled.

## Rate-Limit Backed Cache Posture (2026)

GitHub's published limits make caching mandatory for any non-trivial report (`docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api`, `docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api`):
- 5,000 REST req/hr primary; 900 REST points/min secondary; 100 concurrent (shared with GraphQL); 2,000 GraphQL points/min.
- A monthly report covering 500 merged PRs costs ~5 paginated REST requests when `per_page=100` is honored — but adding per-PR review timelines balloons quickly. Cache review timelines (15 min TTL) before fanning out.
- Use ETag / `If-Modified-Since` conditional requests where available; conditional 304 responses do not count against most secondary limits per GitHub's published guidance.
- Webhooks beat polling for live data — for any near-real-time report, route through Pulse rather than tightening the Harvest cache TTL.
