# Diagram Templates Reference

Purpose: Read this when you need a fast, syntax-safe starter for a common diagram family.

## Contents

- Selection matrix
- Mermaid starters
- draw.io note

## Selection Matrix

| Diagram | Use For |
|---------|---------|
| Flowchart | Control flow, business process, API routes |
| Sequence | Interactions over time |
| State | Lifecycle or state transitions |
| Class | Types and dependencies |
| ER | Database structure |
| Journey | User or DX experience |
| Mind Map | Concepts or hierarchy |
| Gantt | Schedule and dependencies |
| Git Graph | Branch or merge history |
| Pie Chart | Ratios or composition |
| Architecture | Service topology, infrastructure layout |
| Block | Grid layouts, structured compositions |
| Kanban | Task boards, workflow columns |
| Sankey | Flow volumes, resource distribution |
| XY Chart | Bar/line data visualization |
| Radar | Multi-axis capability comparison |
| Treemap | Hierarchical proportional areas |
| Venn | Set overlap and intersection visualization (v11.12.3+) |
| Ishikawa | Cause-and-effect / fishbone / root-cause analysis (v11.12.3+) |
| Wardley Map | Business strategy value-chain and component-evolution map (v11.14.0+) |

## Flowchart

```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[Alternative]
```

## Sequence

```mermaid
sequenceDiagram
    actor User
    participant API
    participant DB
    User->>API: Request
    API->>DB: Query
    DB-->>API: Result
    API-->>User: Response
```

## State

```mermaid
stateDiagram-v2
    [*] --> idle
    idle --> loading
    loading --> success
    loading --> error
```

## Class

```mermaid
classDiagram
    class User
    class Session
    User "1" --> "*" Session
```

## ER

```mermaid
erDiagram
    USER ||--o{ POST : writes
    USER {
      string id
      string email
    }
    POST {
      string id
      string title
    }
```

## Journey

```mermaid
journey
    title Checkout Flow
    section Cart
      View cart: 4: User
    section Payment
      Submit payment: 2: User
```

## Mind Map

```mermaid
mindmap
  root((System))
    Frontend
    Backend
    Database
```

## Gantt

```mermaid
gantt
    title Release Plan
    dateFormat  YYYY-MM-DD
    section Build
    Implement :a1, 2026-03-01, 5d
    Test      :a2, after a1, 3d
```

## Git Graph

```mermaid
gitGraph
    commit
    branch feature
    checkout feature
    commit
    checkout main
    merge feature
```

## Pie Chart

```mermaid
pie title Test Composition
    "Unit" : 70
    "Integration" : 20
    "E2E" : 10
```

## Architecture

```mermaid
architecture-beta
    group api(cloud)[API Layer]

    service gateway(internet)[Gateway] in api
    service auth(server)[Auth] in api
    service db(database)[Database]

    gateway:R --> L:auth
    auth:R --> L:db
```

## Block

```mermaid
block-beta
    columns 3
    a["Frontend"] b["API"] c["Database"]
    d["CDN"]:3
```

## Kanban

```mermaid
kanban
    column1[Todo]
        task1[Design API]
        task2[Write tests]
    column2[In Progress]
        task3[Implement auth]
    column3[Done]
        task4[Setup CI]
```

## Sankey

```mermaid
sankey-beta

Source A,Target X,30
Source A,Target Y,20
Source B,Target Y,15
Source B,Target Z,35
```

## XY Chart

```mermaid
xychart-beta
    title "Monthly Revenue"
    x-axis [Jan, Feb, Mar, Apr, May]
    y-axis "Revenue (USD)" 0 --> 5000
    bar [1200, 1800, 2400, 3200, 4100]
    line [1000, 1600, 2200, 3000, 3800]
```

## Radar

```mermaid
radar-beta
    title "Team Skills"
    axis Frontend, Backend, DevOps, Testing, Design
    curve a["Alice"] { 4, 5, 2, 3, 3 }
    curve b["Bob"] { 2, 3, 5, 4, 2 }
```

## Treemap

```mermaid
treemap-beta
    root[Repository]
        src[src]
            components[components: 40]
            utils[utils: 20]
            pages[pages: 30]
        tests[tests: 25]
        docs[docs: 15]
```

## Venn (v11.12.3+)

[Source: Mermaid Venn syntax](https://mermaid.ai/open-source/syntax/venn.html)

```mermaid
venn-beta
    A["Backend"]
    B["Frontend"]
    C["DevOps"]
    A-B["Full-Stack"]
    A-C["SRE"]
    B-C["Design-Eng"]
    A-B-C["Generalist"]
```

## Ishikawa / Fishbone (v11.12.3+)

[Source: Mermaid Ishikawa syntax](https://mermaid.ai/open-source/syntax/ishikawa.html)

```mermaid
ishikawa-beta
    effect["High Error Rate"]
    cause1["People"]
        subcause1["Insufficient training"]
    cause2["Process"]
        subcause2["No code review"]
    cause3["Technology"]
        subcause3["Legacy dependencies"]
```

## Wardley Map (v11.14.0+)

[Source: Mermaid Wardley Maps docs](https://mermaid.js.org/syntax/wardley.html)

```mermaid
wardley-beta
    title API Platform Strategy
    anchor User [0.95, 0.63]
    anchor Business [0.95, 0.40]
    component API Gateway [0.68, 0.46]
    component Auth Service [0.55, 0.37]
    component Database [0.30, 0.25]
    User -> API Gateway
    Business -> API Gateway
    API Gateway -> Auth Service
    API Gateway -> Database
```

## draw.io Note

Use `reference/drawio-specs.md` when XML structure, IDs, edge routing, or layout control matters.
