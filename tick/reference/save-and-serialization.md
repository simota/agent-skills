# Save & Serialization

**Purpose:** Versioned save schemas, forward migration, simulation-vs-render state, and the replay save format.
**Read when:** Implementing save/load or serialization (`save` recipe).

## Contents
- The save is a versioned contract
- Save the simulation, not the engine
- Separate "what" from "how"
- Versioning & forward migration
- Snapshot vs replay saves
- Atomicity & corruption
- Determinism interplay
- Pitfalls

---

## The save is a versioned contract

A save file is read by *future* versions of the game whose data shape has changed. Treat it as a long-lived contract:

```jsonc
{
  "version": 7,            // REQUIRED — drives migration
  "savedAtTick": 184320,
  "world": { /* game state */ }
}
```

Without a `version`, the first schema change either breaks every existing save or forces fragile "guess the shape" parsing. Add it from day one.

---

## Save the simulation, not the engine

Serialize **game/simulation** state, never engine/render objects:
- ✅ entity ids, components (position, health, inventory), RNG seed + counter, tick, score.
- ❌ render handles, texture/material refs, node pointers, GPU buffers, scene-graph nodes.

On load, **reconstruct** the render/engine layer from the simulation state. This keeps saves portable across engine versions and platforms, and is exactly the boundary that makes the core headless-testable.

---

## Separate "what" from "how"

Two independent concerns:
- **What to save** — the schema: which fields, their meaning, the version.
- **How to encode** — JSON (debuggable, larger), MessagePack/CBOR/binary (compact, fast), compressed (gzip/zstd).

Define the schema in code (a serialize/deserialize pair per type) and keep encoding swappable. You can ship JSON in dev and binary in release without touching the schema.

---

## Versioning & forward migration

On load, migrate **forward one version at a time** to the current version:

```ts
function migrate(save) {
  let s = save;
  if (s.version === 5) s = v5_to_v6(s);   // e.g., split `name` into first/last
  if (s.version === 6) s = v6_to_v7(s);   // e.g., add default `difficulty`
  // s.version is now CURRENT
  return s;
}
```

Rules:
- Each migration is small, pure, and tested with a real old save fixture.
- Never edit an old migration after release — it has already run on players' files; add a new one.
- Adding a field → default it in migration. Removing → drop it. Renaming → copy then drop.
- Refuse to load a `version` **newer** than the build (a newer save in an older client) with a clear message rather than silently corrupting.

---

## Snapshot vs replay saves

| Type | Stores | Size | Use |
|------|--------|------|-----|
| **Snapshot** | Full world state at a moment | Large | Quicksave/load, checkpoints |
| **Replay** | `{seed, startState, inputLog}` | Tiny | Replays, lockstep, regression tests, anti-cheat |

A **deterministic** simulation enables replay saves: store the seed and the per-tick input log; replaying the inputs reproduces the exact game. This is also the strongest determinism test — replay an input log and assert the final state hash matches. Replays break if determinism breaks, so version the sim and refuse cross-version replay.

---

## Atomicity & corruption

- **Write atomically**: write to a temp file, fsync, then rename over the real file — a crash mid-write must not destroy the previous good save.
- Keep the previous save as a backup (`save.bak`) and roll back on load failure.
- Store a checksum/hash to detect corruption; on mismatch, fall back to backup and warn.
- Autosave on a timer/checkpoint, not only on quit (crashes lose unsaved progress).

---

## Determinism interplay

- Persist the **RNG seed and its advance count** so a loaded game continues the same random sequence.
- Persist the **tick** so timers and scheduled events resume correctly.
- For replays, the input log must be captured in the same fixed order the sim consumes it.
- If the sim isn't deterministic, replay saves aren't an option — use snapshots.

---

## Pitfalls

- **No version field** → first schema change breaks all saves.
- Serializing engine/render objects → unportable, breaks on engine upgrade.
- Editing a shipped migration → corrupts files that already migrated.
- Non-atomic write → a crash bricks the save.
- Loading a newer-version save silently → undefined fields, subtle corruption.
- Replay saves on a non-deterministic sim → diverging playback.
- Saving wall-clock time as game time → resumes wrong after a load.
