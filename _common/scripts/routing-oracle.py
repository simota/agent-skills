#!/usr/bin/env python3
"""
Routing Oracle — mechanical reliability checks for Nexus's routing machinery.

Eight checks, all fail-open (S4: a script crash prints a warning and exits 0,
it never blocks a merge on its own bug):

  RO-1 Dead-reference check
       Every `reference/*.md` / `_common/*.md` path cited inside nexus/SKILL.md
       and nexus/reference/*.md must exist on disk. Catches a renamed/deleted
       file left dangling in prose (e.g. the routing-quick-start.md retirement).

  RO-2 Default-dispatch token-order assertion
       nexus/SKILL.md's explicit `phase:CLASSIFY` Default dispatch must contain
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

  RO-5 Roster completeness
       Every skill directory under the repo root (a directory containing
       a SKILL.md, excluding names starting with `_` or `.`) must appear
       (case-insensitive, word-boundary substring match) in at least one
       of nexus/reference/routing-matrix.md or
       nexus/reference/signal-keywords.md. Catches a live skill that has
       no routing surface at all — the mirror image of RO-1's dead
       reference (a routing mention with no skill behind it).

  RO-6 Bare-subcommand dispatch consistency
       nexus/SKILL.md's Subcommand Dispatch says a first-token match
       skips CLASSIFY. But nexus/reference/task-battery.md carries
       fixtures asserting that certain *bare* subcommands (a Recipe name
       with no object/target) must NOT dispatch silently and must instead
       reach GATE for one clarifying question. Those two rules contradict
       unless Subcommand Dispatch declares a bare-subcommand exception.
       This check asserts (a) the exception clause exists whenever such a
       fixture exists, and (b) no token named by a fixture is also listed
       as exempt from the exception. Found live: `optimize` is both a
       registered subcommand and a battery fixture requiring a GATE.

  RO-7 Retired-reference residue
       Reference files removed during Nexus scope consolidation must stay
       absent, and no Nexus document may cite their retired filenames. The
       owning contracts are routing-matrix, handoff-validation,
       intent-clarification, orchestration-patterns, and apex-recipe.

  RO-8 Confidence-gate shape
       confidence-scoring.md must retain typed blocking unknowns and discrete
       evidence bands, and must not reintroduce the retired source-weight
       arithmetic or fixed clarification bonuses.

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
CONFIDENCE_SCORING = NEXUS_DIR / "reference" / "confidence-scoring.md"

RETIRED_NEXUS_REFERENCES = (
    "agent-communication-anti-patterns.md",
    "apex-walkthrough.md",
    "managed-agents-mapping.md",
    "official-skill-categories.md",
    "orchestration-anti-patterns.md",
    "production-reliability-anti-patterns.md",
    "routing-explanation.md",
    "task-routing-anti-patterns.md",
)

# Matches backticked or plain repo-relative paths under reference/ or _common/
# ending .md. Skill references may use either the global `<skill-name>/` form
# or the canonical project-local `.claude/skills/<skill-name>/` form.
REF_PATH_RE = re.compile(
    r"`?((?:(?:\.claude/skills/)?[a-z][a-z0-9_-]*/)?"
    r"(?:reference|_common)/[A-Za-z0-9_\-{}/.,]+?\.md)`?"
)


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
            # "`architect/SKILL.md` (+ `reference/agent-categories.md`, ...)"
            # means the reference/ file belongs to the just-named architect/ skill,
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
    """RO-2: REDIRECT before SELECT before LADDER in the CLASSIFY Default dispatch;
    compass before architect in the LADDER clause."""
    skill_content = NEXUS_SKILL.read_text(encoding="utf-8")
    m = re.search(
        r"\*\*Default dispatch:\*\*\s*`phase:CLASSIFY`\s+with flow\s+(`[^`]+`)",
        skill_content,
    )
    if not m:
        findings.append(Finding(
            "RO-2", "ERROR",
            "explicit `phase:CLASSIFY` Default dispatch with a flow was not found in nexus/SKILL.md",
        ))
        return
    chain_template = m.group(1)
    tokens = ["REDIRECT", "SELECT", "LADDER"]
    positions = []
    for t in tokens:
        idx = chain_template.find(t)
        if idx == -1:
            findings.append(Finding("RO-2", "ERROR", f"token `{t}` missing from CLASSIFY Default dispatch flow: {chain_template}"))
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


def check_roster_completeness(findings: list[Finding]):
    """RO-5: every skill directory (contains SKILL.md, name not starting with
    `_` or `.`) must appear, case-insensitive word-boundary substring, in at
    least one of routing-matrix.md or signal-keywords.md — the mirror image
    of RO-1's dead-reference check (a live skill with no routing surface)."""
    signal_keywords = NEXUS_DIR / "reference" / "signal-keywords.md"
    if not ROUTING_MATRIX.is_file() or not signal_keywords.is_file():
        findings.append(Finding("RO-5", "WARNING", "routing-matrix.md or signal-keywords.md not found — roster completeness check skipped"))
        return
    combined_text = ROUTING_MATRIX.read_text(encoding="utf-8") + "\n" + signal_keywords.read_text(encoding="utf-8")

    skill_dirs = sorted(
        p.parent.name
        for p in REPO_ROOT.glob("*/SKILL.md")
        if not p.parent.name.startswith("_") and not p.parent.name.startswith(".")
    )
    if not skill_dirs:
        findings.append(Finding("RO-5", "WARNING", "no skill directories with SKILL.md found — roster completeness check may be stale vs repo layout"))
        return

    orphans = []
    for name in skill_dirs:
        pattern = re.compile(r"\b" + re.escape(name) + r"\b", re.IGNORECASE)
        if not pattern.search(combined_text):
            orphans.append(name)

    if orphans:
        findings.append(Finding(
            "RO-5", "WARNING",
            f"{len(orphans)} skill(s) with no routing surface in routing-matrix.md or signal-keywords.md: {', '.join(orphans)}",
        ))


