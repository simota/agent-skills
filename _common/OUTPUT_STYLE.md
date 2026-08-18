# Output Density Protocol — OUTPUT_STYLE.md

> Single source of truth for **runtime output style** across all skills.
> Owner: Architect. Referenced from every SKILL.md `Output Contract` section.
> Distinct from `architect/reference/context-compression.md` (which targets SKILL.md file size, not response density).

Skills inherit these rules so each agent does not re-invent its own output style. Combine with the per-skill `Output Contract` section in SKILL.md.

---

## Why This Exists

Opus 5 calibrates verbosity to task complexity (`OPUS_5_AUTHORING.md` P2), but without a shared style baseline each skill drifts. Symptoms in the wild:

- Filler preamble before the actual answer ("Let me now…", "I'll proceed to…")
- Restating the user's request in different words
- Closing summaries that repeat what the diff already shows
- SKILL.md section headers mirrored back as response headers
- Prose where a 3-row table would carry more signal

This file defines **what to remove** and **what to choose instead**, with measurable criteria.

---

## Output Tiers

Every skill has a default tier — declared in its `## Output Contract`, or inherited as `M` when it has none (§ Inherited default). A skill MUST pick the smallest tier that fully answers the task.

| Tier | Lines | Use For | Example |
|------|-------|---------|---------|
| `S` | 1–3 | Lookup, status, yes/no, single-fact answer | "ファイルは `src/auth.ts:42` にあります。" |
| `M` | 5–15 | Typical task: plan, finding, short fix, single review | Bug RCA summary, quick refactor proposal |
| `L` | 30–80 | Deliverable, structured doc, multi-section finding | Design proposal, audit report |
| `XL` | 80+ | Full document: spec, design, comprehensive review | PRD, RFC, architecture doc |

### When in doubt, choose smaller

- Default to one tier below your first instinct.
- If the user can ask "more detail please" with one keystroke, the cost of starting smaller is near zero.
- Tier ceilings are advisory caps; the floor matters more — never pad to fill a tier.

### Inherited default

A skill with no `## Output Contract` section **inherits `M`**. There is no undeclared tier — an absent contract is a declaration of `M`, not a licence for unbounded output.

Declare an explicit contract only to state something the inherited default does not: a different default tier, per-task overrides, or domain bans. Skills whose deliverable is an inherently long structured document delivered *in the response* declare `L`; skills that write the deliverable to a file stay `M` and summarize (the document lives in the file, not in the reply).

---

## Banned Patterns

These never carry signal. Remove on sight.

### 1. Preamble fillers

```
✗ "Let me analyze this for you."
✗ "I'll now proceed to..."
✗ "まず、ご依頼の内容を確認します。"
✓ (skip — start with the answer or first action)
```

### 2. Request restatement

```
✗ "You asked me to refactor the auth module. I'll refactor the auth module."
✓ (skip — the user knows what they asked)
```

### 3. Tautological closers

```
✗ "I have completed the refactoring as requested."
✗ "以上で対応は完了です。"
✓ End with what's *next*, what's *unverified*, or simply stop.
```

### 4. Hedging stacks

```
✗ "It seems that perhaps possibly the issue might be in the parser."
✓ "原因は parser。"  ← state it; if uncertain, say so once.
```

### 5. Header echo

If the SKILL.md has sections `Analysis / Proposal / Risks`, do NOT auto-emit those three headers in every response. Headers are for L/XL tier only.

### 6. Same-meaning repetition

```
✗ "簡潔かつ明瞭に" / "fast and quick" / "robust and resilient"
✓ Pick one word.
```

### 7. Capability advertising

```
✗ "As an AI agent specialized in X, I can help with Y..."
✓ Just do Y.
```

---

## Conditional Requirements

A SKILL.md `## Output Requirements` list describes what a **complete deliverable** carries. It is a ceiling for the largest form of the task, not a floor every turn must reach.

- **Emit only the items the task actually exercised.** A refactor that touched no configs has no config row; a lookup that produced no fix has no fix section.
- **Never pad to satisfy the list.** `N/A`, "none identified", "not applicable in this case", and empty table shells are filler — deleting them loses no information (Banned Pattern §1 applies).
- **Collapse empty envelope sections to one line, or drop them.** An empty ledger is `Residuals: none`, never a header plus a header-only table.
- **Required-in-substance ≠ required-in-shape.** When a protocol says a ledger is non-optional, that binds the *content* when content exists; the scaffolding is not the obligation.
- **Scale the envelope to the task, not to the schema.** A SIMPLE task reports in the schema's short form; the full form is for the work that filled it.

This rule is inherited by every skill. A SKILL.md may carry the one-line marker at the head of its `## Output Requirements` list — the point where the mandate is read — but must not reproduce the bullets above.

---

## Format Priority

When data is structured, **don't prose it**. Order of preference:

```
table  >  bulleted list  >  numbered list  >  prose
```

| Data shape | Use |
|-----------|-----|
| Comparison across ≥3 attributes | Table |
| Sequence of steps | Numbered list |
| Independent items | Bulleted list |
| Single-thread reasoning | Prose (≤3 sentences) |
| Code, paths, commands | Code block / inline backticks |

