# Judge — Recipe Definitions (full detail)

Full per-Recipe behavior for the SKILL.md Recipes table and Subcommand Dispatch. SKILL.md carries condensed cells and one-line gate summaries; the authoritative "When to Use", "Engine + Focus", and per-recipe VERIFY gate for each Recipe live here. Every recipe's VERIFY gate is **in addition to** Judge's universal FILTER discipline (every shipped finding VERIFIED/CONFIRMED + severity ≥ MEDIUM + concrete fix + not style-only + not mitigated; Claude review always via subagent; report-only no code mod; rejection ledger + SNR indicator emitted).

---

## Recipe table (authoritative When to Use + Engine + Focus)

| Recipe | Subcommand | Default? | When to Use | Engine + Focus | Read First |
|--------|-----------|---------|-------------|----------------|------------|
| Tri-Engine PR Review | `pr` | ✓ | Full diff review of an entire PR (Codex + Antigravity + Claude in parallel) | Tri-engine fan-out; apply cognitive-load gate + SNR optimization | `reference/tri-engine-review.md`, `reference/review-effectiveness.md` |
| Security-First | `security` | | CWE/OWASP focus, stricter checks on AI-generated code | Tri-engine fan-out + security focus; attach OWASP/CWE mapping to every finding; scrutinize AI-generated code | `reference/tri-engine-review.md`, `reference/codex-integration.md` |
| Perf Focus | `perf` | | Focus on N+1 / render cost / bundle size | Tri-engine fan-out + perf focus (N+1, render cost, bundle size) | `reference/tri-engine-review.md`, `reference/review-effectiveness.md` |
| Style Readability | `style` | | Naming and structure only (no bug flagging, Claude single engine) | Claude single-engine subagent; naming/structure/consistency only; no bug or security flags | `reference/code-smell-detection.md`, `reference/consistency-patterns.md` |
| Quick Check | `quick` | | <50 LOC low-risk, Claude single engine | Claude single-engine subagent; all findings treated as CANDIDATE and grounded | `reference/claude-review-usage.md` |
| Intent Alignment | `intent` | | Focus on alignment between code and PR body | Tri-engine fan-out + intent focus (PR body vs diff) | `reference/tri-engine-review.md`, `reference/review-anti-patterns.md` |
| Lean / Waste | `lean` | | Find over-engineering, YAGNI, dead code, redundancy — "make it leaner" | Tri-engine fan-out + lean focus (6 waste patterns); evidence-cited, not style; route to Void/Zen | `reference/lean-review.md`, `reference/code-smell-detection.md` |
| Pair Review | `pair` | | Conversational, fix-as-you-go improvement (secure + high-quality + lean) | Seed (any engine count) → one finding at a time → agree → spawn driver → re-verify; INTERACTIVE | `reference/pair-review.md`, `reference/fix-prompt-generation.md` |

---

## Per-Recipe VERIFY gates

