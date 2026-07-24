# Opus 5 Authoring Protocol

> Source: Anthropic *Prompting Claude Opus 5* + *Migrating to Claude Opus 5* + *Effort* + *Models overview* (platform.claude.com, verified 2026-07-25)
> Owner: Architect (canonical doc); referenced by orchestrators, reviewers, investigators

Shared protocol that aligns generated and existing skills with Opus 5 default behaviors. Reference this file from any SKILL.md that needs Opus 5 alignment instead of duplicating the rules.

**Principle IDs `P1`–`P11` are stable and cited across the ecosystem.** Several principles inverted relative to prior Opus models — the ID is preserved, the content is not. Re-read a principle before applying it from memory.

---

## Why This Exists

Opus 5 has sharp default behaviors that skills must author for explicitly:

| Behavior | Opus 5 default |
|----------|------------------|
| Response length | **Longer than prior Opus models** — for both chat responses and files written to disk. Effort does *not* reliably shorten visible output; prompt for length |
| Effort | Default `high`; full range `low`–`max`. `low`/`medium` are genuinely strong — use them as the primary cost/latency control |
| Tool calls | Effort controls call volume (lower effort → fewer, more combined calls). For vision work, tool use beats thinking alone |
| Instruction following | Literal on *conservative reporting* instructions ("only high-severity" → reports less). But it **expands scope** on open-ended tasks, adding unrequested steps |
| Subagent spawning | **Delegates readily** — needs caps and explicit criteria, not encouragement |
| Thinking | **On by default** (adaptive). Cannot be disabled above `high` effort (400 error) |
| Self-verification | **Automatic.** Explicit "verify your work" / "double-check" instructions cause *over*-verification — remove them |
| Progress updates | Narrates readily; per-message output in agentic sessions runs long. Tune cadence explicitly |
| Correction narration | Announces corrections to its own earlier statements more than prior models |
| Code review | High precision *and* recall; accuracy holds at low effort (fast pass + thorough pass both viable) |

Apply the eleven principles below.

---

## The Eleven Principles

### P1. Front-Loaded Task Specification

State intent, constraints, acceptance criteria, and file locations on the first turn. Opus 5 performs best given the complete task specification up front and then left to run; it completes full tasks rather than leaving stubs or placeholders.

**Apply by:**
- Trigger Guidance enumerates first-turn required inputs.
- INTERACTION_TRIGGERS batch related confirmations into a single multi-question prompt.
- AUTORUN `_AGENT_CONTEXT` schemas require all decision-affecting inputs up front; ambiguity resolves to safe defaults (documented), not follow-up questions.
- Prefer long autonomous runs over turn-by-turn steering — that is the shape Opus 5 is strongest on (multi-file features, large refactors, end-to-end work).

### P2. Explicit Length Control

**Opus 5's default output runs longer than prior Opus models', in two independent channels.** Effort controls how much the model *thinks*, not how much it *says* — lowering effort does not reliably shorten the visible response. Length must be prompted.

**Apply by:**
- Reference `_common/OUTPUT_STYLE.md` from the SKILL.md `Output Contract` section — single source of truth for tiers (`S`/`M`/`L`/`XL`), banned filler, format priority.
- **Conversational channel** — a short concision instruction works: "Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested."
- **Written-deliverable channel** (reports, Markdown docs, summaries written to disk) is separate and also runs long. Add explicit calibration: "Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate."
- In a long SKILL.md, **repeat a short reminder near the end** — a single instruction at the top under-steers a long prompt.
- Output sections specify envelopes (line counts, bullet counts, table dimensions). `_STEP_COMPLETE` / `## NEXUS_HANDOFF` blocks already provide them — keep them.
- Prefer positive concision examples over negative "do not" instructions.

### P3. Explicit Tool-Use "When/Why"

Effort — not prompt wording alone — governs tool-call volume: lower effort combines operations into fewer calls and proceeds directly to action; higher effort makes more calls and explains the plan first.

