# Knowledge Synthesis — Pattern Extraction Methodology

Purpose: Read this file when harvesting journals, clustering similar insights, deduplicating candidates, resolving contradictions, or producing the Lore synthesis report.

## Contents

- Harvest protocol
- Clustering algorithm
- Relationship tracking
- Deduplication protocol
- Confidence scoring
- Contradiction resolution
- Synthesis report output

How Lore harvests, clusters, deduplicates, and scores patterns from agent journals.

---

## Harvest Protocol

### Source Priority

| Source | Priority | Frequency | Content Type |
|--------|----------|-----------|--------------|
| `.agents/triage.md` | High | After every incident | Incident patterns, detection gaps, mitigation insights |
| `.agents/mend.md` | High | After every remediation | Fix patterns, rollback incidents, verification insights |
| `.agents/builder.md` | High | Weekly | Implementation patterns, API pitfalls, DDD insights |
| `.agents/scout.md` | Medium | Weekly | Bug root cause patterns, investigation techniques |
| `.agents/beacon.md` | Medium | Weekly | Observability insights, SLO patterns |
| `.agents/architect.md` | Medium | Monthly | Design patterns, overlap discoveries |
| `.agents/darwin.md` | Medium | Monthly | Evolution insights, ecosystem health patterns |
| `.agents/PROJECT.md` | Low | Weekly | Activity trends, agent utilization |
| Other agent journals | Low | Monthly | Domain-specific insights |

### Extraction Rules

1. **Read the full journal entry** — never extract from partial context
2. **Identify the core insight** — what was learned that is generalizable?
3. **Extract supporting evidence** — dates, metrics, outcomes
4. **Note the context** — project type, technology stack, scale
5. **Check for prior art** — does this reinforce or contradict existing patterns?

---

## Clustering Algorithm

### Step 1: Semantic Grouping

Group extracted insights by similarity:

```
For each new insight:
  1. Compare against existing METAPATTERNS entries
  2. Calculate semantic similarity (topic + domain + outcome)
  3. If similarity ≥ 80%: cluster with existing pattern
  4. If similarity 50-79%: flag as potential variant
  5. If similarity < 50%: mark as new candidate
```

### Step 2: Cross-Agent Correlation

Look for the same insight appearing across multiple agents:

| Correlation | Significance |
|-------------|-------------|
| Same insight from 2+ agents in same domain | Reinforced domain pattern |
| Same insight from 2+ agents across domains | Cross-cutting pattern (high value) |
| Contradictory insights from different agents | Conflict requiring resolution |
| Agent A's problem = Agent B's solution | Handoff optimization opportunity |

### Step 3: Temporal Analysis

Track pattern evolution over time:

- **Emerging**: First appeared recently, limited evidence
- **Growing**: Evidence increasing, appearing in more contexts
- **Stable**: Consistent evidence over extended period
- **Declining**: Evidence frequency dropping, may be becoming obsolete

---

## Relationship Tracking

Patterns stored as flat entries miss deeper insights. Explicit inter-pattern links improve contradiction detection, reveal systemic issues, and surface emergent knowledge.

<!-- Refs: "A-MEM: Agentic Memory for LLM Agents" (arXiv 2502.12110, 2025); "Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers" (arXiv 2603.07670, 2026); "Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects" (arXiv 2512.12818) -->

### 2026 Memory-Architecture Framing

Recent surveys formalise agent memory as a **write → manage → read** loop and group implementations into five mechanism families. Lore is opinionated about which family does the work at which phase:

| Mechanism family | Phase Lore uses it in | Implementation in this skill |
|------------------|------------------------|------------------------------|
| Context-resident compression | Read (propagation) | `Headline / Summary / Full` compression tiers (`propagation-protocol.md`) |
| Retrieval-augmented stores | Read | `METAPATTERNS.md` + per-agent journal lookup keyed by pattern ID |
| Reflective self-improvement | Manage | Synthesis cycle below + Contradiction Resolution; removing reflection caused Generative Agents to degenerate within 48 simulated hours, so this phase is non-skippable |
| Hierarchical virtual context | Write | Domain × Type × Confidence × Scope taxonomy (`pattern-taxonomy.md`) |
| Policy-learned management | Manage | Confidence modifiers + LEARN safety rules; promotions require evidence diversity, not raw count |

The lifecycle separates into **Formation → Evolution → Retrieval**. Harvest + Clustering populate Formation; Confidence Scoring + Contradiction Resolution + Decay Detection drive Evolution; Propagation owns Retrieval. Skipping any phase produces the same failure mode the surveys document: shallow snapshots that look healthy structurally but cannot inform agent behaviour.

### Link Types

| Link Type | Notation | Meaning | Example |
|-----------|----------|---------|---------|
| **Reinforces** | `→reinforces→` | Pattern A provides additional evidence for Pattern B | INFRA-SUCCESS-003 →reinforces→ INFRA-HEURISTIC-007 |
| **Contradicts** | `→contradicts→` | Pattern A conflicts with Pattern B in some context | APP-SUCCESS-012 →contradicts→ APP-HEURISTIC-005 |
| **Specializes** | `→specializes→` | Pattern A is a domain-specific case of broader Pattern B | SECURITY-ANTI-002 →specializes→ APP-ANTI-009 |
| **Generalizes** | `→generalizes→` | Pattern A is a broader version of Pattern B | META-HEURISTIC-001 →generalizes→ PROCESS-SUCCESS-004 |

