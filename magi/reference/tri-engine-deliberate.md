# Multi-Engine Deliberation

> **Filename retained** as `tri-engine-deliberate.md` for backward compatibility. The content covers both **dual-engine baseline (6-cell matrix)** and **tri-engine optional (9-cell matrix)** modes.

Default flow for `/magi multi`. Run subagents in parallel — one per AVAILABLE engine — each engine independently deliberates from **all three Magi viewpoints (Logos / Pathos / Sophia)** — then integrate into a deliberation matrix (engines × 3 viewpoints) for two-pass scoring (per-viewpoint concurrence + per-engine consistency) and pattern-based final verdict.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 6-cell matrix)**. agy is added as a third axis (tri-engine, 9-cell matrix) only when AVAILABLE at PREFLIGHT. dual-engine mode is the recipe's normal operating state, NOT a degraded mode. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes`.

**Why multi-engine deliberation (Pattern H — Hybrid):** Magi's value model demands both *consensus signal* (high concurrence within a viewpoint raises confidence) AND *dissent signal* (cross-viewpoint divergence reveals trade-offs in the decision). Single-engine deliberation inherits one model's blind spots across all three viewpoints. Multi-engine deliberation produces a matrix where patterns (e.g., "all Logos approve, all Pathos reject") become the verdict's most valuable artifact — not noise to average away. **Dual-engine baseline (Claude judgment + Codex sandbox-execution priors) covers the load-bearing diversity**; the optional agy axis adds a third independent training-data signature when reachable.

**Adapted from `_common/MULTI_ENGINE_RECIPE.md` (Pattern H). Re-uses SCOPE / PREFLIGHT / FAN-OUT / NORMALIZE / DELIVER stages; replaces single-axis CLUSTER/SCORE with a two-pass concurrence model and replaces SYNTHESIZE with matrix visualization + pattern-based verdict synthesis.**

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT (3 subagents, each emits all 3 viewpoints) → NORMALIZE
       → CLUSTER (two-pass: per-viewpoint + per-engine) → SCORE → GROUND/CALIBRATE
       → SYNTHESIZE (9-cell matrix + pattern verdict) → DELIVER
```

**Critical fan-out design**: spawn 3 subagents (not 9). Each subagent independently produces all 3 viewpoint reasonings (Logos + Pathos + Sophia) in one JSON payload. This keeps spawn cost low while still letting each engine reason across all viewpoints with its own training-data priors. Cross-engine viewpoint divergence becomes the cluster-scoring signal.

---

## 1. SCOPE

Define the deliberation target once. All three subagents share the same scope:

- The decision being deliberated (one clear question, not a bundle)
- Decision domain (Architecture / Trade-off / Go/No-Go / Strategy / Priority)
- Reversibility classification (HIGH / MEDIUM / LOW per FRAME)
- Task type (REASONING / KNOWLEDGE per FRAME — controls evidence sharing rules)
- Constraints, evidence, prior options being arbitrated
- Domain-specific context (architecture: stack/patterns; trade-off: option A vs B; Go/No-Go: metrics + readiness criteria; strategy: build/buy data; priority: candidate list)

## 2. PREFLIGHT — engine availability (Magi main context, never delegated)

Use the canonical probe from `_common/MULTI_ENGINE_RECIPE.md §2 PREFLIGHT`. Magi main context runs the combined probe once; subagent PATH is narrower and will produce false negatives. Pass absolute binary paths to subagents when the standard PATH probe failed.

Availability verdicts and "never declare unavailable based on..." rules: identical to the protocol baseline.

## 3. FAN-OUT — parallel subagents (N spawns where N = engine count, NOT N×3)

Spawn **one Agent call per AVAILABLE engine in a single message**. Each subagent runs one engine and produces all three viewpoint deliberations in one JSON response. **Dual-engine baseline = 2 spawns** (Claude + Codex); **tri-engine = 3 spawns** when agy is also AVAILABLE.

| Subagent | Engine | Spawn Condition | Baseline command |
|----------|--------|-----------------|------------------|
| `deliberate-codex` | Codex CLI | Always (Codex required for magi multi) | `codex exec --full-auto "<prompt>"` |
| `deliberate-claude` | Claude Code CLI (subagent) | Always (host engine) | Agent tool with `subagent_type: general-purpose` |
| `deliberate-agy` | Antigravity CLI | **Only when AVAILABLE at PREFLIGHT** | `agy -p "<prompt>" --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) |

