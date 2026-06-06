# Overlap Detection

**Purpose:** Overlap-scoring method and confirmation thresholds.
**Read when:** You must prove differentiation or decide whether overlap is too high.

## Contents
- Overview
- Overlap Calculation Method
- Overlap Categories
- Overlap Detection Matrix
- Threshold Guidelines
- Common Overlap Scenarios
- Differentiation Strategies
- Overlap Report Template
- Automated Overlap Detection
- Exception Cases

---

## Overview

Overlap detection prevents creating agents with duplicate responsibilities.
The threshold for requiring user confirmation is **30%** functional overlap.

---

## Overlap Calculation Method

### Step 1: Capability Extraction

Extract capabilities from both agents:

```yaml
AGENT_A_CAPABILITIES:
  - capability_1
  - capability_2
  - capability_3
  - capability_4
  - capability_5

AGENT_B_CAPABILITIES:
  - capability_1  # Same as A
  - capability_3  # Same as A
  - capability_6
  - capability_7
```

### Step 2: Similarity Matching

Compare capabilities using semantic similarity:

| Match Type | Score |
|------------|-------|
| Exact match | 1.0 |
| Synonym/equivalent | 0.8 |
| Partial overlap | 0.5 |
| Related but different | 0.2 |
| No relation | 0.0 |

### Step 3: Overlap Percentage

```
Overlap % = (Sum of match scores) / (Total capabilities) × 100
```

### Example Calculation

```yaml
NEW_AGENT_CAPABILITIES:
  - Input validation
  - Schema generation
  - Error type creation
  - Type inference

EXISTING_AGENT_BUILDER_CAPABILITIES:
  - Input validation (Zod schemas)    # → 0.8 match
  - Type-safe implementation          # → 0.5 match (partial)
  - Error handling                    # → 0.5 match (partial)
  - API integration                   # → 0.0 match

Match scores: 0.8 + 0.5 + 0.5 + 0.0 = 1.8
Total: 4
Overlap: 1.8 / 4 × 100 = 45%
```

**Result**: 45% > 30% threshold → Trigger ON_AGENT_OVERLAP

---

## Overlap Categories

### 1. Functional Overlap

Same actions performed on same inputs.

**High Risk Examples:**
- Both create tests → Radar vs Voyager conflict
- Both refactor code → Zen vs Builder conflict
- Both analyze security → Sentinel vs Probe conflict

**Resolution Strategies:**
- Narrow scope (unit vs E2E, static vs dynamic)
- Different input types (code vs running app)
- Different output formats

### 2. Domain Overlap

Same technical/business domain.

**High Risk Examples:**
- Both handle authentication → Builder vs Sentinel conflict
- Both optimize performance → Bolt vs Tuner conflict
- Both design UI → Muse vs Palette conflict

**Resolution Strategies:**
- Different aspects (implementation vs security)
- Different layers (app vs database)
- Different concerns (visual vs usability)

### 3. Output Overlap

Same deliverable type.

**High Risk Examples:**
- Both produce Markdown specs → Spark vs Gateway conflict
- Both produce test files → Radar vs Voyager conflict
- Both produce diagrams → Canvas vs Atlas conflict

**Resolution Strategies:**
- Different diagram types (flowchart vs dependency)
- Different test types (unit vs E2E)
- Different spec formats (feature vs API)

---

## Overlap Detection Matrix

### Quick Reference

| New Agent Type | Check Against | Common Overlap Areas |
|----------------|---------------|---------------------|
| Investigation | Scout, Spark, Triage | Root cause analysis, reporting |
| Implementation | Builder, Forge, Artisan | Code generation, patterns |
| Testing | Radar, Voyager | Test creation, coverage |
| Security | Sentinel, Probe | Vulnerability detection |
| Review | Judge, Zen | Code quality, suggestions |
| Performance | Bolt, Tuner | Optimization |
| UX/Design | Palette, Muse, Flow | Visual improvements |
| Documentation | Quill, Canvas | Content generation |

### Detailed Overlap Checklist

For each existing agent, check:

```yaml
OVERLAP_CHECKLIST:
  functional:
    - Does new agent perform same action?
    - Does new agent take same input?
    - Does new agent produce same output?

  domain:
    - Does new agent work in same technical area?
    - Does new agent solve same business problem?
    - Does new agent target same codebase sections?

  collaboration:
    - Does new agent fit same chain position?
    - Does new agent have same partners?
    - Does new agent block existing flows?
```

---

## Threshold Guidelines

| Overlap % | Action | Reasoning |
|-----------|--------|-----------|
| 0-10% | Proceed | Clearly differentiated |
| 10-20% | Note | Minor overlap, document differentiation |
| 20-30% | Review | Significant overlap, verify necessity |
| 30-50% | Confirm | User must approve differentiation |
| 50%+ | Reject | Too much overlap, propose alternative |

