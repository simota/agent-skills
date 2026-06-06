# Audit Checklist

**Purpose:** Category-based audit checklist with PASS/WARN/FAIL criteria for Codex CLI, Antigravity CLI, and Claude Code configuration.
**Read when:** Running the AUDIT phase on `~/.codex/` or `~/.gemini/` configuration files.

---

## Checklist Overview

| ID | Category | Check | Priority |
|----|----------|-------|----------|
| M1 | Model | Model identifier is current and available | P0 |
| M2 | Model | `reasoning_effort` matches typical use pattern | P2 |
| M3 | Model | `verbose` is not permanently enabled | P3 |
| T1 | Trust | No stale paths (non-existent directories) | P1 |
| T2 | Trust | No over-trusted sensitive projects | P0 |
| T3 | Trust | No unnecessary untrust on personal projects | P2 |
| T4 | Trust | No overly broad wildcard patterns | P1 |
| T5 | Trust | Total trust count is manageable (< 100) | P3 |
| F1 | Features | All available flags are reviewed | P1 |
| F2 | Features | No deprecated flags present | P0 |
| F3 | Features | New stable features are enabled | P2 |
| C1 | MCP | Server binaries exist and are executable | P0 |
| C2 | MCP | No unused/orphaned server configs | P1 |
| C3 | MCP | No plaintext secrets in server config | P0 |
| C4 | MCP | Server versions are current | P2 |
| R1 | Rules | No duplicate rules across files | P1 |
| R2 | Rules | Glob patterns are valid and specific | P2 |
| R3 | Rules | No stale rules referencing removed tools/patterns | P1 |
| A1 | AGENTS.md | Instructions are clear and non-contradictory | P1 |
| A2 | AGENTS.md | Priority hierarchy is defined | P2 |
| A3 | AGENTS.md | No redundant/overlapping directives | P2 |
| I1 | Instructions | `instructions.md` exists and is non-empty | P1 |
| I2 | Instructions | Content is current and actionable | P2 |
| N1 | Notice | Migration/deprecation prompts are addressed | P1 |

---

## Judgment Criteria

### PASS
- Configuration meets the check requirement completely.
- No action needed.

### WARN
- Configuration partially meets the requirement or has minor issues.
- Improvement suggested but not urgent.
- Applies to: P2-P3 items with minor deviations.

### FAIL
- Configuration does not meet the requirement.
- Action recommended (P0-P1) or improvement needed (P2-P3).
- Applies to: Missing items, security issues, broken paths.

---

## Priority Definitions

| Priority | Label | Meaning | Action |
|----------|-------|---------|--------|
| P0 | Critical | Security risk or broken configuration | Fix immediately |
| P1 | Recommended | Functional improvement, hygiene | Fix in current session |
| P2 | Improvement | Optimization, best practice alignment | Fix when convenient |
| P3 | Informational | Minor suggestion, cosmetic | Note for future |

---

## Safety Classification

| Label | Meaning | Application |
|-------|---------|-------------|
| `safe` | Can apply without risk | Removing stale paths, adding comments |
| `ask-first` | Needs user confirmation | Changing trust levels, model, features |
| `risky` | May break workflow | Removing MCP servers, changing approval_mode |

---

## Category-Specific Audit Procedures

### Model Audit (M1-M3)

1. Read `model` value from config.toml
2. WebSearch for latest Codex CLI supported models
3. Compare and classify (PASS if current, WARN if one version behind, FAIL if deprecated)
4. Check `reasoning_effort` against user's typical task complexity
5. Verify `verbose` is not permanently enabled

### Trust Audit (T1-T5)

1. Extract all paths from `[project_trust]`
2. Check each path exists on disk (T1)
3. Flag sensitive-looking paths (auth, finance, secrets) that are trusted (T2)
4. Count total entries and flag if excessive (T5)
5. Check for wildcard patterns and assess specificity (T4)

