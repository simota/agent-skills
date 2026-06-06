# Saga Patterns

**Purpose:** Design guide for Saga patterns (Orchestration / Choreography).
**Read when:** Designing distributed transactions or long-running workflows.

---

## Orchestration Pattern

A central orchestrator (the Saga Coordinator) drives each step.

### Structure

```
┌──────────────────────────────────┐
│        Saga Orchestrator         │
│                                  │
│  Step 1 → Step 2 → Step 3       │
│    ↓         ↓         ↓        │
│  Comp 3 ← Comp 2 ← Comp 1      │
│  (rollback on failure)           │
└──────────────────────────────────┘
     ↕         ↕         ↕
  Service A  Service B  Service C
```

### Template

```yaml
SAGA_ORCHESTRATION:
  name: "[SagaName]"
  timeout: "[TotalTimeout]"
  steps:
    - name: "[Step1]"
      service: "[ServiceA]"
      action:
        command: "[ForwardCommand]"
        timeout: "[StepTimeout]"
        retry:
          max_attempts: 3
          backoff: exponential
          base_delay: "1s"
      compensation:
        command: "[CompensationCommand]"
        timeout: "[CompTimeout]"
        retry:
          max_attempts: 5
          backoff: exponential
      on_success: "[Step2]"
      on_failure: "COMPENSATE"
    - name: "[Step2]"
      service: "[ServiceB]"
      action:
        command: "[ForwardCommand]"
      compensation:
        command: "[CompensationCommand]"
      on_success: "[Step3]"
      on_failure: "COMPENSATE"
  compensation_order: "reverse"  # reverse | custom
  idempotency:
    strategy: "idempotency_key"
    key_format: "saga:{saga_id}:step:{step_name}:{attempt}"
```

### Use Cases

- E-commerce order processing (reserve inventory -> charge payment -> dispatch shipment)
- User registration (create account -> send email -> run initial setup)
- Travel booking (flight -> hotel -> rental car)

---

## Choreography Pattern

Each service publishes and subscribes to events, coordinating autonomously.

### Structure

```
Service A ──event──→ Service B ──event──→ Service C
    ↑                    ↑                    │
    └────comp event──────┴────comp event──────┘
```

### Template

```yaml
SAGA_CHOREOGRAPHY:
  name: "[SagaName]"
  services:
    - name: "[ServiceA]"
      listens_to:
        - event: "[TriggerEvent]"
          action: "[Process]"
          emits: "[SuccessEvent]"
          on_failure:
            emits: "[FailureEvent]"
      compensates_on:
        - event: "[CompensationTrigger]"
          action: "[RollbackAction]"
    - name: "[ServiceB]"
      listens_to:
        - event: "[ServiceA.SuccessEvent]"
          action: "[Process]"
          emits: "[SuccessEvent]"
  correlation:
    key: "saga_id"
    timeout: "30m"
    dead_letter:
      destination: "[DLQ]"
      alert: true
```

---

## Compensation Design Rules

### 1. Semantic Undo, Not Technical Undo

```yaml
# Good: undo in business terms
compensation:
  action: "cancel_reservation"  # cancel the reservation
  side_effects:
    - "send_cancellation_email"
    - "release_inventory"

# Bad: reverse the DB operation
compensation:
  action: "DELETE FROM reservations WHERE id = ?"
```

### 2. Idempotent Compensations

```yaml
compensation:
  command: "cancel_payment"
  idempotency:
    check: "SELECT status FROM payments WHERE idempotency_key = ?"
    skip_if: "status IN ('cancelled', 'refunded')"
```

### 3. Timeout and Escalation

```yaml
compensation:
  command: "refund_payment"
  timeout: "30s"
  on_timeout:
    retry: 3
    escalate_to: "manual_intervention_queue"
    alert:
      channel: "#ops-alerts"
      severity: "high"
```

---

## Pattern Selection Decision Tree

```
Need a distributed transaction?
├── No → A single-DB transaction is enough
└── Yes
    ├── Participating services <= 3?
    │   ├── Yes
    │   │   ├── Want loose coupling between services?
    │   │   │   ├── Yes → Choreography
    │   │   │   └── No → Orchestration (simpler)
    │   │   └──
    │   └── No (4+ services)
    │       └── Prefer Orchestration
    ├── Is end-to-end visibility important?
    │   ├── Yes → Orchestration
    │   └── No → Choreography
    ├── Is ease of debugging important?
    │   ├── Yes → Orchestration
    │   └── No → Either works
    └── Want to avoid a single point of failure?
        ├── Yes → Choreography
        └── No → Orchestration
```

---

## Error Handling Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| Retry | Resolve transient failures by retrying | Network timeout, 429 |
| Compensate | Roll back previously completed steps | Business logic failure |
| Pivot | Switch to an alternate flow | Primary path unavailable |
| Park | Pause and wait for human intervention | Unrecoverable, needs decision |
| Ignore | Skip because the impact is minor | Non-critical side effects |

---

## Observability

```yaml
SAGA_OBSERVABILITY:
  tracing:
    correlation_id: "saga:{saga_id}"
    span_per_step: true
    propagation: "W3C Trace Context"
  metrics:
    - name: "saga_duration_seconds"
      type: histogram
      labels: [saga_name, status]
    - name: "saga_step_failures_total"
      type: counter
      labels: [saga_name, step_name, error_type]
    - name: "saga_compensations_total"
      type: counter
      labels: [saga_name, trigger_step]
  logging:
    level: "INFO"
    structured: true
    fields: [saga_id, step, status, duration]
```
