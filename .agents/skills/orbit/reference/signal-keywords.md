# Signal Keywords → Recipe

Canonical natural-language routing table for Orbit. Used by `## Subcommand Dispatch` when the first token is not an explicit Recipe subcommand. An explicit subcommand match always wins over a keyword match.

| Keywords / Artifacts | Recipe (Request Mode) |
|----------------------|------------------------|
| `plan`, `loop plan`, `plan document`, `design the loop`, `loop design doc` | `plan` (GENERATE — plan-only, document-first) |
| `generate`, `new loop`, `create runner` | `generate` (GENERATE) |
| `audit`, `check loop`, `loop status` | `audit` (AUDIT) |
| `recover`, `state drift`, `fix loop`; `runner.log` has failures | `recover` (RECOVER) |
| `health check`, `proactive`, `pre-failure` | Proactive Audit (PROACTIVE_AUDIT) |
| `ralph`, `PROMPT.md`, `<promise>COMPLETE</promise>`, `cat PROMPT.md \| claude` | `ralph` (GENERATE — Ralph variant) |
| `goal.md` exists and well-formed | `audit` (AUDIT) |
| `goal.md` missing/vague, or unclear request | `generate` (GENERATE — default) — see `vague-goal-handling.md` |

Routing rules:

- Subcommand match (first token equals a Recipe subcommand) wins if both a subcommand and a keyword apply.
- If no keyword matches, fall back to the default Recipe (`generate` = GENERATE).
- Applies to natural-language input without an explicit subcommand.
