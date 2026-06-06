# Scripts Directory Organization Reference

Purpose: Design and audit `scripts/` directory layout — language selection (shell vs Node vs Python vs Go), category split (setup/build/release/dev), `package.json scripts` vs dedicated directory trade-offs, naming conventions, and shebang/executable-bit hygiene. Optimizes for discoverability, portability, and resistance to bit-rot.

## Scope Boundary

- **grove `scripts`**: filesystem layout for repo scripts — directory split, language-pick rubric, naming, shebangs, executable bits, package.json delegation. Layout-only, not script content.
- **grove `audit` / `design` / `docs` / `migrate` (default + siblings)**: structural audit, generic directory design, docs/, level-based migration. Use these when scope is broader than scripts/.
- **grove `monorepo` / `tests` (siblings)**: workspace-level layout and tests/ — Grove `scripts` is invoked alongside or per-package.
- **Anvil (elsewhere)**: CLI/TUI implementation. Grove `scripts` decides where a script lives; Anvil owns the CLI command surface and dev-tool wiring once it grows beyond a thin script.
- **Gear (elsewhere)**: CI/CD pipeline config and `npm run`/`make` task graph. Grove `scripts` decides directory; Gear decides when CI calls them.
- **Scaffold (elsewhere)**: cloud IaC. `infra/` provisioning scripts (Terraform, Pulumi) belong to Scaffold, not Grove `scripts`.
- **Hearth (elsewhere)**: personal dotfiles and shell config. Grove `scripts` is repo-shared; Hearth is per-developer.
- **Nest (elsewhere)**: LLM-context ordering of `scripts/`. Grove ships layout; Nest tunes retrieval.

## Workflow

```
INVENTORY → list every existing script (root, scripts/, package.json scripts, Makefile targets, bin/)
          → record language, line count, last-modified date, caller (CI? human? hook?)

CATEGORIZE → tag each script: setup | build | release | dev | ci | maintenance
           → flag duplicates, dead scripts, undocumented entrypoints

LANGUAGE  → apply rubric: shell ≤ 30 lines, Node 30–200, Python > 200 with deps, Go for shipped binaries
          → flag scripts violating the rubric (500-line bash, 5-line Python with no deps)

LAYOUT    → split scripts/<category>/<verb-noun>.<ext>; promote root-level loose scripts; demote one-liners back to package.json
          → set shebang + chmod +x consistently

VERIFY    → every script runs from repo root; no hardcoded paths; portable (macOS + Linux + CI)
          → README.md or `scripts/README.md` lists all entrypoints with one-line purpose

PRESENT   → layout diagram, language-rubric findings, naming/shebang fixes
          → hand CLI growth to Anvil; CI wiring to Gear; IaC to Scaffold
```

## Language Selection Rubric

| Scope | Recommended | Avoid | Rationale |
|-------|-------------|-------|-----------|
| ≤ 30 lines, simple shell pipelines | bash/sh (`#!/usr/bin/env bash` + `set -euo pipefail`) | Node, Python | Zero install footprint, native to CI |
| 30–200 lines, JSON/network/cross-platform | Node (`#!/usr/bin/env node`) or Deno | Bash (quoting hell), pure Python (extra runtime in JS repos) | Already on PATH in JS repos; portable |
| > 200 lines or heavy data/parsing | Python (with `uv` or virtualenv) | Bash, ad-hoc Node | Standard library, tested ecosystem |
| Distributed binary (cross-platform, no runtime) | Go or Rust | Shell (no Windows), Python (runtime install) | Single static binary, fast |
| > 500 lines or growing CLI surface | promote to a real CLI tool | growing the script | Hand off to Anvil |

If a script crosses 200 lines in bash, treat it as a code smell — port to Node/Python or split.

## Category Split

```
scripts/
  setup/                 # one-time per dev: install deps, generate env, init DB
    bootstrap.sh
    install-hooks.sh
    seed-db.ts
  dev/                   # daily inner-loop: start, watch, lint, test helpers
    dev-server.sh
    watch-types.ts
  build/                 # compile, bundle, generate artifacts
    build-all.sh
    generate-types.ts
  release/               # version, changelog, publish, tag
    bump-version.ts
    publish.sh
  ci/                    # CI-only entrypoints (matrix split, cache prime)
    affected.sh
    cache-warm.sh
  maintenance/           # rare: migrations, backfills, cleanups
    backfill-users.ts
    rotate-keys.sh
  README.md              # one-line purpose for every script
```

Optional: `bin/` for executables on PATH after `npm install -g .` (publishable CLIs only). Do not mix `bin/` and `scripts/`.

## package.json scripts vs scripts/ Directory

