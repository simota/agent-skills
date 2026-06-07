# Execution Layers — Per-CLI Detail

**Purpose:** Full per-CLI prereqs, runtime notes, and silent-failure mitigations for Nexus spawn paths.

**Read when:** Authoring a spawn against Codex CLI (`spawn_agent`) or Antigravity (`agy`), or debugging a fall-back to internal execution.

**Source-of-truth for CLI compatibility:** `_common/CLI_COMPATIBILITY.md` (this file expands the Nexus-facing slice).

---

## Claude Code

| Layer | Method | When | API |
|-------|--------|------|-----|
| **L1: Direct Spawn** | Agent tool (foreground) | 1-4 step sequential chains | `Agent(prompt, mode: bypassPermissions)` |
| **L2: Parallel Spawn** | Agent tool (background) | 2-3 independent branches | `Agent(prompt, run_in_background: true)` |
| **L3: Rally Delegation** | Spawn Rally as Agent | 4+ workers, complex ownership | `Agent(prompt="You are Rally...")` |
| **L3-alt: Agent Teams** | TeammateTool (peer-to-peer) | Shared task list, independent contexts | Claude Agent SDK `team_name` parameter |

**Prereq**: fall back only if the `Agent` tool is absent from the tool list (normally always available).

---

## Codex CLI

| Layer | Method | When | API |
|-------|--------|------|-----|
| **L1: Direct Spawn** | `spawn_agent` → `wait_agent` | 1-4 step sequential chains | `spawn_agent(prompt)` → `wait_agent(id)` |
| **L2: Parallel Spawn** | Multiple `spawn_agent` → `wait_agent` all | 2-3 independent branches | `spawn_agent` × N → `wait_agent` × N |
| **L3: Rally Delegation** | `spawn_agent` with Rally prompt | 4+ workers, complex ownership | `spawn_agent(prompt="You are Rally...")` |

**Subagent Tools:** `spawn_agent`, `send_input`, `wait_agent`, `resume_agent`, `close_agent`
**Config:** `agents.max_depth` (default: 1) controls nesting. Omitted fields inherit from parent session.

**Prereqs (must hold or internal-fall-back):**
1. `codex features list | grep multi_agent` → `stable / true` (default true since v0.115+; verify in older builds).
2. `~/.codex/config.toml` has `[agents] max_depth >= 2`. Default `1` only allows the main session to spawn — a nested orchestrator (e.g. Nexus spawned from a slash command) may already be at depth 1 and unable to recurse.
3. If the model claims `spawn_agent` is missing from its tool inventory while both above are satisfied, attempt the call anyway — Codex exposes the tool lazily ("tool not visible" ≠ "tool not callable").

```toml
[agents]
max_depth = 3
```

---

## Antigravity CLI (`agy`)

| Layer | Method | When | API |
|-------|--------|------|-----|
| **L1: Direct Spawn** | `/agent <name> "<task>"` (TUI) or `agy -p "<prompt>"` (one-shot) | 1-4 step sequential chains | TUI: `/agent <slug> "<prompt>"` / Headless: `agy -p "<prompt>" --dangerously-skip-permissions` (use `@<path>` to inject file context; **deliverable captured via prompt-mandated artifact file, NOT stdout** — see "agy headless silent-failure root causes" below + `_common/CLI_COMPATIBILITY.md §9.2`) |
| **L2: Parallel Spawn** | Multiple `/agent` invocations (async, each own context) | 2-3 independent branches | Aggregate via `/tasks`; no explicit `wait` primitive |
| **L3: Role-Driven Team** | Plugin-installed team pack (`oh-my-antigravity` etc. via `agy plugin install <url>`) | 4+ workers, complex ownership | Community pattern — `/oma:taskboard` priority queue + approval gates (no Rally equivalent documented) |

