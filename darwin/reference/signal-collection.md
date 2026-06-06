# Signal Collection

Defines the signals Darwin collects to determine project lifecycle phase and ecosystem state.

> **2026-05 framework / model signal additions**
>
> When scanning `pyproject.toml`, `package.json`, `requirements*.txt`, and source imports, treat the following as **end-of-life drift signals** (feed into ET-10; ET-09 is reserved for Official Spec Conformance drift — see `official-fitness-criteria.md`):
>
> | Detected dependency | Status as of 2026-05 | Successor |
> |---|---|---|
> | `semantic-kernel` (any version) | Maintenance mode since Microsoft Agent Framework 1.0 GA (2026-04-03) — bug/security only | `agent-framework` (.NET / Python) |
> | `pyautogen` / `autogen-agentchat` < 0.12 | Superseded by AG2 0.12.0 (2026-04-17), v1.0 line in progress | `ag2` ≥ 0.12, or Microsoft Agent Framework |
> | OpenAI Assistants API calls | API retirement 2026-08-26 (announced) | OpenAI Responses API / Agents SDK |
> | `gpt-4o` model literals | API retired 2026-03-31 | gpt-4.1 / gpt-5-class |
> | `langgraph` < 1.0 | Pre-GA; LangGraph 1.0 shipped 2025-10-22 with no breaking changes | `langgraph` ≥ 1.0 |
>
> Sources: `https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/`, `https://github.com/ag2ai/ag2/releases`, `https://changelog.langchain.com/announcements/langgraph-1-0-is-now-generally-available`, `https://www.echostash.app/blog/gpt-4o-retirement-prompt-migration-production`.

---

## Signal Categories

### 1. Git Metrics

Collected from `git log`, `git shortlog`, and repository structure.

| Signal | Command/Method | Interpretation |
|--------|---------------|----------------|
| Commit frequency | `git log --since="30 days" --oneline \| wc -l` | Activity level |
| Commit type ratio | Parse conventional commit prefixes (feat/fix/refactor/docs) | Development focus |
| File churn | `git log --stat` — files changed per commit | Codebase stability |
| Contributor count | `git shortlog -sn --since="90 days"` | Team size indicator |
| Branch patterns | Active branches, naming conventions | Workflow maturity |
| Merge frequency | Merge commits per week | Collaboration level |
| Tag/release history | `git tag --sort=-creatordate` | Release maturity |
| First commit date | `git log --reverse --format=%ci \| head -1` | Project age |
| Days since last commit | `git log -1 --format=%cr` | Activity recency |

### 2. File Structure Signals

Collected from directory listing and file analysis.

| Signal | Detection Method | Interpretation |
|--------|-----------------|----------------|
| Total file count | `find . -type f \| wc -l` (excluding .git) | Project size |
| Test presence | `**/test*`, `**/*.test.*`, `**/*.spec.*` | Quality maturity |
| Test-to-source ratio | Test files / source files | Testing coverage indicator |
| CI/CD configs | `.github/workflows/`, `Jenkinsfile`, `.circleci/` | Automation maturity |
| Deploy configs | `Dockerfile`, `docker-compose.*`, `k8s/`, `terraform/` | Production readiness |
| Documentation | `README.md` size, `docs/` directory, JSDoc coverage | Documentation maturity |
| Lock files | `package-lock.json`, `yarn.lock`, `Gemfile.lock` | Dependency management |
| Monitoring configs | Sentry, DataDog, Prometheus configs | Observability maturity |
| Performance configs | Load test configs, benchmark files | Performance focus |
| Deprecation markers | `@deprecated` tags, archive notices | Sunset indicators |

### 3. Activity Log Signals

Collected from `.agents/PROJECT.md` and `.agents/*.md` journals.

| Signal | Detection Method | Interpretation |
|--------|-----------------|----------------|
| Agent invocation frequency | Count rows per agent in PROJECT.md (last 30 days) | Usage patterns |
| Agent diversity | Unique agents invoked (last 30 days) | Ecosystem breadth |
| Dominant agents | Top 3 agents by invocation count | Current focus areas |
| Journal freshness | Most recent entry date per agent journal | Agent relevance |
| Pattern density | Entries with `reusable: true` or insight keywords | Knowledge capture rate |
| Error/recovery entries | Entries mentioning failure, retry, recovery | Stability indicator |
| Chain complexity | Average chain length from Nexus logs | Task complexity |

### 4. Existing Score Signals

Read from other agents' outputs (never recalculated by Darwin).

| Signal | Source | Location |
|--------|--------|----------|
| Health Score | Architect | `.agents/architect.md` or last review output |
| UQS History | Judge | `.agents/judge.md` or last cycle output |
| DNA Score | Grove | `.agents/grove.md` or last profile output |
| Strategy Drift | Helm | `.agents/helm.md` or last monitoring output |
| Reverse Feedback | Judge | `_common/REVERSE_FEEDBACK.md` or judge outputs |

