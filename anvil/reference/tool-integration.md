# Development Tool Integration

**Purpose:** Canonical setup patterns for linters, formatters, test runners, build tools, doctor commands, and modern CLI toolchains.
**Read when:** Selecting or wiring project tooling for a CLI, especially when you need reproducible lint/test/build workflows or a doctor command.

## Contents

- Linter/Formatter Matrix
- Biome
- oxlint
- Ruff
- golangci-lint
- Test Runner Matrix
- Build Tool Matrix
- Modern Toolchain Options

## Linter/Formatter Matrix

| Language | Linter | Formatter | All-in-One |
|----------|--------|-----------|------------|
| **TypeScript** | ESLint v9+ (flat config default) | Prettier | Biome v2, oxlint |
| **Python** | Ruff, Flake8 | Black, Ruff | Ruff |
| **Go** | golangci-lint | gofmt | golangci-lint |
| **Rust** | clippy | rustfmt | - |

---

## Biome (TypeScript/JavaScript)

ESLint + Prettier replacement. Fast, single tool. Biome v2 (stable, 2025+) adds embedded CSS/GraphQL linting in JS template literals, 15 HTML accessibility rules, and `--profile-rules` for CI bottleneck analysis. [Source: biomejs.dev/blog/biome-v2-4](https://biomejs.dev/blog/biome-v2-4/)

```json
{
  "$schema": "https://biomejs.dev/schemas/2.4.0/schema.json",
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": { "noExcessiveCognitiveComplexity": "warn" },
      "suspicious": { "noExplicitAny": "warn" }
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": { "quoteStyle": "single", "trailingCommas": "es5" }
  }
}
```

```bash
pnpm add -D @biomejs/biome && pnpm biome init
pnpm biome check .           # Lint + Format check
pnpm biome check --write .   # Auto-fix
pnpm biome ci .              # CI mode (no writes)
```

## ESLint v9 (TypeScript/JavaScript)

Flat config (`eslint.config.js`) is the default and only format since ESLint v9.0.0 (April 2024). TypeScript config files (`.ts`) are stable since v9.18.0. ESLint v9 EOL is 2026-08-06; ESLint v10 is planned for 2026. [Source: eslint.org/blog/2025/05/eslint-v9.0.0-retrospective](https://eslint.org/blog/2025/05/eslint-v9.0.0-retrospective/)

```javascript
// eslint.config.js (flat config — default in v9)
import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  js.configs.recommended,
  ...tseslint.configs.recommended,
);
```

> **Migration note:** The legacy `.eslintrc.*` format is removed in ESLint v9. Use `npx @eslint/migrate-config .eslintrc.json` to migrate.

---

## oxlint (TypeScript/JavaScript — Rust-based)

Ultra-fast linter, 50-100x faster than ESLint. Use alongside Biome formatter.

```bash
pnpm add -D oxlint
pnpm oxlint .                # Run linter
pnpm oxlint --fix .          # Auto-fix
```

```json
// .oxlintrc.json
{
  "rules": {
    "no-unused-vars": "warn",
    "no-explicit-any": "warn",
    "eqeqeq": "error"
  }
}
```

---

## Ruff (Python)

```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

```bash
uv add --dev ruff
ruff check .           # Lint
ruff check --fix .     # Auto-fix
ruff format .          # Format
```

## golangci-lint (Go)

```yaml
# .golangci.yml
run:
  timeout: 5m
linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused
    - gofmt
    - goimports
    - misspell
linters-settings:
  goimports:
    local-prefixes: github.com/yourorg/yourrepo
```

```bash
golangci-lint run
golangci-lint run --fix
```

---

## Test Runner Matrix

| Language | Unit Test | Integration | Coverage |
|----------|-----------|-------------|----------|
| **TypeScript** | Vitest, Jest | Playwright | v8, istanbul |
| **Python** | pytest | pytest | pytest-cov |
| **Go** | go test | go test | go test -cover |
| **Rust** | cargo test | cargo test | cargo-tarpaulin |

### Vitest Setup (TypeScript)

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    coverage: {
      provider: 'v8',
      thresholds: { branches: 80, functions: 80, lines: 80, statements: 80 },
    },
  },
});
```

### pytest Setup (Python)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-ra", "--strict-markers", "-v"]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80
show_missing = true
```

---

## Build Tool Matrix

| Use Case | Tool | Language |
|----------|------|----------|
| **Library bundling** | tsup, unbuild | TypeScript |
| **App bundling** | esbuild, Vite | TypeScript |
| **CLI bundling** | esbuild, pkg | TypeScript |
| **Single binary** | bun build --compile | Bun |
| **Cross-compile binary** | deno compile | Deno |
| **Native binary** | go build, cargo build | Go, Rust |

### tsup (TypeScript Library/CLI)

```typescript
// tsup.config.ts
import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['src/index.ts', 'src/cli.ts'],
  format: ['cjs', 'esm'],
  dts: true,
  clean: true,
  target: 'node18',
  banner: { js: '#!/usr/bin/env node' },
});
```

### Bun Build (Single Binary CLI)

```bash
# Compile to single binary (cross-platform)
bun build ./src/cli.ts --compile --outfile myapp