### Feature Audit (F1-F3)

1. Extract all feature flags from config
2. WebSearch for current available flags in latest version
3. Identify missing new flags (F1), deprecated flags (F2), stable but disabled flags (F3)

### MCP Audit (C1-C4)

1. Extract MCP server configs
2. Check each binary path exists and is executable (C1)
3. Check for unused servers (C2)
4. Scan for plaintext secrets in args/env (C3)
5. Check server versions against latest (C4)

### Rules Audit (R1-R3)

1. Read all files in `~/.codex/rules/`
2. Compare rules for duplicates across files (R1)
3. Validate glob patterns (R2)
4. Check for references to removed or changed tools (R3)

### AGENTS.md Audit (A1-A3)

1. Read `~/.codex/AGENTS.md`
2. Check for clarity and contradiction (A1)
3. Verify priority hierarchy exists (A2)
4. Check for redundant directives (A3)

### Instructions Audit (I1-I2)

1. Check `~/.codex/instructions.md` exists and is non-empty (I1)
2. Review content for relevance and actionability (I2)

---

## Antigravity CLI Checklist

| ID | Category | Check | Priority |
|----|----------|-------|----------|
| GM1 | Antigravity Model | `selectedModel` is current and available | P0 |
| GM2 | Antigravity Model | Model is compatible with API tier | P1 |
| GM3 | Antigravity Model | Model supports required capabilities (code, multimodal) | P2 |
| GS1 | Antigravity Safety | Safety settings are not overly permissive | P0 |
| GS2 | Antigravity Safety | Safety settings are not overly restrictive for dev use | P2 |
| GE1 | Antigravity Extensions | Extension paths/binaries are valid | P0 |
| GE2 | Antigravity Extensions | No unused extensions detected | P1 |
| GE3 | Antigravity Extensions | No plaintext secrets in extension config | P0 |
| GE4 | Antigravity Extensions | Extension versions are current | P2 |
| GI1 | Antigravity Instructions | `GEMINI.md` exists and is non-empty | P1 |
| GI2 | Antigravity Instructions | Content is current and actionable | P2 |
| GA1 | Antigravity Auth | Authentication method is configured | P0 |
| GA2 | Antigravity Auth | `GEMINI_API_KEY` is not hardcoded in files | P0 |

---

## Gemini Category-Specific Audit Procedures

### Antigravity Model Audit (GM1-GM3)

1. Read `selectedModel` value from settings.json
2. WebSearch for latest Antigravity CLI supported models
3. Compare and classify (PASS if current, WARN if one version behind, FAIL if deprecated)
4. Check model compatibility with the user's API tier (free vs paid)
5. Verify model supports required capabilities (code generation, multimodal input)

### Antigravity Safety Audit (GS1-GS2)

1. Read `safetySettings` array from settings.json
2. Check for `BLOCK_NONE` on all categories without justification (GS1: FAIL)
3. Check for `BLOCK_HIGH_AND_ABOVE` on all categories blocking legitimate dev use (GS2: WARN)
4. Verify all harm categories are configured (missing categories inherit defaults)
5. Assess consistency of threshold levels across categories

### Antigravity Extensions Audit (GE1-GE4)

1. Extract extension configs from settings.json
2. Check each binary path exists and is executable (GE1)
3. Check for unused extensions (GE2)
4. Scan for plaintext secrets in args/env (GE3)
5. Check extension versions against latest (GE4)

### Antigravity Instructions Audit (GI1-GI2)

1. Check `~/.gemini/GEMINI.md` exists and is non-empty (GI1)
2. Check project-level `GEMINI.md` if applicable
3. Review content for relevance and actionability (GI2)
4. Check for contradictions between global and project-level instructions

### Antigravity Auth Audit (GA1-GA2)

1. Check that `selectedAuthType` is configured or `GEMINI_API_KEY` env var is set (GA1)
2. Scan project files and shell configs for hardcoded `GEMINI_API_KEY` values (GA2)
3. Never read actual auth tokens or OAuth session files

