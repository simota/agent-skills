# Gap Report (Gap mode output)

**Purpose:** Minimal structure for the artifact Compass emits when no skill fits a request (Gap mode), so the LADDER's compass step produces a verifiable output instead of a bare "no match" statement.
**Read when:** Running Gap mode (no matching skill found during `recommend` / `classify`).

## Structure

```markdown
## Gap Report
Unmatched input: [the user's request, verbatim or lightly paraphrased]
Nearest skills:
- [skill-1]: [why it doesn't fit — the specific capability/scope gap]
- [skill-2]: [why it doesn't fit]
- [skill-3]: [why it doesn't fit] (omit if fewer than 3 skills are plausibly close)
Next action: [propose-new-skill (hand off to Architect via `COMPASS_TO_ARCHITECT`) | generic-execution (no skill class fits; proceed ad-hoc) | boundary (the act is outside what any skill may perform — e.g. licensed-human-only filings; see `nexus/reference/routing-matrix.md` LADDER non-closable-gap note)]
```

Every field is required — an empty "Nearest skills" list (zero candidates considered) or a missing "Next action" makes the report unverifiable and defeats the point of Gap mode.

## Handoff

`propose-new-skill` → send the Gap Report as the payload of `COMPASS_TO_ARCHITECT` (see `compass/SKILL.md` § Collaboration). Architect returns a gap-fill proposal or declines with a reason; either way the LADDER's `fallback_taken` field records the outcome (`architect-invoked`).
