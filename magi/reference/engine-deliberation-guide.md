# Engine Deliberation Guide

Engine Mode specification for Magi's three-engine deliberation system. In Engine Mode, Claude, Codex, and Gemini each provide a **single integrated analysis** (one unified position per engine) — they do **not** each simulate three internal viewpoints.

**Scope vs `tri-engine-deliberate.md`:** this file covers Engine Mode auto-activated *inside* Simple-Mode Recipes (`decide`, `tradeoff`, `arbitrate`, `strategic`) — one engine = one YAML position, aggregated as a 3-engine vote (or 2 / 1 depending on availability). The `multi` Recipe instead uses Pattern H (`tri-engine-deliberate.md`), where each engine emits **all three viewpoints** as JSON and the result is a 9-cell matrix. When a Recipe routes here, the output schema below applies; when routed to `multi`, the JSON schema in `tri-engine-deliberate.md §3` applies. Engine binaries and silent-failure detection are canonical in `_common/MULTI_ENGINE_RECIPE.md` — this file only references them.

---

## Engine Availability Check

Use the canonical probe from `_common/MULTI_ENGINE_RECIPE.md §2 PREFLIGHT` (combined `which` + `--version` + actual smoke invocation, run from Magi main context — subagent PATH is narrower). Quick reference:

```bash
which codex && echo "codex: available" || echo "codex: not found"
which agy && echo "agy: available" || echo "agy: not found"
```

Engine command summary (full invocation contract lives in `_common/MULTI_ENGINE_RECIPE.md §3 FAN-OUT`):