def check_bare_subcommand_dispatch(findings: list[Finding]):
    """RO-6: task-battery fixtures of the form `bare "<token>"` assert that a
    bare Recipe subcommand must reach GATE instead of dispatching silently.
    SKILL.md's Subcommand Dispatch must therefore carry a bare-subcommand
    exception, and must not list any such token as exempt from it."""
    battery = NEXUS_DIR / "reference" / "task-battery.md"
    if not NEXUS_SKILL.is_file() or not battery.is_file():
        findings.append(Finding("RO-6", "WARNING", "nexus/SKILL.md or task-battery.md not found — bare-subcommand check skipped"))
        return

    skill_text = NEXUS_SKILL.read_text(encoding="utf-8")

    # The dispatch allowlist is the fenced block inside the Recipe Registry section.
    registry = re.search(r"dispatch allowlist only.*?```\n(.*?)```", skill_text, re.S)
    if not registry:
        findings.append(Finding("RO-6", "WARNING", "Recipe Registry allowlist block not found in nexus/SKILL.md — bare-subcommand check skipped"))
        return
    subcommands = {t.rstrip("*") for t in registry.group(1).split()}

    # Fixtures written as: bare "optimize" / bare "landing page"
    fixtures = {m.lower() for m in re.findall(r'bare\s+"([^"]+)"', battery.read_text(encoding="utf-8"))}
    contested = sorted(f for f in fixtures if f in subcommands)
    if not contested:
        return  # no fixture asserts a bare subcommand must not dispatch — nothing to enforce

    dispatch = re.search(r"^## Subcommand Dispatch$(.*?)^## ", skill_text, re.S | re.M)
    if not dispatch:
        findings.append(Finding("RO-6", "WARNING", "`## Subcommand Dispatch` section not found in nexus/SKILL.md — bare-subcommand check skipped"))
        return
    section = dispatch.group(1)

    # Require the exception's DEFINITION (a bolded bullet lead-in), not merely a
    # cross-reference to it — a surviving "see the bare-subcommand exception below"
    # must not satisfy the check after the defining bullet has been deleted.
    defined = re.search(r"\*\*Bare-subcommand exception[.:]?\*\*", section)
    if not (defined and re.search(r"\bGATE\b", section)):
        findings.append(Finding(
            "RO-6", "ERROR",
            "Subcommand Dispatch skips CLASSIFY on a first-token match, but task-battery.md requires "
            f"bare {', '.join('`' + c + '`' for c in contested)} to reach GATE instead of dispatching silently. "
            "Subcommand Dispatch must define a **Bare-subcommand exception** routing them to GATE, "
            "or the fixture(s) must be retired.",
        ))
        return

    # The exception's own exempt list must not re-admit a contested token.
    exempt_clause = re.search(r"\*\*Exempt\*\*[^.]*?:\s*(.+?)(?:\.|$)", section, re.S)
    if exempt_clause:
        exempt = {t.lower() for t in re.findall(r"`([a-z][a-z0-9-]*)`", exempt_clause.group(1))}
        clashes = sorted(exempt & set(contested))
        if clashes:
            findings.append(Finding(
                "RO-6", "ERROR",
                f"bare-subcommand exception lists {', '.join('`' + c + '`' for c in clashes)} as exempt, "
                "but task-battery.md has a fixture requiring the same token to reach GATE — contradiction.",
            ))


