# Webhook Patterns

> **2026 note: webhook is the back-channel of choice for agentic / long-running AI work.** Anthropic's Managed Agents and the broader 2026 "agentic SaaS" stack ship **completion webhooks** as the canonical way to notify external systems that an unattended multi-day run finished, an Evaluator Loop rubric passed, or a remediation action completed. Pair the patterns in this file with the receivers documented in `mend/reference/safety-model.md` and the incident-postmortem hooks in `beacon/reference/incident-learning-postmortem.md`. Treat agentic completion webhooks under the same signing / replay-protection / idempotency discipline as any other production webhook — the AI agent author does not get a discount on supply-chain hygiene.

## HMAC-SHA256 Signature Verification

```typescript
import crypto from 'node:crypto';

// Generic webhook signature verifier
function verifyWebhookSignature(
  payload: string | Buffer,
  signature: string,
  secret: string,
  algorithm: 'sha256' | 'sha1' = 'sha256',
): boolean {
  const expected = crypto
    .createHmac(algorithm, secret)
    .update(payload)
    .digest('hex');

  const sig = signature.replace(/^(sha256|sha1)=/, '');

  // Timing-safe comparison to prevent timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(sig, 'hex'),
    Buffer.from(expected, 'hex'),
  );
}
```

### Platform-Specific Verification

| Platform | Header | Algorithm | Format |
|----------|--------|-----------|--------|
| Slack | `X-Slack-Signature` | HMAC-SHA256 | `v0=<hex>` with timestamp |
| Discord | `X-Signature-Ed25519` | Ed25519 | Hex signature + timestamp |
| Stripe | `Stripe-Signature` | HMAC-SHA256 | `t=<ts>,v1=<hex>` |
| GitHub | `X-Hub-Signature-256` | HMAC-SHA256 | `sha256=<hex>` |
| Telegram | N/A (IP whitelist + secret token) | Token-based | Query param or header |
| LINE | `X-Line-Signature` | HMAC-SHA256 | Base64 |
| WhatsApp | `X-Hub-Signature-256` | HMAC-SHA256 | `sha256=<hex>` |

### Slack Verification (with timestamp)

```typescript
function verifySlackRequest(
  body: string,
  timestamp: string,
  signature: string,
  signingSecret: string,
): boolean {
  // Reject requests older than 5 minutes (replay attack prevention)
  const fiveMinAgo = Math.floor(Date.now() / 1000) - 300;
  if (parseInt(timestamp) < fiveMinAgo) return false;

  const baseString = `v0:${timestamp}:${body}`;
  const hash = crypto
    .createHmac('sha256', signingSecret)
    .update(baseString)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(`v0=${hash}`),
    Buffer.from(signature),
  );
}
```

## Idempotency

### Idempotency Key Strategy

```typescript
interface IdempotencyStore {
  exists(key: string): Promise<boolean>;
  set(key: string, result: unknown, ttlMs: number): Promise<void>;
  get(key: string): Promise<unknown | null>;
}

// Redis-based idempotency
class RedisIdempotencyStore implements IdempotencyStore {
  constructor(private redis: Redis) {}

  async exists(key: string): Promise<boolean> {
    return (await this.redis.exists(`idempotency:${key}`)) === 1;
  }

  async set(key: string, result: unknown, ttlMs: number): Promise<void> {
    await this.redis.set(
      `idempotency:${key}`,
      JSON.stringify(result),
      'PX',
      ttlMs,
    );
  }

  async get(key: string): Promise<unknown | null> {
    const data = await this.redis.get(`idempotency:${key}`);
    return data ? JSON.parse(data) : null;
  }
}
```

### Idempotent Webhook Handler

