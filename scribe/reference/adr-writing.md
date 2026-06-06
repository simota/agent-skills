# ADR Writing Reference

Purpose: Author an Architecture Decision Record (ADR) that captures a single significant architectural decision, the forces behind it, and the consequences it creates. An ADR is a dated, numbered, immutable artifact — once accepted, it is never edited; it is superseded.

## Scope Boundary

- **Scribe `adr`**: the GENERAL ADR-writing recipe. Any agent or human can invoke it to document a decision (tool choice, protocol, process, data model, naming convention, policy). Covers Nygard and MADR formats, numbering, status lifecycle, supersede chain, and review handoff.
- **Atlas (elsewhere)**: owns application/module-level architecture decisions — dependency direction, layer boundary, pattern selection, circular-reference remediation. Atlas performs the tradeoff analysis and authors ADRs for those decisions directly.

If the question is "what are the tradeoffs of moving module A under domain B?" → `Atlas`. If the question is "we have already decided X, write it up as an ADR" → Scribe `adr`.

## Format Selection

| Format | Pick when | Skip when |
|--------|-----------|-----------|
| Nygard (Title / Status / Context / Decision / Consequences) | Default. Small team, short decisions, lightweight process. | Decision needs explicit option comparison with pros/cons per option. |
| MADR 3.0 (Markdown Any Decision Records) | Multiple options evaluated, compliance requires explicit alternatives. | Single-option no-brainer — MADR headers become noise. |
| Y-Statement (one-liner) | Team-internal quick call, not publication-grade. | External stakeholders will read it. |

Default: **Nygard**. Switch to MADR when ≥2 alternatives deserve a named comparison.

## Workflow

```
UNDERSTAND  ->  confirm the decision is made (ADRs record, not explore)
            ->  identify owner, reviewers, date
            ->  locate docs/adr/ and scan the highest existing number

STRUCTURE   ->  assign ADR-NNNN (zero-padded, sequential, never reused)
            ->  pick Nygard vs MADR
            ->  draft supersede chain if this replaces prior ADRs

DRAFT       ->  Title: short imperative ("Use Postgres for primary store")
            ->  Status: Proposed | Accepted | Deprecated | Superseded by ADR-NNNN
            ->  Context: forces, constraints, non-negotiables. Avoid prescribing the solution here
            ->  Decision: start with "We will ..." — use RFC 2119 MUST / SHOULD / MAY
            ->  Consequences: positive, negative, neutral. Include what becomes easier AND harder

REVIEW      ->  decision is testable (you can point at code or config that honors it)
            ->  consequences include at least one negative (no "all upside" ADR passes review)
            ->  supersede chain is bidirectional (old ADR gets Superseded-by footer)

FINALIZE    ->  commit under docs/adr/ADR-NNNN-kebab-title.md
            ->  update docs/adr/README.md index if present
            ->  announce to affected teams; status flips Proposed -> Accepted at sign-off
```

## Immutability Principle

An accepted ADR is a historical record. Do not edit it to reflect a changed decision.

- Fixing a typo or broken link: acceptable.
- Adding "we changed our minds" in the body: forbidden — author a new ADR and set the old one to `Superseded by ADR-NNNN`.
- Deleting an obsolete ADR: forbidden — deprecation is part of the record.

This is what makes ADRs valuable under version control: `git blame` of an ADR is meaningful because the ADR does not drift.

## Supersede Chain

When a new ADR replaces an old one:

1. New ADR header: `Supersedes ADR-0007`.
2. Old ADR status flips: `Superseded by ADR-0021 (YYYY-MM-DD)`.
3. Context of the new ADR cites why the old decision no longer holds (changed constraints, scaled beyond threshold, vendor change).
4. Do not delete the old ADR.

Chains longer than 3 deep on the same topic are a signal to write a `topic overview` doc that links the chain.

## Anti-Patterns

- Writing an ADR as exploration ("we are considering ..."). ADRs record decisions. Use a design doc or `Magi` deliberation for exploration.
- Decision section prescribing implementation detail ("use `pg` npm package v8.11.3"). Keep to architectural level; pin versions in the package manifest, not the ADR.
- Consequences listing only benefits. Every real decision has a cost; absence of costs signals shallow analysis.
- Renumbering ADRs after a deletion. Numbers are immutable identifiers, not positions.
- ADR with no owner and no reviewers. Orphan ADRs rot.
- Mixing multiple decisions ("use Postgres AND switch to gRPC"). One decision per ADR — traceability breaks otherwise.

## Required Header Fields

```markdown
# ADR-0012: Use Postgres for primary operational store

- Status: Accepted
- Date: 2026-04-24
- Deciders: @owner, @reviewer-1, @reviewer-2
- Supersedes: ADR-0007 (optional)
- Superseded-by: ADR-NNNN (added later if applicable)
- Tags: storage, primary-db
```

## Handoff

- From `Atlas`: Atlas completes tradeoff analysis and hands off a decision package; Scribe `adr` formats it as a publishable ADR if Atlas did not author directly.
- From `Magi`: deliberation concluded, Scribe records the chosen path.
- From `Accord`: cross-team alignment reached, Scribe captures the agreement as an ADR.
- To `Scribe` HLD/LLD: HLDs reference relevant ADRs by number rather than restating the decision.
- To `Sherpa`: if the ADR triggers implementation work, decompose downstream tasks.

## ADRs in the SDD Era (2026)

When the codebase ships a Spec-Driven Development harness (Spec-Kit, cc-sdd, BMAD, Tessl, Kiro, OpenSpec) the ADR's role narrows: it documents the **architectural decision**, not the **project constitution**. The two are different artefacts and must not be conflated.

| Artefact | Mutability | Scope | Read by |
|----------|------------|-------|---------|
| **ADR** | Immutable once Accepted; superseded by a new ADR | One named decision | Humans during code review; agents when the decision is cited by a PRD or HLD |
| **`CLAUDE.md` / `AGENTS.md` (project constitution)** | Living document; PRs welcome | Org-wide / repo-wide conventions, testing policy, file layout, code-style non-negotiables | Every AI coding agent on every turn |
| **PRD spec** | Versioned; usually replaced for the next iteration | One feature | Agent during `/specify`, `/plan`, `/tasks` |

Rules of thumb:

- A decision that affects *every* future PR (e.g., "this repo uses Postgres, not MySQL") belongs in **both**: an ADR that records the *decision* and a `CLAUDE.md` / `AGENTS.md` line that operationalises it for agents. The ADR explains *why*, the constitution tells the agent *what*.
- A decision that affects only one feature (e.g., "for this onboarding flow we use a state machine") stays in the PRD or HLD, not in an ADR.
- If you find yourself editing an Accepted ADR to keep `CLAUDE.md` in sync, you have miscategorised the change. Add a new ADR for the new decision, then bump `CLAUDE.md`.

When a new ADR supersedes an old one, **also update the constitution line** that referenced the old decision — otherwise agents continue applying the obsolete rule until someone notices the drift in code review.

## Citations

- Michael Nygard, *Documenting Architecture Decisions* (2011) — original Nygard format.
- MADR 3.0 — https://adr.github.io/madr/
- RFC 2119 — MUST / SHOULD / MAY keyword definitions.
- ISO/IEC/IEEE 42010:2022 — architecture description practices, including rationale capture.
- GitHub Spec-Kit (2026) and the cc-sdd / Kiro / BMAD ecosystems — for the constitution vs ADR vs spec separation summarised above.
