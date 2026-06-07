# Subagent Parallel Protocol

Common protocol for individual skills to spawn parallel sub-agents via the **Agent tool** (formerly Task tool, renamed in v2.1.63).
For Nexus internal parallel branches → `_common/PARALLEL.md`. For full team orchestration (4+ workers) → Rally.

---

## Scope: Three Layers of Parallelism

| Layer | Orchestrator | Workers | Use When |
|-------|-------------|---------|----------|
| **Skill-internal** (this doc) | Individual skill agent | 2-3 Task subagents | Independent subtasks within a single skill's work |
| **Nexus parallel branches** | Nexus | Agent chains per branch | AUTORUN_FULL multi-branch execution |
| **Rally team** | Rally | Multiple Claude instances | 4+ parallel workers, complex coordination |

---

## Decision: When to Spawn Subagents

### USE subagents when:
- 2-3 **independent** subtasks exist (no data dependencies)
- Multiple **perspectives/engines** improve quality (Multi-Engine Mode)
- Parallel **verification** reduces wall-clock time (test + lint + type-check)
- Different **code areas** need simultaneous investigation

### DO NOT use subagents when:
- Tasks have **sequential dependencies** (B needs A's output)
- Working on a **single file** (subagents cannot share file ownership)
- Task completes in **< 30 seconds** (spawn overhead exceeds benefit)
- **4+ workers** needed → use Rally instead
- Task requires **shared mutable state** or iterative refinement

### Decision Flow

```
Task received
  ├─ Single focus, < 30s? ──────────────────→ Do it yourself
  ├─ 2-3 independent subtasks? ─────────────→ Spawn subagents (this protocol)
  ├─ 4+ independent subtasks? ──────────────→ Delegate to Rally
  └─ Sequential chain? ────────────────────→ Do it yourself (or Nexus AUTORUN)
```

---

## Agent Tool Quick Reference

### subagent_type Selection

| Type | Model Default | Tools Available | Best For |
|------|-------------|----------------|----------|
| `Explore` | Haiku | Read-only (Glob, Grep, Read — Write/Edit denied) | Fast codebase exploration, file search |
| `Plan` | Inherits | Read-only (Write/Edit denied) | Architecture analysis, plan mode research |
| `general-purpose` | Inherits | All (including Edit, Write, Bash, MCP) | Implementation, testing, any task requiring changes |
| `Bash` | Inherits | Shell only | Terminal commands in separate context |
| `claude-code-guide` | Haiku | Read-only + WebFetch/WebSearch | Questions about Claude Code features |
| Custom (`name`) | Per definition | Per `.claude/agents/` definition | Domain-specific tasks with tailored config |

**Custom Subagent Definitions:** Markdown files placed in `.claude/agents/` (project) or `~/.claude/agents/` (user) can define your own subagent_type. Fields such as `tools`, `disallowedTools`, `model`, `permissionMode`, `skills`, `memory`, `hooks`, `maxTurns`, `effort`, and `isolation` can be pre-configured.

### model Selection

| Complexity | Model | Use When |
|-----------|-------|----------|
| Low | `haiku` | Simple searches, formatting, extraction |
| Medium | `sonnet` | Standard analysis, code review, moderate reasoning |
| High | `opus` | Complex reasoning, architecture decisions |
| — | `inherit` (default) | Use parent session's model |

Full model IDs (`claude-opus-4-6`, `claude-sonnet-4-6`, etc.) are also supported.

### Key Frontmatter Fields (Custom Subagents)

| Field | Description |
|-------|-------------|
| `maxTurns` | Maximum agentic turns (runaway prevention, cost control) |
| `effort` | Reasoning effort: `low`/`medium`/`high`/`xhigh`/`max` (Opus 4.6+; `xhigh` is the Opus 4.8 default, respected strictly) |
| `isolation` | `worktree` for git worktree isolation (prevents file conflicts during parallel work) |
| `memory` | Persistent memory: `user`/`project`/`local` (cross-session learning) |
| `skills` | Skill content to inject at startup (pre-injection of SKILL.md) |
| `hooks` | Lifecycle hooks scoped to this subagent |
| `background` | `true` to always run as background task |

### Parallel Launch

Spawn multiple subagents by issuing **multiple Agent tool calls in a single message**. The system executes them concurrently.

```
# In one message, call Agent 2-3 times:
Agent(subagent_type="Explore", prompt="Research area A...")
Agent(subagent_type="Explore", prompt="Research area B...")
Agent(subagent_type="Explore", prompt="Research area C...")
```

---

## Codex Orchestrator Parallelism

This document assumes the **Claude Code** `Agent` tool. When the **Codex CLI** drives the hub, the parallelism primitives differ — apply `_common/CODEX_ORCHESTRATION.md` instead of the Agent mechanics above:

| Concept | Claude Code (this doc) | Codex CLI hub |
|---------|------------------------|---------------|
| Spawn | `Agent(prompt, ...)` | `spawn_agent(prompt)` → `wait_agent(id)` |
| Parallel | N `Agent(... run_in_background: true)` (non-blocking) | N `spawn_agent` in one turn → `wait_agent` on **all** (hard join; no background primitive — C2) |
| Max fan-out | soft cap **3** (else Rally) | governed by `agents.max_depth` / budget (C1), not the soft 3 |
| Continue / resume | new `Agent` per step | `send_input` / `resume_agent` / `close_agent` for 4+ step chains (C6) |
| Prereq | `Agent` tool present | `[features] multi_agent = true` + `[agents] max_depth >= 2`; tool may be lazily hidden (C5) |

The patterns below (RESEARCH_FAN_OUT, MULTI_ENGINE, etc.) and their merge strategies are engine-agnostic — only the spawn/join syntax changes.

---

## Patterns

### RESEARCH_FAN_OUT

Multiple Explore agents investigate different areas in parallel.

**When:** Broad investigation across distinct code areas, documentation, or domains.

**Setup:**
- 2-3 `Explore` subagents, each with a distinct search scope
- Each agent receives: Role + Target area + Output format
- No shared files or overlapping scope

**Merge:** Union — collect all findings → deduplicate → consolidate → report.

---

### MULTI_ENGINE

Multiple AI engines independently work on the same task, leveraging diverse knowledge bases. **Default baseline: Claude + Codex (dual-engine).** agy / Antigravity is added as a third axis when AVAILABLE at PREFLIGHT — never required. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy` for tag conventions and Engine Availability Modes.

**When:** Quality-critical tasks where diverse perspectives catch blind spots (security scans, bug hunts, edge-case tests, refactoring proposals).

#### Engine Dispatch Table

| Engine | Command | Fallback (when `which` fails) |
|--------|---------|-------------------------------|
| Codex | `codex exec --full-auto -o /tmp/codex-<slug>.md` (artifact = source of truth; keep foreground — detached-TTY silent crash #19945, see `_common/CLI_COMPATIBILITY.md §9.3`) | Claude subagent (Task) |
| Antigravity | `agy -p --dangerously-skip-permissions --log-file <path> --print-timeout 15m` (use `@<path>` for file refs; **capture output via prompt-mandated artifact file, NOT stdout** — `_common/CLI_COMPATIBILITY.md §9.2`; silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §Engine Runtime Failure Detection`) | Claude subagent (Task) |
| Claude | Claude subagent (Task) | — |

