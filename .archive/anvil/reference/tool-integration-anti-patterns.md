# Tool Integration Anti-Patterns

**Purpose:** Failure patterns for linting, formatting, build/test tooling, doctor commands, and configuration management.
**Read when:** Reviewing project tooling for setup friction, CI drift, missing diagnostics, or fragile config behavior.

## Contents

- Seven Linter and Formatter Setup Anti-Patterns
- Build Tool Integration Anti-Patterns
- Test Runner Integration Anti-Patterns
- Doctor / Healthcheck Anti-Patterns
- Configuration Management Anti-Patterns
- How To Use With Anvil

## 1. Seven Linter and Formatter Setup Anti-Patterns

| # | Anti-Pattern | Problem | Signals | Fix |
|---|-------------|---------|---------|-----|
| **TI-01** | **Config Fragmentation** | Requiring 10+ packages and 3+ config files for basic quality tooling | ESLint + Prettier + tsconfig + `.editorconfig` + lint-staged just to start; setup takes 30+ minutes | Prefer consolidated tooling such as Biome and provide presets |
| **TI-02** | **Rule Suppression Addiction** | Disabling lint rules without understanding them | Files accumulate `// eslint-disable` headers and lint stops meaning anything | Require a reason for suppressions, baseline legacy violations, and keep new code strict |
| **TI-03** | **Version Conflict Hell** | Letting linters, formatters, and plugins drift out of compatibility | `npm install` shows peer dependency warnings or runtime crashes | Lock versions strictly and prefer tested presets |
| **TI-04** | **Format-on-Save Only** | Relying only on editor integration for formatting | Team editors disagree and PRs contain huge formatting-only diffs | Enforce formatting in CI and add pre-commit hooks |
| **TI-05** | **Inconsistent Tool Chain** | Using different tool versions locally and in CI | Local checks pass but CI fails | Pin tool versions with mise/asdf and reuse the same versions in CI |
| **TI-06** | **Kitchen Sink Config** | Enabling every recommended rule regardless of project needs | Meaningless warnings flood the output and developers learn to ignore linting | Start with project-relevant rules and add more gradually |
| **TI-07** | **No Baseline Strategy** | Applying strict new rules to a legacy codebase all at once | Thousands of violations appear and teams abandon the effort | Freeze legacy violations in a baseline and enforce strictness on new code only |

---

## 2. Build Tool Integration Anti-Patterns

```text
Build integration traps:

  ❌ Slow Feedback Loop:
    → Lint or test feedback takes more than 10 seconds after a file change
    → Developers move on before feedback arrives
    → Fix: use incremental builds, change-based checks, and caching

  ❌ Global Install Dependency:
    → Assuming tools are installed globally
    → Team machines drift and onboarding becomes painful
    → Fix: prefer `npx`, `pipx`, `go run`, or project-local installs

  ❌ Implicit Tool Resolution:
    → Using whichever tool version appears first on `PATH`
    → Different environments run different versions and results become non-reproducible
    → Fix: pin versions per project with mise/asdf or equivalent

  ❌ Monolithic Check Script:
    → `npm run check` bundles lint, format, test, and build into one opaque command
    → The first failure stops everything and individual workflows cannot run separately
    → Fix: keep granular commands and add an aggregate entrypoint on top

  ❌ No Cache Strategy:
    → Running full builds and full linting in CI every time
    → Build time and CI costs grow needlessly
    → Fix: use tool-native caches such as `--cache` / `--cached`

  ❌ Hook Bypass Culture:
    → Teams always pass `--no-verify` to skip hooks
    → Local quality gates stop mattering
    → Fix: make CI mandatory and keep hook runtimes fast, ideally under five seconds
```

---

## 3. Test Runner Integration Anti-Patterns

```text
Test integration traps:

  ❌ Inconsistent Test Commands:
    → Every project uses a different way to run tests
    → New contributors have to rediscover the commands
    → Fix: define standard commands in `package.json`, `Makefile`, or `Taskfile`

  ❌ No Watch Mode:
    → Re-running tests manually after every change
    → Feedback loops break
    → Fix: provide `--watch` for file-change-driven execution

  ❌ All-or-Nothing Testing:
    → Always running the full test suite regardless of the change
    → Tests take minutes, so developers stop running them
    → Fix: support changed-test or related-test execution

  ❌ Noisy Test Output:
    → Printing every passing test in detail
    → Failures become hard to find
    → Fix: keep default output failure-focused and move full detail behind `--verbose`

  ❌ No Parallel Execution:
    → Running tests serially by default when the runner supports parallelism
    → Total suite time grows linearly
    → Fix: enable `--parallel`, `--workers`, or runner-specific equivalents
```

---

## 4. Doctor / Healthcheck Anti-Patterns

| # | Anti-Pattern | Problem | Signals | Fix |
|---|-------------|---------|---------|-----|
| **DH-01** | **No Doctor Command** | There is no first-class way to diagnose environment issues | Users manually inspect versions and config state | Provide `app doctor` to run environment checks in one place |
| **DH-02** | **Diagnostic Without Fix** | The tool detects problems but never suggests repairs | Users must research every fix themselves | Print concrete repair commands or next steps per issue |
| **DH-03** | **Silent Dependency** | Missing tools lead to cryptic runtime failures | Users see `command not found` or `ENOENT` without context | Check dependencies at startup and print install instructions |
| **DH-04** | **Version Ambiguity** | Required version ranges are unclear | Old versions fail in strange ways | Show current vs required versions explicitly in `doctor` |

---

## 5. Configuration Management Anti-Patterns

```text
Configuration management traps:

  ❌ Config Discovery Mystery:
    → Users cannot tell which config file actually loaded
    → Misconfigurations are hard to debug
    → Fix: add `--config-debug` to print the loaded files and precedence order

  ❌ Schema-less Config:
    → Config files are never validated
    → Typos like `colr: true` silently do nothing
    → Fix: validate against JSON Schema or an equivalent typed schema and suggest likely keys

  ❌ Breaking Config Changes:
    → Upgrades silently change config structure
    → Existing installs stop working after an update
    → Fix: version config formats and provide migration commands or guides

  ❌ No Default Config:
    → The CLI cannot start without a hand-written config file
    → First-run experience is hostile
    → Fix: support zero-config defaults and offer `app init` to generate config
```

---

## 6. How To Use With Anvil

```text
Use within Anvil:
  1. Review TI-01 to TI-07 during BLUEPRINT to shape toolchain scope
  2. Review build scripts and command structure during CAST
  3. Review CI/CD and cross-environment behavior during HARDEN
  4. Review doctor commands and config management during PRESENT

Quality gates:
  - 3+ config files for one toolchain concern → propose consolidation (prevent TI-01)
  - 5+ disable comments per file → introduce a baseline strategy (prevent TI-02)
  - Global installs required → move to local execution patterns (prevent Global Install Dependency)
  - Full build exceeds 10 seconds → introduce cache or incremental checks (prevent Slow Feedback Loop)
  - No doctor command → add environment diagnostics (prevent DH-01)
  - No config validation → add schema-backed validation (prevent Schema-less Config)
```

**Source:** [Meta: Fixit 2 Linter](https://engineering.fb.com/2023/08/07/developer-tools/fixit-2-linter-meta/) · [Command Line Interface Guidelines](https://clig.dev/) · [Atlassian: 10 Design Principles for Delightful CLIs](https://www.atlassian.com/blog/it-teams/10-design-principles-for-delightful-clis) · [ESLint Documentation](https://eslint.org/)
