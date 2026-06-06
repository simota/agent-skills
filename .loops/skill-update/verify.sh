#!/usr/bin/env bash
# verify.sh — Acceptance criteria verifier for the skill-update loop.
# Usage:
#   verify.sh all                       # run AC1..AC6, exit non-zero on first failure
#   verify.sh check-common-refs         # AC1
#   verify.sh check-reference-map       # AC2
#   verify.sh check-bidir-refs          # AC4
#   verify.sh check-audit-coverage      # AC5
#   verify.sh check-improvements        # AC6
#
# AC3 (CAPABILITIES_SUMMARY drift) is semantic; verifier prints a summary
# pointer to reports/capabilities-drift.md but does NOT auto-pass/fail.

set -euo pipefail

LOOP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_ROOT="$(cd "${LOOP_DIR}/../.." && pwd)"
REPORTS_DIR="${LOOP_DIR}/reports"
PENDING="${LOOP_DIR}/state/skills-pending.txt"
PROCESSED="${LOOP_DIR}/state/skills-processed.txt"

fail() { printf '[verify:FAIL] %s\n' "$1" >&2; exit 1; }
ok()   { printf '[verify:OK]   %s\n' "$1"; }

list_skills() {
  find "${SKILLS_ROOT}" -mindepth 2 -maxdepth 2 -name SKILL.md -type f \
    | sed -E "s|${SKILLS_ROOT}/([^/]+)/SKILL\.md|\1|" \
    | grep -Ev '^(_common|_templates|\.agents|\.loops)$' \
    | sort -u
}

check_common_refs() {
  local skill ref skill_md missing=0 total=0
  while IFS= read -r skill; do
    skill_md="${SKILLS_ROOT}/${skill}/SKILL.md"
    [[ -f "${skill_md}" ]] || continue
    while IFS= read -r ref; do
      total=$((total + 1))
      if [[ ! -f "${SKILLS_ROOT}/${ref}" ]]; then
        printf '  MISS: %s -> %s\n' "${skill}" "${ref}" >&2
        missing=$((missing + 1))
      fi
    done < <(grep -oE '_common/[A-Za-z0-9_.-]+\.md' "${skill_md}" | sort -u)
  done < <(list_skills)
  printf 'AC1 _common/ refs: %d checked, %d missing\n' "${total}" "${missing}"
  (( missing == 0 )) || fail "AC1: ${missing} dead _common/ refs"
  ok "AC1 zero dead common refs"
}

check_reference_map() {
  # Extract `reference/foo.md` references for each skill, but exclude:
  #   - cross-skill refs    (e.g. `rally/reference/foo.md` — owned by rally, not us)
  #   - optional markers    (line contains "(if present)")
  #   - activity-log rows   (lines starting with `| YYYY-MM-DD ` — these cite PROJECT.md examples)
  local skill skill_md ref_path missing=0 total=0
  while IFS= read -r skill; do
    skill_md="${SKILLS_ROOT}/${skill}/SKILL.md"
    [[ -f "${skill_md}" ]] || continue
    while IFS= read -r ref_path; do
      total=$((total + 1))
      if [[ ! -f "${SKILLS_ROOT}/${skill}/${ref_path}" ]]; then
        printf '  MISS: %s -> %s\n' "${skill}" "${ref_path}" >&2
        missing=$((missing + 1))
      fi
    done < <(
      awk '
        # Drop activity-log example rows
        /^[[:space:]]*\| [0-9]{4}-[0-9]{2}-[0-9]{2}/ { next }
        # Drop lines marked optional
        /\(if present\)/ { next }
        {
          s = $0
          while (match(s, /references\/[A-Za-z0-9_.-]+\.md/)) {
            start = RSTART
            len   = RLENGTH
            prev  = (start > 1) ? substr(s, start - 1, 1) : " "
            # Ignore matches preceded by alnum / underscore / dash / slash
            # (which means another path segment owns the reference/ — a cross-skill ref).
            if (prev !~ /[A-Za-z0-9_-]/ && prev != "/") {
              print substr(s, start, len)
            }
            s = substr(s, start + len)
          }
        }
      ' "${skill_md}" | sort -u
    )
  done < <(list_skills)
  printf 'AC2 reference map: %d checked, %d missing\n' "${total}" "${missing}"
  (( missing == 0 )) || fail "AC2: ${missing} dead reference/ refs"
  ok "AC2 reference map valid"
}

