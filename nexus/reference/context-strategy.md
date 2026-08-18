# Context Strategy Reference

**Purpose:** Guidelines for managing context windows across agent chains.
**Read when:** You need to decide how context flows between agents in a chain.
**Sibling:** `reference/adaptive-prompt-policy.md` decides *how spawn directives adapt* to project + session context; this file decides *what context flows* between agents. Used together at spawn time.

---

## Overview

Different tasks and model combinations benefit from different context management strategies. This reference defines three strategies and when to apply each.

### The principle the three strategies serve

> Find **the smallest possible set of high-signal tokens that maximize the likelihood of the desired outcome.** — Anthropic, *Effective context engineering for AI agents*

Context is a finite resource with **diminishing marginal returns**, not a bucket to fill. The mechanism is architectural: attention is n² over tokens, so every token added competes with every other for the model's attention. Degradation as context grows is **"context rot"** — and it is why a 1M-token window does not make context management obsolete. A large window raises the ceiling on what *can* be held; it does not make holding it free or harmless.

Three implications that decide between the strategies below:

- **Just-in-time beats up-front.** Prefer carrying **lightweight identifiers** — file paths, stored queries, links, `feature_id`s — and loading the content through a tool when a step actually needs it, over pre-loading everything a chain *might* need. This is progressive disclosure applied to a chain's state. The trade-off is real and must be named: runtime exploration is **slower** than reading pre-computed context, so a step whose data is stable and certainly needed can justify up-front loading. Anthropic's own guidance is **"do the simplest thing that works"** and hybrid is usually it — which is why `hybrid` is this file's default strategy.
- **Handoffs are distillations, not transcripts.** A step passes forward the decision-relevant residue, not its trace (see `_common/SUBAGENT.md` — the reference figure for a subagent's condensed return is **1,000–2,000 tokens**).
- **Compaction: maximize recall first, then precision.** When summarizing a long trace, start with a compaction prompt that captures *everything* relevant (architectural decisions, unresolved constraints, why a path was abandoned) and only then iterate to tighten it. Dropping a load-bearing detail is unrecoverable; a slightly verbose summary is not. **Tool-result clearing** is the lightweight alternative when stale tool output — not reasoning — is what is consuming the window.

### Lifetime classes (what to keep is decided before how much)

Compaction decides *how much* survives. Lifetime decides *what should have been persistent in the first place* —
and the recurring failure is treating everything loaded as one substance, so ephemeral debugging state gets
carried into a durable summary while a standing constraint gets dropped.

| Class | Examples | Correct home | Fails as |
|-------|----------|--------------|----------|
| `stable` | architecture constraints, security prohibitions, DoD | instruction file / policy — reloaded, never summarized away | quietly dropped mid-run, then violated |
| `scoped` | directory or component conventions | the scoped instruction near what it governs | applied outside its scope |
| `dynamic` | this task's issue, diff, current plan, latest failure | working context; refreshed, never retained past the task | a later task inherits a finished task's state |
| `retrieved` | API docs, external references, search results | fetched on demand with source + version recorded | goes stale silently; the copy outlives its source |
| `ephemeral` | debugging hypotheses, discarded approaches, scratch reasoning | discarded at task end | a rejected hypothesis resurfaces as an accepted fact |

**Rules.**

1. **Persistence is a decision, not a default.** Anything retained past the task carries a source, a scope, and
   what would invalidate it — otherwise it is not retained (`_common/OPERATIONAL.md` § Where a learning goes).
2. **A `stable` item is not protected by being summarized well.** It is protected by living in a file that gets
   reloaded — the Preserve Set below is the fallback for when compaction happens anyway, not the primary
   mechanism.
3. **`retrieved` never gets promoted by being restated.** Restating a fetched claim in your own words does not
   make it project truth; it only removes the version that made it checkable.
4. **Mixed classes in one artifact is the bug.** A single note holding a standing constraint *and* today's
   failing test guarantees one of them is handled wrong — either the constraint expires or the debris persists.

### The Preserve Set (what compaction may never drop)

Recall-first is the *method*; this is the *floor*. Compaction is a lossy transform, and fluent summaries hide
their losses — the characteristic damage is not lost prose but **collapsed state**:

| Before | After | What broke |
|--------|-------|-----------|
| "retry code is 409 or 429, undecided" | "retry code is 409" | An open decision became a settled one |
| "test A passed, full suite not run" | "tests passed" | Verification scope silently widened |
| "process mutex works single-process, not in prod" | "considered a mutex" | The failure *condition* — the reusable part — vanished |

Fix the fields before writing the summary:

```
goal · definition_of_done · current_phase · authoritative_sources · active_constraints
decisions · open_questions · known_failures · failed_attempts · changed_files
execution_state · verification_evidence · next_action · raw_evidence_locators
```

- **`open_questions`, `known_failures`, and `failed_attempts` are the first casualties.** Narrative summaries
  are drawn to what succeeded. Structure what has *not* succeeded, or the next session re-runs it.
- **Never promote an assumption to a fact.** "Started the test" must not compact to "tested". If a field's
  status is unknown, carry `unknown` — an honest gap is recoverable, a confident error is not.
- **A summary is an explanation; a checkpoint is a state contract.** Both may live in one document, but a
  checkpoint is only valid if a fresh session could re-derive sources, compare `HEAD` and changed files,
  confirm what was verified, recover open items, and start the next action from it alone.
- **Recursive compaction drifts.** Compacting a compaction increases distance from the evidence and hardens
  claims. Recompact from raw evidence + current sources, not from the previous summary; when that is no longer
  possible, reset instead (`reference/error-handling.md` § Reset triggers).

#### Verify the Preserve Set actually survived

The field list says what to keep. It does not prove anything was kept, and a compaction that dropped an
exception reads as clean prose. **Do not check this with semantic similarity** — similarity is dominated by
the bulk of the text and is near-blind to exactly what matters here: negations, exceptions, and limits.

Count elements by category, before and after:

| Category | Example |
|----------|---------|
| Conditions | "only when the tenant is on the legacy plan" |
| **Exceptions** | "except for refunds issued before cutover" |
| **Prohibitions** | "never retry a non-idempotent write" |
| Numeric limits | "max 3 retries", "p95 < 200ms" |

Any loss in a category is a **blocking** failure of the compaction, regardless of how high overall overlap is:

```
source:    conditions 12 · exceptions 4 · prohibitions 3 · limits 5
compacted: conditions 10 · exceptions 2 · prohibitions 3 · limits 5
→ critical_loss: exceptions (-2)   acceptable: false
```

Losing two conditions may be tolerable restatement. Losing two exceptions removes the cases the rule was
written for. Re-compact from source rather than patching the summary — a repaired summary is a compaction of
a compaction, which is the drift failure above.

---

## Strategies

### 1. `reset` — File-Based Handoff

Each agent starts with a fresh context window. All inter-agent communication happens via structured files.

| Aspect | Detail |
|--------|--------|
| **Handoff method** | File-based (`.agents/handoffs/` directory) |
| **Context window** | Fresh per agent |
| **Best for** | Long chains (5+ steps), Sonnet/Haiku agents, cost-sensitive runs |
| **Tradeoff** | Information loss at boundaries; requires disciplined handoff structure |

**Implementation:**
- Generator writes `_STEP_COMPLETE` to handoff file
- Nexus extracts key context and passes to next agent's prompt
- Previous agent's full context is not carried forward

### 2. `continuous` — In-Context Handoff

Agent results flow through the orchestrator's context window. Subsequent agents receive accumulated context.

| Aspect | Detail |
|--------|--------|
| **Handoff method** | In-context (prompt includes prior results) |
| **Context window** | Accumulates across chain |
| **Best for** | Short chains (2-3 steps), Opus agents, deep reasoning tasks |
| **Tradeoff** | Context window pressure; higher cost; risk of context anxiety |

**Implementation:**
- Nexus retains full agent outputs in its context
- Next agent's prompt includes relevant prior outputs verbatim
- Best for chains where nuance and reasoning continuity matter

### 3. `hybrid` (Default) — Mixed Strategy

Nexus maintains continuous context; spawned agents use file-based reset.

| Aspect | Detail |
|--------|--------|
| **Handoff method** | Nexus = continuous, spawned agents = reset |
| **Context window** | Nexus accumulates; agents start fresh |
| **Best for** | Standard AUTORUN_FULL execution |
| **Tradeoff** | Balanced; Nexus context may still grow large |

**Implementation:**
- Nexus tracks the full chain state in its context
- Each spawned agent receives a structured prompt with only the context it needs
- Agent outputs are summarized by Nexus before passing to the next step

---

## Strategy Selection

| Condition | Strategy | Rationale |
|-----------|----------|-----------|
| Standard AUTORUN_FULL | `hybrid` | Default; balanced context management |
| Chain length >= 5 steps | `reset` | Prevent context overflow |
| Opus agent doing deep analysis | `continuous` | Preserve reasoning chain |
| Sonnet/Haiku agents | `reset` | Better performance with focused context |
| Evaluator Loop active (evaluators) | `reset` | Evaluators need only contract + output |
| Evaluator Loop active (generator revision) | `continuous` | Generator benefits from feedback accumulation |
| Cost-sensitive execution | `reset` | Minimize token usage |

### Model-Strategy Matrix

| Agent Model | Recommended Strategy | Notes |
|-------------|---------------------|-------|
| opus | `continuous` or `hybrid` | Can handle large context effectively |
| sonnet | `hybrid` or `reset` | Balanced; reset for long chains |
| haiku | `reset` | Always reset; limited context capacity |

---

## Context Anxiety Mitigation

**Problem:** Agents with large accumulated context may exhibit "context anxiety" — spending tokens worrying about remaining task volume rather than focusing on the current step.

**Mitigations:**

1. **Step-focused prompting** — Frame each agent's prompt around its specific step only, not the full chain
   ```
   # Good: focused on current step
   Task: Implement the email-validation logic.

   # Bad: exposes full chain scope
   Task: Implement email validation. Then phone-number validation, address validation,
   the profile UI, tests, and a security scan are also needed.
   ```

2. **Context budget monitoring** — Switch from `continuous` to `reset` for remaining steps at or before session-local turn ~50, per `_common/TOKEN_ECONOMY.md` §2's measured turn-count rule (a turn count in the transcript is checkable via `token-economy.py`; a "70% of context" figure has no counting mechanism behind it and is not used)

3. **Selective context injection** — Pass only relevant prior results, not full chain history
   ```
   # Good: selective
   Result from previous step: Scout identified a token-refresh race condition at auth/refresh.ts:87.

   # Bad: full dump
   Result from previous step: [Scout's entire 2000-line output]
   ```

---

## Platform Compatibility

| Strategy Aspect | Claude Code | Codex CLI | agy |
|----------------|-------------|-----------|-----|
| `reset` handoff | Agent prompt contains summary only | `spawn_agent()` prompt contains summary only | `agy -p` prompt contains summary only + `@<path>` to the handoff file |
| `continuous` handoff | Prior Agent results in Nexus context | Prior `wait_agent()` results in orchestrator context | **Not natively available** — subagent contexts are isolated; approximate with `-c`/`--conversation <id>` resume, or pass prior artifacts by `@<path>` |
| `hybrid` default | Nexus context + Agent(fresh) | Orchestrator context + `spawn_agent(fresh)` | Hub context + fresh `agy -p` one-shot; **filesystem artifacts are the handoff bus** |
| Context budget check | Monitor via conversation length | Monitor via `agents.max_depth` and prompt size | Monitor injected size against the **~128k effective** band, not the 1M window |
| Fallback trigger | Turn ~50 (session-local), per `_common/TOKEN_ECONOMY.md` §2 — past 100 is already late | Prompt token count approaches model limit | Handoff approaching ~128k → summarize/segment before the next spawn |

**Codex-specific notes:**
- `agents.max_depth` (default: 1) limits nesting — factor this into strategy selection
- Use `send_input` for incremental context injection in `continuous` strategy
- Use `close_agent` to release context when switching from `continuous` to `reset`

**agy-specific notes** (`_common/AGY_ORCHESTRATION.md` A2/A4/A5/A9):
- **Isolated by default.** agy subagents get their own context window and inherit none of the hub's history, so `continuous` cannot be assumed — write the state delta into an artifact and hand it over by path. This makes `reset`/`hybrid` the practical defaults on agy.
- **Inject files with `@<path>`, never a bare path** — a bare path is delegated to an internal subagent that dies at the 60s cap, producing a silent empty result.
- **Window ≠ usable window.** Gemini 3.7 Flash (High) offers 1,048,576 input tokens, but effective accuracy degrades past ~128k. This is a *length* claim; keep it separate from **position** dependence (*lost in the middle*, Liu et al., TACL 2024), which applies at any length — mid-context material is used less reliably than material at either end, and the remedy is not simply "put it first and last". Summarize or segment a handoff before it crosses that band rather than trusting the nominal window; label multiple sources with numbered headers ("Document 1", "Document 2").
- **Instruction placement flips for large injections.** With a big data/context block, put the instructions *after* the data and anchor with "Based on the preceding information…"; top-load only in normal-size prompts.

---

## Handoff File Structure

When using `reset` strategy, handoff files follow this structure:

```
.agents/handoffs/
  └── [task-slug]/
      ├── step-1-scout.md      # Scout's _STEP_COMPLETE output
      ├── step-2-builder.md    # Builder's _STEP_COMPLETE output
      ├── eval-1-judge.md      # Judge's EVALUATION_FEEDBACK
      └── contract.md          # Sprint Contract (if applicable)
```

**File format:** Standard `_STEP_COMPLETE` or `EVALUATION_FEEDBACK` YAML, wrapped in a markdown file for readability.

---

## Integration with AUTORUN

The `Context Strategy` column in the Model Selection table (`_common/AUTORUN.md`) indicates the default strategy per agent role. Nexus may override based on chain length and task complexity.
