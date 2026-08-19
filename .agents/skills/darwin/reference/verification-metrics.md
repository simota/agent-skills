# Verification Metrics

Defines how Darwin verifies that evolution actions produced positive results.

> **2026-05 verification-stack baseline**
> - **Hybrid eval is the consensus default**: Anthropic's coding/agent evaluation guidance (2026) recommends combining **unit tests for correctness** with **LLM rubrics for quality** ("readable / efficient / secure"). Darwin's VERIFY phase mirrors this: hard metrics (EFS delta, RS delta, chain success rate) plus rubric judgments (clarity of HANDOFF artifacts, justification quality of evolution proposals). Source: `https://medium.com/@vinodkrane/chapter-8-agent-evaluation-for-llms-how-to-test-tools-trajectories-and-llm-as-judge-788f6f3e0d52`.
> - **Outcomes contract**: when an agent is evaluated against an Anthropic *Outcomes* rubric (Claude Managed Agents, public beta from 2026-05-06), record the rubric ID + measured pass/fail in the VERIFY table. Anthropic reports a **+10 pp** task-success ceiling lift vs. plain prompting loops (+8.4 pp docx, +10.1 pp pptx in internal benchmarks). Use this as the reference effect-size when validating Darwin-proposed rubric changes. Source: `https://claude.com/blog/new-in-claude-managed-agents`.
> - **Agent-as-a-Judge** (arXiv 2508.02994): when evaluating a chain rather than a single output, prefer an *agent* judge (tool-use, memory, multi-step reasoning) over a static LLM judge. Pair with **Krippendorff's α** (AdaRubric framework) as the inter-rater reliability gate before promoting a new rubric into the VERIFY suite.
> - **Guard against benchmark gaming**: the 2026 evaluation literature flags benchmark-gaming as an active failure mode. When Darwin's VERIFY shows EFS lift, cross-check whether the lift came from genuine outcome wins (delivery, regression-free) or from rubric exploitation. Cap rubric-only lifts at +0.5 EFS until corroborated by ≥7 days of production trace.

---

## VERIFY Phase Protocol

After every EVOLVE phase, Darwin runs verification to ensure evolution actions did not harm the ecosystem.

### Verification Criteria

| Criterion | Threshold | Check Method |
|-----------|-----------|--------------|
| EFS non-regression | EFS did not drop after action | Compare current EFS with pre-action EFS |
| RS consistency | RS changes correlate with usage | Cross-reference RS delta with PROJECT.md usage |
| Override relevance | AFFINITY overrides improve routing | Track routing decisions with/without overrides |
| Sunset validation | Sunset candidates confirmed by Void | Void YAGNI verification completed |
| Pattern adoption | Synthesized patterns referenced | Search journal entries for Pattern Card IDs |

### Timing

- **Immediate check** (same session): Verify data integrity and format correctness
- **Short-term check** (7 days): Verify no EFS regression
- **Medium-term check** (30 days): Verify trend improvements
- **Long-term check** (90 days): Verify overall ecosystem health trajectory

---

## EFS Time-Series Comparison

### Format

```markdown
### EFS Trend

| Date | EFS | Grade | Coverage | Coherence | Activity | Quality | Adaptability | Trigger |
|------|-----|-------|----------|-----------|----------|---------|-------------|---------|
| 2026-02-19 | 72 | B | 80 | 65 | 70 | 75 | 68 | Initial |
| 2026-02-12 | 68 | C | 75 | 62 | 65 | 72 | 65 | ET-01 |
| 2026-02-05 | 70 | B | 78 | 60 | 68 | 74 | 66 | Check |
```

### Regression Detection

```
If EFS[current] - EFS[previous] < -5:
  REGRESSION_DETECTED
  Actions:
    1. Identify which dimensions dropped
    2. Correlate with recent evolution actions
    3. Recommend rollback if action was causal
    4. Flag in ECOSYSTEM.md for next review
```

### Trend Analysis

```
trend = linear_regression(last 5 EFS readings)

If slope > +1.0/check: IMPROVING — evolution is working
If -1.0 ≤ slope ≤ +1.0: STABLE — no significant change
If slope < -1.0/check: DECLINING — investigate and adjust
```

