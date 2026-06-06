# Codex Config Schema

**Purpose:** Comprehensive reference for all Codex CLI configuration keys, default values, and recommended settings.
**Read when:** Auditing `~/.codex/config.toml` or proposing configuration changes.
**Last updated:** 2026-03-12 (Codex CLI v0.114.0)

---

## Config File Location

Primary: `~/.codex/config.toml`

---

## Core Settings

| Key | Type | Default | Description | Recommendation |
|-----|------|---------|-------------|----------------|
| `model` | string | `"o4-mini"` | Model identifier | Use latest stable (currently `gpt-5.4`) |
| `provider` | string | `"openai"` | API provider | Match to model availability |
| `model_reasoning_effort` | string | `"medium"` | Reasoning depth: `none`, `minimal`, `low`, `medium`, `high`, `xhigh` | `medium` for general use |
| `model_reasoning_summary` | string | `"auto"` | Reasoning summary: `auto`, `concise`, `detailed`, `none` | `concise` for transparency without verbosity |
| `model_verbosity` | string | `"medium"` | Output verbosity: `low`, `medium`, `high` | `medium` for balanced output |
| `personality` | string | `"none"` | Communication style: `none`, `friendly`, `pragmatic` | `pragmatic` for professional use |
| `hide_agent_reasoning` | boolean | `false` | Suppress reasoning events | Keep `false` for transparency |
| `show_raw_agent_reasoning` | boolean | `false` | Show raw reasoning content | Enable for debugging |

## Policy Settings

| Key | Type | Default | Description | Recommendation |
|-----|------|---------|-------------|----------------|
| `approval_policy` | string | `"on-request"` | Approval mode: `on-request`, `never`, `unless-allow-listed` | `on-request` for safety |
| `sandbox_mode` | string | `"workspace-write"` | Sandbox: `workspace-write`, `off`, `read-only` | `workspace-write` for balanced security |

## TUI Settings

```toml
[tui]
status_line = ["model-with-reasoning", "context-remaining", "current-dir"]
theme = "catppuccin-mocha"
animations = true
show_tooltips = true
alternate_screen = "auto"
notifications = true
notification_method = "auto"
```

### Status Line Items (v0.114.0 確認済み)

| アイテムID | 表示内容 | 備考 |
|-----------|---------|------|
| `model` | モデル名 | |
| `model-with-reasoning` | モデル名 + reasoning レベル | デフォルト含む |
| `model-name` | モデル名（reasoning なし） | |
| `git-branch` | Git ブランチ名 | 非同期取得 |
| `context-remaining` | コンテキスト残量 | デフォルト含む |
| `context-used` | コンテキスト使用量 | |
| `context-window-size` | コンテキストウィンドウサイズ | |
| `current-dir` | ワーキングディレクトリ | デフォルト含む |
| `project-root` | プロジェクトルート名 | |
| `fast-mode` | Fast モード状態 | |
| `session` | セッションID | |
| `version` | Codex バージョン | |

> **注意:** PR #10546 で定義されたが v0.114.0 で未実装の可能性があるID: `rate-limits`, `tokens`, `tokens-input`, `tokens-output`, `cwd`。`/statusline` コマンドで実際の有効アイテムを確認可能。

- `null` または `[]` でステータスライン非表示
- `/statusline` コマンドでインタラクティブに設定可能

### TUI Options

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `tui.status_line` | array<string> \| null | `["model-with-reasoning", "context-remaining", "current-dir"]` | ステータスラインアイテム |
| `tui.theme` | string | auto-detect | テーマ名（kebab-case）。`/theme` で選択可 |
| `tui.animations` | boolean | `true` | ウェルカム画面・スピナー等のアニメーション |
| `tui.show_tooltips` | boolean | `true` | オンボーディングツールチップ |
| `tui.alternate_screen` | string | `"auto"` | 代替スクリーンバッファ: `auto`, `always`, `never` |
| `tui.notifications` | boolean \| array | `true` | デスクトップ通知の有効化/イベントフィルタ |
| `tui.notification_method` | string | `"auto"` | 通知方式: `auto`, `osc9`, `bel` |

