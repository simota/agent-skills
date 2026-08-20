"""Corpus boundary — which skill directories this repository owns and audits.

Every checker in this directory enumerates skills, and each one grew its own
predicate. They disagreed: the same tree counted as 115, 116, and 118 skills
depending on which script asked, because none of them distinguished a skill
this repository authors from one merely *linked into* the skills root.

A skill directory that is a symlink points at a separate repository with its
own owner, its own git history, and its own shared protocols. Auditing it here
produces findings nobody can act on: it is not in this repo's `.gitignore`d
tree by accident, and a routing surface for it would describe a router it does
not use. Externally-owned skills are enumerated only when a caller explicitly
asks for them.

Complexity Budget (`_common/HARNESS_DEBT.md` 3b):
  failure  — checkers reporting findings against skills this repo cannot change,
             and disagreeing on the corpus size while doing it
  effect   — one predicate, five call sites; corpus totals become explainable
             as owned + project-local. Does NOT detect an external skill copied
             in as a real directory; only linked ones are recognized
  owner    — gauge (it owns the checker suite)
  removal  — delete when no external skill set is linked into the skills root,
             i.e. when `external_skill_dirs()` returns empty on a fresh checkout
"""

from __future__ import annotations

import pathlib

#: Directories that never hold an auditable skill, regardless of contents.
INFRA_DIRS = frozenset({
    ".git", "node_modules", ".agents", ".archive",
    "_common", "_loops", "_prompts", "_templates",
})


def is_external(entry: pathlib.Path) -> bool:
    """True when `entry` is a skill directory owned by another repository.

    The signal is the symlink: this repo's own skills are real directories,
    and linked-in skill sets are `.gitignore`d precisely because they are not
    ours to version. Verified against `git check-ignore` at the time of writing.
    """
    return entry.is_symlink()


def is_skill_dir(entry: pathlib.Path, *, include_external: bool = False) -> bool:
    """True when `entry` is a skill directory this repository should audit."""
    if not entry.is_dir() or entry.name.startswith(".") or entry.name in INFRA_DIRS:
        return False
    if not (entry / "SKILL.md").is_file():
        return False
    return include_external or not is_external(entry)


def iter_skill_dirs(root: pathlib.Path, *, include_external: bool = False):
    """Yield the skill directories under `root`, sorted by name."""
    for entry in sorted(root.iterdir()):
        if is_skill_dir(entry, include_external=include_external):
            yield entry


def external_skill_dirs(root: pathlib.Path) -> list[pathlib.Path]:
    """The linked-in skill sets under `root` — reported, never audited."""
    return [
        entry
        for entry in sorted(root.iterdir())
        if entry.is_dir() and is_external(entry) and (entry / "SKILL.md").is_file()
    ]
