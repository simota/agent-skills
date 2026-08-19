# Decay Detection — Knowledge Freshness Management

Purpose: Read this file when evaluating freshness, applying domain TTL multipliers, revalidating stale patterns, or deciding archive and resurrection actions.

## Contents

- Freshness states
- Domain-specific freshness policy
- Decay signals
- Audit protocol
- Revalidation protocol
- Archive management
- Health score contribution

How Lore monitors knowledge freshness, detects staleness, and manages the lifecycle of patterns.

---

## Freshness States

| State | Age Since Last Evidence | Indicator | Action |
|-------|----------------------|-----------|--------|
| **FRESH** | < 30 days | Recently validated or reinforced | None — healthy |
| **CURRENT** | 30-90 days | Still relevant, not recently reinforced | Monitor |
| **AGING** | 90-180 days | Risk of becoming stale | Flag for review |
| **STALE** | > 180 days | Likely outdated, no recent evidence | Review + Archive or Revalidate |

### State Transitions

```
FRESH ──(30 days)──→ CURRENT ──(90 days)──→ AGING ──(180 days)──→ STALE
  ↑                      ↑                     ↑                    │
  └── new evidence ───────┴── new evidence ─────┘                    │
                                                              ┌──────┴──────┐
                                                          ARCHIVED      REVALIDATED
                                                          (removed)     (→ FRESH)
```

---

## Domain-Specific Freshness Policy

Knowledge half-life varies significantly by content type. Applying uniform TTL thresholds causes premature archival of stable process patterns and late detection of stale security patterns. Use domain-specific multipliers to adjust the base freshness thresholds.

<!-- Ref: "The Knowledge Decay Problem" (RAG About It, 2025), "Data freshness rot" (Glen Rhodes, 2025) -->

### Domain TTL Multipliers

| Domain | Multiplier | Effective Thresholds (FRESH/CURRENT/AGING/STALE) | Rationale |
|--------|-----------|--------------------------------------------------|-----------|
| `SECURITY` | 0.5× | 15 / 45 / 90 / 90+ days | Threat landscape changes rapidly; patterns go stale fast |
| `INFRA` | 0.75× | 22 / 67 / 135 / 135+ days | Tool versions and cloud APIs evolve frequently |
| `PERF` | 0.75× | 22 / 67 / 135 / 135+ days | Performance characteristics shift with dependencies |
| `APP` | 1.0× | 30 / 90 / 180 / 180+ days | Standard decay rate (baseline) |
| `TEST` | 1.0× | 30 / 90 / 180 / 180+ days | Testing practices evolve at moderate pace |
| `UX` | 1.0× | 30 / 90 / 180 / 180+ days | Design patterns shift with trends |
| `DESIGN` | 1.25× | 37 / 112 / 225 / 225+ days | Architectural patterns are relatively stable |
| `PROCESS` | 1.5× | 45 / 135 / 270 / 270+ days | Workflow patterns change slowly |
| `META` | 1.5× | 45 / 135 / 270 / 270+ days | Ecosystem-level insights have long shelf life |

### Applying Multipliers

When evaluating freshness state for a pattern:

```
effective_threshold = base_threshold × domain_multiplier

Example: SECURITY-ANTI-005, last evidence 50 days ago
  Base CURRENT threshold = 90 days → Effective = 90 × 0.5 = 45 days
  50 > 45 → State = AGING (not CURRENT as base thresholds would indicate)
```

If a pattern spans multiple domains, use the **lowest multiplier** (most aggressive decay) to err on the side of freshness.

---

## Decay Signals

### Primary Signals (Automatic Detection)

| Signal | Detection Method | Severity |
|--------|-----------------|----------|
| **Time-based decay** | `now - last_validated > threshold` | Proportional to age |
| **Source agent deprecated** | Agent removed from BOUNDARIES.md | High |
| **Technology obsolescence** | Referenced tech no longer in project | Medium |
| **Contradicted by newer evidence** | Newer journal entries conflict | High |
| **Zero consumer references** | No consuming agent has referenced pattern | Medium |

### Secondary Signals (Requires Analysis)

| Signal | Detection Method | Severity |
|--------|-----------------|----------|
| **Domain shift** | Project types in ecosystem have changed | Low |
| **Ecosystem restructuring** | Agent boundaries or routing changed significantly | Medium |
| **Confidence deflation** | Modifiers have reduced confidence below registration threshold | Medium |

---

## Audit Protocol

### Scheduled Audit (Monthly)

1. **Scan all patterns** for freshness state
2. **Identify AGING patterns** — add to review queue
3. **Identify STALE patterns** — flag for immediate review
4. **Check for orphaned patterns** — source agents no longer exist
5. **Generate Decay Report**

### Decay Report Format

```markdown
## Knowledge Decay Report — [YYYY-MM-DD]

### Summary
- Total patterns: [N]
- FRESH: [N] ([%])
- CURRENT: [N] ([%])
- AGING: [N] ([%]) — review recommended
- STALE: [N] ([%]) — action required

### STALE Patterns (Action Required)
| Pattern ID | Title | Days Since Evidence | Source Agents | Recommended |
|------------|-------|--------------------|----|---|
| [ID] | [Title] | [N] | [Agents] | Archive / Revalidate / Remove |

### AGING Patterns (Review Recommended)
| Pattern ID | Title | Days Since Evidence | Consumer Activity |
|------------|-------|--------------------|----|
| [ID] | [Title] | [N] | [Last referenced by consumer] |

### Orphaned Patterns
| Pattern ID | Missing Source Agent | Recommended |
|------------|---------------------|-------------|
| [ID] | [Agent name] | Archive with note |
```

