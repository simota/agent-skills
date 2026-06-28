# Game State Patterns

**Purpose:** Screen/scene management and gameplay state machines — how to structure menus, gameplay, pause, and transitions.
**Read when:** Implementing scene/screen management or a gameplay FSM (`state` recipe).

## Contents
- Two kinds of state
- Screen state: the stack
- Gameplay state: the FSM
- Transitions
- Pause & overlays
- Sub-state nesting
- Handoff from Weave
- Pitfalls

---

## Two kinds of state

Don't conflate them:

| Kind | Granularity | Example | Structure |
|------|-------------|---------|-----------|
| **Screen / scene state** | Whole-game mode | MainMenu, Gameplay, Pause, GameOver | **Stack** of screens |
| **Gameplay state** | Per-entity behavior | Player: idle/run/jump/attack | **Finite state machine** per entity |

A pause menu is a screen pushed over gameplay; a player jump is an FSM transition. Different problems, different tools.

---

## Screen state: the stack

Model screens as a **stack**, not a flat enum, so overlays and "back" compose naturally.

```ts
interface Screen {
  enter(): void;
  exit(): void;
  update(dt: number): void;
  render(alpha: number): void;
  // control flags
  updateBelow?: boolean;   // let the screen under me keep simulating?
  renderBelow?: boolean;   // draw the screen under me (transparent overlay)?
}

class ScreenStack {
  private stack: Screen[] = [];
  push(s: Screen) { s.enter(); this.stack.push(s); }
  pop() { this.stack.pop()?.exit(); }
  replace(s: Screen) { this.pop(); this.push(s); }

  update(dt: number) {
    // update from top down until a screen blocks updateBelow
    for (let i = this.stack.length - 1; i >= 0; i--) {
      this.stack[i].update(dt);
      if (!this.stack[i].updateBelow) break;
    }
  }
  render(alpha: number) {
    // find the lowest screen to draw, then render bottom-up
    let start = this.stack.length - 1;
    while (start > 0 && this.stack[start].renderBelow) start--;
    for (let i = start; i < this.stack.length; i++) this.stack[i].render(alpha);
  }
}
```

Why a stack:
- **Pause** = push `PauseScreen` (`updateBelow=false`, `renderBelow=true`) → gameplay freezes but stays visible.
- **Back** = `pop()`.
- **Dialog/inventory** overlays compose without special-casing.

---

## Gameplay state: the FSM

Per-entity behavior is a finite state machine: states with `enter/update/exit` and guarded transitions.

```ts
type StateId = "idle" | "run" | "jump" | "attack";
interface State { enter?(): void; update(dt: number): StateId | null; exit?(): void; }

// update() returns the next state id, or null to stay
```

Keep it explicit:
- One source of truth for the current state.
- Transitions are guarded (`canJump()`); no implicit fallthrough.
- For hierarchical behavior (grounded → {idle, run}; airborne → {jump, fall}), use **nested** states rather than a combinatorial flat list.

For a **complex** gameplay FSM (many states, guards, invalid-transition risk), get the verified transition table from **Weave** and implement it here — Weave designs/verifies, Tick implements.

---

## Transitions

- **Instant**: swap state this tick.
- **Animated**: a transition is itself a short-lived screen/state (fade, slide) that, on completion, performs the actual push/pop/replace.
- During a transition, decide whether input is blocked (usually yes) and whether the underlying sim runs (usually paused).
- Make transitions **interruptible** only deliberately; uninterruptible transitions are simpler and avoid edge cases.

---

## Pause & overlays

- Pause must stop calling `simulate`, keep calling `render` (see `game-loop-and-time.md`).
- Gameplay timers count simulation time, so pause actually pauses them; UI timers (transition tweens) count real time.
- Multiple overlays (pause → settings) just stack; popping returns to the previous overlay automatically.

---

## Sub-state nesting

For an entity whose behavior has modes within modes (e.g., `Combat { aiming, firing, reloading }` inside `Alive`), nest FSMs: the parent state owns a child FSM and delegates `update` to it. Entering the parent enters the child's initial state; exiting the parent exits the active child. This keeps each level small and avoids an explosion of flat states.

---

## Handoff from Weave

```yaml
WEAVE_TO_TICK_HANDOFF:
  state_machine: "[states, events, transitions, guards]"
  validation_report: "[reachability / deadlock-free / determinism confirmed]"
  implementation_notes: "[guard/action guidance]"
# Tick implements this as a per-entity FSM; preserve the verified transition set exactly.
```

---

## Pitfalls

- Flat enum of screens → can't represent "pause over gameplay"; use a stack.
- One mega-FSM mixing screen state and gameplay state → tangled, hard to reason about.
- Implicit transitions / missing guards → entities stuck or in impossible states.
- Combinatorial state explosion → use nesting/hierarchy.
- Timers on wall-clock → don't pause; count simulation time instead.
- Forgetting `exit()` cleanup → leaked listeners, lingering effects across screens.
