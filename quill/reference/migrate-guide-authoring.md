# Migration Guide Authoring Reference

Purpose: Write the migration / upgrade guide a downstream consumer needs to move from version X to version Y safely. A good guide lets the reader finish the upgrade without reading source code, without opening a support ticket, and without guessing which breaking changes apply to them.

## Scope Boundary

- **Quill `migrate`**: the document the consumer reads — version-jump guide, breaking-change catalog, deprecation timeline, codemod invocation steps, rollback instructions, verification checklist.
- **Shift (elsewhere)**: orchestrates the migration itself — writes the codemods, applies Strangler Fig / Branch by Abstraction patterns, runs before/after verification. Shift produces the executable change; Quill produces the human-readable explanation.
- **Atlas (elsewhere)**: the ADR that says *why* the breaking change was introduced. Link from the migration guide; do not duplicate the reasoning.
- **Scribe (elsewhere)**: internal spec documents (PRD / SRS). A migration guide targets external consumers, not the team spec-ing the change.
- **Zine (elsewhere)**: external-audience article series ("What changed in v4") for note / Zenn / Qiita / dev.to — narrative, not reference.

If the reader needs a step-by-step upgrade with rollback → `migrate`. If they need the story of the upgrade → Zine.

## Guide Archetypes

| Archetype | Pick when | Structure |
|-----------|-----------|-----------|
| Major version (X → X+1) | Breaking changes, codemod available | Overview → breakage → codemod → manual steps → verify → rollback |
| Minor version (X.Y → X.Y+1) | Non-breaking, new APIs replacing old | Deprecation notice → replacement path → timeline |
| Ecosystem upgrade (Node 18 → 20, React 18 → 19) | Platform / peer-dep shift | Compat matrix → peer updates → runtime changes → known issues |
| Fork / rename (moment → luxon) | Full replacement, not a version bump | Why → mapping table → codemod or manual path → gotchas |

Default: **Major version** structure — covers most breaking-change scenarios.

## Breaking-Change Notation

Every breaking change in the guide needs the same five fields so readers can scan and filter:

```markdown
### Breaking: `foo()` returns `Result<T>` instead of `T | null`

- **Scope**: affects every caller of `foo()`
- **Detect**: `rg "foo\(" src/` or TypeScript error `TS2322`
- **Before**: `const x = foo(id); if (x) { ... }`
- **After**: `const x = foo(id); if (x.ok) { ... x.value }`
- **Codemod**: `npx @pkg/codemod@1 foo-result` (covers ~85%, see gotchas)
- **Manual**: destructuring callsites, spread-into-object callsites
```

Readers filter by Scope, decide by Before/After, and act via Codemod or Manual.

## Deprecation Timeline

A deprecation timeline turns a surprise into a schedule. Pair every breaking change with a timeline block so users know when they must act.

```
v3.4  ──────────── old API available, no warning
v3.5  ─── ⚠ ────── old API emits deprecation warning (console + type)
v3.9  ─── 🔇 ───── old API enters "maintenance only" — no new features
v4.0  ─── ✂ ────── old API removed, codemod ships with release notes
```

Document dates when known, version ranges otherwise. Never announce a removal without also announcing the replacement.

## Codemod-Assisted Steps

When Shift has produced a codemod, the migration guide surfaces the command plus its honest coverage.

```markdown
## 1. Run the codemod

```bash
npx @pkg/codemod@1 v3-to-v4 --dry-run ./src
npx @pkg/codemod@1 v3-to-v4 ./src
```

**What it covers** (verified on internal repos):
- ✅ Direct `foo()` calls (≈85% of callsites)
- ✅ Imports from `@pkg/legacy`
- ✅ JSDoc `@see` / `@deprecated` tag rewrites

**What you still do by hand**:
- ❌ Destructuring callsites (`const { data } = foo()`)
- ❌ Dynamic calls (`api[name]()`)
- ❌ String-embedded module paths (config files)
```

Always show `--dry-run` before the destructive command. Always list the gotchas — a codemod that quietly misses 15% of callsites is worse than no codemod.

## Rollback Instructions

A migration guide that only goes forward fails the first time production regresses. Document rollback from day one.

```markdown
## Rollback

If you observe <regression signal> after the upgrade:

1. Revert dependency: `npm install @pkg@3.9.2` (last pre-v4).
2. Revert codemod: `git revert <codemod-commit-sha>` or apply `codemod-rollback.patch`.
3. Restore config: the `legacyMode` flag was removed in v4 — if you relied on it, fork the v3.9 branch until <target date>.
4. Report: file an issue with repro so v4.x can address the regression.
```

Rollback is time-boxed: state how long the old version will be supported. "Forever" is not a commitment.

## Parallel Old/New Semantics

When the old and new APIs coexist during the transition window, the guide must explain semantic differences — not just API shape.

| Behavior | v3 | v4 |
|----------|----|----|
| Empty input | returns `null` | returns `Result.err('EMPTY')` |
| Concurrent calls | last-write-wins | serialized per key |
| Error type | `string` | `{ code, message, cause }` |
| Timezone | local | UTC (breaking for log timestamps) |

A shape-only diff ("the return type changed") hides real bugs. Semantic diffs prevent silent drift.

## Verification Checklist

End every guide with a checklist the reader can run line-by-line. Generic success criteria ("your tests pass") are useless — specify observable signals.

```markdown
## Verify

- [ ] `npm test` passes with `@pkg@4.*`
- [ ] No console warning `DeprecationWarning: foo()` in CI logs
- [ ] No TypeScript error `TS6385` (deprecated symbol usage)
- [ ] Production error rate for endpoint `<path>` unchanged ±10% after rollout
- [ ] Log timestamps are now UTC (check first hour of post-deploy logs)
```

## Anti-Patterns

- ❌ Listing breaking changes without the Before / After pair — readers cannot act.
- ❌ Shipping a codemod claim without stating coverage percent and known gotchas.
- ❌ "Just upgrade and fix what breaks" — that is not a migration guide, that is abandonment.
- ❌ Omitting rollback because "v4 is better" — production does not care about your opinion.
- ❌ Bundling unrelated changes into one guide ("v4 + new CLI + new config format") — split by concern.
- ❌ Inventing deprecation timelines that nobody will honor — align with release cadence.
- ❌ Publishing the guide the day of release — drafts must ship with the deprecation warning, not the removal.
- ❌ Letting `@deprecated` JSDoc tags in the code contradict the guide — run a link-check between code tags and guide sections.

## Handoff / Next Steps

**From Shift → Quill (`migrate`):**
- Codemod name, version, invocation, coverage percent, and uncovered cases.
- Semantic differences Shift discovered during before/after verification.
- Rollback artifact (patch file, git tag, or reverse codemod).

**From Atlas → Quill (`migrate`):**
- ADR number that approved the breaking change — guide links back for the "why".

**From Quill (`migrate`) → Zine:**
- Once the guide is stable and adoption data exists, Zine authors an external-audience article summarizing the upgrade experience (adoption curve, common gotchas observed in the wild).

**From Quill (`migrate`) → Gear:**
- CI gate: fail the release if the migration guide section for this version is missing or still marked `#TODO(agent)`.
