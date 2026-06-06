# Data Reliability — Quality, CDC, Idempotency, Backfill

Purpose: reliability rules for quality gates, CDC selection, idempotency, backfill, replay, and rollback planning.

## Contents

1. Three-layer quality model
2. CDC pattern selection
3. Idempotency patterns
4. Backfill and rollback

## Three-Layer Quality Model

| Layer | Required checks |
|-------|-----------------|
| Source | freshness, volume, schema |
| Transform | uniqueness, completeness, validity, consistency |
| Sink | reconciliation, business rules, anomaly detection |

Use all three layers when the pipeline affects analytics, billing, or user-facing metrics.

### Example Gate

```python
def run_quality_gate(**context):
    result = context.run_checkpoint(checkpoint_name="orders_checkpoint")
    if not result["success"]:
        raise AirflowException(f"Quality check failed: {result['run_results']}")
    return result
```

## CDC Pattern Selection

| Pattern | Latency | Complexity | Use Case |
|---------|---------|------------|----------|
| Timestamp-based | minutes to hours | low | simple incremental loads |
| Trigger-based | seconds | medium | legacy DBs without log access |
| Log-based (`Debezium`) | sub-second | high | real-time sync with minimal DB impact |

Use log-based CDC for low-latency, replay-friendly pipelines. Keep schema and delivery settings versioned.

## Idempotency Patterns

Preferred options:
- deterministic idempotency keys
- Redis or state-store deduplication
- sink-side `UPSERT`
- Kafka transactions only when the end-to-end path justifies them

### Deterministic Key

```python
def generate_idempotency_key(event: dict) -> str:
    components = [
        event["source"],
        event["entity_type"],
        event["entity_id"],
        event["event_type"],
        event["timestamp"][:19],
    ]
    return hashlib.sha256("|".join(components).encode()).hexdigest()
```

## Backfill And Rollback

### Backfill Decision Matrix

| Scenario | Strategy | Risk |
|----------|----------|------|
| Schema change only | reprocess all | low |
| Recent bug fix | reprocess affected window | low |
| Logic change | full historical reprocess | medium |
| New source | incremental from source start | low |

### Pre-Backfill Checklist

- [ ] production pipeline paused if required
- [ ] downstream consumers notified
- [ ] target-table or partition backup created
- [ ] monitoring thresholds adjusted

### Minimal Backfill Runbook

1. Pause the production DAG or consumer if needed.
2. Clear or isolate the target range.
3. Run the backfill command.
4. Verify counts and quality checks.
5. Resume normal processing.

```bash
airflow dags backfill \
  --start-date YYYY-MM-DD \
  --end-date YYYY-MM-DD \
  --reset-dagruns \
  pipeline_name
```

### Rollback Notes

Every backfill plan must include:
- restore path from backup tables, snapshots, or time-travel features
- resume path from checkpoint or retained event log
- downstream notification steps
