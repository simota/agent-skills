# Nexus Output Formats Reference

**Purpose:** Canonical final output and handoff templates.
**Read when:** You need exact `NEXUS_COMPLETE`, handoff, or report formatting.

## Contents
- Envelope Sizing (read first)
- NEXUS_COMPLETE (AUTORUN)
- Work Gate Matrix
- Compact Form (SIMPLE runs)
- NEXUS_COMPLETE_FULL (AUTORUN_FULL)
- NEXUS_HANDOFF_V2 (Standard - Required)
- NEXUS_HANDOFF (Legacy - Deprecated)
- NEXUS_HANDOFF (Extended - AUTORUN_FULL)
- _STEP_COMPLETE Format

Final output formats and handoff protocols.

---

## Envelope Sizing

The templates below are the **largest** form of each envelope, not a per-run floor (`_common/OUTPUT_STYLE.md` § Conditional Requirements). Pick the form the run actually filled.

| Run shape | Form |
|-----------|------|
| SIMPLE — one agent, one step, no branches, no guardrail events | **Compact Form** below |
| MEDIUM — 2–3 steps, sequential | `NEXUS_COMPLETE`, empty ledgers collapsed to one line |
| COMPLEX — 4+ steps, parallel branches, or any guardrail event | `NEXUS_COMPLETE_FULL` |

Collapse rules, binding on every form:

- **A ledger with no entries is one line**, not a header plus a column-header-only table: `Decisions: none` · `Residuals: none` · `Guardrail events: none`.
- **Acceptance Provenance stays a table** whenever there is ≥1 criterion — this is the one ledger that must not collapse, because a criterion silently absent is the defect it exists to catch. With a single criterion, one row is the whole table.
- **`### Changes` lists files, not narration.** One line per file; no restatement of what the diff shows.
- **Never emit `N/A`, "none identified", or placeholder rows** to satisfy a template.
- **The completion sweep line is never dropped**, in any form, including Compact. It carries two counts: residue found, and files written / files evidenced. While the second pair differs the status is not `SUCCESS` — a file in neither the evidence nor the Residual Ledger is an unverified change with nothing declaring it so (`_common/OPERATIONAL.md` § Completion Contract).

---

## NEXUS_COMPLETE (AUTORUN)

```
## NEXUS_COMPLETE
Task: [Task name]
Type: [BUG|FEATURE|REFACTOR|...]
Chain: [Executed chain]
Fallback: [fallback_taken: compass-invoked | architect-invoked | neither — reason: <reason>] (only when the LADDER step ran; omit line otherwise)

### Changes
- [File1]: [Change description]
- [File2]: [Change description]

### Verification
- Tests: [PASS/FAIL + details]
- Build: [status]

### Acceptance Provenance
| Criterion | Class | Evidence / gap |
|-----------|-------|----------------|
| [AC or derived criterion] | verified \| partial \| missed \| dropped(DEC-n) | [observed evidence, or the precise gap] |
| [prohibited outcome] | held \| violated \| unverified | [evidence it did not occur, or why unobservable] |

### Decision Ledger
- [DEC-n (class)]: [decision] — [why] ([interpretation entries first; omit section if empty])

### How to Verify
1. [Verification step 1]
2. [Verification step 2]

### Risks / Residual Ledger
- [Remaining risks + any UNVERIFIED claims]

| ID | Residual | Class | Blocker / owner | Marker location | Route |
|----|----------|-------|-----------------|-----------------|-------|
| RES-n | [what is not done] | blocked-external \| gate-pending \| out-of-contract \| budget-exhausted \| user-declined | [named blocker] | [file:line `#TODO(agent):`, or `none`] | [recipe/agent that finishes it] |

Completion sweep: [command run] — [N hits: each mapped to a RES-n, or `pre-existing`]; [X] changed / [Y] evidenced (`scanned, 0 hits; 7 changed / 7 evidenced` when clean)
```

Acceptance Provenance covers **every** intent-contract criterion (none silent) **and every prohibited outcome on its own axis** — a prohibition is `held` only with evidence that the forbidden result did not occur; `unverified` is honest, `held` by assumption is not, and `violated` caps the run at `FAILED`. Decision Ledger and evidence rules per `reference/autonomy-quality-protocol.md` (Q2, Q4–Q6, Q10, Q15).

The **Residual Ledger** replaces free-text "Recommended follow-ups": every leftover carries a Q17 class, and an untyped residual is a defect that caps status at `PARTIAL` (Q16–Q19). Rows and in-artifact `#TODO(agent):` markers bind bidirectionally — no orphan markers, no orphan rows. Omit the table only when the sweep is clean, and keep the sweep line either way.


