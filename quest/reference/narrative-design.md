# Narrative Design

**Purpose:** Game story structure, world/lore, branching, and integrating narrative with mechanics.
**Read when:** Designing game narrative, world-building, or branching (`narrative` recipe).

## Contents
- Narrative serves the pillars
- Game narrative vs product story
- World / lore bible
- Story structure
- Branching & reconvergence
- Environmental & systemic storytelling
- Narrative–mechanics integration
- Pitfalls

---

## Narrative serves the pillars

In games, story is one system among many — it serves the design pillars and the player's experience, not the other way around. A narrative-driven game makes story a pillar; an action game keeps it light. Match narrative weight to the pillars; don't bolt on a novel.

---

## Game narrative vs product story

Distinct from **Saga** (customer/use-case stories for non-game products): Quest's narrative is in-world fiction experienced through play — characters, world, plot, and the player's agency within it. If the task is product marketing narrative, route to Saga.

---

## World / lore bible

A single source of truth for the fiction:
- **Premise & tone**: the one-line world concept and its mood.
- **Rules of the world**: what's possible (magic/tech rules), so writing stays consistent and mechanics fit the fiction.
- **Factions, places, history**: enough to be consistent, not an encyclopedia nobody reads.
- Keep it lean and living; expand only what the game actually shows.

---

## Story structure

- Choose a backbone: three-act, hero's journey, or vignette/episodic. Map beats to the progression (act breaks at major unlocks/levels).
- **Pacing with gameplay**: place story beats at tension valleys (after a boss, in a safe hub), not mid-intensity.
- Keep exposition diegetic where possible (in-world, through play) rather than cutscene dumps.

---

## Branching & reconvergence

- Define **branch points** (player choices that diverge the story) and whether/where they **reconverge** (to control content cost).
- Track state: which flags each branch sets and reads. For complex branching, hand the state machine to **Weave** to verify reachability and avoid dead/contradictory states; Tick implements it.
- Budget branches against content cost — wide branching multiplies writing/asset work fast. Prefer meaningful choices with bounded divergence.

---

## Environmental & systemic storytelling

- **Environmental**: tell story through the space (a ransacked room, a grave) — cheap, player-paced, high immersion.
- **Systemic/emergent**: let mechanics generate stories (a near-death escape). Design systems that produce memorable moments; don't script what the systems can grow.
- These scale better than branching dialogue for most games.

---

## Narrative–mechanics integration

- **Ludonarrative harmony**: the mechanics should say what the story says. A pacifist story with a kill-everything loop creates dissonance — flag it.
- Tie progression unlocks to story beats so growth feels narratively earned.
- Hand the implementable parts to Tick: dialogue/quest state as data + transitions, flags as save state (versioned).

---

## Pitfalls

- Story that fights the mechanics (ludonarrative dissonance).
- A lore bible larger than what the game ever shows.
- Branches that explode content cost without meaningful payoff.
- Exposition dumps at high-tension moments.
- Branching state with no verification → dead/contradictory paths (use Weave).
- Treating narrative as a skin instead of a system that serves the pillars.
