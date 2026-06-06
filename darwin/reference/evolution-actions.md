# Evolution Actions

Defines the 8 evolution triggers, Dynamic AFFINITY calculation, and Discovery Propagation brief format.

> **2026-05 industry signals to monitor as evolution evidence**
> - **Anthropic Claude Managed Agents** (announced 2026-05-06 at *Code w/ Claude*, SF): four production-grade features now usable as Darwin's own evolution primitives — **Outcomes** (public beta; rubric-driven success criteria, measured +up to 10 percentage-point task-success lift vs. standard prompting loop, +8.4 pp on docx and +10.1 pp on pptx in Anthropic's internal benchmarks), **Webhooks** (HTTP callback on agent completion), **Multiagent Orchestration** (public beta; lead-agent decomposition), and **Dreaming** (research preview; between-session memory consolidation that extracts patterns from past sessions to reduce repeated mistakes). Treat *Outcomes* rubrics as the new external standard for Darwin's "expected impact" field on evolution proposals, and treat *Dreaming* as the upstream prior art for Pattern Card synthesis (ET-04). Source: `https://claude.com/blog/new-in-claude-managed-agents`.
> - **Microsoft Agent Framework 1.0 GA (2026-04-03)**: production-ready convergence of Semantic Kernel + AutoGen with MCP and A2A protocol support, sequential / concurrent / handoff / group-chat / Magentic-One orchestration patterns. Semantic Kernel and the legacy AutoGen line are now in maintenance mode (security/bug fixes only). When Darwin sees `semantic_kernel` or pre-AG2 `autogen` imports during ASSESS, flag the agent for **ET-10 (framework end-of-life drift)** below. Source: `https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/`.
> - **LangGraph 1.0 GA (2025-10-22)**: no breaking changes from late 0.x, battle-tested at Uber/LinkedIn/Klarna. New durable-agent contract treated as the stable baseline for Coherence scoring on graph-based ecosystems. Source: `https://changelog.langchain.com/announcements/langgraph-1-0-is-now-generally-available`.
> - **AG2 0.12.0 (2026-04-17)** (formerly AutoGen): on the path to v1.0 with `autogen.beta` subpackage maturing through 0.13 → 0.14 → 1.0. Source: `https://github.com/ag2ai/ag2/releases`.
> - **CrewAI Cognitive Memory** (2026): five-op model — **encode, consolidate, recall, extract, forget** — over a hierarchical scope tree (paths like `/project/alpha`, `/agent/field/findings`). Darwin's Journal Synthesizer (ET-04) should map Pattern Cards onto the closest CrewAI scope when the deployed framework is CrewAI ≥ 1.x. Source: `https://crewai.com/blog/how-we-built-cognitive-memory-for-agentic-systems`.

---

## Evolution Triggers

### ET-01: Phase Transition

**Condition:** Lifecycle phase changed from previous check.

**Detection:**
```
current_phase ≠ stored_phase AND current_confidence ≥ 0.60
```

**Action:** Recalculate Dynamic AFFINITY overrides for all agents based on new phase.

**Priority:** HIGH — affects all subsequent routing decisions.

**Output:** Updated AFFINITY override table in ECOSYSTEM.md.

### ET-02: Quality Plateau

**Condition:** UQS has not changed significantly for 3+ consecutive Judge cycles.

**Detection:**
```
abs(uqs[cycle_n] - uqs[cycle_n-3]) < 5% of uqs[cycle_n-3]
```

**Action:** Initiate improvement chain: Judge → Architect for ecosystem-level quality review.

**Priority:** MEDIUM — systemic quality issue, not urgent.

**Output:** Improvement proposal with specific agents or patterns to enhance.

### ET-03: Agent Dormancy

**Condition:** An agent has not been invoked for 30+ days.

**Detection:**
```
days_since_last_use(agent) > 30
```

**Action:** Re-evaluate RS for the dormant agent. If RS < 40, flag in Staleness Report.

**Priority:** LOW — dormancy may be expected based on lifecycle phase.

**Output:** Updated RS for affected agent, potential staleness flag.

### ET-04: Journal Pattern Accumulation

**Condition:** 5+ unintegrated reusable patterns exist across agent journals.

**Detection:**
```
count(journal_entries WHERE reusable = true AND NOT in ECOSYSTEM.md discoveries) >= 5
```

**Action:** Launch Journal Synthesizer to cluster and extract Pattern Cards.

**Priority:** MEDIUM — knowledge is being lost without synthesis.

