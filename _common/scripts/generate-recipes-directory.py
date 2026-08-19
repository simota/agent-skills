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
PROJECT_LOCAL_ROOT = SKILLS_ROOT / ".claude" / "skills"
OUTPUT = SKILLS_ROOT / "compass" / "reference" / "recipes-directory.md"
SKIP_DIRS = {"_common", "_templates"}

HEADER = """# Recipes Directory

Catalog of every global skill and available project-local extension's Subcommand (Recipe) list. Default Recipe marked with ★.

Project-local entries are sourced from `.claude/skills/`; availability and fallback rules live in `_common/PROJECT_LOCAL_SKILLS.md`.

Canonical protocol: `_common/RECIPES.md`. Per-skill detail lives in each `SKILL.md` `## Recipes` table.

Invocation: `/<skill> <subcommand> [args]`. Without a matching first token, the default Recipe is activated (backward compatible).

Regenerate with: `python3 _common/scripts/generate-recipes-directory.py`

---
"""

FOOTER_TEMPLATE = """
---

**Total**: {count} skills with Recipes ({global_count} global + {local_count} project-local).

Auto-generated from SKILL.md `## Recipes` tables by `_common/scripts/generate-recipes-directory.py`. Do not edit by hand.
"""


def extract_recipes(content: str, skill_dir: Path | None = None) -> list[tuple[str, bool]]:
    m = re.search(r"^## Recipes\s*\n(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL)
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
    if rows or skill_dir is None:
        return rows
    pointer = re.search(r"`(reference/[a-z0-9-]*recipes?-index\.md)`", block)
    if pointer:
        target = skill_dir / pointer.group(1)
        if target.is_file():
            return extract_recipes(target.read_text(encoding="utf-8"), target.parent)
    return rows


def iter_skill_dirs() -> list[tuple[Path, bool]]:
    entries: list[tuple[Path, bool]] = []
    for entry in SKILLS_ROOT.iterdir():
        if not entry.is_dir() or entry.name in SKIP_DIRS or entry.name.startswith("."):
            continue
        if (entry / "SKILL.md").is_file():
            entries.append((entry, False))
    if PROJECT_LOCAL_ROOT.is_dir():
        entries.extend(
            (entry, True)
            for entry in PROJECT_LOCAL_ROOT.iterdir()
            if entry.is_dir() and (entry / "SKILL.md").is_file()
        )
    return sorted(entries, key=lambda item: item[0].name)


def main() -> int:
    lines: list[str] = [HEADER]
    count = 0
    global_count = 0
    local_count = 0
    for entry, is_local in iter_skill_dirs():
        skill_md = entry / "SKILL.md"
        recipes = extract_recipes(skill_md.read_text(encoding="utf-8"), entry)
        if not recipes:
            continue
        parts = [f"{sub}★" if is_def else sub for sub, is_def in recipes]
        lines.append(f"- **{entry.name}**: {' / '.join(parts)}")
        count += 1
        if is_local:
            local_count += 1
        else:
            global_count += 1
    lines.append(FOOTER_TEMPLATE.format(
        count=count,
        global_count=global_count,
        local_count=local_count,
    ))

    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {count} skills to {OUTPUT.relative_to(SKILLS_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