---

## Lifecycle Phase Signals

### GENESIS

```yaml
signals:
  file_count: < 50
  test_framework: absent
  commit_count: < 20
  contributors: 1
  ci_cd: absent
  documentation: minimal (README only or empty)
  branches: main/master only
  age: < 30 days
weight: 0.15 per matching signal (max 8 signals)
```

### ACTIVE_BUILD

```yaml
signals:
  commit_velocity: > 5/day (or > 25/week)
  feat_ratio: > 50% of commits are feat/add
  file_creation_rate: > 3 new files/day
  branch_count: > 3 active feature branches
  contributors: growing (new contributors in last 30 days)
  test_additions: present but trailing features
  ci_cd: basic (may be incomplete)
  merge_frequency: > 3/week
weight: 0.125 per matching signal (max 8 signals)
```

### STABILIZATION

```yaml
signals:
  refactor_ratio: > 30% of commits are refactor/fix
  test_additions: outpacing feature additions
  code_review_activity: PR comments increasing
  lint_config: present and enforced
  documentation: growing (API docs, guides)
  ci_cd: comprehensive (tests, lint, build)
  feat_velocity: decreasing from peak
  dependency_updates: regular maintenance
weight: 0.125 per matching signal (max 8 signals)
```

### PRODUCTION

```yaml
signals:
  deploy_configs: present (Docker, k8s, terraform, etc.)
  monitoring: configured (Sentry, DataDog, etc.)
  hotfix_branches: pattern observed (hotfix/*, fix/*)
  release_tags: regular cadence (>= monthly)
  ci_cd: complete (deploy stages included)
  security_scanning: present
  environment_configs: staging/production separation
  incident_handling: runbooks or on-call config present
weight: 0.125 per matching signal (max 8 signals)
```

### MAINTENANCE

```yaml
signals:
  commit_velocity: < 2/week
  fix_ratio: > 60% of commits are fix/patch
  dependency_updates: primary activity
  feature_additions: rare (< 1/month)
  contributor_count: stable or declining
  age: > 365 days
  documentation: stable (minimal changes)
  ci_cd: stable (no pipeline changes)
weight: 0.125 per matching signal (max 8 signals)
```

### SCALING

```yaml
signals:
  performance_changes: present (caching, optimization, indexing)
  infrastructure_additions: load balancers, CDN, scaling configs
  load_test_configs: present
  database_optimization: query tuning, partitioning, sharding
  monitoring_expansion: new dashboards, alerts, SLOs
  horizontal_scaling: multi-instance configs
  cost_optimization: resource tuning commits
  capacity_planning: infrastructure docs
weight: 0.125 per matching signal (max 8 signals)
```

### SUNSET

```yaml
signals:
  last_commit_age: > 60 days
  deprecation_markers: @deprecated tags, README notices
  archive_flags: GitHub archived, "unmaintained" badges
  dependency_status: outdated, security vulnerabilities unpatched
  documentation: "end of life" or migration guides
  ci_cd: failing or disabled
  contributor_count: 0 active
  issues_closed_as_wontfix: increasing
weight: 0.125 per matching signal (max 8 signals)
```

---

## Signal Collection Process

```
1. GATHER: Run git commands, scan file structure, read activity logs
2. NORMALIZE: Convert raw values to 0.0-1.0 scores per signal
3. MATCH: Compare normalized scores against phase signal profiles
4. SCORE: Calculate weighted sum per phase
5. SELECT: Choose highest-scoring phase (or mixed if top < 0.60)
6. COMPARE: Check against previous detection for transition events
7. REPORT: Output phase, confidence, and signal breakdown
```

### Normalization Examples

| Signal | Raw Value | Normalized | Method |
|--------|-----------|------------|--------|
| Commit velocity | 12/day | 1.0 | min(raw/10, 1.0) |
| Commit velocity | 3/day | 0.3 | min(raw/10, 1.0) |
| File count | 200 | 0.8 | Custom ranges per phase |
| Test ratio | 0.4 | 0.8 | min(raw/0.5, 1.0) |
| Days since commit | 5 | 0.95 | max(1.0 - raw/60, 0.0) |

---

## Collection Frequency

| Trigger | Collection Scope |
|---------|-----------------|
| `/Darwin` (explicit invocation) | Full signal collection |
| ET-07 (commit velocity change) | Git metrics only |
| ET-08 (DNA score shift) | Existing scores only |
| Nexus Proactive Mode | Read cached ECOSYSTEM.md (no fresh collection) |

**Performance note:** Full signal collection may take 10-30 seconds on large repositories. Git metric collection is the primary bottleneck. Use cached ECOSYSTEM.md when fresh data is not critical.
