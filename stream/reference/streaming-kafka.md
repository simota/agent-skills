# Streaming Architecture — Kafka Design

Purpose: topic, consumer, schema, and delivery guidance for event-driven and Kafka-based pipelines.

## Contents

1. Topic design
2. Consumer-group rules
3. Event schema
4. Delivery guarantees
5. Outbox and processing patterns

## Topic Design

```yaml
topic_naming_convention:
  pattern: "{domain}.{entity}.{event}"
  examples:
    - "orders.order.created"
    - "users.profile.updated"
    - "payments.transaction.completed"
```

### Topic Configuration Rules

| Setting | Rule |
|---------|------|
| Partitions | `10x` expected peak throughput in MB/s |
| Minimum partitions | `3` |
| Practical maximum | `100` per topic |
| Production retention | `7d` by default, extend for replay needs |
| Compacted retention | effectively infinite for state topics |
| Replication factor | prod `3`, staging `2`, dev `1` |

Anti-pattern guards:
- do not create a god topic
- do not use `1` partition for scalable workloads
- do not jump to `1000` partitions without a hard need

## Consumer Group Rules

```yaml
consumer_groups:
  naming: "{service}-{purpose}"
  examples:
    - "analytics-aggregator"
    - "notification-sender"
    - "audit-logger"
```

Rules:
- `consumers <= partitions`
- scale off consumer lag, not guesswork
- separate groups by purpose, not convenience

## Event Schema

Required metadata:
- `event_id`
- `event_type`
- `timestamp`
- `version`
- `source`
- `correlation_id`
- `data`

Compatibility rules:
- allow additive fields
- do not remove fields or change types without versioning
- use Schema Registry for shared or critical streams

Recommended event size: `1KB-10KB`. If payloads grow beyond that, prefer reference patterns.

## Delivery Guarantees

| Level | Use When | Notes |
|-------|----------|-------|
| At-most-once | loss is acceptable | avoid for business-critical data |
| At-least-once | default | combine with idempotent consumers |
| Exactly-once | narrow Kafka-to-Kafka cases | external systems still need idempotent sinks |

Prefer "effectively once": `acks=all` + manual commit after processing + idempotent sink or deduplication.

## Outbox And Processing Patterns

Use Outbox when DB writes and event publication must remain atomic:
1. write business data and outbox record in one DB transaction
2. capture outbox changes with CDC
3. publish to Kafka from the CDC pipeline

Common processing shapes:
- stateless transform
- windowed aggregation
- stream-table join

Operational guards:
- use manual commit after successful processing
- send poison pills to a DLT/DLQ
- track consumer lag, throughput, error rate, rebalance frequency, disk usage, and under-replicated partitions

## 2025-2026 Platform Baseline

- **Kafka 4.0 (GA: 2025-03-18)** ships ZooKeeper mode fully removed — KRaft is the only supported mode. Clusters on ZooKeeper must migrate to KRaft before upgrading to 4.0+. Kafka 4.1 (GA: 2025-09-04) followed with further stability improvements. Source: [kafka.apache.org/blog](https://kafka.apache.org/blog/2025/03/18/apache-kafka-4.0.0-release-announcement/)
- **KIP-848 (new consumer group protocol)** is GA in Kafka 4.0. The server-driven incremental rebalance protocol (opt-in via `group.protocol=consumer`) removes the global synchronization barrier, dramatically reducing rebalance time in large consumer groups. Source: [kafka.apache.org — Consumer Rebalance Protocol](https://kafka.apache.org/41/operations/consumer-rebalance-protocol/)
- **KIP-932 — Queues for Kafka** is in preview (Kafka 4.0+). Share groups enable point-to-point queue semantics on standard Kafka topics. **Not yet production-ready**; evaluate for development workloads only.
- **Tiered Storage** is production-ready (Kafka 3.9+, reinforced in 4.x): hot, recent log segments stay on broker-local disk; closed segments offload to S3 / GCS / Azure Blob via the broker's `RemoteStorageManager`. Extend retention to weeks/months on cold storage without matching broker disk; treat broker disk as a working-set cache.
- **Iceberg Topics / Kafka-Iceberg integration**: surface a Kafka topic as an **Apache Iceberg** table on object storage with zero-ETL and zero-copy semantics (Aiven Iceberg Topics, AutoMQ, WarpStream Iceberg-native flows). Caveat: only **closed segments** are exposed to Iceberg consumers, so this is **not** sub-second real-time — for sub-second joins, keep a Flink / Kafka Streams consumer next to the broker.
- **Flink as the real-time processor** is the 2026 default when the workload is more than stateless transforms. Flink 2.1 Model DDL / `ML_PREDICT` enables in-stream model inference without external ML services. Kafka Streams remains appropriate for JVM-only, tightly-coupled topologies.

### When To Reach For Each Storage Tier

| Need | 2026 default |
|------|---------------|
| Replay last `7 d` for incident recovery | Broker-local retention; standard Kafka |
| Replay last `90 d+` for backfills | Tiered Storage with closed-segment offload to S3 / GCS / Azure Blob |
| Run Spark / Trino / Flink batch on the same data without re-publishing | Iceberg Topics on object storage |
| Sub-second stream-stream join over hours of state | Flink with RocksDB state backend (or Kafka Streams equivalent) — not Iceberg |
