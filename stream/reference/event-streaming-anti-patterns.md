# Event Streaming Anti-Patterns

Purpose: anti-pattern IDs `ES-01..07`, event-modeling rules, Kafka operational guardrails, and outbox guidance.

## Contents

1. Core anti-patterns
2. Event modeling rules
3. Kafka operational guardrails
4. Delivery guarantees
5. Outbox pattern

## Core Anti-Patterns

| ID | Anti-Pattern | Risk | Required Response |
|----|--------------|------|-------------------|
| `ES-01` | God Topic | no domain separation, poor scaling | split by `{domain}.{entity}.{event}` |
| `ES-02` | Schema Anarchy | consumer breakage, no compatibility rules | use schema registry and versioning |
| `ES-03` | Consumer Coupling | producer changes for every consumer | design domain events, let consumers project |
| `ES-04` | Fire and Forget | message loss and inconsistency | `acks=all`, `min.insync.replicas=2`, producer idempotence |
| `ES-05` | Offset Mismanagement | loss or duplication on failure | manual commit after processing |
| `ES-06` | Partition Key Blindness | hot partitions or broken ordering | choose business-key partitioning |
| `ES-07` | Event Soup | command/event confusion and replay pain | use past-tense domain events |

## Event Modeling Rules

- prefer domain events such as `OrderPlaced`, not commands such as `CreateOrder`
- include enough data for consumers to stay mostly self-contained
- keep metadata explicit: `event_id`, `timestamp`, `source`, `correlation_id`, `version`
- preserve backward compatibility when evolving schemas
- target event sizes around `1KB-10KB`

## Kafka Operational Guardrails

| Area | Guardrail |
|------|-----------|
| Partitions | start at `>=3`, stay cautious beyond `100`, scale with throughput needs |
| Retention | default `7d`; longer for replay-heavy systems |
| Consumers | `consumers <= partitions` |
| Error handling | bounded retries + DLT/DLQ for poison pills |
| Monitoring | lag, throughput, error rate, rebalance frequency, disk usage, under-replicated partitions |

## Delivery Guarantees

- `At-most-once`: only for loss-tolerant telemetry
- `At-least-once`: default for most systems
- `Exactly-once`: narrow Kafka-to-Kafka cases only

Prefer "effectively once": `at-least-once` delivery + idempotent processing.

## Outbox Pattern

Use when DB state change and event publication must be atomic:
1. write business data and outbox row in one transaction
2. read the outbox with CDC
3. publish the resulting event stream
