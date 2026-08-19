# Official Design Patterns Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Official design pattern reference for Architect's ENVISION / DESIGN phases.

---

## 1. Three Use Case Categories

### Category 1: Document & Asset Creation

**Used for**: Creating consistent, high-quality output — documents, presentations, apps, designs, code

**Key Techniques**:
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- No external tools required — uses Claude's built-in capabilities

**Real example**: `frontend-design` skill, Office skills (docx, pptx, xlsx, ppt)

### Category 2: Workflow Automation

**Used for**: Multi-step processes that benefit from consistent methodology, including multi-MCP coordination

**Key Techniques**:
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

**Real example**: `skill-creator` skill

### Category 3: MCP Enhancement

**Used for**: Workflow guidance to enhance tool access an MCP server provides

**Key Techniques**:
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

**Real example**: `sentry-code-review` skill (Sentry)

### Approach Selection: Problem-first vs Tool-first

| Approach | When | User Mindset |
|----------|------|-------------|
| **Problem-first** | "I need to set up a project workspace" | Describes outcomes; skill handles tools |
| **Tool-first** | "I have Notion MCP connected" | Has access; skill provides expertise |

> Most skills lean one direction. Knowing which framing fits the use case helps choose the right pattern.

---

## 2. Five Official Patterns

> These are implementation patterns for Claude skill design. For inter-agent structural patterns, see Section 7.

### Pattern 1: Sequential Workflow Orchestration

**Use when**: Users need multi-step processes in a specific order.

```markdown
## Workflow: Onboard New Customer
### Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company
### Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification
### Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)
### Step 4: Send Welcome Email
Call MCP tool: `send_email`
Template: welcome_email_template
```

**Key Techniques**: Explicit step ordering, dependencies between steps, validation at each stage, rollback instructions for failures

---

### Pattern 2: Multi-MCP Coordination

**Use when**: Workflows span multiple services.

**Example**: Design-to-development handoff

| Phase | Service | Actions |
|-------|---------|---------|
| 1. Design Export | Figma MCP | Export assets, generate specs, create manifest |
| 2. Asset Storage | Drive MCP | Create folder, upload assets, generate links |
| 3. Task Creation | Linear MCP | Create tasks, attach links, assign team |
| 4. Notification | Slack MCP | Post summary to #engineering with links and refs |

**Key Techniques**: Clear phase separation, data passing between MCPs, validation before next phase, centralized error handling

---

### Pattern 3: Iterative Refinement

**Use when**: Output quality improves with iteration.

```markdown
## Iterative Report Creation
### Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file
### Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues (missing sections, formatting, data errors)
### Refinement Loop
1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met
### Finalization
1. Apply final formatting
2. Generate summary
3. Save final version
```

**Key Techniques**: Explicit quality criteria, iterative improvement, validation scripts, knowing when to stop

---

### Pattern 4: Context-Aware Tool Selection

**Use when**: Same outcome, different tools depending on context.

**Example**: Smart file storage with decision tree

| Condition | Tool |
|-----------|------|
| Large files (>10MB) | Cloud storage MCP |
| Collaborative docs | Notion/Docs MCP |
| Code files | GitHub MCP |
| Temporary files | Local storage |

**Key Techniques**: Clear decision criteria, fallback options, transparency about choices (explain to user why that tool was chosen)

---

### Pattern 5: Domain-Specific Intelligence

**Use when**: Skill adds specialized knowledge beyond tool access.

**Example**: Financial compliance in payment processing

```markdown
### Before Processing (Compliance Check)
1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision
### Processing
IF compliance passed → process transaction
ELSE → flag for review, create compliance case
### Audit Trail
- Log all compliance checks
- Record processing decisions
- Generate audit report
```

**Key Techniques**: Domain expertise embedded in logic, compliance before action, comprehensive documentation, clear governance

---

### Pattern Selection Guide

