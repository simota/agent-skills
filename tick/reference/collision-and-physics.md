# Collision & Physics

**Purpose:** Broadphase + narrowphase collision, fixed-step physics integration, and the engine-vs-handroll decision.
**Read when:** Implementing collision detection or integrating physics (`physics` recipe).

## Contents
- Run physics in the fixed step
- Two-phase collision
- Broadphase techniques
- Narrowphase tests
- Resolution
- Tunneling & CCD
- Engine vs hand-roll
- Determinism notes
- Pitfalls

---

## Run physics in the fixed step

Physics integration and collision belong inside `simulate(FIXED_DT)` (see `game-loop-and-time.md`), never the render step. A fixed step gives stable, reproducible contacts; a variable step makes restitution and friction frame-rate-dependent and can blow up at low FPS.

```
simulate(dt):
  integrate velocities        # apply forces/gravity: v += a*dt
  broadphase()                # find candidate pairs
  narrowphase(candidates)     # exact tests → contacts
  resolve(contacts)           # separate + apply impulses
  integrate positions         # p += v*dt (or before resolve, engine-dependent)
```

---

## Two-phase collision

Testing every pair is O(n²). Split into:

| Phase | Goal | Output |
|-------|------|--------|
| **Broadphase** | Cheaply reject pairs that can't touch | Candidate pair list |
| **Narrowphase** | Exact test on candidates | Contact points + normals + penetration |

---

## Broadphase techniques

| Technique | Best for | Notes |
|-----------|----------|-------|
| **Uniform spatial hash** (grid) | Many similar-sized objects, roughly uniform density | Pick cell ≈ average object size; O(n) build, near-O(1) neighbor query |
| **Quadtree / octree** | Highly non-uniform density, large empty areas | Rebuild or update per frame; depth cap to bound cost |
| **Sweep and prune (SAP)** | Objects that move little frame-to-frame | Sort AABB endpoints on an axis; exploit temporal coherence |
| **BVH (AABB tree)** | Static geometry, raycasts | Great for static world; costly to rebuild for dynamic |

Default: **spatial hash** for dynamic arcade/2D games; **BVH** for static world + raycasts. State the choice and the cell/leaf sizing.

---

## Narrowphase tests

- **AABB vs AABB**: axis-aligned box overlap — cheapest; good for many 2D games and as a pre-test.
- **Circle/Sphere**: distance vs radius sum — cheap, rotation-free.
- **SAT (Separating Axis Theorem)**: convex polygon/polyhedron overlap + minimum translation vector (MTV) for resolution.
- **Segment/ray casts**: bullets, line-of-sight, ground checks.
- Return a **contact**: point(s), normal, penetration depth — resolution needs all three.

---

## Resolution

- **Positional**: push shapes apart along the normal by the penetration depth (MTV). Split correction by inverse mass for two dynamic bodies.
- **Impulse**: change velocities along the normal using restitution (bounciness) and along the tangent using friction.
- **Iterations**: stacking/jointed scenes need several solver iterations per step for stability — this is where hand-rolling gets hard; prefer an engine.
- Static bodies have infinite mass (don't move); triggers detect overlap but don't resolve.

---

## Tunneling & CCD

A fast object can pass through a thin wall in one step (its position jumps across). Mitigations:
- **Smaller fixed step** or sub-stepping for fast bodies.
- **Swept tests** / **CCD** (continuous collision detection): test the motion segment, not just the end position.
- **Raycast-ahead** for bullets: cast from prev to curr position instead of moving a body.

---

## Engine vs hand-roll

| Need | Choose |
|------|--------|
| Stacking, joints, ragdolls, stable restitution, CCD | **Engine** (Box2D, Rapier, Jolt, PhysX, Chipmunk) |
| Simple arcade collision (overlap, push-out, triggers) | **Hand-roll** AABB/circle + spatial hash |
| Deterministic lockstep across platforms | Engine with a deterministic/fixed-point mode, or a carefully hand-rolled fixed-point sim |

Hand-rolling a *stable, general* rigid-body solver is a large, bug-prone effort — integrate a proven engine unless collision is genuinely simple. Either way, step it at fixed `FIXED_DT`.

---

## Determinism notes

For lockstep/rollback netcode and replays:
- Floating-point results can differ across CPUs/compilers → use a **deterministic** physics build, or **fixed-point** math.
- Fix the **iteration order** of pairs and contacts (stable sort by entity id), not hash order.
- Seed any randomness in the solver.
- Verify by replaying the same input log and diffing the resulting state hash.

---

## Pitfalls

- Physics in the render step → unstable, non-deterministic contacts.
- O(n²) pair testing → fine at 50 objects, dies at 5000; add broadphase early.
- No CCD for fast/thin objects → tunneling.
- Cell size far from object size in a spatial hash → degenerate buckets.
- Mixing units (pixels vs meters) → engines expect consistent scale; pick one.
- Assuming float determinism across platforms → it isn't guaranteed.
