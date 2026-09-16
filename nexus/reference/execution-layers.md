# Execution Layers — Per-CLI Detail

Read when binding a spawn interface or diagnosing a fallback. `_common/CLI_COMPATIBILITY.md` owns current commands, model availability, flags, paths and version-specific workarounds. `reference/hub-authoring.md` owns the outcome brief.

## Claude Code

| Layer | Purpose | Preconditions |
|-------|---------|---------------|
| L1: Direct Spawn | One bounded specialist session | Advertised agent tool and allowed task effects |
| L2: Parallel Spawn | Independent branches, then join | Supported concurrency, exclusive writers, available budget |
| L3: Rally Delegation | Complex ownership/team coordination | Actual team/subagent support; justified coordination cost |

Use the runtime's actual schemas, not pseudocode copied from older documentation. Preserve inherited permissions. A worktree prevents direct write collisions but does not prove compatible APIs, schemas or aggregate constraints. Join required workers and verify the integrated revision.

## Codex CLI

### Prerequisites

Apply `_common/CODEX_ORCHESTRATION.md` C1/C5. Discover advertised tools and effective capacity/nesting limits. A lazily exposed tool requires supported discovery; a guessed `spawn_agent`/`wait_agent` call is not a capability probe.

### Execution layers

L1 is a single native subagent. L2 launches independent work before joining required results. L3 uses supported resume/team coordination when the task requires it. Tool names, parameter shapes and limits come from the active host. A shell-launched CLI is an alternative only when installed, authorized and appropriate to the ownership boundary.

### Runtime notes

Inherit the authorized model, approval and sandbox settings. Validate result status, outputs, stderr and required effects. Current structured output is preferred; historical detached-terminal defects require installed-version reproduction before imposing foreground-only execution. Never convert missing output into a clean review.

## Antigravity CLI (agy)

### Prerequisites

Apply `_common/AGY_ORCHESTRATION.md`. Verify installed CLI help, authorized account/model and the task's required capabilities. TUI commands are not automatically shell commands or tools available in a custom subagent.

### Execution layers

Use advertised native agents or the documented headless interface. Prefer structured results when available; parallelize only isolated calls within budget and join them before synthesis. Do not assume preview teamwork is needed, or enable it automatically.

### Runtime notes

`_common/CLI_COMPATIBILITY.md` §9.1–§9.2 defines permissions and result handling. Normal headless execution does **not** require permission bypass or a PTY. Capture exit status, structured result, stderr and declared artifacts. Denied required tools, timeouts and missing outputs remain incomplete even when the process exits zero.

A reproducible legacy stdout/TTY defect may justify version-scoped PTY or explicit file output. Associate fallback artifacts with the exact current run; never harvest an unrelated “latest transcript,” accept a stale file or swallow a process failure. Remove the workaround once its reproducer passes normally.

### Pre-flight Notification

Notify the user before a material new effect or cost; obtain approval where the contract requires it. Informational narration does not authorize a bypass. Never recommend global allowlisting or change user settings merely to make spawning noninteractive.

## Fallback to Internal Execution

Follow SKILL.md Core Rule #3: record the verified capability blocker and permitted alternatives already checked. Internal execution is not an independent specialist session and cannot expand Nexus's control-plane ownership or a read-only skill's boundary. Preserve frozen ACs, identify any unavailable independent verification and cap status accordingly. Do not repeatedly retry the same failed capability or install/enable a runtime without authorization.