**Loose prompt rule** (per `_common/SUBAGENT.md` MULTI_ENGINE): pass Role + Target + Output format only. Do NOT pass:

- Decision domain templates (decision-domains.md matrices)
- Voting calibration heuristics (voting-mechanics.md)
- Bias detection checklists (deliberation-framework.md)
- Specific viewpoint scoring rubrics

Each engine should reason about the decision from Logos / Pathos / Sophia *using its own training-data priors*. Magi main context applies framework rules at SYNTHESIZE.

**Required JSON output schema (per-subagent — emits 3 cells):**

```json
{
  "engine": "codex|agy|claude",
  "viewpoints": {
    "logos": {
      "verdict": "APPROVE|REJECT|ABSTAIN",
      "confidence": 0,
      "rationale": "One-paragraph technical/data reasoning (analytical lens)",
      "evidence": ["Specific datum or reference", "..."],
      "dissents": ["Counter-anchor this viewpoint considered before scoring"],
      "key_trade_offs": ["Trade-offs this lens surfaces"]
    },
    "pathos": {
      "verdict": "APPROVE|REJECT|ABSTAIN",
      "confidence": 0,
      "rationale": "One-paragraph user/team/ethics reasoning (human-centered lens)",
      "evidence": ["..."],
      "dissents": ["..."],
      "key_trade_offs": ["..."]
    },
    "sophia": {
      "verdict": "APPROVE|REJECT|ABSTAIN",
      "confidence": 0,
      "rationale": "One-paragraph business/ROI/timing reasoning (pragmatic lens)",
      "evidence": ["..."],
      "dissents": ["..."],
      "key_trade_offs": ["..."]
    }
  },
  "engine_notes": "Optional: what bias this engine knows it brings (e.g., 'Codex priors are GitHub-heavy; flags infra-cost trade-offs more often than UX cost')"
}
```

Each subagent therefore emits **3 cells** of the final 9-cell matrix. Three subagents × 3 viewpoints = 9 independent reasonings.

**Independence preservation**: subagents must not see each other's outputs before all have returned. Confidence anchoring across engines is the single biggest contamination risk; running all three Agent calls in the same message guarantees structural independence.

If an engine is genuinely unavailable per PREFLIGHT criteria, record the failure. With 2 engines: 6-cell matrix; with 1 engine: 3-cell degraded mode (flag reduced confidence). All 3 down → abort multi, degrade to `decide` Recipe.

## 4. NORMALIZE

Parse the three JSON blobs into a unified **9-cell matrix** indexed by `cell_id = "{viewpoint}_{engine}"` (e.g., `logos_codex`, `pathos_agy`, `sophia_claude`).

Preserve per-engine wording — divergent rationale phrasing inside the same viewpoint carries diagnostic signal. Do not collapse or summarize at this stage.

If an engine returns free-form Markdown or omits a viewpoint, ask its subagent to re-emit a complete JSON matching the schema before proceeding.

## 5. CLUSTER — two-pass identity (the key Magi-specific design)

Magi runs **two clustering passes** in sequence. Each pass produces a different signal.

### Pass A — Per-viewpoint engine clustering (concurrence axis)

For each viewpoint (Logos, Pathos, Sophia), cluster the 3 engine cells by verdict:

- `viewpoint_concurrence[logos]` = {APPROVE: [engines], REJECT: [engines], ABSTAIN: [engines]}
- Same for `pathos` and `sophia`

Within a viewpoint, two cells "match" when:

- Same `verdict` (APPROVE / REJECT / ABSTAIN)
- Rationale references the same primary concern class (e.g., performance, scalability, ethics, ROI, time-to-market) — semantic overlap, not literal string match
- Key trade-offs overlap (at least one shared trade-off dimension)

### Pass B — Per-engine viewpoint clustering (consistency axis)