---

## Evolution Action Effectiveness

Each evolution action type has specific verification criteria:

### Dynamic AFFINITY Override Verification

```
Success criteria:
  - Routing decisions align with overrides (check next 5 Nexus invocations)
  - Override agents are actually invoked for relevant tasks
  - No increase in chain failures involving overridden agents

Failure indicators:
  - Overridden agents still not being used
  - Chain failures increase post-override
  - User manually bypasses overridden routing
```

### Journal Synthesis Verification

```
Success criteria:
  - Pattern Cards referenced in subsequent journal entries
  - Discovery Briefs acknowledged by target agents
  - Repeated patterns decrease (synthesis prevented recurrence)

Failure indicators:
  - Pattern Cards never referenced after creation
  - Same patterns continue to emerge in new journals
  - Target agents dismiss all briefs
```

### Sunset Recommendation Verification

```
Success criteria:
  - Void confirms YAGNI assessment
  - Retired agent not missed (no manual workarounds appear)
  - EFS does not drop post-retirement

Failure indicators:
  - Void rejects sunset recommendation
  - Users manually perform tasks the retired agent handled
  - Coverage dimension of EFS drops
```

**2026 sunset window standard:** mirror the public-cloud/API deprecation cadence — a **6–18 month window** is the 2026 industry default (Microsoft Foundry programmatically sets GA-model retirement 18 months out at launch; Theneo's 2026 deprecation guide cites 6–18 months as the disruption-minimizing range). For Darwin's ecosystem-internal sunsets, the recommended cadence is:

| Stage | Timing | Action |
|---|---|---|
| Announce | T−90 days | Mark agent `status: deprecated` in catalog, document successor |
| Reminder | T−30 days | Alias forwarding live, dependents enumerated, migration brief in ECOSYSTEM.md |
| Final notice | T−7 days | Replay historical traffic against successor; confirm zero RS dependents |
| Retire | T0 | Move SKILL.md to archive scope; preserve alias for 30 more days as graceful degradation |

Skipping any of the three pre-retirement notices invalidates Sunset verification. Source: `https://www.theneo.io/blog/managing-api-changes-strategies`, `https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-retirements`.

### Phase Transition Response Verification

```
Success criteria:
  - Agent mix shifts within 2 invocations of transition
  - New dominant agents are actually invoked
  - Transition recorded in ECOSYSTEM.md

Failure indicators:
  - Agent mix unchanged despite phase transition
  - Previous-phase agents still dominating
  - Routing conflicts increase
```

---

## Rollback Protocol

### When to Rollback

Rollback is warranted when:
1. EFS drops >5 points within 7 days of an evolution action
2. Multiple chain failures trace to a specific evolution action
3. User explicitly requests reversal

### Rollback Procedures

| Action Type | Rollback Method |
|-------------|----------------|
| AFFINITY override | Remove override row from ECOSYSTEM.md |
| Pattern Card | Mark as `confidence: LOW` or remove from discoveries |
| Sunset recommendation | Re-activate agent, restore RS to pre-sunset level |
| Phase transition | Revert to previous phase if confidence was borderline |

### Rollback Record

```markdown
### Rollback Log

| Date | Original Action | Reason | Rollback Method | EFS Before | EFS After |
|------|----------------|--------|-----------------|------------|-----------|
| 2026-02-19 | AFFINITY: Bolt → H | Chain failures +3 | Removed override | 68 | 72 |
```

---

## Dashboard Output Format

The VERIFY phase produces a verification summary appended to the DARWIN_REPORT:

```markdown
### Verification Summary

**Previous EFS**: [XX] → **Current EFS**: [XX] ([↑↓→])
**Actions verified**: [N] of [M]
**Regressions detected**: [N]
**Rollbacks required**: [N]

| Action | Date | Status | Evidence |
|--------|------|--------|----------|
| AFFINITY recalc | 2026-02-19 | ✅ Verified | Routing improved for 3 chains |
| Journal synthesis | 2026-02-15 | ⏳ Pending | 30-day check on 2026-03-17 |
| Sunset: AgentX | 2026-02-10 | ❌ Regressed | Coverage dropped 8 points |
```