**Apply by:**
- For each tool a skill expects to use, document the trigger condition (when) and value (why).
- For eager tool use: "Read all candidate files before deciding, even if confidence seems sufficient — grounding cost is low compared to wrong-decision cost." Pair with `high`/`xhigh` effort as the baseline.
- For think-first behavior: "Reason about the design before invoking tools; do not begin file reads until the section contract is decided."
- **Vision work:** performance is strongest when the model has tools to iteratively analyze, crop, and visually verify. Tool use is a more cost-effective lever than thinking alone — give visual skills tools, not longer reasoning budgets. Re-validate prompt-side vision workarounds tuned for prior models; many are no longer needed.
- **Web tooling on Opus 5 is asymmetric — but only at the API layer.** The **API server tools**: `web_search` **is** supported on Opus 5 (`web_search_20260318` / `_20260209` / `_20250305`; `$10` per 1,000 searches; citations always on). `web_fetch` is **not** — the tool is GA and un-renamed (`web_fetch_20260318` / `_20260309` / `_20260209` / `_20250910`), Opus 5 is simply absent from its supported-model list. This constrains skills that **generate Messages API code or harnesses**: get the substance from `web_search` results + citations, or route only the fetch step to a supporting model (Sonnet 5 / Fable 5) — on a Nexus chain that is a per-step `model:` override, not a redesign.
- **Do not confuse this with the CLI's own tools.** Claude Code's `WebFetch` / `WebSearch` are **harness tools executed by the CLI**, not the API server tools, so they work on an Opus 5 session regardless of the above (verified empirically 2026-07-25 on an Opus 5 session). Skills that fetch pages *through the harness* need no change.

### P4. Subagent Delegation Caps  *(inverted)*

**Opus 5 delegates to subagents more readily than prior models.** Delegation pays off on genuinely independent, sizeable tracks; it multiplies cost and time on small tasks. The authoring job is to *bound* fan-out, not to encourage it.

**Apply by:**
- State delegation criteria and a cap explicitly: "Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low."
- Prefer deterministic caps in the harness over prompt-level pleading where the platform supports them.
- **Multi-agent coordination is a strength** — writer-verifier patterns work well and agents rarely overwrite each other's work. Independent-verifier architectures (a *different* agent checks the output) remain valid; what must go is instructing an agent to spawn helpers to check *its own* work (see P9).
- Reference `_common/SUBAGENT.md` for the parallelism-layer choice (skill-internal subagents vs Agent Teams).

### P5. Thinking Is On By Default  *(inverted)*

Thinking runs **on by default** in adaptive mode; the model decides depth per step. `thinking: {type: "disabled"}` is accepted only at effort `high` or below — combining it with `xhigh`/`max` returns a **400 error**. `max_tokens` is a hard limit on thinking + response text combined.

**Apply by:**
- Do not author skills that assume thinking is off, and do not instruct the model *not* to think or reason — such rules increase internal-tag leakage.
- Steer depth at decision points rather than toggling thinking: "Think carefully and step-by-step before responding; this decision affects [downstream impact]" / "Prioritize responding quickly rather than thinking deeply."
- Control token cost with **lower effort**, not by disabling thinking. Effort is the *calibrated* lever and should be tried first; prompt wording is the fallback and is sensitive to exact phrasing.
- **Lever order for thinking frequency**, cheapest-correct first: (1) set the effort level that matches the workload's default balance; (2) add system-prompt guidance only if triggering still misses at that level ("Extended thinking adds latency and should only be used when it will meaningfully improve answer quality… When in doubt, respond directly."); (3) steer **per message** for step-by-step variation. Per-message steering is the only one of the three that is **cache-safe** — a nudge appended to the newest user turn leaves earlier breakpoints intact, where changing `effort` invalidates them. Verify any wording-based steering on real traffic (thinking-block frequency, output tokens, latency, quality) before shipping it.
- What each level does to *frequency*, not just depth: `max` always thinks · `xhigh` always thinks deeply · `high` almost always · `medium` may skip simple queries · `low` minimizes and skips simple tasks.
- **If a skill must run with thinking disabled**, two artifacts can appear: (1) a tool call written into user-facing text instead of a structured `tool_use` block — the call never runs and the leaked text persists in history (most common on search-heavy work); mitigate with "You may say a brief sentence before using a tool." (2) `<thinking>` or other internal XML tags in visible output; mitigate with the general form "Do not include internal or system XML tags in your response" — naming the tags specifically is *less* effective.
- Do not embed numeric thinking budgets — control depth via `effort` (P6).

