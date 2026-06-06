# Creative Thinking Framework

**Purpose:** Divergent exploration framework and value-first ideation method.
**Read when:** You are still deciding what should be built.

## Contents
- Architect's Uniqueness
- 3-Dimensional Thinking Model
- Dimension Details
- INSIGHT Generation
- ENVISION Phase
- Value-First Design
- Creative Session Workflow
- Anti-Patterns in Creative Thinking
- Integration with SKILL.md

---

## Architect's Uniqueness

> **"The only agent that tackles questions without answers"**

Other agents know "what to build."
Only Architect asks "what should be built."

| Agent | Question | Nature |
|-------|----------|--------|
| Builder | How to implement this spec? | Convergent |
| Radar | How to test this code? | Convergent |
| **Architect** | What agent is needed? | **Divergent** |

---

## 3-Dimensional Thinking Model

```
                    HEIGHT
                Perspective/Abstraction
                         ↑
                         │
                    ┌────┴────┐
                    │ INSIGHT │
                    └────┬────┘
                   ╱     │     ╲
       BREADTH ←─────────┼─────────→ DEPTH
     (Cross-domain)              (Essence)
```

Creative discoveries emerge at the "INSIGHT" point where all three dimensions intersect.

---

## Dimension Details

### HEIGHT: Perspective & Abstraction

**Core**: Step back to see the whole, adopt a meta-perspective

| Question | Purpose |
|----------|---------|
| "What if...?" | Challenge assumptions, explore alternatives |
| "Describe the essence in 3 words?" | Identify what's truly important |
| "Where will this agent be in 2 years?" | Evaluate with long-term perspective |
| "What if this problem was 10x larger?" | Discover scalability challenges |

**Thinking Techniques**:
- **Abstraction**: Generalize specific requirements
- **Bird's eye view**: See individual problems in system-wide context
- **Time axis**: Distinguish short-term solutions from long-term impact

**Height Questions (Perspective Exploration)**:
```yaml
HEIGHT_QUESTIONS:
  - "What larger problem is this agent's problem a part of?"
  - "If this agent didn't exist, what would users use instead?"
  - "What is this agent's position in the current ecosystem?"
  - "Will this be valuable in 5 years? What risks obsolescence?"
```

---

### BREADTH: Cross-Domain Connection

**Core**: Connect different domains, discover patterns

| Question | Purpose |
|----------|---------|
| "What else...?" | Explore related problems and solutions |
| "What similar patterns exist in other fields?" | Leverage knowledge from other domains |
| "Who are the hidden stakeholders?" | Discover overlooked parties |
| "Can this solution apply to other problems?" | Evaluate reusability |

**Thinking Techniques**:
- **Analogy**: Discover similarities across different domains
- **Combination**: Combine existing elements in new ways
- **Pattern recognition**: Extract common structures from multiple cases

**Breadth Questions (Cross-domain Exploration)**:
```yaml
BREADTH_QUESTIONS:
  - "How do other domains (healthcare, finance, gaming) solve similar challenges?"
  - "Which existing agents take a similar approach?"
  - "What agents would have synergy when combined with this one?"
  - "How do competitors or OSS satisfy this need?"
```

---

### DEPTH: Essence & Root Cause

**Core**: Dig beneath the surface to find root causes and essential value

| Question | Purpose |
|----------|---------|
| "Why really...?" | Reveal true motivation and purpose |
| "Why? (×5 times)" | Reach the root cause |
| "What does the user truly want?" | Discover true needs behind surface requests |
| "If this fails, what would be the cause?" | Anticipate potential risks |

**Thinking Techniques**:
- **5 Whys**: Repeat "Why?" five times to reach root cause
- **First Principles**: Decompose assumptions, rebuild from fundamentals
- **Inversion**: Think from "conditions for failure" instead of success

**Depth Questions (Essential Exploration)**:
```yaml
DEPTH_QUESTIONS:
  - "What is the real reason for wanting to create this agent?"
  - "What's the difference between what users say and what they actually want?"
  - "What is the root cause of this problem? Are we only treating symptoms?"
  - "If there were no constraints, what would the ideal solution be?"
```

---

## INSIGHT Generation

Creative insights emerge when all three dimensions intersect.

```
HEIGHT × BREADTH = System-wide pattern discovery
HEIGHT × DEPTH   = Essential value redefinition
BREADTH × DEPTH  = New solution discovery
HEIGHT × BREADTH × DEPTH = Innovative agent design
```

### Insight Synthesis

```yaml
INSIGHT_SYNTHESIS:
  pattern: |
    Integrate results from all three dimensions to identify:

    1. CORE INSIGHT
       - The most important discovery from 3D exploration
       - Points overlooked by existing approaches

    2. UNIQUE VALUE
       - Value only this agent can provide
       - Essential difference from the existing ecosystem

    3. DESIGN PRINCIPLES
       - Concrete design guidelines derived from insights
       - Rules that guarantee success if followed
```

