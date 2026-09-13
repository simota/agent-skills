#!/bin/bash
# html-to-pdf.sh - Convert an HTML report to A4 PDF.
# Usage: html-to-pdf.sh [--method chrome|wkhtmltopdf|puppeteer]
#                       [--timeout seconds] [--verbose] input.html [output.pdf]
set -euo pipefail

TIMEOUT=${TIMEOUT:-60}
VERBOSE=${VERBOSE:-false}
METHOD=""
INPUT_FILE=""
OUTPUT_FILE=""
WORK_DIR=""

error() { echo "Error: $1" >&2; }
log() { if [ "$VERBOSE" = true ]; then echo "$1" >&2; fi; }
usage() {
  echo "Usage: $0 [options] <input.html> [output.pdf]"
  echo "  --method <method>   chrome, wkhtmltopdf, or puppeteer"
  echo "  --timeout <sec>     Positive integer seconds (default: 60)"
  echo "  --verbose, -v       Show converter diagnostics"
  echo "  --help, -h          Show this help"
}

POSITIONAL=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --method|--timeout)
      if [ $# -lt 2 ] || [[ "$2" == --* ]] || [ -z "$2" ]; then
        error "Missing value for $1"; exit 1
      fi
      if [ "$1" = --method ]; then METHOD="$2"; else TIMEOUT="$2"; fi
      shift 2
      ;;
    --verbose|-v) VERBOSE=true; shift ;;
    --help|-h) usage; exit 0 ;;
    --) shift; POSITIONAL+=("$@"); break ;;
    -*) error "Unknown option: $1"; exit 1 ;;
    *) POSITIONAL+=("$1"); shift ;;
  esac
done

if [ ${#POSITIONAL[@]} -lt 1 ] || [ ${#POSITIONAL[@]} -gt 2 ]; then
  usage >&2; exit 1
fi
if ! [[ "$TIMEOUT" =~ ^[1-9][0-9]*$ ]]; then
  error "Timeout must be a positive integer"; exit 1
fi
case "$METHOD" in
  ""|chrome|wkhtmltopdf|puppeteer) ;;
  *) error "Unknown method: $METHOD"; exit 1 ;;
esac

