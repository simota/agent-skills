# Multi-Engine Recipe Protocol

Cross-skill protocol for the `multi` Recipe — spawning subagents in parallel across engines for tasks where multi-engine perspectives improve quality. Adapted from `judge/reference/tri-engine-review.md` for non-review skills.

**Audience**: Skills implementing a `multi` Recipe (Spark, Plea, Omen, Magi, Compete, Sentinel, Riff, Flux, Field, Vision, Saga, Atlas, Echo, Scout, and future additions).

**Prerequisites**: `_common/SUBAGENT.md §MULTI_ENGINE` (base engine dispatch mechanics), `judge/reference/tri-engine-review.md` (canonical PREFLIGHT/FAN-OUT logic).

---

## Base Engine Policy (2026-05 update)

**Default baseline: Claude + Codex (dual-engine).** agy / Antigravity CLI is an **optional addon** — used when AVAILABLE at PREFLIGHT, gracefully skipped when not. Skills MUST NOT treat agy as a hard prerequisite; recipes MUST function correctly in dual-engine mode.

Rationale: agy v1.0.x has frequent silent runtime failures (RESOURCE_EXHAUSTED quota, OAuth expiry, executor errors, internal subagent timeouts — see §3.5). Building hard dependencies on agy makes recipes brittle. The dual-engine Claude+Codex baseline covers the core diversity need (judgment-oriented engine + sandbox-execution engine with non-overlapping training-data priors); agy contributes a third axis (1M context / multimodal / Deep Think / Search grounding) when reachable but is never load-bearing.

| Engine count at runtime | Mode | Tag convention | Confidence floor |
|-------------------------|------|----------------|------------------|
| Claude + Codex + agy (3) | `tri-engine` | `[codex+agy+claude]` etc. | Standard |
| Claude + Codex (2) | `dual-engine` (default) | `[codex+claude]`, `[codex-verified]`, `[claude-verified]` | Standard — NOT degraded |
| Claude only or Codex only (1) | `single-engine` | `[codex-verified]` / `[claude-verified]` | Degraded — every output requires explicit grounding |

Recipes documented as "tri-engine" historically should be read as "multi-engine with optional third axis". The `tri-engine-{verb}` slug remains as a stable filename convention; rename only when restructuring the skill.

---

## When to Use Multi-Engine

A skill should ship a `multi` Recipe when at least one of these conditions holds:

1. **Training-data divergence value** — different engines (Codex/GitHub-heavy, Antigravity/Google-product-heavy, Claude/Anthropic-curated) have non-overlapping priors that meaningfully change the output (ideation, research design, competitive analysis, failure-mode enumeration).
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

**Examples**: Spark (proposals), Plea (synthetic demand), Omen (failure modes), Compete (competitive coverage), Riff (brainstorming), Flux (reframing), Field (research design), Vision (UX direction), Saga (narratives).

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

