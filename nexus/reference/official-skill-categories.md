# Official Skill Categories Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Official category reference for improving task classification accuracy in the Nexus CLASSIFY phase.

---

## 1. Official 3 Use-Case Categories

### Category 1: Document & Asset Creation

**Definition**: Generating consistent, high-quality output (documents, presentations, apps, designs, code, etc.)

**Task identification signals**:
- `"create"`, `"generate"`, `"design"`, `"build"` + artifact name
- Requests for file generation or template application
- Requests for compliance with style guides or brand standards

**Recommended chain patterns**:
- Scribe / Quill / Morph / Dot / Sketch → generation agent matched to the artifact
- Quality check: Judge

**Key Techniques** (official):
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing

### Category 2: Workflow Automation

**Definition**: Automating multi-step processes executed with a consistent methodology (including multi-MCP coordination)

**Task identification signals**:
- Mentions of `"automate"`, `"workflow"`, `"pipeline"`, `"process"`
- Requests for coordination across multiple tools/services
- Efficiency improvements for repeatedly executed tasks

**Recommended chain patterns**:
- Sherpa (decompose) → domain agents → Radar (verify)
- Large-scale: Titan → Nexus chain dispatch

**Key Techniques** (official):
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

### Category 3: MCP Enhancement

**Definition**: Augmenting tool access provided by MCP servers with workflow knowledge

**Task identification signals**:
- Direct mention of MCP tool names or service names
- `"integrate"`, `"connect"`, `"sync"` + external service
- Requests to optimize API integration

**Recommended chain patterns**:
- Frame / Relay / Vector → service-specific flow
- Hone (configuration optimization)

**Key Techniques** (official):
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

---

## 2. Official 5 Patterns and Routing Decisions

### Pattern → Chain Optimization Mapping

| Official Pattern | When to Apply | Chain Design Guidance |
|-----------------|---------------|----------------------|
| **Sequential Workflow** | Ordered multi-step, dependencies between steps | Sequential chain, no parallel branches |
| **Multi-MCP Coordination** | Cross-service workflow | Phase-separated chain with data passing, validation gates between phases |
| **Iterative Refinement** | Quality-sensitive output | Loop-capable chain with quality check agent (Judge) |
| **Context-Aware Tool Selection** | Same outcome, different tools per context | Decision point at CLASSIFY, context-dependent chain selection |
| **Domain-Specific Intelligence** | Regulatory/compliance/domain expertise required | Canon/domain expert injection before execution |

### Pattern Detection Rules for CLASSIFY

```
IF task involves ordered steps with dependencies:
  → Sequential Workflow pattern
  → Use simple sequential chain

IF task spans 2+ external services:
  → Multi-MCP Coordination pattern
  → Design phase-separated chain with inter-phase validation

IF task output requires quality iteration:
  → Iterative Refinement pattern
  → Include quality-check loop (max 3 iterations)

IF same goal achievable with different tools:
  → Context-Aware Tool Selection pattern
  → Add decision logic before chain selection

IF task requires domain expertise (compliance, finance, security):
  → Domain-Specific Intelligence pattern
  → Inject domain expert (Canon, Sentinel, etc.) before execution
```

---

## 3. Official Category Usage in the CLASSIFY Phase

### Extended CLASSIFY Process

Adds **official category classification** on top of the existing CLASSIFY (task type, complexity, confidence):

1. **Task Type detection** (existing): BUG / FEATURE / SECURITY / REFACTOR / OPTIMIZE / REVIEW
2. **Official Category detection** (new): Document & Asset / Workflow Automation / MCP Enhancement
3. **Official Pattern detection** (new): Sequential / Multi-MCP / Iterative / Context-Aware / Domain-Specific
4. **Chain Selection optimization**: chain adjustment based on official patterns

### Category × Task Type Matrix

| | BUG | FEATURE | SECURITY | REFACTOR | OPTIMIZE | REVIEW |
|--|-----|---------|----------|----------|----------|--------|
| **Document & Asset** | — | Forge→specialist→Judge | — | Zen→Judge | — | Judge |
| **Workflow Automation** | Scout→Builder→Radar | Sherpa→Builder→Radar | Sentinel→Builder | Zen→Radar | Bolt→Radar | Judge→Canon |
| **MCP Enhancement** | Scout→Builder→Radar | Frame/Relay→Builder→Radar | Sentinel→Probe | — | Bolt→Tuner | Judge |

---

## 4. VERIFY Enhancement via Official Success Criteria

### Official Metrics Reference in the VERIFY Phase

After chain execution, VERIFY evaluates official success criteria as supplementary checks:

| Metric | Check | Pass Criteria |
|--------|-------|--------------|
| Skill trigger accuracy | Auto-load rate against description | Conceptual confirmation (quantitative measurement separate) |
| Workflow efficiency | Step count and redundancy in the chain | Completed with minimal number of agents |
| Error handling | Recovery when errors occur | L1-L4 guardrails functioning |
| Output consistency | Result consistency for identical tasks | Structural consistency confirmed |

---

## 5. Problem-first vs Tool-first Approach Classification

At the CLASSIFY phase, determine the user's approach and reflect it in chain design:

| Approach | Detection Signal | Chain Impact |
|----------|-----------------|-------------|
| **Problem-first** | Describes desired outcome or goal ("I need to set up...") | Nexus automates tool selection |
| **Tool-first** | Directly specifies tool or service name ("I have X MCP...") | Respects user-specified tools while optimizing |

> Problem-first allows greater freedom in chain design. Tool-first respects the user's explicit choices.
