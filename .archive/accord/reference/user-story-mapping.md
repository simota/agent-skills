# User Story Mapping Reference

Purpose: Apply Jeff Patton's User Story Mapping to transform a flat backlog into a two-dimensional map — the backbone (user activities) across the top, detailed stories hanging below each activity, and horizontal release slices that describe what ships when. Story mapping gives Accord's L1/L2 layers a spatial skeleton.

## Scope Boundary

- **accord `story-map`**: Story mapping (this document).
- **accord `vision` / `requirements` / `detail` / `ac` (elsewhere)**: L0-L3 canonical staged elaboration.
- **saga `story` (elsewhere)**: Narrative storytelling. Story Mapping is structural; Saga is emotional.
- **sherpa (elsewhere)**: Atomic step decomposition. Sherpa consumes the map slices.
- **rank (elsewhere)**: Priority scoring for backlog. Complements mapping.

## Structure

```
  User Activities (Backbone)
  ─────────────────────────────────────────────────────────
  [Browse]   [Decide]   [Checkout]   [Receive]   [Review]
     │          │           │            │           │
  User Tasks (narrative flow, left-to-right)
  ─────────────────────────────────────────────────────────
  Search     Compare   Cart          Track       Rate
  Filter     Save      Pay           Unbox       Comment
  Category   Share     Address       Install     Photo
     │          │           │            │           │
  Story Details (hang below each task)
  ─────────────────────────────────────────────────────────
  - by cat.  - wishlist - 1-click    - SMS       - 5-star
  - by tag   - friends  - Apple Pay  - email     - text
  - autocom  - side-by  - saved PMs  - in-app    - photo
  ─────────────────────────────────────────────────────────
          ── Release 1 slice (Walking Skeleton) ──
          ── Release 2 slice ──
          ── Release 3 slice ──
```

### Three structural elements

| Element | Definition | Column count typical |
|---------|-----------|----------------------|
| Backbone | High-level user activities in journey order | 4-8 activities |
| User tasks | Steps within each activity | 3-6 per activity |
| Story details | Specific stories / acceptance items | variable |

### Release slices

Horizontal bands cut across tasks. Each slice is a shippable increment.

- **Slice 1 — Walking Skeleton**: thinnest path end-to-end. Proves the backbone works. Typically 1 story per task.
- **Slice 2 — Delightful minimum**: enough quality to sustain user interest.
- **Slice 3+ — Enrichment**: features that deepen engagement, edge cases, secondary paths.

## Why Story Maps Beat Flat Backlogs

| Problem with flat backlog | How map addresses it |
|---------------------------|----------------------|
| Linear priority hides dependencies | Map shows which tasks belong to the same activity |
| Users don't feel the journey | Backbone = narrative arc |
| No "shippable slice" discipline | Horizontal slices force end-to-end thinking |
| Stakeholders argue priority in isolation | Visual map aligns around shared mental model |
| Scope creep within a feature | Bottom-of-map stories = deferrable |

## Workflow

```
FRAME       →  identify the user (who)
            →  identify the goal (outcome)
            →  set the time window (first release / quarter)

BACKBONE    →  write user activities left-to-right in journey order
            →  ~4-8 activities; phrase as goals not features
            →  review: does it read as a story?

TASKS       →  under each activity, list user tasks (steps)
            →  phrase as "user does X"
            →  3-6 per activity

DETAILS     →  under each task, list specific stories / variations
            →  include edge cases, alternate paths, delights
            →  group with sticky notes or equivalent tool

SLICE       →  walking skeleton: one story per task, thinnest path
            →  name each slice (Release 1 / 2 / 3)
            →  validate slice 1 is genuinely end-to-end

VERIFY      →  top-down read: does backbone tell the story?
            →  left-to-right in each slice: does it ship?
            →  resist adding too much to slice 1

HANDOFF     →  to Accord L1: tasks become REQ-*
            →  to Sherpa: slice 1 stories become atomic steps
            →  to Rank: slice-2+ stories become prioritized backlog
```

## Walking Skeleton

The thinnest end-to-end slice. Must touch every backbone activity with the minimum viable story per task.

### Test

> Can a real user accomplish the end-to-end goal using only slice 1 stories?

If "no" → you have a deep vertical prototype, not a walking skeleton. Add stories horizontally until yes.

