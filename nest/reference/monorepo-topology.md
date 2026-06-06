# Monorepo Topology for LLM Efficiency

Reference for Nest's `monorepo` recipe. Design per-workspace CLAUDE.md cascade, package boundaries, and shared rule deduplication for turborepo / nx / pnpm-workspace / yarn workspaces.

---

## 1. Monorepo Tool Detection

```bash
# Detect tool by config presence
[ -f turbo.json ]              && echo "turborepo"
[ -f nx.json ]                 && echo "nx"
[ -f pnpm-workspace.yaml ]     && echo "pnpm"
grep -q '"workspaces"' package.json 2>/dev/null && echo "yarn/npm workspaces"
[ -f Cargo.toml ] && grep -q '\[workspace\]' Cargo.toml && echo "cargo workspaces"
[ -f go.work ]                 && echo "go workspaces"
```

Per-tool conventions:

| Tool | Default workspace dir | Cache hint |
|---|---|---|
| turborepo | `apps/` + `packages/` | `turbo.json` defines pipelines |
| nx | `apps/` + `libs/` | `nx.json` + `project.json` |
| pnpm | per `pnpm-workspace.yaml` globs | `.npmrc` shared |
| yarn/npm | per `workspaces` field | hoisting affects path resolution |

---

## 2. CLAUDE.md Cascade Design

### 3-tier model
```
monorepo-root/
├── CLAUDE.md                          # Tier 1: universal rules
├── .claude/
│   └── rules/                         # Tier 1 imports
│       ├── monorepo-conventions.md
│       └── security-rules.md
├── apps/
│   ├── web/
│   │   └── CLAUDE.md                  # Tier 2: app-specific (TypeScript, Next.js)
│   └── api/
│       └── CLAUDE.md                  # Tier 2: app-specific (Python, FastAPI)
└── packages/
    ├── ui/
    │   └── CLAUDE.md                  # Tier 2: package-specific (React, design tokens)
    └── shared/
        └── CLAUDE.md                  # Tier 2: package-specific (utility lib)
```

### Tier responsibilities

| Tier | Path | Content | Token budget |
|---|---|---|---|
| 1 | root `CLAUDE.md` | Universal: licensing, monorepo tool, security, branching | 150-250 |
| 2 | per-workspace `CLAUDE.md` | Stack-specific: language, framework, test runner, lint | 80-150 |
| 3 | module-level `CLAUDE.md` (rare) | Single-file overrides for unusual modules | 30-60 |

**Rule**: Tier N inherits all rules from Tier 1..N-1. Override only what differs.

---

## 3. Deduplication via `@import`

Common pattern: same lint/format rules across all TypeScript packages.

### Bad — duplicated
```markdown
# apps/web/CLAUDE.md
- ESLint: @typescript-eslint/strict
- Prettier: 2-space indent, single quotes
- Test: vitest with happy-dom

# packages/ui/CLAUDE.md
- ESLint: @typescript-eslint/strict
- Prettier: 2-space indent, single quotes
- Test: vitest with happy-dom
```

### Good — extracted
```markdown
# .claude/rules/typescript.md
- ESLint: @typescript-eslint/strict
- Prettier: 2-space indent, single quotes
- Test: vitest with happy-dom

# apps/web/CLAUDE.md
@../../.claude/rules/typescript.md

## Web-specific
- Framework: Next.js 15
- Routing: app router only
```

```markdown
# packages/ui/CLAUDE.md
@../../.claude/rules/typescript.md

## UI-specific
- Component conventions: see Storybook
- Token system: @repo/design-tokens
```

Drop in shared blocks via `@import`; keep workspace files lean.

---

## 4. Package Boundaries

