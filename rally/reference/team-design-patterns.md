# Team Design Patterns

> Purpose: Read this when selecting a Rally team pattern, deciding headcount, or choosing `subagent_type` and model.

## Table of Contents

1. Pattern Catalog
2. Team Size Rules
3. `subagent_type` Guide
4. Model Guide

## Pattern Catalog

| Pattern | Team size | Use when | Default roles | Dependency rule |
|---------|-----------|----------|---------------|-----------------|
| Pattern A: Frontend/Backend Split | `2-3` | UI and API or data layers separate cleanly | `frontend-impl`, `backend-impl`, optional `test-writer` | Types or interfaces first, then frontend and backend in parallel, then tests |
| Pattern B: Feature Parallel | `2-4` | Multiple features or bug fixes are independent | `feature-a`, `feature-b`, `feature-c` | No `blockedBy` unless a shared writable component appears |
| Pattern C: Pipeline | `2-3` | Research, implementation, and verification must happen in stages | `field`, `implementer`, `tester` | `Phase 2` blocked by `Phase 1`; `Phase 3` blocked by `Phase 2` |
| Pattern D: Specialist Team | `2-4` | Different domains need different expertise | `db-specialist`, `api-specialist`, `security-specialist` | Use explicit ownership boundaries per specialty |
| Pattern E: Code/Test/Docs Triple | `3` | Code, tests, and docs should progress together | `coder`, `tester`, `documenter` | Docs can start early; tests start after interfaces or implementation are stable |

## Ownership Hints by Pattern

| Pattern | Typical `exclusive_write` split | Common `shared_read` |
|---------|-------------------------------|----------------------|
| Frontend/Backend Split | `src/components/**` vs `src/api/**` | `src/types/**`, `src/config/**`, `package.json` |
| Feature Parallel | one feature directory per teammate | `src/shared/**`, `src/types/**`, `src/config/**` |
| Pipeline | `shared_read` for research, `src/**` for implementation, `tests/**` for testing | source files needed by every phase |
| Specialist Team | domain-specific directories such as `migrations/**`, `src/api/**`, `src/security/**` | shared contracts and config |
| Code/Test/Docs Triple | `src/**`, `tests/**`, `docs/**` | public interfaces and shared config |

## Team Size Rules

| Factor | `2` teammates | `3` teammates | `4-5` teammates |
|--------|---------------|---------------|-----------------|
| Files changed | `2-3` | `4-8` | `9+` |
| Independent work areas | `2` clean areas | `3` clean areas | `4+` clean areas |
| Complexity | Low to medium | Medium | Medium to high |
| Time pressure | Low | Present | Tight |

- When in doubt, choose the smaller team.
- Coordination cost scales roughly with `O(N^2)`.
- `5+` teammates require user confirmation.
- `10+` teammates are prohibited.

## `subagent_type` Guide

| `subagent_type` | Tools | Use for | Hard rule |
|-----------------|-------|---------|-----------|
| `general-purpose` | full toolset | implementation, tests, bug fixes, refactoring | default for writable work |
| `Explore` | read-only | investigation, impact analysis, research | never assign implementation |
| `Plan` | read-only | design, architecture review, planning | never assign implementation |
| `Bash` | shell only | builds, tests, script execution | keep scope command-only |

## Model Guide

| Model | Cost | Use for |
|-------|------|---------|
| `haiku` | Low | simple boilerplate, doc updates, lightweight investigation |
| `sonnet` | Medium | default implementation, bug fixes, tests |
| `opus` | High | complex design, security-sensitive work, large refactors |

### Selection Rules

1. Default to `sonnet` when unspecified.
2. Use `haiku` aggressively for low-complexity work.
3. Use `opus` only when the task truly needs it.
4. Investigation work often succeeds with `haiku` or `Explore`.

## `isolation` Guide

Use `isolation: "worktree"` on the `Agent` tool to run a teammate in an independent git worktree.

| Scenario | Use worktree? |
|----------|---------------|
| Teammates edit completely separate files | No (default) |
| Potential overlap in writable files | Yes |
| Need clean merge workflow with PR-style review | Yes |
| Lightweight investigation or read-only work | No |

When worktree isolation is active, the teammate works on a separate branch. If changes are made, Rally receives the worktree path and branch name for merge.

## `auto` Mode

The `auto` mode provides automatic permission handling. Use it when you want teammates to proceed without manual approval but still respect system-level safety checks. It is the most hands-off mode after `bypassPermissions`.

## Evaluator + Memory Hooks (Managed Agents alignment)

These extensions keep Rally compatible with Claude Managed Agents (`managed-agents-2026-04-01` beta) vocabulary so escalations stay portable.

### Outcomes (rubric grader)

When teammate output must pass a quality bar before downstream work, spawn a dedicated `evaluator` teammate (typically `Plan` or `Explore` subagent_type, model `opus` or `sonnet`) and pass it the same rubric the Managed Agents `Outcomes` feature would consume. The evaluator scores in its own context window — keep it free of the implementer's chain so its judgement is not anchored on the writer's reasoning.

| Field | Rally implementation |
|-------|----------------------|
| Rubric | Markdown table inside the evaluator's prompt; one row per criterion with weight and pass threshold |
| Grader isolation | Separate teammate, separate context, read-only access to implementer output |
| Verdict format | `{ score, per_criterion, blockers, recommendation }` returned via `_STEP_COMPLETE` |

### Memory + Dreaming

Per-teammate notes belong in `.agents/{teammate-name}.md` (journal). Cross-team learnings belong in Lore's `MEMORY.md` curation — Rally hands them off via `NEXUS_TO_LORE_HANDOFF`. Do not let teammates write directly into Lore-managed files; Lore validates and propagates patterns.

When the same team pattern reappears across sessions (e.g., Pattern C Pipeline used for the third time on the same repo), prefer surfacing the pattern + ownership split to Lore so it is reused without re-derivation next session. This is the local-hub equivalent of Managed Agents' `Dreaming` between-session memory refinement.
