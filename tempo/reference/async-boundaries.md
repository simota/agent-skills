# Async Boundary Time Contracts: Deadlines & Time Windows

Purpose: Two distinct but related time contracts that travel across async boundaries — **deadlines** (how long a single request has left to finish) and **time windows** (which events belong together over event-time). Both fail silently when implicit; both must be designed explicitly per hop.

When to use which:
- A request crosses two or more service hops and you need an end-to-end time budget → **Deadline Propagation**.
- Events are aggregated over time (rollups, joins, moving averages, sessions) → **Time Window Semantics**.
- A request triggers a windowed aggregation downstream → both apply (deadline bounds the request; window bounds the aggregation).

---

## § Deadline Propagation

Design a coherent deadline that travels with a request across process, network, and service boundaries so every downstream call inherits the remaining budget. Deadlines turn an unbounded retry storm into a bounded, predictable failure, and they let partial-progress return beat a full timeout hang. Read this when a request crosses two or more hops and no single component owns the end-to-end time budget.

### Scope Boundary

- **Tempo `deadline`**: end-to-end time-budget chain, context deadline propagation semantics, partial-progress-on-deadline policy, deadline-exceeded observability contract, cascading-timeout math.
- **Stream (elsewhere)**: pipeline and DAG implementation — deadline is one input Stream consumes; pipeline wiring, batching, and backpressure live there.
- **Gateway (elsewhere)**: HTTP/RPC layer timeout configuration (server read/write, client idle, keep-alive). Gateway owns the wire timeout; Tempo owns the logical deadline that must be shorter than it.
- **Beacon (elsewhere)**: SLO definition and time-budget monitoring (p99 latency, deadline-exceeded rate, error-budget burn). Tempo hands Beacon the target; Beacon alerts.

If the question is "what is the deadline budget and how is it split?" → `deadline`. If it is "how do I wire this through a Kafka/Airflow DAG?" → Stream. If it is "how do I configure nginx/envoy timeouts?" → Gateway. If it is "what alert fires when deadlines are exceeded?" → Beacon.

### Deadline vs Timeout

| Concept | Definition | Propagates? | Example |
|---------|-----------|-------------|---------|
| Timeout | Duration relative to NOW (`5s from here`) | No — resets at each hop | `fetch(url, { signal: AbortSignal.timeout(5000) })` |
| Deadline | Absolute instant (`finish by 10:00:03.200Z`) | Yes — encoded as a wall-clock or monotonic instant | Go `context.WithDeadline`, gRPC `grpc-timeout` header |

Deadlines are strictly more correct for multi-hop requests. Prefer deadlines; derive per-hop timeouts from the remaining deadline budget.

### Budget Chain Math

The budget chain rule: every hop spends some of the budget; downstream hops receive `deadline - (time_spent_upstream + network_margin)`.

```
Client budget   = 3000ms  ┐
                          │ network 50ms + queue 10ms
Gateway receives = 2940ms ┐
                          │ own work 80ms + network 30ms
Service A receives = 2830ms ┐
                          │ own work 200ms + DB call 150ms + fanout margin 50ms
Service B receives = 2430ms
```

Rule of thumb: reserve at least `RTT + 50ms` margin at each hop so the downstream sees a deadline it can actually meet, and so cancellation travels back up before the client gives up.

### Language / Runtime Patterns

#### Go — `context.Context`

```go
ctx, cancel := context.WithDeadline(parent, deadline)
defer cancel()

if dl, ok := ctx.Deadline(); ok {
    remaining := time.Until(dl)
    if remaining < 100*time.Millisecond {
        return nil, fmt.Errorf("insufficient budget: %v", remaining)
    }
}

resp, err := client.Do(ctx, req) // ctx carries deadline down
```

#### TypeScript / JS — `AbortSignal` with deadline

```ts
const deadline = Date.now() + 3000;
const signal = AbortSignal.timeout(deadline - Date.now());

async function hop(path: string, deadlineMs: number) {
  const remaining = deadlineMs - Date.now();
  if (remaining <= 50) throw new Error('deadline-exceeded');
  return fetch(path, { signal: AbortSignal.timeout(remaining - 20) });
}
```

