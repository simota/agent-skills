# Multi-Engine Parallel Review

Default flow for `/judge`. Run reviews in parallel via subagents across the available engines, integrate results, verify findings, and return **only findings that warrant fixing**.

**Base Engine Policy (2026-05 update)**: The default baseline is **Claude + Codex (dual-engine)**. agy / Antigravity is added as an optional third axis when AVAILABLE at PREFLIGHT — never required. Filename retained as `tri-engine-review.md` for backward compatibility; the content covers both tri-engine and dual-engine modes. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy`.

**Why multi-engine:** Each LLM family misses different defect classes. Single-engine review delivers ~45% defect detection; multi-engine concurrence + grounding raises precision above 90% while collapsing noise. Independent subagent contexts also eliminate self-bias — especially critical when Claude is one of the engines. **Dual-engine (Claude + Codex) covers the load-bearing diversity** — judgment-oriented + sandbox-execution priors are non-overlapping. agy contributes a third axis (1M context / multimodal / Search) that lifts coverage further when reachable.

---

## Flow

```
SCOPE → PREFLIGHT → FAN-OUT (parallel subagents for available engines) → NORMALIZE → CLUSTER → SCORE → GROUND → ARBITRATE → FILTER → REPORT
```

### 1. SCOPE

Define the review target once. All three subagents share the same scope:

- Review mode (PR / Pre-Commit / Commit / `--from-pr`)
- Base branch or SHA
- Focus areas (security / intent / framework / AI-code)
- Project guidelines (REVIEW.md / AGENTS.md / CLAUDE.md content)

### 2. PREFLIGHT — engine availability detection (Judge main context, never delegated)

Detect engine availability **once in the main Judge context** before spawning subagents. Subagents must not perform their own availability detection — their inherited PATH may be narrower than the user's interactive shell, leading to false-negative "unavailable" verdicts when the binary actually exists in a non-standard location (`~/.bun/bin`, `~/.local/bin`, npm/pnpm/yarn global, mise/asdf shims).

**Robust detection — try in order, accept first success:**

```bash
# 1. Standard PATH lookup
command -v codex && codex --version

# 2. Explicit fallback to known install locations (run if step 1 fails)
for p in "$HOME/.bun/bin/codex" "$HOME/.local/bin/codex" "/usr/local/bin/codex" "/opt/homebrew/bin/codex" "$HOME/.npm-global/bin/codex"; do
  [ -x "$p" ] && "$p" --version && export CODEX_BIN="$p" && break
