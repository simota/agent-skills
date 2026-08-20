# SPECIFY Phase — Hardening the Instruction Before It Is Delegated

**Purpose:** The gated `SPECIFY` step between `CHAIN_SELECT` and `EXECUTE`: run `Chisel brief` over the intent contract so every downstream `_AGENT_CONTEXT` carries executable acceptance criteria instead of vague wording — and so what each specialist is free to decide stays explicitly free.
**Read when:** Deciding whether `SPECIFY` fires, composing the Specified Brief, or injecting it into spawn prompts.

## Contents
- Why this phase exists
- What it is not
- The gate
- The Specified Brief
- Injection rule
- Delegation discipline (the AS-09 defense)
- Cost and chain-size interaction
- Anti-patterns
- Handoffs

---

## Why This Phase Exists

`CLASSIFY` already crystallizes the **intent contract** (goal + ACs + non-goals + prohibited outcomes). What it does not do is guarantee that contract is written in language a *different session* can execute and score. A brief that says "high-quality implementation, keep it clean, be thorough where it matters" survives CLASSIFY intact and then reaches four specialists who each resolve it differently — and the divergence surfaces at `AGGREGATE`, after the tokens are spent.

`SPECIFY` closes that gap at the one point where it is cheap: **once, before the first spawn**, on the artifact every spawn inherits.

Two existing layers sit next to this one and do not overlap it:

| Layer | Owns | Does not touch |
|-------|------|----------------|
| `adaptive-prompt-policy.md` | Per-spawn **directive fields** — envelope, effort, tool-use, thinking, which references | Task content; it explicitly never writes free-form prompt text |
| `_common/LLM_PROMPT_GENERATION.md` | The **shape** of a generated downstream prompt | Whether the criteria inside it are checkable |
| **`SPECIFY` (this file)** | The **content** of the instruction — goal, ACs, constraints, prohibited outcomes, what stays delegated | Directive fields; those stay with the adaptive policy |

---

## What It Is Not

- **Not a clarifying question.** `Chisel` translates; it never asks the user. If the goal itself admits two incompatible readings, `GATE` fires **first** and asks — `SPECIFY` runs on an intent contract that already passed the confidence floor. A sub-floor classification is never rescued by specifying it harder.
- **Not intent clarification.** The object is the **instruction Nexus is about to delegate**, not the user's raw request. Chisel absorbing the latter is the over-capture failure guarded by `task-battery.md` item 61.
- **Not a verification step.** `SPECIFY` produces; it does not check another agent's output. Producer ≠ verifier is unaffected.
- **Not recursive.** The Chisel spawn's own prompt is never itself passed through `SPECIFY`.

---

## The Gate

`SPECIFY` is an efficiency measure. Running it on work that does not need it violates Core Rule #1 and buys nothing.

**Fires when any of:**
- The intent contract contains **≥ 1 load-bearing ambiguity** — a term whose two readings would change the deliverable, sitting in a goal, AC, or constraint position (`chisel/reference/ambiguity-lexicon.md`). One vague adjective in a passing remark is not load-bearing.
- The chain has **≥ 3 spawns** — the brief is inherited enough times to amortize its cost.
- The Recipe is a **loop or quality-max** recipe (`converge`, `quell`, `burnish`, `whet`, `apex`, `summit`, `wish`, …) — the brief is re-read every cycle, so ambiguity compounds per iteration rather than once.
- A prior step returned a **goal-misalignment or rework signal** (`LT-07` near-miss, an `AGGREGATE` alignment failure). Here `SPECIFY` runs mid-chain, before the retry.

**Skipped when:**
- Single-spawn or trivial run — use the intent contract directly.
- The user supplied **explicit measurable acceptance criteria** already; there is nothing to translate.
- The request is a factual lookup or a meta-question (the LADDER carve-out shapes).
- The route is the `pack` Recipe, proactive no-args mode, or another inline no-spawn Recipe.