---

## Work Gate Matrix

Every spoke emits `WORK_GATE` (`_common/WORK_GATE.md`). Nexus renders them as a matrix — skills
down, axes across — and **never as a rollup**. No row total, no column average, no "overall ★".
The reader's question is *which skill, which axis*, and any aggregate erases exactly that.

```
### Work Gate

| Skill   | IN    | FIT   | EVD   | OUT   | RSK  | CLR   |
|---------|-------|-------|-------|-------|------|-------|
| scout   | ★★☆☆☆ | ★★★★★ | ★★★★☆ | ★★★☆☆ | pass | ★★★★★ |
| builder | ★★★★☆ | ★★★★★ | ★★★☆☆ | ★★★☆☆ | pass | ★★★★☆ |
| radar   | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★☆ | pass | ★★★★☆ |

- scout / IN ★★ — repro steps absent from the report; reproduced from the stack trace alone
- builder / EVD ★★★ — the latency claim is labelled UNVERIFIED
```

Rules:

- Every cell at ★★★☆☆ or below gets one line under the table naming the reason. A low cell with
  no line is an incomplete report.
- `n/a` cells render `n/a`, never blank, never as ★1, never merged into ★5.
- **Any `RSK: risk` blocks `NEXUS_COMPLETE`** and is reported at the top of the envelope, not as
  a cell the reader has to find. `RSK` is never starred.
- A spoke that emitted no gate renders as a `—` row with "no gate emitted". Silence is a finding
  about the spoke, not an empty cell.
- Skip-tier spokes contribute only the axes they emitted; the rest render `·` (not asserted at
  this tier) rather than stars.
- **`IN` is read as a column, not per row.** A chain where `IN` degrades from ★★★★☆ at the head
  to ★★☆☆☆ three spokes down is a handoff defect, and it is invisible in any single spoke's gate.
- **Rework is never invisible.** A spoke that was sent back under `_common/HANDOFF.md` § Handoff
  Admission Gate is marked `↺` beside its name, with the refusing skill and the named missing item
  on a line below the table. Nexus is the arbiter of the one-bounce-per-edge rule; a chain that
  silently reran a step reports a smaller cost than it paid.
- **A second failure on the same condition is a blocker, not a third attempt** — it surfaces at
  the top of the envelope as a typed residual plus the question for the user.

---

## Compact Form (SIMPLE runs)

```
## NEXUS_COMPLETE
Task: [Task name] · Type: [TYPE] · Chain: [Agent]

### Changes
- [file]: [change]

### Verification
- [Tests / build / check]: [result, or `UNVERIFIED — <why>`]

### Acceptance
| Criterion | Class | Evidence / gap |
|-----------|-------|----------------|
| [AC] | verified \| partial \| missed | [evidence] |

Decisions: none | Residuals: none
Completion sweep: [command] — scanned, 0 hits; 1 changed / 1 evidenced
```

Escalate out of Compact the moment any of these is true: a `DEC-n` was taken, a residual exists, a guardrail fired, a criterion is `partial`/`missed`, or a prohibited outcome is `unverified`. Those are the cases the long form exists for — everything else is scaffolding.

---

## NEXUS_COMPLETE_FULL (AUTORUN_FULL)

