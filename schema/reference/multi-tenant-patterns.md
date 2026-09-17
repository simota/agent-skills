# Multi-Tenant Schema and Isolation Contract

Read for a multi-tenant schema or `tenant` mode. Select from isolation requirements, restore/deletion boundaries, tenant-specific DDL, workload measurements, and operating cost—not tenant-count folklore or a vendor release table.

## Isolation decision

| Pattern | Select when | Verify before accepting |
|---|---|---|
| Database per tenant | Independent restore, placement, credentials, or lifecycle is required | Router authorization, provisioning/migration fleet, backup separation, connection/cost budgets; sharing a server still shares some failure and administration boundaries. |
| Schema per tenant | Separate DDL/customization is required within a shared database | Qualified identifiers, schema privileges, trusted `search_path`, migration fan-out, pool reuse, restore limitations. A schema name alone is not authorization. |
| Shared tables + RLS | Uniform schema and shared operation are acceptable | Every tenant-bearing read/write path, application role, policy composition, cross-tenant relationships and pool context. |
| Shared tables + tenant partitioning + RLS | Measured locality/maintenance needs justify partitions | Partition pruning is a performance mechanism, not isolation. Keep authorization/RLS and measure plans with representative tenants. |

No pattern by itself proves regulatory compliance. Pin applicable controls with Canon. Verify selected managed-engine features and pricing against its current official documentation; no database/model/version mandate is implied here.

## RLS and transaction context

- Every tenant-bearing table needs an explicit isolation policy. Enable RLS; use `FORCE ROW LEVEL SECURITY` where owner bypass must be prevented. The runtime role must not be superuser, `BYPASSRLS`, or an uncontrolled owner/definer role. FORCE does not constrain superusers or BYPASSRLS.
- Authenticate the principal and authorize its tenant membership before setting context. A header, subdomain, URL, JWT claim without signature/audience checks, or UUID obscurity is not authorization. Reject inconsistent tenant sources.
- Set context **inside the same transaction and connection as all tenant queries**, using the project's existing context key. Example binding, not a complete migration:

```sql
BEGIN;
SELECT set_config('app.current_tenant_id', $1, true);
-- $1 is the authenticated/authorized tenant ID, bound by the driver.
-- Execute all tenant reads/writes on this transaction's connection.
COMMIT;
```

- `true` makes the setting transaction-local. Never rely on a session-scoped `SET` or another pooled connection. Test commit, rollback, errors, cancellation and reuse; prohibit session defaults that restore a previous tenant. Missing/invalid context must deny or error, never select a fallback tenant.
- A representative predicate is `tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid`. Verify both read visibility (`USING`) and proposed writes (`WITH CHECK`) for the actual commands. Keep the existing project key rather than renaming it from this example.
- An application-set GUC does **not** defend against an attacker who can execute arbitrary SQL with that application's credentials and set another tenant. Document this trust boundary; use stronger independently enforced roles/credentials when required.
- Review every permissive policy's OR composition, restrictive policies, views, SECURITY DEFINER functions, maintenance roles and cross-tenant analytics paths. RLS does not cover every operation: TRUNCATE and REFERENCES are not filtered by row policies.
- On versions supporting security-invoker views, verify caller-policy behavior explicitly. Never substitute an unverified auth helper for tenant identity (a user ID is not a tenant ID).

## Relational integrity and migration

- Tenant-owned relationships include `tenant_id` on both sides. A composite foreign key `(tenant_id, order_id)` requires a matching unique/primary key `(tenant_id, id)` on the parent; global IDs alone do not enforce same-tenant ownership.
- Design indexes from actual predicates and plans. Tenant-leading indexes often help scoped queries; neither UUIDs nor putting `tenant_id` first in every index proves authorization or index-only scans.
- For schema routing, derive the schema from an authorized mapping and quote identifiers through the driver. Exclude untrusted writable schemas from `search_path`; verify prepared statements and pool reuse cannot retain the previous tenant's resolution.
- Existing rows need an approved tenant mapping and staged backfill before NOT NULL, FK validation and enforcement. Do not copy `ADD tenant_id NOT NULL` onto populated tables or assume a global uniqueness constraint becomes tenant-scoped automatically.
- Prove no cross-tenant reads/writes before cutover, reconcile tenant-by-tenant counts/checksums, retain a reversible cutover window, and obtain explicit authorization before destructive consolidation or deprovisioning. A guessed calendar duration is not a migration plan.
- Detailed lifecycle/rollback → `reference/tenant-migration.md` and `reference/tenant-provisioning.md`; runtime quotas/fairness/overage contracts → `reference/tenant-quota-throttling.md`. Do not duplicate their limits here.

## Leakage verification matrix

| Surface | Required negative test |
|---|---|
| Reads/joins/aggregates | Tenant A cannot observe B through ID lookup, joins, counts, views, export, or shared reporting. |
| Insert/update/upsert/delete | A cannot create or move a relationship/row into B; test both old-row visibility and new-row checks. |
| Pool/context | Alternate A/B, missing context, rollback/error/cancel, and concurrent requests; no inherited identity. |
| Caches/search/files | Tenant namespace plus actual access enforcement; cached responses, search results and signed URLs cannot cross tenants. |
| Jobs/webhooks | Reauthorize tenant context at execution/delivery, including retries; never trust a copied payload as authorization. |
| Logs/errors/audit | No other tenant's data in errors/logs; scoped access, redaction and audit provenance are exercised. |
| Backup/restore/admin | Authorized cross-tenant administration is explicit; a tenant restore/export excludes others. |

Deliver: selected pattern and rejected alternatives, tenant identity authority, DDL/policy/index plan, routing/context protocol, negative-test evidence, migration/rollback boundary, and named unverified surfaces. A checklist assertion without executed evidence is not a passed isolation test.

## Canonical specification

Checked 2026-09-17; select the deployed PostgreSQL version, not necessarily `current`.
- https://www.postgresql.org/docs/current/ddl-rowsecurity.html — policy composition, bypass roles, command coverage.
- https://www.postgresql.org/docs/current/functions-admin.html — `current_setting` and transaction-local `set_config`.
- https://www.postgresql.org/docs/current/ddl-schemas.html — schema privileges and trusted search paths.
