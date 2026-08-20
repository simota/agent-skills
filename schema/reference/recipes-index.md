# Schema Recipe Registry

The full Recipe table for `schema`. `schema/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| Schema Design | `design` | ✓ | New table or entity design | `reference/schema-examples.md` |
| Migration Plan | `migration` | | Schema change and migration design | `reference/migration-patterns.md` |
| ER Diagram | `er` | | ER diagram generation and review | `reference/schema-examples.md` |
| Normalization | `normalize` |  | Normalization vs denormalization decisions | — |
| Index Strategy | `index` | | Index design and optimization | `reference/index-strategies.md` |
| Migration Rollback | `rollback` | | Reverse-operation design for destructive migrations (reverse DDL / dual-write / backfill / alternatives to destructive changes) | `reference/migration-rollback.md` |
| Multi-Tenant Design | `tenant` | | Tenant isolation, RLS, routing, migration, provisioning, quota, or cross-tenant security; select `isolation|rls|routing|scale|migration|provisioning|quota` mode from the request | `reference/multi-tenant-patterns.md`, matching `reference/tenant-*.md` |
| Partitioning | `partition` | | range / list / hash / time-based partition design (pruning / maintenance / migration) | `reference/partition-strategies.md` |
| Audit Log | `audit-log` | | Append-only audit-log schema — temporal tables, logical replication, before/after image, retention | `reference/audit-log-schema.md` |
| Event Sourcing | `event-sourcing` | | Event store schema — events / projections / snapshots / outbox, aggregate boundaries | `reference/event-sourcing-schema.md` |
| Soft Delete | `soft-delete` | | Logical deletion patterns (deleted_at / status / tombstone) with GDPR right-to-erasure interaction | `reference/soft-delete-patterns.md` |
