# Combination Engine

**Purpose:** Rules for dynamically combining frameworks and the Serendipity Injection mechanism.
**Read when:** You are in the COMBINE phase or need to compose a multi-framework pipeline.

---

## Contents
- Framework Compatibility Matrix
- Combination Rules
- Iterative Deepening Pipeline
- Serendipity Injection
- Example Combinations

---

## Framework Compatibility Matrix

Compatibility scores (1-5): how well two frameworks amplify each other.

| | FP | AR | DA | Bi | SC | TR | CA | LT | RF | OS | MD |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **First Principles (FP)** | — | 5 | 4 | 3 | 4 | 5 | 3 | 3 | 4 | 2 | 3 |
| **Assumption Reversal (AR)** | 5 | — | 5 | 4 | 3 | 4 | 3 | 4 | 5 | 3 | 4 |
| **Devil's Advocate (DA)** | 4 | 5 | — | 3 | 2 | 3 | 2 | 3 | 4 | 3 | 5 |
| **Bisociation (Bi)** | 3 | 4 | 3 | — | 4 | 3 | 5 | 5 | 3 | 5 | 3 |
| **SCAMPER (SC)** | 4 | 3 | 2 | 4 | — | 4 | 3 | 3 | 3 | 3 | 2 |
| **TRIZ (TR)** | 5 | 4 | 3 | 3 | 4 | — | 4 | 3 | 3 | 2 | 3 |
| **Cross-Domain (CA)** | 3 | 3 | 2 | 5 | 3 | 4 | — | 4 | 3 | 4 | 2 |
| **Lateral Thinking (LT)** | 3 | 4 | 3 | 5 | 3 | 3 | 4 | — | 4 | 5 | 3 |
| **Reframing (RF)** | 4 | 5 | 4 | 3 | 3 | 3 | 3 | 4 | — | 4 | 4 |
| **Oblique Strategies (OS)** | 2 | 3 | 3 | 5 | 3 | 2 | 4 | 5 | 4 | — | 3 |
| **Multi-Agent Debate (MD)** | 3 | 4 | 5 | 3 | 2 | 3 | 2 | 3 | 4 | 3 | — |

**High-synergy pairs (score 5):**
- First Principles + Assumption Reversal (decompose, then flip)
- First Principles + TRIZ (reduce to fundamentals, then resolve contradictions)
- Assumption Reversal + Devil's Advocate (surface, then attack)
- Assumption Reversal + Reframing (flip assumptions, then reframe the problem)
- Bisociation + Cross-Domain Analogy (two modes of domain crossing)
- Bisociation + Lateral Thinking (both break linear connections)
- Bisociation + Oblique Strategies (random stimulus amplifies bisociation)
- Lateral Thinking + Oblique Strategies (both inject randomness)
- Devil's Advocate + Multi-Agent Debate (structured opposition)

---

## Combination Rules

### Rule 1: Pillar Diversity

Always combine frameworks from at least 2 different pillars (CHALLENGE, COMBINE, SHIFT). Same-pillar-only combinations produce diminishing returns.

**Good:** First Principles (CHALLENGE) + SCAMPER (COMBINE) + Reframing (SHIFT)
**Avoid:** First Principles + Assumption Reversal + Devil's Advocate (all CHALLENGE)

### Rule 2: Synergy Threshold

Prefer combinations where all pairwise compatibility scores ≥ 3. Allow one pair below 3 only if it introduces essential pillar diversity.

### Rule 3: Diminishing Returns

Maximum 5 frameworks per pipeline execution. Beyond 5, cognitive load outweighs additional insight.

| Work Mode | Recommended Count |
|-----------|------------------|
| DEEP | 4-5 frameworks |
| RAPID | 2-3 frameworks |
| LENS | 1 (+ optional companion) |

### Rule 4: Sequential Amplification

Order frameworks so each phase's output enriches the next:

```
CHALLENGE output (exposed assumptions)
    → feeds COMBINE input (assumptions become material for recombination)
        → feeds SHIFT input (combined ideas become material for perspective rotation)
```

### Rule 5: Contradiction Preservation

When frameworks produce contradictory insights, preserve both. Contradictions are often the most valuable output — they reveal genuine tensions in the problem space.

---

## Iterative Deepening Pipeline

Each phase transforms the problem representation:

