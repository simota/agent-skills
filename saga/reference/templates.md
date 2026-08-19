# Narrative Templates

**Purpose:** A practical collection of templates for each of Saga's output types.
**Read when:** You need a reference for format and structure while writing a narrative.

> Framework selection and structural definitions live in `saga/SKILL.md`. This file provides only the **application templates** for each output type.

---

## 1. Use Case Story Template

Turning a feature or scenario into a narrative by combining JTBD with the Pixar Story Spine defined in `saga/SKILL.md`.

```markdown
## Use Case Story: [feature/scenario name]

### Meta Info
- **Persona:** [name, role, situation]
- **Framework:** JTBD + Pixar Story Spine
- **Target Audience:** [dev team / PM / stakeholders]

### Story

**[Persona name]'s daily life**

[Persona name] is [occupation/position]. [Concrete depiction of the situation].
Every day, [a recurring challenge or routine] ate up their time.
They felt [emotional burden: anxiety, frustration, fatigue].

**Turning point**

One day, [the trigger for change] arrived.
Trying [product/feature], [depiction of the first experience].

**Chain of change**

Thanks to that, [direct change ①].
On top of that, [indirect change ②].
Before they knew it, [qualitative change ③].

**New daily life**

Now [persona name] is [the transformed self].
[The Before→After contrast in one sentence].

### Job Story Format
> When [situation], I want to [motivation], so I can [outcome].

### Story Element Summary
| Element | Content |
|------|------|
| Hero | [persona] |
| Problem | [external/internal/philosophical] |
| Guide | [product/feature] |
| Transformation | [Before] → [After] |
```

---

## 2. Product Narrative Template

A positioning narrative for the product as a whole, using the StoryBrand SB7 structure defined in `saga/SKILL.md`.

```markdown
## Product Narrative: [product name]

### BrandScript
Apply the SB7 structure and pay particular attention to:
- Write the Hero's "fundamental desire" as **the state they want to achieve**, not a feature
- Fill in all 3 layers of Problem (external, internal, philosophical)
- Keep Plan to 3 steps or fewer (reduce cognitive load)
- Write Failure and Success as contrasts

### One-liner
[Problem] + [Solution] + [Outcome] in one sentence.

> "If [target] is struggling with [problem], get [outcome] with [product]."

### Elevator Pitch (30-second version)
Summarize using the six-line Pixar Story Spine structure in `saga/SKILL.md`.
```

---

## 3. Pitch Story Template

For investors and stakeholders, combine the Pixar Story Spine with quantitative evidence.

```markdown
## Pitch Story: [product name]

### The Story

[Target customer] in a market of [target market size] faces [challenge] every day.

**Current pain:**
- [pain ① shown with a concrete number]
- [pain ② shown with a concrete number]

**Our discovery:**
[Insight. Why existing solutions fall short]

**Our solution:**
[The essence of the product in one sentence]

**Change already happening:**
- [Traction ①: number]
- [Traction ②: number]
- [Customer quote]

**What happens next:**
[Vision. What the world looks like once this product spreads]

### Supporting Data
| Metric | Value |
|------|------|
| TAM | [___] |
| Current user count | [___] |
| Growth rate | [___] |
| NPS | [___] |
```

---

## 4. Customer Success Story Template

A case study / transformation arc combining Hero's Journey (`reference/hero-journey.md`) with CAR.