INPUT_FILE="${POSITIONAL[0]}"
[ -f "$INPUT_FILE" ] || { error "File not found: $INPUT_FILE"; exit 1; }
[[ "$INPUT_FILE" == /* ]] || INPUT_FILE="$PWD/$INPUT_FILE"
OUTPUT_FILE="${POSITIONAL[1]:-${INPUT_FILE%.[hH][tT][mM][lL]}.pdf}"
[[ "$OUTPUT_FILE" == /* ]] || OUTPUT_FILE="$PWD/$OUTPUT_FILE"
if [ "$INPUT_FILE" -ef "$OUTPUT_FILE" ]; then
  error "Input and output must be different files"; exit 1
fi
if [ -d "$OUTPUT_FILE" ]; then
  error "Output is a directory: $OUTPUT_FILE"; exit 1
fi

# Use a fresh file per attempt and publish only a verified result. A previous PDF
# must never make a failed converter appear successful or be destroyed on failure.
WORK_DIR=$(mktemp -d "$(dirname "$OUTPUT_FILE")/.html-to-pdf.XXXXXX")
trap 'rm -rf -- "$WORK_DIR"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
PDF_FILE="$WORK_DIR/report.pdf"

run_with_timeout() (
  if command -v timeout >/dev/null 2>&1; then
    timeout --kill-after=1 "$TIMEOUT" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout --kill-after=1 "$TIMEOUT" "$@"
  else
    # Bash job control gives the converter a process group, including browser
    # children. Kill the whole group, and reap both converter and watchdog.
    set -m
    "$@" &
    local pid=$!
    (
      sleep "$TIMEOUT"
      kill -TERM -- "-$pid" 2>/dev/null || exit 0
      sleep 1
      kill -KILL -- "-$pid" 2>/dev/null || true
    ) &
    local watchdog=$!
    local status=0
    wait "$pid" || status=$?
    kill -TERM -- "-$watchdog" 2>/dev/null || true
    wait "$watchdog" 2>/dev/null || true
    # Terminate descendants that outlived their converter parent.
    kill -KILL -- "-$pid" 2>/dev/null || true
    return "$status"
  fi
)

run_converter() {
  rm -f -- "$PDF_FILE"
  if [ "$VERBOSE" = true ]; then
    run_with_timeout "$@"
  else
    run_with_timeout "$@" >"$WORK_DIR/converter.log" 2>&1
  fi
}

verify_output() {
  [ -f "$PDF_FILE" ] || return 1
  if [ "$(head -c 5 "$PDF_FILE")" != '%PDF-' ]; then
    error "Output is not a PDF file"; return 1
  fi
  # A valid short document can be smaller than 1 KB. Check the terminating
  # marker instead of accepting a large but truncated converter output.
  if ! tail -c 1024 "$PDF_FILE" | LC_ALL=C grep -Eq '^[[:space:]]*%%EOF[[:space:]]*$'; then
    error "Output has no PDF end-of-file marker"; return 1
  fi
}

file_url() {
  # Percent-encode bytes, including #, %, spaces, and UTF-8, without eval.
  local LC_ALL=C
  local value="$1" encoded="" char hex i
  for ((i=0; i<${#value}; i++)); do
    char="${value:i:1}"
    case "$char" in
      [a-zA-Z0-9/._~-]) encoded+="$char" ;;
      *) printf -v hex '%%%02X' "'$char"; encoded+="$hex" ;;
    esac
  done
  printf 'file://%s' "$encoded"
}

find_chrome() {
  local candidate
  for candidate in google-chrome chromium chromium-browser \
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
      "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
    if command -v "$candidate" >/dev/null 2>&1; then
      command -v "$candidate"; return 0
    fi
  done
  return 1
}

convert_with_chrome() {
  local chrome_cmd
  chrome_cmd=$(find_chrome) || return 1
  log "Using Chrome: $chrome_cmd"
  run_converter "$chrome_cmd" --headless --disable-gpu \
    --disable-software-rasterizer --disable-dev-shm-usage \
    "--user-data-dir=$WORK_DIR/chrome-profile" "--print-to-pdf=$PDF_FILE" \
    --no-pdf-header-footer --no-margins --run-all-compositor-stages-before-draw \
    --virtual-time-budget=5000 "$(file_url "$INPUT_FILE")" || return 1
  verify_output
}

convert_with_wkhtmltopdf() {
  command -v wkhtmltopdf >/dev/null 2>&1 || return 1
  log "Using wkhtmltopdf"
  run_converter wkhtmltopdf --page-size A4 --margin-top 15mm \
    --margin-bottom 15mm --margin-left 12mm --margin-right 12mm \
    --enable-local-file-access --javascript-delay 2000 --no-stop-slow-scripts \
    "$INPUT_FILE" "$PDF_FILE" || return 1
  verify_output
}

convert_with_puppeteer() {
  command -v node >/dev/null 2>&1 || return 1
  local script_dir
  script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
  log "Using Puppeteer"
  run_converter node "$script_dir/puppeteer-pdf.js" "$INPUT_FILE" "$PDF_FILE" || return 1
  verify_output
}

echo "Converting: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
METHODS=(chrome wkhtmltopdf puppeteer)
if [ -n "$METHOD" ]; then METHODS=("$METHOD"); fi
for candidate in "${METHODS[@]}"; do
  if "convert_with_$candidate"; then
    mv -f -- "$PDF_FILE" "$OUTPUT_FILE"
    echo "Done ($candidate): $OUTPUT_FILE"
    exit 0
  fi
  log "$candidate unavailable or failed"
done
error "PDF conversion failed. Install Chrome, wkhtmltopdf, or Puppeteer; use --verbose for diagnostics."
exit 1
