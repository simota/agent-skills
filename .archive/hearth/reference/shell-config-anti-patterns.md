# Shell Configuration Anti-Patterns

Purpose: Read this when auditing shell startup performance, module structure, plugin-management risk, or shell regressions. Keep the `SH-*` and `PM-*` identifiers intact in findings and handoffs.

## Contents

- [Startup-performance anti-patterns](#startup-performance-anti-patterns)
- [Structure anti-patterns](#structure-anti-patterns)
- [Plugin-management anti-patterns](#plugin-management-anti-patterns)
- [Measurement and targets](#measurement-and-targets)
- [How Hearth uses this reference](#how-hearth-uses-this-reference)

## Startup-Performance Anti-Patterns

| Code | Anti-pattern | Risk | Signal | Countermeasure |
|------|--------------|------|--------|----------------|
| `SH-01` | Eager version-manager loading | `nvm` / `pyenv` / `rbenv` / `conda` add `300-500ms` each | Shell startup exceeds `1s` | Lazy-load wrappers or consolidate with `mise` |
| `SH-02` | Multiple `compinit` calls | Completion initialization repeats `200ms+` work | Completion setup appears in multiple files | Run `compinit` once after `$fpath` is complete and cache the dump daily |
| `SH-03` | Full `oh-my-zsh` framework usage | Framework + completion dominate startup cost | Framework time dominates `zprof` | Keep only required plugins or switch to `sheldon` / `zim` |
| `SH-04` | Synchronous plugin loading | Startup cost grows linearly with plugin count | Prompt appears only after all plugins load | Use `zsh-defer`, `sheldon` defer, or `zinit` turbo |
| `SH-05` | Heavy prompt rendering | Prompt runs expensive subprocesses on every draw | Large repos make the prompt stall | Prefer `starship` or `powerlevel10k` instant prompt |
| `SH-06` | `eval "$(tool init zsh)"` everywhere | Re-runs tool initialization on every shell start | `starship`, `zoxide`, or `fzf` init calls dominate profiles | Cache the generated init script and `source` the cache |
| `SH-07` | Auto-update on every launch | Hidden network checks slow every shell start | Plugin manager checks the network at startup | Disable auto-update and update explicitly |

## Structure Anti-Patterns

| Pattern | Risk | Countermeasure |
|---------|------|----------------|
| Monolithic `.zshrc` | Change impact is unclear; debugging is slow | Split into `env.zsh`, `aliases.zsh`, `plugins.zsh`, `local.zsh`, and related modules |
| No `local.zsh` separation | Machine-specific values leak into tracked files | Keep machine-local data in a gitignored file |
| Hard-coded paths | Shared configs break across macOS and Linux | Detect OS and tool installation paths before exporting them |
| No XDG compliance | Home directory sprawl and weak portability | Set `ZDOTDIR=$XDG_CONFIG_HOME/zsh` in `~/.zshenv` |
| Source-order mistakes | Tools fail because `PATH` or env vars are not ready | Preserve `env -> path -> plugins -> completions -> aliases -> local` |

## Plugin-Management Anti-Patterns

| Code | Anti-pattern | Risk | Countermeasure |
|------|--------------|------|----------------|
| `PM-01` | Plugin hoarding | Unused plugins keep slowing startup | Review monthly and remove plugins unused for two weeks |
| `PM-02` | Framework lock-in | Adding or swapping plugins becomes expensive | Prefer per-plugin managers such as `sheldon` or `zim` |
| `PM-03` | Compilation overhead | Compile steps add first-run latency and cache issues | Prefer `sheldon` when compile-time tricks are unnecessary |
| `PM-04` | No plugin pinning | Updates break reproducibility | Pin tags or commit SHAs where the manager supports it |

## Measurement and Targets

### Measurement Commands

```text
Profiling:
  1. zmodload zsh/zprof
  2. zprof

Wall-clock:
  /usr/bin/time zsh -i -c exit
  hyperfine 'zsh -i -c exit'
```

### Startup Targets

| Profile | Target | Upper bound |
|---------|--------|-------------|
| `Minimal` | `< 50ms` | `< 100ms` |
| `Standard` | `< 150ms` | `< 250ms` |
| `Power` | `< 250ms` | `< 400ms` |

### Optimization Priority

1. Lazy-load version managers: expected improvement `300-500ms`
2. Run `compinit` once and cache results: expected improvement `100-200ms`
3. Remove unused plugins: expected improvement `50-150ms`
4. Simplify the prompt: expected improvement `50-100ms`
5. Cache `tool init` output: expected improvement `30-80ms`

### Quality Gates

- Startup time `> 250ms` requires `zprof` analysis and a bottleneck report.
- `.zshrc` over `200` lines should trigger modularization guidance.
- `.zshrc` over `500` lines is an anti-pattern, not just a style issue.
- Keep `compinit` to one call after `$fpath` is final.

## How Hearth Uses This Reference

```text
SCAN:
  Screen for SH-01..07 startup regressions

PLAN:
  Check module structure, XDG layout, and plugin strategy

CRAFT:
  Design fixes for PM-01..04 and source-order issues

VERIFY:
  Run timing, profiling, and target comparison
```

### Required Gates

- Detect `eval "$(tool init)"` and recommend cache-based replacement.
- Detect full `oh-my-zsh` usage and recommend lighter alternatives.
- Detect direct `nvm` / `pyenv` eager loading and recommend lazy loading or `mise`.
- Detect non-XDG zsh layouts and recommend `ZDOTDIR` migration.
