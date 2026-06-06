# Moodboard Workflow

Purpose: Use this reference when visual direction is unclear and the project needs exploratory design before committing to a direction. Forge generates moodboard variants that Vision evaluates.

## Contents

- When to Use Moodboard Mode
- 4-Step Workflow
- Variant Definition Structure
- Evaluation Criteria
- Selection and Handoff

---

## When to Use Moodboard Mode

Use moodboard mode when:
- Visual direction is undefined or "make it look good" is the brief
- Stakeholders cannot articulate design preferences
- Brand identity is new or being redefined
- Multiple valid aesthetic directions exist
- The team needs a shared visual vocabulary before proceeding

Do NOT use moodboard mode when:
- Brand guidelines are established and clear
- The task is implementing an existing design direction
- Time constraints require immediate production work

---

## 4-Step Workflow

### Step 1: Collect

Gather inputs that define the design space:

| Input | Source | Purpose |
|-------|--------|---------|
| Brand keywords | Stakeholder interview or brief | Personality anchors (3-5 words) |
| Competitor references | Compete agent or manual research | What to differentiate from |
| Inspiration references | Stakeholder or designer input | Aesthetic preferences |
| Constraints | Technical or brand requirements | Non-negotiable boundaries |
| Content samples | Prose agent or existing content | Real text for realistic mockups |

**Output:** Collected brief with keywords, references, and constraints.

### Step 2: Generate 3+ Variants

Create at least 3 distinct moodboard variants. Each variant must be meaningfully different, not minor variations of the same idea.

Each variant defines:

```markdown
## Variant [A/B/C]: [Name]

### Color Mood
- Primary palette: [3-5 colors with hex values]
- Emotional register: [warm/cool/neutral, bold/subtle, light/dark]
- Contrast strategy: [high-contrast/mid-contrast/low-contrast]

### Typography Character
- Display font suggestion: [font name + why it fits]
- Body strategy: [custom font or system stack]
- Personality: [elegant/technical/playful/authoritative/minimal]

### Image Style
- Photography direction: [real product/lifestyle/abstract/illustration]
- Treatment: [full-bleed/contained/masked/overlaid]
- Mood: [aspirational/documentary/conceptual/minimal]

### Layout Density
- Whitespace strategy: [generous/balanced/compact]
- Section rhythm: [uniform/varied/progressive]
- Grid character: [asymmetric/centered/edge-to-edge]

### Motion Personality
- Animation style: [subtle/expressive/minimal/none]
- Entrance strategy: [fade/slide/scale/instant]
- Interaction feel: [snappy/smooth/weighted/instant]
```

### Step 3: Evaluate

Score each variant on a 4-axis, 5-point scale:

| Axis | 1 (Low) | 3 (Mid) | 5 (High) |
|------|---------|---------|----------|
| **Brand Fit** | Contradicts brand identity | Neutral/acceptable | Reinforces and amplifies brand |
| **Differentiation** | Looks like competitors | Somewhat distinct | Clearly unique in market |
| **Production Feasibility** | Requires custom assets/tools | Standard tooling with effort | Achievable with current stack |
| **Longevity** | Trendy, will date quickly | 1-2 year shelf life | 3+ year timeless quality |

### Evaluation Template

```markdown
## Moodboard Evaluation

| Variant | Brand Fit | Differentiation | Feasibility | Longevity | Total |
|---------|-----------|----------------|-------------|-----------|-------|
| A: [Name] | [1-5] | [1-5] | [1-5] | [1-5] | [/20] |
| B: [Name] | [1-5] | [1-5] | [1-5] | [1-5] | [/20] |
| C: [Name] | [1-5] | [1-5] | [1-5] | [1-5] | [/20] |

### Recommendation
- Selected: Variant [X]
- Rationale: [why this variant best serves the project]
- Adaptations: [any modifications to the selected variant]
```

### Step 4: Select and Handoff

Package the selected variant for Vision and downstream agents.

**Handoff deliverable:**

```markdown
## FORGE_MOODBOARD_HANDOFF

### Selected Direction
- Variant: [Name]
- Score: [X/20]

### Design Tokens (Preliminary)
- Colors: [primary, secondary, accent, background, text]
- Typography: [display font, body strategy]
- Spacing: [density level]
- Motion: [personality summary]

### Key Visual Decisions
- Hero approach: [image type + treatment]
- Layout strategy: [density + rhythm]
- Brand signals: [what makes this recognizably "ours"]

### Constraints Carried Forward
- [Technical or brand constraints that shaped the direction]

### Next Agent
- Vision: to formalize into design direction
- Muse: to convert preliminary tokens into system tokens
```

---

## Variant Naming Conventions

Name variants by their defining characteristic, not by letters:

| Bad | Good |
|-----|------|
| Variant A | "Calm Technical" |
| Variant B | "Bold Editorial" |
| Variant C | "Warm Minimal" |

Names should be 2 words that capture the variant's personality. This helps stakeholders discuss and compare variants meaningfully.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| 3 variants that look the same | No real exploration | Vary at least 2 of the 5 dimensions significantly |
| Moodboard without real content | Cannot evaluate readability or fit | Use content samples from Prose or existing copy |
| Evaluation by "feeling" only | Subjective, non-reproducible | Use the 4-axis scoring system |
| Skipping moodboard for "speed" | Direction changes cost more later | Invest 1-2 hours in exploration to save days of rework |
| Picking the "safest" variant always | Defaults to generic | Evaluate differentiation axis explicitly |
