# Multi-Engine Proposal Generation

> **Filename retained** as `tri-engine-proposal.md` for backward compatibility. Covers both dual-engine baseline (Claude + Codex, 2 spawns / 6 cells) and tri-engine optional (Claude + Codex + agy, 3 spawns / 9 cells) modes.

Default flow for `/spark multi`. Run subagents in parallel — one per AVAILABLE engine — to generate feature proposals, integrate results across two axes (concurrence + divergence), and deliver either a Compete-merged single best proposal or a Portfolio of complementary proposals.

**Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (dual-engine, 2 spawns)**. agy adds a third axis (tri-engine, 3 spawns) only when AVAILABLE at PREFLIGHT. Dual-engine mode is NOT degraded. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy + §Engine Availability Modes` for tag vocabulary (`[codex+claude]` for dual / `[codex+agy+claude]` etc. for tri) and runtime mode selection.

**Pattern**: D (Divergence-primary) per `_common/MULTI_ENGINE_RECIPE.md`. Divergent single-engine proposals are NOT auto-low-value — they often surface the breakthrough opportunity each engine's training-data blind spot would otherwise hide.

**Why three engines for proposals (different from Judge):** Judge optimizes for *agreement on a single defect* — concurrence is the quality signal, divergence is noise. Spark optimizes for *creative recombination of existing data/logic* — concurrence reveals universally strong opportunities, but divergence reveals each engine's unique training-data blind spots. Both axes carry value. A 3/3 concurrent proposal is a "safe bet"; a 1/3 divergent proposal may be the breakthrough.

**Adapted from `judge/reference/tri-engine-review.md`. Re-uses PREFLIGHT, FAN-OUT, NORMALIZE, and CLUSTER stages; replaces SCORE/GROUND/FILTER with Concurrence-Divergence Scoring and Synthesis.**

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT (parallel subagents) → NORMALIZE → CLUSTER → SCORE (concurrence + divergence) → SYNTHESIZE → PRESENT
```

### 1. SCOPE

Define the proposal target once. All three subagents share the same scope:

- Product / feature surface (existing capabilities, unused data, repeated workflows)
- Target persona (ideally from Cast registry at `.agents/personas/registry.yaml`)
- Outcome anchor (the behavioral metric the proposal should move)
- Constraints (effort ceiling, regulated domain, dark-pattern bans)
- Discovery evidence (Pulse metrics, Voice feedback, Compete gaps, Field findings — if present)

### 2. PREFLIGHT — engine availability detection (Spark main context, never delegated)

Detect engine availability **once in the main Spark context** before spawning subagents. Subagent PATH is narrower than the user's interactive shell; never delegate availability detection.

Use the combined preflight from `judge/reference/tri-engine-review.md §2`. The probe order is identical:

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

Availability verdict and "never declare unavailable based on..." rules: identical to Judge tri-engine PREFLIGHT.

### 3. FAN-OUT — parallel subagents

Spawn **three Agent calls in a single message** so they run concurrently. Each subagent has an independent context (different training data, different ideation bias) and produces proposals independently.