### P6. Effort-Level Awareness

**Default effort is `high`** on the Claude API and Claude Code. Opus 5 supports all five levels, and effort was recalibrated — carried-over settings from earlier models should be re-swept on real evals, not reused.

| Effort | When skills should expect this |
|--------|-------------------------------|
| `low` | Most efficient; short, scoped, latency-sensitive tasks, and subagents. Stronger on Opus 5 than on earlier Opus models |
| `medium` | Cost-saving step-down; genuinely viable for agentic work — use liberally wherever evals show quality holds |
| `high` (default) | Complex reasoning, difficult coding, agentic tasks. Equivalent to omitting the parameter |
| `xhigh` | **Recommended starting point for coding and agentic work**, and long-horizon runs (30 min+) |
| `max` | Unconstrained token spend for the most demanding tasks; can overthink and show diminishing returns on simpler ones — flag in `description` if a skill expects `max` |

- Effort affects **all** tokens — response text, tool calls, and thinking.
- At `xhigh`/`max`, set a large `max_tokens` (start ~64k) so the model has room to think and act across tool calls and subagents.
- Effort is request-level and shapes the rendered prompt: **changing it mid-conversation invalidates prompt-cache prefixes.** Pick a level per workload and hold it constant within a cached session.
- Claude Code's `ultracode` is not an API effort level — it pairs `xhigh` with standing permission for multi-agent workflows.

### P7. Delegation-Engineer Framing

Treat the model as a capable engineer being delegated to, not a line-by-line pair programmer.

**Apply by:**
- Skills must be self-directing for the bulk of their workflow.
- Reserve user check-ins for genuine `Ask first` decisions, not micro-steps.
- Provide enough context inside the skill (or via references) that the model does not need to ask clarifying questions for documented decisions.
- Avoid micro-step instructions that prevent the model from exercising judgment; prefer phase-level contracts with verification gates.

### P8. Scope Discipline — Both Directions  *(reframed)*

Two distinct behaviors, opposite in sign:

**(a) Scope expansion (the live risk).** Opus 5 can widen a task — adding steps that weren't requested, or applying its own judgment about what the task *should* be. Narrow tasks need explicit bounds:

> "Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked."

**(b) Literal following of restrictive instructions.** Conservative reporting instructions ("only high-severity", "be conservative", "don't nitpick") are obeyed faithfully and suppress output. See P10.

**Apply by:**
- Bound narrow tasks with the scope snippet above; state explicitly what is *out* of scope.
- State scope explicitly when an instruction should apply broadly: "Apply this to **every** section/file/case, not just the first."
- For structured-extraction / pipeline skills, pin exact output schemas and field-level expectations.
- Audit SKILL.md files for restrictive phrasing that will be taken literally and cost coverage.

### P9. Delete Redundant Verification & Narration Scaffolding  *(inverted — highest-impact change)*

**Opus 5 verifies its own work and catches its own mistakes without being told to.** Explicit verification instructions — "include a final verification step for any non-trivial task", "use a subagent to verify", "double-check your answer", "re-verify before responding" — compound with the model's own behavior, causing **over-verification: wasted tokens with no quality gain.** The same applies to legacy harness scaffolding that bolts on separate self-check steps.

**Apply by:**
- Remove self-check / re-verification instructions from SKILL.md prompts and spawn templates.
- **Distinguish self-verification from independent verification.** A *different* agent verifying a producer's output (`producer ≠ verifier`, Radar-after-Builder, Judge-after-implementation) is an architectural control and stays. What to delete is an agent being told to check, re-check, or spawn helpers to check *its own* work.
- Remove forced interim-status scaffolding ("summarize progress every 3 tool calls"). If cadence matters, describe the shape you want with an example: "Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome."
- Bound correction narration, which Opus 5 does more than prior models: "Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue. For slips that change nothing for the user, make the fix and move on without noting it."

### P10. Coverage-vs-Filter for Review & Detection Skills

Opus 5 reviews code with high precision *and* recall — it finds real bugs at a high rate per pass and its extra findings are mostly real. But it follows conservative reporting instructions literally, so a harness tuned for an older model shows *lower measured recall* — a harness effect, not a capability regression. **Accuracy holds at lower effort**, which makes a cheap fast pass plus a thorough later pass a viable design.

