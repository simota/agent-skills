# Web Sources

**Purpose:** Information source tier classification, search query templates, and freshness management for Codex CLI, Antigravity CLI, and Claude Code best practices.
**Read when:** Entering the FETCH phase or when web research is required.

---

## Source Tier Classification

| Tier | Description | Trust | Examples | Usage |
|------|-------------|-------|---------|-------|
| **T1** | Official documentation | Highest | Codex CLI docs, OpenAI platform docs, Antigravity CLI docs, Google AI docs, Claude Code docs, Anthropic docs | Accept directly; cite as authoritative |
| **T2** | Official repo & maintainer | High | openai/codex GitHub, google-gemini/gemini-cli GitHub, anthropics/claude-code GitHub, OpenAI blog, Google AI blog, Anthropic blog, maintainer statements | Accept with verification; cross-reference with T1 |
| **T3** | Community knowledge | Medium | Reddit, developer blogs, X/Twitter, YouTube tutorials | Signals only; require T1/T2 corroboration |
| **T4** | Indirect/academic | Variable | AI agent papers, general CLI best practices | Theoretical grounding; never sole basis for recommendations |

### Tier Usage Rules

1. **Config change recommendations:** Require at least 1 T1 or 2 T2 sources.
2. **Feature flag guidance:** Require at least 1 T2 source.
3. **General tips:** T3 acceptable if clearly attributed.
4. **Never** recommend config changes based solely on T4 sources.

---

## Search Query Templates

### Codex CLI Official

```
"codex cli" config.toml settings
"codex cli" configuration best practices
site:github.com/openai/codex config
"codex cli" trust level configuration
"codex cli" feature flags
```

### Codex CLI Setup & Optimization

```
"codex cli" setup guide 2026
"codex cli" MCP server configuration
"codex cli" instructions.md best practices
"codex cli" AGENTS.md guide
"codex cli" rules directory setup
```

### Model & Provider Configuration

```
"codex cli" model selection
"codex cli" reasoning_effort setting
openai latest models "codex cli"
```

### Release & Changelog

```
site:github.com/openai/codex releases
"codex cli" changelog new features
"codex cli" breaking changes migration
```

### Community Practices

```
site:reddit.com "codex cli" config tips
"codex cli" workflow optimization
"codex cli" productivity setup
```

### Antigravity CLI Official

```
"Antigravity CLI" settings.json configuration
"Antigravity CLI" configuration best practices
site:github.com/google-gemini/gemini-cli config
"Antigravity CLI" safety settings configuration
"Antigravity CLI" extensions setup
```

### Antigravity CLI Setup & Optimization

```
"Antigravity CLI" setup guide 2026
"Antigravity CLI" GEMINI.md best practices
"Antigravity CLI" extension configuration
"Antigravity CLI" sandbox mode
"Antigravity CLI" yolo mode safety
```

### Antigravity Model & Auth Configuration

```
"Antigravity CLI" model selection
"Antigravity CLI" selectedModel settings
"Antigravity CLI" agy latest version
"Antigravity CLI" oauth vs api key
"GEMINI_API_KEY" best practices
```

### Antigravity Release & Changelog

```
site:github.com/google-gemini/gemini-cli releases
"Antigravity CLI" changelog new features
"Antigravity CLI" breaking changes migration
```

### Claude Code Official

```
"claude code" settings.json configuration
"claude code" CLAUDE.md best practices
site:github.com/anthropics/claude-code config
"claude code" permissions configuration
"claude code" MCP server setup
```

### Claude Code Setup & Optimization

```
"claude code" setup guide 2026
"claude code" CLAUDE.md instructions best practices
"claude code" custom commands setup
"claude code" hooks configuration
"claude code" permissions allow deny
"claude code" settings.json hidden features
"claude code" power user tips
"claude code" experimental settings
"CLAUDE_AUTOCOMPACT_PCT_OVERRIDE" context
"ENABLE_TOOL_SEARCH" MCP context tokens
"claude code" sandbox configuration
"claude code" outputStyle settings
"claude code" companyAnnouncements
"claude code" fileSuggestion command
```

### Claude Code Model & Auth Configuration

```
"claude code" model selection
"claude code" CLAUDE_MODEL settings
anthropic latest models "claude code"
"ANTHROPIC_API_KEY" best practices
"claude code" oauth login
```

### Claude Code Release & Changelog

```
site:github.com/anthropics/claude-code releases
"claude code" changelog new features
"claude code" breaking changes migration
```

---

## Freshness Management

### Staleness Thresholds

| Content type | Stale after | Action |
|--------------|-------------|--------|
| T1 sources (official docs) | 60 days | Re-verify; update citations |
| T2 sources (repo, blog) | 45 days | Re-verify; flag if outdated |
| T3 sources (community) | 30 days | Re-verify; consider removal |
| T4 sources (academic) | 180 days | Re-verify relevance |
| Config schema reference | 60 days | Refresh from latest release |
| This file (web-sources.md) | 90 days | Full refresh of query templates |

### Freshness Check Protocol

