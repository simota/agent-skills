# Context Compression Reference

**Purpose:** Compression strategies, token-budget methods, and equivalence checks.
**Read when:** You need to reduce context cost without changing behavior.

## Contents
- Overview
- Token Estimation Guidelines
- Compression Strategies
- Ma Design Principles
- Equivalence Verification
- Compression Priority Matrix
- COMPRESSION_PROPOSAL Output Template
- Quick Reference

---

## Overview

In a large agent ecosystem, repeated boilerplate can consume a meaningful share of the token budget. This reference provides systematic approaches to reduce token consumption while preserving behavioral equivalence.

---

## Token Estimation Guidelines

### Estimation Method

| Content Type | Chars/Token (approx) | Notes |
|-------------|----------------------|-------|
| English prose | ~4 chars/token | Standard technical writing |
| Japanese prose | ~1.5 chars/token | Higher token density per character |
| YAML/Code | ~3.5 chars/token | Structured content |
| Mixed (EN+JP) | ~2.5 chars/token | Typical SKILL.md content |

### Section Token Budget

| Section | Target Tokens | Priority |
|---------|--------------|----------|
| Frontmatter | 20-40 | Core |
| CAPABILITIES_SUMMARY | 80-150 | Core |
| Philosophy/Identity | 40-80 | Core |
| Boundaries | 100-200 | Core |
| INTERACTION_TRIGGERS | 200-500 | Core |
| Domain Sections | 600-2000 | Core |
| Collaboration | 150-300 | Core |
| Journal | 60-100 | Standard |
| Daily Process | 80-150 | Standard |
| Tactics/Avoids | 50-100 | Standard |
| Activity Logging | 30-60 | Boilerplate |
| AUTORUN Support | 200-400 | Integration |
| Nexus Hub Mode | 100-200 | Integration |
| Output Language | 10-20 | Boilerplate |
| Git Guidelines | 40-80 | Boilerplate |
| **Total Target** | **1500-4000** | — |

### TOKEN_ESTIMATE Template

```yaml
TOKEN_ESTIMATE:
  agent: "[Agent name]"
  date: "[YYYY-MM-DD]"
  sections:
    - name: "[Section name]"
      lines: [count]
      estimated_tokens: [count]
      category: core | standard | boilerplate | integration
      compression_potential: low | medium | high
  totals:
    total_lines: [count]
    estimated_tokens: [count]
    boilerplate_ratio: "[X%]"
    compression_target: "[Y% reduction]"
```

---

## Compression Strategies

### Strategy 1: Deduplication

**Target:** Boilerplate sections repeated across all agents
**Expected Reduction:** 60-85% per deduplicated section
**Risk:** Low (content moves to `_common/`, not deleted)

Identify sections that are identical or near-identical across agents and extract them to `_common/` shared files.

**Before (example across 64 agents: 384 lines):**
```markdown
## Activity Logging (REQUIRED)

After completing your task, add a row to `.agents/PROJECT.md` Activity Log:
| YYYY-MM-DD | [AgentName] | (action) | (files) | (outcome) |

Example:
| 2025-01-15 | [AgentName] | [Sample action] | [Sample files] | [Sample outcome] |
```

**After (1 line per agent):**
```markdown
## Activity Logging
See `_common/ACTIVITY_LOGGING.md` for format.
```

**High-value deduplication targets:**
| Section | Lines/Agent | Agents | Total Lines | Savings |
|---------|------------|--------|-------------|---------|
| Activity Logging | 6 | 64 | 384 | ~320 |
| Output Language | 3 | 64 | 192 | ~128 |
| Git Guidelines | 12 | 64 | 768 | ~640 |
| Nexus Hub Mode | 25 | 64 | 1600 | ~1280 |
| AUTORUN boilerplate | 8 | 64 | 512 | ~384 |
| **Total** | **54** | — | **3456** | **~2752** |

### Strategy 2: Density

**Target:** Verbose prose that can be structured data
**Expected Reduction:** 20-40% per converted section
**Risk:** Low (information preserved, format changed)

Convert verbose prose descriptions into YAML, tables, or structured formats that convey the same information with fewer tokens.