```typescript
async function handleWebhookIdempotent(
  eventId: string,
  handler: () => Promise<unknown>,
  store: IdempotencyStore,
  ttlMs = 24 * 60 * 60 * 1000, // 24 hours
): Promise<{ result: unknown; deduplicated: boolean }> {
  // Check if already processed
  const existing = await store.get(eventId);
  if (existing !== null) {
    return { result: existing, deduplicated: true };
  }

  // Process and store result
  const result = await handler();
  await store.set(eventId, result, ttlMs);
  return { result, deduplicated: false };
}
```

## Retry Strategy

### Exponential Backoff with Jitter

```typescript
interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  jitter: boolean;
}

const DEFAULT_RETRY: RetryConfig = {
  maxRetries: 3,
  baseDelayMs: 1000,
  maxDelayMs: 30000,
  jitter: true,
};

function calculateDelay(attempt: number, config: RetryConfig): number {
  const exponentialDelay = config.baseDelayMs * Math.pow(2, attempt);
  const cappedDelay = Math.min(exponentialDelay, config.maxDelayMs);

  if (!config.jitter) return cappedDelay;

  // Full jitter: random between 0 and cappedDelay
  return Math.random() * cappedDelay;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  config: RetryConfig = DEFAULT_RETRY,
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (attempt < config.maxRetries) {
        const delay = calculateDelay(attempt, config);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError!;
}
```

### Retry Decision Matrix

| Error Type | Retry? | Strategy |
|-----------|--------|----------|
| 2xx | No | Success |
| 400 Bad Request | No | Fix payload |
| 401 Unauthorized | No | Refresh token, retry once |
| 403 Forbidden | No | Check permissions |
| 404 Not Found | No | Fix endpoint |
| 408 Timeout | Yes | Exponential backoff |
| 429 Too Many Requests | Yes | Respect Retry-After header |
| 500 Server Error | Yes | Exponential backoff |
| 502/503/504 | Yes | Exponential backoff |
| Network Error | Yes | Exponential backoff |
| DNS Error | No | Fix configuration |

## Dead Letter Queue (DLQ)

```typescript
interface DeadLetterEntry {
  id: string;
  originalEvent: unknown;
  error: string;
  attempts: number;
  firstFailedAt: Date;
  lastFailedAt: Date;
  metadata: {
    platform: string;
    eventType: string;
    webhookId: string;
  };
}

interface DeadLetterQueue {
  push(entry: DeadLetterEntry): Promise<void>;
  peek(limit: number): Promise<DeadLetterEntry[]>;
  retry(id: string): Promise<boolean>;
  discard(id: string): Promise<void>;
  stats(): Promise<{ total: number; byPlatform: Record<string, number> }>;
}
```

## Webhook Handler Middleware Chain

```typescript
type WebhookMiddleware = (
  ctx: WebhookContext,
  next: () => Promise<void>,
) => Promise<void>;

interface WebhookContext {
  rawBody: Buffer;
  headers: Record<string, string>;
  event: unknown;
  platform: PlatformType;
  verified: boolean;
  idempotencyKey?: string;
  metadata: Record<string, unknown>;
}

// Standard middleware chain
const webhookPipeline: WebhookMiddleware[] = [
  signatureVerification,   // 1. Verify HMAC signature
  timestampValidation,     // 2. Reject stale requests
  rateLimiting,            // 3. Per-source rate limit
  idempotencyCheck,        // 4. Deduplicate events
  eventParsing,            // 5. Parse and normalize
  messageRouting,          // 6. Route to handler
  errorHandling,           // 7. Catch and DLQ
];
```

## Webhook Health & Monitoring

```typescript
interface WebhookMetrics {
  received: number;
  processed: number;
  failed: number;
  deduplicated: number;
  averageLatencyMs: number;
  dlqSize: number;
}

// Health endpoint response
interface WebhookHealth {
  status: 'healthy' | 'degraded' | 'unhealthy';
  uptime: number;
  lastEventAt: Date | null;
  metrics: WebhookMetrics;
  platforms: Record<PlatformType, {
    connected: boolean;
    lastEventAt: Date | null;
    errorRate: number;
  }>;
}
```