# Cross-compile targets
bun build ./src/cli.ts --compile --target=bun-linux-x64 --outfile myapp-linux
bun build ./src/cli.ts --compile --target=bun-darwin-arm64 --outfile myapp-macos
bun build ./src/cli.ts --compile --target=bun-windows-x64 --outfile myapp.exe
```

### Deno Compile (Cross-Platform Binary)

```bash
# Compile to single binary
deno compile --allow-read --allow-write --output myapp src/cli.ts

# Cross-compile
deno compile --target x86_64-unknown-linux-gnu --output myapp-linux src/cli.ts
deno compile --target aarch64-apple-darwin --output myapp-macos src/cli.ts
```

---

## Modern Toolchain Options

### mise (Multi-Language Version Manager + Task Runner)

Replaces asdf, nvm, pyenv, etc. Also serves as a task runner.

```toml
# .mise.toml
[tools]
node = "20"
python = "3.12"
go = "1.22"
rust = "1.78"

[tasks.lint]
run = "biome check ."
description = "Run linter"

[tasks.test]
run = "vitest run"
description = "Run tests"

[tasks.build]
depends = ["lint", "test"]
run = "tsup"
description = "Build project"
```

```bash
mise install          # Install all tool versions
mise run lint         # Run lint task
mise run build        # Run build (with dependencies)
```

### Environment Verification (Doctor Command)

```typescript
interface CheckResult {
  name: string;
  status: 'ok' | 'warning' | 'error';
  message: string;
  fix?: string;
}

async function runDoctorChecks(): Promise<CheckResult[]> {
  const checks: CheckResult[] = [];

  // Node.js version
  const majorVersion = parseInt(process.version.slice(1).split('.')[0]);
  checks.push({
    name: 'Node.js',
    status: majorVersion >= 22 ? 'ok' : majorVersion >= 20 ? 'warn' : 'error',
    message: `Node.js ${process.version}`,
    fix:
      majorVersion < 20
        ? 'Upgrade to Node.js 22 LTS (Node 18 reached EOL 2025-04, Node 20 LTS active through 2026-04)'
        : majorVersion < 22
          ? 'Node 20 LTS is still supported but Node 22 LTS is recommended for new projects'
          : undefined,
  });

  // Package manager
  const hasPnpmLock = fs.existsSync('pnpm-lock.yaml');
  checks.push({
    name: 'Package Manager',
    status: hasPnpmLock ? 'ok' : 'warning',
    message: hasPnpmLock ? 'pnpm detected' : 'pnpm-lock.yaml not found',
  });

  // Dependencies
  try {
    execSync('pnpm install --frozen-lockfile --dry-run', { stdio: 'pipe' });
    checks.push({ name: 'Dependencies', status: 'ok', message: 'All resolved' });
  } catch {
    checks.push({ name: 'Dependencies', status: 'error', message: 'Lockfile out of sync', fix: 'Run pnpm install' });
  }

  return checks;
}
```
