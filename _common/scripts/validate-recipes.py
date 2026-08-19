#!/usr/bin/env python3
"""
Recipes / Subcommand Dispatch validator.

Validates every SKILL.md against the rules defined in `_common/RECIPES.md`:
  R-REC-01: Exactly one fallback owner per skill with Recipes: one Default Recipe
            (✓) or one explicit Default dispatch phase/workflow (ERROR)
  R-REC-02: Subcommand names are kebab-case, 2-16 chars (ERROR)
  R-REC-03: Reserved words (default/auto/help/list) unused (ERROR)
  R-REC-04: Recipe count, tiered (calibrated 2026-07-03 against 132-skill corpus):
            8-10 recipes → INFO (corpus norm band, ≤10 = P95);
            11+ recipes → WARNING (consolidation review candidate);
            hub skills (HUB_SKILLS) → always INFO (recipe breadth by design)
  R-REC-05: Recipes section is RECOMMENDED for Tier 1-2 skills (INFO)

Plus heading integrity:
  H-REC-01: `## Subcommand Dispatch` heading exists alongside `## Recipes` (ERROR)
  H-REC-02: Heading is bare `## Subcommand Dispatch` — no parenthetical suffix (ERROR)

Usage:
  python3 _common/scripts/validate-recipes.py [--severity warning|error|strict]
                                              [--changed-only]  # only skills whose SKILL.md changed vs HEAD

Severity tiers (mirrors lint-frontmatter.py):
  --severity warning  (default)  print findings, exit 0
  --severity error    exit 1 if any ERROR-level finding is reported
  --severity strict   exit 1 if any finding (ERROR or WARNING) is reported

Exit code: 0 if no ERROR-level violations under the chosen severity, 1 otherwise.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
PROJECT_LOCAL_ROOT = SKILLS_ROOT / ".claude" / "skills"
SKIP_DIRS = {"_common", "_templates"}
RESERVED = {"default", "auto", "help", "list"}
KEBAB = re.compile(r"^[a-z0-9][a-z0-9-]{1,19}$")
MAX_RECIPES = 7  # recommended ceiling (scannability)
WARN_RECIPES = 10  # corpus P95 as of 2026-07-03 (125/132 skills ≤ 10); >10 warns
HUB_SKILLS = {"nexus"}  # ecosystem hub: routes 130+ agents, recipe breadth by design


def changed_skill_names() -> set[str]:
    """Skill folder names whose SKILL.md changed vs HEAD. Empty set on any git error (fail-open)."""
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=str(SKILLS_ROOT), check=True, capture_output=True, text=True,
        ).stdout.strip().splitlines()
    except Exception:
        return set()
    names = set()
    for p in out:
        path = Path(p)
        if path.name == "SKILL.md" and len(path.parts) >= 2:
            names.add(path.parts[-2])
    return names


def iter_skills(only: set[str] | None = None):
    roots = [SKILLS_ROOT]
    if PROJECT_LOCAL_ROOT.is_dir():
        roots.append(PROJECT_LOCAL_ROOT)
    entries = []
    for root in roots:
        for entry in root.iterdir():
            if not entry.is_dir() or entry.name in SKIP_DIRS or entry.name.startswith("."):
                continue
            if only is not None and entry.name not in only:
                continue
            skill_md = entry / "SKILL.md"
            if skill_md.is_file():
                entries.append((entry.name, skill_md))
    yield from sorted(entries, key=lambda item: item[0])


def extract_recipes_block(content: str, skill_dir=None) -> str | None:
    m = re.search(r"^## Recipes\s*\n(.*?)(?=^## )", content, re.MULTILINE | re.DOTALL)
    if m is None:
        return None
    block = m.group(1)
    # A skill whose Recipes table has outgrown the SKILL.md size ceiling may keep
    # the table in a sibling registry file and carry only a dispatch allowlist
    # here (`_common/RECIPES.md` "Externalized registry"). Follow the pointer so
    # the table is validated wherever it lives.
    if skill_dir is not None and not re.search(r"^\|\s*Recipe\s*\|", block, re.MULTILINE):
        ptr = re.search(r"`(reference/[a-z0-9-]*recipes?-index\.md)`", block)
        if ptr:
            target = skill_dir / ptr.group(1)
            if target.is_file():
                return target.read_text(encoding="utf-8")
    return block


def parse_rows(block: str):
    # Parse only the recipes table itself (header contains Recipe + Subcommand
    # columns). The Recipes section may also hold keyword-routing tables whose
    # second cell is a backtick-wrapped subcommand; parsing those produced
    # false-positive R-REC-02 duplicates and inflated R-REC-04 counts.
    lines = block.splitlines()
    rows = []
    in_table = False
    for line in lines:
        if not line.lstrip().startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not in_table:
            if len(cells) >= 2 and "recipe" in cells[0].lower() and "subcommand" in cells[1].lower():
                in_table = True
            continue
        if cells[0].startswith("-") or set(cells[0]) <= {"-", ":", " "}:
            continue
        m = re.match(r"^`([^`]+)`$", cells[1]) if len(cells) >= 2 else None
        if m:
            rows.append((cells[0], m.group(1).strip(), cells[2] if len(cells) >= 3 else ""))
    return rows


def heading_issues(content: str) -> list[str]:
    issues = []
    has_recipes = re.search(r"^## Recipes\s*$", content, re.MULTILINE) is not None
    has_dispatch = re.search(r"^## Subcommand Dispatch\s*$", content, re.MULTILINE) is not None
    decorated = re.findall(r"^## Subcommand Dispatch .+$", content, re.MULTILINE)
    if has_recipes and not has_dispatch:
        issues.append("H-REC-01: `## Recipes` present but `## Subcommand Dispatch` missing")
    if decorated:
        issues.append(f"H-REC-02: decorated heading found (expected bare `## Subcommand Dispatch`): {decorated[0]!r}")
    return issues


def default_dispatches(content: str) -> list[str]:
    """Return valid explicit Default dispatch declarations from Subcommand Dispatch."""
    section = re.search(r"^## Subcommand Dispatch\s*$\n(.*?)(?=^## |\Z)", content,
                        re.MULTILINE | re.DOTALL)
    if section is None:
        return []
    return re.findall(
        r"^\*\*Default dispatch:\*\*\s*`((?:phase|workflow):[A-Za-z][A-Za-z0-9_-]*)`",
        section.group(1), re.MULTILINE,
    )


def validate(skill: str, path: Path) -> tuple[list[str], list[str], list[str]]:
    content = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    errors.extend(heading_issues(content))

    block = extract_recipes_block(content, path.parent)
    if block is None:
        infos.append("R-REC-05: no `## Recipes` section (RECOMMENDED for Tier 1-2)")
        return errors, warnings, infos

    rows = parse_rows(block)
    if not rows:
        errors.append("R-REC-01: `## Recipes` table has no rows")
        return errors, warnings, infos

    recipe_defaults = sum(1 for _, _, default in rows if "✓" in default)
    dispatch_defaults = len(default_dispatches(content))
    fallback_owners = recipe_defaults + dispatch_defaults
    if fallback_owners != 1:
        errors.append(
            "R-REC-01: exactly one fallback owner required "
            f"(Default Recipe ✓ or explicit Default dispatch), found {fallback_owners} "
            f"({recipe_defaults} Recipe, {dispatch_defaults} dispatch)"
        )

    for _, subcmd, _ in rows:
        if subcmd in RESERVED:
            errors.append(f"R-REC-03: reserved word used as subcommand: `{subcmd}`")
        if not KEBAB.match(subcmd):
            errors.append(f"R-REC-02: subcommand `{subcmd}` is not kebab-case / 2-20 chars")

    if len(rows) > MAX_RECIPES:
        msg = f"R-REC-04: {len(rows)} recipes exceeds recommended {MAX_RECIPES}"
        if skill in HUB_SKILLS:
            infos.append(f"{msg} (hub skill — recipe breadth by design)")
        elif len(rows) > WARN_RECIPES:
            warnings.append(f"{msg} and warn threshold {WARN_RECIPES} — consolidation review candidate")
        else:
            infos.append(f"{msg} (corpus norm band 8-{WARN_RECIPES})")

    subs = [s for _, s, _ in rows]
    dup = {s for s in subs if subs.count(s) > 1}
    if dup:
        errors.append(f"R-REC-02: duplicate subcommands within skill: {sorted(dup)}")

    return errors, warnings, infos


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", choices=("warning", "error", "strict"),
                        default="warning")
    parser.add_argument("--changed-only", action="store_true",
                        help="validate only skills whose SKILL.md changed vs HEAD")
    args = parser.parse_args()

    only = None
    if args.changed_only:
        only = changed_skill_names()
        if not only:
            print("no changed SKILL.md vs HEAD")
            return 0

    total = 0
    err_count = 0
    warn_count = 0
    info_count = 0
    skills_with_errors: list[str] = []

    for skill, path in iter_skills(only=only):
        total += 1
        errors, warnings, infos = validate(skill, path)
        if errors:
            skills_with_errors.append(skill)
            err_count += len(errors)
            print(f"[ERROR] {skill}")
            for e in errors:
                print(f"  - {e}")
        if warnings:
            warn_count += len(warnings)
            print(f"[WARN]  {skill}")
            for w in warnings:
                print(f"  - {w}")
        if infos and os.environ.get("VERBOSE"):
            info_count += len(infos)
            print(f"[INFO]  {skill}")
            for i in infos:
                print(f"  - {i}")

    print()
    print(f"Checked {total} skills | {err_count} errors | {warn_count} warnings | {info_count} infos (VERBOSE)")
    if skills_with_errors:
        print(f"Skills with errors: {len(skills_with_errors)}")

    if args.severity == "warning":
        return 0
    if args.severity == "error":
        return 1 if err_count else 0
    return 1 if (err_count or warn_count) else 0  # strict


if __name__ == "__main__":
    sys.exit(main())
