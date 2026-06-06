# Event Sourcing Schema Reference

Purpose: Design event-store schemas where events are the system of record. Covers event table structure, aggregate boundaries, optimistic concurrency, projections (read models), snapshots, and the transactional outbox pattern. Distinct from audit logs — events drive state, not just record it.

## Scope Boundary

- **schema `event-sourcing`**: Event store schema design (this document).
- **schema `audit-log` (elsewhere)**: Side-record of mutations; not system of record.
- **weave `compensation` (elsewhere)**: Saga / compensation patterns for distributed transactions.
- **stream (elsewhere)**: Streaming pipelines that consume / project events.
- **gateway (elsewhere)**: API surface; events are not REST resources.
- **shard (elsewhere)**: Multi-tenant partitioning of event streams.

## Event Sourcing Recap

State is derived by replaying events. The event log is the single source of truth.

```
COMMAND  →  Aggregate.handle(cmd)  →  emit Event(s)  →  Append to event store
                                                   →  Update projections (read model)
                                                   →  Publish via outbox
```

Read models are denormalized projections rebuilt by replaying events.

## When to Use Event Sourcing

| Use | Strong fit | Weak fit |
|-----|-----------|----------|
| Audit / regulatory | ✓ history is required by law | — |
| Temporal queries | ✓ "as of" required | — |
| Complex domain | ✓ DDD aggregate-rich | — |
| CRUD admin app | — | use plain SQL |
| Analytics pipeline | — | use warehouse |
| High-write throughput across non-related entities | — | overhead doesn't pay off |

Default to traditional schemas; reach for event sourcing when audit / temporal / complex-domain forces it.

## Core Event Store Schema (Postgres)

```sql
CREATE TABLE events (
  event_id         UUID         PRIMARY KEY,        -- v7 time-sortable
  aggregate_type   TEXT         NOT NULL,           -- e.g. 'order'
  aggregate_id     TEXT         NOT NULL,           -- e.g. 'order_42'
  aggregate_version BIGINT      NOT NULL,           -- monotonic per aggregate, starts at 1
  event_type       TEXT         NOT NULL,           -- e.g. 'OrderPlaced'
  event_version    INT          NOT NULL DEFAULT 1, -- schema version for event_type
  occurred_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
  recorded_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
  payload          JSONB        NOT NULL,           -- domain payload
  metadata         JSONB        NOT NULL,           -- correlation_id, causation_id, actor, ...
  CONSTRAINT uq_aggregate_version UNIQUE (aggregate_type, aggregate_id, aggregate_version)
);

CREATE INDEX ix_events_aggregate ON events (aggregate_type, aggregate_id, aggregate_version);
CREATE INDEX ix_events_type      ON events (event_type, occurred_at DESC);
CREATE INDEX ix_events_recorded  ON events (recorded_at);  -- for projection cursors
```

Constraints:
- `(aggregate_type, aggregate_id, aggregate_version)` UNIQUE → optimistic concurrency.
- Append-only: `REVOKE UPDATE, DELETE`.
- `event_version` lets you evolve event_type schema without break.

## Optimistic Concurrency

```sql
INSERT INTO events (event_id, aggregate_type, aggregate_id, aggregate_version, event_type, payload, metadata)
VALUES ($1, 'order', 'order_42', $expected_version + 1, 'OrderPlaced', $payload, $metadata);
```

If another writer raced, UNIQUE violates → command retries with fresh version.

## Snapshots

Replaying 100k events per aggregate is expensive. Snapshots are periodic state captures.

```sql
CREATE TABLE snapshots (
  aggregate_type   TEXT NOT NULL,
  aggregate_id     TEXT NOT NULL,
  aggregate_version BIGINT NOT NULL,
  taken_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  state            JSONB NOT NULL,
  PRIMARY KEY (aggregate_type, aggregate_id, aggregate_version)
);
```

Loading aggregate:
1. Find latest snapshot ≤ target version.
2. Replay events from snapshot.aggregate_version + 1.

Snapshot cadence: every N events (e.g. 100) or every N days, depending on aggregate volatility.

## Projections (Read Models)

Projections are denormalized tables built by replaying events.