| Your Need | Primary Pattern | Secondary Pattern |
|-----------|----------------|-------------------|
| Ordered multi-step process | Sequential Workflow | — |
| Cross-service coordination | Multi-MCP Coordination | Sequential Workflow |
| Quality-sensitive output | Iterative Refinement | Sequential Workflow |
| Context-dependent routing | Context-Aware Tool Selection | Domain-Specific Intelligence |
| Regulatory/domain constraints | Domain-Specific Intelligence | Sequential Workflow |
| Complex workflow spanning services + quality | Multi-MCP Coordination | Iterative Refinement |

---

## 3. Planning Methodology

### Use Case Definition Template

```
Use Case: [Name]
Trigger: [What user says or does]
Steps:
1. [Action with tool/MCP reference]
2. [Action]
3. [Action]
Result: [Expected outcome]
```

### Technical Requirements Checklist

1. **Tools inventory**: Built-in capabilities vs MCP requirements
2. **File structure**: `SKILL.md` + `scripts/` + `reference/` + `assets/`
3. **Dependencies**: Environment requirements → `compatibility` field
4. **Folder naming**: kebab-case, matching `name` field

### Planning Questions

- What does a user want to accomplish?
- What multi-step workflows does this require?
- Which tools are needed (built-in or MCP)?
- What domain knowledge or best practices should be embedded?

---

## 4. Success Criteria Framework

### Quantitative Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Trigger accuracy | 90%+ on relevant queries | 10-20 test queries, track auto-load rate |
| Workflow efficiency | X tool calls (baseline comparison) | Same task with/without skill |
| API reliability | 0 failed calls per workflow | MCP server logs, retry rates |

### Qualitative Metrics

| Metric | Assessment |
|--------|-----------|
| Self-guided completion | Users don't need to prompt Claude about next steps |
| Correction-free execution | Same request 3-5 times yields consistent quality |
| First-try accessibility | New user accomplishes task with minimal guidance |

### Baseline Comparison Template

| Dimension | Without Skill | With Skill |
|-----------|--------------|------------|
| User instructions | Provided each time | Automatic |
| Back-and-forth | ~15 messages | ~2 clarifying questions |
| Failed API calls | ~3 requiring retry | 0 |
| Token consumption | ~12,000 | ~6,000 |

> Note: These are aspirational targets — rough benchmarks rather than precise thresholds. Anthropic is actively developing more robust measurement guidance and tooling.

### Empirical Evidence for Skill Impact

A production deployment quantifies how much externalizing procedural knowledge into skills matters: in Anthropic's internal self-service analytics agent, the same task scored **21% accuracy without skills and consistently above 95% with skills** — the largest single lever in the stack. The transferable lesson for skill design: the bottleneck is rarely the model's raw capability or its access to information, but whether procedural knowledge (table grain, scope, exclusions, gotchas, common patterns) is encoded as a retrievable, LLM-readable skill. Auto-generating that knowledge with an LLM *failed* — it encoded ambiguity instead of resolving it; human curation of the reference material remained essential. [Source: claude.com — *How Anthropic Enables Self-Service Data Analytics with Claude*]

---

## 5. Progressive Disclosure Design Principle

### Three-Level System

| Level | Content | Loading | Design Goal |
|-------|---------|---------|-------------|
| **1st** | YAML frontmatter | Always in system prompt | Minimal: just enough for Claude to know WHEN to use |
| **2nd** | SKILL.md body | When skill judged relevant | Full instructions, core workflow |
| **3rd** | `reference/`, `scripts/`, `assets/` | On-demand navigation | Detailed docs, validation, templates |

### Application in Design

