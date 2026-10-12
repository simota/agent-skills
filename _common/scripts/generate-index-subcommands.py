#!/usr/bin/env python3
"""
Regenerate the `SUBCOMMANDS` block of `index.html` from every SKILL.md `## Recipes` table.

Each entry is `{"n": <subcommand>, "d": <When to Use, up to its first clause break>}`, keyed by the
display name the page's `AGENTS` roster uses. The Recipes tables are the only source; the
page copy is never edited by hand.

Usage:
  python3 _common/scripts/generate-index-subcommands.py          # rewrite index.html
  python3 _common/scripts/generate-index-subcommands.py --check  # exit 1 if it is stale

Lifecycle: failure: the page's recipe list was a hand-kept copy of 835 table rows that
drifted in wording and had to be co-edited with every Recipe change; effect: one source
(the Recipes tables), with `make validate` failing on a stale page; owner: catalog
maintainers; removal: when index.html is no longer published or reads the tables itself.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import _corpus
from _recipes import recipe_cells, recipe_section, registry_pointer

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
PROJECT_LOCAL_ROOT = ROOT / ".claude" / "skills"
SKIP_DIRS = {"_common", "_templates"}
START = "const SUBCOMMANDS = {\n"
END = "\n};\n"
AGENT_NAME = re.compile(r"\{ name: '([^']+)'")


CLAUSE_BREAK = re.compile(r"; |(?<!\be\.g)(?<!\bi\.e)\. ")


def summary(text: str) -> str:
    """The When-to-Use cell up to its first clause or sentence break that leaves markup whole."""
    text = text.replace("\\|", "|").strip()
    for match in CLAUSE_BREAK.finditer(text):
        head = text[:match.start()]
        if head.count("`") % 2 == 0 and head.count("**") % 2 == 0:
            text = head
            break
    return text.rstrip(" .")


def recipe_rows(skill_dir: Path) -> list[dict[str, str]]:
    block = recipe_section((skill_dir / "SKILL.md").read_text(encoding="utf-8")) or ""
    if not list(recipe_cells(block)):
        pointer = registry_pointer(block)
        if pointer:
            block = (skill_dir / pointer).read_text(encoding="utf-8")
    column = when_to_use_column(block)
    rows = []
    for cells in recipe_cells(block):
        match = re.fullmatch(r"`([^`]+)`", cells[1] if len(cells) >= 2 else "")
        if match and len(cells) > column:
            rows.append({"n": match.group(1), "d": summary(cells[column])})
    return rows


def when_to_use_column(block: str) -> int:
    """Tables differ in column order (some add a Mode column); find the header's cell."""
    for line in block.splitlines():
        cells = [cell.strip().lower() for cell in line.strip().strip("|").split("|")]
        if cells[:2] == ["recipe", "subcommand"]:
            return cells.index("when to use") if "when to use" in cells else 3
    return 3


def skill_dirs() -> list[Path]:
    dirs = [
        entry for entry in ROOT.iterdir()
        if entry.name not in SKIP_DIRS and _corpus.is_skill_dir(entry)
    ]
    if PROJECT_LOCAL_ROOT.is_dir():
        dirs.extend(entry for entry in PROJECT_LOCAL_ROOT.iterdir() if _corpus.is_skill_dir(entry))
    return sorted(dirs, key=lambda entry: entry.name)


def render(html: str) -> str:
    names = {name.lower(): name for name in AGENT_NAME.findall(html)}
    lines = []
    for skill_dir in skill_dirs():
        rows = recipe_rows(skill_dir)
        if rows:
            name = names.get(skill_dir.name, skill_dir.name.capitalize())
            body = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
            lines.append(f"  {json.dumps(name)}: {body},")
    start = html.index(START) + len(START)
    end = html.index(END, start)
    return html[:start] + "\n".join(lines) + html[end:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--check", action="store_true", help="exit 1 if index.html is stale")
    args = parser.parse_args()
    html = INDEX.read_text(encoding="utf-8")
    fresh = render(html)
    if args.check:
        if fresh != html:
            print("error: index.html SUBCOMMANDS is stale — run "
                  "python3 _common/scripts/generate-index-subcommands.py", file=sys.stderr)
            return 1
        return 0
    INDEX.write_text(fresh, encoding="utf-8")
    print(f"Wrote SUBCOMMANDS to {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
