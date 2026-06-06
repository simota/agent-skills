# Pipeline Architecture

Purpose: choose the right pipeline mode and core architecture before designing detailed components.

## Contents

1. Batch vs streaming matrix
2. Decision rules
3. Architecture patterns
4. ETL vs ELT
5. Minimal orchestration template

## Batch vs Streaming Decision Matrix

| Factor | Batch | Streaming | Hybrid |
|--------|-------|-----------|--------|
| Latency requirement | hours to days | seconds to minutes | mixed |
| Data volume | large and bounded | continuous | both |
| Processing complexity | complex joins and aggregations | simpler incremental transforms | both |
| Cost sensitivity | high | moderate | balanced |
| Replay requirement | easy | harder | depends |

## Decision Rules

- `latency < 1 minute` -> streaming candidate
- `volume > 10K events/sec` + low latency -> Kafka + Flink/Spark
- complex analytics without sub-minute latency -> batch
- mixed operational + analytical outputs -> hybrid

## Architecture Patterns

### Lambda Architecture

Use only when legacy constraints require separate batch and speed layers. Avoid for new systems when Kappa or hybrid designs are sufficient.

### Kappa Architecture

Use when stream processing can be unified around an immutable log and replay is a first-class requirement.

### Medallion Architecture

Use for lakehouse-style pipelines with progressive refinement:
- `Bronze`: raw
- `Silver`: cleaned and standardized
- `Gold`: business-ready outputs

### Open Lakehouse on Apache Iceberg (2026 default for new lakehouses)

By 2026 the lakehouse table format conversation has converged on **Apache Iceberg**. Greenfield lakehouse projects should default to Iceberg unless a downstream engine forces Delta or Hudi. Snowflake, BigQuery, Databricks (via Uniform), Trino, Spark, Flink, ClickHouse, and DuckDB all read or write Iceberg in 2026, so the format is no longer a vendor-lock decision.

**Apache Iceberg 1.10** (released 2025-09-11; latest patch 1.10.2 on 2026-05-18) delivers full Flink 2.0 support including automatic schema-evolution propagation from stream to Iceberg table, **Deletion Vectors** (V3 spec — row-level updates without costly read-modify-write), native BigQuery Metastore Catalog, and compute_partition_stats incremental refresh. **Iceberg 1.11.0** was released 2026-05-19. Source: [iceberg.apache.org/releases](https://iceberg.apache.org/releases/)

Three adjacent 2026 shifts that pair with Iceberg-on-medallion:

- **Kafka Iceberg Topics** (see `streaming-kafka.md`) expose closed Kafka segments as an Iceberg table on object storage, removing a copy-job step between Bronze and Silver for log-style data.
- **dbt Fusion + Semantic Layer** (see `dbt-modeling.md`) sit above Gold to produce the metric-level contract surface, replacing one-off BI SQL.
- **External Iceberg catalogs in dbt 1.10** (`catalogs.yml`) enable write integrations directly from dbt to Iceberg tables without a separate catalog-management layer.

### Streaming Lakehouse (Iceberg + Flink) vs Kappa

When the workload mixes long-history batch with short-history streaming, the 2026 pattern is **streaming lakehouse**: Iceberg is the system of record, Flink is the real-time processor, the same Iceberg tables are queried by Spark / Trino for batch. This is a *generalisation* of Kappa, not a replacement — use it when the team is willing to operate Iceberg + Flink and the question "what was the state at time T?" must be answerable from one place.

## ETL vs ELT

| Aspect | ETL | ELT |
|--------|-----|-----|
| Transform location | before load | after load |
| Best for | constrained destinations or legacy systems | powerful warehouses |
| Data volume | small to medium | medium to large |
| Flexibility | lower | higher |
| Common stack | Airflow + Python | dbt + Snowflake/BigQuery |

Rules:
- cloud warehouses usually favor ELT
- constrained operational databases usually favor ETL

## Minimal Orchestration Template

```python
with DAG("etl_orders_daily", default_args=default_args, catchup=False) as dag:
    extract = PythonOperator(task_id="extract_orders", python_callable=extract_from_source)
    validate_source = PythonOperator(task_id="validate_source", python_callable=run_quality_checks)
    transform = PythonOperator(task_id="transform_orders", python_callable=apply_business_logic)
    validate_transform = PythonOperator(task_id="validate_transform", python_callable=run_quality_checks)
    load = PostgresOperator(task_id="load_to_warehouse", postgres_conn_id="warehouse", sql="sql/load_orders.sql")

    extract >> validate_source >> transform >> validate_transform >> load
```
