# Data Modeling Anti-Patterns

Purpose: Use this file when evaluating EAV, polymorphic relations, denormalization, or temporal data design.

Contents:
1. Core anti-patterns
2. EAV decision rules
3. Polymorphic alternatives
4. Normalization vs denormalization
5. Temporal modeling
6. Design gates

## Core Anti-Patterns

| ID | Anti-pattern | Signal | Safer pattern |
|----|--------------|--------|---------------|
| `DM-01` | EAV Abuse | Dynamic attributes are modeled as rows even though the shape is mostly known | Use dedicated columns; reserve EAV/JSONB for truly dynamic fields |
| `DM-02` | Polymorphic Association Trap | `*_type + *_id` pairs block FK integrity and create orphans | Use dedicated FK tables, nullable FK with `CHECK`, or explicit join tables |
| `DM-03` | Over-Normalization | `5+` table joins for routine reads, query latency dominated by join cost | Denormalize strategically or add materialized views |
| `DM-04` | Under-Normalization | Same business fact duplicated in `3+` tables | Normalize to a single source of truth |
| `DM-05` | JSONB Everything | Stable business fields live inside JSONB and block reporting/indexing | Promote stable fields to columns |
| `DM-06` | Multi-Purpose Table | `type` column drives unrelated entity variants, many nullable columns | Split tables or use disciplined STI |
| `DM-07` | Temporal Blindness | Current state only; no way to answer historical questions | Add history table, valid-time range, or event log |

## EAV Decision Rules

Use EAV or JSONB only when all of these are true:
- Attribute shape cannot be fully defined up front
- Attribute count is highly variable, often `100+`
- Each entity uses a small subset, often `<10%`, of the total attribute universe
- Strict relational integrity is not required for those fields

Avoid EAV or JSONB when:
- You need aggregation, sorting, or filtering on the fields often
- The fields need FK references or strong type guarantees
- The field set is stable enough to define as columns

## Polymorphic Alternatives

| Situation | Recommended pattern |
|----------|---------------------|
| `2-3` target tables | Nullable FKs plus `CHECK (num_nonnulls(...) = 1)` |
| `4+` target tables | Separate child tables or join tables per target |
| Legacy framework already uses polymorphic links | Stage toward nullable FK or dedicated relation tables |

## Normalization Vs Denormalization

| Favor normalization when... | Favor denormalization when... |
|-----------------------------|-------------------------------|
| Writes are frequent | Reads dominate |
| Integrity is business-critical | JOIN cost is the bottleneck |
| Shared master data must stay consistent | Dashboard/reporting latency matters |
| Source-of-truth must stay singular | You can document update strategy clearly |

If you denormalize, document:
- Source of truth
- Refresh or sync method
- Integrity checks
- Why a normalized alternative is insufficient

## Temporal Modeling

| Need | Pattern |
|------|---------|
| No history required | Type 1 overwrite |
| Previous value only | Type 3 previous-value columns |
| Full record history | Type 2 history table with `valid_from` / `valid_to` |
| Full event trail | Event sourcing |

### Requirement → Pattern Mapping

| Requirement | Recommended pattern |
|-------------|---------------------|
| "Show me the current value" | Type 1 (simple overwrite) |
| "What changed last time?" | Type 3 (previous-value columns) |
| "Show me the value on date X" | Type 2 SCD (`valid_from` / `valid_to`) |
| "What did the system believe on date X about event Y in period Z?" | Bitemporal (valid time + transaction time) |
| "Replay every change in order" | Event sourcing (`event_store` append-only) |
| "Aggregate historical state efficiently" | CQRS projection + snapshot |

### Bitemporal Signals

Apply bitemporal design when **any** of these are true:
1. Retroactive corrections to historical data are a business requirement (e.g., "we entered the wrong salary — fix it back to Jan 1").
2. Audit requirements demand knowing what the database believed at a specific point in time, not just what was true.
3. Two independent parties control "what is true" vs. "when it was recorded" (e.g., insurance effective dates vs. policy entry dates).

### System-Versioned Tables (PostgreSQL Approximation)

PostgreSQL does not natively support SQL:2011 system-versioned tables, but you can approximate them:

```sql
-- Append-only history table pattern
CREATE TABLE employees (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  role        TEXT NOT NULL,
  -- Transaction time columns
  sys_from    TIMESTAMPTZ NOT NULL DEFAULT now(),
  sys_to      TIMESTAMPTZ NOT NULL DEFAULT 'infinity'
);

-- Trigger-based versioning: on UPDATE, close old row, insert new row
CREATE OR REPLACE FUNCTION versioned_update() RETURNS trigger AS $$
BEGIN
  -- Close the current row
  UPDATE employees SET sys_to = now() WHERE id = OLD.id AND sys_to = 'infinity';
  -- Insert new version
  INSERT INTO employees VALUES (OLD.id, NEW.name, NEW.role, now(), 'infinity');
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_employees_version
  BEFORE UPDATE ON employees
  FOR EACH ROW EXECUTE FUNCTION versioned_update();

-- Query: point-in-time lookup
SELECT * FROM employees
WHERE id = $1
  AND sys_from <= $2
  AND sys_to   >  $2;
```

**Note:** Prefer dedicated audit/history tables with explicit INSERT to avoid trigger complexity for most use cases. Reserve this pattern for high-volume tables where a separate audit table would double storage.

## Design Gates

- EAV table detected -> justify why dedicated columns or JSONB are insufficient
- `*_type + *_id` pair detected -> propose a typed alternative
- `5+` table join in a routine path -> review for denormalization
- Same fact repeated in `3+` tables -> normalize
- `5+` JSONB-heavy core columns -> review for column promotion
- Table has `50%+` nullable columns -> review for table split
- Historical reporting need exists but no history strategy exists -> add temporal design
