# Game Design Document

**Purpose:** GDD structure, design pillars, the core loop, the MDA framework, and scope/vertical-slice planning.
**Read when:** Authoring or extending a GDD, or defining mechanics (`gdd` recipe).

## Contents
- The GDD is a living spec
- Design pillars
- The core loop
- MDA framework
- Mechanic & game-feel design
- Scope & vertical slice
- GDD outline
- Pitfalls

---

## The GDD is a living spec

A GDD exists to align the team and feed implementation — not to be a polished novel. Keep it tight, current, and decision-bearing. Lead with pillars and the core loop (the two things everything else derives from). Cut anything that doesn't change a decision.

---

## Design pillars

2–4 short statements of what the game IS and what experience it delivers. Pillars are the cut-line: every mechanic, level, and number must serve a pillar, or it's scope creep.

Examples:
- "Tense, deliberate combat where positioning beats reflexes."
- "Every run is different; mastery is learning the system, not the map."
- "You always feel powerful, but the world scales to stay threatening."

Use pillars to settle arguments: "Does this feature serve a pillar? Which one? If none — cut it."

---

## The core loop

The repeated moment-to-moment verb cycle the player does for most of the playtime. Define it before any content.

```
explore → encounter → fight → loot → upgrade → (back to explore)
```

- Name each verb and what makes it satisfying (game feel).
- The loop must be fun in isolation BEFORE you design breadth on top of it — prototype it (hand to Forge).
- Nest loops: second-to-second (move/aim) inside minute-to-minute (clear a room) inside session (finish a run) inside meta (unlock permanently).

---

## MDA framework

Mechanics → Dynamics → Aesthetics. Designers build mechanics; players experience aesthetics; dynamics emerge in between.

| Layer | Definition | Designer control |
|-------|-----------|------------------|
| Mechanics | The rules and systems (the verbs, the numbers) | Direct |
| Dynamics | Runtime behavior that emerges from mechanics + players | Indirect (you tune mechanics) |
| Aesthetics | The felt experience (tension, mastery, fellowship, discovery) | The goal you design toward |

Design backward from the target aesthetic to the mechanics likely to produce it, then playtest to see the actual dynamics.

---

## Mechanic & game-feel design

- A mechanic = a player **verb** + its rules + its feedback. "Jump" is hold-time → height, coyote-time, landing squash, sound.
- **Game feel** is the feedback layer (animation, audio, screen shake, input responsiveness). Design the hook points; the feel itself is implemented (Tick) and tuned by playtest. Audio/visual assets come from asset agents.
- Prefer **few deep mechanics** that interact over many shallow ones. Interaction creates emergence (the good kind of surprise).
- Spell out system interactions explicitly: does fire + oil = spread? Define the matrix.

---

## Scope & vertical slice

Scope kills more games than bad design. Control it:
- **Vertical slice**: one fully polished slice (one level, the core loop, real art/audio hooks) that proves the game is fun before building breadth.
- **Content budget**: estimate cost-per-unit (level, enemy, item) × count against team/time. If it doesn't fit, cut count or scope, not polish.
- Flag scope creep against pillars; propose a smaller shippable core.

---

## GDD outline

```
1. Pillars & target experience
2. Core loop (verb cycle, nested loops)
3. Mechanics (verbs, rules, interactions)
4. Progression (session + meta)
5. Economy (resources, sinks/sources)
6. Levels / content (types + budget)
7. Narrative / world (if any)
8. Win / lose conditions
9. Balance model (tables/curves) → balance-and-economy.md
10. Risks & open playtest questions
```

---

## Pitfalls

- Designing content/breadth before proving the core loop is fun.
- Pillar-less feature creep ("wouldn't it be cool if…").
- Mechanics defined without their feedback/feel hook points.
- A GDD nobody updates → drifts from the build.
- Many shallow mechanics instead of few interacting deep ones.
- Scope with no vertical slice → no proof of fun until too late.
