# Advanced Patterns

Purpose: load this during `CRAFT` when one skill must cover variants, monorepo scopes, parameterized templates, or explicit composition with other skills.

## Contents

1. Conditional branches
2. Parameterized templates
3. Monorepo scoping
4. Skill composition
5. Multi-language naming

## Conditional Branches

Use conditional branches when the project has multiple valid implementations and guessing would change behavior.

### Framework-Version Branching

```markdown
## Templates

### Next.js App Router (next >= 13.4)
\```tsx
export default async function Page() { /* Server Component pattern */ }
\```

### Next.js Pages Router (next < 13.4)
\```tsx
export const getServerSideProps = async () => ({ props: {} })
\```
```

### Styling Branching

```markdown
## Styling

### Tailwind CSS
\```tsx
<div className="flex items-center gap-4" />
\```

### CSS Modules
\```tsx
import styles from './Component.module.css'
<div className={styles.container} />
\```
```

Rules:
- Detect the branch during `SCAN`.
- Include every applicable branch; do not collapse them into one guessed path.
- Mark the detected default branch as `(used in this project)`.

## Parameterized Templates

### Standard Variables

| Variable | Source | Example |
|----------|--------|---------|
| `[ProjectName]` | manifest | `my-app` |
| `[Framework]` | framework detection | `Next.js` |
| `[FrameworkVersion]` | manifest dependencies | `14.1.0` |
| `[ComponentDir]` | directory scan | `src/components` |
| `[TestDir]` | test layout | `__tests__` |
| `[TestFramework]` | dependencies | `vitest` |
| `[CSSApproach]` | config or deps | `tailwind` |
| `[PackageManager]` | lock file | `pnpm` |
| `[ImportAlias]` | `tsconfig.json` | `@/` |

### Substitution Rules

1. Replace every variable before installation.
2. If the value is unknown, use the framework default and add `<!-- TODO: verify -->`.
3. If there are multiple valid values, branch explicitly.
4. Never leave raw placeholders in installed skills.

## Monorepo Scoping

### Detection

| Signal | Scope strategy |
|--------|----------------|
| `turbo.json` | root shared skills + per-package skills |
| `nx.json` | per-project skills + library skills |
| `pnpm-workspace.yaml` | per-package skills |
| `lerna.json` | per-package skills |
| `packages/*/package.json` | generic package-based scoping |

### Rules

- Root skills cover cross-cutting concerns only.
- Package skills cover framework-specific workflows.
- Never duplicate a root skill inside a package.
- Keep `.claude/skills/` and `.agents/skills/` synchronized at every level.

## Skill Composition

Use composition when one skill depends on another but should remain separate.

### Prerequisite Chain

```markdown
## Prerequisites
- Follow `naming-rules`
- Run `env-setup` first
```

### Workflow Orchestration

```markdown
## End-to-End Flow

1. `new-model`
2. `new-service`
3. `new-controller`
4. `new-test`
```

Rules:
- Reference other skills by `name`.
- Never copy another skill's full content into a new one.
- If dependencies become circular, merge the skills instead.
- Keep composition chains to `4-5` skills maximum.

## Multi-Language Naming

Use language prefixes only when the project contains multiple active stacks and the unprefixed name would be ambiguous.

Examples:
- `ts-new-component`
- `go-new-handler`
- `py-new-router`

Shared cross-language skills stay unprefixed:
- `naming-rules`
- `pr-template`
- `deploy-flow`
- `env-setup`

For style-profile extraction and language mirroring, use `context-analysis.md`.
