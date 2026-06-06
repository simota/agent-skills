# Prompt Cache Hierarchy — Repository Standard

**Purpose:** Repository-wide convention for keeping the Anthropic prompt-cache hit rate high across skill loads, `_common/` shared context, and per-task variable input.

**Read when:** Designing a new skill, restructuring `_common/`, authoring an orchestration recipe, or auditing prompt-cache miss rate via `hone`.

**Source:** [platform.claude.com — Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), [platform.claude.com — Pricing](https://platform.claude.com/docs/en/about-claude/pricing).

---

## The hierarchy

Anthropic's prompt cache invalidates strictly top-down:

```
tools  →  system  →  messages
```

Any change at level N invalidates level N and **every level below**. A single per-request timestamp in `tools` busts the whole prefix — including all skill SKILL.md content, `_common/` shared text, and conversation history.

Cache read = **10%** of base input price (90% savings). Cache write = **1.25×** (5 min TTL) / **2×** (1 hr TTL). Break-even at **>= 1-2 hits**.

---

## Three-tier content classification

Every byte that flows into the model belongs to exactly one tier. Place it accordingly:

| Tier | Content | Layer | Volatility |
|------|---------|-------|------------|
| **T-static** | Tool definitions, skill SKILL.md, `_common/` protocols, agent persona, system instructions | `tools` + `system` (top) | Changes per release, not per request |
| **T-semi-static** | Active recipe, `_AGENT_CONTEXT` template, current Workflow phase, journal pointers | `system` (middle) | Changes per task, stable within task |
| **T-dynamic** | User input, timestamps, request IDs, `ARGUMENTS`, tool results, conversation deltas | `messages` (always) | Changes per request |

**Hard rule:** Never let T-dynamic content leak into `tools` or `system`. Never put cache breakpoints on T-dynamic content (top failure mode — see Anti-patterns).

---

## Cache breakpoint placement

Place at most 4 cache breakpoints, all on T-static content:

1. **After tool definitions** — covers tools + skill registry.
2. **After `_common/` shared protocols** — covers BOUNDARIES, HANDOFF, OPERATIONAL, OPUS_48_AUTHORING, CODEX_ORCHESTRATION, this file.
3. **After active skill SKILL.md(s)** — covers the skill's static body and any loaded reference excerpts.
4. **After recipe / handoff template** (if T-semi-static) — covers per-task template before user input.

Never place a breakpoint on:
- A line containing `Date.now()`, `new Date()`, ISO timestamps, or `__TIMESTAMP__` macros
- User input, `ARGUMENTS`, `_AGENT_CONTEXT` filled values (only the template)
- Tool call results
- Conversation history past the last static boundary

---

## Repository layout rules

The order in which Nexus (and any orchestrator) assembles context must keep T-static first:

```
[tools]                            ← T-static (skill registry, MCP tools)
[system]
  1. Agent persona / SKILL.md     ← T-static
  2. _common/ protocols loaded     ← T-static
     (BOUNDARIES → HANDOFF → OPERATIONAL → OPUS_48_AUTHORING
      → CODEX_ORCHESTRATION → PROMPT_CACHE_HIERARCHY → ...)
  3. reference/ excerpts          ← T-static (loaded on demand, stable within session)
  4. Active recipe block           ← T-semi-static (cache breakpoint here)
[messages]
  - User input                     ← T-dynamic
  - _AGENT_CONTEXT filled values   ← T-dynamic
  - Tool results                   ← T-dynamic
```

**`_common/` load order** is stable across skills — list them alphabetically or by canonical priority and never inject per-task content between them. If a recipe needs additional `_common/` text, append it to the end of the `_common/` block, not interleaved.

**`reference/` lazy load** is encouraged (progressive disclosure), but once loaded the excerpt must stay above the active recipe block — moving it bottomward on the next turn forces a full miss.

---

## Per-skill authoring requirements

Every SKILL.md should:

1. Place all volatile placeholders (`{TASK}`, `{ARGUMENTS}`, `{TIMESTAMP}`, `_AGENT_CONTEXT` filled fields) inside `messages`-equivalent sections — never in the static body.
2. Reference `_common/` files by path, not by inlined excerpt — inlining duplicates the bytes and forces them into the per-skill cache window twice.
3. Keep date-dependent claims in `reference/` with explicit revision dates, so the live SKILL.md stays stable.
4. Avoid `currentDate` / `userEmail` echoes in the static body — those values come from the harness preamble (T-dynamic).

---

## Anti-patterns (most-common cache busters)

1. **Cache breakpoint on a timestamp line** — every request bumps the prefix; cache hit rate → 0%.
2. **Per-request data in `tools` or `system`** — request ID, user ID, ARGUMENTS interpolated into the system prompt invalidates everything beneath.
3. **Reordering `_common/` loads per task** — the load order itself is part of the cached prefix; swap two files and the whole `_common/` block re-writes.
4. **Inlining `_common/` text into SKILL.md** — duplicate bytes occupy two cache slots; updating one location desyncs both.
5. **Loading reference/ on demand but appending below the recipe block** — the next turn re-orders content, invalidating cache.
6. **Recipe-specific date in the static recipe block** — move dates to `reference/` with explicit revision metadata.
7. **MCP tool list churn** — adding/removing MCP servers per task changes the `tools` layer; consolidate MCP enablement at session start.
8. **Mixing T-static and T-dynamic in a single message** — split into a cached system addendum + a fresh user/tool message.
9. **Cache write on a tiny prefix** — 5-minute TTL writes cost 1.25×; if the prefix is < ~1k tokens, the break-even (1-2 hits) may not be reached. Group small skills under one breakpoint.
10. **Forgetting the 1-hour TTL extended cache** for long sessions — pay 2× once, save 90% on every subsequent hour of work.

---

## Audit hooks for Hone

`hone` should verify (per session, not per request):

- [ ] `_common/` block load order is stable across skills (`hone cache-order`).
- [ ] No `Date.now()` / ISO timestamp / random ID inside any SKILL.md static body or `_common/*.md`.
- [ ] All `_AGENT_CONTEXT` filled values are in `messages`, not `system`.
- [ ] Each active skill has at most one cache breakpoint on its body.
- [ ] References excerpts loaded into context are appended to the static block, not interleaved.
- [ ] Tool / MCP server set is constant across the session (no per-task MCP toggle).

Report cache hit rate from prior session logs (if available) and flag any session below 70% hit rate as a P1 finding.

---

## Reference

- [Prompt Caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Pricing — cache read/write multipliers](https://platform.claude.com/docs/en/about-claude/pricing)
- `_common/OPUS_48_AUTHORING.md` — agent authoring conventions (Claude Code hub)
- `_common/CODEX_ORCHESTRATION.md` — agent authoring conventions (Codex CLI hub)
