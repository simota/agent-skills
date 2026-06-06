# Collaboration Packets

**Purpose:** Handoff formats for Flux's partner agents.
**Read when:** You need to send or receive a handoff to/from another agent.

---

## Contents
- Inbound Handoff Formats (receiving)
- Outbound Handoff Formats (sending)
- Collaboration Patterns
- AUTORUN Templates

---

## Inbound Handoff Formats

### From User (Direct)

```yaml
FLUX_INPUT:
  problem_statement: "[User's problem description]"
  constraints:
    - "[Constraint 1]"
    - "[Constraint 2]"
  work_mode: "DEEP | RAPID | LENS"  # Optional, defaults to DEEP
  specific_frameworks: []  # Optional, user-requested frameworks
  context: "[Additional background]"
```

### From Magi (Deadlocked Deliberation)

```yaml
MAGI_TO_FLUX_HANDOFF:
  source: Magi
  trigger: "Deliberation deadlock — all perspectives share same assumptions"
  decision_context:
    domain: "[Architecture | Trade-off | Go/No-Go | Strategy | Priority]"
    options: "[Options that were evaluated]"
    deadlock_type: "[1-1-1 split | all-same-frame | circular reasoning]"
  logos_frame: "[How Logos framed the problem]"
  pathos_frame: "[How Pathos framed the problem]"
  sophia_frame: "[How Sophia framed the problem]"
  shared_blind_spot: "[What all three perspectives missed]"
  request: "Reframe the problem so Magi can re-deliberate with fresh perspectives"
```

### From Nexus (Complex Problem Routing)

```yaml
_AGENT_CONTEXT:
  Role: Flux
  Task: "[Specific reframing task]"
  Mode: AUTORUN
  Chain: "[Previous agents in chain]"
  Input: "[Handoff from previous agent]"
  Constraints:
    - "[Constraint 1]"
    - "[Constraint 2]"
  Expected_Output: "Reframed problem statements + Insight Matrix"
```

### From Accord (Stakeholder Conflict)

```yaml
ACCORD_TO_FLUX_HANDOFF:
  source: Accord
  trigger: "Stakeholders framing problem from incompatible perspectives"
  stakeholder_frames:
    - stakeholder: "[Role/Name]"
      frame: "[How they see the problem]"
      priority: "[What they value most]"
    - stakeholder: "[Role/Name]"
      frame: "[How they see the problem]"
      priority: "[What they value most]"
  conflict_point: "[Where the frames clash]"
  request: "Find a reframing that encompasses all stakeholder concerns"
```

---

## Outbound Handoff Formats

### To Magi (Reframed Problem → Decision)

```yaml
FLUX_TO_MAGI_HANDOFF:
  source: Flux
  deliverable: "Reframing Package"
  cynefin_domain: "[Clear | Complicated | Complex | Chaotic]"
  original_problem: "[Original problem statement]"
  reframed_statements:
    - id: 1
      label: "[Short label]"
      statement: "[Full reframed problem]"
      novelty: "H/M/L"
      actionability: "H/M/L"
    - id: 2
      label: "[Short label]"
      statement: "[Full reframed problem]"
      novelty: "H/M/L"
      actionability: "H/M/L"
    - id: 3
      label: "[Short label]"
      statement: "[Full reframed problem]"
      novelty: "H/M/L"
      actionability: "H/M/L"
  key_insights:
    - "[Most important insight]"
    - "[Second insight]"
    - "[Third insight]"
  blind_spots:
    - "[Bias or constraint detected]"
  recommendation: "Re-deliberate using reframed statement #[N] as the primary frame"
  suggested_action: "Magi should evaluate options under each reframing"
```

### To Spark (Idea Candidates → Feature Proposals)

```yaml
FLUX_TO_SPARK_HANDOFF:
  source: Flux
  deliverable: "Cross-Domain Insights for Feature Ideation"
  original_problem: "[Original problem]"
  idea_seeds:
    - insight: "[Cross-domain insight]"
      source_domain: "[Domain the analogy came from]"
      framework: "[Bisociation | SCAMPER | TRIZ | Cross-Domain Analogy]"
      potential_feature: "[Rough feature idea]"
      novelty: "H/M/L"
    - insight: "[Another insight]"
      source_domain: "[Domain]"
      framework: "[Framework]"
      potential_feature: "[Rough feature idea]"
      novelty: "H/M/L"
  constraints: "[Any constraints from the original problem]"
  recommendation: "Develop the top [N] seeds into full feature proposals"
```

### To Helm (Strategic Reframe → Scenario Analysis)

