# Evaluator Loop Protocol (Loop + Contract + Rubric)

**Purpose:** Generator-Evaluator separation for active quality assurance, with a Sprint Contract as the acceptance spec and a Rubric as the scoring instrument.
**Read when:** A task qualifies for Evaluator Loop and you need to set it up end-to-end (when to apply, what contract to write, what rubric to score against, how to spawn and iterate).
**Invocable as:** `/nexus converge` — this file is the spec; `converge` is its invocable Recipe, adding mandatory termination bounds and the flatten rule for wrapping loop-recipes. See `reference/converge-recipe.md`.

This file merges the former `evaluator-loop.md` (orchestration pattern), `sprint-contract.md` (acceptance spec format), and `rubric-system.md` (scoring instrument). They form one pipeline: **Contract → Generator → Evaluators(Rubric) → Aggregate → ACCEPT / REVISE / BLOCK**.

---

## Core Principle

> An agent must never evaluate its own output. (GAN-inspired separation)

The Generator produces deliverables; independent Evaluators score them against the Sprint Contract using the Rubric. Separation eliminates self-assessment bias and catches issues the Generator's context window cannot see.

## The Triangle

```
                  Sprint Contract
                 (acceptance spec)
                   /          \
                  /            \
            scored by         used by
                /                \
               ▼                  ▼
           Rubric  ◄── feeds ──   Evaluators
        (0-3 scale)               (parallel)
```

- **Sprint Contract**: declares what "done" means before any code is written.
- **Rubric**: graduated 0-3 dimension scoring (replaces "looks good").
- **Evaluators**: independent agents that score the Generator's output against the contract using the rubric.

---

## Applicability

| Task Type | Complexity | Evaluator Loop | Default Evaluators |
|-----------|-----------|----------------|--------------------|
| FEATURE (UI) | MEDIUM+ | **YES** | Voyager + Radar |
| FEATURE (Backend) | MEDIUM+ | **YES** | Judge + Radar + Attest |
| FEATURE (Full-stack) | MEDIUM+ | **YES** | Judge + Voyager + Radar + Attest |
| BUG | SIMPLE | NO | (VERIFY suffices) |
| BUG | COMPLEX | **YES** | Radar + Attest |
| SECURITY | Any | **YES** | Sentinel + Judge + Radar |
| REFACTOR | SIMPLE | NO | (VERIFY suffices) |
| REFACTOR | COMPLEX | **YES** | Judge + Radar |
| OPTIMIZE | MEDIUM+ | **YES** | Radar + Judge |
| DOCS | Any | NO | (VERIFY suffices) |

**Rule:** When Evaluator Loop applies, a Sprint Contract is required. When it doesn't, Phase 6 VERIFY runs traditional test-only verification.

---

## Sprint Contract

### Format

```yaml
SPRINT_CONTRACT:
  ID: "SC-[task-slug]-[YYYYMMDD]"
  Goal: "[1-2 sentence description of the deliverable]"
  Scope:
    in_scope:     [specific deliverable 1, ...]
    out_of_scope: [explicitly excluded 1, ...]
  Acceptance_Criteria:
    functional:
      - {id: "AC-F-001", criterion: "[what must work]", verification_method: "test|E2E|manual|static", evaluator: "Radar|Voyager|Attest|..."}
    quality:
      - {id: "AC-Q-001", criterion: "[quality requirement]", threshold: "[measurable, e.g., coverage > 80%]", evaluator: "Judge|Zen|Sentinel|..."}
  Rubric_Ref: "FEATURE_UI | FEATURE_BACKEND | BUG_FIX | SECURITY"
  Generator: "[agent name]"
  Evaluators: ["agent1", "agent2", "..."]
  Max_Iterations: [1-5, default: 3]
  Context_Strategy: "reset | continuous | hybrid"   # see context-strategy.md
```

### Creation Flow

Created during **AUTORUN_FULL Phase 2: PREPARE**, after classification and before chain selection.

