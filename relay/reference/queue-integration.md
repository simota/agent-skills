# Queue Integration Reference

Purpose: Wire producers and consumers for a message queue (SQS / SNS / RabbitMQ / Kafka / NATS), with explicit DLQ, ack/visibility semantics, fan-out vs fan-in topology, ordering/throughput trade-offs, idempotent consumers, and consumer-group sharing. Output is a queue topology + delivery contract — not the ETL pipeline behind it.

## Scope Boundary

- **Relay `queue`**: producer/consumer wiring, topic/queue topology, DLQ, ack / visibility / redelivery semantics, ordering keys, consumer-group assignment, idempotency key contract. Messaging-first.
- **Stream (elsewhere)**: batch or streaming ETL — Kafka-as-data-pipeline, dbt / Airflow / Flink, schema registry for analytics, late-arriving data handling. When the question is "how do I enrich, join, window, and land this in a warehouse?" → Stream.
- **Gateway (elsewhere)**: REST/GraphQL API design — no async messaging.
- **Tempo (elsewhere)**: retry *schedule / backoff policy / cron* for business jobs. Queue redelivery is transport-level; business-level retry semantics belong to Tempo.
- **Beacon (elsewhere)**: queue-depth dashboards, consumer-lag SLOs, age-of-oldest-message alerts. Relay emits the metric contract; Beacon shapes the alerting.

If the task is "deliver this event reliably to N consumers with retries and DLQ" → `queue`. If it is "compute windowed aggregates from Kafka and land them in Snowflake" → Stream.

## Broker Selection Matrix

| Broker | Model | Ordering | Fan-out | DLQ native | Pick when |
|--------|-------|----------|---------|-----------|-----------|
| **SQS (standard)** | Pull, at-least-once | None | No (pair with SNS) | Yes (redrive) | Simple async work queue on AWS, no ordering need |
| **SQS FIFO** | Pull, exactly-once per group | Per `MessageGroupId` | No | Yes | Ordered per-entity (userId, accountId) at modest TPS |
| **SNS** | Push, pub/sub | None | Fan-out to SQS/Lambda/HTTP | Subscriber-side | Broadcast one event to many consumers |
| **RabbitMQ** | Push, ack-based | Per queue | Exchanges (topic/direct/fanout) | DLX | Complex routing, rich exchange types, on-prem |
| **Kafka / Redpanda** | Pull, log | Per partition | Consumer groups | Manual DLQ topic | High throughput, replay, event-sourcing |
| **NATS JetStream** | Pull or push | Per subject/stream | Yes | Yes | Lightweight, multi-tenant, edge |
| **Redis Streams** | Pull, consumer groups | Per stream | XREADGROUP | Manual (PEL → claim → DLQ stream) | Small-scale, already-Redis infra |

Default for AWS async job: **SQS + DLQ**. Default for event broadcast: **SNS → SQS per subscriber**. Default for high-throughput log: **Kafka**.

## Producer Contract

Every message must carry:

| Field | Why |
|-------|-----|
| `id` (ULID / UUIDv7) | Idempotency key for consumer dedupe |
| `type` + `version` | Consumer routing and schema evolution |
| `occurredAt` | Event time (distinct from enqueue time) |
| `producer` | Trace attribution |
| `traceId` / `spanId` | Distributed tracing correlation |
| `partitionKey` or `messageGroupId` | Ordering guarantee scope |
| `payload` | Domain data |

Recommended envelope: **CloudEvents 1.0** — vendor-neutral, maps cleanly onto SQS attributes, SNS message attributes, Kafka headers, NATS headers. Schema evolves via `type` + `specversion`; add new fields as optional, never reorder.

## Consumer Contract

1. **Fetch** with broker-appropriate primitive (`ReceiveMessage`, `basic.consume`, `poll`, `XREADGROUP`).
2. **Deduplicate** by `id` — check-and-store as the FIRST DB operation before business logic. TTL 7–30 days (longer than max redelivery window).
3. **Process** business logic within the visibility / ack timeout budget.
4. **Ack / commit** only after durable state change committed.
5. **Nack / extend** on transient failure; re-raise on poison-pill to route via redelivery → DLQ.

The single biggest failure mode is committing ack *before* the DB transaction — a crash between ack and commit loses the message.

## Visibility / Ack Model by Broker

| Broker | Primitive | Default | Extension |
|--------|-----------|---------|-----------|
| SQS | `VisibilityTimeout` per message | 30 s (queue default) | `ChangeMessageVisibility` extends |
| SQS FIFO | Same, scoped per `MessageGroupId` | 30 s | Same |
| RabbitMQ | `ack` / `nack` / `reject` | Unacked forever until consumer disconnect | `basic.ack(multiple=true)` batch ack |
| Kafka | Offset commit (auto or manual) | Auto every 5 s (dangerous) | Prefer manual per-batch commit |
| NATS JetStream | `AckWait` on consumer | 30 s | `InProgress` ack extends |
| Redis Streams | `XACK` after processing | PEL holds until ack | `XCLAIM` steals stuck messages |

Rule of thumb: set visibility to **P99 processing time × 2**. Too short → duplicate processing. Too long → slow failure recovery.

## DLQ Strategy

