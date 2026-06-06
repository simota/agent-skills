# Context Analysis

Purpose: load this during `SCAN` to detect the project's real stack, conventions, rule files, existing skills, and evolution signals before generating anything.

## Contents

1. Tech stack detection
2. Structure and naming
3. Monorepo and polyglot handling
4. Rules and config precedence
5. Existing skill audit
6. Style-profile extraction

## Tech Stack Detection

### Manifest File Mapping

| File | Stack | Inspect for |
|------|-------|-------------|
| `package.json` | Node.js / JavaScript / TypeScript | dependencies, devDependencies, scripts, workspaces |
| `tsconfig.json` | TypeScript | strictness, `paths`, `baseUrl` |
| `go.mod` | Go | module path, dependencies |
| `Cargo.toml` | Rust | dependencies, features |
| `pyproject.toml` / `setup.py` / `requirements.txt` | Python | framework and tool dependencies |
| `Gemfile` | Ruby | gems and Rails presence |
| `pom.xml` / `build.gradle` | Java / Kotlin | starters, plugins |
| `composer.json` | PHP | framework and autoloading |
| `pubspec.yaml` | Dart / Flutter | packages and SDK |
| `mix.exs` | Elixir | deps |
| `bun.lockb` / `bunfig.toml` | Bun | Bun runtime usage |

### Framework Detection

| Framework | Detection signal | Likely priority skills |
|-----------|------------------|------------------------|
| Next.js | `next` dependency + `next.config.*` | `new-page`, `new-api-route`, `new-component` |
| React (Vite / CRA) | `react` without `next` | `new-component`, `new-hook`, `new-context` |
| Vue.js | `vue` dependency | `new-component`, `new-composable`, `new-store` |
| Nuxt | `nuxt` dependency | `new-page`, `new-server-route`, `new-composable` |
| Remix | `@remix-run/node` dependency | `new-route`, `new-loader`, `new-action` |
| Express | `express` dependency | `new-route`, `new-middleware`, `new-controller` |
| Fastify | `fastify` dependency | `new-route`, `new-plugin`, `new-schema` |
| Hono | `hono` dependency | `new-route`, `new-middleware`, `new-validator` |
| NestJS | `@nestjs/core` dependency | `new-module`, `new-controller`, `new-service` |
| tRPC | `@trpc/server` dependency | `new-router`, `new-procedure`, `new-middleware` |
| FastAPI | `fastapi` in Python manifests | `new-router`, `new-model`, `new-schema` |
| Django | `django` in Python manifests | `new-app`, `new-model`, `new-view` |
| Rails | `rails` in `Gemfile` | `new-model`, `new-controller`, `new-migration` |
| Go stdlib / Chi / Echo | `go.mod` without larger framework or with router deps | `new-handler`, `new-middleware`, `new-model` |
| Gin | `github.com/gin-gonic/gin` | `new-handler`, `new-middleware` |
| Actix / Axum | Rust web framework in `Cargo.toml` | `new-handler`, `new-service` |
| Spring Boot | `spring-boot-starter*` | `new-controller`, `new-service`, `new-repository` |
| Laravel | `laravel/framework` | `new-controller`, `new-model`, `new-migration` |
| Flutter | `flutter` SDK | `new-screen`, `new-widget`, `new-bloc` |
| SvelteKit | `@sveltejs/kit` | `new-route`, `new-component`, `new-server` |

## Structure and Naming

### Directory Signals

| Pattern | Meaning | Skill impact |
|---------|---------|--------------|
| `src/app/` | App Router or route-first structure | Route-oriented templates |
| `src/pages/` | Pages Router or Nuxt-style routing | File-based route templates |
| `src/components/` | Shared components | Component creation skills |
| `src/hooks/` / `src/composables/` | Reusable logic layer | Hook/composable skills |
| `src/lib/` / `src/utils/` | Utility helpers | Utility templates |
| `src/services/` | Service layer present | Service and integration skills |
| `src/stores/` / `src/store/` | Centralized state | State-management skills |
| `__tests__/` / `*.test.*` / `*.spec.*` | Test layout | Test placement and naming |
| `e2e/` / `cypress/` / `playwright/` | E2E test framework | End-to-end testing conventions |
| `prisma/` / `drizzle/` / `migrations/` | Database stack | Schema and migration skills |
| `cmd/` / `internal/` | Go package layout | CLI and internal package patterns |

