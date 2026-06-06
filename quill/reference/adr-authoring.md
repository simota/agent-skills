# ADR Authoring Reference

Purpose: Capture an architectural decision with enough context, alternatives, and consequences that a reader in six months can reconstruct the reasoning without interviewing the author. An ADR is a lightweight, code-adjacent artifact — one decision, one file, immutable once accepted.

## Scope Boundary

- **Quill `adr`**: code-adjacent ADR file creation (Nygard / MADR template), supersession lifecycle, index maintenance, cross-linking from JSDoc / README.
- **Atlas (elsewhere)**: the upstream architecture analysis, RFC drafting, dependency / coupling evaluation that *produces* the decision Quill records.
- **Scribe (elsewhere)**: PRD / SRS / HLD / LLD specification documents that describe the product and design surface, not a single decision point.
- **Zine (elsewhere)**: external-audience tech-blog article series discussing decisions after the fact, for publication on note / Zenn / Qiita / dev.to.
- **Shift (elsewhere)**: orchestrating the migration that an accepted ADR unlocks.

If the task is "decide between Postgres and DynamoDB" → Atlas. If the decision is already made and must be recorded → `adr`. If the decision needs a narrative blog post for external readers → Zine.

## Template Selection

| Template | Pick when | Skip when |
|----------|-----------|-----------|
| Michael Nygard (Context / Decision / Status / Consequences) | Team new to ADRs, lightweight PRs, decisions that fit on one screen | Multiple serious alternatives need side-by-side comparison |
| MADR 4.0 (full) | Multiple alternatives, compliance / audit trace, distributed team | Single obvious choice, trivial scope |
| MADR 4.0 (short) | Middle ground — documented alternatives but compact | Decision warrants a full pros/cons matrix |
| Y-Statement (one-liner) | Micro-decision captured inline, not a standalone file | Any decision a new hire would need to understand |

Default: **MADR short** — keeps alternatives visible without Nygard's minimalism dropping that history.

## Core Sections (MADR-aligned)

```markdown
# ADR-NNNN: <decision in imperative form>

- Status: Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
- Date: YYYY-MM-DD
- Deciders: <names or roles>
- Consulted: <names or roles>
- Informed: <names or roles>

## Context and Problem Statement
<1–3 paragraphs. What forces us to decide now? What constraints are non-negotiable?>

## Decision Drivers
- <driver 1, e.g., cost ceiling, latency SLO, team skill>
- <driver 2>

## Considered Options
- Option A
- Option B
- Option C

## Decision Outcome
Chosen option: "Option B", because <one-paragraph justification tied to drivers>.

### Consequences
- Positive: <what improves>
- Negative: <what gets worse or what we're giving up>
- Neutral: <changes in shape but not in quality>

## Pros and Cons of the Options
### Option A
- Good: …
- Bad: …
### Option B
- Good: …
- Bad: …
```

## Status Lifecycle

```
Proposed ──(review)──▶ Accepted ──(time)──▶ Deprecated
                           │
                           └──(new ADR)──▶ Superseded by ADR-XXXX
```

Rules:

- **Never edit an Accepted ADR's decision body.** Fix typos only. If the decision changes, write a new ADR that supersedes it and update the old one's Status line.
- **Superseded** means "this decision no longer applies"; keep the file for history.
- **Deprecated** means "the system this decision governed is gone"; keep the file for archaeology.
- A decision never regresses from Accepted to Proposed. If reopened, that's a new ADR.

## Indexing

Maintain `docs/adr/README.md` (or `docs/adr/index.md`) with:

| ADR | Title | Status | Supersedes | Superseded by |
|-----|-------|--------|------------|---------------|
| 0001 | Record architecture decisions | Accepted | — | — |
| 0002 | Use Postgres for primary store | Superseded | — | 0014 |
| 0014 | Move primary store to Aurora | Accepted | 0002 | — |

Generate / refresh this table as part of the `adr` recipe — an unindexed ADR directory rots fast.

## ADR vs RFC vs Design Doc

| Artifact | Audience | Timing | Immutable? |
|----------|----------|--------|------------|
| ADR | Future maintainers of this codebase | After decision is made | Yes (supersede to change) |
| RFC | Team being asked to agree | Before decision is made | No (revised during review) |
| Design Doc / HLD | Implementers of the feature | During design | No (updated as design evolves) |

If the document is still gathering signatures → it's an RFC, route to Atlas. Only write an ADR when the decision is crossing the "accepted" boundary.

## Anti-Patterns

- ❌ Writing an ADR as a task checklist or implementation plan — that's a design doc, not a decision.
- ❌ Omitting rejected alternatives — "we chose X" without "over Y and Z" makes the decision unreviewable.
- ❌ Editing an Accepted ADR's decision or consequences in place — breaks audit trail; supersede instead.
- ❌ Burying the status — readers must see Accepted / Superseded in the first five lines.
- ❌ One ADR bundling three unrelated decisions — split into three files with cross-links.
- ❌ Numbering gaps (ADR-0007 missing) — either reserve the number or never use it; do not reuse.
- ❌ Writing only positive consequences — if Negative is empty, the decision was not analyzed honestly.
- ❌ Letting the index drift — a stale `docs/adr/README.md` is worse than none.

## Handoff / Next Steps

**From Atlas → Quill (`adr`):**
- The accepted decision in one sentence.
- Drivers and constraints Atlas already evaluated.
- The list of considered options with Atlas's pros/cons.
- Supersession target (which existing ADR, if any, this replaces).

**From Quill (`adr`) → Shift:**
- ADR number + URL for the migration to cite.
- Consequences section flags (breaking changes, deprecation timeline) that Shift will orchestrate.

**From Quill (`adr`) → Canvas:**
- Request a component / context diagram if the decision shifts system boundaries — ADR references the diagram, not the other way around.

**From Quill (`adr`) → Zine:**
- Once the ADR is Accepted and the migration has landed, Zine can author an external-audience retrospective article that links back to the ADR as the canonical record.