**Apply by (reviewers/detectors — Judge, Gauge, Sentinel, Radar, Attest, Canon, Probe, Matrix, Vigil, Cull, Chain):**
- Separate *finding* from *filtering*. At the finding stage: "Report every issue you find, including uncertain and low-severity ones. Do not filter for importance or confidence here — a later stage ranks them. Tag each with confidence + estimated severity."
- Move confidence/severity filtering to a downstream verification, dedup, or ranking stage.
- If self-filtering must happen in one pass, set a **concrete** bar, not a qualitative one: "report anything that could cause incorrect behavior, a test failure, or a misleading result; omit only pure style/naming nits."
- Exploit effort-insensitivity: run the wide pass at `low`/`medium` and reserve `xhigh` for adjudication.
- Validate recall/F1 against a known eval subset after any prompt change.

### P11. Voice & Design Defaults

**(a) Prose voice.** Opus 5 trends direct and opinionated, with sparing emoji, and narrates self-corrections readily (bound it per P9). If a product voice is warmer or more conversational, state it: "Use a warm, collaborative tone. Acknowledge the user's framing before answering." Relevant to Prose, Quill, Scribe, Cue, Zine, Crest, content/marketing skills.

**(b) Office & document artifacts.** Opus 5 generates complex multi-sheet spreadsheets with non-trivial formulas and well-structured slide decks. It needs the target style or template stated — supply it rather than expecting a house default. Relevant to Stage, Morph, Scribe, Harvest.

**(c) Frontend & visual defaults.** Vision and UI/frontend visual replication are strong on Opus 5. The persistent warm-cream/serif "house style" observed on prior Opus models is **not documented for Opus 5** — treat it as unverified rather than assumed. Independent of that, the reliable steering methods are unchanged: (1) specify a concrete alternative (exact palette hexes, typography, radius, spacing); (2) have the model propose 3–4 distinct directions first, then implement the chosen one. Generic negation ("don't use cream", "make it minimal") just shifts to another fixed palette. Relevant to Vision, Muse, Palette, Flow, Forge, Artisan, Funnel, Bazaar, Vitrine, Stage, frontend skills.

---

## Platform Facts (Opus 5)

Verified against the Anthropic docs; affects harness authoring more than prompt wording.

| Fact | Value |
|------|-------|
| Model ID | `claude-opus-5` (fixed snapshot, no date suffix; alias identical) |
| Context window | **1M tokens, default and maximum** — no beta header, no long-context premium. Instruction following, tool calling, and reasoning stay consistent across the window |
| Max output | 128k tokens (300k on the Batch API with `output-300k-2026-03-24`) |
| Pricing | `$5` / MTok input, `$25` / MTok output. Batch `$2.50` / `$12.50`. Fast mode (research preview) `$10` / `$50` |
| Prompt cache minimum | **512 tokens** (down from 1,024 on prior Opus) — shorter prompts now cache |
| Tool-use system prompt | 286 tokens (`auto`/`none`) / 406 tokens (`any`/`tool`); bash tool adds 325 |
| Knowledge cutoff | May 2026 (reliable); training data through May 2026 |
| Mid-conversation system messages | Supported — `role: "system"` accepted after a user turn, preserving earlier cache hits |
| Mid-conversation tool changes | Beta `mid-conversation-tool-changes-2026-07-01` — add/remove tools without invalidating the cached prefix |
| Automatic fallbacks | Beta `server-side-fallback-2026-07-01`, `fallbacks: "default"` — cyber-category refusals route to a fallback model |
| Refusals | `stop_reason: "refusal"` with a public `stop_details.category`; no beta header, no opt-out |
| Server-side compaction | Supported (`anthropic-beta: compact-2026-01-12`; trigger default 150k input tokens, min 50k) |
| Web tooling (API server tools) | `web_search` **supported** (`web_search_20260318` latest; `$10`/1,000 searches; dynamic filtering runs inside code execution at no extra charge). `web_fetch` **not supported** — GA and un-renamed, Opus 5 just isn't in its model list; route fetch steps to Sonnet 5 / Fable 5. Does **not** affect Claude Code's own `WebFetch`/`WebSearch` harness tools |
| Task budgets | Beta `task-budgets-2026-03-13` — an **advisory** loop-wide token budget (thinking + tool calls + tool results + output) the model sees as a countdown and paces against, finishing gracefully instead of being cut off. `effort` = depth per step; `task_budget` = breadth across the loop; `max_tokens` stays the only hard cap. Min `total` **20,000**; size from the **p99** of measured per-task spend. **Not available on Claude Code / Cowork** (Messages API only) and not on Sonnet 5 |
| Thinking cost observability | `usage.output_tokens_details.thinking_tokens` — billed reasoning tokens, always ≤ `output_tokens`. **Billed thinking ≠ visible thinking** (the `display` setting changes what you see, never what you pay). Subtract to get the non-reasoning share; when streaming it appears only on the final `message_delta` |
| Tool-catalog scaling | `tool_search_tool_regex_20251119` / `_bm25_20251119` (GA) + `defer_loading` — cache-safe on-demand tool loading; `code_execution_20260120`+ enables programmatic tool calling. Contract → `oracle/reference/advanced-tool-use.md` |
| Advisor tool | Beta `advisor-tool-2026-03-01` (`advisor_20260301`) — server-side Plan-and-Execute. Opus 5 is valid as **advisor** for any executor, and as **executor** only with a Fable 5 / Mythos 5 / Opus 5 advisor |
| **Not available** | `web_fetch` API server tool; Priority Tier |

