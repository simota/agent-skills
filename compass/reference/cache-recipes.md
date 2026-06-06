# Compass Cache Recipes

Reference for `init`, `refresh`, and the auto-prompt flow that maintains `.claude/compass-cache.md`. The cache file format is defined in `cache-format.md` — this file is the *procedure*.

---

## 1. `/compass init` Flow

`SCAN → SIZE → SCORE → PICK → WRITE → REPORT`

| Step | Action | Output |
|------|--------|--------|
| `SCAN` | Detect project signals (§ 4) by reading manifest files, file extensions, and convention markers | `project_signals` object |
| `SIZE` | Count files (excluding `node_modules`, `dist`, `.git`, vendor dirs) → classify into small / medium / large / xlarge → derive `top_n` (§ 7) | `repo_size`, `top_n` |
| `SCORE` | Match each catalog skill against signals (§ 5), assign affinity H/M/L (§ 6) | scored list of all skills |
| `PICK` | Sort by affinity desc → take `top_n` non-universal skills → record universal skills separately | final candidate set |
| `WRITE` | Generate cache file per `cache-format.md` § 2 to `.claude/compass-cache.md` | cache file |
| `REPORT` | Print 5-line summary (§ 9) | terminal output |

If `.claude/compass-cache.md` already exists, ask "Overwrite the existing cache?" before overwriting. Confirmed yes → route to refresh flow.

---

## 2. `/compass refresh` Flow

Same as `init` but:
- Skip existence check; force overwrite.
- Show a before/after diff in `REPORT`:
  - **Added**: skills new in cache
  - **Removed**: skills dropped
  - **Changed**: affinity changes (e.g., `flow: M → H`)
- Update `generated_at` and `catalog_version`.

Use cases:
- Catalog upgraded (new skills added upstream).
- Repo evolved (new framework adopted).
- TTL expired and the warning has appeared.
- Signal extraction logic improved.

---

## 3. Auto-Prompt on First `/compass recommend`

When `recommend` is invoked and `.claude/compass-cache.md` is missing:

```
No Compass cache found for this repository.
Generating one reduces context cost on later /compass recommend by ~95%.
Create the cache now? (Y/n)
  Y → run init flow → continue with the original recommend request
  n → recommend with the full catalog this time → cache stays absent
```

If `Y`: run `init` inline (SCAN → SIZE → SCORE → PICK → WRITE), then continue with the user's original recommend request using the freshly written cache.
If `n`: fall back to `reference/catalog.md` for this invocation. Do not nag again in the same session, but mention `/compass init` once at the end.

If the cache exists but `catalog_version` mismatches or TTL expired, do NOT auto-prompt. Show the warning per `cache-format.md` § 7 and proceed with the stale cache. The user decides when to refresh.

---

## 4. Signal Extraction Sources

Probe these in order. Stop early if a manifest fully describes the stack.

| File / pattern | Signal extracted | Probe |
|----------------|------------------|-------|
| `package.json` | dependencies, devDependencies, scripts, type | parse JSON; collect dep names |
| `Cargo.toml` | `[dependencies]`, edition, target | parse TOML |
| `pyproject.toml` | `[project] dependencies` / `[tool.poetry] dependencies` | parse TOML |
| `requirements.txt` | Python packages | line-parse |
| `go.mod` | Go modules | parse |
| `Gemfile` | Ruby gems | parse |
| `composer.json` | PHP packages | parse JSON |
| `pubspec.yaml` | Flutter / Dart packages | parse YAML |
| `.github/workflows/*.yml` | GHA presence → `pipe` | dir exists |
| `docker-compose.yml` / `Dockerfile` | container dev → `gear` | exists |
| `terraform/` / `*.tf` | IaC → `scaffold` | dir exists |
| `prisma/schema.prisma` | DB schema → `schema`, `tuner` | exists |
| `migrations/` / `db/migrate/` | migrations → `schema`, `shift` | exists |
| `__tests__/` / `tests/` / `spec/` / `test/` | tests → `radar`, `mint` | exists |
| `*.stories.*` / `.storybook/` | Storybook → `vitrine` | exists |
| `playwright.config.*` / `cypress.config.*` | E2E → `voyager` | exists |
| `.eslintrc*` / `eslint.config.*` | lint config → noted but no skill push | exists |
| `tsconfig.json` | TypeScript present | exists |
| `CLAUDE.md` | hand-written context (frameworks, domains, intent) | full read |
| File-extension distribution | language mix | `find . -type f \( ... \)` excluding ignored dirs |