- **SKILL.md**: Keep under 5,000 words. Focus on core instructions.
- **reference/**: Detailed API patterns, rate limiting, pagination, error codes
- **scripts/**: Deterministic validation (code > language instructions for critical checks)
- **assets/**: Templates, fonts, icons used in output

---

## 6. Composability Principle

### Portability

- Skills work identically across **Claude.ai**, **Claude Code**, and **API**
- Create once, works across all surfaces
- Note environment dependencies in `compatibility` field

### MCP Complementarity (Kitchen Analogy)

| | MCP | Skills |
|---|-----|--------|
| **Metaphor** | Professional kitchen | Recipes |
| **Provides** | Tool access, real-time data | Workflows, best practices |
| **Answers** | What Claude **can** do | How Claude **should** do it |

### Multi-Skill Coexistence

- Skills should work alongside others
- Don't assume exclusive capability
- Design for composition, not isolation

### Distribution Considerations

| Surface | Capability |
|---------|-----------|
| Claude.ai | Upload via Settings > Capabilities > Skills |
| Claude Code | Place in skills directory |
| API | `/v1/skills` endpoint, `container.skills` parameter |
| Organization | Admin workspace-wide deployment |

---

## 7. Agentic Composable Patterns (Anthropic 2025-2026)

> Source: Anthropic "Building effective agents" (2025) + subsequent updates (2026)

The 5 patterns in Section 2 are intra-skill implementation patterns. This section covers inter-agent and inter-workflow structural patterns.

### Design Philosophy: Simplicity First

The key to successful agent systems is to start with the simplest possible configuration and only add complexity when there is measurable improvement. Rather than introducing frameworks or orchestration layers upfront, build up from composable primitive patterns as needed.

### Pattern A: Prompt Chaining

**Structure**: Fixed-step sequential pipeline. Each step's output becomes the next step's input.

```
Step 1 → Gate ✓ → Step 2 → Gate ✓ → Step 3 → Output
                ✗ → Abort/Retry
```

**When to use**: Tasks naturally decompose into independent subtasks, and you want to gate quality at each step.
**Skill design implication**: Superset of Sequential Workflow Orchestration (Pattern 1). Explicitly insert gates (quality checks, approvals, validations) between steps.

### Pattern B: Routing

**Structure**: Classify input and dispatch to specialized handlers.

```
Input → Classifier → Handler A (domain 1)
                   → Handler B (domain 2)
                   → Handler C (domain 3)
```

**When to use**: Different input types require different optimal processing paths. Each path can be optimized independently.
**Skill design implication**: Generalization of Context-Aware Tool Selection (Pattern 4). Nexus routing logic is a canonical example. Use `Output Routing` tables to make branching conditions explicit.

### Pattern C: Parallelization

**Structure**: Execute tasks concurrently and aggregate results. Two variants:

| Variant | Description | Example |
|---------|-------------|---------|
| **Sectioning** | Split task into independent parts for parallel processing | Concurrent review of multiple files |
| **Voting** | Execute the same task multiple times and aggregate results | Multi-perspective evaluation, consensus judgment |

**When to use**: Subtasks are independent (Sectioning), or reliability/diversity is needed (Voting).
**Skill design implication**: Nexus chains and Rally (Sectioning) are existing implementations. Specify parallelizable partners in `COLLABORATION_PATTERNS`.

### Pattern D: Orchestrator-Worker

**Structure**: Central orchestrator dynamically decomposes tasks and delegates to workers.

```
Orchestrator → [dynamic task decomposition]
  → Worker 1 (Task A)
  → Worker 2 (Task B)
  → Worker N (Task N)
Orchestrator ← [result synthesis]
```

**When to use**: Task decomposition cannot be predicted in advance and requires runtime judgment.
**Skill design implication**: Nexus Hub-and-Spoke and its scope-adaptive `deliver` Recipe exemplify this pattern. Ensure hub compatibility via the `Nexus Compatibility` section.

### Pattern E: Evaluator-Optimizer

**Structure**: Generate → Evaluate → Improve feedback loop.

```
Generator → Output → Evaluator → Feedback
    ↑                                 │
    └─────────── Refine ──────────────┘
```

**When to use**: Clear evaluation criteria exist, and iterative refinement improves quality.
**Skill design implication**: Structured version of Iterative Refinement (Pattern 3). Judge→Builder feedback loop is a canonical example. Extract evaluation criteria into `reference/` and separate generation from evaluation responsibilities.

### Pattern F: Autonomous Agent

**Structure**: Autonomously loop tool usage based on environment feedback.

```
while (!done) {
  Observe → Plan → Act (tool use) → Evaluate result
}
```

**When to use**: Exploratory tasks, multi-stage problem solving, or tasks requiring environment interaction.
**Skill design implication**: Scout (bug investigation) and Vector (browser automation) are existing implementations. Always design loop termination conditions and guardrails (max iterations, timeouts, safety constraints).

### Existing ↔ Agentic Pattern Mapping

| Agentic Pattern | Closest Existing Pattern (Section 2) | Relationship | Ecosystem Example |
|----------------|--------------------------------------|--------------|-------------------|
| A: Prompt Chaining | P1: Sequential Workflow | P1 is a concrete impl of A | Orbit (runner scripts) |
| B: Routing | P4: Context-Aware Tool Selection | P4 is B specialized for tool selection | Nexus (Output Routing) |
| C: Parallelization | — (new) | No existing pattern | Rally (Sectioning) |
| D: Orchestrator-Worker | P2: Multi-MCP Coordination | P2 is D specialized for MCP | Nexus (`deliver` included) |
| E: Evaluator-Optimizer | P3: Iterative Refinement | P3 is a self-contained version of E | Judge↔Builder loop |
| F: Autonomous Agent | P5: Domain-Specific Intelligence | P5 adds domain knowledge to F | Scout, Vector |

---

## 8. Simplicity-First Design Principle

### Decision Ladder

A framework for progressively escalating agent system complexity. Do not advance to a higher level if the lower level can solve the problem.

| Level | Composition | When to Use |
|-------|-------------|-------------|
| **L0** | Single prompt + retrieval | One-shot Q&A, knowledge lookup |
| **L1** | Single prompt + tools | Single task with external integration |
| **L2** | Prompt Chaining / Routing | Fixed-flow multi-stage processing |
| **L3** | Orchestrator-Worker / Evaluator-Optimizer | Dynamic task decomposition or iterative refinement needed |
| **L4** | Multi-Agent Autonomous | Multiple autonomous agents cooperating |

### Application to Skill Design

- **ENVISION phase**: Map requirements to the Decision Ladder and identify the minimum level.
- **DESIGN phase**: Apply the Agentic Pattern corresponding to the chosen level. Document specific reasons before escalating to a higher level.
- **VALIDATE phase**: Verify the final design uses the minimum necessary complexity.

---

## 9. Interoperability Awareness

### MCP (Model Context Protocol)

Industry-standard protocol connecting AI models to external services and data sources.

- When a skill depends on MCP servers, declare it explicitly in the `compatibility` field.
- Skills in the MCP Enhancement category (Section 1) assume MCP server availability.
- Recommend **graceful degradation** so basic functionality works without MCP.

### A2A Protocol (Agent-to-Agent)

Agent-to-agent communication protocol proposed by Google. Defines capability advertisement via Agent Cards and task-based asynchronous communication.

- No direct impact on skill design at present, but recognized as a future consideration.
- The ecosystem's `CAPABILITIES_SUMMARY` is conceptually equivalent to Agent Card capability advertisement.
- The Nexus Hub-and-Spoke model is structurally similar to A2A's task delegation pattern.

### Agent Harness Pattern (Anthropic 2026)

State management pattern for long-running agents. Structures interruption, resumption, and state recovery.

- Limited direct applicability since the current ecosystem uses a 1-session = 1-task model.
- However, Orbit's `state files` and Rally's `multi-session` design are partial implementations of this pattern.
- Recorded as a reference pattern for future cross-session design.

---

## 10. Intelligence Harnessing Principles

> Source: Anthropic "Harnessing Claude's Intelligence" (2025)

Three design principles for building agent systems that adapt to evolving model capabilities. These principles complement the Simplicity-First Decision Ladder (Section 8) with empirical evidence and concrete design rules.

### 10.1 General Tools Over Specialized Tools

Prefer composing general-purpose tools (bash, text editor, file I/O) into patterns over building specialized single-purpose tools.

| Evidence | Result |
|----------|--------|
| SWE-bench Verified (2025-Q1 historical reference) | Claude 3.5 Sonnet achieved 49% using only bash + text editor. Current Claude 4.x results have surpassed this number; the historical figure is preserved here to anchor the design rule that simple tools + good models often beat custom-tool architectures. |

**Design rule**: Skills, programmatic tool calling, and memory systems should build on general tool composition. Create specialized tools only when general composition is insufficient — and only when one of the four boundary conditions in Section 10.3 is met.

### 10.2 "What Can I Stop Doing?" Audit

Systematically question whether each piece of orchestration scaffolding is still necessary as model capabilities improve. Three audit dimensions:

| Dimension | Principle | Evidence (as of 2025) | Design Implication |
|-----------|-----------|----------------------|-------------------|
| **Orchestration** | Let agents write code to filter tool outputs instead of routing all results through context | BrowseComp: 45.3% → 61.6% with self-filtering (2025-era Opus-class measurement; not re-verified on Opus 5) | Design agents with code execution for output filtering; avoid piping all tool results through context window |
| **Context management** | Progressive disclosure via skills instead of pre-loading all instructions | See Section 5 (Three-Level System) | Keep L1 frontmatter minimal; load L2/L3 on demand |
| **Persistence** | Memory folders (file-based) vs compaction (in-context summarization) | BrowseComp: 84% with memory folders (2025-era Opus-class measurement) vs 43% flat (Sonnet 4.5); not re-verified on Opus 5 | For Opus-class models, design for file-based persistence; for Sonnet-class, keep context in-window. Effectiveness is model-dependent |

**Application**: Use `_common/HARNESS_EVOLUTION.md` Systematic Scaffold Audit protocol to evaluate each scaffolding component against these dimensions.

### 10.3 Boundary-Aware Design

Three sub-principles for setting effective boundaries without introducing dead weight:

**Prompt caching optimization**: Structure context with stable content first (system prompts, tool definitions, skill instructions), then dynamic content (user input, conversation history, retrieved context). Cached tokens cost 10% of base input tokens. Use ToolSearch for dynamic tool discovery to avoid bloating the static tool list and breaking cache prefixes.

**Declarative tool promotion criteria**: Promote an action from general tool composition to a dedicated declarative tool ONLY when it crosses one of four thresholds:

| Threshold | Rationale | Example |
|-----------|-----------|---------|
| Security boundary | Credential isolation, input sanitization | API calls requiring auth tokens |
| Reversibility | Destructive actions need confirmation gates | Database writes, file deletion |
| UX presentation | Structured output for user-facing display | Rich UI rendering, formatted reports |
| Observability | Structured logging, audit trails | Compliance-sensitive operations |

If none of these thresholds apply, keep the action as a composed general-tool pattern.

**Dead weight pruning**: Every safeguard encodes an assumption about model limitations. Regularly audit whether these assumptions still hold. See `_common/HARNESS_EVOLUTION.md` for the evaluation cycle and simplification conditions.

---

## 11. Opus 5 Operating Principles for Generated Skills

> Source: Anthropic *Prompting Claude Opus 5* + *Migrating to Claude Opus 5* + *Effort* (platform.claude.com, verified 2026-07-25)
> Canonical detail and full principle text: `_common/OPUS_5_AUTHORING.md` (P1–P12). That file is the single source of truth — cite by ID, do not duplicate the principle text here.

Opus 5 has sharp default behaviors that generated skills must author for explicitly. **Three defaults cost tokens on every workload and are the highest-value checks: long output (P2), scope expansion (P8), and automatic self-verification (P9).** Apply the phase mapping below when designing new agents or updating existing ones.

### 11.13 Application in Architect Phases

| Phase | Apply |
|-------|-------|
| `UNDERSTAND` | Confirm caller-provided context is complete (P1); flag missing fields once, not iteratively |
| `DESIGN` | Bake length envelopes for both channels (P2), tool-use rationale (P3), delegation caps (P4), thinking-on assumptions (P5), scope bounds (P8), and — for reviewers — coverage-vs-filter (P10) into the section contract |
| `GENERATE` | Verify generated SKILL.md states effort-level expectations against a `high` default (P6), delegation-engineer framing (P7), scope bounds (P8), carries **no** self-verification scaffolding (P9), (writers/designers) voice/artifact defaults (P11), and holds to context minimalism (P12) |
| `VALIDATE` | Add Opus 5 readiness checks to the validation pass — a skill that omits P2 / P8 / P9 guidance will over-produce, over-reach, and over-verify at runtime; one that omits P12 ships prompt bloat that costs tokens on every call |