```
Problem Statement (P₀)
    │
    ├─ CLASSIFY → Domain + Framework Set
    │
    ├─ CHALLENGE → P₁ (assumptions exposed, reversed)
    │     Input: P₀
    │     Output: Assumption Map + reversed problem variants
    │
    ├─ COMBINE → P₂ (cross-domain connections injected)
    │     Input: P₁ + Assumption Map
    │     Output: Bisociated concepts + SCAMPER variants + TRIZ solutions
    │
    ├─ SHIFT → P₃ (perspective rotated)
    │     Input: P₂ + all prior outputs
    │     Output: Reframed problem statements + lateral insights
    │
    └─ CRYSTALLIZE → Final Output
          Input: P₀, P₁, P₂, P₃ + all artifacts
          Output: 3-5 reframed problems + Insight Matrix + Blind Spot Report
```

**Key principle:** P₃ should be recognizably related to P₀ but offer genuinely different angles. If P₃ ≈ P₀, the pipeline hasn't produced sufficient transformation — escalate framework intensity.

---

## Serendipity Injection

### Concept

Deliberate introduction of random stimuli to break cognitive fixation. Applied during COMBINE and SHIFT phases.

### Mechanism

1. **Random Word Injection** (Lateral Thinking → Random Entry)
   - Generate or select a random word unrelated to the problem.
   - Force 3 connections between the word and the problem.
   - Keep the most surprising connection.

2. **Oblique Strategy Draw**
   - Select 1-2 strategies randomly from the Oblique Strategies collection.
   - Apply as constraints or questions to current thinking.
   - Force at least one idea per strategy.

3. **Domain Roulette** (Bisociation)
   - Randomly select an unrelated domain.
   - Map the problem's structure onto that domain.
   - What solution would that domain suggest?

4. **Provocation PO**
   - Construct an intentionally absurd statement about the problem.
   - Extract the useful principle buried in the absurdity.

### When to Inject

| Trigger | Injection Type |
|---------|---------------|
| COMBINE phase starts | Domain Roulette (always) |
| SHIFT phase starts | Oblique Strategy Draw (always) |
| Pipeline feels stuck | Random Word Injection |
| All insights feel predictable | Provocation PO |
| Need to stress-test an insight | Oblique Strategy (constraint) |

### Serendipity Quality Check

After injection, verify:
- [ ] The stimulus produced at least one genuinely unexpected connection.
- [ ] The connection is meaningful, not just word-play.
- [ ] The insight would NOT have emerged from systematic analysis alone.

If all checks fail, inject again with a different mechanism.

---

## Example Combinations

### Complex Domain (User Churn Problem)

```
CLASSIFY: Complex (cause-effect retrospective only, multiple interacting factors)

CHALLENGE:
  - Assumption Reversal (20 assumptions about why users leave)
  - First Principles (what is the irreducible value we provide?)

COMBINE:
  - Bisociation: Churn × Restaurant loyalty → "regulars" concept
  - TRIZ: Contradiction "personalization requires data, data collection repels users"
  - Serendipity: Domain Roulette → "Gaming" → progression systems

SHIFT:
  - Reframing (Iceberg): Surface "users leave" → Pattern "they never truly arrived"
  - Oblique Strategy: "Honor thy error as a hidden intention" → churned users as product testers
  - Multi-Agent Debate: "Churn is healthy" vs "Churn is failure"

Result: 5 reframed problem statements
```

### Complicated Domain (API Design Decision)

```
CLASSIFY: Complicated (expert analysis needed, multiple valid approaches)

CHALLENGE:
  - Assumption Reversal (10 assumptions about REST vs GraphQL)

COMBINE:
  - SCAMPER on existing API patterns
  - Cross-Domain Analogy: Library catalog systems

SHIFT:
  - Six Thinking Hats (quick rotation)

Result: 3 reframed problem statements
```

### Chaotic Domain (Production Crisis Response)

```
CLASSIFY: Chaotic (unprecedented failure mode, no clear cause-effect)

CHALLENGE:
  - Quick Assumption List (5 assumptions about the failure)

COMBINE:
  - Random Entry: "bridge" → "what connects the failing components?"

SHIFT:
  - Oblique Strategy: "What would you do if given unlimited resources?"
  - PO Provocation: "PO: The system is working perfectly"

Result: 3 rapid reframings + immediate action hypotheses
```
