# Nexus Routing Explanation Reference

**Purpose:** How to explain routing choices and alternatives clearly.
**Read when:** You need to justify the chosen chain or present multiple candidates.
**See also:** If the request is ambiguous, use `intent-clarification.md` first to resolve intent, then return here to present the chain and alternatives.

## Contents
- ENHANCED_ROUTING Decision Factors
- ROUTING_EXPLANATION Output Format
- MULTI_CANDIDATE_MODE
- Task Type Explanation Templates
- Ambiguous Request Patterns
- Rally Parallel Escalation
- Flow Diagram

Explain the rationale behind agent chain selection and present multiple candidates for ambiguous requests.

---

## ENHANCED_ROUTING Decision Factors

### Additional Decision Factors

| Factor | Values | Impact |
|--------|--------|--------|
| `technical_domain` | frontend / backend / database / security / infra | Add domain-specialist agents |
| `scope_indicators` | single_file / multi_file / architectural | Consider adding Atlas |
| `uncertainty_level` | clear / partial / ambiguous | Trigger MULTI_CANDIDATE_MODE |

### technical_domain Extraction Rules

| Keywords / Patterns | domain |
|---------------------|--------|
| React, Vue, CSS, component, UI | frontend |
| API, server, endpoint, auth | backend |
| DB, SQL, schema, migration | database |
| vulnerability, auth, encryption, CORS | security |
| Docker, Terraform, CI/CD, environment | infra |
| codebase, feature, flow, module, structure | investigation |

### scope_indicators Criteria

| indicator | Condition |
|-----------|-----------|
| `single_file` | Explicitly references one file / small change |
| `multi_file` | Affects multiple files / feature addition |
| `architectural` | Design change / module splitting / large refactor |

### uncertainty_level Criteria

| level | Condition |
|-------|-----------|
| `clear` | Specific task instruction / clear goal |
| `partial` | Partially ambiguous but direction is clear |
| `ambiguous` | Abstract / multiple interpretations / vague requests |

---

## ROUTING_EXPLANATION Output Format

Output the following when selecting an agent chain:

```markdown
## Routing Analysis

**Task Classification**: [BUG / FEATURE / INVESTIGATE / REFACTOR / etc.]
**Technical Domain**: [frontend / backend / investigation / etc.]
**Scope**: [single_file / multi_file / architectural]

### Selected Chain

`[Agent1]` → `[Agent2]` → `[Agent3]`

### Selection Rationale

1. **Primary Agent Selection**
   - [Agent1]: [Why this agent is needed]
   - [Agent2]: [Why this agent is needed]
   - [Agent3]: [Why this agent is needed]

2. **Additional Considerations**
   - [Reason for adding/not adding agents]

### Alternatives

| Option | Chain | Reason Not Selected |
|--------|-------|---------------------|
| A | [Alternative chain] | [Why this was not chosen] |
```

---

## MULTI_CANDIDATE_MODE

Triggered when `uncertainty_level: ambiguous`.

### Trigger Conditions

- Vague instructions ("make it better", "fix it somehow", "improve this")
- Requests that could match multiple task types
- Requests with unclear scope

### Output Format

```markdown
## Multiple Approaches Available

Your request can be interpreted in several ways. Which approach should we take?

| # | Approach | Chain | Description | Recommended |
|---|----------|-------|-------------|-------------|
| 1 | [Approach A] | [Chain A] | [Overview of this approach] | ⭐ |
| 2 | [Approach B] | [Chain B] | [Overview of this approach] | - |
| 3 | [Approach C] | [Chain C] | [Overview of this approach] | - |

### Approach Details

**Approach 1: [Name]**
- Expected work: [Specific tasks]
- Impact scope: [Files/features affected]
- Risk: [Potential risks]

**Approach 2: [Name]**
- Expected work: [Specific tasks]
- Impact scope: [Files/features affected]
- Risk: [Potential risks]

Select a number or provide more specific instructions.
```

---

## Task Type Explanation Templates

One worked template, then a derivation rule — the other task types follow the same shape, so they are
not re-tabled here.

### BUG Type (worked example)

```markdown
### Selection Rationale

1. **Scout**: Investigate and identify root cause of the bug
2. **Builder**: Implement fix based on identified cause
3. **Radar**: Verify fix works correctly with no regressions

**Additional considerations:**
- Security-related code → +Sentinel
- Complex impact scope → +Sherpa (pre-decomposition)
```

### Derivation rule for every other task type

