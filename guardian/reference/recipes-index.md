# Guardian Recipe Registry

The full Recipe table for `guardian`. `guardian/SKILL.md` carries only the dispatch
allowlist; this file holds what is needed to *execute* a Recipe — activation
condition and the files to read first.

**Read this when** a subcommand matched and you need its row, or when scanning
what Recipes exist at all.

---

| Recipe | Subcommand | Default? | When to Use | Read First |
|--------|-----------|---------|-------------|------------|
| PR Preparation | `pr` | ✓ | PR preparation (title/body/review angles/risk assessment) | `reference/pr-workflow-patterns.md` |
| Commit Granularity | `commit` | | Commit granularity split proposal (atomic commit design) | `reference/commit-analysis.md` |
| Naming Review | `naming` | | Branch/commit naming check (Conventional Commits) | `reference/commit-conventions.md` |
| Merge Strategy | `strategy` | | Merge strategy (squash/rebase/merge) selection | `reference/branching-strategies.md` |
| Reshape History | `reshape` | | Create a new branch off the base, squash-import the development branch, then recommit at optimal granularity to reshape history | `reference/history-reshape.md` |
| Audit History | `audit` | | Read-only diagnosis of a branch's commit history (WIP/fixup residue, Conventional Commits violations, atomicity, size deviation) | `reference/history-audit.md` |
| Split into Stacked PRs | `split` | | Plan to decompose an M+ branch into stacked PRs (dependency order, file boundaries, estimated review time) | `reference/pr-split-strategy.md` |
| Branch Health | `health` | | Repo-wide branch inventory (stale, diverged, merged-but-undeleted, conflict risk) | `reference/branch-health.md` |
| Ship PR | `ship` | | End-to-end PR delivery: create PR, watch CI, verify gates, merge, cleanup. Consumes `pr` and `strategy` Recipe outputs. Merge step is always Ask First. | `reference/pr-ship-flow.md` |
