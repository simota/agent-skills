# Adaptive Prompt Policy — Context-Adaptive Spawn Tuning

**Purpose:** Auto-tailor every spawn prompt to the current **project** and **session** context, and self-reinforce within the session from observed outcomes — so inter-agent instructions get sharper as a session progresses, without any durable global rewrite.
**Read when:** Composing a spawn prompt at an EXECUTE step, or deciding how directives adapt to project/session signals.

> **Scope is the safety model.** This policy operates **only within the current session + project**. It is **ephemeral** (resets at the session/project boundary) and **reversible** (every adjustment is per-spawn; nothing irreversible happens). Prompt-only tuning within the existing grant requires no new approval; cost, permission and mode gates still apply. Durable, cross-project template rewrites are explicitly **out of scope** here; that path stays gated (offline `tune` → Darwin promotion → Guardian commit, see §6).

> **Honest mechanism.** This is **evidence-accumulating, case-based adaptation** — not neural RL. The hub cannot train weights mid-session. "Reinforcement" means: a journaled within-session record of `context-features → directive-choice → outcome`, consulted to bias the next spawn's directive selection. Bounded, **corrective (bidirectional)** heuristics over a vetted directive library, never free-form prompt invention — every adjustment maps to an existing structured directive field (envelope / authorized effort / tool-use / which references), never raw prepended text.

---

## 1. The three layers

```
① PROJECT PROFILE  — built once per session (first spawn / hub init), from project facts
② SESSION LEDGER   — grows through the session, from each spawn's outcome
③ ADAPTIVE ASSEMBLY — every EXECUTE step: base template ⊕ ① ⊕ ② → the spawn prompt
```

> **Boundary vs `specify-phase.md`.** This policy tunes **directive fields** (envelope, authorized effort, tool-use, which references) and never writes task content. The instruction's **content** — goal, acceptance criteria, prohibited outcomes, what stays delegated — is set once at the gated `SPECIFY` phase and copied verbatim into every `_AGENT_CONTEXT`. Order is fixed: Specified Brief first, directive fields layered on after. They occupy disjoint fields and must never overwrite each other.

Layer ③ is the only thing that touches a spawn; ① and ② are the inputs it reads. Layer ① is built during **Orchestrator Detection** (before the first spawn) and cached; ② updates at each step boundary; ③ runs immediately before each `Agent(...)` spawn.

### Applicability — when NOT to apply

