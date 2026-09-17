# Multi-Engine Recipe Protocol

> **Tier:** `orchestration` — activates from the hub, a recipe, or on engine detection. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

Cross-skill protocol for the `multi` Recipe — spawning subagents in parallel across engines for tasks where multi-engine perspectives improve quality. Adapted from `judge/reference/tri-engine-review.md` for non-review skills.

**Audience**: Skills implementing a `multi` Recipe (Spark, Echo[demand], Omen, Magi, Compete, Sentinel, Flux, Field, Vision, Saga, Atlas, Echo, Scout, and future additions).

**Prerequisites**: `_common/SUBAGENT.md §MULTI_ENGINE` (base engine dispatch mechanics), `judge/reference/tri-engine-review.md` (canonical PREFLIGHT/FAN-OUT logic).

---

## Base Engine Policy (2026-05 update)

**Default baseline: Claude + Codex (dual-engine).** agy / Antigravity CLI is an **optional addon** — used when AVAILABLE at PREFLIGHT, gracefully skipped when not. Skills MUST NOT treat agy as a hard prerequisite; recipes MUST function correctly in dual-engine mode.

This is a repository deployment baseline, not a claim that vendors have disjoint training data or fixed domain strengths. An available authorized third engine may add independent evidence; measure its contribution. Runtime failures and partial outputs are handled by §3.5 for every engine. Model and capability selection follows `_common/CLI_COMPATIBILITY.md`.

| Engine count at runtime | Mode | Tag convention | Confidence floor |
|-------------------------|------|----------------|------------------|
| Claude + Codex + agy (3) | `tri-engine` | `[codex+agy+claude]` etc. | Standard |
| Claude + Codex (2) | `dual-engine` (default) | `[codex+claude]`, `[codex-verified]`, `[claude-verified]` | Standard — NOT degraded |
| Claude only or Codex only (1) | `single-engine` | `[codex-verified]` / `[claude-verified]` | Degraded — every output requires explicit grounding |

Recipes documented as "tri-engine" historically should be read as "multi-engine with optional third axis". The `tri-engine-{verb}` slug remains as a stable filename convention; rename only when restructuring the skill.

---

## When to Use Multi-Engine

A skill should ship a `multi` Recipe when at least one of these conditions holds:

1. **Independent perspective value** — different authorized engines may produce useful alternative hypotheses; evaluate their grounded contribution rather than asserting knowledge of their training data.
2. **Self-bias risk** — the skill's output is evaluative and a single engine would inherit blind spots (security scanning, code review, persona channeling).
3. **Decision stakes warrant cross-validation** — strategic judgment, architectural choices, security findings, post-mortems where a single-engine answer is too narrow.

Do NOT add `multi` when:

- The task is deterministic (format conversion, code generation following a spec, math)
- Output quality is purely aesthetic (image gen, color tokens) — engine "agreement" is meaningless
- Single source of truth exists (test execution, build runs) — multi-engine doesn't add signal
- Spawn cost exceeds value (sub-30s tasks, one-line lookups)

---

## Three Pattern Types

Each skill's `multi` Recipe falls into one of three patterns. Choose the one that matches your skill's quality model.

### Pattern D — Divergence-Primary

**Use when**: Output value comes from *breadth of ideas / perspectives*. Disagreement is informative; single-engine insights are often the breakthrough.

**Examples**: Spark (proposals), Echo[demand] (synthetic demand), Omen (failure modes), Compete (competitive coverage), Flux (brainstorming), Flux (reframing), Field (research design), Vision (UX direction), Saga (narratives).

**Scoring**:
- `UNIVERSAL` (3/3) = broadly recognized; safe but possibly obvious
- `LIKELY` (2/3) = strong with one dissenter
- `VERIFIED-DIVERGENT` (1/3 after grounding) = single-engine breakthrough; NOT auto-low-value

**Synthesis**: Preserve divergence. Default to Portfolio merge (multiple complementary outputs); offer Compete merge (single best, re-mixing wording) only on explicit request.

**Filter**: Drop only hallucinated, duplicate, or vague outputs. Divergent outputs that pass grounding ship.

---

### Pattern C — Concurrence-Primary