| Subagent | Engine | Baseline command |
|----------|--------|------------------|
| `propose-codex` | Codex CLI | `codex exec --full-auto "<prompt>"` |
| `propose-agy` | Antigravity CLI | `agy -p "<prompt>" --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) |
| `propose-claude` | Claude Code CLI (subagent) | Agent tool with `subagent_type: general-purpose` |

**Loose prompt rule (per `_common/SUBAGENT.md` MULTI_ENGINE)**: pass only Role + Target + Output format. Do NOT pass JTBD templates, RICE rubrics, OST taxonomies, or persona archetypes — let each engine apply its own training-data priors. The Spark main context applies framework rules during SYNTHESIZE, not at FAN-OUT.

**Required JSON output schema:**

```json
{
  "engine": "codex|agy|claude",
  "proposals": [
    {
      "title": "Problem-named title (user pain, not solution shape)",
      "persona": "Target persona name or archetype",
      "user_problem": "What the user struggles to do today",
      "core_idea": "One-sentence solution shape",
      "evidence_basis": "Which existing data/logic/workflow this recombines",
      "outcome_hypothesis": "Behavioral metric this should move and direction",
      "fail_condition": "Threshold that disproves the hypothesis (e.g., '<2% adoption after 30d')",
      "effort_class": "S|M|L|XL",
      "risk_notes": ["dark-pattern risk", "privacy risk", "scope-creep risk", ...]
    }
  ],
  "engine_notes": "Optional: what bias this engine knows it brings"
}
```

If an engine is genuinely unavailable per PREFLIGHT criteria, record the failure and proceed with remaining engines. Below two engines, downgrade to single-engine output and flag reduced ideation breadth.

### 4. NORMALIZE

Parse the three JSON blobs into a unified proposal list. Tag each proposal with its source engine. If an engine returns free-form Markdown, ask its subagent to re-emit as JSON before integrating.

### 5. CLUSTER — dedup across engines

Group proposals that likely describe the same opportunity. Two proposals match when **all three** hold:

- same or overlapping `persona`
- same `user_problem` (semantic overlap, not literal string match — "can't export large datasets" matches "export limit pain")
- same `core_idea` class (e.g., "bulk export action" and "background export job" are the same class; "scheduled report" is a different class)

Record the set of engines that proposed each cluster. Preserve per-engine wording variations — they may reveal different angles on the same opportunity.

### 6. SCORE — concurrence + divergence (the key difference from Judge)

Spark scores each cluster on **two axes**, not one:

| Engines in cluster | Concurrence label | Divergence label | Interpretation |
|--------------------|-------------------|------------------|----------------|
| 3 / 3 | `UNIVERSAL` | none | All engines independently arrived here — likely a safe, well-recognized opportunity. May also indicate training-data common ground (could be obvious or already shipped — check for duplication). |
| 2 / 3 | `LIKELY` | mild | Two engines concur; one missed it — check whether the missing engine had a substantive reason or just a different angle. |
| 1 / 3 | `CANDIDATE` | `DIVERGENT` | Only one engine surfaced this. Either a unique insight from that engine's training data OR a low-quality random guess. Must pass grounding (step 7) to survive. |

**Critical rule for Spark (does NOT exist in Judge):** A `DIVERGENT` proposal is not automatically lower-value than a `UNIVERSAL` one. The breakthrough proposal often comes from the engine with non-overlapping training data. Surface both axes in the final report.

### 7. GROUND — verify CANDIDATE/DIVERGENT proposals (Spark main context, never delegated)

For every `CANDIDATE / DIVERGENT` cluster, the Spark main context must:

1. **Duplication check** — does this opportunity already exist in the current product? (Read codebase, Lens insight if available, existing feature list.) If duplicate, mark `REJECTED-DUPLICATE` unless the proposal explicitly notes the duplicate and offers a meaningful evolution.
2. **Persona-fit check** — is the named persona real (from Cast registry) or fabricated? If fabricated, downgrade confidence; if it contradicts Cast registry, mark `REJECTED-PERSONA-MISMATCH`.
3. **Evidence-basis check** — does the cited "existing data/logic/workflow" actually exist? AI engines can hallucinate capabilities. If hallucinated, mark `REJECTED-HALLUCINATION`.
4. **Hypothesis quality check** — is `outcome_hypothesis` measurable? Is `fail_condition` specific enough to actually kill the feature? Vague hypotheses (e.g., "users will be happier") fail this check.
5. **Mark each as** `VERIFIED-DIVERGENT` (keep), `REJECTED-{reason}` (drop), or `NEEDS-INFO` (escalate — ask the user).

For `UNIVERSAL` and `LIKELY` clusters, do a lightweight duplication spot-check only — three engines rarely hallucinate the same product capability simultaneously, but they may all suggest something already shipped.

### 8. SYNTHESIZE — Compete vs Portfolio (user-selectable merge strategy)

Spark supports two merge strategies. Default is **Portfolio** unless the user explicitly asks for a single proposal or invokes `multi --compete`.

#### Compete Merge (single best proposal)

When the user wants one RFC, not a menu:

1. Rank surviving clusters by: `UNIVERSAL > LIKELY > VERIFIED-DIVERGENT`.
2. Within the same concurrence tier, rank by hypothesis specificity, fail-condition strength, and effort-to-reach ratio.
3. Select the top cluster as the winner.
4. **Re-mix wording from the other engines** — the winning cluster's core_idea may have better wording in a different engine's version. Take the best phrasing per field across the 2-3 engine variants.
5. Emit a single RFC at `docs/proposals/RFC-[name].md` following the standard Spark proposal template, with an `engine_concurrence` line in the front matter (e.g., `engine_concurrence: 3/3 [codex+agy+claude]`).

#### Portfolio Merge (default — multiple complementary proposals)

When the user wants a menu of options:

1. Keep all `UNIVERSAL`, `LIKELY`, and `VERIFIED-DIVERGENT` clusters.
2. Limit to top 5-7 proposals (Spark's "one feature per session" rule is relaxed in multi mode — but still avoid bloat).
3. Order by: first the `UNIVERSAL` proposals (safe bets), then `LIKELY` proposals (strong-with-one-dissenter), then `VERIFIED-DIVERGENT` proposals (breakthrough candidates from a single engine).
4. Emit a single portfolio document at `docs/proposals/PORTFOLIO-[topic]-[date].md` listing all proposals with concurrence tags, plus a final recommendation section identifying which proposal Spark would pursue first and why.

#### Engine-attribution rule for both strategies

Every proposal that ships must include an `engine_concurrence` tag:

- `[codex+agy+claude]` — 3/3 UNIVERSAL
- `[codex+agy]` (or any 2-engine combo) — 2/3 LIKELY
- `[codex-verified]` (or `[agy-verified]` / `[claude-verified]`) — 1/3 VERIFIED-DIVERGENT after grounding

### 9. PRESENT

Output structure depends on merge strategy:

**Compete output**: a single RFC matching the standard Spark proposal format with `engine_concurrence` front matter, plus a brief "Alternative proposals considered" appendix summarizing the rejected clusters with one-line rationale.

**Portfolio output**: a single document with:

- Summary table: total proposals per concurrence tier (`UNIVERSAL: N, LIKELY: N, VERIFIED-DIVERGENT: N`)
- Engine status: which of the three engines ran successfully; note any unavailability
- Proposals list, each with: ID, title (problem-named), persona, core_idea, evidence_basis, outcome_hypothesis, fail_condition, effort_class, `engine_concurrence` tag
- Rejection ledger (condensed): count and categories of rejected clusters (duplicate / hallucinated / persona-mismatch / vague-hypothesis) — preserves transparency without re-introducing noise
- Recommendation: which proposal to pursue first, and why (specific to concurrence/divergence reasoning)

Do not include rejected proposals in the main list. Do not surface engine-raw output.

---

## Parallel Subagent Invocation

Use the Agent tool three times **in the same message** for genuine parallel execution. Each subagent receives a self-contained prompt:

```
You are the {engine} proposal subagent for Spark.

