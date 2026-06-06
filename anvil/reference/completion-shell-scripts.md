# Shell Completion Reference

**Purpose:** Generate correct, testable shell completion for Bash, Zsh, Fish, and PowerShell. Completion is part of the CLI contract — it must stay in sync with flags, subcommands, and dynamic values without degrading shell startup.
**Read when:** Adding a `completion` subcommand, picking between static vs dynamic completion, wiring cobra / clap / argparse / oclif generators, or documenting install locations across package managers.

## Scope Boundary

- **Anvil `completion`**: completion-script generation, generator integration, install-path conventions, dynamic completion callbacks, completion testing harness.
- **Builder (elsewhere)**: feature/business logic the completion suggests values from (e.g., project listing API).
- **Hearth (elsewhere)**: personal dotfile setup for the user's own shell — sourcing completions in `~/.zshrc`, fpath configuration, completion caching on login.
- **Gear (elsewhere)**: CI pipeline that regenerates and publishes completion files with the release, dependency updates for the completion generator itself.
- **Launch (elsewhere)**: versioning, changelog entries, and rollout plan when completion output format changes.

If the request is "emit a completion script for this CLI" → `completion`. If it is "make completions load fast in my `.zshrc`" → Hearth. If it is "publish completions to Homebrew formula on release" → Launch plus Gear.

## Static vs Dynamic Completion

| Mode | When to pick | Cost |
|------|-------------|------|
| Static | Flags and subcommands only; values are free-form | Single generated file, zero runtime cost |
| Dynamic (callback) | Value completions need live data (projects, branches, hosts, K8s namespaces) | CLI must stay fast: completion shell-out runs on every `<Tab>` |
| Hybrid | Static tree for commands/flags, dynamic only for argument values | Most common; keeps latency bounded |

Rule of thumb: if the dynamic callback takes >150 ms the user perceives lag. Cache dynamic values (file mtime, TTL) or fall back to static suggestions.

## Generator Integration

| Language / Framework | Generator | Invocation | Output supports |
|----------------------|-----------|-----------|-----------------|
| Go / cobra | `cobra.Command.GenBashCompletionV2` / `GenZshCompletion` / `GenFishCompletion` / `GenPowerShellCompletion` | `myapp completion {bash,zsh,fish,powershell}` | All four shells, dynamic via `ValidArgsFunction` |
| Rust / clap | `clap_complete::generate` with `Shell::Bash` etc. | `myapp completion <shell>` | All four; dynamic via `clap_complete::dynamic` (unstable) |
| Python / argparse | `argcomplete` (`register-python-argcomplete myapp`) | eval in shell rc | Bash/Zsh/Fish; dynamic via `completer=` kwarg |
| Python / click | `click.shell_completion` (`_MYAPP_COMPLETE=bash_source myapp`) | Env-var driven emission | Bash/Zsh/Fish; dynamic via `shell_complete=` |
| Node.js / oclif | `@oclif/plugin-autocomplete` | `myapp autocomplete --refresh-cache` | Bash/Zsh/PowerShell |
| Node.js / commander | `tabtab` or hand-rolled | Varies | Limited; hand-roll dynamic callbacks |

Expose a single subcommand the user pipes to their shell:

```
# Bash
myapp completion bash > /etc/bash_completion.d/myapp
# Zsh
myapp completion zsh > "${fpath[1]}/_myapp"
# Fish
myapp completion fish > ~/.config/fish/completions/myapp.fish
# PowerShell
myapp completion powershell | Out-String | Invoke-Expression
```

## Install Location Conventions

| Shell | System path | User path | Notes |
|-------|-------------|-----------|-------|
| Bash | `/etc/bash_completion.d/myapp` or `/usr/share/bash-completion/completions/myapp` | `~/.local/share/bash-completion/completions/myapp` | Requires `bash-completion` package sourced; do not hard-code `/etc/bash_completion.d/` — Debian-only path |
| Zsh | `/usr/share/zsh/site-functions/_myapp` | `~/.zsh/completions/_myapp` (user adds to `fpath`) | File must start with `#compdef myapp` and be named `_myapp` |
| Fish | `/usr/share/fish/vendor_completions.d/myapp.fish` | `~/.config/fish/completions/myapp.fish` | Fish auto-loads — no sourcing needed |
| PowerShell | N/A (per-user only) | `$PROFILE` (typically `~/Documents/PowerShell/Profile.ps1`) | Appended as `Register-ArgumentCompleter` block |

Homebrew formulae install into `#{bash_completion}`, `#{zsh_completion}`, `#{fish_completion}` — let the package manager place files, do not ship post-install scripts writing to `/etc/`.

## Dynamic Completion Contract

When shell invokes the CLI for dynamic completion it usually sets an env var (`COMP_LINE`, `_CLICK_COMPLETE`, `COBRA_COMPLETE_NO_DESC`). Keep callbacks:

1. **Fast**: no network call without a cache; read-only filesystem at most.
2. **Silent on stderr**: any stderr output corrupts the completion stream in older Bash.
3. **Deterministic on failure**: return empty (exit 0) rather than erroring — a failed callback must not break the user's Tab key.
4. **TTY-unaware**: never prompt, never paginate, never emit colour.

## Testing Completion

```
# Bash: assert expected completions for a given prefix
bash -c 'source ./completion.bash; COMP_WORDS=(myapp dep); COMP_CWORD=1; _myapp; echo "${COMPREPLY[@]}"'

# Zsh (non-interactive): use compinit in a fresh env
zsh -c 'autoload -Uz compinit; compinit -u; source ./_myapp; _myapp <<< "myapp dep\t"'

# Fish
fish -c 'source ./myapp.fish; complete -C "myapp dep"'
```

Wire these into the test suite so a dropped subcommand fails CI, not just `--help`.

## Anti-patterns

- Shipping completions that drift from actual flags — always regenerate in CI from the same source as `--help`.
- Hard-coding `/etc/bash_completion.d/` in install scripts; it does not exist on macOS default Bash or NixOS.
- Writing dynamic callbacks that make HTTPS calls on every Tab — latency and rate-limit risk.
- Emitting ANSI colour or progress bars during completion callback execution.
- Using `eval` on unsanitised user input inside completion (shell-injection via crafted completion output).
- Forgetting `#compdef myapp` on the first line of a Zsh completion file — silent non-activation.
- Missing PowerShell completion on Windows-targeted CLIs because "nobody uses it" — users with `pwsh` on macOS/Linux rely on it.
- Coupling completion generation to runtime config: the `completion` subcommand must work on a fresh install with no config file present.

## Handoff

When `completion` is done, pass to the next phase:

- **To Launch**: note whether completion output format changed (breaking change for cached completions in package managers).
- **To Gear**: CI step that regenerates `completion.{bash,zsh,fish,ps1}` and commits / attaches to release.
- **To Hearth** (for the authoring user): one-liner that sources the freshly generated completion into the user's own shell for local testing.
- **To `pkg`**: install-path directives for Homebrew / deb / rpm formulae.
