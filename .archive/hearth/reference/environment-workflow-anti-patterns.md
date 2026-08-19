# Environment and Workflow Anti-Patterns

Purpose: Read this when auditing environment reproducibility, macOS configuration, tool-selection drift, package management, or workflow integration. Keep the `EN-*` and `TS-*` identifiers intact in findings and handoffs.

## Contents

- [Environment reproducibility anti-patterns](#environment-reproducibility-anti-patterns)
- [macOS anti-patterns](#macos-anti-patterns)
- [Tool-selection anti-patterns](#tool-selection-anti-patterns)
- [Workflow-integration traps](#workflow-integration-traps)
- [Modern tool-stack defaults](#modern-tool-stack-defaults)
- [How Hearth uses this reference](#how-hearth-uses-this-reference)

## Environment Reproducibility Anti-Patterns

| Code | Anti-pattern | Risk | Countermeasure |
|------|--------------|------|----------------|
| `EN-01` | Non-reproducible environment | New-machine setup takes `1 day` and drifts from memory | Track dotfiles, `Brewfile`, and bootstrap steps |
| `EN-02` | Version-manager sprawl | Multiple init paths add `500ms+` of shell cost | Consolidate to `mise` where practical |
| `EN-03` | Unmanaged `Brewfile` | Reinstall steps are unclear | Keep `brew bundle dump --describe` in sync |
| `EN-04` | No OS detection | Shared configs break across macOS and Linux | Branch on `uname -s`, `$OSTYPE`, or templates |
| `EN-05` | Tool-version drift | Local behavior diverges from project or CI | Pin versions with `.tool-versions`, `.mise.toml`, or equivalent |
| `EN-06` | Manual font installation | Icons fail on fresh machines | Track Nerd Fonts in package management |
| `EN-07` | No environment validation | Broken setup stays undetected for days | Run version checks, syntax checks, and connectivity tests after setup |

## macOS Anti-Patterns

| Pattern | Risk | Countermeasure |
|---------|------|----------------|
| Undocumented `defaults write` | System behavior changes without explanation or rollback knowledge | Add comments for purpose and inspect current state with `defaults read` first |
| No restart warning | Settings appear not to work | Tell the user when `killall Finder` or `killall Dock` is required |
| Aggressive system modification | Security posture degrades | Require explicit confirmation for SIP, Gatekeeper, or similar changes |
| Over-complex Karabiner rules | Remaps become unmaintainable | Keep rules minimal; `50+` rules is a warning sign |
| No macOS version compatibility check | Scripts break after OS upgrades | Check `sw_vers` and skip unsupported settings |

## Tool-Selection Anti-Patterns

| Code | Anti-pattern | Risk | Countermeasure |
|------|--------------|------|----------------|
| `TS-01` | Hype-driven adoption | Tools change faster than the workflow stabilizes | Keep a trial period before committing |
| `TS-02` | Copy-paste configuration | The setup is impossible to debug later | Add only understood lines and keep comments |
| `TS-03` | Deprecated-tool retention | Older tools stay even when faster replacements exist | Periodically review replacements such as `mise` or `fnm` |
| `TS-04` | Kitchen-sink setup | `Brewfile` exceeds `100+` packages and maintenance balloons | Install tools when needed and prune regularly |

## Workflow-Integration Traps

| Pattern | Risk | Countermeasure |
|---------|------|----------------|
| Inconsistent theme | Visual context switching stays noisy | Apply one theme family consistently, for example Catppuccin |
| Broken clipboard chain | tmux, Neovim, and the system clipboard stop sharing data | Use OSC 52 in Neovim, `set-clipboard on` in tmux, and terminal OSC 52 support |
| SSH incompatibility | TERM, colors, or clipboard break on remote hosts | Provide terminfo transfer and a `TERM=xterm-256color` fallback |
| Undocumented aliases | Alias sets become opaque and conflict-prone | Group aliases and comment them |
| PATH pollution | Duplicate entries grow on every startup | Centralize PATH edits and use `typeset -U path` in zsh |

## Modern Tool-Stack Defaults

| Category | Legacy | Preferred modern default | Reason |
|----------|--------|--------------------------|--------|
| Shell framework | `oh-my-zsh` | `sheldon` / `zim` | Lower startup cost |
| Version manager | `nvm + pyenv + rbenv` | `mise` | One faster tool |
| File listing | `ls` | `eza` | Better Git and tree support |
| File search | `find` | `fd` | Faster and gitignore-aware |
| Text search | `grep` | `ripgrep` | Faster and practical defaults |
| Directory jumping | `cd` | `zoxide` | Learned history |
| Diff | `diff` | `delta` | Better terminal review output |
| `cat` replacement | `cat` | `bat` | Highlighting and pager support |
| Node manager | `nvm` | `fnm` | Faster startup path |

## How Hearth Uses This Reference

```text
SCAN:
  Screen for EN-01..07 and workflow breakpoints

PLAN:
  Decide whether the issue is reproducibility, platform-specific, or tool-selection debt

CRAFT:
  Build the smallest fix that restores reproducibility and integration

VERIFY:
  Run bootstrap, package, font, clipboard, and OS-compatibility checks
```

### Required Gates

- Missing `install.sh`, missing `Makefile`, or missing package tracking should be called out when reproducibility is part of the task.
- Package drift should be verified with `brew bundle check` when Homebrew is in scope.
- `defaults write` changes should keep comments, rollback awareness, and version checks.
- PATH duplication should be fixed centrally rather than by adding more exports.
