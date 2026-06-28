# Game UI Heuristics

**Purpose:** Usability heuristics for game UI, glanceability evaluation, genre conventions, and a playtest/eval plan.
**Read when:** Auditing an existing game UI or framing a new design (`audit` recipe, FRAME phase).

## Contents
- Why game UI heuristics differ
- Game UI heuristics
- Glanceability evaluation
- Genre conventions catalog
- Playtest / evaluation plan
- Common pitfalls

---

## Why game UI heuristics differ

General usability heuristics (Nielsen) apply, but games add constraints: the UI competes with real-time action, runs on a controller without a cursor, must work on a TV across the room, and serves immersion as well as function. Game-specific heuristic sets (PLAY heuristics; Desurvire's HEP/GAP; Pinelle's game usability heuristics) exist for this reason. Evaluate against both general and game-specific lenses.

---

## Game UI heuristics

1. **Glanceable** — critical state reads in <1s during action (position, contrast, pre-attentive encoding).
2. **Consistent position** — state lives in the same place every time; the eye learns it.
3. **Input-appropriate** — focus-navigable on controller, thumb-reachable on touch, hotkey-rich on PC; correct glyphs.
4. **Immediate feedback** — every action produces instant, legible feedback (hit, pickup, error, cooldown).
5. **Minimal & relevant** — only show what serves an in-the-moment decision; progressive disclosure for the rest.
6. **Forgiving** — confirm destructive actions; easy undo/back; no punishing mis-taps.
7. **Accessible** — never single-channel; remappable; scalable; subtitled (see game-accessibility.md).
8. **Legible over immersive** — diegetic flair never costs readability of critical state.
9. **Teachable in context** — new UI/verbs taught just-in-time, not in a wall of text.
10. **Safe-area & scale clean** — holds across resolutions/aspect ratios and inside TV safe area.

---

## Glanceability evaluation

A focused way to test the core game-UI metric:
- **Squint test**: blur/squint at the HUD — do the critical elements still read by shape/position/color? 
- **Worst-case test**: evaluate during the busiest combat/action moment, not a calm screenshot.
- **Background test**: overlay the HUD on the brightest and darkest scenes — does contrast hold?
- **Peripheral test**: with eyes on the action-focus center, is health/threat readable in peripheral vision?
- **Time-to-parse**: can a new player state their health/ammo/objective within 1 second?

---

## Genre conventions catalog

Players carry expectations from the genre; meet them for instant familiarity, break them only deliberately.

| Genre | Conventions players expect |
|-------|---------------------------|
| FPS | Crosshair, bottom-corner ammo/health, hitmarkers, damage-direction indicator, killfeed |
| Action RPG | Bars (HP/MP/stamina), hotbar/abilities, minimap, quest tracker, loot rarity colors+icons |
| RTS | Top resource bar, corner minimap, bottom command card, drag-select, control groups |
| Survival/crafting | Hideable/diegetic status (hunger/temp), heavy inventory + crafting grid, hotbar |
| Fighting | Health + super meter top corners facing inward, round timer center-top, combo counter |
| Racing | Large peripheral speed/gear/lap, track map, position |
| Strategy/card | Hand, board state, turn/phase indicator, resource pips, end-turn affordance |
| Puzzle/casual | Big touch targets, minimal HUD, clear goal + moves/score |

---

## Playtest / evaluation plan

Frame how the UI design will be validated (hand execution to Echo for persona walkthroughs):
- **Tasks**: "find your current objective", "equip a better weapon", "change a control binding", "tell me your health" — time and observe.
- **First-time-user (FTUE)**: can a new player navigate the menus and read the HUD without help?
- **Controller-only pass**: complete every task on a gamepad with no mouse — flag any dead ends or unreachable elements.
- **Accessibility pass**: simulate colorblindness; verify nothing critical is color-only; check text scaling and captions.
- **Metrics**: time-to-parse HUD, menu task completion rate, navigation errors, back-out failures.

---

## Common pitfalls

- Evaluating UI on calm screenshots instead of the worst-case action moment.
- Mouse-first design shipped to console without a focus model.
- Wrong/!mismatched button glyphs for the platform.
- Color-only encoding (fails the colorblind pass).
- HUD clutter — everything always on, nothing reads at a glance.
- Deep menus for frequent actions; inconsistent back behavior.
- Tutorial walls of text instead of just-in-time teaching.
- Critical text in unscalable boxes that break under localization or large-text settings.
