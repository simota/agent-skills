# Shard Examples

## Example 1: SaaS Multi-Tenant Architecture (RLS)

### Requirements

```yaml
tenant_count: 500 (projected: 5,000 in 2 years)
compliance: SOC2
data_sensitivity: standard
customization: low (same schema for all)
budget: startup (cost-sensitive)
```

### Recommended Strategy: Row-Level Security

**Rationale:** Tenant count (500→5,000) and standard data sensitivity favor RLS. SOC2 is achievable with proper RLS + audit logging. Cost is minimal compared to schema/DB-per-tenant.

### Architecture

```
Client → CDN → Load Balancer
  → API Server (tenant context from JWT)
    → PostgreSQL (RLS enforced)
    → Redis (tenant-scoped cache keys)
    → S3 (tenant-prefixed paths)
```

### Implementation Spec

```sql
-- 1. Add tenant_id to all tables
ALTER TABLE orders ADD COLUMN tenant_id UUID NOT NULL;
ALTER TABLE products ADD COLUMN tenant_id UUID NOT NULL;

-- 2. Create indexes
CREATE INDEX idx_orders_tenant ON orders(tenant_id);
CREATE INDEX idx_products_tenant ON products(tenant_id);

-- 3. Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_orders ON orders
  USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- 4. Audit logging
CREATE TABLE tenant_audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL,
  action TEXT NOT NULL,
  table_name TEXT NOT NULL,
  record_id UUID,
  changed_by UUID,
  changed_at TIMESTAMPTZ DEFAULT now(),
  old_values JSONB,
  new_values JSONB
);
```

### Leakage Assessment

| Vector | Status | Notes |
|--------|--------|-------|
| Missing WHERE | Mitigated | RLS enforced at DB level |
| Join leakage | Mitigated | RLS on all tables |
| Cache leakage | Mitigated | `cache:{tenant_id}:*` pattern |
| Log leakage | Mitigated | Structured logging with tenant context |
| Search leakage | Open | Need tenant filter in Elasticsearch |

## Example 2: Enterprise Migration (Single → Multi-Tenant)

### Current State

- Single-tenant Rails app
- PostgreSQL without tenant_id columns
- 1 database per customer (12 customers)

### Migration Plan

```
Phase 1: Add tenant_id (2 weeks)
  - Add nullable tenant_id to all tables
  - Backfill from database name mapping
  - Add indexes

Phase 2: Application layer (3 weeks)
  - Add tenant middleware
  - Scope all queries with tenant_id
  - Update tests

Phase 3: Enable RLS (1 week)
  - Enable RLS policies
  - Test with production data copy
  - Verify no leakage

Phase 4: Consolidate (2 weeks)
  - Migrate data from 12 DBs to 1
  - Switch DNS
  - Decommission old databases
```

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Data leakage during migration | Medium | Critical | Shadow mode: run old + new in parallel |
| Performance degradation | Low | High | Index optimization, query plan analysis |
| Missing tenant_id in queries | Medium | Critical | RLS as safety net + code audit |