Every queue must have a DLQ. Non-optional.

```
main-queue ──(maxReceiveCount=5)──► dlq
                                     │
                                     ├── operator inspects payload + error context
                                     ├── redrive after fix (SQS redrive API / manual republish)
                                     └── retain ≥ 14 days before purge
```

DLQ message must preserve:
- Original payload (byte-identical).
- All delivery attempts with timestamps and consumer-reported errors.
- Original queue / topic / partition.
- Routing headers (trace IDs, producer metadata).

Kafka has no native DLQ — use a dedicated `<topic>.dlq` topic and require every consumer to publish poison pills there with a context header `x-dlq-reason`.

## Fan-Out vs Fan-In

| Pattern | Shape | Broker idioms |
|---------|-------|---------------|
| **Fan-out** | One event → many consumers | SNS → multiple SQS, Kafka topic → multiple consumer groups, RabbitMQ fanout exchange |
| **Fan-in** | Many producers → one queue | Single SQS with many writers, Kafka topic with many producers, RabbitMQ direct exchange |
| **Scatter-gather** | Fan-out + correlated fan-in | SNS fan-out → worker SQS → reply queue keyed on `correlationId` |

Fan-out rule: each subscriber gets its **own** queue with its **own** DLQ. Do not share a queue across subscribers — one slow consumer backs up the others.

## Ordering vs Throughput Trade-Off

| Requirement | Design |
|-------------|--------|
| Strict global order | Single partition / single queue — caps throughput |
| Order per entity | `partitionKey = entityId` (Kafka), `MessageGroupId = entityId` (SQS FIFO) |
| No order | Maximize partitions / standard queue / multi-consumer parallelism |

Partition / group count = max concurrent consumers. You cannot increase parallelism past partition count in Kafka without re-partitioning. Start with **2× projected peak consumer count** to leave headroom.

## Idempotent Consumer Pattern

```ts
async function handle(msg: Message) {
  const seen = await redis.set(`dedupe:${msg.id}`, "1", "NX", "EX", 60 * 60 * 24 * 14);
  if (seen === null) return ack(msg); // already processed
  await tx(async () => {
    await businessLogic(msg.payload);
    await markProcessed(msg.id); // same transaction as business state
  });
  ack(msg);
}
```

Two layers of dedupe: fast Redis check (cheap, 14-day window) + transactional DB marker (authoritative, permanent). Redis misses fall through to DB constraint violation.

## Consumer-Group Semantics

| Broker | "Group" equivalent | Rebalance cost |
|--------|-------------------|----------------|
| Kafka | `group.id` — partitions divided across members | Stop-the-world on join/leave; use cooperative sticky assignor |
| SQS | N workers pulling same queue | None — queue-level pull model |
| NATS JetStream | Durable pull consumer | None |
| RabbitMQ | Competing consumers on same queue | None |
| Redis Streams | `XGROUP CREATE` + `XREADGROUP` | None |

Kafka consumer-group rebalances are the #1 operational hazard — configure `session.timeout.ms`, `max.poll.interval.ms`, and prefer cooperative-sticky rebalancing to avoid stop-the-world pauses.

## Anti-Patterns

- Shipping a queue without a DLQ — poison pills silently re-consume forever until you are paged at 3 AM.
- Acking / committing offset *before* the DB transaction commits — crash loses the message.
- Sharing one queue across multiple unrelated consumers to "save money" — one slow consumer stalls the rest; use fan-out with per-subscriber queues.
- Setting visibility timeout equal to average processing time — P99 outliers cause duplicate processing on every spike.
- Treating Kafka as a request/response system — the log model is append-only; use request-reply brokers (NATS, RabbitMQ direct-reply-to) instead.
- Relying on SQS Standard for ordering — it is best-effort, not guaranteed. Use FIFO or embed sequence numbers.
- Omitting an idempotency key because "the broker says exactly-once" — every exactly-once claim has boundaries; always dedupe at the consumer.
- Increasing Kafka partitions in production without a plan — you cannot decrease them, and per-key ordering breaks across the split.
- Publishing to DLQ without context — operators need the error, attempt count, and routing headers to redrive safely.

## Handoff / Next Steps

**To Builder** (RELAY_TO_BUILDER):
- Broker choice + rationale, envelope schema (CloudEvents or custom), partition / group key strategy, visibility timeout values, DLQ wiring, idempotency-key storage layer.

**To Scaffold** (RELAY_TO_SCAFFOLD):
- IaC for queues / topics / DLQs, access policies (least privilege, separate producer vs consumer roles), VPC endpoints where relevant, partition count and retention.

**To Stream** (when pipeline scope emerges):
- Handoff if the consumer turns into a windowed / joined / enriched pipeline — that is Stream's responsibility, not Relay's.

**To Tempo** (when retry policy requires scheduling):
- Hand off business-level retry schedules (e.g. "retry failed payout after 24h") — Tempo owns scheduled-retry design; `queue` owns transport-level redelivery.

**To Beacon** (RELAY_TO_BEACON):
- Metrics: queue depth, age of oldest message, consumer lag (Kafka `consumer_lag`), DLQ message count, redelivery rate, processing duration histogram. SLO targets: DLQ rate < 0.1%, oldest-message age < 5 min at P95.
