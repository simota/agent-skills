# AI/LLM API Design Patterns

> Design patterns for APIs that expose AI/LLM capabilities — streaming, tool use, structured output, and safety.
>
> **2026-05 baseline**:
> - **OpenAPI 3.2** (2025-09-23) gives streaming endpoints a first-class contract via `text/event-stream` + `itemSchema`, `application/jsonl`, and `application/json-seq` ([spec](https://spec.openapis.org/oas/v3.2.0.html)). Document SSE chat completions with `itemSchema` instead of prose.
> - **OpenAI Structured Outputs** with `strict: true` (gpt-4o-2024-08-06+) guarantees exact JSON Schema conformance — 100% on complex schema-following evals vs ~40% pre-strict ([OpenAI announcement](https://openai.com/index/introducing-structured-outputs-in-the-api/)). Strict-mode constraints: `additionalProperties: false`, all properties in `required` (use `null` union for optional). Function-calling supports the same `strict` flag.
> - **Anthropic Prompt Caching** (GA) cuts long-prompt input cost up to 90% and latency up to 85%; cache hits are 0.1× input price, 5-min TTL default (1-hour optional). Anthropic now **automatically identifies cached segments** — manual `cache_control` markers are still supported but no longer required for many cases ([Anthropic docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)).
> - **OWASP Top 10 for Agentic Applications 2026** (released 2025-12, [genai.owasp.org](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)) — ASI01 Agent Goal Hijacking is the #1 risk for agent-facing APIs. Apply principle-of-least-agency on every tool exposed via function-calling.

---

## Streaming Response Pattern (SSE)

Server-Sent Events (SSE) is the standard for streaming LLM token output to clients.

```http
POST /v1/chat/completions
Content-Type: application/json
Accept: text/event-stream

{
  "model": "claude-opus-4-6",
  "stream": true,
  "messages": [{"role": "user", "content": "Hello"}]
}
```

```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
X-Accel-Buffering: no

data: {"id":"msg_01","type":"content_block_delta","delta":{"type":"text_delta","text":"Hello"}}

data: {"id":"msg_01","type":"content_block_delta","delta":{"type":"text_delta","text":"!"}}

data: {"id":"msg_01","type":"message_stop"}

data: [DONE]
```

### Streaming Design Rules

| Rule | Description |
|------|-------------|
| `text/event-stream` content type | Always set `Content-Type: text/event-stream` and `Cache-Control: no-cache` |
| Terminate with `[DONE]` | Final `data: [DONE]` signals stream completion — clients must handle gracefully |
| Include event IDs | `id:` field on each event enables client-side reconnect with `Last-Event-ID` |
| Heartbeat events | Send `: keep-alive` comment lines every 15s to prevent proxy/load balancer timeouts |
| Error mid-stream | Send `data: {"type":"error","error":{"type":"server_error","message":"..."}}` then close stream |
| OpenAPI spec | Document streaming endpoints with `text/event-stream` response type and link to SSE event schema |

---

## Tool Use / Function Calling

Tool use allows the model to request structured data from external systems during generation.

### Schema Design

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a location. Use when the user asks about weather conditions.",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "City name or 'city, country' format. Example: 'Tokyo, JP'"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"],
          "description": "Temperature unit. Default is celsius."
        }
      },
      "required": ["location"]
    }
  }
}
```

### Best Practices

1. **Descriptions are prompts** — write `description` fields as instructions to the model, not documentation for humans. Specify when to call the tool and how to interpret the result.
2. **Narrow parameter schemas** — use `enum`, `minimum`, `maximum`, `pattern` to constrain valid inputs. Broad schemas lead to hallucinated parameter values.
3. **Idempotent tools first** — prefer read-only tools; flag state-mutating tools with `"confirm_required": true` (custom extension) to prompt user confirmation before execution.
4. **Return structured data** — tool results should be JSON, not prose. The model parses the result; unstructured text increases hallucination risk.
5. **Design for parallel calls** — models may invoke multiple tools simultaneously; tool implementations must be safe to run concurrently.

---

## Structured Output

Forces the model to produce JSON that conforms to a specified schema. As of 2024-08, OpenAI's `strict: true` mode (Structured Outputs) guarantees exact schema conformance on gpt-4o-2024-08-06+ and later — the model is constrained at decode time to emit only schema-conformant tokens.

### Strict-Mode Structured Output (OpenAI, gpt-4o-2024-08-06+)

```json
{
  "model": "gpt-4o-2026-04",
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "extract_product",
      "strict": true,
      "schema": {
        "type": "object",
        "additionalProperties": false,
        "required": ["name", "price", "sku"],
        "properties": {
          "name": { "type": "string" },
          "price": { "type": "number" },
          "sku":  { "type": ["string", "null"] }
        }
      }
    }
  },
  "messages": [
    { "role": "user", "content": "Extract product fields from: ..." }
  ]
}
```

Strict-mode constraints (enforced at request validation):
- `additionalProperties: false` on every object.
- All properties listed in `required`; mark optional fields by adding `null` to the type array.
- Subset of JSON Schema 2020-12 (no `oneOf` with conflicting types, no recursive `$ref` cycles).

### Legacy JSON Mode (still useful for non-OpenAI / older models)

```json
{
  "model": "claude-opus-4-7",
  "response_format": { "type": "json_object" },
  "messages": [
    { "role": "user", "content": "Extract product name, price, SKU from: ..." }
  ]
}
```

### Structured Output Rules

| Rule | Description |
|------|-------------|
| Prefer `strict: true` when available | gpt-4o-2024-08-06+ gives 100% schema-conformance vs <40% for gpt-4-0613. Anthropic tool-use approximates this via tool schemas. |
| Provide schema in prompt | Even with strict mode, include the target schema in the system prompt — models still hallucinate field semantics without context |
| Validate server-side | Never trust model output as schema-valid — always parse and validate with Zod/Pydantic before passing downstream (defense in depth, even with strict mode) |
| Handle partial JSON | Streaming structured output may arrive as partial JSON; buffer and parse only on `[DONE]` |
| Version your schemas | Include a `schema_version` field in output schemas; models may produce output with old field names after schema changes |

---

## Rate Limiting for AI APIs

AI APIs have unique cost dimensions that require multi-axis rate limiting.

| Dimension | Unit | Why It Matters |
|-----------|------|----------------|
| Requests per minute (RPM) | Count | Prevents API abuse and thundering herd |
| Input tokens per minute (TPM) | Tokens | Direct cost driver — long prompts consume quota fast |
| Output tokens per minute (TPM) | Tokens | Streaming output is billed per output token; unconstrained streaming can exhaust quota |
| Concurrent streams | Count | SSE connections hold server resources; limit per user/org |

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 30
X-RateLimit-Limit-Requests: 60
X-RateLimit-Remaining-Requests: 0
X-RateLimit-Limit-Tokens: 100000
X-RateLimit-Remaining-Tokens: 0
X-RateLimit-Reset-Requests: 2026-04-01T12:00:30Z
X-RateLimit-Reset-Tokens: 2026-04-01T12:00:05Z

{
  "error": {
    "type": "rate_limit_error",
    "message": "Token quota exceeded. Retry after 30 seconds."
  }
}
```

---

## Error Handling

AI API errors require distinct handling from standard REST errors due to partial streaming and model-specific failure modes.

### Error Response Format

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "context_length_exceeded",
    "message": "Input tokens (128500) exceed model maximum (128000). Reduce prompt length.",
    "param": "messages"
  }
}
```

### Error Handling Rules

1. **Distinguish error types**: `invalid_request_error` (4xx, fix the request), `authentication_error` (401, check API key), `rate_limit_error` (429, backoff), `api_error` (5xx, retry with exponential backoff).
2. **Handle stream interruption**: If a streaming response stops without `[DONE]`, treat as `api_error` — do not present partial output as complete to the user.
3. **Content filter errors**: `content_policy_violation` errors should be surfaced to users with a user-friendly message; do not silently retry — log for safety review.
4. **Token budget errors**: Return `context_length_exceeded` with the actual and maximum token counts to help clients truncate inputs correctly.
