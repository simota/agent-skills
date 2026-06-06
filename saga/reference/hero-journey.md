# Hero's Journey Reference

Purpose: Apply Joseph Campbell's Monomyth / Christopher Vogler's 12-stage Hero's Journey to major customer transformation stories. Best fit for case studies, onboarding narratives, and flagship success stories where stakes are high, transformation is profound, and the audience needs to *feel* the distance between Before and After.

## Scope Boundary

- **saga `hero-journey`**: 12-stage monomyth deep-dive (this document).
- **saga `story` (elsewhere)**: Short use-case narrative. Hero's Journey is for long-form transformation; `story` is everyday feature scenarios.
- **saga `narrative` (elsewhere)**: Product positioning (StoryBrand/Promised Land).
- **saga `bab` (elsewhere)**: Three-part BAB short-form copywriting.
- **saga `customer` (elsewhere)**: Before→After transformation arc without full 12 stages.
- **Director (elsewhere)**: Demo video scenarios — Hero's Journey provides the script.

## Core Principle

In StoryBrand, the **customer is the hero** and **the product is the guide** (Yoda, not Luke). Hero's Journey adds the depth: the customer's transformation is structured across 12 beats that mirror ancient storytelling patterns humans instinctively recognize.

## 12 Stages (Vogler's Adaptation)

```
         ACT 1: DEPARTURE           ACT 2: INITIATION          ACT 3: RETURN
      ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
      │ 1 Ordinary World    │   │  5 Crossing Threshold│   │ 10 Road Back        │
      │ 2 Call to Adventure │   │  6 Tests/Allies/Enemy│   │ 11 Resurrection     │
      │ 3 Refusal of Call   │──▶│  7 Approach Inmost  │──▶│ 12 Return with Elixir│
      │ 4 Meeting the Agora│   │  8 Ordeal           │   │                     │
      │                     │   │  9 Reward            │   │                     │
      └─────────────────────┘   └─────────────────────┘   └─────────────────────┘
```

### Stage-by-stage mapping for product narratives

| # | Stage | Mythic meaning | Product narrative meaning |
|---|-------|----------------|--------------------------|
| 1 | Ordinary World | Hero's familiar life | Customer's status quo — the pain they've normalized |
| 2 | Call to Adventure | The disruption | Trigger event: new pressure, missed quarter, competitor move |
| 3 | Refusal of the Call | Fear, doubt | "We can't switch now", "Too risky", "Let's patch what we have" |
| 4 | Meeting the Agora | Yoda/Obi-Wan appears | Customer encounters *your product* (or your sales/community) |
| 5 | Crossing the Threshold | Commitment | Trial, POC, first purchase — crosses into unfamiliar territory |
| 6 | Tests, Allies, Enemies | Small wins and losses | Early workflows: first integration, first team convert, internal opponent emerges |
| 7 | Approach to the Inmost Cave | Prep for central ordeal | Scaling decision: big rollout, replacing critical legacy |
| 8 | Ordeal | Life-or-death crisis | Go-live, first incident, board approval, production migration |
| 9 | Reward (Seizing the Sword) | Prize won | First measurable outcome (KPI move, saved launch, customer NPS lift) |
| 10 | The Road Back | New threats on return | Scaling pains: adoption across teams, budget renewal, edge cases |
| 11 | Resurrection | Final transformation | Customer becomes a different organization — culturally, operationally |
| 12 | Return with the Elixir | Bringing the gift home | Advocacy: case study, referral, evangelism, community leadership |

### Shortened 8-stage version (Vogler core)

For shorter case studies, collapse:
- Merge **3 + 4** → "Doubt answered by mentor"
- Merge **6 + 7** → "Early wins leading to bigger bet"
- Keep **8, 9, 11, 12** (the dramatic beats)

## Workflow

```
SCOPE      →  decide full 12-stage vs compressed 8-stage based on length budget
           →  12-stage = 1500-3000 chars (flagship case study)
           →  8-stage  = 800-1500 chars (standard case study)

DISCOVER   →  gather: customer's before-state, trigger event, decision moment,
           →          key hero internal conflict, measurable after-state

CAST       →  name the hero (customer as individual or org with a face)
           →  name the guide (your product / a specific customer-success contact)
           →  name the shadow/antagonist (status quo, incumbent, time pressure)

STRUCTURE  →  map the customer's real story onto the 12 (or 8) stages
           →  if a stage is missing, flag it — don't fabricate

WRITE      →  open with concrete scene in the Ordinary World
           →  one paragraph per stage for flagship; one sentence per stage for compressed
           →  end with the Elixir: what the hero now gives back

REFINE     →  AP-1~AP-9 anti-pattern check (see reference/anti-patterns.md)
           →  specifically: AP-4 (no transformation), AP-8 (no failure), AP-2 (product as hero)

DELIVER    →  include: framework stage map, named characters, measurable before/after,
           →          recommended downstream (Director for video, Prose for pull-quotes)
```

