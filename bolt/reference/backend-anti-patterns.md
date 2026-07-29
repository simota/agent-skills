# Backend Performance Anti-Patterns

> Node.js/backend performance pitfalls, memory leaks, event loop blocking, and async processing issues

## 1. 8 Major Node.js Performance Anti-Patterns

| # | Anti-Pattern | Symptom | Detection Method | Countermeasure |
|---|-------------|------|---------|------|
| **BP-01** | **Event loop blocking** | All requests delayed, CPU 100% | Measure lag with `process.hrtime` | Split heavy computation with Worker Threads / `setImmediate()` |
| **BP-02** | **Memory leak** | Memory usage grows monotonically, OOM crash | `--inspect` + heap snapshot comparison | Resource cleanup, cache limits, use WeakRef |
| **BP-03** | **Unbounded cache** | Data accumulates indefinitely in a Map/Object | Identify large Maps via heap snapshot | Limit cache with LRU + maxSize + TTL |
| **BP-04** | **Synchronous file I/O** | `readFileSync` etc. block the event loop | `--prof` + search for sync APIs | Replace with `fs.promises` / Stream API |
| **BP-05** | **Reference retention via closures** | Callbacks hold large objects | Check for unexpected references via heap snapshot | Pass only the needed data into closures; explicit nulling |
| **BP-06** | **Unremoved event listeners** | `EventEmitter.listenerCount` keeps growing | MaxListeners warning | Reliably remove with `removeListener` / `once` / AbortController |
| **BP-07** | **String concatenation in loops** | `+=` concatenation of large amounts of string data | String operations rank high in CPU profile | Replace with `Array.push` + `join()` / Buffer / Stream |
| **BP-08** | **Connection pool exhaustion** | DB connection timeouts, request delays | Monitor connection count | Right-size pool + detect connection leaks + set timeouts |

---

## 2. Detecting and Countering Event Loop Blocking

```
How the event loop works:

  ┌─────────────────────────────┐
  │        timers (setTimeout)   │
  ├─────────────────────────────┤
  │   pending callbacks          │
  ├─────────────────────────────┤
  │   idle, prepare             │
  ├─────────────────────────────┤
  │   poll (I/O callbacks)      │ ← most processing happens here
  ├─────────────────────────────┤
  │   check (setImmediate)      │
  ├─────────────────────────────┤
  │   close callbacks           │
  └─────────────────────────────┘

Causes of blocking:
  - JSON.parse/stringify of large objects
  - Cryptographic operations (crypto.pbkdf2Sync)
  - Regex ReDoS (catastrophic backtracking)
  - Sorting/filtering large amounts of data
  - Synchronous file I/O (fs.*Sync)

Detection code:
  const start = process.hrtime.bigint();
  setImmediate(() => {
    const lag = Number(process.hrtime.bigint() - start) / 1e6;
    if (lag > 100) alert(`Event loop lag: ${lag}ms`);
  });

Countermeasure patterns:
  1. Split: divide batch processing with setImmediate()
  2. Worker Threads: offload CPU-intensive work
  3. Stream: process large data in chunks
  4. Async API: fs.readFile → fs.promises.readFile
```

---

## 3. Memory Leak Patterns and Countermeasures

### Common Leak Patterns

```
Pattern 1: Unbounded cache
  ❌ const cache = new Map(); // grows without limit
  ✅ LRU cache + maxSize + TTL

Pattern 2: Unremoved event listeners
  ❌ emitter.on('data', handler); // forgot to remove
  ✅ emitter.once('data', handler); // auto-removes
  ✅ const ac = new AbortController();
     emitter.on('data', handler, { signal: ac.signal });
     ac.abort(); // remove all at once

Pattern 3: Reference retention via closures
  ❌ function process(hugeData) {
       return () => console.log(hugeData.length); // retains all of hugeData
     }
  ✅ function process(hugeData) {
       const len = hugeData.length; // extract only what's needed
       return () => console.log(len);
     }

Pattern 4: Timers not cleared
  ❌ setInterval(check, 1000); // runs forever
  ✅ const id = setInterval(check, 1000);
     // at cleanup: clearInterval(id);

Pattern 5: DB connection leak
  ❌ const conn = await pool.connect();
     await conn.query(sql); // not released on error
  ✅ try { ... } finally { conn.release(); }
     // or use pool.query() (auto-releases)
```

