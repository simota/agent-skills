# Shard — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Shard-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Shard
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    design_type: "[full-strategy | rls-design | routing | noisy-neighbor | migration | billing | security-assessment]"
    parameters:
      isolation_level: "[database-per-tenant | schema-per-tenant | row-level | hybrid]"
      tenant_scale: "[current] -> [projected]"
      compliance: "[HIPAA | SOC2 | PCI-DSS | standard]"
      rls_policy: "[fail-closed | query-filter | hybrid]"
      routing: "[subdomain | header | path | jwt-claim]"
      leakage_vectors: [N assessed]
  Next: Schema | Scaffold | Builder | Sentinel | DONE
  Reason: [Why this next step]
```
