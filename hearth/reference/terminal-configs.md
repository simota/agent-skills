# Terminal Emulator Configuration Patterns

Purpose: Read this when configuring `ghostty`, `alacritty`, `kitty`, or `wezterm`, or when you need TERM, True Color, Nerd Font, shell-integration, or split-pane guidance.

## Contents

- [Ghostty](#ghostty)
- [Alacritty](#alacritty)
- [Kitty](#kitty)
- [WezTerm](#wezterm)
- [Cross-terminal topics](#cross-terminal-topics)
- [Ghostty 1.0 plus advanced features](#ghostty-10-plus-advanced-features)

## Ghostty

Config path: `~/.config/ghostty/config`

### Basic Configuration

```text
# Font
font-family = "JetBrains Mono"
font-size = 14
font-thicken = true
adjust-cell-height = 20%

# Theme
theme = catppuccin-mocha

# Window
window-padding-x = 8
window-padding-y = 4
window-decoration = true
macos-titlebar-style = transparent
background-opacity = 0.95

# Cursor
cursor-style = block
cursor-style-blink = false
shell-integration-features = no-cursor

# Mouse
mouse-hide-while-typing = true
copy-on-select = clipboard
```

### Keybindings

```text
keybind = super+d=new_split:right
keybind = super+shift+d=new_split:down
keybind = super+w=close_surface

keybind = super+alt+left=goto_split:left
keybind = super+alt+right=goto_split:right
keybind = super+alt+up=goto_split:top
keybind = super+alt+down=goto_split:bottom

keybind = super+t=new_tab
keybind = super+shift+left_bracket=previous_tab
keybind = super+shift+right_bracket=next_tab

keybind = super+equal=increase_font_size:1
keybind = super+minus=decrease_font_size:1
keybind = super+0=reset_font_size
```

## Alacritty

Config path: `~/.config/alacritty/alacritty.toml`

### Basic Configuration

```toml
live_config_reload = true

[env]
TERM = "xterm-256color"

[window]
padding = { x = 8, y = 4 }
decorations = "Buttonless"
opacity = 0.95
option_as_alt = "Both"

[font]
size = 14.0
normal = { family = "JetBrains Mono", style = "Regular" }
bold = { family = "JetBrains Mono", style = "Bold" }
italic = { family = "JetBrains Mono", style = "Italic" }
```

### Theme Import

```toml
import = ["~/.config/alacritty/catppuccin-mocha.toml"]
```

## Kitty

Config path: `~/.config/kitty/kitty.conf`

### Basic Configuration

```text
font_family      JetBrains Mono
bold_font        auto
italic_font      auto
bold_italic_font auto
font_size        14.0

window_padding_width 4
hide_window_decorations titlebar-only
background_opacity 0.95
macos_option_as_alt yes

cursor_shape block
cursor_blink_interval 0

copy_on_select clipboard
include themes/catppuccin-mocha.conf

map cmd+d       new_window_with_cwd
map cmd+shift+d new_window_with_cwd
map cmd+t       new_tab_with_cwd
map cmd+w       close_window
```

### Kittens

```bash
kitty +kitten icat image.png
kitty +kitten diff file1 file2
kitty +kitten ssh user@host
```

## WezTerm

Config path: `~/.config/wezterm/wezterm.lua`

### Basic Configuration

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

config.font = wezterm.font('JetBrains Mono')
config.font_size = 14.0
config.window_padding = { left = 8, right = 8, top = 4, bottom = 4 }
config.window_background_opacity = 0.95
config.color_scheme = 'Catppuccin Mocha'

config.keys = {
  { key = 'd', mods = 'CMD', action = wezterm.action.SplitHorizontal { domain = 'CurrentPaneDomain' } },
  { key = 'd', mods = 'CMD|SHIFT', action = wezterm.action.SplitVertical { domain = 'CurrentPaneDomain' } },
}

return config
```

## Cross-Terminal Topics

### True Color Support

```bash
printf "\x1b[38;2;255;100;0mTRUECOLOR\x1b[0m\n"
echo $COLORTERM
```

| Terminal | Recommended TERM |
|----------|------------------|
| `ghostty` | `xterm-ghostty` |
| `alacritty` | `xterm-256color` |
| `kitty` | `xterm-kitty` |
| `wezterm` | `xterm-256color` |
| `tmux` | `tmux-256color` |

```tmux
set -g default-terminal "tmux-256color"
set -ag terminal-overrides ",xterm-256color:RGB"
set -ag terminal-overrides ",xterm-ghostty:RGB"
```

### Nerd Font Setup

| Font | Style | Best for |
|------|-------|----------|
| JetBrains Mono | Modern, balanced | General coding |
| FiraCode | Ligatures | Symbol-heavy code |
| Hack | Clean | Terminal-heavy use |
| CascadiaCode | Cross-platform | Windows and mixed setups |

```bash
# macOS
brew install --cask font-jetbrains-mono-nerd-font

# Linux
mkdir -p ~/.local/share/fonts
cd ~/.local/share/fonts
curl -fLO "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.zip"
unzip JetBrainsMono.zip
fc-cache -fv
```

### Terminal Selection Guide

| Feature | Ghostty | Alacritty | Kitty | WezTerm |
|---------|---------|-----------|-------|---------|
| GPU rendering | Yes | Yes | Yes | Yes |
| Built-in splits | Yes | No | Yes | Yes |
| Image protocol | Kitty | No | Kitty | Kitty + iTerm2 |
| Ligatures | Yes | No | Yes | Yes |
| Resource usage | Low | Low | Medium | Medium |
| Customizability | Medium | Low | High | Very high |

## Ghostty 1.0 Plus Advanced Features

### Native Split Panes

```text
keybind = super+d=new_split:right
keybind = super+shift+d=new_split:down
keybind = super+alt+left=goto_split:left
keybind = super+alt+right=goto_split:right
keybind = super+shift+enter=toggle_split_zoom
keybind = super+shift+e=equalize_splits
```

Use native Ghostty splits for simple local workflows. Prefer `tmux` when you need session persistence, remote continuity, scripted layouts, or shared sessions.

### Theme Discovery

```bash
ghostty +list-themes
ghostty +list-themes --preview
```

### Shell Integration

```text
shell-integration = detect
shell-integration-features = no-cursor,sudo,title
```

### terminfo Handling

```bash
infocmp -x xterm-ghostty | ssh remote 'tic -x -'

# Fallback when the remote host cannot install terminfo
alias ssh='TERM=xterm-256color ssh'
```
