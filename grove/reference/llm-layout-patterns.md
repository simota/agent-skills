# Layout Patterns Reference

**Purpose:** Standard LLM-optimized directory templates for common project types.
**Read when:** Designing new structure or recommending restructuring.

---

## Universal LLM Layer

Regardless of project type, apply this LLM optimization layer:

```
project/
├── CLAUDE.md                    # L1: Project rules (≤200 lines)
├── .claude/
│   ├── settings.json            # Tool & permission config
│   ├── rules/                   # L1.5: @imported rule modules
│   │   ├── coding-standards.md  #   Split by concern
│   │   ├── testing-policy.md
│   │   └── security-rules.md
│   └── skills/                  # L2: Project-specific skills
├── .agents/                     # Agent journals & memory
│   ├── PROJECT.md               #   Cross-agent activity log
│   └── memory/                  #   File-based persistence (Opus)
└── docs/
    ├── architecture.md          # L2: Read when relevant
    └── decisions/               # L3: ADRs, deep reference
```

**Key principles:**
- `.claude/` is the LLM's "home" — predictable, stable, cached
- `docs/` is the LLM's "library" — navigated on demand
- `.agents/` is the LLM's "notebook" — written to during work

---

## Pattern 1: Web Application (Next.js / React / Vue)

```
project/
├── CLAUDE.md
├── .claude/
│   ├── rules/
│   │   ├── frontend-conventions.md
│   │   ├── api-patterns.md
│   │   └── testing-strategy.md
│   └── skills/
├── src/
│   ├── app/                     # Routes / pages
│   │   ├── CLAUDE.md            # Page-specific conventions
│   │   └── {route}/
│   ├── components/
│   │   ├── ui/                  # Design system primitives
│   │   └── features/            # Feature-specific components
│   ├── lib/                     # Shared utilities (named by domain)
│   │   ├── auth.ts
│   │   ├── api-client.ts
│   │   └── validation.ts
│   └── types/                   # Shared type definitions
├── tests/
│   ├── e2e/
│   └── unit/
├── docs/
│   ├── architecture.md
│   └── api/
├── scripts/
└── config/                      # Environment configs (stable)
```

**LLM optimization notes:**
- `lib/` uses domain-descriptive names (not `utils.ts`)
- Components split by ui/features for focused navigation
- `config/` separated for cache stability

---

## Pattern 2: API Service (Express / Fastify / Hono)

```
project/
├── CLAUDE.md
├── .claude/rules/
├── src/
│   ├── routes/                  # Route definitions (discoverable via grep)
│   │   ├── users.ts
│   │   ├── payments.ts
│   │   └── index.ts             # Route registry
│   ├── services/                # Business logic by domain
│   │   ├── user-service.ts
│   │   └── payment-service.ts
│   ├── models/                  # Data models
│   ├── middleware/              # Auth, validation, logging
│   └── types/
├── tests/
│   ├── routes/                  # Mirror src/ structure
│   └── services/
├── docs/
│   ├── api-spec.yaml            # OpenAPI spec
│   └── architecture.md
├── scripts/
│   ├── seed-db.ts
│   └── migrate.ts
└── config/
```

**LLM optimization notes:**
- Routes mirror domain (user, payment) — grep-friendly
- Test structure mirrors src/ — predictable navigation
- Scripts named by action (seed, migrate) — self-documenting

---

## Pattern 3: Monorepo (Turborepo / Nx / pnpm workspaces)

```
monorepo/
├── CLAUDE.md                    # Workspace-wide rules
├── .claude/
│   ├── rules/
│   │   ├── workspace-policy.md  # Cross-package conventions
│   │   └── dependency-rules.md  # Import boundary rules
│   └── skills/
├── packages/
│   ├── api/
│   │   ├── CLAUDE.md            # Package-specific overrides
│   │   ├── src/
│   │   └── tests/
│   ├── web/
│   │   ├── CLAUDE.md
│   │   ├── src/
│   │   └── tests/
│   └── shared/
│       ├── CLAUDE.md
│       └── src/
├── docs/
│   ├── architecture.md          # System-level architecture
│   └── package-boundaries.md    # Import rules visualization
├── scripts/
│   ├── setup.sh
│   └── check-boundaries.ts
└── config/                      # Shared configs (tsconfig, eslint)
```

**LLM optimization notes:**
- Each package has its own CLAUDE.md for scoped rules
- Root CLAUDE.md defines workspace-wide conventions
- `shared/` is explicitly named (not `common/` or `utils/`)
- `config/` at root for stable cache prefix

---

## Pattern 4: Python Package (FastAPI / Django / CLI)

```
project/
├── CLAUDE.md
├── .claude/rules/
├── src/
│   └── {package_name}/
│       ├── __init__.py
│       ├── api/                 # HTTP layer
│       │   ├── routes.py
│       │   └── dependencies.py
│       ├── domain/              # Business logic
│       │   ├── models.py
│       │   └── services.py
│       ├── infrastructure/      # DB, external services
│       │   ├── database.py
│       │   └── cache.py
│       └── config.py            # Settings
├── tests/
│   ├── conftest.py
│   ├── test_api/
│   └── test_domain/
├── docs/
├── scripts/
└── pyproject.toml
```

---

## Migration Checklist

When restructuring an existing project:

1. **Map current structure** — `tree -L 3 --dirsfirst`
2. **Identify LLM pain points** — Which files are hard to find? Which are bloated?
3. **Draft target structure** — Use the closest pattern above as a starting point
4. **Plan file moves** — Generate a migration script (mv commands)
5. **Update references** — Fix import paths, CI configs, build scripts
6. **Add LLM layer** — CLAUDE.md hierarchy, `.claude/rules/`, `.agents/`
7. **Verify** — Run discovery test, check build, run tests