---

## ENVISION Phase

Add **ENVISION** phase to the existing framework:

```
UNDERSTAND → ENVISION → ANALYZE → DESIGN → GENERATE → VALIDATE
              ↑ NEW
              Creative Thinking
```

### ENVISION Phase Structure

```yaml
ENVISION_PHASE:
  duration: "20-30% of total process"
  purpose: "Design truly valuable agents through creative exploration"

  steps:
    1_height_exploration:
      name: "Perspective Exploration"
      questions: HEIGHT_QUESTIONS
      output: "Position within the system"

    2_breadth_exploration:
      name: "Cross-domain Exploration"
      questions: BREADTH_QUESTIONS
      output: "Similar patterns and differentiation points"

# ...
```

### ENVISION Session Template

```markdown
## ENVISION Session: [Proposed Agent Name]

### 1. HEIGHT (Perspective)
- **Position in the system**:
- **Long-term value**:
- **Scalability**:
- **Alternatives**:

### 2. BREADTH (Cross-domain)
- **Solutions in similar domains**:
- **Similar points in ecosystem**:
- **Combination possibilities**:
- **External solution comparison**:

### 3. DEPTH (Essence)
...
```

---

## Value-First Design

Clarify value before filling templates.

### 3 Essential Questions

| Question | Purpose | Example |
|----------|---------|---------|
| **World Comparison** | World without vs with this agent | "30-minute manual task completes in 5 minutes" |
| **Primary Beneficiary** | Who benefits most? | "Team leaders struggling with weekly reports" |
| **Success Metric** | How to measure success? | "Task completion rate exceeds 80%" |

### Value-First Checklist

```yaml
VALUE_FIRST_CHECKLIST:
  world_comparison:
    without_agent: "[Describe current pain/inefficiency specifically]"
    with_agent: "[Describe improved state specifically]"
    delta: "[Quantitative improvement]"

  primary_beneficiary:
    persona: "[Who uses it]"
    pain_point: "[Their biggest pain]"
    frequency: "[How often they encounter this problem]"

  success_metric:
    primary: "[Main success indicator]"
    measurement: "[How to measure]"
    target: "[Target value]"
```

### Value Statement Template

```markdown
## Value Statement: [Agent Name]

### World Comparison
**Without this agent:**
[Specific current problem/pain]

**With this agent:**
[Specific improved state]

**Improvement:**
[Quantitative improvement (time, quality, cost, etc.)]

### Primary Beneficiary
**Who:** [Persona]
**Pain:** [Biggest pain]
...
```

---

## Creative Session Workflow

### Full Creative Session (New Agent Design)

```yaml
FULL_CREATIVE_SESSION:
  total_time: "60-90 minutes equivalent"

  phases:
    1_framing:
      duration: "10%"
      activities:
        - "Organize requirements"
        - "Set initial hypothesis"
      output: "Problem Statement"

    2_envision:
      duration: "30%"
      activities:
        - "Height Questions"
# ...
```

### Quick Creative Session (Improvement/Small Design)

```yaml
QUICK_CREATIVE_SESSION:
  total_time: "15-30 minutes equivalent"

  phases:
    1_quick_envision:
      duration: "40%"
      activities:
        - "1 Height Question"
        - "1 Breadth Question"
        - "1 Depth Question"
      output: "Quick Insight"

    2_value_check:
      duration: "20%"
      activities:
# ...
```

---

## Anti-Patterns in Creative Thinking

### Thinking Patterns to Avoid

| Anti-Pattern | Symptom | Countermeasure |
|--------------|---------|----------------|
| **Solution-First** | Starting with "let's use this tool" | Return to problem definition |
| **Feature-Creep** | Adding more and more features | Focus with Value-First Checklist |
| **Copy-Paste Design** | Copying existing agent | Go through ENVISION Phase |
| **Premature Optimization** | Aiming for perfection from the start | MVP thinking, start minimal |
| **Echo Chamber** | Only confirming own hypothesis | Deliberately seek opposing views |

### Creative Thinking Checklist

Verify before design:

```markdown
## Creative Thinking Checklist

- [ ] Did I understand the problem before considering solutions?
- [ ] Did I explore all 3 dimensions (HEIGHT/BREADTH/DEPTH)?
- [ ] Did I answer the Value-First 3 questions?
- [ ] Did I consider the "don't build" option?
- [ ] Did I verify this can't be solved by extending existing agents?
```

---

## Integration with SKILL.md

Reference in SKILL.md:

```markdown
## ENVISION Phase

Creative thinking phase. See `reference/creative-thinking.md` for details.

**3-Dimensional Thinking**:
- HEIGHT: Perspective & Abstraction
- BREADTH: Cross-domain Connection
- DEPTH: Essence & Root Cause

**Required Checks**:
- [ ] Value-First Checklist completed
- [ ] ENVISION Session conducted
- [ ] Insight synthesis completed
```
