# C4 Diagrams Reference (Canvas `c4` recipe)

Purpose: Render C4 model views — System Context, Container, Component, and Code — as Mermaid C4 diagrams (`C4Context` / `C4Container` / `C4Component`) that are readable in-PR and embeddable in Markdown docs. Canvas renders the visual; it does not own the canonical model.

## Scope Boundary

- **Canvas `c4`**: Mermaid C4 rendering only. Input is either a natural-language description of the system, an existing Stratum Structurizr DSL, or reverse-generated structure from code.
- **Stratum (elsewhere)**: Canonical C4 modeling — Structurizr DSL authoring, architectural evaluation (ATAM/CBAM), fitness functions, and DSL-as-source-of-truth governance.

If the ask is "model this architecture in C4 and evaluate it" → hand off to `Stratum`. If the ask is "render a Mermaid C4 diagram I can paste into a PR description or ADR" → stay in Canvas `c4`.

For Code-level (L4) views, Mermaid C4 syntax does not apply — fall back to the Canvas `class` recipe.

## Input Sources

| Source | Use when | Fidelity |
|--------|----------|----------|
| Structurizr DSL (from Stratum) | Canonical model already exists | High — derive names, relationships, tags verbatim |
| Natural-language description | Ad-hoc request, no formal model yet | Medium — flag that Stratum owns the canonical version |
| Reverse-generated from code | Single-container scope (components from package structure) | Medium — verify against actual imports, not inferred ones |
| Existing diagram + refactor request | Re-layout, split, or level-transition | High — preserve existing element names |

## Workflow

```
UNDERSTAND  →  identify target level (Context / Container / Component)
            →  one level per diagram; never mix
            →  locate canonical source: Stratum DSL, code, or verbal

ANALYZE     →  extract Person / System / Container / Component nodes
            →  extract directional relationships with concrete labels
            →  decide boundary: System_Boundary vs Enterprise_Boundary

DRAW        →  pick C4Context / C4Container / C4Component
            →  use Person() / System() / System_Ext() / Container() / Component()
            →  label every Rel() with verb + protocol (e.g. "reads via HTTPS")

REVIEW      →  ≤20 elements per diagram (split by boundary if over)
            →  every Rel has a verb, not just an arrow
            →  external systems use *_Ext variants
            →  flag: "canonical model lives in Stratum DSL at <path>"
```

## Mermaid C4 Syntax Patterns

### Context (L1)

```mermaid
C4Context
    title System Context — Orders Platform
    Person(customer, "Customer", "Places orders, tracks shipments")
    System(ordersPlatform, "Orders Platform", "Core ordering and fulfillment")
    System_Ext(paymentGateway, "Payment Gateway", "Third-party card processor")
    System_Ext(emailSvc, "Email Service", "Transactional email provider")
    Rel(customer, ordersPlatform, "Places orders via", "HTTPS")
    Rel(ordersPlatform, paymentGateway, "Authorizes payment via", "REST")
    Rel(ordersPlatform, emailSvc, "Sends confirmation via", "SMTP")
```

### Container (L2)

```mermaid
C4Container
    title Container View — Orders Platform
    Person(customer, "Customer")
    System_Boundary(c1, "Orders Platform") {
        Container(web, "Web App", "Next.js 15", "Customer-facing UI")
        Container(api, "Orders API", "Node.js / Fastify", "Order lifecycle")
        ContainerDb(db, "Orders DB", "PostgreSQL 17", "Orders, line items")
        Container(worker, "Fulfillment Worker", "Node.js", "Async fulfillment jobs")
    }
    System_Ext(payment, "Payment Gateway")
    Rel(customer, web, "Uses", "HTTPS")
    Rel(web, api, "Calls", "JSON/HTTPS")
    Rel(api, db, "Reads/writes", "SQL/TLS")
    Rel(api, worker, "Enqueues", "SQS")
    Rel(worker, payment, "Charges via", "REST")
```

### Component (L3)

```mermaid
C4Component
    title Component View — Orders API
    Container_Boundary(api, "Orders API") {
        Component(ordersCtl, "Orders Controller", "Fastify route", "HTTP entry point")
        Component(ordersSvc, "Orders Service", "Domain layer", "Order lifecycle rules")
        Component(ordersRepo, "Orders Repository", "Data layer", "Persistence")
        Component(paymentCl, "Payment Client", "HTTP client", "Payment gateway adapter")
    }
    ContainerDb(db, "Orders DB")
    System_Ext(payment, "Payment Gateway")
    Rel(ordersCtl, ordersSvc, "Invokes")
    Rel(ordersSvc, ordersRepo, "Persists via")
    Rel(ordersSvc, paymentCl, "Charges via")
    Rel(ordersRepo, db, "SQL")
    Rel(paymentCl, payment, "REST")
```

## Anti-Patterns

- Mixing levels in one diagram (Person + Component side-by-side) — each view answers one question only.
- Using generic `System` for third-party services — always `System_Ext`.
- Unlabeled `Rel()` arrows — a directional arrow without verb + protocol is noise.
- Re-authoring a Structurizr DSL's node names in Canvas — if Stratum owns the model, derive names verbatim to prevent drift.
- Stuffing 40+ components into one Component view — split by subsystem or bounded context, one diagram per split.
- Using C4 syntax for Code-level (class/package internals) — fall back to Mermaid `classDiagram` via the Canvas `class` recipe.

## Handoff to Stratum

When the user asks for evaluation, fitness functions, or "the source of truth for our architecture," stop rendering and hand off:

- Signal Stratum: "Canvas rendered a Mermaid C4 view at <level>. Canonical DSL should live in Stratum."
- Artifacts to return: the Mermaid block, the element inventory (names + descriptions), and the level rendered.
- Open question for Stratum: "Should the DSL include deployment view or stay logical-only?"

## Output Checklist

- [ ] One C4 level per diagram.
- [ ] Every `Rel()` has a verb and (where meaningful) a protocol/technology.
- [ ] External systems use `System_Ext` / `Container_Ext`.
- [ ] Title states system name and level ("Container View — Orders Platform").
- [ ] If a Stratum DSL exists, note its path in the `Sources` section.
- [ ] ≤20 primary elements; split and cross-link if over.
