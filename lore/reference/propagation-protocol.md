# Propagation Protocol — Knowledge Distribution

Purpose: Read this file when choosing consumers, urgency, message shape, compression level, or feedback collection for propagated knowledge.

## Contents

- Propagation triggers
- Consumer relevance matrix
- Insight delivery formats
- Negative knowledge prioritization
- Context compression
- Feedback loop
- Propagation schedule
- Knowledge gaps report

How Lore distributes insights to consuming agents effectively.

---

## Propagation Triggers

| Trigger | Action | Urgency |
|---------|--------|---------|
| New pattern registered (Confidence ≥ Pattern) | Notify relevant consumers | Normal |
| Pattern promoted to Established/Foundational | Broadcast to all consumers | Normal |
| Contradiction detected | Alert affected agents | High |
| Decay alert (pattern going STALE) | Notify consumers + source agents | Low |
| Anti-pattern discovered | Immediately notify affected agents | High |
| Cross-agent pattern discovered | Notify Architect + Darwin | Normal |

---

## Consumer Relevance Matrix

### Primary Consumers (Always notify)

| Consumer | Relevant Patterns | Why |
|----------|------------------|-----|
| **Architect** | META-*, DESIGN-*, any ECOSYSTEM scope | Informs new agent design and existing agent improvement |
| **Darwin** | META-*, usage trends, staleness signals | Informs ecosystem evolution proposals |
| **Nexus** | PROCESS-*, chain effectiveness patterns | Informs routing matrix optimization |

### Domain Consumers (Notify when domain matches)

| Consumer | Relevant Domains | Example |
|----------|-----------------|---------|
| **Builder** | APP-SUCCESS, APP-ANTI, APP-HEURISTIC | "Validate API responses at integration boundary" |
| **Artisan** | UX-SUCCESS, UX-ANTI, APP-TRADEOFF | "Server Components reduce hydration bugs" |
| **Mend** | INFRA-SUCCESS, INFRA-FAILURE, APP-FAILURE | New remediation pattern candidates |
| **Triage** | INFRA-FAILURE, APP-FAILURE, PROCESS-* | Recurring incident patterns |
| **Sentinel** | SECURITY-* | Security anti-patterns, vulnerability patterns |
| **Radar** | TEST-* | Testing best practices, coverage patterns |
| **Beacon** | PERF-*, INFRA-HEURISTIC | Observability insights, SLO patterns |
| **Gear** | INFRA-SUCCESS, INFRA-ANTI | CI/CD and infrastructure patterns |

### Meta Consumers (Notify for ecosystem patterns)

| Consumer | Relevant Patterns | Why |
|----------|------------------|-----|
| **Sigil** | CROSS scope patterns, PROJECT_AFFINITY matches | Project-specific skill optimization |
| **Judge** | PROCESS-*, quality-related patterns | PDCA cycle improvements |
| **Grove** | DESIGN-*, naming/convention patterns | Cultural drift detection input |

---

## Insight Delivery Format

### Standard Insight Notification

```markdown
## LORE_INSIGHT: [Pattern ID]

**To:** [Consumer Agent]
**Relevance:** [1-2 sentences on why this matters to the consumer]
**Pattern:** [Clear description]
**Confidence:** [Level] ([N] evidence instances)
**Evidence highlights:**
- [Most relevant evidence for this consumer]
- [Second most relevant]
**Recommended action:** [Specific, actionable suggestion for the consumer]
**Full details:** METAPATTERNS.md → [Pattern ID]
```

### Anti-Pattern Alert (Urgent)

```markdown
## LORE_ALERT: [Pattern ID]

**To:** [Consumer Agent]
**Type:** Anti-pattern / Contradiction
**Impact:** [What could go wrong if ignored]
**Pattern:** [Description of what to avoid]
**Evidence:** [Key evidence]
**Instead:** [What to do instead]
**Confidence:** [Level]
```

---

## Negative Knowledge Prioritization

Failure patterns and anti-patterns are the most valuable institutional memory — they prevent repeated mistakes. Research shows organizations disproportionately forget "what doesn't work," leading to wasted effort.

<!-- Ref: "The Real Reason AI Research Keeps Repeating Itself" (ACM, 2024), "Anti-Patterns in Multi-Agent Gen AI Solutions" (Medium, 2025) -->

### Priority Boost Rules

| Pattern Type | Priority Modifier | Rationale |
|-------------|------------------|-----------|
| `FAILURE` | +2 urgency levels | Failures are forgotten fastest; early propagation prevents repetition |
| `ANTI` | +2 urgency levels | Anti-patterns save the most effort when caught early |
| `TRADEOFF` | +1 urgency level | Trade-off awareness prevents one-sided decisions |
| `SUCCESS` | +0 (baseline) | Successes are naturally retained through practice |
| `HEURISTIC` | +0 (baseline) | Rules of thumb are useful but not urgent |

