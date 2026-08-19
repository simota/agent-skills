# Tmux and Prompt Configuration Patterns

Purpose: Read this when configuring `tmux`, `starship`, or `powerlevel10k`, or when you need tmux/editor clipboard, True Color, TPM, or prompt-performance guidance.

## Contents

- [Tmux configuration](#tmux-configuration)
- [Starship prompt](#starship-prompt)
- [Powerlevel10k](#powerlevel10k)
- [Tmux and Neovim integration](#tmux-and-neovim-integration)

## Tmux Configuration

Config path: `~/.config/tmux/tmux.conf` or `~/.tmux.conf`

### Essential Configuration

```tmux
unbind C-b
set -g prefix C-a
bind C-a send-prefix

set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"
set -ag terminal-overrides ",xterm-ghostty:RGB"
set -g mouse on
set -g history-limit 50000
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on
set -sg escape-time 0
set -g focus-events on
set -g set-clipboard on

bind r source-file ~/.config/tmux/tmux.conf \; display "Config reloaded"
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"
bind c new-window -c "#{pane_current_path}"
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R
```

### Status Bar

```tmux
set -g status-position top
set -g status-interval 5
set -g status-style "bg=default,fg=white"
set -g status-left-length 30
set -g status-left "#[fg=blue,bold] #S "
set -g window-status-format " #I:#W "
set -g window-status-current-format "#[fg=magenta,bold] #I:#W "
set -g status-right-length 50
set -g status-right "#[fg=white] %H:%M #[fg=blue] %Y-%m-%d "
```

### TPM

```tmux
set -g @plugin 'tmux-plugins/tpm'
set -g @plugin 'tmux-plugins/tmux-sensible'
set -g @plugin 'tmux-plugins/tmux-resurrect'
set -g @plugin 'tmux-plugins/tmux-continuum'
set -g @plugin 'christoomey/vim-tmux-navigator'

set -g @resurrect-capture-pane-contents 'on'
set -g @continuum-restore 'on'

# Keep TPM at the bottom
run '~/.tmux/plugins/tpm/tpm'
```

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

### Session Management

```tmux
bind s choose-tree -sZ
bind S command-prompt -p "New session:" "new-session -s '%%'"
```

## Starship Prompt

Config path: `~/.config/starship.toml`

### Minimal Configuration

```toml
command_timeout = 500

format = """
$directory\
$git_branch\
$git_status\
$character"""

add_newline = false

[character]
success_symbol = "[❯](bold green)"
error_symbol = "[❯](bold red)"

[directory]
truncation_length = 3
truncation_symbol = "…/"
```

### Standard Configuration

```toml
command_timeout = 500

format = """
$directory\
$git_branch\
$git_status\
$nodejs\
$python\
$rust\
$golang\
$docker_context\
$line_break\
$character"""

add_newline = true

[git_status]
format = '([$all_status$ahead_behind]($style) )'
conflicted = "="
ahead = "⇡${count}"
behind = "⇣${count}"
diverged = "⇕⇡${ahead_count}⇣${behind_count}"
untracked = "?${count}"
stashed = "*${count}"
modified = "!${count}"
staged = "+${count}"
```

### Power Configuration

```toml
right_format = """$cmd_duration$time"""

[time]
disabled = false
format = "[$time]($style) "
style = "dimmed white"
time_format = "%H:%M"
```

## Powerlevel10k

Config path: `~/.p10k.zsh`

### Installation

```zsh
[plugins.powerlevel10k]
github = "romkatv/powerlevel10k"
```

```bash
p10k configure
```

### Key Settings

```zsh
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  dir
  vcs
  prompt_char
)

typeset -g POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(
  status
  command_execution_time
  background_jobs
  node_version
  python_env
)

typeset -g POWERLEVEL9K_INSTANT_PROMPT=verbose
typeset -g POWERLEVEL9K_TRANSIENT_PROMPT=always
```

## Tmux and Neovim Integration

### True Color Pass-Through

```tmux
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",*:Tc"
```

```lua
if vim.env.TMUX then
  vim.opt.termguicolors = true
end
```

### Seamless Navigation

```tmux
set -g @plugin 'christoomey/vim-tmux-navigator'
```

```lua
return {
  "christoomey/vim-tmux-navigator",
  keys = {
    { "<C-h>", "<cmd>TmuxNavigateLeft<cr>" },
    { "<C-j>", "<cmd>TmuxNavigateDown<cr>" },
    { "<C-k>", "<cmd>TmuxNavigateUp<cr>" },
    { "<C-l>", "<cmd>TmuxNavigateRight<cr>" },
  },
}
```

### Clipboard Integration

```tmux
set -g set-clipboard on
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"
```

```lua
vim.opt.clipboard = "unnamedplus"
```

### Undercurl Support

```tmux
set -as terminal-overrides ',*:Smulx=\E[4::%p1%dm'
set -as terminal-overrides ',*:Setulc=\E[58::2::%p1%{65536}%/%d::%p1%{256}%/%{255}%&%d::%p1%{255}%&%d%;m'
```
