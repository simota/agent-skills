# Compass Repo Cache Format

Reference for the per-repository cache file `.claude/compass-cache.md`. Compass reads this slim cache instead of `reference/catalog.md` (~600 lines) and `reference/recipes-directory.md` (~400 lines) during `recommend`, reducing context cost by ~95% per invocation.

The cache is **per-machine, per-repository**, not committed. It is not source-of-truth — `reference/catalog.md` is. The cache is a derived view filtered by repo signals.

---

## 1. Location

`.claude/compass-cache.md` relative to the **repository root** (the directory where `/compass` is invoked, ascending until a git root or `.claude/` is found).

- `.claude/` already exists in most Claude Code projects; cache file lives alongside `settings.json`.
- gitignore recommended: add `.claude/compass-cache.md` to `.gitignore` or `.claude/.gitignore`.
- Created by `/compass init` or by the auto-prompt on first `/compass recommend`.

---

## 2. File Structure

```markdown
---
catalog_version: <8-char hex>
generated_at: <ISO 8601 with timezone>
ttl_days: 30
repo_size: small | medium | large | xlarge
top_n: <integer>
project_signals:
  primary_language: <string>
  secondary_languages: [<string>, ...]
  frameworks: [<string>, ...]
  domains: [<string>, ...]
  detected_from: [<path or glob>, ...]
universal_skills: [scout, judge, zen, builder, scribe, sherpa, void, magi, riff, architect, nexus]
---

# Compass Repo Cache

| skill | affinity | default_recipe | key_subcommands | why |
|-------|----------|----------------|------------------|-----|
| artisan | H | code | hooks, server-components, forms | Next.js + React detected in package.json |
| flow    | H | animate | hover, modal, gesture | UI motion in src/components/**/*.tsx |
| schema  | M | design | audit-log, event-sourcing, soft-delete | prisma/schema.prisma present |
| ...
```

---

## 3. Field Semantics

| Field | Meaning |
|-------|---------|
| `catalog_version` | First 8 chars of `sha256(reference/catalog.md)`. Detects upstream catalog changes. |
| `generated_at` | ISO 8601 with timezone (e.g. `2026-04-25T15:00:00+09:00`). |
| `ttl_days` | Days before stale warning. Default `30`. |
| `repo_size` | One of `small` / `medium` / `large` / `xlarge`. Determines `top_n`. |
| `top_n` | Number of cached non-universal skills. Bound 15-50. |
| `project_signals.primary_language` | Detected primary language by file count or central manifest. |
| `project_signals.secondary_languages` | Other languages with > 10% file presence. |
| `project_signals.frameworks` | Direct dependency-list matches (Next.js, Vue, Tailwind, Prisma, etc.). |
| `project_signals.domains` | Inferred domains (Frontend, Auth, DB, IaC, AI, Game, Mobile, etc.). |
| `project_signals.detected_from` | Files / globs that produced the signals. Transparency. |
| `universal_skills` | Always-included skills. Listed for clarity but not duplicated in the table. |
| Table columns | `skill` (lowercase name), `affinity` (H/M/L), `default_recipe` (Recipe Subcommand from SKILL.md), `key_subcommands` (2-4 representative), `why` (one-line rationale citing a signal). |

Universal skills are recorded in the `universal_skills` array, not in the table, to keep the slim view focused on signal-derived picks. At recommendation time, Compass treats both as candidates.

---

## 4. Affinity Scale

| Affinity | Meaning | When to assign |
|----------|---------|----------------|
| `H` | Strong, load-bearing fit | Direct framework / library match in deps; declared by `CLAUDE.md`; primary language match for that skill's domain |
| `M` | Likely fit | Adjacent domain (Tailwind → palette); convention match (`tests/`, `__stories__/`); secondary stack match |
| `L` | Possible fit | Speculative; included only when slots remain |

Bias toward H and M. Reserve L for filler when `top_n` is large and signal coverage is sparse.

---

## 5. Universal Inclusions

These 11 skills are always considered candidates regardless of repo signals:

`scout`, `judge`, `zen`, `builder`, `scribe`, `sherpa`, `void`, `magi`, `riff`, `architect`, `nexus`

They cover universal tasks (debugging, review, refactor, build, doc, planning, removal, decision, brainstorm, ideation, meta-design, orchestration). They are listed in the `universal_skills` frontmatter array, not in the per-skill table, to keep the table focused.

---

## 6. Invalidation Rules

