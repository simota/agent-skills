# Skill Catalog

Purpose: load this during `DISCOVER` to map detected frameworks to likely high-value skills and to preserve known migration paths during evolution.

## Contents

1. JavaScript / TypeScript
2. Python
3. Go
4. Ruby
5. Rust
6. Cross-framework skills
7. Discovery priority
8. Evolution-path usage

## JavaScript / TypeScript

### Next.js (App Router)

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-page` | Micro | Create an App Router page with `metadata` and Server Component defaults | Pages Router -> App Router |
| `new-api-route` | Micro | Create a Route Handler for `GET/POST/PUT/DELETE` | API Routes -> Route Handlers |
| `new-component` | Micro | Create a React component with typed props and tests | Class -> Functional -> Server Component |
| `new-server-action` | Micro | Create a Server Action with validation and errors | Native to App Router |
| `data-fetching` | Full | Project-specific fetch, cache, and revalidation patterns | `getServerSideProps` -> Server Component fetch |
| `auth-pattern` | Full | Middleware, session, and protected-route patterns | — |
| `form-handling` | Full | Forms with validation, mutations, and error flow | Client-only -> hybrid Server Action |

### Next.js (Pages Router)

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-page` | Micro | Create a page with `getServerSideProps` or `getStaticProps` | -> App Router `new-page` |
| `new-api-route` | Micro | Create an API Route using `req` / `res` | -> App Router `new-api-route` |

### React (Vite / CRA)

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-component` | Micro | Create a component with props and tests | CRA -> Vite |
| `new-hook` | Micro | Create a custom hook with types and tests | — |
| `new-context` | Micro | Create a Context provider and consumer hook | Context -> Zustand / Jotai |
| `state-management` | Full | Standardize local store architecture and migrations | Redux -> Redux Toolkit -> Zustand |

### Vue.js / Nuxt

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-component` | Micro | Create an SFC with `script setup` and typed props | Options API -> Composition API |
| `new-composable` | Micro | Create a reactive composable with tests | Mixin -> Composable |
| `new-store` | Micro | Create a Pinia store | Vuex -> Pinia |
| `new-page` | Micro | Create a Nuxt page with `definePageMeta` | Nuxt 2 -> Nuxt 3 |

### Remix

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-route` | Micro | Create a route module with loader, action, and component | — |
| `new-loader` | Micro | Create a loader with data and error handling | — |
| `new-action` | Micro | Create an action with validation and mutation flow | — |
| `error-boundary` | Micro | Create `ErrorBoundary` and `CatchBoundary` | — |
| `auth-pattern` | Full | Session, cookie, and protected-route patterns | — |

### Express / Fastify

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-route` | Micro | Create a validated route handler | Express -> Fastify |
| `new-middleware` | Micro | Create middleware with project conventions | — |
| `new-controller` | Micro | Create a controller wired to the service layer | — |
| `error-handling` | Full | Standardize error classes and response mapping | — |
| `auth-middleware` | Full | Authentication and role-based authorization middleware | — |

### Hono

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-route` | Micro | Create a typed Hono route | Express -> Hono |
| `new-middleware` | Micro | Create Hono middleware | — |
| `new-validator` | Micro | Integrate Zod or Valibot validation | — |
| `api-pattern` | Full | REST API conventions with docs and errors | — |

### tRPC

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-router` | Micro | Create a router with procedures | REST -> tRPC |
| `new-procedure` | Micro | Create query, mutation, or subscription procedures | — |
| `new-middleware` | Micro | Create auth or logging middleware | — |
| `trpc-pattern` | Full | Full-stack tRPC patterns across client and server | — |

### NestJS

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-module` | Micro | Scaffold module, controller, and service | — |
| `new-guard` | Micro | Create auth or authorization guards | — |
| `new-pipe` | Micro | Create validation pipes | — |
| `new-interceptor` | Micro | Create logging or transformation interceptors | — |

### Bun

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-server` | Micro | Create a `Bun.serve` entrypoint | Node.js -> Bun |
| `new-test` | Micro | Create tests with `bun:test` | Jest -> Bun test |
| `new-script` | Micro | Create Bun scripts for shell or file tasks | — |

## Python

### FastAPI

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-router` | Micro | Create an `APIRouter` with models and dependency injection | Flask -> FastAPI |
| `new-model` | Micro | Create an ORM model | — |
| `new-schema` | Micro | Create a Pydantic schema | Pydantic v1 -> v2 |
| `crud-pattern` | Full | CRUD flow across router, service, and repository | — |
| `auth-pattern` | Full | OAuth2, JWT, and dependency-based auth | — |

### Django

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-app` | Micro | Create an app with models, views, urls, and admin | — |
| `new-model` | Micro | Create a model and migration | — |
| `new-view` | Micro | Create class-based or function-based views | FBV -> CBV |
| `new-serializer` | Micro | Create a DRF serializer | — |
| `new-command` | Micro | Create a management command | — |

### Flask

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-blueprint` | Micro | Create a blueprint with routes and templates | Flask -> FastAPI |
| `new-model` | Micro | Create a SQLAlchemy model | — |

## Go

### Go (stdlib / Chi / Echo)

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-handler` | Micro | Create an HTTP handler with request parsing and response flow | `net/http` -> Chi / Echo |
| `new-middleware` | Micro | Create logging, auth, or CORS middleware | — |
| `new-model` | Micro | Create structs and repository scaffolding | — |
| `new-service` | Micro | Create service interfaces and implementations | — |
| `error-handling` | Full | Standardize sentinel errors, wrapping, and response mapping | — |
| `testing-pattern` | Full | Table-driven, mock, and integration testing patterns | — |

