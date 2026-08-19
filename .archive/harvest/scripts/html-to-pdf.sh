#!/bin/bash
# html-to-pdf.sh - HTMLレポートをA4 PDFに変換
#
# 使用方法:
#   ./html-to-pdf.sh report.html
#   ./html-to-pdf.sh report.html output.pdf
#   ./html-to-pdf.sh --method chrome input.html output.pdf
#
# オプション:
#   --method <chrome|wkhtmltopdf|puppeteer>  変換方法を指定
#   --timeout <seconds>                       タイムアウト秒数 (default: 60)
#   --verbose                                 詳細出力
#
# 必要条件:
#   - Chrome/Chromium (headless PDF生成) - 推奨
#   - wkhtmltopdf (フォールバック)
#   - Puppeteer (Node.js環境)

set -e

# ============================================
# Configuration
# ============================================

TIMEOUT=${TIMEOUT:-60}
VERBOSE=${VERBOSE:-false}
METHOD=""

# ============================================
# Argument Parsing
# ============================================

while [[ $# -gt 0 ]]; do
  case $1 in
    --method)
      METHOD="$2"
      shift 2
      ;;
    --timeout)
      TIMEOUT="$2"
      shift 2
      ;;
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [options] <input.html> [output.pdf]"
      echo ""
      echo "Options:"
      echo "  --method <method>   Conversion method: chrome, wkhtmltopdf, puppeteer"
      echo "  --timeout <sec>     Timeout in seconds (default: 60)"
      echo "  --verbose, -v       Verbose output"
      echo "  --help, -h          Show this help"
      exit 0
      ;;
    *)
      if [ -z "$INPUT_FILE" ]; then
        INPUT_FILE="$1"
      else
        OUTPUT_FILE="$1"
      fi
      shift
      ;;
  esac
done

# ============================================
# Validation
# ============================================

if [ -z "$INPUT_FILE" ]; then
  echo "Error: Input file required"
  echo "Usage: $0 <input.html> [output.pdf]"
  exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File not found: $INPUT_FILE"
  exit 1
fi