check_bidir_refs() {
  # For each reference/X.md, check whether SKILL.md mentions it (one-way is OK
  # but unreferenced reference files are flagged as soft warnings).
  local skill ref_dir orphans=0
  while IFS= read -r skill; do
    ref_dir="${SKILLS_ROOT}/${skill}/references"
    [[ -d "${ref_dir}" ]] || continue
    while IFS= read -r ref; do
      local base; base="$(basename "${ref}")"
      if ! grep -qE "reference/${base}" "${SKILLS_ROOT}/${skill}/SKILL.md"; then
        printf '  ORPHAN: %s/reference/%s\n' "${skill}" "${base}" >&2
        orphans=$((orphans + 1))
      fi
    done < <(find "${ref_dir}" -maxdepth 1 -name '*.md' -type f)
  done < <(list_skills)
  printf 'AC4 bidir refs: %d orphan reference files\n' "${orphans}"
  # Soft check — orphans are warnings, not failures.
  ok "AC4 bidir refs scanned (${orphans} orphans, advisory)"
}

check_audit_coverage() {
  [[ -f "${REPORTS_DIR}/audit.md" ]] || fail "AC5: audit.md missing"
  local total covered
  total=$(list_skills | wc -l | tr -d ' ')
  covered=$(grep -cE '^## audit:' "${REPORTS_DIR}/audit.md" 2>/dev/null || echo 0)
  printf 'AC5 audit coverage: %d/%d\n' "${covered}" "${total}"
  (( covered >= total )) || fail "AC5: ${covered}/${total} skills audited"
  ok "AC5 full audit coverage"
}

check_improvements() {
  [[ -f "${REPORTS_DIR}/improvements.md" ]] || fail "AC6: improvements.md missing"
  local sections
  sections=$(grep -cE '^## improvements:' "${REPORTS_DIR}/improvements.md" 2>/dev/null || echo 0)
  (( sections > 0 )) || fail "AC6: improvements.md has zero sections"
  ok "AC6 improvements has ${sections} sections"
}

check_injection_annotations() {
  # AC7: every URL appearing in a Sources block must carry an injection-check tag.
  [[ -f "${REPORTS_DIR}/audit.md" ]] || { ok "AC7 skipped (audit.md missing)"; return 0; }
  local urls_total urls_annotated missing
  # URLs are listed under "Sources:" lines as "  - <url> — injection-check: ..."
  urls_total=$(grep -E '^[[:space:]]*-[[:space:]]+https?://' "${REPORTS_DIR}/audit.md" | wc -l | tr -d ' ')
  urls_annotated=$(grep -E '^[[:space:]]*-[[:space:]]+https?://.+injection-check:' "${REPORTS_DIR}/audit.md" | wc -l | tr -d ' ')
  missing=$(( urls_total - urls_annotated ))
  printf 'AC7 injection annotations: %d/%d urls annotated\n' "${urls_annotated}" "${urls_total}"
  (( missing == 0 )) || fail "AC7: ${missing} urls missing injection-check"
  ok "AC7 every URL has injection-check annotation"
}

case "${1:-all}" in
  check-common-refs)             check_common_refs ;;
  check-reference-map)           check_reference_map ;;
  check-bidir-refs)              check_bidir_refs ;;
  check-audit-coverage)          check_audit_coverage ;;
  check-improvements)            check_improvements ;;
  check-injection-annotations)   check_injection_annotations ;;
  all)
    check_common_refs
    check_reference_map
    check_bidir_refs
    check_audit_coverage
    check_improvements
    check_injection_annotations
    printf '\n[verify] ALL ACs PASS\n'
    ;;
  *) printf 'unknown: %s\n' "$1" >&2; exit 64 ;;
esac
