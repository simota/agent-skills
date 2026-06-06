# Event-Driven Workflow Patterns

**Purpose:** Pattern catalog for event-driven workflow design.
**Read when:** Designing workflows in an event-driven architecture.

---

## Event-Driven vs Request-Driven

| Aspect | Event-Driven | Request-Driven |
|--------|-------------|----------------|
| Coupling | Loose (pub/sub) | Tight (RPC) |
| Temporal | Async | Sync |
| Failure isolation | High | Low |
| Debugging | Harder | Easier |
| Scalability | High | Medium |

---

## Event Sourcing + Workflow

### Pattern: Event-Sourced State Machine

```yaml
EVENT_SOURCED_WORKFLOW:
  aggregate: "[AggregateName]"
  events:
    - name: "[EventName]"
      version: 1
      schema:
        field1: type
        field2: type
      metadata:
        timestamp: ISO8601
        correlation_id: uuid
        causation_id: uuid

  state_from_events:
    # State is derived by replaying events
    apply:
      OrderCreated: { state: "created", set: [order_id, items] }
      PaymentReceived: { state: "paid", set: [payment_id] }
      OrderShipped: { state: "shipped", set: [tracking_number] }
      OrderDelivered: { state: "delivered", set: [delivered_at] }
      OrderCancelled: { state: "cancelled", set: [reason] }
```

### CQRS Integration

```yaml
CQRS_WORKFLOW:
  command_side:
    commands:
      - name: "[CommandName]"
        validates: "[Business rules]"
        emits: "[EventName]"
        updates_state: true

  query_side:
    projections:
      - name: "[ProjectionName]"
        subscribes_to: ["[Event1]", "[Event2]"]
        builds: "[Read model]"
        storage: "[DB/Cache]"

  workflow_triggers:
    # Events that trigger workflow transitions
    - event: "[EventName]"
      condition: "[Optional condition]"
      triggers_command: "[NextCommand]"
      in_service: "[TargetService]"
```

---

## Process Manager Pattern

A stateful coordinator that manages long-running business processes.

```yaml
PROCESS_MANAGER:
  name: "[ProcessName]"
  correlation_key: "[entity_id]"
  timeout: "[MaxDuration]"

  subscriptions:
    - event: "[Event1]"
      when_in_state: "[StateA]"
      action: "[Send command / transition]"
    - event: "[Event2]"
      when_in_state: "[StateB]"
      action: "[Send command / transition]"

  state_machine:
    initial: "[InitialState]"
    states:
      "[StateA]":
        on:
          "[Event1]":
            target: "[StateB]"
            actions:
              - send_command: "[Command]"
                to: "[Service]"
      "[StateB]":
        on:
          "[Event2]":
            target: "[StateC]"

  timeout_handling:
    "[StateA]":
      after: "1h"
      action: "send_reminder"
    "[StateB]":
      after: "24h"
      action: "escalate"
```

---

## Outbox Pattern

A transactional outbox that guarantees reliable event publishing.

```yaml
OUTBOX_PATTERN:
  description: "Atomically combine DB writes with event publication"

  write_path:
    transaction:
      - update_aggregate: "[State change]"
      - insert_outbox:
          table: "outbox_events"
          columns:
            id: uuid
            aggregate_type: string
            aggregate_id: string
            event_type: string
            payload: jsonb
            created_at: timestamp
            published_at: "null (pending)"

  publish_path:
    poller:
      interval: "100ms"
      query: "SELECT * FROM outbox_events WHERE published_at IS NULL ORDER BY created_at LIMIT 100"
      on_publish:
        - publish_to: "[Message broker]"
        - update: "SET published_at = NOW()"

    # Alternative: CDC (Change Data Capture)
    cdc:
      source: "outbox_events table"
      connector: "Debezium"
      sink: "[Kafka topic]"
```

---

## Dead Letter Queue Strategy

```yaml
DLQ_STRATEGY:
  triggers:
    - max_retries_exceeded: true
    - poison_message: true
    - schema_validation_failure: true

  handling:
    - level: "automated"
      condition: "known_transient_error"
      action: "retry_with_delay(exponential, max=5)"
    - level: "semi_automated"
      condition: "schema_mismatch"
      action: "log_and_alert"
    - level: "manual"
      condition: "unknown_error"
      action: "move_to_dlq, alert_on_call"

  dlq_processing:
    review_interval: "1h"
    auto_expire: "30d"
    replay_capability: true
```

---

## Idempotency Patterns

| Pattern | How | Storage | Trade-off |
|---------|-----|---------|-----------|
| Idempotency Key | Attach a unique key to each request | DB/Redis | Extra storage required |
| Conditional Write | IF NOT EXISTS / version check | DB | DB-dependent |
| Event Dedup | Deduplicate by event ID | In-memory / DB | Memory usage |
| Natural Idempotency | Operation is inherently idempotent | N/A | Design constraint |

```yaml
IDEMPOTENCY:
  key_generation:
    format: "{entity_type}:{entity_id}:{action}:{version}"
    example: "order:123:payment:v1"

  storage:
    type: "redis"
    ttl: "24h"
    check_before: "execute"
    store_after: "commit"

  on_duplicate:
    action: "return_cached_result"
    log: true
```
