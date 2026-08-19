# Shard Multi-Tenant Design Patterns

> **2026 default for new PostgreSQL SaaS: shared tables + RLS + `set_config` in transaction mode.** The 2026 PostgreSQL community guidance has consolidated around three points: (1) **Row-Level Security** is the right balance of simplicity + safety for most workloads, adding only `~2-4%` overhead on properly-indexed tenant columns — over 100x slower without an index on the tenant column ([Supabase RLS Performance & Best Practices](https://supabase.com/docs/guides/troubleshooting/rls-performance-and-best-practices-Z5Jjwv)); (2) **PgBouncer in transaction mode** is the baseline pooler for self-hosted deployments, but **Supavisor** (Supabase's Elixir-based cloud-native pooler, open-source) is now the recommended option for serverless/edge workloads and natively handles per-tenant pool isolation at scale ([Supavisor: Scaling Postgres to 1 Million Connections](https://supabase.com/blog/supavisor-1-million)); in either pooler, the tenant context must be set with **transaction-scoped `set_config(...)`** (NOT session-scoped `SET`) so the next request on the same pooled connection cannot inherit the previous tenant's context — this is the single most common multi-tenant data-leak in 2026 audits; (3) **Citus 13** (PostgreSQL 17 support, available as elastic clusters preview on Azure Database for PostgreSQL – Flexible Server as of 2024-11) is the right tool when row-count or write-volume exceeds what a single PG node handles, with schema-based or distributed-table sharding ([What's new with Postgres at Microsoft, 2025 edition](https://techcommunity.microsoft.com/blog/adforpostgresql/whats-new-with-postgres-at-microsoft-2025-edition/4410710)); (4) **Neon** enables database-per-tenant at scale via its project-per-tenant API, managing 300K+ isolated Postgres databases with copy-on-write branching for dev/staging ([Multitenancy with Neon](https://neon.tech/docs/guides/multitenancy)). See `tenant-quota-throttling.md` for the noisy-neighbor controls that pair with these choices.

## Isolation Strategies

### Database-per-Tenant

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Tenant A │  │ Tenant B │  │ Tenant C │
│   DB     │  │   DB     │  │   DB     │
└──────────┘  └──────────┘  └──────────┘
      ↑              ↑              ↑
      └──────────────┼──────────────┘
                     │
            ┌────────────────┐
            │ Connection Pool│
            │   Router       │
            └────────────────┘
```

**Pros:** Strongest isolation, per-tenant backup/restore, compliance-ready
**Cons:** High infra cost, complex provisioning, cross-tenant queries difficult
**Best for:** <100 tenants, regulated industries (HIPAA, PCI-DSS)

### Schema-per-Tenant

```
┌─────────────────────────────┐
│         Single Database      │
│  ┌─────────┐ ┌─────────┐   │
│  │Schema A │ │Schema B │ … │
│  │ tables  │ │ tables  │   │
│  └─────────┘ └─────────┘   │
└─────────────────────────────┘
```

**Pros:** Good isolation, shared infra cost, per-tenant migrations possible
**Cons:** Schema proliferation, connection management complexity
**Best for:** 10-1,000 tenants, moderate customization needs

### Row-Level Security (RLS)

```
┌────────────────────────────────────┐
│          Single Database            │
│  ┌──────────────────────────────┐  │
│  │      Shared Tables           │  │
│  │  tenant_id | data | ...      │  │
│  │  ─────────────────────────   │  │
│  │  RLS Policy: WHERE           │  │
│  │  tenant_id = current_tenant  │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

**Pros:** Low cost, simple ops, easy cross-tenant analytics
**Cons:** Requires careful RLS design, noisy neighbor risk
**Best for:** 1,000+ tenants, standard data sensitivity

## RLS Implementation Patterns

### PostgreSQL RLS

```sql
-- Enable RLS on table
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- Create policy (fail-closed: denies unless policy allows)
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- Force RLS for table owner too
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

-- CRITICAL: Index the tenant column — without this RLS causes sequential scans
CREATE INDEX idx_orders_tenant_id ON orders USING btree (tenant_id);
```

**Setting tenant context safely under PgBouncer/Supavisor transaction mode (2026 mandatory pattern):**

```sql
-- WRONG: session-scoped — leaks across pooled connections in transaction mode
SET app.current_tenant = 'tenant-uuid-here';

-- CORRECT: transaction-scoped — cleared at COMMIT / ROLLBACK, safe under any pooler
BEGIN;
SELECT set_config('app.current_tenant', 'tenant-uuid-here', true);  -- `true` = local to transaction
-- ... queries ...
COMMIT;
```

The `true` third argument to `set_config` scopes the GUC to the transaction. Without it, a future request on the same pooled connection inherits the previous tenant's context — the most common 2026 multi-tenant data-leak pattern. Treat any RLS code that uses bare `SET app.current_tenant` under pooler transaction mode as a `Sev-1` security finding.

**Performance optimization — wrap auth functions to avoid per-row evaluation (PostgreSQL 15+):**

```sql
-- SLOWER: function evaluated per row
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = auth.uid());

-- FASTER: wrapping causes initPlan — function result cached per statement
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = (SELECT auth.uid()));
```

**Security invoker views (PostgreSQL 15+):** Use `security_invoker = true` on views over RLS-protected tables so the RLS policies of the caller (not the view owner) are applied, preventing privilege escalation through views.

```sql
CREATE VIEW tenant_orders WITH (security_invoker = true) AS
  SELECT * FROM orders;
```

Source: [PostgreSQL docs — Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html), [Supabase RLS Performance & Best Practices](https://supabase.com/docs/guides/troubleshooting/rls-performance-and-best-practices-Z5Jjwv), [pganalyze: RLS, security invoker views, and LEAKPROOF functions](https://pganalyze.com/blog/5mins-postgres-row-level-security-bypassrls-security-invoker-views-leakproof-functions)

### Application-Level RLS (ORM)

```typescript
// Middleware: extract and set tenant context
function tenantMiddleware(req, res, next) {
  const tenantId = extractTenantId(req); // from JWT, header, or subdomain
  req.tenantId = tenantId;
  next();
}

// Repository: always scope queries
class OrderRepository {
  async findAll(tenantId: string) {
    return this.db.orders.findMany({
      where: { tenant_id: tenantId } // Never omit this
    });
  }
}
```

## Tenant Routing Patterns

### Subdomain Routing

```
tenant-a.app.com → tenant_id = "tenant-a"
tenant-b.app.com → tenant_id = "tenant-b"
```

**Pros:** Clean URLs, tenant branding possible
**Cons:** SSL wildcard cert needed, DNS management

### Header Routing

```
GET /api/orders
X-Tenant-ID: tenant-uuid
```

**Pros:** Simple, works with any domain
**Cons:** Easy to forget header, needs middleware enforcement

### JWT Claim Routing

```json
{
  "sub": "user-id",
  "tenant_id": "tenant-uuid",
  "role": "admin"
}
```

**Pros:** Authenticated by default, no extra header
**Cons:** Tenant switch requires new token

### Path Routing

```
/api/tenants/{tenant_id}/orders
```

**Pros:** Explicit, RESTful
**Cons:** Verbose URLs, tenant_id in every route

## Noisy Neighbor Protection

### Rate Limiting per Tenant

```yaml
rate_limits:
  default:
    requests_per_minute: 100
    burst: 20
  premium:
    requests_per_minute: 1000
    burst: 100
  enterprise:
    requests_per_minute: 10000
    burst: 500
```

### Resource Quotas

| Resource | Measurement | Default limit |
|----------|------------|---------------|
| Storage | MB per tenant | 1,000 MB |
| API calls | Per minute | 100 |
| Concurrent connections | Active | 10 |
| Background jobs | Per hour | 50 |
| File uploads | Per day | 100 |

### Fair Scheduling

```
Priority Queue per Tenant:
1. Calculate tenant's fair share (1/N of total capacity)
2. If tenant exceeds fair share, deprioritize their requests
3. If tenant is under fair share, prioritize their requests
4. Never fully block any tenant (minimum guaranteed throughput)
```

## Data Leakage Checklist

| Vector | Check | Mitigation |
|--------|-------|------------|
| Missing WHERE clause | All queries include tenant_id | RLS at DB level as safety net |
| Join leakage | Cross-table joins respect tenant boundary | RLS on all joined tables |
| Aggregate leakage | COUNT/SUM don't cross tenants | RLS + application filter |
| Cache leakage | Cache keys include tenant_id | `cache:{tenant_id}:{key}` pattern |
| Log leakage | Logs don't expose other tenants' data | Tenant-scoped log contexts |
| Error leakage | Errors don't reveal other tenants | Generic error messages |
| Search leakage | Search indexes are tenant-scoped | Tenant filter in search queries |
| File storage leakage | File paths include tenant namespace | `/{tenant_id}/files/` prefix |
| Background job leakage | Jobs process correct tenant data | Tenant context in job payload |
| Webhook leakage | Webhooks route to correct tenant | Tenant validation on delivery |