Excluded dirs (always): `node_modules`, `dist`, `build`, `.next`, `.cache`, `.git`, `vendor`, `target`, `.venv`, `__pycache__`.

---

## 5. Signal → Skill Mapping

Apply the following rules. A skill may be triggered by multiple signals; combine and use the highest affinity.

### Frontend frameworks

| Trigger | Skills (H) | Skills (M) |
|---------|------------|------------|
| Next.js / Remix | artisan, flow | palette, vitrine, gateway |
| React (no meta-framework) | artisan | flow, palette |
| Vue / Nuxt | artisan | flow, palette |
| Svelte / SvelteKit | artisan | flow, palette |
| Solid / Astro | artisan | flow |
| Tailwind | muse, palette | vision |
| CSS-in-JS (styled-components, emotion) | flow | muse |

### Backend / Languages

| Trigger | Skills (H) | Skills (M) |
|---------|------------|------------|
| Rust | builder, anvil | crypt, siege |
| Go | builder, anvil | beacon, gateway |
| Node + TypeScript backend (Hono, Express, Fastify) | builder, gateway | bolt |
| Python + Django/Flask/FastAPI | builder, gateway, schema | bolt |
| Ruby on Rails | builder, gateway, schema | radar |
| PHP / Laravel | builder, gateway | schema |
| Elixir / Phoenix | builder | beacon |

### Data / DB

| Trigger | Skills (H) | Skills (M) |
|---------|------------|------------|
| Prisma / Drizzle / TypeORM / SQLAlchemy / ActiveRecord | schema, tuner | shift |
| Redis / BullMQ / Sidekiq | stream, tempo | beacon |
| Kafka / RabbitMQ | stream | tempo |
| DuckDB / ClickHouse | tuner | seek |
| Elasticsearch / Meilisearch / Typesense | seek | tuner |
| pgvector / Pinecone / Weaviate | seek, oracle | claude-api |

### AI / LLM

| Trigger | Skills (H) | Skills (M) |
|---------|------------|------------|
| `@anthropic-ai/sdk` / `anthropic` | claude-api, oracle | sentinel |
| `openai` (no anthropic) | oracle | claude-api |
| LangChain / LlamaIndex | oracle | claude-api, seek |
| torch / sklearn / transformers | oracle | mint |

### Auth / Security

| Trigger | Skills (H) | Skills (M) |
|---------|------------|------------|
| next-auth / Auth.js / passport / Devise | sentinel, crypt | probe |
| JWT-only auth | crypt, sentinel | probe |
| OAuth provider (Clerk, Auth0, WorkOS) | sentinel | probe, oath |
| OWASP / pen-test config | probe, sentinel | breach |

### Infra / DevOps

| Trigger | Skills (H) | Skills (M) |
|---------|------------|------------|
| `.github/workflows/` | pipe | latch |
| Dockerfile / docker-compose | gear, scaffold | beacon |
| terraform / pulumi / cdk | scaffold | ledger |
| k8s manifests / helm | scaffold | beacon |
| OpenTelemetry / Sentry / Datadog | beacon | triage |

### API / Schema

| Trigger | Skills (H) | Skills (M) |
|---------|------------|------------|
| OpenAPI / Swagger | gateway, attest | canon |
| GraphQL (Apollo, urql, codegen) | gateway | bolt |
| gRPC | gateway | grok |

### Testing

| Trigger | Skills (H) | Skills (M) |
|---------|------------|------------|
| Jest / Vitest / pytest / RSpec | radar | mint |
| Playwright / Cypress / WebdriverIO | voyager | radar |
| Storybook | vitrine | radar |
| k6 / Artillery / Gatling | siege | beacon |

### Domain-specific

| Trigger | Skills (H) | Skills (M) |
|---------|------------|------------|
| LP / Marketing pages | funnel, growth, prose | palette |
| i18n (next-intl, i18next, react-intl) | polyglot | prose |
| Mobile (iOS Swift / SwiftUI, Android Kotlin / Compose) | native | flow, port |
| Web → Native porting (React / Vue / Svelte / Angular SPA → iOS + Android) | port | native, scaffold |
| Founder office hours / startup advisory / "what should I focus on" | sage | sherpa, plea |
| Game (Phaser, Three.js, Unity, Godot) | dot | sketch |
| CMS / Headless CMS | builder | scribe |
| Payment (Stripe, Square) | crypt, ledger | clause |

### Project intent (from CLAUDE.md / repo name)

