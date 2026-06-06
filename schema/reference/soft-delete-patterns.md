# Soft Delete Patterns Reference

Purpose: Design logical deletion strategies that preserve data while hiding it from default queries. Compare `deleted_at` timestamp, `status` enum, and tombstone-row patterns; address foreign-key cascade, partial unique indexes, query-default-filter risk, and GDPR right-to-erasure.

## Scope Boundary

- **schema `soft-delete`**: Logical deletion patterns (this document).
- **schema `audit-log` (elsewhere)**: Records the deletion event; complements soft delete.
- **Cloak (elsewhere)**: GDPR / privacy rules; right-to-erasure pathway must coordinate.
- **Oath (elsewhere)**: Regulatory retention rules.
- **Builder (elsewhere)**: ORM-level default-scope implementation.

## Why Soft Delete (and Why Not)

| Reason for soft delete | Reason against |
|------------------------|----------------|
| Recover from accidental deletion | Storage growth |
| Maintain referential integrity | Query complexity (always filter) |
| Audit / compliance trail | ORM bug risk if default scope misses |
| Preserve historical reports | "Soft" deleted PII still exists (GDPR concern) |
| Undo functionality | Index size + cardinality |

Default to soft delete for user-facing entities (orders, accounts, content). Hard delete is fine for ephemeral data (sessions, expired tokens, OTPs).

## Three Patterns

### Pattern 1: `deleted_at TIMESTAMPTZ NULL`

```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
CREATE INDEX ix_users_active ON users (id) WHERE deleted_at IS NULL;
```

- **Pros**: Records when deletion happened; no separate column for status.
- **Cons**: Cannot represent multiple non-active states (suspended, banned).
- **Default scope**: `WHERE deleted_at IS NULL`.

### Pattern 2: `status` enum

```sql
CREATE TYPE user_status AS ENUM ('active', 'suspended', 'deleted', 'banned');
ALTER TABLE users ADD COLUMN status user_status NOT NULL DEFAULT 'active';
ALTER TABLE users ADD COLUMN status_changed_at TIMESTAMPTZ;
```

- **Pros**: Multi-state lifecycle; richer semantics.
- **Cons**: Two-step query (`status != 'deleted'`); enum migration friction.
- **Default scope**: `WHERE status NOT IN ('deleted', 'banned')` (depends on intent).

### Pattern 3: Separate tombstone table

```sql
-- Active rows in users
-- Deleted rows moved to users_deleted with same shape + deleted_at + deleted_by
```

- **Pros**: Clean active table; fast queries; archive-friendly.
- **Cons**: Cross-table queries for history; FK complexity.
- **Use when**: Volume is huge and most queries are active-only.

### Selection matrix

| Need | Choose |
|------|--------|
| Default + simple recovery | Pattern 1 (`deleted_at`) |
| Multi-state lifecycle | Pattern 2 (`status`) |
| High-volume, active-dominant | Pattern 3 (tombstone table) |
| Audit who-deleted | Pattern 1 + 2 with `deleted_by` column |
| Full event history | Pattern 1 + audit log + event sourcing if appropriate |

## Foreign Keys

Deleting parent: child handling matters.

| Strategy | Behavior on parent soft-delete |
|----------|-------------------------------|
| Cascade soft-delete | Child also gets `deleted_at` (cascade trigger or app-level) |
| Restrict | Block parent soft-delete if active children |
| Orphan | Children remain, parent set deleted (acceptable when child is independent) |
| Tombstone reference | FK still valid (the parent row exists, just marked) |

Default for soft delete: keep FKs valid. Hard cascade only on hard delete.

## Partial Unique Index

Active vs deleted rows can collide on unique constraints.

```sql
-- Wrong: blocks re-creating an account with same email after soft-delete
CREATE UNIQUE INDEX uq_users_email ON users (email);

-- Right: only enforces uniqueness on active rows
CREATE UNIQUE INDEX uq_users_email_active
  ON users (email) WHERE deleted_at IS NULL;
```

Test the migration: an old soft-deleted account with the same email shouldn't block re-registration.

## Default Scope Risk

The most common bug: forgot to filter, exposed deleted rows.

### Defenses

1. **Database view**: `CREATE VIEW users_active AS SELECT * FROM users WHERE deleted_at IS NULL;` — application reads view by default.
2. **Row-Level Security (Postgres)**: policy excludes deleted rows for app role.
3. **ORM default scope**: rails `default_scope`, Django manager, Prisma middleware.
4. **Naming convention**: `users` = active-only view, `users_all` = unfiltered table.
5. **Code review checklist**: every direct query of base table justified.

Belt-and-suspenders: combine RLS + view for defense in depth.

## GDPR Right-to-Erasure (2026-05 stance)

Soft delete preserves PII. GDPR Article 17 (right to erasure) generally requires actual erasure within one month of a valid request — the soft-delete-only model is **not compliant** for production EU/UK data. Combine soft-delete-for-UX with a scheduled hard-erasure pathway. The same posture applies under CCPA/CPRA "right to delete" (15-day acknowledge + 45-day fulfil) and Japan's APPI consent-withdrawal requests.

### Three-stage pathway

```
SOFT DELETE  →  scrub PII fields  →  HARD DELETE (after retention period)
                ↓
              audit_log records the erasure event (no PII)
```

Steps:
1. **Soft delete** with `deleted_at` set; row is invisible to the application but still recoverable for accidental-delete UX.
2. **PII scrub**: replace name, email, phone, address, IP with placeholders (`[redacted]` or null). Triggers downstream cache/search-index invalidation.
3. **Audit log**: record erasure (`subject_id_hash`, `requested_at`, `completed_at`, legal basis) — no PII.
4. **Hard delete**: after the retention-compliance overlap (financial records often 7 years; consent-withdrawal-only data should hard-delete within 30 days of the scrub).
5. **Cascading erasure**: linked tables (sessions, comments, audit log payloads with PII, embeddings, backups, search index, BI warehouse) receive the same treatment — coordinate via Cloak.

