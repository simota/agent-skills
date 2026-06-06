# Shard Handoff Templates

## Receiving Handoffs

### From Schema (DB Design Context)

```yaml
SCHEMA_TO_SHARD_HANDOFF:
  source: Schema
  content:
    tables: ["[table list with key columns]"]
    relationships: ["[foreign key relationships]"]
    current_isolation: "[none | basic | full]"
    indexes: ["[existing indexes]"]
  request: "Design tenant isolation for this schema"
```

### From Gateway (API Routing Context)

```yaml
GATEWAY_TO_SHARD_HANDOFF:
  source: Gateway
  content:
    api_design: "[OpenAPI spec or summary]"
    auth_method: "[JWT | session | API key]"
    current_routing: "[how tenant is currently identified]"
  request: "Design tenant-aware API routing"
```

## Sending Handoffs

### To Schema (RLS Implementation)

```yaml
SHARD_TO_SCHEMA_HANDOFF:
  source: Shard
  destination: Schema
  content:
    isolation_strategy: "[database | schema | row-level]"
    rls_policies:
      - table: "[table name]"
        policy: "[SQL policy definition]"
        indexes_needed: ["[index definitions]"]
    tenant_column: "tenant_id UUID NOT NULL"
    migration_steps: ["[ordered migration steps]"]
  request: "Implement RLS policies and tenant columns"
```

### To Sentinel (Security Verification)

```yaml
SHARD_TO_SENTINEL_HANDOFF:
  source: Shard
  destination: Sentinel
  content:
    isolation_design: "[architecture summary]"
    leakage_assessment:
      vectors_checked: [N]
      mitigated: [N]
      open: [N]
    rls_policies: ["[policy definitions]"]
    cache_strategy: "[tenant-scoped cache design]"
  request: "Verify cross-tenant data leakage protection"
```

### To Scaffold (Infrastructure)

```yaml
SHARD_TO_SCAFFOLD_HANDOFF:
  source: Shard
  destination: Scaffold
  content:
    infrastructure_needs:
      database: "[single shared | per-tenant | hybrid]"
      connection_pooling: "[PgBouncer config if needed]"
      cache: "[Redis tenant namespace config]"
      storage: "[S3 tenant prefix config]"
    provisioning_automation: "[tenant onboarding infra needs]"
  request: "Provision tenant-aware infrastructure"
```