| Hint | Skills (H) |
|------|------------|
| "design system" | muse, palette, vitrine, vision |
| "ML / AI agent" | oracle, claude-api |
| "data pipeline" | stream, schema |
| "monorepo" | nest, grove |

---

## 6. Affinity Scoring Rules

```
1. If trigger is a direct dependency in the manifest → H
2. If trigger is a convention/file-pattern match → M
3. If trigger is inferred only from project intent text → M
4. If multiple signals point to same skill → keep highest affinity
5. If signal is weak (single tangential file) → L
6. Universal skills (§ 8) are not affinity-scored; recorded separately
```

When in doubt between H and M, prefer M. Reserve H for clearly load-bearing matches the user would expect to see.

---

## 7. Top-N Sizing by Repo Size

| Repo Size | File count (post-exclusion) | Default `top_n` |
|-----------|----------------------------|-----------------|
| `small` | < 50 | 15 |
| `medium` | 50 – 499 | 25 |
| `large` | 500 – 4,999 | 40 |
| `xlarge` | ≥ 5,000 | 50 (cap) |

Adjustments:
- Polyglot bias (3+ active languages with > 10% file share): `+5`
- Single-stack bias (1 language ≥ 90%): `-5`
- Hard floor: `15`. Hard ceiling: `50`.

File counting:
```
find . -type f \
  -not -path "./node_modules/*" \
  -not -path "./.next/*" \
  -not -path "./dist/*" \
  -not -path "./build/*" \
  -not -path "./.git/*" \
  -not -path "./vendor/*" \
  -not -path "./target/*" \
  -not -path "./.venv/*" \
  -not -path "./__pycache__/*" \
  | wc -l
```

---

## 8. Universal Inclusions

Always recorded in the `universal_skills` array regardless of signals:

`scout`, `judge`, `zen`, `builder`, `scribe`, `sherpa`, `void`, `magi`, `riff`, `architect`, `nexus`

These cover universal tasks (debug, review, refactor, build, doc, planning, removal, decision, brainstorm, ideation, meta-design, orchestration). They do not consume `top_n` slots.

If a universal skill *also* has signal-driven justification (e.g., `builder` strongly relevant due to Rust + custom auth), include it in the table at H affinity AND keep it in the universal array. The duplication is intentional — readers see both the universal status and the rationale.

---

## 9. REPORT Format

After cache write, print 5 lines:

```
✓ Compass cache generated: .claude/compass-cache.md
  - Detected: <primary_language> + <frameworks joined by, max 3>
  - Size: <repo_size> ({file_count} files) → top_n = <N>
  - Cached: <N> + universal 12 = <total> entries
  - Next runs: /compass recommend works from cache only (~95% context reduction)
  - Refresh: /compass refresh / TTL: <ttl_days> days
```

For `refresh`, prepend the diff:

```
↻ Compass cache refreshed: .claude/compass-cache.md
  - Added: <skill_a>, <skill_b> (<reason>)
  - Removed: <skill_c> (<reason>)
  - Changed: <skill_d>: M → H (<reason>)
  ...followed by the same lines as init
```

---

## 10. Anti-Patterns

- **Caching in low-signal repos** (no `package.json`, `Cargo.toml`, etc.): ask the user if they want a cache; auto-pick may be inaccurate.
- **Treating cache write as best-effort**: always validate the written file by re-reading it. If parse fails, fall back to full catalog and warn.
- **Including the same skill in `universal_skills` and the table at L affinity**: only duplicate when affinity is H.
- **Refreshing without diff**: `refresh` must show what changed; otherwise users can't tell whether the refresh was useful.
- **Auto-refreshing on TTL expiry**: refresh is always user-initiated. The TTL only triggers a warning.
- **Hand-editing `top_n`**: regenerate via `refresh` if the size feels wrong; the formula encodes the trade-off.
- **Caching across `git worktree` checkouts that differ structurally**: cache is per-cwd; worktrees with very different stacks should each have their own cache.

---

## 11. Failure Modes & Fallbacks

| Failure | Behavior |
|---------|----------|
| Cannot read `reference/catalog.md` (e.g., not in skills repo) | Abort with clear error: "Compass cache requires access to reference/catalog.md" |
| Cannot write `.claude/compass-cache.md` (perm error) | Print error, continue with full-catalog recommend |
| Manifest file is malformed JSON/TOML/YAML | Log warning, treat as if absent, continue |
| File-count probe fails | Default to `medium` / `top_n = 25` |
| Cached skill no longer exists in catalog | Drop silently from candidates |
| Cache file's frontmatter is malformed | Treat as missing, auto-prompt to regenerate |
