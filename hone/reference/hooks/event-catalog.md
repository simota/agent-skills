# Hook Event Catalog

Full event lifecycle table plus selection rules. Read when designing a hook and choosing between events, matchers, or hook types.

## Event Table

| Event | Timing | Block? | All types? | Primary use |
|-------|--------|--------|------------|-------------|
| `PreToolUse` | Before tool execution | Yes | Yes | Approval, denial, input modification, or defer to permission system |
| `PostToolUse` | After tool completion | No | No | Feedback, logging, post-action automation |
| `PostToolUseFailure` | After tool failure | No | No | Failure context injection and retry guidance |
| `UserPromptSubmit` | On user prompt submission | Yes | No | Prompt validation or context injection |
| `PermissionRequest` | When a permission dialog is about to show | Yes | Yes | Automated permission decisions (allow/deny/updatedPermissions) |
| `PermissionDenied` | When classifier denies a tool (auto mode) | No | Yes | Signal model it may retry the denied tool call |
| `Stop` | Before the main agent stops | Yes | Yes | Completion and quality gates |
| `StopFailure` | When turn ends due to API error | No | No | Error logging (rate_limit, auth, billing, server_error) |
| `SubagentStart` | When a subagent starts | No | Yes | Subagent context injection and resource limits |
| `SubagentStop` | Before a subagent stops | Yes | Yes | Subagent completion checks |
| `TaskCreated` | When a task is created | Yes | Yes | Enforce naming/description conventions |
| `TaskCompleted` | When a task is marked complete | Yes | Yes | Enforce completion criteria (tests, lint) |
| `TeammateIdle` | When a teammate is about to go idle | Yes | No | Prevent teammate from going idle prematurely |
| `SessionStart` | At session start | No | No | Context loading and environment setup via `CLAUDE_ENV_FILE` |
| `SessionEnd` | At session end | No | No | Cleanup and logging |
| `Notification` | On Claude notifications | No | No | External forwarding and audit logging |
| `InstructionsLoaded` | After CLAUDE.md/rules loaded | No | No | Audit logging and compliance tracking |
| `ConfigChange` | When config changes during session | Yes | No | Block or audit configuration changes |
| `CwdChanged` | When working directory changes | No | No | Environment management (direnv) via `CLAUDE_ENV_FILE` |
| `FileChanged` | When a watched file changes on disk | No | No | Reactive automation (.envrc, .env, lockfiles) |
| `WorktreeCreate` | When git worktree is created | Yes | No | Replace default worktree behavior, return custom path |
| `WorktreeRemove` | When git worktree is removed | No | No | Worktree cleanup automation |
| `PreCompact` | Before compaction | No | No | Pre-compaction logging and context preservation |
| `PostCompact` | After context compaction | No | No | Post-compaction logging and state verification |
| `Elicitation` | When MCP server requests user input | Yes | No | Accept/decline/cancel MCP input requests |
| `ElicitationResult` | When user responds to MCP elicitation | Yes | No | Modify/override user response before sending to MCP |

## Selection Rules

- Prefer the narrowest event that matches the workflow gap.
- "All types?" = Yes means command, prompt, http, and agent hook types are all supported. "No" means command/http only.
- Matcher semantics vary by event: `PreToolUse`/`PostToolUse`/`PermissionRequest` match tool names; `SessionStart`/`SessionEnd` match session type (`startup|resume|clear|compact`); `SubagentStart`/`SubagentStop` match agent type (`Explore|Plan|custom`); `StopFailure` matches error type (`rate_limit|authentication_failed|billing|server_error`); `ConfigChange` matches config source (`user_settings|policy_settings`); `Notification` matches notification type; `InstructionsLoaded` matches load reason (`session_start|nested_traversal|path_glob_match|include|compact`).
- Some events ignore the `matcher` field and always fire on every occurrence: `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged`. `FileChanged` uses matcher as a pipe-separated basename filter (`".env|package-lock.json"`), not a tool name pattern.
- `Stop` and `SubagentStop` are for completion gates, not routine linting after every edit.
- `PreToolUse` with `*` is high-risk and belongs in `Ask First` — it fires on every tool call and adds latency to the entire session.
- `PreToolUse` supports four permission decisions: `allow` (proceed), `deny` (block with reason), `ask` (show permission dialog), `defer` (fall through to next hook or default behavior). Use `defer` when a hook cannot determine the correct action.
- Use MCP Tools for agent actions and Hooks to audit and verify those actions — this separation is the 2026 best practice for deterministic governance.
- Limit hooks per high-frequency event (PreToolUse, PostToolUse) to ≤ 5; target ≤ 200ms per command hook. Keep total synchronous command hooks across all events under 15 — each spawns a separate process, and cumulative startup overhead degrades session responsiveness (real-world reports show 10+ synchronous hooks causing multi-second delays). Consolidate multiple checks into a single dispatcher script where feasible. SessionStart hooks should complete within 1 second.
- Prompt hooks use `$ARGUMENTS` placeholder to inject the hook's JSON input data into the prompt text — omitting it means the LLM receives no context about the tool call.
- `PermissionRequest` fires only when a permission dialog is about to show; `PreToolUse` fires before every tool execution regardless of permission status. Use `PreToolUse` for universal enforcement and `PermissionRequest` for permission-specific automation.
- `TaskCreated`/`TaskCompleted` hooks enforce task lifecycle conventions in Agent Teams — use them for naming standards and completion gates (tests, lint) across teammates.
- `Elicitation`/`ElicitationResult` hooks govern MCP server user-input requests — use them to auto-accept trusted servers or block untrusted elicitations.
