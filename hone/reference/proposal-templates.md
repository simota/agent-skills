# Proposal Templates

**Purpose:** Before/After diff format templates for configuration improvement proposals.
**Read when:** Generating proposals in the PROPOSE phase.

---

## Proposal Structure

Every proposal must include:

1. **ID**: Unique identifier (e.g., `HONE-M1-001`)
2. **Category**: Audit checklist category (Model/Trust/Features/MCP/Rules/AGENTS/Instructions)
3. **Check ID**: Related audit checklist item
4. **Priority**: P0-P3
5. **Safety**: safe / ask-first / risky
6. **Summary**: One-line description
7. **Before/After**: Diff showing the change
8. **Rationale**: Why this change is recommended (with source tier)
9. **Risk**: What could go wrong

---

## Template: Config Value Change

````markdown
### HONE-{CAT}-{NUM}: {Summary}

**Priority:** P{0-3} | **Safety:** {safe|ask-first|risky} | **Check:** {ID}

**Before:**
```toml
{current configuration}
```

**After:**
```toml
{proposed configuration}
```

**Rationale:** {Why this change is recommended} (Source: T{1-4})
**Risk:** {What could go wrong if applied}
````

---

## Template: Trust Level Change

````markdown
### HONE-T{NUM}: {Summary}

**Priority:** P{0-3} | **Safety:** ask-first | **Check:** T{1-5}

**Before:**
```toml
[project_trust]
"{path}" = "{current_level}"
```

**After:**
```toml
[project_trust]
# {path} — removed: {reason}
```

**Rationale:** {Why this change is recommended}
**Risk:** {Impact of changing trust level}
````

---

## Template: Feature Flag Change

````markdown
### HONE-F{NUM}: {Summary}

**Priority:** P{0-3} | **Safety:** ask-first | **Check:** F{1-3}

**Before:**
```toml
[features]
# {flag_name} not set (default: {default_value})
```

**After:**
```toml
[features]
{flag_name} = {proposed_value}
```

**Rationale:** {Why enable/disable this flag} (Source: T{1-4})
**Risk:** {Behavior change description}
````

---

## Template: Removal Proposal

````markdown
### HONE-{CAT}-{NUM}: Remove {item}

**Priority:** P{0-3} | **Safety:** {safe|ask-first} | **Check:** {ID}

**Before:**
```toml
{current entry}
```

**After:**
```toml
# Removed: {reason}
```

**Rationale:** {Why removal is recommended}
**Risk:** {What could break}
````

---

## Template: Addition Proposal

````markdown
### HONE-{CAT}-{NUM}: Add {item}

**Priority:** P{0-3} | **Safety:** {safe|ask-first} | **Check:** {ID}

**Before:**
```toml
# {section} — no entry for {item}
```

**After:**
```toml
{proposed addition}
```

**Rationale:** {Why this addition is recommended} (Source: T{1-4})
**Risk:** {Potential issues}
````

---

## Template: JSON Config Value Change (Gemini)

````markdown
### HONE-{CAT}-{NUM}: {Summary}

**Priority:** P{0-3} | **Safety:** {safe|ask-first|risky} | **Check:** {ID}

**Before:**
```json
{current configuration}
```

**After:**
```json
{proposed configuration}
```

**Rationale:** {Why this change is recommended} (Source: T{1-4})
**Risk:** {What could go wrong if applied}
````

---

## Template: Antigravity Safety Settings Change

````markdown
### HONE-GS{NUM}: {Summary}

**Priority:** P{0-3} | **Safety:** ask-first | **Check:** GS{1-2}

**Before:**
```json
{
  "safetySettings": [
    {
      "category": "{category}",
      "threshold": "{current_threshold}"
    }
  ]
}
```

**After:**
```json
{
  "safetySettings": [
    {
      "category": "{category}",
      "threshold": "{proposed_threshold}"
    }
  ]
}
```

**Rationale:** {Why this threshold change is recommended} (Source: T{1-4})
**Risk:** {Impact of changing safety threshold — may block legitimate content or allow harmful content}
````

---

## Proposal Report Structure

```markdown
# AI CLI Configuration Audit Report

**Date:** YYYY-MM-DD
**Target CLI:** {Codex CLI | Antigravity CLI | Claude Code | All}
**CLI version:** {version}
**Config path:** {~/.codex/ | ~/.gemini/ | both}

## Summary

| Priority | Count | Safety |
|----------|-------|--------|
| P0 (Critical) | {n} | {safe: n, ask-first: n, risky: n} |
| P1 (Recommended) | {n} | {safe: n, ask-first: n, risky: n} |
| P2 (Improvement) | {n} | {safe: n, ask-first: n, risky: n} |
| P3 (Informational) | {n} | {safe: n, ask-first: n, risky: n} |

## P0 Proposals (Critical)

{proposals ordered by priority}

## P1 Proposals (Recommended)

{proposals}

## P2 Proposals (Improvement)

{proposals}

## P3 Proposals (Informational)

{proposals}

## Sources Consulted

| Source | Tier | URL | Verified |
|--------|------|-----|----------|
| {source} | T{1-4} | {url} | {date} |
```