**Subagent Tools:** `/agent`, `/tasks`, `/resume`, `/rewind`, `/btw` (read-only side question), `/schedule`, `/goal` (experimental flag status unverified)
**Config:** Subagent depth-cap key name **unverified** — community guidance says "cap subagent depth" but no JSON/TOML key was found in official docs. Treat as runtime/budget concern via `/usage` polling, not as a config switch.
**Skill root:** `~/.gemini/antigravity-cli/skills/` (global) or `<repo>/.agents/skills/` (workspace, preferred).
**Permission model:** `request-review` (default — pause for review) / `proceed-in-sandbox` (containerized auto) / `always-proceed` (host auto, production-forbidden) / `strict` (read-only).

**Prereqs (must hold or internal-fall-back — distinct from Codex):**
1. **`agy` binary is on PATH** — verify with `which agy && agy --version`.
2. **Main TUI session** — agy launches `/agent` only as a TUI slash command. If Nexus itself runs as a customAgent (its own `agent.json` exists under `~/.gemini/antigravity-cli/brain/<session>/.agents/agents/<name>/`), nested spawn is impossible unless `customAgent.toolNames` permits a `/agent` equivalent.
3. **Headless (`agy -p`) requires OS-level process isolation** — TUI slash commands unavailable. Substitute with `Bash("agy -p '<spawn prompt>' --dangerously-skip-permissions")` to run a separate agy process. The `--dangerously-skip-permissions` flag is **required for autonomous Nexus execution** because headless `agy -p` cannot interactively respond to `request-review` prompts and will hang or fail otherwise. Treat this flag like Claude Code's `bypassPermissions` mode — never use it in production / untrusted-workspace contexts; restrict to ephemeral sandboxes, CI runners, or explicitly-authorized dev environments.
4. **No tool named `spawn_agent` exists in agy** — the correct fallback log form is "`/agent` slash command unavailable (reason: <not in TUI main session | toolNames does not permit | headless mode without --prompt-interactive>)".

**Runtime notes**: (1) Model is switched via `/model` in TUI before spawning, not per-agent — design recipes around the active model or instruct the user to switch. (2) `/usage` does not update live — for long chains (>20 min) prefer `agy -p` one-shot triggered externally over TUI-resident `/agent` to avoid mid-run quota cliffs. (3) Permission mode defaults to `request-review`; recipes assuming autonomy must instruct the user to switch to `proceed-in-sandbox` (TUI) or pass `--dangerously-skip-permissions` (headless `agy -p`) — never use `always-proceed` or unrestricted skip in production. The headless flag is the only way to bypass the interactive review prompt that would otherwise stall a Nexus-orchestrated agy spawn. (4) `request-review` is reported as occasionally ignored for file edits — treat as runtime risk, not configuration guarantee.

**⚠ MANDATORY Pre-flight Notification**: before the first `agy -p ... --dangerously-skip-permissions` spawn of a session, Nexus MUST emit the Pre-flight Notification defined in `_common/CLI_COMPATIBILITY.md §9.1`. Rationale: spawning agy headless from Claude Code's `Bash` tool creates a two-layer autonomous loop that bypasses both sides' approval gates. The notification recommends running the `update-config` skill once to allowlist the specific Bash pattern in `settings.json permissions.allow`. The notification fires in AUTORUN / AUTORUN_FULL too (informational, not a gate). See §9.1 for canonical template.

### agy headless silent-failure root causes (v1.0.5, verified 2026-06)

The `exit 0 + empty stdout` pattern detected by `_common/MULTI_ENGINE_RECIPE.md §3.5` has five root causes, with mitigations. The first is the most consequential: **empty stdout no longer implies failure** — a successful run looks identical when stdout is piped.

