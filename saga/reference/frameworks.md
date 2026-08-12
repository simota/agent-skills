# Narrative Frameworks Reference

**Purpose:** Detailed specification of the storytelling frameworks Saga uses.
**Read when:** You need the detailed structure of a framework, application guidelines, or concrete filled examples.

---

## 1. StoryBrand SB7 Framework

A 7-element brand story framework proposed by Donald Miller. Best suited for product messaging, landing pages, and pitches.

### Structure

```
┌─────────────────────────────────────────────────────┐
│  1. HERO (Customer)                                  │
│     The customer wants something                     │
│            ↓                                         │
│  2. PROBLEM                                          │
│     Facing an external, internal, and philosophical  │
│     problem                                          │
│            ↓                                         │
│  3. GUIDE (Your Product)                             │
│     A guide with empathy + authority appears         │
│            ↓                                         │
│  4. PLAN                                             │
│     The guide presents a clear plan (3 steps or fewer)│
│            ↓                                         │
│  5. CALL TO ACTION                                   │
│     Prompts action (direct + transitional)           │
│            ↓                                         │
│  ┌────────────┬────────────┐                         │
│  │ 6. FAILURE │ 7. SUCCESS │                         │
│  │ What       │ What       │                         │
│  │ happens if │ results if │                         │
│  │ they don't │ they act   │                         │
│  │ act        │            │                         │
│  └────────────┴────────────┘                         │
└─────────────────────────────────────────────────────┘
```

### BrandScript Template

```markdown
## BrandScript: [product name]

### 1. Hero (Customer)
[Who is the customer? What do they want?]
- Desire: ____

### 2. Problem
- External problem: [concrete, surface-level obstacle]
- Internal problem: [emotional anxiety/frustration]
- Philosophical problem: [a belief of the form "things should be..."]
- Villain: [the problem personified]

### 3. Guide (= the product)
- Empathy: ["We understand how you feel"]
- Authority: [track record, numbers, testimonials]

### 4. Plan
1. [Step 1]
2. [Step 2]
3. [Step 3]

### 5. Call to Action
- Direct CTA: [do X right now]
- Transitional CTA: [first, try X]

### 6. Failure
[What is lost by not acting]

### 7. Success
[What results look like after acting]
```

### Application Tips
- Fill in all 3 layers of the Problem (external/internal/philosophical)
- For the Guide, "empathy" comes first, "authority" comes second
- Keep the Plan to 3 steps or fewer (reduce cognitive load)
- Contrast Failure and Success against each other

---

## 2. Pixar Story Spine

A 6-line story template proposed by Pixar's Emma Coats. Best suited for short scenarios, internal sharing, and elevator pitches.

### Structure

```markdown
## Story Spine: [title]

**Once upon a time...**
[The protagonist's daily life and world]

**Every day...**
[The recurring routine / current state]

**Until one day...**
[The trigger for change / the event]

**Because of that...**
[Chained consequence ①]

**Because of that...**
[Chained consequence ②]

**Until finally...**
[The climax / resolution]

**And ever since that day...**
[The new daily life / the transformed world]
```

### Product Adaptation

| Spine Element | Product Context |
|--------------|-----------------|
| Once upon a time | The target customer's current state |
| Every day | The recurring challenge / pain point |
| Until one day | The encounter with the product |
| Because of that (×2) | The chain of change the product brings |
| Until finally | The final outcome / transformation |
| Ever since that day | The new daily life |

### Example

```
Once upon a time, freelancer Sato-san made every month's invoices by hand.
Every day, she spent two hours opening Excel, calculating amounts, converting to PDF, and sending by email.
Until one day, she tried [Product Name].
Because of that, invoices started generating automatically from transaction data.
Because of that, the two hours at month-end shrank to fifteen minutes, and unpaid invoices declined thanks to automatic reminders.
Until finally, Sato-san was freed from the stress of invoicing and could focus on her core work.
And ever since that day, "managing money" stopped being a source of anxiety and became an ally to her business.
```

---

## 3. Hero's Journey (Product Adapted)

Joseph Campbell / Dan Harmon's story structure adapted to a product context. Best suited for major transformation stories and case studies.

### Simplified Product Journey (6 Stages)