1. Record last-verified date for each source citation.
2. During FETCH phase, check all cited sources against staleness thresholds.
3. Flag stale sources for re-verification.
4. Remove sources that are no longer accessible (404, removed).
5. Update query templates if search landscape has changed.

---

## Currently Tracked Sources

### T1: Official Primary

| Source | URL pattern | Last verified | Notes |
|--------|-------------|---------------|-------|
| Codex CLI Docs | openai.com/codex | Initial | Primary reference |
| OpenAI Platform Docs | platform.openai.com | Initial | Model availability, API |

### T2: Official Secondary

| Source | URL pattern | Last verified | Notes |
|--------|-------------|---------------|-------|
| openai/codex GitHub | github.com/openai/codex | Initial | Source code, config schema, issues |
| OpenAI Blog | openai.com/blog | Initial | Feature announcements |

### T3: Community

| Source | URL pattern | Last verified | Notes |
|--------|-------------|---------------|-------|
| Reddit | reddit.com (various) | Initial | Community practices |
| Developer blogs | Various | Initial | Practitioner experiences |

### T1: Official Primary (Gemini)

| Source | URL pattern | Last verified | Notes |
|--------|-------------|---------------|-------|
| Antigravity CLI Docs | ai.google.dev/gemini-cli | Initial | Primary reference |
| Google AI Docs | ai.google.dev | Initial | Model availability, API |

### T2: Official Secondary (Gemini)

| Source | URL pattern | Last verified | Notes |
|--------|-------------|---------------|-------|
| google-gemini/gemini-cli GitHub | github.com/google-gemini/gemini-cli | Initial | Source code, config schema, issues |
| Google AI Blog | blog.google/technology/ai | Initial | Feature announcements |

### T1: Official Primary (Claude Code)

| Source | URL pattern | Last verified | Notes |
|--------|-------------|---------------|-------|
| Claude Code Docs (Settings) | code.claude.com/docs/en/settings | 2026-03-12 | Primary settings reference |
| Claude Code Docs (Security) | code.claude.com/docs/en/security | 2026-03-12 | Security guide |
| Claude Code Docs (Permissions) | code.claude.com/docs/en/permissions | 2026-03-12 | Permission patterns |
| Claude Code Docs (Sandboxing) | code.claude.com/docs/en/sandboxing | 2026-03-12 | Sandbox configuration |
| Claude Code Docs (Hooks) | code.claude.com/docs/en/hooks | 2026-03-12 | Hook events |
| Claude Code Docs (Model Config) | code.claude.com/docs/en/model-config | 2026-03-12 | Model settings |
| Claude Code Docs (StatusLine) | code.claude.com/docs/en/statusline | 2026-03-12 | Custom statusline |
| Claude Code Docs (Plugins) | code.claude.com/docs/en/plugins | 2026-03-12 | Plugin system |
| Claude Code Docs (Scheduled Tasks) | code.claude.com/docs/en/scheduled-tasks | 2026-03-12 | /loop, cron |
| Anthropic Docs | docs.anthropic.com | 2026-03-12 | Model availability, API |

### T2: Official Secondary (Claude Code)

| Source | URL pattern | Last verified | Notes |
|--------|-------------|---------------|-------|
| anthropics/claude-code GitHub | github.com/anthropics/claude-code | 2026-03-12 | Source code, config schema, issues |
| claude-code-settings-schema.json (Gist) | gist.github.com (xdannyrobertsx) | 2026-03-12 | Community schema dump |
| Anthropic Blog | anthropic.com/blog | 2026-03-12 | Feature announcements |
| managed-settings.com | managed-settings.com | 2026-03-12 | Enterprise managed settings reference |

### T3: Community (Claude Code)

| Source | URL pattern | Last verified | Notes |
|--------|-------------|---------------|-------|
| ClaudeFast Settings Reference | claudefa.st/blog/guide/settings-reference | 2026-03-12 | Comprehensive settings guide |
| ClaudeFast Context Buffer | claudefa.st/blog/guide/mechanics/context-buffer-management | 2026-03-12 | Compaction optimization |
| eesel.ai Config Guide | eesel.ai/blog/settings-json-claude-code | 2026-03-12 | Complete config walkthrough |
| DEV Community Ultimate Guide | dev.to (holasoymalva) | 2026-03-12 | Hidden tricks & hacks |
| Paddo MCP Flag Blog | paddo.dev/blog/claude-code-hidden-mcp-flag | 2026-03-12 | ENABLE_TOOL_SEARCH discovery |
| ykdojo/claude-code-tips | github.com/ykdojo/claude-code-tips | 2026-03-12 | 45 community tips |
| Korny Better Permissions | blog.korny.info | 2026-03-12 | Permission pattern best practices |
| Trail of Bits Config | github.com/trailofbits/claude-code-config | 2026-03-12 | Security-focused config |

### T4: Indirect

| Source | URL pattern | Last verified | Notes |
|--------|-------------|---------------|-------|
| CLI best practices | Various | Initial | General CLI configuration patterns |
