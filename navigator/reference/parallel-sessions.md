# Parallel Browser Sessions

Reference for Navigator's `parallel` recipe. Covers `BrowserContext` isolation, worker pool sizing, shared auth state, per-task timeouts, queue management for batches >100 URLs, and throughput vs detection trade-off.

---

## 1. When Parallelism Is Justified

| Scenario | Parallelism? | Reason |
|---|---|---|
| Single page interaction | No | Serialization adds nothing |
| Scraping 5-10 URLs | Maybe | Per-request overhead may dominate |
| Scraping 100-1000 URLs | Yes | Throughput matters; concurrency 3-8 |
| 10K+ URLs | Yes + queue | Backpressure + checkpointing required |
| Logged-in flows across N accounts | Yes | One context per account, isolation mandatory |
| A/B test variants | Yes | One context per variant for clean state |
| Cross-browser validation | Yes | One context per engine (chromium/webkit/firefox) |

**Anti-pattern**: opening N pages in one context for "parallelism" — they share cookies/cache/IndexedDB and serialize on the same JS event loop for blocking operations. **One context per worker** is the only reliable isolation.

---

## 2. Worker Pool Sizing

### Constraints
- **CPU cores** — each Chromium instance ≈ 200-500MB RAM, ~1 core under load
- **Target rate limit** — N workers × M req/sec ≤ allowed rate
- **Detection threshold** — too many concurrent IPs from one source increases bot signal
- **Network bandwidth** — typically not the limit for HTML scraping
- **Anti-bot system tolerance** — Cloudflare/Akamai allow N concurrent connections per source IP

### Default sizing
```
pool_size = min(
  CPU_cores / 2,                           # leave headroom
  target_rate_limit / per_worker_rate,     # rate budget
  detection_safe_concurrency,              # typ. 3-8 per source IP
)
```

### Common starting points
- Local dev: 3-4 workers
- CI runner (4 cores): 2-3 workers
- Dedicated scraping VM (16 cores): 6-10 workers
- With residential proxy rotation: up to 20-30 (each gets unique IP)

---

## 3. BrowserContext Isolation

```js
import { chromium } from 'playwright';

async function runWorker(workerId, urls) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    // Each worker gets isolated cookies, cache, storage
    storageState: workerId === 'authenticated' ? 'auth.json' : undefined,
    viewport: { width: 1280, height: 800 },
    userAgent: rotateUserAgent(),
  });
  const page = await context.newPage();

  for (const url of urls) {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30_000 });
    // ... extract
  }

  await context.close();
  await browser.close();
}
```

### What `newContext()` isolates
- Cookies
- localStorage / sessionStorage / IndexedDB
- HTTP cache
- Service workers
- Authentication state
- Permissions
- Geolocation

### What it shares within a `Browser`
- Browser binary process
- GPU process

For complete isolation (separate process per worker), launch a separate `Browser` per worker — costs more RAM but truly independent.

---

## 4. Shared Auth State (Write-Once Read-Many)

### Step 1: Authenticate once, save state
```js
// auth-setup.js (run once)
const browser = await chromium.launch();
const context = await browser.newContext();
const page = await context.newPage();
await page.goto('https://example.com/login');
await page.fill('input[name="email"]', process.env.EMAIL);
await page.fill('input[name="password"]', process.env.PASSWORD);
await page.click('button[type="submit"]');
await page.waitForURL('**/dashboard');
await context.storageState({ path: 'auth.json' });
await browser.close();
```

### Step 2: Reuse across workers
```js
const context = await browser.newContext({ storageState: 'auth.json' });
```