Spawn **three Agent calls in a single message** for genuine parallel execution. Each subagent has an independent context (no shared bias).

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `{verb}-codex` | Codex CLI | `codex exec --full-auto -o /tmp/codex-<slug>.md "<prompt>"` (artifact file is the source of truth; **keep the spawn foreground** — detached-TTY silently crashes with no output, #19945 unfixed through 0.137.0 — see `_common/CLI_COMPATIBILITY.md §9.3`) |
| `{verb}-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions --log-file <path>` (use `@<path>` to inject files; **output captured via file-handoff, NOT stdout** — prompt must mandate an absolute-path artifact + sentinel per `_common/CLI_COMPATIBILITY.md §9.2`; request JSON inside the artifact, not via the unreliable `--output-format json` flag; silent-failure detection mandatory — see §Engine Runtime Failure Detection below; **Pre-flight Notification required** before first spawn — see `_common/CLI_COMPATIBILITY.md §9.1`) |
| `{verb}-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

`{verb}` is skill-specific: `propose` (Spark), `demand` (Plea), `failure` (Omen), `deliberate` (Magi), etc.

**Loose prompt rule** (per `_common/SUBAGENT.md` MULTI_ENGINE): pass only Role + Target + Output format. Do NOT pass skill-specific frameworks, taxonomies, or templates — those are applied at SYNTHESIZE. The point is to let each engine's training-data priors drive independent output.

**JSON output schema** is mandatory for deterministic integration. Each skill defines its own schema in its `reference/tri-engine-{verb}.md`, but always includes:

```json
{
  "engine": "codex|agy|claude",
  "outputs": [ /* skill-specific output items */ ],
  "engine_notes": "Optional: what bias/strength this engine knows it brings"
}
```

If an engine returns free-form Markdown, ask its subagent to re-emit as JSON before integrating.

### 3.4.1. agy Pre-flight Notification (mandatory)

Before the first `{verb}-agy` subagent of a session emits the Bash spawn, surface the **Pre-flight Notification** defined in `_common/CLI_COMPATIBILITY.md §9.1`. Reason: combining `agy --dangerously-skip-permissions` with a Claude Code `Bash` spawn produces a two-layer autonomous loop that bypasses approval gates on both sides. The notification recommends running `/update-config` once to allowlist the Bash pattern in `settings.json` `permissions.allow`. The notification is informational (does not gate AUTORUN). Subsequent spawns in the same session may downgrade to a single-line reminder if the allowlist entry is confirmed.

### 3.5. Engine Runtime Failure Detection (mandatory)

Some CLIs report runtime failures (quota exhaustion, auth expiry, executor errors, MCP-config corruption) only to a log file, exiting `0` with empty stdout. A subagent that reads only stdout will misclassify the silent failure as "engine returned no findings", polluting CLUSTER / SCORE and producing fake divergence. Each engine has an explicit runtime-failure-detection rule.

| Engine | Failure mode | Detection contract (subagent MUST follow) |
|--------|--------------|--------------------------------------------|
| `agy` v1.0.5 | `exit 0` + empty stdout on any of: **non-TTY stdout-flush bug — a SUCCESSFUL run also emits nothing to piped stdout** (official issue #115, OPEN; unfixed through 1.0.5) / `RESOURCE_EXHAUSTED` 429 / OAuth revoked / `agent executor error` / corrupt `~/.gemini/config/mcp_config.json` / **internal subagent 60s timeout when bare file paths are used instead of `@<path>` syntax** (v1.0.2 changelog: timeout cap restricted to subagents only — main agent escapes it, but delegated file reads still die silently) / **`--print-timeout` (default 5min) exceeded on heavy multi-file synthesis** | **stdout is not the deliverable channel** — apply `_common/CLI_COMPATIBILITY.md §9.2`: prompt-mandated absolute-path artifact + sentinel, verify file exists / non-empty / sentinel present; fallback to transcript harvest (`brain/<conv-id>/.../transcript.jsonl` last `PLANNER_RESPONSE`); ONLY if both artifact and transcript are empty, `grep -E "RESOURCE_EXHAUSTED\|Resets in\|error getting token\|agent executor error\|unexpected end of JSON\|subagent.*timeout\|interaction timeout"` against `--log-file` and report `RUNTIME-BROKEN` with the matched excerpt; retry with `--print-timeout 15m` if heavy synthesis is suspected. Pass file refs as `@<path>` |
| `codex` 0.137.0 | non-zero exit code on most failures; **EXCEPTION: detached-TTY + non-trivial prompt silently crashes with no output** (#19945, regression 0.124.0+, unfixed) — triggered by `setsid` / background-Bash spawns; also `--json`/`--output-schema` silently ignored when MCP tools are active (#15451) | Keep the spawn **foreground**; pass `-o <abs path>` and treat a missing/empty artifact as `RUNTIME-BROKEN` even on `RC == 0`; validate `--output-schema` artifacts parse before aggregating; capture stderr. See `_common/CLI_COMPATIBILITY.md §9.3` |
| Claude subagent | structured Agent-tool errors | Surface verbatim |

**Canonical agy headless pattern** (`_common/SUBAGENT.md` Dispatch Examples carries the same snippet — keep them in sync; full rationale + prompt block: `_common/CLI_COMPATIBILITY.md §9.2`):

```bash
# Prompt MUST end with the §9.2 MANDATORY OUTPUT PROTOCOL block:
#   write deliverable to /tmp/agy-<slug>.md (absolute path) + final-line sentinel <<<END_OF_OUTPUT>>>
SLUG="<task-slug>"
OUT="/tmp/agy-${SLUG}.md"; LOG="/tmp/agy-${SLUG}.log"
rm -f "$OUT"
# agy REQUIRES a TTY: from a socket-stdin shell `agy -p` hangs silently and `script -q /dev/null`
# fails ("Operation not supported on socket"). Give it a real pty via python pty.spawn (§9.2).
# stdout is NOT the deliverable channel either — issue #115 (unfixed v1.0.6).
python3 - "$LOG" <<'PY' || true
import pty, sys
pty.spawn(["agy","-p",open("/tmp/prompt.md").read(),"--dangerously-skip-permissions",
           "--log-file",sys.argv[1],"--print-timeout","15m"])
PY
if [ -s "$OUT" ] && grep -q '<<<END_OF_OUTPUT>>>' "$OUT"; then
  echo "OK: deliverable at $OUT"
else
  # Fallback: transcript harvest (undocumented internal path — bitrot risk)
  TR="$(ls -td "$HOME/.gemini/antigravity-cli/brain"/*/ 2>/dev/null | head -1).system_generated/logs/transcript.jsonl"
  [ -f "$TR" ] && grep '"type":"PLANNER_RESPONSE"' "$TR" | grep '"status":"DONE"' | tail -1 > "${OUT}.transcript.json"
  if [ ! -s "$OUT" ] && [ ! -s "${OUT}.transcript.json" ]; then
    grep -E "RESOURCE_EXHAUSTED|Resets in|error getting token|agent executor error|unexpected end of JSON|subagent.*timeout|interaction timeout" "$LOG" | head -5
    echo "VERDICT: agy RUNTIME-BROKEN"
    exit 42   # caller treats non-0 as RUNTIME-BROKEN; do not silently aggregate
  fi
fi
```

**Integration rules** (main context):

- A `RUNTIME-BROKEN` engine is recorded in the rejection ledger (`engine: RUNTIME-BROKEN (reason: <quota|auth|mcp_corrupt|executor>)`) and excluded from CLUSTER / SCORE.
- Never emit concurrence tags including a `RUNTIME-BROKEN` engine. `[codex+agy+claude]` requires all three engines to have produced real output.
- If `agy` is `RUNTIME-BROKEN` on quota (`RESOURCE_EXHAUSTED`), the reset window is in the log (`Resets in NhNm`). Surface it in the rejection ledger so the user knows when to retry.
- If 2+ engines are `RUNTIME-BROKEN`, fall through to the Degraded Modes table below.

This contract is shared by every `multi` Recipe; do not re-derive it per skill.

### 4. NORMALIZE

Parse the three JSON blobs into a unified output list. Tag each output with its source engine. Preserve per-engine wording — divergent phrasing may carry signal.

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

**For Pattern D (Divergence)**: GROUND `VERIFIED-DIVERGENT` candidates against the artifact base — does the cited evidence/persona/system actually exist? CALIBRATE against real data when available (e.g., Plea against Voice/Trace).

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

Use the Agent tool three times in the same message. Each subagent prompt follows this structure:

```
You are the {engine} {verb} subagent for {Skill}.

# Role
{One-line task persona}. You are one of three engines working independently — do not try to be exhaustive; surface what your training data suggests is most promising.

# Target
{Task-specific context: scope, persona, system, plan, etc.}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{skill-specific JSON schema}

# Constraints
- {Skill-specific quality constraints}
- Do not paraphrase or invent entities the system clearly does not have; if you assert reuse of existing data/logic, name it specifically
- Open with the deliverable (no completion preamble)
```

Engine-specific invocation:

```bash
# Codex (subagent runs this) — foreground only (#19945); artifact file is the source of truth
codex exec --full-auto -o "/tmp/codex-<slug>.md" "$(cat /tmp/prompt.md)"
[ -s "/tmp/codex-<slug>.md" ] || echo "VERDICT: codex RUNTIME-BROKEN (empty artifact despite RC=$?)"

# Antigravity (subagent runs this) — agy needs a real pty (use python pty.spawn, NOT
# `script -q /dev/null` which fails on socket stdin) + file-handoff capture MANDATORY (stdout
# never flushes to non-TTY: issue #115, unfixed v1.0.6). Prompt must end with the §9.2 OUTPUT
# PROTOCOL block: write JSON deliverable to $OUT (absolute path) + final-line sentinel <<<END_OF_OUTPUT>>>.
SLUG="<task-slug>"
OUT="/tmp/agy-${SLUG}.json"; LOG="/tmp/agy-${SLUG}.log"
rm -f "$OUT"
python3 - "$LOG" <<'PY' || true
import pty, sys
pty.spawn(["agy","-p",open("/tmp/prompt.md").read(),"--dangerously-skip-permissions",
           "--log-file",sys.argv[1],"--print-timeout","15m"])
PY
if ! { [ -s "$OUT" ] && grep -q '<<<END_OF_OUTPUT>>>' "$OUT"; }; then
  grep -E "RESOURCE_EXHAUSTED|Resets in|error getting token|agent executor error|unexpected end of JSON" "$LOG" | head -5
  echo "VERDICT: agy RUNTIME-BROKEN — see §Engine Runtime Failure Detection (try transcript fallback per CLI_COMPATIBILITY §9.2 first)"
fi
```

For the Claude subagent, use the Agent tool with `subagent_type: general-purpose` and the prompt above.

**Invocation invariants** (all engines): subscription auth only (no provider API keys), default model (no `-m` / `--model` / `-c model=...`), structured JSON output required.

---

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

For Pattern D skills with calibration (Plea): append a second tag `[validated]` / `[supported]` / `[hypothesis]` / `[synthetic-only]` per the skill's calibration rules.

For Pattern H skills (Magi/Atlas/Scout/Echo): append a perspective tag `[CONVERGENT]` or `[DIVERGENT-N]` (N = number of dissenting positions).

---

## CAPABILITIES_SUMMARY Conventions

Skills implementing a `multi` Recipe should add a capability line to their CAPABILITIES_SUMMARY block:

```
tri_engine_{verb}: `multi` Recipe — {one-line description of what fan-out produces}; {pattern type — Concurrence-primary / Divergence-primary / Hybrid}; {merge strategy default}; {key skill-specific feature, e.g., calibration tags, viewpoint matrix, persona axis}
```

Examples (already shipped):
- Spark: `tri_engine_proposal: ... Compete-merge or Portfolio-merge ... preserves divergent breakthrough proposals`
- Plea: `tri_engine_demand: ... cross-persona-universal signals AND single-engine divergent-voice insights ... calibration tags`

---

## Implementation Checklist

When adding `multi` Recipe to a new skill:

- [ ] Decide pattern type (D / C / H)
- [ ] Add `tri_engine_{verb}` line to CAPABILITIES_SUMMARY
- [ ] Add `Multi-Engine` row to the Recipes table with `multi` subcommand
- [ ] Add `multi` behavior note in Subcommand Dispatch
- [ ] Add `Multi-Engine Mode` section to SKILL.md (use Spark or Plea as template)
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
- `plea/reference/tri-engine-demand.md` — canonical Pattern D with calibration + cross-axis (persona × engine)
- `_common/OPUS_48_AUTHORING.md` — spawn prompt sizing, thinking-depth nudges, parallel-fan-out triggers