| Place in `package.json scripts` | Place in `scripts/` |
|---------------------------------|---------------------|
| One-liner (`tsc -p .`, `vitest run`) | Multi-step or branching logic |
| Standard verb (`build`, `test`, `lint`, `dev`) | Custom workflows (`scripts/release/publish.sh`) |
| What humans type daily | What CI invokes or developers run rarely |
| Composes other scripts (`pre*`, `post*`) | Heavy lifting referenced by package.json |

`package.json scripts` is the entrypoint table; `scripts/` holds the implementations. Pattern: `"build": "node scripts/build/build-all.ts"`. Avoid 5-line bash inside a JSON string — it loses syntax highlighting, quoting safety, and editor support.

## Naming Conventions

- **Pattern**: `verb-noun.ext` (`bump-version.ts`, `seed-db.sh`, `rotate-keys.sh`).
- **Lowercase, hyphens** — never `CamelCase` or `snake_case` (mixing breaks tab-completion expectations).
- **Verb-first** — `bump-version` not `version-bump`. Predictable for `ls scripts/release/`.
- **No leading numbers** unless ordering matters (`01-bootstrap.sh`); prefer documented sequence in README.
- **Extension matters**: `.sh` for bash, `.ts`/`.js` for Node, `.py` for Python, `.go` for Go. Do not strip extensions to "look like commands" — that hides the runtime.

## Shebang and Executable Bit

| Language | Shebang | Notes |
|----------|---------|-------|
| bash | `#!/usr/bin/env bash` | Always pair with `set -euo pipefail` |
| sh | `#!/bin/sh` | POSIX only; avoid bash-isms |
| Node | `#!/usr/bin/env node` | Or `#!/usr/bin/env -S node --experimental-strip-types` for TS |
| Python | `#!/usr/bin/env python3` | Never bare `python` |
| Deno | `#!/usr/bin/env -S deno run --allow-read` | Permissions explicit |

Set executable bit: `chmod +x scripts/**/*.sh scripts/**/*.ts`. Commit it: `git update-index --chmod=+x scripts/...`. Without `+x`, users must invoke `bash scripts/foo.sh` and lose tab-completion of the script name.

## Anti-Patterns

- **AP-SC-01 — root-level loose scripts**: 12 `.sh` files at repo root. Discoverability dies; CI YAML hardcodes paths. Move to `scripts/<category>/`.
- **AP-SC-02 — 500-line bash scripts**: complex logic, no tests, quoting bugs. Port to Node or Python; ≤ 200 lines is the soft ceiling.
- **AP-SC-03 — `package.json` 30-line one-liners**: `"build": "rm -rf dist && tsc && cp -r assets dist/ && node scripts/post.js && ..."`. Move to `scripts/build/build-all.ts` and call once.
- **AP-SC-04 — missing shebang or `+x` bit**: users hit `Permission denied` or bash-runs-Node nonsense. Lint with a pre-commit hook.
- **AP-SC-05 — bash-isms in `#!/bin/sh`**: `[[ ]]`, arrays, `${var,,}` break on Alpine and POSIX sh. Either use `#!/usr/bin/env bash` or strict POSIX.
- **AP-SC-06 — no `set -euo pipefail`**: bash silently continues past errors; failed pipes invisible. Always set it; `set -x` for debug.
- **AP-SC-07 — duplicated `release-*.sh` per package**: copy-pasted release scripts drift. Centralize in `scripts/release/` and parameterize, or use Changesets/Nx release.
- **AP-SC-08 — undocumented entrypoints**: 40 scripts, no README. New devs grep blindly. `scripts/README.md` with one line per script is non-negotiable.
- **AP-SC-09 — hardcoded absolute paths**: `/Users/alice/repo/...` baked in. Use `$(git rev-parse --show-toplevel)` or relative paths from `cd "$(dirname "$0")"`.

## Handoff

- **To Anvil**: when a script grows past 500 lines or spawns subcommands (`scripts/dev/cli.ts <cmd>`), Anvil designs a real CLI on top.
- **To Gear**: package.json scripts that CI calls (`build`, `test`, `lint`) become Gear's pipeline inputs; CI YAML references `scripts/ci/*` after Grove locks paths.
- **To Scaffold**: anything in `scripts/` that provisions cloud resources moves to `infra/` and becomes Scaffold's responsibility.
- **To Hearth**: per-developer environment helpers (shell aliases, prompt configs) go to dotfiles, not repo `scripts/`.
- **To Nest**: once layout is stable, Nest reorders for LLM-context retrieval (README front-loading, category headers).
- **To Sigil**: Grove publishes the scripts layout; Sigil generates project-tuned skills referencing exact script paths.
- **To Guardian**: when reorganizing scripts in an existing repo, Guardian slices PRs (≤ 50 files, CI-green per commit) and updates CI references in lockstep.