done
```

Apply the same loop for `agy` and `claude`. The user's actual install paths today: `~/.bun/bin/codex`, `~/.bun/bin/agy`, `~/.local/bin/claude` — these MUST be probed before declaring any engine unavailable.

**Single combined preflight command (recommended):**

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

**Availability verdict — strict criteria:**

| Outcome | Treatment |
|---------|-----------|
| Binary found AND `--version` returns | `AVAILABLE` — pass absolute path to the subagent if the standard PATH probe failed |
| Binary not found in any probed location | `UNAVAILABLE (binary missing)` — skip this engine, record reason |
| Binary found but `--version` exits non-zero | `AVAILABLE-WITH-WARNING` — still attempt review; surface warning in report |
| Auth error during version check | `AVAILABLE` — auth errors at review time are runtime failures, not unavailability. Pass through to subagent for diagnosis |
| Timeout / network failure during version check | `AVAILABLE` — transient failures are not unavailability. Pass through |

**Never declare an engine unavailable based on:**

- Single CLI run failure (transient network / auth / quota issues)
- A subagent's prior session error from a different invocation
- Assumption from absence in the standard `$PATH` only — always probe fallback paths
- The user's most recent successful invocation pattern (e.g., "they only ran Claude last time")

When passing an absolute binary path to a subagent (because the standard PATH probe failed), tell the subagent to invoke that exact path verbatim instead of the bare command name.

### 3. FAN-OUT — parallel subagents

Spawn **one Agent call per AVAILABLE engine in a single message** so they run concurrently. Each subagent has an independent context window (no self-bias) and runs one engine. **Dual-engine baseline = 2 spawns** (Claude + Codex); **tri-engine = 3 spawns** when agy is also AVAILABLE.

| Subagent | Engine | Spawn Condition | Reference | Baseline command |
|----------|--------|-----------------|-----------|------------------|
| `review-codex` | Codex CLI | Always (Codex required for judge) | `codex-review-usage.md` | `codex review --base <branch> "<focused prompt>"` |
| `review-claude` | Claude Code CLI | Always (host engine) | `claude-review-usage.md` | `claude -p "<focused prompt>" --permission-mode plan` |
| `review-agy` | Antigravity CLI | **Only when AVAILABLE at PREFLIGHT** | `antigravity-review-usage.md` | `agy -p "<focused prompt>" --dangerously-skip-permissions --log-file <tmp>` (silent-failure detection per `antigravity-review-usage.md` § Silent Failure Detection) |

Each subagent prompt must require structured JSON output so integration is deterministic:

```json
{
  "engine": "codex|agy|claude",
  "findings": [
    {
      "severity": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
      "file": "path/to/file.ts",
      "line": 42,
      "line_end": 47,
      "issue_class": "null-access|injection|logic-error|...",
      "issue": "One-line description",
      "evidence": "Quoted code or explanation",
      "suggested_fix": "Concrete change"
    }
  ],
  "scope_summary": { "files_reviewed": 12, "loc_delta": 340 }
}
```

**agy UNAVAILABLE handling**: agy missing or RUNTIME-BROKEN is the **normal dual-engine path**, NOT a degraded mode. Record `agy: skipped (engine unavailable)` in the report header and proceed with Claude + Codex. Auth-expired, network, and quota errors during agy execution → mark RUNTIME-BROKEN per `_common/MULTI_ENGINE_RECIPE.md §3.5` and fall through to dual-engine without aborting. Below two engines (i.e. Claude OR Codex also missing), downgrade to single-engine output and flag reduced confidence explicitly.

**Silent-failure detection (agy in particular):** A subagent must always pass `--log-file <tmp>` and check stdout. If `agy` (or any engine) exits 0 with empty stdout, grep the log for `RESOURCE_EXHAUSTED|Resets in|error getting token|agent executor error|unexpected end of JSON input` and report the engine as `RUNTIME-BROKEN` (with the matched line as evidence) rather than emitting empty findings. Do NOT include such an engine in concurrence tags. Record the reason (`quota`/`auth`/`mcp_corrupt`/`upstream`) in the rejections ledger. See `antigravity-review-usage.md` § Silent Failure Detection.

### 3. NORMALIZE

Parse the three JSON blobs into a unified finding list. Tag each finding with its source engine. If an engine returns free-form Markdown, ask its subagent to re-emit as JSON before integrating.

### 4. CLUSTER — dedup across engines

Group findings that likely describe the same defect. Two findings match when **all three** hold:

- same `file`
- line ranges overlap within ±3 lines (tolerance for slightly different anchors)
- same `issue_class` OR high semantic overlap in the `issue` text (same vulnerability class, same bug pattern, same API contract)

Record the set of engines that flagged each cluster.

### 5. SCORE — initial confidence

**Tri-engine mode** (Claude + Codex + agy AVAILABLE):

| Engines flagging | Label | Action |
|------------------|-------|--------|
| 3 / 3 | `CONFIRMED` | Keep — skip grounding for time, still run a sanity read |
| 2 / 3 | `LIKELY` | Keep — record the dissenting engine's silence as a note |
| 1 / 3 | `CANDIDATE` | Must pass grounding (step 6) to survive |

**Dual-engine mode** (Claude + Codex only — agy UNAVAILABLE):

| Engines flagging | Label | Action |
|------------------|-------|--------|
| 2 / 2 | `CONFIRMED` | Keep — skip grounding for time, still run a sanity read |
| 1 / 2 | `CANDIDATE` | Must pass grounding (step 6) to survive. `LIKELY` is unreachable in dual-engine mode (1/2 is structurally indistinguishable from CANDIDATE), so the bar for shipping a single-engine finding is automatically higher than in tri-engine mode |

### 6. GROUND — verify CANDIDATE and LIKELY findings (and spot-check CONFIRMED)

Grounding is the Judge's own work in the main context — do not delegate this step. Run grounding on every CANDIDATE and LIKELY cluster (LIKELY gets a lighter touch since two engines already concur). For each:

1. Read the actual code at the cited file:line using the Read tool.
2. Answer explicitly:
   - **Does the defect exist in the code as described?** If the engine hallucinated a symbol, import, or API call, reject.
   - **Is there already a mitigation upstream?** (input validation earlier, type guard, framework guarantee, dead-code path, test-only file)
   - **Is the "fix" correctness-bearing or style-only?** Style-only belongs to Zen — drop for Judge output.
   - **Does the suggested fix actually address the stated issue?** If the fix is unrelated, treat the finding as unverified.
3. Mark each as `VERIFIED` / `LIKELY-VERIFIED` (keep), `REJECTED` (drop with reason), or `NEEDS-INFO` (escalate — ask the user). Use `LIKELY-VERIFIED` for 2/3 clusters that passed the lightweight check; use `VERIFIED` for 1/3 CANDIDATE clusters that passed the stricter check.

For CONFIRMED findings, do a lightweight spot-check: read the first CONFIRMED finding's site to confirm the engines didn't all share the same hallucination. Beyond that, trust 3/3 concurrence.

### 7. ARBITRATE — severity and remediation

- **Severity conflicts:** default to the highest severity any engine assigned, then apply override rules from `codex-integration.md` (e.g., downgrade when type-guaranteed, upgrade when on hot path). Record the arbitration reason.
- **Intent-alignment conflicts:** trust the engine with the most specific evidence (the one quoting the PR description verbatim wins over abstract claims).
- **Remediation agent routing:** apply the standard Judge map — CRITICAL/HIGH bug → Builder, Security → Sentinel, Consistency → Zen, Missing tests → Radar, Architecture → Atlas.

### 8. FILTER — keep only actionable fixes

A finding ships to the report only if all of these hold:

- `VERIFIED`, `LIKELY-VERIFIED`, or `CONFIRMED` (no REJECTED)
- Severity ≥ MEDIUM, OR user explicitly asked for LOW/INFO
- Has a concrete `suggested_fix`
- Is not already mitigated in the code
- Is not style-only (those are Zen's domain)

Everything else is dropped. The goal is: **every finding in the output is something that should be changed.**

### 9. REPORT

Structure the final report around the filtered set only. Include:

- Summary table: total findings per severity after filtering, engine concurrence stats (e.g., `3/3: 2, 2/3: 5, 1/3-verified: 3`).
- Engine status: which of the three ran successfully; note any unavailability.
- Findings list, each with: ID, file:line, severity, issue, evidence, suggested fix, engine concurrence (tri-engine: `[codex+agy+claude]` / `[codex+agy]` etc. / `[claude-verified]` ; dual-engine: `[codex+claude]` / `[codex-verified]` / `[claude-verified]`), remediation agent.
- Intent-alignment verdict (if requested).
- Rejections ledger (optional, condensed): count and categories of findings that were dropped during grounding — this preserves SNR transparency without re-introducing noise.
- Overall verdict: `APPROVE` / `REQUEST CHANGES` / `BLOCK`.

Do not include rejected findings in the main list. Do not surface engine-raw output.

---

## Parallel Subagent Invocation

Use the Agent tool three times **in the same message** for genuine parallel execution. Each subagent should receive a self-contained prompt that:

1. States the engine to run and the exact CLI command (per the engine's usage reference).
2. Provides the SCOPE artifacts (base branch, SHA, focus areas, REVIEW.md contents).
3. Requires the JSON output schema above.
4. Forbids modifying code — this is review-only.

Example prompt skeleton:

```
You are the {engine} review subagent. Run the following command verbatim
(no model override, no API key):

    {engine-specific command}

