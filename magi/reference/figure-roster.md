# Figure Roster

**Purpose:** The reusable knowledge asset — profiles of figures' documented thinking, so channeling is grounded and repeatable instead of re-researched every time.
**Read when:** You are in GROUND, or running `advisor roster` to author/refresh a profile.

## Storage

- Profiles: `.agents/magi/expert-roster/{figure-slug}.md` (e.g. `richard-feynman.md`)
- One file per figure. Slug is kebab-case of the documented name.
- Profiles are grounding aids, not authority. A profile never overrides the attestation rules in `attestation-tiers.md`.

## Profile schema

```yaml
---
name: Richard Feynman
slug: richard-feynman
status: deceased        # deceased | living-public | living-private
domain: [physics, pedagogy, problem-solving]
record_strength: strong # strong | moderate | thin
last_reviewed: 2026-06-26
---
```

Then, in the body, the thinking-model layers from `channeling-method.md`, each item sourced or marked `[inferred]`:

- **Mental models** — frameworks they reason with `[source]`
- **Heuristics** — quick rules `[source]`
- **Characteristic questions** — what they ask first `[source]`
- **Values / priorities** — what they optimize for `[source]`
- **Trade-offs accepted** — what they knowingly sacrifice `[source]`
- **Blind spots / known errors / reversals** — where criticized or wrong `[source]`
- **Vocabulary** — terms-of-art (paraphrase; no fabricated quotes)
- **Position log** — dated stances, so channeling can be date-scoped
- **Sources** — works, talks, interviews, papers used to build the profile

## Authoring rules (`advisor roster` variant)

- Every attribute carries a source or an explicit `[inferred]` marker. Unsourced ≠ silent.
- Set `record_strength` honestly: `thin` profiles cap channeling at SPECULATIVE/INFERRED.
- Date-scope positions; note reversals. A profile without a position log invites stale-position errors.
- Set `status` correctly — it drives the ethics handling in `ethics-and-safety.md`.
- Refresh trigger: review `living-public` figures when their documented positions may have shifted, **and `deceased` figures when new scholarship, primary sources, or corrected misattributions surface** — the record of a dead figure is not frozen. Bump `last_reviewed` on review.
- A profile is a grounding aid with a shelf life: at CHANNEL, surface stale `last_reviewed` or `thin` `record_strength` in the attestation rather than treating the profile as silent authority (`channeling-method.md` anti-caricature checklist).

## Seed exemplars (illustrative — verify before use)

These are starting points, not authority. Channel only what you can attest.

| Figure | Domain | Signature frameworks (illustrative) |
|--------|--------|-------------------------------------|
| Richard Feynman | physics, learning | First-principles derivation; "if you can't explain it simply…"; teaching-as-understanding |
| Charlie Munger | investing, decisions | Latticework of mental models; inversion; circle of competence |
| Clayton Christensen | innovation strategy | Jobs-to-be-done; disruptive vs. sustaining innovation |
| Dieter Rams | product design | Ten principles of good design; "less, but better" |
| Barbara Minto | communication | Pyramid Principle; SCQA structuring |

When a requested figure has no profile and the record is reachable, build a lightweight one inline at GROUND and offer to persist it as a roster file.