**Use when**: Output value comes from *agreement reduces false positives*. Disagreement is noise; consensus is the quality signal.

**Examples**: Judge (code review), Sentinel (SAST), Probe (dynamic security), Attest (spec compliance).

**Scoring**:
- `CONFIRMED` (3/3) = high-confidence finding; ship
- `LIKELY` (2/3) = ship with concurrence tag
- `CANDIDATE` (1/3) = MUST pass grounding to ship; drop if rejected

**Synthesis**: Filter aggressively. Single-engine findings ship only after explicit grounding/verification by main context.

**Filter**: Drop style-only, already-mitigated, hallucinated, low-severity findings. Goal: every shipped finding is actionable.

---

### Pattern H — Hybrid (Both Axes Matter)

**Use when**: The skill produces *judgment* — both creative options AND confidence calibration matter. Concurrence raises confidence; divergence reveals trade-offs.

**Examples**: Magi (strategic deliberation), Atlas (architecture/ADR), Scout (RCA), Echo (UX walkthrough).

**Scoring** (use both axes):
- Confidence axis: `CONFIRMED` / `LIKELY` / `CANDIDATE` (per Pattern C)
- Perspective axis: `CONVERGENT` (all engines reach same conclusion) / `DIVERGENT-N` (N ≥ 2 engines split on conclusion — surface the split as a feature, not a bug)

**Synthesis**: Present both the consensus position AND the dissenting perspectives. For Magi-style 3-viewpoint skills, this becomes **3 engines × N viewpoints = N×3 matrix** — extract patterns from the matrix rather than averaging.

**Filter**: Drop hallucinations and incoherent outputs; preserve well-reasoned dissents.

---

## Pattern H Deep Dive (shared by Scout / Atlas / Magi / Echo)

The Pattern H scoring/grounding/tagging mechanics are identical across skills; only the JSON schema, cluster identity rules, and output document shape differ. Skills implementing Pattern H inherit this section verbatim and define only their deltas in `reference/tri-engine-{verb}.md`.

### Confidence axis (per cluster) — initial treatment

| Engines in cluster | Confidence label | Initial treatment |
|--------------------|------------------|-------------------|
| 3 / 3 | `CONFIRMED` | High confidence; light spot-check at GROUND |
| 2 / 3 | `LIKELY` | Strong; note what the missing engine surfaced instead — that often becomes a dissenting cluster |
| 1 / 3 | `CANDIDATE` | Must pass GROUND to ship as primary or dissenting; drop if rejected |

### Perspective axis (cross-cluster)

After confidence scoring, examine the cluster set as a whole:

- `CONVERGENT` — all surviving clusters reduce to the same conclusion class. Ship a single high-confidence output.
- `DIVERGENT-N` — N ≥ 2 surviving clusters reflect genuinely different conclusions. The top-ranked cluster ships as the recommended/primary; remaining N-1 ship as Dissenting/Alternative entries with explicit downstream handoff (verification ordering, supersession triggers, etc.).

**Critical Pattern H rule**: A `DIVERGENT` result is **not a failure of the multi-engine flow** — it is the precise signal multi-engine investigation is designed to produce. Single-engine output cannot tell you when alternative conclusions are plausible; multi-engine can. Ship the divergence explicitly rather than collapsing.

### GROUND verdicts (shared label set)

All Pattern H skills use the same verdict vocabulary. Per-skill grounding checks (code reads, repro attempts, feasibility scans, anti-pattern scans) bind to these verdicts.

| Verdict | Meaning | Disposition |
|---------|---------|-------------|
| `VERIFIED` | All grounding checks pass | Ship as primary or dissenting per perspective axis |
| `LIKELY-VERIFIED` | Primary checks pass; secondary checks inconclusive (e.g., repro inconclusive, severity ambiguous) | Ship as dissenting only — never as the sole primary unless no `VERIFIED` cluster exists; downgrade confidence one tier |
| `REJECTED-HALLUCINATION` | Cited code/evidence/module does not exist | Drop; record in rejection ledger |
| `REJECTED-CHAIN-BROKEN` | Causal/intervention chain has a missing step | Drop; record in rejection ledger |
| `REJECTED-MITIGATED` | Already prevented / addressed upstream | Drop; record in rejection ledger |
| `REJECTED-INFEASIBLE` | Violates a hard constraint (runtime, topology, anti-pattern) | Drop; record in rejection ledger |
| `NEEDS-INFO` | Cannot verify without information main context does not have | Escalate to user; do not ship |

