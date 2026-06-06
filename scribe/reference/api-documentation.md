# API Documentation Reference

Purpose: Transform a machine-readable OpenAPI specification into a human-readable API reference that developers can learn from, copy code out of, and debug with. The OpenAPI YAML is the contract; this document is the experience.

## Scope Boundary

- **Scribe `api-doc`**: authors the human-facing API reference — narrative guides, code samples, error catalog, auth flow explanation, versioning note, changelog. Publishes via Redoc, Stoplight Elements, Mintlify, or equivalent.
- **Gateway (elsewhere)**: owns the OpenAPI spec itself — schema design, versioning rules, breaking-change detection, REST/GraphQL best practices, spec linting. Gateway produces the YAML; Scribe `api-doc` renders the doc site.

If the question is "should this field be required and what is its schema?" → `Gateway`. If the question is "the spec is finalized, now publish developer docs" → Scribe `api-doc`.

Handoff direction: **Gateway → Scribe**. The OpenAPI 3.x file is the source of truth; this reference documents what Gateway specified without re-deciding it.

> **Spec version, 2026-05.** OpenAPI `3.2` is the current shipped version (released late 2025); the OpenAPI Initiative is working on `3.3` with explicit improvements to Security Schemes and tighter integration with MCP / AI protocols. Default to `3.2` for new projects; stay on `3.1` only when tooling has not caught up. AsyncAPI `3.1` is the equivalent baseline for event-driven and message-broker APIs.

## Renderer Selection

| Renderer | Pick when | Skip when |
|----------|-----------|-----------|
| Redoc | Single spec, static hosting, zero JS config | Need multi-spec portal or interactive try-it |
| Stoplight Elements | Embed in existing site, try-it console needed | Heavy customization of layout |
| Mintlify | Want Markdown narrative + generated reference side-by-side, hosted | Prefer self-hosted static output |
| Scalar | Modern look, OpenAPI 3.1 native, open source | Need enterprise SSO on the doc site |
| Docusaurus + redocusaurus plugin | Already using Docusaurus for guides | Greenfield — overkill |

Default: **Redoc** for static OpenAPI 3.1 publishing; **Mintlify** when narrative guides dominate.

## Workflow

```
UNDERSTAND  ->  confirm the OpenAPI spec is frozen for this version (from Gateway)
            ->  identify audience (external partner? internal service team? public SDK users?)
            ->  identify auth model (API key / OAuth 2.1 / mTLS / JWT)

STRUCTURE   ->  decide layout: single-page (Redoc) vs multi-page (Mintlify/Docusaurus)
            ->  plan the required surfaces: Getting Started, Auth, Per-endpoint, Errors, Changelog

DRAFT       ->  Getting Started: one copy-pasteable curl that returns 200
            ->  Authentication: full flow including token refresh and failure modes
            ->  Per-endpoint: description (why), parameters, code samples ≥ 2 languages, response shape
            ->  Error catalog: every documented error code, its meaning, client action
            ->  Versioning policy: how breaking changes are announced, deprecation window
            ->  Rate limits: quotas, headers returned, retry guidance
            ->  Changelog: per-version additions, deprecations, removals

REVIEW      ->  every endpoint has a working curl example (test it)
            ->  error catalog is complete — diff against the spec's documented responses
            ->  auth section includes the unhappy path (expired token, revoked key)
            ->  a new developer can make a successful call within 10 minutes of first read

FINALIZE    ->  publish to the chosen renderer
            ->  link from Gateway's OpenAPI spec as the "human reference"
            ->  wire CI to rebuild docs on spec change
```

## Required Surfaces

| Surface | Purpose | MUST include |
|---------|---------|--------------|
| Getting Started | 10-minute time-to-first-success | Working curl + expected 200 response |
| Authentication | How to obtain and use credentials | Happy path, token refresh, revocation, error codes |
| Endpoint Reference | Per-operation detail | Description, params, samples in curl + ≥1 SDK language, error cases |
| Error Catalog | Central error lookup | HTTP status, domain error code, meaning, retriable? client action |
| Versioning | Contract stability promise | Version scheme, deprecation window, breaking-change policy |
| Rate Limiting | Quota discovery | Limits per tier, response headers, backoff guidance |
| Changelog | What changed per version | Added / Changed / Deprecated / Removed, dates |

## Code Sample Rule

Every endpoint MUST ship with samples in **at least two languages**: `curl` plus one SDK language relevant to the audience (TypeScript, Python, Go, Java).

- Samples MUST be executable against a sandbox or mock server — no pseudo-code.
- Samples SHOULD be generated from the OpenAPI spec where possible (`openapi-generator`, Mintlify auto-samples) to prevent drift.
- Samples MUST NOT embed real API keys — use `${API_KEY}` placeholder and document where to obtain the real key.

## Error Catalog Structure

