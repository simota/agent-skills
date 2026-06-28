# Netcode Patterns

**Purpose:** Multiplayer authority models, prediction/reconciliation, interpolation, and the determinism they require.
**Read when:** Implementing multiplayer sync foundations (`netcode` recipe).

## Contents
- Pick the authority model first
- Client-server authoritative
- Deterministic lockstep
- Rollback (GGPO-style)
- Entity interpolation & extrapolation
- Determinism requirements
- Desync detection
- Transport notes
- Pitfalls

---

## Pick the authority model first

The authority model is the **first and most consequential** netcode decision — it shapes the loop, the state representation, and the cheat surface. Resolve the `NETCODE_MODEL` trigger before writing any sync code.

| Model | Best for | Bandwidth | Latency feel | Cheat resistance | Determinism required |
|-------|----------|-----------|--------------|------------------|----------------------|
| Client-server authoritative | Action, shooters, MMO | Med–high (state) | Hidden via prediction | High (server truth) | No (server is truth) |
| Deterministic lockstep | RTS (100s–1000s of units) | Very low (inputs only) | Input delay | High (peers verify) | **Yes** |
| Rollback (GGPO) | Fighting, low-latency 1v1/2v2 | Low (inputs) | Excellent (predict + correct) | Med (peer) | **Yes** |

---

## Client-server authoritative

The server runs the authoritative simulation; clients send **inputs**, receive **state**.

Loop:
1. Client samples input, sends it (with a sequence number), and **predicts** locally (applies input immediately).
2. Server applies inputs in order, advances the authoritative sim, broadcasts snapshots (often delta-compressed) with the last-processed input seq per client.
3. Client **reconciles**: on a snapshot, snap to the authoritative state for that seq, then **replay** all unacknowledged inputs on top → smooth correction instead of a visible snap.

Key techniques:
- **Client-side prediction** hides RTT for the local player.
- **Server reconciliation** keeps the local player authoritative-correct.
- **Lag compensation** (server rewinds other entities to the shooter's view-time for hit detection).
- **Entity interpolation** for *remote* entities (below).

This is the default for most real-time games — it doesn't require a deterministic sim because the server is the single source of truth.

---

## Deterministic lockstep

Every peer runs the **same** simulation and only exchanges **inputs**. The frame advances only when all peers' inputs for that tick have arrived.

- Tiny bandwidth (inputs scale with players, not world size) — ideal for thousands of units (RTS).
- Requires **strict determinism**: identical input sequence → identical state on every machine, every platform.
- Hides latency with an **input delay** (queue inputs N ticks ahead) so the network has time to deliver them.
- A single nondeterministic op anywhere → **desync**, and the game silently diverges.

---

## Rollback (GGPO-style)

Don't wait for remote input — **predict** it (usually "same as last frame"), simulate immediately, and when the real input arrives:
- If prediction was right → nothing to do.
- If wrong → **rollback** to the last confirmed tick, re-apply correct inputs, and **resimulate** forward to now, all within one frame.

Requirements:
- Deterministic simulation.
- **Fast** save/restore of full game state (rollback happens every time a prediction misses; budget it).
- Bounded rollback window (max prediction frames).

Gives near-zero perceived input latency; best for fast 1v1 fighting games.

---

## Entity interpolation & extrapolation

Remote entities arrive at the network tick rate (e.g., 20 Hz), but you render at 60–144 Hz:
- **Interpolation**: render remote entities ~1 network-tick *in the past*, lerping between the two most recent snapshots → smooth, slightly delayed. Default for non-local entities.
- **Extrapolation (dead reckoning)**: predict ahead using last known velocity when snapshots are late → lower delay but overshoots on direction change; blend back when the snapshot arrives.

Local player uses prediction; remote players use interpolation. Don't interpolate the local player against the server — reconcile instead.

---

## Determinism requirements

Lockstep and rollback **only work** on a deterministic simulation. Checklist:
- **Seed all RNG**; advance it deterministically; sync the seed at match start.
- **Fixed update order** across systems and entities — iterate stable arrays/sorted ids, never hash-map order.
- **No wall-clock** inside the sim — drive everything from the tick count.
- **Float discipline**: floats can differ across CPUs/compilers/build flags → use a deterministic math build or **fixed-point** arithmetic for the sim.
- Same binary/version on all peers, or a versioned protocol guard.

Client-server does **not** require determinism (server is truth) but benefits from it for replay/debug.

---

## Desync detection

- Each peer hashes its game state every N ticks and exchanges the hash; mismatch → desync detected early.
- On desync: log the diverging tick, dump both states, and (in dev) bisect which system/component diverged.
- Treat any nondeterministic call found this way as a P0 — it will recur.

---

## Transport notes

- **UDP** (or reliable-UDP layers: ENet, QUIC, WebRTC DataChannel, WebTransport) for real-time — TCP head-of-line blocking adds latency under loss.
- Inputs/states are often sent **unreliable + redundant** (resend last N inputs each packet) rather than reliable-ordered.
- Separate reliable channel for lobby/chat/match setup.
- Always validate/clamp received input server-side — never trust the client in authoritative mode.

---

## Pitfalls

- Choosing the model late → rearchitecting mid-project.
- Lockstep/rollback on a non-deterministic sim → silent desyncs.
- Interpolating the local player → laggy, mushy controls; predict + reconcile instead.
- No state hashing → desyncs found only by players, never reproduced.
- Trusting client input in authoritative mode → trivial cheating.
- Rollback without fast state save/restore → frame spikes on every misprediction.
- Sending full state when inputs would do (lockstep) → wasted bandwidth.
