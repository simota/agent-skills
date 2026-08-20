#!/usr/bin/env python3
"""
Lint `_common/LESSONS.md` -- the register of failures that have been mechanised.

The register exists to hold exactly one kind of entry: a failure that happened,
paired with the thing that now catches it. Its whole value is the refusal. A
register that accepts "remember to check the count" records the same intention
that failed the first time, while reading like an enforcement -- and that is
strictly worse than no register, because it stops anyone from looking for the
mechanism that is missing.

Checks:

  LS-1  Every row carries a mechanism. An empty cell is a lesson nobody is keeping.
  LS-2  The mechanism is not an intention. "Remember to", "be careful", "always
        try to", "make sure", "should" -- phrasings that describe a disposition
        rather than a check. This is the rule the file exists for.
  LS-3  `Where` resolves to a file in this repository. A mechanism living
        nowhere is an intention with a filename attached.
  LS-4  `F` is one of F1/F2/F3/F4 (`_common/HARNESS_DEBT.md` s 3b). A closed
        vocabulary is what makes the column countable.
  LS-5  IDs are `L###`, unique, and never reused.
  LS-6  `Added` parses as an ISO date and is not in the future.
  LS-7  A row past `LESSON_AGE_DAYS` is re-justified or deleted (advisory).

Severity tiers:
  --severity warning  (default)  print findings, exit 0
  --severity error    exit 1 if any P0/P1 finding is reported

Usage:
  python3 _common/scripts/lint-lessons.py --severity error
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTER = REPO_ROOT / "_common" / "LESSONS.md"

#: A row past this age is re-justified against the current corpus or deleted.
#: Advisory, not blocking: an old lesson is not automatically a wrong one.
LESSON_AGE_DAYS = 365

FAILURE_CLASSES = {"F1", "F2", "F3", "F4"}
ID_PATTERN = re.compile(r"^L\d{3}$")

#: Phrasings that describe a disposition rather than a check. Matched against a
#: lowercased mechanism with backticked code spans stripped, so a mechanism that
#: legitimately quotes such a phrase from a rule it enforces is not caught by
#: its own quotation.
INTENTION_PHRASES = (
    "remember to", "be careful", "always try", "try to remember", "make sure",
    "keep in mind", "don't forget", "do not forget", "take care to", "be sure to",
    "we should", "one should", "agents should", "should always", "should remember",
    "aim to", "strive to", "be mindful", "pay attention", "bear in mind",
)

#: The register's own table. A row is six pipe-separated cells.
ROW = re.compile(r"^\|\s*(L\d{3}|L[^|]*?)\s*\|(.+)\|\s*$")


def strip_code(text: str) -> str:
    return re.sub(r"`[^`]*`", " ", text)


def parse_rows(text: str) -> list[tuple[int, list[str]]]:
    """(line number, cells) for every register row, ignoring the header and rules table."""
    rows = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and ID_PATTERN.match(cells[0] or ""):
            rows.append((lineno, cells))
    return rows


def check(text: str) -> list[tuple[str, str, str]]:
    findings: list[tuple[str, str, str]] = []
    rows = parse_rows(text)
    if not rows:
        findings.append(("P1", "LS-5", "LESSONS.md has no parseable register rows -- has the table shape changed?"))
        return findings

    today = dt.date.today()
    seen: dict[str, int] = {}

    for lineno, cells in rows:
        if len(cells) != 6:
            findings.append(("P1", "LS-5", f"L{lineno}: row has {len(cells)} cells, expected 6"))
            continue
        ident, what, failure, mechanism, where, added = cells

        if ident in seen:
            findings.append(("P0", "LS-5", f"line {lineno}: id {ident} reused (first seen line {seen[ident]})"))
        seen[ident] = lineno

        if not what:
            findings.append(("P1", "LS-1", f"{ident}: no description of what happened"))

        if failure.strip("`") not in FAILURE_CLASSES:
            findings.append((
                "P1", "LS-4",
                f"{ident}: failure class {failure!r} is not one of F1/F2/F3/F4 "
                f"(`_common/HARNESS_DEBT.md` s 3b)",
            ))

        if not mechanism:
            findings.append((
                "P0", "LS-1",
                f"{ident}: no mechanism. A lesson with no mechanism is a hope -- "
                f"find the check, or delete the row and admit nobody is keeping it",
            ))
        else:
            lowered = strip_code(mechanism).lower()
            for phrase in INTENTION_PHRASES:
                if phrase in lowered:
                    findings.append((
                        "P0", "LS-2",
                        f"{ident}: mechanism reads as an intention ({phrase!r}), not a check. "
                        f"Either something enforces it or the row does not belong here",
                    ))
                    break

        if not where:
            findings.append(("P1", "LS-3", f"{ident}: no `Where` -- name the file that carries the mechanism"))
        else:
            target = where.strip("`")
            if not (REPO_ROOT / target).exists():
                findings.append((
                    "P0", "LS-3",
                    f"{ident}: mechanism lives at `{target}`, which does not exist -- "
                    f"the mechanism was deleted or moved and the lesson is no longer kept",
                ))

        try:
            when = dt.date.fromisoformat(added)
        except ValueError:
            findings.append(("P1", "LS-6", f"{ident}: `Added` {added!r} is not an ISO date"))
        else:
            if when > today:
                findings.append(("P1", "LS-6", f"{ident}: `Added` {added} is in the future"))
            elif (today - when).days > LESSON_AGE_DAYS:
                findings.append((
                    "P2", "LS-7",
                    f"{ident}: added {(today - when).days} days ago (> {LESSON_AGE_DAYS}) -- "
                    f"re-justify against the current corpus or delete",
                ))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--severity", choices=["warning", "error"], default="warning")
    args = parser.parse_args()

    if not REGISTER.exists():
        print(f"lint-lessons: {REGISTER.relative_to(REPO_ROOT)} not found")
        return 1

    text = REGISTER.read_text(encoding="utf-8")
    findings = check(text)

    if not findings:
        print(f"lint-lessons: OK ({len(parse_rows(text))} lessons, all mechanised)")
        return 0

    for severity, rule, message in sorted(findings):
        print(f"[{severity}] {rule}: {message}")

    blocking = [f for f in findings if f[0] in ("P0", "P1")]
    print(f"\n{len(findings)} finding(s), {len(blocking)} blocking")
    return 1 if args.severity == "error" and blocking else 0


if __name__ == "__main__":
    sys.exit(main())