Propagate the deadline as a header (`x-deadline-ms` or `grpc-timeout`), not as a relative timeout.

#### gRPC — `grpc-timeout` header

Every gRPC call carries `grpc-timeout: <value><unit>` (e.g., `200m` for 200ms). The server computes the effective deadline and passes it into its own outbound calls. Do not add app-level timeouts on top — use `ctx.Deadline()` directly.

#### Python — `asyncio.timeout` + context var

```python
deadline = loop.time() + 3.0
async with asyncio.timeout_at(deadline):
    result = await downstream(deadline=deadline)
```

Carry `deadline` as a function parameter (or a `contextvars.ContextVar`) across async boundaries.

### Partial Progress on Deadline

When the deadline fires mid-fanout, returning "everything or nothing" wastes the work done so far. Patterns:

| Pattern | When to use | Trade-off |
|---------|-------------|-----------|
| Best-effort batch | Fanout query (search, scatter-gather) | Return completed shards + mark missing with `partial=true` |
| Checkpoint + resume | Long-running job (ETL, backfill) | Persist watermark; resume from `watermark + 1` on next run |
| Degraded response | Enrichment layer (recommendations, ranking) | Return base result without the enrichment; flag `degraded=true` |
| Hard fail | Strict consistency (payment, booking) | Return deadline-exceeded; never partial-commit |

Document which pattern applies per endpoint. Silent partial returns are the worst outcome.

### Observability Contract

Every deadline-aware path emits:

- `deadline_ms_received` — budget at ingress
- `deadline_ms_remaining_on_exit` — budget handed to next hop
- `deadline_exceeded_total{hop,reason}` — counter
- `budget_consumed_ratio` — histogram of `1 - (remaining / received)`; helps find hops that eat too much

Hand these targets to Beacon at design time.

### Anti-Patterns

- Propagating a relative timeout (`timeout=3s`) across hops — each hop restarts the clock; total budget balloons.
- Setting per-hop timeouts greater than the inherited deadline — the deadline wins; the longer timeout is dead code and misleads readers.
- No margin between logical deadline and wire timeout — wire times out first, client sees a network error instead of a clean deadline-exceeded signal.
- Swallowing `context.Canceled` / `AbortError` as a generic error — loses the signal that the upstream already gave up.
- Retrying after deadline-exceeded — the caller is gone; retry is guaranteed waste.
- Cascading timeout trap: caller 2s, service 2s, DB 2s — any slow hop blows the whole chain; each inner hop must be strictly shorter than the inherited deadline.
- Hard-coded sleeps / fixed delays inside a deadline-bounded path — breaks the budget contract.
- Missing deadline on fanout — slowest shard drags the whole response; always apply `min(deadline, per_shard_budget)` per shard.

### Handoff

**To Builder:** deliver the budget chain table (per-hop allocation + margin), the propagation mechanism (context / header / signal), the partial-progress policy per endpoint, and the cancel-signal propagation path.

**To Gateway:** deliver the wire-timeout upper bound (must be ≥ logical deadline + margin) and the header name used to carry the deadline downstream.

**To Beacon:** deliver `deadline_exceeded_total`, `budget_consumed_ratio`, and the SLO target (e.g., `p99 remaining_on_exit > 200ms`) for alerting.

**To Voyager:** deliver test scenarios — deadline exactly at boundary, deadline already exceeded at entry, cancel mid-flight, partial fanout completion.

---

## § Time Window Semantics

Define the time-window math that analytics and streaming workloads need — the shape of the window (tumbling / sliding / session), where the watermark sits, what counts as "late", and how two windowed streams join. A window specification is a contract: given input event-times, the system MUST emit one answer per window, and MUST be deterministic about which events belong to which window. Read this when aggregating events over time or building a windowed join.

### Scope Boundary

- **Tempo `window`**: window shape + watermark strategy + allowed-lateness + late-arrival policy + window-join semantics. Pure time math, platform-neutral.
- **Stream (elsewhere)**: pipeline implementation — Flink/Beam/Kafka Streams/Spark Structured Streaming wiring, operators, state backends, checkpointing. Stream consumes Tempo's window spec.
- **Gateway (elsewhere)**: request/response HTTP concerns — unrelated to event-time windowing.
- **Beacon (elsewhere)**: watermark-lag SLO, late-event rate dashboard, window-emission freshness alerts. Tempo hands the targets; Beacon observes.

