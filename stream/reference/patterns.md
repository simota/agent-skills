# Stream Collaboration Patterns

Purpose: handoff patterns between Stream and partner agents, plus common pipeline archetypes.

## Contents

1. Partner-agent flows
2. Common orchestration patterns

## Partner-Agent Flows

| Pattern | Trigger | Flow | Main Output |
|---------|---------|------|-------------|
| Schema-to-Pipeline | new source/target model exists | `Schema -> Stream -> Builder` | connector and load requirements |
| Analytics Pipeline | KPIs or marts are requested | `Pulse -> Stream -> Schema` | mart and aggregation requirements |
| Pipeline Visualization | architecture must be visualized | `Stream -> Canvas` | data-flow packet |
| Pipeline Testing | tests are needed | `Stream -> Radar` | quality and integration test requirements |
| Cost-Aware Pipeline | infra sizing is needed | `Stream -> Scaffold` | platform resource requirements |

## Common Orchestration Patterns

| Scenario | Pattern |
|----------|---------|
| Real-time analytics | `Source DB -> Debezium -> Kafka -> Flink -> Redis -> Dashboard` |
| Data warehouse ETL | `APIs/DBs -> Airbyte -> Staging -> dbt -> Marts -> BI` |
| ML feature pipeline | `Events -> Kafka -> Spark -> Feature Store -> Models` |
| Event sourcing | `Commands -> Event Store -> Projections -> Read Models` |