### What walking skeleton is NOT

- Not a prototype (it's production code).
- Not a minimum viable product (MVP is slice 1 + slice 2 usually).
- Not every feature at 10% — it's the thinnest *complete path*.

## Slicing Strategies

| Strategy | When | Risk |
|----------|------|------|
| Happy path only in slice 1 | MVP / fastest learning | Edge cases defer |
| One persona in slice 1 | Multi-persona product | Other personas wait |
| One platform in slice 1 | Multi-platform product | Platform gaps |
| One region / locale in slice 1 | i18n later | Localization debt |
| All backbone activities minimally | Most common | Discipline required |

Pick the strategy that matches the product's riskiest assumption.

## Mapping Tools

| Tool | Use case |
|------|----------|
| Physical sticky notes on a wall | Co-located workshop |
| Miro / FigJam / Mural | Remote workshops |
| StoriesOnBoard | Dedicated story-mapping tool |
| Jira Advanced Roadmaps | Enterprise Jira users |
| Google Jamboard | Low-tool-budget teams |
| Plain Markdown tables | Async, durable |

For Accord handoff, capture as Markdown table (backbone cols, task rows, slice annotations) — durable and diff-friendly.

## Output Template

```markdown
## User Story Map: [Product / Feature]

### Frame
- **User**: [primary persona]
- **Goal**: [outcome]
- **Window**: [release / quarter]

### Backbone
| Activity 1 | Activity 2 | Activity 3 | ... |
|-----------|-----------|-----------|-----|
| [goal] | [goal] | [goal] | ... |

### Tasks under each activity
Activity 1:
- task 1.1
- task 1.2
- task 1.3

Activity 2:
- task 2.1
- ...

[repeat]

### Story Details
Under task 1.1:
- story A (slice 1)
- story B (slice 2)
- story C (slice 3)

[repeat for each task]

### Release Slices
#### Slice 1 — Walking Skeleton
End-to-end test: [describe how a user completes the journey with only these stories]
- [story list]

#### Slice 2 — Delightful Minimum
- [story list]

#### Slice 3 — Enrichment
- [story list]

### Risk Check
- [ ] Walking skeleton is truly end-to-end
- [ ] No task lacks a story in slice 1
- [ ] Backbone reads as a coherent user journey
- [ ] Each slice is genuinely shippable

### Handoffs
- Accord L1 `requirements`: promote tasks to REQ-*
- Sherpa: decompose slice-1 stories to atomic steps
- Rank: prioritize slice-2+ backlog
- Canvas: render map as visual
- Scribe: formal PRD section from map
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Backbone = features | Rewrite as user goals/activities |
| Walking skeleton isn't end-to-end | Add stories horizontally until a user can complete the journey |
| Slice 1 = "everything we think is essential" | Slice 1 = thinnest complete path; essentials beyond that go to slice 2 |
| Map has no slices | Map without slices is just a bigger backlog |
| Map is drawn once and forgotten | Re-map quarterly; activities evolve |
| Too many backbone activities (> 10) | Consolidate; activities should represent phases, not tasks |
| Tasks duplicated across activities | Each task belongs to one activity; cross-cutting concerns are NFRs |
| No narrative read-through | Read top row left-to-right; if it doesn't sound like a story, re-order |

## Deliverable Contract

When `story-map` completes, emit:

- **Frame** (user, goal, window).
- **Backbone** with 4-8 activities as goals.
- **Tasks** under each activity (3-6 each).
- **Story details** hanging below tasks.
- **Release slices** with named slice 1 walking skeleton.
- **Risk check** (end-to-end validation).
- **Handoffs**: Accord L1, Sherpa, Rank, Canvas, Scribe.

## References

- Jeff Patton — *User Story Mapping: Discover the Whole Story, Build the Right Product* (O'Reilly, 2014)
- Jeff Patton's original blog posts — "The New User Story Backlog is a Map"
- Alberto Brandolini — *EventStorming* (complementary workshop technique)
- Alistair Cockburn — Walking Skeleton (Crystal Clear / Agile Software Development)
- Mike Cohn — *User Stories Applied* (story writing foundations)
- StoriesOnBoard, Avion — dedicated story-mapping tools
- Miro / FigJam templates for user story mapping
- Henrik Kniberg — "Making Sense of MVP" (parallel concept)
