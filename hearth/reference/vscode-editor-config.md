# VS Code / Cursor Configuration Reference

Purpose: Read this when configuring personal VS Code or Cursor — `settings.json`, `keybindings.json`, snippets, extension curation, Settings Sync, Cursor AI-specific options, and `devcontainer.json` for local reproducibility. Hearth owns **your** editor config; team-wide `.vscode/` policy and CI tooling belong elsewhere.

## Scope Boundary

- **Hearth `vscode`**: personal `settings.json` / `keybindings.json` / snippets, extension curation, Settings Sync account, Cursor AI rules, devcontainer for local reproducibility.
- **Anvil (elsewhere)**: building CLI tools or VS Code extensions for others.
- **Latch (elsewhere)**: Claude Code hook configuration (`.claude/settings.json`). Not the same file as VS Code's `settings.json` — do not conflate.
- **Gear (elsewhere)**: team CI pipelines, committed `.vscode/extensions.json` as dependency manifest, shared devcontainer for team environments.
- **Grove (elsewhere)**: repo-level `.vscode/` layout as a project-structure concern.

If the question is "how do I set this up on my machine?" → `vscode`. If it is "how should our team standardize this in-repo?" → Grove + Gear.

## Settings Scope Model

| Scope | File (macOS) | Syncs via Settings Sync? | Use for |
|-------|--------------|--------------------------|---------|
| User | `~/Library/Application Support/Code/User/settings.json` | Yes | Font, theme, editor behavior, global keybindings |
| Workspace | `<repo>/.vscode/settings.json` | No (committed to repo) | Project linter, formatter, path mappings |
| Folder | `<folder>/.vscode/settings.json` | No | Per-folder multi-root overrides |
| Profile | VS Code Profiles | Per profile | Separating Web / Data / Writing workloads |

Linux XDG: `~/.config/Code/User/settings.json`. Cursor mirrors the layout under `~/Library/Application Support/Cursor/User/` or `~/.config/Cursor/User/`. Rule: personal → User; reproducibility → Workspace and committed.

## Workflow

```
SCAN   →  detect editor (VS Code / Cursor / Insiders), OS, existing profiles,
          Settings Sync account, installed extensions (`code --list-extensions`)
PLAN   →  choose scope (User / Workspace / Profile), Sync on/off,
          extension source, Cursor AI rules layout if Cursor is primary
CRAFT  →  write settings.json / keybindings.json as JSONC, scope snippets
          (global vs language), define devcontainer if needed
APPLY  →  back up settings.json, write changes, reload window,
          export extensions list before / after for rollback
VERIFY →  JSONC parse, reload window, verify keybindings via UI,
          confirm Settings Sync status
```

## Minimal `settings.json`

```jsonc
{
  "editor.fontFamily": "JetBrainsMono Nerd Font, monospace",
  "editor.fontSize": 14,
  "editor.fontLigatures": true,
  "editor.tabSize": 2,
  "editor.formatOnSave": true,
  "editor.rulers": [80, 120],
  "editor.minimap.enabled": false,
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true,
  "terminal.integrated.fontFamily": "JetBrainsMono Nerd Font",
  "terminal.integrated.defaultProfile.osx": "zsh",
  "git.confirmSync": false,
  "git.autofetch": true
}
```

## Keybindings and Snippets

```jsonc
// keybindings.json — always check conflicts in the Keyboard Shortcuts UI
[
  { "key": "cmd+k cmd+w", "command": "workbench.action.closeAllEditors" },
  { "key": "ctrl+`", "command": "workbench.action.terminal.toggleTerminal", "when": "!terminalFocus" }
]
```

Snippet scopes: global (`snippets/global.code-snippets`), language (`snippets/typescript.json`), project (`<repo>/.vscode/<name>.code-snippets`).

## Extension Curation

| Strategy | When | How |
|----------|------|-----|
| Manual list in dotfiles | Small stable set | `code --list-extensions > ~/dotfiles/vscode-extensions.txt` |
| VS Code Profiles | Different workloads | Create profile, install subset, switch contextually |
| Settings Sync (GitHub) | Multi-machine single identity | Sign in, enable Sync selectively |
| Workspace recommendations | Team baseline | `.vscode/extensions.json` → Grove/Gear |

```bash
code --list-extensions > ~/dotfiles/vscode-extensions.txt
xargs -L1 code --install-extension < ~/dotfiles/vscode-extensions.txt
```

Cursor uses `cursor --list-extensions` — do not share the same file blindly between Cursor and VS Code.

## Settings Sync

Sign in with GitHub (preferred) or Microsoft. Sync Settings, Keybindings, Snippets, Extensions, UI State. Exclude machine-specific values:

```jsonc
{ "settingsSync.ignoredSettings": ["terminal.integrated.fontSize"] }
```

## Cursor AI-Specific Config

```jsonc
{
  "cursor.chat.defaultModel": "claude-opus-4",
  "cursor.cmdK.defaultModel": "claude-sonnet-4",
  "cursor.general.privacyMode": true
}
```

Project rules live in `<repo>/.cursor/rules/<name>.mdc` — team-shared conventions the AI follows. Personal preferences ("prefer TS over JS") stay in User settings, not project rules.

## `devcontainer.json` for Personal Reproducibility

```jsonc
{
  "name": "personal-dev",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/node:1": { "version": "20" }
  },
  "customizations": {
    "vscode": {
      "extensions": ["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"]
    }
  },
  "postCreateCommand": "npm install"
}
```

Team-shared devcontainers → Gear. Per-user local reproducibility → Hearth.

## Anti-Patterns

- Editing `settings.json` without backup — VS Code rewrites on reload and may drop a malformed file.
- Storing API keys in `settings.json` — Settings Sync uploads it to GitHub. Use env vars or OS keychain.
- Installing 100+ extensions in one profile — activation events compound. Use Profiles to split.
- Confusing `.vscode/settings.json` (VS Code) with `.claude/settings.json` (Latch). Different schemas.
- Binding over `Cmd+P` / `Cmd+Shift+P` without a clear alternative — breaks command-palette muscle memory.
- Letting Cursor AI auto-index large monorepos without privacy review — toggle `cursor.general.privacyMode` for sensitive repos.
- Committing personal Cursor rules to team repos — project rules are team-shared; personal preferences belong in User settings.

## Handoff

- Bootstrap a new machine from extension list → Hearth dotfile-manager recipe (stow / chezmoi).
- Team-shared `.vscode/extensions.json` or devcontainer → `Gear` + `Grove`.
- Claude Code hooks on VS Code tasks → `Latch`.
- Authoring a VS Code extension → `Anvil`.