**Never ship a sole primary without at least one `VERIFIED` cluster.** If all surviving clusters are `LIKELY-VERIFIED`, ship the highest-confidence as primary with an explicit confidence downgrade and call out the verification gap.

### Per-cluster recording (mandatory)

For every cluster surviving CLUSTER+SCORE, record:

- Engine set that produced it (drives the attribution tag)
- Union of evidence across engines (drives ground-truth audits)
- Union of causal-chain / intervention-step nodes (skills that have chains)
- Highest confidence assigned across engines (entry confidence before GROUND)
- Grounding verdict (set at GROUND)
- Cross-references to other clusters it depends on or supersedes (smell ↔ option in Atlas; primary ↔ alternative ordering in Scout)

### Engine-attribution + perspective tags

Every shipped cluster carries both a concurrence tag and a perspective tag.

| Engines flagging cluster | Concurrence tag | Perspective tag |
|--------------------------|-----------------|-----------------|
| 3 / 3 | `[codex+agy+claude]` | `[CONVERGENT]` (if also the only surviving cluster) or `[DIVERGENT-N → primary/alt-i]` |
| 2 / 3 | `[codex+agy]` (any 2-combo) | `[CONVERGENT]` or `[DIVERGENT-N → primary/alt-i]` |
| 1 / 3 grounded | `[codex-verified]` / `[agy-verified]` / `[claude-verified]` | `[DIVERGENT-N → alt-i]` (almost always alternative/dissenting) |
| 1 / 3 rejected | (not shipped) | (not shipped) |

Atlas variant: append the architectural style to the perspective tag for divergent options (`[DIVERGENT-{style}]`).
Scout variant: append the alternative slot id for verification ordering (`[DIVERGENT-N → alt-i]`).

### Why Pattern H is not Pattern C with extra steps

- **Hypothesis / option lock-in is the dominant single-engine failure mode** for judgment-bearing skills. Once an engine commits to a frame, downstream reasoning is filtered through that frame. Independent fan-out across engines with non-overlapping training-data priors breaks the lock structurally.
- **Concurrence is rare for non-trivial judgment tasks.** When three engines independently converge, the conclusion is almost certainly correct. When they diverge, the divergence itself is diagnostic — single-engine confidence in that case would be falsely high.
- **Pattern C drops dissent; Pattern H ships dissent as a feature.** This matches the actual epistemic state of judgment tasks — multiple plausible answers for the same problem is the common case, not the edge case.

---

## Canonical Flow (all patterns)

```
SCOPE → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE → GROUND/CALIBRATE → SYNTHESIZE → DELIVER
```

The flow is identical across patterns; what differs is the SCORE rubric and the SYNTHESIZE merge strategy.

### 1. SCOPE

Define the task target once. All three subagents share the same scope. Include skill-specific context (persona pool, plan being challenged, system under analysis, etc.) but NOT skill-specific frameworks/templates — those apply at SYNTHESIZE.

### 2. PREFLIGHT — engine availability detection

**Run in skill main context. Never delegate to subagents.** Subagent PATH is narrower than the user's interactive shell, leading to false-negative "unavailable" verdicts.

Canonical probe (per `judge/reference/tri-engine-review.md §2`):

```bash
for cli in codex agy claude; do
  if command -v "$cli" >/dev/null 2>&1; then
    echo "$cli: $(command -v $cli) ($($cli --version 2>&1 | head -1))"
  else
    for p in "$HOME/.bun/bin/$cli" "$HOME/.local/bin/$cli" "/usr/local/bin/$cli" "/opt/homebrew/bin/$cli"; do
      if [ -x "$p" ]; then echo "$cli: $p ($($p --version 2>&1 | head -1))"; break; fi
    done || echo "$cli: NOT FOUND"
  fi
done
```

