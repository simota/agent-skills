#!/usr/bin/env python3
"""
Routing Oracle — mechanical reliability checks for Nexus's routing machinery.

Four checks, all fail-open (S4: a script crash prints a warning and exits 0,
it never blocks a merge on its own bug):

  RO-1 Dead-reference check
       Every `reference/*.md` / `_common/*.md` path cited inside nexus/SKILL.md
       and nexus/reference/*.md must exist on disk. Catches a renamed/deleted
       file left dangling in prose (e.g. the routing-quick-start.md retirement).

  RO-2 Ladder token-order assertion
       nexus/SKILL.md's Auto Classify Chain Template cell must contain
       REDIRECT before SELECT before LADDER (in that relative order), and
       nexus/reference/routing-matrix.md's LADDER clause must mention
       `compass` before `architect` (the ladder is compass-first,
       architect-second, never the reverse).

  RO-3 Producer != verifier check
       In nexus/reference/routing-matrix.md's Primary Chain / Recipe Hints
       columns, whenever a step is annotated `[...verify...]`, the agent
       name immediately before it in the same chain must differ from the
       verifying agent's name — a step cannot self-verify its own output.

  RO-4 Fallback-taken field presence
       nexus/reference/output-formats.md's NEXUS_COMPLETE template must
       contain a `Fallback:` line naming the `fallback_taken` field, and
       that line must enumerate all three enum values (compass-invoked,
       architect-invoked, neither) — catches the LADDER outcome silently
       going unreported in the final handoff.

Usage:
  python3 _common/scripts/routing-oracle.py [--severity warning|error|strict]

Severity tiers (mirrors lint-frontmatter.py / validate-recipes.py):
  --severity warning  (default)  print findings, exit 0
  --severity error    exit 1 if any ERROR-level finding is reported
  --severity strict   exit 1 if any finding (ERROR or WARNING) is reported

Fail-open contract: any unhandled exception during a check is caught, printed
as a single WARNING line, and the check is skipped — this script must never
be the reason a routing-machinery PR is blocked by its own bug.

Exit codes:
  0  no blocking findings under the chosen severity (including "script broke")
  1  blocking findings present
"""

from __future__ import annotations

import argparse
import re
import sys
import traceback
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
NEXUS_DIR = REPO_ROOT / "nexus"
NEXUS_SKILL = NEXUS_DIR / "SKILL.md"
ROUTING_MATRIX = NEXUS_DIR / "reference" / "routing-matrix.md"
OUTPUT_FORMATS = NEXUS_DIR / "reference" / "output-formats.md"

# Matches backticked or plain relative paths under reference/ or _common/ ending .md,
# with an optional leading `<skill-name>/` segment (e.g. `port/reference/x.md`).
REF_PATH_RE = re.compile(r"`?((?:[a-z][a-z0-9_-]*/)?(?:reference|_common)/[A-Za-z0-9_\-{}/.,]+?\.md)`?")


class Finding:
    def __init__(self, check: str, level: str, message: str):
        self.check = check
        self.level = level  # ERROR | WARNING
        self.message = message

    def __str__(self) -> str:
        return f"[{self.level}] {self.check}: {self.message}"


def safe_check(fn, findings: list[Finding]):
    """Run a check function; on any exception, fail open with a WARNING, never raise."""
    try:
        fn(findings)
    except Exception as e:  # noqa: BLE001 - intentional catch-all, fail-open contract
        findings.append(Finding(
            fn.__name__, "WARNING",
            f"check crashed and was skipped (fail-open): {e.__class__.__name__}: {e}",
        ))
        traceback.print_exc(file=sys.stderr)


def _resolve_ref(raw_path: str, referencing_file: Path) -> Path:
    """Resolve a cited path to an absolute file.
    - `_common/X.md` and `<skill>/reference/X.md` (leading skill-name segment present)
      are always repo-root-relative.
    - Bare `reference/X.md` (no leading skill-name segment) is relative to the skill
      folder containing the referencing file (e.g. cited from within nexus/ itself)."""
    if raw_path.startswith("_common/") or not raw_path.startswith("reference/"):
        return REPO_ROOT / raw_path
    skill_dir = referencing_file.parent if referencing_file.parent.name != "reference" else referencing_file.parent.parent
    return skill_dir / raw_path


