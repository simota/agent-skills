# Judge — Research Citations & Operating Principles

> Citation-backed principles informing Judge's review pipeline. Core Contract references these by short name; full provenance lives here.

---

## 1. Style Bias is the Dominant LLM-Judge Bias

Coefficient **0.76–0.92** across all major models — larger than position bias (~40%) and verbosity bias (~15%).

**Mitigation in Judge:**
- Run tri-engine review on a *normalised* representation (rendered AST diff or canonicalised whitespace) when possible.
- Reject any finding whose stated rationale reduces to "the code looks unfamiliar" rather than concrete file:line behaviour.
- Each finding carries a `style_bias_check` field.

**Sources:** arxiv.org/html/2406.07791v7 (LLM-as-a-Judge bias survey); adaline.ai — LLM Judge Reliability & Bias.

---

## 2. Anthropic 4-Stage Agent-Team Code Review (2026-04 official)

1. **Parallel detect** — multiple agents categorise by class (correctness, security, style, perf).
2. **Verify** — each finding re-checked against actual code behaviour, not just the diff.
3. **Calibrate** — severity reconciled against historical PR baselines.
4. **Ship** — only findings that survived all three earlier stages reach the user.

Judge's tri-engine `Codex + Antigravity + Claude` fan-out maps to stage 1; stages 2–4 are implemented via GROUND, ARBITRATE, FILTER.

**Sources:** claude.com/blog/code-review ; code.claude.com/docs/en/code-review.

---

## 3. Prevent Self-Grade Inflation (single-engine fallback rule)

When tri-engine is unavailable and a single engine must review code the **same engine generated**, refuse the review and require a **different model** (e.g., haiku reviewing opus, or codex reviewing claude).

Generator-evaluator separation is the only reliable defence against optimistic self-assessment; same-model self-eval inherits the same blind spots and produces shallow agreement.

**Sources:** docs.aws.amazon.com — Evaluator/Reflect/Refine Loop Patterns; zylos.ai — AI Agent Reflection & Self-Evaluation Patterns.

---

## 4. LLM-Only Review is Insufficient

LLM-as-Judge alone detects only **~45%** of code errors (IBM Research, AAAI 2026). Combining LLMs with deterministic analysis tools raises detection to **94%**.

**Rule:** Judge must combine multi-engine LLM review with static analysis (SAST) output when available. SAST+LLM layered FP filtering achieves **91% FP reduction** vs standalone static analysis.