**Availability verdict — strict criteria** (identical to Judge tri-engine PREFLIGHT):

| Outcome | Treatment |
|---------|-----------|
| Binary found AND `--version` returns | `AVAILABLE` |
| Binary not found in any probed location | `UNAVAILABLE (binary missing)` |
| Binary found but `--version` exits non-zero | `AVAILABLE-WITH-WARNING` |
| Auth/network/timeout error | `AVAILABLE` — runtime failure, not unavailability |

**Never declare unavailable based on**: transient errors, prior session failures, absence from standard `$PATH` alone (always probe fallback paths).

### 3. FAN-OUT — parallel subagents

Launch the selected available engines in independent contexts using `_common/CLI_COMPATIBILITY.md`. The dual-engine baseline requires two real engines, not three mandatory calls; add the optional third only when available and justified. Use exclusive artifacts and a join before synthesis.

**Loose prompt rule:** pass task, revision-bound inputs, ACs, authority/prohibited effects and the skill's output schema. Do not reveal other engines' conclusions or impose the synthesizer's taxonomy prematurely. Never omit safety constraints for “independence.”

**JSON output schema** remains required for deterministic integration. Preserve the skill-specific schema in `reference/tri-engine-{verb}.md` and record actual engine identity. Re-emit malformed output within the original authority/budget or mark that branch incomplete; a parser repair is not new substantive evidence.

```json
{
  "engine": "codex|agy|claude",
  "outputs": [],
  "engine_notes": "Observed limitations, not invented training-data claims"
}
```

### 3.4.1. agy Pre-flight Notification (mandatory)

Before a material new effect, disclose it and resolve any required approval under `_common/CLI_COMPATIBILITY.md` §9.1. The historical informational notice is **not authorization** for permission bypass; no global allowlist/configuration mutation is part of this recipe. Already-authorized normal headless calls need no repetitive notification.

### 3.5. Engine Runtime Failure Detection (mandatory)

For **every engine**, capture process/tool status, structured result where available, diagnostics, required artifacts and the revision/run they belong to. An empty result is “no findings” only after evidence shows the requested analysis completed. A required tool denial, timeout, malformed schema or missing artifact is incomplete even if the process exits zero.

Current command syntax and version-specific workarounds live in `_common/CLI_COMPATIBILITY.md` §9. Prefer documented structured output. Only a reproduced installed-version defect justifies PTY/file-handoff or foreground-only execution; never suppress the exit code or harvest another run's most recent transcript.

**Integration rules** (main context):

- Record `RUNTIME-BROKEN (reason: ...)` in the rejection ledger and exclude that branch from CLUSTER/SCORE. Sanitize diagnostics before surfacing them.
- Never emit concurrence tags for missing, substituted or failed engines. `[codex+agy+claude]` requires three real, usable engine outputs.
- For rate limits/authentication failures, preserve the observed retry/reset information without inventing a delay or opening credential files. Retry only within authorized bounds; repeated identical failures require diagnosis.
- Multiple failures use the Degraded Modes below. Reduced coverage cannot silently satisfy a missing independent-verification requirement.

This contract is shared by every `multi` Recipe; do not duplicate shell wrappers per skill.

### 4. NORMALIZE

Parse the usable JSON results from the selected engines into a unified output list. Tag each output with its source engine. Preserve per-engine wording — divergent phrasing may carry signal.

### 5. CLUSTER — dedup across engines

Group outputs that describe the same item (defect / opportunity / failure mode / argument). Two outputs match when they share enough identity dimensions per the skill's domain definition.

**Generic identity rules** (refine per skill):
- Same primary subject (file, persona, system component, claim)
- Semantic overlap in the core statement
- Same category/class label

Record the set of engines that produced each cluster.

### 6. SCORE — pattern-specific

Apply the scoring rubric for your pattern type (D / C / H). See per-pattern tables above.

### 7. GROUND or CALIBRATE — skill main context, never delegated

**For Pattern C (Concurrence)**: GROUND `CANDIDATE` findings by reading the actual code/system. Mark `VERIFIED` / `REJECTED` / `NEEDS-INFO`.