**Before (5 lines):**
```markdown
When the functional overlap with an existing agent exceeds 30%, you must ask
the user for confirmation before proceeding. This is because high overlap can
lead to confusion in routing and redundant capabilities in the ecosystem.
The user can choose to differentiate, merge, or cancel.
```

**After (3 lines, table format):**
```markdown
| Condition | Action | Options |
|-----------|--------|---------|
| Overlap > 30% | Ask user | Differentiate / Merge / Cancel |
```

### Strategy 3: Hierarchy

**Target:** Detailed content that can be moved to references
**Expected Reduction:** 30-60% of moved content from SKILL.md
**Risk:** Medium (LLM must follow references; core behavior stays in SKILL.md)

Keep essential behavioral instructions in SKILL.md; move detailed methodology, examples, and templates to `reference/*.md`.

**Principle:** SKILL.md = "what to do" + "when to do it"; references = "how to do it in detail"

**Before (in SKILL.md, 40 lines of YAML template):**
```markdown
### Question Templates
**ON_AGENT_OVERLAP:**
[... 15 lines of YAML ...]
**ON_VALUE_UNCLEAR:**
[... 15 lines of YAML ...]
```

**After (in SKILL.md, 3 lines):**
```markdown
### Question Templates
See `reference/interaction-templates.md` for full YAML templates.
Triggers: ON_AGENT_OVERLAP, ON_VALUE_UNCLEAR, ON_QUALITY_FEEDBACK, ON_ENHANCEMENT_PRIORITY
```

### Strategy 4: Symbolic

**Target:** Repeated patterns across sections
**Expected Reduction:** 40-70% for pattern instances
**Risk:** Medium (requires `_common/` schema to be loaded)

Replace repeated structural patterns with symbolic references to `_common/` schemas.

**Before (repeated in every agent):**
```yaml
_STEP_COMPLETE:
  Agent: [AgentName]
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output: ...
  Handoff: ...
  Next: ...
  Reason: ...
```

**After (symbolic reference):**
```yaml
_STEP_COMPLETE:
  $schema: "_common/schemas/step-complete.yaml"
  Agent: [AgentName]
  Output:
    # Agent-specific output only
```

### Strategy 5: Loose Prompt

**Target:** Over-specified instructions that constrain LLM flexibility
**Expected Reduction:** 30-50% of instruction content
**Risk:** Medium-High (requires careful equivalence testing)

Based on the Harvest pattern: provide essential intent and constraints only, omitting step-by-step instructions that capable LLMs can infer.

**Before (12 lines):**
```markdown
## Daily Process
1. RECEIVE - Read the input carefully
   - Parse the user request
   - Identify the key requirements
   - Determine the task type
2. ANALYZE - Examine the codebase
   - Read relevant files
   - Check for existing patterns
   - Note dependencies
3. IMPLEMENT - Make changes
   - Write code following patterns
   - Add tests
   - Verify changes work
```

**After (4 lines):**
```markdown
## Daily Process
RECEIVE → ANALYZE → IMPLEMENT → VALIDATE
- Each phase completes fully before the next begins
- See `reference/workflow.md` for detailed phase descriptions
```

**When to use Loose Prompt:**
- Agent with Health Score A (well-established behavior)
- Sections where LLM can infer from context
- Non-critical operational details

**When NOT to use Loose Prompt:**
- Boundary definitions (Always/Ask/Never)
- Critical safety constraints
- Integration formats (AUTORUN, Nexus Hub)
- New or experimental agents

---

## Ma Design Principles

The concept of "Ma" — meaningful space — applies to how LLMs process context. Attention is not uniform across a context window; strategic placement of content optimizes comprehension.

### Attention Pattern Principles

#### 1. Primacy Effect

**First 15% of context receives heightened attention.**

Place in the first 15%:
- Agent identity and mission
- Core capabilities (CAPABILITIES_SUMMARY)
- Critical boundaries (Always/Never)
- Philosophy statement

#### 2. Recency Effect

**Last 15% of context receives heightened attention.**

Place in the last 15%:
- Actionable templates (AUTORUN, Nexus Hub)
- Output format specifications
- Closing identity reinforcement
- Quick-reference checklists

