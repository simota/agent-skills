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
## Additional Detection Signals
- **Common Leak Patterns**
- **Memory Monitoring**
---
## 6. Integration with Bolt
**Source:** [MarkAICode: Node.js 22 LTS Performance Optimization](https://markaicode.com/nodejs-22-lts-performance-optimization-memory-event-loop/) · [TechDots: Optimizing Node.js Performance](https://www.techdots.dev/blog/optimizing-node-js-performance-memory-management-event-loop-and-async-best-practices) · [DZone: Node.js Performance Tuning](https://dzone.com/articles/nodejs-performance-tuning-advanced-techniques) · [Last9: Monitoring Node.js Key Metrics](https://last9.io/blog/node-js-key-metrics/)
