# Multi-Engine Riff (Parallel Brainstorm Round)

> **Filename retained** as `tri-engine-riff.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex) and tri-engine optional (Claude + Codex + agy) modes.

Implementation notes for `/riff multi`. Reads as a delta on `_common/MULTI_ENGINE_RECIPE.md` — this document only states what is **Riff-specific**. Read the common protocol first.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. dual-engine mode is NOT degraded. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Pattern type**: D (Divergence-primary). **Verb**: `riff`. **Subagent names**: `riff-codex` + `riff-claude` (dual-engine baseline) + `riff-agy` (when AVAILABLE).

**Why three engines for brainstorming.** Riff already rotates through four modes (Expand / Propose / Evaluate / Subtract). Multiplying that by three engines gives a **4 × 3 = 12-angle matrix** on a single theme — but each engine's training-data priors push each mode in a different direction (Codex tilts toward GitHub-shaped solutions, Antigravity tilts toward Google-product ergonomics, Claude tilts toward Anthropic-curated framing). The breakthrough idea usually lives in a single cell of the matrix, not at the consensus center.

**Dialogue posture.** Unlike Spark/Plea, Riff is **interactive**. `multi` is positioned as a **single "parallel brainstorm round"** dropped into an ongoing dialogue — the 9 / 12 outputs become **seed ideas for the next dialogue turn**, not a final deliverable. Riff never replaces dialogue with multi; multi accelerates one divergence step inside dialogue.

---

## Mode Coverage Toggle

Two operating modes, user-selectable at invocation:

| Invocation | Mode coverage | Fan-out shape | Use when |
|------------|---------------|---------------|----------|
| `multi` (default) | **Single mode × 3 engines** | 3 subagents on one mode (default `expand`) | Drop a 3-engine divergence round into an existing dialogue turn |
| `multi --all-modes` | **4 modes × 3 engines = 12 cells** | 3 subagents, each producing ideas for all 4 modes | Open a fresh theme; want a full matrix to harvest from |

The user (or main context interpreting dialogue signals) chooses the active mode:

| Default-mode signal | Active mode for `multi` |
|---------------------|-------------------------|
| Vague theme, early dialogue | `expand` |
| Direction clear, want options | `propose` |
| Multiple candidates, want to compare | `evaluate` |
| Over-packed, want to prune | `subtract` |

If no signal, default = `expand`. Pass the active mode to all three subagents.

---

## JSON Output Schema

Each subagent returns:

```json
{
  "engine": "codex|agy|claude",
  "active_modes": ["expand"],
  "ideas": [
    {
      "id": "codex-expand-01",
      "mode": "expand|propose|evaluate|subtract",
      "idea_text": "One sentence stating the idea or angle (problem-shaped, not solution-shaped when in expand mode)",
      "rationale": "Why this angle matters — what assumption it challenges, what reuse it exploits, what risk it surfaces",
      "connection_to_theme": "How this links back to the user's stated theme (one phrase)"
    }
  ],
  "engine_notes": "Optional: what bias this engine knows it brings (e.g., 'GitHub-heavy priors push toward dev-tool framings')"
}
```

**`id` convention**: `{engine}-{mode}-{nn}` (e.g., `agy-propose-02`). Stable IDs let the next dialogue turn cite "let's expand on `claude-expand-03`".

**Target count per subagent**:
- `multi` (single mode): 3-4 ideas per engine = 9-12 total
- `multi --all-modes`: 2-3 ideas per mode per engine = 24-36 total (cap at 36)

---

## CLUSTER Identity Rules (Riff-specific)

Two ideas match (form one cluster) when **both** hold:

1. **Same active mode** — an `expand` angle and a `propose` angle that touch the same topic are NOT the same cluster (they answer different mode-questions about the same theme).
2. **Semantic overlap on the core move** — what the idea actually asks the user to consider. Examples of matches:
   - "Reframe the export problem as a permission problem" ≡ "Maybe this isn't an export issue — it's about who can see what" (same `expand` move)
   - "Add a bulk-export action" ≡ "Background export job for large datasets" (same `propose` solution class — bulk export)
   - "Drop the dashboard tab entirely" ≡ "Remove the dashboard surface" (same `subtract` move)

**Not a match**:
- Same wording, different mode → keep separate (mode is part of cluster identity)
- Overlapping topic, different challenge axis → keep separate (e.g., "challenge the persona" vs "challenge the timing" are both `expand` but different angles)
- One concrete, one abstract framing of the same thing → match if the abstract framing clearly subsumes the concrete one

Record the engine set per cluster. Per-engine wording variants are preserved — Riff often surfaces them in dialogue as "Codex framed this as X, Claude framed it as Y — does either resonate more?".

---

## SCORE Rubric

Riff is Pattern D (Divergence-primary). Apply the base D rubric per `_common/MULTI_ENGINE_RECIPE.md`, with one Riff-specific tweak: **score within each mode, not across modes**. A `UNIVERSAL` `expand` idea is incomparable to a `VERIFIED-DIVERGENT` `subtract` idea — they serve different turns of the diamond.

| Engines in cluster (within one mode) | Label | Interpretation in Riff |
|--------------------------------------|-------|------------------------|
| 3 / 3 | `UNIVERSAL` | All three engines independently surface this angle for the same mode. Strong shared intuition — but in EXPAND mode this can also mean "obvious framing"; flag for the user as "all three engines went here first — want a less obvious angle?" |
| 2 / 3 | `LIKELY` | Two engines concur. Surface the dissenting engine's alternative angle alongside. |
| 1 / 3 (post-ground) | `VERIFIED-DIVERGENT` | Only one engine surfaced this. For Riff this is often the breakthrough — the angle the others' training data did not point at. Never auto-deprioritize. |

**Critical Riff-only inversion**: in EXPAND mode, an UNIVERSAL idea is **suspect of being the obvious framing** the user could have arrived at alone — Riff's whole job is to surface non-obvious angles. Surface UNIVERSAL EXPAND ideas, but lead the dialogue with VERIFIED-DIVERGENT ones. In SUBTRACT mode, the inversion is gentler — UNIVERSAL "this is excess" signals tend to be correct.

---

## GROUND Checks (Riff-specific)

For each `VERIFIED-DIVERGENT` candidate, the Riff main context checks:

1. **Theme connection** — does the idea actually connect back to the user's stated theme? If only loosely related, downgrade to `NEEDS-INFO` and surface as a tangent-with-question rather than a primary seed.
2. **Mode fit** — does the idea actually do what its declared mode demands? An `expand` idea that proposes a concrete solution is mis-moded; either re-tag as `propose` or drop.
3. **Hallucinated entity check** — if the idea cites a specific feature, persona, competitor, or capability the system clearly does not have, mark `REJECTED-HALLUCINATION`.
4. **Sugar-coat check** (Riff-specific) — if the idea reads as polite cheerleading without a real challenge, drop. Riff's Core Contract demands honest friction; cheerleading ideas waste a divergence slot.
5. **Duplicate-of-prior-turn check** — if the dialogue has already explored this angle, mark `REJECTED-DUPLICATE`.

For `UNIVERSAL` / `LIKELY` clusters, do only the hallucinated-entity check and the duplicate-of-prior-turn check.

---

## SYNTHESIZE — Two Output Shapes

Riff supports two synthesis outputs depending on invocation:

### Per-Mode Portfolio (default, `multi`)

A single dialogue turn containing:

- **Mode header** — which mode the round explored (e.g., "EXPAND round, 3 engines")
- **Idea cards** ordered: `VERIFIED-DIVERGENT` first (lead with breakthroughs), then `LIKELY`, then `UNIVERSAL` (Riff's inversion vs Spark)
- Each card: id, idea_text, engine-attribution tag, rationale (one line), connection_to_theme
- **Riff's framing question** — one open question per shipped idea, in Riff's voice, that pulls the user into reacting (per the Turn Structure: Receive → Challenge → Prompt)
- **Round close** — a "which 1-3 want to go deeper on?" prompt routing the next dialogue turn

The user's pick becomes the **seed for the next dialogue round** — not a multi round, but a normal Riff turn drilling into the selected idea.

### All-Modes Matrix (`multi --all-modes`)

A single dialogue turn with a 4 × N matrix:

| Mode | Universal | Likely | Verified-Divergent |
|------|-----------|--------|--------------------|
| EXPAND | `[codex+agy+claude]` ... | `[codex+claude]` ... | `[agy-verified]` ... |
| PROPOSE | ... | ... | ... |
| EVALUATE | ... | ... | ... |
| SUBTRACT | ... | ... | ... |

Below the matrix:

- **Diamond reading** — Riff's interpretation of which mode the matrix suggests is highest leverage right now (e.g., "PROPOSE column is thin — the theme isn't concrete enough yet; recommend continuing EXPAND")
- **Top breakthrough callout** — the single most interesting `VERIFIED-DIVERGENT` cell, with explicit "this is the angle none of the others reached"
- **Two-track next-step prompt** — "(A) zoom into mode X next round / (B) pick 2 ideas across the matrix to weave into one"

### Engine-Attribution (mandatory on every shipped idea)

- `[codex+agy+claude]` — 3/3 UNIVERSAL
- `[codex+agy]` / `[codex+claude]` / `[agy+claude]` — 2/3 LIKELY
- `[codex-verified]` / `[agy-verified]` / `[claude-verified]` — 1/3 VERIFIED-DIVERGENT (grounded)

---

## Integration with Dialogue Continuation

`multi` is **one turn** inside a larger Riff dialogue. The next turn behavior:

| User reaction to multi output | Riff's next turn |
|-------------------------------|-------------------|
| Picks 1 idea | Drop multi mode; return to normal Riff dialogue with the picked idea as the new active theme; continue with the appropriate mode |
| Picks 2-3 ideas | Use `propose` mode in normal Riff to weave them into a composite; OR offer SCAMPER `combine` lens |
| Picks all / can't pick | Riff diagnoses paralysis — switch to `evaluate` mode in normal dialogue, surface the decisive axis |
| Rejects all | Surface the rejection ledger reasons; offer either (a) re-run multi with `--all-modes` for broader coverage, or (b) reframe the theme first via `flux`-style perspective shift |
| "Run another round" | Re-invoke `multi` with a different active mode; previous round's ideas become anti-duplicate filter for next round |

The Riff main context **tracks dialogue state across rounds**, so the duplicate-of-prior-turn check at GROUND step has data to work with.

---

## Degraded Modes

Identical to `_common/MULTI_ENGINE_RECIPE.md §Degraded Modes`. Riff-specific addition:

| Situation | Behavior |
|-----------|----------|
| User in middle of dialogue invokes `multi` mid-flow | Treat as legitimate; the round becomes a fan-out interlude; previous dialogue state is preserved as the SCOPE input |
| `multi --all-modes` exceeds 36 ideas | Cap each engine at 8 ideas; trim from `UNIVERSAL` first (least breakthrough value), preserve VERIFIED-DIVERGENT |
| Subagent returns ideas in wrong mode | Re-tag if obvious (e.g., a `propose` idea returned under `expand`); drop if confused across multiple modes |

---

## Subagent Prompt Skeleton

Use the Agent tool **three times in the same message** for parallel execution. Each subagent prompt:

```
You are the {engine} riff subagent for Riff (brainstorming partner).