```yaml
FLUX_TO_HELM_HANDOFF:
  source: Flux
  deliverable: "Strategic Reframing for Scenario Planning"
  original_strategy_question: "[Original strategic question]"
  reframed_scenarios:
    - label: "[Scenario label]"
      reframing: "[How the strategic question was reframed]"
      implications: "[Strategic implications]"
    - label: "[Scenario label]"
      reframing: "[How the strategic question was reframed]"
      implications: "[Strategic implications]"
  key_assumptions_challenged:
    - "[Assumption 1 and its reversal]"
    - "[Assumption 2 and its reversal]"
  recommendation: "Simulate scenarios based on reframed strategic frames"
```

### To Atlas (Architecture Reconception → Design Review)

```yaml
FLUX_TO_ATLAS_HANDOFF:
  source: Flux
  deliverable: "Architecture Reconception"
  original_architecture_question: "[Original design question]"
  reconceived_approaches:
    - label: "[Approach label]"
      reframing: "[How the design constraint was reframed]"
      architectural_implication: "[What this means for architecture]"
    - label: "[Approach label]"
      reframing: "[How the design constraint was reframed]"
      architectural_implication: "[What this means for architecture]"
  challenged_assumptions:
    - "[Technical assumption and its reversal]"
  recommendation: "Evaluate reconceived approaches via ADR process"
```

### To Lore (Reusable Patterns → Knowledge Curation)

```yaml
FLUX_TO_LORE_HANDOFF:
  source: Flux
  deliverable: "Reusable Thinking Patterns"
  patterns_discovered:
    - pattern: "[Description of the thinking pattern]"
      context: "[Problem type where this pattern was effective]"
      frameworks_used: "[Framework combination]"
      reusability: "H/M/L"
    - pattern: "[Description]"
      context: "[Context]"
      frameworks_used: "[Frameworks]"
      reusability: "H/M/L"
  recommendation: "Catalog for future use when similar problem types arise"
```

---

## Collaboration Patterns

### Pattern A: Thinking Breakthrough

```
User/Magi → Flux → Magi
```

**Flow:**
1. User has a stuck decision, or Magi reaches a 1-1-1 deadlock.
2. Flux receives the problem + existing frames.
3. Flux runs DEEP mode, produces reframed problem statements.
4. Magi re-deliberates using the reframed statements.

**Trigger:** "All perspectives agree on the same thing" or "We keep going in circles."

---

### Pattern B: Innovation Pipeline

```
Researcher → Flux → Spark
```

**Flow:**
1. Researcher provides research findings and user insights.
2. Flux reframes the findings through COMBINE phase (Bisociation, SCAMPER).
3. Spark receives cross-domain idea seeds and develops feature proposals.

**Trigger:** "We have research data but no new feature ideas."

---

### Pattern C: Strategic Reframe

```
Accord → Flux → Helm
```

**Flow:**
1. Accord identifies stakeholder frame conflicts.
2. Flux reframes the strategic question to encompass multiple stakeholder perspectives.
3. Helm simulates scenarios under the reframed strategic frames.

**Trigger:** "Stakeholders can't agree on the strategic direction."

---

### Pattern D: Architecture Rethink

```
Atlas → Flux → Atlas
```

**Flow:**
1. Atlas encounters a design constraint that seems insurmountable.
2. Flux challenges the technical assumptions and reframes the design space.
3. Atlas evaluates the reconceived approaches.

**Trigger:** "The architecture seems impossible under current constraints."

---

## AUTORUN Templates

### Standard AUTORUN Execution

```yaml
_AGENT_CONTEXT:
  Role: Flux
  Task: "Reframe the problem of [description]"
  Mode: AUTORUN
  Chain: "[Previous agents]"
  Input:
    problem_statement: "[Problem]"
    constraints: "[Constraints]"
    work_mode: "DEEP"
  Constraints:
    - "[Time constraint]"
    - "[Scope constraint]"
  Expected_Output: "Reframed problem statements + Insight Matrix + Blind Spot Report"
```

### AUTORUN Response

```yaml
_STEP_COMPLETE:
  Agent: Flux
  Status: SUCCESS
  Output:
    deliverable: "Reframing Package"
    artifact_type: "Reframing Package"
    parameters:
      cynefin_domain: "[Domain]"
      work_mode: "DEEP"
      frameworks_applied: "[List]"
      reframed_statements_count: 5
      blind_spots_detected: 3
      serendipity_injections: 2
  Handoff:
    Format: FLUX_TO_MAGI_HANDOFF
    Content: "[Full handoff]"
  Artifacts:
    - "3-5 reframed problem statements"
    - "Insight Matrix (12 insights)"
    - "Blind Spot Report (3 biases, 2 hidden constraints)"
  Risks:
    - "Reframings may challenge organizational assumptions"
  Next: Magi
  Reason: "Reframed statements ready for multi-perspective deliberation"
```