```
Phase 1: PLAN (task classified)
   ↓
Phase 2: PREPARE
   ↓
   Evaluator Loop applicable? (see table)
     ├─ NO  → skip contract, proceed to CHAIN_SELECT
     └─ YES
          ↓
        Nexus creates SPRINT_CONTRACT:
          1. Extract Goal from user request
          2. Define Scope (in/out)
          3. Derive Acceptance_Criteria
          4. Select Rubric_Ref from task type (see Rubric Selection below)
          5. Assign Generator + Evaluators from chain
          6. Set Max_Iterations (default 3)
          ↓
        Contract stored in execution context
          ↓
        Phase 3: CHAIN_SELECT (contract informs chain)
```

### Contract in Handoff

```
## NEXUS_HANDOFF
- Summary: [...]
- Contract_Ref: SC-login-feature-20260325
- Next: [...]
```

Generator receives the contract in its spawn prompt. Evaluators receive it to know what criteria to score against.

### Lifecycle

| State | Trigger | Action |
|-------|---------|--------|
| `DRAFT` | PREPARE begins | Nexus creates contract |
| `ACTIVE` | EXECUTE begins | Generator starts work |
| `EVALUATING` | Generator completes iteration | Evaluators score against contract |
| `REVISED` | Evaluator returns REVISE | Generator receives feedback, iterates |
| `FULFILLED` | All Evaluators ACCEPT | Contract complete → DELIVER |
| `TERMINATED` | Max iterations OR diminishing returns | Best result accepted → DELIVER |

---

## Rubric System

### Score Scale

| Score | Level | Description | Decision |
|-------|-------|-------------|----------|
| 3 | Exemplary | Exceeds best practices | (toward ACCEPT) |
| 2 | Sufficient | Meets acceptance criteria | (toward ACCEPT) |
| 1 | Partial | Gaps exist; needs revision | → REVISE |
| 0 | Not considered | Serious issues | → BLOCK |

**Decision mapping:**
- All dimensions ≥ 2 → `ACCEPT`
- Any dimension == 1 AND none == 0 → `REVISE` (targeted feedback)
- Any dimension == 0 → `BLOCK` (escalate to user)

### Evaluation Dimensions

| Dimension | Weight Range | Default Evaluator | Description |
|-----------|-------------|-------------------|-------------|
| Correctness | 0.25 – 0.40 | Radar, Attest | Tests pass, requirements met, no regressions |
| Design Quality | 0.10 – 0.25 | Judge, Zen | Code structure, patterns, maintainability |
| Craft | 0.10 – 0.20 | Judge | Naming, formatting, idioms, documentation |
| Functionality | 0.15 – 0.25 | Voyager, Attest | Feature works as specified, edge cases handled |
| Security | 0.00 – 0.20 | Sentinel | No vulnerabilities, secure patterns |

**Constraint:** Dimension weights MUST sum to 1.0 per rubric instance.

### Task-Type Templates

**FEATURE_UI** — Correctness 0.25 / Functionality 0.25 / UX Quality 0.20 / Design Quality 0.15 / Craft 0.15
**FEATURE_BACKEND** — Correctness 0.35 / Design Quality 0.25 / Functionality 0.20 / Craft 0.10 / Security 0.10
**BUG_FIX** — Correctness 0.40 / Functionality 0.25 / Design Quality 0.20 / Craft 0.15
**SECURITY** — Security 0.35 / Correctness 0.30 / Design Quality 0.20 / Craft 0.15

### Rubric Selection

```
Task == FEATURE && has_ui_changes? → FEATURE_UI
Task == FEATURE && backend_only?    → FEATURE_BACKEND
Task == BUG                          → BUG_FIX
Task == SECURITY                     → SECURITY
Other                                → FEATURE_BACKEND (default)
```

### Rubric Evaluation Output

```yaml
RUBRIC_EVALUATION:
  Evaluator: "[agent name]"
  Contract_Ref: "[sprint contract ID]"
  Iteration: [N]
  Dimensions:
    - {dimension: "Correctness", score: 0-3, evidence: "[findings with file:line]", recommendation: "[action if < 2]"}
    - {dimension: "Design Quality", score: 0-3, evidence: "...", recommendation: "..."}
  Weighted_Score: [0.00 – 3.00]
  Verdict: ACCEPT | REVISE | BLOCK
  Feedback: "[actionable summary for Generator]"
```