```
## NEXUS_COMPLETE_FULL
Task: [Task name]
Type: [BUG|FEATURE|REFACTOR|...]
Mode: AUTORUN_FULL
Complexity: [SIMPLE|MEDIUM|COMPLEX]

### Execution Summary
- Total Steps: [N]
- Parallel Branches: [N branches if any]
- Duration: [Phases completed]
- Recovery Actions: [N if any]

### Chain Executed
Sequential: [Agent1] → [Agent2] → [Agent3]
Parallel (if any):
  Branch A: [Agent4] → [Agent5]
  Branch B: [Agent6] → [Agent7]
  Merge: [Agent8]

### Changes
- [File1]: [Change description]

### Guardrail Events
| Step | Level | Trigger | Action | Result |
|------|-------|---------|--------|--------|
| 3/7 | L2 | test_failure | auto_fix | SUCCESS |

### Verification
- Tests: [PASS/FAIL + details]
- Build: [status]
- Security: [Sentinel result if applicable]
- Final Guardrail: [L2 CHECKPOINT result]

### Context Summary
- Goal: [Original goal + non-goals from the intent contract]
- Acceptance: [per-criterion — see Acceptance Provenance table; never a blanket "all criteria met"]
- Key Decisions: [Decision Ledger — DEC-n entries, interpretation class first]

### Acceptance Provenance
| Criterion | Class | Evidence / gap |
|-----------|-------|----------------|
| [AC or derived criterion] | verified \| partial \| missed \| dropped(DEC-n) | [observed evidence, or the precise gap] |
| [prohibited outcome] | held \| violated \| unverified | [evidence it did not occur, or why unobservable] |

### How to Verify
1. [Verification step 1]
2. [Verification step 2]

### Risks / Residual Ledger
- [Remaining risks + any UNVERIFIED claims]

| ID | Residual | Class | Blocker / owner | Marker location | Route |
|----|----------|-------|-----------------|-----------------|-------|
| RES-n | [what is not done] | blocked-external \| gate-pending \| out-of-contract \| budget-exhausted \| user-declined | [named blocker] | [file:line `#TODO(agent):`, or `none`] | [recipe/agent that finishes it] |

Completion sweep: [command run] — [N hits: each mapped to a RES-n, or `pre-existing`]; [X] changed / [Y] evidenced (`scanned, 0 hits; 7 changed / 7 evidenced` when clean)

### Rollback (if needed)
- Rollback available: [Yes/No]
- Command: [git checkout / restore command]
```

---

## NEXUS_HANDOFF_V2 (Standard - Required)

All agents MUST use V2 format with confidence scoring.

**Compliance Levels:** Level 1 (Minimal) requires only `step`, `agent`, `status`, `summary`, `next_agent`, `next_action` — confidence is inferred from status (see `handoff-validation.md` Compliance Levels). Level 2 adds `confidence` as a single number. Level 3 (Full/Claude default) adds `confidence_breakdown` with 3 axes.

```yaml
## NEXUS_HANDOFF
step: [X/Y]
agent: [AgentName]
status: [SUCCESS|PARTIAL|BLOCKED|FAILED]

# REQUIRED: Confidence scoring for auto-routing
confidence: 0.XX  # Overall score (0.0-1.0)
confidence_breakdown:
  task_completion: 0.XX   # How complete is the work
  output_quality: 0.XX    # Quality of artifacts produced
  next_step_clarity: 0.XX # How clear is the next step

summary: |
  [1-3 line summary of work completed]

key_findings:
  - [Finding 1]
  - [Finding 2]

artifacts:
  - type: [file|command|link]
    path: [path]
    description: [what it is]

risks:
  - [Risk 1]
  - [Risk 2]

open_questions:
  - blocking: [true|false]
    question: [Question]

pending_confirmations:  # Only if status == BLOCKED
  - trigger: [INTERACTION_TRIGGER]
    question: [Question]
    options: [List]
    recommended: [Option]