Return findings as JSON matching this exact schema:

{schema}

Scope:
- Base: {base}
- Focus: {focus areas}
- Project guidelines: {REVIEW.md / AGENTS.md contents inline}

Do not modify any files. Do not emit commentary outside the JSON.
```

---

## Engine Availability Modes

> Per Base Engine Policy: Claude+Codex is the default baseline (NOT degraded). agy is optional — its absence is the normal dual-engine path, not a failure. See `_common/MULTI_ENGINE_RECIPE.md §Engine Availability Modes` for the canonical reference.

| Situation | Mode | Behavior |
|-----------|------|----------|
| Claude + Codex + agy AVAILABLE | `tri-engine` | Run all three; 3/2/1-of-3 scoring per SCORE table tri-engine row |
| Claude + Codex AVAILABLE, agy UNAVAILABLE or RUNTIME-BROKEN | `dual-engine` (default) | Run Claude + Codex; 2/1-of-2 scoring per SCORE table dual-engine row; record agy absence as informational header line, NOT as a failure |
| Only 1 of Claude/Codex AVAILABLE | `single-engine` (degraded) | Single-engine output; treat every finding as CANDIDATE; ground all before reporting; flag reduced confidence explicitly |
| Both Claude and Codex unavailable | Abort; surface the failure to the user; do not guess findings |
| User explicitly requests single engine | Skip fan-out entirely; use that engine's normal flow |
| Scope <50 LOC and low-risk | Optionally use single-engine; record the short-scope rationale |

---

## Why This Works

- **Independent contexts eliminate self-bias** — especially when Claude is one engine reviewing potentially-Claude-authored code.
- **Concurrence filters hallucinations** — engines rarely hallucinate the *same* false positive. A 3/3 cluster is almost never a false alarm.
- **Grounding catches single-engine errors** — the 1/3 cases are where engines disagree; reading the actual code decides truth.
- **Filter-out-style preserves SNR** — Judge's most-damaging anti-pattern is noisy output that erodes developer trust. The tri-engine flow is explicitly designed so every finding that ships is worth fixing.

---

## Cross-References

- `codex-review-usage.md` — how `review-codex` subagent invokes Codex
- `antigravity-review-usage.md` — how `review-agy` subagent invokes Gemini
- `claude-review-usage.md` — how `review-claude` subagent invokes Claude
- `codex-integration.md` — severity override rules, report template, multi-agent verification rationale
- `review-anti-patterns.md` — why filtering noise matters more than maximizing recall
