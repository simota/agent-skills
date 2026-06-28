# Game Loop & Time

**Purpose:** Timestep strategies, the canonical fixed-timestep accumulator, render interpolation, frame pacing, and time control.
**Read when:** Building or fixing the game loop (`loop` recipe).

## Contents
- The core problem
- Timestep strategies
- Canonical fixed-timestep loop
- Render interpolation
- Spiral of death
- Frame pacing
- Time scaling & pause-aware timers
- Pitfalls

---

## The core problem

A frame does two distinct jobs — **advance the simulation** and **draw it**. If you couple them (advance the world by "however long the last frame took"), the game behaves differently at different frame rates: physics tunnels at low FPS, runs fast on a 240 Hz monitor, and is non-deterministic. The fix is to advance the simulation in **fixed-size steps** and decouple drawing from it.

Reference: Glenn Fiedler, "Fix Your Timestep!" — the accumulator pattern below is the canonical solution.

---

## Timestep strategies

| Strategy | How it advances | Use when | Failure mode |
|----------|-----------------|----------|--------------|
| Variable | `update(frameTime)` once per frame | Trivial games, no physics, no determinism | Physics explodes/tunnels under FPS swings; non-deterministic |
| Fixed + interpolation | N fixed steps per frame, render interpolates | Default for physics/determinism/netcode | Needs prev+curr state for interpolation |
| Semi-fixed | Fixed sub-steps until frame budget consumed | Want fixed physics, no interpolation code | Visual stutter (no interpolation) |
| Fixed, no interpolation | One fixed step, render current | Sim rate == display rate and locked | Judder if display rate drifts |

Default: **fixed timestep + interpolation**.

---

## Canonical fixed-timestep loop

```ts
const FIXED_DT = 1 / 60;   // seconds per simulation step
const MAX_FRAME = 0.25;     // clamp the largest delta we'll honor
const MAX_STEPS = 5;        // cap catch-up iterations per frame

let accumulator = 0;
let prevState, currState;   // for interpolation

function frame(now, prev) {
  let frameTime = (now - prev) / 1000;
  frameTime = Math.min(frameTime, MAX_FRAME);   // (1) clamp delta
  accumulator += frameTime;

  let steps = 0;
  while (accumulator >= FIXED_DT && steps < MAX_STEPS) {  // (2) cap catch-up
    prevState = currState;
    currState = simulate(currState, FIXED_DT);  // (3) pure fixed-step advance
    accumulator -= FIXED_DT;
    steps++;
  }
  if (steps === MAX_STEPS) accumulator = 0;      // (4) drop debt after a spike

  const alpha = accumulator / FIXED_DT;          // (5) leftover fraction
  render(prevState, currState, alpha);           // (6) interpolate
}
```

Each numbered guard matters:
1. **Clamp** stops a 5-second stall (debugger, tab switch) from advancing the world 5 seconds in one frame.
2. **Cap** bounds how many sim steps one frame can run.
3. `simulate` is the only place game logic, physics, and netcode advance — always by `FIXED_DT`.
4. After hitting the cap, drop the leftover accumulator so the game slows down instead of spiraling.
5. `alpha ∈ [0,1)` is how far between the last two sim states "now" is.
6. Rendering reads two states and interpolates — visuals are smooth even though the sim is discrete.

---

## Render interpolation

The simulation runs at 60 Hz but the display might be 144 Hz; without interpolation the eye sees the same sim frame repeated, causing judder. Interpolate render-only quantities (position, rotation) between `prevState` and `currState`:

```ts
renderPos = lerp(prev.pos, curr.pos, alpha);
renderRot = slerp(prev.rot, curr.rot, alpha);
```

Interpolate **presentation**, never the simulation. Do not feed interpolated values back into game logic. For values that snap (teleport, respawn), skip interpolation that frame (set `prev = curr`).

Alternative: **extrapolation** (predict ahead of `curr`) reduces latency but overshoots on direction changes — prefer interpolation unless input latency is critical (then see netcode prediction).

---

## Spiral of death

If one sim step takes longer than `FIXED_DT`, the accumulator grows faster than the loop drains it → more steps next frame → even slower → unrecoverable. Prevention:
- **Cap** catch-up iterations (`MAX_STEPS`).
- After hitting the cap, **discard** remaining accumulator (game slows; it does not freeze).
- Keep `simulate(FIXED_DT)` comfortably under `FIXED_DT` in wall-clock; profile the hot systems (hand off to Bolt).

---

## Frame pacing

- Drive the loop from `requestAnimationFrame` (web) / engine vsync callback / a high-resolution monotonic clock — never `setInterval`/`setTimeout` for the render loop (drifts, batches).
- Use a **monotonic** clock (`performance.now`, not `Date.now`) so NTP adjustments and DST can't move time backward.
- On fixed-refresh platforms, align `FIXED_DT` to a divisor of the refresh rate (1/60, 1/120) to minimize beat patterns.

---

## Time scaling & pause-aware timers

- Keep a `timeScale` multiplier applied to `FIXED_DT` for slow-motion/fast-forward: `simulate(FIXED_DT * timeScale)`. For determinism in replays, log the scale per tick.
- **Pause** = stop calling `simulate`, keep calling `render`. Gameplay timers must count *simulation* time (accumulated `FIXED_DT`), never wall-clock, so pausing actually pauses them.
- Distinguish **game time** (scales, pauses) from **real time** (UI animations, network timeouts) — keep two clocks.

---

## Pitfalls

- Using wall-clock delta directly for movement (`pos += velocity * frameTime`) — frame-rate-dependent and non-deterministic.
- Forgetting the accumulator cap → spiral of death on any hitch.
- Interpolating simulation state instead of render state → physics drift.
- Reading `Date.now()` inside the sim → breaks determinism and pause.
- Running physics in the render step instead of the fixed step → variable substeps, unstable contacts.
