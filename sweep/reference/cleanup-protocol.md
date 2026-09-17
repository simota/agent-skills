# Cleanup Readiness and Delivery

Load for every cleanup proposal. Scoring, confirmation, batch limits and test gates are owned by `SKILL.md` § Confidence Gates / Core Contract; this file does not redefine them. Sweep proposes; Builder executes an approved plan.

## Scan Boundary

| Exclude from scanning | Patterns |
|---|---|
| Dependencies | `node_modules/`, `vendor/`, `.venv/`, `venv/`, `__pycache__/` |
| VCS | `.git/`, `.svn/`, `.hg/` |
| Build outputs | `dist/`, `build/`, `out/`, `.next/`, `.nuxt/` |
| Editor | `.idea/`, `.vscode/`, `*.swp`, `*.swo` |
| Caches | `.cache/`, `.parcel-cache/`, `.turbo/` |

| Never delete | Patterns |
|---|---|
| Project/legal | `LICENSE*`, `LICENCE*`, `CHANGELOG*`, `SECURITY*`, `CONTRIBUTING*` |
| Lockfiles | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Gemfile.lock`, `poetry.lock`, `go.sum` |
| Environment | `.env*`, `*.local` |
| Git | `.gitignore`, `.gitattributes`, `.gitmodules` |
| CI | `.github/`, `.gitlab-ci.yml`, `.circleci/`, `Jenkinsfile` |

Honor project-specific `.sweepignore` and ownership boundaries. Record each exclusion's scope and reason; do not blanket-ignore diagnostics to make a scan pass. Inspect tracked-artifact metadata without recursively scanning an excluded output tree. Intentional mirrors, generated inputs and symlinks are not disposable duplicates.

## Candidate Evidence

| Category | Required additional check |
|---|---|
| Dead Code | Active imports/callers, dynamic or reflective entry points, initialization and side effects |
| Orphan Asset | CSS/HTML/templates, config, filename stems and extensionless/string-built paths; docs-linked and runtime-loaded assets |
| Unused Dependency | Load `reference/dependency-cleanup.md` for implicit consumers and manifest/lockfile validation |
| Build Artifact | Proven reproducible output, tracked status and project retention policy; no deletion inside protected/excluded paths by inference |
| Duplicate | Content hash, canonical owner, every path consumer and intentional source/mirror relationship |
| Config Remnant | Actual scripts/build/CI/alias consumers and replacement configuration; protected environment files stay protected |

Before proposing deletion, check imports **and** dynamic import/require/glob/registry strings; config aliases/build registration; tests, fixtures and stories; git history; package `main`/`exports`/`bin`; external/public consumers; and documentation references. Zero textual imports is not a reachability proof. Framework-discovered routes (`pages/`, `app/`, file routes), plugins and convention files require the target project's actual discovery configuration, not a cached framework list.

Use `reference/language-patterns.md` only for the candidate's language. More than 50% unused exports or more than 10 transitive dependencies warrants module-impact review, not deletion proof; any cycle warrants architecture review. Side effects, shared state and reflection trigger the SKILL's Lava Flow individual-review rule.

## Proposal and Recovery

1. Bind ≥2 independent evidence signals, scope, tool/version, baseline checks and confidence to each candidate. Conflicting or missing coverage means review/keep, not “safe.”
2. Prepare the backup branch and restoration plan before implementation. Preserve unrelated uncommitted work; a branch alone does not capture it. For dependencies, capture manifest and lockfile together.
3. Send approved candidates, batch boundaries and verification commands to Builder. Use the SKILL's ≤10-file batch limit, ≥90 batch gate and confirmation exceptions; never infer write permission from a score.
4. Re-run the same build/tests after each batch. Stop on unexpected references, core/infrastructure ambiguity, repeated delete/restore churn, uncertain authorization or unexplained check failures. Restore only the affected batch, investigate and re-score; do not suppress failures or discard unrelated work.
5. Report actual verification separately from proposed savings. Load `reference/maintenance-workflow.md` only for baseline/trend updates or Grove handoffs.

## Report Contract

Summary: scan date, repository, files scanned, candidate count, estimated space savings; category totals with Count / Size / Risk.

Each finding: stable category ID, Path, Category, Size, Risk Level (`Critical|High|Medium|Low`), Last Modified, Last Author, ≥2 evidence signals, Recommendation (`Delete|Review|Keep`), Reason, Confidence Score. Group as Safe to Delete (batch confirmation), Verify Before Delete (individual confirmation), Potentially Needed (manual review), or Do Not Delete. Record post-implementation build/test outcomes and rollback status. Unknown size/last use stays unknown, not zero.
