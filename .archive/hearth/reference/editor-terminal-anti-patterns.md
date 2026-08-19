# Editor and Terminal Configuration Anti-Patterns

Purpose: Read this when auditing `neovim`, `vim`, terminals, `tmux`, completion, or LSP behavior. Keep the `NV-*` and `TM-*` identifiers intact in findings and handoffs.

## Contents

- [Neovim anti-patterns](#neovim-anti-patterns)
- [Terminal anti-patterns](#terminal-anti-patterns)
- [tmux anti-patterns](#tmux-anti-patterns)
- [Completion and LSP traps](#completion-and-lsp-traps)
- [How Hearth uses this reference](#how-hearth-uses-this-reference)

## Neovim Anti-Patterns

| Code | Anti-pattern | Risk | Countermeasure |
|------|--------------|------|----------------|
| `NV-01` | Distro dependency | `NvChad`, `LunarVim`, or `SpaceVim` hides core understanding and breaks on distro changes | Start from `kickstart.nvim` or a small modular base |
| `NV-02` | Monolithic `init.lua` | A `500+` line `init.lua` hides dependencies and makes changes risky | Split into `lua/config/` and domain-specific plugin files |
| `NV-03` | Eager plugin loading | Startup goes above `300ms` and all plugins load on start | Use `event`, `cmd`, `ft`, and `keys`; reserve `VeryLazy` for UI features |
| `NV-04` | Deprecated API usage | Old Vimscript-style patterns block modern features | Use `vim.keymap.set`, `vim.hl`, native snippets, and built-in comments |
| `NV-05` | Excessive keymaps | Defaults break and the setup becomes hard to learn | Prefer `<Plug>` where available and keep leader namespaces coherent |
| `NV-06` | No health check | LSP, Treesitter, or provider issues stay hidden | Run `nvim --headless "+checkhealth" +qa` in `VERIFY` |
| `NV-07` | `setup({})` ceremony everywhere | Empty plugin setup adds noise and cost | Prefer `opts = {}` when `lazy.nvim` can call setup automatically |

## Terminal Anti-Patterns

| Pattern | Risk | Countermeasure |
|---------|------|----------------|
| TERM mismatch | `xterm-ghostty` fails on remote hosts without terminfo | `infocmp -x xterm-ghostty | ssh remote 'tic -x -'` or fallback `TERM=xterm-256color` |
| No font fallback | Nerd Font glyphs render as tofu | Add a fallback such as `"Symbols Nerd Font"` |
| Treating tabs as persistence | Local tabs disappear on restart | Use `tmux` for persistent workspace state |
| Ghostty + tmux keyboard protocol conflict | Modified keys fail to propagate | Enable extended key handling in tmux and design bindings conservatively |
| Missing shell integration | Prompt marks and command navigation do not work | Turn on shell integration explicitly when autodetect is insufficient |
| Over-configuration | Large terminal configs create compatibility and maintenance problems | Treat `100+` lines as a warning sign and keep the config minimal: font, theme, and a few keybindings |

## tmux Anti-Patterns

| Code | Anti-pattern | Risk | Countermeasure |
|------|--------------|------|----------------|
| `TM-01` | Default prefix key | `C-b` is awkward and conflicts with shell shortcuts | Move to `C-a` or `C-space` |
| `TM-02` | Zero-based indexing | Window and pane numbering is harder to reach | Set `base-index 1` and `pane-base-index 1` |
| `TM-03` | Escape delay | Vim mode switches lag because the default is `500ms` | Set `escape-time 0` |
| `TM-04` | Deprecated options | Old option names produce warnings or breakage | Use `-style` family options |
| `TM-05` | Global auto-start | Every shell is forced into tmux, including scripts | Limit auto-start to specific interactive terminals |
| `TM-06` | No session naming | Sessions become `0`, `1`, `2` with no meaning | Use descriptive names such as `tmux new -s project-name` |
| `TM-07` | TPM in the wrong place | Plugins fail to load predictably | Keep `run '~/.tmux/plugins/tpm/tpm'` at the bottom |

## Completion and LSP Traps

| Pattern | Risk | Countermeasure |
|---------|------|----------------|
| New setup starts with `nvim-cmp` | More ceremony than necessary for greenfield config | Prefer `blink.cmp` for new setups |
| Mason without locking | LSP server versions drift between machines | Use a lockfile strategy when reproducibility matters |
| Treesitter installs everything | First setup can take `5+ minutes` and pulls unused parsers | Install only active languages and enable on-demand installation |
| Native features ignored | Extra plugins duplicate Neovim 0.10+ built-ins | Audit `:help news` and remove obsolete plugins |
| No lazy-event optimization | Plugin count directly inflates startup | Prefer `VeryLazy` for UI, `BufReadPre` for file work, and `ft` for language features |

## How Hearth Uses This Reference

```text
SCAN:
  Screen for NV-01..07, terminal incompatibilities, and TM-01..07

PLAN:
  Choose the right editor and terminal scope, then decide whether restructuring is needed

CRAFT:
  Apply modular editor and tmux patterns, plus terminal compatibility fixes

VERIFY:
  Run :checkhealth, inspect startup behavior, and verify TERM / clipboard / tmux integration
```

### Required Gates

- `init.lua` over `300` lines should trigger modularization guidance.
- `init.lua` over `500` lines is an anti-pattern.
- `:Lazy profile` showing all plugins at startup should trigger event-based lazy-loading fixes.
- A missing `escape-time 0` should be reported when tmux is used with Vim or Neovim.
- `Comment.nvim` or similar should be reconsidered on Neovim 0.10+ when built-ins are sufficient.
