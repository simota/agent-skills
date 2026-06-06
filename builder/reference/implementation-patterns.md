# Implementation Patterns: Result, Validation, API, Performance

> Cross-cutting implementation patterns for type-safe, production-ready code

## 1. Result / Railway-Oriented Programming

### Result Type (TypeScript — neverthrow)

**Recommended:** `neverthrow` — `Result<T, E>` for sync, `ResultAsync<T, E>` for async.

```typescript
import { ok, err, Result, ResultAsync } from 'neverthrow';

// Domain method returning Result
class Order {
  confirm(): Result<Order, DomainError> {
    if (this.status !== 'draft')
      return err(new DomainError('Only draft orders can be confirmed'));
    return ok(new Order({ ...this.props, status: 'confirmed' }));
  }
}

// Async with ResultAsync.fromPromise
const fetchUser = (id: string): ResultAsync<User, ApiError> =>
  ResultAsync.fromPromise(
    api.get(`/users/${id}`),
    (e) => new ApiError('Failed to fetch user', e)
  );

// Railway chaining — .andThen() + .match()
const result = await fetchUser(id)
  .andThen(validateUser)
  .andThen(saveUser)
  .match(
    (user) => ({ success: true, user }),
    (error) => ({ success: false, error: error.message })
  );
```

### Combining Multiple Results

```typescript
// Fail-fast: collect all or return first error
function all<T, E>(results: Result<T, E>[]): Result<T[], E> {
  const values: T[] = [];
  for (const r of results) {
    if (r.isErr()) return r;
    values.push(r.value);
  }
  return ok(values);
}

// Collect all errors
function partition<T, E>(results: Result<T, E>[]): { ok: T[]; err: E[] } {
  const out = { ok: [] as T[], err: [] as E[] };
  for (const r of results) {
    if (r.isOk()) out.ok.push(r.value); else out.err.push(r.error);
  }
  return out;
}
```

### Pattern Matching

```typescript
// match() for exhaustive handling
const message = result.match(
  (user) => `Welcome, ${user.name}`,
  (error) => (error.code === 'NOT_FOUND' ? 'User not found' : 'An error occurred')
);

// unwrapOr() for safe defaults
const name = result.unwrapOr('Anonymous');
```

### Cross-Language Result Patterns

| Language | Library | Sync | Async | Pattern Matching |
|----------|---------|------|-------|-----------------|
| TypeScript | neverthrow | `Result<T,E>` | `ResultAsync<T,E>` | `.match()` |
| Go | stdlib | `(T, error)` | same | `errors.Is/As` |
| Python | returns | `Result[T,E]` | `Future[Result]` | `.bind()/.map()` |

- **TypeScript:** `neverthrow` (pragmatic) vs `Effect` (comprehensive, higher complexity)
- **Go:** `(value, error)` tuple is idiomatic ROP; `errors.Is/As` for inspection
- **Python:** `returns` library or exception hierarchies; Pydantic `model_validator` for invariants

---

## 2. Validation

### Zod v4 (TypeScript)

```typescript
import { z } from 'zod';

// Schema + safeParse (v4 top-level validators)
const UserSchema = z.object({
  id: z.uuid(),
  email: z.email(),
  name: z.string().min(1).max(100),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.coerce.date(),
});
type User = z.infer<typeof UserSchema>;

// v4: branded types (stable)
const UserIdSchema = z.uuid().brand<'UserId'>();
type UserId = z.infer<typeof UserIdSchema>;

// v4: unified error field
const NameSchema = z.string({ error: 'Name is required' }).min(1);

// v4: built-in JSON Schema export
// [Source: Zod — JSON Schema (zod.dev/json-schema)](https://zod.dev/json-schema)
const jsonSchema = UserSchema.toJSONSchema();

// v4: @zod/mini (tree-shakable)
import { object, string } from '@zod/mini';
const mini = object({ name: string() });
```

**Discriminated union, cross-field refinement, transform:**

