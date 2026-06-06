# Domain Classifier

**Purpose:** Cynefin-based problem classification and automatic framework selection.
**Read when:** You are in the CLASSIFY phase and need to determine which frameworks to apply.

---

## Contents
- Cynefin Framework Overview
- Domain Classification Criteria
- Framework Selection Matrix
- Classification Procedure
- Edge Cases

---

## Cynefin Framework Overview

The Cynefin framework (Dave Snowden, 1999) classifies problems into domains based on the relationship between cause and effect.

```
┌──────────────────┬──────────────────┐
│    Complex        │   Complicated     │
│  因果は事後判明     │   因果は分析で判明   │
│  Probe→Sense→    │   Sense→Analyze→  │
│  Respond          │   Respond         │
├──────────────────┼──────────────────┤
│    Chaotic        │   Clear           │
│  因果関係なし       │   因果関係明確      │
│  Act→Sense→      │   Sense→          │
│  Respond          │   Categorize→     │
│                   │   Respond         │
└──────────────────┴──────────────────┘
          ┌──────────┐
          │ Confused  │
          │ (未分類)   │
          └──────────┘
```

---

## Domain Classification Criteria

### Clear (明確)

**Characteristics:**
- Cause and effect are obvious to everyone.
- Best practices exist and are well-documented.
- The problem has been solved many times before.
- Constraints are known and stable.

**Signals in user input:**
- "We know the solution but need a better version"
- "Standard approach isn't working well enough"
- "How do we optimize X?"

**Response pattern:** Sense → Categorize → Respond

---

### Complicated (煩雑)

**Characteristics:**
- Cause and effect discoverable through analysis.
- Expert knowledge required to understand relationships.
- Multiple valid approaches exist.
- Good practices (not best practices) apply.

**Signals in user input:**
- "We have options but can't decide which is best"
- "The experts disagree on the approach"
- "We need to analyze before deciding"

**Response pattern:** Sense → Analyze → Respond

---

### Complex (複雑)

**Characteristics:**
- Cause and effect only understood in retrospect.
- Emergent behavior — outcomes are unpredictable.
- Multiple interacting agents/systems.
- The problem changes as you try to solve it.

**Signals in user input:**
- "We keep solving the wrong problem"
- "Every fix creates new problems"
- "We don't know what we don't know"
- "Stakeholders can't agree on what the problem even is"

**Response pattern:** Probe → Sense → Respond

---

### Chaotic (混沌)

**Characteristics:**
- No perceivable cause and effect relationship.
- High turbulence, novel situation.
- Need to act first to create stability.
- No time for analysis.

**Signals in user input:**
- "Everything is falling apart"
- "Nothing we try works"
- "This is completely unprecedented"
- "We need to do something, anything"

**Response pattern:** Act → Sense → Respond

---

### Confused (未分類)

**Characteristics:**
- Cannot determine which domain the problem belongs to.
- Insufficient information to classify.

**Action:** Gather more information. Break the problem into smaller pieces that can be classified independently.

---

## Framework Selection Matrix

Based on Cynefin classification, auto-select the framework combination:

| Domain | CHALLENGE Frameworks | COMBINE Frameworks | SHIFT Frameworks | Intensity |
|--------|---------------------|-------------------|-----------------|-----------|
| **Clear** | First Principles | SCAMPER | Reframing (E5) | Light |
| **Complicated** | Assumption Reversal, Devil's Advocate | TRIZ, Cross-Domain Analogy | Six Thinking Hats | Medium |
| **Complex** | Full Assumption Reversal (20+) | Bisociation, TRIZ | Reframing (Iceberg), Oblique Strategies, Multi-Agent Debate | Heavy |
| **Chaotic** | Quick Assumption List (5-10) | Random Entry (Lateral) | Oblique Strategies, PO Provocation | Rapid |
| **Confused** | First Principles (to decompose) | — | Reframing Matrix (4 perspectives) | Diagnostic |

### Framework Intensity Guide

| Intensity | Assumptions | Frameworks Combined | Iterations | Output Volume |
|-----------|-------------|-------------------|------------|---------------|
| **Light** | 5-10 | 2-3 | 1 | 3 reframings |
| **Medium** | 10-15 | 3-5 | 2 | 3-4 reframings |
| **Heavy** | 15-20+ | 5-7 | 2-3 | 4-5 reframings |
| **Rapid** | 5-10 | 2-3 | 1 | 3 reframings (fast) |
| **Diagnostic** | 10 | 1-2 | 1 | Classification + next steps |

---

## Classification Procedure

### Step 1: Gather Signals

Ask (or infer from context):
- How well understood is the cause-effect relationship?
- How many times has this type of problem been solved before?
- How predictable are the outcomes of actions?
- How many interacting systems/stakeholders are involved?
- Is the situation stable or turbulent?

### Step 2: Score

| Criterion | Clear (1) | Complicated (2) | Complex (3) | Chaotic (4) |
|-----------|-----------|-----------------|-------------|-------------|
| Cause-effect | Obvious | Discoverable | Retrospective only | None |
| Precedent | Many times | Some examples | Few/none | Unprecedented |
| Predictability | High | Medium | Low | None |
| Interactions | Simple | Moderate | Many | Overwhelming |
| Stability | Stable | Mostly stable | Shifting | Turbulent |

Average score → domain classification.

### Step 3: Validate

- Does the classification feel right given the overall context?
- Could the problem span multiple domains? (If so, decompose and classify each part.)
- Is there a dominant domain with minor elements of another?

### Step 4: Select Frameworks

Use the Framework Selection Matrix above. Adjust based on:
- User's stated time constraints (→ reduce intensity).
- User's expertise level (→ adjust explanation depth).
- Specific user requests (→ include requested frameworks regardless of classification).

---

## Edge Cases

### Multi-Domain Problems

Some problems span domains. In this case:
1. Decompose into sub-problems.
2. Classify each independently.
3. Apply appropriate frameworks to each.
4. Synthesize at the CRYSTALLIZE phase.

### Domain Transitions

Problems can shift domains over time:
- Chaotic → Complex (after initial stabilization)
- Complex → Complicated (as patterns emerge)
- Complicated → Clear (as expertise develops)

If the user is describing a transition, apply frameworks for **both** domains.

### User Override

If the user explicitly requests specific frameworks, honor the request regardless of Cynefin classification. Note the classification for context but follow user preference.