Profile assembly + ledger upkeep is meta-overhead; applying it to trivial work violates the minimum-chain principle (Core Rule #1). **Gate:**
- **Skip** for a single-spawn or trivial run — use the base template directly (the Project Profile's hub-engine defaults still apply, since those are free and load-bearing for correctness; the Session Ledger does not spin up).
- **Apply** when the chain has ≥ 3 spawns, runs a loop recipe (`converge`/`kaizen`/`apex`/`migrate`), or the same agent is spawned more than once — i.e. when there is enough repetition for within-session reinforcement to pay back its overhead.

---

## 2. Layer ① — Project Profile (per-session, built once)

Assemble at Orchestrator Detection (before the first spawn) and cache for the session. Sources and the directive defaults they imply:

| Source | Signal | Directive default it sets |
|--------|--------|---------------------------|
| `.agents/PROJECT.md` | project phase, goals, constraints | which references to front-load; tone |
| repo stack (lang / framework) | TS-strict / dynamic / native | tool-use directive emphasis (type rigor, test-first) |
| `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` | conventions, language, style | output language, naming, commit style passed to spawns |
| host runtime and advertised capabilities | adapter and authorized model/effort | Shared P-principles and mandatory outcome/authority fields; CLI-specific syntax from `_common/CLI_COMPATIBILITY.md` |
| domain affinity (Game/SaaS/…) | task domain | default add-on agents, envelope sizing |
| repo size / file count | scope | base output envelope (small repo → tighter) |

The Project Profile is **read-only project context** — it does not modify any project file.

---

## 3. Layer ② — Session Ledger (per-session, accumulates)

Held in working state for the session — **bounded**: keep only the *last-good directive set per agent* plus a short rolling tail, never the full spawn history (it must not itself grow into the context it protects, Core Rule #6). Optionally journaled (§5). After each spawn, update that agent's row:

`{ agent, recipe, directive_choices, reward, output_len vs envelope, token_cost, correction? }`

**Reward = the downstream objective signal, not self-report.** The primary reward is the **VERIFY result** for the step (tests/build/AC pass). `_STEP_COMPLETE.status` is only a *provisional* signal until VERIFY resolves — a self-reported `SUCCESS` that later fails VERIFY counts as a failure, never a win (Nexus warns that valid-schema/wrong-meaning output amplifies downstream; tuning on self-report would reinforce confident-but-wrong prompts).

Within-session signals → next-spawn adjustment. **A directive only flips on a repeated signal (≥ 2 observations of the same class), never on a single outlier** (§7):

| Observed this session | Adjustment to subsequent spawns |
|-----------------------|----------------------------------|
| Output repeatedly overran its envelope | Tighten the envelope for that agent / similar tasks |
| Step failed VERIFY (or `BLOCKED`/`FAILED`) | Diagnose the evidence, then supply the smallest missing context or corrected instruction; change effort only within the authorized runtime and budget |
| Steps repeatedly passed VERIFY cheaply | Loosen — trim directives for token economy (corrective, bidirectional) |
| **User issued an explicit correction turn** (style, scope, wrong assumption) | Map it to a **structured constraint** on subsequent same-agent spawns (envelope / tone / scope / forbidden-actions field) — never prepend the raw correction text. Detected only from an explicit user turn, not inferred. |
| Token budget pressure rising | Trim which references are loaded; shrink envelopes; switch context-strategy toward `reset` |
| Same agent ran before this session | Reuse its last-good directive set as the starting point |

Adjustments are **corrective and bidirectional** (tighten or loosen), and **forgotten after the session** — last session's state never silently persists into a fresh one (warm-start §5 is the one opt-in exception).

---

## 4. Layer ③ — Adaptive Assembly (every spawn)

At each EXECUTE step, compose:

```
spawn_prompt = base template (Agent Spawn Template)
             ⊕ Project Profile defaults (②)
             ⊕ Session Ledger adjustments (③)
```

**Bounded to vetted ranges — the assembly is selection, not invention:**
- Output limits, supported effort settings, tool constraints, and the reference subset are chosen from the libraries in `hub-authoring.md` / `OPUS_5_AUTHORING.md`. The policy **selects and dials within** those; it never authors a novel unsafe directive.
- **Never deletes a behavior or safety rule, acceptance criterion, or output-contract field** (Core Rule #4 — preserve behavior before style). Adaptation only *adds/sizes* guidance; it cannot strip the spawn's required structure.
- **Outcome and authority controls are floors, not dials.** Size the output envelope and scope to the task; preserve frozen ACs, prohibited outcomes and completion criteria. A failed check needs diagnosis and a targeted fix, not a generic self-check instruction or automatic effort escalation.
- **Honor `hub-authoring.md`.** Adapt supported runtime settings within the existing grant; never demand private reasoning, bypass refusal, or weaken independent verification. Concrete tests remain required even when generic self-review prose is removed.

The tuning shapes the spawn prompt but does **not** bypass the active Mode's confirmations (in `INTERACTIVE`/`GUIDED` the step still stops where the Mode requires; only the prompt *content* is adapted, not the gating). It is **internal but never silent**: every adjustment that differs from the base template emits a **Tuning Trace** (§9) so the user can always see what was changed and why.

The result is a spawn prompt tuned to *this* project and *this* session's accumulated signal, every time.

---

## 5. Optional warm-start (off by default)

The only persistence offered: journal the end-of-session Project Profile + last-good directive sets to `.agents/adaptive-prompt-policy.journal.md` (gitignored). On the next session **in the same project**, load it so the session starts pre-tuned instead of cold.

- This is a **context cache, not a template rewrite** — it pre-seeds Layer ① only, still bounded to vetted ranges, still overridable by this session's fresh signals.
- Off by default; enable explicitly. Even on, it never edits a spawn template, a SKILL.md, or any tracked file.

---

## 6. Out of scope (the gated path)

Durable, cross-project changes — rewriting the Agent Spawn Template, `hub-authoring.md`, `_common/HANDOFF.md`, or an agent's `SKILL.md` — are **not** done by this policy. If a within-session pattern proves broadly valuable, it is promoted through the **gated** path, never automatically:

`offline tune (corpus backtest) → Lore curation (METAPATTERNS) → Darwin promotion proposal → user approval → Guardian commit`

This keeps the irreversible, all-spawns-affecting writes behind evidence + approval, while the day-to-day session/project adaptation here stays fully automatic.

---

## 7. Guards

Each guard is defined where it operates; this is the index of what is guarded and where the rule lives.

- **G1 Overfitting to one task** — agent/task-class scoping + the ≥ 2-same-class-observation flip rule (§3).
- **G2 Reinforcing confident-but-wrong output** — reward is the downstream VERIFY result, not self-reported status (§3).
- **G3 Meta-overhead on trivial work** — the applicability gate (§1).
- **G4 Ledger growing into the context it protects** — bounded ledger: last-good per agent + short tail (§3).
- **G5 Free-form injection via user corrections** — corrections map to structured constraint fields, never raw text (§3).
- **G6 Adaptation masking a real problem** — persistent VERIFY-fail / BLOCKED / FAILED escalates through normal error handling instead of being re-tuned (§3).
- **G7 Stripping required structure** — the hard rule that behavior/safety/AC/output-contract fields are never deleted (§4).
- **G8 Cross-session contamination** — ephemeral by default; warm-start pre-seeds Layer ① only (§5).
- **G9 Unsafe directive** — reject private-reasoning extraction and any directive that widens authority (§4).

---

## 8. Relationship to neighbors

- **`context-strategy.md`** — sibling: that decides *what context flows* between agents (reset / persist / hybrid); this decides *how the spawn directives adapt* to project+session signals. Used together at spawn time.
- **`hub-authoring.md` / `OPUS_5_AUTHORING.md`** — the vetted directive library this policy selects from; the source of the P/F principles it must honor.
- **LEARN / `routing-learning.md`** — LEARN adapts *routing* (which chain) across runs with durable safety; this adapts *spawn directives* within a session, ephemerally. Same evidence spirit, different target and scope.

---

## 9. Disclosure — Tuning Trace

The tuning is internal but **never silent** — a tuned spawn is never quietly different from the base template (the "log what changed, no silent caps" principle). Whenever Layer ③ produces a directive that differs from the base, it emits one Tuning Trace entry.

**Entry schema:**

`{ step, agent, field, old → new, trigger, reward_basis }`

- `field` — which directive changed (envelope / scope-bound / effort / tool-use / thinking / references / context-strategy).
- `trigger` — the §3 signal that caused it (e.g. `repeated overlength ×2`, `VERIFY-fail`, `user correction`, `token pressure`).
- `reward_basis` — the evidence the decision rests on (e.g. `VERIFY pass×3`), so the user can judge whether the adaptation was warranted.

**Where it surfaces (delta-only — zero output when nothing was tuned, so it adds no noise):**
1. **Inline in the Nexus Execution Report** — a tuned step's per-step line carries a compact one-liner, e.g.
   `🎛 Forge: envelope 200→120w (repeated overlength) · effort high→med (VERIFY pass×3)`
2. **`## Prompt Tuning` summary subsection in `DELIVER`** — the full per-spawn trace table, included **only when ≥ 1 spawn was tuned**; omitted entirely otherwise.
3. **Journal (with warm-start §5)** — appended to `.agents/adaptive-prompt-policy.journal.md` for audit/resume; carries the trigger + reward_basis so a later session (or the user) can review *why* each tuning happened.

This makes every internal adjustment **inspectable after the fact** without forcing a confirmation gate — the user sees what changed, the signal behind it, and the evidence, but the reversible per-spawn tuning still runs automatically.