### Memory Monitoring

```
Metrics to monitor:
  - process.memoryUsage().heapUsed — heap usage
  - process.memoryUsage().external — C++ objects
  - process.memoryUsage().rss — resident set size

Alert thresholds:
  - heapUsed > 70% of max-old-space-size → warning
  - heapUsed grows 50MB+ over 10 minutes → suspected leak
  - rss > 1.5GB (default config) → OOM risk
```

---

## 4. Async Processing Anti-Patterns

```
❌ Sequential await (serial execution):
  const user = await getUser(id);
  const orders = await getOrders(id);
  const reviews = await getReviews(id);
  // total: user time + orders time + reviews time

✅ Parallel await (concurrent execution):
  const [user, orders, reviews] = await Promise.all([
    getUser(id),
    getOrders(id),
    getReviews(id),
  ]);
  // total: max(user time, orders time, reviews time)

❌ Unhandled Promise rejection:
  someAsyncFn(); // error is caught nowhere

✅ Always handle errors:
  someAsyncFn().catch(handleError);
  // or wrap in try/catch

❌ A single failure in Promise.all stops everything:
  await Promise.all([critical(), optional()]); // optional failing halts all

✅ Handle individually with Promise.allSettled:
  const results = await Promise.allSettled([critical(), optional()]);
  const settled = results.map(r =>
    r.status === 'fulfilled' ? r.value : null
  );
```

---

## 5. Stream Processing Best Practices

```
When Streams are essential for large data processing:
  - File size > 100MB
  - Fetching a large number of rows from a DB
  - Batch processing of CSV/JSON
  - Streaming HTTP responses

❌ Loading the entire file into memory:
  const data = fs.readFileSync('large.csv', 'utf8');
  const lines = data.split('\n'); // uses 2x the memory

✅ Process line-by-line with a Stream:
  import { createReadStream } from 'fs';
  import { createInterface } from 'readline';

  const rl = createInterface({
    input: createReadStream('large.csv'),
    crlfDelay: Infinity,
  });

  for await (const line of rl) {
    processLine(line); // processed one line at a time, constant memory
  }

Pipeline pattern (recommended by Node.js):
  import { pipeline } from 'stream/promises';
  await pipeline(
    createReadStream('input.csv'),
    new Transform({ transform(chunk, enc, cb) { /* ... */ } }),
    createWriteStream('output.csv')
  );
```

---

## 6. Integration with Bolt

```
Usage within Bolt:
  1. Screen for BP-01 through BP-08 in the PROFILE phase
  2. Base the SELECT phase on event loop lag measurement results
  3. Apply async patterns and Stream in the OPTIMIZE phase
  4. Perform memory monitoring + load testing in the VERIFY phase

Quality gates:
  - Synchronous I/O usage → require replacement with async API (prevents BP-04)
  - Map/Object cache without maxSize → require conversion to LRU (prevents BP-03)
  - Sequential await execution → suggest parallelization with Promise.all
  - CPU-intensive work without Worker Threads → recommend offloading (prevents BP-01)
```

**Source:** [MarkAICode: Node.js 22 LTS Performance Optimization](https://markaicode.com/nodejs-22-lts-performance-optimization-memory-event-loop/) · [TechDots: Optimizing Node.js Performance](https://www.techdots.dev/blog/optimizing-node-js-performance-memory-management-event-loop-and-async-best-practices) · [DZone: Node.js Performance Tuning](https://dzone.com/articles/nodejs-performance-tuning-advanced-techniques) · [Last9: Monitoring Node.js Key Metrics](https://last9.io/blog/node-js-key-metrics/)
