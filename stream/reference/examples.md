# Stream Examples

Purpose: compact scenario examples that preserve the main architecture choices, quality gates, and recovery patterns used by Stream.

## Contents

1. Real-time analytics
2. dbt warehouse design
3. Airflow batch ETL
4. CDC with Debezium

## Example 1: Real-Time Orders Analytics

| Input pattern | Key decision | Must-keep notes |
|---------------|--------------|-----------------|
| PostgreSQL -> Snowflake with dashboard latency `< 1 minute` | `Kappa Architecture` with `Debezium -> Kafka -> Flink` | retention `7d`, replay enabled, sink reconciliation required |

Keep:
- topic naming by domain
- source/transform/sink quality checks
- rollback via replay or warehouse snapshot/time-travel capability

## Example 2: dbt Customer Analytics

| Input pattern | Key decision | Must-keep notes |
|---------------|--------------|-----------------|
| customer analytics mart in warehouse | layered dbt design | `stg_ -> int_ -> dim_/fct_`, tests on PK/FK and measure ranges |

Keep:
- staging remains `1:1` with sources
- marts are business-facing outputs
- materialization depends on data size and reuse

## Example 3: Airflow Daily Batch ETL

| Input pattern | Key decision | Must-keep notes |
|---------------|--------------|-----------------|
| daily `S3 -> BigQuery` batch load | idempotent DAG with validation gates | `WRITE_TRUNCATE` or partition overwrite, reconciliation check, backfill command, alert on row-count anomaly |

Minimal alert example:
- SLA breach
- validation failure
- row count `< 80%` of the 7-day average

## Example 4: PostgreSQL CDC To Kafka

| Input pattern | Key decision | Must-keep notes |
|---------------|--------------|-----------------|
| database changes streamed to Kafka | `Debezium` + schema registry + manual consumer commits | lag monitoring, replication-slot monitoring, consumer-lag thresholds |

Minimal thresholds:
- CDC lag alert: `60s`
- replication-slot lag alert: `1GB`
- consumer lag alert: `10000`