def check_dead_references(findings: list[Finding]):
    """RO-1: every reference/*.md or _common/*.md path cited in nexus/ docs must exist."""
    files_to_scan = [NEXUS_SKILL] + sorted((NEXUS_DIR / "reference").glob("*.md"))
    checked = 0
    for f in files_to_scan:
        if not f.is_file():
            continue
        content = f.read_text(encoding="utf-8")
        for m in REF_PATH_RE.finditer(content):
            raw_path = m.group(1)
            # Skip glob/brace patterns used as shorthand for "several files"
            # (e.g. `reference/{a,b,c}-recipe.md`) — not a single resolvable path.
            if "{" in raw_path or "}" in raw_path:
                continue
            checked += 1
            candidate = _resolve_ref(raw_path, f)
            if candidate.is_file():
                continue
            # Fallback: some prose uses an implicit-prefix shorthand — e.g.
            # "`quest/SKILL.md` (+ `reference/game-design-document.md`, ...)"
            # means the reference/ file belongs to the just-named quest/ skill,
            # not to the citing file's own skill dir. Before flagging a true
            # dead link, check whether exactly one same-named file exists
            # anywhere else in the repo under a reference/ dir.
            basename = Path(raw_path).name
            elsewhere = [p for p in REPO_ROOT.rglob(f"reference/{basename}") if p.is_file()]
            if len(elsewhere) == 1:
                continue  # shorthand cross-skill reference, resolvable elsewhere — not dead
            findings.append(Finding(
                "RO-1", "ERROR",
                f"{f.relative_to(REPO_ROOT)} references `{raw_path}` — file not found "
                f"(resolved to {candidate.relative_to(REPO_ROOT)}"
                + (f"; {len(elsewhere)} same-named files exist elsewhere, ambiguous" if elsewhere else "")
                + ")",
            ))
    if checked == 0:
        findings.append(Finding("RO-1", "WARNING", "no reference/_common paths found to check — regex may be stale"))


def check_ladder_token_order(findings: list[Finding]):
    """RO-2: REDIRECT before SELECT before LADDER in the classify chain template;
    compass before architect in the LADDER clause."""
    skill_content = NEXUS_SKILL.read_text(encoding="utf-8")
    m = re.search(r"\|\s*Auto Classify\s*\|.*?\|\s*(`[^`]+`)\s*\|", skill_content)
    if not m:
        findings.append(Finding("RO-2", "WARNING", "Auto Classify row not found in nexus/SKILL.md Recipes table — token-order check skipped"))
        return
    chain_template = m.group(1)
    tokens = ["REDIRECT", "SELECT", "LADDER"]
    positions = []
    for t in tokens:
        idx = chain_template.find(t)
        if idx == -1:
            findings.append(Finding("RO-2", "ERROR", f"token `{t}` missing from Auto Classify Chain Template: {chain_template}"))
            return
        positions.append(idx)
    if positions != sorted(positions):
        findings.append(Finding("RO-2", "ERROR", f"token order violated in Chain Template (expected REDIRECT < SELECT < LADDER): {chain_template}"))

    if not ROUTING_MATRIX.is_file():
        findings.append(Finding("RO-2", "WARNING", "routing-matrix.md not found — compass/architect order check skipped"))
        return
    matrix_content = ROUTING_MATRIX.read_text(encoding="utf-8")
    ladder_match = re.search(r"\*\*LADDER \(no task-type match.*?\*\*\s*—\s*(.*?)(?:\n- \*\*Multi-domain|\n\n)", matrix_content, re.DOTALL)
    if not ladder_match:
        findings.append(Finding("RO-2", "WARNING", "LADDER clause not found in routing-matrix.md — compass/architect order check skipped"))
        return
    ladder_text = ladder_match.group(1)
    compass_idx = ladder_text.find("compass")
    architect_idx = ladder_text.find("architect")
    if compass_idx == -1 or architect_idx == -1:
        findings.append(Finding("RO-2", "ERROR", "LADDER clause must mention both `compass` and `architect`"))
        return
    if not (compass_idx < architect_idx):
        findings.append(Finding("RO-2", "ERROR", "LADDER clause must invoke compass before architect (compass-first, architect-second)"))


# RO-3 reviewed exceptions: (Recipe name, agent) pairs where a same-agent
# verify step was reviewed and accepted as an intentional self-contained
# continuous-measurement loop, not a producer grading its own correctness
# claim without independent review. Keep this list short and each entry
# reviewed — it downgrades the finding's message, not its WARNING severity.
RO3_REVIEWED_EXCEPTIONS = {
    # Pixel re-measures its own fidelity gap after remediation (gap -> verify
    # is the same specialist re-running its own audit instrument, matching
    # DESIGN_AUDIT's documented gap-report -> remediation -> re-audit loop).
    ("DESIGN_AUDIT", "Pixel"),
    # Bolt's auto-tuning loop re-profiles after each parameter change
    # (profile -> tuning-loop -> verify), matching OPTIMIZE's own documented
    # ITERATE re-profile pattern rather than a missing independent verifier.
    ("AUTO_TUNING", "Bolt"),
}