#### Loose Prompt Rules

External engines (Codex, Antigravity) must receive **minimal, unbiased prompts** to maximize independent perspective:

**Pass only:**
1. **Role** — one line describing the task persona
2. **Target** — code, files, or context to analyze
3. **Output format** — expected structure of results

**Do NOT pass:** domain frameworks, category lists, methodology descriptions, checklists, or detailed procedures. Let each engine apply its own knowledge.

#### Dispatch Examples

```bash
# Codex — foreground only (#19945 detached-TTY silent crash); artifact = source of truth
codex exec --full-auto -o "/tmp/codex-<slug>.md" "$(cat /tmp/prompt.md)"
[ -s "/tmp/codex-<slug>.md" ] || echo "VERDICT: codex RUNTIME-BROKEN (empty artifact despite RC=$?)"

# Antigravity — file-handoff capture MANDATORY (stdout never flushes to non-TTY:
# issue #115, unfixed v1.0.5 — a SUCCESSFUL run also produces empty piped stdout).
# In the prompt itself:
#   1. Reference files as @<path> (e.g. @docs/spec.md) — bare path strings trigger the
#      subagent-delegate silent-timeout pattern.
#   2. End with the §9.2 MANDATORY OUTPUT PROTOCOL block: write the COMPLETE deliverable
#      to /tmp/agy-<slug>.md (ABSOLUTE path) + final line <<<END_OF_OUTPUT>>>.
# ⚠ Pre-flight Notification REQUIRED before the first headless spawn of a session —
# see _common/CLI_COMPATIBILITY.md §9.1. Recommends /update-config to allowlist
# the Bash pattern in settings.json (the spawn creates a two-layer autonomous loop).
SLUG="<task-slug>"
OUT="/tmp/agy-${SLUG}.md"; LOG="/tmp/agy-${SLUG}.log"
rm -f "$OUT"
# agy REQUIRES a TTY: from a socket-stdin shell `agy -p` hangs silently and `script -q /dev/null`
# fails ("Operation not supported on socket"). Give it a real pty via python pty.spawn (§9.2).
python3 - "$LOG" <<'PY' || true
import pty, sys
pty.spawn(["agy","-p",open("/tmp/prompt.md").read(),"--dangerously-skip-permissions",
           "--log-file",sys.argv[1],"--print-timeout","15m"])
PY
if [ -s "$OUT" ] && grep -q '<<<END_OF_OUTPUT>>>' "$OUT"; then
  echo "OK: deliverable at $OUT"
else
  # Fallback: transcript harvest (undocumented internal path — bitrot risk)
  TR="$(ls -td "$HOME/.gemini/antigravity-cli/brain"/*/ 2>/dev/null | head -1).system_generated/logs/transcript.jsonl"
  [ -f "$TR" ] && grep '"type":"PLANNER_RESPONSE"' "$TR" | grep '"status":"DONE"' | tail -1 > "${OUT}.transcript.json"
  if [ ! -s "$OUT" ] && [ ! -s "${OUT}.transcript.json" ]; then
    grep -E "RESOURCE_EXHAUSTED|Resets in|error getting token|agent executor error|unexpected end of JSON|subagent.*timeout|interaction timeout" "$LOG" | head -5
    echo "VERDICT: agy RUNTIME-BROKEN — record in rejection ledger, exclude from aggregation"
  fi
fi
# Full pattern + rationale: _common/CLI_COMPATIBILITY.md §9.2 + _common/MULTI_ENGINE_RECIPE.md §Engine Runtime Failure Detection
```

