# Schema Reference Index

Every `reference/` file `schema` owns, and the condition that makes it worth
reading. `schema/SKILL.md` keeps only the shared-contract rows and a pointer here.

**Read this when** you need a reference and the Recipe registry did not already
name it, or when scanning what this skill can consult at all.

---

| File | Read this when... |
|------|-------------------|
| `reference/index-strategies.md` | Choosing index type, column order, partial indexes, or monitoring queries. |
| `reference/migration-patterns.md` | Safe migration sequencing, expand-contract, or framework migration commands. |
| `reference/schema-examples.md` | Concrete schema, migration, ORM, or ER diagram examples. |
| `reference/schema-design-anti-patterns.md` | Reviewing table structure, constraints, naming, or data-type choices. |
| `reference/data-modeling-anti-patterns.md` | Evaluating EAV, polymorphic relations, denormalization, or temporal design. |
| `reference/migration-deployment-anti-patterns.md` | Planning a risky migration, zero-downtime rollout, or rollback strategy. |
| `reference/index-performance-anti-patterns.md` | Reviewing composite indexes, bloat, FK indexes, or index health. |
| `reference/postgresql18-features.md` | On PostgreSQL 18 (GA 2025-09-25) and need UUIDv7, virtual generated columns (default), temporal `WITHOUT OVERLAPS` / `PERIOD`, `RETURNING OLD.*`/`NEW.*`, B-tree skip scan, async I/O, OAuth, or DDL replication. |
| `reference/postgresql17-features.md` | On PostgreSQL 17 and need SQL/JSON (`JSON_TABLE`, `JSON_VALUE`, `JSON_QUERY`, `JSON_EXISTS`), `SPLIT`/`MERGE PARTITION`, logical-replication failover, or `pg_createsubscriber`. Legacy reference — see `postgresql18-features.md` for current release. |
| `reference/multi-tenant-patterns.md` | Designing a multi-tenant schema (database/schema/shared-schema with RLS). |
| `reference/tenant-architecture-patterns.md` | Selecting isolation, RLS, routing, or noisy-neighbor controls for `tenant` mode. |
| `reference/tenant-migration.md` | Rebalancing tenants or upgrading isolation level with zero-downtime cutover and rollback. |
| `reference/tenant-provisioning.md` | Designing idempotent onboarding, reprovisioning, and deprovisioning lifecycle. |
| `reference/tenant-quota-throttling.md` | Designing fair-share quotas, burst budgets, overage signals, and billing handoffs. |
| `reference/tenant-handoffs.md` | Emitting tenant-specific handoffs to Builder, Scaffold, Sentinel, or Gateway. |
| `reference/advanced-patterns.md` | Event sourcing schema, CQRS projections, pgvector/AI schema, or bitemporal design. |
| `reference/migration-rollback.md` | Designing reverse-operation DDL, dual-write windows, backfill scripts, or destructive-change alternatives (`rollback` recipe). |
| `reference/partition-strategies.md` | Designing range/list/hash/time-based partitioning, pruning, maintenance, or staged migration from existing tables (`partition` recipe). |
| `reference/audit-log-schema.md` | Designing append-only audit-log tables — actor/action/before-after image, retention, WORM, HMAC chain (`audit-log` recipe). |
| `reference/event-sourcing-schema.md` | Designing event store, projections, snapshots, outbox pattern, or aggregate boundaries (`event-sourcing` recipe). |
| `reference/soft-delete-patterns.md` | Designing logical deletion (deleted_at / status / tombstone), partial unique indexes, FK cascade, or GDPR right-to-erasure pathway (`soft-delete` recipe). |
| `reference/autorun-schema.md` | Emitting the AUTORUN `_STEP_COMPLETE` block — Schema-specific Output/Next schema. |
| `_common/OPUS_5_AUTHORING.md` | Sizing the schema/migration spec, deciding adaptive thinking depth at PLAN, or front-loading DB version/multi-tenant flag at AUDIT. Critical for Schema: P3, P5. |