---

## Common Overlap Scenarios

### Scenario 1: Same Input, Different Output

```yaml
EXAMPLE:
  new_agent: "Validator"
  existing_agent: "Builder"

  same:
    - Takes code as input
    - Analyzes types

  different:
    - Validator: Produces validation report only
    - Builder: Produces production code

  overlap: 25%
  decision: PROCEED with differentiation note
```

### Scenario 2: Same Output, Different Input

```yaml
EXAMPLE:
  new_agent: "APITester"
  existing_agent: "Radar"

  same:
    - Produces test files
    - Improves coverage

  different:
    - APITester: Takes OpenAPI specs
    - Radar: Takes source code

  overlap: 35%
  decision: CONFIRM (explain scope difference)
```

### Scenario 3: Same Domain, Different Aspect

```yaml
EXAMPLE:
  new_agent: "Formatter"
  existing_agent: "Zen"

  same:
    - Improves code quality
    - Modifies source files

  different:
    - Formatter: Only formatting/whitespace
    - Zen: Semantic refactoring

  overlap: 40%
  decision: CONFIRM (Zen can already format)
```

---

## Differentiation Strategies

When overlap is detected, use these strategies to differentiate:

### 1. Scope Narrowing

```yaml
BEFORE:
  new_agent: "Security scanner"
  overlap_with: Sentinel (70%)

AFTER:
  new_agent: "Dependency vulnerability scanner"
  overlap_with: Sentinel (20%)
  differentiation: "Only scans package dependencies, not code"
```

### 2. Input Specialization

```yaml
BEFORE:
  new_agent: "Test generator"
  overlap_with: Radar (60%)

AFTER:
  new_agent: "Property-based test generator"
  overlap_with: Radar (15%)
  differentiation: "Only generates fuzz/property tests"
```

### 3. Output Format Change

```yaml
BEFORE:
  new_agent: "Documentation writer"
  overlap_with: Quill (55%)

AFTER:
  new_agent: "Video tutorial generator"
  overlap_with: Quill (10%)
  differentiation: "Produces video scripts, not text docs"
```

### 4. Target Audience Change

```yaml
BEFORE:
  new_agent: "Code reviewer"
  overlap_with: Judge (65%)

AFTER:
  new_agent: "Junior developer mentor"
  overlap_with: Judge (20%)
  differentiation: "Explains why, not just what to fix"
```

---

## Overlap Report Template

When overlap is detected, generate this report:

```markdown
## Overlap Analysis Report

### New Agent
- **Name:** [Proposed name]
- **Purpose:** [One-line purpose]
- **Category:** [Category]

### Overlapping Agents

| Agent | Overlap % | Overlap Areas |
|-------|-----------|---------------|
| [Agent1] | [X%] | [Areas] |
| [Agent2] | [Y%] | [Areas] |

### Highest Overlap: [Agent] at [X%]

**Shared Capabilities:**
1. [Capability 1]
2. [Capability 2]

**Unique to New Agent:**
1. [Capability A]
2. [Capability B]

**Unique to [Existing Agent]:**
1. [Capability X]
2. [Capability Y]

### Recommendation

[ ] **PROCEED** - Overlap < 30%, clear differentiation
[ ] **CONFIRM** - Overlap 30-50%, user must approve
[ ] **REJECT** - Overlap > 50%, too similar

### Differentiation Statement

[If proceeding, explain how new agent is different]

### Alternative Approaches

1. **Extend existing agent** - Add capabilities to [Agent]
2. **Merge scope** - Combine into [Name]
3. **Narrow focus** - Reduce scope to [Description]
```

---

## Automated Overlap Detection

When implementing overlap detection:

```yaml
DETECTION_ALGORITHM:
  1. Extract new agent capabilities from requirements
  2. Load all existing agent capability lists
  3. For each existing agent:
     a. Calculate capability similarity scores
     b. Sum scores and divide by total
     c. Record overlap percentage
  4. Identify agents with overlap > 20%
  5. If any overlap > 30%:
     - Generate overlap report
     - Trigger ON_AGENT_OVERLAP
  6. Otherwise:
     - Proceed with design
     - Note overlaps > 20% in documentation
```

---

## Exception Cases

### Valid High Overlap Cases

1. **Replacement Agent**: Intentionally replacing deprecated agent
2. **Specialized Version**: Creating domain-specific variant
3. **User Request**: User explicitly wants overlap

### Documentation Required

For approved high-overlap agents:

```markdown
## Overlap Justification

**Overlapping Agent:** [Name]
**Overlap Percentage:** [X%]
**Justification:** [Why this overlap is acceptable]
**Migration Plan:** [If replacing, how to migrate]
```