- `pr`: Full diff review. **VERIFY**: dual-engine baseline actually spawned (Claude+Codex; agy added when AVAILABLE — not assumed); every finding carries an engine-concurrence tag and CANDIDATE (1/3 or 1/2) findings are grounded by reading real code before shipping; cognitive-load gate applied (>600 LOC → decompose before review, >1,000 refused); SNR ≥ 40% (else recalibrate); consensus findings ship a `## LLM Fix Prompt`; lean axis fires light — only HIGH/MEDIUM L1–L6 with airtight evidence, no boundary defense flagged, LOW lean → leanness-notes sub-list (`reference/lean-review.md`).
- `security`: CWE/OWASP focus, stricter on AI-generated code. **VERIFY**: every finding carries an OWASP/CWE mapping; absence-detection run (missing input validation / parameterized queries / output encoding / URL allowlists — the AI-code primary class); security FP-rate held < 3% ceiling; confirmed security findings routed to Sentinel (Judge stays surface-level, no deep threat-model in-recipe).
- `perf`: N+1 / render cost / bundle size focus. **VERIFY**: each finding is tied to a concrete cost signal (N+1 query count, render measurement, bundle bytes) — not speculative "looks slow"; grounded in actual code at GROUND; deep DB/SQL or measured-optimization work routed to Bolt/Tuner (Judge reports, does not optimize).
- `style`: Claude single-engine, naming/structure/consistency only. **VERIFY**: runs as a Claude **subagent** (never main-context self-review); zero bug/security findings emitted (out of this recipe's scope — escalate those to `pr`); every finding passes `style_bias_check` (reject rationale that reduces to "looks unfamiliar"); routed to Zen.
- `quick`: <50 LOC low-risk, Claude single-engine. **VERIFY**: scope confirmed <50 LOC low-risk (larger/high-risk → escalate to `pr`, do not stretch `quick`); runs as a Claude subagent; ALL findings treated as CANDIDATE and grounded before shipping (single-engine has no concurrence); self-grade-inflation guard — the evaluating model differs from the one that generated the code.
- `intent`: Code-vs-PR-body alignment. **VERIFY**: intent extracted from the PR/commit description first; each finding maps a concrete code-vs-stated-intent delta; scope-creep (code beyond the PR description) flagged explicitly; a structured `intent_alignment: PASS | FAIL | NOT_CHECKED` verdict is emitted (the Guardian `ship` gate signal); stays alignment-focused (pure bugs belong to `pr`, not `intent`).
- `lean`: Waste detection across the 6 patterns (over-engineering, YAGNI, dead code, speculative generality, redundancy, unnecessary dependency). **VERIFY**: every finding cites a verifiable cost (caller count / grep-confirmed non-reference / named duplicate `file:line` / unused param) — speculative "might not need later" rejected; `style_bias_check` passed (no "looks over-engineered"); **no boundary defense flagged as waste** (absence-detection invariant held — secure beats lean); behavior-preservation deferred to fix time (Judge reports, does not assert removal is safe); high-cost-of-keeping removals routed to Void, mechanical ones to Zen. Full gate → `reference/lean-review.md`.
- `pair`: Conversational fix-as-you-go (INTERACTIVE — the dialogue is the deliverable). **VERIFY**: findings presented **one at a time**, severity-ordered (no batch dump); each applied fix passed **explicit user agreement + a per-fix confirmation gate** before any driver spawn; the fix was made by a **driver agent distinct from Judge** (generator ≠ evaluator; propose-only fallback if no driver available — never self-fix); Judge **independently re-verified** each fix against the finding + a scoped regression check; modify/disagreement bounded to 2 turns/finding (anti-Agent-Tennis); session bounded by max-rounds (default 10) / user-stop / diminishing-returns, with remaining findings handed off as a standard report. Full contract → `reference/pair-review.md`.


---

## Per-Recipe VERIFY Gates (SKILL.md excerpt)

Per-Recipe `**VERIFY**` gates below are **in addition to** the universal FILTER discipline (see Workflow `FILTER` + Output Requirements). Full gate text → `reference/recipes-detail.md`.
- `pr`: dual-engine baseline spawned (agy only when AVAILABLE); concurrence-tagged, CANDIDATEs grounded; cognitive-load gate (>600 decompose, >1,000 refuse); SNR ≥ 40%; consensus → `## LLM Fix Prompt`; lean fires light (LOW → leanness-notes).
- `security`: OWASP/CWE per finding; absence-detection run; FP-rate < 3%; confirmed → Sentinel (no deep threat-model in-recipe).
- `perf`: each finding tied to a concrete cost signal (not "looks slow"); grounded at GROUND; deep/measured work → Bolt/Tuner.
- `style`: runs as a Claude subagent; zero bug/security findings; every finding passes `style_bias_check`; → Zen.
- `quick`: scope confirmed <50 LOC low-risk; Claude subagent; all findings CANDIDATE-grounded; self-grade-inflation guard.
- `intent`: intent extracted first; each finding a concrete code-vs-intent delta; scope-creep flagged; emit `intent_alignment: PASS | FAIL | NOT_CHECKED` (Guardian `ship` signal).
- `lean`: verifiable cost per finding; `style_bias_check` passed; no boundary defense flagged (secure beats lean); high-CoK → Void, mechanical → Zen.
- `pair`: findings one at a time, severity-ordered; agreement + per-fix confirmation before driver spawn; distinct driver (never self-fix); Judge re-verifies; bounded by max-rounds/user-stop/diminishing-returns.



---

## Recipe Dispatch Table (SKILL.md excerpt)

| Recipe | Subcommand | Default? | When to Use | Engine + Focus | Read First |
|--------|-----------|---------|-------------|----------------|------------|
| Tri-Engine PR Review | `pr` | ✓ | Full diff review of a PR | Fan-out; cognitive-load gate + SNR | `reference/tri-engine-review.md`, `reference/review-effectiveness.md` |
| Security-First | `security` | | CWE/OWASP focus, stricter on AI code | Security focus; OWASP/CWE per finding | `reference/tri-engine-review.md`, `reference/codex-integration.md` |
| Perf Focus | `perf` | | N+1 / render cost / bundle size | Perf focus | `reference/tri-engine-review.md`, `reference/review-effectiveness.md` |
| Style Readability | `style` | | Naming and structure only | Claude single-engine; no bug/security flags | `reference/code-smell-detection.md`, `reference/consistency-patterns.md` |
| Quick Check | `quick` | | <50 LOC low-risk | Claude single-engine; all findings grounded | `reference/claude-review-usage.md` |
| Intent Alignment | `intent` | | Code-vs-PR-body alignment | Intent focus (PR body vs diff) | `reference/tri-engine-review.md`, `reference/review-anti-patterns.md` |
| Lean / Waste | `lean` | | Over-engineering, YAGNI, dead code, redundancy | Lean focus (6 patterns); routes Void/Zen | `reference/lean-review.md`, `reference/code-smell-detection.md` |
| Pair Review | `pair` | | Conversational, fix-as-you-go | Seed → one at a time → agree → driver → re-verify; INTERACTIVE | `reference/pair-review.md`, `reference/fix-prompt-generation.md` |
