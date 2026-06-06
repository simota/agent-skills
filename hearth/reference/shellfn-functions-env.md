# Shell Functions, Aliases, and Env Management Reference

Purpose: Read this when organizing shell functions and aliases, managing `PATH`, wiring per-project tooling with `direnv` / `mise` / `asdf` / `nvm`, enforcing XDG directories, and lazy-loading heavy completions. Hearth owns **your** personal shell function layout; publishable CLI tools and team tooling manifests belong elsewhere.

## Scope Boundary

- **Hearth `shellfn`**: personal shell functions, aliases, env-var strategy, PATH hygiene, `direnv` / `mise` / `asdf` / `nvm` wiring, XDG migration, lazy-loading completions.
- **Anvil (elsewhere)**: publishable CLI tools — when a function grows flags / help text / tests / release needs, hand it off.
- **Latch (elsewhere)**: Claude Code hooks that invoke shell commands — Hearth provides the env, Latch wires the trigger.
- **Gear (elsewhere)**: team-level dependency manifests (`.tool-versions` / `mise.toml` committed as a contract), CI version pinning.
- **Grove (elsewhere)**: repo structure for `.envrc` / `.tool-versions` / `mise.toml` as project artifacts.

If the question is "how do I organize my own functions and env?" → `shellfn`. If it is "how should the team pin tool versions?" → Gear.

## Function Organization

| Strategy | Pros | Cons | Pick when |
|----------|------|------|-----------|
| One-file-per-function (`~/.config/zsh/functions/`) | Autoload friendly, diff-clean | More files | Standard default |
| Grouped rc file | Single-file grep | Harder autoload, large diffs | Small set (<10) |
| Inline in `.zshrc` | Zero indirection | Bloats startup | Never for reusable logic |

```zsh
# ~/.zshrc — autoload pattern (zsh)
fpath=(~/.config/zsh/functions $fpath)
autoload -Uz ~/.config/zsh/functions/*(:t)
```

Each file is one function named after the file. Bash has no autoload equivalent — source regularly or use a lazy wrapper pattern.

## Alias vs Function

| Use alias when | Use function when |
|----------------|-------------------|
| No args or trailing args only | Args need reordering or validation |
| Simple substitution | Multi-line logic, conditionals, quoting |

Rule: if you ever want to quote `$1` or add `if`, make it a function.

## PATH Hygiene

```zsh
typeset -U path PATH         # enforce uniqueness
path=(
  ~/.local/bin
  ~/bin
  /opt/homebrew/bin          # macOS ARM
  /usr/local/bin             # macOS Intel / Linuxbrew
  $path
)
export PATH

prepend_path() { [[ -d "$1" ]] && path=("$1" $path) }
prepend_path ~/.cargo/bin
prepend_path ~/.bun/bin
```

`typeset -U path` removes duplicate entries on add — eliminates a whole class of PATH bugs. `[[ -d ]]` guards prevent stale entries after uninstalls.

### Anti-Pattern: `brew shellenv` in startup

```zsh
# ❌ spawns Ruby, 50-100ms per shell
eval "$(/opt/homebrew/bin/brew shellenv)"

# ✅ inline static output
export HOMEBREW_PREFIX=/opt/homebrew
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:$PATH"
```

Run `brew shellenv` once, paste output, commit as static. Re-run when Homebrew upgrades.

## Per-Project Tooling: mise vs asdf vs nvm vs direnv

| Tool | Languages | Env vars | Tasks | Startup | Pick when |
|------|-----------|----------|-------|---------|-----------|
| `mise` | All (plugins) | Yes | Yes | Low | Unified dev tool — preferred default |
| `asdf` | All (plugins) | No (pair w/ direnv) | No | Medium | Existing team baseline |
| `nvm` | Node only | No | No | High (~200ms) | Legacy Node-only |
| `direnv` | — (env only) | Yes | No | Low | Env isolation without version management |

```toml
# ~/.config/mise/config.toml
[settings]
legacy_version_file = true  # read .tool-versions (asdf compat)

[tools]
node = "20"
python = "3.12"

[env]
EDITOR = "nvim"
```

nvm adds 150-250ms per shell — the biggest single startup cost on Node-heavy machines. Replace with mise, or at minimum lazy-load with an `unfunction` wrapper (same pattern as the kubectl example below).

direnv whitelists per-directory env via `direnv allow`:

```bash
# <repo>/.envrc
export DATABASE_URL=postgres://localhost/dev
use mise   # compose versions
```

```zsh
eval "$(direnv hook zsh)"
```

## XDG Base Directory

```zsh
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
```

| Tool | Override |
|------|----------|
| zsh history | `HISTFILE="$XDG_STATE_HOME/zsh/history"` |
| less | `LESSHISTFILE="$XDG_STATE_HOME/less/history"` |
| Node REPL | `NODE_REPL_HISTORY="$XDG_STATE_HOME/node_repl_history"` |
| GnuPG | `GNUPGHOME="$XDG_DATA_HOME/gnupg"` |

Create target directories in bootstrap — tools crash silently when the path is missing.

## Lazy-Loading Heavy Completions

```zsh
# kubectl completion — only load on first use
kubectl() {
  unfunction kubectl
  source <(command kubectl completion zsh)
  kubectl "$@"
}
```

### `compinit` Discipline

`compinit` rescans `$fpath` and costs 30-80ms. Run once, cache daily:

```zsh
autoload -Uz compinit
if [[ -n ${ZDOTDIR:-$HOME}/.zcompdump(#qN.mh+24) ]]; then
  compinit
else
  compinit -C
fi
```

If a plugin manager also calls `compinit`, disable one call — running it twice is pure overhead.

## Env-Var Organization

Split env vars into numbered files under `~/.config/zsh/env.d/` (e.g. `10-xdg.zsh`, `20-path.zsh`, `30-editor.zsh`, `90-local.zsh` gitignored for host-specific secrets) and load via `for f in $ZDOTDIR/env.d/*.zsh(N); do source "$f"; done`. Split by concern, number for order, gitignore the `*-local.zsh` variant.

## Anti-Patterns

- 50+ aliases / functions inline in `.zshrc` — impossible to share, huge diffs.
- Alias when a function is needed — silent quoting bugs later.
- Prepending to `PATH` without deduplication — grows every reload.
- Hardcoding `/opt/homebrew/bin` without OS/arch detection — breaks on Intel and Linux.
- Running `nvm` eagerly — 150-250ms per shell. Lazy-wrap or switch to `mise`.
- Calling `compinit` twice (framework + custom) — wasted 30-80ms per shell.
- Secrets inline in `.zshrc` — stays in git history forever. Use gitignored `90-local.zsh`.
- Autoloading completions for monthly-use tools — lazy-wrap instead.
- Committing `.envrc` with production URLs — direnv is dev-only; gitignore secret variants.
- Per-repo `mise.toml` for personal preference — belongs in `~/.config/mise/config.toml` unless the team needs the pin.

## Handoff

- Function outgrowing aliases / needs flags, help, tests, release → `Anvil`.
- Claude Code hooks invoking these functions → `Latch`.
- `.tool-versions` / `mise.toml` as team contract → `Gear` + `Grove`.
- PATH/env audit reveals secrets or risky eval in startup → `Sentinel` + Hearth `audit`.
- Reproducing env on a new machine → Hearth dotfile-manager recipe (stow / chezmoi).