```sql
CREATE TABLE order_summary (
  order_id      TEXT PRIMARY KEY,
  customer_id   TEXT NOT NULL,
  status        TEXT NOT NULL,
  total_amount  NUMERIC NOT NULL,
  placed_at     TIMESTAMPTZ NOT NULL,
  shipped_at    TIMESTAMPTZ,
  -- ...
  last_event_id UUID NOT NULL,
  last_processed_recorded_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE projection_cursor (
  projection_name TEXT PRIMARY KEY,
  last_event_id   UUID NOT NULL,
  last_recorded_at TIMESTAMPTZ NOT NULL
);
```

Each projection has its own cursor. Multiple projections from same event log = different read shapes for different queries.

## Transactional Outbox

Publishing events to a message bus while writing to event store needs to be atomic.

```sql
CREATE TABLE outbox (
  outbox_id     UUID PRIMARY KEY,
  event_id      UUID NOT NULL REFERENCES events(event_id),
  topic         TEXT NOT NULL,
  payload       JSONB NOT NULL,
  status        TEXT NOT NULL DEFAULT 'pending',  -- pending / sent / failed
  attempts      INT NOT NULL DEFAULT 0,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  sent_at       TIMESTAMPTZ
);

CREATE INDEX ix_outbox_status ON outbox (status, created_at) WHERE status = 'pending';
```

Workflow:
1. In one transaction: INSERT events + INSERT outbox.
2. Outbox poller (or CDC via Debezium) reads pending → publishes to bus → marks sent.
3. Idempotent consumers handle re-publish.

Alternative: pure CDC from events table (no outbox) — simpler if Debezium is in place.

## Aggregate Boundaries

| Sign | Action |
|------|--------|
| Two entities always change together transactionally | Same aggregate |
| One entity references but doesn't constrain another | Different aggregates |
| Concurrency contention dominates | Smaller aggregates |
| Cross-aggregate consistency required | Saga (weave `compensation`) |

DDD principle: aggregates enforce invariants; everything inside loads/saves together.

## Schema Evolution

Event payloads will evolve. Two options:

1. **Versioned events**: `event_version` field; consumers handle v1, v2, etc.
2. **Upcasting**: at read time, transform old shape → new shape.

Never edit historical events — evolve forward.

## Workflow

```
DOMAIN-MODEL  →  identify aggregates and events
              →  define event types per aggregate (≥ 1, often 5-15)
              →  list invariants per aggregate

EVENT-STORE   →  events table with UNIQUE (aggregate, version)
              →  append-only privileges
              →  partitioning by occurred_at if high volume

CONCURRENCY   →  optimistic via aggregate_version
              →  retry policy on UNIQUE violation

SNAPSHOTS     →  decide cadence per aggregate
              →  snapshot table

PROJECTIONS   →  one read model per query shape
              →  per-projection cursor
              →  rebuild capability

OUTBOX        →  outbox table
              →  CDC vs poller decision
              →  idempotent consumers

EVOLUTION     →  event_version + upcaster discipline
              →  never edit history

OPS           →  compaction NEVER (events are immutable)
              →  archival to cold storage by partition

HANDOFF       →  weave: saga / compensation patterns
              →  stream: projection pipelines via Kafka
              →  gateway: command APIs (NOT event REST)
              →  shard: tenant partitioning
              →  builder: aggregate implementation
```

## Output Template