```yaml
# Claude (Agent tool)
Agent:
  subagent_type: general-purpose
  mode: dontAsk
  description: "[task description]"
  prompt: |
    [Role]. [Target]. [Output format].
```

#### Fallback Rule

When an engine is unavailable (`which` fails), its workload falls back to a Claude subagent. This ensures 3 independent analyses even when external tools are missing.

#### Merge Strategies for Multi-Engine

| Strategy | When | Process |
|----------|------|---------|
| **Union** | Findings should be comprehensive (scans, tests, investigations) | Collect all → deduplicate same-location/same-type → boost confidence for multi-engine hits → sort by severity → report |
| **Compete** | Best single output needed (refactoring, proposals) | Collect all → evaluate against criteria → select best (or combine best parts) → present with rationale |

Each skill defines its own merge details (criteria, dedup rules, output format) in its SKILL.md.

---

### INDEPENDENT_IMPL

Parallel implementation of independent files/modules.

**When:** Multiple files need changes with no shared dependencies.

**Setup:**
- Each `general-purpose` subagent owns specific files (declare ownership upfront)
- No two subagents may modify the same file

**Merge:** Concat — combine all changes (no conflicts expected).

---

### VERIFICATION_PARALLEL

Run multiple verification tasks simultaneously.

**When:** Test suite, linter, type checker, and/or security scan can all run independently.