### Density rules

- **1 bullet = 1 claim.** No ", and also" inside a bullet.
- **Paragraphs ≤ 3 sentences.** More → list.
- **Tables ≤ 7 rows visible.** More → reference file.
- **No nested bullets past depth 2.** Flatten or section.
- **Inline code over fenced** for single tokens (`auth.ts` not a code block).

---

## Tier-Specific Rules

### S tier (1–3 lines)

- No headers, no lists, no closers.
- Lead with the answer; cite path:line if applicable.
- If a question has no answer, say so in one line.

### M tier (5–15 lines)

- At most one short header (often none).
- Use a 3–5 row table or bullet list when ≥3 distinct items.
- Close with the next action only if non-obvious.

### L tier (30–80 lines)

- 2–4 headers max.
- Mix dense (table) and sparse (1-line principle) blocks (Ma rhythm — see `architect/reference/context-compression.md` §Ma).
- Open with a 1-paragraph TL;DR before sections.

### XL tier (80+ lines)

- Apply Ma layout (Zone 1/2/3/4).
- Every section must justify its existence; if a section fits in 2 lines, fold it elsewhere.
- Provide a contents list at the top if >150 lines.

---

## Self-Audit Before Sending

Three-question check the model runs internally before emitting:

1. **Filler?** Is there a sentence that, if deleted, the user loses no information?
2. **Structure?** Is any 3+ line prose block actually a table or list in disguise?
3. **Tier?** Could one tier smaller still answer the question?

If yes to any → cut.

---

## Domain Overrides

Specific skills may add domain-banned phrases in their `Output Contract`. Examples:

- **Investigators (Scout/Lens/Trail):** never emit "I think" without evidence — say "evidence: …" or "unverified: …" instead.
- **Reviewers (Judge/Gauge/Sentinel):** never restate the file under review; reference by path:line.
- **Builders (Builder/Artisan/Forge):** never narrate code being written — let the diff speak.
- **Designers (Vision/Muse/Palette):** prefer parametric output (`_common/parametric-output.md`) over single-value declarations.

---

## Subagent Completion Pattern (universal ban)

Reports returned from the `Agent` tool (any `subagent_type`, including `general-purpose`) MUST NOT open with completion-announcement preamble. The fact that the subagent finished is **implicit** in the act of returning text — stating it adds zero signal.

**Banned openers (do not emit):**

```
✗ "All work is complete. Here's the summary report."
✗ "X が完了しました。最終レポートを返します。"
✗ "十分な調査が完了しました。350語以下で構造化されたレポートをまとめます。"
✗ "Successfully completed the task. Below is the summary."
✗ "全ての変更を適用しました。以下に結果をまとめます。"
```

**Open instead with the first deliverable line:**
- a `## ` section header that names the deliverable
- a table header
- the lead finding ("V4 のバックスラッシュエスケープは 0 件。`_common` リンクもクリーン。")
- a `_STEP_COMPLETE` / handoff envelope directly (no prose preamble before it)

**Why this matters:** Subagent reports are read in batch by an orchestrator (Architect, Nexus, the user). Completion preamble is filler that orchestrators ignore — but it costs tokens and pushes the actual deliverable below the attention fold.

This rule applies even when the skill's `Output Contract` does not explicitly mention it; subagent invocations inherit OUTPUT_STYLE universally.

---

## Interaction with Existing Protocols

| Protocol | Relationship |
|----------|-------------|
| `OPUS_5_AUTHORING.md` P2 | This file is the implementation. P2 says "calibrate length"; OUTPUT_STYLE says how. |
| `architect/reference/context-compression.md` | Different target: that file compresses SKILL.md; this file shapes runtime responses. |
| `_common/parametric-output.md` | Compatible. Parametric blocks are valid M/L tier content. |
| `_common/AUTORUN.md` | `_STEP_COMPLETE` and `NEXUS_HANDOFF` blocks are exempt from tier limits — they have their own envelopes. |

---

## How to Reference This File

In a SKILL.md `Output Contract` section:

```markdown
## Output Contract
- Default tier: M (5-15 lines per turn)
- Style: `_common/OUTPUT_STYLE.md`
- Task overrides:
  - `validate` → S
  - `generate-spec` → L
- Domain bans: <skill-specific banned phrases, if any>
```

Cite by tier and rule ID (e.g., "Banned Pattern §3"); don't duplicate the rule text inside individual SKILL.md files.

---

## Validation Hooks

Skills validating against ODP must pass:

- **R8.1** Output Contract section exists in SKILL.md, **or** the skill inherits the `M` default and needs no override (see § Inherited default). A contract that only restates `M` with no overrides and no domain bans is redundant and fails R8.1 for the opposite reason.
- **R8.2** Default tier declared (S/M/L/XL) when a contract is present.
- **R8.3** OUTPUT_STYLE.md is referenced (not duplicated) — including § Conditional Requirements.
- **R8.4** Task overrides table present when the skill has ≥2 distinct task types **and** they differ in tier.

See `architect/reference/validation-checklist.md` Section 8.