### Custom Themes

`$CODEX_HOME/themes/` に `.tmTheme` ファイルを配置して `/theme` で選択可能。

## Trust Levels

```toml
[projects."/path/to/project"]
trust_level = "trusted"      # full-auto allowed
```

| Level | Behavior | Use when |
|-------|----------|----------|
| `"trusted"` | Allows `full-auto` mode | Personal projects, well-tested repos |
| `"untrusted"` | Forces `suggest` mode | Third-party code, sensitive repos |

### Trust Level Audit Criteria

- **Stale paths**: Projects that no longer exist on disk
- **Over-trust**: Sensitive dirs (home, `.ssh/`, `.aws/`) marked as trusted
- **Under-trust**: Personal projects unnecessarily restricted
- **Wildcard paths**: Overly broad trust patterns
- **External volumes**: Removable/network paths that may not be mounted

## Feature Flags

```toml
[features]
unified_exec = true
shell_snapshot = true
steer = true
apps = true
personality = true
multi_agent = true
prevent_idle_sleep = true
```

> Feature flags evolve rapidly. Verify against the latest release notes.

## History

```toml
[history]
persistence = "save-all"    # "save-all", "save-none", "ask"
```

## MCP Server Configuration

```toml
[mcp_servers.server-name]
command = "/absolute/path/to/binary"
args = ["arg1", "arg2"]
env = { KEY = "value" }
```

### MCP Audit Criteria

- **Accessibility**: Server binary exists and is executable
- **Path**: Use absolute paths to avoid PATH resolution issues
- **Version**: Server is up-to-date
- **Necessity**: Server is actively used
- **Security**: No secrets in plaintext args/env

## Rules

```
# ~/.codex/rules/default.rules
prefix_rule(pattern=["git", "add"], decision="allow")
prefix_rule(pattern=["git", "commit", "-m"], decision="allow")
```

### Rules Audit Criteria

- **Overly specific**: Individual command rules that should be generalized
- **Redundant**: Rules subsumed by broader patterns
- **Missing**: Common commands that lack allow rules

## Other Configuration Files

| File | Purpose | Audit focus |
|------|---------|-------------|
| `~/.codex/instructions.md` | Global instructions | Non-empty, clear, up-to-date |
| `~/.codex/AGENTS.md` | Agent behavior definitions | Priority clarity, no redundancy |
| `~/.codex/rules/` | Rule files (glob-scoped) | No duplicates, valid patterns |
| `~/.codex/config.json` | Legacy config (pre-TOML) | Should be deleted if present |

## Other Display Settings

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `file_opener` | string | `"vscode"` | Editor for file citations: `vscode`, `vscode-insiders`, `windsurf`, `cursor`, `none` |
| `disable_paste_burst` | boolean | `false` | Disable burst-paste detection |
| `web_search` | string | — | Web search: `cached`, `always`, `never` |

## Profiles

```toml
[profiles.ci]
approval_policy = "never"
sandbox_mode = "workspace-write"

[profiles.review]
model_reasoning_effort = "high"
model_reasoning_summary = "detailed"
```

Usage: `codex --profile ci`

## Notice (Auto-managed)

```toml
[notice]
hide_xxx_migration_prompt = true

[notice.model_migrations]
"old-model" = "new-model"
```

Codex CLI が自動管理するセクション。古い移行プロンプトは手動削除しても安全。

---

## Version History

| Date | Change | Source |
|------|--------|--------|
| 2026-03-12 | Full schema update for v0.114.0: added TUI, Policy, History, Profiles, model_reasoning_summary, approval_policy, sandbox_mode | T1+T2 |
| Initial | Schema documented from Codex CLI v0.1 | T2: openai/codex GitHub |

> This schema should be refreshed when major Codex CLI versions are released.