### Negative Knowledge Preservation Protocol

1. **Tag explicitly**: All FAILURE and ANTI patterns include a `**What went wrong:**` field with concrete consequences
2. **Lower confidence threshold for propagation**: Propagate FAILURE/ANTI patterns at Emerging (2) confidence, not Pattern (3+)
3. **Extend freshness**: FAILURE/ANTI patterns use 1.5× TTL multiplier for decay — negative lessons stay relevant longer
4. **Require explicit deprecation**: FAILURE/ANTI patterns cannot be auto-archived by time alone; require manual review

---

## Context Compression for Propagation

Each token added to a consuming agent's context reduces its effective attention budget. Knowledge propagation must be compact to maximize uptake.

<!-- Refs: "Effective context engineering for AI agents" (Anthropic, 2025); "Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers" (arXiv 2603.07670, 2026) -->

### Why Compression Cost Matters in 2026

Long-context-window models (1M+ tokens) make it tempting to dump full evidence trails into every consumer prompt. Empirically that **degrades** uptake: 2026 agent-memory surveys show that retrieval-augmented stores (which is what Lore essentially is, from a consumer perspective) outperform context-resident dumps on tasks that require acting on the knowledge rather than just citing it. Compression is not a cost-saving measure — it is a quality measure.

### Tiered Detail Levels

| Tier | Max Length | When to Use | Format |
|------|----------|-------------|--------|
| **Headline** | 1 line (≤ 100 chars) | Weekly digest, low-relevance consumers | `[ID]: [one-sentence pattern]` |
| **Summary** | 3-5 lines | Standard propagation, domain consumers | Pattern + confidence + recommended action |
| **Full** | Unlimited | On-request, high-impact patterns, contradictions | Complete METAPATTERNS entry with all evidence |

### Consumer-Type Compression Rules

| Consumer Type | Default Tier | Upgrade Trigger |
|--------------|-------------|-----------------|
| Primary (Architect, Darwin, Nexus) | Summary | Ecosystem-wide pattern → Full |
| Domain (Builder, Mend, etc.) | Headline | Direct domain match → Summary |
| Meta (Sigil, Judge, Grove) | Headline | Cross-agent scope → Summary |

### Compact Context Guidelines

- **Lead with action**: Start every insight with what the consumer should DO, not background
- **Evidence by reference**: Cite `METAPATTERNS.md → [ID]` instead of inlining full evidence lists
- **One insight per message**: Never batch multiple unrelated patterns in a single propagation
- **Omit redundant fields**: Skip confidence/scope if consumer already knows the context

---

## Feedback Loop

After propagation, Lore tracks effectiveness:

### Feedback Collection

| Signal | Meaning | Action |
|--------|---------|--------|
| Consumer references pattern in journal | Pattern was useful | +1 reinforcement |
| Consumer contradicts pattern in journal | Pattern may be wrong | Flag as CONTESTED |
| Consumer ignores pattern (no reference in 90 days) | Pattern may be irrelevant | Review consumer relevance |
| Consumer requests more detail | Pattern description insufficient | Expand evidence/context |

### Propagation Effectiveness Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Uptake rate** | ≥ 60% | Patterns referenced by consumers / patterns propagated |
| **Relevance accuracy** | ≥ 80% | Useful patterns / total propagated (per consumer) |
| **Contradiction rate** | < 10% | Contested patterns / total patterns |
| **Decay prevention** | ≥ 70% | Patterns kept FRESH or CURRENT / total patterns |
| **Recall-on-action rate** | ≥ 50% | Times a consumer journal cites the pattern when applying it / total recommended-action propagations |

The `Recall-on-action rate` is the consumer-impact answer to the 2026 survey question "did retrieval actually change behaviour, or did the pattern just live in the catalog?" Treat it as the single most important effectiveness signal — Uptake measures touch, Recall-on-action measures change.

---

## Propagation Schedule

| Frequency | Activity |
|-----------|----------|
| **Per-event** | Anti-pattern alerts, contradiction alerts |
| **Weekly** | Digest of new patterns + reinforced patterns to primary consumers |
| **Monthly** | Full synthesis report to Architect + Darwin |
| **Quarterly** | Ecosystem knowledge health report (coverage, freshness, gaps) |

---

## Knowledge Gaps Report

When Lore detects areas with sparse pattern coverage:

```markdown
## Knowledge Gap Report — [YYYY-MM-DD]

### Under-documented Domains
| Domain | Pattern Count | Last New Pattern | Assessment |
|--------|--------------|-----------------|------------|
| [Domain] | [N] | [date] | Sparse — needs attention |

### Under-sourced Agents
| Agent | Journal Entries | Insights Extracted | Assessment |
|-------|----------------|-------------------|------------|
| [Agent] | [N] | [M] | Low yield — journal may need enrichment |

### Recommended Actions
1. [Action to address gap 1]
2. [Action to address gap 2]
```