---

## Revalidation Protocol

When a STALE or AGING pattern needs revalidation:

### Steps

1. **Check source journals** — has new relevant evidence appeared but was missed?
2. **Check consumer behavior** — are consumers still acting on this pattern?
3. **Check domain relevance** — is the technology/context still in active use?
4. **Decision matrix:**

| Still relevant? | New evidence? | Action |
|----------------|---------------|--------|
| Yes | Yes | Revalidate → FRESH |
| Yes | No | Keep at AGING, note "awaiting evidence" |
| No | — | Archive with reason |
| Uncertain | — | Flag for domain expert review |

### Revalidation Sources

| Approach | Method |
|----------|--------|
| **Active probing** | Ask relevant agents "is this pattern still observed?" via propagation |
| **Passive monitoring** | Watch for new journal entries that reinforce or contradict |
| **Context check** | Verify referenced technologies/tools still in use |

---

## Archive Management

### Archive Criteria

A pattern is archived (not deleted) when:
- STALE for > 180 days AND no consumer references in that period
- Source agent has been removed from ecosystem
- Superseded by a newer, broader pattern
- Technology context no longer exists

### Archive Format

Archived patterns move to an `## Archive` section at the bottom of METAPATTERNS.md:

```markdown
## Archive

### [PATTERN_ID]: [Title] (Archived: [YYYY-MM-DD])
**Reason:** [Why archived]
**Original confidence:** [Level]
**Last evidence:** [YYYY-MM-DD]
**Superseded by:** [New pattern ID, if applicable]
```

### Resurrection

Archived patterns can be restored if:
1. New evidence emerges that revalidates the pattern
2. Technology/context becomes relevant again
3. Consumer explicitly requests restoration

Restore to EMERGING confidence, regardless of original level — must re-earn confidence.

---

## Health Score Contribution

Lore's decay management contributes to Darwin's Ecosystem Fitness Score:

| Metric | Weight | Calculation |
|--------|--------|-------------|
| **Freshness ratio** | 40% | (FRESH + CURRENT) / total_patterns |
| **Contradiction ratio** | 30% | 1 - (contested / total_patterns) |
| **Coverage ratio** | 20% | domains_with_patterns / total_domains |
| **Uptake ratio** | 10% | patterns_referenced_by_consumers / patterns_propagated |

**Knowledge Health Score** = Σ(metric × weight) × 100

| Score | Grade | Interpretation |
|-------|-------|---------------|
| 90-100 | A | Excellent — knowledge is fresh and well-propagated |
| 80-89 | B | Good — minor staleness or gaps |
| 70-79 | C | Fair — significant staleness, review needed |
| 60-69 | D | Poor — many stale patterns, active curation required |
| < 60 | F | Critical — knowledge base is unreliable, major refresh needed |

### Operational Monitoring Metrics

Track these alongside the Health Score to measure consumer-facing impact of decay:

| Metric | Calculation | Alert Threshold |
|--------|-------------|-----------------|
| **Stale retrieval rate** | queries_returning_AGING_or_STALE / total_consumer_queries | > 15% |
| **Propagation lag** | avg(consumer_notification_time − pattern_update_time) | > 24 hours |
| **Reflection latency** | avg(pattern_register_time − evidence_create_time) | > 7 days |
| **Forgetting violation rate** | archived_patterns_resurrected_within_30d / total_archives | > 10% |

These metrics are output-oriented (measuring consumer impact) rather than structural (measuring catalog state). A healthy catalog with high propagation lag still fails consumers.

### Memory-Consolidation Backstop (Dreaming alignment, 2026)

OpenClaw and related 2026 agent-memory work separate ingestion from promotion into three phases — Light (raw capture), REM (reflection / clustering), Deep (commit to long-term memory). Lore's synthesis cycle is the local equivalent and **must not skip the REM-equivalent reflection step**:

- The Light-equivalent step is journal harvest (Builder / Scout / Mend / etc. writing into `.agents/*.md`). Lore reads but does not promote.
- The REM-equivalent step is `knowledge-synthesis.md` clustering + contradiction resolution + confidence scoring.
- Only the Deep-equivalent step — registering a `PATTERN` or higher into `METAPATTERNS.md` — writes to long-term memory.

Generative-Agents-style ablation studies show that removing the reflection phase degrades coherent multi-day planning within ~48 simulated hours. Treat a missed monthly synthesis cycle as an outage, not a backlog. When `Reflection latency` exceeds the threshold above, prioritise running synthesis over expanding the catalog.

### Knowledge-Decay Adversarial Signals

Long-term-memory survey work in 2026 catalogs ways memory stores degrade beyond honest staleness: prompt injection that overwrites entries, poisoning that flips a high-confidence pattern's recommendation, and silent contradiction by adversarial new evidence. Lore is defensive in three concrete ways:

1. **Append-only evidence list** — never delete prior evidence rows; supersede via `Archive` only.
2. **Confidence cannot rise on a single new datapoint** — promotion requires diverse-context evidence per `knowledge-synthesis.md`.
3. **Cross-agent corroboration is mandatory for `ECOSYSTEM` scope** — no single source can promote an ecosystem-wide pattern.

These rules cost throughput but make memory store integrity auditable.
