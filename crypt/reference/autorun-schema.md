# Crypt — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Crypt-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Crypt
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    design_type: "[encryption | signature | password | key-management | e2ee | tls | audit | pqc]"
    parameters:
      algorithms: ["[algorithm list]"]
      key_sizes: ["[key size list]"]
      compliance: "[FIPS | NIST | standard]"
      anti_patterns_found: [N]
      quantum_vulnerable: [N components]
      libraries: ["[recommended libraries]"]
  Next: Builder | Sentinel | Cloak | Scaffold | DONE
  Reason: [Why this next step]
```
