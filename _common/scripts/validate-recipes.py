#!/usr/bin/env python3
"""
Recipes / Subcommand Dispatch validator.

Validates every SKILL.md against the rules defined in `_common/RECIPES.md`:
  R-REC-01: Exactly one fallback owner per skill with Recipes: one Default Recipe
            (✓) or one explicit Default dispatch phase/workflow (ERROR)
  R-REC-02: Subcommand names are kebab-case, 2-20 chars (ERROR)
  R-REC-03: Reserved words (default/auto/help/list) unused (ERROR)
  R-REC-04: Recipe count, tiered (calibrated 2026-07-03 against 132-skill corpus):
            8-10 recipes → INFO (corpus norm band, ≤10 = P95);
            11+ recipes → WARNING (consolidation review candidate);
            hub skills (HUB_SKILLS) → always INFO (recipe breadth by design)
            reviewed skills (REC04_REVIEWED) → INFO while at or below the reviewed
            count; warns again if the count grows past it
  R-REC-05: Recipes section is RECOMMENDED for Tier 1-2 skills (INFO)

Plus heading integrity:
  H-REC-01: `## Subcommand Dispatch` heading exists alongside `## Recipes` (ERROR)
  H-REC-02: Heading is bare `## Subcommand Dispatch` — no parenthetical suffix (ERROR)

Usage:
  python3 _common/scripts/validate-recipes.py [--severity warning|error|strict]
                                              [--changed-only]  # skills with changed or new files

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

import _corpus
from _markdown import markdown_section
from _recipes import active_text, dispatch_allowlist, recipe_cells, recipe_section, registry_pointer

SKILLS_ROOT = Path(__file__).resolve().parents[2]
PROJECT_LOCAL_ROOT = SKILLS_ROOT / ".claude" / "skills"
SKIP_DIRS = {"_common", "_templates"}
RESERVED = {"default", "auto", "help", "list"}
KEBAB = re.compile(r"^(?=.{2,20}$)[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_RECIPES = 7  # recommended ceiling (scannability)
WARN_RECIPES = 10  # corpus P95 as of 2026-07-03 (125/132 skills ≤ 10); >10 warns
HUB_SKILLS = {"nexus"}  # ecosystem hub: routes 130+ agents, recipe breadth by design

# R-REC-04 reviewed exceptions. Each entry records a completed consolidation review:
# the recipe count at review time, and what the review found. The number is a
# ceiling, not a licence — a skill that grows past its reviewed count warns again,
# so the exception can never quietly cover recipes nobody looked at.
#
# What the 2026-08-20 review measured, per skill: how many recipes share an identical
# `Read First` set. A recipe with its own method reference is breadth (distinct
# activation conditions, each loading only what its task needs); recipes that collapse
# onto one reference and one activation condition are duplication. Only `tome` had the
# latter — four platform variants of `article`, folded back into it. In the rest, a
# shared reference covers a family of distinct triggers, which is the direction
# progressive disclosure wants.
#
# Complexity Budget (`_common/HARNESS_DEBT.md` 3b):
#   failure  — a standing warning nobody can act on trains readers to ignore R-REC-04,
#              and the review that cleared it lives in a commit message instead of the
#              checker
#   effect   — the review is recorded where the check runs, and is bounded by the count
#              it was performed against. Does NOT judge whether the recipes are the
#              right ones — only that the count is not duplication
#   owner    — gauge (it owns the checker suite)
#   removal  — delete an entry when its skill drops to WARN_RECIPES or below; delete the
#              table when no entry remains
REC04_REVIEWED = {
    "builder":  (20, "17 distinct Read First sets; 9 image recipes each carry their own pipeline reference"),
    "canon":    (24, "17 distinct Read First sets; one recipe per standard or legal-document type"),
    "chain":    (12, "7 references covering 12 distinct audit triggers, not 12 names for one audit"),
    "cue":      (17, "14 distinct Read First sets across script, capture, and delivery stages"),
    "launch":   (15, "14 distinct Read First sets; release, rollout, and reporting are separate triggers"),
    "native":   (16, "13 distinct Read First sets across two platforms and their store pipelines"),
    "saga":     (11, "6 references covering 11 narrative frameworks with distinct selection criteria"),
    "schema":   (11, "10 distinct Read First sets; design, migration, and tenancy do not share a method"),
    "scout":    (12, "12 distinct Read First sets — one reference per investigation technique"),
    "tome":     (12, "10 distinct Read First sets after folding note/zenn/qiita/devto into `article`"),
}


def changed_skill_names() -> set[str] | None:
    """Include changed registries and new skills; a git failure selects the full corpus."""
    try:
        changed = subprocess.run(
            ["git", "diff", "--name-only", "-z", "HEAD"],
            cwd=str(SKILLS_ROOT), check=True, capture_output=True, text=True,
        ).stdout.split("\0")
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard", "-z"],
            cwd=str(SKILLS_ROOT), check=True, capture_output=True, text=True,
        ).stdout.split("\0")
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"warning: cannot determine changed skills; validating all skills: {error}",
              file=sys.stderr)
        return None
    names = set()
    for value in changed + untracked:
        parts = Path(value).parts
        if len(parts) >= 4 and parts[:2] in ((".claude", "skills"), (".agents", "skills")):
            names.add(parts[2])
        elif len(parts) >= 2 and not parts[0].startswith(("_", ".")):
            names.add(parts[0])
    return names


def iter_skills(only: set[str] | None = None):
    roots = [SKILLS_ROOT]
    if PROJECT_LOCAL_ROOT.is_dir():
        roots.append(PROJECT_LOCAL_ROOT)
    entries = []
    for root in roots:
        for entry in root.iterdir():
            if entry.name in SKIP_DIRS or not _corpus.is_skill_dir(entry):
                continue
            if only is not None and entry.name not in only:
                continue
            skill_md = entry / "SKILL.md"
            if skill_md.is_file():
                entries.append((entry.name, skill_md))
    yield from sorted(entries, key=lambda item: item[0])


def extract_recipes_block(content: str, skill_dir=None) -> str | None:
    block = recipe_section(content)
    if block is None:
        return None
    # A skill whose Recipes table has outgrown the SKILL.md size ceiling may keep
    # the table in a sibling registry file and carry only a dispatch allowlist
    # here (`_common/RECIPES.md` "Externalized registry"). Follow the pointer so
    # the table is validated wherever it lives.
    if skill_dir is not None and not list(recipe_cells(block)):
        ptr = registry_pointer(block)
        if ptr:
            target = skill_dir / ptr
            if target.is_file():
                return target.read_text(encoding="utf-8")
    return block


def parse_rows(block: str, errors: list[str] | None = None):
    # Parse only the recipes table itself (header contains Recipe + Subcommand
    # columns). The Recipes section may also hold keyword-routing tables whose
    # second cell is a backtick-wrapped subcommand; parsing those produced
    # false-positive R-REC-02 duplicates and inflated R-REC-04 counts.
    rows = []
    for cells in recipe_cells(block):
        raw_subcmd = cells[1] if len(cells) >= 2 else ""
        m = re.fullmatch(r"`([^`]+)`", raw_subcmd)
        if m is None and errors is not None:
            errors.append(
                f"R-REC-02: Recipe {cells[0]!r} requires a nonempty, backtick-quoted subcommand"
            )
        subcmd = m.group(1) if m else raw_subcmd
        rows.append((cells[0], subcmd, cells[2] if len(cells) >= 3 else ""))
    return rows


def heading_issues(content: str) -> list[str]:
    issues = []
    content = active_text(content)
    has_recipes = recipe_section(content) is not None
    has_dispatch = markdown_section(content, "Subcommand Dispatch") is not None
    decorated = re.findall(r"^ {0,3}## Subcommand Dispatch[^\S\n]+(?!#+[ \t]*$)\S.*$",
                           content, re.MULTILINE)
    if has_recipes and not has_dispatch:
        issues.append("H-REC-01: `## Recipes` present but `## Subcommand Dispatch` missing")
    if decorated:
        issues.append(f"H-REC-02: decorated heading found (expected bare `## Subcommand Dispatch`): {decorated[0]!r}")
    return issues


def default_dispatches(content: str) -> list[str]:
    """Return valid explicit Default dispatch declarations from Subcommand Dispatch."""
    section = markdown_section(content, "Subcommand Dispatch")
    if section is None:
        return []
    return re.findall(
        r"^\*\*Default dispatch:\*\*\s*`((?:phase|workflow):[A-Za-z][A-Za-z0-9_-]*)`",
        active_text(section), re.MULTILINE,
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

    rows = parse_rows(block, errors)
    if not rows:
        errors.append("R-REC-01: `## Recipes` table has no rows")
        return errors, warnings, infos

    source_block = recipe_section(content)
    if source_block is not None and registry_pointer(source_block) and not list(recipe_cells(source_block)):
        allowlist = dispatch_allowlist(source_block)
        expected = {subcmd for _, subcmd, _ in rows}
        if allowlist is None:
            errors.append("R-REC-02: external Recipe registry requires a dispatch allowlist")
        else:
            actual = set(allowlist)
            if actual != expected:
                errors.append("R-REC-02: dispatch allowlist differs from Recipe registry "
                              f"(missing: {sorted(expected - actual)}, unknown: {sorted(actual - expected)})")
            if len(allowlist) != len(actual):
                errors.append("R-REC-02: duplicate subcommands in dispatch allowlist")
        declared = re.findall(r"Default Recipe:\s*`([^`]+)`", active_text(source_block))
        defaults = [subcmd for _, subcmd, default in rows if "✓" in default]
        if declared and declared != defaults:
            errors.append("R-REC-01: external registry Default Recipe declaration differs "
                          f"from its table (declared: {declared}, table: {defaults})")

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
        if not KEBAB.fullmatch(subcmd):
            errors.append(f"R-REC-02: subcommand `{subcmd}` is not kebab-case / 2-20 chars")

    if len(rows) > MAX_RECIPES:
        msg = f"R-REC-04: {len(rows)} recipes exceeds recommended {MAX_RECIPES}"
        reviewed = REC04_REVIEWED.get(skill)
        if skill in HUB_SKILLS:
            infos.append(f"{msg} (hub skill — recipe breadth by design)")
        elif reviewed and len(rows) <= reviewed[0]:
            infos.append(f"{msg} (reviewed {reviewed[0]} — {reviewed[1]}, see REC04_REVIEWED)")
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
                        help="validate skills with changed or new files, including Recipe registries")
    args = parser.parse_args()

    only = None
    if args.changed_only:
        only = changed_skill_names()
        if only == set():
            print("no changed skill files vs HEAD")
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