def check_retired_reference_residue(findings: list[Finding]):
    """RO-7: consolidated Nexus references must not be recreated or cited."""
    reference_dir = NEXUS_DIR / "reference"
    files_to_scan = [NEXUS_SKILL] + sorted(reference_dir.glob("*.md"))
    residue: list[str] = []

    for name in RETIRED_NEXUS_REFERENCES:
        if (reference_dir / name).exists():
            residue.append(f"retired file exists: nexus/reference/{name}")
        for path in files_to_scan:
            if path.name == name:
                continue
            if name in path.read_text(encoding="utf-8"):
                residue.append(f"{path.relative_to(REPO_ROOT)} cites retired `{name}`")

    if residue:
        findings.append(Finding("RO-7", "ERROR", "; ".join(residue)))


def check_confidence_gate_shape(findings: list[Finding]):
    """RO-8: confidence stays typed/discrete instead of pseudo-precise."""
    if not CONFIDENCE_SCORING.is_file():
        findings.append(Finding("RO-8", "ERROR", "nexus/reference/confidence-scoring.md is missing"))
        return

    text = CONFIDENCE_SCORING.read_text(encoding="utf-8")
    required = ("## Blocking Unknown Gate", "## Discrete Evidence Bands", "`authority`")
    missing = [token for token in required if token not in text]
    retired_patterns = {
        "source-weight formula": r"git_score\s*[×*]\s*0\.30",
        "fixed clarification bonus": r"(?:boost|bonus)[^\n]*\+0\.20",
        "weighted source table": r"\|\s*Source\s*\|\s*Weight\s*\|",
    }
    returned = [label for label, pattern in retired_patterns.items() if re.search(pattern, text, re.IGNORECASE)]

    if missing or returned:
        parts = []
        if missing:
            parts.append("missing " + ", ".join(missing))
        if returned:
            parts.append("retired construct returned: " + ", ".join(returned))
        findings.append(Finding("RO-8", "ERROR", "; ".join(parts)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", choices=("warning", "error", "strict"), default="warning")
    args = parser.parse_args()

    findings: list[Finding] = []
    safe_check(check_dead_references, findings)
    safe_check(check_ladder_token_order, findings)
    safe_check(check_producer_verifier, findings)
    safe_check(check_fallback_field, findings)
    safe_check(check_roster_completeness, findings)
    safe_check(check_bare_subcommand_dispatch, findings)
    safe_check(check_retired_reference_residue, findings)
    safe_check(check_confidence_gate_shape, findings)

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