### Caveats
- `auth.json` contains session tokens — treat as secret, gitignore, encrypt at rest
- Sessions expire — refresh logic required for long-running pools
- Avoid simultaneous mutations (e.g., 5 workers POST'ing the same form) → server-side dedup or worker-level locking needed
- For multi-account pools: one `auth-{accountId}.json` per identity; never share

---

## 5. Pool Implementation Patterns

### Simple pool with `p-limit`
```js
import pLimit from 'p-limit';
const limit = pLimit(5);
const browser = await chromium.launch();

const results = await Promise.all(
  urls.map(url => limit(async () => {
    const context = await browser.newContext({ storageState: 'auth.json' });
    const page = await context.newPage();
    try {
      await page.goto(url);
      return await page.evaluate(() => document.title);
    } finally {
      await context.close();
    }
  }))
);
await browser.close();
```

### Worker pool with persistent contexts (lower per-task overhead)
```js
const browser = await chromium.launch();
const POOL_SIZE = 5;
const queue = [...urls];
const workers = Array.from({ length: POOL_SIZE }, async (_, i) => {
  const context = await browser.newContext({ storageState: 'auth.json' });
  const page = await context.newPage();
  const results = [];
  while (queue.length > 0) {
    const url = queue.shift();
    if (!url) break;
    try {
      await page.goto(url, { timeout: 30_000 });
      results.push({ url, ok: true, title: await page.title() });
    } catch (err) {
      results.push({ url, ok: false, error: String(err) });
    }
  }
  await context.close();
  return results;
});
const allResults = (await Promise.all(workers)).flat();
await browser.close();
```

Persistent contexts are 3-5x faster than create/destroy per task, but require trusting that pages don't pollute each other (clear cookies between tasks if needed).

### Heavy-duty: BullMQ + Redis
For 10K+ URLs, durable queues with BullMQ:
- Producer: enqueues jobs
- Worker process: pulls jobs, runs Playwright
- Failed jobs auto-retry with exponential backoff
- Persistent across restarts
- Horizontal scale: add workers across machines

---

## 6. Per-Task Timeout & Cancellation

```js
async function runWithTimeout(page, url, timeoutMs = 120_000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    await page.goto(url, { timeout: 30_000, signal: controller.signal });
    await page.waitForLoadState('networkidle', { timeout: 15_000 });
    return await page.evaluate(() => document.body.innerText);
  } finally {
    clearTimeout(timer);
  }
}
```

### Timeout layers
- Navigation: 30s default
- Element wait: 10s default
- Whole task budget: 60-120s (covers nav + extract + recovery)
- Worker max lifetime: 1-2 hours (recycle to avoid memory leaks)

---

## 7. Queue Management for Large Batches

### Backpressure
```js
import PQueue from 'p-queue';
const queue = new PQueue({ concurrency: 5, intervalCap: 30, interval: 60_000 });
// ↑ Max 5 concurrent + at most 30 per minute (rate limiting)

for (const url of largeUrlList) {
  queue.add(() => scrape(url));
}
await queue.onIdle();
```

### Checkpointing (resume after crash)
```js
import fs from 'node:fs';
const CHECKPOINT = '.navigator/checkpoint.jsonl';
const completed = new Set(
  fs.existsSync(CHECKPOINT)
    ? fs.readFileSync(CHECKPOINT, 'utf8').split('\n').filter(Boolean).map(l => JSON.parse(l).url)
    : []
);
const remaining = urls.filter(u => !completed.has(u));
console.log(`Resuming: ${completed.size} done, ${remaining.length} remaining`);

for (const url of remaining) {
  const result = await scrape(url);
  fs.appendFileSync(CHECKPOINT, JSON.stringify({ url, result, ts: Date.now() }) + '\n');
}
```

### Aggregate failure reporting
```js
const failures = results.filter(r => !r.ok);
if (failures.length > 0) {
  console.warn(`${failures.length}/${results.length} failed:`);
  const byError = failures.reduce((acc, r) => {
    const key = r.error.split('\n')[0].slice(0, 80);
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});
  console.table(byError);
}
```

---

## 8. Throughput vs Detection Trade-Off

| Concurrency | Throughput | Detection risk |
|---|---|---|
| 1 (serial) | Lowest | Lowest — looks like one user |
| 3-5 | Good | Low — single power user |
| 10-15 | High | Moderate — small office |
| 30+ | Very high | High — bot pool signature |
| 100+ | Maximum | Almost certain detection without proxy rotation |

### Mitigation when scaling up
- Distribute across residential IPs (one IP per worker minimum)
- Stagger starts (don't fire 50 workers in same second)
- Add jitter between requests
- Honor `Retry-After` headers
- Backoff on 429/503 (exponential + jitter)

---

## 9. Common Pitfalls

| Pitfall | Symptom | Avoidance |
|---|---|---|
| Sharing one context across workers | Cookie pollution, race conditions | One context per worker |
| Not closing contexts | Memory leak, browser zombies | `await context.close()` in finally block |
| Pool size = CPU cores | OOM, swap thrashing | Use `cores / 2` as starting point |
| No checkpointing on 10K+ batch | Crash = restart from zero | Append-only JSONL checkpoint |
| Ignoring 429 retries | IP gets banned | Honor Retry-After + exponential backoff |
| Same UA across 100 workers | Bot pool signature | Rotate UAs + consider per-worker fingerprint |
| Auth shared but session expires | Cascading failures mid-batch | Pre-flight check + refresh logic |
| Writing to same file from N workers | Corruption | Use `appendFileSync` (atomic) or per-worker file |
| Worker zombies after parent crash | Resource leak | Use `process.on('SIGTERM')` cleanup |
| All workers share IP, target detects burst | Block | Residential proxy rotation, one IP per worker |

---

## 10. Decision Walkthrough Template

```
Total URL count: ____
Per-URL avg time: ___s
Target throughput: ___ URLs/min
Detected anti-bot: Yes / No (system: ____)

Pool sizing:
  CPU cores: ___
  RAM available: ___ GB
  Per-worker estimate: 300-500 MB
  Calculated pool size: ___
  Rate-limit budget: ___ req/min

Auth strategy:
  □ No auth required
  □ Single shared auth (storageState)
  □ Per-account auth (one context per identity)

Queue strategy:
  □ Promise.all (small batches < 100)
  □ p-limit (medium batches < 1K)
  □ p-queue with rate cap (1K-10K)
  □ BullMQ + Redis (10K+, persistent, multi-machine)

Resilience:
  □ Per-task timeout (default 120s)
  □ Checkpoint to JSONL (every N tasks or every result)
  □ Worker max lifetime (recycle every 1-2h)
  □ Aggregate failure report at end
  □ Retry transient failures (network, 5xx) with backoff

Detection mitigation:
  □ Jittered delays
  □ UA rotation
  □ Proxy rotation (one IP per worker for >10 concurrency)
  □ Honor Retry-After / 429
```

---

## 11. References
- Playwright `BrowserContext` docs (isolation guarantees)
- `p-limit`, `p-queue` (lightweight concurrency control)
- BullMQ (durable queues with Redis)
- `storageState` API (auth persistence)
- Anti-bot system documentation (Cloudflare Bot Management thresholds)