# Ensure absolute path
if [[ "$INPUT_FILE" != /* ]]; then
  INPUT_FILE="$(pwd)/$INPUT_FILE"
fi

OUTPUT_FILE="${OUTPUT_FILE:-${INPUT_FILE%.html}.pdf}"

# ============================================
# Logging
# ============================================

log() {
  if [ "$VERBOSE" = true ]; then
    echo "[$(date '+%H:%M:%S')] $1"
  fi
}

error() {
  echo "Error: $1" >&2
}

# ============================================
# Timeout Wrapper
# ============================================

run_with_timeout() {
  local cmd="$1"
  local timeout_sec="${2:-$TIMEOUT}"

  if command -v timeout &> /dev/null; then
    # GNU timeout (Linux)
    timeout "$timeout_sec" bash -c "$cmd"
  elif command -v gtimeout &> /dev/null; then
    # GNU timeout via Homebrew (macOS)
    gtimeout "$timeout_sec" bash -c "$cmd"
  else
    # Fallback: background process with kill
    bash -c "$cmd" &
    local pid=$!
    local count=0
    while kill -0 $pid 2>/dev/null; do
      sleep 1
      ((count++))
      if [ $count -ge $timeout_sec ]; then
        kill -9 $pid 2>/dev/null
        error "Timeout after ${timeout_sec}s"
        return 124
      fi
    done
    wait $pid
  fi
}

# ============================================
# Verify Output
# ============================================

verify_output() {
  local file="$1"
  local min_size="${2:-1000}"

  if [ ! -f "$file" ]; then
    return 1
  fi

  local size=$(wc -c < "$file" 2>/dev/null | tr -d ' ')
  if [ "$size" -lt "$min_size" ]; then
    error "Output file too small (${size} bytes). PDF generation may have failed."
    return 1
  fi

  # Check PDF magic number
  if ! head -c 4 "$file" 2>/dev/null | grep -q '%PDF'; then
    error "Output is not a valid PDF file"
    return 1
  fi

  return 0
}

# ============================================
# Chrome/Chromium
# ============================================

find_chrome() {
  local candidates=(
    "google-chrome"
    "chromium"
    "chromium-browser"
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    "/Applications/Chromium.app/Contents/MacOS/Chromium"
    "/usr/bin/google-chrome"
    "/usr/bin/chromium"
  )

  for cmd in "${candidates[@]}"; do
    if command -v "$cmd" &> /dev/null || [ -x "$cmd" ]; then
      echo "$cmd"
      return 0
    fi
  done

  return 1
}

convert_with_chrome() {
  local chrome_cmd
  chrome_cmd=$(find_chrome) || return 1

  log "Using Chrome: $chrome_cmd"

  local temp_dir=$(mktemp -d)
  trap "rm -rf $temp_dir" EXIT

  local cmd="\"$chrome_cmd\" \
    --headless \
    --disable-gpu \
    --no-sandbox \
    --disable-software-rasterizer \
    --disable-dev-shm-usage \
    --print-to-pdf=\"$OUTPUT_FILE\" \
    --print-to-pdf-no-header \
    --no-margins \
    --run-all-compositor-stages-before-draw \
    --virtual-time-budget=5000 \
    \"file://$INPUT_FILE\" 2>/dev/null"

  if run_with_timeout "$cmd" "$TIMEOUT"; then
    if verify_output "$OUTPUT_FILE"; then
      return 0
    fi
  fi

  return 1
}

# ============================================
# wkhtmltopdf
# ============================================

convert_with_wkhtmltopdf() {
  if ! command -v wkhtmltopdf &> /dev/null; then
    return 1
  fi

  log "Using wkhtmltopdf"

  local cmd="wkhtmltopdf \
    --page-size A4 \
    --margin-top 15mm \
    --margin-bottom 15mm \
    --margin-left 12mm \
    --margin-right 12mm \
    --enable-local-file-access \
    --javascript-delay 2000 \
    --no-stop-slow-scripts \
    --debug-javascript \
    \"$INPUT_FILE\" \
    \"$OUTPUT_FILE\" 2>/dev/null"

  if run_with_timeout "$cmd" "$TIMEOUT"; then
    if verify_output "$OUTPUT_FILE"; then
      return 0
    fi
  fi

  return 1
}

# ============================================
# Puppeteer
# ============================================

convert_with_puppeteer() {
  if ! command -v node &> /dev/null; then
    return 1
  fi

  local script_dir="$(dirname "$0")"
  local puppeteer_script="$script_dir/puppeteer-pdf.js"

  if [ ! -f "$puppeteer_script" ]; then
    return 1
  fi

  log "Using Puppeteer"

  local cmd="node \"$puppeteer_script\" \"$INPUT_FILE\" \"$OUTPUT_FILE\" 2>/dev/null"

  if run_with_timeout "$cmd" "$TIMEOUT"; then
    if verify_output "$OUTPUT_FILE"; then
      return 0
    fi
  fi

  return 1
}

# ============================================
# Main
# ============================================

echo "Converting: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"

# If method specified, use only that method
if [ -n "$METHOD" ]; then
  case "$METHOD" in
    chrome)
      if convert_with_chrome; then
        echo "Done: $OUTPUT_FILE"
        exit 0
      fi
      error "Chrome conversion failed"
      exit 1
      ;;
    wkhtmltopdf)
      if convert_with_wkhtmltopdf; then
        echo "Done: $OUTPUT_FILE"
        exit 0
      fi
      error "wkhtmltopdf conversion failed"
      exit 1
      ;;
    puppeteer)
      if convert_with_puppeteer; then
        echo "Done: $OUTPUT_FILE"
        exit 0
      fi
      error "Puppeteer conversion failed"
      exit 1
      ;;
    *)
      error "Unknown method: $METHOD"
      exit 1
      ;;
  esac
fi

# Auto-detect: try each method with fallback
echo "Detecting conversion method..."

# Method 1: Chrome/Chromium (recommended)
if convert_with_chrome; then
  echo "Done (Chrome): $OUTPUT_FILE"
  exit 0
fi
log "Chrome not available or failed, trying next method..."

# Method 2: wkhtmltopdf
if convert_with_wkhtmltopdf; then
  echo "Done (wkhtmltopdf): $OUTPUT_FILE"
  exit 0
fi
log "wkhtmltopdf not available or failed, trying next method..."

# Method 3: Puppeteer
if convert_with_puppeteer; then
  echo "Done (Puppeteer): $OUTPUT_FILE"
  exit 0
fi
log "Puppeteer not available or failed"

# All methods failed
echo ""
error "All PDF conversion methods failed."
echo ""
echo "Install one of the following:"
echo "  - Google Chrome or Chromium (recommended)"
echo "  - wkhtmltopdf: brew install wkhtmltopdf"
echo "  - Puppeteer: npm install puppeteer"
echo ""
echo "Or open the HTML file in a browser and print to PDF."
exit 1