**For Pattern D (Divergence)**: GROUND `VERIFIED-DIVERGENT` candidates against the artifact base — does the cited evidence/persona/system actually exist? CALIBRATE against real data when available (e.g., Echo[demand] against Voice/Trace).

**For Pattern H (Hybrid)**: Both. Ground confidence; preserve dissenting perspectives that are well-reasoned even if not converged.

**Always check**:
1. Hallucinated entities (functions, personas, competitors, APIs, file paths)
2. Duplicates already present in the target system
3. Vague or unmeasurable claims
4. Style/aesthetic-only opinions (drop unless task is explicitly about style)

### 8. SYNTHESIZE — pattern-specific

**Pattern D**: Portfolio (default) or Compete merge. Engine-attribution tag mandatory.
**Pattern C**: Filter to actionable findings only. Concurrence tag mandatory.
**Pattern H**: Present consensus + dissent. Both confidence tag AND perspective tag mandatory.

**Universal output requirements**:
- Engine-attribution tag on every shipped output: `[codex+agy+claude]` (3/3), `[codex+agy]` etc. (2/3), `[codex-verified]` (1/3 grounded)
- Engine status summary in header (which engines ran, which failed/unavailable)
- Rejection ledger (condensed): count by category — preserves SNR transparency without re-introducing noise
- Concurrence distribution: e.g., `UNIVERSAL: N, LIKELY: N, VERIFIED-DIVERGENT: N`

### 9. DELIVER

Output structure follows the skill's existing template, with multi-engine additions documented in that skill's `reference/tri-engine-{verb}.md`.

---

## Parallel Subagent Prompt Skeleton

Use `_common/CLI_COMPATIBILITY.md` §3's scoped spawn template and §9's capture contract. Add only the domain JSON schema and constraints from the selected skill reference; launch the actual available engine count, then join before synthesis.

Do not copy shell wrappers here. Historical PTY, foreground-only, default-model and permission-bypass mandates are superseded by the capability, authorization and reproduced-defect gates in that adapter. Preserve independent inputs, authentic engine identity, current-run artifact provenance and every required output field.

## Engine Availability Modes

> Per Base Engine Policy: Claude+Codex is the default baseline (NOT degraded). agy is optional — its absence is a normal mode, not a failure.

| Situation | Mode | Behavior |
|-----------|------|----------|
| Claude + Codex + agy AVAILABLE | `tri-engine` | Run all three; standard confidence rubric; engine-attribution tags include agy |
| Claude + Codex AVAILABLE, agy UNAVAILABLE or RUNTIME-BROKEN | `dual-engine` (default fallback) | Run Claude + Codex; standard confidence rubric (NOT degraded); engine-attribution tags use 2-of-2 vocabulary; record agy absence in the rejection ledger as informational, not as a failure |
| Only 1 engine AVAILABLE (other RUNTIME-BROKEN or missing) | `single-engine` (degraded) | Single-engine output; every output is CANDIDATE; ground all before reporting; flag reduced confidence explicitly |
| 0 engines AVAILABLE | Abort multi mode; degrade to the skill's default non-multi Recipe |
| User explicitly requests single engine | Skip fan-out; use default Recipe |
| Trivial scope | Optionally skip multi; recommend default Recipe |
| Auth/quota error during execution | Apply §3.5 Engine Runtime Failure Detection; mark engine `RUNTIME-BROKEN`, exclude from aggregation, surface the matched log excerpt in the rejection ledger; if agy is the broken engine, fall through to `dual-engine` mode silently (no abort) |

**Dual-engine tag vocabulary** (when running Claude + Codex only):

| Engines flagging | Tag | Meaning |
|------------------|-----|---------|
| 2 / 2 | `[codex+claude]` | Universal / Confirmed (dual-engine) |
| 1 / 2 grounded | `[codex-verified]` / `[claude-verified]` | Single-engine, passed grounding |
| 1 / 2 rejected | (not shipped) | — |

---

## Engine-Attribution Tag Convention

Every output shipped from a `multi` Recipe carries an engine-attribution tag. The tag set depends on the runtime engine count (see Base Engine Policy + Engine Availability Modes).

**Tri-engine mode** (Claude + Codex + agy AVAILABLE):

