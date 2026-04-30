#!/usr/bin/env bash
# run-emit: append a structured event to <repo>/.agents/run-dash/<run-id>/events.jsonl
# Spec: _common/run-dash/EVENTS.md and INTEGRATION.md
#
# Usage:
#   run-emit <kind> [key=value]...
#
# Examples:
#   run-emit run_start run_kind=apex goal="passkey login" mode=AUTORUN_FULL scope=Standard
#   run-emit run_start run_kind=manual goal="explore module"
#   run-emit agent_start agent=plea phase=P1_Discovery engine=claude_code parent_agent=nexus depth=1
#   run-emit agent_end   agent=plea status=done duration_ms=42000
#   run-emit risk_gate   verdict=Conditional-Go omen=pass ripple=conditional echo=pass
#
# Contract:
#   - Never disrupts the run (errors are silenced, exit 0 unconditionally)
#   - No-op when RUN_ID (or legacy APEX_RUN_ID) is unset, or RUN_DASH_DISABLED=1
#   - Top-level reserved keys: phase / agent / engine / run_kind / recipe /
#     parent_agent / depth. Remaining key=value pairs nest under "meta".
#
# Environment (legacy APEX_* still honoured):
#   RUN_ID            run identifier (preferred)
#   RUN_DASH_DIR      base output dir (default: <repo>/.agents/run-dash)
#   RUN_DASH_DISABLED set to 1 to fully disable
#   RUN_REPO_ROOT     repo root override

{
  set -u

  ID="${RUN_ID:-${APEX_RUN_ID:-}}"
  [ -z "$ID" ] && exit 0

  DISABLED="${RUN_DASH_DISABLED:-${APEX_DASH_DISABLED:-0}}"
  [ "$DISABLED" = "1" ] && exit 0
  [ "$#" -lt 1 ] && exit 0

  KIND="$1"; shift

  REPO_ROOT="${RUN_REPO_ROOT:-${APEX_REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}}"
  if [ -n "${RUN_DASH_DIR:-}" ]; then
    DASH_DIR="$RUN_DASH_DIR"
  elif [ -n "${APEX_DASH_DIR:-}" ]; then
    DASH_DIR="$APEX_DASH_DIR"
  else
    DASH_DIR="$REPO_ROOT/.agents/run-dash"
  fi
  RUN_DIR="$DASH_DIR/$ID"
  EVENTS="$RUN_DIR/events.jsonl"
  SEQ_FILE="$RUN_DIR/.seq"

  mkdir -p "$RUN_DIR"

  LOCK="$RUN_DIR/.seq.lock"
  i=0
  while ! mkdir "$LOCK" 2>/dev/null; do
    i=$((i + 1))
    [ $i -gt 100 ] && break
    sleep 0.01
  done
  CURRENT=$(cat "$SEQ_FILE" 2>/dev/null || echo 0)
  SEQ=$((CURRENT + 1))
  printf '%s\n' "$SEQ" > "$SEQ_FILE"
  rmdir "$LOCK" 2>/dev/null

  TS=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ" 2>/dev/null)
  case "$TS" in
    *3NZ|"") TS=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z") ;;
  esac

  json_str() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\t'/\\t}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    printf '"%s"' "$s"
  }

  json_value() {
    local v="$1"
    if [[ "$v" =~ ^-?[0-9]+$ ]] || [[ "$v" =~ ^-?[0-9]+\.[0-9]+$ ]]; then
      printf '%s' "$v"
    elif [[ "$v" == "true" || "$v" == "false" ]]; then
      printf '%s' "$v"
    else
      json_str "$v"
    fi
  }

  PHASE="" ; AGENT="" ; ENGINE=""
  RUN_KIND="" ; RECIPE="" ; PARENT_AGENT="" ; DEPTH=""
  META_KV=()

  for kv in "$@"; do
    case "$kv" in
      *=*)
        key="${kv%%=*}"
        val="${kv#*=}"
        case "$key" in
          phase)         PHASE="$val" ;;
          agent)         AGENT="$val" ;;
          engine)        ENGINE="$val" ;;
          run_kind)      RUN_KIND="$val" ;;
          recipe)        RECIPE="$val" ;;
          parent_agent)  PARENT_AGENT="$val" ;;
          depth)         DEPTH="$val" ;;
          *)             META_KV+=("$key=$val") ;;
        esac
        ;;
    esac
  done

  J='{"ts":'
  J+="$(json_str "$TS")"
  J+=',"seq":'"$SEQ"
  J+=',"run_id":'"$(json_str "$ID")"
  J+=',"kind":'"$(json_str "$KIND")"
  [ -n "$RUN_KIND" ]     && J+=',"run_kind":'"$(json_str "$RUN_KIND")"
  [ -n "$RECIPE" ]       && J+=',"recipe":'"$(json_str "$RECIPE")"
  [ -n "$PHASE" ]        && J+=',"phase":'"$(json_str "$PHASE")"
  [ -n "$AGENT" ]        && J+=',"agent":'"$(json_str "$AGENT")"
  [ -n "$ENGINE" ]       && J+=',"engine":'"$(json_str "$ENGINE")"
  [ -n "$PARENT_AGENT" ] && J+=',"parent_agent":'"$(json_str "$PARENT_AGENT")"
  if [ -n "$DEPTH" ]; then
    if [[ "$DEPTH" =~ ^-?[0-9]+$ ]]; then
      J+=',"depth":'"$DEPTH"
    else
      J+=',"depth":'"$(json_str "$DEPTH")"
    fi
  fi

  if [ ${#META_KV[@]} -gt 0 ]; then
    META='"meta":{'
    first=1
    for kv in "${META_KV[@]}"; do
      key="${kv%%=*}"
      val="${kv#*=}"
      if [ $first -eq 1 ]; then
        first=0
      else
        META+=','
      fi
      META+="$(json_str "$key"):$(json_value "$val")"
    done
    META+='}'
    J+=",${META}"
  fi
  J+='}'

  printf '%s\n' "$J" >> "$EVENTS"

  exit 0
} 2>/dev/null

exit 0
