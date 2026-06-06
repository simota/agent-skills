# Investigation Patterns Reference

## Pattern Selection Guide

| User Question Type | Applicable Pattern | Investigation Depth |
|-------------------|-------------------|-------------------|
| "Does X exist?" | Feature Discovery | Surface |
| "How does X work?" | Flow Tracing | Moderate-Deep |
| "What is the structure of X?" | Structure Mapping | Moderate |
| "Where does data go?" | Data Flow | Deep |
| 「どんな技術を使ってる？」 | Convention Discovery | Surface-Moderate |
| 「このリポジトリを理解したい」 | Full Onboarding | All patterns combined |

---

## Pattern 1: Feature Discovery (機能探索)

### When
- "Does authentication exist?"
- "Is there a payment integration?"
- "Do we have email sending?"

### Search Strategy

```
Step 1: Keyword Search (broad)
  ├── Domain keywords: "auth", "login", "session"
  ├── Technical keywords: "jwt", "oauth", "passport"
  └── File patterns: "*auth*", "*login*", "*session*"

Step 2: Structural Search (targeted)
  ├── Dedicated directories: src/auth/, src/authentication/
  ├── Dedicated files: authService.ts, loginController.ts
  └── Config references: .env (AUTH_SECRET, JWT_KEY)

Step 3: Dependency Search (verification)
  ├── Package manifest: "passport", "next-auth", "jsonwebtoken"
  └── Import usage: count of imports from auth modules

Step 4: Evidence Assessment
  ├── Implementation depth: Full / Partial / Stub / Config-only
  └── Confidence level: based on evidence count and consistency
```

### Confidence Scoring

| Evidence Count | Evidence Types | Confidence |
|---------------|---------------|------------|
| 5+ | Multi-layer (files + deps + config) | High |
| 3-4 | Two layers | Medium |
| 1-2 | Single layer | Low |
| 0 | None | Not Found |

---

## Pattern 2: Flow Tracing (フロー追跡)

### When
- "How does user registration work?"
- "What happens when an order is placed?"
- "Trace the login flow"

### Tracing Strategy

```
Step 1: Find Entry Point
  ├── HTTP: route definition (GET/POST/PUT/DELETE)
  ├── CLI: command handler
  ├── Event: event listener/subscriber
  ├── UI: onClick/onSubmit handler
  └── Cron: scheduled task

Step 2: Trace Forward (Happy Path)
  ├── Follow function calls sequentially
  ├── Record each step: [file:line] → [action] → [next]
  ├── Note branching points (if/switch/match)
  └── Track external calls (DB, API, filesystem)

Step 3: Trace Error Paths
  ├── try/catch blocks
  ├── Validation failures
  ├── Guard clauses / early returns
  └── Error middleware/handlers

Step 4: Identify Side Effects
  ├── Logging
  ├── Event emission
  ├── Cache operations
  ├── Notification sending
  └── Metric tracking
```

### Entry Point Patterns by Framework

| Framework | Entry Point Pattern | Search Query |
|-----------|-------------------|--------------|
| Express | `router.get/post()` | `grep "router\.\(get\|post\|put\|delete\)"` |
| Next.js App Router | `app/**/route.ts` | `glob "app/**/route.ts"` |
| Next.js Pages | `pages/api/**/*.ts` | `glob "pages/api/**/*.ts"` |
| Django | `urls.py` → `views.py` | `grep "path\|url.*views"` |
| FastAPI | `@app.get/post()` | `grep "@app\.\(get\|post\|put\|delete\)"` |
| Spring | `@GetMapping` etc. | `grep "@\(Get\|Post\|Put\|Delete\)Mapping"` |
| Go net/http | `http.HandleFunc` | `grep "HandleFunc\|Handle("` |
| Gin | `r.GET/POST()` | `grep "r\.\(GET\|POST\|PUT\|DELETE\)"` |

---

## Pattern 3: Structure Mapping (構造把握)

