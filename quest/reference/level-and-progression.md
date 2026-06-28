# Level & Progression

**Purpose:** Level/encounter design, difficulty pacing, tutorialization, and progression/reward loops.
**Read when:** Designing levels, progression, or retention pacing (`level` / `progression` recipes).

## Contents
- Progression vs level design
- Progression curves
- Unlock trees
- Reward & retention loops
- Level/encounter design
- Difficulty pacing
- Tutorialization
- Pitfalls

---

## Progression vs level design

- **Progression** = how the player (and their power/options) grows over the whole game: XP, levels, unlocks, gear.
- **Level/encounter design** = the moment-to-moment space and challenges within a session.
Both serve pacing; design them together so power growth and challenge growth track the intended difficulty band (see balance-and-economy.md).

---

## Progression curves

- Pick an XP/level curve shape: linear (steady), exponential (slows over time — classic RPG), or front-loaded (fast early wins for onboarding).
- `xp_to_next(level) = base * growth^level` — tune `growth` so early levels are quick (hook the player) and later levels pace the endgame.
- Tie each level/unlock to a *meaningful* change (new verb, new option), not just bigger numbers. "+5% damage" every level is hollow.

---

## Unlock trees

- Gate new mechanics/content behind progression to control complexity intake (don't dump all systems at once).
- Branching trees create build identity and replay; linear unlocks are simpler and guarantee pacing.
- Avoid prerequisite mazes; keep the critical path legible. Mark optional/power-user branches.

---

## Reward & retention loops

Nest reward cadence so there's always a "next thing":
| Loop | Cadence | Reward |
|------|---------|--------|
| Micro | seconds | hit feedback, pickups |
| Session | minutes | level cleared, gear, level-up |
| Meta | sessions | unlocks, prestige, new modes |

- **Variable rewards** (loot rarity) drive engagement but design against frustration (pity timers / bad-luck protection).
- Retention loops (daily goals, energy regen) should respect the player; avoid dark patterns and grind walls.

---

## Level/encounter design

- **Critical path vs optional**: guarantee the experience on the path; reward exploration off it.
- Compose encounters from a vocabulary (enemy types, hazards) the player has been taught.
- Introduce → develop → twist → rest: teach a concept safely, develop it, combine/subvert it, then give a breather.
- Pace **tension and release** — peaks (boss, gauntlet) need valleys (safe room, story beat) around them.

---

## Difficulty pacing

- Shape difficulty as a rising sawtooth: each new area spikes, then the player's growth eases it, then the next area spikes higher.
- Provide difficulty options or dynamic adjustment if the audience is broad; keep the *intended* experience as the default.
- Place save/checkpoint cadence to match challenge — punishing setbacks belong only where mastery is the pillar.

---

## Tutorialization

- Teach a verb in a **safe** context before testing it under pressure.
- Prefer "show, let them try, then test" over text walls. Design the first encounter of each mechanic as its lesson.
- Don't tutorialize everything up front — teach just-in-time, gated by the unlock tree.

---

## Pitfalls

- Power growth that outpaces or lags challenge growth → trivial or unfair (see difficulty band).
- Levels that test a mechanic before teaching it.
- All systems unlocked at once → overwhelm.
- Hollow progression (+numbers with no new decisions).
- Retention loops that cross into dark patterns / grind walls.
- No tension/release rhythm → fatigue.