def check_producer_verifier(findings: list[Finding]):
    """RO-3: in a chain's Recipe Hints list, the agent immediately preceding a
    `[...verify...]`-annotated step must not be the same agent as the verifier."""
    if not ROUTING_MATRIX.is_file():
        findings.append(Finding("RO-3", "WARNING", "routing-matrix.md not found — producer/verifier check skipped"))
        return
    content = ROUTING_MATRIX.read_text(encoding="utf-8")
    rows_checked = 0
    for line in content.splitlines():
        if not line.startswith("|") or line.strip().startswith("|---") or "Recipe Hints" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        recipe_hints = cells[2]
        # Steps look like "Agent[annotation]" separated by commas.
        steps = re.findall(r"([A-Za-z][A-Za-z0-9]*)\[([^\]]*)\]", recipe_hints)
        if not steps:
            continue
        rows_checked += 1
        for i, (agent, annotation) in enumerate(steps):
            if "verify" not in annotation.lower():
                continue
            if i == 0:
                continue  # verify step with nothing before it in this list — not a self-verify risk
            prev_agent, _ = steps[i - 1]
            if prev_agent == agent:
                # WARNING not ERROR: a same-agent verify step can be a legitimate
                # self-contained continuous-measurement loop rather than a
                # producer grading its own correctness claim. Surface for
                # human review; don't hard-block on a pattern this heuristic
                # can't structurally distinguish from an intentional design.
                if (cells[0], agent) in RO3_REVIEWED_EXCEPTIONS:
                    findings.append(Finding(
                        "RO-3", "WARNING",
                        f"{cells[0]}: same-agent verify — `{prev_agent}` immediately precedes its own "
                        f"`{agent}[{annotation}]` verify step in Recipe Hints: {recipe_hints} "
                        f"(reviewed exception — accepted self-measurement loop, see RO3_REVIEWED_EXCEPTIONS)",
                    ))
                else:
                    findings.append(Finding(
                        "RO-3", "WARNING",
                        f"{cells[0]}: same-agent verify — `{prev_agent}` immediately precedes its own "
                        f"`{agent}[{annotation}]` verify step in Recipe Hints: {recipe_hints} "
                        f"(review: is this a self-contained measurement loop, or a missing independent verifier?)",
                    ))
    if rows_checked == 0:
        findings.append(Finding("RO-3", "WARNING", "no bracket-annotated Recipe Hints rows found — producer/verifier check may be stale vs table format"))


def check_fallback_field(findings: list[Finding]):
    """RO-4: the NEXUS_COMPLETE template in output-formats.md must carry a
    `Fallback:` line naming the `fallback_taken` field with all three enum
    values, so the LADDER outcome (compass-invoked / architect-invoked /
    neither) can never go silently unreported in the final handoff."""
    if not OUTPUT_FORMATS.is_file():
        findings.append(Finding("RO-4", "WARNING", "output-formats.md not found — fallback-field check skipped"))
        return
    content = OUTPUT_FORMATS.read_text(encoding="utf-8")
    m = re.search(r"## NEXUS_COMPLETE\b.*?```(.*?)```", content, re.DOTALL)
    if not m:
        findings.append(Finding("RO-4", "WARNING", "NEXUS_COMPLETE template block not found — fallback-field check skipped"))
        return
    template = m.group(1)
    if "fallback_taken" not in template or "Fallback:" not in template:
        findings.append(Finding("RO-4", "ERROR", "NEXUS_COMPLETE template is missing the `Fallback:` / `fallback_taken` field"))
        return
    required_values = ("compass-invoked", "architect-invoked", "neither")
    missing = [v for v in required_values if v not in template]
    if missing:
        findings.append(Finding(
            "RO-4", "ERROR",
            f"NEXUS_COMPLETE template's Fallback field is missing enum value(s): {', '.join(missing)}",
        ))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", choices=("warning", "error", "strict"), default="warning")
    args = parser.parse_args()

    findings: list[Finding] = []
    safe_check(check_dead_references, findings)
    safe_check(check_ladder_token_order, findings)
    safe_check(check_producer_verifier, findings)
    safe_check(check_fallback_field, findings)

    errors = [f for f in findings if f.level == "ERROR"]
    warnings = [f for f in findings if f.level == "WARNING"]

    for f in findings:
        print(str(f))
    print()
    print(f"Routing Oracle: {len(errors)} errors | {len(warnings)} warnings")

    if args.severity == "warning":
        return 0
    if args.severity == "error":
        return 1 if errors else 0
    return 1 if (errors or warnings) else 0  # strict


if __name__ == "__main__":
    sys.exit(main())
