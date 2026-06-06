#!/usr/bin/env bash
# verify.sh — Acceptance criteria verifier for the citation loop.
# Usage:
#   verify.sh all                           # C1..C4
#   verify.sh check-citations               # C1
#   verify.sh check-no-regression           # C2
#   verify.sh check-injection-annotations   # C3
#   verify.sh check-pending-empty           # C4

set -euo pipefail

LOOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$(cd "${LOOP_DIR}/../.." && pwd)"
SKILL_UPDATE_LOOP="${LOOP_DIR}/../skill-update"
REPORTS_DIR="${LOOP_DIR}/reports"
TODO_FILE="${LOOP_DIR}/citations-todo.md"
PENDING="${LOOP_DIR}/state/skills-pending.txt"

fail() { printf '[verify:FAIL] %s\n' "$1" >&2; exit 1; }
ok()   { printf '[verify:OK]   %s\n' "$1"; }

list_target_skills() {
  grep -E '^## ' "${TODO_FILE}" | sed -E 's/^## //'
}

check_citations() {
  # C1: each target skill's SKILL.md (or any reference/*.md under that skill)
  # contains at least one citation marker. We use `grep -r` so the check works
  # whether or not a reference/ directory exists.
  local skill skill_dir missing=0 total=0
  while IFS= read -r skill; do
    [[ -z "${skill}" ]] && continue
    total=$((total + 1))
    skill_dir="${SKILLS_ROOT}/${skill}"
    [[ -f "${skill_dir}/SKILL.md" ]] || {
      printf '  MISS: %s SKILL.md missing\n' "${skill}" >&2
      missing=$((missing + 1))
      continue
    }
    if ! grep -rqE '\[Source:[[:space:]]|^Source:|^Sources:|https?://' "${skill_dir}" --include='*.md' 2>/dev/null; then
      printf '  NO CITATION: %s\n' "${skill}" >&2
      missing=$((missing + 1))
    fi
  done < <(list_target_skills)
  printf 'C1 citations present: %d/%d\n' "$((total - missing))" "${total}"
  (( missing == 0 )) || fail "C1: ${missing} skills lack any citation marker"
  ok "C1 every target skill has at least one citation marker"
}

check_no_regression() {
  # C2: AC1/AC2/AC4 from skill-update verifier must still be 0.
  local v="${SKILL_UPDATE_LOOP}/verify.sh"
  [[ -f "${v}" ]] || fail "C2: skill-update/verify.sh not found"
  local ac1 ac2 ac4
  ac1=$(bash "${v}" check-common-refs   2>&1 | grep -oE '[0-9]+ missing' | head -1 | awk '{print $1}')
  ac2=$(bash "${v}" check-reference-map 2>&1 | grep -oE '[0-9]+ missing' | head -1 | awk '{print $1}')
  ac4=$(bash "${v}" check-bidir-refs    2>&1 | grep -oE '[0-9]+ orphan'  | head -1 | awk '{print $1}')
  printf 'C2 regression check: ac1=%s ac2=%s ac4=%s\n' "${ac1}" "${ac2}" "${ac4}"
  (( ac1 == 0 && ac2 == 0 && ac4 == 0 )) || fail "C2: regression detected"
  ok "C2 no regression in AC1/AC2/AC4"
}

check_injection_annotations() {
  [[ -f "${REPORTS_DIR}/citations-applied.md" ]] || { ok "C3 skipped (no report yet)"; return 0; }
  local urls_total urls_annotated missing
  urls_total=$(grep -E '^- URL: https?://' "${REPORTS_DIR}/citations-applied.md" 2>/dev/null | wc -l | tr -d ' ')
  urls_annotated=$(grep -E '^- URL: https?://.+injection-check:' "${REPORTS_DIR}/citations-applied.md" 2>/dev/null | wc -l | tr -d ' ')
  missing=$(( urls_total - urls_annotated ))
  printf 'C3 injection annotations: %d/%d\n' "${urls_annotated}" "${urls_total}"
  (( missing == 0 )) || fail "C3: ${missing} URLs missing injection-check"
  ok "C3 every URL annotated"
}

check_pending_empty() {
  [[ -f "${PENDING}" ]] || fail "C4: pending file missing"
  local n; n=$(wc -l <"${PENDING}" | tr -d ' ')
  (( n == 0 )) || fail "C4: ${n} skills still pending"
  ok "C4 pending empty"
}

case "${1:-all}" in
  check-citations)             check_citations ;;
  check-no-regression)         check_no_regression ;;
  check-injection-annotations) check_injection_annotations ;;
  check-pending-empty)         check_pending_empty ;;
  all)
    check_citations
    check_no_regression
    check_injection_annotations
    check_pending_empty
    printf '\n[verify] ALL ACs PASS\n'
    ;;
  *) printf 'unknown: %s\n' "$1" >&2; exit 64 ;;
esac
