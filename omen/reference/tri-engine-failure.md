# Multi-Engine Failure Mode Enumeration

> **Filename retained** as `tri-engine-failure.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex) and tri-engine optional (Claude + Codex + agy) modes.

Default flow for `/omen multi`. Run subagents in parallel — one per AVAILABLE engine — to enumerate failure modes (pre-mortem), integrate results across two axes (concurrence + divergence), score each failure mode with composite `engine_concurrence × RPN`, and deliver an integrated FMEA + Risk Matrix preserving single-engine breakthrough catastrophic modes.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) when AVAILABLE at PREFLIGHT. dual-engine mode is NOT degraded. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Pattern type: D (Divergence-Primary).** Different training-data biases directly map to **different failure-mode blind spots** — Codex (GitHub/OSS bug corpora), Claude (Anthropic safety/alignment failure modes) form the dual-engine baseline; Antigravity (Google production-incident shapes) adds the third axis when AVAILABLE. Each engine surfaces failure modes the others structurally miss. A divergent failure mode (1/2 dual / 1/3 tri) is often **the most catastrophic** — precisely because the other engines were blind to it.

**Adapted from `spark/reference/tri-engine-proposal.md` (canonical Pattern D). Re-uses PREFLIGHT, FAN-OUT, NORMALIZE, and CLUSTER stages.** Universal mechanics (engine probe, loose-prompt rule, attribution tags, degraded modes) live in `_common/MULTI_ENGINE_RECIPE.md` — read that first; this document is **the Omen-specific delta only**.

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE (concurrence × RPN) → GROUND → SYNTHESIZE (Risk Matrix) → PRESENT
```

Universal phase semantics: `_common/MULTI_ENGINE_RECIPE.md §Canonical Flow`. Sections below describe only what Omen does differently.

---

## 1. SCOPE — Omen specifics

Define the pre-mortem target once. All three subagents share the same scope:

- Target system / plan / feature under analysis (read actual specs, design docs, code at FRAME — failure enumeration depends on grounding in real system state)
- Analysis boundary (component / pipeline / release / org process)
- Stakeholder set and time horizon (24h / 30d / quarter)
- Work mode (`DEEP` / `RAPID` / `LENS-{domain}`)
- Upstream context if any (Accord spec, Spark RFC, Helm plan, Scribe design doc)
- Existing controls inventory — Omen must score **actual** current controls (S/O/D baseline must reflect reality, not aspiration)

---

## 2. PREFLIGHT

Identical to the canonical probe in `_common/MULTI_ENGINE_RECIPE.md §PREFLIGHT`. No Omen-specific deviation.

---

## 3. FAN-OUT — Omen specifics

Spawn three Agent calls in one message:

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `failure-codex` | Codex CLI | `codex exec --full-auto "<prompt>"` |
| `failure-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) |
| `failure-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule — strict for Omen:** pass only Role + Target + Output format. Do NOT pass the FMEA scoring rubric, the AIAG-VDA AP table, the Swiss-Cheese layer taxonomy, the severity-9 critical gate, or example failure-mode IDs. **Framework rules are applied at SYNTHESIZE in the Omen main context, never at FAN-OUT.** The point is to let each engine's training-data priors drive **independent failure-mode discovery** — bias-overlap defeats the purpose of multi-engine.

### Omen JSON Output Schema

Each subagent returns:

```json
{
  "engine": "codex|agy|claude",
  "failure_modes": [
    {
      "id": "FM-{engine-prefix}-{nn}",
      "category": "infra|data|integration|security|ux|process|business|human-factor|external|other",
      "title": "Short failure-mode name (effect-focused, not solution)",
      "cause_chain": [
        "Upstream cause (trigger)",
        "Intermediate propagation step (if any)",
        "Resulting failure mode in the target system"
      ],
      "effect": "What stakeholder-visible damage results (data loss / SLO breach / regulatory / reputation / safety)",
      "severity": 1,
      "occurrence": 1,
      "detectability": 1,
      "current_controls": "Existing prevention/detection in the system (state 'none' if absent — do not invent)",
      "scenario": "One-paragraph narrative of how this plays out end-to-end",
      "engine_blindspot_note": "Optional: which class of failures this engine knows it tends to over-index on"
    }
  ],
  "engine_notes": "Optional: what training-data bias this engine recognizes it brings (e.g., 'GitHub-heavy → strong on race conditions / dependency bugs, weak on regulatory failures')"
}
```

