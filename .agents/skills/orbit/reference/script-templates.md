# Orbit Script Templates

Purpose: routing index. Load this first when Orbit must generate or patch loop scripts — it tells you which template file to open next without forcing all executable bodies into context at once.

For lifecycle, recovery flow, verification structure, and inter-script relationships (producer / consumer / contract), see `reference/script-flow.md` § Inter-Script Relationships.

## Contents

- [Generation decision table](#generation-decision-table)
- [Template selection](#template-selection)

## Generation Decision Table

| Scenario | Generate | Do not generate | Read next |
|----------|----------|-----------------|-----------|
| New loop startup | `bootstrap.sh` | `run-loop.sh` and `notify.sh` separately, because `bootstrap.sh` embeds them | `reference/script-template-support.md` |
| Main runner patch | `run-loop.sh` | other scripts unless the request names them | `reference/script-template-runner.md` |
| Add verify command | `verify.sh` only | unrelated scripts | `reference/script-template-support.md` |
| State recovery | `recover.sh` only | `run-loop.sh` unless recovery changes runner logic | `reference/script-template-support.md` |
| Add notification | `notify.sh` only | unrelated scripts | `reference/script-template-support.md` |
| Mixed script patch | named targets only | untouched scripts | open only the needed template files |

## Template Selection

| Need | Open |
|------|------|
| Runner lifecycle, pre-flight, retry, autocommit, squash, footer | `reference/script-template-runner.md` |
| Bootstrap, recovery, verification, notification | `reference/script-template-support.md` |
| Lifecycle explanation, inter-script relationships, recovery/verification flow without executable bodies | `reference/script-flow.md` |
| Engine-specific `EXEC_CMD` configuration | `reference/executor-engines.md` |
