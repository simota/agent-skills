# Context Strategy Reference

**Purpose:** Guidelines for managing context windows across agent chains.
**Read when:** You need to decide how context flows between agents in a chain.

---

## Overview

Different tasks and model combinations benefit from different context management strategies. This reference defines three strategies and when to apply each.

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
   タスク: メール検証ロジックを実装してください。

   # Bad: exposes full chain scope
   タスク: メール検証を実装してください。その後、電話番号検証、住所検証、
   プロフィールUI、テスト、セキュリティスキャンも必要です。
   ```

2. **Context budget monitoring** — When Nexus context usage exceeds 70%, switch from `continuous` to `reset` for remaining steps

3. **Selective context injection** — Pass only relevant prior results, not full chain history
   ```
   # Good: selective
   前ステップの結果: Scout が auth/refresh.ts:87 にトークンリフレッシュの競合状態を特定

   # Bad: full dump
   前ステップの結果: [Scout's entire 2000-line output]
   ```

---

## Platform Compatibility

| Strategy Aspect | Claude Code | Codex CLI |
|----------------|-------------|-----------|
| `reset` handoff | Agent prompt contains summary only | `spawn_agent()` prompt contains summary only |
| `continuous` handoff | Prior Agent results in Nexus context | Prior `wait_agent()` results in orchestrator context |
| `hybrid` default | Nexus context + Agent(fresh) | Orchestrator context + `spawn_agent(fresh)` |
| Context budget check | Monitor via conversation length | Monitor via `agents.max_depth` and prompt size |
| Fallback trigger | Context usage > 70% | Prompt token count approaches model limit |

**Codex-specific notes:**
- `agents.max_depth` (default: 1) limits nesting — factor this into strategy selection
- Use `send_input` for incremental context injection in `continuous` strategy
- Use `close_agent` to release context when switching from `continuous` to `reset`

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
