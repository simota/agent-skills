# ECS Patterns

**Purpose:** Entity Component System architecture — storage models, system scheduling, query iteration, and when ECS is (and isn't) worth it.
**Read when:** Designing or implementing an ECS (`ecs` recipe).

## Contents
- What ECS is
- When to use ECS vs OOP
- The three parts
- Component storage models
- System scheduling
- Queries / iteration
- Relationships & hierarchy
- Pitfalls

---

## What ECS is

ECS is **composition over inheritance** taken to a data-oriented extreme:
- **Entity** — just an ID (often `{index, generation}` to detect stale references).
- **Component** — plain data, no behavior (`Position`, `Velocity`, `Health`).
- **System** — behavior: a function that iterates all entities matching a component query and mutates their components.

Entities have no methods. Logic lives in systems; data lives in components. This separates *what an entity is* (its set of components) from *what happens to it* (systems), and lays data out for cache-friendly iteration.

---

## When to use ECS vs OOP

ECS is not free — it adds indirection and upfront structure. Choose by the real profile:

| Signal | Favors ECS | Favors OOP / component-object |
|--------|-----------|------------------------------|
| Entities iterated per frame | Thousands+ | Hundreds |
| Hot path | Tight loops over homogeneous data | Mixed, branchy per-object logic |
| Runtime composition | Add/remove capabilities dynamically | Fixed-ish entity types |
| Team / engine | Custom engine, Bevy, DOTS, EnTT, flecs | Unity GameObject, Godot Node, fast iteration |

**Hybrid is legitimate:** OOP shell for gameplay objects, with the hot systems (particles, projectiles, boids) moved into data-oriented arrays. Don't ECS a game with 200 entities just for purity.

---

## The three parts

```ts
type Entity = number;                 // or { index, generation }
interface Position { x: number; y: number }
interface Velocity { dx: number; dy: number }

// System: query (Position, Velocity) → integrate
function movementSystem(world: World, dt: number) {
  for (const e of world.query(Position, Velocity)) {
    const p = world.get(e, Position);
    const v = world.get(e, Velocity);
    p.x += v.dx * dt;
    p.y += v.dy * dt;
  }
}
```

---

## Component storage models

The storage model is the central ECS decision. Pick against your add/remove churn and iteration pattern.

| Model | Layout | Iteration speed | Add/remove cost | Best for |
|-------|--------|-----------------|-----------------|----------|
| **Sparse set** | Per-component dense array + sparse index | Fast (dense per component) | Cheap (swap-remove) | High component churn; most general-purpose ECS |
| **Archetype** (table) | Entities grouped by exact component set | Fastest for full-match queries (SoA, contiguous) | Costly (move entity between tables on add/remove) | Stable component sets, many query-matched iterations |
| **Bitset + array-of-structs** | One array, bitmask of present components | Simple, branchy | Cheap | Small projects, few component types |

Rules of thumb:
- High churn (components added/removed constantly) → **sparse set**.
- Stable sets, query-heavy, max throughput → **archetype**.
- State the choice with a one-line justification in the deliverable.

---

## System scheduling

- **Explicit, fixed order** when determinism matters (lockstep/replays). Order is part of the contract — document it.
- Group systems into stages: `input → simulation (physics, AI, gameplay) → resolution → render-prep`.
- **Parallelism**: systems with disjoint component access can run on different threads; conflicting writes must serialize. Only parallelize after profiling — for most games a well-ordered single thread is enough and keeps determinism simple.
- Run simulation systems inside the fixed-timestep step (see `game-loop-and-time.md`); render-prep systems run once per render frame.

---

## Queries / iteration

- A query is "all entities having components A, B, … (and optionally *not* C)".
- Archetype storage answers full-match queries by iterating matching tables — no per-entity check.
- Sparse-set storage iterates the **smallest** component set and checks membership in the others.
- Cache `query` results' shape, not the entity list, if entities churn each frame.
- Avoid structural changes (add/remove component, despawn) *mid-iteration* — buffer them as commands and apply at a stage boundary (a "command buffer"). This prevents iterator invalidation and keeps order deterministic.

---

## Relationships & hierarchy

ECS has no built-in parent/child. Common patterns:
- **Parent component**: `Parent { entity }` + a transform-propagation system that walks parents in topological order.
- **Relationship pairs** (flecs-style): components keyed by a target entity.
- Keep transforms as `LocalTransform` + computed `WorldTransform`; recompute world from local each frame in a dedicated system.

---

## Pitfalls

- **Premature ECS**: hundreds of entities don't need it; you pay complexity for no cache win.
- **Logic in components**: components are data; behavior belongs in systems.
- **Structural changes mid-iteration**: invalidates iterators / non-deterministic — use a command buffer.
- **Stale entity IDs**: reuse without a generation counter causes "wrong entity" bugs — use `{index, generation}`.
- **Unordered iteration in a deterministic sim**: hash-map iteration order varies — iterate dense arrays in stable order.
- **One giant "GameState" component**: defeats the point; split into the components systems actually query.