**Output:** New Pattern Cards added to ECOSYSTEM.md Cross-Agent Discoveries.

### ET-05: EFS Emergency Drop

**Condition:** EFS has dropped 10+ points from the previous baseline.

**Detection:**
```
previous_efs - current_efs >= 10
```

**Action:** Emergency ecosystem analysis — identify which dimensions dropped and why.

**Priority:** CRITICAL — ecosystem health is degrading rapidly.

**Output:** Emergency DARWIN_REPORT with root cause analysis and immediate action recommendations.

### ET-06: Repeated Feedback Pattern

**Condition:** 2+ high-priority Reverse Feedback entries share the same pattern.

**Detection:**
```
count(feedback WHERE priority = HIGH AND pattern_cluster = same) >= 2
```

**Action:** Launch Discovery Propagator to create briefs for affected agents.

**Priority:** HIGH — recurring issues indicate systemic problem.

**Output:** Discovery Briefs distributed to relevant agents.

### ET-07: Commit Velocity Anomaly

**Condition:** Commit velocity has changed by more than 2 standard deviations from the 30-day mean.

**Detection:**
```
abs(current_velocity - mean_30d) > 2 × stddev_30d
```

**Action:** Re-run lifecycle detection. Significant velocity changes often signal phase transitions.

**Priority:** MEDIUM — may indicate phase transition or project event.

**Output:** Updated lifecycle detection with new confidence levels.

### ET-08: Culture Drift

**Condition:** Grove DNA score has shifted by more than 0.5 from the last recorded value.

**Detection:**
```
abs(current_dna_score - stored_dna_score) > 0.5
```

**Action:** Culture profile resync — update AFFINITY overrides to reflect changed conventions.

**Priority:** MEDIUM — convention changes affect agent behavior expectations.

**Output:** Updated culture alignment notes in ECOSYSTEM.md, potential AFFINITY adjustments.

### ET-10: Framework End-of-Life Drift

> ET-09 (Official Spec Conformance Drift / OSC) is defined separately in `reference/official-fitness-criteria.md`. ET-10 covers external framework/model EOL rather than internal SKILL.md spec drift.

**Condition:** An agent's underlying framework dependency has entered maintenance mode or has a published retirement date.

**Detection:**
```
agent.framework IN {
  "semantic-kernel" (maintenance from 2026-04-03),
  "autogen<0.12" (superseded by AG2 ≥ 0.12 on 2026-04-17),
  "openai.assistants" (API retired 2026-08-26),
  "gpt-4o" (API retired 2026-03-31)
}
OR
azure_foundry_model.retirement_date - today < 90 days
OR
agent_uses_model_at_or_past_provider_announced_eol
```

**Action:** Propose migration plan via Shift (`radar` + `detect` + `framework`/`lang` recipes — technology lifecycle + migration orchestration; modernization absorbed from horizon). Cite the official retirement date and the recommended successor stack (Microsoft Agent Framework 1.0 GA for SK/AutoGen, AG2 ≥ 0.12 for AutoGen, latest Claude/GPT API for retired models). Apply Microsoft Foundry's industry-standard **18-month deprecation window** (set programmatically at GA launch) as the upper bound for staged migration: communicate at **T−90 / T−30 / T−7 days** before the framework EOL date, mirroring 2026 API-deprecation best practice (Theneo, 2026).

**Priority:** HIGH — unmaintained framework drift compounds with model drift (~40% of production agent failures).

**Output:** Migration brief in ECOSYSTEM.md with successor stack, target date, and rollback posture. Sources: `https://devblogs.microsoft.com/agent-framework/migrate-your-semantic-kernel-and-autogen-projects-to-microsoft-agent-framework-release-candidate/`, `https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements`, `https://www.theneo.io/blog/managing-api-changes-strategies`.

---

## Trigger Evaluation Order

When multiple triggers fire simultaneously:

```
1. ET-05 (CRITICAL) — Always first
2. ET-01 (HIGH) — Phase changes affect everything
3. ET-06 (HIGH) — Recurring feedback needs immediate attention
4. ET-10 (HIGH) — Framework EOL drift (2026-05): SK/AutoGen → Microsoft Agent Framework 1.0,
                  legacy AutoGen → AG2 ≥ 0.12, retired model APIs
5. ET-07 (MEDIUM) — May cascade to ET-01
6. ET-02 (MEDIUM) — Quality plateau
7. ET-04 (MEDIUM) — Knowledge synthesis
8. ET-08 (MEDIUM) — Culture drift
9. ET-09 (MEDIUM) — Official Spec Conformance drift (see `official-fitness-criteria.md`)
10. ET-03 (LOW) — Dormancy check
```