#### 3. Middle Sag

**Middle 70% receives relatively lower attention.**

Place in the middle:
- Reference material and catalogs
- Detailed methodology
- Examples and patterns
- Historical/contextual information

#### 4. Cognitive Chunking

**Use `---` separators every 50-80 lines to create attention anchors.**

- Markdown horizontal rules act as "attention resets"
- Each chunk should be self-contained on one topic
- Headers at chunk starts recapture attention

#### 5. Contrast & Rhythm

**Alternate between dense structured content and sparse instructional content.**

```
[Dense: YAML template]     ← High information density
[Sparse: 2-line principle] ← Breathing room
[Dense: Table]             ← High information density
[Sparse: 1-line rule]      ← Breathing room
```

This rhythm prevents attention fatigue and aids information retention.

### Optimal SKILL.md Layout

```
┌─────────────────────────────────────┐
│  ZONE 1: PRIME (first 15%)         │  ← Highest attention
│  - Frontmatter                      │
│  - CAPABILITIES_SUMMARY             │
│  - Identity + Philosophy            │
│  - Boundaries (Always/Ask/Never)    │
│  - INTERACTION_TRIGGERS (table)     │
├─────────────────────────────────────┤
│  ZONE 2: CORE (next 35%)           │  ← Moderate attention
│  - Primary workflow/framework       │
│  - Domain-specific sections         │
│  - Key decision tables              │
├─────────────────────────────────────┤
│  ZONE 3: REFERENCE (next 35%)      │  ← Lower attention
│  - Catalogs and listings            │
...
```

### Anti-patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| Front-loading boilerplate | Wastes primacy attention on low-value content | Move boilerplate to Zone 3/4 or `_common/` |
| Burying identity | Agent doesn't consistently adopt persona | Move identity to first 10 lines |
| Monotone density | Uniform density causes attention fatigue | Alternate dense/sparse sections |
| No separators | Context reads as undifferentiated wall of text | Add `---` every 50-80 lines |
| Critical info in middle | Important constraints get lower attention | Move to Zone 1 or Zone 4 |
| Redundant closings | Multiple "remember you are X" statements | Single strong closing in Zone 4 |

### Cache-Aware Ordering

The Ma layout naturally supports prompt caching efficiency. Cached tokens cost **10% of base input tokens** (as of 2025), making static-first ordering economically significant.

| Content Type | Placement | Cache Behavior |
|-------------|-----------|---------------|
| System prompt, tool definitions | First (stable across turns) | Cached — 90% cost reduction |
| Skill instructions (SKILL.md) | Second (stable within session) | Cached after first load |
| Conversation history, user input | Last (changes each turn) | Not cached — full cost |

**ToolSearch pattern**: For dynamic tool discovery, use ToolSearch (deferred tool loading) rather than pre-loading all tool schemas. This keeps the static tool definition block small and stable, preserving the cache prefix across turns.

---

## Persistence Strategy Selection

When designing agents that manage information across context boundaries, choose the persistence strategy based on task horizon and target model capability.

| Strategy | Mechanism | Best When | Evidence (as of 2025) |
|----------|-----------|-----------|----------------------|
| **Compaction** | Summarize and compress context in-place | Session-scoped tasks, cost-sensitive, Sonnet-class models | Standard context management |
| **Memory folders** | Write findings to files, read back on demand | Multi-session research, complex investigation, Opus-class models | BrowseComp: 84% (Opus 4.6) vs 43% flat (Sonnet 4.5) |
| **Hybrid** | Compaction for working memory + files for durable findings | Long-horizon tasks with both immediate and archival needs | Combines benefits of both approaches |

**Model-dependent effectiveness**: Memory folder strategies show strong model dependence. Opus-class models organize file-based memory tactically and benefit significantly; Sonnet-class models may not show improvement. Design persistence strategies with the target model tier in mind.

**Design implication for skills**: When a skill involves multi-step research or investigation (e.g., Scout, Lens, Trail), consider designing explicit file-based memory checkpoints rather than relying solely on context accumulation.

---

## Equivalence Verification

After compression, verify behavioral equivalence across 4 axes.