### When
- "What's the architecture of this project?"
- "How are modules organized?"
- "What layers does this app have?"

### Mapping Strategy

```
Step 1: Top-Level Scan
  ├── ls top-level directories
  ├── Read README.md
  ├── Read package.json / manifest
  └── Identify src/ entry structure

Step 2: Layer Detection
  ├── MVC: models/ views/ controllers/
  ├── Clean/Hexagonal: domain/ application/ infrastructure/
  ├── Feature-based: features/[name]/ or modules/[name]/
  ├── Flat: all files in src/
  └── Hybrid: mix of patterns

Step 3: Module Cataloging
  ├── For each module:
  │   ├── File count and types
  │   ├── Exported symbols (public API)
  │   ├── Internal helpers
  │   └── Test coverage presence
  └── Cross-module dependencies

Step 4: Convention Extraction
  ├── Naming conventions
  ├── File organization rules
  ├── Import patterns
  └── Testing structure
```

### Architecture Pattern Detection

| Pattern | Indicators |
|---------|-----------|
| **MVC** | models/, views/, controllers/ directories |
| **Clean Architecture** | domain/, usecases/, infrastructure/ layers |
| **Hexagonal** | ports/, adapters/, domain/ structure |
| **Feature-based** | features/[name]/ with co-located files |
| **Layered** | presentation/, business/, data/ layers |
| **Monolith** | Single src/ with mixed concerns |
| **Monorepo** | packages/ or apps/ with separate package.json |

---

## Pattern 4: Data Flow (データフロー追跡)

### When
- "Where is user data stored?"
- "How does order data flow through the system?"
- "What happens to uploaded files?"

### Tracing Strategy

```
Step 1: Find Type Definition
  ├── TypeScript: interface/type definitions
  ├── Python: dataclass/Pydantic model
  ├── Go: struct definitions
  ├── Java: class/record definitions
  └── DB: schema/migration files

Step 2: Trace Lifecycle
  ├── Creation: constructors, factories, form submissions
  ├── Validation: validators, schemas, guard clauses
  ├── Storage: repository.save(), db.insert()
  ├── Retrieval: repository.find(), db.query()
  ├── Transformation: mappers, serializers, DTOs
  └── Output: API responses, UI rendering, exports

Step 3: Map Boundaries
  ├── Input boundary: API request → validated domain model
  ├── Storage boundary: domain model → DB entity
  ├── Output boundary: domain model → DTO/response
  └── External boundary: internal model → external API format
```

---

## Pattern 5: Convention Discovery (規約発見)

### When
- "What technologies does this project use?"
- "What patterns should I follow?"
- "How do I add a new endpoint?"

### Discovery Strategy

```
Step 1: Manifest Analysis
  ├── Dependencies and their versions
  ├── Scripts (build, test, lint, deploy)
  ├── Configuration files (.eslintrc, tsconfig, etc.)
  └── CI/CD pipeline definitions

Step 2: Pattern Sampling
  ├── Pick 3 representative files per layer
  ├── Compare naming, structure, patterns
  ├── Identify consistency and deviations
  └── Note implicit rules

Step 3: Convention Catalog
  ├── File naming: kebab-case.ts, PascalCase.tsx, etc.
  ├── Function naming: camelCase, snake_case, etc.
  ├── Directory structure: by feature, by type, etc.
  ├── Import ordering: external → internal → relative
  ├── Error handling: try/catch, Result type, etc.
  └── Testing: co-located vs separate, naming, coverage
```

---

## Combining Patterns (Full Onboarding)

For "understand this repository" requests, combine patterns in order:

```
1. Convention Discovery (5 min)  → Tech stack and patterns
2. Structure Mapping (10 min)    → Module boundaries
3. Feature Discovery (5 min)     → Key feature inventory
4. Flow Tracing (15 min)         → 2-3 core flows
5. Report Generation (5 min)     → Onboarding document
```

Total: ~40 minutes for a medium-sized codebase.