---

## Per-Role Apply Matrix

Reference this matrix to know which principles your skill must address.

| Role | Critical (◎) | Recommended (○) |
|------|---|---|
| Orchestrators (Nexus, Titan, Sherpa, Rally, Magi, Darwin, Orbit) | P4, P6, P7, P9 | P1, P8 |
| Investigators (Scout, Lens, Trail, Atlas, Triage) | P3, P8, P9 | P2, P6 |
| Reviewers/Detectors (Judge, Gauge, Sentinel, Probe, Radar, Attest, Canon, Matrix, Vigil, Cull, Chain) | P2, P9, P10 | P1, P6, P8 |
| Builders (Builder, Artisan, Forge, Anvil, Native) | P7, P8, P9 | P3, P6, P11 |
| Designers (Vision, Muse, Palette, Schema, Gateway, Flow) | P1, P11 | P3, P8 |
| Writers (Prose, Quill, Scribe, Cue, Zine, Crest) | P2, P11 | P8, P9 |
| Knowledge/Meta (Lore, Compass, Sigil, Architect) | P6, P7, P8 | P1, P2 |

(◎ = address explicitly in SKILL.md; ○ = address if relevant)

**P2 (explicit length control), P8 (scope discipline), and P9 (no redundant verification) apply to every role** — long output, scope creep, and over-verification are the three defaults that cost tokens on every workload.

---

## Validation Hooks

When validating a skill against this protocol, use the eleven checks below (mirrors Architect `validation-checklist.md` Section 7):

- R7.1 Front-loaded context capture
- R7.2 Explicit length control — both conversational and written-deliverable channels
- R7.3 Explicit tool-use rationale; no reliance on the unavailable `web_fetch` tool
- R7.4 Subagent delegation criteria + cap stated (not fan-out encouragement)
- R7.5 No assumption that thinking is off; no instruction against thinking/reasoning
- R7.6 Effort-level expectations declared against a `high` default
- R7.7 Delegation-engineer framing
- R7.8 Scope bounded explicitly; broad-application instructions state their scope
- R7.9 No self-verification / re-check / forced-progress scaffolding (independent-verifier steps exempt)
- R7.10 (reviewers/detectors) Coverage-vs-filter separation; concrete severity bar
- R7.11 (writers/designers) Voice baseline stated; design direction given as concrete specs or option-proposal

Pass criterion: skills must address all `◎` principles for their role; aim for ≥ 7/11 total.

---

## How to Reference This File

In a SKILL.md:

```markdown
- Author for Opus 5 defaults. See `_common/OPUS_5_AUTHORING.md` (apply P[X], P[Y], P[Z] for this role).
```

Avoid duplicating the principle text in individual SKILL.md files. Cite by ID (P1–P11) and let this file be the single source of truth.