**Scale anchors for subagents** (pass these literally — they are coordination, not framework):
- `severity` 1–10 (10 = catastrophic, multi-user data loss / safety / regulatory)
- `occurrence` 1–10 (10 = nearly inevitable per release, 1 = once-in-system-lifetime)
- `detectability` 1–10 (10 = will NOT be detected until customer-visible, 1 = automatic detection at build/CI)

Subagents are asked for raw scores; main context **may re-score** during GROUND if subagent calibration is clearly off (e.g., severity=10 assigned to a UI cosmetic).

**Target count per subagent**: 5–8 failure modes in `DEEP`, 3–5 in `RAPID`. Quality over quantity.

---

## 4. NORMALIZE

Parse three JSON blobs into a unified failure-mode list. Tag each mode with `source_engine`. Renumber to global IDs `FM-001`, `FM-002`, … (preserve original engine IDs in `source_id` for traceability). Preserve per-engine cause-chain phrasing — divergent narration may reveal different propagation paths through the same failure surface.

---

## 5. CLUSTER — Omen-specific identity rules

Two failure modes belong to the same cluster when **all four** hold:

1. **Same affected component / subsystem** (or overlapping when a failure spans layers).
2. **Same effect class** (data loss, SLO breach, regulatory violation, safety incident, brand damage, financial leak).
3. **Causally equivalent trigger** — the upstream cause is semantically the same, even if narrated differently (e.g., "DB connection pool exhaustion" and "thread pool starvation under load spike" are the same cluster if both target the same service under the same load profile; they are **different** clusters if one targets DB and the other targets app threads).
4. **Same category** (`infra` / `data` / `integration` / `security` / `ux` / `process` / `business` / `human-factor` / `external`).

**Edge case — partial overlap (intersecting cause chains, divergent effects):** keep as separate clusters but cross-link via `related_clusters`. Example: "missing rate limit on /export" → one cluster terminates in "DB overload" (`infra`), another in "data scraping by malicious actor" (`security`). Different effect classes ⇒ different clusters ⇒ both ship.

Record the set of engines that produced each cluster. Preserve per-engine S/O/D variance — it is a calibration signal.

---

## 6. SCORE — composite `engine_concurrence × RPN` (Omen-specific synthesis)

Omen scores each cluster on **two integrated axes** (Pattern D plus quantitative RPN):

### Concurrence axis (engines independently surfacing the cluster)

| Engines in cluster | Concurrence label | Interpretation |
|--------------------|-------------------|----------------|
| 3 / 3 | `UNIVERSAL` | All engines independently surfaced this failure mode — broadly recognized, high prior probability. Often well-defended in the industry; check current_controls are actually in place. |
| 2 / 3 | `LIKELY` | Two engines concur; one missed. Note **which** engine missed — the gap is often a training-data blindspot signal (e.g., Codex+Antigravity surface infra/perf modes; Claude misses → expected. Claude+Antigravity surface a safety/alignment mode; Codex misses → expected). |
| 1 / 3 | `CANDIDATE → VERIFIED-DIVERGENT` | Single engine surfaced this. Either a unique training-data insight OR a low-quality guess. Must pass GROUND. **Often the most catastrophic mode in the catalog** — precisely because two engines were structurally blind. |

### Quantitative axis — RPN aggregation

