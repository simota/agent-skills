# Pattern Taxonomy — Classification System

Purpose: Read this file when assigning pattern dimensions, generating IDs, structuring `METAPATTERNS.md`, or deciding lifecycle state transitions.

## Contents

- 4-dimension classification
- Pattern ID convention
- `METAPATTERNS.md` full schema
- Pattern lifecycle

How Lore classifies, names, and structures patterns in METAPATTERNS.md.

---

## 4-Dimension Classification

Every pattern is tagged along 4 orthogonal dimensions:

### Dimension 1: Domain

| Domain Code | Description | Example Sources |
|-------------|-------------|-----------------|
| `INFRA` | Infrastructure, deployment, CI/CD, containers | Gear, Scaffold, Pipe, Mend |
| `APP` | Application logic, business rules, data models | Builder, Schema, Gateway |
| `TEST` | Testing strategies, coverage, quality assurance | Radar, Voyager, Siege |
| `DESIGN` | Architecture, patterns, code structure | Atlas, Zen, Grove, Architect |
| `PROCESS` | Workflows, collaboration, decision making | Nexus, Sherpa, Magi, Judge |
| `SECURITY` | Vulnerabilities, hardening, compliance | Sentinel, Probe, Canon |
| `PERF` | Performance, optimization, capacity | Bolt, Tuner, Beacon |
| `UX` | User experience, design, accessibility | Palette, Flow, Prose, Echo |
| `META` | Ecosystem-level patterns, agent interactions | Darwin, Architect, Lore |

### Dimension 2: Type

| Type Code | Description | Example |
|-----------|-------------|---------|
| `SUCCESS` | Proven approach that reliably works | "Rolling restart resolves memory leaks in 90% of cases" |
| `FAILURE` | Known approach that doesn't work in context | "Increasing timeout masks upstream issues" |
| `ANTI` | Common mistake to avoid | "Alerting on causes instead of symptoms" |
| `TRADEOFF` | Decision with inherent tension | "Consistency vs availability in distributed cache" |
| `HEURISTIC` | Rule of thumb, not absolute truth | "If error rate > 2x baseline within 10min of deploy, rollback" |

### Dimension 3: Confidence

| Level | Code | Evidence Count | Trust Level |
|-------|------|---------------|-------------|
| 1 | `ANECDOTE` | 1 | Low |
| 2 | `EMERGING` | 2 | Low-Medium |
| 3-5 | `PATTERN` | 3-5 | Medium |
| 6-10 | `ESTABLISHED` | 6-10 | High |
| 11+ | `FOUNDATIONAL` | 11+ | Very High |

### Dimension 4: Scope

| Scope Code | Description | Propagation |
|------------|-------------|-------------|
| `AGENT` | Relevant to a single agent's domain | Direct to that agent |
| `CROSS` | Relevant across 2-5 agents | Propagate to all relevant |
| `ECOSYSTEM` | Relevant to the entire ecosystem | Broadcast to Architect/Darwin/Nexus |

---

## Pattern ID Convention

```
[DOMAIN]-[TYPE]-[NNN]

Examples:
  INFRA-SUCCESS-001: "Rolling restart resolves gradual memory leaks"
  APP-ANTI-003: "Catching generic exceptions hides real errors"
  PROCESS-HEURISTIC-012: "Chain length > 5 agents correlates with lower success rate"
  META-TRADEOFF-002: "Agent specialization vs ecosystem complexity"
```

---

## METAPATTERNS.md Full Schema

### File Header

```markdown
# METAPATTERNS — Ecosystem Knowledge Catalog

Last updated: [YYYY-MM-DD]
Total patterns: [N]
Confidence distribution: [N] Foundational / [N] Established / [N] Pattern / [N] Emerging / [N] Anecdote

---
```

### Pattern Entry

```markdown
## [PATTERN_ID]: [Title]

| Field | Value |
|-------|-------|
| **Domain** | [DOMAIN code] |
| **Type** | [TYPE code] |
| **Confidence** | [CONFIDENCE level] ([N] evidence) |
| **Scope** | [SCOPE code] |
| **Consumers** | [Agent1, Agent2, ...] |
| **Created** | [YYYY-MM-DD] |
| **Last validated** | [YYYY-MM-DD] |
| **Freshness** | [FRESH/CURRENT/AGING/STALE] |

**Pattern:** [Clear, actionable 1-3 sentence description]

**Evidence:**
1. [Agent] ([YYYY-MM-DD]): [What was observed, in what context]
2. [Agent] ([YYYY-MM-DD]): [What was observed, in what context]
3. [Agent] ([YYYY-MM-DD]): [What was observed, in what context]

**Implication:** [What consuming agents should do with this knowledge]

**Anti-pattern:** [What NOT to do, if applicable]

**Related:** [PATTERN_ID_1], [PATTERN_ID_2] (if any)

---
```

### Index Section

At the end of METAPATTERNS.md, maintain an index:

```markdown
## Index

### By Domain
- INFRA: [ID1], [ID2], ...
- APP: [ID3], [ID4], ...

### By Confidence (Highest First)
- FOUNDATIONAL: [ID1], [ID2], ...
- ESTABLISHED: [ID3], [ID4], ...

### By Freshness (Stalest First)
- STALE: [ID1], [ID2], ...
- AGING: [ID3], [ID4], ...
```

---

## Pattern Lifecycle

```
CANDIDATE → REGISTERED → REINFORCED → PROMOTED → ... → AGING → ARCHIVED
                ↓                                         ↓
           CONTESTED → RESOLVED / SPLIT / SUPERSEDED    REMOVED
```

| State | Trigger | Action |
|-------|---------|--------|
| **CANDIDATE** | New insight extracted, not yet validated | Hold for additional evidence |
| **REGISTERED** | First evidence + context documented | Added to METAPATTERNS.md as Anecdote |
| **REINFORCED** | Additional evidence adds to existing | Update evidence list + confidence |
| **PROMOTED** | Confidence threshold crossed | Update level label |
| **CONTESTED** | Contradictory evidence found | Document both sides, seek resolution |
| **AGING** | No new evidence for 90+ days | Flag for review |
| **ARCHIVED** | Superseded or no longer applicable | Move to archive section |
| **REMOVED** | Evidence invalidated | Delete from catalog |