For each engine (codex, agy, claude), check whether its three viewpoints agree:

- `engine_consistency[codex]` = "consistent (3-0)" | "mostly aligned (2-1)" | "split (1-1-1)" | "rejected (0-3)"
- Same for `agy` and `claude`

Per-engine consistency reveals whether one engine has a strong overall stance (all 3 viewpoints align) versus genuinely seeing trade-offs (split internally). It does NOT determine the verdict — it informs how to read that engine's contribution.

## 6. SCORE — pattern-specific (Pattern H, both axes)

Magi's scoring uses both Pass A (per-viewpoint concurrence) and Pass B (per-engine consistency), then derives an overall matrix pattern.

### Per-viewpoint concurrence labels (Pass A)

| Engines agreeing within viewpoint | Concurrence label | Perspective tag |
|-----------------------------------|-------------------|-----------------|
| 3 / 3 same verdict | `CONFIRMED` | `CONVERGENT` |
| 2 / 3 same verdict | `LIKELY` | `DIVERGENT-1` |
| 1 / 1 / 1 (all three differ) | `CANDIDATE` | `DIVERGENT-2` |
| 3 / 3 ABSTAIN | `UNDECIDED` | `CONVERGENT-ABSTAIN` |

A `CANDIDATE / DIVERGENT-2` viewpoint signals genuine uncertainty within that lens — surface it; do not average it away.

### Per-engine consistency labels (Pass B)

| Pattern across engine's 3 viewpoints | Engine label |
|--------------------------------------|--------------|
| 3-0 same verdict | `consistent` |
| 2-1 | `mostly-aligned` |
| 1-1-1 | `internally-split` |
| 0-3 reject | `consistent-reject` |

### Cross-cutting matrix patterns (the key Pattern H signal)

After Pass A + Pass B, extract these matrix patterns — they drive the final verdict shape:

| Matrix pattern | Meaning | Suggested verdict shape |
|----------------|---------|-------------------------|
| All 9 cells APPROVE | Universal approval | `GO` (high confidence) — still run devil's advocate per Magi 3-0 rule |
| All 9 cells REJECT | Universal rejection | `NO-GO` (high confidence) |
| Logos: 3/3 APPROVE; Pathos: 3/3 REJECT; Sophia: split | Technical-vs-human trade-off | `CONDITIONAL with ethical guardrails` — surface the lens conflict explicitly |
| All Logos APPROVE; All Sophia REJECT | Technical-vs-business trade-off | `CONDITIONAL` — Sophia objection becomes the gating criterion |
| All Pathos REJECT; Logos+Sophia mixed | Human-cost dominant blocker | `NO-GO unless human-cost mitigation` |
| One engine consistent-approve; other two consistent-reject | Engine-bias asymmetry | Investigate which engine's training data diverges; do not let one engine dominate (Byzantine cap at 50% weight per `_common/MULTI_ENGINE_RECIPE.md`) |
| All three engines `internally-split` (1-1-1 each) | Genuine high-dimensional uncertainty | `ESCALATE TO HUMAN` — the decision has real trade-offs no engine resolves |
| Per-viewpoint `CONFIRMED` on 3/3 viewpoints, but verdicts differ | 3 viewpoints each unanimous but different conclusions | Strong evidence of multi-objective trade-off; explicit `CONDITIONAL` with per-lens guardrails |

The matrix pattern is the verdict's primary input, not the average confidence score.

## 7. GROUND / CALIBRATE — Magi main context, never delegated

For Pattern H, ground both confidence and dissent:

1. **Hallucination check** — for any cell citing specific evidence (file paths, metrics, prior decisions, framework guarantees, regulatory clauses), verify the cited evidence actually exists. Reject cells whose rationale rests on hallucinated facts.
2. **Mitigation check** — does the cited concern already have a mitigation in the existing system? If a Pathos REJECT cites "no rollback path" but the team has a documented rollback runbook, downgrade that cell to ABSTAIN with a note.
3. **Specificity check** — is each cell's rationale concrete enough to be falsifiable? Vague rationales ("users won't like it") fail; specific ones ("survey N=120 showed 38% rejection of this UX pattern") pass.
4. **Confidence stress-test** — for any cell with confidence ≥ 85, apply "what would make this wrong?" Lower confidence if the counter-anchor cannot be answered.
5. **Calibration against shared evidence** — for KNOWLEDGE-type tasks, all three engines should have anchored to the shared factual base from FRAME. If one engine's evidence list diverges sharply, check whether that engine ignored the shared evidence or surfaced an additional fact.

