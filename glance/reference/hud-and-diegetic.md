# HUD & Diegetic UI

**Purpose:** The diegetic taxonomy, HUD layout/anchors, glanceability, information hierarchy under action, and genre HUD patterns.
**Read when:** Designing an in-game HUD or in-world UI (`hud` recipe).

## Contents
- The diegetic taxonomy
- Choosing a UI type
- HUD layout, anchors & safe areas
- Glanceability
- Information hierarchy under action
- Genre HUD patterns
- Pitfalls

---

## The diegetic taxonomy

Classify every UI element on two axes — is it part of the story world (fiction), and does it sit on the 2D screen plane or in 3D space? (Fagerholt & Lorentzon, 2009.)

| Type | In fiction? | On screen plane? | Example |
|------|------------|------------------|---------|
| **Non-diegetic** | No | Yes (2D overlay) | Health bar in the corner, classic minimap |
| **Diegetic** | Yes | No (in the world) | Ammo on the gun model, Dead Space spine health |
| **Spatial** | No | In 3D space | Floating waypoint over a door, enemy nameplate |
| **Meta** | Yes (fiction) | Yes (2D overlay) | Blood/dirt on the "camera lens" as damage feedback |

This isn't academic trivia — it's the decision tool for *where* a piece of information lives.

---

## Choosing a UI type

Decide per element, optimizing readability first, immersion second:
- **Default to non-diegetic** for critical, must-read-instantly state (health when low, ammo in a firefight). It's the most legible.
- **Use diegetic/spatial** when the element deepens immersion AND stays glanceable (objective marker in the world, ammo on the weapon). 
- **Use meta** for ambient feedback that doesn't need precision (screen-edge damage vignette).
- Never make a *critical* element diegetic if it costs readability — immersion never outranks a player needing to read their health.
- Fewer elements, more meaning: a survival game may hide the HUD entirely and surface state diegetically; a competitive shooter needs a dense, instantly-readable non-diegetic HUD.

---

## HUD layout, anchors & safe areas

- **Anchor to corners/edges**, not the center — the center is where the player looks and acts. Keep the action-focus zone clear.
- Common anchors: health/status bottom-left, ammo/resources bottom-right, minimap top-corner, objectives top-center or top-left, hotbar bottom-center.
- **Title/TV safe area**: on console/TV, keep all UI inside ~90% of the screen (overscan). Critical text inside ~80%.
- **Resolution & aspect scaling**: design with anchors + relative units so the HUD holds from 16:9 to ultrawide and handheld; specify what scales vs what stays fixed-size (text legibility floor).
- Provide a **HUD scale** option (accessibility + preference).

Always deliver a wireframe (ASCII or sketched) showing anchors and the safe-area box, e.g.:

```
┌─────────────────────────────────────────────┐  ← screen
│ [objectives]                       [minimap] │
│                                              │
│                    (action                   │
│                     focus —                  │
│                     keep clear)              │
│                                              │
│ [health][status]            [ammo][resource] │
└─────────────────────────────────────────────┘
   └──────────── title-safe ~90% ───────────┘
```

---

## Glanceability

The defining game-UI metric: can the player parse the element in <1 second while busy?
- **Contrast**: HUD must read over any background (bright sky, dark cave). Use outlines, drop shadows, or semi-opaque backplates — never rely on the scene staying a certain color.
- **Position consistency**: state lives in the same place every time so the player's eye learns it (muscle memory beats reading).
- **Pre-attentive encoding**: use position, size, color, and shape so a value reads without focal attention. A health bar going red+short+pulsing is read peripherally.
- **Clutter budget**: cap simultaneous elements; progressive disclosure (show ammo detail only when relevant). Test against the busiest combat moment, not a calm screenshot.

---

## Information hierarchy under action

Rank elements by how urgently the player needs them mid-action:
1. **Survival-critical** (health when low, incoming damage direction) — most prominent, can animate/pulse.
2. **Action-critical** (ammo, cooldowns, current weapon) — clear, fixed position.
3. **Situational** (minimap, objective, score) — present but quieter.
4. **On-demand** (full map, inventory) — hidden behind a button, not on the HUD.

Hide or fade tiers 3–4 during intense moments; surface tier 1 with motion/sound only when it changes.

---

## Genre HUD patterns

| Genre | HUD signature |
|-------|---------------|
| FPS | Crosshair, ammo (bottom-right), health (bottom-left), hitmarkers, damage-direction indicator, minimap |
| RPG | Health/mana/stamina bars, hotbar, minimap, quest tracker, XP bar |
| RTS | Resource counters (top), minimap (corner), command card / unit panel (bottom), selection info |
| Survival | Minimal/diegetic; hunger/temp/stamina, often hideable; inventory-heavy |
| Racing | Speed/gear, lap/position, track map, lap times — large and peripheral |
| Card/strategy | Hand, board state, turn/phase indicator, resource pips |

Follow conventions for instant familiarity; break them only deliberately and only when the break serves a pillar (note the justification).

---

## Pitfalls

- Designing the HUD against a calm screenshot, then it's unreadable in combat.
- Center-screen UI that blocks the action-focus zone.
- Ignoring TV safe area → console UI clipped offscreen.
- Diegetic flourish that sacrifices readability of critical state.
- HUD that doesn't scale → broken on ultrawide/handheld.
- No contrast strategy → vanishes over bright/dark scenes.
- Everything always on → clutter; nothing reads at a glance.
