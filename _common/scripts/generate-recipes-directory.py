#!/usr/bin/env python3
"""
Regenerate `compass/reference/recipes-directory.md` from every SKILL.md `## Recipes` table.

Format: `- **{skill}**: {sub}★ / {sub} / ...` alphabetical by skill name.
The ★ marker indicates the Default Recipe (✓ in the Default? column).

Run after any Recipe/Subcommand change. Idempotent.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = SKILLS_ROOT / "compass" / "references" / "recipes-directory.md"
SKIP_DIRS = {"_common", "_templates"}

HEADER = """# Recipes Directory

Catalog of every skill's Subcommand (Recipe) list. Default Recipe marked with ★.

Canonical protocol: `_common/RECIPES.md`. Per-skill detail lives in each `SKILL.md` `## Recipes` table.

Invocation: `/<skill> <subcommand> [args]`. Without a matching first token, the default Recipe is activated (backward compatible).

Regenerate with: `python3 _common/scripts/generate-recipes-directory.py`

---
"""

FOOTER_TEMPLATE = """
---

**Total**: {count} skills with Recipes.

Auto-generated from SKILL.md `## Recipes` tables by `_common/scripts/generate-recipes-directory.py`. Do not edit by hand.
"""


def extract_recipes(content: str) -> list[tuple[str, bool]]:
    m = re.search(r"^## Recipes\s*\n(.*?)(?=^## )", content, re.MULTILINE | re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    rows: list[tuple[str, bool]] = []
    for row in re.finditer(r"^\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|\s*([^|]*)\s*\|", block, re.MULTILINE):
        name = row.group(1).strip()
        if name.lower() in ("recipe", "---") or name.startswith("-"):
            continue
        subcmd = row.group(2).strip()
        is_default = "✓" in row.group(3)
        rows.append((subcmd, is_default))
    return rows


def main() -> int:
    lines: list[str] = [HEADER]
    count = 0
    for entry in sorted(SKILLS_ROOT.iterdir()):
        if not entry.is_dir() or entry.name in SKIP_DIRS:
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.is_file():
            continue
        recipes = extract_recipes(skill_md.read_text(encoding="utf-8"))
        if not recipes:
            continue
        parts = [f"{sub}★" if is_def else sub for sub, is_def in recipes]
        lines.append(f"- **{entry.name}**: {' / '.join(parts)}")
        count += 1
    lines.append(FOOTER_TEMPLATE.format(count=count))

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {count} skills to {OUTPUT.relative_to(SKILLS_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