### Naming convention
```
apps/{app-name}/         # End-user deployables (web, mobile, cli)
packages/{pkg-name}/     # Shared libraries (ui, utils, types)
libs/{lib-name}/         # Pure logic libraries (nx convention)
services/{svc-name}/     # Backend services (separate deploy units)
tools/{tool-name}/       # Internal dev tooling (codegen, scripts)
configs/{cfg-name}/      # Shared configs (eslint-config, tsconfig)
```

### Path alias alignment
TypeScript `tsconfig.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "@repo/ui": ["./packages/ui/src"],
      "@repo/utils": ["./packages/utils/src"],
      "@repo/api-client": ["./packages/api-client/src"]
    }
  }
}
```

CLAUDE.md should mirror these aliases:
```markdown
# .claude/rules/imports.md
- Use `@repo/*` aliases — never relative paths across packages
- `@repo/ui` → React component library
- `@repo/utils` → Pure utility functions
- `@repo/api-client` → Generated REST/GraphQL client
```

LLM consistency: agents now know aliases without grep'ing tsconfig.

---

## 5. Discoverability Patterns

### Workspace listing
Add to root `CLAUDE.md`:
```markdown
## Workspaces

| Path | Purpose | Stack |
|---|---|---|
| `apps/web` | Marketing site | Next.js 15, TypeScript |
| `apps/dashboard` | Admin UI | Vite + React, TypeScript |
| `apps/api` | Public REST API | FastAPI, Python 3.12 |
| `packages/ui` | Component library | React 19, Storybook |
| `packages/utils` | Shared utils | Pure TypeScript |
| `services/worker` | Background jobs | Bun, TypeScript |
```

LLM can route file searches to the right workspace immediately.

### Glob patterns LLM should know
```markdown
## Glob patterns

| Find | Pattern |
|---|---|
| All package CLAUDE.md | `{apps,packages,services,libs}/*/CLAUDE.md` |
| All TypeScript sources | `{apps,packages}/*/src/**/*.ts` |
| All tests | `**/*.{test,spec}.{ts,tsx,js,py}` |
| All package.json | `{apps,packages,services,libs}/*/package.json` |
| Config files | `{**/,}*.config.*` |
```

---

## 6. Polyglot Monorepo Handling

When mixing languages (TypeScript + Python + Go), shard rules by language:

```
.claude/rules/
├── universal.md          # Git, security, naming (language-agnostic)
├── typescript.md         # Imported by TS packages
├── python.md             # Imported by Python packages
└── go.md                 # Imported by Go packages
```

Each workspace `@import`s only what it needs:
```markdown
# apps/api/CLAUDE.md (Python)
@../../.claude/rules/universal.md
@../../.claude/rules/python.md

## API-specific
- Framework: FastAPI
- Async: asyncio (not trio)
```