### Rubric → Quality Band Conversion (long-term tracking)

`evaluator_normalized_score = (weighted_rubric_score / 3.0) × 100`

This yields **this evaluator's normalized 0-100 contribution**, not UQS itself. UQS is the weighted composite across agents defined in `quality-iteration.md` § Unified Quality Score; the value above enters it as one term.

| Rubric Weighted | Normalized Score | Band |
|-----------------|----------------|------|
| 2.70 – 3.00 | 90 – 100 | Excellent |
| 2.40 – 2.69 | 80 – 89 | Good |
| 2.10 – 2.39 | 70 – 79 | Acceptable |
| 1.80 – 2.09 | 60 – 69 | Fair |
| < 1.80 | < 60 | Poor |

Rubrics drive per-Sprint evaluation; UQS tracks long-term trends via PDCA (`quality-iteration.md`).

**Comparability guard.** A normalized score is only comparable across cycles when the rubric text, the evaluator prompt, and the evaluator model are all unchanged. Record `rubric_version`, `evaluator_prompt_version`, and `evaluator_model` alongside every `RUBRIC_EVALUATION`; when any of the three changes, re-score the retained cases before comparing, and never read a trend across the boundary.

---

## Evaluator Team

| Evaluator | Assessment Target | Method |
|-----------|------------------|--------|
| Judge | Code quality (static) | Code review, style, patterns |
| Voyager | Functional behavior (dynamic) | Playwright E2E, active exploration |
| Attest | Spec compliance | Acceptance-criteria verification |
| Radar | Test coverage & correctness | Test execution, coverage measurement |
| Sentinel | Security posture | Static security scan |

**Evaluators are read-only.** They never modify code — they return structured feedback for the Generator to act on.

---

## Loop Control

| Parameter | Default | Range |
|-----------|---------|-------|
| Max Iterations | 3 | 1-5 |
| Termination: All ACCEPT | — | — |
| Termination: Diminishing returns | — | weighted score improves < 0.2 between iterations |
| Termination: Max reached | — | best result accepted |

---

## Evaluation Feedback Format

Each Evaluator emits:

```yaml
EVALUATION_FEEDBACK:
  Evaluator: "[agent name]"
  Contract_Ref: "[sprint contract ID]"
  Iteration: [N]
  Verdict: ACCEPT | REVISE | BLOCK
  Rubric_Scores:
    - {dimension: "[name]", score: 0-3, evidence: "[file:line + finding]"}
  Issues:
    - {severity: CRITICAL|HIGH|MEDIUM|LOW, description: "...", location: "[file:line]", suggestion: "..."}
  Summary: "[1-2 sentence overall]"
```

## Feedback Aggregation

```
Collect all EVALUATION_FEEDBACK
  ↓
Aggregate verdict:
  - Any BLOCK    → ESCALATE (present BLOCK reasons + context to user)
  - All ACCEPT   → DELIVER
  - Any REVISE   → compile REVISION_BRIEF and iterate

If REVISE:
  - Merge all REVISE issues into one brief
  - Prioritize CRITICAL > HIGH > MEDIUM > LOW
  - Remove duplicates across Evaluators
  - Pass brief to Generator for next iteration
```

```yaml
REVISION_BRIEF:
  Contract_Ref: "[sprint contract ID]"
  Iteration: [N → N+1]
  Issues_To_Address:
    - "[CRITICAL] description (from Evaluator)"
    - "[HIGH] description (from Evaluator)"
  Issues_Deferred:
    - "[LOW] description — deferred, does not block acceptance"
  Evaluator_Verdicts:
    Judge: REVISE | Radar: ACCEPT | Attest: REVISE
```

---

## Orchestration Pattern (Pattern H)

Extends `orchestration-patterns.md` Patterns A-G.

