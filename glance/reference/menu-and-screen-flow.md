# Menus & Screen Flow

**Purpose:** Screen-state mapping, menu types, common game-screen patterns, and navigation depth.
**Read when:** Designing menus, screen flow, or in-game panels (`menu` recipe).

## Contents
- Model menus as a screen-state map
- Screen inventory
- Per-screen contract
- Common screen patterns
- Navigation depth
- Modals, overlays & pause
- Pitfalls

---

## Model menus as a screen-state map

A game's menus form a state machine, not a loose pile of panels. Define which screen is active, what transitions open/close it, and what the back/cancel button does at every node. (For complex flows, hand the transition table to Weave to verify reachability; Tick implements.)

```
Title ──Play──▶ Save Select ──▶ Game (HUD)
  │                                 │
  └──Settings──▶ Settings           ├─Start/Pause──▶ Pause ──Resume──▶ Game
                   │                 │                  │
                   └─Back─▶ Title    │                  ├─Settings──▶ Settings
                                     │                  └─Quit──▶ Title (confirm)
                                     ├─Tab──▶ Inventory / Map / Skills
                                     └─Interact──▶ Shop / Dialogue
```

---

## Screen inventory

Typical game screens — include only what the game needs:
- **Front-end**: title, save/profile select, settings, credits, extras.
- **In-game core**: HUD (not a menu), pause.
- **In-game panels**: inventory, map, skill/tech tree, character/equipment, quest log, codex/journal.
- **Transactional**: shop/store, crafting, dialogue, level-up/allocation.
- **System**: settings (display/audio/controls/accessibility/gameplay), save/load, confirm dialogs.

---

## Per-screen contract

Every screen specifies:
- **Open/close**: what opens it, what closes it, and the back/cancel target.
- **Default focus**: where focus lands on open (controller) — never "nothing focused".
- **Action set**: the actions available and their button bindings + on-screen prompts.
- **Persistence**: does it pause the game? Does game state keep simulating behind it (see HUD glanceability for transparent overlays)?

---

## Common screen patterns

| Screen | Key design notes |
|--------|------------------|
| **Settings** | Grouped tabs (Display / Audio / Controls / Accessibility / Gameplay); apply/revert; show current values; remember last tab |
| **Inventory** | Grid or list; sort/filter; item detail panel; compare-to-equipped; quick-actions; stack handling |
| **Skill/tech tree** | Clear prerequisites and current node; legible at zoom; respec affordance; preview effects |
| **Map** | Pan/zoom, legend, fast-travel nodes, markers/filters, "you are here", objective overlay |
| **Shop** | Buy/sell tabs, price + owned currency always visible, can-afford state, confirm on spend |
| **Dialogue** | Speaker clarity, choice list with focus, history/backlog, skip/auto, branching legibility |
| **Save/Load** | Slot metadata (time, location, playtime, screenshot), overwrite confirm, autosave indicator |

---

## Navigation depth

- Every extra menu level is a cost (more button presses, more "where am I"). Keep depth shallow.
- Surface frequent actions at the top level; bury rare ones.
- Provide shortcuts: tab-switching between sibling panels (Inventory↔Map↔Skills) without going back to a hub.
- Show a breadcrumb or clear title so the player always knows the current screen and how to exit.
- Consistent back/cancel binding everywhere — the player should never wonder how to back out.

---

## Modals, overlays & pause

- **Pause**: stops simulation, keeps the world visible behind a dim; resume returns to exact state.
- **Transparent overlays** (radial menu, ping wheel) may keep the game running — decide deliberately and state it.
- **Confirm dialogs**: reserve for destructive/irreversible actions (overwrite save, quit without saving, spend rare currency). Default focus on the safe option.
- Don't stack deep modal chains; each modal needs an obvious dismiss.

---

## Pitfalls

- Menus designed as panels with no defined transitions → dead ends, inconsistent back behavior.
- No default focus on open (controller user faces a screen with nothing selected).
- Inconsistent back/cancel binding across screens.
- Deep nesting for frequent actions.
- Confirm dialogs defaulting to the destructive option.
- Settings that don't show current values or can't revert.
- Inventory/shop without "can I afford / is it equipped" at-a-glance state.