```
┌─────────────────────────────────────────────┐
│                                             │
│    1. ORDINARY WORLD                        │
│    (the customer's daily life / current     │
│    challenge)                                │
│              ↓                              │
│    2. CALL TO ADVENTURE                     │
│    (realizing change is needed)             │
│              ↓                              │
│    3. CROSSING THE THRESHOLD                │
│    (the decision to try the product)        │
│              ↓                              │
│    4. TRIALS & ALLIES                       │
│    (adoption challenges / encountering       │
│    support)                                  │
│              ↓                              │
│    5. TRANSFORMATION                        │
│    (dramatic change / outcome)              │
│              ↓                              │
│    6. RETURN WITH THE ELIXIR                │
│    (the new daily life / sharing with       │
│    others)                                   │
│                                             │
└─────────────────────────────────────────────┘
```

### Template

```markdown
## Hero's Journey: [customer name/persona name]

### 1. Ordinary World
[The customer's current state. What they struggle with. What their days look like]

### 2. Call to Adventure
[What triggered the search for change. What was the breaking point]

### 3. Crossing the Threshold
[The decision to choose the product. What tipped the scale]

### 4. Trials & Allies
[Early adoption challenges. How they were overcome. Who helped]

### 5. Transformation
[Concrete outcomes. What changed, both numerically and emotionally]

### 6. Return with the Elixir
[The new daily life. The wisdom gained from this experience. Impact on others]
```

---

## 4. JTBD Job Story

A job story based on Clayton Christensen / Alan Klement's JTBD theory. Best suited for individual feature use cases, aimed at dev teams.

### Structure

```
When [situation/context],
I want to [motivation/action],
so I can [expected outcome].
```

### Extended Job Story Template

```markdown
## Job Story: [feature/use case name]

### Context
**When** [the specific situation/trigger]
- Location: [where]
- Timing: [when]
- Emotional state: [how they feel]
- Constraints: [what they're bound by]

### Motivation
**I want to** [the desired action]
- Functional need: [wanting to complete a task]
- Emotional need: [wanting reassurance/confidence]
- Social need: [wanting to be recognized/to contribute]

### Outcome
**So I can** [the desired result]
- Direct outcome: [what's gained immediately]
- Indirect outcome: [what's gained long term]

### Forces (dynamics of adoption vs. non-adoption)
| Force | Direction | Description |
|-------|-----------|-------------|
| Push (dissatisfaction with the status quo) | → toward the new solution | [what's dissatisfying] |
| Pull (appeal of the new solution) | → toward the new solution | [what's appealing] |
| Anxiety | ← toward the status quo | [what's worrying] |
| Habit | ← toward the status quo | [what's a barrier] |
```

---

## 5. Story Mapping (Jeff Patton)

Visualizes the narrative flow of the product as a whole. Best suited for product discovery and roadmap design.

### Structure

```
Backbone (JTBD / major activities)
┌──────┬──────┬──────┬──────┬──────┐
│Act 1 │Act 2 │Act 3 │Act 4 │Act 5 │
├──────┼──────┼──────┼──────┼──────┤  ← Walking Skeleton (MVP)
│Step  │Step  │Step  │Step  │Step  │
│1a    │2a    │3a    │4a    │5a    │
├──────┼──────┼──────┼──────┼──────┤  ← Release 2
│Step  │Step  │Step  │Step  │Step  │
│1b    │2b    │3b    │4b    │5b    │
├──────┼──────┼──────┼──────┼──────┤  ← Release 3
│Step  │Step  │Step  │Step  │Step  │
│1c    │2c    │3c    │4c    │5c    │
└──────┴──────┴──────┴──────┴──────┘
```

### Narrative Flow Template

```markdown
## Story Map: [product/feature name]

### Narrative Backbone
1. **[activity 1]** - [what the user does first]
2. **[activity 2]** - [what they do next]
3. **[activity 3]** - [the main activity]
4. **[activity 4]** - [confirming the result]
5. **[activity 5]** - [repeating/sharing]

### Walking Skeleton (MVP story)
[The minimal story flow. The simplest possible steps for each activity]

### Release Slices
- **Release 1 (MVP):** [the slice where a minimal story holds together]
- **Release 2:** [the slice that enriches the story]
- **Release 3:** [the slice of the complete story experience]
```

---

## 6. CAR Framework

Three elements: Context → Action → Results. Best suited for outcome-focused case studies and success stories.

### Template

```markdown
## Case Study: [customer name/project name]

### Context
[The customer's situation, industry, size, challenge]
- Industry: [___]
- Size: [___]
- Challenge: [___]

### Action
[What was adopted and how it was used]
- Adoption process: [___]
- Usage approach: [___]
- Duration: [___]

### Results
[Concrete outcomes. Shown with numbers]
- Quantitative outcome: [___% improvement / ___ hours saved / ¥___ in value]
- Qualitative outcome: [team change / culture change]
- Customer quote: "[quote]"
```

---

## 7. Promised Land Framework (Andy Raskin)

