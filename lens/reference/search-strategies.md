# Search Strategies Reference

## Multi-Layer Search Architecture

Lens uses a 5-layer search approach. Execute from the top layer down, drilling deeper as needed. When LSP is available, Layer 3a is preferred over Layer 3b.

```
Layer 1:  Structure Search ──── Fastest, broadest (directories, file names)
Layer 2:  Keyword Search ────── Targeted narrowing (domain, technical terms)
Layer 3a: LSP Navigation ────── Type-aware symbol lookup (go-to-definition, find-references)
Layer 3b: Reference Search ──── Grep-based relationship tracking (import/export/calls)
Layer 4:  Contextual Read ───── Deep understanding (file content analysis)
```

### LSP vs Grep Decision

| Situation | Preferred Layer |
|-----------|----------------|
| LSP available + typed language | Layer 3a (zero false positives) |
| LSP available + dynamic language | Layer 3a first, Layer 3b to catch dynamic dispatch |
| No LSP / LSP errors | Layer 3b (grep fallback) |
| Cross-repo / monorepo boundary | Layer 3b (LSP may not span repos) |

---

## Layer 1: Structure Search

### Purpose
Quickly grasp the overall project layout.

### Methods

| Target | Method | What It Reveals |
|--------|--------|----------------|
| Directory structure | `ls`, `Glob "**/"` | Module boundaries, architecture patterns |
| File name patterns | `Glob "**/*auth*"` | Feature existence and placement |
| Manifests | `Read package.json` | Tech stack, dependencies |
| Config files | `Glob "**/*.config.*"` | Toolchain, build settings |

### Common Directory Patterns

```
# MVC Pattern
src/
├── models/          → Data models
├── views/           → UI/templates
├── controllers/     → Request handlers
└── routes/          → Route definitions

# Clean Architecture
src/
├── domain/          → Business rules
├── application/     → Use cases
├── infrastructure/  → External integrations
└── presentation/    → UI/API

# Feature-based
src/
├── features/
│   ├── auth/        → Authentication module
│   ├── payment/     → Payment module
│   └── user/        → User management module
└── shared/          → Shared utilities

# Next.js App Router
app/
├── (auth)/          → Auth-related pages
├── api/             → API routes
├── dashboard/       → Dashboard
└── layout.tsx       → Root layout
```

---

## Layer 2: Keyword Search

### Purpose
Narrow down to specific features or implementations.

### Domain Keyword Dictionary

| Feature Area | Search Keywords |
|-------------|----------------|
| Authentication | `auth`, `login`, `logout`, `session`, `token`, `jwt`, `oauth` |
| Authorization | `permission`, `role`, `rbac`, `policy`, `guard`, `middleware` |
| Payment | `payment`, `checkout`, `stripe`, `billing`, `invoice`, `subscription` |
| Email | `email`, `mail`, `smtp`, `sendgrid`, `ses`, `notification` |
| File storage | `upload`, `storage`, `s3`, `blob`, `file`, `asset` |
| Caching | `cache`, `redis`, `memcached`, `ttl`, `invalidate` |
| Queue | `queue`, `job`, `worker`, `bull`, `rabbitmq`, `sqs` |
| Search | `search`, `elasticsearch`, `algolia`, `fulltext`, `index` |
| Logging | `logger`, `log`, `winston`, `pino`, `sentry`, `monitoring` |
| Testing | `test`, `spec`, `mock`, `fixture`, `stub`, `__tests__` |

### Framework-Specific Entry Point Search

```bash
# Express.js
Grep "app\.(get|post|put|delete|patch|use)\("
Grep "router\.(get|post|put|delete|patch)\("

# Next.js (App Router)
Glob "app/**/route.ts"
Glob "app/**/page.tsx"

# Next.js (Pages Router)
Glob "pages/api/**/*.ts"

# Django
Grep "path\(|re_path\("
Grep "class.*View.*:"

# FastAPI
Grep "@(app|router)\.(get|post|put|delete)\("

# Spring Boot
Grep "@(Get|Post|Put|Delete|Patch|Request)Mapping"

# Go (net/http)
Grep "http\.Handle(Func)?\("

# Go (Gin)
Grep "\.(GET|POST|PUT|DELETE|PATCH)\("

# Ruby on Rails
Grep "(get|post|put|delete|patch|resources|resource)\s"
```

---

## Semantic Search Enhancement

### Purpose
Complement keyword search with meaning-based retrieval when exact identifiers are unknown.

### When to Use

| Situation | Use Semantic Search? |
|-----------|---------------------|
| Natural language query ("where is auth handled?") | Yes — semantic search understands intent |
| Exact symbol name known (`loginUser`) | No — grep/LSP is faster and precise |
| Conceptual exploration ("error handling patterns") | Yes — finds related code across naming conventions |
| Investigation stall after 2 keyword iterations | Yes — recovers results keyword search missed |

### Available Tools (2026)

