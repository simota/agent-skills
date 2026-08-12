# Xquik AUTORUN Schema

Use this schema for Xquik work returned through `_STEP_COMPLETE`.

```yaml
_STEP_COMPLETE:
  Agent: Xquik
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    mode: PUBLIC_READ | PAID_READ | ACCOUNT_READ | MONITOR | WEBHOOK | EXPORT | WRITE
    surface: REST | MCP | OPENAPI | SDK | ACTOR | WEBHOOK
    operation: "<documented operation or tool>"
    docs_url: "https://docs.xquik.com/..."
    target: "<accounts, query, post URLs, or resource IDs>"
    response_contract: "<documented contract or default>"
    result:
      artifact: "<source packet, monitor packet, integration packet, or action receipt>"
      location: "<path, URL, or inline>"
    authorization:
      credential_source: "<environment variable name, connection name, or none>"
      connected_account_required: true | false
      approval_required: true | false
      approval_received: true | false
    payment:
      mechanism: NONE | ACCOUNT_CREDITS | GUEST_WALLET | MPP
      estimate: "<credits, currency amount, or none>"
      approval_required: true | false
      approval_received: true | false
    bounds:
      page_limit: <integer or null>
      result_limit: <integer or null>
      time_range: "<range or null>"
      stop_reason: "<why collection or polling stopped>"
    validation:
      status: passed | flagged | blocked
      checks:
        - "<schema, cursor, rate limit, action status, or webhook check>"
  Next: Builder | Relay | Stream | Voice | Compete | Sentinel | USER | DONE
  Reason: "<why this handoff is next>"
```

Rules:

- Never include a credential, cookie, private payload, payment detail, or raw
  direct message.
- Keep resource IDs and cursors opaque.
- For side effects, `approval_received` must be `true`.
- For a new payment or top-up, `payment.approval_received` must be `true`.
- A payment receipt proves settlement, not application success.
- For durable writes, report the terminal action state.
- Use `BLOCKED` when required approval, authority, or documentation is absent.