---

## Claude Code Checklist

| ID | Category | Check | Priority |
|----|----------|-------|----------|
| CCM1 | Claude Code Model | Model identifier is current and not deprecated | P0 |
| CCM2 | Claude Code Model | Model matches typical task complexity | P2 |
| CCP1 | Claude Code Permissions | No overly broad `Bash` allow in global settings | P0 |
| CCP2 | Claude Code Permissions | Destructive commands are explicitly denied | P0 |
| CCP3 | Claude Code Permissions | No redundant allow/deny rules | P1 |
| CCP4 | Claude Code Permissions | No stale tool/server references in permission rules | P1 |
| CCS1 | Claude Code MCP | Server commands exist and are executable | P0 |
| CCS2 | Claude Code MCP | No unused/orphaned server configs | P1 |
| CCS3 | Claude Code MCP | No plaintext secrets in server config (use `${env:VAR}`) | P0 |
| CCS4 | Claude Code MCP | Server packages are current | P2 |
| CCS5 | Claude Code MCP | Global vs project server placement is appropriate | P2 |
| CCI1 | Claude Code Instructions | `CLAUDE.md` exists and is non-empty | P1 |
| CCI2 | Claude Code Instructions | Content is current and actionable | P2 |
| CCI3 | Claude Code Instructions | No secrets or credentials in CLAUDE.md | P0 |
| CCI4 | Claude Code Instructions | No contradictions between global and project CLAUDE.md | P1 |
| CCK1 | Claude Code Commands | Custom command files are valid Markdown | P1 |
| CCK2 | Claude Code Commands | No hardcoded secrets in command templates | P0 |
| CCH1 | Claude Code Hooks | Hook commands are executable and paths exist | P1 |
| CCH2 | Claude Code Hooks | No plaintext secrets in hook commands | P0 |
| CCA1 | Claude Code Auth | Authentication method is configured | P0 |
| CCA2 | Claude Code Auth | `ANTHROPIC_API_KEY` is not hardcoded in settings or CLAUDE.md | P0 |
| CCE1 | Claude Code Env Tuning | `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` is set (70-80 recommended, default 95 is suboptimal) | P1 |
| CCE2 | Claude Code Env Tuning | `ENABLE_TOOL_SEARCH` is `auto:0` when MCP servers are configured (saves ~32% context) | P1 |
| CCE3 | Claude Code Env Tuning | `CLAUDE_CODE_MAX_OUTPUT_TOKENS` is reviewed (default 32K, max 64K) | P2 |
| CCE4 | Claude Code Env Tuning | `MAX_THINKING_TOKENS` is calibrated with `alwaysThinkingEnabled` | P2 |
| CCE5 | Claude Code Env Tuning | No unnecessary telemetry enabled (privacy review) | P2 |
| CCD1 | Claude Code Display | `outputStyle` is set for consistent output behavior | P3 |
| CCD2 | Claude Code Display | `attribution` is explicitly configured (not relying on deprecated `includeCoAuthoredBy`) | P2 |
| CCD3 | Claude Code Display | `cleanupPeriodDays` is explicitly set | P3 |
| CCD4 | Claude Code Display | `autoUpdatesChannel` is explicitly set (`stable` recommended) | P2 |
| CCD5 | Claude Code Display | `respectGitignore` is true | P3 |
| CCB1 | Claude Code Sandbox | Sandbox configuration reviewed for security posture | P1 |
| CCB2 | Claude Code Sandbox | `sandbox.filesystem.denyRead` blocks sensitive paths (`~/.aws/credentials`, `~/.ssh/*`) | P1 |

---

## Claude Code Category-Specific Audit Procedures

### Claude Code Model Audit (CCM1-CCM2)