user_confirmations:
  - question: [Previous Q]
    answer: [User's A]

next_agent: [AgentName|DONE]
next_action: [CONTINUE|MERGE|VERIFY|ESCALATE|ABORT]
reason: [Why this next step]
```

### Auto-Routing Rules

| Confidence | Status | Action |
|------------|--------|--------|
| >= 0.75 | SUCCESS | Auto-route to next_agent |
| 0.50-0.74 | SUCCESS/PARTIAL | Route with logged assumptions |
| < 0.50 | any | Pause for user input |
| any | BLOCKED | Present pending_confirmations |
| any | FAILED | Execute recovery chain or escalate |

See `reference/handoff-validation.md` for full validation rules.

---

## NEXUS_HANDOFF (Legacy - Deprecated)

```
## NEXUS_HANDOFF
- Step: [X/Y]
- Agent: [AgentName]
- Summary: 1-3 lines
- Key findings / decisions:
  - ...
- Artifacts (files/commands/links):
  - ...
- Risks / trade-offs:
  - ...
- Open questions (blocking/non-blocking):
  - ...
- Pending Confirmations:
  - Trigger: [INTERACTION_TRIGGER name]
  - Question: [Question]
  - Options: [Available options]
  - Recommended: [Recommended option]
- User Confirmations:
  - Q: [Previous question] → A: [User's answer]
- Suggested next agent: [AgentName] (reason)
- Next action: CONTINUE
```

**Note**: Legacy format will be auto-migrated to V2 with inferred confidence.
See `handoff-validation.md` for migration rules.

---

## NEXUS_HANDOFF (Extended - AUTORUN_FULL)

```
## NEXUS_HANDOFF
- Step: [X/Y]
- Branch: [branch_id or "main"]
- Agent: [AgentName]
- Summary: 1-3 lines
- Key findings / decisions:
  - ...
- Artifacts (files/commands/links):
  - ...
- Files Modified: [List of files]
- Risks / trade-offs:
  - ...
- Guardrail Events:
  - Level: [L1|L2|L3|L4 or "none"]
  - Trigger: [What triggered if any]
  - Action: [Action taken]
  - Result: [SUCCESS|FAILED|ESCALATED]
- Context Delta:
  - Added: [New knowledge/artifacts]
  - Changed: [Modified state]
- Suggested next agent: [AgentName]
- Next action: [CONTINUE|MERGE|VERIFY|ESCALATE|ABORT]
```

---

## _STEP_COMPLETE Format

```
_STEP_COMPLETE:
  Agent: [Name]
  Branch: [branch_id if parallel, else "main"]
  Status: SUCCESS | PARTIAL | BLOCKED | FAILED
  Output:
    type: [Output type]
    summary: [Brief summary]
    files_changed: [List if applicable]
  Handoff:
    Format: [AGENT_TO_AGENT_HANDOFF format]
    Content: [Full handoff for next agent]
  Artifacts:
    - [List of produced artifacts]
  Next: [NextAgent] | VERIFY | DONE
  Reason: [Why this next step]
```


## Handoff Directions (SKILL.md excerpt)

| Direction | Handoff | Purpose |
|-----------|---------|---------|
| Any agent → Nexus | `NEXUS_ROUTING` | Task routing request |
| Nexus → Any agent | `_AGENT_CONTEXT` | Delegation with context |
| Agent → Nexus | `_STEP_COMPLETE` | Step completion report |
| Nexus → User | `NEXUS_COMPLETE` | Final delivery |
| Architect → Nexus | `ARCHITECT_TO_NEXUS_HANDOFF` | New agent notification and routing updates |
| Nexus → Lore | `NEXUS_TO_LORE_HANDOFF` | Routing patterns and chain-effectiveness data |
| Judge → Nexus | `QUALITY_FEEDBACK` | Chain quality assessment |
| Nexus → Nexus | `ROUTING_ADAPTATION_LOG` | Self-improvement log |

External feedback sources: Nexus[deliver] (epic-chain results), Judge (quality), Architect (new agents), Lore (validated routing knowledge), Darwin (ecosystem evolution signals).



## NEXUS_COMPLETE Required Elements (SKILL.md excerpt)

- `## NEXUS_COMPLETE` header (canonical template: `reference/output-formats.md`)
- Task description and acceptance criteria
- Chain selected and mode used
- Per-step results with agent, status, and output summary
- Verification results (tests, build, security) — evidence-bound; unexercised paths labeled `UNVERIFIED` (Q10)
- **Acceptance Provenance** — every intent-contract criterion classified `verified`/`partial`/`missed`/`dropped(DEC-n)`, none silent (Q15)
- **Decision Ledger** — `DEC-n` judgment calls made without the user, interpretation entries first; omit only when empty (Q4-Q6)
- `## Prompt Tuning` trace when any spawn's directives were adapted (`field, old→new, trigger, reward_basis`), delta-only — omit entirely when no spawn was tuned
- Summary with overall status
- **Residual Ledger** — each leftover as `RES-n` (class, blocker/owner, marker location, route), bound bidirectionally to any `#TODO(agent):` left behind, plus the completion-sweep line, which carries **two** counts — residue and coverage (`scanned, 0 hits; 7 changed / 7 evidenced`), never omitted