### Verification Axes

| Axis | What to Check | Method |
|------|---------------|--------|
| **Behavioral** | Agent produces same outputs for same inputs | Test with 3 representative prompts |
| **Structural** | All required sections still present | Checklist against `skill-template.md` |
| **Integration** | AUTORUN/Nexus/Handoff formats intact | Format validation against schemas |
| **Routing** | Nexus can still route to this agent correctly | Verify CAPABILITIES_SUMMARY coverage |

### EQUIVALENCE_REPORT Template

```yaml
EQUIVALENCE_REPORT:
  agent: "[Agent name]"
  date: "[YYYY-MM-DD]"
  compression_applied:
    strategies: ["dedup", "density", "hierarchy"]
    lines_before: [count]
    lines_after: [count]
    reduction: "[X%]"
  verification:
    behavioral:
      status: PASS | FAIL
      test_prompts: [count]
      issues: ["[issue if any]"]
    structural:
      status: PASS | FAIL
# ...
```

---

## Compression Priority Matrix

### By Section (ecosystem-wide)

| Priority | Section | Lines/Agent | Compression Strategy | Expected Savings |
|----------|---------|------------|---------------------|-----------------|
| P1 | AUTORUN boilerplate | 8 | Symbolic → `_common/` schema | 75% |
| P1 | Nexus Hub Mode | 25 | Deduplication → `_common/` | 80% |
| P1 | Git Guidelines | 12 | Deduplication → `_common/` | 85% |
| P2 | Activity Logging | 6 | Deduplication → `_common/` | 83% |
| P2 | INTERACTION_TRIGGERS templates | 30-60 | Hierarchy → reference/ | 50% |
| P2 | Daily Process (verbose) | 15-30 | Density → table/list | 30% |
| P3 | Output Language | 3 | Deduplication → `_common/` | 67% |
| P3 | Collaboration diagrams | 20-40 | Hierarchy → reference/ | 40% |

### By Agent (individual targets)

| Priority | Agent | Current Lines | Target Lines | Strategy |
|----------|-------|--------------|-------------|----------|
| P1 | Guardian | >1400 | <1200 | Hierarchy + Density |
| P1 | Builder | >1400 | <1200 | Hierarchy + Density |
| P1 | Probe | >1400 | <1200 | Hierarchy + Dedup |
| P2 | Agents 800-1400 lines | varies | -15% | Dedup + Density |
| P3 | Agents <800 lines | varies | no change | Ma layout only |

---

## COMPRESSION_PROPOSAL Output Template

```yaml
COMPRESSION_PROPOSAL:
  agent: "[Agent name]"
  date: "[YYYY-MM-DD]"
  analysis:
    current_lines: [count]
    estimated_tokens: [count]
    boilerplate_lines: [count]
    boilerplate_ratio: "[X%]"
    ma_compliance:
      zone1_identity: [true/false]
      zone4_actionable: [true/false]
      separator_frequency: "[avg lines between ---]"
      density_rhythm: "[good/poor]"
  proposals:
    - id: 1
# ...
```

---

## Quick Reference

### Compression Decision Tree

```
Is the section identical across 80%+ of agents?
  YES → Strategy 1: Dedup to _common/
  NO  ↓
Is the content verbose prose that could be a table/YAML?
  YES → Strategy 2: Density conversion
  NO  ↓
Is the section >30 lines of detail that reference/ could hold?
  YES → Strategy 3: Hierarchy (move to reference/)
  NO  ↓
Is the section a structural pattern repeated with minor variations?
  YES → Strategy 4: Symbolic ($schema reference)
  NO  ↓
Is the section step-by-step instructions an LLM can infer?
  YES → Strategy 5: Loose Prompt (if agent is mature)
  NO  → Keep as-is
```

### Safety Rules

1. **Never compress Boundaries** (Always/Ask/Never) — these are behavioral constraints
2. **Never compress CAPABILITIES_SUMMARY** — Nexus routing depends on it
3. **Always verify integration formats** after compression (AUTORUN, Nexus Hub)
4. **Always run equivalence check** before finalizing compression
5. **Prefer reversible compression** (hierarchy > loose prompt)