1. Check for `CLAUDE_MODEL` in settings.json env block or environment
2. WebSearch for latest Claude Code supported models
3. Compare and classify (PASS if current, WARN if one version behind, FAIL if deprecated)
4. Assess model appropriateness for typical task complexity

### Claude Code Permissions Audit (CCP1-CCP4)

1. Read `permissions.allow` and `permissions.deny` from both global and project settings
2. Check for overly broad patterns like bare `Bash` in global allow (CCP1: FAIL)
3. Check for missing deny rules for destructive commands (CCP2: WARN)
4. Compare allow and deny for redundant overlaps (CCP3: WARN)
5. Check for references to tools/servers that no longer exist (CCP4: WARN)

### Claude Code MCP Audit (CCS1-CCS5)

1. Extract `mcpServers` from both global and project settings
2. Check each server command exists and is executable (CCS1)
3. Check for unused/orphaned servers (CCS2)
4. Scan for plaintext secrets — recommend `${env:VAR}` syntax (CCS3)
5. Check server package versions (CCS4)
6. Assess global vs project placement appropriateness (CCS5)

### Claude Code Instructions Audit (CCI1-CCI4)

1. Check `~/.claude/CLAUDE.md` exists and is non-empty (CCI1)
2. Check project-level `CLAUDE.md` and `.claude/CLAUDE.md` if applicable
3. Review content for relevance and actionability (CCI2)
4. Scan for API keys, tokens, or credentials in instruction files (CCI3)
5. Check for contradictions between global and project instructions (CCI4)

### Claude Code Commands Audit (CCK1-CCK2)

1. List files in `~/.claude/commands/` and `<project>/.claude/commands/`
2. Verify each is valid Markdown (CCK1)
3. Scan for hardcoded secrets in command templates (CCK2)

### Claude Code Hooks Audit (CCH1-CCH2)

1. Read hooks configuration from project settings.json
2. Check that hook commands are executable and paths exist (CCH1)
3. Scan for plaintext secrets in hook commands and environment (CCH2)
4. Note: Detailed hook design review is delegated to Latch agent

### Claude Code Auth Audit (CCA1-CCA2)

1. Check that `ANTHROPIC_API_KEY` env var is set or OAuth is configured (CCA1)
2. Scan settings.json and CLAUDE.md files for hardcoded API keys (CCA2)
3. Never read `~/.claude/credentials.json` or auth session files

### Claude Code Env Tuning Audit (CCE1-CCE5)

1. Check `env` block in settings.json for performance-critical variables
2. If MCP servers are configured, verify `ENABLE_TOOL_SEARCH` is `auto:0` for context savings (CCE2)
3. Check `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` — default 95% causes late compaction; 70-80% recommended (CCE1)
4. If `CLAUDE_CODE_MAX_OUTPUT_TOKENS` is unset, note default 32K may truncate large outputs (CCE3)
5. If `alwaysThinkingEnabled: true`, verify `MAX_THINKING_TOKENS` is calibrated for cost/quality balance (CCE4)
6. Review telemetry/privacy env vars for unnecessary data sharing (CCE5)

### Claude Code Display & Config Hygiene Audit (CCD1-CCD5)

1. Check if `outputStyle` is set for consistent output behavior (CCD1)
2. Check `attribution` uses new format (not deprecated `includeCoAuthoredBy`) (CCD2)
3. Verify `cleanupPeriodDays` is explicitly set (CCD3)
4. Verify `autoUpdatesChannel` is set, prefer `stable` for production use (CCD4)
5. Verify `respectGitignore` is true (CCD5)

### Claude Code Sandbox Audit (CCB1-CCB2)

1. Review whether sandbox settings exist and are appropriate for security posture (CCB1)
2. If sandbox enabled, check `sandbox.filesystem.denyRead` blocks sensitive paths (CCB2)
3. Check `sandbox.network.allowedDomains` is scoped appropriately
4. Note: Sandbox adoption should be gradual — recommend ask-first for initial enablement