```markdown
## Customer Success Story: [customer name]

### Overview
| Item | Content |
|------|------|
| Industry | [___] |
| Size | [___] |
| Adoption period | [___] |
| Key outcome | [___] |

### 1. Daily Life (Before)
[The customer's situation before adoption. Depicted in a concrete scene]

> "[Customer quote: how they felt at the time]"

### 2. Turning Point
[What triggered the search for change. Depiction of the breaking point]

### 3. Decision
[Why they chose this product. The comparison/evaluation process]

### 4. Trials and Overcoming
[Early adoption challenges and how they were overcome]

### 5. Transformation (After)
[Concrete outcomes. Numbers + emotional change]

**Quantitative outcomes:**
- [KPI improvement ①]
- [KPI improvement ②]

**Qualitative outcomes:**
- [Team/culture change]
- [The customer's own growth]

> "[Customer quote: how they feel now]"

### 6. New Daily Life
[The post-transformation world. Future outlook]

### Before → After Summary
| Dimension | Before | After |
|------|--------|-------|
| [metric 1] | [value] | [value] |
| [metric 2] | [value] | [value] |
| [emotion] | [state] | [state] |
```

---

## 5. Onboarding Narrative Template

The story flow of a first-time experience using Story Mapping.

```markdown
## Onboarding Narrative: [product name]

### Narrative Flow

```text
[Step 1]      [Step 2]       [Step 3]       [Step 4]       [Step 5]
Welcome  →  First Value  →  Aha Moment  →  Habit Loop  →  Advocacy
```

### Step 1: Welcome
**User's feeling:** [anxiety, anticipation, curiosity]
**Narrative:** "[Tone of the welcome message. Reassuring]"
**Goal:** [What should be achieved at this step]

### Step 2: First Value
**User's feeling:** [exploration, trial]
**Narrative:** "[The narration that leads to the first successful experience]"
**Goal:** [Minimize Time-to-Value]

### Step 3: Aha Moment
**User's feeling:** [discovery, delight]
**Narrative:** "[The moment they realize the product's essential value]"
**Goal:** [Experiencing the core value]

### Step 4: Habit Loop
**User's feeling:** [confidence, sense of efficiency]
**Narrative:** "[The story of the hook that makes them want to come back]"
**Goal:** [Establishing retention]

### Step 5: Advocacy
**User's feeling:** [satisfaction, desire to share]
**Narrative:** "[The story of the experience that makes them want to recommend it]"
**Goal:** [Word of mouth / referral]
```

---

## 6. Scenario Narrative Template

A persona-specific scenario combining JTBD with concrete context depiction.

```markdown
## Scenario Narrative: [scenario name]

### Persona
| Item | Content |
|------|------|
| Name | [___] |
| Age / Occupation | [___] |
| Tech proficiency | [___] |
| Primary goal | [___] |
| Primary frustration | [___] |

### Scene Setup
**When:** [specific timing]
**Where:** [specific location]
**What's happening:** [the action right before]

### Narrative

[Persona name] is [situation] at [location].
[A depiction appealing to the senses: what's seen, heard, felt].

[The challenge arises. Concrete depiction].
[The emotional shift].

[The point of contact with the product/feature].
[Depiction of the operation. Step by step, alongside the emotional shift].

[The felt sense of the outcome].
[The post-transformation emotion].

### Tension Points
| Point | Content | Resolution |
|---------|------|--------|
| [①] | [challenge] | [how the product addresses it] |
| [②] | [anxiety] | [reassurance] |
| [③] | [barrier] | [how it's overcome] |
```

---

## Writing Guidelines

### Choosing a Tone

| Audience | Tone | Characteristics |
|------|--------|------|
| Dev team | Straightforward, concrete | Includes technical context, states hypotheses explicitly |
| PM/PdM | Strategic, insightful | Emphasizes business impact |
| Stakeholders | Concise, high-impact | Numbers and transformation front and center |
| End users | Empathetic, approachable | A narrative easy to relate to personally |
| Investors | Confident, data-backed | Market size and traction |

### Length Guidelines

| Output Type | Short | Standard | Detailed |
|-----------|------|------|------|
| Use Case Story | 200 words | 500 words | 800 words |
| Product Narrative | 300 words | 800 words | 1500 words |
| Pitch Story | 150 words | 300 words | 500 words |
| Customer Success | 500 words | 1200 words | 2000 words |
| Onboarding | 100 words/step | 200 words/step | 300 words/step |
| Scenario | 300 words | 600 words | 1000 words |