If the question is "which events belong to which window, and when does the window close?" → `window`. If it is "how do I configure the Flink watermark strategy API?" → Stream. If it is "what alert fires when watermark lag exceeds 5 minutes?" → Beacon.

### Window Shapes

| Shape | Definition | Emits per | Use for |
|-------|-----------|-----------|---------|
| Tumbling | Fixed, non-overlapping, contiguous intervals of size `S` | Window | Hourly/daily aggregates, periodic rollups |
| Sliding | Fixed size `S`, advances by step `P` (where `P < S`); windows overlap | Slide step | Moving averages, N-minute rolling counts |
| Session | Dynamic; opens on event, closes after `gap` of inactivity | Session | User sessions, device bursts, conversation turns |
| Global + trigger | One unbounded window; custom trigger fires emission | Trigger | Custom aggregations with bespoke firing logic |

```
Tumbling (S=5m):
[00:00-00:05)[00:05-00:10)[00:10-00:15) ...

Sliding (S=5m, P=1m):
[00:00-00:05)
  [00:01-00:06)
    [00:02-00:07) ...

Session (gap=30m):
e1--e2---e3-------------e4---e5
└─── session A ─┘       └session B┘
      (gap < 30m)       (gap > 30m)
```

Event-time vs processing-time: always prefer **event-time** for windows. Processing-time windows look simple but silently mis-bucket under backpressure, replay, or clock skew.

### Watermark Design

A watermark is a monotonic marker asserting "no event older than T will arrive." It drives when a window is safe to close.

| Strategy | Definition | Trade-off |
|---------|-----------|-----------|
| Perfect | Watermark = max(event_time) seen, minus 0 | Lowest latency, wrong if any event is late |
| Bounded-out-of-orderness | max(event_time) - `maxDelay` | Common default; pick `maxDelay` from observed p99 lateness |
| Punctuated | Emit watermark on explicit marker events | Accurate when source emits completion markers (end-of-partition) |
| Periodic | Emit watermark on a wall-clock tick | Simple; tune emit interval (typically 200ms - 1s) |
| Idle-source fallback | Advance watermark on idle partition after `idleTimeout` | Prevents stuck pipelines when one partition has no traffic |

Rule: set `maxDelay` from a measured lateness distribution, not a guess. If p99 observed lateness is 2m, a 30s bound drops 1%+ of events silently.

### Allowed Lateness & Late-Arrival Handling

After the watermark closes a window, events can still arrive (clock skew, mobile buffering, upstream outage recovery). Policy options:

| Policy | Behavior | Cost |
|--------|----------|------|
| Drop | Discard events arriving after window close | Cheapest; data loss |
| Side output | Route late events to a dedicated "late" stream/topic | Preserves data; downstream must re-ingest |
| Allowed lateness + re-fire | Keep window state for `allowedLateness`; re-emit updated result on late event | Correct; state cost |
| Retraction | Emit negative delta to revise the prior window answer | Consumer must handle retractions |

Pick one policy per window and document it. Default for analytics dashboards: `allowedLateness = maxDelay × 2` with re-fire semantics.

### Window Join

Two streams can be joined within a window. The join semantics depend on the window shape:

```ts
// Stream A ⨝ Stream B on key within ±2m
streamA
  .keyBy(e => e.userId)
  .intervalJoin(streamB.keyBy(e => e.userId))
  .between(Time.minutes(-2), Time.minutes(2))
  .process((a, b, ctx, out) => out.collect({ a, b }));
```

| Join type | Semantics |
|-----------|-----------|
| Tumbling window join | Pair events falling in the SAME tumbling window |
| Sliding window join | Pair events falling in at least one shared sliding window |
| Interval join | Pair event A with B if `A.time + lowerBound ≤ B.time ≤ A.time + upperBound` |
| Session window join | Pair events belonging to the SAME session (per key) |

