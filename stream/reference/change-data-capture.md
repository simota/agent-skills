# Change Data Capture Reference

Purpose: Design a log-based CDC pipeline that streams row-level changes from an OLTP source (Postgres / MySQL / SQL Server) into Kafka, with a clean snapshot-to-incremental handoff and idempotent downstream consumption. CDC is about capture; the source schema itself stays with `Schema`.

## Scope Boundary

- **Stream `cdc`**: the replication pipeline off a source DB — connector choice, snapshot mode, slot/publication, topic layout, downstream idempotency, cutover.
- **Schema (elsewhere)**: the source table design itself — PK, indexes, `REPLICA IDENTITY`, `wal_level`, column changes, migration ordering.

If the question is "what should the source table look like?" → `Schema`. If the question is "how do we stream changes off that table without losing events during snapshot cutover?" → `cdc`.

## Connector Selection

| Source | Connector | Log source | Notes |
|--------|-----------|------------|-------|
| Postgres | Debezium Postgres | Logical replication (`pgoutput` built-in, `wal2json` legacy) | Prefer `pgoutput` — no extension install, maintained in-core. `wal2json` only for Postgres < 10 or JSON-first pipelines. |
| MySQL | Debezium MySQL | Binlog (ROW format required) | `binlog_format=ROW`, `binlog_row_image=FULL`, GTID strongly recommended for failover. |
| SQL Server | Debezium SQL Server | SQL Server CDC (built-in) | `sys.sp_cdc_enable_db` + per-table enable; MS SQL CDC is a pull capture on change tables, not a streaming log reader — expect polling latency. |
| MongoDB | Debezium MongoDB | Oplog / Change Streams | Change Streams preferred (≥ 4.0); requires replica set. |
| Oracle | Debezium Oracle (LogMiner or XStream) | Redo logs | XStream license-gated; LogMiner is free but heavier. |

Default: **Debezium on Kafka Connect**. Current stable release: **Debezium 3.4.0.Final** (2025-12-16); 3.5.x series in progress as of early 2026. Debezium 3.x requires Kafka Connect 3.x or 4.x — align with your Kafka version. Source: [debezium.io/releases](https://debezium.io/releases/). Confluent Cloud, Strimzi, or self-hosted Connect cluster — pick by ops posture, not by feature gap.

## Workflow

```
FRAME     →  declare source (DB + version), tables in scope, volume (writes/sec),
             target latency, PII columns, retention window
          →  confirm source prerequisites: wal_level=logical / binlog ROW / CDC enabled
          →  decide snapshot mode: initial | initial_only | never | schema_only | when_needed

LAYOUT    →  pick connector + Kafka Connect topology (distributed cluster, >=3 workers)
          →  name replication slot + publication (Postgres) or server-id + GTID set (MySQL)
          →  design topic layout: one topic per table, key = primary key
          →  pick serialization (Avro + Schema Registry preferred; JSON for early PoC only)
          →  choose sink: Kafka Connect JDBC sink, Iceberg sink, or downstream stream processor

OPTIMIZE  →  idempotent sink keyed by (PK, source LSN/GTID/LSN-equivalent)
          →  DLQ topic for deserialization + sink failures
          →  heartbeat topic to keep slot / binlog position advancing on low-traffic tables
          →  snapshot throttling (max.queue.size, snapshot.fetch.size) to protect source
          →  monitor replication slot lag (Postgres `pg_replication_slots.confirmed_flush_lsn`)

WIRE      →  cutover plan: snapshot → streaming handoff without event loss
          →  rollback: preserve slot + offsets before connector delete
          →  runbook for slot bloat (Postgres) / binlog retention exhaustion (MySQL)
```

## Snapshot → Incremental Handoff

This is where CDC pipelines fail most often. The connector must bracket the snapshot with log positions so no change between "snapshot start" and "streaming start" is dropped or duplicated ambiguously.

- **Debezium incremental snapshots** (signal table / Kafka signal topic): prefer over blocking snapshots for production. Ad-hoc resnapshot of a single table without re-streaming the whole source.
- **Blocking snapshot**: acceptable for first bring-up on low-traffic sources; reserves a consistent read point before streaming.
- **`schema_only` + backfill from warehouse**: valid when full historical backfill is too expensive — combine with a dbt backfill from a prior ELT landing.

Never delete and recreate a connector to "fix" a stuck snapshot without capturing the slot LSN first — that is event loss.

## Postgres Specifics

- `wal_level = logical`, `max_replication_slots >= connectors + headroom`, `max_wal_senders` matched.
- `REPLICA IDENTITY FULL` on tables without a PK, or on tables whose UPDATE/DELETE need full before-image. Default `DEFAULT` only emits PK columns in before-image.
- Publication: `CREATE PUBLICATION dbz_pub FOR TABLE ...` — prefer explicit table lists over `FOR ALL TABLES` for blast-radius control.
- Slot naming: `dbz_<env>_<service>` — slots survive connector restarts; orphaned slots cause unbounded WAL growth.
- TOASTed columns arrive as `__debezium_unavailable_value` unless `REPLICA IDENTITY FULL` — plan downstream handling.

## MySQL Specifics

- `binlog_format = ROW`, `binlog_row_image = FULL`, `binlog_expire_logs_seconds` ≥ connector downtime tolerance.
- GTID mode strongly recommended: enables reconnect to a different replica without position-remapping.
- `server-id` must be unique per connector instance (Debezium presents itself as a replica).
- Schema history topic is mandatory — Debezium replays DDL from the binlog to reconstruct column types.

## SQL Server Specifics

- Enable at DB and table level: `sys.sp_cdc_enable_db`, `sys.sp_cdc_enable_table`.
- Capture is a pull from change tables (`cdc.<schema>_<table>_CT`) — latency floor ≈ CDC capture job interval (default 5 s).
- Change-table retention (`cleanup_threshold`) must exceed connector downtime tolerance, or history is lost.

## Downstream Sink Patterns

- **Kafka → Iceberg via Tableflow / Iceberg sink**: materialize CDC topics into lakehouse with compaction. Maps to `elt` handoff.
- **Kafka → JDBC sink (upsert)**: direct replication to warehouse/OLTP mirror. Key = PK, `pk.mode=record_key`, `insert.mode=upsert`.
- **Kafka → Flink**: in-stream joins, enrichment, materialized views. Use `DEBEZIUM-JSON` or `DEBEZIUM-AVRO` format.
- **Kafka → Stream processor → warehouse**: fan-out for fact-table construction.

## Anti-Patterns

- Dual-writing application writes to both DB and Kafka — use the transactional outbox pattern instead, or rely on CDC as the single source.
- Keying topics by something other than the source PK — breaks compaction, breaks idempotent upsert.
- Deleting a Postgres replication slot to "clean up" without confirming downstream has consumed through the slot's LSN.
- Running Debezium without a heartbeat on a low-traffic table — slot LSN stalls, WAL fills disk.
- Treating tombstone (`null` value) records as garbage — they are the delete signal for log-compacted sinks.
- Snapshotting a multi-TB table on the primary during peak hours — use a read replica or incremental snapshot.

## Handoff

- To `Schema`: source schema changes needed (add PK, set `REPLICA IDENTITY FULL`, add index supporting the capture).
- To `Builder`: connector config, Connect cluster deploy, sink adapter code.
- To `Beacon`: slot-lag SLI, connector-status SLI, snapshot-duration SLI.
- To `Sentinel`: PII columns in CDC stream — masking / tokenization strategy before topic publish.
- To `elt` (within Stream): CDC topics landing into Bronze tier for downstream dbt transformation.
