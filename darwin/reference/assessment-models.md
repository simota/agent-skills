# Assessment Models

Defines the calculation formulas and algorithms for Ecosystem Fitness Score (EFS), Relevance Score (RS), and lifecycle phase detection.

> **2026-05 baseline notes**
> - Failure attribution defaults: when grading Coherence and Quality, anchor on the **MAST taxonomy** (Cemri et al., ICLR 2026 — 1,600 traces across 7 frameworks, 14 failure modes, Cohen's Kappa = 0.88). Distribution: **Specification & System Design 41.8%, Inter-Agent Misalignment / Coordination 36.9%, Task Verification & Termination 21.3%**. Use these weights when allocating root-cause budget across EFS dimensions.
> - Trace-level error amplification by topology (Towards Data Science, 2026): **SAS = 1.0× baseline, Centralized = 4.4×, Hybrid = 5.1×, Decentralized = 7.8×, Independent = 17.2×**. Independent (i.e. "bag of agents" without orchestrator) is the only architecture above the 10× cliff — penalize EFS Coherence accordingly.
> - LangChain *State of Agent Engineering* (survey conducted Nov–Dec 2025, published 2025): 57% of surveyed orgs run agents in production; **32% cite quality as the top deployment barrier**. Use as the external benchmark when calibrating Quality dimension scoring. Source: `https://www.langchain.com/state-of-agent-engineering`.
> - Sources: `https://arxiv.org/abs/2503.13657` (MAST paper), `https://openreview.net/forum?id=wM521FqPvI` (ICLR 2026 proceedings), `https://towardsdatascience.com/why-your-multi-agent-system-is-failing-escaping-the-17x-error-trap-of-the-bag-of-agents/`.

---

## Ecosystem Fitness Score (EFS)

### Formula

```
EFS = Coverage × 0.25 + Coherence × 0.20 + Activity × 0.20 + Quality × 0.20 + Adaptability × 0.15
```

### Dimension Definitions

#### Coverage (25%)

Measures whether the agent ecosystem covers the project's actual needs.

```
Coverage = (matched_needs / total_needs) × 100

Where:
  total_needs = count of task types that occurred in last 90 days
  matched_needs = count of task types with an appropriate agent invoked
```

**Scoring guide:**
- 100: Every task type in last 90 days had a matching agent invoked
- 80: Most task types covered, 1-2 gaps filled by manual work
- 60: Several gaps; common tasks lack dedicated agents
- 40: Significant coverage gaps; many tasks done without agent support
- 20: Minimal agent usage relative to project needs

**Data sources:** Routing matrix vs PROJECT.md task types, lifecycle phase dominant agents vs actual usage.

#### Coherence (20%)

Measures how well agents work together in chains and handoffs.

```
Coherence = (successful_chains / total_chains) × 0.6 + (avg_handoff_quality) × 0.4

Where:
  successful_chains = chains that completed without error or rollback
  total_chains = all chains attempted in last 90 days
  avg_handoff_quality = mean quality of NEXUS_HANDOFF artifacts (0.0-1.0)
```

**Scoring guide:**
- 100: All chains complete successfully, handoffs are clean and informative
- 80: Occasional chain adjustments, handoffs generally good
- 60: Regular chain failures requiring recovery, some handoff quality issues
- 40: Frequent failures, poor handoff quality, agents stepping on each other
- 20: Chains rarely complete, severe handoff problems

**Data sources:** Nexus execution logs, NEXUS_HANDOFF quality assessment, error/recovery entries.

**Topology-aware adjustment (2026-05):** Cap Coherence at 60 when the deployed topology is *Independent* (no central orchestrator) because measured trace-level error amplification is 17.2× the single-agent baseline, well above the 10× regression cliff. Centralized (4.4×) and Hybrid (5.1×) topologies remain eligible for the full 0–100 range. Source: Towards Data Science, "Why Your Multi-Agent System is Failing" (2026).

#### Activity (20%)

Measures whether the ecosystem is actively used.

```
Activity = unique_agents_30d × 0.4 + invocation_rate × 0.3 + journal_freshness × 0.3

Where:
  unique_agents_30d = (unique agents used in 30 days / total available agents) × 100
  invocation_rate = normalized invocations per week (target: project-size dependent)
  journal_freshness = (agents with journal entries in 30 days / agents used in 30 days) × 100
```

**Scoring guide:**
- 100: Diverse agent usage, high invocation rate, fresh journals
- 80: Good variety, regular usage, most journals updated
- 60: Moderate usage, some agents neglected
- 40: Low diversity, sporadic invocations, stale journals
- 20: Minimal agent usage, ecosystem largely dormant

**Data sources:** PROJECT.md row counts, agent journal dates, unique agent counts.

#### Quality (20%)

Measures whether agent outputs are improving over time.

```
Quality = uqs_trend × 0.4 + feedback_ratio × 0.3 + health_score × 0.3

Where:
  uqs_trend = direction of UQS over last 3 cycles (improving=100, stable=60, declining=20)
  feedback_ratio = positive Reverse Feedback / total Reverse Feedback × 100
  health_score = latest Architect Health Score (if available, else 50)
```

**Scoring guide:**
- 100: UQS improving, positive feedback dominant, high health score
- 80: UQS stable-good, mostly positive feedback
- 60: UQS plateau, mixed feedback
- 40: UQS declining, negative feedback increasing
- 20: Poor quality indicators across the board

**Data sources:** Judge UQS history, Reverse Feedback entries, Architect Health Score.

#### Adaptability (15%)

Measures how quickly the ecosystem responds to project changes.

```
Adaptability = override_freshness × 0.3 + transition_response × 0.4 + gap_fill_rate × 0.3

Where:
  override_freshness = days since last AFFINITY update (fresher = higher, max at 30 days)
  transition_response = speed of agent mix change after lifecycle transition (faster = higher)
  gap_fill_rate = new agents or skills created to fill identified gaps / total gaps identified
```

**Scoring guide:**
- 100: Rapid adaptation, fresh overrides, all gaps addressed
- 80: Good responsiveness, some lag in adaptation
- 60: Moderate adaptation, overrides somewhat stale
- 40: Slow to adapt, overrides outdated, gaps unaddressed
- 20: No adaptation, ecosystem stuck in previous phase

**Data sources:** ECOSYSTEM.md timestamps, lifecycle transition history, Architect gap analyses.

### EFS Grading

| Grade | Score Range | Interpretation |
|-------|------------|----------------|
| **S** | 95-100 | Exceptional — ecosystem perfectly tuned |
| **A** | 85-94 | Excellent — minor improvements possible |
| **B** | 70-84 | Good — some optimization opportunities |
| **C** | 55-69 | Fair — notable gaps or inefficiencies |
| **D** | 40-54 | Poor — significant evolution needed |
| **F** | 0-39 | Critical — ecosystem not serving the project |

### EFS Trend Indicators

| Symbol | Meaning | Threshold |
|--------|---------|-----------|
| ↑ | Improving | +5 or more from previous |
| → | Stable | Within ±4 of previous |
| ↓ | Declining | -5 or more from previous |

---

## Relevance Score (RS)

### Formula

```
RS = Usage × 0.40 + Affinity_Match × 0.25 + Feedback × 0.20 + Freshness × 0.15
```

### Component Definitions

#### Usage (40%)

```
Usage = (w30 × count_30d + w60 × count_60d + w90 × count_90d) / normalizer

Where:
  w30 = 0.50 (most recent period weighted highest)
  w60 = 0.30
  w90 = 0.20
  count_Xd = number of invocations in last X days
  normalizer = project-dependent (based on total agent invocations)
```

Scale: 0-100, where 100 = top quartile agent by usage.

#### Affinity_Match (25%)

```
Affinity_Match = phase_affinity × 0.60 + type_affinity × 0.40

Where:
  phase_affinity = how well the agent matches the current lifecycle phase (from phase table)
  type_affinity = agent's PROJECT_AFFINITY rating for current project type
```

**Phase Affinity Table:**

| Phase | Dominant Agents (affinity = 1.0) | Supporting (0.6) | Neutral (0.3) |
|-------|----------------------------------|-------------------|----------------|
| GENESIS | Nexus, Forge, Spark, Architect | Builder, Radar, Scout | All others |
| ACTIVE_BUILD | Builder, Forge, Radar, Artisan | Schema, Gateway, Scout | All others |
| STABILIZATION | Judge, Sentinel, Zen, Nexus | Radar, Sweep, Atlas | All others |
| PRODUCTION | Guardian, Beacon, Triage, Gear | Sentinel, Launch, Latch | All others |
| MAINTENANCE | Shift (`detect`/`modernize`/`radar`), Sweep, Trail | Builder, Radar, Scout | All others |
| SCALING | Bolt, Tuner, Scaffold | Beacon, Gear, Stream | All others |
| SUNSET | Sweep, Quill, Morph | Canvas, Trail, Archive | All others |

#### Feedback (20%)

```
Feedback = (positive_count - negative_count × 1.5) / total_feedback × 100

Where:
  positive_count = positive Reverse Feedback entries for this agent
  negative_count = negative Reverse Feedback entries (weighted 1.5× to penalize issues)
  total_feedback = total feedback entries for this agent

  If no feedback exists: Feedback = 50 (neutral default)
```

#### Freshness (15%)

```
Freshness = max(100 - days_since_update × 1.5, 0)

Where:
  days_since_update = min(days_since_skill_update, days_since_journal_entry)
```

Scale: 100 at 0 days, 0 at 67+ days. This encourages regular agent maintenance.

### RS Status Classification

| Status | Score Range | Meaning | Recommended Action |
|--------|-----------|---------|-------------------|
| **Active** | 80-100 | Agent is highly relevant and frequently used | Continue as-is |
| **Stable** | 60-79 | Agent is relevant, usage is adequate | Monitor for trends |
| **Dormant** | 40-59 | Agent is underused relative to its potential | Review affinity match |
| **Declining** | 20-39 | Agent relevance is dropping | Investigate cause, consider improvement |
| **Sunset** | 0-19 | Agent may no longer be needed | Verify with Void, consider retirement |

---

## Lifecycle Detection Algorithm

### Step-by-Step Process

```
1. COLLECT signals (see signal-collection.md)
2. For each phase P in [GENESIS, ACTIVE_BUILD, STABILIZATION, PRODUCTION, MAINTENANCE, SCALING, SUNSET]:
     score[P] = sum(signal_match[P][s] × weight[P][s] for s in signals)
3. Sort phases by score, descending
4. If score[top_phase] >= 0.60:
     detected_phase = top_phase
     confidence = score[top_phase]
5. Else:
     detected_phase = MIXED
     phases = top 2 phases with scores
     confidence = max(scores)
6. Compare detected_phase with previous_phase (from ECOSYSTEM.md)
7. If transition detected:
     Fire ET-01 trigger
     Record transition in history
8. Return {phase, confidence, signals_breakdown, transition}
```

### Confidence Interpretation

| Range | Meaning |
|-------|---------|
| 0.90-1.00 | Very high — clear phase signal |
| 0.75-0.89 | High — dominant phase with some secondary signals |
| 0.60-0.74 | Moderate — phase detected but mixed signals present |
| 0.40-0.59 | Low — mixed phase, report as dual-phase |
| 0.00-0.39 | Very low — insufficient signal, report as UNKNOWN |

### Transition Detection

A phase transition is confirmed when:
1. Detected phase differs from stored phase
2. New phase confidence ≥ 0.60
3. OR new phase has been the top scorer for 2+ consecutive checks

On transition:
- Record in ECOSYSTEM.md transition history: `{from, to, date, confidence}`
- Fire ET-01 trigger (AFFINITY recalculation)
- Log to `.agents/darwin.md` journal