| Trigger | Action |
|---------|--------|
| `catalog_version` ≠ current `catalog.md` hash | Soft warn at top of `recommend` output, propose `/compass refresh` |
| `generated_at + ttl_days` ≤ today | Soft warn, propose `/compass refresh` |
| Cache file missing | Auto-prompt to run `init` |
| `/compass refresh` issued | Force regenerate, regardless of state |
| `--force` style explicit user override | Skip warnings, proceed with stale cache |

The warnings are non-blocking. Compass continues with the stale cache and lets the user decide.

---

## 7. Stale-but-Valid Handling

| State | Behavior |
|-------|----------|
| Only TTL expired | Use cache, prepend single-line warning: `⚠ Cache is N days old. Run /compass refresh to update.` |
| Only catalog hash mismatch | Use cache, prepend warning: `⚠ catalog.md has changed. Run /compass refresh to re-sync.` |
| Both stale | Use cache, stronger warning combining both messages |
| Catalog drift detected mid-flow (newly missing skill referenced in cache) | Drop that skill from candidates silently, proceed |

Compass never auto-refreshes during `recommend`. Refresh is always user-initiated.

---

## 8. Example

```markdown
---
catalog_version: a3f2b1c8
generated_at: 2026-04-25T15:00:00+09:00
ttl_days: 30
repo_size: medium
top_n: 25
project_signals:
  primary_language: TypeScript
  secondary_languages: [JavaScript, CSS]
  frameworks: [Next.js, Tailwind, Prisma, next-auth]
  domains: [Frontend, Auth, DB, SaaS]
  detected_from: [package.json, prisma/schema.prisma, src/app/**/*.tsx, .github/workflows/ci.yml]
universal_skills: [scout, judge, zen, builder, scribe, sherpa, void, magi, riff, architect, nexus]
---

# Compass Repo Cache

| skill | affinity | default_recipe | key_subcommands | why |
|-------|----------|----------------|------------------|-----|
| artisan   | H | code     | hooks, server-components, forms | Next.js 15 + React 19 in package.json |
| flow      | H | animate  | hover, modal, gesture | UI motion suspected from src/components/**/*.tsx |
| schema    | H | design   | audit-log, event-sourcing, soft-delete | prisma/schema.prisma present |
| tuner     | H | optimize | explain, index, slow | Prisma + relational schema |
| sentinel  | H | scan     | secrets, sqli, headers | next-auth + auth/ folder |
| crypt     | H | design   | tls, kms, e2ee | next-auth session token storage |
| gateway   | M | review   | auth, rate-limit, deprecation | Next.js API routes / route handlers |
| pipe      | M | design   | reusable, security, performance | .github/workflows/ci.yml present |
| muse      | M | tokens   | spacing, color, typography | Tailwind config with custom theme |
| palette   | M | improve  | error, empty, loading | Frontend SaaS context |
| vitrine   | M | story    | a11y, chromatic, coverage | Storybook config detected |
| radar     | M | edge     | flaky, coverage, regression | __tests__/ folder + jest config |
| voyager   | M | e2e      | auth, parallel, vrt | playwright.config.ts present |
| polyglot  | M | extract  | rtl, plurals, dates | next-intl in deps |
| pulse     | M | design   | northstar, retention, activation | SaaS domain |
| growth    | M | seo      | keyword, audit, vitals | Marketing pages in app/ |
| pixel     | L | reproduce | responsive, dark, animation | Possible mockup-to-code work |
| accord    | L | requirements | story-map, stakeholder, raci | Multi-stakeholder SaaS |
| beacon    | L | observability | slo, dashboard, alert | No explicit telemetry detected; speculative |
| ...
```

---

## 9. Anti-Patterns

- **Cache in repo root** (`./compass-cache.md`): pollutes user's workspace. Always `.claude/compass-cache.md`.
- **Top-N > 50**: defeats the slim cache purpose. Use full catalog instead.
- **Caching all 130 skills**: same as above — just read `catalog.md`.
- **Skipping universal inclusions**: breaks recommendations for common tasks (debug, review, plan).
- **Hand-editing the cache**: re-run `/compass refresh` instead. Hand edits drift from the catalog and the scanner.
- **Refreshing on every `recommend`**: defeats the cost saving. Only refresh on user request or invalidation trigger.
- **Caching from inside `node_modules` or vendored deps**: scanner must exclude them.
- **Treating cache as authoritative**: cache is a derived view; `reference/catalog.md` is source of truth.
