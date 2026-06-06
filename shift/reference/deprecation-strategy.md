# Deprecation Strategy Reference

Purpose: Orchestrate the sunset phase of a feature, API, or public interface — from deprecation announcement to safe removal — with telemetry-driven evidence, documented migration paths, and a reversible removal playbook. This is the "how to remove it safely" recipe; decisions about *whether* to remove live elsewhere.

## Scope Boundary

- **Shift `deprecate`**: orchestrates the sunset phase — deprecation period design, usage telemetry, Sunset header, removal playbook, client migration docs.
- **Void**: proposes *what* to cut (YAGNI, scope trimming). Void's output is the input to `deprecate` when the candidate is a shipped/public surface.
- **Launch**: owns release/version strategy — semver decisions, CHANGELOG, release notes. `deprecate` feeds Launch the deprecation-notice content and the removal-release target.
- **Horizon**: detects *our own* reliance on deprecated third-party surfaces. `deprecate` governs *our* surfaces that others rely on.
- **Shift `migrate` / `framework` / `lang`**: execute the caller-side migration away from something deprecated. `deprecate` runs the provider-side sunset.

If the question is "should we delete this?" → Void. If it is "we decided to delete it, how do we wind it down without breaking callers?" → `deprecate`.

## Deprecation Period Design

Length is a function of caller diversity and criticality, not a default.

| Surface | Recommended minimum period | Rationale |
|---------|----------------------------|-----------|
| Internal API, same team | 2 weeks | Refactor coordinated in-team |
| Internal API, cross-team | 1–2 quarters | Backlog alignment across teams |
| Public SDK minor change | 1 minor release with warning | Semver expectation |
| Public SDK breaking change | 2+ minor releases, next major | Callers plan around majors |
| Public HTTP API | ≥6 months after Sunset header | Industry norm; see RFC 8594 |
| Long-term data format | 12+ months + dual-write window | Archive/BI consumers |

Always publish three dates: **announced**, **warn-loudly** (halfway — telemetry-driven escalation), and **removed**. Hold dates public; slip only with a re-announcement.

## Telemetry on Deprecated Usage

You cannot remove what you cannot measure. Instrument before announcing.

- **Server-side**: counter per deprecated endpoint / function, labeled by caller identity (API key, user agent, service ID). Keep labels cardinality-bounded.
- **Client-side / SDK**: emit a one-time `deprecation.used` event per session/process with call-site tag.
- **HTTP signals**: add `Deprecation: true` and `Sunset: <HTTP-date>` headers (RFC 8594). Callers can alert on these.
- **Logs**: include a stable `deprecation_id` in warning messages so log aggregators can count.

Removal-readiness gate: usage must be **zero for N consecutive days from all known callers**, or all remaining callers are explicitly unreachable (abandoned, out of business) with evidence in the journal.

## Sunset HTTP Header (RFC 8594)

```
Deprecation: true
Sunset: Sat, 31 Jan 2026 23:59:59 GMT
Link: <https://api.example.com/docs/migrate-v1-to-v2>; rel="deprecation"; type="text/html"
Link: <https://api.example.com/docs/migrate-v1-to-v2>; rel="sunset"
```

- `Deprecation` is a boolean-or-date flag; `Sunset` is the removal timestamp.
- Emit them *before* any in-payload deprecation field — headers are machine-readable and callers can wire alerts without parsing bodies.

## Client Migration Documentation

Every deprecated surface ships a migration doc with these sections:

1. **What is deprecated** — exact symbol / endpoint / field, with version.
2. **Why** — 1–3 sentences; link to the Void / Horizon finding if applicable.
3. **Replacement** — direct mapping with code examples in each supported language.
4. **Behavior diffs** — call out any *semantic* change (e.g., null handling, timezone, default).
5. **Timeline** — announced / warn-loudly / removed dates, copied verbatim from the deprecation registry.
6. **Fallback during transition** — feature flag name, compat shim availability, support contact.

Link this doc from the `Link: rel="deprecation"` header and from every deprecation warning log/console message.

## Fallback Strategy

Removal must be reversible for at least one release after it lands.

- Keep the old code path behind a feature flag (`deprecated.<name>.enabled`) for one release cycle post-removal. Default off; flip-on is the rollback.
- Database / data-format deprecations: retain dual-read (old + new) for one cycle beyond the announced removal; drop dual-write first, then dual-read.
- SDK major removal: publish a final minor on the old major that contains only a throw-with-migration-link — this is cheaper than re-publishing the real code if rollback is needed.

## Removal Playbook

```
T-N: ANNOUNCE       →  ship Deprecation/Sunset headers, warning logs, migration doc
                    →  register in deprecation-registry.md with the three dates
                    →  telemetry dashboard live and alerting on sustained usage

T-N/2: WARN LOUDLY  →  escalate warnings (from debug → warn → error-log)
                    →  direct outreach to remaining callers from telemetry
                    →  freeze any new features on the deprecated surface

T-7d: PRE-REMOVAL   →  verify usage == 0 for required window
                    →  dry-run removal in staging; run caller integration tests
                    →  stage rollback flag; confirm flip restores behavior

T-0: REMOVE         →  land removal behind default-off flag (old behavior still available via flip)
                    →  ship release with removal in CHANGELOG (coordinate with Launch)
                    →  monitor error rates, 4xx spike, caller alerts for 24–72h

T+1 cycle: FINALIZE →  delete feature-flag code path
                    →  purge telemetry counters
                    →  close deprecation-registry entry with removal evidence
```

Abort criteria: any previously-silent caller surfaces with >0.1% error rate attributable to the removal → flip the rollback flag, re-announce with a new removal date.

## Anti-Patterns

- Announcing deprecation without telemetry — you will never know when it is safe to remove.
- Removing on the announced date regardless of remaining usage ("we warned them") — causes outages and is almost always cheaper to postpone.
- Shipping the `Sunset` header with a date in the past or <30 days out — callers cannot react.
- Leaving "deprecated" comments in code with no registry entry, no date, no telemetry — zombie deprecation.
- Using deprecation as a substitute for a real migration plan for callers you control — if you own both sides, run `migrate` / `framework` / `lang` instead.
- Removing the code but leaving the route / symbol returning a generic 404/undefined — return a structured error with the migration link.

## Handoff

- → `Launch`: deprecation announcement and removal release coordination; CHANGELOG entry content.
- → `Builder`: implementation of warnings, headers, feature flags, and final removal PR.
- → `Radar`: test that deprecated surface emits warnings; test that removal with flag-off returns the migration-link error; test that flag-on restores behavior.
- → `Gear`: telemetry dashboard, alert rules on sustained deprecated-usage.
- ← `Void`: YAGNI / scope-cut proposals for surfaces that are already shipped.
- ← `Horizon`: our-side mirror — when a third party deprecates something we use, Horizon triggers Shift `framework`/`lang`/`migrate`, not `deprecate`.
