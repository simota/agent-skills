# Project Scaffolding Anti-Patterns

Purpose: Use this reference when auditing initial repository setup, template design, config hygiene, and staged structure growth.

## Contents

- Scaffolding anti-pattern catalog
- Progressive scaffolding strategy
- Config hygiene rules
- Template-repository design
- AI-era scaffolding rules
- Startup checklist
- Grove integration

Initial repository setup failures, template traps, and config-management risks.

## 1. Project Scaffolding Anti-Patterns

| ID | Anti-Pattern | What Goes Wrong | Typical Signals | Recommended Response |
|---|---|---|---|---|
| **PS-01** | **Template Cargo Cult** | A team copies a FAANG-scale repository layout wholesale. | Many unused directories exist and nobody understands the tooling. | Start from the smallest structure that fits the team and domain. |
| **PS-02** | **Skeleton Overload** | The project starts with too much empty structure. | Empty `features/`, `adr/`, or `auth/` trees exist before any code. | Add directories only when the project actually needs them. |
| **PS-03** | **Config Proliferation** | Config files multiply early and drift apart. | `15+` config files live at the root; overlapping configs coexist. | Consolidate with flat config, inheritance, or a dedicated `config/` directory. |
| **PS-04** | **Framework Lock-in Structure** | The layout overfits one framework. | A framework swap forces a full directory redesign. | Prefer domain-centered structure with framework adapters at the edges. |
| **PS-05** | **AI-Generated Chaos** | AI tools invent structure ad hoc. | Generated files land in inconsistent places and patterns drift. | Establish scaffolding before AI-assisted generation and document placement rules. |
| **PS-06** | **Monorepo Premature** | A single app starts in monorepo form without real need. | `apps/web/` and `packages/` exist but hold only one application. | Start as a single repository and split only when real package boundaries emerge. |
| **PS-07** | **Convention Blindness** | The layout ignores language or framework defaults. | Go uses `src/`; Next.js uses a custom router layout; Django skips app conventions. | Detect the platform first and apply the official structural baseline. |

## 2. Progressive Scaffolding Strategy

| Phase | Typical size | Structure rule |
|---|---|---|
| Phase 0 | Prototype | `src/`, `README.md`, `.gitignore`, language config only |
| Phase 1 | Up to `20` files | Add `tests/`, `docs/`, `scripts/`, `.github/` only when first needed |
| Phase 2 | `20-100` files | Start feature grouping, extract shared code, split tests by scope |
| Phase 3 | `100+` files | Evaluate FSD, DDD, stricter module boundaries, or package splits |

Core rules:
- do not create empty directories speculatively
- let structure evolve with code volume
- prefer staged refactors over upfront full design

## 3. Config Hygiene Rules

Root-required config:
- `package.json` / `pyproject.toml` / `go.mod`
- `tsconfig.json`
- `turbo.json` / `nx.json` if monorepo
- `.gitignore`

Root-recommended config:
- `eslint.config.js`
- `prettier.config.js`
- `vitest.config.ts` or `jest.config.ts`

Usually movable to `config/`:
- `webpack.config.js`
- `postcss.config.js`
- `docker-compose.yml`

Consolidation guidance:
- move to ESLint flat config
- use `extends` for TypeScript config families
- keep one test runner
- keep one formatter
- keep one bundler unless there is a proven need

Thresholds:
- `<=10` config files at root: healthy
- `10-15`: review for consolidation
- `15+`: treat as `AP-003`

## 4. Template Repository Design

Required template elements:
- `README.md`
- `.gitignore`
- language configuration
- CI workflow
- `.editorconfig`

Optional elements:
- `docs/` skeleton for larger projects
- `tests/` starter structure
- `.agents/`
- `CLAUDE.md` or cursor rules when the team uses AI tooling

Do not include:
- tool configs the project will not use
- many empty feature directories
- project-specific business logic
- hard-coded project names or URLs
- outdated dependencies

Refresh templates quarterly or when core tooling conventions change.

## 5. AI-Era Scaffolding Rules

To help AI understand structure:
- document directory conventions
- document naming rules
- expose public APIs clearly
- add directory-level READMEs only when they carry real decision value

To control AI generation:
- finish scaffolding before broad AI-assisted generation
- specify expected destination directories explicitly
- verify structural consistency after generation

Do not accept AI-suggested structure uncritically. Team size, domain shape, and project maturity still decide the right structure.

## 6. Startup Checklist

At project start:
- detect language and framework
- confirm the standard layout for that stack
- start with Phase 0
- add `README.md`, `.gitignore`, and language config
- add a basic CI workflow
- add `.editorconfig`

Add later as needed:
- `tests/` at first test
- `docs/` at first spec
- `scripts/` at first automation script
- `features/` at `20+` files
- `shared/` when duplication appears
- stronger module boundaries at `100+` files

Avoid:
- designing the full structure on day one
- copying another project’s tree wholesale
- creating many empty folders
- adding tools with no immediate use

## 7. Grove Integration

Use this reference in Grove as follows:
1. Screen `PS-01` through `PS-07`.
2. Apply staged scaffolding for new repositories.
3. Run config-hygiene checks for existing repositories.
4. Audit template repositories periodically.

Quality gates:
- copied enterprise template: require scale-fit review
- many empty directories: propose the minimum viable structure
- `15+` root configs: propose consolidation
- convention violations: propose the standard template
- one-app monorepo shell: recommend a single-repo baseline

**Source:** [Iterators: Project Codebase Organization](https://www.iteratorshq.com/blog/a-comprehensive-guide-on-project-folder-organization/) · [GitHub Well-Architected: Anti-Patterns](https://wellarchitected.github.com/library/scenarios/anti-patterns/) · [FnJoin: Code Your Own Scaffolding First](https://fnjoin.com/post/2025-12-21-code-your-own-scaffolding-first/)