### Common 2026 violation patterns

- "We soft-deleted; that satisfies GDPR" — no, PII still exists.
- Embeddings (pgvector) of user content not scrubbed — text reconstructable from embeddings under some models; treat embeddings as PII derivatives.
- Backups untouched — document that PITR/backup retention is the legitimate-interest exception under Art. 17(3)(b), with a documented expiry window.
- Audit logs still hold PII after scrub — store only `subject_id_hash` going forward; rewrite historical audit rows with a one-shot scrub job.

### Subject ID continuity

Use a hashed subject ID in audit logs so erasure is traceable without retaining PII:

```
audit.subject_id_hash = SHA256(subject_id || HMAC_secret)
```

After PII scrub, the hash still allows verifying compliance without identifying.

## Schema Design Workflow

```
INVENTORY    →  list entities; classify which need soft delete
             →  PII flag per entity (Cloak coordination)

CHOOSE       →  per entity: deleted_at / status / tombstone
             →  audit columns (deleted_by, deleted_reason)

INDEX        →  partial unique on active subset
             →  filtered indexes for hot queries
             →  plain index on deleted_at for cleanup jobs

FK           →  cascade strategy on soft delete (typically: keep refs valid)
             →  hard delete cascade rules (separate)

DEFAULT      →  view + RLS + ORM default scope (belt-and-suspenders)
             →  naming convention if applicable

GDPR         →  PII scrub procedure
             →  retention period before hard delete
             →  audit log entries
             →  Cloak handoff for PII tagging

CLEANUP      →  scheduled hard-delete after retention
             →  archive to cold storage if regulated

VERIFY       →  unique-collision test
             →  default-scope leak test
             →  ORM N+1 / scope inheritance test
             →  GDPR walkthrough

HANDOFF      →  Cloak: PII rules
             →  Oath: retention compliance
             →  Builder: ORM scope wiring
             →  Audit-log: deletion event capture
```

## Output Template

```markdown
## Soft Delete Design: [Schema / Entity]

### Entities & Pattern Choice
| Entity | Pattern | PII? | Lifecycle |
|--------|---------|------|-----------|
| user | status enum | Yes | active → suspended → deleted |
| order | deleted_at | No | active / deleted |
| ... | ... | ... | ... |

### DDL
[ALTER TABLE statements + partial unique indexes + FK strategy]

### Default Scope
- View: [name]
- RLS: [policy]
- ORM: [default_scope / middleware]
- Naming convention: [yes/no]

### GDPR Pathway
- Stage 1 — Soft delete: [SQL/code]
- Stage 2 — PII scrub: [columns to redact, scrub script]
- Stage 3 — Audit log entry: [shape]
- Stage 4 — Hard delete after [N period]: [cleanup job]

### Cleanup Job
- Schedule: [cadence]
- Idempotent: yes
- Audit entry per cleanup batch

### Test Plan
- [ ] Re-create with same email after soft-delete works (partial unique)
- [ ] Direct base-table query rejected by RLS
- [ ] ORM default scope in place; deletion test passes
- [ ] GDPR full walkthrough: request → soft → scrub → hard → audit-only trace
- [ ] Cascade behavior on parent soft-delete

### Handoffs
- Cloak: PII tagging
- Oath: retention compliance
- Builder: ORM wiring
- audit-log: deletion event capture
- migration-rollback: reverse pathway if soft-delete column added/removed
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Plain unique index instead of partial | Use `WHERE deleted_at IS NULL` |
| ORM forgot default scope | View + RLS as backstop |
| Soft delete on PII without scrub plan | GDPR violation; design two-stage erasure |
| Boolean `is_deleted` instead of timestamp | No "when" history; use `deleted_at` |
| Hard cascade FK on soft-delete | Breaks referential integrity for child records |
| No partial index on `deleted_at IS NULL` | Hot queries scan all rows including deleted |
| Mixing soft and hard delete on same table inconsistently | Pick one default; document exceptions |
| Not testing re-create after soft-delete | Production blocks user re-registration |
| `deleted_at` without `deleted_by` | Cannot answer "who deleted this" |
| Soft delete without retention policy | Unbounded growth; never actually erased |
| GDPR right-to-erasure ignored for soft-deleted | Not compliant |
| Storing scrub-replacement as static "[deleted]" without unique handling | Conflicts with new active rows using same placeholder |

## Deliverable Contract

When `soft-delete` completes, emit:

- **Per-entity pattern choice** (deleted_at / status / tombstone) with rationale.
- **DDL** including partial unique indexes and FK strategy.
- **Default scope strategy** (view + RLS + ORM).
- **GDPR pathway** (soft → scrub → hard + audit).
- **Cleanup job** schedule.
- **Test plan** including re-create, RLS, ORM, GDPR walkthrough.
- **Handoffs**: Cloak, Oath, Builder, audit-log, migration-rollback.

## References

- Postgres — partial indexes, RLS policies
- *Database Design for Mere Mortals* — Hernandez (logical-deletion fundamentals)
- Joe Celko — *SQL for Smarties* (state machines via flags)
- GDPR Article 17 — Right to erasure
- ICO (UK) — Right to be forgotten guidance
- Rails — `default_scope` / Paranoia gem
- Django — soft-delete managers
- Prisma — middleware for soft delete
- AWS Database blog — soft-delete patterns
- *Refactoring Databases* — Ambler & Sadalage (transitional schemas)
- *Domain-Driven Design* — Evans (when soft delete is a domain concept)