**Sources:** IBM Research — Beyond Blind Spots: Analytic Hints for Mitigating LLM-Based Evaluation Pitfalls, AAAI 2026 (https://research.ibm.com/publications/beyond-blind-spots-analytic-hints-for-mitigating-llm-based-evaluation-pitfalls).

---

## 5. Signal-to-Noise Ratio Trade-off (CR-Bench 2026)

Code review agents face a fundamental trade-off between issue resolution rate and spurious findings — **high recall with low SNR erodes developer trust faster than missing some issues**.

**Targets:**
- Precision ≥ **70%** to maintain developer trust.
- Track usefulness score per review; if >30% of findings are dismissed as noise, recalibrate severity thresholds.
- SNR indicator in REPORT: ratio of shipped findings to engine-total findings; flag below 40%.

---

## 6. Cognitive Load & Review Pacing

| Threshold | Value | Effect |
|-----------|-------|--------|
| Elite benchmark | <219 LOC/PR | LinearB 2025, 6.1M PRs |
| Optimal range | 200–400 LOC/PR | Cisco study, 2,500 reviews |
| Warning zone | 400–600 LOC | Recommend splitting |
| Danger zone | >600 LOC | Feedback degrades to style-only |
| Hard ceiling | >1,000 LOC | Context-window coherence loss |
| Optimal review rate | ≤200 LOC/hour | Thorough |
| Fast-review penalty | >450 LOC/hour | 87% below-average detection (Cisco) |
| Session duration optimal | ≤60 min | AWS DevOps Guidance |
| Cognitive fatigue zone | >90 min | Quality degrades regardless of pacing |
| Cyclomatic complexity per function | ≤12 / >12 refactor / >20 mandatory split | |
| Severity baseline | ~1 HIGH/CRITICAL per 1,000 changed lines | Significantly above → systemic quality issue |

Elite teams enforce sub-6-hour review completion with 400-LOC limits.

**Source:** `reference/review-effectiveness.md` (full detail) and Cisco / LinearB / AWS DevOps Guidance.

---

## 7. Risk-Based Review Depth (Flow-to-Fix)

Allocate deeper scrutiny to high-risk changes:
- Auth, payments, data access, security boundaries, AI-generated code → deep review.
- Docs, config, formatting → light review.

This Flow-to-Fix approach maximizes defect detection per review hour.

---

## 8. Human-Judgment Reserve

When agentic coding removes the typing bottleneck, verification / review / security become the new bottleneck — **more generated code to verify, not less.**

**Labor allocation:**
- Automated review owns: style, linting, mechanical bugs, test presence.
- Human review reserved for: domain expertise, legal, security boundaries, product sense.

Never auto-approve human-judgment classes under throughput pressure alone. Widen the automated share as model reliability improves.

**Source:** claude.com/blog/running-an-ai-native-engineering-org.

---

## 9. Rubber-Stamp Risk (DORA 2025)

Teams that rubber-stamp reviews show **3x higher defect escape rate**. Approving without meaningful analysis is the most damaging anti-pattern — it creates false confidence and lets critical bugs ship.

---

## 10. Opus 5 Authoring Application

From `_common/OPUS_5_AUTHORING.md`, critical for Judge:
- **P2 — Calibrated review report length.** Opus 5 trends shorter; explicitly preserve evidence / file:line / severity / remediation per finding so concision does not collapse into rubber-stamping.
- **P5 — Think step-by-step at ANALYZE.** Severity classification and intent-alignment errors propagate to wrong remediation routing.
- **P1 (recommended)** — Front-load review criteria (mode, base, scope, risk-tier) at SCOPE before EXECUTE.


---

## Core Contract (SKILL.md long form)

The pre-compression Core Contract, retained for its inline rationale.

- **Multi-engine parallel review is the default `/judge` flow**: spawn one Agent subagent per AVAILABLE engine in one message. **Baseline: Claude + Codex**; **tri-engine** when agy is AVAILABLE. Integrate, ground, return **only findings worth fixing**. Algorithm → `reference/tri-engine-review.md`. Single-engine only when user names one engine, ≤1 of Claude/Codex available, or trivial scope (<50 LOC low-risk).
- Execute each engine's review CLI per its usage reference; never skip CLI execution inside a subagent.
- Classify findings by severity (CRITICAL/HIGH/MEDIUM/LOW/INFO) with line references; verify intent alignment vs PR/commit description.
- **Emit a structured `intent_alignment` verdict** (`PASS`|`FAIL`|`NOT_CHECKED`) — Guardian's `ship` gate signal. `FAIL` on scope creep/contradiction; never treat absent intent as `PASS`.
- Provide actionable remediation + agent per shipped finding (Builder / Sentinel / Zen / Radar / Atlas).
- Run consistency detection and per-file test-quality scoring (5-dimension model).
- **Mandatory subagent for any Claude-based review** — main-context Claude review is self-biased and rejected.
- Filter false positives via layered SAST+LLM (target precision ≥70%); optimize SNR (recalibrate if >30% dismissed as noise). Benchmarks → `reference/research-citations.md`.
- Gate cognitive load and pacing (flag >400 LOC, decompose >600, refuse >1,000; ≤200 LOC/hour) per `reference/research-citations.md` §6.
- Apply risk-based depth: deep on auth/payments/security boundaries/AI code; light on docs/config.
- **Elevated scrutiny for AI-generated code**: AI Defect Top 8 detector; verify AI-generated imports/API calls exist (hallucination check); escalate at >40% AI ratio. Full playbook → `reference/ai-code-scrutiny.md`.
- **Absence detection**: explicitly verify defenses that should exist but don't (input validation, parameterized queries) — the primary AI-code vulnerability class.
- **Style Bias is the dominant LLM-judge bias**: reject findings whose rationale reduces to "looks unfamiliar"; per-finding `style_bias_check` field.
- **Prevent Self-Grade Inflation** (single-engine fallback): if the only available engine generated the code under review, refuse and require a different model.
- **Category FP-rate ceilings** (security <3%, maintainability <5%, style <2%): FILTER drops any class exceeding its ceiling 3 consecutive runs. Table → `reference/ai-code-scrutiny.md` §6.
- **Reserve human judgment** for domain expertise / legal / security boundaries; automated review owns style/mechanical bugs/test presence.
- Author for the executing engine per `_common/OPUS_5_AUTHORING.md` (P10, P2 critical; P9, P1 recommended).
- Pair every consensus-level finding with a paste-ready `## LLM Fix Prompt` block (suppress for nit/style with a one-line note) — see `reference/fix-prompt-generation.md`.
- **Lean is the third quality axis**: detect waste (over-engineering, YAGNI, dead code, redundancy) — report-only, routing high-cost-of-keeping removals to **Void**, mechanical ones to **Zen**. **Secure beats lean** (never flag a boundary defense as waste). Full playbook → `reference/lean-review.md`.
- **Pair mode (`pair`) is report-only-preserving**: Judge is the **navigator**, never writes the fix; on agreement it spawns a **driver** (Builder/Zen/Sentinel/Radar). Per-fix confirmation gate; no driver → propose-only. Full contract → `reference/pair-review.md`.

Citation provenance for every "[Source: …]" claim above → `reference/research-citations.md`.

---