Avoids LLM seeing irrelevant rules (Python agent doesn't need ESLint config).

---

## 7. Turborepo Pipeline Awareness

`turbo.json` defines task dependencies. LLM should respect these:

```markdown
# .claude/rules/turbo-tasks.md

## Task pipelines (from turbo.json)

| Task | Depends on | Cache |
|---|---|---|
| `build` | `^build` | yes |
| `test` | `^build` | yes (on test files only) |
| `lint` | — | yes |
| `dev` | — | no (persistent) |

## Rules
- Don't manually run `tsc` — use `turbo build`
- Don't bypass cache with `turbo --force` unless debugging
- Add new packages to root `pnpm-workspace.yaml` AND verify `turbo build` includes them
```

---

## 8. Nx Workspace Awareness

Nx uses `project.json` per project + `nx.json` for orchestration:

```markdown
# .claude/rules/nx-tasks.md

## Project queries
- List all projects: `nx show projects`
- See affected: `nx affected -t test --base=main`
- Project graph: `nx graph`

## Tags (from project.json `tags` field)
- `scope:web` — web apps
- `scope:api` — backend services
- `type:lib` — shared libs
- `type:feature` — feature modules

## Module boundaries (from .eslintrc)
- `scope:web` cannot import `scope:api`
- `type:feature` cannot import another `type:feature` directly
```

---

## 9. CI Path Alignment

Ensure CI workflows reference workspace paths consistently with CLAUDE.md cascade:

```yaml
# .github/workflows/ci.yml
on:
  pull_request:
    paths:
      - 'apps/web/**'
      - 'packages/ui/**'
      - 'packages/utils/**'
```

Document in root `CLAUDE.md`:
```markdown
## CI triggers
- Web app changes: `apps/web/**`, `packages/ui/**`, `packages/utils/**`
- API changes: `apps/api/**`, `packages/api-types/**`
- Cross-cutting: any `package.json`, `tsconfig*.json`, `.github/**`
```

---

## 10. Verification Checklist

| Check | Method |
|---|---|
| Each workspace has `CLAUDE.md` | `find apps packages services -maxdepth 2 -name CLAUDE.md` |
| Root rules apply to all | Spot-check: open random workspace CLAUDE.md, confirm cascade |
| No duplicated rule blocks | grep for distinctive rule strings across workspaces |
| Path aliases match tsconfig | Diff CLAUDE.md aliases vs `tsconfig.json` paths |
| Workspace table up-to-date | Diff with `pnpm-workspace.yaml` glob expansion |
| `@import` paths resolve | Verify each `@../../.claude/rules/*.md` exists |
| Token cost per workspace | Estimate sum (root + workspace + imports) ≤ 2,500 |
| LLM workspace routing | Discovery test: ask "where does X feature live?" |

---

## 11. Common Pitfalls

| Pitfall | Avoidance |
|---|---|
| Single root CLAUDE.md with all stacks → 5K+ tokens | Cascade by workspace |
| Each workspace duplicates lint/format rules | Extract to `.claude/rules/typescript.md`, `@import` |
| Workspace table drifts from `pnpm-workspace.yaml` | Generate via script or pre-commit hook |
| Path aliases in CLAUDE.md ≠ tsconfig.json | Single source of truth — generate one from the other |
| Polyglot rules dumped together → noisy | Shard by language |
| Module-level CLAUDE.md (Tier 3) used eagerly | Reserve for genuine outliers; don't over-fragment |
| `@import` paths break after workspace move | Use root-relative `@/.claude/rules/...` if tool supports |
| CI paths not aligned with CLAUDE.md scope | Cross-document in both |
| Nx tags / Turbo cache not surfaced to LLM | Document in `.claude/rules/{nx,turbo}-tasks.md` |
| Adding new workspace forgot to add CLAUDE.md | Pre-commit lint: every workspace must have CLAUDE.md |

---

## 12. Decision Walkthrough Template

```
Monorepo tool: □ turborepo  □ nx  □ pnpm  □ yarn/npm  □ cargo  □ go
Workspace dirs: ____________

Workspaces detected: ____ apps, ____ packages, ____ services, ____ libs

Languages: ____________

Cascade design:
  Tier 1 (root): ____ tokens
  Tier 2 (per-workspace avg): ____ tokens
  Tier 3 (module): used / not used

Shared rule files (`.claude/rules/`):
  □ universal.md
  □ typescript.md
  □ python.md
  □ go.md
  □ tool-specific (turbo / nx)
  □ ____________

Path alias source of truth: tsconfig.json / CLAUDE.md / generated

Workspace table maintained in: root CLAUDE.md / generated

CI paths cross-documented: ✓ / ✗

Verification:
  □ Each workspace has CLAUDE.md
  □ No duplicated rule blocks
  □ @import paths resolve
  □ Path aliases match tsconfig
  □ Total token cost per agent invocation ≤ 2,500
  □ Discovery test passes (workspace routing)
```

---

## 13. References
- Turborepo documentation
- Nx workspace documentation
- pnpm workspaces
- Cargo workspaces (Rust)
- Go workspaces (`go.work`)
- Claude Code `@import` cascade
