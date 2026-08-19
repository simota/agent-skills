# Shell Configuration Patterns

Purpose: Read this when configuring `zsh`, `fish`, or `bash`, or when you need module structure, startup tuning, plugin-manager guidance, aliases, or shared shell environment rules.

## Contents

- [Zsh configuration](#zsh-configuration)
- [Fish configuration](#fish-configuration)
- [Bash configuration](#bash-configuration)
- [Cross-shell patterns](#cross-shell-patterns)

## Zsh Configuration

### Modular `.zshrc` Structure

```text
~/.config/zsh/
├── .zshrc              # Entry point — sources modules in order
├── env.zsh             # Environment variables (PATH, XDG, LANG)
├── options.zsh         # setopt / unsetopt
├── aliases.zsh         # Aliases
├── functions.zsh       # Custom functions
├── plugins.zsh         # Plugin manager config (sheldon / zinit)
├── completions.zsh     # Completion setup
├── keybindings.zsh     # bindkey settings
└── local.zsh           # Machine-specific, gitignored
```

### Entry-Point Pattern

```zsh
# XDG Base Directory
export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"
export ZDOTDIR="${XDG_CONFIG_HOME}/zsh"

# Source modules
for conf in "${ZDOTDIR}"/{env,options,aliases,functions,plugins,completions,keybindings}.zsh; do
  [[ -f "$conf" ]] && source "$conf"
done

# Machine-local overrides
[[ -f "${ZDOTDIR}/local.zsh" ]] && source "${ZDOTDIR}/local.zsh"
```

Required source order: `env -> path -> plugins -> completions -> aliases -> local`. Preserve that dependency order when splitting or merging modules.

### Startup Performance

```bash
# Wall-clock timing
time zsh -i -c exit

# Detailed profiling
zmodload zsh/zprof
# ... end of .zshrc
zprof
```

### Optimization Techniques

```zsh
# Rebuild completion dump at most once per day
autoload -Uz compinit
if [[ -n ${ZDOTDIR}/.zcompdump(#qN.mh+24) ]]; then
  compinit
else
  compinit -C
fi

# Compile zsh files for faster loading
zcompile "${ZDOTDIR}/.zshrc"

# Lazy-load nvm
lazy_nvm() {
  unset -f nvm node npm npx
  export NVM_DIR="$HOME/.nvm"
  [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
}
nvm() { lazy_nvm; nvm "$@"; }
node() { lazy_nvm; node "$@"; }
npm() { lazy_nvm; npm "$@"; }
npx() { lazy_nvm; npx "$@"; }
```

### Startup Targets

Treat these as ideal shell-only targets for a tuned shell configuration. The broader operational gate stays in `SKILL.md`.

| Profile | Target | Acceptable |
|---------|--------|-----------|
| `Minimal` | `<50ms` | `<100ms` |
| `Standard` | `<100ms` | `<200ms` |
| `Power` | `<200ms` | `<400ms` |

### Plugin Managers

| Manager | Language | Config | Lazy load | Speed |
|---------|----------|--------|-----------|-------|
| `sheldon` | Rust | TOML | Yes (`defer`) | Fast |
| `zinit` | Zsh | Zsh script | Yes (`turbo`) | Fast |
| `antidote` | Zsh | Text file | Yes | Medium |
| `oh-my-zsh` | Zsh | Zsh script | No | Slow |

```toml
# ~/.config/sheldon/plugins.toml
shell = "zsh"

[plugins.zsh-defer]
github = "romkatv/zsh-defer"

[plugins.zsh-autosuggestions]
github = "zsh-users/zsh-autosuggestions"
apply = ["defer"]

[plugins.zsh-syntax-highlighting]
github = "zsh-users/zsh-syntax-highlighting"
apply = ["defer"]
```

```zsh
# zinit turbo mode
source "${XDG_DATA_HOME}/zinit/zinit.git/zinit.zsh"

zinit ice wait lucid
zinit light zsh-users/zsh-autosuggestions

zinit ice wait lucid atinit"zicompinit; zicdreplay"
zinit light zsh-users/zsh-syntax-highlighting
```

### Essential Options

```zsh
# History
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt SHARE_HISTORY
HISTSIZE=50000
SAVEHIST=50000
HISTFILE="${XDG_DATA_HOME}/zsh/history"

# Navigation
setopt AUTO_CD
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS

# Globbing
setopt EXTENDED_GLOB
setopt GLOB_DOTS

# Correction
setopt CORRECT
```

### Alias Pattern

```zsh
# Safety aliases
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# Navigation
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# ls replacements
if command -v eza &>/dev/null; then
  alias ls='eza --icons'
  alias ll='eza -la --icons --git'
  alias lt='eza --tree --level=2 --icons'
else
  # Portable ls color: GNU uses --color=auto, BSD (macOS) uses -G
  if ls --color=auto / >/dev/null 2>&1; then
    alias ls='ls --color=auto'
  else
    alias ls='ls -G'
  fi
  alias ll='ls -lah'
fi
```

## Fish Configuration

### Structure

```text
~/.config/fish/
├── config.fish
├── fish_variables
├── conf.d/
│   ├── aliases.fish
│   └── env.fish
├── functions/
│   ├── fish_prompt.fish
│   └── mkcd.fish
└── completions/
```

### Key Differences from Zsh

- Use `set -gx` instead of `export`.
- Functions autoload from `functions/`.
- Fish already includes syntax highlighting and autosuggestions.
- Add a plugin manager only when the built-ins are insufficient.

```fish
if status is-interactive
  set -gx EDITOR nvim
  set -gx XDG_CONFIG_HOME $HOME/.config

  abbr -a g git
  abbr -a ga 'git add'
  abbr -a gc 'git commit'
end
```

## Bash Configuration

### Loading Order

```text
Login shell: /etc/profile → ~/.bash_profile → ~/.bash_login → ~/.profile
Interactive: ~/.bashrc
Logout: ~/.bash_logout
```

### Minimal `.bashrc`

```bash
[[ $- != *i* ]] && return

HISTCONTROL=ignoreboth
HISTSIZE=10000
HISTFILESIZE=20000
shopt -s histappend

shopt -s autocd cdspell dirspell

eval "$(starship init bash)"

[ -f ~/.bash_aliases ] && . ~/.bash_aliases
```

## Cross-Shell Patterns

### Shared Environment Variables

```bash
# ~/.config/shell/env
export EDITOR="nvim"
export VISUAL="nvim"
export PAGER="less"
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"

export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_CACHE_HOME="$HOME/.cache"
export XDG_STATE_HOME="$HOME/.local/state"

export PATH="$HOME/.local/bin:$PATH"
```

### Tool Version Management (`mise`)

```toml
# ~/.config/mise/config.toml
[tools]
node = "lts"
python = "3.12"
go = "latest"
```