### Relationship Maintenance Protocol

1. **On registration**: When adding a new pattern, scan existing patterns in the same domain for potential links. Check cross-domain patterns with similarity ≥ 60%.
2. **On reinforcement**: When updating evidence, check if the new evidence also reinforces or contradicts linked patterns.
3. **On contradiction detection**: Automatically create a `→contradicts→` link between the conflicting patterns.
4. **On archival**: When archiving a pattern, review its links — if a `→generalizes→` target is archived, check if the specialized pattern should also be flagged.

### Recording Links in METAPATTERNS.md

Extend the existing `**Related:**` field with typed links:

```markdown
**Related:**
- →reinforces→ INFRA-HEURISTIC-007 (rolling restart effectiveness)
- →contradicts→ APP-SUCCESS-012 (when scale > 10k RPS)
- →specializes→ APP-ANTI-009 (security-specific case)
```

### Relationship-Driven Insights

During synthesis, actively look for:
- **Contradiction clusters**: 3+ patterns with mutual `→contradicts→` links indicate a domain with unclear best practices — escalate to Architect
- **Reinforcement chains**: A→B→C reinforcement chains indicate foundational knowledge — consider promoting the root pattern
- **Orphan patterns**: Patterns with zero relationships after 90 days may be too narrow or poorly classified

---

## Deduplication Protocol

Before registering a new pattern, check:

| Check | If True | Action |
|-------|---------|--------|
| Exact match in catalog | Already registered | Update evidence count + last_validated |
| Partial match (same root cause, different symptoms) | Variant exists | Add as variant to existing pattern |
| Same symptoms, different root cause | Different pattern | Register separately, link as related |
| Superseded by broader pattern | Subsumed | Archive and reference from parent pattern |

### Merge Rules

When merging insights into an existing pattern:
1. Preserve all unique evidence instances
2. Update confidence level based on new evidence count
3. Expand consumer list if new agents are relevant
4. Update last_validated timestamp
5. Note any new context (project type, scale, etc.)

---

## Confidence Scoring

### Evidence-Based Scoring

| Level | Evidence Count | Label | Trust |
|-------|---------------|-------|-------|
| 1 | 1 instance | **Anecdote** | Low — single observation, may be coincidence |
| 2 | 2 instances | **Emerging** | Low-Medium — possible pattern, needs validation |
| 3-5 | 3-5 instances | **Pattern** | Medium — reliable enough to propagate |
| 6-10 | 6-10 instances | **Established** | High — proven across multiple contexts |
| 11+ | 11+ instances | **Foundational** | Very High — core ecosystem knowledge |

### Confidence Modifiers

| Factor | Effect | Example |
|--------|--------|---------|
| Cross-agent corroboration | +1 level | Builder and Artisan both report same API pattern |
| Diverse project types | +1 level | Pattern holds across SaaS, CLI, and E-commerce |
| Contradiction exists | -1 level | Conflicting evidence from another agent |
| Single project context | -1 level | Only observed in one project |
| Recent evidence (< 30 days) | +0 (no modifier) | Freshness is tracked separately |
| Stale evidence (> 180 days) | -1 level | Pattern may be outdated |

### Promotion Criteria

A pattern is promoted to the next confidence level when:
1. New evidence instance from a different context (not just same project repeated)
2. No active contradictions at time of promotion
3. Last evidence instance is within 90 days (freshness requirement)

---

## Contradiction Resolution

When conflicting insights are discovered:

### Resolution Protocol

1. **Document both sides** — preserve both perspectives with full evidence
2. **Identify the variable** — what differs between contexts? (scale, domain, tech stack)
3. **Classify the contradiction**:
   - **Context-dependent**: Both are correct in their respective contexts → Create conditional pattern
   - **Temporal**: Older insight superseded by newer knowledge → Archive old, promote new
   - **Genuine conflict**: Fundamentally incompatible → Escalate to relevant domain agents
4. **Register resolution** with reasoning in pattern entry

### Conditional Pattern Format

```markdown
**Pattern:** [Description]
**When [context A]:** [Approach A] — Evidence: [sources]
**When [context B]:** [Approach B] — Evidence: [sources]
**Deciding factor:** [What determines which context applies]
```

---

## Output: Synthesis Report

After each synthesis cycle, produce:

```markdown
## Lore Synthesis Report — [YYYY-MM-DD]

### Journals Scanned
| Agent | Entries Processed | New Insights | Updated Patterns |
|-------|-------------------|-------------|------------------|

### New Patterns Registered
| Pattern ID | Title | Confidence | Consumers |
|------------|-------|------------|-----------|

### Patterns Reinforced
| Pattern ID | Previous Confidence | New Confidence | New Evidence |
|------------|--------------------|----|------|

### Contradictions Detected
| Pattern ID | Conflicting Source | Resolution Status |
|------------|-------------------|-------------------|

### Decay Alerts
| Pattern ID | State | Days Since Last Evidence | Recommended Action |
|------------|-------|------------------------|-------------------|
```