| Root cause | Mechanism | Mitigation |
|------------|-----------|------------|
| **TTY requirement (silent hang from socket-stdin shells)** | agy opens `/dev/tty`; spawned from a no-controlling-terminal shell (Claude Code `Bash`, CI, cron) `agy -p` hangs to `exit 124` with empty stdout, **no artifact, and no log file**. `script -q /dev/null agy ...` also fails (`tcgetattr/ioctl: Operation not supported on socket`). Verified 2026-06-08, agy 1.0.6 | **Give agy a real pty** via `python3 -c 'import pty; pty.spawn([...])'` — the ONLY mitigation verified in that context (the `script` reattach does NOT work). Canonical block: `_common/CLI_COMPATIBILITY.md §9.2` |
| **Non-TTY stdout flush bug (affects SUCCESSFUL runs too)** | `agy -p` renders output via TUI drip (`text_drip.go`) and never flushes to a non-TTY stdout — redirection/`tee` capture nothing even when the model responded (official issue #115, OPEN; unfixed through v1.0.6) | **Never use stdout as the deliverable channel.** Mandate an absolute-path artifact write + sentinel in the prompt per `_common/CLI_COMPATIBILITY.md §9.2`; combined with the pty wrapper above, artifact verification stays mandatory |
| **File path written as plain string** | agy treats `docs/foo.md` (no `@`) as literal text; main agent delegates the read to an internal subagent | **Always use `@<path>` syntax** to inject file context directly into the main agent (e.g. `Compare @docs/a.md and @docs/b.md ...`) |
| **Internal subagent 60s timeout** | v1.0.2 changelog restricts the 60s timeout to subagents only (main agent is no longer capped); long-file reads via delegated subagents still die silently | `@` syntax avoids subagent delegation entirely; for unavoidable delegation, split prompt into multiple smaller `agy -p` calls |
| **`--print-timeout` exceeded** | Default 5min on the main agent's wait; long syntheses can hit it | Pass `--print-timeout 15m` (or appropriate) for heavy reviews |
| **Quota / OAuth expiry** | Silent runtime failure with no stderr emission | `--log-file <path>` + post-run `grep -i "quota\|auth\|expired"` per `_common/MULTI_ENGINE_RECIPE.md §3.5` |

**`--output-format json` status (re-verified 2026-06, v1.0.5)**: availability is **inconsistent across installs** — demonstrated in a community guide, but "flag not defined" errors are reported on the same guide, and no JSON schema is documented anywhere. **Do not depend on it.** Request structured JSON inside the §9.2 artifact file instead.

**Recommended headless template** (full protocol + verification chain: `_common/CLI_COMPATIBILITY.md §9.2`). **agy needs a real pty — use `python3 pty.spawn`, NOT `script -q /dev/null`** (the latter fails with `tcgetattr/ioctl: Operation not supported on socket` from Claude Code's Bash tool):
```bash
SLUG="<task-slug>"
cat > /tmp/agy-${SLUG}.prompt <<EOF
[Role and task]

Primary: @<path>
References: @<path1>, @<path2>

MANDATORY OUTPUT PROTOCOL:
- Write your COMPLETE deliverable to the absolute path /tmp/agy-${SLUG}.md (create or overwrite).
- End that file with a final line containing exactly: <<<END_OF_OUTPUT>>>
- To stdout, print only a single status line: DONE /tmp/agy-${SLUG}.md
EOF
python3 - "$SLUG" <<'PY' || true
import pty, sys
slug = sys.argv[1]
prompt = open(f"/tmp/agy-{slug}.prompt").read()
pty.spawn(["agy","-p",prompt,"--dangerously-skip-permissions",
           "--print-timeout","15m","--log-file",f"/tmp/agy-{slug}.log"])
PY
# Then run the §9.2 verification chain: [ -s /tmp/agy-${SLUG}.md ] && sentinel grep;
# fallback 1 = transcript harvest (brain/<conv-id>/.../transcript.jsonl last PLANNER_RESPONSE);
# fallback 2 = --log-file grep → RUNTIME-BROKEN. Typed retry: max 1.
```

**Cross-CLI mapping:** see `_common/CLI_COMPATIBILITY.md`.
