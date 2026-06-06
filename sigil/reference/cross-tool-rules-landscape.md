# Cross-Tool Rules Landscape

Purpose: load this during `SCAN` when the project uses multiple AI rule systems and Sigil must avoid generating skills that conflict with them.

## Contents

1. Tool comparison
2. Shared rule shapes
3. Interoperability strategies
4. Path-based scoping
5. Canonical rule file patterns (SCAN detection set)
6. Sigil implications

## Canonical Rule File Patterns

When running `SCAN`, detect convention sources by matching these glob patterns. Presence of any pattern in this set should trigger ingestion during the SCAN phase (the file's content informs naming/import/testing/error-handling conventions).

### AI-tool rule files

| Pattern | Origin tool |
|---------|-------------|
| `CLAUDE.md`, `CLAUDE.local.md`, `**/CLAUDE.md` | Claude Code |
| `AGENTS.md`, `**/AGENTS.md` | Cline / Roo / Codex CLI |
| `.cursorrules`, `.cursor/rules/**/*.mdc` | Cursor |
| `.windsurfrules` | Windsurf |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `GEMINI.md` | Antigravity CLI (`agy`) |

### JavaScript / TypeScript

| Pattern | Purpose |
|---------|---------|
| `.eslintrc*`, `eslint.config.{js,mjs,cjs,ts}` | Lint rules → coding conventions |
| `tsconfig*.json` | Path aliases, strictness, target |
| `.prettierrc*`, `prettier.config.{js,cjs,mjs}` | Formatting policy |
| `jest.config.*`, `vitest.config.*`, `playwright.config.*` | Test framework + location convention |
| `next.config.{js,mjs,ts}`, `vite.config.*`, `webpack.config.*` | Framework-specific build rules |
| `package.json` (`scripts`, `engines`, `workspaces` fields) | Toolchain, command surface, monorepo layout |

### Python

| Pattern | Purpose |
|---------|---------|
| `pyproject.toml` | Build, deps, linter, formatter (Ruff/Black) config |
| `setup.cfg`, `setup.py` | Legacy build/lint config |
| `pytest.ini`, `tox.ini`, `conftest.py` | Test discovery + fixtures |
| `mypy.ini`, `.mypy.ini` | Type-check strictness |
| `requirements*.txt`, `Pipfile`, `poetry.lock`, `uv.lock` | Dependency lock |

### Go

| Pattern | Purpose |
|---------|---------|
| `go.mod`, `go.sum`, `go.work` | Module/workspace structure |
| `.golangci.yml`, `.golangci.yaml` | Lint policy |
| `Makefile` (target naming) | Build/test entry conventions |

### Rust

| Pattern | Purpose |
|---------|---------|
| `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml` | Crate, deps, toolchain pin |
| `clippy.toml`, `rustfmt.toml` | Lint + formatting policy |

### General (cross-language)

| Pattern | Purpose |
|---------|---------|
| `.editorconfig` | Indentation, line endings |
| `.gitignore`, `.gitattributes` | What is/isn't source |
| `.env*` (read names only — never values) | Required runtime config keys |
| `.pre-commit-config.yaml`, `lefthook.yml`, `.husky/**` | Git hooks → quality gates |
| `Dockerfile`, `compose.{yml,yaml}`, `.devcontainer/**` | Runtime environment |
| `.github/workflows/**/*.{yml,yaml}`, `.gitlab-ci.yml`, `.circleci/config.yml` | CI policy → automation surface |
| `LICENSE`, `LICENSE.md` | License constraint on generated artifacts |
| `README.md`, `docs/**/*.md` | Implicit conventions and onboarding |

**SCAN policy**: read these files with **path + selective excerpt** strategy. Do not full-read everything — sample first 100 lines and grep for keys that match Sigil's detection patterns (e.g., `paths` in tsconfig, `[tool.ruff]` in pyproject, `lint:` in eslint config). Heavy reads are reserved for files with confirmed convention payload.

## Tool Comparison

| Capability | `CLAUDE.md` | `.cursorrules` / `.cursor/rules/` | `.windsurfrules` | `AGENTS.md` | `.github/copilot-instructions.md` |
|------------|-------------|------------------------------------|------------------|-------------|-----------------------------------|
| Primary tool | Claude Code | Cursor | Windsurf | Cline / Roo | GitHub Copilot |
| Scoped by directory | Yes | partial / file-pattern based | No | Yes | No |
| `@import` support | Yes | No | No | No | No |
| Dynamic context | Yes (`!`command``) | No | No | No | No |
| Hook integration | Yes | No | No | No | No |
| Skill system | Yes | No | No | No | No |

## Shared Rule Shapes

These rule shapes translate well across tools:

| Pattern | Example |
|---------|---------|
| prohibition list | do not leave `console.log` in production code |
| preferred pattern | use `Result` types for domain errors |
| file placement rule | components live in `components/` |
| testing policy | add an integration test for each API endpoint |
| documentation rule | public functions require JSDoc |

Keep tool-specific instructions separate when they depend on:
- tool APIs
- MCP or hook configuration
- editor behavior

## Interoperability Strategies

### Strategy A: Shared Core + Tool-Specific Wrappers

Best when the project intentionally supports multiple AI tools.

```text
project/
├── .ai-rules/
├── CLAUDE.md
├── .cursorrules
├── .windsurfrules
└── .github/copilot-instructions.md
```

### Strategy B: `rulesync`-Style Build Step

Use when one source of truth should feed multiple rule formats.

```bash
npm run sync-rules
```

### Strategy C: `CLAUDE.md` as Master

Use when Claude Code is primary and the team can derive flatter rule files for other tools.

## Path-Based Scoping

| Tool | Scope model |
|------|-------------|
| `CLAUDE.md` | directory-local files |
| `.cursor/rules/` | file-pattern matching |
| `AGENTS.md` | directory-local files |
| `.windsurfrules` | global only |
| Copilot instructions | global only |

For monorepos, prefer directory-scoped rule systems for per-package conventions.

## Sigil Implications

During `SCAN`:

1. Detect every active rule file.
2. Extract shared rules first.
3. Preserve Claude Code-specific strengths only where they will not conflict with broader project rules.
4. Check that generated skills do not contradict other tool-specific guidance.

Sigil may suggest `CLAUDE.md` generation or repair when:
- the project has strong rules elsewhere but no Claude-facing version
- the current `CLAUDE.md` is clearly behind other rule files
- the repository needs a scoped monorepo rule layout