> ET-10 outranks ET-07/ET-02 because unmaintained framework drift silently inflates *all* downstream failure categories in MAST (Spec 41.8% / Coordination 36.9% / Verification 21.3%) once vendor support stops.

---

## Dynamic AFFINITY Calculation

### Formula

```
Dynamic_AFFINITY(agent) = base_affinity × 0.40 + phase_affinity × 0.30 + usage_modifier × 0.20 + feedback_modifier × 0.10
```

### Components

| Component | Source | Range |
|-----------|--------|-------|
| base_affinity | PROJECT_AFFINITY.md (H=1.0, M=0.5, —=0.1) | 0.0-1.0 |
| phase_affinity | Phase Affinity Table (see assessment-models.md) | 0.0-1.0 |
| usage_modifier | Normalized usage in last 30 days | 0.0-1.0 |
| feedback_modifier | Positive feedback ratio | 0.0-1.0 |

### Override Rules

Dynamic AFFINITY overrides are stored in ECOSYSTEM.md:

```markdown
### Dynamic Affinity Override

| Agent | Base | Override | Reason | Date |
|-------|------|---------|--------|------|
| Bolt | M | H | SCALING phase, performance focus | 2026-02-19 |
| Growth | H | M | STABILIZATION phase, reduced marketing need | 2026-02-19 |
```

**Application by Nexus:**
1. Nexus reads `.agents/ECOSYSTEM.md` Dynamic Affinity Override section
2. For agents with overrides, use override value instead of base affinity
3. Override expires after 90 days if not refreshed by Darwin
4. Manual overrides by user always take precedence

---

## Journal Synthesis

### Pattern Card Format

```markdown
#### PC-[NNN]: [Pattern Title]

- **Source agents**: [agent1, agent2, ...]
- **First observed**: YYYY-MM-DD
- **Frequency**: [N] occurrences across [M] agents
- **Insight**: [What was discovered]
- **Apply when**: [Future scenario where this pattern is relevant]
- **Confidence**: HIGH/MEDIUM/LOW
- **Related patterns**: PC-[XXX], PC-[YYY]
```

### Clustering Algorithm

```
1. Scan all .agents/*.md files for entries with:
   - Explicit `reusable: true` tag
   - Keywords: "pattern", "always", "never", "whenever", "insight"
   - Repeated similar findings across multiple agents
2. Group entries by semantic similarity:
   - Same file/module referenced
   - Same problem type (performance, quality, security, etc.)
   - Same solution approach
3. For each cluster with 2+ entries:
   - Generate Pattern Card
   - Assign confidence based on source diversity and frequency
4. Store new Pattern Cards in ECOSYSTEM.md Cross-Agent Discoveries
```

---

## Discovery Propagation

### Brief Format

```markdown
## DISCOVERY_BRIEF

**ID**: DB-[NNN]
**Source**: [agent name]
**Date**: YYYY-MM-DD
**Finding**: [What was discovered — 1-2 sentences]
**Evidence**: [Specific journal entry or feedback reference]
**Relevant to**: [list of target agent names]
**Recommended action**: [What target agents should consider — 1-2 sentences]
**Priority**: HIGH / MEDIUM / LOW
**Status**: PENDING / ACKNOWLEDGED / APPLIED / DISMISSED
```

### Propagation Rules

1. A discovery is propagated when:
   - It affects agent behavior or output quality
   - It applies to agents beyond the original source
   - It has supporting evidence (not speculation)

2. Target agent selection:
   - Agents that share input/output with the source agent
   - Agents that handle the same task types
   - Agents specified in collaboration patterns

3. Brief lifecycle:
   - PENDING: Brief created, not yet reviewed
   - ACKNOWLEDGED: Target agent has read the brief
   - APPLIED: Target agent has incorporated the finding
   - DISMISSED: Finding determined not relevant (with reason)

---

## Evolution Action Log Format

Each evolution action is recorded in ECOSYSTEM.md:

```markdown
| Date | Trigger | Action | Agents Affected | Outcome | Verified |
|------|---------|--------|-----------------|---------|----------|
| 2026-02-19 | ET-01 | AFFINITY recalculated | All | Updated 8 overrides | Pending |
| 2026-02-15 | ET-04 | Journal synthesis | Scout, Builder, Radar | 3 Pattern Cards created | Yes |
```
