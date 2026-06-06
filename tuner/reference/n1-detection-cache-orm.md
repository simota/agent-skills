# N+1 Detection, Cache Integration & ORM Optimization

Purpose: Use this file when diagnosing N+1 patterns, deciding whether to cache, or suggesting ORM eager-loading changes.

Contents:
- N+1 detection signals
- cache decision matrix
- cache-aside pattern
- ORM eager-loading examples

## N+1 Detection Signals

- repeated similar queries with different IDs
- query count scaling with returned rows
- lazy-loading traces in ORM logs

Typical symptom:
- page load reaches `2500ms+`
- many nearly identical per-row queries

## Detection Checklist

```markdown
## N+1 Detection Report

### Symptoms
- [ ] page load > 1s with many DB calls
- [ ] repeated queries differ only by ID
- [ ] query count scales with N rows

### Fix Recommendations
| Pattern | Recommended fix |
|---------|-----------------|
| lazy load | eager load |
| loop query | batch `IN (...)` query |
| nested load | `JOIN` or eager relation fetch |
```

## Cache Decision Matrix

| Query Type | Frequency | Volatility | Recommended Cache |
|------------|-----------|------------|-------------------|
| user profile | high | low | Redis (`TTL: 1hr`) |
| product catalog | high | medium | Redis (`TTL: 10min`) |
| search results | high | high | application cache (`TTL: 1min`) |
| analytics | low | low | materialized view |
| real-time data | high | high | no cache |

## Cache-Aside Pattern

```typescript
async function getUserWithCache(userId: string): Promise<User> {
  const cacheKey = `user:${userId}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const user = await db.user.findUnique({ where: { id: userId } });
  await redis.setex(cacheKey, 3600, JSON.stringify(user));
  return user;
}
```

## ORM Eager-Loading Examples

```typescript
// Prisma
await prisma.user.findMany({ include: { posts: true } });

// TypeORM
await userRepository.find({ relations: ['posts'] });

// Drizzle
await db.query.users.findMany({ with: { posts: true } });
```
