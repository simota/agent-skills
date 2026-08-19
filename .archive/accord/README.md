# Accord Archive And Reactivation

## Archive Record

- Archived: 2026-08-19
- Reason: Accord's cross-team unified-specification capabilities were consolidated into Scribe's `unified` recipe; `vision`, `requirements`, `detail`, `ac`, `story-map`, `stakeholder`, and `raci` remain compatibility modes.
- Active owner: `scribe/SKILL.md`
- Active references: `scribe/reference/unified-spec/`
- Reactivation window: 2026-08-19 through 2026-11-17 (90 days)

The archived `SKILL.md` and `reference/` files are retained unchanged as a rollback source. Active skills must not load files from `.archive/accord/`.

## Reactivation Criteria

Reactivate Accord only when runtime evidence shows that Scribe cannot preserve one or more of these distinct outcomes without material routing ambiguity or quality loss:

- one shared Biz/Dev/Design source of truth
- staged `L0 -> L1 -> L2 -> L3 -> L4` elaboration
- Full/Standard/Lite scope selection and traceability thresholds
- collaborative BDD / Three Amigos review
- story mapping, stakeholder mapping, or RACI/DACI/RAPID governance
- downstream executable-spec handoffs

Preference, naming familiarity, or an unverified concern is not sufficient evidence.

## Reactivation Procedure

1. Capture failing Scribe examples and identify the non-preserved capability.
2. Confirm the problem cannot be fixed inside `scribe/reference/unified-spec/` without restoring role overlap.
3. Move this directory back with `git mv .archive/accord accord`.
4. Restore active Accord routing/profile references and remove any conflicting Scribe route.
5. Run frontmatter, local-link, recipe, routing, and task-battery validation before enabling the skill.
6. Record whether the reactivation is permanent or a time-boxed experiment.

After 2026-11-17, removal of this archive requires a separate evidence-based sunset decision; it is not automatic.
