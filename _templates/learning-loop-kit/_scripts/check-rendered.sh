#!/usr/bin/env bash
# check-rendered.sh — verify a rendered Learning-Loop Kit has no leftover template residue.
# Usage: check-rendered.sh <kit-dir>
# Exit 0 = clean; exit 1 = residue found (prints offending file:line).
#
# Run this after rendering base/ into a new <slug>-kit and substituting tokens.
# It is the render gate: a kit must pass before it is committed or installed.
set -euo pipefail

DIR="${1:?usage: check-rendered.sh <kit-dir>}"
[ -d "$DIR" ] || { echo "not a directory: $DIR" >&2; exit 2; }

fail=0

# 1. Unrendered {{TOKEN}} placeholders.
if grep -rnE '\{\{[A-Z_]+\}\}' "$DIR"; then
  echo "✗ unrendered {{TOKEN}} placeholders above — substitute them." >&2
  fail=1
fi

# 2. Leftover date placeholders in seeded entries (skeleton not replaced).
#    _templates/ is exempt — entry templates legitimately keep date/slug placeholders.
if grep -rn --exclude-dir='_templates' 'YYYY-MM-DD\|YYYYMMDD-<slug>' "$DIR"; then
  echo "✗ leftover date placeholders above — replace with real dates/IDs in seeded entries." >&2
  fail=1
fi

# 3. Leftover angle-bracket skeleton markers in non-template files.
if grep -rn --include='*.md' --exclude-dir='_templates' '<slug>\|<LAYER>\|<kit-slug>' "$DIR"; then
  echo "✗ leftover skeleton markers above (outside _templates/) — fill in concrete values." >&2
  fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "✓ $DIR is clean — no template residue."
fi
exit "$fail"