For each cluster, compute:
- `RPN_per_engine[i] = severity[i] × occurrence[i] × detectability[i]` (using each contributing engine's raw scores)
- `RPN_max = max(RPN_per_engine)` — primary ranking signal (worst-case across engines)
- `RPN_median = median(RPN_per_engine)` — calibrated ranking signal
- `RPN_variance = max - min` — calibration disagreement signal (variance > 100 means engines disagree on severity / occurrence; flag for main-context re-scoring)
- `AP` (Action Priority H/M/L per AIAG-VDA) — computed in main context from median scores using `reference/scoring-methodology.md`

### Composite priority score

```
composite_priority = concurrence_weight × RPN_signal

concurrence_weight:
  UNIVERSAL (3/3)              → 1.0    (well-supported but possibly well-known)
  LIKELY (2/3)                 → 1.1    (modest amplification for cross-engine support)
  VERIFIED-DIVERGENT (1/3)     → 1.3    (amplification — divergent modes are often most catastrophic)

RPN_signal:
  base = RPN_max
  if any severity ≥ 9 anywhere in cluster → composite_priority = max(composite_priority, RPN_max × 1.5)
                                            (severity-9 critical gate dominates)
```

**Critical override (Omen-specific, non-negotiable):** Any cluster with `severity ≥ 9` from **any** contributing engine is flagged `CRITICAL` regardless of composite_priority, concurrence, or detectability. Catastrophic severity cannot be offset by low occurrence or high detectability. This mirrors the existing Omen `Core Contract` rule and is preserved in multi mode.

---

## 7. GROUND — Omen main context, never delegated

For every cluster, the Omen main context must:

1. **Hallucination check** — does the cited component / file / dependency / external service actually exist in the target system? AI engines may invent module names. If hallucinated, mark `REJECTED-HALLUCINATION`.
2. **Current-controls verification** — does the claimed `current_controls` actually exist? If a subagent asserts "rate limiter at gateway" and there is no rate limiter, the RPN is too low. Re-score `detectability` and `occurrence` upward.
3. **Duplicate-with-existing-mitigation check** — has this failure mode already been mitigated since the system snapshot the engines were reasoning over? If so, mark `ALREADY-MITIGATED` and drop from active modes (but record in ledger).
4. **Scenario plausibility check** — does the cause chain require physically impossible steps or contradict documented system invariants? If implausible, mark `REJECTED-IMPLAUSIBLE`.
5. **Calibration re-score** — if `RPN_variance > 100` (engines disagree by >100 RPN points), re-derive S/O/D from `reference/scoring-methodology.md` calibrated scales and overwrite the cluster's canonical RPN. Preserve per-engine raw scores in an appendix.

Mark each cluster as `VERIFIED-UNIVERSAL` / `VERIFIED-LIKELY` / `VERIFIED-DIVERGENT` / `REJECTED-{reason}` / `ALREADY-MITIGATED` / `NEEDS-INFO`.

**Critical rule for Pattern D:** A `VERIFIED-DIVERGENT` cluster is NOT auto-low-value. Divergent catastrophic modes (e.g., a single engine surfaces a regulatory failure mode the other two structurally miss) often dominate the Risk Matrix.

---

## 8. SYNTHESIZE — Risk Matrix integration (Omen-specific)

### 8.1 Risk Matrix plot

Plot all surviving clusters on a 2D matrix:

- **X-axis** — `occurrence` (1–10, median)
- **Y-axis** — `severity` (1–10, max — severity dominates, never averaged downward)
- **Z-axis (tag)** — concurrence label (`UNIVERSAL` / `LIKELY` / `VERIFIED-DIVERGENT`)
- **Cell color** — by composite_priority quartile (Critical / High / Medium / Low)
- **Annotation** — `engine_concurrence` tag (`[codex+agy+claude]` etc.)

```
Severity ↑
  10 │ ◆D ◆U │ ●U ●U │ ▲L     │ CRITICAL (sev≥9 — auto-flagged regardless of occurrence)
   9 │       │       │        │
   8 │       │ ◆D    │ ●U     │ HIGH (RPN > 200 or AP=H)
   7 │       │       │ ▲L     │
   6 │       │       │        │ MEDIUM (RPN 100-200)
   5 │       │       │        │
   …
     └───────┴───────┴────────┘
              Occurrence →

Legend:
  ●U  UNIVERSAL (3/3)             — well-recognized; verify defenses in place
  ▲L  LIKELY (2/3)                — strong with one dissenter
  ◆D  VERIFIED-DIVERGENT (1/3)    — single-engine breakthrough; often most catastrophic
```

### 8.2 Composite-priority Top-N list

Rank surviving clusters by `composite_priority`. The **Top-N Critical Failures** section in the output (existing Omen requirement) is now ranked by composite_priority — concurrence boosts and severity-9 multipliers are applied. Include a **Divergent Spotlight** sub-list — VERIFIED-DIVERGENT modes that survived grounding, with explicit note on which engine surfaced each and what training-data angle likely explains why the other two missed.

### 8.3 Mitigation Plan (three-layer — Detection / Prevention / Recovery)

Unchanged from Omen default workflow. For each Top-N cluster:
- **Detection** — what monitor/alert would catch this. Cite Beacon handoff.
- **Prevention** — guardrail/validation. Cite Builder handoff.
- **Recovery** — runbook/rollback. Cite Triage/Mend handoff.

### 8.4 LLM Fix Prompt blocks

Generated per existing Omen `LLM Fix Prompt Generation` rules (`reference/fix-prompt-generation.md`). One change in multi mode:

- Add `engine_concurrence` and `composite_priority` to the prompt header so the receiving agent (Builder/Beacon/Triage/Mend) sees the multi-engine evidence basis.
- For `VERIFIED-DIVERGENT` modes, append a note: `[divergent-mode] surfaced by {engine} only; counterpart engines structurally blind to this class — consider the mitigation a higher priority than concurrence alone suggests.`

### 8.5 Engine-attribution mandatory

Every shipped cluster carries an `engine_concurrence` tag:

| Engines | Tag | Concurrence label |
|---------|-----|-------------------|
| 3/3 | `[codex+agy+claude]` | UNIVERSAL |
| 2/3 | `[codex+agy]`, `[codex+claude]`, `[agy+claude]` | LIKELY |
| 1/3 grounded | `[codex-verified]` / `[agy-verified]` / `[claude-verified]` | VERIFIED-DIVERGENT |

---

## 9. PRESENT — Output structure

Extends the standard Omen pre-mortem report with multi-engine artifacts:

- **Header** — engines run, engines failed/unavailable, total clusters, concurrence distribution (`UNIVERSAL: N, LIKELY: N, VERIFIED-DIVERGENT: N`), rejected count
- **Failure Mode Catalog** — all surviving clusters with full FMEA fields + `engine_concurrence` tag
- **Risk Matrix** — ASCII grid per §8.1
- **Top-N Critical Failures** — ranked by composite_priority; divergent spotlight sub-section
- **Mitigation Plan** — three-layer per cluster
- **Residual Risk** — post-mitigation projection
- **LLM Fix Prompt blocks** — for every actionable cluster (per existing rules)
- **Rejection ledger (condensed)** — count by category (hallucination / implausible / already-mitigated / persona-out-of-scope) — preserves SNR transparency
- **Recommended Next Steps** — Ripple (blast radius), Magi (mitigation trade-offs), Triage (playbooks), Beacon (monitoring), Radar (test cases), Sentinel (security escalation)

Do not include rejected clusters in the main list. Do not surface engine-raw output.

---

## Parallel Subagent Prompt Skeleton

Use the Agent tool three times in the same message. Subagent prompt:

```
You are the {engine} failure-mode enumeration subagent for Omen.

# Role
Enumerate {N=5-8 in DEEP / 3-5 in RAPID} failure modes for the target below using prospective hindsight — assume the project / system has already failed and reverse-engineer the causes. You are one of three engines working independently — do not try to be exhaustive across all failure classes; surface what your training data suggests is most likely to actually fail. Different engines will cover different categories; that is by design.

# Target
- Target system / plan / feature: {scope, including read paths to specs / design / code}
- Analysis boundary: {component / pipeline / release / org process}
- Stakeholders and time horizon: {who is affected within {24h | 30d | quarter}}
- Work mode: {DEEP | RAPID | LENS-{domain}}
- Upstream context: {Accord spec / Spark RFC / Helm plan / Scribe design doc if any}
- Existing controls inventory: {what defenses currently exist — score against ACTUAL, not aspirational}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{Omen JSON schema from §3 above}

# Constraints
- Use prospective hindsight: "the project HAS ALREADY FAILED — why?" (Klein/Mitchell 1989)
- Each failure mode has an ordered cause_chain — upstream trigger → propagation → resulting failure
- Score severity / occurrence / detectability on 1-10 scales (anchors in this prompt)
- current_controls must reflect ACTUAL existing defenses — do not invent guardrails that are not there; write "none" if absent
- Do not paraphrase or invent components / files / dependencies the target system clearly does not have; if you assert a cause chain touches a specific module, name it specifically
- Categories you should consider but not be limited to: infra, data, integration, security, ux, process, business, human-factor, external
- Do not write implementation code, mitigations, or fix prompts — failure modes only (Omen main context applies framework rules at SYNTHESIZE)
- Open with the deliverable (the JSON), no completion preamble
```

---

## Degraded Modes

Universal table in `_common/MULTI_ENGINE_RECIPE.md §Degraded Modes`. Omen-specific deltas:

- **1 engine missing**: continue with two. Note in the report that one engine's failure-class blindspot may now be uncovered (e.g., "Claude unavailable — safety/alignment failure-mode class may be under-represented; recommend manual audit of that domain"). `VERIFIED-DIVERGENT` from a single remaining engine requires stricter GROUND.
- **2 engines missing**: single-engine output. Mark every failure mode as `CANDIDATE`; ground all before reporting. Flag in report: "Reduced ideation breadth — failure-mode classes structurally biased toward {remaining engine's} training-data shape."
- **All 3 fail**: abort multi mode; fall back to standard `premortem` Recipe.
- **Severity-9 disagreement**: if engines disagree on severity ≥ 9 for the same cluster (one says S=9, another says S=5), default to the higher severity. Critical-gate decisions are one-way doors.

---

## Why Pattern D Works for Failure Mode Enumeration

- **Training-data bias maps directly to failure-class blindspots.** Codex (GitHub OSS) tends to surface race conditions, dependency / supply-chain, integer overflow, regex DoS. Antigravity (Google production) tends to surface capacity / quota / sharding / cross-region replication / SRE failure modes. Claude (Anthropic-curated) tends to surface prompt-injection, model misalignment, refusal-edge-case, data exfiltration via context, safety/regulatory failure modes. A single-engine `DIVERGENT` mode often reflects one engine seeing a class the other two are structurally blind to — and that mode may be the most catastrophic in the catalog.
- **Severity-9 critical gate dominates concurrence.** Catastrophic outcomes do not need consensus. One engine surfacing a regulatory-violation pathway is enough to ship the cluster.
- **Composite priority blends both axes without collapsing either.** Concurrence weight modestly amplifies VERIFIED-DIVERGENT (1.3×) and severity-9 dominates (1.5× override), preserving Omen's "worst case wins" principle while honoring multi-engine evidence.
- **Risk Matrix visualization separates likelihood from severity** — required by the existing Omen Output Requirements. Multi mode adds the concurrence dimension as glyph shape, keeping the matrix readable.

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — universal protocol (PREFLIGHT probe, loose-prompt rule, attribution tags, degraded modes, implementation checklist) — read this first
- `_common/SUBAGENT.md §MULTI_ENGINE` — base engine dispatch table
- `spark/reference/tri-engine-proposal.md` — sibling Pattern D implementation; CLUSTER and SYNTHESIZE logic mirrored here
- `judge/reference/tri-engine-review.md` — canonical PREFLIGHT and FAN-OUT mechanics
- `omen/reference/failure-frameworks.md` — FMEA procedures and pre-mortem framing applied at SYNTHESIZE
- `omen/reference/scoring-methodology.md` — RPN scales and AP table used at GROUND calibration re-score
- `omen/reference/output-templates.md` — pre-mortem report template extended at PRESENT
- `omen/reference/fix-prompt-generation.md` — LLM Fix Prompt rules; extended in multi mode with `engine_concurrence` header line
- `_common/OPUS_48_AUTHORING.md` — spawn prompt sizing, thinking-depth nudges at SCORE/GROUND