Key hazard: asymmetric lateness between A and B. If A is 30s late and B is on time, the window must wait for A's watermark, not just B's — watermark in a join = min(upstream watermarks).

### Language Sketches

#### Python (pure, no framework)

```python
from collections import defaultdict

def tumbling(events, size_s: int):
    buckets = defaultdict(list)
    for e in events:
        key = (e.event_time // size_s) * size_s
        buckets[key].append(e)
    return buckets

def session(events, gap_s: int):
    events = sorted(events, key=lambda e: e.event_time)
    sessions, current, last_t = [], [], None
    for e in events:
        if last_t is None or e.event_time - last_t <= gap_s:
            current.append(e)
        else:
            sessions.append(current); current = [e]
        last_t = e.event_time
    if current: sessions.append(current)
    return sessions
```

#### TypeScript (sliding window count)

```ts
function slidingCount(events: Event[], sizeMs: number, stepMs: number) {
  const out: { start: number; end: number; count: number }[] = [];
  const minT = Math.min(...events.map(e => e.t));
  const maxT = Math.max(...events.map(e => e.t));
  for (let s = minT; s < maxT; s += stepMs) {
    const e = s + sizeMs;
    const count = events.filter(x => x.t >= s && x.t < e).length;
    out.push({ start: s, end: e, count });
  }
  return out;
}
```

### Anti-Patterns

- Mixing processing-time and event-time windows in the same pipeline — results become non-reproducible.
- Using wall-clock `NOW` as the watermark — any backpressure corrupts every window.
- `allowedLateness = 0` with `drop` policy, then surprise at "missing" data — it was silently discarded.
- Tumbling windows aligned to epoch 0 in a specific timezone without stating which — the first window of the day shifts by DST.
- Session gap shorter than p99 inter-event time — splits real sessions into fragments.
- Sliding windows with step much smaller than size (`S=1h, P=1s`) — emits 3600× more output than intended; explodes downstream state.
- Window join without ensuring matching key partitioning on both streams — runs, produces empty results, no error.
- Trusting the wall clock of the producer — device clocks drift; for mobile events, bound `maxDelay` by observed skew (often multi-minute).

### Handoff

**To Stream:** deliver the window shape (tumbling/sliding/session with parameters), the watermark strategy, `maxDelay`, `allowedLateness`, late-event policy, and join semantics. Stream chooses the framework operator and state backend.

**To Beacon:** deliver watermark-lag SLO (e.g., `p99 < 30s`), late-event rate budget, and window-emission freshness alert (`no emission > 2 × size`).

**To Voyager:** deliver test scenarios — exact-boundary events, p99-late events, out-of-order bursts, idle-partition watermark advance, and window-join with asymmetric lateness.

**To Builder:** deliver the window-output contract (schema of emitted rows, retraction policy if any, key type, timestamp field) so the downstream consumer handles it correctly.

---

## § Interactions Between Deadlines and Windows

The two contracts intersect when a request triggers (or queries) a windowed aggregation:

- **Deadline bounds the request; window bounds the result freshness.** A 3s deadline cannot wait for a window whose watermark is 5s behind. Either accept a partial answer (last closed window) or fail fast with deadline-exceeded — never silently return stale data without flagging.
- **Watermark lag eats into deadline budget.** Downstream watermarks may be minutes behind under backpressure. Document an explicit "freshness floor" alongside the deadline: "return windows closed within the last `maxDelay + margin`; deadline-exceed otherwise."
- **Late-arrival policy must align with retry policy.** If the upstream retries after deadline-exceeded, a `retraction` window policy will emit a revised answer for the original window — the retrying caller may double-count. Pair retracting windows with caller-side idempotency.
- **Fanout deadlines vs window-join watermarks.** A scatter-gather across two windowed sources uses `min(watermark_A, watermark_B)` for join correctness, but the deadline still ticks against wall-clock — the slower source can starve the join past the deadline. Document the partial-join policy: "emit pairs from the faster side only, flag `partial=true`."

Default stance: deadline owns wall-clock fail-safety; window owns event-time correctness. Surface both numbers in every response that touches both contracts (`served_at`, `window_close_time`, `deadline_remaining_ms`).
