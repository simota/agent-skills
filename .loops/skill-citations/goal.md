# Goal: Apply Source Citations from skill-update Loop

## Objective

Apply the 22 source-citation MID proposals surfaced by the `skill-update` loop's IMPROVE pass. For each affected skill, add a verifiable `[Source: ...]` citation to the relevant SKILL.md or reference/*.md, with the source URL recovered via WebFetch and validated against `_common/WEB_FETCH_SAFETY.md` injection checks.

## Why

Source-attribution improves trust, freshness signals, and reviewer auditability. The `skill-update` IMPROVE loop applied HIGH-priority fixes but deferred 240 MID-tier proposals; 22 of those are pure citation additions — small, low-risk edits that benefit from automated batch application.

## Scope

- Input file: `citations-todo.md` (22 skills with their proposed citations)
- Per iteration: 4 skills (smaller batch — citation work needs careful URL verification)
- **Read-write mode** restricted to the per-iteration batch's SKILL.md / reference/*.md
- WebFetch / WebSearch encouraged (max 2 calls per skill) to recover canonical URLs
- WEB_FETCH_SAFETY injection check **mandatory** for every fetched URL

## Acceptance Criteria

| ID | Criterion | Verification |
|----|-----------|--------------|
| C1 | Each of the 22 skills has at least one `[Source: <url>]` or `[Source: <publisher> — <title>]` citation added | `verify.sh check-citations` |
| C2 | No regression in AC1/AC2/AC4 (skill-update verifier) | `verify.sh check-no-regression` |
| C3 | Every URL added carries an `injection-check: PASS / SOFT / STRONG-rejected` annotation in `reports/citations-applied.md` | `verify.sh check-injection-annotations` |
| C4 | `state/skills-pending.txt` is empty at completion | `verify.sh check-pending-empty` |

## Out of Scope

- Editing skills outside the 22-skill list
- Editing `_common/`, `_templates/`, `.agents/`, `.loops/`
- Creating new files in `reference/`
- Applying any non-citation MID/LOW proposals

## Rollback

Per-iter regression guard via `git checkout HEAD --` if AC1/AC2/AC4 dead counts increase. Branch isolation on `feat/skill-update-loop` (or successor branch).