Mark each cell as `VERIFIED` (keep as-is), `DOWNGRADED` (kept with adjusted verdict/confidence), or `REJECTED-{reason}` (drop from matrix).

For `CONFIRMED / CONVERGENT` viewpoints, do a lightweight spot-check on the first cell only — three engines rarely hallucinate the same concern simultaneously.

For `CANDIDATE / DIVERGENT-2` viewpoints (the 1-1-1 case within a lens), ground all three cells strictly — divergence is informative, but each dissent must rest on real evidence to count.

## 8. SYNTHESIZE — 9-cell matrix visualization + pattern-based verdict

Magi's `multi` SYNTHESIZE has two mandatory outputs:

### Output A — 9-cell matrix table (always present)

```
                      |  codex          |  agy            |  claude         | Viewpoint Concurrence
----------------------|-----------------|-----------------|-----------------|----------------------
Logos (Analyst)       |  APPROVE c.82   |  APPROVE c.78   |  REJECT  c.71   |  LIKELY (2/3 APPROVE) [DIVERGENT-1]
Pathos (Advocate)     |  REJECT  c.88   |  REJECT  c.85   |  REJECT  c.91   |  CONFIRMED (3/3 REJECT) [CONVERGENT]
Sophia (Strategist)   |  APPROVE c.74   |  ABSTAIN c.60   |  APPROVE c.69   |  LIKELY (2/3 APPROVE) [DIVERGENT-1]
----------------------|-----------------|-----------------|-----------------|----------------------
Engine Consistency    | mostly-aligned  | internally-split| internally-split|  Matrix pattern: see below
```

Each cell shows verdict + confidence. Row trailer = per-viewpoint concurrence + perspective tag. Column trailer = per-engine consistency.

Below the table, summarize each cell's rationale in 1-2 sentences (9 mini-paragraphs). Preserve the dissents — every well-reasoned `DOWNGRADED` cell stays in the synthesis with its counter-anchor visible.

### Output B — Pattern-based final verdict

Map the matrix pattern (from §6 cross-cutting table) to a final verdict:

```
FINAL VERDICT: [GO | NO-GO | CONDITIONAL | ESCALATE]

Matrix pattern: [one of the §6 patterns]
Weighted confidence: [0-100, derived from per-viewpoint CONFIRMED/LIKELY/CANDIDATE distribution
                      with single-engine influence capped at 50% per Byzantine resilience rule]

Verdict shape:
  - If GO / NO-GO: which matrix pattern justifies the unanimity, and what dissent (if any) is documented
  - If CONDITIONAL: which viewpoint(s) gate the decision, and what guardrails must accompany approval
  - If ESCALATE: which dimensions of uncertainty drove the split (per disagreement diagnostic)
```

### Devil's advocate trigger

If the matrix shows `CONFIRMED / CONVERGENT` on all 3 viewpoints (i.e., 9 cells unanimous), Magi's standard 3-0 groupthink rule applies — run a devil's advocate challenge before finalizing. In `multi` mode, the DA challenge is more credible because the unanimity already crosses 3 independent engines AND 3 independent viewpoints, so the DA must specifically attack the matrix pattern (not just one cell).

### Engine-attribution tags (mandatory)

Every shipped output carries tags per `_common/MULTI_ENGINE_RECIPE.md`:

- Per-viewpoint concurrence tag: `[codex+agy+claude]` (3/3) / `[codex+agy]` etc. (2/3) / `[codex-verified]` (1/3 grounded)
- Per-viewpoint perspective tag: `[CONVERGENT]` / `[DIVERGENT-1]` / `[DIVERGENT-2]`
- Final verdict carries a matrix-pattern label: `[matrix:all-9-approve]`, `[matrix:pathos-block]`, `[matrix:logos-sophia-split]`, etc.

