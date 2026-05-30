<!--
Paste the block below into the target project's CLAUDE.md (or AGENTS.md).
This is what makes principles ENFORCED: every agent loads them before UI work.
-->

## Design Principles (enforced)

This project learns UI/UX feedback into durable principles under `design/`. The principles files are the source of truth.

- **Before any UI/UX work** (web frontend or native iOS/Android), scan `design/principles/INDEX.md` by tag, then read `design/principles/core.md` **and** the layer for the target platform: `design/principles/frontend.md`, `design/principles/ios.md`, or `design/principles/android.md`. Treat every `status: accepted` principle as a hard constraint (ignore the `## Archive` section). Prefer the named design `Token:` over a literal value where one exists.
- **When UI/UX feedback arrives**, run the learning loop in `design/README.md` (CAPTURE → ANALYZE → REVIEW → PROMOTE → ENFORCE). New principles require **human approval** at the REVIEW step before becoming binding — never self-promote a draft, even in AUTORUN. `/nexus` orchestrates the chain.
- **PR review gate (mandatory for UI diffs):** verify the diff violates no accepted principle for its platform; a violation blocks merge until fixed or human-waived. Quantitative (`Token:`-backed) principles are machine-checkable; qualitative ones are reviewer judgment. If a violation reveals a *missing* rule, append it to `design/feedback-log.md` (`source: review`) so the loop captures it.

Full mechanism: `design/README.md` · Agent procedure: `design/AGENT_GUIDE.md`.