| Engines flagging | Tag format | Meaning |
|------------------|------------|---------|
| 3 / 3 | `[codex+agy+claude]` | Universal / Confirmed |
| 2 / 3 | `[codex+agy]`, `[codex+claude]`, `[agy+claude]` | Likely (two-of-three) |
| 1 / 3 grounded | `[codex-verified]`, `[agy-verified]`, `[claude-verified]` | Single-engine, passed grounding |
| 1 / 3 rejected | (not shipped) | — |

**Dual-engine mode** (Claude + Codex only — default baseline):

| Engines flagging | Tag format | Meaning |
|------------------|------------|---------|
| 2 / 2 | `[codex+claude]` | Universal / Confirmed (dual-engine baseline) |
| 1 / 2 grounded | `[codex-verified]`, `[claude-verified]` | Single-engine, passed grounding |
| 1 / 2 rejected | (not shipped) | — |

For Pattern D skills with calibration (Echo[demand]): append a second tag `[validated]` / `[supported]` / `[hypothesis]` / `[synthetic-only]` per the skill's calibration rules.

For Pattern H skills (Magi/Atlas/Scout/Echo): append a perspective tag `[CONVERGENT]` or `[DIVERGENT-N]` (N = number of dissenting positions).

---

## CAPABILITIES_SUMMARY Conventions

Skills implementing a `multi` Recipe should add a capability line to their CAPABILITIES_SUMMARY block:

```
tri_engine_{verb}: `multi` Recipe — {one-line description of what fan-out produces}; {pattern type — Concurrence-primary / Divergence-primary / Hybrid}; {merge strategy default}; {key skill-specific feature, e.g., calibration tags, viewpoint matrix, persona axis}
```

Examples (already shipped):
- Spark: `tri_engine_proposal: ... Compete-merge or Portfolio-merge ... preserves divergent breakthrough proposals`
- Echo[demand]: `tri_engine_demand: ... cross-persona-universal signals AND single-engine divergent-voice insights ... calibration tags`

---

## Implementation Checklist

When adding `multi` Recipe to a new skill:

- [ ] Decide pattern type (D / C / H)
- [ ] Add `tri_engine_{verb}` line to CAPABILITIES_SUMMARY
- [ ] Add `Multi-Engine` row to the Recipes table with `multi` subcommand
- [ ] Add `multi` behavior note in Subcommand Dispatch
- [ ] Add `Multi-Engine Mode` section to SKILL.md (use Spark or Echo[demand] as template)
- [ ] Add `multi-engine` row to Output Routing
- [ ] Create `reference/tri-engine-{verb}.md` with skill-specific:
  - JSON output schema
  - CLUSTER identity rules
  - SCORE rubric (per pattern type)
  - GROUND/CALIBRATE checks
  - SYNTHESIZE merge strategy
  - Subagent prompt skeleton
- [ ] Add `reference/tri-engine-{verb}.md` and `_common/SUBAGENT.md` to Reference Map
- [ ] Add `tri_engine:` block to `_STEP_COMPLETE.Output` schema
- [ ] Verify CAPABILITIES_SUMMARY HTML comment block is intact (`<!--` opens, `-->` closes)

---

## Cross-References

- `_common/SUBAGENT.md §MULTI_ENGINE` — base protocol (engine dispatch, loose prompts, fallback rules)
- `judge/reference/tri-engine-review.md` — canonical Pattern C implementation
- `spark/reference/tri-engine-proposal.md` — canonical Pattern D implementation (with Portfolio/Compete merge)
- `echo/reference/tri-engine-demand.md` — canonical Pattern D with calibration + cross-axis (persona × engine)
- `_common/OPUS_5_AUTHORING.md` — spawn prompt sizing, thinking-depth nudges, parallel-fan-out triggers

## Lifecycle

- **failure:** F1: dated model traits and duplicated invocation recipes drifted from current execution interfaces.
- **effect:** Central dispatch guidance replaces repeated model/permission mandates; authentic engine provenance and failure handling remain required.
- **owner:** Judge
- **removal:** Remove local dispatch guidance when every recipe consumes the compatibility adapter and runtime tests cover capture and failure states.