Record the outcome either way: `Specify: applied (trigger: <which>)` or `Specify: skipped (reason: <which>)`. A silent skip is indistinguishable from a bug.

---

## The Specified Brief

Chisel returns one artifact. It is internal — it is **not** the user-facing four-section deliverable.

```yaml
SPECIFIED_BRIEF:
  goal: "<one line, no term with two defensible readings>"
  acceptance_criteria:          # each a bound, an observable behavior, or a scorable criterion
    - "<AC-1>"
    - "<AC-2>"
  non_goals:                    # the scope boundary. MAY NOT BE EMPTY — see below
    - "<what this run will not do, though a reader might expect it>"
  falsifier: "<the observation that would prove the delivered result wrong>"
  prohibited_outcomes:          # Q2/Q23 axis — kept separate from ACs on purpose
    - "<what must not happen>"
  constraints:
    - rule: "<constraint>"
      precedence: "<which constraint it yields to, when they collide>"
  delegated:                    # the ambiguity budget — see below
    - decision: "<what stays open>"
      owner: "<which agent in the chain decides it>"
      reason: "executor-has-better-information | reversible | premature-formatting"
  unresolved_parameters:        # only those that materially change the output
    - name: "<PARAM>"
      assumption: "<the reading being proceeded on>"
      surfaces_as: "DEC-n"
```

Every reading Chisel chose where the source admitted more than one becomes a **`DEC-n` interpretation entry** in the existing Decision Ledger (`output-formats.md`). No new ledger is introduced.

### Three fields that gate execution

**`non_goals` may not be empty.** An empty boundary is not a wide scope — it is an unstated one, and it is
the single most common route by which a chain widens mid-run: nothing was excluded, so nothing was crossed.
Writing down what will *not* be done fixes the edge before the first spawn, and it is what `frozen-scope`
is measured against at `AGGREGATE`. `non_goals` is distinct from `prohibited_outcomes` and neither
substitutes for the other: a non-goal is work deliberately left undone, a prohibited outcome is a state the
work must not produce. Both travel verbatim.

**`falsifier` is what separates a brief from a wish list.** The acceptance criteria say what success
looks like; a falsifier says what would *defeat* the claim of success, and it must name an observation
somebody could actually make. "It would be wrong if the user disliked it" is not one — nothing about it
can be checked, and it will therefore never fire. "It would be wrong if the existing `/orders` response
changed shape for any current client" is one: it names a thing to look at.

The failure it catches is the one ACs cannot: **every criterion met and the result still wrong**, because
the criteria measured the work rather than the outcome. A falsifier is checked at `VERIFY` alongside the
ACs, and an unchecked one is reported `UNVERIFIED` like any other unexercised path. Where the honest answer
is that no observation would falsify the result, that is a finding about the brief — the goal is not yet
stated in terms anyone can be wrong about, and it goes back to the dialogue rather than forward to a spawn.

**`unresolved_parameters` is not a place to park an open question.** Each entry carries the assumption
being proceeded on, which is what makes it safe to start: the run has an answer and is recording that it
chose it. A parameter with no assumption is an open question, and an open question is settled before
execution or asked as the `Ask First` gate it is — never deferred to "decide while implementing", which is
the shared entrance to both rework and scope creep.

---

## Injection Rule

The brief is **chain-level, written once, inherited by all**:

- `goal`, `acceptance_criteria`, `non_goals`, `falsifier`, `prohibited_outcomes`, `constraints` are copied verbatim into every `_AGENT_CONTEXT` in the chain. Verbatim matters — paraphrasing per spawn re-introduces exactly the divergence this phase removes.
- `delegated` is filtered per recipient: each agent sees the decisions **it** owns, so it knows what it is expected to decide rather than ask about.
- `unresolved_parameters` go to every spawn, with the stated assumption. A specialist that discovers the assumption is wrong reports it rather than silently working around it.
- Per-spawn directive fields (envelope, effort, references) are still assembled by `adaptive-prompt-policy.md` afterwards. Brief first, directives second; they never overwrite each other because they occupy different fields.

