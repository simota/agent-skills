# Audit Log Schema Reference

Purpose: Design append-only audit-log tables that record who did what, when, and to what — with before/after images, correlation IDs, retention policy, and tamper-evidence. Used for compliance (SOC2 / HIPAA / PCI-DSS / GDPR), security forensics, and operational debugging.

## Scope Boundary

- **schema `audit-log`**: Append-only audit table design (this document).
- **schema `event-sourcing` (elsewhere)**: Event store as system-of-record (different intent).
- **Cloak (elsewhere)**: PII handling rules; audit logs that contain PII inherit Cloak constraints.
- **Oath (elsewhere)**: Regulatory mapping (SOC2 CC7.2 / HIPAA §164.312(b) / PCI-DSS 10).
- **Beacon (elsewhere)**: Operational logs (different from audit logs).
- **Vigil (elsewhere)**: Detection rules over audit logs.

## Audit Log vs Other Logs

| Log type | Purpose | Mutability | Retention |
|----------|---------|------------|-----------|
| Application log | Debug, performance | Mutable in storage tier | Days-weeks |
| Audit log | Compliance, forensics | **Append-only** | Months-years |
| Event log (event sourcing) | System of record | Append-only | Forever |
| Operational metrics | SLO, alerting | Mutable aggregations | Weeks-months |

Audit logs MUST be append-only at the schema/storage level — never UPDATE, never DELETE.

## Core Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `audit_id` | UUID v7 | Yes | Time-sortable; primary key |
| `occurred_at` | TIMESTAMPTZ | Yes | Server-side `now()` at write |
| `actor_type` | enum | Yes | `user` / `service` / `system` / `anonymous` |
| `actor_id` | TEXT | Yes | User ID, service name, or `null` for anonymous |
| `actor_ip` | INET | Recommended | Client IP if applicable |
| `actor_user_agent` | TEXT | Optional | UA string |
| `action` | TEXT | Yes | Verb-led (`user.create`, `payment.refund`) |
| `target_type` | TEXT | Yes | Resource type (`user`, `payment`, `tenant`) |
| `target_id` | TEXT | Yes | Resource id |
| `before_image` | JSONB | Conditional | Old state for UPDATE/DELETE; null for CREATE |
| `after_image` | JSONB | Conditional | New state for CREATE/UPDATE; null for DELETE |
| `result` | enum | Yes | `success` / `failure` / `denied` |
| `failure_reason` | TEXT | Conditional | Required when result != success |
| `correlation_id` | UUID | Recommended | Trace ID for stitching across services |
| `request_id` | UUID | Recommended | HTTP request boundary |
| `session_id` | UUID | Optional | Auth session |
| `tenant_id` | TEXT | Conditional | Required for multi-tenant systems |
| `metadata` | JSONB | Optional | Extension fields per action |
| `prev_hash` | BYTEA | Optional | Tamper-evidence chain (HMAC) |
| `row_hash` | BYTEA | Optional | HMAC of canonicalized row |

## Schema (Postgres example)

```sql
CREATE TYPE audit_actor_type AS ENUM ('user', 'service', 'system', 'anonymous');
CREATE TYPE audit_result    AS ENUM ('success', 'failure', 'denied');

CREATE TABLE audit_log (
  audit_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  occurred_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  actor_type      audit_actor_type NOT NULL,
  actor_id        TEXT,
  actor_ip        INET,
  actor_user_agent TEXT,
  action          TEXT NOT NULL,
  target_type     TEXT NOT NULL,
  target_id       TEXT NOT NULL,
  before_image    JSONB,
  after_image     JSONB,
  result          audit_result NOT NULL,
  failure_reason  TEXT,
  correlation_id  UUID,
  request_id      UUID,
  session_id      UUID,
  tenant_id       TEXT,
  metadata        JSONB,
  prev_hash       BYTEA,
  row_hash        BYTEA
)
PARTITION BY RANGE (occurred_at);

-- Monthly partition example
CREATE TABLE audit_log_2026_04 PARTITION OF audit_log
  FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');

-- Indexes
CREATE INDEX ix_audit_actor   ON audit_log (actor_type, actor_id, occurred_at DESC);
CREATE INDEX ix_audit_target  ON audit_log (target_type, target_id, occurred_at DESC);
CREATE INDEX ix_audit_action  ON audit_log (action, occurred_at DESC);
CREATE INDEX ix_audit_corr    ON audit_log (correlation_id) WHERE correlation_id IS NOT NULL;
CREATE INDEX ix_audit_tenant  ON audit_log (tenant_id, occurred_at DESC) WHERE tenant_id IS NOT NULL;

-- Append-only enforcement
REVOKE UPDATE, DELETE ON audit_log FROM PUBLIC;
-- Only allow INSERT for application role; admin/superuser cannot UPDATE/DELETE without explicit grant
```