## 9. DELIVER

Output structure layered on top of Magi's standard verdict template:

1. **MAGI MULTI-ENGINE VERDICT** header — banner naming the three engines that ran (and any failures)
2. **Decision restatement** + reversibility + task type (from FRAME)
3. **9-cell matrix table** (Output A above)
4. **Per-cell summaries** (9 short paragraphs, grouped by viewpoint)
5. **Cross-cutting matrix pattern** identified
6. **Final verdict + weighted confidence** (Output B above) with matrix-pattern label
7. **Risk register** — derived from `key_trade_offs` aggregated across cells, deduped, ranked by severity
8. **Cognitive bias check** — Magi standard (anchoring, confirmation, sunk cost, curse of knowledge) plus multi-engine-specific: cross-engine anchoring (any engine override another's framing?), engine-bias asymmetry (did one engine dominate the matrix?)
9. **Dissent record** — every DIVERGENT viewpoint's minority cells stay visible; for 9-cell-unanimous matrices, include the DA challenge result
10. **Engine status + rejection ledger** — which engines ran/failed, how many cells were REJECTED/DOWNGRADED at GROUND, by category
11. **Next steps + agent routing** — per Magi standard

Do not surface raw subagent JSON in the final report. Do not collapse the 9-cell matrix into a single "average verdict" — the matrix itself is the deliverable's most valuable artifact.

---

## Parallel Subagent Invocation

Use the Agent tool three times **in the same message** for genuine parallel execution. Each subagent receives a self-contained prompt:

```
You are the {engine} deliberation subagent for Magi.

# Role
Deliberate on the decision below from all three Magi viewpoints — Logos (technical/data),
Pathos (user/team/ethics), Sophia (business/ROI/timing). You are one of three engines
working independently. Apply your training-data priors; do not try to be exhaustive across
all engines — just give each viewpoint your honest reasoning.

Critically: keep the three viewpoints INDEPENDENT inside your own reasoning. Score each
viewpoint before considering the others. Do not let one viewpoint's verdict anchor the next.

# Target
- Decision question: {one clear question}
- Domain: {Architecture | Trade-off | Go/No-Go | Strategy | Priority}
- Reversibility: {HIGH | MEDIUM | LOW}
- Task type: {REASONING | KNOWLEDGE}
- Constraints: {constraints from FRAME}
- Shared evidence (for KNOWLEDGE tasks only): {metrics, test results, compliance evidence}
- Options being arbitrated: {explicit list if multi-option}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{viewpoints JSON schema from §3 FAN-OUT}

# Constraints
- Each viewpoint produces APPROVE / REJECT / ABSTAIN + confidence 0-100 + rationale
- Stress-test any confidence >= 85 with "what would make this wrong?" and include the counter-anchor in `dissents`
- For each viewpoint, list at least one counter-anchor BEFORE scoring (consider-the-opposite)
- Cite specific evidence in `evidence` — do not invent facts, file paths, metrics, or prior decisions the system clearly does not have
- Do not write implementation code
- Open with the deliverable (no completion preamble)
```

The three subagents return JSON; Magi main context handles NORMALIZE through DELIVER.

---

## Engine Availability Modes

> Per Base Engine Policy: Claude + Codex is the default baseline (NOT degraded). agy is optional — its absence is the normal dual-engine path, not a failure. See `_common/MULTI_ENGINE_RECIPE.md §Engine Availability Modes`.

| Situation | Mode | Behavior |
|-----------|------|----------|
| Claude + Codex + agy AVAILABLE | `tri-engine` | Run all three; 9-cell matrix; concurrence labels per tri-engine rubric (3/3 CONFIRMED, 2/3 LIKELY, 1/3 CANDIDATE) |
| Claude + Codex AVAILABLE, agy UNAVAILABLE or RUNTIME-BROKEN | `dual-engine` (default baseline) | Run Claude + Codex; **6-cell matrix**; concurrence labels per dual-engine rubric (2/2 CONFIRMED, 1/2 CANDIDATE — `LIKELY` is unreachable with 2 engines, so the bar for shipping a single-engine viewpoint is naturally tighter); matrix-pattern detection FULLY enabled (6 cells is sufficient for pattern recognition); record agy absence as informational header line, NOT as a failure |
| Only 1 of Claude/Codex AVAILABLE | `single-engine` (degraded) | Single-engine 3-cell matrix; every cell treated as CANDIDATE; ground all before reporting; flag reduced confidence; matrix-pattern detection DISABLED (3 cells too sparse for cross-engine pattern signal) |
| Both Claude and Codex unavailable | Abort multi flow; degrade to `decide` (Simple Mode three internal lenses) |
| User explicitly requests single engine | Skip fan-out; use standard `decide` Recipe |
| Trivial / low-stakes / fully-reversible decision | Recommend `decide` instead; reserve multi for high-stakes, low-reversibility |
| One engine's all 3 viewpoints return ABSTAIN | Treat as that engine declined to deliberate; flag but do not auto-replace |
| Engine returns < 3 viewpoints | Ask subagent to re-emit; if it cannot, mark missing viewpoints as ABSTAIN with `confidence: 0` |

---

## Why This Works for Magi (Pattern H — both axes matter)

- **9-cell matrix is the verdict's signal, not noise.** A single-engine three-viewpoint deliberation can only surface 3 perspectives; the tri-engine matrix surfaces 9 independent reasonings, and the *patterns across those 9 cells* (e.g., "all Pathos REJECT regardless of engine") are stronger evidence than any individual cell.
- **Concurrence within a viewpoint raises confidence.** When 3 engines independently approve from the Logos lens, that approval is more trustworthy than 3 viewpoints from one engine — independent priors cannot easily hallucinate the same evidence.
- **Divergence across viewpoints reveals trade-offs.** Pattern H explicitly preserves dissent. "All Logos APPROVE, all Pathos REJECT" is not a bug to average away — it is the decision's actual shape, and the verdict must reflect that as `CONDITIONAL` rather than collapsing to a meaningless 50%.
- **Two-pass clustering separates engine bias from viewpoint signal.** Per-viewpoint concurrence (Pass A) measures inter-engine agreement on one lens; per-engine consistency (Pass B) measures intra-engine alignment across lenses. The two passes together prevent one engine's strong stance from dominating the matrix (Byzantine 50%-cap rule).
- **Independence preserved across both axes.** Subagents emit all 3 viewpoints in one payload, but the prompt instructs them to keep the 3 viewpoints independent inside their reasoning. Cross-engine independence comes from parallel spawn; cross-viewpoint independence comes from prompt discipline.
- **Pattern-based verdict matches real Magi use cases.** GO / NO-GO / CONDITIONAL / ESCALATE are not derived from averaged confidence but from the matrix shape — the same way an experienced decision-maker reads a disagreement.

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — Pattern H protocol (concurrence + divergence both matter), PREFLIGHT, FAN-OUT, engine-attribution tags, degraded modes
- `_common/SUBAGENT.md §MULTI_ENGINE` — base engine dispatch and loose-prompt rules
- `judge/reference/tri-engine-review.md` — canonical Pattern C reference (PREFLIGHT and FAN-OUT mechanics mirrored here)
- `spark/reference/tri-engine-proposal.md` — sibling Pattern D reference (divergence preservation analog)
- `magi/reference/deliberation-framework.md` — three-viewpoint heuristics applied inside each cell's reasoning
- `magi/reference/voting-mechanics.md` — confidence calibration, consensus patterns, escalation rules
- `magi/reference/decision-domains.md` — domain-specific viewpoint focus matrices applied at SYNTHESIZE
- `magi/reference/engine-deliberation-guide.md` — Engine Mode sibling for Simple-Mode Recipes (`decide` / `tradeoff` / `arbitrate` / `strategic`); each engine emits ONE integrated YAML position (not 3 viewpoints) and the result is a 3-engine vote, not a 9-cell matrix. `multi` Recipe supersedes it when tri-engine 9-cell deliberation is required.
- `magi/reference/devils-advocate.md` — DA challenge protocol invoked when 9-cell matrix is unanimous