| Tool | Approach | Integration |
|------|----------|-------------|
| Augment Context Engine | Semantic indexing + dependency graphs | MCP server |
| code-graph-mcp | Tree-sitter AST + BM25/vector hybrid | MCP server (16 languages) |
| CodeGrok MCP | AST parsing + vector embeddings | MCP server |
| GitLab Semantic Code Search | Vector embeddings + vector DB | GitLab Duo |
| Cursor Semantic Search | Custom embeddings from agent traces | IDE-integrated |

### Performance

Cursor benchmarks show semantic search achieves 12.5% higher accuracy than grep alone (range 6.5–23.5% depending on model). Hybrid approach (grep + semantic + LSP) performs best. [Source: cursor.com/blog/semsearch]

### Integration with Layer Architecture

Semantic search is a cross-cutting enhancement, not a replacement layer:
- **Augments Layer 2**: Find files by meaning when keywords require guessing exact identifiers
- **Augments Layer 3b**: Discover semantic relationships that string matching misses
- **Does not replace Layer 3a**: LSP remains authoritative for typed symbol navigation

---

## Layer 3a: LSP Navigation

### Purpose
Type-aware, AST-accurate symbol navigation. Zero false positives for typed languages.

### Methods

| Operation | What It Reveals | When to Use |
|-----------|----------------|-------------|
| Go-to-definition | Where a symbol is defined | Tracing imports, finding source of truth |
| Find-references | All usage sites of a symbol | Understanding impact, dependency mapping |
| Workspace symbol search | Symbols matching a query across the project | Feature discovery by type/function name |
| Hover / type info | Type signatures, documentation | Quick understanding without reading full file |

### Advantages Over Grep

- **No false positives**: `User` in grep matches comments, strings, variable names; LSP only finds the actual type
- **Rename-safe**: Tracks the semantic symbol, not the string
- **Cross-file resolution**: Follows re-exports, barrel files, and aliased imports automatically
- **Dynamic language caveat**: LSP in Python/JS/Ruby may miss dynamically dispatched calls; supplement with Layer 3b grep

### When to Fall Back to Layer 3b

- LSP is not configured or returns errors
- Investigating string-based dispatch (event names, route strings, DI tokens)
- Cross-repository boundaries in monorepos
- Searching for patterns rather than specific symbols (e.g., "all functions that call `db.query`")

---

## Layer 3b: Reference Search

### Purpose
Track inter-module dependencies and call chains.

### Import/Export Chain Tracking

```bash
# TypeScript/JavaScript - Find import sources for a module
Grep "from ['\"].*authService['\"]"
Grep "require\(['\"].*authService['\"]\)"

# Find call sites of specific functions
Grep "authService\.(login|verify|logout)"

# Find usage of specific types
Grep "User(Entity|DTO|Response|Request)"

# Python - Import tracking
Grep "from.*auth.*import"
Grep "import.*auth"

# Go - Package usage tracking
Grep "\".*\/auth\""
```

### Call Graph Construction Procedure

```
1. Identify target function
   e.g., `loginUser()` in `src/services/authService.ts`

2. Search for callers (upward)
   Grep "loginUser\(" → List of calling files

3. Read callees (downward)
   Read authService.ts → Extract function calls within loginUser()

4. Repeat
   Apply same procedure for each callee (usually 2-3 levels is sufficient)
```

---

## Layer 4: Contextual Read

### Purpose
Deeply understand file content, reading intent and design decisions.

### What to Focus On

| File Type | Focus Points |
|-----------|-------------|
| Service layer | Business logic, validation, error handling |
| Controller layer | Request/response transformation, routing |
| Repository layer | Query patterns, caching strategy |
| Middleware | Pre/post processing, auth/authz checks |
| Config files | Environment variables, feature flags, connections |
| Test files | Expected behavior, edge cases |
| Type definitions | Data models, interface contracts |

### Efficient File Reading Strategy

```
1. Read file header first (import statements → understand dependencies)
2. Find export statements (understand public API)
3. Grasp main function/class structure
4. Read detailed logic only where needed
```

---

## Recommended Search Sequences by Investigation Type

### "Does X exist?"
```
Layer 1 → Glob for file name search
Layer 2 → Grep for keyword search
Layer 4 → Read found files to confirm
→ Existence verdict + implementation depth assessment
```

### "How does X flow?"
```
Layer 2 → Grep for entry point search
Layer 4 → Read entry point to confirm
Layer 3 → Grep for call chain tracking
Layer 4 → Read each step for detail
→ Flow diagram + step table
```

### "What is the structure of this repo?"
```
Layer 1 → Directory structure scan
Layer 1 → Manifest reading
Layer 2 → Pattern detection
Layer 4 → Representative file sampling
→ Structure map + convention guide
```

### "Where does data go?"
```
Layer 2 → Grep for type/model definition search
Layer 3 → Grep for usage tracking
Layer 4 → Read transformation logic
→ Data lifecycle diagram
```
