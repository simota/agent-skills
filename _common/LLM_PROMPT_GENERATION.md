# LLM Instruction Prompt Generation (Common Pattern)

**Purpose:** Universal authoring rules and prompt structure shared by every agent that pairs its report with a paste-ready LLM instruction prompt for a downstream coding LLM (Builder, Claude, Codex, Forge, Artisan, Native).
**Read when:** You are designing or maintaining a per-agent `fix-prompt-generation.md` (or similar) and want the universal rules in one place.

## Contents

- Pattern intent
- Adopting agents
- Universal authoring rules
- Universal prompt structure
- Universal suppression principle
- What stays in each agent's reference
- Cross-agent consistency

---

## Pattern Intent

Investigation, audit, analysis, and specification agents typically produce structured findings that another LLM must reformulate into an action prompt before fixing/implementing. Pairing each finding with a paste-ready prompt eliminates this reformulation step:

- single block embeds the agent's full diagnostic
- explicit acceptance criteria so the receiving LLM knows when to stop
- explicit "what NOT to do" so the receiving LLM does not silence the symptom or expand scope
- explicit ruled-out hypotheses / alternatives so the receiving LLM does not re-litigate dead ends
- explicit confidence so the receiving LLM calibrates trust

Without this pattern, the user manually copies file paths, evidence, and constraints between sessions — high friction, easy to lose context.

---

## Adopting Agents

| Agent | Prompt scope | Default verb family |
|-------|--------------|---------------------|
| `echo[demand]` | User demand → next agent | `PROPOSE`, `DESIGN`, `DRAFT-SPEC`, `PROTOTYPE`, `REFINE`, `ANALYZE` |
| `scout` | Bug fix | `FIX`, `FIX-WITH-TEST`, `MITIGATE`, `INVESTIGATE-FURTHER`, `REFACTOR-FIX` |
| `trail` | Regression remediation | `FIX-REGRESSION`, `REVERT`, `REVERT-WITH-FORWARD-FIX`, `INVESTIGATE-FURTHER`, `REFACTOR-FIX` |
| `sentinel` | Security remediation (when handed off, not when shipped inline) | `SECURE-FIX`, `HARDEN`, `MITIGATE`, `BREAKING-FIX`, `AUTH-FIX`, `REVOKE-AND-ROTATE`, `INVESTIGATE-FURTHER` |
| `siege` (`concurrency` recipe) | Concurrency / memory / resource remediation | `RACE-FIX`, `LEAK-FIX`, `LOCK-FIX`, `RESOURCE-FIX`, `MITIGATE`, `INVESTIGATE-FURTHER`, `REFACTOR-FIX` |
| `probe` | DAST / runtime exploit remediation | `EXPLOIT-FIX`, `HARDEN-RUNTIME`, `MITIGATE`, `BREAKING-FIX`, `AUTH-FIX`, `INVESTIGATE-FURTHER` |
| `judge` | Tri-engine code review consensus finding | `APPLY-FIX`, `REWRITE`, `REVERT-AND-RESTART`, `BREAKING-FIX`, `INVESTIGATE-FURTHER`, `DOWNGRADE` |
| `canon` | Standards compliance gap remediation | `REMEDIATE`, `EXEMPT-WITH-RATIONALE`, `BREAKING-REMEDIATE`, `MITIGATE`, `INVESTIGATE-FURTHER` |
| `attest` | Spec compliance AC gap closure | `CLOSE-GAP`, `RECONCILE-SPEC`, `BREAKING-CLOSE`, `INVESTIGATE-FURTHER`, `WAIVE` |
| `omen` | Pre-mortem failure mode mitigation | `ADD-GUARDRAIL`, `ADD-MONITOR`, `ADD-RUNBOOK`, `MITIGATE`, `INVESTIGATE-FURTHER`, `ACCEPT-RISK` |
| `tuner` | DB query plan / index remediation | `OPTIMIZE-QUERY`, `ADD-INDEX`, `BREAKING-OPTIMIZE`, `MIGRATE-WORKLOAD`, `INVESTIGATE-FURTHER`, `MITIGATE` |

Future candidates: `trail static-rules` (legacy migration prompt), and any new investigation/audit agent that hands findings off to a coding agent.

---

## Universal Authoring Rules

These apply to every agent's prompt block. Domain-specific elaboration belongs in the agent's own `fix-prompt-generation.md`.