A strategic positioning narrative. Best suited for fundraising, organizational alignment, and sales decks. A story that leads the customer to a "promised land."

### Structure (5 Elements)

```
┌─────────────────────────────────────────────────────┐
│  1. CHANGE                                           │
│     Show a major, undeniable change happening in     │
│     the world                                        │
│              ↓                                       │
│  2. STAKES                                           │
│     Show that this change creates winners and losers │
│              ↓                                       │
│  3. PROMISED LAND                                    │
│     Paint the compelling future the customer should  │
│     reach                                             │
│     (one that is difficult to reach without you)     │
│              ↓                                       │
│  4. MAGIC GIFTS                                      │
│     Introduce the product's features as the "gifts"  │
│     that get them to the promised land               │
│              ↓                                       │
│  5. EVIDENCE                                         │
│     Show evidence that this story can actually happen│
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Template

```markdown
## Strategic Narrative: [product name]

### 1. Change (the undeniable change)
[The major change happening in the industry/world. Backed by data]

### 2. Stakes (winners and losers)
- **Winners:** [what happens to companies/people who adapt to this change]
- **Losers:** [what happens to companies/people who don't adapt]

### 3. Promised Land
[The future the customer should reach. Depicted concretely and compellingly]
- This future is difficult to reach without our product

### 4. Magic Gifts
[Introduce the product's features as "tools for reaching the promised land"]
- Gift 1: [feature → the change it brings]
- Gift 2: [feature → the change it brings]
- Gift 3: [feature → the change it brings]

### 5. Evidence
[Cases/numbers where this story is already coming true]
- [customer case / traction]
- [industry data / third-party assessment]
```

### Application Tips
- The "promised land" should be compelling to the customer, yet improbable to reach without your company
- Position features as "Magic Gifts" — the "weapons" the customer (Hero) needs to reach the promised land
- Choose a Change that is undeniable — one the audience can't dismiss as "that's not true"
- Zuora's "Subscription Economy" deck is a well-known successful example

---

## 8. ABT Framework (And, But, Therefore)

A minimal 3-element narrative structure proposed by Randy Olson, drawn from science communication. Best suited for social media posts, internal communication, and concise messaging.

### Structure

```
[Context] AND [Additional context],
BUT [Tension/problem],
THEREFORE [Resolution/action].
```

### Template

```markdown
## ABT Narrative: [theme]

### And
[Set the scene. Shareable context. A premise the audience can nod along to]

### But
[The tension. The problem/challenge/obstacle. The pivot point of "but..."]

### Therefore
[The resolution. The action/proposal/conclusion. The consequence of "therefore..."]

### Complete Sentence
[Context] AND [Additional context], BUT [Tension], THEREFORE [Resolution].
```

### Application Tips
- Watch out for becoming AAA (And, And, And) — without the "But" tension, it becomes boring
- Watch out for becoming DHY (Despite, However, Yet) — stacking negations creates a defensive impression
- Can be completed in a single sentence, or each element can be expanded into a paragraph
- Also applicable to slide structure in presentations, email openings, and Slack messages

---

## Framework Combination Patterns

Patterns for combining multiple frameworks.

| Combination | Use Case | How |
|-------------|----------|-----|
| SB7 + Pixar | Landing page + elevator pitch | Design structure with SB7 → summarize with Pixar |
| JTBD + Hero's Journey | Feature proposal + case study | Feature-level with JTBD → full picture with Hero's Journey |
| Story Mapping + JTBD | Roadmap + individual stories | Place each JTBD onto the Story Map's backbone |
| CAR + SB7 | Case study + messaging | Facts with CAR → messaging with SB7 |
| Promised Land + SB7 | Strategic narrative + landing page/pitch | Big picture with Promised Land → individual messaging with SB7 |
| ABT + Pixar | Social + elevator pitch | Summarize with ABT → expand with Pixar |
| Promised Land + CAR | Strategy + case study | Future vision with Promised Land → evidence with CAR |


---

## INTERACTION_TRIGGERS Question Schemas (SKILL.md excerpt)

### AUDIENCE_UNCLEAR

```yaml
questions:
  - question: "Who is the primary audience for this narrative?"
    header: "Audience"
    options:
      - label: "Development team"
        description: "Technical context included, hypothesis-driven, JTBD format preferred"
      - label: "Stakeholders / investors"
        description: "Data-backed, concise pitch format, transformation arc emphasized"
      - label: "End users / customers"
        description: "Empathetic tone, relatable scenarios, plain language"
      - label: "Cross-team (Biz/Dev/Design)"
        description: "Balanced depth, shared vocabulary, L0 vision style"
    multiSelect: false
```

### FRAMEWORK_CHOICE

```yaml
questions:
  - question: "Which storytelling framework should be applied?"
    header: "Framework"
    options:
      - label: "StoryBrand SB7 (Recommended)"
        description: "7-element brand story: Hero→Problem→Guide→Plan→CTA→Failure→Success"
      - label: "Pixar Story Spine"
        description: "6-line narrative: Once upon a time→Every day→Until one day→Because of that→Until finally"
      - label: "JTBD Job Story"
        description: "When [situation], I want to [motivation], so I can [outcome]"
      - label: "Hero's Journey"
        description: "6-stage transformation: Ordinary World→Call→Threshold→Trials→Transformation→Return"
      - label: "Promised Land (Andy Raskin)"
        description: "Strategic positioning: Change→Stakes→Promised Land→Magic Gifts→Evidence"
      - label: "ABT (And, But, Therefore)"
        description: "Quick narrative structure for social posts, internal comms, concise messaging"
    multiSelect: false
```

### VOICE_ALIGNMENT

```yaml
questions:
  - question: "How should the narrative align with the existing brand voice?"
    header: "Voice"
    options:
      - label: "Follow existing guide (Recommended)"
        description: "Adhere strictly to the project's established voice and tone guidelines"
      - label: "Adapt for this context"
        description: "Use the existing guide as a base but adjust tone for the specific audience"
      - label: "No existing guide"
        description: "No brand voice guide exists; Saga will propose a tone direction"
    multiSelect: false
```



---

## Core Contract — Long Form with Rationale (SKILL.md excerpt)

- Position the customer as the hero and the product as the guide in every narrative — brands that position themselves as the hero distance customers who perceive competition for scarce resources (StoryBrand SB7 principle).
- Explicitly apply a named story framework (SB7/Pixar/Hero's Journey/JTBD/CAR/Story Mapping/Promised Land/ABT) to every narrative and state which was chosen and why.
- Focus on one core problem per narrative — tackling multiple problems causes audience confusion and dilutes the call to action (common SB7 anti-pattern).
- Connect all three problem levels: external (tangible obstacle), internal (emotional frustration), and philosophical (why it matters universally) — companies sell solutions to external problems, but customers buy solutions to internal problems. Disconnected levels break narrative coherence.
- Include a Before→After transformation arc with observable or measurable change — "metric-free success" is an anti-pattern.
- Embed tension (challenge/conflict) in every narrative — resolution without struggle fails to engage.
- Use concrete scenes with sensory details (visual, auditory, emotional) — avoid abstract feature descriptions.
- Target narratives by audience type: development team (hypothesis-driven, JTBD), stakeholders/investors (data-backed, transformation arc), end users (empathetic, relatable), cross-team (balanced depth, shared vocabulary).
- Validate every narrative against the AP-1 through AP-9 anti-pattern checklist before delivery.
- Narrative length targets: Use Case Story 300-800 chars, Product Narrative 500-1500 chars, Pitch Story 200-500 chars, Customer Success 800-2000 chars, Onboarding Flow 150 chars/step.
- Adapt narratives for micro-narrative formats (short, interconnected, platform-tailored stories) when the target channel is social media or episodic content.
- For product-level narratives, define a "Controlling Idea" (StoryBrand 2.0) — a single statement capturing the brand's promised transformation that unifies all messaging touchpoints. Every narrative, tagline, and CTA should trace back to this one idea.
- For strategic positioning and fundraising, consider the Promised Land framework (Andy Raskin): define a compelling future state the product commits to bringing about — this aligns customers, product teams, and sales around a single purpose without corporate jargon.
- When the audience can participate (community, beta, co-creation contexts), design narratives that invite audience contribution — participatory storytelling drives deeper engagement than passive consumption.
- For multi-product portfolios, apply a five-layer narrative architecture: Customer Reality → Category Promise → Core Value Story → Product Chapters → Moment Stories — each layer must trace back to the Controlling Idea. This prevents narrative fragmentation as product lines multiply.
- When using StoryBrand 2.0 AI tools for BrandScript generation or message refinement, treat AI output as a draft requiring human validation — AI ensures consistency at scale but cannot verify emotional authenticity or cultural nuance.
- State all unverified premises in a dedicated "Assumptions" section — narrative bias (distorting facts to fit story) is a critical anti-pattern.
- Author for the executing engine (P1–P11 bind only on Opus 5; P12 generation-wide). See `_common/OPUS_5_AUTHORING.md` (P3, P5 critical for Saga; P2, P1 recommended).
