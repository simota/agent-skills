# PostgreSQL 18 Features Guide

Reference for PostgreSQL 18 (GA 2025-09-25) schema-design–relevant features. Snapshot: 2026-05.

> Migrating from PostgreSQL 17? Most 17 features still apply — see `postgresql17-features.md` for SQL/JSON (`JSON_TABLE`, `JSON_VALUE`, `JSON_QUERY`, `JSON_EXISTS`), partition maintenance, logical replication failover, and `pg_createsubscriber`. PostgreSQL 18 keeps those capabilities and adds the items below.

## Release Timeline

| Version | GA | Status (2026-05) |
|---------|----|-----|
| PostgreSQL 17 | 2024-09-26 | minor 17.5 (May 2025), full community support |
| PostgreSQL 18 | 2025-09-25 | minor 18.x in 2026, current stable |
| PostgreSQL 19 | expected late-2026 | in beta cycle |

Source: postgresql.org news/release-18.html.

## UUIDv7 Native Generator

PostgreSQL 18 adds the built-in `uuidv7()` SQL function for time-ordered UUIDv7 identifiers defined by RFC 9562 (published 2024-05).

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
-- No table rewrite; ALTER TABLE still acquires ACCESS EXCLUSIVE until commit.
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
CREATE EXTENSION IF NOT EXISTS btree_gist; -- GiST equality support for UUID

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

**Schema design implication:** Service-to-DB credentials can be replaced with short-lived OAuth tokens using a configured validator from `oauth_validator_libraries`. OAuth authenticates/maps a database role; it does not automatically populate `app.tenant_id`. A custom session GUC is application-controlled unless an explicit trusted mechanism enforces it, so do not treat `current_setting('app.tenant_id')` alone as proof of a verified tenant claim. Design the RLS identity mapping and pool reset behavior separately. Source: [PostgreSQL 18 OAuth authentication](https://www.postgresql.org/docs/18/auth-oauth.html), verified 2026-09-13.

## Schema Changes with Logical Replication

PostgreSQL 18 does **not** replicate schema definitions or DDL commands. There is no `ddl` publication option. Schema migrations must be coordinated on the publisher and each subscriber. Source: [PostgreSQL 18 logical replication restrictions](https://www.postgresql.org/docs/18/logical-replication-restrictions.html), verified 2026-09-13.

**Schema design rules:**
- Copy the initial schema separately, for example with `pg_dump --schema-only`, before starting data replication.
- For compatible additive changes, update subscribers before the publisher so incoming rows fit their destination schema.
- Use expand-contract for breaking changes and verify schema compatibility and replication lag before cutover.

## `NOT VALID` Constraint Validation (still relevant in PG 18)

```sql
ALTER TABLE t ADD CONSTRAINT chk_age CHECK (age >= 0) NOT VALID;
-- short ACCESS EXCLUSIVE; no full-table scan

ALTER TABLE t VALIDATE CONSTRAINT chk_age;
-- SHARE UPDATE EXCLUSIVE; concurrent reads and writes continue
```

`NOT VALID` has long been available for CHECK/FK constraints; PostgreSQL 18 also supports named `NOT NULL` constraints added with `NOT VALID`. PostgreSQL 12–17 instead require a validated `CHECK (column IS NOT NULL)` before `SET NOT NULL` can skip its table scan. Source: [PostgreSQL 18 ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html), verified 2026-09-13.

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
- PostgreSQL 18 temporal keys and GiST requirements — https://www.postgresql.org/docs/18/sql-createtable.html (verified 2026-09-13)
- PostgreSQL 18 announcement (2025-09-25) — https://www.postgresql.org/about/news/postgresql-18-released-3142/
- Aiven blog — temporal constraints walkthrough
- Crunchy Data — Get Excited About Postgres 18
- Bytebase — What's New in PostgreSQL 18
- Xata — Postgres 18 features
- RFC 9562 (Universally Unique IDentifiers) — 2024-05


---

## Migration and Constraint Rules (SKILL.md excerpt)

- Use expand-contract for risky rename/type-change flows, populated `NOT NULL`, and phased deprecation. Consider pgroll for automated expand-contract with versioned schemas and data backfills. On PostgreSQL 18, use `RETURNING OLD.*` / `RETURNING NEW.*` in UPDATE/DELETE statements to verify data correctness during dual-write and backfill phases without separate SELECT queries.

- On PostgreSQL 18, use `NOT VALID` when adding CHECK, FK, or NOT NULL constraints to skip immediate validation of existing rows — validate separately with `VALIDATE CONSTRAINT` after the transaction commits to avoid long-held `ACCESS EXCLUSIVE` locks during migrations.

- On PostgreSQL 18, use virtual generated columns (now the default) for derived values — they compute on read without storing, avoiding table rewrites during schema evolution.

- On PostgreSQL 18, use temporal constraints (`PRIMARY KEY ... WITHOUT OVERLAPS`, `FOREIGN KEY ... PERIOD`) for scheduling, booking, and bitemporal schemas instead of application-level overlap checks.

- Use `UNIQUE NULLS DISTINCT` (PostgreSQL 15+) for unique constraints on nullable columns — treats each NULL as a distinct value, eliminating partial-index workarounds for optional-but-unique fields (e.g., email, external_id).