**Setup:**
- Each subagent runs one verification tool
- Results are independent pass/fail

**Merge:** All-pass gate — all must pass for overall success. Any failure blocks.

---

### COMPETITIVE_APPROACH

Multiple subagents implement different solutions to the same problem, then the best is selected.

**When:** Design exploration, algorithm comparison, or uncertain approach.

**Setup:**
- 2-3 `general-purpose` subagents, each with a different approach/constraint
- Each works in isolation on the same problem

**Merge:** Compete — evaluate each against criteria → select winner → adopt (or combine best elements).

---

## Result Aggregation

| Strategy | Description | Use With |
|----------|-------------|----------|
| **Union** | Collect all → deduplicate → consolidate → rank | RESEARCH_FAN_OUT, MULTI_ENGINE (comprehensive) |
| **Concat** | Combine all outputs (no overlap expected) | INDEPENDENT_IMPL |
| **All-pass** | Every result must pass; any failure = overall failure | VERIFICATION_PARALLEL |
| **Compete** | Evaluate against criteria → select best | COMPETITIVE_APPROACH, MULTI_ENGINE (selective) |

---

## Error Handling

| Scenario | Action |
|----------|--------|
| **1 of 3 subagents fails** | Continue with remaining results; note reduced coverage in report |
| **All subagents fail** | Fall back to sequential single-agent execution |
| **Timeout** (subagent takes too long) | Use available results; note incomplete coverage |
| **Conflicting results** | Flag contradictions explicitly; escalate to user if safety-critical |
| **Engine unavailable** (MULTI_ENGINE) | Fallback to Claude subagent per dispatch table |

---

## Constraints

| Rule | Limit | Reason |
|------|-------|--------|
| Max parallel subagents | **3** | Beyond 3 → use Rally for proper coordination |
| File ownership | **Exclusive** | No two subagents modify the same file |
| Cost awareness | **Each subagent = separate Claude instance** | Only parallelize when benefit > overhead |
| Spawn decision | **Agent's judgment** | Unless Nexus explicitly instructs `multi-engine` |
| Nesting | **Prohibited** | Subagents cannot spawn other subagents |
| Output style | **No completion preamble** | See `_common/OUTPUT_STYLE.md §Subagent Completion Pattern` — open with the deliverable, never with "completed/finished/here is the report" |

## Subagent Output Rules

Subagents return text to the orchestrator (parent skill or user). Apply universally regardless of `subagent_type`:

- **Open with the deliverable.** No "All work is complete. Here's the summary." Begin with the first `## ` header, table, or lead finding. The completion is implicit.
- **End at the last deliverable line.** No trailing closer ("以上で完了です", "Let me know if anything else").
- **Tier the report.** Pick S/M/L/XL based on what was actually asked; don't pad to fill an L-tier report shape when M would do. See `_common/OUTPUT_STYLE.md §Output Tiers`.
- **Structure beats prose.** ≥3 distinct items → table or bullet list, not paragraph.
- **`_STEP_COMPLETE` and handoff blocks are exempt** from tier limits but must NOT be preceded by prose preamble.

When invoking a subagent via the `Agent` tool, instruct it explicitly in the prompt: *"Open with the deliverable, not with completion preamble."*

## Context Inheritance Rules

Understanding subagent context behavior is important:

| Aspect | Inherits? | Notes |
|--------|-----------|-------|
| Parent's conversation history | No | Must be passed explicitly via prompt |
| Parent's Skills | No | Must be pre-injected via the `skills` field |
| Permission settings | Yes | Inherits parent's permissions. `bypassPermissions` cannot be overridden |
| MCP servers | Partial | Must be explicitly specified via `mcpServers`. Inline definitions are subagent-only |
| CLAUDE.md | Yes (teams) | Agent Teams teammates load it normally |
| Tool access | Configurable | Can be restricted via `tools`/`disallowedTools` |