## Capture Strategies

### 1. Application-layer (recommended default)

App emits audit events as part of the same transaction as the business write.

- **Pros**: full business context, easy to add metadata.
- **Cons**: discipline required; missed sites = audit gaps.
- **Pattern**: middleware or aspect layer that wraps mutating calls.

### 2. Database trigger-based

`AFTER INSERT/UPDATE/DELETE` triggers populate audit table.

- **Pros**: cannot be bypassed; works for any client.
- **Cons**: limited business context (no actor / IP unless set as session var); migration-heavy.
- **Pattern**: `current_setting('app.actor_id')` set per session.

### 3. CDC / logical replication (Debezium)

Read WAL → topic → audit consumer → audit table.

- **Pros**: zero app overhead; eventually consistent.
- **Cons**: eventually consistent; dual storage cost; delete-before-CDC race.
- **Pattern**: Stream agent owns the pipeline.

### 4. Postgres temporal tables / SQL:2011

System-period temporal tables (SQL:2011-style) automatically maintain history.

- **PostgreSQL 18 status (2026-05)**: built-in `PRIMARY KEY ... WITHOUT OVERLAPS` and `FOREIGN KEY ... PERIOD` cover **application-time / valid-time**. **System-time / transaction-time** (`FOR SYSTEM_TIME AS OF`) is **not yet built in** — community proposals are in review for PG 19. Today, approximate with a `recorded_at` / `invalidated_at` pair plus an append-only audit table.
- **Pros**: standards-aligned; valid-time uniqueness no longer needs `EXCLUDE USING gist`.
- **Cons**: less explicit actor context; transaction-time half still DIY.

### Selection matrix

| Need | Choose |
|------|--------|
| Business action context (refund-by-actor) | Application-layer |
| Compliance "all writes captured" | Trigger-based or CDC |
| Cross-service distributed audit | Application-layer + correlation_id |
| Time-travel queries | Temporal tables |

Combine app-layer + trigger-based as belt-and-suspenders for high-stakes systems.

## Retention & WORM

| Compliance | Min retention |
|-----------|---------------|
| SOC2 | 1 year (some auditors require longer) |
| HIPAA | 6 years |
| PCI-DSS | 1 year (3 months online + 1 year archive) |
| GDPR | proportional to processing purpose; typically 1-3 years |
| SOX | 7 years |

WORM (Write-Once-Read-Many) options:
- AWS S3 Object Lock (Compliance mode).
- Azure Immutable Blob Storage.
- GCS Bucket Lock.
- Postgres partitioning + revoke modify on closed partitions + tape/cold storage.

## Tamper Evidence (Hash Chain / Merkle Tree)

For high-trust contexts (financial, healthcare, government, KYC) the 2026 baseline is:

### Linear HMAC chain (simplest)

```
row_hash_n  = HMAC(secret, canonicalize(row_n))
prev_hash_n = HMAC(secret, row_hash_{n-1})

-- Verification: walk the chain, recompute, compare.
```

- Pros: cheap to compute, append-only friendly.
- Cons: O(N) verification; one-row corruption forces full re-verify.

### Merkle tree per partition (current best practice for high-volume audit logs)

Bucket rows by partition (daily / hourly), compute a Merkle root per bucket, store the root in a separate immutable `audit_merkle_roots` table.

```sql
CREATE TABLE audit_merkle_roots (
  bucket_start TIMESTAMPTZ PRIMARY KEY,
  root_hash    BYTEA       NOT NULL,
  leaf_count   BIGINT      NOT NULL,
  anchored_at  TIMESTAMPTZ,
  anchor_ref   TEXT       -- TSA token / S3 Object Lock id / chain tx hash
);
```

- O(log N) verification for any single row.
- A corrupted row invalidates only the affected leaf path, not the whole log.
- Common pattern in 2025–2026 fintech / KYC stacks; aligns with how AWS QLDB (deprecated 2024-07; AWS recommends Aurora PostgreSQL with verifiable hash chains as the replacement) modelled the journal.

### External anchoring (independent third party)

Periodically (hourly / daily) commit the latest root hash to:
- **RFC 3161 Time-Stamp Authority** — lightweight, accepted by most regulators (eIDAS in EU, JIPDEC in JP).
- **S3 Object Lock (Compliance mode)** cross-region copies — same provider but enforced retention.
- **Public blockchain anchoring** (e.g., OpenTimestamps over Bitcoin) — heavy but maximum independence; usually reserved for KYC/AML systems.

## PII Handling

