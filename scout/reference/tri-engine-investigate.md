# Multi-Engine Parallel Investigation (Scout Delta)

> **Filename retained** as `tri-engine-investigate.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex) and tri-engine optional (Claude + Codex + agy) modes.

Default flow for `/scout multi`. Run subagents in parallel — one per AVAILABLE engine — as independent RCA subagents, integrate hypotheses across both axes (confidence + perspective), and deliver a **Pattern H — Hybrid** investigation report that ships a primary root cause backed by consensus while preserving well-reasoned alternative hypotheses as verification-recommended branches.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. dual-engine mode is NOT degraded — Codex sandbox-execution priors + Claude judgment break the most common hypothesis lock-in cases. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Why multiple engines for RCA (Pattern H, not Pattern C):** A single-engine RCA is structurally prone to hypothesis lock-in — once an engine commits to a causal chain, downstream evidence is filtered through that frame. Independent fan-out across engines with non-overlapping training-data priors (Codex/GitHub-heavy + Claude/Anthropic-curated as dual-engine baseline; Antigravity/Google-product-heavy when AVAILABLE) breaks the lock and surfaces alternative root cause hypotheses that the primary engine never considered. **Concurrence raises confidence on the primary RCA; divergence is not noise — it preserves the alternative hypothesis space for parallel verification.** Scout's downstream (Builder) does not write code from a single committed RCA — it receives a primary-plus-alternative bundle with explicit verification ordering.

**This file specifies Scout-specific deltas only.** Read `_common/MULTI_ENGINE_RECIPE.md` first for shared mechanics:

- `§Pattern H Deep Dive` — confidence axis, perspective axis, GROUND verdicts, per-cluster recording, engine-attribution + perspective tag tables, "DIVERGENT is not a failure" rule
- `§Canonical Flow` — SCOPE → PREFLIGHT → FAN-OUT → NORMALIZE → CLUSTER → SCORE → GROUND → SYNTHESIZE → DELIVER skeleton
- `§PREFLIGHT` — engine availability probe (run in Scout main context only)
- `§FAN-OUT` — Agent tool dispatch, loose-prompt rule, runtime-failure detection (`agy` silent-failure pattern)
- `§Degraded Modes` — baseline fallback table; Scout-specific overrides below
- `§Engine-Attribution Tag Convention` — base tag formats

---

## Scout Deltas (what differs from `_common/MULTI_ENGINE_RECIPE.md`)

### 1. SCOPE — RCA-specific inputs

All three subagents share:

- Symptom and observed behavior (verbatim error message, stack trace, log lines)
- Reproduction status (reproduced / partially reproduced / not reproduced) and minimal repro if available
- Environment context (runtime, version, deployment)
- Prior investigation state if multi mode was triggered by `consensus` auto-promotion (3 hypotheses exhausted) — include the **ruled-out hypotheses with their elimination evidence** so subagents do not re-traverse dead ends
- Affected files / area (optional — subagents read the code themselves; do not pre-commit them)

Do **not** pass RCA frameworks (5 Whys, Fishbone, Fault Tree templates) into subagents — each engine applies its own RCA priors. Frameworks apply at SYNTHESIZE.

### 2. FAN-OUT — Scout subagent names

| Subagent | Engine |
|----------|--------|
| `investigate-codex` | Codex CLI (`codex exec --full-auto`) |
| `investigate-agy` | Antigravity CLI (`agy -p` + silent-failure detection per `_common/MULTI_ENGINE_RECIPE.md §3.5`) |
| `investigate-claude` | Claude Code subagent (Agent tool, `subagent_type: general-purpose`) |

### 3. JSON output schema (Scout-specific)

```json
{
  "engine": "codex|agy|claude",
  "hypotheses": [
    {
      "symptom": "Verbatim observed failure (error string, behavior, metric anomaly)",
      "root_cause_hypothesis": "One-sentence systemic root cause — NOT the surface symptom, NOT 'human error'",
      "causal_chain": [
        "Step 1: trigger condition",
        "Step 2: intermediate state transition",
        "Step 3: failure manifestation"
      ],
      "evidence": [
        {"type": "code|log|trace|metric|history|reproduction", "location": "file:line or log source", "quote": "verbatim evidence"}
      ],
      "reproduction_steps": ["Minimal repro step 1", "Minimal repro step 2"],
      "affected_areas": ["file/module/service path 1", "file/module/service path 2"],
      "severity": "Critical|High|Medium|Low",
      "confidence": 0.0,
      "rca_method": "5-whys|fishbone|fault-tree|causal-graph|pattern-match",
      "ruled_out": ["Hypothesis text 1 — why eliminated", "Hypothesis text 2 — why eliminated"]
    }
  ],
  "engine_notes": "Optional: what bias/strength this engine knows it brings"
}
```

Each engine returns 1-3 hypotheses. Single-hypothesis returns are acceptable when the engine has high conviction; multi-hypothesis returns are preferred for ambiguous symptoms.

### 4. CLUSTER — group by root cause hypothesis identity (NOT by symptom)

**Scout's CLUSTER rule is the most consequential delta from generic Pattern H skills.** Engines investigating the same bug always agree on the symptom — they may diverge dramatically on the root cause. Symptom-based clustering would collapse meaningful divergence.

Two hypotheses belong to the **same cluster** when **all three** hold:

- **Same systemic root cause class** — e.g., "race condition in cache write" and "concurrent write to cache without lock" are the same cluster; "cache invalidation timing" and "cache key collision" are different clusters even though both involve the cache.
- **Same primary affected component** — file, module, service boundary, or external dependency named as the locus of the cause.
- **Same causal-chain shape** — the trigger → state-transition → failure sequence has the same key nodes, even if phrased differently. If one hypothesis says "race condition causes stale read" and another says "missing memory barrier causes stale read", they share the chain shape and cluster.

Two hypotheses belong to **different clusters** when **any** of these hold:

- Different layers of causation (application-code bug vs library bug vs infrastructure bug vs config drift)
- Different mechanisms (logic error vs race condition vs resource exhaustion vs upstream dependency)
- Different ultimate fix locations (different files / different owners)

**Do not** force same-symptom hypotheses into the same cluster — divergent root causes for the same symptom are exactly the value Pattern H preserves.

### 5. GROUND — code reading + reproduction attempt (Scout main context, never delegated)

Grounding for RCA is **stricter than for Spark or Plea** because Scout's output drives downstream code changes. Two grounding actions are mandatory for every cluster that may ship (primary OR alternative).

**5a. Code reading (mandatory for every shipping cluster).** For each cluster, read the cited `affected_areas` files and the `causal_chain` step locations with the Read tool. Answer explicitly:

1. **Does the code path described actually exist?** If the cited symbol is absent, mark `REJECTED-HALLUCINATION`.
2. **Does the causal chain match the actual control/data flow?** If any intermediate step does not exist in code, mark `REJECTED-CHAIN-BROKEN`.
3. **Is there an upstream mitigation already in place?** (Input validation, type guard, framework guarantee, lock, retry layer.) If the cluster's failure mode is already prevented in code, mark `REJECTED-MITIGATED`.
4. **Are the cited evidence quotes accurate?** Verify verbatim log/error strings against actual sources. Hallucinated evidence is `REJECTED-HALLUCINATION`.

**5b. Reproduction attempt (mandatory when reproducible).** For each cluster, attempt reproduction using the cluster's `reproduction_steps` when (a) the original bug is reproducible AND (b) the cluster's repro steps are tractable (no production data dependency). A cluster that survives code-read GROUND but fails reproduction is `LIKELY-VERIFIED` (kept, confidence downgraded one tier — CONFIRMED → LIKELY, LIKELY → CANDIDATE). A cluster that survives both is `VERIFIED`.

See `_common/MULTI_ENGINE_RECIPE.md §Pattern H Deep Dive → GROUND verdicts` for the full verdict-to-disposition mapping.

### 6. SYNTHESIZE — Primary RCA + Alternative Hypotheses with verification ordering

Scout's SYNTHESIZE is **the most distinctive step in the multi-engine flow** because Scout does not write fixes. The output must be a verification-ordered bundle that Builder can act on without re-doing the RCA.

**6a. Select Primary RCA.** Rank surviving clusters by: (1) Confidence label, (2) grounding verdict (`VERIFIED > LIKELY-VERIFIED`), (3) evidence count and specificity (file:line + repro + log > inferred chain), (4) causal chain specificity (named state transition > vague "something happens"). Top-ranked surviving cluster = Primary RCA.

**6b. Select Alternative Hypotheses.** If perspective axis is `DIVERGENT-N`, the remaining N-1 surviving clusters ship as Alternative Hypotheses (same ranking criteria). If `CONVERGENT`, no Alternatives — note explicitly in the report ("Three engines reached the same root cause class").

**6c. Author the verification-ordered handoff.** The synthesized output is a Scout Investigation Report containing:

- **Primary RCA section** — full investigation report shape (see `reference/output-format.md`), tagged with concurrence + perspective tags
- **Alternative Hypotheses section** — one block per surviving alternative, each with: root cause hypothesis, causal chain, evidence, suggested verification step, attribution + perspective tags `[DIVERGENT-N → alt-i]`
- **Verification Ordering block** — explicit instruction for Builder:

  ```
  Verification Order:
  1. Apply Primary RCA fix (see ## LLM Fix Prompt).
  2. If symptom persists after Primary fix, verify Alternative Hypothesis #1 by [specific verification step].
  3. If symptom still persists, verify Alternative Hypothesis #2 by [specific verification step].
  ```

- **Engine status summary** — engines run, unavailability notes, confidence distribution (`CONFIRMED: N, LIKELY: N, CANDIDATE-VERIFIED: N`), perspective verdict (`CONVERGENT` or `DIVERGENT-N`)
- **Rejection ledger** (condensed) — count by category (hallucination / chain-broken / mitigated / needs-info)
- **LLM Fix Prompt** — emitted **only for the Primary RCA** when its grounding verdict is `VERIFIED`. Suppress if Primary is `LIKELY-VERIFIED` (use `INVESTIGATE-FURTHER` verb) or if any alternative cluster has comparable or higher confidence in a different fix location (escalation to user judgment).

### 7. REPORT — Scout Investigation Report extensions

The multi-engine report extends `reference/output-format.md` with:

- Front matter: `engine_concurrence` line + `perspective_verdict` line
- New section after Root Cause Analysis: `## Alternative Hypotheses` (omit if `CONVERGENT`)
- New section before LLM Fix Prompt: `## Verification Order`
- New section before Regression Prevention: `## Engine Status` (engines run, distribution, rejections)

`SCOUT_TO_BUILDER_HANDOFF` carries the verification ordering inline; Builder must process alternatives in the listed order before declaring the bug fixed.

---

## Scout Subagent Prompt Skeleton

Use the Agent tool three times in the same message. Each subagent receives:

```
You are the {engine} investigation subagent for Scout.

# Role
Independently perform root cause analysis for the bug below. You are one of three engines working in parallel — do not aim for exhaustiveness; surface the root cause hypotheses your training data suggests are most plausible. Genuinely different hypotheses across engines are valuable; do not anchor to the most obvious explanation.

# Symptom
{Verbatim error message, stack trace, log lines, behavioral description}

# Reproduction state
{reproduced | partially reproduced | not reproduced}
{Minimal repro steps if available}

# Environment
{Runtime, version, deployment context}

# Ruled-out hypotheses (do not re-traverse)
{List from prior single-engine investigation if multi mode was auto-promoted, with elimination evidence}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema from §3}

# Constraints
- Return 1-3 hypotheses. Single-hypothesis is acceptable for high-conviction cases; multiple are preferred for ambiguous symptoms.
- Each `root_cause_hypothesis` must name a SYSTEMIC cause, not a surface symptom and not "human error".
- Each `causal_chain` must trace trigger → state transition → failure. No hand-waving steps.
- Each `evidence` entry must cite a real source (file:line, log source, trace ID) with a verbatim quote. Do not invent evidence.
- Each hypothesis must include `reproduction_steps` even if speculative — label as "speculative repro" if unverified.
- Confidence is 0.0-1.0 numeric. Calibrate honestly; the integration step downgrades over-confident outputs.
- Do not write fix code — RCA only.
- Open with the deliverable (no completion preamble).
```

For Codex / Antigravity subagents, the subagent's first action is `codex exec --full-auto` / `agy -p` (with silent-failure detection per `_common/MULTI_ENGINE_RECIPE.md §3.5`). For the Claude subagent, use the Agent tool with `subagent_type: general-purpose`.

---

## Scout-Specific Degraded-Mode Overrides

Inherits the base table from `_common/MULTI_ENGINE_RECIPE.md §Degraded Modes`. Scout overrides:

| Situation | Scout behavior |
|-----------|----------------|
| 1 engine binary missing | All clusters cap at `LIKELY` (2/3 ceiling); GROUND must be stricter for surviving CANDIDATEs |
| 2 engines fail | Every hypothesis is `CANDIDATE` and must be `VERIFIED` to ship as Primary; Alternative Hypotheses section omitted (no divergence to preserve from a single engine) |
| All 3 fail | Degrade to default `bug` Recipe |
| Symptom is a known pattern (e.g., null deref with obvious cause) | Optionally skip multi; recommend default Recipe |
| Reproduction requires production data | Multi mode still useful for hypothesis breadth, but GROUND produces many `NEEDS-INFO` verdicts; flag in report |

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — base protocol; **Pattern H Deep Dive** carries the shared confidence/perspective/GROUND-verdict/tagging mechanics this file extends
- `_common/SUBAGENT.md §MULTI_ENGINE` — engine dispatch, loose-prompt rule, fallback rules
- `judge/reference/tri-engine-review.md` — Pattern C canonical implementation (confidence-only axis, dissent dropped)
- `spark/reference/tri-engine-proposal.md` — Pattern D canonical implementation (divergence-primary, dissent preserved as Portfolio)
- `scout/reference/output-format.md` — Scout's canonical Investigation Report shape that multi-engine output extends
- `scout/reference/fix-prompt-generation.md` — LLM Fix Prompt rules; multi mode emits one Fix Prompt for the Primary RCA only
- `_common/INVESTIGATION_ESCALATION.md` — confidence scale aligned across Scout / Lens / Trail / Specter
- `_common/OPUS_48_AUTHORING.md` — spawn prompt sizing (P2), tool-use eagerness during GROUND (P3), thinking depth during SYNTHESIZE (P5)