```markdown
| HTTP | Code | Meaning | Retriable | Client Action |
|------|------|---------|-----------|---------------|
| 400 | `invalid_argument` | Request failed validation | No | Fix the request; see `errors[].field` |
| 401 | `unauthenticated` | Missing or invalid credentials | No | Obtain a fresh token |
| 403 | `permission_denied` | Authenticated but not authorized | No | Request access from admin |
| 409 | `conflict` | Version mismatch on optimistic update | Yes (re-fetch) | Refresh resource, retry |
| 429 | `rate_limited` | Quota exceeded | Yes (after retry-after) | Honor `Retry-After` header |
| 503 | `unavailable` | Temporary service degradation | Yes (exponential backoff) | Backoff and retry |
```

## Anti-Patterns

- Documentation that drifts from the spec. Build the doc site from the spec in CI — do not hand-maintain both.
- Auth section that covers only the happy path. Developers get stuck on expired tokens and revoked keys; document those.
- One endpoint-per-page without a searchable index. Single-page (Redoc) or good search (Mintlify) beats paginated 404 hunting.
- No versioning policy. Consumers cannot plan upgrades without knowing the deprecation window.
- Rate-limit doc that says "be reasonable". Publish numbers, headers, and retry guidance.
- Shipping a changelog named `v2` with no date and no scope. Every entry MUST include the version, date, and Added / Changed / Deprecated / Removed bucket.
- Inventing fields not in the spec. The spec is the source of truth; if a field is missing from the spec, fix the spec via Gateway, not the doc.

## MCP Server Generation from the Spec (2026 baseline)

As of 2026, the dominant integration pattern for an API that AI agents are expected to call is to generate an **MCP server** directly from the OpenAPI spec, then publish the agent-facing reference alongside the human-facing reference. MCP is supported across Claude, ChatGPT, GitHub Copilot, Cursor, VS Code, Windsurf, LangChain / LangGraph, CrewAI, and AutoGen, so a single MCP wrapper covers nearly the entire agent landscape.

### Tooling Snapshot

| Tool | Input | What you get | Use it when |
|------|-------|--------------|-------------|
| **Speakeasy** | OpenAPI 3.x | Typed MCP server + typed SDK + tool-design polish | Production-grade MCP from OpenAPI; you want LLM-friendly tool descriptions, not raw operation IDs |
| **Stainless** | OpenAPI 3.x | Managed MCP server + multi-language SDKs | One spec, multiple distribution channels (MCP + SDKs) |
| **FastMCP** | OpenAPI 3.x | Python MCP server | You already ship a Python backend; add MCP next to the existing FastAPI app |
| **openapi-mcp-generator** (TS / Node) | OpenAPI 3.x | TypeScript MCP server with Zod validation, stdio + HTTP transports | Node-first stack; want to keep MCP server in the same repo as the API |
| **DigitalAPI** | OpenAPI 3.x | One-click hosted MCP server | Need an MCP server fast without writing code |

### Documentation Responsibilities Split

| Surface | Audience | What it covers |
|---------|----------|----------------|
| Human API reference (Redoc / Mintlify / Scalar) | Developers | Per-endpoint detail, curl + SDK samples, error catalog, auth flow |
| MCP tool reference | AI agents and their human reviewers | One *tool description* per MCP tool — name, when-to-call, parameter schema, expected output, idempotency, side-effect class |
| Auth & permissions doc | Both | Same source of truth; reference from both sides |

The MCP tool reference is **not optional** for an agent-callable API in 2026. Treat it as a first-class deliverable from Scribe `api-doc` — written in the same workflow, published alongside the human reference, regenerated on every spec change.

### Tool-Description Discipline

Pulled from Speakeasy / FastMCP best practice (2026):

- Each MCP tool description must explain **when the agent should call this tool**, not just what the endpoint does.
- Operations that are read-only must be tagged so the agent can call them under read-only auth without confirmation; write operations must declare their side-effect class (`creates`, `updates`, `deletes`, `external-effect`) so the agent's safety policy can gate them.
- Auto-generation from OpenAPI is the starting point — review every tool description by hand. Raw `operationId` text is rarely a good tool name.

## Handoff

- From `Gateway`: OpenAPI 3.2 spec finalized for a version → Scribe renders the reference.
- From `Scribe` SRS: SRS API sections reference the published doc by URL rather than restating endpoints.
- To `Prose`: error message copy and onboarding text handed off for UX writing review.
- To `Growth`: developer-portal landing page and SEO for public API docs.
- To `Morph`: if a PDF API reference is required for partner contracts.

## Citations

- OpenAPI 3.2 Specification (2025-Q4 release) — https://spec.openapis.org/
- AsyncAPI 3.1 Specification — https://www.asyncapi.com/docs/reference/specification/v3.1.0
- Model Context Protocol (Anthropic) — https://modelcontextprotocol.io/
- RFC 2119 — MUST / SHOULD / MAY for capability and error-handling language.
- RFC 7807 — Problem Details for HTTP APIs (error response shape).
- RFC 6749 / OAuth 2.1 draft — auth flow reference for OAuth-based APIs.
- Google API Design Guide, AIP-193 — error model conventions.
