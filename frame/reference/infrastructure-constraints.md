# Frame Infrastructure & Constraints

Purpose: load this when Frame must connect to Figma MCP, plan rate budget, troubleshoot extraction issues, or enforce security and operational constraints.

## Contents

- [Connection Methods](#connection-methods)
- [Connection Verification](#connection-verification)
- [Rate Limits (GA — Schema 2025)](#rate-limits-ga--schema-2025)
- [Request Cost by Tool](#request-cost-by-tool)
- [Budget Planning](#budget-planning)
- [Optimization Patterns](#optimization-patterns)
- [Rate Limit Error Handling](#rate-limit-error-handling)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Monitoring Template](#monitoring-template)

## Connection Methods

### Remote MCP (API Key)

For Claude Desktop, Claude Code, or any MCP-compatible client.

**Prerequisites:** Figma Personal Access Token, Node.js 18+

```json
// Claude Desktop: ~/Library/Application Support/Claude/claude_desktop_config.json
// Claude Code: .mcp.json or settings
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-developer-mcp", "--stdio"],
      "env": {
        "FIGMA_API_KEY": "<YOUR_PERSONAL_ACCESS_TOKEN>"
      }
    }
  }
}
```

**Token Permissions Required:** File content (read) · File metadata (read) · Variables (read) · Code Connect (read/write — if managing mappings)

### Desktop Plugin (WebSocket)

For Figma Desktop app with real-time selection access.

```json
{
  "mcpServers": {
    "figma": {
      "transport": "websocket",
      "url": "ws://localhost:3845"
    }
  }
}
```

**Advantages over Remote:** Access to current selection · Real-time file state · No rate limiting on local operations · Variable resolution across files

---

## Connection Verification

Always verify in CONNECT phase:

```
# Step 1: Check MCP server availability (tools listed)
# Step 2: Verify identity and permissions
whoami()
# Step 3: Test basic operation
get_metadata(file_url="https://figma.com/file/KNOWN_FILE")
```

---

## Rate Limits (GA — Schema 2025)

| Plan | Requests/min | Limit | Concurrent | Notes |
|------|-------------|-------|------------|-------|
| **Starter** | 10 | 6/month | 1 | Extremely limited; single component only |
| **Professional** | 15 | 200/day | 3 | Batch by page, selective screenshots |
| **Organization** | 20 | 200/day | 5 | Same daily as Pro, higher burst |
| **Enterprise** | 20 | 600/day | 10 | Full file extraction feasible |

**Rate-limit-exempt tools:** `whoami`, `add_code_connect_map`, `send_code_connect_mappings`, `generate_figma_design`, `use_figma`, `search_design_system`, `create_new_file` (all write tools are rate-exempt)

**Claude Code token limit:** Responses exceeding 25,000 tokens cause errors. Set `MAX_MCP_OUTPUT_TOKENS=50000` or `100000` in environment to increase.

---

## Request Cost by Tool

| Tool | Info Density | Priority | Rate-Exempt |
|------|-------------|----------|-------------|
| `get_design_context` | **High** — full structure + styles | Extract first | No |
| `get_variable_defs` | **High** — all variables in file | Extract early | No |
| `create_design_system_rules` | **High** — system rules | On demand | No |
| `get_figjam` | **High** — full board content | On demand | No |
| `get_metadata` | **Medium** — file-level info | Once per file | No |
| `get_code_connect_map` | **Medium** — mapping data | On demand | No |
| `get_code_connect_suggestions` | **Medium** — AI suggestions | On demand | No |
| `generate_diagram` | **Medium** — generated output | On demand | No |
| `get_screenshot` | **Low** — visual only | Selective | No |
| `whoami` | **Low** — auth check | Once per session | **Yes** |
| `add_code_connect_map` | **Low** — single mapping | Per mapping | **Yes** |
| `generate_figma_design` | **Low** — generative | Ask first | **Yes** |
| `send_code_connect_mappings` | **Low** — batch send | Once per sync | **Yes** |

---

## Budget Planning

### Per-Task Budget Estimates

| Task Type | Estimated Calls | Starter | Pro (200/day) |
|-----------|----------------|---------|---------------|
| Single component analysis | 3-5 | ❌ (6/month) | ✅ |
| Page-level extraction | 10-20 | ❌ | ✅ |
| Full file extraction | 30-100+ | ❌ | ⚠️ 50% budget |
| Variable/token extraction | 2-3 | ❌ | ✅ |
| Code Connect audit | 5-10 | ❌ | ✅ |
| Design system rules | 3-5 | ❌ | ✅ |

### Budget Allocation (Enterprise 600/day)

```
Available: 540 requests (600 - 10% safety buffer)

  CONNECT phase:  2 (whoami + metadata) — whoami is exempt
  SURVEY phase:   5 (metadata + shallow scans)
  EXTRACT phase:  ~500 (bulk of budget)
  PACKAGE phase:  0 (local processing)
  DELIVER phase:  0 (local processing)
  Reserve:        33 requests (retries/follow-ups)
```

---

## Optimization Patterns

### Pattern 1: Context-First (Default)

```
1. get_design_context → 1 call, rich structural data
2. get_variable_defs (if tokens needed) → 1 call
3. get_screenshot (only for handoff) → selective calls

Avoid: Multiple get_screenshot calls when get_design_context suffices.
```

### Pattern 2: Incremental Extraction

For large files, extract page by page.

```
1. get_metadata → identify pages
2. For each page (by priority):
   a. get_design_context (depth=1) → structure overview
   b. get_design_context (specific nodes) → deep extraction
   c. get_screenshot (key frames only)
3. Budget check between each page
4. Stop if budget < 10% remaining
```

### Pattern 3: Screenshot-Minimal

For low-budget plans (Professional/Organization with 200/day).

```
1. get_design_context → structural data only
2. get_variable_defs → token data
3. Skip get_screenshot entirely
4. Provide Figma URLs for manual visual reference
```

### Pattern 4: Code Connect Focus

For Code Connect management tasks (uses exempt tools where possible).

```
1. get_code_connect_map → current mappings
2. get_code_connect_suggestions → AI recommendations
3. add_code_connect_map → per new mapping (exempt)
4. send_code_connect_mappings → batch sync
```

---

## Rate Limit Error Handling

| Scenario | Detection | Response |
|----------|-----------|----------|
| Approaching limit (>80%) | Track request count | Reduce scope, skip optional screenshots |
| 429 received | HTTP 429 response | Pause 60s, resume with reduced scope |
| Daily limit reached | Persistent 429 | Stop extraction, deliver partial results |
| Monthly limit reached (Starter) | Persistent 429 | Stop, suggest plan upgrade |

### Recovery Procedure

1. **Immediate**: Stop all pending requests
2. **Assess**: Calculate remaining budget
3. **Prioritize**: Identify minimum viable extraction
4. **Resume**: After rate window reset (60s for per-minute)
5. **Report**: Include rate usage in delivery report

---

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Tool not found" | MCP server not started | Restart server, check config |
| "401 Unauthorized" | Token expired/invalid | Regenerate Personal Access Token |
| "403 Forbidden" | Insufficient permissions | Check token scopes, file access |
| "429 Too Many Requests" | Rate limit exceeded | Wait and retry, reduce scope |
| "File not found" | Invalid URL or no access | Verify URL, check sharing |
| "Node not found" | Invalid node_id | Use metadata to discover valid IDs |
| WebSocket failed | Plugin not running | Start Figma Desktop + plugin |
| Timeout on large files | File too complex | Extract by page/section |
| Response too large | >25,000 tokens | Set `MAX_MCP_OUTPUT_TOKENS` env var |

---

## Security

- **Never** hardcode Figma API keys in committed files
- Use environment variables or secret management
- Rotate tokens periodically (quarterly recommended)
- Use minimum required token scopes
- For CI/CD: use service account tokens, not personal tokens

---

## Monitoring Template

```markdown
## Rate Usage Report

**Session**: [YYYY-MM-DD HH:MM - HH:MM]
**Plan**: [Plan type]

| Metric | Value |
|--------|-------|
| Total requests | [N] |
| Budget used | [N%] |
| Remaining (daily) | [N] |
| Peak rate | [N/min] |
| Throttle events | [N] |

### Request Breakdown
| Tool | Calls | % of Total |
|------|-------|-----------|
| get_design_context | [N] | [%] |
| get_variable_defs | [N] | [%] |
| get_screenshot | [N] | [%] |
| Other | [N] | [%] |
```
