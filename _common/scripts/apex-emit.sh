#!/usr/bin/env bash
# apex-emit (compat alias): forwards to run-emit.sh
# The dashboard machinery was renamed apex-dash → run-dash.
# Keep this thin wrapper so callers using APEX_RUN_ID / apex-emit invocation
# keep working without modification.
exec "$(dirname "$0")/run-emit.sh" "$@"
