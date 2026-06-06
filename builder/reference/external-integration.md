# External API Integration Reference

Purpose: Build production-grade integration with third-party APIs. Sandbox-first, secure secret handling, vendor-aware retry/backoff, webhook verification, and failure-mode tested.

## Integration Checklist

Before writing any integration code:

- [ ] Sandbox / test account set up (never prototype against prod)
- [ ] Secrets stored outside repo (env vars / Vault / AWS SM / Doppler)
- [ ] API spec (OpenAPI / docs) reviewed for rate limits, auth, idempotency, pagination
- [ ] Webhook endpoint required? signature verification pattern identified
- [ ] Vendor-specific quirks documented (known retry semantics, error codes)
- [ ] Failure modes enumerated: timeout, rate limit, 5xx, partial success, retry storm

## Stage 1: Sandbox Prototype

All integration work starts in sandbox. Never test against production keys.

```ts
// config.ts
const config = {
  STRIPE_API_KEY: requireEnv('STRIPE_API_KEY'), // sk_test_* in sandbox
  STRIPE_WEBHOOK_SECRET: requireEnv('STRIPE_WEBHOOK_SECRET'),
  STRIPE_BASE_URL: process.env.STRIPE_BASE_URL ?? 'https://api.stripe.com',
};
```

Sandbox key prefix conventions (confirm in docs):
- Stripe: `sk_test_*`, `sk_live_*`
- Twilio: separate sub-account
- GitHub: separate OAuth app
- AWS: separate account or least-privilege IAM role

## Stage 2: Retry / Backoff

### Vendor-aware retry matrix

| Status | Retry? | Strategy |
|--------|--------|----------|
| 2xx | never | success |
| 4xx (except 408, 425, 429) | never | client error, fail immediately |
| 408, 425 | yes | client retry with exponential backoff |
| 429 | yes | respect `Retry-After` header, then exponential |
| 500, 502, 503, 504 | yes | exponential backoff + jitter, max 5 retries |
| Network error | yes | exponential backoff + jitter, max 5 retries |

```ts
async function call(req: Request, opts: RetryOpts = {}): Promise<Response> {
  const max = opts.maxRetries ?? 5;
  let attempt = 0;
  while (true) {
    try {
      const res = await fetch(req, { signal: AbortSignal.timeout(opts.timeoutMs ?? 30_000) });
      if (res.status >= 200 && res.status < 300) return res;

      if (res.status === 429 || (res.status >= 500 && res.status < 600)) {
        if (attempt >= max) throw new RetryExhausted(res);
        const retryAfter = parseRetryAfter(res.headers.get('retry-after'));
        const delay = retryAfter ?? expBackoff(attempt);
        await sleep(delay);
        attempt++;
        continue;
      }

      // 4xx non-retryable
      throw new ClientError(res);
    } catch (e) {
      if (isNetworkError(e) && attempt < max) {
        await sleep(expBackoff(attempt));
        attempt++;
        continue;
      }
      throw e;
    }
  }
}

function expBackoff(attempt: number): number {
  const base = Math.min(1000 * 2 ** attempt, 30_000);
  return base + Math.random() * base * 0.25; // 0-25% jitter
}
```

### Idempotency keys (for mutations)

```ts
await stripe.charges.create(
  { amount: 1000, currency: 'usd' },
  { idempotencyKey: `charge-${orderId}-${attempt}` }
);
```

Always use a stable key derived from the business operation (not a random UUID generated each call).

## Stage 3: Webhook Verification

Vendors send webhooks signed with HMAC or similar. Verifying signatures is **mandatory** for security.

### Stripe

```ts
import Stripe from 'stripe';
const stripe = new Stripe(config.STRIPE_API_KEY);

app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(req.body, sig, config.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }
  // dispatch event
  handleStripeEvent(event);
  res.json({ received: true });
});
```

### GitHub

```ts
import crypto from 'crypto';
function verifyGithubSignature(payload: Buffer, signature: string): boolean {
  const expected = 'sha256=' + crypto
    .createHmac('sha256', config.GITHUB_WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');
  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
}
```

**Use `timingSafeEqual`**, never `===` — prevents timing attack.

### Idempotency on receive side

Webhooks can be redelivered. Dedupe via event ID:

```ts
async function handleStripeEvent(event: Stripe.Event) {
  if (await seenEvent(event.id)) return; // idempotent
  await markSeen(event.id);
  // process
}
```

## Stage 4: Failure-Mode Tests

| Scenario | How to test |
|----------|-------------|
| 500 then success | mock server returns 500 once, then 200 |
| Timeout | mock server delays > timeout |
| 429 with Retry-After | mock returns 429 with header |
| Network error | use `nock.disableNetConnect()` or offline harness |
| Partial success | mock returns 200 but `items[2].status === 'failed'` |
| Webhook replay | send same payload twice, assert idempotent |
| Invalid signature | send tampered payload |
| Clock skew | send old timestamp (past tolerance window) |

## Stage 5: Observability

Every integration must emit:
- Request count by vendor + endpoint
- Latency p50/p95/p99
- Error rate by status category (4xx / 5xx / network / timeout)
- Rate limit consumption (if vendor reports headers)
- Retry count per operation
- Circuit breaker state (if used)

Log shape (PII-safe):
```json
{
  "vendor": "stripe",
  "endpoint": "POST /v1/charges",
  "status": 200,
  "latency_ms": 340,
  "retries": 1,
  "idempotency_key": "charge-order-42-attempt-1",
  "request_id": "req_xyz123"
}
```

Never log full request/response bodies without PII scrubbing.

## Vendor-Specific Gotchas

| Vendor | Quirk |
|--------|-------|
| Stripe | idempotency keys expire after 24h; webhook timestamp tolerance 5 min |
| Twilio | messages have segments (SMS > 160 chars); cost varies |
| GitHub | rate limit tied to auth method (unauth 60/h, app-installation up to 15k/h) |
| Slack | rate limits per-workspace, per-method; `retry_after` in JSON body, not header |
| OpenAI | RPM + TPM (tokens-per-minute) limits; 429 can mean either |
| AWS | exponential backoff w/ jitter built into SDKs; still cap at max attempts |
| Google (OAuth) | refresh token rotation; handle `invalid_grant` re-auth flow |
| Shopify | 40 req/s across all shop APIs; leaky bucket |

## Handoff

- **Gateway**: if this integration's internal API needs to be exposed downstream
- **Crypt**: if signature/token handling needs review
- **Sentinel**: secret-scanning before commit
- **Beacon**: observability dashboard for the new integration
- **Radar**: failure-mode test suite
- **Guardian**: PR preparation with vendor credentials checklist