```typescript
// Discriminated union
const PaymentSchema = z.discriminatedUnion('method', [
  z.object({
    method: z.literal('credit_card'),
    cardNumber: z.string().regex(/^\d{16}$/),
    expiryMonth: z.number().min(1).max(12),
    expiryYear: z.number().min(2024),
    cvv: z.string().regex(/^\d{3,4}$/),
  }),
  z.object({
    method: z.literal('bank_transfer'),
    bankCode: z.string().length(4),
    accountNumber: z.string().min(7).max(14),
  }),
  z.object({ method: z.literal('paypal'), email: z.email() }),
]);

// Cross-field refinement
const RegistrationSchema = z.object({
  email: z.email(),
  password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/),
  confirmPassword: z.string(),
}).refine(d => d.password === d.confirmPassword, {
  message: 'Passwords do not match', path: ['confirmPassword'],
});

// Transform + coerce for query params
const SearchSchema = z.object({
  q: z.string().transform(s => s.trim().toLowerCase()),
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  tags: z.preprocess(
    (v) => typeof v === 'string' ? v.split(',') : v,
    z.array(z.string()).default([])
  ),
});
```

**Safe parsing with Result integration:**

```typescript
function parseRequest<T>(schema: z.ZodType<T>, data: unknown): Result<T, ValidationError> {
  const r = schema.safeParse(data);
  if (!r.success) {
    const errors = r.error.errors.map(e => ({ path: e.path.join('.'), message: e.message }));
    return err(new ValidationError('Validation failed', errors));
  }
  return ok(r.data);
}
```

### Pydantic v2 (Python)

- Prefer `Annotated[T, Field()]` constraints over custom validators
- Use `model_validator` for cross-field rules
- Pydantic at API boundary; frozen dataclasses in domain layer

### Validation Architecture

- **Validate at boundaries:** API endpoints, CLI args, file input, external data
- **Domain objects enforce invariants:** always-valid model — never instantiate in an invalid state
- **Skip redundant validation:** if data cleared a boundary check, trust it downstream

---

## 3. API Integration

### REST Client with Retry

```typescript
class ApiClient {
  private readonly config = {
    maxRetries: 3, baseDelay: 1000, maxDelay: 10000,
    retryableStatuses: [408, 429, 500, 502, 503, 504],
  };

  async request<T>(options: RequestOptions): Promise<Result<T, ApiError>> {
    let lastError: ApiError | null = null;
    for (let attempt = 0; attempt <= this.config.maxRetries; attempt++) {
      try {
        const response = await fetch(options.url, {
          method: options.method,
          headers: { 'Content-Type': 'application/json', ...options.headers },
          body: options.body ? JSON.stringify(options.body) : undefined,
          signal: AbortSignal.timeout(options.timeout ?? 30000),
        });
        if (!response.ok) {
          if (this.config.retryableStatuses.includes(response.status) && attempt < this.config.maxRetries) {
            await this.delay(attempt); continue;
          }
          return err(new ApiError(response.status, await response.text()));
        }
        return ok(await response.json() as T);
      } catch (error) {
        lastError = this.handleError(error);
        if (attempt < this.config.maxRetries) { await this.delay(attempt); continue; }
      }
    }
    return err(lastError ?? new ApiError(0, 'Unknown error'));
  }

  private delay(attempt: number): Promise<void> {
    const ms = Math.min(this.config.baseDelay * Math.pow(2, attempt), this.config.maxDelay);
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### GraphQL Client

```typescript
class GraphQLClient {
  constructor(private endpoint: string, private headers: Record<string, string> = {}) {}

  async query<T, V extends Record<string, unknown>>(
    query: string, variables?: V
  ): Promise<Result<T, GraphQLClientError>> {
    const res = await fetch(this.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...this.headers },
      body: JSON.stringify({ query, variables }),
    });
    const { data, errors }: { data?: T; errors?: GraphQLError[] } = await res.json();
    if (errors?.length) return err(new GraphQLClientError(errors));
    if (!data) return err(new GraphQLClientError([{ message: 'No data returned' }]));
    return ok(data);
  }

  mutation<T, V extends Record<string, unknown>>(mutation: string, variables: V) {
    return this.query<T, V>(mutation, variables);
  }
}
```

### WebSocket Manager

```typescript
type ConnectionState = 'connecting' | 'connected' | 'disconnected' | 'reconnecting';

class WebSocketManager<TMessage> {
  private ws: WebSocket | null = null;
  private state: ConnectionState = 'disconnected';
  private reconnectAttempts = 0;
  private readonly maxReconnectAttempts = 5;
  private messageQueue: TMessage[] = [];

  constructor(
    private readonly url: string,
    private readonly handlers: {
      onMessage: (m: TMessage) => void;
      onStateChange: (s: ConnectionState) => void;
    }
  ) {}

