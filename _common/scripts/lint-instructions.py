#!/usr/bin/env python3
"""
Lint repository instruction files (AGENTS.md, CLAUDE.md) for staleness and drift.

Instruction files are read at the start of every session and are rarely re-read by a
human. A number or path that stopped being true does not fail loudly -- it silently
teaches every agent something false. These checks make that failure mode visible.

Checks:

  I1  Skill-count claims in instruction files match the actual corpus.
      Drift here is the canonical HD-DRIFT instance (declared structure vs real corpus).
  I2  Referenced repo-relative paths exist. A pointer to a moved or deleted file
      routes agents to a dead end.
  I3  AGENTS.md and CLAUDE.md do not restate the same rule. AGENTS.md declares
      "tool-specific files should contain only deltas, not duplicates" -- duplicated
      text is what drifts apart later. Reported as a warning (P2), never blocking.

Severity tiers:
  --severity warning  (default)  print findings, exit 0
  --severity error    exit 1 if any P0/P1 finding is reported

Usage:
  python3 _common/scripts/lint-instructions.py
  python3 _common/scripts/lint-instructions.py --severity error
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

INSTRUCTION_FILES = ["AGENTS.md", "CLAUDE.md"]

# Sentences that assert how many skills exist, e.g. "123 specialist skill agents"
# or "123のスキルエージェント".
COUNT_PATTERN = re.compile(r"(\d{2,4})\s*(?:specialist\s+skill\s+agents?|のスキルエージェント)")

# Backtick-quoted repo-relative file references, e.g. `_common/HANDOFF.md`.
#
# Deliberately narrow: a ref counts only if it has a directory part AND a .md suffix.
# Bare filenames (`SKILL.md`, `GEMINI.md`) and directory conventions (`reference/`)
# are naming patterns, not claims that a specific file exists -- flagging them trains
# readers to ignore this lint, which costs more than the coverage it would buy.
PATH_PATTERN = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_.-]+)+\.md)`")


def actual_skill_count() -> int:
    """Directories holding a SKILL.md, excluding infrastructure dirs (_common, _templates)."""
    return sum(
        1
        for p in REPO_ROOT.iterdir()
        if p.is_dir() and not p.name.startswith((".", "_")) and (p / "SKILL.md").is_file()
    )


def check_counts(path: Path, text: str, actual: int) -> list[tuple[str, str, str]]:
    findings = []
    for m in COUNT_PATTERN.finditer(text):
        claimed = int(m.group(1))
        if claimed != actual:
            line = text[: m.start()].count("\n") + 1
            findings.append(
                (
                    "P1",
                    "I1",
                    f"{path.name}:{line} claims {claimed} skills, corpus has {actual}",
                )
            )
    return findings


def check_paths(path: Path, text: str) -> list[tuple[str, str, str]]:
    findings = []
    seen: set[str] = set()
    for m in PATH_PATTERN.finditer(text):
        ref = m.group(1)
        if ref in seen or "*" in ref or ref.startswith("<"):
            continue
        seen.add(ref)
        if not (REPO_ROOT / ref).exists():
            line = text[: m.start()].count("\n") + 1
            findings.append(("P1", "I2", f"{path.name}:{line} references missing path `{ref}`"))
    return findings


def check_duplication(texts: dict[str, str]) -> list[tuple[str, str, str]]:
    """Flag substantial lines that appear verbatim in more than one instruction file."""
    if len(texts) < 2:
        return []
    findings = []
    names = list(texts)
    lines = {
        name: {
            ln.strip()
            for ln in texts[name].splitlines()
            # Long enough to be a rule, not a heading or a list marker.
            if len(ln.strip()) >= 60 and not ln.lstrip().startswith(("#", "|", "```", ">"))
        }
        for name in names
    }
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            for dup in sorted(lines[a] & lines[b]):
                findings.append(
                    ("P2", "I3", f"{a} and {b} both state: {dup[:70]}...")
                )
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--severity", choices=["warning", "error"], default="warning")
    args = ap.parse_args()

    actual = actual_skill_count()
    findings: list[tuple[str, str, str]] = []
    texts: dict[str, str] = {}

    for name in INSTRUCTION_FILES:
        path = REPO_ROOT / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        findings += check_counts(path, text, actual)
        findings += check_paths(path, text)

    findings += check_duplication(texts)

    if not findings:
        print(f"lint-instructions: OK ({actual} skills, {len(texts)} instruction files)")
        return 0

    for sev, rule, msg in sorted(findings):
        print(f"[{sev}] {rule}: {msg}")

    blocking = [f for f in findings if f[0] in ("P0", "P1")]
    print(f"\n{len(findings)} finding(s), {len(blocking)} blocking")
    return 1 if args.severity == "error" and blocking else 0


if __name__ == "__main__":
    sys.exit(main())
