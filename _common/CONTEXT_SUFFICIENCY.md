# Context Sufficiency Gate (Common Definition)

A Context-Engineering-grounded protocol for deciding, **before acting**, whether the agent holds
enough context — and when it does not, asking a *systematic, targeted* question instead of a vague
"can you clarify?". Context Engineering means filling the working context with *just the right*
information; this gate operationalizes that as: inventory the context an outcome needs → retrieve
what's derivable → ask only for the irreducibly-missing, in one structured turn.

Pairs with: `_common/INTERACTION.md` (`QUESTION_FORMAT`, trigger registry — the `ON_MISSING_CONTEXT`
/ `ON_SCOPE_UNCLEAR` triggers point here), `nexus/reference/intent-clarification.md` (intent decoding,
"retrieve before ask"). This file owns **what dimensions to inventory and how to ask**; those own
when to interpret vs. proceed.

---

## 1. Context Dimensions Taxonomy

The kinds of context an outcome can depend on. Run the task's outcome against this list and mark
each dimension's state (§2). `Core` dimensions are almost always load-bearing; `Conditional` ones
matter only for the task types noted.

| Dim | Question it answers | Tier | Load-bearing for |
|-----|--------------------|------|------------------|
| `GOAL` | What outcome, and *why* (the intent behind the ask)? | Core | every task |
| `SCOPE` | What is explicitly in / out of bounds? | Core | every task |
| `ACCEPTANCE` | How is "done" verified — what makes it correct? | Core | build / fix / spec / review |
| `INPUTS` | What data/artifacts/examples to operate on (shape, a real sample, location)? | Core | anything consuming data |
| `CONSTRAINTS` | Stack, perf/security/compliance limits, deadline, budget | Conditional | impl / design / infra |
| `ENVIRONMENT` | Runtime, versions, deploy target, branch & repo state | Conditional | impl / migration / ops |
| `INTERFACES` | Upstream/downstream contracts, APIs, dependencies touched | Conditional | integration / API / refactor |
| `AUDIENCE` | Who consumes the output (reader, end-user, persona, tone) | Conditional | docs / UX / content / marketing |
| `PRIOR_ART` | Existing code/patterns/docs to reuse or conform to | Conditional | feature / refactor in an existing repo |
| `RISK` | Reversibility tolerance and acceptable blast radius | Conditional | destructive / irreversible actions |

The taxonomy is the checklist that makes a clarification *comprehensive* — "give me X, Y, Z" instead
of one ad-hoc guess. It is NOT a mandate to ask about every dimension (that violates §3).

---

## 2. Per-Dimension Sufficiency Triage

Classify each relevant dimension into one state. The state — not the mere absence of info — decides
the action.

| State | Meaning | Action |
|-------|---------|--------|
| `KNOWN` | Present in the request or conversation | Use it; never re-ask (anti-pattern: asking what the user already said) |
| `INFERABLE` | Not stated but derivable from a retrievable source (§3) | **Retrieve, don't ask.** Then state the inference ("I'm assuming …") |
| `MISSING / non-blocking` | Absent, and a safe default exists with reversible consequences | Pick the safe default, document it inline, proceed |
| `MISSING / blocking` | Absent, AND (no safe default OR the action is hard to reverse) | Ask — bundle into the §4 question turn |

Reversibility rule (aligns with the Autonomy contract): *ambiguous + reversible → safe default + note;
ambiguous + irreversible → ask*. A missing `RISK`/destructive-scope dimension is blocking by default.

---

## 3. Retrieve Before Asking (Context-Engineering core)

A dimension is only `MISSING` after these sources are exhausted. Asking for something retrievable
wastes user trust and is the primary anti-pattern.

1. **Conversation history** — resolve pronouns ("it", "that"); re-read what was already stated.
2. **Repo state** — `git status` / `git log` / `git diff`, branch, recent commits.
3. **Project memory** — `.agents/PROJECT.md`, the agent's `.agents/<name>.md` journal.
4. **Config & conventions** — `CLAUDE.md` / `AGENTS.md`, stack manifests, existing specs in `docs/`.
5. **Codebase** — existing patterns answer `PRIOR_ART`, `INTERFACES`, `ENVIRONMENT` directly.

Only dimensions still unresolved after retrieval are eligible for a question.

---

## 4. Structured Question Assembly

When ≥ 1 dimension is `MISSING / blocking`, emit **one** `AskUserQuestion` turn (per
`_common/INTERACTION.md` `QUESTION_FORMAT`) that batches them — up to the tool's 4-question cap,
highest-leverage / most-irreversible first. Each missing dimension becomes one question with concrete,
option-driven choices (never an open "what do you mean?"). Offer a recommended default first when one
exists, so the user can one-tap proceed.

Per-dimension question seeds (fill the brackets from the actual task; `header` ≤ 12 chars):

| Dim | `header` | Question seed |
|-----|----------|---------------|
| `GOAL` | "Goal" | "What's the primary outcome you want from [task] — [A] / [B] / [C]?" |
| `SCOPE` | "Scope" | "How wide should this go — [just the named target] / [the feature] / [system-wide]?" |
| `ACCEPTANCE` | "Done when" | "What signals this is done correctly — [test passes] / [metric ≥ X] / [manual check]?" |
| `INPUTS` | "Input data" | "What should it run on — [sample/path A] / [B]? Can you share one real example?" |
| `CONSTRAINTS` | "Constraints" | "Any hard limit I must respect — [stack/version] / [perf budget] / [compliance]?" |
| `ENVIRONMENT` | "Target env" | "Which runtime/target — [local] / [staging] / [prod] / [version]?" |
| `INTERFACES` | "Contracts" | "Does this touch a contract I must preserve — [API X] / [schema Y] / [none]?" |
| `AUDIENCE` | "Audience" | "Who reads/uses the output — [end-user] / [engineer] / [exec]? Tone?" |
| `PRIOR_ART` | "Follow" | "Anything existing to match — [module X] / [doc Y] / [start fresh]?" |
| `RISK` | "Reversibility" | "How reversible must this stay — [easily revert] / [coordinated rollback ok] / [no data loss]?" |

After the answer, record it (`_common/INTERACTION.md` `CONFIRMATION_RECORD`) and, for orchestrated
runs, pass the resolved dimensions as the next step's context delta so the question is asked once,
not re-asked downstream.

---

## 5. Economy Rules (don't over-collect)

Context Engineering optimizes for *just enough*, not maximal. Violating these re-creates the
"over-questioning sin".

- **Never ask what's `KNOWN` or `INFERABLE`.** Retrieval first, always.
- **One turn, ≤ 4 questions.** Batch blocking dimensions; never a multi-message interrogation.
- **Safe default beats a question** whenever consequences are reversible — proceed and disclose.
- **Stop at sufficiency.** Once the blocking set is resolved, act; don't keep gathering nice-to-haves.
- **Disclose every inference** ("I interpreted … / assumed …") so a wrong fill is cheap to correct.

---

## 6. Gate Flow (summary)

```
Outcome defined
  → inventory relevant dimensions (§1, Core always + Conditional by task type)
  → triage each (§2) after retrieval (§3)
  → blocking-missing set empty?
       YES → act now (disclose inferences + safe defaults taken)
       NO  → one AskUserQuestion turn batching the blocking set (§4)
              → record answers, proceed
```

Output language for questions follows the CLI global config (`_common/OPERATIONAL.md`); IDs and
technical terms stay in English.