# Role
Generate brainstorming ideas for the active mode(s) below. You are one of three engines working independently — do not try to be exhaustive; surface what your training data suggests is the most non-obvious angle. Riff's whole purpose is to find ideas the user could not easily reach alone.

# Target
- Theme: {user's stated theme}
- Prior dialogue context: {short summary of what was already explored, to avoid duplication}
- Active mode(s): {expand | propose | evaluate | subtract | ALL}
- Target idea count: {3-4 if single mode, 2-3 per mode if all-modes}
- Persona pool (if relevant): {personas from Cast registry or "open"}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema with id / mode / idea_text / rationale / connection_to_theme fields}

# Constraints
- EXPAND ideas must name an ANGLE OR ASSUMPTION TO CHALLENGE, not a solution
- PROPOSE ideas must be ONE concrete sentence, not a paragraph
- EVALUATE ideas must name a TRADE-OFF AXIS, not pick a winner
- SUBTRACT ideas must name SPECIFICALLY what to drop and what survives
- Each idea must connect back to the stated theme (state how in connection_to_theme)
- Do not paraphrase or invent capabilities, personas, or competitors the user did not mention; if you cite reuse of something existing, name it specifically
- Honest friction is the whole point — do not produce polite cheerleading; if you see a fatal flaw in the user's theme framing, surface it as a high-priority EXPAND idea
- Open with the deliverable (no completion preamble)
```

Loose-prompt rule applies — do NOT pass the SCAMPER lens taxonomy, Crazy-8 axis catalog, Steelman protocol, or any other Riff Recipe templates. Those apply at SYNTHESIZE in the main context only.

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — base protocol (read first)
- `_common/SUBAGENT.md §MULTI_ENGINE` — engine dispatch mechanics
- `spark/reference/tri-engine-proposal.md` — canonical Pattern D implementation (mirror this structure)
- `plea/reference/tri-engine-demand.md` — Pattern D with calibration (Riff does NOT calibrate but the dialogue-integration pattern is similar)
- `riff/reference/patterns.md` — mode definitions and transition signals (referenced when interpreting which mode `multi` should default to)
- `riff/reference/examples.md` — Riff dialogue tone; multi output cards inherit this voice
