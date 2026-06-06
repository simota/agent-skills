# Data Quality Monitoring

## 2026 Observability Landscape

For analytics-pipeline quality, the 2026-relevant tools are:

| Tool | Coverage | Note |
|------|----------|------|
| **Snowflake Cortex `ML.ANOMALY_DETECTION`** / **BigQuery ML `ML.DETECT_ANOMALIES`** | In-warehouse, SQL-native | Pair with daily completeness check |
| **Monte Carlo / Bigeye / Soda** | Data observability vendors | Schema drift, freshness, volume, distribution |
| **dbt tests + `dbt-expectations`** | Inline assertions on transformed tables | Default for any dbt project |
| **dbt Semantic Layer** (GA 2024-10) | Defines metrics once → consistent across BI, no scope drift in GA4-vs-warehouse comparisons | [dbt SL docs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl) |
| **RudderStack Tracking Plan as Code** | Catches event schema drift at ingest, not at query | Launched 2025 |

Coordinate with Beacon for infra-level monitoring; Pulse owns the analytics-pipeline quality contract.

## Quality Dimensions

| Dimension | Target | Alert | How to Monitor |
|-----------|--------|-------|----------------|
| **Completeness** | 99% | < 95% | Expected vs actual event count |
| **Timeliness** | < 5 min | > 15 min | Event timestamp vs ingestion time |
| **Validity** | 99.5% | < 98% | Zod schema validation rate |
| **Uniqueness** | 99.9% | < 99% | Dedup by event_id |
| **Consistency** | 95% | < 90% | Cross-platform comparison |

## Schema Validation with Zod

```typescript
import { z } from 'zod';

const BaseEventSchema = z.object({
  event_name: z.string().min(1).max(100),
  timestamp: z.string().datetime(),
  user_id: z.string().optional(),
  anonymous_id: z.string().min(1),
  context: z.object({
    page_url: z.string().url(),
    page_title: z.string(),
    referrer: z.string(),
    user_agent: z.string(),
  }),
  properties: z.record(z.unknown()),
});

function validateEvent(event: unknown): { valid: boolean; errors?: z.ZodError } {
  const result = BaseEventSchema.safeParse(event);
  return result.success ? { valid: true } : { valid: false, errors: result.error };
}
```

## Freshness Monitor

```typescript
interface FreshnessConfig {
  eventName: string;
  maxStalenessMinutes: number;
}

const configs: FreshnessConfig[] = [
  { eventName: 'page_view', maxStalenessMinutes: 5 },
  { eventName: 'user_signed_up', maxStalenessMinutes: 30 },
  { eventName: 'purchase_completed', maxStalenessMinutes: 15 },
];
```

## BigQuery Quality Dashboard

```sql
-- Completeness check
SELECT event_name, DATE(event_timestamp) as date, COUNT(*) as actual,
  AVG(COUNT(*)) OVER (PARTITION BY event_name ORDER BY DATE(event_timestamp) ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) as expected
FROM events
WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY event_name, date;

-- Duplicate detection
SELECT event_name, COUNT(*) as total, COUNT(DISTINCT event_id) as unique_events,
  COUNT(*) - COUNT(DISTINCT event_id) as duplicates
FROM events WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
GROUP BY event_name ORDER BY duplicates DESC;
```