---

## Delegation Discipline (the AS-09 Defense)

The failure mode of this phase is **over-specification**: a brief so complete that four specialists become four transcription clerks, capped at the hub's first idea. That is `AS-09 Over-Specified Process` (`architect/reference/agent-specification-anti-patterns.md`), and it is the reason `delegated` is a required field rather than an optional one.

A brief with an **empty `delegated` list on a multi-agent chain is a defect**, not a thorough job. If the hub genuinely decided everything, the specialists were not needed and the chain should have been shorter.

Concretely, leave delegated: approach selection on an unsolved problem, naming, section and file ordering, decomposition shape, and any reversible choice the specialist will make with material the hub cannot see. Fix only what carries correctness, safety, auditability, or the user's stated requirement.

---

## Cost and Chain-Size Interaction

`SPECIFY` costs **one additional spawn per chain** (not per step). On a 3-spawn chain that is ~33% more agents for a brief inherited three times; on a loop recipe it is amortized across every cycle.

**Ordering vs `Ask First` — `SPECIFY` runs last.** When any `Ask First` gate applies to the chain (10+ files, L4, destructive, 5+ agents, …), **every such gate resolves before `SPECIFY` runs**. Two reasons, and the second is the load-bearing one:
1. Hardening a brief for work the user may cancel spends a spawn on nothing.
2. **The user's answer routinely changes the scope the brief was written against** — "all 123 files or a subset?", "auto-apply or report back first?" — and a brief written before that answer is not merely stale, it is confidently wrong in the specific way this phase exists to prevent. Re-running Chisel afterwards means the first pass was pure waste.

A gate whose answer cannot change scope (a pure go/no-go) may be resolved in either order; when in doubt, ask first and specify second.

**Chain-size collision:** the Chisel step **counts** toward the `Ask First` threshold for 5+ agent chains — it is a real spawn and hiding it would make the threshold a fiction. But when the gate would push a chain from 4 to 5 and thereby trigger a confirmation, **the gate yields and `SPECIFY` is skipped** (logged as `skipped (reason: would cross the 5-agent confirmation threshold)`). An efficiency measure must never become the reason to interrupt the user.

---

## Anti-Patterns

| Anti-pattern | Why it fails |
|--------------|--------------|
| Running `SPECIFY` on every chain unconditionally | Coordination tax on work that had no ambiguity; Core Rule #1 violation |
| Using it to skip `GATE` | Specifying a guessed intent produces a precise instruction to do the wrong thing |
| Running it before an unresolved `Ask First` gate | The answer usually changes scope, so the brief is written against the wrong target and must be redone |
| Per-spawn Chisel passes instead of one chain-level brief | N extra agents for an artifact that only needed writing once |
| Paraphrasing the brief per recipient | Reintroduces the divergence the phase exists to remove |
| Empty `delegated` on a multi-agent chain | Over-specification; the specialists are now clerks |
| Chiselling the Chisel spawn prompt | Infinite regress with no added information |
| Treating the brief as the user-facing deliverable | It is internal; the user gets `NEXUS_COMPLETE`, not a prompt-specification report |

---

## Handoffs

| Direction | Handoff | Payload |
|-----------|---------|---------|
| Nexus → Chisel | `NEXUS_TO_CHISEL_SPECIFY` | Intent contract, selected chain (agent list + role per agent), Recipe, mode |
| Chisel → Nexus | `CHISEL_TO_NEXUS_BRIEF` | `SPECIFIED_BRIEF` (schema above) + the reading chosen per resolved ambiguity, for `DEC-n` |

The Chisel spawn uses the standard Agent Spawn Template (`hub-authoring.md`) and inherits the same agy/codex silent-output mitigations as every other Nexus spawn.
