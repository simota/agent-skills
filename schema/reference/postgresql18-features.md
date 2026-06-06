# PostgreSQL 18 Features Guide

Reference for PostgreSQL 18 (GA 2025-09-25) schema-design–relevant features. Snapshot: 2026-05.

> Migrating from PostgreSQL 17? Most 17 features still apply — see `postgresql17-features.md` for SQL/JSON (`JSON_TABLE`, `JSON_VALUE`, `JSON_QUERY`, `JSON_EXISTS`), `SPLIT`/`MERGE PARTITION`, logical replication failover, and `pg_createsubscriber`. PostgreSQL 18 keeps all of them and adds the items below.

## Release Timeline

| Version | GA | Status (2026-05) |
|---------|----|-----|
| PostgreSQL 17 | 2024-09-26 | minor 17.5 (May 2025), full community support |
| PostgreSQL 18 | 2025-09-25 | minor 18.x in 2026, current stable |
| PostgreSQL 19 | expected late-2026 | in beta cycle |

Source: postgresql.org news/release-18.html.

## UUIDv7 Native Generator

PostgreSQL 18 adds the built-in `uuidv7()` SQL function — the first community release to ship RFC 9562 (published 2024-05) UUID variants 6/7/8.

```sql
CREATE TABLE orders (
  id          UUID PRIMARY KEY DEFAULT uuidv7(),
  placed_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  customer_id UUID NOT NULL
);

-- Recover the embedded millisecond timestamp
SELECT uuid_extract_timestamp(id) FROM orders LIMIT 5;
```

**Schema design rules:**
- Prefer `uuidv7()` over `gen_random_uuid()` (UUIDv4) for new PKs — the 48-bit Unix-ms prefix is K-sortable, so new rows cluster in the right-most B-tree leaf pages, eliminating UUIDv4's random-write amplification and FILLFACTOR-induced bloat.
- Keep storing as native `UUID` (16 bytes). Do **not** store UUIDv7 as `VARCHAR(36)` — that defeats both space and sort benefits.
- Use `uuid_extract_timestamp(id)` for cheap row-age queries and as a partition-key surrogate when you want UUID PK + time partitioning without a separate `created_at` column.

## Virtual Generated Columns (Default)

Generated columns now default to `VIRTUAL` (computed on read, not stored). PostgreSQL 12 introduced `STORED` only and required a full table rewrite to add one; PostgreSQL 18 makes adding a virtual generated column an O(1) metadata change.

```sql
-- O(1) metadata change — no table rewrite, no AccessExclusiveLock duration
ALTER TABLE products
  ADD COLUMN display_price TEXT
  GENERATED ALWAYS AS (currency || ' ' || amount::text) VIRTUAL;
```

**Schema design rules:**
- Use `VIRTUAL` for cheap derivations referenced by reports/views (locale formatting, status display strings, derived flags).
- Use `STORED` only when the expression is expensive AND queried far more often than rows are written, AND you can afford the table-rewrite cost on initial add.
- Virtual columns cannot be indexed directly — wrap in an expression index (`CREATE INDEX ... ON t ((expression))`) if you need lookups.

## Temporal Constraints — `WITHOUT OVERLAPS` / `PERIOD`

PostgreSQL 18 brings SQL:2011 temporal primary keys and foreign keys directly into the engine — no more handcrafted `EXCLUDE USING gist` workarounds for the common case.

```sql
CREATE TABLE room_bookings (
  room_id   UUID NOT NULL,
  period    tsrange NOT NULL,
  guest_id  UUID NOT NULL,
  PRIMARY KEY (room_id, period WITHOUT OVERLAPS)
);

CREATE TABLE room_charges (
  booking_room  UUID NOT NULL,
  booking_range tsrange NOT NULL,
  amount        NUMERIC NOT NULL,
  FOREIGN KEY (booking_room, PERIOD booking_range)
    REFERENCES room_bookings (room_id, PERIOD period)
);
```

**Schema design rules:**
- Use for scheduling, room/asset booking, employment contracts, price effective-windows, and bitemporal "valid-time" axes.
- Combine with audit-log capture for "transaction-time" axis to model full bitemporal — temporal PK covers business time only.
- Pair with the `range_agg` aggregate from PG 14+ when reporting on coverage gaps.

