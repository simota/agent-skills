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

### BUG Type

```markdown
### Selection Rationale

1. **Scout**: Investigate and identify root cause of the bug
2. **Builder**: Implement fix based on identified cause
3. **Radar**: Verify fix works correctly with no regressions

**Additional considerations:**
- Security-related code → +Sentinel
- Complex impact scope → +Sherpa (pre-decomposition)
```

### FEATURE Type

```markdown
### Selection Rationale

1. **Forge**: Rapidly build prototype of new feature
2. **Builder**: Elevate prototype to production quality
3. **Radar**: Add tests for new feature

**Additional considerations:**
- UI changes involved → +Muse (design tokens)
- Complex feature → +Sherpa (pre-decomposition)
- API addition → +Gateway (API design)
```

### INVESTIGATE Type

```markdown
### Selection Rationale

1. **Lens**: Systematic codebase investigation using 4-layer search architecture

**Additional considerations:**
- Bug-related investigation → Scout (RCA-focused)
- Git history investigation → Trail (commit archaeology)
- Web → mobile native porting design → Port (blueprint, parity matrix, roadmap)
- Pure-native mobile implementation (iOS Swift/SwiftUI, Android Kotlin/Compose) → Native
- Product image acquisition with provenance / license → Haul
- Founder office-hours advisory → Sage (bottleneck + 1-2 week action)
- Incident impact scoping → Triage (first response)
- Visualization of findings → +Canvas
- Implementation after investigation → +Builder
```

### REFACTOR Type

```markdown
### Selection Rationale

1. **Zen**: Code quality improvement, refactoring execution
2. **Radar**: Verify behavior remains unchanged

**Additional considerations:**
- Architecture change → +Atlas
- Large-scale change → +Sherpa (phased execution plan)
```

### SECURITY Type

```markdown
### Selection Rationale

1. **Sentinel**: Vulnerability detection and static analysis
2. **Builder**: Implement security fixes
3. **Radar**: Verify fixes

**Additional considerations:**
- Dynamic testing needed → +Probe
- Auth/authz related → focused review
```

---

## Ambiguous Request Patterns

| Request Pattern | uncertainty_level | Action |
|----------------|-------------------|--------|
| "Fix this bug" | partial | Identify from context, start with Scout |
| "Improve performance" | partial | Select Bolt, confirm target area |
| "Make it better" | ambiguous | MULTI_CANDIDATE_MODE |
| "Something is wrong" | ambiguous | MULTI_CANDIDATE_MODE |
| "Review this" | partial | Select Judge/Zen based on context |
| "Test this" | clear | Select Radar/Voyager based on scope |
| "Does X feature exist?" | clear | Lens (feature discovery) |
| "How does X flow work?" | clear | Lens (flow tracing) |
| "Understand this codebase" | clear | Lens (full onboarding) |
| "Why is X broken?" | clear | Scout (RCA), not Lens |
| "When did X regress?" | clear | Trail (git history) |
| "Web から iOS / Android にネイティブ移植したい" | clear | Port (porting blueprint) |
| "iOS Swift / Android Kotlin で実装したい" | clear | Native (pure-native impl) |
| "React Native / Flutter で実装したい" | clear | out of scope; Forge for prototype |
| "商品画像を SKU で集めたい" | clear | Haul (product image acquisition) |
| "ログイン必要なサイトから商品画像" | clear | Vector → Haul (auth handoff) |
| "office hours 受けたい / 何にフォーカスすべきか" | clear | Sage (founder advisory) |
| "創業者として stuck している" | clear | Sage triage recipe |
| "ピッチ資料をレビューしてほしい" | clear | Sage pitch recipe |

---

## Rally Parallel Escalation

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

### Rally Routing Decision

```
Chain designed by Nexus
    ↓
Check for parallelizable steps
    ├── No parallel steps → Execute sequentially
    ├── Light parallel (< 50 lines/branch) → Nexus _PARALLEL_BRANCHES
    └── Heavy parallel → Check further
         ├── Sherpa produced parallel_group → Rally via SHERPA_TO_RALLY_HANDOFF
         ├── Frontend + Backend split detected → Rally (Frontend/Backend Split)
         ├── Multiple independent features → Rally (Feature Parallel)
         └── Impl + Test + Docs simultaneous → Rally (Code/Test/Docs Triple)
```

### Rally Routing Explanation Template

```markdown
### Selection Rationale

1. **Rally**: Parallel execution of independent implementation tasks
   - Team pattern: [Frontend/Backend Split / Feature Parallel / Specialist Team]
   - Teammates: [count] ([role descriptions])

**Parallel justification:**
- [Why sequential is insufficient]
- [File ownership partitioning]
- [Expected speedup]

**Alternatives:**
- Sequential (Nexus): Simpler but slower
- Nexus _PARALLEL_BRANCHES: Insufficient for this scope
```

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