```markdown
## Event Sourcing Schema: [Bounded Context]

### Aggregates & Events
| Aggregate | Events | Invariants |
|-----------|--------|------------|
| Order | OrderPlaced, OrderPaid, OrderShipped, OrderCancelled | total ≥ 0, status FSM |
| ... | ... | ... |

### Event Store DDL
[events + uniq + indexes + privileges]

### Optimistic Concurrency Pattern
[INSERT with expected_version + 1]

### Snapshots
- Cadence: [every N events / every D days]
- Snapshot DDL

### Projections
| Projection | Read shape | Source events | Cursor |
|-----------|------------|---------------|--------|
| order_summary | per-order denorm | Order* | order_summary_cursor |

### Outbox
- Pattern: [transactional outbox poller / CDC pure]
- DDL

### Schema Evolution Strategy
- event_version on every event_type
- Upcasting: [yes/no, where]

### Operational
- Append-only privileges: REVOKE UPDATE, DELETE
- Archive: [partition by month, cold after N years]
- Backup: [WAL + base; events MUST be recoverable]

### Handoffs
- weave: saga design (cross-aggregate)
- stream: projection pipelines
- gateway: command API design
- shard: tenant strategy
- builder: aggregate impl
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| UPDATE on events table | Append-only; correct via compensating event |
| No optimistic concurrency | Lost updates / inconsistent state |
| Aggregate spans many entities | Tighten boundary; use saga for cross |
| One projection for all queries | Project per query shape |
| Synchronous projection in command path | Async via outbox; commands stay fast |
| Edit historical events for "fix" | Use upcaster + event_version |
| No snapshots on long-lived aggregates | Replay cost grows linearly |
| Outbox without idempotent consumers | Duplicates on retry |
| Mixing CRUD tables with event store | Choose one paradigm per bounded context |
| Unbounded event growth | Archive partitions; cold storage |
| Projection cursor not transactional | Risk of double-projection |
| Event payload too coarse (whole entity dump) | Capture intent + delta |

## Deliverable Contract

When `event-sourcing` completes, emit:

- **Aggregates + events** mapped with invariants.
- **Event store DDL** (uniq, indexes, append-only).
- **Optimistic concurrency pattern**.
- **Snapshot strategy** with cadence.
- **Projections** per read shape with cursors.
- **Outbox** pattern (or CDC choice).
- **Schema evolution** plan (event_version + upcasters).
- **Operational** rules (privileges, archive, backup).
- **Handoffs**: weave, stream, gateway, shard, builder.

## Dedicated Event Stores (2026-05 landscape)

When a Postgres `events` table outgrows OLTP — typically > 100 M events/aggregate-type or > 50 K events/s sustained — consider a purpose-built event store. Schema design implications differ from the Postgres recipe above.

| Engine | Status (2026-05) | Schema model | Notes |
|--------|------------------|--------------|-------|
| **KurrentDB** (formerly EventStoreDB) | Rebranded Dec 2024 alongside Event Store → Kurrent (+ $12 M raise). Current major: KurrentDB 26 (late-2024 / 2025) | Streams (one per aggregate) with global position; gRPC client | KurrentDB 26 added native Kafka source connector and a Relational Sink (auto-projects to Postgres / SQL Server) — narrows the projection-layer custom code. |
| **Marten** (.NET on Postgres) | v7 GA early-2024; v8 active in 2026 | Postgres `mt_events` table + projection tables; uses PG 12+ SQL/JSON | v7: renamed `aggregation` → `projection`, `SelfAggregate` → `Snapshot` + `LiveStreamAggregation`. Built-in Polly resiliency replaces `IRetryPolicy`. Document-by-identity tracking in async projections. Continues to be the canonical "event store on Postgres" for .NET. |
| **Axon Server** | 2026.x | JPA-style aggregate stream | Java-only; tight Spring integration. |
| **Postgres + outbox/CDC** | Baseline | DIY (see schema above) | Default for non-.NET, modest scale. Use Debezium for CDC, or pgvector-style direct projections. |

### Migration notes if switching engines

- **Domain event payload schema is portable** — JSON metadata and `event_type` strings travel cleanly. Aggregate-id format and stream-name conventions usually need a mapping function.
- **Optimistic-concurrency model differs**: Postgres uses UNIQUE(aggregate, version); KurrentDB uses `expectedRevision`; Marten exposes both. Keep the abstraction in the application layer.
- **Snapshots are tool-specific** — plan a re-snapshot job at migration time.

### "Domain events vs. integration events" reminder (2025–2026 discourse)

The current convention separates:
- **Domain events** — past-tense facts inside an aggregate; payload is intent-only and bounded to the domain language. Stored in the event store.
- **Integration events** — what gets published outside the bounded context via outbox/CDC; can be a transformed projection of one or many domain events.

Schema design rule: never publish raw domain events on the message bus. Wrap or project to an integration-event shape on the outbox row.

## References

- Greg Young — *Event Sourcing* (canonical talks, CQRS Documents)
- Martin Fowler — *Event Sourcing*, *CQRS* patterns
- Vaughn Vernon — *Implementing Domain-Driven Design*
- Eric Evans — *Domain-Driven Design*
- Chris Richardson — *Microservices Patterns* (saga, outbox, event-driven)
- Kurrent / KurrentDB (kurrent.io) — formerly EventStoreDB; rebranded December 2024
- Marten (martendb.io) — embedded event store on Postgres for .NET; v7 (2024), v8 (2026)
- Axon Framework — Java event-sourcing toolkit
- Debezium — CDC for outbox/event publishing
- Pat Helland — *Immutability Changes Everything*
- O'Reilly — *Designing Data-Intensive Applications* (Stream Processing chapter)
- Confluent — *Designing Event-Driven Systems* (Ben Stopford)