```
Nexus → Agent(Generator, foreground) → _STEP_COMPLETE
                                          ↓
Nexus → spawn Evaluators (parallel, background):
         Agent(Evaluator-1, bg) + Agent(Evaluator-2, bg) + ...
                                          ↓
         Wait for all Evaluators
                                          ↓
Nexus → Aggregate EVALUATION_FEEDBACK
         ├─ All ACCEPT                       → DELIVER
         ├─ Any REVISE (iter < max)          → REVISION_BRIEF → Generator → loop
         ├─ Any REVISE (iter >= max)         → accept best → DELIVER with quality notes
         └─ Any BLOCK                        → ESCALATE to user
```

### Spawn Template (shared body)

For per-CLI spawn syntax, see `nexus/reference/execution-layers.md`. The Evaluator prompt body differs from a normal agent in just two lines:

```
Mode: EVALUATOR (read-only — do not modify code; return EVALUATION_FEEDBACK only)
Sprint Contract:
[contract content]

Target to evaluate: [Generator's output summary + artifact paths]
```

Run Generators on foreground (sequential dependency); fan out Evaluators in parallel (background). When all Evaluators return, aggregate.

---

## Integration with Execution Phases

```
Phase 6: VERIFY
  ├─ Evaluator Loop DISABLED → Traditional verification (tests, build, security scan)
  └─ Evaluator Loop ENABLED
       ↓
     6a: Spawn Evaluators (parallel, background)
     6b: Aggregate EVALUATION_FEEDBACK
     6c: Decision
          ├─ ACCEPT → Phase 7: DELIVER
          ├─ REVISE → return to Phase 4: EXECUTE (Generator re-executes with brief)
          └─ BLOCK → ESCALATE
```

Traditional VERIFY checks (tests pass, build OK) are subsumed by the Evaluator team — Radar handles tests, Sentinel handles security, etc.

---

## Best Practices & Anti-Patterns

**Do:**
1. Keep contract scope tight — one Sprint, not an epic.
2. Make every criterion measurable with a concrete verification method.
3. Map each criterion to exactly one Evaluator.
4. Default Max_Iterations to 3 (1 for trivial, 5 only for critical).
5. Make out-of-scope explicit — prevents Generator gold-plating.

**Don't:**
1. Let the Generator evaluate its own output — always independent Evaluators.
2. Assign more than 4 Evaluators per loop — diminishing returns.
3. Run without Max Iterations — accept best result when exhausted.
4. Accept vague feedback — Evaluators must include `file:line` + actionable suggestion.
5. Let Evaluators modify code — they only return feedback.

### Where to Spend Tuning Effort

Source: `anthropic.com/engineering/harness-design-long-running-apps` (2026-03-24).

1. **Tune the Evaluator, not the Generator.** Making an Evaluator appropriately skeptical is *far more tractable* than making a Generator self-critical. Iterate the Evaluator prompt against logged cases where its verdict diverged from a human's — that log is the tuning dataset, and it is the highest-leverage artifact in the loop.
2. **Ground the Evaluator in tools, not description.** An Evaluator that reads a diff guesses; one that drives the artifact (Playwright/browser MCP for UI, the actual test runner for code) observes. Give every Evaluator at least one tool that exercises what it scores.
3. **Calibrate with scored few-shots.** Attach 2-3 worked examples with full score breakdowns to the rubric — without them, scores drift across iterations and cross-iteration comparison is meaningless.
4. **Rubric wording is a steering input, not just a measurement.** Criterion phrasing measurably shifts what the Generator produces even with no explicit feedback ("museum quality" reshaped visual output on its own). Weight the dimensions where the model is *weak*; over-weighting dimensions it already handles buys nothing.
5. **Budget the loop against solo-agent baseline.** A measured comparison: solo agent 20 min / $9 (core feature broken) vs. full Generator-Evaluator harness 6 hr / $200 (working) — ~18× wall-clock and ~22× cost. The loop earns that only when the task sits *beyond* what the model does reliably solo. For a task inside solo range, the loop is pure overhead; check this before spawning Evaluators.
6. **Expect non-linear scores.** Improvement is not monotonic across 5-15 iterations, and a mid-run iteration is sometimes the best one. Retain per-iteration artifacts and select the best, rather than shipping the last.
7. **A tuned Evaluator still misses.** Subtle bugs, layout defects, and deeply nested features survive it. `converge` passing is not a substitute for an independent VERIFY step.
