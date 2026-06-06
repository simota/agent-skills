# Dotfile Management Strategies

Purpose: Read this when choosing or applying `stow`, `chezmoi`, `yadm`, bare Git, `Brewfile`, or XDG migration patterns for personal dotfiles.

## Contents

- [GNU Stow](#gnu-stow)
- [chezmoi](#chezmoi)
- [yadm](#yadm)
- [Bare Git repository](#bare-git-repository)
- [Brewfile management](#brewfile-management)
- [XDG Base Directory specification](#xdg-base-directory-specification)
- [Selection guide](#selection-guide)

## GNU Stow

Recommended for a single machine or a simple shared layout.

### Directory Structure

```text
~/dotfiles/
├── zsh/
│   ├── .zshrc
│   └── .config/
│       └── zsh/
├── nvim/
│   └── .config/
│       └── nvim/
├── ghostty/
│   └── .config/
│       └── ghostty/
```

Rule: each package mirrors the target path under `$HOME`.

### Commands

```bash
stow -d ~/dotfiles -t ~ zsh
cd ~/dotfiles && stow */
stow -d ~/dotfiles -t ~ -D zsh
stow -d ~/dotfiles -t ~ -R zsh
stow -d ~/dotfiles -t ~ -n -v zsh
```

### `.stow-local-ignore`

```text
\.git
\.gitignore
\.gitmodules
README\.md
LICENSE
^\.DS_Store
```

### Multi-Machine Pattern

```text
~/dotfiles/
├── zsh/
├── nvim/
├── zsh-work/
├── zsh-personal/
└── linux-specific/
```

```bash
cd ~/dotfiles && stow zsh nvim zsh-work
```

## `chezmoi`

Recommended for multiple machines, template logic, or secret integration.

### Workflow

```bash
chezmoi init
chezmoi add ~/.zshrc
chezmoi edit ~/.zshrc
chezmoi diff
chezmoi apply
```

### Go Template Example

```text
{{ if eq .chezmoi.os "darwin" -}}
eval "$(/opt/homebrew/bin/brew shellenv)"
{{ end -}}
```

### Config Example

```toml
[data]
    name = "Your Name"
    email = "{{ if eq .chezmoi.hostname "work-laptop" }}work@company.com{{ else }}personal@email.com{{ end }}"
```

### Secret Management

```text
{{ onepasswordRead "op://vault/item/field" }}
{{ (bitwarden "item" "My SSH Key").notes }}
chezmoi add --encrypt ~/.ssh/id_rsa
{{ (keyring "service-name" "username") }}
```

### Naming Conventions

| Prefix | Meaning | Example |
|--------|---------|---------|
| `dot_` | Leading dot | `dot_zshrc` |
| `private_` | `0600` permissions | `private_dot_ssh/` |
| `executable_` | Executable file | `executable_dot_local/bin/script` |
| `modify_` | Modify existing file | `modify_dot_zshrc` |
| `create_` | Create if missing | `create_dot_gitconfig` |
| `symlink_` | Create symlink | `symlink_dot_config/nvim` |
| `.tmpl` | Template | `dot_zshrc.tmpl` |

## `yadm`

### Basic Workflow

```bash
yadm init
yadm add ~/.zshrc ~/.config/nvim/init.lua
yadm commit -m "initial dotfiles"
yadm remote add origin <repo-url>
yadm push -u origin main

yadm clone <repo-url>
```

### Alt Files

```text
~/.config/zsh/aliases.zsh##os.Darwin
~/.config/zsh/aliases.zsh##os.Linux
~/.config/zsh/aliases.zsh##h.work-laptop
~/.config/zsh/aliases.zsh##default
```

### Bootstrap Script

```bash
#!/bin/bash

if ! command -v brew &>/dev/null; then
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew bundle --file="$HOME/Brewfile"
nvim --headless "+Lazy! sync" +qa
```

## Bare Git Repository

Minimal approach when you want Git only and no templates.

### Setup

```bash
git init --bare $HOME/.dotfiles
alias dotfiles='git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
dotfiles config --local status.showUntrackedFiles no
```

### Workflow

```bash
dotfiles add ~/.zshrc
dotfiles commit -m "add zshrc"
dotfiles push

git clone --bare <repo-url> $HOME/.dotfiles
dotfiles checkout
```

Limitation: no templates, no secret management, and weak multi-machine support.

## Brewfile Management

### Structure

```ruby
tap "homebrew/bundle"
tap "homebrew/cask-fonts"

brew "git"
brew "neovim"
brew "tmux"
brew "starship"
brew "sheldon"
brew "mise"
brew "ripgrep"
brew "fd"
```

### Commands

```bash
brew bundle
brew bundle --file=~/dotfiles/Brewfile
brew bundle dump --force
brew bundle check
brew bundle cleanup
brew bundle cleanup --force
```

### Tips

- Keep `Brewfile` in the dotfiles repo.
- Prefer `brew bundle dump --describe` when you want comments.
- Split `Brewfile` and `Brewfile.work` if machines differ.
- Run `brew bundle check` in bootstrap scripts or CI.

## XDG Base Directory Specification

### Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `XDG_CONFIG_HOME` | `~/.config` | Config files |
| `XDG_DATA_HOME` | `~/.local/share` | Data files |
| `XDG_STATE_HOME` | `~/.local/state` | State and history |
| `XDG_CACHE_HOME` | `~/.cache` | Cache |
| `XDG_RUNTIME_DIR` | `/run/user/$UID` | Runtime sockets and pipes |

### Tool Support

| Tool | XDG support | Location |
|------|-------------|----------|
| `neovim` | Native | `$XDG_CONFIG_HOME/nvim/` |
| `ghostty` | Native | `$XDG_CONFIG_HOME/ghostty/` |
| `tmux` | Since `3.1` | `$XDG_CONFIG_HOME/tmux/tmux.conf` |
| `starship` | Native | `$XDG_CONFIG_HOME/starship.toml` |
| `zsh` | Manual | `ZDOTDIR=$XDG_CONFIG_HOME/zsh` |
| `bash` | No | `~/.bashrc`, `~/.bash_profile` |

### Migration Steps

```bash
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"

export ZDOTDIR="$XDG_CONFIG_HOME/zsh"
mkdir -p "$XDG_CONFIG_HOME" "$XDG_DATA_HOME" "$XDG_STATE_HOME" "$XDG_CACHE_HOME"
```

## Selection Guide

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Single machine, simple setup | `GNU Stow` | Transparent symlinks |
| Multiple machines, different configs | `chezmoi` | Templates and conditionals |
| Git power user, minimal tooling | bare Git repo | No extra dependency |
| Existing `yadm` user | `yadm` | Familiar workflow |
| Fewer than ~10 files | Manual symlinks or bare Git | Lower overhead |

### Decision Flow

```text
Need machine-specific configs?
├── Yes -> Need secrets management?
│   ├── Yes -> chezmoi
│   └── No -> chezmoi or yadm
└── No -> Need more than ~10 config files?
    ├── Yes -> GNU Stow
    └── No -> Manual symlinks or bare Git
```
