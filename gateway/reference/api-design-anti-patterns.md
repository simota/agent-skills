# REST API Design Anti-Patterns
> Failure patterns in URL design, HTTP methods, response design, error handling, and pagination
>
> **2026-05 update**: Assumes RFC 9457 Problem Details (2023-07, obsoletes RFC 7807) and OpenAPI 3.2 (2025-09-23). RFC 6648 formally deprecated `X-` headers back in 2012 — Standard Webhooks also dropped the `X-` prefix, using `webhook-id` / `webhook-timestamp` / `webhook-signature` instead. Using an `X-` prefix on a new API header is equivalent to the AD-08 anti-pattern.
## 1. The 7 Major REST API Design Anti-Patterns
| # | Anti-Pattern | Problem | Symptoms | Countermeasure |
|---|-------------|------|------|------|
| **AD-01** | **Verb-in-URL** | Embedding action verbs in the URL, e.g. `/getUsers`, `/createOrder` | URLs proliferate per CRUD operation, departs from REST principles | Use resource nouns only: `GET /users`, `POST /orders`; express the action via the HTTP method |
| **AD-02** | **POST for Everything** | Using POST for every operation, including search/delete/update | Not cacheable, no idempotency guarantee, middleware can't be leveraged | Use GET=retrieve, POST=create, PUT=full update, PATCH=partial update, DELETE=delete appropriately |
| **AD-03** | **Inconsistent Naming** | camelCase/snake_case/kebab-case mixed across APIs | Developer confusion, higher documentation burden, lower API adoption | Enforce naming conventions with an API linter (Spectral/Vacuum), define a style guide upfront |
| **AD-04** | **Kitchen Sink Response** | Always returning every field, bloating the payload with unneeded data | Response latency, bandwidth waste, unnecessary client-side parsing | Sparse fieldsets: `?fields=id,name,email`, minimal defaults, related resources as separate endpoints |
| **AD-05** | **Implementation Exposure** | DB table/column names exposed in the URL | Internal structure leaks, e.g. `/api/database/tables/book_inventory/records` | Use abstract resource names: `GET /api/books?available=true`, hide internal implementation |
| **AD-06** | **Excessive Nesting** | `/companies/456/departments/2/employees/123/projects` | URLs become unwieldy, related resources are hard to discover | Cap at 2 levels: `/employees/123/projects` or `/projects?employeeId=123` |
| **AD-07** | **No Pagination** | Returning all records at once; adding pagination later breaks every client | 10,000-record responses time out, memory exhaustion | Build in pagination from the initial design: cursor-based recommended (at scale), offset only for small scale |
---
## 3. Response Design Pitfalls
| # | Anti-Pattern | Problem | Symptoms | Countermeasure |
|---|-------------|------|------|------|
| **RD-01** | **Nullable vs Optional Confusion** | Not distinguishing null from unset, producing tri-state logic | Unclear whether null means "unset," "explicit null," or "error" | Omit optional fields entirely, avoid explicit null, clarify nullable/required in OpenAPI |
| **RD-02** | **No HATEOAS** | Clients hardcode the URL structure | Every client needs updating on API change, workflows undiscoverable | Include links/actions in responses to enable dynamic navigation |
| **RD-03** | **Hyrum's Law Ignorance** | Clients depend on undocumented behavior such as array ordering | Changing sort order unexpectedly breaks clients | Document all observable behavior, explicitly state which behaviors are not guaranteed |
| **RD-04** | **No Idempotency Keys** | Retrying a POST request creates duplicates | An order gets created twice after a retry following a network error | Provide an Idempotency-Key header (Stripe-style) |
---
## 5. Collaboration with Gateway
**Source:** [Zuplo: Common Pitfalls in RESTful API Design](https://zuplo.com/blog/2025/03/12/common-pitfalls-in-restful-api-design) · [Specmatic: API Design Anti-patterns](https://specmatic.io/appearance/how-to-identify-avoid-api-design-anti-patterns/) · [Milan Jovanovic: 5 Most Common REST API Design Mistakes](https://www.milanjovanovic.tech/blog/the-5-most-common-rest-api-design-mistakes-and-how-to-avoid-them) · [DEV.to: 7 API Design Mistakes](https://dev.to/maxxmini/7-api-design-mistakes-that-make-your-users-hate-you-and-how-to-fix-them-3722) · [Speakeasy: Errors Best Practices in REST API Design](https://www.speakeasy.com/api-design/errors)