### Naming Detection

Check at least `3+` existing files of the same kind before templating:

1. File names: `kebab-case`, `camelCase`, `PascalCase`, `snake_case`
2. Component names: `Button.tsx` vs `button/index.tsx`
3. Test layout: colocated vs separate `__tests__/`
4. Import style: relative imports, aliases, barrel exports

## Monorepo and Polyglot Handling

### Monorepo Detection

| File | Tool | Scope signal |
|------|------|--------------|
| `turbo.json` | Turborepo | pipeline and package graph |
| `nx.json` | Nx | projects and target defaults |
| `pnpm-workspace.yaml` | pnpm workspaces | workspace globs |
| `lerna.json` | Lerna | managed packages |
| root `package.json` with `workspaces` | npm/yarn workspaces | workspace entries |

### Monorepo Strategy

1. Scan the root to detect the monorepo tool and package graph.
2. Run full `SCAN` per package.
3. Generate shared root skills for cross-cutting concerns only.
4. Generate package-specific skills for framework-specific workflows.
5. Never duplicate a root skill inside a package.

### Package Priority Order

1. Primary application packages
2. API / backend packages
3. Shared libraries
4. Tooling packages

### Polyglot Detection

| Pattern | Strategy |
|---------|----------|
| `package.json` + `go.mod` | Separate JS/TS and Go skill sets; share conventions |
| `package.json` + `pyproject.toml` | Separate JS/TS and Python skill sets; share conventions |
| `Cargo.toml` + `package.json` | Add bridge skills only for interop boundaries |
| Multiple manifests in subdirectories | Scope skills per directory or package |

For ambiguous names, prefix the skill directory with the language: `ts-new-component`, `go-new-handler`, `py-new-router`.

## Rules and Config Precedence

### Convention Priority

1. Explicit config and rule files
2. Existing code patterns
3. Framework defaults
4. Community standards

### Rule Files to Inspect

- `CLAUDE.md`
- `.cursorrules`
- `.windsurfrules`
- `AGENTS.md`
- `.github/copilot-instructions.md`

### Config Files to Inspect

| File group | What to infer |
|------------|---------------|
| `.eslintrc*`, `eslint.config.*`, `.prettierrc*`, `.editorconfig` | naming, formatting, import expectations |
| `tsconfig.json` | aliases, module resolution, strictness |
| `Makefile`, `Taskfile.yml` | recurring commands worth skilling |
| `docker-compose.yml` | service topology and local dev flow |
| `.github/workflows/*.yml` | CI/CD and deployment workflows |
| `.husky/`, `.lefthook.yml` | git-hook expectations |

## Existing Skills Audit

Before generating or updating skills, inspect:

1. Project `.claude/skills/`
2. Project `.agents/skills/`
3. Project `CLAUDE.md`
4. Ecosystem agents, to avoid overlapping core functions

### Deduplication Rules

A skill already exists if any of these are true:

- Same name exists in either project skill directory
- Functional overlap is greater than `70%`
- It duplicates an ecosystem agent's core function

### Directory Sync Check

Both directories must stay identical.

1. List skills in `.claude/skills/` and `.agents/skills/`
2. Find orphans that exist in only one directory
3. Copy the orphan to the missing directory before new generation
4. Report every sync repair

## Style-Profile Extraction

When the project already contains skills, learn their style before authoring new ones.

### What to Sample

- Section ordering and naming
- Description tone
- Heading language
- Template depth
- Example style
- Checklist usage

### Extraction Rules

1. Read all existing skills in both directories.
2. Use majority patterns when at least `10+` comparable files exist.
3. Match language, structure, and depth unless the existing pattern is clearly low quality.
4. If existing skills are low quality, note the drift and do not propagate the defect.
5. If no existing skills exist, use Sigil defaults from `skill-templates.md`.
