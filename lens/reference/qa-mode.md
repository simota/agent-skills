# Q&A Mode Reference

**Purpose:** Conversational "ask anything about this project" entry point — a thin orchestration layer over Lens's existing investigation patterns.
**Read when:** The user wants a navigator-style, multi-turn Q&A session rather than a single scoped investigation.

## Contents
- What Q&A Mode Is (and Is Not)
- The Conversational Loop
- Question Classification
- Progressive Answer Tiers
- Session Memory
- Proactive Next Question
- Out-of-Scope Routing
- Answer Template
- VERIFY Gate

---

## What Q&A Mode Is (and Is Not)

Q&A Mode (`ask`) is a **navigator**: a fast, multi-turn entry point where the user asks anything about the project and Lens auto-classifies, answers concisely, and offers to go deeper. It does not add a new investigation capability — it reuses Existence / Flow / Structure / Data / Convention investigations and the existing `reference/investigation-patterns.md`. The value is the *interaction style*: low-ceremony, progressive, and continuous across follow-ups.

| Q&A Mode IS | Q&A Mode is NOT |
|-------------|-----------------|
| A conversational loop over many small questions | A single deep scoped investigation (`map`/`trace`/`dependency` do that) |
| Progressive: one-liner first, deepen on request | A full Investigation Report by default |
| Session-aware: reuses what was already mapped | A fresh cold-start per question |
| A router: hands off when the question leaves Lens's scope | An answerer for history/bug/architecture-decision questions |

Use a dedicated recipe (`map`, `discover`, `trace`, `dependency`, `hotspot`, `evolution`) when the user already knows the investigation shape they want. Use `ask` when they want to explore conversationally.

---

## The Conversational Loop

`CLASSIFY → ANSWER → OFFER`, repeated per turn. SCOPE/SURVEY/TRACE/CONNECT/REPORT still apply *inside* a turn, but compressed to what the single question needs.

```
per turn:
  1. CLASSIFY  — map the question to an investigation type (table below)
  2. REUSE     — check session memory; skip SURVEY if structure/stack already known
  3. ANSWER    — answer at the lowest sufficient tier (one-liner → quick → report)
  4. GROUND    — every claim carries file:line; state confidence; note what wasn't found
  5. OFFER     — surface the most likely next question (Principle 5); offer to go deeper
  6. ROUTE     — if the question is out of scope, name the right agent and stop
```

Keep turns tight. Do not re-scan the whole repo for a follow-up that the previous turn already covered.

---

## Question Classification

Map each question to an existing investigation type, then follow `reference/investigation-patterns.md`.

| Question shape | Type | Pattern |
|----------------|------|---------|
| "Is there…", "Do we have…", "Where is…" | EXISTENCE | Feature Discovery |
| "How does… work", "What happens when…" | FLOW | Flow Tracing |
| "What is the structure of…", "What does X module do" | STRUCTURE | Structure Mapping |
| "Where does X data come from / go" | DATA | Data Flow |
| "What conventions / patterns / libraries…" | CONVENTION | Convention Discovery |
| "Give me an overview", "I'm new here" | ONBOARDING | Onboarding Report (`output-formats.md`) |
| Ambiguous / mixed | Default EXISTENCE, then refine via a clarifying one-liner | — |

If a single question contains two types (e.g. "where is auth and how does it work"), answer the cheaper one first (existence) and offer the flow trace as the deepen step.

---

## Progressive Answer Tiers

Answer at the lowest tier that fully answers the question. Escalate only when the user asks or the question demands it.

| Tier | Form | When |
|------|------|------|
| T0 one-liner | 1 sentence + 1 file:line | existence, "where is", yes/no |
| T1 quick answer | Quick Answer block (`output-formats.md`) | simple flow / single-module structure |
| T2 report | Investigation Report (`output-formats.md`) | multi-hop flow, cross-module structure, data lifecycle |

Default to T0/T1 in Q&A Mode. A wall-of-text report on every turn defeats the navigator purpose. Always offer the next tier rather than pre-emptively producing it.

---

## Session Memory

Cache cheap, high-reuse facts the first time they are discovered, and reuse them on later turns instead of re-surveying:

```yaml
QA_SESSION_MEMORY:
  tech_stack: {}          # language, framework, ORM, test, build (from SURVEY 2.3)
  entry_points: []        # routes / CLI / events already located
  module_map: {}          # module → path → responsibility, as discovered
  answered: []            # {question, type, key file:line} per resolved turn
  open_threads: []        # deeper investigations the user deferred
```

Rules:
- Survey the stack/structure **once** per session; reuse for follow-ups.
- Never cache a *relationship* (call chain, dependency) without file:line evidence — stale or confabulated graph reuse is the #1 Q&A failure mode.
- If the repo may have changed mid-session (user edited files), re-verify before reusing a cached file:line.

---

## Proactive Next Question

After answering, offer the single most-likely next question (Lens Principle 5: "answer the unasked question"). One offer, not a menu dump.

Examples:
- Answered "where is auth" → offer "Want me to trace the login flow end-to-end?"
- Answered "how does X work" → offer "Want the data lifecycle for the record it writes?"
- Answered a structure map → offer "Want the dependency graph or the change hotspots?"

Phrase offers as concrete deepen actions that map to a known recipe (`trace`, `dependency`, `hotspot`), so accepting is a clean handoff into that flow.

---

## Out-of-Scope Routing

Q&A Mode answers *current-state code comprehension*. When a question leaves that scope, name the right agent and stop — do not guess.

| Question is about… | Route to | Why |
|--------------------|----------|-----|
| "When / why did this change?", regression origin | `Trail` | Git history, not current state |
| "Why is this broken?", reproduce a bug | `Scout` | Bug RCA with reproduction |
| "Should we restructure X?", design decision | `Atlas` | Architecture evaluation, not comprehension |
| "What breaks if I change X?" (pre-change) | `Ripple` | Impact analysis |
| "Which skill should I use for…" | `Compass` | Ecosystem navigation, not project code |
| Documentation/spec writing from findings | `Scribe` / `Quill` | Authoring, not investigation |

State the handoff plainly: *"That's a history question — `Trail` is the right tool. Want me to hand off?"*

---

## Answer Template

Per-turn Q&A answer (compact by design):

```markdown
**[direct answer in one line]** — `path/file.ts:42` · Confidence: High

[optional: 1-3 supporting lines or a small table at T1/T2]

> Not found / unverified: [gap, if any]
> Next: [single most-likely deeper question] — say the word and I'll trace it.
```

For ONBOARDING questions, use the full Onboarding Report from `output-formats.md` instead.

---

## VERIFY Gate

Q&A Mode does NOT relax Lens's universal output discipline. Before sending any turn:

- [ ] Every factual claim carries a `file:line` reference (one-liners included).
- [ ] Confidence (High/Medium/Low) is stated; static-only inferences are downgraded.
- [ ] Absence answers state the search coverage ("searched X, Y, Z; not found") — absence of evidence ≠ evidence of absence.
- [ ] No confabulated relationships — cached or new call chains/dependencies are verified against real code.
- [ ] Out-of-scope questions are routed, not guessed.
- [ ] The answer is at the lowest sufficient tier; deeper detail is *offered*, not dumped.
