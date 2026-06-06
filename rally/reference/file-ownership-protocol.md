# File Ownership Protocol

> Purpose: Read this before spawning teammates, when validating writable boundaries, or when resolving output conflicts.

## Table of Contents

1. Core Principles
2. Declaration Format
3. Assignment Rules
4. Validation Checks
5. Runtime Enforcement
6. Conflict Resolution
7. Templates

## Core Principles

1. `exclusive_write`: only one teammate may write a given file.
2. `shared_read`: any teammate may read a file.
3. Declare ownership before spawning.
4. Every file that may be modified must have an owner.

## Declaration Format

```yaml
ownership_map:
  [teammate_name]:
    exclusive_write:
      - [glob pattern 1]
      - [glob pattern 2]
    shared_read:
      - [glob pattern 1]
      - [glob pattern 2]
```

## Assignment Rules

| Rule | Guidance |
|------|----------|
| Prefer directory-based ownership | It is simpler and less error-prone than file-by-file splits |
| Use file-based ownership only when needed | Split files inside the same directory only when there is no safer partition |
| Treat shared contracts as `shared_read` | Types, config, constants, and public APIs are usually shared |
| Convert shared reads to a single writer when edits are needed | One teammate gets `exclusive_write`, everyone else keeps `shared_read` |
| No ownership gaps | Every writable file or glob must appear in exactly one teammate's `exclusive_write` |

### Common `shared_read` Categories

| Category | Example |
|----------|---------|
| Type definitions | `src/types/**`, `*.d.ts` |
| Config files | `tsconfig.json`, `.eslintrc`, `package.json` |
| Environment reference | `.env.example` |
| Shared utilities | `src/utils/**`, `src/lib/**` |
| Constants | `src/constants/**` |

## Validation Checks

Run these checks before spawning:

| Check | Failure example |
|-------|-----------------|
| No `exclusive_write` overlap | teammate A owns `src/components/**` and teammate B owns `src/components/Button.tsx` |
| Every target file has an owner | `src/middleware/auth.ts` appears nowhere |
| `shared_read` and `exclusive_write` stay consistent | one explicit writer is allowed, many writers are not |

## Runtime Enforcement

1. Collect `files_changed` from each teammate.
2. Compare them against `ownership_map`.
3. If a teammate changed an unowned or foreign file, warn and roll back or reassign as needed.
4. Treat same-file edits as a conflict candidate even when line ranges differ.

## Conflict Resolution

| Conflict class | Detection | Default response |
|----------------|-----------|------------------|
| Minor | same file, no same-line clash | attempt merge, then re-check ownership |
| Major | same line or incompatible intent | trigger `ON_RESULT_CONFLICT` |

### Resolution Options

1. Re-partition ownership under one teammate.
2. Sequentialize via `blockedBy`.
3. Define a shared interface first, then separate implementations.
4. Escalate for manual merge.

## Templates

### Web Application

```yaml
ownership_map:
  frontend:
    exclusive_write:
      - src/components/**
      - src/pages/**
      - src/styles/**
      - src/hooks/**
      - public/**
    shared_read:
      - src/types/**
      - src/config/**
  backend:
    exclusive_write:
      - src/api/**
      - src/services/**
      - src/models/**
      - src/middleware/**
      - prisma/**
    shared_read:
      - src/types/**
      - src/config/**
```

### Microservices

```yaml
ownership_map:
  auth-service:
    exclusive_write:
      - services/auth/**
    shared_read:
      - shared/types/**
      - shared/config/**
  user-service:
    exclusive_write:
      - services/user/**
    shared_read:
      - shared/types/**
      - shared/config/**
```

### Monorepo

```yaml
ownership_map:
  pkg-core:
    exclusive_write:
      - packages/core/**
    shared_read:
      - packages/types/**
  pkg-ui:
    exclusive_write:
      - packages/ui/**
    shared_read:
      - packages/types/**
      - packages/core/src/index.ts
```
