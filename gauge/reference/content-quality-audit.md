# Content Quality Audit (CQ items)

Two content-level checks complementing the 19 structural items (F1, F2, L1, H1-H3, S1-S11, A1-A2).
Source: Anthropic Engineering, "Lessons from Building Claude Code: How We Use Skills" (2026).

Structural items verify that the SKILL.md *looks* right.
Content items verify that the SKILL.md *says* something the model would not already do.

---

## CQ1 — Obviousness Density

**Definition**: Proportion of lines that restate default programming knowledge the model already exhibits without the skill.

**Why it matters**: Obvious content wastes context, dilutes high-signal directives, and trains the model to skim the skill rather than apply it.

### Detection signals

A line is flagged as *obvious* when it matches one or more:

| Signal | Example |
|--------|---------|
| Generic language tip | "Use `const` instead of `var` in JavaScript." |
| Universal good-practice | "Write tests for your code." |
| Tautological framing | "Bugs should be fixed." |
| Restated tool description | "The `grep` command searches files." |
| Empty hedge | "Be careful when modifying production code." |

A line is *not* obvious when it:

- Names a project-specific path, identifier, or convention.
- Records a non-default behavior the model would otherwise miss.
- Captures a system-specific quirk (auth flow, env divergence, append-only table).
- Contains a measurable threshold, deadline, or limit.

### Scoring

| Density (obvious lines / total non-frontmatter lines) | Verdict | Priority |
|--------------------------------------------------------|---------|----------|
| < 5% | PASS | — |
| 5% - 15% | PARTIAL | P2 |
| > 15% | FAIL | P1 |

Apply 2-of-3 corroboration (Gauge Core Contract): single-pattern hits enter the soft-flag queue.

### Fix template

For each flagged line, propose one of:

1. **Delete** — line carries no project-specific signal.
2. **Specialize** — rewrite with concrete file path, threshold, or system name.
3. **Promote to Gotchas** — if the line records a real trap, move it to the `## Gotchas` section.

---

## CQ2 — Description Trigger-Word Presence

**Definition**: The frontmatter `description` field is written for *model discovery* (when to fire this skill), not as a human summary.

**Why it matters**: The model reads `description` first to decide whether to load the skill. Human-summary prose ("This skill helps you …") does not anchor activation intent.

### Detection signals

A description is *trigger-anchored* when it contains:

| Signal | Example |
|--------|---------|
| Activation verb at start | "Use when …", "Trigger when …", "Run after …" |
| Concrete invocation keywords | "babysit", "audit", "rotate", "ship", "rollback" |
| Negative routing ("don't use for") | "Don't use for X (Agent), Y (Agent)." |
| Domain noun list | "PRs, CI status, release notes, changelog." |

A description is *under-anchored* when it:

- Starts with "This skill …" or "Helps with …".
- Describes the agent's persona without a trigger.
- Lists capabilities in vendor-marketing voice ("powerful", "comprehensive").
- Lacks any of the four signals above.

### Scoring

| Trigger-signal count | Verdict | Priority |
|----------------------|---------|----------|
| 3+ signals present | PASS | — |
| 1-2 signals present | PARTIAL | P2 |
| 0 signals present | FAIL | P1 |

### Fix template

Rewrite as:

```
description: "<gerund/verb activation phrase>. Use when <concrete signal 1>, <concrete signal 2>, or <concrete signal 3>. Don't use for <X> (<OtherAgent>)."
```

Reference exemplar: Architect, Sigil, and Chain descriptions in the current ecosystem.

---

## Audit invocation

`gauge audit` runs CQ1 and CQ2 alongside the 19 structural items.
`gauge checklist CQ1` or `gauge checklist CQ2` narrows to a single content item.

Both items respect the change-budget and self-evolution Safety Levels defined in `self-evolution.md`.

---

## False-positive guards

- **CQ1**: Skip lines inside fenced code blocks, frontmatter, and `<!-- HTML comments -->`. Skip the closing motto line ("> ...").
- **CQ1**: Do not flag rationale lines that explicitly justify a non-default choice ("**Why:** …", "**Rationale:** …").
- **CQ2**: A description that intentionally omits the trigger because the skill is invoked via Recipe subcommand only (e.g., always routed by Nexus) may waive CQ2 with a top-line HTML comment `<!-- CQ2-waived: Recipe-only invocation -->`.

---

## Provenance

These items derive from Anthropic Engineering, "Lessons from Building Claude Code: How We Use Skills" (2026, T1 source). The article identifies "Avoid Obviousness" and "description as model-discovery trigger" as two of the highest-impact principles observed across hundreds of internal skills.
