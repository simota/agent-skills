# Schema Tenant Handoff Templates

Handoff templates used by Schema's `tenant` Recipe. Tenant isolation design (RLS policies, tenant columns, migration steps) is produced inside Schema itself, so there is no internal handoff for it; only cross-agent handoffs are listed. Tokens match the `schema/SKILL.md` handoff table.

## Receiving Handoffs

### From Gateway (API Routing Context)

```yaml
GATEWAY_TO_SCHEMA:
  source: Gateway
  content:
    api_design: "[OpenAPI spec or summary]"
    auth_method: "[JWT | session | API key]"
    current_routing: "[how tenant is currently identified]"
  request: "Design tenant-aware API routing"
```

## Sending Handoffs

### To Sentinel (Security Verification)

```yaml
SCHEMA_TO_SENTINEL:
  source: Schema
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
SCHEMA_TO_SCAFFOLD:
  source: Schema
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