### Gin

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-handler` | Micro | Create a Gin handler with binding and response flow | Gin -> Chi / Echo |
| `new-middleware` | Micro | Create Gin middleware | — |

## Ruby

### Rails

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-model` | Micro | Create an ActiveRecord model with validations and associations | — |
| `new-controller` | Micro | Create a controller with strong params and filters | — |
| `new-migration` | Micro | Create a migration | — |
| `new-service` | Micro | Create a Service Object | — |
| `new-job` | Micro | Create an ActiveJob | — |
| `api-endpoint` | Full | Build an API endpoint with serializer, auth, and tests | — |

## Rust

### Actix-web / Axum

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `new-handler` | Micro | Create a handler with extractors and response types | Actix -> Axum |
| `new-middleware` | Micro | Create middleware | — |
| `error-handling` | Full | Define error types and response conversion | — |

## Cross-Framework Skills

| Skill | Type | Description | Evolution path |
|-------|------|-------------|----------------|
| `naming-rules` | Micro | Capture project naming conventions | Project-specific |
| `pr-template` | Micro | Standardize PR descriptions and checks | — |
| `env-setup` | Micro | Document environment and setup steps | — |
| `deploy-flow` | Full | Deployment workflow, checks, and rollback guidance | Platform-specific evolution |
| `incident-response` | Full | Escalation, diagnosis, and recovery workflow | — |
| `onboarding` | Full | New teammate onboarding path | — |
| `code-review` | Micro | Review checklist tailored to the project | — |
| `testing-guide` | Full | Unit, integration, and E2E testing strategy | — |

## Discovery Priority

Prioritize candidates in this order:

1. High frequency
2. High complexity
3. High risk
4. Onboarding value
5. Consistency value

## Evolution-Path Usage

Use the evolution-path column during updates:

1. Compare the current project state to the listed path.
2. If migration is detected, use the path to guide the update.
3. If the path is `—`, prefer in-place updates for minor version changes.
4. Framework switches usually require replacement, not in-place editing.


---

# Worked Examples

Canonical home for the invocation examples referenced from `SKILL.md`.

Representative invocations and their expected behavior. Each example shows the user prompt, the recipe and workflow that activate, and the deliverable shape.

### Example 1: Project-local skill generation (default recipe)

> User: "Generate skills for this Next.js + Prisma + tRPC project."

- Subcommand: none → default `generate` recipe.
- Workflow: `SCAN → DISCOVER → CRAFT → INSTALL → VERIFY → ATTUNE`.
- SCAN detects Next.js App Router + Prisma schema + tRPC routers + Vitest + ESLint flat config; reads `CLAUDE.md` if present.
- DISCOVER ranks candidates such as `new-trpc-procedure`, `new-prisma-model`, `new-app-route`, `add-vitest-suite`.
- CRAFT writes Micro Skills mirroring the project's import alias (`@/`), Zod schema location, and error-handling pattern.
- INSTALL writes identical content to `.claude/skills/<name>/SKILL.md` and `.agents/skills/<name>/SKILL.md`.
- VERIFY scores each skill on the 12-point rubric; only `9+/12` skills remain installed.
- ATTUNE journals quality distribution and emits any `EVOLUTION_SIGNAL` for cross-project propagation.
- Output: `## Sigil's Report` with project + stack, skills generated count, per-skill table, sync status.

### Example 2: Stale-skill refresh after framework migration

> User: "We just upgraded from Next.js 14 to 15. Refresh our skills."

- Subcommand: `migrate` (Migrate Existing recipe).
- Workflow: Skill Evolution path — `SCAN → DIFF → PLAN → UPDATE → VERIFY → ATTUNE`.
- SCAN re-detects framework version from `package.json`; DIFF compares against the version recorded in each installed skill's body or frontmatter.
- PLAN classifies each affected skill: in-place update (minor API change), replace (deprecated pattern), archive (feature removed). Asks user before archiving any actively used skill.
- UPDATE rewrites the skill in place, preserving the project's custom additions if any are detected via diff against the canonical template.
- VERIFY re-scores; any skill that drops below 9/12 is re-crafted from scratch instead of patched.
- ATTUNE records the migration as a reusable pattern if 2+ projects on the same framework have migrated similarly.

### Example 3: Skill quality audit

> User: "Audit the skills in this repo — which ones are stale?"

- Subcommand: none, but Output Routing matches `audit skills` signal.
- Workflow: `SCAN → VERIFY` (no generation).
- SCAN inventories both `.claude/skills/` and `.agents/skills/`; detects sync drift if directories diverge.
- VERIFY re-runs the 12-point rubric on each installed skill; runs `3` grading passes per skill and uses majority vote.
- Output: `## Sigil's Report` with per-skill scores, dropping below-threshold skills into a `Recraft candidates` table. No file changes unless the user confirms remediation.

### Example 4: Sync drift repair

> User: "`.claude/skills/` and `.agents/skills/` are out of sync — fix it."

- Subcommand: none, Output Routing matches `sync drift` signal.
- Workflow: `SCAN → sync repair`.
- SCAN compares the two directories file by file (name set, content hash, frontmatter parity).
- Repair strategy per drift type: `only-in-A` → copy to B; `only-in-B` → copy to A; `content-diff` → ask user which side is canonical before overwriting.
- Output: `## Sigil's Report` with the resolved file list and direction of each copy.