1. **Quote evidence verbatim** — paste the exact error message, log line, stack frame, query plan, scanner finding, or commit SHA. Do not paraphrase. The receiving LLM may search for these strings.
2. **Cite file paths with line numbers** in the form `src/path/to/file.ts:123` so the receiving LLM can `Read` directly.
3. **Embed acceptance criteria as a checklist** (`- [ ]`). At minimum: original symptom no longer occurs, regression test added, no new test failures.
4. **Embed ruled-out alternatives** (or equivalent: ruled-out hypotheses, considered-and-rejected fixes) with the evidence that eliminated each. Saves the receiving LLM from re-investigating dead ends.
5. **Embed "what NOT to do"** — at minimum: do not silence the symptom (catch-and-ignore, swallow logs, suppress the error), do not expand scope beyond cited files unless evidence demands it.
6. **State confidence at the top** so the receiving LLM calibrates trust. Use the unified scale from `_common/INVESTIGATION_ESCALATION.md` when the agent participates in the investigation cluster (HIGH ≥0.8, MEDIUM 0.5–0.79, LOW <0.5).
7. **Wrap the prompt in a fenced code block** (```` ```text ````) so the user can copy it cleanly without markdown rendering artifacts.
8. **Self-contained** — the prompt must work without the rest of the agent's report. Assume the receiving LLM sees only the prompt.
9. **One verb, one finding** — do not bundle multiple findings into one prompt. Multi-finding handoffs require multiple prompts (or an orchestration prompt at the report level, demand-simulation-style).
10. **Declare the action verb at the top of `# Your task`** — exactly one verb per prompt. The verb tells the receiving LLM what shape of output to produce.

---

## Universal Prompt Structure

Every per-finding prompt follows this skeleton. Agents add domain-specific blocks (e.g., Scout adds Reproduction; Sentinel adds OWASP/CWE; Trail adds Timeline).

```text
# Your task
<VERB> the [bug | regression | vulnerability | spec gap | …] described below.

# Context
- [domain-specific identification — title, severity, confidence, etc.]
- [classification fields — OWASP, CWE, reproducibility, etc.]

# [Diagnostic block — domain-specific name]
[Cause / vulnerability / regression description with evidence]
Location: <file>:<line> in <function>

# [Reproduction / Trigger / Exploit block — when applicable]
[Steps to observe the issue, exact strings to search for]

# Recommended action
Approach: [strategy]
Files to modify: [list with expected change]
Constraints:
- [coupling, side effect, or backward-compat note]

# Acceptance criteria
- [ ] [domain-specific verifiable outcome 1]
- [ ] [verifiable outcome 2]
- [ ] No new test failures in the affected module

# Ruled-out alternatives (do not revisit)
- [alternative 1] — eliminated because [evidence]
- [alternative 2] — eliminated because [evidence]

# What NOT to do
- Do not silence the symptom (catch-and-ignore, swallow logs, suppress the error)
- Do not expand scope beyond the cited files unless evidence demands it
- [domain-specific anti-action]
```

Verb modifiers (apply per agent):
- `INVESTIGATE-FURTHER` family → replace "Recommended action" with "Verification plan" (steps to confirm or refute the hypothesis before changing code).
- `MITIGATE` family → add "Underlying status" line stating why the underlying cause is not being addressed in this pass.
- `REFACTOR-FIX` family → add "Structural concern" section explaining why a one-line patch is insufficient.
- `BREAKING-FIX` / `AUTH-FIX` family (Sentinel) → add "User-facing impact" and "Rollback plan" sections.

---

## Universal Suppression Principle

Do not emit a Fix/Action Prompt when:

| Case | Reason | Note in report |
|------|--------|----------------|
| Escalation to a more specialized agent | The receiving agent owns the remediation prompt | "Prompt suppressed — [Agent] owns remediation prompt." |
| Investigation-only or audit-only scope | Out of scope for this engagement | "Prompt withheld per scope: [scope]." |
| Evidence too weak even for `INVESTIGATE-FURTHER` | A prompt would mislead | "Insufficient evidence for prompt; reopen after [missing data]." |
| Classified `WONTFIX` or works-as-designed | Not actionable | "Prompt withheld — classified as [WONTFIX / WAD]." |
| Agent ships the fix inline (e.g., Sentinel ≤50 lines) | The fix is the artifact, not a prompt | "Prompt N/A — fix shipped inline (see changed files)." |

In all cases, write a one-line note in the report explaining why the prompt is withheld. Silent omission breaks downstream expectations.

---

## What Stays in Each Agent's Reference

The per-agent `fix-prompt-generation.md` (or equivalent) keeps:

- **Action verbs table** — domain-specific verbs with "when to use" and "receiving agent"
- **Verb selection heuristic** — confidence × scope × escalation flowchart
- **Domain-specific suppression cases** — beyond the universal list (e.g., Scout: when escalating to Sentinel)
- **Domain-specific template fields** — reproduction steps, OWASP/CWE, timeline, etc.
- **Worked example** — paste-ready prompt for a representative finding in the agent's domain

The per-agent reference should explicitly link back to this file:

```markdown
> Universal authoring rules and prompt structure: `_common/LLM_PROMPT_GENERATION.md`.
> This file documents only [agent]-specific verbs, suppression cases, template fields, and an example.
```

---

## Cross-Agent Consistency

Agents that share downstream consumers (e.g., Scout / Trail / Sentinel all hand off to Builder) should keep verb naming consistent where the action is the same:

- `INVESTIGATE-FURTHER` is universal — same meaning across agents
- `MITIGATE` is universal — workaround/symptom-only fix
- `REFACTOR-FIX` is universal — structural change required
- Domain-specific verbs vary (`FIX` for Scout vs `FIX-REGRESSION` for Trail vs `SECURE-FIX` for Sentinel) and that variance is intentional — it cues the receiving LLM to apply domain-appropriate care.

When adding a new adopting agent, register its verb family in the table above and audit naming overlap with existing agents.