Take the task type's **default chain** and its **Additions** column from `routing-matrix.md`, then:

1. Number the default-chain agents in order; one line each, stating the role bracket the matrix
   assigns it (e.g. `Radar[failing repro test]` → "write the failing repro test").
2. List that row's conditional Additions verbatim under **Additional considerations**, as
   `<trigger> → +<Agent>`.
3. Optional steps in the matrix (marked `?`) stay optional in the explanation — say what makes them
   fire, don't present them as unconditional.

Worked check — FEATURE resolves to `Lens? → Sherpa → Forge? → Builder → Radar → Guardian`
(Lens reuse-scan on existing codebases, Forge only when the approach is unproven), with additions
`+Muse/+Palette` (UI), `+Artisan` (frontend production), `+Matrix` (variant exploration),
`+Flux[reframe]`, `+Riff[expand]`. If a derived explanation disagrees with `routing-matrix.md`, the
matrix wins.

INVESTIGATE has no matrix row of its own; its sibling-routing contrasts (Scout for RCA, Trail for git
history, Port for web→native design, Native for pure-native implementation, Triage for incident
scoping, Sage for founder advisory) live in the table below and in `signal-keywords.md`.

---

## Ambiguous Request Patterns

Rows here carry a verdict **this file owns** (MULTI_CANDIDATE_MODE triggers and sibling-routing
contrasts). Anchors already routed elsewhere are not repeated: keyword → recipe mappings live in
`signal-keywords.md`, and overloaded anchors that need a one-question REDIRECT (`fix this`,
`improve`, `audit`/`review`/`check`, `migrate`, …) live in `intent-clarification.md` §
Overloaded-Anchor REDIRECT.

| Request Pattern | uncertainty_level | Action |
|----------------|-------------------|--------|
| "Make it better" | ambiguous | MULTI_CANDIDATE_MODE |
| "Something is wrong" | ambiguous | MULTI_CANDIDATE_MODE |
| "Test this" | clear | Select Radar/Voyager based on scope |
| "Does X feature exist?" / "How does X flow work?" / "Understand this codebase" | clear | Lens (feature discovery / flow tracing / full onboarding) |
| "Why is X broken?" | clear | Scout (RCA), not Lens |
| "When did X regress?" | clear | Trail (git history) |
| "Implement in React Native / Flutter" | clear | out of scope; Forge for prototype |
| "Want office hours / what should I focus on?" · "Stuck as a founder" · "Please review my pitch deck" | clear | Sage (founder advisory — triage / pitch recipe by phrasing) |

---

## Rally Parallel Escalation

**Source of truth: `agent-chains.md`** § Rally Parallel Escalation Triggers / § Rally Non-Escalation /
§ Rally Parallel Chain Variants. It owns which conditions escalate to Rally, which keep the chain
sequential, and what the parallel chain becomes. Only the routing-side decision factor lives here.

### Additional Decision Factor

| Factor | Values | Impact |
|--------|--------|--------|
| `parallelizability` | none / light / heavy | Determine Rally escalation |

### Parallelizability Assessment

| Level | Condition | Action |
|-------|-----------|--------|
| `none` | Single domain, sequential dependencies | Standard chain (no Rally) |
| `light` | 2-3 small independent branches (< 50 lines each) | Nexus _PARALLEL_BRANCHES (internal) |
| `heavy` | 2+ domains, 4+ files, real implementation work | Escalate to Rally |

When the level resolves to `heavy`, pick the team pattern from `agent-chains.md` and explain the
choice with the standard Selection Rationale shape: Rally + team pattern + teammate count, a parallel
justification (why sequential is insufficient, how file ownership partitions, expected speedup), and
the two alternatives it beats (sequential Nexus; `_PARALLEL_BRANCHES`, insufficient at this scope).

---

## Flow Diagram

```
User Request
    ↓
┌─────────────────────────────┐
│ Extract Decision Factors    │
│ - task_type                 │
│ - technical_domain          │
│ - scope_indicators          │
│ - uncertainty_level         │
│ - parallelizability         │
└─────────────────────────────┘
    ↓
uncertainty_level?
    ├─ clear → Direct chain selection
    ├─ partial → Chain selection + confirmation points
    └─ ambiguous → MULTI_CANDIDATE_MODE triggered
         ↓
parallelizability?
    ├─ none → Sequential execution
    ├─ light → Nexus _PARALLEL_BRANCHES
    └─ heavy → Rally escalation
         ↓
ROUTING_EXPLANATION output
```
