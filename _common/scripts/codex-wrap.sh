#!/usr/bin/env bash
# codex-wrap: emit agent_start / agent_end around a Codex CLI invocation so the
# engine boundary (claude_code → codex_cli) is observable in run-dash.
#
# Spec: _common/RUN_DASH_PROTOCOL.md (§Codex CLI integration)
#
# Usage:
#   codex-wrap --agent=<name> [--phase=<phase>] [--parent=<agent>] [--depth=<n>] \
#              [--meta key=value ...] -- <codex-command...>
#
# Example:
#   codex-wrap --agent=builder --phase=P6_Implementation --parent=orbit -- \
#     codex exec --task-id "$TASK" -- bun run build
#
# Behaviour:
#   - Emits agent_start engine=codex_cli before the command
#   - Runs the command verbatim, preserving its exit code
#   - Emits agent_end with status=done|error and duration_ms after the command
#   - No-op on emit (silent) when RUN_ID is unset or RUN_DASH_DISABLED=1
#   - Never alters the wrapped command's stdout / stderr / exit code

set -u

AGENT=""
PHASE=""
PARENT=""
DEPTH=""
META_ARGS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --agent=*)   AGENT="${1#*=}" ; shift ;;
    --phase=*)   PHASE="${1#*=}" ; shift ;;
    --parent=*)  PARENT="${1#*=}" ; shift ;;
    --depth=*)   DEPTH="${1#*=}" ; shift ;;
    --meta)
      shift
      [ $# -gt 0 ] || break
      META_ARGS+=("$1")
      shift
      ;;
    --)
      shift
      break
      ;;
    *)
      printf 'codex-wrap: unknown option: %s\n' "$1" >&2
      exit 64
      ;;
  esac
done

if [ "$#" -lt 1 ]; then
  printf 'codex-wrap: missing command (use -- to separate)\n' >&2
  exit 64
fi

if [ -z "$AGENT" ]; then
  printf 'codex-wrap: --agent=<name> is required\n' >&2
  exit 64
fi

EMIT="${RUN_DASH_EMIT:-$HOME/.claude/skills/_common/scripts/run-emit.sh}"
emit() {
  [ -x "$EMIT" ] || return 0
  bash "$EMIT" "$@" 2>/dev/null || true
}

start_args=(agent_start "agent=$AGENT" "engine=codex_cli")
[ -n "$PHASE" ]  && start_args+=("phase=$PHASE")
[ -n "$PARENT" ] && start_args+=("parent_agent=$PARENT")
[ -n "$DEPTH" ]  && start_args+=("depth=$DEPTH")
if [ ${#META_ARGS[@]} -gt 0 ]; then
  for m in "${META_ARGS[@]}"; do
    start_args+=("$m")
  done
fi

emit "${start_args[@]}"

START_S=$(date +%s)
"$@"
RC=$?
END_S=$(date +%s)
DUR_MS=$(( (END_S - START_S) * 1000 ))

if [ "$RC" -eq 0 ]; then
  STATUS="done"
else
  STATUS="error"
fi

end_args=(agent_end "agent=$AGENT" "engine=codex_cli" "status=$STATUS" "duration_ms=$DUR_MS" "exit_code=$RC")
[ -n "$PHASE" ] && end_args+=("phase=$PHASE")

emit "${end_args[@]}"

exit "$RC"