## The Three Most Important Beats

Not every stage carries equal weight. If time is short, emphasize:

| Beat | Why it matters |
|------|----------------|
| **Call to Adventure (stage 2)** | Without a trigger event, the story has no tension. "They were doing fine" is not a story. |
| **Ordeal (stage 8)** | The moment of maximum doubt. If the audience doesn't feel the risk, the reward lands flat. |
| **Return with Elixir (stage 12)** | Without giving back, the hero's journey is incomplete. This is where advocacy, case-study-ability, community leadership live. |

Skipping any of these three = story feels hollow.

## Internal vs External Arc

For a satisfying monomyth, both must be present.

| Arc | What changes |
|-----|-------------|
| External | What the hero *does*: signs the contract, goes live, hits the metric |
| Internal | Who the hero *is*: goes from skeptic to believer, from reactive to strategic, from operator to leader |

A case study with only external ("they switched to our tool and shipped faster") is a feature story. The internal arc ("their engineering manager stopped firefighting and became a systems thinker") is what makes it a hero's journey.

## Output Template

```markdown
## Hero's Journey Narrative: [Customer / Case]

### Cast
- **Hero**: [customer — person or org with a name]
- **Ordinary World**: [status quo — 1-2 sentences]
- **Agora/Guide**: [your product, or a named CS/community figure]
- **Shadow/Antagonist**: [status quo, incumbent, time pressure, internal skeptic]

### Arc
- **External change**: [before metric → after metric]
- **Internal change**: [who the hero was → who they became]

### Stage-by-Stage (12 or 8)

**Act 1 — Departure**

1. **Ordinary World**: [concrete scene of the status quo, with sensory detail]
2. **Call to Adventure**: [trigger event — date, context]
3. **Refusal of the Call**: [internal doubt, objections raised]
4. **Meeting the Agora**: [first encounter with product/guide]

**Act 2 — Initiation**

5. **Crossing the Threshold**: [commitment moment — POC, trial, signed contract]
6. **Tests, Allies, Enemies**: [early wins, early losses, who joined and who resisted]
7. **Approach to the Inmost Cave**: [preparing for big bet]
8. **Ordeal**: [the crisis — go-live, incident, board challenge]
9. **Reward**: [first measurable outcome]

**Act 3 — Return**

10. **The Road Back**: [scaling pains]
11. **Resurrection**: [final transformation — org culture change]
12. **Return with the Elixir**: [advocacy, case study, community leadership]

### Anti-Pattern Check
Run the full AP-1~AP-9 checklist from `reference/anti-patterns.md` and report results in the standard format. Hero's Journey emphasizes AP-2 (Hero Product), AP-4 (No Transformation), AP-8 (Happy Path Only) — these are the failure modes most common to long-form transformation arcs.

### Assumptions
- [list unverified premises]

### Handoffs
- Director: 12-scene demo video script
- Prose: pull-quotes and LP hero
- Prism: NotebookLM steering for audio narration
- Growth: LP copy adapted from stages 1-2 (hook) and 11-12 (proof)
```

## Anti-Patterns Specific to Hero's Journey

| Anti-pattern | Fix |
|--------------|-----|
| Product = hero (Luke, not Yoda) | Rewrite with customer as subject; product appears only at stage 4 |
| Skipping Refusal of the Call | Add objection: "they almost didn't switch because..." |
| No Ordeal (no real risk) | Name the moment the outcome was genuinely uncertain |
| Elixir missing | Show what the hero now gives back (case study, referral, community) |
| Fabricated internal arc | If you don't know the internal change, interview to find it — don't invent |
| Mythologizing the product | Guide has wisdom but never upstages the hero |
| Compressing beyond 8 stages | Below 8 stages it stops being a hero's journey; use BAB or JTBD instead |

## Deliverable Contract

When `hero-journey` completes, emit:

- **Cast** (hero with name, mentor, shadow).
- **External + internal arc** with measurable change.
- **12 or 8 stages** written out with concrete scenes.
- **Three critical beats** (Call, Ordeal, Elixir) emphasized.
- **Anti-pattern check** (AP-1~AP-9 per `reference/anti-patterns.md`).
- **Assumptions** section.
- **Handoffs**: Director, Prose, Prism, Growth.

## References

- Joseph Campbell — *The Hero with a Thousand Faces* (1949, original monomyth)
- Christopher Vogler — *The Writer's Journey: Mythic Structure for Writers* (12-stage adaptation)
- Donald Miller — *Building a StoryBrand* (customer-as-hero for brand work)
- Nancy Duarte — *Resonate* (applies narrative arcs to presentations)
- Pixar's "22 Story Basics" (Emma Coats) — related principles
- Robert McKee — *Story* (screenwriting structure)
- HBR — "Storytelling That Moves People" (Robert McKee interview)
