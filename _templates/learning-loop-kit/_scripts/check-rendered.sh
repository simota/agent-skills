#!/usr/bin/env bash
# Verify a rendered Learning-Loop Kit has no leftover template residue.
# Usage: check-rendered.sh <kit-dir>
# Exit 0 = clean; 1 = residue; 2 = invalid input or scan failure.
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo 'usage: check-rendered.sh <kit-dir>' >&2
  exit 2
fi
DIR="$1"
[ -d "$DIR" ] || { echo "not a directory: $DIR" >&2; exit 2; }
fail=0

# scan MESSAGE PATTERN [GREP-OPTION...]: options precede `-e PATTERN` so the
# call also parses under POSIXLY_CORRECT, where the first operand ends options.
scan() {
  local message="$1" pattern="$2" status
  shift 2
  if grep "$@" -e "$pattern" -- "$DIR"; then
    echo "✗ $message" >&2
    fail=1
  else
    status=$?
    if [ "$status" -ne 1 ]; then
      echo "Unable to scan: $DIR" >&2
      exit 2
    fi
  fi
}

# All uppercase tokens must be rendered, including entry templates.
scan 'unrendered {{TOKEN}} placeholders above — substitute them.' \
  '\{\{[A-Z_][A-Z0-9_]*\}\}' -rnE

# Entry templates legitimately retain date and slug placeholders.
scan 'leftover date placeholders above — replace seeded dates/IDs.' \
  'YYYY-MM-DD|YYYYMMDD-<slug>' -rnE --exclude-dir='_templates'
scan 'leftover skeleton markers above — fill in concrete values.' \
  '<slug>|<LAYER>|<kit-slug>' -rnE --include='*.md' --exclude-dir='_templates'

if [ "$fail" -eq 0 ]; then
  echo "✓ $DIR is clean — no template residue."
fi
exit "$fail"