## `RETURNING OLD.*` / `NEW.*` in UPDATE / DELETE / MERGE

```sql
UPDATE orders
   SET status_v2 = translate_status(status)
 WHERE status_v2 IS NULL
RETURNING OLD.status, NEW.status_v2;
```

**Schema design rule:** Use during expand-contract backfill phases to verify the transformation in the same round-trip — replaces the SELECT-after-UPDATE pattern that races with concurrent writers.

## Asynchronous I/O Subsystem

PostgreSQL 18 introduces an async I/O subsystem. The official release notes cite 2–3× improvement on sequential scan, bitmap heap scan, and vacuum for storage-bound workloads (`io_method = worker` default; `io_method = io_uring` on Linux).

**Schema design implication:** Large partitioned fact tables that previously needed BRIN-on-time + aggressive vacuum tuning to keep scans fast can now tolerate slightly looser vacuum schedules. Re-evaluate `autovacuum_naptime` and `autovacuum_vacuum_scale_factor` after upgrading.

## OAuth Authentication (`oauth` method in `pg_hba.conf`)

```text
# pg_hba.conf
host all all 0.0.0.0/0 oauth issuer="https://idp.example.com" scope="postgres"
```

**Schema design implication:** Service-to-DB credentials can be replaced with short-lived OAuth tokens (validated via `oauth_validator_libraries`). Combine with RLS `current_setting('app.tenant_id')` to pull tenant context from the verified token claim instead of an application-set GUC — this hardens multi-tenant isolation against application-layer bypass.

## DDL Replication in Logical Replication

PostgreSQL 18 propagates `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE` from publisher to subscribers — eliminates the manual `psql -f schema.sql` step on every replica during migrations.

**Schema design rules:**
- Add `WITH (ddl = 'all')` to the publication to enable.
- Verify subscriber catches up before reading off it — DDL apply is serial with DML, so a long `ALTER TABLE` blocks the replication slot.
- Continue to use expand-contract for breaking changes; DDL replication does not change application compatibility requirements.

## `NOT VALID` Constraint Validation (still relevant in PG 18)

```sql
ALTER TABLE t ADD CONSTRAINT chk_age CHECK (age >= 0) NOT VALID;
-- short ACCESS EXCLUSIVE; no full-table scan

ALTER TABLE t VALIDATE CONSTRAINT chk_age;
-- SHARE UPDATE EXCLUSIVE; concurrent reads and writes continue
```

Available since PG 9.x for CHECK/FK and PG 12 for `NOT NULL`; called out here because it remains the single most useful primitive for zero-downtime schema migrations and pairs naturally with PG 18's virtual generated columns.

## B-tree Skip Scan

PG 18 lets the planner skip across leading-column values that don't appear in the predicate (`WHERE b = ?` on an `(a, b)` index). Reduces — but does not eliminate — the need for a dedicated index on `b` when `a` has low cardinality. Combine with partial indexes for high-skew leading columns. (Tuner owns query-plan tuning; Schema's concern is when *not* to add a redundant single-column index.)

## Bitemporal-Friendly Type Combinations

PG 18 retains and refines the building blocks:

| Need | PG 18 idiom |
|------|-------------|
| Business time interval | `WITHOUT OVERLAPS` on `tstzrange`/`tsrange` |
| Transaction time interval | append-only audit table + `recorded_at`/`invalidated_at` |
| Multi-version aggregate state | event sourcing + snapshot table |
| Daily / monthly history | range or hash partitioning by `recorded_at` |

## References

- PostgreSQL 18 release notes — https://www.postgresql.org/docs/18/release-18.html
- PostgreSQL 18 announcement (2025-09-25) — https://www.postgresql.org/about/news/postgresql-18-released-3142/
- Aiven blog — temporal constraints walkthrough
- Crunchy Data — Get Excited About Postgres 18
- Bytebase — What's New in PostgreSQL 18
- Xata — Postgres 18 features
- RFC 9562 (Universally Unique IDentifiers) — 2024-05
