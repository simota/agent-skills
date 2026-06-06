# Bolt Caching Strategy Patterns

Cache-aside, LRU, HTTP caching, and Redis patterns.

## 2026 Notes

- **Anthropic prompt caching** is the single highest-ROI caching to enable on any LLM-backed feature in 2026: pin stable system prompts and tool definitions inside `cache_control` blocks; provider-managed KV cache delivers `up to ~90%` input-cost reduction with no application code changes. See `oracle/reference/llm-application-patterns.md` for the canonical hit-rate table.
- **Next.js 16 Cache Components** replace the implicit "cache everything by default" of earlier App Router versions — caching is now **opt-in per-component**. When migrating a Next.js codebase to `16+`, treat every previously-cached fetch as suspect until it is explicitly re-annotated; see `shift/reference/framework-migration.md`.
- **HTTP `Cache-Control: stale-while-revalidate`** is now baseline across every major CDN and origin runtime in 2026 — wire it on for any read-heavy endpoint before reaching for the in-process LRU below. The cheapest cache is one you do not run.

---

## Cache-Aside Pattern (Lazy Loading)

```typescript
interface CacheOptions {
  ttl: number; // seconds
  staleWhileRevalidate?: number;
}

class CacheService {
  constructor(private redis: Redis) {}

  async get<T>(
    key: string,
    fetcher: () => Promise<T>,
    options: CacheOptions
  ): Promise<T> {
    const cached = await this.redis.get(key);

    if (cached) {
      const { data, timestamp } = JSON.parse(cached);
      const age = (Date.now() - timestamp) / 1000;

      // Return cached data, optionally revalidate in background
      if (age < options.ttl) {
        return data as T;
      }

      if (options.staleWhileRevalidate && age < options.ttl + options.staleWhileRevalidate) {
        // Return stale data, revalidate in background
        this.revalidate(key, fetcher, options);
        return data as T;
      }
    }

    // Cache miss or expired: fetch fresh data
    return this.revalidate(key, fetcher, options);
  }

  private async revalidate<T>(
    key: string,
    fetcher: () => Promise<T>,
    options: CacheOptions
  ): Promise<T> {
    const data = await fetcher();
    await this.redis.setex(
      key,
      options.ttl + (options.staleWhileRevalidate ?? 0),
      JSON.stringify({ data, timestamp: Date.now() })
    );
    return data;
  }

  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }
}

// Usage
const user = await cache.get(
  `user:${userId}`,
  () => db.user.findUnique({ where: { id: userId } }),
  { ttl: 300, staleWhileRevalidate: 60 }
);
```

---

## In-Memory LRU Cache

```typescript
class LRUCache<K, V> {
  private cache = new Map<K, { value: V; expiry: number }>();
  private readonly maxSize: number;
  private readonly defaultTtl: number;

  constructor(maxSize: number = 1000, defaultTtlMs: number = 60000) {
    this.maxSize = maxSize;
    this.defaultTtl = defaultTtlMs;
  }

  get(key: K): V | undefined {
    const entry = this.cache.get(key);

    if (!entry) return undefined;

    if (Date.now() > entry.expiry) {
      this.cache.delete(key);
      return undefined;
    }

    // Move to end (most recently used)
    this.cache.delete(key);
    this.cache.set(key, entry);

    return entry.value;
  }

  set(key: K, value: V, ttlMs?: number): void {
    // Remove oldest entries if at capacity
    while (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }

    this.cache.set(key, {
      value,
      expiry: Date.now() + (ttlMs ?? this.defaultTtl)
    });
  }

  delete(key: K): boolean {
    return this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }
}

// Usage with async wrapper
const cache = new LRUCache<string, User>(500, 5 * 60 * 1000);

async function getUser(id: string): Promise<User> {
  const cached = cache.get(`user:${id}`);
  if (cached) return cached;

  const user = await db.user.findUnique({ where: { id } });
  if (user) cache.set(`user:${id}`, user);
  return user;
}
```

---

## HTTP Cache Headers

```typescript
// Next.js App Router
export async function GET(request: Request) {
  const data = await fetchData();

  return Response.json(data, {
    headers: {
      // Cache for 60 seconds, allow stale for 1 hour while revalidating
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=3600',
      // ETag for conditional requests
      'ETag': generateETag(data),
    }
  });
}

// Express middleware
function cacheControl(options: { maxAge: number; staleWhileRevalidate?: number }) {
  return (req: Request, res: Response, next: NextFunction) => {
    const directives = [`public`, `max-age=${options.maxAge}`];

    if (options.staleWhileRevalidate) {
      directives.push(`stale-while-revalidate=${options.staleWhileRevalidate}`);
    }

    res.setHeader('Cache-Control', directives.join(', '));
    next();
  };
}

// Cache strategies by content type
const cacheStrategies = {
  // Static assets: Long cache with immutable
  static: 'public, max-age=31536000, immutable',

  // API data: Short cache with revalidation
  api: 'public, s-maxage=60, stale-while-revalidate=300',

  // User-specific: Private, short cache
  private: 'private, max-age=60',

  // No cache: Dynamic content
  noCache: 'no-store, must-revalidate',
};
```

---

## Redis Caching Patterns

```typescript
// Write-through: Update cache on every write
async function updateUser(id: string, data: UpdateUserData): Promise<User> {
  const user = await db.user.update({ where: { id }, data });
  await redis.setex(`user:${id}`, 300, JSON.stringify(user));
  return user;
}

// Write-behind: Queue updates, batch write to DB
class WriteBackQueue {
  private queue: Map<string, { data: unknown; timestamp: number }> = new Map();
  private flushInterval: NodeJS.Timeout;

  constructor(private flushMs: number = 1000) {
    this.flushInterval = setInterval(() => this.flush(), flushMs);
  }

  async set(key: string, data: unknown): Promise<void> {
    this.queue.set(key, { data, timestamp: Date.now() });
    await redis.setex(key, 300, JSON.stringify(data));
  }

  private async flush(): Promise<void> {
    const entries = Array.from(this.queue.entries());
    this.queue.clear();

    if (entries.length === 0) return;

    await db.$transaction(
      entries.map(([key, { data }]) => {
        const [type, id] = key.split(':');
        return db[type].update({ where: { id }, data });
      })
    );
  }
}

// Cache invalidation patterns
async function invalidateUserCache(userId: string): Promise<void> {
  await Promise.all([
    redis.del(`user:${userId}`),
    redis.del(`user:${userId}:profile`),
    redis.del(`user:${userId}:orders`),
  ]);

  // Invalidate list caches that might contain this user
  const keys = await redis.keys('users:list:*');
  if (keys.length > 0) {
    await redis.del(...keys);
  }
}
```
