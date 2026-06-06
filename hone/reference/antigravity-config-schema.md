# Gemini Config Schema

**Purpose:** Comprehensive reference for all Antigravity CLI configuration keys, default values, and recommended settings.
**Read when:** Auditing `~/.gemini/` or proposing configuration changes.

---

## Config File Location

Primary: `~/.gemini/settings.json`

---

## Core Settings

| Key | Type | Default | Description | Recommendation |
|-----|------|---------|-------------|----------------|
| `selectedModel` | string | `"gemini-2.5-pro"` | Model identifier for completions | Use latest stable model; verify availability for your API tier |
| `selectedAuthType` | string | `"oauth"` | Authentication method: `"oauth"` or `"api-key"` | OAuth for personal use; API key for CI/automation |
| `theme` | string | `"system"` | Color theme: `"system"`, `"dark"`, `"light"` | Personal preference; no security impact |

## Safety Settings

```json
{
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]
}
```

| Category | Description | Recommendation |
|----------|-------------|----------------|
| `HARM_CATEGORY_DANGEROUS_CONTENT` | Dangerous or harmful content | `BLOCK_MEDIUM_AND_ABOVE` for general use |
| `HARM_CATEGORY_HARASSMENT` | Harassment content | `BLOCK_MEDIUM_AND_ABOVE` for general use |
| `HARM_CATEGORY_HATE_SPEECH` | Hate speech content | `BLOCK_MEDIUM_AND_ABOVE` for general use |
| `HARM_CATEGORY_SEXUALLY_EXPLICIT` | Sexually explicit content | `BLOCK_MEDIUM_AND_ABOVE` for general use |

### Threshold Levels

| Threshold | Behavior | Use when |
|-----------|----------|----------|
| `BLOCK_NONE` | No blocking | Security research, specific testing (use with caution) |
| `BLOCK_LOW_AND_ABOVE` | Block low+ probability | Development with relaxed filtering |
| `BLOCK_MEDIUM_AND_ABOVE` | Block medium+ probability | General development (recommended default) |
| `BLOCK_HIGH_AND_ABOVE` | Block high probability only | Strict filtering for sensitive contexts |

### Safety Settings Audit Criteria

- **Over-permissive**: `BLOCK_NONE` on all categories without justification
- **Over-restrictive**: `BLOCK_HIGH_AND_ABOVE` on all categories blocking legitimate dev use
- **Inconsistent**: Mixed thresholds without clear rationale
- **Missing categories**: Not all harm categories configured

## Extensions

```json
{
  "extensions": [
    {
      "name": "extension-name",
      "command": "/path/to/extension",
      "args": ["--flag", "value"],
      "env": { "KEY": "value" }
    }
  ]
}
```

### Extension Audit Criteria

- **Accessibility**: Extension binary exists and is executable
- **Version**: Extension is up-to-date
- **Necessity**: Extension is actively used
- **Security**: No secrets in plaintext args/env

## GEMINI.md Instruction Files

| File | Scope | Purpose | Audit focus |
|------|-------|---------|-------------|
| `~/.gemini/GEMINI.md` | Global | Global instructions for Antigravity CLI | Non-empty, clear, up-to-date |
| `<project>/GEMINI.md` | Project | Project-level instructions | Relevant to project, no contradictions with global |

## Authentication

| Method | Configuration | Use when |
|--------|--------------|----------|
| OAuth | `selectedAuthType: "oauth"` | Personal interactive use; browser-based auth flow |
| API Key | `GEMINI_API_KEY` env var | CI/CD, automation, headless environments |

### Auth Audit Criteria

- **Configured**: At least one auth method is set up and working
- **No hardcoded keys**: `GEMINI_API_KEY` not hardcoded in config files or scripts
- **Token freshness**: OAuth tokens are valid (not expired)

> **NEVER read:** `~/.gemini/` auth tokens, OAuth session files, or cached credentials.

## CLI Flags

| Flag | Description | Recommendation |
|------|-------------|----------------|
| `-p` | Non-interactive single prompt mode | Use for scripted/automated queries |
| `--dangerously-skip-permissions` | Skip all confirmation prompts | Development only; never in production scripts |
| `--sandbox` | Run in sandboxed environment | Recommended for untrusted code execution |

### CLI Flag Audit Criteria

- **`--dangerously-skip-permissions` usage**: Flag should not appear in shared scripts or CI pipelines
- **`--sandbox` adoption**: Recommended for projects handling untrusted input

---

## Version History

| Date | Change | Source |
|------|--------|--------|
| Initial | Schema documented from Antigravity CLI v1.0 | T2: google-gemini/gemini-cli GitHub |

> This schema should be refreshed when major Antigravity CLI versions are released. Check `reference/web-sources.md` for staleness thresholds.