Audit logs often contain PII (names, emails, IP). Coordinate with Cloak:
- Explicit PII fields: tag at schema level.
- Pseudonymize where possible (hashed user_id).
- For GDPR right-to-erasure: replace PII with placeholder, keep audit row + reference; do NOT delete audit rows.
- Region-pinning: keep EU subjects' audit data in EU region.

## Workflow

```
INVENTORY     →  list mutating actions to audit (CRUD on critical entities)
              →  classify: PII / financial / config / auth / admin

CHOOSE        →  capture strategy (app / trigger / CDC / temporal)
              →  partitioning (monthly default for high-volume)

DESIGN        →  fields per row (use core 19 fields above + per-domain extensions)
              →  before/after image granularity (full row / changed-cols only / event-shaped)

GUARD         →  REVOKE UPDATE/DELETE
              →  WORM / immutable storage
              →  hash chain if regulatory or tamper concern

INDEX         →  by actor / target / correlation / tenant + time-DESC
              →  partition pruning verified

RETAIN        →  partition rotation + cold archive
              →  legal-hold mechanism

CLOAK         →  PII tagging + GDPR erasure pathway
              →  region pinning for sovereignty

VERIFY        →  inject synthetic audit events; verify capture
              →  retention policy applies
              →  attempt UPDATE/DELETE → must fail

HANDOFF       →  Oath: regulatory mapping
              →  Cloak: PII rules
              →  Beacon: operational log separation
              →  Vigil: detection rules over audit
              →  Stream: CDC pipeline if chosen
              →  Builder: middleware / triggers
```

## Output Template

```markdown
## Audit Log Schema: [System / Tenant]

### Inventory
| Action | Entity | PII? | Strategy |
|--------|--------|------|----------|
| user.create | user | Yes | app + trigger |
| payment.refund | payment | No | app |
| ... | ... | ... | ... |

### Schema
[DDL]

### Capture Strategy
- **Default**: [app-layer / trigger / CDC / temporal]
- **Combined?**: [yes/no, rationale]

### Append-Only Guards
- [ ] REVOKE UPDATE/DELETE
- [ ] WORM tier configured
- [ ] Hash chain (if applicable)

### Retention
- **Online**: [N months]
- **Archive**: [N years]
- **WORM**: [yes/no, mechanism]
- **Legal hold**: [process]

### PII Handling
- Tagged fields: [list]
- GDPR erasure pathway: [pseudonymize / placeholder]
- Region pinning: [yes/no]

### Indexing & Partitioning
- Partition: [monthly by occurred_at]
- Indexes: [list]

### Verification Plan
- [ ] Synthetic events captured
- [ ] Retention auto-rotation
- [ ] UPDATE/DELETE attempts fail

### Handoffs
- Oath: SOC2/HIPAA/PCI mapping
- Cloak: PII rules
- Beacon: log separation
- Vigil: detection rules
- Stream: CDC pipeline
- Builder: middleware
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Writing audit log via UPDATE | Audit table append-only; UPDATE breaks integrity |
| Soft-deleting audit rows | Audit logs cannot be deleted; use retention rotation |
| Storing actor as just "name" | Use stable actor_id; name changes |
| No correlation_id | Cannot trace across services |
| before_image and after_image as TEXT | Use JSONB for queryability |
| Same table as application data | Mixes mutable/immutable; separate concern |
| No partitioning | Single huge table; no pruning |
| App-only capture without trigger fallback | Bypass via direct DB access leaves no trace |
| PII in audit without tagging | Cloak / GDPR violation risk |
| No append-only privilege | Anyone with write access can rewrite history |
| No retention policy | Unbounded growth + compliance risk |
| Audit log shares connection pool with app | Audit failures shouldn't block business |

## Deliverable Contract

When `audit-log` completes, emit:

- **Inventory** of audited actions with PII flag.
- **Schema DDL** with append-only guards.
- **Capture strategy** with rationale.
- **Retention + WORM** plan.
- **PII handling** + GDPR erasure pathway.
- **Index + partitioning** strategy.
- **Verification plan**.
- **Handoffs**: Oath, Cloak, Beacon, Vigil, Stream, Builder.

## References

- SQL:2011 — System-Period Temporal Tables
- PostgreSQL — pg_audit extension, temporal_tables extension
- AWS S3 Object Lock — Compliance mode (WORM)
- NIST SP 800-92 — Guide to Computer Security Log Management
- ISO/IEC 27037 — Identification, collection, acquisition of digital evidence
- RFC 3161 — Time-Stamp Protocol (TSP)
- Debezium — CDC connector documentation
- Martin Fowler — *Audit Log* pattern
- O'Reilly — *Designing Data-Intensive Applications* (audit + change-data chapters)
- SOC2 CC7.2, HIPAA §164.312(b), PCI-DSS Requirement 10
