# Gateway — AUTORUN `_STEP_COMPLETE` Schema

See `_common/AUTORUN.md` for the protocol (`_AGENT_CONTEXT` input, mode semantics, error handling).

Gateway-specific `_STEP_COMPLETE.Output` schema:

```yaml
_STEP_COMPLETE:
  Agent: Gateway
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    deliverable: [artifact path or inline]
    artifact_type: "[OpenAPI Spec | GraphQL SDL | API Review | Versioning Plan | Breaking Change Report | Security Config]"
    parameters:
      api_type: "[REST | GraphQL | gRPC]"
      endpoints_designed: "[count]"
      spec_version: "[OpenAPI 3.0 | 3.1 | 3.2]"
      versioning_strategy: "[URL path | Header | Query param]"
      breaking_changes: "[none | list]"
      security_methods: ["[OAuth 2.0 | JWT | API Key | CORS | Rate Limit]"]
    review_status: "[passed | issues: [list]]"
  Next: Builder | Quill | Voyager | Sentinel | DONE
  Reason: [Why this next step]
```