  connect(): void {
    this.setState('connecting');
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => { this.setState('connected'); this.reconnectAttempts = 0; this.flushQueue(); };
    this.ws.onmessage = (e) => this.handlers.onMessage(JSON.parse(e.data) as TMessage);
    this.ws.onclose = () => { this.setState('disconnected'); this.attemptReconnect(); };
    this.ws.onerror = () => this.ws?.close();
  }

  send(message: TMessage): void {
    this.state === 'connected' && this.ws
      ? this.ws.send(JSON.stringify(message))
      : this.messageQueue.push(message);
  }

  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) return;
    this.setState('reconnecting');
    const delay = Math.min(1000 * Math.pow(2, ++this.reconnectAttempts), 30000);
    setTimeout(() => this.connect(), delay);
  }

  private flushQueue(): void {
    while (this.messageQueue.length) this.send(this.messageQueue.shift()!);
  }

  private setState(s: ConnectionState): void {
    this.state = s; this.handlers.onStateChange(s);
  }
}
```

### Rate Limiter

```typescript
class RateLimiter {
  private tokens: number;
  private lastRefill = Date.now();

  constructor(private maxTokens: number, private refillRate: number) {
    this.tokens = maxTokens;
  }

  async acquire(): Promise<void> {
    this.refill();
    if (this.tokens < 1) {
      await new Promise(r => setTimeout(r, (1 - this.tokens) / this.refillRate * 1000));
      this.refill();
    }
    this.tokens -= 1;
  }

  private refill(): void {
    const elapsed = (Date.now() - this.lastRefill) / 1000;
    this.tokens = Math.min(this.maxTokens, this.tokens + elapsed * this.refillRate);
    this.lastRefill = Date.now();
  }
}

// Compose with ApiClient
class RateLimitedApiClient extends ApiClient {
  constructor(private limiter: RateLimiter) { super(); }
  async request<T>(opts: RequestOptions): Promise<Result<T, ApiError>> {
    await this.limiter.acquire(); return super.request(opts);
  }
}
```

---

## 4. Performance Patterns

### N+1 Prevention

```typescript
// ❌ N+1 — one query per order
for (const order of orders) {
  order.items = await db.orderItem.findMany({ where: { orderId: order.id } });
}

// ✅ Eager loading — single JOIN
return db.order.findMany({ where: { customerId }, include: { items: true } });

// ✅ DataLoader (for GraphQL / batched contexts)
const orderItemsLoader = new DataLoader<string, OrderItem[]>(async (orderIds) => {
  const items = await db.orderItem.findMany({ where: { orderId: { in: orderIds as string[] } } });
  const byId = groupBy(items, 'orderId');
  return orderIds.map(id => byId[id] ?? []);
});
```

### Caching

```typescript
class CacheService {
  constructor(private redis: Redis) {}

  async getOrSet<T>(key: string, fetcher: () => Promise<T>, ttlSeconds = 300): Promise<T> {
    const cached = await this.redis.get(key);
    if (cached) return JSON.parse(cached) as T;
    const value = await fetcher();
    await this.redis.setex(key, ttlSeconds, JSON.stringify(value));
    return value;
  }

  async invalidate(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length) await this.redis.del(...keys);
  }
}

// Usage (stale-while-revalidate via TTL)
const user = await cache.getOrSet(`user:${userId}`, () => userRepo.findById(userId), 600);
```

### Batch Processing

```typescript
async function processLargeDataset<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  options = { batchSize: 100, concurrency: 5 }
): Promise<R[]> {
  const results: R[] = [];
  for (const batch of chunk(items, options.batchSize)) {
    results.push(...await Promise.all(batch.map(i => limit(() => processor(i), options.concurrency))));
    await sleep(100); // Backpressure between batches
  }
  return results;
}
```

### Virtualization

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
    overscan: 5,
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map((row) => (
          <div key={row.key} style={{
            position: 'absolute', top: 0, left: 0, width: '100%',
            height: row.size, transform: `translateY(${row.start}px)`,
          }}>
            <ItemRow item={items[row.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Sources

- `result-patterns.md` — Result type, ROP chaining, combining results, pattern matching, fromPromise
- `validation-recipes.md` — Zod schemas, discriminated unions, refinements, transforms, safe parsing
- `api-integration.md` — REST retry client, GraphQL client, WebSocket manager, rate limiter
- `performance-patterns.md` — N+1 prevention, Redis cache, batch processing, virtualization