# Role
Generate {N=3-5} feature proposals for the target below. You are one of three engines working independently — do not try to be exhaustive; surface what your training data suggests is most promising.

# Target
- Product / feature surface: {scope}
- Persona pool: {personas from Cast registry or "open"}
- Outcome anchor: {behavioral metric to move}
- Discovery evidence: {Pulse / Voice / Compete / Field findings if any}

# Output format
Return ONLY JSON matching this exact schema (no commentary outside the JSON):

{JSON schema}

# Constraints
- Each proposal names the user PROBLEM, not the solution (e.g., "Difficulty exporting large datasets" not "CSV Export Button")
- Each proposal targets a SPECIFIC persona (never "everyone")
- Each proposal includes a measurable outcome_hypothesis AND a fail_condition
- Do not write implementation code — proposals only
- Do not paraphrase or invent capabilities the product clearly does not have; if you assert reuse of existing data/logic, name it specifically
```

The three subagents return JSON; Spark main context handles NORMALIZE through PRESENT.

---

## Degraded Modes

| Situation | Behavior |
|-----------|----------|
| 1 engine binary missing | Run the other two; note reduced ideation breadth; `CANDIDATE / DIVERGENT` clusters from the single remaining engine require stricter grounding |
| 2 engines fail | Single-engine output; treat every proposal as `CANDIDATE`; ground all before reporting; flag reduced confidence |
| All 3 fail | Abort tri-engine flow; degrade to standard `propose` Recipe with the Spark main context |
| User explicitly requests single engine | Skip fan-out; use standard `propose` Recipe |
| Scope obviously trivial (e.g., "add a button to do X") | Optionally skip multi mode; recommend single-engine `propose` |

---

## Why This Works for Proposals (different from Judge)

- **Independent training data surfaces non-overlapping ideas.** Codex's GitHub-heavy corpus, Antigravity's Google-product corpus, and Claude's Anthropic-curated corpus all bias toward different reference designs. A 1/3 divergent proposal often represents one engine's unique angle, not a hallucination.
- **Concurrence still filters obvious hallucinations.** When all three engines independently recombine the same existing capabilities into the same proposal, that proposal is almost certainly grounded in the product's real surface area.
- **The Compete/Portfolio split matches real product-discovery use cases.** Users sometimes want one RFC (Compete); sometimes want a menu (Portfolio). Forcing one mode would mismatch the workflow.
- **Spark's anti-pattern guardrails (no "everyone" personas, no activity-framed JTBD, no Confidence >50% without evidence, ≤20% Impact=3 distribution) apply in SYNTHESIZE, not at FAN-OUT.** Letting engines run loose maximizes divergence; rule enforcement happens centrally.

---

## Cross-References

- `_common/SUBAGENT.md §MULTI_ENGINE` — base protocol for engine dispatch and loose prompts
- `judge/reference/tri-engine-review.md` — sibling tri-engine flow (review domain); PREFLIGHT and FAN-OUT logic mirrored here
- `spark/reference/proposal-templates.md` — Compete-merge output format
- `spark/reference/feature-ideation-anti-patterns.md` — applied during SYNTHESIZE to filter weak hypotheses
- `spark/reference/modern-product-discovery.md` — OST framing applied at SYNTHESIZE to anchor proposals to outcomes