| Engine | Command | Role in Engine Mode |
|--------|---------|---------------------|
| **Claude** | (internal) | Primary deliberator, orchestrator |
| **Codex** | `codex exec --full-auto "{prompt}"` | Independent external deliberator |
| **Antigravity** | `agy -p "{prompt}" --dangerously-skip-permissions --log-file <path>` (silent-failure detection mandatory — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection`) | Independent external deliberator |

---

## Deliberation Prompt Template (Codex)

Codex is invoked via `codex exec --full-auto` with a concise, directive prompt optimized for structured output.

**Important:** This is a text analysis task, not code generation. The prompt must explicitly request analytical output.

### Prompt Structure

```text
codex exec --full-auto "You are a decision analyst. Evaluate the following decision independently.

DECISION: {subject}
TYPE: {decision_type}
CONTEXT: {context_summary}
OPTIONS: {options}
CONSTRAINTS: {constraints}

Provide your analysis as YAML in a code block:

\`\`\`yaml
position: APPROVE | REJECT | ABSTAIN
confidence: 0-100
rationale: "2-3 sentence explanation of your position"
key_evidence:
  - "Evidence point 1"
  - "Evidence point 2"
risks:
  - "Risk 1"
  - "Risk 2"
conditions:
  - "Condition for approval (if any)"
dissent_note: "Key concern if this decision goes the other way"
\`\`\`

Be direct. State your position clearly. Do not hedge."
```

### Codex Optimization Notes

- Keep prompts concise and directive (Codex performs best with clear instructions)
- Avoid verbose background sections
- Request YAML output explicitly
- Use `--full-auto` to avoid interactive prompts

---

## Deliberation Prompt Template (Gemini)

Antigravity CLI (`agy`) is invoked via `agy -p` with `--dangerously-skip-permissions` plus `--log-file <path>` for non-interactive execution. Antigravity benefits from additional context due to its larger context window. **agy v1.0.0 silent-failure detection is mandatory** — see `_common/MULTI_ENGINE_RECIPE.md §3.5 Engine Runtime Failure Detection` for the canonical headless pattern (mktemp log file, empty-stdout grep, `RUNTIME-BROKEN` ledger).

### Prompt Structure

```text
agy -p "You are a decision analyst. Evaluate the following decision independently.

## Background
{extended_context}

## Decision
DECISION: {subject}
TYPE: {decision_type}
OPTIONS: {options}
CONSTRAINTS: {constraints}

## Instructions
Provide your analysis as YAML in a code block:

\`\`\`yaml
position: APPROVE | REJECT | ABSTAIN
confidence: 0-100
rationale: "2-3 sentence explanation of your position"
key_evidence:
  - "Evidence point 1"
  - "Evidence point 2"
risks:
  - "Risk 1"
  - "Risk 2"
conditions:
  - "Condition for approval (if any)"
dissent_note: "Key concern if this decision goes the other way"
\`\`\`

Be direct. State your position clearly. Do not hedge." --dangerously-skip-permissions
```

### Gemini Optimization Notes

- Include a `## Background` section with extended context (leverages larger context window)
- Same YAML output format as Codex for consistent parsing
- `--dangerously-skip-permissions` flag enables non-interactive execution

---

## Claude Internal Deliberation (Engine Mode)

In Engine Mode, Claude does **not** simulate three perspectives (that is Simple Mode). Instead, Claude provides a single, integrated analysis as one unified viewpoint.

### Claude's Engine Mode Behavior

1. Analyze the decision from a **unified perspective** (combining technical, human, and strategic considerations)
2. Output in the **same YAML format** as Codex and Gemini
3. Complete analysis **before** collecting external engine outputs (contamination prevention)

### Claude Output Format

```yaml
position: APPROVE | REJECT | ABSTAIN
confidence: 0-100
rationale: "2-3 sentence integrated analysis"
key_evidence:
  - "Evidence point 1"
  - "Evidence point 2"
risks:
  - "Risk 1"
  - "Risk 2"
conditions:
  - "Condition for approval (if any)"
dissent_note: "Key concern if this decision goes the other way"
```

---

## Output Parsing Strategy

Parse engine outputs using a progressive fallback approach:

### Stage 1: YAML Block Extraction

Extract content from ` ```yaml ... ``` ` fenced code blocks in the engine output.

### Stage 2: Key Validation

Required keys (parse fails without these):
- `position` (required)
- `confidence` (required)
- `rationale` (required)

Optional keys:
- `key_evidence`
- `risks`
- `conditions`
- `dissent_note`

### Stage 3: Value Validation

| Field | Valid Values | Default |
|-------|------------|---------|
| `position` | APPROVE, REJECT, ABSTAIN | ABSTAIN |
| `confidence` | Integer 0-100 | 0 |
| `rationale` | Non-empty string | "No rationale provided" |

### Stage 4: Fallback Text Analysis

If YAML parsing fails, scan the full output text for:

| Keyword Pattern | Inferred Position |
|----------------|-------------------|
| "approve", "recommend", "proceed", "yes" | APPROVE |
| "reject", "against", "deny", "no" | REJECT |
| "abstain", "uncertain", "insufficient" | ABSTAIN |

Confidence is estimated from language strength:
- Strong language ("clearly", "strongly", "definitely") → 70
- Moderate language ("likely", "probably", "reasonable") → 50
- Weak language ("possibly", "might", "uncertain") → 30

### Stage 5: Complete Failure

If all parsing stages fail:
```yaml
position: ABSTAIN
confidence: 0
rationale: "Engine output could not be parsed"
```

---

## Engine Availability Modes

> **Base Engine Policy (2026-05)**: Default baseline = **Claude + Codex (2-Engine Mode)**. 3-engine mode adds agy as an optional third axis when AVAILABLE. See `_common/MULTI_ENGINE_RECIPE.md §Base Engine Policy`.

Engine Mode adapts based on available engines:

| Available Engines | Mode | Behavior |
|---|---|---|
| 3 (Claude + Codex + Antigravity) | **3-Engine Mode** | 3 engines deliberate independently — adds agy's 1M context / multimodal / Deep Think axis |
| 2 (Claude + Codex — DEFAULT BASELINE) | **2-Engine Mode** | 2 engines deliberate independently; consensus patterns: 2-0 / 1-1 / 0-2. NOT degraded — this is the recipe's normal operating state |
| 2 (Claude + agy, Codex unavailable) | **2-Engine Mode (variant)** | Same scoring as above but with agy in place of Codex; flag the substitution because Codex is the preferred second axis |
| 1 (Claude only) | **Auto-fallback** | Automatic switch to Simple Mode, notify user |

### 2-Engine Mode Details (default baseline)

When the recipe runs in 2-Engine Mode (Claude + Codex):
- Both engines deliberate independently
- Consensus patterns reduce to: 2-0 (unanimous), 1-1 (split), 0-2 (unanimous rejection)
- Weighted confidence is 2-engine average
- Split (1-1) always escalates to user
- agy absence is recorded as informational header line, NOT as a failure

### Auto-Fallback Notification

When falling back to Simple Mode, inform the user:

```
⚠ Engine Mode requested but external engines unavailable.
  Codex: [available/not found]
  Gemini: [available/not found]
→ Falling back to Simple Mode (Logos/Pathos/Sophia internal deliberation).
```

---

## Error Handling

| Error | Response |
|---|---|
| **Timeout** (engine does not respond within 60s) | Retry once → if retry fails, treat as ABSTAIN |
| **Parse failure** (output not parseable) | Apply fallback text analysis → if complete failure, ABSTAIN |
| **API/CLI error** (non-zero exit code) | Treat as ABSTAIN, record error in risk register |
| **Both external engines fail** | Fall back to Simple Mode with notification |

### Error Recording Format

```yaml
engine_error:
  engine: "[Codex | Gemini]"
  error_type: "[timeout | parse_failure | cli_error]"
  detail: "[Error message or description]"
  action_taken: "[ABSTAIN | retry_succeeded | fallback_to_simple]"
```

---

## Engine Mode Execution Flow

```
1. AVAILABILITY CHECK
   └─ Verify codex/Antigravity CLI availability
   └─ Determine mode (Full / 2-Engine / Auto-fallback)

2. CLAUDE ANALYSIS (FIRST — contamination prevention)
   └─ Claude completes integrated analysis
   └─ Output stored before external calls

3. EXTERNAL ENGINE CALLS (PARALLEL)
   └─ codex exec --full-auto "{prompt}"
   └─ agy -p "{prompt}" --dangerously-skip-permissions

4. OUTPUT PARSING
   └─ Parse each engine's YAML output
   └─ Apply fallback parsing if needed

5. VOTE ASSEMBLY
   └─ Combine 3 (or 2) engine positions
   └─ Calculate weighted confidence
   └─ Determine consensus pattern

6. SYNTHESIS & DELIVERY
   └─ Present Engine Mode MAGI display
   └─ Include risk register and next steps
```

---

## Cross-References

- `_common/MULTI_ENGINE_RECIPE.md` — canonical engine binaries, PREFLIGHT probe, FAN-OUT contract, silent-failure detection
- `magi/reference/tri-engine-deliberate.md` — sibling Pattern H spec for the `multi` Recipe (each engine emits 3 viewpoints → 9-cell matrix); use that file instead when running tri-engine 9-cell deliberation
- `magi/reference/deliberation-framework.md` — perspective heuristics applied to Claude's integrated analysis
- `magi/reference/voting-mechanics.md` — vote aggregation and confidence calibration for the 3/2/1-engine consensus patterns

